# STATUS · N_HNCO_HYDROLYSIS（异氰酸单水气相水解，HNCO + H2O → NH3 + CO2）

工作目录：`gold_fill_20261018/N_HNCO/`　｜　方法：Gaussian 16（/home/ly/g16/g16）B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight，气相、q=0/m=1、闭壳层；%nprocshared=8 / %mem=14336MB / priority 0。
能量口径：只用同批 Gaussian `SCF Done` 纯电子能相减，无 ZPE/热校正，不跨程序混减。
输入草案：`gold_compute/queue_20261018/specs/TASKSPEC_N_HNCO_HYDROLYSIS.md`（197 行 / sha256 facd0b91de9dec94c68fb3f334a44f12ec73da0b996eb3fe9fac26338fc5c9ca）。

## 0. 当前状态（随时更新）

| 项 | 状态 |
|---|---|
| 原子序（全程固定） | 1=C1(异氰酸 C)、2=O2(C=O)、3=N3、4=H4(N–H)、5=O5(水的 O)、6=H6(E1 中迁到 N3)、7=H7(加成后留在 O5、E3 中迁到 N3) |
| R 复合物初猜 | HMFF/MMFF 组装 HNCO···OH2（N–H···O 氢键，H4···O5 1.723 Å、C1–O5 3.264 Å）→ `geom/R_complex.xyz` |
| I1 初猜 | 氨基甲酸 MMFF 构象，O2=C1–O5–H7 = 0°（syn）→ `geom/I1.xyz` |
| I2 初猜 | 同一分子绕 C1–O5 旋至 O2=C1–O5–H7 = 180°，H7···N3 2.998 → 2.048 Å → `geom/I2.xyz` |
| P 初猜 | NH3 + CO2 dot 复合物 → `geom/P.xyz` |
| E1 剖面 | **作业 1111（ts_0027 scan）已提交、排队中**（C1–O5 3.264→1.400 Å，17 点，opt=modredundant 松弛扫描） |
| E2 TS | **作业 1112（ts_0028 ts_opt）已提交、排队中** |
| E3 TS | **作业 1115（ts_0029 ts_opt）已提交、排队中**（曾因 CO2 两个等价 O 的对称映射歧义阻塞，已显式选 selected_candidate=0 解除，化学不变） |
| 预算 | 已用 3 / 16 个 QM 作业；预计主线 13（3 边四件套 12 + E1 剖面 1），余 3 作重试 |

> 注：`geom/*.xyz` 是 Agent 准备的初猜几何（非计算证据），已由 ts_prepare 的 build 阶段导入并存成 `ts/ts_00xx/build/.../snapshot`；一切证据以原生 Gaussian 日志为准。

## 1. 逐边交付（待日志回来后填）

| 边 | ΔE‡ | 起点极小值（路径+sha256+SCF 行号+能量） | TS（路径+sha256+虚频行号+虚频值+模矢主原子） | IRC + 两端 Opt/Freq | 身份核验 | 结论 |
|---|---|---|---|---|---|---|
| E1 R→I1 | 缺测（剖面排队中） | 缺测（R 端点待 IRC 反向端点 Opt+Freq） | 缺测 | 缺测 | — | 待测 |
| E2 I1→I2 | 缺测（TS 排队中） | 缺测 | 缺测 | 缺测 | — | 待测 |
| E3 I2→P | 缺测（TS 排队中） | 缺测（I2 端点待 E2 的 IRC 端点确认） | 缺测 | 缺测 | — | 待测 |

## 2. E1 协同 vs 分步（待剖面）

判据（coordinator 定）：出现两性离子驻点需同一点满足「C1–O5 ≤ 1.55 Å、O5–H6 ≤ 1.15 Å、N3–H6 ≥ 1.6 Å」且在 C1–O5 轴上为局部极大/平台（两侧能量都更高，或相邻点 ΔE < 0.3 kcal/mol）。斜率变缓但单调下降不算驻点。
剖面只作候选/上界，不是 ΔE‡。
→ 结果：待填。

## 3. E3 分母（连接构象）单列

- I2 二面角：待 Opt 后记录 O2=C1–O5–H7 与 H4–N3–C1–O2。
- 氨基甲酸全局最小构象能量与 ΔE(I2 − 全局最小)：待填（若 E2 的 IRC 端点显示构象面不一致，则按「构象面不一致，E3 分母改用 X」记录，不做拼接求差）。

