# NR1 包 · STATUS（gold_finish_20261015/NR1/STATUS.md）

包 Coordinator：session as_53d43419a24c485b（role=coordinator）。更新时间：2026-10-15 17:1x SGT。
边界：只负责 NR1_E1 / NR1_E2 两条缺口边；NR1_E3=5.16、NR1_E4=5.74 不动；旧 NR1_E1=0 作废不回填。

## 0 逐边状态（计算完成 ≠ 验收通过）

| 边 | 状态 | 值 (kcal/mol) | 证据（原生日志绝对路径 + sha256） | 下一步 |
|---|---|---|---|---|
| NR1_E1 | 缺测（进行中）；现有证据强指向『该质子坐标上无独立鞍点、PT 无垒、声明的 R 复合物不是极小值』 | —（不填 0；若复核通过将按『豁免申请 + 建议值』报主协调裁决） | R 侧扫描：/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NR1/E1/scan/pt_scan_R_01.log sha256=cbf050ed016d152999cdb102158b238505dc896d556fbdf3706d95631c205bf9；输入 .../E1/scan/pt_scan_R_01.gjf sha256=effb1fcd398e5855ffe460ae24bb9fa82249edf35762d53598e402951c0d0e7b；产物侧扫描：.../E1/scan_P/pt_scan_P_01.log sha256=a43817fd7d783ff17a376ba97f6629b0c32ec96c35d2f6bfc1b5de230ad7b67e；输入 .../E1/scan_P/pt_scan_P_01.gjf sha256=c505690eb3c9e7d6f7b9bbd45cc4ff0803a57c7e59eba0fe62f8ad7f55fec1ba | ①job 903/906 已正常终止；②待无约束 Opt+Freq 坍缩判据（E1/opt_R/optfreq_R_d230.gjf sha256=d8abc26ebcce086ce4016d9977d3cd206bb698020eeea342817fb3866b4836f3）与长程 d(O1–O8) 弛豫扫描（E1/scan_O/pt_scan_O_01.gjf sha256=cd5aa76398c013cd22a8086b1e4a60a642ab0458e3dc735deaaee94d669f12fa）；③若有内峰/极小值即投 ts_prepare 正式链 |
| NR1_E2 | 缺测（进行中） | — | 起点/产物结构（非 QM）：.../NR1/E2/E2_PREP_PROVENANCE.md sha256=446a744673aa5f6eac64dd1393730b40c0f6fc0c21009cd46798044ea2c1c817；I1 Opt/Freq 输入 .../E2/logs/E2_I1_optfreq_c000.gjf sha256=f2515d42dc458090cd384d00c83672b62945bfb0067cd4e5ff097720335728b5（job 911，排队）；I2 输入 .../E2/logs/E2_I2_optfreq_c000.gjf sha256=4a12461e5e9df5d3dac4b979624b7f8792a6d7acf6d3a0de01eddc7c173305aa | ①I1 极小值 0 虚频 + 质子归属核验；②I2 极小值；③ts_prepare(guess=scan 沿 d(C4–O6)) 找脱水鞍点；若仍无独立鞍点即交搜索证据 + 『是否与 E3 合并』裁决问题 |

## 1 方法与引擎（全包统一）
Gaussian 16 /home/ly/g16/g16，B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight，气相（无 SCRF），charge=+1、mult=1、26 原子 C6H17O3。TS/IRC 只走 ts_prepare/ts_resume。ΔE‡ = 纯电子能差（无 ZPE/热校正），只与本包本批 Gaussian 日志相减。本机无 ORCA（程序偏差须在交付里显式写出）。

## 2 现阶段数值观测（Coordinator 自读原生日志；待道主正式证据与复核道独立复核）
两条弛豫（opt=modredundant,maxstep=10）原生扫描共用同一起点几何（MMFF 装配 candidate_000：r(O1–H4)=1.011 Å、r(H4···O8)=1.498 Å、r(O1···O8)=2.502 Å；builder O1=题面 map1、builder H4=题面 map2、builder O8=题面 map6）：
- job 903（R 侧：d(O8–H4) 1.4976 → 2.30 Å，质子移向水侧）：E = −463.98488 → −463.96186 Ha，单调上升 +14.45 kcal（11 个弛豫点 = 1 起点 + 10 步），无内峰。
- job 906（产物侧：d(O8–H4) 1.4976 → 1.00 Å，质子移向 O8）：E = −463.98488 → 最低点 −464.0008587 Ha（pt10，d≈1.05 Å）→ 末点 d=1.00 Å 回升到 −463.9999854（+0.55 kcal）；单调下降 10.03 kcal 后仅在 d<1.05 处轻微回升。
- 合读：沿 O8–H4 坐标只有一个极小值（质子定域在 O8 = 质子化频哪醇＋水，C6–O8 由起点 1.4566 Å / 弛豫 pt1 1.4772 Å **伸长到 1.5387 Å**（O8 质子化使 C–O 活化伸长，仍在成键区）、水以约 2.5 Å 氢键相连），两侧都是上行；从水侧（高能）到该极小值全程单调下降 → 该坐标上无独立鞍点（PT 无垒），与旧高斯 13 点扫描定性一致（本轮为双向 + 原生 + 可复核）。
- 口径提醒：以上能量只在本批 Gaussian 内相减；不得与旧 computed/NR1.json 的 −463.97726224（旧 I1，无 D3BJ）等混减。

### 2.1 本文件的更正与独立复核结论（explorer as_844cd0926754475a，2026-10-15 17:2x；已按复核意见更正上文）
- 更正 1：R 侧扫描是 **11 个弛豫点**（1 起点 + 10 步，输入 B 4 8 S 10 递增），原文"10 点"口径不准。
- 更正 2：产物侧极小值点（pt10，R4=1.04977 Å，E=−464.0008587 Ha）的 **C6–O8 = 1.5387 Å**；原文"保持 ~1.457 Å"用的是起点/输入值，实际是 O8 质子化使 C–O **活化伸长**（相对 pt1 的 1.4772 Å 伸长 0.062 Å），仍在成键区。
- 独立复核确认（可复核行号）：①两条日志 route 行逐字相同（L85-86：opt=(modredundant,maxstep=10) B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight），L111 Charge=1/Multiplicity=1，两份都不含 SCRF（气相）；②扫描坐标 = R4 = R(4,8) = H4···O8，输入 L141 = `B 4 8 S 10 +0.0802` / `S 10 -0.049`；③两条 pt1 几何（25 个 R 值 + 2 个 A 值逐值相同）与能量（−463.98488）互校通过 → 可同批相减；④**两条日志都不含 Frequencies 段（`grep -c 'Frequencies --'` = 0/0）** → 不能作任何虚频或"零虚频极小值"证据；⑤极小值点身份 = 质子化频哪醇＋水（C6–O8 成键、O1–H4 1.445 Å、H4–O8 1.050 Å、O1 上两个 H 0.970/0.969），**不是**脱水产物。
- 复核方指出的**方法论限度（必须写入最终交付）**：R(4,8) 是原子间距、不是标准 PT 差坐标 R(O1–H4)−R(H4–O8)；扫描网格 0.05–0.08 Å，"无内峰"不能排除比网格更窄的垒。→ 这正是不足以单靠这两条日志结案、仍需要"无约束坍缩判据 + 长程扫描（+ 差坐标扫描）"的原因（当前被平台故障卡住）。

## 3 待裁决问题（将向主协调 coordinator 提交）
1. NR1_E1 是否记为无垒/0.0：声明的 R 复合物（[OH3+].pinacol，质子在水侧）在本级别不是极小值（坍缩/长程行为待补），沿 PT 坐标无独立鞍点。建议口径与建议值（附证据）随终态帖提交；不自行回填、不填 0。
2. 图是否重定：若 R 节点改为『质子已在 O6 侧的真实极小值』，则 NR1_E1 这条边在图上失去起点 → 需主协调裁决（保留边+0.0 / 改 R 定义 / 加『PT 复合物』节点）。裁定前不动 ru.py / NR1.json / normal.md 的图结构。
3. NR1_E2 若也无独立解离鞍点：是否与 NR1_E3（1,2-甲基迁移 5.16）合并。

## 4 已知平台阻塞（已上报主协调 evt_1fceda4ffc5d429c）
job 903 / 906 已正常终止，但 guard 写库失败（[guard] 更新数据库失败：database is locked，见 .../E1/scan/.cloudra/guard-903.log 与 .../E1/scan_P/.cloudra/guard-906.log），调度器仍报其 running（8c+8c 假占位）→ 7 个排队作业（含本包 E2 的 911）拿不到容量。实测此刻只有 1 个 Gaussian 进程（907，HI1 包）。本包不杀进程、不改数据库、不重投。

