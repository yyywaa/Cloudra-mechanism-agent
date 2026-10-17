# HL1_E1 交付决策与证据包（终值 v1 · 2026-10-17）

包：gold_finish_20261015/HL1（边 HL1_E1 = hard/HL1.json 的 L1 第 1 步）
Coordinator：as_939ca5a73ff445c2（接任）；工作根：/home/ly/Cloudra-mechanism-agent
方法：Gaussian 16（/home/ly/g16/g16）B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight，**气相**，q=+1 / m=1，19 原子 C4H12NO2+（51 模）。手工作业 8c/10240MB/priority 0。

## 0 交付结论（一行）

**HL1_E1 = 0.0 kcal/mol**，语义 = **声明方向（接触离子对 → O-质子化产物）无合格鞍点 / 相对该步自身起点无垒**；参考态改判为接触离子-分子对（题面声明的 RC（质子留在 H3O+ 的 O1 上）在本级别不是驻点）。**反向（产物侧 B → 接触离子对方向）的受约束弛豫剖面存在内部极大 pt8 ≥ +3.5705 kcal/mol（相对 B，仅下界）；该 pt8 帧不是已验证鞍点**（详见 §8）。

**口径加固（2026-10-17 R8.1，主协调裁定）**：0.0 是**「无独立鞍点」的约定值（convention value）**，语义 = 本级别气相不存在该步的独立鞍点/能垒，**不是**「0 垒 TS」，也**不是**「IRC 证明无垒」；参考态 = 接触离子-分子对。硬档测试 `tests/test_benchmark.py::test_hard_replacement_and_hl1_reframed_graph` 的期望表已由本包唯一写权会话同步为 `[0.0, 23.13, 10.44, 13.46]`（L2138；改后文件 sha256 037a424b05cc5d28f0bd2540af456aedf034908d5e59525b356994d38bd8d014），三守卫输出见 HL1/STATUS.md §22。

⚠ 引擎偏差（必须在交付中显式声明）：题源既有 gold 口径为 **ORCA 6.1.1**（B3LYP-D3(BJ)/def2-SVP、RIJCOSX/def2-J、TightSCF）；本机无 ORCA，本包全部数值为 **Gaussian 16**，泛函/基组/色散/溶剂模型同级但**程序不同**。本包所有能量只在**同一程序、同一批日志**内相减，绝不与他机 ORCA/旧 Gaussian 值（23.13 / 10.44 / 13.46 / 0）混减，也绝不复用旧值。

## 1 声明与口径

- 步定义（registry 原文）：`out` = `[O:1]([H:9])[H:10].[CH3:11][CH2:5]/[C:4](=[N:6]/[O+:7]([H:8])[H:2])/[CH3:3]`，`type` = "proton transfer from H3O+ to the oxime OH (leaving-group activation)"；mapped reactant = `[O+:1]([H:2])([H:9])[H:10].[CH3:11][CH2:5]/[C:4](=[N:6]/[O:7][H:8])/[CH3:3]`。
- 原子序（1-based，本包全线统一）：1=O1(H3O+/水的 O)、2=H2(声明转移质子)、3=H4、4=H10、5=C11、6=C5、7=C4、8=N6、9=O7(肟 O)、10=C3、11-13=H(C11)、14-15=H(C5)、16=H8(肟 OH 的 H)、17-19=H(C3)。反应中心：break [1,2] / form [2,9]。
- 参考极小值口径（题面 prompt 逐字）：bimolecular 步的起点极小值 = RC 反应络合物；ΔE‡ 为**纯电子能**（无 ZPE/热校正），换算 627.509474 kcal/mol per Hartree。

## 2 决定依据

### 2.1 该步的「起点极小值」在本级别气相不存在（5 个独立种子全部坍缩）

