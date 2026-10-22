"""Lossless, read-only public projection of owned TS scientific feedback.

This is not a scientific evaluator. It does not change execution outcomes or
authoritative records. Only known output schemas and owned text templates are
projected; unfamiliar mixed prose remains intact rather than losing evidence.
The short text marker ``?`` means judgment not provided, not a negative result.
"""

from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import replace
from typing import Any

_NOT_PROVIDED = "Scientific judgment not provided."
_SCIENTIFIC_OUTCOMES = frozenset({"verified", "candidate_only"})
_JUDGMENT_WORDS = frozenset({
    "verified", "candidate_only", "candidate", "pass", "fail", "inconclusive",
    "unlikely", "aligned", "misaligned", "undecidable",
})
# These are declarations, native material or raw evidence, not public diagnoses.
_RAW_FIELDS = frozenset({
    "input", "arguments", "content", "stdout", "stderr", "declarations",
    "native_output", "native_stdout", "native_stderr", "raw", "raw_output",
    "structures", "geometry", "coordinates", "methods", "calculation",
    "actual_calculation", "method_contract", "method_checks", "diagnostics",
})


def _is_view(value: dict) -> bool:
    return {"run_id", "revision", "run_dir", "stage", "status", "result"} <= value.keys()


def _is_record(value: dict) -> bool:
    return {"format_version", "run_id", "run_dir", "input", "stage_records", "job_steps", "terminal"} <= value.keys()


def _is_guess(value: dict) -> bool:
    return {"is_success", "verification_status", "verdict", "n_imag", "imag_freqs"} <= value.keys()


