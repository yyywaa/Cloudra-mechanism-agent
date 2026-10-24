# HL1_E1 鞍点归属补算 · 状态（2026-10-18）

只做 HL1_E1；工作目录 gold_fill_20261018/HL1/HL1_E1/。不动 NR1/NY3/HI1，不改 method_policy / jl.py / HL1.json / hard.md / tests。

## 0. 当前结论（截至 2026-10-18 04:38；覆盖本文件下方任何更早的相反表述）

- **HL1_E1 = 该级别下不可计算**：声明的「肟 O-质子化」产物态在 B3LYP/def2SVP 气相下不是稳定极小值 ⇒ 本步无定义起点；题源保持 **null**。
- **旧「0.0 约定值」口径作废**（更正链 D34→D35→D37→D38→D40→D42→D43）：不得再用「无独立鞍点」作为填 0.0 的理由；**不得填任何 ΔE‡**（含早期的 +3.5683）。
- **鞍点本体合格**：#1093 freq 恰 1 虚频 **−254.4556 cm⁻¹**（sha d4f9171d…，(a) 符号无关形状判定通过，(b) 三份额已登记）。
- **反侧（REV）不是声明反应物**：#1099 双向 IRC 只作方向证据且未达端点；两轮外层 Opt（#1100 = decl_0004、#1101 = rev_outer）都漂到「N-质子化肟 + 水」后以 l103 **FormBX** 失败 ⇒ 逐字「该端未达极小」，**不分类、不给 ΔE‡**。
- **环③ 已完成（真收敛，04:47:00）**：#1102（declaration_0005 reactant_opt，species_reference 独立种子）L18868 Optimization completed. / L18869 Stationary point found、末 SCF −364.334597427（L18666）、19,301 行、sha d010704f…。末帧（几何块 L19045）：**R(H4–N8) = 1.0267**（标准 N–H）、R(O1–H4) = 2.3033（断）、R(O1–H2) = 0.9704（水）、R(O1–O9) = 2.5887（分离）⇒ **O-质子化意图的种子收敛为 N-质子化肟 + 水**。该值比 job 978（−364.326887674）低 4.84 kcal/mol（仅描述，不作 gold）。
- **环④ 已完成（04:49:53，0 虚频）**：#1105 = declaration_0005/reactant_frequency/reactant_frequency.log，sha c5184477…、1968 行；L510 SCF −364.334597427（与 Opt 末帧逐位相同）、`imaginary` 计数 **0**、51 模（3N−6）全部为正（首组 L849 44.4026/59.0952/75.1013）、L1968 Normal termination ⇒ **N-质子化肟+水 是该级别本地极小值**。四环齐备。
- **仍在跑的笛卡尔修法**：#1104（rev_opt2，opt=(cartesian,maxstep=5)，起点 = #1100 末帧 L17301）Step 28/67，未收敛；它的作用是独立复核「反侧确实收敛到同一 N-质子化物种」。
- **本边的两个参照点**（本边体系 = 19 原子 C4H12NO2⁺，本批全部能量在 −364.29… 区间）：产物侧 **B = −364.295965289**（O-质子化产物极小）；「N-质子化肟 + 水」**job 978 = −364.326887674**（另一批次，仅作几何/身份参照，**不相减**）。
- **更正（04:47，D44）**：本节初版误把 HI1_EM1 的对照极小 **job 924 = −939.308218263** 写进本边 §0 —— 那是 41 原子 HI1 体系的值，与本边 19 原子体系无关，**已删除，不得引用**。本边不自行回填，回填由主协调按 BACKFILL_PROPOSAL 决定。

## 1. 已提交（durable run）

- run = **ts_0022**，run_dir = /home/ly/Cloudra-mechanism-agent/ts/ts_0022，revision 11
- 方法（全流程同一口径）：Gaussian 16，B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight，气相，q=+1 / m=1
- reaction_center（1-based 本包序）：break [1,2]、form [2,9]
- guess：gold_finish_20261015/HL1/round4/T3_scan_peak_pt8_ts_guess.xyz（sha256 7018f688…），来源见 [GUESS_PROVENANCE.md](GUESS_PROVENANCE.md)
- TS 优化作业 **job 1084**（opt=(TS,calcfc,noeigen)），输入 ts/ts_0022/jobs/declaration_0001/ts_opt/refine.gjf；日志 ts/ts_0022/jobs/declaration_0001/ts_opt/refine.log
- 后续阶段已声明（同一 run 自动推进）：frequency → IRC（keywords 带 IRC=(MaxPoints=60,StepSize=10)，用于覆盖框架默认 10 点/方向，#184）→ 两端点 Opt+Freq（seed=null，端点取自 IRC）

