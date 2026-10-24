# TaskSpec 草案 · N_FORMAMIDE（甲酰胺气相闭式脱水，拟替 NR1）

> **状态：草案（DRAFT），未入库。本文件不含任何 gold 数值、不含任何文献能垒回填。**
> 版本：v3（2026-10-18）｜ 档位：normal（多步机理）
> v3 变更：按协调方实测二面角/虚频份额定死 E2/E3 性质；**统一 H 编号**——spec map **5** = E1 中
> 由 N3 迁到 O2 的 H（E1 之后即 O–H，E3 旋转它、E4 随水带走），spec map **6** = E1 后仍留在 N3 上的
> H（E2 翻转它、E4 迁移它）。全文（含边表、二面角、TS 行）一律用这套 spec map 号。
> 任务书（只读输入）：`gold_compute/queue_20261018/N_FORMAMIDE.txt`
> 替代对象：`NR1`（pinacol 重排，normal）；来源与风险见 `gold_compute/REPLACEMENT_PROPOSAL_20261018.txt`
> 机理背景文献（**仅作假设起点，不作 gold**）：Nguyen et al., *Theoretical Study of Formamide
> Decomposition Pathways*, J. Phys. Chem. A 2011, 115, 841–851, DOI 10.1021/jp109143j；
> 公开资料 SI Table S1/S2（结构与频率）。本地**未取得**该文的已验证笛卡尔坐标，节点身份须按 §5(2) 回核。

---

## 1. 总反应与模型

| 项 | 取值 | 说明 |
|---|---|---|
| 净反应式 | `NC=O >> C#N.O` | NH2CHO → HCN + H2O，闭壳层脱水（**不含**脱 CO / 卡宾通道） |
| 分子式 | CH3NO | 孤立中性分子，全程原子数不变 |
| 原子数 | 6 | 3 重原子 + 3 H |
| 重原子数 | 3（C, N, O） | |
| 电荷 / 重数 | q = 0 / mult = 1 | 闭壳层单重态，全程无离子、无质子酸、无显式水催化剂 |
| 相态 | **气相（gas phase）** | 不加 CPCM/SMD，不加显式辅助水 |
| 方法口径 | B3LYP-D3(BJ)/def2-SVP，ORCA 或 Gaussian 原生 | 沿用项目现行口径；不跨程序混减能量 |
| elements | `["C", "H", "N", "O"]` | 纯第 2 周期 |
| max_heavy_atoms | `3` | |
| single_step | `false` | 多步网络 |
| closed_shell | `true` | |

**单分子体系的直接后果**：全程没有反应物复合物、没有离子对，"本步起点极小值"就是上一节点自身的
极小值；每步能垒 = E(该边 TS) − E(该边起点节点的极小值)，纯电子能，不混 ZPE / 热校正，
不跨步拼接、不用产物侧复合物能量差充当能垒。

---

## 2. 节点表

### 2.1 原子映射约定（与 `bond_changes` 同一套编号）

沿用 `cloudra/benchmark/gen_normal_tasks.py` 的口径：**映射 SMILES 里的 1-based atom-map 编号**即
`bond_changes` 的 `[i, j]` 索引；`[i, j]` 归 `break` 表示该键**键级下降**（含断到 0），归 `form`
表示键级上升（含自 0 新建）。编号不是 SMILES 书写顺序，也不是 0-based。

本部草案固定 6 个原子的映射号（全程不变，每步映射号集合必须相同）：

| map | 原子 | 路径中的角色 |
|---|---|---|
| 1 | 甲酰基 C | 全程不动；最终为 HCN 的 C |
| 2 | O（羰基 → 羟基 → 水的 O） | E1 接受迁移 H；E4 随水离去 |
| 3 | 酰胺 N | 最终为 HCN 的 N |
| 4 | C 上的 H | 全程不动；最终为 HCN 的 H |
| 5 | N 上的第一个 H | **E1 中迁到 O2**，之后作为水的 H 之一 |
| 6 | N 上的第二个 H | **E4 中随水离去**（N3→O2 的 1,3 迁移） |

