# HL1_E1 鞍点归属补算 · 终报（2026-10-18 05:xx，按「替换题停算」指令归档）

边：**HL1_E1**（hard/HL1.json 第 1 步：H3O+ 把质子交给肟氧）／ task id：HL1（旧题，已在题库保留历史值，等待被 HCNO+降冰片烯替换）
工作目录：gold_fill_20261018/HL1/HL1_E1/；durable run：**ts_0022**（/home/ly/Cloudra-mechanism-agent/ts/ts_0022）
方法（全流程同一口径）：Gaussian 16，B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight，**气相**，q=+1 / m=1，19 原子 C4H12NO2+，51 模。
停止记录：主协调广播 evt_1368eb1b076741ac（用户 05:0x「被换掉的题的任务可以杀了」）⇒ ts_stop(ts_0022, rev→49+)；排队中的 product_opt **job 1116 已撤（cancelled，从未起跑）**。全部日志/几何原样保留。

## 边 → job id → 卡在哪一环

| 环节 | job | 结果 | 卡点 |
| --- | --- | --- | --- |
| OptTS（pt8 guess） | 1084 | done，收敛 | — |
| frequency | 1093（1086 撤单重发） | done，**恰 1 虚频 −254.4556 cm⁻¹** | — |
| IRC 双向 | 1099 | done，但**双向各 10 点被引擎默认上限截断** | 平台无入口设 MaxPoints（见下） |
| 端点 opt（反侧，IRC 帧直起） | 1100 | **failed** l103 `Bend failed for angle 1-4-8` / FormBX | 冗余内坐标崩坏（同类于 gold job 921） |
| 端点 opt（反侧，改 seed=1100 末帧） | 1102 | done，收敛 | — |
| 端点 freq（反侧） | 1105 | done，**0 虚频 / 51 模** | — |
| 端点 opt+freq（正侧 = 声明产物侧） | 1116 | **未起跑即按停算指令撤回** | 缺 **B 侧本 run 端点 Opt/Freq** |

## 原生日志与摘要（sha256 / 行号）

| 文件（绝对路径） | sha256 | 关键行 |
| --- | --- | --- |
| /home/ly/Cloudra-mechanism-agent/ts/ts_0022/jobs/declaration_0001/ts_opt/refine.log | 1726d4b5fab08d4ecca81a487e69cc2396487cdc7ac18ff7591eb45e780ec598 | L1372 `SCF Done: E(RB3LYP) = -364.290279158`；L1546–1547 `Optimization completed.`/`Stationary point found.`；L1969 `Normal termination` |
| /home/ly/Cloudra-mechanism-agent/ts/ts_0022/jobs/declaration_0003/frequency/frequency.log | d4f9171d2430f18620ef8100c091e632a36a824bc76e57656f60f8c4668f4aad | L510 `SCF Done = -364.290279158`；L841 `1 imaginary frequencies`；**L850 `Frequencies -- -254.4556 48.8070 86.3945`**；L1972 `Normal termination` |
| /home/ly/Cloudra-mechanism-agent/ts/ts_0022/jobs/declaration_0004/irc/irc.log | b2f2974677120745f1e060dcb286a7ce524749f1c96d0a4eaa39903212e741c8 | L4952 / L9070 `Maximum number of steps reached.`；L9072 `Reaction path calculation complete.`；L9413 `Normal termination` |
| /home/ly/Cloudra-mechanism-agent/ts/ts_0022/jobs/declaration_0005/reactant_opt/reactant_opt.log | d010704f59ad083824dc90cba4889163fcb802f9d3daae7672fa7975af02f29a | L18666 `SCF Done = -364.334597427`；L18868–18869 `Optimization completed.`/`Stationary point found.`；L19301 `Normal termination` |
| /home/ly/Cloudra-mechanism-agent/ts/ts_0022/jobs/declaration_0005/reactant_frequency/reactant_frequency.log | c51844775bfc8a2417029653cfec05178e984c7de870b944f08e71f78bcdd72f | L510 `SCF Done = -364.334597427`；**无 imaginary 横幅，51 个频率（L849 起 44.4026…）**；L1968 `Normal termination` |
| /home/ly/Cloudra-mechanism-agent/ts/ts_0022/jobs/declaration_0004/reactant_opt/reactant_opt.log（失败件） | 见 run 目录 | L17600–17602 `Bend failed for angle 1 - 4 - 8` / `FormBX had a problem.` / l103 `Error termination` |

