# NY3 · E1 升级阶梯候选附录（d230 与 img_03）· small_mol 道 as_f99001ff9213455c

用途：按整合道 2026-10-17 的答复（evt_afd6b1eab42e4fa5）要求，为升级阶梯里的两个**备用初猜**各补一份「构造参数 + 三判据读数 + 有无 compute record 的说明」。**本文件不含任何能量主张**，两个候选都是几何初猜。

判据（整合道 §22 确认版）：① d(O1···C4) ∈ 2.10–2.40 Å；② |ΔD(8,4,5,6)| ≤ 10° **且** |ΔD(1,2,3,11)| ≤ 15°（同时）；③ Na–O1 ≤ 2.60 Å 且 |Δ∠Na-O1-H6| ≤ 25°；参考 BD∠O1–C4–O5 ∈ 100–115°。
RC 基准（`gold_finish_20261015/NY3/E1/rc_dft_min_working_order.xyz` sha256 `449cad42aa779d00dd0f454c5b0eb93a9b4bdb771d6de8772cf9912aa7adef68`，job 967）：d 2.803｜C4–O3 1.329｜C4=O5 1.222｜O1–H6 0.965｜Na–O1 2.093｜Na–O5 2.409｜Na–O3 4.258｜BD 96.1｜D_Me −60.4｜D_OH −152.4｜∠Na-O1-H6 145.4。
原子序（1-based，与 ts_0007 工作序同）：1 Na｜2 O1｜3 H6｜4 C2(Me)｜5 O3(OMe)｜6 C4｜7 O5(=O)｜8-10 H(Me)｜11 H(C4)。
符号提醒：`internal_coordinates(analyze)` 报 H8-C4-O5-C6 **τ = +60.4°**，与自算的 **−60.4°** 是同一取向的两种约定。

---

## A. `gold_finish_20261015/NY3/E1/e1_tsguess_rigid_swing_d230.xyz`（刚性摆动族，升级阶梯首选）
sha256 `523392c1735a83f670566401e3e18a51387b13899d254fb3c4aceabc82ff6e36`

### A.1 构造参数（逐位可复算）
- 源：RC = 上述 `rc_dft_min_working_order.xyz`（sha 449cad42…）。
- 摆动轴：过 Na（原子 1）、方向 `n = unit((O1−Na) × (C4−Na))` = Na–O1–C4 平面法向；实测 `n = (0.0049, −0.0194, −1.0000)`（≈ −z；该分子在 RC 近平面，全部原子方向与此法向夹角 79.4–99.9°）。
- 摆动对象：原子 **{2 O1, 3 H6} 整体刚体旋转**（Rodrigues 右手法则绕 n）；**其余 9 个原子完全冻结**。
- 角度：由余弦定理 `cos θ = (r1² + r2² − d²)/(2 r1 r2)`，r1 = |Na–O1| = 2.093 Å、r2 = |Na–C4| = 2.931 Å；RC θ = 65.4° → 目标 d = 2.30 Å 对应 θ = 51.2°，**Δθ = 14.12°**（顺时针/逆时针由「使 d 更接近目标」的符号搜索确定，程序内两符号都算后取误差小者）。
- 未落盘的邻近值仅供对照：d = 2.40/2.20/2.10 Å 对应 Δθ = 11.36/16.87/19.61°。

### A.2 三判据读数（自算公式 + `internal_coordinates(analyze)` 交叉核对）
| 量 | 值 | 判据 | 结论 |
|---|---|---|---|
| d(O1···C4) | **2.300** | ① 2.10–2.40 | ✔ |
| Na–O1 | **2.093**（= RC） | ③ ≤ 2.60 | ✔ |
| ∠Na-O1-H6 | **145.4**（Δ 0.0） | ③ |Δ| ≤ 25 | ✔ |
| D(8,4,5,6) | **−60.4**（Δ 0.0） | ② ≤ 10 | ✔ |
| D(1,2,3,11) | **−156.5**（Δ +4.1） | ② ≤ 15 | ✔ |
| BD∠O1–C4–O5 | 98.5 | 参考 100–115 | 低 1.5°，**不达标但如实登记** |

