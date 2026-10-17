# 最终交付报告（草稿 DRAFT，2026-10-17 07:05 CST 起笔）

> 状态：**终稿候选（快照 10:40 CST；E3 判读 11:00、NY3 参照态 11:05 补入）**。11 条边：**3 条已回填并守卫通过**（NI5_E1 = 0.93、NR1_E1 = 0.0、HL1_E1 = 0.0）、**8 条未取得 ΔE‡**——其中 **6 条按「缺测 + 缺什么 + 已证伪」定稿**（NR1_E2、HI1_E1、HI1_E2、HI1_E3（甲基伪鞍点 −128.0397 cm⁻¹）、NY3_E2、NY3_E3）与 **2 条收口前仍在跑**（HI1_EM1 = result=null、未验收（job 1032 排队）；NY3_E1 = 参照极小值已取得（job 1031：0 虚频、E_ref = −466.986564213）但 TS 与连通性未取得（job 1034 在跑））。本文件只登记**已由真实工具读数或原生日志核实**的内容；未完成项显式标注，不以估计值填充。
> 台账与巡检记录：`gold_finish_20261015/LEDGER.md`（R1–R41）。约束文件：`gold_finish_20261015/BRIEF.md`（含 §9 机理选择政策）。

## 1 任务范围
题库活跃 52 题 / 81 边中，本轮要关闭的缺口边：**HI1_E1、HI1_E3、HL1_E1、NI5_E1、NR1_E1、NR1_E2、NY3_E1、NY3_E2、NY3_E3**（9 条真缺口），外加 **HI1_E2 / HI1_EM1** 两条身份可疑旧值（13.36 / 15.52）的重算与替代。约束：2 条 PT 豁免边（NB1_E2、NQ5_E2）、8 条 impossible 边、4 条性质边不动；其余 58 条已有值边不动。

## 2 计算方法与引擎偏差声明（必读）
- 本机**无 ORCA**，全部本轮计算使用 **Gaussian 16 Rev C.01（/home/ly/g16/g16）**；级别 **B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight**，按边加 `SCRF=(CPCM,Solvent=…)`。
- 既有题库参考值由 **ORCA（5.0.2 / 6.1.1）** 产生 ⇒ 本轮数值与历史参考值之间**存在程序偏差，严禁跨程序相减或相加**；每条边的能垒只用**同一程序、同一批日志**内的纯电子能相减（不含 ZPE/热校正），且相对**该步自身起点极小值**。
- 所有被引用的原生日志均为 Gaussian 原生输出、**未改写**；引用时给出绝对路径 + sha256（+ 行号）。

## 3 已关闭的边（已回填 + gen_* + `regenerate_identically` 守卫通过）

| 边 | 值（kcal/mol） | 依据摘要 | 回填文件与 sha256 | 守卫 |
|---|---|---|---|---|
| **NI5_E1**（水相亚胺形成 C–N 加成） | **0.93** | ts_0006 全链：TS 恰 1 虚频 −164.4792 cm⁻¹、E(TS)=−286.604225293、RC-A=−286.605711957、加合物=−286.613531483；受约束单峰 job 923 p16=−286.604343399 变分自洽；端点松弛补强 job 969→RC-A、job 970→加合物 | ai.py（155 行）ecfe72de…；NI5.json a95ce872…；normal.md **771a6c7f…**（原记 5ba1f04f… 已被 NR1 对同一文件的写入取代）；tests **037a424b…**（共享文件，后经 NR1/HL1 断言同步，见 §3.1） | gen_normal_tasks --check OK；regenerate_identically 4 passed；全量 pytest 0 F/E |
| **NR1_E1**（H3O+ 质子化频哪醇） | **0.0**（约定值，非「0 垒 TS」） | 918 无约束 Opt+Freq 自坍缩到质子化频哪醇 + 水（−464.000864850，0 虚频）；903/906 合并真 PT 差坐标 21 点无内峰；929 长程 9 点单调升；973 细网格 26 点无内峰；974 定骨架单调升；977 证明 929 pt9 不是极小值 | ru.py 154650c1…（barrier 行 = L35/L57/L66）；NR1.json 6eab2f24…；normal.md 771a6c7f…；tests 037a424b…（见 §3.1）；NR1/MECHANISM_REVISION.md **2559935d…**、NR1/STATUS.md **65f120de5cee52db55ec96ef86ca2f8d1be22344436b396796582c58f8d58912（已冻结，08:05:34，55131 bytes；取代链 e1488446→…→55c1ffe8）**（§13.5 勘误：tests 两个字节版本 1d4f723b / 037a424b 不得共用同一引用值）、ADJUDICATION v3 9a187125…、E1_FINAL_EVIDENCE 2eb69ae5… | gen_normal_tasks --check OK；regenerate_identically 4 passed；-k pinacol 1 passed |
| **HL1_E1**（H3O+ 质子化肟 O） | **0.0**（声明方向无合格鞍点/相对自身起点无垒；反向受约束剖面极大 ≥ +3.5705 kcal/mol 仅下界；pt8 非已验证鞍点；非 0 垒 TS） | ts_0010 唯一 TS 候选的虚频模 = 产物侧 C3 甲基转动 pseudo-saddle（−67.9886 cm⁻¹，质量加权 88.1%，H2 仅 0.07%）；5 个「质子留在 O1」种子全坍缩（2.60/3.00/3.50 Å、双齿 → B/B′；4.20 Å → N-质子化态）；T1（job 995）独立复现 N-质子化驻点 | jl.py **944346f4…**（仅注释收紧，原 706592ea…）；hard.md 4940fa66…、HL1.json 240865b1…（未动）；HL1/round4/HL1_E1_DECISION.md **07939270…**、HL1/STATUS.md **6e3f3e24…**（§25/§26）、只读补强页 round4/HL1_CROSSCHECK.md **9d7da778…**；终版报告 round4/CALC4_REPORT.md 875a8636… | regenerate_identically 4 passed（改前基线同） |

### 3.1 与回填同步的测试断言（防「gold 已改、断言未改」的静默不一致）

回填会改变 `tests/test_benchmark.py` 里对相应边 barrier 的**期望值**；本战役共同步 3 处，均为数据（期望值）改动、**不涉及任何评分规则/生成器逻辑**，且随各包回填同轮复跑守卫：

| 断言位置 | 边 | 改动 | 复核 |
|---|---|---|---|
| L1991 | NI5_E1 | 期望表首项 0.93 | 与 ai.py 155 行一致 |
| L2062 | NR1_E1 | 期望 `[0.0, null, 5.16, 5.74]` | `-k pinacol` 1 passed |
| L2138 | HL1_E1 | `[None, 23.13, 10.44, 13.46]` → `[0.0, 23.13, 10.44, 13.46]` | 由 NR1 侧全量 pytest 发现 1 failed；主协调裁定保持 HL1_E1 = 0.0 并授权 HL1 写权会话同步（evt_ce44f06d041c480d） |

`tests/test_benchmark.py` 现盘 sha256 = **037a424b05cc5d28f0bd2540af456aedf034908d5e59525b356994d38bd8d014**；主协调在**该字节上**同轮复跑：`gen_normal_tasks --check` = check passed: 10 tasks、`-k regenerate_identically` = 4 passed、`-k "hard_replacement or pinacol"` = 2 passed、`pytest tests/test_benchmark.py` = **188 passed / 1 skipped / 0 failed**（1 skip = 既有 rdkit 类跳过）。

> **范围说明（防误述）**：本节「全量」= **tests/test_benchmark.py 单文件**。仓库级 `pytest` 仍有 **66 条 FAILED**，全部落在平台/基础设施与其它模块（test_compute / test_crest_runner / test_dag_* / test_runtime_v2_* / test_web_launcher / test_xtb_* / test_scan_interface / test_ts_* 等），**不含 test_benchmark.py 的失败**（NR1 侧 run#2 权威记录：EXITCODE=1、按进度字符统计 **通过 5343 / 失败 66 / 跳过 61**，其中失败含 **tests/test_benchmark_sandbox_fp.py** 等**其它文件**，`tests/test_benchmark.py` 本身 0 failed）⇒ 不得把「benchmark 主测试文件全绿」表述为「仓库全绿」；NR1 的门禁固定四条（gen_normal_tasks --check / 重生成 NO_DIFF / -k regenerate_identically / -k pinacol），全量 pytest 只作环境说明。

## 4 已按「明确缺测 + 缺什么 + 已证伪什么」交付的边
- **NR1_E2（I1→I2 脱水）= 缺测（保持 null，不填 16.26）**。已证伪 4 条：① 候选软鞍点（job 933，E=−463.974034272，恰 1 虚频 −74.5623 cm⁻¹）的虚频模 ±位移两端**不是** I1/I2（− 方向 = I1 家族极小值 +0.64 kcal；+ 方向 = 三元环氧鎓 + 2H₂O +15.18 kcal）；② 917 大 r 帧无约束优化落到环氧鎓（+3.62 vs I2）；③ 约束面大 r 侧 +17.2 高于 I2 的 +11.55；④ 产物侧 IDPP 未收敛（job 948 NStep=134）。**缺什么**：连接 I1 与声明 I2（碳正离子 + 2H₂O）的独立一阶鞍点或任何路径证据（native IRC = job 941 l123 积分失败，工具层无 IRC 步长/算法入口，issue #184）。16.26 只登记为「到环氧鎓异构体的候选垒（candidate_only）」。

## 5 仍在管线中（TODO，不得以估计值交付）

