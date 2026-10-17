# HL1 包 STATUS（边：HL1_E1）

包 Coordinator：**as_6bae89a048434b92（接班，18:30）**——前任 as_e9e07289de3d4c62 因平台重启 runtime_interrupted；计算 owner：small_mol **as_d19b16bce0144217**（前任 as_e24133cbb8374c2f failed）；只读复核：explorer **as_1f9af4a22e4640d9**（前任 as_b0db9add78de47e3）。
更新时间：2026-10-15 18:30（SGT）。工作根：/home/ly/Cloudra-mechanism-agent；本包目录：gold_finish_20261015/HL1/。

## 1 边级状态（结论先行）

| 项 | 状态 |
| --- | --- |
| 合格 ΔE‡ 写入题源 | **尚未**（未回填、未改图、未填 0） |
| 声明的 O-质子化 TS1 | **未找到**（截至本行：无 OptTS/IRC 作业；912/913 剖面未出） |
| 声明的 RC 极小值（H3O+···肟，质子仍在 O1） | **未确立**。O-侧种子（O1···O7=2.60 Å、H2 在 O1 0.988 Å）未约束 Opt **自发把质子转到 O7**，落到与产物种子**同一个**极小值 |
| 已确立的极小值 | H2O + O-质子化肟 强氢键复合物（O1···O7=2.457 Å、O7-H8=0.978 Å、H2-O7=1.077 Å、N6-O7=1.554 Å），**0 虚频**，两次独立优化同一驻点 |
| 下一步分岔 | ① 松态 A 种子（O1···O7=3.00 Å）未约束 Opt 若停住 → 走 ts_prepare 找 TS1、交合格 ΔE‡；② 连续滑落（2.60/3.00/3.50/4.20 Å）+ 剖面无内部极大 + ts_prepare 无鞍点 → NO_SADDLE_PACKAGE.md + 选项 A/B/C 裁决请求 |
| R2 状态（18:30 接班轮） | 平台已恢复、提交暂停解除（24 核空闲）；912/913 判定为 **Gaussian 自身报错**（见 §4）；C2_RC3A + A 族递推 + 双齿 + 剖面重设计 + ts_prepare 已整批派给计算 owner as_d19b16bce0144217；只读复核/证据包派给 explorer as_1f9af4a22e4640d9 |

## 2 方法（本包全线统一，引擎偏差必须转述）

Gaussian 16（/home/ly/g16/g16）：B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight，**气相（无 SCRF）**，q=+1、m=1、闭壳层；19 原子 C4H12NO2+。
本机无 ORCA（题源既定口径为 ORCA 6.1.1）→ 程序差异显式登记；能量只在**本批 Gaussian 日志**内相减，不与历史 ORCA（23.13 / 10.44 / 13.46）或旧 Gaussian 0 混减。
参考极小值口径（题面 prompt 逐字）：bimolecular 步的起点极小值 = **RC 反应络合物**，不是分离物种；ΔE‡ 为**纯电子能**（无 ZPE/热校正），627.509474 kcal/mol per Hartree。

## 3 证据（原生日志绝对路径 + sha256，均为本批 Gaussian 16，未改写）

| 角色 | 绝对路径 | sha256 | 结论 |
| --- | --- | --- | --- |
| O-侧 RC 种子 Opt+Freq（job 904） | /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HL1/ts_run/jobs/A_RC_optfreq.log | dd2736788cb8e0fc01914efbf02c91c40408d97bb17e456c354d2a8a621c781e | Normal termination ✓；opt 收敛；51 modes、**0 虚频**；E=-364.2959652889999 Eh（末 SCF Done）；终点 H2 已在 O7（R(2,9)=1.0774）→ RC 种子不是驻点 |
| 产物种子 Opt+Freq（job 905） | .../HL1/ts_run/jobs/A_PC_optfreq.log | f62601ab694362f90183e282e15c9a00bf91826143f4787b3135bd67cc0b5040 | Normal termination ✓；同一驻点（E=-364.29596528700006 Eh，逐原子最大偏差 0.003 Å）；51 modes、0 虚频 |
| 输入 | .../HL1/ts_run/jobs/A_RC_optfreq.gjf | 339108576666454a6eadaa583aff77ee1a66a1db480920756ed61dce06c142ac | 路由逐字：opt freq B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight；1 1；%nproc=12、%mem=13GB |
| 输入 | .../HL1/ts_run/jobs/A_PC_optfreq.gjf | 239bad2a8832713ba86c9d609294ffd46a564b56f854e20fa8d72ba8a3f1ee77 | 同上 |
| 运行记录 | .../HL1/ts_run/NOTES.md | 7a902ae2e6f08dd2984f572732e28c9df4d53f67f4000643d0535035d135764a | owner 原子序、种子构造、假设 H1/H2 |
| 历史与已证伪清单 | .../HL1/HISTORY.md | 03f4305161568a082302d880b602285e929ae1112b5a2d981a158924ab3e8c18 | explorer A 段（含「95/104/105/107 原生日志本地不存在」的真实文件系统核实） |
| 独立只读复核 | .../HL1/AUDIT.md | fc01bf50c8b5b63aa6e67fa1f7822b8ee8199cd8b27631e34e981e6c0aee8363 | explorer B 段 interim（逐条给日志行号） |
| 独立只读复核 2 | .../HL1/AUDIT_B2.md | 2314240fde2064a9b4a3310acfc0061bb5d6f38700b4fed20950b8ba87b02df8 | explorer B 段 interim-2（数字独立复算通过 + 状态口径不一致报告） |

## 4 本包队列表（job_id / cpus / 内存 / 目的）——交付时逐行引用

| job | cpus/内存 | 输入 | 目的 | 状态 |
| --- | --- | --- | --- | --- |
| 904 | 12c/13GB | jobs/A_RC_optfreq.gjf | O-侧 RC 种子 Opt+Freq | **done**（证据见 §3） |
| 905 | 12c/13GB | jobs/A_PC_optfreq.gjf | 产物种子 Opt+Freq | **done**（证据见 §3） |
| 912 | 12c/13GB | jobs/B_sepscan_OO.gjf | 松弛扫 d(O1···O7) 2.457→3.457 Å（20 步 +0.05） | **failed（Gaussian 自身）**：前 10 点收敛、逐点单调上坡 0→+6.42 kcal/mol、**无内部极大、无第二极小值**；第 11 点 NStep=88 耗尽 → l9999 终止（17:33:42）。日志 sha256 `89a0bdad76c805e36b025848a3723b74c14c119498e8da540d495401981e23df`（本 Coordinator 实测，补上前轮缺失的 hash） |
| 913 | 12c/13GB | jobs/B_ptscan_frozenOO.gjf | 冻结 O···O=3.00 Å 扫 d(O1-H2) 0.988→2.188 Å（12 步 +0.1） | **failed（Gaussian 自身）**：scan point 1 即 `Error imposing constraints` → l103 终止（17:35:18），**零可用扫描点**；冗余坐标/约束构建失败，非 SCF 崩溃。日志 sha256 `6fecdc7ef0e3c016020677d6eae99171a278e274239ee7b70a87c7e8d2fb7c03` |
| 待提（8c/10GB） | 8c/10GB | jobs/C2_RC3A_optfreq.gjf | **决胜**：O1···O7=3.00 Å 的 A 种子未约束 Opt+Freq | 暂停已解除；18:3x 由 R2 计算 owner as_d19b16bce0144217 提交（job 号待其回帖） |
| 待提 | 8c/10GB | jobs/C2_sideN_optfreq.gjf | N 侧竞争通道（可选） | 同上 |
| 待提 | 需改 8c/10GB | jobs/D_H3O_optfreq.gjf、D_oxime_optfreq.gjf | 分离态单体参考 | 同上 |

归属更正：908/910=HI1、909/914=NI5、911=NR1（非本包，不认领）。
状态口径纪律：queued 与 running 严格分开；未产出日志不得当证据。

## 5 已证伪 / 已撤回（引自 HISTORY.md，本包不重复劳动）

- 已撤回：HL1_E1 barrier=0（旧 Gaussian/WSL 13 点约束扫描，「candidate barrierless」）；旧 0 不得回填。
- 已证伪：把 job 531（−1791.63 cm⁻¹）当作 E1 的 O-质子化 TS——它是肟自身 O5→N4 分子内 PT，位移 99% 在 H18。
- 未验收：95（RC Opt 撞 MaxIter）、104/105（path 准备无候选）、107（第 9 点未收敛 + SHARK 读临时输入失败，据记录终点在 N 侧；**本地无其输入与日志，扫描坐标/约束不足以确证**）。
- 仍有效：E1 的化学定义与参考极小值口径；E1 现值 null（open）；「107 只能否定它那条路线，不能证明 O 路线无鞍点」。

## 6 阻塞与待裁决

- 平台阻塞**已解除**（主协调 17:20 恢复记录：compute.db 可写、integrity_check=ok、scheduler adopt 收尾；17:44 起队列恢复流动）。本包 912/913 是**在平台恢复之后真实运行并以 Gaussian 自身报错终止**（912 l9999 / 913 l103，见 §4），**不是平台故障**。
- 待裁决（仅在证实无鞍点后提交）：E1 的三选一 —— 选项 A：记 0.0（PT 前平衡/无鞍点/RC 非驻点）+ caveat（库内先例：normal_registry/yo.py 的 O3 第 1 步 carbonyl O protonation by hydronium = 0.0；同题第 4 步 PT=0.332）；选项 B：申请该边豁免（参照既有 PT 豁免边）；选项 C：改图（合并/调整节点与边）。**裁决前不写值、不改图。**

## 7 新线索（**假设，非证据**）：双齿氢鎓 RC 可能是真正的起点极小值

来源：gold_compute/edge_barriers/computed/HL1.json（旧 Gaussian16/WSL 记录，sha256 e9d456f338e93f1442219d13e42a4c74eebff94db535cc826cc032befca52e39）。**该文件与其中的 0 已作废、不引用其数值**；只借用其几何思路。
- 它自述找到过 0 虚频的 R 极小值，结构为**双齿氢鎓**（hydronium 同时向肟 O 与 N 供氢；逐字 O1-H16···O8 1.447 + O1-H3···N7 1.898，“proton on water”），E=-364.26678667 Eh。
- 同时它记录：**朴素（单齿）种子自由优化会直接落到 O-质子化或 N-质子化组成** —— 与本批 904 的观测完全一致（我们的 seedB 是单齿 pose，H2···N6=2.70 Å）。
- 推论（待验证）：**用第二个氢键把氢鎓锁住的“双齿/螯合”pose 才可能是真正的 RC 极小值**。若成立，则 E1 的参考极小值存在，TS1 可搜，ΔE‡ 可给。
- 已在做：owner 构造 RC_bi（H2→O7 ≈1.45–1.60 Å，另一个氢→N6 ≈1.85–2.00 Å，O1···O7 ≈2.60–2.75 Å）+ 未约束 Opt+Freq（8c/10GB）；平台故障期间先构造不提交。
- 级别不可比警示：旧记录的 I1 = -364.2735 比本批 O-质子化极小值 -364.2960 高约 14 kcal/mol，说明级别/构象不同 → **一切数值只用本批同级别日志**。

