# HI1_E3 证据清单（small_mol 道）

工作根目录：`/home/ly/Cloudra-mechanism-agent`
本道产出目录：`/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/`

本文件按 PLAN §4 第 5 项登记：原生产物绝对路径 + sha256 + 原始行能量 + 方法一句。**未产生的项写“缺”，不填 0。**

---

## 1 A 段（只读复核）证据

### 1.1 本地确实存在的可复用几何（只作起点/身份参考，非本道能量证据）

| 绝对路径 | sha256 | 原子/内容 | 方法/引擎 | 原始行能量 |
|---|---|---|---|---|
| `/home/ly/Cloudra-mechanism-agent/gold_compute/grant_materials_20261001/raw/HI1/job_51/rc_clean_np8.xyz` | `5b7b7aa2df9466c456614c9af3ddfe4e264339fd1b39a2dadd58690fb5f9b594` | 41 原子；烯胺+水+苯甲醛（= HI1_I1 物种），非 I2 | ORCA 6.1.1 B3LYP-D3BJ/def2-SVP RIJCOSX CPCM(DMSO)（几何文件本地，日志不在本地） | 本地无原始行；文档记录 E=−938.760019066499 Ha（**不可作本道能量**） |
| `.../raw/HI1/job_52/rc_shared_opt.xyz` | `460aa78fde5def3d42741f0c6ad6b6b47ec5c7e29edeeb4ce1bae87931ba5f8d` | 41 原子；烯胺+水+苯甲醛另一构象 | 同上 | 本地无原始行（文档 +2.495 kcal vs job51，仅参考） |
| `.../raw/HI1/job_54/minor_rc_opt.xyz` | `1bed5958e8826676044a1b83d256542b5ad93641f02e120d0b7791e1864ebdb8` | 41 原子；副面预复合物 | 同上 | 本地无原始行（文档 +2.254 kcal vs job51，仅参考） |
| `.../raw/HI1/job_64/ts2_np8.xyz` | `26b53f25a511c050fe71d6fb566fb74b995de9465655f159ec0e90ece3b1031b` | 41 原子；C–C 加成 TS 近似几何 | 同上 | 本地无原始行（仅几何参考） |

### 1.2 本地确认缺失、因而**无法复核**的历史产物（缺项，非 0）

| 目标 | 期望路径（记录） | 本地核验 |
|---|---|---|
| job82 I2 原几何 em1_epF_optfreq.xyz | `…/HI1_E3/input/I2_start.xyz`（原 sha `a618fd1dcebb32b536c7fbb63a18e2fa8ccebb9538dd437bf9dd8c63583af10f`） | 不存在（find 全库零命中） |
| job71/72/83 端点 | 远端 `HI1_gold_20260929/paratera_20260930/minor_spec/em1_endpoints/` | 不存在 |
| E3 验收链 114/115/116/117/118/119/120 | 远端 `HI1_E3/ts/ts_0001/jobs/declaration_0004/{ts_opt,frequency,irc,reactant_opt,reactant_frequency,product_opt,product_frequency}` | 不存在（无任何 calc-114..120 日志） |
| E1 链 94/100/102 | 远端 `HI1_E1/…` | 不存在（属 E1 道） |
| 历史备份目录 / tar 快照 | `gold_compute/remote_backups/`、任何 `*.tar.gz` | 不存在 |

---

## 2 B 段（I2 重建）证据

待填：I2 无约束 Opt+Freq 日志绝对路径 + sha256 + 原始行能量（SCF Done / 频率行）。

## 3 C 段（E3 TS）证据

待填：ts_prepare/ts_resume run 目录、TS 频率日志、IRC 双向轨迹与两端 Opt/Freq 日志绝对路径 + sha256 + 原始行能量。

---

## 4 方法一句（适用于本道全部新计算）

Gaussian 16 (`/home/ly/g16/g16`)，B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight + SCRF=(CPCM,Solvent=DMSO)，q0/m1；TS/IRC 走 ts_prepare/ts_resume（引擎 gaussian）。历史 ORCA 能量只作参考，绝不与本道 Gaussian 数值相减。

---

## 1.3 A 段追加：本地"有索引、无实体"（job082/071/072/083）

