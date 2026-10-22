"""D-arm public feedback projection, never a decision or persistence policy.

Call only at model/guest/export boundaries. Authoritative tool results, gates,
reviews and database records retain their full diagnostics. This is an
information ablation, not an OS sandbox: shell access to audit storage and
native scientific logs is deliberately unchanged.
"""
from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import replace
from typing import Any

OMITTED = 'Diagnostic details omitted.'
_FAILED = frozenset({'failed', 'fail', 'blocked', 'rejected', 'reject', 'disagree',
                     'needs_evidence', 'incomplete', 'invalid', 'misaligned', 'undecidable',
                     'candidate_only', 'search_failed', 'invalid_input', 'inconclusive', 'error', 'continue_work'})
# These names are diagnostic only in an established failure object. Do not
# erase equally named scientific observations or normal successful outputs.
_TEXT = frozenset({'message', 'msg', 'summary', 'reason', 'detail', 'next_action',
                   'recovery_hint', 'repair_hint', 'recommendation', 'rationale'})
_ALWAYS_TEXT = frozenset({'error', 'last_error', 'error_message', 'planned_error', 'reject_reason'})
_CONTEXTS = frozenset({'error', 'errors', 'validation_errors', 'blocked', 'failed_attempt', 'unresolved_gaps',
                       'delivery_gaps', 'unresolved', 'inconclusive'})
_LOCATION = frozenset({'atom_details', 'needs', 'required_inputs', 'repair_actions',
                       'next_steps'})
# Native outputs, numerical facts and explicit declarations are not diagnostics.
_OPAQUE = frozenset({'arguments', 'input', 'effective_arguments', 'structures',
                    'coordinates', 'frequencies', 'stdout', 'stderr',
                    'content'})


def brief_text(text: str) -> str:
    """Keep an existing coarse protocol category; never infer a new verdict."""
    if not text or text == OMITTED:
        return text
    if text.startswith('Invalid tool arguments:'):
        return 'Invalid tool arguments.'
    if text == 'Invalid tool arguments.':
        return text
    if text.startswith('protocol_error['):
        category, end, _ = text.partition(']')
        if end:
            return category + ']'
    return OMITTED if len(text.encode('utf-8')) >= len(OMITTED) else '-'


def _bounded_text(original: str, public: str) -> str:
    # JSON string escaping matters to bridge limits, not Python character count.
    def size(text):
        return len(json.dumps(text, ensure_ascii=False).encode('utf-8'))
    return public if size(public) <= size(original) else original


def _failure(value: dict) -> bool:
    return (value.get('is_success') is False or value.get('passed') is False or bool(value.get('failure_class'))
            or any(isinstance(value.get(key), str) and value[key] in _FAILED
                   for key in ('status', 'state', 'outcome', 'verdict', 'action', 'verification_status')))


def _locations(value: Any) -> Any:
    if isinstance(value, str):
        return brief_text(value)
    if isinstance(value, list):
        return [_locations(item) for item in value]
    if isinstance(value, dict):
        return project_feedback(value, diagnostic=True)
    return deepcopy(value)


def project_feedback(value: Any, *, diagnostic: bool = False) -> Any:
    """Copy structured feedback, shortening only diagnostic text/localization.

    Categories, status/code/target IDs, numbers, booleans, nulls, effect state,
    control decisions, evidence paths, native outputs and partial data survive.
    Successful queries still traverse nested failure objects. No regular
    expressions, mutation of caller objects, or interpretation of prose.
    """
    if isinstance(value, list):
        return [project_feedback(item, diagnostic=diagnostic) if not isinstance(item, str)
                else brief_text(item) if diagnostic else item for item in value]
    if not isinstance(value, dict):
        return brief_text(value) if diagnostic and isinstance(value, str) else deepcopy(value)
    failed = diagnostic or _failure(value)
    out = {}
    for key, item in value.items():
        if key in _OPAQUE or (key == 'manifest' and isinstance(item, dict)
                             and item.get('kind') == 'exit_review_decision'):
            out[key] = deepcopy(item)
        elif key in _ALWAYS_TEXT and isinstance(item, str):
            out[key] = brief_text(item)
        elif key == 'final_summary' and isinstance(item, str):
            out[key] = brief_text(item) if value.get('final_summary_source') == 'run_error' else _bounded_text(item, project_notice(item))
        elif key == 'verdict' and value.get('verification_status') in {'fail', 'inconclusive'} and isinstance(item, str):
            category, marker, detail = item.partition(': ')
            out[key] = category + marker + brief_text(detail) if marker else item
        elif key == 'imag_mode_alignment' and value.get('imag_mode_aligned') is False and isinstance(item, str):
            out[key] = brief_text(item)
        elif key in {'checks', 'verdicts'} and isinstance(item, list):
            # This owned standalone instruction contains no observed data.
            # Other legacy entries mix measurements and explanations: retain
            # them, rather than guessing which scientific facts to discard.
            remedy = ('Optimize each actual IRC outer frame to its endpoint minimum and confirm zero imaginary '
                      'frequencies. Submit the native Opt/Freq logs as reactant_logs / product_logs '
                      '(combined or separate logs), with reactant_path / product_path identifying the expected species.')
            out[key] = [OMITTED if row == remedy else project_feedback(row) for row in item]
        elif failed and key in _TEXT and isinstance(item, str):
            before, marker, preparation = item.partition('\nPreparation performed:')
            out[key] = brief_text(before) + marker + preparation
        elif failed and key in _LOCATION:
            out[key] = _locations(item)
        elif diagnostic and key in {'field', 'loc'}:
            out[key] = _locations(item)
        else:
            # Do not spread a parent's failure to normal result data. Specific
            # failure containers and each child's own status carry the context.
            child_failure = key in _CONTEXTS or (key == 'issues' and failed)
            if key == 'next' and failed:
                child_failure = True
            if key == 'next_steps' and isinstance(value.get('last_run'), dict):
                child_failure = value['last_run'].get('outcome') == 'failed'
            out[key] = project_feedback(item, diagnostic=child_failure)
    return out


