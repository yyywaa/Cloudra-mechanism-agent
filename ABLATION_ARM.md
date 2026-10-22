# Ablation arm: dag_record

The DAG is a tool the agent may use, not a gate.

- Every benchmark task runs under `OrchestrationMode.DAG_RECORD`
  (`ABLATION_ARM` in `cloudra/benchmark/runner.py`).
- Tools, mechanism graph and agent-invoked chemistry verification stay.
- No supervisor review (already absent in this mode).
- The stop gate is advisory: `complete` and `partial` both end the run, no
  delivery artifact or endpoint-evidence publication is required.
