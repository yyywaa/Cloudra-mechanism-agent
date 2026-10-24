# PROCESS — Cloudra 机理项目共享进度记录

> 本文件为项目级共享记录。各 Agent 在自己的任务段内追加/修正，勿整篇覆盖他人较新的记录。
> 约定：区分「直接观测」= 从实际计算输出读出；「假设」= 待检验；「结论」= 已被独立证据支持。

## 跨道（E2 ↔ 协调者）已核准的记法约定
- 记录构象变化必须写全「**原子集 + RMS + max|Δ| + 最差原子号**」（Kabsch/SVD、det=+1、位移取逐原子欧氏范数）：例 heavy20 0.9859 / 1.5271 / a28；all-41 1.2336 / 2.1911 / a39。这两组数已由本 lane 与 E2 面板表 lane 独立复算一致、协调者登记台账 §R191，为**双签值，可直接进报告脚注**。
- 提醒：本 lane 曾把「对齐后逐原子位移的单轴分量最大值 1.712 Å」误标为 max|Δ|，该数已撤回；RMS 1.234 本身无误（all-41）。引用时一律按上一行的四元组格式。
- 剖面结论措辞上限：「**已覆盖段内无内部极大**」；未采样区不得外推，一维剖面不得写成「该剖面无峰」。
- 凡跨构象分支的能量一律不拼接、不作 TS、不作势垒上界、不写 ΔE‡；HI1_E2 的 result / barrier 保持 null。

## HI1_E2 一维受约束扫描（R(C1···C29)，DMSO/CPCM，B3LYP/def2SVP+GD3BJ，UltraFine）

### 直接观测（原始日志读数，已与协调者独立复算逐位一致）
- 首轮扫描 job 1075（maxstep=8，B 1 29 S 14 −0.2000）收敛 8 点后于 scan point 9 死于 l103「New curvilinear step failed: FormB failed.」/「Error imposing constraints」（[日志](gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan.log) 末尾 L103879 附近）。8 点 ΔE（参照 −939.308205969 Eh）= 0.00/0.13/0.76/1.88/3.11/4.06/5.09/6.60 kcal/mol，单调上升（分支 A）。
- 续扫 job 1076（[输入](gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan_cont1.gjf) maxstep=6、B 1 29 S 4 −0.1000，起点 = 上轮第 8 收敛帧几何）5/5 点全部收敛，[日志](gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan_cont1.log) L79310 正常终止（termination 1 / Error 0），sha256 4445b098…，无任何 l103 报错。逐点 ΔE = +6.6004 / +3.5977 / +4.5592 / +5.7832 / +7.3156 kcal/mol（R=2.9543/2.8543/2.7543/2.6543/2.5543）。
- 末次 SCF 锚点：L3257 / L55438 / L67269 / L72050 / L77656；收敛块 L3625 / L55826 / L67653 / L72418 / L78025；几何块 L3023 / L55204 / L67050 / L71800 / L77422。
- 逐点表与行号由 [分析脚本](gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan_cont1_analyze.py) 生成；该脚本在首轮日志上复现出与人工读数一致的 8 点 ΔE 与 R 值（0.00…6.60），可作为读数口径的交叉校验。
- 质子：12 个点全部 H24 留在羧基 O11 上（R(11,24) 0.9847→0.9984，R(28,24) 1.8425→1.7716，协调者另测 R(4,26) 3.4167→2.8896），无质子转移，质子档恒为档 0。

### 假设 / 已登记的分支切换（关键分歧点）
- 续扫在 2.9543→2.8543 这一步发生构象分支切换：heavy20 RMS 0.9859 / max 1.5271 / a28；all-41 RMS 1.2336 / max 2.1911 / a39（其他相邻步仅 0.058–0.125 Å）；dih(C1,C2,C29,O28) 由 −145.4° 变 +151.9°、dih(C2,C1,C29,C30) −92.7°→−157.9°；R(2,29) 4.039→3.742；E 反降 3.00 kcal/mol。
- 因此：main-scan 的 8 点（分支 A）与 cont1 的 pt2–pt5（分支 B）不是同一条约束极小路径；pt1 计支 A（与主扫 pt8 同几何：ΔE 9e-9 Eh、rmsd 0.0003 Å），绝不计支 B。
- 2.9543 处「+6.60 高于 +3.60」是分支滞后造成的表观极大（假峰）：不作 TS、不作势垒上界、不写 ΔE‡。B 分支自洽序列（以 2.8543 为 0）= 0.00 / +0.96 / +2.19 / +3.72 kcal/mol，单调上升。
- 检验方案（**均未授权、配额为零，不得起作业**；已登记于协调者台账 §R190 第 5 条）：①优先——以分支 B 的 2.8543 几何为初猜做 R(1,29)=2.9543 的约束单点优化（1 个几何即可定量分支能量差）；②其次——cont2 从 2.5543 反向扫描（B 1 29 S 4 +0.1000）回到 3.35，检验 B 分支在 2.95–3.35 是否仍低于 A。

### 模型条件与边界（明确记录）
- 隐式 DMSO（CPCM）、电荷 0 / 单重态、C15H21NO4、41 原子；无显式抗衡离子或助剂，未含温度/浓度/频率热化学。
- 已覆盖段 = A 分支 2.9543–4.3543 Å（8 点）+ B 分支 2.5543–2.8543 Å（4 点）；2.5543 Å 以远未采样，剖面仅一维。
- 未改动交付面文件（FINAL_DELIVERY_DRAFT.md、11 个交付文件、HI1.json、hi.py），未触碰其他边与他人题源，未 kill 任何作业、未改 priority。
- Hub 帖：提交帖 evt_3e06810e02674c13、结果帖 evt_b1aff52b8b2e4c8f、口径更正与登记确认 evt_00b26a2345254280（协调者回复 evt_fe1c3a83c3f642ab），主题 gold-finish-20261015。

## 2026-10-18 裁决后的 HI1 / HL1 补算线（本 lane；记录面，不含结论）

### 裁决口径（引自主协调帖，非本 lane 自定）
- 成模判据三步：**(a) 方向硬闸门**（虚频模在声明 watch pair 上的净位移方向须与 gold 的 bond_changes 同向；相反 = pseudo-saddle 永不回填）；**(b) 成分记录项**（报反应中心对 / 该模重原子 / 最大单原子位移三份额，不设百分比阈值，最大份额落在 spectator 即写 soft-mode-dominated）；**(c) 交付判据**（同程序同方法、TS 一虚频 + 双向 IRC 到端点 + 两端 Opt/Freq 0 虚频，且与本步自身起点极小值相减）。
- 车道：NR1 / NY3 归另一会话（gold_fill_20261018/NR1、/NY3），本 lane 只做 HI1（E1b / E4 / E5 / EM1）与 HL1_E1。最多 5 槽、8 cpus/作业、priority 0，不 kill job 1074。
- NI5_E1 = 0.93 的对外表述固定为「同批 G16 全链齐备、值已回填、BRIEF ①② 未满足」，不得写「验收通过」。

### 直接观测（本轮实测，可复核）
- **历史 ts run 不可 resume**：ts_inspect("ts_0016" / "ts_0012" / "ts_0020") 三次均返回 is_success=false，逐字 "ts_inspect: TS run not found in the authorized project and workspace" ⇒ 这些 run 属旧会话/旧工程，本 lane 只能以文件 guess 新建 ts_prepare，不能就地延长 IRC。
- 盘上题源与 10-17 冻结表已不同：ai.py 822b898a…、normal.md 1ee4b83e…、tests 07e616f5…；NR1_E1 的 0.0 已被回退为 null（ru.py 6a20f6a7… 无 barrier 键）。以上均非本 lane 写入。
- 队列（2026-10-18 02:5x–03:0x 实测）：running 1074（HI1 E3b 2D 扫描）+ 1080/1081/1082（NR1 道），32 cpus 占满、free cpus = 0，1083 排队。

### 已有的关键证据（供各道引用；带 sha 前缀，引用须回原日志核行号）
- HI1_E4 候选 TS：ts/ts_0016/jobs/declaration_0007/frequency/frequency.log（c5ac8402…）L1501 imaginary、L1510 = −783.7914；同 run irc.log（0f9679f9…）双向各 10 点被 maxpoints 截断（L9503 / L18200 / L18232 Total 20）。
- HI1_EM1 候选 TS：ts/ts_0012/jobs/declaration_0002/frequency/frequency.log L1541 imaginary、L1550 = −314.2861，E = −939.283734374（L857）；同 run irc.log（dfc4d3ec…）L25166 l123 失败。
- HL1_E1：ts/ts_0010 .../frequency/frequency.log（9074df80…）L864 = −67.9886（甲基转动 = pseudo-saddle）；受约束剖面 round4/T3_ptscan_H2O9_relaxed.log（40ce3be2…）20/20 点，pt8 = B + 3.5705（仅下界）；pt8 guess 见 round4/T3_scan_peak_pt8_ts_guess.xyz（7018f688…）。

### 派道（本 lane）
- HI1_E4（E3a）连通性补算：session as_59169f6989874877，工作目录 gold_fill_20261018/HI1/HI1_E4/
- HL1_E1（pt8 鞍点归属）：session as_eb687a63ebb243bd，工作目录 gold_fill_20261018/HL1/HL1_E1/
- HI1_E1b 脱水 TS：session as_e38fb7c615094945，工作目录 gold_fill_20261018/HI1/HI1_E1b/
- HI1_EM1 连通性 + 产物端：session as_fae50a6580774668，工作目录 gold_fill_20261018/HI1/HI1_EM1/
- TaskSpec 草案（只写文档，不建 gold 数值）：as_03036138773c45e1（N_FORMAMIDE、N_HNCO_HYDROLYSIS）、as_d742ca478b2e4257（H_COPE_ELIMINATION、H_HCNO_NORBORNENE），产出目录 gold_compute/queue_20261018/specs/

### 假设（待各道日志检验，勿当结论）
1. HI1_E4 只差「IRC 到达端点」一环（TS 与两端 0 虚频已具备）。
2. HI1_E1b 分母（carbinolamine_27 = job 1051 = −593.929762803）成立，只差 C2–O4 断裂 / C2=C3 形成的协同鞍点。
3. HI1_EM1 的 −314.2861 若方向与声明副面产物一致，则只缺 IRC 与产物端 Opt+Freq。
4. HL1_E1 的 pt8 若给出落在 [1,2]/[2,9] 的虚频模，则 0.0 的约定口径可升级为真实鞍点，或被正式否定。

### HI1_EM1（副面通道）· 本道进度（as_fae50a6580774668，目录 gold_fill_20261018/HI1/HI1_EM1/）

- **直接观测（2026-10-18T03:0x）**：候选 TS 的两个原生文件已自算 sha 一致 —— [frequency.log](ts/ts_0012/jobs/declaration_0002/frequency/frequency.log) a471aa7b…（L1541 恰 1 虚频、L1550 = −314.2861/33.5499/44.0361、E = −939.283734374 @L857、117 模、L5340 正常终止）；[refine.log](ts/ts_0012/jobs/declaration_0002/ts_opt/refine.log) 66691e0e…（L24549/L24550 收敛驻点，末次 SCF −939.283734374 @L24183 = 与 freq 同值，L25650 正常终止）。
- **直接观测（(a) 方向硬闸门在该驻点上成立）**：由 freq 模向量重算（[analyze_mode.py](gold_fill_20261018/HI1/HI1_EM1/build/analyze_mode.py)），C3–C6(1,29) 净投影 −1.109 = 缩短、C2=C3(2,1) +0.166 = 拉长、C6=O5(28,29) +0.177 = 拉长，与题源 bond_changes 同向（另 C2=N20 −0.070 缩短）。(b) 份额：反应中心原子 {1,2,4,28,29} 0.6665、heavy 0.6951、最大单原子 = 原子 1(C3) 0.3282（落在反应中心，非 spectator）。
- **直接观测（CIP 口径坑）**：RDKit 3D 判定若**保留 atom-map 号**会把 Cα(8) 判成 R，strip map 后为 **S**（同一几何、同一拓扑）；本道一律 strip map（[cip_check.py](gold_fill_20261018/HI1/HI1_EM1/build/cip_check.py)）。TS 几何 CIP = Cα(8) S / C6(29) R，与副面通道声明一致。
- **提交**：旧 run（ts_0012 及其 IRC）不属本授权工程 ⇒ 按新 run 走：[ts_prepare 回执](gold_fill_20261018/HI1/HI1_EM1/build/TS_SEED_PROVENANCE_EM1_JOB1032.md) **run_id ts_0025 / job 1088（ts_opt，ready 排队）**，种子 = job 1032 收敛帧 xyz（sha 663fe231…，41 原子、d(1,29)=1.8791 Å、与 refine.gjf 坐标 maxdev 0.0000 Å，无重排）。verification.irc 显式 MaxPoints=140 / StepSize=5 / Recalc=20（针对旧 IRC 的 10 点截断 + l123 Delta-x 不收敛）。
- **未完成 / 缺什么**：ts_opt → freq → 双向 IRC → 两端 Opt+Freq 全部尚未跑（机器 free cpus=0，作业排队）。**ΔE‡ 仍未取得**（参考态固定 job 924 = −939.308218263 Eh）。任何数值在 IRC 双向到达端点前一律 candidate_only。

### HI1_E1b（HI1_E2，半缩胺脱水 → 烯胺 + H2O，27 原子子系统）· 本道进度（as_e38fb7c615094945，目录 gold_fill_20261018/HI1/HI1_E1b/）

- **直接观测（原子序/物种，核对已完成）**：27 原子工作序 = `INT1_27_opt_frame.xyz` 序（sha b2f2ffaa…）：1=C1 甲基、2=C2、3=O4、4=C3、5-7=H@C1、8/9/10=H@C3（10=H22）、11=O13、12=C14、13=O15、14-17 环 C、18=N20、19=H@O15、20-26 环 H、27=H21；元素序列 C8H15NO3、q0/m1，与 `hi.py` 第 2 步 reaction_center（工作序 form (2,4)/(3,10)、break (4,10)/(2,3)）逐条对上。分母 = [INT1_27_optfreq.log](gold_finish_20261015/HI1/E1/split/INT1_27_optfreq.log)（sha c03e0a82…，L26615/L28142 E=−593.929762803，L26904 Stationary point，L28588-28589 75 模 0 虚频、最低实模 78.1638）。
- **产物端没有现成原生日志**：盘上只有 41 原子 `I1_S_start.xyz`（sha c9d59aea…）+ 含键 MOL，其 provenance 明确「不主张极小值」；27 原子烯胺+水的 Opt/Freq 必须由本次 run 自算。
- **假设（待 freq/IRC 检验）**：C2–O4 断裂 / C2=C3 形成 / H22 迁移可以走一个协同四中心鞍点。几何自查给出的张力事实：C2 距 C3···O4 直线仅 0.86–1.2 Å，因此协同构造里 H22 必然贴近 C2（guess 中 C2···H22 = 1.595 Å，C3-H22···O4 = 152.8°，其余非键最近 H···H = 1.77 Å，无 <0.5 Å 撞原子）。若 freq/方向否决，则结论应写成「协同四中心不可行」，改判分步（先断 C2–O4）或羧基穿梭（本 27 原子模型里羧基此刻离 H22 有 5.4 Å，帮不上，需另立模型）。
- **提交**：[guess provenance](gold_fill_20261018/HI1/HI1_E1b/TS_GUESS_PROVENANCE.md)（插值参数 + minsep + 原子表；构建脚本 build/build_final.py）→ ts_prepare 新建 **run ts_0026**，reaction.selected_candidate=0（C1/C3 在反应物图里对称，平台给出 2 个同分候选），execution 4 cpus / 6144 MB；**job 1092 = ts_opt（opt=(TS,calcfc,noeigen) B3LYP/def2SVP+GD3BJ/UltraFine/CPCM(DMSO)），ready 排队**。IRC 段另设命名配置 g16_irc（IRC=(CalcFC,MaxPoints=80,StepSize=5,Recalc=10)）。
- **中途修正（保留记录）**：guess v1 因构建脚本索引笔误（3-1 应为 4-1）把旁观 H8/H9 平移出 2.5 Å，绑定的 job 1091 几何含两个游离 H；已重新生成并 ts_resume 换 guess（job 1092），现每个 H 距母原子 0.97–1.10 Å。教训：minsep 自查必须包含「每个 H 的最近重原子」，不能只查反应对。
- **未完成 / 缺什么**：ts_opt → freq（恰 1 虚频 + (a) 方向 + (b) 三份额）→ 双向 IRC → 两端 Opt+Freq + 身份；**ΔE‡ 未取得**，现在任何数值都只能写 candidate_only。

## NY3 · 单水中性水解 HNCO + H2O → NH2COOH → NH3 + CO2（本道；目录 gold_compute/queue_20261018/results/NY3/）

方法（题面固定，未改）：Gaussian 16，B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight，气相 q0/m1 闭壳层；资源 4c/6144MB、priority 0。原生日志全部留在 results/NY3/jobs/，未删未覆盖。

### 直接观测（本道实测；E 为纯电子能 / Ha）

