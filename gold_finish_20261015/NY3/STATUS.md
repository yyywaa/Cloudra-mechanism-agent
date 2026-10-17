# NY3 包 · 状态（Na⁺ 中性模型皂化 · NY3_E1/E2/E3）

第五任（**整合**）包 Coordinator **as_a396e35616564357**（本包唯一写权会话）｜主题 gold-finish-20261015｜更新 2026-10-17 07:3x +08:00
工作根：/home/ly/Cloudra-mechanism-agent｜包目录：gold_finish_20261015/NY3/
依据：BRIEF.md（§5 资源 / §9 机理选择政策）、LEDGER.md（R1–R5）、prep/PREP.md、E2E3/I2_SEED_NOTE.md、E2E3/I2_DFT_VERDICT.md

## 0 一句话状态
- **回填仍 0/3**（yo.py / NY3.json / normal.md 的 Y3 行尚未改）。
- **E1**：第 3 版 ts_opt（**job 1004**，guess = 扫描最高帧 2.503 Å）**收敛**：`Optimization completed.` / `-- Stationary point found.` @L17835/17836，E(RB3LYP) = **−466.985305161**（末次 SCF @L17712），末帧 O1···C4 **2.806** / O1–H6 0.965 / C4–O3 1.330 / C4=O5 1.221 Å；日志 sha256 `d11c078cb98c80f28b142f9c362be188664a9cbe4a5e41e310bcdc7a81b19487`。管线已排队 **job 1010 = frequency**（rev 43）⇒ **虚频数与虚频模归属待出**。**ΔE‡(E1) 未成立**（暂算 E(TS候选)−E(RC, job 967) ≈ +0.79 kcal/mol，须经「恰 1 虚频 + 该模以 O1–C4 为主 + IRC 双向 + 两端点 0 虚频」后才可用）。
- **E2/E3**：判定落定 = **分步**（I2 型 = DFT 0 虚频极小值，job 990，经我独立复算几何确认）⇒ E2 = I1→I2、E3 = I2→P 两条独立边。四条参考极小值中 **I2、P 已具 0 虚频证据**；RC/I1 的 0 虚频待 ts_0007 端点 Opt+Freq。**ΔE‡(E2/E3) 缺测**（TS 已建、未收敛）。
- **E2/E3 两条 durable run 已建（2026-10-17 07:2x，ts_prepare 均 accepted）**：E2 = **ts_0013**（rev 5 / build / job 1006 candidate_opt）、E3 = **ts_0014**（rev 5 / build / job 1007）；端点配对与 1-based 声要以 E2E3/E2E3_ENDPOINTS_PROVENANCE.md（sha256 e8b73ab49529e48a5c0e9e15cb9ba87481f21e98913613c268820323d03c8ba3）为准。E1 = **ts_0007 已推进到 rev 39 / declaration_0003 / job 1004**（guess = 扫描最高帧 2.503 Å）。
- 交付必须显式声明：本批引擎 = **Gaussian 16**，替代既有 gold 档的 ORCA；能量只在同批 Gaussian 内相减。

## 1 口径（不变）
- 引擎：Gaussian 16（/home/ly/g16/g16）｜B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight + SCRF=(CPCM,Solvent=Water)｜charge 0 / multiplicity 1（Na⁺ 中性模型，Na 不参与键变化）。**本机 Gaussian 只认 def2SVP（无连字符；连字符→l1 QPErr，issue #189）。**
- 能量：纯电子能（无 ZPE/热校正），只在**同批 Gaussian 日志内部**相减；相对**该步自身起点极小值**；不得与历史 ORCA 值混减。
- 资源：手工 QM ≤2 同刻、priority 一律 0、8c/≤10240MB；TS/IRC 只走 ts_prepare/ts_resume（手工 TS/IRC 提交被禁）。
- 原子序（reactant 序，1-based）：1 Na｜2 O1(羟基 O，带 H6)｜3 H6｜4 C2(甲基 C)｜5 O3(甲氧基 O)｜6 C4(羰基 C)｜7 O5(羰基 O)｜8-10 H(甲基)｜11 H(C4,甲酰 H)。
- 虚频判据：权威 = band 表（3N−6 模）+ `imaginary frequencies` 行；**Low frequencies 行的首个负值不是振动模**（已确认极小值上也有，如本包 -12.1370、P 端 -20.2987）。

## 2 写权与协作（防同包并发写）
- **写权（STATUS.md / yo.py / ideapool/tasks/normal/NY3.json / normal.md Y3 行 / 生成器与守卫）= 我 as_a396e35616564357**（主协调 2026-10-17 公告指定）。
- ts_0007 **管线驾驶** = 第 5 任 as_a0ffef5393594045（已 stand-down 写权，只读+终态后 resume；同刻不重复 revision）。
- **E2/E3 道** = small_mol **as_f99001ff9213455c**（几何/provenance/判定；回报走主题，首行 to: as_a341823c436e47ed 并 cc 我）。

## 3 已完成计算（原生日志；只读、不改写）
### 3a 孤儿 run（只能作历史/交叉核对，跨会话不可 ts_resume；issue #180）
| job | 内容 | 日志 | sha256 | 能量原始行 | 语义 |
|---|---|---|---|---|---|
| 919 | RC candidate_opt（ts_0002） | ts/ts_0002/jobs/declaration_0001/candidate_opt/seed-opt.log | 8c6991b38f699b214bf94d247794dbe080ce1859955db7b55d83e99ef4bb7e92 | −466.986564979 @L14762 | 离子-偶极复合物：Na-O1 2.093 / Na-O5 2.409 / O1···C4 2.803 / C4=O5 1.222 / O1-H6 0.965 Å |
| 922 | I1 product_seed_opt（ts_0002） | ../product_seed_opt/seed-opt.log | 658285856a60aee683a6e88e115a3e445ae4f3dcfa77703ee9479345314422ea | −467.004842486 @L14872 | 四面体 I1：C4-O1 1.427 / C4-O5 1.290 / C4-O3 1.503；H6 仍在 O1 |
| 927 | I1 candidate_opt（ts_0003） | ts/ts_0003/.../candidate_opt/seed-opt.log | db30483e93c5f7bc959a5b0eb74df3b17befca22dbf67888e5d32063c9984799 | −467.004842486 @L14872 | 与 922 同值 ⇒ I1 极小值两次独立复现 |
| 934 | I2 product_seed_opt（失败） | ts/ts_0003/.../product_seed_opt/seed-opt.log | 3ae4dccbe8ca3119d3fa0853b3bc5ac3743ba3abc3fa52a3314e3858048de8be | 末次 SCF −467.045443536 @L24228；l9999 @L24632 | 从 prep/i2.xyz 自由优化时 H6 由 O1 迁到 O3，末态已是 P；NStep=44 截断（Gaussian 自身） |

### 3b 本包正式 run **ts_0007（NY3_E1）**
| job | 内容 | 日志 | sha256 | 能量行 | 状态 |
|---|---|---|---|---|---|
| 967 | candidate_opt（RC） | ts/ts_0007/jobs/declaration_0001/candidate_opt/seed-opt.log | 730caaa08baa079eeac78ab5cc40bcfed285eda1044f578b281ce4a4f202f53f | −466.986564979 @L14762；Normal @L15168 | done；末帧 = RC 极小值（O1···C4 2.803） |
| 985 | product_seed_opt（I1） | .../product_seed_opt/seed-opt.log | 56e90cc4eea1dd7c5c1cd96e62a8db22ff2e7627ee190fc06eb9fa39720d3fe2 | −467.004842485 @L14872；Normal @L15296 | done；末帧 = I1 |
| 987 | ts_opt（refine，guess = prep/ts_e1_guess.xyz，O1···C4 2.192 Å） | .../ts_opt/refine.log | 36b3a6ad5cf75f560b6eca71ba07997636f0584f909861b370a4fde6441de105 | 末 SCF −466.981285573；l9999 @L21945 | **failed**：NStep=46 截断，末帧 O1···C4 漂回 2.351 Å（**不构成「无鞍点」证据**） |
| 997 | ts_opt（refine，guess = interp/img_05.xyz，O1···C4 2.086 Å） | .../declaration_0002/ts_opt/refine.gjf（log sha256 c69479aabbdc7df61ebedbb8c45ea4054727b2ab9bf666dce82922e5305279ef） | 末次 SCF −466.994187812 @L23363 | — | **failed（nonconvergence）**：NStep=45 截断 @L23495、l9999（06:50:56）；末帧 **O1···C4 滑到 1.539 Å**（滑向 I1 侧）、C4–O3 1.423、O1–H6 0.967 ⇒ 初猜距离偏短（**不作「无鞍点」证据**） |
| 1004 | ts_opt（refine，guess = E1/guess_scan_p04_d2503.xyz，O1···C4 2.503 Å） | .../declaration_0003/ts_opt/refine.gjf（log sha256 d11c078cb98c80f28b142f9c362be188664a9cbe4a5e41e310bcdc7a81b19487） | **−466.985305161 @L17712** | 07:21:45–07:25:46 | **done**：`Optimization completed.`/`Stationary point found.` @L17835/17836、Normal termination @L18089；末帧 O1···C4 **2.806**（≈RC 值）、O1–H6 0.965、C4–O3 1.330、C4=O5 1.221 ⇒ **鞍点候选**（是否真 TS 待 freq） |
| 1010 | frequency（管线自动，声 0003） | .../declaration_0003/frequency/frequency.gjf | （ready；终态后补） | — | **ready/排队**（rev 43）⇒ 出虚频数与虚频模归属 |

### 3c 手工弛豫扫描 **job 989**（E1；结论性证据，非平台管线）（2026-10-17 06:34–06:38）
- 输入：gold_finish_20261015/NY3/E1/E1_scan_O1C4.gjf，sha256 `8e2a37eb4e745d4d8196899d96183a67aa08ee3057c78615577424794cb0a1cf`；route `opt=modredundant b3lyp/def2svp + empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=water)`；起点 = job 967 RC 极小值；扫描键 `B 2 6 S 12 -0.1`（O1···C4 2.803→1.603 Å，13 点）。
- 原生日志：E1/E1_scan_O1C4.log，sha256 `62ac90e3732663dc82de1339fe1623b3e3457a4528d2d1f92d8bf3748442dca4`（40686 行）；**终止 = Error termination via Lnk1e (l9999) @L40683，"Number of steps exceeded, NStep= 45" @L40448**（第 5 点优化耗尽，Gaussian 自身失败，**不作「无鞍点」证据**）。
- **已收敛点表（判据 = `Optimization completed.`；点能量 = 该边界前最后一个 `SCF Done`；第 5 任独立重算与我逐位一致）**
| 点 | d(O1···C4)/Å | E(RB3LYP)/Ha | SCF Done 行 | 边界行 | ΔE vs RC/(kcal/mol) |
|---|---|---|---|---|---|
| 1 | 2.803 | −466.986565136 | L2285 | L2418 | −0.00（RC 极小值独立复现；job 967 = −466.986564979） |
| 2 | 2.703 | −466.986190365 | L9284 | L9429 | +0.24 |
| 3 | 2.603 | −466.984669315 | L14020 | L14164 | +1.19 |
| 4 | **2.503** | **−466.981571100** | L19607 | L19754 | **+3.13（最高已收敛点）** |
| 5 | 2.403 | 未收敛（末次 SCF −466.984727401 @L40314） | — | — | **不作证据** |
- ⇒ 已收敛区间沿 d(O1···C4) 缩短方向**单调上升**，最高收敛点在 2.503 Å，而未收敛的 2.403 Å 帧更低 ⇒ **鞍点大概率在 ≈2.40–2.55 Å**（与 job 987 从 2.192 Å 漂到 2.351 Å = 朝更长距离爬一致）。
- **备用 provided guess（已落盘）**：E1/guess_scan_p04_d2503.xyz（sha256 `2a9bb8506de69d5cd20a1e90371868d8edb6f482013c0447811219157bc66e22`，11 原子，reactant 序，坐标取自日志 L19384–19394）；provenance = E1/E1_SCAN_PROVENANCE.md（sha256 `30b625eb003acacbfb3070aa68072656dd448008a18ef62df6ec8c5b3bbc8e63`）。
- **勘误（2026-10-17 07:0x）**：本文件前一版 §4 列的「逐点末次 SCF：pt1 −466.984281494 / pt2 −466.982790247 / pt3 −466.979565357 / pt4 −466.974209173」**全部撤回**——那是用 `scan point N` 行作分界造成的**点内中间步能量**错配；权威值以本节上表为准（第 5 任 as_a0ffef5393594045 同轮公告同一撤回，两方数字逐位一致）。

### 3d E2/E3 的 DFT 证据（同批 Gaussian 16、同 route）
| job | 内容 | 日志 | sha256 | 读数 |
|---|---|---|---|---|
| 971 | I2 型候选 Opt（起点 = xTB 极小 candA，H6 远离 O3） | E2E3/i2_candA_optfreq.log | c4e3e99136f11f537cfec51f8a2e6ae36ac616f43c3a12d70d6d15948daab182 | **力判据已收敛**（Max Force 0.000120<0.00045、RMS 0.000040<0.0003，L21871–21874）但位移未达、**NStep=48 截断（l9999）**、**无频率段**；末帧（L21720）E = −466.986020418，几何 = I2 型 |
| 981 | 同上（紧凑起点） | E2E3/i2_candA_compact_optfreq.log | aa65642ff8952b141c638534c5972c469b2bbf74d417416ce99c41a973f5a4a4 | NStep=51 截断、力判据**未**收敛（0.006789）、无频率段 ⇒ 不作 I2 极小值证据 |
| **990** | **I2 型候选 freq（几何 = job 971 末帧抽帧 i2_min_candA.xyz）** | **E2E3/freq_i2_candA/i2_candA_freq.log** | **df2548644fc22ac7b64b0da08bded3f44e1ecc9f4db1c5e2015aa2ed954e598b** | Normal termination @L1470；E = **−466.986020418 @L512**；**9 组 band = 27 = 3N−6 全实**（最低 21.6936/25.3657/39.6978 @L770），日志内 `imaginary` 出现 0 次 ⇒ **0 虚频**；Low frequencies 首值 −12.1370 @L760 非振动模 |
| **994** | **P 端 Opt+Freq（起点 = job 934 截断的 P 型末帧）** | **E2E3/p_optfreq/p_ref_optfreq.log** | **ff7ecb5aab3724bd2574c37c9a78b309e45f7eabfeb5ec9ec703c53860f816df** | `Optimization completed.` @L10591 / `Stationary point found.` @L10592 / 2× Normal termination（@L10845、@L12318）；E = **−467.045937735 @L10443**；27 模**无虚频**（最低 44.5544/85.1565/98.2713）；极小值几何 = p_min_ref.xyz（sha256 f69ef3c9215d95fe31a17d4cfecc9a2a0bf111fd932894bf0f236a985348f4ea，i2 序） |
- **我（as_a396e35616564357）对 job 990 几何的独立复算**（读 i2_candA_freq.log 的 Standard orientation 块，L204+，i2 序 1 Na｜2 C2｜3 O3｜4-6 H(Me)｜7 C4｜8 O5｜9 O1｜10 H(C4)｜11 H6）：O1–H6 **0.972**｜C4–O1 1.326｜C4=O5 1.209｜**C4···O3 4.568**｜O3···H6 5.056｜Na–O3 2.047｜Na–O5 2.312｜Na–O1 3.381 Å ⇒ **I2 型（甲酸 + 甲醇盐 + Na⁺，H6 仍在 O1）成立**，与道报数逐位一致。
- 极小值间能量（同批 G16 纯电子能，**不是能垒**）：RC −466.986564979（967）｜I1 −467.004842485（985）｜I2 −466.986020418（990）｜P −467.045937735（994）⇒ I1 比 RC 低 11.47；I2 比 I1 高 **+11.81**、比 RC 高 +0.34；P 比 I2 低 **−37.60**、比 I1 低 −25.79 kcal/mol。

## 4 参考极小值登记（BRIEF §5b：job / 绝对路径 / sha256 / 0 虚频）
| 边 | 极小值 | job | 绝对路径（工作根下） | sha256（原生日志） | 0 虚频 |
|---|---|---|---|---|---|
| E1 起点 | RC | 967 | ts/ts_0007/jobs/declaration_0001/candidate_opt/seed-opt.log | 730caaa08baa079eeac78ab5cc40bcfed285eda1044f578b281ce4a4f202f53f | 待 ts_0007 反应物端点 Opt+Freq |
| E1 终点 / E2 起点 | I1 | 985 | ts/ts_0007/jobs/declaration_0001/product_seed_opt/seed-opt.log | 56e90cc4eea1dd7c5c1cd96e62a8db22ff2e7627ee190fc06eb9fa39720d3fe2 | 待 ts_0007 产物端点 Opt+Freq |
| E2 终点 / E3 起点 | I2 | 990（几何=971 末帧） | gold_finish_20261015/NY3/E2E3/freq_i2_candA/i2_candA_freq.log；几何 E2E3/i2_min_candA.xyz | df2548644fc22ac7b64b0da08bded3f44e1ecc9f4db1c5e2015aa2ed954e598b（几何 1715f6d7d77e93bb5200a71b23db31fc84cb45564b1d48f6bbab2e7ee3c0ef85） | **✓ 0 虚频**（27 模全实） |
| E3 终点 | P | 994 | gold_finish_20261015/NY3/E2E3/p_optfreq/p_ref_optfreq.log；几何 E2E3/p_min_ref.xyz | ff7ecb5aab3724bd2574c37c9a78b309e45f7eabfeb5ec9ec703c53860f816df（几何 f69ef3c9215d95fe31a17d4cfecc9a2a0bf111fd932894bf0f236a985348f4ea） | **✓ 0 虚频**（`Stationary point found`） |
- 限定（如实）：job 990 的几何来自 job 971 末帧（力判据满足、位移判据未达、无 `Stationary point found`）；它 + job 994 已在**固定几何上**给出 0 虚频。若验收要求「Opt+Freq 收敛 + 0 虚频」的端点身份，补一次该几何的 opt+freq 复算即可（成本小，起点已在驻点上）——**列入待办**。

## 5 E1（NY3_E1 = RC→I1）现状与下一步
- 曲线：job 987（guess 2.192 Å）l9999 漂向 RC 侧 ⇒ 不用；job 989 定位鞍点区 ≈2.40–2.55 Å ⇒ 备用 guess 落盘；job 997（IDPP img_05，2.086 Å）**亦 failed**（l9999 / NStep=45、末帧滑到 I1 侧）⇒ 第三次 ts_opt 已用**扫描最高帧**启动（**job 1004**，declaration_0003）。两类初猜各失败一次，说明该鞍点位于浅势区、Berny 步长不足。
- 已建 E2/E3 两条 run（本轮）：E2 = **ts_0013**、E3 = **ts_0014**（均 rev 5 / build / candidate_opt 1006/1007），端点几何与 mol 同序、1-based 声明见 E2E3/E2E3_ENDPOINTS_PROVENANCE.md。
- **2026-10-17 07:26 更新（下列分叉条目起作废）**：job 997 已 failed、**job 1004 已 done 且 ts_opt 收敛**（`Stationary point found.` @L17836，E = −466.985305161 @L17712，末帧 O1···C4 2.806 Å ≈ RC）⇒ 管线排队 **job 1010 frequency**（rev 43）。freq 出后必须核「恰 1 虚频 + 该模以 O1–C4 为主」，否则按 BRIEF §4/§9 记 pseudo-saddle；若合格则继续 IRC 双向 + 两端点 Opt+Freq。
- **构象级差异（第 5 任 as_a0ffef5393594045 只读复核，帖 evt_5c34f5d919744521）**：job 1004 收敛点与 RC 的差别集中在 **甲基旋转**（H8/H9/H10 位移 ≈1.0 Å；二面角 D(8,4,5,6) −60.4° → −120.9°）与 **羟基 H 旋转**（H3 位移 0.295 Å；D(1,2,3,11) −152.4° → +155.0°），骨架键长几乎一致；四条收敛判据全 YES（Max Force 0.000012 / RMS 0.000004 / Max Disp 0.001541 / RMS Disp 0.000630 @L17830–17833）⇒ 该驻点**很可能是反应物复合物的另一构象极小值（或取向类软鞍点），而非 O1–C4 成键 TS**。freq 分叉判据：0 虚频 ⇒ 构象极小值（换初猜）；恰 1 且模以 O1–C4 为主 ⇒ 继续 IRC/端点；1 虚频但为甲基/羟基转动 ⇒ pseudo-saddle（如实标注、不回填）；≥2 虚频 ⇒ 高阶鞍点，不得当 TS。
- [历史] 判据分叉：job 997 若收敛 ⇒ 直接进 freq（恰 1 虚频 + 虚频模归属 O1–C4 成键）→ IRC 双向 → 两端点 Opt+Freq（RC / I1）→ ΔE‡ = E(TS) − E(RC，job 967)。
- [历史，已执行] job 997 若再 l9999/漂移 ⇒ 终态后立即以 **E1/guess_scan_p04_d2503.xyz** 走 ts_resume（同一 run，declaration_0003），其余不变。
- 记录要求：ts_inspect 逐段 `result.outcome` 原文（TS 虚频数与虚频模、IRC 端点归属、两端点 0 虚频）全部回填本文件。