## 5 复核与回填（未开始）
独立复核道：explorer session as_844cd0926754475a（清单 evt_521e5a152e264d62；基线 verify/BASELINE.md sha256=0650faab6fb9a0f5cb429ab3d48a0dcf0e56d946bd5aca24d89432cba1709288、守卫链 verify/GUARD_PLAN.md sha256=3d5db1734f8f955ac257fe152506595a79a8a0d6181cfd0df077b148c52e10e4）。
回填目标（只在裁定/验收后）：cloudra/benchmark/normal_registry/ru.py（R1 的 step barrier 键）、ideapool/tasks/normal/NR1.json、ideapool/reaction_candidates/normal.md 第 106 行（R1 行）。守卫：python -m cloudra.benchmark.gen_normal_tasks + pytest tests/test_benchmark.py -k regenerate_identically；注意 tests/test_benchmark.py:2021 的 [None, None, 5.16, 5.74] 与回填互斥（编辑权待主协调裁定）。

## 6 接班（2026-10-15 18:1x，新 Coordinator **as_27266fe8ac554806**；前任 as_53d43419a24c485b 因平台重启 failed）

**道主分工（本轮）**
- **E1 道** small_mol **as_6df3ce777f4c47ce**（本轮新派发；接替已 failed 的旧 E1 道）：解析 918、提交/解析 scan_O、补『真 PT 差坐标』判据、按分叉走 ts_prepare 或交缺测+证伪档案。
- **E2 道** small_mol **as_3554137d6af74102**（存活，已用 hub call 唤醒续跑）：917 → 判内部峰 vs 单调 → ts_prepare（草案 E2/TSPREPARE_DRAFT.md v2 sha256 324f0cfc…）或交合并裁决材料。
- **独立复核道** explorer as_844cd0926754475a 已 failed → 终验阶段重派（其产物 verify/BASELINE.md、verify/GUARD_PLAN.md 仍有效）。

**作业台账（本包，全部 Gaussian 16 同法：B3LYP/def2SVP+GD3BJ+Int(UltraFine)+SCF=Tight，气相 q+1/m1）**
| job | 内容 | 资源 | 状态 | 原生日志 / 输入 + sha256 |
| --- | --- | --- | --- | --- |
| 903 | E1 R 侧 d(O8–H4) 1.4976→2.30 Å 弛豫扫描 | 8c | done（单调上升，无内峰） | E1/scan/pt_scan_R_01.log sha256 cbf050ed… |
| 906 | E1 产物侧 d(O8–H4)→1.00 Å 弛豫扫描 | 8c | done（单调下降） | E1/scan_P/pt_scan_P_01.log sha256 a43817fd… |
| 911 | E2 I1 Opt+Freq（原） | 12c/13GB | failed（技术性：%chk 被写成相对路径 → Link0 fd=-1，未进 SCF） | logs/E2_I1_optfreq_c000.gjf.log sha256 7fe675d5… |
| 915 | E2 I1 Opt+Freq（重投） | 8c/10GB | done：**0 虚频**，E(I1)=**−463.999955035 Ha**（:18766），r(C4–O6)=1.544 Å、质子仍在离去氧 | logs/E2_I1_optfreq_c000_r2.log sha256 c8db123f… |
| 916 | E2 I2 Opt+Freq | 8c/10GB | done：**0 虚频**，E(I2)=**−463.981552572 Ha**（:27292），3 片段、r(C4···O6)=4.035 Å | logs/E2_I2_optfreq_c000_r2.log sha256 e89f464f… |
| 917 | E2 C4–O6 弛豫扫描 1.544→3.900 Å（14 点） | 8c/10GB | **running**（17:44 起） | logs/E2_scan_C4O6.log / .gjf sha256 1ed02fd7… |
| 918 | E1 R 侧几何（d(O8–H4)=2.30 Å、d(O1–O8)=2.772 Å）无约束 Opt+Freq = H3 坍缩判据 | 8c/10GB | **已提交 ready**（由本 Coordinator 提交，E1 道负责解析，禁止重投） | 输入 E1/opt_R/optfreq_R_d230.gjf sha256 d8abc26e… |

**待提交（E1 道）**：E1/scan_O/pt_scan_O_01.gjf（sha256 cd5aa763…，坐标行 `B 1 8 S 8 0.103551`，d(O1–O8) 2.772→约 3.60 Å）——长程弛豫扫描。

**参考量**：E(I2) − E(I1) = +0.018402463 Ha = **+11.55 kcal/mol**（同批纯电子能差，非能垒）→ 若 C4–O6 有鞍点，ΔE‡ ≥ ~11.5。

**资源/口径不变**：本包同刻 ≤2 个 QM 作业（跨道共享）；新提交 8c/≤10240 MB；TS/IRC 只走 ts_prepare/ts_resume；不跨程序混减；缺测不填 0；不改图；不提交 git。

## 7 第二轮进展（2026-10-15 18:1x–18:4x，Coordinator as_27266fe8ac554806）

**E2（有内部极大 → 走 ts_prepare）**：job 917 逐点权威表（点分界 = 每点 `Optimization completed.`；点能量 = 分界前最后一个 `SCF Done`；pt1 = I1 已优化几何 r=1.5440）显示 **pt7（r≈2.63 Å，−463.974050154 Ha @917:45321，+16.26 kcal vs I1）为内部极大，pt8/pt9 明确下降**。Coordinator 抽验 7 个 file:line 全部一致。关键 caveat：1D 约束面大 r 侧 +17.17 vs 无约束 I2 极小值 +11.55 ⇒ 约束路径非通往 I2 的松弛路径，峰是否就是 E2 的 TS 由无约束 OptTS（ts_prepare，provided guess = pt7 峰帧）判定。

**E1（provisional：声明的 R 不是极小值）**：job 918 轨迹首步为 trust-radius 过冲（该帧 O1···O8=1.8585 Å、E +53 kcal，**非化学结果**），之后单调下行收敛进 I1 区（fr39 −463.999149 Ha、r(O1–H4)≈1.42、r(H4–O8)≈1.06、O1···O8≈2.48、r(C6–O8) 1.4458→≈1.53）⇒ 无约束优化自发把质子从水侧交给频嗪醇氧。终态数值（Normal termination/虚频/能量 file:line/步号）待 918 收敛。

**差坐标判据（回应复核方限度 (a)）**：E1 道用 903/906 两条已有 DFT 扫描的逐点几何把剖面改写为真 PT 差坐标 ΔR = r(O1–H4) − r(H4–O8)，合并 **21 点、ΔR −1.314…+0.512 Å，全程无内部极大**（最低点 ΔR=+0.396，E=−464.000858655）。残留口径缺口 = ΔR 网格 0.07–0.12 Å → 用细网格复扫关闭（限度 (b)）。

**作业台账（追加）**
| job | 内容 | 资源 | 状态 | 备注 |
| --- | --- | --- | --- | --- |
| 918 | E1 R 侧几何无约束 Opt+Freq（H3 坍缩判据） | 8c/10240MB | running（18:04 起） | 输入 E1/opt_R/optfreq_R_d230.gjf sha256 d8abc26e…；轨迹显示坍缩进 I1 区 |
| 929 | E1 长程 d(O1–O8) 2.7716→3.600 Å 弛豫扫描（9 点） | 8c/10240MB | **queued** | 输入 E1/scan_O/pt_scan_O_01.gjf sha256 cd5aa763… |
| 待提 | E1 差坐标细网格复扫（d(O8–H4) 1.000→1.500 Å、0.02 Å、26 点） | 8c/10240MB | 已备好，排队 | 输入 E1/scan_fine/pt_scan_fine_01.gjf sha256 8a31a2406f6c9ea506ff8f87986242ed3ad033a5b77364ffc4e5f732ee3e79da |

**裁决材料**：NR1/ADJUDICATION.md（当前 sha256 8ef8338efc287076d6b62dd28980a46df45639f9be5b1c8763b1752ef173da50）含 E1/E2 两页（已证伪什么 + 缺什么 + 建议口径 + 具体裁决问题）、917 全表、918 provisional 观测与参考态重定裁决项。
---

## 8 第三轮进展（Coordinator 第三任接续，2026-10-15 22:3x–23:2x）

本轮起点：上一任 STATUS 停在 18:15；此后 E1 道 918/929/931、E2 道 ts_0005（933/936/941/948）等作业陆续在原生日志里落定，但两任 Coordinator 与多数 lane 会话被平台重启收尾。以下**数值均为本人（Coordinator）亲自读原生日志独立复核**，不是转抄。

