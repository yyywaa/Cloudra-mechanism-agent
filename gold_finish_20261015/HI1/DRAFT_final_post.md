# HI1 终态交付帖草稿（写权会话 as_ec848a7673b74e35；11:20 CST 截断后填终值）

to: as_a341823c436e47ed
主题：gold-finish-20261015

## 一、结论（一句话/边）

| 边 | run / job | result.outcome | 判读 | 回填 |
|---|---|---|---|---|
| HI1_E1 | ts_0008 / 1017 | **null** | 走上 +42.67 kcal/mol 级高能脊（11:14 截断读数；built 序 (4,10) = C3–H22 未参与、C2–N20 built (2,32) = 1.634 Å 偏长），声明 7 对合并边未获单鞍点 ⇒ **缺测** | 不回填 |
| HI1_E2 | ts_0009 / 1008 | **null** | 沿反应坐标外漂（d(1,29) 2.646→5.09 Å；11:14 截断读数 +2.43），未获鞍点 ⇒ **缺测** | 不回填 |
| HI1_EM1（通道 B） | ts_0012 / 1026 IRC + 第 2 次尝试 | **null** | 第 1 次 ts_opt 收敛到 **pseudo-saddle**（−27.9419 cm⁻¹，虚频模对 *[1,29]* 投影仅 0.078%）⇒ 已证伪；第 2 次尝试已提交并在跑（job 1032，11:14 实测 running），未验收（见下） | 不回填 |
| HI1_E3 | ts_0011 / 999 | **null** | ts_opt 收敛到 **I2 盆地几何的浅驻点**（比 job 961 高 +0.98 kcal/mol），**非声明单步 TS** ⇒ **缺测**；1029 频率判定为甲基转动 pseudo-saddle（−128.0397 cm⁻¹） | 不回填 |

**回填 0/4；题源零改动（hi.py、ideapool/tasks/hard/HI1.json、hard.md 均未改）；守卫 `python -m pytest tests/test_benchmark.py -k regenerate_identically` = 4 passed。**

## 二、E1 / E2 / E3 / EM1 的「缺测 + 缺什么 + 已证伪什么」

### E1（ts_0008 / 1017）——非终态截断读数（11:14 CST，job 1017 仍 running，无 termination）
- 读数：末次 SCF `-939.240831682`（**L98349**）；step **99 / 246**（L97487）；日志 **6,289,380 B**，sha256 `3b8e0996febb643be22a2a9dc8e74ccf7784422a280d8c48c71d6bc83457ba0b`；ΔE 相对 **job 907** `-939.308829219`（`E1/runs/RC_optfreq/RC_optfreq.log`，sha256 `fa28545612332f69c60c0b778cd5dd1907b22b8ad36f6b1da7811da1295563ba`）= **+42.67 kcal/mol**。**明文：非终态读数、无 Normal/Error termination、无 Optimization completed ⇒ 不得作为能垒申报。**
- 缺什么：该 7 对合并边的鞍点几何 + 恰 1 虚频且虚频模以声明键对主导的频率证据。
- 已证伪：单步合并（C2–O4 π 断裂 / C2–N20 形成 / H21 迁移 / C3–H22（built (4,10)）参与）在 declaration_0003 seed 下沿一条 **+42–47 kcal/mol 高能脊**缓慢下降（+47.20 → +46.8 → +45.6 → +45.2 → +44.97 → +45.4 → **+42.67 @11:14 截断**），不是鞍点；末帧两分片 = 丙酮+脯氨酸 27 原子 + 苯甲醛 C7H6O 14 原子（**旁观者**，非崩解）。几何导出 `HI1/verify/ts_0008_job1017_last_frame_from_log.xyz` sha256 `5108a92fa63bb13cd90d38981aa8bbf2b7189f5e84ea3ed7c029ad2d88f6a197`。

### E2（ts_0009 / 1008）——非终态截断读数（11:14 CST，job 1008 仍 running，无 termination）
- 读数：末次 SCF `-939.304351052`（**L120485**）；step **129 / 226**（L119614）；日志 **7,696,987 B**，sha256 `e3a0e54301c6db71796a47ca985939948438a6d61291c11e14f1011d7ca334c7`；ΔE 相对 **job 924** `-939.308218263`（`E2EM1/runs/I1_optfreq/I1_S_optfreq.log`，sha256 `6ecf06238ee6e1e976ba30eb15faf655f3ebe5a0126ed37d0dfe9b687dea6a87`）= **+2.43 kcal/mol**。**明文：非终态读数、无 Normal/Error termination、无 Optimization completed ⇒ 不得作为能垒申报。**
- 缺什么：同 E1 的鞍点几何 + 频率证据。
- 已证伪：d(1,29) C1–C29 由 2.646 → **5.093 Å** 持续外漂，反应中心不再成键 ⇒ 该 seed 未走向声明单步。

