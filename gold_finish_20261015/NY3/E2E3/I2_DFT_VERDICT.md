# I2_DFT_VERDICT — NY3 E2/E3：I2（甲酸 + 甲醇盐 + Na⁺）在本战役级别是否为真极小值

道：NY3 small_mol（E2/E3 势面探索 + 几何与 Opt/Freq 判定道）｜工作根 /home/ly/Cloudra-mechanism-agent｜目录 gold_finish_20261015/NY3/E2E3/
日期：2026-10-17（接 2026-10-15 I2_SEED_NOTE.md 的续作；该文件记录 xTB 筛选与 job 971/981 起点）
口径（逐字）：Gaussian 16 `B3LYP/def2SVP` + `EmpiricalDispersion=GD3BJ` + `Int(UltraFine)` + `SCF=Tight` + `SCRF=(CPCM,Solvent=Water)`，charge 0 / multiplicity 1，%nproc=8 / %mem=10GB，priority 0；半经验探索 xtb 6.5.0 `GFN2-xTB --alpb water`。
原子序约定：**i2 序（1-based）= 1 Na｜2 C2(甲基 C)｜3 O3(甲醇盐/甲醇 O)｜4,5,6 H(甲基)｜7 C4(甲酸 C)｜8 O5(甲酰 O)｜9 O1(羟基 O)｜10 H(C4)｜11 H6**。另一套序 **i1 序 = 1 Na｜2 C2｜3 O3｜4 C4｜5 O1｜6 O5｜7,8,9 H(Me)｜10 H(C4)｜11 H6**（= prep/i1.xyz 与 E2E3/i1_dft_min_ref.xyz 的序）。

---

## 0 结论

1. **I2 成立（本战役级别）**：存在与「H6 仍在 O1（r(O1–H6)=0.972 Å）、C4–O3 已断（4.568 Å）」相容、**梯度已收敛且 0 虚频**（最低实频 21.69 cm⁻¹）的局部极小值（job 990）。⇒ **E2/E3 可按「分步」定义**：E2 = I1→I2 独立步；E3 = I2→P 独立步。
2. **本判据带来的新结构信息（对 E3 的 TS 搜索很关键）**：该 I2 极小值是**松散离子对**，不是紧离子对+氢键：
   Na⁺ 只双配位 O3(2.047 Å)/O5(2.312 Å)，**O1···O3 = 4.194 Å、C4···O3 = 4.568 Å**。
   而 P 极小值（job 994）里 O1···O3 = 2.608 Å、O1···H6 = 1.605 Å（甲酸根···H–O 氢键）。
   ⇒ **E3 不只包含质子转移**：从 I2_min 到 P_min，甲氧基 O3 必须同时向 O1 接近约 1.6 Å。任何"只扫 O1–H6 / O3–H6 一个坐标"的 E3 猜测都不完整；建议 E3 的 guess/IRC 至少覆盖 (O1···O3 接近) + (O3–H6 成键) 两个耦合坐标。
3. **端点极小值之间的相对电子能（同程序、同批、同 route，可相减；均为"极小值之差"，不是能垒，不含任何 ΔE‡）**

| 端点 | job | 能量原始行 | E(RB3LYP) / Ha |
|---|---|---|---|
| I1（四面体中间体） | 927（=922 复现，**只读引用**，无频率） | ts/ts_0003/jobs/declaration_0001/candidate_opt/seed-opt.log:14872 | -467.004842486 |
| **I2（本判据，0 虚频）** | **990**（起点 971 末帧） | freq_i2_candA/i2_candA_freq.log:512 | **-466.986020418** |
| **P（本判据，0 虚频）** | **994** | p_optfreq/p_ref_optfreq.log:10443 | **-467.045937735** |