## 2. 只读剖面分析（尚未参与判定，仅作 guess 背景）

T3_ptscan_H2O9_relaxed.log（sha256 40ce3be2…）逐帧实测（R 单位 Å，E 为受约束弛豫能量）：

| frame | R(H2–O7) | E / Ha | R(1,2) | R(1,9) | R(N6,H4) | 身份 |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1.0774 | −364.29597 | 1.381 | 2.457 | 3.284 | 产物侧 B（O-质子化） |
| 7 (=pt8) | 1.4274 | **−364.29028** | 1.076 | 2.400 | 1.913 | 接触离子对（H3O+ 型 O1） |
| 9 | 1.5274 | −364.29123 | 1.037 | 2.384 | 1.576 | 接触离子对（H4 已在 O1/N6 之间） |
| 10 | 1.5774 | −364.30060 | 0.991 | 2.408 | **1.061** | **N-质子化肟 + 水（换物种）** |
| 19 | 2.0274 | −364.31604 | 0.972 | 2.568 | 1.048 | N-质子化肟 + 水 |

要点：pt8 是 **O-质子化支路**上的内部极大；frame≥10 的「能量下降段」是**另一物种**（质子经 H4 转到 N6），不能当作 O1→O7 通道的下坡。因此 pt8 的 +3.568 kcal/mol（相对 B）只是**受约束剖面上界**，既不是 ΔE‡ 也不是鞍点证据。

## 3. 分析工具

[analyze_mode.py](analyze_mode.py)：解析 Gaussian 频率日志，输出 (a) 虚频模在两个 watch pair 上的 δR 与 û(O1→O7)·d(H2)、以及 (b) 三份额（声明反应中心原子 / 全部重原子 / 最大单原子 + 主分量），不做任何百分比闸门。
已用历史日志 ts/ts_0010/jobs/declaration_0001/frequency/frequency.log 复核：复现 −67.9886 cm⁻¹ 与 H17/18/19 份额 0.222/0.397/0.347、H2 份额 0.0008（≈决策文档的 4% 量级说法）——即历史驻点是产物侧 C3 甲基转动 pseudo-saddle，方向判据在噪声级（δR(1,2)=+0.0007 Å、δR(2,9)=−0.0009 Å），不可采信为「方向通过」。

## 3b. TS 优化结果（job 1084 · done）

- 日志：ts/ts_0022/jobs/declaration_0001/ts_opt/refine.log（1969 行）
  - **L1546–1547** `Optimization completed.` / `-- Stationary point found.`（第 2 步即收敛，L1544 RMS Displacement 0.000004 YES）
  - **L1372** `SCF Done:  E(RB3LYP) =  -364.290279158     A.U.`（末步；guess 帧受约束值 −364.290279321，差 0.0000002 Ha）
  - **L1969** `Normal termination ... Sun Oct 18 03:02:42 2026`
- 收敛几何（L1720 起标准取向块）：R(1,2)=1.0679、R(2,9)=1.4280、R(1,9)=2.3937、R(1,3)=0.9753、R(1,4)=0.9888、
  R(9,16)=0.9765、R(8,9)=1.4448、R(7,8)=1.2653、R(N6,H4)=1.9048 Å
  ⇒ 仍是**接触离子对型（H2 留在 O1 侧、肟 OH 完整）**，与 guess 帧同族；相对产物侧 B（−364.295965289）= +3.5683 kcal/mol。
- **+3.568 与 +3.5705 的口径统一**：本文件与 §2 剖面表用受约束帧值（`gold_finish_20261015/HL1/round4/T3_ptscan_H2O9_relaxed.log` L68443 `Eigenvalues -- -0.29149 -0.29063 -0.29028 -0.29053 -0.29123`，pt8 = **−0.29028**）⇒ ΔE(pt8) − B = **+3.568**；`gold_finish_20261015/HL1` 侧定稿写 **+3.5705**，来自另一取帧（OptTS 收敛能量 −364.290279158）。两者差 0.002 kcal/mol，**都只是受约束剖面上界、不是 ΔE‡、不是鞍点证据**；对外引用统一写 +3.568（受约束帧口径）并注明来源行号。
- **这只是「OptTS 收敛」，不是 TS 判定**：是否有且仅有 1 个沿 [1,2]/[2,9] 的虚频必须由 frequency（job 1086）给。
- 注意：本步能量与 pt8 受约束弛豫值几乎相同（Δ=2×10⁻⁷ Ha）⇒ 该帧在 B3LYP/def2SVP 气相确实非常接近驻点。

