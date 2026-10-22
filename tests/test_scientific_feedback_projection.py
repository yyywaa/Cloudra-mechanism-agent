"""Public scientific feedback is separate from execution state and raw facts."""

import json
from copy import deepcopy

import pytest

from cloudra.runtime_v2.js_protocol import encode_tool_result_frame


def _view():
    return {
        "run_id": "ts_0001", "revision": 2, "run_dir": "/work/ts_0001",
        "status": "ended", "stage": "verdict",
        "result": {"outcome": "verified", "verified": True,
                   "reason": "verified", "evidence_refs": ["/work/freq.out"]},
    }


def test_js_public_frame_hides_scientific_verdict_without_changing_execution():
    raw = {"is_success": True, "summary": "", "data": _view(), "error": None}
    frame = json.loads(encode_tool_result_frame("r1", raw))
    projected = frame["result"]
    assert projected["data"]["result"]["verified"] is None
    assert projected["data"]["result"]["outcome"] is None
    assert projected["is_success"] is True
    assert projected["data"]["status"] == "ended"
    assert raw["data"]["result"]["verified"] is True


def _project(value):
    from cloudra.runtime_v2.scientific_feedback import project_scientific_feedback

    return project_scientific_feedback(value)


def _record():
    return {
        "format_version": 7, "run_id": "ts_0001", "pipeline_id": "p1",
        "run_dir": "/work/ts_0001", "stage": "verdict", "terminal": "verified",
        "input": {"reaction": {"status": "verified", "passed": True}},
        "stage_records": [{"stage": "verdict", "status": "done", "detail": "verified"}],
        "job_steps": [], "attempt_history": [],
    }


@pytest.mark.parametrize("outcome", ["verified", "candidate_only"])
def test_known_ts_view_hides_judgment_in_nested_lists_without_mutation(outcome):
    view = _view()
    view["result"]["outcome"] = outcome
    raw = {"processes": [{"process": view}]}
    original = deepcopy(raw)
    public = _project(raw)
    verdict = public["processes"][0]["process"]["result"]
    assert verdict["outcome"] is None
    assert verdict["verified"] is None
    assert verdict["evidence_refs"] == ["/work/freq.out"]
    assert raw == original
    verdict["evidence_refs"].append("changed public copy")
    assert raw == original


@pytest.mark.parametrize("outcome", ["failed", "cancelled", "search_failed", "invalid_input"])
def test_execution_failure_outcomes_and_diagnostics_are_preserved(outcome):
    view = _view()
    view["result"].update(outcome=outcome, verified=False, reason="invalid_input: atom 9 missing")
    view["waiting_for"] = [{"state": outcome, "passed": False}]
    public = _project(view)
    assert public["result"]["outcome"] == outcome
    assert public["result"]["verified"] is None
    assert public["result"]["reason"] == "invalid_input: atom 9 missing"
    assert public["waiting_for"] == view["waiting_for"]


def test_unrelated_generic_statuses_and_user_owned_subtrees_are_untouched():
    raw = {
        "status": "verified", "verified": True, "passed": True, "verdict": "pass",
        "result": {"outcome": "verified", "verified": True},
        **{key: _view() for key in (
            "input", "arguments", "content", "stdout", "stderr", "declarations", "native_output",
        )},
    }
    assert _project(raw) == raw


def test_ts_view_numeric_evidence_and_mode_details_are_lossless():
    view = _view()
    view["frequency_analysis"] = {
        "log_path": "/work/verified/freq.out", "log_sha256": "abc",
        "modes": [{"frequency_cm1": -321.5, "atom_fractions": [0.2, 0.8]}],
        "mode_alignment": {"status": "aligned", "aligned": True,
            "message": "Imaginary mode is consistent with the declared reaction coordinate: watch_pairs max relative displacement 0.500 ≥ 0.50×global max 0.600 (max pair=(1,2)).",
            "details": ["Atom pair (1,2) relative displacement=0.500 (threshold 0.50×0.600=0.300)"]},
    }
    view["structures"] = {"reactant": {"geometry": [[1.2, 0.0, -0.2]], "status": "verified"}}
    view["available_results"] = [{"stage": "frequency", "status": "done", "artifacts": ["/work/freq.out"]}]
    public = _project(view)
    alignment = public["frequency_analysis"]["mode_alignment"]
    assert alignment["aligned"] is None
    assert alignment["status"] is None
    assert "consistent with" not in alignment["message"]
    assert "0.500 ≥ 0.50×global max 0.600 (max pair=(1,2))" in alignment["message"]
    assert alignment["details"] == view["frequency_analysis"]["mode_alignment"]["details"]
    for key in ("modes", "log_path", "log_sha256"):
        assert public["frequency_analysis"][key] == view["frequency_analysis"][key]
    assert public["structures"] == view["structures"]
    assert public["available_results"] == view["available_results"]