> **本节是 2026-10-17 09:44 CST 的历史快照，保留作演进记录；当前逐边状态以 §10（10:38 CST）与 §10.3、§10.5 为准。** 其后发生的终态：job 999（HI1_E3）done 10:30:07 → 收敛回 I2 盆地（非 TS）；job 1022 + job 1027（NY3_E1）→ RC 为一阶鞍点（1 虚频 −134.4181 cm⁻¹，羟基氢软模）；job 1026（EM1 的 IRC）failed 10:37:21 → 通道 B 第 2 次已由 ts_resume 提交（job 1032）；job 1024/1025（NY3_E2/E3）→ 软模墙已证伪。
| 边 | run | 现状（2026-10-17 09:44 CST 实读，ts_inspect） |
|---|---|---|
| HI1_E1 | ts_0008 rev29 waiting/refine | job 1017 ts_opt 运行中（08:42 起）；起点 product_seed_opt = job 1009 已收敛（E = −939.308218263，与 job 924 同值；几何 optimized_seed.xyz 5e528ea6…，Cα = S）；atom_map 已补齐并被接受（receipt tc_de20a17281f7491a，rev 20→21）；收敛后走频率门禁（117 模 + imaginary 行 + 虚频模对 7 对声明键对的投影）→ 连通性 → 两端点 → ΔE‡（相对 job 924 = −939.308218263）；**禁止再对 ts_0008 做 ts_resume** |
| HI1_E2 | ts_0009 rev33 waiting/refine | job 1008 ts_opt 运行中（07:39 起）且**在漂离**：d(1,29) 由 2.646 Å（step1）单调增至 4.75 Å（step67），电子结构始终烯胺型（C1=C2 1.358 / C2–N4 1.381）⇒ 有失败风险；**有条件预批准**：若终态不合格 ⇒ 用通道 A 自身 TS-like 帧 TS_guess_E2_j58f8.xyz（sha 5024997e…，d = 1.938 Å，CIP (8,S)(29,S)）作 provided guess 做**一次** ts_resume（changes 只含 guess 组） |
| HI1_E3 | ts_0011 rev23 waiting/refine | job 999 ts_opt 运行中（06:53 起，已 > 2.8 h） |
| HI1_EM1 | ts_0012 rev23 waiting/refine | 第一次尝试已判 **pseudo-saddle**（恰 1 虚频 −27.9419 cm⁻¹；watch-pair [1,29] 投影仅 0.078%、heavy_atom_fraction 0.322、位移前 6 大原子 5/6 为 H；几何 = 类反应物松散复合体 d(1,29) = 3.198 Å、C=O 完整；比 job 924 高 +0.014546634 Ha ≈ +9.13 kcal/mol）⇒ **不回填**、只记 candidate_only（其 IRC = job 1026 建在无效驻点上）；**通道 B 第 2 次（= 最后一次）换种子已批准**（种子 …/build/TS_guess_EM1_j58f8_faceflip.xyz sha 9f4d651a…，Re/Si 面翻转、d(C1···C29) = 1.9375 Å），但 ts_resume **被平台并发保护拒绝**（call_id tc_f74238b0861f47af，逐字 `ts_resume: active compute jobs prevent input revisions; use ts_inspect`，因该 run 的自动 IRC job 1026 仍排队且从未起跑）⇒ 已提 issue **#194**；等 1026 终态后立即重提 |
| NY3_E1 | ts_0007 rev71 waiting/refine | 第 5 版 d230（job 1022）虽收敛（29 步、四项判据全 YES、Stationary point found L13364）但**索引安全几何核对判为 RC 侧构象极小值**（仅比 RC −466.986564979 高 +0.0007 kcal/mol；D_OH 由 −152.44° 变 +159.78°）⇒ **guess 证伪**、ΔE‡ 仍缺测；job 1027（declaration_0005 frequency）排队中，只作补强登记；按 (i) 授权以 job 1023 反向弛豫扫描的脊线峰帧作**唯一**新 seed（提交前报备，仅一次），现 1023 剖面：p1 0.00（锚定 I1 = −467.004842486 @L556）/ p2 +3.70 / p3 +10.42 / p4 +16.93 / **p5 +22.23（约束 2.0271 Å）**，p6 回落（中途 ≤ +11.14，已低于 RC 的 +11.47）⇒ 内部极大在 p5 附近、疑似 p5→p6 换支，待同支核对后按三情形决定 |
| NY3_E2 | ts_0013 rev20 waiting/build | product_seed_opt = job 1024 排队第 1（seed = candD）；B′（readfc，job 1016）已证伪 |
| NY3_E3 | ts_0014 rev15 **blocked**/build | conformer_optimization_failed（job 1019 l9999：步上限 48、首 SCF −466.935846471 比 job 990 的 I2 极小值高 ≈31.4 kcal/mol ⇒ candD 是 DFT 层高能坏种子）；包外预收敛 job 1025 排队第 2 |

**NY3 统一修复路径（预先批准 + 已按证据更新）**：calcfc（job 1012）失败 ⇒ readfc（B′，job 1016）亦失败 ⇒ 走 B（换构象 candD）。1024/1025 若同型失败 ⇒ 按 R21.1 (i) 包外预收敛后经 ts_resume 交给两 run（方法级别逐字一致、同作业带 freq、priority 0、手工在飞 ≤ 2、收敛后显式登记**起点定义变化**：I2 端参考由 candA 型（job 990 = −466.986020418）改为 candD_classB 型，**新旧值不得混减**；E2 参考仍为 I1 = −467.004842485/486）；两条探针（p11 → p12）顺序执行、一次只开一个、不得删除或覆盖任何失败证据；全失败 ⇒ 转 (B)「明确缺测 + 缺什么 + 已证伪」。

**NY3_E1/E2/E3 失败链（每条只作失败登记，均不构成「该步无鞍点」证据）**：job 987（NStep=46，末帧 d 由 2.192 漂回 2.351）/ job 997（NStep=45，末帧 1.539 滑向 I1 侧）/ job 1004（收敛但 job 1010 freq 唯一虚频 −98.2487 cm⁻¹ = 甲基转子 pseudo-saddle，H 模矢占 99.49%，声明键对 O1+C4 仅 0.01%）/ job 1014（IRC l123，双向均停在 point 1）/ job 1018（NStep=45，末帧漂回 RC 2.806 Å）/ job 1022（= 上述 RC 侧极小值）/ job 1007 与 1011（ts_0014/ts_0013 candidate_opt NStep=42）/ job 1012（calcfc NStep=100）/ job 1016（readfc NStep=100）/ job 1019（candD NStep=48）。**软模墙**：job 1012 @L1150–1153 与 job 1016 @L789–792 的 Step 1 位移完全相同（Max Disp 0.168688 NO / RMS 0.069832 NO，力判据均 YES），模型 Hessian 路径亦 42 步漂移，而 I1 端一步即收敛 ⇒ 默认位移判据在该端点在现有步预算内不可达（并入 issue #191）。**NY3 E1 的 xTB 受约束扫描 job 1015 亦不可用**：scan_status=complete 但 usable_as_guess=false、candidates=[]；道侧 14 帧 0/14 通过三条硬判据。

## 6 证据驱动的机理修订（旧 → 新 + 依据 + 影响面）
1. **HL1_E1：声明的 R 不是本级别气相驻点** → E1 记 0.0（无垒离子-分子质子转移），参考态改判为接触离子-分子对；**登记** +0.3454 kcal/mol 只是产物侧 B 上甲基转子 pseudo-saddle 相对 B 的差、**不是该步能垒**；**登记** N-质子化肟 + 水（job 978 / job 995，两条独立到达路径）比 O-质子化态低 **19.4041 kcal/mol**，为竞争/旁观通道（不导向 Beckmann 迁移），**不改图、不改 E2/E3/E4**；E2/E3/E4 既有 ORCA 值（23.13/10.44/13.46）限定为「以 O-质子化分支为参考态」的口径。
2. **NR1_E1：声明的 R 不是极小值** → 该步改述为「无垒前平衡」，0.0 为约定值（无独立鞍点），不是「0 垒 TS」；影响 E1 自身与 E2 的起点参考态（E2 用 I1 = −463.999955035）。另有勘误：STATUS §8.1 的 929「+18.48」更正为 **+18.140**。
3. **NY3_E2/E3：由「可能协同步合并」改为「分步」** → job 990 的 I2 型结构 27 模全实、无 imaginary 行（0 虚频），几何独立复算（O1–H6 0.972 / C4–O1 1.326 / C4···O3 4.568 / Na–O3 2.047）；E2 = I1→I2、E3 = I2→P 各自独立声明；影响面仅 NY3 的 E2/E3 节点与边定义。
4. **NR1_E2：候选垒 16.26 不是 I1→I2 的 ΔE‡**（见 §4），只作 candidate_only 登记。
5. **HI1_E3：起点参考态 = 实测互变体**「aldol-OH + 羧酸根 + 旁观水」（job 961），与题源声明的 alkoxide + COOH 只差 H24 位置（质子互变异构体）；job 980 的一维约束切片只覆盖「水逼近 C2 + 羧酸根质子化」，不含 C2–N4 断裂 / H26→N4 ⇒ 峰帧只作 TS 初猜、扫描能量不作能垒。
6. **HI1_E2 / EM1：既有 13.36 / 15.52 原样保留、标为「不可用于 (S) 题面定量引用」**（L2 身份缺口：两条旧值建在 R-脯氨酸几何上，而题源为 (S)）。本机无 ORCA、无 Oct-1 原生日志 ⇒ 既无法核验、也不作无证据删除；本批 Gaussian 重算未取得替代值（E2 = job 1008 于 11:20 CST 截断；EM1 = 首候选 pseudo-saddle、通道 B 第 2 次的 job 1032 仍在排队未跑）⇒ 终稿显式声明该缺口，题源与生成物本轮零改动。
7. **拆步/改图提案（只文字、本轮未提交任何作业、零改图）**：① HI1_E1 → 步 A「RC→INT1（两性离子 carbinolamine）」+ 步 B「INT1→I1+H2O」，reaction_center（1-based 与 0-based）与 7 对映射见 §10.2 与 lane1 §18；② HI1_E3 → 「I2→hemiaminal」+「hemiaminal→P」（lane2 §I）；③ NR1_R/E2 参考态重定（job 992 = 中性频哪醇 + H₃O⁺，比 I1 低 11.48 kcal/mol）仍**未采纳**（PA 预期反向意见与 BSSE 疑点未排除）；④ NY3 E2 产物若最终不落在声明 I2 → 改述为环氧鎓路径（本批 candD 已证伪，未实施）。以上仅在证据站得住时执行，执行者 = 各包写权会话 + 守卫。 **实测支撑（新增）**：step A 的产物已在 job 1028 取得真正的半缩胺型驻点（L17230 Stationary point found、L18325 Normal termination 10:56:06；C2–O25 1.4728 新成键、C2–N4 1.4248 保留、H27 已转到羧基氧 O10–H27 0.9949、C9–O10 1.330 / C9–O11 1.214；E = −939.312626605 = +5.04 vs job 961，只作身份证据），频率判定已取得（0 虚频、117 模、最低实模 19.8439 cm⁻¹、11:10:09 正常终止）⇒ 该拆步提案从「文字」升级为「**step A 产物为 verified 局部极小**（半缩胺 + COOH），但仍无 TS、无垒」。
8. **NR1_E3/E4：本批显示 step3（迁移）与 step4（去质子）在气相模型里耦合为单条通道**（不改变 gold 值）。证据（job 998，受约束扫描）→ 沿 r(C4–C8)：I2 极小值起单调升到 **+3.77 kcal/mol（pt6，r=2.067 Å，唯一内部极大）**，随后 12.10 kcal/mol 崖式换谷、一路降到 **−29.44**，末端几何 = **频哪醇酮 + H₃O⁺ + H₂O（= P，去质子已完成/近乎完成；C7–O10 1.240 Å、O1 带 3 H）**；峰值帧 = 桥式甲基/氧碳正离子型半迁移（C4–C7 1.446 显著缩短）⇒ **未观察到 I3（质子化频哪醇酮）作为独立极小值**。口径：+3.77 是**受约束扫描下界**（网格未分辨极大 + 峰后换谷）**不是 ΔE‡**，既不支持也不否定「有独立鞍点」（方向相反），**不得写成「IRC 已双向到达端点」**。处置：维持 `NR1_E3 = 5.16`（旧 ORCA 5.0.2）/ `NR1_E4 = 5.74`（旧 G16-WSL）＋跨程序与非本批 caveat；本批同批值编为**可选增强项**（需 ts_prepare 声明 I2→P 协同单步 + 补 I3/P 极小值，约 2–4 h），在本轮资源与优先级下**未授权**，不在本次交付必交清单。
9. **HL1_E1 的 T3 追认（不改变数值，限定措辞）**：从产物侧极小值 B 出发的 R(H2–O9) 受约束弛豫剖面（job 1005，**20/20 点收敛**，日志 sha **40ce3be2c6d07120b36d7bf8ce9580aad6becaee16cdf8d1b2c3cb0ab0e60c07**，`Normal termination` L69007 @08:00:33）显示 **严格内部极大 pt8 = +3.5705 kcal/mol（相对 B，R(2,9) = 1.4274 Å）**；pt8 身份 = **O1:[H2,H3,H4] 氢鎓 + 中性肟、O1···O9 = 2.3999 Å ⇒ 即声明步反应物侧的接触离子-分子对**，而 **pt8 → B 单调下坡、无中间极大 ⇒ 声明方向无垒，HL1_E1 = 0.0 维持**。新增登记：**反向（B → 接触离子对）受约束剖面势垒 ≥ +3.5705 kcal/mol（只是下界；受约束弛豫扫描的真实 MEP ≤ 3.5705）**，且 **pt8 帧不是已验证鞍点**（是否自由 PES 一阶鞍点未经管线 OptTS+freq 判定）；该剖面另经 frames 9→10 换谷直下到 **N-质子化肟 + 水**（相对 B −12.594，朝 −19.404 的 N-质子化极小值），并独立再确认「质子留在 O1 的 A 形极小值不存在」。TS guess 已备：`round4/T3_scan_peak_pt8_ts_guess.xyz` sha **7018f6880a335c7ccd013a47d44fcf8599c3e9f5842bfa872571ae33f9a014ac**（可选增强，不改变该边值）。
10. **HI1 三边的单步/合并声明在本级别未取得一阶鞍点（这是证据判读，不是「无鞍点」证明）**：E1/job 1017 沿高能脊升到 +45.06 kcal/mol（10:36 读数），且 C3–H22 未断、O4···H22 反拉到 2.721 Å；E2/job 1008 的 d(1,29) 由 2.646 Å 单调外漂至 5.09 Å（烯胺型电子结构不变）；E3/job 999 收敛回 I2 盆地驻点。三条 result.outcome 均保持 null。
11. **NY3_E1：起点参照态已建立，但 H6 坐标处于数值极软区（措辞修正）**：job 1031（沿 −134.4181 cm⁻¹ 虚模位移 0.300 Å 后的普通 Opt+Freq，日志 sha ed579d01…、7,974 行）**无 imaginary 行、band 表 27 模全正（最低 48.2631 / 61.5384 / 101.3513 cm⁻¹）**，E_ref = **−466.986564213**（L6122；+11.4705 kcal/mol vs I1 = −467.004842485）；同一区域另有近简并驻点（job 1022 的 OptTS 输出，内坐标差 ≤0.0054 Å（逐原子未对齐最大 0.4172 Å、质心对齐后 0.3414 Å，全部落在羟基氢 H6）、能量差 **−0.00026 kcal/mol**（E_ref 更低）），其 freq（job 1027）给 1 虚频 −134.4181 cm⁻¹（模矢几乎全在羟基 H6、与 O–H 键方向点积 −0.01），两者曲率约 +0.0016 与 −0.0123 mDyn/Å ⇒ **「RC 是一阶鞍点」不宜作定论**，正确表述为「同一极小值区域同时存在 0 虚频极小值与 1 虚频近简并驻点，H6 坐标极软」。影响：E1 的 ΔE‡ 仍缺测（缺一个 1 虚频且模矢以 O1–C4 为主的一阶鞍点 + 双向连通性），但分母已有 E_ref，不再写「参照态未确立」。剖面事实只作背景：RC→I1 方向存在支-RC 与支-I1 两条 Na⁺ 配位通道交叉窗（支-RC 沟底 +11.06 vs I1），正/反剖面在 2.48–2.50 Å 重叠区差 2.4 kcal/mol ⇒ 两条都不是 MEP。
12. **HI1_E3 的终态是「收敛回起点」而不是「找到垒」**：job 999 末帧 C2–O25 = 3.1385（job 961 为 3.1596）、水完整（O25–H26 0.9666 / O25–H27 0.9891）、N4–H26 = 3.9822（质子未转移）⇒ 唯一可登记的结论是「该声明在本级别未获鞍点」；+0.98 kcal/mol 只是该极浅 off-target 驻点相对 job 961 的能量差。

