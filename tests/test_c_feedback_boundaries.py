"""C exposes measurements, not automatic acceptance; the ledger stays authoritative."""

import json
from types import SimpleNamespace

import pytest

from cloudra.persistence.database import ComputeDB
from cloudra.runtime_v2.events import EventLog
from cloudra.runtime_v2.invocation import tool_result_context_content
from cloudra.runtime_v2.notices import NoticeManager
from cloudra.runtime_v2.policies.base import ToolResult
from cloudra.services.ts_pipeline_store import create_process, get_process, save_process_record
from cloudra.tools.core.ts_inputs import TsInput
from cloudra.tools.core.ts_process import TsProcessRecord, TsStageRecord
from cloudra.tools.core.ts_state_view import build_process_view

REASON = (
    "frequency analysis found 2 imaginary mode(s) ([-400.0, -50.0]); the candidate is "
    "a point with 2 imaginary modes, not a first-order saddle point. This falsifies the candidate — it does NOT "
    "mean the reaction is impossible"
)


def record_fixture(tmp_path, *, durable=True):
    inputs = TsInput(reaction=dict(reactant_smiles="O", product_smiles="O", charge=0, multiplicity=1))
    db = ComputeDB(data_dir=tmp_path / "ledger").init()
    process = create_process(db, request_key="c-feedback", payload=dict(
        project_id="p", owner_id="a", workspace_dir=str(tmp_path), input=inputs.model_dump(mode="json"),
    ))
    run_dir = tmp_path / "ts" / "ts_001"
    run_dir.mkdir(parents=True)
    record = TsProcessRecord(
        run_id="ts_001", run_dir=str(run_dir), workspace_dir=str(tmp_path),
        owner_conversation_id="p", owner_session_id="a", input=inputs,
        pipeline_id=process["process_id"] if durable else "",
        stage="verdict", terminal="candidate_only",
        stage_records=[TsStageRecord(stage="verdict", status="done", detail=REASON)],
        evidence_candidates=["freq.out", "irc.out"],
    )
    return db, record


@pytest.mark.parametrize("exporter", ["save", "revision", "stop"])
def test_public_exports_keep_ids_but_ledger_keeps_real_verdict(tmp_path, monkeypatch, exporter):
    from cloudra.services.ts_pipeline_store import _write_revision_exports, stop_process
    from cloudra.tools.core.ts_process import save_record

    db, record = record_fixture(tmp_path)
    monkeypatch.setattr("cloudra.services.ts_pipeline_context.pipeline_database", lambda: db)
    save_process_record(db, process_id=record.pipeline_id, record=record.model_dump(mode="json"))
    record.revision = get_process(db, record.pipeline_id)["revision"]
    if exporter == "save":
        save_record(record)
    elif exporter == "revision":
        _write_revision_exports(record.model_dump(mode="json"))
    else:
        stopped = stop_process(db, process_id=record.pipeline_id, project_id="p", owner_id="a", reason="user stop")
        assert stopped["stop_reason"] is None  # stopping an already terminal workflow is a no-op
        assert stopped["terminal"] == "candidate_only"
    public = json.loads((tmp_path / "ts" / "ts_001" / "process.json").read_text())
    stored = get_process(db, record.pipeline_id)["record"]
    assert public["pipeline_id"] == record.pipeline_id
    assert public["revision"] == stored["revision"]
    assert public["terminal"] is None
    assert "-400.0" in public["stage_records"][0]["detail"]
    assert "-50.0" in public["stage_records"][0]["detail"]
    assert "falsifies" not in public["stage_records"][0]["detail"]
    assert public["evidence_candidates"] == ["freq.out", "irc.out"]
    assert stored["terminal"] == record.terminal == "candidate_only"
    assert stored["stage_records"][0]["detail"] == record.stage_records[0].detail == REASON


def test_file_only_authority_remains_loadable(tmp_path):
    from cloudra.tools.core.ts_process import load_record, save_record

    _, record = record_fixture(tmp_path, durable=False)
    save_record(record)
    loaded = load_record(str(tmp_path), record.run_id)
    assert loaded.terminal == "candidate_only"
    assert loaded.stage_records[0].detail == REASON


def test_durable_reader_uses_authoritative_state_not_public_export(tmp_path, monkeypatch):
    from cloudra.tools.core.ts_process import TsBlocked, load_record, save_record

    db, record = record_fixture(tmp_path)
    record.blocked = TsBlocked(failure_class="wrong_mode", stage="verdict", message=REASON, needs=[])
    monkeypatch.setattr("cloudra.services.ts_pipeline_context.pipeline_database", lambda: db)
    save_record(record)
    loaded = load_record(str(tmp_path), record.run_id)
    assert loaded.terminal == "candidate_only"
    assert loaded.blocked.failure_class == "wrong_mode"
    assert loaded.blocked.message == REASON


