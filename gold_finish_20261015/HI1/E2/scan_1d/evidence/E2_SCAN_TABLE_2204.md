# E2 1D relaxed scan — per-point table (6 of 15 points converged; job still running)

Measured **2026-10-17 22:03:56–22:04:24 CST**. Full read-only re-extraction with
`evidence/extract_scan_table.py` (sha256 `f2e9e1c9754722b99e6f4891a161adb2d5843b602cfe38dd90b37831c77342b6`)
and motion diagnostics with `evidence/diag_motion.py` (sha256 `f2c64b5ba70c620e97d5f59a0645b7b7980dcb3ae2dd7afd69effea13b68ba9`).

- log: `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan.log`
- log sha256: `3ec67e7cfac03d7ee2c6c09d305e2d9a176931e16a12666c3a65ca6e6def7f8e` (at 22:03:59, **71084 lines / 4591229 B**)
- note: the log keeps growing; a later read (22:04:24) gave sha256 `c17410c7feafda23c20dfe565715433ac619900f201110112ddfe440c7c9a1c0`, 71146 lines — same 6 converged points
- input gjf sha256 `6301b836b6ca0006f365d80e28cff2f552bd06edae8f54475d6985e751ffbb16` (52 lines / 2415 B)
- job **1075** (started_at 2026-10-17T20:39:26+08:00, 8 cpus / 10240 MB / priority 0) — submitted by the submission lane, **not by me**
- M measured in log: **15** (`on scan point N out of 15`); point 7 already started (L69372)

## Marker line numbers (measured)
`Optimization completed.` L15381, L23685, L33635, L43674, L56487, L67553 ;
`-- Stationary point found.` L15382, L23686, L33636, L43675, L56488, L67554 ;
`Normal termination` none yet ; `Error termination` none yet.

## Per-point table (converged frames only)

| scan point N out of M | converged? | frame line | SCF Done line | E(RB3LYP)/Ha | dE vs pt1 (kcal/mol) | step increment (kcal/mol) | R(1,29)/A | R(28,29)/A | R(2,4)/A | R(28...H24)=R(O28-H24)/A | R(O11-H24)/A | R(25...29)/A | R(25...1)/A | minsep/A (pair) | heavy Kabsch RMSD vs prev/A | tier | opt steps / SCF cycles |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 out of 15 | True (L15375) | L14777 | L14996 | -939.308205969 | +0.000 | — | 4.3543 | 1.2258 | 1.3751 | 1.6706 | 1.0010 | 2.7635 | 3.1774 | 0.9738 (O25-H26, bonded) | n/a (first) | 0 | 16 / 6 |
| 2 out of 15 | True (L23679) | L23076 | L23310 | -939.307993585 | +0.133 | +0.133 | 4.1543 | 1.2259 | 1.3751 | 1.6688 | 1.0005 | 2.7391 | 3.1280 | 0.9737 (O25-H26, bonded) | 0.131 | 0 | 9 / 7 |
| 3 out of 15 | True (L33629) | L33028 | L33247 | -939.306988918 | +0.764 | +0.631 | 3.9543 | 1.2260 | 1.3749 | 1.6686 | 0.9997 | 2.7396 | 3.0897 | 0.9735 (O25-H26, bonded) | 0.144 | 0 | 11 / 6 |
| 4 out of 15 | True (L43668) | L43069 | L43288 | -939.305208981 | +1.881 | +1.117 | 3.7543 | 1.2254 | 1.3747 | 1.6822 | 0.9972 | 2.8114 | 3.0769 | 0.9732 (O25-H26, bonded) | 0.166 | 0 | 11 / 6 |
| 5 out of 15 | True (L56481) | L55882 | L56101 | -939.303251773 | +3.109 | +1.228 | 3.5543 | 1.2245 | 1.3745 | 1.7278 | 0.9930 | 3.0288 | 3.1380 | 0.9730 (O25-H26, bonded) | **0.525** | 0 | 14 / 6 |
| 6 out of 15 | True (L67547) | L66948 | L67167 | -939.301736263 | +4.060 | +0.951 | 3.3543 | 1.2237 | 1.3738 | 1.7711 | 0.9895 | 3.1517 | 3.1852 | 0.9731 (O25-H26, bonded) | **0.833** | 0 | 12 / 6 |

