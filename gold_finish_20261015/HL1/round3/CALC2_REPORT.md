# CALC2 报告 · HL1_E1 · A 族递推 + N 侧驻点身份 + 反向剖面

计算 owner：as_a341823c436e47ed（CALC2 包）；出报告时间：2026-10-15 23:5x（SGT），**进行中（批次 3/4 已提交，T3c 待跑）**。
引擎/方法（全线统一，BRIEF §3）：Gaussian 16（/home/ly/g16/g16），B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight，**气相（不写 SCRF）**，q=+1、m=1，闭壳层；19 原子 C4H12NO2+。手工作业 8c / 10240 MB / priority 0，同刻 <=2。
原子序（沿用 ts_run/NOTES.md，1-based）：1=O1(H3O+ 的 O)、2=H2(声明的转移质子)、3=H9、4=H10、5=C11、6=C5、7=C4、8=N6、9=O9(肟 O)、10=C3、11-13=H(C11)、14-15=H(C5)、16=H16(肟 OH 的 H)、17-19=H(C3)。
判别式（本包预先声明）：R(1,2) <= ~1.05 A 且 R(2,9) >= ~1.4 A 且 0 虚频 ⇒ A 型 RC 极小值存在；R(1,2) ~ 1.38 / R(2,9) ~ 1.08 ⇒ 坍缩到产物侧 B 极小值。

## 0 结论速览（证据见 §1 起）

- **A 型 RC 极小值是否存在**：截至批次 1（2.60 / 3.00 / 3.50 A 单齿 + 双齿螯合）——**在已尝试的搜索中未找到 A 型 RC 极小值**：四种 A 种子未约束 Opt+Freq 全部坍缩到产物侧极小值。批次 2（4.20 A）与 N 侧身份见后续小节。
- 只报「计算完成」，**不宣称验收通过**；未回填任何数值、未改图、未动 registry/题面/STATUS.md。

## 1 job 965 · E2_RCbi_optfreq.gjf（双齿螯合种子，未约束 Opt+Freq）

| 项 | 值 |
|---|---|
| job_id | 965（query_compute_queue/terminal 与推送通知 state=done） |
| 输入 | /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HL1/ts_run/jobs/E2_RCbi_optfreq.gjf |
| 输入 sha256 | 6ab9b94e67c7f9c18b020149f1a86ab74965e506617f5da04b62eabc013b7670 |
| 种子 | ts_run/prep/RC_bi_seed.xyz（sha256 3874b0eeb18752dd…）；构造记录 prep/seed_bi_construction.json（sha256 026a9b54d22edddc…）；@种子 R(2,9)=1.6225、R(3,8)=2.2889、R(1,9)=2.6100 A |
| 原生日志 | .../HL1/ts_run/jobs/E2_RCbi_optfreq.log（32706 行，2002374 B） |
| 日志 sha256 | a4d182472ff195ac8c1e6bbc3a2c5a57e8daa67b29a45fee470c4a235d6e0dcf |
| 结束原文 | L30773 `Normal termination of Gaussian 16 at Thu Oct 15 23:19:49 2026.`；收敛原文 L30346 `Optimization completed.` / L30347 `-- Stationary point found.` |
| 频率 | 51 个实频、**0 虚频**、最低 27.0812 cm-1（log_parser） |
| 末步 SCF Done | L30140 `SCF Done:  E(RB3LYP) =  -364.295965301     A.U. after    7 cycles`（振荡段末 SCF L31128 同值） |
| 终态距离 | R(1,2)=1.3811 / R(2,9)=1.0774 / R(1,9)=2.4568 / R(2,8)=2.0727 A（由 format_converter log→xyz 导出的末帧 round3/E2_RCbi_final.xyz，sha256 cb1559ea1024aef39f858ea0764c85eceed4c1df11fc24edfc7b7c46c18c8303；）另 R(1,3)=0.9703、R(3,8)=3.2836（H3 留在水 O1 上） |
| 结论 | **坍缩**：质子已从 O1 转到 O9（R(2,9)=1.0774 为 O-H 键长，R(1,2)=1.3811 为强氢键），落在与 904/905/920 相同的产物侧 B 极小值（E=-364.29596530 ≈ B 的 -364.2959653）。双齿螯合 pose 未能把质子锁在 O1。 |

## 2 job 966 · E2_RC35A_optfreq.gjf（d(O1...O9)=3.50 A 单齿 A 种子）

| 项 | 值 |
|---|---|
| job_id | 966（state=done，推送通知已收） |
| 输入 | .../HL1/ts_run/jobs/E2_RC35A_optfreq.gjf |
| 输入 sha256 | 5748a44528e2a8680c31196100c3eab4bf298a7fda2a5c473ea190f80832cd17 |
| 种子 | prep/RC_35A_seed.xyz（sha256 b975fbf74df516aa…），起始 R(1,9)=3.5000、质子仍在 O1 |
| 原生日志 | .../HL1/ts_run/jobs/E2_RC35A_optfreq.log（29346 行，1791078 B） |
| 日志 sha256 | 48da3dcb0ca8e2bce3e9e3d67a15bf7d46bb6abcc963b0296b1499776302a384 |
| 结束原文 | L27424 `Normal termination of Gaussian 16 at Thu Oct 15 23:18:54 2026.`；收敛原文 L26998 `Optimization completed.` / L26999 `-- Stationary point found.` |
| 频率 | 51 个实频、**0 虚频**、最低 27.5286 cm-1 |
| 末步 SCF Done | L26803 `SCF Done:  E(RB3LYP) =  -364.295777129     A.U. after    7 cycles`（L27774 同值） |
| 终态距离 | R(1,2)=1.3878 / R(2,9)=1.0740 / R(1,9)=2.4601 / R(2,8)=2.0793 A（导出末帧 round3/E2_RC35A_final.xyz，sha256 e2fc5c07caae5b77f322955c0d23bef9653c5d93c959ca0907ee4da756737ce4）；R(1,3)=0.9700、R(3,8)=3.3408 |
| 结论 | **坍缩**到产物侧极小值（质子交到 O9）；与 job 965/904/905/920 的 B 极小值能量差 +0.000188172 Ha = **+0.1180 kcal/mol**（同程序同批相减），疑为产物复合物的另一构象。判据不成立。 |

## 3 待补（进行中）

- job 978 = jobs/E2_RC42A_optfreq.gjf（4.20 A，输入 sha256 ec9dcdc5e1b285e66fe73fec30a31439be5c15c9e95abaf5a89a451d496a0ac9）— 已提交，排队中。
- job 983 = jobs/N_side_optfreq.gjf（N 侧身份；种子由 T3a_ptscan_O1H2.log 经 format_converter 导出 → prep/N_side_frame_from_T3a.xyz sha256 dfacf479…；输入 sha256 0ff3f55d…）— 已提交，排队中。
- T3c 反向剖面 jobs/T3c_revscan_H2O9.gjf（输入 sha256 f16801286becbd16f7fde94d3e6fe42fc320d334c9d351320c9c14668e31297c）— 待提交。

## 4 平台观察（#176 复发，只读取证；不属本包范围）

23:20–23:41 期间 `更新数据库失败：database is locked`：guard-965.log / guard-966.log 末行逐字；HI1 的 guard-963.log 同形；NR1 的 guard-964.log 先失败后补写成功。当时 `pgrep -c -x g16` = 0 而 ledger 仍记 963/964/965/966 running（32 核空占）；提交侧两次返回 `database is locked`，重试后 job 978/983 成功。本轮自愈，未做任何处置（未重启服务、未杀进程、未改数据库）。已发帖 coordinator（evt_155f7c7df9234f33）。
