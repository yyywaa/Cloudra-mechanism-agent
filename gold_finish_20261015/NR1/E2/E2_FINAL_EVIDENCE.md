# NR1_E2（small_mol 收口核验道）· E2_FINAL_EVIDENCE.md

- 道: as_a341823c436e47ed（E2 收口核验道）；包: gold_finish_20261015/NR1/E2/；run: ts_0005 (run_dir /home/ly/Cloudra-mechanism-agent/ts/ts_0005)
- 本文件所有数值均来自盘上原生日志（绝对路径 + sha256 + file:line），原生日志未被改写；本道未改图/registry/题面/ru.py，未填 0。
- 版本: v1（含 §11 待完成作业；位移下坡与两份 Opt+Freq 到齐后升 v2）

## 0 模型与条件边界（本道自检；引用本文件结论必须带这一节）

- 模型: 气相（无 SCRF、无额外显式水）、q=+1、m=1、26 原子 C6H17O3；G16 RevC.01（/home/ly/g16/g16）；B3LYP/def2SVP + empiricaldispersion=gd3bj + scf=tight + int=ultrafine。
- **未建模**: 额外显式水/微溶剂化、抗衡离子、温度与浓度、熵与自由能、核量子效应。凡涉及『自由离子对 vs 接触离子对』『离子对是否可及』的陈述都只在该气相模型内成立。
- 反应: 题面声明 I1（C4-O6 成键 1.544 A，质子化频哪醇 + 一分子水）→ I2（叔碳正离子 + 2 H2O，r(C4...O6)=4.035 A）；键变化 = 断 (5,7)（job 原子序，= 题面 map4(C4)-map6(O6)）。
- 参考能（同为上述级别、同一批 G16 纯电子能）:
  - E(I1) = -463.999955035 Ha（E2/logs/E2_I1_optfreq_c000_r2.log:18766；sha256 c8db123fce61fc35f1e668f8a2d328b46f9673630e58ca6f1058d2c0e01dacaf；:20374 Optimization completed、:21179 Normal termination；0 虚频: :19184 Low frequencies 全正、无 imaginary 行、:19194 首个 Frequencies -- 23.2523）
  - E(I2) = -463.981552572 Ha（E2/logs/E2_I2_optfreq_c000_r2.log:27292；sha256 e89f464f0712f44ea7e5520d0052a5b9b8a2b8cde86e1bbcb0cfc0dd8e828eee；:27548 Optimization completed、:31046 Normal termination；0 虚频: :29047 Low frequencies 全正、:29057 首个 Frequencies -- 33.9981）
  - E(I2)-E(I1) = +11.55 kcal/mol（参考差，不是能垒）

## 1 ts_0005 权威状态（ts_inspect run_id=ts_0005，revision=36，逐字登记）

| 字段 | 原样值 |
| --- | --- |
| status | blocked |
| stage | refine |
| result | null（**无 verdict**；不是 verified=false 的判据，而是没有判定） |
| blocked.failure_class | job_failed |
| blocked.message | refinement job 948 (ts_opt) ended as failed; plain per-engine failure classes come from the log below — the run is stopped, not silently retried |
| blocked.needs | [ts_optimization, execution, reaction.reaction_center] |
| failed_attempt | attempt_id 3:ts_opt:948, failure_class nonconvergence, job_id 948, input_revision 3, log_path .../declaration_0003/ts_opt/refine.log, log_sha256 fa7f1f5571106e74210dfb404defb53fd3e670ddab095c4935565a6ee6ff39cd |
| next | action=inspect, required_inputs=[], editable_groups=[] |
| methods.ts_opt | planned = actual = gaussian / B3LYP / def2SVP / keywords empiricaldispersion=gd3bj scf=tight int=ultrafine（contract.matched=true） |
| methods.frequency / irc / reactant_* / product_* | planned 同上，**actual=null**（未再执行） |
| usage | interventions=2, compute_actions=4；jobs: 933 (8c/10240MB, 221.4 s), 936 (127.5 s), 941 (597.4 s), 948 (1864.8 s) |
| available_results | declare/build/map/assemble/guess/validate/submit 均 done |
| details_path | /home/ly/Cloudra-mechanism-agent/ts/ts_0005/process.json（export_revision=36，与 revision 一致） |