| 驻点 | job | E | 虚频 | 判定 |
|---|---|---|---|---|
| I1 syn 氨基甲酸（H7···O2 = 2.288 Å 分子内氢键） | 1133 | -244.966495972 | 0（15/15 实频） | 已验证极小值 |
| 同上（ts_0028 反应物端 freq） | 1157 | -244.966496071 | 0 | 与 1133 一致（6e-8 Ha），端点身份成立 |
| I2.xyz 起点（题面“反式 O–H”几何） | 1134 | -244.953252173 | 1（-272.9714） | opt 收敛但非极小值，D1 端点不合格 |
| 反式 O–H 最小（沿 -272.97 模位移 ±0.40 后重优化，两方向收敛同一结构） | 1163 / 1169 | -244.953791465 / -244.953791466 | 0 | 已验证极小值（H7···O2 = 3.016 Å） |
| ts_0028 TS（I1 → 反式旋转体，构象边） | 1112 + freq 1129 | -244.948872987 | 恰 1（-465.6897） | 驻点成立 |
| 同上 IRC 双向 | 1130 | 端点 -244.951863 / -244.953593 | — | 各 10 点、未到端点（bothconv=false） |
| HNCO·H2O 预络合物（R_complex.xyz 直接优化） | 1132/1139 | -244.934373855 | 2（-212.1, -38.6） | 非极小值 |
| HNCO·H2O 预络合物最小（沿 -212 模位移后重优化，N3–H4···O5 = 1.802 Å） | 1152 | -244.935406907 | 0（15/15） | 已验证极小值 |
| 同上沿 -38.6 模位移 | 1153 | — | — | opt l9999 未收敛，失败尝试，不采用 |
| 两性离子 H3N⁺–COO⁻ 猜测（N–C 1.50 Å） | 1136 | -244.9640755 | 1（-20.5，NH3 转动） | 优化后 C1–N3 = 2.754 Å、N 上 3×H(1.02 Å)、两个 C–O 1.164 Å ⇒ 解离成 NH3 + CO2；本水平未找到两性离子驻点 |
| NH3···CO2 产物复合物（MMFF 起点） | 1164 | -244.958065 | — | opt l9999（PES 极平，MaxDisp 0.05 不降）；重试 job 1168（CalcFC/MaxCycle=200）进行中 |

### ts_0028 的 D1 三环（实测，不设阈值）
- (a) 方向：虚频 -465.6897 的未加权平方位移份额：原子 7(H) 0.9704、原子 6(H) 0.0168、5(O) 0.0056；top pair (6,7)=0.6659、(3,7)=0.4709、(4,7)=0.3925、(2,7)=0.3700。该边为构象边（两端同一物种，reaction_center 为空、bond_changes 为空），故无“同向/反向键变化”可判；如实记为空，不捏造断键。
- (b) 成分：反应中心份额 = null（未声明 watch pair）；全重原子份额 0.007674；最大单原子 = 原子 7 (H) 0.9704；基数 = 未加权平方位移（非质量加权）。
- (c) ΔE‡：TS − 本步自身起点 I1（job 1157，-244.966496071）= +0.017623 Ha ≈ +11.06 kcal/mol；相对反式端最小（job 1163）= +0.004919 Ha ≈ 3.09 kcal/mol。两端 Opt+Freq 均 0 虚频（I1：1133/1157；反式：1163/1169）。

### 判定 / 假设（分开写）
1. 直接观测：**ts_0028 终局 verdict = verified（verified=true）**。过程：首轮 verdict 为 candidate_only，理由是“declared SMILES vs built MOL 身份核对不一致（两端几何感知 SMILES 都是 NC(=O)O）”；按工具契约把反应式改成**无原子映射的同一 SMILES（NC(=O)O）**、并给两端显式 seed（反应物端 = job 1133 的 I_syn 极小值、产物端 = job 1163 的 I_anti 极小值）后重跑（ts_opt 1174 → freq 1176（1 虚频 -465.6897）→ 两端 opt/freq 1177/1178、1183/1184 全部 0 虚频），IRC 复用 job 1130 原生日志（declaration_0006/irc/existing.log，未改动）。ΔE‡ = TS(-244.948872987) − I_syn(-244.966495972) = +0.017623 Ha = **+11.06 kcal/mol**。
2. E1（协同 vs 两性离子分步）：唯一直接证据是“两性离子猜测在本水平不驻留，直接滑到 NH3 + CO2（job 1136）”，与单步协同 4 中心加成相容；但 E1 的 TS/IRC 属 ts_0027（他道，当前 status=blocked），故不宣称已核实，登记为待 ts_0027 的 TS + 双向 IRC 定案。扫描峰/受约束剖面一律不作势垒。
3. 题面给的 I2.xyz“反式旋转体”几何其实是 NH2 面外化方向的鞍点（-272.97）；真正的反式极小值仅低 0.34 kcal/mol，但“是否 0 虚频”是 D1 端点的分水岭。

### 平台问题（非科学失败，已登记）
- 05:08–05:12 期间 submit_compute_job(job_type=gaussian) 间歇性在 admission 被拒（PATH is missing … g16）：失败 1132/1135/1140/1154/1155/1156/1160/1161，成功 1133/1134/1136/1139/1152/1153/1163/1168/1169，同批交错出现，重试即通过。未改平台代码、未 kill、未改 priority。

## NR1 · 甲酰胺气相脱水 NH2CHO → HCN + H2O（协调者本道；目录 gold_compute/queue_20261018/results/NR1/ 与 ts/ts_0032…ts_0035）

### 直接观测（实测；E 为纯电子能 / Ha；B3LYP/def2SVP+GD3BJ+UltraFine+SCF=Tight，气相）

| 物种 | job | E/Ha | 虚频 | 几何判据 |
|---|---|---|---|---|
| 甲酰胺 R（SMILES NC=O） | 1121（NR1/jobs/R_formamide_optfreq.log，3398 行，sha 5351eb3a…，L3209 Stationary point found） | -169.772982663 | 0（12 模） | C=O 1.2207、C–N 1.3588、N–H 1.0097/1.0117（N 上 2H）、C–H 1.1019、O 上无 H |
| INT-1a（甲亚胺酸构象 A） | 1123 | -169.751090026 | 0（12） | C=N 1.265、C–O 1.341、O–H 0.974 |
| INT-1b（构象 B） | 1124 | -169.745424789 | 0（12） | C–O 1.352 |
| INT-1c（构象 C） | 1125 | -169.744844814 | 0（12） | C–O 1.357 |
| 第 4 个甲亚胺酸构象 D | 1126 | -169.741299945 | 0（12） | 与 A/B/C 均不同；四个构象两两差 >1.3 kcal/mol |
| HCN | 1127 | -93.3535186313 | 0（4 模，含 764.99 双重简并） | 线性 |
| H2O | 1128 | -76.3588896845 | 0（3 模） | — |
| HCN···H2O 复合物 | 1213（NR1/jobs/NR1_P_complex_optfreq.log） | -169.720742486 | 0（12 模，最低 47.48/53.29 cm-1） | 松散复合物，相对分立产物结合能约 5.2 kcal/mol |

| TS | run / jobs | E/Ha | 虚频 | ΔE‡（TS − 本步自身起点） | verdict |
|---|---|---|---|---|---|
| tsH-1,3（R ↔ INT-1a，成键步） | ts_0032：ts_opt 1205 / freq 1206 / IRC 1207 / 端点 1210+1214、1215+1216 | -169.699169421 | 1（-1897.6514） | 46.32 kcal/mol（-0.073813242 Ha；起点 = 甲酰胺 job 1210 = -169.772982663） | verified=true（swapped pairing，interval proof 通过） |
| tsR-1a1b（INT-1a ↔ INT-1b，构象边） | ts_0033：ts_opt 1143 / freq 1148 / IRC 1172 / 端点 1196+1198、1200+1202 | -169.714755466 | 1（-991.8673） | 22.80 kcal/mol（起点 = 1196 = -169.751090026；反向 19.25） | verified=true（direct pairing） |
| tsR-1b1c（INT-1b ↔ INT-1c，构象边） | ts_0034：ts_opt 1145 / freq 1149 / IRC 1173 / 端点 1187+1190、1192+1194 | -169.733877738 | 1（-508.3050） | 7.25 kcal/mol（起点 = 1187 = -169.745424733；反向 5.67） | verified=true（swapped pairing） |
| INT-1c-tsH2O（INT-1c → HCN+H2O，成键步） | ts_0035 | 未定 | 未定 | 未定 | 进行中，见下 |

### D1 (a)(b) 实测（份额基数 = 未加权平方位移，非质量加权；阈值为约定值）
- ts_0032：虚频 -1897.6514 位移份额 原子5(H) 0.9732、原子4(H) 0.0201、C 0.0026、O 0.0017；reaction_center（1 基）= (1,5),(3,5)；mode_alignment = aligned：pair(1,5) 相对位移 1.002、pair(3,5) 0.998，阈值 0.50×全局最大 1.033 = 0.517；pair 投影 0.758 / 0.846。
- ts_0033：虚频 -991.8673，原子4(H) 0.9758、N1 0.0169；top pair (4,6)=0.551、(3,4)=0.340；构象边（reaction_center 空），alignment 按规则 skip。
- ts_0034：虚频 -508.3050，原子6(H) 0.9326、原子5(H) 0.0443；top pair (4,6)=0.657、(5,6)=0.431；构象边，alignment skip。

### 关键坑（本轮实测，可复用）
1. IRC 声明形状：calc 的 keywords 只能写电子结构设置；任何 irc= 令牌都会被 admission 判 keywords mismatch（ts_0032 declaration_0006/0007 matched=false，declaration_0008 matched=true）。IRC 选项写 end_setting，但 end_setting 不进 route，Gaussian 用默认 10 点上限（三条 IRC 均 10 点/方向），方向证据靠逐帧距离表 + 两端 Opt+Freq + interval proof 补齐。
2. 端点 verify 必须给完整 calculation 对象（engine/method/basis_set/keywords 全写）；给 ref 会被判 missing_input: Explicit calculation required。
3. reaction_center 必须按实际迁移氢声明：ts_0032 最初按 SMILES 0 基映射填 (1,4),(3,4)，而 IRC 逐帧距离显示搬家的是 H5（N1–H5 1.042→1.792、O3–H5 1.811→0.995、N1–H4 恒 1.017）。改成 (1,5),(3,5) 后 alignment=aligned、verdict 由 candidate_only 变 verified。逐帧脚本 NR1/logs/irc_geom_dump.py。
4. 端点槽会被 IRC 标签自动指派：无显式 seed 时 ts_0032 把通向甲亚胺酸的臂放进 reactant 槽，导致 identity/interval 全错；给显式 seed（该物种已核验极小值 + 日志）后修复。

### 失败尝试（保留，不作结论）
- ts_0035 的 xTB path：默认 100 次被截断（path_not_converged，31 s，纯算力上限）→ 提到 400 次给出 guess，但 ts_opt（job 1182）停在第 24 步未收敛（Max Force 0.00096 vs 阈值 0.00045），末帧 C–O 2.3209、N–H4 1.0279、O3–H4 2.4004，H4 没搬、O 上只有 1 个 H ⇒ guess 落在化学错误区，不是「无 TS」。
- 一维松弛扫描沿 O3···H4（NR1_tsH2O_scan_OH.gjf，job 1203）在 l103 FormBX 失败：平面分子 dihedral 5-2-3-6 退化。用 internal_coordinates transform 把 H6 绕 C2–O3 旋 35°（geoms/INT1c_twist35.xyz，无键/角异常）后的 v2（job 1212）重跑。
- job 1208 / 1209 / 1211 的 failed 均为 exit_code = -15（.cloudra/calc-*.exit.json）⇒ 调度终止（SIGTERM），不是科学失败；已重提为 1212 / 1213 / 1214。

### ts_0035 的一维扫描读数（job 1212；O3···H4 约束，其余自由；能量相对 INT-1c = -169.744844814）

| O3···H4 / Å | E / Ha | 相对 INT-1c / kcal·mol-1 |
|---|---|---|
| 2.3992 | -169.744844814 | 0.00 |
| 2.2868 | -169.744197625 | 0.41 |
| 2.1743 | -169.742218670 | 1.65 |
| 2.0619 | -169.738771281 | 3.81 |
| 1.9495 | -169.733658682 | 7.02 |
| 1.8370 | -169.726622798 | 11.43 |
| 1.7246 | -169.717338404 | 17.26 |
| 1.6122 | -169.705413159 | 24.75 |
| 1.4997 | -169.690427107 | 34.15 |
| 1.3873 | -169.672113907 | 45.63 |
| 1.2749 | -169.650950080 | 58.91 |
| 1.1624 | -169.696759436 | 30.14 |

⇒ 峰在 O3···H4 ≈ 1.22 Å，峰高约 60 kcal/mol（约定阈值，非文献界）；与 SI 的 INT-1c→TS 差 59.1 kcal/mol 量级一致。扫描剖面**不作势垒**，只用来给 TS guess：取 R(3,4)=1.2749 那一帧（N1–H4 1.170、C2–O3 1.414、N1–C2 1.246、O3–H6 0.970）写成 provided guess（geoms/tsH2O_guess_fromscan.xyz），ts_0035 的 ts_opt = job 1217。该点 12 个扫描点中第 12 点超步未收敛（Multi-step exit l9999），只用已收敛点的读数。

### ts_0035 的二维网格读数（job 1223；坐标 = C2–O3 与 N1–H4；起点 INT1c_twist35；18/36 点收敛后 l9999 中止，只登记已收敛点）

能量相对 INT-1c（-169.744844814），单位 kcal/mol；行 = C2–O3 / Å，列 = N1–H4 / Å：

| C2–O3 / N1–H4 | 1.028 | 1.229 | 1.429 | 1.629 | 1.830 | 2.030 |
|---|---|---|---|---|---|---|
| 1.357 | 12.4 | 34.4 | 56.4 | 75.6 | 91.6 | 103.8 |
| 1.558 | 31.5 | 11.4 | 24.2 | 46.5 | 68.7 | 88.0 |
| 1.758 | 44.5 | 67.0 | 89.1 | 49.8 | 47.1 | — |

判定（观测与推断分开）：
- 观测：C2–O3 = 1.357 一行随 N1–H4 单调上升（+12→+104），即只拉 N–H 不拉 C–O 不是反应方向。
- 观测：C2–O3 = 1.558 一行在 N1–H4 = 1.229 处出现明显洼地（+11.4），两侧升高（+31.5 / +24.2）——「C–O 已部分拉开 + H 处桥位」的局部谷，不是鞍点。
- 观测：C2–O3 = 1.758 一行在 N1–H4 = 1.429 处为局部极大（+89.1），到 1.629 又降到 +49.8。
- 推断（未证实）：真正的鞍点应在这两个特征之间的脊线上（C2–O3 约 1.6–1.8、N1–H4 约 1.4–1.5、O3–H4 约 1.2–1.4），该分辨率不足以直接给出，需沿脊线加密。
- 该网格 36 点只收敛 18 点后因单点超步（NStep=24）整作业 l9999 中止；网格点一律不作势垒，只作 guess 定位。

### ts_0035 后续试验（进行中）
- job 1222（峰区 Hessian 探测，几何 = tsH2O_guess_fromscan.xyz）：E = -169.650950084，虚频 -137.9179（H6 0.873 / H4 0.110，逐键投影 ≤0.021），其余最低实频 85.17 ⇒ 峰区点在最软方向上是 H2O 转子脊，不是 H 迁移鞍点。
- job 1232：从网格 r14 几何（C2–O3 = 1.758、N1–H4 = 1.228、O3–H4 = 2.554）出发，沿 O3···H4 2.554→1.050 做一维松弛扫描（12 步），用于在「C–O 已拉开」前提下定位 H 迁移的峰。

### 判读警示：约束扫描的极大 ≠ 一阶鞍点（NR1 tsH2O 实例，本轮实测）
- 观测：一维 O3···H4 约束扫描在 O3–H4 = 1.275 Å 处出现能量极大（E = -169.650950084，相对 INT-1c = +58.9 kcal/mol）；该几何 N1–C2 1.246、C2–O3 1.414、N1–H4 1.170、O3–H4 1.275、O3–H6 0.970。
- 观测：同一几何的解析 Hessian（job 1222）最低**实频** 85.17 cm-1，唯一虚频 -137.9179 属 H6（份额 0.873，逐键投影 ≤0.021）⇒ 迁移方向是**正曲率**。
- 推断：该极大是**约束造成的伪极大**，不是一阶鞍点。凡「沿某内坐标扫描出峰」，都必须用峰处 Hessian 的曲率核一次（迁移方向是否负曲率），再决定是否起 OptTS；只凭扫描峰起 OptTS 会滑到别的软模（本轮已两次滑到 O–H 转子）。
- 口径：扫描剖面/网格点永不写成势垒；NR1 的 INT-1c-tsH2O（e4）在拿到一阶鞍点之前 ΔE‡ 保持 null。

### NR1 收尾读数（2026-10-18 05:44）
- job 1232（只约束 O3···H4、C–O 自由，12 点）：2.554 → -169.743718（+0.71）；2.428 → -169.744807（+0.02）；2.303 → +0.30；2.178 → +1.60；2.052 → +4.04；1.927 → +7.80；1.802 → +13.10；1.677 → +20.25；1.551 → +29.60；1.426 → +41.46；1.301 → +57.56；1.175 → +198.3（末点严重应变，约束伪影）。日志原文 `Step number 25 out of a maximum of 25 on scan point 12 out of 13`（route `opt=(modredundant,maxstep=10)`，无 maxcycle）。
- 网格 pt17 / pt18 帧实测：pt17 N–C 1.178、C–O 1.758、N–H4 1.830、O–H4 0.991、O–H6 0.975；pt18 N–C 1.177、C–O 1.758、N–H4 2.030、O–H4 0.980、O–H6 0.975 ⇒ 已到「N≡C + H2O」的产物侧结构（C–O 被冻住），不是鞍点。
- 结论：TS4 本轮未定位（四次尝试全部记录），E / 虚频 / ΔE‡ = null；文本已固化在 `results/NR1/REPORT.txt` 第四节、`BACKFILL_PROPOSAL.md` 第三节、`CURRENT_STATE.md` 缺口行。
- 若继续：二维约束加密到 C–O 1.6–1.8 × N–H 1.4–1.7，且 modredundant **必须显式 maxcycle=200**（本轮 1223/1232 都是被默认 24/25 步上限砍掉）。