I2 − I1 = +0.018822068 Ha ≈ **+11.8 kcal/mol**；P − I2 = -0.059917317 Ha ≈ **-37.6 kcal/mol**（I2 比 P 高约 37.6）；P − I1 ≈ **-25.8 kcal/mol**。
与 GFN2-xTB/ALPB water 的 I2 − P = +31.3 kcal/mol（见 I2_SEED_NOTE.md §3）**方向一致**；两个程序不得混减，此处只作方向一致性说明。
**本文件不含任何未测的能垒数字。**



5. **采纳记录**：本结论已由 NY3 整合 Coordinator **as_a396e35616564357** 于 **2026-10-17**（第二轮派单帖，主协调广播时段 06:4x）独立复核后采纳（其独立复算：job 990 的 Frequencies 行 9×3 = 27 = 3N-6 全实、"imaginary" 在日志中出现 0 次、Low frequencies 首值 -12.1370 不是振动模；并从该日志的 Standard orientation 块独立复算几何 O1–H6 0.972 / C4–O1 1.326 / C4=O5 1.209 / C4···O3 4.568 / Na–O3 2.047 / Na–O5 2.312 Å ⇒ 确为 I2 型）。采纳依据 = **job 990 的 0 虚频 + 几何独立复算**；据此 E2/E3 按「分步」定义。

6. **需要补的（缺测）**：E2/E3 的鞍点 + ΔE‡ 完全缺测（本道不提交 TS/IRC，见 §5）；I2_min 尚无「Stationary point found」收敛声明（见 §5）。

---

## 1 证据表（绝对路径 + sha256 + file:line）

| 对象 | 绝对路径 | sha256 | 关键行 |
|---|---|---|---|
| I2 候选几何（交付） | gold_finish_20261015/NY3/E2E3/i2_min_candA.xyz | 1715f6d7d77e93bb5200a71b23db31fc84cb45564b1d48f6bbab2e7ee3c0ef85 | 11 原子，i2 序；末帧坐标 |
| 其来源日志（job 971，opt 被截断） | gold_finish_20261015/NY3/E2E3/i2_candA_optfreq.log | c4e3e99136f11f537cfec51f8a2e6ae36ac616f43c3a12d70d6d15948daab182 | 末帧几何 L21929–21941（Input orientation）/ L21975–21987（Standard orientation）；E = -466.986020418 @L21720；力判据收敛 L21871–21874；NStep=48 超步 L21877；Error termination l9999 @L22116 |
| **freq 判定（job 990）** | gold_finish_20261015/NY3/E2E3/freq_i2_candA/i2_candA_freq.log | **df2548644fc22ac7b64b0da08bded3f44e1ecc9f4db1c5e2015aa2ed954e598b**（1470 行） | E = -466.986020418 @L512；Frequencies -- 首块 21.6936/25.3657/39.6978 @L770；Low frequencies 诊断 @L760-761；ZPE 0.072973 @L968；**Normal termination @L1470**（无 Error termination） |
| freq 输入 | …/freq_i2_candA/i2_candA_freq.gjf | 4127ea8fd30089bf37137f382ee36eb9d4089ebacb67dd144e51f30175a13325 | `#p freq B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=Water)`，0 1 |
| freq 实际几何核验 | …/freq_i2_candA/freq_lastframe.xyz vs i2_min_candA.xyz | （diff 仅注释行："single point" / "opt step=47"） | ⇒ 频率确实算在交付几何上 |
| P 端极小值（job 994） | gold_finish_20261015/NY3/E2E3/p_optfreq/p_ref_optfreq.log | **ff7ecb5aab3724bd2574c37c9a78b309e45f7eabfeb5ec9ec703c53860f816df**（12318 行） | **Optimization completed @L10591 / Stationary point found @L10592**；E = -467.045937735 @L10443（freq 段同值 @L11154）；Frequencies -- 最低 44.5544/85.1565/98.2713 @L11412,11430；ZPE 0.075296 @L11612；Normal termination @L10845 与 @L12318 |
| P 极小值几何 | …/E2E3/p_min_ref.xyz | f69ef3c9215d95fe31a17d4cfecc9a2a0bf111fd932894bf0f236a985348f4ea | i2 序，11 原子 |
| P 端输入 / P 端起点种子 | …/p_optfreq/p_ref_optfreq.gjf；…/E2E3/ref_dft_p_from_i2seed_lastframe.xyz | d0f4f7d341a4c051fac8698a270ecf03e630025cca0fb2c618a8d968f7cc4016；30400b0ccbc1c91af2b0ed241c840a59e42d9bfd6af25f6ffc8ab8bb6cd44be9 | 起点 = job 934 被 NStep=44 截断的 P 型末帧（**不是极小值**） |
| I1 极小值（只读引用，无频率） | ts/ts_0003/jobs/declaration_0001/candidate_opt/seed-opt.log | db30483e93c5f7bc959a5b0eb74df3b17befca22dbf67888e5d32063c9984799 | E = -467.004842486 @L14872；**Optimization completed @L15024 / Stationary point found @L15025**；Normal termination @L15285 |
| I1 几何副本（i1 序，本道复制） | …/E2E3/i1_dft_min_ref.xyz | b7e835859f231194f6b3a967d44d53861c9dc8b971769c5e79fe08a8ff97b7eb | 与 ts/ts_0003 …/optimized_seed.xyz 逐字节相同 |
| xTB 筛选与本轮起点来源 | …/E2E3/I2_SEED_NOTE.md | c1fb933fe4e66b9636a31599fed23a52c78991a3b28884d8326482faf20ed925 | §3 5 个起点全部 0 虚频；§4 job 971/981 |