- 裁决（主协调口径）: declaration_revision=3 是 durable 声明版本，ts_inspect.revision=36 是权威 input revision；两者并列登记。
- 容量结论: run 已被平台判为 stopped/blocked（不是 running/waiting），不占算力；next.action=inspect 表示仍可由 ts_resume 重新提交（本道未提交，见 §11）。

## 2 四项原生日志独立核验（本道只读复核，不重跑）

### 2.1 job 933 · ts_opt（declaration_0002）
- 路径: /home/ly/Cloudra-mechanism-agent/ts/ts_0005/jobs/declaration_0002/ts_opt/refine.log；sha256 72a641896e37d8ea5378cc874cd1959c64337638e9137d52b8d45bb880ac3a66（4827 行）
- :3987 SCF Done: E(RB3LYP) = -463.974034272 A.U. after 7 cycles（**这是能量行**）
- :4220 Optimization completed.；:4221 -- Stationary point found.；:4827 Normal termination of Gaussian 16 at Thu Oct 15 18:44:00 2026.
- 鞍点几何（最后一次 Standard orientation，:4485 起）: r(C4-O6)=d(5,7)=**2.597 A**；该几何与 frequency.gjf 输入几何逐位相同。
- 结论: 与前任道记录一致（收敛的 candidate 鞍点，E=-463.974034272）。

### 2.2 job 936 · frequency（declaration_0002）
- 路径: .../jobs/declaration_0002/frequency/frequency.log；sha256 c5b0e878123f74420937b997d5d13520e73ba3421aba30f38b8c052752f241d6（2813 行）
- :999 Low frequencies --- -74.5657 -0.0006 -0.0004 -0.0002 4.1981 5.7927
- :1001 ******    1 imaginary frequencies (negative Signs) ******  → **虚频数 = 1**
- :1010 Frequencies --    -74.5623                42.0933                82.1039  → **虚频值 = -74.5623 cm-1**
- :1844 1 imaginary frequencies ignored.（ZPE 段）；:1865 Zero-point correction= 0.227700
- **位移块（:1015-:1040，26 行 = 模式 1（虚频模）的 X/Y/Z）逐位复算**（本道重新解析，未用工具摘要）:
  - Sigma|d|^2 = 0.9933（≈1 → 该矢量是 Cartesian 归一；占比以 Sigma|d|^2 为分母）
  - 最大单原子位移 = **原子 17（C6 上甲基 H）|d|=0.403**；其次 12(0.397)、19(0.352, O6-H)、16(0.337)、13(0.337)、14(0.267)、7(0.234, O6)。前十名里**只有原子 7(O6) 一个是重原子**。
  - 重原子占比（重原子 = 1,4,5,6,7,8,9,10,11）: **Sigma|d|^2 口径 = 0.169**；**Sigma|d| 口径 = 0.216**（两个定义都列出）。
  - **(5,7) 投影 = |u(5->7) . (d5-d7)| = 0.384**（u = 鞍点几何 C4->O6 单位矢量），本道逐位复算 = 0.3838
  - **最大位移对 |d12-d16| = 0.701**（对全部 (i,j) 对扫描后确认 (12,16) 为最大对；= C4 上同一甲基两个 H 的相对运动，即甲基转动）
- 结论: **虚频数与虚频值两项与前任道完全一致**；0.384/0.701 完全复现；**前任道写的『重原子分数 0.127』本道无法复现**（见 §2.5 更正）。

