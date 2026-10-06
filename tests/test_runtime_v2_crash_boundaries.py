"""Durable command/effect boundaries and consumed input after compaction."""

from __future__ import annotations

import asyncio

import pytest

from cloudra.runtime_v2 import commands as commands_mod
from cloudra.runtime_v2.commands import CommandBus
from cloudra.runtime_v2.core import RuntimeCore
from cloudra.runtime_v2.effects import DeliverMessage, ScheduleAgent
from cloudra.runtime_v2.persistence import RuntimeStore, restore_core
from cloudra.runtime_v2.schemas import Command


class ProcessInterrupted(BaseException):
    """Simulate process death without entering ordinary exception recovery."""


class RecordingRunner:
    def __init__(self):
        self.scheduled = []

    def schedule(self, session_id):
        self.scheduled.append(session_id)


@pytest.mark.asyncio
@pytest.mark.parametrize("boundary", ["before_delivery", "after_delivery", "after_schedule"])
@pytest.mark.parametrize("snapshot", [False, True])
async def test_durable_spawn_recovers_unread_query_without_reexecuting_effects(
    tmp_path, monkeypatch, boundary, snapshot,
):
    store = await asyncio.to_thread(RuntimeStore, tmp_path / "runtime.db")
    core = RuntimeCore(strict_events=True)
    core.store = store
    core.runner = RecordingRunner()
    bus = CommandBus(core)
    project = (await bus.execute(Command(type="project.create", payload={"name": "crash"}))).data
    if snapshot:
        await bus.flush_snapshot()
    execute_effect = commands_mod._execute_effect

    async def interrupt_at_boundary(runtime, effect):
        if boundary == "before_delivery" and isinstance(effect, DeliverMessage):
            raise ProcessInterrupted
        await execute_effect(runtime, effect)
        if boundary == "after_delivery" and isinstance(effect, DeliverMessage):
            raise ProcessInterrupted
        if boundary == "after_schedule" and isinstance(effect, ScheduleAgent):
            raise ProcessInterrupted

    monkeypatch.setattr(commands_mod, "_execute_effect", interrupt_at_boundary)
    with pytest.raises(ProcessInterrupted):
        await bus.execute(Command(
            type="agent.spawn", target={"project_id": project.id},
            payload={"role_id": "coordinator", "query": "unread instruction"},
        ))
    agent_id = next(iter(core.agents))
    injected = core.event_log.query_session(agent_id, types={"agent.message_injected"})
    assert len(injected) == 1
    event_ids = [event.event_id for event in core.event_log]
    for _ in range(2):
        restored = RuntimeCore(strict_events=True)
        restored.runner = RecordingRunner()
        await asyncio.to_thread(restore_core, restored, store)
        assert list(restored.agents) == [agent_id]
        assert restored.runner.scheduled == []
        inbox = restored.mailbox.inbox(agent_id)
        assert inbox.qsize() == 1
        message = inbox.get_nowait()
        assert message["message_id"] == injected[0].data["message_id"]
        assert message["content"] == "unread instruction"
        assert [event.event_id for event in restored.event_log] == event_ids


@pytest.mark.asyncio
@pytest.mark.parametrize("snapshot", [False, True])
async def test_compacted_consumed_message_is_not_redelivered_after_restart(tmp_path, snapshot):
    store = await asyncio.to_thread(RuntimeStore, tmp_path / "runtime.db")
    core = RuntimeCore(strict_events=True)
    core.store = store
    bus = CommandBus(core)
    project = (await bus.execute(Command(type="project.create", payload={"name": "compact"}))).data
    agent = (await bus.execute(Command(
        type="agent.spawn", target={"project_id": project.id},
        payload={"role_id": "coordinator", "query": "consumed instruction"},
    ))).data
    message = core.mailbox.inbox(agent.id).get_nowait()
    await core.contexts.commit_input(
        agent=agent, run_id="run_crash", context_prefix=None, notices=None,
        user_messages=[{"role": "user", "content": message["content"], "message_id": message["message_id"]}],
    )
    assert await core.contexts.install_compacted(
        agent=agent, run_id="run_crash", messages=[{"role": "assistant", "content": "summary"}],
        prefix_meta=None, expected_version=1, trigger="manual",
    )
    assert core.contexts.filter_pending_input(agent.id, [message]) == []
    if snapshot:
        await bus.flush_snapshot()
    for _ in range(2):
        restored = RuntimeCore(strict_events=True)
        await asyncio.to_thread(restore_core, restored, store)
        assert restored.mailbox.inbox(agent.id).empty()
        assert restored.contexts.current_messages(agent.id) == [{"role": "assistant", "content": "summary"}]