> 5 与 6 在 R 中是化学等价的（两个 N–H 对称），角色差异**由路径指定**，不是由初始结构区分。
> 入库时必须核对 SI 里"哪个 N–H 先迁移"，若与本文相反，只需交换 5/6 的语义并重排
> 边 E1/E4 的 `[i, j]`，总反应与图拓扑不变。

### 2.2 节点

| 节点 id | 角色 | 映射 SMILES（推导 `bond_changes` 用） | 去映射后规范 SMILES（graph 节点交付） | 身份说明 |
|---|---|---|---|---|
| `N_FORMAMIDE_R` | reactant | `[H:4][C:1](=[O:2])[N:3]([H:5])[H:6]` | `NC=O` | 甲酰胺，平面酰胺构象。**R 必须取"迁移的那个 N–H(map 5) 与 C=O 同侧（syn/O-cis）"的极小值**——它是 E1 的分母。另一侧（O-trans）是不同极小值、能量不同，不能混用 |
| `N_FORMAMIDE_I1` | intermediate 1 | `[H:5][O:2][C:1]([H:4])=[N:3][H:6]` | `N=CO` | 甲酰亚胺酸（formimidic acid, HN=CH–OH）。H5 已由 N3 迁到 O2；重原子骨架 cis（O2–H5 与 C1=N3 同侧）。候选对应论文 **INT-1a**（待 SI 回核） |
| `N_FORMAMIDE_I2` | intermediate 2 | 同 I1（键级不变，纯构象） | `N=CO` | 对应 **INT-1b**：**N–H 绕 C1–N3 翻转**（map 6：dih 180°→0°），O–H 取向不变（map 5 仍 0°） |
| `N_FORMAMIDE_I3` | intermediate 3 | 同 I1（键级不变，纯构象） | `N=CO` | 对应 **INT-1c**：**O–H 绕 C1–O2 翻转**（map 5：dih 0°→180°），N–H 取向不变（map 6 仍 0°）。**E4 的分母**；实测该构象的 map 6（N–H）已朝向 O2，落在 1,3-迁移窗口内 |
| `N_FORMAMIDE_P` | product | `[H:4][C:1]#[N:3].[H:5][O:2][H:6]` | `C#N.O` | HCN + H2O。按交付协议，多分子物种用**一个 dot-joined 节点**（可同时附 HCN···H2O 氢键复合物的极小值证据）。HCN 保留 C–H(map 4)；水的两个 H = map 5 + map 6 |

**关于三个中间体 SMILES 相同**：1a/1b/1c 是同一分子的不同构象/几何异构体，拓扑 SMILES 天然相同。
若评分侧需要区分它们，有两条互不冲突的做法（入库时择一，不要两条同时硬塞）：
(a) 维持相同 SMILES，靠 `id`/`label` 与各自的证据日志（`properties.evidence_log`）区分；
(b) 若 1b/1c 的差异确实是 C=N 的 E/Z，则在映射 SMILES 里用 `/\` 显式写出该双键构型，并验证
RDKit 规范化后仍保留立体标记（unmap 后仍可区分）。**不得**为了"看起来不一样"而虚构键级变化。

---

## 3. 边表

命名沿用现库风格（`<TASK>_E<k>` / `via = <TASK>_TS<k>`）；`step_type` 为 registry `type` 字段的英文文本。

| 边 id | from → to | via | 论文 TS 标签 | step_type（英文，registry `type`） | break | form | weight |
|---|---|---|---|---|---|---|---|
| `N_FORMAMIDE_E1` | R → I1 | `_TS1` | `tsH-1,3` | `1,3-hydrogen shift from the amide nitrogen to the carbonyl oxygen (formamide -> formimidic acid): N-H cleavage, O-H formation, C-N single bond tightening to C=N with reduction of the C=O pi bond` | `[[1,2],[3,5]]` | `[[1,3],[2,5]]` | 1.0 |
| `N_FORMAMIDE_E2` | I1 → I2 | `_TS2` | `tsR-1a1b` | `conformational N-H flip of formimidic acid about the C1-N3 axis (rotamer INT-1a -> INT-1b; the O-H orientation is unchanged); no bond-order change and no C1=N3 E/Z change` | `[]` | `[]` | 0.5 |
| `N_FORMAMIDE_E3` | I2 → I3 | `_TS3` | `tsR-1b1c` | `conformational O-H rotation of formimidic acid about the C1-O2 single bond (rotamer INT-1b -> INT-1c; the N-H orientation is unchanged); no bond-order change and no C1=N3 E/Z change` | `[]` | `[]` | 0.5 |
| `N_FORMAMIDE_E4` | I3 → P | `_TS4` | `INT-1c-tsH2O` | `water elimination from INT-1c: C-O bond cleavage with concerted 1,3-hydrogen shift from the nitrogen to the departing hydroxyl oxygen, C=N tightening to C#N -> HCN + H2O` | `[[1,2],[3,6]]` | `[[1,3],[2,6]]` | 1.0 |