## 8 R2（接班轮，18:30）执行清单与判据

**已派实验（计算 owner as_d19b16bce0144217）**
| # | 实验 | 判据 | 现状 |
| --- | --- | --- | --- |
| T1 | **job 920**（8c/10240MB，18:09:01→18:13:43）：jobs/C2_RC3A_optfreq.gjf（A 族，d(O1···O9)=3.00 Å，H2 在 O1）未约束 Opt+Freq | 停住（0 虚频、R(1,2)≈0.97–1.05、R(2,9)≥1.4）→ RC 极小值存在 → 转 T4；滑落 → 坍缩证据 | **结果 = 坍缩**：Normal termination（18:13:43）、opt 收敛、51 modes **0 虚频**（最低 27.1292）、E=−364.295965302 Eh、末帧 R(1,2)=1.3810 / R(2,9)=1.0774 / R(1,9)=2.4568 → **与 904/905 同一 B 极小值**（H2O+O-质子化肟）。日志 `…/ts_run/jobs/C2_RC3A_optfreq.log`，21343 行，sha256 `01c7b36f48170832a44652217c1796242969fd95befe3137413e08650f11c559`（中途快照 sha a166dd16… 已作废，以本终值 sha 为准） |
| T3a | **job 921**（8c/10240MB，18:09:14→18:20:46）：jobs/T3a_ptscan_O1H2.gjf（`B 1 2 S 20 0.050` = 松弛扫 d(O1–H2) 0.988→2.088 Å，O1···O9 自由），输入 sha256 645d280c… | 逐点 E + 有无内部极大 | **failed（Gaussian 自身）**：18:20:46 l103 终止，逐字 `Tors failed for dihedral 3-1-9-16 / 4-1-9-16`、`FormBX had a problem.`（Berny 冗余坐标系崩坏）。日志 `…/ts_run/jobs/T3a_ptscan_O1H2.log`，12261 行 → **不能作为任何能垒/无垒证据，仅作重设计输入**。⚠ 崩坏前中间帧出现 **H3–N8=1.211 Å（H3 迁到 N8）**、几何 = H2O + N-质子化肟，SCF 已到 **−364.301672236 Eh**（低于 O-质子化络合物 −364.295965 约 3.6 kcal/mol）→ 已列为 N 侧驻点核身份任务（见 §10） |
| T3b | **job 930**（8c/10240MB，≈18:16→18:27:59）：jobs/T3b_sepscan_OO_in.gjf（O···O 反向递减 18×−0.1），输入 sha256 见 owner 帖 | 长程剖面有无第二极小值 | **failed（Gaussian 自身）**：18:27:59 l9999，逐字 `Optimization stopped. / -- Number of steps exceeded,  NStep=  88` @ scan point **1/19**（同 912 模式）。日志 `…/ts_run/jobs/T3b_sepscan_OO_in.log`，52382 行 |
| T2 | E2_RC35A（3.50 Å）/ E2_RC42A（4.20 Å）/ E2_RCbi（双齿螯合）未约束 Opt+Freq；可选 E2_H3O / E2_oxime 单体 | 任一停住 → RC 存在；全滑落 → 支持「无 RC 极小值」 | 已派，串行 ≤2 并发 |
| T3 | 剖面重设计（逐项留证：坐标/步长/有无内部极大/是否试过其它 PT 通道）：单坐标 PT 剖面 + ≥4–5 Å 长程剖面（912 只到 3.4 Å），必要时二维网格 | 逐点 E + 明确「有无内部极大」 | 已派 |
| T4 | ts_prepare（provided guess；含 freq+IRC+两端端点 Opt/Freq） | run_id/revision/status/result.outcome 原文留证；**即使无候选峰也必须跑一次** | 已派 |

**只读复核（explorer as_1f9af4a22e4640d9）**：独立复核 904/905/912/913；整理 (a) 坍缩起终点对比 (b) 完整剖面 (c) B 极小值身份 (d) ts_prepare 原文；逐项列验收链缺口。

## 9 R2 首批结果（18:15，Coordinator 自核，仅用本批日志）

- **T1（C2_RC3A，job 920）＝ 坍缩**：O1···O9=3.00 Å 的 O-侧松态种子（H2 原在 O1）未约束 Opt+Freq **不停顿地滑到 B 极小值**（与 904/905 同一驻点：R(1,2)=1.3810、R(2,9)=1.0774、R(1,9)=2.4568；E=−364.295965302 Eh；51 modes、0 虚频）。→ 「RC 极小值存在」的路线 (i) **在本距离下被否定**；O-侧 A 种子的坍缩距离已扩到 2.60 → 3.00 Å。
- 待续：E2_RC35A（3.50 Å）/ E2_RC42A（4.20 Å）/ E2_RCbi（双齿）；T3a/T3c 单坐标 PT 剖面；T3b 长程剖面（≥4.96 Å）；T3d N 侧 / T3e 另一氢通道；最后 ts_prepare。
- 纪律提醒：job 920 的中途快照 sha（a166dd16…）只在巡检帖里出现过一次，**对外引用一律用终值 sha** 01c7b36f48170832a44652217c1796242969fd95befe3137413e08650f11c559。
- **判据更正（18:19，回应主协调 18:1x 巡检）**：主协调据「2×Normal termination + 51 频率全正 + E 落回 −364.295965」判为「停住 ⇒ RC 极小值存在」；本包以同一日志的**几何**证据更正为**坍缩**——起始帧（L341，=输入 3.00 Å A 种子）R(1,2)=0.988 / R(2,9)=2.012 / R(1,9)=3.000；37 帧单向轨迹；末帧（L18643/L19178）R(1,2)=1.381 / R(2,9)=1.077 / R(1,9)=2.457；与 A_PC（L12213）1.3810/1.0774/2.4568、A_RC（L15861）1.3812/1.0774/2.4569 **同一驻点**。
- **判别式（写入交付）**：看收敛驻点中质子归属——R(1,2) ≤ ~1.05 Å 且 R(2,9) ≥ ~1.4 Å = RC 型（参考极小值）；R(1,2) ≈ 1.38 / R(2,9) ≈ 1.08 = 产物侧络合物（本批 904/905/920）。**A/B/C 三选项不降级**，仅在没有合格 TS 时启用；仍不写 0.0、不改图。已发 hub 帖 evt_b8476a2f73c9440e。

## 10 R2 第二批（18:28）：两个重设计剖面都失败 + 一条 N 侧线索

**失败（均为 Gaussian 自身报错，非平台）**
- job 921（T3a，扫 d(O1–H2)、O···O 自由）：l103 `Tors failed for dihedral 3-1-9-16 / 4-1-9-16` + `FormBX had a problem.` → **Berny 冗余坐标系崩坏**（把 O1–H2 拉大而其余全自由时，体系跑到别的质子化态，坐标系退化）。
- job 930（T3b_in，O···O 反向递减）：l9999 `Number of steps exceeded, NStep= 88` @ scan point 1/19 → **步数耗尽**。
→ 两条剖面都**不进证据**；已按「逐项留证」要求登记扫描坐标/步长/失败机制/是否试过其它通道。

**线索（未收敛中间帧，不是结论）**：T3a 崩坏前最后几帧 = **H2O（O1 带 H2 0.984 Å、H4 0.974 Å）+ N-质子化肟（H3–N8 = 1.211 Å，R(9,16)=0.973）**，SCF 原文 `SCF Done: E(RB3LYP) = −364.301672236 A.U.`（L12194 附近）→ 比已确立的 O-质子化络合物（−364.295965）**低约 3.6 kcal/mol**。若经 Opt+Freq 证实为驻点，则 N 侧产物优于 O 侧（与历史「证据指向 N 侧」一致），将成为选项 C（改图）的实测证据。**在拿到 0 虚频 + 频率 + 身份前不作结论、不改图。**

**改道（已下发给 owner，按优先级）**：A) 立刻 T4 ts_prepare（质子居中 guess + 真实 provenance 文件；freq+IRC 双向+两端端点；无论如何跑一次取「无鞍点」原文）→ B) N 侧驻点 Opt+Freq 核身份 → C) 剖面稳健重设计（二维网格 / 分段短扫描 / 按点冻结独立作业 / xTB 二维面图喂 ts_prepare 的 xtb_path guess，至少一条并说明理由）→ D) A 族 3.50/4.20 Å + 双齿。

**912/913 失败机制（供「搜索是否充分」答辩）**：912 是「扫描点未收敛 + 原生步数耗尽」，不是扫描坐标错误；913 是「冗余坐标/约束构建失败（l103 Error imposing constraints）」，需更换约束构造方式而非放弃扫描目标。二者**均不能**作为「无鞍点」的证据，只作为重设计的输入。

## 11 R3（第三任 Coordinator **as_0cbe3c2ee0ed460d**，22:58 接班；前任 as_6bae89a048434b92 于平台重启被收尾为 failed）

**起点盘点（真实文件系统读，非二手）**：本包计算作业止于 18:35（921/930 由 adopt 收尾）；ts_run/jobs 下无 18:35 之后的新日志 → 前任 R2 派出的 T2（3.50/4.20/双齿）与 T4（ts_prepare）**均未实际落盘**。队列快照（22:58）：全节点仅 1 个 running = **963（HI1 包，8c）**，free 24c / 9 槽；本包当时 0 作业。故本轮从 T2/T4 接续，**不重复** 904/905/920 与 912/913/921/930 的任何计算。

**本 Coordinator 独立复核（本轮用 log_parser/log 实读，sha 由 sha256sum 实算）**

| 日志（前缀 = `gold_finish_20261015/HL1/ts_run/jobs/`） | sha256 | 末 SCF Done / Ha | 模数 | 虚频 | Normal | opt |
| --- | --- | --- | --- | --- | --- | --- |
| A_RC_optfreq.log（904） | dd273678…c781e | -364.295965289 | 51 | 0（min 27.18） | ✓ | ✓ |
| A_PC_optfreq.log（905） | f62601ab…b5040 | -364.295965287 | 51 | 0（min 27.17） | ✓ | ✓ |
| C2_RC3A_optfreq.log（920） | 01c7b36f…c559 | -364.295965302 | 51 | 0（min 27.13） | ✓ | ✓ |
| B_sepscan_OO.log（912） | 89a0bdad…e23df | 扫描，无内峰 | — | — | ✗ | l9999 第 11 点 |
| B_ptscan_frozenOO.log（913） | 6fecdc7e…b7c03 | 零可用点 | — | — | ✗ | l103（point 1） |
| T3a_ptscan_O1H2.log（921） | 22dd89f4…9d67e | 扫描 | — | — | ✗ | l103 FormBX |
| T3b_sepscan_OO_in.log（930） | d739912b…bf4218 | 扫描 | — | — | ✗ | l9999（point 1） |
| A_RC_last.xyz（产物极小值末帧） | 303ec8b4…b5afe6 | — | — | — | — | 几何 |

