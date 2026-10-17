# ts_0011 身份取证报告（只读 · 零提交）

**范围**：`ts/ts_0011`（revision 51 / declaration_revision 4 / stage=verdict / terminal=candidate_only / result.verified=false），
job 999 (ts_opt) · 1029 (freq) · 1033 (IRC) · 1035 (reactant_opt) · 1038 (reactant_freq) · 1041 (product_opt) · 1043 (product_freq)，
外加两个同一步的已 freq 验证参考点：job 1061 (P) 与 job 961 (I2)。
**纪律**：本次**零新提交**（未 ts_prepare / ts_resume / submit_compute_job / kill / 调 priority），未改 `ts/` 下任何文件，
未改 `gold_finish_20261015/HI1/` 下任何既有文件；只新建本报告与 `E3/forensic/scripts/` 下 5 个只读分析脚本。
所有数字均在本轮从原生日志/文件重测，每项给 `文件 + 行号 + sha256`。
**三档标注**：`【观察】` 直接读数；`【推断】` 由观察推出、未被独立测量直接确认；`【未能判定】` 现有证据不足。
**能量口径**：本 run 无 verified TS，全文不出现 ΔE‡；所有差值都是相对 **I2 极小（job 961，E = −939.320655479 Eh）** 的纯电子能差 ΔE。

---

## 0 一句话结论（先给判定，再给证据）

> **B1 与 B2 都不成立。** 装配出来的产物种子 `build/input_0004/product/seed.{xyz,mol}` 的化学连接性**就是**声明的产物
> （InChIKey `SMPZMOQIWMNUBG-YBVIJTQESA-N`，与声明串、与实测 P 三者完全一致）⇒ **B1（装配错）被排除**；
> 而 `product_opt`(1041) **根本没有从这颗种子出发**，它的输入是 IRC 外帧（`endpoint_source.json` kind=`irc_outer_frame`，
> 该帧 InChIKey = 反应物 `FYDMZWJHNXGWEQ-BWNURDBISA-N`）⇒ **B2（种子构象塌回）也未被执行到，不能作为解释**。
> 真正的断点在两处：**(i) ts_opt(999) 把 guess 里 C2–O25 = 1.900 Å 的入射键“丢掉”了（收敛到 3.138 Å），“TS”落回 I2 盆地，
> 唯一虚模 99.2% 是 C3 甲基转动；(ii) 两个端点槽都用 IRC 外帧当种子而非声明 seed，于是必然双双回到 I2。**
> 平台 verdict 的 “product built MOL does not match its declared SMILES” 因此**不是化学不符**，而是**索引/映射层**（atom_map 与 0-based reaction_center）的问题 `【推断】`。
> **推论：ts_0011 的失败不构成“E3 单步协同不可达”的证据，也完全没有区分一步 vs 两步。**

---

## 1 取证对象与哈希（本轮实测）

### 1.1 结构 / 声明
| 用途 | 路径（项目相对） | sha256 |
|---|---|---|
| 运行状态 | `ts/ts_0011/process.json` | `d17a5712b90f1b4db2a6a1e2139c765b375592d200a37c295e0275a40e459333` |
| 声明原文 | `ts/ts_0011/declare.json` | `b5b883bd09fb0b173fc4d561a5218d3920f6aa04c966e37f0eb7b0eeac8b23ef` |
| 反应物 build（xyz） | `ts/ts_0011/build/input_0004/reactant/seed.xyz` | `9a6203ff67d9f0d95ad774e78b17bc397b22992f24cbcdf448f8c5558142ef2b` |
| 反应物 build（mol） | `ts/ts_0011/build/input_0004/reactant/seed.mol` | `c8911a212490c6c594aa3659f13bb44616002b539bcd2b9d4b0590880ff2c670` |
| **产物 build（xyz）** | `ts/ts_0011/build/input_0004/product/seed.xyz` | `06161a1411edf1e1402620ee13ca448c14d2ac167846c10f1e56bf8ec175078a` |
| **产物 build（mol）** | `ts/ts_0011/build/input_0004/product/seed.mol` | `2d84490ae0f9aed220b715338f845c45fc6f899cc11f47f5f758d2df2db4f034` |
| 声明产物装配源（mol，同 sha） | `gold_finish_20261015/HI1/E3/prep/structure_build_P/assembly/complex_candidate_000.mol` | `2d84490ae0f9aed220b715338f845c45fc6f899cc11f47f5f758d2df2db4f034` |
| TS guess | `gold_finish_20261015/HI1/E3/prep/guess_c2o25_190/ts_guess_c2o25_190.xyz` | `2568ca035c3ee37dc9472cd86bd3a751547ba835f99332cf8ce2ac91177bb186` |
| **product_opt 实际输入** | `ts/ts_0011/jobs/declaration_0004/product_opt/product_source.xyz` | `331d65c24bc30a9ffd3dee362448ee90d9482efa9718d5dcd657e8d4f74d27d8` |
| reactant_opt 实际输入 | `ts/ts_0011/jobs/declaration_0004/reactant_opt/reactant_source.xyz` | `62c944bc6ddbf1841f1816546967ce13bd1b39055297b185cd690d9700a28c54` |
| P（job 1061）收敛帧 | `gold_finish_20261015/HI1/E3/prep/P_1061_optframe.xyz` | `957b95970f05a052d882094d5434027594498cbe6d733590180a2c3003006f9a` |
| I2 极小帧 | `gold_finish_20261015/HI1/E3/runs/I2_optfreq/I2_min_v5.xyz` | `9a6203ff67d9f0d95ad774e78b17bc397b22992f24cbcdf448f8c5558142ef2b`（= 反应物 seed，逐字节相同） |

