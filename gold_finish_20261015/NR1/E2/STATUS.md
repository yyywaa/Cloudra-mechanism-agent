# STATUS · NR1_E2（E2 计算道 small_mol as_3554137d6af74102）

更新时间：2026-10-15 放行后
每条边一行：状态 / run_id 与 run_dir / 原生日志路径 + sha256 / 方法一句 / 下一步。

- **NR1_E2** · 状态：**进行中（准备完成，QM 已开工，尚无 ΔE‡ 数值）**。缺测项：脱水的 C4–O6 解离 TS、ΔE‡、IRC 双向端点证据、I1/I2 的 DFT 极小值能量。已证伪：无（尚无结论）。待裁决：若最终无独立鞍点，E2 是否与 E3 合并 / 是否记为无垒（裁决 A：E2 产物按 **26 原子**（水(O1)+水(O6/H2)+叔碳正离子）推进，主协调 2026-10-15 裁定，理由见 E2_NOTES.md §5）。
- run_id / run_dir：**暂无**（durable TS 流程尚未启动；当前只有普通 Opt/Freq 作业 911，job 目录 gold_finish_20261015/NR1/E2/logs/）。
- 原生日志：job 911（I1 Opt+Freq）**排队中，未终态**；终态后补绝对路径 + sha256。
- 方法一句：Gaussian 16 `/home/ly/g16/g16`，B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight，气相（无 SCRF），q=+1/m=1，26 原子 C6H17O3。
- 资源口径：job 911 = 12c/13GB（已排队，不取消重投）；新作业一律 **8 cpus / 10 GB**（主协调 16:35 口径，已确认）。
- 下一步：①job 911 终态 → 核验 0 虚频 + O6–H/O1–H 质子归属 + 片段数 + r(C4–O6) 实测值；②提交 I2 Opt/Freq（logs/E2_I2_optfreq_c000.gjf 已预生成，sha256 4a12461e5e9df5d3dac4b979624b7f8792a6d7acf6d3a0de01eddc7c173305aa）；③ts_prepare（guess=scan 沿 d(C4–O6)）→ OptTS+Freq → 双向 IRC → 两端 Opt/Freq。

准备档案（非 QM）：`E2_PREP_PROVENANCE.md`（sha256 446a744673aa5f6eac64dd1393730b40c0f6fc0c21009cd46798044ea2c1c817）。

## 作业台账（E2 道）
| job | 目的 | 资源 | 状态 | 原生日志 + sha256 |
| --- | --- | --- | --- | --- |
| 911 | E2 起点 I1 无约束 Opt+Freq | 12c/13GB | **failed（技术性）**：`%chk` 被渲染为相对路径、CWD=logs/ 下不存在 → Link 0 `fd = -1 / open-new-file`，未进入 SCF。非科学失败。 | logs/E2_I1_optfreq_c000.gjf.log sha256 7fe675d584560ba11bb72453aa5168f88b0e03f7916ddb99ef523ebf1a208ea0（无 Normal termination；原始行 L81/L85/L87） |
| 待投 | 同目的重投（修复 `%chk`=裸文件名） | 8c/10GB | **未提交**（平台故障期暂停；输入已就绪 logs/E2_I1_optfreq_c000_r2.gjf sha256 359e83717722c4adf5c95b2941105a194da3f80cd1fae0ad19de2b8922950484） | 待生成 |

坑提示：`qm_input_writer` 的 chk_name/fchk_name 不要给绝对路径（会被相对化 → CWD 下不存在 → 崩在 Link 0）；给裸文件名或省略。

## 平台级观察（供主协调提 issue；只读取证，未改平台代码/DB/进程）
1. **`qm_input_writer` 的 `chk_name` 绝对路径被相对化 → Gaussian 崩在 Link 0（P1，可复现）**
   - 复现：`qm_input_writer(engine="gaussian", output_path="<工作区内绝对路径>", chk_name="<工作区内绝对路径>.chk", ...)`
   - 结果：写出的 .gjf 第 1 行是**相对路径** `%chk=gold_finish_20261015/NR1/E2/logs/E2_I1_optfreq_c000.chk`（证据 file:line：`gold_finish_20261015/NR1/E2/logs/E2_I1_optfreq_c000.gjf:1`），而**作业 CWD = 输入文件所在目录**（…/NR1/E2/logs/）。
   - 后果：Gaussian 找不到该相对路径 → `fname=gold_finish_20261015/NR1/E2/logs/E2_I1_optfreq_c000.chk fd = -1` → `open-new-file` → 退出码 1，**未进入任何 SCF**。证据：`logs/E2_I1_optfreq_c000.gjf.log`（sha256 7fe675d584560ba11bb72453aa5168f88b0e03f7916ddb99ef523ebf1a208ea0）L81/L85/L87；job 911 state=failed，`state_911.json` 同目录。
   - 规避：`chk_name` 传**裸文件名**（相对 CWD 有效）或省略（Opt/Freq 不需要 chk）。我已用裸文件名重投（job 915）。
   - 建议：writer 对 `chk_name/fchk_name` 要么保留绝对路径、要么相对 output_path 所在目录解析，而不是相对工作根目录。