其余量逐位等于 RC：C4–O3 1.329｜C4=O5 1.222｜O1–H6 0.965｜Na–O5 2.409｜Na–O3 4.258。
工具原文（`internal_coordinates(analyze)` 直接读该文件）：`Fragments: 1`；`r(O2-C6)=2.300 Å [forming (distance heuristic)]`；`r(O2-H3)=0.965`；`r(O5-C6)=1.329`；`r(C6-O7)=1.222`；`r(Na1-O2)=2.093 [bonded]`；`r(Na1-O7)=2.409 [bonded]`；`r(Na1-O5)=4.258 [far]`；`H8-C4-O5-C6 τ=60.4°`；`Bond anomalies: 2  Angle anomalies: 8`（与 RC 同计数）。

### A.3 compute record 状态（**必须随引用**）
- 该文件由**会话内刚体旋转代码**（Rodrigues，参数见 A.1）机器生成 ⇒ 写入时平台给出 **“suspected handwritten coordinates”** 提示；坐标**不是**手抄、不是凭记忆转录，但**没有任何 compute record 与之绑定**（无 SCF、无梯度、无频率、无日志）。
- 因此：**它只能是 provided guess**，不能作为任何 DAG 证据；E1 的正式证据必须来自管线以它为起点跑的 TS Opt+Freq（+ 连通性口径）之原生日志。若评审要求「坐标必须可追溯到工具/compute record」，本文件**不满足**该要求，请改用有工具回执的 `e1_tsguess_img04_retorsion.xyz`（sha `3af1c8c2…`，`internal_coordinates(transform)` 的 operations_applied 可查）或 IDPP 帧。
- 也**不是**鞍点、不是能垒证据；它的价值只在于「三个硬判据全过、且两个软自由度与 RC 逐位相同」。

---

## B. `gold_finish_20261015/NY3/E1/interp/img_03.xyz`（IDPP 帧，升级阶梯次选）
sha256 `0ece3b21bf249368bf5b3a929bf0abced81a6d1ba7703cc17f01b751affde789`

### B.1 构造参数（引自 `gold_finish_20261015/NY3/E1/E1_GUESS_V2_PROVENANCE.md` §2，该文件 sha256 见 §D.3）
- 工具调用：`ts_guess(mode='interpolate', engine='gaussian', interp_method='idpp', n_images=11, atom_map=[1,4,5,6,2,7,8,9,10,11,3]（product 序 → reactant 序，1-based）, watch_pairs=[[2,6],[6,7],[2,3]], output_dir=gold_finish_20261015/NY3/E1/interp)`
- 两个端点（都是本 run ts_0007 内、同批 G16 同口径的实测极小值）：
  - reactant（= RC/job 967）`ts/ts_0007/jobs/declaration_0001/candidate_opt/optimized_seed.xyz` sha256 `fb6f29c5bbc098007632979c3b1361194e1efc1ee827fc2c83827a0d49cafa7d`，E(RB3LYP) = −466.986564979
  - product（= I1/job 985）`ts/ts_0007/jobs/declaration_0001/product_seed_opt/optimized_seed.xyz` sha256 `b7e835859f231194f6b3a967d44d53861c9dc8b971769c5e79fe08a8ff97b7eb`，E(RB3LYP) = −467.004842485
- img_03 的来源自证：上述文件 §2 的 IDPP 距离表 frame 3 为 O1···C4 = 2.3608、C4=O5 = 1.2410、O1–H6 = 0.9662 Å，与我实测该文件得到的 2.361 / 1.241 / 0.966 Å 逐位一致 ⇒ `img_03.xyz` = 该插值路径第 3 帧。
- 注意：§2 当时**选中**的帧是 `img_05`（2.086 Å，工具 `ts_candidate_index=5`），不是 img_03；img_03 是升级阶梯里的备选。

