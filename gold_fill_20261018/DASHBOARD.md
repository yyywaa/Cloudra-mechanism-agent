# gold 填充总看板（自动刷新）

> 刷新时间：2026-10-18 04:23:09　算力：**32/32 cpus**

## 已出结论的边

| 边 | 结论 | 关键证据 | 台账 |
|---|---|---|---|
| **HL1_E1** | **该级别下不可计算**（O-质子化端点不是极小值） | TS −254.4556 cm⁻¹（1093）；IRC 双向 10 点方向正确但未达端点（1099）；1100/1101 端点 Opt 均塌成 N-质子化肟（H4–N8 = 1.055/1.056 Å，E ≈ −364.33） | D34→D35（撤回）→D37→D38→D40 |
| **HI1_E5** | **受约束 2D 网格不可作势垒**（脊在盒外） | 17 格 + A1/A2/A4；1.2193 行 2.4248→2.6248 = +4.75、0.9693 行 = +8.12（均继续上升）；沿 R(25,26) 在 R(2,4)=2.2248 列有内部极大（48.82/67.86/41.95） | D18→D39 |
| NI5_E1 | 0.93（已回填，缺 BRIEF ①②） | 软模主导；IRC 仅方向区间 | 早前记录 |

## 在跑作业

| job | 输入 | 归属 | cpus | 当前状态（04:46 巡检；ps g16 进程数 8 = 账本 running 8，无僵尸） |
|---|---|---|---|---|
| ~~#1092~~ | ts_0026/declaration_0003/ts_opt/refine.gjf | HI1_E1b | 4 | **终态：调度终止 04:51:04**（用户 05:0x 指令「被换掉的题的任务可以杀了」；我执行 `ts_stop(ts_0026)` → run status=stopped/rev23，job state=**cancel_requested**）。停止瞬间 **Step 33/153**（L23848）、末条 SCF `-593.859284599`（L23775）、`Normal termination` 0 条 / `Error termination` 0 条 ⇒ **未收敛、未进 freq、无虚频**；日志 `ts/ts_0026/jobs/declaration_0003/ts_opt/refine.log` 1,519,164 B，sha256 `a27d5f147487f099e7938798bd63a96bd61ae4c0b405d3b33de5de9a5af6099d`。**HI1_E1b 现值仍 null**（D1 a/b/c 全未测），按调度终止登记、不写成科学失败结论；第 33 步能量不得作 ΔE‡。证据归档：`HI1/HI1_E1b/E1B_STATUS_AND_EVIDENCE.md`（sha `e9e21e86…`）；未执行的项：reaction_center 0-based 缺陷（`[[1,3],[2,9],[3,9],[1,2]]` 应作 `[[2,4],[3,10],[4,10],[2,3]]`）因停算未修正 |
| #1094 | ts_0024/declaration_0012/ts_opt/refine.gjf | HI1_E4 | 4 | 在算，Step 5，未收敛 |
| ~~#1095~~ | ts_0025/declaration_0003/ts_opt/refine.gjf | HI1_EM1 | 4 | **终态：ts_opt 收敛**（L3003 Stationary point found、L4114 Normal termination 04:28:56、末 SCF −939.283734386 @L2625，log sha 57cb8439…）；该值与 ts/ts_0012/jobs/declaration_0002 的 TS 帧同一点（**不是 job 1032**：1032 = declaration_0001，E = −939.293671629 @L24138、虚频 −27.9419 @L1516；两者差 6.24 kcal/mol）⇒ TS 驻点复现，不是极小；job 924 参考极小实为 −939.308218263 Eh（两者不同，先前「同值」说法已更正）|
| #1096 | routeA/A1/A1_opt.gjf | HI1_E5 路线A A1 | 4 | 未收敛，Step 14（注：日志 L115 的 `Optimization completed` 是输入头溯源 title 文字，不是收敛） |
| #1097 | routeA/A2/A2_opt.gjf | HI1_E5 路线A A2 | 4 | 未收敛，Step 12 |
| #1098 | routeA/A4/A4_opt.gjf | HI1_E5 路线A A4 | 4 | 未收敛，Step 12 |
| ~~#1100~~ | ts_0022/declaration_0004/reactant_opt/reactant_opt.gjf | HL1_E1 端点 Opt（N-质子化证据） | 4 | **终态：Error termination（l103 Bend failed for angle 1-4-8，04:26:11）⇒ 该端未达极小**，不分类、不给 ΔE‡ |
| ~~#1101~~ | HL1_E1/irc_endpoints/rev_outer/rev_outer_opt_fix1.gjf | HL1_E1 端点 Opt（N-质子化证据） | 4 | **终态：Error termination（l103 Tors failed for dihedral 1-4-8-9 / 1-4-8-7 / 3-1-4-8，04:29:17）⇒ 该端未达极小**，不分类、不给 ΔE‡ |
| ~~#1102~~ | ts_0022/declaration_0005/reactant_opt/reactant_opt.gjf | HL1_E1 端点 Opt（**species_reference 独立种子**） | 4 | **终态：真收敛 04:47:00**（L18868 Optimization completed、L18869 Stationary point、末 SCF −364.334597427 @L18666，sha d010704f…）；末帧 **H4–N8 1.0267 / O1–H4 2.3033 / O1–O2 水 0.9704 / O1···O9 2.5887** ⇒ O-质子化意图收敛成 N-质子化肟+水 |
| ~~#1105~~ | ts_0022/declaration_0005/reactant_frequency/reactant_frequency.gjf | HL1_E1 **环④** | 4 | **终态：0 虚频**（04:49:53，sha c5184477…，1968 行；L510 SCF −364.334597427 与 Opt 末帧逐位相同；51 模全正，首组 L849 44.4026/59.0952/75.1013；L1968 Normal termination）⇒ N-质子化肟+水 是该级别本地极小，四环齐备 |
| #1103 | ts_0025/declaration_0003/frequency/frequency.gjf | HI1_EM1 freq（平台自动接在 #1095 收敛几何上） | 4 | 在算（l1110 348% CPU，解析频率），尚无 `Frequencies --` 段；判读口径：1 虚频→(a) 可继续；0 虚频→#1095 是极小、本次作废换 seed；≥2→换 seed |
| #1104 | HL1_E1/irc_endpoints/rev_opt2/rev_opt2_cart.gjf | HL1_E1 端点 Opt 修法 A（**opt=(cartesian,maxstep=5)**，起点 = #1100 末帧 L17301） | 4 | 在算，Step 28/67，未收敛；输入 sha f81033c4…，与 #1102 的 `#p opt` 内坐标不同（避 FormBX） |


