"""Offline D-arm invariants; no provider, compute backend or telemetry calls."""
import json
from copy import deepcopy

from cloudra.runtime_v2.brief_errors import project_feedback, project_notice, project_tool_result
from cloudra.runtime_v2.policies.base import ToolResult

CANARY = 'CANARY: atom 9 field guess.scan is wrong; change distance to 1.7 and retry'


def test_projection_is_pure_idempotent_and_preserves_controls_and_measurements():
    raw = {'is_success': True, 'status': 'blocked', 'stage': 'verify',
           'blocked': {'failure_class': 'wrong_mode', 'message': CANARY, 'needs': ['guess.scan'],
                       'issues': [{'code': 'invalid', 'field': 'guess.scan', 'message': CANARY}]},
           'result': {'outcome': 'candidate_only', 'verified': False, 'reason': CANARY},
           'frequency_analysis': {'frequencies': [-110.3, 42.0], 'mode_alignment':
                                  {'status': 'misaligned', 'message': CANARY, 'score': 0.2}},
           'structures': {'atoms': [{'element': 'C', 'x': 1.7}]},
           'manifest': {'kind': 'exit_review_decision', 'verdict': 'reject', 'request_id': 'r1'},
           'next': {'action': 'resume', 'required_inputs': ['guess.scan']}}
    before = deepcopy(raw)
    public = project_feedback(raw)
    assert raw == before
    assert project_feedback(public) == public
    assert CANARY not in json.dumps(public)
    assert public['blocked']['failure_class'] == 'wrong_mode'
    assert public['blocked']['issues'][0]['code'] == 'invalid'
    assert public['status'] == raw['status'] and public['stage'] == raw['stage']
    assert public['manifest'] == raw['manifest']
    assert public['frequency_analysis']['frequencies'] == [-110.3, 42.0]
    assert public['frequency_analysis']['mode_alignment']['score'] == 0.2
    assert public['structures'] == raw['structures']
    assert public['next']['action'] == 'resume'


def test_successful_data_and_native_output_unchanged():
    raw = {'is_success': True, 'result': 'native ORCA output and measurements',
           'message': 'finished', 'reason': 'scientific observation', 'detail': 'energy -10.3',
           'energy': -10.3, 'normal_termination': True, 'partial': {'energy': -9.0}}
    assert project_feedback(raw) == raw
    for name in ['bash', 'read', 'log_parser']:
        native = ToolResult(False, json.dumps(raw), raw)
        assert project_tool_result(native, tool_name=name).data['result'] == raw['result']


def test_successful_queries_cannot_recover_nested_diagnostics():
    raw = {'is_success': True, 'jobs': [{'state': 'failed', 'last_error': CANARY, 'job_id': 3}],
           'decision': {'verdict': 'reject', 'reason': CANARY, 'next_action': CANARY},
           'scientific_checks': {'frequency': {'status': 'failed', 'detail': CANARY, 'next_action': CANARY}},
           'unresolved': [{'code': 'frequency_missing', 'detail': CANARY, 'target_id': 's1'}]}
    result = ToolResult(True, json.dumps(raw), raw)
    public = project_tool_result(result)
    assert CANARY not in public.summary and CANARY not in json.dumps(public.data)
    assert CANARY in result.summary
    assert public.data['jobs'][0]['state'] == 'failed'
    assert public.data['unresolved'][0]['code'] == 'frequency_missing'


def test_notice_projection_retains_generic_guidance_and_error_categories():
    generic = '[Guidance] Choose methods under the existing budget and verify frequencies.'
    assert project_notice(generic, key='guidance-ts-sop') == generic
    supervisor = '[Supervisor review decision] decision_id=d1 request_id=r1 verdict=reject reason=' + CANARY + ' next_action=' + CANARY
    assert CANARY not in project_notice(supervisor)
    assert 'verdict=reject' in project_notice(supervisor)
    reflection = '[Guidance] Structured TS verification failed. (source: secret). ' + CANARY
    assert CANARY not in project_notice(reflection, key='guidance-scientific-reflection:verify')
    assert 'verification failed' in project_notice(reflection, key='guidance-scientific-reflection:verify')