## 7 平台与工具问题（GitHub issues）
- **#176** compute.db 持久写锁（含恢复流程与副作用；并追加 ts_prepare tool_exception 为其下游症状的闭合 comment）。三次复发均以「只 TERM uvicorn + `gold_finish_20261015/fix_db_lock.sh`」处置，`db_lock_recovery.log` 记录三次 `DB WRITE OK`。
- **#177** 工具面/角色面缺口（explorer 无 write、bash 白名单过窄 ⇒ 本战役 >2 MiB 原生日志只能由 Coordinator 代算 sha；含子代理无法 call 父会话 comment）。
- **#178** integrity.py 组分规则在 schematic SMILES 下的评分缝隙（NI5_R 2 组分 vs 真实 3 组分；当前字节下 NI5 实例已不成立，是否关闭待定）。
- **#179** Na⁺ 多组分准备链 5 处（含 reaction_mapping 对多组分体系的错误 unique 映射；NY3 已按证据修正声明与序对照）。
- **#180** TS run 孤儿化 + 语义更正：跨会话 ts_resume **不是**一律被拒（本战役累计 ≥7 次 accepted，其中 owner 会话已 failed 的样本 ≥5），口径改为「优先 ts_resume，仅真出现逐字 owner 拒绝文本才重建」；另追加两条 comment：run 归属与**终端通知路由**缝隙（comment 6226179730）、输入身份校验拒绝样本（comment 6226058229）。
- **#181** agent_hub role 名寻址误投（子代理回报一律改为「主题帖 + 首行 to: <session_id>」）。
- **#184** ts_prepare 声明层无法设 IRC 步长/算法（软模 IRC 无合法重试入口）。
- **#189** qm_input_writer 对 engine=gaussian 的 basis_set 不做语法归一化（`def2-SVP` 连字符 → l1 立即 QPErr，0.1 s 退出）；附两个探针输入 sha b14f8e7e… / 017809ae…。
- **#190** frequency 门禁只数虚频数、不核对虚频模与声明 reaction_center（两例：HL1_E1 的 −67.9886 cm⁻¹ 与 NY3_E1 的 −98.2487 cm⁻¹ 均为甲基转子软模，却被当作「恰 1 虚频 ⇒ 可推进」）。
- **#191** `maxcycles` 被 Link1 接受但优化器步预算与之无关且随作业/阶段不同（build opt = 100：job 1012 L1096 / job 1016 L735；ts_opt = 45；HI1 ts_opt = 226/232/240/246）⇒ 声明与真实步预算不符；含两条补证 comment（6227558968、6227843708）。
- **#192** 证据引用只存路径不存字节 ⇒ provenance 文件可就地改写而被引用字节静默漂移（实例：E1_GUESS_V2_PROVENANCE.md 由 97c422d5… 就地勘误为 e2b9906f63d05ef089be9a2885ebc24521675d7d5a356bc992fd86e8a7bae355）。
- **#193** `ts_guess(mode='xtb_path')`：传 atom_map 被 schema 拒（`Invalid tool arguments: arguments: invalid value`），不传则 `termination=invalid_endpoints`；两次尝试均失败。
- **#194** `ts_resume` 被**从未起跑的排队作业**阻塞（ts_0012 的自动 IRC = job 1026，state=ready、无 .cloudra）：call_id tc_f74238b0861f47af、逐字 `ts_resume: active compute jobs prevent input revisions; use ts_inspect`；agent 不得杀进程/调 priority ⇒ 只能等其终态。诉求 = 未起跑排队作业不阻塞输入修订 / 或 ts_resume 显式失效旧 revision 的待跑作业 / 或给出受支持的放弃路径。正文文件 `gold_finish_20261015/ISSUE_194_TS_RESUME_BLOCKED_BY_QUEUED_JOB.json` sha256 123f5100c834ea93cbfd73e0481dca9bf7ce6390e2e8625be2a1478362732af3。
- **#194 第二例（同型，已追加 comment 6228173757）**：ts_0007 被**自身排队、从未起跑的 frequency 作业**（job 1027）阻塞（call_id tc_106c24eac2434f78、逐字 `ts_resume: active compute jobs prevent input revisions; use ts_inspect`、process.json revision 71 零变更）；job 1027 终止后管线又自动提交 job 1030（IRC）继续锁住 ⇒ 「未起跑的排队作业阻塞输入修订」已连续阻挡两个 run（ts_0012、ts_0007）共三次。
- **#195** durable 管线 **build 阶段「软模墙」拒绝已验证 seed**：job 1007 的起点本来就是 job 990 已验证的 I2 极小值，仍在固定步预算内被位移判据拒绝；连同 1012 / 1016 / 1019 / 1024 / 1025 共七条同型（Max Force 与 RMS Force 均 YES、Max Disp / RMS Disp 均 NO）⇒ 需要「以已验证极小值作起点时放宽位移判据」或允许显式跳过 build 重优化。正文文件 `gold_finish_20261015/ISSUE_195_BUILD_STAGE_SOFT_MODE_WALL.json` sha256 fb4b063784f619c53ae6a51f2a74d203fbdabc81c80ab6b08107d6b736527fe4。

## 8 事故复盘（平台重启 → 会话 failed → hub call 被 park）
- 观察 1：只重启 uvicorn 会把正在跑的包 Coordinator 会话收尾为 `failed`（多次复现）。恢复流程后**必须**立刻 `agent_hub directory` 查 state 并重派。
- 观察 2：**运行时通知的 succeeded/ended ≠ 会话死亡** —— 被 agent_hub 消息唤醒后会再次 running；同角色多任会话可同时存活 ⇒ 必须为每个包的可写文件指定**唯一写权会话**（本战役写权表见 LEDGER）。
- 观察 3：发给已结束会话的消息会被 **park**；因此回报路由统一为「主题帖 + 首行 `to: <常驻会话>`」。
- 观察 4：为等待作业而挂的唤醒提醒无法可靠按 id 取消；且长期挂在 past 的提醒只在空闲时触发 ⇒ 用「绝对时间/一次性 check」而非依赖 id 取消。

## 9 交付面清单（2026-10-17 10:35 CST 实测；交付冻结以本表 sha256 为准）
**交付面 11 个文件（2026-10-17 10:35 CST 实测，交付冻结以本表 sha256 为准）**