## 3c. 资源变更（协调授权，2026-10-18 04:xx）

- 全流程 execution 定为 **cpus=4 / memory_mb=6144**（协调裁决 A，freq→IRC→两端 Opt/Freq 全程不回改 8c）。
- 队列中的 freq 作业 1086（8c，从未起跑）经授权 **ts_stop → ts_resume** 撤回重发：1086 → cancelled；新作业 **1093**（declaration_0003），ts_inspect 读回 req_cpus=4 / req_memory_mb=6144，输入 `%nproc=4`/`%mem=6144MB`，坐标 = job 1084 收敛 TS 几何。
- 平台行为（协调已登记 D11）：ts_resume 的 execution 变更只对**未入队**作业生效；已入队者需 ts_stop→ts_resume 撤单重提（不丢 ts_opt 证据，只丢一次 attempt 记录）。

## 3d. frequency 结果（job 1093 · done）与 (a)(b) 判定

日志 ts/ts_0022/jobs/declaration_0003/frequency/frequency.log，sha256 **d4f9171d2430f18620ef8100c091e632a36a824bc76e57656f60f8c4668f4aad**，1972 行
- L510 `SCF Done: E(RB3LYP) = -364.290279158`；L841 `1 imaginary frequencies`；**L850 `Frequencies -- -254.4556 48.8070 86.3945`**（恰 1 虚频）；末 `Normal termination`；51 模。

**(a) 方向闸门：通过。** 以 −img 为反应正方向：
δR(1,2)=**+0.0207 Å**（拉长，break ✓）、δR(2,9)=**−0.0495 Å**（缩短，form ✓）、û(O1→O7)·d(H2)=**+0.3555**（|d(H2)|=0.4734，cos 0.75）。
振幅比：声明中心最大 |d|=0.4734 vs 全模最大 |d|=0.6875 ⇒ 0.69，**不是噪声级**（对比历史 ts_0010 −67.99 cm⁻¹：+0.0002/−0.0000）。

**(b) 份额（记录项）**：中心对 {1,2,9}=**0.2542**；全部重原子=**0.0512**；最大单原子=**原子 4（H4）0.4739（主分量 y）**。
逐原子：H4 0.474 / H2 0.225 / H3 0.137 / H16 0.091 / O1 0.021 / N6 0.013 / O7 0.008。
归属：H3O+ 给体不对称伸缩 + 质子转移的**真模**（不是甲基转动/水取向），但最大单原子落在声明对之外 ⇒ 按裁决 (b) 如实登记，不套阈值、不标 soft-mode-dominated。

**(c) 尚缺**：双向 IRC 连通性 + 两端 Opt/Freq ⇒ 现为 candidate_only。

## 3e. IRC 平台限制（#184 新证据）

- keywords 里写 `IRC=(MaxPoints=60,StepSize=10)` → **blocked**：`compute_admission_rejected`，expected keywords 含 irc 选项、actual 不含（渲染器固定注入 `irc=calcfc` 并丢弃声明 token）。
- 改写进 `end_setting` → admission 通过，但生成的 ts/ts_0022/jobs/declaration_0004/irc/irc.gjf L4 仍是 `#p irc=calcfc B3LYP/def2SVP empiricaldispersion=gd3bj int(ultrafine) scf=tight` ⇒ **end_setting 也被静默丢弃**。
- 结论：ts_prepare irc 阶段无入口设 MaxPoints/StepSize/算法；1099 只能跑引擎默认（约 10 点/方向）。端点身份改由**两侧外层帧无约束 Opt+Freq** 承担，并如实写「IRC 未达端点」。

## 3f. IRC 结果（job 1099 · done，双向各 10 点 = 引擎默认上限被截断）

日志 ts/ts_0022/jobs/declaration_0004/irc/irc.log，9413 行（sha256 见下条报告）
- L9070–9072 `Maximum number of steps reached.` / `Reaction path calculation complete.`；L9413 `Normal termination`（2026-10-18 04:06:08）。双向各跑满 10 点后停（无 l123、无 Error termination）。

