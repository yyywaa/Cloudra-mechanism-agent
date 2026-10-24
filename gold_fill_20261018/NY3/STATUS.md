# NY3 补算 · 交接状态（gold_fill_20261018/NY3/STATUS.md）

交接时刻：**2026-10-18 03:36 CST**｜本会话 = 接手 NY3 三条 gold 边的新计算 lane（按主协调 03:1x 指令：**即起停止提交新作业**，在飞作业自然跑完，不 kill、不重投、不 ts_resume）
口径：Gaussian 16（`/home/ly/g16/g16`），`#p` + B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight + SCRF=(CPCM,Solvent=Water)，q=0 / m=1（Na⁺ 中性制衡，Na 不参与键变化），%nproc=8、%mem=14336MB、priority 0。**能量只在本批 G16 内相减**；无 ORCA；xTB/GFN2 数值不参与任何差值。

## 0 一句话状态
**三条边 ΔE‡ 均未取得可回填值**（无一条有「合格 TS + 双向 IRC + 两端 Opt+Freq」）。本会话共花 **3 个 QM 作业**（1081 failed、1085 failed、1087 被主协调取消），**E1 从未提交**。产物：`gold_fill_20261018/NY3/{NY3_SOURCES.md, E2_GUESS_ATTEMPT2.md, e2_guess_i1_interp_t060.xyz}`。

## 1 关键工作流发现（对下一条 lane 最有用）
- **`conformers.*.optimization = null` 可绕开 ts_0013/ts_0014 的 build 阻塞**：既有两个 E2/E3 run 的失败全部发生在 build 阶段 conformer 预优化（`conformer_optimization_failed`，job 1007/1011/1012/1016/1019/1024/1025 NStep/l9999）。本会话把端点几何直接声明为「按原样使用」，**build/map/assemble 三阶段 0 作业通过，直接进 ts_opt**。
- **reaction_center 现为 1-based 输入、0-based 存储**：E2 声明 `[[4,3],[4,6]]` → declare.json 存 `[[3,2],[3,5]]`；E3 声明 `[[9,11],[3,11]]` → 存 `[[8,10],[2,10]]`。前者是我 attempt 1 写错（`[[3,2],[3,5]]` = O3–C2/O3–O1）后更正的；模式归属判据要用更正后的键对。
- 管线 ts_opt 的 route = `opt=(TS,calcfc,noeigen)`（**无法**改成 cartesian/readfc；只能在 guess 与 reaction_center 上做文章）。

## 2 作业与证据（原生日志；未改动任何既有文件）

### 2a NY3_E2（I1→I2，甲氧基消除）—— run **ts_0021**，status **blocked / stage refine / rev 31**，result=null
| job | 内容 | 输入 | 原生日志 | sha256 | 终态与读数 |
|---|---|---|---|---|---|
| **1081** | ts_opt attempt 1（guess = E2E3/ts_e2_guess.xyz，IDPP 帧，r(C4–O3)=2.417 Å） | `ts/ts_0021/jobs/declaration_0002/ts_opt/refine.gjf`（d43d08bf034af0f48d9f7d2c2f15413797f8726d4ee0c350693f0e043dd490d8） | `ts/ts_0021/jobs/declaration_0002/ts_opt/refine.log` | d509a6c1445d68c64ca639a59c60fbfb431cf1eb1867c501a28fda1f76667165 | **failed（l103 FormBX）**：`FormBX had a problem.` L10784、`Error termination via Lnk1e in /home/ly/g16/l103.exe at Sun Oct 18 03:00:50 2026` L10785；平台记录原文原因 `Tors failed for dihedral 9-2-3-1`（同类 L10780–10783 共 4 条甲基/Na 扭转）。末 SCF **−466.987210759**（L10726）。末帧（`Input orientation` L10484）：**r(C4–O3)=3.308**、C4–O5 1.210、C4–O1 1.323、O1–H6 0.977、Na–O3 2.057、Na–O5 2.322 ⇒ **向产物侧下滑（过脊线）** |
| **1085** | ts_opt attempt 2（guess = 我构造的 I1→IDPP 线性插值 t=0.60，r(C4–O3)=2.044；见 `E2_GUESS_ATTEMPT2.md`） | `ts/ts_0021/jobs/declaration_0003/ts_opt/refine.gjf`（0938e4af6b83afaf804418adc0ba8d0ef3d3cbf69c6f3614c269ce837cc98269） | `ts/ts_0021/jobs/declaration_0003/ts_opt/refine.log` | cf84514743fd6a87de9aef85080a6e827a1bd89ff1e18f4d4cbcd6ce9cd14b6f | **failed（NStep）**：`-- Number of steps exceeded,  NStep=  42` L20435、l9999 L20669（03:13:34）。末判据 L20429–20432 **四项全 NO**（Max Force 0.019932 / RMS 0.004972 / Max Disp 0.638982 / RMS Disp 0.309201）。末 SCF **−466.993406557**（L20305）⇒ 相对 I1(−467.004843，job 985) **≈ +7.2 kcal/mol**（诊断；非驻点）。末帧（`Input orientation` L20482）：**r(C4–O3)=1.948**（从 2.044 向 I1 侧内移）、C4–O5 1.238、C4–O1 1.354、O1–H6 0.973、Na–O3 2.151、Na–O5 2.273、Na–O1 3.755 ⇒ 仍在**支-I1**（Na 桥联 O3+O5），未越过脊线 |