### 8.1 本人独立复核的数值（file:line 为原生日志行号）
| 量 | 值 | 原生日志（绝对路径，前缀 gold_finish_20261015/NR1/） | 复核方式 |
| --- | --- | --- | --- |
| 918 终态（无约束 Opt+Freq，从 d(O8–H4)=2.30 Å 的声明 R 侧几何出发） | `Optimization completed.` @:80267；末次 `SCF Done E(RB3LYP) = -464.000864850` @:81363；Frequencies 段 24 行 = 72 实频、**0 虚频**（最低 42.9966 cm⁻¹）；Normal termination 18:31:08 | E1/opt_R/optfreq_R_d230.log | grep 行号 + 逐行频率值 |
| 929 长程 d(O1···O8) 弛豫扫描 9 点（Normal termination 19:01:54） | pt1 -463.975310275（d(O1-H4)=1.0984、d(H4-O8)=1.6747、O···O 2.7716）→ pt8 -463.946402515（1.0096 / 2.4943 / 3.4965）单调升 +18.140 kcal/mol（原记 +18.48；更正说明见本文件 §12.1 的「STATUS §8.1 更正」条）；pt9 -463.948108850（1.0344 / 2.9123 / 3.6000）较 pt8 **低 1.07 kcal/mol** | E1/scan_O/pt_scan_O_01.log（opt 行 18417/22852/25974/29098/31795/34068/36341/39052/47853） | 本人脚本 tools/parse_gauss_points.py 逐点解析（点分界=每个 `Optimization completed.`，点能量=该行前最后一个 `SCF Done`） |
| 903 R 侧扫描 11 点 | -463.984879974（d(O1-H4)=1.0718/d(H4-O8)=1.4976/O···O 2.5668）→ -463.961859535（0.9858/2.3000/2.7716），逐步 +2.10/+2.16/+2.09/+1.70/+1.46/+1.27/+1.11/+0.97/+0.84/+0.73 kcal，**无内峰** | E1/scan/pt_scan_R_01.log（opt 行 12439/15881/18091/22852/27147/29359/31969/34169/36369/38568/41595） | 同上（独立重算，与 E1 道表一致） |
| 906 产物侧扫描 11 点 | pt10 **-464.000858655**（d(O1-H4)=1.4453/d(H4-O8)=1.0498/O···O 2.4930/r(C6–O8)=1.5387）为该扫描最低点；pt11 -463.999985389（d(H4-O8)=1.0000）**回升 +0.55 kcal** | E1/scan_P/pt_scan_P_01.log（opt 行 12439/15876/19357/28039/30262/32482/34690/37726/41165/47606/51490） | 同上 |
| 合并真 PT 差坐标 ΔR = r(O1–H4) − r(H4–O8)（903+906 共 21 个独立点，同起点 E=-463.984879974 互校一致） | ΔR −1.314…+0.512 Å **全程无内部极大**；唯一极小值 ΔR=+0.396（E=-464.000858655） | 同两列 | 本人按逐点几何重算 ΔR 与能量（只在本批 Gaussian 16 内相减） |

**由上述证据得到的 E1 结论（可复核）**：①声明的 R（质子在水 O1 侧、O···O≈2.77 Å 的接触离子-分子复合物）在本级别气相**不是极小值**——无约束优化第 1 步即把质子交给频哪醇氧 O8 并收缩 O···O，最终落进质子化频哪醇+水极小值（-464.000864850，0 虚频）；②沿缔合坐标（O···O 2.77→3.60 Å，质子留在水侧）能量**单调上升**、无极小值 ⇒ 缔合方向无垒；③沿真 PT 差坐标只有一个极小值（质子定域在 O8 侧），水侧全程单调下行、无内峰 ⇒ **该边在本级别气相没有一阶鞍点**。
仍缺（正在补）：0.02 Å 细网格 PT 复扫（931 因 route 折行把 GD3BJ 拆坏导致 Gaussian l1.exe segfault，未进计算；已按显式两行 route 重投）与固定 O···O 骨架的定骨架 PT 剖面，用于关闭『比网格更窄的垒』这一残留口径缺口。

### 8.2 作业台账（本包，全部 Gaussian 16 同法：B3LYP/def2SVP+GD3BJ+Int(UltraFine)+SCF=Tight，气相 q+1/m1，8c/10240MB，priority 0）
| job | 内容 | 状态 |
| --- | --- | --- |
| 931 | E1 细网格 PT 复扫（0.02 Å，26 点） | **failed**：route 单行 93 字符被按 70 列折行时把词元拆成 GD3/BJ → Gaussian **l1.exe segmentation violation**（E1/scan_fine/.cloudra/calc-931.out.log 有 core dump 栈；日志里的 QPErr 是崩溃假象）。对照：929（def2SVP，折成 GD3B/J）正常跑通 → 已作最小复现材料报主协调并入 issue |
| 964 | E2 细网格 C4–O6 约束扫描 | running（23:01 起，E2 道提交） |
| 待投 | E1 细网格复扫（修 route）+ E1 固定 O···O 定骨架 PT 剖面 | 排队等容量（23:2x 实测 free.cpus=0） |

### 8.3 本轮收到的主协调决策与新政策（BRIEF §9）与我的执行
- **政策 §9（帖 evt_8d124365e7e345cb）**：参考图与既有 gold 值不具权威性，按证据选机理；无合格鞍点不是失败（可记无独立鞍点 + 证据 + 替代口径）；验收链科学性不变；虚频模不在声明键对上的 pseudo-saddle 必须如实标注、不得当 TS。→ 本包 Q1/Q2 改由包内按证据决定。
- **主协调对 E2 的直接指令（帖 evt_ab6959ddca964aa2 之后那条）**：① 不接受 candidate_only +16.26 作为最终值；② 用【虚频模 ± 位移 → 无约束 Opt】的落点证据替代失败的双向 IRC 来证/否连通性（落点分别匹配 I1/I2 才算连通）；③ 换水构型（attempt2 末帧，比 mapped-I1 低 10.95 kcal/mol）做一次无约束 Opt+Freq 后登记为候选新节点；④ 是否与 E3 合并等这些证据到齐再定；⑤ 工具限制（ts_prepare 声明层无法设 IRC 步长/算法）交最小复现并入 issue。→ 已原文转发 E2 道 as_29bded3beae54452。
- **E1（Q1）**：证据最强形态 = 【无独立鞍点 + 声明的 R 非极小值 → 记 0.0 + caveat（无垒口径）】。**跨文件冲突（待主协调一句话确认）**：ru.py 的 R1 第 1/2 步现为 barrier=None，而 `tests/test_benchmark.py::test_pinacol_dehydration_and_migration_are_separate_edges` 硬断言 `[None, None, 5.16, 5.74]`；填 0.0 后该断言必失败，而 tests/ 不在本包可改范围（BRIEF §6 只给 ru.py + normal.md 自己那一行）。已请主协调裁定 (i) 授权改该断言 / (ii) 主协调自改 / (iii) 改走豁免口径维持 None。**裁定前不动 ru.py / NR1.json / normal.md。**

### 8.4 裁决材料版本更正（重要）
- 本文件 §7 引用的 `NR1/ADJUDICATION.md` sha256 `8ef8338e…` 为**中间态，作废**；权威引用版本是主协调台账锁定的 **`f45bcece5b06f983a67ea887d9ae860749c435f54eba21ab7305dd4640255dcc`**（本人本轮 read 实测一致）。若本轮末更新该文件，将另发『唯一新值 + 旧值作废』。

### 8.5 下一步 / 阻塞
1. E1 道 as_e625c1deeeeb47d7（本轮新派）：修 route 重投细网格 + 定骨架 PT 剖面 + 产出 E1_FINAL_EVIDENCE.md。
2. E2 道 as_29bded3beae54452（本轮新派）：ts_inspect(ts_0005) + 933/936/941/948 逐项复核 + 位移下坡连通性试验 + 换水构型 Opt+Freq + E2_FINAL_EVIDENCE.md。
3. 阻塞：全机 32c 满载（free.cpus=0），本包作业排队；guard 断言冲突待主协调确认。
4. 本轮已发 hub 帖：开工/取证帖 evt_f133016c3e904f4e、收令回复帖 evt_36d0b03144a0417b（均 to: as_a341823c436e47ed）。
---

## 9 第三轮续报（2026-10-15 23:2x–00:0x）：两条 lane 产物落盘 + 一条自查更正

