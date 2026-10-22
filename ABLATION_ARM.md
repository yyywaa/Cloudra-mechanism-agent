# Ablation arm: standard

The existing standard arm, synchronized with master
`8c568ca6753ecf2cd40a90a8f0f8b5c8e19dd1d2`. Its feedback treatment is **automatic scientific judgment obfuscation**, not
removal of chemistry calculations or alteration of the offline scientific standard.

- `ts_guess` mode `verify` (including `strict`) is rejected. The independent
  saddle/IRC verifier does not run.
- Geometry/path/scan helpers and native calculation capabilities remain.
- DAG tools are hidden (standard mode's catalog filter); the agent records the
  mechanism in `mechanism_graph.json` itself. This differs from the record arm,
  which retains the DAG.
- Every benchmark task in this checkout runs under `OrchestrationMode.STANDARD`
  (`ABLATION_ARM` in `cloudra/benchmark/runner.py`).
- TS prepare/resume/inspect calculations and internal verdicts remain unchanged.
  Public scientific acceptance fields are neutral (`null`, not pass or fail),
  with measurements, evidence and execution state preserved. See
  [the exact feedback boundaries](docs/benchmark/SCIENTIFIC_FEEDBACK_ABLATION.md).
- Known remaining differences: C still hides DAG while record retains it; the
  input schema still lists verify although execution rejects it, and the common
  task prompt mentions DAG binding. Unknown mixed scientific prose and legacy
  file-only records remain intact to avoid losing evidence. This is not a pure
  "record minus verification tools" arm, nor complete blinding.

## Launch and isolation

Run from this branch's checkout with its own runtime process and data directory:

```sh
python -m cloudra.benchmark --backend runtime_v2 --tasks-dir ideapool/tasks/easy --only D3 --data-dir benchmark_data/arm-standard --concurrency 1
```

This is an actual model/compute run and can incur costs; this synchronization did
not run it. Without `--backend runtime_v2`, the CLI defaults to a no-model dry run,
not an experimental measurement. Use the same task IDs, model configuration,
method policy and budget across arms, and do not reuse another arm's data folder.
Tasks have no overall duration limit; `--concurrency 1` is not a spending cap.

The Web benchmark service uses the same branch-pinned arm. Restart it from this
checkout and use an isolated `CLOUDRA_DATA_DIR` / config `data_dir` before launching
its batch; `--data-dir` is a CLI flag, not a Web setting. Task JSON's requested
mode is intentionally overridden: project, root spawn, inherited child mode,
batch provenance and every result path all use `runner.ABLATION_ARM`.
Batch provenance also records the baked `experiment_arm` branch name and
`error_feedback="full"`, so full and brief-feedback arms remain distinguishable
without changing their orchestration mode. C additionally records
`scientific_feedback="neutralized_public_verdicts"` to distinguish its revised
feedback contract from earlier C runs.
Role, method policy, YOLO/unattended/clean-context defaults and scoring stay intact.

## Focused local checks

`tests/test_benchmark_arm_wiring.py` covers all three conflicting task modes,
coordinator and small_mol root roles, real CLI/Web spawn-setting resolution,
child inheritance, provenance, scored/error/cancelled result metadata, and the
complete-only guided IRC gate. Model scheduling is stubbed, the Web core has no
LLM runner, and socket connections are prohibited.

`tests/test_benchmark_standard_tools.py` checks that independent verify is rejected
without reading logs while interpolation, xTB-path and scan-parser dispatch remain
available. Helpers are stubbed; no chemistry calculation is launched.


`tests/test_scientific_feedback_projection.py` and
`tests/test_c_feedback_boundaries.py` cover the new public projection, native
facts, execution failures, protocol limits, raw ledger/export separation,
workspace-scoped durable reads and unchanged standalone reads. They do not
constitute a paid benchmark run or full-repository acceptance.