### 1.2 原生日志
| job | 路径（项目相对） | sha256 | 行数 |
|---|---|---|---|
| 999 ts_opt | `ts/ts_0011/jobs/declaration_0004/ts_opt/refine.log` | `a8f56a49dcec0404da9d23071ad444e6a59641852f2657d2d0903fc3e70b4177` | 125 662 |
| 1029 freq | `ts/ts_0011/jobs/declaration_0004/frequency/frequency.log` | `8366cbc6ec3d40d66bfb001cee746ac39f9fdc86896098d088e82e4d3cc133af` | 5 302 |
| 1033 IRC | `ts/ts_0011/jobs/declaration_0004/irc/irc.log` | `17da5ef2a63e7af2a4a1e232ef06d9b8ceb3e488504e0f9bad569a87dc071edb` | 3 672 |
| 1035 reactant_opt | `ts/ts_0011/jobs/declaration_0004/reactant_opt/reactant_opt.log` | `5c64c8b8e1c37ed23e15208a9adbdee7bea1581e11ed844e503cb4702718a585` | 22 902 |
| 1038 reactant_freq | `ts/ts_0011/jobs/declaration_0004/reactant_frequency/reactant_frequency.log` | `139a17b917f196387276142a4c3ae5a88b9cc0433eff114373914509b798ad0d` | 5 297 |
| 1041 product_opt | `ts/ts_0011/jobs/declaration_0004/product_opt/product_opt.log` | `b91175b78786e00d30a7c6ce309ce3908b64be99fa8d51d07f152556e8f25b7e` | 35 617 |
| 1043 product_freq | `ts/ts_0011/jobs/declaration_0004/product_frequency/product_frequency.log` | `b5f62db2d4f2630b7c51cec44f01bb5e21b41ac74f2ccf45574199266f5f046f` | 5 301 |
| **1061 P** | `gold_finish_20261015/HI1/E3/runs/P_e3b/P_optfreq.log` | `183590c1ff28965769ebab84704e50f0ffbf0f9d63320bd9e0a4d0ec36aea15a` | 73 964 |
| 961 I2 | `gold_finish_20261015/HI1/E3/runs/I2_optfreq/I2_optfreq.log` | `63dda25e04529e65920526304fb88755db9393e9c22bd3a6efb76eeee0af0d0e` | 24 001 |

> 路径校正：任务书写的 `E3/runs/P_optfreq/P_optfreq.log` **不存在**；P 的实际路径是
> `E3/runs/P_e3b/P_optfreq.log`（同一 job 1061；`E3/runs/P_e3b/state_1061.json` 亦在该目录）。

---

## 2 三套原子编号体制（不先对齐，下面的表会全部读错）

| 体制 | 数量 | 特征 | 谁用 |
|---|---|---|---|
| **W｜canonical 工作序**（1-based work index，本报告默认） | 41 | 元素串 `CCCNCCCCCOOHHHHHHHHHHHHHOHHOCCCCCCCHHHHHH` | ts_opt / freq / IRC / 两个端点 opt / P(1061) / I2 seed —— 全部原生日志的 orientation 块都按这个序（脚本逐帧断言 True） |
| **S｜产物种子序** | 41 | 元素串 `CCOCCOCCCCCCHHHHHHHHHHHHOCOCCCCNHHHHHHHHH`（按 product_smiles 的 20 个重原子顺序，每个片段的 H 紧跟其后） | 只有 `build/input_0004/product/seed.xyz` / `.mol`（与装配源 `complex_candidate_000.{xyz,mol}` 逐字节相同） |
| **M｜题源 product_smiles 的 atom_map 标签** | 1–22 | `[CH3:1][C:2](=[O:4])[CH2:3]…[N:20]1([H:21])`；`[O:5][H:22]` | 声明串本身；`structures.product.smiles_heavy_atoms`（label 1–20） |

**W ↔ S 的化学对应**（本轮实测，由 RDKit 全 41 原子 chirality-aware 子结构匹配得到，脚本 `b_logs.py` §8）：

S1→W3, S2→W2, S3→W25, S4→W1, S5→W29, S6→W28, S7..S12→W30..W35, S13→W14, S14→W15, S15→W16, S16→W12, S17→W13, S18→W36, S19→W24, S20→W37, S21→W38, S22→W39, S23→W40, S24→W41, S25→W11, S26→W9, S27→W10, S28→W8, S29→W7, S30→W6, S31→W5, S32→W4, S33→W27, S34→W23, S35→W21, S36→W22, S37→W19, S38→W20, S39→W17, S40→W18, S41→W26

**化学标签（本报告统一用）**：
W2 / map2 / 亚胺碳（= 产物酮羰基 C） · W4 / map1 / 环亚胺 N（= 产物二级胺 N） · W25 / map10 / 水 O（= 产物酮羰基 O） ·
W26 / map9 / 水 H（→ 产物 N–H） · W27 / map11 / 水 H（→ 产物羧酸 O–H） · W10 / map33 / 羧基 O（−O⁻ → COOH 的 OH） ·
W11 / map34 / 羧基 O（=O 保留） · W3 / map25 / 甲基 C · H14,H15,H16 / 甲基三 H · W29 / map5 / 苄位 CH · W28 / map8 / 醇 O。

> map 值取 `process.json input_binding.atom_map`（41 元，1-based；等于 `declare.json` 的 0-based 表逐项 +1，脚本 `a_identity.py` 断言为 True）。
> **但这套 map 值本身不自洽**，见 §7.5 —— 不要拿它当“化学对应”用。

---

## 3 问题 1：身份四方对照（declared / built MOL / optimized endpoint / 实测 P）

方法：每个几何都从**坐标**出发做 RDKit `DetermineBonds(charge=0)` 键感知（不手写任何键），再取剔除 H 的规范异构 SMILES 与 InChIKey；
SMILES / MOL 文件走 `MolFromSmiles` / `MolFromMolFile`。脚本 `a_identity.py`、`b_logs.py` §6。