→ 904/905/920 三者是**同一驻点**（ΔE ≤ 1.3×10⁻⁸ Ha ≈ 8×10⁻⁶ kcal/mol），**0 虚频**；几何判据（前任 R2 自核 + 主协调独立复核，见 LEDGER 18:2x）：R(1,2)=1.381 / R(2,9)=1.077 / R(1,9)=2.457 Å ⇒ 质子已在肟 O 上 = **产物侧络合物 B，不是声明的 RC**（T1 = 坍缩，判据不降级）。

**本轮已派道（subagent_launcher 新会话，均为本包 lane）**

| lane | session_id | 任务 | 期望产出 |
| --- | --- | --- | --- |
| CALC2（small_mol，手工作业 owner） | as_89da86aa3fc54ff5 | ① E2_RCbi 双齿未约束 Opt+Freq ② E2_RC35A（3.50 Å）③ E2_RC42A（4.20 Å）④ 921 中间帧 N 侧几何未约束 Opt+Freq 核身份 ⑤ T3c 反向剖面 d(H2–O9) | HL1/round3/CALC2_REPORT.md（逐作业 job_id/日志 sha256/频率/能量/末态 R 值/行号） |
| TS（small_mol，TS 管线 owner） | as_6ede162e1cc94641 | ts_prepare（provided guess = t4_interp/img_06.xyz，evidence_refs = prep/TS1_guess_provenance.md 等）；freq + IRC 双向 + 两端端点 Opt/Freq；gaussian B3LYP/def2-SVP + EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight | HL1/round3/TS_RUN_REPORT.md（run_id / process.json / result.outcome 原文） |
| EXPLORER（只读） | as_0c20c4751ebc4ca0 | 独立复核 904/905/920/912/913/921/930 + 搜索充分性清单 + 验收链缺口清单（与 AUDIT.md / AUDIT_B2.md / AUDIT_B3.md 去重） | 回报正文（explorer 无写权限，由 Coordinator 落盘） |

已把 **registry 原文 SMILES** 补给 TS 道（避免自造物种声明）：reactant = L1 的 mapped_reactants 原文；product = L1 第 1 步 out 原文 `[O:1]([H:9])[H:10].[CH3:11][CH2:5]/[C:4](=[N:6]/[O+:7]([H:8])[H:2])/[CH3:3]`；reaction_center [[1,2],[2,9]]（本序）。配额：本包手工作业 ≤2 并发（8c/10GB/priority 0），ts_prepare 自动作业不占配额。

**缺失证据（截至 22:5x）**
1. 合格 ΔE‡：**无**（无 TS、无 IRC 双向、无端点 Opt+Freq 对）。
2. ts_prepare 的 run_id / process.json / result.outcome 原文：**无**（本轮首次尝试）。
3. 「A 形（质子留 O1）RC 极小值」：2.60 Å 与 3.00 Å **已证伪（坍缩）**；3.50 / 4.20 Å 与双齿螯合 = 本轮在算。
4. N 侧驻点身份（未收敛帧候选 E=-364.301672236 Ha，比 B 低约 3.6 kcal/mol）：**未确立**，本轮在算。
5. 完整剖面有无内部极大：912 前 10 点单调上坡无内峰（但不覆盖 >2.96 Å）；913/921/930 全部失败 ⇒ **不能作为「无鞍点」证据**；反向剖面本轮在算。

**下一步判据（判据不变，裁决前不写值、不改 jl.py、不改图）**
- 任一 A 形种子**停住**（0 虚频 + R(1,2) ≤ ~1.05 Å 且 R(2,9) ≥ ~1.4 Å）⇒ RC 极小值成立 ⇒ 以该几何作参照重估 ΔE‡，再谈回填。
- 全部 A 形种子**坍缩** + 双向剖面**无内峰** + ts_prepare outcome=search_failed/无峰 ⇒ 出 `NO_SADDLE_PACKAGE.md`（起点/终点几何对比 + 完整剖面 + 极小值身份核验 + ts_prepare 原文 + 搜索充分性逐项留证）+ A/B/C 裁决请求（A 记 0.0+caveat（先例 normal_registry/yo.py O3 第 1 步）/ B 申请豁免 / C 改图，并把 N 侧驻点实测身份作为 C 的补充证据）。

**阻塞**：无平台阻塞（队列 1 running；本节点 24c 空闲）。引擎偏差（Gaussian 16 替代题源既定 ORCA 6.1.1）继续在交付中逐条声明；本包能量只在本批 Gaussian 日志内相减。

## 12 R3 · 政策更新落地（主协调 2026-10-15，BRIEF §9；本包回复帖 evt_d35e20c39be14618）

主协调广播 evt_8d124365e7e345cb：**题源参考图与既有 gold 值不具权威性**；证据支持更好机理时按证据选（可改参考态、改质子化位点/通道、拆步或合并节点与边、替换身份可疑旧值），但必须同批原生日志 + sha256 + 行号、同程序同批相减、驻点虚频与身份核验、写明改了什么/依据/与旧图差别/影响哪些边；有鞍点的验收链（恰 1 虚频 + 模式归属 + 双向 IRC + 两端 0 虚频身份）不变；**无合格鞍点不是失败**（可记无独立鞍点 + 替代口径，不得凭空填数）；交付单列「证据驱动的机理修订」。

HL1_E1 落地口径（包内自行决定，仅跨包/改别人包才上报）：
1. **O 侧 vs N 侧**以 CALC2 实测为准：N 侧络合物若 0 虚频且能量更低，则它是更好的机理 → 写成独立节点/边并说明化学差别（N-质子化肟不是 Beckmann 的离去基团活化态，不导向迁移）；O 侧 B（-364.2959653 Ha，0 虚频，本批三点同一驻点）仍是已证实的真实极小值。
2. **ts_prepare 仍按声明的 O-质子化步骤跑一次**（不因机理可能改判而跳过），留 run_id / process.json / result.outcome 原文。
3. 若「全部 A 形种子坍缩 + 双向剖面无内峰 + ts_prepare 无峰」成立 → 以 **0.0 + caveat（无独立鞍点 / 无垒离子-分子质子转移）** 口径回填（先例 normal_registry/yo.py O3 第 1 步 = 0.0），并同时给替代口径（RC 非驻点 ⇒ 参考态重定为离子-分子对/产物侧极小值）。
4. 回填面：`cloudra/benchmark/hard_registry/jl.py` 的 L1 第 1 步 barrier + `ideapool/reaction_candidates/hard.md` 的 L1 行（实读确认第 145 行；现行文字含「E1 保持 null」）+ 生成器重跑 + `pytest tests/test_benchmark.py -k regenerate_identically` 原样粘贴。**裁决前不写值、不改图。**

## 13 R3 第二批（23:19–23:20 终态；本 Coordinator 独立核验：log_parser 实读 + 自行由 xyz 逐原子算距离）

| job | 输入（sha256） | 原生日志（sha256） | E / Ha | 模数 / 虚频 | 末态 R(1,2) / R(2,9) / R(1,9) Å | 判定 |
| --- | --- | --- | --- | --- | --- | --- |
| 965 | E2_RCbi_optfreq.gjf 6ab9b94e… | E2_RCbi_optfreq.log a4d18247… | -364.295965301 | 51 / 0（min 27.08） | 1.3811 / 1.0774 / 2.4568 | **坍缩到 B**（与 904/905/920 同一驻点，Δ ≤ 1.2×10⁻⁸ Ha） |
| 966 | E2_RC35A_optfreq.gjf 5748a445… | E2_RC35A_optfreq.log 48da3dcb… | -364.295777129 | 51 / 0（min 27.53） | 1.3878 / 1.0740 / 2.4601 | **坍缩**（质子已在 O7；比 B 高 0.118 kcal/mol，同一质子化态的另一构象） |

末帧文件：round3/E2_RCbi_final.xyz sha256 cb1559ea…、round3/E2_RC35A_final.xyz sha256 e2fc5c07…（坐标未改）。

⇒ **A 形（质子留 O1）在本级别气相已用 4 个独立种子全部证伪**：2.60 Å（904/905）、3.00 Å（920）、3.50 Å（966）单齿 + 双齿螯合（965）。两处坍缩终点 R(2,8) = 2.073 / 2.079 Å（质子不指向 N8）⇒ 终点是 **O-质子化络合物**，不是 N 侧。

**CALC2 已备好、待跑（下一批）**：E2_RC42A_optfreq.gjf（输入 sha256 ec9dcdc5…）；N_side_optfreq.gjf（sha256 0ff3f55d…，种子由 format_converter 从 T3a 原生日志导出：ts_run/prep/N_side_frame_from_T3a.xyz sha256 dfacf479…，对应 SCF 行 T3a_ptscan_O1H2.log:12194 E = -364.301672236 Ha）；随后 T3c 反向剖面。**CALC2 更正（重要）**：该帧实测 R(1,3)=1.2077、R(3,8)=1.2184 Å ⇒ H3 夹在 O1 与 N8 之间，是**未收敛桥式中间帧、不是 N 侧驻点证据**（我复核 965/966 末帧亦未见 N 侧迹象）；其驻点身份只能由 N_side_optfreq 的 Opt+Freq 判定。

**TS 道（T4）进展**：已用 NR1 的 ts_0005 反推平台「具体原子序」规则（组分内先重原子、再按母原子顺序追加 H），并在 ts_0005 上逐位重现其 atom_map；据此给出本包 reactant 具体序（1=O1, 2-4=H(O1), 5=C11, 6=C5, 7=C4, 8=N6, 9=O7, 10=C3, 11-13=H(C11), 14-15=H(C5), 16=H8(O7), 17-19=H(C3)，与 guess img_06.xyz 逐位一致）与 product→reactant atom_map [1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,2,17,18,19]；另落盘 product_endpoint_seed_B_prodorder.xyz（A_RC_last.xyz 纯行置换，坐标未改；我实测 R(O7–H2)=1.0774、R(O7–H8)=0.9779、R(O1···O7)=2.4569 与原件一致）。证据文件 round3/T4_INPUT_ORDER_PROVENANCE.md sha256 a97f0467…（引用 NR1 ts_0005/process.json sha 19140d1b…）。**ts_000X run 尚未创建**（23:30 快照：ts_0007=NY3、ts_0008/ts_0009=HI1）。

## 14 R3 第三批：explorer 独立复核终版（已落盘）+ 两处结论降级（重要）

