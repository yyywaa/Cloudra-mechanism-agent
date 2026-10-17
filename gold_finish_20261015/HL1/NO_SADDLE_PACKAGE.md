# HL1_E1 收口材料包（NO_SADDLE_PACKAGE）· v1 草稿

> **状态（先读这段）**：本文件是 HL1_E1（气相 q+1/m1，H3O+ 对 (E)-butan-2-one oxime 的 O-质子化）的收口材料汇总，**v1 = 2026-10-15 23:5x**。
> **已完整**：已落盘原生日志的逐项核验（§2–§5）、已知极小值身份（§3）、剖面清单与解释力边界（§4）、搜索充分性（§5）、证据清单（§9）。
> **待补（②③）**：E2_RC42A（4.20 Å 种子）结果、N_side_optfreq（N 侧驻点身份）、ts_prepare 的 run_id/process.json/result.outcome 原文（§6）。截至本行三者均因平台写锁复发（#176 复现，24 核中约 16 核被卡死行空占）尚未产出。
> **未决定**：§7 的三选一（记 0.0+caveat ／ 豁免 ／ 改图）**尚未作出**；裁决前未写值、未改 jl.py、未改图。

## 1 声明的边与参考态口径
- 边：HL1_E1；题面 = `[OH3+].CC/C(=N/O)/C >> CCNC(C)=[OH+].O`（+1/1，浓 H2SO4/酸催化加热）。
- registry：`cloudra/benchmark/hard_registry/jl.py` 的 `L1` 第 1 步（O-质子化肟 OH，`type = proton transfer from H3O+ to the oxime OH (leaving-group activation)`），**当前无 `barrier` 键**（缺测）。该步 `out` = `[O:1]([H:9])[H:10].[CH3:11][CH2:5]/[C:4](=[N:6]/[O+:7]([H:8])[H:2])/[CH3:3]`（水 + O-质子化肟）。
- 题面 prompt 逐字要求：网络从**反应络合物（pre-reaction complex）**起，不从分离反应物起；ΔE‡ 为**纯电子能**（无 ZPE/热校正），相对该步自身起点的极小值。
- 方法（本批统一）：Gaussian 16（`/home/ly/g16/g16`）B3LYP/def2SVP + `EmpiricalDispersion=GD3BJ` + `Int(UltraFine)` + `SCF=Tight`，**气相（无 SCRF）**，q=+1/m=1。引擎偏差：题源既定口径为 ORCA 6.1.1，本机无 ORCA ⇒ 程序不同、泛函/基组/色散/溶剂模型同级；**本包所有能量只在本批 Gaussian 日志内相减**（627.509474 kcal/mol per Ha）。

## 2 起点（声明 RC = 质子留 O1）的证伪证据
四个独立种子做**未约束** Opt+Freq，全部滑落到质子已在肟 O（O7/O9）的络合物（判据 R(1,2) ≈ 1.38 Å 且 R(2,9) ≈ 1.08 Å ⇒ 产物侧；「停住」判据是 R(1,2) ≤ ~1.05 且 R(2,9) ≥ ~1.4）：

| 种子 | d(O1···O7) 起点 | job | 原生日志（前缀 `gold_finish_20261015/HL1/ts_run/jobs/`）+ sha256 | E / Ha | 模数/虚频 | 末帧 R(1,2)/R(2,9)/R(1,9) Å | 判定 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 单齿 A | 2.60 Å | 904 | A_RC_optfreq.log dd2736788cb8e0fc01914efbf02c91c40408d97bb17e456c354d2a8a621c781e | -364.295965289 | 51 / 0 | 1.3812 / 1.0774 / 2.4569 | **坍缩** |
| 产物侧（对照） | 2.60 Å | 905 | A_PC_optfreq.log f62601ab694362f90183e282e15c9a00bf91826143f4787b3135bd67cc0b5040 | -364.295965287 | 51 / 0 | 1.3810 / 1.0774 / 2.4568 | 同一驻点 B |
| 单齿 A | 3.00 Å | 920 | C2_RC3A_optfreq.log 01c7b36f48170832a44652217c1796242969fd95befe3137413e08650f11c559 | -364.295965302 | 51 / 0 | 1.3810 / 1.0774 / 2.4568 | **坍缩**（38 帧：帧1→18 单向 0.9877→1.3834，帧18→38 小振幅收敛） |
| 单齿 A | 3.50 Å | 966 | E2_RC35A_optfreq.log 48da3dcb0ca8e2bce3e9e3d67a15bf7d46bb6abcc963b0296b1499776302a384 | -364.295777129 | 51 / 0 | 1.3878 / 1.0740 / 2.4601 | **坍缩**（比 B 高 0.118 kcal/mol 的同质子化态构象） |
| 双齿螯合 | 2.61 Å | 965 | E2_RCbi_optfreq.log a4d182472ff195ac8c1e6bbc3a2c5a57e8daa67b29a45fee470c4a235d6e0dcf | -364.295965301 | 51 / 0 | 1.3811 / 1.0774 / 2.4568 | **坍缩到 B** |

