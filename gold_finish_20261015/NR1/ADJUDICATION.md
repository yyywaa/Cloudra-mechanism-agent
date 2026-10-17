# NR1 裁决材料 v2（FINAL for Q1 · Q2 缺测口径）

> 维护：NR1 包 Coordinator **as_a2aa6951d46042ae**（第三任）。
> **版本锁**：本文件上一引用版本 sha256 `f45bcece5b06f983a67ea887d9ae860749c435f54eba21ab7305dd4640255dcc`（interim v1）**自本版起作废**；唯一有效版本 = 本文件当前 sha256（见文末“版本”节，亦随 hub 帖发布）。
> 口径：Gaussian 16 Rev C.01 `/home/ly/g16/g16`，`B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight`，气相（无 SCRF），q=+1/m=1，26 原子 C6H17O3。ΔE 只取纯电子能（SCF Done），**只在同一批本包 Gaussian 16 日志内相减**；不与旧 ORCA/历史值混减。缺测不填数、不改图；任何数值都能由“绝对路径 + sha256 + file:line”复核。

## 0 结论速览
| 边 | 处置 | 值 | 依据（一句话） |
| --- | --- | --- | --- |
| **NR1_E1**（H3O+ → 频哪醇 OH 的 PT） | **已回填**：按“无独立鞍点 / 无垒”记 **0.0 kcal/mol + caveat** | ru.py R1 step① barrier = 0.0 | 声明的 R 复合物不是极小值（无约束 Opt+Freq 塌缩到质子化频哪醇+水 0 虚频极小值）；真 PT 差坐标 21 点剖面与长程 O···O 9 点剖面均无内峰 ⇒ 无 TS、无垒 |
| **NR1_E2**（质子化频哪醇脱水，C4–O6 异裂） | **缺测（不填数）** + 已证伪 + 合并建议 | barrier_kcal_mol = null | 无合格独立鞍点：唯一内部极大 r∈[2.632,2.812] Å / +16.26 kcal/mol 对应的无约束 OptTS 恰 1 虚频但为软模 −74.5623 cm⁻¹，native IRC 积分失败 ⇒ 连通性未证；且约束面两侧都出现 C4 被相邻氧分子内捕获 ⇒ 声明的自由离子对 I2 可能不可及 |

## 1 Q1 · NR1_E1（已决定并回填）
### 1.1 已确立（可复核数值）
1. **声明的 R 不是极小值**：`gold_finish_20261015/NR1/E1/opt_R/optfreq_R_d230.log`（sha256 `130e686378d8393402f86c74cc017cf8a20b175e2f7549900b77092936fbf407`）从声明 R 几何（d(O8–H4)=2.30 Å、O1···O8=2.7716 Å）出发的无约束 Opt+Freq：第 1 个优化步即把 O1···O8 塌缩 0.9131 Å（2.7716→1.8585，L1250，该畸变帧 +53.52 kcal/mol、Maximum Displacement 1.659931），质子归属 O8 出现在第 9 步输出（L6214）；收敛终态 `Optimization completed.` @L80267、末次 `SCF Done` **−464.000864850 Ha** @L81363、72 实频 **0 虚频**（最低 42.9966 cm⁻¹ @L81791），末帧 r(O1–H4)=1.4508 / r(H4–O8)=1.0457 / O1···O8=2.4944 / r(C6–O8)=1.5395 Å。
2. **真 PT 差坐标剖面无内峰**：903 + 906 两条弛豫扫描（`E1/scan/pt_scan_R_01.log` sha256 `cbf050ed…`；`E1/scan_P/pt_scan_P_01.log` sha256 `a43817fd…`）的逐点几何合并为 ΔR = r(O1–H4) − r(H4–O8) 的 21 个独立点：ΔR −1.314…+0.512 Å **全程无内部极大**，唯一极小值 ΔR=+0.396（E=−464.000858655 Ha，该点 r(C6–O8)=1.5387 Å）。
3. **长程 O···O 剖面：质子全程在水侧且能量单调上升**：`E1/scan_O/pt_scan_O_01.log`（sha256 `365311b339474956bb33e3b048f6f992e66ebf05a61abbc6193b5a117e8d76b6`，Normal termination @L48745）9 点逐点（点分界 = 每个 `Optimization completed` 行；点能量 = 该行前最后一个 `SCF Done`）：pt1 −463.975310275（O1···O8=2.7716）/ pt2 −463.969890450 / … / pt8 −463.946402515（3.4965）/ pt9 −463.948108850（3.6000）。质子 9 点全程 r(O1–H4)=1.0096–1.0984 Å ≪ r(H4–O8)=1.6747–2.9123 Å。**pt9 比 pt8 低 1.071 kcal/mol**（两点均真收敛；几何上 pt8 近线性氢键 171.8°，pt9 弯折 124.4° + 水取向翻转 −96.8°→−178.5°）。
   该文件的 Coordinator 独立复核（本人脚本 `NR1/tools/parse_gauss_points.py`，2026-10-15 23:2x）与 E1 道的独立实现逐位一致；原生汇总表 L48000-48007 亦佐证。
