# NI5_E1 · 计划与进展（small_mol as_0093ab74272a41da）

工作根目录：/home/ly/Cloudra-mechanism-agent
本包输出目录：gold_finish_20261015/NI5/（本执行者拥有 rc/ intermediate/ ts/ seeds/ notes/）

## 1 科学模型（按题面 conditions 自判，未改题源）
- 物种：CH2O + CH3NH2 + **1 分子接力水**，共 14 原子，q=0，m=1（闭壳层）。
- 引擎/方法（全阶段统一）：Gaussian 16 `/home/ly/g16/g16`；
  `#p <task> B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=Water)`。
- 条件与模型差异（明示）：题面为水溶液、弱酸性 pH 4–6、钟形速率曲线。本轮模型**未显式加酸催化剂**
  （E1 为胺对中性羰基的 C–N 加成，经典图像中该步本身不依赖酸；酸催化主要作用于脱水步 E3）。
  隐式 CPCM(Water) + 1 个显式接力水仅近似真实介质。**这是近似，不是"溶剂/酸是旁观者"的证明。**

## 2 原子序号口径（工具序号 ↔ 题源 map 号）
自建 RC 坐标顺序（来自共享结构生成器的 3 组分装配体，见 §3）：
| 工具序号 | 元素 | 说明 | 题源 mapped SMILES 号 |
|---|---|---|---|
| 1 | C | 羰基 C | map 1 ([CH2:1]) |
| 2 | O | 羰基 O | map 2 ([O:2]) |
| 3,4 | H | 甲醛 C–H | 未编号（隐式 H） |
| 5 | C | 甲基 C | map 4 ([CH3:4]) |
| 6 | N | 胺 N | map 3 ([N:3]) |
| 7,8,9 | H | 甲基 H | 未编号 |
| 10,11 | H | 胺 N–H | map 5, 6 ([H:5],[H:6]) |
| 12 | O | 水 O | 接力水（题面 schematic 不画） |
| 13,14 | H | 水 H | 同上 |

任务书的 "C1–N6" = 工具序号 1 与 6 = 题源 map 1 与 map 3。反应中心对 = (1,6)。

reaction_mapping 结果（concrete 绑定，reactant=candidate_002.xyz, product=intermediate candidate_000.xyz）：
- mapping_status=unique，binding_status=complete，reactant_identity=match，product_identity=match
- atom_map（product 序 → reactant 1-based 序）= [2,1,6,5,3,4,10,11,7,8,9,12,13,14]
- concrete_watch_pairs = [[1,6]]；formed_bonds=[[1,4]]（图级：C–N）；broken=[]；
  order_changes: C1=O2 键级 2 → 1（π 打开）

## 3 RC 起点几何的 provenance
- 生成工具：`conformer_search`/共享结构生成器（smiles_to_mol, 3 组分 complex 装配；
  smiles=`C=O.CN.O`, charge 0, mult 1）→ 7 个装配候选（assembly.json）。
- 选用 candidate 002（placement 16, rel_energy_kcal=0.9430, min_interfragment_distance=1.7687）。
  原始文件：gold_finish_20261015/NI5/rc/build/assembly/complex_candidate_002.xyz
  sha256=86bb894ce0db87bb315aef92b9b79623d45cb036871661b40082f56b6afbee23
- 该候选的氢键拓扑（internal_coordinates 报告，watch_pairs 复核）：
  r(O2···H13)=1.769 Å（水 O–H 捐给羰基 O）、r(O12···H10)=1.985 Å（胺 N–H10 捐给水 O）、
  r(C1···N6)=3.150 Å（>2.8 Å，无 C–N 成键）、r(O12–O2)=2.737 Å、r(N6–O12)=3.010 Å
  → 六元环接力拓扑 C1=O2···H13–O12···H10–N6···C1（O2–H13–O12–H10–N6 五条边 + C1···N6 闭合）
- **未被选用的对照**：candidate 000/001 是"水只接胺 N、胺 N–H 直接对羰基 O"的开链型
  （O2···H10=1.965 Å、N6···H14=1.827 Å），不满足声明的"水桥接 N–H 与 C=O"六元环拓扑，故弃用。

## 4 加成中间体起点几何的 provenance
- `smiles_to_mol`(smiles=`[O-]C[NH2+]C.O`, generate_3d=true) → 装配候选 000
  gold_finish_20261015/NI5/intermediate/build/assembly/complex_candidate_000.xyz
- internal_coordinates 报告：r(O1–C2)=1.306 Å（C–O 单键，烷氧负离子）、r(C2–N3)=1.459 Å（C–N 已成键）、
  N3 连 C4+H7+H8（铵，4 键）、O1 上无 H、水完整（O12–H13 0.997、O12–H14 0.972），2 个片段。

## 5 作业台账（本包同时只 1 个 QM 作业）
| # | 目的 | 输入 | job_id | 状态 |
|---|---|---|---|---|
| 1 | RC 无约束 Opt+Freq | rc/job01_rc_optfreq/rc_optfreq_m13.gjf | 902 | 已提交（local, async, 12 cpus/13312 MB） |
| 2 | 中间体 无约束 Opt+Freq | intermediate/job02_zwitterion_optfreq/*.gjf | — | 待作业 1 终态后提交 |
| 3 | TS1 全链（ts_prepare） | ts/… | — | 待 RC/中间体核验后 |

## 6 待验证假设
- H1：RC（六元环水接力）在 B3LYP-D3(BJ)/def2SVP+CPCM(Water) 下是无约束极小值（0 虚频）。→ 作业 902
- H2：加成中间体 [O-]CH2–NH2(+)(H)CH3·H2O 是该级别极小值（0 虚频）。→ 作业 2
- H3：C1–N6 加成存在以 C1–N6 为主的唯一虚频鞍点，IRC 双向分别到 RC 与中间体。→ ts_prepare 链

## 7 已知风险
- RC 为氢键/离子型松散络合体，Hessian 软模可能给出微小虚频（软模警告）→ 若出现需按软模流程处理并如实记录。
- 旧 ORCA 路线（91 未收敛、103/106 扫描第一点未收敛+SHARK）已封顶，本轮不重交、不复活其产物；
  本轮为 Gaussian 16 新路线，能量只在本批 Gaussian 日志内相减。
