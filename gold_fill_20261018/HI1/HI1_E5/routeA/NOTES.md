# HI1_E5（E3b）路线 A · A1–A4 补算记录

记录人：molecular specialist（本次执行）　时间基准：本机 date -Is 实测
上游计划：`gold_fill_20261018/HI1/HI1_E5/GRID_PLAN_A.md`（v2，69 行，sha256 728470ccb158f891830aa4886d637508ebdfb435127b3d63e8686ad55bf398b2；v1 为 56 行 / ac9b90cac7e5559b5ba0ce4f0bed592bd2ffd589db463e62a6d13396d4c2ea31，v2 §4.1 已把 maxcycle=400、A3 串行、溯源写进输入头注释三条固化）
上游快照：`gold_fill_20261018/HI1/HI1_E5/GRID_SNAPSHOT.md`（90 行，sha256 0278129523b3ef3341693ee479b296bc8a01887763b50208eb2f0297b16e9979）
只读几何来源：`gold_finish_20261015/HI1/E3/runs/e3b_scan2d_c2n4_o25h26.log`
（sha256 9044f74b2dd8678f69e07b8eeaadc903694070a18d8c644ec400ab8bf5b49cfe，19,577,855 B，303,154 行；本次全程只读，未改写）

## 1 起点几何出处（实测行号，均取该扫描点收敛前的最后一个 Standard orientation 块）

| 抽取件 | 对应扫描点 | 块头行 | 能量行 / E(Ha) | Optimization completed | 实测 R(2,4) / R(25,26) / R(10,27) | sha256 |
|---|---|---|---|---|---|---|
| `_src/src_scan17_conv.xyz` | scan#17 | L288385 | L288593 / -939.245779342082 | L289017 | 2.2248 / 1.4693 / 0.9949 | c07bb225548b3e8c59ca7c9ce54430f0207b166057fa79a51f37ff585992d340 |
| `_src/src_scan7_conv.xyz` | scan#7 | L95956 | L96192 / -939.193490136014 | L96617 | 2.4248 / 1.2193 / 0.9949 | 5bd2333a3f44ad6a96a6ba3557e953e2b578980df9c4b8c1d601058f142cc392 |
| `_src/src_scan6_conv.xyz` | scan#6 | L73766 | L73987 / -939.219797517977 | L74409 | 2.4248 / 0.9693 / 0.9949 | 636ccea5d32a90d1f602421600e45c03507cdffaad71916be538e60a7982fe0c |

每块 41 原子，元素序与原始输入一致：2=C、4=N、10=O、25=O、26=H、27=H ⇒ `B 2 4`=`C2–N4`、`B 25 26`=`O25–H26`、`B 10 27`=`O10–H27`，与计划中的三条约束键一一对应。

## 2 从「帧」到「格点」的显式一步（重要，勿漏读）

取出的三个帧本身的 R(2,4) 并不等于计划格点：scan#17 帧是 2.2248（A1 目标 2.4248），scan#7/scan#6 帧是 2.4248（A2/A4 目标 2.6248）。
`B i j F` 冻结的是**当前**键长，若把帧原样投递，A1 会退化为 scan#17 的重复件。
因此按 Gaussian 扫描协议的既有做法：只沿 C2–N4 轴做刚性位移到计划值（A1/A2/A4 各 0.2 Å；A3 待 A1 收敛后同样 0.2 Å），其余 39 个原子坐标一字未改。
该位移量与目标值已逐字写进每个 .gjf 的头部注释，可核。

## 3 输入文件（4c/6144，maxcycle=400）

公共设置（与 job 1074 一致，仅资源与约束写法不同）：B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight + SCRF=(CPCM,Solvent=DMSO)；route `#p opt=(modredundant,maxcycle=400) ...`；约束 `B 2 4 F` / `B 25 26 F` / `B 10 27 F`；首行 `%nproc=4`、次行 `%mem=6144MB`。