Each point's energy is the last `SCF Done:` of its converged block (line number in the table); dE is pure electronic energy vs point 1 (1 Ha = 627.509474 kcal/mol);
heavy-atom Kabsch RMSD uses the 20 non-H atoms, optimal rigid superposition vs the previous point, no permutation.

## Convergence-check tables (verbatim, thresholds in the middle column)
- p1 (L15375): Max Force 0.000034/0.000450 YES; RMS Force 0.000007/0.000300 YES; Max Disp 0.001535/0.001800 YES; RMS Disp 0.000323/0.001200 YES
- p2 (L23679): 0.000060/0.000450 YES; 0.000009/0.000300 YES; 0.001754/0.001800 YES; 0.000520/0.001200 YES
- p3 (L33629): 0.000029/0.000450 YES; 0.000004/0.000300 YES; 0.000507/0.001800 YES; 0.000116/0.001200 YES
- p4 (L43668): 0.000024/0.000450 YES; 0.000004/0.000300 YES; 0.001001/0.001800 YES; 0.000274/0.001200 YES
- p5 (L56481): 0.000006/0.000450 YES; 0.000001/0.000300 YES; 0.000514/0.001800 YES; 0.000135/0.001200 YES
- p6 (L67547): 0.000016/0.000450 YES; 0.000003/0.000300 YES; 0.000728/0.001800 YES; 0.000167/0.001200 YES

## Frozen-criteria verdicts
- **Scan direction (design stop cond. 3)**: R(1,29) 4.3543 / 4.1543 / 3.9543 / 3.7543 / 3.5543 / 3.3543, deviation from the designed sequence = -0.0000 A at every point ⇒ not triggered.
- **Enamine C-N (design stop cond. 1)**: R(2,4) 1.3751 → 1.3738, max change 0.0013 A (≪ 0.05 A) ⇒ not triggered.
- **Proton tier (same-frame rule)**: R(28...H24) = 1.6706 / 1.6688 / 1.6686 / 1.6822 / 1.7278 / 1.7711 A — **all > 1.50 A ⇒ all tier 0** (plain H-bond, they stay in the main profile). R(O11-H24) 1.0010 → 0.9895 A shrinks only 0.012 A; no shared-proton or transferred-proton point exists yet, so no separate tier view is needed yet.
- **Branch-switch guard (three conditions must hold together)**: Kabsch RMSD jumps to 0.525 A (4→5) and 0.833 A (5→6), i.e. the first condition IS met; but the energy **rises** (+1.228, +0.951 kcal/mol) and there is **no** energy jump-down, and the H-bond distances move smoothly (1.6822 → 1.7278 → 1.7711 A, ~0.045 A per step, no jump). Two of three conditions fail ⇒ **not** a conformational branch switch; the two points are treated as ordinary points and flagged in the table.
- **Why the RMSD is large anyway (motion diagnostic, evidence/diag_motion.py)**: after a common heavy-atom superposition the motion is distributed over all three fragments (enamine rms 0.53/0.91 A, water 0.74/1.15 A, benzaldehyde 0.73/1.12 A for 4→5 and 5→6), while internal torsions change smoothly: aryl C29-C30-C31-C32 stays 178.85 / 179.05°, enamine C3-C2-N4-C5 1.97 / 2.07°, C1-C29-O28-C27 39.09 / 42.01° (approach torsion, smooth), water orientation 24.29 / 25.60°. No ring flip, no coordinate switch: this is a soft non-covalent complex relaxing under a steeply rising constraint, not a different conformer/tautomer.
- **Profile**: monotonic rise +0.133 → +4.060 kcal/mol with step increments 0.133 / 0.631 / 1.117 / 1.228 / 0.951 kcal/mol. **No peak in the first six points** ⇒ no TS candidate, **no ΔE‡ written**, and no statement about a barrier or its absence (6 of 15 points).

NOT a terminal reading: job 1075 was still running at 22:04:24 CST (point 7 at step 3, L70308).