# NI5 包 · 缺口边收口状态（2026-10-15 开工；**终态定稿 2026-10-17，见文末 §13**）

> **终态摘要（先读这一块）**
> - **值**：NI5_E1（水溶液 C–N 加成）= **+0.93 kcal/mol**（纯电子能、无 ZPE/热校正；相对本步自身起点 RC-A；E(TS) − E(RC-A) = −286.604225293 − (−286.605711957) = +0.001486664 Eh = +0.9329 kcal/mol；同一批 Gaussian 16 日志内相减）。
> - **硬标注 ①（措辞）**：必须写 **soft-mode-dominated C–N addition saddle**（恰 1 虚频 −164.4792 cm⁻¹、C1–N6 伸缩成分 13.4%、振幅由醛基 H 主导、watch pair 投影 1.62%）。
> - **硬标注 ②（连通性）**：必须写「**受约束单峰(job 923) + 变分自洽（TS 低于受约束峰 0.074 kcal/mol）+ 两端点 0 虚频身份(job 956/958) + 端点松弛补强通过（job 969→RC-A r=3.3215/4.1°/36 模 0 虚频；job 970→加合物 r=1.6410/53.8°/36 模 0 虚频）**」；**严禁**写「IRC 双向到达端点」（IRC job 954 为原生梯度判据每向 1 帧早停）。
> - **口径不确定性保留**：±0.24 kcal/mol（同 R 不同扭转族 0.616），随值一起转述。
> - **引擎**：本机无 ORCA，本步为 **Gaussian 16**（B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight + SCRF=(CPCM,Solvent=Water)）；E2/E3 的 ORCA 5.0.2 值（3.59 / 31.2）不得与本值混减。
> - **交付字节（2026-10-17 终值）**：normal.md `5ba1f04f…` ／ NI5.json `a95ce872…` ／ ai.py `399c0468…` ／ tests/test_benchmark.py `1d4f723b…`；`gen_normal_tasks --check` exit 0（check passed: 10 tasks）、`pytest -k regenerate_identically` exit 0、全量 `pytest tests/test_benchmark.py -q` exit 0（0 F/E、1 skipped）。
> - **接任说明**：本文件由 NI5 接任 Coordinator（2026-10-17）定稿。前几任 session（as_0416b318783f4693 / as_5fe6997c26664fc3 / as_c04a464228e143a7）均因平台进程重启被收尾为 failed，**工作产物全部在盘上、未重算**；下面 §0–§12 为历史记录（含已作废的判定与更正），终态以 §13 为准。

包 Coordinator session: **as_5fe6997c26664fc3**（接班；上级 as_0416b318783f4693 因平台重启 runtime_interrupted 变 failed）
主协调 session: as_a341823c436e47ed ｜ 工作根目录: /home/ly/Cloudra-mechanism-agent

## 0 接手中继（2026-10-15 18:4x，平台 API 重启风险期间写；继承人先读本节）
- **本包在飞（手工，priority 应按 0）**：job **923** = `ts/scan02_inner_C1N6/scan02_inner_C1N6.gjf`（sha256 `f6ea803a7935d3017a76356e54dc247b9a6a12e4c46130ad860d5befb54b7444`，8c/10240MB，`B 1 6 S 16 0.099998` = 1.6413→3.2413 Å，17 点，起点 = 902 末帧）；job **926** = `seeds/spec_CH2O/spec_CH2O.gjf`（8c/10240MB）。无 ts_prepare 自动作业。
- **可直接引用的已知数值**（全部本批 Gaussian 16，同法；sha 见 §3）：
  - 902 加合物（= E1 终点 = E2 起点同超面）：E = **-286.613531375 Eh**，0 虚频，r(C–N)=1.6413 / r(C–O)=1.2968 / 水双向氢键；末帧 xyz sha256 `11474dff…`。
  - 909：同物种**另一构象**，E = -286.612267390 Eh（+0.793 kcal），0 虚频。
  - 914 收敛态剖面（口径：`Optimization completed.` 前紧邻的 `SCF Done`）：3.1496 = -286.605325567 / 3.3496 = -286.605703511（**浅凹 −0.237**）/ 3.5496 = -286.605254172 / 3.7496 = -286.604385105 / 3.9496 = -286.603372588 / 4.1496 = -286.602365200 / 4.3496 = -286.601432704 / 4.5496 = -286.600689561（kcal/mol 相对点 1：0 / −0.237 / +0.045 / +0.590 / +1.226 / +1.858 / +2.443 / +2.909）；点 9（4.7496 Å）failed。
  - **关键观察（explorer 只读复核）**：3.3496 Å 收敛态几何是**加成前氢键/离子–偶极络合物**（C=O 1.2137、C–N 3.3496、六元环接力完整、双双近线性氢键），浅凹仅 0.24–0.28 kcal/mol ≈ 该 C–N 软模 ZPE（~0.22 kcal）→ **"勉强束缚"的极浅 RC 候选**。
- **分支判据（等 923 结果）**：① 内区 1.64→3.14 Å 若单调升 ⇒ 3.15–3.35 Å 之间必存在**局部极大**（= C–N 加成 TS 初猜）；② **重叠自检**：923 的 3.2413 Å 收敛态应 ≈ -286.60550 Ha（±0.0002）；偏离 >0.3 kcal/mol ⇒ 两次扫描不同分支、不可拼接；③ **P2**【关键路径】以 914 的 3.3496 Å 收敛态几何做无约束 Opt+Freq：**0 虚频 → 真 RC 成立**（可进 ts_prepare 的 reactant 端点）；**滑落 → 本级别无加成前极小值**（缺测 + 裁决）；**1 虚频 → 可能是"络合物↔加合物"的松散外层鞍点**（若虚频模以 C–N 为主，可作另一个 TS 初猜，勿与 ③ 混淆）；④ **P3** 细网格 3.00–3.50 Å（≤0.05 Å）定位极大并取峰 xyz；⑤ **P4**（补强）其余分离组分与其它拓扑 Opt+Freq。
- **继承人下一步**：a) 按 §3/§4 口径复核 923/P2/P3 的**原生日志**（含 3.2413 Å 重叠自检）；b) **有真 RC + 内峰** → 按 `notes/TS_PREPARE_DRAFT.json`（reaction_center=[[1,6]] 已核）启动 durable ts_prepare 全链（TS 1 虚频+watch pair、IRC 双向、两端点 Opt+Freq）；**无 RC/无内峰** → 按 BRIEF §4 交缺测 + 把 §7 的 (a)/(b)/(c) 裁决问题上交主协调；c) normal.md I5 行脚注更正 + 重跑生成器与守卫（基线：`gen_normal_tasks --check` = "check passed: 10 tasks"、`pytest -k regenerate_identically` = 4 passed，均在本包任何改动前测得）。
- **协作方**：small_mol as_9240d61bec654989（唯一 QM 提交者）、explorer as_6b520c684f5548ea（只读复核，无写权限，产出走 hub）。