### 1.2 已证伪 / 更正
- **证伪**：沿 d(O8–H4) 的 R 侧上行段 ⇒ 存在 R 侧极小值 —— 903/906 合并剖面单调（无内峰）。
- **证伪**：声明的 R（质子在水侧、O···O=2.7716 Å）是极小值 —— 918 无约束优化塌缩（§1.1-1）。
- **更正（本包自查）**：v1 与 E1_NOTES §4.3 曾写“918 第 1 步即把质子交给 O8”；实测第 1 步的主导事件是 O1···O8 塌缩、质子仍更近 O1，质子归属 O8 出现在第 9 步输出。结论方向不变。
- **更正（本包自查）**：v1 曾把 job 931 的 l1 段错误归因于“Gaussian 回显按 70 列折行拆坏 GD3BJ”；E1 道用 929/918 两条反例（同样折行、正常终止）**证伪**该归因。替代假设（中等置信、未定论）：basis 词元写成带连字符的 `def2-SVP`。
### 1.3 决定与回填记录（本包按 BRIEF §9(1)(2)(4) 自行决定）
采取 **0.0 + caveat**（对照选项：正式豁免 / 重定 R 节点）：证据表明该步在本级别气相**没有一阶鞍点**，0.0 是“无垒”的直接编码，且使该边可评分（先例：yo.py O3 第 1 步、NI1）。**caveat**：(a) 本值不是由 TS 得到的 ΔE‡，而是“无垒”的约定值；(b) pt9 身份（水侧是否存在 ~3.6 Å 的浅极小值）正由 job 977 判定，若其确为极小值，本步的垒也只是 pt8/pt9 之间约 1 kcal/mol 量级（远小于 rubric 的 small_barrier_threshold=10），届时按同一证据基础修订单个数值即可；(c) 程序偏差：本轮为 Gaussian 16，既有 58 条 gold 为 ORCA，跨程序不混减。
**回填改动（4 个文件）**：
| 文件 | 改前 sha256 | 改后 sha256 | 内容 |
| --- | --- | --- | --- |
| `cloudra/benchmark/normal_registry/ru.py` | `6a20f6a7d088c8b15999c2b9def83383a46e8b4f3589188394af71604dd315de` | `d03ea683ad023eb37b73b9486976d1c2c086f0c383e5074d29bcca8ff573e61d` | R1 step① 增 `barrier = 0.0` + 证据/口径注释；step② 注释改为“无合格独立鞍点（含候选与失败原因）”。**只动 R1 的两个 step dict** |
| `ideapool/reaction_candidates/normal.md` | `2c919e2714815645bf34ca2ba6f45734c593df619e3858e2869906f6593af3f0` | `173064671ad389b1fe44ff8972024d505e14c09bf931ab7e3aa5b8453ee815b6` | 第 106 行（R1）能垒格改写：E1 = 0.0（口径+依据）、E2 = null（缺测原因）、E3/E4 保留、引擎偏差显式写出、附证据文件路径。未动 SMILES/图/其它行 |
| `ideapool/tasks/normal/NR1.json`（生成产物） | `a6a17e2e53812c029cd3166b4331a04d659f9808e5e74a40d63610c57fda6920` | `2f6400f87a3a4039baa864f5330f37ceae3579c436d0fb7f233d115b84bc4a33` | NR1_E1 barrier_kcal_mol = 0.0（第 154 行）；E2 仍 null（175）；E3 5.16、E4 5.74 未动 |
| `tests/test_benchmark.py` | `587768d6d9cfc6588b5209ed9e5afa95ec46fc32f8ccc72db11a34ebff472554` | `09b1ed1f66e987357bb9e38aa64651d71dd677b177c068792f29000aaecd9d1b` | **仅** `test_pinacol_dehydration_and_migration_are_separate_edges` 的一条期望值 [None, None, 5.16, 5.74] → [0.0, None, 5.16, 5.74] + 3 行注释；未动其它测试/生成器/评分规则（参照 NI5 包对同一文件同类改动的先例 evt_122f359149244da2） |
**命令与原样输出**（`cd /home/ly/Cloudra-mechanism-agent`）：
- `python -m cloudra.benchmark.gen_normal_tasks --check` → `check passed: 10 tasks`（10 行 OK，含 `OK NR1: 9 nodes, 4 steps`）
- `python -m cloudra.benchmark.gen_normal_tasks` → `wrote 10 tasks to /home/ly/Cloudra-mechanism-agent/ideapool/tasks/normal`
- `python -m pytest tests/test_benchmark.py -k regenerate_identically -q` → `....`（4 passed）
- `python -m pytest tests/test_benchmark.py -k pinacol -q` → `.`（1 passed；改前 1 failed，失败行为 `assert [0.0, None, 5.16, 5.74] == [None, None, 5.16, 5.74]` at tests/test_benchmark.py:2024）
- `python -m pytest tests/test_benchmark.py -q` → 全文件通过（1 skipped）

