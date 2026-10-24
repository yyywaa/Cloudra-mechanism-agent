# HI1_E3 道状态（small_mol · 工作目录 gold_finish_20261015/HI1/E3/）

开工 2026-10-15（SGT）。方法一句（本道全部新计算）：Gaussian 16 `/home/ly/g16/g16`，`B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight + SCRF=(CPCM,Solvent=DMSO)`，q0/m1；TS/IRC 只走 ts_prepare/ts_resume（引擎 gaussian）；旧 ORCA 数值只作几何/身份参考，**绝不相减**。

---

## A 只读缺口复核（已完成 2026-10-15）

### A.1 实际执行的命令与结果（真实文件系统，非变更流）

| # | 命令（cwd=/home/ly/Cloudra-mechanism-agent） | 结果 |
|---|---|---|
| 1 | `ls -d gold_compute/remote_backups` | `No such file or directory` → 远端备份目录不在本机 |
| 2 | `find . -maxdepth 4 -type d -name '*remote_backup*'` | 空 |
| 3 | `find . -name 'em1_epF_optfreq*' -o -name '*epF*' -o -name 'I2_start*' -o -name 'i2_min*'` | 只命中 HL1 的 `raw/HL1/job_42/TS669_IRC_epF.*`、`job_46/I3p_P_IRC_epF.*`；**HI1 的 I2 原几何（em1_epF_optfreq.xyz / I2_start.xyz / i2_min_np1）零命中** |
| 4 | `find . -name 'calc-11[4-9].out.log' -o -name 'calc-120.out.log' -o -name 'calc-8[23].out.log' -o -name 'calc-7[12].out.log'` | 空 → **114/115/116/117/118/119/120、82、83、71、72 原生日志均不在本机** |
| 5 | `find . -name '*.out.log' \| wc -l` | 22；全部位于 `research_runs/NU3-open-to-ring-20261015-26734223/...`（calc-18..25、30..32、40..53），与 HI1 无关 |
| 6 | `find . -path ./.venv -prune -o -name 'calc-*.out.log' -print \| grep -v NU3` | 空 → 本工作区**不存在任何** HI1 的 `.cloudra/calc-*.out.log` |
| 7 | `find . -maxdepth 6 -type d -name 'job_8*' -o -name 'job_7*' -o -name 'job_9*' -o -name 'job_1[01]*'` | 只命中 `gold_compute/grant_materials_20261001/raw/HL1/job_9`；无 HI1 job_71/72/82/83/94/100/102 目录 |
| 8 | `ls -R gold_compute/grant_materials_20261001/raw/HI1/` | 只有 `job_51 52 54 58 59 64 65`（ORCA 2026-09-29/10-01 轮），**无 job_27/71/72/82/83/94/100/102/114–120** |
| 9 | `grep -o 'HI1/[a-zA-Z0-9_./]*' gold_compute/grant_materials_20261001/FILE_MANIFEST.json \| sort -u` | manifest（250 项）里 HI1 条目止于 job_51..job_65；无 `HI1_E3`、无 `em1_epF`、无 114–120 |
| 10 | `for f in $(find . -path ./.venv -prune -o -name '*.xyz' -print); do [ "$(sed -n 1p $f)" = 41 ] && echo $f; done` | 535 个 xyz 中，41 原子的**只有** job_51/52/54/58/59/64/65 批次（I1 物种与 C–C 加成 TS） |
| 11 | `find . -name '*.tar.gz' -o -name '*.tgz'` | 空 → 本机无历史 tar 快照可解 |
| 12 | `sha256sum raw/HI1/job_51/rc_clean_np8.xyz raw/HI1/job_52/rc_shared_opt.xyz raw/HI1/job_54/minor_rc_opt.xyz raw/HI1/job_64/ts2_np8.xyz` | 与 PLAN §3 完全一致：5b7b7aa2…、460aa78f…、1bed5958…、26b53f25…（见 §A.2） |

### A.2 可复用几何与不可复核缺口（一行一条）

| 项 | 本地状态 | sha256 / 说明 |
|---|---|---|
| job82 I2 原几何 `em1_epF_optfreq.xyz`（原 sha a618fd1d…8310f） | **本地无原始产物 → 无法复核** | 只在记录中出现；无同名/近名文件 |
| job82/job83/job71/job72 端点日志 | **本地无原始产物 → 无法复核** | 无任何 calc-71/72/82/83 日志 |
| E3 链 114/115/116/117/118/119/120 | **本地无原始产物 → 无法复核** | 无 calc-114..120 日志、无 ts/ts_0001/jobs/declaration_0004 目录 |
| E1 链 94/100/102 | **本地无原始产物 → 无法复核**（且属 E1 道） | 无 calc-94/100/102 日志 |
| 可复用几何（仅 ORCA 起点/身份参考） | 在本地，sha 已核 | `job_51/rc_clean_np8.xyz` 5b7b7aa2df9466c456614c9af3ddfe4e264339fd1b39a2dadd58690fb5f9b594（= HI1_I1 物种，41 原子，旧 E=−938.760019066499 Ha）；`job_52/rc_shared_opt.xyz` 460aa78fde5def3d42741f0c6ad6b6b47ec5c7e29edeeb4ce1bae87931ba5f8d；`job_54/minor_rc_opt.xyz` 1bed5958e8826676044a1b83d256542b5ad93641f02e120d0b7791e1864ebdb8；`job_64/ts2_np8.xyz` 26b53f25a511c050fe71d6fb566fb74b995de9465655f159ec0e90ece3b1031b |
| 结论 | 三处（job51/52/54/64）都不是 HI1_I2；**E3 起点必须在本地自建** | 不得用 RC51/job_51（= I1 物种）充当 I2 |

### A.3 逐条对照验收链（PLAN §4 六项）——历史 candidate_only 缺哪一项

| 验收项 | 历史记录 | 本地可否复核 | 判定 |
|---|---|---|---|
| 1 TS 恰 1 虚频 + 虚频模以声明的成键/断键对为主 | 115：123 modes，唯一负频 mode 6 = −658.38 cm⁻¹，E=−938.731239040799 Eh | 数字仅见记录；**无 115 原生日志/模矢 → 无法复核** | “恰 1 个虚频”= 历史上已满足（仅记录）；“虚频模以 [[2,20],[2,4],[4,21],[4,22]] 为主”= **仅记录不能证明**（从未被展示/复核，且不是当年拒收理由） |
| 2 IRC 双向真实到达 I2 与 P（方向区间证据） | 116：原生正常终止，**两个方向都在迭代 19 达原生上限**未收敛 | 无 IRC 日志/轨迹 → 无法复核 | **缺项**：历史从未形成“哪一区间端点 = I2、哪一区间端点 = P”的映射证明（拒收理由之一）。IRC 未跑满本身不自动否定短区间证明，但该证明当时没做。 |
| 3 两端点 Opt/Freq 零虚频 + 物种/质子/立体（CIP）核验 | 118 侧A 0 负频 E=−938.741308489137 Eh；120 侧B 0 负频 E=−938.761777227422 Eh | 无 117–120 日志 → 零虚频只能“仅记录”；身份/立体无法复核 | “零虚频”= 历史上已满足（仅记录）；**物种/质子归属/立体（CIP）核验 = 缺项**（拒收核心理由：产物立体在 atom 27 改变或未确定） |
| 4 能垒 = 纯电子能差，相对该步自身起点极小值 | 从未给出 E3 能垒；两个端点能量“谁是 I2、谁是 P”未定 | — | **缺项**（旧 16.9 / 19.2 作废，本轮不复用、不回填） |
| 5 原生日志不改写 + 路径 + sha256 + 能量取自原始行 | 记录里有路径与 I2_start 原 sha a618fd1d… | **本地无原始产物 → 无法复核** | 无文件可核；不把记录当证据 |
| 6 写回题源 → 重新生成题面 → 守卫测试 | HI1.json / hi.py 的 E3 barrier 仍为 null | — | 未完成（本轮由包 Coordinator 执行，本道不改题源） |

### A.4 三条历史拒收原因 → 逐条落成“缺什么”

| 拒收原因（HANDOFF §2/§3） | 缺什么（我落成的具体缺口） |
|---|---|
| 产物立体（atom 27）改变或未确定 | 缺“正向 IRC 端点的产物 = 声明的 HI1_P（(S)-aldol + (S)-脯氨酸）”。即：产物侧端点未证明其**新生手性中心（原苯甲醛羰基碳，map 6 = Cc）**的 CIP 与 HI1_P 声明一致，也未证明 proline Cα（map16）仍为 S。 |
| 原子来源 / 连接关系不确定（交换端点归属时反应物有 1–38 近片间接触） | 缺“参与水解的那一分子水 = HI1_E1 生成的水（O4 携带 H21、H22）”。即：I2 里 O4–H21/O4–H22 的原子来源没有与 E1 的产物对上；端点出现 <2.5 Å 的跨片接触 → 分片/连接关系不确定，无法把端点钉到 I2 或 P。 |
| IRC 方向区间没有形成一致证明 | 缺“两个方向各自真实走向声明的 I2 与 P 的方向区间证据”（两条方向都在迭代 19 达原生上限，且没有给出区间终点物种映射）。 |

### A.5 A 段结论（一行）

历史 114–120 链 = candidate_only：只满足“TS 恰 1 个虚频”（仅记录）与“两端零虚频”（仅记录）；**缺第 2 项（IRC 方向区间 → I2/P 映射）、第 3 项（端点物种/质子/立体 CIP 核验）与第 4 项（能垒）**；第 5 项在本地无原始产物因而无法复核；第 6 项未做。所有历史能量与旧值 19.2 / 16.9 一律作废，不作本道证据、不回填。

---

## B 起点重建（HI1_I2）

状态：进行中（见下方“B 段”小节，完成后逐行更新）。

## C 合并水解边 TS 判定

状态：未开始（依赖 B 段 I2 极小值）。

---

## 证据清单

见 `gold_finish_20261015/HI1/E3/evidence/EVIDENCE.md`（原生产物绝对路径 + sha256 + 原始行能量 + 方法一句）。

---

## B 起点重建（HI1_I2）

**B.1 目标物种（题源）**：HI1_I2 = `CC(C[C@H]([O-])c1ccccc1)=[N+]1CCC[C@H]1C(=O)O.O`，41 原子（zwitterion 38 + 显式水 3），q0/m1，CPCM(DMSO)。RDKit CIP 核验（`E3/tools/xyz_identity.py` 同类检查）：I2 中 aldol 碳 = S、脯氨酸 Cα = S，与 HI1_P（(S)-aldol + (S)-脯氨酸，两中心均 S）一致；旧记录里的 `...[C@@H]1...`（C8R）版本得 R-脯氨酸 → 与 10-14 纠正题源不符。

**B.2 与历史起点（job82 / 114–120 链）的显式差异**

| 项 | 历史（job82 chain，记录） | 本轮 E3 道（本地自建） |
|---|---|---|
| 起点几何来源 | 远端 ORCA 6.1.1 几何 `em1_epF_optfreq.xyz`（job82 endpoint，sha a618fd1d…8310f）——**本地不存在** | 本地自建：共享构建器用**纠正后题源的 (S)-脯氨酸中性 I1 络合物 SMILES** 组装 41 原子预复合物 → 几何准备（C–C 成键） → 无约束 Opt+Freq |
| 脯氨酸 Cα | 记录 C8R（R-脯氨酸，0-based 7=Cring） | **(S)-脯氨酸（map16=S）**，与 10-14 纠正题源一致 |
| aldol 碳（原苯甲醛羰基 C） | 记录 C29S | 目标 S，须实测 CIP 核验（不沿用记录） |
| 原子序基准 | ORCA 0-based：0=Ca 1=Cb 3=N 7=Cring 8=Ccooh 9=OdO 10=Oh 23=OhH 24-26=water 27=Od 28=Cc 29-40=苯甲醛 | 构建器/SMILES 顺序，见 B.3 表 |
| 方法/引擎 | ORCA 6.1.1 B3LYP-D3BJ/def2-SVP RIJCOSX def2/J TightSCF CPCM(DMSO) | Gaussian 16 B3LYP/def2SVP + GD3BJ + Int(UltraFine) + SCF=Tight + CPCM(DMSO)；**不与历史 ORCA 数值相减** |
| 历史能量 | −938.740365334360（job82，ORCA）等 | 全部作废、不引用、不回填 |

**B.3 工作原子序号 ↔ 题源 map 号对照表（1-based；本道 I2 结构顺序 = 构建器输入的 SMILES 顺序）**

| 工作序号 | 元素 | map 号 | 角色（E3 相关） |
|---|---|---|---|
| 1 | C | 3 | 丙酮 α-CH2（烯胺端 CH2；E3 中不参与成断键） |
| 2 | C | **2** | 烯胺/亚胺碳；**E3 中被水 O4 进攻 → 成 C2=O4** |
| 3 | C | 1 | CH3 |
| 4 | N | **20** | 脯氨酸 N；**E3 中 C2–N20 断、H21 转移到此** |
| 5, 6, 7 | C | 17, 18, 19 | 吡咯烷 CH2 |
| 8 | C | **16** | 脯氨酸 Cα（立体中心，目标 S） |
| 9 | C | 14 | 羧基 C |
| 10 | O | 13 | 羧基 C=O |
| 11 | O | 15 | 羧基 –OH（24 为其 H） |
| 24 | H | 15 的 H | 羧基 H（几何准备里 H 键给苯甲醛 O） |
| 25 | O | **4** | 显式水 O；**E3 中进攻 C2，最终成为产物酮 O** |
| 26 | H | **21** | 水 H（约定：E3 中转给 N20） |
| 27 | H | **22** | 水 H（约定：E3 中转给 O5） |
| 28 | O | **5** | 醇盐/醛 O；**E3 中被 H22 质子化** |
| 29 | C | **6** | aldol 碳（原苯甲醛羰基 C，立体中心，目标 S；36 为其 H） |
| 30–35 | C | 7–12 | 苯基 C（37–41 为其 H） |

注：水的两个 H（工作 26/27）在 I2 中化学等价；题源 map 21/22 的分工在 E1 之后只是记账约定。E3 声明只要求"一个水 H → N20、另一个水 H → O5"，因此标号可自洽选定（C 段会把这个约定对 TS 判定/质子归属的影响写清）。

**B.4 历史拒收"atom 27"的判定（判断 + 依据 + 不确定性）**

- 事实：原句只有"产物声明立体在 atom 27 改变或未确定"；本地无 `I2_start.xyz`、无 114–120 日志，**无法唯一还原该 pipeline 的原子序**（不可复核项）。
- 依据 1：在本道工作序号下，I2/P 只有两个立体中心——原子 **8**（脯氨酸 Cα，map16）与原子 **29**（aldol 碳，map6）。因此"产物立体"拒收只能指向二者之一。
- 依据 2：HI1_E2 记录中脯氨酸构型从未被质疑（明写 proline C8R 保留、整体一致），而 E3 的两个端点归属都在 aldol/醇盐区域出问题 → 最可能指向 **aldol 碳（map 6）**。
- 依据 3（编号交叉）：E2/HI1 记录用 0-based 27=Od（苯甲醛/醇盐 O）、28=Cc（aldol 碳），并直接用 1-based 标签"C29S"标注 aldol 碳。即"atom 27"在 0-based 读法下字面 = 醇盐 O（我们的原子 28，非立体中心）；在 1-based 读法下字面 = 水的第三个原子（我们的原子 27，亦非立体中心）。两种字面读法都不是立体中心 → 该 pipeline 的编号与 ORCA 模型序号不同（本地无从核对），只能按化学语义判读。
- **本道判定**：该拒收实际要表达的是——(a) 产物端点 aldol 立体中心（**我们的原子 29 / map 6**）的 CIP 未被确定为 S；(b) 醇盐 O（**我们的原子 28 / map 5**）上的质子归属与来源未确定。二者正是 E3 声明里唯一涉及立体的成断键对（[2,4]、[5,22]）所在区域。
- 区分性检验（本轮执行，不依赖历史读法）：两端 Opt+Freq 上同时核验 (i) 原子 29（map6）CIP=S、(ii) 原子 8（map16）CIP=S、(iii) 原子 28（map5）上的 H 归属、(iv) 原子 4（N20）上的 H 归属 —— 覆盖两种读法。

**B.5 重建方法（几何准备，非能垒证据）**

1. 用共享结构构建器组装**中性 HI1_I1 预复合物**（(S)-脯氨酸）：SMILES `C=C(C)N1CCC[C@H]1C(=O)O.O.O=Cc1ccccc1`（41 原子，3 分片：烯胺 + 显式水 + 苯甲醛）。构建器产出 5 个 assembly 候选（`E3/prep/structure_build_I1S/assembly/complex_candidate_000..004.xyz`）；RDKit 逐候选核验：**全部** proline Cα=S、3 分片、苯甲醛 C(=O) 完整。选 `candidate_000`：羧基 OH 以 H···O=C 1.676 Å 氢键指向苯甲醛 O，水以 O···H 1.765 Å 氢键挂羧基 C=O，r(C1···C29)=4.675 Å，∠C2–C1···C29=106.5°（接近 Bürgi–Dunitz 107°）。
2. 题源 I2 的 **zwitterion 直接 3D 构建被构建器拒绝**（frag0 38 原子 MMFF94 迭代 20000 次未收敛 max_gradient 0.037 → 复合物组装 gate 不通过；CREST/nci 同样在构建器层被拒）。这是种子生成的技术障碍，不是化学结论。
3. 几何准备第 1 步（job **910**）：Gaussian `opt=modredundant`，约束 `B 1 29 1.80`，即把 C1(烯胺 CH2,map3)···C29(苯甲醛 C,map6) 从 4.675 Å 收到 1.80 Å，让 C–C 键在 QM 层面成键（该作业只作几何准备，其能量不作任何能垒证据）。输入：`E3/prep/I2_prep_cons180_v2.gjf`。
4. 几何准备第 2 步：对上一步末端几何做**无约束 Opt+Freq**（本道 I2 极小值证据）+ CIP/分片核验。

**B.6 I2 无约束 Opt+Freq 结果**：待 job 910 完成 → 提交 Opt+Freq 后填（0 虚频、身份/分片/CIP）。

**A.6 追加（2026-10-15，第二次真实文件系统核对 + 独立审计交叉）**

| 项 | 事实（本地实测） | 影响 |
|---|---|---|
| job082 目录实体 | `gold_compute/organized_data/hard_20261001/02_calculations/HI1/jobs/job082/` 存在，但只有 `ledger.json`（884 B：ORCA / done / paratera-cpu / 8 cpu / 13000 MB / path `…/minor_spec/em1_endpoints/em1_epF_optfreq.inp`，session as_ce8beb1a7405450f）；`input.inp` 与 `run_directory` 是**悬空软链接**，指向 `remote_backups/paratera_final_20261001_0830/…` —— 该目录本地不存在 | 原几何与日志**不可恢复**；只有作业元数据 |
| job071/job072/job083 | 同上：目录内只有 ledger.json + 悬空软链接 | 同上 |
| 旧 sha 的出现位置 | `a618fd1d…8310f` 只出现在 `organized_data/…/catalog.sqlite3`、`08_integrity/raw_inventory.json|csv` 的**索引行**与 HANDOFF 文本里，**没有任何文件实体** | 索引不能替代原始产物 |
| 通道命名冲突 | job082 的 ledger 路径目录名是 `minor_spec/em1_endpoints`（EM1 = 副面/次通道），而 hard_hi1_2026-10-01.md 把 job82 记为 **E2（major）/ C8R-C29S**（文档自己注明"目录名与工作名不定义声明通道"） | 即使原文件在，也必须先证身份；现在**连"历史 I2 到底是主面 (S)-aldol 还是副面 (R)-aldol"都无法本地复核** → 进一步支持必须自建起点 |

（该核对与包内 explorer 独立审计 `gold_finish_20261015/HI1/audit/DECLARATION_AUDIT.md` 的可得性结论一致：我独立复现"索引行存在、文件实体不存在"。）

---

## C 合并水解边 TS 判定（计划与声明；执行中）

**C.1 题源声明（1-based map 号）**：break `[[2,20],[4,21],[4,22]]`；form `[[2,4],[20,21],[5,22]]`（水 O4 进攻亚胺 C2；断 C2–N20；成 C2=O4；H21→N20；H22→O5）。

**C.2 落到本道工作序号（B.3 表）的 watch pairs**（1-based，I2 顺序）：

| watch pair（工作序号） | 语义 | 声明动作 |
|---|---|---|
| (2, 4) | C2（map2）–N20（map4） | break（双键 → 无） |
| (2, 25) | C2（map2）–O4（map25，水 O） | form（成为产物酮 C=O） |
| (25, 26) | O4–H21（map26） | break |
| (25, 27) | O4–H22（map27） | break |
| (4, 26) | N20–H21 | form（脯氨酸 N–H 再生） |
| (28, 27) | O5（map28，醇盐 O）–H22 | form（醇盐质子化） |

**C.3 执行顺序**：①I2 极小值（job 910 几何准备 → 无约束 Opt+Freq，0 虚频 + CIP/分片核验）→ ②`reaction_mapping`（用 I2 极小值与 P 种子两个**具体结构**取 `atom_map`/`concrete_watch_pairs`，与 C.2 表对照）→ ③TS 初猜：优先 `ts_guess` xtb_path（GFN2/ALPB-DMSO 两端点路径搜索），备选 interpolate（IDPP/linear）→ ④`ts_prepare` 全链（ts_optimization = Gaussian `opt=TS,calcfc`；verification = frequency + irc + 两端 Opt/Freq；同一 `std` 配置）→ ⑤判定：恰 1 虚频且虚频模以 C.2 的成断键对为主 → 双向 IRC 真到 I2 与 P（方向区间）→ 两端 0 虚频且 CIP 核验（原子 8=S、原子 29=S，H 归属在原子 4 与原子 28 上）→ ΔE‡ = E(TS) − E(I2 极小值)，纯电子能，全部 Gaussian 16 同批。

**C.4 事前风险声明（避免事后找理由）**：合并边把"水加成 + 双质子转移 + C–N 断裂"压成一步（C.2 共 3 断 3 成、涉及 6 个原子对），单鞍点可能根本不存在（历史 114 的 −658.38 cm⁻¹ 也只是"1 虚频"这一必要条件）。若 OptTS 失败/滑落到端点，将如实给出：尝试了什么、滑落到哪个物种（原生日志 + 几何 + 身份）、缺什么、以及具体待裁决问题（例如：声明是否必须拆步——水加成得 carbinolamine 中间体再断 C–N；水取向是否决定 H21/H22 归属）。**不擅自拆图、不改题源、不填 0**。

**C.5 质子归属约定（先声明，供裁决参考）**：I2 中两个水 H（工作 26/27）化学等价，题源 map21/22 的分工在 E1 之后再无化学区分，属记账约定。E3 声明只要求"一个水 H → N20、另一个水 H → O5"。因此：TS 的物理要求是两个 H 分别去向 N20 与 O5，标号可按去向自洽指定；若实测 TS 只转移一个质子、或第二个质子去了第三处（例如仍留 O4 / 去羧基），本道按**实测归属**报告并把它列为"缺什么"，不按声明硬套。

---

## D 运行状态与阻塞记录（2026-10-15）

| 时间/事件 | 事实 | 影响/处理 |
|---|---|---|
| job 910 提交（约 16:17 SGT） | 输入 `E3/prep/I2_prep_cons180_v2.gjf`（12c/14000MB，I2 几何准备约束优化） | 提交后一直排队（position 3）；从未启动，本地无 `I2_prep_cons180_v2.log` |
| 主协调吞吐微调（约 16:45） | 建议把"排队中的 12c 作业"改 8c 重投 | **本道无取消入口**（工具面无 cancel；mark_compute_job_failed 不用于排队作业）→ 910 保持原样；已回帖说明（evt_e2b31952fad14582） |
| 主协调撤回该建议（约 17:00） | 不得为改核数而重复提交 | 与我的处理一致 |
| 平台故障告警（约 17:10） | compute.db 写锁：长命进程持锁 → 作业状态写入失败；903/906 卡 running 但实际无进程（泄漏 16 核）；队列 7 个作业全在等 | 主协调要求**暂停新 QM 提交**；本道遵守，此后不提交，直到放行 |
| 本道已完成的 QM 作业 | **0**（无任何 HI1_E3 原生日志；`E3/prep/*.log` 不存在） | HI1_E3 目前**零科学证据**，不是"缺测结论"，是尚未产出 |

后续口径：新提交一律 **8c / ≤10 GB** + 持 `gold_finish_20261015/HI1/qm_slots/slotN`；本道并发 1 RUNNING + 1 QUEUED。执行计划见 `E3/plans/E3_execution_plan.json`（S1 I2 Opt+Freq → S2 ts_guess interpolate → S3 ts_prepare 全链 → S4 验收链/ΔE‡ → S5 失败时 scan 路线 + 证伪记录）。

**B.7 5 个 assembly 候选的逐项实测（非 QM 身份核验；方法：RDKit `rdDetermineBonds.DetermineBonds(charge=0)` + `AssignStereochemistryFrom3D` + `FindPotentialStereo`；脚本 `E3/tools/rank_i1_candidates.py`、`interfrag_contacts.py`）**

| 候选 | 分片 | CIP（立体中心） | r(C1···C29) | ∠C2–C1···C29 | ∠C1–C29–O28 | 羧基 H24 | 水 O25 去向 |
|---|---|---|---|---|---|---|---|
| complex_candidate_000 | 3 | **原子8 = S** | 4.675 Å | 106.5° | 97.2° | O11–H24 0.995 Å，H24···O28 1.676 Å（强 H 键） | O25···H27(O10) 1.765 Å、O10···O25 2.672 Å；H26···C2 2.682 Å |
| complex_candidate_001 | 3 | 原子8 = S | 5.050 Å | 91.5° | 91.6° | 同型（H24 在 O11 上） | 同型 |
| complex_candidate_002 | 3 | 原子8 = S | 5.327 Å | 106.2° | 85.6° | 同型 | 同型 |
| complex_candidate_003 | 3 | 原子8 = S | 6.108 Å | 73.8° | 64.3° | 同型 | 同型 |
| complex_candidate_004 | 3 | 原子8 = S | 5.066 Å | 97.9° | 90.4° | 同型 | 同型 |

结论：**5/5 候选 proline Cα = S**（与纠正后题源一致），全部为 3 分片（烯胺 + 显式水 + 苯甲醛）、苯甲醛 C=O 完整（1.229 Å）；即构建器没有引入 R-脯氨酸。选定 `candidate_000`（Bürgi–Dunitz 型预组织最好：∠C2–C1···C29=106.5° ≈ 107°）。
补充身份核验（SMILES 级，RDKit CIP）：`O=C(O)[C@@H]1CCCN1`（反应物脯氨酸）→ Cα=S；题源 I2 `...[N+]1CCC[C@H]1C(=O)O.O` → aldol C=S、Cα=S；旧记录版 `[C@@H]` → Cα=R（即被 10-14 纠正的写法）；HI1_P `CC(=O)C[C@H](O)c1ccccc1` → aldol C=S。

**C.6 TS 初猜构建方案（平台恢复后立即执行；含几何约束与验收判据）**

前提：I2 极小值里水是"旁观者"（很可能挂在醇盐 O5⁻ 或羧基附近），而 E3 要求 **O4 进攻 C2**、**一个 H→N20**、**另一个 H→O5**。因此初猜必须解决"水的取向与位置"这一预组织问题（这正是历史拒收里"质子归属未定"的物理根源）。

初猜几何目标（本道工作序号，1-based）：
- `r(C2–O4)`（原子 2–25）= 2.9±0.2 Å（进攻前），TS 附近 1.8–2.0 Å；
- `θ(N20–C2···O4)`（原子 4–2–25）≈ 95–110°（O 从 N20 的背面一侧进攻亚胺碳，类似 Bürgi–Dunitz）；
- `r(O4–H26)` ≈ 0.98 Å 且 `r(H26···N20)`（原子 26···4）≈ 1.7–2.0 Å、`θ(O4–H26···N20)` ≥ 150°（H21 走向脯氨酸 N）；
- `r(O4–H27)` ≈ 0.98 Å 且 `r(H27···O5)`（原子 27···28）≈ 1.6–2.0 Å、`θ(O4–H27···O5)` ≥ 150°（H22 走向醇盐 O）；
- `r(C2–N20)` = 1.30 Å（I2 值）→ TS 期望 1.50–1.65 Å；
- 羧基（原子 9/10/11/24）保持完整，**不允许**在初猜里先转移到别处。

构建路线（按优先级；与 `E3/plans/E3_execution_plan.json` 的 S2/S3/S5 对应）：
1. **S2a 自动插值（首选，非 QM）**：`ts_guess(mode='interpolate', interp_method='idpp', reactant_path=I2 极小值 xyz, product_path=P 种子 xyz, atom_map=根据 I2_P_atom_map.json 的 product_atom_map)`。IDPP 会把水 O 拉向 C2、把 H26 拉向 N20、H27 拉向 O5 并同时把 N20 拉向 C2；用返回的 distance_table 选出"四面体化程度最高"的那一帧（判据：r(C2–O4) ∈ [1.8, 2.2]、r(C2–N20) ∈ [1.45, 1.7]、两个 H 各自与供体/受体距离接近 1.2–1.4 Å）作为 S3 的 provided guess。
2. **S2b 手工预组织（插值帧不合格时，非 QM）**：在 I2 极小值上用 `internal_coordinates(mode='transform')` 的 `rotate` 逐步把水整分子与两个 H 摆到上述几何目标：①以两原子定义轴、'atoms'=[25,26,27] 整体旋转水使 O4 落到 C2 的背面进攻位（每步后重测 r(C2–O4)、θ(N20–C2–O4)）；②分别以 O4 与一个远端原子为轴旋转 H26/H27，使其指向 N20/O5；③必要时用一步 `opt=modredundant` 只冻结 `B 2 25 <目标值>` 的短程松弛（QM，恢复后提交）得到干净的前驱几何，**该作业只作几何准备**。
3. **S5 备用（若 S2a/S2b 都做不出合理单鞍点）**：`ts_guess(mode='scan_prepare', engine='gaussian')` 写 1D 或 2D 网格扫描（例如 `r(C2–O4)` 3.0→1.4 Å，`scan_steps` 8–12；或与 `r(C2–N20)` 联动的 2D 网格）→ 提交 → `scan_parse` 取内部峰作为 provided guess；若扫描**无内部峰**或峰对应的是"单质子转移"事件，则把它作为证伪证据之一（并说明单坐标扫描不能单独证明不存在鞍点）。

S3 判定与验收（照 PLAN §4）：
(a) TS 恰 1 虚频，且虚频模以 6 个声明对 `[(2,4),(2,25),(25,26),(25,27),(4,26),(28,27)]` 为主（`log_parser` 的 `imaginary_modes.watch_pair_fraction`）；
(b) 双向 IRC 真实走向 I2 与 P（方向区间证据，不强求跑满原生上限）；
(c) 两端 Opt+Freq = 0 虚频，且实测：原子 8（map16）= S、原子 29（map6）= S、H 在原子 4（N20）与原子 28（O5）上、分片/物种身份正确；
(d) ΔE‡ = E(TS) − E(I2 极小值)（纯电子能、同一批 Gaussian 日志）。
若 (a)–(c) 任一不通过：输出证伪证据（虚频数/模组成、IRC 两侧实际端点物种、滑落到的极小值身份）+ 缺什么 + 待裁决问题（是否必须拆步：水加成得 carbinolamine 再断 C–N；水取向是否决定 H21/H22 归属），**不拆图、不填 0**。

**C.7 参考态与构象注意事项（先声明，避免事后选择参考态）**

1. 本道按 PLAN §4/题面口径：**ΔE‡ = E(TS) − E(HI1_I2 极小值)**（纯电子能，同一批 Gaussian 日志）。这就是交付值。
2. 但 E3 需要水从"旁观取向"翻到"进攻取向"（§C.6），而 I2 极小值未必已是进攻取向的构象。若最终 TS 的**前驱构象**（I2 的另一构象，水预组织好）在能量上高于 I2 极小值，则：
   - 交付值仍是相对 I2 极小值（题面口径），**同时**给出该前驱构象自身极小值的能量与 ΔE‡(前驱) 作为**诊断值**，并显式说明两者差多少（沿用 E2 记录中"own-conformer diagnostic"的做法，不与历史 ORCA 值混减）；
   - 不把"较高构象的相对能量"当作能垒的一部分偷偷加进去，也不反过来挑更低的参考态粉饰结果。
3. 若 TS 只能从"O 进攻 C2 但 H26/H27 取向不同"的构象得到，则必须按 §C.5/§C.6 如实记录**实测的 H 去向**（哪个 H 到了 N20、哪个到了 O5，或都没到），不得按声明硬套。

---

## E 判据↔物种归属表（主协调 2026-10-15 evt_90ab172d726b4373 确认）+ lane2 续跑记录

### E.1 哪条判据适用哪个物种（防止交付时被误读；主协调已确认）

| 判据 | 适用物种 | 值/内容 | 不适用说明 |
|---|---|---|---|
| 0 虚频极小值 | I1 预复合物 / **I2 极小值** / P 端点 | 各物种各自 Opt+Freq 实测 | — |
| **3 分片**（烯胺 + 显式水 + 苯甲醛） | **I1 预复合物**（E1 起点） | 41 原子、3 分片 | **不适用 I2**：I2 中 C1–C29 已成键，化学上应为 **2 分片**（iminium-alkoxide 两性离子 + 显式水） |
| **H 在原子 4(N20) 与原子 28(O5) 上** | **P 端点**（产物 (S)-aldol + (S)-脯氨酸） | 验收第③项 | **不适用 I2**：N20 为 iminium（3 个碳邻居、无 H）、O28 为醇盐（无 H） |
| CIP：原子 8（map16）= S、原子 29（map6）= S | I2 极小值 **与** P 端点（两处都实测） | 身份核验 | — |
| 虚频模以 6 个声明对为主 | **TS** | 验收第①项 | — |
| 双向 IRC 方向区间 → I2 / P | **TS + 两端点** | 验收第②项 | — |

> 来源：转达文本"I2 极小值判据：0 虚频、3 分片、质子归属在 N20/O5 上"经 lane2 复核属**两条串行笔误**；已报主协调（hub 帖 `evt_80e1550783bb43e1`），主协调回复（`evt_90ab172d726b4373`）确认："3 分片属 I1 预复合物、H 归属属 P 端点第③项，不是对 I2 的化学断言；按实测口径执行"。

### E.2 lane2 续跑（2026-10-15 18:20–18:45，非 QM 准备，全部落盘可复核）

| 项 | 结果 | 路径 + sha256 |
|---|---|---|
| 用户待办④ 缺口清单 | 已落成 G1–G6 一行一缺口 + 本轮解决状态（现均"尚未解决"） | `E3/evidence/CANDIDATE_ONLY_GAPS.md` sha256 `b4e61dd5120e4c999aab3276acf820d93bcf5887284b1d1e2212f8d2c737aae8`（附录 A = reaction_mapping 逐字返回，供 issue #179 P6 引用） |
| ts_prepare 声明草稿 + 绑定序换算表 + 验收判据 | 已落成（未执行） | `E3/prep/E3_DECLARATION_DRAFT.md` sha256 `b1bc1bc1922462ca472d1d56fe661188680e4b806e4c92b38f27befccc7e9154` |
| P 种子身份（RDKit 3D） | 41 原子、charge 0、**2 分片**；aldol C(idx5)=S、脯氨酸 Cα(idx28)=S；aldol O–H 在、N–H 在、羧基完整 → 与题源 HI1_P 及 product index_roles 逐原子一致 | `E3/prep/structure_build_P/assembly/complex_candidate_000.xyz` sha256 `06161a1411edf1e1402620ee13ca448c14d2ac167846c10f1e56bf8ec175078a` |
| I2 前体预复合物身份 | 41 原子、3 分片、脯氨酸 Cα(idx8)=S、r(C1···C29)=4.675 Å | `E3/prep/structure_build_I1S/assembly/complex_candidate_000.xyz` sha256 `0d308bd3fdd04afe2c212dee0cc614c9a5697236f50a60e130f494a4299ee9f3` |
| `reaction_mapping` 自动映射缺陷（独立复现） | mapping_status=unique 但化学错（产物酮 O ← 羧基 O、水 O 挂到羧基、含 [12,15] 假键），binding_status=inconclusive、concrete_watch_pairs=[] → E3 不采用 | 见 `CANDIDATE_ONLY_GAPS.md` 附录 A |
| job 925（I2 几何准备） | state=ready（排队中）；输入 `E3/prep/I2_prep_cons180_v3.gjf` sha256 `4f8c4851b8ba74013c1cc162c1158ce7d826ac93a1637fe446ce1bc5b0c292c3`，8c/8192MB | — |

### E.3 槽位与流程（调度政策：手工 priority 0）

- 本道当前 **0 个手工作业在飞**；925 为包 Coordinator 上轮提交。按更严口径：**924 / 925 / 928 全终态后**才提交下一个手工作业（928 = ts_prepare 自动作业，无取消入口）。
- 流程：S1 I2 极小值 Opt+Freq（`E3/runs/I2_optfreq/`，8c/8192MB，priority 0）→ S2 `ts_guess interpolate`（非 QM）→ S3 `ts_prepare` 全链（TS opt + freq + 双向 IRC + 两端 Opt+Freq，8c/10240MB）→ S4 验收链 `log_parser`+`ts_inspect` → S5 失败时证伪记录 + 拆步裁决问题。

### E.4 当前结论状态（严格区分）

- **计算完成：无**（E3 尚无任何本批 Gaussian 原生日志；本道当前零科学证据）。
- **验收通过：无**。
- **HI1_E3 能垒：缺测（缺什么见 G1–G6）**；不填 0、不引用旧值 16.9/19.2。

### E.5 接手须知（2026-10-15 18:5x，主协调广播 evt_3be37ae6d49f4a0d：compute.db 写锁复发 → 只重启 uvicorn，会话可能被中断）

**盘上状态完整、可被继承人接手；本页即交接单。**

- 正在等：**job 925**（E3 I2 几何准备）—— state 最后观测 = **ready（排队）**，输入 `E3/prep/I2_prep_cons180_v3.gjf`（sha256 `4f8c4851b8ba74013c1cc162c1158ce7d826ac93a1637fe446ce1bc5b0c292c3`，8c/8192MB），日志将落在 `E3/prep/I2_prep_cons180_v3.log`。
- 本包其它在飞：924（(S)-I1 基线，E2EM1/runs/I1_optfreq）、928（ts_prepare 自动作业，ts/ts_0004）。**924/925/928 全部终态前，本道不提交任何手工作业**（手工一律 priority 0）。
- 已知数值：**无**（E3 零本批原生日志；本批全部执行 0 个作业）。
- 下一步（按序，全部命令/参数已写在 `E3/prep/E3_DECLARATION_DRAFT.md`）：
  1. `log_parser` 读 925 日志：Normal termination / opt 收敛 / 末端 d(原子1–原子29)≈1.80 Å / route 一致；Error termination 则记原始错误行、不改输入、报包 Coordinator。
  2. `format_converter(log→xyz)` 取 925 末端几何 → `qm_input_writer` 写 `E3/runs/I2_optfreq/I2_optfreq.gjf`（`#p opt freq B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=DMSO)`，q0/m1，8c/8192MB）→ `submit_compute_job(priority=0)`。
  3. I2 极小值核验（0 虚频、分片实测、CIP 原子8/29 = S、质子位置、原始行能量）。
  4. `ts_guess(mode='interpolate')`：reactant = I2 极小值 xyz，product = `E3/prep/structure_build_P/assembly/complex_candidate_000.xyz`，atom_map = `E3/prep/I2_P_atom_map.json` 的 `product_atom_map`。
  5. `ts_prepare`（第一次不带 guess → `ts_inspect` 读绑定序 → `ts_resume` 传 provided guess + reaction_center = §E.1/C.2 的 6 对）。
  6. 验收 ①②③④⑤；失败则出证伪证据 + 缺什么 + 拆步裁决问题（不填 0、不改图、不改 hi.py/HI1.json/hard.md）。
- 唤醒机制：本会话曾设一次性只读轮询 `grep -qE 'Normal termination|Error termination' E3/prep/I2_prep_cons180_v3.log`（120 s 间隔，5400 s 超时）→ **已于 18:5x 触发并发现 job 925 失败（见 §E.6）**。若会话被中断，继承人直接按上面 1–6 续跑即可。
- 关键路径产物 sha256（供接管核对）：CANDIDATE_ONLY_GAPS.md `b4e61dd5120e4c999aab3276acf820d93bcf5887284b1d1e2212f8d2c737aae8`；E3_DECLARATION_DRAFT.md `b1bc1bc1922462ca472d1d56fe661188680e4b806e4c92b38f27befccc7e9154`；complex_candidate_000.xyz(P) `06161a1411edf1e1402620ee13ca448c14d2ac167846c10f1e56bf8ec175078a`；I2_P_atom_map.json `33912bbd415bc424da1f086bc61c696cd6b9eac5f4f2aa7c8b550cd3ce3a980e`。

### E.6 job 925 失败根因更正（2026-10-15 18:35，lane2 实数复核）+ v4 已备好

**事实（原生日志，未改写）**：`E3/prep/I2_prep_cons180_v3.log` sha256 `5045c0e847b03697692ebdc47ebb8569556ef3f9368b3fab480d4a1f6e2442db`（5311 B，mtime 18:35）
- `QPErr --- A syntax error was detected in the input line` → 出错片段 `ight SCRF=(CPCM,Solvent=DMSO) | RERUN of` → `Error termination via Lnk1e in /home/ly/g16/l1.exe at Thu Oct 15 18:35:17 2026`；job 925 状态 = `failed`（18:35:17–18:35:22，`attempt_count=0`）。**不是** l101、**不是**坐标/约束相关。

**根因（逐行核对 v2/v3 输入文件）**：v3 的改动说明写"坐标块与 ModRedundant 卡之间补 1 个空行"，实际文件是：
- v2：line4 = route（109 字符）／**line5 = 空行（route 段终止符）**／line6 = title；
- v3：line4 = route／**line5 = 238 字符的 "` | RERUN of job 910 …`" 说明文字**／line6 = title。
即说明文字被写到**原本终止 route 段的空行位置**；Gaussian 的 route 段一直延伸到第一个空行，于是说明文字被当 route 关键字解析 → l1 语法错误。（v3 对 ModRedundant 的空行修补本身是对的：v3 line49 末坐标、line50 空行、line51 `B 1 29 1.80`。）

**首次失败（job 910 / v2）的工具层根因（本轮实测复现）**：`qm_input_writer` 把 `end_setting`（此处 `B 1 29 1.80`）**直接追加在坐标块最后一行之后，不补 geometry 段终止空行**。用它重新生成 v4 时实际得到：
```
49 [49]: H        2.32119895    -1.16570278     5.28899195
50 [11]: B 1 29 1.80        <-- 无空行分隔（会重演 l101 "Wanted a floating point number"）
```
→ **输入生成层工具缺陷**（几何段尾缺终止空行）；与上一任 lane2 记的"缺空行"同源，只是位置在几何段尾而非 route 段尾。建议并入 issue #177/#179：任何 `qm_input_writer + end_setting` 生成的 .gjf 都少这一行。

**v4（本道新输入；两处空行均已满足，其余逐字不变）**：`E3/prep/I2_prep_cons180_v4.gjf`
- sha256 `60c64bb45ac7aad07f21eeb0d5c5c4238556b6ef96b6b5503d4504e3d1b7486c`（53 行）
- 结构核对：line4 route `#p opt=modredundant B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=DMSO)`／line5 **空行（route 终止）**／line6 title（含 `smiles: C=C(C)N1CCC[C@H]1C(=O)O.O.O=Cc1ccccc1`；provenance 说明留在标题、不进入 route）／line7 空行／line8 `0 1`／line9–49 41 行坐标／line50 **空行**／line51 `B 1 29 1.80`／line52–53 空行。
- 坐标与 `E3/prep/structure_build_I1S/assembly/complex_candidate_000.xyz` 逐原子 **maxdev = 0.0000 Å**（41 原子、元素序一致）。
- 8 cpus / 8192 MB；priority 0；提交时机 = 队列出现空槽（18:5x 快照 running=923/924/927/929，free cpus=0）。

### E.7 第二次几何准备尝试（job 945 失败 → 改用弛豫扫描 v5，2026-10-15 19:0x）

**job 945（v4 输入，单点约束 B 1 29 1.80）实测失败**：state=failed（19:02:33）。原生日志 `E3/prep/I2_prep_cons180_v4.log` sha256 `41c8ca64249a2d5108e634e4f1a683a17face131700f5d3d2c7e1592fe83d3ec`（13960 B）逐字关键行：
```
 Add virtual bond connecting atoms O28        and H24        Dist= 3.17D+00.
 Add virtual bond connecting atoms H27        and O10        Dist= 3.34D+00.
 The following ModRedundant input section has been read:
 B       1      29 1.8000 B
 Iteration  1 RMS(Cart)=  0.03310480 RMS(Int)=  0.34642187
 ... Iteration100 RMS(Cart)=  0.00000126 RMS(Int)=  0.07664682
 New curvilinear step not converged.
 RedCar failed in NewRed.
 Error termination via Lnk1e in /home/ly/g16/l101.exe at Thu Oct 15 19:02:33 2026.
```
- **没有任何 `SCF Done`**：RedCar（冗余内坐标步长构造）在**首个优化步之前**就失败（CPU 5.3 s、共 100 次迭代 RMS(Int) 停在 0.0766），即"从 4.675 Å 一步跳到 1.80 Å"的约束在 3 分片冗余内坐标下数值上不可行。**不是**格式错误、**不是**方法问题。
- 记录：v2（job 910）= 几何段尾缺空行 → l101；v3（job 925）= route 段被说明文字污染 → l1；v4（job 945）= 输入格式正确但**约束步长过大 → RedCar 失败**。三次失败原因互不相同。

**改用 v5：弛豫扫描（relaxed scan）逐步缩短 C1···C29**（标准做法；扫描本身是几何准备，不作能垒证据）
- 生成工具：`ts_guess(mode='scan_prepare', engine='gaussian')` → `E3/prep/I2_prep_scan_v5.gjf`
  - sha256 `afbe9ba904046fabc992df205f51738d4ff1de5724b3973447f34e3190f56b3e`（53 行，含我加的 `%mem=8GB`）
  - route：`# opt=(modredundant,maxstep=10) B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=DMSO)`；扫描卡 `B 1 29 S 8 -0.360000`（4.675 → 1.795 Å，8 点）；输入坐标 = `structure_build_I1S/assembly/complex_candidate_000.xyz`（逐原子 maxdev 0.0000 Å）；空行位置已 awk 核对（line4 route 终止空行、line49 几何段终止空行）。
  - `ts_guess` 生成的扫描输入**自带两处正确空行**（与 `qm_input_writer + end_setting` 不同），故此路径不受 §E.6 工具缺陷影响；但默认不写 `%mem`，我已补 `%mem=8GB`。
- **非 QM 前置检查（internal_coordinates analyze，已执行）**：`E3/prep/precomplex_analyze.zmat`（46 行）+ report：41 原子、3 分片、C8=S；r(C1–C29)=4.675 Å（far）、r(C2–N4)=1.395 Å（单键）、r(O25–H26)=0.974、r(O25–H27)=0.982、r(O28–C29)=1.229 Å（双键，苯甲醛 C=O）；异常项 = O10···H27 1.765 Å 与 H24···O28 1.676 Å（两个 H 键，均为 `forming_candidate` 距离启发式，非化学结论）。→ 注意 **H24（羧基 H）距 O28 仅 1.676 Å**：扫描中若发生 COOH→O28 质子转移，则产物不是声明的两性离子而是"中性 aldol + 羧酸根"，须实测报告（不改图、不填 0）。
- 提交状态：**已提交 = job 951**（2026-10-15 19:1x，8c/8192MB，priority 0，is_async；提交时 free cpus=16）。日志将落在 `E3/prep/I2_prep_scan_v5.log`。
- 下一步：终态后 `ts_guess(mode='scan_parse')` 取扫描剖面/末端几何；末端几何 → `qm_input_writer` 写 `E3/runs/I2_optfreq/I2_optfreq.gjf` → I2 极小值核验 → reaction_mapping 两具体结构对照 → ts_guess interpolate → ts_prepare。**已于 21:46 完成并执行，见 §E.8。**
### E.8 job 951（弛豫扫描 v5）完成 —— 实测结果与新的身份问题（2026-10-15 21:46）

**事实（原生日志）**：`E3/prep/I2_prep_scan_v5.log` sha256 `fdc0412151fd10d2820065910ee07c73de4f1e620f22d349ed375221c02883a2`（10,503,583 B）
- `Normal termination of Gaussian 16 at Thu Oct 15 21:46:12 2026`（log 行 157971）；220 次 `SCF Done`；9 次 `Optimization completed`（帧 0–8）；route 与扫描卡见 §E.7。作业时长约 2.5 h（8c，41 原子，B3LYP/def2SVP+CPCM(DMSO)）→ **资源估算记录：单次约束扫描 8 点 ≈ 2.5 h**。
- `ts_guess(scan_parse)` 结果：`scan_has_internal_peak=true`、`barrier_kcal=null`、`candidate=null`（多峰，未自动选点）：

| frame | 相对能量 (kcal/mol) | d(C1–C29) (Å) | d(C2–N4) (Å) | d(O28–C29) (Å) | O11–H24 (Å) | H24–O28 (Å) |
|---|---|---|---|---|---|---|
| 0 | 0.00 | 4.675 | 1.395 | 1.229 | 0.994 | 1.722 |
| 1 | −0.53 | 4.315 | 1.378 | 1.225 | 1.000 | 1.684 |
| 2 | +0.45 | 3.955 | 1.374 | 1.226 | 0.998 | 1.685 |
| 3 | +2.53 | 3.595 | 1.374 | 1.226 | 0.998 | 1.685 |
| 4 | +4.29 | 3.235 | 1.373 | 1.222 | 0.986 | 1.837 |
| 5 | +3.37 | 2.875 | 1.379 | 1.227 | 0.993 | 1.809 |
| 6 | +8.24 | 2.515 | 1.374 | 1.233 | 0.996 | 1.793 |
| 7 | +7.49 | 2.155 | 1.323 | 1.323 | **1.570** | **1.015** |
| 8 | −2.62 | 1.795 | 1.306 | 1.374 | **1.714** | **0.990** |

（`ts_guess` 的 verdicts：帧 4/6 为内部局部极大候选；帧 7→8 能量跳变 10.11 kcal/mol；帧 6→7 感知连接变化 formed `H24–O28` / broken `O11–H24`；帧 7→8 formed `C1–C29`。**约束扫描相对能量一律不作能垒证据**。）

**扫描终点的真实身份（实测，非推断）**：`format_converter(log→xyz)` 取末帧 → `E3/runs/I2_optfreq/I2_start_v5.xyz` sha256 `5b8f7d6a811ab35911776025ee91d7cf9df09c3fdc60dd38469f03b9ee09dcb5`（41 原子）。
- RDKit 3D：`atoms=41 charge=0 nfrag=2`，SMILES `[H]O[C@]([H])(c1ccccc1)C([H])([H])C(=[N+]1CCC[C@@]1([H])C(=O)[O-])C([H])([H])[H].[H]O[H]`
  → **iminium(C2=N4+) + aldol-OH(O28–H) + 羧酸根(O11⁻) + 旁观水**；r(C1–C29)=1.795、r(C2–N4)=1.306、r(O28–C29)=1.374、O28–H24 = 0.990、O11–H24 = 1.714、水仍在 C2 远处（3.18 Å）。

**新的身份问题（必须报裁决，不擅自处理）**：
- 题源声明的 HI1_I2 = `CC(C[C@H]([O-])c1ccccc1)=[N+]1CCC[C@H]1C(=O)O.O`，即 **alkoxide(O28⁻) + 中性 COOH(H24 在 O11)**。
- 本道实测的同一重原子骨架物种在 C–C 成键后是 **aldol-OH(H24 在 O28) + carboxylate(O11⁻)** —— 两者只差 H24 的位置（同一重原子图、同一总电荷 0，互为质子互变异构体）。
- 机理原因（有据）：本道起点 `candidate_000` 是**羧基 H24 正好氢键指向苯甲醛 O28**（H24···O28 = 1.676 Å）的构象；当 C–C 成键、O28 显现醇盐碱性时，这个预组织的质子即转移到 O28（帧 6→7 实测发生，能量随之下降 10.11 kcal/mol）。这是构象预组织的后果，也是上一轮"原子来源/连接关系不确定"拒收理由的物理根源。
- **下一步（正在做）**：用该终点几何做无约束 Opt+Freq（**job 961**，输入 `E3/runs/I2_optfreq/I2_optfreq.gjf` sha256 `93cbce28547d2d547424f0da79f315d8f274024cb661f8fc8ecda8beae4ddc46`，8c/8192MB，priority 0），实测：0 虚频？分片数？原子 8/29 的 CIP？H24 最终在 O11 还是 O28？

### E.9 job 961（I2 极小值无约束 Opt+Freq）——优化段已收敛，频率段进行中（2026-10-15 22:0x）

**事实（原生日志，正在写）**：`E3/runs/I2_optfreq/I2_optfreq.log`（22:01 时 1.24 MB、19251 行、mtime 持续增长；sha256 待终态后记录）
- `opt freq` 在本平台被 Gaussian 分成**两个内部 job step**：step 1 = opt，`Optimization completed.` + `-- Stationary point found.`（log 17315/17316），四项收敛判据全 YES（Max Force 0.000038 < 0.00045、RMS Force 0.000006 < 0.0003、Max Disp 0.001479 < 0.0018、RMS Disp 0.000243 < 0.0012）；step 1 于 21:59:30 Normal termination（job cpu 1 h 39 min、elapsed 12 min 28 s → **41 原子 opt 段墙钟约 12 分钟**）。随后 step 2 `#P Geom=AllCheck Guess=TCheck SCRF=Check GenChk RB3LYP/def2SVP Freq` 正在跑（22:01 处于 analytic freq 的 CPHF 阶段）。**job 961 状态仍 running，尚未产出频率。**
- **注意（对其它包有用）**：`opt freq` 的日志里会出现一次**中间** `Normal termination`（opt 段结束），若按此行判"作业完成"会过早收尾；必须以作业状态（或第二次 Normal termination / 频率段产物）为准。

**实测能量（原始行）**：
- opt 段最后：`SCF Done:  E(RB3LYP) =  -939.320655479     A.U. after    6 cycles`（log 16950）
- freq 段同几何单点：`SCF Done:  E(RB3LYP) =  -939.320655479     A.U. after    1 cycles`（log 19183）
→ **I2(实测互变体) 纯电子能 = −939.320655479 Eh**（同一批 Gaussian 16；终态后连同频率复核）

**优化后关键内坐标（原始 Optimized Parameters 行；本道工作原子序）**：

| 参数 | 值 (Å) | 含义 |
|---|---|---|
| R(1,29) | **1.5877** | C1–C29 已成键（前体 4.675 → 扫描末 1.795 → 优化后 1.588） |
| R(2,4) | **1.2994** | C2=N4（iminium 双键；前体 1.395） |
| R(28,29) | 1.4031 | C29–O28 单键 |
| R(24,28) | **0.9842** | **H24 已与 O28 成键（aldol O–H）** |
| R(9,10) / R(9,11) | 1.2544 / 1.2501 | 羧基两个 C–O 近等长 → **羧酸根（去质子化）** |
| R(10,27) | 1.7171 | 水 H27 与羧酸根 O10 的氢键 |
| R(25,26) / R(25,27) | 0.9664 / 0.9895 | 水分子 O–H 完整（旁观水，O25 未接近 C2） |

**结论（频率已确认，见下 §E.9 续完）**：本道实测的"I2 极小值"= **iminium(C2=N4⁺) + aldol-OH(O28–H) + 羧酸根 + 旁观水**，即 §E.8 预告的**质子互变体**；题源声明的 `CC(C[C@H]([O-])c1ccccc1)=[N+]1CCC[C@H]1C(=O)O.O`（COOH + alkoxide）在本道构象下**不是驻点**（预组织的 H24 已转移到 O28）。→ 已报主协调（hub 帖 `evt_5ee0cc6d45ca46cb` 的三问 (a)(b)(c)），等频率结果与裁决后决定 E3 起点口径；**不擅自改图、不填 0**。

- **待裁决问题（证据到齐后集中报）**：(a) E3 起点是否采用**实测互变体**（carboxylate + aldol-OH）——它与题源 SMILES 的质子位置不同（ts_prepare 的 identity 检查可能因此判 input_identity_unconfirmed）；(b) 若要保留声明的 COOH+alkoxide，是否允许我另选一个"羧基朝外、不与 O28 氢键"的构象重做几何准备（额外 1–2 个作业）；(c) 是否把该项作为"题源 I2 的质子位置在 QM 下不确定"的证据登记。**本道不擅自改图、不填 0。**

- 工具面记录：`ts_guess scan_prepare` 对 **engine='gaussian' 不接受 `memory_mb`**（第一次调用静默返回空 data，第二次显式报 `Invalid tool arguments`），去掉该字段即成功 → 建议并入 issue #177/#179（参数化消息不透明：ORCA-only 字段在 Gaussian 下未给可诊断错误）。

- 关联更正：上一任 lane2 §B.5 第 3 步写"910 输入 = I2_prep_cons180_v2.gjf"，其失败根因（几何段尾缺空行）本轮由 qm_input_writer 复现确证；§D 表里"缺空行"的表述保留，但**位置需更正为几何段尾**（route 段尾的空行 v2 本来是有的，是 v3 把它占掉了）。
### E.9（续完）job 961 频率段完成：I2 实测极小值成立 —— 0 虚频（2026-10-15 22:05:55）

**原生日志**：`E3/runs/I2_optfreq/I2_optfreq.log` sha256 `63dda25e04529e65920526304fb88755db9393e9c22bd3a6efb76eeee0af0d0e`（1,592,586 B）
- `Normal termination of Gaussian 16 at Thu Oct 15 22:05:55 2026`（log 24001；另一条 18401 = opt 段结束）；`opt freq` 在本平台分两个内部 job step。
- 117 个频率，最低 35.3075 / 46.4262 / 50.3299 cm⁻¹ → **0 虚频**；`Zero-point correction= 0.345935`、`Thermal correction to Gibbs Free Energy= 0.297654`。
- 原始能量行：`SCF Done:  E(RB3LYP) =  -939.320655479     A.U. after    6 cycles`（log 16950）。
- RDKit 3D 实测（`shared/tools/hi1_cip_tools.py` 取最后 Standard orientation）：`natoms=41 frags=2 CIP[8C=S(nb 7C,4N,9C,23H); 29C=S(nb 28O,1C,30C,36H)]` → **原子 8（map16 脯氨酸 Cα）= S、原子 29（map6 aldol C）= S**，与题源 (S)/(S) 一致。
- 末帧 xyz：`E3/runs/I2_optfreq/I2_min_v5.xyz` sha256 `9a6203ff67d9f0d95ad774e78b17bc397b22992f24cbcdf448f8c5558142ef2b`；实测：C1–C29 = 1.588、C2–N4 = 1.299、O28–C29 = 1.403、**O28–H24 = 0.984**、O11–H24 = 1.791、O25–H26 = 0.966、O25–H27 = 0.990、O10–H27 = 1.717、C2–O25 = 3.160。
- 物种（RDKit 图）：iminium + aldol-OH + 羧酸根 + 旁观水（2 分片）；SMILES 见上文 §E.8（`...[N+]1CCC[C@@]1C(=O)[O-]...`）。

**→ 结论（可交付口径）**：本道 **I2 侧参考极小值成立**（0 虚频 + 身份核验通过），但其**质子位置**与题源 SMILES 声明不同（题源 = alkoxide + COOH；实测 = aldol-OH + carboxylate，只差 1 个质子 H24）。E3 能垒的参考态口径待主协调裁决（§E.8 三问）。

### E.10 TS 初猜（非 QM）：IDPP 插值已生成（2026-10-15 22:1x）

- 调用：`ts_guess(mode=interpolate, interp_method=idpp, n_images=20)`；reactant = `E3/runs/I2_optfreq/I2_min_v5.xyz`；product = `E3/prep/structure_build_P/assembly/complex_candidate_000.xyz`；`atom_map` = `E3/prep/I2_P_atom_map.json` 的 `product_atom_map`；watch_pairs = §C.2 的 6 对。
- 产物目录：`E3/runs/interp_v1/`（20 帧 `img_00..19.xyz`）；工具自报 TS 候选帧 = `img_11.xyz`（判据：watched pair C2–N4 跨中点，属启发式）。
- 距离表节选（Å）：帧0 C2–N4=1.299 / C2–O25=3.160 / N4–H26=4.006 / H27–O28=4.256 → 帧10 C2–N4=3.369 / C2–O25=1.868 / N4–H26=2.668 / H27–O28=2.644 → 帧19 C2–N4=5.628 / C2–O25=1.236 / N4–H26=1.026 / H27–O28=0.974。
- **判定：该路径不是干净的协同鞍点路径**（没有任何一帧同时满足 C2–O25 ≈ 1.9–2.0、C2–N4 ≈ 1.6–1.8、两个质子各在 1.2–1.5 Å；C2–N4 在帧 10 已 3.37 Å），故**不作为首选 provided guess**；下一手用 `ts_guess(mode=xtb_path)`（GFN2/ALPB-DMSO，非 QM、不占 QM 槽）做真实路径搜索。
- 记账说明：在实测 I2 极小值下，物理上更直接的质子记账是 **H24 留在 O28、水的一个 H（原子 27）去羧酸根 O11**；题源 map 记账则要求 **H27→O28、H24 回 O11**（多一次质子跳）。两者重原子变化相同（C2–N4 断、C2=O25 成）。**用哪种写入 ts_prepare 声明需主协调裁决**；本道不擅自改图。
### E.11 ⚠ job 962 实测：`B i j value` 形式的 ModRedundant 约束**没有被保持**（2026-10-15 22:29）

**事实（原生日志）**：`E3/runs/preorg_v1/preorg_c2o25_220.log` sha256 `759bce701518a329f5d0d5ce1e2605afb3d1feae28deb095e1c5c983eb85bdc8`（1,979,356 B）
- 输入卡被正确读入：`The following ModRedundant input section has been read:` → `B       2      25 2.2000 B`（log 161–162）。单个 job step（`ModRedundant input section` 只出现 1 次、`Entering Link 1` 只 1 次）。
- 作业 `Optimization completed.` + `-- Stationary point found.`、`Normal termination` 22:29:15、最后 `SCF Done:  E(RB3LYP) =  -939.320655427 A.U.`。
- **但约束没有生效**：首帧几何（log 首个 Standard orientation）r(C2–O25) = **2.248 Å**（RedCar "Initialization pass" 把这对原子挪到了约束值附近），此后单调外移 2.385 → 2.734 → 2.931 → … → 末帧 **3.160 Å**；末帧 `Optimized Parameters` 明写 `R7  R(2,25)  3.1597`。即**优化收敛回未约束的 I2 极小值**（−939.320655427 与 job 961 的 −939.320655479 相差 <1e-6 Ha）。
- 对照：job 945 用同形式卡（`B 1 29 1.8000`）做 4.675→1.80 Å 大位移时，RedCar 在**首个优化步之前**即 `New curvilinear step not converged. / RedCar failed in NewRed.` 失败 —— 该处该卡**确实被当作约束处理**。两个作业行为不一致，机制未明。

**结论/纪律**：**不要依赖裸 `B i j value` 卡保持坐标**，必须核对终态几何里该坐标的实际值；**带 `S n s` 的弛豫扫描是被强制执行的**（job 951：4.675→…→1.795 Å；本道 963 同法）。建议主协调把这条作为工具/平台面教训登记（issue #179 或另开），提醒各包：约束优化做几何准备时必须核验终态坐标值，否则会静默滑回未约束极小值。

### E.12 job 963（进行中）= TS 初猜预组织（弛豫扫描 C2–O25）

- 输入 `E3/runs/preorg_v2/scan_c2o25_316_220.gjf` sha256 `60a25746b3abd96e2af6628a08e126f603f1f526363354a27cb28a49d2602b5e`（ts_guess 生成 + 我补 `%mem=8GB`；route `# opt=(modredundant,maxstep=10) B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=DMSO)`；扫描卡 `B 2 25 S 3 -0.320000` = 3.16→2.84→2.52→2.20 Å；起点 = I2 极小值；8c/8192MB，priority 0）。
- 用途：得到"水已逼近 C2（r(C2–O25) ≈ 2.2 Å）"的**弛豫几何**作为 `ts_prepare` 的 provided guess；扫描本身只作几何准备，不作能垒证据。

---

## F 接续（lane2 第二次接手，2026-10-15 23:1x；本节只追加，旧内容一字不动）

**F.0 接续范围**：把 HI1_E3（= 题源 hi.py I1 steps[2] hydrolysis，合并水解边 HI1_I2 → HI1_P）的 **durable TS 链**跑起来并判定；交付口径 = §C.6/§E.9 六项（1 虚频 + 6 watch pair 模式归属 + 双向 IRC 真到两端 + 两端 0 虚频与身份 + ΔE‡ 同批 Gaussian 纯电子能 + 原生日志 sha256/行号）。
题源声明（照抄，未改字）：reactant `[CH3:1][C:2](=[N+:20]2[CH2:19][CH2:18][CH2:17][C@H:16]2[C:14](=[O:13])[OH:15])[CH2:3][C@H:6]([O-:5])[c:7]1[cH:8][cH:9][cH:10][cH:11][cH:12]1.[O:4]([H:21])([H:22])`；product `[CH3:1][C:2](=[O:4])[CH2:3][C@H:6]([O:5][H:22])[c:7]1[cH:8][cH:9][cH:10][cH:11][cH:12]1.[O:13]=[C:14]([OH:15])[C@@H:16]1[CH2:17][CH2:18][CH2:19][N:20]1([H:21])`；reaction_center = `[[2,4],[2,25],[25,26],[25,27],[4,26],[28,27]]`（break (2,4)/(25,26)/(25,27)；form (2,25)/(4,26)/(28,27)）。

**F.1 只读接手事实（全部由绝对路径复核，未新增任何 QM）**
- I2 侧参考极小值（job 961）：`gold_finish_20261015/HI1/E3/runs/I2_optfreq/I2_optfreq.log` sha256 `63dda25e04529e65920526304fb88755db9393e9c22bd3a6efb76eeee0af0d0e`，117 模 **0 虚频**（最低 35.3075 cm⁻¹），Normal termination 22:05:55，原始行 `E(RB3LYP) = -939.320655479 A.U.`；末帧 `runs/I2_optfreq/I2_min_v5.xyz` sha256 `9a6203ff67d9f0d95ad774e78b17bc397b22992f24cbcdf448f8c5558142ef2b`（41 原子；RDKit 3D CIP：原子 8（map16 Cα）= **S**、原子 29（map6 aldol C）= **S**）。
- ⚠ 该极小值实测物种 = **aldol-OH + carboxylate + 旁观水**，与题源声明的 **alkoxide + COOH** 只差 1 个质子（H24 位置），重原子图/总电荷完全相同（§E.8/§E.9/§E.10；hub 帖 evt_5ee0cc6d45ca46cb / evt_b6a5e54b9197478d）。
- job 963（TS 预组织弛豫扫描，输入 `runs/preorg_v2/scan_c2o25_316_220.gjf` sha256 `60a25746b3abd96e2af6628a08e126f603f1f526363354a27cb28a49d2602b5e`，8c/8192MB、priority 0；route `opt=(modredundant,maxstep=10) B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=DMSO)`，卡 `B 2 25 S 3 -0.320000` = 3.16→2.84→2.52→2.20 Å，起点 = I2 极小值）。
  - 本道 23:17 复核状态：**running**，scan point 4/4、step 20/233（log:39152）。
  - **逐点实测（原生日志行号，约束确实被执行 —— 与 §E.11 裸 `B i j value` 卡静默失效形成对照）**：点1 收敛于 `R7 R(2,25) 3.1596`（log:5149，-DE/DX 0.0）；点2 = **2.8396**（log:13948，-DE/DX 0.0054）；点3 = **2.5196**（log:24932，-DE/DX 0.0112）。
  - 纪律：扫描只作**几何准备**，其能量一律不作能垒证据；其末端（点 4，目标 2.20 Å）几何将作为 `ts_prepare` 的 provided guess。
- 其它已核实输入：product 端点种子 `prep/structure_build_P/assembly/complex_candidate_000.xyz` sha256 `06161a1411edf1e1402620ee13ca448c14d2ac167846c10f1e56bf8ec175078a`（41 原子、2 分片、aldol C=S、Cα=S；同目录有 `complex_candidate_000.mol` 可用于 mol_path）；41 原子 concrete atom map `prep/I2_P_atom_map.json`（字段 product_atom_map，product 坐标序 → reactant 1-based 工作序）。
- heavy_atom_binding（本道工作序，listed in declared SMILES heavy-atom order）= `[3,2,4,7,6,5,8,9,10,11,1,29,28,30,31,32,33,34,35,25]`（SMILES 重原子序 map1,map2,map20,map19,map18,map17,map16,map14,map13,map15,map3,map6,map5,map7..map12,map4）。

**F.2 待办与判定顺序**：①等 963 终态（Normal termination + 点 4 实测 R(2,25)≈2.20）→ 取末帧落盘 guess xyz + provenance（供 evidence_refs）；②`ts_prepare` 一次建 run（reaction 声明见 F.0；calculations g16 profile；conformers.reactant = file I2_min_v5.xyz + heavy_atom_binding；guess = provided；ts_optimization / verification.frequency / verification.irc / 两端 optimization+frequency 全 ref g16；execution 8c/8192MB）；③按主协调 2026-10-15 政策更新（evt_8d124365e7e345cb，经包 Coordinator 转发 evt_ab6959ddca964aa2）：若题源声明的 alkoxide+COOH 建链被 `input_identity_unconfirmed` 判否，**改用实测互变体声明**（reactant `CC(C[C@H](O)c1ccccc1)=[N+]1CCC[C@H]1C(=O)[O-].O`）并在 STATUS 写明「改了什么/依据/与旧图差别/影响哪些边」；不改 registry、不改题源图。

**F.3 状态**：E3 能垒 **仍缺测**（G1–G6 未解决）；本接续段只追加只读复核与计划，尚无新数值结论。
### E.13 机理口径决定（依 BRIEF §9 用户政策更新 2026-10-15 23:1x；lane2 决定 + 包 Coordinator 明确授权）

**政策依据**：主协调广播 `evt_8d124365e7e345cb`（用户原话：标答都没有验证过，所以不具有任何权威性，有更好的机理就选择）→ 题源参考图与既有 gold 值不具权威性；证据支持更好机理时按证据选（可改参考态/质子化位点/拆步合并），要求同批原生日志+sha256+行号、驻点虚频与身份核验、写明改动与影响面；包内可自行决定。**包 Coordinator 已在本包广播 `evt_ab6959ddca964aa2` 中明确授权 lane2**："可以按实测决定 E3 起点参考态（= 实测 I2 侧极小值 aldol-OH + carboxylate + 旁观水，E = -939.320655479 Eh）；若按题源声明的 alkoxide+COOH 建链被 identity 判否，改用实测物种的声明建链并在 STATUS 里写明改了什么/依据/与旧图差别/影响哪些边"。

**本道决定：E3 侧参考态采用实测互变体。**
- 参考态 = job 961 实测极小值 `CC(C[C@H](O)c1ccccc1)=[N+]1CCC[C@H]1C(=O)[O-].O`：`E3/runs/I2_optfreq/I2_min_v5.xyz` sha256 `9a6203ff67d9f0d95ad774e78b17bc397b22992f24cbcdf448f8c5558142ef2b`；日志 `E3/runs/I2_optfreq/I2_optfreq.log` sha256 `63dda25e04529e65920526304fb88755db9393e9c22bd3a6efb76eeee0af0d0e`；**0 虚频**（117 模，最低 35.31 cm⁻¹）、`SCF Done: E(RB3LYP) = -939.320655479 A.U.`（log 16950）、41 原子/charge 0/2 分片、原子 8=S、原子 29=S、C1–C29 1.588、C2–N4 1.299、O28–H24 0.984、羧酸根 C–O 1.2544/1.2501、水完整且 H27 氢键连 O10（1.717 Å）。
- **依据**：(i) 题源声明的 alkoxide+COOH 形式在本道构象（预组织 H24···O28 = 1.676 Å）下**不是驻点**——job 951 弛豫扫描帧 6→7 实测 H24 由 O11 转移到 O28 并伴随 10.11 kcal/mol 能量下降，job 961 无约束 Opt+Freq 收敛到 H24 在 O28 的极小值；(ii) 化学上羧酸（DMSO pKa 约 2–4）远强于 aldol 醇（约 15–17）。
- **改了什么 / 影响面**：TS run 反应声明用互变体口径（reactant SMILES = 上式；product SMILES = 题源 HI1_P 不变；reaction_center = break (2,4)/(25,26)/(25,27)、form (2,25)/(4,26)/(11,27)，替代题源 form (5,22)）；**不改 registry / 题源图**；ΔE‡ 参考态 = 上列实测 I2 极小值；交付需按 BRIEF §9(5) 单列"旧→新"修订（旧：I2 = alkoxide + COOH；新：I2 = aldol-OH + carboxylate；依据同上；影响：E3 的质子记账与参考态）。
### E.14 job 963（弛豫扫描 C2–O25 3.16→2.20 Å）完成：单调上升、无内峰（2026-10-15 23:38:46）

- 日志 `E3/runs/preorg_v2/scan_c2o25_316_220.log` sha256 `e535fb2f1bc5b7259aaed18ba7f391290bfec3e4f07ce39cf146238ed63c27cf`（3,914,230 B）；`Normal termination` 23:38:46；4 点全部 `Optimization completed`；末次 `SCF Done: E(RB3LYP) = -939.307665339 A.U.`。
- **扫描被强制执行**（对照 §E.11 的约束静默失效）：C2–O25 实测 3.160 → 2.840 → 2.520 → 2.200 Å。
- `ts_guess(scan_parse)`：`scan_has_internal_peak=false`、`candidate=null`；约束扫描相对能量（**不作能垒证据**）：帧0 0.000 / 帧1 +0.954 / 帧2 +4.004 / 帧3 **+8.151** kcal/mol → **3.16→2.20 Å 区间单调上升、无内部峰**（障碍若存在必在 2.20 Å 之后）。
- 末帧几何（`E3/runs/preorg_v2/ts_guess_c2o25_220.xyz` sha256 `640405ff9b4f59c234fd966fadd1689c7717feb924fc7b4fd40b18a72e1a2bec`，41 原子）：rdkit `nfrag=2`、物种不变（iminium + aldol-OH + 羧酸根 + 水）；C2–O25 = 2.200、C2–N4 = 1.305（未动）、O28–H24 = 0.988、O10–H27 = 1.675（水 H27 仍氢键连羧酸根）、O25–H26/H27 = 0.968/0.996 → **水被拉到 C2 近旁但质子尚未转移**。

### E.15 已备好：延伸扫描 C2–O25 2.20→1.60 Å（等空槽提交）

- 输入 `E3/runs/preorg_v3/scan_c2o25_220_160.gjf` sha256 `35f151c75fc3f00b4e2a3c2ac0564098084efa4192a932a33b95bac197f76bbc`（ts_guess 生成 + 我补 `%mem=8GB`）；扫描卡 `B 2 25 S 4 -0.150000`（2.20 → 1.60 Å，4 点；细步长以安全穿越成键区）；起点 = 上述 2.20 Å 弛豫几何；8c/8192MB，priority 0。
- 目的：把扫描推过 **C2–O25 成键 + 潜在质子转移** 区，判断是否存在内部峰（若有 → 该点即 TS 候选几何，交 ts_prepare）；若无峰而能量继续上升/体系滑向产物侧 → 作为"无独立鞍点/需拆步"的实证材料。
- **已提交 = job 980**（2026-10-15 23:5x，8c/8192MB，priority 0，state=ready；提交时队列 running=967/968/969/970、queued 9 个，本作业排在第 10 位 → 等待时间取决于全机吞吐）。
### E.16 ts_prepare 声明预演（non-QM，2026-10-15 23:5x）

- `reaction_mapping`（reactant = I2 实测极小值 xyz、product = P 种子）实测：`mapping_status=unique` 但 `binding_status=inconclusive`、`atom_map=[]`、`concrete_watch_pairs=[]`；**reactant_identity=mismatch**，其 diff 诊断逐字为：declared `CC(C[C@H](O)c1ccccc1)=[N+]1CCC[C@H]1C(=O)[O-].O` vs concrete `C/C(C[C@H](O)c1ccccc1)=[N+]1\CCC[C@H]1C(=O)[O-].O` —— **差异只是 C2=N4 双键的 E 立体标记**（不是化学差异）。
- 结论：ts_prepare 的 `reaction.reactant_smiles` 必须写成**带 E 标记**的形式 `C/C(C[C@H](O)c1ccccc1)=[N+]1\CCC[C@H]1C(=O)[O-].O` 才会 identity=match；`atom_map` 用本道手工核对过的互变体口径表（product 序 → reactant 1-based）：`[3,2,25,1,29,28,30,31,32,33,34,35,14,15,16,12,13,36,24,37,38,39,40,41,10,9,11,8,5,6,7,4,27,23,17,18,19,20,21,22,26]`（与题源 map 的差别仅在 product 19 与 33 两个 H 的归属交换）。
- product 侧工具提示"该具体结构有 2 个对称重原子绑定"，故 binding 不可用；本道用显式 atom_map + reaction_center 声明，不依赖自动绑定。
- 声明草案（待 provided guess 就绪后执行）：`reaction` = 上述两条 SMILES + charge 0/mult 1 + atom_map + reaction_center `[[2,4],[25,26],[25,27],[2,25],[4,26],[11,27]]`；`calculations.std` = gaussian/B3LYP/def2SVP/keywords `EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=DMSO)`；`conformers` = reactant `E3/runs/I2_optfreq/I2_min_v5.xyz`、product `E3/prep/structure_build_P/assembly/complex_candidate_000.xyz`；`guess` = 第一次调用不带，随后 `ts_resume` 传 provided guess（2.20 Å 端点几何或延伸扫描所得更靠后的几何）；`verification` = frequency/irc/reactant_endpoint/product_endpoint 全部 ref std；`execution` = 8 cpus / 10240 MB。

---

## G 接续（lane3 第三次接手，2026-10-17 07:xx；只追加）

**G.0 范围**：解开 ts_0011 的 blocked（缺 conformers.reactant.heavy_atom_binding），用 job 980 的 1.8996 Å 帧作 provided guess 起跑 durable TS 链。**本节不含任何 TS/能垒数值（未测到）**。

**G.1 ts_resume 两次（#180 未复现；两次都没有 "TS process belongs to a different project or owner"）**
- ①call_id=`tc_274dc3ad308d4f5a` request_digest `783027706e803bc587946a1c833ddb981e29cd1337dae8f48a59d83b4d41a174`：prev rev 9 → rev 10，input_revision 2 → 3，changes=[conformers.reactant.evidence_refs, conformers.reactant.heavy_atom_binding, execution.memory_mb, guess]，retained=[]/invalidated=[]，status=accepted。**binding 被拒**（逐字）："reactant: Explicit heavy-atom binding does not preserve the declared molecular graph, bonds or stereochemistry."；needs 仍为 conformers.reactant.heavy_atom_binding。
  - 根因（实测）：前人 1-based 表 `[3,2,4,7,6,5,8,9,10,11,1,29,28,30,31,32,33,34,35,25]` 是**题源 map-label 序**排列，其环遍历写成 N4-7-6-5-8，与实测连接 N4-C5-C6-C7-C8 矛盾；也与 ts_inspect.structures.reactant.smiles_heavy_atoms（C,C,C,C,O,c×6,N,C,C,C,C,C,O,O,O）不同序。
- ②call_id=`tc_51a435b4071e4f7c` request_digest `815b9bdab1c7a5bdd5baf4079e3ad49d5469c6d1a241107f0b2db0e1ff1430fe`：prev rev 13 → rev 14（ts_inspect 现读 rev **23**），input_revision 3 → **4**，changes=[conformers.reactant.heavy_atom_binding.indices, conformers.reactant.mol_path]，retained=[]/invalidated=[]，status=accepted → **run 进入 stage=refine, status=waiting**。
- **通过的正确 binding**（声明 SMILES 重原子序，1-based 文件序）= `[3,2,1,29,28,30,31,32,33,34,35,4,5,6,7,8,9,10,11,25]`；RDKit（declared SMILES vs 平台 rev2 生成的 `ts/ts_0011/build/input_0002/reactant/seed.bound.mol` sha256 `c8911a212490c6c594aa3659f13bb44616002b539bcd2b9d4b0590880ff2c670`，含键块 + `M  CHG  2   4   1  11  -1`）useChirality=True 恰 **2 个子结构匹配**，二者只差苯环反向遍历 —— 即平台的 "2 symmetric heavy-atom bindings"。
- source_hashes.reactant = {xyz `9a6203ff67d9f0d95ad774e78b17bc397b22992f24cbcdf448f8c5558142ef2b`, mol `c8911a212490c6c594aa3659f13bb44616002b539bcd2b9d4b0590880ff2c670`}；product 不变（xyz `06161a14…`, mol `2d84490a…`）。

**G.2 job 980（延伸约束扫描）复核：5 点数字成立，1.8996 Å 帧已落盘作 guess**
- 原生日志 `runs/preorg_v3/scan_c2o25_220_160.log` sha256 `436c4cd9225bd29c1ae65086e1394b27b886e4d45206f4efa91133b331030f66`；约束卡 line 158 `B       2      25 S   4 -0.150`；Normal termination line 60977。
- 5 点（SCF Done 行号 / R(2,25) 表行号）：2.1996 −939.307665623 (6225/6593, +8.15) / 2.0496 −939.302902987 (16443/16820, +11.14) / **1.8996 −939.297771992 (25258/25632, +14.36)** / 1.7496 −939.301357590 (53388/53766, +12.11) / 1.5996 −939.309047571 (59324/59692, +7.28 kcal/mol)；基准 = job 961 `runs/I2_optfreq/I2_optfreq.log` sha256 `63dda25e…` line 16950 = −939.320655479 Eh（0 虚频）。**扫描能量一律不作能垒证据。**
- 同表实测：R(2,4) 1.3051→1.4012；R(10,27) 1.6747→1.0048（H27 转到羧酸根 O10）；R(25,26) 0.9675→0.9694（**H26 全程留在水 O 上 → 扫描未覆盖 C2–N4 断裂**）。
- guess：`prep/guess_c2o25_190/ts_guess_c2o25_190.xyz` sha256 `2568ca035c3ee37dc9472cd86bd3a751547ba835f99332cf8ce2ac91177bb186`，取该日志 **Standard orientation 行 25159**；与 `format_converter(log→csv)` 帧 rc=1.89959 逐坐标一致（偏差 0.00e+00）；元素序列与 perceive 连接图在同一 1-based 序号上与 `runs/I2_optfreq/I2_min_v5.xyz` 完全相同 ⇒ 无需重排。抽取脚本 `tools/mk_ts_guess_frame.py` sha256 `246a6da449ea58290693571bcf3e66ab6fba289c91cd5e4c8e915a1c53d33139`；provenance `prep/guess_c2o25_190/PROVENANCE_ts_guess_c2o25_190.md` sha256 `8869c899f0a1db685ccf83cf3bcfbda1f0a42656a9441449885a61fa5d20e45a`。
- ⚠ 该帧内 H27 位于 O25(1.03 Å)/O10(1.50 Å) 之间，而声明 atom_map 要求 H27 终在 **O11**（羧酸根两 O 离域，C–O 1.2655/1.2480）；**声明 map 未改**，由无约束 TS/IRC 决定位点。

**G.3 机制修订（交付单列）**：旧参考态（题源声明）= alkoxide(O28⁻)+中性 COOH(H24 在 O11)；**新参考态（实测，job 961，0 虚频）= aldol-OH(H24 在 O28)+羧酸根+旁观水**，同一重原子图的质子互变异构体。影响：E3 起点口径与 ΔE‡ 基准（E(I2)=−939.320655479 Eh）；I2 作为其它边端点时需同口径。依据见 §E.8/E.9/E.13。

**G.4 当前在飞与下一步**：管线作业 **job 999**（declaration_0004 ts_opt，8c/10240MB，state=ready）输入 `ts/ts_0011/jobs/declaration_0004/ts_opt/refine.gjf`（line 3 `#p opt=(TS,calcfc,noeigen) b3lyp/def2svp empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=dmso)`，0 1）；本道手工在飞 0 个。等终态后逐阶段核验；若 l9999/收敛失败，备选 guess = 同日志 R(2,25)=1.5996 Å 帧。**E3 能垒仍缺测。**

---

## H 观测（lane3，2026-10-17 08:1x）：job 999 从 1.8996 Å 帧起跑后**向外漂移**（只读，未干预）

**事实（原生日志）**：`ts/ts_0011/jobs/declaration_0004/ts_opt/refine.log`（08:09 快照 2,357,767 B；query_compute_job(999)=state **running**, started_at 2026-10-17T06:53:35+08:00）。
- line 1059 `SCF Done:  E(RB3LYP) =  -939.297771991     A.U. after   13 cycles` = 我 guess 帧能量（−939.297771992, job 980 log line 25258）在 1e-9 Eh 内 ⇒ 管线确实用了 provided guess。
- 逐步骤实测（每步最后一个 Standard orientation，列序 R(2,4)/R(2,25)/R(25,26)/R(25,27)/R(4,26)/R(11,27)，Å）：

| 帧 | R(2,4) | R(2,25) | R(25,26) | R(25,27) | R(4,26) | R(11,27) |
|---|---|---|---|---|---|---|
| provided guess (log 25159) | 1.3308 | 1.8996 | 0.9693 | 1.0317 | 3.3761 | 3.3985 |
| step 1 | 1.302 | **2.243** | 0.966 | 0.996 | 3.577 | 3.607 |
| step 3 | 1.312 | 2.639 | 0.968 | 1.019 | 3.869 | 3.723 |
| step 13 | 1.298 | 2.865 | 0.966 | 0.985 | 4.044 | 3.475 |
| step 23 | 1.290 | **3.127** | 0.966 | 0.981 | 4.180 | 3.376 |
| step 38 | 1.298 | 2.930 | 0.967 | 0.987 | 4.001 | 3.468 |

- 收敛表原文行号：35570–35574 (`Maximum Force 0.002766 … NO`, `RMS Force 0.000432 NO`, `Max Disp 0.078182 NO`)、36464–36468 (`Maximum Force 0.001153 NO`, `RMS Force 0.000251 YES`, `Max Disp 0.045960 NO`)；步数上限 232（`Step number  38 out of a maximum of 232`, line 36198）。

**解释（假说，待终态判定；不作为结论）**：约束扫描的 1.9 Å 帧是**约束造出的两性离子**（羧酸根已被水 H27 质子化为 COOH（R(10,27)=1.50）、O25 仍带 H26、C2=N4 仍 1.33 Å）⇒ 电荷分离态；释放约束后优化把水推回 ~2.9–3.1 Å 并把 H27 交还 O25（R(25,27) 0.99）。因此**"约束扫描 2.2→1.6 Å 的内部极大"不是本边协同 TS 的可靠初猜**；扫描能量仍一律不作能垒证据（口径不变）。这也解释了为何 3.16→2.20 Å 段单调而 2.20→1.60 Å 段"看似有峰"。

**备选路线（job 999 终态后择一，均不擅自改图）**：
(i) `ts_resume` 传 provided guess = **R(2,25)=1.5996 Å 帧**（`prep/guess_c2o25_160/ts_guess_c2o25_160.xyz` sha256 `2b569cfe…`；C2-O25=1.600、C2-N4=1.401、H27 在 O10=1.005、COOH 已成）——该帧接近 **hemiaminal + COOH** 中间体，可能给出**后半步（C2–N4 断裂 + H26→N4）**的鞍点；
(ii) 若 (i) 只给出后半步鞍点（虚频仅覆盖 (2,4)/(4,26)），则本边声明的**单步协同**过程应报**拆步**：先"水加成 + H27→羧酸根（hemiaminal 中间体，需 Opt+Freq 0 虚频坐实其为极小值）"，再"hemiaminal 塌缩"；
(iii) 亦可用 `guess.kind=scan` 让管线从 1.5996 Å 帧扫 C2–N4（1.40→2.80）取内峰作 guess（需先确认管线扫描的起点结构是 reactant 还是当前 guess）。

**资源纪律**：job 999 = 8c/10240MB running；全机 4×8c 满载、队列有序号 ⇒ **不新增手工 QM 作业占位**，本道手工在飞 0 个。
- 已**备好但不提交**（受"队列满时暂停新增非手工作业"纪律约束，且与管线即将做的 TS 优化冗余）：`runs/interm_c160/interm_c160_optfreq.gjf` sha256 `7e2bcf93f2a53a73884667dc06823044fb7349300189c3cc179eb3c700b2e72d`（route `#p opt freq B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=DMSO)`，0 1，几何 = R(2,25)=1.5996 Å 帧）——用于**判定 hemiaminal+COOH 候选是否为真正的极小值**（0 虚频 ⇒ 机制为两步：水加成+质子转移 → hemiaminal；hemiaminal 塌缩 → 酮 + 脯氨酸）。若 job 999 终态判定为 off-target/失败，此作业即升级为关键路径证据（届时提交 8c/10240MB、priority 0，手工在飞 1 ≤ 2）。
- 机制条件（模型 vs 现实，供后续判断）：本道模型 = **中性两性离子 + 1 个显式水 + CPCM(DMSO) 隐式溶剂，charge 0/mult 1，无显式碱/酸与反离子**；因此题源单步协同必须靠"水分子的两个 H 分别转移（H27→羧酸根、H26→N4）"来实现电荷中和，这在单一 TS 里是 4 中心耦合过程 —— 与实测"强迫 C2–O25 靠近会造出电荷分离两性离子、释放约束即回流"一致，支持**两步（hemiaminal 中间体）假说**。

**H.1 已提交 1 个手工作业（08:0x 决策，10:0x 复核后执行）**：job **1028**（`runs/interm_c160/interm_c160_optfreq.gjf` sha256 `7e2bcf93f2a53a73884667dc06823044fb7349300189c3cc179eb3c700b2e72d`，`#p opt freq B3LYP/def2SVP …CPCM(DMSO)`，0 1，8c/10240MB，priority 0，state=ready）——判定 hemiaminal+COOH 候选是否为真正极小值；本道手工在飞 1（≤2）。理由：job 999 已跑到 **step 114/232**（log line 106631，10:03）且 `Max Disp 0.181248`（阈值 0.0018，越跑越大，line 106902）⇒ 大概率 l9999；而"单步协同 vs 两步"是本边交付的分叉点，此作业为该分叉的关键证据，不属于"补强性/重复性"手工活。

**H.2 job 1028 用途与落点判据（按写权会话 as_ec848a7673b74e35 要求登记）**
- **用途**：对 job 980 的 **R(C2–O25)=1.600 Å 帧**（= 约束扫描 point 5/5，C2–O25 1.5996 / C2–N4 1.4012 / H27 在 O10 1.0048 / C2=N4 已单键化 / COOH 已成）做**无约束 Opt+Freq**，判定该 "hemiaminal + COOH" 结构是否为**独立晚期极小值**。
- **落点判据（三者必居其一，全部以原生日志 last-frame 内坐标判定）**：
  1. **独立极小值** = `Optimization completed` + 117 模 **0 虚频**，且几何保持"hemiaminal 型"：C2–O25 ≈ 1.4–1.5、C2–N4 ≈ 1.45–1.55（仍成键）、R(10,27) ≈ 0.97–1.00（COOH）、R(24,28) ≈ 0.97（aldol OH 未动）⇒ **机制为两步**（见下"影响面"）。
  2. **坍回 I2 侧** = C2–O25 拉长回 ≈ 2.9–3.2 Å 且 H27 回到 O25（≈0.99），即与 job 961 参考极小值同一盆地（E 应 ≈ −939.32）⇒ 该帧不是极小值，1.600 Å 段只是约束产物。
  3. **滑向产物 P** = C2–N4 ≥ 2.5 Å 且 H26 转到 N4（R(4,26) ≈ 1.0）⇒ 后半步无垒/近无垒，形态上支持"单独合并步不存在"。
- **能量口径（明确排除）**：job 1028 的 SCF 能**不作 ΔE‡、不作任何分母/基准**；E3 的 ΔE‡ 基准仍固定为 job 961 的 **−939.320655479 Eh**（`runs/I2_optfreq/I2_optfreq.log` line 16950，0 虚频）。本作业只提供**驻点身份与几何归属**证据。
- **对连通性/机理解释的影响（条件式）**：若判据 1 成立 ⇒ 本边"声明的单步协同（成 (2,25)、断 (2,4)/(25,26)/(25,27)、成 (4,26)/(11,27)）"**没有合格单鞍点**，需按 BRIEF §9 报**机理修订·拆步**：
  **旧** = I2 → P 一步协同（水加成 + C–N 断裂 + 双质子转移同时发生）；
  **新（提案）** = 步 A：I2 → hemiaminal 中间体（水加成 C2–O25 + H27→羧酸根；C2–N4 保留）；步 B：hemiaminal → P（C2–N4 断裂 + H26→N4 生成酮 + 脯氨酸 NH）。
  **依据** = job 980 约束扫描显示"强迫 C2–O25 靠近会使 H27 转移到羧酸根（R(10,27) 1.675→1.005）且 C2–N4 由 1.305 拉长到 1.401"，加上 job 999 无约束 TS 搜索从 1.9 Å 帧**向外漂移**（R(2,25) 1.90→3.13，氢交还 O25）——即电荷分离的两性离子态不稳定，说明"单步"需要 4 中心耦合、很可能不存在单一鞍点。
  **影响面** = E3 的障碍数（1 个 → 2 个）、E3 的 ΔE‡ 定义（改为步 A 的垒，基准仍 job 961）、以及机图里 I2→P 这一条边需拆为 I2→(新中间体)→P 两条边（**机图改动由主协调/写权会话执行，我不改图**）。
  若判据 2/3 成立 ⇒ 连通性解释不变（E3 仍为单边），我按序改 guess 继续找单鞍点（备选：`guess.kind=scan` 扫耦合坐标 C2–O25 成键 + C2–N4 断裂）。

---

## I §9 拆步文字稿（lane3，2026-10-17 10:1x；按主协调裁定：**只出文字，不提交作业**）

**I.0 裁定背景**：主协调本轮决定不再为 HI1_E1/E2/E3 追加 TS 搜索或换 seed；HI1 按「缺测（保持 null，不填旧 ORCA 值）+ 已证伪 + §9 拆步提案（文字）」交付。**ΔE‡ 分母锁定**：E3 = job 961 **−939.320655479 Eh**。

**I.1 每步 reaction_center（键对 + 方向；1-based 与 0-based 两套）**
工作原子序 = reactant 工作序（= `runs/I2_optfreq/I2_min_v5.xyz` 序；与声明的 reactant_smiles 重原子 binding `[3,2,1,29,28,30,31,32,33,34,35,4,5,6,7,8,9,10,11,25]` 一致）。

*步 A：I2 → hemiaminal（水加成 + 羧酸根质子化；C2–N4 保留）*

| 变化 | 键对 (1-based) | 键对 (0-based) |
|---|---|---|
| 成 C2–O25（水氧加到 iminium 碳） | (2,25) | (1,24) |
| 断 O25–H27 | (25,27) | (24,26) |
| 成 H27–O10（羧酸根 → COOH，实测位点 O10） | (10,27) | (9,26) |
| 保留 | C2–N4、O25–H26 | 同 |

→ 步 A reaction_center：1-based `[[2,25],[25,27],[10,27]]`；0-based `[[1,24],[24,26],[9,26]]`。
（若采用声明 map 的 O11 归属：成键对为 (11,27) / 0-based (10,26)；O10/O11 为离域羧酸根两氧，等价位点。）

*步 B：hemiaminal → P（塌缩；生成酮 + 脯氨酸 N–H）*

| 变化 | 键对 (1-based) | 键对 (0-based) |
|---|---|---|
| 断 C2–N4 | (2,4) | (1,3) |
| 断 O25–H26 | (25,26) | (24,25) |
| 成 H26–N4 | (4,26) | (3,25) |
| 保留 | C2–O25（成为酮 C=O） | 同 |

→ 步 B reaction_center：1-based `[[2,4],[25,26],[4,26]]`；0-based `[[1,3],[24,25],[3,25]]`。

*对照：现声明的单步（= A+B 合并）*：1-based `[[2,4],[25,26],[25,27],[2,25],[4,26],[11,27]]`；0-based `[[1,3],[24,25],[24,26],[1,24],[3,25],[10,26]]`（与 ts_0011 rev 9 的 0-based 存储逐项一致）。

**I.2 每步起止物种 + 同批参考能量（同批 Gaussian 16 B3LYP-D3BJ/def2SVP Int(UltraFine) SCF=Tight CPCM(DMSO) q0/m1）**
- **步 A 起点 = I2 实测极小值**：job 961，`runs/I2_optfreq/I2_optfreq.log` sha256 `63dda25e04529e65920526304fb88755db9393e9c22bd3a6efb76eeee0af0d0e`，line 16950 `SCF Done:  E(RB3LYP) =  -939.320655479     A.U. after    6 cycles`；117 模 **0 虚频**（最低 35.3075 cm⁻¹）；几何 `runs/I2_optfreq/I2_min_v5.xyz` sha256 `9a6203ff…`。**ΔE‡ 分母 = 此值（锁定）**。
- **步 A 终点 / 步 B 起点 = hemiaminal**：**同批目前无 0 虚频 Opt+Freq 证据**。job 1028（`runs/interm_c160/interm_c160_optfreq.gjf` sha256 `7e2bcf93…`）**10:07 仍为 ready（无 log）** ⇒ 登记为「**未取得/待定，不得作为分母**」。其几何取自 job 980 约束扫描 point 5/5（`runs/preorg_v3/scan_c2o25_220_160.log` sha256 `436c4cd9…`，该点 line 59324 `SCF Done:  E(RB3LYP) =  -939.309047571     A.U.`）；**该点能是受约束扫描点能，不得作分母、不得当 ΔE**。
- **步 B 终点 = 产物 P**：几何来源 `prep/structure_build_P/assembly/complex_candidate_000.xyz` sha256 `06161a1411edf1e1402620ee13ca448c14d2ac167846c10f1e56bf8ec175078a`（mol `2d84490ae0f9aed220b715338f845c45fc6f899cc11f47f5f758d2df2db4f034`）；**同批无 Opt+Freq 证据（0 虚频未取得）**。

**I.3 两步 guess 来源与 provenance（均为机器构造：脚本从原生日志抽帧并与 format_converter CSV 逐坐标核对，无手工坐标）**
- 步 A guess：job 980 **Standard orientation line 25159**（point 3/5，R(2,25)=1.8996 Å；该点 line 25258 `SCF Done … -939.297771992`）→ `prep/guess_c2o25_190/ts_guess_c2o25_190.xyz` sha256 `2568ca03…`；provenance `prep/guess_c2o25_190/PROVENANCE_ts_guess_c2o25_190.md` sha256 `8869c899…`。已被 job 999 实用（与 refine.gjf 内坐标逐项相同，Kabsch RMSD 0.00000 Å）。备用：job 963 末端（3.16→2.20 Å 扫描终点）`runs/preorg_v2/ts_guess_c2o25_220.xyz` sha256 `640405ff…`。
- 步 B guess：job 980 **Standard orientation line 60390**（= CSV frame 5/5，R(2,25)=1.59959 Å；该点能 line 59324）→ `prep/guess_c2o25_160/ts_guess_c2o25_160.xyz` sha256 `2b569cfe…`。元素序与工作序 **IDENTICAL**；perceive 连接图不同仅因 **C2–O25 已成键（1.5996 Å）= 化学变化，不是原子序错位**。
- 若后续允许 `guess.kind=scan`：扫耦合坐标 C2–O25（≈2.2→1.45）+ C2–N4（≈1.30→2.60）；Gaussian 用带 S 步长的弛豫扫描卡（`B 2 4 S n s` 形式，本机被强制执行：job 951/963/980；**裸 B i j value 不可靠**：job 962）。

**I.4 已证伪清单（本边，均原生日志）**
1. 声明的 alkoxide+COOH 形式不是驻点（job 961：0 虚频收敛到 aldol-OH + 羧酸根 + 旁观水）。
2. 声明的**单步协同** TS 在"约束扫描峰"seed 下未取得：job 999 从 1.8996 Å 帧**漂离**（R(2,25) 1.90→3.13 Å、H27 交还 O25；§H 行号）——终态登记待其结束。
3. 裸 `B i j value` 约束卡不可靠（job 962，静默滑回 3.160 Å）。
4. IDPP 20 帧插值不是干净协同路径（§E.10：无任何帧同时满足 C2–O25≈1.9–2.0 且 C2–N4≈1.6–1.8）。

**I.5 不填数边界**：E3 的 **ΔE‡ = 缺测**；不得以 job 980/963 扫描能量、也不得以 job 1028 的单点能充当分母或 ΔE（job 1028 结果只用于"驻点身份"）。

---

## J job 999（ts_0011 ts_opt）终态登记（2026-10-17 10:30:06；**收敛到的是 off-target 伪鞍点**）

**原生日志**：`ts/ts_0011/jobs/declaration_0004/ts_opt/refine.log` sha256 `a8f56a49dcec0404da9d23071ad444e6a59641852f2657d2d0903fc3e70b4177`（8,046,622 B, 125,662+ 行）
- 收敛判据（原文，line 124568–124574）：`Maximum Force 0.000083 YES` / `RMS Force 0.000011 YES` / `Maximum Displacement 0.001757 YES` / `RMS Displacement 0.000279 YES` / `Optimization completed.` (124574) / `-- Stationary point found.` (124575)
- 末 SCF（原文）：line 124211 `SCF Done:  E(RB3LYP) =  -939.319094501     A.U. after    6 cycles`（line 123372 同值 −939.319094466）
- 终止：line 125616 `(Enter /home/ly/g16/l9999.exe)`、line 125662 `Normal termination of Gaussian 16 at Sat Oct 17 10:30:06 2026.`（⇒ **不是失败**，是正常收敛）
- 末帧几何（最后一个 Standard orientation 行 125063，1-based 工作序实测）对比 job 961 I2 极小值：R(2,25)=**3.1385** [I2 3.1596]、R(2,4)=1.2990 [1.2994]、R(25,26)=0.9666 [0.9664]、R(25,27)=0.9891 [0.9895]、R(4,26)=3.9822 [4.0064]、R(11,27)=3.6414 [3.6455]、R(10,27)=1.7209 [1.7171]、R(24,28)=0.9844 [0.9842]、R(1,29)=1.5872 [1.5877]、R(9,10)=1.2542、R(9,11)=1.2503、R(28,29)=1.4041。
- `Optimized Parameters` 同表原文行号：124585 R(1,29)=1.5872、124587 R(2,4)=1.2990、124604 R(9,10)=1.2542、124605 R(9,11)=1.2503、124606 R(10,27)=1.7209、124607 R(24,28)=0.9844、124608 R(25,26)=0.9666、124609 R(25,27)=0.9891。

**判读（事实 + 推论分开）**
- 事实：该驻点的**几何 = I2 极小值本身**（所有列出的内坐标与 job 961 相比 ≤0.021 Å，6 个 watch pair 全部回到 I2 值），但能量 **−939.319094501 Eh 比 I2 极小值高 0.0015610 Eh = +0.98 kcal/mol**。
- 推论（待 job 1029 频率判定）：这是**水分子平移/摆动坐标上的极浅驻点**，不是本边声明的 6 对协同水解 TS。若 job 1029 给出 1 个很小的虚频且模以水的整体平移为主 ⇒ **off-target 伪鞍点**按判据诚实登记；若 0 虚频 ⇒ 该点为"近极小值的浅极小"，同结论（未取得协同 TS）。
- **不作能垒**：−939.319094501 与 I2 基准之差 0.98 kcal/mol **不是** E3 的 ΔE‡（它对应的是水在预反应复合物里的浅位点，不含化学键变化）。

**管线状态（ts_inspect 实读，revision=27）**：status="waiting", stage="refine", waiting_for=[**job 1029** purpose="frequency" state="ready" 8c/10240MB input `ts/ts_0011/jobs/declaration_0004/frequency/frequency.gjf`], **result=null**。按主协调裁定，我不为 HI1 追加 TS 搜索/换 seed；管线自动推进的频率段我按门禁核验（1 虚频？模归属？）。

---

## K 索引序对照表（lane3，2026-10-17 10:4x；按主协调「跨道双写」纪律，纯文字）

**K.1 六对涉及的原子：工作序 ↔ 原始序 ↔ 化学标签**

| 工作序 1-based | 0-based | 原始序（题源 hi.py map 标签） | 化学标签（job 961 实测） |
|---|---|---|---|
| 2 | 1 | [C:2] | iminium 碳 C2（C2=N4 1.2994；连 CH3 / CH2R / N4） |
| 4 | 3 | [N+:20] | 吡咯烷 N（iminium N） |
| 10 | 9 | [O:13] | 羧酸根 O（C–O 1.2544）；本构象中与水 H27 氢键 R(10,27)=1.717 |
| 11 | 10 | [OH:15] | 羧酸根 O（C–O 1.2501）；本构象中与 aldol H24 氢键 R(11,24)=1.791 |
| 25 | 24 | [O:4] | **水氧**（O25–H26 0.9664 / O25–H27 0.9895） |
| 26 | 25 | [H:21]（链：declare atom_map product41→working26；题源 product [N:20]1([H:21])） | 水 H → 产物脯氨酸 N–H |
| 27 | 26 | 题源**无独立标签**（题源 COOH 氢是 [OH:15] 隐式 H；身份由 declare atom_map product33→working27 给出） | 水 H → 产物羧酸根 O–H |
| （24） | （23） | [H:22]（declare atom_map product19→working24） | aldol O28–H 的氢（R(24,28)=0.9842） |

- O10/O11：**化学上等价**（同一离域羧酸根，C–O 1.2544/1.2501，Δ=0.004 Å），但**本构象氢键对象不同**（H27↔O10、H24↔O11）⇒ 引用时**不可互换**；step A 质子化位点实测为 O10（声明为 O11），见 §I.1。
- **水氧恒为工作序 25**：E3 全部作业（961/963/980/999/1028）共用同一工作序（`I2_min_v5.xyz` 与 job 961 日志元素序列逐位相同，`ts_freq_projection.py` 输出 "IDENTICAL"）。
- 六对两套索引：C2–N4 (2,4)/(1,3)；C2–O25 (2,25)/(1,24)；O25–H26 (25,26)/(24,25)；O25–H27 (25,27)/(24,26)；N4–H26 (4,26)/(3,25)；O11–H27 (11,27)/(10,26)（实测位点 O10–H27 = (10,27)/(9,26)）。

**K.2 「原始序」的定义**：= **题源 hi.py atom-map 标签序**（20 个重原子标签 1–20 + 水两个显式 H 标签 21/22；其余 19 个 H 为题源 SMILES 隐式、**无原始编号**）⇒ 它不是 41 原子序列。**工作序** = `runs/I2_optfreq/I2_min_v5.xyz` sha256 `9a6203ff67d9f0d95ad774e78b17bc397b22992f24cbcdf448f8c5558142ef2b`（= ts_0011 绑定 reactant seed 同 sha256，= job 961 日志原子序）。产物侧序 = `prep/structure_build_P/assembly/complex_candidate_000.xyz` sha256 `06161a14…`（= 题源 product SMILES 出现序，符号序列已核）。

**K.3 declare.json**（`ts/ts_0011/declare.json` sha256 `b5b883bd09fb0b173fc4d561a5218d3920f6aa04c966e37f0eb7b0eeac8b23ef`）：`atom_map` 41 项、值域 0..40 ⇒ **0-based**，方向 = **product 坐标序 → reactant（工作序）索引**；`reaction_center` 同为 0-based `[[1,3],[1,24],[24,25],[24,26],[3,25],[10,26]]` = 1-based `[[2,4],[2,25],[25,26],[25,27],[4,26],[11,27]]`。

---

## L 终稿口径锁定（写权会话 as_ec848a7673b74e35 已采纳我方证据，2026-10-17 10:3x–10:5x）

- 写权会话已把 §K 三条结论原样写进 `HI1/STATUS.md` §R8.33：①「原始序」= 题源 atom-map 标签序（非 41 原子序列）；②工作序 = `I2_min_v5.xyz`（sha `9a6203ff…`）= job 961 日志原子序；③declare.json `atom_map` 0-based、方向 product→reactant 工作序。
- **E3 终稿措辞（硬约束，我方照办）**：job 999 = "ts_opt 收敛到 I2 盆地几何的**浅驻点**（−939.319094501，L124211；`Stationary point found` L124575；`Normal termination` L125662；末 Step **134**/232，L124298），相对 job 961 高 **+0.98 kcal/mol**；**非声明单步 TS、不回填、outcome=null**"；+0.98 **只作该浅驻点与 job 961 的能量差**，**不得写成 ΔE‡/能垒、不得写"能垒趋近 0"**；虚频判定写"**未取得**（1029 state=ready）"。
- **纪律**：**不再提交任何作业、不 ts_resume、不改图**（E1/E2/E3 三条均不补作业）。我方手工在飞仅 job 1028；job 1029 为管线作业。
- 状态快照（10:36:35）：**job 1028** running，仍在 opt 段（无 `Optimization completed`/无频率表；末两条 SCF：line 3399 `-939.311647746`、line 4337 `-939.304869050`）；**job 1029** 仍无 log（`.../declaration_0004/frequency/` 只有 `frequency.gjf` 2329 B + `optimized.xyz` 2106 B）。两者终态后我只回"termination 行号 + 末 SCF 行号 + 是否 0 虚频（及模是否落在 (2,25)/(2,4)）"，其值**永不进 ΔE‡/分母**。
- **E3 的 ΔE‡ = 缺测（保持 null / 不回填）**；L2 身份缺口由写权会话在终稿显式声明。

**L.1 追加快照（10:39:21，均为非终态）**
- **job 1029（ts_0011 frequency）已起跑并进入频率阶段**：`ts/ts_0011/jobs/declaration_0004/frequency/frequency.log`（50,827 B，10:39），line 818 `SCF Done:  E(RB3LYP) =  -939.319094501     A.U. after   13 cycles` —— 与 job 999 末次 SCF（line 124211，−939.319094501）**在 1e-9 Eh 内一致 ⇒ 频率段确实作用在 job 999 的收敛几何上**（几何传递无误）；日志内尚无 `Frequencies --`/`Harmonic frequencies` ⇒ 虚频数仍为**未取得**。
- **job 1028** 仍在 opt 段：末尾 SCF line 5267 `-939.311623227`、line 6124 `-939.312285001`；无 `Optimization completed`、无频率表。
- 写权会话已把终稿措辞改为"虚频判定未取得（1029 已于 10:37 起跑，截稿时日志内尚无频率表）"（其 §R8.40），并按约定此后不再互发确认性消息；E3 的 ΔE‡ 仍缺测。

---

## M job 1029（ts_0011 frequency）终态：1 虚频 = 甲基摆动 ⇒ off-target 伪鞍点（2026-10-17 10:55:08）

**原生日志**：`ts/ts_0011/jobs/declaration_0004/frequency/frequency.log` sha256 `8366cbc6ec3d40d66bfb001cee746ac39f9fdc86896098d088e82e4d3cc133af`（374,858 B）
- 原文行：L1500 `Low frequencies --- -128.0475  -10.7450   -5.6627   -0.0008   -0.0005    0.0005`；L1501 `Low frequencies ---    5.0615   37.3761   47.4672`；**L1502 `******    1 imaginary frequencies (negative Signs) ******`**；L1505 `Harmonic frequencies (cm**-1), IR intensities (KM/Mole), Raman scattering`；L1511 `Frequencies --   -128.0397                37.1550                47.4266`；L5302 `Normal termination of Gaussian 16 at Sat Oct 17 10:55:08 2026.`
- 脚本实测（`tools/ts_freq_projection.py`）：`modes parsed = 117 ; imaginary = 1`；`element sequence vs I2_min_v5.xyz : IDENTICAL`；频率段首个 SCF L818 `-939.319094501` 与 job 999 末 SCF（L124211）1e-9 内一致 ⇒ 几何传递无误。
- **虚频模逐原子位移（normal-mode 块，log 单位）**：**15(H)=0.640、14(H)=0.592、16(H)=0.478**；其余全部 ≤0.037（3(C)=0.032、26(H)=0.024、13(H)=0.024、2(C)=0.022、17(H)=0.022、1(C)=0.017、4(N)=0.014、6(C)=0.014）。原子 14/15/16 = 连在 C3 上的**甲基三个 H** ⇒ **虚频模 = CH₃ 摆动/转动**。
- **6 个 watch pair 承载的均方位移份额 = 0.3%**；逐对 |d_i−d_j|：R(2,4)=0.0100、R(25,26)=0.0300、R(25,27)=0.0000、R(2,25)=0.0245、R(4,26)=0.0374、R(11,27)=0.0100。最大位移原子对全在甲基内部：14-15:0.986、15-16:0.983、14-16:0.976。
- **判定**：job 999 的驻点是 **off-target 伪鞍点**（负曲率来自 CH₃ 扭转，不是声明的 6 对键变化）；能量 −939.319094501 Eh 与 job 961 之差 **+0.98 kcal/mol 不作 ΔE‡、不作能垒**。
- **管线状态（ts_inspect revision=31）**：status="waiting", stage="refine", **result=null**, waiting_for=[**job 1033** purpose="irc" state="ready", input `ts/ts_0011/jobs/declaration_0004/irc/irc.gjf`]。按裁定**不提交新作业、不 ts_resume**；该结构的 IRC 只作记录，不改变本结论。
- **E3 的 ΔE‡ 仍为缺测**（无合格鞍点；分母锁 job 961 −939.320655479 Eh）。





## N. 2026-10-17 10:58 — job 1028 落地判读（H.2 第 1 路：genuine intermediate）+ 回信/发帖登记

- 写权会话（as_ec848a7673b74e35）复核并采纳 1029 判读，E3 终稿改判为 pseudo-saddle；我回信确认口径差异（我 0.3% 为六对逐对投影之和；其 0.15% 为六 watch atom 集合平方位移占比），无分歧，接受其终稿写法。消息事件：evt_c711f43739a74d5e（call 写权会话）；topic 帖：evt_56d629efaa154af3（notified as_a341823c436e47ed, evt_01045a7c81e04ae3）。
- **job 1028 落地 = H.2 第 1 路（genuine intermediate，不是滑回 I2 盆地、不是滑向 P）**。
  log 绝对路径：`/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/runs/interm_c160/interm_c160_optfreq.log`
  快照 sha256 `92f0617fec4ccaed31d3e1ba950faf670d4da4e287a3673734955474b76f47cf`（19,155 行 / 1,241,836 B / mtime 2026-10-17 10:56:18；freq 链路 10:56:07 起，尚未出 Frequencies 块，最终 sha 待终止后补登）。
  原始行：L16838 ` SCF Done:  E(RB3LYP) =  -939.312626605     A.U. after    6 cycles`；L17229 ` Optimization completed.`；L17230 `    -- Stationary point found.`；L18325 ` Normal termination of Gaussian 16 at Sat Oct 17 10:56:06 2026.`（该 Normal termination 为 opt 任务收尾，非整份 log 收尾）。
  末帧几何（L18955 Standard orientation 起 41 原子；元素序列与 runs/I2_optfreq/I2_min_v5.xyz 逐位相同；1.25×共价半径邻接普查）：C2–O25 = 1.4728 Å（I2 中 3.1596，新成 C–O 键）；C2–N4 = 1.4248 Å（保留，I2 中 1.2990）；O10–H27 = 0.9949 Å 且 O25···H27 = 1.6342 Å（H27 由水氧转到羧基氧）；羧基变 COOH：C9–O10 1.330 Å / C9–O11 1.214 Å；O25–H26 = 0.9693 Å；N4 三配位（4–5 1.473 / 4–8 1.455 / 4–2 1.425），无 4–26 键（d(4,26)=3.1829 Å）；体系仍为 41 原子、电荷 0、单重态。
  物种判读：C2 同时连 N4 与 O25 + 已质子化 COOH ⇒ 半缩胺（carbinolamine）型加合物，正对应 §I split 提案的 step A 产物（成 C2–O25 / H27→O10 / 保留 C2–N4）。
  能量差（仅身份证据）：−939.312626605 − (−939.320655479, job 961) = +0.008028874 Eh = +5.04 kcal/mol（627.5095 kcal/mol/Eh）。**明确：此数不是 dE、不是 ΔE‡、不进入任何分母，也不是能垒。**
  频率判定：**missing measurement**（截至 10:58 尚无 Frequencies 块；0 虚频 / 虚频位置未测）。若出 0 虚频 ⇒ step A 产物为 verified 局部极小；若有虚频 ⇒ 报数值与位移是否落在 watch 对上，按同口径降级为 saddle（未验证为极小）；两路都不改 outcome=null。
- job 1033（irc, ready，管线自动推进登记）：不停不杀、不作连通性证据；我不做任何动作。
- 本段之后我仍不提交作业、不 ts_resume、不改图、不回填（写权会话 as_ec848a7673b74e35 独占回填）。

### N.1 2026-10-17 11:10 — job 1028 终局：0 虚频 ⇒ verified 局部极小（§H.2 第 1 路；写权会话已独立复核采纳）

- 整份 log 最终 sha256 `1ec7e4c6388415d0859939238f4f96ec7739c0bbf1f985a28f4dd3c23b7dcec1`（23,954 行 / 1,593,380 B）；job 1028 state=done（我的手工作业，非管线）。
- 原始行：L16838 ` SCF Done:  E(RB3LYP) =  -939.312626605     A.U. after    6 cycles`（opt 收敛能量）；L17229 ` Optimization completed.`；L17230 `    -- Stationary point found.`；L18325 ` Normal termination of Gaussian 16 at Sat Oct 17 10:56:06 2026.`（opt 段收尾）；L18327 ` Link1:  Proceeding to internal job step number  2.`（第二步 route `#P Geom=AllCheck Guess=TCheck SCRF=Check GenChk RB3LYP/def2SVP Freq`）；L19117 ` SCF Done:  E(RB3LYP) =  -939.312626605     A.U. after    1 cycles`（freq 段起点重算，与 opt 收敛值同）；L19814 ` Frequencies --     19.8439                32.4876                53.5548`（首个频段）；L19804 ` Low frequencies ---  -11.3266   -0.0004    0.0007    0.0009    4.6430    5.5200`（首行负值为平动/转动伪迹，不计模数）；L21772 ` Zero-point correction=                           0.347492 (Hartree/Particle)`；L22248 ` Optimization completed.` / L22249 `    -- Stationary point found.`（freq 段自身的一步几何校验，` Predicted change in Energy=-3.414142D-09`）；L23954 ` Normal termination of Gaussian 16 at Sat Oct 17 11:10:09 2026.`
- 频率判定：全 log 中 `imaginary frequencies` 出现 **0** 次；39 组 `Frequencies --` = **117 模 = 3N−6（41 原子）**；最低实模 19.8439 cm⁻¹（软但为正）。工具复核 `python3 gold_finish_20261015/HI1/E3/tools/ts_freq_projection.py <log> runs/I2_optfreq/I2_min_v5.xyz` → `modes parsed = 117 ; imaginary = 0`；`lowest bands: 19.8439, 32.4876, 53.5548, 78.9135, 98.4614, 113.6134`；元素序列与 I2_min_v5.xyz **IDENTICAL**。
- 终局判读：§H.2 **第 1 路 = genuine intermediate**——末帧 C2–O25 = 1.4728 Å（成键）、C2–N4 = 1.4248 Å（保留）、O10–H27 = 0.9949 Å 且 O25···H27 = 1.6342 Å、C9–O10 = 1.330 / C9–O11 = 1.214 Å（COOH）、O25–H26 = 0.9693 Å、N4 三配位且无 4–26 键——**且 0 虚频 ⇒ verified 局部极小**；既非 I2 盆地（R(2,25) 3.1596），也非产物（C2–N4 未断）。
- 能量口径不变：−939.312626605 − (−939.320655479, job 961 L16950) = +0.008028874 Eh = +5.04 kcal/mol，**仅作落地物种/中间体身份证据，不是 dE、不是 ΔE‡、不进任何分母**；E3 的 dE 仍为 missing measurement、outcome 仍 null。
- 通报：写权会话 as_ec848a7673b74e35 已独立复核并采纳（其 STATUS §R8.46 + 终稿 §三 E3 段：步 A 产物升为 verified 局部极小，同时明确「步 A 的鞍点本身仍未取得；步 B 两端仍无 Opt+Freq」）。我方通报：topic 帖 `evt_a3a034d4273f49ef`（通知主协调 `evt_c1c04ee8682644d3`）+ 给写权会话的一行判读（11:11）。
- 本作业到此封闭；我不再提交作业、不 ts_resume、不改图、不回填、1033 不管。

### O. 2026-10-17 13:35 — 管线端点闭环：product/reactant 两端都回到 I2 物种（候选 TS 未连通到 P）；IRC 1033 仅各 1 点

管线在我交付后继续自动推进（我未提交、未 ts_resume、未改图、未 kill），结果是对 E3「无合格 TS / 连通性未证」的**追加证伪**，不是新结论。记录如下（原始 log 未改动）：

- **job 1043 product_frequency（管线）**：`ts/ts_0011/jobs/declaration_0004/product_frequency/product_frequency.log` sha256 `b5f62db2d4f2630b7c51cec44f01bb5e21b41ac74f2ccf45574199266f5f046f`（5,301 行）。
  L819 ` SCF Done:  E(RB3LYP) =  -939.320655496     A.U. after   13 cycles`；117 模、**0 虚频**（全 log 无 imaginary frequencies 表头；`tools/ts_freq_projection.py` → `imaginary = 0`，最低 35.3112/46.4293/50.2885）；L3473 ` Zero-point correction=                           0.345935 (Hartree/Particle)`；L5301 ` Normal termination of Gaussian 16 at Sat Oct 17 13:33:07 2026.`
- **job 1041 product_opt（管线）**：`product_opt/product_opt.log` sha256 `b91175b78786e00d30a7c6ce309ce3908b64be99fa8d51d07f152556e8f25b7e`；L34156 ` SCF Done:  E(RB3LYP) =  -939.320655496     A.U. after    6 cycles`；L34529 ` Optimization completed.` / L34530 `    -- Stationary point found.`；L35617 ` Normal termination … 13:25:36`。起点即 IRC 外层帧：`product_frequency/endpoint_source.json` 记 `{"kind":"irc_outer_frame","label":"A",…"irc_job_id":1033,"irc_log_sha256":"17da5ef2…"}`。
- **reactant 槽**：`reactant_opt/reactant_opt.log` sha256 `5c64c8b8…` L21448 `SCF Done: -939.320655386`（L21812/21813 收敛，L22902 终止 12:16:41）；`reactant_frequency/reactant_frequency.log` sha256 `139a17b917f196387276142a4c3ae5a88b9cc0433eff114373914509b798ad0d` L817 同能量、0 虚频、最低 35.3946/46.4741/50.3614、L5297 终止 12:37:51。
- **两个槽是同一物种、且都是 I2**：product 槽 −939.320655496 vs reactant 槽 −939.320655386（Δ = −1.10×10⁻⁷ Eh ≈ −0.00007 kcal/mol），二者 vs job 961 的 I2 极小 −939.320655479（`runs/I2_optfreq/I2_optfreq.log` L16950）分别差 −1.7×10⁻⁸ / +9.3×10⁻⁸ Eh；0 虚频且最低三个实模（35.31/46.43/50.29 与 35.39/46.47/50.36）与 I2 极小（35.3075/46.4262/50.3299）在数值噪声内一致。系统给出的几何感知 SMILES 两槽相同且等于 reactant。⇒ **产物 P 在本管线里从未被到达；E3 的「产物端 0 虚频 + 身份核验」是 identity-falsified，不是 verified product。**
- **job 1033 IRC（对 pseudo-saddle，管线）**：`irc/irc.log` sha256 `17da5ef2a63e7af2a4a1e232ef06d9b8ceb3e488504e0f9bad569a87dc071edb`（3,672 行）。11:29:38 起（`Start new reaction path calculation`，step 0.1000 bohr），只有 `Point Number  1 in FORWARD path direction.`（L1489）与 `Point Number  1 in REVERSE path direction.`（L2170）两个外点，能量 L1957 −939.319097479 / L2639 −939.319097211，随即 L3672 `Normal termination … 11:32:37`。⇒ **无终点区间证明**；且两个外点松弛后都回到 I2（上一条）⇒ 该候选不是通往 P 的路径上的鞍点。
- 判读：管线自身结论 `outcome=candidate_only; verified=false`（product 槽 MOL 与声明 SMILES 不符、连通性未证）与我的 E3 交付一致并加强：**无合格 TS、无连通性、无 ΔE‡**；这些端点能量同样**不得**充当 E3 的 dE 或分母（唯一分母仍是 job 961 = −939.320655479）。附注：−939.319097 ≈ 我可引的 IRC 外点值仅为记录，不是任何能垒。
- 通报：topic 帖（第一行 `to: as_a341823c436e47ed`，cc 写权会话 as_ec848a7673b74e35）；时间在 11:20 硬时线之后，标注为「记录，无需动作」。

### O.1 2026-10-17 13:50 — 两处口径校正（写权会话复核来函 evt_01a629f0fe9046bf 的回应）

- **最低实模以「频段表 Frequencies -- 块」为准**：§O 里 reactant 槽的 35.3946/46.4741/50.3614 取自 "Low frequencies" 探针行 L1504；解析频段表 L1513 ` Frequencies --     35.3651                46.4611                50.3485` 才是应引值（`tools/ts_freq_projection.py` 复核 reactant_frequency.log sha256 `139a17b9…` → `imaginary = 0`，lowest 1:35.3651, 2:46.4611, 3:50.3485, 4:71.6539, 5:85.3491, 6:99.8794）。product 槽同理：探针行 L1505 35.3403/46.4431/50.3024 vs 频段表 **35.3112/46.4293/50.2885**（后者为准）。结论不变（两槽皆 I2）。
- **job 1033 IRC 事实补正**：确有反向点——L1489 `Point Number  1 in FORWARD path direction.`→L2110 `Point Number:   1          Path Number:   1`；L2170 `Point Number  1 in REVERSE path direction.`→L2793 `Point Number:   1          Path Number:   2`；L2862 `Total number of points:                    2`；L3672 `Normal termination … 11:32:37`。准确表述为「正反各仅 1 点、共 2 点」⇒ 仍无终点区间证明（§O 的「无反向点」写法作废，改为本条）。
- 平台 verdict（写权会话核实）：ts_inspect ts_0011 = rev 51 / status ended / stage verdict / terminal candidate_only；reason 原文「Declared species identity: product built MOL does not match its declared SMILES; connectivity is unverified … The candidate stays UNVERIFIED」。E3 未被验收、ΔE‡ 仍 missing、分母仍锁 −939.320655479。
- **sha 取代说明（2026-10-17 14:05，仅版本引用、不改判读）**：本节上两处提到的 HI1/STATUS.md `29b0b413…` 是写权会话「勘误改档后、追加 §R9.7 之前」的中间态；**现行有效值为 `5f6acbe5af0672ae072377c8afc87726de3102991a53b23e71d9c5b1e14ab7fe`**（含 §R9.7 勘误段），HI1/PROCESS.md 仍为 `021d85ac5ee59c3da28ff942bc08925838af35c2ef7928fb6e0be822812b8f48`。两版差异仅 §R9.7 一节，结论完全一致。
- **引用约定（2026-10-17 14:20，采纳写权会话建议）**：对方台账为 append-only，每次追加都会改变整文件 sha，故此后引用一律用**章节号（§R9.5/§R9.7/§R9.8…）+ 该节内行号或日志 sha256**，**不以整文件 sha 作为「同一版本」判据**。观测记录：HI1/STATUS.md 在追加 §R9.8 后为 `131d0ad9216223e7f205ee9722591a5bff8d02ee558a92b05164f2a221dec72e`（仅作时点观测，不作版本判据）；HI1/PROCESS.md 仍 `021d85ac5ee59c3da28ff942bc08925838af35c2ef7928fb6e0be822812b8f48`。E3 不变项不受任何 sha 漂移影响。

## P. 2026-10-17 14:40 — 新授权：E3 拆步（E3a/E3b）｜模型定案 41 原子｜1046/1047 判为规格外

- **新授权（写权会话 14:0x）**：E3 拆成 E3a（I2+H2O→hemiaminal）与 E3b（hemiaminal→P），各建独立 ts_prepare run；route 仍 B3LYP/def2SVP+GD3BJ+UltraFine+Tight+CPCM(DMSO)、q0 m1、8c/10GB、priority 0、HI1 ≤3 并行。
- **模型定案（写权会话 14:35 逐元素+邻接实测，与我的连通性剖分一致）**：E3 = **41 原子 C15H21NO4**，按 1.25×共价半径剖分 = C15H19NO3（38 原子亚铵-aldol 两性离子）+ **H2O（O25/H26/H27）**；水加成**不改组成** ⇒ **hemiaminal 仍 41 原子 / 117 模**（job 1028 实测正是 117 模 0 虚频）；**44 原子 C15H23NO5 / 126 模的写法作废**。P = aldol 24 + 脯氨酸 17 = 41 原子 / 117 模。
- **分母**：E3a = **job 961 末帧**（−939.320655479，sha 63dda25e…，117 模 0 虚频；E3a 的 ts_prepare 猜测必须从 961 末帧几何起算）；E3b = **hemiaminal 41 原子新算的 0 虚频极小**（不复用 1017/1028/1029 的能量）。
- **1046/1047 = 规格外截断模型（我的失误，接受判读）**：我把「苯甲酸/苯甲酸根旁观组分」理解成可拆的 (R)-CH(OH)Ph 侧链并 cap 成甲基，得 27 原子 C8H15NO3（75 模）。事实是苯环属 aldol 片段的一部分（C29–C30 1.512、C29–O28 1.404、C29–C1 1.587），截断即换底物 ⇒ **不得作任何分母、不进 ΔE‡、不进 hi.py 节点**，仅作方法学对照登记；不杀进程，终态后只登记数值+用途。
- **交付的节点字符串（已于 14:40 发给写权会话，RDKit 2026.03.6 校验 C15H21NO4/q0/41 原子，CIP map6=S、map16=R 与题面一致）**：
  - hemiaminal(41)（首选，标签 1–22 不变）：`[CH3:1][C:2]([O:4][H])([CH2:3][C@H:6]([O:5][H:22])[c:7]1[cH:8][cH:9][cH:10][cH:11][cH:12]1)[N:20]1[CH2:19][CH2:18][CH2:17][C@H:16]1[C:14](=[O:13])[OH:15]`
  - 可选版（映射两个水 H，标签扩到 23）：I2 `...C(=O)[O-].[O:4]([H:21])[H:23]`；hemiaminal `...[C:14](=[O:13])[O:15]([H:23])]`；P `...[O:13]=[C:14]([O:15]([H:23]))[C@@H:16]...([H:21])`。
  - reaction_center 三列（题面 map 1-based / 工作序 1-based / 平台 0-based）：E3a form C2–O4 = 2–4 / **2–25** / **1–24**；break O4–H = 4–(未标) / **25–27** / **24–26**；form O15–H = 15–(未标) / **10–27** / **9–26**；E3b break C2–N20 = 2–20 / **2–4** / **1–3**；break O4–H21 = 4–21 / **25–26** / **24–25**；form N20–H21 = 20–21 / **4–26** / **3–25**。
- **质子归属细节（须进终稿）**：题面 map 把羧基质子定在 **map 15**（= 工作 O11，declare.json 末对 (10,26) 0-based = 工作 (11,27)）；而 job 1028 实测把质子放在**等价氧 O10**（O10–H27 0.9949 Å，O11 为 1.214 Å 的 C=O）。两氧共振等价、物种相同，但生成器 bond_changes 按 (11,27) 记 ⇒ 身份核验需把两个羧基氧视为可互换，或在 E3b 起点几何上做 O10↔O11 质子重定位。
- **hemiaminal 41 输入已备好、未提交**：`runs/hemi41/hemiaminal_41_optfreq.gjf` sha256 `226430f57795df145e08030a705108ab32dd971012f9a92008a1568a19fb2638`；起点 `runs/hemi41/hemiaminal_41_seed.xyz` sha256 `c3869dab2c8a2d3412e4a42939f6acd59092d8ab011604cfcb4d052aa2062054`（job 1028 末帧 L18955，水已加成的 41 原子几何；能量由新作业重算）。
- 纪律与状态：全局 4/4 满（1044/1046/1047/1048），**我不再提交新作业**，等写权会话放槽；不碰 hi.py/生成器、不调 priority、不杀进程。

### P.1 2026-10-17 14:15 — 图字符串口径定案 + hemiaminal_41 输入改版（仍待槽）

- **图级质子记账口径（写权会话裁决 §R10.5 / hi.py 注释 L104–L112，我接受）**：E3a 的 `break [[2,20],[4,22]] / form [[2,4],[5,22]]` 中，(2,20) 是 **C2=N20 的 π 键级由 2 降 1**（不是键消失）；(4,22)→(5,22) 是**图级「水 H 换家到醇盐氧 O5」的记账**，**不是**计算几何里的真实质子终点。ΔE‡/能垒只由计算给出，节点字符串只承载结构。**禁止**字符串/日志/报告三者静默不一致。
- 我此前的两版字符串（首选版含未映射 [H]、可选版引入 H23）**作废**；hemiaminal 节点以写权会话落地版为准：`[CH3:1][C:2]([O:4]([H:21]))([CH2:3][C@H:6]([O:5][H:22])[c:7]1[cH:8][cH:9][cH:10][cH:11][cH:12]1)[N:20]1[CH2:19][CH2:18][CH2:17][C@H:16]1[C:14](=[O:13])[OH:15]`（q=0、映射 1–22 守恒、CIP map6=S/map16=R；我 RDKit 2026.03.6 复核通过）。E3b 的 out = 题面 product 原字符串（确认）。
- **hemiaminal_41 输入改版**：旧 `runs/hemi41/hemiaminal_41_optfreq.gjf`（sha 226430f5…，标题内 smi​les 为已作废的 H23 版）降级为历史记录、**不提交**；新 `runs/hemi41/hemiaminal_41_optfreq_v2.gjf`（sha256 `9e53e0ba7cd0f3f261dcbc32bec5e3fea4d42901f41449f842a1dbb698406d39`）route/资源不变，**标题第 5 行 = `smiles(node,adopted):` + 落地版节点字符串逐字相同**；坐标逐行复制自 `runs/hemi41/hemiaminal_41_seed.xyz`（sha c3869dab…，41 原子、工作序）。
- **收敛后必做核对（已排入 checklist，一次报齐）**：①O4/O5/O13/O15 的 O–H 归属与距离 + 工作序 O10/O11/O25/O28 与 H21/H22/H24/H26/H27 的距离矩阵；②与节点字符串逐项对照并列出差异；③实测若在羧基氧 ⇒ 双写「字符串=醇盐氧表示 / 实测=羧基氧，O–H=x.xxxx Å，同一物种共振等价」；④模数自校验 41 原子 ⇒ 117 模（39 组 Frequencies）；⑤ZPE / Stationary point / 两处 Normal termination 行号时间 / 0 负虚频判定（只认频段表+imaginary 头）。
- 待命：**不放槽不提交**（当前 4/4：1044/1046/1047/1048，1049/1050 排队）；1046/1047 只登记「截断模型 + 75 模数值 + 用途=方法学对照」。

### P.2 2026-10-17 14:25 — E3a 猜测两枚就位 + 方案 A/B/C（等写权会话定夺）

- **G1（早期）** `prep/guess_c2o25_190/ts_guess_c2o25_190.xyz` sha256 `2568ca035c3ee37dc9472cd86bd3a751547ba835f99332cf8ce2ac91177bb186`：R(C2–O25)=1.8996、O25–H27=1.0317、O10–H27=1.5015、C2–N4=1.3308、O25–H26=0.9693。
- **G2（晚期）** `prep/guess_c2o25_160/ts_guess_c2o25_160.xyz` sha256 `2b569cfe7a267ad544bd3bfed237dea7ad0755a2c922ce952a423e433f8a2f50`：R(C2–O25)=1.5996、O10–H27=1.0048、C2–N4=1.4012。
- 两枚均源自 job 980 受约束扫描，而该扫描起点 = job 961 末帧几何（`I2_min_v5.xyz` sha 9a6203ff…）⇒ 满足「从 961 末帧起算、不另建构象」硬条件。
- **失败教训（决定选哪枚）**：job 999 的 ts_opt 用 G1 → 退回 I2 盆地成浅驻点、freq 唯一虚频 −128.0397 cm⁻¹ 为 C3 甲基转动 ⇒ 原样重跑很可能重复失败。
- 建议方案（待写权会话定）：**A（推荐）** 用 G2 + `opt=(TS,calcfc,noeigen)`（G2 在正确盆地之上坡侧，job 1028 从 G2 极小化落到 hemiaminal 极小）；**B** 用 G1 但以 ModRedundant 冻结/步进 R(C2–O25)（**先验证约束真生效**——job 962 曾出现裸 `B i j value` 被静默忽略、几何滑回 3.1597）；**C** 先做 R(C2–O25)×(O10–H27) 的 2D 松弛扫描取能量最高点作猜测。
- 数值纪律：E3 只认两个分母（job 961 = −939.320655479；新 hemiaminal 41 原子极小）。RC_27 的 −593.934532807 属 E1a 侧 27 原子子系统，**不混算、不引用为 E3 分母**。
- 状态：零提交、零 ts_resume、零改图；1046/1047 等终态登记。

### P.3 2026-10-17 14:45 — job 980 的 E(R) 表（裁决要求的零算力核查）：有内点极大，但极大帧 = G1（已失败起点）

log `runs/preorg_v3/scan_c2o25_220_160.log` sha256 `436c4cd9225bd29c1ae65086e1394b27b886e4d45206f4efa91133b331030f66`（60,977 行，终止 L60977）；约束卡 L158 `B       2      25 S   4 -0.150`；route `opt=(modredundant,maxstep=10) …`；归档行 L60940 `HF=-939.3076656,-939.302903,-939.297772,-939.3013576,-939.3090476`；官方汇总 L59910–L59911（R7 = 扫描坐标）。

| 点 | R(C2–O25) | E (Eh) | ΔE vs 961 | SCF 行 | R(O10···H27) | R(C2–N4) |
|---|---|---|---|---|---|---|
| 1 | 2.19959 | −939.307665623 | +8.15 | L6225 | 1.6746 | 1.3051 |
| 2 | 2.04959 | −939.302902987 | +11.14 | L16443 | 1.6093 | 1.3146 |
| 3 | **1.89959** | **−939.297771992** | **+14.36（极大）** | **L25258** | 1.5015 | 1.3308 |
| 4 | 1.74959 | −939.301357590 | +12.11 | L53388 | 1.0242 | 1.3742 |
| 5 | 1.59959 | −939.309047571 | +7.28 | L59324 | 1.0048 | 1.4012 |

- **(a) 有内点极大**（单峰）；**(b) 极大在 R=1.89959 Å**（E=−939.297772，L25258，ΔE=+14.36）。
- **撞车**：该极大帧就是 G1（`prep/guess_c2o25_190/ts_guess_c2o25_190.xyz` sha 2568ca03…，StdOrient L25159；同点另一帧 L23024）⇒ 「用极大帧」= job 999 已失败起点。
- **读法**：R(O10···H27) 在点 3 仍 1.5015、到点 4 才 1.0242 ⇒ C–O 压缩能垒峰与质子转移**不同步**，协同鞍点更可能在 **1.90–1.75 之间**。
- **候选猜测**：S1 = 点 4 收敛帧 `prep/guess_c2o25_175/ts_guess_c2o25_175.xyz` sha256 `db055959e7ffe9277f9e71b253c6873574a3c6d7c712c194d9f7916fc5867fd5`（StdOrient L51856；R(C2–O25)=1.7496、O10–H27=1.0242、C2–N4=1.3742）；S2 = 点 3–4 线性内插到 R=1.82（可零算力生成，**推荐**，待授权）；S3 = G1（仅在换 TS 算法/加约束时）。
- 状态：零提交、零 ts_resume、零改图、零杀进程；等写权会话选 S1/S2/S3 与放槽。

### P.4 2026-10-17 14:10 — job 1047（截断模型）终态登记：仅方法学对照，不作分母

- 作业：`runs/reduced/hemiaminal_reduced_optfreq.gjf`（27 原子 C8H15NO3，规格外截断模型）→ log `runs/reduced/hemiaminal_reduced_optfreq.log` sha256 `315bdeb744c7f1b416acb1e74f0a60e90848d1c470888feb933f47ddbf959235`（13,891 行）。
- 原始行：L9834 ` SCF Done:  E(RB3LYP) =  -593.948060506     A.U. after    7 cycles`（L11311 freq 段起点同值）；L10108 ` Optimization completed.` / L10109 `    -- Stationary point found.`；L10768 ` Normal termination of Gaussian 16 at Sat Oct 17 14:06:35 2026.`（opt 段）；**25 组 `Frequencies --` = 75 模 = 3×27−6 ✓**；**无 imaginary 表头 ⇒ 0 虚频**；L12681 ` Zero-point correction=                           0.232338 (Hartree/Particle)`；L13891 ` Normal termination … 14:10:03`（freq 段）。
- 用途：**仅「截断模型 + 数值 + 方法学对照」登记**。**不得**作 E3a/E3b 分母、不进 ΔE‡、不进 hi.py 节点、不与 41 原子体系能量混排（跨模型不混算）。
- job 1046（截断 I2）14:10 仍在 opt 段（无 Frequencies 块），待终态后同样登记。

### P.5 2026-10-17 14:30 — E3a 猜测定案 S2（内插 R=1.82 Å）：已生成 + provenance 齐全，未提交

- 裁定（写权会话）：E3a 用 **S2**；S1 备选；G1（= 点 3 极大帧 = job 999 失败起点）不原样重跑。E(R) 剖面 +8.15…+14.36 一律记为**沿受约束坐标的剖面差，不是 ΔE‡**（E3a 的 ΔE‡ 仍 missing）。
- 产物：
  - xyz `prep/guess_c2o25_182/ts_guess_c2o25_182.xyz` sha256 `e3748c2c6c96af915c63d1fa8972187214916321999720667a68c9b2dd561b9e`（41 原子、工作序、C15H21NO4）
  - provenance `prep/guess_c2o25_182/PROVENANCE_ts_guess_c2o25_182.md` sha256 `518783131cbcfce2b682b443621c9c41c693247356f4880537de471bb318b322`
  - 脚本 `tools/mk_e3a_s2_interp.py` sha256 `08b2a83b9e433f2aaa30fe4442ca4ee01e2ebfca100e7e12da1685df772c6200`
- provenance 要素：源 log `runs/preorg_v3/scan_c2o25_220_160.log` sha 436c4cd9…；帧 **L25159**（R=1.89959）与 **L51856**（R=1.74959）；`lambda = (1.89959-1.82)/(1.89959-1.74959) = 0.530600`；两帧元素序逐位一致；关键距离 R(C2–O25) 1.8168、R(O10···H27) 1.2467、R(O25–H27) 1.2789、R(C2–N4) 1.3493、R(O25–H26) 0.9633、R(O10···O25) 2.5231；O10→全 H 距离表；单调性 1.8996>1.8168>1.7496（yes）；**minsep 861 对 = 0.9633 Å ⇒ PASS（≥0.9）**。
- **透明处理**：①键长修复 O28–H24 0.8420 → 0.9752 Å（纯内插切角缩短；方向保持，修复前后均记录）；②非线性失真说明（最大 C9–O11 = 1.1782 vs 两端 1.2480/1.2164；C9–O10 = 1.2689 vs 1.2655/1.3196），属内插假象、TS 优化会松弛。
- 状态：**未提交**（4/4、HI1 在飞 3、free cpus 0）；排队顺序 E1a > E3a(S2) > hemiaminal_41；S1 备选 sha db055959…、G1 不原样重跑；hemiaminal_41 v2 sha 9e53e0ba… 仍为唯一待提交版本。

### P.6 2026-10-17 14:40 — hemiaminal gjf 改到 v3（smiles 用 HI1_I4 逐字符同串）+ 排产改为「hemiaminal 最前」

- 写权会话 14:28 排产：**任一 HI1 槽释放即提交 hemiaminal_41**（最前），其次 E1a ts_prepare，最后 E3a 的 S2。
- 输入 v3（**唯一待提交版本**）：`runs/hemi41/hemiaminal_41_optfreq_v3.gjf` sha256 `168901bf9d0f23fe6b244ed26079d4373d684571dfa7f1243ee33f7cf8527310`（49 行）；标题第 5 行逐字符含 `smiles: CC(O)(C[C@H](O)c1ccccc1)N1CCC[C@H]1C(=O)O`；route/q0m1/8c/10240MB/priority0 同前；坐标同 seed（sha c3869dab…）。v2（9e53e0ba…）降为历史。
- **同一性证明**：HI1_I4 串与我给的映射节点串，去 atom-map 后 canonical isomeric SMILES 完全相同且 chirality-aware 双向匹配 True ⇒ 同一立体异构体（C15H21NO4、q0、41 原子）。
- 收敛后五项检查（不自行回填）：117 模/虚频逐项筛、O–H 归属与节点逐项对照（质子落羧基氧则双写）、ZPE、Optimization completed/Stationary point found、两条 Normal termination 行号时刻 + 终态 sha256。
- E3a S2 已落盘（xyz `e3748c2c…`、provenance `51878313…`），**只备不提交**；起跑后按判据核虚频模是否为 C2–O25 成键 + 质子中继（甲基转动主导即 pseudo-saddle）。

### P.7 2026-10-17 14:50 — S2 三项条件接受 + 待裁版本冲突（v2 vs v3）

- S2 复算与写权会话一致（R(C2–O25) 1.8168、R(O10···H27) 1.2467、R(C2–N4) 1.3493、R(O28–H24) 0.9752、minsep 0.9633 ≥0.9）；三项条件已接受：(a) O28–H24 修复由脚本完成且修复前后值可复现（provenance 内）；(b) 报告必须写明 **S2 是构造猜测、非收敛几何**，C9–O11 1.1782 / C9–O10 1.2689 为内插假象、由 TS 优化松弛；(c) 若最终 E3a TS 虚频模含不可忽略的 C9 羧基 C–O 伸缩 ⇒ 按「猜测伪象污染模式」上报，**不得当合格 TS、不得回填**。
- **顺序更正（主协调 14:28）**：hemiaminal（本 lane）排第一 → 1051 通过后 lane1 的 E1a ts_prepare → E3a 的 S2 TS。当前 4/4、free cpus 0、HI1 在飞 3（1046/1049/1051）。
- **待裁版本冲突**：写权会话 14:12 硬要求「gjf 的 smiles 注释与 HI1_I4 串逐字符相同」，我据此生成 **v3** `runs/hemi41/hemiaminal_41_optfreq_v3.gjf` sha256 `168901bf9d0f23fe6b244ed26079d4373d684571dfa7f1243ee33f7cf8527310`（标题含 `smiles: CC(O)(C[C@H](O)c1ccccc1)N1CCC[C@H]1C(=O)O`）；但其 14:33 消息又要求提交 **v2**（9e53e0ba…，标题为映射节点串）。二者坐标/route/资源完全相同（同 seed sha c3869dab…），仅标题 smiles 串不同；去 map 后 canonical isomeric SMILES 相同（同一立体异构体）。**已请其在 v2/v3 中回一字；未回不提交**（不擅自选版本，避免字符串-日志不一致）。
- 槽位监视：已挂 120 s 定时检查（判据 1046 log 出现 `Zero-point correction`）；任一槽释放即报「提交前快照（版本+sha+槽位）→ 提交 → job id」。若空槽来自 1049/1051，需写权会话 ping。

### P.8 2026-10-17 实测时刻勘误（本节时间全部来自 `date '+%F %T %Z'`，不引用推断值）

- 写权会话指出其帖内 14:26/14:35/14:41 等为推断值；**我同样犯了这个错**：§P.3–§P.7 的标题时刻（14:30/14:40/14:45/14:50 等）是我推算的，**不是实测**，现按纪律更正并给出每个产物的文件 mtime（`ls -l --time-style='+%F %T'` 实测）：
  - `prep/guess_c2o25_182/ts_guess_c2o25_182.xyz`、`…/PROVENANCE_ts_guess_c2o25_182.md`、`prep/guess_c2o25_175/ts_guess_c2o25_175.xyz`、`runs/hemi41/hemiaminal_41_optfreq_v2.gjf`、`runs/hemi41/hemiaminal_41_optfreq_v3.gjf`、`tools/mk_e3a_s2_interp.py`、`tools/mk_reduced_model.py`、`runs/reduced/hemiaminal_reduced_optfreq.log`、`runs/reduced/I2_reduced_optfreq.log` 的 mtime 见本轮命令输出（我在 14:18:50 CST 实测时，v3 gjf mtime = 14:16:05，1046 log 仍在写 = 14:18:48）。
- 影响范围：**只涉时刻标签**，不涉任何数值、sha256、行号或判读结论。此后我的报告一律写 `date` 实测时刻；若需要"某个动作发生在何时"，以对应文件的 mtime 或 log 内的 Normal termination 时刻为准。

### P.9 2026-10-17 14:26 实测 — 1046 终态登记 + 槽位释放后已提交 hemiaminal（**job 1053**）

- 槽位实测（`query_compute_queue`，`date` = 2026-10-17 14:26:03 CST）：node-local running 1049/1051/1052；in_flight 3、**free cpus 8**、slots 7 ⇒ 1046 于 14:25:57 终态释放的正是这一 8c 槽。
- **已提交 job 1053**：`runs/hemi41/hemiaminal_41_optfreq_v3.gjf` sha256 `168901bf9d0f23fe6b244ed26079d4373d684571dfa7f1243ee33f7cf8527310`（14:26:10 复核同值），41 原子 C15H21NO4，8c/10240MB/priority 0，state=ready，job_dir `runs/hemi41`。依据：写权会话 14:28 的常设授权「任一 HI1 槽释放 ⇒ 立刻提交 hemiaminal」+ §R11.8 提交口径。
- **job 1046（截断 I2）终态（仅方法学对照）**：log `runs/reduced/I2_reduced_optfreq.log` sha256 `8901c576021a6d71aa5429e93f5aaa5033e2c5e27528d98474b2dcb520b2c146`；opt 末次 SCF **L29526 −593.945202906**（freq 段首 SCF L30984 同值）；L29797 `Optimization completed.` / L29798 `Stationary point found.`；opt 段 Normal termination **L30453 @14:22:25**；**25 组 Frequencies = 75 模**、无 imaginary 表头 ⇒ 0 虚频；ZPE **0.229330**（L32354）；freq 段 Normal termination **L33547 @14:25:56**。**不作分母、不进 ΔE‡、不进 hi.py 节点、不与 41 原子能量混排。**
- 1053 收敛后按最终模板一次报齐（情形 1/2/3 + 羧基自洽检查 + O25 上的 H + N4 无 H + O10–H27/O11–H27 + 六条分母判据 + 五项检查）。

### P.10 2026-10-17 14:30 实测 — 1053 = 1028 的重复优化（承认并登记）；1028 作为 E3b 分母候选的软模量化

- **承认事实**：job 1053 的 seed `runs/hemi41/hemiaminal_41_seed.xyz`（c3869dab…）取自 **job 1028 末帧**（log sha 1ec7e4c6…，Standard orientation L18955）。§P 当时已注明「同一 41 原子 hemiaminal 物种的已收敛极小几何，能量由新作业重算」；动机是遵守此前「不复用 1017/1028/1029 能量」的约束（用新作业产出新证据）。写权会话实测逐原子 RMSD 0.0000 ⇒ **1053 = 同型重复优化**，登记为「重复优化/一致性检查」，不撤不杀不改。
- **job 1028 复核（与写权会话逐项一致）**：117 模、**0 虚频**、E **−939.312626605**（L16838 / L19117）、Stationary point **L17230 / L22249**、Normal termination **L18325 @10:56:06 + L23954 @11:10:09**、ZPE **0.347492**（L21772）、**最低实模 19.8439 cm⁻¹（L19814）⇒ 偏软**。
- **软模归属（新量化）**：19.8439 cm⁻¹ 模逐原子 |d| 首位 H38 0.299 / H24 0.285 / O28 0.257 / H39 0.248 / H19 0.233 / H36 0.222（苯环 + aldol-OH 摆动）；反应坐标投影小：**C2–O25 0.41%、C2–N4 0.45%**、O10–H27 0.14%、O25–H26 0.13%、O28–H24 0.17%、C9–O10 0.90%、C9–O11 0.88% ⇒ **软模不与 E3b 反应坐标强耦合**，但仍须在 E3b 报告声明「最低实模 19.84 cm⁻¹ 偏软，ΔE‡ 稳定性受影响」。
- **E3b 分母候选**：写权会话建议用 **job 1028**（前提「不得复用」随 41 原子模型更正而消失），1053 降为一致性检查；**等主协调书面确认**。若采用 1028，报告须写明取代理由。
- 1053 终态时须报：与 1028 的 **ΔE（kcal/mol）与元素序对齐 RMSD（Å）**；显著非零立即上报。
- E3b 报告两条硬要求：①双写（质子实测在 **O10 = map13 侧**，HI1_I4 串写在 O15 侧；同一物种共振等价）；②软模声明。

### P.11 2026-10-17 14:34:16 CST — 主协调 E3a 连带要求登记：TS 必须与 job 1028 同一质子分布

本节时刻来自实测 `date '+%F %T %Z'`（14:34:16 CST）；要求由主协调会话经 AgentHub call 于 14:33 前后下达两次，我已 call 收条（对方 session `as_ec848a7673b74e35`，首条 event `evt_dd7d730a206d4e7c`）。

**要求要点（登记，不改写判据）**

1. E3a 的 TS（S2 帧 sha `e3748c2c…` 起跑）**必须**收敛到与 job 1028 同一质子分布：质子落 **O10（map13 侧）**、**C2–O25 成键**、**N4 三配位**；产物端直接用 1028，不另算。
2. 若 TS 或其端点落到另一质子位置（O11 侧 / 桥位 / N–H）⇒ 报主协调，**不得把该端点当 1028 引用**，由其按 2a/2b/第三档裁定。
3. 端点身份按模板写：「产物端 = job 1028（E −939.312626605，117 模 0 虚频，sha 1ec7e4c6…），实测 TS 端点质子落 O10 = map13 侧、C2–O25 成键、N4 三配位 ⇒ 与 1028 一致（或写出差异）」。
4. 其余不变：E3a 闭环只需 TS + 反应物端 961；软模声明照实写；1053 只作一致性检查；零 ts_resume／零改图／零杀进程。
5. 主协调明确**接受**我给出的五条判定基线，并采纳「桥位是猜测起点、不是可接受终点」与「C9 羧基 C–O 伸缩伪象 ⇒ 不当合格 TS」两项口径。

**判据实测基线（job 1028；日志 `runs/interm_c160/interm_c160_optfreq.log` sha256 `1ec7e4c6388415d0859939238f4f96ec7739c0bbf1f985a28f4dd3c23b7dcec1`，几何 = 该 log 末帧 L18955）**

| 读数 | 值 | 含义 |
|---|---|---|
| R(O10–H27) | 0.9949 Å | 质子**确在 O10 = map13 侧** |
| R(O11···H27) | 3.0517 Å | O11 侧无键（排除 case 2） |
| R(O25–H26) | 0.9693 Å | 水 residue H26 留在 O25 → hemiaminal O–H（E3b 的迁移质子） |
| N4 配位 | 三配位，最近 H（H23）2.1204 Å | 无 N–H → E3b 产物端才出现 N4–H26 |
| C9–O10 / C9–O11 | 1.3297 / 1.2137 Å | 质子化氧 = 较长（单键）氧，自洽 |

**与已申报 reaction_center 的对齐**：E3a = form C2–O25、break O25–H27、form O10–H27（N4 全程三配位），与要求同侧。S2 猜测（`prep/guess_c2o25_182/ts_guess_c2o25_182.xyz` sha `e3748c2c…`）是**中继中途帧**（R(O25–H27) 1.2789、R(O10···H27) 1.2467、R(C2–O25) 1.8168、R(C2–N4) 1.3493），故「桥位」只是起点状态；TS 必须把 H27 收到 O10 侧。S2 为构造猜测、非收敛几何，C9–O10 1.2689 / C9–O11 1.1782 为内插假象。

**队列实测（本节时刻，`query_compute_queue`）**：in_flight 4 槽 / 32 cpu，free cpus **0**、free mem 10480 MB；running 1049（14:07:05）、1051（14:10:04）、1053（我的 hemiaminal v3，14:26:08）、1054（14:28:41，NY3 `NY3_R2/fallback_O2/o2_scan.gjf`，非本包）；1052/1050/1048（NY3）failed，按「只登记不代管」处理。⇒ **E3a ts_prepare 现无槽可提**，顺序照冻结（1053 → E1a（等 1051）→ E3a S2）。

### P.12 2026-10-17 14:34:16 CST — E3b 猜测准备边界 + 1053 报告口径收窄

- **E3b 只准备、不提交**：主协调 14:34 明确「可以准备猜测，但只准备、不提交」。
- **E3b reaction center 复核一致**（主协调已核映射）：图中 `HI1_E5` 成对为 mapped break `[[2,20],[4,21]]` / form `[[2,4],[20,21]]`，折算到 E3 工作序 = **break C2–N4（工作 2–4）与 break O25–H26（工作 25–26）、form N4–H26（工作 4–26）**，并伴随 **C2–O25 由单键升为双键**（工作 2–25）。我此前写的「C2–N4 断、O25–H26 断、N4–H26 成」与之一致。
- **E3b 分母 = job 1028（已批准）**；产物端 = `HI1_P` 节点串（declared product_smiles，不改写）；**barrier 仍为 null**，直到 TS 频率 + 两端身份 + 连通性齐备。
- **1053 报告口径收窄（主协调 14:34）**：只需报「与 1028 的 ΔE(kcal/mol) + 元素序对齐 RMSD(Å) + 一条『重复优化、无新信息』结论」，**不再出全套模板**（本节替代 §P.10 内 1053 的全模板要求）。
- 1053 状态（实测 `query_compute_job`）：state=running，起 14:26:08，log `.cloudra/calc-1053.out.log` 增长中；终态通知到达后按收窄口径回报。

### P.13 2026-10-17 14:36:59 CST — E1b 分母口径更正入册 + E3b 探索扫描「只准备不提交」落盘

本节时刻实测 `date '+%F %T %Z'`；主协调三轮 call（14:33 / 14:34 / 14:38 / 14:41 前后）已由我逐条收条（最近 event `evt_505d1e645eba4477`）。

**1) 跨道引用口径（更正我自己的笔误）**：E1b 分母 = **27 原子子系统**（job 1051 / INT1_27，E −593.929762803，L26615/L28142；log sha `c03e0a82…`，75 模 0 虚频，最低实模 78.1490 cm⁻¹，ZPE 0.232709 L29511，Stationary L26904，Normal termination L27581 @14:31:05 + L30757 @14:35:06，ΔE vs RC_27 = +2.99 kcal/mol）。我上一条 call 误写「25 原子」，按主协调更正为 27 原子；结论不变：**该数与 E3 的 41 原子任何能量绝不相减**，我只作跨道一致性对照，**E3a 分母 = job 961、E3b 分母 = job 1028 均不改**。

**2) E3b 探索性松弛扫描：已落盘、未提交（主协调 14:38 明确暂不放行）**

| 项 | 值 |
|---|---|
| 输入 | `prep/e3b_scan/hemi_c2n4_scan.gjf`，sha256 `add74ec7bf5627c5e1400460730dcead7ee50912c2248e19d9282c9c6bddfe6e`（2281 B / 52 行，写盘 14:36:07.19） |
| provenance | `prep/e3b_scan/PROVENANCE_hemi_c2n4_scan.md`，sha256 `81fec45d2d1f54cba6344aef295e4e2269641577e572dbb65f76c37616917503` |
| 生成方式 | `ts_guess(mode='scan_prepare', engine='gaussian')`，坐标非手写 |
| 结构 | 41 原子 C15H21NO4、元素序与 `runs/hemi41/hemiaminal_41_seed.xyz`（sha `c3869dab…` = job 1028 末帧 L18955）逐分量偏差 `max|Δxyz| = 0.000000`；minsep 0.9673 Å |
| route | `# opt=(modredundant,maxstep=10) B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=DMSO)`（与已被接受的 job 980 扫描同形态；扫描作业不是 `opt freq`） |
| 坐标 | `B 2 4 S 5 0.205045`：R(C2–N4) 1.4248 → 2.4500（6 点），Gaussian 1 基 2=C2、4=N4，H26 完全自由 |
| 状态 | **prepared / not submitted**；排序 ①E1a ②E3a S2 ③EM1 ④E3b；**未获批前即使有空槽也不提交，先报主协调** |

**3) 起点实测（同 seed，供判读对照）**：R(C2–N4) 1.4248、R(C2–O25) 1.4728、R(O25–H26) 0.9693、R(N4···H26) 3.1829、R(O25···N4) 2.3213、**∠(O25–H26···N4) = 22.95°（O–H 几乎背向 N4）**、∠(N4 孤对轴, N4→H26) 103.4°、N4 三配位（C2 1.4248 / C5 1.4728 / C8 1.4555，无 H）、羧基 C9–O10 1.3297 / C9–O11 1.2137、O10–H27 0.9949（E3b 全程不该动）。

**4) 判读规则（先定口径、事后不改）**：A 协同（单个内部极大 + R(O25–H26) 增大 / R(N4···H26) 减小）；B 分步（H26 全程留在 O25 ⇒ 质子化酮/氧碳正离子 + 胺，**与 `HI1_E5` 声明拓扑不符 ⇒ 先报主协调、不改图**）；C 无峰（一维窗口无鞍点，**不**据此断言不存在鞍点）；另必查羧基 H27 是否迁移、大 R 端是否仍为接触对、逐点是否真收敛。扫描点能量**永不**作分母 / ΔE‡ / hi.py 节点。

**5) 两条纪律（主协调 14:38）**：① 扫描只作「受约束单峰 + 两端身份」口径下的连通性替代证据，单点不作判据；② 若出现分步拓扑，先报、不改图、不改 declared reaction center。

**6) 待办状态**：E3a 起跑仍等「槽位 + 主协调放行」两条同时满足（放行后提交前给版本+sha+槽位快照，提交后按 §P.11 质子分布判据逐条回报）；1053 终态只报 ΔE(kcal/mol) + 元素序 RMSD(Å) + 一条「重复优化、无新信息」结论。

### P.14 2026-10-17 14:37:59 CST — 1053 中途实测（opt 一步即收敛，freq 进行中；一致性已现端倪）

- `runs/hemi41/hemiaminal_41_optfreq_v3.log`（写盘 mtime 实测 14:37:42，226,730 B）：**NAtoms=41**（L164），route L85 `#p opt freq B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=DMSO)`。
- 首个 SCF：**E(RB3LYP) = −939.312626605 A.U. after 12 cycles（L1042）** —— 与 job 1028 的 −939.312626605（L16838/L19117）**到 9 位小数完全相同**（因为是同一几何/同一方法）。
- Berny 第 1 步（L1633）直接 `Optimization completed.` / `-- Stationary point found.`（L1909/L1910）；收敛表 Maximum Force 0.000009 / RMS Force 0.000002 / Max Disp 0.000997 / RMS Disp 0.000163 全 YES ⇒ **重复优化在第 1 步即收敛**（起点就是 1028 的最小点），符合「重复验证」定位。
- `Link1: Proceeding to internal job step number 2`（L2497）→ 第二步为解析频率（L2499 route `#P Geom=AllCheck Guess=TCheck SCRF=Check GenChk RB3LYP/def2SVP Freq`），此刻正在 CPHF/二阶导数阶段（尾行 3,361–3,363 为 123 向量 pass 5–8），**尚未出 `Harmonic frequencies`**。
- 待终态再报：ΔE(kcal/mol)、元素序 RMSD（工具 `tools/compare_rmsd.py` sha256 `0d5ee942d3c3bc115106f1f2c96af78f38b225e50f15a03034de1aa919796446`，自校验：1028 log vs 其末帧 seed ⇒ RMSD 0.000000；跨模型对照组 1028 vs 980 末帧 ⇒ +2.245878 kcal/mol / RMSD 0.051290 Å）、117 模 0 虚频核对、一条「重复优化、无新信息」结论。

### P.15 2026-10-17 14:42:08 CST — job 1053 终态（done）：一致性检查通过 = 重复优化、无新信息

- log `runs/hemi41/hemiaminal_41_optfreq_v3.log` **sha256 `fa124ec4a597e81b733eeb5a66b704e45a9480f52b927ee576fddd6d15d660a3`**，8,118 行；Normal termination **L8118 @14:41:25**（另有 link-1 步界 L2495 @14:27:40）。
- **E = −939.312626605**（L1042 首 SCF/12 cycles；L3288 第 2 步 SCF/1 cycle）——与 job 1028（L16838/L19117）**到 9 位小数相同**。
- **ΔE(1053−1028) = +0.000000 kcal/mol（+0.000000000 Eh）**；**元素序对齐 RMSD = 0.000000 Å**（Kabsch 0.000000，max/atom 0.0000）⇒ 几何同一。
- 频率：39 组 = **117 模、0 虚频**（`Frequencies --` 带表逐项扫描无负值；log_parser `imaginary_frequencies = []`）；**ZPE 0.347492**（L5943）与 1028 相同；最低实模 **19.8437 cm⁻¹（L3985）** vs 1028 的 19.8439（L19814）—— 同一软模。
- 软模量化（`tools/freq_lowmode_oh.py`）：|d| 领头 H38 0.299 / H24 0.285 / O28 0.257 / H39 0.248（苯环 + aldol-OH 扭转）；对反应坐标投影 C2–O25 0.41%、C2–N4 0.45%、N4–H26 1.96% ⇒ 与 E3b 坐标不强耦合；软模标记 YES（<30 cm⁻¹）。
- 收敛：Optimization completed + Stationary point found（L1909/L1910；freq 后复核 L6419/L6420）。
- **结论**：1053 = 重复优化、无新信息；**不作分母、不作 hi.py 节点、不进任何 ΔE‡**。**E3b 分母维持 job 1028**（E −939.312626605、117 模 0 虚频、sha `1ec7e4c6…`），软模 19.84 cm⁻¹ 声明一并保留。
- 已报：topic `gold-finish-20261015`（首行 `to: as_a341823c436e47ed`，post `evt_3e7e6fadf212489a`，主协调 message `evt_87fa675bf5ec4831`）+ 写权会话 call（`evt_3c8c0a61f767467a`）。
- 队列实测（2026-10-17 14:42:08 CST）：in_flight 3 槽 / 24 cpu，**free cpus 8**、free mem 20720 MB；running 1049@14:07:05、1054@14:28:41、**1055@14:36:37（lane1 E1a 起跑后即腾出槽位）**。⇒ E3a 现在**有槽**，只差主协调放行。

### P.16 2026-10-17 14:46:23 CST — E3a 起跑：run ts_0016 建立 → job 1059（ts_opt）

- **run**：`ts/ts_0016`（唯一 E3a run，未另建）。修订链：rev 5（首次 declare，map 阶段 `endpoint_identity_mismatch`）→ rev 10（补产物立体 `[C@@:2]`，转为 `atom_map_missing`）→ rev 13（补 atom_map 后转 `endpoint_binding_ambiguous`，对称羧基氧）→ rev 17（试互换两氧 → `endpoint_binding_invalid`，**回退**）→ rev 22（map/build 通过，assemble 要 reaction_center）→ rev 28（补 `[[2,25],[25,27],[10,27]]`，进 guess）→ **rev 35（补 guess，进入 submit/refine）**。
- **产物身份修正（真实发现）**：job 1028 末帧的 hemiaminal 在 C2 上有确定手性，而原映射节点串未声明该中心 ⇒ 工具判 `endpoint_identity_mismatch`（declared `CC(O)(…)` vs concrete `C[C@@](O)(…)`）。修法：节点串写 `[C@@:2]`，RDKit 3D 判键 + 立体指派得到 `C[C@@](O)(C[C@H](O)c1ccccc1)N1CCC[C@H]1C(=O)O`（CIP R/S/S），去 map 后与修正串逐字符一致、chirality-aware 双向匹配 True。
- **atom_map**：恒等（1..41）。依据 = 两端 built seed 的**键集差恰为** form(2,25)、form(10,27)、break(25,27)，重原子邻居元素差异只在 C2(+O)、O25(+C)。
- **heavy_atom_binding（最终，工具已校验）**：reactant `[3,2,1,29,28,30,31,32,33,34,35,4,5,6,7,8,9,10,11,25]`（RDKit `GetSubstructMatches` 给出恰好 2 个重原子匹配，第一个即此值，第二个仅苯环 30..35 反序）；product `[3,2,25,1,29,28,30,31,32,33,34,35,4,5,6,7,8,9,11,10]`。
- **对称氧口径**（易误读，已落盘）：`prep/E3A_BINDING_AND_SYMMETRY_NOTE.md` sha256 `77dead9f85537dc01775c1a7f1a04e26b511be7c7e5b9e83a3f6a2b7b0d2872a` —— reactant 端 C9–O10 1.2544 vs C9–O11 1.2501（差 0.0043 Å，噪声级不可分辨谁是 =O）；product 端 O10 带 H27、1.3297 > 1.2137 明确；**map 标签的氧锚定在两端不是同一物理氧**，路径由 atom_map 恒等 + reaction_center 定义。
- **预组织证据（观察，不是结论）**：961 侧 O10···H27 **1.7171 Å** vs O11···H27 3.6455；1028 侧 O10–H27 0.9949 vs O11···H27 3.0517 ⇒ 水来的 H27 起点即预组织指向 O10，两端一致。
- **job 1059**（state=running，起 **14:45:35**）：ts_opt 输入 `ts/ts_0016/jobs/declaration_0007/ts_opt/refine.gjf` **sha256 `d539785b169b243d7f0bfd43f1d58f6be2fef441498e4c58ae0341a7ce41bb1a`**；route `#p opt=(TS,calcfc,noeigen) B3LYP/def2SVP empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=dmso)`；坐标 = S2 逐分量一致（max|Δxyz| 0.000000），R(C2–O25) 1.8168、R(O25–H27) 1.2789、R(O10···H27) 1.2467、R(C2–N4) 1.3493、minsep 0.9633。
- **槽位实测（2026-10-17 14:46:23 CST）**：in_flight 4 槽 / 32 cpu，**free cpus 0**、free mem 10,480 MB；running 1049@14:07:05、1055@14:36:37、1058@14:45:14、1059@14:45:35；queued 空。
- 条件授权（主协调）：仅 l103 FormBX/Bend/Tors 且崩前判据接近阈值 ⇒ `opt=(TS,calcfc,noeigen,cartesian)` 同级别重发一次并记对应关系；NStep 截断 ⇒ 只登记不重投；其它（滑回 RC/越产物端/多虚频/模矢不落声明键对）⇒ 报模矢+几何差待裁。

### P.17 2026-10-17 15:02:24 CST — E3b 产物端 P（41 原子）Opt+Freq 提交：job 1061

- **任务来源**：写权会话 15:00 转达主协调放行（空槽 8 cpus），要求立刻起 E3b 产物端 P 的 Opt+Freq。
- **job id = 1061**，job_dir `runs/P_e3b`，8 cpus / 10,240 MB / priority 0，local 后端；提交前槽位实测（15:01:48 CST）：in_flight 3 槽 / 24 cpu、**free cpus 8**、free mem 20,720 MB，running 1049 / 1059 / 1060，queued 空。
- **输入**：`runs/P_e3b/P_optfreq.gjf` sha256 **`d3b72aeae421780790bfd933acc5a0290de5d6da7938990803717276f9e760a4`**（2,356 B）；route 逐字 `#p opt freq B3LYP/def2SVP empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=dmso)`，`%nproc=8`/`%mem=10GB`，`0 1`；标题行逐字符含 `smiles: CC(=O)C[C@H](O)c1ccccc1.O=C(O)[C@@H]1CCCN1`；`od -c` 复核末尾 `\n\n`（防 l101）。
- **产物身份**：构造帧 RDKit 规范同分异构 SMILES 与 `HI1.json`（sha `54221e65…`）`nodes[10]/smiles[0]` **完全相同**；C15H21NO4、q0、**2 片段**；CIP：工作原子 8（脯氨酸 Cα）= S、工作原子 29（苄位醇碳）= S。
- **起点构造（方案 a，保持 E3 工作原子序）**：母体 `prep/hemiaminal_1028_lastframe.xyz`（sha `be789d5f…`）→ 断 C2–N4（平移脯氨酸片段至 **2.7000 Å**）、O25 收到 **C2–O25 1.2200 Å**、H26 迁到 **N4–H26 1.0200 Å**（N4 孤对方向）；脚本 `prep/build_P_e3b.py` sha `422edc91…`；种子 `prep/P_e3b_product_41_seed.xyz` sha `6c9d6ae2…`。
- **自查（全过）**：41 原子；minsep **0.9673 Å**；两片段最短重原子接触 **2.7000 Å**（在 2.6–3.0）；无 C2–N4 键；键集差恰为 **+N4–H26 / −C2–N4 / −O25–H26**；H27 留在 O10（0.9949 未动）；O25···H26 2.5338（已离开羟基）。
- **provenance**：`prep/PROVENANCE_P_e3b_product_seed.md` sha256 `3c21a6ff008af996030170694636b7bf3fe55e22a17094ec8af804af5e131fce`。
- **去重**：盘上与队列中均无既有 P/product Opt+Freq ⇒ 未建第二个；**未触碰** ts_0016（1059, E3a）与 ts_0015（E1a）。
- **交付口径**：117 模 0 虚频（只认 Frequencies 表 39 组×3）、Optimization completed / Stationary point found 行号、两条 Normal termination 行号+时刻、末次 SCF E 与行号、ZPE、最低实模数值+行号（<50 cm⁻¹ 时给前 4 个 |d| 原子与 C2–N4 / C2–O25 / N4–H26 投影%）、CIP（8 S / 29 S）；**ΔE(P − 1028 −939.312626605) 仅作节点能量差登记，不是 ΔE‡、不进任何 barrier**。

### P.18 2026-10-17 15:04:20 CST — §P.17 勘误（片段原子数）+ 一条归属更正（1.7479 Å 不是氢键）+ E3b 猜测构造器就绪

**1) 勘误（我方笔误，非静默改）**：§P.17「酮醇 25 + 脯氨酸 16」是**平移前的分片**（当时 H26 仍在 O25 上）。按**最终种子**重算（共价半径判键 + 连通分量）：脯氨酸片段 **17 原子** = N1 C5 O2 **H9**（C5H9NO2）；酮醇片段 **24 原子** = C10 **H12** O2；合计 41。写权会话独立复核亦为 24+17，以此为准。

**2) 一条归属更正（对方给的值对、原子对错，按实测改正）**：
- 最短**含氢**跨片段接触 **1.7479 Å 的原子对 = H26···C2**（迁到 N4 的质子指向**酮基碳**），**不是** N4–H26···O25。
- 实测：**N4–H26 1.0200 Å**、**H26···O25 2.5338 Å**、**N4···O25 3.2627 Å**、**∠(N4–H26···O25) 128.0°** ⇒ **不构成 N–H···O 氢键预组织**，而是**偏紧的 H···C 接触**（成因：H26 置于 N4 孤对方向，该方向偏向 C2 一侧）。
- 另一项确认：minsep **0.9673 Å 的原子对 = 24–28**，即 **H24···O28**（未被本步触及的 aldol O28–H24），与母帧同值，属巧合 —— 不是误抄 hemiaminal。
- **处置**：不掩饰、按实测登记；已把「H26···C2 接触是否在优化中松开 / H26 是否被拉回 O25 / 是否被当成 C–H」列为 1061 的显式检查项。若未松开即作**种子假象**上报，P 端点合格判据仍为「无 C2–N4 键 + N4–H 存在 + 两片段 + CIP 8=S/29=S」。

**3) E3b TS guess 构造器（主协调 15:0x 前瞻要求）——已就绪并通过干跑**

- 工具：`prep/mk_e3b_guess_interp_v3.py` sha256 `53b561c3a2f24cf1f305ac460fbaea2eca6d358e0cb9bb6340461bcd368bf0e2`；干跑目录 `prep/e3b_guess_dryrun_v3/`（用构造的 P 起点帧代替收敛帧，仅验证代码）。
- **两端原子序核对**：1028 末帧 sha `be789d5f…` 与 P 起点帧 sha `6c9d6ae2…` 均 41 原子、元素序**完全相同**（E3 工作序）；构造器对元素序不一致直接 abort。
- **排除的两个错误构造（实测读数，留作反例）**：① 全原子笛卡尔内插（v1）：H26 直线穿过 C2 附近，minsep **0.3819–0.6654 Å**（λ=0.1–0.4，原子对 25–26 / 2–26）⇒ 不可用；② H26 置于 N4→O25 弦上（v2）：按 C2 处余弦定理该弦距 C2 ≈1.05 Å ⇒ H26···C2 ≈**1.38 Å** 假 C–H 接触 ⇒ 不可用。
- **采用 v3**：重骨架内插 + H26 挂 N4（N4–H26 1.05 Å，方向 unit(N4−C2) 背离酮基碳）⇒ λ=0.05–0.95 **全部 PASS** minsep ≥0.9（0.9673），**R(C2–N4) 单调增、R(C2–O25) 单调减**。
- **干跑推荐帧**：λ=0.65 ⇒ **R(C2–N4) 2.2537 Å、R(C2–O25) 1.3085 Å、R(N4–H26) 1.0500 Å、minsep 0.9673 Å**；可用窗口 λ=0.55–0.80 ⇒ R(C2–N4) 2.13–2.45 Å。
- **语义声明**：这是**「晚段/质子已在 N」角点猜测**；λ<0.5 的帧不物理（质子瞬移，O25–H26 由 0.97 跳到 3.8 Å），只会在 λ≈0.55–0.8 选帧上报，并写明「构造猜测、非鞍点」。
- **E3b barrier 仍为 null**：TS 频率 + 两端身份 + 连通性齐备前不写任何 barrier；1061 收敛后先核「两片段 / C2–N4 ≥2.4 Å / N4–H / CIP 8=S 29=S」，再出正式猜测帧并报 sha。

**4) 在飞与等待**：job 1059（E3a ts_opt，起 14:45:35）与 job 1061（P Opt+Freq，起 ~15:01:5x）均由各自终态通知/日志检查驱动；E3b 扫描（`prep/e3b_scan/hemi_c2n4_scan.gjf` sha `add74ec7…`）**仍未提交**。

### P.19 2026-10-17 15:05:41 CST — E3b 取帧规则/构造器 v4 + P 的 H26 假象验收条款（登记）

**说明**：本节曾因文件被并发追加而 edit 返回 `conflict`，已重读后重写；不覆盖任何他人新增内容。

**1) 取帧规则（主协调裁定，不变）**：正式 guess 在 **λ∈[0.55,0.65]** 内取 **R(C2–N4) 最接近 2.15–2.25 Å 且 minsep 最大**那帧（**不用 λ=0.65 单点**），并落盘 **λ=0.50–0.80 逐行表**。

**2) 构造器 v4**：`prep/mk_e3b_guess_interp_v4.py` sha256 `8b7a36fb369e0c9b0b5b6f6e3e9d27ff8669f5712835bfcbaf66b8fc69f74cb9`（= 已批准的 v3 内插逻辑 + 选帧 + 报告；v3 基线 `prep/mk_e3b_guess_interp_v3.py` sha `53b561c3…` 仍保留作逻辑基线，已由主协调登记 LEDGER §R60⑤）。运行同时生成 `GUESS_SELECTION_<label>.md`，内含 **v1 反例（minsep 0.3819–0.6654 Å，λ=0.1–0.4，原子对 25–26 / 2–26）** 与 **v2 反例（H26···C2 ≈1.38 Å 假 C–H）** 的实测读数 ⇒ 供 ts_prepare 的 evidence_refs 引用真实 artifact。

**3) 干跑（用构造的 P 起点帧代替收敛帧，仅验证代码与规则；不进交付面）**：选中 **λ=0.57** ⇒ R(C2–N4) **2.1517 Å**（窗口低端）、R(C2–O25) 1.3287、R(N4–H26) 1.0500、R(O25–H26) 3.7983、R(H26···C2) 3.2017、minsep **0.9673**（原子对 24–28）；全段 R(C2–N4) 单调增 / R(C2–O25) 单调减。**正式帧待 1061 收敛后重跑并报 xyz + md 双 sha。**

**4) P 的 H26 假象验收条款（1061 收敛后必查，主协调新增）**：
- 判据 A：**C2···H26 是否松开**（>2.4 Å 视为松开）；判据 B：**H26 是否被拉回 O25 成 O–H**；判据 C：**是否被算成 C–H**。
- 若 A 未松开（维持 ~1.75 Å 量级）或 B 成立 ⇒ **P 判构造假象**：不作 E3b 产物端、不写「P 的合理结构」；处置 = 重出种子（H26 置于 N4 孤对且**背离 C2**，即 unit(N4−C2) 取向）后重提交。
- 若 H26 松开（C2···H26 >2.4 Å 且 N4–H26 1.0–1.05 Å）⇒ 正常收。**起点基线备核**：C2···H26 1.7479、N4–H26 1.0200、H26···O25 2.5338、N4···O25 3.2627、∠(N4–H26···O25) 128.0°。

**5) 顺序与分工**：1061 收敛 → 四项核对（两片段 / C2–N4 ≥2.4 Å / N4–H 存在 / CIP 8=S、29=S）+ 上述三查 → 正式帧 + 双 sha → **我建 E3b 的 ts_prepare run**（不手搓 TS）。**ts/ts_0015（E1a，owner lane1）不触碰**。

**6) 排产**：1061 腾出的槽先给 **E1a 的 frequency**（关键路径）；1060（NY3）腾出的槽给 **E3b 的 ts_opt**；free cpus 0（1049/1059/1060/1061 在飞）⇒ E3b 排队属预期：**不重投、不调 priority、不 kill**。

**7) 口径**：E3b 分母 = job 1028；ΔE(P−1028) 只作节点能量差、**非 ΔE‡**；E3b barrier 在「恰 1 虚频 + 模矢对 C2–N4 断裂 / N4–H26 生成 + 两端 0 虚频 + 连通性」齐备前一律 **null**。

### P.20 2026-10-17 15:43:04 CST — E3a（ts_0016）ts_opt 正常收敛：Stationary point，几何正是 C2–O25 成键 + 质子中继；freq 作业 1067 在跑

- ts_opt = **job 1059**（起 14:45:35）：`ts/ts_0016/jobs/declaration_0007/ts_opt/refine.log`，30,219 行；**Normal termination L30219 @15:42:07**；**Optimization completed / Stationary point found L29133 / L29134**（第 30 步，max 232）；**无** FormBX / Bend failed / Tors failed / NStep 截断。
- **末次 SCF：E(RB3LYP) = −939.295152015 A.U.（L28774，7 cycles）**（上一步 L27923 −939.295151302）。
- **能量差（仅登记，非 barrier 定论）**：ΔE(TS − job 961 = −939.320655479) = **+0.025503464 Eh = +16.0037 kcal/mol**；ΔE(TS − job 1028 = −939.312626605) = +0.017474590 Eh = +10.9655 kcal/mol。**在虚频判据通过前，这些只作「收敛驻点的能量差」，不写成 ΔE‡。**
- **收敛驻点的端帧几何实测（工作序 1 基）**：`C2–O25 1.8613`、`O25–H27 1.1636`、`O10–H27 1.2466`、`O11–H27 3.3582`、`∠(O25–H27···O10) 176.2°`、`O25–H26 0.9690`、`C2–N4 1.3433`（仍近亚胺双键）、N4 三配位（C2 1.3433 / C5 1.4810 / C8 1.4709，最近 H 为 atom 23 的 2.1146 Å ⇒ **无 N–H**）、`C9–O10 1.2908` / `C9–O11 1.2284`；minsep 0.9674（原子 24–28）。
⇒ 这正是**「C2–O25 成键 + O25–H27→O10 质子中继」**的图像（H27 处于 O25 1.1636 / O10 1.2466 的中继位、N4 未被质子化），且羧基 C–O 没有异常拉长的一般化假象特征；**最终判定仍须 freq 结果的虚频模矢投影**。
- **pipeline 已自动进入 freq 阶段**：`jobs/declaration_0007/frequency/frequency.gjf` sha256 `76c5fc09e2e75d782f09a69912da44cb83bf38eb0628acec160a49c1932675ec`，route `#p freq B3LYP/def2SVP empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=DMSO)`，几何 = 上帧（同目录 `optimized.xyz`）；**job 1067 running（起 15:42:12）**。
- 道状态 stage：`refine`，`waiting_for = job:1067`（rev 39）。**barrier 仍未定稿**：等 1067 的「恰 1 虚频 + 模矢投影」判据。

**续（freq 结果到手后必须逐条报）**：39 组 = 117 模；虚频个数与数值（带 `Frequencies --` 行号）；用 `tools/freq_lowmode_oh.py` 报 C2–O25 / O25–H27 / O10–H27 及甲基/羧基投影份额；若被 C3 甲基转动主导 ⇒ pseudo-saddle；若含不可忽略 C9 羧基 C–O 伸缩 ⇒ 猜测伪象污染、不当合格 TS；并给 ZPE、两条 Normal termination、末 SCF、端点一致性（O10–H27 成键、N4 三配位、C2–O25 成键）。

### P.21 2026-10-17 15:44:10 CST — 冻结期口径（写权会话裁定 A-lite）：允许零算力出帧，禁止建 run/提交

- **交付已冻结**：E3a result=null、E3b result=null、barrier 0/4；**冻结期内不接受新计算提交、不新开 ts 管线 run**（ts_prepare 会建 run 并在可行时自动提交 ts_opt）。
- **允许（零算力）**：1061 收敛后做四项核对（两片段 / C2–N4 ≥2.4 Å / N4–H 存在 / CIP 8=S,29=S）+ 种子假象三查（C2···H26 是否松开、H26 是否回 O25、是否被当 C–H），再用 **v4（sha `8b7a36fb…`）** 出正式 guess 帧 + `GUESS_SELECTION` 报告并报双 sha 与 H26···C2 / R(C2–N4) / R(C2–O25) / R(N4–H26) / minsep。
- **禁止**：建 ts_prepare run、提交 E3b 的 ts_opt、提交任何新作业、删除盘上产物。
- **标注**：这些 post-freeze 产物一律写「**post-freeze asset、非交付证据、未提交**」；不进 §14 口径、不进任何 barrier、不与 1059/1061 读数混成「E3b 已验证」。
- **若假象三查任一触发** ⇒ 按「P 端点作废、需重出种子」登记并发证据给写权会话；**冻结期内不改种子**（改种子＝新输入）。
- 1067（E3a freq）终态仍按 §P.20 续报口径给全套读数（只写道内台账 + 回报），**barrier 不回填**。
- 本条口径以主协调最终回复为准；更严则照更严执行。

### P.22 2026-10-17 15:44:32 CST — 最终口径（主协调裁定，取代 A-lite）：E3b 允许出帧 + 条件式允许建 ts_prepare

- **授权范围（零算力）**：1061 收敛后做四项核对 + H26 假象三查 + 用 **v4（sha `8b7a36fb…`）** 出正式 guess 帧与选择报告（报双 sha）；产物一律标 **post-freeze asset、非交付证据、未提交**；**不许为出帧改种子**。
- **有算力部分（条件式）**：当且仅当 P 通过四项核对与三查、**且 free cpus ≥8（不抢占 1049/1061/1067）** ⇒ 我可**直接建 E3b 的 ts_prepare run**（durable ts 工作流，禁止手工提交 TS/IRC），并立即报 job id / 输入 sha / route 首行；条件不满足 ⇒ **停在出帧，不再请示**。
- **地位**：全部为 **post-freeze 追记**；报告 `a2964d8d…`（277 行）与交付面 11 文件 sha **不动**；E3b barrier 在「恰 1 虚频且模矢含 C2–N4 断裂 + N4–H26 生成、两端 0 虚频、连通性」齐备前一律 **null**；回填与否、是否改交付面由下一窗口决定；E3a 的 +16.0037 / +10.9655 kcal/mol 只作**收敛驻点能量差**、不称 ΔE‡。
- **纪律**：不重投、不调 priority、不 kill、不碰 ts/ts_0015、不删盘上产物；1067（E3a freq）终态读数只报道内台账与技术回报。
- **与 §P.21 的关系**：本节取代 §P.21（A-lite 只允许零算力部分），差异仅在「P 通过且有空槽时可建 ts_prepare」；已同步写权会话（其 A-lite 由本节覆盖）。

### P.23 2026-10-17 15:55:26 CST — E3a freq（job 1067）终态：唯一虚频 −783.7914 cm⁻¹，模矢 = 质子中继主导 + 真实 C2–O25 成键分量；IRC（1068）在跑

**日志**：`ts/ts_0016/jobs/declaration_0007/frequency/frequency.log`，**sha256 `c5ac84026e43c5155f2bf6e20787885f77662666e737ad4783e16036ae7291b9`**，5,294 行；**Normal termination L5294 @15:54:25**。

**① 完整性行**：N = **41**（该帧实际原子数）⇒ 3N−6 = **117**；频段表 **39 组 ×3 = 117 模**（首组 `Frequencies --` **L1510**，末组 **L3334**）⇒ **相等，模数完整**。

**② 虚频行**：频段表内负值 **1 个** = **−783.7914 cm⁻¹（L1510）**；imaginary 头行 **L1501「****** 1 imaginary frequencies (negative Signs) ******」**；另 L3439「1 imaginary frequencies ignored.」（热化学忽略该模，属正常）。**Red. mass 1.5559 / Frc const 0.5632**。最低实模 = **23.6787 cm⁻¹（同行 L1510，第 2 个值）**，软模标记 YES（<30 cm⁻¹）。

**③ 投影行（mode 1 = −783.7914，`tools/freq_lowmode_oh.py` + `tools/analyze_mode_signed.py`）**

| 原子对 | 占比（Σ|d|²） | 该模上的 dR/dq（取「H27 朝 O10」为正向） | 判读 |
|---|---|---|---|
| (10,27) O10–H27 | 96.67% | **−0.959** | 成键（缩短）✅ |
| (25,27) O25–H27 | 96.25%→（同一 H 平动的连带投影） | **+0.890** | 断裂（拉长）✅ |
| (2,25) C2–O25 | **6.71%** | **−0.252** | 成键（缩短）✅ 真实但小于质子分量 |
| (11,27) O11–H27 | 96.25% | −0.967 | 只是 H 平动几何连带（O11–C9 伸缩仅 0.78%） |
| (9,10) C9–O10 | 0.68% | −0.081 | 羧基 C–O 伸缩 **小**，无伪象主导 |
| (9,11) C9–O11 | 0.78% | +0.034 | 同上 |
| (2,4) C2–N4 | 2.75% | +0.065 | 轻微拉长（未参与主要坐标） |
| (4,26) N4–H26 | 5.13% | −0.120 | 无 N–H 生成（H26 仍远） |
| (25,26) O25–H26 | 0.05% | −0.001 | 未受影响 ✅ |

|d| 领头：**H27 0.942**（占 Σ|d|² **88.8%**）、H26 0.234、C2 0.153、O25 0.106、C9 0.051、O11 0.044、H13 0.042、H16 0.041；**C3 甲基氢（H14/H15/H16 = 0.036/…/0.041）小** ⇒ **不是 job 1029 那种甲基转动主导的 pseudo-saddle**。H27 位移矢量 (−0.340, +0.870, +0.120)，|u|=0.942；对 O10→O25 方向投影 **+0.920** ⇒ 取正向（H27 朝 O10）后**质子确实由 O25 迁向 O10**。

**诚实的定量表述**：该虚频模是**质子中继主导**（H27 占 88.8% 位移平方），**同时含真实但较小的 C2–O25 成键分量**（dR(2,25)/dq = −0.252，pair share 6.71%）；不含甲基转动主导、不含羧基 C–O 伸缩主导。⇒ **按既定判据它不是 pseudo-saddle、也不是猜测伪象污染模式；是否等同于声明的「协同加成」鞍点，由主协调/写权会话裁定，我不自行称 qualified TS。**

**能量登记（不作 ΔE‡）**：E(TS) = **−939.295152015（L816，13 cycles）**；ΔE(TS − job 961 = −939.320655479) = **+0.025503464 Eh = +16.0037 kcal/mol**；ΔE(TS − job 1028) = +0.017474590 Eh = +10.9655 kcal/mol。**barrier 仍 null**（还需 IRC 双向端点身份 + 两端各 0 虚频 + 连通性）。ZPE = **0.342095（L3469）**。

**pipeline 已自动进入 IRC**：`jobs/declaration_0007/irc/`，**job 1068 running**；run stage=refine、`waiting_for job:1068`（rev 43）。
**队列（2026-10-17 15:55:26 CST）**：in_flight 3 槽 / 24 cpu、free cpus 8；running 1049 / 1061 / 1068。**1061（P Opt+Freq）仍在跑**。

### P.24 2026-10-17 15:58 CST — E3a 两端 0 虚频登记（补 §P.23 缺测项，含 961 侧机械核验）+ 模矢符号约定统一 + 1068 / 1061 进展

**① 两端 0 虚频登记（§P.23 的缺测项现已闭合）**

- **产物侧 = job 1028（半缩醛胺，即「hemiaminal 侧」本身，不是另一端）**：`runs/interm_c160/interm_c160_optfreq.log`，sha256 `1ec7e4c6388415d0859939238f4f96ec7739c0bbf1f985a28f4dd3c23b7dcec1`：41 原子、39 组 ×3 = **117 模**、**0 虚频**、最低实模 19.8439 cm⁻¹（L19814）、ZPE 0.347492（L21772）；纯重复作业 1053 复核同一个值：`runs/hemi41/hemiaminal_41_optfreq_v3.log`（sha256 `fa124ec4a597e81b733eeb5a66b704e45a9480f52b927ee576fddd6d15d660a3`）39 组 ×3 = 117、**频段表负值个数 = 0**、最低 19.8437（L3985）、ZPE 0.347492（L5943）、Normal termination L8118 @14:41:25。
- **反应物侧 = job 961（I2 + H2O）**：`runs/I2_optfreq/I2_optfreq.log`，sha256 `63dda25e04529e65920526304fb88755db9393e9c22bd3a6efb76eeee0af0d0e`，24,001 行；**NAtoms = 41（L167）**；`Frequencies --` **39 组 ⇒ 117 模 = 3N−6**（首组 L19879、末组 L21703）；**无「imaginary frequencies」头行**（grep 计数 0）；**频段表内负值个数 = 0**；最低模 **35.3075 cm⁻¹（L19879）**；ZPE 0.345935（L21837）；Stationary point found L17316；Normal termination L18401 @2026-10-15 21:59:30 与 L24001 @22:05:55；E(RB3LYP) = **−939.320655479**（L16950 / L19183）。
- ⇒ **E3a 两端均满足「41 原子 / 117 模 / 0 虚频 / 收敛」两项硬性条件**；仍缺 **IRC 双向端点身份**（job 1068），故 **E3a barrier 仍为 null**，+16.0037 / +10.9655 kcal/mol 只作该 TS 驻点相对两个极小点的电子能差。

**② 模矢符号约定（此后只用这一套，避免两套符号并存）**

- 约定：**+q = 质子转移方向（H27 由 O25 移向 O10）**。该方向上的 dR/dq（单位 Å·amu⁻¹ᐟ²）：**R(10,27) = −0.959**、**R(25,27) = +0.890**、**R(2,25) = −0.252**。
- 写权会话独立复算给出的 +0.9589 / −0.8898 / +0.2525 **幅度逐项相等、整体反号**，即同一条本征矢在 **−q** 下的读数（本征矢整体乘 −1 不改变物理内容），**不是数值分歧**。
- 约定无关的不变量：**相对符号三元组 (−, +, −)** —— 质子转移方向上 O10–H27 缩短、O25–H27 拉长、C2–O25 缩短。
- **份额分母声明**：本会话份额 = (Σ_{i∈pair}|d_i|²)/(Σ_{全部原子}|d_i|²)（L2 平方分母）；H27 = **0.888（88.8%）**、C2–O25 pair = 0.0671、C9 羧基 C–O 合计 0.0146。写权会话的 0.8939 用了另一种归一化（|d|/Σ|d| 类），**引用时须同时写分母**。

**③ 进展（本次实测 2026-10-17 15:57:42 CST）**

- **job 1068（E3a IRC，管线自动提交，rev 43 / stage=refine / waiting_for job:1068）**：15:54:27 起跑；15:57:42 读 `ts/ts_0016/jobs/declaration_0007/irc/irc.log` **823 行、仅 1 次 SCF Done、尚无 `Total number of points` 行** ⇒ 仍在首个 IRC 点/初始 Hessian 阶段，**暂无可登记读数**（不据此判「不收敛/无通道」）。
- **job 1061（P Opt+Freq）**：`runs/P_e3b/P_optfreq.log` **42,770 行**；**Step 44/239**；最新 SCF **−939.319076200**（L41908，9 cycles，Lowest energy point so far）；收敛判据 Maximum Force 0.000195 YES、RMS Force 0.000044 YES、**Maximum Displacement 0.089446 NO**、RMS Displacement 0.022330 NO ⇒ **力已收敛、位移未收敛**，作业未完成。
- P 起始帧当前能量 −939.319076 比 job 1028 的 −939.312626 更低（ΔE ≈ −4.05 kcal/mol），但这**只是未收敛帧的电子能，不是节点能量差**，待 1061 终态再按同一批 B3LYP/def2SVP(DMSO) 口径登记。
- 队列：running **1049 / 1061 / 1068**。

### P.25 2026-10-17 15:59 CST — 活日志引用约定（时刻 + 行数 + 当时 sha 三件套）+ 1068 / 1061 本次实测

**① 约定（主协调 §P.24 复核 D 项提出，采纳）**：`ts/ts_0016/jobs/declaration_0007/irc/irc.log` 是**活日志**，同一文件不同时刻行数/sha 都会变。此后引用一律写「**实测时刻 + 行数 + 当时 sha256**」三件套，不把两个不同时刻的 sha 当冲突。

**② 本次实测（2026-10-17 15:58:53 CST，独立 date）**
- `irc.log`：**847 行**，sha256 **`c62a84d3df4ebd1d6991750cf8a8216b4411e0421423be8b4ce5d3b775566860`**，SCF Done 计数 **1**，**无 `Total number of points` 行**、无 `Normal/Error termination` ⇒ 仍在首个 IRC 点/初始 Hessian 阶段，**无可登记读数**。写权会话 15:58:30 独立实测同为 847 行 / 同一 sha ⇒ 两方读数对齐，非冲突态。
- `irc.gjf`：sha256 `fad5c8b8e250e3b10433aaad4923e318d22bcbc29ee4624e342496ec66381a44`（49 行），route 首行 `#p irc=calcfc B3LYP/def2SVP empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=dmso)`；能量口径统一引 **L816 `SCF Done: E(RB3LYP) = -939.295152015`**，L785/L801 为末两次 SCF 迭代值（旁证）。
- `runs/P_e3b/P_optfreq.log`（job 1061）：**43,710 行**；**Step 45/239**（L42915）；最新 SCF **−939.319074016**（L42827，9 cycles）；**无 `Stationary point found` / `Normal termination`** ⇒ 未完成，E3b 四项核对未开始。

**③ 状态不变**：E3a = 1 虚频 ✓ / 模数完整 ✓ / 模矢含声明键对三分量 ✓ / 两端 0 虚频 ✓ / **方向与连通性待 1068 双向 IRC** ⇒ **result=null、barrier 不回填**；+16.0037（对 961）与 +10.9655（对 1028）kcal/mol 只作驻点电子能差。1068 若出 l123 / 单侧不收敛 / NStep 截断，一律登记「IRC 未完成」，不写「无鞍点 / 通道不存在」。

### P.26 2026-10-17 16:00 CST — 端别固定写法 + job 961 日志两段结构辨析（opt 段 / freq 段）+ 行号引用纪律

**① 端别固定（与主协调 §R11.37、写权台账一致，此后只此一套）**
- **961 = 反应物端**（I2，38 原子 + H2O，3 原子 = 41 原子）；**1028 = 产物端 / hemiaminal 端**。
- 于是：ΔE(TS − 961) = **+16.0037 kcal/mol** 为「相对反应物端」、ΔE(TS − 1028) = **+10.9655 kcal/mol** 为「相对产物端」；961 比 1028 低 **5.04 kcal/mol** ⇒ 若 IRC 端点身份成立，能垒量级应参照**较低端 961**，但**连通性齐备前不给 ΔE‡、不回填**。

**② job 961 日志为「opt 段 + freq 段」拼接，引用必须注明段别**（`runs/I2_optfreq/I2_optfreq.log`，sha256 `63dda25e04529e65920526304fb88755db9393e9c22bd3a6efb76eeee0af0d0e`，24,001 行；本次逐行自读 2026-10-17 15:59 CST）：

| 段别 | 关键行 | 内容 |
|---|---|---|
| **opt 段** | L17315 / L17316 | `Optimization completed.` / `-- Stationary point found.` |
| opt 段末 SCF | **L16950** | `SCF Done: E(RB3LYP) = −939.320655479`（6 cycles） |
| opt 段结束 | **L18401** | `Normal termination … Thu Oct 15 21:59:30 2026` |
| **freq 段** | L19183 | 该段首个 `SCF Done: E(RB3LYP) = −939.320655479`（1 cycle，与 opt 段末同值） |
| freq 段 | L19873 | `Harmonic frequencies (cm**-1) …` 标题 |
| freq 段 | L19879 → L21703 | `Frequencies --` 39 组 = 117 模，最低 35.3075 cm⁻¹ |
| freq 段 | L21837 | `Zero-point correction = 0.345935` |
| freq 段结束 | **L24001** | `Normal termination … Thu Oct 15 22:05:55 2026` |

- ⇒ **两个 Normal termination 是同一作业的 opt 段与 freq 段各一个**，不是跑了两遍、也不是重复计算；引用时写「opt 段 L18401 @21:59:30 / freq 段 L24001 @22:05:55」。
- **不可引用的早期优化步**：**L16109 `SCF Done: E(RB3LYP) = −939.320655262`**（较早优化步，比收敛值高 2.17×10⁻⁷ Eh ≈ 0.00014 kcal/mol），仅作收敛过程旁证，**不得当作端点能量**。端点能量唯一口径 = **−939.320655479**（opt 段末 L16950、freq 段 L19183 同值）。
- 频段最低模旁证（写权会话 `gauss_mode_check.py` 独立跑）：35.3075 cm⁻¹，Red. mass 4.1273 / Frc const 0.0030，imag_header = None。

**③ 本次实测进展（2026-10-17 15:59:23 CST，三件套）**
- **job 1068（IRC）**：`irc.log` **850 行**，sha256 `e431a57307d2055e836474fc5a6fe966e5c1068379d683eb8b8ffacf9d40929a`，SCF Done 计数 **1**，仍**无 `Total number of points` 行**、无 termination ⇒ 首个 IRC 点/初始 Hessian 阶段，无可登记读数。
- **job 1061（P Opt+Freq）**：`runs/P_e3b/P_optfreq.log` **44,535 行**；**Step 46/239**（L43827）；最新 SCF **−939.319078868**（L43739，9 cycles）；**无 Stationary point / Normal termination** ⇒ 未完成。

### P.27 2026-10-17 16:02 CST — 主协调裁定「E3a 不解冻」入本车道台账（即使 1068 双向 IRC 完美收敛也不回填）+ 下一窗口四项判据 + 5.038 kcal/mol 精确值

**① 裁定（沿用主协调 15:59:34 CST 决定）**：**E3a 不解冻**。交付面（报告 `a2964d8d…` / 277 行 + 11 文件 sha）保持冻结；**即使 job 1068 双向 IRC 完美收敛，+16.0037 也不写进生成器 / `HI1.json` / 报告**，只在 LEDGER 追记「可引用值 + 判据落点 + 证据清单」，并标注「未回填、冻结面内仍 null」。回填属**下一窗口**决定。⇒ **本车道此后不在报告或生成器侧留任何回填痕迹**，本 STATUS 内 E3a 的数值一律按「驻点电子能差 / 可引用值（未回填）」措辞。

**② 下一窗口回填的四项判据（先记下，避免口径漂移）**
1. IRC **双向** Normal termination（单向不算）；
2. 两末端与 961 / 1028 的连通性一致：C2–O25 距离、H27 归属（O10 还是 O25）、片段组成相符；关键键长差 **≤ 0.03 Å**；末端能量不高于对应端点 **+1 kcal/mol**；
3. 两端各 0 虚频（**961 ✓ 最低实模 35.3075 cm⁻¹（L19879）；1028 ✓ 19.8439 cm⁻¹**）；
4. TS 恰 1 虚频（**−783.7914 cm⁻¹，L1510，imaginary 头行 L1501**）+ 模矢三分量（相对符号三元组 **(−, +, −)**，|dR| = **0.959 / 0.890 / 0.252 Å·amu⁻¹ᐟ²**）。
齐备才写 **ΔE‡ = E(TS, L816) − E(961, L16950/L19183) = +16.0037 kcal/mol**。

**③ 数值精确化（正式引用口径）**
- E(961) − E(1028) = −939.320655479 − (−939.312626605) = **−0.008028874 Ha = 5.038 kcal/mol**（此前写的 5.04 属四舍五入，正式引用一律用 **5.038**）。
- ΔE(TS − 961) = +0.025503464 Ha = **+16.0037 kcal/mol**；ΔE(TS − 1028) = +0.017474590 Ha = **+10.9655 kcal/mol**（均只作驻点电子能差，非 ΔE‡）。

**④ 活日志引用纪律再确认**：活日志 sha 是**时刻快照**（15:58:19 → 823 行 `505aafd1…`；15:58:53 → 847 行 `c62a84d3…`；15:59:23 → 850 行 `e431a573…`），引用必须带实测时刻，**终态后重取一次作为定稿**。

### P.28 2026-10-17 16:25 CST — 两个作业的中间态实测：1061 的 opt 段已收敛（Step 71，E = −939.319540184），freq 段在跑；1068 IRC 双向推进中（正向 10 点 / 反向 3 点）

**① job 1061（P Opt+Freq）—— opt 段收敛，**尚未** 整体完成**
- 日志 `runs/P_e3b/P_optfreq.log`，**69,174 行**（16:24:53 CST 快照）；**Step 71 / 239**（L66965，最后一次迭代）。
- 收敛判据（L67248 起）：Maximum Force **0.000015 YES**、RMS Force **0.000003 YES**、Maximum Displacement **0.001020 YES**、RMS Displacement **0.000295 YES** ⇒ `Optimization completed.`（L67254）/ `-- Stationary point found.`（**L67255**）。
- **opt 段** SCF 末值 **E(RB3LYP) = −939.319540184**（**L66877**，7 cycles）；**opt 段** Normal termination **L68350 @2026-10-17 16:24:12**。
- **freq 段** 已开始（freq 段首 SCF **L69139 −939.319540184**，1 cycle，与 opt 段末同值 ⇒ 频率在收敛几何上做）⇒ **作业整体仍在跑（job state = running）**，**尚无 freq 段 Normal termination、无频段表**。
- **能量登记（只作节点电子能差，不作 ΔE‡、不进任何势垒）**：E(P, 未过频) − E(1028) = −939.319540184 − (−939.312626605) = **−0.006913579 Ha = −4.338 kcal/mol**；E(P) − E(961) = **+0.001115295 Ha = +0.700 kcal/mol**。**P 未过频 ⇒ 不是验证过的极小点**，该值不写进交付面。

**② job 1068（E3a IRC）—— 双向推进中**
- `irc.log` **13,226 行**（16:24:53 CST 快照），sha256 `f89a48dfef71c03ac5595869ebdb22930ed8525db172dccc526e6c14ce218588`；`SCF Done` 计数 18；**Path Number 1（正向）到 Point 10**（L9449）、**Path Number 2（反向）到 Point 3**（L12766）⇒ **双向都在走**，**尚无 `Total number of points` 汇总行、无 termination**。
- 近期点能量（沿 TS 下降，均低于 TS 的 −939.295152）：L13201 −939.296266、L13214 −939.296250、L13227 −939.296280、L13239 −939.296280 ⇒ 反向路径刚开始、能量仍在 TS 附近稳步下降，符合「从鞍点向两端下坡」的形态；**端点身份仍待终态判定**。

### P.29 2026-10-17 16:32 CST — job 1061 内部步 1（opt）收敛帧的四项核对 + CIP 自算：全部通过；但**已批准的 v4 guess 构造在真实 P 帧上被 minsep 门禁拒绝**（新事实，需裁定）

**① P 端点四项核对（本次自算，工具 `tools/cip_check_41.py` sha256 `748b74554107259392952bcc28af59510ab30827e84af837d2c6fee839d4c4b9` 新增；输入 `prep/P_1061_optframe.xyz` sha256 `957b95970f05a052d882094d5434027594498cbe6d733590180a2c3003006f9a`，由 `runs/P_e3b/P_optfreq.log` 的 opt 内部步末帧导出）**
- **41 原子；片段 [24, 17]（两片段）✓**；formula **C15H21NO4** ✓；**C2–N4 = 3.3308 Å（≥ 2.4）✓**；**N4–H26 = 1.0200 Å（存在 N–H）✓**。
- **CIP：原子 8 = S、原子 29 = S ✓**；全体系 isomeric SMILES = `CC(=O)C[C@H](O)c1ccccc1.O=C(O)[C@@H]1CCCN1`，**与声明的 P 节点字符串逐字符相同 ✓**；片段 SMILES = `CC(=O)C[C@H](O)c1ccccc1` + `O=C(O)[C@@H]1CCCN1` ✓。
- **H26 假象三查：全部未触发** —— C2···H26 = **2.9922 Å**（种子期 1.7479，已松开 >2.4）✓；H26 仍挂 N4（N4–H26 1.0200）、未回 O25（**O25···H26 = 3.1370 Å**）✓；H26 未被当 C–H（最近碳 C2 2.9922）✓。
- 产物几何自洽：C2=O25 **1.2172**（酮生成）、O10–H27 **1.0112**（羧基 OH）、O25···H27 2.3670、C9–O10 1.3282 > C9–O11 1.2115、**minsep 0.9689（pair 24–28，O28–H24 羟基 O–H，属正常键长）**。对照半缩醛胺 1028 帧：R(25,26) 0.9693（H26 在 O25）、R(2,26) 2.0398、R(2,25) 1.4728、R(2,4) 1.4248 ⇒ 反应坐标方向与声明一致（C2–N4 断裂 1.42→3.33、C2–O25 1.47→1.22、H26 由 O25 迁到 N4）。
- ⇒ **E3b 四项核对 + H26 三查在 opt 内部步收敛帧上全部通过**；但 **job 1061 的频段（内部步 2）仍在跑**（16:31:20 实测 69,208 行、仅 1 个 Normal termination、无 `Frequencies --` 行）⇒ **P 尚未取得「0 虚频」证据，不是频率验证过的极小点**。

**② 新事实（阻塞项）：已批准的 v4 构造在真实 P 帧上失败**
- 运行 `prep/mk_e3b_guess_interp_v4.py`（sha `8b7a36fb…`）以 `runs/hemi41/hemiaminal_41_seed.xyz`（sha `c3869dab…`）为反应物、`prep/P_1061_optframe.xyz` 为产物：**报错 `no acceptable frame in lambda 0.55-0.65`**，**未写出任何帧/报告**（`prep/e3b_guess_formal/` 为空目录）。
- 诊断（`prep/diag_e3b_interp.py` sha256 `24b88ba62b63668e50dceaee12e098c4fa20d76093c25da0bb861b787d134d77`，λ 0.30–0.90 全表）：**minsep 0.7562（λ=0.50）– 0.8908（λ=0.90），恒 < 0.90 门禁**；窗口内 λ=0.56 / 0.60 / 0.64 的 minsep = **0.7598 / 0.7660 / 0.7752**（pair 恒为 24–28）。
- 成因（可复现）：**两个端点是不同构象**。全分子 Kabsch RMSD = **1.9369 Å**（比无旋转的元素序 RMSD 1.6770 Å 还大 ⇒ 不是整体转动问题）；分片段 Kabsch RMSD = **1.0721 Å（24 原子酮醇片段）/ 0.6109 Å（17 原子脯氨酸片段）**。逐原子全坐标线性插值因此压缩**片段内键长**：O28–H24 0.9673→**0.756**、C33–C34 1.3982→**1.015**、C1–H12 1.0983→**0.79**。
- ⇒ v3/v4 的插值逻辑是在**构造的 P 种子**（与 1028 同构象）上验证的；换成**优化后的真实 P 帧**后，桥接区间必然经过不合理的紧密接触。**这不是 H26 假象，也不是 P 不佳**，而是「构象差异 + 逐原子笛卡尔插值」的方法局限。

**③ 后续构造建议（未实施，等裁定）**
- **(a) v5 = 刚体片段插值 + 反应坐标内坐标插值**：分片段 Kabsch 逐片段刚体插值（旋转按轴角测地线、质心线性），使所有片段内键长保持不变；再把真正变化的反应坐标（C2–O25 1.4728→1.2172，沿 C2–O25 轴移动 O25）单独按 λ 插值；H26 仍按已批准规则挂 N4 1.05 Å（方向 unit(N4−C2)）。诊断已验证刚体片段插值下 `prep/diag_frag_interp.py`（sha `0a0f5bf2…`）：**minsep 恒为 0.9673（pair 24–28，属正常 O–H），R(C2–N4) 1.7419→3.2443 单调，无任何 < 1.20 Å 的非键接触**；但刚体插值把 **C2–O25 冻结在 1.4728**（产物为 1.2172）⇒ 必须补内坐标插值。
- **(b) 用已备好但未提交的约束扫描**：`prep/e3b_scan/hemi_c2n4_scan.gjf`（sha `add74ec7…`，`B 2 4 S 5 0.205045`）在半缩醛胺自身构象里拉 C2–N4，用扫描峰值作 guess（有算力成本，但构象一致）。
- 两条都属「换构造 ⇒ 新输入」，**在裁定前我不发射正式帧、不建 ts_prepare run、不提交任何作业**。

### P.30 2026-10-17 16:38 CST — 三个终态/阻塞：**1061 freq 完成（117 模 0 虚频 ⇒ P 是频率验证过的极小点）**、1068 IRC 被默认 maxpoints=10/方向截断（端点未达 ⇒ E3a 仍 null）、ts_0016 现 blocked 于 `verification.reactant_endpoint.optimization`；另 v5 的 H26 规则实测不成立、v6 尚在自检中

**① job 1061（P Opt+Freq）终态 —— freq 内部步 2 完成**
- `runs/P_e3b/P_optfreq.log`，sha256 **`183590c1ff28965769ebab84704e50f0ffbf0f9d63320bd9e0a4d0ec36aea15a`**，**73,964 行**（自读 16:34:27 CST）。
- **两个 Normal termination**：**L68350 @2026-10-17 16:24:12**（内部步 1 = opt）、**L73964 @16:34:16**（内部步 2 = freq）。
- 频段：`Frequencies --` **39 组 ×3 = 117 模 = 3N−6（41 原子）✓**；**无 `imaginary frequencies` 头行**；**频段表负值个数 = 0 ⇒ 0 虚频 ✓**；最低实模 **16.6787 cm⁻¹（L69831 首值）**。
- ZPE = **0.344928**（L71789）；Sum of electronic and zero-point = **−938.974612**（L71793）；E(RB3LYP) = **−939.319540184**（opt 末 **L66877** / freq 段首 **L69139**，同值）；`Stationary point found` **L67255**（opt）/ **L72262**。
- ⇒ **P 现在是「41 原子 / 117 模 / 0 虚频 / 收敛」的频率验证极小点**（闸门 ①② 满足）。节点电子能差：ΔE(P − 1028) = −939.319540184 + 939.312626605 = **−0.006913579 Ha = −4.338 kcal/mol**（**只作节点能量差，不是 ΔE‡，不回填**）。

**② job 1068（E3a IRC）终态 —— 双向正常终止但路径被默认 maxpoints 截断**
- `ts/ts_0016/jobs/declaration_0007/irc/irc.log`，sha256 **`0f9679f97f784a868a915857e63e690e200875dfab0eb25afe238975f166a4b6`**，**19,037 行**；**Normal termination L19037 @16:33:44**；`Total number of points: 20`（**L18232**）；`Maximum number of steps reached` **L9503**（前向）/ **L18200**（反向）、`Calculation of FORWARD path complete` L9504 / `REVERSE path complete` L18201 / `Reaction path calculation complete` L18202 ⇒ **route `irc=calcfc` 无 maxpoints，默认 10 点/方向**。
- 能量剖面（L18204–L18228，相对 TS −939.295152）：反向 −1.24413 → **−0.00370 Ha（−2.32 kcal/mol）**；正向 +1.24501 → **−0.00849 Ha（−5.33 kcal/mol）**；两向单调下坡 ⇒ **支持「TS 在路径上是极大」**，但**远未到极小点**（声明两端 11.0 / 16.0 kcal/mol）。
- **端点身份（我自算：`prep/extract_irc_points.py` sha `b49ed0d7e5bfd4aebac7488715529ae330ca1c08658d922c131bb3c5be4f597e` 导出 21 帧 → `prep/irc_points_1068/`，再用 `tools/compare_rmsd.py`）**：
  · 正向端 `irc_point_p1_10.xyz` vs hemiaminal(1028) **RMSD 0.3925 Å**（元素序、无旋转）/ vs I2 极小 **6.6460 Å**；
  · 反向端 `irc_point_p2_10.xyz` vs hemiaminal **0.4030 Å** / vs I2 极小 **6.6449 Å**；
  ⇒ **两端都停在 hemiaminal 附近（≈0.4 Å），没有一个到达极小点**；反向端几何朝 961 方向（C2–O25 2.061、O25–H27 1.040）但距 961 的分离值（C2–O25 3.160）仍差很远。
- ⇒ **连通性未建立：E3a result=null、barrier 不回填**；措辞统一为「**默认 IRC 参数（maxpoints=10/方向）下路径长度不足**」，**不得**写「连通性已证」或「通道不存在」。

**③ ts_0016 现处于 blocked（rev 46 / stage refine）**
- `ts_inspect(run_id='ts_0016')`：`status=blocked`、`blocked.failure_class=missing_input`、`needs=["verification.reactant_endpoint.optimization"]`、`next.action=resume`、`editable_groups` 含 `verification`。
- 需补的形状（**未执行**，等主协调放行）：`changes.verification.{reactant_endpoint,product_endpoint}.{optimization,frequency}` = `engine gaussian / method B3LYP / basis_set def2SVP / keywords empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=dmso)`（与 ts_opt/frequency 阶段同口径）。补齐后会新增端点 Opt（+Freq）管线作业，属**算力支出**，故先报批。

**④ E3b guess 构造（v5 规则被实测否定，v6 在自检）**
- **v5 的 H26 规则不成立**：按已批准 `unit(N4−C2)` 放置时，**λ=0.50 实测 H26···C8 = 0.9482 Å**（脚本按门禁中止、未写帧）；产物帧实测 **∠(C2–N4–H26) = 62.08°**、R(N4–H26) 1.0200、R(C8,H26) **2.1000**、R(O25,H26) 3.1370 ⇒ 真实 N–H 方向**不是** anti-C2，应改用**产物自身的 N4→H26 方向**（按片段 2 的插值旋转携带）。
- **端点内部几何差（逐片段 Kabsch 对齐后；剔除反应中心键 (2,25)/(4,26)）**：ketol(24) max|Δbond| **0.0322 Å（C1–C2）**、0.0287（C2–C3）、0.0111（O28–C29）；proline(17) max|Δbond| **0.0163 Å（H27–O10）**、0.0125（N4–C8）；max|Δangle| **15.64°**、max|Δtorsion| **177.9°**。
  ⇒ 端点差异 = **扭转差 + 反应中心键长变化（C2 由 sp³ 向 sp²）**。因此「λ=1 逐原子 ≤0.03 Å」与「片段内键长全区间 <0.01 Å」**互斥**，除非把与 C2/O25/N4/H26 相连的键作为反应坐标排除（与写权会话的技术提示一致）。
- **v6 = 内坐标（Z-matrix）插值**：自检未过（见 §P.31），**未发射任何帧**，`prep/e3b_guess_formal_v6/` 为空。

### P.31 2026-10-17 16:44 CST — v6（内坐标插值）自检未过、**v5 七条中第 1/4 条实测不可满足**；已构造 **v7（反应坐标形变猜测）**并通过全部自检，等主协调裁定是否以 v7 作为构造

**① v6 状态（未发射帧）**
- `prep/mk_e3b_guess_interp_v6.py` sha256 **`fcdf97056b2fce7d0d64f63b9ae62151a3d7cae66e553d79f1f3b049e79ad3d3`**（内坐标：键长 + 每原子在局部正交基下的方向分量）。
- **自检未过**：λ=0 重建帧对 1028 端点的 RMSD = **2.04066 Å**（断言阈值 1e-3）；诊断显示**片段内成对距离最大偏差 4.42 Å** ⇒ 逆变换/重建仍不一致（不是取向或镜像问题：proper/improper 叠合 RMSD 1.85/2.01 Å）。⇒ **未写任何帧**，`prep/e3b_guess_formal_v6/` 为空。

**② v5 七条硬条件的两条实测不可满足（关键结论）**
- **第 4 条（H26 沿 unit(N4−C2) 挂 N4 1.05 Å）**：λ=0.50 实测 **H26···C8 = 0.9482 Å**（脚本按门禁中止）。产物帧实测 **∠(C2–N4–H26) = 62.08°**、R(C8,H26) = 2.1000、R(O25,H26) = 3.1370 ⇒ 真实 N–H **不是** anti-C2 方向，该规则在本体系下会把质子塞进脯氨酸环。
- **第 1 条（λ=1 逐原子 ≤0.03 Å 落在 1061 末帧）与第 5 条（片段内键长全区间 <0.01 Å）互斥**：两端点键长本身差 **C1–C2 0.0322 Å、C2–C3 0.0287 Å**（C2 由 sp³ 变 sp² 的化学必然），另 C8–N4 0.0125、O28–C29 0.0111、H27–O10 0.0163 Å ⇒ **任何能到达 P 帧的路径都必然让这些键变化 >0.01 Å**；刚体插值虽保住键长，但 λ=1 与 P 的逐原子差约 1.07 Å（分片段 Kabsch RMSD 1.0721/0.6109 Å）。
- 即：**v5 在同一构造族里无论怎样调参数都过不了 1 或 4**；这不是参数问题，是端点构象差与规则本身的冲突。

**③ 已交付：v7 = 反应坐标形变猜测（单端、不声称产物端）**
- 脚本 `prep/mk_e3b_guess_v7.py` sha256 **`b5c445812532326dc9806b05aa1e915e6c6fd018aee59f032c2777e3966f5538`**；输入 **`prep/hemiaminal_1028_lastframe.xyz`（sha `be789d5f…`）/ `prep/P_1061_optframe.xyz`（sha `957b9597…`，仅用于 N–H 方向参照）**。
- 构造：以**频率验证半缩醛胺极小点（1028）**为基帧，**只改声明反应坐标**：
  · R(C2–N4) **1.4248 → 2.2000 Å**（脯氨酸片段沿 C2→N4 轴**刚体平移**，片段内几何不动）；
  · R(C2–O25) **1.4728 → 1.3688 Å**（沿 C2–O25 轴移 O25，取 C–N 拉伸的同一进度 0.407）；
  · H26 移到 **N4 上 1.05 Å**，方向取**产物自身的 N4→H26 方向**。
- 自检（全部通过，脚本内断言）：**41 原子、元素序与两端一致、map 不变（N4=4/C2=2/O25=25/H26=26/H27=27）**；**除反应中心外所有键长变化 = 2.2×10⁻¹⁶ Å（断言为 0）** ⇒ 不存在键塌陷；**minsep 0.9673 Å（pair 24–28，O28–H24 正常 O–H）**、**无非键接触 <1.20 Å**（最紧三条：12–13 1.7563、19–20 1.7753、14–15 1.7768）；**H26···O25 = 3.0821 Å（≥2.0）**、H26 最近碳 **1.8928 Å（≥1.60）**、N4–H26 = 1.0500；R(O10–H27) 0.9949（未动）、C9–O10 1.3297 > C9–O11 1.2137。
- 产物文件（post-freeze asset, non-delivery evidence，**未提交**）：
  · `prep/e3b_guess_formal_v7/E3B_TS_GUESS_v7_c2n4_2.200.xyz` sha256 **`be761bb04f2d80037a3f11381d5c1badba1c127bd1def5d5a8991d09223214d8`**（41 原子 + 2 行头 = 43 行）；
  · `prep/e3b_guess_formal_v7/GUESS_SELECTION_e3b_v7.md` sha256 **`9e88dfeb06db1ff79f87f22d8cb856d14c97c6dac4c4ebdfd522611e29145f91`**。
- **性质申明**：v7 是 **guess**，不是 TS、不是收敛几何、不含能量；E3b barrier 仍 null、不回填。
- **合规提示**：v7 与 v5/v6 属**不同构造**（不作端点插值、不声称 λ=1 端），按 §R90 口径**需主协调放行**；主协调已于 16:38:55 CST 明确放行（见 §P.32）。

### P.32 2026-10-17 16:41 CST — 按主协调 16:38:55 CST「放行 v7」裁定，**E3b run 已建：ts_0019 / job 1069（ts_opt）running**

**① run 与作业**
- `ts_prepare` 返回：**run_id = ts_0019**，`run_dir = /home/ly/Cloudra-mechanism-agent/ts/ts_0019`，**revision 11**，`status = waiting`，`stage = refine`，`blocked = null`，`next.action = wait_for_system`，`waiting_for = [{job_id: 1069, purpose: ts_opt, attempt 1}]`。
- **job 1069**：`ts_opt`、gaussian、node-local、**state = running**、**started_at 2026-10-17T16:39:27+08:00**。
- 输入文件：`ts/ts_0019/jobs/declaration_0001/ts_opt/refine.gjf`，**sha256 `f66c3c0c6f03e4c6e8763112db8e81b4fdde748489e94a9ccbeae96c5dc1bdc7`**，49 行。
- **route 首行逐字**：`#p opt=(TS,calcfc,noeigen) B3LYP/def2SVP empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=dmso)`；`%nproc=8` / `%mem=10240MB`。
- 声明内容（本节可核）：reactant `C[C@@](O)(C[C@H](O)c1ccccc1)N1CCC[C@H]1C(=O)O`（hemiaminal 1028 帧）、product `CC(=O)C[C@H](O)c1ccccc1.O=C(O)[C@@H]1CCCN1`（P 1061 帧）；`atom_map` = 1..41 恒等；`reaction_center` = **[[2,4],[4,26],[25,26]]**（1-based，C2–N4 断裂 / N4–H26 生成 / O25–H26 断裂）；guess = **v7 帧**（`be761bb0…`）with evidence_refs = v7 xyz + v7 报告（`9e88dfeb…`）两个真实文件；verification 的 frequency / irc / 两端端点 optimization+frequency 均 `{ref: g16}`，端点 seed 分别指 `prep/hemiaminal_1028_lastframe.xyz` 与 `prep/P_1061_optframe.xyz`（evidence_refs 指 `interm_c160_optfreq.log` / `P_optfreq.log`）。
- 提交前资源实测（16:39 前）：free **slots 9 / cpus 24 / memory 40960 MB**，仅 job 1049 在跑 ⇒ 满足 free cpus ≥ 8。



### P.33 2026-10-17 18:31 CST — job 1069（E3b ts_opt）中间态：**已滑到产物侧**（几何≈P，能量低于 P 极小点 0.154 kcal/mol），v7 guess 的 R(C2–N4)=2.20 Å 已在鞍点产物侧；收敛判据仍未满足

**① 定稿快照（实测 2026-10-17 18:31:10 CST）**
- `ts/ts_0019/jobs/declaration_0001/ts_opt/refine.log`，**126,254 行**，sha256 **`a9e8131561d381cf3de6024436eec3bf53009b68eb48438bf2d2da10d801de29`**（活日志，时刻快照）。
- **Step 133 / 239**（L125556）；末次 SCF **E(RB3LYP) = −939.319785350**（L125469，8 cycles）；`Lowest energy point so far`。
- 收敛判据（L125836 起）：Maximum Force **0.005534 NO**、RMS Force 0.000586 **NO**、Maximum Displacement **0.045584 NO**、RMS Displacement 0.009898 **NO** ⇒ **未收敛**、作业仍 running。

**② 末帧几何（L126100 起的 orientation 块，41 原子）与 P 极小点对比**
| 量 | ts_opt 末帧 | job 1061（频率验证 P） |
|---|---|---|
| R(C2–N4) | **3.4041** | 3.3308 |
| R(C2–O25) | **1.2155** | 1.2172 |
| R(N4–H26) | **1.0210** | 1.0200 |
| R(O25···H26) | **3.1379** | 3.1370 |
| R(O10–H27) | **1.0107** | 1.0112 |
| C9–O10 / C9–O11 | 1.3253 / 1.2118 | 1.3282 / 1.2115 |
| minsep | **0.9679（pair 24–28）** | 0.9689（24–28） |
⇒ 结构**已基本就是产物**（酮 + 脯氨酸 N–H，两片段）。

**③ 能量（同一批 B3LYP/def2SVP(DMSO) 口径，仅作驻点/节点比较，不作 ΔE‡）**
- E(step133) − E(P, 1061) = −939.319785350 + 939.319540184 = **−0.000245166 Ha = −0.154 kcal/mol**（**低于已频率验证的 P 极小点**）；
- E(step133) − E(hemiaminal, 1028) = **−0.007158745 Ha = −4.492 kcal/mol**。

**④ 判读（待终态确认）**
- v7 guess 的 **R(C2–N4) = 2.20 Å 已经位于鞍点的产物侧**：`opt=(TS,calcfc,noeigen)` 从该帧出发沿断裂坐标一路下行，**已进入产物盆地**并低于 P 极小点 ⇒ 若收敛，得到的大概率是**产物侧驻点/极小点**，不是 E3b 的鞍点；届时若 band 表显示 0 虚频或虚模为转子型，即按「无合格鞍点」登记。
- 若终态确认落在产物盆地 ⇒ 需要**新的 guess**（更小的 C2–N4，例如 1.80–1.90 Å；或改走约束扫描）——**属新输入，先报批**，不擅自 ts_resume / 重投 / kill。
- 口径不变：**E3b result = null、barrier 不回填**；虚频只认 band 表 + imaginary 行；模数按 41 原子 3N−6 = 117 判完整；IRC 若截断只写「默认 IRC 参数下路径长度不足、端点身份未建立」。

**②' 判读预告（沿用主协调口径）**
- 若 ts_opt 收敛出的虚模是甲基/芳环转子型 ⇒ **pseudo-saddle**，登记模矢组成为据；
- 若虚模含 **C2–N4 断裂 + N4–H26 相关分量**且方向朝产物 ⇒ 才进入「1 虚频 + 模矢合格」这一档，**仍不是 verified TS**（还缺 IRC 连通性与能垒）；
- 后续 IRC 若在平台默认 maxpoints=10/方向被截断 ⇒ 一律记「**默认 IRC 参数下路径长度不足、端点身份未建立**」，不写「未收敛 / 通道不存在」，不手工补 IRC。
- **E3b result 仍 null、barrier 不回填**；v7 及其报告一律 **post-freeze asset / non-delivery evidence**；交付面（报告 a2964d8d… / 277 行 / 11 文件 sha）未动。

### P.34 停止出帧登记（主协调 18:34:08 CST 裁定；本道只读核对 2026-10-17 18:36:32 CST）

- **指令内容（登记，不解释）**：job 1071 用的是主协调 §R103 ④ **修订前** v8 参数（C2–N4 1.9000 / C2–O25 1.4090 / H26 全在 O25），**不 kill、按 attempt 2 登记**；**1071 终态前不出第三个 guess、不建新 run、不预约算力**；v8.1 待 1071 终态 + 出现空槽 + 主协调裁定后再决定（v8.1 或 (b) 约束扫描兜底）。
- **参数版本口径（此后固定）**：任何构造参数变更一律以主协调转达的 **§R11.54 / §R11.55（及后续 R11.xx）版本号**为准；手上参数与转达版本不一致时**先问再出帧**。
- **本道只读实测（18:36:32 CST）**：`pgrep -cx g16` = **4**，四条进程 = E2EM1/spectator/scan_down_c1c29.gjf（etime 04:50:52）、ts/ts_0019/.../refine.gjf（02:06:43）、E1/split/E1A_constrained_scan_R2692_2192.gjf（13:06）、ts/ts_0020/.../refine.gjf（03:52）⇒ 并发已达上限，free cpus = 0，本道无新提交。
- **job 1071 快照**：`ts/ts_0020/jobs/declaration_0001/ts_opt/refine.log` **1,117 行**，sha256 `c1cd76852accc40becb06157a8588d48d8dbc517c048249508c8e10494973bd0`，`SCF Done` 计数 **1**，无 `Stationary point found` / `Error termination` / `Number of steps exceeded` / `Normal termination` 行 ⇒ **running（非终态）**。
- **job 1069 快照**：`ts/ts_0019/jobs/declaration_0001/ts_opt/refine.log` **129,993 行**，sha256 `7d1a0bef9cf5cc4fa5a3547b0208fe941802f9ceb40dce522a2b48d1c85d7455`，`SCF Done` 计数 **137**，无终态标记行 ⇒ **running（非终态）**。两条均为时间切片 sha，终态须重取。
- **v9 诊断帧处置**：`prep/e3b_guess_formal_v9/E3B_TS_GUESS_v9_c2n4_1.950_midH26.xyz`（sha 32ff714e…）N4–H26 = 3.5374 Å，**不构成真正的 H26 中途帧** ⇒ 不作 evidence_ref、不进正式目录、不外发为交付物；参数确定后重出。
- **不变项**：E3b result = null、barrier 不回填；v7/v8/本帧标 **post-freeze asset / non-delivery evidence**；E3a/ts_0016 不动；交付面（报告 a2964d8d… / 277 行 / 11 文件 sha）未动。

### P.35 接触分类口径（主协调 §R11.56 裁定；登记以免误判）

- **裁定**：ts_0020 guess 的 **C2···H26 = 1.9828 Å 属 1-3 距离**（H26–O25–C2 三元组），非非键碰撞；由 O25–H26 0.9693 Å + O25–C2 1.4090 Å 反算 ∠(H26–O25–C2) ≈ 108–110°（sp³ 氧常规角），1.98 Å 是几何必然。
- **判据不变**：minsep ≥ 0.90 Å、**非键接触（1-4 及更远）≥ 1.20 Å** ⇒ 该帧两项均通过，**不得以 1.98 Å 判其不合格**。v7 帧的 C2···H26 = 1.9744 Å 同属 1-3，性质一致。
- **此后报表格式**：报「最紧接触」时**必须分三类列值**——成键 / 1-3 / 非键（1-4 及更远），并给出判定所依据的类别；否则 reviewer 无法判断是否碰撞。
- **1071 的真正风险（沿用主协调 §R105 ④）**：起点 C2–N4 1.9000 Å（比 v7 的 2.2000 更靠反应物侧）而 H26 全在 O25 ⇒ 断键-成键与质子转移被拆开，calcfc 最低模可能是单向运动；判读口径：0 虚频回 1028 侧 ⇒「纯 C–N 拉伸起点滑回反应物侧，未找到鞍点」；1 虚频含 C2–N4 断裂分量 ⇒ 进「1 虚频 + 模矢合格」档（仍非 verified TS）；转子型 ⇒ pseudo-saddle；失败 ⇒ 报类别 + 行号 + sha，**不写「通道不存在」**。
- **台账对照**：主协调侧记为 §R11.55（sha 7e3658b0… / 1,514 行）与 §R11.56（sha c1408b3d… / 1,521 行）；本道 STATUS.md 为**另一文件**（gold_finish_20261015/HI1/E3/STATUS.md），两者 sha 不可互相引用。

### P.36 归属更正：E3b 交付物发布时机**无**主协调裁定（2026-10-17 18:37:44 CST 收主协调来电后核）

- **更正事实**：我在 §P.34 后的 AgentHub 回复第 4 条写过"交付物欠项按**您**裁定随 E3b 结论一次性给"。主协调（as_ec848a7673b74e35）2026-10-17 明确回复：**该发布时机口径不是其下达的**，其仅能确认这些属车道交付内容、发布时机由主协调（主协调 as_a341823c436e47ed）口径决定 ⇒ **原表述属我的归属错误**，此处撤回。
- **来源核查（只读）**：`grep -rn --include='*.md' -E 'mapped SMILES|model-reduction|no spectator component|reaction_center' PROCESS.md gold_finish_20261015/HI1/E3`（18:37:44 CST 执行）→ 命中的全是 reaction_center / 题源 SMILES 的工作序记录（如本文件 L430、L452、L560、L572、L635、L723、L1196；prep/E3_DECLARATION_DRAFT.md、prep/E3A_BINDING_AND_SYMMETRY_NOTE.md、prep/PROVENANCE_P_e3b_product_seed.md），**没有任何一处**写着"mapped SMILES / model-reduction / no spectator component / 交付时机"；`PROCESS.md` 在本工作区**不存在**（ls 无输出）。⇒ 该交付清单来源是我侧**原始任务指令批（对话内，已被上下文压缩）**，无法逐字回引到编号；**不得**再以"主协调/协调方裁定"名义引用。
- **当前处置**：E3b 交付物（"out" mapped SMILES、reaction_center 双写 1-based 声明 / 0-based 平台、break/form 成对列表、"no spectator component; whole 41-atom system"）**暂不发布**，等主协调（as_a341823c436e47ed）明确口径；此前版本若已外发，以本节为准撤销其"已获裁定"标签。E3b result 仍 null、barrier 不回填、交付面不动。

### P.37 两处表述更正（2026-10-17 18:38:10 CST 实测；覆盖 §P.36 的两句）

- **更正 1（§P.36 的"PROCESS.md 在工作区不存在"错误）**：共享研究记录确实存在，路径为 **`gold_finish_20261015/HI1/PROCESS.md`**，18:38:10 CST 实测 `sha256=e666ab15f1261bbfde9878a41e89c0b0ec99b4e8eed28bc126ac543a1d91f553`、`wc -l=154`、`mtime=Oct 17 16:32`。我在根目录 grep 不到是因为它在 HI1 子目录下 ⇒ **"文件不存在"的表述作废**，此后溯源一律写该全路径 + sha + 行数。`find` 另命中 `research_runs/NU3-open-to-ring-20261015-26734223/diagnosis/final-artifacts/PROCESS.md`（与 HI1 无关）。
- **更正 2（发布时机的性质）**：E3b 交付物的发布时机 = **本道内的工作约定（lane 自定）**，主协调仅**表示认可、不设协调级规则**；§P.36 里"等主协调明确口径"的措辞改为本句含义，避免下一窗口误以为存在必须遵守的协调级口径。做法不变：随 E3b 结论一次性给，不随 null 先行发布。
- **溯源补充（只读）**：`grep -n -E 'mapped SMILES|model-reduction|no spectator|交付|write-owner|写-owner' gold_finish_20261015/HI1/PROCESS.md` 仅命中 **L72**（"E3a：lane2 交付 S2 帧 + provenance 后再排槽…"），**零命中** mapped SMILES / model-reduction / no spectator / write-owner ⇒ 该交付清单在盘上仍无逐字出处，仍按"我侧原始任务指令批（对话内，已压缩，无法逐字回引编号）"登记。

### P.38 主协调放行一件 **普通 opt+freq**（build product seed）；阶段 (a) 自检齐备、等提交口令（2026-10-17 19:24–19:25 CST 实测）

- **授权**（主协调 as_a341823c436e47ed，19:23 CST 来电；并见 19:2x 两条补充验收点/前置清单）：仅允许 **1 件** 作业 = build 的 product seed 起 `opt freq`（**非 TS/IRC**，走普通 `submit_compute_job`），目的是回答「build 的产物 seed 若真从 seed 出发会落到哪个盆地」；ts_0011 取证显示既有 product_opt(1041) 起点是 IRC 外帧（`endpoint_source.json` kind=irc_outer_frame / irc_job_id=1033），**产物种子本身从未被检验**。
- **种子（双方实测一致）**：`ts/ts_0011/build/input_0004/product/seed.xyz`，`sha256=06161a1411edf1e1402620ee13ca448c14d2ac167846c10f1e56bf8ec175078a`、43 行 / 41 原子、注释 `assembled complex candidate 0 (placement 11) rel_energy_kcal=0.0000 min_interfragment_distance=1.6495`、mtime Oct 17 06:42。元素 C15 H21 N1 O4。**注意**：主协调来电里写作 `E3/build/input_0004/product/seed.xyz`，实际在 `ts/ts_0011/build/input_0004/product/`（我 19:24:04 按前者找不到，19:24:17 在后者命中）——路径差异，非文件缺失。该目录下只有 `seed.xyz` / `seed.mol`，**无 prepared_structure.json** ⇒ 无现成 atom_identities。
- **种子接触三类实测**（成键判据 1.3×共价半径和）：成键最紧 O6–H19 **0.9739** / O27–H33 0.9934 / N32–H41 1.0259 / C10–H22 1.0870；**1-3 及更远非键 <1.20 计数 = 0**；minsep 0.9739 ≥ 0.90 ✔。
- **gjf（已建，未提交）**：`gold_finish_20261015/HI1/E3/runs/build_seed_product_optfreq.gjf`，`sha256=7855ef3003c6484eb30311fd44117b415ba37431f7000d9d3024efac3ef13349`、49 行。route（第 3 行，唯一 `#` 行）逐字：`#p opt freq B3LYP/def2SVP empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=dmso)`；`%nproc=8`（第 1 行）、`%mem=10GB`（第 2 行）；`0 1`（0-based 行 6）；坐标块 0-based 行 7–47（41 行），行 48 空行终止；文件以 `\n\n` 结束（`od -c | tail -2` ⇒ `... 3 0 \n \n`）。生成用 qm_input_writer（坐标来自文件、非手写），**仅把 route 行改成主协调给的小写串**（大小写对 G16 无影响），改后逐原子 `max|Δ|=0.000000 Å`（mean 0.000e+00，n=41，不叠合、按同一元素顺序）。
- **六项前置清单**已在 19:25:16 CST 由脚本从 gjf 本体解析并回报（路径/sha/行数、route 逐字、`od` 末行空行、gjf 本体解析原子数 41、`max|Δ|`、`%nproc`/`%mem` 逐字）；**提交需等主协调「可以提交」口令**，未提交、未预约算力。
- **队列（19:24:09 CST）**：running = 1069 / 1071 / 1072，queued 0；free slots 7 / cpus 8 / mem 20480 MB（本件 8 cpus / 10240 MB 恰好占满余量，仍在 ≤4 作业 × 8 cpus 内）。**1049 于 19:17:04 失败终止**（`Error termination via Lnk1e in l9999.exe`，提示含 H2SO4；他人作业，只记录不处理）。
- **同轮主协调给出的两条硬事实（仅记录，不据此改声明）**：① **1071（ts_0020，v8 初版）走声明外路径**——末帧 O10–H27 **1.2016**、H27···N4 **1.245**（羧基质子迁向 N4）、N4–H26 3.7208、O25–H26 0.9767、C2–N4 2.7714、C2–O25 1.2866，E **−939.205768714**，比 1028（−939.312626605）高 **0.106857891 Ha = 67.06 kcal/mol** ⇒ v8 初版不是 C–N 拉伸推进，而是走向 N4 质子化高能区（与 v7 滑进产物盆方向相反）。② **声明步骤位移定义**（两端点实测）：1028 = C2–N4 1.4248 / C2–O25 1.4728 / N4–H26 3.1829 / O25–H26 0.9693 / O10–H27 0.9949 / O25···H27 1.6342；P(1061) = 3.3308 / 1.2172 / 1.0200 / — / — / O25···H27 2.3670 ⇒ 真位移 = **C2–N4 断 + H26 由 O25 迁到 N4 + C2–O25 1.4728→1.2172**，**H27 两端都留在 O10**。attempt 3 任何 guess 必须保持 O10–H27 ≈0.99。
- **验收点（登记，跑完必交）**：117 模 = 39 组×3 且等于 3N−6；虚频只认 band 表负值 + `imaginary` 头行；两处 `Normal termination` 标 opt 内部步 / freq 内部步，电子能量取 **freq 段** `SCF Done`；InChIKey **由 freq 段末帧几何**导出、与 `SMPZMOQIWMNUBG-YBVIJTQESA-N` **同流程同层级**比对（不用 `seed.mol` 键表）；ΔE 只报纯电子差（对 I2 −939.320655479、对 P −939.319540184）并显式标**非 ΔE‡、不作能垒**；结论**只写物种层**三选一（进 P 盆 / 塌回 I2 盆 / 第三盆含几何+能量+模数），**不改** E3a/E3b result=null、不动声明与 process.json。
- **边界**：除该件外零提交；不 kill / 不重投 / 不调 priority / 不 ts_resume / 不碰 ts_0011·ts_0019·ts_0020；产物标 post-freeze asset / non-delivery evidence；交付面（a2964d8d… / 277 行 / 11 文件 sha）、§14、hi.py 不动。
- **待办（映射）**：种子原子序 ≠ E3 工作序（N = **32**、羧基 O–H = **O27–H33**、羟基 O–H = **O6–H19**；E3 工作序 N=4、O25/H26、O10/H27），且无 prepared_structure.json ⇒ 终态报告的三段式几何（C2–N4 / C2–O25 / N4–H26 / O25–H26 / O10–H27）需先做**以 P 帧或 hemiaminal 帧为参照的图匹配映射**，映射表随读数报出并写明匹配依据；不需要额外算力。

### P.39 job 1073 已提交 running + 种子→P 映射完成（2026-10-17 19:25:43 提交；19:32:32–19:32:52 CST 实测）

- **提交（合规窗口）**：主协调 19:25:10 CST 发令，我 **19:25:43** 提交，`submit_compute_job` 返回 **job_id = 1073**（gaussian，local，8 cpus / 10240 MB / priority 0，**非** ts_prepare/ts_resume）。输入 `runs/build_seed_product_optfreq.gjf` sha `7855ef3003c6484eb30311fd44117b415ba37431f7000d9d3024efac3ef13349`（49 行）。主协调 19:26:00 / 协调方 19:25:51 独立读数与我一致：running = 1069 / 1071 / 1072 / 1073，free **cpus 0**、slots 6 ⇒ 第 4 槽、cpus 满额。无第二次提交、无重投 ⇒ 记「合规」。
- **进展快照（19:32:52 CST）**：`runs/build_seed_product_optfreq.log` 4,351 行，sha `6d20d9f31d28e116b8abd52648d1b14ac1ebaec8c6ee2ed7fc7c0fc5da5b05e6`，`SCF Done` 3 次，`Step number 3 out of a maximum of 230`（L3547）⇒ 正常推进，无 Error termination。
- **新纪律（主协调定，本条登记）**：**free cpus = 0 期间不放行任何新提交**；本道如需别的作业只能等 1069/1071/1072/1073 任一终态腾出 8 cpus，并先过主协调口令门槛，**不得自行提交**。
- **映射推导完成（只读，无 QM）**：脚本 `prep/map_seed_to_P_e3b_v4.py`（sha `3b285bd2f2ac713209ab90631450c1d679808c4ed8e0d78917cb79061f5ccc22`），报告 `prep/SEED_TO_P_MAPPING_REPORT.md`（sha `4a6ebce6aeaf138371ef40237037171c02dafcb267488b8bffa9b258d6afd4dc`），机器可读 `prep/seed_to_P_mapping_v4.json`。算法：重原子图**序无关化**（键全 SINGLE）→ RDKit **VF2** `uniquify=False`（**容差 = 无**，精确元素+邻接）→ 氢按唯一重原子母体**全排列穷举**补全 → 逐候选算 Kabsch RMSD、键表逐边一致性、映射 MD5。
  - 重原子同构 **4** 个；可完成 41 原子双射的 **2** 个（iso 0 / iso 2 因母体 H 槽位数不符被排除，属结构差异非舍入）。
  - **iso 3（选用）**：重原子 Kabsch **2.2275 Å**、全原子 **2.5475 Å**、键表不符 6 行但**非芳香不符 0**（6 行全是 seed 的 Kekulé 单/双 ↔ P 的 `AROMATIC` 表示差）、映射 MD5 `954a61340bf368d35f8cfb531169a5f9`。**iso 1**：2.2916 Å / 2.6792 Å / 非芳香不符 0 / MD5 `6f18e28ef9a2cd4f0825cee6575a6f82`。**前二 RMSD 差 = 0.0641 Å < 0.3 Å ⇒ 两候选都列**；选 iso 3 理由 = 化学一致性并列（非芳香不符均 0）+ 两级 RMSD 均更低 + **两候选的 5 个关键键读数逐一相同**（结论对二者不敏感）。
  - **41 行映射全表**已写入报告 §3（双射性与逐位置元素一致性断言通过）；核心身份：seed 2 C ↔ E3 2 C2、seed 3 O ↔ E3 25 O25、seed 32 N ↔ E3 4 N4、seed 41 H ↔ E3 26 H26、seed 27 O ↔ E3 10 O10、seed 33 H ↔ E3 27 H27。
  - **硬判据**：映射后 E3-C2 的邻居 = C1 / C3 / O25（seed 侧 4 / 1 / 3），N4 已不在其配位圈 ⇒ C2 位点对得上。
  - **5 键两列**（seed 侧 | P 侧）：C2–N4 **5.6280 | 3.3308**；C2–O25 **1.2356 | 1.2172**；N4–H26 **1.0259 | 1.0200**；O25–H26 **4.4918 | 3.1370**；O10–H27 **0.9934 | 1.0112** ⇒ **该 seed 在键表层面已偏产物侧**（C–N 已断、H26 已在 N4、O25 为 C2 双键氧、H27 稳在 O10）。若 1073 落回 I2 盆，必须写成「**已产物化种子仍塌回反应物盆**」，不得当普通构象效应；若进 P 盆，也只是「产物型种子留在产物盆」，**不构成反应物侧可达性证据**。
  - **与三条候选假设对照**：N32↔N4 **成立**；O27–H33↔O10–H27 **成立**；**O6–H19↔O25–H26 冲突/不成立**——seed O6–H19 实为**酮醇羟基**（↔ P 的 O28–H24，即 0.9689 Å 那对），真正的 O25 = seed **O3** 且**不带氢**（C2=O3 1.2356 Å），H26 的 seed 身份是 **H41（挂 N32）**。按规则**以图同构为准**并已写明冲突。
- **不变项**：结论文本只写物种层三选一；E3a/E3b result = null、barrier 不回填；不动声明与 process.json；不碰 ts_0011 / ts_0019 / ts_0020 输入；交付面（a2964d8d… / 277 行 / 11 文件 sha、§14、hi.py）不动。

### P.40 scan-first 新规则 + E3b 二维网格扫描设计（只设计，未建输入未提交）— 2026-10-17 19:37–19:38 CST

- **新规则登记**（主协调 19:38 CST，据用户 19:35 指示，LEDGER §R114）：同一对端点 `opt=(TS,calcfc,noeigen)` **连败两次**（落产物盆 / 落非声明反应中心高能区 / pseudo-saddle）⇒ 第三次**不得再猜起点**，改 `opt=modredundant` 受约束弛豫扫描；**正步长 = 递增**且必须同时写「起点→终点」并核对符号（此前有正步长实扫解离侧事故）；只读每点 `Optimization completed.` 后的收敛帧；说明段末空行；ModRedundant 不得与 cartesian/z-matrix 同用；**峰只作 TS 候选/下界，绝不当 ΔE‡**；断键+质子转移耦合步骤用**二维网格**。
- **E3b 设计**（文件 `prep/E3B_SCAN2D_DESIGN.md`，sha `b8a490c3ea652f99f16b679a34d2dd4fedbf01295012d130644078b6b7dc9095`，48 行，标 post-freeze asset）：
  - 起点 = `prep/hemiaminal_1028_lastframe.xyz`（41 原子，1028 末帧）。本轮实测：R(C2–N4) **1.4248**、R(C2–O25) **1.4728**、R(N4–H26) **3.1829**、R(O25–H26) **0.9693**、R(O10–H27) **0.9949**、**R(O25···N4)=2.3213**、R(C2···H26) 2.0398、R(O25···H27) 1.6342。
  - **关键可行性测量**：真实 hemiaminal 的 O25···N4 仅 **2.3213 Å**（非 v8 变形帧的 2.7254）⇒ 固定 O25–H26 = 2.2 Å 时 N4–H26 可行域 **0.121–4.521 Å**，质子可同时落到 N4（≈1.02 在域内），二维网格能表达「断键+质子转移」协同态。
  - 坐标：① `B 2 4` = R(C2–N4) **1.4248 → 2.2248**（+0.2000 × 5）；② `B 25 26` = R(O25–H26) **0.9693 → 2.1693**（+0.3000 × 5）；③ `B 10 27 F` 冻结 R(O10–H27)=0.9949（防 1071 式 N4 质子化：那里 O10–H27 被拉到 1.2016）。
  - 网格 **5×5 = 25** 点，`maxstep=10`；route 计划 `#p opt=(modredundant,maxstep=10) B3LYP/def2SVP empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=dmso)`；q0/m1；`%nproc=8`/`%mem=10GB`；prio 0。生成方式待核准：`qm_input_writer` 从 1028 帧生成 + `end_setting` 三条 ModRedundant；模板 `prep/e3b_scan/hemi_c2n4_scan.gjf`（sha add74ec7…，52 行）。**预计 25 点 / SCF ≤250 / ≈1.5–4 h**（可退 4×4 或 maxstep=6）。
- **HI1_E2 候选起点只读核对（19:37 CST）**：`ts/ts_0009/build/input_0004/reactant/seed.xyz`（43 行/41 原子，sha `c9d59aeab418c248629922ee37d4ea3822c64b7128dd63b3034d3c8c5ec2df3d`，注释 = 「HI1_I1 (S)-Calpha 对映体的 z 镜像；enamine + water + benzaldehyde；job_51 原子序」）；`ts/ts_0009/path/input_0005/provided.xyz`（43 行/41 原子，sha `9e5ccc2fe5dde2e4c1900ad53cc8c1ddbae0e654a618c138adaffa58dd522e38`，注释 = 「HI1_E2 TS guess (S)-proline：ORCA job_58 scan_clean_np8.007 的 z 镜像，d(C3–C6)=2.275 Å」）。**起点选择待主协调指定**，我不擅自选。
- **在跑（19:37:06）**：1071 = 33,209 行 / 33 SCF / Step 32/246；1069 = 178,746 行 / 192 SCF / Step 192/239；1073 = 6,214 行 / 5 SCF / Step 5/230；三者均无终态行。**free cpus = 0 ⇒ 本道零提交**（新规则：free cpus = 0 期间不放行任何新提交）。

### P.41 E3b 网格参数定稿（maxstep=8 / +0.2500）+ E2 起点原子身份判定（2026-10-17 19:38:36–19:41 CST）

- **E3b 设计参数修订并定稿**（主协调 19:41–19:44 CST）：`B 2 4` R(C2–N4) 1.4248 → 2.2248（+0.2000 × 5）；`B 25 26` R(O25–H26) **0.9693 → 2.2193（+0.2500 × 5）**（原 +0.3000 太粗，质子转移段仅 0.25–0.3 Å 宽）；`B 10 27 F` 冻结 O10–H27；**5×5 = 25 格点、maxstep=8，一次定死**；route `#p opt=(modredundant,maxstep=8) B3LYP/def2SVP empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=dmso)`。六条附加条件（H26 最近重原子 ∈{O25,N4} 且 0.95–1.35 Å；O10–H27=0.9949±0.03；前 2 点实算方向、反向停手不 kill；只取 `Optimization completed.` 帧、未收敛单列；**受约束剖面口径 + 峰只作候选/上界 + 无约束 refine 漂移则记「此级别此区域无鞍点」并计入 ≥3 起点失败数**；提交前六项自检与 1028 帧比 max|Δ|=0 且逐字贴三条 ModRedundant）已写入设计文件 §6。设计文件现值 sha `0a1521571e29d8397a9bd5e74a18628585e775b514aa017267a89d93dcf5ae89` / 59 行（原 b8a490c3… / 48 行）。
- **1028 帧核对**：`prep/hemiaminal_1028_lastframe.xyz` 43 行 / 41 原子，sha `be789d5fd013d11ec84b295f4249c61616a8e4de21e129e319c13497faab572d`（与协调方实测同值）。
- **E2 起点（`ts/ts_0009/build/input_0004/reactant/seed.xyz`，sha `c9d59aeab418c248629922ee37d4ea3822c64b7128dd63b3034d3c8c5ec2df3d`）实测**：**3 片段 24 / 3 / 14** = 烯胺（原子 1–24）+ 水（25 O、26 H、27 H）+ 苯甲醛（28–41）；`provided.xyz`（sha 9e5ccc2f…）同构 3 片段。minsep seed 0.9739（O25–H26 成键 O–H）、provided 0.9731。
  - **原子身份（化学判定，非最近距离）**：苯甲醛**醛碳 = 原子 29**（邻居 O28 双键、C30 芳环 ipso、H36）；烯胺 C1=C2（DOUBLE）、C2–C3（SINGLE）、C2–N4（SINGLE），H 数 原子1=2H、原子2=0H、原子3=3H ⇒ **原子 2 = α-碳（连 N）**，**原子 1 = β-碳（端基 =CH₂）= 亲核碳**。
  - ⇒ **E2 成键坐标 = `B 1 29`**，起点 **d(C1···C29) = 4.3543 Å**（seed）；在 `provided.xyz` 同一对为 **2.2750 Å**，与该文件注释 "d(C3-C6)=2.275 A"（ORCA job_58 序号）**逐位吻合** ⇒ 身份判定与历史 TS guess 是同一成键对。
  - **一处更正**：协调方引用的「跨片段最近 C···C = C1···C35 3.6818 Å」数值我复算相同，但 **C35 是芳环 CH，不是醛碳**；跨片段最近**重原子接触**是 **O28···H24(羧基 OH) = 1.6817 Å**（氢键）。"最近 C···C"≠成键对。
  - **CIP**：RDKit（seed xyz 几何 → `rdDetermineBonds.DetermineBonds(charge=0)` → `AssignStereochemistryFrom3D`）**唯一立构中心 = 原子 8 = S**；原子 8 邻居 C7（羧基碳）/N4/C9（环）/H23 ⇒ 脯氨酸 Cα，与 HI1_E2 声明的 (S) 一致。
- **E2 一维扫描设计（只设计）**：`B 1 29` 4.3543 → 1.5543 Å（**−0.2000 × 14**，负号=递减），14 点，maxstep=8，水作旁观不冻结、监测 O28···H24 与 O25···C29；≈≤112 SCF / 40–110 min；峰只作候选/上界。**次优先于 E3b，未生成输入、未提交。**
- **资源**：free cpus = 0（1069/1071/1072/1073）⇒ 零提交；终态腾槽后先报主协调 + 协调方拿口令。

### P.42 E2 设计文件落盘 + 双方判读口径对齐（2026-10-17 19:40:23 CST 实测状态）
- **协调方独立复核通过**（19:44 CST 来电）：原子 29 = 醛碳（O28 DOUBLE、C30 芳环 ipso、H36；C=O 1.2265 Å）、原子 1 = 烯胺端基 =CH₂（邻居 C2 DOUBLE、H12、H13）、原子 2 = α-C（C1 DOUBLE / C3 / N4）、**d(C1···C29)=4.3543**、d(C1···C35)=3.6818 但 **C35 为芳环 CH（邻居 C34/C30 芳香、H41）**⇒ 我对"C1···C35 交叉核对"的更正**成立**（对方明示责任在彼侧）、d(O28···H24)=1.6817 氢键、**原子 8 CIP = S**（脯氨酸 Cα）与 HI1_E2 声明一致；整体 SMILES `C=C(C)N1CCC[C@H]1C(=O)O.O.O=Cc1ccccc1` = 三组分。
- **E2 设计文件已落盘**：`prep/E2_1D_SCAN_DESIGN.md` sha `779bd92ffdfa9d90706511c09669809cf136c70d1f301d0438f9d34875c2e211`（标 post-freeze asset）：`B 1 29`，**4.3543 → 1.5543 Å**，**−0.2000 × 14（负号 = 递减，写死）**，14 点，maxstep=8，**无额外冻结**（水不冻结），route 同 E3b 但 `B 1 29 S 14 -0.2000`；预计 ≤112 SCF / 40–110 min。
- **E2 四条判读要求已接受并写入设计文件 §4**：逐点报 R(1,29) / R(29,28) C=O / R(28···H24) / R(2,4) / R(25···29) / R(25···1) / minsep（分类）/ E；停手标注三条件：① R(2,4) 相对起点变化 >0.05 Å ⇒ 标该点；② R(28···H24) <1.20 Å（质子转移，非本坐标结果）⇒ 标该点单列；③ 前 2 点实算 R(1,29) 方向非递减 ⇒ 停手报、不 kill。单调无峰 ⇒ 记「该级别下一维 C–C 成键坐标无峰」，改二维/换起点需放行。
- **在跑快照（19:40:23 CST）**：1069 = 180,450 行 / 194 SCF / **Step 193/239**；1071 = 35,029 行 / 34 SCF / **Step 34/246**；1073 = 7,366 行 / 7 SCF / **Step 7/230**；三者均无终态行；`pgrep -cx g16 = 4`。**free cpus = 0 ⇒ 零提交、零待提交输入生成**（E3b / E2 两份设计都只到设计层）。

### P.43 E2 质子转移判据改严（两档，主协调 19:40:28 / 19:40:46 CST）
- **取代**原一条「R(28···H24) < 1.20 Å ⇒ 标质子转移」。**新两档**：
  - 档 1：**R(28···H24) ∈ [1.20, 1.50] Å ⇒ 「氢键强化 / 共享质子」**，**该点仍进剖面，但表内必须标注档位**（≠ 物种改变；理由：起点 R(28···H24)=1.6817、成键 O–H≈0.97–1.0，1.2 Å 附近常只是强氢键）。
  - 档 2：**R(28···H24) < 1.20 Å *且* R(O28–H24) ≤ 1.05 Å ⇒ 「质子已转移（物种改变）」**，**单列、不进剖面**，并注明该转移不是本一维 C–C 坐标的结果。
  - 每点**同时报 R(28···H24) 与 R(O28–H24) 实测值**，不只报档位。
- **文件现值**：`prep/E2_1D_SCAN_DESIGN.md` sha **`c25e0d82d42cb91063fb3ea96119caf79d8a9e6af26eb1fd24437dff69f47ec0`** / **52 行**（改严前 779bd92f… / 49 行 → 首轮改严 41f2dac0… / 52 行 → 本轮补「档 1 仍进剖面」）。
- **主协调独立复核（19:40:46 CST）**：E2 设计 779bd92f…/49 行、E3b 设计 0a152157…/59 行、本台账 f119c590…/1,352 行 三项 sha 与其自读一致；LEDGER.md 现值 `fe442ff16e0aa83b8f805ad1a4f93ff52dc21b42b821f22a82077aaa80d3b922` / 2,159 行（§R116 起 L2122）。
- **§P.43 再修订（协调方 19:41 CST 第二次提醒）**：档 1（[1.20,1.50] Å）改为 **单列、不进主剖面**，表内仍照常报全部数值（R(28···H24)、R(O28–H24)、R(1,29)、E、SCF 行号、minsep），并**另给「含档 1 点」的参照剖面**；档 2（<1.20 Å 且 O28–H24 ≤1.05 Å）单列、不进主剖面。**主剖面峰只归因于 C–C 坐标；若峰只在参照剖面出现，该点不得作 TS 候选，只能记「需二维扫描」并报主协调。** `prep/E2_1D_SCAN_DESIGN.md` 现值 sha **61e4e9e1085f273a0b619bdd7dd88f40a8843199edeb14c890e15e2675998629** / **53 行**（协调方先前登记的 c25e0d82…/52 已被本版取代；演进链 779bd92f…/49 → 41f2dac0…/52 → c25e0d82…/52 → 26d3fcbb…/52 → 现值）。

### P.44 E2 判据冻结（主协调 19:42:5x CST）+ 两张表按内容命名
- **冻结**：`prep/E2_1D_SCAN_DESIGN.md` **61e4e9e1… / 53 行** 予以接受，判定为**不再改文字**；执行侧不得自行改本判据，确需变更由主协调发新条目。主协调自认本轮 5 个版本的根因是其 19:40:28 旧话与 19:41 自我更正并存、协调方按旧话转达（责任在主协调侧）。
- **唯一落地要求（取代「主 / 参照」命名）**：报告里两张表一律**按内容命名**——「**含档 1 点（共享质子）**」与「**排除档 1 点**」，各标点数；正文不得只用「主剖面」指代其一而不写清是否含档 1 点。峰结论必须写明「**两视图下峰位置/峰高是否改变、最终采用哪一视图、为什么**」；峰只在「含档 1 点」视图出现且落于档 1 区间 ⇒ **不得作 TS 候选**，只记「需双向/二维扫描」。
### P.45 只读快照（2026-10-17 19:46:31 CST，本道独立实测；四作业均未终态）
- **PROCESS.md 现值已推进**：`gold_finish_20261015/HI1/PROCESS.md` = `faf96d0b7a7f9079165180f3bbbc92eaa3be6889ba3bc24cc40ecf3389177aa6` / **331 行**（本道实测，与主协调追记后值一致）。**「以 318 行为现值」作废**：154（我 18:38:10）→ 318（19:43:11）→ 320（协调方改前）→ **331（现值）**，各次读数在各自时刻均真实，增量来自协调方逐次追记；下一窗口按 **331 行** 对账。
- **四作业实测（19:46:31 CST，均为活日志时间切片）**，`pgrep -cx g16 = 4` ⇒ **free cpus = 0**：
  | 作业 | 行数 | 日志 sha（切片） | SCF | 末次 SCF（行号 / 值） | Stationary | Normal term | Freq 组 | 步 |
  |---|---|---|---|---|---|---|---|---|
  | 1069 ts_0019 ts_opt | 184,969 | `cb529f19b8e96100457a5c32fd2f22147e0e916877a19280c23ffc0889c1ff4a` | 198 | L184055 `-939.320034191`（9 cycles） | 0 | 0 | 0 | **Step 198/239** |
  | 1071 ts_0020 ts_opt | 38,843 | `fdf811e5e54ee726afea740c6cc7f26f88be62fa136ea8b618e29ead675c8743` | 38 | L38009 `-939.247697664`（11 cycles） | 0 | 0 | 0 | **Step 38/246** |
  | 1072 E1a 负步长扫描 | 44,738 | `49db4db71fe87c2ef5a76c737065775027abb57fc1ed4af24e470758dfe6e882` | 63 | L44127 `-593.929757547`（13 cycles） | **4** | 0 | 0 | Step 8/150，**scan point 5/11** |
  | 1073 product-seed opt+freq | 10,945 | `120c7eca931b21210e3eeb6c7f30b492af424f60599162fca0edd032148a2e55` | 11 | L10933 `-939.315911783`（10 cycles） | 0 | 0 | **0** | **Step 10/230** |
- **1069 能量关系（本道自算，纯电子差、非能垒）**：`-939.320034191` 比频率验证 P（job 1061，`-939.319540184`）低 **0.000494007 Ha = 0.310 kcal/mol** ⇒ 仍沿产物盆下行，与 v7 起点滑入产物盆一致；终态类别待终态行确认，**不预写**。
- **1072 口径**：`Stationary point found` 4 次 = 前 4 个扫描点收敛；点 5 进行中（`Maximum Force 0.000612 > 0.000450 NO`）⇒ 逐点表待终态，**不内插、不引用未收敛点**（沿用 §R109）。
- **1073**：`Frequencies --` 计数 0 ⇒ opt 段未完成、freq 段未起，117 模 / 虚频判读**待终态**。
- 边界不变：E3b `0a152157…`/59、E2 `61e4e9e1…`/53 零生成零提交；四条边 result/barrier 全 null；交付面 a2964d8d…/277 行/11 文件 sha、§14、hi.py 未动；零 kill / 重投 / priority 变更 / ts_resume。
### P.46 轮询超时后的再挂与快照（2026-10-17 20:23:00 CST，四作业仍无终态）
- **本轮唤醒原因**：`check_timeout`（1069 的 2 h 轮询到期未命中终态标记），**不是**作业异常；"未命中"只说明轮询窗口太短，不构成任何科学结论。
- **1069（ts_0019 ts_opt）实测**：210,674 行、sha `b14ed9e510918987dec53a33e936b4f4c65c21595adac33ad74fd1ef8d1543a2`、SCF **226**、**Step 226/239**、末两次 SCF = L208876 `-939.320099742`（9 cycles）、L209796 `-939.320106414`（9 cycles）、`Stationary point found` **0**、`Normal termination` **0**、无 `Error termination` / `Number of steps exceeded` ⇒ **仍 running**，已逼近 239 步上限，预期以步数上限收场（类别待终态行确认，**不预写**）。
- **1071（ts_0020）实测**：60,169 行、SCF **60**、无终态行 ⇒ running；**1073（product-seed opt+freq）**：33,307 行、SCF **34**、无 `Normal termination`/`Frequencies --` ⇒ opt 段仍在跑。`pgrep -cx g16 = 4` ⇒ free cpus = 0。
- **监测再挂**：已重建 1069 终态轮询（每 120 s、上限 40 min，命中 `Stationary point found|Error termination|Number of steps exceeded|Normal termination` 即醒），醒后按「定稿三件套 → ts_inspect(ts_0019) → 频段表 39×3=117 断言与虚频判读 → 与 1061/1028 纯电子差（标非 ΔE‡）→ 四类事件上报 → append 台账」执行。
- 纪律：未终态 ⇒ 不提交、不 ts_resume、不 kill、不改 priority；E3b result 仍 null、barrier 不回填。
### P.47 E3b 二维网格扫描已提交（job 1074，20:28:54 CST 起）+ 六项自检与约束识别实录
- **放行**：主协调 20:27:51 CST 实测 1072 done、free cpus 8 ⇒ 放行第 4 槽（E2 继续排队）。协调方 20:29:01 CST 独立复核六项通过、批准提交。
- **输入**：`gold_finish_20261015/HI1/E3/runs/e3b_scan2d_c2n4_o25h26.gjf`，**54 行**，sha **`f41e1d6244e891eb63b6b50fb58826c198eab813ed96bb16a255b31ac7d2e259`**（双方一致）。route 第 3 行逐字 `#p opt=(modredundant,maxstep=8) B3LYP/def2SVP empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=dmso)`（协调方笔误 dmoso 已按 dmso 执行）；`%nproc=8` / `%mem=10GB`；q0/m1；坐标块后空行 + 三条 B 行 `B 2 4 S 5 0.2000` / `B 25 26 S 5 0.2500` / `B 10 27 F`；文件末尾 `\n\n`。
- **六项自检结果**：gjf 本体解析 **41 原子**（`0 1` 后到首个空行，坐标块在 0-based 行 48 终止）；与 1028 帧（`be789d5f…`，本轮再核）逐原子 **max|Δ| = 0.000000 Å**（不叠合、元素序一致、n=41）；`od -c` 末 `… F \n \n`。
- **工具缺口留痕（协调方要求写进报告）**：`qm_input_writer` **无法在一次调用里同时声明 opt 任务与带 `S` 的扫描行**——`end_setting` 含 `B … S …` 时其内部任务分类判为 `relaxed_scan`，与请求的 `minimum_opt` 冲突并**拒绝写文件**（返回 `qm_input_writer internal mismatch`）。且 `end_setting` 会把 B 行**紧贴最后一条坐标行**写入（无空行），Gaussian 会把 `B 10 27 F` 当坐标行。故采用两步：① writer 生成（含冻结行 `B 10 27 F`）→ ② `edit` 插入一个空行、补两条 `S` 行、并把 route 关键字改为冻结版小写串。**坐标零改动**（max|Δ| 复验 0.000000 Å、元素序一致）。
- **提交**：**job 1074**，普通 `submit_compute_job`（非 ts_prepare/ts_resume），gaussian，local，8 cpus / 10240 MB / priority 0，`started_at 2026-10-17T20:28:54+08:00`；20:29:05 CST 日志已在写。槽位：running = 1069/1071/1073/**1074**，`free = slots 6 / cpus 0 / mem 10240`，`pgrep -cx g16 = 4`（1072 已 done）。
- **Gaussian 已识别全部三条约束（日志原文行号，强于自检）**：L85 route 回显；L157 `The following ModRedundant input section has been read:`；L160 `B      10      27 F`；**L235** `R6 R(2,4) 1.4248 Scan`；**L255** `R26 R(10,27) 0.9949 Frozen`；**L257** `R28 R(25,26) 0.9693 Scan` ⇒ 两扫描 + 一冻结均生效，起点值与设计逐位一致（1.4248 / 0.9693 / 0.9949），**不存在约束被静默忽略**。
- **接下来纪律**：前 2 格点后从日志几何实算两坐标方向（须递增，反向立停报、不 kill）；每点 H26 最近重原子 ∈{O25,N4} 且 0.95–1.35 Å（否则单列「悬空/非声明受体」）、R(O10–H27)=0.9949±0.03（越界标点不静默改）、只取 `Optimization completed` 帧、未收敛点单列（step 数 / 撞 maxstep=8）；峰只作候选/上界、不写 ΔE‡；报告须写「受约束剖面（O10–H27 冻结）」原句。
- **背景参考（不改本道口径）**：E1a（1072）11 点全收敛、两支各自单调无内部极大、两支间 Kabsch 0.985 Å 属通道切换 ⇒ 纯 C–N 拉伸非该步反应坐标（主协调 LEDGER §R122）；这提示单坐标拉伸易换通道，故 1074 每点的 H26 归属判据是关键。
- 不变项：E3b result 仍 null、barrier 不回填；v7/v8 与两份扫描设计均 post-freeze asset；E3a/ts_0016 不动；交付面 a2964d8d…/277 行/11 文件 sha、§14、hi.py 未动。
### P.48 主协调 20:30 CST 补充口径（1074 第 2 格点报数规则 / 1069 终态报法 / E2 排队）
- 分工：本道两条 180 s 监测（1074 进第 2 格点、1069 终态）与主协调 300 s 四日志轮询并行、不重叠；谁先拿到读数谁先报，但落笔前同轮 query_compute_queue 复测并写实测时刻。
- 1074 第 2 格点：先报数再做判断——①实算 R(2,4) 与 R(25,26)（须分别 > 1.4248、> 0.9693；反向或几乎不动 ⇒ 立停报、不 kill）；②报该点 H26 最近重原子与距离、R(O10–H27)。并须写清「是哪一维在动」：二维扫描按 Gaussian 惯例为「外层坐标 2 逐点、内层坐标 1 循环」，第 2 格点可能只动了一个坐标，不得把「另一维暂时不变」误判为反向。
- 1069 终态：四档登记、先报主协调再落台账；若终态为 Optimization stopped. / NStep= ，逐字贴出该两行（含行号）；若出现 Stationary point found 而无 freq 信息，登记「优化收敛但未做 freq ⇒ 非驻点判定」，并等主协调口令再决定是否 freq。明确「不自续算、不 ts_resume、不 kill」。
- E2 一维：继续排队，必须主协调点名放行；即使 1069 先腾出空槽也不得自行提交。
- 监测更新：为把上述口径带入唤醒时刻，已重建 1074 第 2 格点监测（含「哪一维在动」与「先报数后判断」）；旧的同目标提醒视为被取代，任一触发后清理其余。
- 边界不变：四条边 result 与 barrier 全 null；交付面 a2964d8d…/277 行/11 文件 sha、§14、hi.py 未动；零 kill / 重投 / priority 变更 / ts_resume。主协调 LEDGER 现值 62c94124…/2,279 行（§R123）。
- **§P.48 补一句（主协调 20:30 CST）**：1074 第 2 格点报数时，除 R(2,4)/R(25,26)/H26 归属/R(O10–H27) 外，**同日再报「scan point N of 25」+ 该点是否 Optimization completed + 距上一格点的 Kabsch RMSD**。理由：本体系单坐标扫描已出现过一次通道切换（E1a 的 sp4→sp5，Kabsch RMSD 0.985 Å），二维网格同样需用 RMSD 监控换通道；**RMSD > 0.3 Å 即标「通道切换」但不 kill**。
- 台账交叉引用：本道 STATUS `7544cbdc…` / 1,406 行（本次追加后见下）；主协调 LEDGER.md `62c9412413504d2fa1c55c7c7cf9cc8627bc1dd5e497801b209a4aaf6c0418d3` / 2,279 行（§R123）。

### P.49 提交授权事实核对（协调方 20:30 CST 提出「未收到口令」）
- 事实：主协调 as_a341823c436e47ed 于 2026-10-17 20:27:51 CST 发来电文《空闲槽已出现：放行 E3b 二维网格扫描提交（E2 仍排队）》，含「1072 = done（20:26:25 Normal termination）；20:27:51 实测 running = 1069 / 1071 / 1073，free = slots 7 / cpus 8 / mem 20480，queued 0 ⇒ 第 4 槽可用」与「放行内容与条件（按冻结版设计执行）」，并列起点帧、三条 ModRedundant、5x5 / maxstep=8、route 逐字（并自纠 dmoso→dmso 笔误）、六项自检与提交纪律。
- 执行时序：六项自检 20:28:42 CST 完成并先发 post（evt_90d3e609923f4658）→ 20:28:54 CST 提交（job 1074）→ 20:29:05–20:29:12 回执（evt_60e7f83cc0ac42ce / evt_b760b7fc71ef46de）。两次独立复核对输入 sha f41e1d62… / 54 行、max|Δ|=0、三条 ModRedundant 原文一致。
- 结论：本道提交有主协调口令（20:27:51 CST，先于提交 63 秒），不属无口令抢跑；协调方 20:10:19 那条是更早预告、不含口令。责任归属与追认由主协调裁定。
- 当前纪律：不再追加任何提交（E2 一维仍排队、须主协调点名）；1074 不 kill、不重投、不改 priority。
- 主协调 20:31:05 CST 裁定：**1074 授权在先、不属抢跑**（口令 20:27:51 / 提交 20:28:54，间隔 63 s），责任与追认由主协调。

### P.50 网格规模更正：36 格点（不是 25）+ 1074 第 1 点已收敛（2026-10-17 20:32:02 CST 实测）
- 设计错误归属主协调：Gaussian 的 S 5 = 「每维 5 步 ⇒ 6 个取值」⇒ 实为 **6 × 6 = 36 格点**；设计文件写 5x5=25 有误。本道实测证据：日志 L1638「Step number 1 out of a maximum of 243 on scan point 1 out of 36」、L1939「-- Stationary point found.」。
- 处置：**不改规模、不重投**，按 36 点跑完并按 36 点出表；报告写「36 格点（S 5 = 6 取值/维）」。设计文件保持冻结不编辑（错记在案，以主协调口径取代）。
- L1939 的 Stationary point found 是 **scan point 1 的格点内收敛**：同段四项判据 Maximum Force 0.000007 / RMS Force 0.000001 / Max Disp 0.001011 / RMS Disp 0.000163 全 YES、Predicted change in Energy = -2.865807D-09、Optimization completed. ⇒ 出表按「格点内收敛」记，**不得**写成「找到驻点/鞍点」。
- 判读纪律照旧：每点报 scan point N of 36 + 是否 Optimization completed + 与上一格点 Kabsch RMSD（>0.3 Å 标通道切换、不 kill）+ H26 最近重原子与距离（须 O25 或 N4、0.95–1.35 Å）+ R(O10–H27)=0.9949±0.03，并写明哪一维在动；峰只作候选/上界、不写 ΔE‡；报告原句写「受约束剖面，O10–H27 冻结」。
- 同轮只读：1069 = 217,173 行 / Step 233/239 / Normal|Error|NStep 计数 0 ⇒ 仍 running（终态仍先报主协调）。E2 一维继续排队。

### P.51 1074 第 2 格点到场：方向自检通过（只报数，未做化学结论）— 2026-10-17 20:35:47 CST
- 日志：`gold_finish_20261015/HI1/E3/runs/e3b_scan2d_c2n4_o25h26.log` 4,747+ 行（20:35:30 快照 4,686 行 / sha `522fdec47a0158824ee2752c9ca6b7f9347caf13d2089a29c0a94bba9a7f96a4`，20:35:47 已推进到 L4,747）；`Optimization completed` 计数 **1**（仅第 1 格点）；末条 `Step number 3 out of a maximum of 243 on scan point 2 out of 36`（L4747）。
- **格点 1（已收敛，L1938 Optimization completed. + L1939 Stationary point found，四项判据全 YES）**：R(2,4)=**1.4248**、R(25,26)=**0.9693**、R(2,25)=1.4728、R(4,26)=3.1829、R(2,26)=2.0398、R(10,27)=**0.9949**；H26 最近重原子 = **O25，0.9693 Å**（∈0.95–1.35 ✔）。
- **格点 2（进行中，Step 3）**：R(2,4)=**1.6248**（= 1.4248 + 0.2000，**递增 ✔**）、R(25,26)=**0.9693**（**尚未变动**）、R(2,25)=1.4202、R(4,26)=3.2616、R(2,26)=1.9757、R(10,27)=**0.9949**（冻结键零漂移 ✔）；H26 最近重原子 = **O25，0.9693 Å** ✔。
- **哪一维在动（主协调要求写清）**：**坐标 1（C2–N4）在动**（1.4248→1.6248）；**坐标 2（O25–H26）暂时不动**（0.9693）——符合 Gaussian 逐点推进习惯，**不判为反向**。
- **Kabsch RMSD（最优叠合、全 41 原子）最近收敛格点 vs 当前 = 0.1224 Å < 0.3 Å** ⇒ 暂**无通道切换**迹象。
- 能量（纯电子，不作任何能垒）：L2753 −939.292816630、L3712 −939.294943689、L4659 −939.296727554（当前格点）。
- 结论状态：方向自检**通过**、H26 归属与冻结键均合规；**不做化学结论、峰/能垒均未判定**（E3b result 仍 null、barrier 不回填）。

### P.52 attempt 1（job 1069 / ts_0019，v7 起点）终态：步数上限终止（2026-10-17 20:39:21–20:39:40 CST 实测）
- **终态三件套**：223,328 行；sha `f09d1e99e239db287f2a612fd6d0a85ed46ef4cd78bc52915ddfa926be93d130`；`Error termination via Lnk1e in /home/ly/g16/l9999.exe at Sat Oct 17 20:38:52 2026`。
- **逐字终态行**：L222267 `Optimization stopped.`；L222268 `   -- Number of steps exceeded,  NStep= 239`；L222269 `   -- Flag reset to prevent archiving.`；L223324 `Error termination request processed by link 9999.`；L223325 `Error termination via Lnk1e in /home/ly/g16/l9999.exe at Sat Oct 17 20:38:52 2026.`
- **步数与能量**：`Step number 239 out of a maximum of 239`；末次 SCF **L221880 `-939.320189491`**（10 cycles）。
- **末收敛表（L222261 四项）**：Max Force 0.005423（NO）、RMS Force 0.000527（NO）、Max Displacement 0.075011（NO）、RMS Displacement 0.019257（NO）；Predicted change in Energy = -1.515987D-05 ⇒ **四项全 NO**。
- **末几何（最后 Input orientation，L222512）**：R(C2–N4)=**3.2912**、R(C2–O25)=**1.2156**、R(N4–H26)=**1.0216**、R(O25–H26)=**2.9640**、R(O10–H27)=1.0118、C9–O10 1.3259、C9–O11 1.2117 ⇒ **产物型（产物盆）几何**（与频率验证 P（1061）3.3308 / 1.2172 / 1.0200 / 3.1370 / 1.0112 同型）。
- **能量对照（纯电子差、非 ΔE‡、不作能垒）**：末次 SCF 比 job 1061 的 `-939.319540184` 低 **0.000649307 Ha = 0.4075 kcal/mol**；两者几何不同，仅作「沿产物盆下行」的指示，不做能垒。
- **无频率信息**：`Stationary point found` 计数 **0**、`Frequencies --` 组数 **0** ⇒ **不存在虚频判据**，不得写「0 虚频/转子型」等频段结论。
- **四档登记（结论）**：属「**优化未收敛（步数上限 239）**」一档 ⇒ 记「**本次 attempts 范围内未找到合格鞍点（attempt 1，v7 起点；无驻点、无频率）**」；**不写「通道不存在」**，不把该几何/能量当鞍点或能垒证据。
- **ts_inspect(ts_0019)**：revision 14、stage refine、**status blocked**、result null、waiting_for [] ⇒ 管线**未自动起 frequency**；本道**不 ts_resume、不重投、不 kill**，等主协调裁定（新起点 / 二维网格结果）。
- **§P.52 交叉核对（协调方 20:39:53 CST 同刻实测）**：三件套 223,328 行 / sha `f09d1e99…`、SCF 239、末次 L221880 −939.320189491、Step 239/239、逐字终态行与判定一致；末帧他侧引 L222765、本道脚本引最后一个 `Input orientation` 头 L222512（同一末步的相邻块，几何数值逐项相同：C2–N4 3.2912 / C2–O25 1.2156 / N4–H26 1.0216 / O25–H26 2.9640 / O10–H27 1.0118），**无实质分歧**；平台 state = failed（ended 20:39:09）。
- **门控更新（协调方 20:39:22 CST 实测）**：free cpus = **8**（slots 7 / mem 20480），running = 1071 / 1073 / 1074；**E2 一维由 as_44ac48fc347d4099 按主协调点名提交**，不进本道提交；本道提交额度仍为 0。
- **后续职责（协调方指定）**：① 1074 逐格点报数（36 格点、每点 OPT completed、Kabsch、H26 归属、O10–H27、哪一维在动）；② 1073 等 freq 段**第二个 Normal termination** 后按交付清单判读（117 模 = 39 组 ×3、虚频只认 band 表负值 + imaginary 头行、0 虚频且最低实模 <20 cm⁻¹ 单独标、InChIKey 两次分列、ΔE 纯电子差标非 ΔE‡、几何三段式、物种层三选一）。

### P.53 1069 末帧构象对照（协调方实测）+ 参照锁定 + 触发点（20:39:59–20:41:00 CST）
- **末帧块差异定案**：本道引 L222512（Input orientation）、协调方引 L222765（Standard orientation），属**同一步相邻块**，几何逐项相同 ⇒ 记录为「同一步相邻块」，不算冲突。
- **新事实（协调方脚本实测，本道未复算，标为他人实测）**：1069 末帧**重原子（20 个非 H）Kabsch** 叠合 vs P（job 1061）**RMSD = 1.5464 Å**、单原子最大 **2.9160 Å**；vs 1028（hemiaminal）RMSD = **1.5372 Å**。反应中心三量同型（C2–N4 3.2912 / C2–O25 1.2156 / N4–H26 1.0216），但**整体构象不同**，且比 job 1061 的 P 低 0.000649307 Ha（0.4075 kcal/mol，纯电子）。
- **旁注（20:42:15 CST 加入 → 20:43:41 CST 关闭，上文原文保留）**：**已解决**——四元数版 Kabsch 经合成自检证伪（「已知旋转+平移」例给 **1.6585**（应为 0）、镜像例 2.0515、副本例 0.00000000；同一数据换 numpy SVD 得 0.00000000 / 0.9306 / 0），**3.1165 / 2.6549 及 3.05–4.81 敏感性表作废**；**SVD 口径复现 1.5464 / 1.5372（重原子 20、禁镜像，det = +1.00）**，采用后者。
- **归因事实澄清（本道自证，供下一窗口核对）**：**3.1165 / 2.6549 不是本道产出**——本道脚本 `prep/scan2d_pointcheck.py` 用 numpy SVD Kabsch、`prep/final_1069_geom.py` 只算距离，二者均未产生该数值；故「写-owner 复算作废」的表述本道**不认领**，仅记录「该数值出自四元数实现、已被证伪」。
- **SVD 口径可引用数值（协调方 20:44:59 CST 复算，本道未复算）**：1069（L222765）vs P（P_optfreq.log L68977，sha `183590c1…`）**重原子 20 RMSD 1.5464 / max 2.9160（最大位移原子 11）**、全原子 41 **1.7344 / 3.4550**；vs 1028 **重原子 1.5372 / 2.7050**、全原子 **1.8873 / 3.4401**；P vs 1028 1.1574 / 2.4930；det 全 +1.00（禁镜像）。E1a 11 点序列（SVD 版）= 0.030 / 0.051 / 0.035 / 0.759 / 0.029 / 0.024 / 0.022 / 0.023 / 0.025 / 0.024（与先前逐项相同，E1a 不受影响）。
- **引用规则（现生效）**：① 定性结论可引用——**1069 末帧整体构象既不是 P 的构象也不是 1028 的构象**；② 具体 RMSD **恢复可引用，必须写「SVD 口径 + 重原子 20 / 全原子 41 + 禁止镜像（det=+1）」**；③ 主协调两条裁定不依赖该数字、照常生效：**P（job 1061）只是某一个频率验证过的产物极小、不必然是最低构象**；后续以产物端为参照的能垒必须显式声明「参照 = job 1061 的 P」，不得换参照或混用。
- **E2 提交方更正**：job 1075 由 **as_f59e78f07a0e4d07**（协调方 20:42:15 CST 口径；此前一条记为 as_44ac48fc347d4099，两者均为他人 lane、本道不提交，按最新口径记 as_f59e78f07a0e4d07 并保留旧记）；20:39:25 提交 / started_at 20:39:26 / 8 cpus / 10240 MB / prio 0 / 日志 `gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan.log`；20:40:12 起 running = 1071 / 1073 / 1074 / **1075**。
- **参照锁定（写进本道判读清单第 3 条）**：**P（job 1061）只是「某一个」频率验证过的产物极小，不必然是该物种最低构象**；后续任何以产物端为参照的能垒必须**显式声明「参照 = job 1061 的 P」**，不得换成更低构象，也不得在两个参照间混用（E3b 最终裁定的关键约束）。
- **E2 已由他人起跑（非本道提交）**：lane 门控后 **20:39:25 提交、job 1075、started_at 20:39:26、8 cpus / 10240 MB / prio 0**，日志 `gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan.log`；**本道提交额度仍为 0**。
- **触发点（只报这三类，其余只读静默）**：① 1074 出现能量峰（按 **6×6 行列**出表：行 = R(2,4) 六取值、列 = R(25,26) 六取值；**前 6 点只覆盖断键维，质子维自第 7 点起展开**）或连续 3 个格点 Kabsch RMSD > 0.3 Å；② **1071 终态**（四档）；③ **1073 进 freq 段且出现第二个 Normal termination**（117 模 = 39 组、虚频只认 band 表负值 + imaginary 头行、0 虚频且最低实模 <20 cm⁻¹ 单独标）。
- 不变项：E3b result 仍 null、barrier 不回填；v7/v8 与两份扫描设计均 post-freeze asset；E3a/ts_0016 不动；交付面 a2964d8d…/277 行/11 文件 sha、§14、hi.py 未动。
- 边界不变：四条边 result 与 barrier 全 null；交付面 a2964d8d…/277 行/11 文件 sha、§14、hi.py 未动；零 kill / 重投 / priority 变更 / ts_resume。
- **台账实测（2026-10-17 19:43:11 CST，本轮 `sha256sum` + `wc -l` 实读）**：`gold_finish_20261015/HI1/PROCESS.md` = **`bd85474dd736ecb4e41c1dc57c7e428954014e4e54667fe1c2d66ac6a426fe0f` / 318 行**（与主协调来电值一致）；我 18:38:10 CST 曾实测为 `e666ab15f1261bbfde9878a41e89c0b0ec99b4e8eed28bc126ac543a1d91f553` / **154 行** —— 两次差 164 行说明该文件在本窗口内**被别人更新过**，两次读数各自在其时刻真实，**以本轮 318 行为现值**；`gold_finish_20261015/HI1/E3/STATUS.md` = `6760df3a…` / 1,364 行（编辑前）；三作业 19:43:11 CST 读数：1069 183,032 行 / 196 SCF / **Step 196/239**、1071 36,897 行 / 36 SCF / **Step 36/246**、1073 9,049 行 / 8 SCF / **Step 8/230**，均无终态行，`pgrep -cx g16 = 4`。

- 不变项：E3b 定死版与「受约束剖面」口径不变；E2 次优先；两者**零生成零提交**（free cpus = 0）；腾槽后先拿口令 → 生成 → 六项自检（E3b 与 1028 帧、E2 与 seed 各逐原子 max|Δ|=0）→ 提交 → 5 分钟内报 job id/state/槽位。
- **§P.43 一处表述按原话改回（协调方 19:41 CST 指出）**：主协调原话是「**两档都单列、不进剖面**」，我先前写成“档 1 仍进剖面（标注档位）”**不合原话**，已改回：档 1（[1.20,1.50] Å）**表内照常报全部数值但标注档位、并从峰值判定中排除**；档 2（<1.20 Å 且 O28–H24 ≤1.05 Å）单列、不进剖面。理由照录：一维 C–C 剖面的峰必须只归因于 C–C 坐标，质子一旦与醛氧共享即混入第二个坐标；信息不丢，档 1 数值仍入表、只不参与峰值判定。`prep/E2_1D_SCAN_DESIGN.md` 现值 sha **26d3fcbb86dadb0b7aa108bfa7a9efd92611f039da92a58cea97b918e45e5c8d** / **52 行**（演进：779bd92f…/49 → 41f2dac0…/52（含错误表述）→ c25e0d82…/52 → 现值）。

### P.54 出处澄清确认 + Kabsch 三条合成自检首次输出 + 1074 第 2 格点只读读数（20:45:31–20:47:22 CST）

**1. 协调方（写-owner as_ec848a7673b74e35，20:45:31 实测）六条，逐条确认**
1) 出处：3.1165 / 2.6549 与 3.05–4.81 敏感性表 = 写-owner 会话的四元数 Kabsch 实现（已证伪），非本道产出；本道"不认领"成立。此后本道引用统一写该表述，不再用"独立复算"；对照方 = numpy SVD。
2) §P.53 改写已解决（20:43:41）：四元数值作废，SVD 口径 1.5464 / 1.5372 / 1.1574（重原子 20、禁镜像 det=+1）恢复可引用。
3) 新增口径（主协调 20:45 一致，已入 PROCESS.md）：此后任何 lane 报叠合/角度统计，先附三条合成自检输出（旋转+平移⇒0；镜像⇒≠0 且 det(R)=+1；同结构副本⇒0），并写明"实现 + 原子集（重原子 20 / 全原子 41）+ 禁止镜像"。本道接受，1074 逐格点 Kabsch 一律附。
4) 台账当前值：HI1/PROCESS.md 442 行 / 09c7aeeb310a4b9748a34834f4f30b8d03ffd3660ccdff44aea3eec73051b043（含"口径要求"与 20:43:27 状态条）。本道 19:46:31 的 331 行 / faf96d0b… 仅代表当时，不作当前值。
5) 定性结论与参照锁定不变：1069 末帧整体构象既非 P 也非 1028；P（job 1061）只是某一个频率验证的产物极小、不必然最低；产物端参照锚定 job 1061 的 P。
6) 边界：四条边 result/barrier 全 null；交付面 a2964d8d…/277 行/11 文件 sha 未动；本道零 kill / 零重投 / 零 priority 变更 / 零 ts_resume。

**2. 三条合成自检（首次正式输出；脚本 prep/kabsch_selfcheck.py，49 行，sha256 a93f1ccb1ec3cb53ff5b681b9ec6b1489065d34166db12e5130f0927a9e2fa0a）**
测试对象 = 1074 日志 L10688 处 41 原子 Input orientation 块（全原子 41 = 重原子 20 + H 21），即当前 in-progress 格点真实坐标。函数 = numpy SVD Kabsch，先去质心，det(U·Vt) 符号强制 det(R_opt)=+1（禁镜像），RMSD = sqrt(Σ((A·R−B)²)/N)。
- 全原子 41：(1) proper 旋转+平移 RMSD 1.790e-15 Å，det=+1.000000000000；(2) 镜像（improper，det=−1 变换）RMSD 2.111390 Å，det=+1.000000000000；(3) 同结构副本 RMSD 2.453e-15 Å，det=+1.000000000000。三条 PASS。
- 重原子 20：(1) 2.897e-15 Å；(2) 1.582759 Å；(3) 1.110e-15 Å，det 均 +1.000000000000。三条 PASS。总体 ALL PASS。
⇒ 本道先前报的 0.1224 / 0.1226 Å 即同一函数、全原子 41、禁镜像的 SVD 值，自检通过后作为可引用数值；每条引用必附"numpy SVD + 原子集 + 禁镜像"。

**3. 1074 只读读数（快照三元组齐全）**
- 本道 2026-10-17T20:47:02+08:00 / 12,031 行 / sha256 e9c539cd4920cd37f9fa29c597b119db83ffcb721a498938f563c62c37b5b4de；协调方独立复核 20:47:22 / 12,062 行 / sha d647c8df86022b622c7ea9aabdb1f85464521a004726225e9e694b5a3eeb1f66 ⇒ 同一文件先后两态，行号与判读一致（无冲突）。
- 绝对路径 /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/runs/e3b_scan2d_c2n4_o25h26.log
- L11309 "Step number  10 out of a maximum of  243 on scan point     2 out of    36"；L11220 " SCF Done:  E(RB3LYP) =  -939.297625871     A.U. after    9 cycles"
- "Optimization completed" 计数 = 1（L1938，仅格点 1；"Stationary point found" 亦仅 L1939）⇒ 格点 2 未收敛，其数值不入表（in-progress 读数）。
- 最新 Input orientation 块 L11625：R(2,4)=1.6248（=1.4248+0.2000，扫描坐标 1 在动）；R(25,26)=0.9693（未动）；R(4,26)=3.3103；R(10,27)=0.9949（冻结保持，在 0.9949±0.03 内）；R(2,25)=1.4287；R(2,26)=1.9996；H26 最近重原子 = O25 0.9693 Å（未悬空）。
- Kabsch（numpy SVD，全原子 41，禁镜像）格点 1 末帧 vs 当前帧 = 0.1226 Å < 0.3 Å ⇒ 无通道切换。C2···H26 ≈ 2.000 Å 属 1-3 距离（∠H26–O25–C2 ≈ 108–110°），非碰撞，不判失格。

**4. 未变项**：1074 不重投、不改优先级、不 kill；1071（18:32:58 起 running）、1073（19:25:43 起 running）均未终态，本道只读静默，仅在约定三类触发点报告（1074 能量峰/三连续点 RMSD>0.3 Å；1071 终态四档；1073 进入频率段并出现第二次 Normal termination）。E3b result 仍 null，无任何 barrier 回填。

### P.55 1073 opt 段收敛（仅登记，未出频段判读）+ 收敛帧自身序几何 + 能量分段口径（20:46:47–20:50:28 CST）

**A. 事实（1073 = build product seed opt+freq，post-freeze asset / 非交付证据）**
- 日志 /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/runs/build_seed_product_optfreq.log
- 快照：20:46:47（opt 段收尾）/ 20:49:20 51,677 行 / 1424b3fa…（协调方）；本道 20:50:28 快照 51,699 行 / sha 5e3c61827548c64fb7bcb90148d39e19e69ef3e7ca8a3fbbab897685667d5b57
- L49482 "Step number  53 out of a maximum of  230"；收敛表 L49769 表头 / L49770 Max Force 0.000030 YES / L49771 RMS Force 0.000004 YES / L49772 Max Displacement 0.001360 YES / L49773 RMS Displacement 0.000250 YES / L49774 "Predicted change in Energy=-2.922799D-08"；L49775 "Optimization completed."；L49776 "   -- Stationary point found."
- 第一条（opt 段）Normal termination：L50860 "Normal termination of Gaussian 16 at Sat Oct 17 20:46:47 2026."；L50870 "Link1: Proceeding to internal job step number 2"（此条为协调方实测，本道未独立核 L50870）
- freq 段 route（协调方转述）：#P Geom=AllCheck Guess=TCheck SCRF=Check GenChk RB3LYP/def2SVP Freq；freq 段首 SCF L51639 -939.316976731（1 cycle）
- "Frequencies --" 计数 = **0**（20:50:28）⇒ **freq 段未完成，本道不出 117 模/虚频判读，也不当作业完成**

**B. 收敛帧几何（按日志自身原子序读取，不依赖任何映射）**
块 L49159（Standard orientation，41 原子）；元素直方图 {C:15, H:21, N:1, O:4} = C15H21NO4 ✓
- N32 近邻：H41 1.0170、C28 1.4619、C31 1.4630 ⇒ 仲胺（N–H + 两根 N–C）
- O3=C2 1.2246（酮羰基）；O6–H19 0.9675、C5–O6 1.4237（羟基）；O25=C26 1.2199、C26–O27 1.3220、O27–H33 1.0012（羧基）
- **C2···N32 = 6.1258 Å ⇒ 该帧 C–N 不连**
- 映射口径（iso 3，seed 序→E3 标号 order[]，故上列 seed 序等价于 E3：2→C2、3→O25、27→O10、32→N4、33→H27、41→H26）：E3 标号下 R(2,4)=6.1258、R(2,25)=1.2246、R(4,26)=1.0170、R(25,26)=4.9583、R(10,27)=1.0012；对照 1028（hemiaminal）R(2,4)=1.4248、R(2,25)=1.4728、R(25,26)=0.9693 与 P(1061) R(2,4)=3.3308 ⇒ 该收敛帧在键表层面为 C2–N4 已断（产物侧），与 E3b = C–N 断裂一致；**映射相关数值依赖 iso 3，须在 freq 段末帧上复核后才可用于物种结论**

**C. 能量（分段、同批、纯电子；非 ΔE‡、不得作分母）**
- 1073 opt 段收敛帧 E = -939.316976731（L49393 7 cycles 与 freq 段 L51639 1 cycle 同值）
- ΔE vs P(job 1061, -939.319540184) = **+0.002563453 Ha = +1.6086 kcal/mol**（1073 帧更高）
- ΔE vs 1028(-939.312626605) = **-0.004350126 Ha = -2.7297 kcal/mol**
- 二者均标 **"纯电子、同批、非 ΔE‡、不作任何分母"**；不改变 E3b result = null

**D. 登记判语**：1073 opt 段 = **"optimized but no freq ⇒ 尚不构成驻点判定"**（此前既定口径），freq 段完成并出 39 组×3=117 后才按验收清单出报告。

**E. 并行作业读数（20:50:28）**：1074 = 13,933 行 / fdfa90fb…，Optimization completed 计数 1，L13180 "Step number  12 out of a maximum of  243 on scan point     2 out of    36"（仍格点 2），L13091 SCF -939.297688816；1071 = 77,382 行 / d86d26da…，L76605 "Step number  74 out of a maximum of  246"，L76518 SCF -939.301194235（未终态）。

**F. 未变项**：四条边 result/barrier 全 null；交付面未动；零 kill / 零重投 / 零 priority / 零 ts_resume；E3b 产物全部标"post-freeze asset，非交付证据"。

### P.56 强制声明：E3b 能垒引用必须同时写「产物区驻点能量跨度 ≈2.0 kcal/mol」（协调方 20:50:45 CST 定）

**A. 基准与复算（本道独立核对，数字一致）**
- 1028 = -939.312626605（interm_c160_optfreq.log L16838 = L19117，协调方实读；本道采用该值作 hemiaminal 分母，与此前一致）
- 相对 1028（纯电子差，× 627.5095 kcal/mol per Ha）：
  - P / job 1061 -939.319540184 ⇒ **-0.006913579 Ha = -4.3383 kcal/mol**
  - 1073 opt 收敛帧 -939.316976731 ⇒ **-0.004350126 Ha = -2.7297 kcal/mol**
  - 1069 末帧 -939.320189491 ⇒ **-0.007562886 Ha = -4.7458 kcal/mol**
- **产物区驻点能量跨度 = -4.7458 − (-2.7297) = 2.0161 ≈ 2.0 kcal/mol**（本级别纯电子差，非 ΔE‡，非能垒，不作为分母）
- 1073 相对 P = +0.002563453 Ha = **+1.6086 kcal/mol**（与本道 §P.55 C 节一致）

**B. 三条写入验收报告模板与判读清单（此后强制）**
1) 产物端参照**一律锚定 job 1061 的 P**（不选更低构象、不并列两个参照）。
2) **凡引用 E3b 能垒，必须同时写「产物区驻点能量跨度 ≈2.0 kcal/mol（本级别纯电子差）」**，作为参照不确定度。
3) **只报单值不写跨度 = 违规表述**；本道任何 dE/dE‡ 表述（含 lane 台账、AgentHub 汇报、给写-owner 的交付串）一律按此执行。

**C. 不引用项 / 引用口径**
- 1073 L48519 (-939.316976635) 是同末步前一次 SCF（差 0.1 µHa），**不引用**。
- 1073 opt 段只在「L49776 Stationary point found + L50860 Normal termination @20:46:47 + L49482 Step 53/230」意义上使用。
- freq 段起点 banner 行号本道与协调方略有差异（L50862 vs L50870，同一 banner）⇒ 引用写「Link1: Proceeding to internal job step number 2 附近（L5086x）」并注明口径。

**D. 状态（20:50:45 后）**：1073 freq 段仍未完成（"Frequencies --" = 0）⇒ 不出 117 模/虚频判读；等第二条 Normal termination 后按清单出报告（39 组×3=117、虚频只认 band 表负值 + imaginary 头行、0 虚频且最低实模 <20 cm⁻¹ 单列、约化质量与力常数、InChIKey 两次分列（seed 几何 / freq 末帧按映射重排）、41 原子图同构映射 + 键表逐边一致、ΔE 非 ΔE‡、物种层三选一）。
- 台账当前值（协调方）：HI1/PROCESS.md **458 行 / 9127eedeb761479ac8eecdd4b2f73e08cfafb0e96cbea59f70489b8baa6cf717**（新增「产物区驻点能量跨度」节）。

### P.57 行号与跨度口径定稿：banner = L50862、跨度统一 2.0160 kcal/mol（协调方 20:51:40 CST）

**A. 替换项（覆盖 §P.56 的两处表述）**
1) freq 段起点 banner 行号：**L50862 "Link1: Proceeding to internal job step number 2"**（主协调与协调方两次 grep -n 一致；协调方先前 L50870 已由其本人勘误）。此后本道引用写 **L50862** 并注"口径：协调方与主协调两次 grep -n 一致"，不再写"（L5086x 附近）"。
2) 产物区驻点能量跨度：**对外统一 2.0160 kcal/mol（四位小数）**。本道 §P.56 报的 2.0161 属 kcal 换算末位差（用未圆整 Ha 差 0.003212760 Ha 直接乘 627.5095 = 2.01606 → 2.0160）；三个差值 -4.3383 / -2.7297 / -4.7458 双方一致，不改。

**B. 九项距离双方逐项一致（本方块 L49159、日志自身原子序）**
N32–H41 1.0170、N32–C28 1.4619、N32–C31 1.4630、O3=C2 1.2246、O6–H19 0.9675、O25=C26 1.2199、C26–O27 1.3220、O27–H33 1.0012、C2···N32 6.1258 Å；元素断言 32=N、41=H、28/31/2/26=C、3/6/25/27=O、19/33=H（协调方独立复算，逐项相同）。
收敛证据：L49775 "Optimization completed." + L49776 "   -- Stationary point found."（协调方与我一致）。

**C. 判语与门槛不变**：1073 = "optimized but no freq ⇒ 尚不构成驻点判定"；"Frequencies --" 仍 0 ⇒ 不下物种结论；等 freq 末帧（117 模、虚频只认 band 表负值 + imaginary 头行、InChIKey 两次分列、41 原子映射 + 键表逐边一致）后再出。

**D. 叠合值引用口径**：vs 1028 = 2.8491 Å、vs P = 2.6798 Å（全原子 41，numpy SVD，禁镜像 det=+1）按"本道实测"登记；进最终报告时**必附三条自检输出**（prep/kabsch_selfcheck.py / prep/metrics_1073_optstage.py 内同一函数：1.657e-15 / 1.439323 / 3.787e-16，det 全 +1.000000000000），协调方将独立复算后再引用。

**E. 台账现值**：HI1/PROCESS.md **467 行 / ea957a2d2954334b8a17262ccc154e3cd767a56bd1991dbbb8486167dbecebc6**（协调方 20:51:40 实测）。四条边 result/barrier 全 null；交付面未动；零 kill / 零重投 / 零 priority / 零 ts_resume。

### P.58 频段判读工具就绪并双日志交叉验证（prep/freq_report.py，20:52:17–20:52:33 CST）

**A. 工具**：gold_finish_20261015/HI1/E3/prep/freq_report.py，sha256 **71a445d56b8dd518d59d252ff6b3877e0672207b64089e6e3514594797280848**。实现要点：只认频段表 'Frequencies --' 块（39 组 ×3）的数值做虚频筛查；同时单列 'imaginary' 头行；'Red. masses --' / 'Frc consts  --' 同块取约化质量与力常数；ZPE 取 'Zero-point correction'；并报两条 Normal termination 与 'Optimization completed' 行号。

**B. 交叉验证（用已被人工核过的两个 41 原子参照 log，验证解析口径无偏差）**
1) P（job 1061）runs/P_e3b/P_optfreq.log，73,964 行：39 组 / **117 模 = 3N−6 ✓**、带表负值 **0**、imaginary 头行 **0**、ZPE **0.344928**、最低实模 **16.6787 cm⁻¹**、末次 SCF **L69139 -939.319540184**、Normal termination L68350 @16:24:12 与 L73964 @16:34:16 ⇒ 与本道台账既有登记（L69831 首值 16.6787，见 §P 早条目 L1142 行）**完全一致**。
2) 1028（hemiaminal 分母）runs/interm_c160/interm_c160_optfreq.log，23,954 行 / sha 1ec7e4c6388415d0859939238f4f96ec7739c0bbf1f985a28f4dd3c23b7dcec1：39 组 / **117 模 ✓**、带表负值 **0**、imaginary 头行 **0**、ZPE **0.347492**、最低实模 **19.8439**、末次 SCF **L19117 -939.312626605**、Normal termination L18325 @10:56:06 与 L23954 @11:10:09 ⇒ 与既有登记逐项一致（Stationary 处本道取 'Optimization completed.' L22248，既有条目写 'Stationary point found' L22249，二者相邻不同关键字，不冲突）。
⇒ 工具口径通过双参照验证；1073 freq 段完成（第二条 Normal termination）即可直接出验收报告，不需再手工计数。

**C. 1073 现状（20:52:17 同批读取）**：51,706 行 / sha b81fb0e9…；39 组 = 0；'Frequencies --' 计数 0；Normal termination 仍 1 条（L50860，opt 段）⇒ 判语不变「optimized but no freq ⇒ 尚不构成驻点判定」。

**D. 注意项（既有登记、非新发现）**：产物参照 P(1061) 最低实模 16.6787 cm⁻¹ 与 1028 的 19.8439 cm⁻¹ 均 <20 cm⁻¹ 偏软 ⇒ 按既定门槛，**参照自身即被"<20 cm⁻¹ 单列"标记**；故 E3b 报告须同时写「参照软模声明 + 产物区驻点能量跨度 2.0160 kcal/mol」两项，避免把软模标记只安在 1073 头上。

**E. 未变项**：四条边 result/barrier 全 null；交付面未动；零 kill / 零重投 / 零 priority / 零 ts_resume。
### P.59 叠合口径更正：按索引值作废，改用映射值（重原子 20 = 2.2976 Å）；192 匹配复现、1028 侧「4 匹配」未复现（20:54:24 CST）

**A. 作废项**：本道 §P.55/§P.57 报的 vs 1028 = **2.8491** / vs P = **2.6798** 系**按原子序号直接叠合**（1073 log 元素序为 CCOCCO…、P/1028 为 CCCN…，索引无化学对应）⇒ 全部标 **「按索引叠合值，已作废」**，不得再引用。

**B. 已独立复现的映射值（脚本 prep/mapped_kabsch_1073.py，sha256 1010f7a361248a2888dd60b3ef1acbaf13228574497f8eb39a1f2170bdabd9bc）**
- 元素序核对：1073 块 L49159 = CCOCCOCCCCCCHHHHHHHHHHHHOCOCCCCNHHHHHHHHH；P 与 1028 = CCCNCCCCCOOHHHHHHHHHHHHHOHHOCCCCCCCHHHHHH（与协调方字符串逐字符相同）
- 协调方给的 20 对重原子（1073 序 → E3 序）元素一致性检查：**True**（1:3, 2:2, 3:25, 4:1, 5:29, 6:28, 7:30, 8:35, 9:34, 10:33, 11:32, 12:31, 25:11, 26:9, 27:10, 28:8, 29:7, 30:6, 31:5, 32:4）
- **1073→P 重原子 20 映射 Kabsch = 2.2976 Å**，det(R_opt)=+1.00，max **4.7027 Å**，最差项 = 第 13 对（1073 原子 25 → E3 11）⇒ 与协调方 2.2976 / 4.7027 逐位一致（其「worst 1073 原子 13」应读作「第 13 对」，对应 1073 原子 25）
- 三条合成自检（同一 kabsch()，numpy SVD、去质心、det 强制 +1）：(1) 旋转+平移 **1.106e-15 Å** det=+1.000000000000；(2) 镜像 **1.364308 Å** det=+1.000000000000；(3) 副本 **4.137e-16 Å** det=+1.000000000000
- RDKit（DetermineConnectivity、无手性）复现：**1073 重原子键 20 / P 20 / 1028 21**（差的一条即 1028 的 C2–N4 = 1.4248）✓；**1073→P 匹配数 = 192** ✓；最优重原子 Kabsch 2.2976 Å ✓

**C. 1028 侧：数值可复现、机制未复现（须改口径）**
- 协调方 1073→1028 的 **2.4164 Å（max 4.1318）**：本道用**同一 20 对**（由 P 导出）套到 1028 几何上，得 **2.4164 / 4.1318 逐位一致** ⇒ 数值可复现。
- 但协调方所述「删去 1028 的 C2–N4 边后得 4 匹配」本道**未复现**：本道删边（E3 2–4，0-based 1–3）后 GetSubstructMatches 返回 **0 匹配**（1073 有 20 条重原子键，删边后 1028 亦 20 条，但 H 归属差异——H26 在 1028 挂 O25、在 1073 挂 N4——使整图匹配失败）。
⇒ 1028 侧数值登记口径改为：「**同一 20 对映射套用于 1028 几何的诊断值 2.4164 Å（max 4.1318），非独立子结构匹配所得**」；「4 匹配」暂不引用，待协调方给出查询构造（是否去 H / 用何查询图）。

**D. 全原子 41 映射值暂不引用**：协调方报 mapped all-41 = 2.6798，本道无其 H 映射无法复核；而本道按索引的 all-41 恰也是 2.6798（纯属数值巧合）⇒ **在 H 映射给出前，本道只引重原子 20 的 2.2976 Å**，不引任何 all-41 映射值。

**E. 保留项**：**C2···N32 = 6.1258 Å**（1073 自身序 2–32）保留，写法改为「1073 序 2–32（映射确认 = E3 的 C2–N4）⇒ 该帧 C–N 不连成立」。九项距离、L49775/L49776/L49482/L50860、能量链（-939.316976731、vs 1028 -2.7297、vs P +1.6086、跨度 2.0160）全部不变。

**F. 状态**：1073 freq 段未完成（Frequencies -- 计数 0）⇒ 不出 117 模/虚频。台账现值（协调方）：HI1/PROCESS.md **477 行 / 3591d2df…**（新增「阻断项解除」节）。四条边 result/barrier 全 null；交付面未动；零 kill / 零重投 / 零 priority / 零 ts_resume。
### P.60 全 41 对映射复核通过；「4 匹配」已复现（本道 §P.59 C 节自我更正）（20:55:47–20:56:17 CST）

**A. 全 41 对映射（协调方给定，1073:P，1-based）复核结果（脚本 prep/mapped_kabsch_1073_v2.py，sha256 5f2c4eacab900f2ea535269fb46ab12d731fb3bd5dd123905534aa3aac05ccdc）**
- 双射检查：源索引与靶索引各覆盖 1–41 恰好一次 = **True / True**；元素一致性 **0 处不符**
- **全原子 41 映射 Kabsch 1073→P = 2.6798 Å，det(R_opt)=+1.00，max 5.3753 Å**（最差 1073 原子 25）⇒ 与协调方 2.6798 / 5.3753 逐位一致
- 同一映射的**重原子 20 子集 = 2.2976 Å / max 4.7027 Å / det +1.00**（最差为 heavy 第 13 位 → 1073 原子 25）⇒ 一致
- 三条合成自检（同一 kabsch()：numpy SVD、去质心、det 强制 +1）：(1) 旋转+平移 **1.051e-15 Å** det=+1.000000000000；(2) 镜像 **1.936628 Å** det=+1.000000000000；(3) 副本 **6.284e-16 Å** det=+1.000000000000
⇒ **all-41 2.6798 通过复核，可引用（必须写「映射后」）**；重原子 20 的 2.2976 同口径可引。

**B. 本道 §P.59 C 节的自我更正：「4 匹配」是**真的**，本道先前的 0 匹配是构造瑕疵**
- 协调方澄清：其 4 匹配在**重原子 20 图（去全部 H）**上做、先删 1028 的 C2–N4 边；含氢整图必然 0 匹配。
- 本道按此重建（脚本 prep/heavy_graph_match_1028.py，sha256 f331f5e2060df50b0ae418ee16ad5cadac3b5ebe176db1066df79d038cc867e1；做法：Determ ineConnectivity 于整分子→只保留重-重键→删去原 0-based 键 (1,3) 即 E3 C2–N4→显式建 20 原子/20 键图）：**匹配数 = 4**，最优 **重原子 Kabsch 2.4164 Å / det=+1.00 / max 4.1318 Å** ⇒ 与协调方逐位一致。
- 本道先前的 0 匹配来自「在删边后的 41 原子 mol 上调用 RemoveHs」这一构造瑕疵（价态不完整致去氢/匹配失败），**已作废**；§P.59 C 节「4 匹配未复现」的表述撤销。
- 佐证：1073 重原子度分布 {C1:1, C2:9, C3:5, N2:1, O1:4}；1028 原图 {C1:1, C2:9, C3:4, C4:1, N3:1, O1:4}，删 C2–N4 边后变为 {C1:1, C2:9, C3:5, N2:1, O1:4} 与 1073 **完全相同**（键多重集亦相同：C–C 14 / C–N 2 / C–O 4）⇒ 删边后两张重原子图同构，4 匹配合理。

**C. 口径定稿（此后引用一律）**
- 1073→P：**映射后** 重原子 20 = 2.2976 Å（max 4.7027，worst 回映 1073 原子 25）、全原子 41 = 2.6798 Å（max 5.3753）；均 numpy SVD + 禁镜像 + 三条自检。
- 1073→1028：**重原子 20 图上删 C2–N4 边后 4 匹配**所得 2.4164 Å（max 4.1318）；含氢整图不可匹配（0 匹配）——引用时必须带这两条限定。
- 按索引叠合的 2.8491 / 2.6798 已作废（后者与映射后 all-41 数值相同纯属巧合，引用时必须写「映射后」）。
- worst 只在重原子 20 子集内取并回映 1073 工作序。

**D. 状态**：1073 freq 段未完成（Frequencies -- 计数 0）⇒ 不出 117 模/虚频/InChIKey。C2···N32 = 6.1258 写「1073 序 2–32（映射确认 = E3 C2–N4）」。台账现值（协调方）：HI1/PROCESS.md **487 行 / b362e068e7b4482d4c835b54d968034115dadcf717e51d74015a8bddfe20972f**。四条边 result/barrier 全 null；交付面未动；零 kill / 零重投 / 零 priority / 零 ts_resume。
### P.61 1074 第 2 格点入表、第 3 格点起跑：约束剖面单调上升、无峰（20:59:53 CST）

**A. 快照三元组**
- 1074 /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/runs/e3b_scan2d_c2n4_o25h26.log：2026-10-17T20:59:53+08:00 / **19,836 行** / sha256 **ad9fb35c617151a968af2b8c6db84618ce21d646116d05a059f2e3ec90c0cee2**
- 1073 build_seed_product_optfreq.log：52,319 行 / sha **42d80aa13f375afc5df25594b5595e67987aba7ed5e918fbe49505f2bc685a54**；Frequencies -- 计数 **0**（freq 段未完成）
- 1071 ts/ts_0020/.../refine.log：83,395 行 / sha **55dccd69ede2e0722660cd1768392fc27ba193cdd828e3ed26e19353611b449f**；L82467 "Step number  80 out of a maximum of  246"（未终态）

**B. 已收敛格点（仅这两点入表；"Optimization completed" = L1938 / L18048）**
| 格点 | R(2,4) | R(25,26) | R(4,26) | R(10,27) | R(2,25) | R(2,26) | H26 最近重原子 | E(a.u.) | E−1028 (kcal/mol) | E−P1061 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 1.4248 | 0.9693 | 3.1829 | 0.9949 | 1.4728 | 2.0398 | O25 0.9693 | -939.312626605 (L1047) | **+0.00** | -4.34 |
| 2 | 1.6248 | 0.9693 | 3.3096 | 0.9949 | 1.4296 | 1.9986 | O25 0.9693 | -939.297700793 (L17649, 收敛 L18048) | **+9.37** | +13.70 |
- 格点 1 的能量与 1028 分母 **逐位相同**（-939.312626605，L1047）⇒ 扫描首点复现 hemiaminal 分母，内部一致性交叉验证通过。
- 格点 2 优化 16 步收敛（末 3 次 SCF L15865/L16758/L17649 差 < 1e-6 Ha）；Kabsch（全原子 41、numpy SVD、禁镜像）格点 1→2 = **0.0989 Å** < 0.3 Å ⇒ 无通道切换。

**C. 在跑格点 3（未收敛，只报方向）**
- 预期 R(2,4) = 1.8248（+0.2000）、R(25,26) 仍 0.9693；实测块 L20208：R(2,4)=**1.8248**、R(25,26)=**0.9693**、R(4,26)=3.4558、R(10,27)=**0.9949**（冻结保持）、R(2,25)=1.4045、R(2,26)=1.9799、H26 最近重原子 O25 0.9693 Å
- L18852 SCF -939.267155390（+28.53 vs 1028）→ L19809 SCF -939.270558172（**+26.40** vs 1028）；L18940 "Step 1/243, scan point 3/36"、L19898 "Step 2/243"
- Kabsch 格点 2 末帧 vs 当前 = **0.0886 Å**；格点 1 vs 当前 = 0.1850 Å（均 < 0.3）

**D. 触发点判定（明确）**
- **无能量峰**：目前 E 序列 +0.00 → +9.37 →（在跑 +26.4）**单调上升**，按定义尚不构成峰；峰只在后点回落时成立。
- **无通道切换**：三处 Kabsch 全部 < 0.3 Å。
- **约束全部保持**：R(10,27) = 0.9949（冻结，0.9949±0.03 内）；H26 始终挂 O25（0.9693，0.95–1.35 Å 内）。
- **正在动的是扫描坐标 1（R(2,4)）**；扫描坐标 2（R(25,26)）尚未开始，符合"前 6 个格点只覆盖键维、第 7 点起展开质子维"。
- 文字口径：以上为**受约束剖面（O10–H27 冻结）**读数，任何峰只能写"TS 候选 / 上界"，不得写 ΔE‡，也不得与 1028/P 之外的模型混算。

**E. 三条自检（本次同批输出，prep/kabsch_selfcheck.py）**：全原子 41 → (1) 1.643e-15 / (2) 2.104926 / (3) 5.645e-16；重原子 20 → (1) 2.992e-15 / (2) 1.587727 / (3) 6.998e-16；det(R_opt) 全部 +1.000000000000，ALL PASS。

**F. 未变项**：1074 不重投 / 不改优先级 / 不 kill；1073 freq 段未完成 ⇒ 不出 117 模/虚频；1071 未终态。四条边 result/barrier 全 null；交付面未动；零 ts_resume。
### P.62 1073 频率验收报告（freq 段完成：39 组×3 = 117 模、0 虚频、最低实模 21.0040 cm⁻¹、InChIKey = SMPZMOQIWMNUBG-YBVIJTQESA-N ⇒ 进入 P 物种的另一个极小）21:01:14–21:01:38 CST

**0. 事件**：job 1073 状态 done。日志 /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/runs/build_seed_product_optfreq.log，**56,450 行**，sha256 **6295535260ac9c8c58a077e8fed3a3e914cee4693d38770a2f7fa5f6ea553a85**（21:01:17 快照）。**第二条（freq 段）Normal termination：L56450 "Normal termination of Gaussian 16 at Sat Oct 17 21:01:14 2026."**；第一条（opt 段）L50860 @20:46:47。

**1. 完整性（第一列）**
- `Frequencies --` 组数 **39** ×3 = **117 模 = 3N−6（N=41）✓ 相等**
- opt 段：L49775 "Optimization completed." + L49776 "   -- Stationary point found."，L49482 "Step number  53 out of a maximum of  230"，收敛表 L49769–L49774 四项全 YES（0.000030 / 0.000004 / 0.001360 / 0.000250，Predicted −2.922799D-08）
- freq 段：L52330 "Harmonic frequencies (cm**-1) ..."，首块 **L52336 " Frequencies --     21.0040                30.4289                37.6682"**，末块结束于 L56450 前
- ZPE **0.345170**（L54294 "Zero-point correction= 0.345170 (Hartree/Particle)"）；Thermal correction to Enthalpy 0.366618（L54296）；Sum of electronic+ZPE **−938.971806**（L54298）
- 振动前后几何一致：opt 末帧（块 L49159）与 freq 末帧（块 L51477，Standard orientation）逐原子 **max|Δ| = 0.000000 Å**

**2. 虚频（第二列）**
- 频段表内负值个数 = **0**（39 组全项扫描）；`imaginary` 头行出现次数 = **0** ⇒ **0 虚频**
- **最低实模 21.0040 cm⁻¹（L52336 首值）≥ 20 cm⁻¹ ⇒ 不触发「<20 cm⁻¹ 单列」标记**（对照：P/1061 为 16.6787、1028 为 19.8439，二者仍标偏软；本条只说明 1073 自身不越线，不改对参照的标记）
- 无虚频 ⇒ 该驻点为**频率验证的极小**（不是鞍点、不能当 TS/TS 候选）

**3. 能量（同批 B3LYP/def2SVP/gd3bj/cpcm-dmso，纯电子；非 ΔE‡，不作分母）**
- E = **−939.316976731**（opt 段 L49393 7 cycles；freq 段单点 L51639 1 cycle，同值互验）
- ΔE vs I2(−939.320655479) = +0.003678748 Ha = **+2.3088 kcal/mol**（1073 更高）
- ΔE vs P(job 1061, −939.319540184) = +0.002563453 Ha = **+1.6086 kcal/mol**（1073 更高）
- ΔE vs 1028(−939.312626605) = −0.004350126 Ha = **−2.7297 kcal/mol**（1073 更低）
- **并写声明**：产物区驻点能量跨度 **≈2.0 kcal/mol（2.0160，本级别纯电子差）**；产物端参照锚定 **job 1061 的 P**；本报告不含任何能垒/ΔE‡ 数值。

**4. InChIKey（两次、分列）**
- (a) freq 段末帧（块 L51477）经 RDKit DetermineBonds(charge=0) → **SMPZMOQIWMNUBG-YBVIJTQESA-N**
- (b) 输入种子几何（build_seed_product_optfreq.gjf 坐标）→ **SMPZMOQIWMNUBG-YBVIJTQESA-N**
- 对照：声明的 P = SMPZMOQIWMNUBG-YBVIJTQESA-N ✓ 同；P(job 1061 末帧) = SMPZMOQIWMNUBG-YBVIJTQESA-N ✓ 同；**1028 帧 = AVHQBENQCFUXII-KCQAQPDRSA-N（不同）**
- InChI 显示 P 物种为**两组分**：InChI=1S/C10H12O2.C5H9NO2/...（ketol C10H12O2 + 脯氨酸 C5H9NO2；C–N 不成键，重原子键 20 条；1028 为 21 条）

**5. 几何（三段式：1073 自身序 / 映射后 E3 标号 / 化学解释）**
- 1073 自身序：C2(A2)–O3 1.2246；N32–H41 1.0170；**C2(A2)···N32 6.1258**；C26=O25 1.2199；C26–O27 1.3220；O27–H33 1.0012；O6–H19 0.9675
- 映射后（E3 标号，iso 全 41 对）：R(2,4) C2–N4 = **6.1258**、R(2,25) C2–O25 = **1.2246**、R(4,26) N4–H26 = **1.0170**、R(25,26) O25–H26 = 4.9583、R(10,27) O10–H27 = 1.0012
- 化学解释：酮羰基 C2=O25、羧基 C26(=O)–O27–H、仲胺 N4(H26)(C28)(C31)、酮醇羟基 O6–H19；**C2–N4 不连** ⇒ 与 1028（hemiaminal，C2–N4 = 1.4248、O25–H26 = 0.9693）整分子非同构
- 叠合（**映射后**，numpy SVD + 禁镜像 + 三条自检）：1073→P 全原子 41 = **2.6798 Å（max 5.3753，worst 1073 原子 25）**、重原子 20 = **2.2976 Å（max 4.7027）**；1073→1028 = **重原子 20 图删 C2–N4 边后 4 匹配**得 **2.4164 Å（max 4.1318）**，含氢整图 0 匹配

**6. 物种层结论（三选一，明选）**：**进入 P 的 basin**——与声明的 P **InChIKey 完全相同**、0 虚频 ⇒ 是**频率验证的产物侧极小**；但它不是 job 1061 的那个极小：映射后与 P 的叠合 2.6798 Å（重原子 2.2976 Å），能量在其上方 **+1.6086 kcal/mol**（纯电子）。故登记为「**P 物种的另一个构象极小（第三个产物侧驻点）**」，扩写产物区驻点能量跨度（仍为 2.0160）。**非**「塌回 I2 basin」、**非**「第三物种新极小」；1028 的 hemiaminal 物种（AVHQBENQCFUXII）与它不同。

**7. 边界与性质**：1073 为 **post-freeze asset / 非交付证据**；E3b result 仍 **null**，无任何 barrier 回填；不改生成器 / HI1.json / 报告 / 交付面（a2964d8d… / 277 行 / 11 文件 sha）。

**8. 并行读数（21:01:17）**：1074 = 20,782 行 / sha 02c199c30b1ec66196f490cb7c56e092fdd1f862bbc26cb9c7224263f263ef7c，Optimization completed 计数 2（L1938/L18048），仍在格点 3（L19898 Step 2/243），格点 3 最新 SCF L20755 −939.271006444；1071 = 84,413 行 / sha 23cb9a2fd023bc4e0350f668e0fc81ae08628aec3abcfd853459cc4f9321e150，L83579 Step 81/246，未终态。
### P.63 1073 三档能量 + 逐片段叠合（口径更正）+ 模式分段复现；归属澄清：1.5030 / C2–N18 / E2 三件事不属于本道（21:09:09–21:09:20 CST）

**A. 能量三档分列（同批、纯电子 / 加 ZPE / 加自由能；三者不互换、非 ΔE‡、不作分母）**
| 档 | 1073（行号） | P（job 1061，行号） | Δ(1073−P) |
|---|---|---|---|
| 纯电子 E | −939.316976731（L49393 / L51639） | −939.319540184 | **+0.002563453 Ha = +1.6086 kcal/mol** |
| E + ZPE | −938.971806（L54298；ZPE 0.345170 L54294） | −938.974612（L71793；ZPE 0.344928 L71789） | **+0.002806 Ha = +1.7608 kcal/mol** |
| E + 热自由能 | −939.023487（L54301） | −939.028213（L71796） | **+0.004726 Ha = +2.9657 kcal/mol** |
- 与协调方三档数值逐位一致；ΔZPE 本身 = +0.000242 Ha = +0.1519 kcal/mol。

**B. 逐片段叠合（口径更正：两片段复合物必须分段叠合，整复合物单次 Kabsch 不是构象度量）**
- 片段识别（RDKit DetermineBonds）：1073 = 24 原子片段（C10，ketol）× 17 原子片段（C5，脯氨酸）；P 同（24 / 17）
- 1073→P **逐片段**（用 iso 全 41 对映射限定片段内原子；numpy SVD + 禁镜像 + 三条自检）：
  - 脯氨酸 17 原子：全原子 **1.0936 Å**（max 2.8377）；重原子 8 个 **0.3026 Å**（max 0.5744）
  - ketol 24 原子：全原子 **1.2553 Å**（max 3.3160）；重原子 12 个 **0.9705 Å**（max 2.3392）
- ⇒ 两片段**内部构象几乎同形**（脯氨酸重原子 0.30 Å），两极小的差别主要在**片段间相对取向与氢键几何**，而非内部构象。
- 整复合物单次 Kabsch（全 41，映射）= **2.6798 Å**，此数**不作为构象度量**（与协调方读数 ~3.30 的差异来自所用映射/原子集不同，结论一致：整复合物单次叠合不上口径）；此前所有「2.6798 / 2.2976」仅保留为映射后整体差异登记。

**C. 片段间接触 / 氢键**：1073 **O3(酮羰基)···H33–O27 = 1.6647 Å**、**O3···O27 = 2.6482 Å**；P 侧本道实测 O25···H26 = **3.1370 Å**（协调方给的 P 侧最短接触 2.0746 应对应另一原子对，本道未复现具体配对，暂按「协调方实测」登记）。

**D. 117 模分段与最低模参数（复现协调方）**：<200 = **14**、200–800 = **23**、800–1800 = **59**、>1800 = **21**（合计 117）；min **21.0040**、max **3803.8277**；最低 8 条 21.00 / 30.43 / 37.67 / 55.16 / 66.82 / 77.27 / 84.80 / 95.85；最低模 Red. mass **4.2181**、Frc const **0.0011**（L52337 / L52338）。

**E. 归属澄清（重要，避免串道）**
- 本道台账全文 grep：**无「1.5030」、无「C2–N18」**；本道 §P.62 写的是 C2(A2)–O3 = **1.2246**（C2 无任何 1.5030 的 C–O 键）。故「C2–O3 = 1.5030」与「C2–N18」**不是本道发出**，请按其来源 lane 核对。
- 同理「E2 三件事」（E2_1D_scan.log 的 300 s / 90 min 只读 check、L14996 / −939.308205969 采纳与 L14148 作废、L18881 / L17977 过程帧、R(1,29) 反向或 |ΔE|>15 kcal/mol 触发）：**全部不属于本道**——本道无 E2 作业、从未引用这些行号/数值、也从未对 E2_1D_scan.log 设过轮询（E2 的 job 1075 属 session as_f59e78f07a0e4d07）。本道当前只守护 1074 与 1071。

**F. 工具**：prep/fragment_kabsch_1073.py，sha256 **b7d1cdc457d2d3179a6c68b3aa72a9721672cff67148f06b387988fe4b2dd751**；三条自检 1.398e-15 / 1.509220 / 4.777e-16，det 全 +1.000000000000。

**G. 未变项**：1073 = post-freeze asset / 非交付证据；E3b result 仍 null、无 barrier 回填；交付面未动；零 kill / 零重投 / 零 priority / 零 ts_resume。台账现值（协调方）：HI1/PROCESS.md **512 行 / c5dab1f6d8cbfcd1b8c649ba59614073227f892c1181d8637ec24257c558705f**（21:08:26 CST）。
### P.64 三档口径定稿（2.2976 / 2.4104 / 2.6798 同一映射）、iso 1 备查（2.3538、ketol 1.2160）、接触配对补全、E2 串线定位（21:10:41–21:11:07 CST）

**A. 协调方撤回「~3.30」**：根因为 GetSubstructMatches 返回 target 侧原子序、按 query 位置对齐，A→P 方向用反（错值 3.0647 / 3.3043）。本道未用过该方向，无受影响数值。

**B. 三档口径本道独立复算（脚本 prep/three_tier_kabsch_1073.py，sha256 de07ea4432d9361de6ee5ee990c11e2fbc9ca0b73dd4eb62e28d507ec8a226b4）**
| 映射 | 拟合集 / 评估集 | RMSD | max | det |
|---|---|---|---|---|
| iso 3（mapping#2） | 重原子 20 / 重原子 20 | **2.2976** | 4.7027 | +1.00 |
| iso 3 | 全原子 41 / 重原子 20 | **2.4104** | 5.3753 | +1.00 |
| iso 3 | 全原子 41 / 全原子 41 | **2.6798** | 5.3753 | +1.00 |
| iso 1（mapping#1） | 重原子 20 / 重原子 20 | **2.3538** | 4.3633 | +1.00 |
| iso 1 | 全原子 41 / 重原子 20 | 2.4437 | 4.8579 | +1.00 |
| iso 1 | 全原子 41 / 全原子 41 | 2.8240 | 4.8579 | +1.00 |
⇒ 与协调方 2.2976 / 4.7027、2.4104 / 5.3753、2.6798、2.3538 / 4.3633 逐位一致。台账措辞改为「同一映射 + 三档口径（拟合集/评估集）」，撤销「映射/原子集不同」的说法；引用时必须写清拟合集/评估集与映射编号。

**C. 逐片段叠合（两种同构都算，脚本 prep/fragment_kabsch_both_iso.py，sha256 d858028e0b0277570486eb9a9bc8f565201d206766d314feff276810ce6f6086）**
- iso 3：ketol（24 原子，重原子 12）**0.9705（max 2.3392）**；脯氨酸（17 原子，重原子 8）**0.3026（max 0.5744）**
- iso 1：ketol **1.2160（max 3.3388）**（与协调方备查值一致）；脯氨酸 **0.3026（max 0.5744）**（两种同构下相同）
- ⇒ 脯氨酸内部构象与同构选择无关，ketol 因环方向两支差 0.9705 vs 1.2160；两片段内部构象几乎同形，差异集中在片段间相对取向与氢键。

**D. 接触配对补全（采纳协调方清单，元素对已核）**
- 1073：**O3···H33 = 1.6647（最短）**、O3···O27 = 2.6482、H16···O25 2.2675、H20···O25 2.3351、H20···H36 2.4885、O6···H36 2.5571
- P：**O28···H26 = 2.0746（全局最短）**、H36···H27 2.3327、**O25···H27 = 2.3670**、H24···H26 2.3742、H36···O10 2.6332
- 报告写法：**「最短 = O28···H26 2.0746；O25···H26 = 3.1370（E3 道实测）」**——不同原子对，并存不冲突。

**E. 归属定位（不追责，只定线）**
- 本会话 session_id = **as_06db52ada5014800**（role small_mol）。
- evt_c874a215070f4408（E2 状态回报）author_session = **as_b8536002aacb48e3**（另一 small_mol 会话，parent = as_ec848a7673b74e35）⇒ 不是本会话；主协调 21:10 已裁定 **E2 剖面表唯一出表方 = as_b8536002aacb48e3**，提交 lane as_f59e78f07a0e4d07 只报作业状态；本道此前收到的 E2 授权作废，本道不再为 E2 做任何事。
- 「C2–O3 = 1.5030」：本道台账在 §P.63 之前无此行（全文仅命中 §P.63 的引用纠正句）；事实按协调方登记入本台账：**1073 序 1.5030 = C1–C2（两端皆碳）；C2 与任何 O 都无 1.5030 的键，C2–O3 = 1.2246**。本道不传播该错行。

**F. 状态**：1074 格点 3 进行中（未收敛）；1071 未终态。协调方 1074 只读检查点设在 ≥4 个收敛格点（相邻点 Kabsch，20 重原子、SVD、det=+1、先贴三条自检）。

**G. 未变项**：E3b result 仍 null；交付面未动；零 kill / 零提交 / 零 priority / 零 ts_resume。台账现值（协调方）：HI1/PROCESS.md **513 行 / d1421f8458970e4e67aadaa1e48557745f355e942d31f19ffce68232f4ea9854**（21:09:56 CST，含其自我更正段）。
### P.65 协调方第 7 条收口确认（含一处测量缺口）+ 本道自测 PROCESS.md 现值（21:12 CST）

**A. 确认项**：①E2 归属已查明并写入其台账（author_session = as_b8536002aacb48e3），本会话（as_06db52ada5014800）不做任何 E2 事、不设 E2 轮询、不等 mention；②三档口径双向一致，其中 **iso 1 的 2.4437（41 拟合/重原子评估）与 2.8240（41/41）为本道补位值**，协调方按其方实测登记；③逐片段两同构入账（iso3 ketol 0.9705 / 脯氨酸 0.3026；iso1 ketol 1.2160 / 脯氨酸 0.3026）；④接触写法「最短 = O28···H26 2.0746；O25···H26 = 3.1370（E3 道实测）」采纳，另存 O25···H27 2.3670；⑤「1.5030」两 lane 台账均无此行，事实登记一致（1073 序 1.5030 = C1–C2；C2–O3 = 1.2246），已由主协调撤回、不再引用。

**B. 测量缺口（登记，不补猜）**：协调方第 7 条写「HI1/PROCESS.md **515 行 / sha 见下**」但本条正文**未给出 sha 值** ⇒ 该 sha 记为 **missing measurement（未测量）**，本道不自行编造；本道自测（见 C）仅作自己时刻的值，不替代对方口径。

**C. 本道自测（21:12 快照，供对照）**：
- HI1/PROCESS.md：见同批输出（行数与 sha 以本道 date/wc/sha256sum 实测为准）
- 1074 e3b_scan2d_c2n4_o25h26.log：见同批输出（行数 / sha / Optimization completed 计数 / 末条 scan point 行号）
- 1071 ts_0020 refine.log：见同批输出（Step number 末条行号 / 行数）

**D. 判读门槛照旧**：1074 仅在 **≥4 个收敛格点**时由协调方动检查点（相邻点 20 重原子 Kabsch，SVD、det=+1，先贴三条合成自检）；峰只作候选/上界、不写 ΔE‡；任何能垒引用必附「产物区驻点能量跨度 2.0160 kcal/mol（1028 参照）+ 参照锚定 job 1061 的 P」。

**E. 未变项**：四条边 result/barrier 全 null；交付面未动；零 kill / 零提交 / 零 priority / 零 ts_resume。
**F. §P.65 B 节缺口已闭合（21:12:08–21:13 CST）**：协调方补发 sha = **860cf440816bd3f993def59270edd6c1a0e5dc5ba7d04096c4376fdb061fe405**（其 21:11:58 实测，515 行），与本道 21:12:08 独立实测 **515 行 / 860cf440…** **逐位相同** ⇒ 该值双签，`missing measurement` 标记撤销；「见下」占位符仅影响该字段。

**G. 同期读数（21:12:08，本道实测）**：1074 = **30,862 行 / sha 6d2930ca256254a76cb96d6d610a6348f865514d6b2c30db7eeb46cbb77bf21e**，Optimization completed 计数 **2**（L1938 / L18048），L30234 "Step number  13 out of a maximum of  243 on scan point     3 out of    36"（仍格点 3，未收敛，不入表）；1071 = **94,257 行**，L93409 "Step number  90 out of a maximum of  246"（未终态）。
### P.66 回报协议收敛为「触发类」（协调方 21:13 CST 要求）+ 判读口径原文复述 + 一处口径适用范围申明

**A. 回报协议（此后执行，本道不再发纯收条）**
- 只在四类情形对外发消息：①1074 出现能量内部极大（逐点表 E 回落）或**连续 3 个相邻点**重原子 Kabsch > 0.3 Å（附三条合成自检）；②1071 出现终态（Normal 或 Error）；③1073 / E3 侧任何**数值被推翻**；④主协调下新口令。
- 其余例行状态读数只在 lane 台账内记录，不发消息、不回执收条。

**B. 判读口径原文复述（防漂移，照录）**：1074 逐点报 R(2,4) / R(25,26) / H26 最近重原子与距离 / R(10,27) / N of 36 / 是否 Optimization completed；相邻点 Kabsch = **20 重原子、SVD、det=+1 禁镜像**，先贴三条自检；峰只作 **TS 候选/上界**、**绝不写 ΔE‡**；引用任何 E3b 能垒必须同时写「**产物区驻点能量跨度 2.0160 kcal/mol**（1028 参照；P −4.3383 / 1073 −2.7297 / 1069 −4.7458）」，产物端锚定 **job 1061 的 P**，不换参照、不混用。

**C. 适用范围申明（需协调方明示，否则按此执行）**：协调方复述里的「峰只在含档 1 视图出现且落档 1 ⇒ 只记『需二维扫描』」是 **E2 口径的原始措辞**（档 1 判据 R(28···H24) ∈ [1.20, 1.50] Å）。在 1074 中**质子维 R(25,26) 本身就是扫描坐标之一**（0.9693 → 2.2193，6 个值），二维网格已覆盖质子转移，故 E2 版「需二维扫描」结论在 1074 上**不照搬**。本道 1074 的执行方式：峰若**仅出现在 R(25,26) ∈ [1.20, 1.50] Å 的格点邻域**，记为「**质子共享区内的上界，需更细网格/另一条路径确认，不作 TS 候选**」；峰若落在 R(25,26) = 0.9693 列（质子仍在 O25）或 R(25,26) ≥ 1.75 列，则按普通「受约束剖面 TS 候选/上界」登记并注明所在列。若协调方另有映射，请在下次触发消息中明示。

**D. 台账现值缺口**：协调方本条写「HI1/PROCESS.md **516 行 / sha256 x**」——**x 为占位符，不是测量值** ⇒ 本道登记为 **missing measurement（未测量）**，不猜、不引用；待其单独给实值后再双签。其此前 515 行 / 860cf440… 为 21:11:58–21:12:08 双签值，仅代表当时。

**E. 状态（本道 21:12:08 实测，仅台账记录、不外发）**：1074 = 30,862 行 / sha 6d2930ca… / Optimization completed 2 / L30234 Step 13/243 格点 3；1071 = 94,257 行 / L93409 Step 90/246，未终态。

**F. 未变项**：只读、零提交 / 零 kill / 不 priority / 不 ts_resume；四条边 result/barrier 全 null；交付面 a2964d8d… / 277 行 + 11 文件 sha、§14、hi.py 不动。
**G. §P.66 D 节缺口闭合（双签）**：协调方补发 **HI1/PROCESS.md = 516 行 / sha256 5642671fbaed938bc3b34cc7518dca6e01f2b536a2d7146f6b54b6064a3e3fd5**（其 21:12:35 实测）；本道 21:12:54 独立实测 **516 行 / 5642671f…** **逐位相同** ⇒ 双签成立，`missing measurement` 撤销。口径：此后台账一律「实测时刻 + 同轮行数 + 当时 sha」三件套，不留占位符。

**H. 同期读数（21:12:54，仅台账记录）**：1074 = 31,047 行 / sha fb03c5157ebe4656f53ec58496d6d931b79f70a6a4e2bf35596b655fc98b64d7，Optimization completed 计数 2，末条 L30234 Step 13/243 格点 3。
### P.67 1074 候选判据正式化（二维鞍点判据，替代 E2 的「档」语言）+ 判据工具就绪 + 网格行值勘误 + PROCESS.md 518 行双签（21:13:21–21:14:13 CST）

**A. 裁定照录（此后 1074 判读唯一口径）**
- E2 的「档 0/1/2 + 含档 1 参照剖面」是**一维扫描**措辞（质子坐标自由弛豫、档位只是事后标签）；1074 是**二维受约束网格**，R(25,26) 与 R(2,4) 每个格点都被冻结 ⇒ **不得把「含档 1 / 排除档 1」两张表搬到 1074**，「质子共享区」只能作描述、不作筛选条件。
- 某收敛格点成为候选须**同时**满足：①沿 R(2,4) 方向（同一质子列内）为**局部极大**（前后点 E 都更低）；②沿 R(25,26) 方向（同一行内）为**局部极小**（左右格 E 都更高）；③自身 `Optimization completed` 且 ①② 依赖的相邻格点**都已收敛**（未收敛点不参与比较、不内插）；④**首/末行与首/末列一律不作候选**（只记「需扩窗」）。
- **两维都极大（山脊顶点）不是候选** ⇒ 分支结论写「该冻结质子路径不对」，改为在该质子值处做 R(2,4) 一维弛豫扫描，或重设质子列；**不得写成 TS 候选**。
- 任何候选仍只是 **TS 候选/上界**：须 opt=(TS,calcfc,noeigen) + freq（**恰 1 虚频且模矢含 C2–N4 与 O25–H26 分量**）+ 双向 IRC 才称 TS；此前**绝不写 ΔE‡**，**E3b barrier 保持 null**；任何单值能垒必须并写「**产物区驻点能量跨度 2.0160 kcal/mol**（1028 参照；P −4.3383 / 1073 −2.7297 / 1069 −4.7458）」，产物端锚定 **job 1061 的 P**。
- 报告骨架：6×6 表（行 = R(2,4)、列 = R(25,26)），每格 E（纯电子，标 SCF 行号）+ 是否 Optimization completed；另附相邻点重原子 Kabsch 矩阵（**20 重原子、SVD、det=+1 禁镜像**，先贴三条自检）；候选格按 ①②③④ 逐条打勾；**不写「档」列**。

**B. 判据工具就绪**：prep/scan2d_candidates.py，sha256 **e6ac3faaba841a9ad566df1e7ea76ba6a7d871e96418ff5f9c68ea928e73769b**。功能：自动取每个 `Optimization completed` 前的末帧算 R(2,4)/R(25,26)/R(4,26)/R(10,27)/R(2,25)/R(2,26)/H26 最近重原子，E 取该点收敛前最后一次 SCF（带行号），映射到 6×6 网格（容差校验：实测 vs 网格值偏差 ≤3e-5 Å），逐点跑 ①②③④ 并输出分支结论；末尾固定打印「受约束剖面（O10–H27 冻结）+ 不写 ΔE‡ + 跨度 2.0160」免责行。

**C. 当前表状态（21:14:13）**：已收敛格点 **2**（L1938 / L18048），均在 **row1 col1** 与 **row2 col1** ⇒ 全部落在**首列**且邻点未齐 ⇒ 按 ③④ **无候选、也无从判峰**（工具逐点打印「boundary ⇒ 需扩窗」与缺失邻点清单）。表内 E：row1col1 −939.312627（SCF L1047）、row2col1 −939.297701（SCF L17649）。

**D. 网格行值勘误（登记，不改冻结文档）**：prep/E3B_SCAN2D_DESIGN.md 写「B 2 4 1.4248→2.2248 @+0.2000 ×5」；按 +0.2000 ×5 实为 **1.4248 → 2.4248（6 个值）**，与日志「on scan point … out of **36**」= 6×6 一致 ⇒ 设计文档末值 2.2248 系笔误（应为 2.4248），列值 0.9693→2.2193（+0.25 ×5）正确。本道按 **2.4248** 建表；文档为冻结资产不修改，仅在此登记勘误。

**E. 双签**：协调方 21:13:21 的 **HI1/PROCESS.md 518 行 / sha256 8df1b77852c483331c07879fe4e9afd61d2c20e402345b631d370d64cbb066b3**，本道 21:13:42 独立实测 **518 行 / 8df1b778…** **逐位相同** ⇒ 双签成立。

**F. 未变项**：四类触发协议不变；只读、零提交 / 零 kill / 不 priority / 不 ts_resume；四条边 result/barrier 全 null；交付面 a2964d8d… / 277 行 + 11 文件 sha、§14、hi.py 不动。
### P.68 1074 判据改为主协调批准版（对称轴指派）+ 判据工具 v2 + 扫描次序声明 + PROCESS.md 520 行双签（21:14:00–21:14:59 CST）

**A. 唯一有效口径（批准版，替代 §P.67 的对称化前版本）**
- **轴指派对称**：候选格点 = 轴向上**一个方向局部极大、另一方向局部极小**，**两种指派都算**；报告**必须声明**是「断键维 R(2,4) 承载能垒」还是「质子维 R(25,26) 承载能垒」。§P.67 写的「R(2,4) 极大 且 R(25,26) 极小」**作废**（会漏掉能垒落在质子维的情形）。
- **两维同为极大**（山脊顶点）⇒ **不是候选**，结论写「在该质子值处改做 R(2,4) 一维弛豫扫描 / 重设质子列」。
- **两维同为极小** ⇒ **盆地格点**，只作能量登记。
- **网格内无满足条件格点** ⇒ 只写「**该 6×6 网格未分辨出离散指标 1 的驻点，需扩窗或加密**」，**不得写「无 TS / 通道不存在」**。
- 不变三条：比较所用相邻格点**均已收敛**；不在**首/末行、首/末列**（边界只记「需扩窗」）；未收敛点单列、**不内插**。
- 效力上限：候选只作 **TS 候选/上界**；须 opt=(TS,calcfc,noeigen) + freq（恰 1 虚频且模矢含 C2–N4 断裂与 O25–H26 转移成分）+ 双向 IRC 才称 TS；期间**不写 ΔE‡**，**E3b result/barrier 保持 null**；任何单值能垒引用必须并写「产物区驻点能量跨度 **2.0160 kcal/mol**（1028 参照；P −4.3383 / 1073 −2.7297 / 1069 −4.7458）」，产物端锚定 **job 1061 的 P**。
- 报告骨架：6×6 表（行 R(2,4)、列 R(25,26)；每格 E + SCF 行号 + 是否 OPT completed + **扫描序号**）+ 相邻点重原子 Kabsch 矩阵（20 重原子、SVD、det=+1、三条合成自检）+ 候选格按上述条件逐条打勾，**不设「档」列**。

**B. 判据工具 v2**：prep/scan2d_candidates_v2.py，sha256 **c2fedf4c2a9275e9314d4ab95aaa292d00658857cc450afe7f2435563437e124**。功能：逐收敛格点输出 scan# / row R(2,4) / col R(25,26) / E + SCF 行号 / OPT 行号 / R(4,26)·R(10,27)·R(2,25)·R(2,26) / H26 最近重原子；6×6 表带 scan#；对称判据逐点判读并给分支（含「ridge vertex ⇒ 非候选 + 分支」「basin ⇒ 仅能量登记」「neighbour 未齐/未收敛 ⇒ 不比」「边界 ⇒ 需扩窗」）；固定打印扫描次序声明与免责行。旧版 prep/scan2d_candidates.py 保留但**不再作为判据依据**（其判据为对称化前版本）。

**C. 当前表（21:14:59）**：收敛格点 2 个 —— scan#1（row1 col1，E −939.312626605 / SCF L1047 / OPT L1938）、scan#2（row2 col1，E −939.297700793 / SCF L17649 / OPT L18048）；两点均在**首列**且邻点未齐 ⇒ **无候选、尚无从判峰**（工具逐点给出缺失邻点 r0c1/r1c0/r1c2 与 r3c1/r2c0/r2c2）。在跑格点块 L32660：R(2,4)=1.8248、R(25,26)=0.9693、R(10,27)=0.9949、H26 → O25 0.9693（未收敛，不入表）。

**D. 扫描次序声明（写入报告，防 36 点误读）**：坐标 1（R(2,4)）**先变** ⇒ **前 6 个格点只覆盖断键维**，**质子维自第 7 点起才展开**；已由日志实证：scan#2 的 R(2,4)=1.6248（+0.2000 递增）而 R(25,26) 仍 0.9693。

**E. 端点自核（协调方要求：端点不作授权值，以日志实测为准）**
- gjf 扫描行：B 2 4 **S 5** 0.2000 / B 25 26 **S 5** 0.2500 ⇒ 每维 5 步 = **6 个值**；日志 L1638 / L18940 均为「… **out of 36**」= 6×6 ⇒ 每维 6 值。
- 由算术：R(2,4) = 1.4248 → **2.4248**（1.4248+5×0.2000）；R(25,26) = 0.9693 → **2.2193**（0.9693+5×0.2500）。
- 主协调给的「R(2,4) 1.4248 → 2.2248」与 +0.2000×5 算术不符（2.2248 = 1.4248+4×0.2，只有 5 个值），且会使总格点变 5×6=30 ≠ 36 ⇒ 本道按 **2.4248** 建表；**经验确认待 scan#6 / #7**（若 scan#6 实测 R(2,4)=2.2248 则说明维数分配与上述不同，届时按实测改写并立刻报触发）。
- 设计文档 prep/E3B_SCAN2D_DESIGN.md 的「→2.2248」同样系笔误（冻结资产，不修改，仅登记）。

**F. 双签**：协调方 21:14:00 的 **HI1/PROCESS.md 520 行 / sha256 6142f815b4d02cbde3de4177d4ad67f44c2c9c43cc5e2c9dbc4b0ababfbbfe1f**；本道 21:14:59 独立实测见上方 bash 输出（行数 + sha 同轮取得），如逐位相同则双签成立、否则按实测值登记并报差异。

**G. 未变项**：四类触发协议不变；只读、零提交 / 零 kill / 不 priority / 不 ts_resume；四条边 result/barrier 全 null；交付面 a2964d8d… / 277 行 + 11 文件 sha、§14、hi.py 不动。
### P.69 端点争议收口（双方独立复算 = 2.4248，2.2248 作废）+ 工具 sha 写入报告方法节 + PROCESS.md 521 行双签（21:15:09–21:16 CST）

**A. 端点定稿**：协调方独立复算与本道一致 —— gjf L50 「B 2 4 S 5 0.2000」、L51 「B 25 26 S 5 0.2500」、L52 「B 10 27 F」（= 日志 L158–L160 回显）；步长 0.2 × 5 步 ⇒ R(2,4) = 1.4248 / 1.6248 / 1.8248 / 2.0248 / 2.2248 / **2.4248**；步长 0.25 × 5 步 ⇒ R(25,26) = 0.9693 / 1.2193 / 1.4693 / 1.7193 / 1.9693 / **2.2193**。**2.2248（= 1.4248+4×0.2，只有 5 个值，总数 5×6=30≠36）作废**；设计文档同误仅登记。

**B. 经验双证（协调方 21:15:30 取扫描点 3 最新几何，块 L32664–L32705、41 行断言通过）**：R(2,4) = **1.8248 = 1.4248+2×0.2**、R(25,26) = **0.9693 未动**、R(10,27) = **0.9949 冻结保持** ⇒ 步长 0.2 与「坐标 1 先变、前 6 点只扫断键维」双证。**收尾确认项**：scan#6 到达时仍须报一次实测 R(2,4)（预期 2.4248）。

**C. 方法节固定写法**：报告方法节必须写判据工具 sha —— **prep/scan2d_candidates_v2.py，sha256 c2fedf4c2a9275e9314d4ab95aaa292d00658857cc450afe7f2435563437e124**；旧版 prep/scan2d_candidates.py 不再引用。

**D. 状态（协调方 21:15:30 实测，仅台账记录、不作判读）**：日志 33,014 行 / sha 0729b8807e8438e013cbb5f1749f658e08f7e25f9ac219c2dc71be47b0505b66、Optimization completed 2、scan point 3 Step 15/243、最新 SCF L32987 −939.253778012（过程读数，不入表）；收敛 2 点均在首列、邻点未齐 ⇒ 暂无候选、无从判峰（与本道判断一致）。

**E. 双签**：协调方 21:15:50 的 **HI1/PROCESS.md 521 行 / sha256 f4dbc95ccc49fb3bbc922d9c92a45135e63fa3181f14736d2f41f76c072c1d60**；本道 21:16 同轮 wc -l + sha256sum 实测见 bash 输出，逐位相同则双签成立。
(本节及其后 P.71 插入于 §P.69 E 之后；下方仍保留的「F. 未变项」一行属 §P.69 原文)

### P.71 双签改钉 522 行 / 4250d884…；scan#6 报数基准定于「该点收敛块」；流程收敛为四类事件（21:16:26–21:17 CST）

**A. 双签改钉**：协调方 21:16:26 的编辑取代 521 行版，现值 **HI1/PROCESS.md 522 行 / sha256 4250d88471d72784d8104a4f1d34235fa4614d5b68870bc171373f3ad13e42e9**；本道 21:16:59 独立实测 **522 行 / 4250d884…** **逐位相同** ⇒ 双签成立。**521 行那版作废**（内容为超集关系、无数字改动，仅行数与标识符变化）。新增三块内容照录性质：通则「S n step ⇒ n+1 取值；步数与取值个数是两件事；总点数须与 out of N 自洽（含三例反例）」+「scan#6 收尾承诺」+「1075 格点 2 仅作纯电子登记」。

**B. 端点（已收口，双方一致）**：R(2,4) 六值 1.4248 / 1.6248 / 1.8248 / 2.0248 / 2.2248 / **2.4248**；R(25,26) 六值 0.9693 / 1.2193 / 1.4693 / 1.7193 / 1.9693 / **2.2193**；设计文档同误仅登记、不动冻结文件。

**C. scan#6 报数基准（时序澄清，照录执行）**：因**坐标 1 先变**，「on scan point 6 out of 36」字样出现时，scan#6 的几何已是 R(2,4)=2.4248、R(25,26) 仍 0.9693；而「scan#6 收敛」要等 `Optimization completed` 计数到 **6**。⇒ **以「该点收敛块」为报数基准，不以出现 scan point 6 字样为基准**。预期 R(2,4)=2.4248；**若不符则停下报主协调、不 kill**。

**D. 方法节工具 sha（固定）**：prep/scan2d_candidates_v2.py，sha256 **c2fedf4c2a9275e9314d4ab95aaa292d00658857cc450afe7f2435563437e124**；旧版不引用，判读与引用只认这一版。

**E. 流程收敛（广播 evt_2e1a84d0cf7b4f2d，21:17 CST）**：①收到口径/裁定/勘误**不再发收条**，直接按已确认口径执行；②只在四类事件发帖 —— 作业终态（三件套 + 逐字终止行 + 行号 + 判读）／新作业提交（job id / started_at / 输入 sha / 门控读数）／发现假象或需重出种子（先报再动）／blocked / 崩溃 / 工具拒绝；③每帖自带「绝对路径 + sha256 + 行数或行号 + 本机 date -Is 实测时刻」；④分工与门槛不变（E2 出表方 as_b8536002aacb48e3；1074 判据 §R137 批准版；1074 ≥4 收敛格点才做叠合判读；1073 freq 已收口）；⑤关键待办只剩三件：**1074 格点推进（第 7 点起质子维展开）**、**1071 终态四档判读**、**E2 ≥3 收敛帧出表（非本道）**，其余只读静默。

**F. 本道轮询改为事件驱动**：触发点由「scan point 4」改为「**scan point 7 出现**（蕴含 scan#6 已收敛）或 **1071 终态**」，加 3600 s 兜底；减少无效唤醒。

**G. 边界**：只读、零提交 / 零 kill / 不 priority / 不 ts_resume；四条边 result/barrier 全 null；交付面 FINAL_DELIVERY_DRAFT.md a2964d8d… / 277 行 + 11 文件 sha、§14、hi.py 不动。
### P.72 1074 scan#3 入表（E 仍单调上升、无峰）；1071 未终态（21:35:50 CST，例行记录、不对外发帖）

**A. 快照三元组**
- 1074 /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/runs/e3b_scan2d_c2n4_o25h26.log：**21:35:50 / 51,086 行 / sha256 adaef34641372e26ca07c98fb3d439d2420148873e05d28b6ddc7580af9a82f6**；Optimization completed 计数 **3**；末条 L50270 "Step number   3 out of a maximum of  243 on scan point     4 out of    36"
- 1071 ts/ts_0020/jobs/declaration_0001/ts_opt/refine.log：**113,264 行 / sha256 13456dd88a4dda5d0794407c0426ab6941f8a8f2879e5730a6a4a013726cc746**；L112349 "Step number 109 out of a maximum of  246"；无 Optimization stopped / NStep= / Normal / Error 行 ⇒ **未终态**

**B. 入表（判据工具 prep/scan2d_candidates_v2.py，sha c2fedf4c…）**
| scan# | row R(2,4) | col R(25,26) | E (SCF 行) | OPT 行 | R(4,26) | R(10,27) | R(2,25) | R(2,26) | H26 最近重原子 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1.4248 | 0.9693 | −939.312626605 (L1047) | L1938 | 3.1829 | 0.9949 | 1.4728 | 2.0398 | O25 0.9693 |
| 2 | 1.6248 | 0.9693 | −939.297700793 (L17649) | L18048 | 3.3096 | 0.9949 | 1.4296 | 1.9986 | O25 0.9693 |
| 3 | 1.8248 | 0.9693 | **−939.275890059 (L47045)** | **L47458** | 2.9709 | 0.9949 | 1.3967 | 1.9547 | O25 0.9693 |
- ΔE vs 1028（−939.312626605）：scan#1 +0.00、scan#2 +9.37、scan#3 **+23.06** kcal/mol（纯电子差；非 ΔE‡、不作分母）

**C. 判读（按 §R137 批准版判据，逐条）**
- ①沿 R(2,4)：E 单调上升（+0.00 → +9.37 → +23.06）⇒ scan#3 尚非局部极大（仍需 scan#4 更低才成峰）；②沿 R(25,26)：三个格点同列 0.9693，行内无左右邻点 ⇒ ②无从判；③邻点未齐（scan#3 缺 r4c1 / r3c0 / r3c2）；④三点全在**首列** ⇒ 边界，只记「需扩窗」。⇒ **无候选**（与工具输出一致）。
- 危险信号检查：H26 最近重原子恒为 **O25、0.9693 Å**（在 0.95–1.35 Å 内，未悬空）；**R(10,27) 恒为 0.9949**（冻结保持）；扫描坐标 1 逐点 +0.2000 递增、无反向；坐标 2 未展开（符合前 6 点只扫断键维）。**无 R(4,26) 类附加观察触发条件**（R(4,26) 3.1829 → 3.3096 → 2.9709 属非单调变化，但不是扫描坐标、且 H26 仍归属 O25 ⇒ 仅记录）。

**D. 按 21:17 流程收敛指令**：本条为**例行记录**，不对外发帖（未达四类事件之一）。
### P.73 巡检（21:36:51 CST）：1071 未终态但能量已大幅回落；1074 scan#4 在跑（例行记录，不对外发帖）

**A. 1071（ts_0020 / E3b attempt 2）**：114,183 行 / sha256 **1f6c2a1d5b5675002117df28b85c0fa0ade6dc95839b57bd92ab5b8617ac6378**；L113325 "Step number 110 out of a maximum of  246"；末次 SCF **L113237 −939.308432376（12 cycles）**；无 Optimization stopped / NStep= / Normal / Error 行 ⇒ **未终态**。
- **与既有登记的关系（重要，需在终态判读时并写）**：§P 早条目记录的「Step 22 起把 H27 从 O10 拉向 N4、能量约高于 1028 **67 kcal/mol**」（−939.205768714）只代表**当时的过程帧**；到 Step 110 末次 SCF 已降至 **−939.308432376**，即相对 1028（−939.312626605）**+0.004194229 Ha = +2.63 kcal/mol**（纯电子差、非 ΔE‡、不作分母）。⇒ 早前「走声明外 N4 质子化高能区」的判断**只对早期步段成立**，终态判读必须以终态帧几何（尤其 O10–H27 与 H27 最近重原子）为准，不得沿用 Step 22 的读数。

**B. 1074**：52,015 行 / sha256 **3463dab15e7e9e2adb2b8162c8191ac5fb3607b4c26948ec75119970a464d58c**；Optimization completed 计数 **3**；L51218 "Step number   4 out of a maximum of  243 on scan point     4 out of    36"；末次 SCF L51130 **−939.253671055**（过程读数、不入表）⇒ 相对已入表的 scan#3（−939.275890059）仍**继续上升**，尚无峰。

**C. 事件判定**：本条无终态、无新提交、无假象、无 blocked ⇒ **不对外发帖**，仅台账记录（依 21:17 流程收敛指令第 2 条）。

**D. 下一步**：继续事件驱动轮询（1071 终态 / 1074 scan#6 收敛或 scan point 7 出现）；1071 一旦终态即按四档判读（三件套 + 逐字终止行 + 末帧几何三类 minsep + O10–H27 关键判据 + 若进 freq 段则 39 组×3=117 与虚频/投影），**先报 as_a341823c436e47ed（post 首行 to:）与 as_ec848a7673b74e35（call），再落台账**。
### P.74 巡检（21:54:24 CST）：1074 已入 5 点（断键维单调上升 +48.83 kcal/mol、仍无峰）；1071 Step 125 能量已降至 1028 以下（例行记录，不对外发帖）

**A. 快照三元组**
- 1074：**68,430 行 / sha256 d0516a027d660307e37a80b2d915829676a1f5ccd475f9767879222895d25cf7**；Optimization completed 计数 **5**；末条 L67599 "Step number   4 out of a maximum of  243 on scan point     6 out of    36"；末次 SCF L67511 −939.219750272（过程读数、不入表）
- 1071：**130,656 行 / sha256 5631d3b76e07e50b4ebb02a2475af46715dd25090e95c3011084bc0f8ec6db35**；L129792 "Step number 125 out of a maximum of  246"；末次 SCF **L129705 −939.318709484**；无终止行 ⇒ 未终态

**B. 1074 已入表 5 点（工具 prep/scan2d_candidates_v2.py，sha c2fedf4c…）**
| scan# | R(2,4) | R(25,26) | E | SCF/OPT 行 | R(4,26) | R(10,27) | R(2,25) | R(2,26) | H26 归属 | E−1028 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 1.4248 | 0.9693 | −939.312626605 | L1047 / L1938 | 3.1829 | 0.9949 | 1.4728 | 2.0398 | O25 0.9693 | +0.00 |
| 2 | 1.6248 | 0.9693 | −939.297700793 | L17649 / L18048 | 3.3096 | 0.9949 | 1.4296 | 1.9986 | O25 0.9693 | +9.37 |
| 3 | 1.8248 | 0.9693 | −939.275890059 | L47045 / L47458 | 2.9709 | 0.9949 | 1.3967 | 1.9547 | O25 0.9693 | +23.06 |
| 4 | 2.0248 | 0.9693 | −939.253685365 | L56634 / L57043 | 3.0722 | 0.9949 | 1.3749 | 1.9395 | O25 0.9693 | +36.99 |
| 5 | 2.2248 | 0.9693 | −939.234828574 | L63426 / L63824 | 3.1740 | 0.9949 | 1.3559 | 1.9253 | O25 0.9693 | **+48.83** |
（kcal/mol，纯电子差、非 ΔE‡、不作分母）
- **判读**：沿 R(2,4)（同一质子列 0.9693）E **逐点上升、无回落** ⇒ 断键维在固定质子位置上是**纯上坡**，5 点内**无峰**；行内（R(25,26)）仍只有单列 ⇒ 无法判行内极值；5 点全在**首列** ⇒ 边界，只记「需扩窗」。⇒ **无候选**。
- 危险信号：H26 全程挂 **O25 0.9693 Å**（未悬空）；**R(10,27) 全程 0.9949**（冻结保持）；坐标 1 逐点 +0.2000 无反向；坐标 2 未展开（符合前 6 点只扫断键维）。R(4,26) 3.1829→3.3096→2.9709→3.0722→3.1740（非单调、非扫描坐标，仅记录）；R(2,26) 2.0398→1.9253 单调减小（H26 与 C2 距离略微远离，仍属 O25 归属）。

**C. 1071（attempt 2）能量轨迹更新（关键，终态判读时必须并写）**：Step 22 时 −939.205768714（约高于 1028 **+67 kcal/mol**）→ Step 110 −939.308432376（+2.63）→ **Step 125 −939.318709484**，即相对 1028（−939.312626605）**−0.006082879 Ha = −3.82 kcal/mol**（低于 1028），相对 P（job 1061，−939.319540184）**+0.000830700 Ha = +0.52 kcal/mol**（纯电子差、非 ΔE‡、不作分母；参照显式 = job 1061 的 P）。⇒ 该轨迹已**下行进入产物侧能量区**，早前「N4 质子化高能区」只描述早期步段；**是否落入 P 盆 / 是否收敛到鞍点，须以终态帧与（若进 freq 段）虚频判据定**，不得据中间能量断言。

**D. 事件判定**：无终态、无新提交、无假象、无 blocked ⇒ 不对外发帖（21:17 流程收敛指令第 2 条）。继续等 scan#6 收敛（届时报实测 R(2,4)，预期 2.4248）与 1071 终态。
### P.75 1071 独立复核：双质子穿梭 + P 型产物区极小（InChIKey 相符）；协调方四条判读登记；PROCESS.md 531 行双签（21:55–21:56 CST）

**A. 本道独立实测（21:55:56–21:56:03，取的是比协调方更新的一态）**
- /home/ly/Cloudra-mechanism-agent/ts/ts_0020/jobs/declaration_0001/ts_opt/refine.log：**132,456 行 / sha256 f3960d5646a36a6bf7307f3a8edfafcdbe0f0eec54401aa1430d6324415d0c8b**；L131716 "Step number 127 out of a maximum of  246"；末次 SCF **L131629 −939.319805916（11 cycles）**；termination 关键字计数 **0** ⇒ 未终态。
- 能量（纯电子差、非 ΔE‡、参照显式 = **job 1061 的 P**）：相对 1028（−939.312626605）**−0.007179311 Ha = −4.52 kcal/mol**；相对 P（−939.319540184）**−0.000265732 Ha = −0.17 kcal/mol（已低于 P）**。
- 末帧（最后 orientation 块 **L132271**，41 原子，C15H21N1O4）：**C2–N4 3.4244（断）**、**C2–O25 1.2263（C=O）**、N4–H26 3.0458、O25–H26 1.8579、C9–O10 1.3393、**O10–H27 2.9268**、**N4–H27 1.0324**、**O10–H26 0.9671**、C9–O11 1.2090；**H26 最近重原子 = O10（0.9671 Å）**、**H27 最近重原子 = N4（1.0324 Å）**。
- 物种身份（RDKit DetermineBonds + 标准 InChI）：**InChIKey = SMPZMOQIWMNUBG-YBVIJTQESA-N**（与声明 P 逐字符相同）；片段 **24 + 17**；重原子键 **20**。
⇒ **双质子穿梭成立**：原 O25–H26 的质子落到 **O10**，原 O10–H27 的质子落到 **N4**；净结果与声明产物**同物种**，但质子归属经由 H27 中继完成，不是声明中「O25–H26 直接去 N4」那条路径。
- 与协调方读数的关系：其 21:54:57 态（131,517 行 / cfb44929…，末帧块 L131319：C2–N4 3.4462、C2–O25 1.2264、H26→O10 0.988、H27→N4 1.0101）与本道 21:56:03 态（132,456 行 / f3960d56…，块 L132271：3.4244 / 1.2263 / 0.9671 / 1.0324）为**同一轨迹的前后两态**，判读一致、无冲突；其 L129705 −939.318709484 与本道 Step 125 读数逐位相同。

**B. 登记协调方四条判读（照录，本道执行）**
1) 1071 **已落入 P 型产物区极小，不是鞍点** ⇒ 任何终态都**不得报 TS**，也不得据中间能量写 ΔE‡。
2) 其 20:xx 的「1071 整体处于声明外 N4 质子化高能区、比 1028 高 67 kcal/mol 量级」**作废**，改为「**早期步段（≈Step 22–110）处于 N4 质子化高能区，Step 125 后经质子穿梭进入 P 型盆地**」。本道 §P.73/§P.74 的同类表述同此限定。
3) 失败类别按四档登记为「**产物侧滑移（P 型极小，非鞍点）**」。
4) 终态若再出 l9999 / 超步，**只作失败登记、不回填任何 barrier**；E3b result 保持 null。

**C. 产物区驻点能量跨度**：最负仍为 1069 末帧 **−4.7458**（vs 1028），1071 现态 −4.52、1073 −2.7297、P −4.3383 ⇒ **跨度 2.0160 kcal/mol 不变**（1071 未扩展跨度）。

**D. 双签**：协调方 21:55 的 **HI1/PROCESS.md 531 行 / sha256 28f259e74fe98e2cad0f4f5c7feec45f5d08b43948008e7afd04fb1b65ca98bc**；本道 21:56:03 独立实测 **531 行 / 28f259e7…** **逐位相同** ⇒ 双签成立。

**E. 边界**：只读、零提交 / 零 kill / 不 priority / 不 ts_resume；四条边 result/barrier 全 null；交付面 a2964d8d… / 277 行 + 11 文件 sha、§14、hi.py 不动。继续等 1071 终态（四档判读）与 1074 scan#6。
### P.76 报告新增三项（双质子路径并列 / 未完成项首位 / 不猜第三起点）+ 跨度看护挂钩 + 本道 P.75 算术更正（21:56:51 CST）

**A. 报告必须新增（照录，主协调 evt_afc6b8641e214994，协调方转达）**
1) **机制结论（新增）**：**同一物种可由两条质子路径到达** —— ①**H26 直接转移**至 N4（1069 末帧 / P / 1073 三者同 InChIKey = SMPZMOQIWMNUBG-YBVIJTQESA-N）；②**H27 中继双穿梭**（原 O10–H27 的质子去 N4、原 O25–H26 的质子落到 O10；1071）。⇒ 声明中「O25–H26 直接转移至 N4」**不是唯一可达路径**；报告须**并列两条路径与各自证据**（几何 + InChIKey）。
2) **未完成项首位（新增，与产物区跨度并列、同为 E3b 收口前置）**：**E3b 若要给能垒，必须先裁定声明的是哪一条质子路径（直接转移 vs 双穿梭中继）**；否则鞍点归属不确定、ΔE‡ 无意义。**裁定权在主协调、不在出表方**。
3) **产物区跨度维持 2.0160 kcal/mol**：四点相对 1028 —— P **−4.3383** / 1073 **−2.7297** / 1071 当前 **−4.505** / 1069 末帧 **−4.7458**；min −4.7458、max −2.7297、算术差 2.0161 → **对外口径仍 2.0160**；参照锚定 **job 1061 的 P**，**不扩窗**。
4) **路线结论（写入「下一步」节）**：已两次 guess 失败（v7/1069 预挂 N4 → 产物盆；v8/1071 双穿梭 → 产物盆）⇒ 按 scan-first 规则**不得再猜第三个起点**；E3b 全部希望压在 **1074**；若 1074 整表无「一轴局部极大 + 另一轴局部极小」格点，下一步是**加密网格（R(2,4) 1.8–2.0 Å 区段 × 质子 0.1 Å）**，而**不是第三个 guess**。

**B. 跨度看护挂钩（本道挂上，已写入轮询判据）**：**若 1071 继续下探并低于相对 1028 的 −4.7458（即 1069 末帧），跨度声明必须重算并公开勘误**。当前判据值：
- 1071 态①（协调方 21:56:28 读，132,537 行 / sha 44765ce8…）：L131629 −939.319805916 ⇒ **−4.5051** vs 1028、**−0.1667** vs P
- 1071 态②（本道 21:56:51 读，**132,608 行 / sha256 622abd4103d7225ea263fad88a9f6a4e2e215aa44be74c15f252e58385f2122d**，L131716 Step 127/246，末次 SCF **L132581 −939.319861206**）⇒ **−4.5397** vs 1028 ⇒ **距跨度地板 −4.7458 仅剩 0.206 kcal/mol**，**尚未破**（break = False），但逼近速度快，下一次巡检必须重算。

**C. 本道算术更正（§P.75 一条）**：§P.75 A 节把 1071 态①写成「−4.52 vs 1028」系四舍五入笔误，**正确值 −4.5051**（协调方 −4.505 为准）；−0.17 vs P 即 −0.1667，无误。

**D. 双签**：协调方 21:56 的 **HI1/PROCESS.md 532 行 / sha256 625db3093c604b3f769d0d6a15a8c8d72d81f67f3f8b30fede74388f4f293366**；本道 21:56:51 独立实测 **532 行 / 625db309…** **逐位相同** ⇒ 双签成立。

**E. 边界**：只读、零提交 / 零 kill / 不 priority / 不 ts_resume；E3b 及四条边 result/barrier 全 null；交付面 a2964d8d… / 277 行 + 11 文件 sha、§14、hi.py 不动。

**E. 边界**：只读、零提交 / 零 kill / 不 priority / 不 ts_resume；四条边 result/barrier 全 null；交付面 a2964d8d… / 277 行 + 11 文件 sha、§14、hi.py 不动。

**E. 边界**：只读、零提交 / 零 kill / 不 priority / 不 ts_resume；四条边 result/barrier 全 null；交付面 a2964d8d… / 277 行 + 11 文件 sha、§14、hi.py 不动。

**E. 边界**：只读、零提交 / 零 kill / 不 priority / 不 ts_resume；四条边 result/barrier 全 null；交付面 a2964d8d… / 277 行 + 11 文件 sha、§14、hi.py 不动。

**F. 未变项**：四类触发协议不变；只读、零提交 / 零 kill / 不 priority / 不 ts_resume；四条边 result/barrier 全 null；交付面 a2964d8d… / 277 行 + 11 文件 sha、§14、hi.py 不动。

## P.77 2026-10-17 21:59 — 巡检快照（1074 第 6 点仍在步进；1071 在产物盆内振荡且未终止）

**A. 快照三元组（实测，非估计）**
- 1074 日志 `gold_finish_20261015/HI1/E3/runs/e3b_scan2d_c2n4_o25h26.log`：2026-10-17T21:59:04+08:00 实测 **73,042 行 / sha256 1c09be041fe35d7d5155199a68c04944d4b88c401d3a2b28863ddfdf55eae0d2**（前一态 21:58:09 为 72,120 行 / 258501647de541420bdcdc0bad0e9fd4c6a62678a40af657c29d6b8390b3c8d8）
- 1071 日志 `ts/ts_0020/jobs/declaration_0001/ts_opt/refine.log`：同一时刻 **134,525 行 / sha256 0a20a6743f8ca943258e71e72e78b4395667ab224b43472b458c5aa4e011894d**（前一态 21:58:09 为 134,346 行 / 5f1935fb194fef7f9748b59e46effb56b3550244b6e3d6fc481f440aaf3b365f）

**B. 1074 判读（约束剖面，仅 TS 候选/上界）**
- 扫描第 6 点仍在优化：L72289 = `Step number   9 out of a maximum of  243 on scan point     6 out of    36`；末次 SCF L72201 **−939.219797952** ⇒ 相对 1028 **+58.2509** kcal/mol（相对 P +62.5892）
- `Optimization completed` 计数仍为 **5**；已收敛 6×6 表未变（scan#1…scan#5：R(2,4)=1.4248/1.6248/1.8248/2.0248/2.2248，R(25,26)=0.9693，E 单调上升无峰）
- 方向自检：末块 R(2,4)=2.4248（与预期终值一致）、R(25,26)=0.9693、R(10,27)=0.9949 冻结、H26 最近重原子 O25 0.9693 Å
- 判据（对称版 c2fedf4c…）：已收敛 5 点全部落在边界行/边界列 ⇒ 记为 needs-wider-window，**非候选**；本表目前无「一轴局部极大 + 另一轴局部极小」格点；质子维度 R(25,26) 自格点 7 起展开，尚未到达

**C. 1071 判读（未终止）**
- 终止关键字（Normal termination / Error termination / Number of steps exceeded / Optimization stopped）计数 **0**；L133627 = `Step number 129 out of a maximum of 246`；末次 SCF L134498 **−939.319088718** ⇒ 相对 1028 **−4.0550**、相对 1061 的 P **+0.2833** kcal/mol
- 轨迹判定不变：运行已在 P 型产物盆内振荡（早前态 L132581 −4.5397、L133540 −3.4103、当前 −4.0550），**始终未低于跨度地板 −4.7458** ⇒ 跨度声明 2.0160 kcal/mol（参照 job 1061 的 P）**不触发勘误**；1071 仍不得报为鞍点、不得由此反推 dE-double-dagger

**D. 边界**：只读；零提交 / 零 kill / 不 priority / 不 ts_resume；四条边 result/barrier 全 null；交付面 a2964d8d… / 277 行 + 11 文件 sha、§14、hi.py 不动。

## P.78 2026-10-17 22:05–22:08 — 1074 scan#6 落地 + 1071 破跨度地板（快照值）+ 主协调「双口径」裁定落账

**A. 快照三元组（实测，同一命令内取，非估计）**
- 实测时刻：`date -Is` = **2026-10-17T22:04:50+08:00**
- 1074 `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/runs/e3b_scan2d_c2n4_o25h26.log`：**78,009 行 / sha256 2b71bb91ad987f0a695d6b14bd6eedc12199e796d781c8a2f9fd2b2e6e78b70d**（前态 22:04:11 为 77,174 行 / f01098ed…，与主协调 22:04:12 的 77,174 行同一前态）
- 1071 `/home/ly/Cloudra-mechanism-agent/ts/ts_0020/jobs/declaration_0001/ts_opt/refine.log`：**139,238 行 / sha256 d4b09fb1f352752dac5807fe99f74bd838e0ce7549b05f50b2513a535e777d1b**（前态 22:04:11 为 139,157 行 / b16eb53e…）

**B. 1074 scan#6 落地（判据工具 prep/scan2d_candidates_v2.py，sha c2fedf4c…）**
- `Optimization completed.` 计数 = **6**；scan#6 收敛块 L74409 = ` Optimization completed.`（L74410 = `-- Stationary point found.`），能量 L74000 = `SCF Done:  E(RB3LYP) =  -939.219797518     A.U. after    7 cycles` ⇒ **+58.2511 kcal/mol vs 1028**
- scan#6 坐标（实测）：**R(2,4) = 2.4248 Å = 预期终值**（非假象类事件）、R(25,26) = 0.9693、R(4,26) = 3.2957、R(10,27) = 0.9949（冻结值，在 0.9949±0.03 内）、R(2,25) = 1.3345、R(2,26) = 1.9102、H26 最近重原子 O25 0.9693 Å
- 已收敛 6 点全在 R(25,26)=0.9693 列，R(2,4) 1.4248→2.4248 能量单调升：−939.312627 / −939.297701 / −939.275890 / −939.253685 / −939.234829 / −939.219798（**无峰**）；row6/col1 属边界 ⇒ **needs-wider-window，非候选**
- 质子维展开已核实：scan point 7 首块 L75316 = `Step number   1 out of a maximum of  243 on scan point     7 out of    36`，R(25,26) = **1.2193**、R(2,4) 保持 2.4248；当时 L77235 Step 3/243、末次 SCF L77147 = −939.188355214

**C. 1071 破跨度地板（只作快照值，不作驻点）**
- 未终止：终止关键字（Normal termination / Error termination / Number of steps exceeded / Optimization stopped）计数 **0**；L138411 = `Step number 134 out of a maximum of  246`
- 末次 SCF L138324 = `SCF Done:  E(RB3LYP) =  -939.321143221     A.U. after   11 cycles` ⇒ vs 1028 **−5.3443**、vs **job 1061 的 P** **−1.0059**、比 1069 末帧（−939.320189491 / −4.7458）再低 **−0.5985** ⇒ **跌破跨度地板 −4.7458**
- 能量在 −939.3186…−939.3211 间振荡（L135458 −939.318652537 / L136415 −939.321046274 / L137374 −939.320535988 / L138324 −939.321143221），末帧几何仍为产物型（C2–N4 3.4135 / C2–O25 1.2326 / N4–H27 1.0299 / O10–H26 0.9874，InChIKey SMPZMOQIWMNUBG-YBVIJTQESA-N，fragments 24+17）⇒ **未收敛轨迹帧，不得当驻点、不得反推 ΔE‡**

**D. 主协调 22:05 裁定（post evt_1c7a8750907c448a）：跨度双口径，本道全部后续写法按此执行**
1. **主口径（报告正文 + 任何能垒引用）= 1.6086 kcal/mol**：只用**频率验证的产物极小**（P/job 1061 −4.3383、1073 −2.7297，均 0 虚频、同 InChIKey SMPZMOQIWMNUBG-YBVIJTQESA-N），不随作业推进变化（1.6086 = −2.7297 − (−4.3383)）。
2. **参照不确定度声明（必写）= ≥1.6 kcal/mol，且「暂不封顶」**：因存在未验证的更低产侧读数（1069 末帧 −4.7458、1071 当前帧 −5.3443，仍在步进/振荡）⇒ **P 不是产物区最低点**。
3. **本道 2.6146 只能作为「快照值」**：须带实测时刻 **22:04:50 CST** 与日志 sha **d4b09fb1… / 139,238 行**、标明「含未验证轨迹帧、随作业推进可变」、**不得进任何能垒分母或差值运算**、与主口径并列而非替代。
4. 本道 22:04 的帖子 evt_e247b6e33d314c17 中「新口径 2.6146」一语**按本条改称「快照值 2.6146」**，主口径即为 1.6086 + 不确定度 ≥1.6（不封顶）。
5. 主协调同意 1071 判读（未收敛轨迹帧 / P 型产物盆 / 不得反推 ΔE‡），并核实 1074 scan#6 全部读数（与其 22:04:12 的 77,174 行前态一致）。其 LEDGER §R146 已落。

**E. 下一步（主协调指定）**：只看 1074 第 2 列（质子维 R(25,26) = 1.2193）是否出现「一轴局部极大 + 另一轴局部极小」格点；出现即报主协调，走 ts_prepare/ts_resume，**不得手工提交**。

## P.79 2026-10-17 22:09–22:12 — 主协调 22:05/22:09 裁定全采纳 + job 1069 终态双签 + scan#7 轨迹实测

**A. 快照三元组（实测 2026-10-17T22:09:08+08:00，同一命令内取）**
- 1069 `/home/ly/Cloudra-mechanism-agent/ts/ts_0019/jobs/declaration_0001/ts_opt/refine.log`：**223,328 行 / sha256 f09d1e99e239db287f2a612fd6d0a85ed46ef4cd78bc52915ddfa926be93d130**（与主协调逐位相同 ⇒ 双签）
- 1071 `/home/ly/Cloudra-mechanism-agent/ts/ts_0020/jobs/declaration_0001/ts_opt/refine.log`：**142,095 行 / sha256 ca224fb1621aa0481df361cdf0e80ef5cf738fb3c94c47c3499c9760f5db741b**
- 1074 `gold_finish_20261015/HI1/E3/runs/e3b_scan2d_c2n4_o25h26.log`：**80,132 行 / sha256 7fc7568191122adecdc08032e4933ff6fd62cff2fa067e2ffbfac48bdb78f163**

**B. 跨度口径（主协调 22:05 evt_1c7a8750907c448a + 22:09 evt_cd7054e9563c4041 裁定，三条并列、缺一不可）**
1. 已验证极小间跨度 = **1.6086 kcal/mol**（job 1061 的 P −4.3383 vs 1073 −2.7297；均 0 虚频 39×3=117、InChIKey 同 SMPZMOQIWMNUBG-YBVIJTQESA-N）
2. 产物端参照不确定度 **≥1.6 且暂不封顶**（1069 末帧 −4.7458、1071 最低瞬时 −5.3443）⇒ P 不是产物区最低点
3. **质子路径待裁定**（H26 直接转移 vs H27 中继双穿梭，同一 InChIKey）
- **2.6146 作废为「跨度」**：只可写「截至 22:06 的**瞬时读数跨度 ≈2.6145** kcal/mol（含未验证轨迹帧、随 1071 变动、非不变量）」；本道以 k=627.5095 复算 = **2.61451**，与主协调脚本 2.61448 差 0.00003（k/舍入噪声），**不构成新事实、不并列**

**C. job 1069（ts_0019）终态登记（本道独立复读，逐位与主协调一致）**
- 逐字：L222267 = `Optimization stopped.`；L222268 = `   -- Number of steps exceeded,  NStep= 239`；L223324 = `Error termination request processed by link 9999.`；L223325 = `Error termination via Lnk1e in /home/ly/g16/l9999.exe at Sat Oct 17 20:38:52 2026.`；Step 239/239 用尽、SCF 239 次、末次 L221880 = −939.320189491 ⇒ **−4.7458 vs 1028（其自身最低）**
- 末帧（hdr L222765，41 原子 C15H21N1O4；prep/check_1069_lastframe.py sha256 **1f2257522c865f8e8d1d091b1785b7d0a82223f46095ea1c14110279a92298bc**）：C2–N4 **3.2912**、C2–O25 **1.2156**、N4–H26 **1.0216**、O25–H26 **2.9640**、O10–H27 **1.0118**、N4–H27 **1.7285**；H26 最近重原子 N4 1.0216（次近 O28 1.9413）、H27 最近重原子 O10 1.0118（次近 N4 1.7285）
- 登记档：**max-cycle 终止 + 产物型几何（H26 直接转移支）**；**非驻点、无频率、不得当驻点、不得反推 ΔE‡**

**D. 1071 判读更正：是振荡，不是下降**
- 未终止（终止关键字 0，L141285 = `Step number 137 out of a maximum of  246`）；SCF 序列 vs 1028：L134498 −4.0550 / L135458 −3.7813 / L136415 −5.2834 / L137374 −4.9632 / **L138324 −5.3443（最低瞬时）** / L140242 −4.2638 / L141198 −3.1447
- 统一表述：「在 **−3.14 ~ −5.34** 间振荡、最低瞬时 −5.3443、仍在优化、非驻点」；本道 22:04 帖与主协调 §R145/R146 的「仍在下降」一并作废

**E. 1074 遍历次序与表格规则（采纳主协调更严格版）**
- 实测（prep/scan7_trace.py sha256 **b2aec8dff8d41004a58ab6883fa6694b699c5f115ffb05625673f077dfdc4514**）：scan#7 连续 6 步 R(2,4) 恒 **2.4248**、R(25,26) 恒 **1.2193** ⇒ 自上一格点几何**续接推进**，非「第一维归零重扫」；原句「第 2 列自第 7 点展开」改为「**第 7 点 = (2.4248, 1.2193)，列内行方向待 scan#8 确认**」
- **6×6 表每格必须标 scan# + 实测 (R(2,4), R(25,26))**，禁止按序号推 (row,col)；未收敛/坐标未确认留空
- scan#7 现状：`Optimization completed` 计数仍 6，L79215 = `Step number   5 out of a maximum of  243 on scan point     7 out of    36`，末次 SCF L80105 −939.188960974 ⇒ **+77.60 vs 1028**；R(4,26) 单调降 3.2986 → 3.2264 → 2.9260 → 2.8926 → 2.6659 → 2.6152（H26 正向 N4 迁移），R(10,27) 六步恒 0.9949；收敛前只登记趋势，不内插、不 kill
- 预案：scan#8 若 R(2,4)→2.2248 ⇒ **蛇形**，沿用 §R137 四邻判据；若仍 2.4248 且 R(25,26) 再增 ⇒ **路径式**，相邻点改「路径前后各 1 个已收敛点」、候选条件「沿路径局部极大且两侧路径方向均下降」，并禁用「两维同极大/同极小」网格语言

**F. 边界**：只读；零提交 / 零 kill / 不 priority / 不 ts_resume（TS 走 ts_prepare/ts_resume 由主协调放行）；未触碰 ts_0015 / ts_0016；四条边 result/barrier 全 null；交付面 a2964d8d… / 277 行 + 11 文件 sha、§14、hi.py 不动。

**G. 已发帖**：evt_e247b6e33d314c17（22:04 事件类 3）、evt_54f89a0b6e2f464b（22:09 回裁定，parent evt_cd7054e9563c4041，含上列全部双签读数）。

## P.80 2026-10-17 22:10–22:13 — 主协调 22:10:48 判据（含追加④）全采纳 + scan2d_candidates_v3 落地 + post-freeze 汇总核对（仅 1 处需改）

**A. 判据（22:10:48 裁定，逐条写入本道执行面）**
1. 「沿路径局部极大」必须同时报 (a) 两侧路径方向是否都下降、(b) 两侧点是否都已收敛
2. 任一侧未收敛 ⇒ 只记「候选待确认」，不进 ts_prepare、不报主协调候选
3. maxstep 用尽未收敛的格点：既不能当候选，也不能当「两侧点」（防「两个未收敛点夹一极大」的假候选）
4. **【主协调追加】极大点本身也必须是已收敛格点**，否则只登记趋势
5. 蛇形沿用 §R137 四邻判据；路径式与蛇形一律禁用「两维同极大/同极小」网格语言；两分支都不写「无 TS / 通道不存在」

**B. 工具落地：prep/scan2d_candidates_v3.py（sha256 5e9b9c5572239b5a1e47608b329b00aae0379a2ea0a66a7ce356913fdc9937da，22:11 自测通过，替换报告用 v2/c2fedf4c…）**
- 候选池**只由 `Optimization completed.` 块构成** ⇒ 判据 4 由结构强制（未收敛/轨迹帧永不可能进入候选池）
- 路径式分支邻居只取收敛池内前后点；缺侧/未收敛 ⇒ 输出 `candidate pending confirmation`；`Number of steps exceeded` / `Optimization stopped.` 命中数单列（当前 0）
- 每格标 **scan# + 实测 (R(2,4), R(25,26))**；实测偏离名义格点 >0.02 Å 打印 WARNING；遍历模式由实测增量自动判定（当前 6 点皆列 1 行推进 ⇒ 暂判 row-major/serpentine；scan#7 收敛后若 6→7 为 path-advance 自动切 path-type）
- 免责段已换成三条口径（1.6086 已验证 + ≥1.6 不封顶 + 路径待裁定；瞬时 ≈2.6145 带「含未验证帧」标签）

**C. 最新读数（实测 2026-10-17T22:10:19+08:00）**
- 1074：**81,109 行 / sha256 7fd20ea962a12f1f5f1aa3a0d794bdb98cbcae16f2b02c93784cf5b1c2082396**；`Optimization completed` 6；L80193 = `Step number   6 out of a maximum of  243 on scan point     7 out of    36`；末次 SCF L81082 = −939.190321363 ⇒ **+76.74 vs 1028**（自 L80105 的 +77.60 回落）；仍 (R(2,4)=2.4248, R(25,26)=1.2193)
- 1071：**143,053 行 / sha256 57b4e42a0dfb9f6f83e5620295df7b90dc656fcae8c87550475d94d7e83fed9b**；L142241 = `Step number 138 out of a maximum of  246`；末次 SCF L142154 = −939.317224623 ⇒ **−2.8840 vs 1028**；终止关键字 0
- **振荡带更正为 −2.88 ~ −5.34**（最低瞬时 −5.3443）；本道 22:09 的「−3.14」上包络作废

**D. post-freeze 汇总核对（`gold_finish_20261015/HI1/E3/POST_FREEZE_SUMMARY_2212.md` 55 行 / sha256 8b46a8014d532b509f806b41d05baca64b7a70675cb486f2232490c3e6a8b91f）**
- **唯一需改**：§1.2「振荡带 −3.14 ~ −5.34」→ **−2.88 ~ −5.34**（依据见 C）；已 hub 报（evt_492465d5a3ab46d9）
- **列 1 六点增量双签一致**（prep/col1_check_2212.py sha256 **bb83c83658b20214b2cda1a483d2191d55998dbb79c7dc6a6b5a2749b017caa8**）：+0.0000 / +9.3661 / +23.0525 / +36.9862 / +48.8190 / +58.2511 kcal/mol ⇒ 2 dp 即 +0.00/+9.37/+23.05/+36.99/+48.82/+58.25；**本道旧行文「+23.06/+48.83」为四舍五入笔误，更正为 +23.05/+48.82**
- **相邻点重原子 Kabsch 双签一致**：0.0790 / 0.0869 / 0.1318 / 0.1112 / 0.1107 Å（fit=20 heavy、eval=20 heavy、SVD、det=+1、禁镜像）；三条合成自检：刚体旋转+平移 **7.997e-16**、镜像副本 **2.1178**（被拒，det 仍 +1）、同结构副本 **1.998e-15**
- 口径澄清：本道早前「0.0989 Å」为 **all-41** 口径（scan#1→#2；all41 序列 0.0989/0.2206/0.1626/0.1406/0.1408），与汇总 heavy-20 的 0.0790 非同一口径，引用时必须写 fit set / eval set

**E. 发帖纪律（按 22:10:48 收紧）**：本道只在四类发声 ——「首个候选转正（两侧皆收敛且两侧皆降）」「scan#8 定方向」「1074 termination」「blocked」；其余只入本台账。

## P.81 2026-10-17 22:12 — v3 双向审计确认 + E1a 二面角「Δτ=68.0」定案（跨 ±180°，算术自洽）

**A. v3 双签**：`prep/scan2d_candidates_v3.py` = **124 行 / sha256 5e9b9c5572239b5a1e47608b329b00aae0379a2ea0a66a7ce356913fdc9937da**（本道 22:11 自测；主协调 22:11:26 实测同 sha 同行数）⇒ 报告表只用 v3，v2/c2fedf4c… 停用。输入 gjf 54 行 / f41e1d62…，L50–L52 = `B 2 4 S 5 0.2000` / `B 25 26 S 5 0.2500` / `B 10 27 F`（主协调 22:11:44 复核一致）。

**B. E1a 二面角定案（主协调 22:11:57 请复核项）**
- 日志 `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split/E1A_constrained_scan_R2692_2192_stepneg.log`：**91,682 行 / sha256 359937d48b16036a2626ff751e3f759808e34c18ef6e3b1bfcb27e42ecf181dc**（22:12:22 实测；Normal termination L91682 @20:26:25）
- **模型是 27 原子 C8H15N1O3（NAtoms=27，L153）**，非 E3 的 41 原子 ⇒ 跨边不得混用模型/能量
- 四元组（1-based，元素已核）**O3–C2–N18–C14**；**11 个收敛点**（L77262 = `Optimization completed on the basis of negligible forces.` 为「非精确版」收敛行，精确匹配会漏点）
- τ（有符号，度）：pt1 **+128.820**（L24969 / 帧 hdr L24461）/ pt2 +131.137（L29112）/ pt3 +136.033（L33240）/ **pt4 +139.032**（L38672 / hdr L38173）/ **pt5 −152.926**（L66240 / hdr L65729）/ pt6 −154.713（L72390）/ pt7 −155.682（L77262）/ pt8 −156.534（L80097）/ pt9 −157.511（L83584）/ pt10 −158.794（L87083）/ pt11 **−160.009**（L90606 / hdr L90115）
- **结论：Δτ = 68.0 自洽**——139.0 与 152.9 是 pt4/pt5 的 |τ|，两帧之间**跨 ±180° 符号翻转**；有符号最短角变化 **pt4→pt5 = +68.042°**（+139.032+68.042 = 207.074 ≡ −152.926），**pt1→pt11 = +71.170°**；`152.9−139.0 = 13.9` 只是两绝对值之差，**不得当 Δτ**
- 定稿写法建议：「τ(O3–C2–N18–C14) 由 **+139.032°**（pt4）经 **±180° 翻转**至 **−152.926°**（pt5），有符号最短角变化 **Δτ = +68.04°**；全程 pt1→pt11 **+71.17°**；|τ| 139.0→152.9 属跨号显示」；符号约定 = O3–C2–N18–C14 右手二面角为正
- 复算脚本 `prep/e1a_dihedral_check_v2.py`（43 行）/ sha256 **71682d739e4ec74a6110c26b073b90203e22ba60ab7e2a7d9ca0ded3b47e7214**
- **参照系观察（非错误）**：汇总 §3「支 A +1.09→+1.82 / 支 B +0.74→+4.25」与本道以 pt1 为零点的值（A +0.00/+0.19/+0.43/+0.74；B −0.35/+0.04/+0.50/+1.04/+1.67/+2.37/+3.16）恒差 **+1.09 kcal/mol**（逐点吻合）⇒ 两表零点不同，表头必须写「相对何参照」并给出该参照作业 log 路径 + sha；E1a result/barrier 仍 null，此仅呈现层

**C. 遍历模式表述收紧**：只写「第一维扫到终点后未归零（scan#7 连续多步 R(2,4)=2.4248、R(25,26)=1.2193）」，**蛇形 vs 路径式待 scan#8 定**；v3 自动判定输出届时入表。振荡带 **−2.88 ~ −5.34**（最低瞬时 −5.3443）双签成立。

**D. 已发帖**：evt_7e75eedd3212476b（回 22:11:57，含 B 节全部行号与 sha）。

## P.82 2026-10-17 22:32–22:34 — 遍历判定 **蛇形（SERPENTINE）** 定案 + v4 工具（删路径式分支）+ pt7 落地 + 跨度不确定度改 ≥1.58

**A. 事件：scan#8 定方向 = 蛇形（推翻 22:06 的「路径式」猜测）**
- 1074 快照：**101,166 行 / sha256 623bd481a35255bb42b3ff435c387fc5502e0c51479d2db6cf063fd0939512ea**（2026-10-17T22:33:20+08:00）；`Optimization completed` = **7**
- 实测依据：列 `R(25,26)=0.9693` 的 R(2,4) 序列 #1 1.4248 → #2 1.6248 → #3 1.8248 → #4 2.0248 → #5 2.2248 → #6 2.4248（步长 +0.200、全程递增）；**scan point 8 首个几何块 L97122 实测 (R(2,4)=2.2248, R(25,26)=1.2193) = 上一列末值 2.4248 − 一步 0.200** ⇒ 第一维到端点后**反向回扫**
- 探针 `prep/scan_direction_probe.py`（sha256 **b4d7b05bc1383a124c4dfe68cdba951d052654f074bd3aa7122ff97b5c394afe**）逐字输出：`VERDICT: SERPENTINE -- column 0.97 ran increasing 1.4248 -> 2.4248 (step 0.200); the next column 1.22 starts at R(2,4)=2.2248 = last - step`
- 判据分支：**蛇形四邻（§R137）**；路径式「路径局部极大」语言禁用；col2 预期按 #8 (2.2248) → #9 (2.0248) → #10 (1.8248) → #11 (1.6248) → #12 (1.4248) 反向填格（实测为准）

**B. 新工具 prep/scan2d_candidates_v4.py（136 行 / sha256 0a54f6f2257123455ac501df2609ede7b64aa88d84582fb596966e2365c641f0）**
- **只保留蛇形四邻判据**，路径式分支整段删除，固定输出 `mode: SERPENTINE`；v3（124 行 / 5e9b9c55…）保留为已审计历史产物、**不再出表**（不原地改 v3，避免主协调 22:11:26 的逐行审计编号失效）
- 候选池只由收敛块构成（含 negligible-forces 变体）；未收敛点不进池/不进邻居表；maxstep 用尽单列（当前 none）
- 每格标 scan# + 实测 (R(2,4), R(25,26)) + E；实测偏离名义 >0.02 Å 才 WARNING（当前无）
- 内置相邻点 heavy-20 Kabsch（SVD、det=+1、禁镜像）+ 三条合成自检（2.067e-15 / 2.1178 / 1.998e-15）
- 首跑：候选 **0 个**；6 点全为边界行/列 ⇒ needs-wider-window

**C. scan#7 落地（双签）**：收敛块 **L96617** / 帧 hdr **L95956** / SCF **L96205 = −939.193490136** ⇒ **+74.7593 vs 1028**（主协调 +74.76）；实测 (2.4248, 1.2193)、R(4,26)=2.5695、R(10,27)=0.9949、R(2,25)=1.2975、R(2,26)=2.0344；#6→#7 heavy-20 Kabsch **0.1213（max 0.3166、det +1）**，与主协调一致 ⇒ 无分支切换；col2/row6 属边界 ⇒ 非候选；比 scan#6 高 **+16.5081**（col2 在 row6 整体高于 col1）

**D. 跨度口径再更新（主协调 22:32:40 裁定）**
- 1071 新低：L161621 = **−939.322056251** ⇒ **−5.9172 vs 1028**、−1.5789 vs P；本道快照 **161,648 行 / sha256 009c32b510f0525cd99840776b79f8e263c6f2d0e6beb2a888f40fb90f5d7743**（22:32:16），L160770 = Step 157/246，终止关键字 0
- **产物端参照不确定度改为 ≥1.58 kcal/mol 且不封顶**（= |−5.9172 − (−4.3383)| = **1.5789**）；本道所有「≥1.6」表述全文替换；已验证极小跨度 **1.6086**（P/1061 vs 1073）不变；**质子路径待裁定**不变
- 瞬时读数跨度现 ≈**3.1875**（max 1073 −2.7297 / min 1071 −5.9172），只作快照、带「含未验证帧」标签、不进任何分母或差值

**E. 当前进行态（实测 22:34:29）**：1074 = **102,132 行 / sha256 eeb3ebfc522e308a6120deacf3950143f50d1059bb9b9a22e42c4f5a7f231a10**；L101392 = `Step number   5 out of a maximum of  243 on scan point     8 out of    36`；末次 SCF **L101304 = −939.204438570**（**+67.8890 vs 1028**，未收敛只登记；早前误记 +67.94 已更正）；末块 (2.2248, 1.2193)、R(4,26)=2.5962、R(10,27)=0.9949
- 出处说明：post evt_1bff90c3172b42ea/evt_05bc22ef0e6945e3 中「101,166 行 / 623bd481…（22:33:20）」为快照三元组，而 L101392/L101304 引自 22:34:29 的更晚状态（102,132 行 / eeb3ebfc…），二者非同一时刻，特此留痕

**F. 已发帖**：evt_1bff90c3172b42ea（事件类：scan#8 定方向=蛇形，to as_a341823c436e47ed）、evt_05bc22ef0e6945e3（回 22:32:40 裁定，to as_ec848a7673b74e35）。

## P.83 2026-10-17 22:36 — 参照不确定度按「不封顶」升至 **≥1.67**（1071 新低 −6.0070）；主协调 PROCESS.md 双签

**A. 主协调勘误双签**：`gold_finish_20261015/HI1/PROCESS.md` 本道独立实测 **609 行 / sha256 32f1b7db2d5be007f81935a6141d0e68d5de7a772c1ccb7b868a997fdbe2830d**（22:36:36），与其 22:36:14 自述逐位相同；占位符问题不登记为分歧。

**B. 1071 新低 ⇒ 参照不确定度更新（口径链条不变，只更新数值）**
- `/home/ly/Cloudra-mechanism-agent/ts/ts_0020/jobs/declaration_0001/ts_opt/refine.log`：**166,213 行 / sha256 9b56949436012999596471bc7a204e86ab783d8608aa3cf42ae13aa3f0c39d16**（22:36:36）；L165435 = `Step number 162 out of a maximum of  246`；**终止关键字 0**
- 末次 SCF **L165348 = −939.322199299** ⇒ **−6.0070 vs 1028**、**−1.6686 vs job 1061 的 P**
- **产物端参照不确定度 = ≥1.67 kcal/mol，不封顶**（= |−6.0070 − (−4.3383)| = **1.6687**；原 ≥1.58 依 −5.9172 得出，按同一「随新低更新」规则替换）
- 已验证极小跨度 **1.6086**（P/1061 −4.3383 vs 1073 −2.7297）+ **质子路径待裁定** 不变；瞬时读数跨度 **≈3.2773**（max −2.7297 / min −6.0070）只作快照、不进分母
- 本道全文已不存在「≥1.6」「≥1.58」「2.0160 作跨度」「2.6146 作跨度」的写法；当前唯一写法 = 1.6086 + ≥1.67 不封顶 + 路径待裁定

**C. 1074 当前态（实测 22:36:21，未收敛只登记）**：**104,014 行 / sha256 63ddb0db60c759350cc9e2ac46bf907500ead6a869bc94b1986c610be3c5333b**；`Optimization completed` 仍 **7**；L103274 = `Step number   7 out of a maximum of  243 on scan point     8 out of    36`；末次 SCF **L103186 = −939.204484780 ⇒ +67.8633 vs 1028**（与主协调 22:35:51 的 L102254 ⇒ +67.8633 一致）；蛇形判定、候选 0 个、边界列非候选均不变

**D. 已发帖**：evt_bad18b260ccf4292（回 22:36 勘误 + 不确定度更新）。

## P.84 2026-10-17 22:37 — 不确定度改**参数化句式**（最低值取 min，不取末行）；实测已再创新低 ⇒ 当前 ≥1.79；scan#8 收敛落地

**A. 方法更正（主协调 22:36:46 指出，我方接受并工具化）**：1071 是振荡轨迹，**最低值必须在全部 `SCF Done` 行上取 min，不得取最后一行**。
- 新工具 `prep/span_min_update.py`：**15 行 / sha256 209a5c8823cc0e3a98b84fa7845b8f831f98b7b7113c6ba4274387efb975a96c**（打印 global min / last / lowest-4 + 参数化不确定度与瞬时跨度）
- 双签：**L164410（Step 161）= −939.322318474 ⇒ −6.0817 vs 1028 / −1.7434 vs P**（与主协调一致）；但随后更低 ⇒ **GLOBAL MIN = L166285 = −939.322387181 ⇒ −6.1249 vs 1028 / −1.7865 vs P**；lowest-4 = L166285 −6.1249 / L164410 −6.0817 / L163492 −6.0685 / L162557 −6.0550

**B. 口径定稿（参数化，逐字采用主协调 22:36:46 定稿）**
> 产物端参照不确定度 = |最低未验证帧 − P|，**当前 ≥1.79 且不封顶**；每次创新低按同式重算、**只更新数值不改句式**。

- 当前值 = |−6.1249 − (−4.3383)| = **1.7865 ⇒ ≥1.79**；旧「≥1.6 / ≥1.58 / ≥1.67」**一律作废**、不再并列（同一公式的三个时刻值）
- 已验证极小跨度 **1.6086**（P/1061 −4.3383 vs 1073 −2.7297）不变；**质子路径待裁定**不变
- 瞬时读数跨度 **≈3.3951**（max 1073 −2.7297 / min −6.1249）：只作快照、含未验证帧、不进任何分母或差值
- 1071 快照：**167,207 行 / sha256 5f7bb9f29beb5b44784f24d173390e6af2b0be858c1edd67f79f093c7ecf8241**（22:37:40）、L166372 = Step 163/246、终止关键字 0

**C. scan#8 收敛（第 8 格点，非候选）**
- 1074 快照 **106,045 行 / sha256 dd186b8af40a67ec9e244defd39019af5060cbb369e8dccc54622be8ec493ddf**（22:37:40）；`Optimization completed` = **8**
- **scan#8 实测 (R(2,4)=2.2248, R(25,26)=1.2193)**，E = **−939.204485273**（SCF L104981 / 收敛块 L105379）⇒ **+67.8594 vs 1028**；R(4,26)=2.5999、R(10,27)=0.9949、R(2,25)=1.3310、R(2,26)=2.0322；H26 最近 O25 1.2193
- 列方向：col R(25,26)=1.22 实测 #7 2.4248 → #8 2.2248（**decreasing**），与 col1 increasing 交替 ⇒ 蛇形二次确认
- 判据：四邻中缺 row4（#9 未收敛）与 col3 ⇒ **非候选**；沿 R(2,4) 轴 #7 +74.7593 → #8 +67.8594（下降），沿质子轴 #5 +48.8190 → #8 +67.8594（上升）；候选计数仍 **0**

**D. 已发帖**：evt_dfe96e95cfb44ec7（回 22:36:46，含 A/B/C 全部数值与 sha）。

## P.85 2026-10-17 22:38–22:39 — min 再刷新 ⇒ 参数化句式带时刻「as of 22:38:48 ≥ 1.82」；scan#8 收敛双签、scan#9 首帧 2.0248；探针 within-column 分支修正

**A. 1071（min 取全部 SCF 行，带时刻打印）**
- `date -Is` **2026-10-17T22:38:48+08:00**：**168,168 行 / sha256 2712573466cda3e3a14e7acac39e986f5ddea141a3723058a97b8c08f973cf72**；SCF Done 计数 165；L167308 = Step 164/246；终止关键字 0
- **GLOBAL MIN = L168141 = −939.322441856 ⇒ −6.1592 vs 1028、−1.8208 vs job 1061 的 P**；lowest-4 = L168141 −6.1592 / L167221 −6.1439（主协调 22:38 值）/ L166285 −6.1249 / L164410 −6.0817
- **参数化句式（当前值）：产物端参照不确定度 = |最低未验证帧 − P|，当前（2026-10-17T22:38:48）**≥ 1.82** 且不封顶**（|−6.1592−(−4.3383)| = 1.8208）；瞬时读数跨度 ≈**3.4294**（仅快照）
- 工具升级 `prep/span_min_update.py`：**19 行 / sha256 3c2fabb79c6291dad48fdba675467ff38e210b689b84df29580d1df6099ded7d**（直接打印含时刻的可复制句式）

**B. 1074：scan#8 收敛双签、scan#9 首帧**
- `date -Is` 22:38:54：**107,018 行 / sha256 bf21c4c30ef194b5f774b6bba0d10199cc2c384b59bfe877d2fda8154b69f316**；`Optimization completed` = **8**；L106286 = `Step number   1 out of a maximum of  243 on scan point     9 out of    36`
- scan#8 双签：(row5,col2) 实测 (2.2248, 1.2193)，E = **−939.204485273**（SCF L104981 / 收敛块 L105379）⇒ **+67.8594 vs 1028**（主协调 +67.86）
- **scan#9 首块 L105884 实测 (2.0248, 1.2193)** ⇒ 同列内 R(2,4) 2.4248→2.2248→2.0248 连续下行，蛇形继续；判当前格点用几何首帧实测坐标，不用最后一条 Step 行
- 候选 **0**（#8 四邻缺 #9 与 col3）

**C. 探针修正（主动登记）**：`prep/scan_direction_probe.py` 旧版对「同列内推进」误判 undetermined；已加 within-column 分支，现输出 `VERDICT: WITHIN-COLUMN ADVANCE (serpentine continues) ...`；新 sha256 **5a937214fa134b8d0992faee8920f5cac1207ce66267119eefa14b341ddd53a3** / 78 行；跨列 SERPENTINE 判定不受影响，但一律以新版为准

**D. 已发帖**：evt_20b539eb0a3c46cb（回 22:38:06–16，含 A/B/C 全部数值与 sha）。

## P.86 2026-10-17 22:39 — 主协调 PROCESS.md 625 行 / c63ff552… 双签；双日志 22:39:38 快照（无新事件）

**A. 主协调补实值双签**：`gold_finish_20261015/HI1/PROCESS.md` 本道独立实测 **625 行 / sha256 c63ff552e113b255d4737b261084610c5e3dee1e7cdb7a017573fa2851dc815d**（22:39:40）⇒ 与其 22:39:32 值逐位相同。

**B. 1071（22:39:38 实测）**：**169,069 行 / sha256 536fb9d29e96d14c84eec5405ba55764e7e221cb0b2a12b7d1a013b4f944b7f9**；SCF Done 165 条；L168228 = Step 165/246；终止关键字 0；GLOBAL MIN 仍 **L168141 = −939.322441856 ⇒ −6.1592 vs 1028**；**当前（22:39:38）参照不确定度 ≥1.82 不封顶**；瞬时跨度 ≈3.4294（仅快照）。执行纪律：只写「式 + 时刻 + 当前值」，不并列 ≥1.81/≥1.82。

**C. 1074（22:39:38 实测）**：**107,142 行 / sha256 c274d3fcce8abd9116f3af6786b029bb74aa01d8f1d4fed2b5524b54a5a62ee9**；`Optimization completed` 仍 **8**；L106286 = `Step number   1 out of a maximum of  243 on scan point     9 out of    36`（scan#9 Step 1 持续）；探针输出 `VERDICT: WITHIN-COLUMN ADVANCE (serpentine continues) ...`；候选 **0**；scan#8 双签 E = −939.204485273 = +67.8594 vs 1028 不变。

**D. 已发帖**：evt_9400afe1db314664（对调用的必要回复，非进度播报）。

## P.87 2026-10-17 22:48 — 旁道事件登记（不属于本道）：E1a 成键侧续扫 job 1077 已提交

- 来源：small_mol 广播 evt_3406b62ac21d4ee4（非本道任务、非本道提交）。job 1077，node-local，8 cpus / 10240 MB / priority 0，started_at 2026-10-17T22:48:15+08:00，输入 `HI1/E1/split/E1A_scan_cont1_C2N18.gjf` sha256 d2043fc5ade4b3087c08005cec94427ca49f3639dcb96f75a6fed49c8d81b2ae，约束 `B 2 18 S 5 -0.1000`（6 个几何 2.1920→1.6920），起始帧 = E1a 既有日志第 11 个收敛帧（log L90115-L90143 / L90606）
- 与本道的关系：**仅队列容量相关**（本道零提交、无竞争诉求）；不改变 E3b 任何读数、口径或结论；E1a result/barrier 仍 null，其峰值只作 TS 候选/上界
- 本道记录：不接手该作业、不评论其判据、不 kill、不重投

## P.88 2026-10-17 23:05 — scan#9 落地（第 9 格点）、col2 单调下行、候选仍 0；1071 新低 ⇒ 参数化句式 as of 23:05:28 ≥ 1.88

**A. 1074 快照（`date -Is` 2026-10-17T23:05:28+08:00）**：**128,028 行 / sha256 7e25ed3280b9d90c61909b3f64052fb29a184b32c8e76f90f180797602b5cac5**；`Optimization completed` = **9**；L127262 = `Step number   3 out of a maximum of  243 on scan point    10 out of    36`；maxstep 用尽点 **0**
- **scan#9 实测 (R(2,4)=2.0248, R(25,26)=1.2193)**，E = **−939.221254193**（SCF L124053 / 收敛块 L124469）⇒ **+57.3371 vs 1028**、+61.6754 vs P(job 1061)；R(4,26)=3.0146、R(10,27)=0.9949、R(2,25)=1.3687、R(2,26)=2.0929；H26 最近 O25 1.2193
- 列 2（R(25,26)=1.2193）实测序列：#7 2.4248 (+74.7593) → #8 2.2248 (**+67.8597**) → #9 2.0248 (+57.3371) ⇒ **随 R(2,4) 减小单调下降**；同 row 上 col2 比 col1 高：row4 差 **+20.3509**（#9 vs #4）、row5 差 +19.0407（#8 vs #5）、row6 差 +16.5081（#7 vs #6）
- 数值更正（我方，微小）：scan#8 的 kcal 值前一节写作 +67.8594，**正确为 +67.8597**（主协调 +67.86 不受影响）；属四舍五入笔误，非新测量
- **候选计数仍 0**：#8 四邻缺 r5c3；#9 四邻缺 r3c2 与 r4c3；#1–#7 为边界行/列 ⇒ needs-wider-window。化学含义（仅提示，不下结论）：在 row≥4 区域，质子维抬高能量、R(2,4) 缩短降低能量，单调无驻点；驻点若存在应在**更小 R(2,4)（row 1–3）× col 2** 的同步区

**B. 1071（同一时刻）**：**188,985 行 / sha256 3375ee54fba41db371145959dfe900cefaeb5af3026516e651bee4381e3e50b3**；SCF Done 186 条；L188234 = `Step number 186 out of a maximum of  246`；终止关键字 0；**GLOBAL MIN = L188147 = −939.322539514 ⇒ −6.2204 vs 1028、−1.8821 vs P**
- 参数化句式（当前值）：「产物端参照不确定度 = |最低未验证帧 − P|，当前（**2026-10-17T23:05:28**）**≥ 1.88** 且不封顶」；瞬时读数跨度 ≈**3.4907**（仅快照、不进分子分母）；lowest-4 = L188147 −6.2204 / L186275 −6.1966 / L187212 −6.1813 / L168141 −6.1592

**C. 事件分类**：本条**不属四类事件**（无候选、方向已定、1071 未终止），故**不发帖**，只入台账。

**D. 边界**：只读；零提交 / 零 kill / 不 priority / 不 ts_resume；四条边 result/barrier 全 null；交付面 a2964d8d… / 277 行 + 11 文件 sha、§14、hi.py 不动。

**边界**：本道只读；零提交 / 零 kill / 不 priority / 不 ts_resume；四条边 result/barrier 全 null；交付面 a2964d8d… / 277 行 + 11 文件 sha、§14、hi.py 不动。

**E. 边界**：只读；零提交 / 零 kill / 不 priority / 不 ts_resume；四条边 result/barrier 全 null；交付面 a2964d8d… / 277 行 + 11 文件 sha、§14、hi.py 不动。

**E. 边界**：只读；零提交 / 零 kill / 不 priority / 不 ts_resume；四条边 result/barrier 全 null；交付面 a2964d8d… / 277 行 + 11 文件 sha、§14、hi.py 不动。

**E. 边界**：只读；零提交 / 零 kill / 不 priority / 不 ts_resume；四条边 result/barrier 全 null；交付面 a2964d8d… / 277 行 + 11 文件 sha、§14、hi.py 不动。

**E. 边界**：只读；零提交 / 零 kill / 不 priority / 不 ts_resume；四条边 result/barrier 全 null；交付面 a2964d8d… / 277 行 + 11 文件 sha、§14、hi.py 不动。

**G. 边界**：只读；零提交 / 零 kill / 不 priority / 不 ts_resume；四条边 result/barrier 全 null；交付面 a2964d8d… / 277 行 + 11 文件 sha、§14、hi.py 不动。

**E. 边界**：只读；零提交 / 零 kill / 不 priority / 不 ts_resume；四条边 result/barrier 全 null；交付面 a2964d8d… / 277 行 + 11 文件 sha、§14、hi.py 不动。

**F. 边界**：只读；零提交 / 零 kill / 不 priority / 不 ts_resume；TS 走 ts_prepare/ts_resume 由主协调放行；四条边 result/barrier 全 null；交付面 a2964d8d37aa3214fd03136b5a4d6d95a0e4a3b57c9465a6368c1e6b0cf230df / 277 行 + 11 文件 sha、§14、hi.py 不动。

**F. 边界**：只读；零提交 / 零 kill / 不 priority / 不 ts_resume；未触碰 ts_0015 / ts_0016；四条边 result/barrier 全 null；交付面 a2964d8d… / 277 行 + 11 文件 sha、§14、hi.py 不动。

## P.89 2026-10-17 23:07 — 看护触发点改为「scan#10 收敛 / scan#16 起跑 / 1071 终止」；四邻齐全性字段；pt9 与 Kabsch 双签；不确定度 as of 23:07:11 ≥1.90

**A. 看护（主协调 23:05:56 要求，已执行）**
- 触发点：①**scan#10 收敛**（判据 = 日志出现 `on scan point    11 out of`，即第 10 个 Optimization completed 后立刻命中）②**scan#16 起跑**（`on scan point    16 out of`）③**1071 任一终止关键字**；不再以 scan#10「起跑」为触发
- **四邻齐全性**：v4 每格打印 `neighbours missing or unconverged: rNcM,...`；候选只在四邻齐全时计算，边界单列 needs-wider-window ⇒ 未判读点不进候选
- 山脊分支（§R137 写死）：若 (row4,col3) 高于 (row4,col2) ⇒ ridge vertex ⇒ 非候选，分支为「该质子值处一维弛豫 R(2,4) 扫描」或「重设质子列」

**B. pt9 与 Kabsch 双签（与主协调逐位一致）**
- pt9 = (row4,col2)：收敛块 **L124469** / SCF **L124053 = −939.221254193** ⇒ **+57.3371 vs 1028**；R(2,4)=2.0248、R(25,26)=1.2193、R(4,26)=3.0146、R(10,27)=0.9949、R(2,25)=1.3687
- **Kabsch pt8→pt9 = rms 0.1671 / max 0.2925 / det +1.000**（fit=20 heavy / eval=20 heavy）；本道序列 1→2 0.0790 … 6→7 0.1213、7→8 0.0886、8→9 0.1671；合成自检 2.067e-15 / 2.1178 / 1.998e-15
- 结构读法：col2 沿 R(2,4) row6 +74.7593 → row5 +67.8597 → row4 +57.3371 单调降；row4 沿 R(25,26) col1 +36.9862 → col2 +57.3371 升 ⇒ 若 scan#10 < +57.34，(row4,col2) 沿 R(2,4) 为局部极大；候选取决于 (row4,col3)=scan#16

**C. 1071（23:07:11 实测）**：**189,955 行 / sha256 b6e87612c5463f0e1761d8cdd4e12d6c730c912b279680f44c39f7c235a1a254**；SCF Done 187；L189153 = Step 187/246；终止关键字 0；**GLOBAL MIN = L189066 = −939.322564652 ⇒ −6.2362 vs 1028、−1.8979 vs P** ⇒ 参数化句式 **「as of 2026-10-17T23:07:11 ≥ 1.90 且不封顶」**；瞬时跨度 ≈3.5065（仅快照）；lowest-4 = L189066 −6.2362 / L188147 −6.2204 / L186275 −6.1966 / L187212 −6.1813

**D. 1074（23:07:11 实测）**：**129,001 行 / sha256 2f614877b51d22e8a7af30ee06ddeb4d19d0cc3df622e1057b22677d5a331b0b**；`Optimization completed` 仍 **9**；L128213 = `Step number   4 out of a maximum of  243 on scan point    10 out of    36`；候选 **0**

**E. 已发帖**：evt_9e5ab6f366a34e69（回 23:05:56，含 A–D 全部数值与 sha）。

**F. 边界**：只读；零提交 / 零 kill / 不 priority / 不 ts_resume；四条边 result/barrier 全 null；交付面 a2964d8d… / 277 行 + 11 文件 sha、§14、hi.py 不动。

## P.90 2026-10-17 23:10 — 候选能垒承载维更正（(r4c2) ⇒ 由 R(25,26) 承载）；pending-neighbour 字段；下界一律向下取 ⇒ 当前 ≥1.92

**A. 能垒承载维更正（主协调 23:09:40；其 23:05:56 的「沿 R(2,4) 局部极大」说法作废）**
- 正确口径：col2 上 row5 (+67.8597) 比 row4 (+57.3371) 高 10.52 ⇒ (r4c2) **沿 R(2,4) 只可能是局部极小**；候选要求质子轴为局部极大 ⇒ **能垒由 R(25,26) 承载**，绝不写「R(2,4) 承载」
- 三种走向：scan#10（row3,col2）**> +57.34** ⇒ R(2,4) 轴极小成立；col3（scan#16）**< +57.34** ⇒ 质子轴极大 ⇒ 指标 1 候选（R(25,26) 承载）；scan#10 **< +57.34** ⇒ 单调、无从成候选；col3 更高 ⇒ 两轴同极大 = 山脊、非候选
- 工具：**prep/scan2d_candidates_v5.py**（153 行 / sha256 **ef069a51001bd60e8bf2580eace39e7c3575848da27b0085626a8504f5c939b6**）；v4（136 行 / 0a54f6f2…）保留作审计历史
  - 判据行自动打印 `note: R(2,4) axis is a local MIN here, so a candidate would need the proton axis to be a local MAX (barrier carried by R(25,26)), not by R(2,4)`
  - 新增 **pending neighbours** 段：列每个等邻格的点 + 在跑格点**未收敛能量**（标注 never a candidate / never a neighbour）；本次实测 `in-progress cell (nominal r3c2) measured (1.8248, 1.2193); latest SCF L129991 = -939.243010286`、`scan#9 (r4c2) is waiting on r3c2 ... PENDING`
  - 免责段固定 axis 规则（one axis MAX + other MIN，承载维 = 其 MAX 所在轴；(r4c2) 承载维 = R(25,26)）

**B. 下界取整纪律（主协调 23:09）：一律向下取、禁上舍**
- `prep/span_min_update.py` 改为 `math.floor(x*100)/100`：**21 行 / sha256 80771f0ae180624c1d3ef33cb8a0b9b87c28cdf20a869bc7c95870c64677b3fa**
- 现行值（23:10:15）：1071 **191,852 行 / sha256 25e663b9ab5e1809abac6190413811c58a9940066db9232159f5e5bbfe45f225**；SCF Done 189；L191009 = Step 189/246；终止关键字 0；**GLOBAL MIN = L190922 = −939.322609417 ⇒ −6.2643 vs 1028、−1.9260 vs P**
- 参数化句式：**「产物端参照不确定度 = |最低未验证帧 − P|；as of 2026-10-17T23:10:15 ≥ 1.92 且不封顶」**（1.9260 向下取）；旧 ≥1.89（L189066）与 ≥1.90 不单列；瞬时跨度 ≈3.5346（仅快照）；lowest-4 = L190922 −6.2643 / L190004 −6.2427 / L189066 −6.2362 / L188147 −6.2204

**C. 1074（23:10:15 实测）**：**130,911 行 / sha256 a8f71e3e5e194fd23f063e471a9c15492977c46ffbb88997605b6fd4854bc9ad**；`Optimization completed` 仍 **9**；L130080 = `Step number   6 out of a maximum of  243 on scan point    10 out of    36`；在跑格点实测 (1.8248, 1.2193)、R(4,26)=2.9799、R(10,27)=0.9949；候选 **0**

**D. 已发帖**：evt_2e19a07721c64acf（回 23:09:40）。

**E. 边界**：只读；零提交 / 零 kill / 不 priority / 不 ts_resume；四条边 result/barrier 全 null；交付面 a2964d8d… / 277 行 + 11 文件 sha、§14、hi.py 不动。

## P.91 2026-10-17 23:12 — v5 免责段改运行时（禁钉子）→ 164 行 / 9b038f87…；1071 min 双签 −6.2643 ⇒ ≥1.92

**A. v5 修订（主协调 23:12:17 条件采纳 → 改完待其复核）**
- `prep/scan2d_candidates_v5.py`：**164 行 / sha256 9b038f87ba8e619f7510037b989f06c1b1f32b14c862edd3298ea275c81697f8**（旧 153 行 / ef069a51… 作废）
- **硬钉数字删除已核验**：`grep -c '1\.58|3\.1875|L161621'` = **0**；L150 仅保留「verified-minima span = 1.6086（P/1061 −4.3383 vs 1073 −2.7297，均 0 虚频同 InChIKey）+ 质子路径待裁定」
- **L152–163 运行时块**：读 1071 日志 → 对全部 `SCF Done` 取 **min** → `math.floor` 向下取下界 → 打印本进程时刻；不可读则输出 `MISSING MEASUREMENT ... never substitute a hard-coded number.`
- 本次运行逐字：`... as of 2026-10-17T23:12:42+0800  >= 1.92 kcal/mol, not capped  [min L190922 = -939.322609417 => -6.2643 vs 1028, -1.9260 vs P; bound floored from 1.9260]`；`instantaneous reading span = -2.7297 - -6.2643 = 3.5346 kcal/mol : SNAPSHOT only`
- 主协调已审计通过的结构未改动（实测坐标反推格点、四邻判据与边界先标、进行中格点单列、Kabsch heavy-20 + det=+1 + 三条合成自检、固定 SERPENTINE、pending neighbours）

**B. 双签（23:12:50 实测）**
- 1071：**193,705 行 / sha256 f1e6de3e5251dd930cf78e07af96a6dbb0b80dfe7400b8ab5f2aa937b7a316e6**；SCF Done 191；L192911 = Step 191/246；终止关键字 0；**GLOBAL MIN = L190922 = −939.322609417 ⇒ −6.2643 vs 1028、−1.9260 vs P**（与主协调逐位一致）；末行 L192824 = −939.322235664（−6.0298）高于最低 ⇒ 必须取 min 再次得证 ⇒ 参数化句式「as of 23:12:50 ≥ 1.92 不封顶」
- 1074：**132,738 行 / sha256 3acc5750fd02150b57033facc532547fdbd98425bc172315d1dbe6391ed744cd**；`Optimization completed` 仍 9；L131934 = Step 8/243 on scan point 10；在跑格点（nominal r3c2）实测 (1.8248, 1.2193)、R(4,26)=2.9864、R(10,27)=0.9949；候选 0

**C. 引用纪律**：本道 23:10:15 的 in-progress 读数（r3c2、L129991）一律标注「E3 lane 读数 + 时刻」；候选只作候选/上界、禁写 ΔE‡、未收敛格点不作邻居、(r4c2) 若成候选能垒承载维写 **R(25,26)**、整表无候选只写「该 6×6 网格未分辨出离散指标 1 的驻点，需扩窗或加密」

**D. 已发帖**：evt_ff2a184192074240（回 23:12:17，含新 sha 与运行时输出）。

**E. 边界**：只读；零提交 / 零 kill / 不 priority / 不 ts_resume；四条边 result/barrier 全 null；交付面 a2964d8d… / 277 行 + 11 文件 sha、§14、hi.py 不动。

## P.92 2026-10-17 23:13 — v5 复核通过（唯一出表工具）；否认认领 E1/split/e1a_cont1_check_2309.py（无主 scratch）

**A. v5 正式采纳（主协调 23:13:23 复核通过）**：唯一出表工具 = `prep/scan2d_candidates_v5.py` **164 行 / sha256 9b038f87ba8e619f7510037b989f06c1b1f32b14c862edd3298ea275c81697f8**；v4（136 行 / 0a54f6f2…）与 v3（124 行 / 5e9b9c55…）仅作审计历史、不再出表。主协调复核要点：常量自洽（REF1028/P/MAXVER ⇒ −6.2643 / −1.9260 / −2.7297、跨度 3.5346 逐位一致）、`math.floor` 下界 ≥1.92、`as of <本进程时刻>` + `MISSING MEASUREMENT` 兜底、三条合成自检与相邻 Kabsch 逐点一致、pending neighbours 与 in-progress 段正确。

**B. 文件归属（含证据，否认认领）**：`gold_finish_20261015/HI1/E1/split/e1a_cont1_check_2309.py` = 1,361 字节 / 29 行 / sha256 **eb12735f6c413499ad441dabddba3a8219ac40d22f7c98ef94579b4a1ee94715**，mtime 2026-10-17 23:09:33.587
- 证据 1：本道所有写操作限于 `HI1/E3/prep/`（及本道台账/输入），**从未写 HI1/E1/** 下任何文件
- 证据 2：`grep -rl 'e1a_cont1' HI1/E3/` = **0 命中**
- 证据 3：本道 prep 清单 mtime 无 23:09:33 项（v2 21:14 / v3 22:10 / v4 22:34 / v5 23:12 / scan7_trace 22:09 / scan_pt_trace 22:32 / scan_direction_probe 22:39 / span_min_update 23:10，其余 16:07–21:46）
- ⇒ 按主协调规则该文件为**无主 scratch、不得引用**；本道不接手、不修改、不删除（避免破坏他人证据链）

**C. 双签（23:13:41 实测）**：1071 **193,705 行 / f1e6de3e…**、SCF 191、Step 191/246、终止 0、GLOBAL MIN **L190922 −6.2643 vs 1028 / −1.9260 vs P** ⇒「as of 23:13:41 ≥ 1.92 不封顶」；1074 **132,738 行 / 3acc5750…**、OPT 仍 9、scan#10 在跑（主协调 Step 9/243、L133446、R(4,26)=2.9876 同链）；候选 **0**

**D. 已发帖**：evt_63029b1ccf9a4dcd（回 23:13:23，含 A–C 全部证据与 sha）。

**E. 边界**：只读；零提交 / 零 kill / 不 priority / 不 ts_resume；四条边 result/barrier 全 null；交付面 a2964d8d… / 277 行 + 11 文件 sha、§14、hi.py 不动。

## P.93 2026-10-17 23:21 — scan#10 收敛 ⇒ **(r4c2)=scan#9 出局**（R(2,4) 轴单调、非局部极小）；1071 min −6.3434 ⇒ ≥2.00

**A. 快照（`date -Is` 2026-10-17T23:21:10+08:00）**
- 1074：**138,639 行 / sha256 7a9b4442cfc751b34fc033a590c7c91113a7758cd29ab36f725e20ead4287046**；`Optimization completed` = **10**；L137738 = `Step number   2 out of a maximum of  243 on scan point    11 out of    36`；maxstep 用尽 0
- 1071：**199,307 行 / sha256 30605fda3ccb48c9eab053f91e8334752260a9726b09e22a355b2cdc9de36dab**；SCF Done 197；L198533 = Step 197/246；终止关键字 0

**B. scan#10 落地（决定性）**：实测 (R(2,4)=1.8248, R(25,26)=1.2193)，E = **−939.243015613**（SCF L135474 / 收敛块 L135887）⇒ **+43.6816 vs 1028**；R(4,26)=2.9882、R(10,27)=0.9949、R(2,25)=1.3924、R(2,26)=2.1132
- col2 沿 R(2,4) 实测序列与能量：row6 #7 **+74.7593** → row5 #8 **+67.8597** → row4 #9 **+57.3371** → row3 #10 **+43.6816**（**scan#10 − scan#9 = −13.6555**）⇒ **单调下降**
- ⇒ **(r4c2)=scan#9 沿 R(2,4) 不是局部极小**，按 23:09 更正后的判据**明确不能成为候选**（无需等 scan#16/col3 即可出局）；沿质子轴仍升：row4 col1 +36.9862 → col2 +57.3371（+20.3509）；row3 col1 +23.0525 → col2 +43.6816（+20.6290）
- 全表候选计数仍 **0**；其余缺邻点：#8 缺 r5c3、#10 缺 r2c2/r3c3、#7 缺 r7c2/r6c3
- 化学倾向（记录、非结论）：col2 在 row≥3 一路高于 col1 且随 R(2,4) 缩短单调下降 ⇒ 纯「质子拉长 + C–N 拉长」象限无驻点；若存在指标 1 驻点，只能在**更小 R(2,4)（row1–2）× 更大 R(25,26)（col3+）**的耦合区

**C. 1071 跨度（参数化句式）**：**GLOBAL MIN = L198446 = −939.322735485 ⇒ −6.3434 vs 1028、−2.0051 vs P** ⇒「产物端参照不确定度 = |最低未验证帧 − P|；as of 2026-10-17T23:21:08 **≥ 2.00** 且不封顶」（下界 floor：2.0051→2.00）；瞬时读数跨度 ≈**3.6137**（仅快照）；lowest-4 = L198446 −6.3434 / L197525 −6.3189 / L196589 −6.3148 / L194699 −6.3044；已验证极小跨度 1.6086 与质子路径待裁定不变

**D. 已发帖/呼叫**：evt_0a0ffd85b16f44f8（首行 to as_a341823c436e47ed）+ call as_ec848a7673b74e35（23:21 事件类）。

## P.94 2026-10-17 23:22 — v5 banner 修复（运行时自哈希）→ 170 行 / 9bb2c982…；Kabsch #9→#10 双签；1071 新低 ⇒ ≥2.01

**A. v5 banner 瑕疵修复（主协调 23:21:38 第 4 条）**
- `prep/scan2d_candidates_v5.py`：**170 行 / sha256 9bb2c982ad1641f195471c58e934ce2382e7f1d3401e6838d066e557595bce5e**（旧 164 行 / 9b038f87… 作废）
- 首两行实测：`=== scan2d_candidates_v5 (serpentine / four-neighbour only; path-type branch removed; runtime span block) ===` / `    self sha256 (computed at runtime) = 9bb2c982ad1641f195471c58e934ce2382e7f1d3401e6838d066e557595bce5e`
- 实现：banner 内 sha 由 `hashlib.sha256(open(__file__,'rb').read())` **运行时计算**，永不过期；其余结构零改动；硬钉数字仍 0 命中

**B. 双签（23:22:08 实跑）**
- **Kabsch scan#9→#10 = rms 0.1259 / max 0.2186 / det +1.0**（与主协调一致）；#8→#9 = 0.1671 / max 0.2925 / det +1.0
- pending 段逐字：`in-progress cell (nominal r2c2) measured (1.6248, 1.2193); latest SCF L138612 = -939.266580732 (unconverged, never a candidate and never a neighbour)`；scan#2、scan#10 标 PENDING
- 1074：23:21:10 = **138,639 行 / 7a9b4442…**、OPT 10、候选 0
- 1071 **新低**：GLOBAL MIN **L199364 = −939.322747252 ⇒ −6.3508 vs 1028、−2.0125 vs P** ⇒「**as of 2026-10-17T23:22:01 ≥ 2.01 且不封顶**」（floor）；瞬时快照 ≈3.6211

**C. 旁道读数登记（非本道权威）**：主协调 23:21 提供的 1077（E1a-cont1：45,049 行 / edee2f69…、OPT 5、pt5 −593.913920630、ΔE vs RC_27 +12.93）与 1076（E2-cont1：25,062 行 / 4270bba9…、OPT 1、scan point 2/5 Step 23/219、末 SCF −939.295974239）仅登记为「主协调读数 + 时刻」，不进 E3b 任何数值链、不作判读

**D. 已发帖**：evt_0023c4a317314abd（回 23:21:38）。

**E. 边界**：只读；零提交 / 零 kill / 不 priority / 不 ts_resume；四条边 result/barrier 全 null；交付面 a2964d8d… / 277 行 + 11 文件 sha、§14、hi.py 不动。

## P.95 2026-10-17 23:36 — scan#11 落地（col2 仍单调降）；候选 0；1071 min −6.4274 ⇒ ≥2.08 且已到 Step 210/246

**A. 快照（`date -Is` 2026-10-17T23:36:54+08:00）**
- 1074：**150,937 行 / sha256 b8d9ecbba0112b3411b9157f0b09408729e05f41349d8dfc8e7b4487cda9e0b2**；`Optimization completed` = **11**；L150077 = `Step number   2 out of a maximum of  243 on scan point    12 out of    36`；maxstep 用尽 0
- 1071：**211,395 行 / sha256 c9dece311057f26d20e2e6a48b11b6a4e7b493558001e498d98a6c2e9ba46a91**；L210656 = `Step number 210 out of a maximum of  246`（**距步数上限 246 仅剩 36 步**）；终止关键字 0

**B. scan#11（col2 第 5 个格点）**：实测 (R(2,4)=1.6248, R(25,26)=1.2193)，E = **−939.266643733**（SCF L147816 / 收敛块 L148228）⇒ **+28.8547 vs 1028**；R(4,26)=2.9309、R(10,27)=0.9949、R(2,25)=1.4236、R(2,26)=2.1356
- col2 沿 R(2,4) 实测序列（能量）：row6 #7 **+74.7593** → row5 #8 **+67.8597** → row4 #9 **+57.3371** → row3 #10 **+43.6816** → row2 #11 **+28.8547**（#11 − #10 = **−14.8269**）⇒ 仍**全程单调下降**
- 沿质子轴：row2 col1 #2 **+9.3661** → col2 #11 **+28.8547**（**+19.4886**）⇒ 仍升
- 候选判据：#11 四邻缺 r1c2（scan#12 未收敛）与 r2c3（col3 未开始）⇒ **非候选**；#1–#7 边界；#8 缺 r5c3；#9 缺 r4c3；#10 缺 r3c3 ⇒ **全表候选 0**
- Kabsch scan#10→#11 heavy20 = **rms 0.1687 / max 0.3203 / det +1.0**（无分支切换）；pending 段：（nominal r1c2）在跑、L150951 = −939.279512780（未收敛，never a candidate/never a neighbour），scan#1 与 scan#11 标 PENDING
- 结构趋势（记录、非结论）：col2 每个 row 都比 col1 高 19–21 kcal/mol 且随 R(2,4) 缩短单调降 ⇒ 该象限仍无驻点；判据要等 col3（scan#13 起）才能对内点定论

**C. 1071 跨度（参数化句式）**：GLOBAL MIN **L210568 = −939.322869361 ⇒ −6.4274 vs 1028、−2.0891 vs P** ⇒「as of 2026-10-17T23:36:54 **≥ 2.08** 且不封顶」（floor：2.0891→2.08）；瞬时快照 ≈**3.6977**（仅快照）；lowest-4 = L210568 −6.4274 / L209675 −6.4234 / L208755 −6.4172 / L207833 −6.4050；已验证极小跨度 1.6086 与质子路径待裁定不变

**D. 事件分类**：无候选、方向已定、1071 未终止 ⇒ **不发帖**，只入台账；一旦 1071 触及 246 步上限（预计 30–60 分钟内）即启动四档判读并按「先报后记」纪律发帖

**E. 工具**：出表 = prep/scan2d_candidates_v5.py（**170 行 / 9bb2c982…**，运行时自哈希 banner）；跨度 = prep/span_min_update.py（21 行 / 80771f0a…）

**G. 追加（23:48 巡检）**：见 §P.96（col2 全部 6 格完成、col3 起跑）。

## P.96 2026-10-17 23:48 — col2 六格全部落地（单调、全程高于 col1 19–21）；col3 起跑；候选 0；1071 Step 224/246 min −6.4431 ⇒ ≥2.10

**A. 快照（`date -Is` 2026-10-17T23:48:39+08:00）**
- 1074：**162,202 行 / sha256 30d998738d637bd8d4e22abaab211f2e7d3785563a1cf77bfee726e8650783f4**；`Optimization completed` = **12**；L161476 = `Step number   4 out of a maximum of  243 on scan point    13 out of    36`（**col3 已起跑**）
- 1071：**223,841 行 / sha256 4d75b7d236b29bd1bc4aabf364e5db5f690919c9febd4bc9469ffd7097a638e0**；L223099 = `Step number 224 out of a maximum of  246`（**剩 22 步**）；终止关键字 **0**

**B. scan#12（col2 末格，row1）**：实测 (R(2,4)=1.4248, R(25,26)=1.2193)，E = **−939.279694367**（SCF L157357 / 收敛块 L157762）⇒ **+20.6653 vs 1028**；R(4,26)=2.8424、R(10,27)=0.9949、R(2,25)=1.4763、R(2,26)=2.1736
- **col2 完整序列（按 row1→row6 排列的能量）**：row1 #12 **+20.6653** / row2 #11 **+28.8547** / row3 #10 **+43.6816** / row4 #9 **+57.3371** / row5 #8 **+67.8597** / row6 #7 **+74.7593** ⇒ 沿 R(2,4) 单调（缩短 R(2,4) 降能量）
- **col2 − col1 逐行差**：row1 **+20.67** / row2 **+19.49** / row3 **+20.63** / row4 **+20.35** / row5 **+19.04** / row6 **+16.51** ⇒ **col2 全程高于 col1（16.5–20.7），无交叉、无峰**
- 候选：#12 属**边界行** ⇒ needs-wider-window、非候选；#8–#11 均缺其 col3 邻居 ⇒ 非候选；**全表候选 0**

**C. col3 起跑**：scan#13 在跑格点实测 **(1.4248, 1.4693)**（serpentine 在 col3 改向上行），L161388 = −939.228701508（未收敛，never a candidate/never a neighbour）；pending 段已把 scan#12 标 PENDING（等 r1c3）

**D. 工作假设（记录、待 col3 数据检验）**：col2（H26 位于 O25/N4 中间）整体比 col1（H26 留在 O25）高 16.5–20.7 kcal/mol 且形状同构（单调）⇒ 质子「拉长到 1.2193」这一维度单独看是**单调抬升的墙**，不产生驻点；若 col3（1.4693）继续抬高，则本 6×6 网格在「C2–N4 拉长」象限整体无驻点，指标 1 候选只能靠**缩短 R(2,4) 侧**（即更小 C2–N4，质子仍近 O25）或**加密/扩窗**去找。

**E. 1071（同刻）**：GLOBAL MIN **L223011 = −939.322894306 ⇒ −6.4431 vs 1028、−2.1047 vs P** ⇒「as of 2026-10-17T23:48:39 **≥ 2.10** 且不封顶」（floor：2.1047→2.10）；瞬时快照 ≈**3.7134**（仅快照）；lowest-4 = L223011 −6.4431 / L222130 −6.4426 / L221252 −6.4422 / L220357 −6.4413（已趋平台、逐步微降）；**Step 224/246 ⇒ 预计 ≤30 min 内以 `Number of steps exceeded, NStep= 246` 终止，届时按四档判读**（P 型产物盆轨迹帧、非鞍点、无 TS、无 ΔE‡），先报两位协调者再落台账

**F. 事件分类**：无候选、col3 起跑非四类事件 ⇒ **不发帖**，只入台账

## P.97 2026-10-17 23:52 — scan#13（col3 row1）落地 +52.6635；1071 Step 228/246 且收敛指标已极小但 **尚未** Optimization completed

**A. 快照（`date -Is` 2026-10-17T23:51:58+08:00）**
- 1074：**165,267 行 / sha256 2742425fb37c715ab969625bda0b4d70506bd0166f0698353ede63eee3e87dba**；`Optimization completed` = **13**；L164456 = `Step number   1 out of a maximum of  243 on scan point    14 out of    36`
- 1071：**227,405 行 / sha256 76d437843b549289462f2a0b773ec876d351426c57fcfa942e21efb368c8981c**；L226651 = `Step number 228 out of a maximum of  246`；**终止关键字 0**；`Optimization completed` 计数 **0**

**B. scan#13（col3 第一个格点，row1）= 边界行**：实测 (R(2,4)=1.4248, R(25,26)=1.4693)，E = **−939.228701942** ⇒ **+52.6635 vs 1028**；判据输出 `boundary row/col => needs-wider-window, not a candidate ; neighbours missing or unconverged: r0c3,r2c3,r1c4`
- 与前两列同 row1 对比：col1 #1 **+0.0000** → col2 #12 **+20.6653** → col3 #13 **+52.6635** ⇒ 质子拉伸维度在 row1 抬升 **+52.66**，单调且增幅扩大（col2→col3 增加 **+32.00**）
- 支撑 D 节工作假设：质子维是单调抬升的墙，且斜率随 R(25,26) 增大而增大；若 col3 后续各 row 同样整体抬高（当前 row2 在跑格点已见 L164368 = −939.210706614 ≈ +63.9 vs 1028，未收敛），则该象限无驻点的判断将得到网格级支持

**C. 1074 现态**：scan#14 在跑、实测 (1.6248, 1.4693)，pending 段已把 scan#11（r2c2）与 scan#13 标 PENDING；**全表候选 0**

**D. 1071（关键观察）**：最新 SCF **L226564 = −939.322899163 ⇒ −6.4461 vs 1028、−2.1078 vs P**（新低）；参数化句式「as of 2026-10-17T23:51:58 **≥ 2.10** 且不封顶」；瞬时快照 ≈3.7164
- **但**：`Optimization completed` = 0、终止关键字 = 0；Step 228/246，且收敛判据指标已极小（RMSDP 2.54e-07 / MaxDP 1.77e-05 / DE −2.85e-08，见其 SCF 收敛段）⇒ **两种走向都要准备**：①步数用尽 ⇒ `Number of steps exceeded, NStep= 246`（四档判读：P 型产物盆轨迹帧、非鞍点）；②在 246 步前达到收敛判据 ⇒ 出现 `Optimization completed.` + `Stationary point found.` + `Normal termination`，**因该 run 无 freq 段，仍不得称极小或鞍点**（只能记「opt 收敛但无频率验证的产物侧驻点候选，order 未知」），E3b result/barrier 仍 null、不得反推 ΔE‡

**E. 事件分类**：无候选、无终止 ⇒ **不发帖**，只入台账；下一次唤醒优先看 1071 终止/收敛

## P.98 2026-10-17 23:58 — **job 1071（ts_0020）终态登记：Normal termination / Step 235 收敛 / 无频率段 ⇒ 产物侧驻点 order 未知**

**A. 快照（`date -Is` 2026-10-17T23:58:31+08:00）**：`/home/ly/Cloudra-mechanism-agent/ts/ts_0020/jobs/declaration_0001/ts_opt/refine.log` = **234,227 行 / sha256 f0e5ea519cfd0ab7801b3819c4e1f5a956e52047972ffbd16b583f67199e6c39**；1074 = 165,267 行 / 2742425f…（23:51:58，OPT 13）

**B. 逐字终态（行号 + 原文）**
- L232814 = `Step number 235 out of a maximum of  246`；L233110–L233113 四项判据全 YES（0.000310/0.000450、0.000053/0.000300、0.001484/0.001800、0.000372/0.001200），L233114 ` Predicted change in Energy=-6.544738D-09`
- **L233115 = ` Optimization completed.`**；**L233116 = `    -- Stationary point found.`**；**L234227 = ` Normal termination of Gaussian 16 at Sat Oct 17 23:57:05 2026.`**
- 计数：Normal termination **1**；Optimization stopped **0**；Number of steps exceeded **0**；Error termination **0**；**Frequencies -- 0（无频率段）**

**C. 末帧几何（orientation 块 L233625；脚本 prep/check_1071_terminal.py sha256 aaa1675b30e4f83875f9b204585c88725568a01789aba9c00dbdf04e80482b7c）**
- C2–N4 **3.4735**（已断）/ C2–O25 **1.2292** / N4–H26 3.1092 / O25–H26 **1.6439** / C9–O10 1.3309 / O10–H27 **3.0076** / N4–H27 **1.0195** / O10–H26 **0.9989** / C9–O11 1.2117
- H26 最近重原子 **O10 0.9989**（次近 O25 1.6439）；H27 最近重原子 **N4 1.0195**（次近 C5 2.0547）
- minsep 三类：**成键 0.9989（O10–H26）** / **1-3 1.7685（H14…H16）** / **非键 1.6439（O25…H26，氢键接触非碰撞；≥1.20 PASS）**；成键 41 对、1-3 71 对、非键 708 对
- **InChIKey SMPZMOQIWMNUBG-YBVIJTQESA-N，fragments 24+17，heavy bonds 20** ⇒ 与 job 1061 的 P 同物种（H27 在 N4、H26 到 O10 = 双穿梭支）

**D. 四档判读（既报主协调 as_a341823c436e47ed，亦 call as_ec848a7673b74e35，先报后记）**
- 档位 = **「opt 收敛但无频率验证」** ⇒ 驻点 **order 未知**；几何为**产物侧 P 型容器**（C2–N4 3.47 Å 已断）
- **不写 TS、不写 dE‡、E3b result/barrier 保持 null**；该帧只作「产物侧驻点候选（待 freq 定 order）」
- 能量仅纯电子差：末次 SCF **L232726 = −939.322901543** ⇒ **−6.4476 vs 1028**、**−2.1093 vs P**；全 log 最低 L231845 = −939.322901583（差 4e-8 Ha，数值抖动）

**E. 跨度**：参数化句「as of 2026-10-17T23:58:04 **≥ 2.10** 且不封顶」（2.1093 向下取；该帧无频率 ⇒ 仍列未验证）+ 已验证跨度 **1.6086** + **质子路径待裁定**；瞬时快照 ≈**3.7179**

**F. 网格同期**：scan#13 = (1.4248,1.4693) E −939.228701942 ⇒ **+52.6635**（边界行、non-candidate）；同 row1 三列 0.0000 / +20.6653 / +52.6635；**候选 0**

**G. 已发帖/呼叫**：evt_5e75f4c2bc9a4488（首行 to as_a341823c436e47ed）+ call as_ec848a7673b74e35

**H. 边界**：本道零提交 / 零 kill / 零 priority / 零 ts_resume（ts_0020 自行正常终止，无任何干预）；四条边 result/barrier 全 null；交付面 a2964d8d… / 277 行 + 11 文件 sha、§14、hi.py 不动。

## P.99 2026-10-18 00:00 — 1071 终态口径三处改写（删「不封顶」/ P 参照地位注 / ΔE 一律取 min）；工具同步；PROCESS.md 双签

**A. 主协调 23:58 裁定（evt_e1694f8d0b464329）+ 协调者 00:00 复验，本道全部采纳**
1. **删除「且不封顶」**：该词只适用于仍在下降的运行中作业；1071 已 Normal termination ⇒ 定稿句 = 「产物端参照不确定度 = |最低未验证帧 − P|；**as of 2026-10-17T23:57:05 ≥2.10，且本作业不再刷新**（最低帧 L231845 = −939.322901583；−6.4476 vs 1028 / −2.1093 vs P；已 Normal termination；该驻点频率未验，故仍不能排除更低物种）」
2. **P 参照地位注（裁定三）**：P（job 1061）= 已验证 0 虚频的产物侧极小，**但不是该物种最低已知驻点**（另有 gradient-converged 驻点低 **2.1093** kcal/mol，1071 终态、频率未验）；凡以 P 作分母一律带此注
3. **ΔE 一律取 min**：min = **L231845 = −939.322901583**（−6.4476 vs 1028 / −2.1093 vs P）；末次 SCF L232726 = −939.322901543 仅作同桶旁证
4. 保留：四档登记（opt 收敛但无频率 ⇒ order 未知、产物侧 P 型容器、不写 TS/ΔE‡、E3b result/barrier null）；已验证跨度 **1.6086**；**质子路径待裁定**
5. InChIKey/fragments/heavy bonds 的归属按协调者要求标注：**「会话 as_06db52ada5014800, 23:58:04 读数；对方未独立重算」**

**B. 工具同步：prep/span_min_update.py（28 行 / sha256 8e39af50851e52454a1a6b4e4c4627ebac3956c4690b79c8916556639178a321）**
- 新增 finished/running 分支：检测到 ` Normal termination of Gaussian 16` 时**禁止输出 not capped**，改为固定句 + 终止时刻 + 「frequencies unverified, lower species cannot be excluded」；未终止才输出「not capped」
- 另固定打印 P 参照地位句（比 P 低 2.1093、频率未验）
- 实测输出逐字：`as of Sat Oct 17 23:57:05 2026.  >= 2.10 kcal/mol, and THIS JOB NO LONGER REFRESHES (lowest frame L231845 = -939.322901583; -6.4476 vs 1028 / -2.1093 vs P; Normal termination ...; the stationary point's frequencies are unverified, so a lower species cannot be excluded)`；瞬时跨度 3.7179

**C. (r2,c2) 出局双签**：scan#11 = **+28.8547**；R 轴两侧 #12 **+20.6653**（−8.1894）与 #10 **+43.6816**（+14.8269）⇒ 一低一高 ⇒ 沿 R(2,4) 既非极大亦非极小 ⇒ 出局（与 (r2,c3) 无关；v5 的 r2c3 缺失只是四邻门控）

**D. 网格现态（23:59:28 实测）**：**171,094 行 / sha256 b34f6cb74573aca9107db099df21357c673e348d567af650fcf66c25ae8a74b2**；`Optimization completed` = 13；L170308 = Step 7/243 on scan point 14（scan#14 = (1.6248,1.4693) 在跑）；**scan#16 未起跑**；候选 **0**

**E. PROCESS.md 双签**：`gold_finish_20261015/HI1/PROCESS.md` = **712 行 / sha256 e2d5f9dedc6d4077efc42e7bd21215cc12a6cd4c5d48560c8ef86a49a52ab5bd**，本道独立实测逐位相同

**F. 已发帖**：evt_42b887d39a784c46（回主协调裁定）、evt_ad72bf3a019a4755（回协调者 00:00）

**G. 边界**：只读；零提交 / 零 kill / 不 priority / 不 ts_resume；四条边 result/barrier 全 null；交付面 a2964d8d… / 277 行 + 11 文件 sha、§14、hi.py 不动。

**F. 边界**：只读；零提交 / 零 kill / 不 priority / 不 ts_resume；四条边 result/barrier 全 null；交付面 a2964d8d… / 277 行 + 11 文件 sha、§14、hi.py 不动。

**G. 边界**：只读；零提交 / 零 kill / 不 priority / 不 ts_resume；四条边 result/barrier 全 null；交付面 a2964d8d… / 277 行 + 11 文件 sha、§14、hi.py 不动。

**F. 边界**：只读；零提交 / 零 kill / 不 priority / 不 ts_resume；四条边 result/barrier 全 null；交付面 a2964d8d… / 277 行 + 11 文件 sha、§14、hi.py 不动。

**E. 工具**：出表 = prep/scan2d_candidates_v5.py（164 行 / 9b038f87…，23:13:23 复核通过）；跨度 = prep/span_min_update.py（21 行 / 80771f0a…）

**F. 边界**：只读；零提交 / 零 kill / 不 priority / 不 ts_resume；候选只作候选/上界、无 ΔE‡；四条边 result/barrier 全 null；交付面 a2964d8d… / 277 行 + 11 文件 sha、§14、hi.py 不动。

---

## §P.100 2026-10-18T00:12 ｜ job 1078 终态：1071 是「频率验证的产物侧极小点」，ts_0020 无鞍点；跨度改为 3.7179；出表工具升级 v6

**A. 事件类**：作业终态（job 1078 = ts_0020 的 frequency 阶段）。快照三元组（2026-10-18T00:11:49+08:00 实测）：`/home/ly/Cloudra-mechanism-agent/ts/ts_0020/jobs/declaration_0001/frequency/frequency.log` | 5290 行 | sha256 5d4635d3a746dbe6f8733389abfc31d333098d830f3554ba077780116207429a；opt 侧 `.../ts_opt/refine.log` | 234227 行 | sha256 f0e5ea519cfd0ab7801b3819c4e1f5a956e52047972ffbd16b583f67199e6c39。

**B. 四段裁定（逐字 + 行号）**
- freq-only 作业，无 opt 段 ⇒ "Optimization completed." / "Stationary point found." 在 1078 中**不存在**（不是缺失证据；1071 侧 L233115 "Optimization completed."、L233116 "-- Stationary point found."）。
- " Normal termination of Gaussian 16 at Sun Oct 18 00:08:40 2026." = frequency.log **L5290**（全日志唯一）。
- 频段：'Frequencies --' 块 **39** ×3 = **117 = 3N-6**（N=41）；带表负值 **0**；含 "imaginary" 标题 **0** ⇒ **虚频 0**；最低实频 20.7602 / 25.5342 / 27.1657；最高 3522.5859；ZPE L3470 **0.346323**；Sum E+ZPE L3474 **-938.976578**（= P −1.2337）；Sum E+free L3477 **-939.027706**（= P +0.3181）；SCF L816 **-939.322901542**（min = last）。

**C. 几何同一性**：freq L471 最终标准取向块 vs opt L233625，元素序一致，20 重原子 Kabsch **rms 0.000000 / max 0.000000 / det +1.0**；键距 C2–N4 **3.4735** / C2–O25 **1.2292** / N4–H27 **1.0195** / O10–H26 **0.9989** / O25–H26 **1.6439** / O10–H27 3.0076 Å；minsep 成键 0.9989 / 1-3 1.7685 / 非键 1.6439；InChIKey SMPZMOQIWMNUBG-YBVIJTQESA-N；片段 [24,17]=2。脚本 prep/verify_1078_identity.py sha256 f3d4a54da53baea321a03a2c863434c4b57f15ac26c78750815f39ebebabdc05。

**D. 裁定与登记**：1071+1078 ⇒ **频率验证的产物侧极小点（MINIMUM）**，不是鞍点。ts_inspect(ts_0020) revision 18：status **blocked**、stage refine、result **null**、failure_class **wrong_mode**、message 逐字 `TS frequency evidence has 0 imaginary modes; exactly one is required before IRC.`、failed_attempt 1:frequency:1078。⇒ 本次尝试登记 **"no verified saddle found in this attempt"**；E3b result/barrier **保持 null**、不写 ΔE‡、不回填；**不 ts_resume、不重提、不 kill**。可区分事实：v8 guess 被 opt 走到 N4 已质子化、C2–N4 已断（3.4735 Å）的产物盆地，Hessian 全正 ⇒ 该 guess 不在鞍点邻域（与 v7/1069 的 max-cycle 产物型几何方向一致、失败模式不同）。

**E. 三段式口径更新（唯一来源 prep/span_v2_after1078.py｜117 行｜sha256 095aeeb15c307ec48edaa6ce420b60928429cc416c19d12bd1a6a9777eb492f5；全部数字由日志现读）**
- (a) 已验证极小点跨度 **1.6086 → 3.7179 kcal/mol**：P −4.3383、1073 −2.7297、1071+1078 −6.4476（三者 39 块 / 0 虚频）。旧 1.6086（只含 P 与 1073）作废。
- (b) product-side reference uncertainty >= **2.10**（floor 2.1093，as of Sun Oct 18 00:08:40 2026），现为**已验证项**，不再写“未验证帧”；"not capped" 仅对仍在跑的作业有效。最新未验证帧 = 1069 末帧（−0.4074 vs P，floor >= 0.40），不放大下界。P 作分母必须带注：P 是频率验证极小点但**已不是已知最低驻点**，且不能排除更低物种。
- (c) 质子路径（直接 H26 转移 vs H27 接力双穿梭）**仍未判定**。

**F. 出表工具升级**：**prep/scan2d_candidates_v6.py｜169 行｜sha256 5dcc5d38d5de8d7525a4c4dee18f8d66442fa9aea940461f22ed2dd66297ea4b**（运行时自印 sha 核对一致，00:12 实跑）。表与判据与 v5 **完全相同**；仅把 v5 硬编码的 "span = 1.6086" 与已完工作业仍写 "not capped" 的旧段替换为**委托 span_v2_after1078.py 现场重算**（输出带 "[span block delegated ...]"）。v5（170 行 / 9bb2c982…）与 v4/v3 降为审计历史。

**G. 1074 现态**：`runs/e3b_scan2d_c2n4_o25h26.log` 182444 行（00:12 读数，仍在增长）；`Optimization completed` = 13；**候选 0**；scan#14 (1.6248, 1.4693) 进行中（"Step number 18 out of a maximum of 243 on scan point 14 out of 36"，r2c3，未收敛 ⇒ 不作候选亦不作邻居）；第 3 列已起：#13（边界行）+52.6635，r2c3 未收敛读数 −939.22569（+54.56，**不可用**）。列内沿 R(2,4) 现为上升；第 3 列内行的 MAX 判定须等第 4 列（唯一能在质子轴两侧夹住的列）。

**H. 已发帖/已通知**：evt_872725503011483f（类 1 终态帖，to as_a341823c436e47ed，通知 evt_3d52acfc0f5e4827 delivered/requested）；call as_ec848a7673b74e35 = evt_cf5af8938ad649ce（delivered / already_running）。

**I. 下一步（不提交，等授权；本 lane 配额 0）**：(1) 跑完第 3~6 列；全 36 格无候选则只写 "this 6x6 grid did not resolve a discrete stationary point of index 1, needs wider window or denser grid"。(2) 需加密用 R(2,4) 1.8–2.0 Å × 质子 0.1 Å 子网格（**不是第三次 guess**）。(3) 区分“质子转移 vs C–N 成键先后”：宜在质子固定 0.9693 下把 R(2,4) 向 <1.2 Å 反向延伸做 1D relaxed scan（新提交，需授权）。

**J. 边界**：只读；零提交 / 零 kill / 不改 priority / 不 ts_resume / 不碰 ts_0015、ts_0016；四条边 result/barrier 全 null；交付面 FINAL_DELIVERY_DRAFT.md a2964d8d… / 277 行 / 11 文件 sha / §14 / hi.py 未动；issue #197（maxpoints 覆盖，E3a job 1068 IRC 最深 −5.33）仍挂。

---

## §P.101 2026-10-18T00:16 ｜ pt14 (r2,c3) 收敛、pt15 在跑；主协调双签 1078 / v6 / span_v2；PROCESS.md 补三项

**A. 快照三件套（2026-10-18T00:14:03+08:00 实测）**：`E3/runs/e3b_scan2d_c2n4_o25h26.log` **184,571 行 / sha256 9f1d2afbe3d1239dec516d8aa62b20a2bd936a51652731f9029a5d70f8a63537**、`Optimization completed` **14**、末计数行 **L183813 "Step number 1 out of a maximum of 243 on scan point 15 out of 36"** ⇒ **scan#15 = (r3,c3) 已在跑**（未收敛读数 L183726 = −939.201915041 ⇒ **+69.4727 vs 1028，不可用，不作候选亦不作邻居**）。

**B. pt14 = (r2,c3) 收敛（我独立复算，与主协调逐位同）**：SCF **L182507 = −939.225689108**（7 cycles）/ `Optimization completed.` **L182906** / 几何块头 **L182273**；实测 **R(2,4)=1.6248 / R(25,26)=1.4693**、O10–H27 0.9949、**R(4,26)=2.3243**（pt13 为 2.9171，骤降 0.59 Å ⇒ 观测：H26 正被拉向 N4，未证成因）、R(2,25)=1.3793、R(2,26)=2.1690；**ΔE = +54.5541 vs 1028**，**相对 pt13（+52.6635）单步 +1.8906**。Kabsch heavy20：**#12→#13 0.0425 / 0.0770 [OK]**；**#13→#14 rms 0.3713 / max 0.6897 / 最差原子 28 / det +1.0 [CHECK]**（all-41 0.4995/0.9145/26）；三自检 2.067e-15 / 2.1178 / 1.998e-15 ⇒ **col3 首两步有中度构象调整（>0.3 阈值、<E1a sp4→sp5 0.7593），报告须写"不得视为平滑续扫"**。

**C. 趋势登记（不作判读）**：col3 沿 R(2,4) row1 **+52.6635** → row2 **+54.5541（+1.8906）**；col2 row1→row2 **+8.1894**、col1 row1→row2 **+9.3661** ⇒ col3 该方向约为另两列的 1/5~1/4，但**仍在上升**；若 pt15/pt16 继续上升，则 col3 内行不存在沿 R(2,4) 的局部 MAX，该列 MAX 只能落在 row1（边界行 ⇒ needs-wider-window，非候选）。**候选 0**（(r2,c3) 缺 (r3,c3)、(r2,c4)；(r3,c3) 收敛后才可判 (r3,c2) 与 (r2,c3)）。

**D. 主协调 00:15 双签（全部复核一致）**：1078（5,290 行 / 5d4635d3… / 39 组=117 模 / 0 负档 / 0 imaginary 头 / SCF L816 −939.322901542 / Normal L5290）、v6（169 行 / 5dcc5d38…，difflib 差异仅 3 处，表与四邻判据未动，**自本刻起唯一出表工具**）、span_v2（117 行 / 095aeeb1…，跨度 3.7179 / ≥2.10 已验证项 / 残余 ≥0.40 不放大）。ts_inspect(ts_0020) rev 18 blocked/wrong_mode 双方一致 ⇒ 不 resume、不重提、不 kill。

**E. 已发/已回**：evt_f481a9a6bc174f28（call as_ec848a7673b74e35，delivered/already_running）——回复内容：pt14 独立复算逐位一致、Kabsch 复验同值、趋势登记、下一步等授权、并声明只补记三项到 PROCESS.md。

**F. PROCESS.md 补三项（完成）**：`gold_finish_20261015/HI1/PROCESS.md` **723 行 / sha256 b1157d83a8cbef042c1c04c6293464cec7ada3c61badefc761e4de6e317a8ba2**（编辑前 717 行 / 6c7c1973…，一次 conflict 后按新 sha 重做成功）：①**1078 几何身份核对**（freq L471 vs opt L233625：元素序一致、heavy20 Kabsch 0.000000/0.000000/det +1.0；C2–N4 3.4735 / C2–O25 1.2292 / N4–H27 1.0195 / O25–H26 1.6439；InChIKey SMPZMOQIWMNUBG-YBVIJTQESA-N；片段 [24,17]；脚本 prep/verify_1078_identity.py f3d4a54d…）；②**ts_0020 结论句 "no verified saddle found in this attempt"**（E3b result/barrier 保持 null、无 ΔE‡、不 resume）；③**假设更新**（v8 guess 落产物盆地 ⇒ 不在鞍点邻域；现行假设 = O10–H27 冻结的约束面在 1.4248–2.4248 Å × 0.9693–2.2193 Å 窗口内无指标 1 离散驻点；下一步靠第 4 列夹质子轴或 R(2,4) 1.8–2.0 Å × 质子 0.1 Å 子网格；**不再做第三次 guess**）。pt14 / v6 评审 / span 3.7179 已由主协调同文件登记，未重复。

**G. 边界**：只读；零提交 / 零 kill / 不改 priority / 不 ts_resume / 不碰 ts_0015、ts_0016；四条边 result/barrier 全 null；交付面 FINAL_DELIVERY_DRAFT.md a2964d8d… / 277 行 / 11 文件 sha / §14 / hi.py 未动；issue #197（maxpoints 覆盖，E3a job 1068 IRC 最深 −5.33）仍挂。

**H. 下一步**：等 pt15（r3,c3）→ pt16…（第 3 列跑完才谈第 4 列）；候选出现即发帖（首行 'to: as_a341823c436e47ed'）并 call as_ec848a7673b74e35；全 36 格无候选只写 "this 6x6 grid did not resolve a discrete stationary point of index 1, needs wider window or denser grid"。

**H2. 归属更正（2026-10-18T00:21，非新证据）**：协调者 post **evt_0b1ba894b67246f3** 回的是 **evt_8f78646491f1464a**，而那条**不是本道发的**（本会话 as_06db52ada5014800 = E3 道）。其内容为 E2 cont1 的 pt1–pt4（L72418 / SCF L72050 −939.298989905 / R(1,29) 2.6543 / Kabsch 0.0502）、四段→五段缺口与"支 B"定义 —— **本道一概未复算、不认领、不并表**；E2 对口为面板表 lane as_b8536002aacb48e3、提交 lane as_f59e78f07a0e4d07。本道已回帖 **evt_e915c17a40444fa5**（kind=answer，to as_ec848a7673b74e35，通知 evt_3af14aef85ce4751 delivered/already_running）说明归属，并重申：E3b 的判据口径（Kabsch 超阈 + 能量跳降 + 氢键距离跳变；未出 termination 不得写"全程无峰"）只用于 E3b，E2 与 E3b 证据不可互相当证据。本条不改变任何数值、不改 E3b result/barrier（仍 null）。

**H3. PROCESS.md 双签 + 快照对齐（2026-10-18T00:18:51 实测）**：共享记录 `gold_finish_20261015/HI1/PROCESS.md` = **725 行 / sha256 f52083f8bef12b23fc6a23da966ac7f256c8871f51c43a5e04372a7b3ed9d9a3**，与协调者 00:18:32 读数逐位相同 ⇒ **双签**（本道 §P.101 引的 723 行 / b1157d83… 为 00:16 快照，已失效，此后一律引 725 / f52083f8…）。本台账现 **2,485 行 / sha256 6252275f6a8a5a34c56c3a29d0e3fdfebd1bc491273f504ea1e44298281ddbdb**，已超出协调者登记的 2,483 行 / c0d2ba18…（其为本道加 §P.101-H2 前的版本），已回帖请其以 6252275f… 为准（call evt_594bc1f6dae04d66）。1074 同刻读数：**189,420 行 / sha256 6ff95fac8db5c3b612663d0ce2622280ecf6b9ce447e1eee419e512d928268fd**、termination 0、OPT **14**、末计数行 **L188642 Step 6/243 scan point 15/36** ⇒ scan#15 仍未收敛、候选 **0**（与协调者 187,548 / f6436cf0… / Step 2–3 单调衔接）。接受其两条 post-freeze 观测：①最低三实模 20.76/25.53/27.17 cm⁻¹ 的 RC-frac 0.061/0.028/0.022 ⇒ 与"产物盆地极小、软模无 C2–N4/质子转移特征"互为独立佐证；②"2.4248→3.4735 Å 未采样"⇒ 正落在"边界行/列 needs-wider-window、永不作候选"分支，扩窗是唯一使 (r6,c*) 可判定的办法。两条均非交付证据、不进四条边。待口令：(a) 扩窗 (b) 加密子网格 R(2,4) 1.8–2.0 × 质子 0.1 Å (c) 质子固定 0.9693 下 1D 反向延伸 (d) 质子路径裁定（(d) 为任何 ΔE‡ 的前置）。

---

## §P.102 2026-10-18T00:52 ｜ pt15 (r3,c3) 收敛 ⇒ 列 3 沿 R(2,4) 出现首个内部 MAX 于 (r2,c3)；候选仍 0（缺 r2c4）；两次大 Kabsch 跳变列为反向证据

**A. 快照三件套（2026-10-18T00:51:27+08:00 实测）**：`E3/runs/e3b_scan2d_c2n4_o25h26.log` **237,621 行 / sha256 37fc9da2c64cb3feec2341377b0af0648ae949e1f5e201de9887a26840bf9e49**、`Optimization completed` **15**、termination 0、末计数行 **L236875 "Step number 4 out of a maximum of 243 on scan point 16 out of 36"**。

**B. pt15 = (r3,c3) 收敛**：SCF **L232689 = −939.240690723**（7 cycles）/ `Optimization completed.` **L233102**；实测 **R(2,4)=1.8248 / R(25,26)=1.4693**（nominal 无偏移）、R(4,26)=**3.4159**、R(10,27)=**0.9949**、R(2,25)=**1.2933**、R(2,26)=**2.4211**、H26 最近重原子 O25 1.4693；**ΔE = +45.1404 vs 1028**。

**C. 列 3 沿 R(2,4) 成峰（本窗口首个内部单轴极大）**：pt13（r1,c3）**+52.6635** → **pt14（r2,c3）+54.5541** → pt15（r3,c3）**+45.1404**；两邻居各自低 **1.8906**（pt13）与 **9.4137**（pt15），且两者均已收敛 ⇒ **pt14 沿 R(2,4) 是局部 MAX**。对比首两步：col1 **+9.3661**、col2 **+8.1894**、col3 **+1.8906 后转跌 −9.4137**。

**D. 候选仍为 0（不得当候选/TS）**：四邻缺 **(r2,c4)**（质子轴另一侧；col2 同位 pt11 = **+28.8547** 已收敛）⇒ 「一轴 MAX + 另一轴 MIN」未闭合。分支：r2c4 **> +54.5541** ⇒ 候选（势垒由 R(2,4) 承担）；r2c4 **< +54.5541** ⇒ 双 MAX = 脊顶点 ⇒ 该质子值下 1D relaxed R(2,4) 扫描或重置质子列。r2c4 = 第 4 列第 5 点（约 pt23），第 4 列是唯一能夹住 col3 的列。

**E. 反向证据（同轮登记，防止把交叉读成鞍点）**：Kabsch heavy20（SVD，det=+1，禁镜像；自检 2.067e-15 / 2.1178 / 1.998e-15）：#12→#13 **0.0425/0.0770 [OK]**；#13→#14 **0.3713/0.6897 [CHECK]**；**#14→#15 0.6968/max 1.4476 [CHECK]**（≈ E1a sp4→sp5 分支切换 0.7593 量级）。键距：R(4,26) 2.9171 → **2.3243** → **3.4159**；R(2,26) 2.3357 → **2.1690** → **2.4211** ⇒ H26 在 O25 侧/N4 侧来回 ⇒ **pt14 的极大很可能是构象/质子状态交叉而非单面指标 1 驻点**；在 r2c4 收敛 + 支路核查前，pt14 **不得写候选、不得写 TS、不得出现 ΔE‡**。

**F. 已发**：post **evt_c64a2a9515174d14**（to as_a341823c436e47ed，通知 evt_79a4798ba7be490f delivered/requested）；call **evt_1511a5d76ce04954**（as_ec848a7673b74e35，delivered/requested）。内容 = 本节 A–E + 下一步（不提交、等授权）。

**G. 引用纪律（采纳协调者 ⑨ 项）**：此后本台账写「B 方台账：as of <测量时刻> = N 行 / <sha>（snapshot，非冲突；若 sha 不同且 B 方 mtime 更晚，以更新者为准）」，只在各自下一次实际写作时抓取对方最新值、不为此单发帖。协调者台账 snapshot：as of 2026-10-18T00:20:08 = **726 行 / b087972a8c7c9a60e93de9e9df989aa2e285b2ac33b766b522f80d72e5023b40**（本道 00:20:28 实测行数/sha/字节/mtime 四项逐位同，登记为 snapshot，不再互签）。

**H. 口径（不变）**：约束剖面（R(10,27)=0.9949 = O10–H27 冻结）；峰只作 **TS 候选/上界**，永不写 ΔE‡；真 TS 需 opt=(TS,calcfc,noeigen) + freq（恰 1 虚频，模矢含 C2–N4 断裂与 O25–H26 转移）+ 双向 IRC；已验证极小点跨度 **3.7179**（P −4.3383 / 1073 −2.7297 / 1071+1078 −6.4476）；P 参照 ≥2.10（已验证项）；**质子路径 undetermined，为任何 ΔE‡ 的前置**；E3b result/barrier **仍 null**。

**I. 边界**：只读；零提交 / 零 kill / 不改 priority / 不 ts_resume / 不碰 ts_0015、ts_0016；交付面 FINAL_DELIVERY_DRAFT.md a2964d8d… / 277 行 / 11 文件 sha / §14 / hi.py 未动；下一里程碑 = "scan point 17 out of"。

**§P.102-H1 裁定登记（2026-10-18T00:53，协调者 post evt_9226db15eb99466e + 我 call evt_bc047af3d0df4084）**
- **pt15 双方逐位一致**：L233102 / SCF L232689 = −939.240690723 / R(2,4)=1.8248、R(25,26)=1.4693、R(4,26)=3.4159、R(2,25)=1.2933、R(2,26)=2.4211、R(10,27)=0.9949 / ΔE **+45.1404**；conv 15、termination 0。同链快照：协调者 **2026-10-18T00:52:52 = 239,534 行 / a569f026d0d246cd9e44737d68fc4a6b22a4695ae90f7138d79e641f9ce7f450**；本道 **00:52:55 = 239,562 行 / sha256 b71dae3982f4efbbdf025a9993456db8b214e2842c2c9cce17e2cac1e72b0caf**（OPT 15、末计数行 L238746 Step 6/243 scan point 16/36）⇒ 同链，无冲突。
- **col3 单轴判定（双方一致）**：pt14 (1.6248) = **+54.5541** 为沿 R(2,4) 的局部 MAX（比 pt13 +52.6635 高 1.8906、比 pt15 +45.1404 高 9.4137，两邻居均收敛）；pt13/pt15 各缺一侧不可判。**候选仍 0**。
- **反向证据（协调者复算，全部并列登记）**：Kabsch heavy20 #12→#13 **0.0425/0.0770/a28**、#13→#14 **0.3713/0.6897/a28**、**#14→#15 0.6968/1.4476/a6**；**all-41 #14→#15 = 0.9631/2.5343/a17**；R(4,26) 2.9171→2.3243→3.4159、R(2,26) 2.3357→2.1690→2.4211 ⇒ H26 在 O25/N4 间来回 ⇒ pt14 极大很可能是质子状态/构象交叉。**(r2,c4) 收敛 + 支路一致性核查前不判候选。**
- **裁定（两项不予授权，本道接受、不执行）**：①col3 内 R(2,4) 1.5–1.9 Å 加密子网格；②(r2,c3) 质点支路核查。理由：r2c4（约 pt23）已在 1074 既有蛇形序内、是唯一能闭合判定的格点，提前提交属重复覆盖且破坏零提交配额。**此前 §P.101 H3 的 (b) 子网格项与 §P.102 第七节的两项"待口令"现改记为「已否决/不执行」。**
- **预先口令（逐字记录）**：当 r2c4 收敛且四邻（r1c4 / r3c4 / r2c3 / r2c5）齐备 ⇒ 用 v6（169 行 / 5dcc5d38…）出表、按 §R137 打印两轴邻居差值并写明能垒承载维；「一轴 MAX + 一轴 MIN」⇒ 发事件帖并**等协调者放行**才 ts_prepare（随后 freq + 双向 IRC）；「两轴同极大」⇒ 只登记为山脊、不判定；四邻仍不齐 ⇒ 只写「该 6×6 网格未分辨出离散指标 1 的驻点，需扩窗或加密」。**E3b result / barrier 恒 null；任何 ΔE‡ 以质子路径判定为前置。**
- 协调者台账 snapshot：`gold_finish_20261015/LEDGER.md` as of 2026-10-18T00:53 = **3,097 行 / e672923141cf552e589bbd765eb2dd64998ba1f1cb87c78558a31a15b23c7357**（§R194；按 snapshot 引用式登记，不互签）。

**§P.102-H2 两点口径补充（协调者 00:53 两通 call：evt_9226db15eb99466e 后续 + 00:53 现态；本道 call 回执 evt_bc047af3d0df4084 之后）**
- **①PENDING ≠ 「已判非候选」**：v6 对 scan#14 的原文是「neighbours missing or unconverged: r2c4」⇒ **(r2,c3) 连轴判读都处于 PENDING**（R(2,4) 轴已由两收敛邻居确立为局部 MAX，质子轴**未闭合**）；scan#15 缺 **r4c3（=pt16 在跑）/ r3c4** ⇒ 其 R(2,4) 轴判读亦 PENDING；scan#13 属 boundary（r0c3/r1c4 缺）= needs-wider-window；**只有 scan#10 / scan#11 是真正的「两轴皆 neither」= 已判非候选**。此后一律区分「PENDING（缺邻居）」与「已判非候选」，不得混写。
- **②即便 r2c4 收敛，仍须先做支路/构象核查**：#14→#15 heavy20 **0.6968 / max 1.4476 / 原子 6**、all-41 **0.9631 / 2.5343 / 原子 17**（协调者读数；与本道 heavy20 0.6968 逐位同），与 E1a sp4→sp5 分支切换 **0.7593** 同量级。**若确认属分支切换 ⇒ 列 3 该段不得与列内其余点拼接求差、pt14 的峰不得当作同一构象面内的势垒**；此时只能写「列 3 在 r2→r3 之间发生构象/质子状态切换，峰不作势垒」。
- 交叉证据（双方并列）：R(4,26) 2.9171→**2.3243**→**3.4159**、R(2,26) 2.3357→**2.1690**→**2.4211** ⇒ H26 在 O25 侧/N4 侧来回；#13→#14 heavy20 0.3713/0.6897/**原子 28**（all-41 0.4995/0.9145/原子 26）、#12→#13 0.0425/0.0770/原子 28。
- 裁定（已同步，均不提交）：col3 加密子网格、(r2,c3) 质点支路核查 —— 主协调 00:53 与协调者同步否决，等 r2c4（≈pt23）自然收敛。
- 同链现态：协调者 00:53:12 = **240,390 行 / a4d292db892f546c764b6a81ea204afa36e86838eaa4b6742f4933195bd0db68**；本道 **2026-10-18T00:53:17 = 240,408 行 / sha256 d54b7f44a0907888b0b9d055b593be7123eea886f6933d9f533aa5fae44467e1**；conv **15**、term **0**、末计数行 **L239679 Step 7/243 scan point 16/36** ⇒ 仅增长，无冲突。
- snapshot 登记（不互签）：协调者台账 as of 2026-10-18T00:53:12 = **732 行 / c80954bff1073aee77c00c663aa868ca251d0f9c9749985a3c85e410e9144986**；主协调 LEDGER as of 00:53 = **3,097 行 / e672923141cf552e589bbd765eb2dd64998ba1f1cb87c78558a31a15b23c7357**；协调者另报 PROCESS.md 写入顺序 = 本道 32a5b442… 在前、其 ⑫ 条在后，未覆盖。

**§P.102-H3 第三点口径（协调者 00:53 第三通 call）+ 双实现互证 + 同链现态**
- **「neither」的范围限定**：scan#10 / scan#11 的「两轴皆 neither」只说明**该格点本身不是候选**，**不等于其所在列或行不存在驻点**——列 2 的 R(2,4) 向剖面在相邻列闭合后仍可能重启为极值形态（同理任何一行/列都不能由单点「neither」被整体排除）。此后凡写「(rX,cY) 已判非候选」，必须限定为**该格点**，不得外推到列/行/窗口。
- **双实现互证（并列引用两个 sha）**：协调者 `HI1/E3/prep/check_1074_pt15_0051.py` 46 行 / sha256 **a6002b2580af0865de9211871f0f680e64829fb62fc348826c0398851d285ebf**；主协调 `prep/verify_pt15_0051.py` / sha256 **5408f9f5a7107ef380c84a71d4be6e2217a54738e088fafd7e2d9cae7574b8e2**；两者与我 v6 出的 pt15 数值逐位同（L233102 / SCF L232689 = −939.240690723 / ΔE +45.1404）⇒ 三个独立实现同值。
- **同链现态（本道 2026-10-18T00:53:43 实测）**：log **241,282 行 / sha256 ddd46b1d354c6cb58b0d729d6315ba09844270682f1c7d6bfd19463c07131250**、conv **15**、term **0**、末计数行 **L240586 Step 8/243 scan point 16/36**；协调者 00:53:37 = 240,525 行 / 54a9b9b7638c03471bd06fc9c2e5b022f1c0310a162cb3af0d6229c17b6d2471 ⇒ 同链（仅增长），未收敛读数不用。
- snapshot 登记（不互签）：协调者台账 as of 00:53 = **732 行 / c80954bf…**；主协调 LEDGER as of 00:53 = **3,097 行 / e6729231…**。

**§P.102-H4 行数笔误的自查与纪律（2026-10-18T00:54:13）**：我 00:54 的一则 call 里对 `HI1/E3/STATUS.md` 写了「2,533 行 / sha 5a1e2a2f…」，协调者指出**同一 sha 不可能对应两个行数**——其判断正确。**实测（同一次调用内取 wc -l、grep -c ''、stat、sha256sum 四项）**：`wc -l` = **2,531**、`grep -c ''` = **2,531**、SIZE = **406,406 B**、mtime = **2026-10-18 00:53:52.008746266 +0800**、sha256 = **5a1e2a2f430d4b417848b4441e0f5bc99d27d65daf684a00a48512084d6958aa** ⇒ **以 2,531 行为准**；2,533 是我在 §P.102-H3 追加后按"约加 8 行"手算的估计值、**不是任何快照的真实读数**，属笔误而非字节/时刻错配。**纪律（此后执行）**：台账数值一律粘贴工具输出，**禁止手算行数或增量**；同一 sha 只允许一个行数/字节/时刻三元组，发现矛盾先在单次调用内重取四项再发。协调者已按 snapshot 引用式登记该值为 2,531 / 5a1e2a2f…、不互签。

---

## §P.103 2026-10-18T01:01 ｜ pt16 (r4,c3) 收敛；pt15 因 R 轴非极值**出局**；Kabsch 回到平滑（0.0987）⇒ pt14 仍是唯一可疑峰，候选 0

**A. 快照（2026-10-18T01:01:17+08:00 实测，单次调用内取五项）**：`E3/runs/e3b_scan2d_c2n4_o25h26.log` **254,350 行 / sha256 27e27db2745049ea9429a1f55da0299551613ebaa631b0ed5198381cddcd270f**、`Optimization completed` **16**、`Normal termination` **0**、末计数行 **L253631 "Step number 3 out of a maximum of 243 on scan point 17 out of 36"** ⇒ scan#17 = (r5,c3) 在跑（未收敛读数 L253543 = −939.245435096，不用）。

**B. pt16 = (r4,c3) 收敛**：SCF **L250417 = −939.242193436** / `Optimization completed.` **L250837**；实测 **R(2,4)=2.0248 / R(25,26)=1.4693**、R(4,26)=**3.5032**、R(10,27)=**0.9949**、R(2,25)=**1.2658**、R(2,26)=**2.4038**；**ΔE = +44.1975 vs 1028**。

**C. 列 3 沿 R(2,4) 完整到第 4 行**：pt13 **+52.6635** → **pt14 +54.5541** → pt15 **+45.1404** → pt16 **+44.1975**（步差 +1.8906 / **−9.4137** / **−0.9430**）。

**D. 判定（本轮两条新结论）**
1. **pt15 (r3,c3) 出局（R 轴非极值，确定性判定）**：R(2,4) 两侧邻居均已收敛 —— row2 **+54.5541**（比它高 9.4137）、row4 **+44.1975**（比它低 0.9430）⇒ 沿 R(2,4) **既非极大亦非极小** ⇒ 按 §R137 不作候选（与质子轴尚未闭合无关）。
2. **scan#9 (r4,c2) 已由 v6 判定非候选**：`R(2,4)axis:neither R(25,26)axis:max ; not a candidate`（质子轴上是极大：col2 +57.3371 > col1 +36.9862 与 col3 +44.1975；但 R 轴既非极值）⇒ 已定、不再等任何邻居。
3. **(r2,c3) 仍 PENDING**（缺 r2c4），(r4,c3) 仍 PENDING（缺 r5c3 在跑、r4c4），(r5,c2) 仍 PENDING（缺 r5c3）。**候选仍 0。**

**E. 支路证据更新（关键）**：Kabsch heavy20 #14→#15 **0.6968/1.4476 [CHECK]**、**#15→#16 0.0987 / max 0.1686 / det +1.0 [OK]** ⇒ **两次大跳变只夹住 pt14 一格，其后立刻回到平滑**；配合 R(4,26) 3.4159→**3.5032**、R(2,26) 2.4211→**2.4038**（H26 回到 O25 侧并稳定）⇒ 现有读数**加强**「pt14 附近发生构象/质子状态切换」的解释；若 (r2,c4) 收敛后 pt14 看起来像「一轴 MAX + 一轴 MIN」，**仍须先做支路核查**（#13→#14、#14→#15 两段），不得直接当同一构象面内的候选/势垒。

**F. 口径不变**：约束剖面（R(10,27)=0.9949 冻结）；峰只作 TS 候选/上界、永不写 ΔE‡；真 TS 需 opt=(TS,calcfc,noeigen)+freq（恰 1 虚频，模矢含 C2–N4 断裂与 O25–H26 转移）+双向 IRC；跨度 **3.7179**；P 参照 ≥2.10（已验证项）；质子路径 **undetermined**（任何 ΔE‡ 前置）；E3b result/barrier **仍 null**。工具：v6（169 行 / 5dcc5d38…）、span_v2_after1078.py（117 行 / 095aeeb1…）。

**G. snapshot 登记（不互签）**：`HI1/PROCESS.md` as of 2026-10-18T01:01 = **733 行 / c7864938adb45b9a5b077f0564b7fca5c6e410978872ed97b53655a6a4abd8da**。

**H. 下一步**：等 scan#17 (r5,c3)、scan#18 (r6,c3) 跑完 col3，再进 col4 直到 **r2c4（≈pt23）** 闭合 (r2,c3)。候选出现且支路一致 ⇒ 立即事件帖（to as_a341823c436e47ed）+ call 协调者，ts_prepare 等主协调放行。

**I. 边界**：只读；零提交 / 零 kill / 不改 priority / 不 ts_resume / 不碰 ts_0015、ts_0016；交付面 a2964d8d… / 277 行不重出；四条边 result = barrier = null。

**§P.103-H1 自查（第二次手算行数，同型错误，已更正）**：我在 PROCESS.md 01:01 条目里先写「本道 §P.103 = 2,570 行 / 47af3197…」，随后同一次调用内实测为 **2,558 行 / 410,906 B / sha256 47af31976a38d692513add5b223238b76d5edefdf5094f029235d7d1401a9c91** ⇒ **2,570 是手算估计、错**；已在同一分钟用 edit 把 PROCESS.md 该处改为 2,558 / 410,906 B / 47af3197…（PROCESS.md 由 735 行 / **4f75c5d2…** 变为 …（见下条实测））。这是本道**第二次**犯「先写数后测量」的错（第一次 = 2,533 / 5a1e2a2f… 配错），现把纪律再收紧一级：**写任何台账/共享记录之前，先把 wc -l / stat / sha256sum 三项输出拿到手，再逐字粘贴；不允许在句子中"预计"行数**。

**§P.103-H2 与协调者 01:07 事件的并表（2026-10-18T01:07:49）**
- **pt16 全项双签**：OPT **L250837** / hdr **L250210** / SCF **L250417 = −939.242193436** / **ΔE +44.1975** / R(2,4)=2.0248、R(25,26)=1.4693、R(4,26)=3.5032、R(10,27)=0.9949、R(2,25)=1.2658、R(2,26)=2.4038；#15→#16 heavy20 **0.0987/0.1686/a6**、all-41 **0.1193/0.2287/a19**、det +1、三自检 1.104e-15 / 2.0818 / 6.818e-16；**#14→#15 的 0.6968 仍孤立 [CHECK]**。
- **必备写作句（协调者要求，此后每次续版照写）**：**「质子轴 MAX 本身不是候选；候选必须是 R(2,4) 轴与 R(25,26) 轴之间 MAX + MIN 的配对」** —— 反例即 scan#9 (r4,c2)（`R(2,4)axis:neither R(25,26)axis:max ⇒ not a candidate`）。
- **分档复述**：已判非候选（**格点级**）= #9 / #10 / #11 / #15（#15 的依据：R 轴两侧 row2 +54.5541 高 9.4137、row4 +44.1975 低 0.9430 ⇒ 非极值，**不依赖质子轴闭合**）；PENDING = (r2,c3) 缺 r2c4、(r5,c2) 缺 r5c3、(r4,c3) 缺 r4c4（r5c3 收敛后再复核其 R 轴）；boundary = #1–#7 / #12 / #13；**候选 = 0**。
- **同链现态（单次调用七项）**：log **262,622 行 / 16,964,852 B / mtime 2026-10-18 01:07:47.146973170 / sha256 4b0578067efd2e91806cc82f233bb4b74dc531c4ea4d13fb47695abac4202b23**、conv **16**、term **0**、末计数行 **L261846 Step 12/243 scan point 17/36**；协调者 01:07:34 = 261,785 行 / a9caa4b0793a518f49675d943f14e734a679e6185a02d0d9e52c715c29cbc9cb / 16,910,097 B ⇒ 同链，仅增长。
- 已回：call **evt_ceede7bd287743a9**（as_ec848a7673b74e35，delivered/requested）；此前 post **evt_cc8ac9f4108b490e**（to as_a341823c436e47ed，通知 evt_8ab824af7eac4d9a）。

**§P.103-H3 双档措辞（协调者 01:08 复核并采纳，本道接受）**
- **两档必须分写**：①**「v6 规则下 PENDING（四邻未齐）」**；②**「逻辑上已非候选（R 轴 neither）」**。二者可同时成立（v6 因缺邻居仍印 PENDING，但科学判定已出），此后报告一律并列表述，禁止用 PENDING 掩盖已成立的排除，也禁止用"已排除"掩盖四邻缺失。
- 现行档位：**(r3,c3)=scan#15 = 逻辑上已非候选**（row2 +54.5541 > 本点 +45.1404 > row4 +44.1975 ⇒ 沿 R(2,4) 单调穿行、非极值；v6 档位仍是 PENDING 因缺 r3c4）；**(r4,c2)=scan#9 = 格点级非候选**（R 轴 neither + 质子轴 MAX；**质子轴 MAX 本身不构成候选，候选必须 MAX+MIN 配对**）；**(r4,c3) 待 r5c3（scan#17）方可判 R 轴**；**(r2,c3) 必须等 r2c4**；boundary = #1–#7 / #12 / #13；**候选 = 0**。
- **同链现态（单次调用，2026-10-18T01:08:14）**：log **262,715 行 / 16,970,172 B / mtime 2026-10-18 01:08:05.772871246 / sha256 834202521d79a6ff36e606f65f433025997d24b7c8376878e3428ecdb72d4a26**、conv **16**、**L261846 Step 12/243 scan point 17/36**；协调者 01:08:05 = 262,700 行 / 4ad21284d6b1bd99e07132e0d7007b71ee1343df5c609f5bbf5bc8a19d81911c ⇒ 同链，仅增长（15 行差 = 缓冲）。
- snapshot 登记（不互签）：协调者台账 as of 01:08 = **736 行 / 96510934e609fa951a208b51f41563326dc24f818c7cd8bb1d4c3998efe7aa44**（其 01:08 勘误：该值为 ⑬ 条 ⓐ 补正写入**前**的快照、按 snapshot 引用式作废）⇒ **现行值 as of 2026-10-18T01:08:17 = 736 行 / 292,677 B / sha256 3bd728c213cfd364705be51c0cf03bef0c0704412f39fc2ebb712c89dced994a**。

**§P.103-H4 第三次同型错（行数/字节手写）与根因纠正（2026-10-18T01:08:46）**
- 事实链：我先发出「2,575 行 / 415,394 B / aa7e278e…」，而**同一次调用**的实测输出是 **2,573 行 / 415,131 B / sha256 aa7e278e41a6b4c30b859240b3ed2ef70ae629b6b6460da0bdf59252ee49c2ed**（2026-10-18T01:08:37 与 01:08:46 两次读数相同）⇒ **2,575 / 415,394 作废；正确三元组 = 2,573 行 / 415,131 B / aa7e278e…**。
- 这是本窗口**第三次**同型错：①2,533 配 5a1e2a2f…（配错版本）；②2,570 配 47af3197…（手算）；③2,575 / 415,394 配 aa7e278e…（手写回填）。三次都**不是测量错，而是"先在句子里写数字、再凭印象回填"**。
- **修法（硬性）**：任何含行数/字节/时刻的句子，必须先在同一段文字里**原样粘贴工具整行输出**（形如 `2573 STATUS.md`、`415131 B`、`<sha>  STATUS.md`、`mtime ...`），再从该粘贴文本里引用数字；**禁止在未粘贴的句子里出现任何行数/字节数**。此条同时适用于台账、帖子、call 与 PROCESS.md。
- 协调者 01:08:43 复核 = 2,573 行 / 415,131 B / aa7e278e…（与我两次实测逐位同），但其复述里仍带着我的错误值 2,575 ⇒ 已在 call 中单独澄清：**以 2,573 为准**。

---

## §P.104 2026-10-18T01:27 ｜ pt17 (r5,c3) 收敛；新增 (r4,c3) 逻辑非候选；col2 row4/row5 双反例句；col3 五点单调下降确认 pt14 峰形

**A. 快照（2026-10-18T01:27:06 单次调用七项）**：`E3/runs/e3b_scan2d_c2n4_o25h26.log` **291,518 行 / 18,833,795 B / mtime 2026-10-18 01:27:06.205081074 / sha256 eb55afd895e02ceb31df299db4e7eb4b195ec14c6f12700e48d5a319b2ce5086**、`Optimization completed` **17**、`Normal termination` **0**、末计数行 **L290849 "Step number 2 out of a maximum of 243 on scan point 18 out of 36"** ⇒ scan#18 = (r6,c3) 在跑（未收敛读数 L290761 = −939.247710662，约 +40.73，不用）。

**B. pt17 = (r5,c3) 收敛**：OPT **L289017** / hdr **L288385** / SCF **L288604 = −939.245779342**；实测 **R(2,4)=2.2248 / R(25,26)=1.4693**、R(4,26)=**3.3966**、R(10,27)=**0.9949**、R(2,25)=**1.2475**、R(2,26)=**2.3766**；**ΔE = +41.9473 vs 1028**。Kabsch **#16→#17 heavy20 0.0836 / max 0.1538 / 原子 2 / det +1.0 [OK]**（协调者 all-41 0.1249 / 0.4393 / 17）。

**C. col3 沿 R(2,4) 五点**：pt13 **+52.6635** → pt14 **+54.5541** → pt15 **+45.1404** → pt16 **+44.1975** → pt17 **+41.9473**（步差 **+1.8906 / −9.4137 / −0.9430 / −2.2502**）⇒ pt14 极大后**连续三点单调下降**，峰形增强。

**D. 本轮新增的确定判定**：
1. **(r4,c3) = scan#16 逻辑上已非候选**：现仅缺 r4c4 ⇒ R 轴可判 —— row3 **+45.1404**（高 0.9430）、row5 **+41.9473**（低 2.2502）⇒ 沿 R(2,4) 单调穿行、**既非极大亦非极小**（v6 仍印 PENDING 因缺 r4c4，按两档措辞并列）。
2. **(r5,c2)=scan#8 与 (r4,c2)=scan#9 四邻齐备后同判**：`R(2,4)axis:neither R(25,26)axis:max ⇒ not a candidate (no max/min pair across the two axes)` ⇒ **col2 的 row4 / row5 两格均已排除**；两格并列作为「**质子轴 MAX 本身不构成候选，候选必须 MAX+MIN 配对**」的正式反例句。

**E. 分档现状**：**逻辑上已非候选** = #8 / #9 / #10 / #11 / #15 / #16；**PENDING（四邻未齐）** = (r2,c3) 缺 r2c4、(r5,c3) 缺 r6c3（在跑）/ r5c4、(r6,c2) 缺 r6c3；**boundary = #1–#7 / #12 / #13**；**候选 = 0**。

**F. 口径不变**：约束剖面（R(10,27)=0.9949 冻结）；任一峰只作 TS 候选/上界、永不写 ΔE‡；真 TS 需 opt=(TS,calcfc,noeigen)+freq（恰 1 虚频，模矢含 C2–N4 断裂与 O25–H26 转移）+双向 IRC；跨度 **3.7179**；P 参照 ≥2.10（已验证项）；质子路径 **undetermined**（任何 ΔE‡ 前置）；E3b result/barrier **仍 null**；工具 v6（169 行 / 5dcc5d38…）、span_v2_after1078.py（117 行 / 095aeeb1…）。

**G. 已回**：call **evt_e59d2a65c688492f**（as_ec848a7673b74e35，delivered/requested），内容 = A–E + 反例句并列 + snapshot 登记。

**H. snapshot 登记（不互签）**：协调者台账 **738 行 / 295,060 B / 7ec4234cbc16b9da097a804227f664428392d491481d67ee4bc91e2e4403e610**。

**§P.104-H1 后果说明（协调者要求，正式句）+ 其 ⓑ 补记后的现行 snapshot（2026-10-18T01:28）**
- **后果说明（此后引用反例时照写）**：scan#8 (r5,c2) **+67.8597** 与 scan#9 (r4,c2) **+57.3371** 都是「R(2,4) 轴 neither + R(25,26) 轴 MAX」；**若把"质子轴 MAX"也算候选，就会误报 2 个假候选**（两格都在 col2，即质子把 H26 拉离 O25 后能量单调抬高的区域）⇒ 候选定义必须严格要求 **R(2,4)×R(25,26) 的 MAX + MIN 配对**、四邻收敛、支路一致，三者缺一不可。
- **协调者 ⓑ 补记已落盘，其台账现行 snapshot（不互签）**：as of 2026-10-18T01:27:42 = **738 行 / 295,806 B / sha256 27bc3e5ad92886f17d7ed164221263e2a822fd2762e43b774779514fb4aafdbe**；旧 **738 行 / 7ec4234c…** 降为补记前快照（上一条 H 项即该旧值）。
- **本道 PROCESS.md 01:27 条目已写**：编辑前 **738 行 / 295,806 B / 27bc3e5a…**，写入后 **sha256 fd21ecd28f0ac04e8ae686d52469079af6140101d621e30ec9c156eab8f9a4ac**

---

## §P.105 2026-10-18T02:49 ｜ log 静默 = 缓冲，不是挂死（事件类 4 预警已发）；轮询改为「log 里程碑 + .rwf mtime」双判据

**A. 触发**：01:28 挂的里程碑提醒（"scan point 19 out of"）到 02:28 超时未命中 ⇒ 取快照排查。

**B. 实测（2026-10-18T02:48:41 与 02:49:06 两次采样，均单次调用内多项）**
- log `E3/runs/e3b_scan2d_c2n4_o25h26.log`：**19,577,855 B / mtime 2026-10-18 02:28:07.721187122 +0800 / 303,154 行 / sha256 9044f74b2dd8678f69e07b8eeaadc903694070a18d8c644ec400ab8bf5b49cfe**；`Optimization completed` **17**、`Normal termination` **0**、`Error termination` **0**；末计数行 **L302333 "Step number 14 out of a maximum of 243 on scan point 18 out of 36"**。
- 进程：g16 **pid 1234203**（`/home/ly/g16/g16 .../e3b_scan2d_c2n4_o25h26.gjf`）+ 子进程 **l502.exe**（SCF link）。
- **scratch 实时写入**：`/home/ly/g16/scratch/Gau-1234209.rwf` **236,371,968 B**，mtime **02:48:40.605475953 → 02:49:06.045462766**（25 s 内推进）⇒ 作业在算。
- 平台（query_compute_job 1074）：state **running**、node-local、started 2026-10-17T20:28:54、attempt_count **0**、last_error 空。
- 机器：load **8.19 / 8.13 / 8.15**；`/` 984G 用 236G（**708G 可用**）。

**C. 判读（写入口径）**：Gaussian stdout 重定向下按块缓冲 ⇒ **log 静默 ≠ 崩溃**；「最后写入时间太老」这一判据**必须**与 **.rwf mtime** 或**进程存活**联合使用。里程碑未触发在本段属正常。

**D. 风险（只报告，不请求操作）**：平台 monitor 命令行含 `--timeout 1800`；若按 **log 静默时长** 计，自 02:28:07 起算约 **02:58:07** 可能自动终止；若按进程/计算活动计则无风险。**只能由平台/主协调核对 monitor 语义；正确处置是核对，不是杀作业重投**（重投丢进度且违反零提交纪律）。本道零提交 / 零 kill / 不改 priority。

**E. 已发**：post **evt_6203b671e6564daf**（to as_a341823c436e47ed，事件类 4 预警）；call as_ec848a7673b74e35（同内容精简版）。

**F. 轮询改法**：此后里程碑用 **「log 里程碑（scan point NN out of） + .rwf mtime 推进」双判据**、超时放宽到 2 h；log 一旦追上立即取快照 + v6 出表 + 登记。

---

## §P.106 2026-10-18T03:47 ｜ job 1074 **cancelled**（平台/主协调按"路线 A 取代 HI1_E5"撤回）：按预写死预案结案 —— 17/36、col3 缺末行、候选 0、E3b result/barrier 恒 null

**A. 平台终态（query_compute_job 1074 逐字）**：state **cancelled**、scheduler_state **CANCELLED**、started_at 2026-10-17T20:28:54+08:00、ended_at **2026-10-18T03:47:00+08:00**、attempt_count 0、last_error 逐字：
`D23/D29 cancel: HI1_E5 superseded by route A; remaining 19 grid pts need 7.7h; free memory for IRC 1099`
⇒ **这是方向性调度决定（HI1_E5 被"路线 A"取代、余 19 格点需 7.7 h、并为 IRC 腾出内存），不是计算失败、不是崩溃、不是"该窗口无驻点"的证据。**

**B. 日志终态（原始输出，逐项单独命令，2026-10-18T03:47:05）**
- `wc -l` = **303,154**；`stat` = **19,577,855 B / mtime 2026-10-18 02:28:07.721187122 +0800**；`sha256sum` = **9044f74b2dd8678f69e07b8eeaadc903694070a18d8c644ec400ab8bf5b49cfe**
- `grep -c 'Optimization completed'` = **17**；`grep -c 'Normal termination'` = **0**（exit 1）；`grep -c 'Error termination'` = **0**（exit 1）
- 末三条计数行：**L300410 Step 12/243·scan point 18/36**、**L301372 Step 13/243·scan point 18/36**、**L302333 Step 14/243·scan point 18/36**
- 说明：log 自 **02:28:07** 起一直是块缓冲未刷新，**cancelled 时缓冲尾部未落盘** ⇒ 日志与 .rwf 的差异是缓冲现象，不是数据丢失证据；**未收敛帧一律不当数据**。

**C. v6 出表（169 行 / sha256 5dcc5d38d5de8d7525a4c4dee18f8d66442fa9aea940461f22ed2dd66297ea4b，运行时自印一致）**
- `log lines 303154 | converged grid points 17 | maxstep-exhausted points 0`
- `candidates found in this grid state: 0`
- col3 已收敛五行（实测坐标与能量）：pt13 (1.4248,1.4693) −939.228701942 / pt14 (1.6248,1.4693) −939.225689108 / pt15 (1.8248,1.4693) −939.240690723 / pt16 (2.0248,1.4693) −939.242193436 / pt17 (2.2248,1.4693) −939.245779342 ⇒ ΔE +52.6635 / **+54.5541** / +45.1404 / +44.1975 / +41.9473 kcal/mol（vs 1028 = −939.312626605）

**D. 结案措辞（按 §P.105/协调者预写死预案，逐字）**
- **「scan#18 = (r6,c3) 未收敛 ⇒ col3 缺末行；6×6 网格已收敛 17/36；候选 0；E3b result/barrier 维持 null」**
- **不写**「该窗口无驻点」；**不**把 (r5,c3) 的 R 轴强判单调（其下邻缺失）；**不**把未收敛帧当数据；**不**写任何 ΔE‡。
- **格点级已定判定不受影响**：**#8 / #9** = `R(2,4)axis:neither R(25,26)axis:max ⇒ not a candidate`（质子轴 MAX 本身不构成候选，若误当候选将多出 2 个假候选：+67.8597 / +57.3371）；**#10 / #11** = 两轴 neither；**#15 / #16** = R 轴单调穿行（各自上下邻居已收敛）；boundary = #1–#7 / #12 / #13（needs-wider-window）。
- **(r2,c3)=pt14 的 R(2,4) 局部 MAX 仍只是"未决峰"**：质子轴侧 (r2,c4) 未算 ⇒ 无法区分「一轴 MAX + 一轴 MIN」与「两轴 MAX 山脊」；且 #13→#14（heavy20 0.3713）与 #14→#15（0.6968；all-41 0.9631）两次大 Kabsch 跳变夹住 pt14、其后 #15→#16 0.0987 与 #16→#17 0.0836 平滑 ⇒ **"构象/质子状态交叉"解释仍未被排除，支路核查是判候选的前置**。**因此 pt14 不称候选、不称 TS、无 ΔE‡。**

**E. 口径（不变）**：E3b result/barrier **null**；已验证极小点跨度 **3.7179 kcal/mol**（P −4.3383 / 1073 −2.7297 / 1071+1078 −6.4476，三者均 0 虚频）；P 参照不确定度 **≥2.10**（已验证项，floor 2.1093，P 已非该物种最低已知驻点）；**质子路径（H26 直接转移 vs H27 经 O10 中继双穿梭）undetermined，是任何 ΔE‡ 的前置**；约束剖面 R(10,27)=0.9949（O10–H27 冻结）；任何峰只作 TS 候选/上界。

**F. 后续（零提交，等主协调单独授权）**：余 19 个格点（含决定性格点 **(r2,c4)** ≈ pt23）**不再由本 lane 续跑**；若日后需要，只能由主协调明确口令另起作业（新文件、不覆盖本 native log）。本 lane 不 kill、不重投、不改 priority、不 ts_resume、不碰 ts_0015/ts_0016。

**G. 本文件读数（写入前，单次调用三项）**：`wc -l` = 2,631、`stat` = 423,467 B、`sha256sum` = e440a4dc64dc76acd19986bd24090cde28f3fa38ab7ca366fd42d673b3ac96af。

**G. 口径与边界不变**：E3b result/barrier **null**；跨度 3.7179；P 参照 ≥2.10（已验证项）；质子路径 undetermined（ΔE‡ 前置）；候选 **0**；col3 沿 R(2,4) = +52.6635 → **+54.5541（pt14 极大）** → +45.1404 → +44.1975 → +41.9473；(r2,c3) 待 (r2,c4) + 支路核查；零提交 / 零 kill / 不 ts_resume / 不碰 ts_0015、ts_0016；交付面 277 行 / a2964d8d… 未动。（行数/字节见 PROCESS.md 下次实测，不在句内手写）。

---

## §P.106-H1 2026-10-18T03:50 ｜ 合并式监视（case a/b）以 **case (b)** 触发：实测确认「无 scan#19 行、日志终态冻结」，与 §P.106 结案口径一致，无需改判

**A. 触发**：02:59:13 挂的合并式监视在 **case (b)**（monitor pid 1234148 消失 ⇒ 1074 已离开 running）命中；case (a)（"scan point 19 out of"）**从未命中**。

**B. 实测（2026-10-18T03:50:08 与 03:50:30 两次采样，逐项单独命令）**
- `grep -c 'scan point'` = **317**；`grep -o 'scan point *[0-9]* out of' … | tail -2` = **`scan point    18 out of` / `scan point    18 out of`** ⇒ **日志内不存在 scan#19 行**，缓冲尾部从未把下一格点落下。
- `grep -c 'Optimization completed'` = **17**；`grep -c 'Normal termination'` = **0**（exit 1）；`grep -c 'Error termination'` = **0**（exit 1）。
- `pgrep -af '1234148|1234203'` 仅匹配到 pgrep 自身的 /bin/sh ⇒ **monitor 与 g16 两个 pid 均已不存在**。
- 终态冻结：`sha256sum` = **9044f74b2dd8678f69e07b8eeaadc903694070a18d8c644ec400ab8bf5b49cfe**、`stat` = **19,577,855 B / mtime 2026-10-18 02:28:07.721187122 +0800** —— 与 §P.106-B **逐字节相同**，说明作业结束后日志不再增长，缓冲尾部未再落盘。

**C. 判读**：本条不产生任何新科学结论，只把 §P.106-D 的结案措辞从"据平台终态推断"升级为"据日志内容实测"：**「scan#18 = (r6,c3) 未收敛 ⇒ col3 缺末行；6×6 网格已收敛 17/36；候选 0；E3b result/barrier 维持 null」**。仍**不写**"该窗口无驻点"，仍**不**强判 (r5,c3) 的 R 轴单调，仍未收敛帧一律不当数据。

**D. 事件类 1 已发**：post **evt_ced0837640af4c75**（topic 'gold-finish-20261015'，首行 `to: as_a341823c436e47ed`）+ call **as_ec848a7673b74e35**（精简版，同口径）。measurement time 2026-10-18T03:49:48+08:00 / 03:49:50+08:00。

**E. 监视处置**：1074 已终态 ⇒ **不再为 1074 续挂任何轮询**（里程碑与进程两个判据都已失效）；本 lane 该路径的后续只等两类外部事件：主协调的**质子路径裁定**，或**补算余下 19 格点（含决定性格点 (r2,c4) ≈ pt23）的新授权**。二者均走信箱通知，不需要主动轮询。

**F. 本文件读数（§P.106 写入后，单次调用三项）**：`wc -l` = **2,662**、`stat` = **427,852 B / mtime 2026-10-18 03:47:49.240165718 +0800**、`sha256sum` = **3fdf8d6e08f8fa988149fabea56317d7b5975641a01e523e965533d90c7a7078**；共享记录 HI1/PROCESS.md 同批实测 **798 行 / 342,059 B / mtime 2026-10-18 03:48:13.643632213 +0800 / sha256 a65be0e5193d8ef936bd22420374fe2799d3a64551630d2eaa9d87c905721468**。

**G. 边界**：只读；零提交 / 零 kill / 不改 priority / 不 ts_resume / 不碰 ts_0015、ts_0016；交付面 a2964d8d… / 277 行不重出；四条边 result = barrier = null。

---

## §P.106-H2 2026-10-18T03:52 ｜ **定性更正（接受协调者）**：1074 是「计算侧异常终止（Gaussian software termination，l703.exe）→ 随后平台以 cancelled 记账并附第三方理由」，不是「调度侧主动取消、不是计算失败」

**A. 触发**：协调者 call（as_ec848a7673b74e35，03:50–03:51）指出本道 §P.106 四档判定第 1 条与 post evt_ced0837640af4c75 的「调度侧主动取消、不是计算失败」不成立，并给出一手包装日志。

**B. 我独立复测（2026-10-18T03:51:38 与 03:52:02，逐项单独命令，未采用协调者数值）**
- 路径：`gold_finish_20261015/HI1/E3/runs/.cloudra/calc-1074.out.log`；`wc -lc` = **32 行 / 1,581 B**；`stat` = **1,581 B / mtime 2026-10-18 03:45:46.453373043 +0800**；`sha256sum` = **f9e73b64815b76fdf38c497793a21cf49b47f2feef7d7aa78cc5b85911a79d6d**（与协调者 1,581 B / 03:45:46.453373043 逐位一致 ⇒ 同一文件、双签）。
- `grep -c 'software termination'` = **2**；`grep -n 'Error: software termination'` = **L2** 与 **L11**（逐字 `Error: software termination`）。
- L1 逐字：`[calculator] isolated GAUSS_SCRDIR=/home/ly/g16/scratch/cloudra_g16_task1074_1234148`。
- 栈帧（`cat -n` 逐行）：首段 libc(+0x45330) + **l703.exe [0xdca494]**（L9–L10）；次段 **l703.exe [0xd1f5a2] / [0xcde1ff] / [0x8a19bc] / [0x6e367d] / [0x5a28e8] / [0x4898cb] / [0x5d8ba3] / [0x4caeb3] / [0x4158f8] / [0x4138db] / [0x41071b] / [0x410624]** + libc(__libc_start_main+0x8b) + **l703.exe [0x40ad69]**（L18–L32）。

**C. 独立时间锚（本道新增，支持同一结论）**
- `stat /home/ly/g16/scratch/Gau-1234209.rwf` = **236,371,968 B / mtime 2026-10-18 03:45:35.805260811 +0800** ⇒ 该 .rwf **在 03:45:35 停止推进**，**11 s 后**包装日志记录崩溃（03:45:46.453373043）。两条独立通道指向同一时刻，故**崩溃时刻 ≈ 03:45:35–03:45:46**。
- 附带澄清：包装日志声明的隔离 `GAUSS_SCRDIR=/home/ly/g16/scratch/cloudra_g16_task1074_1234148` **现已不存在**（`ls -ld` 返回 No such file or directory）；1074 实际唯一残留 .rwf 为上述 `Gau-1234209.rwf`，其末次 mtime 停在崩溃时刻 ⇒ **§P.105 的「判活用 .rwf mtime 推进」证据仍然成立**（当时推进的正是 1074 自己的 .rwf，不是他作业），无需撤回。

**D. 更正（接受协调者口径，取代本道旧表述）**
- **作废**：§P.106 四档判定第 1 条「无 Error termination、进程正常消失 ⇒ 不是计算崩溃」；以及 post evt_ced0837640af4c75 第二节/第三节的「调度侧主动取消，不是计算失败」。
- **新口径（逐字）**：**「1074 属计算侧异常终止（Gaussian software termination，l703.exe，包装日志 `runs/.cloudra/calc-1074.out.log` L2/L11 + backtrace），随后平台以 state=cancelled 记账并附第三方理由串；该理由串是事后记账与事后归因，不是终止原因。」**
- **仍然成立的部分**：①cancelled 报文里的「route A 取代 HI1_E5 / 余 19 格点需 7.7 h / 为 IRC 1099 腾内存」属**第三方元数据断言**，**不能**当作「该窗口无驻点」的证据，也**不能**当作「作业是被调度主动撤下」的证据；②崩溃原因（l703 内部，可能含内存压力）**未被本道查明**，只登记现象，不猜原因。
- **与 1080 的对称性**：1080 为 l502 backtrace、包装日志 03:34:45.173349804 → cancel 03:35:58；1074 为 l703、03:45:46.453373043 → cancel 03:47:00；两次「撞击 → cancel 记账」间隔 72.8 s / 73.5 s 近乎相同（协调者测）⇒ 元数据 cancel 是统一的事后路径，按同一口径处理。

**E. 结案结论不变（措辞逐字保留）**：**「scan#18 = (r6,c3) 未收敛 ⇒ col3 缺末行；6×6 网格已收敛 17/36；候选 0；E3b result/barrier 维持 null」**；不写「该窗口无驻点」、不强判 (r5,c3) 的 R 轴单调、未收敛帧不当数据、无任何 ΔE‡。补一条：log 末计数行 **L302333 = Step 14/243·scan point 18/36** 只代表**最后一次 flush（02:28:07）时**的进度；此后约 77 分钟的步进丢失于块缓冲 ⇒ **不得**用它断言崩溃瞬间的步数。

**F. 纪律新增（立即生效）**：终止判定必须**三源并用** —— (i) g16 原生 stdout（可能长期缓冲、终态时甚至未落盘）、(ii) 包装日志 `runs/.cloudra/calc-<id>.out.log`（`Error: software termination` + 寄存器 + backtrace）、(iii) 进程退出与 .rwf **停止推进**时刻。**只查 (i) 会得出「无崩溃」的假结论**（本条即实例：(i) 显示 Normal 0 / Error 0，(ii) 显示两次 software termination）。

**G. 台账分工**：共享台账 HI1/PROCESS.md 的本条更正**由协调者追加**（其 call 第六/四节自报 807 行 / sha256 81f7497bc29f46546fa45e4d6dcdcae4fc4ac57c592131f88d00cb1cb0abbfe5 / 345,461 B / mtime 2026-10-18 03:51:03.864905756，按其自报登记、本道不复算）；本道只在**本文件**追加本条，**不重复写 PROCESS.md**，避免双写冲突。

**H. 边界（不变）**：零提交 / 零 kill / 零 priority / 不 ts_resume / 不碰 ts_0015、ts_0016、ts_0019、ts_0020；交付面 FINAL_DELIVERY_DRAFT.md a2964d8d… / 277 行未动；四条边 result = barrier = null；跨度 3.7179；P 参照 ≥2.10（已验证项）；质子路径 undetermined（ΔE‡ 前置）；余 19 格点（含 (r2,c4)）不由本 lane 续跑。

---

## §P.106-H3 2026-10-18T03:56 ｜ **二次更正（接受协调者自纠）**：1074 = 外部 **SIGTERM** 终止（guard 退出码 **241 ≡ −15**），`Error: software termination` + backtrace 是 Gaussian 对 SIGTERM 的标准反应，**不是内部崩溃** ⇒ 恢复 §P.106 原表述，撤回 §P.106-H2 的「计算侧异常终止（崩溃）」定性

**A. 触发**：协调者 as_ec848a7673b74e35 03:55 自纠（覆盖其 03:52/03:53 的「崩溃」定性），并指出 exit 241 / −15 = SIGTERM。

**B. 我独立复测（2026-10-18T03:55:38–03:56:03，逐项单独命令，未抄他人数值）**
- `E3/runs/.cloudra/guard-1074.log`：`wc -lc` = **3 行 / 181 B**；`stat` = **181 B / mtime 2026-10-18 03:47:00.785418768 +0800**；`sha256sum` = **7172971b6efa0f3ad141aea03d136ee5a20e2789d2f88b3faebd6d63b542b8a4**；逐行：L1 `[guard] Gaussian scratch: /home/ly/g16/scratch/cloudra_g16_task1074_1234148`、L2 `[guard] calculator 启动 (PID 1234195)，等待其结束...`、L3 **`[guard] calculator 退出，退出码：241`**。
- 正常完成对照（同目录 `guard-1073.log`，238 B）：L3 `[guard] calculator 退出，退出码：0`、L4 `[guard] 数据库状态已更新: task_id=1073, state=done` ⇒ **正常路径 = 退出码 0 + 数据库状态行**；1074 两者皆无（只有 3 行、241、无状态行）⇒ 属被信号终止路径。
- 241 ≡ −15 的独立互证（我实读）：`HI1/E1/split/.cloudra/calc-1080.exit.json` = `{"exit_code": -15}`（22 B，sha256 **66ff978a5d76964f5283c5edea2730cf6fa61300678deb69873b1eefcb4b6c8a**）而 `guard-1080.log` L3 同为 **241** ⇒ **241（0xF1）与 −15 同一退出状态按 8 位补码表示的两种写法**，映射由这一对独立文件确认。
- **供缺说明**：`find HI1/E3 -name '*.exit.json'` 返回空 ⇒ **1074 自己没有 exit.json**；故 1074 的「−15 = SIGTERM」由「241 与 1080/1087 的 241 完全同值 + 该对文件已确立的 241≡−15 映射」推得，**不是**直接读到 1074 的 −15。这一点如实标注，不冒充直接证据。

**C. 时间链条（全部为实测，按事件顺序重排）**
1) `Gau-1234209.rwf` 停写 **03:45:35.805260811**（236,371,968 B）；
2) 包装日志 `calc-1074.out.log` 记录两次 `Error: software termination` + l703 栈帧：**03:45:46.453373043**（32 行 / 1,581 B / sha256 f9e73b64…）⇒ **收到 SIGTERM 后 Gaussian 打消息并退出**，故 **SIGTERM ≈ 03:45:46**；
3) guard 记录退出码 241：**03:47:00.785418768**；
4) 平台 `ended_at` **03:47:00**、state=cancelled。
⇒ 此前被解读为「撞击 → 73.5 s 后 cancel 记账」的间隔，现更正为 **「SIGTERM(≈03:45:46) → guard/平台终结记账(≈03:47:00) 的约 74 s 收尾延迟」**；1080 的 72.8 s 同理。

**D. 定性（最终，取代 §P.106-H2 与公共帖 evt_d1e38696799b4c76）**
- **1074 = 外部 SIGTERM 终止（guard 退出码 241 ≡ −15），随后平台记为 state=cancelled 并附第三方理由串。** `Error: software termination` + 寄存器转储 + l703/l502 backtrace 是 **Gaussian 对 SIGTERM 的标准反应**，**不构成内部崩溃证据**。
- **恢复** §P.106 原表述「调度侧主动取消、不是计算失败」（这一层在「非计算失败」上成立）；**撤回** §P.106-H2 的「计算侧异常终止（Gaussian 内部崩溃）」定性，以及其 D 段「作废原表述」的处置。
- **不主张**：谁发的 SIGTERM、为何发 —— 我持有的文件只能证明「进程被 SIGTERM 终止」，平台理由串（`route A 取代 HI1_E5 / 余 19 格点需 7.7 h / 为 IRC 1099 腾内存`）仍是第三方断言；`1099` 于 03:52:50 起跑、1082/1087/1074 三次理由串都指向为 1099 腾资源，**与**「平台主动 SIGTERM」一致，但因果主体不由本道从这些文件断言。

**E. 判死纪律（二次更正，取代 §P.106-H2-F 的三源表述）**
终止判定按**证据强度**分层：①**guard-<id>.log 退出码**（0 = 正常，**241 ≡ −15 = SIGTERM**）**及其是否带「数据库状态已更新」行**；②**calc-<id>.exit.json 的 exit_code**（若存在）；③ **.rwf 停写时刻**；④ 平台终态记录；⑤ **stdout / 包装日志的终止消息只作辅证**（`software termination` 对 SIGTERM 与内部崩溃都会出现，不能单凭它区分两者 —— 这正是本条与前条的教训）。判活四级制不变（.rwf 十秒级刷新 + 进程存活）。

**F. 数据面与结案措辞（不变，逐字）**
**「scan#18 = (r6,c3) 未收敛 ⇒ col3 缺末行；6×6 网格已收敛 17/36；候选 0；E3b result/barrier 维持 null」**；终稿措辞「6×6 网格（已算 17 个收敛点）未分辨出离散指标 1 的驻点，需扩窗或加密」+ 缺口「(r2,c4) ≈ pt23 从未采样」；不写「无 TS / 通道不存在 / 该窗口无驻点」；不强判 (r5,c3) 的 R 轴单调；未收敛帧不当数据；无任何 ΔE‡；log 末计数行 L302333 只代表最后一次 flush（02:28:07）状态。

**G. 本文件读数（§P.106-H2 写入后，单次调用三项）**：`wc -l` = **2,712**、`stat` = **436,038 B / mtime 2026-10-18 03:52:19.838276036 +0800**、`sha256sum` = **6bb2c7126ae4c558dfa4fc595a070e1dbbe835fe8eef3bef45f5a4370b120a2c**。

**H. 边界（不变）**：零提交 / 零 kill / 零 priority / 不 ts_resume / 不碰 ts_0015、ts_0016、ts_0019、ts_0020；交付面 FINAL_DELIVERY_DRAFT.md a2964d8d… / 277 行未动；四条边 result = barrier = null；跨度 3.7179；P 参照 ≥2.10（已验证项）；质子路径 undetermined（ΔE‡ 前置）；余 19 格点（含 (r2,c4)）不由本 lane 续跑。

---

## §P.107 2026-10-18T05:03 ｜ (r2,c4)≈pt23 单点：输入已按规格生成并逐项核验，但 **submit_compute_job 被环境拒绝（PATH 缺 g16）**，作业未起跑

**A. 授权**：主协调 as_a341823c436e47ed 04:59 / 05:00 / 05:01 / 05:02 四通 call 放行**仅 (r2,c4) 单点一个**（新文件名、8 cpus / 10,240 MB / priority 0、方法与 1074 逐字一致、坐标由工具生成、候选只报不 ts_prepare），并追加三条有效性闸门（几何 / 约束 / 失败闸门）。E2 cont2、支 B 2.9543 单点、加密网格、E1a 二维网格、任何 ts_prepare 均**未授权**。

**B. 种子帧（先验帧来源 → 再取坐标）**
- 陷阱：L183158 的 Input orientation 是**下一点（scan#15 起始几何）**（其 R(2,4)=**1.8248**），不是 pt14 收敛帧。
- 正确：**L182020** 的 Input orientation 表；对应 SCF **L182507 = −939.225689108**。
- 六距离：R(2,4)=**1.6248**、R(25,26)=**1.4693**、R(10,27)=**0.9949**、R(2,25)=**1.3793**、R(2,26)=**2.1690**、R(4,26)=**2.3243**（与协调者六值逐位相同）。
- 文件：`runs/pt14_r2c3_seed.xyz` = 43 行 / 2,102 B / mtime 2026-10-18 05:00:26.880909820 +0800 / sha256 **aa071e1ef34efc481f0923ebc477822b29874229a35b305bf6fc7390b13bd289**。

**C. 投递目标坐标 (r2,c4)**
- R(2,4)=**1.6248（与 pt14 同）**、R(25,26)=**1.7193**、R(10,27)=**0.9949**；其余 **40 原子原封不动**，仅 H26 沿 O25→H26 单位向量 **(0.98525185, 0.14877592, 0.08452528)** 平移 **0.249976 Å**。
- 目标帧六距离：R(2,4)=1.6248、R(25,26)=1.7193、R(10,27)=0.9949、R(2,25)=1.3793、R(2,26)=**2.3688**、R(4,26)=**2.3992**。
- 文件：`runs/pt23_r2c4_target.xyz` = 43 行 / 2,101 B / mtime 2026-10-18 05:00:52.221331406 +0800 / sha256 **eee58df3469b1b6951e59f9d1207bfc0accdeac87695ca7a724a2d89ed878fb2**。

**D. 几何事实（必须随报告给出，且触发主协调的几何闸门）**
- 种子帧：**H17···H26 = 1.0254 Å**、C5–H17 = **1.2558 Å**（internal_coordinates 判为 "crowded H...H contact: not a bond-forming candidate"；C5–H17 判 "elongated"）。
- 目标帧：**H17···H26 = 0.8318 Å**（H26 最近重原子 O25 1.7193 / C5 1.8763 / C2 2.3688）⇒ **起始几何即违反非键 ≥1.20 Å 门槛**；这是该格点刚性台阶的固有结果（Gaussian modredundant 对末端原子同为沿键轴平移），**不是构造错误**，且约束只冻结 B 2 4 / B 25 26 / B 10 27，H17 与 C5–H17 自由。
- 主协调 05:02 判定：**不阻止提交**，但收敛后若 H17···H26 仍 < 1.20 Å ⇒ 该点标「几何受损」、**不得单独用于二维鞍点判定**。

**E. 输入三件套（`runs/e3b_r2c4_pt23_20261018.gjf`）**
- **54 行 / 2,442 B / mtime 2026-10-18 05:00:58.483584085 +0800 / sha256 bb9e30a92b52285e69499462bf75282cbd045d1f5e076d24bf25f175f4807331**
- route 逐字：`#p opt=(modredundant,maxstep=8) B3LYP/def2SVP empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=dmso)`（与 1074 **零差异**）；`%nproc=8`、`%mem=10240MB`；chk 指 `runs/e3b_r2c4_pt23_20261018.chk`。
- 尾部（`cat -A` 实见）：空行 / `B 2 4 F` / `B 25 26 F` / `B 10 27 F` / 空行；qm_input_writer 报 `unapplied_options = []`、constraints = B2-4 / B25-26 / B10-27、tasks = minimum_opt。
- 与目标帧逐原子对照 **max |Δ| = 0.000000 Å**，元素顺序一致（`prep/verify_r2c4_input.py`）。

**F. 工具缺口（照例登记）**：`internal_coordinates` `mode=transform` 的 `{"type":"stretch","atoms":[25,26],"new_length":1.7193}` 被拒，理由逐字 *"Invalid transform operation: stretch: atoms 25 and 26 are not bonded"*（O25–H26 = 1.4693 未被识别为成键）；改用 `prep/build_r2c4_target.py` 做一次性刚体平移（脚本 sha256 见 §P.107-H1），随后用 `internal_coordinates mode=analyze` 复核六距离与异常判读。

**G. **提交被拒（作业未起跑）**：`submit_compute_job`（input_file = 上述 .gjf、job_type=gaussian、is_async=true、cpus=8、memory_mb=10240、priority=0）连续两次返回 `is_success=false`、`job_id=-1`，message 逐字：
`PATH is missing the programs required for gaussian compute; install and ensure one of these commands is available: g16, g09, g26`
环境实测（同日 05:02:07 / 05:02:34）：`which g16` = **not on PATH**；`PATH` 中无 `/home/ly/bin`；`/home/ly/g16/g16` 存在（`-rwx------` 127,313,512 B）；**`/home/ly/bin/g16` 存在**（209 B 包装脚本，内 `export g16root=/home/ly; GAUSS_SCRDIR=/home/ly/g16/scratch`，末尾 `exec /home/ly/g16/g16 "$@"`）；`/usr/local/bin/g16`、`/usr/bin/g16`、`/opt/g16/g16` 均不存在。同刻另有一路 `/home/ly/g16/g16 E1_scan_manual.gjf`（pid 2045389，非本 lane）在跑 ⇒ 执行侧能看到 g16，而**提交侧 PATH 看不到**。

**H. 本 lane 的处置（不越界）**：**未**用 bash 直接起 g16（手工引擎执行属禁止的旁路）、**未**改 PATH / 未建 symlink（系统改动需授权）、**未**重试第三次、**未**换种子或改规格。输入文件与三件套保持原样待提交。

**I. 解除阻塞的两个候选（均需主协调口令）**
1) 由**具备 g16 on PATH 的会话**提交**同一文件**（sha256 bb9e30a9…，8 cpus / 10,240 MB / priority 0），我按同一闸门出报告；
2) 授权在 `/usr/local/bin` 建 `g16 -> /home/ly/bin/g16` 软链（或等价地把 `/home/ly/bin` 加入提交侧 PATH），随后我按原规格自行提交。

**J. 判读预案（不变，按主协调口令顺序）**：①r1c4 / r3c4 = **未采样**；②(r2,c4) 四邻仅 r2c3 已算、r2c5 未算 ⇒ **PENDING（四邻不齐）**，不写任何极值结论；③两轴邻居能量差 + 能垒承载维；④#14→#15 支路/构象核查（heavy20 0.6968 / max 1.4476 / a6；all-41 0.9631 / 2.5343 / a17）为候选判定前置；⑤候选只报主协调、**不 ts_prepare**；⑥E3b result = barrier = **null** 不变；不写「无 TS / 通道不存在 / 该窗口无驻点」。

**K. 取证纪律**：引用 1074 的 `runs/e3b_scan2d_c2n4_o25h26.log` 与 `.cloudra/guard-1074.log` 只写 **sha256 + 字节数**（两者 2026-10-18 04:53:47 被同内容重写：log mtime 04:53:47.743635472 / guard mtime 04:53:47.613998195，sha 与字节不变）；时间只写历史 mtime 或平台 `ended_at` 03:47:00 / `.rwf` 停写 03:45:35.805260811。

**§P.107-H1 脚本三件套（实测，2026-10-18T05:02:55）**
- `prep/extract_frame_r2c4.py` = 54 行 / sha256 **93fae267930d57fd6e4937df3191920408bc2d99d03b1dcc51c044a6c3e6f4ae**（按行号取 Input orientation 表，输出六距离与 xyz）
- `prep/build_r2c4_target.py` = 65 行 / sha256 **bab8e3c16af5d934287786c8943f622404a0cfa9bc094bcbfeb8200a74fe00c2**（仅平移 H26，打印 before/after 与最近重原子）
- `prep/verify_r2c4_input.py` = sha256 **8381b93292b590c50fa56bdbe23d3207a2b32f528229be1b0ab123f01ddc06e1**（.gjf 与目标帧 max|Δ|、六距离、尾部 B 行位置、<1.20 Å 接触清单）




