- 输入 sha256：A_RC_optfreq.gjf 339108576666454a6eadaa583aff77ee1a66a1db480920756ed61dce06c142ac｜A_PC_optfreq.gjf 239bad2a8832713ba86c9d609294ffd46a564b56f854e20fa8d72ba8a3f1ee77｜C2_RC3A_optfreq.gjf（见 STATUS §4）｜E2_RC35A_optfreq.gjf 5748a44528e2a8680c31196100c3eab4bf298a7fda2a5c473ea190f80832cd17｜E2_RCbi_optfreq.gjf 6ab9b94e67c7f9c18b020149f1a86ab74965e506617f5da04b62eabc013b7670。
- 末帧几何文件：round3/E2_RCbi_final.xyz cb1559ea…、round3/E2_RC35A_final.xyz e2fc5c07…（坐标为日志原值，未改）。

## 3 已确立的极小值（身份核验）
**B = H2O + O-质子化肟 强氢键络合物**（不是声明的 RC）：
- 身份：H2 在 O7 上（R(2,9)=1.0774 Å）、O7 另带 H8（R(9,16)=0.9779 Å）、O1 带 H3/H4（0.970 Å 级）而 H2 与 O1 仅剩强氢键（R(1,2)=1.381 Å）、O1···O7 = 2.457 Å、R(8,9) = 1.554 Å（N–O 单键）。
- 三份独立作业同一驻点：ΔE ≤ 1.3×10⁻⁸ Ha；末帧逐原子最大偏差 ≤ 0.0031 Å；各 51 模、**0 虚频**（最低实频 27.1816 / 27.1707 / 27.1292 cm⁻¹；Low-frequencies 首值 ≈ -4.9 cm⁻¹ 为投影平动/转动残值，不计虚频）。
- 独立复核：explorer（round3/EXPLORER_R3_INDEPENDENT_VERIFY.md sha256 2bf40d42…）与主协调各一次。
**仍缺**：N 侧（N-质子化肟 + 水）驻点身份 —— 候选帧 E = -364.301672236 Ha 出自**约束且未收敛**的扫描帧，只能读作上界（§4）。

## 4 剖面清单：各自能说什么、不能说什么
| 剖面 | job | 结果 | 能否支持「无鞍点」 |
| --- | --- | --- | --- |
| 松弛扫 d(O1···O9) 2.457→3.457（外向） | 912 | 10 点收敛，逐点单调上坡 0→+6.42 kcal/mol；pt11 NStep=88 耗尽 → l9999 | **不能**：pt1 几何就是 B 本身（L1877 R(1,2)=1.3812、L1881 R(2,9)=1.0774），质子全程在 O9 ⇒ 这是 **B 的解离曲线**，不是声明步的反应坐标 |
| 冻结 O···O=3.00 扫 d(O1–H2) | 913 | scan point 1 第 12 步 `Error imposing constraints` → l103；**0 个收敛点** | **不能**（输入构造失败；与 921 机制不同：无 FormBX/Tors 报错） |
| 松弛扫 d(O1–H2) 0.988→2.088 | 921 | scan point 1 第 20 步 `Tors failed for dihedral 3-1-9-16 / 4-1-9-16` + `FormBX had a problem.` → l103；**0 个收敛点** | **不能**（Berny 冗余坐标系崩坏）；附带观察：H3 连续移向 N8（末块 R(1,3)=1.2123 / R(3,8)=1.2111 桥式） |
| 松弛扫 d(O1···O9) 4.200→2.400（内向） | 930 | scan point 1 走满 88 步 → l9999；**0 个收敛点**；能量在 -364.2616/-364.2623 Ha 往复（≈0.45 kcal/mol），O···O 几乎未动（4.200 Å）、质子仍在 O1 | **不能**（长程端平坦区未收敛） |

- 结论：四个剖面都**不具备最低条件**（扫描点全收敛 + 覆盖声明步两端）⇒ 均不得作为「无鞍点」证据，只作重设计输入（与 explorer 独立复核结论一致）。
- 关于 N 侧的既有数字（-364.301672236 Ha，「比 B 低 3.58 kcal/mol」/「2.0 kcal/mol」）：**降级为上界**，因为该帧是约束扫描中的未收敛帧，不是驻点，驻点间能量差无效。

## 5 搜索充分性（逐项留证）
**已试**：① O1–H2 单坐标松弛扫（921，l103 崩坏）；② O1···O9 外向松弛扫 2.46→3.46（912，10 点后 NStep 耗尽）；③ O1···O9 内向松弛扫 4.20→2.40（930，第 1 点耗尽）；④ 扫 O1–H2 + 冻结 O1···O9（913，l103 约束构建失败）；⑤ A 族未约束 Opt+Freq 4 个种子（2.60 / 3.00 / 3.50 Å + 双齿螯合）全部坍缩；⑥ 质子居中 IDPP 内插 guess 已备（t4_interp/img_06.xyz，r(O1–H2)=1.280 / r(H2–O7)=1.306 Å）等 ts_prepare。
**未试/待补**：⑦ 4.20 Å 种子未约束 Opt+Freq（E2_RC42A，已备未跑）；⑧ N 侧未约束 Opt+Freq（N_side_optfreq，已备未跑）；⑨ ts_prepare 的 OptTS/IRC（未跑）；⑩ 二维网格 / xTB 二维面图（未做，理由：单坐标与种子递推已给出坍缩结论，缺的是长程通道与 N 侧身份）。