## 2 Q2 · NR1_E2（缺测口径 + 合并建议，候选值单独登记）
### 2.1 已确立（同批 Gaussian 16）
| 量 | 值 | 原生日志 + file:line |
| --- | --- | --- |
| I1 极小值（起点） | −463.999955035 Ha（0 虚频，72 实频；r(C4–O6)=1.544 Å） | `E2/logs/E2_I1_optfreq_c000_r2.log:18766`（Frequencies 首行 :19194） |
| I2 极小值（声明的产物） | −463.981552572 Ha（0 虚频；3 片段；r(C4···O6)=4.035 Å） | `E2/logs/E2_I2_optfreq_c000_r2.log:27292` |
| 约束扫描唯一内部极大 | r(C4–O6)=2.6313 Å，−463.974050154 Ha = **+16.26** vs I1 | `E2/logs/E2_scan_C4O6.log:45321`（14 点，Normal termination） |
| 0.05 Å 细网格复扫 | 2.632→2.032 Å **单调下降无次级峰**；pt1 −463.974050240 与 917 pt7 在 5e-8 Ha 内一致 | `E2/logs/E2_scan_fine_C4O6.log`（13 点，Normal termination） |
| 无约束候选鞍点（ts_0005 attempt1） | −463.974034272 Ha；**恰 1 虚频 −74.5623 cm⁻¹** | `ts/ts_0005/jobs/declaration_0002/ts_opt/refine.log:3987`（收敛判据 :4220/:4221）；`.../frequency/frequency.log:1001/:1010` |
| 候选鞍点的虚频模归属 | 工具口径 imag_mode_aligned=true（(5,7) 投影 0.393 ≥ 0.50×0.701=0.350）；复核口径 **(5,7) 不是最大位移对**（最大对 (12,16)=0.701，同一甲基两 H）；重原子占比 Σ|d|²=0.169 / Σ|d|=0.216（前任写的 0.127 不可复现） | 同上 frequency.log :1015-1040 |
| 双向 IRC | **失败**：Bulirsch-Stoer 不收敛 → Delta-x NOT Met → l123 Error termination，只有 Point 0 与 Forward Point 1 | `ts/ts_0005/jobs/declaration_0002/irc/irc.log:9978-9980`（sha256 `d5787702…`） |
| attempt2（IDPP 产物侧 guess） | 跑满 134 步未收敛后 Error termination l9999；末帧 −464.017399243 Ha（比 mapped-I1 低 10.95 kcal/mol），身份 = H2 桥连 O1(1.310 Å)/O7(1.118 Å)、C4–O1 成键 1.498 Å、O1···O7 = 2.403 Å（**不是**干净 2 片段换水） | `ts/ts_0005/jobs/declaration_0003/ts_opt/refine.log:83884/84124/84125/84705` |
| ts_0005 权威状态 | status=blocked、stage=refine、result=null（**无 verdict ⇒ 未验证**）、blocked.failure_class=job_failed、failed_attempt=3:ts_opt:948 (nonconvergence)、revision=36；process.json 的 declaration_revision=3（durable 声明版本） | `ts/ts_0005`（`ts_inspect` 2026-10-15 23:3x） |
### 2.2 已证伪
1. 从 917 扫描峰出发的无约束 OptTS 能给出以 C4–O6 断裂为主的干净鞍点 —— **不成立**（虚频模 H 主导）。
2. 从产物侧 IDPP 图像出发能收敛到独立解离鞍点 —— **不成立**（134 步未收敛，滑落到低 10.95 kcal/mol 的构成异构体）。
3. 1D 约束扫描（0.181 Å）能刻画 I1→I2 的 MEP —— **不成立**（大 r 侧 +17.2 远高于无约束 I2 的 +11.55）。
4. 约束扫描的大 r 侧通往声明的自由离子对 I2 —— **不成立**：917 末帧 r(C4–O6)=3.9005 Å 但 **r(C4–O10)=1.5509 Å 已成键**（本人用 awk 从 `E2/seeds/scan917_last_frame_r390.xyz`（sha256 `749a88b9…`）独立复算）；964 末帧（r=2.032 Å）同样是 r(C4–O10)=2.262 Å、且能量 +10.17 已**低于** I2 的 +11.55。
### 2.3 缺什么 / 建议
- 缺：**连通性**（native IRC 因软模数值积分失败；工具面无 IRC 步长/算法入口）与**干净的模式归属**。故 **ΔE‡ 不填数**。
- 候选值（**不作为交付值**，仅登记）：ΔE‡ = E(TS) − E(I1) = −463.974034272 − (−463.999955035) = +0.025920763 Ha = **+16.26 kcal/mol**，标注 candidate_only（附替代连通性证据）。
- **建议（按证据）**：E2 与 E3 很可能是同一步的两面（C4–O6 异裂后阳离子被相邻氧 O10（或另一分子水 O1）迅速捕获）⇒ 支持 **E2/E3 合并**或把声明的 I2 重定为“被邻居氧捕获”的物种；最终取舍取决于位移下坡试验（jobs 972/979）、换水/桥连构型 Opt+Freq、917 大 r 帧 Opt+Freq 的结果。E3 的 5.16 以碳正离子/水离子对为参考态（旧 ORCA 值），若合并需同步重定参考态。