@pytest.mark.parametrize(("reason", "facts", "removed"), [
    ("frequency analysis found 2 imaginary mode(s) ([-321.5, -12.0]); the candidate is a point with 2 imaginary modes, not a first-order saddle point. This falsifies the candidate — it does NOT mean the reaction is impossible",
     "frequency analysis found 2 imaginary mode(s) ([-321.5, -12.0])", "falsifies"),
    ("frequency analysis supports a first-order saddle point (-321.5 cm^-1, exactly one imaginary mode), but no IRC was run: the two path directions were not checked to connect the declared minima. The candidate is a plausible saddle, NOT a verified one (submitting IRC needs the native %irc settings that live in the engine skill)",
     "-321.5 cm^-1", "plausible saddle"),
    ("verified transition state: exactly one imaginary mode (-321.5 cm^-1), both actual IRC outer frames from the same TS optimized independently to zero-imaginary-frequency minima with the declared reactant and product identities (origins={'A': 'reactant', 'B': 'product'}). Geometry interval advisory: RMSD=0.12; source=/work/irc.out",
     "RMSD=0.12; source=/work/irc.out", "verified transition state"),
    ("the frequency job's log was not found at its registered location /work/freq.out; without it the stationary point is UNVERIFIED",
     "/work/freq.out", "UNVERIFIED"),
    ("the declared IRC log does not exist at /work/irc.out; the candidate stays unverified",
     "/work/irc.out", "unverified"),
])
def test_owned_mixed_reasons_preserve_observations_and_paths(reason, facts, removed):
    view = _view()
    view["result"]["reason"] = reason
    view["message"] = reason
    public = _project(view)
    for value in (public["message"], public["result"]["reason"]):
        assert facts in value
        assert removed not in value
        assert len(value.encode()) <= len(reason.encode())


def test_unknown_mixed_scientific_text_is_preserved_not_guessed():
    reason = "verified by custom procedure, frequency=-17.0; RMSD 0.9; evidence /work/pass.xyz"
    view = _view()
    view["result"]["reason"] = reason
    view["message"] = reason
    public = _project(view)
    assert public["result"]["reason"] == reason
    assert public["message"] == reason


def test_owned_record_history_and_stages_project_but_native_declarations_do_not():
    record = _record()
    history = {key: deepcopy(record[key]) for key in ("terminal", "input", "stage_records", "job_steps")}
    history["declaration_revision"] = 1
    record["attempt_history"] = [history]
    record["job_steps"] = [{"purpose": "frequency", "state": "done", "frequency_analysis": {
        "mode_alignment": {"status": "misaligned", "aligned": False, "message": "unusual raw result", "details": ["RMSD=1.2"]},
    }}]
    public = _project(record)
    assert public["terminal"] is None
    assert public["stage_records"][0]["status"] == "done"
    assert public["stage_records"][0]["detail"] == "?"
    assert public["attempt_history"][0]["terminal"] is None
    assert public["attempt_history"][0]["input"] == history["input"]
    assert public["job_steps"][0]["state"] == "done"
    assert public["job_steps"][0]["frequency_analysis"]["mode_alignment"]["aligned"] is None
    assert public["input"] == record["input"]


def test_public_export_projects_pipeline_records_only():
    from cloudra.runtime_v2.scientific_feedback import public_scientific_record

    record = _record()
    assert public_scientific_record(record)["terminal"] is None
    record["pipeline_id"] = ""
    assert public_scientific_record(record) == record
    assert record["terminal"] == "verified"