def _observed_text(text: Any) -> Any:
    """Remove only conclusions in fixed, owned templates, never guessed prose."""
    if not isinstance(text, str):
        return deepcopy(text)
    if text in _JUDGMENT_WORDS:
        return "?"

    # Preparation and stale-export facts are not part of the TS verdict.
    head, separator, tail = text.partition("\nPreparation performed:\n")
    if separator:
        projected = _observed_text(head)
        return (projected or "") + separator + tail
    head, separator, tail = text.partition("; JSON export is stale (revision ")
    if separator:
        previous, marker, remaining = tail.partition("); use this authoritative revision ")
        current, ending, remainder = remaining.partition(" and its current atom tables.")
        if previous.isdecimal() and marker and current.isdecimal() and ending and not remainder:
            return _observed_text(head) + separator + tail

    exact = {
        "no frequency job was run, so the stationary point is UNVERIFIED":
            "no frequency job was run; " + _NOT_PROVIDED,
        "the frequency job produced no frequency data, so the stationary point is UNVERIFIED":
            "the frequency job produced no frequency data; " + _NOT_PROVIDED,
        "pass: both actual IRC outer frames optimize to the expected zero-imaginary endpoint minima.":
            "Both optimized IRC outer frames: zero imaginary frequencies; ?",
        "fail: the strict check requires exactly one imaginary frequency.": _NOT_PROVIDED,
        "unlikely: no imaginary frequency; the structure looks more like a minimum.":
            "No imaginary frequency; " + _NOT_PROVIDED,
        "unlikely: multiple imaginary frequencies; the structure looks more like a higher-order saddle point.":
            "Multiple imaginary frequencies; " + _NOT_PROVIDED,
        "unlikely: the rough connectivity of the IRC endpoints is inconsistent with the expected structures.":
            _NOT_PROVIDED,
        "A normally terminated frequency job has no imaginary frequency: the structure is a minimum, not a first-order saddle point.":
            "A normally terminated frequency job has no imaginary frequency; " + _NOT_PROVIDED,
        "No imaginary frequency: the structure is a minimum, not like a first-order saddle point.":
            "No imaginary frequency; " + _NOT_PROVIDED,
        "at least one IRC endpoint does not lie within the pair-distance interval between the TS and either declared minimum":
            _NOT_PROVIDED,
        "the geometric change between the TS and the declared minima is too small to judge the direction of the IRC endpoints":
            _NOT_PROVIDED,
    }
    for pairing in ("direct", "swapped"):
        exact["each IRC endpoint lies between the TS and the corresponding declared minimum "
              f"({pairing} pairing; interval proof per irc_path.assign_irc_endpoints)"] = _NOT_PROVIDED
    if text in exact:
        return exact[text]
    prefix = (
        "Warning: endpoint optimization establishes the two path directions, "
        "but the geometric interval is unusual or could not be judged; inspect the trajectory. "
    )
    if text.startswith(prefix):
        return _observed_text(text[len(prefix):])

    # These producer-owned outer shells contain opaque labels, SMILES and
    # mixed evidence text. Keep the whole interior, without parsing ':' or '.'
    # inside paths/labels or guessing at the meaning of an inner diagnosis.
    prefix = "Verified TS connectivity to separated products "
    suffix = " minimum remains UNVERIFIED."
    if text.startswith(prefix) and text.endswith(suffix) and ". The bound complex " in text:
        return "Separated-product observations: " + text[len(prefix):-len(suffix)] + "; Not provided."
    prefix = "Separated-product IRC proof is incomplete: "
    if text.startswith(prefix):
        return "Separated-product IRC (no judgment): " + text[len(prefix):]

    for role in ("reactant", "product"):
        prefix = f"{role} endpoint optimization cannot support a minimum: "
        suffix = ". Revise this run with an explicit endpoint seed through ts_resume"
        if text.startswith(prefix) and text.endswith(suffix):
            return f"{role} endpoint optimization observations: " + text[len(prefix):]
        prefix = f"Declared {role} minimum is unverified: "
        if text.startswith(prefix):
            inner = text[len(prefix):]
            suffix = "; the complex remains unverified."
            if role == "reactant":
                return f"Declared {role} observations: " + inner
            if inner.endswith(suffix):
                return f"Declared {role} observations: " + inner[:-len(suffix)] + "; Not provided."
        for source in ("IRC side A", "IRC side B", "explicit species seed"):
            prefix = f"The {role} endpoint candidate from {source} did not qualify as an optimized minimum: "
            marker = f". Repair verification.{role}_endpoint.seed for the declared {role} "
            suffix = "; IRC A/B labels do not declare species identity."
            if text.startswith(prefix) and marker in text and text.endswith(suffix):
                return f"{role} endpoint from {source} (no judgment): " + text[len(prefix):]

    prefix = (
        "The optimized IRC outer frames did not establish one consistent species identity, "
        "source provenance, and actual outer-frame optimization lineage: "
    )
    suffix = ". These observations do not override the failed checks. The candidate stays UNVERIFIED"
    if text.startswith(prefix) and text.endswith(suffix):
        return "IRC outer-frame observations: " + text[len(prefix):-len(suffix)] + "; " + _NOT_PROVIDED

    prefix = "frequency analysis found "
    marker = "; the candidate is "
    if text.startswith(prefix) and marker in text:
        observation, _, conclusion = text.partition(marker)
        count, count_marker, _ = observation[len(prefix):].partition(" imaginary mode(s) (")
        if count.isdecimal() and count_marker and observation.endswith(")"):
            kind = "a local minimum" if count == "0" else f"a point with {count} imaginary modes"
            expected = (kind + ", not a first-order saddle point. This falsifies the candidate — it does NOT "
                        "mean the reaction is impossible")
            if conclusion == expected:
                return observation + "; " + _NOT_PROVIDED

    prefix = "frequency analysis supports a first-order saddle point ("
    suffix = (
        " cm^-1, exactly one imaginary mode), but no IRC was run: the two path directions were not checked to "
        "connect the declared minima. The candidate is a plausible saddle, NOT a verified one "
        "(submitting IRC needs the native %irc settings that live in the engine skill)"
    )
    if text.startswith(prefix) and text.endswith(suffix):
        frequency = text[len(prefix):-len(suffix)]
        return f"Frequency observation: {frequency} cm^-1, exactly one imaginary mode; no IRC was run. {_NOT_PROVIDED}"

    prefix = "verified transition state: exactly one imaginary mode ("
    marker = (
        " cm^-1), both actual IRC outer frames from the same TS optimized independently to zero-imaginary-frequency minima "
        "with the declared reactant and product identities (origins="
    )
    if text.startswith(prefix) and marker in text:
        frequency, _, rest = text[len(prefix):].partition(marker)
        origins, separator, advisory = rest.partition("). Geometry interval advisory: ")
        if separator:
            return (f"Frequency observation: exactly one imaginary mode ({frequency} cm^-1); origins={origins}. "
                    "Both optimized endpoints: zero imaginary frequencies. "
                    f"{_NOT_PROVIDED} Geometry interval advisory: {_observed_text(advisory)}")

    for prefix, suffix in (
        ("the frequency job's log was not found at its registered location ",
         "; without it the stationary point is UNVERIFIED"),
        ("the declared IRC log does not exist at ", "; the candidate stays unverified"),
    ):
        if text.startswith(prefix) and text.endswith(suffix):
            # Keep the entire path, including spaces, punctuation and verdict words.
            return text[:-len(suffix)] + "; Not provided."

    for prefix in (
        "Imaginary mode is consistent with the declared reaction coordinate: ",
        "Imaginary mode is inconsistent with the declared reaction coordinate: ",
    ):
        if text.startswith(prefix):
            return "Mode observations: " + text[len(prefix):]

    prefix = "The imaginary mode's dominant motion is on the NON-BONDED atom pair "
    suffix = (
        ": a torsion/angle-dominated mode (hindered rotation, ring flip, pyramidal inversion) "
        "barely moves bonded-pair distances, so pair-distance alignment against watch_pairs cannot judge its "
        "direction. The material is insufficient for a pass/fail verdict."
    )
    if text.startswith(prefix) and text.endswith(suffix):
        return "Dominant mode atom pair " + text[len(prefix):-len(suffix)] + "; " + _NOT_PROVIDED

    prefix = "TS frequency evidence has "
    suffix = " imaginary modes; exactly one is required before IRC."
    if text.startswith(prefix) and text.endswith(suffix):
        count = text[len(prefix):-len(suffix)]
        if count.isdecimal():
            return prefix + count + " imaginary modes; " + _NOT_PROVIDED

    for suffix in (
        ": the first-order saddle-point premise holds.",
        ": acceptable as a first-order saddle-point candidate, but this is not sufficient proof.",
    ):
        if text.startswith("Exactly 1 imaginary frequency (") and text.endswith(suffix):
            return text[:-len(suffix)] + "; Not provided."

    prefix = "TS verification complete: "
    if text.startswith(prefix):
        remainder = text[len(prefix):]
        projected = _observed_text(remainder)
        if projected != remainder:
            return projected
    return text


