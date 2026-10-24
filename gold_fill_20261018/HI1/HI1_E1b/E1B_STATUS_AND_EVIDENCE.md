# HI1_E1b（HI1_E2）· 状态与实测证据 —— **重建版 v2**（2026-10-18T06:1x）

> **事故自陈**：本文件于 2026-10-18T06:09 被我自己的 write 以空内容覆盖（与 06:04 PROCESS.md 被截断同一类事故；截断后 sha 01ba4719…、1 字节）。本版按本会话内的原始写入块重建；关键数值同源码：本轮实测，并已在 AgentHub 报告与同目录 `REPORT.txt`（3,047 B）留过一份。原生日志仍未动。

## 1 模型与声明（沿用，不重算）
- 27 原子子系统 C8H15NO3，q0/m1，工作序 = INT1_27 序（1-based，atom_map = identity）。
- 反应中心（1-based）：**form (2,4) C2–C3、(3,10) O4–H22；break (4,10) C3–H22、(2,3) C2–O4**。
- 方法固定：Gaussian 16（/home/ly/g16/g16）B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight + SCRF=(CPCM,Solvent=DMSO)；资源 %nproc=4 / %mem=6144MB。

## 2 分母（本步起点极小）—— 已回读原生日志确认
- 日志：`gold_finish_20261015/HI1/E1/split/INT1_27_optfreq.log`，**sha256 c03e0a82d78d22b96474ab48ee40799adb63a894bb9cefcd27c7051799024f63**，30,757 行；几何帧 `INT1_27_opt_frame.xyz` sha b2f2ffaaf64169916e29d59fa44a49e223e394e21f69907980b8a83151fa5d36。
- **E(RB3LYP) = −593.929762803 Eh**（L26615 opt 末帧 / L28142 freq 段单点，同值）；`Optimization completed.` L26903、`-- Stationary point found.` L26904；`Normal termination` L27581（14:31:05 opt 段）/ L30757（14:35:06 整作业）；`Error termination` 0 条。
- `Frequencies --` 25 组 = **75 模 = 3N−6（N=27）**，`imaginary` 0 条；伪模 L28588；**最低实模 78.1490 cm⁻¹（L28598）**；版本 L78 = Gaussian 16 ES64L-G16RevC.01。
⇒ 分母口径成立（同程序同方法同模型，0 虚频）。

## 3 TS guess（构造与自查）
- 文件 `build/ts_guess_27.xyz`，**sha256 88162e53ae6598e8550cc1e4f2a0037fda402a0212e6b607267ee8d97f585d4d**；建构脚本 `build/build_final.py`（sha b2eccbcdffda209ded10da6632583c52cb58348550f0baf78b8ca652646be18e）由分母帧内坐标插值（r(C2–O4) 1.4208→2.200、r(C2–C3) 1.5351→1.440、ang(C3–C2–O4) 108.87°→90.00°、H22 置 C3···O4 远侧分支）。
- **实测关键距离**：R(2,4)=**1.4400**、R(3,10)=**1.3507**、R(4,10)=**1.3547**、R(2,3)=**2.2000**、R(2,18) C2–N20=1.4755（起点 1.5351 / 2.7348 / 1.1006 / 1.4208 / 1.4755）。
- **最小原子间距 0.9699 Å（O4–H21）≥ 0.9 ⇒ 自查通过**；无 H 落在任一重原子 0.5 Å 内。登记张力 r(C2···H22)=**1.5947 Å**（1-3 关系）⇒ 高张力四中心协同质子转移假设（未验证）。
- provenance 缺陷：旧 `TS_GUESS_PROVENANCE.md`（sha 510909cf…）的 guess sha 0c8e4687…、build sha 3d8161…、最低实模 78.1638 均写于最终构建之前，与本文件实测不符，**勿引用**。

## 4 durable TS 工作流（ts_0026）
- guess = provided（运行内副本 `path/input_0003/provided.xyz` sha 88162e53…）；reactant = 分母帧；product = `build/product_start_27.xyz`（sha 21b910fe41146bf0f47ba5603ee3689214e69c2c5e09eae8582eb87e31c398d4，仅端点种子，不主张是极小值）。
- 阶段方法全部 ref=g16；IRC ref=g16_irc = 同 route + `irc=(calcfc,maxpoints=80,stepsize=5,recalc=10)`；execution cpus=4 / memory_mb=6144。
- ts_opt 输入 `jobs/declaration_0003/ts_opt/refine.gjf` sha256 **658b0cc3e836d8ef929f2e634aa30376dbe65bdfb157119db91af67ad3df51c7**，route `#p opt=(TS,calcfc,noeigen) b3lyp/def2svp empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=dmso)`，%nproc=4 / %mem=6144MB。
- 历史 attempt：0 = map 歧义（blocked，已由 selected_candidate 解决）；1 = job 1091（被 1092 取代）。

## 5 已登记的输入缺陷（因停算未修正）
- `reaction.reaction_center` 被写成 0-based `[[1,3],[2,9],[3,9],[1,2]]`，契约要求 1-based，**正确值 `[[2,4],[3,10],[4,10],[2,3]]`**；只影响 run 自带 mode 份额/方向诊断，不影响作业物理（opt=(TS,calcfc,noeigen) 不读该字段），也不影响 IRC 端点身份（走 species atom map）。