## 1 边级状态

| 边 | 溶剂/电荷/重数 | 状态 | 值 (kcal/mol) | 证据 |
|---|---|---|---|---|
| NI5_E1 (C–N 加成 → 两性离子) | CPCM(Water)/0/1 | **进行中**：产物侧 0 虚频极小值已成立；**加成前极小值/独立鞍点尚未判定**（内区松弛扫描在跑） | —（未回填，不填 0） | 见 §3 |
| NI5_E2 (六元环水接力双质子转移) | CPCM(Water)/0/1 | 已有关数值，**不重算/不改动** | 3.59（ORCA） | 题源 ai.py I5 / NI5.json |
| NI5_E3 (水接力脱水) | CPCM(Water)/0/1 | 已有关数值，**不重算/不改动** | 31.2（ORCA） | 题源 ai.py I5 / NI5.json |

> 计算完成 ≠ 验收通过。本表"状态"列只描述证据状态。

## 2 口径（终报必须显式转述）
- **引擎**：本机无 ORCA，统一 Gaussian 16（/home/ly/g16/g16）：`B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight + SCRF=(CPCM,Solvent=Water)`。
- **模型**：题面为 schematic SMILES（接力水与酸不画进反应物侧）→ 实际参与物种 = CH2O + CH3NH2 + **1 分子接力水**（14 原子，q0/m1，闭壳层）。理由：E2 的 3.59 相对"加成中间体·H2O"极小值、且 E2 声明为六元环水接力，故显式水在 E1 起点即须存在。
- **能垒口径**：纯电子能差（无 ZPE/热校正），相对**本步自身起点的极小值**。**G16 与旧 ORCA 值绝不混减**；E1 的 E2 终点必须与 E2 起点同物种（两性离子·H2O）。
- 原子序（RC 输入序，全 H）：1=C(羰基 C，题源 map1)、2=O(map2)、3,4=H(甲醛)、5=C(甲基，map4)、6=N(胺 N，map3)、7–9=H(甲基)、10,11=N–H(map5,6)、12=O(水)、13,14=水 H。任务书"C1–N6"= 序号 1 与 6 = 题源 map1 与 map3；reaction_center=[[1,6]]。

## 3 已确证事实（原生日志，只读）

### 3.1 job 902 — "RC 候选"无约束 Opt+Freq（**滑落**）
- 日志（绝对路径）：`/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NI5/rc/job01_rc_optfreq/rc_optfreq_m13.log`
  - sha256 = `e82ba58586b95764240844bc3ed60fc9484c63b616a35cf062d46bf0824d4eb9`
- 输入：rc/job01_rc_optfreq/rc_optfreq_m13.gjf；起点几何 rc/build/assembly/complex_candidate_002.xyz（r(C1···N6)=3.1496 Å，六元环水接力拓扑）；12 cpus / 13312 MB；q0/m1。
- 关键量：normal termination；opt 收敛；36 个频率**全为正值（0 虚频）**；末条 SCF Done **E = -286.613531375 Eh**（行 18282/19092）。
- **几何核验**：r(C1–N6)=1.641 Å（C–N 已成键）、r(C1–O2)=1.297 Å（C–O 单键）、O2···H13=1.597 Å、O12–H13=1.018 Å、O12···H10=1.864 Å，N 四配位、O2 上无 H → **该极小值是"两性离子·H2O"加合物，不是加成前络合物**。
- 含义：以 candidate_002（r=3.15 Å）为起点、无约束优化一路下坡成键（轨迹约 -11.9 kcal/mol，无上坡特征步）。**不能证明鞍点不存在**，只说明该起点不在加成前络合物盆内。
- 末帧 xyz（同序）：rc/job01_rc_optfreq/rc_optfreq_m13_last.xyz，sha256 = `11474dff0e6d18ac3f8fa9fe61b968963f25606367ea7aef7b72cc8666285032`

### 3.2 job 909 — 加成中间体 Opt+Freq（done）
- 日志：`.../NI5/intermediate/job02_zwitterion_optfreq/zwitterion_optfreq_m13.log`
  - sha256 = `f50c3b8076584e51345eebbc005d6474d0de8a41717b1d03a141aca0372f9c7a`
- 输入：.../zwitterion_optfreq_m13.gjf（sha256 `112dfae550ef9ccc6f43f0b2d2c659c6b0c19baf628e83f537fcc19cd2742001`）；12 cpus / 13312 MB；q0/m1。
- 关键量：normal termination；opt 收敛；36 个频率 **0 虚频**；E = **-286.612267390 Eh**。
- **判读（explorer 复核，待其对账表）**：与 902 **同一物种的另一构象**，比 902 高 **0.793 kcal/mol**。→ **E1 终点无需重算**；E1 终点取更低者（902 末帧），它与 E2 起点同超面。

### 3.3 job 914 — C1–N6 上行松弛扫描（**failed，已封顶，不重投**）
- 日志：`.../NI5/ts/scan01_C1N6/scan01_up_C1N6.log` sha256 = `4bca52fa38168c9eab4def118f52c57f44329025faedfbaca3f8a627243eeac9`
- 输入：.../scan01_up_C1N6.gjf sha256 = `db077c996a46f9e186337d5ddb792708fbb612277c0502a7b8f5538f45bcadfd`（`B 1 6 S 10 0.200000`，3.1496→5.1496 Å；`opt=(modredundant,maxstep=10)` 为 ts_guess 生成默认）
- 终态：**calculator 退出码 1；Error termination via Lnk1e in l9999.exe**（原生行 39686/39687）；点 1–8 收敛，点 9（4.7496 Å）报 `Number of steps exceeded, NStep= 58`（原生行 39411）。
- **逐点能量（口径已裁定 2026-10-15；协调者先前那一组作废）**：relaxed scan 的可引用值是**每个扫描点的收敛态** = `Optimization completed.` 前紧邻的那条 `SCF Done`（其几何的 R(1,6) 即该点扫描值）。协调者先报的 8 个数（-286.605427601 … -286.600071272）实为**下一个点的刚性位移"入口几何"能量**，整体错位一格 → **作废**。我已行级复核 explorer 的裁定：行 10398 `SCF Done -286.605325567` 紧接行 10525 `Optimization completed.`（`R4 R(1,6)=3.1496`）；行 10738 `-286.605427601` 出现在行 10649 的 3.3496 Å 入口几何之后、行 10772 `scan point 2` 之前。
  - **收敛态（可引用，Eh）**：3.1496 = -286.605325567（行 10398）/ 3.3496 = -286.605703511（行 15183）/ 3.5496 = -286.605254172（行 16601）/ 3.7496 = -286.604385105（行 18530）/ 3.9496 = -286.603372588（行 19663）/ 4.1496 = -286.602365200（行 20798）/ 4.3496 = -286.601432704（行 22198）/ 4.5496 = -286.600689561（行 23612）
  - 相对点 1（kcal/mol）= 0.000 / **−0.237** / +0.045 / +0.590 / +1.226 / +1.858 / +2.443 / +2.909 → **3.3496 Å 处有 ~0.24 kcal/mol 浅凹**，3.15–4.55 Å **无极大**；点 9（4.7496 Å）无收敛态（NStep=58 超限失败）。
  - 参照（仅解释用、不作证据）：入口（刚性位移）态相对点 1 收敛态 = −0.064 / +0.115 / +0.645 / +1.263 / +1.900 / +2.484 / +2.963 / +3.297 kcal/mol（行 10738/15522/16930/18865/19992/21127/22529/23941）。