| # | 文件（仓库相对路径） | 字节 | mtime | sha256 | 说明 |
|---|---|---|---|---|---|
| 1 | cloudra/benchmark/normal_registry/ai.py | 12,954 | 06:25:36 | 399c0468f173cf27c44d9fa32d27d96b9c93d76e65433e83942e5734f43483f3 | NI5_E1 回填 0.93 |
| 2 | cloudra/benchmark/normal_registry/ru.py | 11,949 | 06:50:41 | 154650c18062c5f637b55342c939dd168373a361cdf8b1dba731e396e616a73d | NR1_E1 回填 0.0 |
| 3 | cloudra/benchmark/normal_registry/yo.py | 4,221 | 10-04 | dc58b4f5a01738c96001c32fcf913899d79cd00098e30909cfc83716ad0aefc8 | 零改动（NY3 0/3） |
| 4 | cloudra/benchmark/hard_registry/jl.py | 5,148 | 08:07:15 | 944346f44465eac0b2fda3c47df58180427bc00d59963b5e9e2ce521baa64481 | HL1_E1 回填 0.0（仅注释） |
| 5 | ideapool/reaction_candidates/hard.md | 56,248 | 06:37:50 | 4940fa667289ed038c888f8d63f84f6c301b123681f5982158b5a8b93e70a089 | HL1 题源行 |
| 6 | ideapool/reaction_candidates/normal.md | 65,752 | 06:51:19 | 771a6c7ffa23a358ed8b35005c31d64931530d2f6aeb54c7ecc568e5c0fbdc89 | NI5/NR1 行（竖线缺陷已修） |
| 7 | ideapool/tasks/hard/HL1.json | 12,529 | 08:08:17 | 240865b13d28a1fb13f1cd5fe7211a993bc33fe413c60d2b3adbb67cc9db1678 | 生成物 |
| 8 | ideapool/tasks/normal/NI5.json | 11,068 | 06:53:19 | a95ce872a8312325d4ecdf503cf1024aebbebe433593bff88c745c9b0232349c | 生成物 |
| 9 | ideapool/tasks/normal/NR1.json | 11,336 | 06:53:19 | 6eab2f24fbaff453aa958b3714c12de588108731fce6155350f80c88322ac020 | 生成物 |
| 10 | ideapool/tasks/normal/NY3.json | 9,836 | 06:53:19 | 4e7e754e23272578572359c127115cfd039efe02bc08a055575fc647c3857f3e | 生成物（零改动） |
| 11 | tests/test_benchmark.py | 4,234 | — | 037a424b05cc5d28f0bd2540af456aedf034908d5e59525b356994d38bd8d014 | 断言同步 |
**每条边的证据绝对路径 + sha256 + 行号**：见 §10 逐边结算快照与 LEDGER 各轮段；证据面（原生日志、STATUS、provenance）不进入交付面、不改写原生日志字节。
**三处回填的守卫**：NI5_E1 = 0.93（ai.py L155/L156；NI5.json a95ce872…）、NR1_E1 = 0.0（ru.py；NR1.json 6eab2f24…）、HL1_E1 = 0.0（jl.py 944346f4…；HL1.json 240865b1…）——每处均走「写回填 → 重跑生成器 → regenerate_identically 守卫」，守卫原文见 LEDGER 对应轮次；HL1 包另加四条守卫（措辞收紧后复跑全绿）。
**git status --porcelain（10:36 实测，13 条）**：M jl.py / M ai.py / MM ru.py / M hard.md / MM normal.md / M HL1.json / MM NI5.json / M NR1.json / MM tests/test_benchmark.py；未跟踪 gold_finish_20261015/、ts/、ts_path/、structure.zmat。**yo.py 与 NY3.json 未出现在改动列表**（NY3 本批 0/3 回填，交付面零改动，与 §10.3 一致）。
**断言同步链**：tests/test_benchmark.py 的 HL1 首项由 None 改 0.0（改前 sha 1d4f723b… → 改后 037a424b…，L2138）；主协调独立复跑该文件 = 188 passed / 1 skipped / 0 failed。
**写轮结束后的终值 sha 复核**：NR1/STATUS.md 65f120de…（冻结 08:05:34）、MECHANISM_REVISION.md 2559935d…、HL1/STATUS.md dcf138f9…（§23）、HL1_E1_DECISION e33f32d9…；交付冻结前以同一轮实测值为准，见文末「实测时点」。
**HI1 四边与 NY3 三边的终态**：见 §10（10:40 CST 起）与 §10.5；未取得终态的边一律按「缺测 + 缺什么 + 已证伪」登记，result.outcome 保持 null，不以估计值填充。

## 10 逐边结算快照（2026-10-17 10:38 CST；取代 §5 的进程型列表）

> 口径：每条边只有两种可交付终态 —— **已回填 + 守卫通过**，或 **明确缺测 + 缺什么 + 已证伪什么**。两条仍在等作业的边单列在 §10.3；若终稿前仍无终态，按「管线在跑、result=null、未验收」如实标注。

### 10.1 已回填并通过守卫（3 / 11）
| 边 | 值 kcal/mol | 语义 | 交付面文件（现盘 sha256） |
|---|---|---|---|
| NI5_E1 | **0.93** | 水相 C–N 加成 TS；soft-mode-dominated 已如实标注（−164.4792 cm⁻¹、C–N 伸缩成分 13.4%、watch pair 投影 1.62%）；连通性只写「受约束单峰 + 变分自洽 + 两端点 0 虚频 + 端点松弛补强」 | ai.py 399c0468…、NI5.json a95ce872…、normal.md 771a6c7f…、tests 037a424b… |
| NR1_E1 | **0.0** | 约定值 = 无独立鞍点 / 无垒前平衡（**不是** 0 垒 TS） | ru.py 154650c1…、NR1.json 6eab2f24…、normal.md 771a6c7f… |
| HL1_E1 | **0.0** | 声明方向无合格鞍点、相对自身起点无垒；反向受约束剖面极大 **≥ +3.5705 kcal/mol（仅下界）**；pt8 非已验证鞍点；参考态 = 接触离子-分子对 | jl.py 944346f4…、HL1.json 240865b1…、hard.md 4940fa66… |

### 10.2 明确缺测 + 缺什么 + 已证伪（6 / 11）
| 边 | 缺什么 | 已证伪（要点） | 证据驱动的处置 |
|---|---|---|---|
| **NR1_E2** | 连接 I1 与声明 I2 的独立一阶鞍点或任何路径证据 | 4 条（软鞍点 −74.5623 cm⁻¹ 两端不匹配；917 坍到环氧鎓；约束大 r 侧 +17.2；产物侧 IDPP NStep=134）；IRC job 941 l123 | 16.26 只作 candidate_only（§6 第 4 条） |
| **HI1_E1** | 7 对合并边的一阶鞍点在**本级别**的虚频与归属、整条边的连通性、ΔE‡（分母锁定 job 907 −939.308829219） | **已证伪**：① 合并 7 对的 provided 初猜不走向 7 对单鞍点（H22 始终在甲基上、O4···H22 由 1.713 反拉大到 2.52–2.72 Å、C2–O4 由 1.550 缩短到 1.358 Å、仅 C2···N20 与 O4···H21 推进）⇒ 只能当**步 A** 素材；② 该 ts_opt 到 11:07 已 96 步仍未收敛（四项判据全 NO），不能充当鞍点；③【防误用】E1/runs/I1_optfreq（job 908）输入为镜像、末帧 CIP **R** ⇒ 不作 E1 产物侧基准（产物侧用 job 924）。**截断登记（11:07 CST 末次读数，非终态、无 termination）**：job 1017 refine.log sha256 **672779c9bfe561d81e994893842df024f68681fdfbc0452cdf416c0de82f715f**、95,347 行；L94635 `Step number 96 out of a maximum of 246`；末 SCF **−939.241345208（L94547，after 11 cycles）= +42.35 kcal/mol vs job 907**（Δ = 0.067484011 Ha；同值对 job 924 为 +43.00，只作读数、非 ΔE‡）；**HI1 写权会话 11:14 CST 的终局登记值**（采用其登记口径）：step **99/246**、末 SCF **−939.240831682（L98349）**、日志 sha256 **3b8e0996febb643be22a2a9dc8e74ccf7784422a280d8c48c71d6bc83457ba0b**、**+42.67 kcal/mol vs job 907**；此后文件继续增长（11:15 复核 sha d4cbaee6…、step 100/246），**仍无 termination**；四项判据 L94926–94929 全 NO（Max Force 0.002508 / RMS Force 0.000583 / Max Disp 0.538071 / RMS Disp 0.165154）；日志内 Normal/Error termination 计数 = 0。同向的早期读数（lane1 §19，10:36、sha 45575313…、step 78/246、−939.237012718 = +45.06、C3–H22 1.093 未断、O4···H22 2.721）表明全程沿高能脊缓慢下降、位置判读不变。run ts_0008 revision 29：status=waiting、stage=refine、blocked=null、**result.outcome=null**（从未进入 freq/IRC/端点）；TS 虚频数与连通性 = 缺测（无 frequency、无 IRC）。 | 拆步提案（只文字、未提交作业）：步 A「RC→INT1」form (2,32) C2–N20 σ + (3,41) O4–H21，break (2,3) C2=O4 π + (32,41) N20–H21；步 B「INT1→I1+H2O」form (2,4) C2=C3 π + (3,10) O4–H22，break (4,10) C3–H22 σ + (2,3) C2–O4 σ；0-based：form [1,31]/[2,40] 与 [1,3]/[2,9]，break [1,2]/[31,40] 与 [3,9]/[1,2]。**INT1 无同批 Opt+Freq ⇒ 不得作分母**；INT1 候选帧 lane1/INT1_candidate_from_job1017_step61.xyz 0aacfe68…（内容为第 60 步帧、文件名笔误）。 |
| **HI1_E2** | 单步鞍点 | **截断登记（11:07 CST 末次读数，非终态、无 termination）**：job 1008 refine.log sha256 **40a8cb1b4a27527cea075b774003645bca38023a3434f9e9c7e4db9dc5128fb2**、117,515 行；L116784 `Step number 126 out of a maximum of 226`；末 SCF **−939.303717935（L116696，after 12 cycles）= +2.82 kcal/mol vs job 924**（Δ = 0.004500328 Ha）；四项判据 L117055–117058 全 NO；termination 计数 = 0；**HI1 写权会话 11:14 CST 的终局登记值**：step **129/226**、末 SCF **−939.304351052（L120485）**、日志 sha256 **e3a0e54301c6db71796a47ca985939948438a6d61291c11e14f1011d7ca334c7**、**+2.43 kcal/mol vs job 924**；11:15 复核 sha 7d31af9d…、step 130/226，**仍无 termination**；**d(1,29) 由 2.646 Å（step1）持续外漂至 5.093 Å**（更早帧 4.75），电子结构始终烯胺型；**L2 身份缺口**（旧 13.36 建在 R-脯氨酸几何） | 旧值保持 13.36、标「不可用于 (S) 题面定量引用」；不补作业 |
| **HI1_E3** | 单步鞍点（声明 6 对键变化） | **终态 + 频率判定（job 999 done 10:30:07；job 1029 freq done 10:55:08）**：末 SCF **−939.319094501（refine.log L124211）= +0.98 kcal/mol vs job 961**、Step 134/232、Stationary point found L124575、Normal termination L125662；末帧 C2–O25 **3.1385**（job 961 为 3.1596）、C2=N4 1.2990、水完整、N4–H26 3.9822（质子未转移）⇒ **收敛回 I2 盆地**。frequency.log sha256 **8366cbc6ec3d40d66bfb001cee746ac39f9fdc86896098d088e82e4d3cc133af**（374,858 B）：**117 模**、L1502 `1 imaginary frequencies`、L1511 **−128.0397 cm⁻¹**；位移 15(H) 0.640、14(H) 0.592、16(H) 0.478（= C3 甲基三个 H），其余 ≤0.037；**6 个 watch pair 只承载 0.3% 均方位移**（最大单对 R(4,26)=0.0374）⇒ **负曲率来自甲基扭转，是 off-target 伪鞍点、E3 无合格 TS** | 不回填、result.outcome 保持 null；**+0.98 不是 ΔE‡**；旧值 16.9/19.2 不采用；§9 拆步提案 I2→hemiaminal / hemiaminal→P（只文字）；管线自动排队的 job 1033（IRC）只作记录，不改变结论；**拆步提案的 step A（I2→半缩胺）产物已有实测驻点**：job 1028（lane2 对 1.600 Å 晚段帧做 Opt+Freq）L17229/L17230 Optimization completed + Stationary point found、L18325 Normal termination 10:56:06，末帧 C2–O25 1.4728（新成键）、C2–N4 1.4248、O10–H27 0.9949 且 O25···H27 1.6342（质子已转到羧基氧）、C9–O10 1.330 / C9–O11 1.214（COOH），E = −939.312626605（**opt 链收敛点 SCF，L16838**；同一几何在 freq 链路起点重算得同值，L19117、"after 1 cycles"，两者同值但语义不同）= **+5.04 kcal/mol vs job 961**（只作落地物种身份证据、不是 ΔE‡、不进任何分母），频率判定 **已取得：0 虚频**（freq 段 Normal termination 11:10:09；**117 模**、无 imaginary 行、最低实模 19.8439 cm⁻¹；日志最终 sha256 **1ec7e4c6388415d0859939238f4f96ec7739c0bbf1f985a28f4dd3c23b7dcec1**、23,954 行）⇒ **step A 的产物是 verified 局部极小（半缩胺 + COOH）**，但仍然不是 TS、不提供任何 ΔE‡ |
| **NY3_E2** | 任何 TS 搜索（从未进入） | 管线 build 阶段的**软模墙**：job 1007/1011（NStep=42）、1012/1016（NStep=100）、1019/1024（NStep=48）、1025（NStep=100）七条同型；且 job 1007 的起点本来就是 job 990 的**已验证极小值**，仍被位移判据拒绝 | **issue #195**；I2 端参考定义**不变**（= job 990 −466.986020418，candD 已证实为同一极小值） |
| **NY3_E3** | 同上 | 同上（build blocked：needs conformers.reactant / product） | 同上 |