## 05:0x 指令：被替换题停算（归档口径）

- 主协调广播（evt_1368eb1b）：四道替换候选（NR1→甲酰胺、NY3→HNCO、HI1→Cope、HL1→HCNO+降冰片烯）确定后，旧题剩余作业一律停止，把 32 核让给两道新题。
- 本 lane 受影响的在飞作业：**#1104**（HL1_E1 rev_opt2 笛卡尔端点 Opt）——需由主协调走账本 cancel 通道；我无该通道。**#1105**（HL1_E1 环④ N-质子化肟·水的 freq）不在广播点名范围，等指示。
- 已归档、不删不覆盖（这就是本轮全部产出）：HL1_E1/STATUS.md（154 行 / sha 3d7d9013 之后再次更新）、HL1_E1/BACKFILL_PROPOSAL.md（77 行 / sha 0b824c19…，四环证据 + 失败记录 + 不得引用清单）、HI1_E5/GRID_SNAPSHOT.md（133 行，17 格 + A 组 3 格 + 外部外延终止）、HI1_EM1/BACKFILL_PROPOSAL.md（142 行）。
- 停算登记口径：若平台记为 failed/cancelled，按「**调度终止**」登记，**不得写成科学失败结论**；本 lane 不把任何被停作业写成「算不出来」。
- 本 lane 自 05:0x 起**不再提交任何作业、不 ts_resume**。

### 本 lane 收尾清单（05:00，全部按「调度终止」登记，不写科学失败）

