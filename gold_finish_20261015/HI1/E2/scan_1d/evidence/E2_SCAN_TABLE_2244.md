# E2 1D relaxed scan — TERMINAL: 8 of 15 points converged, then Error termination at scan point 9

Measured **2026-10-17 22:44:19–22:45:07 CST**, read-only. Job **1075** is terminal: state `failed`, ended_at **2026-10-17T22:44:09+08:00**.

## Three-item kit
- log: `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan.log` — sha256 **`445956fd7491b68f65da4b1d0172f68ac4e35e19a9a55215d9358390fbe2932e`**, **103879 lines / 6703953 B** (22:44:31 / 22:44:37 CST; unchanged 22:45:07)
- input: `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan.gjf` — sha256 `6301b836b6ca0006f365d80e28cff2f552bd06edae8f54475d6985e751ffbb16`, 52 lines / 2415 B
- job: **1075**, gaussian, started_at 2026-10-17T20:39:26+08:00, ended_at **2026-10-17T22:44:09+08:00**, state **failed**, last_error `calculator 退出码 1；Error termination via Lnk1e in /home/ly/g16/l103.exe at Sat Oct 17 22:44:01 2026. | New curvilinear step failed:  FormB failed. | Error imposing constraints`

## Termination evidence, verbatim
```
103874:  New curvilinear step failed:  FormB failed.
103875:  Error imposing constraints
103876:  Error termination via Lnk1e in /home/ly/g16/l103.exe at Sat Oct 17 22:44:01 2026.
103877:  Job cpu time:       0 days 16 hours  4 minutes 41.9 seconds.
103878:  Elapsed time:       0 days  2 hours  4 minutes  2.1 seconds.
```
`Normal termination` **never appears** in this log. `FormB failed` occurs twice: L103822 and L103874 (the fatal one); `Error imposing constraints` only at L103875.
Preceding internal-coordinate back-transform oscillated: `SLEqS3 Cycle: 120 Max:0.208607 RMS: 117.553` (L103862), `RMS: 36.6973` (L103864), `RMS: 590.951` (earlier in the same point), while `RMS(Cart)` stayed ~1e-4 — i.e. Cartesian steps were tiny but the internal-coordinate solution could not be formed.

## Converged points: 8 of 15 (M = 15)
`Optimization completed.` L15381, L23685, L33635, L43674, L56487, L67553, L75938, **L85975**; `-- Stationary point found.` one line later each.

| 点 | 帧 / SCF Done 行号 | E(RB3LYP)/Ha | ΔE vs 首点 kcal/mol | 步增量 | R(1,29)/Å | R(28,29)/Å | R(2,4)/Å | R(28···H24)=R(O28–H24)/Å | R(O11–H24)/Å | R(25···29)/Å | R(25···1)/Å | minsep/Å（对） | 重原子 Kabsch RMSD vs 上一点/Å (约定 A) | 档 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | L14777 / **L14996** | −939.308205969 | +0.000 | — | 4.3543 | 1.2258 | 1.3751 | 1.6706 | 1.0010 | 2.7635 | 3.1774 | 0.9738（O25–H26） | n/a | 0 |
| 2 | L23076 / **L23310** | −939.307993585 | +0.133 | +0.133 | 4.1543 | 1.2259 | 1.3751 | 1.6688 | 1.0005 | 2.7391 | 3.1280 | 0.9737（O25–H26） | 0.1311 | 0 |
| 3 | L33028 / **L33247** | −939.306988918 | +0.764 | +0.631 | 3.9543 | 1.2260 | 1.3749 | 1.6686 | 0.9997 | 2.7396 | 3.0897 | 0.9735（O25–H26） | 0.1437 | 0 |
| 4 | L43069 / **L43288** | −939.305208981 | +1.881 | +1.117 | 3.7543 | 1.2254 | 1.3747 | 1.6822 | 0.9972 | 2.8114 | 3.0769 | 0.9732（O25–H26） | 0.1657 | 0 |
| 5 | L55882 / **L56101** | −939.303251773 | +3.109 | +1.228 | 3.5543 | 1.2245 | 1.3745 | 1.7278 | 0.9930 | 3.0288 | 3.1380 | 0.9730（O25–H26） | 0.5255 | 0 |
| 6 | L66948 / **L67167** | −939.301736263 | +4.060 | +0.951 | 3.3543 | 1.2237 | 1.3738 | 1.7711 | 0.9895 | 3.1517 | 3.1852 | 0.9731（O25–H26） | 0.8334 | 0 |
| 7 | L75323 / **L75557** | −939.300096247 | +5.089 | +1.029 | 3.1543 | 1.2230 | 1.3733 | 1.8089 | 0.9868 | 3.2048 | 3.2143 | 0.9725（O25–H27） | 0.3746 | 0 |
| 8 | L85370 / **L85589** | −939.297687588 | **+6.600** | +1.511 | **2.9543** | 1.2224 | 1.3731 | 1.8425 | 0.9847 | 3.2420 | 3.2663 | 0.9711（O25–H27） | 0.1575 | 0 |