**逐边键变账（供人工核对，键级写成 before→after）**

- E1：C1=O2 2→1（break）；N3–H5 1→0（break）；C1–N3 1→2（form）；O2–H5 0→1（form）。
- E2 / E3：所有成对键级不变 ⇒ `break`/`form` 双空。registry 里这两步**必须**带
  `"conformational": True`，否则生成器的 fail-loud 校验会报"无键级变化且未声明 conformational"。
- E4：C1–O2 1→0（break）；N3–H6 1→0（break）；O2–H6 0→1（form）；C1–N3 2→3（form）。

**E2 / E3 的构象身份（已由 3D 判读确认，取代早期"绕 C–O 旋转 / C=N 几何翻转"的猜测）**

| 节点 | dih(**H6**–N3–C1–O2)（N–H 相对 C–O；H6 = spec map 6） | dih(**H5**–O2–C1–N3)（O–H 相对 C=N；H5 = spec map 5） |
|---|---|---|
| I1（INT-1a） | 180° | 0° |
| I2（INT-1b） | 0° | 0° |
| I3（INT-1c） | 0° | 180° |

> 编号提醒：本表的 H5/H6 是 **spec map 号**（见 §2.1 与节点 SMILES：`[H:5][O:2]...[N:3][H:6]`，
> 即 E1 之后 map 5 在 O2 上、map 6 在 N3 上）。协调方实测 xyz 序为 `1 N / 2 C / 3 O / 4 H(N) /
> 5 H(C) / 6 H(O)`，故 **xyz 序的 H4 ≡ spec map 6**、**xyz 序的 H6 ≡ spec map 5**；引用实测日志时
> 不要直接照抄序号，否则 E2/E3 的二面角归属会整体互换。

- **E2 = N–H 翻转**（绕 C1–N3 轴，180°→0°；动的是 **map 6**；O–H 朝向不变）。
- **E3 = O–H 旋转**（绕 C1–O2 单键，0°→180°；动的是 **map 5**；N–H 朝向不变）。
- 两条边端点处 C1=N3 的双键拓扑与几何均保持不变 ⇒ **不是 C1=N3 的 E/Z 异构化**，边表不得写成"双键几何翻转"。
- 两段虚频位移的重原子份额都 <2%（位移几乎全在 H 上）⇒ 无 π(C=N) 参与，纯构象步；`break`/`form` 双空 + `conformational: True` 成立。
- 因此 E2 与 E3 的 `step_type` **不能互换、也不能合并**：一条动 N–H，另一条动 O–H；两者的构象身份必须分别标注。

**纪律（重要）**

1. 上表 `break`/`form` 是"按映射 SMILES 差分**应当**得到"的预期结果，**不是可手填的自由值**。
   按 `gen_normal_tasks.py` 的纪律，真实入库值由 `_derive_bond_changes(上一步 out, 本步 out)` 自动推导。
   若推导结果与本表不一致，改的是映射 SMILES 或原子编号，**不是**这张表。
2. `weight` 是草案建议值（化学步 1.0、构象步 0.5，理由：构象边 `bond_changes` 双空，匹配代价低，
   不宜与真实成/断键步同权）。**最终权重由出题人/评分口径裁定**，本草案不锁定，也不含任何能垒数值。
3. 每步 `out` 的映射号集合必须与上一步完全相同、形式电荷守恒（本反应全程 0）。
4. 不允许把 E2/E3 两段构象转换合并成"无垒直接相连"，也不允许改写成未经验证的"两步化学步"。

