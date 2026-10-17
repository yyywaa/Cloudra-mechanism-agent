# PROVENANCE — E3b 产物端 P（41 原子）构造种子与 Opt+Freq 输入

写入时刻见 STATUS §P.17。作者：E3 道 small_mol。**本文件只记录构造与自查，不含任何能量结论。**

## 1. 产物身份（与交付节点串逐字符一致）

- 节点串（源 `ideapool/tasks/hard/HI1.json` sha `54221e6591c75f88d2f6d96e853302c48bb25aefb9cc191aab2f6113119b61d0`，`/gold/mechanism_graph/nodes[10]/smiles[0]`）：
  `CC(=O)C[C@H](O)c1ccccc1.O=C(O)[C@@H]1CCCN1`
- 构造帧经 RDKit（`DetermineBonds(charge=0)` + `AssignStereochemistryFrom3D` + `RemoveHs`）得到的规范同分异构 SMILES **逐字符等于上面这串**（chirality-aware 双向匹配 True）；formula C15H21NO4、charge 0、**2 片段**、20 重原子 + 21 H = 41 原子。
- CIP：脯氨酸 Cα（**工作原子 8**）= **S**；苄位醇碳（**工作原子 29**）= **S** ⇒ (S)-aldol + (S)-脯氨酸。

## 2. 起点构造（方案 a：从 job 1028 收敛帧改键，保持 E3 工作原子序）

| 项 | 文件 / 值 |
|---|---|
| 母体几何 | `prep/hemiaminal_1028_lastframe.xyz` sha256 `be789d5fd013d11ec84b295f4249c61616a8e4de21e129e319c13497faab572d`（= job 1028 末帧，log sha `1ec7e4c6…`） |
| 构造脚本 | `prep/build_P_e3b.py` sha256 `422edc91959fe2abf3cb142917714b946663f112e6069f844ee5747cb02d7020` |
| 输出种子 | `prep/P_e3b_product_41_seed.xyz` sha256 `6c9d6ae26e161b6579fcd2c5fcbb70e44bc5a27f76e12cb01f52d40527f46eae` |
| Opt+Freq 输入 | `runs/P_e3b/P_optfreq.gjf` sha256 `d3b72aeae421780790bfd933acc5a0290de5d6da7938990803717276f9e760a4` |
| job | **1061**（8 cpus / 10240 MB / priority 0，local 后端） |

**三处几何操作（全部可复现）**
1. 断 C2–N4：把「脯氨酸片段」（以 N4 为种子、不经 C2 的连通分量，16 原子：4,5,6,7,8,9,10,11,17-23,27）沿 C2→N4 单位向量整体平移，使 **C2···N4 = 2.7000 Å**。
2. 还原酮：O25 移到 **C2–O25 = 1.2200 Å**（沿原 C2→O25 方向）。
3. 质子迁移：H26 从 O25 移到 **N4–H26 = 1.0200 Å**（沿 N4 孤对方向，由 N4 剩余两根键 C5/C8 反向和确定；N4 由三配位变四配位电子计数上为「二级胺 + H」= 3 根键）。

## 3. 自查（提交前实测，全部通过）

| 判据 | 实测 | 结论 |
|---|---|---|
| 41 原子 / C15H21NO4 / q0 / m1 | 41 / 是 / 0 / 1 | ✅ |
| 片段数 = 2（与节点一致） | 2（25 + 16 原子） | ✅ |
| minsep（全原子） | 0.9673 Å（原子 24–28） | ✅ ≥0.9 |
| 两片段最短重原子接触 | 2.7000 Å（N4···C2） | ✅ 2.6–3.0 |
| 虚假成键 | 无 C2–N4 键；键集差 = 新增 N4–H26、消失 C2–N4 与 O25–H26 | ✅ 恰为 E3b 预期 |
| 质子记账 | H27 留在 O10（0.9949 Å 未动）；H26 从 O25 (0.9693) 迁到 N4 (1.0200) | ✅ |
| 文件末尾 | `od -c` ⇒ `… 0 0 \n \n` | ✅ 防 l101 秒退 |

## 4. 用途与边界

- 该收敛帧将作 **E3b TS 的产物端种子**；因保持 E3 工作原子序，E3b 的 atom_map 可用**恒等映射**，reaction_center（1 基）= break C2–N4 (2,4)、break O25–H26 (25,26)、form N4–H26 (4,26)（C2–O25 由单键升为双键）。
- **ΔE(P − job 1028)** 仅作节点能量差登记（1028 = −939.312626605），**不是 ΔE‡、不进任何 barrier**。
- 该帧为**构造种子**（不是 TS，也不是已收敛的产物端）：产物端的收敛性由 job 1061 的 Opt+Freq 结果判定（117 模、0 虚频、Stationary point）。
