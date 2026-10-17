# HI1 包状态 · 2026-10-15（包 Coordinator）

## ★ 最新状态块（第三任 Coordinator，2026-10-15 23:2x；权威，下方旧段保留为历史）

**一句话**：本包 3 条边（HI1_E1 / HI1_E3 / HI1_E2+EM1 的 (S) 重算）都还停在「计算未完成」；已完成的是起点/中间体极小值（907 / 924 / 961），缺的是 TS+频率+IRC+两端链。三道已按新会话重新派发（前任三道会话全部 failed）。主协调 2026-10-15 政策更新（BRIEF §9：标答不具权威性、按证据选机理）已收到，本包按证据自行决定机理问题、不再等裁决。

### 每条边一页状态块

**HI1_E1（合并边，题源 hi.py I1 steps[0]；CPCM(DMSO)/q0/m1；41 原子）**
- 状态：**缺测（TS 链未跑出）**；值：无（旧 19.2 作废，不回填）。
- 已完成：job 907 = (S)-RC 极小值 = 该步起点（0 虚频）。
- 缺失证据：TS（恰 1 虚频且模以 7 个声明对为主）、双向 IRC、两端 Opt/Freq、ΔE‡。
- 阻塞/根因：ts/ts_0004 在 build 阶段 blocked（failure_class=conformer_optimization_failed，attempt 1:candidate_opt:928）；**根因是平台自动生成的 ETKDGv3 反应物种子原子重叠（H35…H36 = 0.299 Å）→ l202**，不是化学。修法 = ts_resume 把 conformers.reactant 换成文件 conformer（已验证 RC 几何）+ provided guess + reaction_center。
- 预期：合并边 7 对（3 断 4 成）很可能没有合格单鞍点 → 按 BRIEF §9 由证据拆步。
- 参考极小值（= 能垒基准）：job 907，(S)-RC，0 虚频（117 模，最低 9.70 cm-1）；**E(RB3LYP) = -939.308829219 Eh**（末条 SCF Done 原始行）；log `gold_finish_20261015/HI1/E1/runs/RC_optfreq/RC_optfreq.log`；sha256 `fa28545612332f69c60c0b778cd5dd1907b22b8ad36f6b1da7811da1295563ba`。

**HI1_E3（水解合并边，I1 steps[2]；CPCM(DMSO)/q0/m1）**
- 状态：**缺测（TS 链未建）**；值：无（旧 16.9/19.2 作废，不回填）。
- 已完成：job 961 = I2 侧 Opt+Freq 极小值（0 虚频），实测物种 = **aldol-OH + carboxylate + 旁观水**（与题源声明的 alkoxide+COOH 只差 1 个质子，互为质子互变异构体）；job 951 = I2 重原子骨架几何准备（弛豫扫描，起点 = 前体预复合物，终点 = 该互变体）。
- 缺失证据：TS（恰 1 虚频 + 模以 6 对为主）、双向 IRC 到 I2 与 P、两端 Opt/Freq + 身份核验、ΔE‡。
- 参考态口径（按 BRIEF §9 由证据定）：**以实测 I2 侧极小值为该步起点参考态**；题源声明的 alkoxide+COOH 质子位置在本级 QM 下不是驻点（预组织的羧基 H 自发转移到醇盐 O）。该项属「参考态/质子化位点重定」，交付时单列。
- 参考极小值：job 961；**E(RB3LYP) = -939.320655479 Eh**（行 16950）；log `gold_finish_20261015/HI1/E3/runs/I2_optfreq/I2_optfreq.log`；sha256 `63dda25e04529e65920526304fb88755db9393e9c22bd3a6efb76eeee0af0d0e`；0 虚频（117 模，最低 35.3075）；CIP 原子 8（map16）= S、原子 29（map6）= S。
- 下一步：等 job 963（预组织弛豫扫描 3.16→2.20 Å）终态 → 取 r(C2-O25)≈2.20 Å 帧作 provided guess → ts_prepare 全链（6 watch pair + 41 原子 concrete atom_map）。

**HI1_E2 / HI1_EM1（(S)-脯氨酸体系重算，L2 身份缺口；主协调已授权）**
- 状态：**缺测（两通道 TS 链未建）**；既有 E2=13.36 / EM1=15.52 **不动、不回填**（建在本机不存在的 R-脯氨酸几何上，非对映体关系）；新值通过验收后替换并写 provenance。
- 已完成：job 924 = (S)-HI1_I1 极小值（共享基线）；两条通道的 ORCA 源帧镜像种子 + provenance + 原子序换算表 + 重排脚本（非 QM 准备）。
- 缺失证据：两通道各自 TS（恰 1 虚频 + C3-C6 主导）、双向 IRC、两端 Opt/Freq + CIP、ΔE‡、ΔΔ。
- 基线：job 924；**E(RB3LYP) = -939.308218263 Eh**（行 20025 / 22238）；log `gold_finish_20261015/HI1/E2EM1/runs/I1_optfreq/I1_S_optfreq.log`；sha256 `6ecf06238ee6e1e976ba30eb15faf655f3ebe5a0126ed37d0dfe9b687dea6a87`；0 虚频（117 模，最低 24.6404；两条 Normal termination：行 21468 = opt 段、行 27032 = 总）；Cα = S；与 (R)-I1（908，E=-939.308218263）等能 = 对映体关系（交叉验证一致）。
- 能垒口径（写死）：ΔE‡ = E(TS) − E(job 924)，纯电子能、同批 Gaussian 16；禁止改用 907、禁止用工作流自身 reactant 端点替换 924。

### 本批原生日志 sha256 复核表（全部由我本轮真实 sha256sum/读数获得）
| 作业 | 内容 | 日志（相对 gold_finish_20261015/HI1/） | sha256 | 结论 |
|---|---|---|---|---|
| 907 | (S)-RC Opt+Freq | `E1/runs/RC_optfreq/RC_optfreq.log` | `fa28545612332f69c60c0b778cd5dd1907b22b8ad36f6b1da7811da1295563ba` | 0 虚频，E=-939.308829219 Eh |
| 908 | 实为 (R)-I1 Opt+Freq（口径作废） | `E1/runs/I1_optfreq/I1_optfreq.log` | `d35b0abfdb25154e54d848bdbcf2bd7af387fb63a7f4a2229325d557d1d933eb` | 0 虚频，E=-939.308218263 Eh |
| 924 | (S)-I1 Opt+Freq | `E2EM1/runs/I1_optfreq/I1_S_optfreq.log` | `6ecf06238ee6e1e976ba30eb15faf655f3ebe5a0126ed37d0dfe9b687dea6a87` | 0 虚频，E=-939.308218263 Eh |
| 961 | E3 的 I2 侧 Opt+Freq | `E3/runs/I2_optfreq/I2_optfreq.log` | `63dda25e04529e65920526304fb88755db9393e9c22bd3a6efb76eeee0af0d0e` | 0 虚频，E=-939.320655479 Eh（互变体） |
| 951 | E3 的 I2 骨架几何准备（弛豫扫描） | `E3/prep/I2_prep_scan_v5.log` | `fdc0412151fd10d2820065910ee07c73de4f1e620f22d349ed375221c02883a2` | 9 帧；终点 = 互变体（扫描能量不作能垒） |
| 962 | E3 预组织约束优化（裸 B 卡静默失效） | `E3/runs/preorg_v1/preorg_c2o25_220.log` | `759bce701518a329f5d0d5ce1e2605afb3d1feae28deb095e1c5c983eb85bdc8` | 收敛回未约束 I2 极小值 |
| 963 | E3 TS 预组织弛豫扫描（进行中） | `E3/runs/preorg_v2/scan_c2o25_316_220.log` | 终态后补 | 3.16→2.20 Å，23:0x 做第 3 帧 |
| 910 / 925 / 945 | E3 I2 几何准备三次失败 | `E3/prep/I2_prep_cons180_v2/v3/v4.log` | `de8c66db2578099a…` / `5045c0e847b03697…` / `41c8ca64249a2d51…` | 依次为 l101 几何段缺空行 / route 被说明文字污染（l1 语法错）/ RedCar 约束步长过大 |
| 928 | ts/ts_0004 candidate_opt（种子优化） | `../../ts/ts_0004/jobs/declaration_0001/candidate_opt/seed-opt.log` | `e3286543d054fd48cab499cea8bca605156f0e7ff318253b4c21d19c393c7694` | l202：自动种子 H35…H36 = 0.299 Å |

### 道与协作
- 包 Coordinator 会话 = `as_d7c75bc2ebf046a9`（第三任；主协调 = as_a341823c436e47ed）。
- lane1（E1 合并边）：small_mol `as_fc7fdbb5e5564d93`，产出 `E1/LANE1_STATUS.md`。
- lane2（E3）：small_mol `as_e5bb8c58d7b84e9c`，更新 `E3/STATUS.md`。
- lane3（E2/EM1 (S) 重算）：small_mol `as_bc146127755a404d`，更新 `E2EM1/STATUS.md`。
- 本包 hub 帖（主题 gold-finish-20261015，正文首行 `to: as_a341823c436e47ed`）：`evt_d5b48a3adc624da1`（开工 + 裁决重申）、`evt_4213cb81a4d6484c`（对 §9 政策的回执与落地计划）、`evt_ab6959ddca964aa2`（政策转发给三道）。

### 下一步 / 阻塞 / 回填前置
1. E1：lane1 修 ts/ts_0004 的 build 阶段并跑全链；若无合格单鞍点 → 拆步证据包 + 节点/边划分提案（由我改 hi.py）。
2. E3：job 963 终态 → lane2 建 ts_prepare 链；参考态 = 实测 I2 侧极小值（§9 口径，交付单列修订）。
3. E2/EM1：lane3 两通道串行（E2 先、EM1 后），ΔE‡ 相对 924，ΔΔ 与历史 2.16 对照。
4. 阻塞：(i) ts/ts_0004 的 owner 会话已 failed，ts_resume 可能被拒（issue #180 同型）→ 按先例重建新 run；(ii) 平台无排队作业取消入口（排队只能等）。
5. 回填前置（我在满足后执行）：只改 `cloudra/benchmark/hard_registry/hi.py` 自己边的 barrier/必要注释 + 同步 `ideapool/tasks/hard/HI1.json` 重新生成 + `pytest tests/test_benchmark.py -k regenerate_identically` 原样粘贴 + `ideapool/reaction_candidates/hard.md` 的 I1 行 edit；交付单列「证据驱动的机理修订」。

## 巡检 R2（2026-10-15 23:45，权威增量）

**回填基线（改动前）**：`python -m pytest tests/test_benchmark.py -k regenerate_identically -q` → **4 passed**（无预先存在的 mismatch）。任何回填前重跑此测试作基线。

### E1：ts_resume 被拒 + 已重建 ts_0008（job 968 在跑）
- `ts_resume(ts_0004)` **被平台拒**：逐字 `ts_resume: TS process belongs to a different project or owner`，call_id `tc_f284ae99aa9243d1`（owner 会话 as_84bdf87a0f94416c 已 failed；issue #180 同型第 3 次复现）。ts_0004 未改动，失败证据保留。
- 已按先例用 `ts_prepare` 重建 **ts/ts_0008**（call_id `tc_cb41ccb084734cd9`）：reaction 段逐字复制 ts_0004 的 mapped SMILES；conformers.reactant = file（`E1/lane1/RC_S_canonical.xyz` sha256 71b23e07b73a7241e19c3c94e927040f5f113f815184bfa44387d58bbc0e6597 + `.mol` cbdb052b5e49b7ac3872df703b7b4e6e7ee1ade61d6cfad0232986fb56c2459c；heavy_atom_binding = [1,2,3,4,11,12,13,14,15,16,17,18,25,26,27,28,29,30,31,32]）；guess = provided（`E1/lane1/TS_guess_merged_canonical.xyz` sha256 a2c0fa28667eb5afd814d8b876f40dd5873967c8a63973ff89bf9b0d0b980c4c；evidence_refs = `E1/TS_GUESS_PROVENANCE.md` sha256 d7a82f39e7d068400a0da60d4b59b7679c66441fd13cf885bb25f909f37a3276）；execution 8c/8192MB。
- **我（包 Coordinator）独立复核 ts_0008 的绑定序**：`ts_inspect(ts_0008)` → `structures.reactant.index_base = 1`、41 原子符号序 C,C,O,C,…；实测原子 10 = H、原子 32 = N、原子 41 = H → 与 7 对 `break (2,3)=C2=O4、(4,10)=C3–H22、(32,41)=N20–H21；form (2,4)=C2=C3、(2,32)=C2–N20、(3,41)=O4–H21、(3,10)=O4–H22` 逐对相符（1-based 绑定序）。`smiles_heavy_atoms` 位置 1..20 的 atom_map_label = 1,2,4,3,5..20，与 TS_GUESS_PROVENANCE.md §3 表一致。
- **索引约定（lane1 交叉证实 + 我复核）**：输入契约 1-based；run 落盘的 declare.json/process.json 为 **0-based**（决定性旁证：ts/ts_0006/declare.json 记录 reaction_center=[[0,5]]，1-based 输入不可能出现 0）。对外引用一律给 1-based 并注明「= 落盘值 +1」。
- job **968** = `ts/ts_0008/jobs/declaration_0001/candidate_opt/seed-opt.gjf`（candidate_opt，23:41 起跑）→ 终态后应重现 RC 极小值（≈ -939.3088 Eh）。lane1 已监控（我用 hub call 唤醒其 succeeded 会话，wake_status=requested）。
- 907 参考态行号（我本轮复核）：`RC_optfreq.log` sha256 fa285456…63ba；L59761 `SCF Done: E(RB3LYP) = -939.308829219 A.U. after 6 cycles`（L61974 频率段同值）；L60132 `Optimization completed.`；L61206 = opt 段**中间** Normal termination（勿当终点）、L66757 = 总 Normal termination；39 组 `Frequencies --`×3 = 117 模，最低 9.7022 cm⁻¹ → 0 虚频。

### E3：963 完成（单调上升、无内峰）+ 链未建
- job **963** 完成：`E3/runs/preorg_v2/scan_c2o25_316_220.log`，sha256 `e535fb2f1bc5b7259aaed18ba7f391290bfec3e4f07ce39cf146238ed63c27cf`，`Normal termination` **23:38:46**，4 点全部 `Optimization completed`；C2–O25 实测 3.160 → 2.840 → 2.520 → **2.200 Å**（约束确实被执行，与 962 的裸 `B i j value` 静默失效形成对照）。
- `ts_guess(scan_parse)`：**无内部峰**；约束扫描相对能量 0.000 / +0.954 / +4.004 / **+8.151 kcal/mol**（单调上升；**扫描能量不作能垒证据**）。→ 若存在鞍点，必在 r(C2–O25) < 2.20 Å 一侧。
- 末帧几何（= provided guess 候选）：`E3/runs/preorg_v2/ts_guess_c2o25_220.xyz` sha256 `640405ff9b4f59c234fd966fadd1689c7717feb924fc7b4fd40b18a72e1a2bec`（41 原子，2 分片，C2–O25 2.200、C2–N4 1.305、O28–H24 0.988、水完整且 H27 氢键连羧酸根 O10 1.675）。
- 延伸扫描已备好（等空槽）：`E3/runs/preorg_v3/scan_c2o25_220_160.gjf` sha256 `35f151c75fc3f00b4e2a3c2ac0564098084efa4192a932a33b95bac197f76bbc`（2.20→1.60 Å，4 点）。
- 参考态口径（BRIEF §9）：E3 起点 = **实测 I2 侧互变体**（aldol-OH + carboxylate + 旁观水，job 961，E = -939.320655479 Eh）。lane2 正在建链（E3/STATUS.md 23:40 仍在更新）。

### E2/EM1：ts_0009 已建但缺 product 构象
- `ts_inspect(ts_0009)`：rev 4 / status=**blocked** / stage=build / `failure_class=missing_input` / `needs=[conformers.product]`；reaction = 烯胺+水+苯甲醛 → iminium-aldolate（E2 major 通道），conformers.reactant = file（`E1/build/I1_S_start.xyz` + `E2EM1/build/I1_S_start_ref.mol`），guess 暂缺、reaction_center 暂空。lane3（as_bc146127755a404d）仍在运行，正在补。


## 接手机读块（2026-10-15 23:5x，平台第 3 次写锁重启前；继承人按此续跑即可）

**包 Coordinator**：as_d7c75bc2ebf046a9（第三任）。主协调：as_a341823c436e47ed。hub 主题：gold-finish-20261015（回报首行写 `to: as_a341823c436e47ed`）。

**三道会话与其唯一任务（盘上状态自足）**：
- lane1 = `as_fc7fdbb5e5564d93`（HI1_E1 合并边）：状态文件 `gold_finish_20261015/HI1/E1/LANE1_STATUS.md`（23:17 起，含 ts_resume 被拒逐字 + call_id）。正在等 **ts/ts_0008 的 job 968 = candidate_opt**（`ts/ts_0008/jobs/declaration_0001/candidate_opt/seed-opt.log`）→ 之后管线自动 ts_opt → frequency → 双向 IRC → 两端 Opt/Freq。
- lane2 = `as_e5bb8c58d7b84e9c`（HI1_E3）：状态文件 `gold_finish_20261015/HI1/E3/STATUS.md`（末段 E.13/E.14/E.15）。963 已终态（单调上升、无内峰）；下一步用 `E3/runs/preorg_v2/ts_guess_c2o25_220.xyz`（sha 640405ff…）作 provided guess 建 ts_prepare 链，或先跑已备好的延伸扫描 `E3/runs/preorg_v3/scan_c2o25_220_160.gjf`（sha 35f151c7…）。
- lane3 = `as_bc146127755a404d`（HI1_E2/EM1 (S)）：状态文件 `gold_finish_20261015/HI1/E2EM1/STATUS.md`。已建 `ts/ts_0009`（E2 通道 A）但 **blocked: missing_input / needs=[conformers.product]**（rev 4）→ 补 product conformer（P/iminium-aldolate 种子 + mol）后继续；EM1 通道串行在后。

**已知数值与参考态（本批 Gaussian 16，同批相减）**：E1 基线 job 907 = -939.308829219 Eh（0 虚频）；E3 基线 job 961 = -939.320655479 Eh（0 虚频，实测互变体 aldol-OH+carboxylate）；E2/EM1 基线 job 924 = -939.308218263 Eh（0 虚频，Cα=S）。
**回填基线**：改动前 `pytest tests/test_benchmark.py -k regenerate_identically -q` = 4 passed。
**重启后第一步**：跑 `ts_inspect` 复核 ts_0008 / ts_0009 的权威 revision 与 job 状态（不要凭 process.json 或旧记忆）；跑 `query_compute_queue` 看幻影行是否被 adopt 收尾；再让三道继续。
### 队列/进程快照（23:42 实测）
- 在跑：job 968（HI1 ts_0008 candidate_opt，8c）、job 967（NY3 ts_0007 candidate_opt，8c）、NI5 两个端点 opt+freq（job09/job10）。963 已终态。
- 本包手工提交在飞 = 0（963 已终态，968/967 为管线自动作业，不占手工配额）。

> **交付级更正（2026-10-15 18:20，接班 Coordinator as_84bdf87a0f94416c；主协调已复核并写入 LEDGER）**
> **作业 908 = (R)-脯氨酸 I1 极小值，不是 (S)** → 「908 = (S)-I1 共享基线」口径作废。
> 实测（可复现）：`python3 gold_finish_20261015/HI1/shared/tools/hi1_cip_tools.py gold_finish_20261015/HI1/E1/runs/I1_optfreq/I1_optfreq.log gold_finish_20261015/HI1/E1/runs/RC_optfreq/RC_optfreq.log`
> → `I1_optfreq.log CIP[8C=R(nb 7C,4N,9C,23H)]`、`RC_optfreq.log CIP[8C=S(nb 7C,4N,9C,23H)]`（RDKit：取 log 最后一个 Standard orientation → DetermineBonds → AssignStereochemistryFrom3D → AssignCIPLabels）。
> 且 `E1/runs/I1_optfreq/I1_optfreq.gjf` 的坐标与 `gold_compute/grant_materials_20261001/raw/HI1/job_51/rc_clean_np8.xyz` 逐原子 **maxdev = 0.0000 Å**（提交时用的是历史 R 几何，注释里却写 S）。
> 908 log sha256 `d35b0abfdb25154e54d848bdbcf2bd7af387fb63a7f4a2229325d557d1d933eb`（117 模、0 虚频、E(RB3LYP) = −939.308218263 Eh、Normal termination）；907 log sha256 `fa28545612332f69c60c0b778cd5dd1907b22b8ad36f6b1da7811da1295563ba`（Cα=S、0 虚频、E = −939.308829219 Eh）。
> 结论：E1 现有两端点 **RC(S)/I1(R) 互为对映体**，R↔S 不是基元步、不得互连；(S)-I1 基线改由 **job 924** 提供（输入 `E2EM1/runs/I1_optfreq/I1_S_optfreq.gjf`，实测 Cα=S，8c/8192MB）。
>
> **输入级坑（E3 复算必读）**：910 的 l101 失败根因 = 坐标块与 ModRedundant 卡 `B 1 29 1.80` **之间缺 1 个空行**（不是"多了空行"、也不是重启副作用）→ 已修 `E3/prep/I2_prep_cons180_v3.gjf`（sha `4f8c4851b8ba74013c1cc162c1158ce7d826ac93a1637fe446ce1bc5b0c292c3`）并重提为 **job 925**。

计划：`gold_finish_20261015/HI1/PLAN.md`。**非 QM 准备产物登记（交付按路径引用）**：`gold_finish_20261015/HI1/PREP_ARTIFACTS.md`（sha256 `975d1750570548989197101ae0029b663fdd249945445fb3929c820481ccf516`；**该文件随各道落盘持续更新，交付时以重取 sha 为准**，本文件内其他 sha 亦同）——E1 的 7 个声明成断键对（map 号；主协调来函写 6 个，实为 3 断 + 4 成）、E3 的 6 个 watch pair、lane3 两通道的 TS 种子/CIP 工具与「barrier = E(TS) − E(job 924)」硬约束、各道待产出项与属主。方法：Gaussian 16 B3LYP-D3(BJ)/def2-SVP + Int(UltraFine) + SCF=Tight + CPCM(DMSO)，q0/m1（本机无 ORCA）。

| 边 | 状态 | 已回填值 | 缺测/缺什么 | 证据 |
|---|---|---|---|---|
| HI1_E1 | 进行中 | — | — | 待填 |
| HI1_E3 | 进行中（先只读缺口复核） | — | — | 待填 |

## 巡检 3（接班 Coordinator as_84bdf87a0f94416c，2026-10-15 18:0x–18:1x）

**① 908 身份核验（我独立复核；工具 `shared/tools/hi1_cip_tools.py`）**：`E1/runs/I1_optfreq/I1_optfreq.log` sha256 `d35b0abfdb25154e54d848bdbcf2bd7af387fb63a7f4a2229325d557d1d933eb`（1,785,921 B, mtime 17:43）。log_parser：117 模、**imaginary_frequencies=[] → 0 虚频**、`SCF Done E(RB3LYP) = −939.308218263` Eh、Normal termination ✓、opt_converged=true。**但几何身份 = (R)-脯氨酸**：RDKit 由 3D 实测唯一立体中心 = 原子 8（Cα，邻接 7C,4N,9C,23H），`_CIPCode = R`；且其输入 `I1_optfreq.gjf`（sha `fb9db8b79c78d333a32d2986f4d114e090b4e5e6d631f6a4c0855f1e26355b0f`）坐标与 `gold_compute/grant_materials_20261001/raw/HI1/job_51/rc_clean_np8.xyz` **逐原子 maxdev = 0.0000 Å** → 用的是历史 R-脯氨酸几何，与 gjf 注释声明的 S 不符（注释/几何不一致）。
- 反向核验：`E1/runs/RC_optfreq/RC_optfreq.log`（job 907）sha256 `fa28545612332f69c60c0b778cd5dd1907b22b8ad36f6b1da7811da1295563ba`，最终几何 Cα **= S**，0 虚频，E = −939.308829219 Eh。
- ⇒ **E1 现有两端点互为对映体（RC=S、I1=R）**；R↔S 不是基元步，**908 不能当 (S)-I1 共享依赖**。已提交 (S)-I1 Opt+Freq 基线 **job 924**，输入 `E2EM1/runs/I1_optfreq/I1_S_optfreq.gjf` sha `8b843b95bb55f46921f9aa23f9c172d906261b881e433db4c419605913cef0a9`（Cα=S 实测）。
- 其余 S 身份复核（均 RDKit 3D 实测 Cα=S）：`E1/build/I1_S_start.xyz`、`E1/build/RC_start.xyz`、`E1/build/TS_guess_merged.xyz`、`E2EM1/build/TS_guess_E2_j58f7.xyz`、`E2EM1/build/TS_guess_EM1_j59f9.xyz`。

**② job 910 重提 = job 925**。根因：l101 把坐标块后的 `B 1 29 1.80` 当坐标行读（**几何与 ModRedundant 卡之间缺空行**）。新输入 `E3/prep/I2_prep_cons180_v3.gjf` sha `4f8c4851b8ba74013c1cc162c1158ce7d826ac93a1637fe446ce1bc5b0c292c3`（旧输入 sha `a1bfb5093857d99e62f238f0e46a968d88f665c8df76855f5cf2f1972de1e8ab`）；route/坐标/约束逐字不变，仅补空行 + %nproc 12→8、%mem 14000MB→8GB。

**③ QM 槽（本包同刻 ≤2）**：slot1 = job 924（(S)-I1 基线；我接管已 failed 的 lane3 令牌，holder.txt 已记）；slot2 = job 925 I2 几何准备。两槽已满。

## 巡检 4（2026-10-15 18:1x，ts_prepare 实测 + 分道派发）

## 巡检 5（2026-10-15 18:2x–18:3x）：各道非 QM 准备已落盘（我逐一真实 sha256sum 复核）

- **lane3（as_2f1b7321a5e042c8）**：`E2EM1/build/TS_SEED_PROVENANCE_E2.md` sha `121ac600…`、`TS_SEED_PROVENANCE_EM1.md` sha `73ee4aa8…`（两条都含源帧 sha + 镜像 maxdev=0.000000 Å + dbg_cip_adduct 原始输出：A {8:'S',29:'S'} / B {8:'S',29:'R'}）；`ATOM_ORDER_AND_WATCHPAIRS.md` sha `6820379b…`（41 原子 work idx↔元素↔map 全表 + source 序 reaction_center=[[1,29],[2,4],[2,1],[28,29]]）；`reorder_guess_by_permutation.py` sha `30e39ec7…`（identity 往返 maxdev=0.000000）。源帧复核：job_58/scan_clean_np8.007.xyz sha `e662627f…`、job_59/scan_minor_clean.009.xyz sha `ae2ca403…`（与自报一致）。基线硬约束已写入 E2EM1/STATUS.md 与 PLAN_LANE3 §5。**未提交任何作业**（等 924）。
- **lane1（as_99941bb328454a0c）**：`E1/TS_GUESS_PROVENANCE.md` sha `d7a82f39…`；`E1/lane1/` 下 `RC_S_canonical.{xyz,mol}`、`TS_guess_merged_canonical.{xyz,mol}`（绑定序版本，含 bond block）、`make_lane1_binding_order.py`（生成脚本）。
- 全部登记进 `PREP_ARTIFACTS.md`（§F）。
- **工具面问题取证（2026-10-15 18:3x，主协调将开 issue #181）**：我本人做了一次**路由探针**：`agent_hub({action:"call", to:"coordinator", message:"【路由探针 · 仅为 issue #181 取证…】"})` → 返回 `data.session_id = as_7479852819ea48c0`、notifications=[{"session_id":"as_7479852819ea48c0","message_event_id":"evt_40b83fd606544028","delivery":"delivered","wake_status":"already_running"}]（即 role 名 "coordinator" 解析到的**不是**本包 as_84bdf87a0f94416c）。同时已请 lane3（观测方 as_2f1b7321a5e042c8）补交 (a) 被拒 call 的完整入参 + 逐字返回 + call_id。
- **工具面问题（登记，待主协调提单）**：lane3 报 `agent_hub call` 到 `as_84bdf87a0f94416c` 被拒（"Delegation would grant permissions absent from the caller: manage"）；且 `post to_agent="coordinator"` 被解析到 NY3 包协调会话 `as_7479852819ea48c0` 而非本包。⇒ 本包统一口径：**各道回报一律 post 到主题 `gold-finish-20261015`，正文首行写 `to: as_84bdf87a0f94416c`**；我不再依赖 role 名解析。

> **时间标注更正**：18:05–18:19 发给主协调的 agent_hub 回执里出现的「18:2x／19:0x／19:2x／19:3x」为误标，实际发出时间为 18:05–18:19（容器 `date` 实测）。文件内时间戳以更正后为准。

- **ts_prepare 已恢复可用**：我用最小声明（E1 合并边：题源映射 SMILES + 单一 profile + generated ETKDGv3 反应物构象 + 8c/8192MB）成功建出 run `/home/ly/Cloudra-mechanism-agent/ts/ts_0004`（**run_id ts_0004，revision 5，status=waiting，stage=build**），它已自动提交 **job 928** = `ts/ts_0004/jobs/declaration_0001/candidate_opt/seed-opt.gjf`。⇒ 上一位 Coordinator 报的 `tool_exception` 是 compute.db 写锁（issue #176）的下游表现，**不是 ts_prepare 自身缺陷**。
- 共享基线证明落地：`shared/SHARED_I1_identity_20261015.md`（含可复现命令与原始输出）+ `shared/I1_identity_20261015.json` + 工具 `shared/tools/hi1_cip_tools.py`。
- 分道派发（新会话，共同纪律：≤2 并发 / ts_prepare-only / 同批 Gaussian 相减 / 缺测不填 0 / 不改题源）：
  - lane1 = E1 合并边：small_mol `as_99941bb328454a0c`（接手 ts_0004；产出 E1/LANE1_STATUS.md）
  - lane2 = HI1_E3：small_mol `as_7da73f2d3f6d40a9`（接手 job 925 → I2 极小值 → 水解 ts_prepare 链；产出 E3/STATUS.md 更新）
  - lane3 = E2/EM1 (S) 重算：small_mol `as_2f1b7321a5e042c8`（基线 = job 924；两通道串行 ts_prepare；产出 E2EM1/STATUS.md 更新）
- 队列状态（18:1x）：924/925/928 均 state=ready（排队，节点被其他包 4×8c 占满）；本包不再加手工作业，等槽空出。

### 引用定位（供主协调逐条引用；shared/SHARED_I1_identity_20261015.md，共 54 行）
- 907 的 log sha256 `fa285456…` → **第 13 行**；908 的 log sha256 `d35b0abf…` → **第 14 行**；908 输入 gjf sha `fb9db8b7…` 与「与 job_51/rc_clean_np8.xyz 逐原子 maxdev = 0.0000 Å」→ **第 15 行**；924 输入 sha `8b843b95…` → **第 16 行**。
- 实测 CIP 的**命令**（python3 hi1_cip_tools.py …）→ **第 20–30 行**；**原始输出**（含 I1_optfreq.log … CIP[8C=R…]、RC_optfreq.log … CIP[8C=S…]、三行 maxdev）→ **第 34–42 行**；方法说明 → **第 44 行**、工具 sha256 → **第 45 行**（更正：先前写 44–48 有误）。
- 机读版：`shared/I1_identity_20261015.json`（907/908/924 的身份、sha256、虚频数、能量）。
- 口径澄清（主协调来函第 3 点措辞）：lane3 的参考极小值是**该步自身起点 = (S)-HI1_I1（烯胺+水+苯甲醛）极小值 = job 924**，不是 E1 的 (S)-RC（job 907）；两者物种不同（907 = 脯氨酸+丙酮+苯甲醛）。lane3 能垒一律相对 924，E1 能垒相对 907。
  - **硬约束（主协调 19:1x 确认，写死）**：lane3 两通道的交付值 = **E(TS) − E(924 极小值)**（纯电子能、同批 Gaussian 16）；**禁止**改用 907、**禁止**用工作流自己的 reactant 端点替换 924；仅当 924 未通过验收（0 虚频 / Cα=S）时才可考虑替代，且必须先向我报备并写明替代 provenance。E1 的能垒则相对 907（或 E1 自身 reactant 端点，须注明）。

## 证据清单（日志绝对路径 + sha256）
待填。

## 分工
- E1 道：small_mol `as_4c9dafe225a84580`
- E3 道：small_mol `as_3b1f55fa9f7743a9`
- 只读审计道：explorer `as_3bbca92b7c0446a5`
- QM lane：`gold_finish_20261015/HI1/qm_lane/`（本包同一时刻只 1 个 Gaussian 作业，≤12 cpus/≤14000 MB）

## 范围变更（主协调 2026-10-15 扩权）：本包 2 边 → 4 边
- 新增 **lane 3**：HI1_E2 / HI1_EM1 的 **(S)-脯氨酸体系重算**（small_mol 会话 as_3509ff4f56ea402c，产出目录 gold_finish_20261015/HI1/E2EM1/）。理由：既有 E2=13.36 / EM1=15.52 建在 R-脯氨酸几何上，与纠正后题源为非对映体关系（L2 证据身份缺口）。规则：复用 E1 道的 (S) RC/I1 几何；两通道各自 TS+Freq+IRC 双向+两端 Opt/Freq；能垒相对同一 (S) I1 极小值；**新值验证通过前不动旧值**，通过后替换并写 provenance（含引擎差异）；ΔΔ 如实报（对比历史 2.16）。
- 本包现在共 4 条边：E1（lane1 as_4c9dafe225a84580）、E3（lane2 as_3b1f55fa9f7743a9）、E2/EM1（lane3 as_3509ff4f56ea402c）。
- 资源：3 道共用 **2 个 QM 槽**（qm_slots/slot1|slot2，提交前 mkdir、run 结束 rmdir；见 qm_slots/README.md）；新提交优先 8 cpus / 10 GB 以内，硬上限 12 cpus / 14000 MB。
## 巡检 2（2026-10-15 16:50–17:00）：首份原生日志到手 + 平台故障
**E1 道（lane1）第一份原生日志（已由我直接解析）**：`gold_finish_20261015/HI1/E1/runs/RC_optfreq/RC_optfreq.log`（4,319,373 B，mtime 16:52:47）
- 41 原子、Charge 0 / Multiplicity 1；route `#p opt freq B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=DMSO)`；Optimization completed + Stationary point found；117 个频率（39 行），最低 9.70 / 14.74 / 25.45 cm⁻¹ → **0 虚频**；最终 `SCF Done E(RB3LYP) = -939.308829219` Eh；**Normal termination** ✓（16:52:47）。
- 结论：E1 道反应物复合物（(S)-脯氨酸 + 丙酮 + 苯甲醛，C15H21NO4）已成为候选极小值；**待 lane1 自己对优化后几何**做身份核验（3 分片 / 无异常成键 / Cα 实测 CIP=S）后才算合格起点。
- 观察（不改口径）：本批 Gaussian 41 原子 C15H21NO4 绝对能量在 −939.31 Eh 量级，历史 ORCA 同式为 −938.76 Eh 量级；跨程序绝对值本就不可比，本包所有能垒只用本批 Gaussian 日志内部相减。

### 巡检 2 补充（Coordinator 独立复核，2026-10-15 17:05–17:15）
- **E1 关键几何 Cα 实测（我的 RDKit 复核）**：`E1/build/TS_guess_merged.xyz` = S（d(C2–N20)=1.95 Å，加成物距离）、`E1/build/I1_S_start.xyz` = S（d(C2–N20)=1.375 Å，烯胺 C=N）、`E1/build/RC_start.xyz` = S（d(C2–N20)=4.008 Å，无成键，反应物复合物）✓。
- **lane3 通道↔CIP 映射已被我独立复现**（用其修正拓扑脚本 `E2EM1/build/dbg_cip_adduct.py`）：ORCA job_58 链 = Cα R + aldol C **R**（R-Pro+R-aldol）→ 镜像 = (S)-Pro+S-aldol = 题源 **E2/I2**；job_59 链 = Cα R + aldol C **S** → 镜像 = (S)-Pro+R-aldol = 题源 **EM1/M1**；历史 E2=13.36（记录 C8R/C29S）实为 job_59 链。**限定：这是几何预测（加成物拓扑 3D 定 CIP），不是 QM 端点证据。**
- **发现一处证据可复现性问题**：`E2EM1/build/check_cip_lane3.py` 的 `adduct` 模式拓扑有 bug——删掉 C6–O5 (28,29) 后未补回单键，导致 aldol 碳只有 3 个邻居，输出 `(8,'?')`/`Tet_CW`（我复现）。已要求 lane3 修正或废弃该模式，并把每条 CIP 结论绑定到实际运行命令 + 输出。
- **镜像等能先验（可证伪，非证据）**：由历史数值推得 (S) 体系 ΔΔ = E(TS_M1) − E(TS_E2) ≈ 13.36 − 15.52 = **−2.16 kcal/mol（与历史反号）**，且与“(S)-脯氨酸→(S)-aldol”的实验方向镜像矛盾 → 又一条支持 L2 身份缺口（历史几何/数值不可靠）的独立线索。已报主协调；纪律：不改图、不改 favored、不继承旧值。
- **平台修复中**（主协调只重启 uvicorn API 释放 compute.db 写锁）。恢复后提交顺序（三道共用 2 槽）：910(E3 I2 几何准备) → (S) I1 极小值 Opt+Freq（lane3，共享依赖，跑完发 lane1 与本文件）→ E1 合并边 OptTS → lane3 两通道 TS 链 → lane2 E3 水解 TS 链。
**平台故障（compute.db 写锁）影响**：所有作业状态写入失败；907 实际已跑完但状态卡 running；903/906 无进程却占 16 核；队列 7 个全停；lane3 的 submit 返回 `database is locked`（job_id=-1）。主协调令：暂停新 QM 提交，继续非 QM 准备与已有原生日志分析；不动数据库/进程/平台文件。

**平台缺陷 #176 的下游症状（已随锁恢复解除；历史报错留档备复核）**：lane1 会话内 ts_prepare 曾**完全不可用**——三种最小输入（reaction-only / reaction+calculations / 加 conformer 文件）均抛 `tool_exception: Tool execution failed internally`（call_id 之一 `tc_81d1fd610acd4957`），无 run_id、无 run 目录、无作业。根因是 compute.db 持久写锁（GitHub issue #176），**不是 ts_prepare 自身缺陷**：2026-10-15 18:35 接班 Coordinator as_84bdf87a0f94416c 用最小声明一次成功建出 run `ts/ts_0004`（rev 5，waiting，stage=build）+ 自动 job 928；与 NY3 的 ts_0002/ts_0003 一起构成「锁恢复后 ts_prepare 恢复可用」的样本（3/3）。原报错文本与 call_id 原样保留。

**lane2（E3）**：无任何原生日志（job 910 = I2 几何准备，从未启动，仍排队）。等待期已完成非 QM 准备：E3 声明的 6 个 concrete watch pairs（按其工作序号 break (2,4)(25,26)(25,27) / form (2,25)(4,26)(28,27)）；I2→P 完整 41 原子 concrete atom_map（`E3/prep/I2_P_atom_map.json` sha `33912bbd415bc424da1f086bc61c696cd6b9eac5f4f2aa7c8b550cd3ce3a980e`）；踩坑记录：`reaction_mapping` 对该边自动映射会把产物酮 O / 羧基 O / 水 O 错配（不要用它定质子来源）。

**lane3（E2/EM1 (S) 重算）**：0 作业（submit 被 DB 锁拒）。已发现 PLAN §3 未列的本地素材：`gold_compute/grant_materials_20261001/raw/HI1/job_58/`（major 通道 ORCA 弛豫扫描 4.3→1.6 Å，9 帧）与 `job_59/`（minor 通道 6.0→2.4 Å，10 帧），并已镜像为 (S) 生成 7 个 TS 种子（`E2EM1/build/TS_guess_*`）；(S) I1 起点 = `E1/build/I1_S_start.xyz`（sha c9d59aea…，与 job_51 逐原子 z 镜像 maxdev=0，Cα 三重积 −5.026→+5.026 = S）。
## 主协调裁定与政策更新（2026-10-15 巡检 1）
- 既有 **HI1_E2=13.36 / HI1_EM1=15.52 保持不动**（本机无 2026-10-01 原生日志，无法本地复核；由主协调写进最终交付）。登记 caveat：题源 step_type 文本声明产物为 (S)，10-14 的改动属 CIP 标记纠正；其 provenance（历史记录为 C8R/R-脯氨酸模型）待有日志的机器复核。本包只做 computed_by_us 的 Gaussian 16 同批能量相减，不与旧 ORCA 值混减。
- 资源政策更新：**每包最多 2 个并发 QM 作业**（单作业仍 ≤12 cpus / ≤14000 MB）。HI1 的 E1 道与 E3 道各自最多持 1 个作业，跨道不再互斥（各道自持 1 个；qm_lane/ 仅作记录，不作跨道锁）。

## 独立审计要点（explorer as_3bbca92b7c0446a5，全文 gold_finish_20261015/HI1/audit/DECLARATION_AUDIT.md）
- 本地可得性（真实 ls/find）：本工作区**不存在** job82 的 I2（sha a618fd1d…，只在索引行/文本里）、job 71/72/83（job 目录内 input.inp 与 run_directory 是悬空软链）、E3 链 114–120、E1 链 94/100/102，也无任何 HI1 的 .cloudra/calc-*.out.log；PLAN §3 四几何 sha 逐字一致。
- 声明自洽性：E1/E3 的 bond_changes 与 mapped_reactants / steps[].out 一一对应；E1+E2+E3 三步逐对相加首尾闭合（净剩 break(3,22)(5,6)/form(3,6)(5,22)）；题源内部 CIP 自洽（map16 全程 S）。
- ⚠ 新事实：四个“可复用几何”脯氨酸中心**全是 R**（T≈−8.39…−8.48）→ 只能作骨架起点，须翻转/重建为 S 并实测 CIP（已写入 PLAN §3 并通知 E1/E3 道；E1 道新建 RC 实测为 S）。
- E3 历史 candidate_only 的缺口分类：TS 单虚频=记录自述；虚频模是否以声明键对为主=不可证明；IRC 双向端点归属=**缺测**；端点物种/质子/立体 CIP=**缺测/不可证明**；能垒=缺测。E1 历史链：TS/IRC/端点/能垒全部缺测，且历史做的是第一子步 carbinolamine（图/粒度层缺口）。
- “atom 27”无法本地裁决：三种可核序号体系下它都落在非手性原子（水 H / 隐式 H / 羟基 H），需原始 verdict 或 I2_start.xyz 才能还原 → 本轮改为让产物自证（输入注释写 map↔本地原子序号对照）。
- E2/EM1 caveat 建议升级（属 L2 证据身份层，非纯 CIP 标记）：(i) 13.36/15.52 来自 R-脯氨酸几何；(ii) favored/minor 通道命名不能在 (S) 题源下原样沿用（镜像论证下历史数值指向 (R)-aldol 更有利，与题源 favored 通道相反）；(iii) 需在仍有 Oct-1 原生日志的机器上重导 C8/C29 CIP 与通道归属。**本包不改这两个值**，仅登记（待主协调确认口径）。
## 关键事实（开工基线与更正）
- 2006-10-15 真实文件系统核对：本工作区无 `gold_compute/remote_backups`，历史产物（job82 I2 sha `a618fd1dcebb32b536c7fbb63a18e2fa8ccebb9538dd437bf9dd8c63583af10f`、E3 的 114–120、E1 的 94/100/102）**均不在本地**；可复用几何起点只有 job_51/52/54/64（见 PLAN §3）。
- 旧值作废不回填：HI1_E1 19.2、HI1_E3 16.9/19.2。
- 题源一致性问题（报主协调）：E2/EM1=13.36/15.52 建在 C8R（R-脯氨酸）模型，与 2026-10-14 纠正后的 (S)-脯氨酸题源不一致。

---

## R5 接任块（第 4 任 Coordinator as_d9005401ea014f4e，2026-10-17 06:3x；真实文件系统/工具读数）

**平台**：已恢复（query_compute_queue 正常，0 running / 0 queued / free 10 槽 32c；987/988 收尾 failed，986 done）。前几任包会话均被重启收尾 failed，本包磁盘产物完整（最后一次落盘 = 2026-10-16 01:55 job 980）。**回填仍为 0/3**。

**本轮我把三条 run 的权威状态与一个关键新读数补齐**（ts_inspect + 真实 sha256sum）：
- ts_0004：rev8 blocked / conformer_optimization_failed（job 928 l202，平台 ETKDGv3 种子 H35···H36=0.299 Å）→ 保留为 #180 证据，不动。
- ts_0008（HI1_E1）：rev8 blocked / missing_input / needs=conformers.product（reactant 文件 + provided guess 已在位；7 对 reaction_center 已声明）。
- ts_0009（HI1_E2）：rev12 blocked / map / atom_map_missing（两端点已 concrete：reactant I1_S_start.xyz + I1_S_start_bonded.mol；product TS_guess_E2_j58f7.xyz + _adduct.mol）。
- ts_0011（HI1_E3）：rev9 blocked / map / input_identity_unconfirmed，仅缺 conformers.reactant.heavy_atom_binding（product 侧 binding 已通过；atom_map 41 项 + 6 对 reaction_center 已在位；reactant_smiles 已是 E 标记形式）。

**★ 新证据：job 980（E3 延伸约束扫描 C2–O25 2.20→1.60 Å）于 2026-10-16 01:55:25 Normal termination**
- 日志 E3/runs/preorg_v3/scan_c2o25_220_160.log sha256 436c4cd9225bd29c1ae65086e1394b27b886e4d45206f4efa91133b331030f66
- 5 个收敛扫描点：R(2,25) = 2.1996 / 2.0496 / 1.8996 / 1.7496 / 1.5996 Å；该点末次 SCF = −939.307665623(L6225) / −939.302902987(L16443) / −939.297771992(L25258) / −939.301357590(L53388) / −939.309047571(L59324)
- 相对 job 961 I2 极小值（−939.320655479）：+8.16 / +11.15 / +14.37 / +12.11 / +7.28 kcal/mol → 与 3.16→2.20 Å 段的单调上升（端点 +8.15）拼起来是**单一内部极大（≈1.90 Å，约束上界）**。约束峰不作能垒，但 1.90 Å 帧是合格 TS 初猜来源。
- 意义：E3 从「无内峰/峰必在 2.20 Å 之后」升级为「已定位约束极大区」，lane2 可直接用它建链。

**本轮派发（新会话，关键路径并行，均带完整交接）**：
- lane1 = HI1_E1：small_mol as_700f852fe3af412f（跑 ts_0008 的 conformers.product + provided guess 链；跨会话不可续则 ts_prepare 重建；7 对合并边若确无单鞍点 → 交拆步证据包）。
- lane2 = HI1_E3：small_mol as_06db52ada5014800（修 ts_0011 的 reactant heavy_atom_binding + reactant MOL；provided guess = job 980 的 1.8996 Å 帧 + provenance 文件；6 watch pair 对齐全链）。
- lane3 = HI1_E2/EM1：small_mol as_375f0d91a9bc43f2（ts_0009 补 41 原子 concrete atom_map（product 序、含 H）+ provided guess 重排；通道 A 先、B 后；ΔE‡ 相对 job 924）。

**三条边的能垒基准（同批 Gaussian 16，禁用旧 ORCA 值）**：E1 = job 907（−939.308829219，L59761，(S)-RC，0 虚频）；E3 = job 961（−939.320655479，L16950，实测互变体 aldol-OH + 羧酸根 + 旁观水，0 虚频）；E2/EM1 = job 924（−939.308218263，L20025，Cα=S，0 虚频）。

**回填前置**：改动前基线 = pytest tests/test_benchmark.py -k regenerate_identically -q → 4 passed（第 3 任已测，本轮回填前重跑）。属主：cloudra/benchmark/hard_registry/hi.py + ideapool/tasks/hard/HI1.json（重生成）+ ideapool/reaction_candidates/hard.md 的 I1 行。

**待办（本人）**：① 收三条 lane 的终态并核证据；② 视结果回填（含 §9 证据驱动的机理修订单列节）；③ 交付必须显式声明 Gaussian 16 替代 ORCA、L2 身份缺口（13.36/15.52 的 R-脯氨酸 provenance）、(S) 题源下 E2/EM1 通道命名不可沿用。

---

## R6 接任块（第 5 任 Coordinator as_4f933afb7d98418e，2026-10-17 06:3x–07:1x；**整合 + 回填轮**）

**身份/权限**：本会话 = HI1 包第 5 任 Coordinator，session `as_4f933afb7d98418e`（parent = 主协调 `as_a341823c436e47ed`），**本包唯一有权写本文件的会话**。第 4 任 `as_d9005401ea014f4e` 已 succeeded 结束；它派出的三道 small_mol 会话仍在 running，回报口径改为「post 主题 gold-finish-20261015 + 正文首行 to: as_4f933afb7d98418e」。本轮已向三道投递交接令（lane1 call 回执 evt_46e7c15b5d5142f8 / lane2 evt_cdb28d937b4b4d3d / lane3 evt_2b444a1d80c84963，均 delivered、wake_status=already_running）。

### R6.1 本轮权威 run 状态（`ts_inspect` 实读，2026-10-17 06:3x–06:5x）

| run | 边 | rev | status | stage | failure_class | needs | owner_session_id（落盘 process.json） | owner 会话 state |
|---|---|---|---|---|---|---|---|---|
| ts_0004 | HI1_E1（旧） | 8 | blocked | build | conformer_optimization_failed | conformers.reactant | as_84bdf87a0f94416c | failed |
| ts_0008 | HI1_E1 | 8 | blocked | build | missing_input | conformers.product | as_fc7fdbb5e5564d93 | failed |
| ts_0009 | HI1_E2 | 12 | blocked | map | atom_map_missing | reaction.atom_map | as_bc146127755a404d | failed |
| ts_0011 | HI1_E3 | 9 | blocked | map | input_identity_unconfirmed | conformers.reactant.heavy_atom_binding | as_e5bb8c58d7b84e9c | failed |

四条 run 的 `result` 均为 null（无 verified 判定）。**ts_0010（rev22 / refine / job 988 irc failed）与 ts_0007 属 HL1 / NY3 包，不是本包资产，勿动。**

### R6.2 ★ 结构性风险：四条 run 的 owner 会话**全部已 failed**（issue #180 同型）——⚠ **本节「预期被拒」的结论已被 §R6.8(A) 更正：跨会话 ts_resume 在本平台未复现拒绝**

- 预期：跨会话 `ts_resume` 被平台拒（逐字 "TS process belongs to a different project or owner"）。本轮已令三道：**先各试一次 ts_resume 并逐字留证（拒绝文本 + call_id，作 #180 证据）**，随后用 `ts_prepare` **重建同一声明**（reaction / conformers / guess / calculations 逐字照抄），把新 run_id 与声明内容写回各自状态文件。
- 因此 ts_0004 / ts_0008 / ts_0009 / ts_0011 的价值 = **声明内容模板 + #180 证据**（ts_0004 另含 job 928 的 l202 种子重叠证据）；**不删除、不修改**。

### R6.3 参考极小值 / 关键证据（同批 Gaussian 16；本轮**真实 sha256sum** 复核通过，未改字节）

| 用途 | 作业 | 日志（相对 gold_finish_20261015/HI1/） | sha256 | E(RB3LYP) / Eh | 结论 |
|---|---|---|---|---|---|
| E1 起点 | 907 | `E1/runs/RC_optfreq/RC_optfreq.log` | fa28545612332f69c60c0b778cd5dd1907b22b8ad36f6b1da7811da1295563ba | -939.308829219（L59761） | (S)-RC，0 虚频 |
| E3 起点 | 961 | `E3/runs/I2_optfreq/I2_optfreq.log` | 63dda25e04529e65920526304fb88755db9393e9c22bd3a6efb76eeee0af0d0e | -939.320655479（L16950） | 实测互变体 aldol-OH + 羧酸根 + 旁观水，0 虚频 |
| E2/EM1 起点 | 924 | `E2EM1/runs/I1_optfreq/I1_S_optfreq.log` | 6ecf06238ee6e1e976ba30eb15faf655f3ebe5a0126ed37d0dfe9b687dea6a87 | -939.308218263（L20025） | Cα=S，0 虚频 |
| E3 初猜来源 | 980 | `E3/runs/preorg_v3/scan_c2o25_220_160.log` | 436c4cd9225bd29c1ae65086e1394b27b886e4d45206f4efa91133b331030f66 | 5 点末 SCF 见 R6.4 | 约束单峰 ≈1.90 Å；能量不作能垒 |
| E1 反应物文件 | — | `E1/lane1/RC_S_canonical.xyz` | 71b23e07b73a7241e19c3c94e927040f5f113f815184bfa44387d58bbc0e6597 | — | 绑定序输入 |
| E1 provided guess | — | `E1/lane1/TS_guess_merged_canonical.xyz` | a2c0fa28667eb5afd814d8b876f40dd5873967c8a63973ff89bf9b0d0b980c4c | — | evidence_refs = `E1/TS_GUESS_PROVENANCE.md`（d7a82f39e7d068400a0da60d4b59b7679c66441fd13cf885bb25f909f37a3276） |

**能垒口径（写死）**：ΔE‡ = E(TS) − E(该步自身起点极小值)，纯电子能、同批 Gaussian 16、同机同方法（B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight + CPCM(DMSO)，q0/m1）。**禁止与旧 ORCA 值相减**；E2/EM1 禁止改用 907、禁止用工作流自身 reactant 端点替换 924（除非 924 未过验收并先报本会话）。

### R6.4 三道现状与本轮收到的回报

- **lane1 = HI1_E1**：small_mol `as_700f852fe3af412f`（running）。回报 evt_2740fef4b40f4108：ts_0008 rev8 blocked / missing_input / needs=[conformers.product]；candidate_opt **job 968 已完成**（artifacts `ts/ts_0008/jobs/declaration_0001/candidate_opt/seed-opt.log`）；计划补 product 显式构象源（`E1/build/I1_S_start.xyz` sha c9d59aeab418c248629922ee37d4ea3822c64b7128dd63b3034d3c8c5ec2df3d + 自建 MOL + heavy_atom_binding 20 重原子）后推进（按 R6.2 改为重建）。**尚无 TS/freq/IRC → 无 ΔE‡**。lane1 已声明不再让其它道碰 ts_0008/HI1_E1 目录。
- **lane2 = HI1_E3**：small_mol `as_06db52ada5014800`（running）。回报 evt_910064dd43994d1f：ts_0011 rev9 blocked / input_identity_unconfirmed / needs=[conformers.reactant.heavy_atom_binding]（product 侧 binding 已接受）；atom_map 41 项 + reaction_center=[[1,3],[1,24],[24,25],[24,26],[3,25],[10,26]]（0-based 落盘 = 1-based 断 (2,4)/(25,26)/(25,27)、成 (2,25)/(4,26)/(11,27)）已在位；guess=null；planned 计算全为 gaussian/b3lyp/def2svp。lane2 独立复核 job 980：E = -939.307665623(L6225) / -939.302902987(L16443) / -939.297771992(L25258) / -939.301357590(L53388) / -939.309047571(L59324)，R(2,25) = 2.1996 / 2.0496 / 1.8996 / 1.7496 / 1.5996 Å → 相对 961 = **+8.15 / +11.14 / +14.36 / +12.11 / +7.28 kcal/mol**（3.16→2.20 段单调上升，故该一维切片内部极大 ≈1.90 Å，**约束峰 ≠ TS**）；1.8996 Å 帧作 provided guess。**同表实测**：R(2,4) 1.3051→1.4012、R(10,27) 1.6747→1.0048（水中 H27 转移到羧酸根 O10）、R(25,26) 0.9675→0.9694（H26 全程留 O25）⇒ 该扫描只覆盖「水逼近 C2 + 羧酸根质子化」，**不含 C2–N4 断裂 / H26→N4**。机制修订（§9）：E3 起点参考态 = 实测 I2 侧互变体，与题源声明的 alkoxide+COOH 只差 H24 位置（质子互变异构体）。
- **lane3 = HI1_E2/EM1**：small_mol `as_375f0d91a9bc43f2`（running）。回报 evt_6dfac2c1232b4f99：ts_0009 rev12 blocked / atom_map_missing；已逐原子核验两端点并声明 **41 原子恒等 atom_map**（reactant = `ts/ts_0009/jobs/declaration_0002/candidate_opt/optimized_seed.xyz` sha ffb7569f3662d878d77a028e28ba8351431c077561646284810c2764c3c5f3aa；product = `ts/ts_0009/build/input_0002/product/seed.xyz` sha 9e5ccc2fe5dde2e4c1900ad53cc8c1ddbae0e654a618c138adaffa58dd522e38），唯一连接性变化 = 新增 C1–C29，reaction_center=[[1,29],[2,4],[2,1],[28,29]]（= 生成中的 C3–C6 = work 原子 1 与 29）。**一次 ts_resume 被平台输入校验拒**（与 map 无关）：product 继承的 heavy_atom_binding 判 "declared identity: CC(C[C@H]([O-])c1ccccc1)=[N+]1CCC[C@H]1C(=O)O.O vs concrete identity: C/C(C[C@H]([O-])c1ccccc1)=[N+]1\\CCC[C@H]1C(=O)O.O"（几何→图推断的甲基/环构象与声明 SMILES 描述符不一致）→ 本轮指导：**改声明文本使其与 concrete 图一致，不动已核验几何**；若拒绝文本再次出现，逐字留证（可能是平台输入校验层的候选 issue 证据）。两通道（A = E2 → HI1_I2，map6=S；B = EM1 → HI1_M1，map6=R）均无 TS/freq/IRC → **无 ΔE‡ / 无 ΔΔ**。
- **共同欠缺**：TS（恰 1 虚频）/ 双向 IRC（或 BRIEF §9 替代口径）/ 两端点 Opt+Freq / ΔE‡ —— 四条边**回填 0/4**。

### R6.5 回填靶点（机读；本轮**尚未改动任何靶点**）

- `cloudra/benchmark/hard_registry/hi.py`：105 行，本轮实读 sha256 `a0372a924ed90962ff819d5b3919535d81f7c34396d2d26ea68bf9ba2562094c`。I1 结构 ↔ 边映射（已逐条核对）：`I1.steps[0].barrier = None` ← **HI1_E1**；`steps[1].barrier = 13.36` ← **HI1_E2**（channel=major_face）；`steps[2].barrier = None` ← **HI1_E3**；`I1.competing[0].barrier = 15.52` ← **HI1_EM1**（channel=minor_face, from_step=1, is_product=False）。
- 同步件：`ideapool/tasks/hard/HI1.json`（由 hi.py 重新生成）+ `ideapool/reaction_candidates/hard.md` 第 112 行 I1 行。
- 守卫：`python -m pytest tests/test_benchmark.py -k regenerate_identically -q`。**改动前基线（本轮实测）= 4 passed / exit 0**（无预存漂移）。
- 若 E1 合并边经证据确认无单鞍点需拆步：节点/边划分属**机图改动，只有本人执行**（lane 只交提案）。

### R6.6 交付必须显式声明的三项（沿用 R5）

① **引擎偏差**：本批以 Gaussian 16（B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight + CPCM(DMSO)，q0/m1）替代既有 58 条 gold 的 ORCA 5.0.2/6.1.1；跨程序不得相减。
② **HI1 的 L2 身份缺口**：历史 HI1_E2=13.36 / HI1_EM1=15.52 建在 **R-脯氨酸几何**上（4 个可复用几何 Cα 实测全 R），与纠正后的 (S) 题源为非对映体关系；本机无 Oct-1 原生日志 → 无法本地复核。只有本批 (S) 体系实测替换值通过验收后才替换并写 provenance，否则保留旧值 + 登记缺口。
③ **(S) 题源下 E2/EM1 通道命名不可原样沿用**（镜像论证下历史数值指向 (R)-aldol 更有利，与题源 favored 通道相反）。

### R6.7 四条边的当前交付判定（本轮权威）

| 边 | 判定 | 缺什么 | 已证伪 / 已排除 |
|---|---|---|---|
| HI1_E1 | **缺测** | TS（恰 1 虚频）+ 双向连通 + 两端 Opt/Freq + ΔE‡（基准 907 = -939.308829219） | 平台 ETKDGv3 反应物种子不可用（H35…H36 = 0.299 Å → l202，job 928 证据）；R↔S 不是基元步（907=S / 908=R 互为对映体，908 不能当 (S) 基线） |
| HI1_E3 | **缺测** | TS + 连通 + 两端 + ΔE‡（基准 961 = -939.320655479） | 题源声明的 alkoxide+COOH 质子位置在本级 QM 下不是驻点（H24 自发到 O28）；约束扫描单峰只给初猜、能量不作能垒 |
| HI1_E2 | **缺测** | 通道 A TS + freq + 连通 + 端点 + ΔE‡（基准 924 = -939.308218263） | 历史 13.36 建在 R-脯氨酸几何 → 不可用 |
| HI1_EM1 | **缺测** | 通道 B 同上 | 历史 15.52 同上 |

**队列/容量快照（06:4x 实测）**：node-local online；running = job 989（NY3 E1 扫描，非本包）；queued 0；free 9 槽 / 24 cpus / 41200 MB。本包手工在飞 = 0。

### R6.8 ⚠ 同轮更正 + lane3 新证据（2026-10-17 07:1x，真实工具读数）

**(A) R6.2 的「跨会话 ts_resume 预期被拒」在本平台未复现 —— 结论更正（原文不删，以本节为准）**
lane3（`as_375f0d91a9bc43f2`）在其会话内对 ts_0009 的 `ts_resume` **被正常接受**：resume #1 **rev 12→13**（request_key `tc_cafbf2fec2e14c24`，request_digest `1dff4afd4d53bebcde91a81f898d4a8c3edb504e579be4a780ca7e7a78f36858`，receipt.status=accepted，changes 含 reaction.atom_map / reaction.product_smiles / reaction.reaction_center / calculations.lane3_g16_dmso / ts_optimization / verification.*），平台回读 revision=13、input_revision=3；**未出现** "TS process belongs to a different project or owner"。更早一次 resume 的拒绝是**参数形状**错误与 **product 身份**错误，均非 owner 拒绝。
⇒ **口径更正**：三道**优先 ts_resume**（保留既有 run 的声明与证据），只在真出现 #180 逐字文本时才用 ts_prepare 重建；已同轮通知 lane1（evt 已投递）与 lane2。要求各道把 resume receipt（request_key / revision / input_revision / changes / retained / invalidated）写进状态文件。

**(B) product 身份拒绝的根因与修复（lane3，已通过校验）**
逐字拒绝文本："...product: inherited heavy-atom binding is invalid: The concrete structure's molecular graph or stereochemistry differs from the declared SMILES. Declared identity: CC(C[C@H]([O-])c1ccccc1)=[N+]1CCC[C@H]1C(=O)O.O; concrete identity: C/C(C[C@H]([O-])c1ccccc1)=[N+]1\CCC[C@H]1C(=O)O.O. Changing binding indices cannot repair this identity mismatch."
根因 = 声明缺 C2=N4 的 **E/Z（STEREOCIS）**。RDKit 复核 `ts/ts_0009/build/input_0002/product/seed.mol` 的 canonical isomeric SMILES **逐字等于** concrete identity，且同一 mol 的 3D CIP = 1-based 原子 **8 = S（Cα）/ 原子 29 = S（aldol C）** = 通道 A 要求的 I2（map6=S）。修法 = 把 product_smiles 改为该 concrete 字符串（**不动已核验几何**）→ 校验通过（rev 13 accepted）。

**(C) lane3 当前阻塞（rev 16，平台输入校验、非化学问题）**
`status=blocked / stage=build / failure_class=input_identity_unconfirmed / needs=["conformers.reactant"]`，文本："reactant: The concrete structure has 2 symmetric heavy-atom bindings; without concrete atom-map labels the binding is not unique."
lane3 已定位根因 = 遗产声明的 reactant 标签 SMILES 把 `[CH3:1]` 与 `[CH2:3]` 指到同一对 C（concrete 原子 3=CH3 / 原子 1=CH2）⇒ 重原子匹配有 2 解；正在提交显式 heavy_atom_binding indices 解锁。atom_map（恒等 1..41）与 reaction_center=[[1,29],[2,4],[2,1],[28,29]]（平台内部 0-based 存为 [[0,28],[1,3],[1,0],[27,28]]）**已被接受**。

**(D) R6.1 表中 ts_0009 的 rev/状态以本节为准**：rev 12→13→**16**（blocked / input_identity_unconfirmed / needs=[conformers.reactant]）。

**(E) 四条边判定不变：仍为 0/4 回填**（E2/EM1 仍缺 TS / freq / 双向连通 / 两端点 Opt+Freq / ΔE‡，无值可回填）。

### R7 增量（2026-10-17 07:2x–07:4x；三道回报 + 我独立复核）

**★ #180 口径彻底更正：跨会话 ts_resume 已两次被正常接受（两条 run 的 owner 会话都是 failed）**
- lane3：ts_0009 rev 12→13（request_key tc_cafbf2fec2e14c24，digest 1dff4afd…f36858，receipt.status=accepted）。
- lane1：ts_0008 rev 8→**9**（call_id/request_key **tc_4d31217523af4aa2**，request_digest **2f0388da3eefc1696fed781939f710f1ea23e6dca273a144bcd1c91255983c42**，previous_input_revision 1→2，changes=["conformers.product"]，retained=[]，invalidated=[{declaration_revision 1, stage_key candidate_opt, attempt 1, job_id 968}]，status=accepted）。
⇒ 本包不再把「ts_prepare 重建」当默认路径；ts_0004 仍保留为 l202 平台种子证据（H35…H36 = 0.299 Å）。请主协调在 #180 定性时按 run 区分（ts_0001/ts_0002/ts_0004 的拒绝文本仍有效；ts_0008/ts_0009 接受是反例）。

**ts_0008 现状（我本轮 ts_inspect 独立复核）**：revision=**12** / status=**waiting** / stage=build / blocked=null / waiting_for=[job **991** candidate_opt, state=running, 8c/8192MB, input_path ts/ts_0008/jobs/declaration_0002/candidate_opt/seed-opt.gjf, input_revision 2]。

**lane1 的 product 端点证据（我用真实 sha256sum 复核，三个 sha 全部逐字相符）**
| 文件 | sha256 |
|---|---|
| `E1/build/I1_S_start_bonded.mol` | 69de27c2a3319074932fb4bb6e2107431e11608f240df8948bb549b8b7921fd9 |
| `E1/I1_PRODUCT_PROVENANCE.md` | 07f4bd00907a76630cf189f52960b2014a14497d394176c8565c94783725e0f4 |
| `E1/verify_product_endpoint.py` | 47dbadaddfa471928cbe933f800ae6fc40eaeaf85f344bd4e341a177c3bdcc68 |
lane1 报告的核验结论（element/coords identical、Kekulize 归一后键表 identical、canonical SMILES = C=C(C)N1CCC[C@H]1C(=O)O.O.O=Cc1ccccc1、3 组分 C15H21NO4、形式电荷全 0、CIP 原子 8 = S = map16、heavy_atom_binding.indices=[3,2,1,4,5,6,7,8,9,10,11,25,28,29,30,31,32,33,34,35]）**属 lane1 自报，尚未由我逐原子重跑**（交付前若要引用我会重跑 verify_product_endpoint.py 并记录输出）。
lane1 亦提醒（与 STATUS 既有口径一致）：job 908 的输入几何是 I1_S_start.xyz 的 z 镜像、终态 CIP=(R) ⇒ **E1 的 ΔE‡ 基准只用 job 907 (S)-RC**；(S) 产物侧参照 = job 924。

**lane1 行号复核（自报，供交付引用）**：907 RC_optfreq.log L59761 原始行 ` SCF Done:  E(RB3LYP) =  -939.308829219     A.U. after    6 cycles`；L60132 Optimization completed.；L66757 Normal termination；L62670 ` Frequencies -- 9.7022 14.7388 25.4515` ⇒ 0 虚频；末帧 C2···N20 3.753 Å（松散预复合物，3 组分分离）。

**三道进度（07:4x）**：lane1 ✅ resume 通过 + job 991 在跑；lane2 ⏳ 未回报（ts_0011 rev9 blocked 待 resume）；lane3 ⏳ ts_0009 rev16 blocked/needs=[conformers.reactant]（见 R6.8 C）。**四条边回填仍 0/4**。

**队列（07:4x 实测）**：running = job 991（ts_0008 candidate_opt，本包管线）+ job 989（NY3）；本包手工在飞 0。

### R8 增量（2026-10-17 07:5x；管线推进快照）

- **ts_0008（HI1_E1）**：rev **12** / waiting / stage=build / waiting_for job **991** candidate_opt（running）。
- **ts_0009（HI1_E2）**：rev **20** / waiting / stage=build / waiting_for job **993** candidate_opt（running）⇒ lane3 已解锁 reactant 显式 binding 并让管线推进（R6.8 C 的阻塞已过）。
- **ts_0011（HI1_E3）**：rev **23** / waiting / **stage=refine** / waiting_for job **999** ts_opt（ready，等 8c 槽）⇒ build 段已完成，管线进入 TS 优化。
- 三条 run 的 blocked 均为 null、result 均为 null（**尚无 verified 判定、仍 0/4 回填**）。
- 队列（07:5x 实测）：running = 991 / 992 / 993 / 995（各 8c，全机 32 核满载）；queued = 996 / 997 / 998 / 999（= 本包 ts_0011 ts_opt）/ 1000；free = 6 槽 / 0 cpus / 14336 MB。本包手工在飞 0（三条都是 ts_prepare 管线自动作业）。
- **主协调 07:5x 路由广播已转发三道**（终态帖首行 to: as_a341823c436e47ed + cc 本会话；帖内必需字段清单；中途进展写各自状态文件；HI1 的回填写权在本会话）；另转发「Gaussian 只认 def2SVP（无连字符）」。
- 待办（本人）：收到任一条边的完整证据链 → 回填 hi.py 的 I1.steps[0]/[1]/[2]/competing[0] + 同步 HI1.json + hard.md 第 112 行 + 守卫 regenerate_identically（改前先跑基线）。

---

## R8 接任块（第 6 任 Coordinator `as_ec848a7673b74e35`，2026-10-17 07:5x；**本文件唯一写者**）

### R8.0 主协调编排更新（收到广播 `evt_4d0671dac90b412c`，2026-10-17 08:0x）+ 本包回填写权声明

- **回报路由**：各道终态帖 **首行写 `to: as_a341823c436e47ed`（主协调，跨唤醒常驻）**，需要时再 cc 本包 Coordinator；中途进展写各自 STATUS.md。本包三道已按此执行（其帖首行多为 `to: as_ec848a7673b74e35` + cc 主协调，两条路由信息都在）。
- **回填写权**：广播第 4 条要求「registry / task json / md / 生成器 / regenerate_identically 由主协调按边指定的唯一写权会话执行」。本包第 6 任 Coordinator 的上工序任务书（用户/主协调下发的 HI1 包任务）明确要求 ③「拿齐后回填 hi.py + ideapool/tasks/hard/HI1.json + hard.md 的 I1 行 + gen_hard_tasks + pytest -k regenerate_identically」。⇒ **本会话按任务书自认 HI1 的回填写权会话**（仅 HI1 相关行；不动生成器/评分规则/其它题；不改 git 提交）。若主协调另指定写权会话，请在主题回帖并以该指定为准（本人不会并发写同一行）。
- **机器**：Gaussian 只认 `def2SVP`（无连字符）——本包所有新输入沿用。
- 队列（08:0x 实测）：running = 991 / 993 / 995 / 996（各 8c，32 核满）；queued = 997 / 998 / **999（ts_0011 ts_opt）** / 1000；free.cpus=0。不重复提交、不改 priority、不杀他人作业。

### R8.7 增量（2026-10-17 07:1x；本人实测）

- **新 run：`ts_0012` = HI1_EM1（通道 B）**（lane3 建并驱动）。`ts_inspect` 实读：revision=**5** / status=**waiting** / stage=build / result.outcome=**null** / waiting_for=[{job_id:**1000**, purpose:candidate_opt, state:ready, 8c/10240MB, source_input_revision:1, input_path `/home/ly/Cloudra-mechanism-agent/ts/ts_0012/jobs/declaration_0001/candidate_opt/seed-opt.gjf`}]。⇒ 本包活跃 run = **ts_0008（E1）/ ts_0009（E2）/ ts_0011（E3）/ ts_0012（EM1）**，另有 ts_0004 作 #180 证据（不动）。
- **我对 lane2 的 provided guess 独立读数**（真实 `sha256sum` + python 读文件，非转述）：`E3/prep/guess_c2o25_190/ts_guess_c2o25_190.xyz` sha256 **`2568ca035c3ee37dc9472cd86bd3a751547ba835f99332cf8ce2ac91177bb186`**（与 lane2 自报逐字一致）、41 原子、元素序 `CCCNCCCCCOOHHHHHHHHHHHHHOHHOCCCCCCCHHHHHH`；实测 R(2,25)=**1.8996**（= job 980 第 3 个约束点的目标值）、R(2,4)=1.3308、R(25,26)=0.9693、R(25,27)=1.0317、R(10,27)=**1.5015**、R(28,24)=0.9831、R(11,24)=1.7845 ⇒ 与 lane2 所述「H27 位于水 O25(1.03 Å) / 羧酸根 O10(1.50 Å) 之间、C2–N4 未断」一致。**该帧仍只是初猜（约束扫描帧），不是 TS 证据、其能量不作能垒。**
- 主协调队列纪律（广播 `evt_c8a52d5ce1a14cf5`）已遵守：本包 **不再新增手工作业**；管线作业排队期间只做非 QM 准备（STATUS.md / provenance / 机理修订文本）。本包手工在飞 = 0。

### R8.8 交付待用：证据驱动的机理修订（**草案**，待 TS 终态后定稿；依 BRIEF §9）

格式 = 旧 → 新 + 依据 + 影响面；三项目前可写、且有证据支撑的内容：

1. **HI1_E3 参考态（质子化位点重定，最高把握的一项）**
   - 旧：题源 `I1.steps[2]` 的反应物 = 亚铵 + **alkoxide `[O-:5]` + COOH `[OH:15]`**（water O 为 O4）。
   - 新（按实测）：该步起点参考态 = **aldol-OH + 羧酸根 + 旁观水**（即 protonation 位点在 O28/aldol 醇、羧基以 carboxylate 存在），`E = -939.320655479` Eh（job 961）。
   - 依据：job 961 无约束 Opt+Freq 收敛到该互变体（0 虚频、117 模、最低 35.3075 cm⁻¹、Normal termination L24001、SCF L19183），且 job 951 弛豫扫描帧 6→7 实测 H24 由 O11 转移到 O28 并伴随 10.11 kcal/mol 下降；化学上 DMSO 中羧酸（pKa≈2–4）远强于 aldol 醇（≈15–17）。题源声明的 alkoxide+COOH 在本级 QM 下**不是驻点**。
   - 影响面：E3 的 ΔE‡ 基准（961 而非另取）；该步的质子记账与 watch pair 归属；**不改 registry 的图/其它边**。
2. **HI1_E1 粒度（条件项，取决于 TS 终态）**：若合并边（7 对：断 (2,4)/(3,22)/(20,21)，成 (2,3)/(2,20)/(4,21)/(4,22)）在管线内确无可信单鞍点（虚频模不落在声明对 / 优化坍缩回两端），则按 §9(4) 记「无独立鞍点」并给替代口径（受约束单峰剖面 + 峰帧 + 两端点 0 虚频身份），或按证据拆步（RC→carbinolamine / carbinolamine→I1+水）。**拆步属机图改动，只有本会话执行**。
3. **HI1_E2 / HI1_EM1 通道命名（必须显式声明，不原样沿用）**：(S) 题源下历史 `major_face`=13.36 / `minor_face`=15.52 建在 **R-脯氨酸几何**（L2 身份缺口），镜像论证下历史数值指向 (R)-aldol 更有利、与题源 favored 通道相反 ⇒ 本批改记为 **通道 A（→HI1_I2，map6=S）/ 通道 B（→HI1_M1，map6=R）**，值只用本批 (S) 体系实测 TS 差（相对 job 924）；旧值在替换前不动、替换后写 provenance。

**交付必须显式声明的三项**（沿用 R5/R6.6，逐字重申）：① 引擎偏差——本批 Gaussian 16（B3LYP/def2SVP+GD3BJ+Int(UltraFine)+SCF=Tight+CPCM(DMSO)，q0/m1）替代既有 58 条 gold 的 ORCA；跨程序不得相减。② HI1 的 L2 身份缺口——历史 E2=13.36 / EM1=15.52 建在 R-脯氨酸几何，非对映体关系，本机无 Oct-1 原生日志无法本地复核。③ (S) 题源下 E2/EM1 通道命名不可原样沿用。旧值 19.2 / 16.9（HI1_E1 / HI1_E3）已作废不回填。

### R8.9 巡检 #2（2026-10-17 07:2x；本人 `ts_inspect` + 真实文件读数）

| run | 边 | rev | status | stage | waiting_for | **result.outcome** | 原生日志现场读数 |
|---|---|---|---|---|---|---|---|
| ts_0008 | HI1_E1 | 12 | waiting | build | job **991** candidate_opt **running** | **null** | `seed-opt.log` 2,051,918 B，mtime 07:12 仍在增长（SCF 段） |
| ts_0009 | HI1_E2 | **33** | waiting | **refine** | job **1008** **ts_opt ready** | **null** | `declaration_0004/candidate_opt/seed-opt.log` **Normal termination 07:07:34**（candidate_opt 完成，run 已自动推进到 ts_opt） |
| ts_0011 | HI1_E3 | 23 | waiting | refine | job **999** ts_opt **running** | **null** | `declaration_0004/ts_opt/refine.log` mtime 07:12 增长中（SCF 段） |
| ts_0012 | HI1_EM1 | 5 | waiting | build | job **1000** candidate_opt **running** | **null** | `declaration_0001/candidate_opt/seed-opt.log` mtime 07:12 增长中 |

- 队列（07:2x）：running = 991 / 998 / 999 / 1000（各 8c，32 核满）；queued = 1001…1008（含 **1008 = ts_0009 的 ts_opt**）；terminal 新增 993 done、995 done、996/992/994 done、997 failed（非本包）。本包手工在飞 = 0（遵守队列纪律）。
- **本包两条边的 TS 优化作业已进入管线**（ts_0011 job 999 运行中、ts_0009 job 1008 排队），E1（ts_0008）仍卡在 candidate_opt、EM1（ts_0012）在 candidate_opt。**四条 run result 仍全为 null ⇒ 回填 0/4。**
- 时间口径（本轮更正确认）：**AgentHub 帖的 `created_at` 是 UTC**，本机 `ls`/日志为 CST（UTC+8）。搜索确认三道与历届 Coordinator 的帖均已在主题内（lane1 的接管自检帖 `evt_04539c2285544d13`、lane3 的 `evt_57e60b8e946d4b25`、第 5 任 STAND-DOWN `evt_732446d5a9164b9f`、第 4 任回执 `evt_fd3c495f1b384936`）。本文件既有的 hub 事件时间若与本地时钟不一致，一律以「本地 CST」与我登记的 `ls` mtime 为准（仅时间标注受影响，id/sha/数值不受影响）。

### R8.10 主协调 R9 询问的判定（2026-10-17 07:3x；我实测 + 已回帖 `evt_52be99b9742c41e7`）

**问题（主协调）**：job 991（ts_0008 的 candidate_opt）末次 SCF = `-939.308829132` 与 job 907 RC 极小值 `-939.308829219` 只差 8.7e-8 Ha ⇒ candidate_opt 是「反应物侧参考优化」的设计步骤，还是 E1 的 TS 候选塌回 RC 的预警？

**我的判定 = 设计步骤（不是 TS 塌回预警）**，三条实读证据：
1. `ts/ts_0008/process.json` 的 `input.guess` = `{"kind":"provided","xyz_path":"gold_finish_20261015/HI1/E1/lane1/TS_guess_merged_canonical.xyz","evidence_refs":["gold_finish_20261015/HI1/E1/TS_GUESS_PROVENANCE.md"]}` ⇒ **TS 起始几何由 provided guess 承担**（我复核 sha256：guess xyz `a2c0fa28667eb5afd814d8b876f40dd5873967c8a63973ff89bf9b0d0b980c4c`、provenance `d7a82f39e7d068400a0da60d4b59b7679c66441fd13cf885bb25f909f37a3276`，与既有登记一致）。
2. 管线记录：`declare` done、`candidate_opt` done（job 991）；`structures.reactant.xyz_path` 已替换为 `jobs/declaration_0002/candidate_opt/optimized_seed.xyz`（sha256 `69469643ad970550bd8ce80ce5f71257a68e262207dfb9b7698652ea143b751c`）；下一步 `product_seed_opt`（job 1009）→ 即 build 阶段**分别准备两端点构象参考**，之后才进 ts_opt；`current_ts_guess_path` 为空属正常。
3. 化学上即应如此：该步声明反应物 = (S)-RC 复合物，其参考构象优化收敛到 RC 极小值与 907 同值是预期。
- 我对 `optimized_seed.xyz` 的读数注意（供后续引用）：该文件按 **ts_0008 绑定序**，元素序 `C,C,O,C,…`，**不能按题源 map 号直接读**（实测 d(C2–O3)=1.219 = 丙酮 C=O、d(C2–C4)=1.509）。
- 我如实标注的**真实风险**：provided guess 是**合并边 7 对**初猜（d(C2–N20)≈1.95 Å），它自身可能同样滑回 RC；若发生，管线报 `no_peak`/`search_failed` ⇒ 触发 §9 替代口径（受约束单峰剖面 + 拆步提案），**与 NY3 的 l9999 不同类，也不能当作"无鞍点"证据**。已要求 lane1 在 `E1/LANE1_STATUS.md` 写明并说明如何区分「塌回」与「无鞍点」。
- 已投递给 lane1（`as_700f852fe3af412f`，call 回执 `evt_db1f316f7b184be2`，投递时该会话 state=succeeded、wake_status=requested ⇒ 会被唤醒）。

### R8.11 巡检 #3（2026-10-17 07:22 本地 CST；本人实测）

| run | rev | status | stage | waiting_for | result.outcome |
|---|---|---|---|---|---|
| ts_0011 | 23 | waiting | refine | job **999** ts_opt **running**（`refine.log` 590,064 B，mtime 07:22 正在增长） | null |
| ts_0009 | 33 | waiting | refine | job **1008** ts_opt **ready**（排队） | null |
| ts_0008 | 16 | waiting | build | job **1009** product_seed_opt **ready**（排队；job 991 candidate_opt 已 done） | null |
| ts_0012 | 5 | waiting | build | job **1000** candidate_opt **running** | null |

- 队列（07:22）：running = 998 / 999 / 1000 / 1004；queued = 1005–1009；terminal 新增 991 done、993 done、1001/1002/1003 done、997 failed（`l9999`，非本包）。本包手工在飞 = 0。
- **现场进程核对**（单独 ps 命令，非复合自匹配）：4 个 `l502/l703` 子进程在跑（etimes 2024/1863/963/53 s，CPU ~650–720%），确认管线作业真实在算，无静默停顿。
- 四条 run `result` 仍全 null ⇒ **回填 0/4**；TS 阶段的两个作业（999 运行、1008 排队）是当前关键路径。

### R8.12 巡检 #5（2026-10-17 08:10 本地 CST；本人实测）

| run | rev | status | stage | waiting_for | result.outcome |
|---|---|---|---|---|---|
| ts_0011 | 23 | waiting | refine | job **999** ts_opt **running**（`refine.log` 2,365,102 B，末次 SCF L37005 = -939.316511171） | null |
| ts_0009 | 33 | waiting | refine | job **1008** ts_opt **running**（`refine.log` 633,075 B，末次 SCF L9150 = -939.305803414） | null |
| ts_0008 | 16 | waiting | build | job **1009** product_seed_opt **running** | null |
| ts_0012 | **15** | waiting | **refine** | job **1013** ts_opt **ready** | null |

- ⚠ **重要读数（ts_0012 的 candidate_opt 终态）**：`ts/ts_0012/jobs/declaration_0001/candidate_opt/seed-opt.log` **Normal termination 08:07:09**，末次 `SCF Done: E(RB3LYP) = -939.302926757`（L40743）⇒ 比该边唯一基线 **job 924（-939.308218263）高 +0.005291 Ha ≈ +3.32 kcal/mol**。含义有两种可能：(a) 只是种子优化落到同一物种的**另一构象**（水/苯甲醛取向或氢键网络不同）；(b) 落到了别的极小值。**按本包写死口径 ΔE‡ = E(TS) − E(job 924) 不变**，但若管线随后自动跑的 `reactant_endpoint` Opt+Freq 也落在 -939.3029，则「工作流自身 reactant 端点」≠ 924 基线，交付必须显式标注两者关系、**不得**用工作流端点替换 924。已向 lane3（`as_375f0d91a9bc43f2`，call 回执 `evt_abc03f60cc8a47db`）索取一行解释（同物种/同构象？哪个构象？端点落点？）。
- 队列（08:10）：ts_0011 job 999、ts_0009 job 1008、ts_0008 job 1009 运行中；ts_0012 job 1013 排队。本包手工在飞 = 0。
- 四条 run `result` 仍全 null ⇒ **回填 0/4**。

### R8.13 ts_0008 推进到 refine（2026-10-17 08:3x；本人实测 + 主协调 R19 更正）

- **ts_0008 现 rev29 / status=waiting / stage=refine / blocked=null**，waiting_for=[job **1017**, purpose=ts_opt, state=ready, 8c/8192MB, declaration_0003, input `ts/ts_0008/jobs/declaration_0003/ts_opt/refine.gjf`]；`declare.json` / `jobs/declaration_0003/` mtime 08:30。
- 起因链（主协调 R19 两条来函）：主协调 08:29–08:31 先测到 ts_0008 rev20 blocked/`atom_map_missing`，随后 lane1（HI1_E1，帖 `evt_6d865763d19842b7`）提交 **FULL 1-based 41 原子映射**被接受（receipt request_key=`tc_de20a17281f7491a`、digest `14a280a1c3a476f40c411905b5ffa46eaaed6f0b41d99304b7b715e2ffe45df1`、rev 20→21、input_rev 2→3、changes=["reaction.atom_map"]、retained=[991,1009]、status=accepted）；我实读 `declare.json` `reaction.atom_map` **len 41**、`reaction_center`=[[1,2],[3,9],[31,40],[1,3],[1,31],[2,40],[2,9]]（0-based 内部）、`declaration_revision=3`，与之自洽。
- **本会话未对 ts_0008（或任何 run）做 ts_resume，未写任何 run 文件**；对 ts_0008 全程只读。主协调 R19 第二条已撤销「由我声明 atom_map」的请求（{`evt_4a3ceb67e3dc4df8` 作废}），我回执确认不再触碰其声明。
- **只读取证（ts_0009/0011/0012 的 atom_map）**：三条 run 的 `declare.json` 与 `process.json` 的 `reaction.atom_map` **均为 len 41**（decl_rev 5 / 4 / 1，stage 均 refine）；reaction_center：ts_0009=[[0,28],[1,3],[1,0],[27,28]]、ts_0011=[[1,3],[1,24],[24,25],[24,26],[3,25],[10,26]]、ts_0012=[[0,28],[1,3],[1,0],[27,28]]。⇒ ts_0008 是**唯一**曾被 `atom_map_missing` 挡住的一条，现已补齐；成因（本条声明当初未带 map）按事实登记，不下结论。
- **E1 TS 待核键对（主协调给的 ts_0008 built 序 1-based）**：[2,3] / [4,10] / [32,41] / [2,4] / [2,32] / [3,41] / [3,10]（7 对：3 断 + 4 成）。job 1017 终态后按 ① 117 模 + imaginary 行 ② 虚频模对该 7 对的投影（集中在甲基/H 转动 ⇒ pseudo-saddle，issue #190，不回填）③ 双向连通性 ④ 两端 0 虚频 + CIP ⑤ ΔE‡ − 907(-939.308829219) 逐门核验。
- 四条 run `result` 仍全 null ⇒ **回填 0/4**。

**身份/口径**：本会话 = HI1 包第 6 任 Coordinator，session `as_ec848a7673b74e35`（parent = 主协调 `as_a341823c436e47ed`）。第 5 任 `as_4f933afb7d98418e` 已 succeeded 结束；它派出的三道仍在 running，换任令已投递：lane1 `evt_fb4cb6a9e2a341aa` / lane2 `evt_889c52378a9c4fdc` / lane3 `evt_f3507a0b84bb4ef5`（均 delivered、wake_status=already_running）。**三道回报口径 = post 主题 `gold-finish-20261015` + 正文首行 `to: as_ec848a7673b74e35`**；本包 TS/IRC 只走 ts_prepare/ts_resume，优先 ts_resume。

### R8.1 本轮权威 run 状态（本人 `ts_inspect` 实读，2026-10-17 06:5x–07:0x）

| run | 边 | revision | status | stage | failure_class / needs | waiting_for | **result.outcome 原文** |
|---|---|---|---|---|---|---|---|
| ts_0008 | HI1_E1 | 12 | waiting | build | — / — | [{job_id:991, purpose:candidate_opt, state:running, 8c/8192MB, source_input_revision:2, input_path `ts/ts_0008/jobs/declaration_0002/candidate_opt/seed-opt.gjf`}] | **null**（无科学判定） |
| ts_0009 | HI1_E2 | 20 | waiting | build | — / — | [{job_id:993, purpose:candidate_opt, state:running, 8c/8192MB, source_input_revision:4, input_path `ts/ts_0009/jobs/declaration_0004/candidate_opt/seed-opt.gjf`}] | **null** |
| ts_0011 | HI1_E3 | 13（我读）/ **23**（lane2 同轮读） | blocked（我读）→ waiting/refine（lane2 读） | map → refine | `input_identity_unconfirmed` / needs=[`conformers.reactant.heavy_atom_binding`]；我读到的 message 原文：`reactant: Explicit heavy-atom binding does not preserve the declared molecular graph, bonds or stereochemistry.; product: Explicit heavy-atom binding accepted against the concrete graph.` | 我读时 []；lane2 读 [job 999, purpose:ts_opt, state:ready, 8c/10240MB] | **null** |
| ts_0004 | HI1_E1（旧/证据） | 8 | blocked | build | `conformer_optimization_failed` / needs=[`conformers.reactant`]；failed_attempt=`1:candidate_opt:928`（input_sha256 `2bc8fb03ab7401182c50799ef3b9913cba1d712cf57b5b670591a574f983b779`，log_sha256 `e3286543d054fd48cab499cea8bca605156f0e7ff318253b4c21d19c393c7694`） | [] | **null** |

⇒ **四条 run 的 `result` 全为 null**（无 verified / candidate_only / search_failed / invalid_input 判定），因此 **ΔE‡ 无值可回填，回填进度 0/4** 不变。ts_0004 保留为 #180 证据，不动。

### R8.2 队列/容量（06:5x 实测，本人 `query_compute_queue`）

node-local online，容量 32 cpus / 51200 MB / 10 槽；**running = 991 / 992 / 993 / 994（全 8c，合计 32/32 cpus、36864 MB）**；queued = 995 / 996 / 997 / 998（各 8c，理由 "waiting: not enough free cpus/memory on node node-local right now"）；terminal = 989 **failed**（`l9999`，非本包 NY3）、990 done。⇒ 全机 cpus 已满（free.cpus=0），**本包不再新增手工作业**，只让三道的关键路径管线作业排队前进。本包手工在飞 = 0；本包管线在飞 = 991（ts_0008）+ 993（ts_0009）+ 999（ts_0011，ready）。

### R8.3 我本轮**独立复核**的基准（真实 `sha256sum` + `grep` 原始行；非转述他人）

| 文件 | 我实测 sha256 | 我实测原始行 |
|---|---|---|
| `E1/runs/RC_optfreq/RC_optfreq.log`（job 907） | `fa28545612332f69c60c0b778cd5dd1907b22b8ad36f6b1da7811da1295563ba` ✓ 与既有登记逐字一致 | `grep -c 'Frequencies --'`=**39**（×3 = 117 模）、`grep -c imaginary`=**0**、L66757 `Normal termination`；`SCF Done` 末次出现 **L61974** = `-939.308829219`（与 907 优化段 L59761 同值，频率段重印） |
| `E3/runs/I2_optfreq/I2_optfreq.log`（job 961） | `63dda25e04529e65920526304fb88755db9393e9c22bd3a6efb76eeee0af0d0e` ✓ | 39 频率行（117 模）、imaginary=**0**、L24001 `Normal termination`、`SCF Done` 末次 **L19183** = `-939.320655479` |
| `E2EM1/runs/I1_optfreq/I1_S_optfreq.log`（job 924） | `6ecf06238ee6e1e976ba30eb15faf655f3ebe5a0126ed37d0dfe9b687dea6a87` ✓ | 39 频率行（117 模）、imaginary=**0**、L27032 `Normal termination`、`SCF Done` 末次 **L22238** = `-939.308218263` |
| `E3/runs/preorg_v3/scan_c2o25_220_160.log`（job 980，约束扫描） | `436c4cd9225bd29c1ae65086e1394b27b886e4d45206f4efa91133b331030f66` ✓ | 只作 TS 初猜来源，能量不作能垒 |

**行号口径说明（本轮实测更正）**：同一条 log 里优化段与频率段各印一次 `SCF Done`（同值）。既有登记引用的 L59761/L16950/L20025 = **优化段**行号；我用 `tail -1` 取到的是**频率段**行号 L61974/L19183/L22238。**数值相同、结论不变**；交付引用时写明取的是哪一段，避免"行号对不上"的误判。

### R8.4 三道同轮回报要点（原文摘录 + 我收到的 hub 事件号）

- **lane1 = HI1_E1（`as_700f852fe3af412f`）**，帖 `evt_a32b4008c60040c1` / `evt_6e3a6ac7387f460c`：ts_0008 rev12 waiting、job 991 candidate_opt running；**ts_resume 被接受**（request_key=`tc_4d31217523af4aa2`，digest `2f0388da3eefc1696fed781939f710f1ea23e6dca273a144bcd1c91255983c42`，rev 8→9，input_rev 1→2，changes=[`conformers.product`]，invalidated=[declaration_revision 1 / candidate_opt / attempt 1 / job_id 968]）；product 端点源 `E1/build/I1_S_start.xyz` `c9d59aeab418c248629922ee37d4ea3822c64b7128dd63b3034d3c8c5ec2df3d`、`E1/build/I1_S_start_bonded.mol` `69de27c2a3319074932fb4bb6e2107431e11608f240df8948bb549b8b7921fd9`、provenance `E1/I1_PRODUCT_PROVENANCE.md` `07f4bd00907a76630cf189f52960b2014a14497d394176c8565c94783725e0f4`、heavy_atom_binding.indices=[3,2,1,4,5,6,7,8,9,10,11,25,28,29,30,31,32,33,34,35]；**TS/虚频/IRC/端点/ΔE‡ 全为 missing measurement**；已证伪：job 908（`I1_optfreq.log`，-939.308218263）输入几何是 I1_S_start.xyz 的 z 镜像、末帧 CIP=**R** ⇒ 不能作 E1 基准（(S) 产物侧只用 job 924）。
- **lane2 = HI1_E3（`as_06db52ada5014800`）**，帖 `evt_78baea314efe452c`：ts_0011 **rev 23 / status=waiting / stage=refine / blocked=null / result=null**，waiting_for=job **999** purpose=**ts_opt** state=ready 8c/10240MB，input `ts/ts_0011/jobs/declaration_0004/ts_opt/refine.gjf`（route 原文 `#p opt=(TS,calcfc,noeigen) b3lyp/def2svp empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=dmso)`，q0/m1，41 原子）；**两次 ts_resume 均 accepted**（`tc_274dc3ad308d4f5a` digest `783027706e803bc587946a1c833ddb981e29cd1337dae8f48a59d83b4d41a174`，rev 9→10，input_rev 2→3；`tc_51a435b4071e4f7c` digest `815b9bdab1c7a5bdd5baf4079e3ad49d5469c6d1a241107f0b2db0e1ff1430fe`，rev 13→14，input_rev 3→4，changes=[`conformers.reactant.heavy_atom_binding.indices`,`conformers.reactant.mol_path`]）；正确的 1-based 文件序 binding = **[3,2,1,29,28,30,31,32,33,34,35,4,5,6,7,8,9,10,11,25]**（首版环遍历方向错 → 被拒，逐字拒绝文本见其帖）；provided guess = `E3/prep/guess_c2o25_190/ts_guess_c2o25_190.xyz` `2568ca035c3ee37dc9472cd86bd3a751547ba835f99332cf8ce2ac91177bb186`（取自 job 980 的 Standard orientation L25159 = R(2,25) **1.8996 Å** 帧，SCF L25258 = -939.297771992）、provenance `8869c899f0a1db685ccf83cf3bcfbda1f0a42656a9441449885a61fa5d20e45a`、抽取脚本 `E3/tools/mk_ts_guess_frame.py` `246a6da449ea58290693571bcf3e66ab6fba289c91cd5e4c8e915a1c53d33139`；**TS/IRC/端点/ΔE‡ 仍缺测**。
- **lane3 = HI1_E2/EM1（`as_375f0d91a9bc43f2`）**，帖 `evt_fcad2d7e07a24081` / `evt_1779c9ccb0274c5c`：ts_0009 **rev 20 / waiting / build / result.outcome=null**，waiting_for=job 993 candidate_opt（8c/8192MB）；**三次 ts_resume accepted**（`tc_cafbf2fec2e14c24` rev12→13；`tc_a1d1eaf0bdec40b1` rev16→17；一次被 "ts_resume: active compute jobs prevent input revisions" 拦住属并发保护）；已修平台两次输入校验拒绝——product SMILES 缺 C2=N4 STEREOCIS、reactant heavy_atom_binding 有 2 解（证据 `E2EM1/evidence/BINDING_AND_MAP_VERIFICATION_20261017.md` `3432e7c19a685859ff37aef1140c1e4b293150c5e067066300c77bd981aea67a`）；通道 B 准备件 `build/I1_S_from_job59_bonded.mol` `0a8bed4bb738aca52ad5a3aee3f38a22ef9b902fa32be66c89294a476c642e49`、`build/TS_guess_EM1_j59f9_adduct.mol` `f25e6cbc6c45b646b001762f76ef337de559376ca698a81d6e0f7dcf4369929a`、`verify_channelB_lane3.py` `94d543d68869d1b081cd4ef0007c1e01a8ceb8d55ececa23f4e8c05e074ac714`、`make_mol_EM1_lane3.py` `fac51f609bcd66e13fcdb6e693ab602b8ec5db036c51088c656e52d2e7b4a8be`（RDKit 3D：Cα(8)=S、aldol C(29)=**R** = 题源 M1）；**两通道 TS/虚频/IRC/端点/ΔE‡/ΔΔ 全缺测**。

### R8.5 四条边判定（本轮，权威）

| 边 | 判定 | 基准（同批 Gaussian 16 纯电子能） | 缺什么 | 已证伪 / 已排除 |
|---|---|---|---|---|
| HI1_E1 | **缺测** | job 907 = -939.308829219 | TS(恰 1 虚频)+双向连通+两端 Opt/Freq+ΔE‡ | 908 是 (R) 镜像；平台 ETKDGv3 反应物种子不可用（ts_0004 l202） |
| HI1_E3 | **缺测** | job 961 = -939.320655479 | 同上（TS 已在管线 refine 阶段，job 999） | 声明的 alkoxide+COOH 在本级 QM 下不是驻点；裸 `B i j value` 卡静默失效 |
| HI1_E2 | **缺测** | job 924 = -939.308218263 | 通道 A TS+虚频+连通+端点+ΔE‡ | 历史 13.36（R-脯氨酸几何，L2 缺口）不可用 |
| HI1_EM1 | **缺测** | job 924 = -939.308218263 | 通道 B 同上 | 历史 15.52 同上 |

### R8.6 我的下一步（检查点；等各道 TS 阶段落地后逐项核验并回填）

1. 每轮读三道 hub 帖 + `ts_inspect` 四条 run，把新的 **result.outcome 原文**与证据 sha256 追加进本文件（只追加，不改旧段）。
2. 收到 TS 终态后逐项核验：① 恰 1 虚频且 `Frequencies` 的 imaginary 行投影以该步声明 pair 为主（用 `log_parser(watch_pairs=...)` 取 watch_pair_fraction）；② 连通性双向 IRC 或 §9 替代口径；③ 两端 Opt+Freq 0 虚频 + 身份（CIP/原子 map）；④ ΔE‡ = E(TS) − 该步自身起点（907 / 961 / 924），同批同机相减。
3. 回填靶点（收齐后一次性）：`cloudra/benchmark/hard_registry/hi.py` + `ideapool/tasks/hard/HI1.json`（重生成）+ `ideapool/reaction_candidates/hard.md` I1 行；守卫 `python -m pytest tests/test_benchmark.py -k regenerate_identically -q`（回填前先重跑基线 4 passed，输出原样留档）。
4. 交付单列「证据驱动的机理修订」（E3 参考态 alkoxide+COOH → aldol-OH+carboxylate；E1 若确无单鞍点则按拆步提案）。
5. 若某边在合理机时内仍无法取得合格单鞍点：按「缺测 + 缺什么 + 已证伪什么」交付，不填任何无证据数值。

### R8.14 巡检 #6（2026-10-17 08:34 本地 CST；本人实测）

| run | rev | status | stage | waiting_for | result.outcome |
|---|---|---|---|---|---|
| ts_0008 | 29 | waiting | refine | job **1017** ts_opt **ready** | null |
| ts_0009 | 33 | waiting | refine | job **1008** ts_opt **running**（`refine.log` 1,526,110 B，0 次 termination） | null |
| ts_0011 | 23 | waiting | refine | job **999** ts_opt **running**（`refine.log` 3,361,614 B，0 次 termination） | null |
| ts_0012 | 15 | waiting | refine | job **1013** ts_opt **running**（`refine.log` 111,124 B，0 次 termination） | null |

- 队列（08:34）：running = 999 / 1008 / 1013 / 1014；queued = 1015 / 1016 / 1017；terminal 新增 1009 done、1000 done、1005/1010 done、1011/1012 failed（非本包）。⇒ **四条 run 的 ts_opt 均已进入运行/就绪**，是本轮 HI1 的关键路径；四条 `result` 仍全 null ⇒ **回填 0/4**。
- 监接口径留痕（本轮实例）：巡 #6 提醒被 ts_0008 `product_seed_opt` 的**已完成**日志（08:29 Normal termination）提前触发 ⇒ 「检查条件引用已完成工件」的假触发；后续提醒只指向当时仍在跑的阶段日志。仅监控纪律留痕，不影响任何数值/结论。
- 本文件当前 sha256 = `590f8d1cd2b413f8496cb2743d29f7f8a51da62bddebab360d092c5fb7605f97`（= §R8.13 版）；本节写入后由新的 after_sha256 取代，取代关系随下一条回报给出。

### R8.15 里程碑：ts_0012（HI1_EM1）ts_opt 完成 → frequency 已排队（2026-10-17 09:09 本地 CST；本人实测）

- `ts/ts_0012/jobs/declaration_0001/ts_opt/refine.log`：**Normal termination 09:08:23**（L25604）、`Optimization completed.`（L24507）、`-- Stationary point found.`（L24508）、末次 `SCF Done: E(RB3LYP) = -939.293671629`（L24138）。
- ts_0012 现 **rev19 / status=waiting / stage=refine / blocked=null / result.outcome=null**，waiting_for=[job **1021**, purpose=**frequency**, state=ready, 8c/10240MB, input `ts/ts_0012/jobs/declaration_0001/frequency/frequency.gjf`]。
- **候选 ΔE‡（未验收，暂不写入任何交付文件）**：若 job 1021 判为**恰 1 虚频**且虚频模投影落在声明键对上，则通道 B（HI1_EM1）= −939.293671629 − (−939.308218263) = **+0.014546634 Ha ≈ +9.13 kcal/mol**（同批 Gaussian 16 纯电子能；基准 job 924 不变）。
- 其余三条仍在 ts_opt：ts_0008 job 1017 running（最近 SCF −939.207261678，远高于 RC，属合并边初猜早期步，尚不作任何解读）、ts_0009 job 1008 running（−939.304748108）、ts_0011 job 999 running（−939.318892473，I2 基准 −939.320655479）。
- **读数纪律（本轮踩到）**：直接对 Gaussian log 的 `Standard orientation` 块按声明 1-based 序号算距离**不可靠**——Gaussian 会重排内部原子序；实测 ts_0012 ts_opt 末帧按此法得 d(1,29)=3.198 Å，与该步「成键」的预期不符，说明该块不是工作流的声明序。⇒ 虚频模投影/连通性判据一律走 `log_parser(watch_pairs=...)` 或工作流自带的映射分析，不用裸索引几何读数下结论（本节不据此做任何结论）。
- 已向 lane3（`as_375f0d91a9bc43f2`，call 回执 `evt_16ec5951c9d340f8`）索取：117 模 + imaginary 行、虚频模对 4 对声明键对的投影、连通性（IRC 或 §9 替代）、两端 0 虚频与身份、以及 ts_0012 candidate_opt = −939.302926757 的一行解释。
- 四条 run `result` 仍全 null ⇒ **回填 0/4**（本节的 +9.13 只是候选，验收前不落地）。

### R8.16 ★ 正式判读：ts_0012（HI1_EM1）ts_opt 驻点 = **pseudo-saddle（不合格 TS）**（2026-10-17 09:3x–09:4x 本地 CST；本人实测 + 工具解析）

**① 频率门禁（job 1021，我实测）**
- 日志 `ts/ts_0012/jobs/declaration_0001/frequency/frequency.log` sha256 **`a70f1e784e0a30d4598d68e45907bc0f520b6a571af0c4a2a9177c5e3834b54c`**（375,829 B，mtime 09:34）；`Normal termination` 09:34:32；`SCF Done: E(RB3LYP) = -939.293671629`（L819，与 ts_opt 末次同值）。
- **117 模 = 3N−6**（我逐组核过 `Frequencies --` 共 39 组）；**`****** 1 imaginary frequencies`**（L1507）；虚频 **−27.9419 cm⁻¹**（L1516）；`Low frequencies --- -28.0390 -8.2267 -5.1269 -0.0007 0.0006 0.0008`（L1505，按纪律不作虚频判据）。
- **索引安全复核**：`frequency.gjf` 几何的元素序 = 日志末个 `Standard orientation` 块元素序 = `CCCNCCCCCOOHHHHHHHHHHHHHOHHOCCCCCCCHHHHHH`（**逐位相同 ⇒ 未发生 Gaussian 重排，1-based AN 即工作流声明序**，故键对投影可信）。

**② 虚频模投影（`log_parser(watch_pairs=[[1,29],[2,4],[1,2],[28,29]])` 原文数值）**
- `watch_pair_fraction.fraction = 0.000776`（= **0.078%**）；分对投影：1–29 = 0.0322、2–4 = 0.0138、1–2 = 0.0029、28–29 = 0.0082；`heavy_atom_fraction = 0.322`。
- 位移最大的原子（元素/序/模长）：**H38 0.328、H24 0.273、H37 0.244、H41 0.229、H18 0.207、C32 0.207**（前 6 中 5 个是 H）。

**③ 索引安全几何导出（本次新增，可复核）**
- 权威导出（走 `format_converter(input_format='log', output_format='xyz')`，工具自报 "Detected gaussian freq+sp, extracted final frame"）：`gold_finish_20261015/HI1/verify/ts_0012_freq_geom_from_log.xyz` sha256 **`4894c55d94d2c312105254e9db9bd06ae662157ad785d9744a024140ba40be6a`**。
- 我的程序化对照件（从 frequency.gjf 直接抽坐标、非手键；内容与上面**逐坐标相同，maxdev = 0.0 Å**）：`gold_finish_20261015/HI1/verify/ts_0012_freq_geom_framework_order.xyz` sha256 `24522011c4f22beeedaf6ba890c07b9c4600044ee9aee36e9a367729cb654517`（write 工具曾给「suspected handwritten coordinates」告警 —— 属**误报**：坐标由脚本从该作业日志/gjf 自动抽取，非人工键入；权威件仍是 format_converter 导出）。
- 该几何（声明序 1-based）实测：**d(1,29) = 3.198 Å（成键 C1–C29 根本没形成）**、d(1,2) = 1.355、d(2,4) = 1.388（亚铵 C2–N4 拉长）、**d(28,29) = 1.216 Å（C29=O28 双键完整）**；CIP 实测（`shared/tools/hi1_cip_tools.py` 对同一日志）：`natoms=41 frags=3 CIP[8C=S(...)]` ⇒ **Cα = S 通过**。

**④ 判读结论：= (ii) `pseudo-saddle`，不是本步的合格 TS**
理由（三条独立同向）：(a) 虚频模对声明 4 对键对的总投影仅 **0.078%**，几乎没有反应坐标成分；(b) 模位移由 H 主导（前 6 大中 5 个 H，力常数 0.0023、约化质量 4.9408 ⇒ 软模）；(c) 该驻点几何是**类反应物松散复合体**——成键 C1–C29 = 3.198 Å 未成键、aldehyde C=O 完整，而能量却比 job 924 高 **+0.014546634 Ha ≈ +9.13 kcal/mol**。
⇒ 按 issue #190 口径：**不得当作 TS、不得回填**；EM1 登记为「第 1 次未取得合格 TS（pseudo-saddle，−27.9419 cm⁻¹ 集体软模）」。ts_0012 现 rev23/waiting（waiting_for = job **1026 `irc`** ready）——该 IRC 建立在已判不合格的驻点上，**不能作为连通性证据**，如何处理由主协调裁定；**我不对该 run 做任何 ts_resume**。
- 四条 run `result` 仍全 null ⇒ **回填 0/4**（EM1 候选 +9.13 不落地）。

### R8.17 EM1 后续：主协调批准「再试一次（仅一次）」+ 派发给 lane3（2026-10-17 09:4x 本地 CST）

- 主协调 R25.1 采纳我的判读（(ii) pseudo-saddle）并**批准通道 B 再试一次、仅一次**（我回执 `evt_977df10982764383`；派单 `evt_254c34336a7f4cbe` → lane3 `as_375f0d91a9bc43f2`）。
- **种子优先序（主协调原话）**：① 若通道 A（ts_0009 job 1008）先出**合格 TS** ⇒ 以其为模板按声明映射做**对映/同面镜像帧**（给模板日志路径 + sha256 + 构造脚本）；② 否则沿声明反应坐标做**受约束弛豫扫描**（起点 = I1 参考 job 985 末帧）取**脊线峰帧**（**扫描极大不是 ΔE‡**）；③ 否则 **IDPP 插值帧**（沿声明 `atom_map`）。
- **提交方式**：`ts_resume(ts_0012)` 由**管线**提交（8c/≤10240MB、priority 0）；`evidence_refs` 必须是已存在 artifact 路径 + provenance note，并声明该帧是否机器构造、有无 compute record；**提交前先在主题报**（种子档位 / artifact 路径 + sha256 / 理由 / 手工在飞数）。
- **门禁阈值（写死，与主协调同口径）**：报 117 模、imaginary 数与波数、`watch_pair_fraction`、**[1,29] 单对占比**、`heavy_atom_fraction`、位移前 5 原子；**合格 = 虚频模以 [1,29] 为主导**（本轮伪鞍点基线 = 0.078%）；模属甲基/H/水转动 ⇒ pseudo-saddle（#190）⇒ **停止**，EM1 交主协调按「明确缺测 + 缺什么 + 已证伪」入终稿。
- **job 1026（ts_0012 IRC）**：不拦截；只作失败/一致性登记，**不能作为连通性证据**（先例 job 988/1014 均 l123）。
- 现状（09:38 我实测）：ts_0008 rev29（job 1017 ts_opt running）、ts_0009 rev33（1008 running，**通道 A 仍在 ts_opt**）、ts_0011 rev23（999 running）、ts_0012 rev23（1026 irc ready）；全机 32c 满载（free cpus 0），本包手工在飞 0；四条 run `result` 全 null ⇒ **回填 0/4**。

### R8.18 只读几何判读：ts_0008（HI1_E1）job 1017 ts_opt 的 +46 kcal/mol 高能态 = **无碎裂、沿声明合并坐标的早期阶段**（2026-10-17 09:5x 本地 CST；本人实测）

- 日志 `ts/ts_0008/jobs/declaration_0003/ts_opt/refine.log` sha256 **`82b8cfe40c4af43488bc11cef8d38fa1e6f2607e1d01d39b6a044e82430316ca`**（3,525,078 B，mtime 09:55）；**Step 54 / 246**（L54332）；末次 `SCF Done: E(RB3LYP) = -939.234244984`（L54245；近 8 步在 −939.2336…−939.2342 间小幅振荡）。
- **能量相对量级**：对 E1 自身起点 RC（job 907 = −939.308829219）差 **+0.074584 Ha ≈ +46.8 kcal/mol**；对 I1（job 924 = −939.308218263）差 **+0.073973 Ha ≈ +46.4 kcal/mol**（两个基准在本步几乎同值，结论一致）。
- **索引安全**：末帧取最后一个 `Input orientation` 块（L54631 起，41 原子），元素序 `CCOCHHHHHHOCCCCCCCHHHHHHOCOCCCCNHHHHHHHHH` = 声明序（1=C 2=C 3=O 4=C 5–10=H 11=O 12–18=C 19–24=H 25=O 26=C 27=O 28=C 29–31=C 32=N 33–41=H）⇒ 可直接按 1-based 判读。
- **声明 7 对键对实测（Å）**：`(2,3) C2–O3 = 1.365`（丙酮 C=O 已显著拉长，RC 时 1.219）、`(4,10) C4–H10 = 1.097`（**未断**）、`(32,41) N32–H41 = 1.226`（拉长；正常 N–H ≈ 1.01）、`(2,4) C2–C4 = 1.533`（单键，π 未成）、`(2,32) C2–N32 = 1.634`（已成但偏长；正常 C–N ≈ 1.47）、`(3,41) O3–H41 = 1.321`（质子桥接 N↔O）、`(3,10) O3–H10 = 2.612`（H10 仍在 C4 上）。另：C26–O27 = 1.336（脯氨酸羧基 C–O）。
- **连接性/分片**：共 **2 个分片** —— (i) 27 原子 = 丙酮 + 脯氨酸（C1,C2,O3,C4,H5–H10 + O25,C26,O27,C28,C29,C30,C31,N32,H33–H41）；(ii) **14 原子 = 苯甲醛 C7H6O（O11,C12–C18,H19–H24）**。⇒ 苯甲醛本就是该步声明中的**旁观组分**，**不是意外碎裂**；最长"键" = C2–N32 1.634；最小非键接触 = O3···H41 1.321（即声明成键对）、C2···H41 1.679，H···H 最近 1.76–1.77 ⇒ **无 < 1.2 Å 冲突、无单元崩解**。
- **判读**：几何沿声明合并坐标（N 进攻 1.634 + C=O 断裂 1.365 + 质子 H41 桥接 1.226/1.321），仅 `(4,10) C4–H10` 这一支尚未参与 ⇒ 是**早期阶段的高能脊**，而非碎裂。+46~47 kcal/mol 远超该步合理垒（历史 19.2 已作废，但量级不符）⇒ 与本包预登记的结构性判断一致：**7 对合并边很可能不存在低垒单鞍点**（BRIEF §9 拆步口径）。
- **处置建议（已报主协调）**：不杀 job 1017、不 ts_resume；等其终态。若收敛出 1 虚频 ⇒ 按 7 对投影门禁判（预期 H/甲基主导或混合）；若 l9999/超步 ⇒ 记「本次 ts_opt 走上 +46~47 kcal/mol 高能脊（H10 未参与、C2–N32 1.634 偏长），7 对合并边未取得单鞍点」，并按 §9 转拆步（RC→carbinolamine / carbinolamine→I1+水）。**本条不构成"无鞍点"结论**（l9999/超步只作失败登记）。

### R8.19 主协调 R30 口径更正登记（E1 参考态 = job 907）+ job 1017 高能帧导出 + 三项裁定（2026-10-17 10:0x 本地 CST）

**A. 参考态口径（主协调 R30 更正，本包一律以此为准）**
- **HI1_E1 参考态 = job 907（(S)-RC，−939.308829219，0 虚频）**；
- **HI1_E2 / HI1_EM1 参考态 = job 924（(S)-I1，−939.308218263，0 虚频）**；
- **HI1_E3 参考态 = job 961（实测 I2 侧互变体，−939.320655479，0 虚频）**。
- 自查：我**未按「E1 相对 924」产出过任何 ΔE‡ 数值**；§R8.18 中我把 +46.8（对 907）与 +46.4（对 924）**并列给出且各自标注了基准**，属量级说明而非 ΔE‡。§R8.1/§R8.6/§R8.12 的基准列本来就是 907 / 961 / 924，无错值。本段即为主协调要求的**登记句**：「主协调 R30 口径更正：E1 参考 = job 907」，终稿证据完整性说明引用本段。

**B. job 1017 高能帧导出（主协调 3(b) 授权，已执行）**
- 导出（`format_converter(input_format='log', output_format='xyz')`，工具自报 "Detected gaussian opt+ts, extracted final frame (frame 54)"）：`gold_finish_20261015/HI1/verify/ts_0008_job1017_last_frame_from_log.xyz` sha256 **`5108a92fa63bb13cd90d38981aa8bbf2b7189f5e84ea3ed7c029ad2d88f6a197`**（41 原子）。
- **原子序核对（按主协调要求逐位核）**：导出件元素序 = `CCOCHHHHHHOCCCCCCCHHHHHHOCOCCCCNHHHHHHHHH`，与 §R8.18 从 `Input orientation` 块读到的声明序**逐位一致 ⇒ 未被 Standard orientation 重排**，可按 1-based 声明序引用。该帧 = 「沿声明合并坐标的早期高能帧（+46.8 kcal/mol 相对 job 907）」。

**C. 三项裁定（记录在案）**
- (a) **不杀 job 1017、不 ts_resume**，跑至终态（已在执行）。
- (b) 导出已按上面 B 完成。
- (c) **拆步提案预批准但本轮不提交**：条件 = ① job 1017 终态判为不合格（l9999 或 1 虚频属 H/甲基主导）② 999/1008 终态释放槽位 ③ 先交两步完整声明（reaction_center 精确到键对与方向、每步起止物种与参考能量、guess 来源与 provenance）④ 一次只开一条，且**由主协调逐条授权**。
- **本轮终稿对 HI1_E1 的写法**（主协调给定）：「缺测 + 已证伪（本次 ts_opt 走上 +46~47 kcal/mol 高能脊：C4–H10 未参与、C2–N32 1.634 偏长；7 对合并边未取得单鞍点）+ 证据驱动的拆步提案（**未计算**）」。
- 纪律补充（主协调 R30 第 4 条）：Gaussian 输出中 `N imaginary frequencies ignored.` 一行**不作模数**，模数只看 band 表 3N−6。

### R8.20 ★ 独立复核：ts_0011（HI1_E3）job 999 的 ts_opt **正在漂回 I2 反应物极小值**（2026-10-17 10:1x 本地 CST；本人实测）

- 我在 `ts/ts_0011/jobs/declaration_0004/ts_opt/refine.log` 上按 **Input orientation** 帧（共 116 帧）测声明内坐标（1-based，E3 工作序 = `CCCNCCCCCOOHHHHHHHHHHHHHOHHOCCCCCCCHHHHHH`；`reaction_center` 0-based 原值 [[1,3],[1,24],[24,25],[24,26],[3,25],[10,26]]）：
  | 帧（行号） | d(2,25) C2–O25 | d(2,4) C2–N4 | d(10,27) | d(25,27) | d(11,27) |
  |---|---|---|---|---|---|
  | 0（L462，起点 1.9 Å 帧） | **1.900** | 1.331 | 1.501 | 1.032 | 3.398 |
  | 38（L36475） | 2.930 | 1.298 | 1.733 | 0.987 | 3.468 |
  | 77（L72690） | 3.134 | 1.299 | 1.726 | 0.989 | 3.659 |
  | 115（L107821，最近） | **3.142** | 1.299 | 1.717 | 0.989 | 3.635 |
- 判读：**水分子被推回（C2–O25 1.90 → 3.14 Å，逼近 job 961 的 3.16 Å）、H27 交还水 O25（1.032 → 0.989）、C2–N4 回到亚胺 1.299** ⇒ 该 ts_opt **正沿反应坐标漂回 I2 反应物极小值**，不是走向鞍点。与 lane2 的「1.90→3.13 Å 漂移」独立一致（两条独立读数同向）。
- 含义（与我 §R8.18 的 E1 判断同类）：**E3 声明的单步协同（成 (2,25)；断 (2,4)/(25,26)/(25,27)；成 (4,26)/(11,27)）在该 guess 下没有表现出鞍点**；若它最终收敛 ⇒ 大概率是 0 虚频的 I2 极小值（则不是 TS）；若超步/l9999 ⇒ 只作失败登记。**本条不作「无鞍点」结论**。
- lane2 已据此提出 **BRIEF §9 拆步提案**（步 A：I2 → hemiaminal（成 C2–O25 + H27→羧酸根，C2–N4 保留）；步 B：hemiaminal → P（断 C2–N4 + H26→N4）），并登记了 job 1028（1.600 Å 帧无约束 Opt+Freq）作驻点判定。**机图改动只有本会话可执行，且本轮按主协调裁定不提交**；E3 的 ΔE‡ 分母仍固定 job 961（−939.320655479）。

### R8.21 ★ 主协调裁定（本轮 HI1 三边定型）：**不再追加 TS 搜索；按「缺测 + 已证伪 + §9 拆步提案（只出文字）」交付**（2026-10-17 10:2x 本地 CST）

**裁定要点（逐条照录执行）**
1. **三条独立证据同向**（三条 ts_opt 全部离开声明反应坐标）：E1 job 1017 = 上 +46.6~46.8 kcal/mol 高能脊（C4–H10 未参与、C2–N32 1.634）；E2 job 1008 = d(1,29) 2.646→4.75 Å 外漂；E3 job 999 = 水被推回 1.90→3.14 Å、H27 交还水 O（0.989）、C2–N4 回亚胺 1.299（= 我 §R8.20 的独立读数）。⇒ 判读：**声明的合并/单步描述在本级别下没有被 ts_opt 捕获的一阶鞍点**（证据判读，**不是**「无鞍点」的数学证明）。
2. **本轮不再为 E1/E2/E3 追加 TS 搜索或换 seed**（资源：32c 长期满载 + 会挤掉别的包的唯一授权尝试）。
3. job 999 终态处置：收敛为 0 虚频 I2 极小值 ⇒ 登记「E3 单步协同在该 seed 下未取得 TS，ts_opt 收敛回 I2 极小值」；超步/l9999 ⇒ 失败登记（NStep 行号 + l9999 行 + 末判据 + 末 SCF）。两者都不补作业。
4. **§9 拆步提案本轮只出文字、不提交作业**（与 E1 同口径），三段式要求：① 每步 reaction_center（键对 + 方向，0-based 与 1-based 都写）；② 每步起止物种 + **同批**参考能量（并注明参考态 Opt+Freq 是否已有 0 虚频证据）；③ guess 来源与 provenance。E3 拆法 = 步 A：I2→hemiaminal；步 B：hemiaminal→P。E1 拆法 = RC→carbinolamine；carbinolamine→I1+H2O。
5. **ΔE‡ 分母锁定**：E1 = job 907（−939.308829219）、E2 = job 924（−939.308218263）、E3 = job 961（−939.320655479）。任何情形不改分母；终稿措辞 =「在声明的单步/合并描述下未取得已验收一阶鞍点」。
6. **终稿对三边写法（预告对齐）**：「缺测（保持 null / 不填旧 ORCA 值）+ 已证伪（逐边列 ts_opt 漂离读数与失败作业）+ 证据驱动的 §9 拆步提案（未计算）」；并保留 E2/EM1 的 **L2 身份缺口**声明（旧 13.36/15.52 建在 R-脯氨酸几何、本机无 ORCA 原生日志）。
7. **回填动作 = 无**：三条边保持 `null`、E2/EM1 保持既有 13.36/15.52 不动 ⇒ `hi.py` / `HI1.json` / `hard.md` **不需要改动**；守卫只需复核「未漂移」。

**EM1（通道 B）待裁决的一处口径（我按保守处理）**：lane3 已构造并校验了**第 2 次尝试的种子**（帖 `evt_b9cc92e58f88443c`，尚未提交）。主协调最新裁定只点名 E1/E2/E3 且理由为资源；EM1 虽在 R25.1 获得过一次授权，但与「本轮不再追加 TS 搜索」的资源理由同源 ⇒ **本轮不提交**，等主协调一句确认（已在回报中明确标出）。ts_0012 现 rev23 / waiting / job **1026 `irc` running**（该 IRC 建立在已判伪鞍点上，只作失败/一致性登记）。

### R8.22 交付前「无漂移」复核（2026-10-17 10:3x 本地 CST；本人实测）

- **守卫**：`python -m pytest tests/test_benchmark.py -k regenerate_identically -q` → `....  [100%]`（**4 passed**，与回填前基线一致；原样留档于本轮输出）。
- **回填靶点未被我改动**：`git status --porcelain cloudra/benchmark/hard_registry/hi.py ideapool/tasks/hard/HI1.json ideapool/reaction_candidates/hard.md` → 只有 ` M ideapool/reaction_candidates/hard.md`，且该改动**在本会话开始前即存在**（主协调台账：HL1_E1 = 0.0 已由 HL1 会话回填，hard.md 为其改动）；`hi.py` 与 `HI1.json` **均未列为 modified ⇒ 本包本轮未改题源/生成物**，与 §R8.21 第 7 条「回填动作 = 无」一致。
- 结论：按主协调裁定，HI1 三边保持 `null`、E2/EM1 保持 13.36/15.52 不动；守卫为绿，交付不引入任何生成物漂移。

### R8.23 ★ 更正 + 执行：EM1（通道 B）第 2 次尝试 = **已批准、非挂起**（主协调澄清）；E2/EM1 旧值 13.36/15.52 **保持不动**（2026-10-17 10:4x 本地 CST）

- **更正我 §R8.21 第 7 段的保守处置**：主协调澄清 —— R36 裁定**只点名 E1/E2/E3**，**EM1 不在其中**；EM1 的通道 B 第 2 次尝试是更早已明确批准的授权，目前**仅被平台并发保护挡住**（ts_0012 上有 job 1026 未终态），**不是资源裁定**。⇒ 我原「本轮不提交」的判断作废，改为「**1026 一终态立即提交**」。
- **已转告 lane3**（`as_375f0d91a9bc43f2`，call 回执 `evt_28977379eb734864`）：job 1026 终态后立即 `ts_resume(ts_0012)`，载荷不变（changes 只含 guess 组；种子 `E2EM1/build/TS_guess_EM1_j58f8_faceflip.xyz` sha256 `9f4d651aff4c75ef7ec9e582184c2581f4f22873d73b06b18e868cdd554ea10b`；`evidence_refs` = `CHANNEL_B_RETRY_SEED_20261017.md` 9ec11790… + `TS_SEED_PROVENANCE_EM1.md` 73ee4aa8… + `BINDING_AND_MAP_VERIFICATION_20261017.md` 3432e7c1…），并要求回报 receipt 逐字（request_key / digest / revision / input_revision / changes / retained / invalidated / status）+ 新 job id + stage。
- **门禁不变**：117 模（band 表）、imaginary 行、虚频模以 **[1,29]** 主导，并列报 `watch_pair_fraction` / [1,29] 单对占比 / `heavy_atom_fraction` / 前 5 位移原子（反例基线 = −27.9419 cm⁻¹ / **0.078%**）；ΔE‡ 参考固定 **job 924 = −939.308218263**；job 1000（−939.302926757）只作连通性/身份核验；任何 pseudo-saddle ⇒ 不回填、只记证伪。
- **E2/EM1 既有值 13.36 / 15.52 保持不动（不改 null）**：它们有 ORCA 依据但**建在 R-脯氨酸几何（L2 身份缺口）**；本机无 ORCA 原生日志无法核验、本批也无替代值 ⇒ 改 null 等于用「无证据的删除」替换「有证据但身份存疑的值」。终稿**显式声明 L2 缺口**并注「不可用于 (S) 题面的定量引用」，题源/生成物**本轮零改动**。
- 现状（10:4x 我实测）：ts_0012 **rev23 / waiting / job 1026 `irc` running**；ts_0008 1017、ts_0009 1008、ts_0011 999 三条 ts_opt 均 running；四条 run `result` 全 null ⇒ **回填 0/4**（EM1 若 1026 后提交并通过门禁，则届时按 job 1024/1026 后的新 ts_opt 结果评估）。
### R8.24 §9 拆步文字稿到件（E3）+ EM1 重试种子 / lane3 登记 独立复核（2026-10-17 10:5x 本地 CST；本人实测 sha256）

- **E3 拆步文字稿已到**（lane2 帖 `evt_e5502b0c182a4225`，写入 `E3/STATUS.md` §I）：我实测 `E3/STATUS.md` sha256 = `d288ee561bfa0bb11667794238b8c30336e7828afe497b38a1a5c9b2161dc5a2`（与自报逐字一致），§I 内确含步 A/B 与两套索引。要点：
  - **步 A：I2 → hemiaminal**：成 C2–O25；断 O25–H27；成 H27–O10（实测位点，声明 map 的 O11 归属为等价位点）。**1-based `[[2,25],[25,27],[10,27]]` / 0-based `[[1,24],[24,26],[9,26]]`**。
  - **步 B：hemiaminal → P**：断 C2–N4；断 O25–H26；成 H26–N4。**1-based `[[2,4],[25,26],[4,26]]` / 0-based `[[1,3],[24,25],[3,25]]`**。
  - 现声明单步（A+B 合并）：1-based `[[2,4],[25,26],[25,27],[2,25],[4,26],[11,27]]` / 0-based `[[1,3],[24,25],[24,26],[1,24],[3,25],[10,26]]`（与 ts_0011 存储逐项一致）。
  - 参考能量：步 A 起点 = job 961（−939.320655479，0 虚频，`I2_optfreq.log` 63dda25e…，L16950）⇒ **ΔE‡ 分母**；**hemiaminal 无同批 0 虚频 Opt+Freq 证据**（job 1028 仍排队无 log ⇒ 未取得/待定，不得作分母；其几何取自 job 980 point 5/5，该点能 −939.309047571 不得作分母）；产物 P 同批亦无 Opt+Freq 证据（`complex_candidate_000.xyz` 06161a14…）。
  - guess provenance：步 A = job 980 Standard orientation L25159（R(2,25)=1.8996；`ts_guess_c2o25_190.xyz` 2568ca03…，provenance 8869c899…，已被 job 999 实用、Kabsch RMSD 0.00000 Å）；步 B = job 980 Standard orientation L60390（R(2,25)=1.59959；`ts_guess_c2o25_160.xyz` 2b569cfe…）。**均机器构造/取自原生日志，无手工坐标**。
  - 已证伪四项 + 缺测两项（ΔE‡、两端 0 虚频身份）已列入 §I。
- **EM1 侧独立复核**：重试种子 `E2EM1/build/TS_guess_EM1_j58f8_faceflip.xyz` sha256 = `9f4d651aff4c75ef7ec9e582184c2581f4f22873d73b06b18e868cdd554ea10b`（与主协调给定值逐字一致）。lane3 已按 §R8.23 把 `E2EM1/STATUS.md` 的挂起改为「**已批准、待 job 1026 终态提交**」（其新 sha 9b3aba51…，自报；其 §10 记明阻塞原因 = 平台并发保护 `ts_resume: active compute jobs prevent input revisions`，call_id `tc_f74238b0861f47af`，issue #194），并登记弃用件 `TS_guess_EM1_j58f8_flip.xyz`（6625991c…，RDKit 仍报 (29,'S')，不得使用）。
- **待件**：E1 的 §9 拆步文字稿（lane1 未到）；三条 ts_opt 终态（999/1008/1017）；job 1026 终态（10:01:20 起跑，irc.log 已 853 行、尚无 Normal termination）。
- **三条 ts_opt 的最新时刻值（11:0x 我实测，供终稿更新；作业仍在跑）**：
  - **E1** job 1017：末次 `SCF Done: -939.236244006`（L62080）⇒ **+45.55 kcal/mol vs job 907**（曾 +46.8/+47.2，缓慢下降）；声明 7 对 = C2–O3 **1.361**、C4–H10 **1.095（未断）**、N32–H41 **1.226**、C2–C4 1.531、C2–N32 **1.641**、O3–H41 **1.334**、O3–H10 2.599。
  - **E2** job 1008：末次 `-939.304529125`（L82639）⇒ **+2.31 kcal/mol vs job 924**；**d(1,29) = 5.093 Å**（外漂已超过早期 4.75 帧）。
  - **E3** job 999：末次 `-939.319384470`（L109270）⇒ **+0.80 kcal/mol vs job 961**；**d(2,25) = 3.156 Å ≈ job 961 的 3.160 ⇒ 实质已回到 I2 极小值几何**、C2–N4 1.300（亚胺）、O25–H27 0.990（H27 已交还水）、d(11,27) 3.614。
  - 已把这些「时刻值 vs 主协调草稿快照（+47.20 / 4.75）」的差异报给主协调（`evt_0984f427bece409a`），并建议草稿标注「作业仍在跑，时刻值 + 行号」。
- **路由登记更正**：lane1 现行会话 = `as_700f852fe3af412f`（主协调 10:08 曾误投 `as_4f933afb7d98418e`，已由正式送达版重发）；§R8 各段引用的就是该 id。
- **待件**：E1 的 §9 拆步文字稿（lane1 未到）；三条 ts_opt 终态（999/1008/1017）；job 1026 终态（10:01:20 起跑）。
### R8.25 E1 拆步文字稿到件（lane1 `LANE1_STATUS.md` §15/§16；2026-10-17 10:1x–10:2x，我实测 sha256）

- 文件 `E1/LANE1_STATUS.md` sha256 = **`290277480fd0d624d0dce9d9c7d8650291044f091c5ab103e2a8c0b0482227a8`**（42,116 B，mtime 10:09）；§15 = §9 拆步文字稿（仅文字，未提交作业/未 ts_resume/未改图），§16 = INT1 候选帧导出登记。三段式齐全：
  - **① reaction_center（双套索引）**：**步 A RC→INT1（carbinolamine）** form (2,32) C2–N20 σ、(3,41) O4–H21；break (2,3) C2=O4 π、(32,41) N20–H21；0-based form [1,31]/[2,40]、break [1,2]/[31,40]。**步 B INT1→I1+H₂O** form (2,4) C2=C3 π、(3,10) O4–H22；break (4,10) C3–H22 σ、(2,3) C2–O4 σ；0-based form [1,3]/[2,9]、break [3,9]/[1,2]。覆盖性说明了 (2,3) 在 A 记 π、B 记 σ 的不重复计数规则。
  - **② 起止物种 + 同批参考能量**：步 A 起点 = job 907（−939.308829219，0 虚频，log sha fa285456…，L59761；117 模、最低 L62670 9.7022）；**INT1 无同批 Opt+Freq ⇒ 明确缺测、不得作任何分母**；步 B 终点 = (S)-I1（job 924，−939.308218263，0 虚频，L20025/L22238，最低带 L22931 24.6404，L22921 的负值为平动/转动伪模，非虚频）。另指出 E1 自己的 job 1009 product 端点同值但 **只有 opt 无 freq ⇒ 不能当 0 虚频证据**。
  - **③ guess provenance**：步 A 首选 job 1017 末帧（1017 终态后导出 xyz + provenance；备用 `guess.kind=scan` coord_type=bond atoms=[2,32] 3.75→1.55 Å 8 步）；步 B 现无可用帧（推荐 scan atoms=[2,3] 1.40→3.00 Å 9 步，或 2D 网格 (2,3)×(3,10)）；明确 `TS_guess_merged_canonical.xyz`(a2c0fa28…) **只能作合并边历史初猜、不得作 A/B 步 guess**。
  - **§15.4 已证伪**：合并 7 对 provided 初猜未走向单鞍点（H22 始终留甲基、O4···H22 反被拉到 2.60、C2–O4 反缩到 1.36）⇒ 该初猜只能作步 A 素材。其时刻读数 L61113 −939.233606719 = **+47.20 vs 907**（= 主协调草稿所引用的那个快照；我 11:0x 的最新为 L62080 −939.236244006 = **+45.55**，作业仍在跑）。
  - **§16 INT1 候选帧**：`E1/lane1/INT1_candidate_from_job1017_step61.xyz` sha256 `0aacfe68819340dc30506005434568f969e300229ab52f11c733fe2abd330421`（41 原子，format_converter 导出 frame 60，与 L60786 的 Input orientation 逐坐标一致 max|Δ|=0.000000）——**登记为「INT1 候选（未验证极小值）」，不得作步 B 分母**。
- ⇒ **两份 §9 拆步文字稿均已到齐**（E1 见本节、E3 见 §R8.24）。**剩余待件**：三条 ts_opt 终态（999/1008/1017）、job 1026 终态（→ lane3 提交 EM1 第 2 次尝试）。
### R8.26 编号口径统一（主协调 R39 第 2 点）+ 我此前 E1 化学标签的**标签级勘误**（数值不变）

**统一口径（本文件自此执行，终稿同）**：键对一律写 **「声明序 1-based 索引对」 +（化学标签，取自题源 map 号）**，例如 `(2,3) = C2–O4`。索引 = 该 run 的 built/声明序；化学标签 = 题源 map 号，两者不再混用。

**E1（ts_0008 built 序）索引 ↔ 化学标签对照（lane1 §15.0 给出，我据此核对过 §R8.18 的帧）**：
| built 1-based | map 号 / 化学标签 |
|---|---|
| 2 | map2 = C2（丙酮羰基 C） |
| 3 | map4 = **O4**（丙酮羰基 O） |
| 4 | map3 = C3（烯胺 β-C） |
| 10 | H22（C3 上 α-H） |
| 32 | map20 = N20（脯氨酸 N） |
| 41 | H21（N20–H） |

⇒ 合并 7 对按统一口径应读作：**断 (2,3)=C2=O4 的 π、(4,10)=C3–H22、(32,41)=N20–H21；成 (2,4)=C2=C3 的 π、(2,32)=C2–N20、(3,41)=O4–H21、(3,10)=O4–H22**。

**标签级勘误（仅标签，数值/结论均不变）**：§R8.14 / §R8.18 / §R8.24 表里我写的 `C2–O3 1.361`、`N32–H41 1.226`、`C2–N32 1.641` 等，是按**索引**当标签的简写，应分别读作 `(2,3)=C2–O4`、`(32,41)=N20–H21`、`(2,32)=C2–N20`；所引距离（1.361/1.226/1.641 等）与行号不受影响。E2/E3/EM1 各段用的标签本就取自各自 `declare.json`/题源 map（E3: C2–N4 / C2–O25 / O25–H26 / O25–H27 / N4–H26 / O11–H27），无需改。

- 另：lane1 的 §15/§16 已由主协调受理登记（其帖 `evt_55bd2c6b540b4abf`；台账 R37/R38），我 §R8.25 的独立复核与之一致。
### R8.27 时间标注勘误 + 三条 ts_opt 时刻值刷新（本条实测 `date` = **2026-10-17 10:15:29 CST**）

**勘误（仅时间标注，数值/sha/行号全不受影响）**：§R8.24 标题的「10:5x」、§R8.25 之后的叙述以及 10:1x–10:2x 期间发给主协调消息中的「**11:0x**」均为**误标**；这些读数实际测量时刻在 **10:05–10:15 CST** 之间（同一台机 `date` 实测：10:05:42、10:15:29）。终端机时以本段 `date` 为准。

**三条 ts_opt 时刻值（10:15:29 CST，含行号；作业仍在跑、非终值）**：
| 边 | run / job | 末次 `SCF Done` | 步数 | 相对自身基准 |
|---|---|---|---|---|
| **E1** | ts_0008 / 1017 | `-939.236880294`（**L64952**） | step **65**/246（L65039） | **+45.15 kcal/mol** vs job 907（−939.308829219） |
| **E2** | ts_0009 / 1008 | `-939.304108452`（**L86335**） | step **93**/226（L86423） | **+2.58 kcal/mol** vs job 924（−939.308218263） |
| **E3** | ts_0011 / 999 | `-939.319467892`（**L112986**） | step **121**/232（L113073） | **+0.75 kcal/mol** vs job 961（−939.320655479） |

- 趋势一致：E1 高能脊缓慢下降（+47.20 → +46.8 → +45.6 → **+45.2**）、E2 仍在外漂、E3 已回到 I2 盆地（d(2,25) ≈3.16）。ts_0012 job **1026 IRC** 仍在跑（irc.log 791 行，末次 SCF 仍 = TS 的 −939.293671629，无 termination）。四条 run `result` 仍全 null ⇒ **回填 0/4**。
- 终态后按裁定登记（E1/E2/E3 均不补作业），并以终值替换本表。

## §R8.28 10:17 CST 巡检（时刻值，终值待替换）＋与主协调的勘误闭环

- 本轮实测（`query_compute_job`，10:15–10:17 CST）：**999 running**（06:53:35 起）、**1008 running**（07:39:26）、**1017 running**（08:42:22）、**1026 IRC running**（10:01:20）、**1028 ready**（排队未起，E3 interm_c160 Opt+Freq，只作驻点判定）。
- 时刻读数（`grep` 直读日志，**非终值**）：
  - **E1** ts_0008 / job 1017：`refine.log` 4,269,372 B；末次 SCF `-939.237001642`（**L65901**）；step **66**/246（L65988）；无 Normal/Error termination 行 ⇒ 相对 job 907 约 **+45.07 kcal/mol**（时刻）。
  - **E2** ts_0009 / job 1008：5,624,525 B；`-939.303993142`（**L87243**）；step **94**/226（L87331）；无 termination ⇒ 约 **+2.65 kcal/mol**（时刻）。
  - **E3** ts_0011 / job 999：7,333,159 B；`-939.318976876`（**L113916**）；step **122**/232（L114003）；无 termination ⇒ 约 **+1.05 kcal/mol**（时刻）。
  - **EM1** ts_0012 / job 1026 IRC：`irc.log` 86,106 B / 1,429 行，仅 1 条 `SCF Done`（= TS 的 `-939.293671629`，**L791**），无 `Step number`、无 termination ⇒ **仍停在第一点**，不能作任何连通性证据。
- 趋势与判读不变：E1 缓慢下降的高能脊（+47.20 → +46.8 → +45.6 → +45.2 → 时刻 +45.07），E2 外漂，E3 已回 I2 盆地 ⇒ 三条均不补作业、均不回填（未取得 TS）。
- 与主协调的闭环（本轮双向消息）：① 我此前「11:0x」的时刻误标按实测改为 **10:05–10:17 CST**，主协调草稿 §10.2 写的是「10:0x 时刻值」故**无需改稿**，勘误只入台账；② 约定 **三条 ts_opt 终态后一次性发终值**（末次 SCF 能量@行号 + step N/M@行号 + 日志 sha256 + ΔE 相对该步自身参考态），主协调一次替换，我不再逐次刷稿；③ 主协调明确「无回执要求」⇒ 此后除**终值、技术性失败（含 call_id）、需其裁决的临界**外，我不再发确认性回执，进展只落本文件。

_（本节为 10:17 CST 时刻快照，终态后以终值整表替换；sha256 见同轮 bash 实测。）_

## §R8.29 终态登记 ①：E3 / ts_0011 / job 999 的 ts_opt 已收敛（10:30:07 CST done）——落到 I2 盆地驻点，非声明单步 TS

实测（`bash` + `grep` 直读 `ts/ts_0011/jobs/declaration_0004/ts_opt/refine.log`，同轮 `sha256sum`）：

| 项 | 终值 | 行号 |
|---|---|---|
| 末次 SCF | `-939.319094501` A.U. | **L124211** |
| 末步 | step **134** / max 232 | **L124298** |
| 收敛判据 | **Stationary point found.** | **L124575** |
| 终止行 | **Normal termination** of Gaussian 16 at Sat Oct 17 10:30:06 2026 | **L125662** |
| 日志体积 / sha256 | 8,046,622 B / `a8f56a49dcec0404da9d23071ad444e6a59641852f2657d2d0903fc3e70b4177` | — |
| ΔE vs job 961（I2 极小，`-939.320655479`） | Δ = 0.001560978 Ha = **+0.98 kcal/mol** | — |

- **几何终帧**（`format_converter` log→xyz，frame 133；`HI1/verify/E3_ts0011_job999_final_from_log.xyz` sha256 `46f9512cd898726f53911b0cd0f5601d03b81ae94069c5c85d53275dd9c2d799`，41 原子，元素序 CCCNCCCCCOO…，与声明 1-based 序一致）：d(2,4) C2=N4 = **1.299 Å**（回到亚胺/氮杂缩醛前的 N4=C2）；**d(2,25) C2–O25 = 3.138 Å（未成键）**；水完整 O25–H26 0.967 / O25–H27 0.989；**d(4,26) N4–H26 = 3.982 Å（质子未转移）**；d(11,27) O11–H27 = 3.641 Å。
- **判读**：E3 声明的单步协同（水作质子梭、C2–O25 与 N4–H 同步形成/断裂）在该 seed 与 declaration_0004 下**未取得该步的鞍点**；ts_opt 收敛到的是 **I2 盆地的驻点（比 job 961 的 I2 极小高 +0.98 kcal/mol，几何连通性同 I2）**。⇒ 按 #190 与主协调裁定：**不回填**、`run result.outcome` 保持 **null**。
- **模数判定待定**：管线已由 workflow 自动排队 frequency **job 1029**（ready，8c/10240MB，`source_input_revision=4`，输入 `ts/ts_0011/jobs/declaration_0004/frequency/frequency.gjf`）——这是**管线自动推进**，非我补作业；0 虚频可确证其为极小值，若出现 1 虚频则须按模组成判是否为伪鞍点。该 job 终态后按其 `frequency.log` 补登。
- 队列实况（10:32 CST 实测 `query_compute_queue`）：running 1008(8c)/1017(8c)/1026(8c)/**1028(8c，10:30:33 起，E3 interm_c160 Opt+Freq)**，queued 1029 位置 1；free.cpus=0、free.slots=6 ⇒ 本包手工在飞 = 1（1028），未新增任何手工作业。
- E1（1017，step 75/246，末次 SCF `-939.237241320`@L74472，4,816,966 B，sha `b58949514b69051a1bf75300a0479ff2e989f0620980b2618c962903af9064ee`）与 E2（1008，step 103/226，`-939.304352718`@L95478，6,153,803 B，sha `669eeb728ccf717e4f1e2820a10b3cc9ac09c16cb66684b3abf23b74fe8d9d8f`）仍在 running；EM1 的 1026 IRC 已到 **Pt 1 step 13/20**（`-939.293671878`@L9215，589,669 B，sha `565d9f467b95169eda7468b6dffa92e26f9421fdd18d582a9ad1ca28c52f51cb`），尚未终态 ⇒ ts_0012 rev 23 仍 waiting_for job 1026，lane3 的 ts_resume 仍受并发保护未提交。
- `ts_inspect` 同轮原文：ts_0011 rev **27** status **waiting** stage **refine** result **null** waiting_for job **1029** frequency ready；ts_0008 rev 29 waiting_for 1017 ts_opt；ts_0009 rev 33 waiting_for 1008 ts_opt；ts_0012 rev 23 waiting_for 1026 irc。

## §R8.30 第二次巡检：无新终态；一次假唤醒已归因；关键路径与 lane 存活状态

- **假唤醒归因（监控纪律复核）**：本次唤醒来自上一轮布下的提醒，其 check 引用了 **ts_0011 的 refine.log**——该日志已在 §R8.29 登记为 Normal termination，故 check 立即成功。这不是新终态。新建提醒已**移除**该路径，只保留仍在跑/未创建的日志（ts_0008/ts_0009 ts_opt、ts_0012 irc、ts_0011/E1/E2 的 frequency、E3 interm_c160）。
- **作业实况**（`query_compute_job` + `grep` 同轮实测）：
  - **E2 / 1008**：running，step **104**/226，末次 SCF `-939.304369457`（L96385），6,210,453 B ⇒ 时刻 ΔE **+2.42 kcal/mol** vs job 924。
  - **E1 / 1017**：running，step **76**/246，末次 SCF `-939.237167536`（L75453），4,876,303 B ⇒ 时刻 ΔE **+44.97 kcal/mol** vs job 907。
  - **EM1 / 1026 IRC**：running，**Pt 1 step 14/20**（max 20），末次 SCF `-939.293671878`（L9821），627,027 B。
  - **1028**（E3 interm_c160 Opt+Freq）：running（10:30:33 起），66,321 B。
  - **1029**（ts_0011 frequency，管线自动推进）：ready，队列第 1；**1030** 为 ts_0007（非本包）。
- **关键路径**：节点 32c 已满（1008+1017+1026+1028 = 32c，free.cpus=0），**1029 必须等 1008/1017/1026 之一结束**才起跑；因此 E3 的 0 虚频/伪鞍点判定要先等 IRC 收尾。E1/E2 均 ~0.5–0.7 步/分，若在 max 步数前不收敛，预计 12:00–14:00 CST 才终态。
- **lane 存活状态**（`agent_hub directory`）：as_700f852fe3af412f（lane1/E1）、as_06db52ada5014800（lane2/E3）、as_375f0d91a9bc43f2（lane3/E2+EM1）均 **state=succeeded**，且均无「EM1 第 2 次尝试已提交」的痕迹 ⇒ 1026 终态后由我直接 call lane3 唤醒并催办（succeeded ≠ 死亡，投递消息可唤醒）。
- 本轮写动作：仅本文件追加；无新作业、无 ts_resume、无回填。

> **同轮自更正**：本节 E1 的 ΔE 数字首次写入误作 +44.94，按实测 0.071661683 Ha × 627.5095 = **+44.97 kcal/mol** 更正（−939.237167536 vs job 907 −939.308829219，L75453）。仅该数字受影响，行号、能量、字节数与其余各条不变；本文件之外未发布过 +44.94。

## §R8.31 主协调接受 E3 组 + 本轮新增口径

- **E3 独立复核（主协调，非转述）吻合**：refine.log 8,046,622 B / sha256 `a8f56a49…b4177`；L124211 `-939.319094501`、L123372 `-939.319094466`；L124298 `Step number 134 out of a maximum of 232`；L124568–124575 四项判据全 YES + L124574 `Optimization completed` + L124575 `Stationary point found`；L125662 `Normal termination ... Sat Oct 17 10:30:06 2026`；`verify/E3_ts0011_job999_final_from_log.xyz` 2,107 B / sha256 `46f9512cd898726f53911b0cd0f5601d03b81ae94069c5c85d53275dd9c2d799`。⇒ **E3 组整体接受**，主协调按此替换草稿 E3 行。
- **E3 终稿措辞（硬约束）**：收敛到 **I2 盆地几何**、**非声明单步 TS**、**不回填**、`result.outcome` 保持 **null**；**+0.98 kcal/mol 只能写「该浅驻点相对 job 961 的能量差」**，**禁止**出现为 ΔE‡ 或能垒，**也不得写「能垒趋近 0」**；虚频判定待 1029，未取得即如实写「未取得（1029 state=ready、节点 4×8c 满）」，**E3 不因此改判**。
- **截断口径改为 11:20 CST**（主协调不同意 12:30；交付硬线 11:30，留 10 分钟登记）。截断读数**必填**：末次 SCF 值 + 行号；step N/M + 行号；明文「**非终态读数、无 termination**」；日志 sha256；相对自身参考的 ΔE（**E1 对 job 907 `-939.308829219`**、**E2 对 job 924 `-939.308218263`**）并注明参考态文件路径。截断值**不得进入任何能垒申报**，`result.outcome` 仍为 null。若 11:20 前出现 Normal termination / Optimization completed，则按**终态**登记（同样只作「缺测」判读的补强）。
- **1029 不必等**（排在 1026 之后，早于 11:20 起跑概率低）。
- **EM1 时限**：1026 一终态即唤醒 lane3 提交 ts_resume(ts_0012)（changes 只含 guess 组，种子 `9f4d651a…`；门禁 117 模 + 虚频模以 **[1,29]** 主导，反例基线 −27.9419 cm⁻¹ / 0.078%；ΔE‡ 参考固定 job 924）。若 **11:20 前** 1026 未终态或 ts_resume 未起跑 ⇒ **EM1 按 partial 写「result=null、未验收」**，不再等。
- **索引双写（跨道）**：已向 lane1 `as_700f852fe3af412f`、lane2 `as_06db52ada5014800` 发出对照表请求（工作序 1-based ↔ 原始序 1-based ↔ 题源 map 号/化学标签，并要原始序的定义文件与 sha256）。**在两份回执到手前，本文件已发布的一切键对编号一律读作「工作序／声明序 1-based」，不得跨道直接当原始序使用**；收到后写入终稿并做一次全文件口径复核。
- 无回执要求 ⇒ 本条只落 STATUS，不发确认帖。

## §R8.32 终稿预置

- 已把终态交付帖正文预写成草稿 `HI1/DRAFT_final_post.md`（sha256 `04eeef6705aaeca396c268da2305cded8ec975ee93ce35fe577eb12fc6ddd4d7`），含四边「缺测/缺什么/已证伪」、E1 与 E3 两份 §9 拆步文字稿、三项必声明、回填 0/4 与守卫口径；E1/E2 的终态/截断字段与索引序说明留占位符，**11:20 CST 截断时替换后即为交付帖**（草稿本身不是交付物，不作证据引用）。
- 已设 11:17 CST 定时唤醒取截断读数（另有终止触发提醒在跑，二者独立）。

## §R8.33 索引序双写落实 ①：E3 侧对照表到手（lane2 as_06db52ada5014800 回执）

- **定义澄清（关键）**：所谓「原始序」= **题源 hi.py atom-map 标签序（SMILES 出现序）**，即重原子标签 1–20 + 水的两个显式 H 标签 21、22；题源 SMILES 里其余 19 个 H 是**隐式、无原始编号**，因此原始序**不是一份 41 原子序列**（原文见 `HI1/E3/STATUS.md` §F.0）。
- **工作序** = `HI1/E3/runs/I2_optfreq/I2_min_v5.xyz`（41 原子，sha256 `9a6203ff67d9f0d95ad774e78b17bc397b22992f24cbcdf448f8c5558142ef2b`）；证据链：与 `ts/ts_0011/build/input_0003/reactant/seed.xyz` 同 sha256；与 job 961 日志（sha `63dda25e…0af0d0e`）逐位元素序相同；job 999 refine.gjf 与 guess 内坐标 Kabsch RMSD 0.00000。
- **对照（工作序 1-based ↔ 原始序/题源标签 ↔ 化学标签）**：2↔**[C:2]**（iminium C）；4↔**[N+:20]**（吡咯烷 N）；10↔**[O:13]**（羧酸根 O 之一，C9–O10 1.2544 Å，本构象接受 H27，R(10,27)=1.717 Å）；11↔**[OH:15]**（另一等价 O，C9–O11 1.2501 Å，接受 H24，R(11,24)=1.791 Å）；**25↔[O:4]（水氧；job 961/963/980/999/1028 恒定）**；26↔**[H:21]**（水 H → 产物脯氨酸 N–H）；**27↔题源无独立标签**（declare `atom_map` product33↔working27，水 H → COOH）；易混项：**24↔[H:22]**（aldol O28–H 的氢，R(24,28)=0.9842 Å）。
- **O10/O11 不等价不可互换**：化学上等同（C–O 1.2544 / 1.2501），但构象中氢键对象不同（H27↔O10、H24↔O11），故 §9 步 A 用 (10,27) 而非声明 (11,27) 是有意为之。
- **`atom_map` 基数与方向**：`ts/ts_0011/declare.json`（sha256 `b5b883bd09fb0b173fc4d561a5218d3920f6aa04c966e37f0eb7b0eeac8b23ef`）41 项、值域 0..40 ⇒ **0-based，方向 = product 坐标序 → reactant 工作序**；`reaction_center` 同为 0-based。抽样：atom_map[0]=2 → product1(CH3)↔working3；atom_map[2]=24 → product3(酮 O)↔working25(水 O)；atom_map[40]=25 → product41(N–H)↔working26。
- **交叉验证**：lane2 用同一终帧（最后 Standard orientation L125063）复算的六个距离与我 §R8.29 完全一致（1.299 / 3.138 / 0.967 / 0.989 / 3.982 / 3.641 Å）。
- **机制修订口径（同源）**：题源记账（alkoxide+COOH）与本道实测极小值（aldol-OH + 羧酸根）差别**仅在 product 19 与 33 两个 H 的归属交换**（`HI1/E3/STATUS.md` §E.16 / §G.3 / §I.0）；ΔE‡ 分母仍锁 job 961 = `-939.320655479`。
- 已把该对照写入终稿草稿的索引段（`HI1/DRAFT_final_post.md`，新 sha 见下轮实测）；E1 侧对照仍等 lane1 回执，未到则终稿明写「仅工作序 1-based、原始序对照未回」。

## §R8.34 索引序双写落实 ②：E1 侧三套序对照到手（lane1 as_700f852fe3af412f 回执；我独立核 sha）

- **三套序（不可混用）**：① **原始序** = job 907 实际输入原子序（`E1/runs/RC_optfreq/RC_optfreq.gjf` sha256 **81b083aff4fcfb18166b7060c1983b38e028dc2adc193a1d1851903ad29ee835**，首几何 `E1/build/RC_start.xyz` sha256 **f4eb0ba6f085114c97cb13bcdbe03a8613a2f95262782bcb5fb9da5c6d9b93c0**；log 的 `Input orientation` 首块与 .gjf 逐坐标一致 max|Δ|=0.0 ⇒ 读 log 用 Input orientation 即原始序）；② **built 序** = `E1/lane1/RC_S_canonical.xyz` sha256 **71b23e07b73a7241e19c3c94e927040f5f113f815184bfa44387d58bbc0e6597**（= declaration_0002 candidate_opt/optimized_seed.xyz，lane1 报 69469643…）；③ **product built 序**（第三套：product C2=2、C3=1、N20=4、O4=25、H21=26、H22=27）。
- **我独立复核（bash sha256sum，同一轮）**：RC_optfreq.gjf **81b083af** 与 lane1 报一致；`E1/build/RC_start.xyz` **f4eb0ba6** 一致；`E1/lane1/RC_S_canonical.xyz` **71b23e07** 一致；`E1/LANE1_STATUS.md` 现为 **f494fdd48f9be28773b95ba1ea4119563894f3f1e8889fdde7a36991a7c00ef2**（§18 已含本表）。lane1 报的 `E1/RC_start.xyz`、`E1/RC_S_canonical.xyz` 实际位于 `E1/build/` 与 `E1/lane1/` 下——**只是路径前缀不同，内容 sha 相同**。
- **7 对对照（built 1-based ↔ 原始序 1-based ↔ 题源 map 号 ↔ 化学标签）**：(2,3)↔**(2,25)**↔(2,4)↔C2–O4；(2,4)↔**(2,1)**↔(2,3)↔C2–C3；(4,10)↔**(1,27)**↔(3,22)↔C3–H22；(32,41)↔**(4,26)**↔(20,21)↔N20–H21；(2,32)↔**(2,4)**↔(2,20)↔C2–N20；(3,41)↔**(25,26)**↔(4,21)↔O4–H21；(3,10)↔**(25,27)**↔(4,22)↔O4–H22。
- **全 41 原子置换**（built 1..41 → 原始序）：`[3,2,25,1,14,15,16,12,13,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,10,9,11,8,7,6,5,4,24,23,21,22,19,20,17,18,26]`；依据：优化前同一几何两份文件元素+坐标逐原子匹配 **41/41 唯一双射、max|Δ| ≤ 1e-6 Å**（lane1 脚本 `E1/check_order_vs_job907.py` sha256 **5a78996acfd7c4f98f0845119799c52ec8f5ca048d4330321a78af82d07b21f6**）。
- **结论一行**：**job 907 日志原子序 ≠ built 序**（为上表置换）⇒ 本文件此前所有 E1 键对编号按 **built 序 1-based** 读；跨道引用必须同时给原始序，例如 C2–O4 = built (2,3) = 原始序 (2,25)。

## §R8.35 索引序双写落实 ③ ＋ 两条在跑作业的现场（lane2 同轮回报）

- `ts/ts_0011/jobs/declaration_0004/ts_opt/refine.log` 的 step 行原文经 lane2 复核为 `Step number 134 out of a maximum of  232`（**L124298**），收敛表 **L124568–124575**，与 §R8.29 一致 ⇒ E3 终值「step 134/232」可引用。
- **job 1028**（interm_c160 Opt+Freq，10:30:33 起跑）：仍 running、停在 opt 段，无 `Optimization completed`、无频率表；末两条 SCF `-939.311647746`（L3399）、`-939.304869050`（L4337）。终态前不 sha 中间态。
- **job 1029**（ts_0011 frequency）：**仍无 log**（`declaration_0004/frequency/` 只有 `frequency.gjf` 2,329 B 与 `optimized.xyz` 2,106 B）⇒ E3 虚频判定按「**未取得**（1029 state=ready、节点 4×8c 满）」落稿。
- lane2 已确认停手（不再提交作业、不 ts_resume、不改图），并承诺 1028/1029 终态时只回「行号 + 读数 + 是否落在 (2,25)/(2,4) 上」，数值永不进 ΔE‡/分母。

## §R8.36 时刻标注勘误（只涉时刻）

- §R8.30–§R8.33 的标题原先写了 10:36 / 10:45 / 10:50 / 10:55 CST，**这些分钟数是我按假设写的、未经同轮 `date` 实测**，现已从标题删除。实测锚点只有两个：**10:17:00 CST**（§R8.28 轮）与 **10:36:38 CST**（本轮 lane1 核 sha 同轮）；因此 §R8.29–§R8.35 全部落在 **10:17–10:37 CST** 区间内。
- 受影响项：仅时刻标注。能量、行号、sha256、字节数、判读结论均不受影响；本文件之外也未把这些分钟数当作证据时点引用过。

## §R8.37 标签级勘误（E1 键对的化学标签，非索引）

- 我在 §R8.29 之前的 E1 表里把键对写成「(4,10)=C4–H10」「C2–N32」这类形式：编号（built 序 1-based）是对的，**但把索引当成了化学标签**。按 lane1 §18 的三套序，`(4,10)` 是 **C3–H22**（丙酮甲基 C–H），`(2,32)` 是 **C2–N20**，`(32,41)` 是 **N20–H21**，`(2,3)` 是 **C2–O4**。
- 影响面：仅标签字面。距离、行号、能量、判读（C3–H22 未断、C2–N20 1.634 Å 偏长 ⇒ 高能脊）全部不变。
- 终稿草稿已按 lane1 标签重写（索引段改为三套序逐对对照，C4–H10 处改为 C3–H22），草稿现 sha256 **608231b013a4f4d911fb6b235ae28f544d692e162b55853899d5a1632cf8291f**。
- 后续纪律：跨道引用一律写「built 序 1-based（原始序 1-based）+ 化学标签」三段，禁止只给索引式简写。

## §R8.38 终态登记 ②：EM1 / job 1026 IRC failed（l123，10:37:21 CST）——只作失败登记，不作连通性证据

- `ts/ts_0012/jobs/declaration_0001/irc/irc.log` 820,189 B / 13,596 行，sha256 **0670edd201ea6347ca9cbc202e61cdb8ae5e3856b241f8f7e51f03c601d19a0f**。
- **L13593** Error termination via Lnk1e in /home/ly/g16/l123.exe at Sat Oct 17 10:37:21 2026；**L13506** Pt  1 Step number  20 out of a maximum of  20；末次 SCF **L13397** -939.293671877；末段判据：**WARNING: Bulirsch-Stoer Method is not Converging** / **Delta-x Convergence NOT Met** / **Maximum number of corrector steps exceded**；Job cpu 4h35m23.3s、Elapsed 35m59.2s。
- 判读：IRC 只跑 **Pt 1（正向）**、在第 20 点耗尽并由 l123 收尾，**无反向支路、无终点匹配** ⇒ **不作任何连通性证据**（与前例 job 988 / 1014 的 l123 同型）；**不因此对 ts_0012 写「无鞍点」**。

## §R8.39 EM1 第 2 次尝试已由 lane3 提交（我独立核到 declaration 2 / job 1032 / 种子逐坐标相同）

- `ts_inspect ts_0012`：**revision 33**、**declaration_revision 2**、stage **refine**、result **null**、`waiting_for` = job **1032**（purpose ts_opt、state **ready**、8c/10240MB、`jobs/declaration_0002/ts_opt/refine.gjf`，文件时间 10:37）。
- `process.json`：**owner_session_id = as_375f0d91a9bc43f2**（lane3）、**intervention_count = 1**；重试理由原文含 Channel-B retry (approved once): job 1026 IRC on the pseudo-saddle (1 imaginary -27.9419 cm-1。
- **种子核对（我独立做）**：`jobs/declaration_0002/ts_opt/refine.gjf` 首几何 与 `HI1/E2EM1/build/TS_guess_EM1_j58f8_faceflip.xyz`（sha256 **9f4d651aff4c75ef7ec9e582184c2581f4f22873d73b06b18e868cdd554ea10b**）**逐坐标相同**：41 原子、元素序一致、**max|Δ| = 0.0** ⇒ 提交的是被授权的 faceflip 种子，未被替换。
- 队列：节点 32c 被 1017/1008/1028/1029 四个 8c 作业占满 ⇒ **1032 与 1030(ts_0007) 均排队**；本包**手工在飞仍为 1**（1028），1032 属 lane3 的管线作业、未越配额。
- 待办：1032 终态后按门禁判（117 模、imaginary 行、以 declare.json reaction_center 作 watch_pairs 的 watch_pair_fraction/单对占比/heavy_atom_fraction/前 5 位移原子、索引安全、format_converter 导出；虚频模以 **[1,29]** 主导才合格，H/甲基/水转动 ⇒ pseudo-saddle 不回填）；ΔE‡ 参考固定 job 924 -939.308218263。

## §R8.40 措辞更正（E3 虚频判定，lane2 同轮指出）

- 1029 **已于 10:37 起跑**：`ts/ts_0011/jobs/declaration_0004/frequency/frequency.log` 存在（40,448 B），日志内**尚无** SCF Done / Frequencies -- / Harmonic frequencies。
- 因此 E3 终稿不得再写「1029 state=ready、节点满」，改为「**虚频判定未取得**（job 1029 frequency 已于 10:37 起跑，截稿时日志内尚无频率表）」。E3 判读与 +0.98 的「浅驻点相对 job 961 能量差」措辞不变、仍不回填。

## §R8.41 lane3 的 ts_resume receipt 已收（逐字存档要点）

- request_key **tc_a8a157a2432141a7**；request_digest **f6be0b42494dd8b8ae8c2c9fe253f8e65ea524cc2b449d2b974a1f448741ea62**；**previous_revision 26 → revision 27**、**previous_input_revision 1 → input_revision 2**；**status accepted**。
- **changes = ["guess.evidence_refs","guess.xyz_path"]**（只动 guess 组）；retained = declaration_revision 1 的 candidate_opt/job 1000；**invalidated = ts_opt/1013、frequency/1021、irc/1026**。
- reason 原文含：「Channel-B retry (approved once): job 1026 IRC on the pseudo-saddle (1 imaginary -27.9419 cm-1, [1,29] watch_pair_fraction 0.000776) failed with 'Delta-x Convergence NOT Met' / 'Maximum number of corrector steps exceded.' (l123, 10:37:21). Replace the TS guess only with the face-flipped TS-like seed (RDKit CIP (8,S)/(29,R), d(1,29)=1.9375 A, element order identical to the bound reactant), keeping reaction/reaction_center/atom_map unchanged.」
- lane3 一行确认：除 guess 组外**未改** reaction_center / atom_map / 端点结构 / 方法 / route（methods 各 stage 仍指 profile lane3_g16_dmso、contract matched=true）；本次只新增 job **1032**。
- **版本号差异说明（我自己核清，不需外人解释）**：receipt 记 rev 26→27，而 `ts_inspect` 现报 **revision 33**——其间的增量来自 job 排队/启动/证据绑定这类生命周期 revision，不是我或 lane3 又改了输入；**判定依据是输入几何本身**：`jobs/declaration_0002/ts_opt/refine.gjf` 首几何与授权种子 sha 9f4d651a… **max|Δ|=0.0**（§R8.39）。

## §R8.42 10:39 CST 读数（截断前最后一次巡检；全部仍 running）

- **E1 / 1017**：running，step **80**/246（L79448），末次 SCF **-939.236510821**（L79360），5,129,922 B ⇒ 时刻 ΔE ≈ **+45.4 kcal/mol** vs job 907（读数略回升，仍属同一高能脊）。
- **E2 / 1008**：running，step **109**/226（L101019），末次 SCF **-939.304337614**（L101841），6,506,347 B ⇒ 时刻 ΔE ≈ **+2.44 kcal/mol** vs job 924。
- **1029（ts_0011 frequency）**：running（10:37:29 起），50,827 B，仅 1 条 SCF（= TS 的 -939.319094501），**尚无频率表** ⇒ E3 虚频仍未取得。
- **1028（E3 interm_c160 Opt+Freq）**：running，step **6**/243（L6212），末次 SCF -939.312285001（L6124），445,974 B，仍 opt 段。
- **1030 / 1032**：均 ready 排队（节点 4×8c 满：1017 / 1008 / 1028 / 1029）。

## §R8.43 终态登记 ③：E3 / job 1029 frequency = **pseudo-saddle（甲基转动）**，E3 未取得合格 TS

- `ts/ts_0011/jobs/declaration_0004/frequency/frequency.log` 374,858 B / 5,302 行，sha256 **8366cbc6ec3d40d66bfb001cee746ac39f9fdc86896098d088e82e4d3cc133af**；**L5302** `Normal termination of Gaussian 16 at Sat Oct 17 10:55:08 2026`。
- **L1502** `******    1 imaginary frequencies (negative Signs) ******`；**L1511** `Frequencies --   -128.0397                37.1550                47.4266`；39 组 `Frequencies --` = **117 模**。**L1500–1501** `Low frequencies --- -128.0475  -10.7450  -5.6627  -0.0008  -0.0005   0.0005` ——首行负值即该虚频自身，**不是额外虚频**；**L3440** `1 imaginary frequencies ignored.` 按口径**不计入模数**。
- **我的独立判读（自算：解析 L1509 起的位移块，41 原子 × 3 模）**：模式 1 的 |d| 前六 = **H15 0.640 / H14 0.592 / H16 0.478** / H12 0.037 / C3 0.032 / H13 0.024；其余原子 ≤0.024。
- **化学身份核定（我自算 1.25 Å 邻接，末帧几何）**：H14/H15/H16 全部挂在 **C3（1.093–1.101 Å）**，而 **C3 恰好带三个 H（14/15/16）⇒ C3 是甲基碳（题源 [C:3]）**；C1 只带两个 H（12/13）为 CH2；水氧 O25 带 H26/H27。⇒ 该虚频是 **C3 甲基的转动/摆动**（C3 自身 |d| 仅 0.014，近乎纯绕轴的 H 转动）。
- **投影**：六个 watch atom {2,4,11,25,26,27} 的**平方位移占比 = 0.0015（0.15%）**（我的集合口径，自算）；lane2 按每对求和报 0.3%，两者同量级、均 ≪ 任何 TS 判据；各对 |d|：(2,4) 0.022/0.014、(2,25) 0.022/0.010、(25,26) 0.010/0.024、(25,27) 0.010/0.010、(4,26) 0.014/0.024、(11,27) 0.000/0.010。
- **判读**：E3 的驻点（job 999 几何、−939.319094501）是 **pseudo-saddle（甲基转动，#190 同型）**，**不是**声明的 6 对协同水解 TS ⇒ **E3 未取得合格 TS、不回填、result.outcome 保持 null**；+0.98 kcal/mol 仍只作「该浅驻点相对 job 961 的能量差」，**不作 ΔE‡/能垒**。
- 几何导出（`format_converter` log→xyz 末帧）：`HI1/verify/E3_ts0011_freq1029_geom_from_log.xyz` sha256 **62eea5858336a69e09e26acd6e684fc50ad4cc3c6f61c107ed0075919ee6a160**；重原子 1..11 元素 = C C C N C C C C C O O，与工作序一致（未重排）。
- **索引双写**：虚频模涉及原子 = 工作序 **14/15/16（H）+ 3（C3，题源 [C:3]）**；题源 SMILES 里甲基 H 为隐式、**无原始编号**（原始序见 lane2 §F.0）。
- 后续：管线已自动排队 **job 1033（irc, ready）**——**自动推进，非我或 lane2 手工提交**；按裁定不停不杀、只登记，节点 4×8c 满 ⇒ 截稿前不会起跑，**不作任何连通性证据**。

## §R8.44 job 1028（E3 interm_c160 Opt+Freq）= hemiaminal 驻点收敛（我独立复核；尺度只作身份证据）

- `E3/runs/interm_c160/interm_c160_optfreq.log` 1,241,836 B / 19,155 行，sha256 **92f0617fec4ccaed31d3e1ba950faf670d4da4e287a3673734955474b76f47cf**（10:56:18 mtime）。
- **L17229** `Optimization completed.`、**L17230** `-- Stationary point found.`、**L18325** `Normal termination of Gaussian 16 at Sat Oct 17 10:56:06 2026`；末次 SCF **-939.312626605**（L19117，freq 段首个 SCF）。
- **我独立解析末个 Standard orientation（L18955 起，41 原子）**：元素序 **CCCNCCCCCOOHHHHHHHHHHHHHOHHOCCCCCCCHHHHHH**，与 `E3/runs/I2_optfreq/I2_min_v5.xyz` **逐位相同 ⇒ 未重排**，可按工作序直读几何：
  - **d(2,25) = 1.4728 Å（新成 C2–O25 键）**；**d(2,4) = 1.4248 Å**（C2–N4 保留，由 I2 的 1.2990 拉长）；
  - **d(10,27) = 0.9949 Å**（H27 已转到羧基氧 O10），O25···H27 = 1.6342；C9–O10 1.3297 / C9–O11 1.2137（COOH 形成）；
  - H26 仍在 O25（d(25,26) = 0.9693）；**d(4,26) = 3.1829 ⇒ 无 N4–H 键**；N4 仍三配位。⇒ 物种 = **C2 同时带 N4 与 O25 的半缩胺 + 已质子化 COOH**（q0/m1，41 原子不变）。
- **能量**：-939.312626605 − (-939.320655479, job 961) = 0.008028874 Eh = **+5.04 kcal/mol**。按主协调锁定口径，该数**只作「落地物种/是否存在该中间体」的身份证据，不是 ΔE、不是能垒、不进任何分母**。
- **频率判定：未取得**（job 1028 的 freq 链路 10:56:07 起跑，截稿时 `Frequencies --` 块计数 = **0**）⇒ hemiaminal 是否 0 虚频仍未证；若后续出 1 虚频须按模组成再判（同上 #190 口径）。
- 意义：E3 的 §9 步 A（I2→hemiaminal）**产物侧首次有实测无约束驻点**（此前只有受约束扫描点 job 980 point 5/5 = -939.309047571，永远不能当 ΔE），这为「单步声明应拆两步」提供正向证据；**但 E3 的 outcome 仍为 null、仍不回填**。
- 索引双写：几何读数全部按**工作序 1-based**（= I2_min_v5.xyz 序）；对应题源标签 2=[C:2]、4=[N+:20]、10=[O:13]、11=[OH:15]、25=[O:4]（水氧）、26=[H:21]、27=无独立标签（product33↔working27），见 §R8.33。

## §R8.45 交付前守卫与题源状态复核（10:59:06 CST 实测）

- `python -m pytest tests/test_benchmark.py -k regenerate_identically -q` → **4 passed**（`....  [100%]`）。
- `git status --porcelain`：**`ideapool/tasks/hard/HI1.json` 未出现在修改列表** ⇒ 本包的题源 json 未被我改动；`cloudra/benchmark/hi.py` 亦未改动（其不在列表）；`ideapool/reaction_candidates/hard.md` 显示为已修改（` M`），该改动**早于本会话**（HL1 道回填所致，非我所为），**HI1 的 I1 行本轮未被改写**。
- 结论：**回填 0/4、题源零改动、守卫 4 passed** 三条在本次交付中可如实声明（以本行实测为凭）。
- 其它未跟踪目录（`gold_finish_20261015/`、`ts/`、`ts_path/` 等）为运行产物，未提交 git（遵守不提交纪律）。

## §R8.46 job 1028 freq 终态（11:10:09）= **0 虚频** ⇒ E3 §9 步 A 产物为 verified 局部极小（我独立复核）

- `E3/runs/interm_c160/interm_c160_optfreq.log` 1,593,380 B / 23,954 行，最终 sha256 **1ec7e4c6388415d0859939238f4f96ec7739c0bbf1f985a28f4dd3c23b7dcec1**。
- **全 log 中 `imaginary frequencies` 出现次数 = 0** ⇒ **无虚频**；`Frequencies --` 组数 = **39** = **117 模（3N−6）**；首个频段 **L19814** `19.8439 / 32.4876 / 53.5548`（最低实模 **19.8439 cm⁻¹**）；**L19804** `Low frequencies --- -11.3266  -0.0004  0.0007  0.0009  4.6430  5.5200` 首行负值为平动/转动伪迹，按既定口径**不计模数**。
- **L18325** opt 段 Normal termination @10:56:06；freq 段 **L23954** Normal termination @**11:10:09**；L21772 `Zero-point correction= 0.347492`；L22248/L22249 freq 段自身一步几何校验 `Optimization completed. / -- Stationary point found.`（Predicted change in Energy = −3.41e−09）⇒ 与 opt 收敛点为同一几何。
- **判读升级**：E3 的 §9 步 A 产物（半缩胺 + 已质子化 COOH，C2–O25 1.473 / C2–N4 1.425 / O10–H27 0.995）由「频率未取得」升为「**0 虚频 ⇒ verified 局部极小**」，这是「单步声明应拆两步」的正向证据；**但 E3 的 outcome 仍 null、ΔE‡ 仍缺测、+5.04 kcal/mol 仍只作身份证据、永不进分母**。
- 至此 E3 的 §9 步 A 两端都有 0 虚频证据（起点 job 961、产物 job 1028），**但步 A 的鞍点本身仍未取得**；步 B 的 hemiaminal→P 仍无任何端点 Opt+Freq。

## §R8.47 11:14:25 CST 截断读数（E1 / E2）＋ 交付前最终作业状态

- **E1 / job 1017**（仍 running，无 termination）：末次 SCF **-939.240831682**（**L98349**）；step **99 / 246**（L97487）；日志 **6,289,380 B**，sha256 **3b8e0996febb643be22a2a9dc8e74ccf7784422a280d8c48c71d6bc83457ba0b**；ΔE vs job 907 = 0.067997537 Eh = **+42.67 kcal/mol**。**明文：非终态读数、无 termination ⇒ 不作能垒申报。**
- **E2 / job 1008**（仍 running，无 termination）：末次 SCF **-939.304351052**（**L120485**）；step **129 / 226**（L119614）；日志 **7,696,987 B**，sha256 **e3a0e54301c6db71796a47ca985939948438a6d61291c11e14f1011d7ca334c7**；ΔE vs job 924 = 0.003867211 Eh = **+2.43 kcal/mol**。**明文：非终态读数、无 termination ⇒ 不作能垒申报。**
- 作业状态（11:14:25 实测）：1008 running、1017 running、**1032 running（EM1 第 2 次 ts_opt 已起跑）**、**1033 running（E3 管线自动 IRC）**、1030 failed（ts_0007，非本包）。
- 三条 ts_opt 的 `result.outcome` 全部仍为 **null** ⇒ **回填 0/4**；E1/E2 截断值不进入任何能垒申报。
- 终稿正文定稿于 `HI1/DRAFT_final_post.md`，替换全部占位符 + 最后一次措辞微调后 **sha256 = 2098a74b71384aa278e50a14d0f0eaebaa6c791180a7a3e7d8b6b5aaa99d5fd6**（8,156 字符）。

## §R8.48 交付帖已发布（11:18 CST 前后）

- **帖子 id evt_7fbdfb416f1e41bf**，主题 **gold-finish-20261015**，kind=message，首行 `to: as_a341823c436e47ed`；投递结果：as_a341823c436e47ed **delivered**（message_event_id evt_90f98fa0670c4a45、wake_status=requested）。
- 正文即 `HI1/DRAFT_final_post.md` 全文（sha256 2098a74b…），含：四边逐条「缺测 + 缺什么 + 已证伪什么（带读数与行号）」；E1 与 E3 两份 §9 拆步文字稿（E3 步 A 产物 job 1028 = 0 虚频 verified 局部极小，但步 A 鞍点仍缺测、步 B 两端无 Opt+Freq）；三项必声明（Gaussian 16 替代 ORCA / L2 身份缺口 13.36、15.52 保持不动 / (S) 题源下 E2、EM1 通道命名不可沿用）；**回填 0/4、题源零改动、守卫 4 passed**。
- 仍在跑的作业（不属于本次交付范围、不等待）：**job 1032**（EM1 第 2 次 ts_opt，running）、**job 1033**（E3 管线自动 IRC，running）、**1008/1017**（E2/E1 ts_opt，running，其读数为 11:14 截断值）。若其后续终态需要更新，属下一轮追加，不改本文件的已发布结论。

## §R9.0 交付后追加轮（13:26–13:30 CST）：1032/1033/1039/1040 全部终态，EM1 出现候选 TS、E2 再次伪鞍点

- 作业终态：**1032 ts_opt done**（10:56→12:00:41）、**freq 1036 done**（12:19:43）、**IRC 1039 failed**（13:25:23）；**1008 ts_opt done** → **freq（ts_0009/declaration_0005/frequency）done**（12:25:15）、**IRC 1040 failed**（13:02:30）；**1033（E3 自动 IRC）done**；**1043（ts_0011 product_frequency）running**。
- 权威状态：**ts_0012 rev 44 status=blocked blocked.failure_class=job_failed result=null**；**ts_0009 rev 44 同状**；两者 waiting_for 均为空 ⇒ 管线在 IRC 失败处停止，**不自动补测端点**。

## §R9.1 EM1 通道 B：候选 TS 成立但**只能记 candidate_only**（我独立复核全部数字）

- ts_opt（job 1032）：`ts/ts_0012/jobs/declaration_0002/ts_opt/refine.log` 1,647,410 B，sha256 **66691e0e68e9044d7d10e45e8953e6c5468efee3d361713d3e34d7bfbb2b4241**；末次 SCF **-939.283734374**（**L24183**）；L24549 `Optimization completed.`、L24550 `-- Stationary point found.`；L25650 Normal termination @12:00:41。
- 频率（job 1036）：`…/declaration_0002/frequency/frequency.log` 377,050 B / 5,340 行，sha256 **a471aa7b6c2b34b7ccff44a98bbcd0dee7c4ae5f436653fe79f094f44fe53a65**；**L1541** 1 imaginary、**L1550** `Frequencies -- -314.2861  33.5499  44.0361`；39 组 = **117 模**；L3479 `1 imaginary frequencies ignored.`（不计模数）；L5340 Normal termination @12:19:43。
- **模组成（我自算，解析 L1548 起的位移块）**：|d| 前五 = **atom1 0.574 / atom29 0.538** / atom13 0.313 / atom15 0.225 / atom14 0.185 ⇒ 虚频模确由 **[1,29]** 主导（前二就是该对两端）；watch atom 集合 {1,2,4,28,29} 平方位移占比 **66.7%**；分对 |d|：(1,29) 0.574/0.538、(2,4) 0.158/0.057、(1,2) 0.574/0.158、(28,29) 0.149/0.538。
- **CIP 独立复算（RDKit 2026.03.6，`rdDetermineBonds` + `AssignStereochemistry`，几何取自 freq 末帧 `verify/EM1_retry_TSB_job1036_geom_from_log.xyz`，sha256 **165f4968114cd808c41c864a1605493635a19739b3dc128e7952f94047b76026**）**：手性中心仅两处——**atom 8 = (S)**、**atom 29 = (R)**，与通道 B 要求一致。
- **能量**：E(TS_B) - E(job 924) = 0.024483889 Eh = **+15.36 kcal/mol**（相对 `-939.308218263`）。
- **缺的两项（决定它只能是 candidate_only）**：① **双向连通性缺失**——IRC job 1039 `…/declaration_0002/irc/irc.log` 1,512,886 B / 25,169 行，sha256 **dfc4d3ec2bba6c84e634eeb7105fb48fe0481969c7e61b73413fb2ed47ff31e3**，L25164 `Delta-x Convergence NOT Met`、L25165 `Maximum number of corrector steps exceded.`、**L25166 Error termination via Lnk1e in l123.exe at 13:25:23**；② **两端点 Opt+Freq 未跑**（管线停止，waiting_for 为空）。
- ⇒ 按验收链：`result.outcome` 仍 **null**、**不回填**；+15.36 只作「候选 TS 的电子能差、未验收」，**不得作为 ΔE‡ 申报**，也不得写成「已取得 TS」。

## §R9.2 E2 通道 A：又一次伪鞍点 + IRC 失败（两项证伪）

- 频率（`ts/ts_0009/jobs/declaration_0005/frequency/frequency.log` 375,703 B，sha256 **185d01fa41677507e672e29953892f8f11b92a839ac02bc6f5b3e8c9d1e114d4**）：**L1507** 1 imaginary、**L1516** `Frequencies -- -32.6774  15.9782  25.0955`；39 组 = 117 模；L5316 Normal termination @12:25:15。
- **模组成（我自算）**：|d| 前六 = atom41 0.359 / atom40 0.323 / atom38 0.287 / atom37 0.279 / atom14 0.214 / atom35 0.201（芳香环 H 为主）；watch atom {1,2,4,28,29} 平方位移占比仅 **4.0%**；分对 |d|：(1,29) 0.112/0.076、(2,4) 0.093/0.041、(1,2) 0.112/0.093、(28,29) 0.106/0.076 ⇒ **pseudo-saddle**，非声明单步 TS。（lane 报的 0.19% 是键向投影口径，与我的集合口径同量级，均 ≪ 判据。）
- IRC job 1040 `…/declaration_0005/irc/irc.log` 815,322 B，sha256 **5479aa7945951dce0ef590cb0b4eca6864bf794b7c106098d56c7d22b9c71682**；L13494 Delta-x NOT Met、L13495 Maximum number of corrector steps exceded、**L13496 Error termination via Lnk1e in l123.exe at 13:02:30**。
- ⇒ E2 = 「未取得合格鞍点」+「IRC 失败」两项证伪；`result.outcome` 仍 null、不回填。

## §R9.3 决策（写权会话口径，已同时报文给主协调）

- **不建议**为通道 A 再换 guess 重建：本轮已是同型伪鞍点第二次 + IRC 第三次 l123，继续在同一 seed 家族上试错没有证据增量。
- **通道 B 按 candidate_only 交付**（+15.36、−314.2861 cm⁻¹、[1,29] 主导、CIP (8S,29R)），并**显式写明缺什么**：双向 IRC 连通性 + 两端点 Opt+Freq。若主协调愿意为这两项开口子，最小补测清单是「TS_B 的 IRC 加倍 maxpoints/更小步长」+「reactant/product 两端点 Opt+Freq」；**在得到授权前我不提交任何新作业**（当前口径禁手工作业，且本包手工在飞 0）。
- HI1 的**回填计数仍为 0/4**，四条边 `result.outcome` 全部 null；终稿（已发布帖 evt_7fbdfb416f1e41bf）中 EM1 段与 E2 行的「已提交/进行中」措辞由本追加轮**取代**为「candidate_only + 明确缺测」与「伪鞍点 + IRC 失败」，其余结论不变。

## §R9.4 追加轮通告已发布（13:32 CST）

- 帖子 **evt_337e3044d87c4ce8**（主题 gold-finish-20261015，首行 to: as_d9005401ea014f4e，cc as_a341823c436e47ed）；投递：as_d9005401ea014f4e **delivered**（message_event_id evt_c16e9159145d405b）。
- 内容：通道 B = candidate_only（+15.36、−314.2861 cm⁻¹ 由 [1,29] 主导、CIP (8S,29R) 我自算复核）+ 缺「双向 IRC 连通性、两端点 Opt+Freq」；通道 A = 伪鞍点 + IRC l123 两项证伪；回填仍 0/4；**不申请新作业**，仅在主协调明确授权时才做最小补测（TS_B 的 IRC 加 maxpoints/减步长 + 两端点 Opt+Freq）。
- 仍在跑的管线作业：**1043 = ts_0011 product_frequency（E3 产物端点频率）**，属 workflow 自动推进、非手工提交；若其终态为 0 虚频，可作为 E3 §9 步 B 终点的端点证据写入下一轮追加，但**不改变** E3 的 outcome=null。

## §R9.5 E3 端点身份证伪 + 平台 verdict（13:34 CST，我独立复核）——取代 §R9.4 中「1043 仍在跑」与终稿 E3 行措辞

- **E3 两个端点槽都弛豫回 I2**（`ts/ts_0011/jobs/declaration_0004/`）：`product_frequency/product_frequency.log`（374,811 B，sha256 **b5f62db2d4f2630b7c51cec44f01bb5e21b41ac74f2ccf45574199266f5f046f**）收敛点 **-939.320655496**（L819），**117 模 0 虚频**（39 组 Frequencies，无 imaginary 行），最低实模 35.3112/46.4293/50.2885（L1515），ZPE 0.345935（L3473），L5301 Normal termination @13:33:07；`reactant_frequency/reactant_frequency.log`（sha256 **139a17b917f196387276142a4c3ae5a88b9cc0433eff114373914509b798ad0d**）**-939.320655386**（L817），0 虚频，最低 35.3651/46.4611/50.3485（L1513），@12:37:51 终止。
- 与 job 961（I2 极小 -939.320655479、最低 35.3075/46.4262/50.3299）之差 **−1.7e−8 / +9.3e−8 Eh**，最低实模在噪声内 ⇒ **两端槽都是 I2，声明的产物 P 从未被到达**。此结论已由**平台判定独立确认**：ts_0011 **rev 51、stage verdict、terminal candidate_only**，verdict.reason 明写「product built MOL does not match its declared SMILES；两个槽的几何感知 SMILES 完全相同；candidate stays UNVERIFIED」。
- **E3 的 IRC（job 1033）只有正向 1 点 + 反向 1 点**（`.../irc/irc.log` 223,169 B / 3,672 行，sha256 **17da5ef2a63e7af2a4a1e232ef06d9b8ceb3e488504e0f9bad569a87dc071edb**，L2058），**共 2 点**（L1489 `Point Number 1 in FORWARD path direction.` → L2110 `Point Number: 1 Path Number: 1`；L2170 `Point Number 1 in REVERSE path direction.` → L2793 `Point Number: 1 Path Number: 2`；**L2862 `Total number of points: 2`**），L3672 Normal termination @11:32:37 ⇒ **无终点区间证明**（结论不变）。
- ⇒ **E3 的措辞升级**：由「ts_opt 收敛到 I2 盆地浅驻点 + 1029 伪鞍点」（§R8.43）追加为「**声明的两端（reactant/product 槽）经 Opt+Freq 都回到 I2（0 虚频），产物端点身份被证伪；平台 verdict = candidate_only（verified=false）**」。E3 的 **outcome 仍非 verified、ΔE‡ 仍 missing、分母仍锁 -939.320655479**；上列能量只作身份/连通性证据，不进 ΔE‡ 或分母。
- 已建共享研究记录 **`HI1/PROCESS.md`**（sha256 **4fed6ab24582c36e24f31ccd2967a3b520f579a8ee1c105860c6f5382cc072f1**）：假设 H1–H4、直接观测（含路径与 sha256）、判定结论、四条有区分力的下一步（均需授权、未提交）、未决风险。
- 复核纪律：1043/1041/reactant_frequency 均为**管线自动推进**作业（非我或 lane2 手工提交）；我本轮写盘仅 STATUS 与 PROCESS.md，**未提交任何新作业**（本包手工在飞 0）。

## §R9.6 E3 结论通告已发布（时刻标注见 §R9.8 勘误）

- 帖子 **evt_01a629f0fe9046bf**（主题 gold-finish-20261015，首行 to: as_06db52ada5014800，cc as_a341823c436e47ed），投递 delivered。内容：我方独立复核两槽 → 均为 I2（0 虚频、能量差 1e−8 Eh 量级）；平台 verdict（ts_0011 rev 51 terminal candidate_only、reason 明写两槽几何感知 SMILES 相同、product built MOL 与声明 SMILES 不符）；IRC 1033 仅 Pt 1 Step 1；终稿 E3 措辞升级；PROCESS.md 建文件信息；下一步四项测试均需授权。
- 与 lane2 的一处**小数差异（不影响结论）**：reactant 槽最低实模我实测 35.3651/46.4611/50.3485（L1513），lane2 报 35.3946/46.4741/50.3614；两者都与 I2 的 35.3075/46.4262/50.3299 同量级，身份判定不变。已请其确认来源，未回不影响交付。
- 本包当前对外结论（供主协调定稿直接引用）：**E1 缺测（截断读数）、E2 伪鞍点+IRC 失败、EM1 candidate_only（+15.36 未验收）、E3 candidate_only（端点身份证伪、平台 verified=false）**；回填 **0/4**、ΔE‡ 全部 **missing**、题源零改动、守卫 4 passed。

## §R9.7 勘误：job 1033 IRC「无反向点」→「正反各 1 点、共 2 点」

- 我 13:34–13:37 的表述「job 1033 只有 Pt 1 Step 1 一点、**无反向点**」错误。经 `grep` 复核：L1489 `Point Number 1 in FORWARD path direction.` → L2110；**L2170 `Point Number 1 in REVERSE path direction.` → L2793**；**L2862 `Total number of points: 2`**；L3672 Normal termination @11:32:37。同文件 sha256 仍为 `17da5ef2…`（未变）。
- 受影响范围：仅该句表述（§R9.5、PROCESS.md §2 第 3 条、13:37 通告 evt_01a629f0fe9046bf）。**结论不变**：2 点不足以构成终点区间证明 ⇒ E3 无连通性证据、candidate_only、ΔE‡ missing、分母仍锁 -939.320655479。
- 同轮改档：STATUS（本文件现 sha256 **29b0b413…** 起算，见 §R9.7 追加后终值）、PROCESS.md **021d85ac5ee59c3da28ff942bc08925838af35c2ef7928fb6e0be822812b8f48**。
- 同时定案口径：最低实模一律取 `Frequencies --` 频段表（reactant 35.3651/46.4611/50.3485；product 35.3112/46.4293/50.2885），`Low frequencies` 探针行只用于识别平动/转动伪迹（差额 ~0.03 cm⁻¹），已写入 PROCESS.md。
- 勘误通告：**evt_548c0886d81c47f6**（to as_06db52ada5014800，cc as_a341823c436e47ed，delivered）。

## §R9.8 时刻标注勘误（再次自罚，只涉时刻）

- §R9.6 原写「13:37 CST」、§R9.7 原写「13:42 CST」，**这两个分钟数未经同轮 `date` 实测**（当时最近一次实测为 13:34:01，本次为 **13:35:43**）⇒ 已从标题删除。§R9.5 的「13:34 CST」有 `date` 实测支撑，保留。
- 受影响范围：仅这两处时刻标注（以及 13:37 通告 evt_01a629f0fe9046bf 与本轮勘误帖中对「13:37」的转述）。能量、行号、sha256、判读结论均不受影响。
- 纪律复述：此后本节之后的一切时刻一律在写入前用 `date` 实测；无实测即写区间或省略。
## §R10.1 拆步+多组分开工登记（本轮实测时点见同轮 date）
## §R10.2 主协调裁决（14:0x CST）已执行：E3 无苯甲酸旁观组分；EM1 纳入本轮
## §R10.3 hi.py I1 已改写为 5 步（E1/E3 双拆）+ 生成器与守卫通过（本轮实测）
## §R10.4 主协调对 hi.py 落地的复核与三条裁决（已执行）

- **主协调独立复测**（非引我回执）：hi.py `0ac110bc…`、HI1.json `54221e65…`；同轮复测交付面其余文件**全部未变**（jl.py 944346f4…、hard.md 4940fa66…、normal.md 771a6c7f…、HL1.json **240865b1… 与冻结值逐字符一致**、NI5 a95ce872…、NR1 6eab2f24…、NY3 4e7e754e…、tests 037a424b…）⇒ **重生成无旁损**，我的 HL1 判断成立。
- **HEMI 裁决：采纳候选 A（我已落地的版本）**，追加一致性核对：hemiaminal_41 Opt+Freq 收敛后，同轮把「收敛几何的质子归属 + 各 O–H 距离」与节点字符串逐项对照；若实测把质子放在羧基氧，则在 hi.py 注释与报告里**双写**「字符串=醇盐氧表示 / 实测=羧基氧，同一物种共振等价，O–H 距离 xxx」。**禁止**节点字符串、证据日志、报告三者静默不一致；证据 gjf 的 `smiles:` 注释必须与节点同字符串，若与几何质子位置不同则在同一行注明等价关系。
- **交付面扩列**：HI1.json 属预期变更，**不在原冻结 11 文件清单内** ⇒ 新版交付清单必须含 **hi.py（0ac110bc…）+ HI1.json（54221e65…）**，并注明与旧清单的关系（本条已由主协调记账，我这里记「交付面扩列」）。
- **1047 不取消、不 kill**（平台无作业级 cancel）⇒ 只作方法学对照，确认正确。
- **barrier 回填纪律（新增）**：**不得先改 hi.py 的 null 占位**；四条边逐条「TS 频率合格 + 两端 0 虚频 + 连通性」齐一条填一条，**每填一条重跑一次守卫并报 sha**；E3a 的 ts_prepare 猜测仍须从 **job 961 末帧**起算。

## §R10.5 进度快照（14:05:22 实测）
## §R10.6 主协调前瞻提醒（已记入执行清单）
## §R10.7 RC_27（job 1044）opt 段收敛、freq 段在跑（14:06:10 实测）
## §R10.8 主协调两点确认（记入执行清单）
## §R10.9 E3a 的 TS 猜测裁决（14:1x CST）

- lane2 报两枚猜测：**G1** `prep/guess_c2o25_190/ts_guess_c2o25_190.xyz`（sha 2568ca03…，R(C2–O25)=1.8996、O10–H27 1.5015、C2–N4 1.3308）与 **G2** `prep/guess_c2o25_160/ts_guess_c2o25_160.xyz`（sha 2b569cfe…，R=1.5996、O10–H27 1.0048、C2–N4 1.4012），均源自 job 980 受约束扫描、其起点为 job 961 末帧（满足「同构象、不另建」硬条件）。
- **裁决：两者都不直接用**。G1 正是 job 999 已失败的起点（甲基转动伪鞍点 −128.0397 cm⁻¹），原样重跑＝重复失败；G2 已在 hemiaminal 盆地（job 1028 从它极小化即落到 hemiaminal），从它起 TS 更可能滑回极小。
- **改走方案 C-lite（零新增算力）**：先读 job 980 的 `E3/runs/preorg_v3/scan_c2o25_220_160.log`，把 E(R) 全表（R、SCF、行号）报出；若 2.20→1.60 窗口内**有内点极大**，就用该帧作 E3a 猜测（provenance 落成真实文件：扫描 log 行号 + 抽帧 xyz + sha256）；若单调无极大，才用一次加密松弛扫描（1.60–2.00）的最高点作猜测（需槽，排在 E1a TS 之后）。
- 约束纪律：禁用裸 `B i j value`（job 962 有被静默忽略、几何滑回 R=3.1597 的记录）；用约束前先做小作业验证末帧 R 实际值。
- 数值纪律：RC_27 的 −593.934532807 只属 E1a 侧 27 原子模型，不混算进 E3；E3 仅两个分母（E3a = job 961 −939.320655479；E3b = 待算 hemiaminal 41 原子极小）。

1) **模型账证据（要写进报告）**：27 原子子体系 −593.934532807 Eh 与 41 原子含苯甲醛体系 −939.31 Eh 量级的差 ≈ 苯甲醛单体的量级 ⇒ **旁观组分拆分未改变物种账**，可作为「模型约化正确」的证据之一。
2) **freq 段收尾的三条硬断言**：① `Frequencies --` 块数 = **25**（27 原子 ⇒ 3N−6 = 75 模，每块 3 模）；② `imaginary` 行数 = **0**；③ `Low frequencies` 探针行**不作判据**。若出虚频：先报最低虚频数值 + 模矢 + 几何差，不重投同型。freq 正常结束后 **E1a 分母固定为这个 RC_27**（同程序同批），随后 INT1_27 与 E1a ts_prepare。
- 当前（14:06:54 实测）：`RC_27_optfreq.log` 850,689 B / 13,457 行，**Frequencies 块数仍为 0**（freq 段 Hessian 尚未出表；L13017 为 freq 段首个 SCF），仅有 opt 段终止行 L12487。

- `E1/split/RC_27_optfreq.log` **850,689 B，sha256 a4d52542708ee1d8f4b0712ccbd8f9c93f59cc060b5aadbdc0e7062c5146ff66**：末次 SCF **-593.934532807**（L11565；L13017 为 freq 段首个 SCF，同值）；**Optimization completed L11841 / Stationary point found L11842**；**opt 段 Normal termination L12487 @14:04:13**；**freq 段仍在跑**（`Frequencies --` 组数 0、无 `Low frequencies`/`Zero-point`）⇒ **75 模 / 0 虚频尚未出来**，job 1044 仍 running。
- 体系核对：27 原子 C8H15NO3（脯氨酸+丙酮）在 −593.93 Eh 量级收敛；41 原子含苯甲醛体系在 −939 量级，差值正是苯甲醛（约 −345 Eh 量级）⇒ 与「旁观组分拆出」的模型账一致。
- 队列（同轮）：running **1044（freq 段）+ 1046 + 1047 + 1048（NY3）** = 4/4；queued **1049（EM1 下扫）、1050（NY3）**；free cpus 0 ⇒ INT1_27 与 hemiaminal_41 均需排队，属预期。
- 已下发 lane1：等 freq 收尾→报 75 模/0 虚频→提交 INT1_27 Opt+Freq→准备 E1a 的 ts_prepare（evidence_refs 必须是盘上 artifact；被拒则 ts_resume 只改该字段）。已下发 lane2：v2（sha 9e53e0ba…）为唯一待提交版本，旧 226430f5… 降级，5 项核对保留。

1) **E1a 的 ts_prepare 起跑前**：guess 的 `evidence_refs` 必须是**盘上已存在的 artifact 文件路径**（例：RC_27 末帧 xyz / 测量脚本输出），纯文本会被平台以 `provided_guess_invalid` / "Provided candidate provenance artifact missing" 拒；若被拒，用 `ts_resume` 只改 `guess.evidence_refs` 一个字段，并按回执核对 rev bump 与 `changes` 仅含该字段。⇒ **起跑前先落 provenance note 与末帧坐标文件**。
2) **槽位纪律**：1046/1047 不为「补回」再提交；RC_27 一收敛立刻起 E1a TS（优先级高于 hemiaminal_41）；若 RC_27 出多虚频或失败，**不立刻重投同型**——先报虚频模矢与几何差，再定改起点还是改约束。
3) **π 降级 ≠ 断键** 的说明保留在报告里：E3a 的 `break [2,20]` = C2=N20 的 π 由 2 降 1（生成器记法，同 E1a 的 `break [2,4]`）；`break [4,22]` / `form [5,22]` 是图级质子记账。

- 队列 running：**1044（RC_27 Opt+Freq，step 17/149，18 条 SCF，828,645 B）+ 1046 + 1047（lane2 截断模型）+ 1048（NY3）** = 4/4 满；queued：**1049（EM1 下扫）、1050（NY3）**；free cpus 0。
- **E1a 的 ts_prepare 仍无槽**（等 1046/1047/1048 让位或 RC_27 收敛后腾出），按 E1a > E3a > E1b > E3b > EM1 > E2 排队。
- E3 图字符串的 bond_changes 语义（回应 lane2 的提问）：E3a 的 break [2,20] 是「C2=N20 的 π 由 2 降 1」在生成器约定下的记法（与 E1a 的 break [2,4] 同理），**不是** N–C 键消失；break [4,22]/form [5,22] 是「水 H 转到醇盐氧」的图级记账，与 job 1028 实测的质子落羧基氧属同一物种的互变异构表示（已按主协调要求在注释与报告双写）。

- **hi.py 改前 sha256** `a0372a924ed90962ff819d5b3919535d81f7c34396d2d26ea68bf9ba2562094c`（备份 `/tmp/hi_py_backup_140116.py`，7,476 B）→ **改后 `0ac110bc7e5b57618c1cc272cb93caa3054d3204c5db185d512330f3e97bc4cc`**。
- **结构**：I1 由 3 步 → **5 步**：R →(E1a, 行 66)→ 半缩胺 →(E1b, 行 82)→ 烯胺 →(E2, 13.36 旧值)→ 亚铵-醇盐 →(E3a, 行 104)→ 半缩胺(hemiaminal) →(E3b, 行 123)→ P；competing 的 `from_step` 由 1 改为 **2**（行 144）。
- **生成器**：`python -m cloudra.benchmark.gen_hard_tasks --check` → `OK HI1: 13 nodes, 6 edges`（其余 9 题不变）；正式重生成 → `wrote 10 tasks`。
- **HI1.json 改前 `5fd0ecb2eefcf6b185484eba59f27e10604adac7883ddc679d13afe6d91539dc` → 改后 `54221e6591c75f88d2f6d96e853302c48bb25aefb9cc191aab2f6113119b61d0`**。
- **守卫**：`pytest tests/test_benchmark.py -k hard_tasks_regenerate_identically -q` → **1 passed**。
- **competing 断言（主协调要求）**：`enamine node id = HI1_I2`，`HI1_EM1.from = HI1_I2` ⇒ **ASSERT True**（副面通道挂在烯胺上，不再挂到半缩胺）。
- **新边 barrier 全部 null**：HI1_E1(E1a) None、HI1_E2(E1b) None、HI1_E3(E2) **13.36（旧程序旧模型的 L2 身份值，已在 type 文本显式标注「非本轮实测」）**、HI1_E4(E3a) None、HI1_E5(E3b) None、HI1_EM1 15.52（同旧值口径）。
- **HEMI 图的电荷/标签一致性（我自测，非 lane 转述）**：候选 A（质子留在 O4、H22 转到醇盐 O5）→ 映射集 1–22 守恒、**形式电荷 0**，推导 break [[2,20],[4,22]] / form [[2,4],[5,22]]；候选 B（质子转到羧基 O15）→ **电荷 −1**，被生成器守恒检查否掉；lane2 给的「首选版」把 O4 上的 H 写成未映射 `[H]`，会让 map 21 消失 ⇒ 同样不可用。**故采用候选 A**，并在 hi.py 注释里写明「job 1028 实测几何把中转质子放在羧基氧（O10–H27 0.9949），与图字符串在醇盐氧是同一物种的质子共振等价表示」。
- **HL1.json 未被本次重生成破坏（证据）**：`cloudra/benchmark/hard_registry/jl.py:41` 就是 `"barrier": 0.0`，即生成器本该输出 0.0；`git diff` 显示 HL1.json 相对 HEAD 只差这一行（null→0.0），与重生成前一致 ⇒ 本次写入对 HL1 **无内容改动**。
- **平台无「作业级 cancel」工具**：可用的只有 `mark_compute_job_failed`（失败登记，且受活动锁保护），不是取消；故 1047 不取消、任其跑完（不 kill 进程）。
- 待办（等证据）：E1a/E1b/E3a/E3b 的 barrier 分别等 RC_27、carbinolamine_27、job 961（已有）、hemiaminal_41 的分母 + TS 频率 + 两端 0 虚频 + 连通性证据齐了再填；填的时候只改对应 `barrier` 键并重跑生成器 + 守卫。

- **裁决 1（更正我此前的错误前提）**：E3 的物种是 **41 原子 C15H21NO4 单分子**（脯氨酸 C5H9NO2 + aldol 片段 C10H12O2，以 **C2–N20** 相连；job 1029 的 117 模 = 3×41−6 印证）**+ H2O(3 原子)** 两个组分，全中性 q0/m1 —— **不存在苯甲酸/苯甲酸根旁观组分**。lane3 的独立实测（芳环 = Ph–CH(OH)–、羧基在吡咯烷 C9、O25 为水）与此一致。⇒ 苯甲酸、苯甲酸根两项任务**作废**。
- **E3 新边与分母**：E3a = 41 原子亚铵-醇盐 + H2O → **hemiaminal 44 原子 C15H23NO5**（水并入、成 C2–O4），分母 = 亚铵-醇盐(41)；E3b = hemiaminal(44) → **P = aldol(24) + 脯氨酸(17) dot-joined complex(41)**，分母 = hemiaminal(44)。频率断言按原子数：41→**117 模**、44→**126 模**。
- **我的一个判定（已在通告中写明理由）**：E3a 分母优先直接用 **job 961**（`-939.320655479`，41 原子、117 模、0 虚频、已独立核），因为它就是同一 41 原子亚铵-醇盐物种，而「不复用」清单只点名 1017/1028/1029；若 lane2 认为本轮模型一致性必须重算，需报理由再起作业。
- **裁决 2（E1 侧写法）**：节点 SMILES **保留完整 dot-joined complex（含苯甲醛 maps 5–12）**，不把旁观组分从节点删掉（否则 E2 的差集会出现苯甲醛凭空进出的假键变化）；证据按组分给（27 原子子体系单独 Opt+Freq/TS，苯甲醛 14 原子单独 Opt+Freq，日志 input 前加 `smiles:` 注释），`type` 文本写「模型约化：旁观组分苯甲醛按分离组分计算、不进该步分母」。E1 分母 = RC_27 / carbinolamine_27（均 **75 模**），苯甲醛 **36 模**。
- **裁决 3（EM1 纳入本轮）**：lane3 已改派 —— 沿 C1–C29 成键坐标从 job 1032 末帧做**受约束弛豫扫描**（双向、步长 ≤0.05 Å、单调单峰）+ **两端 Opt+Freq（0 虚频）** + 端点身份核对（几何感知 SMILES）；补齐后只能写「**verified（替代口径：无 IRC）**」，不得写 IRC 双向到达；job 1026 的失败 IRC 永不作连通性证据；+15.36 在补齐前保持 candidate_only。E2 排最后、仅一次机会（起点 = enamine·benzaldehyde 41 原子 complex，不含水）。
- **并发实况（13:57:46 实测）**：running 1044（RC_27）+ 1045（BZA_14），NY3 在飞 0，free cpus 16/slots 8 ⇒ HI1 占 2、**剩余 1 槽留给 E1a 的 TS**（RC_27 出 0 虚频即起 ts_prepare），不把小分子单体铺满。
- **hi.py 仍未动**：等 lane1/lane2 交映射 SMILES 字符串；到手一次成型改 5 步并跑生成器 + regenerate_identically 守卫。

- **授权**：用户 2026-10-17 13:5x CST 同意「拆中间体、旁观中间体拆成多组分」；主协调同时把算力放宽为「全局在飞 ≤4 个 g16、每作业 ≤8c/≤10240MB、HI1 最多 3 个」。
- **lane1（as_700f852fe3af412f）已提交**：**job 1044** = RC 子系统 Opt+Freq（27 原子 C8H15NO3 = 脯氨酸+丙酮，输入 `E1/split/RC_27_optfreq.gjf` sha256 7fb6f67f8c96fb0d1ee9d828c14dd45f8936f62398cc53ed7bc9819bcf25819f；起点 `E1/split/RC_27_start.xyz` sha256 eb193d5f02a75b42d3dc449e50e389f11736737fb01ba2fdcd9e24eaff25c7c4，2 片段 = 丙酮 + (S)-脯氨酸，由 built reactant 去掉原子 11–24 得到）；**job 1045** = 苯甲醛 spectator Opt+Freq（14 原子 C7H6O，输入 sha256 8fa424207a120717a9094c268ad24bfd64fe8db172165c59c2e3107c9b0956a3，起点 sha256 0234f6f9142587b6d7f8125adb7d56780542a8c529716021563b5382b600f761）。route 逐字 `#p opt freq B3LYP/def2SVP empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=dmso)`，q0/m1、8c/10240MB/prio 0。
- **lane1 已备好第 3 步**：INT1_27（27 原子两性离子 carbinolamine）起点 `E1/split/INT1_27_start.xyz` sha256 3c48099cf8e77f2bad7a5379901a23ab68503bdedc620955ae18f1ce0ad91a40（取自 job 1017 末帧 L159994 同剖分）。
- **lane1 声明的模型条件（重要，写进终稿时必须复述）**：只有 CPCM(DMSO) 连续介质，**无显式溶剂/抗衡离子/外加碱**；41 原子模型里苯甲醛距反应中心 2.6–3.7 Å（可能提供 H 键）；27 原子模型的两性离子只靠连续介质稳定 ⇒ 旧 +41.39 kcal/mol 质子转移鞍点可能因「缺质子受体」被抬高；可检验假设 = 脯氨酸 COOH（built 25/27）作分子内质子穿梭。**这些都不改变方法声明，但必须随新边数值一起写明**。
- **重复风险已处理**：lane1 的 job 1045 已覆盖苯甲醛 spectator，我已通知 lane3 **不要再提交苯甲醛**，改做苯甲酸 spectator；并保留「−1 苯甲酸根需先问电荷账」的约束。
- **hi.py 尚未动**：等 lane1/lane2 给出两条新边的映射 SMILES 后一次成型改写（R→carbinolamine→I1→I2→hemiaminal→P 共 5 步），barrier 先 null，跑生成器 + regenerate_identically 守卫后报改前/改后 sha 与行号。

## §R11 阶段实测（14:12–14:22 CST，本 Coordinator 自读日志）

### §R11.1 RC_27 = E1a 分母，verified（我自己读的终态）
- 路径 `gold_finish_20261015/HI1/E1/split/RC_27_optfreq.log`，15,572 行，sha256 `9d68305052b492c15774082f528f94acf61ffcee9885d8729f020ed1a20589dd`（终态、不再增长）。主协调 14:0x 引用的 `a4d52542…` 是中间态哈希，一律以 9d683050… 为准。
- 硬断言：**'Frequencies --' 带数 = 25 ⇒ 75 模 = 3N−6（N=27）**；对 25×3 个数值逐项筛负值，**命中 0 个 ⇒ 0 虚频**；log 中无 'imaginary' 行。
- 首带 L13474 `Frequencies --     21.4691                25.1412                41.4769`；末带 L14290 `Frequencies --   3169.1001              3470.3495              3733.9233`；ZPE L14387 `Zero-point correction=  0.228709`（仅备查，不进纯电子能垒）。
- 收敛/终止：L11841 `Optimization completed.` / L11842 `-- Stationary point found.`；L12487 `Normal termination ... 14:04:13 2026`（opt 内部 step 1）、**L15572 `Normal termination ... 14:07:03 2026`（整作业）**。
- 能量：**E(RC_27) = −593.934532807 Eh**（L11565 opt 末次 SCF、L13017 freq 段复算同值 ⇒ 同批同法可作差）。
- 几何（L12515–L12541 坐标块）：C2···N20 = 3.757 Å、O4···H21 = 2.030 Å、N20–H21 = 1.023 Å、C2=O4 1.220 Å ⇒ **RC_27 是松散 N–H···O=C 氢键复合物**。后果写进终稿：E1a 的 ΔE‡ 因而含「N 进攻前的结合/去溶剂化代价」；且 RC_27 末帧不得直接当 E1a 猜测。

### §R11.2 E1a 猜测 artifacts（lane1 落盘，我核对存在性与 sha）
- 猜测几何 `E1/split/INT1_27_start.xyz` sha256 `3c48099cf8e77f2bad7a5379901a23ab68503bdedc620955ae18f1ce0ad91a40`（27 原子，元素序与 `RC_27_opt_frame.xyz` 相同，sha256 `c1f789e0b6653c7de55a291c98f28dd3088f1e6cb3c0124617abecda398f691a`）。
- provenance note `E1/split/E1A_GUESS_PROVENANCE.md` sha256 `560faf431a35cd4adfe7e45f0dd6bef9e15cf1f8580adeb0a8d627fb5339c319`（含来源 log 路径+sha+行号、索引映射、分母、模型条件 §5）。
- 来源链（note §2 自述）：`ts/ts_0008/jobs/declaration_0003/ts_opt/refine.log` sha `0e726b32…`（L159450 step 165/246、L159743/L159744 收敛、L159994 末帧 41 原子 Input orientation）+ `frequency/frequency.log` sha `a5783c38…`（L1507 `1 imaginary frequencies`、L1516 `-1547.0708`，虚频模 H 主导 (3,41) 0.932 / (32,41) 0.795 = (C3,H22)/(N20,H21)）。
- 该猜测的化学：C2–O4 1.362、C2···N20 1.633、N20–H21 1.226、O4···H21 1.334、C3–H22 1.097 ⇒ 晚期协同「胺加成 + N–H 质子转移」鞍点。
- 索引约定（note §1）：工作序 1-based C2=2、O4=3、C3=4、H22=10、N20=18、H21=27；atom_map = 恒等 1..27。

### §R11.3 INT1_27 = job 1051（HI1 第 3 个在飞作业）
- 14:10:04 起跑，14:12 实测：`E1/split/INT1_27_optfreq.log` 237,563 B，step 4/162（L2580/L3256），末次 SCF `−593.873744488`（L3182）。
- **中间读数**：相对 RC_27 高 **+38.1 kcal/mol**（(−593.873744488) − (−593.934532807) ×627.5095）——与「从 41 原子鞍点帧截去苯甲醛」的高能起点一致；只作过程读数，**不作任何分母、不进 ΔE‡**。
- 风险与判定口径（lane1 已接受并写入其记录）：起点是质子转移鞍点帧（N20–H21 1.226 / O4–H21 1.334），可能滚回松散复合物。判据 = 终态 0 虚频 + O4–H21 ≈0.97 Å + N20···H21 ≈2.0 Å + C2–N20 ≈1.47 Å ⇒ carbinolamine_27 成立；若滚回复合物或出现多虚频 ⇒ 先报模矢与几何差，再用 internal_coordinates 只沿 H21 转移方向位移重建一次起点，两次结果都上报（不掩盖）。

### §R11.4 队列实况（14:12–14:20 实测）
- running：1046（HI1 截断 I2_reduced）、1049（HI1 EM1 下扫 `E2EM1/spectator/scan_down_c1c29.gjf`）、1050（NY3 `NY3_R2/scan_O6C4.gjf`）、1051（HI1 INT1_27）。
- queued：1052（NY3 `NY3_R2/rc_cont_optfreq.gjf`，waiting: not enough free cpus/memory）。
- terminal：1044 done（RC_27）、1045 done（BZA_14）、1047 done（HI1 截断 hemiaminal）、1048 **failed**（NY3，l9999 @14:08:17，非本包）。
- 容量：free cpus 0、in_flight 4/4；**HI1 在飞 = 3（1046/1049/1051）= 已达 HI1 上限 3** ⇒ 现在不得新提交；E1a ts_prepare 待任一 HI1 作业释放后提交，且**优先于 hemiaminal_41_optfreq_v2**；不得重投 1046/1047 来补槽位。
- 1047 截断 hemiaminal（**lane2 报告值，我未逐行复读**）：log `E3/runs/reduced/hemiaminal_reduced_optfreq.log` sha `315bdeb744c7f1b416acb1e74f0a60e90848d1c470888feb933f47ddbf959235`，E −593.948060506（L9834），25 组 Frequencies = 75 模 = 3×27−6、0 虚频、ZPE 0.232338（L12681），opt 段终止 L10768 @14:06:35、freq 段终止 L13891 @14:10:03。用途固定为「截断模型 + 数值 + 方法学对照」：不作 E3a/E3b 分母、不进 ΔE‡、不进 hi.py 节点、不与 41 原子体系能量混排。

### §R11.5 E3a 猜测裁定 = S2（内插 1.82 Å），S1 备选，G1 不作首选
- 依据（job 980 剖面，零新增算力）：`E3/runs/preorg_v3/scan_c2o25_220_160.log` sha `436c4cd9225bd29c1ae65086e1394b27b886e4d45206f4efa91133b331030f66`（60,977 行，约束卡 L158 `B 2 25 S 4 -0.150`，汇总 L59910/L59911）：
  2.19959 Å / −939.307665623（+8.15）→ 2.04959 / −939.302902987（+11.14）→ **1.89959 / −939.297771992（+14.36，极大）** → 1.74959 / −939.301357590（+12.11）→ 1.59959 / −939.309047571（+7.28），基准 = job 961 末帧 −939.320655479。
- 读法：单峰，极大在 1.90 Å；但 R(O10···H27) 在点 3 仍 1.5015、到点 4 才 1.0242 ⇒ **C2–O25 压缩峰与质子转移不同步**，真鞍点应在 1.90–1.75 Å 之间。
- **撞车**：点 3 帧就是 G1（sha `2568ca03…`），即 job 999 已失败起点（opt=(TS,calcfc,noeigen) 滑回 I2 盆地；其 freq job 1029 单虚频 −128.0397 cm⁻¹ 为 C3 甲基转动 pseudo-saddle）⇒ 不原样重跑 G1。
- 裁定：**首选 S2** = 在点 3 与点 4 之间按 R(C2–O25) 线性内插到 **1.82 Å**（预期 O10–H27 ≈1.25、C2–N4 ≈1.35）；**备选 S1** = 点 4 收敛帧 `prep/guess_c2o25_175/ts_guess_c2o25_175.xyz` sha `db055959e7ffe9277f9e71b253c6873574a3c6d7c712c194d9f7916fc5867fd5`（R=1.7496 / O10–H27 1.0242 / C2–N4 1.3742）；**G1 仅在 S1/S2 都失败后**，且必须先做小作业验证约束真生效（job 962 裸 `B i j value` 曾被静默忽略、几何滑回 3.1597）。
- S2 交付要求：provenance 写源 log sha + 两帧行号（L25258 点 3、L51856 点 4）+ 内插公式 + 距离表 + 可容许性自查（N–C 距离单调、minsep ≥0.9 Å），落盘后报 sha；**无槽不提交**。

### §R11.6 本包 ΔE‡ 现状（不得误读）
- 四条新边 E1a / E1b / E3a / E3b 的 ΔE‡ **全部 missing**；hi.py barrier 仍 null（回填 0/4）。
- §R11.5 的 +8.15…+14.36、§R11.3 的 +38.1、以及旧的 +0.98/+5.04/+15.36 全部**不是 ΔE‡**（前者是沿受约束坐标的剖面差 / 中间读数，后者是相对其他极小值或旧口径）。

### §R11.7 同轮更正与三项硬检查（14:26 CST）
- **更正（lane1 提出、我采纳）**：`E1/split/INT1_27_start.xyz`（3c48099c…）是 job 1042（−1547.0708 cm⁻¹）的质子转移**鞍点帧**，H21 仍在 N20/O4 之间（1.226 / 1.334）⇒ 只能作 **E1a 的 guess**，**不得**作 `conformers.product` / `verification.product_endpoint` 的种子（否则等于把鞍点当产物端）。E1a 的产物端种子必须用 **job 1051 收敛出的 carbinolamine_27 极小值帧**（判据：0 虚频 + O4–H21 ≈0.97 + N20···H21 ≈2.0 + C2–N20 ≈1.47），这也是 E1b 分母的同一硬依赖。
- **minsep 自查（我实测，脚本直读 xyz）**：INT1_27_start.xyz 27 原子最小原子间距 = **0.9749 Å**（工作序 13=O、19=H，羧基 O–H）；RC_27_opt_frame.xyz = 0.9737 Å（同一对）⇒ 均 ≥0.9 Å，无「删掉苯甲醛后的伪近距」。关键距离复算：guess 帧 C2–N20 1.633 / C2–O4 1.362 / N20–H21 1.226 / O4–H21 1.334 / C2–C3 1.531；RC_27 帧 C2–N20 3.757 / C2–O4 1.220 / N20–H21 1.023 / O4–H21 2.030。
- **字符串一致性（以生成器真值为准，非自拟）**：`ideapool/tasks/hard/HI1.json` 的 HI1_R = `CC(C)=O.O=Cc1ccccc1.O=C(O)[C@@H]1CCCN1`、HI1_I1 = `CC(C)(O)N1CCC[C@H]1C(=O)O.O=Cc1ccccc1`（13 nodes / 6 edges）。lane1 拟用于 ts_prepare 的 reactant `CC(C)=O.O=C(O)[C@@H]1CCCN1` 与 product `CC(C)(O)N1CCC[C@H]1C(=O)O` 分别是上述节点串去掉旁观组分 `.O=Cc1ccccc1` 后的**逐字符投影** ⇒ 与 hi.py 图谱不冲突（图谱保留完整 dot-joined 复体，证据按 27 原子子系统给）。边 HI1_E1 的 bond_changes = break [[2,4],[20,21]] / form [[2,20],[4,21]]，与双写一致。
- **主协调三条硬检查已下传 lane1**：(a) provenance 内列明被删的 14 个原子 = 苯甲醛 maps 5–12（1 个 C=O 的 O + 6 个芳碳 + 芳氢），剩余 27 原子与 mapped_reactants 1,2,3,4,22,13–21 一一对应；(b) minsep 数值写入证据（我已给出 0.9749 Å，lane1 须引用同一数值并注明测量方式）；(c) E1a 终态虚频**必须只有一个**，且模矢在 **N20 与 C2 上都有可观位移**、同时 H21/O4 有位移；若出现「纯质子转移」模（N20/C2 位移近零）⇒ 它只是质子转移子步、**不得**回填 E1a，须先报我，再改走 fallback 内插帧或把 E1a 再拆一档。
- **E3a 同类要求**：S2 起跑后须核「虚频模 = C2–O25 成键 + 质子中继」组成；若模矢由 C3 甲基转动主导（参 job 1029 的 −128.0397 cm⁻¹）即判 pseudo-saddle、不作 E3a TS。
- **必须写进终稿的定性**：+38.1 kcal/mol 的来源 = 受约束帧/两性离子在缺苯甲醛与显式氢键伙伴的 27 原子模型里被连续介质单独稳定；故 E1a 的 ΔE‡ 含「N 进攻前的结合/去溶剂化代价」，E1b 的分母是**模型内**高能两性离子极小值。若 job 1051 滚回松散复合物 ⇒ 按规则重建一次起点、两次结果都入册、E1b 暂记缺分母。

### §R11.8 14:31–14:35 CST：S2 猜测独立核验、E1a provenance 升版、排产与 EM1 升格条件
- **E3a 猜测 S2 已落盘（lane2 生成，我独立复算）**：`E3/prep/guess_c2o25_182/ts_guess_c2o25_182.xyz` sha256 **e3748c2c6c96af915c63d1fa8972187214916321999720667a68c9b2dd561b9e**（41 原子，元素计数 C15H21NO4）；provenance `PROVENANCE_ts_guess_c2o25_182.md` sha256 **518783131cbcfce2b682b443621c9c41c693247356f4880537de471bb318b322**；生成脚本 `E3/tools/mk_e3a_s2_interp.py` sha256 **08b2a83b9e433f2aaa30fe4442ca4ee01e2ebfca100e7e12da1685df772c6200**。我直读 xyz 复算：R(C2–O25) **1.8168**、R(O10···H27) **1.2467**、R(O25–H27) 1.2789、R(C2–N4) **1.3493**、R(O25–H26) 0.9633、R(O28–H24) 0.9752、R(C9–O11) 1.1782；**minsep = 0.9633 Å**（工作序 25=O、26=H，即水 O–H）⇒ ≥0.9 Å，与 lane2 自查一致。
- **S2 的两处透明处理（须随该猜测进入报告，不得省略）**：(i) 纯笛卡尔内插把转动中的 O28–H24 压到 0.8420 Å（低于 0.9 判据），已由脚本按两帧均值恢复到 **0.9752 Å**（方向保持，修复前值记录在案；这是唯一被修复的键）；(ii) 内插对距离非线性，出现键长假象（C9–O11 1.1782：两端 1.2480/1.2164；C9–O10 1.2689）。⇒ **S2 是构造出来的猜测（非收敛几何）**，上述假象由 TS 优化自行松弛，但必须在证据链中原文记录，且其修复是脚本化的、可复现。
- **E1a provenance 升版（lane1，我核过盘上文件）**：`E1/split/E1A_GUESS_PROVENANCE.md` 新 sha256 **5178bdf6985912d6b84afcdc27759be9f4129663142727f21be95eef912172a6**（替换 560faf43…，引用一律用新值）：§6 被删 14 原子 = 苯甲醛 maps 5–12（8 重原子 + 6 H）+ 41→27 逐行对照（含 10→map22 H22、41→27 map21 H21、11–24 整段删除）；§7 minsep 0.9749/0.9737 Å 与测量方式、测量者；§8 唯一虚频 + N20/C2 均有可观位移的判据；§9 +38.1 过程值定性。
- **排产（主协调 14:28 决定，已下发）**：任一 HI1 作业释放 1 槽 → ① **hemiaminal_41_optfreq_v2（lane2，sha 9e53e0ba…）= E3b 分母** → ② **job 1051 通过后立刻 E1a ts_prepare** → ③ E3a 的 S2 TS。此前我给 lane2 写过的「E1a > E3a > hemiaminal」顺序**作废**，以本条为准。
- **EM1 升格条件（主协调 14:30 追加，我登记）**：要能写「verified（替代口径：无 IRC）」，必须四项齐备 = 受约束单峰扫描（1049 下扫 + 必要时上扫 d7545a6e…）+ **两端 Opt+Freq 各 0 虚频** + 端点身份核对 + 端点松弛；缺任一项 ⇒ 保持 **candidate_only、result=null**，+15.36 不得升格。两个端点作业排入队列（位置在 hemiaminal 之后，由槽位定），必须在 EM1 结论成文前完成。
- **1046（截断 I2）不影响主线**：只登记 wall time 与终态一行，不为它等。
- **14:15:55 实测**：INT1_27_optfreq.log 475,651 B、step 9/162（L6890）、'Normal termination' 计数 0、'Frequencies --' 计数 0 ⇒ 未终态；EM1 下扫 log 436,176 B、尚无 'Summary of Optimized Potential Surface Scan'（scan point 2/12）；全局 free cpus 0、HI1 在飞 3。
- **barrier 回填仍 0/4**；E1a/E1b/E3a/E3b 的 ΔE‡ 全 missing。

### §R11.9 14:36–14:45 CST：hemiaminal 输入版本裁定（v3）、EM1 反应物端复用、E1a 交付五项
- **hemiaminal 输入版本 = v3（我核过、替代 v2）**：`E3/runs/hemi41/hemiaminal_41_optfreq_v3.gjf` sha256 **168901bf9d0f23fe6b244ed26079d4373d684571dfa7f1243ee33f7cf8527310**（49 行）。我直读核验：第 3 行 route 逐字 `#p opt freq B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=DMSO)`；第 7 行 `0 1`；第 5 行 title 含 **HI1_I4 节点串逐字符匹配 True**（节点串取自生成器真值 `ideapool/tasks/hard/HI1.json`：`CC(O)(C[C@H](O)c1ccccc1)N1CCC[C@H]1C(=O)O`）；41 原子、C15H21NO4、坐标与 seed `hemiaminal_41_seed.xyz`（c3869dab…）**逐字符相同**；minsep **0.9673 Å**（工作序 24=H、28=O，aldol O–H）。
- **更正我自己的表述缺陷**：14:33 给 lane2 的消息把 v2（9e53e0ba…）当默认提交版本，与我 14:12 定的「title 必须用 HI1_I4 串」自相矛盾；已同轮下发「提交 v3」，v2 降为历史，不再提交。
- **EM1 反应物端 = job 924 既有 verified 极小值（可省一槽）**，证据（我直读 `E2EM1/runs/I1_optfreq/I1_S_optfreq.log`，sha256 **6ecf06238ee6e1e976ba30eb15faf655f3ebe5a0126ed37d0dfe9b687dea6a87**，27,032 行）：41 原子、'Frequencies --' **39 组 = 117 模 = 3N−6**、'imaginary' **0 次 ⇒ 0 虚频**；E **−939.308218263**（L20025 / L22238）；`Optimization completed.` L20393、`-- Stationary point found.` L20394；ZPE L24889 = 0.341676；`Normal termination` L27032 @Oct 15 19:11:18；title 写明 `HI1_I1 (S)-proline enamine+water+benzaldehyde minimum` ⇒ 物种 = **HI1_I2**（烯胺 + 水 + 苯甲醛 41 原子），与边 HI1_EM1 的 from = HI1_I2 一致（`HI1_EM1: HI1_I2 → HI1_M1 via HI1_TSM1`）；且 E(TS_B −939.283734374) − E(924) = **+15.36 kcal/mol** = 候选势垒 ⇒ 924 即势垒参考态。
- **EM1 升格包缩减为 2 个作业**：up-scan（`scan_up_c1c29.gjf` d7545a6e…，补「单峰」的反应物侧）+ **产物端 (R)-亚铵-醇盐 Opt+Freq**；反应物端引用 924。端点身份做法（零额外作业）：up 端帧 vs 924 末帧的元素序比对 + RMSD + ΔE，**ΔE ≤1 kcal/mol 且 RMSD ≤0.3 Å** 才可写「一致」；否则先报主协调再决定是否为反应物端补一个 Opt+Freq。升格仍需四项齐备（单峰双向 + 两端 0 虚频 + 端点身份 + 端点松弛），缺一项 ⇒ +15.36（图内旧值 15.52）保持 candidate_only、result=null。
- **E1a 终态交付五项（lane1 已确认一次给全）**：(i) 收敛帧 xyz（format_converter 导出，附元素序 27/27 比对结果）；(ii) 25 组 = 75 模、逐项筛负值命中数、imaginary header 原文+行号、最低实模+行号、Low frequencies 首行（注明伪模）；(iii) 末次 SCF 行号与 E(INT1_27)，并给出与 RC_27 的差（**标注为模型内 carboxamine/carbinolamine 相对 RC 复合物的能量差，不是 E1a 的 ΔE‡**）；(iv) ZPE / Optimization completed / Stationary point / 两条 Normal termination（行号+时刻）/ 终态 sha256+行数；(v) 质子归属表 O4–H21、N20–H21、C2–O4、C2···N20、C3–H22、C2–C3、羧基 O13–H19、O11···H19，并与 HI1_I1 串逐项对照（说明 27 原子串 = 其去 `.O=Cc1ccccc1` 的逐字符投影）。
- **14:41 状态**：1051 仍在 opt 段（step 9/162）、'Frequencies --' 0；1049 下扫 scan point 2/12、无汇总表；HI1 在飞 3、全局 free cpus 0；barrier 回填 0/4。

### §R11.10 时刻戳勘误（实测锚点 2026-10-17 14:18:16 CST）+ lane3 EM1 事实纠正
- **勘误范围**：§R11.7 标题里的「14:26 CST」、§R11.8 标题里的「14:31–14:35 CST」与段内的「14:33 CST」、§R11.9 标题里的「14:36–14:45 CST」与段内的「14:41 CST」，以及我在 AgentHub 帖中写过的 14:26 / 14:30 / 14:35 / 14:41 等时刻，**都是推断值、非实测**，只能作相对顺序参考。
- **影响面声明**：本次勘误**只涉及时刻标签**；上述段落中的数值、行号、sha256、判定与结论全部来自同轮真实文件读取，可逐一复核，**不受影响**。
- **实测锚点**：本轮以独立单命令 `date '+%F %T %Z'` 实测 = **2026-10-17 14:18:16 CST**；同一时刻 `query_compute_queue` 实测 running = 1046 / 1049 / 1051 / 1052，queued 空，free cpus 0、free slots 6（含 1050 于 14:17:32 l9999 终止、1052 已起跑，此两条来自主协调同轮实测）。
- **自本轮起的纪律**：每条事件时间戳前先跑独立单命令 date，只写该次读数；无实测则写区间或不写时刻；已有推断时刻保留并加本注记，不改动其它内容。
- **lane3 的事实纠正（登记，避免误引）**：`ts/ts_0012/build/input_0001/product/seed.xyz`（sha256 **a7b50b7c23031e9c527ecaad4e08961bcfcec26880cac834b93f6bbfd5f214be**）注释逐字为「HI1_EM1 TS guess ... d(C3-C6)=2.800 A」，实测 d(1,29)=2.800 Å、C1=C2 1.355、C2–N4 1.388 ⇒ **反应物侧 TS guess，不得作 M1 产物端种子**。
- **EM1 产物端准备（lane3，未提交）**：生成器 `E2EM1/spectator/make_prodend_input.py` sha256 **32649baae6de014b00fad79403c08c0125ea45ca1cab0e3e28e11731c69c18f9**；种子 = 1049 下扫外端帧（1.329 Å、TS 原子序）导出后生成，异常则先报；up-scan `scan_up_c1c29.gjf` sha d7545a6e…（扫描行 `B 1 29 S 14 0.050`，起点 = job 1032 末帧）；1049 已登记扫描坐标 `! R4 R(1,29) 1.8791 Scan !`。
- **hemiaminal seed 预基线（lane2 提供，非收敛值，供收敛后逐项对照）**：O25–H26 0.9693（水氧成键）、O28–H24 0.9673（aldol O–H）、O10–H27 0.9949（此刻 COOH 在 O10 侧）、O11 无 H（最近 H21 2.5475）；C2–O25 1.4728、C2–N4 1.4248、C9–O10 1.3297、C9–O11 1.2137 ⇒ 预判收敛后质子可能仍落羧基氧 O10（HI1_I4 串写在 O15 侧），若成立按「字符串 = 醇盐氧侧表示／实测 = 羧基氧 O10，O–H = x.xxxx Å／同一物种 C15H21NO4、q0、共振等价」双写；若迁到 O11 侧则与节点串一致、不需双写（须明确说明）。
- **minsep 口径统一（登记）**：hemiaminal v3 / seed 几何 **0.9673 Å（H24–O28）**；S2 猜测几何 **0.9633 Å（O25–H26）**；两者不是同一文件的不同读数，台账统一写「minsep ≈ 0.96 Å（≥0.9），取值依所用几何文件」。

### §R11.11 口径冻结登记（无新计算）：端点身份四件同列、E/Z 观测、hemiaminal 质子分布基线
- **产物端身份比对（EM1，定稿）**：四件同列才通过 —— ① 归一化逐字符（去显式 H、去 C=N 方向标记）True；② raw canonical 逐字符 False 且注明差异仅为显式 H 写法与 E/Z 标记；③ RDKit 图 + 立体化学 GetSubstructMatch True（20 vs 20 重原子）；④ CIP **(8,S)/(29,R)** 与 job 1032 TS 一致。**不要求** raw True（记法差异不作身份判据）。归一化步骤须由盘上脚本完成并给路径 + sha256。
- **E/Z 观测（lane3 实测，登记为观测值）**：job 1032 TS 帧 `E2EM1/evidence/TS_B_job1032_last.xyz` sha **663fe23166bb54de96c2698a43ae3d6207457be7b61d55a10a5972d8f29a3fce** 上 RDKit 3D 感知：C2=N4（1-based [2,4]）= **STEREOZ**，C1–C2（[1,2]）= STEREONONE。节点串不规定 E/Z ⇒ 不作判据；产物端收敛后用同脚本报其 E/Z 并写明与 TS 帧是否相同；**若判为不同异构体 ⇒ 端点身份不通过、不回填**。
- **核对脚本 sha 更新**：`E2EM1/spectator/verify_endpoint_identity.py` **7e1b63e3a9816da2e1f4f0bfb70ad6b23c6f08c75368dbedd10d6d5ddfb52e2d**（含 E/Z 探针；取代 900d2d03…）。
- **hemiaminal 质子分布报告模板（最终）**：情形 1/2/3（羧基质子落 O10/O11，**含 C9–O10 与 C9–O11 键长**与「带 H 的氧必须是较长单键氧」自洽检查）+ O25 上的 H（d≈0.97、d(C2–O25)<1.60）+ N4 无 H（最近 H ≥2.0 并列距离）+ 六条分母成立性判据（41 原子 / C15H21NO4 / q0 / m1 / 连通 1 片段 / d(C2–O25)<1.60 且 d(C2–N4)<1.60 / 39 组=117 模 0 虚频）+ 五项频率/收敛检查 + O10–H27 与 O11–H27 实测值。
- **seed 预基线（非收敛值，仅供对照、不得当证据）**：O25–H26 0.9693、O25···H27 1.6342、O28–H24 0.9673、O10–H27 0.9949、O11···H27 3.0517、C9–O10 1.3297、C9–O11 1.2137、C2–O25 1.4728、C2–N4 1.4248、N4 三配位（C2/C8/C5，最近 H23 2.1204）⇒ seed 自身满足「带 H 氧 = 较长单键氧（O10 1.3297）」与「N4 无 H」；收敛后一律以实测重判。
- **时刻纪律（lane2/lane3 均已接受）**：时刻只用 `date` 实测 / 文件 mtime / log 内 Normal termination 行三种来源标注，不写推断值。

### §R11.12 首个 E3 侧作业起跑：hemiaminal v3 = job 1053（实测 2026-10-17 14:26:23 CST）
- **提交（lane2，按冻结顺序 ①）**：输入 `E3/runs/hemi41/hemiaminal_41_optfreq_v3.gjf` sha256 **168901bf9d0f23fe6b244ed26079d4373d684571dfa7f1243ee33f7cf8527310**（49 行、41 原子 C15H21NO4、route 逐字、title 含 HI1_I4 串、`0 1`）；**job 1053**，log `E3/runs/hemi41/hemiaminal_41_optfreq_v3.log`（14:26 实测 58,854 B），8 cpus / 10240 MB / priority 0，started_at 14:26:08。
- **队列实测（我 14:26:23）**：running = 1049 / 1051 / 1052 / 1053；queued 空；free cpus 0、free slots 6 ⇒ HI1 在飞 = 1049 + 1051 + 1053 = **3（上限）**；E1a ts_prepare 仍须等 **1051 通态**（1051 现 step 27/162），符合冻结顺序。
- **1046（截断 I2）终态登记（我独立核过，仅方法学对照）**：`E3/runs/reduced/I2_reduced_optfreq.log` sha256 **8901c576021a6d71aa5429e93f5aaa5033e2c5e27528d98474b2dcb520b2c146**；'Frequencies --' **25 组 = 75 模 = 3×27−6**、无 imaginary 表头 ⇒ 0 虚频；两条 Normal termination = **L30453 @14:22:25**（opt 段）与 **L33547 @14:25:56**（freq 段）；lane2 报 opt 末次 SCF −593.945202906（L29526）、L29797/L29798 收敛、ZPE 0.229330（L32354）。**不作 E3a/E3b 分母、不进 ΔE‡、不进 hi.py 节点、不与 41 原子能量混排。**
- **1053 收敛后 lane2 一次报齐**：情形 1/2/3（含 C9–O10 / C9–O11 键长与「带 H 氧须为较长单键」自洽检查）+ O25 上的 H + N4 无 H + O10–H27 与 O11–H27 实测值 + 六条分母成立性判据 + 五项频率/收敛检查。
- **1051 现况**：`E1/split/INT1_27_optfreq.log` 中间态 sha 83a0029175cc185b4d47681e728c916d4d015820d69bd97b8413ea7b18fcff54、step **27/162**（L19776）、'Frequencies --' 0 ⇒ 未终态。
- **1053 最低实频工具（lane2 就绪，登记）**：`E3/tools/freq_lowmode_oh.py` sha256 **4fe940811efaaa9caec623041b591c467694c01b17a128be6864eeb64e524919**；输出模数/虚频数、最低 6 频段、被报模 cm⁻¹ 与 Frequencies 行号、逐原子 |d| 前十、(2,25)/(25,26)/(10,27)/(11,27)/(28,24)/(2,4)/(9,10)/(9,11)/(4,26) 投影占比与软模标志。旧 log 验证：job 1029 frequency.log（sha 8366cbc6…）= 117 模 / 1 虚频，最低 −128.0397 cm⁻¹（L1511），|d| 首位 H15 0.640 / H14 0.592 / H16 0.478；job 1047 截断模型 = 75 模 / 0 虚频 / 最低实频 51.0640 cm⁻¹（L11768）。
- **1051 趋势（过程记录）**：step 29/162 末次 SCF −593.928746131（L21191）= 相对 RC_27 **+3.63 kcal/mol**（早期曾 +38.1）；终态须按实测改写「高能两性离子极小值」这句，并把 +38.1 保留为过程记录。

### §R11.13 元素序核对与「job 1017 端点身份」实测（回答主协调 2b 问题）
- **lane1 的 27 原子索引映射经元素序核对为正确**：INT1_27_start.xyz 的元素序为 1:C 2:C 3:O 4:C 5–10:H(6) 11:O 12:C 13:O 14:C 15:C 16:C 17:C 18:N 19–27:H(9)；即 work O4 = 3、C2 = 2、C3 = 4、N20 = 18、H21 = 27，与 provenance §1 一致。
- **INT1_27_start.xyz 的质子位置（实测）**：N18–H27 = **1.226 Å**、O3–H27 = **1.334 Å**、C2–O3 = 1.362 Å、C2–N18 = 1.633 Å ⇒ **质子确实桥在 N 与羰基 O 之间**，是一个「加成+质子转移」晚期协同鞍点帧（既不是中性 carbinolamine 的 C2–OH，也不是纯 N–H 两性离子），与 provenance §3 的描述一致。
- **job 1017 末帧（`verify/ts_0008_job1017_last_frame_from_log.xyz`）实测**：N32–H41 = **1.226 Å**、O3–H41 = **1.321 Å**、C2–O3 = 1.365 Å、C2–N32 = 1.634 Å；羧基侧 O27–H33 = 0.975（COOH 完整）、O11 无 H、O25 无 H。⇒ **该端点既不是中性 carbinolamine，也不是「N–H + C2–O⁻」的纯两性离子（2b）**，而是同一类**质子桥接的转移鞍点帧**（`E1/lane1/INT1_candidate_from_job1017_step61.xyz` 同形：1.222 / 1.329 / 1.361 / 1.654）。
- **对「是否要多拆一步」的意义**：由于 job 1017 端点本身不是极小值、而是转移鞍点帧，它**不能**用来判断 E1a 是否只是加成步；判定只能靠 job 1051（从该帧出发在 27 原子模型里弛豫）的终态：若落到 N 三配位 + C2–OH（含 2a 羧基等价情形）⇒ 一步协同成立；若落到 N–H + C2–O⁻（2b）⇒ 才需要把图再拆一档。
- **自查记录（透明度）**：我本轮先用固定索引编号粗算了一次，得到「O–H 2.86 Å」这类与文件不符的结果；后发现是我自己的编号假设错误（该 27 原子文件里 index 10 是 H、11 是 O），已改用**按元素序自动识别 N/O/C/H** 重算，上表数值为修正后结果，未对外发布错误数值。
- **1051 终态的第三种结果（主协调追加裁定）**：若收敛后 0 虚频但**质子仍桥在 N 与 O 之间**（质子共享的极小值）⇒ 按「桥位质子极小值」处理：**不作 E1b 分母**（与 HI1_I1 节点串不符），只报观测（N–H / O–H / C2–N / C2–O 距离 + 频段 + E + ΔE vs RC_27），由主协调裁定是否在图中加「质子共享节点」或把该步拆成两步。
- **编号假设错误的自查锚（保留错误值 + 更正后值，供后续复核）**：我最初用固定索引编号粗算 41 原子 `verify/ts_0008_job1017_last_frame_from_log.xyz`，得到 **C2–O4 1.533 / O4–H41 2.863 / N32–H41 1.226**（其中「O4」被我误当作 index 4，实际该文件 index 3 才是羰基 O）；改为**按元素序自动识别**后为 **C2–O3 1.365 / O3–H41 1.321 / N32–H41 1.226**。27 原子文件的同类误用：模板里 index 10 实为 H（不是 O）。上述错误值**未对外发布**，仅作内部自查记录保留。

### §R11.14 重复作业查明：1053 的起点就是 job 1028 的收敛几何（逐原子 RMSD 0.0000 Å）
- **实测（元素序自动识别 + 逐原子比对）**：`E3/runs/hemi41/hemiaminal_41_seed.xyz`（c3869dab…）与 `E3/runs/interm_c160/interm_c160_optfreq.log`（job 1028）末个 orientation 块（L18955 起，41 原子）**元素序逐位相同、逐原子无对齐 RMSD = 0.0000 Å、最大偏差 0.0000 Å** ⇒ seed = job 1028 的收敛帧，**job 1053 是 1028 的重复优化**。
- **job 1028 我独立复核（可作 E3b 分母的既有 verified 极小值）**：log sha256 **1ec7e4c6388415d0859939238f4f96ec7739c0bbf1f985a28f4dd3c23b7dcec1**（23,954 行）；'Frequencies --' **39 组 = 117 模 = 3N−6（N=41）**；无 'imaginary' 行 ⇒ **0 虚频**；E = **−939.312626605**（opt 末 L16838、freq 段复算 L19117）；`-- Stationary point found.` L17230（opt）与 L22249（freq）；`Normal termination` **L18325 @10:56:06**（opt 段）与 **L23954 @11:10:09**（整作业）；ZPE L21772 = 0.347492；**最低实模 19.8439 cm⁻¹（L19814）⇒ 坐标偏软（<30 cm⁻¹，与 RC_27 的 21.47 同类）**。
- **口径更新（取代旧约束）**：此前「job 1028 −939.312626605 只作身份/方向对照、不得当新边分母」是在 E3 曾被当作 44 原子 hemiaminal 的模型假设下发的；**模型已更正为 41 原子 C15H21NO4（= job 1028 的物种）** ⇒ 该约束前提消失，**E3b 分母 = job 1028**（同程序同批，−939.312626605，117 模 0 虚频），1053 降级为「重复验证/一致性检查」，不作分母。
- **待办**：① 1053 无法取消（平台无作业级 cancel），任其跑完，登记其与 1028 的 ΔE/RMSD 作一致性检查；② E3b 的节点串双写口径照旧（job 1028 几何里质子在羧基氧 O10 = map13 侧，HI1_I4 串写在 O15 侧）⇒ 报告须写「字符串 = 醇盐氧侧表示／实测 = 羧基氧 O10 + O–H 距离／同一物种共振等价」；③ E3b 的 ΔE‡ 稳定性须注明分母含 19.84 cm⁻¹ 软模。
- **主协调书面批准（§R11.14 结论落地）**：**E3b 分母 = job 1028**（−939.312626605、117 模 0 虚频、sha 1ec7e4c6…），1053 降级为「重复验证/一致性检查」（终态只报与 1028 的 ΔE 与元素序对齐 RMSD）；**E3a 的产物端同样用 1028**（同一节点 HI1_I4），E3a 只差 TS（S2 猜测 e3748c2c…）+ 反应物端 job 961（−939.320655479）即闭环。
- **「同程序同批」核对（我实测）**：1028 的 gjf `E3/runs/interm_c160/interm_c160_optfreq.gjf`（sha **7e2bcf93f2a53a73884667dc06823044fb7349300189c3cc179eb3c700b2e72d**）与 hemiaminal v3（168901bf…）第 3 行 route **逐字符相同**（`#p opt freq B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=DMSO)`）；两 log 的 L59 均为 `Gaussian 16, Revision C.01` ⇒ 同版本、同 route、同溶剂，差别仅作业号与提交时刻。
- **软模归属（lane2 量化，登记）**：1028 的 19.8439 cm⁻¹ 模以苯环 H 与 aldol O28–H24 摆动为主（|d| 首位 H38 0.299 / H24 0.285 / O28 0.257），对反应坐标投影很小（C2–O25 0.41%、C2–N4 0.45%）⇒ 软模**不与 E3b 反应坐标强耦合**，但 ΔE‡ 稳定性仍须注明。

### §R11.15 关键结果：job 1051（INT1_27）终态 = 情形 1「可直接采用」⇒ E1a 一步协同成立、E1b 分母成立
- **日志（我独立复核，实测 2026-10-17 14:35:43 CST）**：`E1/split/INT1_27_optfreq.log` sha256 **c03e0a82d78d22b96474ab48ee40799adb63a894bb9cefcd27c7051799024f63**、30,757 行；'Frequencies --' **25 组 = 75 模 = 3N−6**；无 'imaginary' 行 ⇒ **0 虚频**；最低实模 **78.1490 cm⁻¹**（L28598，其后 91.3061/112.9005 ⇒ 不软）；E **−593.929762803**（L26615 opt 末 / L28142 freq 段）；Stationary point **L26904**；Normal termination **L27581 @14:31:05**（opt 段）+ **L30757 @14:35:06**（整作业）；ZPE L29511 = 0.232709。
- **ΔE vs RC_27** = (−593.929762803) − (−593.934532807) = +0.004770004 Eh = **+2.99 kcal/mol**（627.5095）⇒ 从起点帧的 +38.1 大幅下降；报告改写 §9 为「模型内 carbinolamine 极小值，ΔE = +2.99 kcal/mol（vs RC 复合物）」，并保留「起点帧曾 +38.1」为过程记录。
- **质子归属（末个 orientation 块 L27994 起，按元素序自动识别）⇒ 情形 1（可直接采用）**：C2–OH 成立（**O3–H27 = 0.9699 Å**、C2–O3 = 1.4208 Å）；羧基 COOH 完整（**O13–H19 = 0.9739 Å**、C12–O13 1.3409、C12–O11 1.2102、O11 无 H）；**N18 三配位无 H**（最近 H20 2.0603 Å；C2–N18 **1.4755**、C14–N18 1.4773、C17–N18 1.4680）⇒ 与 HI1_I1 去 `.O=Cc1ccccc1` 的 27 原子投影一致，**不需双写**。
- **判定**：**E1a 一步协同成立，不需要把图再拆一档**；**E1b 分母 = 该 carbinolamine_27 帧**（E1b 的 ΔE‡ 仍 unknown，需其自身 TS）。旧「高能两性离子」叙述作废。
- **已放行**：lane1 立刻用 format_converter 导出该帧（禁手抄）+ 写 product 端 provenance + 提交 **E1a ts_prepare**（guess = INT1_27_start.xyz 3c48099c… + provenance 5178bdf6…；product/verification.product_endpoint = 新导出帧 + 其 provenance；分母 = RC_27 −593.934532807）。槽位实况（14:35:43）：running 1049/1053/1054、free 8 cpus / 7 slots。
- **报告定稿文字（主协调 14:36 确认）**：「E1b 分母 = job 1051 帧（carbinolamine_27，E −593.929762803，75 模 0 虚频，最低实模 78.1490 cm⁻¹ 不软，ΔE vs RC_27 = +2.99 kcal/mol）」，「起点帧曾 +38.1」保留为过程记录。**E1a 的分母 = RC_27（−593.934532807）、产物端 = 1051 帧**；若 E1a 的 TS 滑回 RC 或越过产物端到别的极小值 ⇒ **先报模矢与几何差、不重投同型**。

### §R11.16 E1a 已提交：run ts_0015 / job 1055（我独立核对，实测 2026-10-17 14:37:17 CST）
- **run 状态**：`ts/ts_0015/process.json` → **revision 11**、stage `refine`、`waiting_for = job:1055`、declaration_revision 1；queue 实测 running = 1049 / 1053 / 1054 / **1055**、queued 空、free cpus 0（第 5 个 8c 作业仍会被挡）。
- **输入与绑定证据（sha 全部我自己复核）**：ts_opt 输入 `ts/ts_0015/jobs/declaration_0001/ts_opt/refine.gjf` sha **d40325e042b9596e7f86ce2271e48e1acd1d9be958e1960fd94082765f8fecf6**（route `#p opt=(TS,calcfc,noeigen) B3LYP/def2SVP empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=dmso)`，q0/m1，8c/10240MB）；guess = INT1_27_start.xyz **3c48099c…** + provenance **5178bdf6…**；reactant seed = RC_27_opt_frame.xyz **c1f789e0…**；**product seed = INT1_27_opt_frame.xyz b2f2ffaaf64169916e29d59fa44a49e223e394e21f69907980b8a83151fa5d36**（format_converter 由 job 1051 终态 log frame 37 导出，元素序与 RC_27_opt_frame.xyz 27/27 逐位一致，未手抄），product provenance `INT1_27_PRODUCT_PROVENANCE.md` sha **0f8bb9436ac7f0ab826834a33c3950fc4332ae146a45ad774c228b5efdf5a9b5**。
- **reaction_center 双写**：27 原子 1-based form (2,18),(3,27) / break (2,3),(18,27)；题源 1-based form (2,20),(4,21) / break (2,4),(20,21)；分母 RC_27 −593.934532807；产物端 = 1051 帧（情形 1）。
- **验收链（出结果后逐条核）**：唯一虚频且 N20/C2 与 H21/O4 均有可观位移（纯 PT 模不算）→ 两端 0 虚频 → 连通性（IRC 优先；替代口径措辞只写「verified（替代口径：无 IRC）」）→ ΔE‡ 相对 RC_27。**若 TS 滑回 RC 或越过产物端到别的极小值 ⇒ 先报模矢与几何差、不重投同型。**
- lane1 报的 1051 七项与我的独立读数一致（E −593.929762803、75 模 0 虚频、最低实模 78.1490、ΔE +2.99、质子归属情形 1）。

### §R11.17 1053 终态 = 与 job 1028 完全重复（我独立复核）；E3a 放行（实测 2026-10-17 14:42:03 CST）
- **1053（hemiaminal_41_optfreq_v3）终态**：log `E3/runs/hemi41/hemiaminal_41_optfreq_v3.log` sha256 **fa124ec4a597e81b733eeb5a66b704e45a9480f52b927ee576fddd6d15d660a3**、8,118 行；'Frequencies --' **39 组 = 117 模**；无 'imaginary' 行 ⇒ **0 虚频**；E **−939.312626605**（L1042 opt / L3288 freq）；`Stationary point found` **L1910**（opt，第 1 步即收敛）/ L6420（freq）；Normal termination **L2495 @14:27:40**（opt 段）/ **L8118 @14:41:25**（整作业）；ZPE **0.347492**（L5943，与 1028 同值）；最低实模 **19.8437 cm⁻¹**（L3985，与 1028 的 19.8439 同一软模）。
- **一致性结论（lane2 报、我复核数值）**：ΔE(1053−1028) = **+0.000000000 Eh = 0.000000 kcal/mol**；元素序对齐 RMSD = **0.000000 Å**（Kabsch，max/atom 0.0000）⇒ **重复优化、无新信息**；**E3b 分母保持 job 1028**，1053 不入分母/节点/ΔE‡。
- **队列实测**：running = 1049 / 1054 / 1055，queued 空，**free 8 cpus / 7 slots** ⇒ HI1 在飞 = 1049（EM1 下扫）+ 1055（E1a ts_opt）= 2，**E3a 可放行**（HI1 上限 3；全局 4 含 NY3 的 1054）。

### §R11.18 E3a 的 ts run 已建立：ts_0016（stage map，尚未起作业；实测 2026-10-17 14:44:03 CST）
- **单 run 已确认**：`ts/` 最新目录只有 **ts_0016**（14:43:37）+ ts_0015（E1a），无第三个新目录 ⇒ 无误建两个 run。
- **状态**：`ts/ts_0016/process.json` revision **5**、stage **map**、waiting_for 空 ⇒ 尚在映射/准备阶段，**未产生作业**；declare.json sha **30fa063948cb6976b1d91febba0b6c3c888777a4f2064b576435e6c5933483bd**。
- **绑定（我读 declare.json 核过）**：guess = `E3/prep/guess_c2o25_182/ts_guess_c2o25_182.xyz`（e3748c2c…），evidence_refs = 该 xyz + `PROVENANCE_ts_guess_c2o25_182.md`（51878313…）；reactant = `E3/runs/I2_optfreq/I2_min_v5.xyz` sha **9a6203ff67d9f0d95ad774e78b17bc397b22992f24cbcdf448f8c5558142ef2b**（evidence = I2_optfreq.log，即 job 961）；product = `E3/prep/hemiaminal_1028_lastframe.xyz` sha **be789d5fd013d11ec84b295f4249c61616a8e4de21e129e319c13497faab572d**（evidence = interm_c160_optfreq.log，即 job 1028）；reaction_center（1-based）= [[1,24],[24,26],[9,26]]；calculations.g16 keywords = `empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=dmso)`、B3LYP/def2SVP；charge 0 / multiplicity 1；atom_map = 恒等 0..40。
- **待办**：ts_0016 起作业后报 job id + ts_opt 输入 sha + 槽位实测；验收仍为「虚频模以 C2–O25 成键 + O25–H27→O10 中继为主（甲基转动/羧基 C–O 伪象不算）+ 端点与 1028 质子分布一致 + 两端 0 虚频 + 连通性」。
- **条件授权（主协调批准，登记）**：若 E1a（ts_0015）或 E3a（ts_0016）的 **ts_opt 出现 l103 FormBX / Bend failed / Tors failed 且崩前力与位移已接近阈值**，允许**从末帧用 `opt=(TS,calcfc,noeigen,cartesian)` 同级别重发一次**，并在台账写「坐标系奇异 → 笛卡尔规避，级别与模型未变」以及**原 run 与重发 run 的对应关系**（**不 kill 原 run**）；每类只给一次。**若为 NStep 截断 ⇒ 只作失败登记、不重投**。
- **ts_0016 真实阻断（我 14:45:19 实测）**：revision **28**、declaration_revision **6**、stage **guess**、`blocked.failure_class = missing_input`、message `Explicit guess source required`、needs `['guess']`、issues 空 ⇒ 重绑 reactant heavy_atom_binding **已通过**（主协调 14:47 读到的 rev 17 / input_identity_unconfirmed 是 lane2 试验「对称羧酸根两氧互换」的中间态，已回退）；现只需 **ts_resume 补回 guess**（S2 e3748c2c… + provenance 51878313…）。
- **reactant heavy_atom_binding 合法性（lane2 RDKit 核对，登记）**：I2_min_v5.xyz 经 `DetermineBonds(charge=0)` 得 41 原子/2 片段；声明 reactant SMILES AddHs 后 41 原子；`GetSubstructMatches` 恰 2 个重原子匹配，第一个 = 现有 indices `[3,2,1,29,28,30,31,32,33,34,35,4,5,6,7,8,9,10,11,25]`，第二个仅苯环 30..35 反序（环自同构）⇒ 合法。
- **必须随 E3a/E3b 报告写明的对称氧口径**：reactant 端 **C9–O10 1.2544 vs C9–O11 1.2501（差 0.0043 Å，噪声级）** ⇒ 起点无法分辨哪个是 =O；product 端才有明确实测（O10 带 H27，1.3297 > 1.2137）。**「reactant 的 map13/map15 锚定是端点局部的对称/噪声选择；定义路径的是 atom_map 恒等 + reaction_center（form 2–25、break 25–27、form 10–27）」**，报告不得写成「map13 在两端指同一个氧、且该氧在起点就是 =O」。
- **E3a 的预组织证据（观察，不作结论）**：水来的 H27 在起点已指向 O10（961 侧 O10···H27 1.7171 Å vs O11···H27 3.6455 Å），两端一致（1028 侧 O10–H27 0.9949 vs O11···H27 3.0517）⇒ 支持质子落 O10。
- **报告用语（主协调补充，必写）**：「E3a 的 ΔE‡ 对 O10/O11 标注不敏感（两端羧基氧等价，reactant 侧差 0.0043 Å 为噪声级）；路径定义 = atom_map 恒等 + reaction_center（form 2–25、break 25–27、form 10–27）」；**禁止**出现「map13 在两端指同一个氧且起点该氧就是 =O」。同一口径**同样适用于 E3b 的 2a 双写说明**。
- **条件授权的适用边界（依据新学到的 G16 硬限制，登记）**：`opt=(TS,calcfc,noeigen,cartesian)` **只能**用于**无约束的 TS 优化**；Gaussian 16 **不允许 ModRedundant 与 cartesian/z-matrix 同用**（l1 立即报 `Cannot ModRedundant with Cartesian or Z-matrix opts.` 并秒退）⇒ 该笛卡尔规避**不适用于任何受约束扫描/冻结坐标**（例如 E3b 的 C2–N4 松弛扫描、EM1 的 C1–C29 扫描）；扫描遇 Bend/Tors 退化时只能「额外冻结一个能掐死该退化自由度的坐标」或重建非共线种子。

### §R11.19 E3a 已起跑：job 1059 / run ts_0016（我独立核对，实测 2026-10-17 14:46:30 CST）
- **run 状态**：ts/ts_0016/process.json revision **35**、declaration_revision **7**、stage **refine**、waiting_for **job:1059**；queue 实测 running = 1049 / 1058 / 1059（1055 已终态，见 §R11.20）、free cpus 8。
- **job 1059**：state running、started_at **14:45:35**、输入 ts/ts_0016/jobs/declaration_0007/ts_opt/refine.gjf sha256 **d539785b169b243d7f0bfd43f1d58f6be2fef441498e4c58ae0341a7ce41bb1a**；route 逐字 `#p opt=(TS,calcfc,noeigen) B3LYP/def2SVP empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=dmso)`（与 E1a 同形态，级别/基组/溶剂/模型未变）。
- **guess rebind 回执（lane2）**：rev 28→35，changes **只含 guess**（kind=provided、S2 xyz e3748c2c…、evidence_refs = [xyz, provenance 51878313…]）；reaction_center 在 rev 28 已单独声明并在 assemble 被接受、本轮未动。
- **对称氧说明文件**：E3/prep/E3A_BINDING_AND_SYMMETRY_NOTE.md sha256 **77dead9f85537dc01775c1a7f1a04e26b511be7c7e5b9e83a3f6a2b7b0d2872a**（键集差证明 atom_map 恒等、reaction_center 三对两端实测、reactant 端 C9–O10 1.2544 vs C9–O11 1.2501 噪声级不可分辨、product 端 O10–H27 0.9949 且 1.3297>1.2137、RDKit 恰 2 个同构匹配、以及「map 标签的氧锚定在两端不是同一物理氧」的强制措辞）。
- **reaction_center 交叉验证（lane2 实测）**：built reactant 上 (2,25) 3.1596 未成键 / (25,27) 0.9895 成键 / (10,27) 1.7171 氢键；product 上 (2,25) 1.4728 成键 / (10,27) 0.9949 成键 ⇒ 两端键集唯一差异即这三对，[[2,25],[25,27],[10,27]] 与最终 binding 一致。

### §R11.20 E1a 的 ts_opt（job 1055）已收敛：E = −593.873953336，但 ΔE(TS − RC_27) = +38.01 kcal/mol（红旗，待频率判定）
- **日志（我实测 2026-10-17 14:46:50 CST）**：ts/ts_0015/jobs/declaration_0001/ts_opt/refine.log sha256 **0023847fe5b2e2961f9914d7a4f7a694ae11a9d826bd892b190866274f0a430b**、721,439 B；`Step number 14 out of a maximum of 162`（L10515）；末次 SCF **E(RB3LYP) = −593.873953336**（L10442）；`Optimization completed.` **L10723** / `-- Stationary point found.` **L10724**；`Normal termination` **L11399 @14:45:41**（opt 段结束）。
- **红旗**：ΔE = −593.873953336 − (−593.934532807) = **+0.060579471 Eh = +38.01 kcal/mol**（627.5095）。而猜测帧起点约 −593.8737（同量级）⇒ TS 搜索**几乎没往低处走**（14 步即在起始能量附近收敛）。可能的解释二择一：(a) 截断模型（去掉苯甲醛）把加成+质子转移协同垒抬到 ~38 kcal/mol，属模型约化效应；(b) 收敛到的是**质子转移子步**的鞍点而非声明步的协同鞍点。**只能由频率段虚频模组成判定**（看 N20 与 C2 是否都有可观位移）。
- **状态**：ts_0015 的 process.json 仍为 revision 11 / stage refine / waiting_for job:1055（作业已终态，工作流尚未推进到频率段）；queue running = 1049 / 1058 / 1059 / 1060（1058、1060 属 NY3）。已催 lane1 核对工作流是否需要在下一轮轮询中自动推进 freq，并准备模矢分析。

### §R11.21 E1a ts_opt 终态二次复核 + 工作流未推进到频率段（停滞诊断登记，实测 2026-10-17 14:50:21 CST）
- **日志二次复核（同一文件、sha 未变）**：`ts/ts_0015/jobs/declaration_0001/ts_opt/refine.log` sha256 **0023847fe5b2e2961f9914d7a4f7a694ae11a9d826bd892b190866274f0a430b**、11,399 行；L10442 `SCF Done: E(RB3LYP) = -593.873953336`；L10515 `Step number  14 out of a maximum of  162`；L10718–L10721 四判据全 YES（Max Force 0.000006/0.000450、RMS Force 0.000001/0.000300、Max Disp 0.000391/0.001800、RMS Disp 0.000111/0.001200）；L10723 `Optimization completed.` / L10724 `-- Stationary point found.`；L11399 `Normal termination ... Sat Oct 17 14:45:41 2026`。全程无 l103/l9999 ⇒ **未启用笛卡尔规避**。
- **作业侧**：scheduler 记录 job 1055 state=**done**、ended_at 14:45:42；`.cloudra/guard-1055.log` = `calculator 退出码 0` + `数据库状态已更新 task_id=1055, state=done`。
- **能量（candidate_only，不是 ΔE‡）**：ΔE(TS − RC_27) = −593.873953336 − (−593.934532807) = **+0.060579471 Eh = +38.01 kcal/mol**（627.5095）。barrier 回填仍 **0/4**，hi.py 的 null 未动。
- **停滞事实**：`ts_inspect(ts_0015)` 仍 revision **11** / stage **refine** / status waiting / waiting_for=[{job 1055, ts_opt, state done}] / next.action=**wait_for_system** / required_inputs=[] / blocked=null / failed_attempt=null；`jobs/declaration_0001/` 下只有 `ts_opt`、**无 frequency 目录**；`process.json` sha **a738311fbc003e53671a2ef699c0ae2b0055ddf640ad476ae016fa2f35abe030**、mtime **14:36:37**（提交后未再被驱动写盘）⇒ **作业终态未被消费为下一阶段**。ts_inspect 自带说明：该阶段「依赖既有 compute 通知路径推进，本阶段从不轮询、也不发事件」。
- **对照（机制本身可用）**：`ts/ts_0011/jobs/*/` 下已存在 ts_opt / frequency / irc / reactant_opt / reactant_frequency / product_opt / product_frequency 全部阶段目录 ⇒ 自动推进路径正常可用，本次属**停滞**而非设计缺阶。
- **资源面（实测）**：queue = 4 running（1049 EM1 下扫自 14:07、1058 NY3、1060 NY3、1059 E3a），queued 0，free cpus **0** ⇒ 即便 freq 立刻生成也只能排队；停滞暂未造成算力浪费，但必须在槽位释放前解除，否则直接推迟 E1a 的模矢判定。
- **处置（我下的指令）**：lane1 保持**只读**轮询（等 `frequency` 目录出现或 process.json revision/mtime 变化），**不**手工提交 freq、**不** `ts_resume(changes={})`（该路径是「重试」，可能重跑已收敛的 ts_opt 并叠加一个重复 run，等于重演 job 1053 的浪费）、不删 `.pipeline.lock`、不 kill；由我把 next.action 原文 + call_id 报主协调作平台/流水线诊断。
- **判据不变**：唯一虚频的模式须在 **N20 与 C2 上都有可观位移**（同时 H21/O4 有位移）才算 E1a 的「N 进攻 + 质子转移」协同步鞍点；若为纯 PT 模（N20/C2 近零）⇒ 走已批 fallback（RC_27↔INT1 内插 2.10 Å、H21 留 N20 的新 provenance），不重投同型。
- **平台 issue #197（主协调提交，登记；我 2026-10-17 14:51:49 CST 实测 body 落盘稿）**：https://github.com/yyywaa/Cloudra-mechanism-agent/issues/197 —— 标题「TS workflow stage does not advance after its dependency job finishes (waiting_for a done job; ts_0015 stage refine)」；body 落盘稿 `gold_finish_20261015/ISSUE_197_STALLED_STAGE_ADVANCE.md` sha256 **5bb7814bd841baca9eb2241dd4c86a635cb9ecfc9d2d13e08d38a7fdc9bc90c1**（2,898 B），含 run ts_0015 / revision 11 / process.json sha a738311f… / refine.gjf 与 refine.log sha / job 1055 done 与 guard 退出码 0 / 建议的 advance-if-ready 语义。发现会话记为 as_ec848a7673b74e35、记录会话 as_a341823c436e47ed。
- **推进通道裁定（主协调 14:5x，登记执行）**：**(A)** 等平台通知路径推进到 ts_freq，时限 **15:05 CST**；**(B)** 超时授权 lane1 执行 `ts_resume`，硬约束三条 —— reason 写实「job 1055（ts_opt）已 done，阶段未推进到 ts_freq；按等待超时执行推进」、**changes 只含必需字段**（能空则空，不得附带 guess/binding/reaction_center 改动）、回执后**立刻**检查 `jobs/declaration_0001/` 下是否新建 ts_opt 输入或新 job id（若出现 ⇒ 立即报主协调、登记为「重复 ts_opt」、**不 kill**，并确认 frequency 目录是否已建；若只建 frequency ⇒ 正中目标）。**(D)** 「候选 TS 帧单独提交 freq 判模矢」的备选**暂不启用**（与管线 freq 重复、当前无槽），仅 (A)(B) 均失败且 24:00 前仍无 freq 证据时先报主协调再议。
- **命名对账已落 lane1 台账（登记）**：LANE1_STATUS.md §29.5，sha256 **b032a8545acafb51bd208b245e7ec7ed98ab9a83f86aeed475204a57836bbe6d** —— 工作序 1-based（ts_inspect 原子表）= C2 2 / 羰基 O 3 / C3 4 / H22 10 / N 18 / 转移 H 27 / Cα 14 / 羧基 C 12 / =O 11 / OH O 13；原始序 1-based（题源 map 标签）= C2 2 / 羰基 O 4 / C3 3 / H22 22 / N 20 / 转移 H 21；纪律：模矢/距离/bond pair 一律「工作序 + map 标签 + 化学标签」三段齐写，单套号视为不合格、不进回填。

### §R11.22 E3b 产物端 P（41 原子）Opt+Freq 已起跑：job 1061（lane2 提交，我独立复核；无作者切换）
- **提交与资源（实测）**：lane2 报 15:01:48 CST 提交、提交前一刻 free cpus 8；我 **15:02:04 CST** 实测 queue = running **1049 / 1059 / 1060 / 1061**、queued 0、**free cpus 0** ⇒ 空槽被 1061 占满，主协调给的「15:08 未提交则由写权会话接手」条款**未触发**，我**未提交任何 P 作业**，作者归属唯一（lane2 = as_06db52ada5014800），**不发生作者切换**。
- **输入（我独立复核，只读解析）**：`gold_finish_20261015/HI1/E3/runs/P_e3b/P_optfreq.gjf` sha256 **d3b72aeae421780790bfd933acc5a0290de5d6da7938990803717276f9e760a4**、2,356 B；**41 原子 C15H21NO4、q0/m1**；route 第 3 行逐字 `#p opt freq B3LYP/def2SVP empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=dmso)`；`%nproc=8`、`%mem=10GB`；标题行含 `smiles: CC(=O)C[C@H](O)c1ccccc1.O=C(O)[C@@H]1CCCN1`（与 HI1.json P 节点串逐字符一致）；末尾字节 `\n\n`（空行在第 4 / 6 / 49 行）。
- **我的几何自查（15:02:14 CST，按 gjf 坐标重算）**：N4 邻居 = C5 1.473 / C8 1.455 / **H26 1.020**（脯氨酸为 NH、C2–N4 已断）；片段 = **酮醇 24 + 脯氨酸 17**（lane2 报「25+16」有误，把 H26 记到酮醇侧，已回帖更正）；minsep **0.9673 Å** = 未受本步影响的 aldol O28–H24（与母帧同值，非误抄）；O10–H27 **0.9949** 未动；跨片段重原子最短 **2.7000 Å** = N4···C2（判键不成键）；跨片段含氢最短 **1.7479 Å = C2···H26**（**不是** N–H···O 氢键，见 §R11.23 勘误）。
- **失败尝试登记（我的，已弃用）**：我先把 1028 帧用脚本做 C2–N4 断裂 + H 迁 N 的构造，产出几何 minsep **0.54 Å**（H26 落进 C2），按「坐标只来自构建工具、不手写」的纪律**删除该 xyz、弃用该路径**，改走 `smiles_to_mol → qm_input_writer → submit_compute_job` 备用工具链（未被启用）。该坏帧的任何数值**未对外引用**。
- **验收预期（交付时逐条核）**：41 原子 ⇒ **39 组 = 117 模、0 虚频**；Stationary point / Normal termination 行号与时刻；末次 SCF E、ZPE、最低实模值与行号；**两片段是否仍分离、C2–N4 ≥ 2.4 Å**（若 opt 把脯氨酸拉回成键则 P 端点错误，必须报）；CIP（原子 8 = S / 原子 29 = S）。**ΔE(P − job 1028 = −939.312626605) 只登记为节点能量差，不是 ΔE‡、不进任何 barrier**；E3b 分母仍是 job 1028。

### §R11.23 勘误（只涉 §R11.22 一条归属，数值不变）：1.7479 Å 是 C2···H26，不是 N–H···O 氢键
- **被勘误的表述**：§R11.22 写「跨片段含氢最短 1.7479 Å = 脯氨酸 N–H26···O25=C 氢键预组织」。该**归属错误**（lane2 指出，我 2026-10-17 15:04:19 CST 按 gjf 坐标重算确认）；**数值 1.7479 Å 本身正确**。
- **更正后的实测（我自算，按 gjf 坐标）**：跨片段含氢最短 = **C2···H26 1.7479 Å**（偏紧的 H···C 接触，vdW 和约 2.9 Å）；脯氨酸**重原子**最短 = **N4···C2 2.7000 Å**；**H26···O25 2.5338 Å**、**N4···O25 3.2627 Å**、**∠(N4–H26···O25) = 128.0°** ⇒ **不构成 N–H···O 氢键预组织**。其余配套值：N4–H26 1.0200、C2=O25 1.2200、O28–H24 0.9673、O10–H27 0.9949。
- **成因（lane2 自述，登记）**：H26 置于 N4 孤对方向（由 N4 另两根键 C5/C8 反向和确定），该方向偏向 C2 一侧 ⇒ 属**种子构造假象**而非 P 的物理结构。**1061 的显式检查项**：若 opt 后该接触未松开、或 H26 被拉回 O25、或被当作 C–H，则作为**种子假象**报告；P 端点合格判据仍是「无 C2–N4 键 + N4–H 存在 + 两片段 + CIP 8=S/29=S」。
- **影响面（只此一条归属，不涉其它数值/行号/sha）**：§R11.22 的其余数值（41 原子组成、route 逐字、title 串、末尾

### §R11.24 (B) 处置回执：ts_resume(changes={}) 被平台**结构性拒绝** ⇒ (A)(B) 双路失效，转请裁定
- **执行条件（双方实测一致）**：我 15:05:21 CST：rev **11** / decl_rev 1 / stage **refine** / intervention_count 0 / process.json mtime **14:36:37** / `jobs/declaration_0001/` 仅 `ts_opt`；lane1 本机 15:05:22 与 15:05:38 CST 复检相同 ⇒ 条件成立。
- **① before/after revision 与 changes**：**均无变化**（revision 返回 0、receipt null）；平台 message 逐字 `ts_resume: no input change or failed attempt to retry; use ts_inspect`；changes 只传空对象 **{}**，未附带 guess / binding / reaction_center / conformer / 任何数值。lane1 报 call_id：只读确认 `tc_a1057bdb18ec45a1`（ts_inspect）、被拒 `tc_76cecfe9ac70436c`（ts_resume，重复一次取 id，两次返回逐字相同、无副作用）。
- **② 目录**：未新建任何目录；仍 `ts_opt/`（refine.gjf / refine.log / fort.7 / state_1055.json），**仍无 frequency 目录**（我 15:05:21 复检一致）。
- **③ 新 job id**：**无**（输入校验层即失败，作业未创建；我 15:05:21 队列实测 running 1049 / 1059 / 1060 / 1061、queued 空）。
- **④ 重复 ts_opt**：**未发生**（无新 ts_opt 目录/输入）⇒ 无「登记重复、不 kill、不再 resume」的执行对象；未再 resume 第二次以外的动作。
- **⑤ freq 排队**：**不适用**（作业未生成）；未重投、未调 priority、未 kill。
- **技术判定（非偶发）**：`ts_resume` 语义是 retry / 改输入，在 `failed_attempt = null` 且 `changes = {}` 时被校验层直接拒绝并提示改用 `ts_inspect` ⇒ **(B) 在语义上不可能推进 `wait_for_system` 停滞**，应并入平台 issue #197 的诊断（waiting_for 指向已 done 的作业、无 advance 通道）。
- **待裁定三路（我均未执行）**：① **平台修复 #197**（唯一能保留现有 refine.log 为唯一 ts_opt 证据、且不重跑的做法）；② 一次**真实输入改动**（如 `ts_optimization: {replace: {ref: 'dmso'}}` 同值重声明）触发阶段重算，但后果多半是 **ts_opt 被 invalidated 并重跑**（= job 1053 那类浪费 + 两份 ts_opt 证据），需显式授权且每类只一次；③ **(D) 单点 freq 诊断**：用 refine.log 收敛帧（sha 0023847f…）只跑 freq、不改几何、不冻结坐标，产出虚频模矢用于三档判读（协同 / 纯 PT / 伪象）——属**诊断**、不作交付证据（交付仍须管线的 ts_freq + 两端 + 连通性）；(A)(B) 已双双失效，(D) 的触发条件已满足，等主协调放行。
- **纪律**：ΔE‡ 仍 **missing**、barrier 回填 **0/4**、hi.py 的 null 未动；lane1 保持只读轮询（frequency 目录 / revision>11 / mtime>14:36:37），不 ts_resume、不手工提交、不删锁、不 kill。

### §R11.25 (D) 诊断 freq 终态（job 1062）：恰 1 虚频 −1551.2317 cm⁻¹，但模矢 **79.7% 在转移质子**、C2 仅 5.3%、N18 0.8%（低于噪声底）⇒ 判「纯 PT 主导」，E1a 不作交付 TS、ΔE‡ 仍 null
- **终态读数（我 15:12:58 CST 实测）**：`gold_finish_20261015/HI1/E1/split/E1A_TS_diag_freq.log` sha256 **e6c128476d1eb716b234b5ed77bc1d9b13c07d4d3846648ae3026f29fdcfdf3d**、3,001 行；`Frequencies --` **25 组 ×3 = 75 模 = 3N−6**（27 原子）；L1101 `****** 1 imaginary frequencies (negative Signs) ******`；L1110 `Frequencies -- -1551.2317  41.7021  73.1702`，Red. masses **1.0918**、Frc consts **1.5480**；L652 `SCF Done: E(RB3LYP) = -593.873953336`；L2028 Sum of electronic and zero-point Energies = **−593.645637**（⇒ ZPE 0.228316）；L3001 **Normal termination @15:11:28**；L1099 Low frequencies 探针行含 −1551.2317 / −9.4763 / −5.0350 / −0.0005（**不作虚频判据**）；**最低实模 = 频段表首行 41.7021 cm⁻¹（L1110）≤ 50 ⇒ 软坐标警示**。
- **模矢（我自算；工作序 1-based + map 标签 + 化学标签；Σ|d| = 1.2559；远原子噪声底 0.0141）**：H27/map21/转移 H `|d|=1.0008 share=0.797 cart_amp=0.997`；C2/map2 `0.0671 / 0.0534 / 0.0194`；O3/map4/羰基 O `0.0490 / 0.0390 / 0.0123`；N18/map20 `0.0100 / 0.0080 / 0.0027`（**低于噪声底**）；H 合计 share **0.869**、重原子 **0.131**。
- **方向与键响应（同一模，单位模振幅）**：û(O3→N18) = (0.5576, 0.8216, 0.1190)，d(H27)·û = **0.9916**（H 沿 O3→N18 方向）；**δR(O3–H27) = +0.9162**（伸长）、**δR(N18–H27) = −0.7612**（缩短）、**δR(C2–N18) = +0.0140（沿模微增，不是成键压缩）**、δR(C2–O3) = −0.0195。
- **三档判定**：**纯 PT 主导**（协同档要求 C2 与 N 均有可观位移；此处 C2 5.3%、N18 0.8% 低于噪声底，且 C–N 沿模反而略增）⇒ 该帧**不作 E1a 的交付 TS**；job 1055 的 **+38.01 kcal/mol 只能写成「27 原子模型内该 PT 驻点相对 RC_27 的电子能差（−593.873953336 vs −593.934532807）」**，**不是 ΔE‡、不回填 hi.py**，ΔE‡ 保持 **null**。
- **交叉校验（排除截断伪象）**：同一几何在 41 原子模型（job 1042）的虚频 **−1547.0708 cm⁻¹**、组成 H 0.794 / C2 0.051 / O 0.033，与本文几乎一致 ⇒ 纯 PT 特征**不是去掉苯甲醛造成的伪象**（我用自写解析器在 ts_0008 参照 log 上校验过：117 模、表头 L1507、−1547.0708（L1516）、约化质量 1.0979、力常数 1.5482、atom41 share 0.7943 ⇒ 与 lane1 独立解析一致，工具 sha `d3e77e77…`）。
- **端点连接的不确定性（如实登记，不得越过）**：该驻点把 H 置于 N18 1.2217 / O3 1.3488 的桥位，模的正反方向分别通向 N–H 与 O–H 两种质子归属；它究竟连到 RC_27（N–H）与 INT1_27（O–H 0.9699）中的哪一个、以及是否属于声明步的路径，**需要 IRC 才能定**；而 IRC 通道受 #197 停滞阻塞、手工 TS/IRC 提交被禁用 ⇒ 本包**没有**端点连通性证据，报告**不得**写「IRC 已证」或「已证明该步无鞍点」；已证伪的是「job 1055 帧 = N 进攻+质子转移的协同鞍点」这一假设本身。
- **归因声明（按主协调指定必写）**：「(D) 诊断：ts_opt 经管线 job 1055（refine.log sha 0023847f…）；频率段因 #197 停滞改由**同级单点 freq**（含 CPCM(DMSO)，输入 `E1A_TS_diag_freq.gjf` sha ef3d748c…）补做，几何（xyz sha 2b4cf70f…）与 refine.log 收敛帧逐原子一致」。
- **documented next action（本轮不执行）**：以 RC_27↔carbinolamine_27 沿 C2–N18 的内插帧（骨架内插、质子位置单独处理、minsep ≥ 0.9、R(C2–N18) 单调）作新 guess，走 `ts_resume`（**真实输入改动 ⇒ 平台接受并重跑 ts_opt，job 1055 的旧证据随之失效**），随后再补一次同级单点 freq；槽位与时限均不在本轮，如实记为未完成。
- **标签对账（本节一律工作序 1-based）**：C2 = atom 2、羰基 O = atom 3、N = atom **18**、转移 H = atom **27**；对应 map 标签 C2=map2 / 羰基 O=map4 / N=map20 / 转移 H=map21。lane1 §29.3 写的「N20 / O4 / H21」是 **map 标签**（= 工作序 18 / 3 / 27），不是 atom 20/4/21。
- **资源**：1062 于 **15:11:28** 正常终止；我 15:12:58 实测 free cpus **8**；E3a（job 1059）与 E3b 产物端（job 1061）仍在跑；E1a 侧**无在飞作业**。

### §R11.26 槽位时序更正 + 排产裁定：(D) 腾出的槽被 NY3 的 1063 占用；E1a fallback 维持「只制备、不执行」；E3b ts_opt 优先
- **槽位时序（主协调实测，我接受更正）**：1062 于 **15:11:28** 终止 ⇒ **15:12:13** free cpus 8 ⇒ **15:12:48** NY3 的 **job 1063**（产物端 Opt+Freq、输入 sha 6197876b…、17 原子、0 1、CPCM(Water)、8c/10240/prio0）起跑占用 ⇒ **15:13:31** running = 1049 / 1059 / 1061 / **1063**、free cpus **0**。**我 15:12:58 读到的 8 cpu 是 37 秒前的状态**（以此为记录，避免把旧读数当现值）；**E1a fallback 与 E3b 均未占用该槽**。
- **待定项 ①（E1a fallback 现在跑？）⇒ 维持不执行**，并新增一条硬理由：`ts_resume` 走 retry 语义时**可能覆盖 ts_opt/`refine.log`**，而该日志（sha 0023847f…）正是报告里引用的**诊断几何来源**（xyz 2b4cf70f… 由其末帧导出）⇒ 覆盖它等于毁掉本条边的证据链（与「不得触碰 ts_0006」同源风险）。交付窗口内**不重跑 E1a**；只允许 lane1 **制备**内插帧 + provenance（**不提交**），作为 documented next action。
- **待定项 ②（优先级）⇒ E3b ts_opt 优先**：E3b 两端齐（分母 job 1028 已定、产物端 1061 在跑）、guess 工具 v4 就绪，一次 ts_opt + freq 的完成概率明显高于 E1a 的两段重跑。**排产序：E3b ts_opt > NY3 ts_prepare > E1a fallback（不执行）**；单槽时按此序。
- **进报告「方法/判据」节的硬定量（主协调指定，已在 §R11.25 记录）**：δR(O3–H27) **+0.9162**、δR(N18–H27) **−0.7612**、**δR(C2–N18) +0.0140（沿模微增、无成键压缩）**、δR(C2–O3) −0.0195；以及 41 原子交叉校验（同一几何 −1547.0708 cm⁻¹、H 0.794 / C2 0.051 / O 0.033）⇒「纯 PT 不是截断伪象」。
- **读数纪律（主协调将写入报告）**：L1099 的 −1551.2317 / −9.4763 / −5.0350 属 Low frequencies 探针行，**不作虚频判据**；最低实模一律取 Frequencies 频段表首行（本次 41.7021，L1110）。
- **标签**：本节及 §R11.25 一律工作序 1-based（C2=2、羰基 O=3、N=18、转移 H=27）；map 标签 C2=map2 / O=map4 / N=map20 / H=map21 与 lane1 §29.3 的 N20/O4/H21 指同一批原子，两套号并存处必须显式对账。

### §R11.27 EM1 定稿：**缺测**（ΔE‡ = null）；下扫未完成、上扫与产物端从未起跑
- **直接观测（我 2026-10-17 15:15:07 CST 实测）**：`gold_finish_20261015/HI1/E2EM1/spectator/scan_down_c1c29.log` **3,650,901 B / 55,997 行**；`Optimization completed` **8 次**（= 已完成 8 个 scan point）；末行进度 `Step number 10 out of a maximum of 246 on scan point 9 out of 12`（L55198；L54184 为 scan point 9 的第 9 步）；**无 Normal / Error termination** ⇒ 交付窗口内**下扫不会跑完**。
- **升格包状态**：up-scan（`scan_up_c1c29.gjf`，sha **d7545a6e…**）与产物端 (R)-亚铵-醇盐 Opt+Freq **从未起跑**。
- **已有数值口径**：13.36 / 15.52 仅作 **candidate_only**，并标注**不可用于 (S) 题面定量引用**；已跑到的部分只登记为「下扫进行至 scan point 9/12，未完成、未判读」——**不得**把未完成扫描的任何单点当连通性或能垒证据。
- **EM1 缺什么（交报告「证据驱动修订」节）**：(a) **下扫完整剖面 + 上扫**，且二者并集满足单峰判据（步长 ≤0.05 Å、单调单峰）；(b) **产物端 (R)-亚铵-醇盐 Opt+Freq**（自身收敛、0 虚频、CIP 标签、与 HI1_M1 节点串比对、外围构象差异写明）；(c) **连通性替代口径声明**（无 IRC：两端 Opt+Freq 0 虚频 + 端点身份 + 端点松弛 + 扫描单峰，四项齐备才可写 verified）。三项缺一即 ΔE‡ = **null**（现状）。
- **其余各边现状（同轮）**：E1b = 分母成立（job 1051，−593.929762803，0 虚频）但 **TS 未起跑**；E3b = 等 job 1061（产物端 P）收敛后由 lane2 建 ts_prepare；E3a = 等 job 1059；NY3 = 等槽。

### §R11.28 本轮只读动作与工具登记（主协调指定）+ E1a fallback 的零算力替代路径获批
- **我本轮做了什么（全部只读/分析）**：① 自读 `E1A_TS_diag_freq.log`（sha e6c12847…）并按 §R11.25 判读；② 自写并**校验**模矢解析器 `HI1/E1/gauss_mode_check.py` sha256 **d3e77e77e0338b04489c08174b3b5bfe5484626765ee42d2faa03ffa94eb6698**（在 ts_0008 参照 log 上复核：117 模、imaginary 表头 L1507、−1547.0708（L1516）、Red. mass 1.0979、Frc const 1.5482、atom41 share 0.7943 ⇒ 与 lane1 独立解析一致）；③ `HI1/E1/e1a_diag_mode_analysis_v2.py` sha256 **aab0c0296167b1135fff39f27719a3f1f87c8f2dc645053609662681a94a9498**（键响应 δR 与方向投影）；④ `HI1/E1/check_fallback_frame.py` sha256 **10cdaf10adcdcab2b7bc7f7167c99a8e764ad77be68d91cec7635641606e692c**（复核 lane1 fallback 帧：27 原子 C8H15NO3、minsep 0.9000 @ 7H–18N、R(C2–N18) 2.2916、C2–O3 1.2195、N18–H27 1.0228、O3–H27 3.8705）。
- **边界声明**：本轮**未**提交任何作业、**未** ts_resume、**未** kill、**未**调 priority、**未碰** `ts/ts_0015/process.json`（我 15:19:21 复检：rev **11** / stage **refine** / 30,059 B / mtime **14:36:37** / `jobs/declaration_0001/` 仅 `ts_opt`）；除本节与 §R11.25–§R11.27（均由主协调要求）外**未改** STATUS/PROCESS 内容。
- **E1a fallback 的刚性结论（主协调已写入报告 §13.2 与台账 §R67）**：刚性内插在 R(C2–N18) ≤2.3 Å **无解**（v1–v11 全失败）；达标点 f589a848… 的 minsep 0.9000 Å 是由 **甲基 H···N18 0.90 Å 碰撞**换来 ⇒ **不得作 guess**；116a1b0d…（minsep 0.49）作废；唯一可行路径是**固定 R(C2–N18) 的约束松弛**（需算力+授权，本窗口不执行）。
- **零算力替代路径（主协调 15:2x 批准，只制备）**：用 `conformer_search` guided（ring_order + distance_filters；其输出在文档中明确为 constrained TS seed、非平衡系综）在力场层面做碰撞剔除 + 松弛：R(C2–N18) 限 **2.2–2.5 Å**、N18–H 限 **1.0–1.1**。交付门槛：27 原子且元素序与 refine 收敛帧逐位一致、minsep ≥0.9 **且列出最紧 3 个接触**（不得靠单点 H···N 0.90 换来）、C2–O3 ≥1.30、provenance 含工具参数 + ensemble sha + 「力场层面 ≠ QM 面」显式声明、帧 sha 与「仅 guess、非鞍点」声明。若也被拒或全撞 ⇒ 按「工具路径亦不可行」登记（报告 §13.2 同句）。
- **排产不变**：E3b ts_opt（等 1061）> NY3 ts_prepare（已放行，占现 8 cpu）> E1a fallback（不占槽）；1061 收敛后该槽归 E3b，lane2 需先把 v4 帧双 sha 备好。
- **NY3 的 1063 判读（登记，供「读数纪律」引用）**：45 模但 **1 imag −30.5951 cm⁻¹（k = 0.0006、甲基转子型）**、最低实模 45.5679 ⇒ **缺「0 虚频」这一条，不得写成已验证极小**；与 E1a 判例并列进「单虚频或软模不足以单独判定极小/鞍点」的纪律。
- **队列（主协调 15:18:5x / 我 15:19:21）**：running 1049 / 1059 / 1061、free cpus 8（1063 于 15:18:14 done）；8 cpu 放行给 NY3 的 ts_prepare。

### §R11.29 受导构象搜索的能力边界 + E1a 的 documented guess（裁定：接受但不进窗口）
- **能力边界（登记）**：`conformer_search` guided 在**片段间刚体摆放**语义下（工具诊断原文 `intra-fragment geometry stays rigid during placement`）**无法**达到 R(C2–N18) 2.2–2.5 Å 的早期进攻窗口：v1/v2/v4 三次调用均 **0 qualified**，最接近帧的 R(C2–N18) 为 **2.69–3.05 Å**；能拿到的干净帧下限约 **2.69–2.75 Å**。
- **可复核帧（我 15:20:50 CST 自算，脚本 check_seed_search_frames.py sha 963475ae…）**：`E1a_seed_search_v2/closest_attempt.xyz` **27 原子、元素序与 refine 收敛帧 27/27 逐位一致**、**R(C2–N18) = 2.7508**、R(N18–H27) = 1.0303、**C2–O3 = 1.2327**（羰基仍为双键）、O3–H27 = 2.3036；**最紧 3 接触全是正常化学键**：O13–H19 0.9807、N18–H27 1.0303、C1–H6 1.0926（**不是**靠 H···N 0.90 换来的）。v4 的 closest 为 R = 3.0481。
- **裁定（主协调 15:2x，登记）**：① **接受该 2.7508 Å 帧作 documented guess**，标注「力场来源（conformer_search guided）／**仅 guess、非鞍点**／**落在 2.2–2.5 Å 目标窗口之外**（早期反应物型，定位加成鞍点的概率低）」；② E1a 的表述由「结构性不可行」改为「**QM 闭环仍需固定 R(C2–N18) 的约束松弛（需一个 ts_opt 量级算力），本窗口未执行**」；③ **不放进窗口**（现在 0 空槽；即使腾槽优先级为 E3b ts_opt > NY3 > 本 guess），仅当交付前出现第三空槽且 E3b/NY3 均不需要时由主协调点名；④ **E1a 仍「未验证」、ΔE‡ 仍 null**、barrier 0/4、hi.py null 未动。
- **两处更正**：① 我此前的门槛「C2–O3 ≥ 1.30」**方向写反**——早期帧应保持**羰基双键**（C2–O3 ≈ 1.22–1.28），v2 的 **1.2327 属通过**（勘误记主协调转述名下、我执行有责）；② lane1 报的 v1 帧 sha **845a4bd9…（R = 2.6920）在盘上找不到**（`split/` 下无 `E1a_seed_search_v1` 目录）⇒ 标「**引用未核实、不得进报告**」，需恢复或重跑后给真实路径与可复核 sha。
- **仍在跑（15:21:35 实测）**：running 1049 / 1059 / 1061 / 1064、queued 空、free cpus **0**；1049（EM1 下扫）在 `scan point 9` 第 14 步、**无** Summary of Optimized Potential Surface Scan（下扫未完成）；1061（E3b 产物端 P）与 1059（E3a ts_opt）两 log 均**无** Normal termination。

### §R11.30 勘误：A 帧**在盘**（我上节误判「找不到」）+ manifest 映射更正（只涉标识，不涉数值）
- **被勘误的表述**：§R11.29 写「lane1 报的 v1 帧 sha 845a4bd9…（R = 2.6920）**在盘上找不到**…标『引用未核实』」。**该判断错误**：文件存在，路径是 `split/E1a_seed_search/closest_attempt.xyz`（**目录名不带 _v1 后缀**）；我上一轮按 `E1a_seed_search_v1/*` 匹配落空，把 glob 未命中误当成不存在 —— 正是「不得用搜索失败推断 artifact 缺失」的那条纪律。
- **现在的真实复核（我 2026-10-17 15:22:00–15:22:11 CST 实测）**：A 帧 sha256 **845a4bd9908e1607e7ead78d17896912bf2bc874d0310f50bb399fb90e813435**、**27 原子、元素序与 refine 收敛帧 27/27 逐位一致**；**R(C2–N18) = 2.6920**、R(N18–H27) = 1.0349、C2–O3 = **1.2383**、O3–H27 = 2.2993；**最紧 3 接触全为正常化学键**：O13–H19 0.9794、N18–H27 1.0349、C1–H7 1.0926。⇒ A 帧与 B 帧同级干净，且 **R 更接近 2.2–2.5 目标窗口（2.6920 vs 2.7508）**。
- **manifest 映射更正（我逐个实测）**：A `E1a_seed_search/guidance_manifest.json` = **c9098d91d1b34f5bb22bdd1ea91637a4d51017a9a9f5a2f0210871a624ad70e4**；B `_v2/…` = **8a4e3cea…**；C `_v3/…` = **06e18dd5…**；D `_v4/…` = **892f988e…**。帧：A **845a4bd9…**、B 与 C **同为 9a5c9c32…**（同一几何、两份 manifest）、D **aa6fc0a0…**。lane1 的候选 provenance 把 A 的 manifest 写成 8a4e3cea…（那是 **B** 的）⇒ **需更正**；其余数值一致。
- **provenance 文件**：`split/E1A_SEED_CANDIDATE_PROVENANCE.md` sha256 **2b37153e705c7f3d4b4b52ef0f7c456d15b1951297954d093d811c0a6bcc3394**（我实测存在）；其中「四次均为 0 qualified ⇒ 无 ensemble、ensemble_path 为空」的说明**正确**，引用应改为 closest_attempt + guidance_manifest 双 sha（不虚构 ensemble sha）。
- **影响面**：仅「A 帧是否存在」这一判断与 manifest 的标识映射；**所有 R / 接触 / minsep 数值不变**，§R11.29 的裁定（接受 2.7508 Å 帧作 documented guess、不放进窗口、E1a 表述改为「需固定 R(C2–N18) 约束松弛」）不变。**候选集**现有 A（2.6920）与 B（2.7508）两帧同为干净帧，主协调已接受 B；若采用 A 需主协调点头（我不自行改选）。

### §R11.31 裁定落定：E1a 的 documented guess = **A 帧**（B 作备选）；口径与「不提交」不变
- **裁定（主协调 15:2x）**：documented guess 由 B（2.7508）改为 **A** —— `split/E1a_seed_search/closest_attempt.xyz` sha256 **845a4bd9908e1607e7ead78d17896912bf2bc874d0310f50bb399fb90e813435**、**R(C2–N18) = 2.6920**、R(N18–H27) 1.0349、**C2–O3 = 1.2383**、O3–H27 2.2993、最紧 3 接触全为正常化学键（O13–H19 0.9794 / N18–H27 1.0349 / C1–H7 1.0926）、元素序 27/27 与 refine 收敛帧一致；**B（9a5c9c32…，2.7508）作备选记录**。
- **口径不变（五条同时成立）**：① 力场来源（conformer_search guided，RDKit 力场）≠ QM 面；② **仅 guess、非鞍点**（无 Hessian、无虚频、无连通性）；③ 落在 2.2–2.5 Å 目标窗口**之外**（早期反应物型，定位加成鞍点的概率低）；④ **本窗口不提交、不采用**（现 0 空槽；即使腾槽优先级为 E3b ts_opt > NY3 > 本 guess，仅第三空槽且前两者不需要时由主协调点名）；⑤ **E1a 未验证、ΔE‡ = null**、barrier 0/4、hi.py null 未动。
- **E1a 的最终表述**：协同加成鞍点**未被定位**；已定位并判读的是 **O/N 质子桥 PT 鞍点**（−1551.2317 cm⁻¹，模 79.7% H、δR(C2–N18) = +0.014 无成键分量，相对 RC_27 +38.01 kcal/mol，仅作电子能差）；fallback 走 QM 闭环仍需**固定 R(C2–N18) 的约束松弛**，本窗口未执行。
- **能力边界（登记）**：受导构象搜索在**片段间刚体摆放**下 R(C2–N18) 下限 ≈ **2.69–2.75 Å**（四次调用 0 qualified）；刚性内插同窗口无解（v1–v11）。
- **交付节奏（主协调 15:2x）**：约 **15:33** 开始整理终稿；1049（EM1 下扫，scan point 9 第 14 步）、1061（E3b 产物端 P）、1059（E3a ts_opt）若届时仍在跑，按「**未终态、result = null**」写，不追赶。
- **勘误已复核落盘（我 15:23:52 CST 实测）**：lane1 的候选 provenance **2b37153e… → cb07019c196d6e759bc34945807784d4ff1437846d4134ef39898cfa7203363a**（§3 表 A 行就地改为 **c9098d91…**，并新增 §7「Erratum — correction, NOT a silent edit」说明 8a4e3cea 属 B）；`LANE1_STATUS.md` **2a7e8f6c5398572cef02db3a98a559b9e5154673560a54612012db3ca5a1010c**。四组映射现与我实测一致：A frame 845a4bd9 / manifest **c9098d91**；B 9a5c9c32 / **8a4e3cea**；C 9a5c9c32（与 B 同几何）/ **06e18dd5**；D aa6fc0a0 / **892f988e**。
- **约束松弛的口径（答复 lane1）**：**本窗口不授权**（0 空槽；即使腾槽优先级 E3b ts_opt > NY3；且它是 ts_opt 量级重跑）；仅当交付前出现**第三个空槽**且 E3b/NY3 都不需要时，由主协调点名授权**一次**。
- **会话标识**：lane1 后续回报的会话 id 为 **as_fc7fdbb5e5564d93**（同一 lane1 角色、同一职责），台账按此记。

### §R11.32 交付结算（partial，追记起点）：报告 §14 口径、交付面 sha、与包内贡献/未完成清单
- **交付判定：partial**（主协调 15:3x）：11 条边中 **3 条已回填并通过守卫**（NI5_E1 0.93、NR1_E1 0.0、HL1_E1 0.0）、**8 条按「明确缺测 + 缺什么 + 已证伪什么」交付、result = null**。
- **报告**：`gold_finish_20261015/FINAL_DELIVERY_DRAFT.md` sha256 **a2964d8d37aa3214fd03136b5a4d6d95a0e4a3b57c9465a6368c1e6b0cf230df**、277 行；§14 为交付结论。
- **§14 两表结构（我 awk 复核，避免口径误算）**：主表 **5 列 × 11 行**（L249–L259）＝ 3 已回填 + 8 null，其中 #5 **HI1_E1** 与 #7 **HI1_E3** 是「旧边被五步模型取代 → 拆为 E1a/E1b、E3a/E3b」的两条 legacy 行；**新拆四边表 4 列 × 4 行**（L265–L268：HI1_E1a / E1b / E3a / E3b，全 null）。⇒ 「8 条缺测」指主表第 4–11 行，**不得**再与新增 4 行相加（否则误算为 12）。
- **交付面最终 sha**：`hi.py` **0ac110bc7e5b57618c1cc272cb93caa3054d3204c5db185d512330f3e97bc4cc**、`HI1.json` **54221e6591c75f88d2f6d96e853302c48bb25aefb9cc191aab2f6113119b61d0**；其余 9 文件与冻结值一致。
- **交付后纪律（主协调）**：1059 / 1061 / 1049 / 1064 的终态只写成 **§R11.33 起的追记**，**不改 §14 口径、不改任何交付面文件、不回填任何 barrier**；**不再发起 ts_resume / 新提交**；原生日志字节不改写。
- **本包（HI1 写权会话）贡献摘要**：① `hi.py` 的 I1 改写为 5 步（R→carbinolamine→enamine→iminium-aldolate→hemiaminal→P）+ `HI1.json` 重生成（5fd0ecb2… → 54221e65…）+ `regenerate_identically` 守卫通过；② 复核 RC_27（0 虚频，−593.934532807）、job 1051（情形 1，+2.99）、job 1053（1028 的重复优化）、job 1028（E3b 分母）、job 924（EM1 反应物端）；③ E1a 的 ts_opt 复核（L10724 Stationary point、+38.01 红旗）与 (D) 诊断判读（PT 鞍点，模 79.7% H、δR(C2–N18) +0.014）；④ 平台 **#197** 停滞诊断（含 ts_resume 在 failed_attempt=null 时被结构性拒绝的逐字证据）；⑤ E3b 产物端 P 的输入/几何复核（41 原子 C15H21NO4、24+17 片段、N4 三配位含 H26 1.020、最紧含氢接触 1.7479 Å = C2···H26）；⑥ 三次勘误（1.7479 Å 归属、A 帧「缺失」误判、C2–O3 门槛方向）；⑦ EM1 缺测定稿。
- **未完成（如实登记）**：E1a 协同加成鞍点、E1b 的 TS、E3a（job 1059）/ E3b（产物端 1061 + ts_opt）验收、EM1 下扫/上扫/产物端、NY3 三边；本包四条新边 **ΔE‡ 全部 null**、barrier 回填 **0/4**、hi.py 的 null 未动。

### §R11.33 追记（交付后，不改 §14 口径）：E3a 的 ts_opt（job 1059）正常收敛，管线**自动**进入 freq（job 1067）
- **ts_opt 终态（我 15:43:10–15:43:19 CST 自读）**：`ts/ts_0016/jobs/declaration_0007/ts_opt/refine.log` sha256 **696f993747cad4bc8acdb1ecb201e21fff7b58c015bc5c23162f6c9b51742612**、**30,219 行**；**L29133 `Optimization completed.` / L29134 `-- Stationary point found.`**（第 30 步，max 232）；**L30219 `Normal termination` @15:42:07**（elapsed 56 m 25.2 s）；末次 SCF **E(RB3LYP) = −939.295152015**（**L28774**）；全程无 FormBX / Bend failed / Tors failed / NStep 截断 ⇒ 不需笛卡尔规避、未重投。
- **我的独立几何复核（41 原子；末 orientation 块自 L29622 起，解析后断言 41 行 = NAtoms，元素 C15 H21 N1 O4）**：C2–O25 **1.8613**、O25–H27 **1.1636**、O10–H27 **1.2466**、O11–H27 3.3582、O25–H26 **0.9690**、**C2–N4 1.3433**（仍近亚胺双键）、C9–O10 1.2908、C9–O11 1.2284、**∠(O25–H27···O10) = 176.2°**（近线性中继）、minsep **0.9674** ⇒ 与 lane2 报值**逐项一致**。
- **能量差（仅登记，不是 ΔE‡）**：ΔE(TS − job 961) = +0.025503464 Eh = **+16.0037 kcal/mol**；ΔE(TS − job 1028) = +0.017474590 Eh = **+10.9655 kcal/mol**。
- **管线自动推进（重要对照）**：`jobs/declaration_0007/frequency/frequency.gjf` sha256 **76c5fc09e2e75d782f09a69912da44cb83bf38eb0628acec160a49c1932675ec**（route 含 CPCM(DMSO)，纯 freq），**job 1067 起 15:42:12 running**，ts_0016 rev **39**、waiting_for job:1067 ⇒ **同一 pipeline 在 ts_0016 上 stage 推进正常**，故 #197 的挂起是 **run 特定**（ts_0015），不是通用 stage-advance 缺陷；这与 lane1 的「ts run 在 stage 之间推进处特定挂起」口径一致。
- **仍待验收（不改变冻结口径）**：freq 的 39 组 = 117 模与**恰 1 虚频 + 模矢落 C2–O25 成键 / O25–H27→O10 中继**（甲基/羧基伪象不算）；E3a 的 barrier **不回填**（交付已冻结、§14 口径不变）；E3b 产物端 job 1061 仍在优化（step 30/239）。
- **队列（15:43:03 实测）**：running **1049 / 1061 / 1067**、queued 空、free cpus 8。

### §R11.34 冻结期 E3b 口径定稿（主协调 15:45 裁定，优先于我先前的 A-lite）
- **零算力部分（允许）**：1061 收敛后做**四项核对**（仍两片段 / C2–N4 ≥2.4 Å / N4–H 存在 / CIP 8=S、29=S）+ **H26 假象三查**（C2···H26 是否松开 >2.4 Å、H26 是否回 O25、是否被当 C–H）→ 用 v4（sha 8b7a36fb…）出**正式 guess 帧 + GUESS_SELECTION 报告**（报双 sha 与 H26···C2 / R(C2–N4) / R(C2–O25) / R(N4–H26) / minsep）；产物一律标「**post-freeze asset、非交付证据、未提交**」；**不得为出帧改种子**（改种子＝新输入，冻结期内不做）；三查任一触发 ⇒ 按「P 端点作废、需重出种子」登记。
- **有算力部分（条件式允许）**：当且仅当 **P 通过四项核对与三查、且 free cpus ≥ 8（不抢占 1049 / 1061 / 1067）**，lane2 **可直接建 E3b 的 ts_prepare run**（走 durable ts 工作流，**禁止手工提交 TS/IRC**），并立即报 job id / 输入 sha / route 首行；条件不满足则**停在出帧、不再请示**。
- **地位**：全部为 **post-freeze 追记**——报告 `FINAL_DELIVERY_DRAFT.md`（sha a2964d8d…、277 行）与交付面 11 文件 **sha 不动**；E3b 的 barrier 在「恰 1 虚频且模矢含 C2–N4 断裂 + N4–H26 生成、两端 0 虚频、连通性」齐备前**一律 null**；是否回填、是否改交付面由**下一窗口**决定；E3a 的 +16.0037 / +10.9655 kcal/mol 只作收敛驻点能量差、**不称 ΔE‡**。
- **纪律**：不重投、不调 priority、不 kill、不碰 `ts/ts_0015`；不删盘上产物。
- **口径沿革**：我先前的 A-lite（仅允许零算力部分）只在帖子里出现、未写入 STATUS，现由本条取代；差异仅「P 通过且有空槽时可建 ts_prepare」。我无异议，已原文转 lane2 执行。











 `\n\n`、片段 24+17、minsep 0.9673 = O28–H24、N4 三配位含 H26 1.020、N4···C2 2.7000）均不变；已同步更正给主协调与 E3 道（主协调 15:03 的回帖里引用了错误归属，已单发勘误）。


### §R11.35 追记（交付冻结期内，不改 §14 口径）：E3a 的 freq（job 1067）终态读数 + 管线**自动**起 IRC（job 1068）
- **时刻**：读数轮 `date` 实测 2026-10-17T15:54:56+08:00；写入轮实测 2026-10-17T15:56:53+08:00。
- **日志**：`ts/ts_0016/jobs/declaration_0007/frequency/frequency.log`，sha256 `c5ac84026e43c5155f2bf6e20787885f77662666e737ad4783e16036ae7291b9`，5,294 行，**Normal termination L5294 @ Sat Oct 17 15:54:25 2026**；无 Error termination、无 l9999/l103/l123。
- **① 完整性**：NAtoms=41（L157）⇒ 3N−6 = 117；`Frequencies --` **39 组 ×3 = 117**（首组 L1510、末组 L3334）⇒ 相等，二阶导数算全（非「未算全」）。
- **② 虚频**：imaginary 头行 **L1501**「******    1 imaginary frequencies (negative Signs) ******」；频段表内负值 **1 个 = −783.7914 cm⁻¹（L1510 第 1 值）**，Red. masses **1.5559**、Frc consts **0.5632**（L1511/L1512）。L3439「1 imaginary frequencies ignored.」属热化学段忽略该模的例行行，**不是第二个虚频**。
- **③ 最低实模**：**23.6787 cm⁻¹**（L1510 第 2 值，频段表内首个正值；不取 L1499 `Low frequencies` 行的 −10.1298/−0.0004 探针值）⇒ ≤50，软模。
- **④ 模矢投影**（自算脚本 `gold_finish_20261015/HI1/E3/check_e3a_freq_1067.py`，sha `38492fe3fe7655693592b074891a1999b751363be172d8835f3e63d3cfe41733`；几何取同一日志 Standard orientation L475–L515，恰 41 行）：
  - **L2 份额**：H27（工作序 27 / map H21）**0.8939**、H26 **0.0553**、C2（map2）**0.0237**、O25 **0.0114**、O10（map O4）**0.0017**；羧基 C9/O10/O11 合计 **0.0062**；吡咯烷 N4 **0.0002**；甲基 H(36–41) 最大 |d| 0.0283。
  - **键响应**（|d| 归一化，+q 取 H27 朝 O10 一侧）：dR(O10–H27) **+0.9589**、dR(O25–H27) **−0.8898**、dR(C2–O25) **+0.2525**、dR(O25–H26) +0.0011、dR(C2–N4) −0.0650、dR(C9–O10) −0.0811、dR(C9–O11) +0.0341；d(H27)·û(O25→O10) = **−0.9199**（cos −0.9768）。
  - **判读**：非甲基转动主导、非羧基 C–O 伸缩主导；模以**质子转移**为主（H27 89%），但 **C2–O25 有 0.2525 的真实成键分量（约质子分量的 26%）**——与 E1a「C–N 分量 +0.014 ≈ 噪声」不同，此鞍点确实耦合了 C–O 生成与 O25–H27→O10 中继。**是否等同声明的协同加成/中继鞍点仍以 IRC 连通性为准**，不据模矢单独称 qualified TS。
- **几何（同一日志，L475–L515，恰 41 行，已断言行数）**：C2–O25 **1.8613**、O25–H27 **1.1636**、O10–H27 **1.2466**、O25–H26 **0.9690**、C2–N4 **1.3433**、C9–O10 **1.2908**、C9–O11 **1.2284**、O10–O11 2.2251、∠(O25–H27···O10) **176.2°**、minsep **0.9674**（O24–H28）；与 ts_opt（job 1059）收敛帧逐项一致 ⇒ freq 确在 TS 几何上做，不是换了结构。
- **能量**：E = **−939.295152015**（L816，与 1059 末次 SCF 同）；ZPE **0.342095**（L3469）= 898171.0 J/mol（L3440）；Sum of electronic and zero-point = −938.953057（L3473）。**ΔE(TS−961) = +16.0037、ΔE(TS−1028) = +10.9655 kcal/mol 只作驻点能量差，不是 ΔE‡**（我按 E(1028) = −939.312626605 复算 10.9655 一致）。
- **管线（关键新事实）**：freq 终态后管线**自动**开 IRC——`jobs/declaration_0007/irc/irc.gjf`（15:54 写入），**job 1068 running @15:54:27+08:00**；`process.json` **revision 43 / stage=refine / waiting_for job:1068 / failed_attempt null / blocked null / intervention_count 6**。**非我提交**（durable 工作流自动推进）；这也是 #197 的第二个对照（ts_0015 在同位置停滞、ts_0016 连续走完 ts_opt→freq→IRC）。
- **口径不变**：E3a result 仍 **null**、barrier **不回填**（仍 0/4）；本轮**未提交作业、未 ts_resume、未 kill、未改交付面 11 文件**；`FINAL_DELIVERY_DRAFT.md`（sha a2964d8d…、277 行）不动。
- **本轮自查勘误（内部，未对外引用错值）**：我第一版脚本按 `p[2],p[3],p[4]` 取坐标（列错位，把 Atomic Type 当 X），得出 C2–O25 0.1137、C9–O10 0.7764 等化学上不可能的值；已改为 `p[3..5]` 并重算，上面所有几何/键响应均为修正后值，并已核对 minsep 与 ∠ 合理。

### §R11.36 追记（同轮补正，不改 §R11.35 数值）：引用约定统一 + IRC 输入只读事实
- **引用约定（与主协调 15:58 CST 对齐）**：模矢一律写「物理陈述 + |dR|」，不单给带符号 dR；附脚本 sha（本包 `38492fe3…`）与归一化分母（全原子 L2：H27 0.8939；全原子 L1：0.4892；四原子内 90.8% 须注明「四原子内」）。**勿把 +0.959/−0.890 与 lane 的 −0.959/+0.890 并列引用**——那是同一物理量在两套 q 正向下的符号。
- **模矢行号映射（不依赖脚本可复核）**：`Atom  AN` 表头 **L1514**，原子行 = 1515+(序−1) ⇒ C2 **L1516**、O25 **L1539**、H26 **L1540**、H27 **L1541**；频段表行 L1510。
- **能量行号**：L785 `E= -939.295152015081`、L801 `E= -939.295152015109` 为频率段末两次 SCF 迭代（差 2.8e-11 Ha，数值噪声）；**可引用值取 L816 `SCF Done: E(RB3LYP) = -939.295152015`**。
- **IRC 输入（管线自动生成，非任何一方提交）**：`jobs/declaration_0007/irc/irc.gjf` sha256 `fad5c8b8e250e3b10433aaad4923e318d22bcbc29ee4624e342496ec66381a44`；route 首行逐字 `#p irc=calcfc B3LYP/def2SVP empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=dmso)`；title 含「IRC both directions from the refined saddle」；电荷/多重度 0 1 与原 TS 一致。
- **IRC 日志（当轮实测 2026-10-17T15:58:19+08:00）**：`irc.log` sha256 `505aafd141c19a2726da48c6d26d8319c6eea13e8f36f34d76fb0f45f951e170`、823 行；L221 进 l123、L222/L239 为 IRC 段标记，**尚无 Point Number 表、无 termination**。
- **口径不变**：E3a result=null、barrier 不回填；上述 IRC 事实只作「连通性尝试已由管线发起」的登记，不构成连通性证据。

### §R11.37 追记：E3a **两端均满足「41 原子 / 117 模 / 0 虚频 / 收敛」**（仅连通性未闭合）
- **两端归属固定（此前我只写 ΔE(TS−961)/ΔE(TS−1028)、未定义端别）**：**961 = 反应物侧 I2（38 原子 + H2O 3 原子 = 41）**；**1028 = hemiaminal 侧（产物端）**。两者都是 E3a 的两端，不是我先前文字里可能读成的「同一端的两种叫法」。
- **961 独立复核（自读，`runs/I2_optfreq/I2_optfreq.log` sha256 `63dda25e04529e65920526304fb88755db9393e9c22bd3a6efb76eeee0af0d0e`、24,001 行）**：NAtoms=**41**（L167）⇒ 3N−6=117；`Frequencies --` **39 组 ×3 = 117**（首组 **L19879**、末组 **L21703**）；**无 `imaginary frequencies` 头行（grep 计数 0）**、频段表**无负值**；最低实模 **35.3075 cm⁻¹**（L19879 第 1 值，Red. mass 4.1273 / Frc const 0.0030）；ZPE **0.345935**（L21837）；`Optimization completed` **L17315**、`Stationary point found` **L17316**；**两段 Normal termination**：**L18401 @2026-10-15 21:59:30**（opt 段）与 **L24001 @22:05:55**（freq 段）——该日志是 opt+freq 两段拼接，引用时须注明是哪一段。
- **961 能量**：**E = −939.320655479**（L16950 opt 段收敛末次 SCF；freq 段单点 **L19183 同值 −939.320655479**；L16109 −939.320655262 是较早优化步，勿引）。
- **1028（hemiaminal 侧）既有证据不变**：E −939.312626605、117 模、**0 虚频**、最低实模 19.8439（log sha `1ec7e4c6…`）。
- **驻点能量差（复算一致，仍非 ΔE‡）**：ΔE(TS−961) = **+16.0037**、ΔE(TS−1028) = **+10.9655** kcal/mol；961 比 1028 低 **5.04** kcal/mol ⇒ 若 IRC 双向端点身份成立，E3a 的能垒量级应参照**较低端 961**（+16.00），但**在连通性证据齐备前不给任何 ΔE‡**。
- **仍未闭合的唯一项**：IRC（job 1068）双向端点身份 ⇒ **E3a result=null、barrier 不回填**；交付面 11 文件与报告 a2964d8d… 不动。
- **来源分工**：961 的端别指认与读数由 lane2（as_06db52ada5014800）提出，我据原生日志逐项复核通过；复核脚本 `HI1/E1/gauss_mode_check.py`（sha `d3e77e77…`）。

### §R11.38 裁定登记：**不解冻**——E3a 在交付面内保持 result=null，IRC 成功后只作 LEDGER 追记
- **裁定（主协调 2026-10-17 15:59:34 CST，本会话采纳并执行）**：交付面已冻结（报告 a2964d8d…/277 行 + 11 文件 sha），**即使 IRC（job 1068）双向完美收敛，也不把 +16.00 写进生成器/HI1.json/报告**；仅在 LEDGER 追记「可引用值 + 判据落点 + 证据清单」并标注「未回填、冻结面内仍 null」。回填由**下一窗口**决定，不由执行 lane 或本窗口决定。
- **数值口径精确化（取代我 §R11.37 里「5.04」的写法）**：E(961) − E(1028) = −939.320655479 − (−939.312626605) = **−0.008028874 Ha = 5.038 kcal/mol**（5.04 是四舍五入）。
- **若下一窗口回填，四项判据（先写清，避免口径漂移）**：
  1. IRC **双向** Normal termination（calcfc 下两方向都出路径点），单向完成不算；
  2. 两方向末端与 961 / 1028 连通性一致：C2–O25 距离、H27 归属原子（O10 还是 O25）、片段组成与端点相符；关键键长差 ≤0.03 Å；末端能量不高于对应端点 +1 kcal/mol；
  3. 两端各 0 虚频（961 ✓ `63dda25e…` 117 模 0 虚频最低实模 35.3075；1028 ✓ 117 模 0 虚频最低实模 19.8439）；
  4. TS 恰 1 虚频 + 模矢含声明键对三分量（相对符号三元组 (−,+,−)，|dR| 0.959 / 0.890 / 0.252）。
- **回填写法（仅在四项齐备时）**：ΔE‡ = E(TS, **L816**) − E(961, **L16950 / L19183**) = **+16.0037** kcal/mol；否则保持 null，登记「IRC 未完成」。
- **本会话状态**：零提交、未 ts_resume、未 kill、未碰 `ts/ts_0015` / `process.json`；交付面 11 文件与报告未动；对 IRC 1068 与 1061 只读巡检中。

### §R11.39 追记：E3b 产物端 P 的 **opt 内部步**收敛 + 四项核对/H26 三查通过；freq 内部步未出（E3b 仍 null）
- **时刻**：实测 2026-10-17T16:27:49 / 16:28:20+08:00（date）。
- **日志**：`gold_finish_20261015/HI1/E3/runs/P_e3b/P_optfreq.log`，69,203 行，时刻快照 sha256 `bc0e340d92bc0bbec407e60a1f2ef1ac9ac9f468de2d7926f22493508c24be70`（活文件，非定稿）。
- **收敛与终止**：`Optimization completed` **L67254**、`Stationary point found` **L67255**；**Normal termination L68350 @Sat Oct 17 16:24:12 2026**——**只结束内部步 1**；**L68352「Link1: Proceeding to internal job step number 2」**、**L68354 route `#P Geom=AllCheck Guess=TCheck SCRF=Check GenChk RB3LYP/def2SVP Freq`**，当前在 CPHF（"123 vectors produced by pass 0"）⇒ **频率段未出**：模数/虚频/最低实模/ZPE/最终终止均无。
- **几何四项**（opt 段末 orientation **L67755–L67795**，断言行数 = 41）：① 仍两片段 **24 + 17**（共价半径阈值 1.25×(r_i+r_j)）；② **C2–N4 = 3.3308 Å**（≥2.4）；③ **N4–H26 = 1.0200**（N4 最近邻 H26 1.020 / C8 1.4679 / C5 1.4706 / H27 1.7593）；④ CIP 原子 8=S / 29=S **未判**（需立体感知，留给 lane2）。
- **H26 假象三查（全未触发）**：C2···H26 = **2.9922**（原 1.7479，已松开）；H26···O25 = **3.1370**（未回 O25，仍以 1.020 挂 N4）；H26 最近碳 = **2.10**（非 C–H）。
- **产物自洽**：C2=O25 **1.2172**、O10–H27 **1.0112**（O25–H27 2.3670）、C9–O10 1.3282、C9–O11 1.2115、minsep **0.9689**（O24–H28）；title 逐字给 P = `smiles: CC(=O)C[C@H](O)c1ccccc1.O=C(O)[C@@H]1CCCN1 | HI1_P | E3b product endpoint | 41 atoms C15H21NO4 q0/m1 | built from job 1028 frame (C2-N4 broken, O25-H26 -> N4-H26, C2=O25)` ⇒ 酮 + 脯氨酸，与几何一致。
- **能量**：opt 内部步末次 SCF **E = −939.319540184（L66877，7 cycles）**；**ΔE(P−1028) = −4.3383 kcal/mol 只作节点能量差，非 ΔE‡**；E3b result 仍 **null**、barrier 不回填。
- **机制更正（取代我 §R11.37 前的「两段拼接＝两次作业」表述）**：一个输入含两个 Gaussian **内部作业步**（Link1），每步各自打印 Normal termination ⇒ I2_optfreq 的 L18401/L24001 与本文 L68350 同属此机制，**不是两次提交、不是重复计算**；引用仍标「内部步 1(opt)/内部步 2(freq)」。
- **顺带**：IRC 1068 于 16:28:20 实测 15,266 行、sha `49c72512…`、`Point Number 7 in REVERSE path direction`（Path Number 2，17 处 Path Number 行），无 termination ⇒ 反向路径推进中。

### §R11.40 追记：E3b —— P 四项核对 + CIP 通过（lane2 自算、我登记）；**新阻塞项**：v4 guess 构造在真实 P 帧被 minsep 门禁拒绝，未写出任何帧、未提交
- **时刻**：lane2 报告（16:31 前后）+ 我当轮实测 2026-10-17T16:31:59+08:00。
- **P（job 1061，opt 内部步）四项核对与 CIP（lane2 工具 `tools/cip_check_41.py` sha `748b7455…`，输入 `prep/P_1061_optframe.xyz` sha `957b9597…`，由 opt 内部步末帧导出）**：41 原子、片段 **[24, 17]**、formula C15H21NO4、**C2–N4 3.3308**、**N4–H26 1.0200**、**CIP 原子 8 = S、原子 29 = S**；isomeric SMILES `CC(=O)C[C@H](O)c1ccccc1.O=C(O)[C@@H]1CCCN1` 与声明 P 节点字符串**逐字符相同**；H26 三查未触发（C2···H26 2.9922 / O25···H26 3.1370 / 最近碳 2.9922 非 C–H）；几何 C2=O25 1.2172、O10–H27 1.0112、O25···H27 2.3670、C9–O10 1.3282 > C9–O11 1.2115、minsep 0.9689（O28–H24）——与我 §R11.39 的数字逐一相等。
- **对照 1028（反应坐标方向与声明一致）**：R(25,26) 0.9693、R(2,26) 2.0398、R(2,25) 1.4728、R(2,4) 1.4248 ⇒ 由 1028 到 P：C2–N4 1.42→3.33、C2–O25 1.47→1.22、H26 由 O25 转到 N4。
- **重要限定（不得越读）**：16:31:59 实测 P_optfreq.log **69,814 行、`Frequencies --` 计数 0、Normal termination 计数 1** ⇒ **频段仍在跑，P 尚无 0 虚频证据，不是频率验证过的极小点**；E3b result 仍 **null**。
- **新阻塞项（未实施任何补救、未提交）**：按既定要求用真实 1061 收敛帧跑 **v4（sha 8b7a36fb…）**，返回 **`no acceptable frame in lambda 0.55-0.65`**，**未写出帧与报告**，`prep/e3b_guess_formal/` 为空目录。诊断（`prep/diag_e3b_interp.py` sha `24b88ba6…`）：λ 0.30–0.90 全区间 minsep **0.7562–0.8908**，恒 <0.90；λ 0.56/0.60/0.64 = 0.7598/0.7660/0.7752（pair 恒 24–28）。成因：两端构象不同（全分子 Kabsch RMSD **1.9369 Å** > 无旋转 1.6770 Å ⇒ 非整体转动；分片段 1.0721 / 0.6109），笛卡尔插值把片段内键压塌（O28–H24 0.9673→0.756、C33–C34 1.3982→1.015、C1–H12 1.0983→0.79）。**结论：v3/v4 只在「构造的 P 种子（与 1028 同构象）」上验证过，换真实优化帧必然穿过不合理接触；不是 H26 伪象、也不是 P 不合格。**
- **候选修法（待主协调裁定，我不擅自授权）**：(a) **v5 = 逐片段 Kabsch 刚体插值 + 反应坐标内坐标插值**（诊断 `prep/diag_frag_interp.py` sha `0a0f5bf2…`：minsep 恒 0.9673、R(C2–N4) 1.7419→3.2443 单调、无非键接触 <1.20 Å；缺口是 C2–O25 被冻结需补内坐标插值）；(b) 用已备未提交的 `prep/e3b_scan/hemi_c2n4_scan.gjf`（sha `add74ec7…`，`B 2 4 S 5 0.205045`）在半缩醛胺自身构象上拉 C2–N4、以峰值作 guess（有算力成本）。
- **我当轮实测的旁证**：队列 free **8 cpus**（in_flight 3 槽 / 24 cpus：1049、1061、1068）⇒ 若主协调放行，资源闸门满足；但**建 run 仍须主协调裁定，且正式帧只能来自被批准的构造**。
- **纪律**：本轮无任何写帧之外的补救、无提交、未 ts_resume、未 kill、未改交付面；E3a/E3b barrier 均 null。

### §R11.41 裁定登记：E3b 的 guess 构造走 **(a) v5**（逐片段刚体 + 反应坐标内坐标插值）；(b) 仅作 fallback；提交等 P freq 通过
- **裁定（主协调 2026-10-17T16:32:44 CST）**：**(a) v5**；(b) 只在 v5 失败时 fallback 且须先报批；**提交一律等 P freq 通过**。裁定与我 16:32 的技术意见同向，并采纳我提的四条硬条件、另补三条。
- **七条执行硬条件（登记原文口径）**：
  1. λ=1 帧逐原子须落在 1061 opt 末帧 **≤0.03 Å**（端点不得漂移）；
  2. 全区间 **minsep ≥0.90 Å**，每帧报最紧 3 接触；任一 **<1.20 Å 非键接触**即该 λ 不合格；
  3. 原子序/map 固定：**N4=4、C2=2、O25=25、H26=26、H27=27**，41 原子断言；
  4. 只出**正式帧**（不写临时帧进 formal 目录），evidence_refs 只指真实文件路径；
  5. 片段内键长在 λ 全区间变化 **<0.01 Å**（显式断言；v4 的病根）；
  6. **C2–O25 1.4728→1.2172** 与 **C2–N4 1.7419→3.3308** 同单调、回跳即报错不写帧；**H26 挂 N4 1.05 Å**（沿 unit(N4−C2)）且 **H26···O25 ≥2.0 Å**；
  7. 报告须给 **λ0.50–0.80 全表** + xyz/报告双 sha + v5 脚本 sha + 两端输入 sha；**v5 帧只作 guess，不得称 TS**。
- **共同红线**：**绝不为过门禁而降 minsep 阈值**。若 v5 在 λ 窗口内做不到 minsep ≥0.90 或双单调 ⇒ 转 (b)，且 (b) 须先报批（算力成本 + 构象端点须由 IRC 连通性证明）。
- **提交闸门（不变）**：free 8 cpus 成立，但 **P freq 未过 ⇒ 不建 run**；须「freq 段 117 模 + 0 虚频 + 最低实模」「第二 termination」「free ≥8」三条齐备；建后立即报 job id / 输入 sha / route 首行。
- **我的验收动作（预告，避免执行侧走样）**：收到 v5 帧后我独立复核——λ=1 与 1061 末帧逐原子偏差、全区间 minsep 与最紧 3 接触、片段内键长漂移 <0.01 Å、C2–O25 与 C2–N4 单调性、H26–N4 1.05 与 H26···O25 ≥2.0、原子序与 41 原子断言、双 sha 与脚本 sha。
- **口径不变**：E3b result=null、barrier 不回填、交付面 11 文件与报告 a2964d8d… 不动。

### §R11.42 追记（触发事件①）：IRC 1068 双向正常终止但**路径被默认 maxpoints 截断** ⇒ E3a 端点身份/连通性未建立，仍 null
- **时刻**：终止 2026-10-17T16:33:44（日志）；我当轮独立复核 2026-10-17T16:35:08+08:00（date）。
- **日志**：`ts/ts_0016/jobs/declaration_0007/irc/irc.log`，sha256 **`0f9679f97f784a868a915857e63e690e200875dfab0eb25afe238975f166a4b6`**、**19,037 行**（我自读复核，与主协调读数一致）。
- **结构读数（我逐行核过）**：**L9503–9504** `Maximum number of steps reached.` / `Calculation of FORWARD path complete.`（止于 Point 10）；**L18200–18202** `Maximum number of steps reached.` / `Calculation of REVERSE path complete.` / `Reaction path calculation complete.`；**L18232** `Total number of points: 20`（梯度计算 26 次、Hessian 1 次）；**L19037** `Normal termination of Gaussian 16 at Sat Oct 17 16:33:44 2026.`；步长 0.100 bohr；route 为 `irc=calcfc` **无 maxpoints** ⇒ 默认 10 点/方向。
- **剖面（主协调读数，我采信其不变量：两方向单调下坡、最深仅 −5.33 kcal/mol ≪ 声明两端 11.0 / 16.0）**；末端几何：正向端 C2–O25 **1.878**（鞍点 1.861，未向 1.473 前进）、反向端 C2–O25 **2.061**、O10–H27 1.436、O25–H27 1.040（朝 961 走但远未到达）。
- **判读（与主协调同口径，不另起数值）**：(i) 双向端点身份**不满足**（截断）；(ii) **连通性不成立**；(iii) 两端 0 虚频 ✓；(iv) 1 虚频 + 模矢三分量 ✓ ⇒ **E3a result=null、barrier 不回填**；+16.0037 / +10.9655 仍只作驻点能量差。**只能写「默认参数下路径长度不足」，禁止写「连通性已证」或「通道不存在」。**
- **新增事实（我本轮自读发现，主协调 16:36 读数未含）**：`ts/ts_0016/process.json` 现 **revision 46 / stage=refine / terminal=None / failed_attempt=None**，但 **blocked = {failure_class: `missing_input`, message: `Explicit calculation required: verification.reactant_endpoint.optimization`, needs: ['verification.reactant_endpoint.optimization']}** ⇒ **管线自身要求「反应物端点优化」的显式验证输入**，run 处于 **blocked（非终态、非失败）**。按冻结口径我**不提交、不 ts_resume**，交由 lane2 与主协调处置；若下一窗口要推进，需先满足该 needs。
- **处置**：不手工补 IRC（TS/IRC 只走 ts_prepare/ts_resume）；该 maxpoints 限制已由主协调追加到 issue #197（`issuecomment-6231801912`）。
- **口径不变**：E3b 闸门仍等 P freq（16:33 读数 69,814 行、`Frequencies --` 0、termination 1）；E3a/E3b result 均 null

### §R11.43 追记（触发事件②）：E3b 产物端 P（job 1061）**freq 内部步完成**——117 模 / 0 虚频 / 最低实模 16.6787 ⇒ **P 为频率验证的极小点**，E3b 建 run 闸门四项全满足
- **时刻**：作业终态 ended **2026-10-17T16:34:17**（query_compute_job: state=done）；我当轮实测 2026-10-17T16:35:40 / 16:35:50+08:00。
- **日志**：`runs/P_e3b/P_optfreq.log`，**73,964 行**、sha256 **`183590c1ff28965769ebab84704e50f0ffbf0f9d63320bd9e0a4d0ec36aea15a`**（定稿：第二 termination 即末行，无后续追加）。
- **① 完整性**：NAtoms=41 ⇒ 3N−6 = **117**；`Frequencies --` **39 组 ×3 = 117**（首组 **L69831**、末组 **L71655**）⇒ 相等。
- **② 虚频**：**无 `imaginary frequencies` 头行**（grep 计数 0）、频段表**无任何负值**（全表扫描 0 命中）⇒ **0 虚频**。L69821 `Low frequencies --- -5.6987 -4.0098 -0.0005 0.0001 0.0006 2.8053` 是平动/转动探针行，**不作虚频判据**（本包第二次用到这条纪律）。
- **③ 最低实模**：**16.6787 cm⁻¹（L69831 第 1 值）**，Red. mass **5.0612**、Frc const **0.0008** ⇒ **极软但为正**；模矢（`HI1/E1/gauss_mode_check.py`）由芳环扭转/CH 摇摆主导（原子 38 |d| 0.374、37 0.275、32 0.255、16 0.239、39 0.234、15 0.218；L1 份额各 4–7%），**无单一重原子主导、无质子转移分量** ⇒ 属构象软模，不构成「非极小」。
- **④ 热化学/能量**：ZPE **0.344928**（L71789）；Thermal correction to Gibbs **0.291327**（L71792）；Sum of electronic and zero-point **−938.974612**（L71793）；freq 段单点 SCF **E = −939.319540184**（**L69139**，1 cycle，与 opt 段末 L66877 同值）。
- **⑤ 终止**：**第二 termination L73964 @Sat Oct 17 16:34:16 2026**（内部步 1 的 L68350 @16:24:12 仍有效；两者属同一作业的两个内部步，不是两次提交）。
- **闸门四项（对照主协调 §R11.41 口径）**：① 117 模 + 0 虚频 + 最低实模 ✓；② 第二 Normal termination ✓；③ 几何四项 + **CIP 8=S / 29=S** + H26 三查 ✓（§R11.40）；④ **free cpus = 24**（slots 9；仅 job 1049 在跑）⇒ ≥8 ✓。**四项齐备。**
- **口径**：P **是频率验证的极小点**，但 **E3b result 仍 null、barrier 不回填**（无 TS、无连通性）；下一步是 lane2 按 (a) v5 出正式帧（七条硬条件），我按 §R11.41 独立验收后才可谈建 run。

### §R11.44 裁定登记：E3b **条件式放行** v5 建 run（先建后 5 分钟内报四项）
- **裁定（主协调 2026-10-17T16:36:23 CST，其复核与 §R11.43 逐项一致）**：① P 身份成立（0 虚频的极小点），ΔE(P−1028) = −4.3383 kcal/mol 仍只是节点能量差；② **允许建 E3b 的 ts_prepare**——前提是 v5 帧按 §R11.41 七条硬条件**全部自检通过**（λ=1 逐原子 ≤0.03 Å、片段内键长漂移 <0.01 Å、C2–O25 与 C2–N4 双单调、H26–N4 1.05 Å 且 H26···O25 ≥2.0 Å、全区间 minsep ≥0.90 + 每帧最紧 3 接触、41 原子与原子序 map 固定、只出正式帧）；**满足七条即可先行建 run，不必等逐项目验**；③ **建后 5 分钟内**必须报：**job id / 输入 gjf 的 sha256 / route 首行逐字 / running 确认**，并附 v5 帧 xyz 与报告双 sha、七条自检表；**若核到不一致，停在下一阶段之前（不 kill 在跑作业）**；④ 资源照旧（单作业 ≤8 cpus / ≤10240 MB、priority 0、不重投、不调 priority）；⑤ **barrier 仍 null**，v5 只作 guess 不得称 TS，E3b 的 ΔE‡ 需 1 虚频 + 模矢含声明键对（C2–N4 断裂 + N4–H26 相关）+ 方向朝产物后才谈；⑥ E3a 维持「双缺口结案」（result=null、ts_0016 保持 blocked，��补输入、不 resume、不 kill）。
- **我的执行分工**：把放行条件与四项报备要求原样转达 lane2；收到建 run 报备后核 job id / 输入 sha / route 首行 / running，并抽验七条中的机器可判项（λ=1 逐原子偏差、minsep、键长漂移、双单调、H26 约束、原子序断言、双 sha）；不一致则要求停在该 run 下一阶段之前，不 kill。

### §R11.45 E3b guess 构造族评估：v5 结构性不可满足、v6 自检未过；**v7（反应坐标形变）经我独立验收通过**，等主协调一字放行
- **v5 不可满足（lane2 实测，我复核其化学必然性）**：两端点自身键长差 **C1–C2 0.0322 Å、C2–C3 0.0287 Å**（C2 sp³→sp²），另有 C8–N4 0.0125、O28–C29 0.0111、H27–O10 0.0163 ⇒「λ=1 等于 P 帧」与「片段内键长漂移 <0.01 Å」**互斥**；且按 unit(N4−C2) 挂 H26 在 λ=0.50 得 **H26···C8 = 0.9482 Å**（产物实测 ∠(C2–N4–H26) = **62.08°**，N–H 并非 anti-C2）⇒ 第 4 条方向假设本身错。
- **v6（内坐标插值）未过自检**：λ=0 重建帧对 1028 的 RMSD **2.04066 Å**（断言 1e-3 未过）、片段内成对距离最大偏差 4.42 Å ⇒ **未写任何帧**（`prep/e3b_guess_formal_v6/` 为空；脚本 sha `fcdf9705…`）。
- **v7（以频率验证的半缩醛胺 1028 末帧为基，只改声明反应坐标）文件**：xyz `prep/e3b_guess_formal_v7/E3B_TS_GUESS_v7_c2n4_2.200.xyz` sha **`be761bb04f2d80037a3f11381d5c1badba1c127bd1def5d5a8991d09223214d8`**；报告 `GUESS_SELECTION_e3b_v7.md` sha **`9e88dfeb06db1ff79f87f22d8cb856d14c97c6dac4c4ebdfd522611e29145f91`**。
- **我的独立验收（脚本 `HI1/E3/verify_e3b_v7_frame.py` sha `8f9442cd…`，与 1028 末帧 `hemiaminal_1028_lastframe.xyz` 逐键对比）**：41 原子、元素序与两端完全一致；**C2–N4 1.4248→2.2000**、**C2–O25 1.4728→1.3688**、**N4–H26 3.1829→1.0500**、H26···O25 **3.0821（≥2.0）**、H26 最近碳 C8 **1.8928（≥1.60）**、C2···H26 1.9744；O10–H27 0.9949、C9–O10 1.3297、C9–O11 1.2137 **全未动**；全局 minsep **0.9673（O28–H24，成键对）**、最紧非键 12–13 **1.7563** / 19–20 1.7753 / 14–15 1.7768、**无非键接触 <1.20**；**除反应中心外所有成键对 |dR| ≤ 2.2×10⁻¹⁶ Å**（唯二超 0.01 的是 (2,25) 0.104 与 (4,26) 2.133，即反应坐标本身）⇒ 报告声明属实。∠(C2–N4–H26) in v7 = 63.74°（P 为 62.08°，差 1.7° 因 C2–N4 方向不同，guess 可接受）。
- **规格勘误（我方两条，需修正后再引用七条）**：(i) 第 5 条「片段内键长漂移 <0.01 Å」须限定为**排除反应中心相关键**（C2/N4/O25/H26/H27 参与的键），否则与端点化学互斥；(ii) 第 6 条 H26 挂接方向应取**产物自身 N4→H26 方向**，不是 unit(N4−C2)（产物 ∠ 62°）。两条只改判据适用范围，不改任何已产出的数值。
- **性质与口径**：v7 **只是 guess，不是鞍点、不是收敛几何、无能量**；不声称产物端 ⇒ 产物身份须由 IRC 连通性证明。**E3b barrier 仍 null。**
- **风险提示（我提出）**：E3a 的教训表明该平台 IRC 默认 **maxpoints=10/方向**；E3b 的 C2–N4 需 1.42→3.33 且伴随 H26 转移，路径可能同样超长 ⇒ **E3b 的连通性也可能结构性拿不到**，届时表述须为「默认 IRC 参数下路径长度不足」，不得写「未收敛/通道不存在」。
- **授权状态**：v7 属**换构造**，放行权在主协调（其 16:36:23 口径：(a) v5 已放行、(b) 须先报）。我已把 v7 验收结果与建议上报，**未授权 lane2 提交**；放行后 lane2 建 run 须 5 分钟内报 job id / gjf sha / route 首行 / running。

### §R11.46 裁定登记：**放行 v7** 建 E3b 的 ts_prepare（主协调 16:39:37 CST，权威版；主题帖 evt_4fbd8be2ae984200）
- **放行内容**：以 v7 建 E3b 的 ts_prepare。**适用判据按其 §R94 修订版**（**第 1、4 条已撤回，非执行侧未达标**）：第 2 条本意＝除反应坐标外不得出现人为塌陷（v7 实测满足）；第 3 条只改 R(C2–N4) 1.4248→2.2000、R(C2–O25) 1.4728→1.3688（同进度 0.407）；第 5 条重述＝排除反应中心键后其余成键对漂移 <0.01 Å + minsep ≥0.90 + 无非键 <1.20（实测 0.9673、1.7563/1.7753/1.7768 ✓）；第 6 条重述＝H26 沿**产物自身** N4→H26 挂 1.05 Å（∠ 63.74° vs P 62.08°）、H26···O25 ≥2.0（3.0821）、最近重原子 ≥1.6（1.8928）；第 7 条＝41 原子 + 元素序 + map 固定、只出正式帧、evidence_refs 只指 xyz 与报告两文件、报告写「guess、非鞍点、无能量」。
- **v6 作废**（RMSD 2.04066 Å 未过断言、未出帧）；**v5 撤回**（其第 1/4 条为判据缺陷，责任在我方规格，非执行侧）。
- **报账要求（不变）**：建后 **5 分钟内**报 job id / gjf sha256 / route 首行逐字 / running 确认；资源 ≤8 cpus、≤10240 MB、priority 0、不重投、不调 priority；若核到不一致 ⇒ 停在下一阶段之前，不 kill 在跑作业。
- **E3b 的 IRC 预期口径（现即定死）**：若 IRC 同样被默认 maxpoints=10/方向截断（末点能量与两端差一个量级、末端几何未到 P 或 1028）⇒ **端点身份未建立 ⇒ E3b result=null、barrier 不回填**；表述统一「默认 IRC 参数下路径长度不足」；不写「未收敛/连通性已证/通道不存在」。真失败（l123、单侧不终止、NStep）按「IRC 未完成」登记并保留模值与模矢组成。
- **平台侧**：「IRC maxpoints 覆盖入口」列为 **E3a/E3b 共同瓶颈**（非 E3b 单独问题），主协调在 issue #197 追加适用于 E3b，并注明双向端点验证在这类 10+ kcal/mol 深步骤上结构性不可得。
- **其它不变**：E3a result=null、ts_0016 保持 blocked（不补输入/不 resume/不 kill）；E3b barrier 不回填；v7 及其报告标 post-freeze asset / non-delivery evidence；交付面（报告 a2964d8d…/277 行、11 文件 sha）不动。
- **我的动作**：把上述适用判据原文转达 lane2；收到建 run 四项后核 job id / gjf sha / route 首行 / running 与起跑时刻，并登记。

### §R11.47 追记：E3b 的 ts_prepare 已建 **ts_0019 / job 1069**，四项报账经我独立核对成立
- **时刻**：建 run 2026-10-17T16:39；job started **16:39:27**；我独立核对 2026-10-17T16:40:05+08:00。
- **run 侧**：`ts/ts_0019`，`process.json` **revision 11 / stage=refine / declaration_revision 1 / job_id 1069 / waiting_for job:1069 / blocked null / failed_attempt null / path_kind provided / current_ts_guess_path ts/ts_0019/path/input_0001/provided.xyz**。
- **输入**：`jobs/declaration_0001/ts_opt/refine.gjf`，**49 行**、sha256 **`f66c3c0c6f03e4c6e8763112db8e81b4fdde748489e94a9ccbeae96c5dc1bdc7`**（与 lane2 报值一致）；route 首行逐字 `#p opt=(TS,calcfc,noeigen) B3LYP/def2SVP empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=dmso)`、`%nproc=8` / `%mem=10240MB`。
- **guess 一致性（比 lane2 报的更强）**：`ts/ts_0019/path/input_0001/provided.xyz` 的 sha256 = **`be761bb04f2d80037a3f11381d5c1badba1c127bd1def5d5a8991d09223214d8`**，与 v7 帧**逐字节相同**（不是「≤0.03 Å 近似」）。
- **declare.json（我自读）**：q0/m1；**atom_map 恒等 0..40**；**reaction_center 0-based [[1,3],[3,25],[24,25]] = 1-based [[2,4],[4,26],[25,26]]**（与 lane2 报的 C2–N4 / O25–H26 / N4–H26 一致）；conformers.reactant `hemiaminal_1028_lastframe.xyz` + evidence `runs/interm_c160/interm_c160_optfreq.log`、conformers.product `P_1061_optframe.xyz` + evidence `runs/P_e3b/P_optfreq.log`。
- **作业**：query_compute_job → job **1069 running**、started_at **16:39:27+08:00**、路径即上述 refine.gjf；主协调独立用 `pgrep -cx g16 = 2`（1049+1069）佐证。`refine.log` 现 **1,066 行、`SCF Done` 计数 0** ⇒ 仍在 calcfc 初始 Hessian（CPHF），**尚无优化步**。
- **判读纪律（主协调口径，我采纳）**：运行期先看虚模是否**转子型**（pseudo-saddle），再看是否含 **C2–N4 断裂 + N4–H26 形成**；模数按 **3N−6 = 117** 判完整；虚频只看 band 表 + imaginary 行。
- **口径不变**：E3b result=null、barrier 不回填；v7 只作 guess 不得称 TS；若 IRC 被默认 maxpoints=10/方向截断 ⇒「默认 IRC 参数下路径长度不足、端点身份未建立」；真失败另按「IRC 未完成」保留模值与模矢；E3a result=null、ts_0016 保持 blocked（不补输入/不 resume/不 kill）；交付面 11 文件与报告 a2964d8d… 不动。
- **监测面更正**：`ts/ts_0017` 与 `ts/ts_0018` 不属于本包——owner_session_id **as_6fdd1a4300b74a9f**，分别 blocked 于 `conformer_input_invalid`（frequency_mode_without_frequency）与 `conformer_optimization_failed`（candidate_opt job 1064 failed）。本包 E3b 的 run 是 **ts_0019（owner as_06db52ada5014800）**，后续巡检只指向 ts_0019 的 ts_opt 日志，不再指向已终态的 irc.log / P_optfreq.log。

### §R11.48 记录口径补正（lane2 16:41 CST 提出，我采纳）：atom_map 的 1-based 声明 vs 0-based 落盘
- **事实**：lane2 调 `ts_prepare` 时 `reaction.atom_map` 传 **1..41（1-based，按其文档口径）**；落盘 `declare.json` 显示 **0..40** ⇒ **运行时规范化为 0-based**。两者是**同一个恒等映射**，不是两份不同声明。
- **引用写法（此后统一）**：「声明侧 1..41 / 落盘 declare.json 0..40（恒等，运行时规范化）」；`reaction_center` 的 **0-based [[1,3],[3,25],[24,25]] ↔ 1-based [[2,4],[4,26],[25,26]]**。
- **不影响**：v7 帧 sha `be761bb0…`、gjf sha `f66c3c0c…`、route、run/作业状态与任何几何或能量数值。
- **一并确认的硬证据**：`ts/ts_0019/path/input_0001/provided.xyz` 与 v7 帧**逐字节相同**（同 sha），此后作为「guess 即被验收的 v7 帧」的登记依据。

### §R11.49 裁定（回应 lane1 18:22 CST 请求）：**空槽不构成提交理由，E1a 额外约束松弛仍不授权**，维持只读
- **请求**：lane1（as_700f852fe3af412f）报 ts_0015 仍冻结（rev 11 / stage refine / process.json mtime **14:36:37**、jobs 下仅 ts_opt）、队列出现空槽（我实测 18:22:41：running **1049、1069**；free **8 slots / 16 cpus / 30,720 MB**），请裁定是否提交「固定 R(C2–N18) 的约束松弛」。
- **裁定：不授权，维持只读。** 理由：(i) **空槽不是闸门**——冻结的依据是 §14 已按 partial 结算（15:33）与「此后不再接受新的提交」，资源余量不改变授权状态；(ii) 该作业属 **TS 相关计算**，本包纪律是 TS 只在 durable workflow 内推进，管线外手工提交须**主协调点名授权**且逐项给定（固定距离、opt 还是 opt+freq、级别、资源）；(iii) E1a 的 documented next action（固定 R(C2–N18) 约束松弛→`ts_resume`）本就列为**下一窗口**事项，本窗口只做追记。
- **若主协调要破例，需要写明**：固定距离取值（建议 2.3–2.5 Å）、opt 还是 opt+freq、级别不变（B3LYP/def2SVP+GD3BJ+UltraFine+Tight+CPCM(DMSO)、q0/m1）、资源 ≤8 cpu / ≤10,240 MB / priority 0、产物标 post-freeze asset 且**不得回填 E1a barrier**、不改 §14 口径与交付面。
- **事实复核（我自读）**：ts_0015 `process.json` revision **11** / stage **refine** / blocked **None** / failed_attempt **None**、mtime **2026-10-17 14:36**、`jobs/declaration_0001/` 下仅 `ts_opt/`（无 frequency）⇒ 与 lane1 的 #197「stage 间推进处特定挂起」口径一致，无新证据。
- **不动交付面**：报告 a2964d8d…/277 行、11 文件 sha 未变；E1a/E3a/E3b barrier 均 null。

### §R11.50 裁定登记：主协调**点名授权 1 个 E1a 约束松弛扫描作业**（非 TS/IRC），六项条件已转成 lane1 可执行指令
- **授权（主协调 18:2x CST，主题帖 to as_700f852fe3af412f）**：仅放行 **1 个** `opt=modredundant` 扫描作业（**no freq**），级别不变（B3LYP/def2SVP + GD3BJ + UltraFine + SCF=Tight + CPCM(dmso)）；扫描段 `B 2 18 S 10 0.0500`（**2.6920→2.1920，11 点**）；**禁与 cartesian/z-matrix 混用**；gjf 末尾须留空行。
- **种子**：固定 A 帧 `845a4bd9…`（R(C2–N18) 2.6920 Å）；需换起始距离只能用上一扫描点末帧；**minsep ≥0.90 硬门禁**，不得用碰撞换帧。
- **资源**：≤8 cpus / ≤10,240 MB、priority 0、不重投、不调 priority、不 kill；并发 ≤4（现 1049+1069，加本作业 = 3）。
- **产物与口径**：标 **post-freeze asset / non-delivery evidence**；**E1a barrier 保持 null**、不回填、不改 §14、不动报告 a2964d8d… 与 11 文件 sha。
- **报账**：job id / 输入 sha / route 首行 / running；完成后逐点表 + 选定 guess 帧 xyz sha + 五项距离。
- **判读**：扫描峰**只作 TS 候选/下界、不是 ΔE‡**；l103/NStep 只登记失败类别与行号，不写「通道不存在」；**C2–O3 须保持 1.22–1.28 Å（>1.32 判不合格）**。
- **我补的两条操作提醒（不改变授权范围）**：(i) 每个扫描点的 **minsep ≥0.90** 须逐点断言，任一点靠碰撞达到更短 R(C2–N18) 即该点作废、不得进逐点表；(ii) 该输入为 modredundant，务必保留**文件末尾空行**（缺空行会 l101「End of file in ZSymb」秒退），且**不得**加 cartesian/z-matrix 优化器（l1 会直接拒绝）。
- **先前裁定关系**：§R11.49 的「不授权」在无点名授权的条件下正确；本条为**主协调点名授权后的例外**，范围严格限于上述 1 个扫描作业，不构成对其它提交的放行。

### §R11.51 追记：E1a 点名授权的约束松弛扫描已建 **job 1070**，四项报账经我独立核对成立
- **时刻**：提交/起跑 **2026-10-17T18:24:26**（job 1070）；我独立核对 2026-10-17T18:24:55+08:00。
- **输入**：`HI1/E1/split/E1A_constrained_scan_R2692_2192.gjf`，**38 行 / 1,708 B**、sha256 **`95bbbe6469e97da9a380f6a88782c881cc32892b1e9fc7232e4a37b81b883981`**；`%chk` / `%nproc=8` / `%mem=10GB`。
- **route 首行（我逐字核）**：`#p opt=modredundant B3LYP/def2SVP empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=dmso)` ⇒ 级别未改、**无 freq**（`freq` 关键字计数 0）、未与 cartesian/z-matrix 混用。
- **扫描段与尾部字节（我 od -c 实读）**：坐标块后为 `\n\n B 2 18 S 10 0.0500 \n\n`，**文件以 `\n\n` 结尾** ⇒ 末尾空行门禁满足（l101 风险排除）。
- **种子几何（我自算，27 原子，元素序与 refine 帧一致）**：**R(2,18)=2.6920**、**R(2,3)=1.2383**（羰基在 1.22–1.28 内 ✓）、R(18,27)=1.0349、R(3,27)=2.2993、R(2,4)=1.5071；**minsep 0.9794（13–19，成键 O–H）**；最紧三个非键接触 25–26 1.7726 / 5–6 1.7741 / 9–10 1.7742 ⇒ 无碰撞换距离。
- **种子身份**：授权文写的 `split/E1A_seed_candidate_A.xyz` 在盘不存在（**我复核确认该路径不存在**），lane1 改用**逐字节相同**的 `split/E1a_seed_search/closest_attempt.xyz`，其 sha256 **`845a4bd9908e1607e7ead78d17896912bf2bc874d0310f50bb399fb90e813435`** 与授权 sha 一致 ⇒ 种子身份无歧义，不算偏离授权。
- **资源与并发**：job 1070 **running**、8 cpus / 10,240 MB / priority 0；队列 running **1049 + 1069 + 1070**（并发 3）、free 7 slots / 8 cpus。
- **工具边界（建议报平台，非化学问题）**：lane1 报 `qm_input_writer` **无法直接生成 relaxed-scan 路线**——`task_type=[{"opt":"modredundant"}]+end_setting="B 2 18 S 10 0.0500"` 返回 `internal mismatch: generated file encodes tasks ['relaxed_scan'] but ['minimum_opt'] were requested; no file was written`；`{"scan":"relaxed"}` / `{"scan":"relaxed_scan"}` / `{"opt":"modredundant"}+{"scan":"relaxed_scan"}` 均被拒（"bare scan = RIGID scan"）。其合规绕法：先由 writer 生成 `#p opt` 输入（坐标由工具写、未手写），再仅改两处文本（`opt`→`opt=modredundant`、几何段后追加扫描行并保留末尾空行），坐标块未动——**该绕法在授权范围内（级别与坐标未改），我认可**。
- **口径**：产物标 post-freeze asset / non-delivery evidence；**E1a barrier 保持 null**、不回填、不改 §14、不动报告 a2964d8d… 与 11 文件 sha；扫描峰只作 TS 候选/下界；逐点须 Optimization completed、逐点 minsep ≥0.90、C2–O3 须 1.22–1.28（>1.32 不合格）；l103/NStep 只登记类别 + 行号 + 日志 sha。

### §R11.52 裁定登记：writer 绕法**仅限本件**、不构成先例；工具边界并入平台 issue
- **主协调 2026-10-17T18:26:01 CST 复核六项成立**（输入 sha `95bbbe64…`/38 行、尾部 `\n\n B 2 18 S 10 0.0500 \n\n`、route 逐字、无 freq、%mem=10GB ≤ 10,240 MB；**坐标逐原子 max|Δ| = 0.000000 Å、元素序一致**；种子 sha `845a4bd9…` 与授权一致；几何 R(2,18) 2.6920 / R(2,3) 1.2383 / minsep 0.9794；并发 3、8 cpus / priority 0）。
- **裁定（限本件，不可外推）**：`qm_input_writer` 生成 `#p opt` → 仅改 route 词元（`opt`→`opt=modredundant`）+ 末尾追加扫描行并保留空行、**坐标未动**的绕法**本件认可**；**后续任何 relaxed scan 必须以「writer 原生支持」或「主协调另一份点名授权」为前提**，不得默认复制该绕法。
- **授权文路径勘误（主协调自认）**：授权文写的 `split/E1A_seed_candidate_A.xyz` **不存在**；实际引用一律写 `split/E1a_seed_search/closest_attempt.xyz` + sha `845a4bd9…`。
- **工具边界（并入平台记录）**：`task_type=[{"opt":"modredundant"}]+end_setting="B 2 18 S 10 0.0500"` → `internal mismatch: generated file encodes tasks ['relaxed_scan'] but ['minimum_opt'] were requested; no file was written`；`{"scan":"relaxed"}` / `{"scan":"relaxed_scan"}` 及组合写法均被拒（"bare scan = RIGID scan"）。
- **判读与边界不变**：扫描峰只作 TS 候选/下界非 ΔE‡；每点须 Optimization completed；逐点 minsep ≥0.90（碰撞点作废且不进表）；C2–O3 须 1.22–1.28（>1.32 该点不合格）；l103/NStep 只登记类别 + 行号 + sha；**E1a barrier 保持 null**。

### §R11.53 追记（判读方向改变）：E3b 的 ts_opt（job 1069）**滑到产物侧**，v7 的 2.20 Å 已在鞍点产物侧 ⇒ E3b 鞍点未定位
- **时刻**：lane2 报 2026-10-17T18:31:10 CST；我独立复核 18:31:54+08:00（日志已推进，数值随之微动）。
- **日志**：`ts/ts_0019/jobs/declaration_0001/ts_opt/refine.log` 126,403 → 127,051+ 行（活日志）；Stationary point / Optimization completed / Normal|Error / NStep **均 0 命中 ⇒ 未终态**。
- **末帧几何（我自算，orientation L127011–L127051，恰 41 行）**：**C2–N4 = 3.4020**（P 3.3308）、**C2–O25 = 1.2155**（1.2172）、**N4–H26 = 1.0209**（1.0200）、**O25···H26 = 3.1296**（3.1370）、O10–H27 1.0107、C9–O10 1.3253、C9–O11 1.2119、C2···H26 2.8539；minsep **0.9679（O28–H24，成键对）**；最紧非键 **N4–H27 1.7389** / 12–13 1.7633 / 15–16 1.7718 ⇒ **结构即产物（酮 + 脯氨酸 N–H，两片段）**。
- **能量（同级电子能，只作节点比较）**：E(step133, L125469) = **−939.319785350** ⇒ 相对频率验证的 P（−939.319540184）**−0.000245166 Ha = −0.1538 kcal/mol**、相对 1028 **−0.007158745 Ha = −4.4922 kcal/mol**；其后 L126376 **−939.319793065**（更低，仍下行）⇒ **该帧低于 P 极小点**。
- **判读**：v7 的 **R(C2–N4)=2.20 Å 起点已在鞍点产物侧**，`opt=(TS,calcfc,noeigen)` 沿断键方向下行进入产物盆地 ⇒ 即便收敛也大概率是**产物侧驻点/极小点**，不是 E3b 鞍点；**E3b 鞍点未定位**。终态仍按 band 表判（117 模 + imaginary 行）：若 0 虚频或虚模为转子型 ⇒ 登记「**未找到合格鞍点（本次 attempts 范围内）**」，不写「通道不存在」。
- **两条派生事实（须进后续口径）**：(i) **P 不是该盆地最低点**（存在低 0.154 kcal/mol 的构象/相邻驻点）⇒ 将来 E3b 的 barrier 必须显式声明参照「频率验证的 P」，并说明 P 之上 0.154 的差；(ii) **v7 把 H26 直接挂在 N4（1.05 Å）使 guess 过度产物化**——TS 附近 H26 应在转移中途（N4–H26 ≈1.3–1.5、O25–H26 ≈1.2–1.3），否则 calcfc 初始 Hessian 的最低模即产物侧运动，易下行到产物。
- **候选下一步（需主协调裁定，我不授权）**：(a) 零算力 **v8**：基帧 1028，C2–N4→**1.95 Å**、C2–O25→**1.43 Å**、H26 置于**转移中途**（N4–H26 ≈1.35 / O25–H26 ≈1.25），其余 0 改动；(b) 用已备未提交的 `prep/e3b_scan/hemi_c2n4_scan.gjf`（sha `add74ec7…`）在半缩醛胺自身构象做 C2–N4 受锁扫描、取峰帧作 guess（有算力成本）。
- **口径不变**：E3b result=null、barrier 不回填；v7 与本帧标 post-freeze asset / non-delivery evidence；不重投、不 kill、不调 priority；E3a/ts_0016 不动；交付面 11 文件与报告 a2964d8d… 不动。

### §R11.54 裁定登记：E3b 下一步 = (a) v8，**合并参数版**（取代主协调 §R103 ④ 原数字）
- **裁定（主协调 2026-10-17T18:33:11 CST）**：走 (a)，v8 参数如下（**唯一有效版本**；主协调原 §R103 ④ 的 1.9000 / 1.4091 / H26 留 O25 **作废**）：
  - 基帧 = **频率验证的 1028 末帧**；其余一切 **0 改动**（片段内非反应坐标键长不变、原子序/map 固定、41 原子断言）；
  - **R(C2–N4) = 1.9500 Å**；**R(C2–O25) = 1.4300 Å**；
  - **H26 置于转移中途**：**N4–H26 ≈ 1.350 Å、O25–H26 ≈ 1.250 Å**（用两端点 H26 位置内插/重定位求；两距离须落在 **1.20–1.40** 且 ∠ 合理）；
  - 门禁：**minsep ≥0.90**、每候选帧报**最紧 3 接触**、**无非键接触 <1.20**、**O10–H27 保持 0.9949**（不得顺手转移第二个质子）；
  - 出帧后按 §R94 修订判据验收（除反应坐标外不得塌陷、只出正式帧、evidence_refs 只指真实文件），**再由 lane2 建 ts_prepare**。
- **采纳理由（主协调）**：其原版让 H26 留在 O25，等于把 C–N 断裂与质子转移拆开、起点仍是纯 C–N 拉伸，calcfc 最低模大概率仍是 C–N 方向；把 H26 放到中途才与「C2–N4 断裂 + O25–H26 断裂 + N4–H26 形成」的协同本质一致。
- **派生事实 1 入总口径**：**P 不是该盆地最低点**（存在低约 0.154 kcal/mol 的构象/相邻驻点）⇒ 将来任何 E3b barrier 必须**显式声明参照 = 频率验证的 P（job 1061，41 原子 / 117 模 / 0 虚频）并注明 P 之上约 0.154 的差**。
- **派生事实 2 采纳**：v7 把 H26 直接挂 N4（1.05 Å）是过度产物化的**起点设计问题**（非 opt 参数问题）；责任按设计层记主协调，**执行层无责**。
- **(b) 仍为 fallback**：仅在 v8 也滑落且报批后启用；注意 modredundant 与 writer 的既有坑、以及「仅本件」授权口径。
- **边界不变**：1069 不 kill、盯到终态按 band 表判（0 虚频或转子型虚模 ⇒「未找到合格鞍点（本次 attempts 范围内）」）；E3b result=null、barrier 不回填；v7/v8 与本帧标 post-freeze asset；E3a/ts_0016 不动；交付面不动。

### §R11.55 追记（与 §R11.54 并列）：E3b 已起**第二个 run ts_0020 / job 1071**，用的是**修订前**的 v8 参数；并发达上限 4
- **事实（主协调 18:34:08 CST 报 + 我 18:34:14 独立核对）**：`ts/ts_0020` owner **as_06db52ada5014800**、`process.json` **revision 11 / stage refine / declaration_revision 1 / job_id 1071 / waiting_for job:1071 / blocked null / failed_attempt null**；`path/input_0001/provided.xyz` sha256 **`0a7e43a4a1dd98ca82715bdfe5fbff85434c49301c6be88998fd814c28043f65`**（文件名 `E3B_TS_GUESS_v8_c2n4_1.900_hnou.xyz`）；`jobs/declaration_0001/ts_opt/refine.gjf` sha256 `81c99f86…`、route 同为 `#p opt=(TS,calcfc,noeigen) B3LYP/def2SVP …`。
- **我自算 guess 几何（41 原子）**：**C2–N4 = 1.9000**、**C2–O25 = 1.4090**、**N4–H26 = 3.5675**、**O25–H26 = 0.9693**、O10–H27 = 0.9949、C2···H26 = 1.9828 ⇒ **即 §R103 ④ 初版（H26 仍留在 O25）**，**不是 §R11.54 的 1.9500 / H26 中转版**。作业 started **18:32:58**、running；`refine.log` 1,063 行、`SCF Done` 0。
- **并发**：队列 running **1049 + 1069 + 1070 + 1071**、**free cpus = 0**、free 6 slots / 10,240 MB ⇒ **并发已达上限 4**。
- **处理（主协调裁定，我执行）**：**不 kill**；按 **attempt 2** 登记（时序差，不算违规）；**v8.1 现在不出帧、不建 run**；**任何新提交须等主协调放行**；等 1071 终态 + 出现空槽 + 其裁定后，再决定 v8.1 还是 (b) 扫描兜底。
- **给 lane2 的抑制指令**：在 1071 结束前**不得再出第三个 guess、不得建新 run**。
- **口径不变**：E3b result=null、barrier 不回填；v7/v8/本帧标 post-freeze asset / non-delivery evidence；E3a/ts_0016 不动；交付面 11 文件与报告 a2964d8d… 不动。

### §R11.56 判据澄清登记：C2···H26 ≈1.98 Å 是 **1-3 距离**，不是非键碰撞
- **主协调 2026-10-17 澄清（我采纳）**：ts_0020 的 guess 中 **C2···H26 = 1.9828 Å** 属 **H26–O25–C2 的 1-3 距离**，不是非键接触；按 O25–H26 0.9693、O25–C2 1.4090 反算 **∠(H26–O25–C2) ≈ 108–110°**（sp³ 氧常规角），1.98 Å 是几何必然。
- **判据不变**：minsep ≥0.90、**非键接触（1-4 及更远）≥1.20** ⇒ 该帧两项均通过，**不得因 1.98 判其不合格**。
- **同一读数一致性**：v7 帧的 C2···H26 = 1.9744 同性质，此前亦未据此判不合格；后续报「最紧接触」须**区分成键 / 1-3 / 非键**再判。
- **真正隐忧不变（§R11.55）**：1071 起点把断裂-成键与质子转移拆开（H26 仍全在 O25），calcfc 初始 Hessian 最低模可能仍是单向（C2–N4 或 O25–H26）运动。
- **1071 判读口径（主协调 §R105 ④）**：0 虚频回 1028 侧 ⇒「纯 C–N 拉伸起点滑回反应物侧，未找到鞍点」；1 虚频含 C2–N4 断裂分量 ⇒ 进「1 虚频 + 模矢合格」档（仍非 verified TS）；转子型 ⇒ pseudo-saddle；失败 ⇒ 类别 + 行号 + sha，不写「通道不存在」。、barrier 不回填、交付面 11 文件与报告 a2964d8d… 不动。




