| 格点 | 输入（绝对路径） | 行数 | sha256 | 起点内坐标实测 |
|---|---|---|---|---|
| A1 | /home/ly/Cloudra-mechanism-agent/gold_fill_20261018/HI1/HI1_E5/routeA/A1/A1_opt.gjf | 56 | f0c5656a96b81faf22ee0ce73d905edd6f0bf0ee6d47e9b100dbb5fd1b3f26db | 2.4248 / 1.4693 / 0.9949 |
| A2 | /home/ly/Cloudra-mechanism-agent/gold_fill_20261018/HI1/HI1_E5/routeA/A2/A2_opt.gjf | 56 | a5b5f7bccd337267a2f1a1aa0dd1c3bfa78f4018aecd8d829419227c629d4c38 | 2.6248 / 1.2193 / 0.9949 |
| A4 | /home/ly/Cloudra-mechanism-agent/gold_fill_20261018/HI1/HI1_E5/routeA/A4/A4_opt.gjf | 56 | 4e47aedf5e0140edd7ebb352295103fcb57965bcce1e9935d878c1eda7bbecab | 2.6248 / 0.9693 / 0.9949 |
| A3 | 待建（等 A1 收敛几何） | — | — | 目标 2.6248 / 1.4693 / 0.9949 |

溯源注释写在 #p 行之后的 title/comment 块（不是字面 #p 之前）：Gaussian 的 Link0 段在 `#` 行处结束，其前只允许 `%` 命令；把自由文本放在 #p 之前有触发 Link0 报错的风险。title 块会被 Gaussian 逐字回显到 .log 头部，审计同样可核。

## 3.1 种子帧参考内坐标（收敛后漂移核查用，实测）

| 种子帧 | R(2,25) | R(2,3) | R(4,5) | R(4,8) | R(25,26) | R(10,27) | R(2,4) |
|---|---|---|---|---|---|---|---|
| src_scan17_conv.xyz（A1） | 1.2475 | 1.5086 | 1.2756 | 1.4802 | 1.4693 | 0.9949 | 2.2248 |
| src_scan7_conv.xyz（A2） | 1.2975 | 1.4959 | 1.3833 | 1.4574 | 1.2193 | 0.9949 | 2.4248 |
| src_scan6_conv.xyz（A4） | 1.3345 | 1.4896 | 1.4618 | 1.4455 | 0.9693 | 0.9949 | 2.4248 |

收敛后逐项对照：任一键长漂移 > 0.15 Å、任一原子间距 < 0.9 Å、或被 maxcycle=400 截断 ⇒ 记「没算完」，不当数据、不插值、不用近邻格点补数。

## 4 作业与排产

| 格点 | job id | 提交时状态 | 资源 |
|---|---|---|---|
| A1 | 1096 | ready（排队） | 4c / 6144 MB / priority 0 |
| A2 | 1097 | ready（排队） | 4c / 6144 MB / priority 0 |
| A4 | 1098 | ready（排队） | 4c / 6144 MB / priority 0 |

D20 排产口径：A1 唯一不依赖他人、最先（1096 在本人三个作业中最前）；A2/A4 排在 1093(HL1_E1 freq)/1095(HI1_EM1 ts_opt) 之后。实测队列 FIFO 顺序为
1089(8c) → 1092 → 1093 → 1094 → 1095 → **A1 1096** → A2 1097 → A4 1098，与该口径一致；未为避免排队而重复提交。

## 5 A3 的串行规则

A3 **不得**用 scan#17 帧直接建（那等于 A1 的重复件）。规则：等 A1 收敛 → 取 A1 日志最后一个 Standard orientation 块 → 沿 C2–N4 刚性位移 0.2 Å 到 2.6248（R(25,26) 已由 A1 约束在 1.4693）→ 输入头注释写明「起点 = A1 收敛几何，A1 job id = 1096」→ 单独提交。
A1 若未收敛（含被 maxcycle 截断），A3 不提交。

## 6 判活口径（D20）

1. `/home/ly/g16/scratch/Gau-<pid>.chk` 与 `.rwf` 的 mtime 是否 10 秒级刷新（最强）；
2. 子进程 CPU% > 0 且 STAT = R；
3. 日志 Normal/Error termination 计数为 0；
4. .log 的 mtime 最弱（Gaussian 写缓冲可能一小时不刷）。
不使用 `/proc/<pid>/io`（本机读不到）。不用日志静默判死。