def test_child_manifest_does_not_reveal_raw_run_error():
    raw = {'state': 'failed', 'last_run': {'outcome': 'failed', 'failure_kind': 'pipeline_internal'},
           'final_summary': CANARY, 'final_summary_source': 'run_error',
           'gate': {'action': 'continue_work', 'reason': CANARY},
           'unresolved': [CANARY], 'next_steps': [CANARY]}
    public = project_feedback(raw)
    assert CANARY not in json.dumps(public)
    assert public['last_run'] == raw['last_run']


def test_scalar_error_and_invocation_error_keep_error_semantics():
    from cloudra.runtime_v2.invocation_types import InvocationError
    raw = ToolResult(False, CANARY, {'error': CANARY}, error=InvocationError(
        code='policy_blocked', message=CANARY, effect_state='not_started', stage='science'))
    public = project_tool_result(raw)
    assert CANARY not in json.dumps(public.data)
    assert CANARY not in public.summary and CANARY not in public.error.message
    assert public.error.code == raw.error.code
    assert public.error.stage == raw.error.stage
    assert public.error.effect_state == raw.error.effect_state
    assert raw.error.message == CANARY
    assert project_tool_result(ToolResult(False, CANARY)).error is None
    assert CANARY not in project_feedback(CANARY, diagnostic=True)


def test_js_frames_project_after_original_size_checks():
    from dataclasses import replace

    import pytest

    from cloudra.runtime_v2.js_protocol import (
        ProgramLimits,
        ProtocolError,
        encode_tool_error_frame,
        encode_tool_result_frame,
    )
    data = {'error': CANARY, 'energy': -10.3}
    envelope = {'is_success': False, 'data': data, 'summary': json.dumps(data),
                'call_id': 'c1', 'duration_ms': 3}
    public = json.loads(encode_tool_result_frame('r1', envelope))['result']
    assert CANARY not in json.dumps(public)
    assert public['duration_ms'] == 3 and public['data']['energy'] == -10.3
    assert envelope['data']['error'] == CANARY
    limits = replace(ProgramLimits(), tool_result_bytes=40)
    with pytest.raises(ProtocolError):
        encode_tool_result_frame('r1', envelope, limits=limits)
    error = {'code': 'policy_blocked', 'message': CANARY, 'stage': 'science',
             'effect_state': 'not_started', 'raw_result_event_id': 'e1'}
    public_error = json.loads(encode_tool_error_frame('r1', error))['error']
    assert CANARY not in json.dumps(public_error)
    assert public_error['code'] == error['code']
    assert public_error['raw_result_event_id'] == error['raw_result_event_id']
    with pytest.raises(ProtocolError):
        encode_tool_error_frame('r1', error, limits=replace(ProgramLimits(), rpc_line_bytes=100))


def test_pins_replay_incremental_and_mailbox_keep_full_audit():
    from cloudra.runtime_v2.agent_runner import AgentRunner
    from cloudra.runtime_v2.events import EventLog
    from cloudra.runtime_v2.notices import NoticeManager
    from tests.notice_support import commit_notices
    text = '[Supervisor review decision] decision_id=d1 request_id=r1 verdict=reject reason=' + CANARY
    log = EventLog(strict=True)
    notices = NoticeManager()
    notices.attach(log, lambda sid: 'p1')
    notices.pin('s1', 'review-d1', text)
    assert CANARY in notices.pin_content('s1', 'review-d1')
    assert CANARY in json.dumps([event.data for event in log])
    assert CANARY not in json.dumps(notices.render_current('s1'))
    assert CANARY not in json.dumps(notices.collect_batch('s1', fresh=True))
    commit_notices(notices, 's1')
    notices.pin('s1', 'review-d1', text + ' updated')
    assert CANARY not in json.dumps(notices.collect_batch('s1', fresh=False))
    restored = NoticeManager()
    restored.restore_from(log)
    assert CANARY not in json.dumps(restored.collect_batch('s1', fresh=True))
    inbox = [{'sender': 'supervisor', 'content': text,
              'manifest': {'kind': 'exit_review_decision', 'verdict': 'reject', 'request_id': 'r1'}}]
    prepared = AgentRunner._prepare_inbox_messages(None, None, inbox)
    assert CANARY not in prepared[0]['content']
    assert prepared[0]['manifest'] == inbox[0]['manifest']
    assert CANARY in inbox[0]['content']