- 端点声明（未改动）：reactant `E2E3/i1_dft_min_ref.xyz`（b7e83585…，job 985 −467.004842485）+ `prep/i1.mol`（c4165dfc…）；product `E2E3/i2_min_candA.xyz`（1715f6d7…，job 990 −466.986020418，固定几何 0 虚频）+ `prep/build/art_I2_src/assembly/complex_candidate_000.mol`（af67740f…，含键块，**必须用它**：`prep/i2.mol` 无键块会让 build 报 `endpoint_identity_mismatch`）。
- **缺什么**：合格 TS（恰 1 虚频且模以 C4–O3 为主）＋ freq（从未跑到）＋ 双向 IRC ＋ 两端 Opt+Freq。两次 ts_opt 失败均为**技术性失败**，**不构成「E2 无鞍点」证据**。

### 2b NY3_E3（I2→P，甲酸→甲氧基质子转移）—— run **ts_0023**，status **blocked（job 1087 cancelled）/ stage refine / rev 11**，result=null
| job | 内容 | 输入 | 原生日志 |
|---|---|---|---|
| **1087**（已 cancelled） | ts_opt attempt 1（guess = E2E3/ts_e3_guess_v2.xyz，3ccf834e…；O1–H6 1.536 / O3–H6 1.409 / O1···O3 2.808） | `ts/ts_0023/jobs/declaration_0001/ts_opt/refine.gjf`（fe174dc011b63144ec1c5109b18c7b8aac55a72e5874ed5975fa88d3b5cad956） | `ts/ts_0023/jobs/declaration_0001/ts_opt/refine.log`（**在飞，03:35 时 16 次 SCF，未终态**） |
- **终态 = cancelled（由主协调 D23/D32 撤销，原因原文 "free 8c/14336MB so HL1_E1 IRC (1099) can start"），第 22 步中止 ⇒ 技术性中止，不是科学结果，也不构成「E3 无鞍点」证据。** 原生日志 `ts/ts_0023/jobs/declaration_0001/ts_opt/refine.log`（sha256 **d975ed0eb02afa66d70560929db22fea52a3ea1982a5cddcee44df2fcbdb9108**，11762 行、22 次 SCF、无 `Optimization completed`/`Error termination` 行）。末 SCF **−467.027212892**（L11660）⇒ 相对 I2(−466.986020) **−25.9**、相对 P(−467.045938) **+11.8 kcal/mol**（诊断值，非驻点）。末帧（`Input orientation` L11364）：**O1–H6 1.113 / O3–H6 1.368 / O1···O3 2.480**、C4–O3 3.149、C4=O5 1.247、C4–O1 1.268、Na–O3 2.171、Na–O5 2.288 ⇒ 质子确实夹在 O1/O3 之间（短氢键 2.48 Å），但能量仍在向 P 侧下降、`SLEqS3` 迭代剧烈振荡，**未见任何驻点**。
- 端点声明：reactant `E2E3/i2_min_candA.xyz` + `complex_candidate_000.mol`；product `E2E3/p_min_ref_pmol_order.xyz`（bca75d0a…，job 994 −467.045937735，0 虚频）+ `prep/p.mol`（165702ab…）。
- **缺什么**：合格 TS（1087 被撤销，从未到 `Stationary point found`）＋ freq（虚频数与模归属，应为 O1–H6/O3–H6 对）＋ 双向 IRC ＋ 两端 Opt+Freq。E3 的可用线索只有「质子夹在 O1/O3 之间（O1···O3 ≈2.48–2.51 Å）时能量比 P 高 ≈+11.8 kcal/mol」这一**非驻点诊断**，不可当 ΔE‡。

