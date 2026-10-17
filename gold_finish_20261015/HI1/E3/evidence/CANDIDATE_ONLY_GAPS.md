# HI1_E3 · 上轮 candidate_only 缺口清单（只读复核，2026-10-15 lane2 续跑）

> 依据：`gold_finish_20261015/HI1/E3/STATUS.md` §A.3 / §A.4 / §A.5（上一任 lane2 的只读缺口复核）+ `gold_finish_20261015/HI1/audit/DECLARATION_AUDIT.md` + `HANDOFF_UNFINISHED_20261004.md` 记录。
> 本轮状态列只写"本轮有新证据产出"或"仍无证据"；**未产出前不判"已解决"**。
> 历史 114–120 链的原生日志在本地不存在（§A.1 已逐条 find 核实）→ 一切"历史上已满足"只算记录，不算本道证据。

## 一行一缺口

| # | 缺口（用户三分类） | 历史状态 | 本地可否复核 | 本轮措施（本道已定方案） | 本轮是否已被新证据解决 |
|---|---|---|---|---|---|
| G1 | **产物立体**：产物侧 aldol 碳（工作原子 29 / map6）的 CIP 是否 = S；脯氨酸 Cα（工作原子 8 / map16）是否仍 = S | 缺（历史拒收核心理由："产物立体在 atom 27 改变或未确定"；"atom 27"三种编号读法下都落在非手性原子，本地无法还原其 pipeline 编号 → 按化学语义判读为 aldol 碳 + 醇盐 O 质子归属） | 无 117–120 日志 → 不可复核 | 对 **P 侧端点经 Opt+Freq 后的实际几何**用 RDKit 3D 实测 CIP（原子 8=S、原子 29=S），并把 map↔本批原子序对照写进证据 | **尚未**（等 job 925 → I2 极小值 → TS 链 → 端点 Opt/Freq） |
| G2 | **原子来源**：参与水解的那一分子水的来源与连接关系（O4–H21/O4–H22 是否就是 HI1_E1 生成的水；端点是否出现 <2.5 Å 跨片接触导致分片/归属不确定） | 缺（历史拒收理由之一："交换端点归属时反应物有 1–38 近片间接触"） | 无 I2_start.xyz / 114–120 日志 → 不可复核 | 显式 map↔本批原子序对照表（`E3/prep/I2_P_atom_map.json`）+ 两端点 RDKit 分片/连接实测（氧来源：25 = map4 水 O；28 = map5 醇盐 O；氮：4 = map20） | **尚未**（方案与对照表已落盘；端点实测待产出） |
| G3 | **IRC 方向**：双向 IRC 两个方向各自真实走向声明的 I2 与 P（方向区间 → 端点映射） | 缺（116：两个方向都在迭代 19 达原生上限，从未形成"哪一侧 = I2、哪一侧 = P"的映射证明） | 无 IRC 日志/轨迹 → 不可复核 | ts_prepare 的 verification.irc（双向）+ 两侧端点 Opt+Freq 身份核验 +（可选）ts_guess verify(strict) 的路径方向一致性检验 | **尚未**（TS/IRC 链未建） |
| G4 | **虚频模组成**：唯一虚频模是否以 6 个声明成键/断键对为主 | 仅记录（115：唯一负频 −658.38 cm⁻¹） | 无 115 模矢 → 不可证明 | log_parser 的 `imaginary_modes.watch_pair_fraction`（watch pairs = C.2 的 6 对） | **尚未** |
| G5 | **能垒**：ΔE‡ = E(TS) − E(I2 极小值)（纯电子能、同一批 Gaussian 16） | 缺（历史从未给出；两端点"谁是 I2/谁是 P"未定） | — | 本批 Gaussian 16 同批日志内部相减 | **尚未** |
| G6 | **证据可核性**：原生日志不改写 + 绝对路径 + sha256 + 能量取自原始行 | 缺本地实体（§A.1：job82 I2、71/72/83、114–120、94/100/102 全不在本机；只有索引行） | 不可复核 | 本批全部作业走本机原生 .log，逐条记绝对路径 + sha256 + 原始行 | **尚未** |

## 判定口径

- 上轮 `candidate_only` 的正式含义（§A.3/§A.5）：只满足"TS 恰 1 个虚频（仅记录）"与"两端零虚频（仅记录）"；**缺第 2 项（IRC 方向区间 → I2/P 映射）、第 3 项（端点物种/质子/立体 CIP 核验）与第 4 项（能垒）**，第 5 项本地无原始产物无法复核，第 6 项未做。
- 一项缺口只有在**本批原生日志**上实测通过后才改写为"已解决"；不得用历史记录、索引行或几何预测替代。
- 旧值 16.9 / 19.2 一律作废，不回填、不引用。
---