| 作业 | 最终状态 | 归档证据 |
|---|---|---|
| #1093 HL1 TS freq | done（04:39） | freq.log sha d4f9171d…，L841 1 imaginary、L850 −254.4556 |
| #1099 HL1 IRC | done（04:06） | irc.log sha b2f29746…，双向各 10 点被引擎默认截断 |
| #1100 HL1 反端 Opt | **failed（l103 Bend 1-4-8，04:26:11）** | 未达极小；末帧写入 reactant_endpoint_seed_last_frame.xyz |
| #1101 HL1 反端 Opt | **failed（l103 Tors 1-4-8-x，04:29:17）** | 与 #1100 同因同向 |
| #1102 HL1 端点 Opt | **done，真收敛（04:47:00）** | L18868/18869、末 SCF −364.334597427 @L18666、sha d010704f… |
| #1105 HL1 端点 freq | **done，0 虚频（04:49:53）** | sha c5184477…，1968 行，51 模全正，L510 同值 |
| #1104 HL1 笛卡尔对照支 | **仍 running（l703 285% CPU，Step 46/67）** | **待主协调走账本 cancel 通道撤销**（我无该通道） |
| #1096/1097/1098 HI1_E5 A1/A2/A4 | 停算（未收敛） | GRID_SNAPSHOT §6 保留过程帧 + 「外部外延到此为止」 |
| #1092 / #1094 / #1103 | 由对应 lane ts_stop 停算 | 各自 lane 的 STATUS 已登记 |

**HL1_E1 归档结论（不进题源，旧值 0.0 保留为历史条目）**：四环齐备 —— ① TS 恰 1 虚频 −254.4556；② IRC 双向仅方向证据（未达端点）；③ O-质子化意图的独立种子收敛成 N-质子化肟+水（H4–N8 1.0267、O1–H4 2.3033、O1···O9 2.5887）；④ 该物种 0 虚频、51 模全正。⇒ 声明的 O-质子化端点在该级别气相不是稳定极小值，该 TS 是 B ↔ N-质子化肟+水的质子中继鞍点，不能用于本步。详见 HL1_E1/BACKFILL_PROPOSAL.md（80 行 / sha ebdb1d1b…）。

## 判据定义（D1，不变）
- **(a) 方向**：虚频模在声明 watch pair 上净位移必须与 `bond_changes` 同向；反向即 pseudo-saddle，永不回填。
- **(b) 成分**：三种归一化份额 + 最大份额落点；只记录不设阈值。
- **(c) 交付**：同程序同方法 TS（恰 1 虚频）减本步自身起点，双向 IRC 到声明端点 + 两端 Opt/Freq 0 虚频。

## 方法层面结论（本轮新增）
1. **B3LYP/def2SVP 气相下「肟 O-质子化」不是稳定极小值**（两条独立路径都塌到 N-质子化）⇒ HL1_E1 不存在可定义起点。
2. **平台限制 #184**：`ts_prepare` 的 irc 阶段无入口设 MaxPoints/StepSize，`end_setting` 亦被静默丢弃 ⇒ IRC 只能跑引擎默认（~10 点/向），端点身份必须靠外层帧 Opt+Freq 承担。
3. **内存是并发硬闸门**：`cap_mem = 51200 MB`；8c 作业最多同时 3 个，8 个 4c 恰好塞满 32 核 ⇒ 新作业一律 4c/6144。

## 文件索引
- 裁决台账：`DECISION_LOG.md`（D1–D40）
- HL1_E1：`HL1/HL1_E1/{STATUS.md, irc_endpoints/, analyze_mode.py, analyze_endpoint.py}`
- HI1_E5：`HI1/HI1_E5/{GRID_SNAPSHOT.md, GRID_PLAN_A.md, routeA/A1..A4}`
- HI1_EM1：`HI1/HI1_EM1/BACKFILL_PROPOSAL.md`
- HI1_E3 legacy：`HI1/HI1_E3/LEGACY_NOTE.md`
- NY3 快照：`NY3/{NY3_SOURCES.md, E2_GUESS_ATTEMPT2.md, TS0023_SNAPSHOT_D32.md}`
- NR1 快照：`NR1/{STATUS.md, E2_SCAN_SNAPSHOT_D29.md}`
- 外机多参考请求：`../gold_compute/queue_20261018/specs/EXTERNAL_MR_REQUESTS_IG8_IF3_IC3.md`

## 收敛判据（不许把「跑到某个能量」当收敛）
Gaussian Opt 必须同时满足四条且日志出现 `Optimization completed.` / `Stationary point found.`：
1. `RMS Force` YES
2. `MAX Force` YES
3. `RMS Displacement` YES
4. `MAX Displacement` YES
⇒ 当前在跑的 1096/1097/1098/1100/1101 **全部 dispYES=0、forceYES=0**，即**都未收敛**；它们的最新能量只是**过程帧**，不得写进任何结论表。
⇒ 端点/格点必须等到 `Optimization completed.` 才算数；freq 必须在**收敛后**的几何上跑（同一 chk 续算），否则虚频判据无效。