---

## 2 频率判定细节：为什么「Low frequencies --- -12.1370」不是虚频

job 990 的 `Low frequencies ---` 诊断行（L760-761：-12.1370 / -0.0007 / -0.0001 / 0.0010 / 9.4453 / 16.3711 与 24.5933 / 30.6699 / 43.1316）**不是**虚频，三条独立依据：

1. **模数**：`Frequencies --` 列表 9 行 × 3 = **27 = 3N-6（N=11）且全为正**；最低 21.6936 cm⁻¹（L770）。若存在虚频，Gaussian 会把它作为首个频率以负值打印在该列表里。
2. **热化学模数**：`Vibrational temperatures` 列出 **27** 个值，最低 31.21 K ≙ 21.7 cm⁻¹，与列表逐项吻合（L~950 区）。
3. **ZPE 复算**：日志 ZPE = 0.072973 Ha = 45.79153 kcal/mol（@L968）；对该 27 个正模独立求和 Σ(½hν) = 45.79 kcal/mol，**完全一致**。若把 -12.1370 计入，ZPE 对不上。

补充：日志热化学段还有一行 `Warning -- explicit consideration of 10 degrees of freedom as vibrations may cause significant error`。该警告**不改变**上面的结论：模数（27）、Vibrational temperatures 个数（27）与 ZPE 复算三者互相印证，且 27 = 3N-6 正好用满；若有模态被排除在振动之外，这三者不可能同时吻合。

（log_parser 独立读数：`imaginary_frequencies = []`、`frequencies_cm` 27 项、`normal_termination = true`。）

---

## 3 端点身份与键长（实测，Å）

| 量 | I1_min（只读引用，i1 序） | **I2_min（job 990，i2 序）** | **P_min（job 994，i2 序）** |
|---|---|---|---|
| O1–H6 | 0.971 | **0.972** | 1.605（氢键） |
| O3–H6 | —（H6 在 O1） | **5.056** | **1.009**（H6 在 O3 ⇒ 甲醇） |
| C4···O3 | 1.503 | **4.568** | 3.217 |
| C4–O1 | 1.427 | 1.326 | 1.257 |
| C4=O5 | 1.291 | 1.209 | 1.253 |
| O1···O3 | 2.27（prep 值参考） | **4.194** | **2.608** |
| Na–O3 / Na–O5 / Na–O1 | 2.294 / 2.206 / 2.752 | 2.047 / 2.312 / 3.381 | 2.287 / 2.242 / 3.433 |
| 身份 | 四面体烷氧盐（C4 四配位） | 甲酸 + 甲醇盐 + Na⁺ | 甲酸根 + 甲醇 + Na⁺ |
| 频率 | 未测（无频率段） | **27 模 / 0 虚频 / 最低 21.69** | **27 模 / 0 虚频 / 最低 44.55** |