| job | 种子/构造 | 原生日志（gold_finish_20261015/HL1/ts_run/jobs/） | 日志 sha256 | 末步 SCF / Ha | 模数·虚频 | 末帧 R(1,2)/R(2,9)/R(1,9) Å | 落点 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 904 | A_RC_optfreq.gjf，d(O1···O7)=2.60 Å，H2 在 O1 | A_RC_optfreq.log | dd2736788cb8e0fc01914efbf02c91c40408d97bb17e456c354d2a8a621c781e | −364.295965289 | 51 / **0** | 1.3812 / 1.0774 / 2.4569 | 产物侧 B |
| 905 | A_PC_optfreq.gjf（产物种子对照） | A_PC_optfreq.log | f62601ab694362f90183e282e15c9a00bf91826143f4787b3135bd67cc0b5040 | −364.295965287 | 51 / **0** | 1.3810 / 1.0774 / 2.4568 | 同 B（逐原子最大偏差 0.0031 Å） |
| 920 | C2_RC3A_optfreq.gjf，d(O1···O9)=3.00 Å | C2_RC3A_optfreq.log | 01c7b36f48170832a44652217c1796242969fd95befe3137413e08650f11c559 | −364.295965302 | 51 / **0** | 1.3810 / 1.0774 / 2.4568 | 同 B |
| 965 | E2_RCbi_optfreq.gjf（双齿螯合 pose） | E2_RCbi_optfreq.log | a4d182472ff195ac8c1e6bbc3a2c5a57e8daa67b29a45fee470c4a235d6e0dcf | −364.295965301 | 51 / **0** | 1.3811 / 1.0774 / 2.4568 | 同 B |
| 966 | E2_RC35A_optfreq.gjf，d(O1···O9)=3.50 Å | E2_RC35A_optfreq.log | 48da3dcb0ca8e2bce3e9e3d67a15bf7d46bb6abcc963b0296b1499776302a384 | −364.295777129（= B′） | 51 / **0** | 1.3878 / 1.0740 / 2.4601 | B′（比 B 高 0.1181 kcal/mol） |
| 978 | E2_RC42A_optfreq.gjf，d(O1···O9)=4.20 Å | E2_RC42A_optfreq.log | 9450eb9d48fcfbba6e30388ffe2b5a6d5ab760bb39fc95ff508ef93fa3e09505 | **−364.326887674** | 51 / **0** | 见 2.2b | **N-质子化肟 + 水**（更深的另一个极小值） |

判别式（本包预先声明并在每份日志上执行）：**R(1,2) ≤ ~1.05 Å 且 R(2,9) ≥ ~1.4 Å = 「质子留在 O1」的 RC 型驻点**；R(1,2) ≈ 1.38 / R(2,9) ≈ 1.08 = 产物侧复合物。5 个「质子留在 O1」的种子无一满足前者。

### 2.2 唯一一次真实 TS 搜索（durable 管线 ts_prepare → ts_0010）只给出**甲基转动伪鞍点**

| job | 文件（= /home/ly/Cloudra-mechanism-agent/ts/ts_0010/jobs/declaration_0001/） | sha256 | 关键原文行 | 内容 |
| --- | --- | --- | --- | --- |
| 975 | ts_opt/refine.log（输入 ts_opt/refine.gjf，route `#p opt=(TS,calcfc,noeigen) B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight`，`1 1`） | d7ab3228d830b140bbec0f83c3597c9b331666763fc2f1597a9b6f76d43144e7（gjf 19e0cc6d652f3e7bef9cbd4cfc1126ab1f6f14b60673697a3b217b8bd895c0af） | L23071 SCF −364.295414931；L23249–23250 `Optimization completed.` / `-- Stationary point found.`；L23671 `Normal termination`（2026-10-16 00:17:53） | TS 优化收敛 |
| 986 | frequency/frequency.log | 9074df8074476386e05bbc2f89124aca6a453298270ce9cc418346bd0e575fed | L524 SCF −364.295414931；L855 `****** 1 imaginary frequencies (negative Signs) ******`；L864 `Frequencies -- -67.9886 25.2962 65.4614`；L1987 `Normal termination`（2026-10-17 06:27:49） | 恰 1 虚频 |
| 988 | irc/irc.log（输入 irc.gjf，`irc=calcfc`） | ce6f2b3a4356b31d45d3d450175343c175e14095a6c4d00f809012655b13808a（gjf d60706e896261a1202cad06c128eb33427a74eae6ae2fd44e9b8847b386b85d1） | L859/L861 `Point Number: 0` / `Point Number 1 in FORWARD path direction.`；全程 21 个 `SCF Done`，能量平在 −364.2954159 附近；末 `Delta-x Convergence NOT Met` / `Maximum number of corrector steps exceded` / `l123`（2026-10-17 06:30:52） | **IRC 未完成**（仅 FORWARD point 1） |

**(a) 虚频模归属（frequency.log L866–L886 逐原子表，mode 1 列三分量取模长）**