## 6 ts_prepare 原文（**待补**）
- run_id：—；run_dir：—；revision/status/stage：—；result.outcome：—（`process.json` 路径与 sha256 待补）。
- 已备输入：guess = `ts_run/t4_interp/img_06.xyz`（sha256 99749b1630e3e654e1523df8cc9726134bfe58b42d59a948082dd1563110fe2d），evidence_refs 含 `ts_run/prep/TS1_guess_provenance.md`（sha256 6aaf09e1d5891346ecd0607fa383b23f6dee5b1dcd31afb5e8667ccbc0cde5c2）等真实文件；声明用 registry 原文：reactant `[O+:1]([H:2])([H:9])[H:10].[CH3:11][CH2:5]/[C:4](=[N:6]/[O:7][H:8])/[CH3:3]`、product `[O:1]([H:9])[H:10].[CH3:11][CH2:5]/[C:4](=[N:6]/[O+:7]([H:8])[H:2])/[CH3:3]`、reaction_center [[1,2],[2,9]]；平台具体原子序与 atom_map 见 `round3/T4_INPUT_ORDER_PROVENANCE.md`（sha256 a97f0467a46bbcade4e900135be57aa32f2d9269e77e951bd3e8adc57aed3d24）。

## 7 裁定/决定（**未作出**；按 BRIEF §9 由本包 Coordinator 依证据决定）
- 选项 A：本步记 **0.0 + caveat**（无独立鞍点 / 无垒离子-分子质子转移；库内先例 normal_registry/yo.py 的 O3 第 1 步 = 0.0）。需要的最低证据：声明的 RC 非驻点（**已有**：4 种子坍缩）+ 沿反应坐标无内部极大（**缺**：需一条覆盖两端且点全收敛的剖面）+ ts_prepare 无峰记录（**缺**）。
- 选项 B：申请该边豁免（无独立鞍点，交证据 + 替代口径）。
- 选项 C：改图（例如把「O-质子化」与该步的参考态重定义，或显式引入 N-质子化竞争通道作为独立节点/边）。判据：N 侧驻点若 0 虚频且能量更低 ⇒ N-质子化是更有利通道；但 N-质子化肟**不是** Beckmann 的离去基团活化态（不导向腈鎓离子），故即便成立，也只是**竞争/非生产性通道**，不替代 O 侧步骤。
- 影响面（无论选哪一个）：jl.py 的 `L1` 第 1 步 barrier（新增或保持 null）、`ideapool/tasks/hard/HL1.json` 重新生成、`ideapool/reaction_candidates/hard.md` 第 145 行（L1 行）文字、以及 mechanism_graph 中 RC/TS1 节点的身份说明。

## 8 替代口径（供交付的「证据驱动机理修订」一节）
1. 「RC（质子留 O1）」在本级别气相不是驻点 ⇒ 参考态若坚持用 RC，则其极小值不存在；替代口径 = 以**离子-分子对/产物侧极小值 B** 为参照，本步只报「无独立鞍点」。
2. 若最终确认无峰：本步 ΔE‡ 只能以 **0.0 + caveat** 登记（或豁免），**不得**用 912 的峰、约束扫描或未收敛帧的任何数字充数。
3. 与历史 gold 的关系：本边现行无参考值（`barrier` 缺键），不存在「替换旧值」问题；旧 Gaussian/WSL 的 0 已作废、不回填（HISTORY.md）。

## 9 证据清单（路径 + sha256 指位）
- 本包 STATUS.md（总台账）：`gold_finish_20261015/HL1/STATUS.md`（sha256 见历次编辑记录；现行 §11–§14 为本轮接手后的记录）。
- 独立复核：`gold_finish_20261015/HL1/round3/EXPLORER_R3_INDEPENDENT_VERIFY.md` 2bf40d42…；更早 `HL1/AUDIT.md` fc01bf50…、`AUDIT_B2.md` 2314240f…、`AUDIT_B3.md`（见文件）。
- 原生日志：见 §2 表（904/905/920/965/966）与 §4 表（912/913/921/930），全部未改写。
- 输入与 provenance：`ts_run/NOTES.md`、`ts_run/T3_SCAN_DESIGN.md`、`ts_run/prep/TS1_guess_provenance.md`、`round3/T4_INPUT_ORDER_PROVENANCE.md`、`ts_run/prep/N_side_frame_provenance.md`。
- 平台侧：`ts_run/jobs/.cloudra/guard-965.log`、`guard-966.log`（`更新数据库失败：database is locked`）＋主协调帖 evt_77cfc31850924fd6（#176 复发）。
