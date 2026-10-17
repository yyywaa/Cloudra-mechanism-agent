# E2 1D relaxed scan — per-point table (7 of 15 points converged) + Kabsch-convention reconciliation

Measured **2026-10-17 22:12:09–22:12:26 CST**; read-only (`evidence/extract_scan_table.py` sha256 `f2e9e1c9754722b99e6f4891a161adb2d5843b602cfe38dd90b37831c77342b6`,
`evidence/diag_kabsch_variants.py` sha256 `64393be824f8d0824bb95a1599596c57643819f55b7d5d1f9715c63da44062d6`).

- log: `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan.log`
- log sha256 `1018dad6d016e90243c22908bae8cd79b82427ac26db07e6d1965b06f0723bcb` at 22:12:09 (**77577 lines / 5012194 B**); a later read at 22:12:26 gave `36181da971ffd05fb3b897bbb982eecf366e23da8c1c68551c9526165e582ef7` (same 7 converged points; log still growing)
- input gjf sha256 `6301b836b6ca0006f365d80e28cff2f552bd06edae8f54475d6985e751ffbb16` (52 lines / 2415 B); job **1075** (started_at 2026-10-17T20:39:26+08:00, 8 cpus / 10240 MB / prio 0), submitted by the submission lane, not by me
- M = **15** (`on scan point N out of 15`); `Optimization completed.` L15381, L23685, L33635, L43674, L56487, L67553, **L75938**; `Normal termination` / `Error termination`: none yet

| 点 | 帧 / SCF Done 行号 | E(RB3LYP)/Ha | ΔE vs 首点 kcal/mol | 步增量 | R(1,29)/Å | R(28,29)/Å | R(2,4)/Å | R(28···H24)=R(O28–H24)/Å | R(O11–H24)/Å | R(25···29)/Å | R(25···1)/Å | minsep/Å（对） | 重原子 Kabsch RMSD vs 上一点/Å (约定 A) | 档 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | L14777 / **L14996** | −939.308205969 | +0.000 | — | 4.3543 | 1.2258 | 1.3751 | 1.6706 | 1.0010 | 2.7635 | 3.1774 | 0.9738（O25–H26） | n/a | 0 |
| 2 | L23076 / **L23310** | −939.307993585 | +0.133 | +0.133 | 4.1543 | 1.2259 | 1.3751 | 1.6688 | 1.0005 | 2.7391 | 3.1280 | 0.9737（O25–H26） | 0.1311 | 0 |
| 3 | L33028 / **L33247** | −939.306988918 | +0.764 | +0.631 | 3.9543 | 1.2260 | 1.3749 | 1.6686 | 0.9997 | 2.7396 | 3.0897 | 0.9735（O25–H26） | 0.1437 | 0 |
| 4 | L43069 / **L43288** | −939.305208981 | +1.881 | +1.117 | 3.7543 | 1.2254 | 1.3747 | 1.6822 | 0.9972 | 2.8114 | 3.0769 | 0.9732（O25–H26） | 0.1657 | 0 |
| 5 | L55882 / **L56101** | −939.303251773 | +3.109 | +1.228 | 3.5543 | 1.2245 | 1.3745 | 1.7278 | 0.9930 | 3.0288 | 3.1380 | 0.9730（O25–H26） | 0.5255 | 0 |
| 6 | L66948 / **L67167** | −939.301736263 | +4.060 | +0.951 | 3.3543 | 1.2237 | 1.3738 | 1.7711 | 0.9895 | 3.1517 | 3.1852 | 0.9731（O25–H26） | 0.8334 | 0 |
| 7 | L75323 / **L75557** | −939.300096247 | +5.089 | +1.029 | 3.1543 | 1.2230 | 1.3733 | 1.8089 | 0.9868 | 3.2048 | 3.2143 | 0.9725（**O25–H27**） | 0.3746 | 0 |

## Kabsch/RMSD convention battery (why 0.131/0.144 vs 0.0709/0.0698 cannot both be the same quantity)
15 explicitly-labelled conventions were evaluated on the SAME converged frames (last `Standard orientation` before each `Optimization completed.`), 20 non-H atoms:

| convention | pair 1→2 | pair 2→3 | pair 4→5 | pair 5→6 | pair 6→7 |
|---|---|---|---|---|---|
| A heavy superpose / heavy RMSD sqrt(Σd²/N) | 0.1311 | 0.1437 | 0.5255 | 0.8334 | 0.3746 |
| B heavy superpose / heavy sqrt(Σd²/3N) (per-coordinate) | 0.0757 | 0.0829 | 0.3034 | 0.4812 | 0.2163 |
| C reflection allowed / heavy sqrt(Σd²/N) | 0.1311 | 0.1437 | 0.5255 | 0.8334 | 0.3746 |
| D all-atom superpose / heavy sqrt(Σd²/N) | 0.1442 | 0.1578 | 0.5315 | 0.8475 | 0.3866 |
| E all-atom superpose / all-atom | 0.1718 | 0.1861 | 0.6161 | 0.9964 | 0.4601 |
| F all-atom superpose / heavy per-coordinate | 0.0833 | 0.0911 | 0.3069 | 0.4893 | 0.2232 |
| G heavy superpose / heavy excluding C1,C29 | 0.1423 | 0.1572 | 0.5255 | 0.8477 | 0.3893 |
| H heavy superpose / heavy mean\|d\| | 0.1236 | 0.1362 | 0.4797 | 0.7815 | 0.3463 |
| I enamine superpose / heavy | 0.1425 | 0.1456 | 0.2942 | 0.4820 | 0.2017 |
| J mass-weighted heavy superpose | 0.1314 | 0.1441 | 0.5285 | 0.8338 | 0.3738 |
| K enamine-heavy superpose / enamine-heavy | 0.1922 | 0.1963 | 0.3967 | 0.6500 | 0.2720 |
| L heavy-no-water superpose / same set | 0.1305 | 0.1424 | 0.4982 | 0.8030 | 0.3629 |
| M benzaldehyde-heavy superpose / same set | 0.1224 | 0.1470 | 0.7314 | 1.0081 | 0.5012 |
| N ring-core (atoms 2–9) superpose / same set | 0.1768 | — | — | — | — |
| O ring-core (atoms 2–9) per-coordinate | 0.1021 | — | — | — | — |

**Observation:** for pairs 1→2 and 2→3 **every** Cartesian convention gives 0.0757–0.1963, and **every** one of them *increases* from the first pair to the second. The reported 0.0709/0.0698 lies below the whole Cartesian range **and decreases** in the same direction where all Cartesian variants increase.
⇒ 0.0709/0.0698 cannot be a Cartesian heavy-atom Kabsch RMSD on these frames; it is either a different frame pair, a different atom set, an internal-distance (alignment-free) RMSD, or a different normalization. **Open question, not a settled correction.**

## Effect on the frozen 0.3 Å branch-switch guard
The guard needs three conditions together (RMSD jump, energy jump-**down**, H-bond jump). Under every convention tested the >0.3 Å pairs are 4→5 and 5→6 (A: 0.5255/0.8334; B: 0.3034/0.4812; 6→7 also 0.3746 under A only), but the energy **rises** (+1.228 / +0.951 / +1.029 kcal/mol) and R(28···H24) moves smoothly (1.6822 → 1.7278 → 1.7711 → 1.8089 Å, ≈0.04 Å per step, no jump) ⇒ **not a conformational branch switch under any convention**; the verdict does not depend on the convention dispute.

## Frozen-criteria verdicts at 7 points
- tier: R(28···H24) = 1.6706/1.6688/1.6686/1.6822/1.7278/1.7711/1.8089 Å — all > 1.50 Å ⇒ **all tier 0**; R(O11–H24) 1.0010 → 0.9868 Å (−0.014 Å) — donor O–H intact, no shared/transferred proton.
- R(2,4) 1.3751 → 1.3733 Å (max change 0.0018 Å ≪ 0.05 Å) ⇒ design stop cond. 1 not triggered; R(1,29) 4.3543 → 3.1543 Å keeps decreasing (dev. 0.0000 Å) ⇒ stop cond. 3 not triggered.
- profile: monotonic rise 0 → +5.089 kcal/mol (increments 0.133 / 0.631 / 1.117 / 1.228 / 0.951 / 1.029) ⇒ **no peak in 7 points**, no TS candidate, **no ΔE‡**, no claim about a barrier or its absence (7 of 15).
- side note: at point 7 the global minsep switches from O25–H26 (0.9731 Å) to **O25–H27 (0.9725 Å)** — a water internal reorientation, not a proton transfer in the 28···24 pair.

NOT a terminal reading: job 1075 was still running at 22:12:26 CST (point 8 in progress).