## 6 D1 判据进度（最终）
| 项 | 状态 | 说明 |
|---|---|---|
| (a) 方向 | **未测** | 需虚频模矢；测法 = `analysis/d1_report.py`（sign-free 形状判定 + s/δR 两种标度） |
| (b) 成分 | **未测** | 三份额：声明中心对原子 {2,3,4,10} / 全重原子 / 最大单原子 + 最大自由度；只记录不设阈值 |
| (c) 交付 | **未过** | 缺 TS 恰 1 虚频 → 双向 IRC → 两端 Opt/Freq 0 虚频 |
⇒ 现值 **null**，不回填、不得引用任何数值作势垒。

## 7 判据脚本与协调口径（可复用到新题）
- `analysis/geom_check.py`（sha b956470864a4cf3f97cacf411f728d114bfbf5c46bd7043d4eb00dde5ac26ba1）：几何 minsep 与关键距离。
- `analysis/d1_report.py`（sha **94e282021720cd3a212ce8027cdc992efbe7fde7830ef7d33cd65423148aaf6a**，主脚本）：① 27 原子「序号→元素＋角色」全表 ② 反应中心候选原子（2,3,4,10,18,27）<2.0 Å 近邻表 ③ 虚频三份额 + 最大单原子自由度 ④ (a) **sign-free 形状判定**（form 两对同号 + break 两对同号 + 两组相反 ⇒ 形状过；方向须由 IRC 端点钉定，**不得凭模态符号**）⑤ 两种投影标度（单位模矢 s；\|d\|_total = 0.1 Å 的 δR）。
  自检（job 1051）：R(2,4)=1.5351 / R(3,10)=2.7348 / R(4,10)=1.1006 / R(2,3)=1.4208 与几何帧逐位一致；身份表确认 2=C2、3=O4、4=C3、10=H22、18=N20、27=H21；近邻：2→O3 1.421/N18 1.476/C1 1.534/C4 1.535；3→H27 0.970/C2 1.421；4→H8 1.099/H9 1.099/H10 1.101/C2 1.535；10→C4 1.101；18→C17 1.468/C2 1.476/C14 1.477；27→O3 0.970。
- (b) 双套份额口径：(A) run 侧 frequency_analysis（misaligned 也照登；不存在则写明原因）与 (B) 我 1-based 脚本份额并列，逐项 |A−B|，>0.02 单列点名，不取平均。
- #184：IRC 无入口设 MaxPoints/StepSize（keywords 被拒、end_setting 被静默丢弃）⇒ IRC 只作方向证据，端点身份由最外层帧 Opt+Freq 承担，并逐字写「未达声明端点」。
- ts_resume 在作业 running 时被契约拒绝（Running jobs prevent revisions）⇒ 改声明只能抓「上一作业终态、下一作业未起跑」窗口或趁下一作业仍 queued。

## 8 【调度终止】记录（2026-10-18）
- 依据：用户 05:0x 指令（协调者广播 evt_1368eb1b076741ac）「被换掉的题的任务可以杀了」。
- 执行：ts_stop(run_id='ts_0026') → run **status=stopped**、**revision 23**、stage refine；job **#1092 = cancel_requested**（04:51:04 发起）。
- **#1092 终态 = cancelled @ 2026-10-18T04:51:42**，last_error 空；`.cloudra/calc-1092.exit.json` → **exit_code = −15**（SIGTERM）；`guard-1092.log` → calculator 退出码 241；`calc-1092.out.log` 的 Error: software termination + l502 栈回溯 = 信号打断，**不是** Gaussian 科学失败。
- 停止瞬间日志：`ts/ts_0026/jobs/declaration_0003/ts_opt/refine.log`，1,519,164 B，**sha256 a27d5f147487f099e7938798bd63a96bd61ae4c0b405d3b33de5de9a5af6099d**，mtime 04:50（停止后无新内容）；`Step number 33 out of 153`（L23848）、末条 `SCF Done −593.859284599`（L23775）；Normal termination 0、Gaussian Error termination 0 ⇒ **未收敛、未进 freq、无虚频**。
- 口径：**调度终止（SIGTERM，用户指令）**，不写「算不出来/发散/未达极小」；第 33 步过程能量不作 ΔE‡。
- 槽位：释放 4c/6144；05:12 实测队列已由新题作业（1158/1159/1168/1172–1175）填满。

## 9 更正记录（2026-10-18T06:09）
- 我 05:5x 曾写「job 1032 = ts_0012 declaration_0001（E −939.293671629、虚频 −27.9419）」，**该条错误、已撤回**。实测 `ts/ts_0012/process.json`：attempt 0（declaration_0001）= job 1000/1013/1021/1026；`state_1032.json` 位于 `jobs/declaration_0002/ts_opt/`，job_id=1032、declaration_revision=2 ⇒ **job 1032 = declaration_0002**（E −939.283734374，配 −314.2861）。协调者原表述（−939.283734386 为 TS 驻点、与 1032 帧同一驻点）是对的。该批数据属 EM1 车道，本节只作记录。

## 10 归档位置
- 本文件（重建版）；`REPORT.txt`；`STATUS_STOPPED_20261018.md`；`TS_GUESS_PROVENANCE.md`（数值作废、构造说明有效）；`build/`；`analysis/`。
- `ts/ts_0026/process.json`（rev23、status=stopped）与 `jobs/declaration_0003/ts_opt/{refine.gjf, refine.log, .cloudra/}`；`DASHBOARD.md` 的 #1092/HI1_E1b 行已改记为「调度终止」；`PROCESS.md` 已追加 HI1_E1b 归档节。
