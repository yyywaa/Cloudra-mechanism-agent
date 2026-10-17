# NY3 交付说明（进行中 · 供终态帖与回填引用）

作者：NY3 包整合 Coordination 会话 **as_a396e35616564357**（本包唯一写权会话）｜更新 **2026-10-17 08:0x +08:00**（本版刷新 §4 逐边状态并新增 §7/§8；前版 sha256 778a4174e68a2ef3747079cb302c5e7c47ce9d1f08937d43a0b85b7554c7ce5b 仅为 07:2x 的暂时快照，已被本版取代）
状态：**未完成交付**（三条边 ΔE‡ 均缺测）；本文件汇集「已可交付的部分」与「逐边缺什么/已证伪什么」，避免终态时重新整理。

## 1 口径与引擎偏差声明（交付必须原样保留）
- 本批引擎 = **Gaussian 16**（/home/ly/g16/g16），路线：**B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight + SCRF=(CPCM,Solvent=Water)**，charge 0 / multiplicity 1（Na⁺ 中性制衡模型，Na 不参与键变化）。
- 既有 gold 档的 58 条值由 **ORCA 5.0.2/6.1.1** B3LYP-D3(BJ)/def2-SVP 计算；本机**无 ORCA**。
- **能量只在同批 Gaussian 16 日志内部相减**；**严禁**与历史 ORCA/Gaussian 数值混减。报告 `computed_by_us=True` 时必须附本句。
- 方法级同一性：泛函/基组/色散/溶剂模型同级，**程序不同**（Gaussian 16 vs ORCA）⇒ 存在引擎偏差，已逐条登记。

## 2 证据驱动的机理修订（旧 → 新 + 依据 + 影响面）
**条目 1：E2/E3 由「可能协同步合并」→「分步」（采纳，2026-10-17）**
- 旧：E2（I1→I2，甲氧基消除）与 E3（I2→P，质子转移）被疑为同一步的两面（旧 run ts_0003 的 I2 端几何在优化中直接滑到 P，job 934）。
- 新：**E2 = I1→I2 独立边、E3 = I2→P 独立边**（分步），各自建 durable run（E2 = ts_0013、E3 = ts_0014）。
- 依据：
  1) job 971 的末帧（力判据已满足：Max Force 0.000120 < 0.00045、RMS 0.000040 < 0.0003）几何抽帧 → E2E3/i2_min_candA.xyz；
  2) **job 990**（在该固定几何上的 freq）：E2E3/freq_i2_candA/i2_candA_freq.log，sha256 `df2548644fc22ac7b64b0da08bded3f44e1ecc9f4db1c5e2015aa2ed954e598b`，Normal termination @L1470，E = −466.986020418 @L512，**9 组 band = 27 = 3N−6 全实**、日志内无 `imaginary frequencies` 行 ⇒ **I2 型是 0 虚频真极小值**；
  3) 我（as_a396e35616564357）**独立复算几何**（同日志 Standard orientation 块）：O1–H6 0.972 / C4–O1 1.326 / C4=O5 1.209 / **C4···O3 4.568（已断）** / O3···H6 5.056 / Na–O3 2.047 Å ⇒ 甲酸 + 甲醇盐 + Na⁺（H6 在 O1），与 yo.py 第 2 步产物式一致。
- 影响面：**仅 NY3_E2 与 NY3_E3 两条边**（参考图节点划分保持 I1/I2/P；E1 不受影响）。
- 待关闭项：端点身份以**管线产出的 IRC 两端点 Opt+Freq（0 虚频）**为正式证据（job 990/994 只作预判，job 990 的几何来自末帧、位移判据未达、无 `Stationary point found`）。