## NY3 成键步 TS（ts_0027 = E1 RC→I_syn；ts_0029 = E3 I_syn→NH3+CO2）——本轮接管记录

目标：只做两条成键步 TS/IRC，不重算已完成驻点；方法沿用 B3LYP-D3BJ/def2SVP + UltraFine + SCF=Tight、气相 q0/m1、4c/6144、priority 0。

### 起点（不改动，只引用）
- RC 预络合物极小值（N3–H4···O5 = 1.802 Å）：gold_compute/queue_20261018/results/NY3/geoms/NY3_R_complex_min.xyz（job 1152，E = -244.935406907，0 虚频）
- I1_syn 氨基甲酸极小值：.../geoms/NY3_I1_syn_min.xyz（job 1133/1157，E = -244.966495972，0 虚频）

### 本轮做法（与 D64 一致）
1. 不新建 run：用 ts_resume 改 guess 指向"约束优化后的 guess 几何"。
2. guess 准备作业（guess_prep/）：只冻结目标成键距离的 opt=modredundant，其余全部自由弛豫：
   - E1：冻 C1–O5 1.95 / O5–H6 1.35 / N3–H6 1.45（迁移氢 H6 处桥位；H7 摆出平面破平面简并）
   - E3：冻 C1–N3 1.95 / O5–H7 1.40 / N3–H7 1.40（迁移氢 H7 处桥位；H4/H6 旋出平面破平面简并）
   起点几何是手工构造的（C1–O5 2.0 / 环闭合），仅作输入，不作证据；最终 guess 取约束优化 log 的末帧（compute-derived）。
3. ts_opt 用工具默认 opt=(TS,calcfc,noeigen)；出 freq 后按 D58 先核转子，再双向 IRC + 两端 Opt+Freq。

### 未定/风险（诚实登记）
- E1 的 4 元环 C1–O5–H6–N3 因 C1–N3 只有 1.21 Å 而受几何约束：迁移氢无法完全到位（C1···H6 ≥ 1.9 要求 N3···H6 ≈ 1.4–1.5），故 guess 里质子转移略滞后于 C–O 成键；真实鞍点由 eigenvector following 定。
- E3 产物端 NH3···CO2 是极平复合物，历史三次尝试（1164/1168/1181）均未给出 0 虚频极小值；若端点 opt/freq 再次失败，按题面口径以分量（NH3 1179 + CO2 1180）注释并如实登记缺口。
- 路径口径：任务书写的是 results/NY3/...，仓库里实际目录是 gold_compute/queue_20261018/results/NY3/（无 results/NY3）；本轮所有文件写在后者，REPORT/mechanism_graph 追加在同一处。

### 本轮实测（2026-10-18 05:46–05:56）

| 边 | 步骤 | job | 结果 |
|---|---|---|---|
| E1 (ts_0027) | guess 约束优化 v2 | 1235 | 收敛；C1–O5 1.95 / O5–H6 1.35 / N3–H6 1.45 三键均 Frozen 命中；E = -244.863795213（guess_prep/E1_guessprep_opt_v2.log） |
| E1 | ts_opt | 1237 | Stationary point found；E(TS1) = **-244.876786249**；几何 C1–O5 1.718 / O5–H6 1.210 / N3–H6 1.309 / C1–N3 1.301 / C1–O2 1.179 |
| E1 | freq | 1240 | **恰 1 虚频 -1579.3842 cm-1**，H6 份额 0.957；watch pair 逐键投影 (5,6)=0.880、(3,6)=0.819 ⇒ 远大于转子阈值，非转子；mode_alignment = aligned |
| E1 | IRC | 1241 | 双向各 10 点。F 臂：O5–H6 1.164→0.991、N3–H6 1.353→1.698、C1–O5 1.724→1.835（回预络合物侧）；R 臂：N3–H6 1.266→1.031、O5–H6 1.256→1.690、C1–O5 1.713→1.645（去氨基甲酸侧）⇒ 连接正确 |
| E3 (ts_0029) | ts_opt | 1239 | 收敛（氨基甲酸侧起点） |
| E3 | freq | 1242 | **恰 1 虚频 -1656.9651 cm-1**，H7 份额 0.977；watch pair (5,7)=0.892、(3,7)=0.811 ⇒ 非转子；aligned |
| E3 | IRC | 1243 | 双向各 10 点。F 臂：N3–H7 1.224→1.030、O5–H7 1.346→1.780、C1–N3 1.606→1.673（去 NH3+CO2 侧）；R 臂：O5–H7 0.990、C1–N3 1.539（去氨基甲酸侧）⇒ 连接正确 |

关键失败模式（两条边都遇到，已定位并修复中）：
- **端点槽被自动指派到错误 IRC 臂**：ts_0027 的 reactant_endpoint 取自带 F 侧的点，自由优化又滑回氨基甲酸 -244.966496，身份核验失败；ts_0029 同样。修法 = 给显式 seed（kind:file + xyz_path + evidence_refs），reactant 端用已验证极小值（E1→RC 1152；E3→I1_syn 1133）。重跑 job 1249 / 1255。
- guess-prep v1（1233/1234）失败原因：end_setting 的前导换行让 Gaussian 把 ModRedundant 段读成空段（log 127 行后为空），实际做成了无约束优化；v2 用 B 1 5 F 紧跟坐标块后的单个空行 + route opt=(modredundant,maxcycle=200) 修好。

ΔE‡（纯电子能，1 Ha = 627.509474 kcal/mol）：
- E1：TS1 − RC = -244.876786249 − (-244.935406907) = **+0.058620658 Ha = +36.79 kcal/mol**
- E3：TS3 − I1_syn = 待 ts_0029 的 TS 能量 grep 后填。

### 端点修复（本轮两条边的共同失败模式，05:56–06:00）
1. **端点槽方向错**：ts_0027/ts_0029 的 reactant_endpoint 都被自动指派到产物侧的 IRC 臂，自由优化后落到氨基甲酸（ts_0027 得 -244.966496），身份核验失败 → 显式 seed 修复。
2. **未映射 SMILES 身份核对**：把反应式从原子映射 SMILES 改为未映射 SMILES（ts_0027：N=C=O.O → NC(=O)O；ts_0029：NC(=O)O → O=C=O.N）是 ts_0028 已验证过的修法；改动会清空 reaction_center 与 guess，必须在同一次 resume 里重新声明，否则 assemble/guess 会 blocked。ts_0029 改完还出现 CO2 两个等价 O 的映射歧义，选 candidate 0（恒等 atom map）解决。
3. **NH3···CO2 产物复合物确有干净极小值（新结果，推翻旧登记）**：job 1136 的 -20.6233 cm-1 虚频是 NH3 绕 N···C 轴的扭转；把该虚频模 ±0.5 位移后重优化（job 1261，guess_prep/P_rotp_optfreq.log）得 **E = -244.964075631，15 个全实频，最低 7.01 cm-1**，几何 gold_compute/queue_20261018/results/NY3/geoms/NY3_P_min_1261.xyz。旧的三次失败（1164/1168/1181）是 guess 方位未沿虚频模跟随所致。

- E3：TS3 − I1_syn = -244.897758392 − (-244.966495972) = **+0.068737580 Ha = +43.13 kcal/mol**


### 2026-10-18 06:0x 协调 lane 更正与分工（附证据路径）

**NR1（甲酰胺脱水，gold_compute/queue_20261018/results/NR1/）四处更正**
1. 编号对照：Gaussian/xyz 序与题面 atom-map **不一致**——Gaussian 1 N ≡ map 3、2 C ≡ map 1、3 O ≡ map 2、4 H(N) ≡ map 6、5 H(C) ≡ map 4、6 H(O) ≡ map 5（题面 SMILES [H:5][O:2][C:1]([H:4])=[N:3][H:6]）。本 lane 写 H4 = N–H、H6 = O–H，回填不得照抄序号。REPORT.txt L39 原写「两套一致」已改正。
2. 甲酰胺 R 几何：REPORT.txt L40 原记 C=O 1.2207 / C–N 1.3588 等是**旧输入几何**读数，作废。以本步分母 job 1210 实测：C2=O3 1.2097、C2–N1 1.3604、N1–H4 1.0117、N1–H5 1.0145、C2–H6 1.1200；证据 ts/ts_0032/jobs/declaration_0011/reactant_opt/reactant_opt.log 的 Standard orientation 块 L688–694，能量 L436 = −169.772982663。
3. E1 分母构象：同一几何 dih(H4–N1–C2–O3) = −180.0°、dih(H5–N1–C2–O3) = 0.0° ⇒ 一个 N–H 与 C=O 同侧 = **syn 甲酰胺**，满足「分母须 syn」；反侧构象未计算，只能写未算。
4. e4 二维窗口更正：旧窗口「C–O 1.6–1.8 × N–H 1.4–1.7」错。job 1223 实测低能谷在 C2–O3 = 1.558 行、N1–H4 = **1.229**（相对 INT-1c +11.4），同行邻点 1.03 → +31.5、1.43 → +24.2；N–H 1.4–1.7 侧是 +24…+46 爬坡面。正确窗口 = C2–O3 1.50–1.65 × N1–H4 1.10–1.35。REPORT.txt L58 已改写。
- REPORT.txt 仍 62 行，sha256 **e462adace10c0f3206051395fb97372ad6784f233e5ee4505dec3d9b69207102**（改前 df3f0eec…，旧 sha 作废）。

**NR1 e4 委派**：交 small_mol 会话 as_ebc2eac267254580，本 lane 不再自行提交 e4。起点 geoms/INT1c_twist35.xyz（sha 817115dd…，H6 绕 C2–O3 旋出平面以避 l103 FormBX）；job 1247 = C2–O3 {1.550,1.600} × N1–H4 {1.08…1.24} 共 10 点、opt=(modredundant,maxcycle=200)、4c/6144MB/p0；第二轮 15 点。判读：同一行只动 N1–H4，谷 ⇒ 无桥位；脊点且 O3–H4 ∈ 1.3–1.6 ⇒ 桥位候选；桥位候选帧先 Hessian（报 O3–H4/C2–O3/N1–H4 三个净投影），虚频仍属 H6 转子即判「仍非目标鞍点」并停。INT-1c 几何 geoms/opt/INT1c.xyz sha 00baf536…、E = −169.744844814（job 1125）。

**NY3 归属**：ts_0027/0028/0029 归 results/NY3/ 那条道；gold_fill_20261018/N_HNCO/ 即日停手（不 resume、不写输入、不换初猜），其 STATUS.md 与 evidence/E1_profile.md 只作方法学对照原地保留。预算按 lane 记。交付面统一 results/NY3/。

**NY3 端点归属规则（本 lane 定的判据，供 NY3 道执行）**：三个 0 虚频极小值 #1244/1245、#1246/1248、#1249/1250 中谁充当某步分母，**不能按能量高低或名称定**，须按「该步 IRC 对应臂末帧几何 与 候选极小值几何 的 RMSD」定：报 RMSD 数值 + 最大单原子偏差 + 叠合原子集；RMSD 最小者才是该臂的端点。若最小 RMSD 仍 > 0.3 Å 或身份（N3/O5 上氢数）不符，说明该极小值不在该臂盆地，须延长 IRC 或重优化，不得直接当分母。E1 的化学身份要求：reactant = HNCO + H2O（分离或预络合物，N3:1H、O5:2H），product = 氨基甲酸（N3:2H、O5:1H, C1–O5 ≈1.36）。

**HL1 exo/endo 定名**：采纳 specialist 自认更正——HL1_P_exo_optfreq.log(#1228) 真身份 endo、HL1_P_endo_optfreq.log(#1229) 真身份 exo、#1226/#1227 互换、ts_0036=endo、ts_0037=exo；依据 = 日志 smiles 行 + sdist/d(C10,C18)，文件名不作依据。行号：P SCF Done L6281 = −441.098273660 / L6306 = −441.095689093，d(输入7,C18) = 3.0459 / 3.7066，判据式 REPORT.txt:13。ts 侧 refine.log 内**无** isoxazoline 字样（grep 0），面标签只在 P 端日志，故「ts 侧标题行」不再作证据。未决：ts_0036/0037 自身 sdist(C18) 待算（框架 n = (0.461998,0.373382,−0.804452)、u = (0.594986,0.542159,0.593342)、w = u×n）。另：HL1 新增 #1251/#1252 两片段参考（降冰片烯、HCNO）属**结合能基准**，不得当能垒或选择性使用。

**HI1**：底物 Opt+Freq 已收敛——HI1_erythro_R_optfreq.log L8082、E = −598.229013613；HI1_threo_R_optfreq.log L8184、E = −598.231556225（freq 段 05:52 仍在算）。两值不得相减做能垒（不同非对映底物）。

**全批口径**：(c) 一律写「短 IRC 方向区间（10 FORWARD + 10 REVERSE）+ 两端 Opt+Freq 0 虚频 + interval proof」，显式标「替代口径」，原因 #184；k = 627.509474；巡检按 ts_00xx / job id；spec（TASKSPEC_N_FORMAMIDE.md）单一写权归 writer。

### e4 第一轮网格（job 1247）结论与下一轮（06:1x）
- 实测：Gaussian 把约束展开成 C2–O3 {1.550,1.600,1.650} × N1–H4 {1.08…1.28} 共 17 个不同点（报 18 个 Optimization completed，末点重复），全部 2–6 步收敛。相对 INT-1c（−169.744844814）的指示值：1.550 行 +14.13→+28.95、1.600 行 +16.65→+33.77、1.650 行 +21.68→+38.79，**三行沿 N1–H4 全部单调升**；O3–H4 全部落在 2.46–2.54 Å。
- 判读：**不是 C2–O3 行不够密**，而是这个二维子空间缺关键自由度。INT-1c 的 dih(H4–N1–C2–O3) = **0.0°**（H4 与 O3 在 N=C 上同侧 cis；此值由 small_mol 实测复核，本 lane 先前把它写成 180° 是错把 INT-1a 的值移用，已更正），O3–H4 远达 2.46–2.54 Å 的原因是 ∠N1–C2–O3 ≈ 122° 把 O3 从 C2 向外张出，而不是二面角反位；只拉 N1–H4 等于把它往远离 O 的方向拽。能拉近 O3–H4 的自由度是 **∠N1–C2–O3 的角闭合**（四元环 N1–C2–O3–H4 需该角从 122° 收到 ~70–90°）。本轮**无桥位候选帧**，未起 Hessian/OptTS。
- 已批准并交 small_mol 执行（各 1 作业，4c/6144/p0，opt=(modredundant,maxcycle=200)）：A = O3–H4 2.30→1.30（6 点）× C2–O3 {1.650,1.750}，N1–H4 自由；B = dih(H4–N1–C2–O3) 180°→0°（步长 30°，7 点，C2–O3 固定 1.60）。
- 合并判据：O3–H4 ∈ 1.30–1.60 且 dih ∈ 100–170 且 C2–O3 ∈ 1.65–1.90 ⇒ 桥位候选，对该帧 calcfc，报 O3–H4 / C2–O3 / N1–H4 / dih 四个净投影；虚频若仍是 H6 转子（参 job 1222 的 −137.9 cm⁻¹、H6 份额 0.873）即判「仍非目标鞍点」并停。
- 文件：NR1/E4_GRID.md 43 行 sha 9a22956034a2f32ec6539afb6eac899ebb6cf62d40bf794a29802a5ba7699baf；NR1/jobs/E4_GRID_r2x5.log 16177 行 sha a567b1dcb748bbbd9d3b5761bf08fc09aa6139305a46c3259edde68fe568fd21；gjf sha 52a0656e508249ba0cd7666a234bcd514d78f25d72a194c1d59db9d9a7fbc9f4。

### HL1 面选择性参考态口径（协调 lane 定；不再用「各面自带 RC」当各面分母）
- **两面共用同一个分离参考** E_ref = E(降冰片烯 opt) + E(HCNO opt) = **−441.013264959 Ha**。已核：HL1_ref_HCNO_optfreq_b.log L1556 SCF = −168.452546517（L1979 Stationary，7 模 3N−5，Low frequencies L1747/1748，无虚频，最低实模 16.57）；HL1_ref_norbornene_optfreq_b.log **SCF Done L4295 = −272.560718442**（L3840 的 −272.560717675 是 opt 中间帧，不可用；freq 段 L5300 同值），Stationary L4509/L6257，Frequencies -- 15 行 = 45 模 = 3N−6，Low frequencies L5598/L5599，**0 虚频、最低实模 257.12 cm⁻¹**，Normal termination L6730（05:57:47）。**更正**：此前写「norbornene freq 尚未出、用 −272.560512015」是抓了 05:56 的日志快照（作业 05:57:47 才结束、freq 段其后落盘），该判断与数值均作废。
- 理由（两条硬事实）：#1226（C10 同侧）收敛的是很松的 vdW 接触（sdist(C18) +3.342、起点 +2.78 往外漂、d 3.663 Å），结合能量级 1–2 kcal/mol；#1227（C10 反侧）的 RC 因内坐标退化（L18772 Tors failed 21-18-19-20 / FormBX，线性 HCNO 扭转退化）已用刚性线性 HCNO 重建（#1253，opt=(cartesian,maxcycle=200)）。两条面的 RC 非同源，不能各自相减。
- RC 结合能另行列，注明**未做 BSSE/CP 校正**（def2SVP 下可能虚高 1–2 kcal/mol 量级），不得进选择性数字。
- 能量—文件映射（我自己 grep 核对；文件名 endo/exo 与真实通道相反，引用必须写「文件 + 行号 + 通道」）：HL1_RC_exo_optfreq_v2.log L23359 = −441.019015104、Stationary L22376；HL1_RC_endo_optfreq_v2.log 末 SCF L18708 = −441.020073887、无 Stationary、freq 计数 0。
- sdist 符号约定：HL1 取「n0 或 −n0 使 sdist(C10) > 0」，最终报告只保留一套 n，并注明与 BUILD_PROVENANCE 的 n_old 差一个整体负号（C10 同侧 = n 正侧 = n_old 负侧）。C10 = 工作序号/坐标块序号 7 = 题面 map10（序号 10 是 H，此前按序号 10 算出的 d = 4.13/4.33 作废）。

#### HL1 RC 与 TS-endo 实测（06:2x）
- RC（文件名 HL1_RC_exo_optfreq_v2.log，真实通道 = C10 同侧）：E = −441.019015104（opt 末帧 L22033、freq 段 L23359），Stationary L22376，Normal termination L22912 与 L25307（05:57:17），57 模，Low frequencies L23719/L23720，**0 虚频、最低实模 6.3314 cm⁻¹**（极软分子间模）。结合能 = −0.005750145 Ha = **−3.61 kcal/mol**（未做 BSSE/CP，caveat，不进选择性）。
- TS-endo（ts_0036）：refine.log Stationary L18331、Normal termination L18853（05:58:13），E = **−441.002183678**（L18090）⇒ 相对 E_ref 的 ΔE‡ = **+6.95 kcal/mol（预备值，待 freq 定稿，不进图）**；相对 RC 的对照值 +10.56（只作对照，不作选择性分母）。freq 作业 1267 在跑，须核「恰 1 虚频 + 成键对 (18,1)/(20,2) 逐键投影 + 单原子份额 < 0.90」。
- 教训（本 lane）：日志快照 ≠ 作业终态。判定「某段没跑」前须先确认作业已终止（末尾含 l9999 archive + 最后一条 Normal termination），不能只用一次 grep 计数。

### NR1 e4 第二轮（A / B'）与曲率先验帧（06:3x–06:4x）
- **两条新判据（本 lane 定）**：
  1) **能量下界**：产物复合物 HCN···H2O 已有实测（job 1213，E = −169.720742486，12 模、0 虚频），相对 INT-1c（−169.744844814）= **+15.12 kcal/mol**。路径为 0 → TS → +15.12，故 TS 能量必然 ≥ +15.12；任何候选帧 ΔE < +15.12 直接排除，不必做 Hessian。
  2) **撤回 ∠C2–O3–H4 = 90–130° 的护栏**：该体系是面内应变型四中心消除，实测该角上限 66°（在 ∠N1–C2–O3 95°、N1–H4 1.35、C2–O3 1.85 下），45–70° 才是正常值。替代护栏：O3–H6 保持 0.96–0.99、∠N1–C2–O3 ≥ 95°、四元环三角不等式。