def project_tool_result(result, *, tool_name: str = ''):
    """Return a detached public ToolResult without changing error semantics."""
    data = project_feedback(result.data, diagnostic=not result.is_success)
    native = tool_name in {'bash', 'read', 'log_parser'}
    if tool_name and not native and not result.is_success and isinstance(data.get('result'), str):
        data['result'] = brief_text(data['result'])
    summary = result.summary
    try:
        parsed, end = json.JSONDecoder().raw_decode(summary)
    except (ValueError, TypeError):
        if not result.is_success and tool_name != 'js_exec':
            summary = brief_text(summary)
    else:
        public = project_feedback(parsed, diagnostic=not result.is_success)
        if parsed == result.data:
            public = data
        if public != parsed:
            # Rare noncanonical numeric spellings can expand when re-encoded.
            # Retain that original summary rather than changing bridge outcomes
            # or dropping its normal observations. Structured data stays brief.
            summary = _bounded_text(summary, json.dumps(public, ensure_ascii=False, separators=(',', ':')) + summary[end:])
    error = replace(result.error, message=brief_text(result.error.message)) if result.error else None
    return replace(result, summary=summary, data=data, error=error)


def project_notice(content: str, *, key: str = '') -> str:
    """Project only owned, recognizable notification formats; not agent prose."""
    if key.startswith('guidance-scientific-reflection:'):
        causes = ('The parsed scan found no internal peak.', 'Structured TS verification failed.',
                  'The xTB path refinement exhausted its cycle ceiling.',
                  'This TS optimization did not converge.')
        for cause in causes:
            if content.startswith('[Guidance] ' + cause):
                return '[Guidance] ' + cause
        if content.startswith('[Guidance] This TS optimization did not converge;'):
            return '[Guidance] This TS optimization did not converge.'
        return '[Guidance] The target TS step remains unverified.'
    if content.startswith(('[Supervisor call verdict]', '[Supervisor draft verdict]',
                           '[Supervisor review decision]')):
        head, separator, _ = content.partition(' reason=')
        if separator and any('verdict=' + state in head.split() for state in _FAILED):
            return head + ' reason=' + OMITTED
    if content.startswith('[Review superseded]'):
        return content.partition(' reason=')[0] + ' reason=' + OMITTED
    if content.startswith('[Completion gate] This run cannot finish yet:'):
        lines = ['[Completion gate] action=continue_work. ' + OMITTED]
        for line in content.splitlines():
            if line.startswith('- ') and ': ' in line:
                lines.append(line.partition(': ')[0])
        # Keep the no-progress counter and consequence, not repair advice.
        marker = 'Exit attempt '
        if marker in content:
            lines.append(marker + content.rsplit(marker, 1)[1])
        return '\n'.join(lines)
    if key == 'supervisor-research-observation' and 'workflow_verified=true' not in content:
        return '\n'.join('Recorded check: ' + OMITTED if line.startswith('Recorded check:') else line
                         for line in content.splitlines())
    if content.startswith('Compute Event: '):
        # Unverified observations, normal stops and partial results are not
        # failures. Use only explicit states/outcomes or the owned advisory.
        lines = content.splitlines()
        failed = ('state=failed.' in lines[0] or any(
            line.startswith('Advisory from ts_guess: ')
            or any(line.startswith(f'Physical Reality: outcome={outcome};') for outcome in _FAILED)
            for line in lines))
        return project_compute_notice(content, failed=failed)
    if content.startswith('[Completion gate] Run ended as failed:'):
        head, separator, _ = content.partition(' (latest: ')
        if separator:
            return head + '. The run was NOT marked complete.'
    return content


def project_compute_notice(content: str, *, failed: bool) -> str:
    if not failed:
        return content
    lines = []
    for line in content.splitlines():
        if line.startswith('Physical Reality: '):
            text = line.removeprefix('Physical Reality: ')
            if text.startswith('outcome=') or text.startswith('verified='):
                text = text.partition('.')[0] + '.'
                lines.append('Physical Reality: ' + text)
            else:
                lines.append('Physical Reality: ' + OMITTED)
        elif line == 'NEXT: Do not resubmit or restart without a new explicit user request.':
            lines.append(line)
        elif line.startswith(('Process: ', 'Advisory from ts_guess: ', 'NEXT: ')):
            lines.append(line.partition(':')[0] + ': ' + OMITTED)
        else:
            lines.append(line)
    return '\n'.join(lines)


def public_process_record(record: dict) -> dict:
    """Only redact exports with a durable DB authority, never the sole record."""
    if not record.get('pipeline_id'):
        return deepcopy(record)
    return project_feedback(record)
