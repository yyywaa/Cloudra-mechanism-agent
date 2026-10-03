from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from cloudra.runtime_v2.events import EventLog
from cloudra.services.api_v2.sse import _sse_replay


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("count", "cursor", "expected_queries"),
    [
        (0, 0, [0]),
        (1, 0, [0]),
        (500, 0, [0, 500]),
        (501, 0, [0, 500]),
        (1000, 0, [0, 500, 1000]),
        (1201, 0, [0, 500, 1000]),
        (1201, 200, [200, 700, 1200]),
        (1201, 1201, [1201]),
        (0, 42, [42]),
    ],
)
async def test_sse_replay_reads_bounded_pages(count, cursor, expected_queries):
    log = EventLog(strict=True)
    for index in range(count):
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

    chunks = [chunk async for chunk in _sse_replay(core, project, cursor=cursor)]

    envelopes = [json.loads(chunk.split("data: ", 1)[1]) for chunk in chunks]
    events, synced = envelopes[:-1], envelopes[-1]
    assert [event["seq"] for event in events] == list(range(cursor + 1, count + 1))
    assert [event["data"]["index"] for event in events] == list(range(cursor, count))
    assert synced["type"] == "project.synced"
    assert synced["seq"] == 0
    assert synced["data"]["replayed_through"] == max(cursor, count)
    assert calls == [(after, 500, False) for after in expected_queries]