| 侧 | 点 | R(1,2) | R(2,9) | R(1,9) | N6–H4 | N6–H2 | N–O | E / Ha |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TS | — | 1.0756 | 1.4286 | 2.3995 | 1.907 | 2.094 | 1.4665 | −364.290279158 |
| FWD | 0 | 1.0864 | 1.4023 | 2.3955 | 1.945 | 2.075 | 1.4697 | −364.290299 |
| FWD | 5 | 1.1555 | 1.2770 | 2.3784 | 2.128 | 1.999 | 1.4879 | −364.290901 |
| FWD | 9 | 1.2350 | 1.1816 | 2.3764 | 2.264 | 1.961 | 1.5062 | −364.291781 |
| REV | 1 | 1.0563 | 1.4818 | 2.4076 | 1.832 | 2.133 | 1.4600 | −364.290366 |
| REV | 5 | 1.0252 | 1.5982 | 2.4247 | 1.687 | 2.221 | 1.4477 | −364.291121 |
| REV | 10 | 1.0019 | 1.7259 | 2.4432 | **1.549** | 2.316 | 1.4355 | −364.292717 |

读数：
- **FWD = 声明方向**：H2 由 O1 走向 O7（R(1,2) 1.086→1.235 拉长、R(2,9) 1.402→1.182 缩短），单调下坡（−364.29030→−364.29178）。10 点内**还没到 B**（B 的 R(2,9)=1.0774），也未收敛。
- **REV**：H2 回到 O1（1.002），同时 **H4 稳步靠向 N6（1.832→1.549）** ⇒ 反侧确实朝 **N-质子化肟+水**（job 978，−364.326887674）走，而不是「质子留在 O1 的接触离子对」。
- 两侧能量都还在下降、均未达端点 ⇒ **IRC 只提供方向证据，不构成 (c)**（平台默认 maxpoints 截断，#184）。

## 3g. 端点 Opt 第一轮（declaration_0004）：反侧失败但暴露了关键物种

- **job 1100 reactant_opt = failed**（ts/ts_0022/jobs/declaration_0004/reactant_opt/reactant_opt.log，17605 行）：
  L17600–17602 `Bend failed for angle 1 - 4 - 8` / `FormBX had a problem.` / `Error termination via Lnk1e in l103.exe`（2026-10-18 04:26:11）；**无** `Optimization completed`。
  失败原因：反向 IRC 末端帧上 H4 同时桥 O1 与 N6（角度 1-4-8 近线性），冗余内坐标成形失败 —— 与 gold 历史 job 921 同类（`FormBX had a problem`）。
- 但该 opt 已经走完 30 步，末几何（导出 gold_fill_20261018/HL1/HL1_E1/reactant_endpoint_seed_last_frame.xyz，sha256 98d14d55…，opt step=30）**已是 N-质子化肟 + 水**：
  R(1,2)=0.9706、R(2,9)=4.1634、R(1,9)=3.5307、**R(N6,H4)=1.054**、R(8,9)=1.3636、R(7,8)=1.2935、R(9,16)=0.983、片段 2 个（[1,2,3]=水、其余=肟）。
  末步 SCF **E = −364.330446174 Ha**（L17539）⇒ 比 gold job 978 的 N-质子化极小值（−364.326887674）**再低 0.00356 Ha = 2.23 kcal/mol**（同程序同批；不同构象/离子对分离，未做频率，**不得当已验证极小值**）。
- 处置与实况更正（04:30 起）：平台在 #1100 失败后**没有**用该末帧作 seed，而是进到 declaration_0005，用 `species_reference`（`reactant_source.xyz`，sha256 2dc67cb0…，与 IRC 任一帧的最小 RMS = 0.967 Å）作种子起了 **#1102**（`#p opt`，4c/6144）。我另按修法 A 起了 **#1104**：`opt=(cartesian,maxstep=5)`、起点逐字取 #1100 末帧 L17301（输入 gold_fill_20261018/HL1/HL1_E1/irc_endpoints/rev_opt2/rev_opt2_cart.gjf，sha256 f81033c4…，title 里写全来源日志绝对路径 + sha256 337ee933… + L17301 + 失败时刻）。product endpoint 仍由 FORWARD IRC 帧直接优化。

**结论方向（待端点频率确认）**：−254.4556 cm⁻¹ 鞍点的**反侧不是声明反应物（H3O+ + 中性肟），而是 N-质子化肟 + 水**；正侧朝 B（O-质子化产物）走但被截断。


## 3h. 反侧第二轮回调：job 1101 同样 FormBX 失败（复现证据）