（I1_min 的 O1···O3 一栏留空说明：job 927 的末帧我没有逐对复测，见 §5 缺测。其余 I2/P 行均由交付文件独立测量。）

---

## 4 对「E2 = I1→I2 独立步 + E3 = I2→P」vs「E2 重定义为 I1→P 协同步、E3 无独立鞍点」的支持方向

- **支持"分步"**：I2 型几何在 DFT 上确为 0 虚频极小值（§1、§2）。一个 0 虚频极小值的松弛产物、且身份与 registry 的 I2（`[Na+].[CH3][O-].[CH](=O)O`）逐项吻合（H6 在 O1、甲氧基独立、C4=O5 双键），就是"E2 有独立产物态"的直接证据。若 E2/E3 真的只能协同步，自由优化不会在"甲氧基已断、质子未转移"的构象上留下一个梯度收敛的盆地。
- **协同步的旁证只覆盖一个特定构象**：job 934 从 `prep/i2.xyz` 出发的自由优化顺流到 P（日志 ts/ts_0003/jobs/declaration_0001/product_seed_opt/seed-opt.log，sha256 3ae4dccbe8ca3119d3fa0853b3bc5ac3743ba3abc3fa52a3314e3858048de8be；末次 SCF -467.045443536 @L24228；NStep=44 @L24632 l9999）。但该起点自身已在 PT 过渡区（O3···H6 1.674 Å、O1···O3 2.671 Å，见 STATUS.md §3 补充事实）⇒ 它证明的是「那个构象不是极小值」，**不是**「所有 I2 构象都不是极小值」。
- **因此本道的判定**：E2 保留为 **I1→I2 独立步（产物端 = job 990 几何）**；E3 保留为 **I2→P 独立步（起点 = job 990 几何、终点 = job 994 几何）**。协同步作为**已被证伪的竞争假设**记录（仅对预转移构象成立；不写进图）。
- **对 E3 的额外提示（§0.2）**：I2_min 里 O3 距 O1 4.194 Å，E3 必须包含 O3 的接近。若 E3 的 TS 搜索只动 H6，会得到 pseudo-saddle 或直接顺流。

---

## 5 缺测清单（不含任何推测值）

1. **E2 / E3 的鞍点与 ΔE‡**：完全缺测。需要：OptTS（恰 1 虚频 + 虚频模归属 watch pair）+ 双向 IRC + 两端点 Opt/Freq 0 虚频身份核验。属 Coordinator 的 ts_prepare 流程，本道不提交。
2. **I2_min 的收敛声明**：job 990 是 freq-only（几何来自被 NStep=48 截断的 job 971，力判据收敛但位移判据未达）。若验收口径要求端点必须是"Opt+Freq 收敛 + 0 虚频"，需补一个 i2_min_candA.xyz 的 opt+freq 复算（成本很小，起点已在驻点上）。
3. **I1 的 0 虚频未判**：job 922/927 无频率段（只读引用，未复核）。
4. **E3 的耦合坐标**：起步几何与终点差 O1···O3 1.6 Å + 质子转移，1D 扫描不足以证明鞍点唯一性；建议两个耦合坐标都覆盖。
5. **模型省略与可能的影响**（必须与结论一起读）：水相只用 CPCM 隐式溶剂，**无显式水/反离子动力学、无温度与浓度**；I2 是松散离子对（Na⁺…甲酸根 3.38 Å、甲醇盐被 Na⁺ 拉住），显式溶剂或显式水分子可能明显改变 I2 与 P 的相对稳定性，也可能给出"溶剂辅助质子转移"的另一种 E3 通道。本文件的结论只在本模型口径内成立。
6. **历史值**：旧 15.5 / 12.5 / 0.0 一律不引用、不作证据。

