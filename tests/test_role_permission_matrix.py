"""按角色最小权限的默认矩阵（评审 5.6）。

矩阵的唯一事实源是 ``runtime_v2/roles.py`` 的 ``BUILTIN_ROLES``；本文件是它
**有意钉住**的判据（改矩阵必须同时改这里，且要有理由）：

- ``script`` 只给真正要在 shell 里跑程序/脚本的角色（三个计算角色 + 环境角色）；
- ``destructive`` 谁都不默认给：删除/覆盖类操作一律走审批通道
  （``tools_class.ensure_safety``），yolo 只影响审批策略、**不扩大**角色本来
  没有的能力；
- 研究/实验角色拿谱图与文献工具，不默认获得任意脚本执行；
- 计算角色仍能完成科学工作流（读日志、跑分析脚本、写输入/交付文件）。

判据消费点：``tools/Bashtool/bash.py`` 的 ``has_command_permission`` ——
它把命令经 ``BashCommandClassifier`` 分类成权限位再与角色权限比对
（只读=READ、纯写=WRITE、跑程序=SCRIPT、删除/覆盖=WRITE|DESTRUCTIVE）。
本文件里的命令清单按**分类器实测口径**选取，不是猜的。
"""

from __future__ import annotations

import pytest

from cloudra.runtime_v2.roles import BUILTIN_ROLES
from cloudra.tools.Bashtool.bash import Bash
from tests.dag_identity import make_actor

#: 期望矩阵：role_id -> (read, write, manage, script, destructive)
_EXPECTED: dict[str, tuple[bool, bool, bool, bool, bool]] = {
    "coordinator": (True, True, True, True, False),
    "explorer": (True, False, False, False, False),
    "writer": (True, True, False, False, False),
    "researcher": (True, False, False, False, False),
    "small_mol": (True, True, False, True, False),
    "md": (True, True, False, True, False),
    "dft": (True, True, False, True, False),
    "experiment": (True, True, False, False, False),
    "env": (True, True, True, True, False),
    "supervisor": (True, False, False, False, False),
}

# 分类器实测：READ=1 / WRITE=2 / SCRIPT=8 / 删除覆盖=16（或 19）
_READ_COMMANDS = ("ls -la", "cat f.txt")
_WRITE_COMMANDS = ("tee f.txt", "truncate -s 0 f.txt")
_SCRIPT_COMMANDS = ("python train.py", "bash run.sh")
_DESTRUCTIVE_COMMANDS = ("rm -rf /tmp/x", "mv a b", "chmod 777 f", "echo hi > f.txt")

_READ_ONLY_ROLES = ("explorer", "researcher", "supervisor")
_NO_SCRIPT_ROLES = ("explorer", "writer", "researcher", "experiment", "supervisor")
_SCRIPT_ROLES = ("small_mol", "md", "dft", "env")


def _bash(role_id: str, **settings) -> Bash:
    """按角色构造在线身份（权限取自 RoleProfile），再用真实 bash 工具判定。

    身份经 ``dag_identity.make_actor``：与派发路径同一投影（``_LegacyAgentBridge``），
    不是测试自造的权限位。
    """
    return Bash(subagent=make_actor("perm-matrix", role_id, **settings))


def _denied(role_id: str, commands: tuple[str, ...]) -> list[str]:
    """返回该角色在这批命令里**被拒**的那些（空列表 = 全部放行）。"""
    tool = _bash(role_id)
    return [command for command in commands if not tool.has_command_permission(command)]


def test_builtin_matrix_matches_the_least_privilege_table():
    """钉住矩阵本身：任何一格变化都会在这里显形（评审要求逐角色有预期）。"""
    actual = {
        role.role_id: (
            bool(role.permissions.read),
            bool(role.permissions.write),
            bool(role.permissions.manage),
            bool(role.permissions.script),
            bool(role.permissions.destructive),
        )
        for role in BUILTIN_ROLES
    }
    assert actual == _EXPECTED, {
        role_id: (got, _EXPECTED.get(role_id))
        for role_id, got in actual.items()
        if got != _EXPECTED.get(role_id)
    }
    # 没有任何内置角色默认握有破坏性权限（yolo 不改变这一点）。
    assert not any(row[4] for row in actual.values())


@pytest.mark.parametrize("role_id", sorted(_EXPECTED))
def test_no_role_can_delete_or_overwrite_through_bash(role_id):
    """``destructive`` 谁都不默认给：删除/覆盖类命令对每个内置角色都是拒绝。"""
    assert _denied(role_id, _DESTRUCTIVE_COMMANDS) == list(_DESTRUCTIVE_COMMANDS)


@pytest.mark.parametrize("role_id", _READ_ONLY_ROLES)
def test_read_only_roles_only_read(role_id):
    """只读角色：读得到，写/脚本/删除都拒。"""
    assert _denied(role_id, _READ_COMMANDS) == []
    assert _denied(role_id, _WRITE_COMMANDS) == list(_WRITE_COMMANDS)
    assert _denied(role_id, _SCRIPT_COMMANDS) == list(_SCRIPT_COMMANDS)


@pytest.mark.parametrize("role_id", ("researcher", "experiment"))
def test_research_and_experiment_roles_cannot_run_arbitrary_scripts(role_id):
    """验收：研究/实验角色不默认获得任意脚本执行（谱图/文献工具照常用）。"""
    assert _denied(role_id, _SCRIPT_COMMANDS) == list(_SCRIPT_COMMANDS)


def test_writer_writes_but_does_not_script():
    assert _denied("writer", _READ_COMMANDS) == []
    assert _denied("writer", _WRITE_COMMANDS) == []
    assert _denied("writer", _SCRIPT_COMMANDS) == list(_SCRIPT_COMMANDS)


@pytest.mark.parametrize("role_id", _SCRIPT_ROLES)
def test_compute_and_env_roles_keep_their_science_commands(role_id):
    """验收：计算角色（与环境角色）仍能完成现有科学工作流：读、写、跑脚本。"""
    for commands in (_READ_COMMANDS, _WRITE_COMMANDS, _SCRIPT_COMMANDS):
        assert _denied(role_id, commands) == [], f"{role_id} 被挡: {commands}"


@pytest.mark.parametrize("role_id", ("small_mol", "researcher", "env", "experiment"))
def test_yolo_does_not_widen_role_permissions(role_id):
    """验收：yolo 只影响审批策略，不扩大角色本来没有的能力。

    yolo 打开后 bash 的逐条判定与关闭时**完全一致**——审批通道不参与权限
    判定，所以"删干净/覆盖"这类操作不会因为 yolo 而变得可行。
    """
    plain, yolo = _bash(role_id), _bash(role_id, yolo=True)
    for command in (
        _READ_COMMANDS + _WRITE_COMMANDS + _SCRIPT_COMMANDS + _DESTRUCTIVE_COMMANDS
    ):
        assert yolo.has_command_permission(command) == plain.has_command_permission(
            command
        ), command
