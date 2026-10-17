# O2 TS working-order 映射表（提交门禁物，**先落盘再提交**）

生成：2026-10-17 15:10 CST（同轮 `date` 实测）｜会话 as_6fdd1a4300b74a9f（small_mol）
用途：`ts_prepare` 提交前的「文件行序 → working order」硬门禁表；**本文件只落盘，不含任何提交**。

## 0. 结论（一句话）
**working order = 具体坐标文件的行序（identity，1:1）**：reactant 用 `o2_seed.xyz`（与 guess `o2_butterfly_seed.xyz` **同一 17 原子序**，元素序列 `C C C O O C C H×10`），product 用 `build/art_prod/assembly/complex_candidate_000.xyz`。
依据：`reaction_mapping` 在**两侧都给出显式 heavy-atom binding** 后返回 `binding_status = complete`、`binding_source = concrete`、`mapping_status = unique`，其 `atom_map` 与 `concrete_watch_pairs` 就是**按这两个文件行序**给出的全原子映射。**guess xyz 的元素标签与本表同源**（同一 C C C O O C C H×10 序列，且 DMDO 片段坐标与 `o2_seed.xyz` 逐位一致、只重排乙烯），不存在「product 序坐标配 reactant 序标签」。

## 1. 文件与校验
| 文件 | sha256 | 行数/原子 |
| --- | --- | --- |
| `fallback_O2/o2_butterfly_seed.xyz`（guess，17 原子） | `e778222da483bc62c945e15a5d1e251337ed093639f8c6c7c4bda9249da71be2` | 19 行 / 17 原子 |
| `fallback_O2/o2_seed.xyz`（reactant 端点起点，**同序**） | `d7f812f89274c1ffc3a5deb1f0501bfb35a04d1e46b9bc0ea6ae18895675d4c4` | 19 行 / 17 原子 |
| `fallback_O2/build/art_prod/assembly/complex_candidate_000.xyz`（product 端点起点） | `4bdc98e0137fbd51b1b0bf7fb513cc207b56711230d0c6505ec0a37a1a10c45a` | 19 行 / 17 原子 |
| `fallback_O2/O2_BUTTERFLY_SEED.md`（guess provenance） | `98b5c2d1da7220d67f8aefb0022c671a667518aaf16dff5d58ffdf15e53f004a` | — |
| `fallback_O2/o2_product_optfreq.gjf` | `6197876b95aba5ca45eec5829c0e2e0238e914c17bb92d1455512317eb06a845` | 26 行 |

## 2. reactant working order（= 文件行序，17 行全覆盖）
键变化口径：成 `O4–C1`、`O4–C2`；断 `C3–O4`、`O4–O5`；`C3=O5` 双键生成；`C1–C2` 双→单。

| 文件序 | 元素 | working order | 角色（本表命名） | 映射号(DESIGN_O2) | 该原子参与的成/断键 |
| --- | --- | --- | --- | --- | --- |
| 1 | C | 1 | 乙烯碳 C1 | 6 | **成 O4–C1**；C1–C2 双→单 |
| 2 | C | 2 | 乙烯碳 C2 | 7 | **成 O4–C2**；C1–C2 双→单 |
| 3 | C | 3 | DMDO 环碳 C3 | 2 | **断 C3–O4**；**成 C3=O5**（丙酮羰基碳） |
| 4 | O | 4 | **转移氧 O4（反应中心）** | 4 | **成 O4–C1、O4–C2**；**断 O4–O5、C3–O4** |
| 5 | O | 5 | 过氧氧 O5 | 5 | **断 O4–O5**；**成 C3=O5**（丙酮羰基氧） |
| 6 | C | 6 | 甲基 C6 | 1 | 旁观（留在丙酮甲基） |
| 7 | C | 7 | 甲基 C7 | 3 | 旁观（留在丙酮甲基） |
| 8 | H | 8 | H on C1 | （随 C6） | C1 的 H，成环后仍在 C1 |
| 9 | H | 9 | H on C1 | （随 C6） | 同上 |
| 10 | H | 10 | H on C2 | （随 C7） | C2 的 H |
| 11 | H | 11 | H on C2 | （随 C7） | 同上 |
| 12 | H | 12 | H on 甲基 C6 | （随 C1） | 丙酮甲基 H |
| 13 | H | 13 | H on 甲基 C6 | （随 C1） | 同上 |
| 14 | H | 14 | H on 甲基 C6 | （随 C1） | 同上 |
| 15 | H | 15 | H on 甲基 C7 | （随 C3） | 丙酮甲基 H |
| 16 | H | 16 | H on 甲基 C7 | （随 C3） | 同上 |
| 17 | H | 17 | H on 甲基 C7 | （随 C3） | 同上 |