## 3 参考极小值登记（BRIEF §5b：job / 绝对路径 / sha256 / 0 虚频）
| 物种 | job | 原生日志（工作根相对） | sha256 | E(RB3LYP)/Ha | 0 虚频 |
|---|---|---|---|---|---|
| RC（E1 起点） | 967 | ts/ts_0007/jobs/declaration_0001/candidate_opt/seed-opt.log | 730caaa08baa079eeac78ab5cc40bcfed285eda1044f578b281ce4a4f202f53f | −466.986564979 | 待 ts_0007 反应物端点 Opt+Freq |
| I1（E1 终点/E2 起点） | 985 | ts/ts_0007/jobs/declaration_0001/product_seed_opt/seed-opt.log | 56e90cc4eea1dd7c5c1cd96e62a8db22ff2e7627ee190fc06eb9fa39720d3fe2 | −467.004842485 | 待 ts_0007 产物端点 Opt+Freq |
| I2（E2 终点/E3 起点） | 990 | gold_finish_20261015/NY3/E2E3/freq_i2_candA/i2_candA_freq.log | df2548644fc22ac7b64b0da08bded3f44e1ecc9f4db1c5e2015aa2ed954e598b | −466.986020418 | **✓**（27 模全实） |
| P（E3 终点） | 994 | gold_finish_20261015/NY3/E2E3/p_optfreq/p_ref_optfreq.log | ff7ecb5aab3724bd2574c37c9a78b309e45f7eabfeb5ec9ec703c53860f816df | −467.045937735 | **✓**（`Stationary point found`） |
- 极小值间差（同批 G16 纯电子能，**非能垒**）：I1 − RC = −11.47｜I2 − I1 = +11.81｜I2 − RC = +0.34｜P − I2 = −37.60｜P − I1 = −25.79 kcal/mol。
- 几何/序配对与 mol 选择依据：gold_finish_20261015/NY3/E2E3/E2E3_ENDPOINTS_PROVENANCE.md（sha256 `e8b73ab49529e48a5c0e9e15cb9ba87481f21e98913613c268820323d03c8ba3`）。

## 4 逐边状态（截止 2026-10-17 08:01 +0800）
| 边 | durable run | 参考极小值 | 在飞 | ΔE‡ | 缺什么 / 已证伪什么 |
|---|---|---|---|---|---|
| NY3_E1 (RC→I1) | **ts_0007**（rev 43 / declaration_0003） | RC = job 967（−466.986564979；本批 job 989 点 1 独立复现同一极小值） | job **1010** frequency（ready，队列位置 1） | 缺测 | ts_opt 已收敛：job 1004 `-- Stationary point found.` @L17836、E = −466.985305161 @L17712、日志 sha256 d11c078cb98c80f28b142f9c362be188664a9cbe4a5e41e310bcdc7a81b19487；但末帧 O1···C4 2.806 Å ≈ RC、几何差异集中在甲基/羟基旋转 ⇒ 该驻点可能是 RC 另一构象极小值（freq 出后按四分叉判定）。缺：合格 TS（恰 1 虚频 + 模归属 O1–C4）+ IRC 双向 + 两端点 Opt+Freq。已证伪（技术性）：`job 987`（2.192 Å）与 `job 997`（2.086 Å）的 ts_opt l9999/NStep 截断（**不构成无鞍点证据**）；job 989 第 5 点（2.403 Å）未收敛，**不作能垒** |
| NY3_E2 (I1→I2) | **ts_0013**（rev 9） | I1 = job 985（本批独立复现：job 1006 E = −467.004842486，与 985 的 −467.004842485 差 1e-9 Ha） | job **1011** product_seed_opt（ready；candidate_opt job 1006 已 done 且收敛） | 缺测 | 缺：TS + freq + IRC + 两端点 Opt+Freq。**风险预警**：`conformers.product` 用的几何与 E3 起点相同（i2_min_candA.xyz）⇒ job 1011 有同款 l9999 概率（届时同法修复） |
| NY3_E3 (I2→P) | **ts_0014**（rev 8） | I2 = job 990（−466.986020418，0 虚频；构象 = Na⁺ 桥联 O3/O5） | **无（build 阻塞）** | 缺测 | **status=blocked / conformer_optimization_failed**：job 1007 candidate_opt l9999（NStep=42，log sha256 42eae1463d39094f4e9be22c24a7ae0449fe68e591280a4687c42ffb37e909ab）⇒ 见 §7。产品端 P = job 994 |

