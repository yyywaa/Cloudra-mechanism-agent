# Molecular workbench editing implementation plan

**Approved scope:** The user approved automatic hybridization/lone-pair-aware placement, manual hybridization, MMFF94 preoptimization with explicit UFF selection and no fallback, and requested canvas deselection, faster picking and a coordinate editor popup with actual starting values.

**Architecture:** Keep chemistry in the shared Python workbench edit path. Keep the main WebGL model stable during selection; update selection overlays independently. Use one native dialog for coordinate adjustment/freezing/scanning with state initialized from the selected geometry.

**Constraints:** Preserve scientific provenance and explicit graph/atom identities; never silently change force fields. Workbench endpoints already run chemistry in a worker. Preserve existing unrelated changes. Run only affected checks locally; submit a PR without merging.

- [x] Reproduce and test geometry placement; implement one authority for add/fill, manual override and current-conformer force-field optimization.
- [x] Test and fix canvas background clicks versus picking/dragging; retain the main render model and camera during selection.
- [x] Test and implement the coordinate popup, actual starting values, keyboard close/focus, preview/cancel and saved definitions.
- [x] Add hybridization/readout and force-field controls; show energy/convergence in preview and preserve undo.
- [ ] Run scoped Python compile/lint/tests, frontend typecheck/build and workbench browser regressions; inspect final UI.
- [ ] Review integrated changes and deliver a work-branch PR.

Review focus: undefined dihedrals, incomplete graphs/unsupported atom states, stale selection or preview data, click versus drag/touch, failed preoptimization without draft mutation, frozen-coordinate constraints and undo.

Verification note: backend regression runs, frontend typecheck and build pass. Browser tests are authored but cannot run locally: Vite bind is denied and Chromium launch fails. Independent review findings on nonunit placement, uncertain graph provenance and camera preservation have been fixed. Browser verification must run in CI.