## 6 E2/E3 判定（BRIEF §9 包内自决，已定）与下一步
- **判定（2026-10-17 07:0x，采纳）= 分步**：I2 型 = DFT 0 虚频极小值（job 990 + 我独立复算几何）⇒ **E2 = I1→I2 独立边**（产物端种子用 i2_min_candA.xyz 几何）、**E3 = I2→P 独立边**。
- ⚠ **待消解的技术风险（采纳任何 TS 初猜前必须做）**：E2E3/xtb_scan_e2/scan_e2_manifest.json（`bond [3,2] 1.55→3.9`）与 xtb_scan_e3/scan_e3_manifest.json（`bond [2,10] 1.05→2.9`）只在 **0-based** 读法下化学正确（→ C4–O3、O3–H6）；两个 manifest 的 reactant_xyz 序 = ts_0007 product/I1 序（1 Na｜2 C2｜3 O3｜4 C4｜5 O1｜6 O5｜7-9 H(Me)｜10 H(C4)｜11 H6）。而 ts_prepare/ts_resume 文档规定 **Gaussian/xTB scan 引用是 1-based** ⇒ 若接口按 1-based 解释就会扫错键（O3–C2 / C2–H(C4)）。**已派道用 2 点实测消歧 + 按正确索引重出 manifest**（1-based 应为 E2 = [4,3]、E3 = [3,11]）。
- ✅ **已消解（2026-10-17 07:2x，道 as_f99001ff9213455c 实测，帖 evt_9dc6143672e141e1）**：manifest 的 `atoms` 按 **0-based** 消费，两条扫描都扫在**正确键**上 ⇒ 上文「按 1-based 读会扫成 O3–C2 / C2–H(C4)」的假设**被证伪**，无需重出 manifest。逐帧实测（awk 直接读帧文件，非转述）：
  - job 1001（E2，输入 i1 序）：声明（1-based）[4,3] = C4–O3；manifest 存值 [3,2]；实测 **C4–O3 1.542（点1）→2.525（点6）→3.508（点11）→3.900（点13）Å**，对照键 O3–C2 全程 1.35–1.42 Å **不动** ✓
  - job 1003（E3，输入 i2 序）：声明 [3,11] = O3–H6；manifest 存值 [2,10]；实测 **O3–H6 1.030（点1）→1.683（点5）→2.208（点8）→2.899（点12）Å**，对照键 C2–H(C4) 5.57–6.31 Å **不动** ✓
  - 原生调用行（本轮实测原文，实测文件:行 = `E2E3/xtb_scan_e2/native_scan_runs/native_scan_0001/engine.out:85`）：`program call : xtb …/input.xyz --gfn 2 --opt --input …/scan.inp --parallel 1 --chrg 0 --uhf 0 --verbose --alpb water`（GFN2 + ALPB water 生效）；`input.xyz` 与 manifest 的 `reactant_xyz` 逐位相同。完整表见 I2_DFT_VERDICT.md §8.1。
  - **口径边界**：manifest 与两条扫描现仅可用于「索引/几何口径说明」；其能量是 **GFN2/ALPB**，**绝不可与任何 DFT 值相减**。
- 已完成：道交付 ts_e2_guess.xyz / ts_e3_guess_v2.xyz + provenance；我建 E2/E3 两条 durable run（ts_prepare）→ 管线 ts_opt→freq→IRC→两端点。
- **独立复核（道 as_f99001ff9213455c 只读核对 ts_0013/ts_0014 的 declare.json，帖 seq 98601）**：run 的 reactant 元素序列 = 声明的序（ts_0013 = i1 序、ts_0014 = i2 序）；atom_map 与我给的 1-based 映射整体减 1 一致；reaction_center 按 0-based 读正是 E2（断 C4–O3／成 C4=O5）与 E3（断 O1–H6／成 O3–H6）⇒ **未触发 Na⁺ 体系自动映射误判（issue #179 P6）**。裁决文书 E2E3/I2_DFT_VERDICT.md **现** sha256 `3e8859fb09753b35c7eb596214ebe20d23932b9525bcbe3e85d41a7c6e1e5fa3`（本轮 sha256sum 实测；道已更新该文件加入 §8 索引消歧表）——**勘误**：本文件此前引用的 `c6823c4fedd7afda4b733eeba33924ea505d9d3f47d6f70bbcbcd92591239590` 为其**旧版**、已被取代，引用时一律用新值。
- 声明预备（须按最终几何复核）：E3 atom_map 预推 = [1,2,3,4,5,6,11,7,8,9,10]；reaction_center（1-based）= [[9,11],[3,11]]（断 O1-H6、成 O3-H6）。reaction_mapping 对含 Na⁺ 多组分体系会给化学上错误的 unique 映射（issue #179 P6）。

## 7 逐边状态
| 边 | run | stage | 在飞作业 | 状态 |
|---|---|---|---|---|
| NY3_E1 (RC→I1) | **ts_0007**（rev 43 / declaration_0003） | refine | job 1010 frequency（ready） | ts_opt **收敛**（job 1004，E=−466.985305161，O1···C4 2.806）；虚频数与模归属待出；**ΔE‡ 未成立（暂 ≈+0.79 kcal/mol）** |
| NY3_E2 (I1→I2) | **ts_0013**（rev **9**） | build | job **1011** product_seed_opt（ready，队列位置 4） | 判据 = 分步；**build/candidate_opt（job 1006）已 done 且收敛** ⇒ 反应物端身份 = I1 极小值（E 与 job 985 差 1e-9 Ha，见 §13）；guess = ts_e2_guess.xyz；**ΔE‡ 缺测** |
| NY3_E3 (I2→P) | **ts_0014**（rev 8） | build | **无（blocked）** | 端点 I2/P 极小值；guess = ts_e3_guess_v2.xyz；**candidate_opt job 1007 l9999 失败 ⇒ build 阻塞**（conformer_optimization_failed，needs=conformers.reactant，见 §15）；已提交 I2 极小值复优化 **job 1012**；**ΔE‡ 缺测** |

## 8 回填进度（0/3）与计划
- 目标文件（仅我写）：cloudra/benchmark/normal_registry/yo.py 的 Y3 step barrier；ideapool/tasks/normal/NY3.json（重生成）；ideapool/reaction_candidates/normal.md 的 Y3 行（第 65 行）；随后 `python -m cloudra.benchmark.gen_normal_tasks` + `pytest tests/test_benchmark.py -k regenerate_identically`（输出原样留档）。
- 每条边登记参考极小值（本文件 §4）+ ΔE‡ 的 TS 证据行；旧值 15.5（文献 ΔG）/12.5/0.0 **作废、不回填**。
- 交付单列「证据驱动的机理修订」：本包已有一条 = **E2/E3 由「合并疑云」→「分步」**（旧→新 + 依据 job 990 + 独立复算 + 影响面仅 E2/E3）。

## 9 变更与勘误
- 2026-10-17 07:2x（第五任整合）：登记第 5 任只读复核的构象级差异（甲基/羟基旋转，帖 evt_5c34f5d919744521）+ freq 四分叉判据；主协调 R11 的「E1 反应中心 = C4–O3」口径错误已由我更正（E1 = 成 O1–C4 / 断 C4=O5 π，即 1-based [[2,6],[6,7]]；C4–O3 属 E2），主协调已在 LEDGER R11.1 采纳更正。
- 2026-10-17 07:26（第五任整合，关键进展）：**job 1004（ts_0007 第 3 版 ts_opt）done 且收敛**（`Stationary point found.` @L17836；E = −466.985305161 @L17712；日志 sha256 d11c078cb98c80f28b142f9c362be188664a9cbe4a5e41e310bcdc7a81b19487）；末帧 O1···C4 2.806 Å ≈ RC 值 ⇒ 已在 §5 登记「虚频模可能不在 O1–C4 键对上」的判读风险。管线排队 **job 1010 frequency**（rev 43）。E2/E3（ts_0013/ts_0014）仍 build / job 1006/1007 ready（队列位置 1/2）。
- 2026-10-17 07:1x（第五任整合，巡检轮）：三边管线作业（1004/1006/1007）截至 07:09 仍为 ready/排队（free cpus = 0，全机 4 个 g16 在跑，属正常排队，**未重复提交**）；登记道的独立声明复核（帖 seq 98601）与 E2E3/I2_DFT_VERDICT.md sha256 c6823c4f…；xTB manifest 索引基准消歧作业仍为 1001/1003（各 1 cpu，道在做，**结论未到，不使用其任何扫描结论**）；新增交付预备件 DELIVERY_NOTES.md（sha256 778a4174e68a2ef3747079cb302c5e7c47ce9d1f08937d43a0b85b7554c7ce5b）。本包手工在飞 = 0（遵守队列纪律）。
- 2026-10-17 07:3x（第五任整合，本轮）：job 997 失败登记（NStep=45、末帧 O1···C4 1.539 Å、log sha256 c69479aabbdc…）；按扫描最高帧（2.503 Å）ts_resume（rev 32→33 → run rev 39）→ job **1004**；**建 E2 = ts_0013 / E3 = ts_0014 两条 durable run**（ts_prepare accepted、无 blocked）；新增 E3 产端几何 E2E3/p_min_ref_pmol_order.xyz（sha256 bca75d0ac100298d955b3826fc8ade3bc1413783ed905d5dca62d57a83486d8b，按 prep/p.mol 序重排）；新增 E2E3/E2E3_ENDPOINTS_PROVENANCE.md。
- 2026-10-17 07:0x（第五任整合接任）：全量重写本文件；登记 job 989 修正后逐点表 + 撤回旧错值、job 990/994 的 0 虚频与身份、job 997 在跑、E2/E3 判定=分步、xTB manifest 索引基准风险、备用 guess 与 provenance（含 sha256）、写权/驾驶分工。
- 2026-10-17 06:4x（第四任）：登记 job 987 失败、job 989 扫描、E2/E3 道派发（已由本节取代相关表述）。
- 旧值 15.5（文献 ΔG）/12.5/0.0 与前一版 §4 的错配逐点能量一律作废。
- 2026-10-17 07:3x（本轮巡检）：登记 xTB 索引基准**实测消歧结论**（0-based 消费、两扫描键正确；见 §6、§10）与 E2 备用初猜、E3 扫描的 P 端构象风险（§10/§11）；**勘误**：E2E3/I2_DFT_VERDICT.md 现 sha256 = 3e8859fb09753b35c7eb596214ebe20d23932b9525bcbe3e85d41a7c6e1e5fa3，取代本文件此前引用的 c6823c4f…。

## 10 E2 备用初猜与 xTB 剖面（道交付，本轮登记）
- 主初猜不变：E2E3/ts_e2_guess.xyz（sha256 8bbc6dbb866df8619b5a150b6c3ea196c575d3b0b9e1398a89b9497de32e9ea0，IDPP frame 3，C4–O3 2.417 Å），已被 ts_0013 采用。
- **备用第二来源（弛豫帧；同 i1 序，可直接替换）**：E2E3/ts_e2_guess_xtb.xyz｜sha256 **74fa12bc12d95e9d4250c20e9b0ce7dc96ad1f49e021230e80afb3bfeeb42986**（本轮 sha256sum 实测；= E2 xTB 扫描 point_0006 弛豫几何：C4–O3 2.525｜C4–O5 1.215｜C4–O1 1.297｜O1–H6 0.981｜Na–O3 1.897 Å）；provenance E2E3/TS_E2_GUESS_XTB_PROVENANCE.md｜sha256 **891ceb88e2aece1fb2382414ee7c3ab59e8d89d7c0c806c0d178dba2ffa78220**（本轮实测）。
- E2 的 xTB 剖面（**GFN2/ALPB 约束弛豫扫描；不是 DFT 能垒、不是 ΔE‡**）：0.0（1.54 Å）→ +20.9（2.53）→ **+23.2（3.51，工具判峰）** → +23.1（3.90）kcal/mol；2.5–3.9 Å 全在峰顶 2.3 kcal/mol 内（极平顶、晚型）。

## 11 E3 扫描**不可**用作初猜 + P 端构象风险（如实登记，不填数）
- job 1003（E3）逐帧：O3–H6 1.030→2.899 Å 跟着扫描走（索引已消歧），但 **O1–H6 在点 1 就是 5.056 Å** 且点 1–10 恒为 5.0–5.8 Å ⇒ 该扫描**从未采样「质子夹在 O1/O3 之间」的几何**；能量单调升到 **+108.0 kcal/mol（点 10）**，点 11 出现 **78.9 kcal/mol 跳变**后质子跳到 O1（O1–H6 0.981）落到 **+29.1** kcal/mol 的 I2 型区。
- 含义：**GFN2/ALPB 把 DFT 的 P 极小值弛豫成了另一个构象**（GFN2 偏好 Na⁺ 三配位、甲醇不再与甲酸根氢键；DFT 的 P 极小值里 O1–H6 = 1.605 Å，GFN2 里 ≈5.06 Å）⇒ **P 端多构象问题**，尚未做 DFT 构象搜索（**缺测**）。
- 处置：E3 初猜仍只用 DFT 两端点之间的 IDPP 帧 E2E3/ts_e3_guess_v2.xyz（O1–H6 1.536｜O3–H6 1.409｜O1···O3 2.808 Å）；**ts_0014 的 IRC 产物端身份一律以 DFT 侧为准**；**GFN2 与 DFT 能量绝不混减**。
- 备用 guess（若 ts_0013/ts_0014 失败时可用）：ts_e2_guess_xtb.xyz、E2E3/ts_interp_e2/img_01,02,04、E2E3/ts_interp_e3/img_08,10（均在 E2E3/ 下）。

## 12 本轮巡检（2026-10-17 07:3x）
- ts_inspect：**ts_0007** rev 43 / stage refine / status waiting / waiting_for job **1010**（purpose frequency，state ready，8c/10000MB，input ts/ts_0007/jobs/declaration_0003/frequency/frequency.gjf）；**ts_0013** rev 5 / build / waiting_for **1006**（candidate_opt，ready，8c/10240MB）；**ts_0014** rev 5 / build / waiting_for **1007**（candidate_opt，ready，8c/10240MB）。三段 **result=null、blocked=null**（另有 ts_0007 的 ts_opt stage 已 done，job 1004）⇒ **本轮无新增 stage result.outcome 可回填**。
- query_compute_queue：running **998/999/1000/1005**（各 8c/10240MB，priority 0）；queued 位置 1–5 = **1006, 1007, 1008, 1009, 1010**；free cpus = **0** ⇒ 关键路径（1010/1006/1007）在**正常排队**：未重复提交、未调 priority、未杀他人作业；本包手工在飞 = **0**。
- 回填仍 **0/3**（三边均缺合格 TS 证据）⇒ 回填前不得改 yo.py / NY3.json / normal.md 第 65 行。

## 13 E2（ts_0013）build/candidate_opt 阶段证据（2026-10-17 07:3x，原文口径）
- **stage = candidate_opt（job 1006）已 done**：日志 `ts/ts_0013/jobs/declaration_0001/candidate_opt/seed-opt.log`，sha256 **2d4a1b03e2938ddc4af110683fbdf65852adc3d0e10067f94dfbc98954309369**（本轮 sha256sum 实测）；`Optimization completed.` @L789 + `-- Stationary point found.` @L790；`Normal termination of Gaussian 16 at Sat Oct 17 07:35:40 2026` @L935；E(RB3LYP) = **−467.004842486** @L549；输入 seed-opt.gjf sha256 0de1c9d35da5db9059c2bf4f448502477aee83338c9cc4e70d8cbedde12ab65b（route = `#p opt b3lyp/def2svp empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=water)`，**本阶段只有 opt、无 freq**）；几何 optimized_seed.xyz sha256 **fdf9531006a29ef733ec58bedec5c822826cb464c63c1af1742265e43315590c**。
- **身份（反应物端 = I1 极小值）**：E = −467.004842486 与 §4 登记的 I1 参考极小值（job 985，−467.004842485）**差 1e-9 Ha（≈6×10⁻⁷ kcal/mol）** ⇒ 管线把 E2 反应物端候选优化回了 **I1 极小值**，与「E2 = I1→I2 独立边」一致。
- **几何（本轮 awk 由 optimized_seed.xyz 实测；序 = ts_0013 建库序 1 Na｜2 C2｜3 O3｜4 C4｜5 O1｜6 O5｜7-9 H(Me)｜10 H(C4)｜11 H6）**：C2–O3 1.403｜**C4–O3 1.503**｜C4–O1 1.427｜C4=O5 1.291｜**O1–H6 0.971（H6 仍在 O1）**｜Na–O3 2.294｜Na–O5 2.206｜C2–H7 1.105｜C4–H10 1.125 Å ⇒ 单端质子化烷氧基型（H6 未迁移）、C4–O3 仍成键 = I1 型。
- 待办（口径）：该 stage 是 **opt-only**，故「端点 0 虚频」**尚未**由本 stage 建立；正式端点身份证据仍须来自管线的端点 Opt+Freq（reactant_frequency / product_frequency）或 IRC 产物端优化。
- run 状态：**rev 5 → 9**，stage build / waiting job **1011**（product_seed_opt，ready；输入 = i2 序几何：Na｜C｜O｜H｜H…）。E3（ts_0014）candidate_opt（job 1007）**正在跑**（07:38 仍在 SCF 迭代；EnMin = −466.986024240492，与 I2 参考 job 990 的 −466.986020418 同区域）。

## 14 下一轮巡检动作（不变）
1) 1010（E1 frequency）终态 → 读 band 表 27 模 / imaginary 行 / 能量行，判 0-1-≥2 虚频与最低模 O1(2)–C4(6) 分量占比；2) 1011（E2 product_seed_opt）、1007（E3 candidate_opt）终态 → build 收尾后自动进 ts_opt，随时 blocked 用 ts_resume 修；3) ΔE‡ 三条齐全前不进回填。

## 15 E3 build 阻塞（job 1007 l9999）与 I2 极小值复优化（2026-10-17 07:39–07:44 CST）
- **管线权威态**：ts_inspect(ts_0014) = **status blocked / stage build / rev 8**；`failure_class = conformer_optimization_failed`，`message = "candidate_opt job 1007 failed; revise or retry through ts_resume."`，`needs = ["conformers.reactant"]`，`editable_groups = reaction/calculations/conformers/guess/ts_optimization/verification/execution`；`failed_attempt` 记 log_sha256 = 42eae1463d39094f4e9be22c24a7ae0449fe68e591280a4687c42ffb37e909ab、input_sha256 = a408d306cfa7e242cd3ab41b5041850571671c4ca207936d646d1974c03164d3。
- **job 1007 终止原文**：`-- Number of steps exceeded,  NStep=  42` @L18771；`Error termination request processed by link 9999.` @L19000；`Error termination via Lnk1e in /home/ly/g16/l9999.exe at Sat Oct 17 07:39:17 2026` @L19001；末次收敛表 Maximum Displacement 0.674299 / RMS 0.291096（远未收敛）；最后 SCF E(RB3LYP) = **−466.984880863** @L18644（比 I2 参考 −466.986020418 高 ≈0.7 kcal/mol）；cpu 23m21.6s / elapsed 3m28.1s。route（逐字）= `#p opt b3lyp/def2svp empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=water)` ⇒ **def2svp 无连字符，不是 issue #189**；本阶段 opt-only、无 freq。
- **关键判定**：失败起点**就是本 run 已声明的 `conformers.reactant`** = E2E3/i2_min_candA.xyz（sha256 1715f6d7d77e93bb5200a71b23db31fc84cb45564b1d48f6bbab2e7ee3c0ef85）⇒ 原样重声明 = 原地复现同一失败点，**不是修订**。同一几何此前两次 opt+freq 亦全部 NStep 截断且**无任何频率段**：i2_candA_optfreq.log（sha256 c4e3e99136f11f537cfec51f8a2e6ae36ac616f43c3a12d70d6d15948daab182）NStep=48 @L21877；i2_candA_compact_optfreq.log（sha256 aa65642ff8952b141c638534c5972c469b2bbf74d417416ce99c41a973f5a4a4）NStep=51 @L23035（两日志 `Frequencies --` 计数 = 0）。结论：该帧是「力判据达标、从未被判定收敛」的近极小值。
- **纪律**：l9999/NStep 属**非预期技术性失败**（与主协调 R13 一致），**不得**当作「E3 无鞍点」或任何机理证据。
- **本轮动作**：提交手工诊断作业 **job 1012**（node-local、priority 0、8c/10240MB、is_async；本包手工在飞 = 1）：输入 `gold_finish_20261015/NY3/E2E3/i2_min_conv_optfreq/i2_min_conv.gjf`（sha256 **2301cd4bd9c7a9316aff6aa081a5040cface67a895ac28a582d40ba55b0962ca**），route = `#p opt=(calcfc,maxcycles=200) freq b3lyp/def2svp empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=water)`，起点 = 同一 i2_min_candA.xyz，工作目录 `gold_finish_20261015/NY3/E2E3/i2_min_conv_optfreq/`。目的 = 用精确初始 Hessian + 更长步数上限**收敛**该近极小值，得到「Stationary point found + 0 虚频」的 I2 极小值（既作 conformers.reactant 修订种子，也把 I2 端点身份从 freq-only 升级为收敛极小值）。**该作业在收到主协调 R13 之前已提交，已在 hub 帖 evt_7f6c948088004108 向主协调透明登记，并承诺不再新增第三个手工作业。**
- **修订分支（经 ts_resume，由本会话唯一写权执行）**：A 若 1012 收敛 ⇒ 写 provenance（日志绝对路径 + sha256 + 行号）后 `ts_resume(ts_0014, changes={conformers:{reactant:{kind:"file", xyz_path:<收敛几何>, mol_path:<同一 I2 mol>, evidence_refs:[<provenance>], optimization:{ref:"g16"}, heavy_atom_binding:{indices:[1,2,3,7,8,9]}}}}, reason=…)`，重跑 build→ts_opt（参考极小值仍是原 DFT I2 构象，ΔE‡ 参考不变）；B 若 1012 仍不收敛 ⇒ 换构象种子（E2E3/i2_seed_candB_methoxide_out.xyz sha bc247792…／candC sha 3cb50421…／candD_classB sha 78448225332a095326025a2c3beaa891c287746889656f7cba6d83bd4856c840，均在 prep/i2 序 = 本 run 反应物序），**并显式登记「参考极小值构象改变」及其对 ΔE‡ 参考的影响**。
- **E2 同款风险预警**：ts_0013 的 `conformers.product` 用**同一 i2_min_candA.xyz 几何** ⇒ job 1011（product_seed_opt，ready，队列位置 3）有很高同款失败概率；若失败，用同一修复改 `conformers.product`。
- 已通知道 as_f99001ff9213455c（hub call evt_e53a8febecf4443e）：**不要重复优化同一几何**，并备好可用的备用 I2 构象种子文件（含 provenance）。