| 路径 | 状态 | 说明 |
|---|---|---|
| `gold_compute/organized_data/hard_20261001/02_calculations/HI1/jobs/job082/ledger.json` | 存在（884 B） | ORCA / done / paratera-cpu / 8 cpu / 13000 MB / `…/minor_spec/em1_endpoints/em1_epF_optfreq.inp` |
| `…/jobs/job082/input.inp`、`run_directory` | **悬空软链接** | 指向 `remote_backups/paratera_final_20261001_0830/final_archive_20261001_1522/…`，该目录本地不存在 |
| `…/jobs/job071`、`job072`、`job083` | 同上 | 只有 ledger.json + 悬空软链接 |
| 旧 sha `a618fd1d…8310f` 的实体 | **不存在** | 仅出现在 `…/catalog.sqlite3`、`08_integrity/raw_inventory.json|csv` 索引行与 HANDOFF 文本 |

通道命名冲突（不可复核项）：job082 的 ledger 路径目录名为 `minor_spec/em1_endpoints`（副面通道），而 hard_hi1_2026-10-01.md 把 job82 记为 E2（major）/C8R-C29S —— 原文件缺失，连"历史 I2 是主面 (S)-aldol 还是副面 (R)-aldol"都无法本地复核。

---

## 2 B 段（I2 重建）证据（进行中）

### 2.1 起点构建（非 QM，属于结构准备）

| 产物 | 绝对路径 | sha256 | 说明 |
|---|---|---|---|
| I1(S) 预复合物候选（构建器组装） | `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/prep/structure_build_I1S/assembly/complex_candidate_000.xyz`（另有 001–004） | 见下方 sha 表 | 41 原子，3 分片（烯胺+水+苯甲醛），RDKit 3D 判定 proline Cα=S；r(C1···C29)=4.675 Å；COOH H···O=C(Ph) 1.676 Å |
| P(S,S) 产物候选 | `…/E3/prep/structure_build_P/assembly/complex_candidate_000.xyz`（另有 001–008） | 见下方 sha 表 | 41 原子，2 分片（aldol + 脯氨酸），CIP：aldol C=S、proline Cα=S |
| 几何准备输入（约束优化） | `…/E3/prep/I2_prep_cons180_v2.gjf` | 见下方 sha 表 | `#p opt=modredundant B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=DMSO)` + `B 1 29 1.80`；%nproc=12 %mem=14000MB |
| 核验脚本 | `…/E3/tools/xyz_identity.py`、`rank_i1_candidates.py`、`interfrag_contacts.py` | 见下方 sha 表 | RDKit DetermineBonds + AssignStereochemistryFrom3D 的 CIP/分片核验 |

### 2.2 QM 作业（本道，Gaussian 16）

| job | 角色 | 输入 | 状态 | 能量 |
|---|---|---|---|---|
| 910 | I2 几何准备（约束优化 d(C1···C29)=1.80 Å） | `…/E3/prep/I2_prep_cons180_v2.gjf` | **failed**（l101，几何段尾缺空行） | —（**不作能垒证据**） |
| 待提交 | I2 无约束 Opt+Freq（本道 I2 极小值） | — | 待 910 末端几何 | 待填 |

**拒绝的构建尝试（技术障碍，非化学结论）**：`smiles_to_mol("CC(C[C@H]([O-])c1ccccc1)=[N+]1CCC[C@H]1C(=O)O.O", generate_3d=True)` → 构建器 frag0（38 原子 zwitterion）MMFF94 迭代 20000 次未收敛（final max_gradient 0.037）→ 复合物组装 gate 拒绝；`conformer_search(backend='crest', mode='nci')` 在同一构建器层被拒。产物目录：`…/E3/prep/structure_build/`（zwitterion 38 原子 + 水）与 `…/E3/prep/crest_nci/`。

---

## 2.3 B 段续跑（lane2，2026-10-15 19:0x）：实际作业与产物记录

### 2.3.1 本道 QM 作业（全部 Gaussian 16；日志绝对路径 + sha256 + 原始行）