- **判读**：UP 段（3.15–4.55 Å）**无极大**，但 3.35 Å 有 ~0.24 kcal/mol 浅凹（0.2 Å 步长下分辨率有限）；**1.64–3.15 Å 仍未覆盖（job 923 在跑）**。若内区扫描自 1.64 Å 单调升到 ~3.15 Å，则 3.15–3.35 Å 之间必存在局部极大 → 需细网格定位，并判定 3.35 Å 浅凹是否为**真实 0 虚频极小值**（RC 候选，见 §4.1b）。

## 4 在跑 / 待做（决策路径）
新 small_mol = **as_9240d61bec654989**（本包唯一 QM 提交者，8c/≤10240 MB，≤2 并发）：
1. **【关键路径】内区松弛扫描**：自 902 末帧（r(C1–N6)=1.641 Å）沿 B 1 6 上行至 ~3.2 Å（1.6–2.6 Å 窗口步长 ≤0.1 Å）→ 判定有无内峰；有峰则给出峰的 r/峰高/真实 xyz 帧。job 923（ts/scan02_inner_C1N6/scan02_inner_C1N6.gjf，sha256 `f6ea803a7935d3017a76356e54dc247b9a6a12e4c46130ad860d5befb54b7444`，8c/10240MB）= 已提交（ready）。
1b. **【关键路径·RC 极小值判定】** 以 914 扫描 **3.3496 Å 收敛态几何**（该点在 relaxed profile 上是局部浅凹、且垂直方向已优化 → 天然候选驻点）为种子做**无约束 Opt+Freq**（同法同批）：0 虚频 → 存在真实加成前极小值（RC 候选，可作 ts_prepare 的 reactant 端点）；滑落到两性离子·H₂O → 本级别无加成前极小值。输入需自行从 914 日志的 `Standard orientation` 块（行 15094 起，R(1,6)=3.3496）导出为 xyz，并在新目录提交。
2. 分离反应物参考态：seeds/spec_CH2O、spec_CH3NH2、spec_H2O 各 Opt+Freq（同批同法，0 虚频）→ 14 原子配平的渐近能量和。
3. 加成前络合物存在性：rc/job03_cand000、job04_cand001、job06_cand005（必要时 job05/job07）无约束 Opt+Freq → 是否停在 0 虚频加成前极小值，或滑落到 902 那个加合物。
4. **仅在**"真实加成前极小值 + 扫描内峰"同时成立时，才走 durable **ts_prepare** 全链（notes/TS_PREPARE_DRAFT.json 填实；TS 1 虚频 + watch pair 占比 + IRC 双向 + 两端点 Opt+Freq）。
   TS/IRC **只走 ts_prepare/ts_resume**（手工提交被禁用）。

## 5 交付级 caveat（必须随终报转述）
- E2 = 3.59、E3 = 31.2 是 2026-10-02 前 **ORCA 5.0.2** 基线值（normal.md I5 行记载 TS 476 / 中间体 478 / 羟胺复合物 440 / TS 421），其原生日志**不在本工作区** → "本轮 G16 中间体与旧 ORCA 基线是否同一构象/同一水位置"无法本地核验；本包不为对齐而改物种。**跨程序绝对值不得混减。**
- **#178（平台级，已由主协调登记）**：`cloudra/benchmark/integrity.py:_species_file_qualities` 要求证据 `smiles:` 注释的 dot 组分个数 == 图节点 smiles 组分个数，否则节点 quality=0 → 该边能垒"不可从证据推导"。本题实例：参考图 `NI5_R` = `C=O.CN`（2 组分），而真实模型证据注释为 `C=O.CN.O`（3 组分）。**建议**（不实施）：交付图与证据注释统一用含 1 显式水的 dot-joined SMILES。本包不改参考图、不改平台代码。
- 基线（本包任何改动前）：`python -m cloudra.benchmark.gen_normal_tasks --check` = "check passed: 10 tasks"；`pytest tests/test_benchmark.py -k regenerate_identically -q` = 4 passed。**无预先存在 mismatch。**

## 6 文献锚点（explorer，只读；用于 md 归属更正）
- **Hall & Smith 1998**（JPCA 102, 4930, DOI 10.1021/jp9810825）：**26.7 kcal/mol = 羟胺 → 亚胺（分子内 PT/脱水）步**；**加成 → 羟胺（经两性离子）= 14.7 kJ/mol = 3.5 kcal/mol**（G2(MP2,SVP)、气相、2 显式水、相对 MA+FA+2H₂O 复合物、电子能）。该文摘要未给 C–N 成键步单独垒值。
- 26.7 的第二出处（Liao 2007, DOI 10.1021/jp070130v）同样是 **1,3-质子转移步**，不是加成步。
- Boz 2018（DOI 10.1039/c8ra08135b）：中性介质加成 "in a barrierless process"、相对复合物 ~3 kcal/mol；Louie 2015（DOI 10.1021/acs.jpca.5b04887）：单水催化二甲胺加成的 TS 在分离反应物**之下 5.4 kcal/mol**（沉没垒），无水裸反应 20.1。
- **界限**：文献**没有**"加成与 PT 耦合故无独立鞍点"的原文；若本包结论为"无独立鞍点"，那是**我们自己的计算结果**，不得写成文献结论。
- **已批准更正**（LEDGER 2026-10-15 追加裁定 3）：normal.md I5 行把 26.7 错挂在加成步语境 → 改为"26.7 属脱水步、加成步锚 3.5"；限改该行文字，不改数值/SMILES/图；改后必须重跑生成器 + regenerate_identically 守卫并留证。