| 原子 | 归属 | 位移模长 | 结论 |
| --- | --- | --- | --- |
| 1 | O1（H3O+/水的 O） | 0.000 | 不动 |
| 2 | **H2（声明转移质子）** | **0.028** | 几乎不动（仅为最大分量的 4%） |
| 9 | O7（肟 O） | 0.046 | 几乎不动 |
| 17 / 18 / 19 | **C3 甲基的三个 H** | **0.469 / 0.628 / 0.587**（17 与 18/19 反相，分量和≈0 = 扭转） | 主导位移 |

Red. masses = 1.0990、Frc consts = 0.0030 mDyne/Å（L865/L866）= 单氢转子量级。
⇒ **该虚频模与声明键对 [1,2]/[2,9] 基本无关**，是产物侧复合物上 C3 甲基转动的软模；按 BRIEF §4 第 1 条（虚频模必须以声明键对为主）与 §9 第 3 条，**属 pseudo-saddle，不得当该步 TS**。

**(b) 该驻点的几何与能量都落在产物侧**：ts_opt 收敛几何（= irc.gjf 起点坐标）实测 **R(1,2)=1.387 / R(2,9)=1.074 / O1···O7=2.460 Å**，与产物侧极小值 B（1.3811 / 1.0774 / 2.4568）几乎同构、只差甲基朝向；E(TS) − E(B) = (−364.295414931) − (−364.295965289) = +0.000550358 Ha = **+0.3454 kcal/mol**。
⇒ **+0.3454 kcal/mol 只是「B 上甲基转动 pseudo-saddle 相对 B」的差，不是该步能垒**（本包在 registry 注释、hard.md 行与本文档中三处明写此语义，防止被误读成 E1 的 ΔE‡）。

**(c) guess 本身是「质子居中」的桥式帧**（gold_finish_20261015/HL1/ts_run/path/input_0001/provided.xyz，provenance 见 path/input_0001/provenance_0000.md；IDPP 内插 frame 表）：r(O1–H2)=1.280、r(H2–O9)=1.306、O1···O9=2.584 Å。
⇒ TS 搜索从**真正的候选 PT 鞍点几何**出发，仍滑到产物侧、只收敛出甲基转动软模。

### 2.3 job 978 的竞争通道（N-质子化肟 + 水）

E2_RC42A_optfreq.log（sha256 9450eb9d…）：L31253/L32228 `SCF Done` = **−364.326887674**；L31454 / L33303 `Optimization completed.`；L31878 / L33798 `Normal termination`（2026-10-16 00:46/00:47）；频率段 L32557–L32558 首值为 4.7863 / 64.6417 cm⁻¹（前 6 个为投影平动转动残值）⇒ **0 虚频**、51 模。
末帧坐标（L32129 起标准取向块）逐原子复算：**d(N6–H3)=1.060、d(O1–H3)=1.626、d(O1···N6)=2.681、d(O7–H8)=0.973、d(C4–N6)=1.292、d(N6–O7)=1.353、d(O1···O7)=3.469 Å**
⇒ 结构 = **N-质子化肟 + 水**氢键复合物（质子落在 N6 上，水以 O1–H3···N6 短氢键相连）。
⇒ 比 O-质子化的 B（−364.295965289）**低 19.4041 kcal/mol**（同程序同批）。**影响面**：E2/E3/E4 既有值（23.13 / 10.44 / 13.46，ORCA）全部是「以 O-质子化分支（I2 / I3′）为参考态」的口径；N-质子化是更深但**不导向迁移**的旁观/死端通道（Beckmann 的离去基团活化必须走 O-质子化），故本包**不改图、不改 E2/E3/E4**，只把「不得把 N-质子化态当作第 1 步的起点参考态」写入 caveat。

### 2.4 搜索充分性（逐项；**不得**写成「IRC 报错 ⇒ 无鞍点」）