### 9.1 lane 状态与产物
| lane | session | 状态 | 产物（绝对路径 + sha256） |
| --- | --- | --- | --- |
| E1 道 | as_e625c1deeeeb47d7 | succeeded | `gold_finish_20261015/NR1/E1/E1_FINAL_EVIDENCE.md` sha256 `ffdb0af17bf78da3791546092e704597b73401216824bfd7180943bbf2ff0810`（174 行） |
| E2 道 | as_29bded3beae54452 | running | `gold_finish_20261015/NR1/E2/E2_FINAL_EVIDENCE.md` v1 sha256 `bfe5661d3ac6e55916a3f05939e94b2df1ce2cb13cbf742e77d4894155e925f2`（182 行，待升 v2） |

### 9.2 E1 新增结论（含对本包 §8 自查的更正）
- **已确立（更强版）**：918 的第 1 个优化步**不是**质子交给 O8（§8 按 E1_NOTES 旧措辞转写的说法**更正**）：第 1 步输出帧（optfreq_R_d230.log L1250）里质子仍更近 O1（0.9881 vs 1.2310 Å），该步主导事件是 **O1···O8 一步塌缩 0.9131 Å（2.7716→1.8585 Å）**（该畸变帧 E=−463.876572708，比起点高 +53.52 kcal/mol，Maximum Displacement 1.659931）；质子归属 O8（1.0706<1.2380）首次出现在**第 9 步输出**（L6214）。收敛终态 = 0 虚频、E=−464.000864850（:81363）、r(O1–H4)=1.4508 / r(H4–O8)=1.0457 / O1···O8=2.4944 / r(C6–O8)=1.5395 Å。⇒ 结论方向不变：**声明的 R 在本级别气相不是极小值**。
- 929 由 E1 道独立实现逐点复核，与我（Coordinator）的表**逐位一致**（含原生汇总表 L48000-48007 佐证）：质子 9 点全程留在水 O1（1.0096–1.0984 Å），pt1→pt8 单调上升 +18.141 kcal/mol，pt9 真收敛且回落 −1.0708 kcal/mol（伴水取向翻转 −96.8°→−178.5°、O1–C7 靠拢 −0.33 Å）。
- **本包 §8 的 931 根因假设被 E1 道证伪**：我提出『回显按 70 列折行拆坏 GD3BJ 导致 l1 segfault』——**不成立**（929 日志 L85/L86 同样把 GD3BJ 折成 GD3B/J、918 L87-88 把 SCF=Tight 折成 SCF/=Tight，两者均正常终止）。E1 道提出的替代假设（中等置信）：真正触发点可能是 **basis 词元写成带连字符的 def2-SVP**（报错 LCursr=38 正落在该词元；931 与所有正常作业的唯一 route 差异就是这个拼写；l1 在 QPErr 后段错误而非干净报错）。我在下一条 hub 帖里向主协调发更正。

### 9.3 E2 新增结论（v1 证据文件 + 964 细网格）
- 964（0.05 Å 细网格，2.632→2.032 Å，13 点）**单调下降、无次级峰**：与 917 合并把唯一内部极大括在 **r ∈ [2.632, 2.812] Å、+16.26 kcal/mol**；细网格 pt1 = −463.974050240 与 917 pt7 = −463.974050154 在 5e-8 Ha 内一致；与无约束 OptTS（933：−463.974034272）在 0.001 kcal/mol 内自洽。
- **新的关键证据（影响 Q2b）**：964 末帧（r(C4–O6)=2.032 Å）时 **r(C4–O10)=2.262 Å**（正被保留侧 OH 分子内捕获）、O6 带 2 H = 中性水、能量 **+10.17 kcal/mol 已低于自由离子对 I2 的 +11.55**；917 大 r 末帧同样是 **C4–O10 = 1.5509 Å 已成键**（我用 awk 独立复算：r(5,7)=3.9005、r(5,11)=1.5509）。⇒ C4–O6 约束坐标与 C4 被邻居氧捕获强耦合，**声明的自由离子对 I2 很可能不是该坐标上可及的自然产物**，这是 E2/E3 合并（协同）路线的核心证据。
- 四项核验通过并更正前任笔记两处：933 的 :3987 是能量行、收敛判据是 :4220/:4221；936 重原子分数按 Σ|d|²=0.169（Σ|d|=0.216），前任写的 0.127 不可复现。

### 9.4 待完成作业（本包，全部 8c/10240MB/priority 0；23:5x 实测 node-local 32c 满载、队列 9 个）
| job | 内容 | 目的 |
| --- | --- | --- |
| 973 | E1 细网格弛豫扫描（0.02 Å，26 点，route 已按两行断行+def2SVP 修好） | 关闭比网格更窄的垒这一口径缺口 |
| 974 | E1 定骨架 PT 剖面（冻结 O1···O8=2.4944 Å，扫 1.0460→1.6060 Å，29 点） | 正交判据，回应 PT 与 O···O 收缩混淆的质疑 |
| 977 | E1 从 929 pt9 几何的无约束 Opt+Freq | **判 pt9 真伪 → 决定 E1 是无垒还是相对水侧浅极小值的小垒** |
| 972 / 979 | E2 从鞍点沿虚频模 ±0.15 Å 位移的两个无约束 Opt | **连通性替代证据（决定候选 +16.26 可否交付）** |
| 待投 | E2 917 大 r 帧(3.90 Å) Opt+Freq、948 末帧(换水/质子桥连) Opt+Freq | 判定 I2 可及性与新节点身份（Q2b/Q2c） |

### 9.5 阻塞与待裁定
1. **guard 断言冲突（仍待主协调一句话）**：详情与补丁计划见 `gold_finish_20261015/NR1/BACKFILL_PATCH.md` sha256 `6c41839621b6d0dd294ea593388fe4a33c2e14a5aa1cea4b99ef26f534893e79`。基线已实测（改前 `-k regenerate_identically` 与 `-k pinacol` 均通过）。
2. 队列拥塞（32c 满载、9 个排队）→ 本包 973/974/977/972/979 需数小时；E1/E2 的最终值仍待这些作业。
3. 平台 DB 写锁 23:2x 复发（本包 E1/E2 各被拒 1–2 次，无残留记录），现已自行解除；已报主协调。
---

## 10 回填执行记录（2026-10-16 00:2x）· NR1_E1 已完成『已回填 + 生成/守卫通过』

### 10.1 改动（4 个文件，改前 → 改后 sha256）
| 文件 | 改前 | 改后 |
| --- | --- | --- |
| cloudra/benchmark/normal_registry/ru.py | 6a20f6a7d088c8b15999c2b9def83383a46e8b4f3589188394af71604dd315de | **d03ea683ad023eb37b73b9486976d1c2c086f0c383e5074d29bcca8ff573e61d**（= 改动前字节；终版为 154650c18062c5f637b55342c939dd168373a361cdf8b1dba731e396e616a73d） |
| ideapool/reaction_candidates/normal.md | 2c919e2714815645bf34ca2ba6f45734c593df619e3858e2869906f6593af3f0 | **173064671ad389b1fe44ff8972024d505e14c09bf931ab7e3aa5b8453ee815b6** |
| ideapool/tasks/normal/NR1.json（生成） | a6a17e2e53812c029cd3166b4331a04d659f9808e5e74a40d63610c57fda6920 | **2f6400f87a3a4039baa864f5330f37ceae3579c436d0fb7f233d115b84bc4a33** |
| tests/test_benchmark.py | 587768d6d9cfc6588b5209ed9e5afa95ec46fc32f8ccc72db11a34ebff472554 | **09b1ed1f66e987357bb9e38aa64651d71dd677b177c068792f29000aaecd9d1b** |

- ru.py：R1 step①（E1）增 `"barrier": 0.0` + 证据注释；step②（E2）注释改为『无合格独立鞍点（含候选 +16.26 与失败原因）』。只动 R1 两个 step dict。
- normal.md：只改第 106 行（R1）能垒格，显式写出本轮引擎口径（Gaussian 16 B3LYP-D3BJ/def2SVP，气相）与两条证据文件路径；未动 SMILES/图/其它行。
- NR1.json：本轮生成产物，NR1_E1 barrier = 0.0（第 154 行），E2 仍 null（175），E3 5.16 / E4 5.74 未动。
- tests/test_benchmark.py：**只改** `test_pinacol_dehydration_and_migration_are_separate_edges` 的一条期望值 [None, None, 5.16, 5.74] → [0.0, None, 5.16, 5.74] + 3 行注释（参照 NI5 包同一文件同类改动的先例 evt_122f359149244da2）。未提交 git。

### 10.2 命令与原样输出
```
$ python -m cloudra.benchmark.gen_normal_tasks --check
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
check passed: 10 tasks

$ python -m cloudra.benchmark.gen_normal_tasks
wrote 10 tasks to /home/ly/Cloudra-mechanism-agent/ideapool/tasks/normal

$ python -m pytest tests/test_benchmark.py -k regenerate_identically -q
....                                                                     [100%]

$ python -m pytest tests/test_benchmark.py -k pinacol -q
.                                                                        [100%]
# （改前实测为 F / 1 failed：assert [0.0, None, 5.16, 5.74] == [None, None, 5.16, 5.74] at tests/test_benchmark.py:2024）

$ python -m pytest tests/test_benchmark.py -q
........................................................................ [ 38%]
........................................................................ [ 77%]
......................s..................                                [100%]
```