@pytest.mark.parametrize("status", ["pass", "fail", "candidate", "inconclusive"])
def test_known_ts_guess_schema_hides_conclusions_not_execution_or_numbers(status):
    raw = {
        "is_success": True, "message": "TS verification complete: pass: both actual IRC outer frames optimize to the expected zero-imaginary endpoint minima.",
        "verification_status": status, "verdict": "pass: both actual IRC outer frames optimize to the expected zero-imaginary endpoint minima.",
        "n_imag": 1, "imag_freqs": [-321.5], "imag_mode_aligned": False,
        "imag_mode_alignment": "Imaginary mode is inconsistent with the declared reaction coordinate: watch_pairs max relative displacement 0.100 < 0.50×global max 0.600 (dominant motion on atom pair (1,2)).",
        "checks": ["IRC outer frames extracted: irc_end_a.xyz (rx=-2.0), irc_end_b.xyz (rx=3.0) -> /work/irc", "RMSD=0.112"],
        "irc_end_a_path": "/work/a.xyz", "irc_end_b_path": "/work/b.xyz",
    }
    public = _project(raw)
    assert public["is_success"] is True
    assert public["verification_status"] is None
    assert public["imag_mode_aligned"] is None
    assert "pass:" not in public["message"]
    assert "pass:" not in public["verdict"]
    for key in ("n_imag", "imag_freqs", "checks", "irc_end_a_path", "irc_end_b_path"):
        assert public[key] == raw[key]


def test_tool_result_type_controls_raw_data_and_json_summary_are_preserved():
    from cloudra.runtime_v2.policies.base import ToolResult
    from cloudra.runtime_v2.scientific_feedback import project_scientific_tool_result

    raw = ToolResult(is_success=False, data=_view(), summary=json.dumps(_view()), duration_ms=42)
    public = project_scientific_tool_result(raw)
    assert isinstance(public, ToolResult)
    assert public.is_success is False
    assert public.error is raw.error
    assert public.duration_ms == 42
    assert json.loads(public.summary) == public.data
    assert public.data["result"]["verified"] is None
    assert raw.data["result"]["verified"] is True
    assert json.loads(raw.summary)["result"]["verified"] is True


def test_tool_result_non_json_raw_summary_is_not_rewritten():
    from cloudra.runtime_v2.policies.base import ToolResult
    from cloudra.runtime_v2.scientific_feedback import project_scientific_tool_result

    summary = 'stdout: {"verified": true}; native frequency -321.5'
    raw = ToolResult(is_success=False, data={"status": "failed"}, summary=summary)
    assert project_scientific_tool_result(raw) == raw


def test_owned_compute_notice_preserves_job_status_numbers_and_evidence():
    from cloudra.runtime_v2.scientific_feedback import project_scientific_notice

    text = ("Compute Event: Job 23, state=failed. TS ts_0001: verdict / frequency.\n"
            "Physical Reality: outcome=candidate_only; verified=false. frequency analysis found 2 imaginary mode(s) ([-321.5, -12.0]); the candidate is a point with 2 imaginary modes, not a first-order saddle point. This falsifies the candidate — it does NOT mean the reaction is impossible\n"
            "NEXT: Use ts_inspect(run_id='ts_0001') for diagnostics, then revise the research input with ts_resume as needed.\n"
            "Evidence: Log: /work/freq.out; Details: /work/process.json")
    public = project_scientific_notice(text)
    assert public.splitlines()[0] == text.splitlines()[0]
    assert "candidate_only" not in public
    assert "verified=false" not in public
    assert "[-321.5, -12.0]" in public
    assert public.splitlines()[-1] == text.splitlines()[-1]


def test_owned_guidance_and_unknown_notices_are_context_scoped():
    from cloudra.runtime_v2.scientific_feedback import project_scientific_notice

    text = "[Guidance] The target TS step remains unverified; Source: /work/freq.out. Check the source."
    public = project_scientific_notice(text, key="guidance-scientific-reflection:ts-process:ts_0001")
    assert "unverified" not in public
    assert "Source: /work/freq.out. Check the source." in public
    assert project_scientific_notice(text, key="user-note") == text
    assert project_scientific_notice("User says verified=true. RMSD=0.2") == "User says verified=true. RMSD=0.2"


