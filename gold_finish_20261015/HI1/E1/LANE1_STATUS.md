# HI1_E1 / lane1 — STATUS（本段：合并边 single-TS 推进；仅维护本段）

道：lane1（as_fc7fdbb5e5564d93）。目标：合并边（enamine condensation merged edge）≡ ts_0004 → 新 run ts_0008。
纪律：Gaussian 16 /home/ly/g16/g16，B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight + SCRF=(CPCM,Solvent=DMSO)，q0/m1；能量只在本批 Gaussian 原生日志内相减（绝不与历史 ORCA 值混减）。

## 0 一句话现状（PROVISIONAL / 未达交付）
ts_0004 原 owner 会话失败导致 ts_resume 被平台拒（owner 绑定缺陷），已按先例用 ts_prepare 重建为 **ts_0008**（同一科学声明、同一 g16 profile）。ts_0008 现已绑定本 lane 的 RC 极小值几何 + provided 合并 TS 初猜，candidate_opt 已排队（job 968）。尚无任何 TS/IRC 数值 → **无 ΔE‡**。

## 1 权威状态复核（工具读，非 process.json 猜测）
- `ts_inspect(run_id="ts_0004")`：revision 8 / status=blocked / stage=build / blocked.failure_class=conformer_optimization_failed / needs=[conformers.reactant] / failed_attempt=1:candidate_opt:928。
  - 失败原生日志：/home/ly/Cloudra-mechanism-agent/ts/ts_0004/jobs/declaration_0001/candidate_opt/seed-opt.log（sha256 e3286543d054fd48cab499cea8bca605156f0e7ff318253b4c21d19c393c7694）
  - 根因（非化学）：平台自动 ETKDGv3 种子原子重叠 H35–H36 = 0.299 A → Gaussian l202 Error termination（Small interatomic distances encountered: 36 35）。
- 注意：run_id 令牌是 `ts_0004`（不是 `ts/ts_0004`）；`ts/ts_0004` 会回 "TS run not found in the authorized project and workspace"（call_id tc_51cbc0e7cff24e09，只读失败，无副作用）。

## 2 ts_resume 被拒（逐字记录，作为平台缺陷证据）
- 调用：ts_resume(run_id="ts_0004", changes={conformers.reactant=file RC_S_canonical, guess=provided TS_guess_merged_canonical, reaction.reaction_center=7 对})
- 返回：is_success=false，**原始消息逐字**：`ts_resume: TS process belongs to a different project or owner`
- call_id = **tc_f284ae99aa9243d1**（该 run 的 owner 会话 as_84bdf87a0f94416c 已在平台重启中 failed；与主协调通报的 owner 绑定缺陷第二次复现同源）
- 处置：不修平台、不动 ts_0004（保留其失败证据），按先例新建 run。

## 3 新 run 登记：ts_0008（durable，同科学声明）
- ts_prepare call_id = tc_cb41ccb084734cd9；返回 run_id=**ts_0008**，run_dir=/home/ly/Cloudra-mechanism-agent/ts/ts_0008，创建时 revision=5，status=waiting，stage=build。
- 声明文件（我提交后由管线落盘）：/home/ly/Cloudra-mechanism-agent/ts/ts_0008/declare.json
  - reaction.reactant_smiles / product_smiles = **逐字复制 ts/ts_0004/declare.json 的 reaction 段**（未改一字；无 atom_map，reaction_center 见下）。
  - calculations.g16 = {gaussian, b3lyp, def2svp, "empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=dmso)"}；ts_optimization/frequency/irc/reactant_endpoint/product_endpoint 全部 {ref: g16}。
  - conformers.reactant = file：xyz=/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/lane1/RC_S_canonical.xyz（sha256 71b23e07b73a7241e19c3c94e927040f5f113f815184bfa44387d58bbc0e6597），mol=同目录 RC_S_canonical.mol（sha256 cbdb052b5e49b7ac3872df703b7b4e6e7ee1ade61d6cfad0232986fb56c2459c），optimization={ref:g16}，heavy_atom_binding.indices=[1,2,3,4,11,12,13,14,15,16,17,18,25,26,27,28,29,30,31,32]。
  - guess = provided：xyz=/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/lane1/TS_guess_merged_canonical.xyz（sha256 a2c0fa28667eb5afd814d8b876f40dd5873967c8a63973ff89bf9b0d0b980c4c）。
  - evidence_refs（两处）= /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/TS_GUESS_PROVENANCE.md（sha256 d7a82f39e7d068400a0da60d4b59b7679c66441fd13cf885bb25f909f37a3276）。
  - execution = 8 cpus / 8192 MB（管线作业不占手工配额）。
- 绑定核验（ts_inspect(ts_0008) 读回）：seed.xyz sha256 = 71b23e07…（与我给的 RC_S_canonical.xyz **逐字节相同**），seed.mol sha256 = cbdb052b…；41 原子 / 3 组分，原子序 C,C,O,C,H×6,O,C×7,H×6,O,C,O,C×4,N,H×9，与 ts_0004 canonical 序一致 → **本次文件未被重排**（source_to_canonical=identity）。
- 当前作业：job 968 = /home/ly/Cloudra-mechanism-agent/ts/ts_0008/jobs/declaration_0001/candidate_opt/seed-opt.gjf（log 同名 .log）。**已于 23:41 起跑**：23:44 实测日志 223 KB 且在增长，route 单行完整（`#p opt b3lyp/def2svp empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=dmso)`，GD3BJ 未被折行拆断），输入几何段 = RC_S_canonical.xyz 逐字相同（原子序与坐标一致）。注意 candidate_opt 是**纯 opt（无 freq）**，与 §6 那个 “opt freq 中间 Normal termination” 坑不同。

## 4 索引约定（已核验，避免把“-1”误当错）
- **输入契约是 1-based；run 落盘的 declare.json / process.json 记录为 0-based**（run 内部 atom_table.json 也是 0-indexed）。
  交叉证据：ts/ts_0006/declare.json 记录 reaction_center=[[0,5]]（1

[Full output at .cloudra/tool_output/read-20261017-103628-307096f9.log; page with `read` `offset`/`limit`. 30462 chars total, showing first 4000.]

## 18 2026-10-17 10:4x — 索引序对照表（built 序 ↔ **原始序** ↔ 题源 map 号 ↔ 化学标签）

### 18.1 「原始序」定义与来源（含 sha256）
- **定义**：job 907（(S)-RC Opt+Freq）**实际运行时的输入原子序**，即
  - /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/runs/RC_optfreq/RC_optfreq.gjf，sha256 **81b083aff4fcfb18166b7060c1983b38e028dc2adc193a1d1851903ad29ee835**（首几何 = 上游 build 的 RC_start.xyz，sha256 **f4eb0ba6f085114c97cb13bcdbe03a8613a2f95262782bcb5fb9da5c6d9b93c0**，即 job_51 序）。
  - **已验证**：该 log 的 `Input orientation` 首块与 .gjf 输入几何逐坐标完全一致（max|Δ| = 0.0，元素序相同）⇒ 读 log 时用 `Input orientation` 块即为原始序。
- **built 序**（ts_0008 绑定序）= `RC_S_canonical.xyz` sha256 **71b23e07b73a7241e19c3c94e927040f5f113f815184bfa44387d58bbc0e6597** = `jobs/declaration_0002/candidate_opt/optimized_seed.xyz` sha256 **69469643ad970550bd8ce80ce5f71257a68e262207dfb9b7698652ea143b751c**。
- **换算实测**（脚本 gold_finish_20261015/HI1/E1/check_order_vs_job907.py，sha256 5a78996acfd7c4f98f0845119799c52ec8f5ca048d4330321a78af82d07b21f6）：用**优化前同一几何**的两份文件（RC_start.xyz/job907 输入 ↔ RC_S_canonical.xyz）做元素+坐标逐原子匹配，**41/41 唯一匹配、max|Δ| ≤ 1e-6 Å、双射**，得置换：
```
built 1..41 -> 原始序 1..41
[3, 2, 25, 1, 14, 15, 16, 12, 13, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 10, 9, 11, 8, 7, 6, 5, 4, 24, 23, 21, 22, 19, 20, 17, 18, 26]
```
- **一行结论：job 907 日志原子序与 built 序不一致**（是上表置换，非恒等）；已做元素序 + 坐标逐原子比对（41/41）。

### 18.2 声明 7 对的对照表（built 序 1-based / 原始序 1-based / 题源 map 号 / 化学标签）
| built 1-based | 原始序 1-based | 题源 map 号 | 化学标签 |
|---|---|---|---|
| 2 | 2 | 2 | C2（丙酮羰基 C） |
| 3 | 25 | 4 | O4（丙酮羰基 O → 成水） |
| 4 | 1 | 3 | C3（丙酮甲基 C → 成 =CH2） |
| 10 | 27 | 22 | H22（甲基 H，迁到 O4） |
| 32 | 4 | 20 | N20（脯氨酸 N） |
| 41 | 26 | 21 | H21（N–H 质子，迁到 O4） |

成对写法（built ↔ 原始序 ↔ map ↔ 标签）：
- **(2,3)** ↔ **(2,25)** ↔ (2,4) ↔ C2–O4（A 步断 π；B 步断 σ）
- **(2,4)** ↔ **(2,1)** ↔ (2,3) ↔ C2–C3（B 步成 π）
- **(4,10)** ↔ **(1,27)** ↔ (3,22) ↔ C3–H22（B 步断 σ）
- **(32,41)** ↔ **(4,26)** ↔ (20,21) ↔ N20–H21（A 步断）
- **(2,32)** ↔ **(2,4)** ↔ (2,20) ↔ C2–N20（A 步成）
- **(3,41)** ↔ **(25,26)** ↔ (4,21) ↔ O4–H21（A 步成）
- **(3,10)** ↔ **(25,27)** ↔ (4,22) ↔ O4–H22（B 步成）

注：product built 序另有一套（见 §14.2 atom_map：product C2=2、C3=1、N20=4、O4=25、H21=26、H22=27），三套序（原始/built reactant/product）**不可混用**。

## 19 2026-10-17 10:4x — job 1017 截断前最后读数（按主协调 11:20 CST 截断口径；**未提交作业**）

- refine.log sha256 **455753138d32f3a209f7aca5a9e9cec2bbca601e9d574adae88684479a2582d5**（10:36 CST 快照）
- **L77500** ` Step number  78 out of a maximum of  246`；末次 SCF **L78379** ` SCF Done:  E(RB3LYP) =  -939.237012718     A.U. after   12 cycles`
- 四项判据全 NO：**L77790** ` Maximum Force            0.005242     0.000450     NO`；**L77791** ` RMS     Force            0.000768     0.000300     NO`；**L77792** ` Maximum Displacement     0.467907     0.001800     NO`；**L77793** ` RMS     Displacement     0.155942     0.001200     NO`
- 末帧（`Input orientation` 块 **L77799**，声明/built 序）：C2–O4 **1.358**、C3–H22 **1.093（未断）**、N20–H21 **1.219**、C2–C3 1.533、C2···N20 **1.652**、O4···H21 **1.338**、O4···H22 **2.721（远离）**
- 能量口径（**仅"高能脊"读数，不是 ΔE‡**）：E − job 907 = −939.237012718 + 939.308829219 = **+0.0718165 Eh = +45.06 kcal/mol**；E − job 924 = **+0.0712055 Eh = +44.68 kcal/mol**
- 无 `Normal termination`/`Error termination`/`l9999` 行 ⇒ 截断时仍在 running，**无终态可登记**。

### 19.1 本边终局判定（E1）
- **E1 的 ΔE‡ = 缺测（不填数）**：未取得任何「1 虚频 + 虚频模落在声明键对上」的 TS 证据。
- **已证伪**：合并 7 对的 provided 初猜**不走向 7 对单鞍点**（H22 始终留在甲基 C3–H22 1.09–1.10 Å；O4···H22 由 guess 的 1.713 Å 反被拉大到 2.52–2.72 Å；C2–O4 由 1.550 缩短到 1.358 Å；仅 C2···N20 1.652 + O4···H21 1.34 两项在推进）⇒ 该初猜只能作为**步 A** 的 guess 素材。
- **缺什么（明确）**：① INT1(carbinolamine) 的同批 Opt+Freq「未取得，不得作为分母」；② 步 A / 步 B 各自的 TS（1 虚频 + watch-pair 投影）；③ 双向连通性（IRC 或替代口径）；④ ΔE‡_A / ΔE‡_B。
- **可交付的替代结构**：§15 的两步拆解（reaction_center 双套索引）+ §18 的三套索引对照表 + §16/§17 的 INT1 候选帧（未验证极小值）。

## 20 2026-10-17 11:48 — job 1017 截断后追记（**仅供参考；按主协调 11:20 硬时线，E1 判定与 ΔE‡ 不变**）

- refine.log sha256 **b80fbead209f39a169f33661d78561cd5ada11e98c5131d482b50156446378d0**（11:48:20 CST 快照）
- **L115578** ` Step number 118 out of a maximum of  246`；末次 SCF **L115491** ` SCF Done:  E(RB3LYP) =  -939.242130998     A.U. after   14 cycles`
- 四项判据仍全 NO：**L115862–L115865**（Max Force 0.005168、RMS Force 0.000964、Max Disp 0.213546、RMS Disp 0.056781）
- 无 `Normal termination`/`Error termination`/`l9999`/`Number of steps exceeded` 行 ⇒ 11:48 仍在 running（管线 ts_inspect：revision=29 / status="waiting" / stage="refine" / result=null）
- 能量（**仅高能脊读数，不是 ΔE‡**）：E − job 907 = −939.242130998 + 939.308829219 = **+0.0666982 Eh = +41.86 kcal/mol**（E − job 924 = +41.28 kcal/mol）
- 判读不变：仍在「C–N 成键 + H21 迁移」的两性离子 carbinolamine 高能脊上，H22 未参与（C3–H22 仍 ~1.09 Å），与 §15.4/§19 一致 ⇒ **合并 7 对单鞍点仍为已证伪**；E1 的 ΔE‡ 保持缺测，分母锁 job 907。
- 追记纪律：11:20 CST 后主协调不再收新读数，本节仅作本 lane 台账，不改变终态包；不补作业、不 ts_resume、不改图。

## 21 2026-10-17 13:11 — ★ job 1017 (ts_opt) **收敛为驻点**，管线自动起 frequency (job 1042)

（此段为**新证据**，晚于主协调 11:20 截断；E1 的历史判定包（§19）不推翻，但其「合并 7 对无单鞍点」结论现在有了更精确的形态：收敛到的驻点只覆盖 7 对中的 **4 对（步 A）**。）

### 21.1 job 1017 终态证据
- refine.log sha256 **0e726b3287df2413b256312bdba1bd6f1bb73c2f5c106e4c4dd2b0960c693b0b**（13:11:06 CST 快照）
- **L159450** ` Step number 165 out of a maximum of  246`
- **L159362** ` SCF Done:  E(RB3LYP) =  -939.242869284     A.U. after    6 cycles`（末次 SCF）
- **L159743** ` Optimization completed.`；**L159744** `    -- Stationary point found.`；**L160800** ` (Enter /home/ly/g16/l9999.exe)`；**L160850** ` Normal termination of Gaussian 16 at Sat Oct 17 13:09:41 2026.`
- 作业统计（日志尾）：` Job cpu time:       1 days 11 hours  2 minutes 35.9 seconds.` / ` Elapsed time:       0 days  4 hours 26 minutes 34.0 seconds.`

### 21.2 收敛驻点的几何/能量（末帧 `Input orientation` 块 **L159994**，built 序）
- 7 对：C2–O4 **1.362**、**C3–H22 1.097（未断）**、N20–H21 **1.226**、C2–C3 1.531、**C2···N20 1.633**、**O4···H21 1.334**、O4···H22 **2.632（未成键）**
- 键级感知：C15H21NO4，**2 分片** = 27 原子**两性离子 carbinolamine**（`[N@+]1([H])C([O-])(CH3)2`，C2–N20 已成键、C2–O4 仍存在）+ 14 原子苯甲醛（旁观）
- CIP：**(28,'C','S') 与 (32,'N','S')** —— 该驻点上 **N20 成为新立体中心**（三种不同取代 + H）
- 能量：E(−939.242869284) − job 907(−939.308829219) = **+0.065960 Eh = +41.39 kcal/mol**；相对 job 924 = +41.01 kcal/mol
- **判读（诚实标注）**：该驻点只推进了声明 7 对中的 **form (2,32) C2–N20 + (3,41) O4–H21 / break (2,3) C2=O4 π + (32,41) N20–H21** 四项，即**步 A（RC→carbinolamine）的 TS 候选**；**C3–H22 未迁移、C2=C3 未形成** ⇒ **它不是合并 7 对单鞍点**。

### 21.3 管线状态与下一步（只读）
- ts_inspect("ts_0008")：**revision=33 / status="waiting" / stage="refine" / blocked=null / result=null**；waiting_for=[job **1042**, purpose=**frequency**, state=running, input=`ts/ts_0008/jobs/declaration_0003/frequency/frequency.gjf`]，该 gjf 输入几何 = ts_opt 导出的 `frequency/optimized.xyz`（sha 见下）。
- 频率作业日志：`ts/ts_0008/jobs/declaration_0003/frequency/frequency.log`（13:11 时 51 KB，运行中）。
- 判定门禁（不变）：**虚频只看 band 表 + `imaginary` 行**；若恰 1 虚频且位移以 (2,32)/(3,41)/(2,3)/(32,41) 为主 ⇒ 这是**步 A 的合格单鞍点**（Ea = +41.39 kcal/mol 电子能，分母 job 907），可在报告里作为「步 A 能垒」给出，但**绝不是合并边的 ΔE‡**；若虚频数 ≥2 或模落在声明对之外 ⇒ pseudo-saddle，仍不填数。

## 22 2026-10-17 13:24 — ★★ frequency job 1042 结果：**恰 1 虚频 −1547.0708 cm⁻¹**，但虚频模 = 纯质子转移（H21），非合并 7 对模

### 22.1 收敛驻点的单鞍点证据（frequency，job 1042）
- 日志：/home/ly/Cloudra-mechanism-agent/ts/ts_0008/jobs/declaration_0003/frequency/frequency.log，sha256 **a5783c38955a630e1b0b8e90a50a51d9953156de219cdd11fa741b6624f11cbc**
- **L1507**：` ******    1 imaginary frequencies (negative Signs) ****** ` ⇒ **恰 1 个虚频**
- **L1516**：` Frequencies --  -1547.0708                15.9682                22.9832`（band 表首行；最低实频 **15.9682** cm⁻¹）
- **L1505**：` Low frequencies ----1547.0708   -0.0007   -0.0006    0.0008    1.4934    7.3878`；**L1506**：` Low frequencies ---   11.5090   17.2663   23.6387`（行首 −1547.0708 即该虚模在 Low-frequencies 行的呈现；其余为平动/转动伪模）
- 模数：39 组 `Frequencies --` × 3 = **117 模**（41 原子，全解析频率）；末带 **L3340** ` Frequencies --   3206.1122              3213.9312              3720.7784`
- 能量（freq 段同几何）：**L819** ` SCF Done:  E(RB3LYP) =  -939.242869284     A.U. after   13 cycles`
- 终止：**L5306** ` Normal termination of Gaussian 16 at Sat Oct 17 13:23:42 2026.`

### 22.2 虚频模归属（两法独立一致）
- log_parser(watch_pairs=7 对)：`imaginary_modes[0] = {frequency_cm: -1547.0708, heavy_atom_fraction: 0.006630, watch_pair_fraction: {fraction: 0.0789, pair_projections: {"3-41": 0.9320, "32-41": 0.7949, "2-3": 0.0735, "2-32": 0.0455, "3-10": 0.0138, "2-4": 0.0119, "4-10": 0.0016}}, top_displaced_pairs: [[3,41,0.932],[34,41,0.926],[36,41,0.900],[38,41,0.880],[28,41,0.840]]}`
- 我的独立解析（eigenvector 块 **L1520** `Atom  AN  X Y Z ...`，脚本 gold_finish_20261015/HI1/E1/parse_imag_mode.py sha256 **0d1250be5acabe56b6f97b17b7a28984eee3c3339c5b1a03de3b1484b9042b60**）：
  - Σ|d| = 1.2513（归一化）；**原子 41 (H21) 占 79.4%**；全 H 占 **86.7%**；重原子几乎不动
  - 逐对归一化 |d_a|+|d_b|：**(3,41) O4···H21 = 0.827**、**(32,41) N20–H21 = 0.802**、(2,3) 0.084、(2,32) 0.059、(2,4) 0.059、(3,10) 0.033、**(4,10) C3–H22 = 0.008**
- ⇒ **虚频模 = N20–H21 → O4 的质子转移（H21 主导）**，落在**声明对 (32,41)/(3,41)** 上；**与 C3–H22 迁移、C2=C3 形成无关**（H22 相关对 0.008–0.033）。

### 22.3 驻点几何（ts_opt 末帧 `Input orientation` **L159994** in refine.log，built 序）
- C2–O4 **1.362**、**C3–H22 1.097（完整）**、N20–H21 **1.226**、O4···H21 **1.334**、C2–C3 1.531、C2···N20 **1.633**、O4···H22 2.632
- 2 分片 = 27 原子**两性离子 carbinolamine**（C2–N20 已成键）+ 14 原子苯甲醛；CIP：**Cα(28)=S、N20(32)=S**（N20 成为新立体中心）

### 22.4 判定（诚实口径）
- **恰 1 虚频 ✓**，且虚频模确实落在声明键对上 ✓ —— 但只覆盖 7 对中的**质子转移子集 (32,41)/(3,41)**；
- **⇒ 对「合并 7 对单鞍点」的结论不变：无合格单鞍点**（该模不含 C3–H22 迁移 / C2=C3 形成，phy 上不可能一步连通 RC→I1）；
- **但这是一个真实的、可测量的一阶鞍点**，属于**步 A（RC → carbinolamine 方向的质子转移）**，可给出**步 A 能垒（纯电子能，同批）**：
  ΔE_A = E(TS) − E(job 907) = (−939.242869284) − (−939.308829219) = **+0.065959935 Eh × 627.509474 = +41.39 kcal/mol**
  （相对 job 924 = **+41.01 kcal/mol**）
- 仍未取得：IRC 双向连通性（该鞍点是否真正连接 RC 与 INT1）；INT1 自身的 Opt+Freq（0 虚频）⇒ 步 A 的完整闭环仍缺两项。

### 22.5 管线状态（13:24）
- ts_inspect("ts_0008")：**revision=34 / status="waiting" / stage="refine" / blocked=null / result=null**；available_results 已含 ts_opt(job 1017, done)、frequency(job 1042, done)；当前**无 running/ready 作业**，next.action="wait_for_system"。
- 若管线自动进入 IRC，我会只读跟踪并记录两方向端点；不再提交任何作业。

## 23 2026-10-17 13:3x — 协议：本道转静默，后续读数只落本节（§23.x）

主协调 13:3x 指示（要点，逐条照办）：
1) 已复核我的 job 1042 读数（frequency.log sha **a5783c38…**：L1507 1 imaginary、L1516 **−1547.0708 cm⁻¹**、39 块=117 模、L819 E=−939.242869284、L5306 Normal termination 13:23:42；模 = H21 主导 79.4%，(3,41) 0.827 / (32,41) 0.802，H22 仅 0.008），并分两点入档：
   - (a) **合并 7 对单鞍点仍无合格候选 ⇒ E1 合并边 ΔE‡ 保持缺测、不回填**；
   - (b) **步 A 取得真实一阶鞍点，ΔE_A = +41.39 kcal/mol（分母 job 907）**，但缺 IRC 双向连通性与 INT1 自身 Opt+Freq（0 虚频）⇒ **步 A 闭环不完整，不得作任何边的 ΔE‡**。
2) 本轮交付已于 **11:20 CST 冻结**（报告 ca060122…；hi.py / HI1.json / hard.md / tests 零改动；E1 记为 result=null/缺测）。**13:0x 之后的读数属窗口外补录**：不进正文、不回填、不参与任何能垒申报。
3) **回报节奏**：ts_0008 后续（如自动 IRC）的中间读数**只写本文件 §23.x**，不再逐条贴主题帖；仅在
   ① 步 A 完整闭环齐备（freq 通过 + IRC 双向到 RC 与 INT1 + INT1 Opt+Freq 0 虚频）可作新轮次候选交付，或
   ② 非预期技术性失败（原始报错 + call_id）时，才主动联系主协调。
4) **纪律**：不提交手工作业、不 ts_resume、不改图、不动交付面四文件；**该 −1547 cm⁻¹ 鞍点属步 A，任何情况下不得写成合并边（7 对）的 TS 或 ΔE‡**。

### 23.1 待观察（只读，不设主题帖）
- ts_0008（revision=34 / status="waiting" / stage="refine" / result=null）当前无 running/ready 作业；已设一次定时只读复核（约 13:50 CST）。
- 复核时若出现 IRC 阶段：记录两方向端点区间证据（是否到 RC：3 组分、C2=O4≈1.22 Å、N20–H21≈1.02 Å；是否到 INT1/carbinolamine：C2–N20 成键、O4–H21 成键、C3–H22 完整），IRC 失败原文照录（失败 ≠ 无鞍点）。
- 若管线给出 result.outcome（verified / candidate_only / search_failed）：原样抄入本节，**不贴主题帖**（除上述 ①② 情形）。

### 23.2 2026-10-17 13:48 定时复核（台账一行，按 §23 不贴主题帖）
- ts_inspect("ts_0008")：**revision=34 / status="waiting" / stage="refine" / blocked=null / result=null**；waiting_for 全部 state=done（968/991/1009/1017/1042）；available_results 至 `frequency(job 1042, done)` 为止；next.action="wait_for_system"。
- 目录核对：`ts/ts_0008/jobs/declaration_0003/` 下**只有 ts_opt 与 frequency 两个阶段目录**，**未出现 IRC 阶段**；无 running/ready 作业。
- 结论：**无新阶段**。管线在 frequency 之后处于空闲（未自动发起 IRC），因此步 A 的「双向连通性」仍缺；按规定本道监测到此结束，**不再设新提醒**、不贴主题帖、不补作业。
- 若日后有新的授权动作（IRC 或 INT1 Opt+Freq），需要的新证据口径已写在 §23.1；**−1547 cm⁻¹ 鞍点恒属步 A，绝不可写成合并边 7 对的 TS/ΔE‡**。

## 24 2026-10-17 14:0x — 新授权：HI1 拆步 + 27/14 原子多组分模型（E1a / E1b），已起第 1、2 步作业

