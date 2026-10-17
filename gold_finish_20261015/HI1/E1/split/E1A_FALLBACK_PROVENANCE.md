# E1a fallback (a) — preparation record (lane1)

Status: **PREPARED ONLY, NOT SUBMITTED** (documented next action). E1a remains **unverified**; its
DeltaE-double-dagger is **null**.

## 1. Sources (all on disk, tool-derived)
| artifact | sha256 |
|---|---|
| `RC_27_opt_frame.xyz` (RC_27 minimum, job 1044 final frame) | `c1f789e0b6653c7de55a291c98f28dd3088f1e6cb3c0124617abecda398f691a` |
| `INT1_27_opt_frame.xyz` (carbinolamine_27 minimum, job 1051 final frame) | `b2f2ffaaf64169916e29d59fa44a49e223e394e21f69907980b8a83151fa5d36` |
| `ts/ts_0015/jobs/declaration_0001/ts_opt/refine.log` (diagnostic geometry source) | `0023847fe5b2e2961f9914d7a4f7a694ae11a9d826bd892b190866274f0a430b` |
| `E1A_TS_diag_freq.log` (job 1062, frequency characterisation) | `e6c128476d1eb716b234b5ed77bc1d9b13c07d4d3846648ae3026f29fdcfdf3d` |

## 2. Why a fallback frame was attempted
The ts_opt candidate (job 1055) and its diagnostic frequency (job 1062) give **one** imaginary mode at
**-1551.2317 cm-1** whose displacement is **79.7 % on H21**, 5.3 % on C2 and 0.8 % on N20 (below the
0.0100-0.0141 printing-noise floor of the eigenvector table). That is a proton-transfer-dominated saddle,
not a concerted C-N/PT saddle, so the agreed fallback is an earlier attack frame with
R(C2-N18) ~ 2.10 A and H21 still on N18.

## 3. Construction attempts and their measured failures (all rigid-fragment, no QM)
Let A = RC_27 frame and B = carbinolamine_27 frame. Working-order indices: C2 = 2, O3 (carbonyl O) = 3,
C3 = 4, H22 = 10, N18 = 20 (map label 20, working 18), H21 = 27.

| attempt | construction | measured outcome | verdict |
|---|---|---|---|
| v1/v2 | Cartesian interpolation of every atom after a Kabsch fit on heavy atoms | R(C2-O3) collapses to 0.97 A, R(C3-H22) 0.52 A, minsep 0.45-0.52 A | rejected: bond collapse |
| v3 | rigid-body interpolation of the acetone fragment (centroid + rotation slerp) | minsep 0.33-0.49 A (methyls sweep through the proline ring) | rejected: clashes |
| v4 | pure slide of the acetone fragment along C2->N18 to 2.10 A | monotonic R, but R(O3...H21) = 0.61 A and R(O3...N18) = 1.53 A | rejected: O/H and O/N overlap |
| v5-v9 | rotate acetone about C2 to O3-C2...N18 = 100-130 deg (Buergi-Dunitz), then slide | best minsep 0.48-0.71 A; methyl H's collide with proline (pairs 6-14, 1-18, 8-20) | rejected: clashes |
| v10 | add an azimuth spin of the fragment about the C2->N18 axis (0-350 deg, 10 deg grid) | best minsep **0.854 A** at R(C2-N18) = 2.10 A | below the 0.9 A floor |
| v11 | same rigid model, slide bisected so that minsep = 0.90 A | **R(C2-N18) = 2.2916 A**, minsep **0.9000 A** between atoms 7 (acetone methyl H) and 18 (N) | meets the number, but only via a 0.90 A H...N contact |

## 4. Delivered artifact and its honest interpretation
- File: `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split/E1A_fallback_earlyattack_minsep090.xyz`
  sha256 `f589a84857249e6156c09d67b2f646d300f7dc04b88ee2a01f954083a3bfb7bd` (27 atoms).
- Parameters: proline fragment and H21 unchanged from RC_27 (H21-N18 = 1.0228 A, re-oriented away from
  the carbonyl to clear the incoming C=O); acetone rigid-rotated about C2 to O3-C2...N18 = 105 deg,
  spun 150 deg about the C2->N18 axis, slide bisected for minsep = 0.90 A => R(C2-N18) = 2.2916 A.
- Key distances in the delivered frame: C2-O3 1.2195 (unchanged), N18-H21 1.0228, O3...H21 3.8705,
  C2...H21 3.2948, O3...N18 2.8610; angles O3-C2...N18 105.0 deg, H-N-Calpha 98.3, H-N-C17 71.6.
- Slide table of the same rigid model (R vs global minsep): 3.7571/0.9737, 3.4257/0.9737, 3.0943/0.9737,
  2.7628/0.9737, 2.4314/0.9567, 2.2916/**0.9000**, 2.2657/0.8915, 2.1000/**0.8540**.

**Interpretation (must travel with this file)**: the 0.90 A floor is met only because an acetone methyl
hydrogen sits 0.90 A from N18 - a severe non-bonded contact, not a physical approach geometry. A rigid
fragment model therefore cannot produce a chemically acceptable early-attack frame at
R(C2-N18) <= 2.3 A: the proline ring must relax. Consequently this xyz is **not** recommended as a TS
guess as-is; a physically meaningful frame needs a constrained re-optimisation at fixed R(C2-N18)
(a compute job, not authorised and not submitted).

## 5. Rejected intermediate artifact
The first rigid-body artifact `E1A_fallback_earlyattack_R210.xyz` (minsep 0.49 A) was renamed to
`E1A_fallback_earlyattack_R210_REJECTED.xyz`; it must not be used for anything.

## 6. Model conditions
CPCM(DMSO) continuum only, no explicit solvent, no counterion, no added base; benzaldehyde is excluded
from the 27-atom model and enters no denominator; pure electronic energies from one Gaussian batch only.
