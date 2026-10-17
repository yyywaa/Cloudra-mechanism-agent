# NI5_E1 · IRC 两端点无约束松弛补强（job09 / job10）—— 终态报告

**结论（仅作连接性补强证据）**：从 ts_0006 的两个 IRC 端点几何各自无约束 Opt+Freq，
- REVERSE 侧端点（irc_end_a.xyz）→ **RC-A**（题面接力环极小值，job08 参考几何）；
- FORWARD 侧端点（irc_end_b.xyz）→ **加合物**（job01 参考几何）。
两帧均 Normal termination、优化收敛、**36 个频率、0 虚频**，能量与对应参考极小值一致到 2×10⁻⁷ Eh 以内。
因此**支撑"ts_0006 的 TS 双向分别通往 RC-A 与加合物"**（本批 G16 同程序同批）。

⚠ 证据力度声明：每个 IRC 方向原生只推进 1 点（rx=±0.119 amu^1/2·bohr），
本节证明的是"在 TS 两侧各做一次无约束松弛，落点分别是 RC-A 与加合物"，
即**端点归属的补强**；不等价于一条跑完整收敛的原生 IRC 轨迹。
未触碰 ts_0006（无 ts_resume、无 revision 改动）；本包手工 QM 作业总数 = 2（job09/job10），未提交第 3 个。

## 1 作业与文件（原生日志不改写；能量取自日志原始行）

| 作业 | job_id | 输入 gjf（绝对路径 / sha256） | 原生日志（绝对路径 / sha256） | chk |
|---|---|---|---|---|
| job09_ircend_a | **969** | /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NI5/rc/job09_ircend_a/job09_ircend_a_optfreq.gjf / 46a6f13de5310d00f3bb7ad0a9525ea70fd887a0a36b770b5a99e554dc4ade28 | /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NI5/rc/job09_ircend_a/job09_ircend_a_optfreq.log / **7c90c2188b33ef4981af86bbaa084b4352d5ecf640b9301abb6dd14ddcd3fb75** | /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NI5/rc/job09_ircend_a/job09_ircend_a_optfreq.chk（独立绝对路径） |
| job10_ircend_b | **970** | /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NI5/rc/job10_ircend_b/job10_ircend_b_optfreq.gjf / c3539bc9f39b69bfb139393ac3c5a31dab7ba26147be8dfe7232c6c80fd1f423 | /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NI5/rc/job10_ircend_b/job10_ircend_b_optfreq.log / **a6f5b82b20d33dfdecc178124a9955265014cd533e603eb2680a8d6a4143457d** | /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NI5/rc/job10_ircend_b/job10_ircend_b_optfreq.chk（独立绝对路径） |

路由（与本批一致，未改一字）：`#p opt freq B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=Water)`；
`%nproc=8`、`%mem=10GB`、`0 1`、标题含 `smiles: C=O.CN.O`。提交参数：priority **0**、cpus 8、memory_mb 10240（提交前 query_compute_queue 显示节点 4×8c 满载、free.cpus=0，排队属正常，未调 priority、未重复提交）。

## 2 种子（坐标来自 artifact，经 qm_input_writer 生成输入，未手打）
| 种子 | 绝对路径 | sha256 | r(C1–N6) | IRC 归属 |
|---|---|---|---|---|
| A | /home/ly/Cloudra-mechanism-agent/ts/ts_0006/verdict/irc_end_a.xyz | 7fc97e9459bc52ac56e1d08e33ddda4c6feb6d9d458a6fc1671f5e88ade7af57 | 3.1341 | path=2, rx=−0.11931（REVERSE） |
| B | /home/ly/Cloudra-mechanism-agent/ts/ts_0006/verdict/irc_end_b.xyz | effa287b70c0965c71c4a82f5ff0d878d66b245a69616ca85c58e9c3ac2bc850 | 3.1160 | path=1, rx=+0.11932（FORWARD） |

两输入文件坐标与上述种子逐位一致（qm_input_writer 直接从 xyz 生成）。
与 run 内两个端点 Opt+Freq 的 endpoint_source.json（kind=species_reference、irc_job_id=null）不同，**本次两个作业的起点就是 IRC 端点几何本身**。