---

## 6 TS 初猜（本道交付）

两个初猜均为**已落盘的真实几何**（工具产物 + 各自 provenance），供 ts_prepare 使用：

| 步 | 文件 | sha256 | 序 | 构造 | 该帧实测关键键长（Å） |
|---|---|---|---|---|---|
| **E2**（I1→I2，断 C4–O3 / 成 C4=O5） | E2E3/ts_e2_guess.xyz | 8bbc6dbb866df8619b5a150b6c3ea196c575d3b0b9e1398a89b9497de32e9ea0 | **i1/反应物序** | `ts_guess(interpolate, idpp, n_images=11)`：I1 极小值（i1_dft_min_ref.xyz）↔ I2 极小值（i2_min_candA.xyz），atom_map=[1,2,3,7,8,9,4,6,5,10,11]；取 **frame 3** | C4–O3 **2.417**｜C4–O5 **1.262**｜C4–O1 1.390｜O1–H6 **0.969（H6 仍在 O1）**｜C2–O3 1.383｜Na–O3 2.228 / Na–O5 2.219 |
| **E3**（I2→P，H6: O1→O3） | E2E3/ts_e3_guess_v2.xyz | 3ccf834e473dc4f6f0e19b1ad1502d9e0f026ea602d8957b3c5b4fdc4fbfa43f | **i2 序** | `ts_guess(interpolate, idpp, n_images=11)`：I2 极小值（i2_min_candA.xyz）↔ P 极小值（p_min_ref.xyz），atom_map=identity；取 **frame 9**（|O1–H6 − O3–H6| 最小 = 0.127） | O1–H6 **1.536**｜O3–H6 **1.409**（质子居中、两 O 均未成键）｜O1···O3 2.808｜C4···O3 **3.369（甲氧基仍断）**｜C4–O1 1.263 / C4=O5 1.248｜Na–O3 2.261 / Na–O5 2.244 |

provenance：E2E3/TS_E2_GUESS_PROVENANCE.md（sha256 1f911489c7af5a06a3fd1c53b201fefbfce31c81509935f92ee93a2a40a09af9）、E2E3/TS_E3_GUESS_V2_PROVENANCE.md（sha256 059494a83c49d69a1fb789723f9cc26d4aa84a9f12148606d295acf849f99612）；两份都含两端点绝对路径 + sha256、工具与参数（mode/idpp/n_images/atom_map/watch_pairs）、所选帧号、该帧实测键长、1-based 原子序对照。
**声明：两个 guess 只作 TS 搜索的起始几何；IDPP 插值不含任何能量，其能量/键长不作任何能垒/ΔE‡ 证据。**

---

## 7 本道产出文件（sha256 见各自 provenance；此表为索引）