| job | 角色 | 输入（绝对路径） | 输入 sha256 | 日志（绝对路径） | 日志 sha256 | 状态 / 原始行 |
|---|---|---|---|---|---|---|
| 910 | I2 几何准备 v2（约束 d(C1···C29)=1.80 Å） | `…/HI1/E3/prep/I2_prep_cons180_v2.gjf` | `a1bfb5093857d99e62f238f0e46a968d88f665c8df76855f5cf2f1972de1e8ab`（上轮记录值） | `…/E3/prep/I2_prep_cons180_v2.log` | 未取（失败作业） | **failed**：l101 `Wanted a floating point number` @ `B 1 29 1.80`（几何段尾缺终止空行）；错误另存 `state_910.json` sha256 `62090dcc2fc53403b9b157df0d64b1dfb61757862006e9762ac865c84607b912` |
| 925 | I2 几何准备 v3 | `…/E3/prep/I2_prep_cons180_v3.gjf` | `4f8c4851b8ba74013c1cc162c1158ce7d826ac93a1637fe446ce1bc5b0c292c3` | `…/E3/prep/I2_prep_cons180_v3.log` | `5045c0e847b03697692ebdc47ebb8569556ef3f9368b3fab480d4a1f6e2442db`（5311 B） | **failed**：l1 `QPErr --- A syntax error was detected in the input line`（说明文字占用 route 段终止空行）@ 18:35:17 |
| 945 | I2 几何准备 v4（格式正确；单跳约束） | `…/E3/prep/I2_prep_cons180_v4.gjf` | `60c64bb45ac7aad07f21eeb0d5c5c4238556b6ef96b6b5503d4504e3d1b7486c` | `…/E3/prep/I2_prep_cons180_v4.log` | `41c8ca64249a2d5108e634e4f1a683a17face131700f5d3d2c7e1592fe83d3ec`（13960 B） | **failed**：`New curvilinear step not converged. / RedCar failed in NewRed.` @ l101 19:02:33，**无任何 SCF Done** |
| 951 | I2 几何准备 v5 = **弛豫扫描** `B 1 29 S 8 -0.360000` | `…/E3/prep/I2_prep_scan_v5.gjf` | `afbe9ba904046fabc992df205f51738d4ff1de5724b3973447f34e3190f56b3e` | `…/E3/prep/I2_prep_scan_v5.log` | 待产出 | **已提交** 19:1x（8c/8192MB，priority 0）；该作业只作几何准备，能量不作能垒证据 |

### 2.3.2 非 QM 产物（本道）

| 产物 | 绝对路径 | sha256 |
|---|---|---|
| 上轮 candidate_only 缺口清单 G1–G6（含 reaction_mapping 逐字返回附录 A） | `…/HI1/E3/evidence/CANDIDATE_ONLY_GAPS.md` | `b4e61dd5120e4c999aab3276acf820d93bcf5887284b1d1e2212f8d2c737aae8` |
| ts_prepare 声明草稿 + 绑定序换算表 + 验收判据 | `…/HI1/E3/prep/E3_DECLARATION_DRAFT.md` | `b1bc1bc1922462ca472d1d56fe661188680e4b806e4c92b38f27befccc7e9154` |
| I2→P 完整 concrete atom_map（手工；产品序 → 反应物 1-based） | `…/HI1/E3/prep/I2_P_atom_map.json` | `33912bbd415bc424da1f086bc61c696cd6b9eac5f4f2aa7c8b550cd3ce3a980e` |
| P(S,S) 种子候选（41 原子、2 分片、aldol C=S、Cα=S） | `…/HI1/E3/prep/structure_build_P/assembly/complex_candidate_000.xyz` | `06161a1411edf1e1402620ee13ca448c14d2ac167846c10f1e56bf8ec175078a` |
| I1(S) 预复合物候选（41 原子、3 分片、Cα=S、r(C1···C29)=4.675 Å） | `…/HI1/E3/prep/structure_build_I1S/assembly/complex_candidate_000.xyz` | `0d308bd3fdd04afe2c212dee0cc614c9a5697236f50a60e130f494a4299ee9f3` |
| 预复合物内部坐标分析 Z-matrix（46 行）+ 报告 | `…/HI1/E3/prep/precomplex_analyze.zmat` | `bc4f2e0949f10f23cd71f2222dc1844c44587787a67685a7a1d94375985a3bf5` |
| 槽位记录 | `…/HI1/qm_slots/slot2/holder.txt` | `f4d00f3d87683baad73792ea90b723ab4563fe959220f9d8d3c142206c118048` |

预复合物 analyze 关键读数（可复现）：41 原子 / 3 分片 / C8=S；r(C1–C29)=4.675 Å（far）；r(C2–N4)=1.395 Å（单键）；r(O25–H26)=0.974 Å、r(O25–H27)=0.982 Å（水）；r(O28–C29)=1.229 Å（苯甲醛 C=O 双键）；异常项 = O10···H27 1.765 Å 与 **H24···O28 1.676 Å**（`forming_candidate`，距离启发式，非化学结论）。**风险登记**：H24 为羧基 H，若扫描中转移到 O28，终点将是"中性 aldol + 羧酸根"而非声明的两性离子 → 按实测报告。