## (a)(b)(c) 逐项

**(a) 方向（硬闸门）：通过。** 模矢（frequency.log L852 起的逐原子表，0.1 Å 标度、以 −img 为反应正方向）：
- δR(1,2) = **+0.0207 Å**（拉长 = break ✓）；δR(2,9) = **−0.0495 Å**（缩短 = form ✓）
- û(O1→O7)·d(H2) = **+0.3555**（|d(H2)| = 0.4734，cos ≈ 0.75）⇒ H2 沿 O1→O7 输送
- 振幅比 0.4734 / 0.6875 = **0.69**（非噪声级）。对比历史 ts_0010 的 −67.9886 cm⁻¹：+0.0002 / −0.0000 Å，属伪鞍点。

**(b) 份额（记录项，不设阈值）**：声明反应中心对 {1,2,9} = **0.2542**；该模全部重原子 {1,5,6,7,8,9,10} = **0.0512**；**最大单原子 = 原子 4（H4，H3O+ 的另一个质子）0.4739，主分量 y**。
逐原子：H4 0.474 / H2 0.225 / H3 0.137 / H16 0.091 / O1 0.021 / N6 0.013 / O7 0.008。
归属：H2+H3+H4+O1 联动的 **H3O+ 给体不对称伸缩 + 质子转移**，**不是**甲基转动/水取向 spectator；但最大份额落在声明对之外（H4），按裁决 (b) 如实登记，不标 soft-mode-dominated。

**(c) 交付：不通过（candidate_only，不回填）。** 三环里只完成一环半：
- TS 恰 1 虚频 ✓（1093）
- **双向 IRC 未达声明端点**：FWD 侧 10 点内只走到 R(2,9)=1.182（B 是 1.077），仍在下坡；REV 侧落点在 **N-质子化肟 + 水**（R(N6,H4)=1.549、R(1,2)=1.002），**不是**「质子留在 O1 的接触离子对」，且两侧均被引擎默认 10 点截断。
- 反侧端点 Opt+Freq 已做（0 虚频）✓，但它是 **N-质子化肟+水**，不是声明反应物；**正侧（B）端点 Opt/Freq 未跑**（1116 按停算指令撤回）。

## 纯电子能（同程序同方法同模型；Ha → kcal/mol × 627.509474）

| 物种 | E / Ha | 来源（本 run 或 gold，均为同一 Gaussian 16 / B3LYP/def2SVP+GD3BJ+UltraFine+SCF=Tight 气相） |
| --- | --- | --- |
| TS（本 run，pt8 鞍点） | **−364.290279158** | ts_0022 refine.log L1372 = frequency.log L510 |
| 反侧端点极小值（本 run，**N-质子化肟 + 水**，0 虚频） | **−364.334597427** | reactant_opt.log L18666 = reactant_frequency.log L510 |
| 产物侧极小值 B（gold，O-质子化肟 + 水，0 虚频） | −364.295965289 | gold_finish_20261015/HL1/ts_run/jobs/A_RC_optfreq.log L15960（sha256 dd2736788cb8e0fc…） |
| T3 剖面 pt8（受约束弛豫） | −364.290279（−364.290279321 末步） | T3_ptscan_H2O9_relaxed.log L17400（sha256 40ce3be2…） |

