# NR1_E2 准备档案（全部非 QM，2026-10-15）

作者：NR1 包 E2 计算道 small_mol（session as_3554137d6af74102）。
口径：气相、charge=+1、multiplicity=1、26 原子 C6H17O3。正式级别（后续 QM）= Gaussian 16 `/home/ly/g16/g16`，B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight，不写 SCRF。

## 1 构造方法（非 QM）

- 工具：`smiles_to_mol(generate_3d=true, charge=1, multiplicity=1)`，输入为带 1-based 原子映射的复杂体 SMILES（组分以 `.` 分隔）。
  - I1（质子化频哪醇 + 水）：`[OH2:1].[CH3:3][C:4]([CH3:5])([OH+:6][H:2])[C:7]([CH3:8])([CH3:9])[O:10][H:11]`
  - I2（叔碳正离子 + 2 H2O）：`[OH2:1].[OH:6][H:2].[CH3:3][C+:4]([CH3:5])[C:7]([CH3:8])([CH3:9])[O:10][H:11]`
- 多组分输入由共享构建器做刚性取向采样 → 碰撞筛除 → MMFF94 弛豫，输出多个 complex candidate（xyz 与 mol 来自同一次 build：元素标签与坐标同源）。
- **已知工具现象（与 E1 道独立复现一致）**：复杂体构建会返回 `is_success=false`，消息为 "builder reported status='ok' but produced no MOL candidate"，但 candidate 的 xyz/mol 实际已落盘。本档案一律以磁盘文件 + sha256 为准。
- 结构校验：`internal_coordinates(mode=analyze, charge=+1)` 确认 26 原子、C6H17O3、总电荷 +1；I1 = 2 片段 / 24 键；I2 = 3 片段 / 23 键（含 1 个三配位 C+）。
- 反应坐标统一记为本道文件序 1-based `(5,7)`：row5 = 题面映射号 4（C4，离去侧碳），row7 = 题面映射号 6（O6，离去水氧）。与题源 `break [[4,6]]` 一致。

## 2 文件与 sha256（均为本目录相对路径）

I1 候选（`structures/build_I1/assembly/`）：
- complex_candidate_000.xyz `b5e3d673e9a6c5f190f074cde41232d14abf3ee655b756afffbe42acf95ac186` / .mol `b0f848c7953ff9e06066d1fca08a77dc36373f7301e63007e93e4a9eb87e7e3b`
- complex_candidate_001.xyz `da8df97156ea4a9a5f153d8a712dd8f716be633585354bdab2cc1b28bc87911a` / .mol `b0a9893abf61aee31d5c6dd254346a24298815bbc77c46630517984943b8accb`
- complex_candidate_002.xyz `0abdbb7cf40716dbe4a51e9368ad56d12140f9b7235c5e01b0d37c82a61da9af` / .mol `6d344f589fd8b07c8b0864a4176e35146347ae5cf0ade49dbb06367a71b4947f`
- 构建记录：`structures/build_I1/assembly/assembly.json`

I2 候选（`structures/build_I2/assembly/`，共 9 个；此处列前四个）：
- complex_candidate_000.xyz `5ecc2aae54a681669eb2d345af4dcfa36fa39ec97a2e68eac21e1dfc119d12ba` / .mol `6d2ef839a3c743bce48b9d425fa9d5492956e92acec77a7c8c286328ebdcfeab`
- complex_candidate_001.xyz `7770e06e5278750e26d771763b3af2c0c141cbdfbb5e988f580c9d78a0febd0a` / .mol `da29f6b3d29ffdcbc4c2c85182189f0e73a1d25094828699719835c208887f24`
- complex_candidate_002.xyz `f235db3656106eefffcd458dcd76e70ad50ca305a7154564be2b5b2c8ab322a4` / .mol `dec678acd764abb622c638352ac5c60b47931eb1112a30655a3b1272bb28bfd5`
- complex_candidate_003.xyz `2ca40615a9701006cf1ce7756a5c211e6cae2421326d20d4acf7df06179414b8` / .mol `fa8e894f99bc989fa5f02c7968dfa39d5329ee132f0ac382d592cbfcc8ff8a5e`
- 其余 004–008 见磁盘（同目录，`assembly.json` 记 MMFF 能量与放置索引）。