- 落盘文件：round3/EXPLORER_R3_INDEPENDENT_VERIFY.md，sha256 **2bf40d42…914df71**（正文 = explorer 会话 as_0c20c4751ebc4ca0 在主题 gold-finish-20261015 的终版帖 evt_7f57430b6bd7474f 逐字；explorer 无 write 权限，由本 Coordinator 落盘）。explorer 复算的 sha 与我一致：A_RC dd273678…、A_PC f62601ab…、C2_RC3A 01c7b36f…、B_sepscan_OO 89a0bdad…、B_ptscan_frozenOO 6fecdc7e…、T3a 22dd89f4…；**T3b（930）它无法自证（>2 MB 读取上限 + 无 sha256sum 权限）→ 本 Coordinator 已用 sha256sum 实测 d739912b0b3b6d187576bbf22319443dd2bb324fba38a80ad8d13af99bbf4218**。
- 同一驻点 B 再获独立佐证：末帧逐原子最大偏差 A_RC↔A_PC 0.0031 Å、A_RC↔C2 0.0015 Å、A_PC↔C2 0.0019 Å；能量极差 1.3×10⁻⁸ Ha；51 模 0 虚频（最低实频 27.1816/27.1707/27.1292 cm⁻¹，Low-frequencies 首值 ≈ -4.9 cm⁻¹ 为投影平动转动残值，不计虚频）。

**(降级 1) 912 剖面的解释力作废重述**：explorer 实测 912 的 **scan point 1 几何就是 B 极小值本身**（L1877 R(1,2)=1.3812、L1881 R(2,9)=1.0774），逐点 R(1,2) 由 1.3812（pt1）单调增到 1.8877（pt10）、1.9412（失败点），质子**始终在 O9** ⇒ 该剖面是 **B 复合物沿 O1···O9 拉长的解离曲线**，**不是声明步（O1→O9 质子转移）的反应坐标**。因此「912 前 10 点单调上坡、无内峰」**不能**用来支持「O-质子化无鞍点」（它连声明步的反应坐标都不是）；此前 §11/§13 的相关表述按本行降级。

**(降级 2) N 侧 3.58 kcal/mol 降级为上界**：921 的 N 侧桥式帧出自**约束扫描**（B 1 2 被约束在 ~0.99 Å）且**未收敛**（全日志 0 个 Optimization completed、0 个频率计算）⇒ E = -364.301672236 Ha 只能读作「N 侧极小值 ≤ 该值」的**上界**，**不是**合法驻点间能量差（既有 NOTES 的 ~2.0 / 3.6 kcal/mol 同此降级）。N 侧驻点身份仍只能由 N_side_optfreq（未约束 Opt+Freq）判定（截至 23:40 无 .log）。

**搜索充分性（explorer 独立复核，成立）**：四个失败剖面（912/913/921/930）都**不具备最低条件**（扫描点全收敛 + 覆盖声明步两端）：912 起点即 B 且第 11 点 NStep 耗尽；913 零收敛点（l103 Error imposing constraints，且无 FormBX/Tors 报错，机制与 921 不同）；921 零收敛点（Tors failed 3-1-9-16 / 4-1-9-16 + FormBX）；930 零收敛点（单点 88 步耗尽，能量在 -364.2616/-364.2623 Ha 间往复 ≈0.45 kcal/mol、O···O 几乎未动）。⇒ 四者均**不能**作为「无鞍点」证据。
**921 轨迹的正确读法**（explorer 逐帧）：H3 从 O1 侧连续移向 N8（R(1,3)/R(3,8)：1.1096/1.4066 → 1.1231/1.3798 → 1.1242/1.3781 → 1.2067/1.2193 → 1.2077/1.2184 → 末块 1.2123/1.2111 桥式），而 H2 始终留在 O1（0.9877→0.9838）。导出文件 prep/N_side_frame_from_T3a.xyz 对应倒数第二个 SO 块（@L10998），不是最后一块（登记为 provenance 细节：两帧同一迁移趋势，不构成冲突）。
**920 逐帧轨迹（explorer 自算 38 帧）**：R(1,2) 帧1→18 单向 0.9877→1.3834，帧18→38 在 1.362–1.383 间小振幅收敛 ⇒ 正确表述是「单向迁移 + 落点附近小振幅收敛」，**不是严格单调**（此前 §11 的「37 帧单向」按本行修正）。
## 15 R3 第四批（23:40–23:45）：explorer 续帖落盘 · 平台写锁已解 · 收口材料包 v1

- explorer 终版**续帖（§5–§10）**已落盘：round3/EXPLORER_R3_INDEPENDENT_VERIFY_part2.md（sha256 a64691e5…；正文 = 帖 evt_74ecf69f2b3c48d3 逐字）。要点：
  - **搜索尚未穷尽**（explorer 独立结论，与我一致）：4.20 Å 种子**从未运行**（无 .log）；T3c（反向 H2–O9）、T3d（H2→N8）、T3e（H3–O9）**只有输入无结果**；**HL1 一次真实 TS 搜索都没做**（ts/ts_0001–ts_0009 无任何 HL1 run，ts_0007 实读为 NY3）⇒ 现在**不能**宣布「无鞍点」。
  - **产物侧不是一个点**：除 B（-364.295965289/-287/-302，三日志同一驻点）外，3.50 Å 种子落到 **B' = -364.295777129 Ha（0 虚频，51 模，最低实频 27.5308 cm⁻¹）**，比 B 高 **0.118 kcal/mol** ⇒ 机理/参考态描述须写清用哪一个（B 或 B'）。
  - explorer 独立复核 965/966：2×Normal termination、51 模 0 虚频、末 SCF -364.295777129 / -364.295965301、末帧 1.3878/1.0740/2.4601 与 1.3811/1.0774/2.4568（@L27675 / @L31029），与我的数值一致。
  - explorer 独立复核 product_endpoint_seed_B_prodorder.xyz：按声明的置换逐行比对，**坐标最大偏差 0.000 Å、元素序列一致**（「只做行置换」成立）。
  - 工具面（供 issue）：explorer 无 write、bash 无哈希命令 ⇒ **>2 MB 日志（930）本角色无法自算 sha256**（本 Coordinator 已代算）；无 query_compute_queue；read/bash 结果分别在约 28 KB / 4000 字符处截断。
- **平台写锁已解除（23:41）**：965/966 行由 running 正确收尾为 **done**（ended_at 23:41:20），队列恢复流动（running = 967 NY3 ts_0007 / 968 HI1 ts_0008，均 23:41:21 起；queued = 971–975）。我未做任何平台处置（只读取证 + 上报，见帖 evt_77cfc31850924fd6）。
- 收口材料包 v1 已落盘：**NO_SADDLE_PACKAGE.md**（sha256 b2da19a9…）——§1–§9 含声明口径、起点证伪表、极小值身份、四剖面解释力边界、搜索充分性逐项、ts_prepare 待补、A/B/C 三选一（**未决定**）、替代口径、证据清单；v1 明确标注「待补 4.20 Å / N_side / ts_prepare 原文」，**不是终版**。
## 16 R3 第五批（23:43）：**ts_prepare 已建 run（T4 开跑）**

- **run_id = ts_0010**（owner_session_id = as_6ede162e1cc94641 = 本包 TS 道）。本 Coordinator 用 `ts_inspect(run_id="ts_0010")` 独立读到（原文）：`revision=11`、`status=waiting`、`stage=refine`、`result=null`（**尚无科学结论**）、`run_dir=/home/ly/Cloudra-mechanism-agent/ts/ts_0010`、`details_path=/home/ly/Cloudra-mechanism-agent/ts/ts_0010/process.json`；`waiting_for=[{job_id: 975, purpose: ts_opt, state: ready, req_cpus: 8, req_memory_mb: 10240, input_path: ts/ts_0010/jobs/declaration_0001/ts_opt/refine.gjf, job_type: gaussian}]`。
- 声明的物种 = registry 原文（TS 道已采用我给的原串）：reactant `[O+:1]([H:2])([H:9])[H:10].[CH3:11][CH2:5]/[C:4](=[N:6]/[O:7][H:8])/[CH3:3]`（ts_0010/declare.json 原文）；guess kind 记录含 `provided`（1 处）与 `file`（3 处）⇒ 用的是质子居中内插帧。
- ts_opt 输入 route 原文（refine.gjf 第 3 行）：`#p opt=(TS,calcfc,noeigen) B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight`，第 5 行 `1 1` ⇒ 方法/电荷/重数与本包口径一致（Gaussian 原生 token `def2SVP`）。
- 平台构建的具体原子序可复核：ts_0010/build/input_0001/reactant/seed.{xyz,mol}（+ atom_table.json）与 build/input_0001/product/seed.{xyz,mol}；与 round3/T4_INPUT_ORDER_PROVENANCE.md 推导一致。
- **待办**：job 975 仍在队列（971–975 ready，975 排最后）；其结束后管线自动进入 freq / IRC 双向 / 两端端点 Opt+Freq，`result.outcome` 才会出现（verified / candidate_only / search_failed / invalid_input）。**在拿到 outcome 原文前不得宣布「无鞍点」**。
- 队列快照 23:43：running = 967(NY3 ts_0007 candidate_opt) / 968(HI1 ts_0008) / 969 / 970；ready = 971–975。
## 17 R3 第六批（23:46–23:50）：T4 报告落盘 + ts_0010 平台映射复核原文 + 一条工具面缺陷上报

- TS 道报告已落盘：round3/TS_RUN_REPORT.md（165 行，sha256 **15a2e005…d3fdc6**）。要点（我逐条读过，与 ts_inspect 一致）：
  - 调用参数逐字留证（reaction = registry 原文；calculations/guess/verification/execution 见该文件 §1）；端点 seed：reactant prep/RC_3A_seed.xyz（xyz sha 18dd830d…）、product round3/product_endpoint_seed_B_prodorder.xyz（xyz sha 5b03a2ea…）+ 两端 build_*/assembly/complex_candidate_000.mol；执行 8c/10240MB，无非原生 MaxIter/MaxSteps；refine.gjf sha256 19e0cc6d…。
  - **平台映射复核原文**：binding_status=complete、binding_source=concrete、reactant_identity=product_identity=match、权威 atom_map=[1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,2,17,18,19]（与声明逐位一致）、reaction_center 存为 0-based [[0,1],[1,8]] ≡ [[1,2],[2,9]]；bound 元素序：reactant O,H,H,H,C,C,C,N,O,C,H×9（= img_06.xyz 原序，guess 无需重排）、product O,H,H,C,C,C,N,O,C,H×10。
  - 阶段进度：declare / build（both endpoints built）/ map（19 atoms mapped）/ assemble（2 reaction-centre pairs）/ guess（Provided candidate bound）/ validate（internal validation passed）/ submit（job 975）全部完成；process.json rev 11 sha256 e71d5810…、declare.json sha256 1ca9f56d…。
  - **verdict 仍为 null**（无 outcome 原文可抄录，不是缺测）；后续 freq → IRC 双向 → 两端 Opt/Freq 由管线自动推进。