### 10.3 仍在等作业（1 / 11；EM1 已确认按 partial 交付）
- **HI1_EM1**：第一次尝试（ts_0012 的 ts_opt，job 1013）已判 **pseudo-saddle**（恰 1 虚频 −27.9419 cm⁻¹，[1,29] 投影仅 0.078%、H 主导、几何 d(1,29)=3.198 Å）⇒ +9.13 kcal/mol 只作 candidate_only；其 IRC（job **1026**）**已于 10:37:21 失败**（`Delta-x Convergence NOT Met` L13591、`Maximum number of corrector steps exceded.` L13592、`Error termination via Lnk1e in /home/ly/g16/l123.exe` L13593；日志 sha256 0670edd201ea6347ca9cbc202e61cdb8ae5e3856b241f8f7e51f03c601d19a0f、13,596 行）⇒ **该 IRC 的任何端点读数不作连通性证据**（建在已判 pseudo-saddle 的驻点上）。通道 B 第 2 次（= 最后一次）换种子已按批准执行：ts_resume(ts_0012) **accepted**（request_key tc_a8a157a2432141a7、revision 26→27、input_revision 1→2、changes 仅 guess.evidence_refs 与 guess.xyz_path、retained candidate_opt/attempt1/job 1000、invalidated ts_opt 1013 + frequency 1021 + irc 1026），新作业 **job 1032（ts_opt，ready）**，绑定种子 TS_guess_EM1_j58f8_faceflip.xyz sha 9f4d651a…（d(1,29)=1.9375 Å、41 原子，与 provided.xyz 逐字节相同）。**队列演变**：10:38 queued 1032(pos3) → 11:04 **job 1032 已起跑（running）** ⇒ 11:20 前不会终态，本条按 **partial：result=null、未验收（ts_opt 在跑、无 freq/IRC/端点判定）** 交付。ΔE‡ 参考固定 **job 924 = −939.308218263**（job 1000 = −939.302926757 只作连通性/身份核验）。
- **NY3_E1**（结局：**缺测，但参照态已在收口前取得**）：① d230 版（job 1022）收敛到与 RC 逐项相等的驻点 ⇒ guess 证伪；② job 1027 freq 在该区域给出 **1 虚频 −134.4181 cm⁻¹**（羟基氢 98.87%、与 O–H 键方向点积 −0.01、Red. mass 1.1599 / frc 0.0123；日志 sha 385214fd…、L769 与 L773–L786）——它是与下述 0 虚频极小值**近简并（−0.00026 kcal/mol、内坐标差 ≤0.0054 Å、逐原子最大 0.4172 Å 全在羟基氢）**的软区驻点，不能据此断言「RC 是一阶鞍点」；③ 裁定「甲」= job **1031**（沿该虚模位移 0.300 Å 的普通 Opt+Freq，sign +1、s=0.30284、8c/10000MB/priority 0）**已终态 11:04:44**：`Optimization completed` L6266 / `Stationary point found` L6267 / `Normal termination` L7974（日志 sha **ed579d010fc917856598fee6b769348e5b848ebcb99892152db5906e94d4cbb6**、7,974 行），**27 模全正、无 imaginary 行、最低实模 48.2631 cm⁻¹**（L7084；L7074 的 −14.1988 按锁定规则不计模），末 SCF **−466.986564213（L6122；freq 段 SP 同值 L6826）**，身份四项全过（Na–O1 2.092 / Na–O7 2.410 / Na–O3 4.258 远端 ⇒ 支-RC；O1–H6 0.965；O1···C4 2.800）⇒ **E_ref = −466.986564213 Ha 可作 E1 候选参照**；**但必须标注近简并**：该点与该 −134.4181 cm⁻¹ 鞍点**内坐标差 ≤0.0054 Å（逐原子未对齐 0.4172 Å、质心对齐 0.3414 Å，且全部落在羟基氢 H6）、能量差 −4.11e−7 Ha ≈ −0.00026 kcal/mol**（仅诊断、不相减）⇒ 这是极平羟基扭转区里的近简并点，「哪个是极小值」在本级别已接近数值噪声水平。④ 尝试 1（帧 A/p6，xyz 9ee4e847… + provenance 8dc2c267…）**已由 ts_resume 接受**（request_key tc_290eb3b0bc5c44ea，revision 78→79、input_revision 5→6、changes 仅 guess.evidence_refs 与 guess.xyz_path；retained candidate_opt/job 967 与 product_seed_opt/job 985；invalidated ts_opt 1022 + frequency 1027 + irc 1030），管线作业 **job 1034** 在跑 ⇒ 11:20 硬时线前不可能给出 TS 与双向连通性。⑤ job 1030（IRC）**l123 失败**（Delta-x Convergence NOT Met / corrector steps exceeded，11:02:48），全日志只有 Point 0 与 Point 1 FORWARD、无 Point 2 ⇒ 该鞍点上无可用端点。⇒ **E1 仍按缺测交付（ΔE‡ 无值），但「缺什么」已收窄为：一个 1 虚频且模矢以 O1–C4 为主的一阶鞍点 + 双向连通性**；STATUS §38 sha d9758d48a2d99c3ef65482c451fcb7b08d1882c35a155bca837b3901a35f9d7d（700 行）。

### 10.4 本轮新增的方法学与读数纪律（终稿必引）
1. **位置线性平均 ≠ 距离线性平均**：把两支帧逐原子做位置平均会使 O–H 塌到 0.508 Å、Na–O5 压缩到 1.956 Å ⇒ 任何帧构造必须先做化学可容许性自查（O–H/N–H、金属配位、minsep）。
2. **扫描内部极大不是 ΔE‡**：NY3_E1 反向扫描唯一内部极大 p5 = +22.232 vs I1 / **+10.756 vs RC**，只作 TS 候选/下界；且 p1–p5 与 p6–p9 **分属两条 Na⁺ 配位支**（支-I1：Na 桥联 O3+O5；支-RC：Na 桥联 O1+O5），正/反剖面在 2.48–2.50 Å 重叠区相差 2.4 kcal/mol ⇒ 两条都不是 MEP。
3. **虚频模必须与声明键对对照**：「N imaginary frequencies ignored.」是热化学常规行、**不是模数**；模数只看 band 表 3N−6（HI1 = 117、NY3 = 27）。已登记三例甲基/羟基转子 pseudo-saddle：HL1_E1 −67.9886 cm⁻¹（C3 甲基）、NY3_E1 −98.2487 cm⁻¹（甲基，H 占 99.49%）、HI1_E3 −128.0397 cm⁻¹（C3 甲基三 H 占 0.640/0.592/0.478，6 个 watch pair 仅 0.3%），另加 EM1 的 −27.9419 cm⁻¹（[1,29] 投影 0.078%）⇒ 四例全部「恰 1 虚频但不覆盖声明键对」，不得回填。
4. **进程计数量纲**：作业数用 pgrep -cx g16（=4）；进程族用 pgrep -cf 「[g]16」（=12）；pgrep -cf g16 会**自匹配**（13）。
5. **edit 落盘判定**：回执必须 is_written=true 且 after_sha256 ≠ before_sha256；两者相同即「未写入」（本战役发生过一次「自报已写、实测未变」，已由对方 STATUS §35.6 留档）。

### 10.5 截断口径与队列关键路径（2026-10-17 10:38 CST 裁定）