## 附录 A · `reaction_mapping` 自动映射缺陷的逐字返回（主协调 issue #179 P6 引用页）

**调用**（`reaction_mapping`，一次调用；给了 product 具体结构，未给 reactant 具体结构）：

```json
{
  "reactant_smiles": "CC(C[C@H]([O-])c1ccccc1)=[N+]1CCC[C@H]1C(=O)O.O",
  "product_smiles": "CC(=O)C[C@H](O)c1ccccc1.O=C(O)[C@@H]1CCCN1",
  "product_path": "gold_finish_20261015/HI1/E3/prep/structure_build_P/assembly/complex_candidate_000.xyz",
  "reactant_charge": 0, "product_charge": 0, "reactant_multiplicity": 1, "product_multiplicity": 1
}
```

**逐字返回（ToolResponse.data 关键字段，未改写）**：

```json
{
  "is_success": true,
  "mapping_status": "unique",
  "binding_status": "inconclusive",
  "binding_source": "not_available",
  "reactant_identity": "not_provided",
  "product_identity": "match",
  "atom_map": [],
  "heavy_atom_map": [1,2,18,3,4,5,6,7,8,9,10,11,19,17,20,16,13,14,15,12],
  "formed_bonds": [[2,18],[12,15],[13,16],[17,20]],
  "broken_bonds": [[2,12],[12,13],[15,16],[17,18]],
  "order_changes": [{"atoms":[17,19],"reactant_order":1,"product_order":2}],
  "concrete_watch_pairs": [],
  "watch_pairs": [[2,12],[2,18],[12,13],[12,15],[13,16],[15,16],[17,18],[17,20]],
  "binding_diagnostics": ["Both reactant and product concrete structures are required to generate a full-atom mapping."],
  "message": "Graph-edit and atom-environment scoring produced a single leading candidate; still check it against the mechanism. Both reactant and product concrete structures are required to generate a full-atom mapping.",
  "n_candidates": 1
}
```

**这些下标属于工具自己的 SMILES 图序（不是本道工作原子序）**：
- reactant 重原子序：1 C(CH3) / 2 C(iminium) / 3 C(CH2) / 4 C(aldol) / 5 O(醇盐) / 6–11 苯基 C / 12 N / 13–15 吡咯烷 C / 16 Cα / 17 C(羧基) / 18 O(=O) / 19 O(OH) / 20 O(水)。
- product 重原子序：1 C / 2 C(酮 C) / 3 O(酮 O) / 4 C(CH2) / 5 C(aldol) / 6 O(aldol OH) / 7–12 苯基 / 13 O(羧基 C=O) / 14 C(羧基) / 15 O(羧基 OH) / 16 Cα / 17–19 吡咯烷 C / 20 N。

**为何"unique 但化学错"（逐项对照）**：

| 项 | 工具给出 | 化学正确值 | 判定 |
|---|---|---|---|
| product 3（产物酮 O）来源 | reactant **18**（羧基 C=O 的 O） | reactant **20**（水的 O = 本道 map4 / 工作原子 25） | ✗ 错配（与 E3/STATUS §D 记录"产物酮 O / 羧基 O / 水 O 错配"一致） |
| product 13（羧基 C=O 的 O） | reactant **19**（羧基 OH 的 O） | reactant 18 | ✗ 两个羧基 O 互换 |
| product 15（羧基 OH 的 O） | reactant **20**（水的 O） | reactant 19 | ✗ 水 O 被挂到羧基上 |
| 成键表 | formed [[2,18],[12,15],[13,16],[17,20]] | 语义上只应有 (2,25)/(4,26)/(28,27) 三个新键（本道工作序） | ✗ 含 [12,15]（N–环 C）等假键 |
| 断键表 | broken [[2,12],[12,13],[15,16],[17,18]] | 语义上只应有 (2,4)/(25,26)/(25,27)（本道工作序） | ✗ 把环 C / 羧基原子当断键对象 |
| concrete 绑定 | binding_status=inconclusive, concrete_watch_pairs=[] | 需 concrete 绑定才给 watch pairs | 不可用（缺 reactant 具体结构所致） |

**结论**：该调用**不可用于 E3 的 TS 声明**；E3 采用手工推导并逐原子核对的 `E3/prep/I2_P_atom_map.json`（sha256 `33912bbd415bc424da1f086bc61c696cd6b9eac5f4f2aa7c8b550cd3ce3a980e`），并在拿到 I2 极小值后用**两个具体结构**重跑一次 concrete 对照。
（与 NY3 独立发现的"甲氧基脱离被误读成甲基迁移"同源缺陷，已由主协调并入 issue #179 P6。）