## 16 I2 构象的科学观察（登记为缺测，不做数值推断）
- 本包登记的 DFT I2 极小值（job 990 几何 = i2_min_candA.xyz，i2 序）：**O3···O9 = 4.19 Å、O3···H11 = 5.06 Å**（甲酸的 O–H **背向**甲氧基、不成氢键），C2–O3 1.349｜C7–O8 1.209｜C7–O9 1.326｜O9–H11 0.972｜Na–O3 2.047｜Na–O8 2.303 Å（Na⁺ 桥联甲氧基 O 与甲酸羰基 O）。
- 而 E3（I2→P；1-based 断 [9,11]／成 [3,11]）的 TS 需要质子夹在 O3/O9 之间（guess ts_e3_guess_v2.xyz：O1–H6 1.536｜O3–H6 1.409｜O1···O3 2.808 Å）⇒ **参考极小值与 TS 所在构象不同**，属道的「P 端多构象」提示的直接体现。DFT 侧构象搜索**缺测**；不与 GFN2/ALPB 能量混减；本项**不影响**已登记的 ΔE‡ 定义（E3 参考仍取该 DFT I2 极小值），但若最终改用别的构象作参考，必须在交付里显式登记。
- 2026-10-17 07:4x（本轮）：登记 §15（E3 build 阻塞 + job 1012 + 修订分支）、§16（I2 构象观察）与 §7 E3 行更新；向主协调回报 R13（hub 帖 evt_7f6c948088004108），并 call 道 as_f99001ff9213455c 要求「勿重复优化 + 备用构象种子」。

## 17 备用 I2 构象种子 + readfc 备选修复（道交付 evt_44bb2ca13a6c4a48；本轮 sha256sum 实测逐项核对）
- 道 as_f99001ff9213455c 交付的可用种子（**全部 i2 序**，本轮实测 sha 与道所报逐位一致）：
  - E2E3/i2_seed_xtb_na3_p11.xyz = **10177bfad77af2cee20e8b3191c7265ad271c29bd5ff7471f63bd3b222568e44**（O1–H6 0.981｜O3···H6 2.731｜C4···O3 3.908｜C4–O5 1.210｜C4–O1 1.291｜Na–O3 1.887 / Na–O5 2.043 / Na–O1 3.377；来源 job 1003 反向扫描 point_0011）
  - E2E3/i2_seed_xtb_na3_p12.xyz = f5be86f6102d80c1c4395246f6b1917b2d568f7e9c920ee7954fd0fe7de38043（同源 point_0012）
  - E2E3/i2_seed_candB_methoxide_out.xyz = bc2477926f83aa4b25cf004b70b372c276fb8e41e2a425fef0f5e7c559b1b870（Na–O3 3.600，Na⁺ 脱离甲醇盐）
  - E2E3/i2_seed_candC_combined.xyz = 3cb504218c690d904a612b1f72e316c1e3056aa12ce921ab81c4184d40859dce
  - E2E3/i2_seed_candD_classB.xyz = 78448225332a095326025a2c3beaa891c287746889656f7cba6d83bd4856c840（Na–O1 2.528 / Na–O5 2.111，双齿甲酸根）
  - 索引/来源/provenance：E2E3/I2_BACKUP_SEEDS_PROVENANCE.md = b17f71ba9e818f32d3a89dba403aa9843ddff42a1de258b9bc909d1af26efa60
  - 道的换种子优先序（按静电与配位合理性）：**(b) candD 双齿甲酸根 → (a) 桥联 O3/O5（p11/p12/candA_xtbmin）→ (c) candB/candC（Na⁺ 离开甲氧基，带额外静电应变，失收敛风险最高）**。
- **readfc 备选修复（B′ 分支，优先于换构象）**：job 990 的频率作业就是在**同一几何**上做的，故 E2E3/freq_i2_candA/i2_candA_freq.chk（sha256 **343c0fd5576fdf3c491e98e1933e0a60b9cbd3582bb60f656a8c2521005b8f17**，4689920 B）内存有该几何的**解析 Hessian**。本轮**实测**：同目录 freq_i2_candA/freq_lastframe.xyz 与 E2E3/i2_min_candA.xyz 的 11 行「元素 + 坐标」**逐字相同**（程序内逐行比对）⇒ opt=(readfc,...) 要求「chk 几何 = 输入几何」成立。启用方式（仅在 job 1012 失败时）：复制该 chk → route 改 `#p opt=(readfc,maxcycles=200) freq b3lyp/def2svp empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=water)`，坐标块仍送同一 i2_min_candA 几何。**calcfc（job 1012）与 readfc 不得同时占配额**（道已提示，采纳）。
- 道的科学判定登记：i2_min_candA.xyz 的 **0 虚频（job 990；最低实频 21.69 cm⁻¹）站得住**，是 I2 极小值；三次 opt 的 l9999/NStep 是「力判据达标、位移判据不达标」的优化器记账问题，**不得**写成「I2 不存在」。
- 2026-10-17 07:4x（本轮）：新建本节；§15 的 B 分支细化为 **B′（readfc，优先）→ B（换构象，按道给出的优先序）**；B/B′ 若最终改用别的构象作反应物参考，**必须在交付里显式登记参考极小值构象改变及其对 ΔE‡ 参考的影响**。
- **道（small_mol）本轮补充的两条操作要点（evt_08a7fb472c6c4d50，采纳）**：① B′ 时必须把 E2E3/freq_i2_candA/i2_candA_freq.chk **复制**到新作业目录使用（原 chk 留作 job 990 的证据链，不移动/不共用），坐标块与 i2_min_candA.xyz 逐位相同，日志出现 `Reading force constants` 即表示 readfc 生效；② A 分支收敛几何可**直接复用**到 ts_0013 的 `conformers.product`（同一几何、同一 i2 序），只需替换 `xyz_path` 与 `evidence_refs`，**atom_map / reaction_center 不需重推**。③ 道的口径提醒：本包 I2 参考极小值（−466.986020418，0 虚频）对应「(a) Na⁺ 桥联 O3/O5」构象；若 B 分支改用 (b)/(c) 类构象，则 I2 端参考能量**必须整批重算**，不得与旧值混减，且 E2/E3 起点定义需同步改。
- **时间勘误（2026-10-17 07:44 实测 `date` = 2026-10-17 07:43:53 +0800 CST）**：本节与 §15/§16 早先写的「08:0x」是笔误，实际为 **07:4x**；hub 帖 evt_7f6c948088004108 与 evt_92e0b6d0afc74f72 中的「08:0x」同此更正。**只影响时间标注，不影响任何 sha256、行号、能量或结论。**

## 18 巡检记录（2026-10-17 08:01 +0800）
- **三边状态未变，本轮无新增 stage result.outcome**：ts_0007 rev 43 / refine / waiting job **1010**（frequency，ready）；ts_0013 rev 9 / build / waiting job **1011**（product_seed_opt，ready）；ts_0014 rev 8 / build / **blocked**（待按 A/B′/B 修订）。queue：running **999/1000/1008/1009**（均为他会话作业），queued **1010(1) / 1011(2) / 1012(3)**，free cpus = **0** ⇒ 正常排队；本包手工在飞 = **1**（job 1012）；未重复提交、未调 priority、未杀他人作业。
- **B′ 已预置（未提交）**：gold_finish_20261015/NY3/E2E3/i2_min_readfc_optfreq/ 下 i2_min_readfc.gjf（sha256 **d87d2480b9cd34b34af444f637bfc336c0ec8cdc4ded5ad74bc096495e383802**；route = `opt=(readfc,maxcycles=200) freq` + 同批方法，坐标块与 i2_min_candA.xyz 逐位相同）与 i2_min_readfc.chk（sha256 **343c0fd5576fdf3c491e98e1933e0a60b9cbd3582bb60f656a8c2521005b8f17**，本轮 sha256sum 实测 = job 990 原 chk 逐位副本）。仅当 job 1012 失败时按主协调 R13.2 预授权提交，且**不与 1012 并行**。
- **交付说明刷新**：DELIVERY_NOTES.md 现 sha256 **0d5eefdbc4afd5d12802f00bd209b13b7b99b2d16c5e918f35d29e6a631879fb**，前版 **778a4174e68a2ef3747079cb302c5e7c47ce9d1f08937d43a0b85b7554c7ce5b 已被取代**（前版仅作 07:2x 的暂时快照）；本版刷新 §4 逐边状态并新增 §5（E3 build 阻塞与 I2「未收敛帧」问题、A/B′/B 分支、P 端构象缺测 caveat）与 §6（xTB 索引消歧 + I2_DFT_VERDICT.md sha 勘误 + 时间勘误）。**仅影响该文件的 sha 与其 §4–§8 内容，不影响任何阶段证据、日志 sha256、行号或数值。**
- **主协调授权**：R13.2 已预先授权 B′（readfc）与 B（换构象），条件 = 手工在飞 ≤2 且顺序执行、priority 0、每步留证、走 B 时整批重算 I2 端参考能量并显式登记起点定义变化、A 与 B′ 均失败则一次性回报（hub 帖 evt_d8000ed0c0f64add）。

## 19 E1（ts_0007）frequency 段终态与判定：**甲基转子 pseudo-saddle，不是声明的 E1 TS**（2026-10-17 08:07–08:10）
- 管线态：ts_0007 **rev 47 / stage refine / status waiting**，waiting_for = job **1014**（purpose irc，ready）；管线 message 原文：`frequency job 1010 finished; IRC job 1014 submitted (both directions) from the same optimised geometry.`（⇒ 管线把该驻点当 TS 并自动推进 IRC）。
- **frequency 段（job 1010，stage status=done）证据**：日志 ts/ts_0007/jobs/declaration_0003/frequency/frequency.log，sha256 **17226935566369e38d474a5e14b077cc60a6d9d4684d5f1400d80392f03f9287**（本轮实测）；`******    1 imaginary frequencies (negative Signs) ******` @L760；`Frequencies --    -98.2487   46.2758   91.7059` @L769；**band 行 9 组 = 27 = 3N−6 模**（L769–913）；`1 imaginary frequencies ignored.` @L956；E(RB3LYP) = **−466.985305161** @L510（与 job 1004 的 ts_opt 值一致）；`Normal termination of Gaussian 16 at Sat Oct 17 08:07:34 2026` @L1491。`Low frequencies` 行首 −98.2843 @L758 **不是振动模**。
- **虚频模归属（本轮由日志 L772–783 位移块逐原子解析；工作序 1-based = 1 Na｜2 O1｜3 H6｜4 C2｜5 O3｜6 C4｜7 O5｜8-10 H(Me)｜11 H(C4)）**：模矢平方占比 —— **甲基 H8/H9/H10 = 99.49%**（|d| = 0.5833 / 0.5833 / 0.5700），**全部重原子合计 0.44%**，其中 **O1(atom 2) + C4(atom 6) = 0.01%**（C4 位移分量 0.0000）⇒ 该虚频是**甲基转动（rotor）模**，与声明的 E1 反应中心（成 O1–C4 / C4=O5 π 变化，1-based [[2,6],[6,7]]）**不符**。
- **判定（BRIEF §4/§9）**：job 1004 的驻点 = **甲基转子 pseudo-saddle**（其几何与 RC 的差异亦集中在甲基旋转 D(8,4,5,6) −60.4°→−120.9° 与羟基 H 旋转，E 比 RC 高 ≈0.79 kcal/mol）⇒ **E1 的 ΔE‡ 仍缺测，不回填任何数值**；本次结果与 job 987/997 的 l9999 **均不构成**「E1 无鞍点」证据。
- **平台观察（供主协调登记）**：管线 freq 门只判「恰 1 虚频」即推进 IRC，**未核对虚频模的原子组成与声明键对**；本次因此把甲基转子鞍点当 TS 提交了 IRC（job 1014）。与 HL1_E1 的 −67.99 cm⁻¹ 甲基转子案例同类，建议作平台行为项登记。
- **job 1014（IRC）处置**：不干预（无撤销工具；其结果为「该鞍点连接的端点」提供正面证据，成本小）。若 IRC 双向端点确为两个 RC 类构象，则进一步证明该驻点不是 E1 TS。
- **下一版 guess 计划（等 job 1014 终态、解除 active-job 封锁后执行）**：目标 = **O1–C4 加成通道内、保留 RC 旋转构象、d(O1···C4) ≈ 2.1–2.4 Å** 的初猜（2.806 / 2.503 Å 的帧都会滑向转子鞍点；IDPP img_05 = 2.086 Å 的帧漂到 I1 侧）。路线 ①：用管线自身的 **scan 型 guess**（管线跑扫描取帧，不占手工配额）；路线 ②：由 small_mol 道用**受约束扫描 / 固定 d(O1–C4) 预优化**产出候选几何 + provenance（手工 ≤1 个、priority 0、8c/10240MB），再由我 ts_resume 绑定。两条路线并行准备，先到先用。

## 21 E1 几何准备（道中间回报 evt_8f1ecf480ae249d5；本轮 sha256sum 逐项核对通过）与配额裁定
- 道实测表（工作序 1 Na｜2 O1｜3 H6｜4 C2｜5 O3｜6 C4｜7 O5｜8-10 H(Me)｜11 H(C4)；BD 角定义 = ∠O1–C4–O5）：
  - RC（job 967 工作序副本）E1/rc_dft_min_working_order.xyz = **449cad42aa779d00dd0f454c5b0eb93a9b4bdb771d6de8772cf9912aa7adef68**：d(O1···C4) **2.803**｜C4–O3 1.329｜C4=O5 1.222｜O1–H6 0.965｜Na–O1 2.093｜Na–O5 2.409｜BD **96.1°**｜D(8,4,5,6) **−60.4°**｜D(1,2,3,11) **−152.4°**
  - IDPP 帧：img_03（0ece3b21bf249368bf5b3a929bf0abced81a6d1ba7703cc17f01b751affde789）2.361 Å、BD 109.1°、D_Me −33.4°、D_OH −99.8°；img_04（44b4495200a345189e1402fe600332465b60ef741f6620bab99458fa9d7496fb）2.230 Å、BD 110.3°、D_Me −19.3°、D_OH −97.4°；img_05（fecd47be40ed93445b1778b74fe63a84670fda0b428b88d6b4e5674094b64afb）2.086 Å、BD 109.9°、D_Me +3.9°、D_OH −94.8°；img_00 = RC（8b742630886e69dd010720a88cf5bf077610971f032a111314fec568c57c59b4）
  - job 1004 起点帧 E1/guess_scan_p04_d2503.xyz = 2a9bb8506de69d5cd20a1e90371868d8edb6f482013c0447811219157bc66e22（与 §5 记录一致）：2.503 Å、BD 96.1°、**D_Me −60.6°（≈RC）**、**D_OH +179.5°（≠RC）**
- 判读（采录，非「无鞍点」证据）：IDPP 帧在缩短 O1···C4 的同时把甲基转过 +27/+41/+64°、羟基 H 转过 ≈+53~58° ⇒ 2.1–2.4 Å 区间内 IDPP 帧已不在 RC 的旋转构象盆地；job 1004 起点保住甲基但羟基翻转仍收敛到 −98.25 cm⁻¹ 转子鞍点 ⇒ **「保住甲基」不是充分条件**，需**同时**把两个软二面角压在 RC 附近并让 d(O1···C4) 落进 2.1–2.4 Å。
- 路线 ① job 1015 = 从 RC 出发的受约束 **GFN2-xTB/ALPB(water)** 松弛扫描：manifest E1/e1_xtb_scan/scan_e1_manifest.json = **3e94d59a2a1fc37c9636b22284b6c3d33faba470c72a02362bc6ac8d85383625**（scan bond 原子 **0-based [1,5]** = O1/C4，2.55→1.90 Å，14 点；reactant_xyz = RC），排队中（chem_task，不占手工配额）。
- **配额裁定（我）**：准许道在 job 1015 落定后，**仅当 1015 帧无法同时满足「d(O1···C4) 2.1–2.4 Å + D_Me、D_OH 均接近 RC」** 时，新增 **≤1 个手工作业**（固定 d(O1–C4) 且同时固定 D(8,4,5,6) 与 D(1,2,3,11) 的预优化）；条件 = priority 0、≤8c/≤10240MB、与 1015 **顺序执行不并行**、留原始日志 + sha256 + 行号 + provenance、不碰 ts/、不改 registry/生成器；本包手工在飞合计 ≤2（当前 1 = job 1012）。
- 口径更正采录：BD 角 = ∠O1–C4–O5（此前 §5 记录里引用的 123.4° 是 ∠O3–C4–O5）。
- **job 1012 观察（时刻记录、非证据）**：08:14:43 已到 **Step 38 / 上限 100**（日志 sha256 62961cefb567966fe642e54df6364c3c53b5407b660d100c70a25439acef889e），末两条 SCF = −466.984784293 / −466.985773862 ⇒ 出现回摆（比最低点高 ≈0.8 kcal/mol），形态与 job 1007/1011 的漂移相似；若至 100 步仍不收敛即按预授权走 **B′（readfc）**。

## 22 E1 择优阈值确认 + job 1012 漂移加深（2026-10-17 08:16）
- 道（evt_ae7b48f34db74a0d）提出并请我确认的**选帧口径（我确认采纳；是择优口径、不是物理判据）**：硬性 = d(O1···C4) ∈ **2.10–2.40 Å**；|ΔD_Me(8,4,5,6)| ≤ **10°**（RC = −60.4°）**且** |ΔD_OH(1,2,3,11)| ≤ **15°**（RC = −152.4°）**两个同时满足**；Na–O1 ≤ **2.60 Å** 且 |Δ∠Na–O1–H6| ≤ **25°**（RC 145.4°）。参考项 = BD∠O1–C4–O5 ∈ 100–115°（RC 96.1°）。依据 = 实测：job 1004 起点帧保住甲基（−60.6°）但羟基漂到 +179.5° 仍收敛到甲基转子鞍点；IDPP 帧两个软二面角同时漂移 ⇒ 只保甲基已被证伪为充分条件。
- 道并行做**零资源**的「绕 Na⁺ 刚性摆动 O1–H6 片段」候选族（保持 Na–O1 2.093 / Na–O5 2.409 / O1–H6 0.965 / ∠Na–O1–H6 145.4°，d(O1···C4) 由 2.803 收到 2.40/2.30/2.20 Å；**甲基与羟基二面角与 RC 逐位相同**）；声明为**仅几何初猜、能量不作能垒证据**，若 BD 掉出 100–115° 会如实标注。
- **job 1012 漂移加深（时刻记录、非证据）**：08:16:00 已到 **Step 55 / 上限 100**（日志 sha256 7c313531459868d566a79b9f7a6b0c99e1989c277d6fb43e6f9d8606347de7ef）；最新判据 **Max Force 0.033447 NO / RMS 0.006088 NO / Max Disp 0.029555 NO / RMS 0.012769 NO**，末两条 SCF = −466.985871255 / −466.985365115 ⇒ 未向极小值收敛（反而离开最低点），与 job 1007/1011 的漂移同型。
- 预判与计划：若 1012 到 100 步仍无 Stationary point（很可能）⇒ 立即提交 **B′（readfc；输入已预置 E2E3/i2_min_readfc_optfreq/i2_min_readfc.gjf sha d87d2480…，chk 副本 sha 343c0fd5…）**；B′ 仍不收敛 ⇒ **B（换构象：candD → p11/p12 → candB/candC）**，整批重算 I2 端参考能量并显式登记起点定义变化。两条均按 R13.2 预授权执行：顺序不并行、priority 0、≤8c/≤10240MB、每步留证。