- **工具面缺陷（已只读取证并上报主协调，帖 evt_319145b9d6864a3e）**：ts_prepare 在**未声明 conformers（file + mol_path）**时两次抛 tool_exception（第 2 次带 call_id **tc_1418efb683964e2b**、effect_state=unknown；第 1 次 js_exec 被内部错误打断、无 call_id，只读取证确认**未产生 run、无副作用**）；对照本机已成功的 ts_0005–ts_0008 均声明了 concretely-bound 端点结构，**仅补齐该一项**（不改 registry SMILES/guess/方法）后第 3 次成功（call_id tc_91e760555fee49c4）。同 SMILES 的 smiles_to_mol(3D, +1) 亦报「builder reported status=ok but produced no MOL candidate」→ 与 #179 P1/P4 同类。
- 队列快照 23:50：running = 967–970；ready = 971–979（其中 **978 = 本包 E2_RC42A**，N_side 排在其后）。

## 18 R4（接任 Coordinator **as_939ca5a73ff445c2**，2026-10-17 06:3x–；平台第三次恢复后的终态处置）

### 18.1 起点盘点（真实文件系统读，不用变更流）
前任 as_0cbe3c2ee0ed460d 的记录止于 10-15 23:50（§16/§17）。10-16 00:17–00:54 又落盘 3 个作业（975 ts_opt 收敛、978 E2_RC42A、983 N_side 秒退），此后平台停滞；10-17 06:27/06:30 由管线跑出 986 frequency / 988 irc。本轮**不重做** 904/905/920/912/913/921/930/965/966/975/978/986/988 的任何计算。

### 18.2 ts_0010 终态（本 Coordinator 亲自 grep + sha256sum，原文行号）
| job | 原生日志（绝对路径前缀 = /home/ly/Cloudra-mechanism-agent/ts/ts_0010/jobs/declaration_0001/） | sha256 | 关键原文行 | 结论 |
| --- | --- | --- | --- | --- |
| 975 | ts_opt/refine.log（输入 ts_opt/refine.gjf） | d7ab3228d830b140bbec0f83c3597c9b331666763fc2f1597a9b6f76d43144e7（gjf 19e0cc6d…） | L23071 `SCF Done E(RB3LYP) = -364.295414931`；L23249–23250 `Optimization completed.` / `-- Stationary point found.`；L23671 `Normal termination`（10-16 00:17:53） | TS 优化收敛 |
| 986 | frequency/frequency.log | 9074df8074476386e05bbc2f89124aca6a453298270ce9cc418346bd0e575fed | L524 同上能量；L855 `****** 1 imaginary frequencies ******`；L864 `Frequencies -- -67.9886 25.2962 65.4614`；L1987 `Normal termination`（10-17 06:27:49） | 恰 1 虚频，但模归属见 18.3 |
| 988 | irc/irc.log | ce6f2b3a4356b31d45d3d450175343c175e14095a6c4d00f809012655b13808a（gjf d60706e8…） | L859/L861 `Point Number: 0` / `Point Number 1 in FORWARD path direction.`；全程仅 21 个 `SCF Done`，能量平在 −364.2954159 附近；末 `Delta-x Convergence NOT Met` / `Maximum number of corrector steps exceded` / `l123`（10-17 06:30:52） | **IRC 未完成（仅 FORWARD 第 1 点，积分停滞）**；不能作为「无鞍点」证据，只作 #184（无法设 IRC 步长/算法）的登记 |

### 18.3 决定性核对：该虚频模 **不是**声明键对（pseudo-saddle）
frequency.log L866–L886 的 mode 1 逐原子三分量，取模长（arbitrary）：**H2（原子 2，声明转移质子）= 0.028；O1（原子 1）= 0.000；O7（原子 9）= 0.046；C3 甲基的三个 H（原子 17/18/19）= 0.469 / 0.628 / 0.587，且 17 与 18/19 反相、分量和≈0 = 甲基扭转**。reduced mass 1.0990、force constant 0.0030 mDyne/A（L865–866）= 单氢转子量级。
⇒ 该虚频模与声明键对 [1,2]/[2,9] 基本无关；按 BRIEF §4 第 1 条 / §9 第 3 条属 **pseudo-saddle**，不得当该步 TS。

### 18.4 该驻点的几何与能量：已在产物侧
ts_opt 末帧（= irc.gjf 起点几何）实测 **R(1,2)=1.387 / R(2,9)=1.074 / O1···O7=2.460 Å**（产物侧极小值 B = 1.3811/1.0774/2.4568，几乎同构，只差甲基朝向）；E(TS) − E(B) = (−364.295414931) − (−364.295965289) = +0.000550358 Ha = **+0.3454 kcal/mol**（同程序同批；这是甲基转动垒，**不是** O-质子化垒）。
guess 本身是 IDPP img_06（path/input_0001/provided.xyz；provenance_0000.md）：**r(O1–H2)=1.280、r(H2–O9)=1.306、O1···O9=2.584 = 质子居中桥式帧** ⇒ TS 搜索从真正的候选 PT 鞍点几何出发，仍滑到产物侧并只收敛出甲基转动软模。

### 18.5 该步「起点极小值」在本级别气相不存在（无垒判断的核心证据，不是拿 IRC 失败顶替）
5 个「质子留在 O1」的未约束 Opt+Freq 种子全部坍缩到产物侧：904/905（2.60 Å, −364.2959652889999/−287）、920（3.00 Å, −364.295965302）、966（3.50 Å, −364.295777129 = B′，比 B 高 0.1181 kcal/mol）、965（双齿螯合, −364.295965301）；三者/四者同驻点、均 0 虚频。
**job 978（4.20 Å 种子，10-16 00:47 done）落到一个更深的极小值**：E = **−364.326887674 Ha**（L31253/L32228），0 虚频（L32557–32558 频率段从 64.6417 起），51 模、2×Normal termination（L31878/L33798）；末帧坐标（L32129 起）本 Coordinator 复算 **d(N6–H3)=1.060、d(O1···N6)=2.681、d(O1–H3)=1.626、d(O7–H8)=0.973、d(C4–N6)=1.292、d(N6–O7)=1.353、d(O1···O7)=3.469** ⇒ **N-质子化肟 + 水**氢键复合物，比 O-质子化的 B **低 19.4041 kcal/mol**（同程序同批）。
⇒ 声明的 O-质子化 RC 不是驻点；能算的「TS 差」只有 +0.3454（相对产物侧 B 的甲基转子）与（待单体落地）E(B) − E(分离 H3O+ + 肟) 的沉没值，**没有**「E(TS) − E(该步起点极小值)」这一对象。

### 18.6 包内决定（BRIEF §9 授权，留证；主协调 evt_8508f645/evt_e28378f0 与 evt_efb24952 曾建议按「TS 能垒」主交付，本包以 18.3/18.4/18.5 的证据回复并按证据自决，帖 evt_69b5b234af484b83）
- **HL1_E1 = 0.0 kcal/mol**，语义 = 无独立鞍点 / 无垒离子-分子质子转移；参考态改判为接触离子-分子对。先例 normal_registry/yo.py O3 第 1 步 0.0、NR1_E1（主协调 R4 已接受同口径）。
- 同时登记：+0.3454 kcal/mol（相对产物侧 B）= 甲基转动 pseudo-saddle，不是该步能垒；N-质子化通道比 O-质子化低 19.4041 kcal/mol（新发现的竞争通道，本包不改图，只登记）。
- 若主协调另有证据推翻 18.3–18.5，改值只需重跑同一回填链；本行即为可推翻点。

### 18.7 回填（本轮已完成，同批守卫通过）
| 文件 | 改前 sha256 | 改后 sha256 |
| --- | --- | --- |
| cloudra/benchmark/hard_registry/jl.py（L1 第 1 步加 `"barrier": 0.0` + 依据注释） | 7ed4e63a720ee6fced06cad5bd46811d59214732133b56220d76a75e56cc805c | 706592ea2c5e70d1bc393295340d4fe365e45061d4709a0cb1e22b104757822c |
| ideapool/reaction_candidates/hard.md（仅 L1 那一行，第 145 行「E1 保持 null」→ 新表述） | 4ca22fc3d99339dfec73a59669a3e9cb742861da018f2af56e44c650b0cf903f | 4940fa667289ed038c888f8d63f84f6c301b123681f5982158b5a8b93e70a089 |
| ideapool/tasks/hard/HL1.json（重生成：HL1_E1 null → 0.0，其余 3 边 23.13/10.44/13.46 未动） | 38081ed09c86db4acbf0e5e57d5cb65728d81dd0c15d44e0e4814b1f955384ae | 见 §18.10 终值 |
- 生成方式（只重生成 HL1.json，避免动其它包的 hard 题面）：`python3 -c "from cloudra.benchmark import gen_hard_tasks as g; ...parse_hard_md(g.DEFAULT_SRC, only={'L1'})..."`（与 gen_hard_tasks.main 同一代码路径，仅去掉 `len(tasks)==10` 断言）。
- 守卫：`python -m pytest tests/test_benchmark.py -k regenerate_identically -q` → **4 passed**（改前基线同 4 passed，无既有漂移）；md 行改后同轮复核 cell 数 = 8 = 表头（防 MEMORY 教训：源行 `|` 分裂会静默丢结构化字段），HL1.json 的 `git diff` 仅 1 行（barrier null→0.0），元素/重原子/方法白名单字段未变。

### 18.8 本轮已派（结果落地即补 §19）
| lane | session_id | 任务 |
| --- | --- | --- |
| CALC4（small_mol，手工作业） | as_d3fd414f63364cc8 | T1 N 侧未约束 Opt+Freq 重跑（983 因 route 用 def2-SVP 连字符 → QPErr，0.1 s 退出；日志 sha256 e6393fe1…）；T2 H3O+ / 肟单体 Opt+Freq（沉没垒替代口径）；T3 从 B 出发的质子转移坐标弛豫剖面（判有无内部极大；避开 913 l103 / 921 FormBX / 930 l9999 构造） |
| EXPL4（explorer，只读） | as_25d61de426fc4f9c | 独立复核 18.3 虚频模归属、18.4 几何、job 978 身份与能量差、搜索充分性与残余缺口 |

### 18.9 残余缺口（诚实登记）
1. 完整 PT 剖面（有无内部极大）**仍未测**：913/921/930 全部无可用收敛点（已证伪项：不能当「无鞍点」证据）；CALC4-T3 在跑。
2. 「无 PT 鞍点」的严格性上限：ts_prepare 只证明「从质子居中桥式 guess 出发没有找到合格 PT 鞍点 + 落到甲基转子伪鞍点」，严格性依赖 CALC4-T3 的剖面。
3. 参考态能量（分离 H3O+ 与肟单体）未测 ⇒ 沉没垒数值待 CALC4-T2。
4. T3c/T3d/T3e 反向/侧向剖面只有输入无结果（explorer R3 §5–§10 已登记）。
5. 引擎偏差：本题源既有 gold 口径为 ORCA 6.1.1；本包全部数值为 Gaussian 16（B3LYP/def2SVP + GD3BJ + Int(UltraFine) + SCF=Tight），程序不同、不得与他机 ORCA 值混减。

