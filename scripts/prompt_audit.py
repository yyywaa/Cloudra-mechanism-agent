"""提示词静态检查（评审 5.9）：**无正则**，纯词表比对与 pydantic 内省。

内容归属（与 AGENTS.md「提示词与内容归属」一致，越界即漂移之源）：

| 内容 | 归属 |
| :--- | :--- |
| 不可违反的运行不变量 | runtime / policy stage |
| 参数、结果、失败语义、工具局部流程 | tool schema 与 description |
| 角色使命、交付格式、领域边界 | role prompt |
| 可长按需加载的 SOP | skill |
| 仓库级开发与用户指令 | AGENTS.md |
| 派发协议（不复制完整角色手册） | launcher / swarm 工具描述 |

用法::

    uv run python scripts/prompt_audit.py            # 检查 + 打印 token 用量（违规退出 1）
    uv run python scripts/prompt_audit.py --tokens   # 只看 token 用量
    uv run python scripts/prompt_audit.py --json     # 机器可读（供 CI/telemetry 比对）

检查项：

1. 反引号标识符的**失效工具引用**（提示词会合法地写外部引擎命令、参数值与散文，
   所以不搞"每个反引号都必须是代码"的规矩——那种检查只会被噪声关掉）：

   - **疑似陈旧工具名**：不在词表内、但与某个注册工具名高度相近（``difflib``
     相似度 ≥ 0.85，无正则）——改名/打错时会逐条显形（``dag_remove_nodes`` →
     ``dag_remove_node``）；
   - **挂已知工具家族前缀却不是工具**：``dag_``/``submit_`` 等前缀 token 必须在
     注册表里（外部引擎命令 ``gmx``/``vina`` 不受影响）；
   - **角色 prompt 引用对该角色不可见的工具**：以 registry 的 role allowlist 为准。
2. 角色 prompt 里提到的工具必须**对该角色可见**（registry 的 role allowlist）。
3. 不得手写 a-N 花名册：唯一映射表在 ``cloudra/base/role_identity.py``。
4. 打印每个 prompt 源的 token 估计（口径 = ``infra/token_estimator.py`` 单一事实源），
   供与 telemetry 的压缩成本对照后决定精简谁。
"""

from __future__ import annotations

import argparse
import difflib
import enum
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROMPTS_DIR = ROOT / "cloudra" / "prompts"
SKILLS_DIR = ROOT / "cloudra" / "skills"
def roster_scan_dirs() -> tuple[Path, ...]:
    """花名册检查的扫描面：角色 prompt、技能包、派发工具所在目录。"""
    return (PROMPTS_DIR, SKILLS_DIR, ROOT / "cloudra" / "tools" / "Managetool")


class Violation:
    def __init__(self, kind: str, where: str, detail: str) -> None:
        self.kind = kind
        self.where = where
        self.detail = detail

    def to_dict(self) -> dict[str, str]:
        return {"kind": self.kind, "where": self.where, "detail": self.detail}

    def __str__(self) -> str:
        return f"[{self.kind}] {self.where}: {self.detail}"


# ------------------------------------------------------------------ 词表构造


def _enum_literals() -> set[str]:
    """运行时枚举字面量：编排模式、agent 状态、失败分类、DAG actor/阶段/裁决等。"""
    from cloudra.dag import models as dag_models
    from cloudra.runtime_v2 import failures as failure_mod
    from cloudra.runtime_v2 import schemas as schema_mod

    words: set[str] = set()
    for module in (schema_mod, failure_mod, dag_models):
        for value in vars(module).values():
            if isinstance(value, type) and issubclass(value, enum.Enum):
                for member in value:
                    if isinstance(member.value, str):
                        words.add(member.value)
    return words


def _schema_vocabulary(model: Any, seen: set[Any] | None = None) -> set[str]:
    """递归收集 pydantic 模型的字段名、枚举/Literal 字面量与别名（确定性内省）。"""
    if model is None:
        return set()
    seen = seen if seen is not None else set()
    if model in seen:
        return set()
    seen.add(model)
    fields = getattr(model, "model_fields", None)
    if not isinstance(fields, dict):
        return set()
    words: set[str] = set()
    for name, field in fields.items():
        words.add(name)
        alias = getattr(field, "alias", None)
        if isinstance(alias, str) and alias:
            words.add(alias)
        annotation = getattr(field, "annotation", None)
        words |= _annotation_vocabulary(annotation, seen)
    return words


