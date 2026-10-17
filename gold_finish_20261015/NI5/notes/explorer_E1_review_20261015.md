# NI5_E1 · explorer 只读复核与文献锚点（2026-10-15）

- 作者：NI5 包 explorer 会话 as_6b520c684f5548ea（只读；其自身 write 被权限拒绝，故由 NI5 Coordinator 代为落盘并加勘误）
- 原始全文：agent_hub 主题 gold-finish-20261015 帖 evt_fd2f5caabcd2483e
- **协调者勘误（同轮，帖 evt_3a1cf26696194ef3）**：原笔记 §2.1 末行"参数表内没有 R(1,6) → C1···N6 未成键，预反应络合物成立"**不成立**。rc_optfreq_m13.log 第 18940–18958 行末帧 Standard orientation 复算得 r(C1–N6)=1.6413 Å、r(C1–O2)=1.2968 Å、r(O2···H13)=1.5975 Å、r(O12–H13)=1.0177 Å → 该几何是**两性离子·H₂O**（NI5_I1 物种），不是加成前络合物；Gaussian 坐标集来自输入几何（输入 r=3.1496 Å 未成键），坐标表条目缺失不能判定末帧成键。

## 1 文献锚点（文献报道，附 DOI/URL）
| 量 | 值 | 归属步 | 口径 |
|---|---|---|---|
| Hall & Smith 1998, JPCA 102, 4930, DOI 10.1021/jp9810825 | 14.7 kJ/mol = **3.5 kcal/mol** | **加成 → 羟胺（经两性离子）** | G2(MP2,SVP)、气相、**2 显式水**、相对 MA+FA+2H2O 复合物、电子能 |
| 同上 | 111.9 kJ/mol = **26.7 kcal/mol** | **羟胺 → 亚胺（分子内质子转移/脱水）** | 同上 |
| 同上 | 67.9 kJ/mol = 16.2 | 质子化羟胺脱水 | 同上 |
| Louie/Francisco/Verdicchio 2015, JPCA, DOI 10.1021/acs.jpca.5b04887 | TS 低于分离反应物 **5.4 kcal/mol**（沉没垒）；无水裸反应 **20.1** | 单水催化二甲胺 + 甲醛加成 | 级别摘要未声明；垒高次序 NH₃ > 甲胺 > 二甲胺 |
| Ding/Cui/Li 2015, JPCA, DOI 10.1021/acs.jpca.5b02186 | 无数值 | 中性条件得羟胺非 Schiff 碱；"预反应势阱"软化活性垒 | 摘要 |
| Sayer/Jencks 1973/1974/1977（DOI 10.1021/ja00794a600 / 10.1021/ja00833a027 / 10.1021/ja00444a024） | 无数值（正文未取到） | 加成与脱水都受 general acid/base 催化；含两性离子中间体 | 实验动力学 |

**结论**：题源把"文献两水辅助 ≈ 26.7"与 E1（C–N 加成）语境相连属**错位引用**；26.7 属脱水（E3 型）步，加成步的文献锚是 3.5 kcal/mol（两水、气相、高水平）。→ 建议在回填时把该脚注归属改写（不改 E2/E3 数值、不改图）。
**推断（非文献）**：在"1 显式水 + CPCM(Water) + 相对复合物"口径下 E1 预期落在 0–5 kcal/mol（与 E2=3.59 同量级）；取分离反应物参考则可能 ≤0。文献口径与本轮口径（显式水个数、隐式溶剂、色散、程序）不可直接相减。

## 2 验收复核清单（要点，全文见 hub 帖 §2.2）
- Q1 虚频只数 `Frequencies --` 行中的负值；`Low frequencies` 行的负数是刚体模，**不得**计为虚频；报 3N-6 == 频率个数（14 原子 → 36）。
- Q2 虚频模 watch pair 位移占比：在虚频列的 `Atom AN X Y Z` 表按模长算，C 与 N 合计 > 50%；并核 TS 上的 r(C–N) 介于 RC 与中间体之间。
- Q3 IRC 双向：两向帧数、末帧几何与该侧端点 Opt 起始几何一致。
- Q4 两端点 Opt+Freq 0 虚频 + 身份（RC 侧 r(C–N) 大、O 上无 H 转移；中间体侧 [NH2+]、O 无 H）。
- Q5 能量取每条日志**最后一条** `SCF Done`；日志须有 `Normal termination of Gaussian`（本 rc 日志有 2 条）。
- Q6 ΔE‡ = (E_TS − E_起点极小值) × 627.5094740631 kcal/mol，纯电子能，起点 = 本步自身起点。
- Q9 `smiles: <dot-joined SMILES>` 后接空格再接说明（解析取 smiles 后第一个 token）。
- Q10（代码级，重要）：integrity.py `_species_file_qualities` 要求**证据文件 smiles 注释的组分个数 == 图节点 smiles 的组分个数**，不等则跳过 → 节点未绑定 → 该边能垒不可推导；兜底 `_component_union_coverage` 同样要求逐组分个数相等。→ 若交付图 RC 节点写 "C=O.CN" 而证据注释写 "C=O.CN.O"，E1 即使算对也拿不到分。