## 23 A 分支（job 1012 calcfc）**失败** ⇒ 已提交 B′（job 1016 readfc）；并登记道的 3 个 E1 候选初猜（2026-10-17 08:19–08:22）
- **job 1012 终态证据（本轮实测）**：日志 E2E3/i2_min_conv_optfreq/i2_min_conv.log，**最终** sha256 **219d728089ce45e2be2d4d26a8e5d348d01b2d6a2e49265816322d48fe15443e**（此前 §21/§22 引用的 62961cef… / 7c313531… 是运行中的中间版本，**已被本值取代**）；`Step number 100 out of a maximum of  100` @L44013；`-- Number of steps exceeded,  NStep= 100` @L44075；`Error termination via Lnk1e in /home/ly/g16/l9999.exe at Sat Oct 17 08:19:32 2026` @L44305；末次收敛表 Max Force 0.013017 NO / RMS 0.002370 NO / Max Disp 0.033467 NO / RMS 0.013825 NO（@L44069–44072）；末两条 SCF = −466.985385040 / −466.985895772；**无频率段**（Frequencies -- 计数 = 0）。⇒ A 分支（calcfc + maxcycles=200）未能得到收敛的 I2 极小值；技术性失败，不作机理证据。
- **已提交 B′（预授权分支，job 1016）**：输入 gold_finish_20261015/NY3/E2E3/i2_min_readfc_optfreq/i2_min_readfc.gjf（sha256 **d87d2480b9cd34b34af444f637bfc336c0ec8cdc4ded5ad74bc096495e383802**），chk = 同目录 i2_min_readfc.chk（sha256 343c0fd5576fdf3c491e98e1933e0a60b9cbd3582bb60f656a8c2521005b8f17 = job 990 原 chk 逐位副本），route = opt=(readfc,maxcycles=200) freq + 同批方法；cpus 8 / memory_mb 10240 / **priority 0** / 异步；提交时刻 08:20 前后，状态 ready。
- **技术预判（供下一步决策）**：B′ 的 readfc 与 A 的 calcfc 在数学上取自**同一解析初始 Hessian**（job 990 的 freq 就是在该几何上算的）⇒ 若 A 因「力判据反复达标/位移判据不达标」的软模抖动而失败，B′ 也**可能同样失败**。因此若 B′ 再失败，我将**直接进入 B（换构象）**：用 E2E3/i2_seed_xtb_na3_p11.xyz（10177bfa…）或 i2_seed_candD_classB.xyz（78448225…）作 conformers 种子（Na⁺ 三配位/双齿甲酸根，软模更少、更易收敛），并对两个 run 各做一次 ts_resume；同时**整批重算 I2 端参考能量**并在交付显式登记「参考极小值构象改变」及其对 ΔE‡ 参考的影响（R13.2 条件④）。
- **道的 E1 候选初猜（本轮 sha256sum 实测逐位一致）**：E1/e1_tsguess_rigid_swing_d230.xyz = **523392c1735a83f670566401e3e18a51387b13899d254fb3c4aceabc82ff6e36**（d(O1···C4) 2.300、Na–O1 2.093、D_Me −60.4°(Δ0.0)、D_OH −156.5°(Δ4.1)、BD 98.5°、∠Na-O1-H6 145.4°(Δ0.0) ⇒ ①②③全过，BD 低 1.5°）；E1/e1_tsguess_rigid_swing_d220.xyz = **95b766605cd12732924e1b39fe446017b36a71aa83da7a9eec629ed0f2d69877**（2.200 / 2.093 / −60.4 / −157.3(Δ4.9) / 98.8 / 145.4 ⇒ ①②③全过）；E1/e1_tsguess_img04_retorsion.xyz = **3af1c8c22961c181dec377b735d12dc102c4dae035a112065bc27a4861a6d98a**（2.230 / 2.732 / −60.4 / −152.4 / BD 110.3 / ∠Na-O1-H6 102.9（Δ42.5）⇒ ③不过）；工具别名 e1_tsguess_img04_retorsion_tool.xyz = 2a03d85bf258aff509c67156b743274e59f0e9be434c6167db7c54a92eecfcae；provenance E1/TS_E1_GUESS_CANDIDATES_PROVENANCE.md = **2292b7cab3eb31c872ce7e926d1ab22e156fa0b5daed4ecc5d8ae36d422a8321**。
- **选择倾向（待 1015 帧落定后决定）**：优先 **job 1015 的原生松弛帧**（受约束 GFN2 扫描，provenance 来自 compute record）；若 1015 帧全部不达标，则用 **rigid_swing_d230**（①②③全过、离判据最近）作 provided guess（注意其坐标为会话内刚体旋转机器生成、平台可能给 "suspected handwritten coordinates" 提示且无 compute record），并按已批配额决定是否追加 ≤1 个固定 d + 固定两个软二面角的预优化。
- 纪律：三帧均**仅几何初猜**（无 SCF/无梯度/无频率），不引用任何能量；E1 的 ΔE‡ 仍缺测。

## 20 E2（ts_0013）product_seed_opt 亦失败（同款）与统一修复（2026-10-17 08:11）
- 管线态：ts_0013 **rev 9 → 12 / stage build / status blocked**；`failure_class = conformer_optimization_failed`，`message = "product_seed_opt job 1011 failed; revise or retry through ts_resume."`，`needs = ["conformers.product"]`；`failed_attempt`：job_id 1011、input_path ts/ts_0013/jobs/declaration_0001/product_seed_opt/seed-opt.gjf、**input_sha256 a408d306cfa7e242cd3ab41b5041850571671c4ca207936d646d1974c03164d3（与 ts_0014 的 job 1007 输入逐位相同）**、log_sha256 **83723dbcc8af9a215a054cae193d5be396c27805f13d59464c1421df6962144a**。
- 终止原文（与 job 1007 同款）：`-- Number of steps exceeded,  NStep=  42` @L18771；`Error termination via Lnk1e in /home/ly/g16/l9999.exe at Sat Oct 17 08:11:15 2026` @L19008；末次收敛表 Maximum Force 0.011310（NO）/ RMS 0.004047（NO）/ Max Disp 0.689431 / RMS 0.294005；中间曾出现「力判据 YES、位移判据 NO」（@L18310–18313，Max Force 0.000109 / RMS 0.000037 / Max Disp 0.448356）。⇒ 与 §15 同因：起点是「力判据达标、从未判定收敛」的近极小值帧。
- **纪律**：同为技术性失败，**不作机理证据**。
- **统一修复（两个 run 共用同一收敛几何）**：E2 的 `conformers.product` 与 E3 的 `conformers.reactant` 是同一种物种、同一 i2 序、且 job 1007/1011 的输入逐位相同 ⇒ 一旦得到**收敛的 I2 极小值**（job 1012 的 A 分支，或 B′ 的 readfc 结果），就对**两个 run 各做一次 ts_resume**：
  - ts_0014：`changes={conformers:{reactant:{kind:"file", xyz_path:<收敛几何>, mol_path:<同一 I2 mol /prep/build/art_I2_src/assembly/complex_candidate_000.mol>, evidence_refs:[<provenance>], optimization:{ref:"g16"}, heavy_atom_binding:{indices:[1,2,3,7,8,9]}}}}`
  - ts_0013：同上但键名为 `conformers.product`（atom_map / reaction_center 不需重推）
- **job 1012 进展（仅作时刻记录，非证据）**：已 **running**（08:11:23 起）；日志 E2E3/i2_min_conv_optfreq/i2_min_conv.log 现 sha256 48249ee99300438527b1566e5ff39964f8fd73470a43add36fe6d3545e28a414；calcfc 生效（`Force constants in Cartesian coordinates:` @L826）；已到 Step 6 / 最大 100（L3198）；最近一次判据 Max Force 0.000013 YES / RMS 0.000005 YES / Max Disp 0.140399 NO / RMS Disp 0.064082 NO ⇒ 力判据已达标、位移判据在收敛中（对比失败 run 的末值 0.67/0.29，明显改善）。
- 队列（08:12）：running **999/1008/1009/1012**；queued **1013(1)/1014(2)/1015(3)**；free cpus = 0；本包手工在飞 = 1（job 1012，priority 0、8c/10240MB）。

## 24 R20.1 轮（2026-10-17 08:4x CST）：ts_0007 换 guess 由他 lane 完成（本会话零写入）；job 1016 运行中；1015 十四帧本会话独立复测 = 0/14

### 24.1 防重复动作核对（本轮 ts_inspect 实测）
- 主协调 R20.1（帖 evt_d62a2159022145b9）称 ts_0007 的换 guess 已由 session as_a0ffef5393594045 完成（rev 50→57）；**本会话已撤回 R20 第 5 点的换 guess 计划，且对 ts_0007 未做任何 ts_resume（零写入）**。
- 本轮 `ts_inspect(ts_0007)` 实测：rev **57** / stage **refine** / status **waiting** / blocked=null / waiting_for = job **1018**（`ts/ts_0007/jobs/declaration_0004/ts_opt/refine.gjf`，8c/10000MB，state=ready，attempt 1，source_input_revision 4）。
- 新 guess（主协调同轮实测，与本包记账一致）：`gold_finish_20261015/NY3/E1/interp/img_04.xyz` sha256 `44b4495200a345189e1402fe600332465b60ef741f6620bab99458fa9d7496fb`；provenance `E1/E1_GUESS_V2_PROVENANCE.md` sha256 `97c422d592b662475cd28a1121a50b9b5ed1fed23c86ba6ed4f2575eb91ecf97`。
- ts_0013 rev 12 / build / blocked（needs conformers.product）、ts_0014 rev 8 / build / blocked（needs conformers.reactant）本轮未变。
- 队列（本轮 query_compute_queue 实测，node-local 32c/51200MB）：in_flight slots 4 / cpus 32 / memory 38912MB；free cpus **0**、free memory 12288MB、free slots 6 ⇒ 新作业只能排队（与 R20.1 第 3 点一致；不重复提交、不改 priority、不杀他人作业）。

### 24.2 job 1016（B′ readfc）：running
- state=**running**，started_at `2026-10-17T08:34:12+08:00`；gjf `gold_finish_20261015/NY3/E2E3/i2_min_readfc_optfreq/i2_min_readfc.gjf`；gjf sha256 `d87d2480b9cd34b34af444f637bfc336c0ec8cdc4ded5ad74bc096495e383802`。
- **原生读入行（逐字，本节路径已勘误）**：job 1016 的真实 Gaussian 输出是 `E2E3/i2_min_readfc_optfreq/i2_min_readfc.log`；`.cloudra/calc-1016.out.log` 只是 83 B 的启动器存根（唯一内容 `[calculator] isolated GAUSS_SCRDIR=...`）。**24.2a 勘误**：§24.2 初版把 ReadFC 行记在存根路径名下，属**路径/文件名标注错误**（数字与结论不变）。
- **ReadFC 生效的判据（逐字原生行）**：`No redundant coordinates on chk file, so ReadFC converted to ReadCartesianFC.` @L165（日志 route 回显 @L87 与输入一致）。**注意：`Reading force constants` 这一字样在本日志中实测不存在**（grep 无匹配），也没有 `Force constants in Cartesian coordinates:` 行（job 1012 的 calcfc 日志有 @L826）⇒ 后续引用只用 L165 这一条。
- **几何前提本轮复测成立**：`i2_min_readfc.gjf` 的 11 原子坐标与登记 I2 极小值 `E2E3/i2_min_candA.xyz` **逐原子差 0.000000 Å**（同元素序 Na,C,O,H,H,H,C,O,O,H,H。
- **新风险观察（时刻记录、非证据）**：route 请求 `maxcycles=200`（Link1 旗标 `1/6=200`、L87 回显均生效），但优化器自第 1 步起就打印 `Step number N out of a maximum of 100`（@L735 = Step 1/100）；job 1012 同样在 100 步被截断（NStep=100 + l9999）⇒ **B′ 实际只有 100 步预算**（机制未查清，建议按平台行为项登记）。截至 08:41:46 日志（sha256 `572380fb9b8c764f87475a1911081b2d65d79f661c8f6c509006cbb8e7d7bbd9`）已 Step **90/100**（@L39242），最后判据块 @L39297：Max Force 0.013265 NO / RMS Force 0.002429 NO / Max Disp 0.030493 NO（与 job 1012 同型振荡）；读入 Hessian 的最小本征值 ≈ 0.00007 ⇒ 极软模主导，位移判据难收敛。**若 100 步前无 `Stationary point found` 即按预授权走 B（换构象）**。
- 前序快照（08:40，仅时刻记录）：sha256 `70d495594337b81a91d92e7180872baa07d95c2da4b9cce7174d463259c73fd1`（34015 行，Step 77/100）。

### 24.3 1015 十四帧本会话独立复测（记录/备用口径；与道帖 evt_48ca2002dc3d4b58 逐点一致）
- RC 参考 `E1/rc_dft_min_working_order.xyz`（工作序 Na,O1,H6,C2,O3,C4,O5,H,H,H,H；0-based 度量 = d(1,5) 即 O1···C4、angle(0,1,2) 即 ∠Na-O1-H6、dih(7,3,4,5) 即 D_Me、dih(0,1,2,10) 即 D_OH、angle(1,5,6) 即 BD）：d(O1···C4) 2.803、Na–O1 2.093、Na–O5 2.409、D_Me -60.35、D_OH -152.44、∠Na-O1-H6 145.38、BD 96.06。
- 复测脚本（本会话新建）：`gold_finish_20261015/NY3/coord_measure_e1_frames.py` sha256 `1b18914add49929a7c83e45e3eb51c0a07540fded48efe6f05ded266d24355c5`。
- 逐帧（原生 `E1/e1_xtb_scan/native_scan_runs/native_scan_0001/point_0001..0014.xyz`；Δ 相对 RC；① = d∈2.10-2.40 Å，② = |ΔD_Me|≤10° 且 |ΔD_OH|≤15°，③ = Na–O1≤2.60 Å 且 |Δ∠Na-O1-H6|≤25°）：

| frame | d(O1···C4) | Na–O1 | D_Me(Δ) | D_OH(Δ) | ∠Na-O1-H6(Δ) | BD | ① | ② | ③ |
|---|---|---|---|---|---|---|---|---|---|
| p0001 | 2.558 | 1.915 | -59.95 (+0.4) | 179.55 (+332.0*) | 148.27 (+2.9) | 84.1 | n | n | Y |
| p0002 | 2.495 | 1.890 | -72.90 (-12.5) | -148.74 (+3.7) | 168.66 (+23.3) | 90.2 | n | n | Y |
| p0003 | 2.445 | 1.894 | -72.34 (-12.0) | -149.25 (+3.2) | 171.04 (+25.7) | 91.5 | n | n | n |
| p0004 | 2.394 | 1.894 | -72.00 (-11.6) | -150.57 (+1.9) | 172.81 (+27.4) | 92.6 | Y | n | n |
| p0005 | 2.343 | 1.896 | -71.78 (-11.4) | -148.32 (+4.1) | 173.07 (+27.7) | 93.5 | Y | n | n |
| p0006 | 2.292 | 1.900 | -71.64 (-11.3) | -153.14 (-0.7) | 175.06 (+29.7) | 94.7 | Y | n | n |
| p0007 | 2.241 | 1.902 | -71.39 (-11.0) | -154.43 (-2.0) | 175.25 (+29.9) | 95.7 | Y | n | n |
| p0008 | 2.191 | 1.906 | -71.15 (-10.8) | -159.45 (-7.0) | 175.80 (+30.4) | 96.7 | Y | n | n |
| p0009 | 2.140 | 1.911 | -70.85 (-10.5) | -168.45 (-16.0) | 176.02 (+30.6) | 97.8 | Y | n | n |
| p0010 | 2.089 | 1.917 | -70.55 (-10.2) | -175.40 (-23.0) | 176.12 (+30.7) | 98.8 | n | n | n |
| p0011 | 2.038 | 1.922 | -70.19 (-9.8) | -177.10 (-24.7) | 175.80 (+30.4) | 99.8 | n | n | n |
| p0012 | 1.988 | 1.928 | -69.86 (-9.5) | -178.16 (-25.7) | 175.46 (+30.1) | 100.8 | n | n | n |
| p0013 | 1.937 | 1.939 | -69.56 (-9.2) | -179.56 (-27.1) | 175.07 (+29.7) | 101.7 | n | n | n |
| p0014 | 1.887 | 1.950 | -69.35 (-9.0) | -179.02 (-26.6) | 174.47 (+29.1) | 102.7 | n | n | n |

- * p0001 的 D_OH 跨 ±180° 环绕，等价 Δ ≈ -27.6°（不是 +332° 的物理变化）。
- **结论：三条硬判据 0/14 通过**：① 由 p0004-p0009 满足（2.14-2.39 Å）；③ 的 Na–O1 距离项 14/14 满足（1.89-1.95 Å），但角度项自 p0002 起 Δ=+23.3~+30.7° 越界；② 的 D_Me 自 p0002 起 Δ=-9.0~-12.5° 越界 ⇒ 与本会话此前记录、与道帖、与平台 scan_parse 判读（无内部极大、无候选）一致。
- 同口径复测的候选初猜读数（不改其文件）：`E1/e1_tsguess_rigid_swing_d230.xyz` d 2.300 / Na–O1 2.093 / ΔD_Me 0.0 / ΔD_OH -4.0 / BD 98.5 / Δ∠Na-O1-H6 0.0 ⇒ ①②③ 全过；`_d220.xyz` 2.200/2.093/0.0/-4.9/98.8/0.0 ⇒ 全过；`e1_tsguess_img04_retorsion.xyz` 2.230/**2.732**/0.0/0.0/110.3/-42.4 ⇒ ③不过；`E1/interp/img_04.xyz` 2.230/**2.732**/**+41.1**/**+55.0**/110.3/-42.4 ⇒ ②③ 均不过。

### 24.4 登记一条待裁决观察（本会话未动手）
- job 1018 当前所用 guess 是**原始 IDPP 插值帧** `E1/interp/img_04.xyz`：按 §21 确认的硬判据，它 ②（ΔD_Me +41.1°、ΔD_OH +55.0°）与 ③（Na–O1 2.732 Å > 2.60 Å）**均不过**；同包 `e1_tsguess_rigid_swing_d230/d220.xyz` ①②③ **全过**（BD 98.5/98.8° 略低于 100-115° 参考带）。已按 R20.1 要求**不对 ts_0007 做任何写入**，是否改 guess 由主协调/该 lane 决定。

### 24.5 仍缺测（不填补）
- E1 的 ΔE‡（现无任何合规 TS：job 1004/1010 的驻点 = 甲基转子 pseudo-saddle；job 989 剖面按 §4 订正值仅 4 点收敛）；E1 是否存在独立一阶鞍点；E1 的 IRC 连通性（job 1014 l123 失败只是失败记录，**不是**无鞍点证据）。E2、E3 的 ΔE‡ 仍因 build 阻塞缺测。回填仍 **0/3**。

## 25 R21 轮（2026-10-17 08:42–09:0x CST）：B′ 终态失败（l9999 @100 步）⇒ 已按 R21 预授权执行 B（换构象 candD）；并登记新的「平缓 PES 收敛」诊断

### 25.1 job 1016（B′ readfc）终态：failed
- 终态日志 `gold_finish_20261015/NY3/E2E3/i2_min_readfc_optfreq/i2_min_readfc.log` sha256 **79191906fcd801367453e702d91d1bc5d982bd4ab9cc619120b11497a696882b**：`-- Number of steps exceeded,  NStep= 100` @L43634；`Error termination request processed by link 9999.` @L43864；`Error termination via Lnk1e in /home/ly/g16/l9999.exe at Sat Oct 17 08:42:15 2026` @L43865。ReadFC 生效行 @L165（逐字见 §24.2a）。⇒ **B′ 路线证伪**；本会话 08:41:46 快照 572380fb… 已被取代（主协调同轮复核亦为 79191906…）。

### 25.2 R21 裁决登记（主协调帖）
- **批准立即走 B**（换构象）：种子优先序 candD → p11/p12；ts_0014（conformers.reactant）与 ts_0013（conformers.product）各一次 ts_resume；整批重算 I2 端参考能量；显式登记起点极小值构象改变、新旧不混减。
- **job 1018（NY3_E1 第 4 版）维持 img_04，不叠加第二次 ts_resume**（避免让已排队的 1018 在满载节点上执行被取代的输入）；终态后按失败模式选备选 guess：落甲基扭转 pseudo-saddle 或滑落 ⇒ `e1_tsguess_rigid_swing_d230.xyz`（sha 523392c1735a83f670566401e3e18a51387b13899d254fb3c4aceabc82ff6e36，三判据全过；绑定前须在帖里说明该几何为会话内机器生成、无 compute record、平台可能标 suspected handwritten coordinates）；朝 I1 侧滑落 ⇒ `E1/interp/img_03.xyz`（2.361 Å）；两者均失败 ⇒ 反向弛豫扫描 d(C4–O1) 1.43→3.0 Å 夹逼脊线（**手工扫描，提交前先报主协调**）。
- maxcycles 缺陷由**主协调统一提 issue #191**（正文 `gold_finish_20261015/ISSUE_191_MAXCYCLES_STEP_CAP.md` sha256 7dcd8a5cf11ad4c639ae25d5c928eeef055c8aafc2c67a03df20755efcbba3ce）；本会话只做只读取证，§24.2 的四条读数即该取证（未重提 issue）。
- 1015 十四帧复测 0/14 = 证伪材料（§24.3）。

### 25.3 B 分支执行（本轮两次 ts_resume 均成功）
- 共用输入：xyz `gold_finish_20261015/NY3/E2E3/i2_seed_candD_classB.xyz` sha256 **78448225332a095326025a2c3beaa891c287746889656f7cba6d83bd4856c840**（GFN2-xTB/ALPB(water) 极小值：Na⁺ 螯合甲酸根 O1/O5、甲氧基远离，Na–O1 2.528 / Na–O5 2.111 / Na···O3 3.300 / O1···O3 4.996 Å；文件序 = prep/i2 序）；mol `prep/build/art_I2_src/assembly/complex_candidate_000.mol` sha256 **af67740f8c76f18f0517573c8cb5590aa8bb603d3d1c706df624ebd1ce46f816**；`heavy_atom_binding = [1,2,3,7,8,9]`（本文件序下的重原子位次）；`optimization = {ref: g16}`；未重推 atom_map / reaction_center。
- evidence_refs（均为本轮实测存在的 artifact）：`E2E3/I2_BACKUP_SEEDS_PROVENANCE.md` sha256 b17f71ba9e818f32d3a89dba403aa9843ddff42a1de258b9bc909d1af26efa60；`E2E3/I2_DFT_VERDICT.md` sha256 3e8859fb09753b35c7eb596214ebe20d23932b9525bcbe3e85d41a7c6e1e5fa3；`E2E3/I2_SEED_NOTE.md` sha256 c1fb933fe4e66b9636a31599fed23a52c78991a3b28884d8326482faf20ed925。
- **ts_0014（E3）receipt**：rev **8 → 12**、stage build、status **waiting**、declaration_0002、waiting_for = job **1019**（candidate_opt，8c/10240MB，ready）；新 reactant 结构 `build/input_0002/reactant/seed.xyz` sha256 78448225…（= candD 原坐标）、mol sha af67740f…。**实测 job 1019 输入坐标 = candD 逐位相同** ⇒ E3 的 I2 端起点已换构象。
- **ts_0013（E2）receipt**：rev **12 → 16**、stage build、status **waiting**、declaration_0002、waiting_for = job **1020**（candidate_opt，8c/10240MB，ready）；`ts/ts_0013/process.json` 已含 candD sha ⇒ product 构象登记成功；**实测 job 1020 输入仍是 E2 反应物（I1，opt step=32 几何）** ⇒ declaration_0002 先重跑 reactant opt，**product_seed_opt（用 candD）排在其后**；reactant 文件 `input_0002/reactant/seed.xyz` sha256 b7e835859f231194f6b3a967d44d53861c9dc8b971769c5e79fe08a8ff97b7eb（与 input_0001 坐标逐位相同，仅文件重写改变 sha）。
- 手工配额：本轮**未新开任何手工作业**（1012/1016 均已 failed 终止 ⇒ 本包手工在飞 = 0）；pipeline 的 1019/1020 不占手工配额。