---

## 4. 参考极小值与 TS 清单

### 4.1 需要的极小值（每个都要 Opt+Freq，0 虚频）

| 节点 | 用途（作为哪条边的"本步起点"分母） | 备注 |
|---|---|---|
| R（甲酰胺 syn 构象） | **E1 分母** | 必须是 H5 与 O2 同侧的那个极小值；须报出两平面构象的相对能量以便说明选择 |
| I1（INT-1a） | **E2 分母**，同时是 E1 的终点身份 | E1 的 IRC 下游端点必须回到同一极小值 |
| I2（INT-1b） | **E3 分母** | |
| I3（INT-1c） | **E4 分母** ★ | 全路径最关键：E4 的 TS 只能相对 I3 **自身**极小值，不得用 I1 或 I2 代 |
| P（HCN + H2O） | 不作为任何能垒分母 | 仅记录反应能；可用"分离优化"与"氢键复合物极小值"两种，图节点仍用一个 dot 节点 |

### 4.2 需要的 TS（4 个）

| TS | 对应边 | 性质 | 验收要求 |
|---|---|---|---|
| `N_FORMAMIDE_TS1` | E1 | 1,3-H 迁移，第一个真正改变键级的化学步 | 恰 1 虚频；虚频位移落在 N3–H5 与 O2–H5 上；双向 IRC |
| `N_FORMAMIDE_TS2` | E2 | 真实鞍点，但 `bond_changes` 双空（N–H 翻转，绕 C1–N3） | 恰 1 虚频；位移以 **map 6** 的 H 为主（落在 H6–N3–C1–O2 二面角上），重原子份额 <2%；双向 IRC 连 I1/I2 |
| `N_FORMAMIDE_TS3` | E3 | O–H 旋转，绕 C1–O2 单键；`bond_changes` 双空 | 恰 1 虚频；位移以 **map 5** 的 H 为主（落在 H5–O2–C1–N3 二面角上），重原子份额 <2%；双向 IRC 连 I2/I3 |
| `N_FORMAMIDE_TS4` | E4 | 脱水步，**最可能的决速步（待算，不预设结论）** | 恰 1 虚频；位移同时含 C1–O2 伸长与 N3–H6 拉伸；双向 IRC 连 I3 与 P 侧 |

**分母口径（逐字执行）**：参考极小值 = **该步自身起点的极小值**，纯电子能相减：
`ΔE‡(边 k) = E_elec(TS_k) − E_elec(本步起点极小值)`。不混 ZPE / 热校正 / 自由能，
不跨程序混减，不用"从 R 起算的跨步高度"填作某一步的能垒（NR1 曾出现的口径错误在此显式禁止）。
构象边同样要报能垒（旋转需克服的鞍点），只是不进 `bond_changes`。

- **E4 的 `barrier` 保持空**：已实测排除两类误判——① 一维 O···H 约束扫描的极大点经 Hessian 判为**约束伪极大**（唯一虚频属 H-转子，最低实频为正），且以该帧起 OptTS 会滑回构象鞍点；② 二维约束网格在 C–O × N–H 上，质子转移窗口很窄且窗口内未采到"H 同时桥接 N 与 O"的帧 ⇒ 分步 vs 协同**证据不足，不下结论**。故 E4 边保留、`barrier` 留空，且**不得**把本题写成"四步全部完成"。

### 4.3 实证对齐状态（2026-10-18 05:46 版台账；**只登记状态与日志编号，不含任何能量数值**）

| 边 | 实测结论 | 证据（协调方台账口径；路径以其登记为准） |
|---|---|---|
| E1 | 已定位鞍点，恰 1 虚频；起点 = 甲酰胺 R | `ts_0032`；R 极小值 job 1210 / 1121 |
| E2 | 已定位鞍点，恰 1 虚频；N–H 翻转（map 6），双空成立 | `ts_0033`；I1 极小值 job 1196 |
| E3 | 已定位鞍点，恰 1 虚频；O–H 旋转（map 5），双空成立；interval proof 已指到 INT-1b / INT-1c | `ts_0034`；I2 极小值 job 1187 |
| E4 | **未定位，保持 null**（不填 0、不写成"四步已完成"） | `ts_0035`（未定） |