- A（job 1263，O3–H4 2.54→1.34 × C2–O3 {1.65,1.75}）：两行随 O3–H4 减小单调升（1.750 行 +30.9→+69.8；1.650 行 +21.9→+61.6），行内无极值，∠C2–O3–H4 仅 47–62°。日志 20063 行 sha e0314f12…。
- B'（job 1264，∠N1–C2–O3 113.8°→70.3°，C2–O3 固定 1.60）：单调升，第 5 点（∠79.0°）已 +100.84，越过 +80 止损线（单作业算到底，如实登记）。日志 sha 136219fb…。
- 曲率先验帧（job 1282，freq）：按目标构帧（O3–H4 1.45 / N1–H4 1.35 / C2–O3 1.85 / 几何上限 ∠C2–O3–H4 65.9°），E = −169.598748866 = **+91.68 kcal/mol**；**3 个虚频**：−1291.60（迁移模：O3–H4 +0.747、N1–H4 −0.849、C2–O3 −0.081）、−579.39（纯面外，全平面帧的构造应变）、−222.60（C–O/N–H 混合环变形）；最低实频 588.57。日志 sha 534646a6…、帧 sha 690294dc…、E4_GRID.md 126 行 sha 30a8cdf4…。
- 判读：+91.68 帧证明「H4 由 N1 迁向 O3」这个方向在该几何上是负曲率，但该帧不是鞍点（3 虚频，两个来自构造应变），且能量远高于预期区。下一步 = 对该三距离做**受约束重优化**（opt=(modredundant,maxcycle=200)，冻结 O3–H4 1.45 / N1–H4 1.35 / C2–O3 1.85，不冻角度）以弛豫面外应变，再 freq 核是否恰 1 虚频（迁移方向）。若迁移方向也转正 ⇒ 构造应变假象，E4 收 null；若 OptTS 40 步内滑回 −508 cm⁻¹ 转子（job 1217 的同类失败）⇒ 不重试超过 2 次，转 dih × O3–H4 二维映射（C2–O3 固定 1.80，12 点）。
- 已知失败档案（避免重复）：job 1217（峰区帧 provided guess OptTS）滑到 −508.38 cm⁻¹、H6 份额 0.933；job 1222 峰区 Hessian 仅 −137.9（H6 转子）；job 1232 / 1223 均被默认步数上限截断。

## HI1 · threo/erythro N,N-二甲基-3-苯基-2-丁胺氧化物 Cope 消除（HI1 自算线；目录 gold_compute/queue_20261018/results/HI1/）

### 直接观测（B3LYP/def2SVP+GD3BJ+UltraFine+SCF=Tight，气相 q0/m1，4c/6144MB/prio 0）
- 两个**独立**底物极小值（各自 opt+freq，93 实频、log_parser imaginary=[]、opt 收敛）：
  erythro = C[C@@H]([N+](C)(C)[O-])[C@H](C)c1ccccc1 (2R,7R)，job 1224，E=-598.229013613（HI1_erythro_R_optfreq.log L9502，sha 9d6040a0…），最低实模 46.19 cm⁻¹；
  threo   = C[C@@H]([N+](C)(C)[O-])[C@@H](C)c1ccccc1 (2R,7S)，job 1225，E=-598.231556225（HI1_threo_R_optfreq.log L9616，sha ceb76390…），最低实模 37.58 cm⁻¹。
- CIP 由 3D 几何算（RDKit AssignStereochemistryFrom3D，**strip atom-map**）：build 几何与 QM 几何给同一结果。
- 相对构型判据 inv=[dih(N3,C2,C7,C9) − dih(C1,C2,C7,C8)]：erythro≈0°、threo≈±120°；先在 L-Thr(2S,3R)=+118.4°、L-allo-Thr(2S,3S)=−1.9° 上验证。实测 erythro +3.91°、threo −97.14°（QM 几何）。**threo 的 −97° 与理想 ±120° 差 23°，已如实登记**，定名以两个 CIP 标签 + Fischer 构造为准。
- 烯烃 E/Z 由 TS guess 几何二面角读（provisional）：erythro dih(C1,C2,C7,C9ipso)=−22.5°（C1 与 Ph 顺式，高优先基团同侧）⇒ **Z**；threo 对应 H18–Ph 顺式 ⇒ **E**。须在 IRC 产物端复读。
- 三条 durable 路径：ts_0038（erythro syn，ts_opt job 1286）、ts_0039（threo syn，1289）、ts_0040（erythro 区域异构 C1–H 抽取，1292）；**ΔE‡ 尚未取得**。

### 假设 / 待检验
1. 两条 syn 通道应给相反 E/Z；若 IRC 产物端几何与 guess 相反，以产物端为准改 E/Z。
2. 区域异构（3-苯基-1-丁烯 + Me2NOH）势垒应高于主通道（成烯仅二取代）；未算前不写理由。
3. 平台 mapping：主通道 map 阶段报 4 个对称候选，选 candidate 0（其 atom_map 把迁移 H25 映到产物 O–H）；区域异构那条 candidate 0 把 H16 映到烯烃 H（化学上不对，但重原子对应正确，已在报告注明）。

### 缺口
三条边的 ΔE‡、IRC 方向区间（10+10 点）与两端 Opt+Freq 全无；产物 E/Z 未在产物端复读；REPORT.txt / mechanism_graph.json 已先行落盘（PARTIAL，null + GAP 逐条）。

### 环境坑（可复用）
- 共享 3D builder 的 xyz 带尾列 ` in:N`，RDKit MolFromXYZBlock 直读报 "Cannot convert ... to double"，需先去尾列。
- MMFF `MMFFAddDistanceConstraint` 力常数 500 太弱（C2–N3 只到 1.76 vs 目标 1.95），2000–10000 才到位；反应中心过远时 MMFF BFGS 抛 "bad direction in linearSearch"，改用**纯几何刚性片段构造**。
- 事故记录：本道误将 PROCESS.md 覆写为空（write 传空内容），已从 .cloudra/tool_output/read-20261018-060419-d39370e7.log（06:04:19 的整档快照）原样恢复，sha 338412b7… 与覆写前一致，然后才追加本节。

### HI1 结论（2026-10-18 08:45 最终）
- **两条主通道均已 verified**：ts_0038（erythro syn：ts_opt 1286 / freq 1318 / irc 1321 / 端点 1328+1330+1332+1334）虚频 **−940.1938**（1 个）；ts_0039（threo syn：1289 / 1320 / 1323 / 1333+1335）虚频 **−1069.2742**（1 个）；两次 runtime verdict 都 verified=true。
- **ΔE‡（各自减自己的极小值，纯电子能）**：erythro = −598.208585697 −(−598.229013613) = +0.020427916 Ha = **+12.82 kcal/mol**；threo = −598.208059052 −(−598.231556225) = +0.023497173 Ha = **+14.74 kcal/mol**。两个底物极小值差 1.60 kcal/mol，只作记账，从未用于势垒或面选择性。
- **方向判据（投影标度＝沿键单位矢量 Å，Σd²=1，符号按 C7–H25 投影为正固定）**：erythro C7–H25 +0.9984 / O6–H25 −1.0528 / C2–N3 +0.1210 / C2–C7 −0.1234；threo +1.0034 / −1.0317 / +0.0942 / −0.1056；四对符号与 bond_changes 同向。份额 H25 0.9386/0.9594、重原子 0.0371/0.0269；单原子>0.90 但逐键投影 ~1.0 Å ≫0.001 ⇒ 不是转子。
- **E/Z 由 3D 读出**：erythro TS dih(C1,C2,C7,C9ipso)=−3.5° ⇒ C1 与 Ph 顺式 ⇒ **Z**（产物端几何重感知 C/C=C(/C)c1ccccc1.CN(C)O）；threo TS dih(C1,C2,C7,C8)=−5.5° ⇒ Ph 反 C1 ⇒ **E**（产物端 C/C=C(\C)c1ccccc1.CN(C)O）。孤立烯烃 opt+freq 1325/1326 均 0 虚频，E 比 Z 低 0.26。
- **构象歧义（登记）**：IRC 反应物端优化到更低构象（erythro −598.235079186 低 3.78；threo −598.233321696 低 1.13，均 0 虚频）⇒ 以更低构象为参照 ΔE‡ = 16.63 / 15.85。REPORT §1.6/§2.6 两值都在，图里边绑与 reactant 节点日志一致的那个。
- **区域异构通道未解决**：ts_0040（C1–H 抽取 → 3-苯基-1-丁烯）ts_opt 1292 在 Gaussian l9999 步数上限（169/169）失败 ⇒ barrier 留空，不写优选/未优选结论。
- 交付面：REPORT.txt 236 行 sha b794548b…、mechanism_graph.json 8 节点/3 边（12.82 / 14.74 / null）sha b4163eb9…。
- 第二次事故记录：08:47 我又用「read 全文 + write 回写」的方式追加（read 返回被截断到 4000 字符），把 PROCESS.md 截成 56 行；已用 .cloudra/tool_output/read-20261018-084554-e1f09f35.log（08:45:54 整档快照）cp 恢复，sha 0b73928a… 与截断前逐位一致，再用 edit 追加本节。教训：**read 无 limit 会截断，绝不能拿它做整档回写**；共享 Markdown 只能 edit 追加。

## HL1_E1（已归档为方法学对照，不再推进；本 lane 追加）

> 定位：题源替换后 HL1_E1 不再作为任何活跃题的 gold。本节只留**可复核的事实与失败档案**，不含 ΔE‡、不改题源。

### 三层锁定口径（04:45 冻结，逐字引用）
- **事实层**：−254.4556 cm⁻¹ 鞍点连通的是 B（O-质子化产物）↔ N-质子化肟+水；声明的「接触离子对 → O-质子化产物」这一步**未找到对应鞍点**。
- **口径层**：HL1_E1 的 ΔE‡ 不给；题源维持旧值 0.0 作历史条目（「无独立鞍点」的理由作废）。
- **禁用表述**：不得写成「该边整体不可算 / 物种不存在」——#1102/#1105 已证 N-质子化肟+水 在该级别是 0 虚频真实极小值，与「声明的步没有对应鞍点」是两件独立的事。

### 直接观测（行号与 sha 均可复核）
- TS 频率：`ts/ts_0022/jobs/declaration_0003/frequency/frequency.log`（sha d4f9171d2430f18620ef8100c091e632a36a824bc76e57656f60f8c4668f4aad）L850 `Frequencies -- -254.4556 48.8070 86.3945`，恰 1 虚频。
- 虚频模（独立复算，与协调者逐位一致）：模式块 Σd²=0.9972（未质量加权）；单位模矢净投影 O1–H2 −0.193、H2···O9 +0.496、**H4···N8 −0.705（全模最大）**、O1–H4 +0.084。三份额（0.9972 归一）{1,2,9}=25.4%、全重原子=5.1%、最大单原子 **H4=47.4%（0.4739）** ⇒ (b) 记「水质子摆动型，最大份额落在声明中心外的 H4」，不写「中心主导」。
- IRC：`ts/ts_0022/jobs/declaration_0004/irc/irc.log`（sha b2f2974677120745f1e060dcb286a7ce524749f1c96d0a4eaa39903212e741c8，9413 行，Normal termination L9413，04:06:08）。`IRC=(MaxPoints=60,StepSize=10)` **未生效**（route 回显无 maxpoints/stepsize、全文零命中，见 #184）；实跑默认 10 点/方向，Path 1 = FORWARD（pt0–pt10）、Path 2 = REVERSE（pt1–pt10）。
- 端点帧（程序化解析；元素序 1=O 2=H 3=H 4=H 5=C 6=C 7=C 8=N 9=O 10=C 11–19=H）：FWD pt10（L4538）O1–H2 1.2350 / H2···O9 1.1816 / H4–N8 2.2639 / O1···O9 2.3764；REV pt10（L8672）O1–H2 1.0019 / H2···O9 1.7259 / **H4–N8 1.5487** / O1–H4 1.0900 / O1···O9 2.4432。q' = R(H2–O9) − R(O1–H2)：FWD −0.0535、REV +0.7239 ⇒ 异号且 |Δq'| = 0.7774 > 0.5，两端帧分居两侧（约定阈值，自设/非文献界）。
- 反端 Opt 失败档案（两条独立运行、同种子，均**未达极小**）：
  - #1100（`declaration_0004/reactant_opt/reactant_opt.log`，sha 337ee9334fb50ae789641a16ee784edd2b5aac4b404c5ff843a0c9a9f9ea9d44）L17602 `Error termination via Lnk1e in l103.exe`（04:26:11），原文 `Bend failed for angle 1 - 4 - 8` / `FormBX had a problem.`；末次收敛表 L17207 四项全 NO；末次 SCF −364.330446174。
  - #1101（`gold_fill_20261018/HL1/HL1_E1/irc_endpoints/rev_outer/rev_outer_opt_fix1.log`，sha fd7450ea711c894ea855437fdc50c63ec0819dcb4e40e1952b1d6dbdcaa12bc5）04:29:17 `Tors failed for dihedral 3-1-4-8 / 1-4-8-7 / 1-4-8-9` → `FormBX had a problem.`；末次 SCF −364.325340665。
  - 崩溃**中间帧**（不作端点几何）：O1–H4 1.6395/1.6677、H4–N8 1.0538/1.0565、O1···O9 3.5307/3.4746。
- 反端真实极小（环④，独立复核通过）：`declaration_0005/reactant_opt/reactant_opt.log`（sha d010704f59ad083824dc90cba4889163fcb802f9d3daae7672fa7975af02f29a）L18869 `Stationary point found`、收敛表 L18862 四项全 YES、L19301 Normal termination 04:47:00、末次 SCF L18666 **−364.334597427**；`declaration_0005/reactant_frequency/reactant_frequency.log`（sha c51844775bfc8a2417029653cfec05178e984c7de870b944f08e71f78bcdd72f，1968 行）L510 同值（与 Opt 末帧逐位相同）、**0 虚频**（无 imaginary 行，51 模全正：首组 L849 44.4026、末组 L1265 3852.7538）、L1968 Normal termination。末帧几何：O1–H2 0.9704、H2···O9 3.2161、**O1–H4 2.3033（断）**、**H4–N8 1.0267（成键）**、O9–H16 0.9987、**O1···O9 = 2.5887**（一律用 2.5887）。