### 25.4 新诊断：I2 端起点是「梯度已收敛、位移判据达不到」的极平缓极小值
- pipeline build opt 的历史失败（job **1007** = ts_0014 candidate_opt、job **1011** = ts_0013 product_seed_opt；两者输入逐位相同 sha256 a408d306…）**Step 1** 判据即 `Maximum Force 0.000221 YES / RMS Force 0.000060 YES / Maximum Displacement 0.021015 NO / RMS Displacement 0.010184 NO`（@L776–779，两日志同值），此后 42 步位移判据始终不达 ⇒ `NStep= 42` + l9999（07:39:17 / 08:11:15）。
- job 1016（readfc，同一几何）Step 1 判据 = `0.000221 YES / 0.000060 YES / 0.168687 NO / 0.069831 NO`（@L789–792；读入 chk 的 Hessian 给出更大步长），100 步后 l9999 ⇒ 与 A 分支同型。
- job 990（freq，同一几何）自身 `Forces (Hartrees/Bohr)` @L1055、判据 @L1264 = `Maximum Force 0.000194 YES` ⇒ 该几何**已是梯度平稳点**（这也是 job 990 报 0 虚频、被登记为 I2 极小值的依据）。
- route 对比：pipeline build opt = `opt b3lyp/def2svp empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=water)`（@L85–86），与本 run 计划中的 ts_opt/freq 方法字段（`methods` 实测）**同法同溶剂同泛函** ⇒ **不存在方法/溶剂层级不一致**。
- 诊断结论（技术诊断，非机理结论）：失败模式 = **极平缓 PES（Na⁺ 配位 + 甲基转动软模）下位移判据在步数预算内达不到**，与是否存在该中间体无关；因此 B（换构象）**有再次撞同一面墙的风险**。若 declaration_0002 的 build opt 再以同型签名失败（Step 1 力判据 YES、位移判据 NO、NStep 上限处 l9999），应把对策从「换构象」升级为「换收敛策略」，可选用：(i) 在包外把 candD 预先优化到**四项判据全 YES**，再以收敛几何作为 conformer 文件交给 pipeline（build opt 起步即收敛）；(ii) 申请 build opt 的 maxstep/maxcycles 控制（与 issue #191 同族）。**两项都需先报主协调**（(i) 涉及手工作业与包外几何，(ii) 属平台能力）。

### 25.5 「起点极小值构象改变」的显式登记（对 ΔE‡ 参考定义的影响）
- 变更：I2 端起点极小值构象由 **candA 型（Na⁺ 桥接甲氧基 O 与甲酸根 O；job 990 = i2_min_candA.xyz）** 改为 **candD_classB 型（Na⁺ 螯合甲酸根 O1/O5、甲氧基远离）**；**物种不变**（仍是分立的 Na⁺·甲酸根 / 甲氧基离子对），变的是 Na⁺ 配位与甲氧基位置。
- 影响：**E3（ts_0014）的 ΔE‡ 参考极小值定义随之改变** ⇒ 旧 I2 参考能量 −466.986020418（job 990 = `E2E3/freq_i2_candA/i2_candA_freq.log` 的 `SCF Done` **@L512**，本轮实测；同一数值亦见于 `E2E3/i2_candA_optfreq.log` 的最终帧 @**L21720**，而该日志 @**L21269** 的 −466.986020551 是中间帧 ⇒ 引用必须写清「哪个日志 + 行号」）**不得**与新的 I2 端数值相减；E3 的新 ΔE‡ 必须整体以 declaration_0002 的 I2 端极小值为参考。**新参考极小值待 job 1019（及 ts_0013 后续 product 段）收敛后按 §4 格式补登记**（job / 绝对路径 / sha256 / 0 虚频）。**E2（ts_0013）的 ΔE‡ 参考 = I1，不变**（I2 只是它的产物端）。
- 回填仍 **0/3**；E1 的 ΔE‡、E1 是否独立一阶鞍点、三边 IRC 连通性仍缺测。

## 26 道交付登记（2026-10-17 09:1x CST）：E1 升级候选附页 + E1_GUESS_V2_PROVENANCE.md §3 勘误 + DFT/xTB 方向张力

### 26.1 新增书面材料（道 small_mol；本轮 sha256sum 逐项实测通过）
- `E1/TS_E1_ESCALATION_CANDIDATES_APPENDIX.md` sha256 **c11f965e00c2583b390bd6d61716c59e0c21d247ed8d09b594e8de35f5c14bc9**（实测存在，可作后续 ts_resume 的 evidence_refs）。
  - §A `e1_tsguess_rigid_swing_d230.xyz`（sha 523392c1735a83f670566401e3e18a51387b13899d254fb3c4aceabc82ff6e36）：构造参数完整（源 RC sha 449cad42…；刚体摆动轴 = Na–O1–C4 面法向过 Na；r1 2.093 / r2 2.931；Δθ 14.12°；其余 9 原子冻结）；三判据全过（d 2.300｜Na–O1 2.093｜∠Na-O1-H6 145.4（Δ0.0）｜D_Me −60.4（Δ0.0）｜D_OH −156.5（Δ+4.1）｜BD 98.5，低 1.5°）。
  - **compute-record 说明（关键，引用时必须带）**：d230 由会话内刚体旋转代码**机器生成**、**无 compute record**，平台写入时可能标 suspected handwritten coordinates ⇒ **只能作 provided guess，不能充当 DAG 证据**；E1 的正式证据必须来自管线以它为起点的 TS Opt+Freq 原生日志。若评审要求坐标可追溯到工具，改用 `e1_tsguess_img04_retorsion.xyz`（sha 3af1c8c2…，有 operations_applied 回执）或 IDPP 帧。
  - §B `E1/interp/img_03.xyz`（sha **0ece3b21bf249368bf5b3a929bf0abced81a6d1ba7703cc17f01b751affde789**）：IDPP 第 3 帧（两端点 job 967 RC / job 985 I1）；读数 d 2.361｜Na–O1 2.567｜∠Na-O1-H6 113.3（Δ−32.1）｜D_Me −33.4（Δ+27.0）｜D_OH −99.8（Δ+52.6）｜BD 109.1 ⇒ **仅 BD 达标，② ③ 均不过**。IDPP 不含能量、端点能量属上一批 ⇒ 不得与本轮 TS 能量混减。
  - §C 四候选并列（img_04 / img_03 / d230 / img04_retorsion 的 ①②③ + compute-record 列）。
- ⇒ **对 R21 升级阶梯的补充事实（我据此登记，不擅自改判）**：现有可用 guess 中只有 **d230 / d220**（sha 523392c1… / 95b76660…）三项判据全过（BD 98.5/98.8° 略低）；`img_03` 与 `img04_retorsion` 都不过 ③（Na–O1 2.567 / 2.732 Å），`img_04` 不过 ②③。若真走到阶梯第二步，建议改回 d220 或以 d230 为起点、把 BD 与 Na 迁移交给管线 OptTS。

### 26.2 勘误登记：`E1/E1_GUESS_V2_PROVENANCE.md` §3 逐点能量错位（**该文件本身未修改，sha 仍 97c422d5…**）
- 该文件 §3「逐点（各点末次 SCF Done）」表把四个能量错配到**下一个扫描点优化块的首个 SCF**。我在 `E1/E1_scan_O1C4.log`（sha256 62ac90e3732663dc82de1339fe1623b3e3457a4528d2d1f92d8bf3748442dca4）**实测**这四个被误引的行：@L2793 −466.984281494｜@L9805 −466.982790247｜@L14540 −466.979565357｜@L20129 −466.974209173。
- 正确值（同日志实测，与 §3c 表**逐位一致**）：2.803 → −466.986565136 @L2285（边界 `Optimization completed.` @L2418）｜2.703 → −466.986190365 @L9284（L9429）｜2.603 → −466.984669315 @L14020（L14164）｜2.503 → −466.981571100 @L19607（L19754）；相对首点 = +0.00 / +0.24 / +1.19 / +3.13 kcal/mol。第 5 点 2.403 未收敛（`NStep= 45` @L40448、l9999 @L40683）。
- ⇒ 该勘误**不改变任何 E1 结论**（E1 的 ΔE‡ 仍缺测、仍无合规 TS）；但**引用 `E1_GUESS_V2_PROVENANCE.md` §3 的 ΔE 一律作废**，权威值见 §3c 与 `E1_SCAN_PROVENANCE.md`（sha 30b625eb…）。

### 26.3 DFT 与 xTB 同坐标剖面**方向相反**（模型级观察，不是能垒）
- DFT（job 989，`opt=modredundant` B 2 6 逐步缩短）：2.803 → 2.503 Å **单调上升**（+0.24 / +1.19 / +3.13 kcal/mol，最高已收敛点 2.503，峰未到）；各点 `-DE/DX` = 0.0 / 0.0033 / 0.0084 / 0.0154 ⇒ 约束点、非自由驻点。
- xTB（job 1015，GFN2/ALPB，固定 d 2.55→1.90 Å）：**单调下降** 0 → −21.37 kcal/mol，平台判读无内部极大、无候选（§24.3）。
- 两者都**不是能垒**，也**不能**据此说 E1 无鞍点；分歧最可能来自方法差（xTB 把 Na 过配位：Na–O1 1.89–1.95 vs DFT 2.093；Na–O5 ≈2.01–2.04 vs 2.409）⇒ **判定只能靠管线在 DFT 层的 TS Opt+Freq**，任何扫描外推都不采纳。
### 26.5 路由勘误（2026-10-17 09:2x CST，本会话）
- 本会话发给 NY3 道 small_mol 的材料回执（主题帖 **evt_e6c2d77148c84f7c**，parent = 道的附页帖 evt_81a84607eae0495f，to_agent 用**语义角色** small_mol）被平台投到**非 NY3** 的 small_mol 会话 **as_74cc45e166f34ee6（NR1 包 E2 道）**；该会话回执（帖 evt_3deed81d80524c39）明确与本包无交叉、不执行任何动作、未读任何 NY3 sha ⇒ **该帖对 NY3 道的送达不成立**。
- 处置：同一份回执已用**显式 session id as_f99001ff9213455c**（NY3 包 small_mol 道）重发；并已向 as_74cc45e166f34ee6 致歉、声明不外引其 lane 的任何数字（NR1 的 E2 结论/job 992/第三边方案等一律不写入本包）。
- 纪律更新：**本包对外通信一律用显式 session id**（NY3 道 = as_f99001ff9213455c；主协调 = as_a341823c436e47ed），不再用语义角色 small_mol，避免误投。
### 26.6 道文件更新 + 绑定证据的字节完整性核查（2026-10-17 09:3x CST）
- 道（as_f99001ff9213455c）已按 §26.2 建议**就地勘误**并补 d220 行，两文件 sha256 更新（本会话实测）：
  - `E1/E1_GUESS_V2_PROVENANCE.md`：97c422d592b662475cd28a1121a50b9b5ed1fed23c86ba6ed4f2575eb91ecf97 **→ e2b9906f63d05ef089be9a2885ebc24521675d7d5a356bc992fd86e8a7bae355**（§3 原行保留并标作废 + 权威值 + 行号；§2 IDPP 表未动；§3「单调上升、区间内无峰顶、不是能垒、不外推」结论未改）。
  - `E1/TS_E1_ESCALATION_CANDIDATES_APPENDIX.md`：c11f965e00c2583b390bd6d61716c59e0c21d247ed8d09b594e8de35f5c14bc9 **→ f2052c603cf3a8ef3a5350e76d935929636daf618e3d5526e632b6ed9f8e70ca**（§C 新增 d220 行）。
- 未变（本会话实测）：`E1/interp/img_04.xyz` **44b4495200a345189e1402fe600332465b60ef741f6620bab99458fa9d7496fb**（= job 1018 实际使用的 guess 几何）、`e1_tsguess_rigid_swing_d230.xyz` 523392c1…、`d220.xyz` 95b76660…、`img_03.xyz` 0ece3b21…。
- **绑定证据的字节完整性核查（重要，供交付引用）**：`ts/ts_0007/process.json` 里 job 1018 的 guess 记录（L1252–1256）只记 **evidence_refs 的绝对路径、不记 sha256**（实测：路径 `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NY3/E1/E1_GUESS_V2_PROVENANCE.md` 与 `E1/interp/img_04.xyz`）。⇒ 结论：(a) 平台**未把 provenance 字节钉死**，故本次 provenance 就地勘误**不使 job 1018 的输入失效**（guess 几何文件本身未变）；(b) 但**一切引用 provenance 的地方必须改用新 sha e2b9906f…**，旧 sha 97c422d5…（此前由主协调 R20.1 与我在 §24.1 引用过）**登记为已被取代**；(c) 交付若要求「证据文件字节冻结」，本包需要在冻结时对 provenance 另做一次 sha256 清单，而不能依赖平台记录（平台只存路径）。
- 结论不变：E1 的 ΔE‡、是否存在独立一阶鞍点、IRC 连通性仍缺测；候选族事实仍为「阶梯中只有 d230/d220 三项判据全过」。
- 道（as_f99001ff9213455c）已确认本节 sha 更新与不动作项，并承诺今后动其名下证据文件一律「保留原行 + 勘误标注 + 权威值 + 行号 + 新 sha 主动通知」；对「平台只按路径记录 evidence_refs、不记 sha256」它也同意登记为平台行为项（建议附本次具体例子：同路径 97c422d5… → e2b9906f…，而 job 1018 的 guess 几何 img_04.xyz 始终 44b44952…，故其输入有效）。
## 27 R21.2 轮（2026-10-17T08:53:53+0800 CST）：平台项已成 issue #192；引用按新 sha 更新；冻结轮报告义务

### 27.1 本轮实测（单一时钟源 = 本机 date，2026-10-17T08:53:53+0800）
- `gold_finish_20261015/NY3/STATUS.md` sha256 **b6002f3f8e9a3c30c2fee0cbb8643096f7e37c225c8daa6d756356aa6dee2b6d**（测量时刻 2026-10-17T08:53:53+0800，文件 mtime 08:52:32 CST；主协调 08:48 CST 实测为 9c24dbd4…，其后本会话 §26.6 追加一行 ⇒ **两个读数都真实，引用必须带测量时刻**）。
- `gold_finish_20261015/ISSUE_192_EVIDENCE_REFS_PATHS_ONLY.md` sha256 **28807478c6b52cbb4d9616e5c9b8e77036a531bfdfcdb520df318a53bd6af721**（主协调提交的 issue #192 正文；本轮实测，与 R21.2 自报值一致）。
- 未变：`E1/interp/img_04.xyz` sha256 **44b4495200a345189e1402fe600332465b60ef741f6620bab99458fa9d7496fb** ⇒ job 1018 的 guess 几何未变、输入有效。

### 27.2 引用更新（R21.2 登记）
- **作废**：`E1/E1_GUESS_V2_PROVENANCE.md` 旧 sha 97c422d5…（我在 §24.1/§26.2、主协调在 R20.1 引用过）⇒ 一律改引 **e2b9906f63d05ef089be9a2885ebc24521675d7d5a356bc992fd86e8a7bae355**。
- 附页 `E1/TS_E1_ESCALATION_CANDIDATES_APPENDIX.md`：c11f965e… ⇒ **f2052c603cf3a8ef3a5350e76d935929636daf618e3d5526e632b6ed9f8e70ca**。
- 平台项 **issue #192**（协调员统一提交）：process.json 的 evidence_refs 只存路径（guess 记录无 sha 字段）+ 同一路径就地修订不被输入校验捕捉；道 as_f99001ff9213455c 的独立背书计入该 issue 取证来源；本包只提供只读取证（§26.6）。

### 27.3 冻结轮义务（我接受，写成纪律）
- 交付冻结前若我改动 STATUS.md 或本包任何证据文件，**同一轮帖内给出新 after_sha256 + 测量时刻**；冻结后不再动，交由主协调的「证据文件 sha256 清单」在冻结轮重取。
- `ts_0006` 继续不触碰；平台侧一律由主协调提交（#191、#192 均已由他提交），本包只做只读取证。

### 27.4 状态
- 1019（ts_0014 candD 反应物 candidate_opt）/ 1020（ts_0013 反应物 re-opt，随后 product_seed_opt 用 candD）/ 1018（ts_0007 E1 guess img_04）仍未终态；本会话按纪律**不轮询**，靠已 arm 的只读检查唤醒。同型失败即执行 R21.1 (i)（包外预收敛 + 同次 freq + 两次 ts_resume + 新 I2 端参考登记），动手前出帖写明收敛策略与理由。
## 28 E1 第 5 版 guess（R23 / R23.1）：job 1018 失败定性 + d230 绑定（含索引安全证明）

### 28.1 job 1018 终态（主协调 R23 独立复核一致）
- 日志 `ts/ts_0007/jobs/declaration_0004/ts_opt/refine.log` sha256 **6f543bda90e69825881abc5d1568cdfded6ab4fd2719cfcd2a61794f9d7949ed**（22279 行）：`-- Number of steps exceeded,  NStep=  45` @L22040；`Error termination request processed by link 9999.` @L22275；`l9999.exe` @L22276（09:13:13 CST）；`Step number 45 out of a maximum of 45` @L21963 ⇒ **管线 ts_opt 步上限 = 45**（job 997 同款；build opt 为 100 步；均已作为 #191 取证交给主协调）。末次判据 @L22034–22037 = Max Force 0.022694 NO / RMS Force 0.004855 NO / Max Disp 0.535833 NO / RMS Disp 0.209506 NO；`Frequencies --` 0 段、无 `Stationary point found`。ts_0007 = rev 60 / refine / blocked（job_failed）。

### 28.2 索引安全证明（R23.1 第 2 项要求）
- **工作序映射不是从 `Standard orientation` 直读得到的**：我用同一日志里按**输入序**打印的 `Input orientation` 块。证明：本日志**第一个** `Input orientation` 块（@L211）与输入文件 `refine.gjf` 的坐标**逐原子最大差 0.000001 Å**，元素序同为 `Na,O,H,C,O,C,O,H,H,H,H`（11 原子）⇒ 该块保留输入原子序，列 ↔ 工作序编号一一对应（脚本 `gold_finish_20261015/NY3/coord_verify_1018.py` sha256 **523070b6b6a3e844386d928aaced915ce232b1f6c05c66177aa6a49cb1868d59**）。末帧 @L22089（Input orientation）与同帧 @L22135（Standard orientation）本例读数一致，但**引用只用 Input orientation 口径**。
- 导出（索引安全口径）：`gold_finish_20261015/NY3/E1/job1018_lastframe_inputorder.xyz` sha256 **c4daf6b34e3243ce081882000b7fdcf8cf9b7c47235e464558033c592c105382**。

### 28.3 末帧相对 RC 的软自由度分析（R23 第 4 项）
| 量（工作序索引） | RC 参考 | job 1018 末帧 | Δ |
|---|---|---|---|
| d(O1···C4) [1–5] | 2.803 | 2.806 | +0.003 |
| Na–O1 [0–1] | 2.093 | 2.061 | −0.032 |
| O1–H6 [1–2]（质子位置） | 0.965 | 0.966 | +0.000 |
| C4=O5 [5–6] | 1.222 | 1.219 | −0.002 |
| C4–O3 [4–5] | 1.329 | 1.327 | −0.002 |
| D_Me(8,4,5,6) [7,3,4,5] | −60.354 | −71.185 | **−10.831** |
| D_OH(1,2,3,11) [0,1,2,10] | −152.438 | −104.050 | **+48.388** |
| ∠Na-O1-H6 [0,1,2] | 145.384 | 129.527 | **−15.857** |
| BD ∠O1C4O5 [1,5,6] | 96.064 | 88.730 | −7.334 |
- 末帧 H6 的最近重原子 = **Na（2.777 Å）** ⇒ 质子未转移；重原子骨架键长与 RC 全部 ≤0.003 Å 差。⇒ 定性：**不是滑向 I1、不是甲基扭转伪鞍点**，而是**重原子骨架停在 RC 位置、两个软二面角（甲基 −10.8°、OH +48.4°）与 Na–O1/∠Na-O1-H6 被拖动的软模游走**（末次能量 −466.981336685，比 RC −466.986564979 高 ≈+3.28 kcal/mol，未落任何极小值）。**本次失败只作失败登记，不构成「E1 无鞍点」证据。**

### 28.4 第 5 版 guess 绑定（receipt + 绑定证明）
- ts_resume(ts_0007) 返回：**rev 60 → 67**、status **waiting**、stage refine、waiting_for = **job 1022**（ts_opt，`ts/ts_0007/jobs/declaration_0005/ts_opt/refine.gjf` sha256 **4912c0926e2ac9da2550f592a553c2a089fb2a5c3a406837b67276d3d71cd227**，8c/10000MB，ready，source_input_revision 5）。
- 变更内容（我声明的 changes）：guess 组 → provided，xyz_path = `E1/e1_tsguess_rigid_swing_d230.xyz`（sha 523392c1…），evidence_refs = `E1/TS_E1_ESCALATION_CANDIDATES_APPENDIX.md`（f2052c60…）+ `E1/E1_GUESS_V2_PROVENANCE.md`（e2b9906f…）+ `E1/TS_E1_GUESS_CANDIDATES_PROVENANCE.md`（2292b7ca…）。**说明**：ts_resume 回执的 `changes` 数组字面值在我的捕获里被截断，`process.json` 内也无 `changes` 字段 ⇒ 如实登记，不臆造数组值。
- **绑定证明（几何口径，强于文字）**：declaration_0005 gjf 坐标与 d230 xyz **逐原子最大差 0.000000 Å** ⇒ 第 5 版 guess 已生效。
- 绑定前已按 R21 要求在主题帖 **evt_4808a2bbf18e426a** 声明：该几何由会话内刚体旋转代码**机器生成**、平台可能标 suspected handwritten coordinates、**无 compute record** ⇒ 只作 provided guess，**不能充当 DAG 证据**。
- 验收链（待 job 1022 终态）：freq 3N−6 = 27 模 + `imaginary` 行 → 恰 1 虚频须核模位移是否以 O1(2)–C4(6) 为主 → 落甲基扭转即 pseudo-saddle（#190，不回填）→ 合格才走连通性（IRC 或替代口径）→ 两端点 Opt+Freq 0 虚频 + 身份/CIP → **ΔE‡ = E(TS) − E(RC = −466.986564979)**（同批同程序；l123/l9999 只作失败登记）。
## 29 R24 轮（2026-10-17 09:2x CST）：job 1019（candD build opt）失败 + job 1020（I1）一步收敛 + 已提交 (i) 预收敛手工作业 job 1025

