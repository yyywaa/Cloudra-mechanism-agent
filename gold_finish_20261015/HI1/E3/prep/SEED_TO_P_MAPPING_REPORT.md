# Seed(ts_0011 build product) → P(E3 工作序) 全 41 原子图同构映射报告

**性质**：post-freeze asset / non-delivery evidence，不进交付面，不改任何声明。
**生成时刻**：2026-10-17 19:32:32 CST（脚本 prep/map_seed_to_P_e3b_v4.py sha256 3b285bd2f2ac713209ab90631450c1d679808c4ed8e0d78917cb79061f5ccc22）。
**输入**：
- seed 坐标：`ts/ts_0011/build/input_0004/product/seed.xyz`，sha256 `06161a1411edf1e1402620ee13ca448c14d2ac167846c10f1e56bf8ec175078a`，41 原子（C15H21NO4）。
- seed 键表：`ts/ts_0011/build/input_0004/product/seed.mol`（41 原子 / 41 键，元素序与 seed.xyz 一致）。
- 参照：P 帧 job 1061 `gold_finish_20261015/HI1/E3/prep/P_1061_optframe.xyz`（41 原子，E3 工作序），P 键表由该几何经 RDKit `rdDetermineBonds.DetermineBonds(charge=0)` 感知（41 键）。

## 1. 算法与容差
1. 重原子子图：seed 与 P 各 20 个重原子，键序做**序无关化**（全部置 SINGLE，只保留元素 + 邻接）；
2. **RDKit VF2**（`GetSubstructMatches(uniquify=False, maxMatches=100000)`）枚举重原子同构；**容差 = 无**（精确元素 + 邻接同构，无 RMSD/距离阈值参与枚举）；
3. 氢补全：按「每个 H 的唯一重原子母体」分组，对每个母体的 H 做**全排列穷举**（CH3 3!=6、CH2 2!=2 …），只保留 41 原子双射且元素一致者；
4. 每个完整映射计算：重原子 **Kabsch 最优叠合 RMSD**、全原子 Kabsch RMSD、**键表逐边一致性**（含键序）、映射表 MD5（41 个 P 序号 1-based 的逗号串）。

## 2. 同构数与判别（要求：同构数、各自 RMSD、指纹、选用理由）
- 重原子同构数（VF2）= **4**；其中 **2 个**可完成 41 原子双射（iso 0 与 iso 2 因某母体 H 槽位数不匹配被排除，属真实结构差异，不是舍入）。
- 完整候选（各 96 个 H 排列，按 (非芳香键序不符, 重原子 RMSD) 取最优）：

| 重原子同构 | 重原子 Kabsch RMSD | 全原子 Kabsch RMSD | 键表不符行数 | 其中**非芳香**不符 | 映射表 MD5 | 备注 |
|---|---|---|---|---|---|---|
| **iso 3（选用）** | **2.2275 Å** | **2.5475 Å** | 6 | **0** | `954a61340bf368d35f8cfb531169a5f9` | 6 行全部是 seed 的 Kekulé 单/双 ↔ P 的 `AROMATIC`，属芳香表示差，不是化学不符 |
| iso 1 | 2.2916 Å | 2.6792 Å | 6 | **0** | `6f18e28ef9a2cd4f0825cee6575a6f82` | 同上；与 iso 3 的**关键键读数完全相同** |
| iso 0 | — | — | — | — | — | 不能完成 41 原子双射（H 槽位不符） |
| iso 2 | — | — | — | — | — | 同上 |

- **排序前二重原子 RMSD 差 = 0.0641 Å（2.2275 vs 2.2916）** ⇒ 小于主协调设定的 0.3 Å 阈值，故**两个候选都列出**；选用 iso 3 的理由：① 非芳香键序不符同为 0（化学一致性并列）；② 重原子与全原子 Kabsch RMSD 均更低（2.2275 < 2.2916；2.5475 < 2.6792）；③ **两个候选的 5 个关键键读数逐一相同**（见 §4），故本报告的任何化学结论对二者不敏感。

