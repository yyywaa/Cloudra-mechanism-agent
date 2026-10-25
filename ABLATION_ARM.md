# Ablation arm: dag_record

The DAG is a tool the agent may use, not a settlement gate.
Synchronized with master `8c568ca6753ecf2cd40a90a8f0f8b5c8e19dd1d2`.

- Every benchmark task runs under `OrchestrationMode.DAG_RECORD`
  (`ABLATION_ARM` in `cloudra/benchmark/runner.py`).
- Tools, mechanism graph and agent-invoked chemistry verification stay.
- No supervisor review (already absent in this mode).
- The scientific stop gate is advisory: `complete` and `partial` do not require
  scientific coverage or endpoint-evidence publication. The common basic
  delivery check still requires a parseable mechanism_graph.json.
- The recorded basis is `declared` for complete (verification label `unverified`)
  and `partial_recorded` for partial (label `partial`), never `dag_verified`.
  The scientific report still records missing evidence honestly.
- Background work still suspends settlement. Authentic user-stop checks and
  concurrent DAG-state protection remain; these are operational safeguards,
  not scientific completion requirements.

## Launch and isolation

Run from this branch's checkout with its own runtime process and data directory:

```sh
python -m cloudra.benchmark --backend runtime_v2 --tasks-dir ideapool/tasks/easy --only D3 --data-dir benchmark_data/arm-record --concurrency 1
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
without changing their orchestration mode.
Role, method policy, YOLO/unattended/clean-context defaults and scoring stay intact.

## Focused local checks

`tests/test_benchmark_arm_wiring.py` covers all three conflicting task modes,
coordinator and small_mol root roles, real CLI/Web spawn-setting resolution,
child inheritance, provenance, scored/error/cancelled result metadata, and the
complete-only guided IRC gate. Model scheduling is stubbed, the Web core has no
LLM runner, and socket connections are prohibited.

`tests/test_benchmark_record_advisory.py` checks incomplete scientific coverage,
malformed delivery artifacts, honest completion labels and retained operational
safeguards, using only temporary local databases.

## Common basic delivery check

All four arms require a parseable `mechanism_graph.json` at the workspace
root before final delivery. Missing files and format errors are returned
to the research agent for repair. The shared check does not evaluate
scientific evidence, write the graph, or change each arm's scientific
acceptance rules. Background waits, child/peer tasks and actual user
cancellation retain their existing behavior. Runs made before this fix
must remain separate from runs made with the updated commits.