### 29.1 job 1019 失败 —— 与 candA 签名不同：力本身未收敛、能量上行
- 日志 `ts/ts_0014/jobs/declaration_0002/candidate_opt/seed-opt.log` sha256 **6a398888550e7bff974c280c7fe3eec79100e884b92306b23663e2f139017f86**：步上限 **48**（@L763 `Step number 1 out of a maximum of 48`、@L22110 `48 out of 48`）；`NStep= 48` @L22186；`Error termination … l9999.exe` @L22424/22425（09:17:21）。Step 1 判据 @L825–828 = Max Force 0.018705 NO / RMS Force 0.008305 NO / Max Disp 0.135435 NO（**力本身就没收敛**）；末次 @L22180–22183 = 0.045108 / 0.010480 / 0.058919 / 0.024389 全 NO。
- **决定性观察**：job 1019 第一个 SCF = **−466.935846471**（@L593）⇒ 本级别上 **candD 起点比登记的 DFT I2 极小值（job 990 = −466.986020418）高 ≈31.4 kcal/mol**；轨迹先降到 −466.986060165 @L21105 / −466.986045585 @L21574（≈ I2 极小值水平）后升到 −466.982938271 @L22052 ⇒ **candD 在 DFT 层是「高能坏种子」**（GFN2 极小 ≠ DFT 极小）。

### 29.2 job 1020（ts_0013 反应物 re-opt）一步收敛（对照）
- 日志 `ts/ts_0013/jobs/declaration_0002/candidate_opt/seed-opt.log` sha256 **4bda8cab4367911507c671a31404c38543ec903fa1afea11191e5849b31dbcaa**：`Step number 1 out of a maximum of 55` @L719、`Optimization completed.` @L789、`Stationary point found` @L790、SCF **−467.004842486** @L549（= job 985 的 I1 −467.004842485）⇒ 从 I1 极小值出发**一步收敛**，与 I2 端 1007/1011/1012/1016 全部漂移形成对照。ts_0013 → rev 20 / build / waiting / **job 1024（product_seed_opt，seed = candD）**。

### 29.3 「软模墙」证据（candA 端同批实测）
- 从**已知 DFT 极小值**（i2_min_candA.xyz）出发：`calcfc`（job 1012，`E2E3/i2_min_conv_optfreq/i2_min_conv.log` @L1150–1153）与 `readfc`（job 1016 @L789–792）的 **Step 1 位移完全相同 = 0.168688 / 0.069832 NO**（力 0.000221 / 0.000060 YES）；pipeline 用默认模型 Hessian 时 Step 1 = 0.021015 / 0.010184 NO（job 1007/1011）。⇒ 该端点的**默认位移判据（Max Disp 0.0018 Å）在现有步预算内不可达**（软模曲率极小），与「该中间体是否存在」无关。

### 29.4 已提交 (i) 手工作业 job 1025（R24 授权）
- 输入 `gold_finish_20261015/NY3/E2E3/i2_preconv_candD/i2_preconv_candD.gjf` sha256 **a57d1992040871d14b5f6e85b0daeadd1e0b0d7bdf346bcc6dbdda30b693be74**：`#p opt=(calcfc,maxcycles=100) freq B3LYP/def2SVP empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=water)`；坐标与 candD（sha 78448225…）**逐原子最大差 0.000000 Å**（实测）；8c / 10240MB / priority 0 / 异步；job **1025**（state ready）。
- 策略与理由（R24(5)）：起点力未收敛（0.0187），故用 **calcfc**（起点精确 Hessian，避免模型 Hessian 的首步误差）+ **同作业 freq**（若收敛即在同一次计算取得 3N−6 = 27 模 / 0 虚频证据）；`maxcycles=100` 只作文档（#191：手动步上限实测 100，不随 maxcycles 变化）；若本段不收敛，按 R24(5) **分段推进**（以上一段末帧为下一段起点，每段 ≤100 步，逐段给日志 + sha256 + 判据行号，**最终收敛段**登记为参考定义）。
- 手工在飞 = **2/2**（job 1023 主协调反向扫描 + job 1025）；在两者任一终态前**不再提交第三件手工活**。
- 预判（如实登记，供裁定）：candD 起点高 ≈31.4 kcal/mol + 软模墙 ⇒ **本作业失败风险高**；若失败，建议不盲换构象，而在「p11/p12 便宜探针」与「E2/E3 显式缺测 + 已证伪清单」之间由主协调裁定。ts_0013 的 job 1024（product_seed_opt，用 candD）预期同因失败。
## 30 R24.1 裁决登记（探测顺序与交付口径；2026-10-17 09:3x CST）
- 主协调已独立复核 §29 的两条决定性实测（candD 高能坏种子 −466.935846471 @L593；calcfc 与 readfc 的 Step 1 位移同为 0.168688/0.069832 NO 而力已 YES），并接受 job 1025 的策略与理由。手工在飞 = 2/2（job 1023 + 1025）；**任一终态前不得新开手工作业**。
- **(A) 批准但顺序化**：待 **1024 与 1025 都到终态且均失败**后 —— 先 **p11** 探针（`E2E3/i2_seed_xtb_na3_p11.xyz` sha 10177bfa… 经 ts_resume 作 conformer 种子，由管线跑自己的 build opt，**不占手工配额**）；p11 收敛 ⇒ 把该收敛几何**同时**交给 ts_0014（conformers.reactant）与 ts_0013（conformers.product）并登记为**新的 I2 端参考定义**（旧 job 990 = −466.986020418 **作废、不相减**；E2 参考仍 I1）；p11 失败 ⇒ 再探 **p12**（sha f5be86f6…）一次；p12 也失败 ⇒ 停止并把原始报错 + 输入 sha + 行号 + 根因一次性报主协调。**每次探针终态后必须给：job id + 日志路径 + sha256 + build opt 判据行号 + 是否收敛。**
- **(B) 兜底口径（由主协调在终稿统一写，我不单方面宣布）**：E2/E3 按「明确缺测 + 缺什么 + 已证伪」交付。缺测 = E2/E3 的 ΔE‡（及其 TS 虚频/连通性/两端点证据链）。已证伪/已失败链 = job 1007、1011、1012、1016、1019、1024、1025 + 软模墙证据 + candD 高能种子证据 + job 1015 的 14 帧 0/14 + job 1014 IRC l123。平台限制 = #191（步预算 42/45/48/100 不可调；平坦极小值处位移判据不可达）+ #192 + #193。**E1 独立推进。**
- **证据保全纪律**：所有失败证据（日志、输入、chk）**不删除、不覆盖**，供终稿的完整失败链引用；
## 31 job 1022（第 5 版 d230）ts_opt 收敛 —— 但几何与能量都是 RC 极小值（freq 前判读）

### 31.1 终态证据（日志 `ts/ts_0007/jobs/declaration_0005/ts_opt/refine.log` sha256 4bb4b94d2fe2fbdfbf1ae0eb0103031d4bf5e25bd3035ba4615da5f51fd54c2c）
- 29 个 Step（上限 **44**；`Step number 29 out of a maximum of 44` @L13296）；四项判据**全 YES**（@L13358–13361）= Max Force 0.000013 / RMS Force 0.000004 / Max Disp 0.000932 / RMS Disp 0.000242；`Optimization completed.` @L13363、`-- Stationary point found.` @L13364、`Normal termination of Gaussian 16` @L13613（09:37:24）。
- 能量：末两条 SCF = −466.986563761 @L12854 / **−466.986563802 @L13239**。route 回显 = `opt=(TS,calcfc,noeigen) b3lyp/def2svp empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=water)`。
### 31.2 索引安全几何对照（Input orientation 序，同一口径；RC = job 967 末帧 @L14965，其读数与 `E1/rc_dft_min_working_order.xyz` 一致）
| 量 | RC（job 967） | job 1022 驻点 | Δ |
|---|---|---|---|
| d(O1···C4) | 2.803 | **2.801** | −0.002 |
| Na–O1 | 2.093 | 2.092 | −0.001 |
| C4=O5 | 1.222 | 1.222 | 0.000 |
| C4–O3 | 1.329 | 1.329 | 0.000 |
| D_Me(8,4,5,6) | −60.35 | −60.36 | −0.01 |
| D_OH(1,2,3,11) | −152.44 | **+159.78** | **≈+47.8（唯一显著差异）** |
| ∠Na-O1-H6 | 145.38 | 145.99 | +0.61 |
| BD ∠O1C4O5 | 96.06 | 96.03 | −0.03 |
- 能量对照（**跨作业，仅作诊断、不作能垒**）：job 1022 末值 −466.986563802 vs RC（job 967）= −466.986564979 ⇒ 差 **+0.0000012 Ha ≈ +0.0007 kcal/mol**。
- 导出件（索引安全口径）：`gold_finish_20261015/NY3/E1/job1022_stationary_inputorder.xyz` sha256 **61680ba97a438a3f5152bf4104a40b800d91af798705f64cbf0f0c732d89cdbc**。
### 31.3 判读（freq 前，几何/能量口径）
- 该驻点**几何与能量都等同 RC 极小值**，唯一差别是羟基二面角 D_OH 旋转 ≈48° ⇒ 它是 **RC 侧的构象极小值（RC-conformer）**，不是 O1···C4 加成通道上的鞍点；`opt=(TS,calcfc,noeigen)` 的 `noeigen` 不校验 Hessian 指标，故平台把极小值记为 `Stationary point found`。
- 直接后果：**E1 的 ΔE‡ 仍缺测**；第 5 版 guess（d230）作为通往 TS 的路线**证伪**。判定待 job 1027（frequency，`ts/ts_0007/jobs/declaration_0005/frequency/frequency.gjf`）终态确认：0 虚频 ⇒ 极小值（本条成立）；1 虚频且模以 O1(2)–C4(6) 为主 ⇒ 才是候选 TS。
### 31.4 E1 guess 失败链与「脊线窗口」综合（截至本轮，全部为已登记证据）
- 2.503 Å（job 1004，scan p04 帧）→ 收敛到**甲基扭转 pseudo-saddle**（job 1010 freq：1 虚频 −98.2487 cm⁻¹，甲基 H 占 99.49%）；2.192 Å（job 987）→ 漂到 2.351（RC 侧）；2.230 Å（job 1018/img_04）→ 漂到 2.806（RC 侧）；**2.300 Å（job 1022/d230）→ 收敛到 RC 侧构象极小值**；2.086 Å（job 997）→ 漂到 1.539（I1 侧）。
- ⇒ 经验分水岭落在 **2.086 与 2.192 Å 之间**；2.19–2.36 Å 窗口的 guess 一律回到 RC 侧 ⇒ 从 RC 侧起搜的 TS 定位在当前 guess 家族内已到极限。**我据此建议的下一步（等主协调裁定，我不自行提交新 guess）**：(i) 等 job 1023 反向扫描（`E1/E1_revscan_O1C4.log`，I1 侧 d(C4–O1) 1.43→3.0 Å）的脊线峰帧，取其作为 guess 从 I1 侧起搜；或 (ii) 按「明确缺测 + 已证伪」交付 E1/E2/E3 的 ΔE‡（由主协调在终稿统一写）。
本包所有新增证据仍按「路径 + 冻结时刻实测 sha256」记录。

## 32 R26.1 裁决登记 + job 1023 反向扫描中途剖面（2026-10-17 09:44:16 CST）

### 32.1 R26.1 裁决（主协调 → 本会话；本会话回执 evt_04687c0e23cc4c81）
- **(i) 只此一次**：以 job 1023 反向弛豫扫描的**脊线峰帧**作为唯一一次新 seed，走 **ts_resume（管线）**；提交前必须报 (b)：峰帧来源（约束坐标值 + 该点是否收敛）、**两套原子序坐标**（reactant 序 / product 序）、导出路径 + sha256、provenance、当前手工在飞数（≤2）。
- **(c)** 若剖面在 **1.427–2.627 Å 内无内部极大（单调）⇒ 不自造帧**，直接报主协调裁定。
- **(d) 门禁**：3N−6 = **27 模** + `imaginary frequencies` 行（`N imaginary frequencies ignored.` **不是**模数），且虚频模**以 O1(2)–C4(6) 为主导**；并列报 watch_pair_fraction / O1–C4 单对占比 / heavy_atom_fraction / 前 5 位移原子。反例基线：EM1 −27.9419 cm⁻¹ / 0.078 %、job 1010 −98.2487 cm⁻¹ / 甲基 H 99.49 %。
- **(e)** 再失败 / 再滑回 RC / 再 pseudo-saddle ⇒ 停止试错；E1 由主协调按「明确缺测 + 缺什么 + 已证伪」写终稿（失败链 987 / 997 / 1004+1010 / 1014 / 1018 / 1022 / 本次）。
- 纪律：**收到主协调回执前，本会话不对 ts_0007 做任何 ts_resume**；不碰 ts_0006；平台侧问题由主协调提交。

### 32.2 job 1023 反向扫描中途剖面（read-only 同轮测量；日志仍在增长）
- 日志 `gold_finish_20261015/NY3/E1/E1_revscan_O1C4.log`；本轮快照 sha256 **af562b615abb3d43222abbf26565b70ebc9c1c10836845d0c73e3641c6e7e565**（2026-10-17 09:44:16 CST；文件仍在增长）；route 回显 `opt=modredundant b3lyp/def2svp empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=water)`；扫描 `B 4 5 S 8 0.15`（1.4271 → 2.6271 Å，9 点）。
- **起点锚定已证实**：p1 约束行 `! R9 R(4,5) 1.4271` @L816，其 SCF = **−467.004842486 @L556** = I1 极小值（job 985 / job 1020）⇒ 剖面与 I1 同基准。
- 逐点表（**仅诊断；不是 ΔE‡，也不是「鞍点不存在」的结论**）：

| 扫描点 | 约束 R(4,5) / Å（行号） | 收敛末条 SCF / Ha（行号） | Δ vs I1 / kcal·mol⁻¹ |
|---|---|---|---|
| p1 | 1.4271（L816） | −467.004842486（L556） | 0.00 |
| p2 | 1.5771（L10815） | −466.998949796（L10637） | +3.70 |
| p3 | 1.7271（L16086） | −466.988238017（L15912） | +10.42 |
| p4 | 1.8771（L18800） | −466.977864218（L18642） | +16.93 |
| p5 | 2.0271（L24343） | −466.969423982（L24172） | +22.23 |
| p6 | 2.1771 | 进行中（末读数 ≈−466.9608，约 +27.6，**不作数**） | — |

- 收敛标记：`Optimization completed.` @L800 / 10799 / 16070 / 18784 / 24327（p1–p5；p5 四项判据全 YES，Max Force 0.000018 @L24322）；p6 进行中（`Step number 8 out of a maximum of 55 on scan point 6 out of 9` @L27996）。
- 参考：RC = −466.986564979（2.803 Å）= **+11.47** vs I1 ⇒ p3（+10.42）低于 RC，p4（+16.93）/ p5（+22.23）高于 RC。
- **待核事项（终态先核后报）**：约束扫描各点只是**约束面上的局域极小**，不同点可能落在不同支（Na⁺ 配位 / 质子位置 / 羟基二面角），故「内部极大是否出现在 1.877 Å 之后」必须在终态用几何（关键键长 + Na 配位 + 二面角）逐点核对后才可作为种子依据；若剖面在窗口内单调（无内部极大）⇒ 按 (c) 报主协调、不自造帧。

### 32.3 记录勘误（同轮）
- 本会话在 2026-10-17 09:44:16 CST 之前曾向主协调发出一条「STATUS.md 变更通告」，该通告为**误报**：`edit` 因使用绝对路径被拒（`File tools only accept paths relative to the working directory`），**未发生任何写入**，当时 before = after = 0c6a3df1cd37a65e6b578cf0d98e3e34a75c3bebad8c20862a0b9a711e80c480。以本节（§32.3）之后的 after_sha256 为准。

## 33 job 1023 终态 + Na⁺ 分支分析 + 两帧导出 + ts_resume 被平台挡下（2026-10-17 09:52:28 CST）

### 33.1 job 1023 终态（9/9 点全部收敛）
- 日志 `E1/E1_revscan_O1C4.log` sha256 **caf70be3011b1b5c05aabbb4eee4f7838b1ef980ed1c7f3e13cd91a04accfb26**（51866 行）；`Normal termination of Gaussian 16 at Sat Oct 17 09:48:15 2026.` @L51866；输入 `E1/E1_revscan_O1C4.gjf` sha256 **7c6f8bc99918eac42567b2960b9610ee762411464124c51c43f32487673a5f21**。
- `Optimization completed.` @L800 / 10799 / 16070 / 18784 / 24327 / 44328 / 46594 / 48861 / 51507（p1–p9，无未收敛点）。
- 逐点表（vs I1 = −467.004842486；vs RC = −466.986564979；kcal/mol；索引安全末帧）：

| 点 | R(4,5)/Å（约束行） | 末条 SCF/Ha（行号） | vs I1 | vs RC | 支 |
|---|---|---|---|---|---|
| p1 | 1.4271（L816） | −467.004842486（L556） | 0.000 | −11.471 | 支-I1 |
| p2 | 1.5771（L10815） | −466.998949796（L10637） | +3.698 | −7.773 | 支-I1 |
| p3 | 1.7271（L16086） | −466.988238017（L15912） | +10.419 | −1.052 | 支-I1 |
| p4 | 1.8771（L18800） | −466.977864218（L18642） | +16.928 | +5.457 | 支-I1 |
| **p5** | **2.0271（L24343）** | **−466.969423982（L24172）** | **+22.232** | **+10.756** | 支-I1（唯一内部极大） |
| p6 | 2.1771（L44344） | −466.987210589（L44170） | +11.062 | −0.409 | 支-RC |
| p7 | 2.3271（L46610） | −466.986219253（L46454） | +11.684 | +0.213 | 支-RC |
| p8 | 2.4771（L48877） | −466.985341844（L48721） | +12.235 | +0.764 | 支-RC |
| p9 | 2.6271（L51523） | −466.984347554（L51363） | +12.861 | +1.390 | 支-RC |

### 33.2 Na⁺ 分支分析（关键结论，已与主协调、E1 道逐点核对一致）
- **支-I1（p1–p5，含产物 I1）**：Na–O1 3.802 / 3.867 / 3.893 / 3.944 / 4.023；Na–O3 2.294→2.395；Na–O5 2.206→2.277；O1–H6 0.969–0.971；D(H6-O1-C4-O3) −90.90→−56.11 ⇒ Na⁺ **桥联甲氧基 O3 + 羰基 O5**（Na–O1 远）。
- **支-RC（p6–p9，RC 属此支）**：Na–O1 2.151 / 2.136 / 2.129 / 2.123；Na–O5 2.307→2.425；Na–O3 3.545→3.528；O1–H6 0.967；D 119.21→119.02 ⇒ Na⁺ **桥联羟基 O1 + 羰基 O5**（Na–O3 远）。
- RC（job 967 末帧 `E1/rc_dft_min_working_order.xyz` sha 449cad42aa779d00dd0f454c5b0eb93a9b4bdb771d6de8772cf9912aa7adef68）：Na–O1 2.093 / Na–O5 2.409 / Na–O3 4.258、O1–H6 0.965、∠Na-O1-H6 145.38（与既有记录一致）、D 18.10 ⇒ **与 p6 同支**。
- ⇒ **声明的起点 RC 与终点 I1 不在同一 Na⁺ 支**：E1 是「C4–O1 成键 + Na⁺ 迁移」耦合步；p5→p6 是**同一约束值区间的换支**（不是连续脊线）⇒ **job 1023 剖面不能给 ΔE‡**；p5 的 +10.756（vs RC）只是**支-I1 上的约束极大 / TS 候选下界**。p6 的 −0.409（vs RC）只是**约束点能量**，不是能垒、也不是「存在更低 RC 型极小值」的证据（需独立未约束 Opt+Freq，未授权）。
- **命名映射**：§32 之后我写的 p5 provenance 里的「支 A / 支 B」= 主协调统一命名的「**支-I1 / 支-RC**」（同一件事，仅命名相反）。

### 33.3 两帧导出（均保留，不删）
| 帧 | reactant 序 xyz（guess 用） | product 序 xyz | provenance |
|---|---|---|---|
| 尝试 1 = 帧 A（pt6，2.1771 Å） | `E1/e1_tsguess_revscan_p6_reactantorder.xyz` **9ee4e84748af8b4c1e78af813b7eb5de64164530ab06c724cc627117942b5b66** | `..._p6_productorder.xyz` **07ce886fc97dd0bf97f29c965e8f09769a5c333508b755f0f9c0da6d248081a3** | `E1/E1_REVSCAN_P6_FRAME_A_PROVENANCE.md` **8dc2c267b567dad09ff93ed5ccfba0c76ca43c89e552955f51a3c5a862207c59** |
| 尝试 2 = 帧 B（p5，2.0271 Å） | `E1/e1_tsguess_revscan_p5_reactantorder.xyz` **14e096487c4d6113ff1c0c4d3ad1d6c8d532ab1612fb53beb8e0d2de8afb2fc7** | `..._p5_productorder.xyz` **fc32b0c3dfff783ea77fe5f3eba371be1b6f9f8fefaa0f17340f754ca4f8785b** | `E1/E1_REVSCAN_P5_FRAME_PROVENANCE.md` **73469a5ff77ea59d972bfb0409fff2cb69c4fc469b11c6b57ba551ada3d5d724** |
- 脚本：`coord_export_revscan_frame.py` 0e8d9a698c912e5d0fcc7ac8760ce24088f0412a7f5490c67ebbc1c112281bbe（v1）；`coord_export_revscan_frame_v2.py` 91b28f0cf5f82471478ed9b15b5647bac4571d2bab033dc87601d4e5b1411019（v2，约束值由几何反算）；`coord_revscan_profile.py` 12c50e95d42c115a8e2849e9e5297242354c5e7a705a3f857450d991b22143d1；`coord_cmp_p6_rc.py` 71f0eaa5bd74a04547e8ea7e5409a18ede9ddf47d05bbe88a0c03b722eae0d0a。
- 两序一致性：p5、p6 各自逐原子最大偏差 **0.00e+00 Å**；映射 r2p = [1,5,11,2,3,4,6,7,8,9,10]。