2. **`smiles_to_mol` 复杂体 3D 构建返回 is_success=false 但产物已落盘**（消息 "builder reported status='ok' but produced no MOL candidate"，而 assemblies 下 xyz/mol 齐全）。本道以磁盘文件为准；E1 道独立复现。建议 reporter 修 is_success 判定，避免调用方误判失败。
3. **排队作业无取消入口**（与 HL1 包结论一致）：`submit_compute_job` 无 cancel；本次我未做任何重复提交，改为等队列流动。

## ⏱ 交接快照（2026-10-15 18:5x，API 重启窗口前写入 —— 若我的会话被收尾为 failed，请继承人从这里接手）

**当前在等的作业**：job 917 = C4–O6 弛豫扫描（logs/E2_scan_C4O6.gjf → logs/E2_scan_C4O6.log；8c/10GB；`B 5 7 S 13 0.181231`，起点 = I1 优化几何实测 1.544 Å → 3.900 Å，14 点）。**13/14 点已收敛，pt14 仍在跑**（大 r 侧水面松弛慢，已 ~27 Berny 步）。日志 sha256（截至 18:4x，未终态）d450540684e998173851183380dbebd55755428572db9e17f4d15eda42a4dc26 —— **终态后必须重新取 sha256**。

**已确立的科学事实（同批 Gaussian 16 / B3LYP-D3BJ/def2SVP / 气相 / q+1 / m=1 / 26 原子 C6H17O3）**
- **E2 起点 I1 极小值（job 915 done）**：E = **−463.999955035 Ha**（logs/E2_I1_optfreq_c000_r2.log:18766），0 虚频（72 实频；Frequencies 首行同日志:19194），r(C4–O6)=1.544 Å，质子仍在离去氧 O6（O6–H 1.046 / O1···H 1.451 Å）；末帧 structures/I1_opt_c000_r2.xyz（sha256 34ed0b5d…）。日志 sha256 c8db123f…。
- **E2 产物 I2 极小值（job 916 done）**：E = **−463.981552572 Ha**（logs/E2_I2_optfreq_c000_r2.log:27292），0 虚频，3 片段、C+ sp2、r(C4···O6)=4.035 Å；末帧 structures/I2_opt_c000_r2.xyz（sha256 555f5f49…）。日志 sha256 e89f464f…。
- **参考能差**（非能垒）：E(I2)−E(I1) = **+11.55 kcal/mol**。
- **扫描判据（13/14 点，权威表见 E2_NOTES.md §3.3 / hub 帖 evt_38a9c7d0…）**：**存在内部极大** —— pt7（r=2.6313 Å）= **+16.26 kcal/mol**（917 日志:45321），随后 pt8 +15.36、pt9 +15.19（下降），r>3.0 又回升至 pt13 +17.17。→ 倾向 E2a（有独立鞍点）；但**扫描峰 ≠ TS**。

**下一步（严格顺序）**
1) 等 job 917 Normal termination（若平台重启把它收尾成 failed，先核对日志是否含 "Summary of ... Potential Surface Scan"；无该表则需重跑扫描或改用 pt7 附近的更小窗口扫描）。
2) `ts_guess(mode="scan_parse", log_path=<917 日志绝对路径>, ts_candidate_path="gold_finish_20261015/NR1/E2/seeds/scan917_peak.xyz")` 取峰帧 xyz（落盘后才可作为 evidence_refs）。
3) 提交 **ts_prepare**（provided guess = 峰帧；reaction=I1→I2 的 26 项 atom_map + reaction_center=[[5,7]]；conformers = structures/I1_opt_c000_r2.xyz 与 structures/I2_opt_c000_r2.xyz（各自 mol_path = 对应 build_* 的 complex_candidate_000.mol）；ts_optimization/verification(freq,irc,两端 endpoint seed) 全部用同一 formal profile = gaussian/B3LYP/def2SVP + keywords "empiricaldispersion=gd3bj scf=tight int=ultrafine"；execution={cpus:8, memory_mb:10240}）。草案见 TSPREPARE_DRAFT.md v2（sha256 324f0cfc…，注意把 evidence_refs 换成已落盘文件）。
4) 验收链：TS 恰 1 虚频且 (5,7)=C4–O6 位移占比 ≥0.30 → 双向 IRC 真实到达 I1 与 I2 → 两端 Opt/Freq 0 虚频 → **ΔE‡ = E(TS) − (−463.999955035 Ha)**（纯电子能，同批日志）。**拿不到该链条就不填数字**，改交"无独立鞍点/需与 E3 合并 + 已证伪材料"。
5) 交付格式见复核道 7 项清单（每驻点 SCF Done 的 file:line + 算术 + run_dir/process.json/verdict）。