E1 的扫描证据（用于 choose guess，不作能垒）：E1/E1_scan_O1C4.gjf（sha256 8e2a37eb…）→ E1/E1_scan_O1C4.log（sha256 `62ac90e3732663dc82de1339fe1623b3e3457a4528d2d1f92d8bf3748442dca4`）；已收敛 4 点 2.803/2.703/2.603/2.503 Å 对应 −466.986565136 / −466.986190365 / −466.984669315 / **−466.981571100**（+0.00/+0.24/+1.19/**+3.13** kcal/mol vs RC），第 5 点 2.403 Å 以 NStep=45 截断 ⇒ 鞍点大概率位于 ≈2.40–2.55 Å。provenance：E1/E1_SCAN_PROVENANCE.md（sha256 `30b625eb003acacbfb3070aa68072656dd448008a18ef62df6ec8c5b3bbc8e63`）。

## 5 E3 build 阻塞与 I2 参考极小值的「未收敛帧」问题（2026-10-17 07:39 起，进行中）
- **事件（技术性失败）**：ts_0014 的 build/candidate_opt（job 1007，起点 = 声明的 `conformers.reactant` = E2E3/i2_min_candA.xyz，sha256 1715f6d7d77e93bb5200a71b23db31fc84cb45564b1d48f6bbab2e7ee3c0ef85）以 `Error termination via Lnk1e in /home/ly/g16/l9999.exe at Sat Oct 17 07:39:17 2026` 结束（`Number of steps exceeded,  NStep=  42` @L18771；末次收敛表 Max Disp 0.674299 / RMS 0.291096）。run 权威态 = **blocked / stage build / rev 8**，failure_class = conformer_optimization_failed，needs = [conformers.reactant]。
- **纪律**：该 l9999/NStep 属**非预期技术性失败**，**不构成**「E3 无鞍点」「I2 不存在」或任何机理证据。
- **同一几何的历史**：job 971（E2E3/i2_candA_optfreq.log，sha256 c4e3e99136f11f537cfec51f8a2e6ae36ac616f43c3a12d70d6d15948daab182）NStep=48；job「compact」（E2E3/i2_candA_compact_optfreq.log，sha256 aa65642ff8952b141c638534c5972c469b2bbf74d417416ce99c41a973f5a4a4）NStep=51；两者**都没有频率段** ⇒ i2_min_candA.xyz 是「力判据达标、从未被判定收敛」的近极小值帧；job 990 是**在该固定几何上的 freq-only 单点**（0 虚频成立，但不能称「收敛极小值」）。
- **修复分支（主协调 R13/R13.2 已预授权；每步留证；手工在飞 ≤2 且顺序执行）**：
  - **A**：手工诊断 job **1012**（`opt=(calcfc,maxcycles=200) freq`，起点同几何，输入 E2E3/i2_min_conv_optfreq/i2_min_conv.gjf sha256 2301cd4bd9c7a9316aff6aa081a5040cface67a895ac28a582d40ba55b0962ca，priority 0、8c/10240MB）收敛后 → 写 provenance（日志绝对路径 + sha256 + 行号 + 末帧几何）→ `ts_resume(ts_0014, changes={conformers.reactant …})` ⇒ 参考构象不变。
  - **B′（已预置、未提交）**：E2E3/i2_min_readfc_optfreq/i2_min_readfc.gjf（sha256 **d87d2480b9cd34b34af444f637bfc336c0ec8cdc4ded5ad74bc096495e383802**；route = `opt=(readfc,maxcycles=200) freq` + 同批方法；坐标块与 i2_min_candA.xyz 逐位相同）+ 同目录 i2_min_readfc.chk（sha256 **343c0fd5576fdf3c491e98e1933e0a60b9cbd3582bb60f656a8c2521005b8f17**，= job 990 原 chk 的逐位副本）。仅在 A 失败后提交，不与 A 并行。
  - **B**：换构象种子（E2E3/i2_seed_candD_classB.xyz sha 78448225… → i2_seed_xtb_na3_p11/p12.xyz sha 10177bfa…/f5be86f6… → candB/candC），**并整批重算 I2 端参考能量、显式登记 E2/E3 起点定义改变**（新旧值不得混减）。
- **科学 caveat（缺测，不做数值推断）**：登记的 I2 参考极小值里 **O3···O9 = 4.19 Å、O3···H11 = 5.06 Å**（甲酸 O–H 背向甲氧基、无氢键），而 E3 的 TS 需要质子夹在 O3/O9 之间（guess 里 O1···O3 2.808）⇒ **P 端/参考端 DFT 构象搜索未做**；这也是把 E3 定为「I2→P 单步」时的已知口径风险；GFN2/ALPB 能量绝不与 DFT 混减。

## 6 索引口径与两处勘误（交付引用须知）
- **xTB scan 索引基准（道 as_f99001ff9213455c 实测消歧，帖 evt_9dc6143672e141e1）**：manifest 的 `atoms` 按 **0-based** 消费，job 1001（E2）与 job 1003（E3）都扫在**正确键**上（逐帧实测 C4–O3 1.542→3.900 Å、O3–H6 1.030→2.899 Å，对照键不动）；原生调用行 = E2E3/xtb_scan_e2/native_scan_runs/native_scan_0001/engine.out:85。**其能量是 GFN2/ALPB，只作几何/索引口径说明，不得与 DFT 相减。**
- **勘误 1（文件 sha）**：E2E3/I2_DFT_VERDICT.md 现 sha256 = **3e8859fb09753b35c7eb596214ebe20d23932b9525bcbe3e85d41a7c6e1e5fa3**；本包早先引用的 c6823c4fedd7afda4b733eeba33924ea505d9d3f47d6f70bbcbcd92591239590 是其**旧版**，已被取代。
- **勘误 2（时间）**：本包 07:4x 的若干记录曾把时刻误写为「08:0x」；实测 `date` = **2026-10-17 07:43:53 +0800 CST**，实际为 **07:4x**。只影响时间标注，不影响 sha256/行号/能量/结论。

## 7 回填计划（未执行；等待 ΔE‡）
- 文件（仅本会话写）：`cloudra/benchmark/normal_registry/yo.py`（Y3 step①/②/③ 的 barrier）；`ideapool/reaction_candidates/normal.md` 第 65 行（Y3 行）；`ideapool/tasks/normal/NY3.json`（重生成）。
- 命令：`python -m cloudra.benchmark.gen_normal_tasks` 然后 `pytest tests/test_benchmark.py -k regenerate_identically`（输出原样留档；guard 是 source↔committed 比较，因此**必须改 md 行 + registry 后同批重生成**）。
- 旧值 **15.5（文献 ΔG，Pliego & Riveros 2002）/ 12.5 / 0.0 一律作废、不回填**。
- ΔE‡ 口径：E(TS) − 该步自身起点极小值（E1: RC 967；E2: I1 985；E3: I2 990），全部同批 G16 纯电子能。

## 8 模型限制（交付 caveat）
- 水相以 **CPCM 隐式溶剂**表达，**无显式水**；Na⁺ 为「中性制衡」模型，未描述溶剂化壳层/反离子动力学；温度、浓度、离子强度均未建模。
- 题目文本里的实验条件为「NaOH 水溶液」；本模型把 OH⁻ 与 Na⁺ 置于同一 CPCM 空腔复合物中，因此得到的是**气相/隐式溶剂势能面上的机理与能垒**，不是实验自由能。
- 虚频判据只用 band 表 + `imaginary frequencies` 行；`Low frequencies` 行首负值不是振动模。
- 含 Na⁺ 多组分体系的 automatic reaction_mapping 会给出化学上错误的 unique 映射（平台 issue #179 P6）；本包 E2/E3 的 atom_map 均由人工按端点几何核定，未使用其自动结果。