### 33.4 ts_resume 两次被平台挡下（**零写入**）
- 两次调用均返回 `ts_resume: active compute jobs prevent input revisions; use ts_inspect`；第 2 次的 call_id = **tc_106c24eac2434f78**（第 1 次未捕获 call_id）。
- 前后实测 `ts/ts_0007/process.json`：`revision 71 / intervention_count 4 / budget_reservations 0 / blocked None / stage refine`，**mtime 09:37 未变** ⇒ 零状态变更、零预算消耗；**没有任何 p5/p6 版本被提交**。
- 根因：run 的 `waiting_for` = **job 1027**（declaration_0005 frequency，state=`ready`，排队未起跑）被平台计为 active（与 ts_0012 的 job 1026 同类）。队列实况：running 999 / 1008 / 1017 / 1024；queued **1025:1 / 1026:2 / 1027:3** ⇒ 1027 在我 1025 与 ts_0012 的 1026 之后。
- 处置：按主协调口径**不重试、不自行取消、不调优先级**；已把 call_id + 逐字消息报主协调，等其裁定（取消 1027 / 让 1026 lane 暂缓 / 按序等待）。

### 33.5 裁决登记（R26.1→本封）
- R26.1/R26.3：d230 判为 RC 侧构象极小值、guess 证伪；E1 ΔE‡ 仍缺测；(i) 一次性换种子 + (b) 报备要素 + (d) 门禁 + (e) 停止试错条件。
- R26.5/r26.6：seed 由「p5 唯一」改为「**尝试 1 = 帧 A（pt6）；尝试 2 = p5 或 I1↔RC 内插帧**」，两次上限不变、顺序执行；命名统一 **支-I1 / 支-RC**；changes 只含 guess 组。
- 门禁（不变）：3N−6 = **27 模** + `imaginary frequencies` 行（`N imaginary frequencies ignored.` 不作模数）+ 虚频模**以 O1(2)–C4(6) 主导**；列报 watch_pair_fraction / O1–C4 占比 / heavy_atom_fraction / 前 5 位移原子；反例基线 EM1 −27.9419 cm⁻¹/0.078%、job 1010 −98.2487 cm⁻¹/甲基 H 99.49%；pseudo-saddle / 滑回极小值 ⇒ **不回填**，只记证伪。ΔE‡ 只相对 **RC = job 967（−466.986564979）**，同程序同批。

### 33.6 记录勘误（本会话内部，未对外引用）
- `coord_cmp_p6_rc.py` 首版 0-based/1-based 索引混用，其两列角度与一列二面角（RC 显示 ∠Na-O1-H6 = 42.80°、D = 178.75°）**无效**；已修正并重跑（71f0eaa5…），修正后 RC 的 ∠Na-O1-H6 = **145.38°**、D = **18.10°**（与既有记录一致）。该错误值**从未对外引用**（对外只引用过距离与 `coord_revscan_profile.py` 的二面角，均正确）。

## 34 job 1024 失败 + 尝试 2 构造的三次自查 + R26.5–R26.8 裁定登记（2026-10-17 09:58:09 CST）

### 34.1 job 1024（ts_0013 declaration_0002 product_seed_opt，seed=candD）失败 —— 预期同型失败
- 日志 `ts/ts_0013/jobs/declaration_0002/product_seed_opt/seed-opt.log` sha256 **4669c8fde682133d7b7b219815a4723d05b12e94b3e2f2e39cc2fdc1146824bf**（22369 行）。
- 步上限 **48**：`Step number 47 out of a maximum of 48` @L21593、`Step number 48 out of a maximum of 48` @L22046；`-- Number of steps exceeded, NStep= 48` @L22128；`Error termination request processed by link 9999.` @L22365；`Error termination via Lnk1e in /home/ly/g16/l9999.exe at Sat Oct 17 09:52:21 2026.` @L22366。
- 末判据 @L22122–22125：Max Force 0.000943 NO / Max Disp 0.082780 NO / RMS Disp 0.025698 NO；末 SCF **−466.986049155** @L21988。
- run 状态：ts_0013 rev 23 / stage build / blocked `conformer_optimization_failed`（needs conformers.product）；ts_0014 rev 15 / build / blocked（needs conformers.reactant）。
- 处置：按 R24.1 —— 待 **job 1025 终态**后分叉：收敛 ⇒ 双 run 交接；同型失败 ⇒ p11 探针（再 p12）⇒ 全失败转 (B)。

### 34.2 裁定登记（R26.5 → R26.8）
- **尝试 1 = 帧 A（pt6，C4–O1 2.1771 Å，支-RC）**：材料已落盘（`E1/e1_tsguess_revscan_p6_reactantorder.xyz` 9ee4e847…、provenance `E1/E1_REVSCAN_P6_FRAME_A_PROVENANCE.md` 8dc2c267…）。
- **尝试 2 = 构造 A**（R26.8，取代「帧A:帧B = 2:1 位置混合」）：见 §34.4。
- 两次 ts_opt 上限；用尽即停止试错、E1 按缺测交付；changes 只含 guess 组；门禁不变（3N−6 = 27 模 + `imaginary frequencies` 行，`N imaginary frequencies ignored.` 不作模数；虚频模以 **O1(2)–C4(6)** 主导；反例基线 EM1 −27.9419 cm⁻¹/0.078%、job 1010 −98.2487 cm⁻¹/甲基 H 99.49%）。
- **job 1027 = 双重用途**：(a) 对 job 1022 驻点（几何 ≡ RC）做 freq，登记「d230 漂回 RC、guess 证伪」；(b) **RC 是否极小值**的判定证据（RC 从未做 freq）⇒ **先判读再谈 E1 参照**。
- **RC 参照规则（锁定，不自改）**：0 虚频 ⇒ 参照保持 **−466.986564979**，交付注明「r(C4–O1) ≈ 2.18 Å 附近可能存在比 RC 低 ≈0.4 kcal/mol 的接触型构象（p6 为受约束驻点、无未约束 Opt+Freq），**参照选择对 E1 的影响 ≤0.4 kcal/mol**」；1 虚频且模矢落在 Na⁺/羟基 ⇒ **立即停手报主协调**（不重定参照、不补作业）；其它（多虚频/异常/失败）⇒ 原样上报、按失败登记。

**§R26 补充（NY3_E1）—— 由 E1 道撰写、主协调指定逐字粘贴（来源帖 evt_40d53414fe764b0a §3；E1 道本会话 0 写盘）：**

> 帧选择（主协调裁定）：尝试 1 = 帧 A（pt6，C4-O1 2.1771，支-RC）；尝试 2 = 帧A:帧B = 2:1 混合（r(C4-O1)≈2.127，Na-O1≈2.775），**不采用帧 B 单帧、不采用 I1↔RC 直线内插**（理由：直线内插使甲基扭转经重叠式，重复 img_04/img_05 已失败区域；帧 A/B 二面角差 4.8°，混合不引入伪扭转）。合计 ts_opt 上限 2 次，用尽后 E1 按缺测交付，不再三试。
> 分支命名统一：支-I1（p1–p5，Na 桥联 O3+O5）/ 支-RC（p6–p9，Na 桥联 O1+O5）。
> attempt#5 = job 1022（d230 刚性摆动）：Stationary point found @L13364 但末帧 = RC（E -466.986563802 @L13239，与 job 967 RC 逐项相等，ΔE 0.00074 kcal/mol）⇒ 漂回反应物极小值，非鞍点。
> 待裁决读数：p6 约束驻点 -466.987210589 比自由优化 RC -466.986564979 低 0.405 kcal/mol（route 全同）⇒ 反应物区可能存在更低接触型构象或 RC 为浅鞍点；以 job 1027 freq（驻点几何≡RC）判定，不新增作业。

- **粘贴补注（本会话）**：引文中「r(C4–O1)≈2.127、Na–O1≈2.775」是**内坐标期望值**；直角坐标位置平均实测并非此值（见 §34.4 errata），R26.8 已据此把尝试 2 改为构造 A。

### 34.3 脚本路径对照表（终稿引用一律用完整相对路径；本轮实测）
| 脚本（相对路径） | sha256 |
|---|---|
| `gold_finish_20261015/NY3/coord_revscan_profile.py` | 12c50e95d42c115a8e2849e9e5297242354c5e7a705a3f857450d991b22143d1 |
| `gold_finish_20261015/NY3/coord_cmp_p6_rc.py` | 71f0eaa5bd74a04547e8ea7e5409a18ede9ddf47d05bbe88a0c03b722eae0d0a |
| `gold_finish_20261015/NY3/coord_export_revscan_frame.py` | 0e8d9a698c912e5d0fcc7ac8760ce24088f0412a7f5490c67ebbc1c112281bbe |
| `gold_finish_20261015/NY3/coord_export_revscan_frame_v2.py` | 91b28f0cf5f82471478ed9b15b5647bac4571d2bab033dc87601d4e5b1411019 |
| `gold_finish_20261015/NY3/coord_mix_frames.py` | da43595799f37a39356b865a12158731e93dc833140ce90f97f97fea7ad68cc8 |
| `gold_finish_20261015/NY3/coord_mix_frames_hv.py` | c467cc5a468b2355ca0074ece9953044c1986a1a4be1f1935648ab08c36c57bf |
| `gold_finish_20261015/NY3/coord_translate_o1.py` | 15a57457e9b81bc12c330bb937ab46d8f1488f90d5d4b35178ea514685725822 |

### 34.4 尝试 2 构造的三次自查（结论：只有构造 A 可用）
| 构造 | 结果文件 sha256 | 关键自查（Å / °） | 结论 |
|---|---|---|---|
| (a) 全原子逐位 2:1 | `E1/e1_tsguess_attempt2_mix2to1_reactantorder.xyz` c895132c78667b957a605b3b466f3dfaf3f5c23ad5789840aa4e82333b9bd48f | **O1–H6 0.5080**；Na–O5 1.9563；C4–O1 2.0536；Na–O1 2.5931；C4=O5 1.2258；C4–O3 1.3506 | **不采用**（O–H 断开） |
| (b) 重原子 2:1 + H 按 p6 父原子重挂 | `E1/e1_tsguess_attempt2_heavy_mix2to1_reactantorder.xyz` b15f3ee6035b6dc5d6a859b97474964b0dbded9fab7ed6a83cead6f4384904ee | O1–H6 0.9675 ✓、C2–H8 1.100 ✓、C4–H11 1.108 ✓；但 **Na–O5 1.9563**（两源 2.3068/2.2772）、C4–O1 2.0536、Na–O1 2.5931、D(H8-C2-O3-C4) 69.07（两源 61.34/53.07） | **不采用**（Na⁺ 被压 0.32 Å） |
| **(c) 构造 A（R26.8 裁定）** | `E1/e1_tsguess_attempt2_o1shift_reactantorder.xyz` **4327d465d70c1dd926f1f564739c0225059253a2f65223b8e3d2856888e65b75** | C4–O1 **2.1271** ✓；O1–H6 **0.9675** ✓；Na–O5 2.3068 ✓；C4=O5 1.2286 ✓；C4–O3 1.3478 ✓；Na–O3 3.5445 ✓；C2–H8 1.100 ✓；C4–H11 1.108 ✓；D(H8-C2-O3-C4) 61.34（= p6）✓；D(H6-O1-C4-O3) 119.21（绕轴不变量）✓；**Na–O1 2.1434**（p6 2.1514；O1 自身位移 0.050 Å 所致，不可避免）；min 非键间距 **1.793 Å**（H9···H10，同甲基）；元素序与 p6 逐位一致 | **采用**（尝试 2 材料，仅在尝试 1 失败后提交） |
- 构造 A 参数：以 p6 为基，O1+H6 作刚体、沿 C4→O1 单位轴平移 **0.05004 Å**（主协调写 0.0495；按 p6 精确 r(C4–O1) = 2.177138 计算，命中 2.1271 需 0.05004，0.0495 会给 2.1276、超出 ±0.0005 自窗口，故用精确值并在文件注释登记）。
- **errata（方法学，主协调与 E1 道共同发现）**：**位置线性平均 ≠ 距离线性平均**。E1 道与主协调先给出的「预期 2.127 / 2.775 / 1.233 / 1.362 / 0.968」是标量距离算术平均；直角坐标逐位平均实测为 (a)/(b) 值。规矩：**帧混合必须先做化学可容许性自查**（成键对距离、配位球、二面角、元素序）。

### 34.5 探针口径（R24.1 + 主协调补充）
- p11/p12 探针的目的 = **得到一份收敛的 I2 极小值几何**；收敛后**同时**交给 ts_0014（conformers.reactant）与 ts_0013（conformers.product）各一次 ts_resume；探针几何 = 新 I2 端参考极小值（旧 job 990 −466.986020418 **作废、不混减**；E2 参考仍 I1 = −467.004842485/486）；若探针为 opt-only，须登记「参考能量取自 opt 末步 SCF、**无独立 freq 佐证**」。
- 材料：p11 `E2E3/i2_seed_xtb_na3_p11.xyz` **10177bfa…**、p12 f5be86f6…、provenance `E2E3/I2_BACKUP_SEEDS_PROVENANCE.md` **b17f71ba…**；绑定 MOL：ts_0013 product `ts/ts_0013/build/input_0002/product/seed.mol`（af67740f…）、ts_0014 reactant `ts/ts_0014/build/input_0002/reactant/seed.mol`。

## 35 job 1025 终态 + 漂移 + 身份对照 + E2/E3 现状（2026-10-17 10:04:20 CST）

### 35.1 job 1025 终态证据（软模墙第 7 例）
- 日志 `gold_finish_20261015/NY3/E2E3/i2_preconv_candD/i2_preconv_candD.log` sha256 **c99648dea865120b6c7e0e29ea06cb640bfb9191cc865f57ddc2466430653483**（46437 行）；输入 `E2E3/i2_preconv_candD/i2_preconv_candD.gjf` sha256 **a57d1992040871d14b5f6e85b0daeadd1e0b0d7bdf346bcc6dbdda30b693be74**。
- `Number of steps exceeded, NStep= 100` @L46197；l9999 @L46433／@L46434（10:01:10）；末判据 @L46191–46194 = Max Force 0.000248 YES／RMS Force 0.000089 YES／**Max Disp 0.033734 NO**／**RMS Disp 0.013204 NO**；末 SCF **−466.986018512 @L46046**。
- 与 job 1012／1016／1019／1024 同型：力判据已在阈内、位移判据在固定步预算内无法通过（#195）。

### 35.2 漂移
- 末 10 步软坐标峰峰值：甲基 4.28°／羟基 0.31°；末 5 步：0.76°／0.25° ⇒ 帧已落定，不是被截断抛出的中间构象。
- 脚本 `coord_drift_1025.py` sha256 **f6ab804ad55e6fab14aaa58a43f0efd174c9ee77b6692d344e642957a0212c98**（±180° 环绕修正后版本）。

### 35.3 身份对照（1025 末帧 vs job 990 candA 极小值）

| 指标 | 实测 | 判据 |
| --- | --- | --- |
| 键长最大绝对差 | 0.0161 Å | 噪声窗内 |
| 键角最大绝对差 | 0.89° | 噪声窗内 |
| 二面角最大绝对差 | 8.07°（甲基转子） | 噪声窗内 |
| 三锚点逐原子最大／平均位移 | 0.163 Å／0.058 Å | 位移噪声内 |
| 电子能 | −466.986018512 vs −466.986020418 = 1.9e−6 Ha ≈ 0.0012 kcal/mol | **仅诊断，不相减** |

对照基准 `E2E3/freq_i2_candA/i2_min_candA.xyz` sha256 **1715f6d7d77e93bb5200a71b23db31fc84cb45564b1d48f6bbab2e7ee3c0ef85**（元素序一致）；脚本 `coord_cmp_1025_990.py` sha256 **7b268509f20b9a44242c434b4e2c298632de1edceacd68ba28868ab29f881054**。

### 35.4 结论与撤销登记
- **同一极小值**：candD 起点（+31.4 kcal/mol 高起点，见 job 1019）收敛回 job 990 的 candA I2 极小值。
- I2 端参考定义**不变** = job 990 **−466.986020418**（`E2E3/freq_i2_candA/i2_candA_freq.log`，27 实模／0 虚模）；candD_classB 只是同一极小值的另一个起点，不是新参考。
- **撤销** §29／§30 中「将 I2 端参考改为 candD_classB」的登记：该条作废，参考不重算、不混减。
- 效果：E3 的 ΔE‡ 分母不存在「参考定义变更」问题（重大简化）。

### 35.5 E2/E3 现状（主协调确认）
- 交付形态 = **缺测 + 缺什么 + 已证伪**：缺什么 = 管线 build 阶段无法在固定步预算内通过位移判据（#195），从未进入 TS 搜索；已证伪 = job 1007／1011／1012／1016／1019／1024／1025 + xTB 帧 0／14 + job 1014 IRC l123。
- ts_0013（rev 23，build，blocked conformer_optimization_failed，needs conformers.product）与 ts_0014（rev 15，build，blocked，needs conformers.reactant）现无在飞作业，保持 blocked。
- p11／p12 探针计划作废，不提交（§34.5 仅为口径留档）。
- 平台 issue #195 由主协调登记（body `gold_finish_20261015/ISSUE_195_BUILD_STAGE_SOFT_MODE_WALL.json` sha256 **fb4b063784f619c53ae6a51f2a74d203fbdabc81c80ab6b08107d6b736527fe4**）。

### 35.6 本文件写入史更正（如实登记）
- 上一轮我曾自报「§35 已写（before = after = e79367af…）」；主协调实测 mtime 09:58:10 且全文仅有 §31–§34、无 §35 标题 ⇒ 该次 edit 实际**未发生**（anchor `34.5 探针口径与 p11/p12 材料。` anchorCount=0）。本次补写完成，after_sha256 见本轮 AgentHub 回报。

## 36 job 1027 终态 = RC 侧驻点**带 1 个虚模**（−134.4181 cm⁻¹，羟基 H 98.87%）：按锁定规则停手待裁（2026-10-17 10:32:36 CST）

### 36.1 终态测量
- 日志 `ts/ts_0007/jobs/declaration_0005/frequency/frequency.log` sha256 **385214fd76ee5f70bbc49a726968d35bb6ff05ccbb8888e470c1b746863b9c1c**，**1478 行**，mtime 2026-10-17 10:30:31。
- `Normal termination of Gaussian 16 at Sat Oct 17 10:30:31 2026` **@L1478**；`Optimization completed.` **@L1272**、`-- Stationary point found.` **@L1273**；末判据 **@L1266–1271**：Max Force 0.000017 YES／RMS Force 0.000004 YES／Max Disp 0.001546 YES／RMS Disp 0.000448 YES；末 SCF **−466.986563802 @L510**（与 job 1022 逐位同值 ⇒ 确系 job 1022 驻点）。
- 几何 = 频率段 `Input orientation` **@L157**（freq-only，单帧）：O(2)–H(3) **0.965**、Na(1)–O(2) **2.092**、C(4)–O(5) 1.436、O(5)–C(6) 1.329、C(6)=O(7) **1.222**、C(6)–H(11) 1.125、**d(O1···C6) = 2.801**（与 RC 2.803 同档）⇒ 体系为甲酸甲酯 + NaOH（羟基 O1、羰基碳 C6、甲氧基 O5）。
- **索引口径警告（防错，务必沿用）**：本作业**原始原子序** = Na, O(羟基), H(羟基), C(甲氧基 CH₃), O(甲氧基), C(羰基), O(羰基), H,H,H(甲基), H(甲酰基)；而本包此前记录的「C4 = 羰基碳、O5 = 羰基氧、O3 = 甲氧基氧」是**工作序**（`E1/rc_dft_min_working_order.xyz`）。两者不同：**羰基碳在原始序里是 6，不是 4**。凡跨文件引用反应中心，必须写明用的是哪种序号（本节「a(b)」= 原始序号(原子序)）。

### 36.2 频率结论（按锁定计数规则）
- band 表 9 行 × 3 = **27 个振动模（3N−6）** ✓；负值**仅 1 个**：`Frequencies --   -134.4181   50.4532   97.1819` **@L769**；`******    1 imaginary frequencies (negative Signs) ******` **@L760**。
- 不构成模计数的两行：`Low frequencies --- -135.2576  -14.5718 ...` **@L758**、`1 imaginary frequencies ignored.` **@L956**。
- 虚模参数：**−134.4181 cm⁻¹**，Red. masses **1.1599**，Frc consts **0.0123** mDyne/Å，IR Inten **148.4689**。
- 组成（模 1 位移矢量逐原子 |v|²，按原始序）：**H(3) 98.87%**、O(2) 0.87%、H(11) 0.17%、其余合计 0.09%（C(6) 0.02%、O(7) 0.02%、H(8) 0.02%、Na(1) 0.01%、C(4) 0.01%、H(9) 0.01%、O(5) 0.00%、H(10) 0.00%）；**heavy_atom_fraction = 0.93%**。
- 方向判据：H(3) 位移方向 (−0.20, 0.02, 0.98) 与 O(2)–H(3) 键方向（单位化 −0.536, 0.833, −0.138）点积 **−0.0102 ⇒ 夹角 90.6°**：该虚模**不是** O–H 伸缩，而是**羟基 H 绕 O1 的扭转/摆动**（O1 几乎不动）。