几何证据：`NR1/geoms/opt/INT1a|INT1b|INT1c.xyz`（xyz 原子序见 §2.1 的编号提醒）。
文档证据：`NR1/REPORT.txt`（62 行，sha256 前缀 `df3f0eec`）、`NR1/BACKFILL_PROPOSAL.md`
（59 行，前缀 `df57c018`）。**能量值一律登记在协调方的 registry/JSON 回填里，本草案按纪律不复制。**

**E4 已排除的路径（避免重复劳动；属"有用的失败记录"，不当结论）**

1. **不是起点构象错**：INT-1c 的 dih(H6–N3–C1–O2)=0°（xyz 序 H4–N1–C2–O3），map 6 的 N–H 已朝向
   O2，落在 1,3-迁移窗口内。
2. **分步假设：证据不足，不下结论**：二维约束网格（`job 1223`，C1–O2 × N3–H6）显示质子转移集中在
   N–H 1.63→1.83 Å 的窄窗口；窗口内未采到"H 同时桥接 N 与 O"的帧，因此不能判为分步，也不能判为
   协同。
3. **一维 O2···H6 约束扫描给的是伪极大**：`job 1212` 在 O···H 1.275 Å 出现极大，但该帧 Hessian
   （`job 1222`）最低实频 85.17 cm⁻¹、唯一虚频 −137.9 cm⁻¹ 属 H 转子 ⇒ 约束伪极大；以该帧起 OptTS
   收敛到 `ts_0034` 同位同模（−508 cm⁻¹ 级 O–H 转子），即滑回 E3 的构象鞍点。
4. **只约束 O2···H6 而放开 C1–O2 时能量立刻回到 INT-1c 附近**（`job 1232` 起点两帧即回到 INT-1c
   附近的能量，无实质垒）⇒ 分子会把 C–O 闭回、H 退回 N；沿该一维方向不可能给出鞍点。
5. 下一步：改用**二维内点**（d(C1–O2) × d(N3–H6) 同时约束到过渡区）做 ts_prepare 初猜；扫描峰只作
   候选/上界，禁作 ΔE‡。

---

## 5. 已知风险与必须核验的点

1. **构象转换 ≠ 化学步。** E2/E3 只能写成 `bond_changes` 双空 + `conformational: True` 的构象边，
   绝不允许捏造"断键/质子转移"；同时也不允许因为"不是化学步"就跳过或删掉这两段——任务书与本
   候选的考点正是"区分成键变化与构象变化"。
2. **中间体身份**：INT-1a/1b/1c 的几何与氢归属已由实测二面角 + 虚频位移份额定死（§3 构象身份表、
   §4.3）：三者都是 HN=CH–OH，差异只在 map 5（O–H）与 map 6（N–H）的取向，C1=N3 全程保持双键。
   **仍缺**的是与论文 SI Table S1/S2 标签的一一对应（须贴二面角依据）；若 SI 的 1a/1b/1c 与本表相反，
   只改 label/节点顺序，不改总反应、不改边表键变。若日后发现某个 INT 实为卡宾/双自由基结构，则该
   节点超出"闭壳层脱水"范围，应报告缺口并停下，不得硬建模、也不得改用脱 CO 通道顶替。
3. **R 构象必须写清。** 甲酰胺有两个平面构象（O-cis/O-trans），能量不同；E1 的分母必须与实际
   迁移侧 N–H 对应。若算的是另一构象，能垒不可比。
4. **找不到鞍点就写缺测。** 若某构象段在本级别退化为近无垒/直接塌陷，记录真实结果并标"能垒缺测"
   （可参照 `normal_registry/yo.py` O3 第 1 步 0.0 的无垒判据写法，但需有自己的证据），
   不以扫描峰、正常退出、工具成功代替鞍点验收；也不为了凑四步而合并或跳过。
5. **不得混入脱 CO（含卡宾）竞争通道**作为本候选的支撑或替代；竞争通道若真的探到，只能作为额外
   边记录，不能改变本条 gold 路径。
