"""The record experiment retains facts but never gates settlement on science."""
import asyncio
from unittest.mock import AsyncMock

import pytest

from cloudra.dag.controller import DagController
from cloudra.persistence.database import ConversationDB


async def _controller(tmp_path):
    db = await asyncio.to_thread(lambda: ConversationDB("record-arm", data_dir=tmp_path / "data").init())
    controller = DagController(db, "s1", "dag_record", conversation_id="record-arm", working_directory=tmp_path)
    await controller.initialize()
    return controller


@pytest.mark.parametrize("disposition,basis", [("complete", "declared"), ("partial", "partial_recorded")])
@pytest.mark.asyncio
async def test_record_settles_without_science_or_delivery_artifact(tmp_path, monkeypatch, disposition, basis):
    controller = await _controller(tmp_path)
    (tmp_path / "mechanism_graph.json").write_text("not a valid graph")
    def forbidden(*args, **kwargs):
        raise AssertionError("record settlement must not gate on scientific proof or artifacts")
    monkeypatch.setattr(controller, "_required_irc_gaps", forbidden)
    monkeypatch.setattr("cloudra.dag.delivery_artifact.prepare_delivery_artifact", forbidden)
    monkeypatch.setattr("cloudra.benchmark.delivery_evidence.write_step_endpoint_evidence", forbidden)
    gate = await controller.audit_stop(disposition)
    assert gate.action == "allow_final"
    assert gate.basis == basis
    from cloudra.runtime_v2.completion import completion_summary
    from cloudra.runtime_v2.events import EventLog
    log = EventLog(strict=True)
    log.append("agent.completion_gate", stream="agent", project_id="record-arm",
        session_id="s1", run_id="r1", data={"action": gate.action, "source": "dag",
        "explicit_stop": True, "reason": gate.reason, "request_id": None, "basis": gate.basis})
    log.append("run.finished", stream="agent", project_id="record-arm",
        session_id="s1", run_id="r1", data={"outcome": "succeeded", "error": None})
    summary = completion_summary(list(log))
    assert summary["verification_label"] == ("partial" if disposition == "partial" else "unverified")
    assert not gate.report.complete
    assert gate.report.unresolved or gate.report.inconclusive
    await controller.commit_stop()
    def recorded():
        with controller.db.connect() as con:
            return con.execute("SELECT disposition FROM dag_delivery_dispositions").fetchall()
    assert await asyncio.to_thread(recorded) == [(disposition,)]
    assert controller._pending_stop is None
    assert controller._delivery_artifact is None


@pytest.mark.asyncio
async def test_record_retains_background_and_user_termination_safety(tmp_path, monkeypatch):
    controller = await _controller(tmp_path)
    monkeypatch.setattr(controller, "_has_pending_background", AsyncMock(return_value=True))
    gate = await controller.audit_stop("complete")
    assert gate.action == "wait_background" and gate.basis == "background_wait"
    gate = await controller.audit_stop("user_terminated")
    assert gate.action == "continue_work" and gate.basis is None


@pytest.mark.asyncio
async def test_record_retains_concurrent_state_protection(tmp_path, monkeypatch):
    controller = await _controller(tmp_path)
    await controller.audit_stop("complete")
    monkeypatch.setattr(controller.store, "delivery_state_fingerprint", lambda: "changed")
    with pytest.raises(RuntimeError, match="changed after audit"):
        await controller.commit_stop()