## 7 记账口径（收口不变）

这 4 格是**受约束剖面上的格点**（R(10,27)=0.9949 冻结），只是候选/上界，**永远不得**写成 HI1_E5 的势垒或 ΔE‡。
被 maxcycle 截断的点记「没算完」，不得当数据，也不得用近邻格点补数或插值。
HI1_E5 要有值必须另起 TS 工作流（ts_prepare，guess = scan#7 几何）；在 (c) 齐备前 HI1_E5 gold 保持 null。

## 12 调度终止记录（2026-10-18T04:5x，用户「被换掉的题的任务可以杀了」）

背景：用户 05:0x 指令「被换掉的题的任务可以杀了」，四道替换候选（NR1→甲酰胺、NY3→HNCO、HI1→Cope 消除、HL1→HCNO+降冰片烯），旧题剩余作业停止，32 核让给 N_FORMAMIDE/N_HNCO。HI1_E5 路线 A 的 A1/A2/A4 在停止清单内。

| 格点 | job | 起始 | 终止（ended_at） | 退出码 | 终止时刻日志 | 进度 | 结论 |
|---|---|---|---|---|---|---|---|
| A1 | 1096 | 03:44:32 | 04:54:11 | -15（SIGTERM） | A1_opt.log 1,106,105 B @ 04:53:55 | 17 Step / 17 SCF Done | 没算完 |
| A2 | 1097 | 03:47:01 | 04:54:12 | 137（SIGKILL） | A2_opt.log 950,994 B @ 04:53:35 | 14 Step / 15 SCF Done | 没算完 |
| A4 | 1098 | 03:47:01 | 04:54:12 | 137（SIGKILL） | A4_opt.log 1,007,865 B @ 04:53:58 | 15 Step / 15 SCF Done | 没算完 |
| A3 | — | — | — | — | — | 从未提交 | 随本道取消，永久不提交 |