## 4. 预算/作业清单

| 作业 | 用途 | 状态 |
|---|---|---|
| 1111 | E1 relaxed scan C1–O5（ts_0027） | ready（排队） |
| 1112 | E2 TS opt（ts_0028） | ready（排队） |
| 1115 | E3 TS opt（ts_0029） | ready（排队） |


## 5. 平台故障与自救（2026-10-18 05:0x）

- **现象**：所有 `job_type=gaussian` 提交在 admission 阶段被拒，报 `PATH is missing the programs required for gaussian compute; install and ensure one of these commands is available: g16, g09, g26`。
- **证据**：诊断 shell 作业 1119（done，1c）输出 `PATH=…:/usr/bin:/bin…`（无 /home/ly/g16）、`which g16 = MISSING`；但 `/home/ly/g16/g16` 存在且可执行（127313512 B，-rwx------ ly:ly），`g16root`/`GAUSS_EXEDIR` 未设置。日志：`gold_fill_20261018/N_HNCO/inputs/.cloudra/calc-1119.out.log`。
- 直接 submit_compute_job(gaussian) 的单点诊断输入同样被拒（job_id=-1，同一消息）。
- 队列已空（free 32c、0 running、0 queued）⇒ 与容量无关。
- **影响**：ts_0027（E1 剖面重提交）、ts_0028（E2 的 freq/IRC/端点）、ts_0029（E3 TS）全部卡在同一门；已报 coordinator 请求平台侧把 /home/ly/g16 加入执行 PATH（或设 g16root/GAUSS_EXEDIR）。

### 三个 run 的真实状态（不得记为科学失败）

| run | 作业 | 真实情况 | 下一步 |
|---|---|---|---|
| ts_0027 | 1111 | 真跑过；扫描点 1/18 用尽 28 个优化循环后 l9999 终止（`Number of steps exceeded, NStep=28`，scan.log L11545/L11724）。属 maxcycles 太小 + MMFF 复合物水取向自由，非化学失败 | 预取向起点（C1–O5 3.000，H6 朝 N3）3.000→1.400 Å / 17 点重扫（自救 shell 作业 1120） |
| ts_0028 | 1112 | **成功**：refine.log L2469-2470 `Optimization completed / Stationary point found`、L2661 `Normal termination` | 待平台恢复后 FIFO 走 freq→IRC→两端 Opt+Freq |
| ts_0029 | 1115 | 从未起算（无 refine.log），admission PATH 门 | 待平台恢复后重提交（reaction_center 已重新声明） |

### 自救：E1 剖面（不做 TS/IRC，只用 shell 调 g16）

- shell 作业 1120：`gold_fill_20261018/N_HNCO/jobs/E1scan/run.sh` → `E1_scan_manual.gjf`（`opt=(modredundant,maxcycle=100,maxstep=10)`，`B 1 5 S 17 -0.1000`），显式调用 /home/ly/g16/g16。
- 预算记账：3（1111/1112/1115）+ 1（1120）= 4 / 16。
- 结论只作候选/上界，不入 ΔE‡。

## 6. E1 剖面实测（job 1120，已完成）

日志 `gold_fill_20261018/N_HNCO/jobs/E1scan/E1_scan_manual.log`（78554 行，sha256 8531bf8e00d810f686d88c0edd3f0cecb634b56f3a4be8496980cb8a1af55bff）；逐点表见 [`evidence/E1_profile.md`](evidence/E1_profile.md)。

- 2.900–2.000 Å 的 10 个收敛点：能量单调升至 +13.51 kcal/mol（@2.0 Å），**O5–H6 全程 0.968–0.979 Å、N3–H6 全程 3.05–3.32 Å ⇒ 无质子转移、无两性离子平台**。
- 第 11 点（C1–O5=2.000）用尽 100 个优化循环未收敛（L78375），作业以 l9999 终止（L78550），**1.90–1.40 Å 区间未测**。
- 剖面只作候选/上界，**不是 ΔE‡**。
- 预算：4 / 16（1111、1112、1115、1120）。
- 待 coordinator 裁定：A) 再批 1 个受约束短剖面（1.95→1.40）；B) 门恢复后直接做 E1 的 TS（协同/分步由虚频+IRC 判定）；C) 等门恢复再做 B。
