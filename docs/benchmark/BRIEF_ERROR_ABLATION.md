# D arm: guided with briefer diagnostic feedback

This arm retains the full guided implementation, Supervisor decisions, scientific
tools, thresholds, permissions, stop gates, retry counts and partial results. Its
only intervention is the public text projection in
`cloudra/runtime_v2/brief_errors.py`. It is **not complete error-information
removal or filesystem isolation**.

## Manifest and provenance

Benchmark provenance maps each task to `dag_guided` in `orchestration_modes`;
result rows retain `orchestration_mode: dag_guided`. Record the branch identity as `experiment_arm: benchmark/arm-guided-brief-errors` and
`error_feedback: brief`; the runner emits these fixed provenance fields. The base
snapshot is master `8c568ca6753ecf2cd40a90a8f0f8b5c8e19dd1d2`, plus the same
runner/backend/batch arm-wiring correction as A. This identity is not a runtime
setting that can silently change the experiment.

## Scope of projection

- Traditional tool context and JavaScript guest result/error frames share the
  projection. JS validates the original payload/frame limits before shortening.
- Successful queries are traversed for nested failed jobs, rejected reviews,
  failed/incomplete scientific checks, delivery gaps and child diagnostics.
- DAG prompt copies, fresh/incremental/replayed pins, model-bound mailbox
  notifications, completion-gate feedback and child reports use the same module.
- Explicit error descriptions and localization/repair fields are shortened:
  `error`, `last_error`, `error_message`, `planned_error`, `reject_reason`, and
  failed-context `message/msg/reason/detail/summary/next_action`, blocked
  `issues.field/loc`, `needs`, `atom_details`, `next.required_inputs`, and failed
  child `final_summary/unresolved/next_steps`.
- Preserve status/code/category/failure_class, target/job/request IDs, action,
  effect state, counts, decisions, evidence paths, measurements, native outputs,
  normal data, declarations and partial subresults. The exit-review handshake
  manifest is preserved exactly. `verified=false` alone is not an error.
- General SOP, scientific standards, resource constraints, tool descriptions,
  normal workflow guidance and cancellation instructions remain intact. Only
  diagnostic-triggered reflection/review/completion advice is shortened.

## Audit retention and explicit residual channels

Authoritative tool/program events, reviews, gate reasons/fingerprints, pin and
mailbox events, and TS database records retain full diagnostics. `process.json`
exports redact only explicit diagnostic fields, and only for records backed by
a pipeline database; standalone file-only records stay complete. No raw record
is overwritten to create an ablation. Public model-context events naturally
contain the shortened text.

This does not remove access to audit databases/events through existing shell or
read tools, native calculation logs/output, long-output offload files, or
standalone process records. No new filesystem permission/sandbox system is
introduced. Legacy TS `checks`/`verdicts` entries mixing numerical or geometric
observations with guidance are retained to avoid deleting scientific evidence;
only the known standalone IRC repair instruction is mapped to brief text.
Normal scan/candidate summaries mixing facts with suggestions are also retained.
Rare noncanonical JSON summaries are retained if re-encoding their normal numbers
would enlarge the original bridge frame; structured diagnostic data is still
projected. Short diagnostic strings use a one-character marker, never expansion.
Previously stored full model-context histories are not scrubbed; benchmark runs
must start fresh. Thus D tests **briefer structured feedback**, not an absolutely
blinded agent.

## Offline verification

`tests/test_brief_error_projection.py` exercises purity, idempotence, unchanged
controls and measurements, unverified/partial success, native output, nested
successful-query errors, traditional/JS frames and original size limits,
notice replay/inbox/stop/child/DAG paths, and durable full SQLite tool/program/TS
records. It uses no provider or compute backend. Run with all telemetry disabled
and an isolated `CLOUDRA_DATA_DIR`. The bundled tokenizer vocabulary must be
available locally; focused checks do not imply a full-suite pass or authorize a
real provider/compute run.