## 3 口径风险
- R1 引擎：E1 本轮 Gaussian 16，E2/E3 为 ORCA 值；不混减（BRIEF §3 + 主协调确认），终报须写明跨程序。
- R2 题面 schematic SMILES 不含接力水/酸 + Q10 组分绑定 → 建议向主协调报"口径确认"（是否要求交付图与证据统一用含 1 个显式水的 dot-joined SMILES）；**不改题源图**。
- R3 E1 起点必须是含 1 个显式水的 14 原子复合物（与 E2=3.59 的"加成中间体·H₂O"同超面）；若 RC 不能作为干净极小值成立，如实记录。

## 4 explorer 追加答复（帖 evt_1af7e1a4da2f440b，2026-10-15）：加成步是否无垒 / 参考态惯例

### 文献报道（原文句 + DOI）
- Boz/Tüzün/Stein, RSC Adv. 2018, DOI 10.1039/c8ra08135b（OA PMC9088820）：中性介质中先形成 pre-complex，"nucleophilic addition … in a barrierless process"；"pre-complex formation is exergonic by 36 to 42 kcal/mol and the following nucleophilic addition takes place via TS_14 with a small barrier of 3 kcal/mol only"；显式水配位使加成变分步并降垒 6–10；隐式溶剂比气相低约 14。
- Liao/Ding/Yu/Fang/Liu, JPCA 2007, DOI 10.1021/jp070130v（甘氨酸 + 甲醛 + nH₂O）：carbinolamine 生成"small barrier or even barrierless"，而"1,3 proton transfer … barrier is 26.7 kcal/mol relative to the reactant complex when including two water molecules"（**26.7 的第二个出处，同属 1,3-PT/脱水步，非加成步**）。
- Hall & Smith 1998：complex → 羟胺 3.5（两水、气相）；羟胺 → 亚胺 26.7。
- Louie 2015：单水催化二甲胺加成 TS 在分离反应物之下 5.4（沉没垒）；无水裸反应 20.1。
- 本包 G16 证据：14 原子接力络合物无约束优化单调下坡（~11.9 kcal/mol）落入 r(C1–N6)=1.6413 Å、0 虚频的两性离子·H₂O。

**界限**：文献没有"加成步与质子转移耦合、故无独立鞍点"的原文；最强表述是 "barrierless process" / "small barrier or even barrierless"。→ 若我们结论为"本级别无独立鞍点"，那是**我们自己的计算结果**，不得写成文献结论。

### 参考态惯例（文献做法）
1. 复合物是极小值 → 以复合物为参考（Hall & Smith 1998；Liao 2007）。
2. 复合物浅/不存在 → 报相对分离反应物的沉没垒（Louie 2015 的 −5.4）。
3. 两者都给 + 明示复合物稳定化能（Boz 2018：复合物 −36~42、加成 3）。
**不建议**用"固定 r(C–N) 的受约束络合物"作参考（非自由极小值，与评分器要求的 0 虚频极小值绑冲突）。

### explorer 的建议（推断，供裁决）
(a) 首选：若同级别另有一个真正的 14 原子预反应极小值（如开链型 candidate 000/001），用它作 E1 起点，并用 IRC 证明与 TS1 相连；
(b) 若确认本级别无任何 14 原子预反应极小值：报"相对分离反应物（三分量各自极小值之和，14 原子配平）"的沉没垒——与 Louie 2015 做法一致，但与题面"从预反应复合物起"冲突 → 需主协调裁决；
(c) 不建议受约束络合物参考；
(d) 若 (b) 且无鞍点：NI5_TS1 无"恰 1 虚频"日志可绑 → 该边 barrier 不可从证据推导 → 走"缺测 + 已证伪"登记，是否改图由主协调决定。