### B.2 三判据读数
| 量 | 值 | 判据 | 结论 |
|---|---|---|---|
| d(O1···C4) | **2.361** | ① 2.10–2.40 | ✔ |
| Na–O1 | **2.567** | ③ ≤ 2.60 | ✔（仅余 0.033 Å） |
| ∠Na-O1-H6 | 113.3（Δ **−32.1**） | ③ |Δ| ≤ 25 | ✘ |
| D(8,4,5,6) | −33.4（Δ **+27.0**） | ② ≤ 10 | ✘ |
| D(1,2,3,11) | −99.8（Δ **+52.6**） | ② ≤ 15 | ✘ |
| BD∠O1–C4–O5 | 109.1 | 参考 100–115 | ✔ |

其余量：C4–O3 1.371｜C4=O5 1.241｜O1–H6 0.966｜Na–O5 2.276｜Na–O3 4.088。
工具原文：`r(O2-C6)=2.361`；`r(Na1-O2)=2.567`；`r(Na1-O7)=2.276`；`H8-C4-O5-C6 τ=33.4°`。

### B.3 compute record 状态
- **有工具级 provenance**（IDPP 由平台 `ts_guess` 生成，两端点均有原生日志与同批能量），但 **IDPP 本身不含能量** ⇒ 只有几何意义；两端点的能量属于「上一批」实测值，**不得**与本轮任何 TS 能量混减。
- 与 A 相反，它**不是** handwritten 提示对象；作为 provided guess 可被直接绑定。
- 同样**不是**鞍点、不是能垒证据。

---

## C. 四个候选并列（供整合道按阶梯挑，全部实测）
| 候选 | d(O1···C4) | Na–O1 | D_Me (Δ) | D_OH (Δ) | ∠Na-O1-H6 (Δ) | BD | ① | ② | ③ | compute record |
|---|---|---|---|---|---|---|---|---|---|---|
| `interp/img_04.xyz`（**job 1018 当前绑定**）sha `44b44952…` | 2.230 | 2.732 | −19.3 (+41.1) | −97.4 (+55.0) | 102.9 (−42.5) | 110.3 | ✔ | ✘✘ | ✘✘ | 工具 IDPP（端点有原生记录；IDPP 无能量） |
| `interp/img_03.xyz` sha `0ece3b21…` | 2.361 | 2.567 | −33.4 (+27.0) | −99.8 (+52.6) | 113.3 (−32.1) | 109.1 | ✔ | ✘✘ | ✔/✘ | 同上 |
| `e1_tsguess_rigid_swing_d230.xyz` sha `523392c1…` | 2.300 | 2.093 | −60.4 (0.0) | −156.5 (+4.1) | 145.4 (0.0) | 98.5 | ✔ | ✔ | ✔ | **无**（会话内机器生成；平台标 handwritten；仅作 guess） |
| `e1_tsguess_rigid_swing_d220.xyz` sha `95b766605cd12732924e1b39fe446017b36a71aa83da7a9eec629ed0f2d69877` | 2.200 | 2.093 | −60.4 (0.0) | −157.3 (+4.9) | 145.4 (0.0) | 98.8 | ✔ | ✔ | ✔ | **无**（同 d230 构造、Δθ = 16.87°；handwritten 提示；仅作 guess） |
| `e1_tsguess_img04_retorsion.xyz` sha `3af1c8c2…` | 2.230 | 2.732 | −60.4 (0.0) | −152.4 (0.0) | 102.9 (−42.5) | 110.3 | ✔ | ✔ | ✘✘ | 工具 `internal_coordinates(transform)`（有 operations_applied 回执） |
（另一族 `e1_tsguess_xtbscan_p0005/p0006/p0007.xyz` 见 `gold_finish_20261015/NY3/E1/TS_E1_XTB_SCAN_FRAMES_PROVENANCE.md`：d ∈ 2.24–2.34、ΔD_Me ≈ −11、∠Na-O1-H6 ≈ +28–30、BD 93.5–95.7。）

---