> H 的映射号一栏写「随」是因为镜像映射只在**重原子**上唯一：`reaction_mapping` 的 `heavy_atom_map = [1,2,5,3,6,4,7]` 唯一确定 7 个重原子的对应，10 个 H 的对应由父原子 + 对称性给出（`atom_map` 见 §4），同碳上的 H 互换对任何可观测量无影响。

## 3. product working order（= 文件行序，17 行全覆盖）
| 文件序 | 元素 | working order | 角色 | 对应 reactant working order |
| --- | --- | --- | --- | --- |
| 1 | C | 1 | 丙酮甲基 C（map 1） | 6 |
| 2 | C | 2 | 丙酮羰基 C（map 2） | 3 |
| 3 | C | 3 | 丙酮甲基 C（map 3） | 7 |
| 4 | O | 4 | 丙酮羰基 O（map 5） | 5 |
| 5 | H | 5 | 甲基 H | 12 |
| 6 | H | 6 | 甲基 H | 13 |
| 7 | H | 7 | 甲基 H | 14 |
| 8 | H | 8 | 甲基 H | 15 |
| 9 | H | 9 | 甲基 H | 16 |
| 10 | H | 10 | 甲基 H | 17 |
| 11 | C | 11 | 环氧乙烷 CH2（map 6） | 1 |
| 12 | C | 12 | 环氧乙烷 CH2（map 7） | 2 |
| 13 | O | 13 | 环氧乙烷 O（map 4 = O4） | 4 |
| 14 | H | 14 | 环上 H | 8 |
| 15 | H | 15 | 环上 H | 9 |
| 16 | H | 16 | 环上 H | 10 |
| 17 | H | 17 | 环上 H | 11 |

## 4. reaction_mapping 原始证据（本轮实跑，参数量级：binding complete / concrete）
- `mapping_status = unique`；`binding_status = complete`；`binding_source = concrete`；`reactant_identity = match`；`product_identity = match`
- `heavy_atom_bindings = {"reactant":[6,3,7,4,5,1,2], "product":[1,2,4,3,11,13,12]}`
- **`atom_map`（product 序 → reactant 1-based 序，全 17 原子）= `[6,3,7,5,12,13,14,15,16,17,1,2,4,8,9,10,11]`**
- `formed_bonds = [[4,6],[4,7]]`（映射号）= 成 O4–C6、O4–C7
- `broken_bonds = [[2,4],[4,5]]`（映射号）= 断 C2–O4、O4–O5
- `order_changes = [{atoms:[2,5], 1→2}, {atoms:[6,7], 2→1}]` = C2=O5 生成、C6–C7 双→单
- **`concrete_watch_pairs`（reactant 文件序）= `[[1,4],[2,4],[3,4],[4,5]]`**
- 结构指纹：reactant `9a101a1c4933a35af92d80c8fe8a7e94ae1f7a224a2f7adfb053a342bacb5571`；product `fcd1b47431c97af674a2d627ab551a445b68ee9204404900bcec1c2c83fab272`

## 5. reaction_center 交叉验证（硬要求）
- 提交用 `reaction_center = [[4,1],[4,2],[3,4],[4,5]]`（reactant working order，1-based）
- 与 reaction_mapping 的 `concrete_watch_pairs [[1,4],[2,4],[3,4],[4,5]]` **逐对相同（集合一致）** ✓
- 与 `formed/broken`（映射号）换算后一致：成 (O4–C1)、(O4–C2)；断 (C3–O4)、(O4–O5) ✓
- 与 DESIGN_O2.md「断 C2–O4 与 O4–O5；成 O4–C6、O4–C7、C2=O5；C6=C7 双→单」**完全一致** ✓
⇒ **reaction_center 已由 mapping 交叉验证通过，不是只看文字。**

## 6. 提交后核对义务
`ts_prepare` 成功后立刻用 `ts_inspect` 读**权威 current atom order**；若其 working order ≠ 本表（例如按 mapped SMILES 重排），我会在回报中给出「文件序 → 实际 working order」的更正表并说明差异来源，不以本表硬套。