| 文件 | 说明 |
|---|---|
| i2_min_candA.xyz | 交付的 I2 极小值候选几何（i2 序），job 990 判定对象 |
| freq_i2_candA/（gjf+log+chk+lastframe） | **I2 0 虚频证据**（job 990） |
| p_min_ref.xyz + p_optfreq/（gjf+log+chk） | **P 端点 0 虚频极小值**（job 994） |
| i1_dft_min_ref.xyz | I1 极小值几何副本（i1 序，只读引用 ts/ts_0003，供 E2 guess 起点） |
| ts_e2_guess.xyz（sha 8bbc6dbb…）+ TS_E2_GUESS_PROVENANCE.md（sha 1f911489…） | E2 初猜（i1 序，IDPP frame 3）|
| ts_e3_guess_v2.xyz（sha 3ccf834e…）+ TS_E3_GUESS_V2_PROVENANCE.md（sha 059494a8…） | E3 初猜（i2 序，IDPP frame 9；相对 I2_SEED_NOTE.md §6 的 ts_e3_guess.xyz 为 v2）|
| ts_interp_e2/、ts_interp_e3/ | IDPP 图集（img_00…img_10，各 575 B） |
| xtb_scan_e2/（job 1001）、xtb_scan_e3/（job 1003）：manifest（sha 508b2fde… / 60e3fe5c…）+ native_scan_runs/native_scan_0001/{engine.out, point_0001–0013.xyz} | 本轮 xTB(GFN2-xTB/ALPB water) 弛豫扫描（见 §8）：索引基准**实测** = manifest atoms 按 0-based 消费、扫的正是目标键；E2 剖面可用（并给出备用初猜），E3 扫描落到**另一个 P 构象**、不能提供 E3 初猜 |
| ts_e2_guess_xtb.xyz（sha 74fa12bc…）+ TS_E2_GUESS_XTB_PROVENANCE.md（sha 891ceb88…） | E2 **备用**初猜（i1 序，job 1001 扫描 point_0006，C4–O3 2.525 Å）|
| ts_e3_guess.xyz（旧，v1） | 上一轮产物（起点是 prewarped prep/i2.xyz），v2 生效后 v1 只作历史 |
---

## 8 xTB（GFN2-xTB / ALPB water）势面探索（job 1001 / 1003）与索引基准实测

### 8.1 索引基准消歧（**实测结论**）

`ts_guess(scan_prepare)` 把**声明的 1-based 原子号减 1** 存进 manifest 的 `scan.scans[].atoms`；runner 按 **0-based** 消费。逐帧实测（直接读帧文件）：

| run | 我的声明（1-based，按其输入文件的序） | manifest 存值 | 逐帧实测：跟着扫描值走的是哪条键 |
|---|---|---|---|
| **job 1001**（E2，输入 i1 序） | [4,3] = **C4–O3** | [3,2] | **C4–O3**：1.542(点1) → 2.525(点6) → 3.508(点11) → 3.900(点13)；对照组 O3–C2 全程 1.35–1.42 不动 ✓ |
| **job 1003**（E3，输入 i2 序） | [3,11] = **O3–H6** | [2,10] | **O3–H6**：1.030(点1) → 1.683(点5) → 2.208(点8) → 2.899(点12)；对照组 C2–H(C4) 5.57–6.31 不动 ✓ |

⇒ **两条扫描都扫在化学正确的键上**；"runner 按 1-based 读、会扫成 O3–C2 / C2–H(C4)"的假设**被实测证伪**。
原生程序调用行（xtb_scan_e2/native_scan_runs/native_scan_0001/engine.out:85）：
`xtb .../input.xyz --gfn 2 --opt --input .../scan.inp --parallel 1 --chrg 0 --uhf 0 --verbose --alpb water` ⇒ **GFN2-xTB + ALPB water 生效**（input.xyz 与 manifest 的 reactant_xyz 逐位相同 = p_min_ref.xyz / i1_dft_min_ref.xyz）。

### 8.2 E2（I1→I2）GFN2/ALPB 约束弛豫扫描（job 1001）

| 点 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| d(C4–O3)/Å | 1.54 | 1.74 | 1.93 | 2.13 | 2.33 | 2.53 | 2.72 | 2.92 | 3.12 | 3.31 | 3.51 | 3.70 | 3.90 |
| rel/kcal | 0.0 | 4.8 | 10.5 | 15.2 | 18.6 | 20.9 | 22.3 | 22.9 | 23.2 | 23.2 | **23.2** | 23.2 | 23.1 |

