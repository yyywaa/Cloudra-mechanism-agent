import json
from pathlib import Path


def test_catalog_retains_all_official_cases_and_missing_input_requirement():
    from cloudra.benchmark.aitomia import load_catalog

    catalog = load_catalog()
    assert len(catalog.cases) == 47
    assert len({case.task_id for case in catalog.cases}) == 47
    assert sum(case.provided_xyz for case in catalog.cases) == 23
    case = next(case for case in catalog.cases if case.task_id == "OPT.AIQM1_GEOMETRIC")
    assert case.provided_xyz is True
    assert "[xyzfile]" not in case.query


def test_prepare_substitutes_paths_without_leaking_published_outcomes(tmp_path):
    from cloudra.benchmark.aitomia import Case, prepare_case

    xyz = tmp_path / "source.xyz"
    xyz.write_text("1\nH\nH 0 0 0\n")
    case = Case(
        task_id="TEST", source_task_id="TEST", level="Low", query="Run [xyzfile] in [working_dir] using AIQM2.",
        provided_xyz=True, source_row=3, reported_success_rate=0.7, reported_runs=10,
    )
    workspace = tmp_path / "case"
    record = prepare_case(case, workspace, xyz)
    request = json.loads((workspace / "request.json").read_text())
    assert record["execution_status"] == "prepared"
    assert request == {"task_id": "TEST", "query": f"Run {workspace}/input.xyz in {workspace} using AIQM2."}
    assert (workspace / "input.xyz").read_bytes() == xyz.read_bytes()
    assert record["score"] is None
    assert record["scientific_status"] == "unreviewed"


def test_prepare_blocks_required_xyz_even_if_query_omits_placeholder(tmp_path):
    from cloudra.benchmark.aitomia import Case, prepare_case

    case = Case(task_id="X", source_task_id="X", level="Low", query="Optimize using AIQM1.",
                provided_xyz=True, source_row=9)
    record = prepare_case(case, tmp_path)
    assert record["execution_status"] == "blocked_input"
    assert not (tmp_path / "request.json").exists()


def test_input_binding_is_visible_for_official_query_without_placeholder(tmp_path):
    from cloudra.benchmark.aitomia import Case, prepare_case

    xyz = tmp_path / "provided.xyz"
    xyz.write_text("1\nH\nH 0 0 0\n")
    case = Case(task_id="X", source_task_id="X", level="Low", query="Optimize using AIQM1.",
                provided_xyz=True, source_row=9)
    workspace = tmp_path / "run"
    prepare_case(case, workspace, xyz)
    query = json.loads((workspace / "request.json").read_text())["query"]
    assert query.startswith(case.query)
    assert str(workspace / "input.xyz") in query


def test_execute_preserves_native_result_without_turning_it_into_scientific_pass(tmp_path):
    from cloudra.benchmark.aitomia import Case, execute_case, prepare_case

    case = Case(task_id="X", source_task_id="X", level="Medium", query="Compute B3LYP/6-31G* energy.",
                provided_xyz=False, source_row=30)
    record = prepare_case(case, tmp_path)

    class Backend:
        def run_prompt(self, *, task_id, query, sandbox):
            assert task_id == "X"
            assert query == case.query
            Path(sandbox, "native.out").write_text("raw calculation output")
            return {"project_id": "p", "session_id": "s", "state": "succeeded", "final_message": "Done."}

    result = execute_case(record, Backend())
    assert result["execution_status"] == "finished"
    assert result["scientific_status"] == "unreviewed"
    assert result["score"] is None
    assert (tmp_path / "answer.md").read_text() == "Done."
    assert (tmp_path / "native.out").read_text() == "raw calculation output"


def test_execute_does_not_dispatch_missing_input(tmp_path):
    from cloudra.benchmark.aitomia import Case, execute_case, prepare_case

    case = Case(task_id="X", source_task_id="X", level="Low", query="Use [xyzfile].",
                provided_xyz=True, source_row=3)
    record = prepare_case(case, tmp_path)
    result = execute_case(record, None)
    assert result["execution_status"] == "blocked_input"


def test_cli_rejects_unknown_case_without_creating_runtime(tmp_path):
    from cloudra.benchmark.aitomia.__main__ import main

    assert main(["--only", "DOES_NOT_EXIST", "--data-dir", str(tmp_path)]) == 2
    assert not list(tmp_path.iterdir())


def test_cli_prepares_complete_bank_without_runtime_or_scientific_scores(tmp_path):
    from cloudra.benchmark.aitomia.__main__ import main

    assert main(["--data-dir", str(tmp_path)]) == 0
    run_dir, = tmp_path.iterdir()
    manifest = json.loads((run_dir / "run.json").read_text())
    assert manifest["mode"] == "prepare"
    assert len(manifest["results"]) == 47
    assert sum(row["execution_status"] == "prepared" for row in manifest["results"]) == 24
    assert sum(row["execution_status"] == "blocked_input" for row in manifest["results"]) == 23
    assert all(row["score"] is None for row in manifest["results"])
    assert not (run_dir / "runtime").exists()


def test_runtime_failure_is_retained_as_error_with_no_scientific_score(tmp_path):
    from cloudra.benchmark.aitomia import Case, execute_case, prepare_case

    case = Case(task_id="X", source_task_id="X", level="Medium", query="Calculate the energy.",
                provided_xyz=False, source_row=30)
    record = prepare_case(case, tmp_path)

    class Backend:
        def run_prompt(self, **kwargs):
            raise RuntimeError("provider unavailable")

    result = execute_case(record, Backend())
    saved = json.loads((tmp_path / "result.json").read_text())
    assert saved == result
    assert saved["execution_status"] == "error"
    assert saved["score"] is None
    assert "provider unavailable" in saved["reason"]
