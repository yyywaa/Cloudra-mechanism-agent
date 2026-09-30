"""Role profiles: the only place role permissions and defaults live.

Coordinator is one role among peers. ``can_spawn`` and ``spawn_roles`` govern
hierarchical launcher/swarm dispatch; AgentHub peer calls use the shared
project-level creation path for every caller.
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
        description="Decomposes objectives and dispatches sub-agents.",
        permissions=PermissionSet(read=True, write=True, manage=True, script=True, destructive=True),
        can_spawn=True,
        spawn_roles=None,
    ),
    RoleProfile(
        role_id="explorer",
        legacy_agent_id=legacy_agent_id_for_role("explorer"),
        display_name="Explorer",
        description="Read-only project structure and evidence review.",
        roster="explore + review. Map project structure and locate files; read-only review of code/docs/data with an evidence-backed report. Read-only.",
        output_only=True,
        permissions=PermissionSet(read=True),
        can_spawn=False,
    ),
    RoleProfile(
        role_id="writer",
        legacy_agent_id=legacy_agent_id_for_role("writer"),
        display_name="Writer",
        description="Writes documents and reports; no script execution.",
        roster="papers and documents. Write reports, papers, docs. Document delivery writes; command permissions and approvals are enforced by runtime policy.",
        output_only=True,
        permissions=PermissionSet(read=True, write=True),
        can_spawn=False,
    ),
    RoleProfile(
        role_id="researcher",
        legacy_agent_id=legacy_agent_id_for_role("researcher"),
        display_name="Researcher",
        description="Literature search and method comparison.",
        roster="literature. Academic search, method breakdown, literature comparison. Academic search, method comparison and delivery; command permissions and approvals are enforced by runtime policy.",
        output_only=True,
        permissions=PermissionSet(read=True, write=True, script=True, destructive=True),
        can_spawn=False,
    ),
    RoleProfile(
        role_id="small_mol",
        legacy_agent_id=legacy_agent_id_for_role("small_mol"),
        display_name="Small-molecule compute",
        description="Gaussian/ORCA molecular and cluster QM.",
        roster="small-molecule compute. Gaussian/ORCA molecular/cluster QM: conformers, TS, spectra, energies.",
        permissions=PermissionSet(read=True, write=True, script=True, destructive=True),
        can_spawn=False,
    ),
    RoleProfile(
        role_id="md",
        legacy_agent_id=legacy_agent_id_for_role("md"),
        display_name="Molecular dynamics",
        description="Classical and enhanced-sampling MD.",
        roster="molecular dynamics. GROMACS/LAMMPS system build, equilibration, sampling, and trajectory analysis.",
        permissions=PermissionSet(read=True, write=True, script=True, destructive=True),
        can_spawn=False,
    ),
    RoleProfile(
        role_id="dft",
        legacy_agent_id=legacy_agent_id_for_role("dft"),
        display_name="First-principles",
        description="VASP/CP2K periodic systems.",
        roster="first-principles. VASP/CP2K periodic systems: bulk, surfaces, defects, electronic properties.",
        permissions=PermissionSet(read=True, write=True, script=True, destructive=True),
        can_spawn=False,
    ),
    RoleProfile(
        role_id="experiment",
        legacy_agent_id=legacy_agent_id_for_role("experiment"),
        display_name="Experiment design",
        description="Experimental design and data analysis.",
        roster="experimental design. DOE, controls, characterization matrix, safety assessment, and failure diagnosis.",
        output_only=True,
        permissions=PermissionSet(read=True, write=True, script=True, destructive=True),
        can_spawn=False,
    ),
    RoleProfile(
        role_id="env",
        legacy_agent_id=legacy_agent_id_for_role("env"),
        display_name="Environment",
        description="Scientific software environment setup and debugging.",
        roster="environment management. Dependency install, conda/venvs, build config, HPC job environments; command permissions and approvals are enforced by runtime policy.",
        permissions=PermissionSet(read=True, write=True, script=True, destructive=True),
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


def dispatch_roster() -> str:
    """Generate the built-in dispatch roster from role profiles."""
    return "".join(
        f"{index}. {role.role_id} ({role.legacy_agent_id}): {role.roster}\n"
        for index, role in enumerate(
            (role for role in BUILTIN_ROLES if role.roster), start=1
        )
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
