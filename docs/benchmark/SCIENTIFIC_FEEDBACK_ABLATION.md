# C: neutral automatic scientific feedback

This treatment is confined to `benchmark/arm-standard`. Product master and A/B/D
are not changed. It implements the user's “自动判定模糊化”: keep calculations and
observations, withhold explicit automatic scientific conclusions from the normal
experimental agent feedback. It is not a new scientific evaluator or permission
system.

## Public meaning

- `result.verified=null` and a neutral `result.outcome` mean **assessment not
  provided**, not false, failed, accepted or complete. The short text `?` has the
  same meaning where the existing field is textual.
- Real execution outcomes (`search_failed`, `invalid_input`, job failures,
  cancellation, waiting and blocked workflow state) stay visible. Scientific
  diagnostic categories such as `wrong_mode` are withheld only in the display;
  the workflow remains blocked and required inputs/actions are not changed.
- Frequency values and counts, displacement measurements, energies, coordinates,
  IRC point counts, engine convergence facts, geometry, input declarations,
  source paths/hashes and native logs remain unchanged. A numerical observation
  can still let the agent form its own scientific judgment; that is intended.
- Independent `ts_guess` verify/strict is still rejected. Other calculations,
  stage progression, stopping/partial semantics and offline scoring are unchanged.

## One projection, multiple existing exits

`cloudra/runtime_v2/scientific_feedback.py` owns the presentation rules. It
recognizes TS result/record schemas and repository-owned text templates, rather
than globally rewriting every `status`, `passed` or occurrence of “verified”.

| Exit | Treatment | What remains authoritative |
| --- | --- | --- |
| Traditional tool context | Copy the known TS fields and matching JSON summary | Raw ToolResult and recorded tool event |
| JS guest ToolResponse | Project before guest code receives data/summary; validate the original frame limits first | Original invocation outcome and envelope controls |
| Compute/guidance notices | Project only their rendering, including restored notices | Original notice events and scheduling decisions |
| TS prepare/resume/inspect and nested ts_guess process | Share the same public view projection | Internal TsProcessView and DB record |
| Durable process.json exports (save/revision/stop) | Write a presentation copy with stable pipeline/revision IDs | Original database record |
| Durable load_record/restart | Resolve the ID to the original DB record; load_record checks run/workspace | Original typed scientific record |
| Public tool documentation | Describe neutral output fields without weakening internal Pydantic validation | Internal schema and scientific computation |

Both parent and child agents execute the same branch code. We do not rewrite a
child's independently generated scientific conclusions or model compaction.
Native `read`/`bash` contents are not scanned or rewritten.

## Deliberate boundaries and residual feedback

1. **Mixed prose:** only exact owned outer templates are stripped. Fixed TS
   frequency and IRC/endpoint templates retain numerical observations, species
   labels, origins and paths. Unknown inner explanations, scan verdicts containing
   energies/geometry and mode-alignment details are preserved rather than guessed
   or deleted. They may still carry scientific judgment.
2. **File-only records:** a legacy record without a pipeline ID remains its own
   authority and is not rewritten. Its original verdict can still be read. New
   experiment runs should use the normal durable pipeline and clean workspaces.
3. **Internal safety review:** YOLO approval continues to receive real risk facts.
   This treatment does not weaken permission checks or suppress genuine errors.
   Approval feedback may be a residual scientific-information channel.
4. **No new file isolation:** raw DB/events remain for offline audit. Existing
   shell/data access is unchanged; this is not a guarantee that the agent can
   never read them. Do not reuse old contexts that already contain full verdicts.
5. **Not all chemistry interpretation is removed:** internal TS decisions,
   geometry heuristics, native log titles and unknown mixed output remain.
   Record actual residual feedback before making an experimental claim.
6. **DAG confound remains:** C hides DAG tools while B retains them. The B/C
   comparison is a package comparison, not an isolated verification-tool effect.
   Restoring C's DAG was not authorized by this change.

## Reproduction and evaluation

Use the branch's existing CLI/Web launch procedure in `ABLATION_ARM.md`, with a
new data directory, the same models/tasks/budgets and independent clean sessions.
The batch provenance adds `scientific_feedback="neutralized_public_verdicts"`.
Freeze the commit alongside that marker; earlier C results are not interchangeable.

Offline adjudication uses retained native evidence and truthful internal records,
not the public null flags. Existing native-log fallback remains available;
`undelivered` is an artifact/protocol metric, not automatically scientific zero.
Do not treat a weighted score as a success rate. No paid experiment or external
QM job was started to implement this treatment.

Focused tests cover original-object/ledger preservation, positive and negative
verdicts, fixed mixed templates, execution failures, JSON/JS boundaries, protocol
limits, restored notices, three durable export paths and scoped reloads. Existing
TS parser/pipeline fixtures and invocation/notice tests are also checked. These
checks are not full-repository acceptance; the previously blocked full test run
has not been retried or claimed green.