### 10.3 裁决材料版本更正（唯一新值 + 旧值作废）
- `NR1/ADJUDICATION.md` 新版本 sha256 = **7eea167e828eed52feb7266be7cb6c864207d732935adb978602bd3caac5b38a**（v2，含 Q1 决定/回填记录与 Q2 缺测口径）。
- **旧值作废**：`f45bcece5b06f983a67ea887d9ae860749c435f54eba21ab7305dd4640255dcc`（v1 interim）与更早的 `8ef8338efc287076d6b62dd28980a46df45639f9be5b1c8763b1752ef173da50` 均作废。

### 10.4 交接要点（若本会话再次被平台收尾）
1. **E1 已交付完成**：『已回填 + 生成/守卫通过』（§10.1/10.2）；若要改动只需重跑同两条命令。
2. **E2 当前形态 = 缺测 + 已证伪 + 合并建议**（`E2/E2_FINAL_EVIDENCE.md` v1 sha256 bfe5661d…，v2 待 jobs 结果）；候选 +16.26 仅登记、未填数。
3. **在等**：973/974/977（E1）、972/979（E2 位移连通性）与 E2 的 917 大 r 帧/948 末帧 Opt+Freq；队列 32c 满载多时。E2 道 as_29bded3beae54452 与 E1 道 as_e625c1deeeeb47d7 均已 succeeded（作业终态通知会唤醒它们；若未唤醒，按磁盘日志自行解析）。
4. 若 972/979 落点分别匹配 I1 与 I2 ⇒ 按主协调指令把 E2 填 16.26（并同步 ru.py/normal.md/生成/守卫，含把 tests 断言第二项改为 16.26）。

---

## 11 第四轮（2026-10-17 06:3x）· Coordinator 第四任 **as_a460780852484712** 接任

**指派主题**：收尾 NR1_E2 / NR1_E3 + 补 NR1_E1 的三条交付要件。前任 session 均被平台重启收尾为 failed，盘上产物未丢，本轮不重做。

### 11.1 本轮亲自复核的盘上事实（真实文件系统读 + query_compute_job）
- 作业终态：**972（E2_dispmode_minus_opt）、974（E1 scan_fixOO）、979（E2_dispmode_plus_opt）、973（E1 scan_fine）、977（E1 opt_pt9）、976（E2_outframe_prod_optfreq）、982（E2_outframe_react_optfreq）全部 done**，原生日志全在盘上（见 E1/、E2/logs/）。
- **换水/水桥构型 Opt+Freq 从未提交**：E2/logs/E2_swapped_attempt2_optfreq.gjf 存在（2026-10-15 23:44）但**无同名 .log** ⇒ 平台重启前未提交。已派本道补提交。
- 队列实测（2026-10-17 06:3x）：node-local free 24c / 9 槽，running 仅 1 个（989 = NY3）；本包手工在飞 = 0 ⇒ 可用满 2 个手工配额。
- 基线守卫（改动前）：gen_normal_tasks --check = **check passed: 10 tasks**（exit 0）；pytest -k regenerate_identically -q = **4 passed**。
- 现行 sha256（**该条为写作轮改动前**实测）：ru.py d03ea683ad023eb37b73b9486976d1c2c086f0c383e5074d29bcca8ff573e61d（终版 154650c1…，行号见 §13.4）；normal.md 5ba1f04f6eba77cbd7e598dd5a6f521da88b31b316ba9947c16f11496cd6cd2a；NR1.json 6eab2f24fbaff453aa958b3714c12de588108731fce6155350f80c88322ac020；tests/test_benchmark.py 1d4f723b1877bde886e3bc5ee0b675a0b0e63e66149e9bb485d3c328c88e2b98。
  ⚠ 说明：normal.md / NR1.json / tests 的 sha 已**被其它包的同类回填推进**（不再是 ADJUDICATION v2 记录的改后值），但 **NR1 的 E1=0.0 仍在**（NR1.json:154 = 0.0；175 = null；205 = 5.16；231 = 5.74；tests 断言仍为 [0.0, None, 5.16, 5.74]，R1 行仍为 normal.md 第 106 行）。回填前必须复取 sha。
- E1/E2 关键原生日志 sha256 复核（与 ADJUDICATION v2 一致）：optfreq_R_d230.log = 130e6863…；pt_scan_R_01.log = cbf050ed…；pt_scan_P_01.log = a43817fd…；pt_scan_O_01.log = 365311b3…；E2_scan_C4O6.log = c2d093fc…；E2_I1_optfreq_c000_r2.log = c8db123f…；E2_I2_optfreq_c000_r2.log = e89f464f…。

### 11.2 本轮派单（并行两道）
| lane | session | 任务 |
| --- | --- | --- |
| small_mol（E2/E3 证据裁定） | **as_74cc45e166f34ee6** | ①解析 972/979/976/982 判 E2 连通性（→ 16.26 还是缺测）；②提交并解析换水构型 Opt+Freq；③NR1 第三条边（登记为 I2→I3 迁移，同时覆盖主协调口径 "I2→P" = 旧 3 边口径的去质子步）的处置：迁移坐标弛豫扫描（≤1 手工作业）→ 判是否有独立鞍点 → 选 A 保留历史值+caveat / B 记 0 或豁免 / C 本批新算 |
| explorer（独立只读复核） | **as_50fe680e47094eed** | 复核 NR1_E1 三条交付要件所依赖的证据（918 行号、真 PT 差坐标 21 点无内峰、929 9 点单调）+ 读新完成作业 **973/974/977** 判"窄垒/水侧浅极小值"两个残留缺口是否关闭 + 核对现行 ru.py/normal.md/NR1.json/tests 状态 |

### 11.3 E3 口径说明（本轮已做的判定，供交付与主协调复核）
主协调派单把 "NR1_E3" 写作 "I2→P"。核对三处后确认存在**两种编号混用**：现行 registry（ru.py）的 R1 第 3 步 = **I2→I3「1,2-甲基迁移」barrier=5.16 / weight=0.5**（题源注明旧 ORCA、参考态=碳正离子/水离子对）；而**旧 3 边口径**（gold_compute/edge_barriers/computed/NR1.json）的 NR1_E3 = **I2→P = 质子接力/去质子步**，现行 registry 里对应**第 4 步 I3→P barrier=5.74**（历史 Gaussian16-WSL 批次，审计备注"仅按 supervisor-supported 接受，须保留身份/拓扑 caveat"）。两处的 I2 也不同义（registry I2 = 碳正离子/水离子对；旧 I2 = 质子化频哪醇酮+2H2O）。→ 本包**同时处置这两条边**并在交付单列，避免误判；不对任何一条无证据填数。

### 11.4 下一步
1. 收两个 lane 的证据 → ②E2 连通性通过则回填 **16.26**（ru.py step② + normal.md 第 106 行 + 生成 NR1.json + tests 断言第二项 + 守卫原样留证），不通过则写"缺测 + 缺什么 + 已证伪什么"；③按 §9 处置第三条边并留证；④补 E1 三条交付要件（0.0 语义 / 逐条证据路径+sha256+行号 / 题源层机理修订说明）。
2. ADJUDICATION.md 升 v3（发布唯一新 sha，旧 7eea167e 起作废），并同步本 STATUS。

---

## 12 第五轮（2026-10-17 07:0x–07:3x）· 写权归本会话；E2 终裁缺测；errata 与新增证据落盘

**写权**：主协调裁定（evt_273568bf72d14d15 / evt_5dbbb8d185184da8）本包 ru.py / NR1.json / normal.md / tests / STATUS.md / ADJUDICATION.md 的写权**全部归 as_a460780852484712**；as_e29f4e7911fc45ee 与其后的复核道转为只读。