### 可复用落盘件（本 lane 产出）
- [ENDPOINT_REVIEW_CHECKLIST.md](gold_fill_20261018/HL1/HL1_E1/ENDPOINT_REVIEW_CHECKLIST.md)（sha 362f02d8cdb2e77255989d6bf6c4305de9f43dd68da213994c3d7c20c11c36cb）：取帧三级核对、主/辅判据、约定阈值限定语、每端必报字段、三句限制语、分母口径。
- 脚本（同目录）：`parse_irc_frames.py`、`neighbor_table.py`、`extract_endpoint_frames.py` —— 可复跑核对逐帧键长与近邻表。
- 端点起点：`irc_endpoints/rev_outer/start.xyz`（sha fbb29cef61b8bb95699594b8d522ec476855013c0eb1229b2e8814f08170290b）、`irc_endpoints/fwd_outer/start.xyz`（sha 1d0417cba441fe4670a1d326050a4f9ac5e0345efa6e5ad20b59d38b43bbf478）。

### 方法学坑（跨题可复用，均已实测）
- `opt=modredundant` 的 .gjf：**坐标块与 modredundant 卡片之间必须空行**，否则 l101 `Wanted a floating point number as input. Found an integer as input.`（job 1079：27 原子缺空行，被当成第 28 个原子）。
- `format_converter(log→xyz)` 的 "final frame" **≠ 日志末尾帧**（双向 IRC 里 Path 1 全段在前、Path 2 在后，给的是 Path 1 末点）⇒ 必须 `grep -n "Path Number"` 核对路径号+步号，并与 `Summary of reaction path following` 的带符号 RxCoord、相对能（1e-5 Eh 内）三方自洽。
- `IRC=(MaxPoints=…)` 可能被静默丢弃（#184）⇒ 看 route 回显是否含 maxpoints/stepsize；没有就走引擎默认，不得按文件里写的点数预期。
- Berny 在质子转移/氢键切换段会死于 l103 `FormBX had a problem.`（`Bend failed for angle …` / `Tors failed for dihedral …`）——**属内坐标退化，不是「物种不存在」**；修法 = 用断裂后的帧作新起点 + `opt=(calcfc,maxstep=5)`，必要时并联 `opt=cartesian` 对照。

### 边界与待办
- #1104（coordinator 提交的 `irc_endpoints/rev_opt2/rev_opt2_cart.gjf`，opt=(cartesian,maxstep=5)，4c/6144）待主协调走账本 cancel 通道；即便跑完出现 Stationary point / 0 虚频，也**不改**三层口径，最多登记「额外观察」，不据此改题源、不给 ΔE‡；若被撤按「归档/调度终止」登记、不作端点证据。
- 本 lane 自 04:29 起零提交、零在飞、零 pending reminder、不轮询；未改题源与交付面文件、未 kill 任何作业。


## HI1_E4（旧称 E3a「水加成到亚铵」）归档 · 2026-10-18 05:0x（本 lane）

### 处置
- 用户 05:0x「被换掉的题的任务可以杀了」+ 主协调指令 ⇒ HI1 线停止。本 lane 唯一 run **ts/ts_0024** 已 ts_stop：job **1094**（ts_opt，4c/6144，declaration_0012）**state=cancelled**（refine.log 476,368 B / 仅 7 个 SCF Done / 无 `Stationary point found` / 无 `Normal termination`，最后写入 04:50）；更早的 job 1090（8c，ready 从未起跑）经 ts_stop→ts_resume 撤回。按「**调度终止**」登记，非科学失败。
- 边界：未碰 NR1/NY3 与 HI1 其它边；未 kill 他人作业；未改 priority / method_policy / 题库；ts/ts_0024 原生日志与输入原样保留（不删不覆盖）。

### 结论：**不回填**
(a) 方向过 / (b) 记录 / (c) 未过 ⇒ candidate_only；且题目已被替换，hi.py 第 4 步 barrier 保持 null。

### 直接观测（**只读历史证据，非本 run 自证**）
- 分母 = 41 原子 I2 极小值：E = **−939.320655479 Ha**（[I2_optfreq.log](gold_finish_20261015/HI1/E3/runs/I2_optfreq/I2_optfreq.log) L19183，sha 63dda25e…，**117 模 0 虚频**，`Frequencies --` 首行 L19879）
- 旧 TS：E = **−939.295152015081 Ha**（[frequency.log](ts/ts_0016/jobs/declaration_0007/frequency/frequency.log) L785，sha c5ac8402…；**L1501 恰 1 虚频**，L1510 = −783.7914 / 23.6787 / 35.9094 cm⁻¹，模矢自 L1512）
- 候选 ΔE‡ = 0.025503463919 Ha = **16.00 kcal/mol**（同程序同批，仅旧日志相减）
- 三帧距离（I2 → TS → P）：R(2,25) 3.160→1.861→1.473；R(2,4) 1.299→1.343→1.425；R(25,27) 0.990→1.164→1.634；R(10,27) 1.717→1.247→0.995（**四项全部单调**）
- 虚频模份额：声明中心对 **0.0714** / 模内重原子 **0.0420** / 最大单原子 **0.8939 @ atom 27 (H)** ⇒ soft-mode-dominated（水↔羧基质子穿梭），但非 spectator

### 声明错位（关键；将来重启此边须先改声明再算）
- 题库把 map22（水的一个 H）译成工作序 atom 24，但 **atom 24 是醇羟基 H**（R(28,24)=0.967–0.984 全程共价；R(24,25)=4.2–4.7 Å 全程不接触）。真穿梭质子是 **atom 27**、受体是羧基 **O10**。
- 平台因此以 `reaction_center_distance_out_of_range` 拒收原申报（ts_0024 rev 38）；修正申报 = form (2,25)、break (2,4)、form (10,27)、break (25,27)。主协调已落盘 DECLARATION_FIX.md（sha fde5f915…）。

### 平台限制（已登记，供开 issue）
- ts_resume **只改 execution 不回改已排队作业**：1090 的 receipt 显示已接受（revision 49），但 waiting 项仍 `req_cpus=8 / req_memory_mb=10240`；排队作业降配只能 ts_stop → ts_resume。原文证据见 [PROVENANCE.md](gold_fill_20261018/HI1/HI1_E4/PROVENANCE.md) 第 6 节。

### 文件（归档面）
- [BACKFILL_PROPOSAL.md](gold_fill_20261018/HI1/HI1_E4/BACKFILL_PROPOSAL.md)（主协调要求 8 项全）、[PROVENANCE.md](gold_fill_20261018/HI1/HI1_E4/PROVENANCE.md)、[STATUS.md](gold_fill_20261018/HI1/HI1_E4/STATUS.md)、analysis/{mode_analysis,geom_table,smi_check}.py


## HI1_E1b（注册表边 HI1_E2，半缩胺脱水 → 烯胺 + H2O，27 原子子系统）· 归档（as_e38fb7c615094945，目录 gold_fill_20261018/HI1/HI1_E1b/）

> 状态：**按用户 05:0x 指令（被替换题停止）于 2026-10-18 05:0x 调度终止**，本节重贴于 06:1x 的 PROCESS.md 重建之后。

- **边 → job id → 卡在哪一环**：HI1_E1b → **job 1092**（run **ts_0026** 的 ts_opt）→ 卡在 **ts_opt 第 33 步未收敛、未进 freq**；run = stopped（rev 23），job = **cancelled**（调度终止，非科学失败）。
- **原生日志与行号（参考态，仍有效）**：[INT1_27_optfreq.log](gold_finish_20261015/HI1/E1/split/INT1_27_optfreq.log) sha256 `c03e0a82d78d22b96474ab48ee40799adb63a894bb9cefcd27c7051799024f63`，E(分母) = **−593.929762803 Eh**（L26615 / L28142），L26904 Stationary point found，75 模 0 虚频（L28588-28589，最低实模 78.1490）。
- **终止作业的原生证据**：`ts/ts_0026/jobs/declaration_0003/ts_opt/refine.log` sha256 `a27d5f147487f099e7938798bd63a96bd61ae4c0b405d3b33de5de9a5af6099d`（1,519,164 B）；`Step number 33 out of a maximum of 153`（L23848），末条 `SCF Done E(RB3LYP) = -593.859284599`（L23775）；Normal/Error termination 各 0 条。输入 `refine.gjf` sha256 `658b0cc3e836d8ef929f2e634aa30376dbe65bdfb157119db91af67ad3df51c7`（`opt=(TS,calcfc,noeigen)`，%nproc=4 / %mem=6144MB）。
- **判据状态（全未测）**：(a) 虚频模方向、(b) 三份额、(c) TS 1 虚频 + 双向 IRC + 两端 Opt/Freq 全无 ⇒ **ΔE‡ 不存在，题库该边必须保持 null**；第 33 步的 −593.859284599（≈ +44 kcal/mol）只是临时几何能量，不得当能垒上界。
- **模型事实（可直接复用）**：27 原子工作序 = INT1_27 序（1=C1、2=C2、3=O4、4=C3、10=H22、18=N20、27=H21），C8H15NO3 q0/m1；反应中心 1-based form (2,4)/(3,10)、break (4,10)/(2,3) 已与 hi.py 第 2 步核对一致；产物端 27 原子烯胺+水**没有**现成原生日志（盘上只有 41 原子 I1_S_start.xyz，其 provenance 明确不主张极小值）。
- **假设（未检验，留给将来）**：协同四中心（O4 直接夺取 alpha-H）几何高度张紧——C2 距 C3···O4 直线仅 0.86–1.2 Å，guess 中 C2···H22 = 1.595 Å、C3-H22···O4 = 152.8°、每个 H 距母原子 0.97–1.10 Å。若重开此边，应优先检验分步（先断 C2–O4）而非在协同 guess 上加优化器参数。
- **归档文件**：[STATUS_STOPPED_20261018.md](gold_fill_20261018/HI1/HI1_E1b/STATUS_STOPPED_20261018.md)（终止记录 + 可复用证据）、[E1B_STATUS_AND_EVIDENCE.md](gold_fill_20261018/HI1/HI1_E1b/E1B_STATUS_AND_EVIDENCE.md)、[TS_GUESS_PROVENANCE.md](gold_fill_20261018/HI1/HI1_E1b/TS_GUESS_PROVENANCE.md)；`build/analyze_freq_mode.py` 为通用频率模三份额/watch-pair 分析脚本（已在 75 模日志上自检）。`ts/ts_0026` 全部原生产物原样保留，未删未覆盖。
- **事故说明**：本 lane 早前对 PROCESS.md 的追加（03:5x）随 06:04 的截断丢失，本节为按原写入块重贴并补入终止状态；未整文件覆写，只用局部 edit 追加。


## 已归档道 · 频哪醇 NR1（pinacol → pinacolone，C6H17O3，26 原子；目录 gold_fill_20261018/NR1/ + 旧包 gold_finish_20261015/NR1/）

> ⚠ 重名警告：本节的 **NR1 = 频哪醇重排**（用户 03:0x 前的原题，已被替换为甲酰胺）；当前活跃的「NR1 = 甲酰胺」在 gold_fill_20261018/N_FORMAMIDE/，两者组成不同（C6H17O3 vs CH3NO）、读数**不得混用**。

### 结论（无待推进项；本道已无在飞/排队作业）
- **NR1（频哪醇）_E1 = 可回填 0.0 kcal/mol 约定值**：无独立一阶鞍点（不是算出的 0 垒 TS），参考态 = 接触离子对，E = −464.000864850 Ha，gold_finish_20261015/NR1/E1/opt_R/optfreq_R_d230.log，sha 130e6863…f407，SCF Done L81363 / Optimization completed L80267 / 首行 Frequencies L81791（72 实频、0 虚频、最低 42.9966 cm⁻¹）。支撑：918 种子坍缩（声明 R 非驻点）；903+906 合并真 PT 差坐标 21 点无内部极大（最低点 −464.000858655，与 918 差 0.0016 kcal）；973（0.02 Å、26 点）与 974（定骨架、实测 **29 点**，更正旧文档的 27 点）无内峰；929 单调 +18.14 且 977 落回同一极小值。E1 消耗 0 个 QM 作业。
- **NR1（频哪醇）_E2 = null（不填值）**：I1 = −463.999955035（E2_I1_optfreq_c000_r2.log:18766）、I2 = −463.981552572（E2_I2_optfreq_c000_r2.log:27292），E(I2)−E(I1)=+11.55。新增判据：I1 二面角 O6–C4–C7–O10 = −179.6°（anti），声明 I2 = −8.1°（syn），差约 170° C4–C7 扭转；917 的 14 点全程保持 anti（r(C4–O10) 2.309→1.930@pt7→1.551@pt14），且我把扭转**完全冻死**的扫描仍在 r(C4–O6)≈2.54 Å 出现 +16.24 kcal 极大 ⇒ **+16.24~16.26 属 anti 通道的环氧鎓捕获脊，不是 I1→I2 的鞍点**。缺：模式以 C4–O6 断裂为主的独立鞍点 + 双向 native IRC + 两端 Opt/Freq（job 941 IRC 在 l123 失败）。syn 起始几何已备好待接手线：gold_fill_20261018/NR1/geom/I1_syn_rot180.xyz（sha 1d9bed0c…884d，dih(7-5-8-11)=+0.4°）。

### 事故/环境记录（可复用）
- job 1082（我的 anti 通道复扫）于 03:44:31 被平台按裁决取消（exit −15，7/11 点，日志 sha 8e3c99cc…dc1f7，**截断无 Normal termination**）⇒ 按「调度终止」登记，不作科学失败结论；其 §3.2b 部分读数保留在 STATUS.md。
- job 1083 = 同一输入的误重复提交，在 ready 状态即用 mark_compute_job_failed 撤回，避免覆盖原生日志；未 kill 他人作业、未改 priority、未用 manual TS/IRC。
- 本道交接文件（含 ≤1 页交接口径、逐点表、文件清单）：gold_fill_20261018/NR1/STATUS.md（sha 92fd8a6e…adc3，217 行）。本道**未**在本次 PROCESS.md 事故前后写过任何共享文件，其它 lane 的丢失内容与本道无关。

## HI1_EM1（副面通道）· 已归档（用户 05:0x 指令「被换掉的题的任务可以杀了」后的停算记录）

> 本节由 QM 执行道（as_fae50a6580774668）在 PROCESS.md 事故后重新追加；原始归档目录 `gold_fill_20261018/HI1/HI1_EM1/` 未动。
> 结论：**HI1_EM1 已归档为方法学对照，candidate_only、未回填、无 ΔE‡**；停算性质 = **调度终止（用户指令），不是科学失败**。

### 直接观测（可复核，全部只读原生文件）
- 旧候选 TS（第二次尝试，declaration_0002）：`ts/ts_0012/jobs/declaration_0002/ts_opt/refine.log` sha256 **66691e0e…**（L24549 `Optimization completed.`、L24550 `Stationary point found`、L24183 末次 SCF **−939.283734374**、L25650 正常终止）；配套 `.../frequency/frequency.log` sha256 **a471aa7b…**（L1541 `1 imaginary frequencies`、L1550 **−314.2861 / 33.5499 / 44.0361**、L857 E 同值、117 模、L5340 正常终止）。
- 编号口径（曾被他处写反，此处以盘上文件为准）：**job 1032 = declaration_0002 ts_opt**（`state_1032.json` 存在；E −939.283734374、freq −314.2861）；**job 1013 = declaration_0001**（`state_1013.json`；E −939.293671629、d(1,29)=3.198 Å 反应物侧、freq −27.9419 已判 pseudo-saddle）。旁证：`gold_finish_20261015/LEDGER.md` L1129、L714。
- (a) 方向硬闸门 **过**（由上述 freq 模向量重算，脚本 `build/analyze_mode.py`）：C3–C6(1,29) 净投影 **−1.109 = 缩短**、C2=C3(2,1) **+0.166 = 拉长**、C6=O5(28,29) **+0.177 = 拉长**，与题源 bond_changes 同向；C2=N20(2,4) −0.070 缩短。
- (b) 成分（无阈值，记录项）：反应中心原子 {1,2,4,28,29} **0.6665**、heavy 20 原子 **0.6951**、最大单原子 = 原子 1（C3）**0.3282** ⇒ 落在反应中心，**非 soft-mode-dominated**。
- (c) 交付：**从未满足**。新 run `ts/ts_0025` 的 ts_opt（job **1095**）04:28:56 收敛（`.../declaration_0003/ts_opt/refine.log` sha **57cb8439…**、L2625 **−939.283734386**、L3002/3003、L4114 正常终止；与 job 1032 帧 maxdev **0.0017 Å**、能量差 1.2e-8 Eh ⇒ 同一驻点复现），但 freq（job **1103**）在解析 Hessian/CPHF 阶段被撤停（**无任何频率输出**，日志冻结 55113 B、sha **4ce6c6cf…**），双向 IRC 与两端 Opt+Freq 均未开始 ⇒ **E(TS) 未取得、ΔE‡ 未算**。
- 旧 IRC（job 1039，`.../declaration_0002/irc/irc.log` sha **dfc4d3ec…**）：正向 10 点被 G16 默认 MaxPoints=10/方向截断（L8405），反向第 3 点起 `Delta-x Convergence NOT Met` 连续 20 次后 L25166 l123 终止；**方向归属**（读几何得）：正向 d(1,29) 1.938→2.438 = 走**反应物**侧，反向 1.822→1.767 = 走**产物**侧且能量极平（−939.28386→−939.28411）。该 IRC 永不作连通性证据。
- 降配/平台限制（原文存 `build/TS_SEED_PROVENANCE_EM1_JOB1032.md` §8）：ts_resume 改 execution **只对今后新提交生效**（retained job 1088 仍 8c/10240）；排队作业降配须 **ts_stop → ts_resume(changes={})**，实测产出 job 1095 = 4c/6144。