### 2.3 job 941 · IRC（declaration_0002）
- 路径: .../jobs/declaration_0002/irc/irc.log；sha256 d57877020625971602fb4d6dda7d1260aa5d0169d3c08e6577683ccc510a8039（9983 行）；输入 .../irc/irc.gjf，route 首行原样 #p irc=calcfc B3LYP/def2SVP empiricaldispersion=gd3bj scf=tight int=ultrafine
- 路径点证据: :1002 Point Number:   0          Path Number:   1；:1004 Point Number  1 in FORWARD path direction. → 日志里**只有 Point 0 与 Forward Point 1**，没有任何终点/双向汇总表。
- 积分器: :1415 Using modified Bulirsch-Stoer corrector integration.；重复出现 WARNING: Bulirsch-Stoer Method is not Converging（:1474, :1921, :2368, :2815, ... , :9967）
- 终结（原始行）: :9978 Delta-x Convergence NOT Met；:9979 Maximum number of corrector steps exceded.；:9980 Error termination via Lnk1e in /home/ly/g16/l123.exe at Thu Oct 15 19:01:20 2026.；:9981 Job cpu time 1 h 10 min 45.8 s。
- 结论: **IRC 失败**，无任何端点到端点证据；与前任道记录一致（其记的约 :9980 即本道精确的 :9978-:9980）。

### 2.4 job 948 · ts_opt（declaration_0003）
- 路径: .../jobs/declaration_0003/ts_opt/refine.log；sha256 fa7f1f5571106e74210dfb404defb53fd3e670ddab095c4935565a6ee6ff39cd（84709 行）
- :83884 SCF Done: E(RB3LYP) = -464.017399243 A.U. after 10 cycles（最后一次 SCF 已收敛；失败不是 SCF 失败）
- 末次判据（:84118-:84121）: Max Force 0.019196/0.000450 NO；RMS Force 0.002761/0.000300 NO；Max Displacement 0.235773/0.001800 NO；RMS Displacement 0.042243/0.001200 NO
- :84124 Optimization stopped.；:84125 -- Number of steps exceeded,  NStep= 134；:84705 Error termination request processed by link 9999.；:84706 Error termination via Lnk1e in /home/ly/g16/l9999.exe at Thu Oct 15 19:34:58 2026.（cpu 4 h 03 min 55.8 s / wall 30 min 43.9 s）
- 末帧几何（最后一次 Standard orientation，:84391 起；与 E2/structures/attempt2_last_frame.xyz 逐位一致），本道自算距离:
  - r(C4-O1) = d(5,1) = **1.498 A（新成键）**；r(C4-O6) = d(5,7) = **3.230 A（原反应键已断）**
  - 质子: r(O1-H2) = 1.310 A、r(H2-O7) = 1.118 A（**H2 处于 O1...O7 之间**，O1...O7 = 2.403 A 的短氢键）；r(O1-H3)=0.970；r(O7-H18)=1.028、r(O7-H19)=0.972 → **O7(O6) 带两个 H = 水**
  - E = -464.017399243 Ha，比 mapped-I1 低 **10.95 kcal/mol**（未收敛，不能当极小值）
- 结论: 与前任道记录一致；补充更正: 该末帧不是干净的 2 片段『换水』，而是『C4-O1 成键 + 质子桥连 O1...O7』（见 §11 待确认）。

### 2.5 与前任道笔记（E2_NOTES.md，sha256 43035515cb27d76a5974accd41595e5a7942399b0a3bf57b24ae15a9e5c36647）的差异更正

1. **933 的行号用途**: 前任笔记 §3.5 把末帧能量标在 refine.log:3987 处并与收敛混述；本道确认 :3987 只是 SCF 能量行，**收敛判据在 :4220/:4221**。→ 前任笔记 §3.5 的表述已更正（数值无误，行号用途需区分）。
2. **936 的『重原子分数』**: 前任写 0.127（log_parser 字段 heavy_atom_fraction）；本道自算 Sigma|d|^2 口径 = 0.169、Sigma|d| 口径 = 0.216，**两种自然定义都不等于 0.127**，无法复现该字段口径；记录下来供主协调追该工具字段定义。结论方向不变（H 主导）。
3. 其余（虚频 -74.5623 @:1001/:1010、(5,7)=0.384、最大对 (12,16)=0.701、941 失败、948 步数与能量）**全部复现，无差异**。