- 三份日志 Normal termination = 0、Stationary point found = 0 ⇒ **均未收敛**，一律记「没算完」，不得当数据、不得插值、不得用近邻格点补数。
- 平台侧 .cloudra：calc-1096.out.log 记 "Error: software termination"；exit.json 分别为 exit_code -15 / 137 / 137。目录内存在 guard-<id>.lock.adopt_last_spawn，说明终止时平台的 adopt 型 monitor 曾介入（一度出现带 --adopt 参数的 monitor 进程）。
- 归档纪律：所有 .gjf / start_*.xyz / _src / .log / .cloudra 原样保留，未删未覆盖；本文件只追加，不删改历史节。
- 终止方式：本会话没有通用 cancel 工具（ts_stop 仅适用 TS run），因此在 OS 层对 g16 driver + calculator.sh + monitor 发信号，随后用 mark_compute_job_failed 把三个 job 由 running 对账为 failed（reason 已逐条记录）；未重投。
- 释放结果（04:54 实测）：free cpus 0 → 8、free memory 2048 MB → 12,288 MB；N_FORMAMIDE 的 E1/E2/E4 scan 随即起算（在跑 g16 进程均为 N_FORMAMIDE/inputs/*.gjf），本道不再是资源占用方。
- 科学口径不变：本道产出即便曾收敛也只是受约束剖面格点，不是 HI1_E5 势垒；HI1_E5 gold 保持 null。停止前 A1 最后一个 SCF Done = -939.249275526（Step 17 附近）只能作过程记录，不是数据点。

## 11 ΔE 对照框架（2026-10-18T03:58 定稿；勿把 2D 对角差当单轴斜率）

单轴（同一 r_H 行、只动 R(2,4)）：
- **A1**：scan#17 (2.2248, 1.4693) → A1 (2.4248, 1.4693) ⇒ 1.4693 行上随 R(2,4) 拉长的单轴读数。注意 scan#17 的 R(2,4)=**2.2248**（实测该帧 R(2,4)=2.2248；GRID_SNAPSHOT §4 第 17 行；2.4248/1.4693 格在 §2 表中记为「缺（scan#18 未完成）」）⇒ ΔE(A1−scan#17) 预期**不为 0**。
- **A2**：scan#7 (2.4248, 1.2193) → A2 (2.6248, 1.2193) ⇒ 1.2193 行的单轴读数（路线 A 的关键判据：脊顶外延一档是否下降）。
- **A4**：scan#6 (2.4248, 0.9693) → A4 (2.6248, 0.9693) ⇒ 0.9693 行的单轴读数。
跨行（如 A1↔A2）一律标「两坐标同时变，属 2D 对角读数，不是单轴斜率」。
可复现性内部控制：A1 与 scan#17 的共享内坐标（R(2,3)/R(4,5)/R(4,8)/R(2,25)）一致性用于判受约束极小化可复现；**不是**用 ΔE≈0 判。
ΔE 换算：1 Ha = 627.509474 kcal/mol；种子能量 scan#17 −939.245779342082、scan#7 −939.193490136014、scan#6 −939.219797517977。所有 ΔE 均标「受约束剖面读点（R(10,27)=0.9949 冻结），非势垒、非 ΔE‡」。

## 10 起跑实测记录（2026-10-18T03:50 CST）与判终态小坑

- 三格均 running：#1096(A1)、#1097(A2)、#1098(A4)，各 4c。队列实测 running = 1087(8c)/1092/1094/1095/1096/1097/1098，free cpus=0、free mem=0。
- 判活（D20）：scratch 下多个 Gau-*.rwf/.chk 的 mtime 均为 03:50（10 秒级刷新）⇒ 在算。
- title 回显行号（各日志）：title 块起始 **L110**；route 回显 **L85**；%nproc=4 在 **L81**、%mem=6144MB 在 **L83**。
- 约束回显行：A1 L166 / A2 L165 / A4 L164 为 "The following ModRedundant input section has been read:"，其后三行为 `B 2 4 F` / `B 25 26 F` / `B 10 27 F`。
- **小坑**：`grep "Optimization completed"` 会命中 title 块里的溯源文字（L115），不能用作收敛证据。判终态必须用 `Normal termination` + 文件末尾（或 `Stationary point found`）。
- 观察：Gaussian 打印 "Step number 1 out of a maximum of 246"，与输入请求的 maxcycle=400 数值不等（1074 同类打印为 243）。是否截断只按实际 Optimization completed / Normal termination 判定，不据该数字推断。
- A1 第 1 个 SCF Done：E(RB3LYP) = -939.237291020 @ A1 日志 L1053（Step 1）。

## 9 终态单行回报模板（协调者 2026-10-18T03:35 确认，数字一律实测后填，不预填）

`E5-A<n> | converged / 没算完 | #<job> | 缺 X` 后附：
1. 输入实测：绝对路径、行数、sha256；注明第 3 行为 `#p opt=(modredundant,maxcycle=400) …`、末尾三行确为 `B 2 4 F` / `B 25 26 F` / `B 10 27 F`。
2. 日志实测：绝对路径、sha256、字节数、行数；title 块回显的实测行号（须含 sha256 9044f74b… 与来源块行号 L288385 / L95956 / L73766）。
3. 终态证据：Normal/Error termination 计数、`Optimization completed` 行号、最后一个 Standard orientation 块行号与 E；被 maxcycle=400 截断或 SCF 不收敛 ⇒ 如实记「没算完」。
4. 约束保持对照「投递值 → 收敛值」：R(2,4)（A1 目标 2.4248；A2/A4 目标 2.6248）、R(25,26)、R(10,27)。
5. 松弛干净性：R(2,25)/R(2,3)/R(4,5)/R(4,8) 实测值对照 §3.1 基线，漂移 > 0.15 Å 或最小原子间距 < 0.9 Å ⇒ 记「没算完」。
6. A3 首行另加：起点 = A1 收敛几何、A1 job id = 1096、A1 的 E 与行号、A1 日志 sha256。

## 8 已作废的草稿（未提交，无 job id）

第一批 maxcycle=200 的三个 .gjf 草稿（A1/A2/A4）在提交前已删除，从未提交、未产生 job id，按 D20 不留两套并行输入。
