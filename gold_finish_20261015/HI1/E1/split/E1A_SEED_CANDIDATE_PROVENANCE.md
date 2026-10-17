# E1a guided-seed candidate — provenance (lane1)

Status: **guess candidate only, NOT a saddle, NOT submitted**. E1a remains unverified; its
DeltaE-double-dagger is **null**.

## 1. Tool and parameters (conformer_search, backend rdkit)
| run | output_dir | distance_filters (1-based working order) | num_confs | seed | energy_window |
|---|---|---|---|---|---|
| A ("v1") | `split/E1a_seed_search/` | (2,18) 2.2-2.5; (18,27) 1.0-1.1; (2,3) 1.32-1.45 | 50 | 42 | 6.0 kcal/mol |
| B ("v2") | `split/E1a_seed_search_v2/` | (2,18) 2.2-2.6; (18,27) 1.0-1.1; (2,3) 1.19-1.45 | 80 | 7 | 10.0 kcal/mol |
| C ("v3") | `split/E1a_seed_search_v3/` | same as B | 80 | 7 | 10.0 kcal/mol |
| D ("v4") | `split/E1a_seed_search_v4/` | (2,18) 2.6-3.0; (18,27) 1.0-1.1; (2,3) 1.19-1.45 | 80 | 7 | 10.0 kcal/mol |
input for every run: `RC_27_opt_frame.xyz` sha256 `c1f789e0b6653c7de55a291c98f28dd3088f1e6cb3c0124617abecda398f691a`,
charge 0, multiplicity 1, backend rdkit (MMFF/UFF level).

## 2. Outcome: no qualified candidate, only a closest attempt
All four runs returned `is_success=false` with counts generated 8 / optimized 8 / **rejected 8** /
retained 0 / **qualified 0**; no ensemble file was written. Tool text (run D):
`No guided assembly candidate qualified; closest attempted geometry: .../E1a_seed_search_v4/closest_attempt.xyz`,
with the diagnostic `reaction mode: placements are guided by the reaction center pairs ...;
intra-fragment geometry stays rigid during placement`.
That last point is the capability boundary: the guided assembly only does **rigid-body placement between
fragments**, so R(C2-N18) bottoms out at **2.69-2.75 A** and cannot enter a 2.2-2.5 A window.

## 3. Candidate frames (files, shas, measured numbers)
| run | closest_attempt.xyz | sha256 | guidance_manifest.json | sha256 |
|---|---|---|---|---|
| A | `split/E1a_seed_search/closest_attempt.xyz` | `845a4bd9908e1607e7ead78d17896912bf2bc874d0310f50bb399fb90e813435` | `split/E1a_seed_search/guidance_manifest.json` | `c9098d91d1b34f5bb22bdd1ea91637a4d51017a9a9f5a2f0210871a624ad70e4` |
| B | `split/E1a_seed_search_v2/closest_attempt.xyz` | `9a5c9c3294834a8d344c66d77d5cc14122bf881c01b7606ae35d1b2267c067e9` | `split/E1a_seed_search_v2/guidance_manifest.json` | `8a4e3ceae53d75a0d8d3faf55b9b1ea51967a21318b12fd573358d040a1aa508` |
| C | `split/E1a_seed_search_v3/closest_attempt.xyz` | `9a5c9c3294834a8d344c66d77d5cc14122bf881c01b7606ae35d1b2267c067e9` | `split/E1a_seed_search_v3/guidance_manifest.json` | `06e18dd537ca4b13efde023c873cce64348885745d9b0d9d860bd4a41d193150` |
| D | `split/E1a_seed_search_v4/closest_attempt.xyz` | `aa6fc0a05b7ac2cca807b55f1fd7d41505e9891ae670f38a680b343bedfda71e` | `split/E1a_seed_search_v4/guidance_manifest.json` | `892f988ecb534972719aae1895fd0654e31243510888a163a0d233564286f803` |

All four frames: 27 atoms, **element sequence identical to the refine.log converged frame
(`E1A_TS_candidate_job1055.xyz`, sha256 `2b4cf70f539a62f941422b7e652d90d1620c4e4a10beefd3162ba0ea2cbd8f50`)
position by position (27/27)**.

| measured quantity | run A | run B (= C) | run D |
|---|---|---|---|
| R(C2-N18) working index 2-18 | **2.6920** | **2.7508** | 3.0481 |
| R(N18-H21) 18-27 (proton on N) | 1.0349 | 1.0303 | 1.0255 |
| R(C2-O3) 2-3 (carbonyl kept) | 1.2383 | 1.2327 | 1.2321 |
| R(O3...H21) 3-27 | 2.2993 | 2.3036 | 3.4945 |
| global minsep | **0.9794** | **0.9807** | 0.9801 |
| three tightest contacts | 13(O)-19(H) 0.9794 (carboxyl O-H); 18(N)-27(H) 1.0349 (N-H); 1(C)-7(H) 1.0926 (methyl C-H) | 13(O)-19(H) 0.9807; 18(N)-27(H) 1.0303; 1(C)-6(H) 1.0926 | 13(O)-19(H) 0.9801; 18(N)-27(H) 1.0255; 4(C)-10(H) 1.0926 |

**The minimum separations are all ordinary chemical bonds** - no H...N or H...O reaction-pair contact
is what satisfies the 0.9 A floor.

## 4. Corrected reading of the C2-O3 gate (erratum)
The earlier gate statement "C2-O3 >= 1.30 (no premature protonation)" was written with the wrong
direction by the coordinator and has been corrected: an early-attack frame must keep the **carbonyl
double bond**, i.e. C2-O3 ~ 1.22-1.28 A; a value > 1.32 A would mean the carbonyl had already become a
single bond. Under the corrected reading, runs A/B/C **pass** the gate (1.2383 / 1.2327) and run D passes too
(1.2321); nothing here is "infeasible by construction".

## 5. Standing of these frames (must travel with any use)
- **Force-field level (MMFF/UFF via RDKit), not the QM surface.** Coordinates are a geometric guess only.
- **Fragment-rigid placement.** The acetone fragment keeps its RC internal geometry and the proline ring
  is not relaxed, which is exactly why R(C2-N18) cannot go below ~2.69 A here.
- **Guess only, not a saddle**: no Hessian, no imaginary mode, no connectivity check has been done on these
  frames. Any TS claim still needs a converged ts_opt with exactly one imaginary mode on the declared pairs
  plus the frequency/connectivity verification chain.
- **Not submitted**; no QM job was launched from this path; `ts/ts_0015/process.json` untouched.

## 6. Model conditions
CPCM(DMSO) continuum only (for any later QM use), no explicit solvent, no counterion, no added base;
benzaldehyde excluded from the 27-atom model and from every denominator; pure electronic energies only
from one Gaussian batch.

## 7. Erratum - manifest sha mis-mapping for run A (correction, NOT a silent edit; 2026-10-17 CST)
The first version of section 3 printed run A's `guidance_manifest.json` sha256 as
`8a4e3cea...`, which in fact belongs to run **B** (`split/E1a_seed_search_v2/guidance_manifest.json`).
Re-verified on disk with `sha256sum` at 15:2xCST 2026-10-17:
`split/E1a_seed_search/guidance_manifest.json` =
`c9098d91d1b34f5bb22bdd1ea91637a4d51017a9a9f5a2f0210871a624ad70e4`.
The A row of section 3 is corrected in place; the B/C/D mapping (8a4e3cea / 06e18dd5 / 892f988e) was already
correct. No coordinate, distance, energy, standing statement or verdict in this document changes.