## 3 关键原生行号与数值

原生日志结构提示：每个 .log 含两段 g16 运行（第 1 段 = opt，第 2 段 = 在已优化几何上做 freq，两段能量相同）。

| 项目 | job09 (A) | job10 (B) |
|---|---|---|
| 优化末圈 SCF Done | L15121 `E(RB3LYP) = -286.605711921 A.U. after 7 cycles` | L18569 `E(RB3LYP) = -286.613531450 A.U. after 7 cycles` |
| 日志**末条** SCF Done | **L15949** `E(RB3LYP) = -286.605711921 A.U. after 1 cycles` | **L19395** `E(RB3LYP) = -286.613531450 A.U. after 1 cycles` |
| Optimization completed / Stationary point | L15288 / L15289 | L18732 / L18733（freq 段另有一次 L20164） |
| Harmonic frequencies 段 | L16227 | L19673 |
| Frequencies 行 | L16233–L16464（12 行） | L19679–L19910（12 行） |
| 频率个数 / **虚频数** | **36 / 0**（3N−6=36） | **36 / 0** |
| 最低频率 | 35.2126 cm⁻¹ | 98.4345 cm⁻¹ |
| Zero-point correction | L16526 = 0.117753 | L19972 = 0.122743 |
| Normal termination | L15600 (opt 段) 与 **L17075**（末条） | L19046 (opt 段) 与 **L20496**（末条） |
| 末帧几何 Standard orientation | L15797（与优化末帧 L15413 逐位相同：energy 同为 −286.605711921） | L19243 |
| 电荷/重数 | L117 `Charge = 0 Multiplicity = 1` | L117 `Charge = 0 Multiplicity = 1` |

**末帧几何（Å，取自上述 Standard orientation 块）**
```
job09 (A) 末帧                          job10 (B) 末帧
C1  -1.655267 -1.300456  0.088058      C1   0.122791 -1.160419  0.403056
O2  -2.253503 -0.296060 -0.238898      O2  -0.613790 -1.167995 -0.664726
H3  -2.181877 -2.282634  0.140241      H3   1.040881 -1.800221  0.400879
H4  -0.568744 -1.278654  0.341282      H4  -0.379754 -1.283488  1.398367
C5   2.566337 -0.394214 -0.416585      C5   1.668289  0.710614 -0.483008
N6   1.472042 -0.276712  0.540174      N6   0.768084  0.332904  0.618547
H7   2.159342 -0.529335 -1.432325      H7   1.154176  0.452240 -1.417383
H8   3.176247 -1.285800 -0.194610      H8   2.601663  0.136812 -0.407302
H9   3.256952  0.473764 -0.454024      H9   1.889982  1.785551 -0.455965
H10  0.906352  0.552550  0.327828      H10 -0.090765  0.924444  0.594997
H11  1.841988 -0.134357  1.481029      H11  1.218232  0.427860  1.533943
O12 -0.554197  1.941420 -0.090915      O12 -1.835309  1.019840 -0.055748
H13 -1.205244  1.218127 -0.210245      H13 -1.531073  0.114087 -0.405821
H14 -0.694128  2.208463  0.829268      H14 -2.433616  0.796463  0.671964
```

## 4 关键几何量（末帧）
| 量 | job09 (A) 末帧 | job10 (B) 末帧 | RC-A 参考 | 加合物参考 |
|---|---|---|---|---|
| r(C1–N6) | **3.3215** | **1.6410** | 3.3234 | 1.6413 |
| r(C1–O2) | 1.2139 | 1.2972 | — | 1.2968 |
| O2···H13（接力水→羰基氧） | 1.8419 | **1.5976** | — | 1.5975 |
| O12···H10（胺 H→水氧） | 2.0585 | 1.8644 | — | — |
| O12–H13（水内 O–H，仍为共价） | 0.9804 | 1.0176 | — | — |
| N6–H10 / N6–H11 | 1.0116 / 1.0101 | 1.0431 / 1.0245 | — | — |
说明：两侧末帧 N6 均仍带 2 个 H（无 N-质子化），H13 在两侧都仍共价连在 O12 上；B 的 O2···H13=1.598 是显著增强的氢键 —— 与 job01 参考几何完全同构（见 §5）。job01 参考帧在本包题面记作"两性离子加合物"，本报告只核验**几何同一性**，不重新裁定其电子结构标签。

