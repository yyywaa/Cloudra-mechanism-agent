# Ablation arm: standard

Tools stay available, chemistry verdicts do not.

- `ts_guess` mode `verify` (and `strict`) is rejected: the harness never tells
  the model whether a saddle/IRC is chemically valid.
- DAG tools are hidden (standard mode's catalog filter); the agent records the
  mechanism in `mechanism_graph.json` itself.
- Every benchmark task in this checkout runs under `OrchestrationMode.STANDARD`
  (`ABLATION_ARM` in `cloudra/benchmark/runner.py`).