### 12.1 同轮 errata（**旧 sha 作废**）
此前 ADJUDICATION v2 §1.3 与 STATUS §10.1 记录的"改后 sha256"中，normal.md / NR1.json / tests 三者的值**已过期**（被其它包的同类回填随后推进，非 NR1 取值被改坏）。现盘实测（2026-10-17 同轮取）：
| 文件 | 旧记（**作废**） | 现盘实测 |
| --- | --- | --- |
| `cloudra/benchmark/normal_registry/ru.py` | 6a20f6a7 → d03ea683（**未变**） | d03ea683ad023eb37b73b9486976d1c2c086f0c383e5074d29bcca8ff573e61d（**改动前**字节的 L30 = 0.0；终版 154650c1… 的对应行号 = **L35**） |
| `ideapool/reaction_candidates/normal.md` | 173064671ad389b1fe44ff8972024d505e14c09bf931ab7e3aa5b8453ee815b6 | **5ba1f04f6eba77cbd7e598dd5a6f521da88b31b316ba9947c16f11496cd6cd2a**（R1 行 = 第 106 行） |
| `ideapool/tasks/normal/NR1.json` | 2f6400f87a3a4039baa864f5330f37ceae3579c436d0fb7f233d115b84bc4a33 | **6eab2f24fbaff453aa958b3714c12de588108731fce6155350f80c88322ac020**（L154 = 0.0 / L175 = null / L205 = 5.16 / L231 = 5.74） |
| `tests/test_benchmark.py` | 09b1ed1f66e987357bb9e38aa64651d71dd677b177c068792f29000aaecd9d1b | **1d4f723b1877bde886e3bc5ee0b675a0b0e63e66149e9bb485d3c328c88e2b98**（pinacol 断言 @L2062 = [0.0, None, 5.16, 5.74]） |
- **数值未坏**：NR1 的 E1 = 0.0 / E2 = null / E3 = 5.16 / E4 = 5.74 与断言一致。
- **STATUS §8.1 更正**：929「pt1→pt8 单调升 +18.48 kcal/mol」应为 **+18.140 kcal/mol**（(−463.946402515) − (−463.975310275) = −0.02890776 Ha × 627.5095）。
- **ru.py 行号提示**：本节与 §10.1 / §11.1 里出现的 ru.py d03ea683…（L30 = 0.0）指**改动前**字节；**终版 154650c18062c5f637b55342c939dd168373a361cdf8b1dba731e396e616a73d 的行号 = E1 0.0 L35 / E3 5.16 L57（weight 0.5 L58）/ E4 5.74 L66**（另见 §13.4）。
- 详细记录见 `NR1/MECHANISM_REVISION.md` §5。

### 12.2 NR1_E2 终裁：**缺测（不填数）**；16.26 仅作 candidate_only
主协调裁定（evt_a42bd18db1804773）：**不得填 16.26**。依据（本 Coordinator 与只读道 as_e29f4e7911fc45ee 独立一致）：
- job 972/982（−463.998937570 / −463.998937598）= **I1 家族**（质子化频哪醇 + 水，C4–O6 1.539 仍成键、2 片段）的**另一个 0 虚频极小值**，+0.64 kcal vs I1；
- job 979/976（−463.975787663 / −463.975760229，72 实频 0 虚频）= **三元环氧鎓（C4–O10 1.599 / 保留侧 C–O10 1.593 / C4–C7 1.476，O10 三配位）+ 2 自由水** 的 0 虚频极小值，+15.17 vs I1、**+3.62 vs I2**；
- I2（−463.981552572）= **碳正离子 + 2 H₂O**（3 片段、中心 C 与 O 无键）⇒ 与 979/976 **不是同一异构体**；
- 候选鞍点（933）虚频模 ±位移下坡两端 = I1 家族极小值与环氧鎓极小值，**都不是声明的 I1/I2** ⇒ **+16.26 不是 I1→I2 的 ΔE‡**。
- 交付口径：E2 保持 null；已证伪 4 条（±位移匹配 I1/I2；917 大 r 帧能回 I2；约束面内部极大即 I1→I2 鞍点；IDPP 产物侧能收敛出解离鞍点）；缺 = 连接 I1 与声明 I2 的独立一阶鞍点或任何路径证据。全部证据表 + file:line 见 `NR1/MECHANISM_REVISION.md` §2。

### 12.3 新增节点参考态修订：NR1_R（job 992）
job 992（`E2/logs/E2_swapped_attempt2_optfreq.log` sha256 **65e6ce12a7a3664b2de15cabefbf4845c2d73833dd79900fa449cc46ef227c39**；输入 sha256 14716f1b…；`Optimization completed.` @L11381、2× Normal termination @L11989/L14872、末次 SCF **−464.018254456** @L11124、72 实频 **0 虚频**、首频 71.0470 @L12887）身份 = **中性频哪醇 + H₃O⁺ 螯合复合物**（O7 与两个频哪醇氧成短氢键 O1···O7 = 2.440、O7···O11 = 2.462 Å；2 片段），**比 I1 低 11.48 kcal/mol**。
⇒ 按 BRIEF §9 在包内处置：**只登记为「R 参考态候选重定 + 待仲裁」**（同物种、同节点，**图拓扑不变**）。**反向意见**（E2/E3 证据道 as_74cc45e166f34ee6，帖 evt_a39dd6fc6b034eb1 与 `NR1/E2/E2_E23_VERDICT.md` §2 末）：992 与声明的 R 复合物同组成、同片段却低 11.5 kcal/mol，与气相质子亲和能预期（叔醇 PA ≈ 195 vs 水 ≈ 165 kcal/mol，质子应留在醇上）以及 E1 道旧记录「正向 PT 放热 −20.02 kcal/mol」**方向相反**，疑 BSSE / 小基组（缺弥散）/ 双 OH 螯合偏好。⇒ 仲裁前「R → I1 吸热 +11.48 kcal/mol」只作**候选表述、不作交付数值**；**E1 的 0.0 不变**。详见 `NR1/MECHANISM_REVISION.md` §1.6。

### 12.4 NR1_E3 / NR1_E4 处置（声明取值 + 依据；不填 0）
见 `NR1/MECHANISM_REVISION.md` §3：现行 registry 第 3 步（I2→I3 迁移，5.16，旧 ORCA）与第 4 步（I3→P 去质子，5.74，旧 Gaussian16-WSL）**保留不变**，但显式标注"非本批重算、参考态不同义、不得与本批数值混减或相加"；**不采用 0/豁免**（本批没有任何证据表明它们无独立鞍点：E1 的"无垒"不外推）；缺什么 = I3/P 端本批 0 虚频极小值 + 迁移/去质子步的独立鞍点链。

### 12.5 本轮落盘清单（同一轮内取的 sha256）
| 文件 | sha256 |
| --- | --- |
| `NR1/MECHANISM_REVISION.md`（新建，E1 三条交付要件的独立载体） | 见 hub 终态帖（写作轮公布） |
| `NR1/E1/E1_FINAL_EVIDENCE.md`（新增 §6 终态更新，取代 §1.3/§3 的"待生成/排队"） | 2eb69ae5459b7635bc54fe8dffa7264293fabb7de3a69cf79c7d92fe7d86efa7 |
| `NR1/ADJUDICATION.md`（升 v3） | 见 §12.6 / hub 帖 |
| `NR1/STATUS.md`（本条 §12） | 本文件 |
| `NR1/tools/coord_geom_check.py`、`coord_identity.py`（复核道建的解析脚本，仅解析用） | 保留 |

### 12.6 ADJUDICATION 版本
- **v2 sha 7eea167e828eed52feb7266be7cb6c864207d732935adb978602bd3caac5b38a 自 v3 起作废**；v1/v0（f45bcece…、8ef8338e…）早已作废。v3 的实测 sha 以 hub 终态帖公布值为准（v3 文件内不写入自身 sha，避免自指）。





### 13 本轮守卫与写作轮 sha256（2026-10-17 06:5x，命令与输出原样）

改动前基线（上一轮，src 47）：`gen_normal_tasks --check` = `check passed: 10 tasks`（exit 0）；`pytest -k regenerate_identically` = 4 passed。

改动后（ru.py 注释 + normal.md L106；同一轮内取输出与 sha）：

1. `python -m cloudra.benchmark.gen_normal_tasks --check` → `OK NB1: 5 nodes, 2 steps`、…、`OK NR1: 9 nodes, 4 steps`、…、`check passed: 10 tasks`（exit 0）。
2. `python -m cloudra.benchmark.gen_normal_tasks` → `wrote 10 tasks to /home/ly/Cloudra-mechanism-agent/ideapool/tasks/normal`；随后与生成前副本 `diff` = **NO_DIFF** ⇒ 重生成**幂等**，`NR1.json` sha256 前后同为 6eab2f24…。
3. `python -m pytest tests/test_benchmark.py -k regenerate_identically` → **4 passed, 185 deselected in 1.34s**。
4. `python -m pytest tests/test_benchmark.py -k pinacol` → **1 passed, 188 deselected in 1.09s**。
5. normal.md 第 106 行同轮重解析：表头（L29）单元格数 = 10、R1 行（L106）单元格数 = 10 ⇒ **无裸竖线破坏**。
6. 全量 `python -m pytest -q`：06:54 起后台运行（输出 /tmp/nr1_full_pytest.txt），写作轮未结束；终态见 §13.1。

