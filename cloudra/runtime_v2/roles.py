"""Role profiles: the only place role permissions and defaults live.

Coordinator is one role among peers; nothing in the runtime may special-case
its role_id.  Agent-to-agent privileges are derived from ``can_spawn`` and
``spawn_roles``, never from a hard-coded coordinator id.

权限矩阵按「角色真实需要什么」反推（评审 5.6），不再给领域角色一律发
``write + script + destructive``：

| role | read | write | manage | script | destructive |
| :--- | :--: | :--: | :--: | :--: | :--: |
| coordinator | Y | Y | Y | Y | - |
| explorer | Y | - | - | - | - |
| writer | Y | Y | - | - | - |
| researcher | Y | - | - | - | - |
| experiment | Y | Y | - | - | - |
| small_mol / md / dft | Y | Y | - | Y | - |
| env | Y | Y | Y | Y | - |
| supervisor | Y | - | - | - | - |

口径（改矩阵先改这几条判据）：

- ``script`` 只给真正要在 shell 里跑程序/脚本的角色：三个计算角色与环境角色。
  研究/实验角色拿谱图与文献工具，不该获得任意脚本执行；
- ``destructive`` **谁都不默认给**：删除/覆盖类操作一律走审批通道（工具内
  ``ensure_safety``），yolo 只影响审批策略、**不扩大**角色本来没有的能力；
- ``write`` 给需要产出交付文件/输入文件/配置的角色；研究角色按需再授
  （``role.updated`` 命令可在运行期调整）；
- ``manage`` 目前只被 launcher/swarm/dag 工具声明（v2 派发链路由
  ``can_spawn`` / ``role_hidden_tools`` 把关），因此它是声明面而非执行面。
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
        # 统筹能力集中在编排与派发；破坏性操作与其它角色一样要单独审批——
        # 「统筹」不自动绕过工具级安全检查（评审 5.6 验收）。
        permissions=PermissionSet(read=True, write=True, manage=True, script=True),
        can_spawn=True,
        spawn_roles=None,
    ),
    RoleProfile(
        role_id="explorer",
        legacy_agent_id=legacy_agent_id_for_role("explorer"),
        display_name="Explorer",
        description="Read-only project structure and evidence review.",
        permissions=PermissionSet(read=True),
        # 纯输出型角色：交付文本，不写 HANDOFF、不管理多阶段状态。
        output_only=True,
        can_spawn=False,
    ),
    RoleProfile(
        role_id="writer",
        legacy_agent_id=legacy_agent_id_for_role("writer"),
        display_name="Writer",
        description="Writes documents and reports; no script execution.",
        permissions=PermissionSet(read=True, write=True),
        # 纯输出型角色：交付文本，不写 HANDOFF、不管理多阶段状态。
        output_only=True,
        can_spawn=False,
    ),
    RoleProfile(
        role_id="researcher",
        legacy_agent_id=legacy_agent_id_for_role("researcher"),
        display_name="Researcher",
        description="Literature search and method comparison.",
        # 检索/阅读为主：不跑任意脚本、不删除/覆盖文件。确有交付文件需求时由
        # 派发方或 role.updated 显式授 write。
        permissions=PermissionSet(read=True),
        # 纯输出型角色：交付文本，不写 HANDOFF、不管理多阶段状态。
        output_only=True,
        can_spawn=False,
    ),
    RoleProfile(
        role_id="small_mol",
        legacy_agent_id=legacy_agent_id_for_role("small_mol"),
        display_name="Small-molecule compute",
        description="Gaussian/ORCA molecular and cluster QM.",
        # 计算所需的 write（输入文件/交付物）+ script（命令行提交与后处理）；
        # 破坏性文件操作仍走审批，不由角色默认放行。
        permissions=PermissionSet(read=True, write=True, script=True),
        can_spawn=False,
    ),
    RoleProfile(
        role_id="md",
        legacy_agent_id=legacy_agent_id_for_role("md"),
        display_name="Molecular dynamics",
        description="Classical and enhanced-sampling MD.",
        permissions=PermissionSet(read=True, write=True, script=True),
        can_spawn=False,
    ),
    RoleProfile(
        role_id="dft",
        legacy_agent_id=legacy_agent_id_for_role("dft"),
        display_name="First-principles",
        description="VASP/CP2K periodic systems.",
        permissions=PermissionSet(read=True, write=True, script=True),
        can_spawn=False,
    ),
    RoleProfile(
        role_id="experiment",
        legacy_agent_id=legacy_agent_id_for_role("experiment"),
        display_name="Experiment design",
        description="Experimental design and data analysis.",
        # 实验/谱图工具 + 限定写；不默认获得任意脚本与破坏性权限。
        permissions=PermissionSet(read=True, write=True),
        # 纯输出型角色：交付文本，不写 HANDOFF、不管理多阶段状态。
        output_only=True,
        can_spawn=False,
    ),
    RoleProfile(
        role_id="env",
        legacy_agent_id=legacy_agent_id_for_role("env"),
        display_name="Environment",
        description="Scientific software environment setup and debugging.",
        # 环境搭建需要装/卸软件与跑构建脚本：manage + write + script；
        # 破坏性操作（删除、覆盖）仍要明确风险与审批。
        permissions=PermissionSet(read=True, write=True, manage=True, script=True),
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