### 方法学坑（可复用）
- **CIP 必须 strip atom-map 再判**：同一几何/拓扑，RDKit 保留 atom-map 号会把 Cα(8) 判成 **R**，strip 后为 **S**（脚本 `build/cip_check.py` 默认 strip，`--keep-maps` 仅诊断）。TS 几何实测 Cα(8)=S、C6(29)=R，与副面通道声明一致。
- 41 原子体系 G16 freq 一旦进入 `Frequencies --` 即一次打全 117 模；停在 CPHF 前 = 一个频率都没有，不能报「部分虚频」。
- 参考态固定 **job 924 = −939.308218263 Eh**（三个独立 Opt+Freq 收敛同值）；禁用 job 1000（−939.302926757，伸展构象）或工作流自身 reactant 端点。

## 2026-10-18 · TaskSpec 草案道（specs lane，as 本会话；目录 gold_compute/queue_20261018/specs/）

> 本节由 specs 道在 PROCESS.md 截断事故后重新追加。本道**不提交计算、不碰 ts/、不碰 registry/JSON**，只产出两份草案文档；无在飞/排队作业。

### 直接观测（文档现状，均为本道新建文件）
- `gold_compute/queue_20261018/specs/TASKSPEC_N_FORMAMIDE.md`：251 行，sha256 `3ed335b8b794e2d0e60b13d634745f77acad98504cd234e86fbf9fc3951cb7ee`（v3）。
- `gold_compute/queue_20261018/specs/TASKSPEC_N_HNCO_HYDROLYSIS.md`：197 行，sha256 `facd0b91de9dec94c68fb3f334a44f12ec73da0b996eb3fe9fac26338fc5c9ca`。
- 两份均**不含任何 gold 数值**（无 `barrier_kcal_mol`、无文献能垒回填），只有节点/边/TS 清单、缺口与自检清单。原生日志读数一律留给协调方回填 registry。

### 已写入两份草案的稳定结论（可直接引用）
- **bond_changes 原子序 = 映射 SMILES 的 1-based atom-map 编号**（`gen_normal_tasks._derive_bond_changes`：`GetAtomMapNum`，0 号即报错）；`break` = 键级下降（含断到 0），`form` = 键级上升（含自 0 新建）；纯构象/翻转步双空 + registry `conformational: True`，否则 `_validate_task` fail-loud。
- 含 H 转移的小分子路径必须在 mapped SMILES 里显式写 `[H:n]`，否则键变会静默变空；`_unmap_canonical` 走标准解析（吸收显式 H），故 R/P 的 unmap 结果仍为 `NC=O` / `C#N.O`。
- 甲酰胺边表（spec map 1=C 2=O 3=N 4=H(C) 5=E1 迁移的 H 6=N–H）：E1 break{[1,2],[3,5]}/form{[1,3],[2,5]}；E4 break{[1,2],[3,6]}/form{[1,3],[2,6]}；E2/E3 双空。
- 甲酰胺 E2 = **N–H 绕 C1–N3 翻转**（动 map 6）、E3 = **O–H 绕 C1–O2 旋转**（动 map 5）；C1=N3 全程双键，不是 E/Z 翻转。已在 spec 内修掉并发写入引入的 H5/H6 互换，并加对照：**协调方 xyz 序 H4 ≡ spec map 6、xyz 序 H6 ≡ spec map 5**（照抄 xyz 序号会让 E1/E4 键变与 E2/E3 归属整体错位）。
- HNCO 单水：E1 break{[1,3],[5,6]}/form{[1,5],[3,6]}；E3 break{[1,3],[5,7]}/form{[1,5],[3,7]}（map 1=C 2=C=O 的 O 3=N 4=N–H 5=水 O 6=迁到 N 的水 H 7=留在 O 的水 H）。**E3 分母只能取「经构象边真正到达的那个氨基甲酸构象」**，不得用更稳定的另一极小值拼接；水数固定 1，失败不加水壳。
- 两份草案的 E4（甲酰胺）与 HNCO 步数都是"候选拓扑"：甲酰胺 E4 目前 **null**、图里保留该边（barrier 空）；HNCO 明确禁止预设"只有两个 TS"。

### 缺口 / 下一步（属记录面，不是结论）
- 甲酰胺：E4 未定位（失败档案见 spec §4.3 五条：伪极大判据、OptTS 滑回 ts_0034 同模、只约束 O···H 时 C–O 回闭），下一步二维内点；SI Table S1/S2 与本地 INT-1a/1b/1c 的标签对应仍缺二面角依据；P 侧用分离优化还是复合物极小值待定。
- HNCO：整条单水路径的 TS 清单未核齐；E1 协同 vs 先成两性离子分步、氨基甲酸是否有第二个构象边、产物侧 NH₃···CO₂ 复合物身份均待实测。
- 协作风险（实测两次 `conflict`）：`TASKSPEC_N_FORMAMIDE.md` 曾有两条 lane 并发整文件覆盖写；今后该文件只用局部 `edit`，且以最新 sha 为准。


### 归档位置与 sha（不再变动）
`gold_fill_20261018/HI1/HI1_EM1/STATUS.md`（**e0044f95…**，含「归档 · 停止记录」）、`BACKFILL_PROPOSAL.md`（现盘 **e48f0c3d…**，八项齐、数值留空，§1b/§9 为他处追加）、`build/TS_SEED_PROVENANCE_EM1_JOB1032.md`（**da98a840…**）、`evidence/{refine,frequency,irc}_frozen.log`（444 只读副本，sha 同源 66691e0e / a471aa7b / dfc4d3ec）。

## NY3（**旧题**：甲酸甲酯皂化 · Na⁺ 中性模型）· 归档索引（gold_fill_20261018/NY3/）

> 命名提示：本节 = registry `cloudra/benchmark/normal_registry/yo.py` 的 Y3 三步（RC→I1→I2→P，q=0/m=1，CPCM(Water)，G16 B3LYP/def2SVP+GD3BJ+UltraFine+SCF=Tight）。**不是**替换后编号的「NY3 = HNCO 单水」（后者 run ts_0028 / 1293+1294 批次；本节 ts_0021 / ts_0023）。索引原件 `gold_fill_20261018/NY3/STATUS.md`（sha256 8cfccaa820742181848e4100a59357933544ac9fa9b56544d2616bc1480e236e）。

### 结论（冻结，未回填）
- 三边 ΔE‡ **全缺测（可回填 0/3）**：无一条有「恰 1 虚频且模属声明键对 + 双向 IRC + 两端 Opt+Freq」；E1 **从未提交作业**。
- 作业账 3 个（上限 12），**技术性/调度失败，均不构成「无鞍点」证据**：**1081** failed（E2 attempt1，l103 `FormBX had a problem`；末帧 r(C4–O3)=3.308 Å 已过脊线滑向产物侧）；**1085** failed（E2 attempt2，guess = 我构造的 I1→IDPP 插值 r=2.044 Å，NStep=42；末帧 r(C4–O3)=1.948 Å、末 SCF −466.993406557 = vs I1 **+7.2 kcal/mol**，四项判据全 NO）；**1087** 记「调度终止」（E3 ts_opt，D23/D32 腾 8c 给 HL1_E1 IRC；22 步、末 SCF −467.027212892 = vs I2 −25.9 / vs P **+11.8 kcal/mol**，非驻点非能垒）。

### 可复用工程结论
1. `conformers.reactant/product.optimization = null` ⇒ build/map/assemble **0 作业通过、直接进 ts_opt**，绕开 ts_0013/ts_0014 的 `conformer_optimization_failed`（既有 1007/1011/1012/1016/1019/1024/1025 全卡在 build 阶段 NStep/l9999）。
2. `reaction_center` 实测 **1-based 输入 / 0-based 存储**；I2 端点须配带键块的 `prep/build/art_I2_src/assembly/complex_candidate_000.mol`（`prep/i2.mol` 无键块 → `endpoint_identity_mismatch`）。
3. 管线 ts_opt route 固定 `opt=(TS,calcfc,noeigen)`（不可换 cartesian/readfc），只能调 guess 与 reaction_center。

### 几何线索（非能垒）
- E2 脊线夹在 r(C4–O3) ≈ **1.95（+7.2 kcal、仍上升）↔ 2.42（已滑向产物侧）**；建议先同批受约束弛豫扫描（`B 4 3 S 8 -0.05`，1.55→2.55 Å）再取最高已收敛帧作 guess。
- E3：质子夹在 O1/O3 间（O1···O3 2.48–2.51 Å）时仍比 P 高 ≈+11.8 kcal/mol 且持续下降，22 步无驻点；参考态风险 = guess 构象（O1···O3 2.81 Å）≠ 登记 I2 极小值（job 990，O3···O9 4.19 Å），换构象须整批重算并登记，新旧值不得混减。
- E1：RC 属**支-RC**（Na 桥联羟基 O1 + 羰基 O5），登记 I1 属**支-I1**（Na 桥联甲氧基 O3 + 酯氧 O5）⇒ 单步 RC→I1 必耦合 Na⁺ 迁移；建议 2D 搜索（r(O1–C4) × Na⁺ 归属）或拆成「加成 + Na⁺ 重排」两步。

## HI1_E1b（旧题线 · 已归档的方法学对照；本会话 = molecular/cluster QM specialist）

> PROCESS.md 事故后重新追加本节；原始归档 `gold_fill_20261018/HI1/HI1_E1b/` 与 `ts/ts_0026/` 均未动。
> 结论：**HI1_E1b 已归档，D1 (a)(b)(c) 全未测 ⇒ 现值 null、不回填**；停算性质 = **调度终止（用户 05:0x 指令「被换掉的题的任务可以杀了」），不是科学失败**。

### 直接观测（可复核，全部只读原生文件）
- 停算：#1092（`ts/ts_0026/jobs/declaration_0003/ts_opt/refine.gjf`）由 `ts_stop(ts_0026)` 于 04:51:04 停止，**cancelled @ 2026-10-18T04:51:42**；`.cloudra/calc-1092.exit.json` **exit_code = −15**（SIGTERM）、`guard-1092.log` calculator 退出码 241；`refine.log` 内 Gaussian 自身 `Error termination` = **0**、`Normal termination` = **0**（被信号打断，未收尾），日志 sha256 **a27d5f147487f099e7938798bd63a96bd61ae4c0b405d3b33de5de9a5af6099d**、mtime 04:50 自停止起未变。停止瞬间 `Step number 33 out of 153`（L23848）、末条 SCF **−593.859284599**（L23775）⇒ **未收敛、未进 freq、无虚频**；该过程能量不作任何 ΔE‡。
- 分母（本步起点极小）：job 1051，`gold_finish_20261015/HI1/E1/split/INT1_27_optfreq.log`，sha256 **c03e0a82d78d22b96474ab48ee40799adb63a894bb9cefcd27c7051799024f63**、30,757 行；E(RB3LYP) = **−593.929762803**（L26615 opt 末 / L28142 freq 段同值）；`Stationary point found` L26904；`Normal termination` L27581 / L30757；`Frequencies --` 25 组 = **75 模 = 3N−6（N=27）**、`imaginary` 0 条；最低实模 **78.1490 cm⁻¹**（L28598）；G16 RevC.01（L78）。
- TS guess 自查：`gold_fill_20261018/HI1/HI1_E1b/build/ts_guess_27.xyz` sha256 **88162e53ae6598e8550cc1e4f2a0037fda402a0212e6b607267ee8d97f585d4d**；**最小原子间距 0.9699 Å ≥ 0.9**；实测 R(2,4)C2–C3 **1.4400**、R(3,10)O4–H22 **1.3507**、R(4,10)C3–H22 **1.3547**、R(2,3)C2–O4 **2.2000**（起点 1.5351 / 2.7348 / 1.1006 / 1.4208）；登记张力 r(C2···H22) = 1.5947 Å ⇒ 高张力四中心协同质子转移假设（未验证）。
- 输入缺陷（留档，因停算未修正）：ts_0026 的 `reaction.reaction_center` 被写成 **0-based** `[[1,3],[2,9],[3,9],[1,2]]`，契约要求 1-based，正确值 **`[[2,4],[3,10],[4,10],[2,3]]`**；只影响 run 自带 mode 份额/方向诊断，不影响作业物理（`opt=(TS,calcfc,noeigen)` 不读该字段）。
- 判据脚本（可复用到任何新题）：`gold_fill_20261018/HI1/HI1_E1b/analysis/d1_report.py`（sha **94e28202…**）—— ① 27 原子「序号→元素＋角色」全表 ② 反应中心候选原子（2,3,4,10,18,27）<2.0 Å 近邻表（D28 式身份核验）③ 虚频模三份额 + 最大单原子自由度 ④ (a) **sign-free 形状判定**（本征矢符号任意：form 两对同号 + break 两对同号 + 两组相反 ⇒ 形状过；**方向须由 IRC 端点钉定**，不得凭模态符号）⑤ 两种投影标度（单位模矢 s / |d|_total = 0.1 Å 的 δR）。已在 job 1051 上自检：R(2,4)=1.5351 / R(3,10)=2.7348 / R(4,10)=1.1006 / R(2,3)=1.4208 与几何帧逐位一致；身份表确认 2=C2、3=O4、4=C3、10=H22、18=N20、27=H21。

### 归档位置与 sha（不再变动）
- `gold_fill_20261018/HI1/HI1_E1b/E1B_STATUS_AND_EVIDENCE.md`（**1ffaeb9726f22c25fd4028634b5cbad2b88293a32984affe0a170fc8e2d58168**；第 2 节分母、3 节 guess、5 节缺陷、8 节协调口径与判据脚本、10/10.1 节终止记录）。
- `ts/ts_0026/process.json`（rev23、status=stopped）、`jobs/declaration_0003/ts_opt/{refine.gjf, refine.log, .cloudra/}`；`gold_fill_20261018/DASHBOARD.md` 的 #1092/HI1_E1b 行已改记为「调度终止」。

### 方法学坑（可复用）
- 平台 #184：IRC 阶段无入口设 MaxPoints/StepSize（写 keywords 被 admission 拒、`end_setting` 被静默丢弃）⇒ IRC 只能跑引擎默认 ~10 点/向，端点身份须由最外层帧 Opt+Freq 承担，并逐字写「未达声明端点」。
- `ts_resume` 在作业 **running** 时被契约拒绝（Running jobs prevent revisions）⇒ 阶段之间改声明只能抓「上一作业终态、下一作业未起跑」窗口，或趁下一作业仍在 queued（此时 supersede 属正常语义，记录 invalidated）。
- 共享 Markdown 并发写：多 lane 同时追加会 conflict；只用局部 edit + 每次先 read 取现盘 sha，冲突就重读再来，绝不 write 整表。
## NY3 · 异氰酸单水中性水解 HNCO + H2O → NH2COOH → NH3 + CO2（本 lane 重追加；目录 gold_compute/queue_20261018/results/NY3/）

### 直接观测（B3LYP/def2SVP + GD3BJ + Int(UltraFine) + SCF=Tight，气相 q0/m1 闭壳层，4c/6144MB/prio 0；原生日志 jobs/，副本 logs/，未删未覆盖）

| 驻点 | job | E / Ha（纯电子） | 虚频 | 判定 |
|---|---|---|---|---|
| RC = HNCO·H2O 氢键预络合物（N3–H4···O5 = 1.802 Å） | 1152 | -244.935406907 | 0（15/15 实频） | 已验证极小值 |
| 失败端点：R_complex.xyz 直接优化 | 1132/1139 | -244.934373855 | 2（-212.1、-38.6） | 非极小值，不得当端点 |
| I_syn = 氨基甲酸 syn（H7···O2 = 2.288 Å 分子内氢键，本水平全局最小） | 1133（复算 1157） | -244.966495972（1157 = -244.966496071） | 0（15/15） | 已验证极小值 |
| 题面 I2.xyz「反式体」几何 | 1134 | -244.953252173 | 1（-272.9714，H6 份额 0.755） | 鞍点，非极小值 |
| I_anti = 氨基甲酸 anti（H7···O2 = 3.016 Å） | 1163 / 1169 | -244.953791465 / -244.953791466 | 0（15/15） | 已验证极小值（沿 -272.97 模 ±0.40 两个方向收敛同一结构） |
| TS2 = syn↔anti 构象边 TS | 1174 / freq 1176 / IRC 1130 | -244.948872987 | 恰 1（-465.6897） | ts_0028 outcome=verified |
| NH3 产物分量 | 1179 | -56.5106949685 | 0（6/6） | 已验证极小值 |
| CO2 产物分量 | 1180 | -188.44467957 | 0（4/4） | 已验证极小值 |
| NH3···CO2 松散复合物 | 1164 / 1168 / 1181 | -244.9581（未收敛） | — | 三次尝试全失败（l9999 / l103 torsion-FormBX / Cartesian l9999）；尝试搜索中未找到极小值 |
| 两性离子 H3N⁺–COO⁻ 猜测 | 1136 | -244.9640755（已解离为 NH3+CO2） | 1（-20.5） | 本水平未找到两性离子驻点 |