## 3 job 964 · C4-O6 细网格约束扫描（2.632 -> 2.032 A，0.05 A）逐点表

- 路径: E2/logs/E2_scan_fine_C4O6.log；sha256 9d2b4f47886b89b6554b9c032f4087de51700dec7b74d57bde8259f4025246cb（63827 行）；:63827 Normal termination 23:34:38；输入 E2/logs/E2_scan_fine_C4O6.gjf（route: opt=(modredundant,maxstep=10) b3lyp/def2svp empiricaldispersion=gd3bj scf=tight int=ultrafine；约束行 B 5 7 S 12 -0.050000；起点 = 917 峰帧）。
- 扫描方向 = **只有内侧**（2.632 -> 2.032 A）；r_i = 2.632 - 0.05*(i-1)（末帧文件自证 parm=2.03185）。能量行 = 该点最后一个 SCF Done；收敛行 = 该点 Optimization completed。

| pt | r(C4-O6) A | E(Ha) | 能量行 | 收敛行 | dE vs I1 (kcal) | dE vs 上一点 (kcal) |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2.632 | -463.974050240 | :2759 | :2982 | +16.256 | - |
| 2 | 2.582 | -463.974036734 | :10371 | :10601 | +16.264 | 0.008 |
| 3 | 2.532 | -463.974107555 | :16271 | :16500 | +16.220 | -0.044 |
| 4 | 2.482 | -463.974341042 | :21768 | :21998 | +16.073 | -0.147 |
| 5 | 2.432 | -463.974770527 | :25176 | :25398 | +15.804 | -0.270 |
| 6 | 2.382 | -463.975383358 | :28180 | :28405 | +15.419 | -0.385 |
| 7 | 2.332 | -463.976173084 | :30770 | :30991 | +14.923 | -0.496 |
| 8 | 2.282 | -463.977127414 | :34595 | :34820 | +14.325 | -0.599 |
| 9 | 2.232 | -463.978335773 | :47039 | :47273 | +13.566 | -0.758 |
| 10 | 2.182 | -463.979548805 | :50892 | :51123 | +12.805 | -0.761 |
| 11 | 2.132 | -463.980852711 | :53099 | :53322 | +11.987 | -0.818 |
| 12 | 2.082 | -463.982246049 | :56977 | :57211 | +11.113 | -0.874 |
| 13 | 2.032 | -463.983745086 | :62611 | :62843 | +10.172 | -0.941 |

**回答 ①『内部极大是否随网格变细仍存在、位置是否移动』**:
- **仍存在，位置未移动**——但细网格只覆盖 r <= 2.632 A，从 pt1(2.632, +16.256) 往内侧**单调下降**（唯一非单调是 pt2 的 +0.008 kcal，低于本级别数值噪声），没有任何次级极大。
- 与粗网格 917（步长 0.181 A）合并，可把约束面极大值括在 **r_max 在 [2.632, 2.812] A 之间**（粗网格 pt7=2.6313 高于 pt6=2.4502 与 pt8=2.8124）；细网格证明 r<2.632 一侧没有第二个峰，**但没有细化峰的位置**（未在峰两侧取样）。
- 交叉校验: 细网格 pt1 能量 -463.974050240 与 917 粗网格 pt7 -463.974050154（logs/E2_scan_C4O6.log:45321）在 5e-8 Ha 内一致 → 两次扫描可互比。
- **附带的结构发现（重要）**: 细网格末帧（r(C4-O6)=2.032 A）不是『拉长的 C4-O6 键』回到 I1 的路径。本道用 format_converter 取末帧（E2/structures/displacement/E2_finescan_last_frame_r2032.xyz，sha256 54ee76f87cd811a79d4faf5b29f47c63bebd91c1caa6007be7a06aa4c1d86a80）自算: r(C4-O10)=**2.262 A（正在被分子内 O10 捕获）**、r(C4-O1)=3.853、r(O1...O6)=2.624、O6 带 H18(1.002)+H19(0.969) = 水、O10 带 H26(0.968) = 醇羟基。即沿约束坐标拉走 O6 的同时 C4 被 O10 接近；且该点能量 (+10.17) **低于**自由离子对 I2 (+11.55)。这把『大 r 侧 C4-O10 分子内捕获』延伸到了小 r 侧，说明**约束坐标与 C4...O10 捕获强耦合**。