- 日志 gold_fill_20261018/HL1/HL1_E1/irc_endpoints/rev_outer/rev_outer_opt_fix1.log，sha256 **fd7450ea711c894ea855437fdc50c63ec0819dcb4e40e1952b1d6dbdcaa12bc5**，11,548 行。
  L11540–11543 `Tors failed for dihedral 2-1-4-8 / 3-1-4-8 / 1-4-8-7 / 1-4-8-9`、L11544 `FormBX had a problem.`、L11545 `Error termination via Lnk1e in l103.exe`（04:29:17）；末 SCF −364.325340665（L11478）；无 Stationary point found。
- 与 #1100 并列（同起点 = IRC REV pt10）：O1–H4 1.6395/1.6677（断）、H4–N8 1.0538/1.0565（成键）、O1···O9 3.5307/3.4746（分离）、O1–H2 0.9706/0.9765、H2···O9 4.1634/3.8880。
- 判读：两条运行都漂到「水 + N-质子化肟」后**因 Z-matrix 内坐标退化**（O1–H4 断键后的弯角/二面角）崩掉 ⇒ 记「该端未达极小（FormBX 内坐标构造失败）」。**这是优化器/内坐标问题，不是「物种不存在」，也不得写成「无极小」或「该边不可算」。**

## 3i. 端点 Opt 仍在跑的两条（04:37 实测）

- **#1102**（ts/ts_0022/jobs/declaration_0005/reactant_opt）：`#p opt`（内坐标），种子 = species_reference `reactant_source.xyz` sha256 2dc67cb0…，与 irc.log 全部 22 个 orientation 块比对最小 RMS 0.967 Å ⇒ **与 #1100/#1101 不同源**。截至 04:36 已 Step 16，末 SCF −364.334396311（L8659）。**同一内坐标风险仍在，若再 FormBX 即弃用。**
- **#1104**（rev_opt2/rev_opt2_cart.gjf）：`#p opt=(cartesian,maxstep=5)`，起点 = #1100 末帧 L17301，输入 sha f81033c4…。截至 04:37 已 Step 11，无 Stationary point found。


## 3j. 平台观察：取消作业后遗留「孤儿 monitor + g16」（2026-10-18 04:4x）

- **现象**（主协调实测）：账本 `running` = 8，但系统里 g16 顶层进程 = 9。多出来的是已 `cancelled` 的 #1089（HI1_E1a 扫描）：`calc-1089.lock` 已不存在、账本已终态，但 monitor 与 g16/l502 仍在跑，已耗 1 h08 m、约 6 核。
- **根因（平台层）**：cancel 流程把账本改终态、清了锁，但 monitor 主循环未退出、calculator 未真正收到 SIGTERM；与「cancel_requested 未被 guard 消费」同族。
- **处置**：主协调按「账本已 cancelled」为前提，依次 TERM guard → TERM calc 进程组 → TERM g16，残留 l502/l103 用 KILL 精确清理；清理后系统 g16 = 8、账本 running = 8，完全对齐。
- **本 lane 的核对规则（已并入巡检）**：任何撤单之后必须比对 `ps -eo args | grep -c '^/home/ly/g16/g16 '` 与账本 running 数；不一致即报主协调。**04:46 实测：ps_g16 = 8，账本 running = 8（1092/1094/1096/1097/1098/1102/1103/1104），无僵尸。**
- 判活补充：#1103 freq 的 `l1110.exe` 348% CPU、Normal/Error termination 计数 0、freq 计算本身不落 scratch（内存计算）⇒ **scratch 空不是判死依据**，与 D20 的四级优先级一致。
## 3h. reactant endpoint（重跑 job 1102 · done，收敛）

日志 ts/ts_0022/jobs/declaration_0005/reactant_opt/reactant_opt.log（19301 行）
- L18868–18869 `Optimization completed.` / `-- Stationary point found.`；L19301 `Normal termination`（2026-10-18 04:47:00）；**无 Bend failed**
- L18666 `SCF Done: E(RB3LYP) = **-364.334597427**`（末步）
- 身份：**N-质子化肟 + 水**，片段 2 个（[1,2,3]=H2O，其余=肟）；R(1,2)=0.9704、R(1,3)=0.970、R(N6,H4)=**1.027**、R(9,16)=0.999、R(1,9)=2.5887、C=N 1.2932、N–O 1.3468
- 该极小值比 gold job 978（−364.326887674）低 0.00771 Ha = 4.84 kcal/mol，比 B（−364.295965289）低 0.03863 Ha = **24.24 kcal/mol**（同程序同批）
- 频率作业 **1105**（4c/6144）正在跑 ⇒ 0 虚频待确认。