## 7 待裁决（不自行选）
若确认"本级别无加成前极小值、无独立鞍点"，请主协调/用户裁定：
(a) 记**缺测**（BRIEF §4：写缺什么 + 已证伪什么，不填 0）；
(b) 改用**分离反应物参考态**报沉没垒（Louie 2015 惯例；证据见 §4.2；但与题面"从预反应复合物起"冲突）；
(c) 视为 **E1/E2 图问题**（合并边/改图）。
另：#178 参考图是否补 1 个显式接力水（仅建议）。

## 8 资源纪律
- 本包同刻 ≤2 个 QM 作业；单作业 8 cpus / ≤10240 MB（上限 12 cpus / ≤14000 MB）；提交前查队列防撞；作业目录独立。
- 不改写原生日志；能量只在本批 Gaussian 内相减；不混 ORCA；不提交 git；不改题源图/平台代码；不杀别人作业。

## 9 下一步
1. 等内区松弛扫描 → 定分支（内峰 → ts_prepare 全链；无内峰 → §7 裁决请求 + 缺测登记）。
2. 回填轮：按批准改 normal.md I5 行文献归属 → 重跑 gen_normal_tasks + regenerate_identically 守卫 → 留证。
3. 更新本文件终稿 + hub 终态帖。

## 10 E1 道执行会话进展（small_mol 执行会话 as_9240d61bec654989，2026-10-15 18:5x 落盘）

### 10.1 在飞作业（等 DB 锁修复后队列恢复）
- **job 923** = 内区上行松弛扫描：输入 `ts/scan02_inner_C1N6/scan02_inner_C1N6.gjf`
  sha256 = f6ea803a7935d3017a76356e54dc247b9a6a12e4c46130ad860d5befb54b7444
  （路由 `opt=(modredundant,maxstep=10) B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=Water)`；
  扫描行 `B 1 6 S 16 0.099998`，R(C1–N6) 1.6413→3.2413 Å；起点 = 902 末帧）；8 cpus / 10240 MB；priority 0；提交时 state=ready（排队）。
- **job 926** = seeds/spec_CH2O Opt+Freq（sha256 6cc08f02eea102b7278c1831c98b77465390b647ea00815ad231315d56990bce）；8c/10240MB；priority 0；排队。
- 手工在飞 = 2（到 2026-10-15 18:5x 仍卡在 917/918/921/930 幻影行之后：队列 923(1)/924(2)/925(3)/926(4)/927(5)/928(6)/929(7)/931(8)）。
- 待提交（空槽即提，关键路径优先）：**P2 = rc/job08_well_3496/job08_well_3496_optfreq.gjf**
  sha256 = e00826dc13e897ef934c6f7cae242b17e842f43da0e4447a7dfb65821fcdf3c6（8c/10GB，同法同批）。

### 10.2 新证据：加成前络合物已现形（914 扫描第 2 点收敛帧）
- 来源：`ts/scan01_C1N6/scan01_up_C1N6.log`（sha256 4bca52fa…eeac9）第 53 帧，E = **-286.605703511 Eh**
  （与原生行 15183 的 SCF Done 一致；该帧即 scan point 2 / R(1,6)=3.3496 Å 的收敛几何）；
  经 `scan01_up_C1N6_frames.csv`（format_converter log→csv，142 帧）取出。
- 落盘：`rc/job08_well_3496/well_3496_seed.xyz` sha256 = b78c56f4d854f9f82d4377a6e1457d2ad83d5f53b7564257296b52bc64e79ecd
- internal_coordinates 复核：C2H9NO2 / 14 原子 / **3 片段**；r(C1–O2)=**1.214 Å（键级 2，C=O）**；r(C1–N6)=**3.350 Å（far，未成键）**；
  N6 中性（C5 1.458、H10 1.026、H11 1.021）；水接力氢键 O2···H13 1.842（forming_candidate）、O12···H10 2.058。
  → **即题面定义的 RC 物种（CH2O + CH3NH2 + 1 显式接力水、无质子转移）**；该点在受约束优化中收敛，收敛时 -DE/DX = -0.0003（沿 R 梯度≈0），
  且 E(R) 在 3.1496 / 3.5496 两侧都更高 ⇒ **强烈提示真实极小值盆**，只差无约束 Opt+Freq 的频率判定（= 上方 P2）。
- **若 P2 得 0 虚频**：加成前极小值 E = -286.605703511 Eh（比 902 两性离子·H₂O 高 **4.91 kcal/mol**，本批 Gaussian 内相减）。

### 10.3 §4.1b 与 P3 的两点更正（务必按此执行）
1. **起点几何不必手抄**：STATUS §4.1b 原写"自行从 914 日志 Standard orientation 块导出 xyz" → 已改为用上述 CSV 第 53 帧，
   已落盘并复核（上 §10.2），无需再解析坐标块。
2. **P3 极大位置更正**：修正后剖面中 3.1496 Å 收敛态 -DE/DX = **+0.0024** ⇒ dE/dR < 0 ⇒ **3.1496 Å 不是极大点**（3.3496 Å 更低 −0.237 kcal）。
   因此"3.15–3.35 Å 之间有极大"与实测梯度相反：**极大若存在只能在 (1.64, 3.15) Å 内**（加合物 R=1.641 比 3.1496 低 5.15 kcal/mol）。
   job 923 正好覆盖该区间；3.00–3.50 Å ≤0.05 Å 细网格**只在 923 把峰定在靠上端时**才需要。

### 10.4 工具面缺口（只报不改，供主协调决定是否提 issue）
- `ts_guess(scan_parse)` 对 **914** 直接失败：`No 'Summary of ... Potential Surface Scan' table found in the log`
  → 未跑到结尾摘要表的（中断）扫描日志无法用该工具分析；本次改用 `awk '/Step number/{sp=$0} /SCF Done/{e=$5} /Optimization completed/{print NR,e,sp}'` 逐点解析。
- **无"导出任意指定帧为 xyz"的入口**（format_converter log→xyz 只给末帧；log→csv 有全帧坐标但无 csv→xyz）→ 本次把第 53 帧坐标从 CSV 逐字拷贝写入 xyz，
  write 工具报 `[Warning: suspected handwritten coordinates]`（坐标非凭记忆、已由 internal_coordinates 独立复核，但属架构面缺口）。