- 起点方向（O1→O7 质子转移）：5 个种子全部坍缩（2.1）——该步**未找到**「质子留在 O1」的驻点。
- 鞍点搜索：durable ts_prepare/ts_0010 一次真实 TS 搜索（job 975/986），从质子居中桥式 guess 出发，只得到甲基转动 pseudo-saddle（2.2）。
- IRC（job 988）**只作**「软模下积分无法推进（仅 FORWARD point 1、能量平在 −364.2959159 附近）+ 平台缺陷 #184（ts_prepare 声明层无法设 IRC 步长/算法）」的登记；**连通性不得写成「IRC 已双向到达端点」**。
- 反例边界（已证伪的四条旧剖面，不能作为任何能垒/无垒证据）：912（起点即 B、第 11 点 NStep=88 l9999）／913（点 1 即 l103 `Error imposing constraints`，零收敛点）／921（Berny 冗余坐标崩坏 `Tors failed for dihedral 3-1-9-16 / 4-1-9-16` + `FormBX had a problem.`，零收敛点）／930（单点 88 步耗尽 l9999，O···O 几乎未动）。
- **结论表述**：该步在 O1→O7 方向**未找到合格鞍点**（起点极小值不存在 + 唯一的 TS 搜索给出伪鞍点），因此按 BRIEF §9 第 4 条记「无独立鞍点」并以 0.0 承载该无垒步。

## 3 数值台账（同一程序同一批 Gaussian 16，纯电子能，Ha → kcal/mol ×627.509474）

| 物种/驻点 | E / Ha | 相对 B / kcal/mol | 证据 |
| --- | --- | --- | --- |
| B = O-质子化肟 + H2O（产物侧极小值，0 虚频） | −364.295965289 | 0.0 | A_RC_optfreq.log（dd273678…）等 4 份同驻点日志 |
| B′（B 的另一构象，0 虚频） | −364.295777129 | +0.1181 | E2_RC35A_optfreq.log（48da3dcb…） |
| TS-candidate（甲基转动伪鞍点，1 虚频 −67.9886） | −364.295414931 | **+0.3454（非该步能垒）** | refine.log（d7ab3228…）+ frequency.log（9074df80…） |
| N-质子化肟 + H2O（竞争通道极小值，0 虚频） | −364.326887674 | **−19.4041** | E2_RC42A_optfreq.log（9450eb9d…） |
| 分离 H3O+ + 肟单体 | 待 CALC4-T2 | — | round4/CALC4_REPORT.md（在跑） |

**HL1_E1 采用值 = 0.0**（无独立鞍点 / 无垒离子-分子质子转移）；相对分离反应物的沉没口径待单体落地后补充，仅作说明用、不改主值。

## 4 证据驱动的机理修订（旧 → 新）

| 项 | 旧（题源/历史） | 新（本批证据） | 依据 | 影响面 |
| --- | --- | --- | --- | --- |
| E1 值 | `null`（未填）；另有一条已作废的旧 `0`（旧 WSL Gaussian 13 点约束扫描，不得复用） | **0.0** = 无独立鞍点 / 无垒离子-分子质子转移 | 2.1–2.4 | 仅 E1 自身；E2 起点（题面 `out` = O-质子化肟 + 水）不变 |
| E1 参考态 | 声明的 RC（H3O+ 与肟的离子-分子络合物，质子仍在 O1） | **参考态改判为接触离子-分子对**（声明的 RC 在本级别气相不是驻点） | 2.1（5 种子坍缩） | E1 的 ΔE‡ 语义；不改变图节点/边与其它步数值 |
| 竞争通道 | 未记录 | **N-质子化肟 + H2O 是更深的极小值（比 O-质子化 B 低 19.4041 kcal/mol）** | 2.3 | 仅作 caveat 与竞争通道登记；不改图、不改 E2/E3/E4 |
| 引擎 | ORCA 6.1.1（既有 gold） | Gaussian 16（本批全部数值） | §0 | 程序差异必须随交付声明；跨程序不混减 |

## 5 回填记录（本轮已完成；守卫输出原样）

| 文件 | 改前 sha256 | 改后 sha256 |
| --- | --- | --- |
| cloudra/benchmark/hard_registry/jl.py（L1 第 1 步加 `"barrier": 0.0` + 依据注释） | 7ed4e63a720ee6fced06cad5bd46811d59214732133b56220d76a75e56cc805c | 706592ea2c5e70d1bc393295340d4fe365e45061d4709a0cb1e22b104757822c |
| ideapool/reaction_candidates/hard.md（仅 L1 行第 145 行） | 4ca22fc3d99339dfec73a59669a3e9cb742861da018f2af56e44c650b0cf903f | 4940fa667289ed038c888f8d63f84f6c301b123681f5982158b5a8b93e70a089 |
| ideapool/tasks/hard/HL1.json（重生成；HL1_E1 null → 0.0） | 38081ed09c86db4acbf0e5e57d5cb65728d81dd0c15d44e0e4814b1f955384ae | 240865b13d28a1fb13f1cd5fe7211a993bc33fe413c60d2b3adbb67cc9db1678 |
| gold_finish_20261015/HL1/STATUS.md（§18） | 802b113f0ad514d5abe7b395544c2ea7b135ea9c7f17096e33af86e042bbe7f0 | 10b04df073032b1b1506e2ad165ffaa85fcf214b13679f8a5a2801d71098a21c |