## 4 工具面限制（IRC 步长/算法）—— issue 材料

- 工作流自生成的 IRC 输入（实测）: /home/ly/Cloudra-mechanism-agent/ts/ts_0005/jobs/declaration_0002/irc/irc.gjf，route 首行 = #p irc=calcfc B3LYP/def2SVP empiricaldispersion=gd3bj scf=tight int=ultrafine → **irc=calcfc 由工作流硬编码在 method/basis 之前，keywords 原样拼接在其后**。
- 最小复现输入: E2/logs/_test_irc_A.gjf（sha256 c9084a2bb130795083c46e967e47c9871d180a94c167b459e85a4981c336c5c4，工作流同款 route）、E2/logs/_test_irc_B.gjf（sha256 9cc0a3d235656c725f543306ae8358b2afe8291e84499b7da74ff495ae50611f，尾部混入 irc=(calcfc,stepsize=5) → 与自带 irc=calcfc 重复同一关键字）。
- **证据强度标注（必须原样引用）**: 『两份 _test_irc_*.gjf 只有输入文件、无对应 .log，故“keywords 尾巴的 irc=… 与工作流自带 irc=calcfc 相撞会被 Gaussian 判为重复关键字”是**未执行验证的构造性推断**，不是实测报错；实测事实只有：工作流为 IRC 自动生成的 route 把 irc=calcfc 硬编码在 method/basis 之前，keywords 原样拼接在后。』
- 科学后果: 本道因此**没有**手工提交 IRC、没有绕过 durable 工作流；job 941 失败后无法通过声明层改步长/算法重试 → 连通性只能走替代证据（§11）。

## 5 【已确立】

1. ts_0005 权威状态（§1）: blocked / refine / result=null / failed_attempt 3:ts_opt:948 / needs=[ts_optimization, execution, reaction.reaction_center]。
2. 两端极小值（本级别气相、同批）: E(I1)=-463.999955035（915 日志:18766，0 虚频）、E(I2)=-463.981552572（916 日志:27292，0 虚频）；r(C4-O6): I1=1.544 A、I2=4.035 A（本道自算）。
3. attempt 1 的驻点是**一阶鞍点候选**（恰 1 虚频 -74.5623 cm-1），能量 -463.974034272（933:3987），相对 I1 = **+16.26 kcal/mol**。
4. 该虚频模是**极软的 H 主导模**（§2.2 全套占比数据）。
5. 917 与 964 两次约束扫描都显示 C4-O6 约束面上存在内部极大（r 约 2.63 A，+16.26 kcal/mol）；964 细网格没有推翻它，也没有在 r<2.632 侧发现第二个峰。
6. 约束面与 C4...O10 分子内捕获强耦合（§3 末帧结构）。
7. 工具面: 工作流 IRC route 硬编码 irc=calcfc（§4，复现文件已固定）。

## 6 【已证伪（针对哪条假设）】