def test_projection_is_idempotent_and_never_expands_short_judgment_values():
    raw = _view()
    raw["result"]["reason"] = "pass"
    public = _project(raw)
    assert _project(public) == public
    assert len(json.dumps(public).encode()) <= len(json.dumps(raw).encode())


def test_scientific_block_preserves_workflow_stop_raw_count_and_real_failure():
    view = _view()
    view["status"] = "blocked"
    view["result"] = None
    message = "TS frequency evidence has 2 imaginary modes; exactly one is required before IRC."
    view["message"] = message
    view["blocked"] = {"failure_class": "wrong_mode", "stage": "refine", "message": message,
                       "needs": ["guess"], "atom_details": ["frequency=-321.5"]}
    view["failed_attempt"] = {"failure_class": "wrong_mode", "log_path": "/work/freq.out"}
    public = _project(view)
    assert public["status"] == "blocked"
    assert public["blocked"]["failure_class"] is None
    assert "2 imaginary modes" in public["blocked"]["message"]
    assert "exactly one is required" not in public["blocked"]["message"]
    assert public["failed_attempt"]["failure_class"] is None
    assert public["blocked"]["atom_details"] == ["frequency=-321.5"]
    view["blocked"]["failure_class"] = "job_failed"
    view["blocked"]["message"] = "SCF failed; native exit code 2"
    view["failed_attempt"]["failure_class"] = "nonconvergence"
    public = _project(view)
    assert public["blocked"] == view["blocked"]
    assert public["failed_attempt"] == view["failed_attempt"]


def test_owned_compute_notice_does_not_leak_verdict_through_next_or_advisory():
    from cloudra.runtime_v2.scientific_feedback import project_scientific_notice

    text = ("Compute Event: Job 23, state=done. TS ts_0001: verdict.\n"
            "Physical Reality: outcome=verified; verified=true. verified\n"
            "Advisory from ts_guess: Imaginary mode is inconsistent with the declared reaction coordinate: watch_pairs max relative displacement 0.100 < 0.50×global max 0.600 (dominant motion on atom pair (1,2)).\n"
            "NEXT: Submit the verified native logs through the DAG evidence tools.\n"
            "Evidence: Log: /work/verified.out")
    public = project_scientific_notice(text)
    assert "verified=true" not in public
    assert "Submit the verified native logs" not in public
    assert "inconsistent with the declared reaction coordinate" not in public
    assert "0.100 < 0.50×global max 0.600" in public
    assert "/work/verified.out" in public


def test_mode_undecidable_template_keeps_atom_pair_without_classification():
    view = _view()
    view["frequency_analysis"] = {"mode_alignment": {"status": "undecidable", "aligned": None,
        "message": "The imaginary mode's dominant motion is on the NON-BONDED atom pair (3,4): a torsion/angle-dominated mode (hindered rotation, ring flip, pyramidal inversion) barely moves bonded-pair distances, so pair-distance alignment against watch_pairs cannot judge its direction. The material is insufficient for a pass/fail verdict.",
        "details": ["Atom pair (1,2) relative displacement=0.100"]}}
    public = _project(view)["frequency_analysis"]["mode_alignment"]
    assert "(3,4)" in public["message"]
    assert "torsion/angle-dominated" not in public["message"]
    assert public["details"] == view["frequency_analysis"]["mode_alignment"]["details"]


@pytest.mark.parametrize("reason", ["pass", "fail", "verified", "candidate_only"])
def test_pure_verdict_text_keeps_string_type_and_uses_short_unprovided_marker(reason):
    view = _view()
    view["result"]["reason"] = reason
    view["message"] = reason
    public = _project(view)
    assert public["message"] == "?"
    assert public["result"]["reason"] == "?"
    assert len(json.dumps(public).encode()) <= len(json.dumps(view).encode())


@pytest.mark.parametrize("with_summary", [False, True])
def test_accepted_exact_size_js_frame_is_not_expanded(with_summary):
    from cloudra.runtime_v2.js_protocol import ProgramLimits

    raw = {"data": {"unrelated": "x"}}
    if with_summary:
        raw["summary"] = "ok"
    frame_size = len(json.dumps({"type": "tool_result", "request_id": "r1", "result": raw}, ensure_ascii=False).encode())
    frame = encode_tool_result_frame("r1", raw, limits=ProgramLimits(rpc_line_bytes=frame_size))
    assert len(frame) <= frame_size
    assert json.loads(frame)["result"] == raw