TS 初猜（非 QM）：
- `seeds/seed_stretch_C4O6_1.8A.xyz` `736e2e640c972d679571624421036a345fa4827d716372c0d7caf3158a64a79c`
- `seeds/seed_stretch_C4O6_2.2A.xyz` `1186e8710abc3031f8de0c68528fe9c8a72e86406e65caa95e8ae59360129948`
- `seeds/seed_stretch_C4O6_2.6A.xyz` `7c58885349be5f262dc813d213729ba4252a15443e23eb438abbef0513a7e7a3`
- `seeds/interp_idpp/img_00.xyz` `53306bc58a84d7b4d83c0561132f4575f78febbe7c71e72bd05b6c99f2c8ee47` … `img_11.xyz` `6c34df9ca814e285b7e0bda931ef5db73869b2d02ce1bce1ef9f47706569f72b`（12 帧全部在磁盘，见 `ts_guess` 距离表）

## 3 I1（E2 起点）候选与原子序对照

| 候选 | MMFF94 能量 | rel (kcal/mol) | r(C4–O6) | r(O1···O6) | 说明 |
| --- | ---: | ---: | ---: | ---: | --- |
| cand000 | 4.4385 | 0 | 1.426 Å | 2.479 Å | 水经 H 键挂在质子化 O6 上（本道首选起点种子） |
| cand001 | 4.4385 | 0 | 1.426 Å | 2.479 Å | 与 000 同构象、不同放置索引（对称等价取向） |
| cand002 | 4.5857 | +0.147 | 1.427 Å | 2.479 Å | 甲基旋转异构取向 |

**I1 cand000 原子序对照表（本道 xyz 行号 = 题面映射号）**

| 本道 1-based 行 | 元素 | 题面映射号 | 身份 |
| --- | --- | --- | --- |
| 1 | O | **1** | 原 H3O+ 的 O（现为水 O1） |
| 2 | H | 未映射 | O1 上 H |
| 3 | H | 未映射 | O1 上 H |
| 4 | C | **3** | C4 上甲基碳 |
| 5 | C | **4** | 离去侧碳 C4（反应坐标原子） |
| 6 | C | **5** | C4 上甲基碳 |
| 7 | O | **6** | 离去水氧 O6（反应坐标原子） |
| 8 | C | **7** | 保留侧碳 C7 |
| 9 | C | **8** | 迁移甲基碳 |
| 10 | C | **9** | 保留甲基碳 |
| 11 | O | **10** | 保留侧 OH 的 O |
| 12–14 | H | 未映射 | row4 甲基 H |
| 15–17 | H | 未映射 | row6 甲基 H |
| 18,19 | H | 其中一个是 **2** | O6 上两个 H（O6H2+，二者等价；映射的酸性 H2 落在此两行之一） |
| 20–22 | H | 未映射 | row9 甲基 H |
| 23–25 | H | 未映射 | row10 甲基 H |
| 26 | H | **11** | O10 上 H |

映射原子 1..11 落行：1→1；2→18 或 19；3→4；4→5；5→6；6→7；7→8；8→9；9→10；10→11；11→26。

## 4 I2（E2 产物）候选与原子序对照

| 候选 | MMFF94 能量 | rel (kcal/mol) | r(C4···O6) | 说明 |
| --- | ---: | ---: | ---: | --- |
| cand000 | −22.0098 | 0 | 4.614 Å | 2 个水互相 H 键并与 C7–OH 成 H 键；C+ 暴露 |
| cand001 | −22.0098 | 0 | 3.937 Å | 与 000 同能量级（对称等价取向） |
| cand002 | −21.6327 | +0.377 | 4.435 Å | 不同水取向 |
| cand003 | −19.3415 | +2.668 | 4.268 Å | 不同水取向 |

9 个取向全部保留在磁盘（000–008），未做 QM 筛选。

**I2 cand000 原子序对照表（本道 xyz 行号 = 题面映射号）**

| 本道 1-based 行 | 元素 | 题面映射号 | 身份 |
| --- | --- | --- | --- |
| 1 | O | **1** | 水 O1（原 H3O+ 的 O） |
| 2,3 | H | 未映射 | O1 上两个 H |
| 4 | O | **6** | 离去水 O6（已断开） |
| 5,6 | H | 其中一个是 **2** | O6 上两个 H |
| 7 | C | **3** | C4 上甲基碳 |
| 8 | C | **4** | 叔碳正离子 C4（CHG +1；键角 116.8/120.0/119.7° ≈ sp2） |
| 9 | C | **5** | C4 上甲基碳 |
| 10 | C | **7** | 保留侧碳 C7 |
| 11 | C | **8** | 迁移甲基碳 |
| 12 | C | **9** | 保留甲基碳 |
| 13 | O | **10** | 保留侧 OH 的 O |
| 14–16 | H | 未映射 | row7 甲基 H |
| 17–19 | H | 未映射 | row9 甲基 H |
| 20–22 | H | 未映射 | row11 甲基 H |
| 23–25 | H | 未映射 | row12 甲基 H |
| 26 | H | **11** | O10 上 H |