- **截断口径**：HI1 的 E1（job 1017）与 E2（job 1008）于 **11:20 CST 截断登记**（比交付硬线 11:30 早 10 分钟）。理由：按 0.5–0.7 步/分推算真终态落在 13:00 之后，而两者读数已不具决定性（E1 停在 +45 kcal/mol 高能脊、E2 的 d(1,29) 已外漂 5.09 Å）。截断值必带五项：末次 SCF 值 + 行号；step N/M + 行号；明文「非终态读数、无 termination」；日志 sha256；相对自身参考的 ΔE（E1 对 job 907 = −939.308829219；E2 对 job 924 = −939.308218263）。**截断值不得进入任何能垒申报，result.outcome 仍为 null。**
- **队列关键路径**（10:35 实测 query_compute_queue）：node-local 32c 饱和、**free cpus = 0**；running 1008 / 1017 / 1026 / 1028；queued **1029（pos 1，E3 频率）/ 1030（pos 2，ts_0007 自动 IRC）/ 1031（pos 3，NY3 参照极小值）** ⇒ FIFO：1026 让出后才轮到 1029，1031 排在最后。因此 E3 的虚频判定与 NY3 的参照态判定都可能到不了 11:20，终稿按「未取得」如实标注，不以推断值填充。
- **索引序双写（全局口径：两包的「原始序」不是同一个东西）**：
  - **HI1 侧**：题源 atom-map tag 序（重原子 1–20 + 水 H 21/22；其余 19 个 H 隐式、无编号）↔ 工作序（= `runs/I2_optfreq/I2_min_v5.xyz` sha256 9a6203ff67d9f0d95ad774e78b17bc397b22992f24cbcdf448f8c5558142ef2b，与 ts_0011 绑定的 reactant seed 同 sha，亦即 job 961 日志原子序）。declare.json（sha256 b5b883bd09fb0b173fc4d561a5218d3920f6aa04c966e37f0eb7b0eeac8b23ef）的 atom_map 共 41 项、值域 0..40 ⇒ **0-based**，方向 = product 坐标序 → reactant（工作序）；reaction_center 同为 0-based，对应 1-based [[2,4],[2,25],[25,26],[25,27],[4,26],[11,27]]。六对化学标签：C2–N4、C2–O25、O25–H26、O25–H27、N4–H26、O11–H27（实测位点 O10–H27 = (10,27)）；O10/O11 化学等价但本构象氢键对象不同 ⇒ **引用不可互换**；水氧恒为 25。 另外 E1 侧存在**三套序号**：built（工作序）／原始序（= job 907 输入序，RC_optfreq.gjf sha 81b083af…，与 built 为 41/41 双射置换、已逐原子元素+坐标核验）／题源 map 标签；E1 的 7 对映射见 lane1 §18，例：(2,3)↔(2,25)、(2,4)↔(2,1)、(4,10)↔(1,27)、(32,41)↔(4,26)、(2,32)↔(2,4)、(3,41)↔(25,26)、(3,10)↔(25,27)。
  - **NY3 侧**：ts_0007/declaration_0005 的原始原子序（Na、O(羟基)、H、C(甲基)、O(甲氧基)、C(羰基)=6、O(羰基)=7 …）≠ 工作序（C4=羰基碳、O5=羰基氧、O3=甲氧基氧）。该包的 H6 = 羟基氢（原始序第 3 原子 / 工作序 H6），必须双写，否则会被读成甲基氢。
  - **通则**：凡引原子一律写「包 + 序种（原始 / 工作 / 0-based）+ 化学标签」，不得只写编号。
- **符号如实记**：NY3 的 job 1031 起点取 sign +1（H6···Na 2.942→2.970 Å、O1–H6 0.965→1.026 Å），E1 道复算建议 sign −1（2.9514 Å），两者差 ≤0.02 Å、E1 道自评无区分度 ⇒ 不返工；但引用必须写全符号与数值，不得写成「按 E1 道建议」。
6. **写入史**：交付面 ideapool/reaction_candidates/hard.md / normal.md 的 mtime 分别为 06:37:50 / 06:51:19，此后各包未再改；平台只记路径不记字节（issue #192）。

## 11 交付声明与未完成项（终稿以本节 + §10 为准）

- **引擎偏差（必读）**：本机无 ORCA，全部本轮计算为 **Gaussian 16 Rev C.01**、B3LYP/def2SVP + GD3BJ + Int(UltraFine) + SCF=Tight（按边加 CPCM 溶剂）。题库既有参考值多为 ORCA 产生 ⇒ 本轮值与历史值之间**存在程序偏差，严禁跨程序相减**；每条边的能垒只用同一程序、同一批日志内的纯电子能差，且相对该步自身起点极小值（不含 ZPE/热校正）。
- **L2 身份缺口**：HI1_E2 / EM1 的旧值 **13.36 / 15.52 原样保留但不可用于 (S) 题面定量引用**（两条旧值建在 R-脯氨酸几何上）；本机无 ORCA 原生日志 ⇒ 无法核验、也不作无证据删除。
- **本批未取得、必须如实标注的三处**：① HI1_EM1 = 通道 B 第 2 次的 job 1032 在 11:20 CST 前未起跑 ⇒ result=null、未验收；② NY3_E1 = **起点极小值已取得**（job 1031：0 虚频、27 模全正、E_ref = −466.986564213，但与该 −134.4181 鞍点近简并 ~0.0003 kcal/mol，须标注），**仍缺 TS 与连通性**（授权 seed 的管线作业 job 1034 在 11:20 前不会终态）⇒ ΔE‡ 无值；③ HI1_E3 = 已判读完毕：job 1029 唯一虚频 −128.0397 cm⁻¹ 属 C3 甲基摆动（watch pair 仅 0.3%）⇒ 伪鞍点、无合格 TS，ΔE‡ 缺测。
- **读数纪律（不得违反的表述）**：受约束扫描内部极大只作候选/下界、不是 ΔE‡；截断读数必须标「非终态、无 termination」且不进能垒申报；「未取得一阶鞍点」不得写成「无鞍点」；`N imaginary frequencies ignored.` 是热化学常规行、不是模数（模数只看 band 表 3N−6：HI1 117、NY3 27）；pseudo-saddle 必须如实标注、不回填。
- **交付面冻结时点**：见 §9 表（10:35 CST 实测）与文末实测记录；任何后续写入都会使该表 sha256 失效，须同轮重测并出勘误。

## 12 实测时点与冻结记录（2026-10-17 11:08 CST）

- **定稿时点**：2026-10-17 11:08 CST（原定 11:20 截断，因两条 ts_opt 与三条排队作业在窗口内不可能终态，提前收口；此后任何读数只作「窗口外补录」，不改正文）。
- **交付面 11 文件 sha256**：11:05 CST 同轮重测，与 §9 表**逐条一致、无漂移**（ai.py 399c0468… / ru.py 154650c1… / yo.py dc58b4f5… / jl.py 944346f4… / hard.md 4940fa66… / normal.md 771a6c7f… / HL1.json 240865b1… / NI5.json a95ce872… / NR1.json 6eab2f24… / NY3.json 4e7e754e… / tests 037a424b…）。
- **队列终态快照（11:07 CST）**：running **1008 / 1017 / 1028 / 1032**（1032 = EM1 通道 B 第 2 次的 ts_opt，11:04 起跑）；queued **1033（E3 的自动 IRC）/ 1034（NY3 E1 尝试 1 的 ts_opt，declaration_0006）**；pgrep -cx g16 = 4；free cpus = 0。
- **各道证据末版 sha256（按各自最后一条实测）**：HI1/E3 STATUS §M 171fba4f…、HI1/E2EM1 STATUS §11 75da3c09…、HI1/E1 lane1 LANE1_STATUS §19 6c71a148…、NY3 STATUS §38.5 b106c380…（711 行）、NR1 STATUS 65f120de…（冻结 08:05:34）、HL1 STATUS dcf138f9…；本节与 §9/§10/§11 的引用均以这些实测值为准；若某道其后仍写盘，则以其新 sha 作补录、不回溯改正文。
- **记录面**：本报告与台账 gold_finish_20261015/LEDGER.md 为记录面、不进入交付面；原生日志与 STATUS/provenance 为证据面，本轮未改写任何原生日志字节。
- **勘误（11:11 CST，同轮）**：本报告 11:08 定稿后追加了 **job 1028 的频率判定**（0 虚频、117 模、无 imaginary 行、最低实模 19.8439 cm⁻¹、freq 段 Normal termination 11:10:09、日志最终 sha256 1ec7e4c6388415d0859939238f4f96ec7739c0bbf1f985a28f4dd3c23b7dcec1），据此本报告

## 13 冻结后追加（2026-10-17 15:15 CST；覆盖 §1–§12 中受影响的 HI1 / NY3 / EM1 表述）

> 本节记录本报告 11:08 CST 冻结之后发生的事实。与正文冲突时**以本节为准**：HI1 的边集合已由「7 对合并 + 3 单边」改为**五步模型**（E1a/E1b/E3a/E3b 为四条新边），NY3 的整题替换已完成方案切换与部分计算，EM1 定稿为缺测。

### 13.1 HI1 机理模型改为五步（旧 7 对合并边作废）

- 新链路：**R → carbinolamine → enamine → iminium-enolate → hemiaminal → P**（13 节点 / 6 边）。交付面：`cloudra/benchmark/hard_registry/hi.py` sha256 **0ac110bc7e5b57618c1cc272cb93caa3054d3204c5db185d512330f3e97bc4cc**（L66/L82/L104/L123/L144 为五步；competing.from_step 由 1 改为 2，并断言 HI1_EM1.from = HI1_I2）、`ideapool/tasks/hard/HI1.json` sha256 **54221e6591c75f88d2f6d96e853302c48bb25aefb9cc191aab2f6113119b61d0**（§9 的 HI1.json 5fd0ecb2… 已被取代）。守卫：`pytest -k hard_tasks_regenerate_identically` 1 passed；`--check` 报 `OK HI1: 13 nodes, 6 edges`。
- **旧值全部作废、不回填**：HI1_E1 旧 19.2、HI1_E3 旧 16.9 / 19.2；新四条边（E1a/E1b/E3a/E3b）的 barrier 在本节写定时**尚未全部取得**，逐条状态见 13.2–13.3。
- 中间体身份（同批 G16、CPCM(DMSO)、B3LYP/def2SVP+GD3BJ/UltraFine/Tight）：**RC_27** 分母 = job 1044 = **−593.934532807**（75 模、0 虚频、最低实模 21.4691 cm⁻¹、sha 9d683050…）；**carbinolamine_27** = job 1051 = **−593.929762803**（75 模、0 虚频、最低实模 78.1490 cm⁻¹、sha c03e0a82…；ΔE vs RC_27 = +2.99 kcal/mol；质子归属 = O3–H 0.9699、N18 无 H ⇒ E1a 一步协同、E1b 分母成立）；**E3b 分母** = job 1028 = **−939.312626605**（117 模、0 虚频、最低实模 19.8439 cm⁻¹、sha 1ec7e4c6…；job 1053 与其逐原子 RMSD 0.0000 Å ⇒ 重复优化、只作一致性凭证）。

### 13.2 E1a：**未验证（缺测 + 已证伪）**，ΔE‡ = null

