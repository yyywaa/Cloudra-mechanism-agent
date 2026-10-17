# HL1_E1 · N 侧候选帧导出 provenance（CALC2 任务 4，2026-10-15 夜）

## 来源（原生日志，未改写）
- 原生日志：`gold_finish_20261015/HL1/ts_run/jobs/T3a_ptscan_O1H2.log`（12261 行，Gaussian 16）
- 该日志结局（原文行号）：
  - L12257 `FormBX had a problem.`
  - L12258 `Error termination via Lnk1e in /home/ly/g16/l103.exe at Thu Oct 15 18:20:46 2026.`
  → l103 Berny 冗余坐标崩坏，**非驻点、非收敛**，仅作种子来源。
- 该日志最后一步 SCF：L12194 `SCF Done:  E(RB3LYP) =  -364.301672236     A.U. after   11 cycles`
  （比已确立的 O-侧/产物侧极小值 B = −364.2959653 低 ≈3.6 kcal/mol）

## 导出方式（平台工具，坐标非手写）
1. `format_converter(input_path=.../T3a_ptscan_O1H2.log, input_format="log", output_path=.../prep/N_side_frame_from_T3a.xyz, output_format="xyz")`
   → 平台回执逐字：`Detected gaussian opt, extracted final frame (frame 19) from .../T3a_ptscan_O1H2.log -> .../prep/N_side_frame_from_T3a.xyz.`
2. 导出文件：`gold_finish_20261015/HL1/ts_run/prep/N_side_frame_from_T3a.xyz`，sha256 `dfacf479e41752b8ffc004631135a260e3c53cb752a4b8aa8c58c4357f378538`（19 原子）
3. 输入由 `qm_input_writer`（source_type=xyz_file 指向上述 xyz）生成：
   `gold_finish_20261015/HL1/ts_run/jobs/N_side_optfreq.gjf`，sha256 `0ff3f55d2f3bb16a8e6e244dc2bd91924ae57b2c68259408d56550fe6bb94fdc`
   路由逐字：`#p opt freq B3LYP/def2-SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight`；`1 1`；%nproc=8 / %mem=10GB（未加约束）

## 导出帧的实测几何（本序 1-based = NOTES.md 原子序；距离由导出 xyz 直接计算）
| 距离 | 值 (Å) |
|---|---|
| R(1,2) O1–H2 | 0.9877 |
| R(1,3) O1–H3 | 1.2077 |
| R(3,8) H3–N8 | 1.2184 |
| R(2,8) H2–N8 | 2.5903 |
| R(2,9) H2–O9 | 2.2067 |
| R(1,9) O1–O9 | 2.5561 |
| R(9,16) O9–H16 | 0.9730 |
| R(1,4) O1–H4 | 0.9735 |

⚠ 判读：这不是「质子已在 N8 上」的终态，而是 **H3 桥接 O1/N8 的过渡型帧**（R(1,3)=1.2077 ≈ R(3,8)=1.2184）。
它只是未收敛中间帧（自带 l103 崩坏），必须经未约束 Opt+Freq 才能谈驻点身份。

## 判据（预先声明，防事后解释）
- 未约束 Opt+Freq 收敛且 0 虚频：若 R(3,8) ≈ 1.0 Å（且 R(1,3) ≳ 1.5 Å）⇒ **N-质子化复合物（H2O + N-质子化肟）驻点身份成立**；
- 若滑回 R(1,2)≈0.99 / R(2,9)≈1.077（B 型产物侧）⇒ 该帧不是 N 侧极小值；
- 若出现虚频，如实记录频率值与虚频模式性质（watch pair 用 log_parser 计 H3–N8 / O1–H3 占比）。
