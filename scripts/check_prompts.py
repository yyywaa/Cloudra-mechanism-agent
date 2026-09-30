"""提示词静态检查（评审 5.9）：职责边界 + 无正则的失效引用扫描 + token 账。

检查面（全部为显式 token 扫描，**无正则**）：

1. **引用存在性**：prompts/*.md 与 skills/**/SKILL.md 里凡是「看起来像工具名」的
   反引号 token（≥4 字符、含下划线、纯 [a-z0-9_]），必须能在 `ToolRegistration`
   的 tool_name 集合里找到，或在 `_NON_TOOL_TOKENS` 显式白名单里（每项都要写理由）。
2. **角色可见性**：角色提示词（`cloudra/prompts/<role>.md`）里引用的**已注册工具**
   必须对该角色可见（使用现有 role_allowlist 投影）。
3. **名册单一事实源**：launcher/swarm 的「Available sub-agents」段必须等于从
   `RoleProfile` 生成的名册；prompts/skills 里不得再出现手写名册行
   （`| a-1 |` … 与 `| **a-1** |` … 的逐字模式）。
4. **关键枚举/默认值**：README/README_CN/AGENTS 里 `invocation_protocol:` 与
   `orchestration_mode:` 后跟的取值必须是 schema 枚举的合法值；schema 默认
   invocation_protocol 必须是 javascript（评审 5.1 的漂移类别）。
5. **token 账**：每个 prompt source 的 token 数（TokenEstimator；取不到真编码时
   降级为估算并标 `~`），降序打印——结合 telemetry 决定是否需要精简。

退出码：0 = 无违规；1 = 有违规（逐条打印）。
用法：`uv run python scripts/check_prompts.py`（CI 亦调用；pytest 外壳见
tests/test_prompt_static_checks.py）。
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:  # 直跑脚本时也能 import cloudra
    sys.path.insert(0, str(REPO_ROOT))

from cloudra.runtime_v2.roles import RoleRegistry  # noqa: E402
from cloudra.runtime_v2.schemas import (  # noqa: E402
    InvocationProtocol,
    OrchestrationMode,
    RuntimeSettings,
)
from cloudra.tools.capabilities import role_hidden_tools  # noqa: E402
from cloudra.tools.registry import TOOL_REGISTRY  # noqa: E402

_BACKTICK = "`"
_NAME_CHARS = frozenset("abcdefghijklmnopqrstuvwxyz0123456789_")
from cloudra.base.role_identity import LEGACY_AGENT_ID_BY_ROLE  # noqa: E402

_LEGACY_IDS = tuple(LEGACY_AGENT_ID_BY_ROLE.values())
_ROSTER_ROW_MARKERS = tuple(f"| {legacy} |" for legacy in _LEGACY_IDS) + tuple(
    f"| **{legacy}** |" for legacy in _LEGACY_IDS
)

# 函数参数列表位置出现但**确定不是参数**的 token：逐一给理由；新增前先自问「它真的不是参数吗」。
_NON_PARAM_TOKENS: dict[str, str] = {
    "summary": "部分工具把 summary 收进参数，但文档里常作业务词用；保留宽容度",
}

# 反引号里出现但**不是工具名**的 token：逐一给理由；新增前先自问「它真的是工具吗」。
_NON_TOOL_TOKENS: dict[str, str] = {
    "add_adsorbate": "ASE 的 API，不是本仓工具",
    "agent_id": "subagent_launcher/swarm 的参数名",
    "atom_map": "参数名（reaction_mapping 输入）",
    "call_verdict": "dag_review_call 的裁决取值",
    "check_command": "参数名",
    "dag_verified": "delivery_report 的确定性支持状态",
    "supervisor_supported": "delivery_report 的督导支持状态",
    "effective_windows": "conformer_search 的输出字段",
    "dag_guided": "OrchestrationMode 取值",
    "dag_message": "dag_message_supervisor 的消息字段名",
    "dag_record": "OrchestrationMode 取值",
    "delay_seconds": "schedule/reminders 参数名",
    "distance_filters": "conformer_search 参数名",
    "draft_verdict": "dag_review_* 的裁决取值",
    "imaginary_modes": "参数名（频率校验）",
    "internal_generated": "internal_coordinates 参数取值",
    "interval_seconds": "schedule 参数名",
    "irc_log": "产物文件名（IRC 日志）",
    "log_path": "参数名",
    "max_concurrency": "subagent_swarm 参数名",
    "mechanism_proposed": "DAG 草稿状态取值",
    "needs_evidence": "裁决取值（要求补证据）",
    "not_applicable": "裁决取值",
    "prompt_template": "subagent_swarm 参数名",
    "reaction_center": "参数名",
    "replace_group": "参数名（结构编辑）",
    "review_decision": "supervisor_access 取值 / 裁决类别",
    "scan_parse": "ts_prepare 参数取值（片段解析策略）",
    "short_irc": "参数取值（短程 IRC）",
    "small_mol": "角色 id（不是工具名）",
    "solvent_smiles": "参数名",
    "stage_kind": "DAG 阶段字段名",
    "submit_approval_decision": "参数名（提交裁决）",
    "timeout_seconds": "参数名",
    "to_agent": "agent_hub 参数名",
    "ts_log": "产物文件名（TS 日志）",
    "ts_opt": "参数取值（TS 优化）",
    "watch_pairs": "参数名（监控原子对）",
}


def _tool_params(tool: str) -> set[str]:
    """该工具 ``input_schema`` 的字段名集合（schema 是唯一事实源）。

    未注册工具由引用检查报告；注册工具的 schema 导入失败必须显式报错，
    不能把无法检查误报为参数有效。
    """
    import importlib

    from cloudra.base.tools_class import input_schema as input_schema_base

    entry = next(
        (reg for reg in TOOL_REGISTRY if (reg.tool_name or reg.class_name) == tool),
        None,
    )
    if entry is None:
        return set()
    try:
        module = importlib.import_module(entry.module)
    except ImportError as exc:
        raise ImportError(
            f"cannot inspect input schema for {tool!r} ({entry.module})"
        ) from exc
    params: set[str] = set()
    for value in vars(module).values():
        if not (isinstance(value, type) and issubclass(value, input_schema_base)):
            continue
        if value is input_schema_base:
            continue
        for field_name, field in (getattr(value, "model_fields", {}) or {}).items():
            params.add(field_name)
            alias = getattr(field, "alias", None)
            if alias:
                params.add(str(alias))
    return params


_ALL_PARAMS: set[str] | None = None


def _all_param_tokens() -> set[str]:
    """全部注册工具的参数名并集（含别名）：反引号里的参数名不该被误判成工具名。"""
    global _ALL_PARAMS
    if _ALL_PARAMS is None:
        params: set[str] = set()
        for name in _tool_names():
            params |= _tool_params(name)
        _ALL_PARAMS = params
    return _ALL_PARAMS


def _is_snake(token: str) -> bool:
    return len(token) >= 3 and all(ch.islower() or ch.isdigit() or ch == "_" for ch in token)


def _paren_groups(text: str) -> list[str]:
    groups: list[str] = []
    depth = 0
    start = 0
    for index, ch in enumerate(text):
        if ch == "(":
            if depth == 0:
                start = index + 1
            depth += 1
        elif ch == ")" and depth:
            depth -= 1
            if depth == 0:
                groups.append(text[start:index])
    return groups


def _param_problems(text: str, rel: str) -> list[str]:
    """工具所在行的括号组里若含已知参数名，则组内其余 snake_case token 也必须是参数名。

    门槛（组内至少含一个该工具的真实参数名）用来避开普通括号散文与枚举清单
    （如 verdict 取值）；命中而非参数的 token 走 ``_NON_PARAM_TOKENS`` 带理由豁免。
    """
    problems: list[str] = []
    tools = _tool_names()
    for line_no, line in enumerate(text.splitlines(), start=1):
        mentioned = {tool for tool in tools if f"`{tool}`" in line}
        if len(mentioned) != 1:
            continue
        tool = mentioned.pop()
        params = _tool_params(tool)
        if not params:
            continue
        for group in _paren_groups(line):
            tokens = [token for token in _backticked(group) if _is_snake(token)]
            if not any(token in params for token in tokens):
                continue
            for token in tokens:
                if token in params or token in _NON_PARAM_TOKENS:
                    continue
                problems.append(
                    f"{rel}:{line_no}: `{token}` 出现在 `{tool}` 的参数列表里，"
                    f"但不是它的参数名"
                )
    return problems


def check_tool_param_names() -> list[str]:
    problems: list[str] = []
    for path in _prompt_files():
        problems += _param_problems(path.read_text(encoding="utf-8"), _rel(path))
    return problems


def _tool_names() -> set[str]:
    return {reg.tool_name for reg in TOOL_REGISTRY if reg.tool_name}


def _backticked(text: str) -> list[str]:
    parts = text.split(_BACKTICK)
    return [parts[i].strip() for i in range(1, len(parts), 2)]


def _looks_like_tool(token: str) -> bool:
    return len(token) >= 4 and "_" in token and all(ch in _NAME_CHARS for ch in token)


def _prompt_files() -> list[Path]:
    files = sorted((REPO_ROOT / "cloudra" / "prompts").glob("*.md"))
    files += sorted((REPO_ROOT / "cloudra" / "skills").glob("*/SKILL.md"))
    return files


def _rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT)).replace("\\", "/")


def check_references() -> list[str]:
    names = _tool_names()
    problems: list[str] = []
    for path in _prompt_files():
        for token in _backticked(path.read_text(encoding="utf-8")):
            if not _looks_like_tool(token):
                continue
            if token in names or token in _NON_TOOL_TOKENS:
                continue
            if token in _all_param_tokens():
                continue
            problems.append(
                f"{_rel(path)}: 引用 `{token}` 不是注册工具（也不是白名单非工具 token）"
            )
    return problems


def check_role_visibility() -> list[str]:
    names = _tool_names()
    registry = RoleRegistry()
    problems: list[str] = []
    for path in sorted((REPO_ROOT / "cloudra" / "prompts").glob("*.md")):
        role = registry.get(path.stem)
        if role is None:
            continue  # yolo_guard 等非角色提示词
        for token in _backticked(path.read_text(encoding="utf-8")):
            if token not in names:
                continue
            if token in role_hidden_tools(role.role_id):
                problems.append(
                    f"{path.stem}.md: 引用 `{token}`，但 role_allowlist 对该角色不可见"
                )
    return problems


# 名册的唯一生成点是 roles.dispatch_roster；这里只做重命名导入（勿再实现一份）。
from cloudra.runtime_v2.roles import dispatch_roster as generated_roster  # noqa: E402


def check_roster_single_source() -> list[str]:
    problems: list[str] = []
    expected = generated_roster()
    from cloudra.tools.Managetool import subagent_launcher, subagent_swarm

    for name, module in (
        ("subagent_launcher", subagent_launcher),
        ("subagent_swarm", subagent_swarm),
    ):
        if expected not in module.description:
            problems.append(f"{name}: 「Available sub-agents」段与 RoleProfile 生成的名册不一致")
    for path in _prompt_files():
        text = path.read_text(encoding="utf-8")
        for marker in _ROSTER_ROW_MARKERS:
            if marker in text:
                problems.append(f"{_rel(path)}: 出现手写名册行 {marker!r}（应引用生成名册）")
    return problems


def check_doc_enums() -> list[str]:
    problems: list[str] = []
    enums = {
        "invocation_protocol": {p.value for p in InvocationProtocol},
        "orchestration_mode": {m.value for m in OrchestrationMode},
    }
    for name in ("README.md", "README_CN.md", "AGENTS.md"):
        path = REPO_ROOT / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for key, values in enums.items():
            marker = f"{key}:"
            start = 0
            while True:
                index = text.find(marker, start)
                if index == -1:
                    break
                start = index + len(marker)
                token = ""
                for ch in text[start : start + 40]:
                    if ch in _NAME_CHARS:
                        token += ch
                    elif token:
                        break
                if token and token not in values:
                    problems.append(
                        f"{name}: `{key}:` 后的取值 `{token}` 不是合法枚举值 {sorted(values)}"
                    )
    default_protocol = RuntimeSettings.model_fields["invocation_protocol"].default
    if InvocationProtocol(default_protocol).value != "javascript":
        problems.append("schema 默认 invocation_protocol 不是 javascript（评审 5.1 的漂移类别）")
    return problems


def token_table() -> list[str]:
    from cloudra.infra.token_estimator import TokenEstimator

    def count(text: str) -> str:
        try:
            return f"{TokenEstimator.count_text(text):>7}"
        except Exception:  # noqa: BLE001 —— 真编码不可用时降级为估算，标 ~
            return f"~{TokenEstimator.estimate_text(text):>6}"

    rows: list[tuple[str, str]] = []
    for path in _prompt_files():
        rows.append((_rel(path), count(path.read_text(encoding="utf-8"))))
    from cloudra.tools.Managetool import subagent_launcher, subagent_swarm

    rows.append(("tools/subagent_launcher.description", count(subagent_launcher.description)))
    rows.append(("tools/subagent_swarm.description", count(subagent_swarm.description)))
    rows.sort(key=lambda row: int(row[1].strip("~ ")), reverse=True)
    return [f"{size}  {name}" for name, size in rows]


def run_checks() -> tuple[list[str], list[str]]:
    problems: list[str] = []
    problems += check_references()
    problems += check_role_visibility()
    problems += check_roster_single_source()
    problems += check_doc_enums()
    problems += check_tool_param_names()
    return problems, token_table()


def main(argv: list[str] | None = None) -> int:
    problems, tokens = run_checks()
    print("== prompt source token 账（降序）==")
    for line in tokens:
        print("  " + line)
    if problems:
        print("\n== 违规 ==")
        for problem in problems:
            print("  - " + problem)
        return 1
    print("\nOK: 无违规")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