### EM1（ts_0012 / 通道 B）
- 第 1 次（declaration_0001 frequency + ts_opt）：117 模、**恰 1 虚频 −27.9419 cm⁻¹**，但虚频模对 4 对声明键对（1-based [1,29]/[2,4]/[1,2]/[28,29]）的 **watch_pair_fraction = 0.000776（0.078%）**、heavy_atom_fraction 0.322、位移前 6 为 H38 0.328/H24 0.273/H37 0.244/H41 0.229/H18 0.207/C32 0.207；几何 d(1,29) = **3.198 Å 未成键**，C29=O28 1.216（羰基仍在）⇒ **pseudo-saddle（#190）**，候选 ΔE‡ +9.13 kcal/mol 只作 candidate_only。frequency 日志 `ts/ts_0012/jobs/declaration_0001/frequency/frequency.log` sha256 `a70f1e78…34b54c`；几何 `HI1/verify/ts_0012_freq_geom_from_log.xyz` sha256 `4894c55d…40be6a`。
- 第 2 次：**已提交、结果待定**：lane3 在 1026 于 10:37:21 失败后按授权执行 ts_resume ⇒ ts_0012 **rev 33 / declaration_revision 2 / job 1032**（ts_opt，8c/10240MB）；输入首几何与授权种子 `TS_guess_EM1_j58f8_faceflip.xyz`（sha256 9f4d651a…）**逐坐标相同**（41 原子、max|Δ|=0.0）。截稿时（11:14 CST）该作业**已起跑、state=running**、无 termination、无任何可用读数 ⇒ **不填任何数值**。
- IRC（1026）：job 1026 IRC **failed**（l123）：`irc.log` 820,189 B / 13,596 行，sha256 0670edd2…；**L13593** Error termination via Lnk1e in l123.exe at Sat Oct 17 10:37:21 2026；**L13506** Pt 1 Step number 20 out of a maximum of 20；末次 SCF **L13397** -939.293671877；末段判据 Bulirsch-Stoer Method is not Converging / Delta-x Convergence NOT Met / Maximum number of corrector steps exceded。**只跑正向支路、在第 20 点耗尽 ⇒ 不作连通性证据，也不据此写「无鞍点」**。

### E3（ts_0011 / 999）——终态（10:30:07 CST done）
- 读数：末次 SCF `-939.319094501`（**L124211**）；step **134**/232（L124298）；L124574 `Optimization completed` / L124575 `Stationary point found`；L125662 `Normal termination ... Sat Oct 17 10:30:06 2026`；日志 8,046,622 B，sha256 `a8f56a49dcec0404da9d23071ad444e6a59641852f2657d2d0903fc3e70b4177`。
- 能量差：相对 **job 961**（`-939.320655479`，`E3/runs/I2_optfreq/I2_optfreq.log` sha256 `63dda25e…af0d0e`，117 模 0 虚频）= **+0.98 kcal/mol**。**这只是「该浅驻点相对 job 961 的能量差」，不是 ΔE‡、不是能垒，也不等于「能垒趋近 0」。**
- 终帧几何（`format_converter` log→xyz，frame 133；`HI1/verify/E3_ts0011_job999_final_from_log.xyz` sha256 `46f9512c…c2d799`）：d(2,4) C2=N4 1.299；**d(2,25) C2–O25 = 3.138 Å 未成键**；水完整（O25–H26 0.967、O25–H27 0.989）；**N4–H26 = 3.982 Å 质子未转移** ⇒ 与 I2 连通性一致，**非声明单步 TS**。
- 缺什么：E3 单步协同的鞍点几何 + 频率证据。**虚频判定（job 1029，已终态）**：117 模、**1 imaginary = −128.0397 cm⁻¹**（frequency.log sha256 8366cbc6…，L1502/L1511，Normal termination L5302 @10:55:08）；模式为 **C3 甲基转动**（H15 0.640 / H14 0.592 / H16 0.478，三 H 皆挂在 C3 1.09–1.10 Å；C3 自身仅 0.014），六个 watch atom 的平方位移占比 **0.15%**（我自算；lane2 每对求和口径 0.3%）⇒ **pseudo-saddle（#190 同型），不是声明的 6 对协同 TS**；E3 仍未取得合格 TS、不回填。

## 三、§9 拆步提案（只出文字、未计算；不得当分母）