def test_completion_feedback_keeps_gate_and_strike_fingerprint_inputs():
    from types import SimpleNamespace

    from cloudra.runtime_v2.agent_runner import AgentRunner
    gate = SimpleNamespace(reason=CANARY, report=SimpleNamespace(
        unresolved=[SimpleNamespace(code='freq_missing', target_type='species', target_id='s1', detail=CANARY)],
        inconclusive=[]))
    runner = SimpleNamespace(max_exit_strikes=3)
    raw = AgentRunner._gate_feedback_text(runner, gate, strike=2)
    public = project_notice(raw)
    assert CANARY not in public
    assert 'freq_missing on species s1' in public
    assert 'Exit attempt 2/3' in public
    assert gate.reason == CANARY and CANARY in raw


def test_compute_failure_projection_keeps_states_evidence_and_cancel_instruction():
    raw = ('Compute Event: Job 12, state=failed. TS t1: refine.\n'
           'Physical Reality: outcome=search_failed; verified=false. ' + CANARY + '\n'
           'Advisory from ts_guess: ' + CANARY + '\nNEXT: ' + CANARY + '\n'
           'Evidence: /work/freq.log')
    public = project_notice(raw)
    assert CANARY not in public
    assert 'outcome=search_failed; verified=false.' in public
    assert 'state=failed' in public and 'Evidence: /work/freq.log' in public
    cancelled = raw.replace('NEXT: ' + CANARY,
                            'NEXT: Do not resubmit or restart without a new explicit user request.')
    assert 'Do not resubmit or restart' in project_notice(cancelled)


def test_file_only_process_retains_raw_and_durable_export_projects():
    from cloudra.runtime_v2.brief_errors import public_process_record
    raw = {'pipeline_id': '', 'blocked': {'failure_class': 'wrong_mode', 'message': CANARY},
           'input': {'reason': 'normal declaration'}, 'partial': {'energy': -1.1}}
    assert public_process_record(raw) == raw
    durable = {**raw, 'pipeline_id': 'p1'}
    public = public_process_record(durable)
    assert CANARY not in json.dumps(public)
    assert CANARY in json.dumps(durable)
    assert public['partial'] == durable['partial'] and public['input'] == durable['input']


def test_child_render_and_traditional_context_remove_diagnostics():
    from cloudra.runtime_v2.child_manifest import render_child_report
    from cloudra.runtime_v2.invocation import tool_result_context_content
    from cloudra.runtime_v2.schemas import AgentSession
    manifest = {'role_id': 'explorer', 'session_id': 's1', 'state': 'failed',
                'runs': {'total': 1, 'succeeded': 0, 'failed': 1, 'cancelled': 0},
                'last_run': {'outcome': 'failed', 'failure_kind': 'pipeline_internal'},
                'final_summary': CANARY, 'final_summary_source': 'run_error',
                'unresolved': [CANARY], 'next_steps': [CANARY]}
    assert CANARY not in render_child_report(manifest)
    agent = AgentSession(id='s1', project_id='p1', role_id='explorer', display_name='explorer')
    data = {'is_success': True, 'manifest': manifest}
    assert CANARY not in tool_result_context_content(agent, ToolResult(True, json.dumps(data), data))
    assert CANARY in manifest['final_summary']