**已知坑**：`qm_input_writer` 的 chk_name 绝对路径会被相对化 → 作业 CWD=输入目录 → Link 0 fd=-1（job 911 如此 failed）；一律用裸文件名。

## ✅ NR1_E2 终态行（2026-10-15 20:0x，E2 计算道 as_3554137d6af74102）

- **NR1_E2 · 状态：缺测（无合格独立鞍点，ΔE‡ 不填）**。
  - 缺什么：①以 C4–O6 断裂为主的唯一虚频模（现有候选鞍点虚频为 H 主导软模）；②双向 IRC 真实连通 I1 与 I2 的方向区间证据（IRC 积分失败，无路径）。
  - 已证伪什么：(a) "从 917 扫描峰出发的无约束 OptTS 能给出以 C4–O6 为主的干净鞍点" —— 假；(b) "从产物侧 IDPP 图像出发能收敛到独立解离鞍点" —— 假（跑满 134 步未收敛，滑落到比 I1 低 10.95 kcal/mol 的换水构型）；(c) "1D 约束扫描（0.181 Å）能刻画 I1→I2 的 MEP" —— 假（大 r 侧 +17.2 远高于真实 I2 极小值 +11.55，且 frames 2→3 有 4.40 kcal 跳变）。
  - 已确立（可复核数值，同批 Gaussian 16 / B3LYP-D3BJ/def2SVP / 气相 / q+1 / m1 / 26 原子）：
    E(I1 极小值) = **−463.999955035 Ha**（logs/E2_I1_optfreq_c000_r2.log:18766，0 虚频，h取 sha256 c8db123f…）；
    E(I2 极小值) = **−463.981552572 Ha**（logs/E2_I2_optfreq_c000_r2.log:27292，0 虚频，sha256 e89f464f…）；
    E(候选软鞍点) = −463.974034272 Ha（+16.26 vs I1；虚频 −74.5623 cm⁻¹，H 主导）；
    E(I2) − E(I1) = **+11.55 kcal/mol**（非能垒）。
- **run_id = ts_0005**；run_dir = `/home/ly/Cloudra-mechanism-agent/ts/ts_0005`；process.json 同目录（verdict = blocked/refine，attempt 2 后 status=blocked→见 ts_inspect）。
- 关键原生日志（绝对路径 + sha256）：
  - logs/E2_I1_optfreq_c000_r2.log c8db123fce61fc35f1e668f8a2d328b46f9673630e58ca6f1058d2c0e01dacaf（915，起点极小值）
  - logs/E2_I2_optfreq_c000_r2.log e89f464f0712f44ea7e5520d0052a5b9b8a2b8cde86e1bbcb0cfc0dd8e828eee（916，产物极小值）
  - logs/E2_scan_C4O6.log c2d093fc91b7c0a88246b75e19785cd30fcf7292fe2d6a897deaf80af57aff3c（917，14 点弛豫扫描）
  - ts/ts_0005/jobs/declaration_0002/ts_opt/refine.log 72a641896e37d8ea5378cc874cd1959c64337638e9137d52b8d45bb880ac3a66（933）
  - ts/ts_0005/jobs/declaration_0002/frequency/frequency.log c5b0e878123f74420937b997d5d13520e73ba3421aba30f38b8c052752f241d6（936，1 虚频 −74.5623）
  - ts/ts_0005/jobs/declaration_0002/irc/irc.log d57877020625971602fb4d6dda7d1260aa5d0169d3c08e6577683ccc510a8039（941，积分失败）
  - ts/ts_0005/jobs/declaration_0003/ts_opt/refine.log fa7f1f5571106e74210dfb404defb53fd3e670ddab095c4935565a6ee6ff39cd（948，134 步未收敛）
