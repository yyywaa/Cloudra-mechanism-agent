# NY3-R2（槽位替换）设计稿：Y2 甲酸甲酯酸催化水解 AAC2

生成时间：2026-10-17 13:5x CST（本机时钟）｜状态：预筛中

## 0. 授权与边界
- 用户 2026-10-17 13:5x：「NY3 干脆换了算了，换个能算的。」⇒ 放弃碱式皂化（Na⁺ 桥联 + 超软羟基扭转面，E1/E2/E3 全部 NStep/软模墙/近简并驻点），NY3 槽位换成 **Y2：甲酸甲酯酸催化水解 AAC2**。
- 旧包证据全部**只读留档**（`gold_finish_20261015/NY3/`，含 STATUS §1–§39、E1/E2E3 全部 log），旧值 15.5/12.5/0.0 作废、不回填。
- 新工作目录：`gold_finish_20261015/NY3_R2/`。

## 1. 体系（真实计算体系，必须与 prompt 的 SMILES 一致）
- 总反应：`[OH3+].COC=O.O >> [OH3+].O=CO.CO`（甲酸甲酯 + H₃O⁺ + H₂O → 甲酸 + 甲醇 + H₃O⁺）
- charge +1 / mult 1；**15 原子**（H₃O⁺ 4 + HCOOCH₃ 8 + H₂O 3）
- 条件：稀酸水溶液，加热（CPCM 水）

## 2. 映射（bond_changes 的索引口径 = 1-based）
`mapped_reactants = "[OH3+:1]([H:10]).[CH3:2][O:3][CH:4]=[O:5].[OH2:6]([H:11])[H:12]"`
| 映射号 | 原子 | 角色 |
| --- | --- | --- |
| 1 | H₃O⁺ 的 O | 酸催化质子源/受体；后续作为水接收质子 |
| 10 | H₃O⁺ 的转移质子（显式） | O1–H10 → O5（羰基 O 质子化） |
| 2 | 甲氧基 CH₃ 的 C | 与 O3 成键，最终随甲醇离去 |
| 3 | 甲氧基 O | C4–O3 消除时断键，接受质子成甲醇 |
| 4 | 羰基 C（甲酰基 C，带 1 个隐式 H） | **反应中心**：水 O6 进攻点 |
| 5 | 羰基 O | 先被质子化；四面体中间体坍塌时重新成 C=O |
| 6 | 进攻水的 O | **O6–C4 成键**（决速步候选） |
| 11 | 进攻水的 H（转移到 O1） | O6–H11 → O1 |
| 12 | 进攻水的另一个 H | 保留在酸羟基上（产物甲酸的 OH） |

## 3. 机理图（4 条边；PT 边沿用 O3 约定 barrier 0.0 + 注明 PT 预平衡）
| 边 | 起点 → 终点 | 键变化（映射号） | 类型 | barrier |
| --- | --- | --- | --- | --- |
| E1 | RC → I1 | 断 O1–H10，成 O5–H10 | 羰基 O 质子化（PT 预平衡） | 0.0 |
| E2 | I1 → I2 | 成 O6–C4，断 C4=O5 π | **水加成（决速步候选，需 TS）** | 自算 |
| E3 | I2 → I3 | 断 O6–H11，成 O1–H11 | 四面体中间体脱质子（PT） | 0.0 |
| E4 | I3 → P | 断 C4–O3，成 C4=O5 π，断 O5–H10，成 O3–H10 | 坍塌消除 MeOH（需 TS） | 自算 |

节点 SMILES（unmapped，用作图节点 smiles 注记）：
- RC：`[OH3+].COC=O.O`
- I1（羰基质子化酯）：`[OH2+? ]` → 记作 `[OH2].COC(=O[H+])...` 由预筛后的真实几何确认后定稿
- I2（质子化四面体）：`[OH2].COC([OH])([OH2+])H` 类，定稿时按实际电荷/质子分布写
- I3（中性四面体中间体）：`[OH3+].COC([OH])(OH)H`
- P：`[OH3+].O=CO.CO`

> 节点 SMILES 必须在每步 Opt+Freq 收敛后按**实际几何**定稿（含显式溶剂水与 H₃O⁺），不得先写死。

## 4. 每条边必须凑齐的证据
1. TS（只走 ts_prepare/ts_resume，禁止手工提交）+ 频率（**恰 1 虚频，且模矢与声明键对一致**）
2. 两端 Opt+Freq **0 虚频**
3. 连通性（IRC 或替代口径；措辞不得写成「IRC 已双向到达」）
4. barrier_kcal_mol = 纯电子能差、相对**该步起点**
5. 竞争通道（若调查）

## 5. 可算性预筛（在跑）
- 会话 as_6fdd1a4300b74a9f（small_mol）：作业 A = RC Opt+Freq（要求 0 虚频）；作业 B = O6–C4 受约束弛豫扫描 2.80 → 1.45 Å（要求单一极大峰、峰高 ≤ ~35 kcal/mol）。
- 判据：≤90 min 机时内二者同时成立 ⇒ 继续全图；否则如实登记失败类型并换候选（O2 DMDO 环氧化）。

## 6. 落地（预筛通过后）
- 重写 `cloudra/benchmark/normal_registry/yo.py` 的 Y3 条目（name_en / conditions_en / mapped_reactants / steps）
- 同步 `ideapool/reaction_candidates/normal.md` 的 Y3 行（单元格禁裸竖线；改完同轮重解析并断言列数 = 表头列数）
- 重新生成 `ideapool/tasks/normal/NY3.json`（`python -m cloudra.benchmark.gen_normal_tasks`），prompt 里 SMILES 必须与实际计算体系一致
- 跑 `pytest tests/test_benchmark.py -k regenerate_identically`
