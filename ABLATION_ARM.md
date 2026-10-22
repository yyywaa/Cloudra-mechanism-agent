# Ablation arm: dag_guided (full)

The current product behaviour, frozen for the ablation.

- Every benchmark task runs under `OrchestrationMode.DAG_GUIDED`
  (`ABLATION_ARM` in `cloudra/benchmark/runner.py`).
- Supervisor adversarial review, required IRC direction proof, delivery
  artifact and endpoint-evidence publication all apply.