def test_failed_mixed_message_preserves_preparation_observations():
    text = CANARY + '\nPreparation performed: native geometry ready; energy -10.3'
    public = project_feedback({'status': 'blocked', 'message': text})
    assert CANARY not in public['message']
    assert '\nPreparation performed: native geometry ready; energy -10.3' in public['message']


def test_process_export_keeps_full_sqlite_authority(tmp_path):
    from cloudra.persistence.database import ComputeDB
    from cloudra.services.ts_pipeline_context import use_pipeline_database
    from cloudra.services.ts_pipeline_store import create_process, get_process
    from cloudra.tools.core.ts_process import TsProcessRecord, save_record
    from tests.test_ts_pipeline_store import payload
    db = ComputeDB(data_dir=tmp_path / 'db').init()
    declaration = payload(workspace_dir=str(tmp_path))
    process = create_process(db, request_key='brief-test', payload=declaration)
    record = TsProcessRecord(
        run_id='t1', pipeline_id=process['process_id'], run_dir=str(tmp_path / 'run'),
        workspace_dir=str(tmp_path), owner_conversation_id='project', owner_session_id='owner',
        input=declaration['input'], stage='validate',
        blocked={'failure_class': 'wrong_mode', 'stage': 'validate', 'message': CANARY,
                 'needs': ['guess.scan'], 'issues': [{'code': 'invalid', 'message': CANARY}]},
    )
    (tmp_path / 'run').mkdir()
    with use_pipeline_database(db):
        path = save_record(record)
    from pathlib import Path
    public = json.loads(Path(path).read_text())
    stored = get_process(db, process['process_id'])['record']
    assert CANARY not in json.dumps(public)
    assert CANARY in json.dumps(stored)
    assert public['input'] == stored['input']
    assert public['revision'] == stored['revision']
    assert record.blocked.message == CANARY


def test_scientific_reflection_projection_is_idempotent():
    text = '[Guidance] This TS optimization did not converge; ' + CANARY
    key = 'guidance-scientific-reflection:ts-process:t1'
    public = project_notice(text, key=key)
    assert project_notice(public, key=key) == public


async def _record_failed_invocation(tmp_path):
    from cloudra.runtime_v2.core import RuntimeCore
    from cloudra.runtime_v2.event_writer import EventWriter
    from cloudra.runtime_v2.invocation import InvocationService, tool_result_context_content
    from cloudra.runtime_v2.persistence import RuntimeStore
    from cloudra.runtime_v2.policies.base import ToolCall
    from tests.test_runtime_v2_invocation import Executor, _agent, _ctx
    core = RuntimeCore(strict_events=True)
    store = RuntimeStore(tmp_path / 'runtime.db')
    writer = EventWriter(core.event_log, store_provider=lambda: store)
    raw = ToolResult(False, json.dumps({'message': CANARY}), {'message': CANARY})
    service = InvocationService(event_writer=writer, stages=[], tools=Executor(raw))
    outcome = await service.invoke(_ctx(_agent()), ToolCall('c1', 'echo', {}))
    assert outcome.result.error is None and outcome.error is None
    assert CANARY not in tool_result_context_content(_agent(), outcome.result, tool_name='echo')
    recorded = store.get_event(outcome.raw_result_event_id)
    assert CANARY in recorded.data['result']['summary']
    assert recorded.data['result']['data']['message'] == CANARY
    finished = [event for event in store.read_events() if event.type == 'tool.finished'][-1]
    assert finished.data['status'] == 'failed'
    assert finished.data['effect_state'] == 'completed'


def test_invocation_persists_full_result_before_public_projection(tmp_path):
    import asyncio
    asyncio.run(_record_failed_invocation(tmp_path))


def test_dag_prompt_preserves_state_and_contract_while_shortening_reason():
    from cloudra.dag.models import DagProjection, OrchestrationMode
    projection = DagProjection(mode=OrchestrationMode.DAG_GUIDED, revisions={'delivery': 2},
                               delivery_gaps=[{'code': 'freq_missing', 'target_id': 's1', 'detail': CANARY}],
                               rejected_draft={'draft_id': 'd1', 'reject_reason': CANARY})
    public = projection.to_prompt_text()
    assert CANARY not in public
    assert 'freq_missing' in public and 'd1' in public
    assert 'exactly one imaginary' in public
    assert projection.delivery_gaps[0]['detail'] == CANARY


