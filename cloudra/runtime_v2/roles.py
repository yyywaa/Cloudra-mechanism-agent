"""Role profiles: the only place role permissions and defaults live.

Coordinator is one role among peers; nothing in the runtime may special-case
its role_id.  Agent-to-agent privileges are derived from ``can_spawn`` and
``spawn_roles``, never from a hard-coded coordinator id.
"""

from __future__ import annotations

from cloudra.base.role_identity import legacy_agent_id_for_role
from cloudra.runtime_v2.schemas import (
    OrchestrationMode,
    PermissionSet,
    RoleProfile,
    RuntimeSettingsPatch,
)

BUILTIN_ROLES: tuple[RoleProfile, ...] = (
    RoleProfile(
        role_id="coordinator",
        legacy_agent_id=legacy_agent_id_for_role("coordinator"),
        display_name="Coordinator",
        description="Decomposes objectives and dispatches peer agents.",
        # 评审 5.6（严格口径）：保留管理能力，但 destructive 默认不授予任何角色
        # ——删除/覆盖类命令执行前硬拒（不进审批，yolo 也不扩权）。如需放开，
        # 改这一行 + tests/test_permission_matrix.py 并同步 AGENTS.md 口径段。
        permissions=PermissionSet(read=True, write=True, manage=True, script=True, destructive=False),
        can_spawn=True,
        spawn_roles=None,
    ),
    RoleProfile(
        role_id="explorer",
        legacy_agent_id=legacy_agent_id_for_role("explorer"),
        display_name="Explorer",
        description="Read-only project structure and evidence review.",
        permissions=PermissionSet(read=True),
        can_spawn=False,
    ),
    RoleProfile(
        role_id="writer",
        legacy_agent_id=legacy_agent_id_for_role("writer"),
        display_name="Writer",
        description="Writes documents and reports; no script execution.",
        permissions=PermissionSet(read=True, write=True),
        can_spawn=False,
    ),
    RoleProfile(
        role_id="researcher",
        legacy_agent_id=legacy_agent_id_for_role("researcher"),
        display_name="Researcher",
        description="Literature search and method comparison.",
        # 评审 5.6：read/search + 交付文件写入；脚本与破坏性操作按最小权限收回
        # （Bash 的 script/destructive 命令硬拒，yolo 不能扩权）。
        permissions=PermissionSet(read=True, write=True),
        can_spawn=False,
    ),
    RoleProfile(
        role_id="small_mol",
        legacy_agent_id=legacy_agent_id_for_role("small_mol"),
        display_name="Small-molecule compute",
        description="Gaussian/ORCA molecular and cluster QM.",
        # 评审 5.6：计算所需 write/script/submit 保留；不可任意删除。
        permissions=PermissionSet(read=True, write=True, script=True),
        can_spawn=False,
    ),
    RoleProfile(
        role_id="md",
        legacy_agent_id=legacy_agent_id_for_role("md"),
        display_name="Molecular dynamics",
        description="Classical and enhanced-sampling MD.",
        # 评审 5.6：计算所需 write/script 保留；不可任意删除。
        permissions=PermissionSet(read=True, write=True, script=True),
        can_spawn=False,
    ),
    RoleProfile(
        role_id="dft",
        legacy_agent_id=legacy_agent_id_for_role("dft"),
        display_name="First-principles",
        description="VASP/CP2K periodic systems.",
        # 评审 5.6：计算所需 write/script 保留；不可任意删除。
        permissions=PermissionSet(read=True, write=True, script=True),
        can_spawn=False,
    ),
    RoleProfile(
        role_id="experiment",
        legacy_agent_id=legacy_agent_id_for_role("experiment"),
        display_name="Experiment design",
        description="Experimental design and data analysis.",
        # 评审 5.6：实验/谱图工具 + 限定写；不默认获得任意脚本与破坏性权限。
        permissions=PermissionSet(read=True, write=True),
        can_spawn=False,
    ),
    RoleProfile(
        role_id="env",
        legacy_agent_id=legacy_agent_id_for_role("env"),
        display_name="Environment",
        description="Scientific software environment setup and debugging.",
        # 评审 5.6（严格口径）：manage/script（环境管理）；删除/覆盖一律硬拒
        # （不默认持有 destructive）。
        permissions=PermissionSet(read=True, write=True, manage=True, script=True, destructive=False),
        can_spawn=False,
    ),
    RoleProfile(
        role_id="supervisor",
        legacy_agent_id=legacy_agent_id_for_role("supervisor"),
        display_name="Supervisor",
        description=(
            "Scientific supervisor in dag_guided mode: a real runtime_v2 agent "
            "driven by the normal LLM pipeline. Each turn it reads the persisted "
            "supervision mailbox (pending call reviews / open drafts / queued "
            "requests) and adjudicates around the submitted claims; an empty "
            "mailbox ends the turn. Its tool surface is the registry "
            "supervisor_access projection (read-only on the delivery graph)."
        ),
        permissions=PermissionSet(read=True),
        can_spawn=False,
        # 裁决工具（dag_review_call/dag_accept_mechanism）的模式门要求
        # dag_guided；督导只在 guided 项目里被创建，缺省即 guided。
        default_settings=RuntimeSettingsPatch(orchestration_mode=OrchestrationMode.DAG_GUIDED),
    ),
)


class RoleRegistry:
    def __init__(self, roles: tuple[RoleProfile, ...] = BUILTIN_ROLES) -> None:
        self._roles = {role.role_id: role for role in roles}

    def list(self) -> list[RoleProfile]:
        return list(self._roles.values())

    def get(self, role_id: str) -> RoleProfile | None:
        return self._roles.get(role_id)

    def require(self, role_id: str) -> RoleProfile:
        role = self._roles.get(role_id)
        if role is None:
            from cloudra.runtime_v2.schemas import CommandRejected

            raise CommandRejected("not_found", f"unknown role {role_id!r}")
        return role

    def update(self, role_id: str, patch: dict) -> RoleProfile:
        role = self.require(role_id)
        # 整模型重校验：patch 里的嵌套 dict（default_settings/permissions/
        # tool_policy）必须落成对应模型实例。裸 model_copy 不校验，会让活
        # core 持 dict 而快照恢复持模型——同一份 role.updated 事件在两条
        # 路径上推出不同形态（等价性门禁实测漂移点）。
        updated = RoleProfile.model_validate({**role.model_dump(mode="json"), **patch})
        self._roles[role_id] = updated
        return updated