## 3. 41 行映射全表（seed 1-based → E3 工作序 1-based；iso 3）
```
seed  1 C  -> E3  3 C      seed 15 H  -> E3 16 H      seed 29 C  -> E3  7 C
seed  2 C  -> E3  2 C      seed 16 H  -> E3 12 H      seed 30 C  -> E3  6 C
seed  3 O  -> E3 25 O      seed 17 H  -> E3 13 H      seed 31 C  -> E3  5 C
seed  4 C  -> E3  1 C      seed 18 H  -> E3 36 H      seed 32 N  -> E3  4 N
seed  5 C  -> E3 29 C      seed 19 H  -> E3 24 H      seed 33 H  -> E3 27 H
seed  6 O  -> E3 28 O      seed 20 H  -> E3 41 H      seed 34 H  -> E3 23 H
seed  7 C  -> E3 30 C      seed 21 H  -> E3 40 H      seed 35 H  -> E3 21 H
seed  8 C  -> E3 35 C      seed 22 H  -> E3 39 H      seed 36 H  -> E3 22 H
seed  9 C  -> E3 34 C      seed 23 H  -> E3 38 H      seed 37 H  -> E3 19 H
seed 10 C  -> E3 33 C      seed 24 H  -> E3 37 H      seed 38 H  -> E3 20 H
seed 11 C  -> E3 32 C      seed 25 O  -> E3 11 O      seed 39 H  -> E3 17 H
seed 12 C  -> E3 31 C      seed 26 C  -> E3  9 C      seed 40 H  -> E3 18 H
seed 13 H  -> E3 14 H      seed 27 O  -> E3 10 O      seed 41 H  -> E3 26 H
seed 14 H  -> E3 15 H      seed 28 C  -> E3  8 C
```
- 双射断言：41 个 P 序号互不相同（`len(set)=41`），逐位置元素一致（`el_s[i]==el_p[order[i]]` 全通过）。

## 4. 硬判据与关键键（要求：C2 邻居 + 5 键两列）
**E3-C2（原子 2）在 P 中的邻居**：C1、C3、O25（P 侧 1-based：1 C / 3 C / 25 O）。
**其 seed 侧伙伴**：seed 4（C1）、seed 1（C3）、seed 3（O25） ⇒ **映射后 E3-C2 的邻居正是 C1/C3/O25 且 N4 已不在其配位圈内**（P 为产物：C2–N4 3.3308 Å 已断），C2 位点对得上。

| 关键键 | seed 侧原子（1-based） | seed 侧值 | P 侧（E3 1-based） | P 侧值 | seed − P |
|---|---|---|---|---|---|
| C2–N4 | seed 2 – seed 32 | **5.6280 Å** | 2 – 4 | 3.3308 Å | +2.2972 Å |
| C2–O25 | seed 2 – seed 3 | **1.2356 Å** | 2 – 25 | 1.2172 Å | +0.0184 Å |
| N4–H26 | seed 32 – seed 41 | **1.0259 Å** | 4 – 26 | 1.0200 Å | +0.0059 Å |
| O25–H26 | seed 3 – seed 41 | **4.4918 Å** | 25 – 26 | 3.1370 Å | +1.3548 Å |
| O10–H27 | seed 27 – seed 33 | **0.9934 Å** | 10 – 27 | 1.0112 Å | −0.0178 Å |

**判定（明写）**：**该 seed 在键表层面已偏产物侧** —— H26 已挂在 N4 上（N4–H26 1.0259 Å）、O25 已无氢且是 C2 的双键氧（C2–O25 1.2356 Å）、C2–N4 已拉大到 5.6280 Å（比 P 的 3.3308 Å 还远）、H27 稳定在 O10 上（0.9934 Å）。
⇒ 若 1073 最终落回 I2（反应物）盆，**不能**解释为普通构象效应，必须写成「**已产物化（C–N 已断、质子已在 N4）的种子在该级别下仍塌回反应物盆**」这一类更强的事实；反之若进 P 盆，也只是「产物型种子保持在产物盆」，**不构成反应物侧可达性的证据**。

## 5. 与主协调三条候选假设的对照（题面要求：冲突以同构为准并写明）
| 假设 | 图同构结果 | 判定 |
|---|---|---|
| seed **N32 ↔ E3 N4** | seed 32 N → E3 4 N | **成立** |
| seed **O27–H33 ↔ E3 O10–H27** | seed 27 O → E3 10 O；seed 33 H → E3 27 H | **成立**（羧基 O–H） |
| seed **O6–H19 ↔ E3 O25–H26** | seed 6 O → E3 **28 O**；seed 19 H → E3 **24 H** | **不成立（冲突）**：该 O–H 是**酮醇羟基**（对应 P 的 O28–H24，0.9689 Å 那对）；真正的 O25 是 seed **O3**，且 **O3 在 seed 中不带氢**（C2=O3 1.2356 Å），与产物 P 的酮羰基一致。氢 H26 的 seed 身份是 **H41（挂在 N32 上）**。 |

## 6. 复现
```
python3 gold_finish_20261015/HI1/E3/prep/map_seed_to_P_e3b_v4.py   # ~20 s，只读，无 QM
```
机器可读结果：`gold_finish_20261015/HI1/E3/prep/seed_to_P_mapping_v4.json`（含 4 个重原子同构的完整行、关键键、41 行映射）。