def test_js_runtime_unavailable_keeps_durable_full_error(tmp_path):
    import asyncio

    from cloudra.runtime_v2.core import RuntimeCore
    from cloudra.runtime_v2.event_writer import EventWriter
    from cloudra.runtime_v2.js_runtime import JavaScriptRuntime
    from cloudra.runtime_v2.persistence import RuntimeStore
    from cloudra.runtime_v2.policies.base import ToolCall
    from tests.test_runtime_v2_invocation import _agent, _ctx
    async def scenario():
        core = RuntimeCore(strict_events=True)
        store = RuntimeStore(tmp_path / 'runtime.db')
        writer = EventWriter(core.event_log, store_provider=lambda: store)
        runtime = JavaScriptRuntime(event_writer=writer, invocations=None)
        async def unavailable():
            return CANARY
        runtime._check_prerequisites = unavailable
        result = await runtime.execute(_ctx(_agent()), ToolCall('c1', 'js_exec', {'code': 'text(1)'}))
        assert CANARY not in result.summary and CANARY not in json.dumps(result.data)
        assert result.data['error']['code'] == 'runtime_unavailable'
        persisted = [event for event in store.read_events() if event.type == 'program.finished'][-1]
        assert persisted.data['error']['message'] == CANARY
    asyncio.run(scenario())


def test_unverified_success_and_partial_are_not_errors():
    raw = {'is_success': True, 'verified': False, 'verification_status': 'candidate',
           'message': 'normal observations', 'detail': 'scientific calculation completed',
           'partial': {'verified': False, 'energy': -10.3, 'reason': 'valid subresult'}}
    result = ToolResult(True, json.dumps(raw), raw)
    assert project_feedback(raw) == raw
    assert project_tool_result(result) == result


def test_unverified_compute_notices_preserve_normal_stops_candidates_and_partial():
    for state, outcome in [('stopped', ''), ('cancelled', ''), ('done', 'partial'),
                           ('done', 'candidate'), ('done', '')]:
        result = f'outcome={outcome}; ' if outcome else ''
        raw = (f'Compute Event: Job 12, state={state}. TS t1: inspect.\n'
               f'Physical Reality: {result}verified=false. Energy -10.3 Eh; distance 1.7 A.\n'
               'NEXT: Inspect the retained partial observations and native log.\n'
               'Evidence: /work/freq.log')
        assert project_notice(raw) == raw


def test_compute_failure_outcomes_and_alignment_advisories_still_shorten_details():
    for outcome in ['candidate_only', 'search_failed', 'invalid_input']:
        raw = ('Compute Event: Job 12, state=done. TS t1: inspect.\n'
               f'Physical Reality: outcome={outcome}; verified=false. {CANARY}\n'
               f'NEXT: {CANARY}\nEvidence: /work/freq.log')
        public = project_notice(raw)
        assert CANARY not in public
        assert f'outcome={outcome}; verified=false.' in public
        assert 'state=done.' in public and 'Evidence: /work/freq.log' in public
    advisory = ('Compute Event: Job 12, state=done.\n'
                f'Advisory from ts_guess: {CANARY}\nNEXT: {CANARY}')
    assert CANARY not in project_notice(advisory)