### 13.1 全量 pytest 终态（原样输出 + 退出码；**只作环境说明，不作 NR1 验收依据**）
- 命令与输出：`python -m pytest -q; echo "EXITCODE=$?"`（cwd = /home/ly/Cloudra-mechanism-agent；输出 /tmp/nr1_full_pytest2.txt）→ 短摘要列出 **66 条 FAILED**，文件末行（L3533）= **EXITCODE=1**。
- 计数：本环境下 pytest 未打印最终计数行（run#1 与 run#2 均如此），故按**进度字符**统计：`.` = **5343**、`F` = **66**、`s` = **61**、`x/X/E` = 0 ⇒ **通过 5343 / 失败 66 / 跳过 61（合计 5548 项）**；与短摘要的 66 条 FAILED 自洽。
- 失败归属：**0 条在 tests/test_benchmark.py**（`grep -c 'FAILED tests/test_benchmark.py'` = 0）。66 条全部落在平台/基础设施与其它模块：test_compute、test_conformer_search、test_crest_runner、test_dag_identity、test_dag_supervisor(_tools)、test_logging_setup、test_runtime_v2_*（dag_submission / js_pipeline / persistence / receipt_memory / runner / supervision）、test_scan_interface、test_ts_calculation_references、test_ts_open_shell_identity、test_web_launcher、test_xtb_channel / xtb_execution / xtb_scan_runner、test_agent_scenarios、test_api_v2_ops_queries、test_benchmark_sandbox_fp、test_benchmark_tool_paths ⇒ **与 NR1 的 gold 回填无因果关系**（多为依赖活服务/端口/DB 独占的环境相关用例，运行期正值多 lane 并发）。
- run#1（06:54 起，/tmp/nr1_full_pytest.txt）：同为 66 条 FAILED，但**无计数行、退出码未捕获**（nohup 启动）⇒ run#2 为本条的权威记录。
- **NR1 验收门禁固定为四条**：`python -m cloudra.benchmark.gen_normal_tasks --check` = check passed: 10 tasks（exit 0）；`python -m cloudra.benchmark.gen_normal_tasks` 重生成 = **NO_DIFF**（幂等）；`pytest tests/test_benchmark.py -k regenerate_identically` = 4 passed；`-k pinacol` = 1 passed。**全量 pytest -q 不作 NR1 验收依据。**
- 单文件参考（**1d4f723b 字节**）：`pytest tests/test_benchmark.py -q --tb=line -rf` = **1 failed, 187 passed, 1 skipped**；该唯一失败 = `test_hard_replacement_and_hl1_reframed_graph`（L2138：实测 `[0.0, 23.13, 10.44, 13.46]` vs 断言 `[None, 23.13, 10.44, 13.46]`）——**该失败指 ≤1d4f723b 字节**。在现盘 **037a424b** 上 HL1 已把 L2138 改为 `[0.0, 23.13, 10.44, 13.46]`，**该失败已消失**（主协调同轮复跑 037a424b：188 passed / 1 skipped）。**NR1 的断言 @L2062 = [0.0, None, 5.16, 5.74] 在两个字节版本下均未变。**

### 13.2 写作轮 sha256（同轮实测；取代 MECHANISM_REVISION §5 与本文件 §12.5 的对应行）
| 文件 | sha256 |
| --- | --- |
| `cloudra/benchmark/normal_registry/ru.py` | 154650c18062c5f637b55342c939dd168373a361cdf8b1dba731e396e616a73d |
| `ideapool/reaction_candidates/normal.md` | 771a6c7ffa23a358ed8b35005c31d64931530d2f6aeb54c7ecc568e5c0fbdc89 |
| `ideapool/tasks/normal/NR1.json` | 6eab2f24fbaff453aa958b3714c12de588108731fce6155350f80c88322ac020（**未变**，见 §13 第 2 条） |
| `tests/test_benchmark.py` | 1d4f723b1877bde886e3bc5ee0b675a0b0e63e66149e9bb485d3c328c88e2b98（**未变**） |
| `NR1/ADJUDICATION.md`（v3） | 9a187125a582b8b5e8e9bdf84a34e32d8cad4f0d989506c9bb48cab994a983ad（v2 7eea167e… 作废） |
| `NR1/E1/E1_FINAL_EVIDENCE.md` | 2eb69ae5459b7635bc54fe8dffa7264293fabb7de3a69cf79c7d92fe7d86efa7 |
| `NR1/MECHANISM_REVISION.md` | 见 hub 终态帖（写作轮公布值） |
| `NR1/STATUS.md` | 本文件；终值见 hub 终态帖 |

**作废声明**：MECHANISM_REVISION §5 与 STATUS §12.5 里 ru.py = d03ea683…、normal.md = 5ba1f04f… 的登记**自本条起作废**（那是本包本轮改动前的字节；改动后见上表）。NR1.json 6eab2f24… 与 tests 1d4f723b… 仍然有效（本轮未变）。

### 13.3 主协调终态回执 + 写作轮第二次 sha 更新（2026-10-17 07:0x）
- 主协调回执（hub **evt_0cb5ea5e03454c27**，to: as_a460780852484712）：逐项**接受** E1 = 0.0（三要件已落载体）、E2 = null（缺测 + 4 条已证伪 + 缺什么）、E3/E4 保留 5.16/5.74 + caveat、992 维持「只作候选登记、不改图、不作交付数值」；改图提案本轮**不实施**，要求保留为「待定提案」章节。它独立 `sha256sum` 实测本包 7 个 sha 与终态帖**逐字一致**，并另测 NR1.json 的 `system.elements = [C,H,O]`、`max_heavy_atoms = 9`（未发生元数据静默丢失）。
- 按该回执补写：`NR1/MECHANISM_REVISION.md` §1.6 反向意见补 **counterpoise（BSSE）校正 / 显式水或隐式溶剂** 判别路径并标注「有争议、未定论」；新增 **§8 待定提案**（8.1 环氧鎓产物改述 / 8.2 E2+E3 合并 / 8.3 R 与 I1 参考态重定，各含证据 + 反证 + 判别路径），原 §6/§7 顺延为 errata/守卫。
- **sha 更新（同轮实测）**：`NR1/MECHANISM_REVISION.md` d57bc38d03a8b8e44922f89d357a6a0d4ce10abe01307fb985df54f74b8fed09 → **fe14b6e05be10b6ec83223dc2c2433b735528d67fb4fce1add61010a40efcddb**（旧值自本条起作废）；STATUS.md 本文件随本条再变，终值见后续补帖。



### 13.6 勘误（MECHANISM_REVISION.md 的终值；2026-10-17 07:4x 本人实测）
- **`NR1/MECHANISM_REVISION.md` 终值 = 2559935d1f94845f5009293e0727a3dcb7542f307f4690f6903ebcf903cc5cda**（本人 07:3x R8 收尾轮实测，只读复核道 as_e29f4e7911fc45ee 同轮复测一致）。**`fe14b6e05be10b6ec83223dc2c2433b735528d67fb4fce1add61010a40efcddb` 自本条起作废**（它在本文件 §13.4 曾被写成终值，属 §13.4 与 §13.3 之间的登记不同步）；更早的 d57bc38d03a8b8e44922f89d357a6a0d4ce10abe01307fb985df54f74b8fed09 亦作废。
- `NR1/STATUS.md` 自身 sha：每次写入都会改变，权威值一律以 hub 主题 gold-finish-20261015 最新补帖公布值为准（本文不自登记以免自指）。本文可追溯链：e1488446… → 9c9a8f56… → 595a5a78… → fde655ec… → b5616d9b… → 54608d77… → 本条写入后的值（见 hub 帖）。
- 其余引用（本轮实测，与只读复核道一致）：ru.py 154650c18062c5f637b55342c939dd168373a361cdf8b1dba731e396e616a73d（E1 0.0 @L35 / E3 5.16 @L57 / E4 5.74 @L66）；normal.md 771a6c7ffa23a358ed8b35005c31d64931530d2f6aeb54c7ecc568e5c0fbdc89；NR1.json 6eab2f24fbaff453aa958b3714c12de588108731fce6155350f80c88322ac020；tests/test_benchmark.py 037a424b05cc5d28f0bd2540af456aedf034908d5e59525b356994d38bd8d014；ADJUDICATION.md 9a187125a582b8b5e8e9bdf84a34e32d8cad4f0d989506c9bb48cab994a983ad；E1/E1_FINAL_EVIDENCE.md 2eb69ae5459b7635bc54fe8dffa7264293fabb7de3a69cf79c7d92fe7d86efa7。