### 追加证据（explorer 复算，与我的勘误一致）
job 902 末帧：r(C1–N6)=1.6413、r(C1–O2)=1.2968、r(O2···H13)=1.5975、r(O12–H13)=1.0177、r(O12–H14)=0.9682、r(N6–H10)=1.0431、r(N6–H11)=1.0245；角度 O2–H13–O12 = 160.3°（近线性强氢键）、N6–H10···O12 = 143.9°。
→ 该 0 虚频极小值（E = -286.613531375 Ha）即 E2 的起点（加成中间体·H₂O），可直接复用为 I1 证据；但其原子序为 RC 输入序（C1,O2,H3,H4,C5,N6,H7–H11,O12,H13,H14），与 intermediate 构建序（O1,C2,N3,C4,…）不同 → 复用前必须给"日志序号 ↔ 题源 map 号"对照或按同一序重建。

## 附录（explorer 第二轮检索原文，按其主要求原样收录；2026-10-15）

**Q1 加成步是不是（近）无垒 —— 文献报道**
- E. Boz, N. Ş. Tüzün, M. Stein, RSC Adv. 2018, DOI 10.1039/c8ra08135b（OA 全文 PMC9088820）："In neutral media, the aldehyde and the amine form a pre-complex before the nucleophilic addition … occurs **in a barrierless process**."；"pre-complex formation is exergonic by 36 to 42 kcal mol⁻¹ and the following nucleophilic addition takes place via TS_14 with **a small barrier of 3 kcal mol⁻¹ only**."；"**Explicit water coordination** … stepwise rather than concerted … **lower activation barrier by 6–10 kcal mol⁻¹**."；"computed energy barriers in an **implicit solvent** … **lower by 14 kcal mol⁻¹** than in gas phase."
- R.-Z. Liao, W. Ding, J. Yu, W.-H. Fang, R. Liu, J. Phys. Chem. A 2007, DOI 10.1021/jp070130v（甘氨酸+甲醛+nH₂O, n=0,1,2）："the **carbinolamine is formed with small barrier or even barrierless**"；同文 "**26.7 kcal/mol relative to the reactant complex** when including two water molecules" 指的是 **1,3-质子转移**步（第二个"26.7"，与 Hall & Smith 的 111.9 kJ = 26.75 数值巧合，勿混）。
- 界限（重要）：文献里**没有**"加成步与质子转移耦合、因此无独立鞍点"的原文；最强表述只是 "barrierless process"（Boz 2018）/"small barrier or even barrierless"（Liao 2007）。**"本级别无独立鞍点"是本包自己的计算结论，不是文献原话。**
- 转述 Patil & Sunoj（经 Boz 2018 正文，explorer **未取到** Patil & Sunoj 原文）："barrierless nucleophilic attack … an **increase by 5 kcal/mol upon pre-complex formation**"。

**Q2 Hall & Smith 1998 补充**：26.7 = 羟胺→亚胺（分子内 PT/脱水），口径 G2(MP2,SVP)/气相/2 显式水/无隐式溶剂/电子能/相对 MA+FA+2H₂O 复合物；加成对应 14.7 kJ/mol = 3.5 kcal/mol 是 **complex→羟胺（含 C–N 成键 + PT）的整体最低垒**；**该文摘要没有给 C–N 成键步单独的垒值**（正文 ACS 闭源、本机取不到，登记为"未取到"）。

**Q3 参考态惯例（预反应络合物不是干净极小值时）—— 三种可引做法**
1. 以复合物为参考：Hall & Smith "…**above the complex** between methylamine, formaldehyde, and two water molecules"；Liao 2007 "**relative to the reactant complex**"。
2. 以分离反应物为参考、直接报沉没垒：Louie 2015 "the transition state being 5.4 kcal/mol **below the (CH3)2NH + H2CO + H2O separated reactants**"。
3. 两者都给 + 显式给复合物稳定化能：Boz 2018 转述 Patil & Sunoj（见上）。

**追加快照**：job 902 末帧（-286.613531375 Ha、0 虚频）中水的取向正是 E2 的六元环接力拓扑（O⁻···H13–O12···H10–N：1.5975 / 1.0177 / 1.8639 Å，O12–H14=0.9682 Å 为自由 O–H）→ 该极小值同时是 E1 的产物 = E2 的起点（加成中间体·H₂O）。

## 附录 2（explorer 只读复核，2026-10-15 晚）