| 对象 | 来源 | 规范异构 SMILES（去 H） | **InChIKey** |
|---|---|---|---|
| ① 声明 product_smiles | `process.json` input.reaction | `CC(=O)C[C@H](O)c1ccccc1.O=C(O)[C`H]1CCCN1` | **`SMPZMOQIWMNUBG-YBVIJTQESA-N`** |
| ② build 产物 MOL | `build/input_0004/product/seed.mol` | `CC(=O)C[C@H](O)c1ccccc1.O=C(O)[C`H]1CCCN1` | **`SMPZMOQIWMNUBG-YBVIJTQESA-N`** |
| ②' build 产物 xyz（键感知） | `build/input_0004/product/seed.xyz` | 同上 | **`SMPZMOQIWMNUBG-YBVIJTQESA-N`** |
| ③ `product_opt`(1041) 收敛几何 | `product_opt.log` 末帧（hdr L35019，原子 L35024–L35064，第 76/76 帧） | `C/C(C[C@H](O)c1ccccc1)=[N+]1\CCC[C@H]1C(=O)[O-].O` | **`FYDMZWJHNXGWEQ-BWNURDBISA-N`**（= 反应物） |
| ④ 实测 P | `P_optfreq.log` 末帧（hdr L68977，原子 L68982–L69022，第 146/146 帧） | `CC(=O)C[C@H](O)c1ccccc1.O=C(O)[C`H]1CCCN1` | **`SMPZMOQIWMNUBG-YBVIJTQESA-N`** |

分片段 InChIKey（声明产物）：酮片段 `MUVVFSVVVHYLMQ-JTQLQIEISA-N`，脯氨酸片段 `ONIBWKKTOPOVIA-BYPYZUCNSA-N`；
声明反应物：主体 `CHSQVVZMPUSMNG-LJLNYXAJSA-N`，水 `XLYOFNOQVPJJNP-UHFFFAOYSA-N`。

### 3.1 结论与**逐原子差异**（这是“哪个原子”的答案）

- **① = ② = ②' = ④（四方完全一致，含立体化学层）** ⇒ 构建/装配产物这一步在化学上是**对的**。`【观察】`
- **③（被当作“产物端点”的那个几何）不是产物，而是反应物 I2**。它与 ①/②/④ 的差异不是“某个 H 挪了一点”，而是整整三件事：

| 差异项 | I2 / ③（= `product_opt` 收敛帧） | P / ① / ② | 判据 |
|---|---|---|---|
| **(a) 亚胺双键** | `C2=N4` **1.299 Å**（双键；N4 三配位、形式电荷 **+1**） | `C2···N4` **3.331 Å**（无键，N4 变成带 H 的二级胺，电荷 0） | 两帧键表；形式电荷（RDKit：I2 只有 N4 +1 / O11 −1，P 全 0） |
| **(b) 羰基** | `C2–O25` **3.160 Å**（O25 是**水**氧，`O25–H26 0.966`、`O25–H27 0.990`） | `C2=O25` **1.217 Å**（O25 变成**酮羰基**氧，且 O25 上**没有 H**） | 键表：P 中 O25 度 = 1 |
| **(c) 质子归属** | `H26` 在 **O25（水）**上；`H27` 也在 **O25** 上；羧基 `C9–O10 1.254 / C9–O11 1.250`（**羧酸根**，O10 无 H） | `H26` 在 **N4** 上（`N4–H26 1.020`）；`H27` 在 **O10** 上（`O10–H27 1.011`）⇒ 羧基变成 `C9–O10 1.328 / C9=O11 1.211`（**COOH**） | H 归属表 + 两个 C–O |

一句话：**反应物 vs 产物不是“某个 H 挪了一点”，而是“水 O 变成酮 O、水的一个 H 落到 N 上、另一个 H 落到羧酸根 O 上、C=N 断开”。**
③ 这一整套都没发生（`C2=N4 1.299`、`C2–O25 3.160`、`N4–H26 4.007`、`O10–H27 1.717`）。

### 3.2 键长化学合理性断言（凡报出的键长先过一遍）

| 键（W 序） | 实测 | 期望区间 | 判定 |
|---|---|---|---|
| I2 `C2=N4` | 1.299 | 亚胺 C=N 1.27–1.31 | PASS |
| I2 `C9–O10 / C9–O11` | 1.254 / 1.250 | 羧酸根共振 1.24–1.27 | PASS（须按 COO⁻ 理解，不能按单一 C–O 1.42 / C=O 1.21 判） |
| I2 `O25–H26 / O25–H27` | 0.966 / 0.990 | O–H 0.95–1.00 | PASS |
| I2 `C28–O29` | 1.403 | C–O 单键 1.40–1.45 | PASS |
| P `C2=O25` | 1.217 | C=O 1.20–1.23 | PASS |
| P `C9–O10 / C9=O11` | 1.328 / 1.211 | 羧酸 1.32–1.36 / 1.20–1.22 | PASS |
| P `N4–H26` | 1.020 | N–H 1.00–1.03 | PASS |
| P `O10–H27` | 1.011 | O–H 0.96–1.01 | PASS |
| 产物 seed（S→W）`C2=O25` | 1.2356 | C=O 1.20–1.24 | PASS |
| 产物 seed `N4–H26` | 1.0259 | N–H 1.00–1.03 | PASS |
| 产物 seed `C2···N4`（非键距离） | 5.6280 | 不适用（断键后两片段分开） | 记作“无键” |

---

## 4 问题 2：反应物侧同样对照

| 对象 | 来源 | InChIKey |
|---|---|---|
| 声明 reactant_smiles | `process.json` | **`FYDMZWJHNXGWEQ-BWNURDBISA-N`** |
| build 反应物 seed.mol | `build/input_0004/reactant/seed.mol` | **`FYDMZWJHNXGWEQ-BWNURDBISA-N`** |
| build 反应物 seed.xyz（键感知） | `build/input_0004/reactant/seed.xyz` | **`FYDMZWJHNXGWEQ-BWNURDBISA-N`** |
| `reactant_opt`(1035) 收敛几何 | `reactant_opt.log` 末帧（hdr L22302，原子 L22307–L22347，48/48） | **`FYDMZWJHNXGWEQ-BWNURDBISA-N`** |
| I2 极小（job 961） | `I2_min_v5.xyz` | **`FYDMZWJHNXGWEQ-BWNURDBISA-N`** |

- 反应物侧**四方一致**：声明 = build = 端点 opt = I2 极小。`【观察】`
- `reactant_opt`(1035) 相对 I2 极小几何 RMSD = **0.0011 Å**（最大单原子偏差 0.003 Å）、ΔE = **+9.3×10⁻⁸ Eh**。`【观察】`
- **IRC 两个外侧帧确实是同一物种、也确实都是反应物**，而且这次不是“误读”：

| 帧 | 相对 TS 末帧 RMSD | 相对 I2 极小 RMSD | InChIKey | 关键键长 |
|---|---|---|---|---|
| IRC 初点（点 0） | 0.0000 Å | 0.2259 Å | FYDMZ… | `C2=N4 1.299 / C2–O25 3.138` |
| 正向 点 1（hdr L1494，原子 L1499） | **0.0082 Å** | 0.2185 Å | FYDMZ… | `1.299 / 3.140` |
| 反向 点 1（hdr L2175，原子 L2180） | **0.0082 Å** | 0.2334 Å | FYDMZ… | `1.299 / 3.137` |

> 两外侧帧互差 0.0165 Å、相对 TS 只差 0.0082 Å ⇒ 它们是“几乎没动”的 TS 副本。
> **所以“两帧 SMILES 相同”是 IRC 只有 2 点的必然结果，不能作为“两侧落到同一物种”的连通性证据**（与 `HI1/PROCESS.md` §2 观测 3 一致）。

---

## 5 问题 3：`ts_opt`(999) 与 `frequency`(1029)

### 5.1 收敛到驻点了吗？——是，但“驻点”不等于“声明的 TS”

| 项 | 值 | 位置 / 证据 |
|---|---|---|
| `-- Stationary point found.` | 有 | `refine.log` **L124575**（Max F 0.000083 / RMS F 0.000011 / Max D 0.001757 / RMS D 0.000279，均 < 阈值） |
| 末次 SCF Done | **−939.319094501 Eh** | `refine.log` **L124211** |
| Normal termination | 2026-10-17 10:30:06 | `refine.log` **L125662** |
| 规模 | 134 个 SCF / 270 个 orientation 块 | `refine.log` |
| 几何与 I2 的关系 | 除甲基三 H 外 RMSD **0.045 Å**，整帧 0.2259 Å（甲基转 120°） | 脚本 `e_rmsd.py` |

### 5.2 频率表校验（严格按 `Frequencies --` 频段表）

| 项 | 值 | 位置 |
|---|---|---|
| 组数 × 3 | **39 × 3 = 117** | 首组 `frequency.log` **L1511**，末组 **L3335** |
| 3N−6（N=41） | **117** | 相等 `True` |
| 负值（表内） | **−128.0397 cm⁻¹**（唯一一个） | **L1511** |
| imaginary 头行 | `******    1 imaginary frequencies (negative Signs) ******` | **L1502** |
| 约化质量 | **1.0379 AMU** | **L1512** |
| 力常数 | **0.0100 mDyne/Å** | **L1513** |
| Low frequencies 探针（只作伪迹识别，不作判据） | −128.0475 / −10.7450 / −5.6627 / −0.0008 … | **L1500–L1501** |

### 5.3 虚模主导成分：**是甲基转动 pseudo-saddle，不是质子转移也不是 C–O 成键**

模矢表（`frequency.log` **L1515–L1555**，逐行断言 41 行、原子号 1..41 顺序、每行 11 字段；占比 = |d|²/Σ|d|²）：

| W 序 | 元素 | dx | dy | dz | \|d\| | 占比 |
|---|---|---|---|---|---|---|
| **W15** | H | −0.41 | −0.22 | +0.44 | 0.640 | **41.1 %** |
| **W14** | H | +0.50 | +0.13 | +0.29 | 0.592 | **35.2 %** |
| **W16** | H | −0.12 | +0.05 | −0.46 | 0.478 | **22.9 %** |
| W12 | H | −0.01 | +0.03 | −0.02 | 0.037 | 0.1 % |
| W3 | C | −0.01 | −0.00 | +0.03 | 0.032 | 0.1 % |
| W2（亚胺碳） | C | −0.00 | +0.01 | −0.02 | 0.022 | 0.1 % |
| W4（N） | N | −0.00 | +0.01 | −0.01 | 0.014 | 0.0 % |
| W25（水 O） | O | +0.01 | +0.00 | −0.00 | 0.010 | 0.0 % |

分组合计：**甲基三 H（W14/W15/W16）= 99.2 %**；亚胺碳 W2 = 0.1 %；N4 = 0.0 %；水 O25 = 0.0 %；W26 = 0.1 %；羧基 O10 = 0.0 %。
声明键对的成对投影点积（d_i·d_j/Σ|d|²）：`2-4: 0.0 % / 2-25: 0.0 % / 25-26: −0.0 % / 4-26: −0.0 % / 2-3: −0.1 %`。

**判读**：H14/H15/H16 都挂在 W3（甲基碳）上（`a_identity.py` H 归属表 `14H-3C@1.095, 15H-3C@1.103, 16H-3C@1.101`），
模内碳位移≈0、三个 H 呈旋转式反相 ⇒ **C3–C2 轴向甲基转动**。这是一个 **pseudo-saddle（甲基转子）**，
而不是 O25–H 质子转移型、也不是 C2–O25 成键型。`【观察】`

### 5.4 更关键的一点：优化的 TS 把 guess 的入射键丢掉了

| 距离 | guess(190) | ts_opt(999) 末帧 | 变化 |
|---|---|---|---|
| `C2–O25`（成键对） | **1.900** | **3.138** | **+1.238 Å（水被推开）** |
| `C2=N4`（断裂对） | 1.331 | 1.299 | 仍为完整双键 |
| `N4–H26`（质子转移对） | 3.376 | 3.982 | 更远 |
| `O25–H26`（质子转移对） | 0.969 | 0.967 | 未动 |
| `O10–H27`（羧基质子化） | 1.501 | 1.721 | 停在 O25(0.989) 与 O10(1.721) 之间，未转移 |

⇒ 优化收敛到了一个**反应物盆地内的甲基转动鞍点**；E3 的任何一个化学事件都没有发生。`【观察】`

---

## 6 问题 4：IRC（job 1033）

| 项 | 值 | 位置 |
|---|---|---|
| 双向是否都跑完 | 名义上都跑完（各 1 点），Normal termination 2026-10-17 11:32:37 | `irc.log` **L3672** |
| 点号范围 | 正向 **点 1**、反向 **点 1**；`Total number of points: 2` | **L1489 / L2110 / L2170 / L2793**；**L2862** |
| 能量：初点 / 正向点1 / 反向点1 | **−939.319094501 / −939.319097479 / −939.319097211 Eh** | **L790 / L1957 / L2639** |
| 相对 I2 的 ΔE（纯电子） | +0.98 / +0.98 / +0.98 kcal·mol⁻¹ | 脚本 `d_energy_rmsd.py` |
| 几何位移（相对 TS） | 0.0082 Å（两侧相同） | 脚本 `e_rmsd.py` |

**每侧末点的四个关键距离（Å，W 序 + 化学标签）**

| 侧 | `C2–O25`（成键） | `C2–N4`（断裂） | `N4–H26`（N 上质子） | `O25–H26`（O 上质子） | E (Eh) |
|---|---|---|---|---|---|
| 正向 点 1 | 3.140 | 1.299 | 3.983 | 0.967 | −939.319097479 (L1957) |
| 反向 点 1 | 3.137 | 1.299 | 3.981 | 0.967 | −939.319097211 (L2639) |

**判读**：两侧都是反应物物种（键长、InChIKey、相对 I2 的 RMSD 全部一致），但**这是“没有位移”的结果，不是连通性结论**：
IRC 每侧只走了 1 点、位移 0.008 Å、能量只降 3×10⁻⁶ Eh。`【观察】`
因此：“两侧同物种”**只能**说明该鞍点的 IRC 没有离开 I2 盆地（因为鞍点本身就在 I2 盆地内），
**不能**说明“声明的产物端点不可达”。`【推断】`

---

## 7 问题 5：端点优化（1035 / 1041）

### 7.1 两个端点槽的**输入**（这是 B1/B2 的岔路口）

| 槽 | 实际输入 | 输入头注释 | InChIKey | `endpoint_source.json` |
|---|---|---|---|---|
| reactant | `reactant_opt/reactant_source.xyz` | `irc point=1 path=1 rx=0.10101 E=-939.31909500 Eh` | 反应物 | `kind=irc_outer_frame, label=B, irc_job_id=1033` |
| **product** | `product_opt/product_source.xyz` | `irc point=1 path=2 rx=-0.10141 E=-939.31909500 Eh` | **反应物** | `kind=irc_outer_frame, label=A, irc_job_id=1033` |

⇒ **两个端点槽都不是从声明的 seed 出发的**，都从 IRC 外帧出发；产物槽的起点本身就是一个反应物几何。`【观察】`

### 7.2 终止状态与末次 SCF

| job | Stationary point | Normal termination | 末次 SCF（行号） | ΔE vs I2 |
|---|---|---|---|---|
| 1035 reactant_opt | L21813 | L22902（12:16:41） | **−939.320655386（L21448）** | +0.00（+9.3×10⁻⁸ Eh） |
| 1038 reactant_freq | —（freq） | L5297（12:37:51） | −939.320655386（L817） | +0.00 |
| 1041 product_opt | L34530 | L35617（13:25:36） | **−939.320655496（L34156）** | −0.00（−1.7×10⁻⁸ Eh） |
| 1043 product_freq | —（freq） | L5301（13:33:07） | −939.320655496（L819） | −0.00 |

频率表校验（同样按 `Frequencies --` 组×3）：1038 = 39×3 = 117、负值 0（首表 L1513，最低 35.3651/46.4611/50.3485）；
1043 = 39×3 = 117、负值 0（首表 L1515，最低 35.3112/46.4293/50.2885）。

### 7.3 `product_opt` 的收敛几何到底是产物、还是塌回反应物、还是第三种？

**答：塌回反应物 I2，而且塌到的是 I2 的“甲基转过 120°”的同一个极小**（第三种物种被排除）。

| 判据 | 结果 |
|---|---|
| InChIKey | `FYDMZWJHNXGWEQ-BWNURDBISA-N` = 声明反应物 / I2（不是产物 SMPZMO…）`【观察】` |
| 键长 | `C2=N4 1.299`、`C2–O25 3.160`、`N4–H26 4.007`、`O25–H26 0.966`（I2 全套）`【观察】` |
| ΔE vs I2 极小 | **−1.7×10⁻⁸ Eh（≈ −0.00001 kcal/mol）**`【观察】` |
| 几何差 | 全 41 原子 RMSD 0.4833 Å，但**去掉甲基三 H 后只有 0.0006 Å**；逐原子最大偏差 = W15 1.805 / W14 1.782 / W16 1.766 Å，其余 ≤0.044 Å `【观察】` |
| 与 P 的关系 | InChIKey 不同；RMSD(③, P) = **2.1531 Å**；ΔE(P − ③) = **+0.001115312 Eh = +0.70 kcal/mol** `【观察】` |

⇒ ③ 与 I2 是**同一化合物的两个甲基转动异构体（对称等价，能量在 10⁻⁸ Eh 内相同）**：不是第三种物种。`【推断：由“仅甲基 H 差 1.8 Å + 其余 <0.05 Å + 能量差 1.7×10⁻⁸ Eh”共同支持；等价性本身是 C3 对称的必然结果】`
另：`reactant_opt`(1035) 与 I2 的 RMSD 只有 0.0011 Å（最大 0.003 Å）⇒ 反应物槽是“原样回到 I2”。`【观察】`

### 7.4 B1 / B2 判定

| 假设 | 判定 | 决定性证据 |
|---|---|---|
| **B1｜build 产物种子的连接性本身就是反应物的** | **排除（假）** | ②/②' 的 InChIKey = ① = ④（`SMPZMOQIWMNUBG-YBVIJTQESA-N`）；② 键长 `C2=O25 1.2356`、`C2···N4 5.628`（无键）、`N4–H26 1.0259`、`C9–O10 1.353 / C9=O11 1.2224`；`seed.mol` 与 `complex_candidate_000.mol` 同 sha256 |
| **B2｜seed 连接性对，但构象/质子位置在优化中塌回 I2** | **未被检验（不是本次的原因）** | 1041 的输入是 IRC 外帧（InChIKey = 反应物，`C2–O25 3.137`），**不是** seed；seed 从未被优化。要检验 B2 必须从 seed 真跑一次 opt（未授权） |
| **B0｜端点槽种子来源错（用 IRC 外帧代替声明 seed）** | **成立（本次真实原因之一）** | `endpoint_source.json` × 2 + `product_source.xyz` 头注释 + 输入帧的 InChIKey |

**“平台 verdict 的 identity mismatch 解释的是哪一部分”**：它解释的是 **(i) 产物槽最终几何 = 反应物** 这一条（真实、可复现）；
而 “product built MOL does not match its declared SMILES” 这一句**在化学层是错的**（①=②），它只能来自**映射层**：
`atom_map` 与化学对应只有 **3/41** 一致（若把 map 值当 product-seed 索引读，元素一致率只有 25/41；
当 reactant 序读 28/41 —— 一个正确的原子对应应当 41/41），`reaction_center` 则只有按 **0-based** 读才是化学上有意义的 6 对（见下表）。`【推断】`

### 7.5 `reaction_center` 的 0-based 自证（6 对全查）

| 声明对（原文） | **1-based** 读法（元素 / I2 d / guess d / TS d） | **0-based（+1）** 读法（元素 / I2 d / guess d / TS d） |
|---|---|---|
| (1,3) | W1C–W3C（C–C 已有键）2.582 / 2.530 / 2.556 | **W2C–W4N（亚胺 C=N，断裂）1.299 / 1.331 / 1.299** |
| (1,24) | W1C–W24H 2.639 / 3.041 / 2.645 | **W2C–W25O（C–O，成键）3.160 / 1.900 / 3.138** |
| (24,25) | W24H–W25O 4.651 / 4.217 / 4.629 | **W25O–W26H（水 O–H，断裂）0.966 / 0.969 / 0.967** |
| (24,26) | W24H–W26H 5.036 / 4.402 / 5.075 | **W25O–W27H（水第二个 O–H）0.990 / 1.032 / 0.989** |
| (3,25) | W3C–W25O 3.286 / 2.544 / 3.356 | **W4N–W26H（N–H，成键）4.006 / 3.376 / 3.982** |
| (10,26) | W10O–W26H 3.126 / 3.015 / 3.135 | **W11O–W27H（羧基 O–H）3.645 / 3.398 / 3.641** |

0-based 读法把“6 个键对”全部落成 E3 的化学语义（其中 5 对完全正确；第 6 对给出的是 W11 而不是实际产物里被质子化的 W10 ⇒ **0-based 也不完全自洽**）。
1-based 读法给出的全是 H–H 5.0 Å 之类的无意义对。`【观察】` ⇒ 声明层的索引体制存在 off-by-one 混乱。
注意 `process.json effective_reaction_center = []`，所以该混乱**没有**被用来约束本次计算（不构成 ts_opt 滑落的因果）。`【观察】`

---

## 8 四项关键距离总表（Å；W 序 + map 标签 + 化学标签；`b_logs.py` §5）

| 帧 | `C2–N4` 亚胺 C–N | `C2–O25` C–水O/酮O | `O25–H26` O–H（水） | `N4–H26` N–H | `O10–H27` 羧基 O–H | `O25–H27` 水第二 O–H |
|---|---|---|---|---|---|---|
| 反应物 seed / I2 极小 | 1.299 | 3.160 | 0.966 | 4.006 | 1.717 | 0.990 |
| TS guess（1.90 帧） | 1.331 | **1.900** | 0.969 | 3.376 | 1.501 | 1.032 |
| ts_opt(999) 末帧 | 1.299 | **3.138** | 0.967 | 3.982 | 1.721 | 0.989 |
| IRC 正向点 1 | 1.299 | 3.140 | 0.967 | 3.983 | 1.721 | 0.989 |
| IRC 反向点 1 | 1.299 | 3.137 | 0.967 | 3.981 | 1.721 | 0.989 |
| reactant_opt(1035) 末帧 | 1.299 | 3.160 | 0.966 | 4.007 | 1.717 | 0.990 |
| product_opt(1041) 末帧 | 1.299 | 3.160 | 0.966 | 4.007 | 1.717 | 0.989 |
| **P(1061) 末帧** | **3.331** | **1.217** | **3.137**（O25 无 H） | **1.020** | **1.011** | 2.367 |
| **产物 seed（S→W 映射后）** | **5.628** | **1.236** | （O25 无 H） | **1.026** | **0.993** | （H27 在 O10） |

---

## 9 能量表（纯电子 RB3LYP/def2-SVP；**不是能垒**）

参考物：**I2 极小 = −939.320655479 Eh**（job 961，`I2_optfreq.log` **L16950**（Link1 step 1 末次 SCF；step 2 的 L19183 同值），sha `63dda25e…`）

| 项目 | E (Eh) | 行号 | ΔE vs I2 (kcal/mol) |
|---|---|---|---|
| ts_opt(999) 末 | −939.319094501 | `refine.log` L124211 | **+0.98** |
| frequency(1029) | −939.319094501 | `frequency.log` L818 | +0.98 |
| IRC 初点 / 正向 1 / 反向 1 | −939.319094501 / −939.319097479 / −939.319097211 | `irc.log` L790 / L1957 / L2639 | +0.98 / +0.98 / +0.98 |
| reactant_opt(1035) 末 | −939.320655386 | L21448 | +0.00 (+9.3e−8 Eh) |
| product_opt(1041) 末 | −939.320655496 | L34156 | −0.00 (−1.7e−8 Eh) |
| **P(1061) 末（step 1 / step 2）** | **−939.319540184** | **L66877 / L69139（同值）** | **+0.70** |
| I2(961)（step 1 / step 2） | −939.320655479 | L16950 / L19183（同值） | 0 |

派生：`ΔE(TS999 − P) = +0.000445683 Eh = +0.28 kcal/mol`；`ΔE(P − product_opt1041) = +0.70 kcal/mol`。
P(1061) 的 Link1 分段：**step 1 = opt（末次 SCF L66877，Normal termination L68350 @16:24:12）**、
**step 2 = 纯 `Freq` 链接（路由 L68354，SCF L69139，频率表首行 L69831，Normal termination L73964 @16:34:16）**；
step 2 里 L72258–L72262 的 “Optimization completed / -- Stationary point found.” 是 Freq 链接回显的优化收敛表，不是第二次优化。
P 的频率表：39×3 = 117、**负值 0**、最低实模 **16.6787 / 25.9714 / 30.2724 cm⁻¹（L69831）**。

> **为什么 P（产物）比 I2（反应物）还高 +0.70 kcal/mol 重要**：说明这一步在纯电子能上近乎热中性、产物端是“两片段松散复合物”
> （P 里 `C2···N4 = 3.331 Å`）。盆地浅 ⇒ 任何从 TS 附近出发的松弛都极易被 I2 盆捕获，这也是“IRC 2 点 + 端点 opt”必然回到 I2 的物理背景。`【推断】`

---

## 10 被显式检验并排除的替代解释

| # | 替代解释 | 检验方式 | 结果 |
|---|---|---|---|
| E-1 | **B1：装配产物的连接性就是反应物**（C2–N4 仍是键、C2–O25 未成键、质子位置像 I2） | ②/②' 键感知 + InChIKey + 逐键长 | **排除**：`C2=O25 1.236`、`C2···N4 5.628`、`N4–H26 1.026`、`COOH 1.353/1.222`；InChIKey = 声明产物 |
| E-2 | B2：1041 从 seed 出发但构象/质子塌回 I2 | 读 1041 的输入文件与 `endpoint_source.json` | **不成立（未发生）**：1041 输入 = IRC 外帧（反应物几何），seed 未被优化。B2 仍**未能判定**（需一次从 seed 起的 opt，未授权） |
| E-3 | IRC 两外侧帧是两个不同物种被误读成同一 SMILES | 两帧 InChIKey + 6 个键长 + 与 TS/I2 的 RMSD | **排除**：两帧互差 0.0165 Å、与 TS 差 0.0082 Å、键长逐项相同；同 SMILES 是“2 点截断”的必然结果 |
| E-4 | 端点身份不成立是因为 built MOL 与声明 SMILES **化学不符** | ①的 InChIKey vs ②的 InChIKey；①与②键数 41/41 | **排除化学不符**；mismatch 只能出在映射层（atom_map 3/41、reaction_center 0-based）`【推断】` |
| E-5 | 端点槽回到 I2 ⇒ 产物端点不存在 / product seed 不可达 | 独立参考点 P（job 1061） | **排除**：P 从 `P_e3b_product_41_seed.xyz` 收敛到声明产物（InChIKey 同 ①）、Stationary point L67255、117 模 0 虚频、最低实模 16.6787 |
| E-6 | 单虚频 −128.04 是 E3 的质子转移 / C–O 成键鞍点 | 模矢表 41 行逐行读数 + 分组占比 | **排除**：99.2 % 落在甲基三 H（W14/W15/W16），声明键对合计 ≈0.1 % |

---

## 11 修正后的步骤假设，以及“用什么测量能区分”

**H-E3-a（一步协同，题源原假设）**：单个 TS 同时完成 C2–O25 成键、C2–N4 断裂、O25–H26 → N4、O25–H27 → O10（羧酸根）四次事件。
**H-E3-b（两步）**：B-1 半缩胺形成（C2–O25 成键 ± H27 → O10）；B-2 半缩胺坍塌（C2–N4 断裂 + H26 → N4）。

当前证据对两者的**净贡献**：

| 证据 | 支持哪一方 | 强度 |
|---|---|---|
| ts_opt(999) 从 `C2–O25 1.900` 直接滑回 `3.138`，无任何键事件 | 说明“在 41 原子模型上、以 1.90 Å 为起点、沿甲基转子模”没有连通产物端的下降方向；**不区分一步/两步**（两步的 B-1 同样要先成 C–O，也可能在此失败） | 中（只覆盖 1 个起点 + 1 个模） |
| 同势能面上存在 0 虚频的离散半缩胺极小（`E3/runs/interm_c160/interm_c160_optfreq.log`：`d(2,25)=1.4728`、`d(2,4)=1.4248`、`d(10,27)=0.9949`；+5.04 kcal vs I2，见 `HI1/PROCESS.md` §2 观测 6） | **偏向两步**：至少“半缩胺”是一个真实极小，两步分解在该 PES 上有落点（存在极小不等于协同路径不存在） | 中 |
| P 只比 I2 高 +0.70 kcal/mol（纯电子） | 与机制无关，但说明产物盆地浅 ⇒ IRC 必须够长才可能跨过去 | — |

**区分这两者的测量（按判别力排序，全部需要在授权后新算）**

1. **半缩胺极小的存在性（最便宜、最直接）**：从 I2 + 水出发，只驱动 `C2–O25` 到 ≈1.45 Å 后放开优化 + 频率。
   - 若得到 **0 虚频**、`C2–O25 ≈ 1.42–1.50`、`C2–N4 ≈ 1.42–1.50`、N4 **未**质子化 ⇒ 两步成立（该点即 B-1 产物）。
   - 若一放开就退回 I2 或直接跨到 P（无极小）⇒ 两步的中间体不存在，协同解释优先级上升。
   （`interm_c160` 已是该测量的一个正结果，但需要独立复核其原子计数与质子化态。）
2. **第一鞍点的 IRC 拓扑（判别力最强）**：拿一个满足两条判据的鞍点（① 恰 1 虚频；② 虚模主导成分落在声明键对，而不是甲基/芳环/水转子），
   跑**双向 IRC，maxpoints ≥ 20、步长 0.1–0.2**，并断言两侧各 ≥10 点、末端梯度下降。
   - 一步协同 ⇒ 单条 IRC 把 I2 与 P 双双连上（两端各自 opt+freq 得 0 虚频）。
   - 两步 ⇒ 第一鞍点的 IRC 必须落在一个**新极小**（半缩胺）上，而 P 只能由第二个鞍点接上。
3. **鞍点几何判据（无需 IRC，即可先筛掉“假协同”）**：
   - 协同 TS：`C2–O25` 与 `C2–N4` 应**同时**处于 1.7–2.2 Å 的过渡区，且 H26 位于 O25 与 N4 之间（`O25–H ≈ N4–H ≈ 1.2–1.4 Å`）。
   - 若第一鞍点处 `C2–N4` 仍 ≈1.30 Å（完整亚胺双键）、H26 仍在 O25 上（本次 999 就是这样，只是连 C–O 也丢了）⇒ 它是“加成步”，不是协同 TS。
4. **能量学上限检查（避免把“没找到”当“不可达”）**：由于 P 只比 I2 高 +0.70 kcal/mol，任何“协同不可达”的结论都必须给出
   (a) 从 I2 到 P 的连续路径存在性证据，或 (b) 在 ≥3 个独立起点（1.75 / 1.82 / 1.90 Å，H27 分别在 O25 侧 / O10 侧）上的一致失败记录 + 每次的虚模成分。
   本次 run 只有 1 个起点、且该起点在第一步就丢了 C–O ⇒ 计数上**不足以**支撑“不可达”。

---

## 12 对共享记录 `HI1/PROCESS.md` 的建议增补（**本报告不改该文件**）

> 版本注记：开工时 `HI1/PROCESS.md` 为 154 行 / sha256 `e666ab15f1261bbfde9878a41e89c0b0ec99b4e8eed28bc126ac543a1d91f553`（Coordinator 给的值，我复核相同）；
> 本报告完成时该文件已被其他会话扩写为 254 行 / sha256 `935dc1be483891dcaae7afccdeb65cdc8a7aca206be9a1d07507a7a962301f3c`。
> 本报告引用的「§2 观测 1–3 / §2 观测 6 / §3 结论 H1」在新版本中**编号与内容未变**，引用仍然有效。我**未修改**该文件。

1. §2 观测 1–3 的措辞建议区分两件事：**“两个端点槽都弛豫回 I2”** 是 `endpoint_source.json` 决定的（输入就是 IRC 外帧），不是产物 seed 的性质；
   建议加一句“product 槽的输入 = IRC 反向点 1（InChIKey = 反应物），声明产物 seed 从未被优化”。
2. §3 结论 H1 成立的范围应收窄：ts_0011 证明的是“**该 guess + 该 2 点 IRC + 该端点种子链**不产生产物端点”，
   **不证明**“E3 单步协同不可达”；H1 若要保留“不可达”的说法，需要 §11 第 4 条那种多起点计数。
3. 新增一条可复用事实：`build/input_0004/product/seed.{xyz,mol}` 与声明产物、与 job 1061 的 P **InChIKey 完全相同** ⇒ 产物端点种子本身可用
   （E3b 的 `P_e3b_product_41_seed.xyz` 只是同物种的另一个构象种子；两者 InChIKey 相同）。
4. 新增一条工具性风险：`input_binding.atom_map` 与化学对应仅 3/41 一致、`reaction_center` 只有 0-based 读法才（基本）自洽
   ⇒ 后续若把 `reaction_center` 交给 `effective_reaction_center` 去约束，必须先修索引体制，否则会约束到错误的原子上。

---

## 13 复现与脚本

| 脚本（项目相对） | sha256 | 作用 |
|---|---|---|
| `gold_finish_20261015/HI1/E3/forensic/scripts/a_identity.py` | `c528a4556b52c5c022dc5702f88b6af8d1f0831d9aa202d7536fba66b595b5c2` | 身份四方对照、键表、H 归属、最小间距 |
| `gold_finish_20261015/HI1/E3/forensic/scripts/b_logs.py` | `2a09020fb03c47031a27d72c23f4114c6875a6652b01eb5dd1ede493ea2ab787` | 能量/终止/驻点台账、帧抽取（含行数断言）、距离表、帧身份、种子↔工作序映射 |
| `gold_finish_20261015/HI1/E3/forensic/scripts/c_cross.py` | `0db253e39c887e054879f75d325cdb9fdb7f22ebd5c1c7dbb531fb8580ae9cc8` | Link1 分段 SCF、频率表完整性、虚模成分表、reaction_center 0/1-based 检验、atom_map 一致性 |
| `gold_finish_20261015/HI1/E3/forensic/scripts/d_energy_rmsd.py` | `810a6a06a77116ba7cb3bf69383bbbc879920dea8d5fd6b70afbb12397923196` | ΔE 精确值与分片段 RMSD |
| `gold_finish_20261015/HI1/E3/forensic/scripts/e_rmsd.py` | `3a5d174daf9bc3fd2296fd52e563e3efdb7deced51e4d8b5919274001a1d4aa6` | 单一实现的标准 RMSD 矩阵 + 逐原子偏差（**本报告所有 RMSD 数字以本脚本为准**） |

运行方式（只读、无副作用）：`python3 gold_finish_20261015/HI1/E3/forensic/scripts/<name>.py`（仅用 rdkit / numpy，默认工作目录 = 项目根）。
**已执行的断言**：每个 orientation 块必须“第二条虚线后恰好 41 行 + 随后是闭合虚线”；元素顺序必须等于 canonical 工作序（8 个日志帧全部 True）；
频段表组×3 必须 = 3N−6（4 个 freq 日志全部 True）；模矢表必须 41 行、原子号 1..41 顺序、每行 11 字段；键长必须落在 §3.2 的化学区间。

### 本轮“未能判定”的三件事
1. `product_opt` 若**真的从声明产物 seed 出发**会落到哪里（P？另一个产物构象？还是塌回 I2）—— 需要一次从 `build/input_0004/product/seed.xyz` 起的 opt+freq（本任务禁止提交）。
2. 平台内部 “built MOL” 的具体构造路径（我从外部只能证明 ①=②、mismatch 只能来自映射层）。
3. E3 单步协同在 41 原子模型上是否真的不可达（本 run 的失败不足以回答；见 §11 第 4 条）。