- 管线 ts_opt（job 1055）收敛：`HI1/E1/split/.../refine.log` sha **0023847f…**、11,399 行、L10724 Stationary point、L11399 Normal termination 14:45:41，末 SCF **−593.873953336**（相对 RC_27 = **+38.01 kcal/mol**）。
- **频率段由管线无法生成**（平台 #197，见 13.6），改由**同级单点 freq 诊断**补做：job **1062**（输入 sha **ef3d748c…**、route 含 `scrf=(cpcm,solvent=dmso)`、纯 freq、8c/10240/prio0；几何由 format_converter 自 refine.log 末帧导出，xyz sha **2b4cf70f…**、27 原子），Normal termination 15:11:28；日志 sha **e6c12847…**、3,001 行。
- 判读：**1 imaginary frequency = −1551.2317 cm⁻¹**，Red. mass **1.0918**、Frc const **1.5480**；25 组 = **75 模**；**最低实模 41.7021 cm⁻¹**；ZPE 0.228317。模矢（工作序）：**H27 = 0.65 / 0.76 / 0.04**（share 0.797，H 合计 0.869）、**C2 = 0.04 / 0.05 / 0.02**（share 0.053）、O3 0.049、N18 0.010（低于噪声底 0.0141）⇒ **纯质子转移模**。
- 方向与键响应（主协调与 HI1 TS 协调员双向核算一致）：û(O3→N18)·d(H27) = **0.9916**；沿模键响应 **δR(O3–H27) = +0.9162、δR(N18–H27) = −0.7612、δR(C2–N18) = +0.0140（微增、无成键压缩）、δR(C2–O3) = −0.0195** ⇒ Hessian 层面**没有 C–N 成键分量**。
- **判定**：声明产物 carbinolamine_27 的质子归属是 **O3–H（0.9699）/ N18 无 H**，而该模把 H 由 O3 送向 N18 ⇒ **方向与声明产物相反**；该驻点是**加合物内 O→N 质子转移鞍点**，既非 C–N 成键协同鞍点，也不在 RC_27→carbinolamine_27 路径上。因此 **E1a 声明步骤未验证，ΔE‡ = null**；+38.01 只能表述为「27 原子模型内该 PT 驻点相对 RC_27 的电子能差（−593.873953336 vs −593.934532807）」，**禁作能垒、禁回填 hi.py**。41 原子同几何交叉校验（−1547.0708 cm⁻¹、H 0.794 / C2 0.051 / O 0.033）证明纯 PT 非截断伪象。
- **未重跑的理由（两条）**：(a) ts_resume 走 retry/重输入语义时可能覆盖 `ts_opt/refine.log`（sha 0023847f…），而该文件正是本报告引用的诊断几何来源，覆盖即毁证据链；(b) 剩余窗口不足以完成 ts_opt + freq 两段。**documented next action**：用 RC_27↔carbinolamine_27 沿 C2–N18 的内插帧（重骨架、质子单独处理）作新 guess 走 ts_resume，再补同级单点 freq。
- **fallback 的刚性内插已被证明结构性不可行（2026-10-17 15:18:40 CST，HI1 TS 协调员独立复核 lane1 制备件）**：刚性片段内插（笛卡尔内插、刚体 slerp、绕轴旋转、方位角网格、二分，v1–v11）在 **R(C2–N18) ≤ 2.3 Å** 无法给出可用帧；勉强可行的帧 xyz sha **f589a848…**（27 原子）是靠 **丙酮甲基 H 与 N18 的 0.90 Å 严重碰撞**换来的（minsep 0.9000 Å @ 7H–18N），不是物理进攻构型，**不得**作 TS guess；更早的 116a1b0d…（minsep 0.49）同样作废。⇒ E1a 若要继续：**QM 侧的闭环路径是固定 R(C2–N18) 的约束松弛**（吡咯烷环必须松弛），需一个 ts_opt 量级算力，**本窗口未执行**。**力场侧的受导构象搜索（conformer_search guided）能力边界已实测**：在「片段间刚体摆放」下 R(C2–N18) 下限只能到 **2.69–2.75 Å**（**A 帧 2.6920 Å**，xyz sha **845a4bd9…**、元素序 27/27 与 refine 帧一致、R(N18–H27) 1.0349、C2–O3 1.2383 保持羰基、最紧 3 接触 O13–H19 0.9794 / N18–H27 1.0349 / C1–H7 1.0926 全为正常化学键；备选 B 帧 2.7508 Å、sha 9a5c9c32…），因此该帧**可作 documented guess（力场来源、仅 guess、非鞍点）**，但落在目标窗口 2.2–2.5 Å 之外、属早期反应物型帧，定位加成鞍点的概率低。**本窗口内既未提交也未采用**，E1a 仍为 ΔE‡ null。报告口径：E1a =「(i) 协同加成鞍点未定位；(ii) 已定位的 +38.0 是 O/N 质子桥 PT 鞍点（模 79.7% H、δR(C2–N18)=+0.014 无成键分量）；(iii) fallback 刚性内插结构性不可行、需约束松弛、未执行」⇒ ΔE‡ null。

### 13.3 E1b / E3a / E3b：状态与分母（本节写定时在飞）

- **E1b**：分母成立（同 13.1 的 carbinolamine_27，情形 1 质子归属）；**TS 尚未起跑** ⇒ ΔE‡ = null。
- **E3a**：run ts_0016 / job **1059**（ts_opt 14:45:35 起，输入 `ts/ts_0016/jobs/declaration_0007/ts_opt/refine.gjf` sha **d539785b…**，reaction_center `[[2,25],[25,27],[10,27]]`，guess S2 e3748c2c… + provenance 51878313…）。验收四条：恰 1 虚频且模矢含 C2–O25 成键 + O25–H27→O10 中继；甲基/羧基软模 ⇒ pseudo-saddle；端点质子分布与 job 1028 一致；两端 0 虚频 + 连通性。**写定时未终态** ⇒ ΔE‡ = null。
- **E3b**：分母 = job 1028（−939.312626605）；产物端 **P** = job **1061**（输入 `HI1/E3/runs/P_e3b/P_optfreq.gjf` sha **d3b72aea…**、41 原子 C15H21NO4、CPCM(DMSO)、8c/10240/prio0，15:01:49 起）⇒ 写定时未终态。**P 的超前登记与本轮新增判据**：起点帧里跨片段含氢最短 **1.7479 Å 是 C2···H26**（偏紧的 H···C 接触，非氢键；H26···O25 2.5338、N4···O25 3.2627、∠(N4–H26···O25) 128.0°；起因是 H26 放在 N4 孤对方向而该方向偏向 C2）⇒ 收敛后必查三项：C2···H26 是否 >2.4 Å、H26 是否回到 O25 成 O–H、是否被算成 C–H；若贴 C2 或回 O25 ⇒ **P 判构造假象、不作 E3b 产物端**，须重出种子（H26 放背离 C2 的 N4 孤对方向）。E3b 的 TS guess 工具已定为 `prep/mk_e3b_guess_interp_v4.py`（sha **8b7a36fb…**，v3 53b561c3… 仅作内插逻辑基线）：正式帧取 λ∈[0.55,0.65] 内 R(C2–N4) 最接近 2.15–2.25 Å 且 minsep 最大者（干跑 λ=0.57 → 2.1517 Å、minsep 0.9673；干跑数不进交付面），并把 v1（minsep 0.3819–0.6654 Å，原子对 25–26 / 2–26）与 v2（H26···C2 ≈1.38 Å 假 C–H）的排除读数写入 provenance 供 ts_prepare 的 evidence_refs 引用。

### 13.4 EM1：定稿「缺测」，ΔE‡ = null

- 下扫 job **1049**（`HI1/E2EM1/spectator/scan_down_c1c29.log`）15:15 CST 实测 3,650,901 B / 55,997 行、`Optimization completed` **8 次**、末行 `Step number 10 out of a maximum of 246 on scan point 9 out of 12`、**无 termination** ⇒ 交付窗口内跑不完；升格包（up-scan `scan_up_c1c29.gjf` sha d7545a6e… + 产物端 (R)-亚铵-醇盐 Opt+Freq）**从未起跑**。
- 13.36 / 15.52 **仍只作 candidate_only**，并标「不可用于 (S) 题面定量引用」；已跑的 9/12 只登记为「未完成、未判读」，**不得**用任何单点当连通性或能垒证据。
- 缺什么（三条）：(a) 下扫完整剖面 + 上扫并集单峰判据（步长 ≤0.05 Å、单调单峰）；(b) 产物端 (R)-亚铵-醇盐 Opt+Freq（自身 0 虚频 + CIP + 与 HI1_M1 串比对 + 构象差异）；(c) 连通性替代口径声明（无 IRC：两端 0 虚频 + 端点身份 + 端点松弛 + 扫描单峰，四项齐备才可 verified）。

### 13.5 NY3：整题替换（Y2 关闭 → O2 带锁扫描证伪 → butterfly 无约束 TS 待槽）

- **候选 1（Y2，AAC2 酸催化水解）= 关闭**：四次失败 job 1048（NStep=59）、1050（scan point 1 NStep=61 + l9999）、1052（第 71 步 l103 FormBX，∠C4–H15–O6 = 180.00°）、1058（笛卡尔 opt NStep=100、`Max Force` 0.000205↔0.000242 八个周期、ΔE = 2.1e-7 Ha 严格 2 周期极限环、Freq 块 0）。**归因是模型/势面选择问题，禁止写成「酸催化水解不可算/通道不存在」。** 旧值 15.5 / 12.5 / 0.0 全部作废、不回填。
- **候选 2（O2：DMDO + 乙烯，17 原子 / 45 模）**：1D 带双锁扫描 job **1060** done 15:05:22（Normal termination 15:05:20、日志 sha **5b15361c…**、68,732 行、`Optimization completed` 10、`Frequencies` 0）。逐点表（`NY3_R2/fallback_O2/SCAN_LOCKED_TABLE.md` sha **0e1aa09d…**、47 行、13 列；旧 3d43e155… 为 11 列版、数值相同仅列数不同）：R(O4–C1) 2.800→1.900 共 10 点，ΔE = 0 / 0.664 / 1.614 / 2.963 / 4.841 / 7.399 / 10.803 / 15.221 / 20.808 / **27.639** kcal/mol，**单调升、窗口内无极大**；双锁有效（A 1 4 5 全距 0.002°、D 8 1 4 5 全距 0.0011°、步长严格 0.1000 Å）；R1 = d(C1–C2) 仅 +0.015 Å（C=C 未活化）、R2 与 R5 始终差 ≥0.935 Å（单侧异步接近）。⇒ **该受锁扫描不括住鞍点**，只能给「受锁单侧接近路径 1.9 Å 处下界 ≥ +27.639 kcal/mol」，**不是 ΔE‡**；报告统一写「带锁扫描未给出任何可用能垒参考值」。
- 判定：点 10 的 ∠(C1–O4–C2) = 24.19°（O4 偏在一侧）⇒ 该路径非协同 butterfly 形貌；改走 **butterfly 种子 v4**（`o2_butterfly_seed.xyz` sha **e778222d…** + provenance `O2_BUTTERFLY_SEED.md` sha **98b5c2d1…**，d(O4–C1)=d(O4–C2)=2.100 Å、∠(C1–O4–C2)=37.10°、∠(C1–O4–O5)=77.09°）走 **ts_prepare 无约束 TS**，两锁不带入、17 原子/0 1/45 模、reaction_center `[[4,1],[4,2],[3,4],[4,5]]`（成 O4–C1、O4–C2；断 C2–O4、O4–O5；C3=O5 升双键、C1–C2 降单键），准入门禁 = `TS_WORKING_ORDER_MAP.md` sha **f63d0e55…**（working order = 文件行序 identity，heavy_atom_map [1,2,5,3,6,4,7]、binding complete/unique）。
- **NY3 全链溶剂/级别**：B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight + **SCRF=(CPCM,Solvent=Water)**（与 HI1 的 CPCM(DMSO) 不同题不同溶剂，禁止跨题混引）。产物端 Opt+Freq = job **1063**（15:12:48 起，输入 sha **6197876b…**、26 行、0 1、17 原子、最小跨片段间距 2.964 Å；0 虚频只证端点极小、**不证连通性**）⇒ 写定时未终态。**NY3 本批未回填**：`yo.py` dc58b4f5…、`NY3.json` 4e7e754e… 均未改动。