Every point's convergence table is four YES (point 8 at L85969: Max Force 0.000011/0.000450, RMS Force 0.000001/0.000300, Max Disp 0.001340/0.001800, RMS Disp 0.000340/0.001200).
R(1,29) matches the designed sequence 4.3543 − 0.2000·(N−1) to −0.0000 Å at all eight points.

## The failed scan point 9 (does NOT enter the profile)
- target R(1,29) = **2.7543 Å**; 18 optimization steps were logged (`Step number 18 out of a maximum of 219 on scan point 9 out of 15`, L103757) and the point never reached `Optimization completed.`
- last (unconverged) frame, `Standard orientation` **L103420**: R(1,29) = 2.7543 Å (on target), R(28,24)=R(O28–H24)=**1.8918**, R(O11–H24)=**0.9828**, R(28,29)=1.2260, R(2,4)=**1.3821** (vs 1.3731 at point 8), minsep **0.9625 (O25–H27)**
- its last `SCF Done` (L103669) E = **−939.296849384** Ha ⇒ would be ≈ **+7.13 kcal/mol** vs point 1 — but it is **not converged**, so it is excluded from the profile by the frozen criteria and is quoted only as an indication.

## Frozen-criteria verdicts
- **tier**: R(28···H24) 1.6706 → 1.8425 Å over the eight converged points, all > 1.50 Å ⇒ **all tier 0** (main profile). R(O11–H24) 1.0010 → **0.9847** Å: donor O–H stays covalent, no shared or transferred proton anywhere.
- **profile (main)**: monotonic rise 0 → **+6.600 kcal/mol** (increments 0.133 / 0.631 / 1.117 / 1.228 / 0.951 / 1.029 / 1.511) ⇒ **no peak, no local maximum, no stationary feature among the eight converged points** ⇒ no TS candidate, **no ΔE‡ written**, and no claim that the C–C coordinate is barrierless (the scan did not reach 1.5543 Å).
- **branch-switch guard**: RMSD > 0.3 Å at 4→5 (0.5255) and 5→6 (0.8334), but energy rises and R(28···H24) changes smoothly (~0.04 Å per point) ⇒ three conditions never hold together ⇒ **no conformational branch switch** (unchanged verdict; `evidence/diag_motion.py` shows internal torsions evolve smoothly).
- **design stop cond. 1**: R(2,4) 1.3751 → 1.3731 over the eight converged points (max change 0.0020 Å ≪ 0.05 Å) ⇒ not triggered; the strain shows only in the unconverged point-9 frame (1.3821, Δ = +0.0090 Å).
- **design stop cond. 3**: R(1,29) decreases monotonically as designed (dev 0.0000 Å) ⇒ not triggered.

## Diagnosis (evidence-based, provisional)
The failure is in the *internal-coordinate machinery*, not in SCF: `SLEqS3` internal-coordinate iterations blow up (RMS(Int) up to ~591 with RMS(Cart) ~1e-4) and l103 then reports `New curvilinear step failed:  FormB failed.` / `Error imposing constraints`. As C1 approaches C29 (2.95 Å → 2.75 Å) plus the simultaneous water/enamine distortion (O25–H27 0.971 → 0.962 Å), the redundant internal set around the forming bond becomes ill-conditioned, so the constraint `B 1 29` could not be imposed any more.
This is an **input/method diagnostic at scan point 9**, not evidence that the PES has no feature: points 1–8 remain valid; point 9 and beyond are simply not available at the present settings.

## Options for the coordinator (I do NOT resubmit; submission authority is not mine)
1. restart the remaining span from the point-8 converged geometry (R=2.9543 Å) with a **smaller step** (`S n -0.10`, or `-0.05` near contact) — reduces step curvature and the chance of a degenerate B matrix;
2. restart with a **smaller trust radius** (`maxstep=5` or `maxstep=3`) and/or `Opt=(ModRedundant,CalcFC)` to get a better initial Hessian at the restart point;
3. treat the C–C approach as a **2D scan** (C1–C29 × the water/proton coordinate) so the second coordinate is explicit rather than absorbed into the redundant internals;
4. if a barrier is the target, note that **no peak exists in 4.3543 → 2.9543 Å** at this level; any TS claim still requires an independent TS search/frequency check, not this scan.

## Files
`evidence/E2_SCAN_TABLE_2244.md` (this file); extractor `evidence/extract_scan_table.py` sha256 `f2e9e1c9754722b99e6f4891a161adb2d5843b602cfe38dd90b37831c77342b6`; last-frame forensics `evidence/diag_lastframe.py` sha256 `28fd49187621ec0465557484ba5d72f99873d20466a45add0fe25d0e2418e3b8`.