def test_durable_reader_rejects_reference_to_another_workspace(tmp_path, monkeypatch):
    from cloudra.tools.core.ts_process import load_record, save_record

    db, record = record_fixture(tmp_path)
    monkeypatch.setattr("cloudra.services.ts_pipeline_context.pipeline_database", lambda: db)
    save_record(record)
    other = tmp_path / "other"
    target = other / "ts" / record.run_id / "process.json"
    target.parent.mkdir(parents=True)
    target.write_text((tmp_path / "ts" / record.run_id / "process.json").read_text())
    with pytest.raises(ValueError, match="workspace|run"):
        load_record(str(other), record.run_id)


def test_context_uses_public_copy_without_changing_internal_view(tmp_path):
    _, record = record_fixture(tmp_path)
    view = build_process_view(record.model_dump(mode="json"), [], can_write=False)
    data = view.model_dump(mode="json")
    raw = ToolResult(True, json.dumps(data), data)
    public = json.loads(tool_result_context_content(SimpleNamespace(project_id="p"), raw))
    assert public["status"] == "ended"
    assert public["result"]["verified"] is None
    assert public["result"]["outcome"] is None
    assert public["result"]["evidence_refs"] == ["freq.out", "irc.out"]
    assert raw.data["result"]["verified"] is False
    assert view.result["outcome"] == "candidate_only"


@pytest.mark.parametrize("fresh", [True, False])
def test_guidance_projection_keeps_source_and_raw_event_across_restore(fresh):
    raw = "[Guidance] The target TS step remains unverified; Source: /work/ts/freq.out. Inspect geometry."
    events = EventLog(strict=True)
    notices = NoticeManager()
    notices.attach(events, lambda _: "p")
    notices.pin("a", "guidance-scientific-reflection:ts-process:ts_001", raw)
    restored = NoticeManager()
    restored.restore_from(events)
    public = restored.collect_batch("a", fresh=fresh)
    assert "unverified" not in public[0]["content"]
    assert "/work/ts/freq.out" in public[0]["content"]
    assert events.query_session("a")[0].data["content"] == raw


def test_public_tool_contract_describes_neutral_values_without_relaxing_internal_model():
    from cloudra.runtime_v2.tool_catalog import tool_declarations
    from cloudra.tools.core.ts_state_view import TsProcessView

    contract = tool_declarations(["ts_inspect"])
    assert '"verified": null' in contract
    assert '"outcome": "search_failed" | "invalid_input" | null' in contract
    # This remains an internal scientific record, not the public display contract.
    raw = TsProcessView(result=dict(outcome="verified", verified=True, reason="raw", evidence_refs=[]))
    assert raw.result["verified"] is True


@pytest.mark.asyncio
async def test_real_js_guest_gets_neutral_view_while_raw_event_keeps_truth(tmp_path):
    import asyncio
    import shutil
    from pathlib import Path

    from cloudra.runtime_v2.core import RuntimeCore
    from cloudra.runtime_v2.event_writer import EventWriter
    from cloudra.runtime_v2.invocation import InvocationService
    from cloudra.runtime_v2.js_runtime import JavaScriptRuntime
    from cloudra.runtime_v2.policies.base import PipelineContext, ToolCall
    from cloudra.runtime_v2.schemas import AgentCapabilities, AgentSession, PermissionSet, RuntimeSettings

    host = Path(__file__).resolve().parents[1] / "cloudra/runtime_v2/js_host"
    if not shutil.which("node") or not (host / "node_modules/quickjs-emscripten/package.json").is_file():
        pytest.skip("optional local JS host prerequisites missing")
    _, record = await asyncio.to_thread(record_fixture, tmp_path)
    data = build_process_view(record.model_dump(mode="json"), [], can_write=False).model_dump(mode="json")
    raw = ToolResult(True, json.dumps(data), data)

    class Executor:
        async def execute(self, agent, call):
            return raw

    core = RuntimeCore(strict_events=True)
    writer = EventWriter(core.event_log)
    runtime = JavaScriptRuntime(event_writer=writer, invocations=InvocationService(
        event_writer=writer, stages=[], tools=Executor(),
    ))
    agent = AgentSession(id="a", project_id="p", role_id="explorer", display_name="explorer")
    ctx = PipelineContext(
        agent=agent, run_id="r", settings_snapshot=RuntimeSettings(),
        capabilities=AgentCapabilities(permissions=PermissionSet(read=True), tools=["ts_inspect"]), inbox_messages=[], emit=lambda *a: None,
    )
    code = "const r = await tools.ts_inspect({}); text([r.is_success, r.data.result.verified, r.data.result.outcome, r.data.result.evidence_refs]);"
    result = await runtime.execute(ctx, ToolCall("c-wire", "js_exec", {"code": code}))
    assert result.is_success
    assert result.data["outputs"] == [[True, None, None, ["freq.out", "irc.out"]]]
    recorded = next(e for e in core.event_log if e.type == "tool.result_recorded")
    assert recorded.data["result"]["data"]["result"]["verified"] is False
    assert recorded.data["result"]["data"]["result"]["outcome"] == "candidate_only"
    assert raw.data["result"]["verified"] is False