**1) 内峰帧 p16 与 RC-A 不是同一扭转族（我自算）**：RC-A（job 932）r(C1–N6)=3.3234、A(O2–C1–N6)=104.3°、A(H4–C1–N6)=17.4°、水角 170.5/168.1°、D(O2–C1–N6–H10)=**4.2°**；加合物（job 902）r=1.6413、A(H4–C1–N6)=99.2°、D=**53.7°**；峰帧 p16（scan02_peak_candidate.xyz，r=3.1413）A(H4–C1–N6)=67.6°、D=**53.8°**（= 加合物的扭转）；923 的 p17（3.2413 Å）A(H4–C1–N6)=17.90°、A21=170.74° 才回到 RC-A 族。同 R 两族能量差：3.1413 = -286.604343399（相对 RC-A +0.859）vs 3.1496 = -286.605325567（+0.242，914 收敛态、SCF 行 10398）= **0.616 kcal/mol**。p16 自身 -DE/DX=-0.0025 超 Max Force 判据（5.5×/2.9× 两种单位读法都超）⇒ 不是驻点。`-DE/DX` 符号 = −dE/dR（由 923 的 17 点剖面自洽钉死）。

**2) job 946（declaration_0004 第一次 TS 细化）原生失败**：`Step number 62/62`、`NStep= 62` 用尽、l9999；末步 Maximum Force 0.000369 (YES) / RMS Displacement 0.077604（65× 阈值）= 平坦面振荡，能量停在 -286.6057 平台 ⇒ 初猜/算法失败，**不构成「无鞍点」证据**。

**3) job 952–958（declaration_0005 第二次 TS 链）独立复核**：ts_opt 收敛（E=-286.604225355、r(C1–N6)=3.1251、A(O2–C1–N6)=93.6°、A(H4–C1–N6)=49.9°、D=41.8°，关键角度我手算复核）；frequency 恰 1 虚频 **-164.4792 cm⁻¹**，但**质量加权位移 C1+N6 仅 2.4–2.5%**（醛基 H3/H4 = 0.584/0.747 主导）⇒ 技能口径为 **pseudo-saddle**；IRC `Total number of points: 2`（每向 1 帧、ΔE≈0.006 kcal/mol、末帧 r(C1···N6)=3.134 Å）；**端点证据循环**：declaration_0005 的 reactant_opt/product_opt 的 `endpoint_source.json` 均为 `"kind":"species_reference"、"irc_job_id":null`，source.xyz 自算 r=3.3234 / 1.6413 ⇒ 不是 IRC 连通性证据。若按管线登记：E1 = E(TS) − E(RC-A) = **+0.9329 kcal/mol**。

**4) job 947（rc/job06_cand005）独立复核 = RC-C**：`Stationary point found`(行 28089)、末条 SCF Done **-286.608664920**、36 模 **0 虚频**（最低 69.1738）、末帧 r(C1–N6)=**2.0598 Å**、r(C1–O2)=1.2398、水只捐 H 给醇氧（O2···H14=1.7307；N6···H13=4.055）⇒ 与本级另两个 0 虚频极小值 RC-A/RC-B 拓扑不同。

**5) 待裁决**：(a) 参考态 RC-A / RC-B(−2.713) / RC-C(−1.853) / 分离碎片；(b) BRIEF §4 第 1 条是否要求虚频模落在成键重原子（技能口径：以 H 为主 ⇒ pseudo-saddle，登记未解决）；(c) IRC 是否用更大步长/步数重跑补连接性；(d) 若无法给出可验收的 C–N 鞍点，按「缺测 + 已证伪候选（p16 折叠点不收敛、attempt2 pseudo-saddle、IRC 无下落）」或按「近乎无垒、E1 ≲1 kcal/mol（相对 RC-A）+ 沉没 −15.05（相对分离反应物）」登记并附 RC-B/RC-C caveat。

**6) 文献报道 vs 我的推断（严格分开）**：文献（Hall & Smith 1998 加成锚 3.5，DOI 10.1021/jp9810825；Boz 2018「barrierless」DOI 10.1039/c8ra08135b；Louie 2015 沉没垒 5.4，DOI 10.1021/acs.jpca.5b04887）只支持「小垒/无垒/沉没垒」的定性叙述，**没有**本模型「无独立鞍点」原文；「本级别 C–N 成键无可分辨独立鞍点、只测到松散络合物软模 ≲1 kcal/mol 起伏」是**我的推断**（本批计算结果）。E2=3.59 / E3=31.2（ORCA 旧基线）未动、未混减。
