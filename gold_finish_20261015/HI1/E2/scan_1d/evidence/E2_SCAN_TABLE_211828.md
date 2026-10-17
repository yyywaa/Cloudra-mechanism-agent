# E2 1D scan — per-point table snapshot at 2026-10-17 21:18:28 CST (2 of 15 points converged)

Produced by (read-only): `python3 evidence/extract_scan_table.py build/E2_1D_scan.log`
script sha256 = f2e9e1c9754722b99e6f4891a161adb2d5843b602cfe38dd90b37831c77342b6
log path    = /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan.log
log sha256  = 02da29e39c072c4558046a57968ee0c1a6dd1531264857845f5edec55ef51075
log lines   = 28892 ; log bytes = 1863515

Measured marker lines: "Optimization completed." at L15381, L23685 ; "-- Stationary point found." at L15382, L23686 ;
M from log = 15 ("... on scan point N out of 15") ; no Normal/Error termination yet.

| scan point N out of M | converged? | frame line | SCF Done line | E(RB3LYP)/Ha | dE vs pt1 (kcal/mol) | R(1,29)/A | R(28,29)/A | R(2,4)/A | R(28...H24)/A | R(O28-H24)/A | R(O11-H24)/A | R(25...29)/A | R(25...1)/A | minsep/A | minsep pair | minsep class | min nonbonded/A | min nonbonded pair | heavy Kabsch RMSD vs prev/A | tier | opt steps | SCF cycles |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 out of 15 | True (L15375) | L14777 (Standard orientation) | L14996 | -939.308205969 | +0.000 | 4.3543 | 1.2258 | 1.3751 | 1.6706 | 1.6706 | 1.0010 | 2.7635 | 3.1774 | 0.9738 | O25-H26 | bonded | 1.5008 | H26-H27 | n/a (first) | 0 (plain H-bond) | 16 | 6 |
| 2 out of 15 | True (L23679) | L23076 (Standard orientation) | L23310 | -939.307993585 | +0.133 | 4.1543 | 1.2259 | 1.3751 | 1.6688 | 1.6688 | 1.0005 | 2.7391 | 3.1280 | 0.9737 | O25-H26 | bonded | 1.5001 | H26-H27 | 0.131 | 0 (plain H-bond) | 9 | 7 |

Scan-coordinate sanity: point 1 R(1,29)=4.3543 vs designed 4.3543 (dev -0.0000); point 2 4.1543 vs 4.1543 (dev -0.0000).
Convergence check (point 1, table L15375): Max Force 0.000034/0.000450 YES; RMS Force 0.000007/0.000300 YES; Max Displacement 0.001535/0.001800 YES; RMS Displacement 0.000323/0.001200 YES.
Convergence check (point 2, table L23679): Max Force 0.000060/0.000450 YES; RMS Force 0.000009/0.000300 YES; Max Displacement 0.001754/0.001800 YES; RMS Displacement 0.000520/0.001200 YES.

NOT a terminal reading: job 1075 was still running at snapshot time; no Normal termination line existed yet.