## 19 R4 收尾交接（整合 Coordinator **as_6a82b2857ef44902**，2026-10-17 06:5x）

**交接**：前任 as_939ca5a73ff445c2 已结束运行；本包两条道仍在跑，已用 agent_hub call 把收集点重指向本任（要求各道结论 post 到主题 gold-finish-20261015 且首行 `to: as_6a82b2857ef44902`）：
- CALC4 = small_mol **as_d3fd414f63364cc8**（notify evt_71daa5f2b87947af，wake_status=requested）：T1 = N 侧未约束 Opt+Freq（round4/T1_N_side_optfreq.gjf sha 0ad4576c…，job **995**）；T2a = H3O+ 单体（job **996**）；T2b = 肟单体、T3 = 从 B 出发的单坐标弛豫 PT 剖面（输入已落盘待提）。结果将写入 round4/CALC4_REPORT.md 并发主题终帖。
- EXPL4 = explorer **as_25d61de426fc4f9c**（notify evt_efa27e11c08f46fc，wake_status=already_running）：只读独立复核 18.3 虚频模归属 / 18.4 几何与 +0.3454 语义 / job 978 身份与 19.4041 kcal/mol / job 988 可解读边界 / 搜索充分性与残余缺口。

**本任实读复核（非引用）**：`cloudra/benchmark/hard_registry/jl.py` sha256 = **706592ea2c5e70d1bc393295340d4fe365e45061d4709a0cb1e22b104757822c**；`ideapool/reaction_candidates/hard.md` sha256 = **4940fa667289ed038c888f8d63f84f6c301b123681f5982158b5a8b93e70a089**；`ideapool/tasks/hard/HL1.json` 第 **154** 行 `barrier_kcal_mol: 0.0`，其余三步仍 23.13 / 10.44 / 13.46（L188/L214/L248）⇒ 回填面与 §18.7 一致，未被本轮任何动作改动。

**口径（本轮不变）**：HL1_E1 = **0.0 kcal/mol**（语义 = 该步在本级别气相无独立鞍点 / 无垒离子-分子质子转移；声明的 O-质子化 RC 不是驻点）；引擎偏差（题源既定 ORCA 6.1.1 vs 本包 Gaussian 16）继续显式声明，能量只在同批 Gaussian 日志内相减。

**收尾前待补**（落地即更新本节，§18.9 缺口 1/2/3 对应项）：① T1 是否 0 虚频极小值 + 与 job 978 是否同一驻点；② T2 单体能量 ⇒ 沉没垒 E(B) − E(分离 H3O+ + 肟)；③ T3 剖面**有无内部极大**（本包 0.0 判定的唯一外部可推翻点）；④ EXPL4 独立复核是否复现 18.3–18.5。

## 20 R4 收尾·EXPL4 独立只读复核已落地（**不推翻、且补强** HL1_E1 = 0.0）

来源：explorer **as_25d61de426fc4f9c** 终态帖 evt_54f0bac1d7454e68（首行 to 本任 as_6a82b2857ef44902），另经前任 as_939ca5a73ff445c2 只读交叉核对帖 evt_42857813707c4d80 确认与 round4/HL1_E1_DECISION.md 逐条一致。explorer 无写权限，本节由写权会话（本任）落盘转述；其数值为 explorer 自算，本任未复算（除第 7 条注明者）。

1. **ts_inspect(ts_0010) 原文**：run_id = ts_0010、status = **blocked**、stage = refine、**revision = 22**、**result = null**（无 result.outcome）；blocked 细节 failure_class = **job_failed**，归因 job 988 (irc)，log_sha256 = ce6f2b3a4356b31d45d3d450175343c175e14095a6c4d00f809012655b13808a、input_sha256 = d60706e896261a1202cad06c128eb33427a74eae6ae2fd44e9b8847b386b85d1；waiting_for = []。⇒ 该 run 未产出可交付 TS 结论（与 §18.2 一致）。
2. **虚频模归属（补强 §18.3）**：frequency.log（sha 9074df8074476386e05bbc2f89124aca6a453298270ce9cc418346bd0e575fed，1987 行）L855 「1 imaginary frequencies」、L864 −67.9886、L865 Red. mass 1.0990、L866 Frc const 0.0030；逐原子 mode 1：原子 17/18/19 = 0.469/0.628/0.587，H2 = 0.028，O1 = 0.000，O7 = 0.046。三条独立佐证：(i) 质量加权 Σm|L|² = 1.0964（印刷 μ = 1.0990，差 0.2%）中甲基三 H 占 **88.1%**、H2 仅 **0.07%**、O1+O7 3.06%；(ii) 取 ω 平行 C10–C7 算理想切向位移，与 mode 1 夹角余弦 **1.000 / 0.995 / 0.984**（径向分量 −0.003/+0.041/−0.081 Å）⇒ 三 H 绕甲基轴刚性转动；(iii) 沿 O1→O7 单位矢量投影 H2 = **−0.0011 Å**（PT 方向无成分），甲基三 H = +0.259/+0.178/−0.485。同几何 Berny Hessian 负曲率本征矢亦以甲基 H 为主（refine.log L1503–1505，Eigenvector X19 X18 Z17 Z18 Z19）⇒ pseudo-saddle 成立。
3. **+0.3454 语义（补强 §18.4）**：ts_opt 末帧与 B（A_RC_optfreq.log L15861–L15879）在反应坐标上几乎同结构（1.387/1.074/2.460 vs 1.381/1.077/2.457；N6–O7 1.556 vs 1.554；C4=N6 1.279 vs 1.280；O7–H8 0.978 vs 0.978），但 171 对原子间距最大偏差 **0.983 Å（H3–H19）**、>0.01 Å 者 116 对，偏差集中在甲基 H 与水的 H ⇒ 差别是甲基/水朝向而不是反应坐标 ⇒ ΔE = +0.3454 kcal/mol 只是甲基转动 pseudo-saddle 相对同物种极小值 B 的差，**不是** HL1_E1 的 ΔE‡。ts_opt/refine.gjf sha256 19e0cc6d652f3e7bef9cbd4cfc1126ab1f6f14b60673697a3b217b8bd895c0af（L3 route 原文）。
4. **job 978 身份（确认 §18.5）**：E2_RC42A_optfreq.log sha256 9450eb9d48fcfbba6e30388ffe2b5a6d5ab760bb39fc95ff508ef93fa3e09505，E = −364.326887674 Ha（L30792/L31253/L32228）；51 模、全文无 imaginary 行（0 虚频；最低实频 64.6386/82.5441/88.4165，最高 3866.2068）；末帧 L32129–L32147 复算 d(N6–H3) = 1.060、d(O7–H3) = 1.990、d(O1···N6) = 2.681、d(C4–N6) = 1.292、d(N6–O7) = 1.353、d(O7–H8) = 0.973、d(O1···O7) = 3.469 Å ⇒ N-质子化肟 + 水氢键复合物真极小值；ΔE(978 − B) = −0.030922385 Ha = **−19.404 kcal/mol**（627.5094740631）；ΔE(978 − ts_0010) = −19.749 kcal/mol。本批两族极小值并存：O-质子化复合物族（B/B′，H2 在 O7，O1···O7 2.457 Å）与 N-质子化肟+水（978，低 19.404）。
5. **job 988（irc）可解读边界**：irc.log sha256 ce6f2b3a4356b31d45d3d450175343c175e14095a6c4d00f809012655b13808a（8652 行）；只尝试 FORWARD 第 1 点（L857–L861；全文件 Point Number 计数 = 2，REVERSE = 0），20 次 Delta-x 不收敛、末步位移 0（New End-Old End Dist. = 0.000000）→ L8645–L8649 「Delta-x Convergence NOT Met」/「Maximum number of corrector steps exceded.」/ l123（06:30:52）；21 次 SCF 能量停在 −364.2954159（1e-9 Ha 平台）；首条 IRC 帧相对 TS 帧近似整体 +0.041 Å(x) 刚体平移（ΔR(1,2) = +0.0001、ΔR(2,9) = −0.0000、H2 沿 O1→O7 投影 −0.033 Å 来自平移）⇒ **无任何 PT 推进**。**能说**：默认步长/corrector 限额下从该驻点连第 1 点都无法收敛、反向从未尝试、作业 l123 失败。**不能说**：鞍点与端点连通性、有无 PT 能垒、「IRC 报错 ⇒ 无鞍点」。本边连通性采用**替代口径**（5 个 O1-质子化种子全部坍缩 + 唯一一次真实 TS 搜索只给甲基扭转 pseudo-saddle），该口径在「未找到合格鞍点」层成立，不得升格为「IRC 证明无垒」。
6. **残余缺口（explorer 独立清单，采纳为交付文字边界）**：(a) d(O1···O7) > 4.20 Å 的种子从未运行（最长程只有输入 T3b_sepscan_OO_long.gjf，无 .log）；(b) T3c/T3d/T3e 只有输入无结果；(c) 本批 4 条剖面全失败（912 L45142 l9999、913 L4803 Error imposing constraints + l103、921 L12257 FormBX + l103、930 L52378 l9999）⇒ PT 弛豫剖面仍缺；(d) N 侧此前只有 978 一个数据点（983 因 def2-SVP 连字符在 L95 l1 QPErr，不构成搜索）；(e) 分离单体（沉没口径）未测；(f) explorer 无 query_compute_queue 权限，无法自证在飞作业状态。方法一致性：逐份 route 核对为 Gaussian 16、B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight，无连字符写法。
7. **本任本轮自核（真实日志读，非引用）**：job 996（T2a = H3O+ 单体 Opt+Freq）state = **done**（06:45:18 → 06:45:28）；round4/T2_H3O_monomer_optfreq.log 2150 行、L1240/L1655 「SCF Done E(RB3LYP) = −76.6445472086」、L1476/L2150 两次 Normal termination、L1839–L1850 频率 756.1115 / 1608.6827 / 1609.1395 / 3559.4235 / 3664.7565 / 3664.9430（6 模 = 3N−6），`grep -c -i imaginary` = **0**。job 995（T1 = N 侧未约束 Opt+Freq）06:43:08 起 **仍 running**（T1_N_side_optfreq.log 已 471 KB）。⇒ 沉没垒仍缺**肟单体**（T2b，待提）。
8. **本节结论**：EXPL4 独立复现 §18.3–§18.5 全部关键数值并给出更硬的模归属证据 ⇒ **HL1_E1 = 0.0 维持不变**（尚无任何证据指向推翻）；剩余三项（T1/T2b/T3）落地后由本任收口。

## 21 R4 收尾·CALC4 首批结果（T1 = job 995 已完成；本任亲自解析原生日志，非引用）