**本道自建的全原子映射**（`reaction_mapping` 以 concrete binding 绑定后返回，product 序 → reactant 序）：
`[1,2,3,7,18,19,4,5,6,8,9,10,11,12,13,14,15,16,17,20,21,22,23,24,25,26]`，`binding_status=complete`、`binding_source=concrete`、reactant/product identity 均 match；
`concrete_watch_pairs=[[5,7]]` = 题面 `break [[4,6]]`。

## 5 TS 初猜（非 QM，供 ts_prepare 的 guess 使用）

- **C4–O6 刚性拉伸种子**：由 I1 cand000 经 `internal_coordinates(mode=transform, operations=[{type:"stretch", atoms:[5,7], new_length:L}])` 得到 L = 1.8 / 2.2 / 2.6 Å，移动原子 = 离去水 (rows 7,18,19)。
  拉伸后检查：r(C4–O6) = 1.800 / 2.200 / 2.600 Å；r(O1···O7) = 2.202 / 2.156 / 2.156 Å → **局限已记录**：刚性拉伸把离去水推向旁观水，两水间距被压到 ~2.2 Å，非物理的拥挤；因此这三个文件只作"坐标插值初猜"，不作能量证据。
- **IDPP 插值路径**：`ts_guess(mode="interpolate", interp_method="idpp", n_images=12, atom_map=上面全原子映射, watch_pairs=[[5,7]])` → `seeds/interp_idpp/img_00..11.xyz`；r(C4–O6) 单调 1.4261 → 1.7138 → 1.9961 → 2.2756 → 2.5532 → 2.8326 → 3.1809 → 3.5501 → 3.9242 → 4.2511 → 4.4817 → 4.6140 Å。自动报出的"TS 候选帧" img_06（3.1809 Å）只按"跨过两端中点"命名，**不是鞍点证据**。

## 6 只读复核：E1 产物端点与本步起点是否同一物种

- 题面/交接只读事实：10-05 只读证据记录旧作业 112 收敛几何（78 modes 零虚频、E = −463.720481390504 Eh）实为 `CC(C)(O)C(C)(C)[OH2+].O`，即**质子化频哪醇＋水**；与题源 E1 声明产物 `NR1_I1 = "O.CC(C)(O)C(C)(C)[OH2+]"` 是同一物种（书写顺序不同）。→ **本步起点与 E1 声明产物同物种，方向一致**。
- 风险 1（质子归属）：E1 的声明起点 `[OH3+].pinacol` 与本步起点 I1 是同一 26 原子的两种质子归属。E1 道报告其 R 复合物几何为 r(O1–H) = 1.011 Å、r(O8–H) = 1.498 Å（质子偏在旁观水一侧）—— 若 DFT 优化时质子回到水一侧，则 I1 不是极小值而坍缩回 R（PLAN 的 H3 假设），E2 的"起点极小值"前提不成立。本道独立 Opt/Freq 后**必须**核验 O6–H / O1–H 归属，再决定是否走 TS；不假定上游 R 是极小值。
- 风险 2（原子序）：E1 道 builder 的编号（O8=题面 O6、C6=题面 C4、H4=题面 H2）与本道不同，**不得跨道复用坐标或索引**；本道全部判据使用 §3/§4 对照表。
- 风险 3（产物侧身份）：题面文字给的 E2 产物示意 `O.C[C+](C)C(C)(C)O` 只有 21 原子（1 个水）；题源图节点 `NR1_I2 = "O.O.C[C+](C)C(C)(C)O"` 与 ru.py steps[1] 的 `[OH2:1].[OH:6][H:2].[CH3:3][C+:4](...)` 都是 **26 原子（2 个水 + 叔碳正离子）**。本道采用 26 原子版本（与题源图、与 E1 产物 26 原子守恒一致）。**若最终按 21 原子版本交付，则与 E1 产物原子数不守恒** —— 已在 hub 记为该口径澄清项（不擅自改图）。