- `agent_hub(action="call")` 对 coordinator 会话被拒：`[dispatch rejected] Delegation would grant permissions absent from the caller: manage` → 改用 topic 帖回复。

### 10.5 接班/续跑指引（若本会话被中断）
- 先读 `notes/EVIDENCE.md`（含 902/909 身份对照、914 逐点更正、P2 起点 provenance）与本文件 §10。
- 恢复后第一步：`query_compute_queue` 看 923/926 是否已被 adopt 收尾；923 终态 → 用 §10.4 的 awk 逐点取收敛态能量与 R(1,6)，判定有无内峰
  （有峰：从收敛帧取峰几何作 ts_prepare 的 provided guess；无峰：按 BRIEF §4 登记缺测）。
  然后按 空槽顺序：P2（job08）→ P4（spec_CH3NH2、spec_H2O、rc/job03、job04、job06）。
- 纪律：手工作业 priority 0、每包 ≤2（含排队）；不改写原生日志；能量只在本批 Gaussian 内相减；不填 0、不改图、不提交 git。

## 11 内峰确认 + ts_prepare 全链启动（small_mol as_9240d61bec654989，2026-10-15 晚）

### 11.1 决策链两个前置条件均已成立
- **① 真实 0 虚频加成前极小值 RC**：job 932（rc/job08_well_3496/）0 虚频，E = -286.605711743 Eh（比 902 高 4.907 kcal/mol）。
- **② 内区松弛扫描有内峰**：job 923（ts/scan02_inner_C1N6/，normal termination）17 点，E 单调升到 **p16 R=3.1413 Å（-286.604343399）**，
  p17 R=3.2413 Å 回落 0.81 kcal/mol（-DE/DX 由 -0.0025 变 +0.0012）⇒ **内峰在 R∈(3.1413, 3.2413) Å**；
  峰高（受约束剖面）相对 902 加合物端点 **+5.767 kcal/mol**，相对 RC 极小值 **≥+0.859 kcal/mol**。
  日志 sha256 10a2b71e…d5346；峰帧 `ts/scan02_inner_C1N6/scan02_peak_candidate.xyz` sha256 f9db2f8c…bb42（真实 artifact）。

### 11.2 ts_prepare run ts_0006（自动推进）
- run_dir `/home/ly/Cloudra-mechanism-agent/ts/ts_0006`；启动 revision 4 → 现 revision 8 / status=waiting / stage=build；
  在跑 job 937 `candidate_opt`（8c/10000MB）。
- reaction `C=O.CN.O` → `C[NH2+]C[O-].O`，q0/m1/closed_shell，reaction_center=[[1,6]]，atom_map=[1..14]；
  reactant = rc/job08_well_3496/job08_well_3496_optfreq_last.xyz（413752ab…）+ 其日志；product = rc/job01_rc_optfreq/rc_optfreq_m13_last.xyz（11474dff…）+ 902 日志；
  guess = provided = scan02_peak_candidate.xyz + 923 日志；各阶段 {ref: dft} = gaussian/B3LYP/def2SVP + EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=Water)。
- 首版声明带 mol_path（ASE xyz→mol 只有原子+坐标、无键）→ build 阶段 input_identity_unconfirmed（C.C.N.O.O.[HH]×9）；
  已用 `ts_resume(ts_0006, reason='drop mol_path …')` 改 xyz-only 通过。**属输入/工具诊断，不是科学限制。**

### 11.3 作业台账增量（本批）
| job | 目的 | 目录/文件 | 状态 |
|---|---|---|---|
| 923 | 内区上行松弛扫描 | ts/scan02_inner_C1N6/scan02_inner_C1N6.gjf | **done**（有内峰） |
| 926 | spec_CH2O Opt+Freq | seeds/spec_CH2O/ | done：E=-114.421603513，6 模 0 虚频 |
| 932 | RC 浅凹无约束 Opt+Freq | rc/job08_well_3496/ | done：**0 虚频**，E=-286.605711743 |
| 935 | spec_CH3NH2 Opt+Freq | seeds/spec_CH3NH2/ | done：E=-95.7931237609，15 模 0 虚频 |
| 937 | ts_0006 build candidate_opt | ts/ts_0006/jobs/declaration_0002/ | running（管线） |
| 938 | spec_H2O Opt+Freq | seeds/spec_H2O/ | ready（排队） |
| 939 | rc/job03_cand000 Opt+Freq | rc/job03_cand000/ | ready（排队） |



## 12 ★ NI5_E1 终态（2026-10-15 晚，small_mol as_9240d61bec654989）

**状态：关键路径完成，ts_prepare 全链 verified=true；数值待主协调裁决参考态与「虚频模占比」口径后回填。**

| 项 | 结果 |
|---|---|
| 鞍点是否存在 | **存在**：受约束内区扫描有内峰（R≈3.20 Å），durable 链给出 1 阶鞍点 |
| TS | job 952（`ts/ts_0006/jobs/declaration_0005/ts_opt/refine.log`，sha256 8a3a3c98…），E = **-286.604225293 Eh**；r(C1···N6)=3.125 Å |
| TS 频率 | job 953（…/frequency/frequency.log，sha256 28983faf…）：**恰 1 虚频 = -164.4792 cm⁻¹**；**heavy_atom_fraction=0.033、watch pair (1,6) 占 pair-projected 位移 1.6%（偏离 BRIEF §4 第 1 条）** |
| IRC | job 954（…/irc/irc.log，sha256 f56ea883…）：native `irc=calcfc`（maxpoints=10、step 0.1 bohr）**在每向第 1 点即按原生判据停止**（rx ∈ [-0.11931,+0.11932]），双向几何分别优化到两个端点 |
| 端点 A（RC） | jobs 955/956：E = **-286.605711957 Eh**、36 模 **0 虚频**（= job 932 的 RC-A，差 2.1e-7 Eh） |
| 端点 B（加合物） | jobs 957/958：E = **-286.613531483 Eh**、36 模 **0 虚频**（= job 902，差 1.1e-7 Eh） |
| **ΔE‡（相对该步自身起点 RC-A）** | **+0.93 kcal/mol**（0.001486664 Eh；纯电子能；本批 Gaussian 内相减；不含 ZPE） |
| 步反应能 | **-4.91 kcal/mol**（放热） |
| 相对三分离碎片 | TS -15.05 / RC -15.99 / 加合物 -20.89 kcal/mol ⇒ **沉没垒** |
| 其它加成前极小值 | RC-B（开链，-286.610034975，jobs 939=943 同一）比 RC-A 低 2.713；RC-C（半成键 2.06 Å，-286.608664920，job 947）低 1.853。若以 RC-B 为参考且鞍点相同（**未测**）ΔE‡ = +3.65 kcal/mol |