### ts_0028 的 D1 三环（实测，不设阈值）
- (a) 方向：-465.6897 虚频的未加权平方位移份额 = 原子7(H) 0.9704、原子6(H) 0.0168、5(O) 0.0056；top pairs (6,7) 0.6659、(3,7) 0.4709、(4,7) 0.3925、(2,7) 0.3700；全局最大相对位移 pair = (5,7)。本边为构象边（两端同为 NC(=O)O，reaction_center 与 bond_changes 均为空，工具 mode_alignment=skipped）⇒ 无 watch pair 可判，如实记空，不捏造断键。
- (b) 成分：反应中心份额 = null（未声明 watch pair）；全重原子份额 0.0076739；最大单原子份额 = 原子 7 (H) 0.97040。
- (c) ΔE‡：TS − 本步自身起点 I_syn = -244.948872987 − (-244.966495972) = +0.017622985 Ha = +11.06 kcal/mol（对 I_anti 端 +3.09）。两端 Opt+Freq 0 虚频并核身份：1178（-244.966495971，15/15）、1184（-244.953791465，15/15）。双向 IRC 10+10 点，端点位于 TS 与对应极小值之间。

### E1 协同 vs 两性离子分步（本 lane 结论）
- 观测：两性离子起点（N–C 1.50 Å）Opt+Freq（job 1136）不驻留——收敛结构 C1–N3 = 2.754 Å、N 上 3×H 1.02 Å、两个 C–O 1.164 Å，即直接解离为 NH3 + CO2 复合物（-244.9640755，仍带 1 虚频 -20.5）⇒ 本水平未找到两性离子中间体。
- 推断：与「协同单步 4 中心加成」相容；但 E1 的 TS/IRC 属 ts_0027（blocked）⇒ 不宣称 E1 已核实、不给 E1 势垒。扫描峰/受约束剖面一律不作势垒。

### 缺环
- E1（RC → I_syn）与 E3（I → NH3+CO2）的 TS 分别在 ts_0027 / ts_0029（他道，均曾因 admission PATH 拒单 blocked）；ΔE‡ 分母分别是 job 1152（RC）与 job 1133（I_syn）；E3 产物参考建议用分量 1179+1180（-244.9553745385）。
- NH3···CO2 单节点若必须合并，需要更松判据或显式约束；未收敛结构不得写成极小值。

### 环境坑（可复用）
- 平台 admission 间歇拒 gaussian 提交（"PATH is missing … g16"）：失败 1132/1135/1140/1154/1155/1156/1160/1161，成功 1133/1134/1136/1139/1152/1153/1163/1168/1169，同批交错、重试即过。按平台阻塞登记，不计科学失败；未 kill、未改 priority。
- 极小值搜索必须核对虚频：R_complex 与 I2 两个看起来正常的 MMFF 几何优化后都不是极小值（2 虚频 / 1 虚频），沿虚频模位移重优化才得到 RC 与 I_anti。
- 产物侧笛卡尔 opt 处理松散复合物仍 l9999；opt=CalcFC 会因冗余内坐标构造失败报 FormBX/torsion。

### 交付面
- results/NY3/REPORT.txt（本 lane 全部实测数值与口径）、results/NY3/mechanism_graph.json（e2 有势垒 11.06；e1/e3 明确标 pending、无势垒）、geoms/ 导出极小值几何。

### 【本轮补齐｜成键步 TS｜只做 TS/IRC，未重算驻点】2026-10-18 05:40–06:10
（上面「e1/e3 pending、无势垒」已被本节取代。方法不变：B3LYP-D3BJ/def2SVP + UltraFine + SCF=Tight，气相 q0/m1，4c/6144、prio 0；k = 627.509474 kcal/mol·Ha⁻¹。）

| 边 | TS | E(TS)/Ha | 虚频 | ΔE‡（分母 = 本步自身起点极小值） | durable verdict |
|---|---|---|---|---|---|
| e1 RC→I_syn | TS1（ts_0027） | -244.876786249 | 恰 1：-1579.3842 | +0.058620658 Ha = **+36.79**（对 RC 1152 = -244.935406907） | candidate_only（见下） |
| e3 I_syn→P | TS3（ts_0029） | -244.897758392 | 恰 1：-1656.9651 | +0.068737580 Ha = **+43.13**（对 I1_syn 1133 = -244.966495972） | **verified = true** |

- 虚频方向（D58 已过，非转子）：E1 份额 H6 0.9570、投影 (5,6)=0.880 / (3,6)=0.819；E3 份额 H7 0.9769、投影 (5,7)=0.892 / (3,7)=0.811；两条 mode_alignment=aligned。
- 双向 IRC（各 10 点 = Gaussian 默认上限）：E1 迁移氢 H6（F 向 O5–H6 0.991 回水、R 向 N3–H6 1.031 成酸）；E3 迁移氢 H7（F 向 N3–H7 1.030、C1–N3 1.673；R 向 O5–H7 0.990）。
- 两端 Opt+Freq 均 0 虚频：E1 RC -244.935406911（job 1285）、氨基甲酸 -244.966495971（1288）；E3 氨基甲酸 -244.966495971（1276）、NH3···CO2 -244.964075631（1279）。

**guess 来源（D64 合规）**：不做平衡态直起 TS。先做只冻结目标成键距离的约束优化（E1 冻 C1–O5 1.95 / O5–H6 1.35 / N3–H6 1.45；E3 冻 C1–N3 1.95 / O5–H7 1.40 / N3–H7 1.40，旁观氢旋出平面破平面简并），取末帧作 provided guess（job 1235 / 1236）。v1（1233/1234）因 end_setting 前导空行使 ModRedundant 段读空、退化成无约束优化，已弃用。

**E1 的缺口（平台性质，非化学）**：IRC 只有 10 点，F 侧外帧停在 C1–O5 1.835 Å，与 RC 最小（3.77 Å）的距离矩阵 RMSD 1.347 Å（E3 通过时约 0.335 Å），interval proof 几何对齐门不过。实测 MaxPoints/StepSize 传不进：写 keywords 判 mismatch、写 end_setting 只落在坐标块之后（declaration_0010/irc/irc.gjf 尾部可见）。
**替代补证（本征矢跟随）**：沿 -1579.3842 单位模矢 ±0.30 Å 各做一次自由优化+频率——job 1293（+）→ **氨基甲酸** -244.966495489，0 虚频，与 I1_syn 的 heavy RMSD 0.0002 Å（同一极小值）；job 1294（−）→ **HNCO + H2O 无氢键旋转体极小值** -244.926200303，0 虚频，但与 RC(1152) 不是同一构象（heavy RMSD 0.6972 Å、N3–H4···O5 3.870 Å vs 1.802 Å、高 +5.78 kcal/mol）⇒ 产物侧连接性精确成立，反应物侧只到物种级，TS→RC 之间还差一个水旋转构象环节（属 E2 类构象边，不在本轮授权内）。

**额外收获（更正旧登记）**：NH3···CO2 复合物**确有** 0 虚频极小值 -244.964075631（job 1261/1262 沿 job 1136 的 -20.6233 扭转模 ±0.5 位移后重优化，15 全实频、最低 7.01）；旧「三次搜索都没找到」应改为「极小值存在，但旧 guess 方位未沿虚频模跟随」。

- 证据与逐帧表：results/NY3/REPORT.txt 第六、九节（REPORT 177 行，sha 2b2c449d984fa9ca…）；图：results/NY3/mechanism_graph.json（e1 36.79、e2 11.06、e3 43.13；223 行，sha 99f615d0d63956fa… 后经一次 provenance 文字修正）。
- 口径：E1 与 E3 能垒不相加、不构成总势垒；NH3···CO2 仅作 E3 产物端驻点，绝不做分母；ΔE‡ 分母一律取本步自身起点极小值。
- 共享文件事故后本节为重建追加；`results/NY3` 现为指向 `gold_compute/queue_20261018/results/NY3` 的符号链接，任务书路径可用。

## NR1 · 甲酰胺脱水第四条边 e4 = INT-1c-tsH2O（本 lane，已定位 64.93）· 2026-10-18 06:2x

- **结论**：e4 一阶鞍点已定位（run ts_0042）。TS E = **−169.641371451 Ha**、**恰 1 虚频 −1923.6069 cm⁻¹**、四列投影 O3–H4 +0.9036 / N1–H4 −0.8482 / C2–O3 −0.1206 / N1–H6 −0.0174、**ΔE‡ = +64.93 kcal/mol**（分母 INT-1c job 1125 −169.744844814），反向 +49.81。四条边因此 4/4 齐（e1 46.32 / e2 22.80 / e3 7.25 / e4 64.93）。
- **处理证据（评审会问）**：平面约束的 cand_b 帧（job 1291）有 2 虚频，其中 −435.71 为纯面外、四列投影全 0；真实 PES 上该面外方向被弛豫（TS 褶皱，dih(H6–O3–C2–N1) −105.8°），故 1291（2 虚频）→ 1296（恰 1 虚频）。
- **端点**（declaration_0004）：reactant −169.744844755（0 虚频，与 INT1c 差 6e−8 Ha，Kabsch <1e−4 Å，dih 0.00°/180.00°）；product −169.720742511（0 虚频，与 job 1213 差 2.5e−8 Ha，P−INT1c = +15.12 kcal/mol，片段间最短 N1···H6 2.094 Å、C2–O3 4.207 Å）。
- **唯一缺口**：工作流 verdict = candidate_only，仅因 IRC 区间证明（产物臂 10 步到 C2–O3 1.82 Å，产物极小在 4.21 Å，外侧帧 vs 产物极小距离矩阵 RMSD 1.68 Å）。原因在平台：end_setting 的 IRC=(CalcFC,MaxPoints=100,StepSize=20) 被 route 里的 irc=calcfc 默认 10 点覆盖（declaration_0005 job 1308 逐帧能量与 0002 逐位相同即为证据）。
- **入口**：数值与行号 → `gold_compute/queue_20261018/results/NR1/REPORT.txt` §二 TS4（80 行，sha 6ddaa7ea…）、逐点与终稿 → `results/NR1/E4_GRID.md`（244 行，sha 029a497e…）、图 → `results/NR1/mechanism_graph.json`（190 行，sha 7aab6eae…，e4 barrier 64.93 带 provenance）、状态 → `results/NR1/CURRENT_STATE.md`（31 行，sha 16ad0870…）。
## HL1_E1（旧题线，已归档）· H3O+ → 肟氧质子转移鞍点归属补算

> 本节由 HL1_E1 计算道在 PROCESS.md 事故后重新追加；归档目录 `gold_fill_20261018/HL1/HL1_E1/` 与原生证据 `ts/ts_0022/` 未动。
> 结论：**candidate_only，HL1_E1 维持 0.0 约定值，不回填 ΔE‡**；停算性质 = 调度终止（用户 05:0x 指令），不是科学失败。
> 交叉参考：本文件另有一节「## HL1_E1（已归档为方法学对照，不再推进；本 lane 追加）」（复核 lane，约 L326），与本节的键长/能量读数逐项一致（O1–H4 2.3033、H4–N8 1.0267、O1···O9 2.5887、E −364.334597427、−254.4556 cm⁻¹、sha d4f9171d…），两节并存不冲突；本节的 job 归属以 run ts_0022 为准。

### 直接观测（run ts_0022；G16 / B3LYP/def2SVP + GD3BJ + Int(UltraFine) + SCF=Tight，气相 q=+1/m=1，19 原子）
- OptTS（job 1084；guess = T3 剖面 pt8 帧 sha 7018f688…）：E = **−364.290279158**（ts/ts_0022/jobs/declaration_0001/ts_opt/refine.log L1372，sha 1726d4b5…；L1546/1547 收敛、L1969 正常终止），R(1,2)=1.0679 / R(2,9)=1.4280 / R(1,9)=2.3937 Å。
- frequency（job 1093）：**恰 1 虚频 −254.4556 cm⁻¹**（declaration_0003/frequency/frequency.log L841/L850，sha d4f9171d…）。
- **(a) 方向闸门通过**：−img 为反应正方向时 δR(1,2)=**+0.0207 Å**（拉长）、δR(2,9)=**−0.0495 Å**（缩短）、û(O1→O7)·d(H2)=**+0.3555**（振幅比 0.69；对比历史 ts_0010 −67.9886 cm⁻¹ 的 ±0.0002 = 噪声级伪鞍点）。
- **(b) 三份额（无阈值）**：中心对 {1,2,9}=**0.2542**、全重原子=**0.0512**、最大单原子=H4 **0.4739**（H3O+ 不对称伸缩与 PT 联动，非 spectator，但落在声明对之外）。
- IRC（job 1099，declaration_0004/irc/irc.log sha b2f29746…）：双向各 **10 点被引擎默认上限截断**（L4952/L9070 `Maximum number of steps reached.`，L9413 正常终止）。FWD=声明方向（R(1,2) 1.086→1.235、R(2,9) 1.403→1.182，单调下坡），10 点内未到 B；REV 侧 H2 回 O1（1.002）同时 H4 走向 N6（1.832→1.549）。
- 端点：反侧 opt 首轮（job 1100）l103 `Bend failed for angle 1-4-8 / FormBX had a problem`；以该原生日志末帧重跑（job 1102）**收敛到 N-质子化肟 + 水**，E = **−364.334597427**（declaration_0005/reactant_opt/reactant_opt.log L18666，sha d010704f…），freq（job 1105，sha c5184477…）**0 虚频 / 51 模**。正侧 B 端点 Opt/Freq（job 1116）按停算指令撤回、从未起跑。

### 数值（同程序同方法同模型；×627.509474）
- E(TS) − E(B) = (−364.290279158) − (−364.295965289，gold A_RC_optfreq.log L15960) = **+3.5681 kcal/mol**
- E(TS) − E(N-质子化肟+水) = **+27.8101 kcal/mol**；E(N-质子化) − E(B) = **−24.2420 kcal/mol**
⇒ 该鞍点身份 = **B（O-质子化产物）↔ N-质子化肟+水 的质子中继鞍点**，不是声明步「接触离子对 → O-质子化产物」的鞍点。

### 缺环（逐字口径）
1. 声明起点 RC（质子留在 O1 的 H3O+···肟接触离子对）在本级别气相**不是极小值**（gold 5 种子全部坍缩到 B；本 run 反向 IRC 直达 N-质子化肟+水）⇒ ΔE‡ 无定义。
2. 双向 IRC 未达端点：平台 #184 —— irc 阶段 keywords 写 `IRC=(MaxPoints=60,StepSize=10)` 被 `compute_admission_rejected`；改写进 `end_setting` 过闸但生成输入 L4 仍是 `#p irc=calcfc …`（**静默丢弃**）⇒ 只能跑默认 ~10 点/方向。
3. 正侧 B 端点 Opt/Freq 未跑（job 1116 撤单）。
4. T3 pt8 的 +3.5705 kcal/mol 只是受约束弛豫剖面下界，且**峰两侧物种不同**（T3_ptscan_H2O9_relaxed.log 自 frame 10 起 H4 已到 N6，R(N6,H4)=1.061）。

### 0.0 约定口径三件并列
① 0.0 是**约定值不是测量值**（≠0 垒 TS，≠IRC 证明的无垒路径）；② pt8 +3.5705 仅为受约束剖面下界且峰两侧不同物种；③ 本步起点 RC 不存在。

### 【NY3 追加｜e0 构象连接结果】2026-10-18 06:16（job 1298）
- 事实：ts_0027(E1) 的本征矢跟随 minus 端（job 1294）落在 **HNCO·H2O 无氢键水旋转体极小值 −244.926200303**（0 虚频），不是声明的 RC(1152)（−244.935406907，N3–H4···O5 1.802 Å）。两者差 **+5.78 kcal/mol**，heavy RMSD 0.6972 Å；短 IRC 的 F 臂同向（F10 帧 H4···O5 已 3.232 Å）。
- 授权作业 1298：以旋转体为起点做松弛一维扫描 R(H4···O5) 3.8715→1.7915 Å（8 步 ×0.26，9 点，opt=(modredundant,maxcycle=200)），9/9 点收敛（步数 1/25/26/7/5/7/19/28/6）。逐点 E：−244.92620 / −244.92577 / −244.92863 / −244.92928 / −244.92973 / −244.92994 / −244.93096 / −244.93406 / −244.93540。
- 结论：构象势垒 **+0.27 kcal/mol（0.00043 Ha，在 R=3.61 Å 处）< 2**；末点与 RC(1152) Kabsch 重原子 RMS 0.0038 / max 0.0065 Å（all-7 0.0039）⇒ 同一极小值。**298 K 下 RC 与旋转体属同一反应物态，e1 用 RC 作分母成立**。
- 口径：e1 ΔE‡ 仍为 **+36.79 kcal/mol（分母 RC 1152）**；不以旋转体为分母的 +31.00 kcal/mol 对外报数；e0 的 0.27 不并入 e1。mechanism_graph 已加 `TS1.properties.intervening_conformer`（含 link_to_RC 子对象）。
- 日志：gold_compute/queue_20261018/results/NY3/guess_prep/E1_rot2RC_scan.log（sha 26b9210a99faa418）L51061 Summary 表；REPORT.txt 第十节。
- 盘面（06:2x 实测）：results/NY3/REPORT.txt 210 行 sha c709bfcf…、mechanism_graph.json 239 行 sha c6f5f2eb…（e1 36.79 / e2 11.06 / e3 43.13）。

## HL1 双面 [3+2]（HCNO + 降冰片烯；exo/endo 两通道）· 分子/团簇 QM 道 · 定稿 2026-10-18 07:2x
> 定位：本节是本道在 PROCESS.md 事故后重新追加的现役/定稿记录。方法与口径未变：Gaussian 16，B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight，气相，q0/m1，4c/6144MB/prio 0。数值一律取原生日志；面标签以 sdist/d(C10,C18) 判定，不用文件名。