- E(TS) − E(B) = (−364.290279158) − (−364.295965289) = **+0.005686131 Ha = +3.5681 kcal/mol**
- E(TS) − E(反侧 N-质子化极小值) = (−364.290279158) − (−364.334597427) = **+0.044318269 Ha = +27.8101 kcal/mol**
- E(N-质子化极小值) − E(B) = **−0.038632138 Ha = −24.2420 kcal/mol**（比 gold job 978 的 −364.326887674 还低 0.00771 Ha = 4.84 kcal/mol，属更有利构象/离子对分离）
- E(TS) − E(T3 pt8) = **+1.4×10⁻⁷ Ha**（OptTS 基本停在 pt8 帧）

⇒ 该鞍点是 **B（O-质子化产物）↔ N-质子化肟+水** 的质子中继鞍点（水分子把质子从 O7 侧接回、再交给 N6），**不是**声明步「接触离子对 → O-质子化产物」的鞍点。

## 第⑦项（缺哪一环）——逐字口径

1. **声明反应物（质子留在 O1 的 H3O+···肟接触离子对）在本级别气相不是极小值**：gold 5 个种子全部坍缩到 B；本 run 的反向 IRC 直接走到 N-质子化肟 + 水。故「本步自身起点极小值」不存在，ΔE‡ 无定义。
2. **双向 IRC 未达端点**：受平台限制（#184），ts_prepare 的 irc 阶段 keywords 里写 `IRC=(MaxPoints=60,StepSize=10)` 被 `compute_admission_rejected` 拒（原文 expected 含 irc 选项 / actual 不含）；改写进 `end_setting` 虽过闸，但生成的 irc.gjf L4 仍是 `#p irc=calcfc …`（**end_setting 被静默丢弃**）。⇒ 实际只跑了引擎默认 ~10 点/方向。
3. **正侧（B）端点 Opt/Freq 未完成**：job 1116 按停算指令撤回（从未起跑），因此「TS 正侧到达 B」目前只有 IRC 方向证据（R(2,9) 1.403→1.182 单调下坡）+ gold 的 B 极小值，**没有本 run 的 B 端点 51 模 0 虚频件**。
4. **pt8 的 +3.5705 kcal/mol 只是受约束弛豫剖面值（下界口径），不是测量能垒**；且该剖面峰两侧**不是同一物种**——T3_ptscan_H2O9_relaxed.log 自 frame 10 起 H4 已转到 N6（R(N6,H4)=1.061 Å，E 由 −364.2906 跳到 −364.3006），即高 R 侧是 N-质子化肟+水。

## 0.0 约定口径（三件并列，缺一不批）

1. **0.0 是约定值（convention value），不是测量值**：语义 = 本级别气相不存在该声明步的独立鞍点 / 相对该步自身起点无实测能垒；**不是 0 垒 TS，也不是 IRC 证明的无垒路径**。
2. **T3 剖面 pt8 = 相对 B 的 +3.5705 kcal/mol 仅为受约束弛豫剖面的下界**，且峰两侧物种不同（见上），不能当 ΔE‡。
3. **该步的起点 RC（质子留在 O1 的接触离子对极小值）不存在**：gold 5 个种子 + 本 run 反向 IRC 两端证据一致。

## 回填建议（归档版；按停算指令本线不再提交新作业）

- **建议维持 HL1_E1 = 0.0（约定值）**，不回填任何 ΔE‡。理由：(c) 三环未齐；(a)(b) 通过的 −254.4556 cm⁻¹ 鞍点经 IRC 方向 + 反侧端点频率证明属于 **B ↔ N-质子化肟+水** 的质子中继通道，不是本步。
- 若将来该题重新启用，最小补测清单：① 正侧（B）端点 Opt+Freq（0 虚频 + 身份）；② 能设 IRC 步长的入口（或改用 LQA / stepsize=5、maxpoints≥40）把两侧真正推到端点；③ 若要给「接触离子对 → 产物」的 ΔE‡，还必须先找到一个**质子留在 O1** 的极小值（本级别气相至今未找到）。
- 影响面：只涉及 HL1 的五步图第 1 步数值语义；不动 gold_finish_20261015 下任何文件、不动 method_policy、不动题库 JSON。