⇒ **反向 IRC 侧确认落到 N-质子化肟 + 水，（−254.4556 cm⁻¹）鞍点不连接声明反应物。**

## 3i. 反侧端点频率（job 1105 · done）与停算归档

- reactant_frequency.log（ts/ts_0022/jobs/declaration_0005/reactant_frequency/reactant_frequency.log，1968 行，sha256 c51844775bfc8a24…）
  L510 `SCF Done = -364.334597427`；**无 imaginary 横幅，51 个频率**（L849 起 44.4026 / 59.0952 / 75.1013 …）；L1968 `Normal termination`（04:49:53）
  ⇒ 反侧端点 = **已验证极小值**：N-质子化肟 + 水（R(N6,H4)=1.027、R(9,16)=0.999、C=N 1.2932、N–O 1.3468、2 片段），0 虚频。
- **2026-10-18 05:xx 停算**：主协调广播 evt_1368eb1b076741ac（用户「被换掉的题的任务可以杀了」）⇒ ts_stop(ts_0022)；排队中的 product_opt **job 1116 → cancelled（从未起跑）**；ts/ts_0022 下全部日志原样保留，未删未改。

## 4. 最终结论（详见 [FINAL_REPORT_HL1_E1.md](FINAL_REPORT_HL1_E1.md)）

- (a) 方向闸门**通过**；−254.4556 cm⁻¹ 是真 PT 模（δR(1,2)=+0.0207、δR(2,9)=−0.0495、û(O1→O7)·d(H2)=+0.3555）。
- (b) 三份额：中心对 0.2542 / 重原子 0.0512 / 最大单原子 H4 0.4739（非 spectator，但落在声明对之外）。
- (c) **不通过**：双向 IRC 被引擎默认 10 点截断（平台 #184，end_setting 亦被静默丢弃）；反侧落到 **N-质子化肟+水**（−364.334597427，0 虚频）而非声明反应物；正侧 B 端点 Opt/Freq 未跑（1116 撤回）。
- ⇒ 该鞍点身份 = **B（O-质子化产物）↔ N-质子化肟+水** 的质子中继鞍点：E(TS)−E(B)=+3.5681 kcal/mol，E(TS)−E(N-质子化)=+27.8101 kcal/mol；E(N-质子化)−E(B)=−24.2420 kcal/mol。
- ⇒ **HL1_E1 维持 0.0 约定值，不回填 ΔE‡**；0.0 三件并列（约定值非测量值 / pt8 +3.5705 仅为受约束剖面下界且峰两侧不同物种 / 起点 RC 不存在）已写入终报。

## 5. 历史待办（已按停算指令中止）（04:38 重写，旧条目 1–2 已完成或已作废）

1. **（已作废，保留痕迹）** 旧条目「等 job 1084 终止 → 判 (a)(b)」已由 §3d 完成；旧条目「若反向 IRC 落回 B 则 0.0 约定口径仍成立」**已作废**：反侧并未落回 B，而是漂到 N-质子化肟 + 水并 FormBX 失败 ⇒ 口径改为「该级别下不可计算」，题源 null。
2. **等 #1102 / #1104 终态**：出 `Optimization completed.` + 四条 YES 者，用其收敛几何提 freq（同目录 chk、geom=allcheck、4c/6144、气相 B3LYP/def2SVP+GD3BJ+Int(Ultrafine)+SCF=Tight），验收「恰 0 虚频」且 freq 首条 SCF Done 与 Opt 末帧差 <1e-6 Ha。**0 虚频 = N-质子化肟+水 是本级别极小的合格证据**；若再 FormBX 失败 ⇒ 记录失败、换起点（opt=(cartesian,maxstep=2) 或分步固定水），不重复同一坐标系。
3. **FORWARD 侧**：#1099 FWD 10 点内未到 B（R(2,9) 1.182 vs B 的 1.0774）⇒ 正侧端点身份同样未建立；若需要，用 FORWARD 最外层帧做一次无约束 Opt（同一口径），仍按「IRC 仅方向证据」写。
4. 结论按「边 → job id → 卡在哪一环」报给主协调，附原生日志绝对路径 + sha256 + 行号；涉及原子号一律给「Gaussian 序 → 元素」全表 + 两套编号对应（D44）。