def _annotation_vocabulary(annotation: Any, seen: set[Any]) -> set[str]:
    if annotation is None:
        return set()
    if isinstance(annotation, type) and issubclass(annotation, enum.Enum):
        return {member.value for member in annotation if isinstance(member.value, str)}
    if hasattr(annotation, "model_fields"):
        return _schema_vocabulary(annotation, seen)
    args = getattr(annotation, "__args__", ())
    words: set[str] = set()
    for arg in args:
        if isinstance(arg, str):
            words.add(arg)
        elif isinstance(arg, type) and issubclass(arg, enum.Enum):
            words.update(m.value for m in arg if isinstance(m.value, str))
        else:
            words |= _annotation_vocabulary(arg, seen)
    return words


def tool_names() -> set[str]:
    from cloudra.tools import get_tools_lst

    return {entry.tool_name for entry in get_tools_lst() if entry.tool_name}


def tool_families() -> set[str]:
    """工具家族前缀：``dag_view`` -> ``dag``（用于 skill 侧的高信号失效引用检查）。"""
    return {name.split("_")[0] for name in tool_names() if "_" in name}


def hidden_tools_for(role_id: str) -> set[str]:
    from cloudra.tools.capabilities import role_hidden_tools

    return set(role_hidden_tools(role_id))


#: yolo 审批官的 function-tool 名（提示词会引用它，但它不是 registry 工具）。
GUARD_TOOL_NAMES = frozenset({"submit_approval_decision"})


def guard_tool_names() -> set[str]:
    """审批官工具名：直接取 ``yolo_guard`` 里声明的 function schema name。"""
    from cloudra.infra import yolo_guard

    names = set(GUARD_TOOL_NAMES)
    source = yolo_guard.__dict__.get("YOLO_DECISION_TOOL_NAME")
    if isinstance(source, str) and source:
        names.add(source)
    return names


def build_vocabulary() -> set[str]:
    from cloudra.runtime_v2.roles import BUILTIN_ROLES
    from cloudra.tools import get_tools_lst

    words = tool_names()
    for entry in get_tools_lst():
        words |= _schema_vocabulary(getattr(entry, "input_schema", None))
        words |= _schema_vocabulary(getattr(entry, "output_schema", None))
    words |= _enum_literals()
    words |= {role.role_id for role in BUILTIN_ROLES}
    if SKILLS_DIR.is_dir():
        words |= {path.name for path in SKILLS_DIR.iterdir() if path.is_dir()}
    words |= guard_tool_names()
    # 常见的运行时固定话术/字段（非工具名，但会出现在提示词里）
    words |= {
        "HANDOFF",
        "MEMORY",
        "AGENTS",
        "README",
        "stop",
        "read",
        "write",
        "bash",
        "ask_user",
        "js_exec",
        "text",
    }
    return words


# ------------------------------------------------------------------ 文本扫描


def code_spans(text: str) -> list[tuple[int, str]]:
    """提取行内反引号片段（跳过 ``` 围栏块），返回 (行号, 内容)。"""
    spans: list[tuple[int, str]] = []
    in_fence = False
    for lineno, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        parts = line.split("`")
        for index in range(1, len(parts), 2):
            spans.append((lineno, parts[index]))
    return spans


def _is_identifier(token: str) -> bool:
    if not token or token != token.lower():
        return False
    if not (token[0].isalpha() or token[0] == "_"):
        return False
    return all(char.isalnum() or char == "_" for char in token)


def identifier_tokens(spans: list[tuple[int, str]]) -> list[tuple[int, str]]:
    return [(lineno, token) for lineno, raw in spans for token in raw.split() if _is_identifier(token)]


