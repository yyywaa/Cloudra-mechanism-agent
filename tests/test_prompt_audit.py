"""提示词静态检查的常驻守卫（评审 5.9）。

两件事：

1. **现状必须干净**：`scripts/prompt_audit.py` 的检查在真实提示词/技能上不得有
   违规——它同时守着「工具改名后提示词里的陈旧引用」「角色 prompt 引用了对该
   角色不可见的工具」「launcher/swarm/skill 各自手抄 a-N 花名册」三件事。
2. **检查有判别力**：造几个假提示词，确认它确实会红（变异校验），否则它会退化成
   一个永远绿的摆设。
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import prompt_audit as audit  # noqa: E402


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_real_prompts_and_skills_pass_the_audit():
    violations, tokens = audit.run_checks()
    assert violations == [], "\n".join(str(item) for item in violations)
    assert tokens, "token 报告不应为空（它是对照压缩成本的输入）"


def test_audit_flags_stale_tool_names(tmp_path, monkeypatch):
    """变异校验：陈旧/打错的工具名必须被指出（否则检查没有判别力）。"""
    prompts = tmp_path / "prompts"
    _write(
        prompts / "coordinator.md",
        "Call `dag_remove_nodes` to drop a node, and `browse` to read the web.\n",
    )
    monkeypatch.setattr(audit, "PROMPTS_DIR", prompts)
    monkeypatch.setattr(audit, "SKILLS_DIR", tmp_path / "skills")
    violations, _tokens = audit.run_checks()
    kinds = {item.kind for item in violations}
    assert "stale-tool-name" in kinds or "unknown-reference" in kinds
    detail = " ".join(item.detail for item in violations)
    assert "dag_remove_nodes" in detail and "browse" in detail


def test_audit_flags_tools_invisible_to_the_role(tmp_path, monkeypatch):
    """角色 prompt 引用对该角色不可见的工具 → 违规（role allowlist 为准）。"""
    prompts = tmp_path / "prompts"
    _write(prompts / "writer.md", "Load `ir_processor` and then `get_skill`.\n")
    monkeypatch.setattr(audit, "PROMPTS_DIR", prompts)
    monkeypatch.setattr(audit, "SKILLS_DIR", tmp_path / "skills")
    violations, _tokens = audit.run_checks()
    assert any(item.kind == "role-invisible-tool" for item in violations), violations


def test_audit_flags_hand_written_roster(tmp_path, monkeypatch):
    """手抄 a-N 花名册 → 违规（唯一映射表在 base/role_identity.py）。"""
    prompts = tmp_path / "prompts"
    _write(
        prompts / "coordinator.md",
        "| a-1 | explorer |\n| a-4 | small_mol |\n",
    )
    monkeypatch.setattr(audit, "PROMPTS_DIR", prompts)
    monkeypatch.setattr(audit, "SKILLS_DIR", tmp_path / "skills")
    violations, _tokens = audit.run_checks()
    assert any(item.kind == "hand-written-roster" for item in violations), violations


def test_output_only_roles_come_from_role_profiles():
    """纯输出型角色分类的唯一事实源是 RoleProfile（不再有第二张角色表）。"""
    from cloudra.infra.config import _reset_for_tests  # noqa: F401  (导入顺序无关)
    from cloudra.runtime.prompt_assembler import is_output_only_role
    from cloudra.runtime_v2.roles import BUILTIN_ROLES

    expected = {"explorer", "writer", "researcher", "experiment"}
    assert {role.role_id for role in BUILTIN_ROLES if role.output_only} == expected
    for role in BUILTIN_ROLES:
        assert is_output_only_role(role.role_id) is role.output_only
    # 自定义 prompt 名（无对应 RoleProfile）按"非纯输出"处理。
    assert is_output_only_role("my-custom-prompt") is False
    assert is_output_only_role(None) is False


def test_dispatch_roster_is_generated_from_role_profiles():
    """launcher/swarm 的花名册来自 RoleProfile，且不再出现 a-N 字面量。"""
    from cloudra.runtime_v2.roles import BUILTIN_ROLES
    from cloudra.tools.Managetool._roster import (
        dispatchable_roles,
        subagent_roster_text,
    )
    from cloudra.tools.Managetool.subagent_launcher import description as launcher_desc
    from cloudra.tools.Managetool.subagent_swarm import description as swarm_desc

    expected_ids = [role.role_id for role in BUILTIN_ROLES if role.role_id not in {"coordinator", "supervisor"}]
    assert [role.role_id for role in dispatchable_roles()] == expected_ids
    for role_id in expected_ids:
        assert role_id in subagent_roster_text()
        assert role_id in launcher_desc
        assert role_id in swarm_desc
    for description in (launcher_desc, swarm_desc):
        assert "a-1" not in description and "a-8" not in description


def test_audit_script_runs_standalone_as_json():
    """脚本入口可直接跑（CI 用途）：退出码 0 + 可解析 JSON。"""
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "prompt_audit.py"), "--json"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=300,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["violations"] == []
    assert payload["prompt_tokens"], "应报告每个 prompt 源的 token 估计"