生成（只重生成 HL1.json，避免动其它包的 hard 题面）：
```
cd /home/ly/Cloudra-mechanism-agent
python3 -c 'import json; from cloudra.benchmark import gen_hard_tasks as g; tasks=g.parse_hard_md(g.DEFAULT_SRC, only={"L1"}); t=tasks[0]; out=g.DEFAULT_OUT/(t.task_id+".json"); out.write_text(json.dumps(t.model_dump(mode="json", by_alias=True), ensure_ascii=False, indent=2), encoding="utf-8"); print("wrote", out); print("edges:", [(e.id, e.barrier_kcal_mol) for e in t.gold.mechanism_graph.edges])'
# wrote /home/ly/Cloudra-mechanism-agent/ideapool/tasks/hard/HL1.json
# edges: [('HL1_E1', 0.0), ('HL1_E2', 23.13), ('HL1_E3', 10.44), ('HL1_E4', 13.46)]
```
守卫（原样输出）：
```
$ python -m pytest tests/test_benchmark.py -k regenerate_identically
....                                                                     [100%]
4 passed, 185 deselected in 0.88s
```
表格陷阱防护（NI5 教训）：改 md 后**同轮**重解析 L1 行 = 8 个单元格（= 表头 8 列），无裸竖线；生成物 `git diff ideapool/tasks/hard/HL1.json` **仅 1 行**（`"barrier_kcal_mol": null` → `0.0`），元素/重原子/方法白名单等元数据字段未受影响。

## 6 残余缺口与可推翻点

1. **完整 PT 弛豫剖面（有无内部极大）仍未测**：913/921/930 全部无可用收敛点；CALC4-T3（从 B 出发的 ΔR 或等价稳健构造）在跑。
2. 「无合格鞍点」的严格性上限：ts_prepare 只证明「从质子居中桥式 guess 出发未找到合格 PT 鞍点，只落到甲基转动伪鞍点」；严格性依赖第 1 项剖面。
3. 分离 H3O+ / 肟单体能量未测（CALC4-T2），故「相对分离反应物的沉没垒」暂缺。
4. T3c/T3d/T3e 反向/侧向剖面只有输入无结果（explorer R3 已登记）。
5. **可推翻点**：若 CALC4-T3 剖面出现内部极大并据此找到合格 PT 鞍点（1 虚频且模以 [1,2]/[2,9] 为主），则 E1 应改为 E(TS) − E(该步起点极小值)，本包回填随之修订。
   - **R14 已裁决（2026-10-17）**：T3 剖面（job 1005）**确有**受约束内部极大 pt8 ≥ +3.5705 kcal/mol（相对 B，仅下界），但**未据此找到合格 PT 鞍点**（无频率/IRC 验证、峰后换通道）⇒ 按 R14.2 维持 HL1_E1 = 0.0，措辞按 §8 限定。

## 7 复现命令（只读）
```
grep -n "imaginary frequencies\|Frequencies --" ts/ts_0010/jobs/declaration_0001/frequency/frequency.log | head
sed -n '855,890p' ts/ts_0010/jobs/declaration_0001/frequency/frequency.log     # 虚频模逐原子位移
sed -n '23240,23252p' ts/ts_0010/jobs/declaration_0001/ts_opt/refine.log      # 收敛原文
tail -20 ts/ts_0010/jobs/declaration_0001/irc/irc.log                          # l123 失败原文
grep -n "SCF Done\|Frequencies --" gold_finish_20261015/HL1/ts_run/jobs/E2_RC42A_optfreq.log | tail -6
```

## 8 R14 登记：T3 受约束剖面、措辞限定与证据（2026-10-17，主协调裁定 R14.2 / R14.4b；本包写权会话落盘）