## 3 仍未决（不影响本轮交付形态）
1. **E1**：job 977（929 pt9 几何的无约束 Opt+Freq）判定水侧是否存在 ~3.6 Å 浅极小值 → 若“是”，把 E1 的 0.0 改述为“相对该极小值的 ~1 kcal/mol 量级小垒”（仍远小于 rubric 阈值）；job 973/974（0.02 Å 细网格、冻结 O···O 定骨架剖面）关闭“更窄的垒”口径缺口。三条均已在队列（8c/10240MB/priority 0）。
2. **E2**：jobs 972/979（沿候选鞍点虚频模 ±0.15 Å 位移的两个无约束 Opt）给连通性替代证据；若两端分别匹配 I1 与 I2 ⇒ 候选 +16.26 可升为交付值；若同盆地 ⇒ 维持缺测。另有 917 大 r 帧与 948 末帧的 Opt+Freq 判定 I2 可及性与新节点身份。
3. **工具面（供主协调提 issue）**：ts_prepare 声明层无法设置 IRC 步长/算法（工作流 route 硬编码 irc=calcfc，keywords 与其撞重复）：`ts/ts_0005/jobs/declaration_0002/irc/irc.gjf`（route 首行 `#p irc=calcfc B3LYP/def2SVP empiricaldispersion=gd3bj scf=tight int=ultrafine`）；`_test_irc_A.gjf` sha256 `c9084a2bb130795083c46e967e47c9871d180a94c167b459e85a4981c336c5c4`、`_test_irc_B.gjf` sha256 `9cc0a3d235656c725f543306ae8358b2afe8291e84499b7da74ff495ae50611f`（两份只有输入、无 .log ⇒ “重复关键字会报错”属构造性推断）。
4. **平台**：23:2x compute.db 写锁复发（本包 E1/E2 各被拒 1–2 次，job_id=-1、无残留记录），后自行解除；931 的 l1 segfault 根因（折行假设已被证伪、`def2-SVP` 拼写假设待最小复现）交主协调并入 issue。