### 直接观测（本道实测，可复核）
- **分离参考**（两面共用）：E_ref = E(降冰片烯) + E(HCNO) = −272.560718442 + (−168.452546517) = **−441.013264959 Ha**；norbornene 45 模 0 虚频（最低实模 257.12，[jobs/HL1_ref_norbornene_optfreq_b.log](gold_compute/queue_20261018/results/HL1/jobs/HL1_ref_norbornene_optfreq_b.log) L4295/L5300，NT L6730），HCNO 7 模（3N−5 线性）0 虚频（[jobs/HL1_ref_HCNO_optfreq_b.log](gold_compute/queue_20261018/results/HL1/jobs/HL1_ref_HCNO_optfreq_b.log) L1556，NT L1364）。
- **TS-endo（ts_0036）**：E = **−441.002183678**，**恰 1 虚频 −375.5525 cm⁻¹**，投影 (18,1) +0.2807 / (20,2) +0.1438 Å、C4=C5 −0.0389（同步缩短），最大单原子份额 C18 0.3494（非转子）⇒ [ts/ts_0036/jobs/declaration_0006/ts_opt/refine.log](ts/ts_0036/jobs/declaration_0006/ts_opt/refine.log) L18090/L18331/L18853（sha 2362634af64ec786）、[.../frequency/frequency.log](ts/ts_0036/jobs/declaration_0006/frequency/frequency.log) L936（sha 02ae57546cc327cc）。
- **TS-exo（ts_0037）**：E = **−440.994316600**，**恰 1 虚频 −426.7474**，投影 (18,1) +0.2618 / (20,2) +0.1301、C4=C5 −0.0409，最大单原子份额 C18 0.2742 ⇒ [ts/ts_0037/jobs/declaration_0001/ts_opt/refine.log](ts/ts_0037/jobs/declaration_0001/ts_opt/refine.log) L19448/L19688/L20211（sha 8af1d15947df3b95）、[.../frequency/frequency.log](ts/ts_0037/jobs/declaration_0001/frequency/frequency.log) L936（sha 18bfe94b6463bf4e）。
- **e_endo 反应物端**（declaration_0009）：E = −441.019350272，57 模 **0 虚频**（首条 Frequencies L922 = 21.9369；L912 的 −6.0983/−3.6395 是平动/转动投影残差，不计入 3N−6）⇒ [ts/ts_0036/jobs/declaration_0009/reactant_frequency/reactant_frequency.log](ts/ts_0036/jobs/declaration_0009/reactant_frequency/reactant_frequency.log) L552/L1729/L2206（sha 1ad6fc2a7f0108b2）；配套 opt 同值（job 1316，L39497/L39756/L40276，sha 26c7f9ce233f7429）。**与 ts_0037 通道络合物 −441.020095712 不是同一构象**（差 0.47 kcal/mol），两通道各有自己的预络合物，不强行统一。
- **e_endo 产物端**（job 1324，独立外框自由 opt+freq，起点 = ts_0036 产物侧 IRC 臂末点 r(18,1)=1.741）：E = **−441.098273730**，57 模 **0 虚频**（首条 Frequencies L11222 = 130.0548），**vs #1228(endo) 21 原子 Kabsch RMSD 0.0005 Å**（最大 0.0012 @O20）、vs #1229(exo) 1.2506 Å；sdist(18) = **+1.2768**、d(工作7,工作18) = **3.0466 Å**；与 #1228 的 −441.098273660 差 7×10⁻⁸ Ha ⇒ [jobs/HL1_armend_relax_ts0036.log](gold_compute/queue_20261018/results/HL1/jobs/HL1_armend_relax_ts0036.log) L9642/L9889/L10414、freq 段 L10852/L11222/L12093/L12719（sha 83aaf62bf84d455b）。
- **e_exo 两端**：反应物端 −441.020095712（57 模 0 虚频，sdist −3.2989、d(7,18)=5.4898，sha c0f0a2544852f992）；产物端 −441.095689377（0 虚频，vs #1229 RMSD 0.0007 Å，sdist −1.2691、d(7,18)=3.7068，sha 7a1b441be5ba3348）；第二独立证据 job 1319（[jobs/HL1_armend_relax_ts0037.log](gold_compute/queue_20261018/results/HL1/jobs/HL1_armend_relax_ts0037.log)，**sha 以定稿字节为准 = e478ab283cde92ef**，E L10709 = −441.095689377）。**更正**：此前记的 358be3287d8de54e 是发稿前快照，作废。
- **短 IRC（替代口径，两臂各 10 点）**：ts_0036 = 10 FORWARD 去产物侧 r(18,1) 2.211→1.741 + 10 REVERSE 回反应物侧 2.314→2.752（[irc.log](ts/ts_0036/jobs/declaration_0006/irc/irc.log) sha 43833bc9e35317db）；ts_0037 = 10 FORWARD 回反应物侧 2.255→2.669 + 10 REVERSE 去产物侧 2.159→1.725（[irc.log](ts/ts_0037/jobs/declaration_0001/irc/irc.log) sha e6205c623eecd396）。两臂均未闭合（反应物侧末点差 8.0、产物侧末点差 44.6 kcal/mol），只作方向区间。

### 结论（有证据支撑的部分）
- **ΔE‡（两面同一 E_ref）**：endo **+6.95**、exo **+11.89** kcal/mol；**ΔΔE‡ = 4.94 kcal/mol**，表述为「**约 5 kcal/mol 量级，倾向 C10 同侧（endo）**」，不作有效数字声明（单点能本征不确定度 ±1–2 kcal/mol；未做 ZPE/热校正）。
- 面选择性**只用 TS 相对同一分离参考**这一栏；ΔE(P_exo − P_endo) = +1.62 kcal/mol 是末态热力学差，不并入。两 RC 结合能（endo −3.61 kcal/mol）未做 BSSE/CP，只作参考、不进选择性。
- 产物立体化学：endo = `C1=NO[C@H]2[C@@H]3CC[C@@H](C3)[C@@H]12`、exo = `C1=NO[C@@H]2[C@@H]3CC[C@@H](C3)[C@H]12`；D65 三维判据 endo sdist(18)=+1.2771 / d(7,18)=3.0459，exo −1.2688 / 3.7066。

### 工具侧限制（非科学结论，已登记）
- ts_0036 / ts_0037 的 durable **verdict 均为 candidate_only**：ts_0037 报「reactant/product built MOL 与声明 SMILES 不符」，实测清 atom-map 后规范化 isomeric SMILES 与声明**逐字符相同（MATCH=True）**；ts_0036 报「几何/频率源/频率日志三者不一致」，实测三者 E 与关键距离相同（−441.019350272、d(1,18)=4.151、d(2,20)=3.302），差异是取向/原子顺序。⇒ 属 binding_status 标志问题；端点与成键结论由独立作业交叉核验，不依赖该 verdict。
- 平台 IRC 每臂上限 10 点（MaxPoints/StepSize 传不进 durable 流），故用「短 IRC 方向区间 + 两端 Opt/Freq 0 虚频 + interval proof」，**不宣称到达端点**。

### 缺口（如实登记）
1. 两面 IRC 两臂均未闭合（差额 8.0 / 44.6 kcal/mol），连接性由「方向区间 + 两端 0 虚频 + RMSD/sdist 身份」间接支撑，无线性能量闭合证明。
2. 两 RC 结合能未做 BSSE/CP 校正，未参与任何选择性数字。
3. e_endo 产物端用的是独立外框弛豫（job 1324），durable 流的 product_opt/product_frequency 未自动排上（run 已 ended），mechanism_graph 中已回填 status=done 并注明来源。

### 盘面
- [results/HL1/REPORT.txt](gold_compute/queue_20261018/results/HL1/REPORT.txt)（243 行，含 §0 编号/面定义/更正痕迹、§2 D65 数值、§4 能量、§8 定稿）；
- [results/HL1/mechanism_graph.json](gold_compute/queue_20261018/results/HL1/mechanism_graph.json)（359 行；6 节点 2 边，e_exo 11.89 / e_endo 6.95，selectivity value_kcal_mol 4.94 + value_statement、reference.E_ref）；
- 几何/面定义：[geoms/BUILD_PROVENANCE.md](gold_compute/queue_20261018/results/HL1/geoms/BUILD_PROVENANCE.md)、[geoms/TS_GUESS_PROVENANCE.md](gold_compute/queue_20261018/results/HL1/geoms/TS_GUESS_PROVENANCE.md)；复算脚本 geoms/build/{rmsd.py, mode_proj2.py, mode_proj3.py, irc_table.py, canon_check.py}。
## HI1 threo/erythro 胺氧化物 Cope 消除 · 主协调维护 · 07:44 更新

### 数值（原生日志，可复核）
- **e1 erythro syn = 12.82 kcal/mol**：TS −598.208585697（[ts_0038 frequency.log](ts/ts_0038/jobs/declaration_0002/frequency/frequency.log) L1214「1 imaginary frequencies」−940.1938、93 模）− 本底物极小值 −598.229013613（job 1224，93 实频）。
- **e2 threo syn = 14.74 kcal/mol**：TS −598.208059052（虚频 −1069.2742）− 本底物极小值 −598.231556225（job 1225）。**更正**：此前多处写 14.75，是同一差值 +0.023497173 Ha 的四舍五入差，已统一为 14.74（[REPORT.txt](gold_compute/queue_20261018/results/HI1/REPORT.txt) L130 与 §7 L225；CURRENT_STATE.md L32）。两数**不得相减**：分母是两个不同非对映底物。
- **e3 erythro regio = null（not located in this round）**：ts_0040 的 ts_opt（job 1292）07:42 实测 step 98/169，仍 running、无驻点 ⇒ 无 TS 能量可减，不编数值、不把 null 读成「不可计算」或选择性结论。措辞与下一步（ts_resume 补 reaction_center → freq 判唯 1 虚频 → 短 IRC 10+10 → 两端 Opt+Freq 0 虚频 + RMSD 身份）已写入 REPORT.txt §6（L193 起）。

### 已登记缺陷 / 缺口
- ts_0040 的 `reaction_center` 为空（declare.json:9、process.json:50/704），出 freq 前必须补「迁移 H + 离开/到达两个重原子」键对。
- e1/e2 的虚频模逐键净投影未给；两端 Opt+Freq 未完成（ts_0038 反应物端 job 1328 step 20/168、ts_0039 反应物端 job 1329 step 14/168，07:42）⇒ 目前只到「TS located + 唯 1 虚频 + 短 IRC 方向区间」，未达 (c) verified。
- 产物 E/Z 现有 TS guess + 参考 job 1325/1326 支撑，最终须在 IRC 产物端复读 C=C 两端二面角数值。

### 盘面
- [results/HI1/REPORT.txt](gold_compute/queue_20261018/results/HI1/REPORT.txt) 227 行 sha a02c3a0a…；[mechanism_graph.json](gold_compute/queue_20261018/results/HI1/mechanism_graph.json) sha ea20c406…（e3 显式 barrier_kcal_mol: null + 理由）；[CURRENT_STATE.md](gold_compute/queue_20261018/results/HI1/CURRENT_STATE.md) sha 0c8d0ff7…
### 07:57 更正：e1 分母改为 IRC 连通的最低极小值，12.82 → **16.62**（短 IRC 反应物臂弛豫出更低构象）
- **观测**：ts_0038 短 IRC 反应物臂末帧经 durable 流弛豫（job 1328，reactant_opt，07:47:24 完成）得 E = **−598.235079186**（[reactant_opt.log](ts/ts_0038/jobs/declaration_0002/reactant_opt/reactant_opt.log) L19086/L19730，Stationary point L20028，sha 1f33bb23eccbb803…），其 freq 作业 93 模 **0 虚频**（Low frequencies L1208 = −6.7330/−3.5826/−2.0507/−0.0007/−0.0004/0.0008 属平动转动投影残差，最低实模 46.51；NT L3797，07:56:02，sha dcd084a74d443ba6…）。该极小值比 e1 原分母 job 1224（−598.229013613）**低 3.81 kcal/mol**。
- **同一立体异构体**：33 原子同元素序；C2–N3 1.5463 vs 1.5654 Å、N3–O6 1.3520 vs 1.3504 Å；C2 有符号体积 −2.48 vs −2.38、C7 +2.54 vs +2.38（同号）⇒ (2R,7R) 未变；重原子 Kabsch RMSD 1.49 Å；两构象 O6 到 C1 甲基三个 H 都是 4.0–4.6 Å（都不是预组织构象）。
- **判定**：ΔE‡ 须以同底物最低已核极小值为分母 ⇒ e1 = −598.208585697 − (−598.235079186) = +0.026493489 Ha = **16.62** kcal/mol；12.82 作为 `barrier_conformer_specific_kcal_mol`（相对 job 1224，即 TS guess 母体构象）保留在 graph 中，不删不覆盖。
- **同时**：两条 syn 边的 `favored` 一律置 null（原 e1 favored=true 实质是跨非对映底物相减，违反本批口径）。
## 09:05 · 用户裁决「分母统一按稳定中间体」的执行结果
- **HI1**：e1 = **16.62**（分母 job 1328/1330, -598.235079186）、e2 = **15.85**（分母 job 1329/1331, -598.233321696）；两条 syn 边 favored 均 null（禁止跨非对映底物相减；且 16.62 vs 15.85 差 0.77 属近简并，按 repo 惯例 selectivity is None）。12.82/14.74 以 barrier_conformer_specific 保留（guess 母体 job 1224/1225，高 3.81/1.11）。**两端均已闭合**：e1 产物 job 1332/1334（-598.246098329, 0 虚频, NT 08:27:47, Z 烯烃）；e2 产物 job 1333/1335（-598.245557178, 0 虚频, NT 08:37:31, E 烯烃）。e3 因 ts_0040 撞 169/169 步数上限无驻点 => barrier null。
- **NR1**：e4 分母由 INT-1c 改为 INT-1a（-169.751090026）=> **68.85**（原 64.93，差 3.92）；e1 46.32（R_formamide 1210）、e2 22.80（INT-1a）、e3 7.25（节点对节点 INT-1b；对 INT-1a 的变体 10.80 记录不采用）。四条边均写 barrier_denominator（物种+job+E+理由）。
- **HL1**：分母改本通道预络合物 => e_endo **10.77**（RC -441.019350272）、e_exo **16.18**（RC -441.020095712），ΔΔE‡ **5.40**；旧分离参考口径 6.95/11.89/4.94 全部保留为 barrier_separated_reference 与 value_kcal_mol_separated_reference。RC 未做 BSSE/CP，只作身份层使用。
- **事故**：08:5x small_mol lane 以 read+write 整档回写把 HI1 的 REPORT/graph 覆盖为 236/212 行版本（本 lane 的 §8-§11 与 16.62/15.85 一度丢失），已在同文件重新落盘 REPORT **263 行 e99e9a9d**、graph **222 行 66712f49**。教训：同一交付文件禁止双 lane 并行整档写，只准单写权 lane 以 edit 局部追加。
- **threo 同理（待 freq 确认）**：ts_0039 反应物臂弛豫（job 1329，07:52:31 完成）E = **−598.233321696**（L20469，Stationary point L20773，sha 6cc2d7401ad1fa11…），比 job 1225（−598.231556225）低 1.11 kcal/mol；同 (2R,7R) 判据（C2 vol −2.389/−2.371、C7 vol −2.186/−2.377 同号、重原子 RMSD 2.9199 Å）⇒ 若其 freq 0 虚频，e2 = −598.208059052 − (−598.233321696) = +0.025262644 Ha = **15.85**（原 14.74）。
- **含义**：两面位移量不同（erythro −3.81、threo −1.11），故新旧口径下两底的相对大小会变；但因禁止跨非对映底物相减，报告中**不给出任何「谁快」的结论**，只给各自对自身最低极小值的 ΔE‡。
- 盘面（07:59）：[REPORT.txt](gold_compute/queue_20261018/results/HI1/REPORT.txt) 276 行 sha dc35ed68…（新增 §8 更正、§9 端点状态）；[mechanism_graph.json](gold_compute/queue_20261018/results/HI1/mechanism_graph.json) 209 行 sha 821a9538…；[CURRENT_STATE.md](gold_compute/queue_20261018/results/HI1/CURRENT_STATE.md) 39 行 sha afc3ab4f…
- **08:01 threo 端 freq 落地，e2 同口径更正 14.74 → 15.85**：ts_0039 反应物臂极小值 −598.233321696（reactant_frequency L670，93 模 **0 虚频**（Low frequencies L1212 全 ≥ −0.0005，最低实模 44.22），NT L3799 08:00:37，sha a143a1dbeb7e8c2c…）；−598.208059052 − (−598.233321696) = +0.025262644 Ha = 15.85（15.8525）。14.74 保留为 `barrier_conformer_specific_kcal_mol`（相对 job 1225，高 1.11 kcal/mol）。两端的位移量不同（erythro −3.81、threo −1.11），所以「谁快」的答案会随口径翻转——正因如此**不做跨非对映底物比较**，favored 一律 null。
- 盘面（08:02）：[REPORT.txt](gold_compute/queue_20261018/results/HI1/REPORT.txt) **309 行 sha 884a46be…**（§8 e1 更正、§9 端点状态、§10 e2 更正）；[mechanism_graph.json](gold_compute/queue_20261018/results/HI1/mechanism_graph.json) **217 行 sha 75fc4688…**（e1 16.62/12.82、e2 15.85/14.74、e3 null）；[CURRENT_STATE.md](gold_compute/queue_20261018/results/HI1/CURRENT_STATE.md) **39 行 sha 9256a809…**