### 36.3 判读与当前状态
- 命中 §34 锁定规则的**第 2 支**：「1 个虚模且模在 Na⁺/羟基上 ⇒ 立即停并回报主协调」。⇒ **RC 侧驻点在羟基 H 扭转方向上是负曲率点，未加约束意义下不是真极小值**。
- 因此本轮：**未改动 RC 参考**、**未提交 E1 尝试 1**（E1 的分母参考可能受影响，等主协调裁定）；RC 参考暂记 job 967 **−466.986564979**，并保留「≤0.4 kcal/mol 接触型构象 caveat」。
- 技术判断（仅供裁定参考）：虚模 −134 cm⁻¹ 与实模 50.45/97.18 cm⁻¹ 处于同一极软区间，属软的羟基扭转自由度；该自由度距反应坐标（O1···C6 = 2.801 Å 的加成方向）为旁观自由度，但**负曲率是真实的**（力判据全 YES）。
- 能量口径：本节只做本作业 SCF 与 job 1022 的同值对照（诊断），未跨作业/跨程序相减。

## 37 主协调裁定「甲」执行：E1 参照极小值重建作业 job 1031 已提交（2026-10-17 10:34:08 CST）

### 37.1 裁定与前置事实
- 主协调裁定 **甲**：从 job 1022 驻点沿 −134.4181 cm⁻¹ 虚模方向位移后做**一次普通 Opt+Freq**，尝试建立 RC 侧合格极小值作为 E1 候选参照态；这是 NY3 包**唯一**的手工作业。
- 平台实况（主协调只读实测）：job 1027 = done @10:30:32；平台自动提交 **job 1030 = ts/ts_0007/.../irc/irc.gjf（ready）** ⇒ ts_0007 再次被排队作业锁住 ⇒ **尝试 1（帧 A）在 1030 终态前无法提交**（不得试，否则重现 `active compute jobs prevent input revisions`）。
- 因此本轮不改 ts_0007 任何声明、不动 1030；尝试 1 仍待 1030 终态。

### 37.2 构造（全部机器生成，无手敲坐标）
- 源几何：`ts/ts_0007/jobs/declaration_0005/ts_opt/refine.log` sha **4bb4b94d2fe2fbdfbf1ae0eb0103031d4bf5e25bd3035ba4615da5f51fd54c2c**（13613 行），最后一个 `Input orientation:` **@L13411**、原子行 **@L13416–L13426**；末 SCF −466.986563802 @L13239。
- 模矢：`.../frequency/frequency.log` sha **385214fd76ee5f70bbc49a726968d35bb6ff05ccbb8888e470c1b746863b9c1c**，模 1 @L769，原子行 **@L773–L786**（11 原子，AN 与源几何逐位一致 11,8,1,6,8,6,8,1,1,1,1）。
- 标度 s = 0.30 / |v(H6)| = **0.30284** ⇒ |Δ(H6)| = **0.300 Å**；符号取 **H6 远离 Na⁺**：H6···Na **2.942 → 2.970 Å**（反号 2.944 Å，未用）。
- 自查：O1–H6 0.965 → **1.026 Å**；d(O1···C6羰基) 2.801 → **2.793 Å**；Na–O1 2.092 → 2.088 Å；Na–O7 2.409 → 2.406 Å；最小原子间距 1.026 Å（无塌陷）；位移 > 0.005 Å 的原子仅 O1 0.028／H6 0.300／H11 0.012 ⇒ 骨架未扰动。
- 原子序保持源序 Na, O, H, C(甲氧基), O(甲氧基), C(羰基), O(羰基), H, H, H(甲基), H(甲酰基)；**羰基碳在此序为 6（工作序的 C4）**，见 §36.1 警告。

### 37.3 文件与作业
| 项 | 路径 | sha256 |
| --- | --- | --- |
| 位移坐标 | `NY3/E1_refmin/e1_refmin_disp030.xyz` | aba124efa1be69c82d8f439ecfa7251d46742de0f6db30f26f1b9e26dffdd323 |
| Gaussian 输入 | `NY3/E1_refmin/e1_refmin_disp030.gjf` | 5e57dd8beb683307878c3630084aa3b94cfc0fa564a87e1efdcfc9c8e015a58a |
| provenance | `NY3/E1_refmin/E1_REFMIN_SEED_PROVENANCE.md` | 0c736de97501acdf02fcce64e2010991a8b1eb96d80fc4bf7d797c1894177501 |

- route（逐字，`qm_input_writer` 输出）：`#p opt freq B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=Water)`；`%nproc=8`、`%mem=10000MB`、电荷/多重度 `0 1`、11 原子（def2SVP 无连字符，issue #189）。
- **job 1031** 已提交：手工作业（NY3 唯一，手工在飞 1），priority 0，8 cpus / 10000 MB，本地 node-local，state=ready（队列满，等槽位）。

### 37.4 预先写定的判读口径
- 收敛且 **0 虚频** ⇒ 该几何 = E1 候选参照极小值（E_ref + 路径 + sha + 行号），先报主协调，再谈尝试 1/2 的 ΔE‡ 分母。
- 仍有虚频（1 或多） ⇒ **不得**作参照，报主协调并按「参照态未确立」处理。
- 时线：若「甲」或尝试 1 在 **11:30 CST** 前无法完成，E1 按「缺测 + 已证伪 + 参照态未确立（RC 为一阶鞍点 −134.4181 cm⁻¹）」入终稿（主协调按 partial 交付）。

### 37.5 措辞校正（主协调裁定）+ 硬时线提前（2026-10-17 10:35:07 CST）
- **符号口径（不返工，但必须如实记全）**：job 1031 起点采用 **sign = +1**：H6···Na **2.942 → 2.970 Å**（O1–H6 0.965 → 1.026 Å）；模矢行 `frequency.log` **L773–L786**（模 1，H6 X −0.20 / Z 0.97），标度 **s = 0.30284**，位移 **0.300 Å**。E1 道复算建议 **sign = −1**（H6···Na 2.9514 Å），两者差 ≤0.02 Å、E1 道自评「无区分度」⇒ **不返工**；但 §37.2/§37.4 与终稿**不得**写成「按 E1 道建议的方向」，必须写全符号与数值——本节即该措辞的更正登记。
- **1031 只是候选参照态**：即便 0 虚频，仍须先做身份核验才可报 E_ref —— Na⁺ 配位支须为 **支-RC**（Na 桥联 O1+O5、Na–O3 为远端）、O1–H6 回落到 ≈0.965 Å、d(O1···羰基碳) ≈2.80 Å；报 E_ref 必须同时给 **行号 + 日志 sha256**。1031 的电子能**只作候选参照能量，不是能垒**。
- **仍有虚频 ⇒ 参照态未确立**：不作 E1 的 ΔE‡ 分母，报主协调，按「参照态未确立」入终稿。
- **硬时线提前到 11:20 CST**（原 11:30）：届时 1031 未终态或判读未完成 ⇒ E1 按「明确缺测 + 已证伪 + 参照态未确立（RC 为一阶鞍点 −134.4181 cm⁻¹）」入终稿，**不再动任何计算、不再提交**；若 1030 在 11:20 后才终态，尝试 1 **不提交**，终稿如实写「尝试 1 因 1030 未终态未提交（1030 state=ready）」。
- **索引双写口径（升格为全局）**：终稿凡引原子一律双写「原始序 1-based」+「工作序/化学标签」；本包的 H6 一律写作「羟基氢（原始序第 3 原子 / 工作序 H6）」，避免被读成甲基 H。

## 38 job 1031 终态（**0 虚频**，身份核验通过）+ job 1030 IRC 失败 + **E1 尝试 1 已被接受（job 1034）**（2026-10-17 11:05:57 CST）

### 38.1 job 1031 终态测量（裁定甲的 Opt+Freq）
- 日志 `NY3/E1_refmin/e1_refmin_disp030.log` sha256 **ed579d010fc917856598fee6b769348e5b848ebcb99892152db5906e94d4cbb6**，**7974 行**，mtime 11:04:44；输入 `e1_refmin_disp030.gjf` sha 5e57dd8b…。
- `Optimization completed.` **@L6266**、`-- Stationary point found.` **@L6267**；`Normal termination of Gaussian 16 at Sat Oct 17 11:04:44 2026` **@L7974**（L6519 的终止行是 opt→freq 内部接续，非最终终止）。
- 末 SCF **−466.986564213 @L6122**（第 8 周期，opt 最后一步）；freq 段 SP 同值 **@L6826** ⇒ 能量自洽。
- **频率：band 表 9 行 × 3 = 27 模（3N−6）✓，全部为正值**，最低实模 **48.2631 cm⁻¹ @L7084**；**无任何负值、无 `imaginary frequencies` 行** ⇒ **0 虚频，是真极小值（在所用级别与网格下）**。
- `Low frequencies --- -14.1988 0.0008 0.0014 0.0015 5.1465 22.2088` @L7074：首个负值属**平移/转动数值残差**，非振动模（按锁定计数规则不计）。
- ZPE `Zero-point vibrational energy 192978.7 (Joules/Mol)` @L7271、`Zero-point correction = 0.073502` @L7282。

### 38.2 身份核验（§37.5 要求，全部通过）
| 判据 | 要求（支-RC） | job 1031 末帧实测 | 结论 |
| --- | --- | --- | --- |
| Na⁺ 配位支 | 桥联羟基 O + 羰基 O，甲氧基 O 为远端 | Na–O(羟基,原始序2) **2.092**；Na–O(羰基,原始序7) **2.410**；Na–O(甲氧基,原始序5) **4.258**（远端） | **支-RC ✓** |
| 羟基 O–H 回落 | ≈0.965 Å | O(2)–H(3) **0.965** | ✓ |
| d(O1···羰基碳) | ≈2.80 Å | O(2)···C(6) **2.800** | ✓ |
| 骨架其他键 | 与 RC 同档 | C6=O7 1.222、C6–O5 1.329、C4–O5 1.436 | ✓ |

- **E_ref（候选参照极小值）= −466.986564213 Ha**（@L6122／@L6826，日志 sha 见 38.1），几何 = `e1_refmin_disp030.log` 末帧 `Input orientation` @L6636。
- 与 RC（job 967，−466.986564979）差 **+6.6×10⁻⁷ Ha ≈ +0.0004 kcal/mol**（**诊断值，不相减**）⇒ 位移-弛豫后回到同一个 RC 侧极小值，但**现在有频率证据（0 虚频）**，RC 本身从未做过 freq。
- 结论：**E1 的参照极小值已确立**（`E_ref = −466.986564213`，freq 验证 0 虚模，支-RC）；job 1022/1027 的驻点（一阶鞍点 −134.4181 cm⁻¹）**不被采用**为参照。

### 38.3 job 1030（平台自动提交的 IRC）失败 —— 解除了 ts_0007 的锁
- `Normal/Error`：**Error termination via Lnk1e in /home/ly/g16/l123.exe at Sat Oct 17 11:02:48 2026**；`Delta-x Convergence NOT Met` / `Maximum number of corrector steps exceded`（原文拼写）。
- 日志 `ts/ts_0007/jobs/declaration_0005/irc/irc.log`；ts_inspect 记录的 input sha **1e2610bd9d355b92bf24492c1ae2c80c9e145bea277769e14678dde57c969281**、log sha **69d39d6eec5b03306f1e2ce44ac19676d46bdbc7d53d7ff6c6bc469ebb29ddde**。
- ts_0007 因此进入 `blocked`（failure_class=job_failed，stage=refine），rev=78，`next.action=resume`。

### 38.4 E1 尝试 1 已被接受（ts_0007 唯一授权的 guess 组修订）
- 调用：`ts_resume(run_id='ts_0007', changes={guess:{kind='provided', xyz_path='gold_finish_20261015/NY3/E1/e1_tsguess_revscan_p6_reactantorder.xyz'(sha 9ee4e847…), evidence_refs=['gold_finish_20261015/NY3/E1/E1_REVSCAN_P6_FRAME_A_PROVENANCE.md'(sha 8dc2c267…)])})`。
- **回执（逐字要点，request_key tc_290eb3b0bc5c44ea）**：previous_revision **78 → 79**，previous_input_revision **5 → 6**，changes = `['guess.evidence_refs','guess.xyz_path']`（**只改 guess 组**，符合授权）；
  - **retained**：`candidate_opt/attempt1/job 967`、`product_seed_opt/attempt1/job 985`（两个端点参照保留）；
  - **invalidated**：`ts_opt/attempt1/job 1022`、`frequency/attempt1/job 1027`、`irc/attempt1/job 1030`。
- 运行态：status=waiting，stage=refine，**新管线作业 job 1034**（ts_opt，declaration_0006，8c/10000MB，state=ready）——**管线作业，不计入手工配额**（手工在飞 0）。
- 时间：11:05:35 CST 接受（远早于 11:20 硬时线）。

### 38.5 近简并 caveat（主协调要求并入，本轮实测复核）（2026-10-17 11:07:32 CST）
- **结论句口径（终稿必须同句出现）**：`E_ref = −466.986564213`（job 1031，0 虚频）**只是候选参照**，且**必须与 job 1027 的 1 虚频驻点（−134.4181 cm⁻¹）近简并这一事实同句标注**；**不得**写成「RC 附近存在一个明确的极小值」。
- **本轮实测的近简并读数（我自己的测量，非转述）**：
  - 能量：E_ref(1031) **−466.986564213**（@L6122／@L6826）vs job 1027 freq 段 SP **−466.986563802**（frequency.log @L510）⇒ Δ = **−4.11×10⁻⁷ Ha ≈ −0.00026 kcal/mol**（1031 更低；**仅诊断，不相减**）。
  - 几何（内坐标级）：13 对近距离原子中的最大差为 **0.0054 Å**（H3···C6 3.591 vs 3.596 Å）；其余键长差 ≤0.003 Å。
  - 几何（逐原子级）：未对齐时最大 **0.4172 Å**；质心对齐后最大 **0.3414 Å**，全部落在**原始序第 3 原子 = 羟基氢（工作序 H6）**上，其余原子 ≤0.16 Å（质心对齐后 ≤0.10 Å 量级）。
  - ⇒ 两点之差**几乎完全落在羟基扭转这个软坐标上**（正是 −134.4181 cm⁻¹ 那个模），骨架相同。故「极小 vs 鞍点」在本级别处于**数值噪声边缘**：0 虚频只能按 §37.5「判据只看本几何自身的 band 表 + imaginary 行」成立，不可外推到邻居。
- 由此 E1 的「缺什么」按主协调收窄版登记：**缺「一个 1 虚频且模矢以 O1–C4（羟基 O···羰基 C）为主的一阶鞍点」+「双向连通性」**；起点极小值问题已由 1031 关闭（带上述 caveat）。
- job 1034 若在 11:20 之后终态，只作「超出终稿窗口、供后续参考」补录，不改正文。

## 39 E1 截止 11:20 CST 状态（硬时线登记，终稿按缺测交付）（2026-10-17 11:19:14 CST）

### 39.1 已确立的事实
- **E1 参照极小值已建立（带近简并 caveat，见 §38.5）**：`E_ref = −466.986564213 Ha`（job 1031，@L6122 opt 末 SCF／@L6826 freq SP），**0 虚频**（band 表 27 模全正，最低实模 48.2631 cm⁻¹），身份核验 **支-RC**（Na–O羟基 2.092／Na–O羰基 2.410／Na–O甲氧基 4.258 远端；O–H 0.965；O···C羰基 2.800）；日志 `NY3/E1_refmin/e1_refmin_disp030.log` sha256 **ed579d010fc917856598fee6b769348e5b848ebcb99892152db5906e94d4cbb6**（7974 行）。**必须同句标注**：与 job 1027 的 1 虚频驻点（−134.4181 cm⁻¹）近简并（ΔE = −4.11×10⁻⁷ Ha；内坐标差 ≤0.0054 Å，逐原子差 0.4172 Å 全落在羟基氢）。
- **E1 尝试 1 已被 ts_resume 接受**（11:05:35 CST，request_key tc_290eb3b0bc5c44ea）：previous_revision **78 → 79**、input_revision **5 → 6**、changes = `['guess.evidence_refs','guess.xyz_path']`（只改 guess 组）；**retained** candidate_opt/job 967、product_seed_opt/job 985；**invalidated** ts_opt/job 1022、frequency/job 1027、irc/job 1030。
- 由此产生管线作业 **job 1034**（purpose=ts_opt，declaration_0006，source_input_revision 6，8c/10000 MB）；**管线作业，不占手工配额**（手工在飞 **0**）。

### 39.2 硬时线时刻的作业状态（本轮实测，非推断）
- **11:19:03 CST 实测**：`ts/ts_0007/jobs/declaration_0006/ts_opt/refine.log` **尚未生成（NO_LOG_YET）**；队列 running = 1008／1017／1032／1033，queued = **1034 @ pos 1**；`query_compute_job` 侧 1034 state = **ready**（未起跑）。
- `ts_inspect(ts_0007)`：revision **85**、status **waiting**、stage **refine**、waiting_for = job 1034（ts_opt，state ready）。

### 39.3 E1 的交付定性（缺测）
- **E1 没有可验证的 ΔE‡**：缺「一个 1 虚频且模矢以 O1–C4（羟基 O···羰基 C）为主的一阶鞍点」+「双向连通性」；起点极小值问题已由 job 1031 关闭（带 §38.5 近简并 caveat）。
- **尝试 2（构造 A，`E1/e1_tsguess_attempt2_o1shift_reactantorder.xyz` sha 4327d465…）从未提交**，原因：尝试 1 的结果在硬时线前不可知（job 1034 仍 ready 未起跑），且 11:20 后不再提交任何作业。
- E2／E3 定性不变：缺测 + 缺什么（build 阶段位移判据过不去，#195）+ 已证伪（1007／1011／1012／1016／1019／1024／1025 + xTB 帧 0／14 + 1014 IRC l123）；另外 **1030（ts_0007 的 IRC）l123 失败**亦为本包已证伪链的一环（Delta-x 未收敛／corrector 步数超限）。
- job 1034 若在本登记之后终态，**只作「超出终稿窗口、供后续参考」补录**，不改正文。

### 39.4 交付面与冻结状态（本轮实测）
- ΔE‡ 已验证 **0/3** ⇒ **backfill 保持冻结**：`cloudra/benchmark/normal_registry/yo.py` **dc58b4f5a01738c96001c32fcf913899d79cd00098e30909cfc83716ad0aefc8**、`ideapool/reaction_candidates/normal.md` **771a6c7ffa23a358ed8b35005c31d64931530d2f6aeb54c7ecc568e5c0fbdc89**、`ideapool/tasks/normal/NY3.json` **4e7e754e23272578572359c127115cfd039efe02bc08a055575fc647c3857f3e**、`tests/test_benchmark.py` **037a424b05cc5d28f0bd2540af456aedf034908d5e59525b356994d38bd8d014** —— 四者均与冻结值一致，**零改动**。
- 引擎声明：本轮全部能量由 **Gaussian 16** 产生（B3LYP/def2SVP + GD3BJ + Int(UltraFine) + SCF=Tight + CPCM(Water)），**Gaussian 16 替代原定 ORCA**；能量只允许在**同一 Gaussian 批次内**相减，绝不与历史 ORCA 值混算。

### 39.5 addendum（窗口外终态，只读补录；不改正文、不改交付面）（2026-10-17 11:40:30 CST）
- **job 1034（E1 尝试 1 的 ts_opt，declaration_0006）终态 = 失败**：日志 `ts/ts_0007/jobs/declaration_0006/ts_opt/refine.log` sha256 **279a4f20a5cf35258e6f7ffcd16ffcd4ddbc6b2c36237fa68c76c5826dfb49c8**，**21902 行**，mtime **11:38:08**。
- `-- Number of steps exceeded,  NStep=  45` **@L21663**（`Optimization stopped.` **@L21662**）；`Error termination request processed by link 9999.` **@L21898**、`Error termination via Lnk1e in /home/ly/g16/l9999.exe at Sat Oct 17 11:38:08 2026` **@L21899**。
- 末判据 **@L21656–21660**：Max Force **0.004568 NO**／RMS Force 0.001263 NO／**Max Disp 0.678686 NO**／RMS Disp 0.170783 NO ⇒ 距收敛很远，不是「已收敛但判据略差」。
- 能量：末 SCF **−466.985339017 @L21528**（第 45 步）；相对 E_ref（−466.986564213）**+1.225×10⁻³ Ha ≈ +0.77 kcal/mol**（**仅诊断**：跨步/同批次张量不同步，且该结构不是驻点）。
- 末帧几何（`Input orientation` @L21712）：**d(O2···C6羰基) = 2.383 Å**（起点 guess 2.1771 Å，RC 2.800 Å ⇒ 沿反应坐标**退回**而非前进）；Na1–O2 2.119、Na1–O7(羰基) 2.392、**Na1–O5(甲氧基) 3.395**（起点 2.307 ⇒ Na⁺ 配位在两个分支之间重排中）；O2–H3 0.967、C6=O7 1.220、C6–O5 1.334。
- **判定**：尝试 1 **未给出任何驻点**（无 Stationary point found、无频率），**不构成 ΔE‡**；其失败模式 = 固定步预算（45 步）内未收敛 + Na⁺ 配位/反应坐标同时重排（与 #191–#195 同族）。E1 的缺测定性（§39.3）**不变**，且本条并入已证伪链：`attempt 1 ts_opt NStep=45 截断，r(O···C)=2.383 Å 退回，末判据全 NO`。
- **尝试 2 未提交**：窗口（11:20 CST）已过，按硬时线规则不再提交；构造 A 材料（`E1/e1_tsguess_attempt2_o1shift_reactantorder.xyz` sha 4327d465…）留档备后续。
- 本轮只读：未提交任何作业、未改 ts_0007 声明、未动交付面四文件（dc58b4f5… / 771a6c7f… / 4e7e754e… / 037a424b… 仍为冻结值）。















