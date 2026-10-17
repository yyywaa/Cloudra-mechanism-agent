# E3a（run ts_0016）绑定与对称氧说明 — 必读，防止误读 map 标签

写入时刻实测：见 STATUS §P.16。作者：E3 道 small_mol。

## 1. 定义路径的是哪三样东西

1. `reaction.atom_map` = **恒等映射**（product atom i ↔ reactant atom i，i=1..41）。依据不是习惯，而是**键集差**：对两个 built seed（`ts/ts_0016/build/input_0002/reactant/seed.xyz` 与 `.../product/seed.xyz`）按共价半径判键后，**唯一差异**为
   - 只有产物有的键：`(2 C, 25 O)` = C2–O25 成键；`(10 O, 27 H)` = O10–H27 成键
   - 只有反应物有的键：`(25 O, 27 H)` = O25–H27 断裂
   重原子邻居元素差异只出现在 C2（+O）与 O25（+C）两处；元素级 H 对照对「O→O 质子迁移」是盲的，所以**键集差才是决定性判据**。
2. `reaction.reaction_center` = `[[2,25],[25,27],[10,27]]`（1 基；等价 0 基 `[[1,24],[24,26],[9,26]]`）：form C2–O25、break O25–H27、form O10–H27。
3. `guess` = S2 构造帧（sha `e3748c2c…`，provenance `51878313…`），中继中途。

## 2. 两端 built seed 上的 reaction_center 逐项实测（本轮新算，1 基原子号）

| 对 | 反应物 seed（= job 961 末帧） | 产物 seed（= job 1028 末帧） | 语义 |
|---|---|---|---|
| (2 C, 25 O) | 3.1596 Å（未成键） | 1.4728 Å（成键） | form C2–O25 |
| (25 O, 27 H) | 0.9895 Å（成键） | H27 已不在 O25 上 | break O25–H27 |
| (10 O, 27 H) | **1.7171 Å（氢键预组织）** | 0.9949 Å（成键） | form O10–H27 |
| (11 O, 27 H) 对照 | 3.6455 Å | 3.0517 Å | 全程不成键 ⇒ 支持落 O10 |
| C9–O10 / C9–O11 | 1.2544 / 1.2501 Å | 1.3297 / 1.2137 Å | 见 §3 |

**判读（观察，不是结论）**：水来的 H27 在**起点**就已预组织指向 O10，且两端一致 ⇒ 支持质子落 **O10** 而非 O11；这**不**构成 E3a verified，最终仍看 TS 虚频模 + 端点身份 + 连通性。

## 3. 羧酸根两氧的对称性：reactant 端不可分辨（必须写清的口径）

- reactant 端：C9–O10 **1.2544** Å vs C9–O11 **1.2501** Å，**差 0.0043 Å = 噪声级**，几何上**无法判定哪个是 C=O、哪个是 C–O⁻**（I2 是羧酸根 `[O-]/=O`）。
- product 端：有明确实测 —— O10 带 H27（0.9949 Å）、C9–O10 1.3297 > C9–O11 1.2137（单键更长）⇒ **hemiaminal 的羟基氧 = O10**。
- ⇒ **reactant 的 map13/map15 锚定是端点局部的对称/噪声选择**，不表示「map13 在两端指同一个氧、且该氧在起点就是 =O」。**不得**据此推断起点有 C=O 指认。
- 实测佐证：曾尝试把 reactant 两氧互换以「对齐」产物标签，工具直接拒收（`reactant: Explicit heavy-atom binding does not preserve the declared molecular graph, bonds or stereochemistry`），说明当时的键级感知把起点 =O 判在另一氧上 —— 正说明该判定在噪声级。

## 4. 两端 heavy_atom_binding（已通过工具校验的最终值）

- reactant（声明 SMILES 重原子序 C,C,C,C,O,ar6,N,C,C,C,C,C,O,O,O → 文件行号）：`[3,2,1,29,28,30,31,32,33,34,35,4,5,6,7,8,9,10,11,25]`
- product（重原子序 map 1,2,4,3,6,5,7,8,9,10,11,12,20,19,18,17,16,14,13,15 → 文件行号）：`[3,2,25,1,29,28,30,31,32,33,34,35,4,5,6,7,8,9,11,10]`

**RDKit 独立核对（reactant）**：`MolFromXYZFile(I2_min_v5.xyz)` + `rdDetermineBonds.DetermineBonds(charge=0)` → 41 原子 / 2 片段；声明 reactant SMILES `AddHs` 后 41 原子；`GetSubstructMatches(uniquify=False, useChirality=False)` 给出**恰好 2 个重原子匹配**：(a) `[3,2,1,29,28,30,31,32,33,34,35,4,5,6,7,8,9,10,11,25]`（= 上表，工具接受）；(b) `[3,2,1,29,28,30,35,34,33,32,31,4,5,6,7,8,9,10,11,25]`（仅苯环 30..35 反序，属环镜像自同构）。⇒ 该列表是合法同构匹配，不是手调。

**产物身份**：`prep/hemiaminal_1028_lastframe.xyz`（sha256 `be789d5fd013d11ec84b295f4249c61616a8e4de21e129e319c13497faab572d`，导出自 `runs/interm_c160/interm_c160_optfreq.log` sha `1ec7e4c6…`）经 RDKit 3D 判键 + 立体指派 ⇒ `C[C@@](O)(C[C@H](O)c1ccccc1)N1CCC[C@H]1C(=O)O`（CIP R/S/S，C15H21NO4，q0，1 片段）；声明的映射节点串 `[CH3:1][C@@:2](...)[C:14](=[O:13])[OH:15]` **去掉 map 后逐字符等于该串**，chirality-aware 双向匹配 True。

## 5. 结论（写给后续报告引用）

路径 = `atom_map`（恒等）+ `reaction_center`（三对）+ provided guess；**map 标签的氧锚定在两端不是同一物理氧**，这一点在报告中必须如实写出，避免把「map13」当成跨端点的同一原子。