job 995（T1 = N 侧未约束 Opt+Freq；输入 round4/T1_N_side_optfreq.gjf sha256 0ad4576c6966abb65c12d1aaf105514c5ff7cef3e0eff60f6e33036d55d39ae6；种子 ts_run/prep/N_side_frame_from_T3a.xyz sha256 dfacf479e41752b8ffc004631135a260e3c53cb752a4b8aa8c58c4357f378538）state = **done**（06:43:08 → 06:53:34）；原生日志 round4/T1_N_side_optfreq.log（1722123 B，26687 行）；末帧导出 round4/T1_N_side_final.xyz（06:53）。

- **opt**：L25587 「Optimization completed.」、L25588 「-- Stationary point found.」；末次 SCF Done = **−364.326887706 Ha**（全日志 50 次 SCF 的最后一次；L25381 / L26365）。
- **freq**：Frequencies 段 17 个 ×3 = **51 模 = 3N−6**；全文 `imaginary` 匹配数 = **0**（本任 python/grep 实读）⇒ **0 虚频**，最低实频 **64.5647 cm⁻¹**（随后 82.5440 / 88.4481 / 110.3337 …）；opt 段 L26012 与整体日志末尾均为 Normal termination。
- **末帧几何**（最后一个 Standard orientation 块，本任由坐标复算）：d(N6–H3) = **1.060**、d(O1–H3) = **1.625**、d(O1···N6) = **2.681**、d(N6–O7) = **1.353**、d(C4=N6) = **1.292**、d(O7–H8) = **0.973**、d(O1···O7) = **3.469**、d(O1–H2) = **0.970**、d(O1–H4) = **0.969 Å**。
- **与 job 978 同一驻点**：978（E2_RC42A，−364.326887674 Ha）末帧为 1.060 / 1.626 / 2.681 / 1.353 / 1.292 / 0.973 / 3.469 ⇒ 能量差 **3.2×10⁻⁸ Ha（≈2×10⁻⁵ kcal/mol）**、几何差 ≤0.001 Å ⇒ **T1 = N-质子化肟 + 水极小值的第二条独立到达路径**（其起点是 T3a 的桥式帧；该桥式帧不构成中间极小值，直接弛豫到 N 侧极小值）。
- 序号警示：T1 输入的原子序为 T3a 帧导出序（1 = O1，2/3/4 = 水的三个 H，其中 3 为迁移质子，8 = N6，9 = O7 …），与包内标准序（2 = H2 为声明转移质子）不同位 ⇒ 身份判定一律用**几何对比**，不用序号。
- **对 0.0 判定的影响：不推翻，进一步支持**「O-质子化（H2 留在 O1）在本级别气相不是驻点」——N 侧极小值越低、到达路径越多，只强化「该步无垒/无独立鞍点」的结论。

**CALC4 仍缺（排队中）**：T2b = 肟单体 Opt+Freq = job **1002**（round4/T2_oximeE_monomer_optfreq.gjf，state ready）；T3 = 从 B 出发的 PT 弛豫剖面 = job **1005**（round4/T3_ptscan_H2O9_relaxed.gjf，state ready，输入 sha256 d4fa530ed2d2ab081699592cb031512eef5641ca431ba8b48b7030a5ffe697c3）。节点满（991/993/998/999 四个 8c 在跑），二者排队中。二者落地即补 §22 并出终态帖。

**CALC4 非 QM 收尾已落盘**：round4/CALC4_REPORT.md sha256 **d75e9496c8ef8f92ae477590090d1fcc089b9ce19f346ca8d81fbaea31b79653**（§1 T1 全栏、§2 T2a 全栏、§3 T2b 待补、§4 T3 构造与理由、§5 无法取证项、§6 复现命令）；其帖 evt_67df1c3298194426 与 evt_38e58bfa9edf4afd。备用细分辨剖面输入 round4/T3b_ptscan_H2O9_fine.gjf sha256 bb8d7edb448ca8e26e783510157c7f770da3975220613c69679f75ba9c179474 —— **只落盘不提交**，仅在 T3 出现可疑结构或 <0.05 Å 宽小内峰时启用。

**本任独立复核回填面（同一轮）**：`git diff --stat` = jl.py 15 行（注释块 + `"barrier": 0.0`）、hard.md 2 行、HL1.json **1 行（L154 `barrier_kcal_mol`: null → 0.0）**；HL1.json 的 `gold` 结构含 mechanism_graph / reference_properties / selectivity，`max_heavy_atoms` 与元素白名单字段与 HI1.json 同构（非空）；`python3 -m pytest tests/test_benchmark.py -k regenerate_identically` = **4 passed, 185 deselected in 1.36s**（exit 0）。

## 22 R8.1 · 硬档测试期望表同步（主协调裁定，本包唯一写权会话执行）

**背景**：NR1 会话回报全量 pytest 有 1 failed = `tests/test_benchmark.py::test_hard_replacement_and_hl1_reframed_graph`（L2138 期望 `[None, 23.13, 10.44, 13.46]` vs 实测 `[0.0, 23.13, 10.44, 13.46]`）——归因是 HL1_E1 回填后该期望表未同步，**属回填收尾项，不构成新证据、不推翻 0.0**。主协调裁定：保持 HL1_E1 = 0.0（口径 = 无独立鞍点的约定值，**不是** 0 垒 TS），把 L2138 首项 None 改为 0.0。

**改动（仅 1 行）**：`tests/test_benchmark.py` L2138 由 `[None, 23.13, 10.44, 13.46]` 改为 `[0.0, 23.13, 10.44, 13.46]`；改前 sha256 `1d4f723b1877bde886e3bc5ee0b675a0b0e63e66149e9bb485d3c328c88e2b98` → 改后 sha256 **`037a424b05cc5d28f0bd2540af456aedf034908d5e59525b356994d38bd8d014`**。未改任何评分规则、生成器、其它题断言（写权仅本轮、仅此文件此 1 行）。

**同轮守卫输出（原样）**：
- `python -m pytest tests/test_benchmark.py -k hard_replacement` → `1 passed, 188 deselected in 0.93s`（exit 0）
- `python -m pytest tests/test_benchmark.py -k regenerate_identically` → `4 passed, 185 deselected in 1.55s`（exit 0）
- `python -m pytest tests/test_benchmark.py --tb=line -rf`（全量）→ `188 passed, 1 skipped in 20.25s`（exit 0，**0 failed**）

**语义确认（供交付报告引用）**：HL1_E1 = 0.0 = **无独立鞍点的约定值**，参考态 = 接触离子-分子对，**不是** 0 垒 TS。该语义写在两处：round4/HL1_E1_DECISION.md §0（改后 sha256 **e33f32d9e344f97461121e274cbc26dc62d1f48dffe09cb07bd288ae29811e83**）与本 STATUS.md §18.6 / §19 / §20。

**队列状态（本轮实读）**：job 1002（T2b 肟单体）与 job 1005（T3 剖面）仍 state = **ready**（排队未开始）；T3 是唯一能外部推翻 0.0 的未决项。

## 23 R10 · T2b（肟单体）已终态 + 沉没口径备料（本任独立复核；**不改** HL1_E1 = 0.0）

job 1002 = T2b（肟单体 Opt+Freq）state = **done**（主协调报 07:21:44）；输入 round4/T2_oximeE_monomer_optfreq.gjf（opt freq B3LYP/def2SVP + GD3BJ + Int(UltraFine) + SCF=Tight，电荷/多重度 0 1）；原生日志 round4/T2_oximeE_monomer_optfreq.log，**本任同轮实测 sha256 = 70e3b718ecc860b667148204a2614c670ab41dff306cfd2ce2d592d68dd544fa**（与主协调所报一致）。

本任 python 解析原生日志（非引用）：
- 原子数 **15**（C4H9NO）；`Frequencies --` 13 段 ×3 = **39 = 3N−6** ✓；全文 `imaginary` 匹配 = **0** ⇒ **0 虚频**（最低实频 73.3386 cm⁻¹；Low frequencies 行首负值为投影残值，不计）；Normal termination ×2（opt / freq）；末次 SCF Done = **−287.574297051 Ha**。
- T2a（H3O+ 单体）日志 round4/T2_H3O_monomer_optfreq.log，本任同轮实测 sha256 = 51a88da244d1441fb02abaa51673db107a6d6fc6b3d50b7959fb3a957b444bd6，E = −76.6445472086 Ha，6 模 0 虚频。

**沉没口径（替代说明；纯电子能、同批 Gaussian、627.509474 kcal/mol per Hartree）—— 必须标明对照的是哪一个产物侧极小值：**
- 对照 **N-质子化肟 + 水**（job 978 / 995，E = −364.326887674 Ha）：ΔE = **−0.1080434144 Ha = −67.798 kcal/mol**（主协调算术复现一致）。
- 对照 **O-质子化产物侧复合物 B**（E = −364.295965289 Ha）：ΔE = **−0.0771210294 Ha = −48.394 kcal/mol**。

**语义与采用**：两值均为负 ⇒ 产物侧复合物在纯电子能上低于「分离的 H3O+ + 肟」之和（离子-分子络合在气相下沉，无垒 PT 的典型情形）。因此「沉没垒」**不能**充当该步 ΔE‡ 的替代数值，只能用于说明「分离态参考比络合物更高」这一事实；**不参与、不改变 HL1_E1 = 0.0**。

**未决**：job 1005（T3 = 从 B 出发的 PT 弛豫剖面）仍 state = ready；**T3 是唯一能外部推翻 0.0 的未决项**，出内部极大即按 BRIEF §9 重裁并上报。

## 24 R14 · T3（job 1005）逐点剖面完成：**存在内部极大** → 按约定触发重估；本任裁定 = **HL1_E1 = 0.0 维持**（约定值），剖面登记为已知竞争坐标

**作业**：job 1005，输入 round4/T3_ptscan_H2O9_relaxed.gjf（sha256 d4fa530ed2d2ab081699592cb031512eef5641ca431ba8b48b7030a5ffe697c3；route `# opt=(modredundant,maxstep=10) B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight`；扫描量 R(2,9) 1.0774 → 2.0274 Å，19×0.05）；原生日志 round4/T3_ptscan_H2O9_relaxed.log **sha256 40ce3be2c6d07120b36d7bf8ce9580aad6becaee16cdf8d1b2c3cb0ab0e60c07**（69007 行）；**20/20 点 Optimization completed + Stationary point found、0 次 Convergence failure**；Normal termination L69007（08:00:33）；剖面表原文 L68362。