**待裁决要点**：(1) 参考态是 RC-A（题面声明拓扑）还是 RC-B/分离碎片；(2) 虚频模以氢为主（heavy-atom 3.3% / watch pair 1.6%）是否满足 BRIEF §4 第 1 条，或改以"IRC 双向方向证据 + 两端点 0 虚频身份"为准；(3) IRC 原生早停（每向 1 点）是否需用更大步长重跑以增强连接性证据（会新建 revision，可能改变现行 verified 状态）。
**全部证据**：notes/EVIDENCE.md（§902/909 对照、914 更正、P2、923 内区扫描、926/935/938 分离组分、939/943/947 其它拓扑、950/949 细化、ts_0006 全链）；原生日志路径与 sha256 均在文中。
**交付纪律**：未改任何原生日志；能量只在本批 Gaussian 内相减（未与 ORCA E2=3.59 / E3=31.2 混减）；未填 0、未改图、未提交 git。

### 11.4 下一步 / 接班
- 用 `ts_inspect(run_id='ts_0006')` 跟踪：TS 1 虚频（watch pair [[1,6]] 占比）+ IRC 双向 + 两端点 Opt+Freq 0 虚频；
  若管线阻塞（blocked/failed_attempt）→ 用 `ts_resume(ts_0006, changes=..., reason=...)` 修正声明，不手工提交 TS/IRC。
- 938/939 终态 → 逐条记能量/虚频；随后补 rc/job04_cand001、job06_cand005 与 P3 细化（若需）。
- 最终：E1 能垒 = E(TS) - E(RC)（纯电子能，本批 Gaussian 内相减）；缺测/裁决要点按 BRIEF §4 与 §7 出终稿。

---

## 13 终态交付（FINAL · 2026-10-17 · 接任 Coordinator 定稿）

### 13.1 值（唯一终值）
| 边 | 值 | 口径 |
|---|---|---|
| NI5_E1（水溶液 C–N 加成 → 两性离子·H₂O） | **+0.93 kcal/mol** | 纯电子能 ΔE‡，相对**本步自身起点** RC-A；= E(TS) − E(RC-A) = +0.001486664 Eh；同批 Gaussian 16 内相减；不含 ZPE/热校正 |
| NI5_E2 / NI5_E3 | 3.59 / 31.2（**未改动**） | 旧 ORCA 5.0.2 基线，原生日志不在本工作区；**跨程序不得混减** |

### 13.2 证据（原生日志绝对路径 + sha256；本轮实测，日志未改写）
| 用途 | 绝对路径 | sha256 | 关键原生行 / 值 |
|---|---|---|---|
| TS 优化（job 952） | /home/ly/Cloudra-mechanism-agent/ts/ts_0006/jobs/declaration_0005/ts_opt/refine.log | 8a3a3c98554b606071335680f939737a336dd68c3848244329117cc38f8c055d | L3706 `SCF Done: E(RB3LYP) = -286.604225293` |
| TS 频率（job 953） | /home/ly/Cloudra-mechanism-agent/ts/ts_0006/jobs/declaration_0005/frequency/frequency.log | 28983faf81628e3e5f65048c6e29afa9bbc3779a18a5c8ac9977b7d1c9beaedd | L802 `Frequencies -- -164.4792 60.9584 68.0916`（36 模中**唯 1 虚频**） |
| IRC（job 954） | /home/ly/Cloudra-mechanism-agent/ts/ts_0006/jobs/declaration_0005/irc/irc.log | f56ea88312e9567404d63d326b9a9625d0d1bcad30bfe4c3fa27d7d1b73e702b | L1747 `Total number of points: 2` ⇒ 每向 1 帧早停 |
| 端点 A：RC-A Opt+Freq（job 955/956） | /home/ly/Cloudra-mechanism-agent/ts/ts_0006/jobs/declaration_0005/reactant_frequency/reactant_frequency.log | 7bc76f5c7dd684156952cdd6816d5a52bc085f7f0739bd1fd707b3262bc8ab73 | L518 `E(RB3LYP) = -286.605711957`；36 模 **0 虚频**（首行 35.1857，L802） |
| 端点 B：加合物 Opt+Freq（job 957/958） | /home/ly/Cloudra-mechanism-agent/ts/ts_0006/jobs/declaration_0005/product_frequency/product_frequency.log | 28ecf5cac878983823f61fe4a8d08deea758a844c245ebee9ffdb3123fb6e9d6 | L534 `E(RB3LYP) = -286.613531483`；36 模 **0 虚频**（首行 98.2438，L818） |
| 受约束内区单峰扫描（job 923） | /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NI5/ts/scan02_inner_C1N6/scan02_inner_C1N6.log | 10a2b71efead3a4ea57d62f8fd14172611fb3106f6e4b53de8901f3fbd1d5346 | 17 点、R(C1–N6) 1.6413→3.2413 Å，唯一内部极大 p16（R=3.1413） |
| 端点松弛补强 A（job 969：irc_end_a → RC-A） | /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NI5/rc/job09_ircend_a/job09_ircend_a_optfreq.log | 7c90c2188b33ef4981af86bbaa084b4352d5ecf640b9301abb6dd14ddcd3fb75 | 末帧 r(C1–N6)=3.3215 Å、36 模 0 虚频（首行 35.2126）、与 RC-A maxdev 0.0040 Å |
| 端点松弛补强 B（job 970：irc_end_b → 加合物） | /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NI5/rc/job10_ircend_b/job10_ircend_b_optfreq.log | a6f5b82b20d33dfdecc178124a9955265014cd533e603eb2680a8d6a4143457d | 末帧 r(C1–N6)=1.6410 Å、36 模 0 虚频（首行 98.4345）、与加合物 maxdev 0.0025 Å |