- **E1（lane1 §15）**：步 A RC→INT1（carbinolamine）：form (2,32) C2–N20 σ、(3,41) O4–H21；break (2,3) C2=O4 的 π、(32,41) N20–H21。步 B INT1→I1+H₂O：form (2,4) C2=C3 的 π、(3,10) O4–H22；break (4,10) C3–H22 σ、(2,3) C2–O4 σ。参考能量：步 A 起点 job 907（0 虚频，锁定）；**INT1 无同批 Opt+Freq 证据 ⇒ 缺测、不得作分母**；步 B 终点 job 924（0 虚频）。
- **E3（lane2 §I）**：步 A I2→hemiaminal：成 (2,25)、断 (25,27)、成 (10,27)（羧酸根 O10；若按声明 map 归 O11 则 (11,27)）；步 B hemiaminal→P：断 (2,4)、断 (25,26)、成 (4,26)。0-based 分别 [[1,24],[24,26],[9,26]] 与 [[1,3],[24,25],[3,25]]。参考能量：步 A 起点 job 961（0 虚频，锁定）；**hemiaminal 现有一条独立无约束 Opt 收敛到的驻点（job 1028：−939.312626605，Optimization completed L17229 / Stationary point found L17230 / Normal termination L18325 @10:56:06；几何 d(2,25)=1.4728、d(2,4)=1.4248、d(10,27)=0.9949、d(25,26)=0.9693、d(4,26)=3.1829，即 C2 同带 N4 与 O25 的半缩胺 + 已质子化 COOH；相对 job 961 +5.04 kcal/mol **只作落地物种/中间体身份证据，不是 ΔE‡、不进任何分母**）**；其**频率判定已取得：0 虚频 ⇒ verified 局部极小**（freq 段 Normal termination L23954 @11:10:09，39 组 Frequencies = 117 模，最低实模 19.8439 cm⁻¹ @L19814，全 log 无 imaginary 表头，log sha256 1ec7e4c6…）；此前仅有的受约束扫描点（job 980 point 5/5，−939.309047571）永不得作分母；P 端点同批无 Opt+Freq。
- 索引序：以上编号均为**工作序/声明序 1-based**；E3 侧编号一律为**工作序 1-based**（= `E3/runs/I2_optfreq/I2_min_v5.xyz` 序，41 原子，sha256 `9a6203ff67d9f0d95ad774e78b17bc397b22992f24cbcdf448f8c5558142ef2b`），与题源 hi.py atom-map 标签（原始序，按 SMILES 出现序；重原子 1–20 + 水 H 21/22，其余 H 无原始编号）对照：**工作序 2=[C:2]**、**4=[N+:20]**（吡咯烷 N）、**10=[O:13]**（羧酸根 O 之一，本构象接受 H27）、**11=[OH:15]**（另一等价 O）、**25=[O:4]（水氧，E3 全部作业恒定为 25）**、**26=[H:21]**（水 H → 产物脯氨酸 N–H）、**27=题源无独立标签**（declare `atom_map` product33↔working27，水 H → COOH）；易混：**工作序 24=[H:22]**（aldol O28–H 的氢，勿与 26/27 混）。`ts/ts_0011/declare.json`（sha256 `b5b883bd09fb0b173fc4d561a5218d3920f6aa04c966e37f0eb7b0eeac8b23ef`）的 `atom_map`（41 项、值域 0..40）为 **0-based、方向 product 坐标序 → reactant 工作序**。E1 侧为**三套序**：**built 序**（声明 `reaction_center` 用）= `E1/lane1/RC_S_canonical.xyz`（sha256 71b23e07…）；**原始序** = job 907 输入序（`E1/runs/RC_optfreq/RC_optfreq.gjf` sha256 81b083af…；log 的 `Input orientation` 首块与 .gjf 逐坐标一致 max|Δ|=0.0）；**product built 序**另成一套（product C2=2、C3=1、N20=4、O4=25、H21=26、H22=27）。逐对对照（built ↔ 原始序 ↔ 题源 map）：C2–O4 = (2,3) ↔ **(2,25)** ↔ (2,4)；C2–C3 = (2,4) ↔ **(2,1)** ↔ (2,3)；C3–H22 = (4,10) ↔ **(1,27)** ↔ (3,22)；N20–H21 = (32,41) ↔ **(4,26)** ↔ (20,21)；C2–N20 = (2,32) ↔ **(2,4)** ↔ (2,20)；O4–H21 = (3,41) ↔ **(25,26)** ↔ (4,21)；O4–H22 = (3,10) ↔ **(25,27)** ↔ (4,22)。全 41 原子置换（built→原始序）= `[3,2,25,1,14,15,16,12,13,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,10,9,11,8,7,6,5,4,24,23,21,22,19,20,17,18,26]`；**job 907 日志原子序 ≠ built 序**。

## 四、三项必声明

1. **方法替代**：本轮 HI1 全部 QM 用 **Gaussian 16（B3LYP-D3BJ/def2SVP，Int(UltraFine)，SCF=Tight，CPCM(DMSO)，q0/m1）**，非题源原定的 ORCA；本机无 ORCA 原生日志，故所有数值均为同批 Gaussian 纯电子能差。
2. **L2 身份缺口**：E2/EM1 既有的 **13.36 / 15.52 kcal/mol 保持不动、不置 null**，但其来源为建在 R-脯氨酸几何上的读数，本机无 ORCA 原生日志 ⇒ 身份缺口已在终稿显式声明（不重算、不改分母）。
3. **(S) 题源下通道命名不可沿用**：题源在 (S) 构型下 E2/EM1 的通道命名与本文实际几何（CIP 原子 8=S、3 分片）不一致，故本文只陈述几何与能量事实，不沿用旧通道标签。

---

_交付说明：全文数值分三类——① 同批 Gaussian 16 纯电子能差（仅 E3 的 +0.98 与 job 1028 的 +5.04，且只作站点/物种身份，不是能垒）；② E1/E2 的 **11:14 CST 非终态截断读数**（禁止作能垒、`result.outcome` 仍为 null）；③ 频率模数/虚频判定（job 1021 伪鞍点、job 1029 伪鞍点、job 1028 0 虚频极小）。_ 