**逐点剖面（Ha，括号内 = 相对 B（−364.295965289 Ha）的 kcal/mol）**：
- pt1 −364.295965（0.00，= B）→ pt2 −364.29555（+0.26）→ pt3 −364.29464（+0.83）→ pt4 −364.29358（+1.49）→ pt5 −364.29251（+2.17）→ pt6 −364.29149（+2.81）→ pt7 −364.29063（+3.35）
- **pt8 −364.290279（内部极大，+3.57）** → pt9 −364.29053（+3.41）→ pt10 −364.29123（+2.97）
- **pt11 −364.300601（−2.91；此处质子 H4 由 O1 转到 N6）** → pt12 −364.30339（−4.66）→ pt13 −364.30580（−6.17）→ pt14 −364.30788（−7.48）→ pt15 −364.30968（−8.61）→ pt16 −364.31126（−9.60）→ pt17 −364.31265（−10.48）→ pt18 −364.31389（−11.25）→ pt19 −364.31500（−11.95）→ pt20 −364.316038（−12.60）

**几何身份（本任由坐标实算，非引用）**：
- **pt1**：d(1,2)=1.381、d(2,9)=1.077、d(1,9)=2.457、d(8,9)=1.554、d(7,8)=1.280、d(9,16)=0.978、d(1,3)=0.970、d(1,4)=0.970 ⇒ 质子 H2 在 O9 上、O1 为水 ⇒ **pt1 = 产物侧复合物 B（HL1_E1 产物节点侧），不是声明的起点（接触离子-分子对）**。
- **pt8（极大）**：d(1,2)=1.076、d(2,9)=1.477、d(1,9)=2.448、d(8,9)=1.467、d(7,8)=1.284、d(9,16)=0.976、d(1,3)=0.975、d(1,4)=1.003 ⇒ H2 在 O1/O9 之间**共享**；O1 上仍有三氢（H3 0.975 + H4 1.003）= **氢鎓完整**；肟为**中性**（N6–O7 = 1.467、N6 上无 H）⇒ 该点的质子化态属于**声明的反应物侧（H3O+ + 中性肟）**，且正落在声明步（O1→O9 质子转移）坐标上 ⇒ **TS 候选**。
- **pt11 起**：d(N6–H4)=1.061、d(1,4)=1.690 ⇒ H4 由 O1 转到 N6 = N-质子化肟 + 水；**pt20**：d(1,2)=0.972、d(2,9)=2.027、d(8,9)=1.375、d(N6–H4)=1.048 ⇒ 仍为 N-质子化肟 + 水，正朝已知 N-质子化极小值（job 978，−364.326887）下降。

**本任裁定（BRIEF §9，留证）＝ 保留 HL1_E1 = 0.0（约定值），并把该剖面登记为已知竞争坐标**：
1. 受约束扫描的极大点**只是 TS 候选、不是已证实鞍点**（无频率、无 IRC；扫描固定 d(2,9)，路径不保证是 MEP）。
2. 声明步 ΔE‡ 必须相对该步**自身起点极小值**（bimolecular ⇒ 接触离子-分子对 RC）。剖面显示反应物侧约束点 pt9/pt10 位于 **B 上方 +3.41 / +2.97 kcal/mol 且仍在下降** ⇒ **没有到达 RC 极小值**，与「5 个 O1-质子化种子全部坍缩到 B」的既有结论一致（该方向是下坡）。
3. 故「相对声明步起点极小值」的 ΔE‡ **依然无法给出**；把 +3.57（相对产物侧 B）当 ΔE‡ 违反纪律，不予采用。
4. 必须**更正**此前「PT 弛豫剖面无内部极大」的表述：本剖面上**确实存在内部极大（pt8）**。但把它读成「该步有 3.57 kcal/mol 垒」不成立 —— 相对反应物侧约束点只高 **0.6 kcal/mol**（pt8 − pt10 = 0.000951 Ha = 0.597 kcal/mol），且反应物侧点本身不是极小值。⇒ **0.0（约定值 = 无独立鞍点、本质无垒）维持，语义不变**；新增证据只是把「该步本质无垒（<1 kcal/mol 量级，受约束剖面分辨率内）」写得更实。
5. **竞争坐标登记**：从产物侧 B 出发沿 d(2,9) 拉长，越过 pt8 极大后经**第二次质子转移（H4→N6）**落入 **N-质子化肟 + 水**通道（pt20 低 B 12.60 kcal/mol，且继续向 978 下降）⇒ 与 job 978 的竞争/死端判定一致；不改变参考图、不改图。

**新增残余缺口（诚实登记）**：pt8 是否为真一阶鞍点**未验证**。关闭该缺口需要：① 以 T3 日志 pt8 帧为 guess 走 **durable ts_prepare**（guess kind=file，evidence_refs = 该帧 + provenance note）；② freq（期望恰 1 虚频且模以 [1,2]/[2,9] 为主）；③ IRC 双向 + 两端点 Opt/Freq（产物侧应为 B；反应物侧可能不存在极小值 ⇒ 可能 search_failed / candidate_only）；④ 全程同批 Gaussian、def2SVP。**本包不擅自提交新作业（队列纪律），需主协调授权。**

## 25 R14.2 / R14.4b · 措辞限定与 T3 证据登记（主协调裁定；本包写权会话执行，2026-10-17）

**定稿措辞（不得再简写为「无独立鞍点 / 无垒」）**：HL1_E1 = **0.0 kcal/mol**，语义 = **声明方向（接触离子对 → O-质子化产物）无合格鞍点 / 相对该步自身起点无垒**；**反向（产物侧 B → 接触离子对方向）受约束弛豫剖面存在内部极大 pt8 ≥ +3.5705 kcal/mol（相对 B，仅下界）**；pt8 帧**不是已验证鞍点**（是否为自由 PES 一阶鞍点未经管线 OptTS+freq 判定）。仅下界的理由：0.05 Å 网格分辨 + **pt10→pt11 单步跌 5.88 kcal/mol**（−364.291229930 → −364.300603835）⇒ 峰后换通道（H4→N6）⇒ 一律写「**受约束剖面极大**」，**不写「鞍点」**。
**登记项（与 round4/HL1_E1_DECISION.md §8 同文）**：
- ① T3 剖面与收敛：round4/T3_ptscan_H2O9_relaxed.log sha256 40ce3be2c6d07120b36d7bf8ce9580aad6becaee16cdf8d1b2c3cb0ab0e60c07（69007 行）、**20/20 点收敛**、Normal termination L69007（08:00:33）、剖面表 L68362；逐点能量表见 DECISION §8。
- ② pt8 身份 = 接触离子对（氢鎓式 O1 + 中性肟；R(1,9)=2.400 等）⇒ 属声明步反应物侧，不是产物 B；TS-guess round4/T3_scan_peak_pt8_ts_guess.xyz sha256 7018f6880a335c7ccd013a47d44fcf8599c3e9f5842bfa872571ae33f9a014ac。
- ③ 竞争 N-质子化通道：峰后 H4→N6 落入 N-质子化肟 + 水，其极小值比 B 低 19.404 kcal/mol；**剖面远端 pt20（−364.316038391 = B − 12.594）仍高于该极小值 6.81 kcal/mol ⇒ 两端都不是已验证极小值端点，不得写成「剖面到达 N-质子化极小值」或「剖面已到达端点」**。
- ④ 沉没口径三值（E(sep) = −364.218844260 Ha）：E(B) − E(sep) = **−48.394**；E(978 N-质子化) − E(sep) = **−67.798**；E(ts_0010 伪鞍点) − E(sep) = **−48.049** kcal/mol（仅替代口径，不参与主值）。
- ⑤ 报告引用：终版 round4/CALC4_REPORT.md sha256 875a863698ee24251ff52160fb58acb048d9d47b42ddb267184696f46785b863；**勘误**：本 STATUS §20/§21 早前引用的 d75e9496… 与主协调提到的 c25886ba… 均为作废版本 ⇒ 对外一律用终版。

**本轮改动与 sha 链（改前 → 改后）**：
- `cloudra/benchmark/hard_registry/jl.py`：**仅注释**（barrier 数值与结构未动）706592ea2c5e70d1bc393295340d4fe365e45061d4709a0cb1e22b104757822c → **944346f44465eac0b2fda3c47df58180427bc00d59963b5e9e2ce521baa64481**
- `gold_finish_20261015/HL1/round4/HL1_E1_DECISION.md`：e33f32d9e344f97461121e274cbc26dc62d1f48dffe09cb07bd288ae29811e83 → **079392707ded6137f3ccf1e3b45f3e37d5550cfcc2ea2d8cb565ffa92fe2a338**（§0 措辞 + §6「可推翻点」裁决注 + 新增 §8 登记）
- `gold_finish_20261015/HL1/STATUS.md`：eb7a89d1a8beb359ca5c148e74584ea62affb11ef0699124e5274f476bd081e8 → 本节改后值（见回帖）
- `ideapool/reaction_candidates/hard.md`（4940fa66…）与 `ideapool/tasks/hard/HL1.json`（240865b13d28a1fb13f1cd5fe7211a993bc33fe413c60d2b3adbb67cc9db1678）**未改动**。

**四条守卫（改动后同轮原样）**：
- `python -m cloudra.benchmark.gen_hard_tasks`（全量重生成）→ 退出码 0、输出 `wrote 10 tasks to …/ideapool/tasks/hard`；**改前/改后 10 份 hard JSON 的 sha256 逐一致**（生成器空操作，其它题面未受影响）
- `python -m pytest tests/test_benchmark.py -k regenerate_identically` → `4 passed, 185 deselected in 2.94s`（exit 0）
- `python -m pytest tests/test_benchmark.py -k hard_replacement` → `1 passed, 188 deselected in 1.19s`（exit 0）
- `python -m pytest tests/test_benchmark.py -k pinacol` → `1 passed, 188 deselected in 0.77s`（exit 0）
- `python -m pytest tests/test_benchmark.py --tb=line -rf`（全量）→ `188 passed, 1 skipped in 15.22s`（exit 0，**0 failed**）

## 26 R15.1 之后：只读补强页 + 勘误（写权会话）

- 新增 `round4/HL1_CROSSCHECK.md`（只读补强：CALC4 / EXPL4 / as_939 三来源交叉核对矩阵 ①–⑦ + 未关闭缺口三条 + CALC4_REPORT 作废 sha 勘误），sha256 **9d7da778716bfdee66ce7d83495b8fdccd36b47e75382d5d3e72be36baa48bb3**；帖 evt_3fb7950d284c4fac。
- 主协调 **R15.1** 裁定：HL1 包终态验收通过；**本轮不授权**用 pt8 帧走 ts_prepare（登记为可选增强项）⇒ HL1 侧不再提交任何作业。
- **勘误（唯一正确值）**：ts_0010 的 `frequency.log` sha256 只有 **9074df8074476386e05bbc2f89124aca6a453298270ce9cc418346bd0e575fed** 这一个值（本 STATUS、DECISION、以及各道帖中的引用均为该值）；帖 evt_3fb7950d284c4fac 第 3 条我把 12 位前缀误写成「9074df804474…」，**作废**，正确前缀为「9074df807447…」。此勘误只涉及前缀笔误，日志基数/数值/行号均未受影响。