| # | 被证伪的假设 | 证据 |
| --- | --- | --- |
| F1 | 『917 约束扫描的内部极大点就是连接 I1 与 I2 的鞍点/能垒』 | 大 r 侧约束面 +17.17…+17.5 kcal/mol **远高于**无约束 I2 极小值 +11.55 kcal/mol（notes §3.3a 与本道 §3）；且 job 933 的 TS 几何 r(C4-O6)=2.597 A 的虚频模并非 C4-O6 断裂主导（§2.2）→ 约束扫描峰不等于 TS |
| F2 | 『attempt 1 的 933 鞍点满足 E2 判据链』 | 判据②边界不通过（(5,7) 不是最大位移对；聚合 watch-pair 占比 2.3%，notes §3.5/§3.8 与本道 §2.2）；判据③完全没有路径证据（941 积分失败，§2.3） |
| F3 | 『917 的大 r 约束面（3.72-3.90 A）通往声明的 I2 自由离子对』 | 大 r 帧 r(C4-O10)=1.551 A 成键（notes §3.9，3 片段）→ 走的是分子内捕获的另一条谷；本道 §3 在 2.032 A 处也观察到 C4...O10=2.262 的同类耦合 |
| F4 | 『attempt 2（IDPP img_06）能给出更干净的鞍点』 | job 948 跑满 NStep=134 未收敛并滑落到 E=-464.017399243 的 C4-O1 型异构体（§2.4）→ 离子对区极平坦，TS 优化无法停留 |
| F5 | （对前任笔记的更正）『936 位移块重原子分数 = 0.127』 | §2.5 第 2 条 |

## 7 【TS 判据链逐项达成情况】

| 判据 | 状态 | 证据（绝对路径 + file:line） |
| --- | --- | --- |
| ① 恰 1 虚频 | **达成** | .../declaration_0002/frequency/frequency.log:1001（1 imaginary frequencies）、:1010（-74.5623 cm-1） |
| ② 该虚频模以 (5,7)=C4-O6 断裂为主 | **不达成（边界情形，两口径并列）** | 工具口径 ts_guess(mode=verify): imag_mode_aligned=true，(5,7) 相对位移 0.393 >= 0.50x0.701=0.350（notes §3.8 原文）；复核口径: (5,7)=0.384 **不是**最大位移对（最大对 (12,16)=0.701）、重原子占比 0.169、聚合 watch-pair 占比 0.023 → 不通过 |
| ③ 双向 IRC 真实连通 I1 与 I2 | **未达成（native IRC 失败）** | 941:1002/1004 只有 Point 0 与 Forward Point 1；:9978 Delta-x Convergence NOT Met，:9979 Maximum number of corrector steps exceded，:9980 Error termination l123；工具面无法改步长/算法（§4）→ 只能给**连通性替代证据**（§11，pending） |
| ④ 两端点 0 虚频极小值（身份核验） | **达成（但两端极小值本身由 915/916 独立建立，不构成连通性证明）** | I1: E2_I1_optfreq_c000_r2.log:20374/:21179、0 虚频 :19184/:19194；I2: E2_I2_optfreq_c000_r2.log:27548/:31046、0 虚频 :29047/:29057 |

## 8 【能垒是否可给】

**不能给（截至 v1）**。缺的是**判据②③**，具体缺两项:
1. 一条**真实连通 I1 与 I2 的路径证据**（native IRC 双向失败，且工具面无 IRC 步长/算法入口，§4）；替代证据（虚频模 ±0.15 A 位移下坡无约束 Opt）已提交、未出结果（§11）。
2. **无约束 OptTS 得到的、虚频模以 (5,7) 断裂为主的干净鞍点**（现有唯一候选 933 的模是 H 主导软模，§2.2）。
硬前置（E(TS)-E(I1) 同批相减）在数值上可用（933:3987 与 915:18766 同程序同级别同批），但**在②③满足前它不能作为 dE‡ 交付**（约束扫描峰不等于 TS）。

## 9 【候选值（明确标注未通过验收、不可直接交付）】