def test_mixed_scientific_checks_retained_but_standalone_repair_shortened():
    from cloudra.tools.Chemtool.ts_guess import _IRC_TRUNCATION_REMEDY
    measured = 'Exactly 1 imaginary frequency (-110.3 cm-1): candidate.'
    raw = {'is_success': True, 'verification_status': 'inconclusive',
           'verdict': 'inconclusive: ' + CANARY, 'n_imag': 1, 'imag_freqs': [-110.3],
           'checks': [measured, _IRC_TRUNCATION_REMEDY],
           'imag_mode_aligned': False, 'imag_mode_alignment': CANARY}
    public = project_feedback(raw)
    assert CANARY not in json.dumps(public)
    assert public['verification_status'] == 'inconclusive'
    assert public['verdict'].startswith('inconclusive:')
    assert public['n_imag'] == 1 and public['imag_freqs'] == [-110.3]
    assert public['checks'][0] == measured
    assert _IRC_TRUNCATION_REMEDY not in public['checks']


def test_brief_projection_never_creates_new_bridge_size_failures():
    from dataclasses import replace

    from cloudra.runtime_v2.js_protocol import (
        ProgramLimits,
        _encode,
        encode_tool_error_frame,
        encode_tool_result_frame,
    )
    data = {'is_success': False, 'errors': [{'message': 'a'} for _ in range(200)]}
    envelope = {'is_success': False, 'data': data, 'summary': json.dumps(data, separators=(',', ':'))}
    original = _encode({'type': 'tool_result', 'request_id': 'r', 'result': envelope}, limits=ProgramLimits())
    limits = replace(ProgramLimits(), rpc_line_bytes=len(original))
    public = encode_tool_result_frame('r', envelope, limits=limits)
    assert len(public) <= len(original)
    assert project_feedback(project_feedback(data)) == project_feedback(data)
    error = {'code': 'tool_failed', 'message': 'a'}
    original_error = _encode({'type': 'tool_error', 'request_id': 'r', 'error': error}, limits=ProgramLimits())
    assert len(encode_tool_error_frame('r', error, limits=replace(limits, rpc_line_bytes=len(original_error)))) <= len(original_error)
    assert project_feedback({'verification_status': 'fail', 'verdict': 'fail: a'})['verdict'].startswith('fail:')


def test_noncanonical_json_summary_retains_measurements_without_growing_frame():
    from dataclasses import replace

    from cloudra.runtime_v2.js_protocol import ProgramLimits, _encode, encode_tool_result_frame
    summary = '{"error":' + json.dumps(CANARY) + ',"normal_values":[' + ','.join(['1e6'] * 100) + ']}'
    data = json.loads(summary)
    envelope = {'is_success': False, 'data': data, 'summary': summary}
    original = _encode({'type': 'tool_result', 'request_id': 'r', 'result': envelope}, limits=ProgramLimits())
    public = json.loads(encode_tool_result_frame('r', envelope, limits=replace(ProgramLimits(), rpc_line_bytes=len(original))))['result']
    assert public['data']['normal_values'] == data['normal_values']
    assert CANARY not in json.dumps(public['data'])
    assert public['summary'] == summary  # Explicit residual, not a new protocol failure.


def test_species_geometry_check_is_not_confused_with_native_geometry():
    raw = {'is_success': True, 'scientific_checks': {
        'geometry': {'status': 'failed', 'detail': CANARY, 'next_action': CANARY}},
        'geometry': {'atoms': [{'element': 'C', 'x': 1.2, 'y': -0.3, 'z': 0.0}]}}
    public = project_feedback(raw)
    assert CANARY not in json.dumps(public)
    assert public['scientific_checks']['geometry']['status'] == 'failed'
    assert public['geometry'] == raw['geometry']


def test_idpp_numerical_nonconvergence_is_not_a_scientific_verdict():
    from cloudra.tools.Chemtool.ts_guess import TsGuess_output_schema

    metadata = {'method': 'idpp', 'idpp_mode': 'standard', 'converged': False,
                'termination': 'max_steps', 'steps': 100, 'residual': 0.2, 'tolerance': 0.1}
    raw = TsGuess_output_schema(is_success=True, interpolation=metadata,
        message='Numerical termination: max_steps; convergence=False.').model_dump(mode='json')
    public = project_feedback(raw)
    assert public['interpolation'] == metadata
    assert public['is_success'] is True
    assert public['message'] == raw['message']