def _frequency(value: Any) -> Any:
    out = deepcopy(value)
    if not isinstance(out, dict):
        return out
    alignment = out.get("mode_alignment")
    if isinstance(alignment, dict) and {"status", "aligned", "message"} <= alignment.keys():
        alignment["aligned"] = None
        if alignment["status"] in _JUDGMENT_WORDS:
            alignment["status"] = None
        alignment["message"] = _observed_text(alignment["message"])
        # Numeric displacement details, geometry and evidence hashes stay exact.
    return out


def _record_parts(out: dict) -> dict:
    if out.get("terminal") in _SCIENTIFIC_OUTCOMES:
        out["terminal"] = None
    for stage in out.get("stage_records", []):
        if isinstance(stage, dict) and "detail" in stage:
            stage["detail"] = _observed_text(stage["detail"])
    for step in [*out.get("job_steps", []), out.get("scan_step")]:
        if isinstance(step, dict) and "frequency_analysis" in step:
            step["frequency_analysis"] = _frequency(step["frequency_analysis"])
    for history in out.get("attempt_history", []):
        if isinstance(history, dict):
            _record_parts(history)
    _scientific_diagnostics(out)
    return out


def _scientific_diagnostics(out: dict) -> None:
    for diagnostic in [out.get("blocked"), out.get("failed_attempt"), *out.get("candidate_attempts", [])]:
        if not isinstance(diagnostic, dict):
            continue
        if diagnostic.get("failure_class") in {"wrong_mode", "endpoint_unconfirmed"}:
            diagnostic["failure_class"] = None
            if "message" in diagnostic:
                diagnostic["message"] = _observed_text(diagnostic["message"])