### 2.3.3 状态口径（严格区分）

- **计算完成：E3 目前 0 个有效 QM 结果**（3 次失败均在输入/优化器层面；1 次在跑）。
---

## 2.4 B 段完成（lane2，2026-10-15 22:0x）：I2 极小值 + TS 初猜记录

### 2.4.1 job 961 = E3 的 I2 侧参考极小值（0 虚频，成立）

| 项 | 值 |
|---|---|
| 输入 | `…/HI1/E3/runs/I2_optfreq/I2_optfreq.gjf` sha256 `93cbce28547d2d547424f0da79f315d8f274024cb661f8fc8ecda8beae4ddc46`（route `#p opt freq B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=DMSO)`，q0/m1，8c/8192MB，priority 0） |
| 起点 | `…/E3/runs/I2_optfreq/I2_start_v5.xyz` sha256 `5b8f7d6a811ab35911776025ee91d7cf9df09c3fdc60dd38469f03b9ee09dcb5`（= job 951 弛豫扫描末帧，d(C1–C29)=1.795 Å） |
| 日志 | `…/E3/runs/I2_optfreq/I2_optfreq.log` sha256 `63dda25e04529e65920526304fb88755db9393e9c22bd3a6efb76eeee0af0d0e`（1,592,586 B） |
| 终止 | `Normal termination of Gaussian 16 at Thu Oct 15 22:05:55 2026`（log 24001；log 18401 = opt 段结束，勿误判） |
| 收敛 | `Optimization completed.` + `-- Stationary point found.`（四项判据全 YES） |
| 频率 | 117 模，最低 35.3075 / 46.4262 / 50.3299 cm⁻¹ → **0 虚频** |
| 能量（原始行） | `SCF Done:  E(RB3LYP) =  -939.320655479     A.U. after    6 cycles`（log 16950）；ZPE 修正 0.345935 Ha；Gibbs 热修正 0.297654 Ha |
| 身份（RDKit 3D） | `natoms=41 frags=2 CIP[8C=S(nb 7C,4N,9C,23H); 29C=S(nb 28O,1C,30C,36H)]` → **原子 8=S、原子 29=S** |
| 末帧 xyz | `…/E3/runs/I2_optfreq/I2_min_v5.xyz` sha256 `9a6203ff67d9f0d95ad774e78b17bc397b22992f24cbcdf448f8c5558142ef2b` |
| 关键几何（Å） | C1–C29 1.588 / C2–N4 1.299 / O28–C29 1.403 / O28–H24 0.984 / O11–H24 1.791 / O25–H26 0.966 / O25–H27 0.990 / O10–H27 1.717 / C2–O25 3.160 |
| 物种 | iminium + aldol-OH + 羧酸根 + 旁观水（2 分片）——**与题源 SMILES 的质子位置不同（题源为 alkoxide + COOH）** |

### 2.4.2 job 962（进行中）= TS 初猜的手工预组织（非能垒证据）

- 输入 `…/E3/runs/preorg_v1/preorg_c2o25_220.gjf` sha256 `5d560c45669d2cff0370b6a0258aabdbe182d4f20c7b22f082c7502200dad5ec`（`opt=modredundant` + 约束 `B 2 25 2.20`，起点 = I2 `I2_min_v5.xyz`，8c/8192MB，priority 0）；用作 `ts_prepare` 的 provided guess。
- 工具缺陷复现（同 §2.3/E.6）：`qm_input_writer` 生成的该输入**缺几何段终止空行**（line49 末坐标 → line50 `B 2 25 2.20`），已手工补空行（补后 sha 如上）。

### 2.4.3 TS 初猜（非 QM）IDPP 插值（两次，均判定不合格）

| 版本 | 目录 | atom_map 口径 | 工具自报候选 | 判定 |
|---|---|---|---|---|
| v1 | `…/E3/runs/interp_v1/`（20 帧） | 题源 map（H27→O28、H24 留 O11） | `img_11.xyz` | 非协同鞍点帧（C2–N4 在帧 10 已 3.37 Å） |
| v2_taut | `…/E3/runs/interp_v2_taut/`（20 帧） | 互变体 map（H24 留 O28、H27→O11） | `img_10.xyz` | 同上（C2–N4 帧 9→10 由 2.75 跳 3.61 Å） |