## 5 落点判定：末帧 vs 4 个参考几何逐原子 maxdev（Å，14 原子，同原子序号一一对应）

| 参考几何（绝对路径 / sha 前缀 / 能量 Eh） | A 末帧 raw maxdev | A 末帧 Kabsch 对齐 maxdev | B 末帧 raw maxdev | B 末帧 Kabsch 对齐 maxdev |
|---|---|---|---|---|
| **RC-A** job08_well_3496_optfreq_last.xyz / 413752ab… / −286.605711743 | **0.0040**（原子 11） | 0.0031 | 3.2689 | 1.9355 |
| **加合物** rc_optfreq_m13_last.xyz / 11474dff… / −286.613531375 | 3.2678 | 1.9355 | **0.0025**（原子 9） | 0.0011 |
| RC-B job03_cand000_optfreq_last.xyz / c5f279ed… / −286.610034975 | 6.0898 | 2.2328 | 5.5367 | 2.3200 |
| RC-C job06_cand005_optfreq_last.xyz / 2a368b45… / −286.608664920 | 4.8412 | 2.6595 | 4.8406 | 2.8249 |

参考几何绝对路径：
- RC-A：/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NI5/rc/job08_well_3496/job08_well_3496_optfreq_last.xyz
- 加合物：/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NI5/rc/job01_rc_optfreq/rc_optfreq_m13_last.xyz
- RC-B：/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NI5/rc/job03_cand000/job03_cand000_optfreq_last.xyz
- RC-C：/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NI5/rc/job06_cand005/job06_cand005_optfreq_last.xyz

**判定**
- **job09（irc_end_a / REVERSE）→ 落到 RC-A**：raw maxdev 0.0040 Å，能量差 −1.78×10⁻⁷ Eh（−0.00011 kcal/mol），且 36 模 0 虚频 ⇒ 与 job08 的 RC-A 是**同一极小值**。
- **job10（irc_end_b / FORWARD）→ 落到加合物**：raw maxdev 0.0025 Å，能量差 −7.5×10⁻⁸ Eh（−0.00005 kcal/mol），36 模 0 虚频 ⇒ 与 job01 的加合物是**同一极小值**。
- 两者与 RC-B（≥5.5 Å raw）、RC-C（≥4.8 Å raw）差一个量级以上，判定为"其它浅凹/RC-B/RC-C"不成立。

## 6 对验收链（BRIEF §4 第 2/3 条）的意义
- §4.2（IRC 双向真实到达声明的两个端点）：原生 IRC 每向只推进 1 点即早停，本补强给出**端点归属的无约束验证** —— 两侧各自松弛后分别落到 RC-A 与加合物两个 0 虚频极小值，方向上不自相矛盾。**但没有跑出完整收敛的 IRC 轨迹**，因此"双向区间证据"仍以 rx=±0.119 的单点区间为限，属补强而非替代。
- §4.3（两端点 Opt+Freq）：本作业的两帧即为**从 IRC 端点几何出发**的 0 虚频极小值，身份经几何同一性核验（RC-A / 加合物）；早前 run 内 endpoint_source.json 标 kind=species_reference 的两帧不承担这一角色。
- 观察（供协调裁决，不作本报告结论）：TS 两侧落点差别主要体现在 r(C1–N6)（3.32 vs 1.64，Δ=1.68 Å），即路径确实沿 C–N 成键方向分开；同时 O2···H13 由 1.842 → 1.598、O12···H10 由 2.059 → 1.864（接力氢键在两侧都已存在，只是 B 侧更强）。这与本包此前"TS 虚频模以 H 位移为主（watch pair 占比 1.6%）"的记录并列，供 pseudo-saddle 判定参考 —— 本作业不改变该判定。

## 7 未做/边界
- 未提交第 3 个作业；未触碰 ts_0006（无 ts_resume / 无 revision）；未改任何原生日志或输入；未提交 git；未改平台代码/数据库。
- 本报告只写本文件：/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NI5/notes/IRC_ENDPOINT_RELAX.md。