**半经验 + 约束扫描 ⇒ 不是 DFT 能垒、不是 ΔE‡**（本战役级别的能垒只能取同批 Gaussian 的 0 虚频鞍点 + 双向 IRC）。只作形状参考：E2 是**晚型、极平顶**的断键步（2.5–3.9 Å 全在峰顶 2.3 kcal/mol 内），与 DFT 侧"过程强吸热（I2 比 I1 高 +11.8 kcal/mol）"一致；工具另报"帧 1→2 能量跳 5.70 kcal/mol，可能有谷滑移"。
**备用初猜已落盘**：E2E3/ts_e2_guess_xtb.xyz｜sha256 **74fa12bc12d95e9d4250c20e9b0ce7dc96ad1f49e021230e80afb3bfeeb42986**（i1 序；= 扫描 point_0006 的**弛豫**几何：C4–O3 2.525｜C4–O5 1.215｜C4–O1 1.297｜O1–H6 0.981｜Na–O3 1.897）；provenance = TS_E2_GUESS_XTB_PROVENANCE.md（sha256 891ceb88e2aece1fb2382414ee7c3ab59e8d89d7c0c806c0d178dba2ffa78220）。**主初猜仍是 ts_e2_guess.xyz**（IDPP frame 3，已被 ts_0013 采用）；本文件是同区域、独立第二来源（xTB 弛豫 vs 刚性插值），供 ts_opt 失败时替换。

### 8.3 E3（I2→P）GFN2/ALPB 反向扫描（job 1003）——提供不了 E3 初猜，但给出 P 构象提示

以 **DFT P 极小值**（p_min_ref.xyz，i2 序）为输入、沿 O3–H6 从 1.05 拉到 2.90 Å。逐帧实测（i2 序 1-based）：

| 帧 | point_0001 | point_0005 | point_0008 | point_0010 | point_0011 | point_0012 |
|---|---|---|---|---|---|---|
| O3–H6 | 1.030 | 1.683 | 2.208 | 2.554 | 2.731 | 2.899 |
| O1–H6 | **5.056** | 5.499 | 5.725 | 5.801 | **0.981** | 0.980 |
| O1···O3 | ~4.0 | — | — | 4.042 | 3.627 | — |
| 相对能/kcal | 0.0 | +62.8 | +97.1 | +108.0 | +29.1 | +29.3 |

读数与含义：
1. **GFN2/ALPB 把该 P 复合物弛豫到另一个构象**：Na⁺ 三配位、甲醇**不再与甲酸根氢键**（点1 起 O1–H6 就 ≈5.06 Å，而 DFT P 极小值是 1.605 Å）。
2. 因而点1–10 里"把 H6 从 O3 拉开"并没有发生质子转移（H6 离 O1 始终 5.0–5.8 Å），能量单调升到 +108 kcal/mol；点11 出现 **78.9 kcal/mol 的跳变**后质子跳到 O1（O1–H6 0.981），落到 +29.1 kcal/mol 的 I2 型区（与 xTB 侧 I2−P ≈ +31.3 kcal/mol 自洽）。
3. ⇒ **该扫描从未采样"质子夹在 O1/O3 之间且 O1···O3 ≈ 2.5–2.8 Å"的几何**，所以**不能**提供 E3 的 TS 初猜；E3 初猜仍只能用 DFT 两端点之间的 IDPP 帧（ts_e3_guess_v2.xyz，O1–H6 1.536 / O3–H6 1.409 / O1···O3 2.808）。
4. **机理提示（须 DFT 复核）**：P 端可能存在多个构象（GFN2 偏好 Na⁺ 三配位、无氢键的那种；DFT 偏好 Na⁺ 双齿 O3/O5 且有甲酸根···H–O 氢键的那种）。本道的 P 端参考极小值（job 994）与 E3 初猜都基于 **DFT** 的 P 构象；ts_0014 的产物质子端身份应以此为准，且**不得**把 GFN2 与 DFT 的能量混减。

