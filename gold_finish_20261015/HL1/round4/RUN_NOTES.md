# HL1 round4 · small_mol 手工作业运行笔记（进行中）

角色：small_mol 手工 Gaussian 道（本包 round4）。工作根 /home/ly/Cloudra-mechanism-agent；
本包目录 gold_finish_20261015/HL1/round4/。方法逐字：Gaussian 16（/home/ly/g16/g16），
B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight，气相（无 SCRF），1 1；
手工作业 8c / 10240 MB / priority 0；本包同刻手工在飞（含排队）<=2。

## 0 任务与状态（2026-10-17 06:4x 起）

| 任务 | 作业 | job_id | 状态 |
|---|---|---|---|
| T1 N 侧驻点身份（未约束 Opt+Freq，种子 prep/N_side_frame_from_T3a.xyz） | round4/T1_N_side_optfreq.gjf | 995 | **done**：E=−364.326887706 Ha、51 模 0 虚频、N-质子化肟+水（= job 978 同一驻点第二条路径） |
| T2a H3O+ 单体参考 Opt+Freq | round4/T2_H3O_monomer_optfreq.gjf | 996 | **done**：E=−76.6445472086 Ha、6 模 0 虚频 |
| T2b (E)-丁酮肟单体参考 Opt+Freq | round4/T2_oximeE_monomer_optfreq.gjf | 1002 | **done**：E=−287.574297051 Ha、39 模 0 虚频、(E) 保持 |
| T3 质子转移弛豫剖面（从 B 出发扫 R(H2–O9) 1.0774→2.0274） | round4/T3_ptscan_H2O9_relaxed.gjf | 1005 | **done**：20/20 收敛、Normal termination；**内部极大 pt8 = +3.5705 kcal/mol 相对 B**；下坡支 = H4→N6 N-质子化通道 |

## 1 输入文件 sha256（本批原生产物，未改写）

| 文件 | sha256 |
|---|---|
| round4/T1_N_side_optfreq.gjf | 0ad4576c6966abb65c12d1aaf105514c5ff7cef3e0eff60f6e33036d55d39ae6 |
| round4/T2_H3O_monomer_optfreq.gjf | 69a0b6ec037b492235f2a5fcd3094a8aeb564adfedd6b22f41ee3ad454479de3 |
| round4/T2_oximeE_monomer_optfreq.gjf | e9d1773f023b95989273704a74e81715628395558469be671e29edc9463e28ba |
| round4/T3_ptscan_H2O9_relaxed.gjf | d4fa530ed2d2ab081699592cb031512eef5641ca431ba8b48b7030a5ffe697c3 |
| round4/geo_check.py（只读几何报告脚本） | 87f80f816eb93ca99d5c1c898454ae7eafcfd9c5729465f7dab1a537a8891383 |

路由逐字（T1/T2）：`#p opt freq B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight`；
（T3）：`# opt=(modredundant,maxstep=10) B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight`。
均无连字符 def2-SVP 写法（job 983 的 QPErr 教训已规避）。

## 2 种子与来源（坐标未手写，全部来自平台工具/上一轮日志）

- T1 种子：ts_run/prep/N_side_frame_from_T3a.xyz sha256 dfacf479e41752b8ffc004631135a260e3c53cb752a4b8aa8c58c4357f378538（19 原子）；
  来源 = format_converter 从 ts_run/jobs/T3a_ptscan_O1H2.log（sha256 22dd89f4a0fa99849d6fd844582f8b1888009c498848ae7424ae9b042569d67e）导出的末帧，
  该日志末段 SCF = -364.301672236 Ha（未收敛中间帧，l103 终止）。实测该帧 R(1,3)=1.2077 / R(3,8)=1.2184 Å ⇒ H3 桥接 O1/N8，不是 N 侧驻点证据本身。
- T2 单体种子：ts_run/prep/monomer_H3O.xyz sha256 74364568…（4 原子，R(O-H)=0.9910×3，H-H=1.6376 全部相等 ⇒ C3v H3O+，种子干净）；
  ts_run/prep/monomer_oximeE.xyz sha256 1c807f30…（15 原子，C=N 1.3003 / N-O 1.3989 / C-C 1.5173 / O-H 0.9754 Å，乙基与 N-OH 反式 ⇒ (E) 构型，种子干净）。
- T3 起点：ts_run/jobs/A_RC_last.xyz sha256 303ec8b48b90fdb1369e31e5eb667b1d222098e29a87a91f11ff6598ffb5afe6（= 产物侧极小值 B 末帧）。
  本道独立复核（round4/geo_check.py 实算）：R(1,2)=1.3812 / R(2,9)=1.0774 / R(1,9)=2.4569 / R(1,3)=0.9701 / R(1,4)=0.9703 /
  R(9,16)=0.9779 / R(8,9)=1.5535 / R(7,8)=1.2798 / R(2,8)=2.0725 Å；
  对应日志 ts_run/jobs/A_RC_optfreq.log sha256 dd273678…：log_parser 实读 E = -364.2959652889999 Ha、51 模、0 虚频、最低实频 27.1816 cm^-1。

## 3 T3 构造与理由（预先声明，防事后解释）

- 目标：判定「沿 O1–H2 / H2–O7 质子转移坐标的弛豫剖面是否存在内部极大」。
- 构造：单坐标弛豫扫描（Gaussian opt=modredundant + `B 2 9 S 19 0.05`），扫描 R(H2–O9) = 1.0774 → 2.0274 Å，
  其余全部自由度弛豫。理由：
  (a) 被扫坐标就是「产物侧已成键」的键长（点 1 即为已收敛极小值 B 本身），起点条件良好；
  (b) 质子被迫离开肟 O9，最近的碱是水 O1（B 中 R(1,2)=1.38 Å），因此扫描自然覆盖 O9→O1 的质子回传；
  (c) 扫描后段（R(2,9) ≳ 1.9）即「质子已在 O1 一侧」的离子-分子对端，满足任务「覆盖到质子回到 O1 一侧」。
- 与已知失败模式的区别：913 用 `B 1 2 S` + `B 1 9 F`（扫描+冻结混用）在 point 1 报 l103 Error imposing constraints；
  921 从 A 侧（质子已在 O1）扫 `B 1 2` 递增、方向与自发迁移方向相反，中途 H3 迁到 N8 导致 Berny 冗余坐标崩坏（Tors failed 3-1-9-16 / 4-1-9-16）。
  本构造不使用冻结坐标、不从高位错配起点出发、扫描坐标与自发松弛方向一致。
- 若扫描在中途失败：改用逐点独立约束优化（每点单约束 `B 2 9 F`，取上一点末帧作起点），并逐点留「Optimization completed + SCF Done」原文；
  失败点与已收敛点分别登记。

## 4 待办

1. 等 job 995/996 终态通知 → 立即用 log_parser + format_converter 取「Normal termination / Optimization completed / 末步 SCF Done 原文+行号 / 模数与虚频 / 末帧关键距离」。
2. 释放槽位后提交 T2b + T3（batch 2）。
3. 全部取证后写 round4/CALC4_REPORT.md（逐作业一节；区分「计算完成」与「验收通过」）。
4. agent_hub 回报（首行 to: as_939ca5a73ff445c2）。
