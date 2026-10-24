# HI1_E3 · legacy 13.36 登记（不参与评分）

记录时间：2026-10-18（主协调裁决：gold 侧置 null，不进准确度评分）

## 1 结论

- **HI1_E3 的盘上值 13.36 kcal/mol 是 legacy 值，不得作为 (S)-脯氨酸题面的定量答案，不进准确度评分。**
- gold 侧按 BRIEF §2「旧值一律作废、不得回填」置 **null**；证据不删，仅在本文件单列。
- 该值目前的唯一盘上位置：cloudra/benchmark/hard_registry/hi.py L99（step 3, channel=major_face），其 step_type 原文自带
  「barrier 13.36 is the legacy L2-identity value measured with the earlier program/model; retained unchanged and NOT a current-model measurement」。

## 2 来源与身份缺口（为什么不能当 (S) 体系的答案）

- 来源：旧三步图的 HI1_E2 槽（历史标答）。2026-10-17 本地把 HI1 拆成五步后，该 13.36 被机械搬到新 HI1_E3（立体决定步：烯胺 β-C 进攻苯甲醛），**没有任何本轮测量支撑**。
- L2 身份缺口：构建 13.36 的几何是 **R-脯氨酸**（RDKit 复核 job_51/52/54/64，Cα 全为 R），而现行题面要求 map16 全程 S ⇒ 两者是非对映体关系，不是 CIP 标注问题。镜像化后 favored/minor 命名不能原样沿用。
  证据：gold_finish_20261015/HI1/E2EM1/STATUS.md（§L2 缺口段）、gold_finish_20261015/FINAL_DELIVERY_DRAFT.md（§6 第 1 条、§11 L2 段）。
- 本批在通道 A 得到的 TS 候选是 pseudo-saddle（H 主导软模），通道 B 的候选 +15.36 仍是 candidate_only，两者都不能替代 13.36。

## 3 若要重算（需先满足的输入清单）

1. (S)-脯氨酸 + 丙酮 + 苯甲醛的 41 原子体系，CPCM(DMSO)、q0/m1，Gaussian 16 B3LYP/def2SVP + GD3BJ + UltraFine + Tight（与既有批次同口径）。
2. 起点极小值：烯胺（I1）自身 Opt+Freq，0 虚频、117 模；分母必须与 TS 同程序同批。
3. TS：Houk-List 椅式主面进攻，watch pair = 烯胺 β-C(C3)–苯甲醛羰基 C(C6)、C2=C3 π、C6=O5 π；要求恰 1 虚频且虚频模覆盖上述键对（按 (a) 方向、(b) 三份额、(c) 交付三步判定）。
4. 双向 IRC 到两端点（maxpoints 显式给足），两端 Opt+Freq 0 虚频 + CIP 核验（C6 = S、脯氨酸 Cα = S）。
5. 副面 (R) 通道须用同一批日志给出 15.52 的替代值，否则 favors/minor 的选择性结论不外推。

## 4 纪律

- 不把 13.36 当 (S) 的定量答案；不与本轮 G16 数值相减；不因它存在而省略 null。
- 本文件只作登记，不改题源；题源回填由主协调统一落盘。
