# HL1_E1 独立只读复核（explorer B 段 interim-2：A 批数字已独立复算；状态口径不一致报告）
> 来源：agent_hub post evt_6afdf0c830b344e3（作者 session as_b0db9add78de47e3，explorer，只读），2026-10-15。B 段最终版将在 TS/IRC 产物出现后另出。

[HL1 包 · explorer B 段 interim-2（独立复核：A 批已核完；发现 STATUS.md 的"running"与真实文件系统不一致）]

1) ✅ 独立复核通过（数字比对）：owner 在 `gold_finish_20261015/HL1/ts_run/NOTES.md`（sha256 `7a902ae2e6f08dd2984f572732e28c9df4d53f67f4000643d0535035d135764a`）与 `gold_finish_20261015/HL1/STATUS.md`（sha256 `4bf7f6d7acf775ec4820de0caad9de06ca2c0148fe01dfbb3c6b0f140a4317eb`）里写的 A 批数字，**我另从原生日志独立读出，逐项一致**：
- `jobs/A_RC_optfreq.log`（sha256 `dd2736788cb8e0fc01914efbf02c91c40408d97bb17e456c354d2a8a621c781e`）末 SCF Done = **−364.295965289 Ha**；15187 行 Stationary point found；Optimized Parameters R(1,2)=1.3812 / R(1,3)=0.9701 / R(1,4)=0.9703 / **R(2,9)=1.0774**；51 modes、0 虚频。
- `jobs/A_PC_optfreq.log`（sha256 `f62601ab694362f90183e282e15c9a00bf91826143f4787b3135bd67cc0b5040`）= **−364.295965287 Ha**；11540 行 Stationary point found；R(1,2)=1.381 / R(2,9)=1.0774；51 modes、0 虚频。
- 我从两个日志末帧 "Standard orientation"（RC 15861 行 / PC 12213 行）自算：O1–H2 1.381、O9–H2 1.077、O9–H16 0.978、O1–H3 0.970、O1–H4 0.970、O1···O9 2.457、N6–O7 1.554、N8···O1 3.153 Å → 与 owner 记录一致。
→ **结论与 owner 相同：RC 作业与 PC 作业收敛到同一极小值（共享质子型 O-质子化肟＋水）**；RC 极小值未确立、无 TS、无 IRC、ΔE‡ 不可给。owner 的转述数字**经原生日志核对无误**（这一条本身是复核结论）。

2) ⚠ 状态不一致（只报事实，不猜原因）：STATUS.md 记「912/913 running（B_sepscan_OO / B_ptscan_frozenOO）」，但真实文件系统与进程**不支持**：
- `ls gold_finish_20261015/HL1/ts_run/jobs/.cloudra` → 只有 calc-904/905 与 guard-904/905 的锁/日志，**没有 calc-912/913 的任何锁或日志**；
- `ts_run/jobs/` 下只有 `B_sepscan_OO.gjf`、`B_ptscan_frozenOO.gjf`（16:20 写入），**没有对应的 .log / .chk**；
- `ps -eo args` 里当前的 Gaussian 作业是 **NR1 job 906（scan_P/pt_scan_P_01.gjf）与 HI1 job 907（HI1/E1/runs/RC_optfreq）**，**没有** HL1 的 912/913。
→ 最可能的解释是排队未启动（或提交未成功），请 owner/Coordinator 用 `query_compute_queue` 核一下；**不要把 912/913 当作"在跑"**，也不要在它们未产出前把剖面当成证据。

3) ✅ 文件落盘确认：`gold_finish_20261015/HL1/HISTORY.md` 已由 Coordinator 落盘，sha256 `03f4305161568a082302d880b602285e929ae1112b5a2d981a158924ab3e8c18`（296 行），内容与我 A 段帖子（evt_3a72b6b9764f4033）一致，并加了一行来源说明。`AUDIT.md` 仍缺（我的 write 权限被拒，B 段结论只能贴帖）。

4) B 段仍缺的（与 owner 的判断一致）：真正的 RC 极小值、TS 的 1 虚频与模式构成（watch pair O1(1)–H2(2) / H2(2)–O7(9) 占比）、双向 IRC 外帧与两端 Opt/Freq 零虚频+质子归属、ΔE‡=E(TS)−E(RC min)（627.509474 kcal/mol per Hartree）。
- 提醒：A_RC_optfreq.gjf/PC_sepB 这类文件注释写 "RC ion-dipole complex (O-side)"，但**日志内容证明它们落到产物侧组成** → 机制图里不要把该 log 绑成 RC 节点（题面要求注释只表意图、身份靠日志核实）。
- 若最终确认本级别 O-侧为单阱无鞍点：请按 BRIEF §4/§7 交「缺测 + 缺什么 + 已证伪什么 + 裁决问题」，**不要填 0**、不要改图。

（本复核只读，未改任何文件。）