**分析/note 件（本包 notes，非原生 QM 日志）**：notes/EVIDENCE.md `259d78406d70d4250fbf077c4da98735b9155230cbabe8169598ece52a8c12d8`；notes/SELFCHECK.md `2768b6e425f902c5429ae52e10e7cf08f4fb09f9cbe4aaea7feab3ae717a4ed6`（独立只读 lane 复算：ΔE‡ = +0.001486450 Eh = **+0.9328 kcal/mol**，与本文件 +0.9329 同值）；notes/IRC_DEEP.md `6c45917a3c57bf45fe554aa1018a78c86060746d1e5f167deb489575bd87a60f`；notes/IRC_ENDPOINT_RELAX.md `35ea3e55722bfc29787bedd07f951efa4c81d854c6fda69aa10554dce54a8462`；notes/explorer_E1_review_20261015.md `eec2fc850c0baf8dd784cb2c5e80a95ed6c1d791b66c496f5be15f2b051579b2`（91 行，explorer 只读复核）；BACKFILL_DRAFT.md `c6822f4b1a5c1cd5db12938b8f3da61cd4a1b88b9db8b0e070a2d43528a59c63`；notes/TS_PREPARE_DRAFT.json `c0b88e3a1bc720203a05bb74fd3c63a49f082c7935e9ad4969e7a58f3cab4599`；notes/PLAN.md `de4e5e0daab0453c759aea029c837d689e4b8a9a8f29d80deaf9e67e3025479d`。
（注：本任务书基线的 BACKFILL_DRAFT.md `bbcb0ad9…` 已被同包后续追加取代，现值为 `c6822f4b…`，内容为上位集。）

### 13.3 两条硬标注（交付文本必须逐字保留）
**① 措辞（不得写成无修饰的 "C–N 加成 TS"）**：
> **soft-mode-dominated C–N addition saddle** —— 1 虚频 **−164.4792 cm⁻¹**；该模与纯 C1–N6 伸缩的质量加权 ｜cos｜ = 0.3657（**C–N 伸缩成分 13.4%**），但振幅主体是**醛基 H3/H4**（|d| 0.584/0.747；重原子占比按 |d| 15.3%、d² 3.31%、m·d² 31.7%），watch pair (1,6) 的 pair-projected 占比仅 **1.62%** ⇒ 属软模主导，**如实标注、不硬当 TS**（偏离 BRIEF §4 第 1 条）。

**② 连通性表述（唯一允许的写法）**：
> 连通性由「**受约束单峰（job 923** 内区松弛扫描沿 r(C1–N6) 1.6413→3.2413 Å 出现单一内部极大）+ **变分自洽（TS 低于受约束峰 0.074 kcal/mol**，区间 0.038–0.086）+ **两端点 0 虚频身份（job 955/956 与 957/958**，各 36 模 0 虚频）+ **端点松弛补强通过（job 969→RC-A r=3.3215 Å/4.1°/36 模 0 虚频；job 970→加合物 r=1.6410 Å/53.8°/36 模 0 虚频）**」支持。
> **严禁**写「IRC 双向到达端点」：IRC（job 954）为原生梯度判据早停（每向 1 点，rx = ±0.119）；且 run 内两端点 Opt+Freq 的 `endpoint_source.json` 记 `kind=species_reference / irc_job_id=null` ⇒ IRC **未**用作连通性证据。

**口径不确定性（随值转述）**：**±0.24 kcal/mol**（同 R 不同扭转族：受约束峰 p16 属加合物型扭转分支，与 RC-A 同族分支在 R=3.14 Å 处相差 **0.616 kcal/mol**，故不排除同 R 存在低于 0.24 kcal/mol 的其它松弛通道）；另参考态敏感性 RC-B −2.713 / RC-C −1.853 kcal/mol（与同一鞍点的连通性**未测，不得相加**）；相对三分离碎片为沉没垒（TS −15.05 / RC −15.99 / 加合物 −20.89）。

### 13.4 证据驱动的机理修订（旧 → 新 + 依据 + 影响面）
1. **参考态：旧「E1 缺测（题面 schematic C=O.CN，无接力水）」→ 新「参考态 = RC-A」**。RC-A 即题面声明的六元接力环拓扑（CH₂O + CH₃NH₂ + 1 分子显式接力水，14 原子 q0/m1），E = **−286.605711957 Eh**、36 模 0 虚频（job 932 / 955-956），对应 gold 图节点 `NI5_R` smiles `C=O.CN.O`。依据：durable 链 ts/ts_0006 的 build/map 绑定（14 原子 concrete 端点）+ job 923 内区扫描 + 端点 A 复核。**影响面**：E1 数值锚定到 RC-A（因此 0.93 = 相对 RC-A，不是相对分离反应物）；E2 起点（两性离子·H₂O，−286.613531483 Eh）与 E2/E3 旧值不受影响。
2. **鞍点资格：标注 pseudo-saddle 风险**。该驻点有 1 虚频且含真实 C–N 分量（13.4%），但模式振幅以醛基 H 为主 ⇒ 按技能口径属**软模主导**，故交付中显式标注为 soft-mode-dominated C–N addition saddle 而**不宣称**已通过 BRIEF §4 第 1 条的"虚频模落在成键重原子"判据。依据：ts_0006 的 verdict 记录（declaration_revision 5：`verified transition state: exactly one imaginary mode (-164.5 cm^-1)…`）+ notes/IRC_DEEP.md 的模分析 + explorer 独立复核（|cos|=0.3657；pair 投影 0.1698；质量加权 2.4–2.5% 为不同归一化，不矛盾）。**影响面**：措辞与 caveat 层，不改值本身；值为"+0.93（相对 RC-A）+ 上述不确定性/标注"。
3. **文献脚注语境更正（normal.md I5 行）**：旧「文献两水辅助 ≈ 26.7」被挂在 **E1 加成步**语境 → 新「**26.7 属羟胺→亚胺的分子内 PT/脱水步**（非 C–N 加成步；G2(MP2,SVP)、气相、2 显式水、相对 MA+FA+2H₂O 复合物、电子能；Hall & Smith 1998 JPCA 102, 4930, DOI 10.1021/jp9810825）；**C–N 加成步的文献锚 = 3.5 kcal/mol**（同篇 complex→羟胺整体最低垒；摘要未给单独成键步垒值；与本处 CPCM(水) 自算口径不可直接相减）」。依据：LEDGER 追加裁定 3（批准）+ explorer 文献复核（notes/EVIDENCE.md §6）；26.7 的第二出处 Liao 2007 亦为 1,3-PT 步。**影响面**：仅该行文字/语境；**未改** 3.59 / 31.2 数值、SMILES、参考图。
4. **本轮追加更正（2026-10-17，格式层，不涉及数值）**：normal.md I5 行内两个 ASCII 竖线（`|cos|`）使该表行解析出 **10 列 vs 表头 8 列**（Markdown 表格被竖线切断），重生成后 **NI5.json 的 `system.elements` 由 [C,H,N,O] 变空、`system.max_heavy_atoms` 由 4 变 null**（题面约束被无声放宽）。已把该处改为全角「｜cos｜」，行内列数复原为 8，重生成后 elements=[C,H,N,O]、max_heavy_atoms=4 复原（NI5.json L23/L29）。**errata（同轮登记，避免两个 sha 并存）**：被取代的中间字节 normal.md `17306467…` → 终值 `5ba1f04f…`；NI5.json `91d27424…` → 终值 `a95ce872…`；**barrier 0.93 / 3.59 / 31.2 三个数值在三个版本中完全一致**（仅元素约束与行文本受影响）。教训：与 CSV 内逗号同理，Markdown 表单元格内的自由文本含 `|` 必须转义或改全角；`regenerate_identically` 守卫**检测不到**这类"md 与 json 同步漂移"（两侧一起漂移）。

