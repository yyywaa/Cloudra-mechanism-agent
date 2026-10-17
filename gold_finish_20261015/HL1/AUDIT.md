# HL1_E1 独立只读复核（explorer B 段 interim：首批 ts_run 日志，尚无 TS/IRC）
> 来源：agent_hub post evt_c5f0f7152f6d4714（作者 session as_b0db9add78de47e3，explorer），2026-10-15。B 段最终版将在 TS/IRC 产物出现后另出并覆盖本文件。

[HL1 包 · explorer B 段 interim（ts_run 首批产物：A_RC_optfreq / A_PC_optfreq）]
⚠ 本会话 write 权限被拒 → `gold_finish_20261015/HL1/AUDIT.md` 无法由我落盘，请 Coordinator 把本文原样保存到该路径。本段**只做了能做的部分**：ts_run 现在**没有 TS、没有 IRC**。

0) 工具限制（须记录）：本会话**没有 log_parser**（`get_tool_docs(['log_parser'])` 返回 "Unknown or unavailable tool names"）。故虚频/能量/几何全部由我**直接读原生日志**得到（grep + read 末帧块），每条给出日志行号，可独立复算。

1) ★重大发现：**A_RC_optfreq 收敛到的不是声明的 RC**
- 输入 `A_RC_optfreq.gjf`（Abs `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HL1/ts_run/jobs/A_RC_optfreq.gjf`，sha256 `339108576666454a6eadaa583aff77ee1a66a1db480920756ed61dce06c142ac`，28 行）确为 O-侧 RC 种子：H2 距 O1 = 0.988 Å（H3O+ 形式），H2···O9 = 1.61 Å。
- 但 `A_RC_optfreq.log`（同目录，sha256 `dd2736788cb8e0fc01914efbf02c91c40408d97bb17e456c354d2a8a621c781e`，17531 行）第 15187 行 "Stationary point found"，其 "Optimized Parameters" 块（15189+）逐字给出：`R(1,2) 1.3812`、`R(1,3) 0.9701`、`R(1,4) 0.9703`、`R(2,9) 1.0774`、`R(5,6) 1.5341`。
  → **H2 已从 O1 移到 O9（肟 O）**：O1 只剩 H3/H4（0.970/0.970）= 水；O9 同时带 H2(1.077) 与 H16(0.978) = **O-质子化肟**。
- `A_PC_optfreq.log`（sha256 `f62601ab694362f90183e282e15c9a00bf91826143f4787b3135bd67cc0b5040`，13883 行）同一批、**几乎同一几何**：`R(1,2) 1.381`、`R(1,3) 0.9701`、`R(1,4) 0.9703`、`R(2,9) 1.0774`、`R(5,6) 1.5342`。
- 电子能（各取日志最后的 `SCF Done`）：**RC 作业 −364.295965289 Ha**（14986 / 15960 行）；**PC 作业 −364.295965287 Ha**（12312 行）。差 **−1.3×10⁻⁶ kcal/mol**（我算 (ΔE)·627.509474）→ **同一个驻点**。
- 我另用日志末帧 "Standard orientation"（RC log 15861 行、PC log 12213 行）**独立复算距离**：O1–H2 1.381 / O9–H2 1.077 / O9–H16 0.978 / O1–H3 0.970 / O1–H4 0.970 / O1···O9 2.457 / O9–N8 1.554 / N8···O1 3.153 Å —— 与内部坐标块一致（自算，不是转述）。
→ **结论：A_RC_optfreq 与 A_PC_optfreq 收敛到同一极小值，组成 = 「H2O + O-质子化肟」；本步的 RC 极小值（H3O+ + 肟）目前尚未取得。**
→ 同时这是一条正面信息：无约束优化自发把质子交到**肟 O9（O-侧）**，不是 N8。
→ 附带：RC 种子首次 SCF = −364.264535571 Ha，收敛极小值 = −364.295965289 Ha → 落差 **−19.72 kcal/mol**（0.031429718 Ha × 627.509474）。O-侧 H3O+···肟 络合物在本级别**很可能不是极小值**（与历史「R 高于 I1／近无垒」方向一致；但历史那条 0 已作废，其数值不得引用）。

2) 虚频与模式（两日志最终频率块，直接读）
- 19 原子 → 3N−6 = **51 modes**；两日志各 17 行 `Frequencies --`×3 = 51 个值，**全为正**（最低真实模 27.1816 cm⁻¹（RC）/ 27.1707 cm⁻¹（PC））→ **虚频数 = 0** ✓。
- 诚实 caveat：两日志 `Low frequencies` 行首值 **−4.9332**（RC）/ **−4.8583**（PC）cm⁻¹，另有 0.6981/2.7267 与 1.3898/2.8855 —— 属投影后平动/转动残值（Gaussian 惯例，不出现在 Frequencies 列表内），**不计为虚频**；但最低真实模仅 ~27 cm⁻¹，络合物势能面很平。
- watch pair（本 run 实际 1-based 号，依 `prep/seed_constructionB.json` 的 order 串：1=O1、2=H2、8=N6、9=O7）→ 该 run 的 watch pair 是 **O1(1)–H2(2)** 与 **H2(2)–O7(9)**。在收敛极小值上：O1–H2 = 1.381 Å（已断）、H2–O9 = 1.077 Å（已成）→ 所以这个"共同极小值"**本身就是迁移后的状态**；O9–H2 1.077 比 O9–H16 0.978 长 0.1 Å，属**共享质子型强氢键**（O1···O9 仅 2.457 Å）。是当 PC 还是当"共享质子络合物"需 owner 定性。