| 候选 | 值 | 状态 | 依据 |
| --- | --- | --- | --- |
| dE‡(候选) | -463.974034272 - (-463.999955035) = **+0.025920763 Ha = +16.26 kcal/mol** | **candidate_only（未通过验收，不可直接交付）** | 933:3987 / 915:18766，同批同级别纯电子能；判据②③未达成 |
| 约束扫描内部极大（仅参考，非 TS） | +16.26 kcal/mol（r 约 2.63 A） | 参考值 | 917 峰 :45321；964 pt1 :2759 |
| 细网格末端（仅参考） | +10.17 kcal/mol（r(C4-O6)=2.032, r(C4-O10)=2.262） | 参考值 | 964:62611 |
| 『换水/质子桥连』异构体（未收敛的几何，不是驻点） | -464.017399243 = 比 mapped-I1 低 10.95 kcal/mol | **未收敛轨迹末帧，禁止当极小值使用** | 948:83884 |
| E(I2)-E(I1) | +11.55 kcal/mol | 参考差（非能垒） | 916:27292 / 915:18766 |

## 10 【裁决问题】

1. 若 §11 的 ± 位移下坡两端分别落到 I1 与 I2（几何/能量匹配）: 是否接受『候选能垒 +16.26 kcal/mol + 替代连通性证据（不是 IRC）』作为 E2 的可交付值？本道默认按『candidate_only，未过验收』登记，除非主协调明确升级。
2. 若两端落进同一盆地: 是否按『无合格独立鞍点』交付、dE‡ 记缺测（不填 0），并把 E2 并入 E3 叙事（注意 E3 的 5.16 参考态是碳正离子/水离子对，与本包 I1 参考态不同）？
3. 『换水/质子桥连』异构体（比 mapped-I1 低 10.95 kcal/mol）若被 Opt+Freq 证实为 0 虚频极小值: 是否作为新的候选节点登记（会改变『产物侧最稳定物种』的叙事与 I2 的可及性），还是仅作旁证？它是否应直接影响 E3 的参考态选择？
4. 936 位移块重原子分数的工具字段口径（前任 0.127 vs 本道 0.169/0.216）是否与 issue 一并报平台？

## 11 待完成作业（本轮已提交/排队；结果到齐后本文件升 v2）

| 作业 | 内容 | 状态 |
| --- | --- | --- |
| job 972 | 位移下坡 (-): 936 虚频模 -0.15 A(max atom) 位移帧无约束 Opt（E2/logs/E2_dispmode_minus_opt.gjf） | 已提交 ready |
| job 979 | 位移下坡 (+): 同法 +0.15 A（E2/logs/E2_dispmode_plus_opt.gjf） | 已提交 ready |
| 待投 | E2/logs/E2_outframe_prod_optfreq.gjf（917 r=3.90 A 帧无约束 Opt+Freq；sha256 f3ad355957632b9f59c2f28072077b30c2e3dc75998f29d832a428893354909c） | 待队列余量（同刻手工作业 <=2） |
| 待投 | E2/logs/E2_swapped_attempt2_optfreq.gjf（948 末帧无约束 Opt+Freq；sha256 14716f1b81d3f505482613514a5493bb1772a61ec980835796b3bb6c1d39f0d5） | 待队列余量 |

- 位移口径（两作业一致）: 起点 = 933/frequency.gjf 鞍点几何（r(C4-O6)=2.597 A）；d = 936 模式 1（虚频模，Sigma|d|^2=0.9933）；d r_i = ±c d_i，c = 0.15/0.403 = 0.37245 → max|d r| = 0.15 A、RMS = 0.0728 A、Sigma|d r|^2 = 0.1378；结构文件 E2/structures/displacement/E2_dispmode_plus.xyz（sha256 f411116dac5194552c81446f108c44a116e20a5a69f3350bd00a8bc152b1a4a0）、E2_dispmode_minus.xyz（sha256 2b154a88344f615c3960bba61ce0b0329385f7292d53a29f63fc3635c8e54300）。级别与 I1/I2 完全一致（同程序同批口径）；判据 = 落点能量/几何是否分别匹配 I1(-463.999955035, r=1.544) 与 I2(-463.981552572, 3 片段, 4.035)。
- **措辞约束（主协调裁决）**: 位移下坡结果只能写成『连通性替代证据（native IRC 因软模数值积分失败 + 工具面无 IRC 步长/算法入口）』，**不得**写成『IRC 双向』。
