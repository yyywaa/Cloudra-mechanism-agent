"""角色权限矩阵与统一权限闸（评审 5.6）。

验收对应：
- 每个角色的“允许 / 必须拒绝”逐格钉死在矩阵表里（该表是唯一预期）；
- researcher/experiment 不能通过 Bash 执行破坏性命令或脚本；计算角色保留
  write/script（计算入口）但不可任意删除；env/coordinator 的破坏性操作仍需审批；
- 统一闸的声明唯一来源是 ``ToolRegistration.required_permissions``，由
  ``PermissionStage`` 消费（工具类内的 is_* 判断只是第二道闸）；
- yolo 只影响审批策略，不扩大角色原本没有的能力。
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from cloudra.runtime_v2.adapters import _LegacyAgentBridge
from cloudra.runtime_v2.policies.base import ToolCall
from cloudra.runtime_v2.policies.permission import PermissionStage
from cloudra.runtime_v2.roles import RoleRegistry
from cloudra.runtime_v2.schemas import AgentCapabilities, AgentSession, PermissionSet
from cloudra.tools import get_tool_load_errors, get_tools_lst
from cloudra.tools.Bashtool.bash import Bash
from cloudra.tools.capabilities import missing_permissions, required_permissions_for
from cloudra.tools.registry import TOOL_REGISTRY

_PERMISSION_DOMAIN = {"read", "write", "manage", "script", "destructive"}
_EXCLUDED_MODULE_PREFIX = "cloudra.tools.Plantool.dag_tools."

# 矩阵的唯一预期表（逐格：允许与拒绝都在表里）。任何一位漂移都会在这里变红；
# 调整口径时改 roles.py 与此表两处即可。
_EXPECTED_MATRIX = {
    "coordinator": {"read": True, "write": True, "manage": True, "script": True, "destructive": True},
    "explorer": {"read": True, "write": False, "manage": False, "script": False, "destructive": False},
    "writer": {"read": True, "write": True, "manage": False, "script": False, "destructive": False},
    "researcher": {"read": True, "write": True, "manage": False, "script": False, "destructive": False},
    "small_mol": {"read": True, "write": True, "manage": False, "script": True, "destructive": False},
    "md": {"read": True, "write": True, "manage": False, "script": True, "destructive": False},
    "dft": {"read": True, "write": True, "manage": False, "script": True, "destructive": False},
    "experiment": {"read": True, "write": True, "manage": False, "script": False, "destructive": False},
    "env": {"read": True, "write": True, "manage": True, "script": True, "destructive": True},
    "supervisor": {"read": True, "write": False, "manage": False, "script": False, "destructive": False},
}

# registry 里 required_permissions 非空的条目数（有意的台账：新增/删除声明须同步
# 这一行，防止“声明被悄悄删掉”这种静默能力漂移）。
_DECLARATION_LEDGER = 37


def test_matrix_is_exactly_the_reviewed_table():
    actual = {role.role_id: role.permissions.model_dump() for role in RoleRegistry().list()}
    assert actual == _EXPECTED_MATRIX


def _bash_for(role_id: str) -> Bash:
    """用生产同款路径（AgentSession → _LegacyAgentBridge）构造 Bash，看命令级判定。"""
    role = RoleRegistry().require(role_id)
    agent = AgentSession(
        id="as_permission_matrix",
        project_id="prj_permission_matrix",
        role_id=role_id,
        display_name=role.display_name,
        capabilities=AgentCapabilities(permissions=role.permissions, tools=["*"]),
    )
    return Bash(subagent=_LegacyAgentBridge(agent, "unused-workspace"))


@pytest.mark.parametrize("role_id", ["researcher", "experiment"])
def test_researcher_and_experiment_bash_cannot_script_or_delete(role_id):
    bash = _bash_for(role_id)
    assert bash.has_command_permission("ls -la") is True
    assert bash.has_command_permission("rm -rf build/") is False
    assert bash.has_command_permission("python run_analysis.py") is False


@pytest.mark.parametrize("role_id", ["small_mol", "md", "dft"])
def test_compute_roles_keep_scripts_but_not_arbitrary_delete(role_id):
    bash = _bash_for(role_id)
    assert bash.has_command_permission("python run_qm.py") is True
    assert bash.has_command_permission("rm -rf old_runs/") is False


@pytest.mark.parametrize("role_id", ["env", "coordinator"])
def test_management_roles_keep_delete_with_approval_path(role_id):
    assert _bash_for(role_id).has_command_permission("rm -rf stale/") is True


def test_yolo_mode_does_not_expand_role_capabilities(monkeypatch):
    monkeypatch.setenv("CLOUDRA_YOLO_MODE", "1")
    assert _bash_for("researcher").has_command_permission("rm -rf stale/") is False


def test_manage_bit_is_held_only_by_management_roles():
    holders = sorted(r.role_id for r in RoleRegistry().list() if r.permissions.manage)
    assert holders == ["coordinator", "env"]


def _stage_ctx(role_id: str, permissions: PermissionSet | None = None):
    return SimpleNamespace(
        capabilities=SimpleNamespace(
            tools=["*"],
            permissions=permissions or RoleRegistry().require(role_id).permissions,
        ),
        settings=SimpleNamespace(visual_mode=False),
        agent=SimpleNamespace(role_id=role_id),
    )


@pytest.mark.asyncio
async def test_unified_gate_blocks_declared_tool_missing_role_bits():
    stage = PermissionStage()
    call = ToolCall(id="tc_write", name="write", arguments={"path": "a.txt", "content": "x"})
    blocked = await stage.before_tool(_stage_ctx("explorer"), call)
    assert blocked.outcome == "block"
    assert "write" in blocked.message
    allowed = await stage.before_tool(_stage_ctx("writer"), call)
    assert allowed.outcome == "allow"


@pytest.mark.asyncio
async def test_unified_gate_passes_unregistered_tools_through():
    stage = PermissionStage()
    call = ToolCall(id="tc_synthetic", name="totally_synthetic_tool", arguments={})
    result = await stage.before_tool(_stage_ctx("explorer"), call)
    assert result.outcome == "allow"


def test_missing_permissions_helper_is_the_declared_gap():
    assert missing_permissions(PermissionSet(read=True), "write") == frozenset({"write"})
    assert missing_permissions(PermissionSet(read=True, write=True), "write") == frozenset()
    assert missing_permissions(PermissionSet(read=True), "totally_synthetic_tool") == frozenset()
    assert required_permissions_for("subagent_launcher") == frozenset({"manage"})
    assert required_permissions_for("bash") == frozenset()  # 动态判定，不设静态闸


def test_declarations_stay_in_domain_and_never_double_gate():
    declared = [reg for reg in TOOL_REGISTRY if reg.required_permissions]
    assert len(declared) == _DECLARATION_LEDGER
    for reg in TOOL_REGISTRY:
        assert set(reg.required_permissions) <= _PERMISSION_DOMAIN, reg.tool_name
        if reg.module.startswith(_EXCLUDED_MODULE_PREFIX) or reg.invocation_direct_only:
            assert reg.required_permissions == frozenset(), reg.tool_name


def test_declared_permissions_match_tool_class_projections():
    """registry 声明 == 工具类 is_* 投影：同一事实不得两处漂移。

    缺可选依赖而导入失败的模块必须在 get_tool_load_errors() 里（不允许静默漏检）；
    可核对数量设下界，防止“全 skip 变绿”。
    """
    entries = {entry.tool_name: entry for entry in get_tools_lst()}
    load_errors = set(get_tool_load_errors())
    checked = 0
    for reg in TOOL_REGISTRY:
        if (
            not reg.tool_name
            or reg.module.startswith(_EXCLUDED_MODULE_PREFIX)
            or reg.invocation_direct_only
        ):
            continue
        entry = entries.get(reg.tool_name)
        if entry is None:
            assert reg.module in load_errors, (
                f"{reg.tool_name}: 未装载但模块 {reg.module} 不在加载失败清单里"
            )
            continue
        tool = entry.instantiate()
        projected = {
            bit
            for bit, flag in (
                ("read", tool.is_read()),
                ("write", tool.is_write()),
                ("manage", tool.is_manage()),
                ("script", tool.is_script()),
                ("destructive", tool.is_destructive()),
            )
            if flag
        }
        assert projected == set(reg.required_permissions), (
            f"{reg.tool_name}: registry={sorted(reg.required_permissions)} "
            f"class={sorted(projected)}"
        )
        checked += 1
    assert checked >= 10, f"可核对工具过少（{checked}）：用例可能被静默跳过"