3) ΔE‡：**不能给**（缺 TS + 缺真正的 RC 极小值）。若误把 RC 种子（−364.264535571 Ha，非驻点初猜）当 RC，会得到 **19.72 kcal/mol 的假值** —— 不得使用。

4) 验收链逐项（现态）
| 项 | 状态 |
|---|---|
| TS 原生正常结束 + 恰 1 虚频且以 O1–H2–O7 为主 | **未做**（ts_run 无任何 OptTS/IRC 作业） |
| 双向 IRC 到 H3O+···肟 与 H2O + O-质子化肟 | **未做** |
| 两端 Opt/Freq 零虚频 + 身份核验 | 零虚频 ✓（RC/PC 各 51 modes、0 虚频），但**两端是同一结构** → 不构成两个端点 |
| RC 几何：H3O+ 氢键在 O7 侧还是 N6 侧 | 现有驻点：H2 在 O9(=O7) 侧（O1···O9 2.457 Å ≪ O1···N8 3.153 Å）→ **O-侧**；但该驻点=产物侧组成 |
| ΔE‡ = E(TS) − E(RC min) | **缺** |

→ **「计算完成」= 否；「验收通过」= 否。** 缺：真正的 RC 极小值、TS（含虚频模式证据）、双向 IRC 端点身份、可相减的同批电子能。

5) 给 owner 的建议（不代替决策）
- 先判 O-侧 H3O+···肟 络合物在本级别**是否存在极小值**：约束优化/松弛扫描固定 d(O1–H2)（扫描只作**探索**，不作 gold 证据），或用更长 O···O、不同取向的种子重建 RC。若扫不到最小 → 本级别 E1 很可能**无垒 PT**，应如实报「缺测 + 为何缺 + 已证伪什么」，按 BRIEF §4/§7 提请裁决（**不要填 0**，也不要把产物侧极小值当 RC）。
- 若要建 TS：起点应从共享质子结构出发并必须能区别于产物侧；注意注意区分 O-质子化 vs N-质子化（历史 107 的 N 侧失败）。
- 身份提醒：`A_RC_optfreq.gjf` 注释写 "RC ion-dipole complex (O-side)"，但**日志内容证明它收敛到产物侧组成**；题面要求 log 不改写、注释只表意图、身份靠日志核实 → **不要**把该 log 绑成机制图的 RC 端点。

6) 证据清单（绝对路径 + sha256）
- `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HL1/ts_run/jobs/A_RC_optfreq.log` · `dd2736788cb8e0fc01914efbf02c91c40408d97bb17e456c354d2a8a621c781e`（17531 行；Normal termination 15610 行 "Thu Oct 15 16:16:02 2026"）
- `.../jobs/A_PC_optfreq.log` · `f62601ab694362f90183e282e15c9a00bf91826143f4787b3135bd67cc0b5040`（13883 行；Stationary point found 11540 行；Normal termination 11962 行 16:15:12）
- `.../jobs/A_RC_optfreq.gjf` · `339108576666454a6eadaa583aff77ee1a66a1db480920756ed61dce06c142ac`；`.../jobs/A_PC_optfreq.gjf` · `239bad2a8832713ba86c9d609294ffd46a564b56f854e20fa8d72ba8a3f1ee77`
- `.../jobs/state_904.json` · `80086b640803e6c4464416a1c48d7704ae66514d4e1a4bf44c8284232b5a6c6b`（= RC 作业，30 个优化步色散列表）；`.../jobs/state_905.json` · `7061be9ae90b1277fb2e3d20751eaafa076653497c2183771891fc57db2c197c`（= PC 作业，23 步）
- `.../jobs/RC_seedB_optfreq.gjf` · `74cea0f5be7c0557786d7cfb41209b2133485b27759a9ff1deb2c13164031980`；`.../jobs/PC_seedB_optfreq.gjf` · `a8cee3725fa3b3e207ef3add6d18ecb2b598c3e6da57d66181262a1900d1e8d9`（尚未运行，注释仍是 RC(O-side)/PC）
- `.../ts_run/prep/seed_constructionB.json` · `8883e502bb3d2a1ab4d01d2fe872856b99cfd4a34e360cdbbb2b58054556dc77`（1-based 号对照：1=O1 2=H2 3=H9 4=H10 5=C11 6=C5 7=C4 8=N6 9=O7 10=C3 11-13=H(C11) 14-15=H(C5) 16=H8 17-19=H(C3)）
- 方法（两作业 .gjf 第 3 行逐字）：`#p opt freq B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight`，`1 1`，气相（无 SCRF），%nproc=12。

7) 我下一轮会做（等 TS/IRC 出现）：TS 最终频率块虚频个数与模式构成（watch pair 占比/重原子占比）、双向 IRC 外帧朝向、两端 Opt/Freq 零虚频与质子归属（H2 在 O7 上、O1 只带 H9/H10）、ΔE‡ = E(TS) − E(RC min)（627.509474 kcal/mol per Hartree）。

（本段未改任何文件；A 段 HISTORY 内容见 post evt_3a72b6b9764f4033，同样因 write 权限未落盘。）