## D. 同一坐标上的 DFT 与 xTB 受约束剖面：**方向相反**（都是约束剖面，都不是能垒）
### D.1 DFT（job 989，B3LYP-D3(BJ)/def2SVP + CPCM(water)，与战役同批同口径）
原生日志 `gold_finish_20261015/NY3/E1/E1_scan_O1C4.log` sha256 `62ac90e3732663dc82de1339fe1623b3e3457a4528d2d1f92d8bf3748442dca4`（40686 行）；输入 `gold_finish_20261015/NY3/E1/E1_scan_O1C4.gjf` sha256 `8e2a37eb4e745d4d8196899d96183a67aa08ee3057c78615577424794cb0a1cf`（`#p opt=modredundant b3lyp/def2svp empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=water)`，`B 2 6 S 12 -0.1`）。
逐点（每点「末次 SCF Done」= 该约束点收敛能量；扫描坐标值取自各点的 `R(2,6)` 打印行）：
| 点 | d(O1···C4) | 收敛能量 Ha | 行号（末次 SCF / Optimization completed / R(2,6)） | ΔE vs 2.803 (kcal/mol) | -DE/DX |
|---|---|---|---|---|---|
| 1 | 2.803 | −466.986565136 | L2285 / L2418 / L2428 | 0.00 | 0.0 |
| 2 | 2.703 | −466.986190365 | L9284 / L9429 / L9439 | **+0.24** | 0.0033 |
| 3 | 2.603 | −466.984669315 | L14020 / L14164 / L14174 | **+1.19** | 0.0084 |
| 4 | 2.503 | −466.981571100 | L19607 / L19754 / L19764 | **+3.13** | 0.0154 |
| 5 | 2.403 | 未收敛（`-- Number of steps exceeded, NStep= 45` @L40448；`Error termination via Lnk1e … l9999.exe` @L40683；最后一次 SCF −466.984727401 @L40314） | — | — | — |
⇒ DFT 侧：d 由 2.803 缩到 2.503 时**约束能量单调上升**（+3.13 kcal/mol），且各点沿该坐标的残余梯度非零（`-DE/DX` 0.0033/0.0084/0.0154，行号同上）⇒ 到 2.503 Å 为止**还没见到峰**，脊线在更短距离处（这正是把 2.2–2.4 Å 作为起点窗口的依据）。**这不是能垒数字**：约束剖面不是反应路径，其最高已收敛点（+3.13）既不是 TS 能量也不是 ΔE‡；第 5 点未收敛属技术性失败，不作任何结论。
### D.2 xTB（job 1015，GFN2-xTB/ALPB water）
见 `gold_finish_20261015/NY3/E1/TS_E1_XTB_SCAN_FRAMES_PROVENANCE.md` sha256 `681712fc4063cf21cb1b327511915abdf59b4fa9b41b31956de81dc20a105a6a`：同一坐标（2.55→1.90 Å）**单调下降** 0 → −21.37 kcal/mol；平台 `ts_guess(scan_parse)` 判 `scan_has_internal_peak = false`、`barrier_kcal = null`、无候选。
### D.3 结论与**勘误**
- **两侧方向相反**：DFT 侧约束能量随 d 缩短而升（到 2.503 Å 仍升），xTB 侧随 d 缩短而降。二者都不是能垒；分歧最可能来自方法（GFN2 的 Na 过配位：xTB 帧 Na–O1 1.89–1.95 vs DFT 2.093、Na–O5 ~2.01–2.04 vs 2.409）与约束/收敛行为差异。**该分歧只能由管线在 DFT 层的 TS Opt+Freq 判定，不能靠任一条扫描外推**。
- **勘误（请整合道登记）**：`gold_finish_20261015/NY3/E1/E1_GUESS_V2_PROVENANCE.md`（sha256 `97c422d592b662475cd28a1121a50b9b5ed1fed23c86ba6ed4f2575eb91ecf97`）§3 的「逐点（各点末次 SCF Done）」表里四个能量不是该点收敛值：它们的行号 L2793 / L9805 / L14540 / L20129 落在**下一个扫描点优化块的开头**，是那一块的首个 SCF；对应的 ΔE（+0.94/+2.96/+6.32）因此偏大。正确值见本文件 §D.1 表（与 `E1_SCAN_PROVENANCE.md`（sha256 `30b625eb003acacbfb3070aa68072656dd448008a18ef62df6ec8c5b3bbc8e63`）§2 表的 +0.00/+0.24/+1.19/+3.13 一致）。建议以 §D.1 表与 `E1_SCAN_PROVENANCE.md` 为准。