6. **产物侧身份**：HCN 与 H2O 在产物侧很容易构成 O–H···N 氢键复合物，IRC 末端会落在复合物而非
   分离渐近线；必须如实报告末端身份，且不得用"复合物 vs 分离物"的能量差充当能垒。
7. **文献数值只作背景**：SI Table 的 ΔE/ΔG 来自不同方法级别（且含热校正），不得填作本项目 gold，
   也不得用来"校准"本级别的数。
8. **单虚线/显式 H 的解析风险**：本反应键变全在 H 上，映射 SMILES 必须显式写 `[H:5]`/`[H:6]`；
   若漏写显式 H，`_derive_bond_changes` 会把 N–H/O–H 变化漏掉，边表会静默变空。入库前用
   `_map_numbers` / `_formal_charge` / `_derive_bond_changes` 三个校验过一遍。

---

## 6. 声明：本草案不含 gold 数值

**本文件不含任何 gold 能垒、不含任何 `barrier_kcal_mol` 数值、不含任何文献数值回填。**
上表 `weight` 只是评分权重建议，不是能量；所有能量列一律留空，等原生日志。

### 正式入库还缺什么（逐项）

> 当前状态：E1–E3 已有实测鞍点（虚频、起点、interval proof 齐）；**E4 未定位**，其
> `barrier_kcal_mol` 保持 null。所有能量值由协调方回填 registry 后重生成 JSON，本文件按纪律不复制。

1. **原生日志**：R / I1 / I2 / I3 / P 五个极小值的 Opt+Freq（ORCA 或 Gaussian 原生），各 0 虚频，
   同程序同方法；纯电子能 Hartree 直接取自日志。
2. **4 个 TS 的原生日志**：`TS1`(tsH-1,3)、`TS2`(tsR-1a1b)、`TS3`(tsR-1b1c)、`TS4`(INT-1c-tsH2O)，
   各恰 1 虚频。
3. **虚频归属**：每个 TS 的虚频位移向量必须落在本步声明成/断键的原子对上（构象边则落在相应二面角），
   附位移分量说明，不能只贴频率数值。
4. **双向 IRC**：四条边各一条短 IRC（不求跑长，但不能用"每向跑了若干点"替代方向判断），
   给出方向区间与两侧末端身份（再到端点做无约束 Opt+Freq，0 虚频闭合）。
5. **端点 Opt+Freq**：IRC 两侧末端重新优化 + 判频，证明它们就是本步起点/终点极小值。
6. **ΔE‡ 计算记录**：逐边 `E(TS) − E(本步起点极小值)`，同一程序同一方法，单位 kcal/mol，
   并说明未混热校正。
7. **SI ↔ 本地节点对应表**：用二面角/键长量（O2–C1–N3–H6、H5–O2–C1=N3 等）把 INT-1a/1b/1c
   与本地 I1/I2/I3 对齐，写清依据；不一致则改节点身份，不改总反应。
8. **生成物**：按 `gen_normal_tasks.py` 结构产出的 `mechanism_graph.json` 与题面 `query`
   （含 "1-based map numbers" 声明、多步网络要求、`bond_changes` 定义、屏障声明条款），
   以及 registry 条目（`mapped_reactants` = R 的映射 SMILES，`system` 里
   `elements/max_heavy_atoms/single_step=false/conditions="gas phase"`）。
9. **替换登记与归档**：NR1 的题源/生成 JSON/回归断言替换记录，旧 NR1 证据归档（不覆盖历史）。

---

## 7. 一条命令级别的自检清单（入库前）

- [ ] `mapped_reactants` 每步映射号集合相同、形式电荷恒为 0；
- [ ] `_unmap_canonical(R) = ["NC=O"]`，`_unmap_canonical(P) = ["C#N", "O"]`；
- [ ] 三个中间体 unmap 后为同一规范 SMILES（`N=CO`）——若为 E/Z 显式写法则确认立体标记保留；
- [ ] `_derive_bond_changes` 对 E1/E4 输出与 §3 表一致，对 E2/E3 输出双空；
- [ ] registry 中 E2/E3 带 `conformational: True`，且 `barrier` 字段为待算空值（不得填 0 收口）；
- [ ] 题面无任何"几步""四步"泄题措辞，也不点名 INT 标签。
