# E2 1D relaxed scan — per-point table (3 of 15 points converged; job still running)

Measured at **2026-10-17 21:26:22–21:26:24 CST** (`date -Is`), full read-only re-extraction:

- log: `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan.log`
- log sha256: `3cabe93222fc0bfb2264296cae5e514682e841351eba81c24cbc17d321e915ea`
- log size at snapshot: **36294 lines / 2343621 bytes** (still growing — this is NOT a terminal reading)
- input gjf: `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan.gjf`, sha256 `6301b836b6ca0006f365d80e28cff2f552bd06edae8f54475d6985e751ffbb16`, 52 lines / 2415 B
- extractor (read-only, prints only): `evidence/extract_scan_table.py`, sha256 `f2e9e1c9754722b99e6f4891a161adb2d5843b602cfe38dd90b37831c77342b6`
- job: **1075** (gaussian, started_at 2026-10-17T20:39:26+08:00, 8 cpus / 10240 MB / priority 0) — submitted by the submission lane, **not by me**
- M measured in log: **15** (`Step number ... on scan point N out of 15`, first at L1635) — matches “15 几何 = S 14 步”

## Marker line numbers (measured)
`Optimization completed.` L15381, L23685, L33635 ; `-- Stationary point found.` L15382, L23686, L33636 ;
`Normal termination` none yet ; `Error termination` none yet ; point 4 already started (L34506).

## Per-point table (converged frames only)

| scan point N out of M | converged? | frame line (Standard orientation) | SCF Done line | E(RB3LYP)/Ha | dE vs pt1 (kcal/mol) | R(1,29)/A | R(28,29)/A | R(2,4)/A | R(28...H24)/A | R(O28-H24)/A | R(O11-H24)/A | R(25...29)/A | R(25...1)/A | minsep/A | minsep pair | minsep class | min nonbonded/A | min nonbonded pair | heavy Kabsch RMSD vs prev/A | tier | opt steps | SCF cycles |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 out of 15 | True (L15375) | L14777 | L14996 | -939.308205969 | +0.000 | 4.3543 | 1.2258 | 1.3751 | 1.6706 | 1.6706 | 1.0010 | 2.7635 | 3.1774 | 0.9738 | O25-H26 | bonded | 1.5008 | H26-H27 | n/a (first) | 0 (plain H-bond) | 16 | 6 |
| 2 out of 15 | True (L23679) | L23076 | L23310 | -939.307993585 | +0.133 | 4.1543 | 1.2259 | 1.3751 | 1.6688 | 1.6688 | 1.0005 | 2.7391 | 3.1280 | 0.9737 | O25-H26 | bonded | 1.5001 | H26-H27 | 0.131 | 0 (plain H-bond) | 9 | 7 |
| 3 out of 15 | True (L33629) | L33028 | L33247 | -939.306988918 | +0.764 | 3.9543 | 1.2260 | 1.3749 | 1.6686 | 1.6686 | 0.9997 | 2.7396 | 3.0897 | 0.9735 | O25-H26 | bonded | 1.4986 | H26-H27 | 0.144 | 0 (plain H-bond) | 11 | 6 |

Column notes: dE is pure electronic energy relative to the FIRST point, kcal/mol (1 Ha = 627.509474 kcal/mol), each point's own `SCF Done` line number is in the table. Heavy-atom Kabsch RMSD uses the 20 non-H atoms (21 H excluded), optimal rigid superposition against the PREVIOUS point, no atom permutation. R(28...H24) and R(O28-H24) are the same atom pair (28-24), so the two columns are numerically identical every frame; both are printed because the criteria require both, and R(O11-H24) (donor covalent O-H) is printed as independent proton-transfer evidence.

## Scan-coordinate sanity (R(1,29) recomputed from coordinates vs designed 4.3543 - 0.2000*(N-1))
- point 1: R(1,29) = 4.3543, designed 4.3543, dev -0.0000 A
- point 2: R(1,29) = 4.1543, designed 4.1543, dev -0.0000 A
- point 3: R(1,29) = 3.9543, designed 3.9543, dev -0.0000 A

## Convergence-check tables quoted verbatim from the log (immediately above each `Optimization completed.`)
- point 1 (L15375): Max Force 0.000034/0.000450 YES; RMS Force 0.000007/0.000300 YES; Max Displacement 0.001535/0.001800 YES; RMS Displacement 0.000323/0.001200 YES
- point 2 (L23679): Max Force 0.000060/0.000450 YES; RMS Force 0.000009/0.000300 YES; Max Displacement 0.001754/0.001800 YES; RMS Displacement 0.000520/0.001200 YES
- point 3 (L33629): Max Force 0.000029/0.000450 YES; RMS Force 0.000004/0.000300 YES; Max Displacement 0.000507/0.001800 YES; RMS Displacement 0.000116/0.001200 YES

## Frozen-criteria checks on these three points
- **Tier (same-frame rule)**: point1 1.6706 A, point2 1.6688 A, point3 1.6686 A → all **> 1.50** ⇒ **tier 0 (plain H-bond)**, all three enter the main profile. No tier-1 or tier-2 point exists yet, so no separate view is needed yet.
- **Design sec.4 stop condition 1 (enamine C-N)**: R(2,4) = 1.3751 → 1.3751 → 1.3749, max change 0.0002 A (≪ 0.05 A) ⇒ not triggered.
- **Design sec.4 stop condition 3 (scan direction)**: R(1,29) decreases 4.3543 → 4.1543 → 3.9543 as designed ⇒ not triggered.
- **Branch-switch guard**: heavy-atom Kabsch RMSD 0.131, 0.144 A (≪ 0.3 A); no energy drop (dE rises +0.133, +0.764 kcal/mol); H-bond distances change by <0.002 A ⇒ no conformational branch switch.
- **Profile so far**: dE rises smoothly with the C1...C29 contraction (+0.764 kcal/mol at 3.9543 A). **No peak exists in the first three points**, so no TS candidate and **no ΔE‡ is written** (and with only 3 of 15 points no statement about a barrier or its absence is made).

NOT a terminal reading: job 1075 was still running at 21:26:24 CST (point 4 at step 2, L35437); no `Normal termination` / `Error termination` line existed yet.