- 方法一句：Gaussian 16 `/home/ly/g16/g16`，B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight，气相（无 SCRF），q=+1/m=1，26 原子 C6H17O3；TS/IRC 全程走 ts_prepare/ts_resume。
- 待裁决：①E2 是否应与 E3（1,2-甲基迁移 5.16）合并 / 是否记为无垒；②"水桥接/换水"构型（比 mapped-I1 低 10.95 kcal/mol，但 C4–O6 已断）是否应作为独立节点登记；③是否需要追加 2D 扫描或 2.4–2.9 Å 细网格受限扫描（本道可做，但需协调者批准预算）。
- 下一步（若获批准）：可选 (i) 2.4–2.9 Å 细网格受限扫描（0.05 Å）判窄垒；(ii) 2D 扫描 (C4–O6, C4–O10) 检验耦合；(iii) 从 attempt2 末帧做无约束 Opt+Freq 确立该换水构型极小值与能量。**不再重复相同 guess 的 TS 尝试。**


## ⏱ 交接快照 v2（2026-10-16 00:0x，平台第三次写锁重启前写入 —— 若我的会话被收尾请继承人从此接手）

**正在等的作业（我这条道的手工作业 = 2 个，已达本包并发上限）**
- **job 976 = 产物侧外框 Opt+Freq**：输入 `logs/E2_outframe_prod_optfreq.gjf`（sha256 f3ad355957632b9f59c2f28072077b30c2e3dc75998f29d832a428893354909c），起点 = 917 扫描末帧（r(C4–O6)=3.900 Å，**该帧 C4–O10 已成键 1.551 Å**）`seeds/scan917_last_frame_r390.xyz`（sha256 749a88b97c45324458c77c1650234e4d83947646d0e74960e8bf30843cd08501）；8c/10240MB。
  判据：落点若 = I2 极小值（E=−463.981552572、C4···O6=4.035 Å）→ 产物侧连通；若 = C4–O10 成键新物种 → E2 声明产物不是该坐标的自然产物（并入 Q2 裁决 + 新节点登记）。
- **job 982 = 反应物侧外框 Opt+Freq**：输入 `logs/E2_outframe_react_optfreq.gjf`（sha256 83d4f16dcc9bba4458508823224dfd77a1e31ab9be305b9d2958cae6a28388f4），起点 = 964 扫描末帧（r(C4–O6)=2.032 Å）`seeds/scan964_last_frame_r203.xyz`（sha256 54ee76f87cd811a79d4faf5b29f47c63bebd91c1caa6007be7a06aa4c1d86a80）；预期落回 I1（E=−463.999955035）。
- 计划中（等上面其一终态后再提，保持 ≤2）：**attempt2 末帧 `structures/attempt2_last_frame.xyz`（sha256 5e024c01e83bb4b8d51f6f8f9d0dc0bd8cb52be334d625df71c1b53d1675a815）的无约束 Opt+Freq** → 确认"换水/水桥接"构型 0 虚频极小值并登记新节点候选（主协调 23:xx 指令 ④）。

**新增科学证据（本轮）**
1) **job 964（0.05 Å 细网格，2.632→2.032 Å，13 点）done**：logs/E2_scan_fine_C4O6.log（normal termination，sha256 59d77190f6c0c2c087db198f4e568615ebc77eee968975c68d1a551e591e890e）→ **窗口内单调下降、无内部极大、无窄垒**（每步 −0.04…−0.94 kcal/mol）；逐点表见 E2_NOTES.md §3.10。合并 917（1.544→3.900 Å）→ **1.54–3.90 Å 内沿 C4–O6 的约束极大唯一，在 r≈2.63 Å = +16.26 kcal/mol**（−463.974050240 @964 日志:2759），与无约束软鞍点（job 933：−463.974034272）自洽到 ~0.001 kcal/mol。
2) **917 末帧结构 = C4–O10 成键（1.551 Å）**：说明 1D 面大 r 侧走的是"C4 被相邻 OH 分子内捕获"的另一条谷（环氧化物/氧鎓型 + 水），**不是**通往声明 I2（C4···O10=4.035 Å、未成键）；与 attempt 2 被"另一个水 O1"捕获（C4–O1=1.498 Å）互相印证 → "自由离子对"在该气相模型很可能不可及。

**E2 交付口径（不变，按 §3.2a + BRIEF §9）**：**不填任何数值**；可交付 = 无合格独立鞍点证据包（917+964 逐点表、候选软鞍点 933/936、IRC 941 失败、attempt2 948 未收敛/换水构型、以及 976/982 外框连通性结果）+ 裁决问题 Q2a（是否接受 candidate_only +16.26）、Q2b（是否与 E3 合并）、Q2c（换水构型是否登记为新节点）。工具面限制（IRC 步长/算法无声明入口，最小复现 + sha256）已发协调者 as_a2aa6951d46042ae。