### 13.5 守卫（本轮实测原样输出）
```
$ python3 -m cloudra.benchmark.gen_normal_tasks --check
OK NB1: 5 nodes, 2 steps
OK NI1: 5 nodes, 2 steps
OK NI5: 7 nodes, 3 steps
OK NY3: 7 nodes, 3 steps
OK NR1: 9 nodes, 4 steps
OK NU3: 7 nodes, 3 steps
OK NU5: 7 nodes, 3 steps
OK NU6: 5 nodes, 2 steps
OK NQ1: 5 nodes, 2 steps
OK NQ5: 5 nodes, 2 steps
check passed: 10 tasks          # exit=0

$ python3 -m pytest tests/test_benchmark.py -k regenerate_identically -q
....                            [100%]   # 4 passed, exit=0

$ python3 -m pytest tests/test_benchmark.py -k aqueous_imine -q
..                              [100%]   # 2 passed, exit=0

$ python3 -m pytest tests/test_benchmark.py -q
......（全量）  [100%]            # exit=0，0 F/E，1 skipped
```
重生成命令：`python3 -m cloudra.benchmark.gen_normal_tasks`（exit 0，"wrote 10 tasks"）；生成前用 `--out /tmp/ni5gen` 预演并逐文件 `cmp`，确认**只有 NI5.json 变化**，其余 9 个 task json 字节不变（未越界改其它包）。`--only I5` **不可用**（生成器入口对 --only 断言 len(tasks)==10 会抛 AssertionError，属生成器 CLI 限制，非数据问题）。

### 13.6 引擎偏差声明（必须随交付转述）
本机**没有 ORCA**（`which orca` 为空）。本步 NI5_E1 的全部能量/频率/IRC 均为 **Gaussian 16**（/home/ly/g16/g16）：`B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight + SCRF=(CPCM,Solvent=Water)`，q0/m1。既有 gold 口径为 ORCA 5.0.2 B3LYP-D3(BJ)/def2-SVP；泛函/基组/色散/溶剂模型同级而**程序不同**，故：本值只与**本批 Gaussian 16** 的 TS/端点相减；**E2 3.59 / E3 31.2（ORCA）不得与本值混减**（题源 I5 行与 ai.py 注释均已写明）。

### 13.7 ts/ts_0006 运行态记账说明（只读取证；与任务书基线不同，特此登记）
- 任务书基线记 `ts_0006 revision 75 / status=ended / verified=true`。本轮 `ts_inspect(ts_0006)` 实测为：**revision=79、status=running、stage=refine、terminal=null、waiting_for=[]、blocked=null**，且 `next.action=wait_for_system`；队列 **0 running / 0 queued**（无在飞作业）。
- 由 `ts/ts_0006/process.json`（mtime 2026-10-15 23:43，本轮未改动）可核：**declaration_revision 5 的那次尝试**（attempt 4）`refine` 与 `verdict` 阶段均为 **done**，verdict 原文 "verified transition state: exactly one imaginary mode (-164.5 cm^-1), usable IRC geometries from both directions…"，即**科学判定确实落盘**；其后 `declaration_revision 6` 的一次 ts_resume（用途 = 设定 IRC 步长 `irc=(calcfc,stepsize=30,maxpoints=30)`）被平台准入拒绝（⇒ issue #184），resume 的 reason 明写「the run is restored to the previously verified configuration so its verdict and evidence are not left in a blocked state」。当前 top-level `declaration_revision=7 / stage=refine` 属这次回滚后的**记账态**（refine 序列未重新跑完），**不是新的科学失败**。
- **风险与纪律**：任何对 ts_0006 的 `ts_resume` / retry 都可能重跑 refine 序列并**覆盖**上面 13.2 引用的原生日志（sha 会变）。本包**不再触碰该 run**；如需重跑须先冻结/另存证据副本。
- 相应：ai.py 注释里的运行态表述"（revision 75 / status=ended / result.verified=true）"应按本轮实测口径读作"verdict 阶段 verified（declaration_revision 5）；运��态记账后续被一次被拒的 IRC 步长 resume 回滚"。

### 13.8 平台登记（只登记不处置）
- **issue #178 保持开着**（`cloudra/benchmark/integrity.py` 的 `_species_file_qualities` 要求证据 `smiles:` 注释的 dot 组分数 == 图节点 smiles 组分数，否则节点不绑定该边能垒）。**本轮实测补充**：现行 `NI5.json` 的 `gold.mechanism_graph.nodes[0]`（`NI5_R`）smiles 已是 **3 组分 `C=O.CN.O`**，与证据注释 `smiles: C=O.CN.O` **一致**（本包全部 QM 输入标题即此串）；即该缝隙的"NI5 实例"在当前题面字节下**已不成立**（题面 `system.reactants` 仍是 schematic 的 `C=O`+ `CN` 两片段）。**是否关闭 #178 的决定权在主协调**，本包不改平台代码、不改评分规则。
- 本包未发现新的平台/工具面缺口（除 13.4-4 的"md 表内竖线 → 生成物约束漂移"这一**流程**缺陷，已在此登记；`regenerate_identically` 守卫的盲区一并写明）。

### 13.9 边界与未做
- 未改写任何原生日志；能量只在同一批 Gaussian 16 内相减；未填 0、未凭空填值；未改参考图/SMILES、未改评分规则、未改生成器、未改其它包的文件、未提交 git。
- 未重算 NI5_E2/E3（旧 ORCA 值无本机原生日志，无法本地复核；不为对齐而改物种）。
- 未做：RC-B/RC-C 与同一鞍点的连通性（因此禁止把 RC-B 的 −2.713 与 +0.93 相加）；同 R 更低扭转族通道的系统搜索（即 ±0.24 的未测部分）；IRC 更大步长重跑（受 issue #184 限制，且会新建 revision/覆盖证据）。
- 缺测项（如实）：无。