### 2c NY3_E1（RC→I1，OH⁻ 加成 + Na⁺ 换支）—— **未提交任何作业**
- 本会话**没有**为 E1 建 run（时间/预算原因）；E1 的既有失败链仍以 `gold_finish_20261015/NY3/STATUS.md` §19/§33.2/§38/§39 为准（job 1004→1010 甲基转子 −98.2487 cm⁻¹/99.49%、job 1027 羟基 H 扭转 −134.4181 cm⁻¹/98.87%、job 1034 NStep=45 退回 2.383 Å）。
- 关键结构事实（既有证据，我未复算）：RC 属**支-RC**（Na 桥联羟基 O1 + 羰基 O5，Na–O3 4.26 远端），登记的 I1 属**支-I1**（Na 桥联甲氧基 O3 + 酯氧 O5）⇒ 声明的单步 RC→I1 在 Na⁺ 模型里**必然耦合一次 Na⁺ 迁移**（job 1023 正/反扫描换支，p5=2.027 Å 支-I1 约束极大 +10.756 vs RC）。这解释了为何从 RC 侧内插的 guess（2.177/2.127 Å）都退回。

## 3 建议下一步（给接手 lane）
1. **E3 优先（需重跑）**：1087 已被撤销，需以同一 guess（ts_e3_guess_v2，或把 guess 放在 O1···O3≈2.5 Å、H 居中的构造上）重新 ts_prepare/ts_resume ⇒ 读 freq（判 1 虚频 + 模归属），IRC 双向；注意**登记参考态可能变**：本 run 的 guess 在 O1···O3 2.81 Å 的构象，而登记的 I2 极小值（job 990）O3···O9=4.19 Å 是另一构象 ⇒ IRC 反应物端优化出的极小值若与 job 990 不同，必须整批重算并显式登记，**新旧值不得混减**。
2. **E2 找脊线**：现有两点界定了区间——r(C4–O3)=1.948 时仍 +7.2 kcal（支-I1，上升）、r=2.417 时向产物侧下滑 ⇒ 鞍点大概率在 **r(C4–O3) ≈ 2.05–2.35 Å**。建议先做一次**同批 DFT 受约束弛豫扫描**（`opt=modredundant`，`B 4 3 S 8 -0.05`，1.55→2.55 Å，普通作业、非 TS）定出真实剖面，取最高已收敛帧作 guess；或直接把 guess 放在 2.20 Å 并同时固定 Na–O3/O5 距离。**扫描峰只作候选/上界**。
3. **E1 若要做**：单步 TS 很可能不存在（Na⁺ 两支），建议要么 (a) 2D 搜索（r(O1–C4) × Na⁺ 归属），要么 (b) 把 E1 拆成「加成（RC→I1′，Na 仍在 O1 侧）+ Na⁺ 重排（I1′→I1）」并在 registry 层登记为两步；不要再用 2.1–2.5 Å 的单一插值 guess 反复试。
4. 三条边都**不得**用扫描峰、xTB 值或历史 ORCA 值充当 ΔE‡。

## 4 交接纪律
- 未改动任何题源/registry/json/md；未触碰他人 run 与 job 1074；未 kill、未改 priority、未重投。
- 本会话作业计数：**1081 / 1085 / 1087 = 3 个 QM 作业**（上限 12，已停）；其中 1087 由主协调 D23/D32 撤销（腾 8c 给 HL1_E1 IRC 1099），非我 kill、非科学结论。