## 4 版本
- 本文件 **v2** 为当前唯一有效版本；sha256 见 hub 帖与 `NR1/STATUS.md`。
- **作废声明**：v1 sha256 `f45bcece5b06f983a67ea887d9ae860749c435f54eba21ab7305dd4640255dcc` 作废；更早的 `8ef8338efc287076d6b62dd28980a46df45639f9be5b1c8763b1752ef173da50` 亦作废。

## 5 v3 更新（2026-10-17 07:0x–07:3x）· 终裁与证据落盘

> §5 优先：与 §0–§4 冲突处，以本节为准（§0–§4 为 v2 内容，保留作历史记录）。
> v3 的实测 sha256 以 hub 终态帖与 `NR1/STATUS.md` §12.6 公布值为准（本文件不自指）。
> 详情与完整证据表（绝对路径 + sha256 + file:line）见新建的 **`NR1/MECHANISM_REVISION.md`**（E1 三条交付要件的独立载体）。

### 5.1 NR1_E2 终裁 = **缺测（null，不填数）**；+16.26 只作 candidate_only
主协调裁定（hub evt_a42bd18db1804773）与本包/只读道（as_e29f4e7911fc45ee）独立复核一致：
- 候选鞍点（ts_0005 job 933，−463.974034272 Ha，**恰 1 虚频 −74.5623 cm⁻¹**，软模、H 主导）的**虚频模 ±0.15 Å 位移下坡两端**：
  - 反应物侧 job 972/982 = −463.998937570 / −463.998937598（72 实频 **0 虚频**）= **I1 家族**另一构象极小值（C4–O6 1.539 仍成键、质子仍在 O6、2 片段；Kabsch RMSD 0.426 Å，差异集中在水的 H），+0.64 kcal vs I1；
  - 产物侧 job 979/976 = −463.975787663 / −463.975760229（72 实频 **0 虚频**）= **三元环氧鎓环 + 2 自由水**（C4–O10 1.599、保留侧 C–O10 1.593、C4–C7 1.476、O10 三配位），+15.17 vs I1、**+3.62 vs I2**；
  - ⇒ **两端都不是声明的 I1 / I2**；声明的 I2（−463.981552572，**碳正离子 + 2 H₂O**，中心 C 与 O 无键）= **与环氧鎓不同异构体**。
- **已证伪（4 条）**：① 虚频模 ±位移两端分别匹配声明的 I1/I2；② 917 大 r 帧无约束优化能回到声明的 I2（落到高 3.62 kcal 的环氧鎓）；③ 约束面 C4–O6 内部极大点即 I1→I2 鞍点；④ 从产物侧 IDPP 图像能收敛到独立解离鞍点（attempt2 134 步未收敛）。
- **缺**：连接 I1 与"声明的 I2"的独立一阶鞍点或任何路径证据（native IRC 因软模数值积分失败；工具面无 IRC 步长/算法入口，issue #184）。
- **登记**：ΔE‡ = −463.974034272 − (−463.999955035) = +0.025920763 Ha = **+16.26 kcal/mol**，标注「**到环氧鎓异构体的候选垒（candidate_only）**」；连通性表述只可用「虚频模 ± 无约束优化落点 + 两端点 0 虚频身份 + 受约束单峰」，**不得**写「IRC 已双向到达端点」。