def a_n_ids(text: str) -> set[str]:
    """文本里出现的 a-N 形式 id（花名册检测；唯一映射表只允许在 role_identity）。"""
    found: set[str] = set()
    for _lineno, token in identifier_tokens(code_spans(text)):
        if len(token) >= 3 and token.startswith("a-") and token[2:].isdigit():
            found.add(token)
    for line in text.splitlines():
        for word in line.replace(",", " ").replace("|", " ").split():
            candidate = word.strip("`.,;:()[]")
            if len(candidate) >= 3 and candidate.startswith("a-") and candidate[2:].isdigit():
                found.add(candidate)
    return found


# ------------------------------------------------------------------ 检查


def _label(path: Path) -> str:
    """报告里用的相对路径；被测目录被替换到仓库外时退化为绝对路径。"""
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def _prompt_files() -> list[Path]:
    files = sorted(PROMPTS_DIR.glob("*.md")) if PROMPTS_DIR.is_dir() else []
    if SKILLS_DIR.is_dir():
        files += sorted(SKILLS_DIR.rglob("SKILL.md"))
    return files


def run_checks() -> tuple[list[Violation], list[tuple[str, int]]]:
    vocabulary = build_vocabulary()
    violations: list[Violation] = []
    token_report: list[tuple[str, int]] = []

    families = tool_families()
    names = tool_names()
    for path in _prompt_files():
        rel = _label(path)
        text = path.read_text(encoding="utf-8")
        role_prompt = path.parent == PROMPTS_DIR
        role_id = path.stem if role_prompt else ""
        hidden = hidden_tools_for(role_id) if role_prompt else set()
        for lineno, token in identifier_tokens(code_spans(text)):
            if token in vocabulary:
                # 已知词表内的东西：只有"工具对该角色不可见"值得报。
                if token in names and token in hidden:
                    violations.append(
                        Violation(
                            "role-invisible-tool",
                            f"{rel}:{lineno}",
                            f"角色 {role_id} 引用了对它不可见的工具 `{token}`",
                        )
                    )
                continue
            if token.split("_")[0] in families:
                violations.append(
                    Violation(
                        "unknown-reference",
                        f"{rel}:{lineno}",
                        f"`{token}` 带已知工具家族前缀但不是注册工具（疑似陈旧引用）",
                    )
                )
                continue
            near = difflib.get_close_matches(token, sorted(names), n=1, cutoff=0.85)
            if near:
                violations.append(
                    Violation(
                        "stale-tool-name",
                        f"{rel}:{lineno}",
                        f"`{token}` 不在注册表里，最接近的工具是 `{near[0]}`（改名残留？）",
                    )
                )
        token_report.append((rel, _estimate_tokens(text)))

    for directory in roster_scan_dirs():
        if not directory.exists():
            continue
        for path in sorted(directory.rglob("*.md")) + sorted(directory.rglob("*.py")):
            rel = _label(path)
            if "role_identity" in rel:
                continue
            found = a_n_ids(path.read_text(encoding="utf-8"))
            if len(found) >= 2:
                violations.append(
                    Violation(
                        "hand-written-roster",
                        rel,
                        f"出现多个 a-N id {sorted(found)}；花名册唯一映射表在 base/role_identity.py",
                    )
                )
    return violations, token_report


def _estimate_tokens(text: str) -> int:
    try:
        from cloudra.infra.token_estimator import TokenEstimator

        return TokenEstimator().count_text(text)
    except Exception:
        return len(text) // 4


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="提示词静态检查（评审 5.9）")
    parser.add_argument("--tokens", action="store_true", help="只打印 token 用量")
    parser.add_argument("--json", action="store_true", help="机器可读输出")
    args = parser.parse_args(argv)

    violations, token_report = run_checks()
    if args.json:
        print(
            json.dumps(
                {
                    "violations": [item.to_dict() for item in violations],
                    "prompt_tokens": [{"source": src, "tokens": n} for src, n in token_report],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1 if violations else 0

    if not args.tokens:
        for violation in violations:
            print(f"VIOLATION {violation}")
    total = sum(n for _src, n in token_report)
    print(f"\nprompt sources: {len(token_report)}  估算 tokens 合计: {total}")
    for src, count in token_report:
        print(f"  {count:>7}  {src}")
    if violations and not args.tokens:
        print(f"\n共 {len(violations)} 处违规（不变量：提示词引用必须仍然存在且对该角色可见）")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
