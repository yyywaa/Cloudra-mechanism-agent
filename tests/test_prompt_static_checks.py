"""提示词静态检查（评审 5.9）的 pytest 外壳：检查脚本必须零违规。"""

from __future__ import annotations

from scripts.check_prompts import (
    generated_roster,
    run_checks,
)


def test_prompt_static_checks_report_no_violations():
    problems, tokens = run_checks()
    assert problems == [], "\n".join(problems)
    assert tokens, "token 账不能为空"


def test_roster_is_generated_from_role_profiles():
    from cloudra.runtime_v2.roles import RoleRegistry
    from cloudra.tools.Managetool import subagent_launcher, subagent_swarm

    roster = generated_roster()
    assert roster.count("(") == 8, roster
    assert "1. explorer (a-1):" in roster
    assert "(a-0):" not in roster, "coordinator 是派发者，不在名册里"
    assert roster in subagent_launcher.description
    assert roster in subagent_swarm.description
    for role in RoleRegistry().list():
        if not role.roster:
            continue
        assert role.roster, f"{role.role_id} 缺 roster：名册无法生成"
        assert f"({role.legacy_agent_id}):" in roster


def test_output_only_roles_derive_from_role_profile():
    from cloudra.runtime.prompt_assembler import _output_only_roles
    from cloudra.runtime_v2.roles import RoleRegistry

    expected = frozenset(
        role.role_id for role in RoleRegistry().list() if role.output_only
    )
    assert expected == frozenset({"explorer", "writer", "researcher", "experiment"})
    assert _output_only_roles() == expected


def test_tool_param_lists_must_match_schema():
    from scripts.check_prompts import _param_problems

    stale = "- `dag_submit_step_evidence`: submit (`ts_file`, `ts_log`, optional `irc_log`).\n"
    fixed = "- `dag_submit_step_evidence`: submit (`step_name`, `ts_file`, optional `irc_file`).\n"
    assert _param_problems(stale, "x.md"), "陈旧参数名必须被检出"
    assert not _param_problems(fixed, "x.md")


def test_agent_hub_is_visible_to_every_builtin_role():
    from cloudra.runtime_v2.roles import RoleRegistry
    from cloudra.tools.capabilities import role_hidden_tools

    for role in RoleRegistry().list():
        assert "agent_hub" not in role_hidden_tools(role.role_id)


def test_schema_import_failure_cannot_hide_invalid_parameters(monkeypatch):
    import importlib

    import pytest

    from scripts.check_prompts import _param_problems

    original = importlib.import_module

    def unavailable(name, **kwargs):
        if name.endswith('.dag_submit_step_evidence'):
            raise ImportError('schema import unavailable')
        return original(name, **kwargs)

    monkeypatch.setattr(importlib, 'import_module', unavailable)
    with pytest.raises(ImportError, match='dag_submit_step_evidence'):
        _param_problems('- `dag_submit_step_evidence`: (`ts_file`, `ts_log`).', 'x.md')