### 13.6 平台与工具问题（本节新增两条）

- **#196**（ts_guess scan_prepare 静默写 charge 0 / nprocshared=4 / 相对 chk、不收 charge/multiplicity）。
- **#197**（TS 阶段在依赖作业 done 后不推进）**本轮补充硬证据**：run ts_0015 process.json **rev 11 / declaration_revision 1 / stage refine / waiting_for `job:1055` / intervention_count 0 / failed_attempt null**，而 job 1055 已于 14:45:42 done；执行 `ts_resume` 且 `changes = {}` 时返回 **revision 0、receipt null**，message 逐字 **`ts_resume: no input change or failed attempt to retry; use ts_inspect`**（call_id tc_a1057bdb18ec45a1 / tc_76cecfe9ac70436c，重复一次逐字相同、无副作用）；同轮 `ts_inspect` 亦不推进。⇒ ts_resume 的语义是 retry/改输入，在 failed_attempt=null 且无输入差异时**没有合法推进通道**，而 process.json 的 `blocked` 仍为 null、`next.action` 仍为 wait_for_system（从外部看完全正常 = 静默停滞）。已在 issue #197 下补评论（含逐字证据、call_id 与三条修复建议）。

### 13.7 交付面复核（2026-10-17 15:15:34 CST 实测，同轮 sha256sum）

| 文件 | sha256 | 与 §9 冻结值比 |
|---|---|---|
| cloudra/benchmark/normal_registry/ai.py | 399c0468f173cf27c44d9fa32d27d96b9c93d76e65433e83942e5734f43483f3 | 未变 |
| cloudra/benchmark/normal_registry/ru.py | 154650c18062c5f637b55342c939dd168373a361cdf8b1dba731e396e616a73d | 未变 |
| cloudra/benchmark/normal_registry/yo.py | dc58b4f5a01738c96001c32fcf913899d79cd00098e30909cfc83716ad0aefc8 | 未变 |
| cloudra/benchmark/hard_registry/jl.py | 944346f44465eac0b2fda3c47df58180427bc00d59963b5e9e2ce521baa64481 | 未变 |
| cloudra/benchmark/hard_registry/hi.py | 0ac110bc7e5b57618c1cc272cb93caa3054d3204c5db185d512330f3e97bc4cc | **新增项（五步模型）** |
| ideapool/tasks/hard/HI1.json | 54221e6591c75f88d2f6d96e853302c48bb25aefb9cc191aab2f6113119b61d0 | **新增项（取代 5fd0ecb2…）** |
| ideapool/tasks/hard/HL1.json | 240865b13d28a1fb13f1cd5fe7211a993bc33fe413c60d2b3adbb67cc9db1678 | 未变 |
| ideapool/tasks/normal/NI5.json | a95ce872a8312325d4ecdf503cf1024aebbebe433593bff88c745c9b0232349c | 未变 |
| ideapool/tasks/normal/NR1.json | 6eab2f24fbaff453aa958b3714c12de588108731fce6155350f80c88322ac020 | 未变 |
| ideapool/tasks/normal/NY3.json | 4e7e754e23272578572359c127115cfd039efe02bc08a055575fc647c3857f3e | 未变（NY3 未回填） |
| tests/test_benchmark.py | 037a424b05cc5d28f0bd2540af456aedf034908d5e59525b356994d38bd8d014 | 未变 |

### 13.8 读数纪律增补（终稿必引）

- **单虚频不足以定 TS**：必须同时核 ①模矢组成（哪些原子、幅度）、②方向（是否朝声明产物，用 û(给体→受体)·d(转移原子) 投影）、③沿模键响应（δR 成键键是否缩短、断键键是否伸长）。E1a 即「1 虚频 + 模矢不符 + 方向相反」的反例。
- `N imaginary frequencies ignored.` 与 `Low frequencies` 段的探针行**都不是模数判据**；模数按 band 表（3N−6）数。
- `l9999 / l103 / l123` 只作**失败登记**，不得写成「无鞍点/通道不存在」；`NStep` 截断与 Berny 显示上限（out of a maximum of NN）不是 maxstep 设置证据（maxstep 看 IOp(1/8)、maxcycles 看 IOp(1/6)）。
- 只能同程序同批相减；本报告全部数值为 Gaussian 16 Rev C.01，**本机无 ORCA**，与历史 ORCA / xTB 值不得混减。

## 14 交付时点状态（2026-10-17 15:33 CST；以本节为交付结论）

**交付判定：partial（部分交付）**。11 条边中 **3 条已回填并通过守卫**、**8 条按「明确缺测 + 缺什么 + 已证伪什么」交付、result = null**；交付时点仍有 4 个作业在跑（本节末）。

| # | 边 | 交付状态 | 值 / result | 关键证据 |
|---|---|---|---|---|
| 1 | NI5_E1 | **已回填 + 守卫通过** | **0.93 kcal/mol**（软模主导已标注） | ai.py 399c0468… / NI5.json a95ce872… |
| 2 | NR1_E1 | **已回填 + 守卫通过** | **0.0**（约定值 = 无独立鞍点 / 无垒前平衡） | ru.py 154650c1… / NR1.json 6eab2f24… |
| 3 | HL1_E1 | **已回填 + 守卫通过** | **0.0**（声明方向无合格鞍点；反向受约束极大 ≥ +3.5705 仅下界） | jl.py 944346f4… / HL1.json 240865b1… |
| 4 | NR1_E2 | 缺测 | null | 4 条证伪 + IRC job 941 l123（#184） |
| 5 | HI1_E1 | 旧边已被五步模型取代 → **拆为 E1a / E1b** | null（旧 19.2 作废） | hi.py 0ac110bc… / HI1.json 54221e65… |
| 6 | HI1_E2 | 缺测（身份可疑旧值） | null（13.36 仅 candidate_only，标「不可用于 (S) 题面定量引用」） | **L2 身份缺口**（旧值建在 R-脯氨酸几何）；job 1008 截断 step ≥130 |
| 7 | HI1_E3 | 旧边已被五步模型取代 → **拆为 E3a / E3b** | null（旧 16.9 / 19.2 作废） | hi.py 0ac110bc… / HI1.json 54221e65… |
| 8 | HI1_EM1 | 缺测 | null（13.36 / 15.52 仅 candidate_only） | 下扫 job 1049 到 scan point 9/12 未完成；上扫与产物端从未起跑 |
| 9 | NY3_E1 | 整题替换（旧值作废） | null | Y2 四失败归因模型/势面；O2 受锁扫描 10 点单调无峰 |
| 10 | NY3_E2 | 整题替换（旧值作废） | null | 同上 |
| 11 | NY3_E3 | 整题替换（旧值作废） | null | 同上；butterfly v4 → run ts_0018 未终态 |

**新拆出的四条边（HI1）**：

| 边 | 状态 | 值 | 依据 |
|---|---|---|---|
| HI1_E1a | **未验证（缺测 + 已证伪）** | null | 管线 ts_opt（job 1055）→ 单点 freq 诊断（job 1062）：1 imag **−1551.2317 cm⁻¹**、约化质量 1.0918、模 79.7% H、δR(C2–N18) **+0.014**（无成键分量）、H 位移沿 O3→N18 投影 0.9916 而声明产物是 O–H 型 ⇒ **PT 鞍点、非声明步骤**；+38.01 仅作该驻点相对 RC_27（−593.934532807）的电子能差 |
| HI1_E1b | 未起跑 | null | 分母成立（carbinolamine_27 = job 1051 = −593.929762803；O3–H 0.9699、N18 无 H） |
| HI1_E3a | job **1059**（run ts_0016）交付时点未终态 | null（未验收） | 输入 d539785b…；reaction_center [[2,25],[25,27],[10,27]] |
| HI1_E3b | 产物端 job **1061** 交付时点未终态 | null（未验收） | 分母 job 1028 = −939.312626605；P 输入 d3b72aea…、41 原子 C15H21NO4；guess 工具 v4 8b7a36fb…（λ∈[0.55,0.65]） |

**交付时点仍在跑的作业（4 个，均未验收）**：job **1049**（EM1 下扫，14:07:05 起，scan point 9/12）、job **1059**（E3a ts_opt，14:45:35 起，step 22）、job **1061**（E3b 产物端 P Opt+Freq，15:01:49 起，step 21）、job **1064**（NY3 butterfly v4 → run ts_0018 candidate_opt，15:19:43 起）；**15:32:49 CST 实测 running 4 / queued 0 / free cpus 0**。这些作业的单点读数与中间帧**一律不作证据**，其终态只作追记、不改本节口径。

**引擎偏差声明（重申）**：本批全部计算为 **Gaussian 16 Rev C.01**（本机无 ORCA），级别 B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight，按题加 CPCM（**HI1 = DMSO、NY3 = Water**，不同题不同溶剂，禁止跨题混引）；**与历史 ORCA / xTB 值不得相减**。

**平台 / 工具问题清单**：#176–#181、#184、#189–#195、**#196**（ts_guess scan_prepare 静默写 charge/nproc/相对 chk）、**#197**（TS 阶段在依赖作业 done 后不推进；本轮补入 ts_resume 在 failed_attempt=null 时被结构性拒绝的逐字证据与 call_id，见 §13.6）。

**复核入口**：台账 `gold_finish_20261015/LEDGER.md`（§R60–§R70 记录 15:02–15:32 CST 的判读、裁定、勘误与 sha 链）；各车道 STATUS 为证据面记录（HI1 8c39cd5c…/1,278 行、NY3 c687cd15…/472 行 等）；**原生日志字节未被改写**。本报告自身 sha256 见台账最后一轮与交付声明。
 sha256 由 **f4d6caeb7d2d0974be13f1e979d0611362faefd6b70fce3409846775f13d9a4d** 更新为本次发布的最终值；被改写的只有 §10.2 的 HI1_E3 行与 §6 第 7 条中「job 1028 频率判定」那一句（missing → 0 虚频 verified 极小），**交付面 11 文件本轮零改动**、其余登记值与行号不受影响。
- **第二次勘误（11:15 CST，同轮）**：把 §10.2 的 HI1_E1/E2 截断登记补上 **HI1 写权会话 11:14 CST 的终局登记值**（E1 step 99/246、−939.240831682 @L98349、日志 sha 3b8e0996…、+42.67；E2 step 129/226、−939.304351052 @L120485、日志 sha e3a0e543…、+2.43），并保留我 11:07 的读数作前一快照；两条边在 11:15 复核时**仍无 termination**（sha 已变为 d4cbaee6… / 7d31af9d…）。据此本报告 sha256 由 **64bef3d9212b80e483c733498bd8d505a0402cbfa957014a6f187366cf920e39** 更新为本次发布值；被改写的只有 §10.2 两处截断登记与本节，**交付面 11 文件仍零改动**。