### 5.2 NR1_R 参考态重定（新增证据 job 992，按 BRIEF §9 包内决定）
- job 992（`E2/logs/E2_swapped_attempt2_optfreq.log` sha256 **65e6ce12a7a3664b2de15cabefbf4845c2d73833dd79900fa449cc46ef227c39**；输入 sha256 14716f1b…）：`Optimization completed.` @L11381、2× Normal termination @L11989/L14872、末次 SCF **−464.018254456 Ha** @L11124、72 实频 **0 虚频**（首频 71.0470 @L12887）。
- 身份 = **中性频哪醇 + H₃O⁺ 螯合复合物**（H₃O⁺ 同时与两个频哪醇氧成短氢键：O1···O7 = 2.440、O7···O11 = 2.462 Å；2 片段）⇒ 即**反应物复合物的真极小值**，**比 I1 低 11.48 kcal/mol**。
- 决定：`NR1_R` 参考态由声明的**非驻点几何**改为该真极小值；图拓扑不变（同物种同节点）。E1 的 0.0（无垒约定值）不变，但新增声明 **R → I1 吸热 ΔE = +11.48 kcal/mol**（同批相减）。

### 5.3 NR1_E3 / NR1_E4 处置（声明取值 + 依据；不填 0）
- 现行 registry 第 3 步（I2→I3「1,2-甲基迁移」**5.16**，旧 ORCA，参考态 = 碳正离子/水离子对）与第 4 步（I3→P「去质子」**5.74**，旧 Gaussian16-WSL 批次；旧 3 边口径把它记作 `NR1_E3 = I2→P`，与主协调派单里的 "I2→P" 同指）**保留不变**，但显式标注：**非本批（Gaussian 16 / B3LYP-D3BJ/def2SVP / 气相）重算值，参考态不同义，不得与本批数值混减或相加**。
- **不采用 0 / 豁免**：本批没有任何证据表明这两步无独立鞍点（E1 的"无垒"不外推；迁移步含 C–C 断/成，去质子步的伙伴与本批建立的两端极小值不同）。
- **明确禁止**：把 E2 的 16.26（或相对 R_min 的跨步高度）写成 E3 的值。
- **缺什么**：I3（质子化频哪醇 + 2 H₂O）与 P 端在本批的 0 虚频极小值 + 迁移/去质子步的独立鞍点链（ts_prepare：TS + freq + 连通性 + 两端 Opt+Freq），起点须取路径一致的可达极小值。

### 5.4 NR1_E1 三条交付要件（已完成，落点）
1. **0.0 的语义** = MECHANISM_REVISION §1.1（约定值 / 无独立鞍点 / **不是** 0 垒 TS / 判据是剖面不是 TS）；
2. **逐条已证伪项的证据路径 + sha256 + 行号** = MECHANISM_REVISION §1.3（8 行证据表）+ §1.4（6 条证伪）+ §1.6（job 992）；
3. **题源层机理修订说明** = MECHANISM_REVISION §1–§3（含 E1 从 PT 步 → 无垒前平衡；影响 E1 自身与 E2 起点参考态；R 参考态重定）。
- **json 层无 caveat 字段**：`ideapool/tasks/normal/NR1.json` 的 step 只有结构化字段（L154 = 0.0 / L175 = null / L205 = 5.16 / L231 = 5.74），**没有**可写 caveat 的键；约定值语义只能落在 `ru.py` 注释 + `normal.md` 该行 + MECHANISM_REVISION，交付必须转述。

### 5.5 复核限度
只读道 explorer as_50fe680e47094eed 因通道限制（read 拒 >2 MiB、bash exit 126）**未能**独立复核本包 7 份大日志的能量/行号（本 Coordinator 用 bash 亲取）；第二条只读道 as_e29f4e7911fc45ee 独立复核了 972/979/976/982 与 I1/I2 的身份与能量口径，与本包一致。全部数值均为 **Gaussian 16 替代 ORCA**（引擎偏差必须随交付声明）。