@pytest.mark.parametrize("bound", ["rpc_line_bytes", "tool_result_bytes"])
def test_raw_js_frame_limits_still_reject_before_projection_can_shrink_result(bound):
    from cloudra.runtime_v2.js_protocol import ProgramLimits, ProtocolError

    raw = {"data": _view(), "summary": json.dumps(_view())}
    if bound == "tool_result_bytes":
        raw_size = len(json.dumps(raw["data"], ensure_ascii=False).encode())
    else:
        raw_size = len(json.dumps({"type": "tool_result", "request_id": "r1", "result": raw}, ensure_ascii=False).encode())
    with pytest.raises(ProtocolError, match=bound):
        encode_tool_result_frame("r1", raw, limits=ProgramLimits(**{bound: raw_size - 1}))


def test_raw_nonfinite_scientific_number_is_not_hidden_by_projection():
    from cloudra.runtime_v2.js_protocol import ProtocolError

    view = _view()
    view["result"]["verified"] = float("nan")
    with pytest.raises((ValueError, ProtocolError)):
        encode_tool_result_frame("r1", {"data": view})


@pytest.mark.parametrize("advisory", [
    "each IRC endpoint lies between the TS and the corresponding declared minimum (direct pairing; interval proof per irc_path.assign_irc_endpoints)",
    "each IRC endpoint lies between the TS and the corresponding declared minimum (swapped pairing; interval proof per irc_path.assign_irc_endpoints)",
    "Warning: endpoint optimization establishes the two path directions, but the geometric interval is unusual or could not be judged; inspect the trajectory. at least one IRC endpoint does not lie within the pair-distance interval between the TS and either declared minimum",
])
def test_owned_irc_advisory_does_not_reintroduce_connectivity_verdict(advisory):
    view = _view()
    view["message"] = (
        "verified transition state: exactly one imaginary mode (-321.5 cm^-1), both actual IRC outer frames from the same TS optimized independently to zero-imaginary-frequency minima with the declared reactant and product identities (origins={'A': 'reactant', 'B': 'product'}). Geometry interval advisory: " + advisory)
    public = _project(view)
    assert "-321.5 cm^-1" in public["message"]
    assert "Both optimized endpoints: zero imaginary frequencies." in public["message"]
    assert "lies between" not in public["message"]
    assert "establishes the two path directions" not in public["message"]
    assert "does not lie within" not in public["message"]


def test_stale_export_and_preparation_suffixes_survive_known_verdict_text():
    view = _view()
    suffix = "; JSON export is stale (revision 1); use this authoritative revision 2 and its current atom tables.\nPreparation performed:\n- Generated input /work/verified.xyz"
    view["message"] = "verified" + suffix
    public = _project(view)
    assert public["message"] == "?" + suffix


@pytest.mark.parametrize(("label", "complex_smiles", "detail"), [
    ("[CH3:1] + [OH:2]", "[CH3:1].[OH:2]", "frequency=-321.5; RMSD=0.112; /work/a:1.pass.out"),
    ("[C@@H:1](O)C + [Na+]", "[C@@H:1](O)C.[Na+]", "native path=/work/folder with spaces/x:y.verified.log; energy=-44.001"),
    ("[13CH3:1] + [Cl-:2]", "[13CH3:1].[Cl-:2]", "custom inner verdict: candidate_only; source=/work/detail. The bound complex fragment.txt"),
])
def test_separated_product_success_preserves_entire_label_details_and_complex(label, complex_smiles, detail):
    view = _view()
    message = (f"Verified TS connectivity to separated products {label}: {detail}. "
               f"The bound complex {complex_smiles} minimum remains UNVERIFIED.")
    view["message"] = message
    view["result"]["reason"] = message
    public = _project(view)
    for projected in (public["message"], public["result"]["reason"]):
        assert f"{label}: {detail}. The bound complex {complex_smiles}" in projected
        assert "Verified TS connectivity" not in projected
        assert "minimum remains UNVERIFIED" not in projected
        assert len(projected.encode()) <= len(message.encode())