结论：IDPP 对"水进攻 + C–N 断裂 + 双质子转移"这类构象重组大的合并边不适用 → 改用手工预组织（job 962）+ `ts_prepare` 的 OptTS 完成正式鞍点搜索。
---

## 2.5 B/T 段补充（lane2，2026-10-15 23:4x）：预组织与扫描实测（含一条工具面教训）

### 2.5.1 job 962 = 约束优化预组织：**约束未生效**（工具面教训，重要）

| 项 | 值 |
|---|---|
| 输入 | `…/E3/runs/preorg_v1/preorg_c2o25_220.gjf` sha256 `5d560c45669d2cff0370b6a0258aabdbe182d4f20c7b22f082c7502200dad5ec`（卡 `B 2 25 2.20`） |
| 日志 | `…/E3/runs/preorg_v1/preorg_c2o25_220.log` sha256 `759bce701518a329f5d0d5ce1e2605afb3d1feae28deb095e1c5c983eb85bdc8`（1,979,356 B） |
| 结果 | `Stationary point found` + `Normal termination` 22:29:15；末次 `SCF Done: E(RB3LYP) = -939.320655427 A.U.` |
| **实测** | 首帧 r(C2–O25)=2.248 Å（RedCar 初始化位移）→ 随后 2.385 → 2.734 → 2.931 → **末帧 3.160 Å**（= 未约束的 I2 极小值）；末帧 `Optimized Parameters` 明写 `R7 R(2,25) 3.1597` → **约束未被保持** |
| 结论 | 裸 `B i j value` 卡本次**静默失效**；对照 job 945 同形式卡（2.9 Å 位移）在 RedCar 阶段失败（那里像被当作约束）。**凡用约束优化做几何准备必须核对终态坐标值** |

### 2.5.2 job 963 = 弛豫扫描 C2–O25 3.16→2.20 Å（被强制执行；无内峰）

| 项 | 值 |
|---|---|
| 输入 | `…/E3/runs/preorg_v2/scan_c2o25_316_220.gjf` sha256 `60a25746b3abd96e2af6628a08e126f603f1f526363354a27cb28a49d2602b5e`（扫描卡 `B 2 25 S 3 -0.320000`；route `# opt=(modredundant,maxstep=10) B3LYP/def2SVP …`） |
| 日志 | `…/E3/runs/preorg_v2/scan_c2o25_316_220.log` sha256 `e535fb2f1bc5b7259aaed18ba7f391290bfec3e4f07ce39cf146238ed63c27cf`（3,914,230 B）；`Normal termination` 23:38:46；4 点全部收敛；末次 SCF `-939.307665339` |
| 扫描剖面（约束扫描相对能量，**不作能垒证据**） | 帧0 0.000 / 帧1 +0.954 / 帧2 +4.004 / 帧3 **+8.151** kcal/mol → 单调上升、**无内部峰**（`scan_has_internal_peak=false`, `candidate=null`） |
| 坐标实测 | C2–O25 3.160 → 2.840 → 2.520 → 2.200 Å（扫描确实被执行） |
| 末帧几何 | `…/E3/runs/preorg_v2/ts_guess_c2o25_220.xyz` sha256 `640405ff9b4f59c234fd966fadd1689c7717feb924fc7b4fd40b18a72e1a2bec`（41 原子、2 分片、物种不变）；C2–N4 1.305、O28–H24 0.988、O10–H27 1.675、O25–H26/H27 0.968/0.996 |

### 2.5.3 已备好、待提交：延伸扫描 C2–O25 2.20→1.60 Å

- 输入 `…/E3/runs/preorg_v3/scan_c2o25_220_160.gjf` sha256 `35f151c75fc3f00b4e2a3c2ac0564098084efa4192a932a33b95bac197f76bbc`（`B 2 25 S 4 -0.150000`；起点 = 2.20 Å 弛豫几何；8c/8192MB，priority 0）。
- 目的：穿过 C2–O25 成键与潜在质子转移区，判定是否存在内部峰（有 → TS 候选交 `ts_prepare`；无 → "无独立鞍点/需拆步"的实证）。


- **验收通过：无**。**能垒：缺测**（G1–G6；不填 0、不引用旧值 16.9/19.2）。

