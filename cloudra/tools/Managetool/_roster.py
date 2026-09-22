"""子 Agent 花名册的唯一来源（评审 5.9）。

派发工具（``subagent_launcher`` / ``subagent_swarm``）的**模型可见描述**从这里取，
不再各自手抄 ``a-1``..``a-8`` 表——内容事实源是 ``runtime_v2/roles.py`` 的
``BUILTIN_ROLES``（与运行时权限同一份 RoleProfile）。

两条内容纪律：

- 角色能力由 policy stage 强制（权限矩阵见 ``tests/test_role_permission_matrix.py``），
  **不**把安全规则复述进提示词——复述出来的那份一定会与执行层漂移；
- ``agent_id`` 用角色语义名（``explorer``/``small_mol``…）；历史 ``a-N`` 词表只在
  ``cloudra/base/role_identity.py`` 映射，不作为派发参数的首选身份（评审 5.4）。
"""

from __future__ import annotations

from cloudra.runtime_v2.roles import BUILTIN_ROLES
from cloudra.runtime_v2.schemas import RoleProfile

#: 不通过派发工具创建的角色：Coordinator 是项目根，Supervisor 由运行时在
#: dag_guided 项目里自行创建（派发它等于绕过督导通道）。
NON_DISPATCHABLE_ROLES = frozenset({"coordinator", "supervisor"})


def dispatchable_roles() -> tuple[RoleProfile, ...]:
    """可派发的角色（RoleProfile 顺序即花名册顺序，稳定可断言）。"""
    return tuple(role for role in BUILTIN_ROLES if role.role_id not in NON_DISPATCHABLE_ROLES)


def subagent_roster_text() -> str:
    """编号花名册：``1. <role_id>: <description>``（逐行，供工具描述拼接）。"""
    return "\n".join(
        f"{index}. {role.role_id}: {role.description}"
        for index, role in enumerate(dispatchable_roles(), 1)
    )


def agent_id_guidance() -> str:
    """``agent_id`` 的取值口径（角色语义名，不是 a-N）。"""
    role_ids = ", ".join(role.role_id for role in dispatchable_roles())
    return (
        "**agent_id is the role id** (one of: "
        f"{role_ids}); the same role id may be dispatched repeatedly to run in "
        "parallel. Historical a-N ids are accepted for old data only — do not use "
        "them for new dispatches."
    )