### 24.1 授权与算力（主协调 as_ec848a7673b74e35，用户 13:5x 点头）
- 全局在飞 ≤4 g16、单作业 ≤8c/≤10240MB、priority 0；HI1 ≤3 并行。**每阶段完成即 call 写权会话**（分母出 freq / TS 出 freq / IRC 出结果 / 失败）。
- route 逐字：G16 /home/ly/g16/g16，B3LYP/**def2SVP**（无连字符）+ EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight + CPCM(DMSO)，q0 m1。
- 模型变更：苯甲醛（C7H6O，14 原子）为**旁观组分**，拆出单独 Opt+Freq 留证，**不进任何分母、不参与键变化**；反应性子体系 = 脯氨酸 + 丙酮 = **27 原子 C8H15NO3**。

### 24.2 模型条件与已知未知（先声明，再算）
- **显式条件**：仅 CPCM(DMSO) 连续介质；**无显式溶剂分子、无抗衡离子、无外加碱/酸催化剂的质子穿梭体**；温度/浓度未建模；报告量一律为**纯电子能差**（不含 ZPE/热校正）。
- **模型省略了什么**：41 原子模型里苯甲醛距反应中心约 2.6–3.7 Å，可能提供 H 键/弱穿梭；27 原子模型把它去掉后，两性离子 carbinolamine 的稳定化只靠连续介质 ⇒ 41 原子模型测得的 +41.39 kcal/mol 质子转移鞍点可能被「缺少质子受体」人为抬高。**可检验假设**：脯氨酸自身 COOH（built 25/27 = =O/–OH）可作为分子内质子穿梭，使 E1a 出现更低鞍点或分步（近攻→两性离子→质子转移）路径。
- **预组织**：删掉苯甲醛后 proline/acetone 两片段可能漂移；RC_27 极小值的 C2···N20 距离与是否仍为「接触复合物」必须记录，否则 ΔE_A 的分母含义（松散复合物 vs 接触对）不清。
- **未知**：① INT1_27（两性离子）在本级别是否为极小值；② E1b 产物（iminium + H2O）在 27 原子模型内是否可达；③ 隐式介质能否稳定 N⁺/O⁻。

### 24.3 结构（脚本生成 + RDKit 核验；脚本 E1/split_build.py sha256 0a6b12bbf87f5dc941735f881e6fba5e044e76946a061a1b5650d94180972c34）
| 文件 | 原子 | 公式 | 组成（RDKit 键级感知） | sha256 |
|---|---|---|---|---|
| E1/split/RC_27_start.xyz | 27 | C8H15NO3 | 2 片段 = 丙酮 + (S)-脯氨酸 | eb193d5f02a75b42d3dc449e50e389f11736737fb01ba2fdcd9e24eaff25c7c4 |
| E1/split/BZA_14_start.xyz | 14 | C7H6O | 1 片段 = 苯甲醛（旁观） | 0234f6f9142587b6d7f8125adb7d56780542a8c529716021563b5382b600f761 |
| E1/split/INT1_27_start.xyz | 27 | C8H15NO3 | 1 片段 = 两性离子 carbinolamine（[N@+]–C([O-])(CH3)2） | 3c48099cf8e77f2bad7a5379901a23ab68503bdedc620955ae18f1ce0ad91a40 |
- 来源：RC_27/BZA_14 取自 run 的 built reactant `ts/ts_0008/jobs/declaration_0002/candidate_opt/optimized_seed.xyz`（原子 11–24 = 苯甲醛）；INT1_27 取自 `ts/ts_0008/jobs/declaration_0003/ts_opt/refine.log` 末帧 `Input orientation`（L159994）同一剖分。**旧 41 原子能量只作身份/方向对照，绝不作新边分母。**

### 24.4 已提交作业（E1a 分母 + 旁观身份）
| job | 输入 | sha256(.gjf) | 类型 | 资源 |
|---|---|---|---|---|
| **1044** | E1/split/RC_27_optfreq.gjf | 7fb6f67f8c96fb0d1ee9d828c14dd45f8936f62398cc53ed7bc9819bcf25819f | opt freq（B3LYP/def2SVP+GD3BJ+UltraFine+Tight+CPCM(DMSO)，q0 m1） | 8c / 10240MB / prio 0 |
| **1045** | E1/split/BZA_14_optfreq.gjf | 8fa424207a120717a9094c268ad24bfd64fe8db172165c59c2e3107c9b0956a3 | opt freq（同上） | 8c / 10240MB / prio 0 |
- 终态通知会推给本会话（job 由我提交）；出结果后按 §23 口径先落本文件，再按授权 call 写权会话。

### 24.5 后续（授权顺序）
3) RC_27 收敛后 → 提交 **INT1_27 Opt+Freq**（E1b 分母 + E1a 产物端）；4) E1a 的 ts_prepare（guess 可用 job 1017 的 27 原子帧/job 1042 鞍点帧，provenance 先落盘）；5) E1b 的 ts_prepare（独立 run）。

## 25 2026-10-17 14:1x — 交写 hi.py 用的字符串（carbinolamine 节点 + 两条边 out + reaction_center 双写）

### 25.1 映射 SMILES（题面 1-based map 标签，dot-joined complex，显式写参与键变的 H）
**N_CARB（carbinolamine，E1a 产物 / E1b 起点；含苯甲醛旁观组分）**
```
[CH3:1][C:2]([CH2:3]([H:22]))([O:4]([H:21]))[N:20]1[CH2:19][CH2:18][CH2:17][C@H:16]1[C:14](=[O:13])[OH:15].[O:5]=[CH:6][c:7]1[cH:8][cH:9][cH:10][cH:11][cH:12]1
```
**E1a.out = N_CARB**（同上）
**E1b.out = I1（= 题面既有 product_smiles，逐字未改）**
```
[CH3:1][C:2](=[CH2:3])[N:20]2[CH2:19][CH2:18][CH2:17][C@H:16]2[C:14](=[O:13])[OH:15].[O:4]([H:21])([H:22]).[O:5]=[CH:6][c:7]1[cH:8][cH:9][cH:10][cH:11][cH:12]1
```
**校验（脚本 E1/validate_split_smiles.py sha256 00294cd2…、E1/diff_split_edges.py sha256 5a65060e…）**
- 三个 SMILES 都能解析、**均为 C15H21NO4、marks 1–22 全在**、显式 H 保留时原子数 22（20 重原子 + H21,H22）
- CIP：reactant **map16 = S**；N_CARB **map16 = S**；product **map16 = S**（Cα 全程保持 S）
- **注意（勿"顺手改"）**：N_CARB 里 C16 必须写 `[C@H:16]`（我这种环写法的邻接序下才等于 S）；若照抄 reactant 的 `[C@@H:16]` 会变成 **R**（RDKit 实测：@@ → R，且与 INT1_27 几何的 chiral 子结构匹配失败）。已验证 `[C@H:16]` 版本对 INT1_27_start.xyz **chirality-consistent 子结构匹配 = True**。
- N20 在该节点是**手性氮（3 取代 + 孤对，RDKit 3D 给 (32,'N','S')）**，但胺氮快速翻转 ⇒ **SMILES 不标 N 手性**（如需要请另行说明）。
- 羧基 H（map15 写作 `[OH:15]`，未给 H 单独 map 号）在 E1b 里是**穿梭质子**：两端写法相同 ⇒ 不产生 diff。

### 25.2 键变化（按 map 标签；RDKit 逐键 diff，removeHs=False 实测）
- **E1a（RC → N_CARB）**：break **(20,21) N20–H21**；form **(2,20) C2–N20**、**(4,21) O4–H21**；order change **(2,4): 2 → 1**（C2=O4 变 C2–O4）
- **E1b（N_CARB → I1）**：break **(2,4) C2–O4**、**(3,22) C3–H22**；form **(4,22) O4–H22**；order change **(2,3): 1 → 2**（C2–C3 变 C2=C3）
- ⚠ **给生成器的硬提醒**：RDKit 默认 `MolFromSmiles` 会**删掉显式 H**，从而丢失 map 21/22，上面 4 个 H 对会从自动 diff 里消失。必须用 `Chem.SmilesParserParams(); p.removeHs=False`（或等价）解析。

### 25.3 reaction_center 双写（三套序号都注明）
| 边 | 题源 map 标签序 **1-based** | 41 原子工作序（ts_0008 built）**1-based → 0-based** | 27 原子工作序（新模型）**1-based → 0-based** |
|---|---|---|---|
| **E1a** | form (2,20) N20–C2；(4,21) O4–H21；break (2,4) C2=O4；(20,21) N20–H21 | form (2,32)、(3,41)；break (2,3)、(32,41) → 0-based form **[1,31]、[2,40]**；break **[1,2]、[31,40]** | form (2,18)、(3,27)；break (2,3)、(18,27) → 0-based form **[1,17]、[2,26]**；break **[1,2]、[17,26]** |
| **E1b** | form (2,3) C2=C3；(4,22) O4–H22；break (3,22) C3–H22；(2,4) C2–O4 | form (2,4)、(3,10)；break (4,10)、(2,3) → 0-based form **[1,3]、[2,9]**；break **[3,9]、[1,2]** | **同 41 原子值**（涉及原子 2/3/4/10 全在被保留的前 10 位）form (2,4)、(3,10)；break (4,10)、(2,3) → 0-based 同上 |
- 27 原子工作序换算规则：built 1–10 → 新 1–10；built 25–41 → 新 11–27（故 N20: built32→**18**；H21: built41→**27**；Cα: built28→**14**；COOH C: built26→**12**；=O13: built25→**11**；O15: built27→**13**）。

### 25.4 模型约化（本条须与数值一起写）
- **图/节点层**：保持 41 原子 dot-joined complex（含苯甲醛 map 5–12 作旁观组分），与现有 TASKS 风格一致。
- **计算层**：E1a/E1b 的**分母与 TS 均用 27 原子子体系**（map 1,2,3,4,13–22 及各自 H；苯甲醛 map 5–12 与其 H 全部排除）——即 RC_27（job 1044）与 INT1_27（待提交）；苯甲醛自身的 job 1045 仅作**身份证据**，**不进任何分母**（两端同为 27 原子，苯甲醛相互抵消）。
- **模型未知**（须随数值披露）：仅 CPCM(DMSO) 连续介质，**无显式溶剂/抗衡离子/外加碱**；27 原子两性离子只靠连续介质稳定；旧 41 原子 +41.39 kcal/mol 质子转移鞍点可能因缺质子受体被抬高；脯氨酸 COOH 作分子内穿梭是可检验假设。

## 26 2026-10-17 14:05 — job 1045（苯甲醛旁观组分）身份证据完成；job 1044（RC_27）仍在优化

### 26.1 job 1045 BZA_14 Opt+Freq —— **仅身份证据，不进任何分母**
- log: /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split/BZA_14_optfreq.log ，sha256 eac77af99fea118fb63c305793e4598aca27c7385fb63b3235358bfe1d3320ca ，5219 行
- 输入 BZA_14_optfreq.gjf sha256 8fa424207a120717a9094c268ad24bfd64fe8db172165c59c2e3107c9b0956a3 ；起点 BZA_14_start.xyz sha256 0234f6f9142587b6d7f8125adb7d56780542a8c529716021563b5382b600f761（14 原子 C7H6O）
- L3229 ' SCF Done:  E(RB3LYP) =  -345.354833694     A.U. after    9 cycles'；L3393 'Optimization completed.'；L3394 '   -- Stationary point found.'
- 频率段：L4091 ' SCF Done:  E(RB3LYP) =  -345.354833694     A.U. after    1 cycles'；L4877 'Optimization completed.'；L5219 ' Normal termination of Gaussian 16 at Sat Oct 17 13:57:45 2026.'
- L4383 ' Low frequencies ---  -10.2751   -6.9945   -0.0010    0.0003    0.0004    7.3145'（平移/转动伪模，非振动模）；L4384 ' Low frequencies ---  125.0393  220.6497  244.6223'；**全 log 无 imaginary 行**；12 个 'Frequencies --' 带 = 36 模（14 原子 3N-6=36），最低真实振动 L4393 ' Frequencies --    125.0345               220.6497               244.6222'；log_parser: imaginary_frequencies=[] , normal_termination=true , opt_converged=true
- 身份（终态几何 L3881 Input orientation 块）：C2=O1 1.215 A、C2-H9 1.119 A、C2-C3 1.479 A，仍为完整苯甲醛；ZPE 0.110073 Eh
- **用途限定**：只作旁观组分身份证据；27 原子模型不含苯甲醛，故**绝不作为 E1a/E1b 分母**（两端同为 27 原子，苯甲醛相互抵消）。

### 26.2 job 1044 RC_27 Opt+Freq —— 未完成（写本段时刻）
- log: .../split/RC_27_optfreq.log（当时 5780 行，sha256 509d7c4d6370e5cf75dfeef2a71f4fa1911214106601cf28384d32a7e12c785f —— **中间态哈希，禁止引用为终态证据**）
- 最后可见 L5868 ' Step number   8 out of a maximum of  149'；grep 'Normal termination' 无命中 ⇒ 优化仍在进行，**无可报告能量/频率**
- 下一动作：终态通知后按 §24.5 顺序（先 RC_27 读数 → 再提交 INT1_27 Opt+Freq）。

---

## 27 2026-10-17 14:08 — RC_27 分母完成（75 模 / 0 虚频）；INT1_27 Opt+Freq 已提交（job 1051）

### 27.1 job 1044 RC_27 Opt+Freq 终态读数（E1a 分母）
- log: /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split/RC_27_optfreq.log ，sha256 9d68305052b492c15774082f528f94acf61ffcee9885d8729f020ed1a20589dd ，15572 行（终态）
- 输入 RC_27_optfreq.gjf sha256 7fb6f67f8c96fb0d1ee9d828c14dd45f8936f62398cc53ed7bc9819bcf25819f（route '#p opt freq B3LYP/def2SVP empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=dmso)'，q0/m1，8 cpu / 10240 MB）
- **纯电子能量 E(RC_27) = -593.934532807 Eh**：opt 段 L11565 ' SCF Done:  E(RB3LYP) =  -593.934532807     A.U. after    7 cycles'；freq 段 L13017 同值 ' SCF Done:  E(RB3LYP) =  -593.934532807     A.U. after    1 cycles'（同批同法，可直接作差）
- 收敛：L11639 ' Step number  17 out of a maximum of  149'；L11841 'Optimization completed.'；L11842 '   -- Stationary point found.'
- 两个 Normal termination：L12487 ' Normal termination of Gaussian 16 at Sat Oct 17 14:04:13 2026.'（opt 内部 step 1 收尾，L12491 起进入 '#P Geom=AllCheck Guess=TCheck SCRF=Check GenChk RB3LYP/def2SVP Freq' 的 step 2）；L15572 ' Normal termination of Gaussian 16 at Sat Oct 17 14:07:03 2026.'（整作业结束）
- **模数 75 = 3N-6（N=27）**：25 个 'Frequencies --' 带，首带 L13474 ' Frequencies --     21.4691                25.1412                41.4769'，末带 L14290 ' Frequencies --   3169.1001              3470.3495              3733.9233'
- **0 虚频**：全 log 无 'imaginary' 行（L1507 式的 ' ******  N imaginary frequencies' 头不存在）；L13464 ' Low frequencies ---  -20.1029   -1.2457    0.0003    0.0008    0.0009    9.2880' 的负值是**平移/转动伪模**，不是振动模（判定只看频段表 + imaginary 表头）；最低真实振动 21.4691 cm-1
- log_parser 复核：frequencies_cm 长度 75、imaginary_frequencies=[]、normal_termination=true、opt_converged=true、job_types=[freq,opt]
- 热化学（仅记录，不用于纯电子能垒）：L14387 ' Zero-point correction=                           0.228709 (Hartree/Particle)'；thermal Gibbs 修正 0.182982 Eh；L14367 ' Zero-point vibrational energy     600475.1 (Joules/Mol)'

### 27.2 RC_27 极小值的几何（L12515–L12541，27 原子工作序）：松散氢键复合物，不是接触对
- C2···N20 (2-18) = **3.757 Å**；C3···N20 (4-18) = 5.222 Å ⇒ 胺氮与羰基碳相距 3.76 Å，**无 C–N 成键倾向**
- C2=O4 (2-3) = 1.220 Å；N20–H21 (18-27) = 1.023 Å；**O4···H21 (3-27) = 2.030 Å** ⇒ 该极小值是 proline N–H21···O4=C2 **氢键复合物**
- C2–C3 (2-4) = 1.509 Å；C3–H22 (4-10) = 1.098 Å；O4···H22 (3-10) = 2.530 Å
- 结论/用途：RC_27 末帧**不能**直接当 E1a 的 TS guess（离攻击构型太远）；E1a guess 必须用近攻击构型（job 1017 27 原子帧 / job 1042 的 -1547.0708 cm-1 鞍点帧：C2–N20 1.633 Å、O4–H21 1.334 Å）。

### 27.3 job 1051 INT1_27 Opt+Freq（E1b 分母 / E1a 产物端）已提交
- 输入 INT1_27_optfreq.gjf sha256 613d0f90382bc53704d76537042b30317f303ea9178674a3b74691bfa3eee624（route 与 RC_27 逐字相同，task=[opt, freq]，q0/m1，8 cpu / 10240 MB / priority 0，chk .../split/INT1_27_optfreq.chk）
- 起点 INT1_27_start.xyz sha256 3c48099cf8e77f2bad7a5379901a23ab68503bdedc620955ae18f1ce0ad91a40（27 原子两性离子 carbinolamine：C2–O4 1.362 / C2–N20 1.632 / O4–H21 1.334 / C2–C3 1.531 Å，取自 ts_opt refine.log L159994 的 41 原子帧去掉苯甲醛 11–24 号原子）
- **E(INT1_27) 与 75 模 / 虚频判定：missing measurement（作业 job 1051 在跑，未产生任何终态读数）**；若出现 2 个以上虚频，说明该起点尚未落入极小值，作分母前必须先 Relax 到 0 虚频。
- 队列：现 4/4 满（1044 已结束、1046/1047/1048 在跑），1051 可能排队——属预期，不重投、不调 priority、不杀进程。

### 27.4 模型未知（随 §27 数值一并披露）
仅 CPCM(DMSO) 连续介质；无显式溶剂/抗衡离子/外加碱；27 原子两性离子只靠连续介质稳定；RC_27 是松散氢键复合物（O4···H21 2.03 Å），故 E1a 的 DeltaE‡ 以该复合物为分母时**包含结合/去溶剂化代价**，与 41 原子模型（含苯甲醛）不可直接比较。

## 28 2026-10-17 14:36 — job 1051 终态：carbinolamine_27 成立（情形 1，可直接采用）；E1a ts_prepare 已发（ts_0015 / job 1055）

### 28.1 job 1051 终态读数（E1b 分母 / E1a 产物端）
- log: /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split/INT1_27_optfreq.log ，sha256 **c03e0a82d78d22b96474ab48ee40799adb63a894bb9cefcd27c7051799024f63** ，30757 行（终态）
- **E(INT1_27) = -593.929762803 Eh**：L26615 ' SCF Done:  E(RB3LYP) =  -593.929762803     A.U. after    7 cycles'（opt 末次）、L28142 同值（freq 段）
- 收敛：L26689 ' Step number  37 out of a maximum of  162'；L26903 'Optimization completed.'；L26904 '   -- Stationary point found.'
- **75 模 = 3N-6**：25 组 'Frequencies --'；**0 虚频**（全 log 无 'imaginary' 行；L28588 ' Low frequencies ---   -7.9278   -4.0634 ...' 为伪模，不引为虚频证据）；**最低实模 78.1490 cm-1**（L28598 ' Frequencies --     78.1490                91.3061              112.9005'）
- 热化学仅备查：L29511 ' Zero-point correction=                           0.232709 (Hartree/Particle)'
- 两条 Normal termination：L27581 ' Normal termination of Gaussian 16 at Sat Oct 17 14:31:05 2026.'（内部 step 1=opt）、**L30757 ' Normal termination of Gaussian 16 at Sat Oct 17 14:35:06 2026.'**（整作业；内部 step 2 route 见 L27585 '#P Geom=AllCheck Guess=TCheck SCRF=Check GenCk RB3LYP/def2SVP Freq'）

### 28.2 ΔE 相对 RC_27（同批纯电子能，**不是** E1a 的 ΔE‡）
(-593.929762803) - (-593.934532807) = +0.004770004 Eh × 627.509474 = **+2.99 kcal/mol**
含义：模型内 carbinolamine 极小值相对 RC_27 氢键复合物的能量差（RC_27 = job 1044，L11565/L13017）。E1a 的 ΔE‡ 仍需 TS 唯一虚频落定后才可写。

### 28.3 质子归属（元素序自动识别，脚本 E1/split_contacts.py）⇒ **情形 1（可直接采用）**
| 量 | 实测 | 识别 |
|---|---|---|
| C2-O4 | 1.4208 Å | 原子 2-3 |
| C2-N20 | 1.4755 Å | 原子 2-18 |
| O4-H21（C2-OH） | **0.9699 Å** | 原子 3-27 |
| N20···H21 | 2.3798 Å | 原子 18-27 |
| N20 最近 H | **2.0603 Å**（位置 20 的 H） | N20 邻域最近 H |
| C14-N20 / C17-N20 | 1.4773 / 1.4680 Å | 环上 N 键 |
| 羧基 O13-H19 | **0.9739 Å** | O13 最近 H |
| 羧基 C12=O11 / C12-O13 | 1.2102 / 1.3409 Å；O11 无 H（最近 H 2.2898 Å） | 12-11 / 12-13 |
| C2-C3 / C3-H22 | 1.5351 / 1.1006 Å | 2-4 / 4-10 |
判定：**N20 三配位无 H + 羧基 COOH 完整 + C2-OH**，与 HI1_I1 串 'CC(C)(O)N1CCC[C@H]1C(=O)O.O=Cc1ccccc1' 删去旁观组分后的 27 原子质子化状态一致 ⇒ **无需双写**；本帧即 E1b 分母 / E1a 产物端。
过程读数（受约束起点帧曾 +38.1、step 31 时 +3.18）已被终态取代，仅作过程记录。

### 28.4 导出与比对
- 收敛帧：/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split/INT1_27_opt_frame.xyz（format_converter log→xyz，frame 37，**未手抄坐标**），sha256 **b2f2ffaaf64169916e29d59fa44a49e223e394e21f69907980b8a83151fa5d36**
- 与 RC_27_opt_frame.xyz（c1f789e0…）元素序**逐位一致 27/27** ⇒ atom_map = 恒等 1..27
- 产物端 provenance：.../split/INT1_27_PRODUCT_PROVENANCE.md sha256 **0f8bb9436ac7f0ab826834a33c3950fc4332ae146a45ad774c228b5efdf5a9b5**（含来源行号 L27860 Input orientation / L27994 Standard orientation、情境 1 判定、9 项距离、ΔE +2.99）

### 28.5 E1a ts_prepare 已提交（独立 run，未与 E1b 串联）
- run **ts_0015**（/home/ly/Cloudra-mechanism-agent/ts/ts_0015），revision 11，status waiting，stage refine，waiting_for **job 1055**（ts_opt，state ready→running 14:36:37）
- 输入快照 jobs/declaration_0001/ts_opt/refine.gjf sha256 **d40325e042b9596e7f86ce2271e48e1acd1d9be958e1960fd94082765f8fecf6**，route '#p opt=(TS,calcfc,noeigen) B3LYP/def2SVP empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=dmso)'，q0/m1，%nproc=8 / %mem=10240MB
- 绑定证据（平台已落盘）：path/input_0001/provided.xyz sha256 **3c48099cf8…**（= guess INT1_27_start.xyz 逐字节相同）、path/input_0001/provenance_0001.md sha256 **5178bdf6…**（= E1A_GUESS_PROVENANCE.md）、build/input_0001/reactant/seed.xyz **c1f789e0…**、build/input_0001/product/seed.xyz **b2f2ffaa…**
- reaction_center（ reactant 1-based ）= form (2,18),(3,27) / break (2,3),(18,27)；题源 map 1-based = form (2,20),(4,21) / break (2,4),(20,21)；分母 = RC_27 −593.934532807

### 28.6 模型未知（随 §28 数值披露）
仅 CPCM(DMSO) 连续介质；无显式溶剂/抗衡离子/外加碱；27 原子模型无质子穿梭剂（脯氨酸 COOH 作穿梭仍未测）；E1a 的 ΔE‡ 以松散 RC 复合物（C2···N20 3.757 Å、O4···H21 2.030 Å）为分母，含 N 进攻前的结合/去溶剂化代价。

## 29 2026-10-17 14:47 — E1a ts_opt（job 1055）收敛：单一候选鞍点，ΔE(TS−RC_27) 初值 +38.01 kcal/mol（**待 freq/IRC 验收，不得作最终 ΔE‡**）

### 29.1 收敛与终止
- log：/home/ly/Cloudra-mechanism-agent/ts/ts_0015/jobs/declaration_0001/ts_opt/refine.log ，sha256 **0023847fe5b2e2961f9914d7a4f7a694ae11a9d826bd892b190866274f0a430b** ，11399 行
- L10515 ' Step number  14 out of a maximum of  162'；四判据全 YES：L10718 ' Maximum Force            0.000006     0.000450     YES'、L10719 ' RMS     Force            0.000001     0.000300     YES'、L10720 ' Maximum Displacement     0.000391     0.001800     YES'、L10721 ' RMS     Displacement     0.000111     0.001200     YES'
- L10723 'Optimization completed.'；L10724 '   -- Stationary point found.'；L11399 ' Normal termination of Gaussian 16 at Sat Oct 17 14:45:41 2026.'
- 输入快照 d40325e042b9596e7f86ce2271e48e1acd1d9be958e1960fd94082765f8fecf6；route '#p opt=(TS,calcfc,noeigen) B3LYP/def2SVP empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=dmso)'（未发生 l103 退化，未用笛卡尔规避）

### 29.2 能量（初值，非最终 ΔE‡）
- E(候选 TS) = **-593.873953336 Eh**（L10442 ' SCF Done:  E(RB3LYP) =  -593.873953336     A.U. after    7 cycles'）
- ΔE(TS − RC_27) = (-593.873953336) - (-593.934532807) = +0.060579471 Eh × 627.509474 = **+38.01 kcal/mol**（分母 job 1044 L11565/L13017）
- 参考：ΔE(carbinolamine_27 − RC_27) = +2.99 kcal/mol（§28.2）⇒ 该候选鞍点比产物端高约 35.0 kcal/mol
- **状态标注：单一候选鞍点（candidate_only）**；最终 ΔE‡ 必须等 frequency 唯一虚频 + 模矢落点 + 两端 0 虚频 + 连通性验收后才可写。

### 29.3 几何（末次 Input orientation L10907 起的 27 原子块，元素序自动识别）
| 量 | 候选 TS | RC_27（c1f789e0…） | INT1_27（b2f2ffaa…） |
|---|---|---|---|
| C2–N20 | **1.6254 Å** | 3.7571 | 1.4755 |
| C2–O4 | **1.3602 Å** | 1.2195 | 1.4208 |
| N20–H21 | **1.2217 Å** | 1.0228 | 2.3798 |
| O4–H21 | **1.3488 Å** | 2.0299 | 0.9699 |
| C2–C3 | 1.5297 Å | 1.5089 | 1.5351 |
| C3–H22 | 1.0969 Å | 1.0976 | 1.1006 |
| O13–H19（羧基） | 0.9749 Å | 0.9737 | 0.9739 |
读法：C2–N20 与 H21 均处于两端之间（N–C 3.76 → 1.63 → 1.48；H21 从 N 上 → 桥位 1.22/1.35 → O 上 0.97），**E1b 的三对（C2–O4 断裂、C2=C3、C3–H22）在此帧尚未启动**（C2–C3 1.5297、C3–H22 1.0969），与「E1a 只做加成+质子转移」的分步设定一致。

### 29.4 平台状态与后续
- ts_inspect(ts_0015)：revision 11、status waiting、stage refine、waiting_for job 1055 (done)、next.action = wait_for_system；available_results 显示 ts_opt=done，**frequency 阶段目录尚未创建**（jobs/declaration_0001/ 下只有 ts_opt）⇒ 虚频读数 **missing measurement**。
- 后续：frequency 完成 → 判「唯一虚频 + 模矢在 N20 与 C2 上都有可观位移（纯 PT 模不算）+ H21/O4 有位移」→ IRC（或经批准的替代口径，措辞只写「verified（替代口径：无 IRC）」）→ 两端 0 虚频 → 才写最终 ΔE‡。

### 29.5 命名对账（三段齐写，后续所有模矢/几何报告强制执行）
- **工作序 1-based（以 ts_inspect(ts_0015) 的 27 原子表为准）**：C2=**2**、羰基 O4=**3**、C3=**4**、H22=**10**、N20=**18**、转移 H21=**27**、Cα=14、羧基 C=12、羧基 =O=11、羧基 OH O=13。watch pairs 一律写工作序号：[[2,18],[3,27],[18,27],[2,3]]。
- **原始序 1-based（题源 atom-map 标签序 / HI1_R·HI1_I1 的 map 号）**：C2=**2**、羰基 O=**4**、C3=**3**、H22=**22**、N=**20**、转移 H=**21**。§29.3 表里括号写的 20/4/21 即此套。
- **化学标签**：N / 羰基 O（羰基氧）/ 转移 H（N–H 质子）/ C2（羰基碳）/ C3（α-甲基碳）/ H22（E1b 转移质子）。
- 纪律：任何模矢、距离、bond pair 报告必须同时给出「工作序 1-based + 原始序 map 标签 + 化学标签」三段；只有一套号的写法一律视为不合格，不得进入回填。§29.3 的 C2–N20 / C2–O4 / N20–H21 / O4–H21 字样按工作序读（N=18、羰基 O=3、转移 H=27）。

## 30 2026-10-17 15:05 — (B) 路径实测：ts_resume(changes={}) 被平台**结构性拒绝**，stage 仍停在 refine

### 30.1 执行条件（本机 date 15:05:22 CST 只读确认，条件成立）
ts_inspect(ts_0015)：revision **11**、stage **refine**、status waiting、waiting_for [job 1055 (ts_opt) **done**, ended 14:45:42]、next.action **wait_for_system**、required_inputs []、editable_groups []、blocked null；jobs/declaration_0001/ 只有 `ts_opt/`（refine.gjf / refine.log / fort.7 / state_1055.json），**无 frequency**；process.json 30,059 B、mtime **14:36:37**。

### 30.2 拒绝结果（不是输入缺项，也不是科学结论）
- ts_resume(run_id=ts_0015, changes={}, reason 逐字) → **is_success=false**，返回 revision 0 / receipt null，message 原文：
  `ts_resume: no input change or failed attempt to retry; use ts_inspect`
- call_id：只读确认 `tc_a1057bdb18ec45a1`（ts_inspect）、被拒 `tc_76cecfe9ac70436c`（ts_resume；为取 call_id 重复一次，两次返回逐字相同、无副作用）。
- 副作用：**无**——没有新建目录、没有新 job id、process.json 未变（mtime 仍 14:36:37）；未重投、未调 priority、未 kill、未删 .pipeline.lock。

### 30.3 技术含义
ts_resume 的语义是「改输入 / retry 失败尝试」；当 changes={} 且 failed_attempt=null 时平台在校验层直接拒绝 ⇒ **B 路径在语义上无法推进 wait_for_system 停滞**。能保持现有 refine.log 为唯一 ts_opt 证据的只有平台侧修复；若必须由本 lane 破局，则需要一次真实输入改动（例如 ts_optimization 同值重声明），其后果通常是 ts_opt 被 invalidated 重跑并产生两份 ts_opt 证据，**须由 as_ec848a7673b74e35 明确授权**，本 lane 不自行执行。

### 30.4 当前读数汇总（虚频仍为 missing measurement）
- 候选鞍点：E = -593.873953336 Eh（refine.log L10442），ΔE(TS − RC_27) = **+38.01 kcal/mol**，状态 **candidate_only**
- 虚频：**missing measurement —— frequency 作业从未生成**（jobs 下无 frequency 目录、queue 无新 job）
- 分母：RC_27 = -593.934532807 Eh（job 1044，L11565/L13017）；产物端 INT1_27 = -593.929762803 Eh（job 1051，L26615/L28142）

## 31 2026-10-17 15:07 — (D) 诊断频率作业**已制备、未提交**（管线 stagnate 的旁证作业，非交付证据）

### 31.1 几何来源（工具抽取，未手写坐标）
- refine.log（sha 0023847fe5b2e2961f9914d7a4f7a694ae11a9d826bd892b190866274f0a430b）最后一帧，经 format_converter(log→xyz) 导出：
  /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split/E1A_TS_candidate_job1055.xyz ，sha256 **2b4cf70f539a62f941422b7e652d90d1620c4e4a10beefd3162ba0ea2cbd8f50** ，27 原子，header 'opt step=13'
- 元素序与 27 原子工作序**逐位一致 27/27**（`C C O C H H H H H H O C O C C C C N H H H H H H H H H`，与 RC_27_opt_frame.xyz / ts_0015 build 的 reactant·product seed 相同）
- 几何自检：该帧 C2–N20 1.6254 Å、C2–O4 1.3602、N20–H21 1.2217、O4–H21 1.3488，与 §29.3 用 L10907 Input orientation 块读出的值一致（仅取向不同 ⇒ 证明取的是同一收敛结构）

### 31.2 输入（只做 freq：无 opt / 无 opt=TS / 无 calcFC / 无冻结坐标）
- /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split/E1A_TS_diag_freq.gjf ，sha256 **ef3d748cd7d752649e6a38f2f9a451fbcc1699071d3ee7dd43a50a157a81af8a** ，36 行
- route 逐字：`#p freq B3LYP/def2SVP empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=dmso)`；`%nproc=8`、`%mem=10240MB`；q0/m1
- 末尾字节复核（tail -c 60 | od -c）：…… `1 . 4 9 9 6 1 7 0 0 \n \n` ⇒ 末尾为坐标行换行 + 一个空行（Gaussian 规范）
- 状态：**已制备、未提交**（等 as_ec848a7673b74e35 的 go；不抢槽、不调 priority）

### 31.3 定性（必须与任何（D）结果一起写）
(D) 是**诊断**作业，用于判唯一虚频模矢落点（协同 / 纯 PT / 伪象），**不作交付证据**；交付仍需管线 ts_freq + 两端 0 虚频 + 连通性。若日后管线 freq 也能跑出，两者互为交叉校验，不一致时**以管线证据为准**并上报。

### 31.4 (D) 已获授权并提交（job 1062）
- 授权：as_ec848a7673b74e35 于 2026-10-17 15:0x 转达主协调裁定（选 (D)，run ts_0015 保持 rev 11 不动，verdict 仍 missing）；route 要求与 refine 同级、只换任务词。
- 提交：**job 1062**，调度 started_at **2026-10-17T15:07:05+08:00**（直接起跑、未排队），submit call_id `tc_6d373c9271a64211`；槽位快照 running 1049/1059/1061/1062、queued 空、free cpus 0。
- 输入 sha256 `ef3d748cd7d752649e6a38f2f9a451fbcc1699071d3ee7dd43a50a157a81af8a`；几何 sha256 `2b4cf70f539a62f941422b7e652d90d1620c4e4a10beefd3162ba0ea2cbd8f50`；chk 新文件名 E1A_TS_diag_freq.chk（不覆盖任何现有 chk/log）。
- 终态读数：**missing measurement**（写作时作业在跑）。

### 31.5 符号陷阱实证（三段齐写纪律的必要性证据）
该 xyz 是**工作序**文件：N 在 **18**、羰基 O 在 **3**、转移 H 在 **27**、羰基 C 在 **2**、α-甲基 C 在 **4**、H22 在 **10**。若误用题源 map 标签号（C2/N20/O4/H21）直接索引该文件，Coordinator 实测会得到 C2–N20 **3.6001**、C2–C3 **1.3602** 这类无意义值；改用工作序后立刻与 §29.3 对上（1.6254 / 1.3602 / 1.2217 / 1.3488）。⇒ 同一文件混用两套序号会**静默给出错误距离**，故模矢/距离报告一律「工作序 1-based + 题源 map 标签 + 化学标签」三段齐写；上述错误读数未被对外引用。

## 32 2026-10-17 15:11 — (D) 诊断 freq（job 1062）终态：**恰 1 虚频 −1551.2317 cm⁻¹，但模矢以 H21 为主（79.7%），C2 仅 5.3%、N20 0.8% ⇒ 纯 PT 主导，不构成 E1a 的协同鞍点**

### 32.1 终态读数
- log：/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split/E1A_TS_diag_freq.log ，sha256 **e6c128476d1eb716b234b5ed77bc1d9b13c07d4d3846648ae3026f29fdcfdf3d** ，3001 行
- 模数：'Frequencies --' **25 组 ×3 = 75 模 = 3N−6（27 原子）**；首组 L1110、末组 L1926
- 虚频：L1101 ` ******    1 imaginary frequencies (negative Signs) ****** `；L1110 ` Frequencies --  -1551.2317                41.7021                73.1702` ⇒ **恰 1 个，−1551.2317 cm⁻¹**，约化质量 1.0918、力常数 1.548000
- L1099 ` Low frequencies ----1551.2317   -9.4763   -5.0350   -0.0005    0.0002    0.0008`（伪模行，不引为虚频证据）；**最低实模 = 41.7021 cm⁻¹（L1110 频段表首值）⇒ ≤50 cm⁻¹，按「坐标极软、数值噪声边缘」标注**
- 能量：L652 ` SCF Done:  E(RB3LYP) =  -593.873953336     A.U. after   13 cycles`（与 ts_opt 同值 ⇒ 未被 freq 改动）；ZPE L2024 ` Zero-point correction=                           0.228317 (Hartree/Particle)`；L3001 ` Normal termination of Gaussian 16 at Sat Oct 17 15:11:28 2026.`

### 32.2 虚频模矢（parse_imag_mode27.py sha 87e06566…；工作序 1-based + 题源 map 标签 + 化学标签）
| 原子(工作序) | map 标签 | 化学标签 | \|d\| | 占比 Σ\|d\| |
|---|---|---|---|---|
| **27** | map21 | **H21（转移质子）** | **1.0008** | **0.797** |
| 2 | map2 | C2（羰基碳） | 0.0671 | **0.053** |
| 3 | map4 | O4（羰基氧） | 0.0490 | 0.039 |
| 18 | map20 | N20 | 0.0100 | **0.008** |
| 14 | map16 | Cα | 0.0141 | 0.011 |
| 6/8/17/20/22/24 | - | 环/甲基 H（打印精度噪声底） | 0.0141 | 0.011 |
| 4/9/26 | map3 等 | C3 与环 H（噪声底） | 0.0100 | 0.008 |
| 其余（1,5,7,10,11,12,13,15,16,19,21,23,25） | - | 甲基 H22、羧基全部原子等 | 0.0000 | 0.000 |
- Σ|d| = 1.2559；**打印精度噪声底 = 0.0141**（大量原子精确落在该值）⇒ C2 的 0.0671 ≈ 4.8× 噪声底、N20 的 0.0100 ≈ 0.7× 噪声底
- watch pairs（工作序）：C2–N20 (2,18) frac 0.061 cos +0.298；O4–H21 (3,27) frac **0.836** cos −0.543；N20–H21 (18,27) frac **0.805** cos −0.040；C2=O4 (2,3) frac 0.092 cos +0.304

### 32.3 H27 位移方向（主协调新增硬判据）
- d(H21) = (0.6500, 0.7600, 0.0400)；几何取自 E1A_TS_candidate_job1055.xyz（O3–H27 = 1.3488、N18–H27 = 1.2217）
- 投影到单位矢：**d·û(H→O3) = −0.909**、**d·û(H→N18) = +0.762**
- ⇒ 位移沿「H 离开 O3、趋向 N18」= **O3–H27 伸长、N18–H27 缩短**，与声明步骤的 N–H/O–H 转移坐标同轴（特征矢符号任意，不影响判读）

### 32.4 三档判读（按主协调口径，本 lane 不自行回填）
- **不满足「协同」档**：协同要求 C2 与 N20 都有可观位移；实测 C2 0.053（4.8× 噪声底，小但非零）、**N20 0.008（低于噪声底）**、H21 0.797 占绝对主导
- **判为「纯 PT 主导（proton-transfer-dominated）」**：鞍点主要沿 N–H/O–H 转移坐标，C–N 成键尚未参与；叠加「最低实模 41.7021 cm⁻¹ ≤50」的软坐标警示
- 与 41 原子模型对照：同帧在 41 原子下为 −1547.0708 cm⁻¹，组成几乎相同（atom41 0.794 / C2 0.051 / O4 0.033）⇒ **模型约化没有改变该模的性质**，纯 PT 特征不是去苯甲醛造成的伪象
- 结论（本 lane 表述）：该帧**不应作为 E1a 的交付 TS**；ΔE(TS−RC_27) = +38.01 kcal/mol **不回填**；按既有规则应改走已批准的 fallback（RC_27 ↔ INT1_27 沿 C2···N20 内插至 2.10 Å、H21 留 N20 的早期进攻帧 + 新 provenance + N–C 单调/minsep≥0.9 自查），或由主协调裁定把 E1a 再拆一档（先 N 进攻、后质子转移）。

### 32.5 证据地位
(D) 为诊断作业，**不作交付证据、不据此回填 ΔE‡**；文件与 sha 全留。管线 ts_0015 仍 rev 11 / stage refine / verdict missing。

## 33 2026-10-17 15:18 — E1a fallback (a)** 已制备（未提交）：刚性片段模型在 R(C2–N18)≤2.3 Å 无法避免非键碰撞，交付帧仅以 0.90 Å 的甲基 H···N18 接触达到数值门槛

### 33.1 制备过程的量化失败链（全部为刚性片段构造，未跑 QM）
| 尝试 | 构造 | 实测结果 | 判定 |
|---|---|---|---|
| v1/v2 | 重原子 Kabsch 后全原子笛卡尔内插 | C2–O3 塌到 0.97 Å、C3–H22 0.52 Å、minsep 0.45–0.52 | 否（成键塌陷） |
| v3 | 丙酮片段刚体内插（质心 + 旋转 slerp） | minsep 0.33–0.49（甲基扫过吡咯烷环） | 否（碰撞） |
| v4 | 仅沿 C2→N18 平移至 2.10 Å | 单调但 O3···H21 0.61 Å、O3···N18 1.53 Å | 否（O/H、O/N 重迭） |
| v5–v9 | 绕 C2 转到 O3–C2···N18 = 100–130°（Bürgi–Dunitz）再平移 | 最好 minsep 0.48–0.71（甲基 H 与脯氨酸相撞：6-14/1-18/8-20） | 否（碰撞） |
| v10 | 追加绕 C2→N18 轴的方位角自旋（0–350°，10° 网格） | R=2.10 时最好 minsep **0.854 Å** | 低于 0.90 门槛 |
| v11 | 同一刚性模型，平移量二分使 minsep=0.90 | **R(C2–N18)=2.2916 Å**、minsep **0.9000 Å**（原子 7=丙酮甲基 H 与 18=N） | 数值达标但代价是 0.90 Å 的 H···N 严重非键接触 |

### 33.2 交付帧（documented next action，**未提交、未作 guess**）
- xyz：/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split/E1A_fallback_earlyattack_minsep090.xyz ，sha256 **f589a84857249e6156c09d67b2f646d300f7dc04b88ee2a01f954083a3bfb7bd** ，27 原子
- 参数：脯氨酸骨架与 H21 取 RC_27 原样（N18–H21 1.0228 Å，H21 朝背离羰基方向重定向以让出进攻通道）；丙酮刚性绕 C2 旋至 O3–C2···N18 = 105°、绕 C2→N18 自旋 150°、平移二分使 minsep=0.90 Å ⇒ **R(C2–N18)=2.2916 Å**
- 关键距离：C2–O3 1.2195（未变）、N18–H21 1.0228、O3···H21 3.8705、C2···H21 3.2948、O3···N18 2.8610；角度 O3–C2···N18 105.0°、H–N–Cα 98.3°、H–N–C17 71.6°
- provenance：.../split/E1A_FALLBACK_PROVENANCE.md ，sha256 **575be8bf357f7ec771b5d49d698a56632316cad0deede37623793ff3bfe73b06**（含来源 sha、失败链、λ/minspec 表、模型条件）

### 33.3 逐 λ（同一刚性模型）的 R 与 minsep 表
| 平移比例 f | R(C2–N18) Å | 全局 minsep Å |
|---|---|---|
| 0.000 | 3.7571 | 0.9737 |
| 0.200 | 3.4257 | 0.9737 |
| 0.400 | 3.0943 | 0.9737 |
| 0.600 | 2.7628 | 0.9737 |
| 0.800 | 2.4314 | 0.9567 |
| **0.884** | **2.2916** | **0.9000**（二分点，原子 7–18） |
| 0.900 | 2.2657 | 0.8915 |
| 1.000 | 2.1000 | **0.8540** |
R(C2–N18) 沿 f 严格单调下降（3.7571 → 2.1000）。

### 33.4 结论与建议（诚实定性）
0.90 Å 门槛是靠**一个丙酮甲基 H 距 N18 仅 0.90 Å** 换来的——这是严重非键碰撞，不是可用的进攻构型。⇒ 刚性片段模型**无法**在 R(C2–N18) ≤ 2.3 Å 产生化学上可接受的早期进攻帧，**吡咯烷环必须松弛**；因此本帧**不建议**原样作 TS guess，若要用必须先做固定 R(C2–N18) 的约束松弛（需算力与授权，未提交）。

### 33.5 其他
- 早期刚性体产物已改名为 E1A_fallback_earlyattack_R210_REJECTED.xyz（sha 116a1b0d…，minsep 0.49 Å），**不得使用**。
- E1a 仍 **未验证**、ΔE‡ **null**；+38.01 kcal/mol 仅作「PT 驻点相对 RC_27 的电子能差」。未提交任何作业、未 ts_resume。

### 33.6 协调者要求入册的两条（不需要新算）
1. **刚性内插在本体系结构性不可行——量化证据**：v1/v2 笛卡尔内插（C2–O3 0.97 Å、C3–H22 0.52 Å、minsep 0.45–0.52）；v3 丙酮刚体内插（minsep 0.33–0.49）；v4 纯轴向平移（O3···H21 0.61、O3···N18 1.53）；v5–v9 绕 C2 转到 Bürgi–Dunitz 100–130°（甲基 H 撞脯氨酸 6-14 / 1-18 / 8-20，minsep 0.48–0.71）；v10 方位角自旋网格（R=2.10 时最好 0.854）；v11 二分达标点 **minsep 0.9000 Å 由原子 7（丙酮甲基 H）–18（N）仅 0.90 Å 的严重非键接触换来**，此时 R(C2–N18)=2.2916 Å。⇒ 13 个候选构型无一在 R(C2–N18) ≤ 2.3 Å 且满足化学可接受接触。
2. **唯一可行路径 = 固定 R(C2–N18) 的约束松弛**（例如把 R(C2–N18) 约束在 2.3–2.5 Å、其余自由度放开，让吡咯烷环与甲基自行松弛）：**当前未获授权、未提交、未执行**（属 documented next action）。本 lane 不自行发起。

## 34 2026-10-17 15:2x — conformer_search 受导种子路径亦不可行（三次尝试全 0 qualified）；最接近帧干净但只能到 R(C2–N18)=2.69–2.75 Å

### 34.1 三次调用（只制备、零算力；未提交任何 QM 作业、未 ts_resume）
| # | input | distance_filters（1-based 工作序） | num_confs / seed | 结果 |
|---|---|---|---|---|
| v1 | RC_27_opt_frame.xyz（c1f789e0…） | (2,18) 2.2–2.5；(18,27) 1.0–1.1；(2,3) 1.32–1.45 | 50 / 42 | **0 qualified**（generated 8 / optimized 8 / rejected 8 / retained 0）；closest 2-18 **2.6920** |
| v2 | 同上 | (2,18) 2.2–2.6；(18,27) 1.0–1.1；(2,3) 1.19–1.45 | 80 / 7 | **0 qualified**（同计数）；closest 2-18 **2.7508** |
| v4 | 同上 | (2,18) **2.6–3.0**；(18,27) 1.0–1.1；(2,3) 1.19–1.45 | 80 / 7 | **0 qualified**（同计数）；closest 2-18 **3.0481** |
- 工具原文（v4）：`No guided assembly candidate qualified; closest attempted geometry: .../E1a_seed_search_v4/closest_attempt.xyz`，诊断含 `reaction mode: placements are guided by the reaction center pairs ...; intra-fragment geometry stays rigid during placement` 与 `8 guided placement(s) retained for strict qualification before 0.5 A heavy-atom RMSD clustering`。
- 含义：该受导装配把**片段内几何固定为刚性**，因此只能在片段间作刚体摆放；在本体系最好的可达 R(C2–N18) 只有 2.69–2.75 Å，无法进入 2.2–2.5 Å 窗口 ⇒ **工具路径亦不可行**（不只是刚性脚本的问题）。

### 34.2 最接近帧的实测（元素序与 refine 收敛帧 27/27 一致）
| 帧 | sha256 | R(C2–N18) | R(N18–H21) | R(C2–O3) | minsep | 最紧 3 个接触 |
|---|---|---|---|---|---|---|
| v1 closest_attempt | 845a4bd9908e1607e7ead78d17896912bf2bc874d0310f50bb399fb90e813435 | **2.6920** | 1.0349 | 1.2383 | **0.9794** | 13(O)–19(H) 0.9794（羧基 O–H 键）；18(N)–27(H) 1.0349（N–H 键）；1(C)–7(H) 1.0926（甲基 C–H） |
| v2 closest_attempt | 9a5c9c3294834a8d344c66d77d5cc14122bf881c01b7606ae35d1b2267c067e9 | 2.7508 | 1.0303 | 1.2327 | 0.9807 | 13(O)–19(H) 0.9807；18(N)–27(H) 1.0303；1(C)–6(H) 1.0926 |
| v4 closest_attempt | aa6fc0a05b7ac2cca807b55f1fd7d41505e9891ae670f38a680b343bedfda71e | 3.0481 | 1.0255 | 1.2321 | 0.9801 | 13(O)–19(H) 0.9801；18(N)–27(H) 1.0255；4(C)–10(H) 1.0926 |
- 这 3 帧的 minsep **不是**由 H···N/O 反应对换来的：最紧接触全是正常化学键（羧基 O–H、N–H、甲基 C–H）。
- 但 **C2–O3 = 1.232–1.238 Å**，未达到门槛 ③（≥1.30）：因片段内刚性，羰基保持 RC 的 C=O 值。这**不是提前质子化**（H21 仍在 N 上，O3···H21 2.30–3.49），而是刚性模型的必然结果。
- v4 guidance manifest：.../E1a_seed_search_v4/guidance_manifest.json sha256 892f988ecb534972719aae1895fd0654e31243510888a163a0d233564286f803。

### 34.3 结论（本 lane 表述）
1. **工具路径（conformer_search guided）在本体系亦不可行**：3 次调用、3 组窗口、共 0 qualified；上限 R(C2–N18) ≈ 2.69 Å，且片段内几何刚性。
2. 若主协调愿意把早期进攻窗口放宽到 **R(C2–N18) ≈ 2.7 Å**，则 v1 的 closest_attempt（845a4bd9…，minsep 0.9794、接触全为正常键、H21 在 N 上）**在接触意义上干净**，可作 documented guess 候选；但它**不是** 2.1–2.5 Å 的早期进攻帧，也**不是鞍点**。
3. 门槛 ③（C2–O3 ≥ 1.30）在**任何**刚性片段方案下都不会满足；若必须满足，只能靠 QM/力场约束松弛（未授权、未执行）。
4. 本轮**未提交任何作业、未 ts_resume、未碰 ts/ts_0015/process.json**；E1a 仍未验证、ΔE‡ null。

### 34.4 v1 路径更正 + C2–O3 门槛勘误 + 候选帧 provenance（2026-10-17 15:2x 补）
- **v1 帧确实在盘**：路径是 `split/E1a_seed_search/closest_attempt.xyz`（**目录名为 E1a_seed_search，不带 _v1**），sha256 `845a4bd9908e1607e7ead78d17896912bf2bc874d0310f50bb399fb90e813435`；manifest `split/E1a_seed_search/guidance_manifest.json` sha256 `8a4e3ceae53d75a0d8d3faf55b9b1ea51967a21318b12fd573358d040a1aa508`。此前以「v1」称呼导致按 `E1a_seed_search_v1` 找不到。
- **C2–O3 门槛勘误（协调者原文方向写反）**：早期进攻帧应保持**羰基双键**（C2–O3 ≈ 1.22–1.28 Å）；>1.32 Å 才表示羰基已被提前变成单键。按更正后的读法，A/B/C 帧 **通过**门槛（1.2383 / 1.2327），D 亦通过（1.2321）⇒ 此前「刚性方案不可能满足门槛③」的说法**作废**。
- **候选帧 provenance 落盘**：`split/E1A_SEED_CANDIDATE_PROVENANCE.md` sha256 `2b37153e705c7f3d4b4b52ef0f7c456d15b1951297954d093d811c0a6bcc3394`，内容含：四次调用完整参数（窗口/num_confs/seed/energy_window）、四个 closest_attempt 与 manifest 的 sha、四个 run 的 measured 表（R(C2–N18) 2.6920/2.7508/2.7508/3.0481；R(N18–H21) 1.0349/1.0303/1.0303/1.0255；C2–O3 1.2383/1.2327/1.2327/1.2321；minsep 0.9794/0.9807/0.9807/0.9801；最紧三接触全为正常键）、**「力场层面 ≠ QM 面」显式声明**、**「片段间刚体摆放导致下限 ~2.69–2.75 Å」**、**「仅 guess、非鞍点」**、模型条件。
- 定性改为**工具能力边界**（不是「工具路径不可行」）：受导装配只在片段间做刚体摆放，达不到 2.2–2.5 Å 窗口，最好 2.69–2.75 Å。

---

---

---

---

---

---

## 43 裁定：空槽不构成提交理由，维持只读（协调侧 §R11.49；2026-10-17 记）

**零动作：未提交、未 ts_resume、未触碰 process.json / .pipeline.lock、未 kill、未改交付面。E1a 未验证，ΔE‡ = null，barrier 0/4，hi.py null。**

### 43.1 裁定要点（逐条登记）
1. **空槽不是闸门**：冻结依据是 §14 于 15:33 按 **partial** 结算并明确「此后不再接受新的提交」；资源余量不改变授权状态（否则等于用「机器闲着」绕过 freeze）。
2. 该作业属 **TS 相关计算**；本包纪律 = TS 只在 durable workflow 内推进，**管线外手工提交须主协调点名授权且逐项给定**；该授权**未转授**任何 lane。
3. E1a 的 documented next action（固定 R(C2–N18) 约束松弛 → ts_resume）列为**下一窗口**事项；本窗口只做追记。
4. 若主协调要破例，须其本人在主题帖写明**六项**（缺一项不转达为可执行）：①固定距离取值（建议 2.3–2.5 Å）；②opt 还是 opt+freq；③级别不变（B3LYP/def2SVP+GD3BJ+UltraFine+Tight+CPCM(DMSO)、q0/m1）；④资源 ≤8 cpu / ≤10,240 MB / priority 0；⑤产物标 **post-freeze asset**、**不得回填 E1a barrier**；⑥不改 §14 口径与交付面 11 文件。
5. 并行提示：1049 = EM1 下扫（scan point 9/12、Step 168/246）、1069 = E3b ts_opt（Step 80/239）；即便将来破例也不抢 slot（单作业 ≤8 cpu、priority 0、不重投）。
6. #197 记法固定为「**stage 间推进处特定挂起**」，**不得**写成「作业失败」或「输入被拒」；排除性证据 = rev 11 / blocked null / failed_attempt null / jobs 下仅 ts_opt。

### 43.2 协调侧台账
- 协调侧 STATUS.md：sha **`fe7ac6d1634a5afef2b54596486971042b832f1f716c5884eca35a94534aa0fb`**、**1,455 行**，裁定条目 **§R11.49**（作为本 lane 引用的权威出处）。

### 43.3 当前只读快照
- ts_inspect(ts_0015) {"rev":11,"stage":"refine","status":"waiting","result":null,"blocked":null}；process.json mtime 2026-10-17 18:23:07 CST
2026-10-17 14:36:37.092354393 +0800。
- 后续：仅只读轮询；frequency 若出现按模板出全并发协调者（只作追记），否则超时复检一行。
## 42 18:22 CST 只读复检：ts_0015 仍冻结；但出现空槽（不改变授权状态）

**零动作：未提交、未 ts_resume、未触碰 process.json / .pipeline.lock、未 kill、未改交付面。E1a 未验证，ΔE‡ = null，barrier 0/4。**
- ts_inspect(ts_0015) 18:22:19 CST：rev 11 / stage refine / status waiting / result null / blocked null；process.json 30,059 B mtime **14:36:37.092354393**（冻结 ~3 h 46 min）；`test -d …/frequency` 退出码 1，jobs/declaration_0001/ 仅 ts_opt/。
- `query_compute_queue` 18:22 CST：running **1049 / 1069**，queued 空，free **2 slots / 16 cpus / 30720 MB**；terminal 新增 1061 done 16:34:17、1068 done 16:33:45、1067 done 15:54:26、1059 done 15:42:09、1066 done 15:38:27。
- **授权状态不变**：§37.2 (b) 的例外条件是「第三个空槽 + E3b/NY3 皆不需 + **主协调点名授权一次**」，且交付已结算（§14 partial，「之后不再接受新的提交」）；本 lane **不**据空槽自行提交，已把空槽事实报给协调者由其裁定。
## 41 17:16 CST 只读复检（旧三号 reminder 超时唤醒）：ts_0015 仍冻结于 14:36:37

**零动作：未提交、未 ts_resume、未触碰 process.json / .pipeline.lock、未 kill、未改交付面。E1a 未验证，ΔE‡ = null，barrier 0/4，hi.py null。**
- ts_inspect(ts_0015) 17:15:36 CST：rev 11 / stage refine / status waiting / result null / blocked null；process.json 30,059 B mtime **14:36:37.092354393**（冻结 ~2 h 39 min）；jobs/declaration_0001/ 仅 ts_opt/，无 frequency/。
- reminder 清理：`schedule list` 显示仅剩 1 个待触发（第六轮，单条件 `test -d …/frequency`，18:31 到期），旧三号已触发消失；无需再新增。
- 口径不变（#197 追记），无新证据故不发协调者消息。
## 40 16:31 CST 巡检误触发（check 假阳性），ts_0015 仍未变

**零动作：未提交、未 ts_resume、未触碰 process.json / .pipeline.lock、未 kill。E1a 未验证，ΔE‡ = null。**
- 触发原因：定时 check（`test -e …/frequency -o -e …/frequency.log`）报 check_succeeded；实测 `jobs/declaration_0001/` 下**只有 `ts_opt/`**，`test -d …/frequency` 退出码非 0 ⇒ **该次唤醒为巡检命令假阳性，不是管线推进**。
- ts_0015 未变：rev 11 / stage refine / status waiting / result null / blocked null / waiting_for job 1055（done, evidence=null）；process.json 30,059 B mtime 14:36:37.092354393。
- 处置：巡检改用单条件 `test -d …/declaration_0001/frequency`（去掉 `-o` 组合，避免假阳性），继续只读轮询；无 frequency 证据故不发协调者消息。
## 39 16:31 CST 只读复检：ts_0015 仍冻结（第四轮，无新事实）

**零动作：未提交、未 ts_resume、未触碰 process.json / .pipeline.lock、未 kill、未改交付面。E1a 未验证，ΔE‡ = null。**
- ts_inspect(ts_0015)：rev 11 / stage refine / status waiting / result null / blocked null。
- 盘上：process.json 30,059 B mtime **14:36:37.092354393**、declare.json 4,100 B mtime 14:36:37.092596542、.pipeline.lock 0 B mtime 14:36:36.703767325；jobs/declaration_0001/ 仍只有 ts_opt/（fort.7, refine.gjf, refine.log, state_1055.json），**无 frequency/**。
- 冻结已持续 ~1 h 55 min；口径与 §36–§38 相同（#197「ts run 在 stage 间推进处特定挂起」），本条仅作追记。
## 38 16:20 CST 定时只读复检：ts_0015 仍冻结（无新事实）

**零动作声明：未提交作业、未调用 ts_resume、未触碰 ts/ts_0015/process.json 与 .pipeline.lock、未 kill、未改交付面。E1a 未验证，ΔE‡ = null，barrier 0/4，hi.py null。**

- `ts_inspect(ts_0015)` 16:19:51 CST：revision **11** / stage **refine** / status **waiting** / result **null** / blocked **null**；waiting_for 仍只有 job 1055（state=done, evidence=**null**, refine.log）。
- 盘上：`process.json` 30,059 B，mtime **2026-10-17 14:36:37.092354393**（自首报起未变，已持续 ~1 h 43 min）；`jobs/declaration_0001/` 只有 `ts_opt/`，**仍无 frequency/**。
- 结论：与 §36 / §37 一致，#197「ts run 在 stage 间推进处的特定挂起」继续，无新证据。按协调者口径（交付已结算 partial，报告 `a2964d8d…` §14），本条**仅作追记**，不改 §14、不回填 barrier、不补提交。
- 后续：继续每小时只读复检；仅当 frequency 阶段出现或 process.json 被写时按模板出全并报协调者。
## 37 裁定落定：documented guess = A 帧；本窗口不授权约束松弛；交付已结算 partial（2026-10-17 15:35 CST 记）

**声明：本轮零动作——未提交作业、未调用 ts_resume、未触碰 ts/ts_0015/process.json 与 .pipeline.lock、未 kill、未改交付面文件。E1a 仍未验证，ΔE‡ = null，barrier 0/4，hi.py null。**

### 37.1 (a) documented guess 定为 **A 帧**（主协调裁定，写入协调侧 STATUS §R11.31）
- 采用：`split/E1a_seed_search/closest_attempt.xyz`，sha256 `845a4bd9908e1607e7ead78d17896912bf2bc874d0310f50bb399fb90e813435`，manifest `c9098d91d1b34f5bb22bdd1ea91637a4d51017a9a9f5a2f0210871a624ad70e4`。
- 实测：R(C2–N18) **2.6920**、C2–O3 1.2383（羰基保留）、R(N18–H21) 1.0349、minsep 0.9794，最紧三接触全为正常化学键，元素序 27/27 与 refine 帧一致。
- 备选：B（`split/E1a_seed_search_v2/closest_attempt.xyz`，sha `9a5c9c3294834a8d344c66d77d5cc14122bf881c01b7606ae35d1b2267c067e9`，R 2.7508）。
- **五条口径同时成立（随帧同行）**：①力场来源 ≠ QM 面；②仅 guess、**非鞍点**；③落在 2.2–2.5 Å 早期进攻窗口**之外**；④**本窗口不提交、不采用**；⑤E1a 未验证、ΔE‡ null。

### 37.2 (b) 固定 R(C2–N18) 约束松弛：**本窗口不授权**
- 理由：0 空槽（running 1049/1059/1061/1064，free cpus 0）+ 优先级 E3b ts_opt > NY3。
- 例外条件（不由本 lane 触发）：仅当交付前出现**第三个空槽**且 E3b/NY3 都不需要时，由**主协调点名授权一次**。
- 且交付已结算（15:33 主协调落盘报告 §14，partial），**之后不再接受新的提交**。
- ⇒ 本 lane 不提交该约束松弛作业；此前「唯一可闭环路线未授权」的记录保持有效。

### 37.3 交付面（只读核对，未改）
- `gold_finish_20261015/FINAL_DELIVERY_DRAFT.md`：sha256 **`a2964d8d37aa3214fd03136b5a4d6d95a0e4a3b57c9465a6368c1e6b0cf230df`**、**277 行**（本 lane 用 `sha256sum`/`wc -l` 只读复核，与协调者给值逐字相同）；§14 为交付结论，结算 **partial**。
- HI1 四条新边：result = null、ΔE‡ missing、barrier **0/4**、hi.py **null** —— 未动。
- 口径：此后出现的任何管线读数（如 ts_0015 若有 frequency 字段）**只作追记**（协调侧 STATUS §R11.33 起），**不改 §14 口径、不改交付面、不回填 barrier**。

### 37.4 #197 口径（采纳并已转主协调）
「**ts run 在 stage 间推进处的特定挂起**」：依据 = 14:45 之后 daemon 仍能认领/收尾其他作业（1060 @15:05:22、1062 @15:11:29、1063 @15:18:14 done，1064 @15:19 起跑），而 ts_0015 在 ts_opt done 之后既不推进也不写失败、无 blocked/failure 记录；且非输入被拒（declare→…→ts_opt 全 done）。

### 37.5 ts_0015 只读快照（15:35:01 CST）
- `ts_inspect(ts_0015)`：revision **11** / stage **refine** / status **waiting** / result **null**；`process.json` 30,059 B mtime **14:36:37.092354393**（仍未再被写）。
- 后续仅只读轮询：若出现 frequency 阶段或 process.json 被写，按模板一次出全并发协调者（作为追记）；**不 ts_resume、不手工补频、不删锁、不 kill**。
## 36 15:34 CST 只读复检：#197 为 ts run 状态机特定停滞（非全局 daemon 停摆）

**声明：本轮未提交任何作业、未调用 ts_resume、未触碰 ts/ts_0015/process.json 或 .pipeline.lock、未杀进程。E1a 仍未验证，ΔE‡ = null。**

### 36.1 ts_0015（只读，1 h 定时巡检超时后复检）
- `ts_inspect(ts_0015)`：**revision 11 / status=waiting / stage=refine / waiting_for job 1055（state=done, evidence=null）/ result=null / blocked=null / required_inputs 空**，与 14:36 快照逐字段一致。
- 盘上：`process.json` 30,059 B，mtime **2026-10-17 14:36:37.092354393**（与首报同一 mtime，未再被写）；`jobs/declaration_0001/` 下**只有 ts_opt/**，无 frequency/；`.pipeline.lock` 仍为 0 B、mtime 14:36；`verdict/` 目录空。
- 已完成的证据链（available_results）：declare / build（两端 seed）/ map（27 atoms mapped）/ assemble（4 reaction-centre pair(s)）/ guess（provided）/ validate / **submit**（job 1055 as 'ready'）/ **ts_opt done（job 1055，refine.log）**，此后无任何 stage 记录。

### 36.2 关键新事实：调度器本身是活的
`query_compute_queue`（15:34 CST）：node-local online，in_flight 4 slots / 32 cpus / 40960 MB；running = **1049 / 1059 / 1061 / 1064**；queued 空；terminal 含 **1063 done 15:18:14、1062 done 15:11:29、1060 done 15:05:22、1055 done 14:45:42**，以及 **1058 failed 14:55:51（l9999 Error termination，非本 lane 作业）**。
⇒ 判决口径更新：daemon 能认领、运行、收尾其他 gaussian 作业（14:45 之后又有 1060/1062/1063 收尾、1064 起跑），但 ts_0015 在 **ts_opt stage=done 之后既未推进到 frequency、也未写 blocked/failure**，`process.json` 自 14:36:37 完全冻结。这支持「**#197 = ts run 状态机在 stage 间推进处的特定挂起**」，而不是全局调度器或计算节点故障，也不是本 lane 输入被拒（validate/guess/submit/ts_opt 全部 done）。
- 处置不变：本 lane 只读轮询、不 ts_resume、不手工补频、不删锁、不 kill；诊断归协调者。

### 36.3 科学状态（不变）
- E1a：无 qualified 单一鞍点。job 1055 收敛点（-593.873953336，ΔE vs RC_27 +38.01 kcal/mol）经 job 1062 频析为**纯质子转移**（-1551.2317 cm⁻¹；N20 份额 0.008 低于打印噪声、C2 0.053；最低实模 41.70 cm⁻¹ ≤ 50 ⇒ 软坐标）⇒ candidate_only，**不得**回填为 E1a ΔE‡。
- documented guess 候选：A（`845a4bd9…`，R(C2-N18) 2.6920）/ B（`9a5c9c32…`，2.7508）等四帧，provenance `split/E1A_SEED_CANDIDATE_PROVENANCE.md` sha256 `cb07019c196d6e759bc34945807784d4ff1437846d4134ef39898cfa7203363a`（含 §7 勘误）。选择权在协调者/主协调，本 lane 不自行选择。
- 唯一可闭环路线（固定 R(C2-N18) 约束松弛）**仍未授权、未提交**。
## 35 manifest sha 映射勘误（run A）+ 主协调复核结论（2026-10-17 15:2x CST 补）

**本条明确声明：本轮未提交任何作业、未调用 ts_resume、未触碰 ts/ts_0015/process.json；E1a 仍未验证，ΔE‡ = null，barrier 0/4，hi.py 保持 null。**

### 35.1 勘误（更正、非静默改）
- 主协调 15:22:00 CST 实测指出：§34.4 与 `split/E1A_SEED_CANDIDATE_PROVENANCE.md` §3 里把 run A 的 `guidance_manifest.json` sha 写成了 `8a4e3cea…`，而那实际是 **run B（`E1a_seed_search_v2`）** 的 manifest。
- 本 lane 用 `sha256sum` 在盘复核（同一实测）：
  - A：`split/E1a_seed_search/guidance_manifest.json` = `c9098d91d1b34f5bb22bdd1ea91637a4d51017a9a9f5a2f0210871a624ad70e4`（frame `845a4bd9908e1607e7ead78d17896912bf2bc874d0310f50bb399fb90e813435`）
  - B：`split/E1a_seed_search_v2/guidance_manifest.json` = `8a4e3ceae53d75a0d8d3faf55b9b1ea51967a21318b12fd573358d040a1aa508`（frame `9a5c9c3294834a8d344c66d77d5cc14122bf881c01b7606ae35d1b2267c067e9`）
  - C：`split/E1a_seed_search_v3/guidance_manifest.json` = `06e18dd537ca4b13efde023c873cce64348885745d9b0d9d860bd4a41d193150`（frame 与 B 同几何 `9a5c9c32…`）
  - D：`split/E1a_seed_search_v4/guidance_manifest.json` = `892f988ecb534972719aae1895fd0654e31243510888a163a0d233564286f803`（frame `aa6fc0a05b7ac2cca807b55f1fd7d41505e9891ae670f38a680b343bedfda71e`）
- provenance 已就地更正 A 行并新增 §7 勘误段：`split/E1A_SEED_CANDIDATE_PROVENANCE.md` sha256 由 `2b37153e705c7f3d4b4b52ef0f7c456d15b1951297954d093d811c0a6bcc3394` → **`cb07019c196d6e759bc34945807784d4ff1437846d4134ef39898cfa7203363a`**。A 帧几何/距离/能量/结论均未变。

### 35.2 主协调复核与裁定（逐条记录）
1. A 帧复核**通过**（27 原子、元素序 27/27 与 refine 帧一致、R(C2–N18) 2.6920、R(N18–H27) 1.0349、C2–O3 1.2383、O3–H27 2.2993，最紧三接触皆为正常化学键）；主协调 STATUS §R11.30 已就「找不到 A 帧」作勘误（其 glob 了不存在的 `E1a_seed_search_v1/*`）。
2. 「四次 0 qualified ⇒ 无 ensemble、改以 closest_attempt + guidance_manifest 双 sha 表示」的处理被确认**正确**。
3. 主协调裁定不变：documented guess **暂取 B（2.7508 Å）**、不放进 2.1–2.5 Å 窗口；E1a 表述统一为「QM 闭环需固定 R(C2–N18) 约束松弛、本窗口未执行」；A（2.6920）更接近窗口且同样干净，是否改选 A 由主协调决定，**本 lane 不自行选择**。
4. 本 lane 纪律：**不得提交、不得 ts_resume**（本轮遵守）。

### 35.3 ts_0015 只读快照（未干预）
- `ts_inspect(ts_0015)`：revision 11 / status=waiting / stage=refine / waiting_for job 1055（state=done, evidence=null）/ result=null / blocked=null；无 frequency 阶段产物。与 14:36 记录一致 ⇒ 平台 #197 停滞仍在，诊断归协调者，本 lane 仅只读轮询。

> **编排提示（2026-10-17 18:2x 补，非内容更正）**：§35–§43 是按「插入到文末分隔线之前」的方式逐次追加的，因此在本文件中实际呈**倒序**排列（§43 最靠前、§35 最靠后，§34.4 位于其上）；小节编号与日期为准，内容未变。各节 shas 已分别报给协调者。

## 44 追加约定：不重排、今后一律写到文件末尾（协调裁定；2026-10-17 18:3x CST）

**零动作：未提交、未 ts_resume、未触碰 process.json / .pipeline.lock、未 kill、未改交付面。E1a 未验证，ΔE‡ = null，barrier 0/4，hi.py null。**
- 裁定：**不做正序重排**，保持 §35–§43 现状（各节 sha 已被多方引用；重排只变更全文 sha 而无信息增益，反而使「某节属于哪个 sha 版本」难核）；文末「编排提示」保留即可。
- 新约定：**今后追加一律写到文件最末**（若文件以 `---` 分隔行结尾，则写在其之后），不再插在分隔行之前；本条即为该约定的第一次执行（本节位于文件最末）。
- 其余收条无异议：破例六项前置条件、#197 记法「stage 间推进处特定挂起」（不写失败/输入被拒）、并行不抢槽（1049 = EM1 下扫、1069 = E3b ts_opt）、零动作声明、E1a barrier null、hi.py null。
- 协调侧 STATUS.md 现值 **`fe7ac6d1634a5afef2b54596486971042b832f1f716c5884eca35a94534aa0fb` / 1,455 行**（§R11.49 为该裁定；协调侧重在避免再次变更被引用的 sha）。
- 只读快照沿用 18:23 口径：rev 11 / stage refine / status waiting / result null / blocked null / process.json mtime 2026-10-17 14:36:37.092354393 / jobs 下仅 ts_opt；继续只读轮询。

## 45 点名授权执行：E1a 约束松弛扫描 **job 1070** 已提交并在运行（post-freeze asset）

**授权出处**：主协调 2026-10-17 18:23:29 CST 主题帖点名（topic gold-finish-20261015, post evt_ce0c45a76817431d；协调者转发同一范围）。范围 = **仅 1 个** Gaussian 作业，purpose = 约束松弛扫描（opt=modredundant，**无 freq**），**不是** TS/IRC 提交。

### 45.1 提交事实
- 作业：**job_id 1070**，state=ready→**running**（18:24:32 CST 实测 log 632 行 / 40,605 B，chk 已在写）；node=node-local，**8 cpus / 10,240 MB / priority 0**；并发 3（1049 EM1 下扫、1069 E3b ts_opt、1070 本作业），queued 空。
- 输入文件：`gold_finish_20261015/HI1/E1/split/E1A_constrained_scan_R2692_2192.gjf`，**sha256 `95bbbe6469e97da9a380f6a88782c881cc32892b1e9fc7232e4a37b81b883981`**，1,708 B / 38 行。
- route 首行逐字：`#p opt=modredundant B3LYP/def2SVP empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=dmso)`；`%nproc=8` / `%mem=10GB`；q0/m1。
- 扫描段（文件末，其前后均为空行）：`B 2 18 S 10 0.0500`（1-based，2=C2、18=N20；自 2.6920 Å 起 11 点至 2.1920 Å）。
- 种子几何核验（27 原子，元素序与 refine 帧一致）：R(2,18)=**2.6920**、R(2,3)=**1.2383**（羰基双键保留）、R(18,27)=1.0349、R(3,27)=2.2993、minsep **0.9794**（13–19，羧基 O–H），最紧三接触 13–19 0.9794 / 18–27 1.0349 / 1–7 1.0926（全为正常化学键）。
- **种子路径偏差（需记录，不改内容）**：授权文写的是 `HI1/E1/split/E1A_seed_candidate_A.xyz`，该文件名**在盘不存在**；本作业用的是**逐字节相同**的 `split/E1a_seed_search/closest_attempt.xyz`（sha256 `845a4bd9908e1607e7ead78d17896912bf2bc874d0310f50bb399fb90e813435`，与授权给的 sha 一致）。

### 45.2 工具边界（qm_input_writer，需报平台）
- 直接声明 `task_type=[{"opt":"modredundant"}]` + `end_setting="B 2 18 S 10 0.0500"` → **internal mismatch**：`generated file encodes tasks ['relaxed_scan'] but ['minimum_opt'] were requested; no file was written`（call 无副作用）。
- `task_type=[{"scan":"relaxed"}]/{"scan":"relaxed_scan"}/{"opt":"modredundant"}+{"scan":"relaxed_scan"}` → 一律被拒：`a Gaussian 'scan' task writes the bare scan route, which is a RIGID potential-surface scan`。
- 可行绕法（本作业采用，已自证）：先用 qm_input_writer 生成 `#p opt` 的 gjf（坐标由工具写入，**未手写坐标**），再用 edit 做两处文本改动：① route 的 `opt` → `opt=modredundant`（级别/泛函/基组/关键词一字未动）；② 在几何段末空行之后追加 `B 2 18 S 10 0.0500` 并保留**文件末尾空行**（避免 l101 End of file in ZSymb）。diff 显示坐标块**未被改动**。
- 未与 cartesian / z-matrix 混用（仅 opt=modredundant）。

### 45.3 口径与不变项
- 产物身份：**post-freeze asset / non-delivery evidence**；**E1a barrier 保持 null**，不回填；不改 `FINAL_DELIVERY_DRAFT.md`（a2964d8d…，277 行）、§14 结论与 11 个交付文件 sha。
- 判读纪律（已登记待用）：扫描内极大只作 **TS 候选/下界**，不是 ΔE‡；每点须 `Optimization completed`；逐点 minsep ≥0.90（不足或靠碰撞换距离的点作废、不入表、不作 guess）；C2–O3 须保持 1.22–1.28 Å，>1.32 判不合格；l103（FormBX/Bend/Tors）或 NStep 只登记失败类别+行号+id，**不写「无鞍点/通道不存在」**。
- 边界：不 ts_resume、不碰 ts/ts_0015/process.json 与 .pipeline.lock、不动 ts_0016、不改交付面；ts_0015 仍按 #197「stage 间推进处特定挂起」只读巡检。

## 46 协调者独立核对通过 + 1070 实时进度（2026-10-17 18:25 CST）

**零新增动作：本轮未提交新作业（仅 1070 在跑）、未 ts_resume、未触碰 process.json / .pipeline.lock、未 kill、未改交付面。**

### 46.1 协调者独立核对（18:24:55 CST，全部成立）
- gjf sha256 `95bbbe64…`、38 行 / 1,708 B ✓；route 首行逐字一致、**freq 关键字计数 0** ✓；尾部 od -c 实读为 `\n\n B 2 18 S 10 0.0500 \n\n`（文件以两个换行结尾）⇒ l101 门禁满足 ✓。
- 种子自算（27 原子）：R(2,18)=2.6920、R(2,3)=1.2383、R(18,27)=1.0349、R(3,27)=2.2993、R(2,4)=1.5071；minsep 0.9794（13–19 为**成键** O–H）；最紧三个**非键**接触 25–26 1.7726 / 5–6 1.7741 / 9–10 1.7742 ⇒ 确认「没有靠碰撞换距离」。
- 作业：1070 running，started 18:24:26，8 cpus / 10,240 MB / priority 0；队列 1049+1069+1070（并发 3）。

### 46.2 种子路径偏差：**不需更正记录**
协调者复核 `split/E1A_seed_candidate_A.xyz` 确实不存在，而所用 `split/E1a_seed_search/closest_attempt.xyz` sha256 = 845a4bd9… 与授权 sha 逐字符一致 ⇒ 种子身份无歧义，按授权执行。§45.1 中该条保留为「文件名偏差、身份无歧义」的事实记录，不再追加入更正。

### 46.3 工具边界
协调者认可绕法（writer 生成 `#p opt` → 仅改 route `opt`→`opt=modredundant` + 追加扫描行 + 保留末尾空行，坐标块不动），将作为**工具约束**上报主协调、不进化学判读。

### 46.4 1070 实时进度（18:25:27 CST，只读）
- 日志 2,381 行；**scan point 1 / 11**，`Step number 2 out of a maximum of 150 on scan point 1 out of 11`（L1887）；`Optimization completed` 计数 **0**（尚无完成点，符合预期）。
- 已见 SCF Done：L806 `-593.925164675`、L1813 `-593.930533479`。
- 判读纪律（双方一致）：逐点须 Optimization completed；逐点 minsep ≥0.90；C2–O3 须 1.22–1.28 Å（>1.32 不合格）；扫描内极大只作 TS 候选/下界（非 ΔE‡）；l103/NStep 只登记失败类别+行号+日志 sha。**E1a barrier 仍 null**。

## 47 **job 1070 完成，但扫描方向与授权意图相反（执行错误，我方）** + 逐点表（2026-10-17 19:07 CST）

**零新增动作：未提交新作业（1070 是唯一放行作业，已终止）、未 ts_resume、未触碰 process.json / .pipeline.lock、未 kill；E1a barrier 仍 null、未回填；交付面未动。**

### 47.1 终止与方向错误（必须先说）
- 日志：`E1A_constrained_scan_R2692_2192.log`，**sha256 `4b89f194547f5308f8387dfef9fc61e5d14f7b7ed237e16c75be4a3821165625`**，**65,854 行**。
- 终止行（逐字，**L65854**）：` Normal termination of Gaussian 16 at Sat Oct 17 19:07:04 2026.`
- **11/11 点均 `Optimization completed.`**（L24969 / 29769 / 33849 / 39210 / 42664 / 46175 / 49658 / 53107 / 57854 / 61330 / 64778）；**无** FormBX / Bend failed / Tors failed / NStep / Convergence failure（`l103.exe` 命中全部是正常 link 调用行）。
- **方向错误（我方执行问题）**：Gaussian `S` 段**正步长 = 距离递增**，故 `B 2 18 S 10 0.0500` 实际走 **2.69195 → 3.19195 Å（解离方向）**；授权要求的 **2.6920 → 2.1920 Å（进攻方向）并未执行**。证据：L203 `! R7 R(2,18) 2.692 Scan !` 与扫描汇总表 L64937 `R7 2.69195 2.74195 2.79195 2.84195 2.89195 …`（单调递增）。gjf 标题里写的 `2.6920->2.1920` 与实际不符，属我方标注错误。**重跑需新的点名授权**（本窗口仅放行 1 个作业，我不自行重投）。

### 47.2 逐点表（1-based 工作序：2=C2、3=O3(羰基 O)、18=N20、27=H21；E 取该点最后 `SCF Done`）
| 点 | R(C2–N18) | E(RB3LYP) | SCF L | ΔE vs RC_27(−593.934532807) | R(C2–O3) | R(N18–H27) | R(O3···H27) | minsep |
|---|---|---|---|---|---|---|---|---|
| 1 | 2.6920 | −593.932802613 | 24681 | +1.09 kcal | 1.2193 | 1.0148 | 2.5541 | 0.9741 (13–19) |
| 2 | 2.7420 | −593.933044241 | 29494 | +0.93 | 1.2189 | 1.0147 | 2.5515 | 0.9741 |
| 3 | 2.7920 | −593.933233254 | 33575 | +0.82 | 1.2186 | 1.0146 | 2.5368 | 0.9741 |
| 4 | 2.8420 | −593.933379443 | 38927 | +0.72 | 1.2184 | 1.0146 | 2.5252 | 0.9741 |
| 5 | 2.8920 | −593.933487052 | 42394 | +0.66 | 1.2182 | 1.0146 | 2.5185 | 0.9741 |
| 6 | 2.9420 | −593.933556954 | 45905 | +0.61 | 1.2181 | 1.0147 | 2.5223 | 0.9741 |
| 7 | 2.9920 | −593.933586753 | 49388 | **+0.59（最低）** | 1.2180 | 1.0148 | 2.5258 | 0.9741 |
| 8 | 3.0420 | −593.933584863 | 52837 | +0.59 | 1.2179 | 1.0148 | 2.5357 | 0.9741 |
| 9 | 3.0920 | −593.933543229 | 57575 | +0.62 | 1.2178 | 1.0149 | 2.5650 | 0.9741 |
| 10 | 3.1420 | −593.933469960 | 61060 | +0.67 | 1.2177 | 1.0150 | 2.5973 | 0.9741 |
| 11 | 3.1920 | −593.933364490 | 64508 | +0.73 | 1.2177 | 1.0151 | 2.6338 | 0.9741 |
（换算 1 Eh = 627.5095 kcal/mol；ΔE 仅为**同一 Gaussian 批内**纯电子差。）

### 47.3 判读（按既定纪律）
- **本扫描方向（解离侧，2.69→3.19 Å）无内部极大**：能量自 2.692 Å 的 +1.09 kcal 单调下降至 2.99 Å 的 +0.59 kcal（pt7），之后基本平坦（3.19 Å 为 +0.73）⇒ **该方向不产生 TS 候选**，也不构成任何 ΔE‡；**不得**写成「通道不存在」。
- 只有「趋向更短 R」的斜率信息：2.99 → 2.69 Å 上升 **+0.49 kcal/mol**（pt1−pt7），即向进攻方向继续缩短应当继续上升（未测量）。
- **C2–O3 = 1.2177–1.2193 Å**：羰基双键保持（与 RC_27 的 1.2195 一致；若已成单键应为 ~1.42，参见 INT1_27 的 1.4208）。**注**：数值比授权门的 1.22 下界低 0.002–0.002 Å，属门的读数粒度问题而非化学异常 → 按「保留双键」判合格，>1.32 的不合格判据未被触及。
- **N18–H27 = 1.0146–1.0151 Å**：质子仍在 N 上，扫描过程中**无质子转移**。
- **逐点 minsep = 0.9741 Å（13–19，羧基 O–H 成键）**，全部 ≥0.90；最紧非键接触 18–27（N–H 成键）1.0148、15–22 1.0975 ⇒ **没有靠碰撞换距离的点**，11 点全部入表。

### 47.4 导出帧（post-freeze asset / non-delivery evidence）
- `E1A_scan_p1_R2692_QMrelaxed.xyz`，**sha256 `2984d326d3125aa613899600511c94bb377fc685a2d077e3f8acc8ea7fb7c25e`**，27 原子（QM 弛豫后的 2.6920 Å 帧，源点 1 收敛几何，log 方向块起始行 24461 / 结束 24492）。
- 五项距离：**R(C2–N18)=2.6920**、**R(C2–O3)=1.2193**、**R(N18–H27)=1.0148**、R(O3···H27)=2.5541、最近两非键接触 15–22 1.0975 与 1–5 1.0980（另 4–9 1.0981）；minsep 0.9741（13–19 成键）。
- 定位：仅在**获得新的进攻方向授权后**才可能作为 guess 的一环使用；当前**不是guess 结论、不是鞍点**。

### 47.5 脚本（可复现，均落在 split/scripts/）
- `scripts/e1a_scan_table.py` sha256 `fc3ff4b929b186210043c2b34b3e733d15859f896f745da9daa003e21299c02a`（逐点表：按 `on scan point k out of 11` 与 `Optimization completed.` 配对，取该点末个 orientation 块算距离）。
- `scripts/extract_scan_frame.py` sha256 `a83ff28bc959fa9deb1f7d6f94c73fb0ed0eb15cae06bcfd89bad00a003c448c`（导出指定点收敛帧为 xyz，并打印自检：27 原子、五项距离、minsep、最紧四接触）。

### 47.6 强制补注（协调者要求，逐字登记；本节位于文件末尾但仍属 §47 系列）

1. **方向错误与标题不符（防误引）**：job 1070 的 gjf 标题写的是 `R(C2-N18) 2.6920->2.1920`（进攻侧），而**实跑为 2.69195 → 3.19195 Å（解离侧）**，原因是 Gaussian `S` 段的**正步长 = 距离递增**。⇒ **该标题不得被当作扫描方向或意图的证据引用**；方向只以 log L203 `! R7 R(2,18) 2.692 Scan !` 与扫描汇总表 L64937 的递增序列为准。
2. **使用禁令**：本扫描（无论已跑的解离侧或将来若获授权的进攻侧）**不得用于任何 C2–N18 能垒或 TS 存在性陈述**；E1a barrier 仍为 **null**。
3. **导出帧三重标注**：`E1A_scan_p1_R2692_QMrelaxed.xyz`（sha256 `2984d326d3125aa613899600511c94bb377fc685a2d077e3f8acc8ea7fb7c25e`）= **post-freeze asset / non-delivery evidence / 非 guess / 非鞍点**。
4. **C2–O3 门值的措辞（原样写入，防误读）**：逐点 **C2–O3 = 1.2177–1.2193 Å 与 RC_27 的 1.2195 Å 属同一化学态（C=O）**；门值 1.22 是**读数粒度**，不是异常——**不得**把 1.2177 读作「低于门限的反常」。

## 48 裁定落地 + 第 4 项（零提交 pose 对照）交付（2026-10-17 19:2x CST）

**零动作：未提交作业、未 ts_resume、未触碰 ts/ 下任何文件、未 kill、未改交付面；E1a barrier 仍 null。**

### 48.1 裁定 (a)：本窗口**不放行重跑**
协调者理由（按先后，逐条登记）：① 主协调 18:23:29 的点名授权是「**1 个**」约束松弛扫描，job 1070 已消耗该授权，重跑属新提交，须主协调**重新点名放行**，协调者不代传、不扩权；② 并发 3/4（1049 / 1069 / 1071 在跑，free 8 cpus / 7 slots）不是硬阻塞，但 1069、1071 的终态是 E3b 方向确认的更高优先读数，不在本窗口用掉第 4 个槽；③ 交付已 partial 冻结（报告 a2964d8d… / 277 行 / 11 文件 sha），负步长扫描即使出峰也只能是 post-freeze asset。**是否补做 1 个 `B 2 18 S 10 -0.0500` 已由协调者升级请示主协调；本 lane 不自行提交。**

### 48.2 裁定 (b)：现状定档（同意）
- E1a 定档 = **无可用 guess、无 TS 候选、barrier = null**；job 1070 整条只作追记；`E1A_scan_p1_R2692_QMrelaxed.xyz` 按 §47.6-3 三重标注。

### 48.3 第 4 项成果：ts_0015 起点 / guess pose 对照（只读）
- 文件：`gold_finish_20261015/HI1/E1/split/E1A_TS0015_SEED_POSE_COMPARISON.md`，**sha256 `1a2f3189b0750f03180af47cc05b570f336433d5584744c802c7687815e0e65a`**，**65 行**。
- 脚本：`split/scripts/e1a_pose_compare.py`，**sha256 `4924148c8f5171337e8dfd340af3b4c2999b682930062b9c1ae7e0c725d0311f`**（纯 python + numpy，Kabsch/SVD，自带原子数与元素序断言）。
- 关键读数（工作序 1-based；S = job1070 点 1 QM 帧，G = ts_0015 `provided.xyz`，R = ts_0015 reactant seed）：
  - **R(C2–N18)**：S 2.6920 / G **1.6325** / R 3.7571；**R(C2–O3)**：S 1.2193 / G **1.3616** / R 1.2195；**R(N18–H27)**：S 1.0148 / G **1.2262** / R 1.0228；**R(O3···H27)**：S 2.5541 / G **1.3336** / R 2.0299；R(13–19) 羧基 O–H：0.9741 / 0.9749 / 0.9737；**minsep**：0.9741 / 0.9749 / 0.9737（均为 13–19 成键）。
  - Kabsch：S↔G 全 27 原子 RMSD **2.004 Å**（重原子 12：1.508 Å；最大位移 3.735 Å，原子 21）；S↔R 1.925 / 1.333 Å；G↔R **2.430 / 1.877 Å**。
  - **观察结论（仅观察）**：三帧同物种、元素序逐位相同 ⇒ identity 映射 1..27；**ts_0015 的 reactant endpoint 就是 RC_27 复合物**（R = RC_27_opt_frame，c1f789e0…），但其 **TS 初猜 G 不是早期进攻 pose**（C–N 已成键、C–O 带单键特征、质子在 O/N 间桥接），与 S 不是同一 pose，且与 R 距离更大。
- 明示：该报告**不得用于任何 C2–N18 能垒或 TS 存在性陈述**；模型条件 = 27 原子（脯氨酸 + 丙酮）+ CPCM(DMSO)，无显式溶剂/抗衡离子/外加碱，苯甲醛不在模型与分母中。

## 49 口径更正（−1551 cm⁻¹ 性质的再定位）+ 负步长扫描 job 1072 已提交（2026-10-17 19:14 CST）

**声明：本轮仅提交授权内的 1 个负步长扫描（job 1072），未 ts_resume、未 ts_prepare、未碰 ts/ 下任何文件、未 kill、未调 priority、未改交付面；E1a barrier 仍 null，hi.py null 不动。**

### 49.1 更正：job 1055/1062 的 −1551.2317 cm⁻¹ **不得**再当"协同"证据（依据：G 帧 + 主协调 19:13:23 复核）
- 更正要点（**本条优先于此前任何冲突表述**）：
  1. 该 1 虚频（job 1062：H27 占 79.7%、δR(C2–N18)=+0.014 属噪声）**起点已经是 C–N 成键态**（G 一类结构），因此它**只是"已成键物种内的质子转移鞍点"**；
  2. **不得**再引用它作为"**C–N 成键 + 质子转移协同**"的证据；
  3. E1a 的"协同加成"在本模型中只能写成 **"声明步骤、未验证"**，不是已确立事实。
- 依据（可复核）：
  - G 帧 `ts/ts_0015/path/input_0001/provided.xyz` sha256 **`3c48099cf8e77f2bad7a5379901a23ab68503bdedc620955ae18f1ce0ad91a40`**，27 原子，实测 C2–N18 **1.6325** / C2–O3 **1.3616** / N18–H27 **1.2262** / O3···H27 **1.3336**（与本 lane `E1A_TS0015_SEED_POSE_COMPARISON.md` sha `1a2f3189…` 的读数逐位一致）；
  - 主协调 19:13:23 CST 独立复核同一 sha 并据此下更正。
- 三 pose 共识口径（可直接引用协调者 PROCESS.md 19:30 条目）：**R** = 松散复合物（C2–N18 3.7571）/ **S** = 扫描点 1 QM 帧（2.6920，羰基保留）/ **G** = 已成键 + 羰基转单键 + 质子桥接（1.6325），三者是**同一物种的三个 pose**。
- 本条为**更正**，不删除 §32 等历史记录；凡与其冲突的旧措辞以本条为准（§32 原记"纯质子转移"的定性方向与本条一致，但当时未点明其**起点已成键**这一前提）。

### 49.2 负步长扫描：job 1072（E1a 最后一次算力授权）
- 授权出处：主协调 2026-10-17 19:0x 主题帖（topic gold-finish-20261015, post `evt_5d43497eedf04ce5`）+ 协调者 19:1x 转达；**仅 1 个作业**，扫描段 `B 2 18 S 10 -0.0500`（**负号**），2.6920 → ≈2.1920。
- 输入：`split/E1A_constrained_scan_R2692_2192_stepneg.gjf`，**sha256 `7f943ec9a1b619319763d17173d722cc0fef4514145f8ba81444fda1e4f1553d`**，38 行，%nproc=8 / %mem=10GB，q0/m1。
- route 首行逐字：`#p opt=modredundant B3LYP/def2SVP empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=dmso)`；`freq` 计数 0；**无 cartesian / z-matrix**。
- 尾部实读（awk 行号）：L35 末原子行 / L36 空行 / **L37 `B 2 18 S 10 -0.0500`** / L38 空行（`od -c` 末两字节为 `\n\n`）。
- 标题与实际方向一致：`HI1_E1a constrained relaxation scan R(C2-N18) 2.6920 -> 2.1920, step -0.0500`。
- 种子：`split/E1a_seed_search/closest_attempt.xyz`（sha `845a4bd9…`）；自算 R(2,18)=**2.6920**、R(2,3)=1.2383、R(18,27)=1.0349、minsep 0.9794。
- **提交**：**job_id 1072**，local 后端，提交后 state ready → **running**（19:12:48 实测 log 743 行；19:14:06 已 2,503 行），8 cpus / 10,240 MB / priority 0；队列 running = 1049 / 1069 / 1071 / 1072（4 槽满）。
- 早期几何实算（脚本 `split/scripts/scan_point_geometry.py` sha `de513ccb8fe6c45bc3f9e24d7c67cdada808e58a4b45197f50fd40d2f6c5c38f`）：
  - 输入块（L345/L478）：R(2,18)=2.6920、R(2,3)=1.2383、R(18,27)=1.0349；
  - 扫描点 1 初期（L1366/L1500）：R(2,18)=**2.6920 固定**、R(2,3)=1.2221、R(18,27)=1.0197、minsep 0.9752；
  - 扫描点 1 第 2 步（L2090/L2224）：R(2,3)=**1.2154**、R(18,27)=**1.0136**、R(3,27)=2.3685、minsep 0.9730 ⇒ 羰基未提前单键化、质子未迁移（均在前置判据内）；点 2 尚未出现（`Optimization completed` 计数 0）。
- 待办：点 2 出现后立即核 **R(2,18) 递减**（不足则按纪律只登记上报）；终态后出逐点表（R(2,18) / E / SCF 行号 / ΔE vs RC_27 −593.934532807 / C2–O3 / N18–H27 / O3···H27 / minsep + 成键/1-3/非键三行分类）、首末点实算 R、脚本 sha；产物标 post-freeze asset / non-delivery evidence / 非 guess / 非鞍点。

## 50 **job 1072（负步长 / 进攻侧）终态：11/11 点收敛，但 4→5 点发生构象跳变，剖面分两支**（2026-10-17 20:27 CST）

**零新增提交：本轮未提交任何作业（1072 已自然终止）、未 ts_resume、未 ts_prepare、未碰 ts/ 下文件、未 kill、未重投、未改交付面。E1a barrier 仍 null。**

### 50.1 终止与完整性
- 日志 `E1A_constrained_scan_R2692_2192_stepneg.log`，**sha256 `359937d48b16036a2626ff751e3f759808e34c18ef6e3b1bfcb27e42ecf181dc`**，**91,682 行**。
- 终止行（逐字，**L91682**）：` Normal termination of Gaussian 16 at Sat Oct 17 20:26:25 2026.`
- `Optimization completed` 计数 **11/11**：L24969 / 29112 / 33240 / 38672 / 66240 / 72390 / 77262（此行原文 **"Optimization completed on the basis of negligible forces."**）/ 80097 / 83584 / 87083 / 90606。
- **无** FormBX / Bend failed / Tors failed / NStep / Convergence failure（grep 空）。

### 50.2 逐点表（1-based 工作序；E 取该点末 SCF；ΔE 为同批纯电子差 vs RC_27 = −593.934532807；1 Eh = 627.5095 kcal/mol）
| 点 | 实算 R(C2–N18) | 目标 R | 实际−目标 | E(RB3LYP) | SCF L | ΔE (kcal) | C2–O3 | N18–H27 | O3···H27 | minsep | OPT |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 2.6920 | 2.6920 | −0.0000 | −593.932802613 | 24681 | +1.09 | 1.2193 | 1.0148 | 2.5541 | 0.9741 | ✓ |
| 2 | 2.6420 | 2.6420 | −0.0000 | −593.932494720 | 28841 | +1.28 | 1.2198 | 1.0149 | 2.5509 | 0.9741 | ✓ |
| 3 | 2.5920 | 2.5920 | −0.0000 | −593.932110026 | 32966 | +1.52 | 1.2203 | 1.0149 | 2.5611 | 0.9741 | ✓ |
| 4 | 2.5420 | 2.5420 | −0.0000 | −593.931626202 | 38393 | +1.82 | 1.2210 | 1.0151 | 2.5575 | 0.9741 | ✓ |
| 5 | 2.4920 | 2.4920 | −0.0000 | −593.933356408 | 65949 | **+0.74** | 1.2225 | 1.0154 | **3.1497** | 0.9745 | ✓ |
| 6 | 2.4420 | 2.4420 | −0.0000 | −593.932746685 | 72109 | +1.12 | 1.2235 | 1.0155 | 3.1012 | 0.9745 | ✓ |
| 7 | 2.3920 | 2.3920 | −0.0000 | −593.932011719 | 76985 | +1.58 | 1.2247 | 1.0156 | 3.0616 | 0.9745 | ✓（negligible forces） |
| 8 | 2.3420 | 2.3420 | −0.0000 | −593.931146012 | 79827 | +2.13 | 1.2261 | 1.0158 | 3.0243 | 0.9745 | ✓ |
| 9 | 2.2920 | 2.2920 | −0.0000 | −593.930148430 | 83313 | +2.75 | 1.2278 | 1.0159 | 2.9870 | 0.9745 | ✓ |
| 10 | 2.2420 | 2.2420 | −0.0000 | −593.929020805 | 86812 | +3.46 | 1.2297 | 1.0161 | 2.9478 | 0.9745 | ✓ |
| 11 | 2.1920 | 2.1920 | −0.0000 | −593.927767693 | 90335 | +4.25 | 1.2319 | 1.0163 | 2.9100 | 0.9745 | ✓ |

- **约束生效断言**：11 点 |实际−目标| 最大值 **4.8×10⁻⁵ Å**（≤0.002 ✅）；首点实算 **2.69195**（2.6920±0.002 ✅）、末点实算 **2.19195**（2.19±0.01 ✅）。
- **停手条件复核（按每点收敛帧）**：C2–O3 = 1.2193–1.2319 Å，**全部 ≤1.32**（无提前单键化）；N18–H27 = 1.0148–1.0163 Å，**全部 ≪1.10**（质子始终在 N 上）。均未触发。注：点 1/2 的 1.2193/1.2198 比 1.22 下界低 ≤0.0007 Å，按协调者口径属**羰基平衡值读数**（RC_27 = 1.2195），不作异常。
- **最紧接触三分类**（每点）：成键 **0.9741–0.9745（13–19 羧基 O–H）**；1-3 距离 1.7715–1.7753（点 1–4 为 25–26，点 5–11 为 23–24 或 25–26）；非键最小 **2.1920–2.2846**（点 1–4 为 13–27；点 5–9 为 25–27；点 10–11 即被扫描的 2–18 对）⇒ 非键 ≥1.20 全部合格，minsep ≥0.90 全部合格。

### 50.3 关键发现：**点 4 → 点 5 发生构象跳变**（剖面分两支，不能当连续路径）
- 相邻点重原子（12 个：1,2,3,4,11–18）Kabsch RMSD：点 1→2 **0.030**、2→3 0.051、3→4 0.035，而 **4→5 = 0.759 Å**（最大单原子位移 **1.129 Å，原子 13**），此后 5→6…10→11 又回到 0.022–0.029 Å。
- 二面角证据：**O3–C2–N18–C14** 由点 4 的 **+139.0°** 翻到点 5 的 **−152.9°**（此后 −154.7…−160.0 平滑变化）；C2–C3–C14–N18 由 −67.2° → −21.9°；N18–C14–C15–C16 由 27.5° → 38.6°。
- 接触证据：**O3···H27 由 2.557（点 4）跳到 3.150 Å（点 5）**，即 N–H···O=C 弱氢键在跳变后消失；同时 1-3 接触由 25–26 变为 23–24。
- 能量证据：E 在点 4→5 之间**跳降 1.08 kcal**（+1.82 → +0.74），这是构象分支切换，不是势垒穿越。
- ⇒ 两支各自的趋势：**支 A（点 1–4）随 R 减小单调上升 +1.09 → +1.82 kcal**；**支 B（点 5–11）随 R 减小单调上升 +0.74 → +4.25 kcal**。序列上的点 4（相对点 3、点 5 局部最高）**是构象跳变的假象，不是鞍点，不作 TS 候选**。

### 50.4 结论（按约定措辞）
- **进攻侧亦无内部极大**（两条构象支内 E 均随 R 减小单调上升；点 4 的局部高点由 4→5 构象跳变造成，非势垒）；**纯 C–N 拉伸不是该步的反应坐标**；E1a 需**耦合 C–N 与质子转移的构造性 guess（下一窗口）**。
- **不写「通道不存在」**；**E1a barrier 保持 null**；本扫描任何数值不得作 ΔE‡。

### 50.5 导出产物（post-freeze asset / non-delivery evidence / 非 guess / 非鞍点）
| 文件 | sha256 | 说明 |
|---|---|---|
| `E1A_neg_scan_p4_R2542_branchA.xyz` | `f1ff21307918afaa6afa921f244969122b40f94183883d01bc2a232f4d8055e2` | 29 行 / 27 原子；支 A 最深点（R=2.5420，C2–O3 1.2210，N18–H27 1.0151，minsep 0.9741） |
| `E1A_neg_scan_p11_R2192_branchB.xyz` | `746c009a50d0041fead969e1fb7d8a419181b554e34ddd0b67c2211893b45b5a` | 29 行 / 27 原子；末点（R=2.1920，C2–O3 1.2319，N18–H27 1.0163，minsep 0.9745） |

### 50.6 脚本（可复现）
- `scripts/e1a_scan_profile.py` sha `12f134905e560dbd1d20a6e92b8d948915aeaf3234572f6e47afc8e01b871307`（逐点表 + 目标差 + 接触三分类，共价半径 0.45 Å 容差建键、图距 1/2/≥3 分类）；
- `scripts/e1a_scan_conformer_check.py` sha `6c8b92efd1bc5a8b3ceff15256c6e936b2f47e1c1d71236344d77539c8c97566`（相邻点重原子 Kabsch RMSD + 关键二面角）；
- `scripts/extract_scan_frame.py` 已修正为匹配 `Optimization completed`（含 negligible-forces 行），现 sha `8462651df71012a37d7fd277a6d5114856beb2c60587aaac444db043ec9e0a82`（旧版只匹配带句号者会漏点 7，已注明）。

### 50.7 二面角口径对齐（协调者 20:28–20:30 CST 独立复算唯一分歧项，已解决）

**零动作：未提交、未 ts_resume、未碰 ts/ 下文件、未 kill、未改交付面。**

- **C14 = 工作序 1-based 原子 14**，元素 **C**，与 N18 成键（**R(14,18) = 1.4701 Å**）、与 C15 成键（1.5435 Å）⇒ 脯氨酸 **Cα**；不是别的碳、不是 map 标签错位。
- 差异原因是**约定**，不是解析错误：
  - 本 lane 用**标准有符号 torsion** `dih(3,2,18,14)`（3-2-18-14 顺序，atan2）：11 点序列 **+128.82 / +131.14 / +136.03 / +139.03 / −152.93 / −154.71 / −155.68 / −156.53 / −157.51 / −158.79 / −160.01**（pt1…pt11）。
  - **勘误（协调者 20:32 CST 自证并撤回）**：协调侧先前报的 **+41.0° / −27.1°** **不是另一种合法约定**，而是其**原实现交叉积顺序写反（n2 = b1×b2）导致输出补角**；用正确写法（n2 = b2×b1）+ 同一 pt4 帧（sha f1ff2130…）得 `dih(3,2,18,14)` = **−139.03°**（与本 lane 的 +139.03° **仅差整体符号约定**），11 点序列 = −128.82 / −131.14 / −136.03 / −139.03 / +152.93 / … / +160.01，4→5 跃变 **68.04°** 完全一致。⇒ 原句「协调者用两平面夹角（补角写法）」**作废**（不把它当作两套合法约定之一）。
  - 变化幅度一致：torsion 139.03 → −152.93（≡ −68.04°；协调侧独立复算 68.04° 同值）。协调侧落账采用 **|τ| 写法：139.0° → 152.9°，Δτ = 68.0°**。
- **引用规则（此后生效，2026-10-17 20:33 修订）**：若要写具体角度，**必须注明符号/定义**（本 lane 为 `torsion(3,2,18,14)` 有符号值；协调侧引用 |τ| 无符号值 139.0° / 152.9°）；**不再使用「补角写法」这一表述**（已撤回）；若不愿涉约定，用稳健表述 **「4→5 出现大角度重构（重原子 Kabsch RMSD 0.759 Å、maxdisp 1.129 Å，原子 13）」**——该表述不依赖角度定义。
- pt4 四原子坐标（供第三方复核，取自 `E1A_neg_scan_p4_R2542_branchA.xyz` sha `f1ff2130…`）：atom2 (C) = (−2.502260, −0.344124, 0.020120)；atom3 (O) = (−2.701760, −0.495796, 1.215108)；atom14 (C) = (1.032510, 0.025115, −0.587075)；atom18 (N) = (−0.091456, 0.420794, 0.273987)。
- 新增可复核脚本：`scripts/e1a_dihedral_recheck.py` sha `fdd4624319937a339ac0e0c7a8401555f694af678d7526fe53f4cde0178385e3`；`scripts/e1a_dihedral_series.py` sha `55b577997f787abf72de696afcbb8d7acb147c5f6d87e74946ac5a9f073ef9c5`；`scripts/e1a_dihedral_convention.py` sha `dddc423876293d61839cace6426a7cd550c0080e1cb7dfa5c6a049689def3b1d`。
- 其余各项（终止三件套、逐点 R(3,27)/E/SCF 行号/ΔE、四元数 Kabsch RMSD 序列、支 A/支 B 单调性、点 4 局部高为跳变假象）**已由协调者独立复算并接受**，本 lane 记为**双人复核**。

## 51 流程收敛：此后不回执（协调者 21:17 CST 广播 post evt_2a1e84d0cf7b4f2d 记于本 lane）

**零动作：本 lane 无在跑作业、零提交、未 ts_resume、未碰 ts/ 下文件、未 kill、未改交付面。**

- 纪律（自 21:17 CST 起）：收到协调者口径/裁定/勘误**不再发收条帖**；只在四类事件发帖：①作业终态（三件套 + 逐字终止行 + 行号 + 判读）；②新作业提交（job id / started_at / 输入 sha / 门控读数）；③发现假象或需重出种子（先报再动）；④blocked / 崩溃 / 工具拒绝。每帖自带**绝对路径 + sha256 + 行数/行号 + date -Is 实测时刻**。
- 本 lane 状态：E1a 算力授权已用尽并收口——**无可用 guess、无 TS 候选、barrier 恒 null**；job 1070（解离侧、方向错误）与 job 1072（进攻侧、4→5 构象跳变）均只作 post-freeze 追记。下一窗口方向（未授权）：耦合 C–N 部分拉伸与质子转移中途的构造性 guess，且起点进度须与两端点距离线性自洽。
- 三条关键待办按广播归**其他道**：1074 格点推进（第 7 点起质子维展开）、1071 终态四档判读、E2 ≥3 收敛帧出表——本 lane 不介入，只读静默。
- 边界不变：四条边 result/barrier 全 null；交付面 `FINAL_DELIVERY_DRAFT.md` a2964d8d…/277 行 + 11 文件 sha、§14、hi.py 不动；零 kill / 重投 / priority / ts_resume。

## 52 22:04 CST 只读巡检（第七轮超时）：ts_0015 仍冻结，未发帖（按 21:17 纪律）

- `ts_inspect(ts_0015)`（2026-10-17T22:04:43+08:00 实测）：rev **11** / stage **refine** / status **waiting** / result **null** / blocked **null**；`process.json` 30,059 B mtime **2026-10-17 14:36:37.092354393**（冻结已 ~7 h 28 min）；`jobs/declaration_0001/` 仅 `ts_opt/`，`test -d …/frequency` 退出码 **1**。
- 按 21:17 广播纪律（仅四类事件发帖），本条属"无变化只读巡检"⇒ **不发帖**，只登记。
- 处理：巡检间隔改为更长周期（6 h）继续只读监测；#197 口径不变（stage 间推进处特定挂起，不写失败/输入被拒），诊断归协调者。

## 53 核对协调者 POST_FREEZE_SUMMARY_2212.md 中本 lane 相关条目（2026-10-17T22:12 CST 只读）

**零动作：未提交、未 ts_resume、未碰 ts/ 下文件、未 kill、未改交付面。**
- 被核对文件：`/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/POST_FREEZE_SUMMARY_2212.md`，**55 行 / sha256 `8b46a8014d532b509f806b41d05baca64b7a70675cb486f2232490c3e6a8b91f`**（22:11:20 CST 实测），与其自述一致。
- **E1a 条目逐项一致**：log sha `359937d4…` / 91,682 行 / L91682 @20:26:25 ✅；支 A（sp1–4）+1.09→+1.82、支 B（sp5–11）+0.74→+4.25 各自单调无内部极大 ✅；ΔE‡ = null ✅；二面角口径 `|τ| = 139.0° → 152.9°、Δτ = 68.0°`（须注明符号约定）✅；「差异来自原子标签」说法作废 ✅。
- **唯一需要补标签处（非数值冲突）**：其 §3 写「sp4→sp5 重原子 Kabsch 0.985 Å / 0.759 Å 双人复现」，但两个值**原子集合不同**：**0.759 Å = 12 重原子**（1,2,3,4,11–18；maxdisp 1.129 Å）、**0.985 Å = 全 27 原子（含 15 H；maxdisp 1.740 Å）**。两者本 lane 均可复现（脚本 `scripts/e1a_rmsd_p4p5.py` sha `f561ef567126676b507de6f58c0a6660c52e56261b5994504cd2ee026330698e`），**不是矛盾**，仅需注明原子集合。
- 新增导出帧（供三方复核 sp4→sp5）：`E1A_neg_scan_p5_R2492_branchB.xyz` sha256 **`4b8d0a55153b41fa013a9351fc6c7d4d59b70745196244a1f38bb83f07941110`**（27 原子，sp5 收敛帧）。
- 其余与本 lane 无关条目（E3/E2/EM1/NY3/NR1）不改、不介入。

## 54 核对 small_mol 的 E1a 成键侧续扫 job 1077 起点（2026-10-17T22:49 CST，只读）

**零动作：本 lane 未提交、未 ts_resume、未碰 ts/ 下文件、未 kill、未改交付面。**
- 对方输入：`split/E1A_scan_cont1_C2N18.gjf`，**sha256 `d2043fc5ade4b3087c08005cec94427ca49f3639dcb96f75a6fed49c8d81b2ae`**、38 行（与其公布一致）；route 逐字 `#p opt=(modredundant,maxstep=6) B3LYP/def2SVP empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=dmso)`；约束 `B 2 18 S 5 -0.1000`（L37，前后空行 L36/L38）；job_id **1077**。
- **起点帧核验（本 lane 独立算）**：27 原子、元素序与我的 sp11 帧完全相同，**逐原子 max|Δ| = 0.000000000000 Å** ⇒ 起点 = job 1072 **第 11 点（支 B 末点）** 收敛帧，未手写坐标、未改原子序（脚本 `scripts/e1a_cont1_seed_check.py` sha `77b559d50452058940a0bd6c55f5ada1d63f6a565fe812b323eb345a36f647ae`）。
- **需注意的语义（可能构成拼接假象）**：起点属 **支 B**（构象已跳变；R(3,27)=2.9100、R(18,27)=1.0163、R(2,3)=1.2319）。因此 1077 的剖面只能与**支 B（我的 sp5–sp11）**相接，**不得与支 A（sp1–sp4，E +1.09→+1.82）拼接**；若要接支 A，应该用支 A 最深帧 `E1A_neg_scan_p4_R2542_branchA.xyz`（sha `f1ff21307918afaa6afa921f244969122b40f94183883d01bc2a232f4d8055e2`，R=2.5420）作起点。
- 已把该点作为「假象风险」在 hub 报出（含路径 + sha + 行号 + date -Is），供对方在逐点表里注明所属分支。

## 55 E1a 收口措辞（协调者 22:49:16 CST 采纳支 A/支 B 划分后定稿；按 21:17 纪律不发回执帖）

**零动作：未提交、未 ts_resume、未碰 ts/ 下文件、未 kill、未改交付面；E1a barrier 恒 null。**

### 55.1 E1a 结论定稿（按协调者要求分两支各一句）
1. **支 A（job 1072 sp1–sp4，R(C2–N18) 2.692→2.542 Å）内部无极大**：E 自 +1.09 单调升至 +1.82 kcal/mol（相对 RC_27 −593.934532807）。
2. **支 B（job 1072 sp5–sp11，R(C2–N18) 2.492→2.192 Å）内部无极大**：E 自 +0.74 单调升至 +4.25 kcal/mol。
3. **sp4→sp5 是构象分支切换**（重原子 12 Kabsch **0.759 Å** / 全 27 原子 **0.985 Å**；|τ|(O3–C2–N18–C14) **139.0°→152.9°**、Δτ 68.0°；O3···H27 **2.557→3.150 Å**；E 跳降 1.08 kcal），**因此不能把 11 点合成单一连续剖面下结论**。
4. ⇒ **纯 C–N 拉伸不是该步的反应坐标**；E1a 需耦合 C–N 拉伸与质子转移中途的构造性 guess（下一窗口，未授权）；**不写「通道不存在」**；**E1a barrier 恒 null**；所有 ΔE 均非 ΔE‡。
5. 支 A 续扫若获主协调口令，起点用 `E1A_neg_scan_p4_R2542_branchA.xyz`（sha `f1ff2130…`，R=2.5420 / C2–O3 1.2210 / N18–H27 1.0151 / minsep 0.9741）；**本 lane 现在不提交**（资源 free cpus=0 + 需主协调口令）。

### 55.2 1077（small_mol 支 B 续扫）判读口径（协调者锁定，本 lane 采用）
- 1077 = **支 B 段单独序列**（R 2.1920→1.6920），**禁止与支 A 能量序列拼接或跨支相减**；ΔE 只对**支 B 自首点（sp11）**取差，且必须写「**相对支 B 首点，非 ΔE‡**」。
- 最低字段：scan# + 实测 R(2,18) 与目标 |Δ|≤0.002 + R(3,27) + R(18,27) + C2–O3 + SCF 能量 + 相对 sp11 的 ΔE（标非 ΔE‡）+ 每点 `Optimization completed` 行号 + 终止行逐字。
- 若 H27 迁至 O3（R(3,27) 显著缩短且 R(18,27)>1.10）⇒ 该步单独标「**已非同一化学通道**」并按纪律停手登记。

### 55.3 登记（不提交）
- 支 A 成键侧候选种子：`split/E1A_neg_scan_p4_R2542_branchA.xyz`，sha256 `f1ff21307918afaa6afa921f244969122b40f94183883d01bc2a232f4d8055e2` —— **post-freeze asset、未提交**；放行条件 = free cpus>0 **且** 主协调口令。
- 队列事实（协调者 22:48:10 实测）：在跑 1071 / 1074 / 1076 / 1077 = 4 作业 = 32 cpus、free cpus = 0 ⇒ 零提交。

## 56 支 A 续扫裁定 = 暂不提交（主协调 evt_f453d0f2e5fa48c7，协调者 22:52:16 CST 转达）+ 1077 双时刻读数并列

**零动作：本 lane 未提交、未 ts_resume、未碰 ts/ 下文件、未 kill、未改交付面。**

### 56.1 裁定与解冻条件（本 lane 遵守）
- **支 A 成键侧续扫暂不提交**（理由：free cpus=0；两支各自单调已足以支撑「纯 C–N 拉伸不是该步反应坐标」；收口优先）。本 lane 不提交，协调者亦不提交。
- 解冻须**同时**满足：①任一在跑作业（1071/1074/1076/1077）自然结束、腾出 **≥8 cpus**；②**1076 与 1077 已出结果并记账**。
- 解冻后固定口径（不在本窗口执行）：种子 `E1/split/E1A_neg_scan_p4_R2542_branchA.xyz` sha256 `f1ff21307918afaa6afa921f244969122b40f94183883d01bc2a232f4d8055e2`、`B 2 18 S 5 -0.1000`、`maxstep=6` ⇒ 6 几何 **2.5420 → 2.0420**；与 1077 **分支配对分列、禁拼接**、ΔE 仅对内、**标非 ΔE‡**、**E1a barrier 保持 null**。

### 56.2 E1a 收口措辞最终确认（数值已 4 位复核）
- 「**支 A sp1–sp4 内部无极大**」+「**支 B sp5–sp11 内部无极大**」两句并列，并明写 **sp4→sp5 为构象分支切换**，**不得合成单一连续剖面**。
- 切换量（本 lane 4 位精度复核，脚本 `scripts/e1a_rmsd_p4p5_4dp.py` sha `a6748034bea42d65194c7b6a403ca0119521cc05a68febcbd98615904937b85f`）：重原子 12 Kabsch **0.7593 Å**（max 1.1290）、全 27 原子 **0.9853 Å**（max 1.7398）；τ 有符号 `torsion(3,2,18,14)` **+139.03° → −152.93°**（环差 **68.04°**）；**E 跳降 1.08 kcal/mol**；O3···H27 2.557 → 3.150 Å。

### 56.3 1077 读数并列（两时刻，互不覆盖）
| 读数方 | 时刻（date -Is） | 日志 | 行数 | sha256 | 收敛点 | 当前位置 |
|---|---|---|---|---|---|---|
| 协调者 | 2026-10-17T22:51:56+08:00 | `split/E1A_scan_cont1_C2N18.log` | 5,600 | `3dda96d8…`（协调者报） | Stationary point found = 1（scan point 1/6） | scan point 2/6 Step 5/162 |
| 本 lane | **2026-10-17T22:52:40+08:00** | 同文件（原生日志，非 .cloudra wrapper） | **6,361** | **`4d277be587c6329b16a3a6c3ecedda4f03fa122a58294d924257b1a6110baeda`** | `Optimization completed` 计数 **1** | **scan point 2/6 Step 6/162**（L5072/L5812） |
- 差异仅来自两时刻之间日志继续增长（22:51:56 → 22:52:40 约 44 s，+761 行），非读数冲突。

### 56.4 监控纪律（主协调提出、本 lane 采纳）
- **只看原生日志**（`split/E1A_scan_cont1_C2N18.log` 等），**不看** `.cloudra/calc-*.out.log` wrapper。
- 终止判据用**长串**匹配：`Error termination via` / `Normal termination of Gaussian`（避免 "Termination" 与逐点伪匹配）。

## 57 脚本归属声明 + 1077 三点读数并列（2026-10-17T23:12 CST）

**零动作：未提交、未 ts_resume、未碰 ts/ 下文件、未 kill、未改交付面。**

### 57.1 归属声明（协调者 23:12:17 询问）
- `split/e1a_cont1_check_2309.py`（1,361 B / sha `eb12735f6c413499ad441dabddba3a8219ac40d22f7c98ef94579b4a1ee94715` / mtime 23:09）：**非本 lane 创建**（本 lane 未在 23:09 写任何文件；此前最后写入为 22:52 的 `scripts/e1a_rmsd_p4p5_4dp.py`）。其 docstring 自称 read-only 分析 cont1，按无主 scratch 处理即可，本 lane 不引用。
- **补正（协调者 23:13:30 CST）**：`split/scripts/e1a_cont1_analyze.py`（7,179 B / sha `bde7b3e714d0b40bdefd33d3f728dbfa368cc96397040a4891633028ff300ed9` / mtime 22:50）**非本 lane 创建，但有主**——**E1a-cont1 执行道 `as_2d57e6a0f2e843c0`** 于 2026-10-17T22:50:30 自报该 sha 为其分析脚本（含三条 Kabsch 合成自检与 1072 旧日志对照复验）。引用时写「E1a-cont1 执行道脚本（as_2d57e6a0f2e843c0）」，不再使用「他道脚本」这种无主措辞（本条为更正，原措辞作废）。
- 本 lane 自有脚本清单（`split/scripts/`，全部为只读分析；sha256 如下，可作归属边界）：
  | 脚本 | sha256（前 16） |
  |---|---|
  | e1a_cont1_seed_check.py | 77b559d504520589… |
  | e1a_dihedral_convention.py | dddc423876293d61… |
  | e1a_dihedral_recheck.py | fdd4624319937a33… |
  | e1a_dihedral_series.py | 55b577997f787abf… |
  | e1a_pose_compare.py | 4924148c8f517133… |
  | e1a_rmsd_atomset_check.py | c3495934d08ca19c… |
  | e1a_rmsd_p4p5.py | f561ef567126676b… |
  | e1a_rmsd_p4p5_4dp.py | a6748034bea42d65… |
  | e1a_scan_conformer_check.py | 6c8b92efd1bc5a8b… |
  | e1a_scan_profile.py | 12f134905e560dbd… |
  | e1a_scan_table.py | fc3ff4b929b18621… |
  | extract_scan_frame.py | 8462651df71012a3… |
  | scan_point_geometry.py | de513ccb8fe6c45b… |
  | snapshot_head_blocks.py | c952bb150ad5c860… |

### 57.2 1077 读数并列（本 lane 不自采 wrapper，只读原生 log）
| 读数方 | 时刻 | 行数 | sha256 | 收敛点 | 当前位置 |
|---|---|---|---|---|---|
| 协调者 | 2026-10-17T23:11:57+08:00 | 32,416 | `c59246b1…` | **3**（L1444 / L23569 / L28082 = 2.1920 / 2.0920 / 1.9920） | scan point 4/6（1.8920）Step 5/162；termination 0 |
| 本 lane（22:52:40） | 2026-10-17T22:52:40+08:00 | 6,361 | `4d277be5…` | 1 | scan point 2/6 Step 6/162 |
- 说明：本 lane 自 22:52 起未再采 1077（该作业属他道、只读关注）；如需更新以协调者 23:11:57 读数为准。**支 B 段第 4 点已推进，仍禁与支 A 拼接。**

### 57.3 取整纪律（本 lane 采纳）
- **下界一律向下取**（如 1.9260 ⇒ ≥1.92），**禁上舍**；1071 参照不确定度写法：`as of 2026-10-17T23:10:45 ≥1.92 并封顶不适用（不封顶）`。本条同样适用于本 lane 台账中任何「≥」型下界表述。

## 58 归属补正 + 1077 多时刻读数表 + 一处读数误归属的澄清（2026-10-17T23:14 CST）

**零动作：未提交、未 ts_resume、未碰 ts/ 下文件、未 kill、未改交付面。**

### 58.1 归属状态（最终）
- `split/e1a_cont1_check_2309.py`（1,361 B / 23:09，sha `eb12735f6c413499ad441dabddba3a8219ac40d22f7c98ef94579b4a1ee94715`）：**无主 scratch**——本 lane、协调者、E1a-cont1 执行道三方均声明非己创建 ⇒ **不得引用**，认领前不进任何表。
- `split/scripts/e1a_cont1_analyze.py`（7,179 B / 22:50，sha `bde7b3e714d0b40bdefd33d3f728dbfa368cc96397040a4891633028ff300ed9`）：**属 E1a-cont1 执行道 `as_2d57e6a0f2e843c0`**（22:50:30 自报）。

### 58.2 1077 多时刻读数（同链不同时刻并列，不设权威值，引用各带时刻）
| 时刻（date -Is） | 读数方 | 行数 | sha256 | 收敛点 | 位置 |
|---|---|---|---|---|---|
| 2026-10-17T22:52:40+08:00 | **本 lane** | 6,361 | `4d277be587c6329b16a3a6c3ecedda4f03fa122a58294d924257b1a6110baeda` | 1 | scan 2/6 Step 6/162 |
| 23:11:57+08:00 | 协调者 | 32,416 | `c59246b1…` | 3 | scan 4/6 Step 5/162 |
| 23:12:35+08:00 | E1a-cont1 执行道 | 33,700 | `76f84f44…` | 3 | scan 4/6 Step 7/162 |
| 23:11:37+08:00 | **（协调者台账记为「你」）** | 31,639 | — | 3 | scan 4/6 Step 5/162 |

- **澄清（需更正误归属）**：**本 lane 没有 23:11:37 的读数**。本 lane 对 `E1A_scan_cont1_C2N18.log` 的读数只有 **22:48:46**（文件/sha/约束行）与 **22:52:40**（6,361 行 / 4d277be5…）两次，之后未再自采（他道作业，只读关注）。23:11:37 那条应属协调者或他道，**不应挂在 lane1 名下**。
- 支 B 单段、禁与支 A 拼接不变；ΔE 只对支 B 首点 sp11 取差并标「非 ΔE‡」。

### 58.3 取整与边界
- 下界**一律向下取**（1.9260 ⇒ ≥1.92）；1071 参照不确定度写法「as of 2026-10-17T23:12:48 ≥1.92 且不封顶」（协调者 23:12:48 实测 min L190922 = −939.322609417，未刷新）。
- E1a 收口 = 支 A / 支 B 各一句「内部无极大」+ 明写 sp4→sp5 分支切换（0.7593 / 0.9853 / τ +139.03°→−152.93° / 68.04° / E 跳降 1.08 kcal），**barrier 恒 null**；四条边 result/barrier 全 null；零 kill / 重投 / priority / ts_resume。

## 59 归属终态 + 1077 前四点独立核验（2026-10-17T23:15 CST，只读）

**零动作：未提交、未 ts_resume、未碰 ts/ 下文件、未 kill、未改交付面。**

### 59.1 归属终态（更新 §58.1）
- `split/e1a_cont1_check_2309.py`（1,361 B / 23:09 / sha `eb12735f6c413499ad441dabddba3a8219ac40d22f7c98ef94579b4a1ee94715`）：**已由主协调 `as_a341823c436e47ed` 于 23:14:13 认领**（evt_284a31831193410f）——其 23:09:33 的只读核验脚本（抽 27 原子几何 + 收敛块末次 SCF，算 R(2,18)/R(3,27)/R(18,27)/R(13,19) 与 ΔE vs RC_27）；登记为「主协调核验脚本、非交付证据」，引用写「eb12735f… + 时刻 + 行号」，**不改不删**。⇒ 不再是「无主 scratch」。
- 另同时认领：`E2/forensic/e2_cont1_check_2252.py`（`15092b7f…`）、`E1/split/e1a_verify_2216.py`（`281e60fa…`）——本 lane 不引用、不改不删。
- `split/scripts/e1a_cont1_analyze.py`（sha `bde7b3e7…`）＝ E1a-cont1 执行道 `as_2d57e6a0f2e843c0`（不变）。

### 59.2 1077 前四点独立核验（本 lane 自采，原生日志）
- 自采时刻 **2026-10-17T23:15:20+08:00**：`split/E1A_scan_cont1_C2N18.log` **37,478 行**（23:15:13 采）/ sha256 `6b1508e25ce8ab792058523449145087e6e54d39c07b88ff900b2c8eec75b727`（23:15:13 采）；`Optimization completed` **4**（L1444 / L23569 / L28082 / **L37012**）；当前 scan point 5/6（1.7920）运行中（L36755 处为 scan 4 step 12/162 之后切换）。
- SCF 值逐行核对（与协调者 23:14:30 所引**逐位一致**）：pt1 L847 = **−593.927767684**；pt2 L23230 = **−593.924918315**；pt3 L27764 = **−593.921506724**；**pt4（新增）L36681 = −593.917681983**（R=1.8920，块 L36296/L36430）。
- ΔE vs RC_27（−593.934532807）：**+4.25 / +6.03 / +8.17 / +10.57 kcal/mol**（pt1→pt4）；相对 pt1：**+0.00 / +1.79 / +3.93 / +6.33**。⇒ **前四点单调上升、无内部极大**（仍缺 pt5–pt6 才能落「支 B 内部无极大」）。
- 通道判据：R(18,27) = 1.0163 → 1.0169 → 1.0177 → **1.0188**（H27 始终在 N18，**通道未变**，未触发「已非同一化学通道」）；C2–O3 = 1.2319 → 1.2531（pt4，仍在 1.22–1.28）；R(3,27) pt4 = 2.7239；minsep pt4 = 0.9743（≥0.90）。
- **可复现性旁证**：cont1 pt1 = −593.927767684 与本 lane job 1072 sp11 = −593.927767693 相差 **9×10⁻⁹ Eh（≈6×10⁻⁶ kcal/mol）**，同一 R=2.1920 约束下能量可复现 ⇒ 续扫的绝对能标与 1072 兼容（但仍禁跨支拼接）。
- 本条按 21:17 纪律**不发帖**（他道作业进度，由其执行道与协调者记账）；如需本 lane 读数，以此节时刻为准。

### 59.3 口径
- 下界一律向下取（1.9260 ⇒ ≥1.92）；1071「as of 23:13:41 ≥1.92 且不封顶」（min L190922 未刷新，主协调 23:14:13 逐位一致）。
- E1a 收口不变：支 A / 支 B 各一句「内部无极大」+ sp4→sp5 分支切换明细（0.7593 / 0.9853 / τ +139.03°→−152.93° / 68.04° / 1.08 kcal）+ **barrier 恒 null**；支 B 单段、禁与支 A 拼接。

## 60 1077 pt4 由协调者复核确认 + 终止时才出表（2026-10-17T23:16 CST）

**零动作：未提交、未 ts_resume、未碰 ts/ 下文件、未 kill、未改交付面。**
- 协调者 23:15:58 复核：日志 38,282 行 / sha `496112c284c8b6dc008a9ae81ffb528af4bbab3746efe075a83f196886421066`、`Optimization completed` 4（L1444/L23569/L28082/**L37012**）、pt4 末次 SCF **L36681 = −593.917681983**（逐字一致）⇒ 自算 **ΔE vs RC_27 = +10.5745**（本 lane +10.57）、相对 pt1 **+6.3263**（本 lane +6.33）⇒ **双方一致**。pt4 几何读数按本 lane 值登记（协调者未独立复算几何）。
- 判读不变：前 4 点 **+4.25 / +6.03 / +8.17 / +10.57** 单调上升、无内部极大；R(18,27) 1.0163→1.0188、H27 始终在 N18、**通道未变**，暂不触发「已非同一化学通道」。当前 scan point 5/6（1.7920）Step 1/162（L37708）；**仍缺 pt5–pt6** 才能落「支 B 内部无极大」。
- 可复现性旁证（cont1 pt1 vs 1072 sp11 差 9×10⁻⁹ Eh）已被采纳，标注「**不作跨支使用**」。
- **报告纪律（协调者 23:15:58）**：1077 终止后**只在终止帖**给三件套 + 逐字终止行 + 逐点表；**中间点不逐点报**。⇒ 本 lane 已布防长串终止判据（`Normal termination of Gaussian` / `Error termination via`）只读监测原生日志，触发时一次性出表。
- 归属与口径照旧：`check_2309.py` = 主协调认领脚本（非交付证据、不改不删）；`e1a_cont1_analyze.py` = E1a-cont1 执行道；下界向下取；1071「as of 23:13:41 ≥1.92 且不封顶」；**E1a barrier 恒 null**。

## 61 **job 1077（支 B 续扫 cont1）终态**：6/6 点收敛、全程单调、无内部极大（2026-10-17T23:22 CST）

**零动作：未提交、未 ts_resume、未碰 ts/ 下文件、未 kill、未改交付面；E1a barrier 恒 null。**

### 61.1 终止与完整性
- 日志：`split/E1A_scan_cont1_C2N18.log`，**sha256 `542706d43875bccf2e6495d11490ab18170f4ab64df90da22665995ef1386b48`**，**47,126 行**（2026-10-17T23:22:05+08:00 实测）。
- 终止行（逐字，**L47126**）：` Normal termination of Gaussian 16 at Sat Oct 17 23:21:48 2026.`
- `Optimization completed` **6/6**：L1444 / 23569 / 28082 / 37012 / 41559 / 46073；**无** FormBX / Bend failed / Tors failed / NStep。

### 61.2 逐点表（支 B 段单独序列；目标 R = 2.1920 − 0.1000×(n−1)；ΔE 为同批纯电子差；1 Eh = 627.509474 kcal/mol）
| pt | convL | 实算 R(2,18) | 目标 | 实际−目标 | E(RB3LYP) | SCF L | ΔE vs RC_27 | ΔE vs pt1 | C2–O3 | R(18,27) | R(3,27) | minsep |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 1444 | 2.1920 | 2.1920 | −0.0000 | −593.927767684 | 847 | +4.25 | 0.00 | 1.2319 | 1.0163 | 2.9100 | 0.9745 |
| 2 | 23569 | 2.0920 | 2.0920 | −0.0000 | −593.924918315 | 23230 | +6.03 | +1.79 | 1.2374 | 1.0169 | 2.8528 | 0.9744 |
| 3 | 28082 | 1.9920 | 1.9920 | −0.0000 | −593.921506724 | 27764 | +8.17 | +3.93 | 1.2445 | 1.0177 | 2.7923 | 0.9744 |
| 4 | 37012 | 1.8920 | 1.8920 | −0.0000 | −593.917681983 | 36681 | +10.57 | +6.33 | 1.2531 | 1.0188 | 2.7239 | 0.9743 |
| 5 | 41559 | 1.7920 | 1.7920 | −0.0000 | −593.913920630 | 41241 | +12.93 | +8.69 | 1.2639 | 1.0199 | 2.6542 | 0.9744 |
| 6 | 46073 | 1.6920 | 1.6920 | −0.0000 | −593.910058898 | 45754 | +15.36 | +11.11 | 1.2769 | 1.0214 | 2.5836 | 0.9745 |
- **约束断言**：6 点 |实际−目标| = 0.0000 Å（≤0.002 ✅）；R 序列 2.1920→1.6920 与 `B 2 18 S 5 -0.1000` 一致。
- **通道判据**：C2–O3 = 1.2319→**1.2769**（全 ≤1.32、且 ≤1.28，羰基保持）；R(18,27) = 1.0163→**1.0214**（全 ≪1.10，**H27 始终在 N18**）⇒ **通道未变**，未触发「已非同一化学通道」。
- **接触三分类**：成键 0.9743–0.9745（13–19 羧基 O–H）；1-3 1.7642–1.7715（25–26）；非键最小 pt1–pt3 = 被扫的 2–18 对（2.1920/2.0920/1.9920）、pt4–pt6 = 13–27（2.1583/2.1355/2.1095）⇒ 非键 ≥1.20 全部合格；minsep ≥0.90 全部合格。

### 61.3 结论（一句话，按约定措辞）
- **支 B（cont1 段 2.1920→1.6920）内部无极大**：ΔE vs RC_27 自 +4.25 单调升至 +15.36 kcal/mol（相对支 B 首点 +0.00→+11.11），6 点无内部极大 ⇒ **该段不产生 TS 候选**；与 job 1072 支 B（sp5–sp11：+0.74→+4.25）相接后，**支 B 全程 2.4920→1.6920 亦单调无内部极大**。
- **禁与支 A 拼接**；所有 ΔE **非 ΔE‡**；**E1a barrier 恒 null**；不写「通道不存在」。
- 化学读数（只描述、不推断机理）：降至 1.692 Å 时 C2–O3 已升至 1.2769 Å（羰基仍双键、C2 仍 sp² 型）、N18–H27 仍 1.0214（质子未迁移）⇒ 纯 C–N 压缩不改质子态，能量持续上升。
- 脚本：`split/scripts/e1a_cont1_profile.py` sha `f4a642f5408970f4cb51a997a02529d8ba1f55a62c72028fa91e5387f01828c3`（目标序列、双 ΔE、接触三分类）。

## 62 E1a 收口措辞定稿（协调者 23:23:00 CST 双签通过）+ rms/max 并列纪律

**零动作：未提交、未 ts_resume、未碰 ts/ 下文件、未 kill、未改交付面。**

### 62.1 双签确认
- 1077 三件套与逐点表**双方逐位一致**（47,126 行 / `542706d4…` / L47126 逐字终止行 / 6 点收敛；E 六值、R 序列、C2–O3、R(18,27)、双 ΔE 全同）。
- 协调者另给相邻点 Kabsch rms 序列 **0.1243 / 0.0441 / 0.0887 / 0.0529 / 0.0498**（det +1.000）。

### 62.2 rms / max 并列纪律（本 lane 采纳）
- **引用相邻点叠合时必须同时给 rms 与 max**（不同判据），**不得只写 rms**。
- 本 lane 独立复核 pt1→pt2（脚本 `scripts/e1a_cont1_step_rmsd.py` sha `744ef709a450728d5a382c241f088251cf7d809c4e3127f08bc4e5daa76d6681`，帧由 `extract_scan_frame.py` 从原生日志抽取）：
  - **重原子 12**：rms **0.1243 Å**、**max 0.3283 Å（原子 7）**、det **+1.000**；
  - **全 27 原子**：rms **0.1149 Å**、max **0.3451 Å（原子 19）**、det +1.000。
  - ⇒ 与协调者 0.1243 / 0.3283 逐位一致；后续引用一律「rms 0.1243 + max 0.3283（重原子 12）」。

### 62.3 E1a 收口措辞（**定稿，逐字可引用**）
1. 「**支 A sp1–sp4 内部无极大**」。
2. 「**支 B 内部无极大**」——job 1072 sp5–sp11（vs RC_27 +0.74→+4.25）与 cont1 pt1–pt6（vs pt1 0.00→+11.11）合并后，**支 B 全程 2.4920→1.6920 Å 单调**。
3. 明写 **sp4→sp5 构象分支切换**（重原子 12 Kabsch **0.7593** / 全 27 原子 **0.9853**；τ **+139.03°→−152.93°**、环差 **68.04°**；E 跳降 **1.08 kcal**）⇒ **两支禁拼接、禁跨支相减**。
4. **E1a result / barrier 恒 null**；所有 ΔE **标非 ΔE‡**。
5. **有界表述**：若纯 C2–N18 压缩坐标上另有驻点，只能位于 **R < 1.6920 Å** 一侧；**禁写「通道不存在 / 无 TS」**。

## 63 协议快照更新后的状态复核（2026-10-18T02:41:23+08:00，只读）

**零动作：未提交、未 ts_resume、未碰 ts/ 下文件、未 kill、未改交付面。**
- 本轮接到「静态协议/工具目录已更新」广播（新增 `ts_stop`；各工具 revision 变更）。本 lane 无在跑作业，无需适配新工具；
- 队列实测（query_compute_queue，02:41:23+08:00）：**running 只有 1074**（起于 20:28:54）；queued 空；**free 9 slots / 24 cpus / 40,960 MB**；terminal 新增 **1076 done @2026-10-18T00:20:14**、1078 done @00:08:42、**1071 done @2026-10-17T23:57:11**、**1077 done @23:21:50**、1075 **failed** @22:44:09（非本 lane 作业）。
- ⇒ 支 A 续扫的 22:51 解冻条件中，**①「腾出 ≥8 cpus」已满足（free 24 cpus）**、**②1076 与 1077 均已终止**（是否「已记账」由协调者判定）。但按既定裁定，**提交仍须主协调点名口令**，本 lane 不自行提交，已把该事实报协调者待裁。
- E1a 定稿措辞、barrier 恒 null、四条边 result/barrier 全 null、交付面不动等口径全部不变。


### 62.4 其它状态
- 1071 参照不确定度现值：**「as of 23:22:38 ≥2.01 且不封顶」**（SCF min −939.322757510）。
- 支 A 续扫仍按 22:51 解冻条件（腾出 ≥8 cpus **且** 1076/1077 已记账）：1077 已记账，但 **1076 仍在跑、free cpus 仍 0** ⇒ **仍不提交**。

## 64 job 1075（E2 侧 1D 扫描）失败性质的只读取证（2026-10-18T02:52+08:00，只读）

**零动作：未提交、未 ts_resume、未 kill、未改 E2 任何文件、未碰交付面。** 本条**仅登记**，**不作 E2 证据**；E2 result / barrier 维持 **null**。

### 64.1 三件套（原生日志）
- 路径：`gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan.log`
- 行数：**103,879**（`wc -l`）
- sha256：`445956fd7491b68f65da4b1d0172f68ac4e35e19a9a55215d9358390fbe2932e`
- mtime：`2026-10-17 22:44:01.203275950 +0800`；大小 6,703,953 B；读取时刻 `2026-10-18T02:50:05+08:00`

### 64.2 失败类别
**failure_class =「Error imposing constraints」（冗余内坐标约束施加失败，l103）**——不是 SCF 失败、不是虚频判据、不是 NStep / 步数耗尽（`Number of steps exceeded` 全文 0 次）。

### 64.3 逐字错误行（带行号）
- L103822 `New curvilinear step failed:  FormB failed.`
- L103874 `New curvilinear step failed:  FormB failed.`
- L103875 `Error imposing constraints`
- L103876 ` Error termination via Lnk1e in /home/ly/g16/l103.exe at Sat Oct 17 22:44:01 2026.`
- L103877 `Job cpu time:       0 days 16 hours  4 minutes 41.9 seconds.`
- L103878 `Elapsed time:        0 days  2 hours  4 minutes  2.1 seconds.`

### 64.4 进度上下文（同一日志）
- 扫描共 **15 点**；L84816 起为 `scan point 8 out of 15`，L86847 起为 **`scan point 9 out of 15`**。
- 最后一次步进打印 L103757：`Step number  18 out of a maximum of  219 on scan point     9 out of    15`。
- `Optimization completed.` 共 **8 次**（末四次 L75938 / L85975 及更早 L43674 / L56487 / L67553）。
- 末三次 SCF Done：L101800 −939.296837073、L102708 −939.296843614、L103669 −939.296849384。
- ⇒ **8 点收敛、第 9 点第 18 步在「施加约束」处中止**。

### 64.5 输入（只读引用，不评价其设定，亦非本 lane 提交）
`E2_1D_scan.gjf` sha256 `6301b836b6ca0006f365d80e28cff2f552bd06edae8f54475d6985e751ffbb16`，52 行，mtime 2026-10-17 20:35:47；
L4 路由 `#p opt=(modredundant,maxstep=8) B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=DMSO)`；L51 约束 `B 1 29 S 14 -0.2000`。

### 64.6 口径与边界
- 本条**不**推断 E2 通道存在/不存在鞍点，**不**把该次中止当作 E2 的任何能量或势垒证据；E2 result / barrier 恒 **null**。
- 另注（不重排既有章节）：§62.4 目前位于 `## 63` 标题之后（历史追加点所致）；**自本节起，新章节一律追加在文件最后一个非空行之后**（本次即文件物理末尾 1120 行前的空行之前），不改动 §35–§43 与既有编号顺序。
## 65 支 A 成键侧续扫：主协调点名放行 + 提交（2026-10-18T02:52+08:00）

### 65.1 口令来源（要点，含来源会话与时刻）
- 来源：协调者会话 **as_a341823c436e47ed**（本 lane 收到 Incoming call），口令写明「放行权由协调者转交给我」；本 lane 记账时刻约 **2026-10-18T02:52+08:00**（实测 `date -Is` = 2026-10-18T02:53:07+08:00）。
- 批准项：**仅此一项** —— E1a 支 A 成键侧续扫，2.5420 → 2.0420 Å，6 个几何。
- 明文硬条件：①种子 `gold_finish_20261015/HI1/E1/split/E1A_neg_scan_p4_R2542_branchA.xyz` sha256 必须 = `f1ff21307918afaa6afa921f244969122b40f94183883d01bc2a232f4d8055e2`，不符即停并报；②扫描关键字 `B 2 18 S 5 -0.1000`（B 2 18 = C2–N18），`maxstep=6`，6 几何、端点 2.5420 → 2.0420；③8 cpus / 10,240 MB / **priority 0**；④输出名带新后缀、**禁覆盖既有文件**（尤其 E1A_constrained_scan_R2692_2192_stepneg.log 91,682 行 / 359937d4…、E1A_scan_cont1_C2N18.log 47,126 行 / 542706d4…）；⑤坐标不手写，方法口径与既有扫段一致（B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight + CPCM(DMSO)，引擎 Gaussian 16）。
- 定性与记分：⑥全部产物标 post-freeze asset / non-delivery / 非 guess / 非鞍点；⑦**E1a result = barrier = null 不变**，峰只写「候选 / 下界」，不写 TS、不写 ΔE‡，**不触发 ts_prepare/ts_resume**；⑧ΔE 仅支 A 内部相对本段首点、标「非 ΔE‡」，**禁与 1077（支 B）或 cont1 拼接、禁跨支相减**。
- 纪律：零 kill / 零 re-submit / 不碰 ts_0015、ts_0016、ts_0020、ts_0006 / 不改交付面（277 行 / a2964d8d…）/ 不改 registry、task、tests。
- 同时批准（早前已批）：1075 只读核验（已完成，见 §64）。

### 65.2 开跑前闸门读数（逐项单独命令实测）
- 种子 sha256 = `f1ff21307918afaa6afa921f244969122b40f94183883d01bc2a232f4d8055e2` ✅ 与口令一致；size 1,118 B，mtime 2026-10-17 20:28:04.107574788；27 原子（1 行注释 + 27 坐标行，共 29 行）；实测时刻 `2026-10-18T02:51:48+08:00`。
- 队列（同一轮）：running 仅 1074（8 cpus / 10,240 MB / priority 0，起于 2026-10-17T20:28:54）；queued 空；node-local free = 9 slots / 24 cpus / 40,960 MB ⇒ ≥8 cpus 可满足。

### 65.3 输入生成（坐标不手写）
- 生成器 `qm_input_writer`（source_type=xyz_file；engine gaussian / B3LYP / def2SVP / charge 0 / multiplicity 1 / nproc 8 / mem 10240MB / keywords `EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=DMSO)`）；首次因未声明 charge 被拒（诊断性质，非化学限制），补 charge=0 后成功。
- 写盘后按既有可行路径补扫描：L4 由 `#p opt` 改为 `#p opt=(modredundant,maxstep=6)`，文件尾追加 `B 2 18 S 5 -0.1000`（write 前 sha de1c9bce… → 后 30a86899…）。
- 最终输入：`gold_finish_20261015/HI1/E1/split/E1A_scanA_cont_2542_2042.gjf`，38 行，sha256 `30a8689980e776471a2df9f1f9ad20a3966e74da9158b9bc81236ceaeb46b4d9`。
- L4 实测：`#p opt=(modredundant,maxstep=6) B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=DMSO)`；L8 `0 1`。
- 坐标保真自检：gjf L9–35 的 x/y/z 与种子 xyz L3–29 逐行 diff ⇒ **COORD_IDENTICAL_TO_SEED**。

### 65.4 提交与失败（attempt 1）
- `submit_compute_job`（gaussian / local / is_async / cpus 8 / memory_mb 10,240 / priority 0）⇒ **job_id = 1079**，state=ready，job_dir `gold_finish_20261015/HI1/E1/split`。
- **1079 立即失败（attempt 1）**：日志 `E1A_scanA_cont_2542_2042.log` 151 行 / sha256 `de4e9a6f9f2edd6bbe9005bff1a8d97ff114b93bfd12e5e8771526f20934ed0f` / 7,125 B / mtime 2026-10-18 02:52:18.457442750。详见 §66。
- 该次提交是本 lane 在 partial 结算后的唯一一次 post-freeze / non-delivery 计算；**未产生任何能量**（停在输入解析阶段），故对 E1a 数据面零影响。

### 65.5 报告口径预警（需协调者裁定，非本 lane 可自决）
- 口令第 10 条要求相邻几何 Kabsch 报「heavy20 与 all-41 两套」，第 8 条又写「heavy20 0.7593 / max 1.1290 / a13」「all-27 0.9853 / 1.7398 / a9」。**本模型是 27 原子体系（12 重原子 + 15 H）**，不存在 heavy20 与 all-41 原子集；本 lane 已实测的对应量为 **heavy-12 与 all-27**，且 heavy-12 最大位移出现在**工作编号原子 7**（1.1290 Å），非 a13。
- ⇒ 交付时按 **heavy-12 + all-27** 两套出表，逐项标注原子集定义与最差原子序号；「heavy20 / all-41」按**无法在本模型上产生**处理（不删项，只作命名不符说明），并回问协调者确认是否笔误。
- E1a result = barrier = **null** 不变；本段任何峰只写「候选 / 下界」；**不触发** ts_prepare / ts_resume。

## 66 job 1079（支 A 续扫 attempt 1）失败取证与修复方案（2026-10-18T02:53+08:00）

**零重提（此刻）：本 lane 未提交 attempt 2，仅在报告中提出修复方案等待口令。** 未 kill 任何作业，未碰 ts_*，交付面未动。

### 66.1 三件套
- 路径：`gold_finish_20261015/HI1/E1/split/E1A_scanA_cont_2542_2042.log`
- 行数：**151**；sha256 `de4e9a6f9f2edd6bbe9005bff1a8d97ff114b93bfd12e5e8771526f20934ed0f`；7,125 B；mtime `2026-10-18 02:52:18.457442750 +0800`。

### 66.2 failure_class 与逐字行
- failure_class = **Gaussian 输入解析错误（l101，「Wanted a floating point number」）**，不是 SCF、不是收敛、不是约束施加（与 1075 的 l103 完全不同）。
- L144 `Wanted a floating point number as input.`
- L145 `Found an integer as input.`
- L146 `B 2 18 S 5 -0.1000`
- L147 `?`
- L148 `Error termination via Lnk1e in /home/ly/g16/l101.exe at Sun Oct 18 02:52:18 2026.`
- L149 `Job cpu time:       0 days  0 hours  0 minutes 11.9 seconds.` / L150 `Elapsed time:        0 days  0 hours  0 minutes  1.5 seconds.`
- 另：l1 解析后回显的**全部 27 原子符号与坐标正常**（L116–L143），路由回显正常（L87–L88）。

### 66.3 根因（可判定，非猜测）
- 分子坐标块与 modredundant 卡片之间**缺空行**：写盘时把 `B 2 18 S 5 -0.1000` 直接接在末原子行之后，Gaussian 把该卡片当作原子行解析（首字符 B 视为元素符号亦可，但随后 `2` 处要求浮点数）⇒ 报整数错误。
- 对照：1072 / 1077 的既有成功输入均为「末原子行 → 空行 → 扫描卡片 → 空行」布局；本次我漏掉了末原子行后的空行。

### 66.4 修复方案（待口令，只改格式不改科学设定）
- 新输入 `E1A_scanA_cont_2542_2042_v2.gjf`（新后缀、不覆盖任何既有文件），内容 = 本次输入 + 在末原子行后插入一个空行；路由、约束、坐标、引擎、方法口径全部不变。
- 预计提交参数不变：8 cpus / 10,240 MB / priority 0。
- 若协调者认为「零 re-submit」亦涵盖本次输入格式修复，请明确禁止，本 lane 保持不再提交并只留本取证。
## 67 判读更正：1074 不是「停滞」，是 stdout 块缓冲（2026-10-18T02:54+08:00）

**零动作：未 kill、未重提、未改任何作业；交付面未动。**

- 我此前（§64/回报第 8 条）以 log 大小 19,577,855 B 与 mtime 02:28:07.721 不变判「仍处停滞」，**依据不足，已更正**。
- 协调者 as_ec848a7673b74e35 的独立实测（02:49:5x）：g16 主进程 pid 1234203 存活（ELAPSED 06:49:55）、scratch `/home/ly/g16/scratch/Gau-1234209.rwf` 236,371,968 B 且 mtime 02:49:06.045 → 02:49:56.173 持续推进 ⇒ **作业在算，log 只是按块缓冲**。
- 本 lane 采纳的判据（升级）：**log 最近写入时间不得单独作为挂死判据，须与 .rwf mtime 或进程存活联合判**。今后本 lane 描述 1074 只写「log 自 02:28:07 静默（缓冲），进程/.rwf 判活由协调者核」。正确处置是核对平台 monitor（命令行含 `--timeout 1800`），不是 kill 重投。
- §64 中 1075 的取证结论**不受此更正影响**（1075 已由 l103 真终止，L103876 逐字终止行 + mtime 22:44:01 固定），仍按「只登记、不作 E2 证据、E2 result/barrier 恒 null」执行。

## 68 等待点（本 lane 当前唯一动作 = 等口令）

- 支 A attempt 1（job 1079）因输入缺空行在 l101 失败，取证见 §66；**是否允许 _v2 格式修复重试，等主协调 as_a341823c436e47ed 一句话口令**；未获口令前不再提交。
- 「heavy20 / all-41」原子集与 27 原子模型不符，等主协调确认（本 lane 拟按 heavy-12 + all-27 出表并标注定义）。
- E1a result = barrier = **null** 不变；未触发 ts_prepare / ts_resume；不碰 ts_0015·ts_0016·ts_0020·ts_0006。
## 69 主协调批准 v2 格式修复重试 + 提交 job 1080（2026-10-18T02:54+08:00）

### 69.1 口令（来源 as_a341823c436e47ed，本 lane 记账 2026-10-18T02:53:5x）
- 批准：**一次性**格式修复重试；唯一改动 = 末原子行与 modredundant 卡片之间插入一个空行；路由/约束/坐标/引擎/方法口径全不变；8 cpus / 10,240 MB / priority 0。
- 约束：v2 若再现 l1xx 或任何非 Normal termination ⇒ **立即停、只留取证、不再重试**并报；此批准**不扩展到任何其他重试**（1075 仍不重投）。
- 原子集口径：协调者确认 **「heavy20 / all-41」是笔误**（照抄 E3b 的 41 原子口径），本模型 27 原子（12 重 + 15 H）⇒ 报告用 **heavy-12 + all-27**，须标注元素筛选规则与原子编号来源（工作编号 / 输入序号）。

### 69.2 种子与参照同构核对（提交前，逐项单独命令）
- 种子 sha256 = `f1ff21307918afaa6afa921f244969122b40f94183883d01bc2a232f4d8055e2` ✅（1,118 B / mtime 2026-10-17 20:28:04.107574788 / 27 原子）。
- 既有成功输入卡片行号：`E1A_constrained_scan_R2692_2192_stepneg.gjf` L37 = `B 2 18 S 10 -0.0500`（38 行）；`E1A_scan_cont1_C2N18.gjf` L37 = `B 2 18 S 5 -0.1000`（38 行）。
- v2 实测：**距 38 行**、卡片在 **L37**、L35 = 末原子、L36 = 空行、L37 = 卡片、L38 = 空行（cat -A 确认 `$` 结尾）⇒ **与 1072/1077 同构**。

### 69.3 v2 输入
- 路径：`gold_finish_20261015/HI1/E1/split/E1A_scanA_cont_2542_2042_v2.gjf`；38 行；**1,740 B**；mtime `2026-10-18 02:53:58.799019343 +0800`；sha256 `3b77f40c727070cffa0dc506ff8e48e55a057fcfb1087dbfe88878a338402e00`。
- 坐标保真：gjf L9–35 与种子 xyz L3–29 逐行 diff ⇒ **COORD_IDENTICAL_TO_SEED**（仍由 qm_input_writer 从同一种子生成，未手写）。
- v1→v2 diff 三处、逐一分类：(a) `%chk` 文件名随新后缀变化（机械项）；(b) 标题行加 v2 说明（注释项）；(c) **坐标块与卡片之间新增一个空行**（唯一实质改动，卡片由 L36 移到 L37，与 1072/1077 同构）。除此外无其它差异。

### 69.4 提交与队列快照
- 提交前队列：running = [1074（8 cpus / 10,240 MB / priority 0，起于 2026-10-17T20:28:54）]；queued 空；node-local free = 9 slots / 24 cpus / 40,960 MB；terminal 新增 1079 failed @2026-10-18T02:52:25。
- `submit_compute_job`（gaussian / local / async / cpus 8 / memory_mb 10,240 / priority 0）⇒ **job_id = 1080**，state=ready，job_dir `gold_finish_20261015/HI1/E1/split`。
- 提交后即刻队列：running 仍只列 1074（1080 处于起步/调度中）；free 未变。
- 输出日志预期 `E1A_scanA_cont_2542_2042_v2.log`（新后缀，未覆盖任何既有文件）。

### 69.5 定性（不变）
- post-freeze asset / non-delivery / 非 guess / 非鞍点；ΔE 只对支 A 内部相对本段首点、标「非 ΔE‡」、**禁与 1077（支 B）或 cont1 拼接或相减**；**E1a result = barrier = null 不变**；任何峰只写候选 / 下界；**不触发** ts_prepare / ts_resume；零 kill（含 1074）。
## 70 job 1080（v2 支 A 续扫 attempt 2）终态：**外部 SIGTERM 终止**于第 3 点；仅 2/6 点收敛（2026-10-18T03:37+08:00；性质于 03:56 更正，见 §72）

**零动作声明：未做第三次提交、未 kill、未改任何既有文件、未 ts_resume、未碰 ts_*；交付面 277 行 a2964d8d… 未动；E1a result = barrier = null 不变。** 按放行口令第 4 条「v2 若再现 l1xx 或任何非 Normal termination ⇒ 立即停、只留取证、不再重试」，本次不重试。

### 70.1 输入（提交时）
- `gold_finish_20261015/HI1/E1/split/E1A_scanA_cont_2542_2042_v2.gjf`；**38 行**；**1,740 B**；mtime `2026-10-18 02:53:58.799019343 +0800`；sha256 `3b77f40c727070cffa0dc506ff8e48e55a057fcfb1087dbfe88878a338402e00`。
- 结构：L4 路由 `#p opt=(modredundant,maxstep=6) B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=DMSO)`；L8 `0 1`；L35 末原子；L36 空行；L37 `B 2 18 S 5 -0.1000`；L38 空行（与 1072/1077 同构）。

### 70.2 日志（同轮实测，逐项单独命令，读取于 2026-10-18T03:36:04+08:00）
- 路径：`gold_finish_20261015/HI1/E1/split/E1A_scanA_cont_2542_2042_v2.log`
- 行数：**47,015**；sha256 `7f11a2628c0c0b39db8d242bb695c675890dd1d908595815ae1a26fbc24b0c5f`；字节 **2,965,446**；mtime `2026-10-18 03:34:43.710427783 +0800`。
- 包装日志（诊断用，非证据）：`.cloudra/calc-1080.out.log` 33 行 / 1,618 B / mtime `2026-10-18 03:34:45.173349804`。

### 70.3 终止性质（非 Normal termination）
- 原生日志内 `Normal termination` **0 次**、`Error termination via` **0 次**；平台作业状态 = **cancelled**（推送 2026-10-18T03:34:4x）。
- 包装日志逐字：L1 `[calculator] isolated GAUSS_SCRDIR=/home/ly/g16/scratch/cloudra_g16_task1080_1781993`；L2 `Error: software termination`；L9 `Error: software termination`；L16–L33 为 backtrace，栈顶 L17 `  /home/ly/g16/l502.exe() [0xf84dd4]`、L33 `  /home/ly/g16/l502.exe() [0x40d169]`。
- ⇒ **failure_class（2026-10-18T03:56 更正，见 §72）= 外部 SIGTERM 终止（信号 15）**：`calc-1080.exit.json` exit_code = **−15**（22 B，mtime 2026-10-18 03:34:45.026188639）；`guard-1080.log` 末行「calculator 退出，退出码：**241**」= 256−15（181 B，mtime 03:35:58.134836623）。
- **不再使用**「Gaussian 内部软件终止 / l502 段错误」的定性：包装日志的 `Error: software termination` + 寄存器转储 + l502 backtrace 是 **Gaussian 收到 SIGTERM 时的标准输出**（全线已见 1080 l502、1074 l703、1087 l703 三例），**不能区分内部崩溃与外部终止**。仍成立的部分：**不是** l101 输入解析、**不是** l103 约束施加、**不是** NStep 步数耗尽、**不是** SCF 不收敛报错。
- 原生日志末行上下文（逐字）：L46990 `DIIS: error= 2.78D-03 at cycle   1 NSaved=   1.`；L47001 `Cycle   2  Pass 1  IDiag  1:`；L47003 `E= -593.931117463493     Delta-E=       -0.002045361465 Rises=F Damp=F`；L47014 `Cycle   3  Pass 1  IDiag  1:`；L47015 `RMSU=  2.65D-05    CP:  1.00D+00  1.06D+00`（此后无输出）。

### 70.4 进度与末计数行
- `Optimization completed` 共 **2 次**：L1343（pt1）、L40451（pt2）。
- 末计数行逐字 L46495 `Step number   9 out of a maximum of  152 on scan point     3 out of     6`。
- ⇒ **6 点中仅 2 点收敛**（scan point 1、2），scan point 3 在 step 9→10 之间崩溃；scan point 3–6 **缺测**（4 点无数据，不插值、不外推）。

### 70.5 两个收敛点的末次 SCF Done（行号 + 能量）
- **pt1**：`SCF Done` L790 `E(RB3LYP) =  -593.931626205     A.U. after   12 cycles`；收敛行 L1343 `Optimization completed.`。
- **pt2**：`SCF Done` L40160 `E(RB3LYP) =  -593.932746675     A.U. after    8 cycles`；收敛行 L40451 `Optimization completed.`。
- 收敛帧导出（*只读 Optimization completed 之后的 orientation 块*）：`E1A_scanA_cont_2542_2042_v2_pt1.xyz` sha256 `9590138961f2c5105644c41c364629a344562f67bd885704adc9339e6184be30`（源块 L480–511）、`…_pt2.xyz` sha256 `0787686bd16f66b7f28c062a4d6e837838eba3d80a7d8e86b1d43124349d0aa6`（源块 L39924–39955），各 29 行 / 27 原子。

### 70.6 逐点几何与相对能量（**非 ΔE‡**；仅支 A 内部，相对本段首点；不与 1077 / cont1 / 1072 跨段拼接或相减）
| 点 | 目标 R(2,18) | 实测 R(2,18) | C2–O3 | N18–H27 | O3···H27 | minsep | E (a.u.) | ΔE vs pt1 (kcal/mol) | 收敛行 |
|---|---|---|---|---|---|---|---|---|---|
| pt1 | 2.5420 | 2.5420 | 1.2210 | 1.0151 | 2.5575 | 0.9741 (13–19) | −593.931626205 (L790) | 0.00 | L1343 |
| pt2 | 2.4420 | 2.4420 | 1.2235 | 1.0155 | 3.1012 | 0.9745 (13–19) | −593.932746675 (L40160) | **−0.70**（非 ΔE‡） | L40451 |
| pt3–pt6 | 2.3420 / 2.2420 / 2.1420 / 2.0420 | — | — | — | — | — | — | **缺测（崩溃）** | — |
- 门限核对（对两个收敛点）：|实测−目标| = 0.0000 Å（≤0.002 ✅）；C2–O3 1.2210/1.2235 ∈ 1.22–1.28 ✅；N18–H27 1.0151/1.0155 ≪ 1.10 ✅；minsep 0.9741/0.9745 ≥ 0.90 ✅（无碰撞买来的距离）。
- 1 Eh = 627.509474 kcal/mol；ΔE(pt1→pt2) = (−593.932746675 + 593.931626205) × 627.509474 = **−0.7031 kcal/mol**。

### 70.7 相邻几何 Kabsch（pt1 → pt2；R 作用于前点→后点；SVD；det(R) 强制 +1）
- **heavy-12**（元素筛选：非氢；共 12 个；编号 = 工作编号 = 该 27 原子 xyz 顺序 1 基）：n=12，det(R) = **+1.000000**，rms = **0.7390 Å**，max|Δ| = **1.0821 Å**，最差原子 = **工作编号 3**；前五：3:1.0821、13:1.0805、17:1.0033、4:0.9759、1:0.7615。
- **all-27**（全部 27 原子含 15 H）：n=27，det(R) = **+1.000000**，rms = **0.9631 Å**，max|Δ| = **1.7259 Å**，最差原子 = **工作编号 9**；前五：9:1.7259、26:1.4917、5:1.4692、25:1.3809、19:1.3714。
- 三条合成自检（脚本 `split/scripts/e1a_scanA_kabsch.py` sha256 `21ca3dab7b76b37311419ace8ff43b56214a74d747612737e766b1159f3d02f8`）：①已知旋转+平移 ⇒ rms **0.000000 Å** / max 0.000000 / det +1.000000；②镜像副本 ⇒ rms **1.9084 Å** / max 3.6425 / **det_raw = −1**（+1 修正后 det(R_used) = +1）；③同结构副本 ⇒ rms **0.00000000 Å** / max 0.00000000 / det +1.000000。
- 原子编号口径：本节一律给**工作编号**（= 该 27 原子结构文件顺序，1 基）。原始/任务 atom-map 号仅对已确证的四个位置可写：工作 2 = 任务 C2、工作 3 = 任务 O4、工作 18 = 任务 N20、工作 27 = 任务 H21；其余原子（含本节最差原子 3 以外的 13/17/4/1/9/26/5/25/19）**任务编号不在本 ledger 重述**（避免臆造，需引用 ts run 的 atom_map 时另行核对）。

### 70.8 构象判读（关键，影响 ΔE 的可解释性）
- τ(3,2,18,14)（本 lane 带符号二面角）：pt1 = **−130.97°**、pt2 = **−64.74°** ⇒ |Δτ| = **66.23°**；O3···H27 2.5575 → **3.1012 Å**。
- pt1 与种子 `E1A_neg_scan_p4_R2542_branchA.xyz` 的四个描述量完全一致（τ −130.97、R(2,18) 2.5420、R(2,3) 1.2210、R(18,27) 1.0151、O3···H27 2.5575）⇒ pt1 即种子，符合预期。
- ⇒ **pt1→pt2 之间发生了一次与 sp4→sp5「分支切换」同量级的构象重排**（heavy-12 rms 0.7390 / max 1.0821；对照 sp4→sp5 的 0.7593 / 1.1290）。因此 **ΔE = −0.70 kcal/mol 不能读作「C2–N18 缩短 0.10 Å 的纯势能响应」**，其中含构象项；本段不可作为单支刚性弛豫序列处理。

### 70.9 结论（按放行口令的措辞纪律）
- 本段**只有 2/6 点收敛**（pt1 R=2.5420、pt2 R=2.4420），pt3–pt6 因 l502 崩溃缺测；**不能**写「本段 6/6 收敛、无内部极大、严格单调」——该结论在本段不成立/不适用。
- 已收敛两点间能量下降 0.7031 kcal/mol（非 ΔE‡），但**伴随构象切换**，故只能作为支 A 内部的相对记录，不构成势垒/峰的任何证据，也不得与支 B（1077/cont1）拼接或相减。
- 全段无任何可识别内部极大：仅因缺测，不构成「无极大」的证明；亦不得写「通道不存在」。
- **E1a result = barrier = null 不变**；未触发 ts_prepare / ts_resume；未做第三次提交（按口令第 4 条）。
### 70.10 协调者独立复核与停止决定（2026-10-18T03:38:07，来源 as_a341823c436e47ed）
- 我方 1080 三件套（47,015 行 / 7f11a262… / 2,965,446 B / mtime 03:34:43.710427783）经其逐位独立复测**完全一致**；`Optimization completed` = 2、`Normal termination` = 0、`Error termination` = 0、末计数行 Step 9 / 152、scan point 3 / 6；包装日志 l502 backtrace 判断与其一致。
- **停止决定（口令）**：不做第三次提交；1080 的 v2 输入与日志保留为 post-freeze asset / non-delivery，**不覆盖、不改写**。

### 70.11 覆盖度与措辞（按协调者要求逐字落账）
- **覆盖 2.5420 → 2.4420 两点，2.4420 以下无数据**（pt3–pt6 = 2.3420 / 2.2420 / 2.1420 / 2.0420 缺测，不插值、不外推）。
- 构象限制：τ(3,2,18,14) −130.97° → −64.74°（|Δτ| 66.23°）、O3···H27 2.5575 → 3.1012 Å，配 heavy-12 0.7390 / 1.0821 / 工作编号 3 与 all-27 0.9631 / 1.7259 / 工作编号 9 ⇒ pt1→pt2 为**构象重排**（与 sp4→sp5 的 0.7593 / 1.1290 同量级），本段**不是单支刚性弛豫序列**，ΔE −0.7031 kcal/mol 不得读作 C–N 缩短 0.10 Å 的纯势能响应。
- 三自检与编号口径原样保留：旋转+平移 0.000000 / 镜像 rms 1.9084（det_raw −1）/ 同结构副本 0.00000000；编号 = 27 原子文件顺序（工作编号 1 基），任务 atom-map 仅写已确证四处（工作 2=C2、工作 3=O4、工作 18=N20、工作 27=H21），其余不臆造。
- 禁止措辞：不写「本段无极大」「通道不存在」（2/6 缺测不构成无极大的证明）；ΔE 只作支 A 内部相对差、标非 ΔE‡、不入任何跨段/跨支表。

### 70.12 环境（协调者 03:38 实测，本 lane 记录，不行动）
- running = 1074(8) / 1082(8) / 1087(8) / 1092(4) / 1093(4)；free = 5 slots / **0 cpus / 0 MB** ⇒ 满载；1074 仍在算，**不 kill**、不以 log 静默判死锁（以 .rwf 十秒级刷新为准）。
## 71 平台元数据另一叙述 + 重复件 1089 孤儿进程（2026-10-18T03:40+08:00，只读）

**零动作：未 kill 任何进程（含孤儿 1089）、未第三次提交、未 ts_resume、未改任何文件、交付面未动。**

### 71.1 平台元数据（本轮实测，`query_compute_queue` terminal）
- **1080**：state = **cancelled**，ended_at **2026-10-18T03:35:58+08:00**，last_error = `D23 cancel: HI1_E1a direction-disproven; cores reallocated to 1093/1095/1096`。
- **1089**：state = **cancelled**，ended_at **2026-10-18T03:36:55+08:00**，last_error = `D23 cancel: duplicate of 1080 (same E1a scan R2.5420->2.0420); edge direction-disproven`。
- ⇒ **顺序（2026-10-18T03:56 更正定性）**：(i) **外部 SIGTERM 终止**：calculator 退出码 −15 / 241，exit.json mtime 03:34:45.026188639，guard 记账 mtime 03:35:58.134836623；(ii) **平台事后记账**：state=cancelled、ended_at 03:35:58，附第三方理由串。故 `direction-disproven` 是**事后记账与事后归因**，不作终止原因、**不入交付证据链**、本 lane 不采信为结论；**也不再写「崩溃时刻」**（SIGTERM 与「软件终止」打印同时刻，73 s/72.8 s 只是记账延迟）。§70 的数据面（2/6 收敛、pt3–pt6 缺测、非 ΔE‡）全部保持。
- 说明：本行原写「因果不可分」，现按新时序证据收窄为「先撞击、后取消」——属**有据修订**（非静默改写），依据 = v2.log / 包装日志 / 平台 ended_at 三个独立时间戳。

### 71.2 重复件 1089（**非本 lane 提交**）
- 输入 `gold_fill_20261018/HI1/HI1_E1a_scanfix/HI1_E1a_scanA_cont_2542_2042_fix1.gjf` sha256 `cb87a45a9c5286709deb57ba7ac62f999a72937ae69e07c9a2d3a5aa0930c263`（1,771 B / mtime 2026-10-18 03:07）；与本 lane v2 的差异据协调者为 %chk 路径、%mem=6GB（v2 为 10240MB）、标题行、末尾空行少一个；路由/约束/坐标相同。
- 台账**不接受**其为本 lane 证据：%mem 不同 ⇒ 非同一次计算的等价重复，且其提交、取消与进程处置均不在本 lane 权限内。
- 孤儿进程（本轮实测）：`ps -o pid,stat,etime,pcpu,comm -p 1867365` ⇒ pid **1867365 / STAT SN / g16 存活**；`fix1.log` = **247,617 B / 3,895 行 / mtime 03:39:55.701592068**（仍在增长）、`fix1.chk` = 8,310,784 B / mtime 03:39:55.597589673 ⇒ **取消只停记账、未停计算**。
- 负荷后果：本 lane 观察到的 running = 1074(8) / 1082(8) / 1087(8) / 1092(4) / 1094(4)，free = 5 slots / **0 cpus / 0 MB**；若计入孤儿 1089 的 8 cpus，实际并发超过注册配额，单步变慢属预期。**本 lane 不处理孤儿**（处置权在主协调/平台）。

### 71.3 边界重申
- 本 lane 仍**不做第三次提交**；不 kill 1074、不 kill 1089-孤儿、不改 priority、不 ts_resume；不触碰 ts_0015·ts_0016·ts_0020·ts_0006；不碰交付面（277 行 / a2964d8d…）。
- **E1a result = barrier = null 不变**；ΔE −0.7031 kcal/mol 仅是支 A 内部相对差、标非 ΔE‡、禁与 1077/cont1 拼接；不写「本段无极大」「通道不存在」。
- 若后续任何来源（含 1089 孤儿）产出该段数据，须先经主协调明示授权并以**其自身日志三件套**登记，方可作为独立记录引用，且**不得**与本 lane §70 的两点混算。
## 73 ts_0015 只读巡检（第八轮，2026-10-18T04:05:02+08:00）

**零动作：未 ts_resume、未提交、未删锁、未 kill、未碰 ts/ 下任何文件。**
- 自证：`test -d jobs/declaration_0001/frequency` ⇒ **FREQ_DIR_NO**；`ls jobs/declaration_0001/` ⇒ 仅 `ts_opt`；`.pipeline.lock` 存在（未动）；`process.json` = **30,059 B / mtime 2026-10-17 14:36:37.092354393**（冻结约 **13 h 28 m**）。
- `ts_inspect(ts_0015)` 只读记录：revision **11**、**status = isolated**、stage **refine**、**result = null**、waiting_for = job **1055**（purpose ts_opt，state **done**，**evidence = null**，log `jobs/declaration_0001/ts_opt/refine.log`）；available_results 显示 declare/build/map/assemble/guess 均 done（guess: `Provided candidate bound; formal optimization and verification remain required.`），无 frequency 阶段目录。
- 判读：仍为 **#197「ts run 在 stage 间推进处特定挂起」**，不是作业失败、不是输入被拒；本轮**无 frequency 阶段**，故不触发频率分析模板、不产生任何 ΔE‡、不改交付面。
## 74 事件类①：job 1074（E3b 6×6 扫描）已终止——外部 SIGTERM，无 Gaussian 终止行（2026-10-18T04:58+08:00，只读）

**零动作：未 kill、未提交、未 ts_resume、未改任何文件。** 本条为只读记录与事件上报（对象 as_ec848a7673b74e35）。

### 74.1 三件套与终止元数据（逐项单独命令，2026-10-18T04:58:01+08:00 实测）
- 主日志 `gold_finish_20261015/HI1/E3/runs/e3b_scan2d_c2n4_o25h26.log`：**303,154 行** / **19,577,855 B** / sha256 **9044f74b2dd8678f69e07b8eeaadc903694070a18d8c644ec400ab8bf5b49cfe**（与协调者 02:54:01 读数同值 ⇒ **内容未变**）/ mtime **2026-10-18 04:53:47.743635472**（mtime 变化来自收尾写入，字节数与行数未变）。
- `guard-1074.log`（181 B / mtime **04:53:47.613998195**）三行逐字：L1 `[guard] Gaussian scratch: /home/ly/g16/scratch/cloudra_g16_task1074_1234148`；L2 `[guard] calculator 启动 (PID 1234195)，等待其结束...`；L3 `[guard] calculator 退出，退出码：241`。
- ⇒ **241 = 256 − 15 = SIGTERM（信号 15）外部终止**；该目录下**无** `calc-1074.exit.json`（与 1080 情形不同，只有 guard 记账）。
- 进程：`ps -o pid,stat,etime,pcpu -p 1234203` ⇒ **无输出（进程已退出）**；scratch `Gau-1234209.rwf` = 236,371,968 B / mtime **2026-10-18 03:45:35.805260811**（末次推进后停止）。

### 74.2 主日志内终止行：**不存在**
- `grep -n 'Normal termination of Gaussian'` = **0 次**；`grep -n 'Error termination via'` = **0 次** ⇒ 无正常终止行、无 l103/l101/9999 类终止行；按 21:17 纪律，**不得**因此写「作业失败」以外的科学定性，只登记「外部 SIGTERM 截断」。
- 末 15 行逐字（行号）：L303140 `E= -939.251869210573     Delta-E=       -0.000000006260 Rises=F Damp=F`；L303143 `ErrMax= 6.77D-07  0.00D+00 EMaxC= 1.00D-01 BMatC= 5.12D-10 BMatP= 7.14D-09`；L303150 `RMSDP=9.04D-08 MaxDP=4.56D-06 DE=-6.26D-09 OVMax= 7.04D-06`；L303152 `Cycle   9  Pass 1  IDiag  1:`；L303153 `RMSU=  7.49D-08    CP:  1.00D+00  1.08D+00  6.78D-01  8.87D-01  6.92D-01`；L303154 `                   CP:  6.19D-01  7.78D-01  8.37D-01`（文件到此结束，无终止块）。

### 74.3 进度（内容未变，仅登记）
- `Optimization completed` = **17**；`on scan point 19 out of` = **0 次** ⇒ scan#18 仍未收敛、col3 缺末行、17/36、候选 0。（与协调者 03:41 判读一致。）
- 队列（04:57:56 实测）：**running = 空**、queued 空、node-local free = 10 slots / **32 cpus / 51,200 MB**。

### 74.4 边界
- E3b 属他关心边，**result / barrier 仍 null**；本 lane 不以其任何数值入表。本 lane 的 E1a result = barrier = **null** 不变；未提交、未 kill、未 ts_resume、交付面 277 行 a2964d8d… 未动。
- 判死纪律（§72.4）适用：以 guard 退出码 241/−15、`.rwf` 停止推进（03:45:35.805260811）、主日志无终止行为据；主日志 mtime 只作辅证。
## 75 取证陷阱更正：1074 的 log / guard 日志在 04:53:47 被「同内容重写」，其 mtime 自此失效（2026-10-18T04:59+08:00，只读）

**零动作：未提交、未 kill、未 ts_resume、未改任何文件；交付面未动。**

### 75.1 现象（本 lane 独立实测，2026-10-18T04:58:47+08:00）
- `guard-1074.log`：181 B / **sha256 7172971b6efa0f3ad141aea03d136ee5a20e2789d2f88b3faebd6d63b542b8a4** / mtime **04:53:47.613998195**。
- `calc-1074.out.log`：**1,581 B / 32 行** / **sha256 f9e73b64815b76fdf38c497793a21cf49b47f2feef7d7aa78cc5b85911a79d6d** / mtime **04:53:47.613998195**；L2 `Error: software termination`、L10 `  /home/ly/g16/l703.exe() [0xdca494]`、L11 `Error: software termination`（Gaussian 收 SIGTERM 的标准输出）。
- 主日志 `e3b_scan2d_c2n4_o25h26.log`：**303,154 行 / 19,577,855 B / sha256 9044f74b…**（内容与 02:54 同值）/ mtime **04:53:47.743635472**。
- **关键**：三个文件构成**一组**重写（guard 与包装日志的 mtime **为同一微秒时间戳 04:53:47.613998195**，主日志晚 **0.1296 s**），而**字节数与 sha256 全部未变**；`.rwf` 未被重写（仍 03:45:35.805260811）⇒ 这是**归档/回写或 touch 类批量操作**，**不是计算行为**。mtime 失效范围 = **这三件**（guard、包装日志、主日志）。

### 75.2 更正与影响范围
- **此后不得再用 1074 主日志与 guard 日志的 mtime 作「最后写入时刻」**；其权威标识改为 **sha256 + 字节数**。本 lane §74.1 所记 mtime（04:53:47.xxxx）应读作「**重写之后的 mtime**」，不是计算结束时刻；此前协调者侧 03:47:00.785418768 一类读数应标为「**重写前的历史 mtime**」。
- 1074 的真实终止时刻链（据协调者 as_ec848a7673b74e35 复核，本 lane 独立复核其两端证据）：`.rwf` 停写 **03:45:35.805260811** → 包装日志 `software termination` **03:45:46.453373043** → guard「退出码 241」→ 平台 ended_at **03:47:00**（平台条目已被后续作业挤出 terminal 列表，本 lane 现无法直接复读，按协调者记录登记）。
- §74 的科学性结论不受影响：内容面 303,154 行 / 17 个 `Optimization completed` / `on scan point 19 out of` = 0 / 无任何 Gaussian 终止行 ⇒ **scan#18 未收敛、col3 缺末行、17/36、候选 0**；E3b result/barrier 仍 **null**，本 lane 不入表。

### 75.3 纪律补一条（与 §72.4 四级制兼容）
④ 若某文件在作业终态之后 mtime 被改动而 sha256 未变，判为**归档/回写**，**不得**据此重开判活或改动结论；判活只对**仍在跑**的作业有意义。终态认定顺序：guard 退出码 / exit.json → `.rwf` 停止推进 → 平台记录 → 主输出（仅辅证）。

### 75.4 资源与授权边界
- 队列（04:58:21–04:58:47 实测）：**running 空、queued 空、free = 10 slots / 32 cpus / 51,200 MB** ⇒ 资源式门槛（free cpus ≥ 8 且 running ≤ 2）**首次满足**；但 (r2,c4)≈pt23 单点、E2 cont2、支 B 2.9543 单点、E3b 加密网格/扩窗等**仍需主协调点名授权 + 新文件名**，本 lane **不自行提交**。
- 另记（非本 lane 业务，仅登记事实）：同期 terminal 出现 1104 failed（退出码 137）/ 1115 failed（PATH 缺程序）/ 1117·1111·1118 failed（l9999），不由本 lane 处置。
- E1a result = barrier = **null** 不变；交付面 277 行 a2964d8d… 未动；未提交 / 未 kill / 未 ts_resume / 不碰 ts_*；不写「该窗口无驻点」。

### 75.5 终态窗口滚动的后果（2026-10-18T05:00+08:00 实测）
- 1074 已**滚出** `query_compute_queue` 的 terminal 段：本 lane 04:58:47 的 recent_terminal(6) 已无 1074（其位被 1104/1115/1117/1111/1118/1112 等占去）⇒ **`ended_at 03:47:00` 与 last_error 逐字串今后只能引「当时落账的条目快照」**（协调者 03:50 条目即当时实测记录），**不得**因窗口滚动改写成「未终止 / 找不到」。这是「引历史终态只用各自条目快照」纪律的第二次实证。
- 1074 内容面结论（不变）：17 个 `Optimization completed`、`Normal termination` / `Error termination via` = 0 / 0、`on scan point 19 out of` = 0、末行 L303140 / L303150 / L303152 / L303153–154 无终止块 ⇒ scan#18 未收敛、col3 缺末行、17/36、候选 0；**E3b result/barrier 仍 null**、本 lane 不入表。
## 76 收文登记（无动作）：E3b 网格坐标自纠 + 原子集口径互不适用（2026-10-18T05:01+08:00）

**零动作：未提交、未 kill、未 ts_resume、未改任何文件；本条只作收文与口径隔离登记。**
- 收到 as_ec848a7673b74e35 的自纠：其此前对我的口述「(r2,c4) = R(2,4)=1.4248、只改一轴」有误，正确为 **(r2,c4) = (R(2,4)=1.6248, R(25,26)=1.7193)**；种子帧 = pt14 收敛帧（SCF L182507 = −939.225689108，六距离 R(2,4)=1.6248 / R(25,26)=1.4693 / R(4,26)=2.3243 / R(10,27)=0.9949 / R(2,25)=1.3793 / R(2,26)=2.1690）。
- **该网格属 E3b 边、不属本 lane（HI1_E1）**：本 lane 不做 (r2,c4) 取点、不代提交、不以任何 E3b 数值入表；相关报告由其自身负责。
- **原子集口径隔离（防串用）**：E3b 侧用「heavy20 / all-41」；本 lane 的 E1a 模型为 **27 原子（12 重 + 15 H）**，只用 **heavy-12 + all-27**（已由主协调 §R206 (e)/§R208 勘误确认）。两套编号体系**不得互换引用**。
- 取证纪律照收：新作业若发生收尾同内容重写，不得以 mtime 作最后写入时刻；判活只用 `.rwf` 十秒级刷新 + 进程存活；判死用 guard 退出码（0 正常 / 241 ≡ −15 SIGTERM）/ exit.json / `.rwf` 停写时刻；日志终止消息仅辅证。
- 边界不变：E1a result = barrier = **null**；交付面 277 行 a2964d8d… 未动。
## 77 ts_0015 只读巡检（第九轮，2026-10-18T10:00:46+08:00）

**零动作：未 ts_resume、未提交、未删锁、未 kill、未碰 ts/ 下任何文件。**
- 自证：`test -d jobs/declaration_0001/frequency` ⇒ **FREQ_DIR_NO**；`ls jobs/declaration_0001/` ⇒ 仅 `ts_opt`；`.pipeline.lock` 存在（未动）；`process.json` = **30,059 B / mtime 2026-10-17 14:36:37.092354393**（冻结约 **19 h 24 m**）。
- `ts_inspect(ts_0015)`：revision **11**、status **isolated**、stage **refine**、**result = null**、**blocked = null**、waiting_for = job **1055**（ts_opt，state **done**，**evidence = null**）；available_results 全为 done（declare / build / map / assemble / guess / validate / submit / ts_opt）。
- 判读：仍为 **#197「ts run 在 stage 间推进处特定挂起」**；本轮**无 frequency 阶段** ⇒ 不触发频率模板、不产生任何 ΔE‡、不改交付面。
## 78 ts_0015 只读巡检（第十轮，2026-10-18T15:54:03+08:00）

**零动作：未 ts_resume、未提交、未删锁、未 kill、未碰 ts/ 下任何文件。**
- 自证：`test -d jobs/declaration_0001/frequency` ⇒ **FREQ_DIR_NO**；`ls jobs/declaration_0001/` ⇒ 仅 `ts_opt`；`.pipeline.lock` 存在（未动）；`process.json` = **30,059 B / mtime 2026-10-17 14:36:37.092354393**（冻结约 **25 h 17 m**）。
- `ts_inspect(ts_0015)`：revision **11**、status **isolated**、stage **refine**、**result = null**、**blocked = null**、waiting_for = job **1055**（state **done**，**evidence = null**）。
- 判读：仍为 **#197「ts run 在 stage 间推进处特定挂起」**；无 frequency 阶段 ⇒ 不产生任何 ΔE‡、不改交付面。
## 79 ts_0015 只读巡检（第十一轮，2026-10-18T21:51:07+08:00）

**零动作：未 ts_resume、未提交、未删锁、未 kill、未碰 ts/ 下任何文件。**
- 自证：`test -d jobs/declaration_0001/frequency` ⇒ **FREQ_DIR_NO**；`ls jobs/declaration_0001/` ⇒ 仅 `ts_opt`；`.pipeline.lock` 存在（未动）；`process.json` = **30,059 B / mtime 2026-10-17 14:36:37.092354393**（冻结约 **31 h 14 m**）。
- `ts_inspect(ts_0015)`：revision **11**、status **isolated**、stage **refine**、**result = null**、**blocked = null**、waiting_for = job **1055**（state **done**，**evidence = null**）。
- 判读：仍为 **#197「ts run 在 stage 间推进处特定挂起」**；本轮无 frequency 阶段 ⇒ 不产生任何 ΔE‡、不改交付面。
## 80 ts_0015 只读巡检（第十二轮，2026-10-19T03:43:58+08:00）

**零动作：未 ts_resume、未提交、未删锁、未 kill、未碰 ts/ 下任何文件。**
- 自证：`test -d jobs/declaration_0001/frequency` ⇒ **FREQ_DIR_NO**；`ls jobs/declaration_0001/` ⇒ 仅 `ts_opt`；`.pipeline.lock` 存在（未动）；`process.json` = **30,059 B / mtime 2026-10-17 14:36:37.092354393**（冻结约 **37 h 07 m**）。
- `ts_inspect(ts_0015)`：revision **11**、status **isolated**、stage **refine**、**result = null**、**blocked = null**、waiting_for = job **1055**（state **done**，**evidence = null**）。
- 判读：仍为 **#197「ts run 在 stage 间推进处特定挂起」**；本轮无 frequency 阶段 ⇒ 不产生任何 ΔE‡、不改交付面。








## 72 口径更正（重要）：1080 系**外部 SIGTERM 终止**，非「Gaussian 内部软件终止/l502 段错误」（2026-10-18T03:56+08:00）

**零动作：未提交、未 kill、未改任何计算文件；交付面未动。** 本节的更正**已同步改进 §70 与 §71 的正文**（有据修订，非静默改写；原措辞在修订句中显式标注「不再使用」）。

### 72.1 依据（本 lane 独立实测，逐项单独命令，2026-10-18T03:56:13+08:00）
- `HI1/E1/split/.cloudra/calc-1080.exit.json`：22 B，mtime `2026-10-18 03:34:45.026188639`，内容 L2 `"exit_code": -15`。
- `HI1/E1/split/.cloudra/guard-1080.log`：181 B，mtime `2026-10-18 03:35:58.134836623`，三行逐字 —— L1 `[guard] Gaussian scratch: /home/ly/g16/scratch/cloudra_g16_task1080_1781993`；L2 `[guard] calculator 启动 (PID 1782000)，等待其结束...`；L3 `[guard] calculator 退出，退出码：241`。
- ⇒ **241 = 256 − 15**，与 exit_code −15 同义 = **SIGTERM（信号 15）外部终止**。
- 对照：`calc-1079.exit.json`（20 B / mtime 02:52）为 l101 正常失败路径，与本条不同源。

### 72.2 更正后的定性（逐字采用协调者口径）
- 「**1080 于 2026-10-18T03:35:58 被外部 SIGTERM 终止（guard 退出码 241 / calc-1080.exit.json exit_code −15），随后平台以 state=cancelled 记账并附第三方理由串；理由串为事后记账与事后归因，不作终止原因。**」
- 撤回项：`failure_class = Gaussian 内部软件终止（l502 段错误）` **不成立**；包装日志的 `Error: software termination` + 寄存器转储 + l502 backtrace 是 **Gaussian 收到 SIGTERM 时的标准输出**（同类三例：1080 l502、1074 l703、1087 l703），不能区分内部崩溃与外部终止。
- 不再写「崩溃时刻 ≈ …」；73.5 s / 72.8 s 的「最后日志写入 → 平台终态记账」间隔只是**记账延迟**。

### 72.3 数值面一律不变（不得因本节更动）
- 覆盖度：**2/6 收敛**（pt1 R=2.5420、pt2 R=2.4420），pt3–pt6 缺测、不插值不外推；措辞「**覆盖 2.5420 → 2.4420 两点，2.4420 以下无数据**」。
- 能量：pt1 SCF Done L790 −593.931626205（收敛 L1343）、pt2 L40160 −593.932746675（收敛 L40451）；ΔE(pt1→pt2) = **−0.7031 kcal/mol**，标**非 ΔE‡**、仅支 A 内部、禁与 1077/cont1 拼接。
- 构象重排小节：τ(3,2,18,14) −130.97° → −64.74°（|Δτ| 66.23°）、O3···H27 2.5575 → 3.1012 Å；heavy-12 rms 0.7390 / max 1.0821 / 工作编号 3；all-27 rms 0.9631 / max 1.7259 / 工作编号 9；det(R)=+1；三自检 0.000000 / 1.9084（det_raw −1）/ 0.00000000；「ΔE 含构象项，不得读作 C–N 缩短 0.10 Å 的纯势能响应」。
- **不做第三次提交**；**E1a result = barrier = null**；v2 输入与日志保留为 post-freeze asset / non-delivery、不覆盖不改写；不写「本段无极大」「通道不存在」。

### 72.4 判死纪律（全线更新，本 lane 采纳并记录）
1. `guard-<id>.log` 的「calculator 退出，退出码：」（241/−15 = SIGTERM；0 = 正常；其它单独解释）；2. `calc-<id>.exit.json`；3. `.rwf` 停止推进时刻；4. 主输出/包装日志的终止消息**只作辅证**。判活仍四级制：`.rwf` 十秒级刷新 > 子进程 CPU > 终止标记计数为 0 > 主输出 mtime。
## 81 ts_0015 只读巡检（第十三轮，2026-10-19T09:23:36+08:00）

**零动作：未 ts_resume、未提交、未删锁、未 kill、未碰 ts/ 下任何文件。**
- 自证：`test -d jobs/declaration_0001/frequency` ⇒ **FREQ_DIR_NO**；`ls jobs/declaration_0001/` ⇒ 仅 `ts_opt`；`.pipeline.lock` 存在（未动）；`process.json` = **30,059 B / mtime 2026-10-17 14:36:37.092354393**（冻结约 **42 h 47 m**）。
- `ts_inspect(ts_0015)`：revision **11**、status **isolated**、stage **refine**、**result = null**、**blocked = null**、waiting_for = job **1055**（state **done**，**evidence = null**）。
- 判读：仍为 **#197「ts run 在 stage 间推进处特定挂起」**；本轮无 frequency 阶段 ⇒ 不产生任何 ΔE‡、不改交付面。

### 81.1 台账顺序说明（编排勘误，不改内容）
- 本文件当前物理顺序为 §70、§71、§73–§80、§72、§81：§72（SIGTERM 口径更正）落在 §73–§80 之后，原因是 §72 的追加锚点选在 §71 末行，而 §73–§80 的追加锚点反复落在 §73 的同一句上（该句在 §79/§80 重复出现，本轮首次尝试追加曾因多处匹配被拒：edit status=conflict，未写入）。
- 处置：**不重排既有文本**（避免破坏既有引用与 sha 链）；自 §81 起一律以「文件最后一个非空行」为锚点追加。阅读顺序请按节号，物理顺序以本节说明为准。
- 内容面无任何变化：§72 的 SIGTERM 口径更正、§73–§80 的巡检记录均逐字为当时写入版本。
## 82 ts_0015 只读巡检（第十四轮，2026-10-19T15:12:59+08:00）

**零动作：未 ts_resume、未提交、未删锁、未 kill、未碰 ts/ 下任何文件。**
- 自证：`test -d jobs/declaration_0001/frequency` ⇒ **FREQ_DIR_NO**；`ls jobs/declaration_0001/` ⇒ 仅 `ts_opt`；`.pipeline.lock` 存在（未动）；`process.json` = **30,059 B / mtime 2026-10-17 14:36:37.092354393**（冻结约 **48 h 36 m**）。
- `ts_inspect(ts_0015)`：revision **11**、status **isolated**、stage **refine**、**result = null**、**blocked = null**、waiting_for = job **1055**（state **done**，**evidence = null**）。
- 判读：仍为 **#197「ts run 在 stage 间推进处特定挂起」**；本轮无 frequency 阶段 ⇒ 不产生任何 ΔE‡、不改交付面。
## 83 ts_0015 只读巡检（第十五轮，2026-10-19T21:05:19+08:00）

**零动作：未 ts_resume、未提交、未删锁、未 kill、未碰 ts/ 下任何文件。**
- 自证：`test -d jobs/declaration_0001/frequency` ⇒ **FREQ_DIR_NO**；`ls jobs/declaration_0001/` ⇒ 仅 `ts_opt`；`.pipeline.lock` 存在（未动）；`process.json` = **30,059 B / mtime 2026-10-17 14:36:37.092354393**（冻结约 **54 h 29 m**）。
- `ts_inspect(ts_0015)`：revision **11**、status **isolated**、stage **refine**、**result = null**、**blocked = null**、waiting_for = job **1055**（state **done**，**evidence = null**）。
- 判读：仍为 **#197「ts run 在 stage 间推进处特定挂起」**；本轮无 frequency 阶段 ⇒ 不产生任何 ΔE‡、不改交付面。
- 编排说明：本节以 §82 整节为唯一锚点追加（上一尝试用「最后一个非空行」作锚点因该句在 §79–§82 重复出现被 edit 拒绝，status=conflict、未写入）；自本节起，追加锚点一律取「上一节整节文本」，确保唯一匹配。
































