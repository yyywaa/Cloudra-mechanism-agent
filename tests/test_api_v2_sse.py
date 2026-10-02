from __future__ import annotations

from types import SimpleNamespace

import pytest

from cloudra.runtime_v2.events import EventLog
from cloudra.services.api_v2.sse import _sse_replay


@pytest.mark.asyncio
async def test_sse_replay_reads_bounded_pages():
    log = EventLog(strict=True)
    for index in range(1201):
        log.append(
            "agent.warning",
            stream="agent",
            project_id="project-1",
            session_id="session-1",
            data={"index": index},
        )

    calls: list[tuple[int, int, bool]] = []
    original = log.query_project

    def query_project(project_id: str, **kwargs):
        calls.append((kwargs["after_seq"], kwargs["limit"], kwargs["tail"]))
        return original(project_id, **kwargs)

    log.query_project = query_project  # type: ignore[method-assign]
    core = SimpleNamespace(event_log=log)
    project = SimpleNamespace(id="project-1")

    chunks = [chunk async for chunk in _sse_replay(core, project, cursor=0)]

    assert len(chunks) == 1202  # events plus the project.synced boundary
    assert len(calls) == 4
    assert all(limit == 500 and tail is False for _, limit, tail in calls)
    assert [after for after, _, _ in calls] == [0, 500, 1000, 1500]