def test_separated_product_negative_preserves_unknown_inner_detail_verbatim():
    detail = "custom identity mismatch: RMSD=0.321; energy=-3.001; source=/work/a:b.verified.out"
    view = _view()
    view["message"] = "Separated-product IRC proof is incomplete: " + detail
    public = _project(view)
    assert detail in public["message"]
    assert "proof is incomplete" not in public["message"]


@pytest.mark.parametrize("role", ["reactant", "product"])
@pytest.mark.parametrize("source", ["IRC side A", "IRC side B", "explicit species seed"])
def test_endpoint_failure_outer_template_preserves_source_reason_and_declared_smiles(role, source):
    detail = f"{role} frequency=-12.4; native file /work/seed 1:a.out; unknown inner unverified assessment"
    smiles = "[C@@H:1](O)C.[Na+]"
    message = (f"The {role} endpoint candidate from {source} did not qualify as an optimized minimum: {detail}. "
               f"Repair verification.{role}_endpoint.seed for the declared {role} {smiles}; "
               "IRC A/B labels do not declare species identity.")
    view = _view()
    view["message"] = message
    public = _project(view)
    assert source in public["message"]
    assert detail in public["message"]
    assert f"verification.{role}_endpoint.seed" in public["message"]
    assert smiles in public["message"]
    assert "did not qualify as an optimized minimum" not in public["message"]
    assert len(public["message"].encode()) <= len(message.encode())


@pytest.mark.parametrize("role", ["reactant", "product"])
def test_declared_minimum_outer_template_preserves_unknown_inner_reason(role):
    reason = f"{role} endpoint log /work/declared:a.out; frequency=-19.2; custom inner unverified judgment"
    suffix = (". For separated products, supply verification.product_endpoint.component_logs; the complex remains unverified."
              if role == "product" else "")
    view = _view()
    view["message"] = f"Declared {role} minimum is unverified: {reason}" + suffix
    public = _project(view)
    assert reason in public["message"]
    assert f"Declared {role} minimum is unverified" not in public["message"]
    assert "the complex remains unverified" not in public["message"]
    if role == "product":
        assert "verification.product_endpoint.component_logs" in public["message"]


def test_outer_frame_failure_preserves_all_inner_evidence_and_geometry_notes():
    detail = ("Declared species identity: missing bonds=[(1, 2)]; IRC endpoint lineage: unknown inner verified claim. "
              "reactant RMSD=0.102 from /work/r:1.out; product RMSD=0.231 from /work/p.verified.out")
    message = ("The optimized IRC outer frames did not establish one consistent species identity, "
               "source provenance, and actual outer-frame optimization lineage: " + detail
               + ". These observations do not override the failed checks. The candidate stays UNVERIFIED")
    view = _view()
    view["message"] = message
    public = _project(view)
    assert detail in public["message"]
    assert "did not establish" not in public["message"]
    assert "failed checks" not in public["message"]
    assert "candidate stays UNVERIFIED" not in public["message"]
    assert len(public["message"].encode()) <= len(message.encode())


def test_strict_pass_text_preserves_zero_imaginary_endpoint_observation():
    text = "pass: both actual IRC outer frames optimize to the expected zero-imaginary endpoint minima."
    view = _view()
    view["message"] = text
    public = _project(view)
    assert public["message"] == "Both optimized IRC outer frames: zero imaginary frequencies; ?"
    assert len(public["message"].encode()) <= len(text.encode())


@pytest.mark.parametrize("role", ["reactant", "product"])
def test_endpoint_optimization_outer_shell_keeps_error_and_repair_advice(role):
    error = "native result: frequency=-21.4, RMSD=0.123, source=/work/seed 1:a.verified.out"
    suffix = ". Revise this run with an explicit endpoint seed through ts_resume"
    text = f"{role} endpoint optimization cannot support a minimum: {error}" + suffix
    view = _view()
    view["message"] = text
    public = _project(view)
    assert public["message"] == f"{role} endpoint optimization observations: {error}" + suffix
    assert len(public["message"].encode()) <= len(text.encode())