**措辞限定（定稿口径，不得再简写为「无独立鞍点 / 无垒」）**：HL1_E1 = 0.0 kcal/mol 的语义 = **声明方向（接触离子对 → O-质子化产物）无合格鞍点 / 相对该步自身起点无垒**；**反向（产物侧 B → 接触离子对方向）的受约束弛豫剖面存在内部极大 pt8 ≥ +3.5705 kcal/mol（相对 B，仅下界）**；pt8 帧**不是已验证鞍点**（其是否为自由 PES 一阶鞍点未经管线 OptTS+freq 判定）。只是下界的两条理由：0.05 Å 网格分辨；**pt10 → pt11 单步跌 5.88 kcal/mol**（−364.291229930 → −364.300603835）说明峰后剖面**换通道**（H4→N6），pt8 的「单步鞍点」身份本身未定 ⇒ 一律写「**受约束剖面极大**」。

**① T3 剖面与收敛**：job 1005；日志 gold_finish_20261015/HL1/round4/T3_ptscan_H2O9_relaxed.log sha256 **40ce3be2c6d07120b36d7bf8ce9580aad6becaee16cdf8d1b2c3cb0ab0e60c07**（69007 行）；**20/20 点 Optimization completed + Stationary point found、0 次 Convergence failure**；Normal termination **L69007**（08:00:33）；剖面表原文 **L68362**；输入 gjf sha256 d4fa530ed2d2ab081699592cb031512eef5641ca431ba8b48b7030a5ffe697c3。
逐点（Ha；括号内 = 相对 B（−364.295965289 Ha）的 kcal/mol）：pt1 −364.295965（0.00）→ pt2 −364.295546（+0.26）→ pt3 −364.294643（+0.83）→ pt4 −364.293581（+1.49）→ pt5 −364.292507（+2.17）→ pt6 −364.291487（+2.81）→ pt7 −364.290629（+3.35）→ **pt8 −364.290279（内部极大，+3.5705）** → pt9 −364.290529（+3.41）→ pt10 −364.291230（+2.97）→ **pt11 −364.300604（−2.91，换通道）** → pt12 −364.303393 → pt13 −364.305800 → pt14 −364.307880 → pt15 −364.309680 → pt16 −364.311260 → pt17 −364.312650 → pt18 −364.313890 → pt19 −364.315000 → **pt20 −364.316038391（−12.594）**。
**② pt8 身份 + TS guess**：pt8 = 接触离子对（O1 上三氢：H2 1.076 / H3 0.975 / H4 1.003 = 氢鎓式；O9 上仅 H16 0.976 = 中性肟；R(1,9) = 2.400、R(8,9) = 1.467、R(4,8) = 1.913 已预组织指向 N6）⇒ 属声明步反应物侧，**不是**声明的 O-质子化产物 B。TS-guess：round4/T3_scan_peak_pt8_ts_guess.xyz sha256 **7018f6880a335c7ccd013a47d44fcf8599c3e9f5842bfa872571ae33f9a014ac**。
**③ 竞争 N-质子化通道**：峰后第二次质子转移（H4→N6）落入 N-质子化肟 + 水；该通道极小值 = job 978/995（−364.326887674 Ha，0 虚频），比 B 低 **19.404 kcal/mol**。**剖面远端 pt20（−364.316038391 = B − 12.594）仍高于该极小值 6.81 kcal/mol ⇒ 剖面两端都不是已验证极小值端点；不得写成「剖面到达 N-质子化极小值」或「剖面已到达端点」**。
**④ 沉没口径三值**（分离极限 E(sep) = E(肟，job 1002) + E(H3O+，job 996) = −287.574297051 + −76.6445472086 = **−364.218844260 Ha**）：E(B) − E(sep) = **−48.394 kcal/mol**；E(N-质子化 978) − E(sep) = **−67.798 kcal/mol**；E(ts_0010 伪鞍点 −364.295414931) − E(sep) = **−48.049 kcal/mol**。三值仅作替代口径说明，**不参与也不改变 HL1_E1 = 0.0**。
**⑤ 报告引用**：终版 round4/CALC4_REPORT.md sha256 **875a863698ee24251ff52160fb58acb048d9d47b42ddb267184696f46785b863**；前一版 c25886ba… 作废，本文件与 STATUS 早前引用的 d75e9496… 亦为作废版本 ⇒ 对外一律用终版。