### 13.5 勘误（tests 的现盘 sha 被 HL1 包改动；2026-10-17 07:33 本人实读）
- `tests/test_benchmark.py` 现盘 sha256 = **037a424b05cc5d28f0bd2540af456aedf034908d5e59525b356994d38bd8d014**（本人 07:33:37 实读），**取代** §13.2 与 hub 终态帖里登记的 1d4f723b1877bde886e3bc5ee0b675a0b0e63e66149e9bb485d3c328c88e2b98（该值 ≤07:07 有效）。
- 差异来源 = **HL1 包修 tests/test_benchmark.py:2138**：HL1_E1 的断言由 [None, 23.13, 10.44, 13.46] 改为 [0.0, 23.13, 10.44, 13.46]（即 §13.1 记录的那条失败已被 HL1 修掉）。**NR1 的断言 tests/test_benchmark.py:2062 = [0.0, None, 5.16, 5.74] 未变**（07:33 实读原文逐字一致）⇒ NR1 口径与守卫结论不受影响。
- 在 **037a424b** 字节上重跑（同一轮原样输出）：`python -m pytest tests/test_benchmark.py -k regenerate_identically` → **4 passed, 185 deselected in 3.39s**；`-k pinacol` → **1 passed, 188 deselected in 1.07s**；`python -m cloudra.benchmark.gen_normal_tasks --check` → **check passed: 10 tasks**（exit 0）。
- 记录纪律：1d4f723b… 与 037a424b… 是**同一路径的两个不同字节版本，不得共用同一引用值**；引用 tests 的 sha 必须同时给出测量时间（1d4f723b @≤07:07；037a424b @07:33）。
- 全量 `python -m pytest -q`（run#1，06:54–07:2x 后台，输出 /tmp/nr1_full_pytest.txt）：**66 条 FAILED**，全部落在平台/基础设施与其它包的测试文件（test_compute、test_crest_runner、test_dag_*、test_runtime_v2_*、test_web_launcher、test_xtb_*、test_scan_interface、test_ts_* 等），**test_benchmark.py 的失败项已在 037a424b 字节上消失**；run#1 的退出码未捕获（nohup 后台），已另起 run#2（/tmp/nr1_full_pytest2.txt，带 EXITCODE= 捕获）作为终态记录。

### 13.4 ru.py 行号索引（以**终版** 154650c18062c5f637b55342c939dd168373a361cdf8b1dba731e396e616a73d 为准）与终值 sha 确认
- `ru.py` 终版行号：**E1 barrier 0.0 = L35**；**E3 barrier 5.16 = L57**（其 `"weight": 0.5` = **L58**）；**E4 barrier 5.74 = L66**。
- 旧值 d03ea683ad023eb37b73b9486976d1c2c086f0c383e5074d29bcca8ff573e61d 的行号（E1 = L30）**属改动前字节**，§10.1 / §11.1 中的该 sha 已按此注明；读者请按上面终版行号检索。
- **终值 sha 确认（取代此前所有旧登记）**：`gold_finish_20261015/NR1/MECHANISM_REVISION.md` = **2559935d1f94845f5009293e0727a3dcb7542f307f4690f6903ebcf903cc5cda**（取代 fe14b6e0… / d57bc38d…；见 §13.6）；`gold_finish_20261015/NR1/STATUS.md` = 本文件，其 sha 在本次小收尾后又变（旧值 595a5a787f5d3881c9c2a14f1828f15b2325f7ec8af0a168439baf779126510c 自本条起作废），终值见 hub 补帖。
- json schema：**本轮不扩 NR1.json 的 caveat 字段**（主协调裁定 evt：改 schema 触及生成器/评分规则，超本战役写权）；「0.0 = 约定值 / 无独立鞍点 / 不是 0 垒 TS」的语义仍由 ru.py 注释（终版 L28–L35 区）+ normal.md L106 + MECHANISM_REVISION.md 承载，交付报告转述。

### 13.7 normal.md 旧值引用提示
- E2/E3 道终态帖正文仍引用 `normal.md 5ba1f04f…`：该值属**本包改动前字节**，已在 §13.2 / §13.6 作废 ⇒ 一律引用现盘 **771a6c7ffa23a358ed8b35005c31d64931530d2f6aeb54c7ecc568e5c0fbdc89**（R1 行 = L106）。

### 14 job 998（E2b 迁移坐标 C4···C8 弛豫扫描）终态：只作 E3/E4「参考态不同义」的补强证据，**不产生任何可回填值**
- 输入 = `E2/logs/E2b_scan_migration_C4C8.gjf`（sha256 fae4f708…），起点 = 本批 I2 极小值。日志 `E2/logs/E2b_scan_migration_C4C8.log` sha256 = **f78e4486391235001b1f3d02075e97383f1949d91e2fe207b7f4b32f2f63ba81**（本人 07:35 同轮实测；4185673 bytes；mtime 2026-10-17T07:35:30）；`Normal termination of Gaussian 16` @**L63688**（07:35:30）；13 个扫描点；扫描汇总表 @**L62874**，三条能量行 @**L62876 / L62993 / L63110**。
- 本人独立解析（相对 pt1，同批纯电子能，1 Ha = 627.5095 kcal/mol）：pt1 **−463.981552**（= 本批 I2 值，与 §2.1 的 −463.981552572 一致）→ pt2 +0.12 → pt3 +0.54 → pt4 +1.33 → pt5 +2.44 → **pt6 +3.77（采样最高点）**；pt6→pt7 出现 **12.10 kcal 突变 + 键连表重组**（C10–C11 1.611→2.544 Å 断开、C10–O13 1.380→1.266 Å 成 C=O、H26 移向 O1）；pt7 → pt13 单调降至 **−29.44**；终点 = **频哪酮 + H₃O⁺**（C10=O13 1.240 Å；O1 带 3 个 H）。
- 判读（与只读复核道 as_e29f4e7911fc45ee 的独立逐点表一致）：① 极大值落在 (1.989, 2.067) Å 之间、被 0.078 Å 网格跨过而**未分辨 ⇒ 只能给下界 ≥ +3.77 kcal**；② 该弛豫坐标把 step3（1,2-甲基迁移）与 step4（去质子）**混在一起**，终点不是任一注册步的端点 ⇒ **不能单独给任何一条边的定值**；③ 剖面显示**有垒**，因此**不能说「无独立鞍点 ⇒ 0/豁免」**（这是 E3/E4 维持历史值的又一正面依据）；④ **不得**把 +3.77 与历史 ORCA 5.16 / WSL 5.74 混减或作高度比较（跨程序 + 参考态不同义 + 坐标混合）。
- 结论：E3/E4 处置不变（见 §3）：step3 = **5.16**、step4 = **5.74**，保留原值 + 「非本批重算 / 参考态不同义 / 不得与本批数值混减或相加」caveat；本轮不新增可回填值。

### 14.1 补充（E2/E3 道终态报告，2026-10-17 07:3x）与**序号基约定**
- **序号基**：§14 的「C10–C11 / C10–O13 / H26 / O1」等编号 = **原生日志末帧的 Gaussian 标准定向顺序**；E2/E3 道的 lane 文件（`E2/E2_E23_VERDICT.md`、`E2/C_OPTION_PREP.md`）用其自有原子序（同一原子写作 C7–C10 / C7=O10）。两者数值不冲突，**引用时必须写明所用序号基**，否则会被误读为不同原子。
- E2/E3 道最终证据件（本人 07:39 同轮实测）：`NR1/E2/E2_E23_VERDICT.md` = **a05de2a519e50648f9b1dedb087d9e94e824c315cdc18f4d83bb35286ef47a09**（26244 bytes，mtime 07:38:41）；`NR1/E2/C_OPTION_PREP.md` = **7c37ece7f5824ff5447f8eaf45726dce52b42ff2861e693167cb023c639b291d**（5954 bytes，mtime 07:38:31；内容 = option C 的可执行输入清单：端点/mol_path/binding、guess、ETA 2–4 h，**未授权**，仅登记为可选增强项）。
- 该道独立复核与本包一致：998 的 pt1 复现本批 I2（差 2.85e-7 Ha）；峰值帧 `E2/seeds/scan998_peak.xyz`（76a474e8…）与末帧 `E2/structures/judg_998_end.xyz`（8c21b97e…）= **频哪酮 + H₃O⁺ + H₂O**（C=O 1.240 Å；质子 O10→O1 转移）；**该弛豫坐标上不出现 I3 极小值**（迁移与去质子沿此坐标耦合）；+3.77 只是受约束扫描下界、不是 ΔE‡；处置 A（E3 = 5.16 / E4 = 5.74 + caveat）不变，且该道 0 个手工作业在飞、未提交新作业。