def project_scientific_feedback(value: Any) -> Any:
    """Detach JSON-like public output and project only identified TS schemas."""
    if isinstance(value, list):
        return [project_scientific_feedback(item) for item in value]
    if not isinstance(value, dict):
        return deepcopy(value)
    out = {key: deepcopy(item) if key in _RAW_FIELDS else project_scientific_feedback(item)
           for key, item in value.items()}
    if _is_view(value):
        verdict = out.get("result")
        if isinstance(verdict, dict) and {"outcome", "verified", "reason", "evidence_refs"} <= verdict.keys():
            if verdict["outcome"] in _SCIENTIFIC_OUTCOMES:
                verdict["outcome"] = None
            verdict["verified"] = None
            verdict["reason"] = _observed_text(verdict["reason"])
        if "message" in out:
            out["message"] = _observed_text(out["message"])
        if "frequency_analysis" in out:
            out["frequency_analysis"] = _frequency(out["frequency_analysis"])
        for stage in out.get("available_results", []):
            if isinstance(stage, dict) and "detail" in stage:
                stage["detail"] = _observed_text(stage["detail"])
        _scientific_diagnostics(out)
    if _is_record(value):
        _record_parts(out)
    if _is_guess(value):
        if out["verification_status"] in _JUDGMENT_WORDS:
            out["verification_status"] = None
        for key in ("verdict", "message", "imag_mode_alignment"):
            if key in out:
                out[key] = _observed_text(out[key])
        if "imag_mode_aligned" in out:
            out["imag_mode_aligned"] = None
        for key in ("checks", "verdicts"):
            if isinstance(out.get(key), list):
                out[key] = [_observed_text(item) for item in out[key]]
    return out


def _summary(text: Any) -> Any:
    if not isinstance(text, str):
        return deepcopy(text)
    try:
        parsed = json.loads(text)
    except (TypeError, ValueError):
        return text
    projected = project_scientific_feedback(parsed)
    if projected == parsed:
        return text
    return json.dumps(projected, ensure_ascii=False, separators=(",", ":"))


def project_scientific_tool_result(result: Any) -> Any:
    """Copy a ToolResult or wire envelope; never change its execution controls."""
    if isinstance(result, dict):
        out = deepcopy(result)
        if "data" in out:
            out["data"] = project_scientific_feedback(out["data"])
        if "summary" in out:
            out["summary"] = _summary(out["summary"])
        return out
    return replace(result, data=project_scientific_feedback(result.data), summary=_summary(result.summary))


def project_scientific_notice(text: str, *, key: str = "") -> str:
    """Render owned notices neutrally without changing durable notice events."""
    prefix = "[Guidance] The target TS step remains unverified; "
    if key.startswith("guidance-scientific-reflection:ts-process:") and text.startswith(prefix):
        return "[Guidance] Judgment not provided; " + text[len(prefix):]
    if not text.startswith("Compute Event: Job ") or " TS " not in text.splitlines()[0]:
        return text
    lines = text.splitlines(keepends=True)
    for index, line in enumerate(lines):
        ending = "\n" if line.endswith("\n") else ""
        content = line.removesuffix("\n")
        if content == "NEXT: Submit the verified native logs through the DAG evidence tools.":
            lines[index] = "NEXT: Inspect the native logs and evidence." + ending
            continue
        suffix = " for the verified evidence, then submit its native logs through the DAG evidence tools."
        if content.startswith("NEXT: Use ts_inspect(run_id=") and content.endswith(suffix):
            lines[index] = content[:-len(suffix)] + " to inspect the native evidence." + ending
            continue
        prefix = "Advisory from ts_guess: "
        if content.startswith(prefix):
            lines[index] = prefix + (_observed_text(content[len(prefix):]) or "Not provided.") + ending
            continue
        prefix = "Physical Reality: "
        if not line.startswith(prefix):
            continue
        body = line[len(prefix):].removesuffix("\n")
        outcome = ""
        if body.startswith("outcome="):
            outcome, separator, body_tail = body.partition("; ")
            if not separator:
                continue
            body = body_tail
        flag, separator, reason = body.partition(". ")
        if flag not in {"verified=true", "verified=false", "verified=true.", "verified=false."}:
            continue
        retained = "" if outcome.removeprefix("outcome=") in _SCIENTIFIC_OUTCOMES else outcome
        observed = _observed_text(reason) if separator else ""
        body = "; ".join(part for part in (retained, observed) if part) or "Not provided."
        lines[index] = prefix + body + ending
    return "".join(lines)


def public_scientific_record(record: Any) -> dict:
    """Export a detached dict; standalone authoritative JSON stays unmodified."""
    value = record.model_dump(mode="json") if hasattr(record, "model_dump") else deepcopy(record)
    return project_scientific_feedback(value) if value.get("pipeline_id") else value
