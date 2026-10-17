# HI1 E2EM1 · lane3 ((S)-脯氨酸体系重算) 状态 · 2026-10-15

会话：small_mol `as_3509ff4f56ea402c`。产出目录：`gold_finish_20261015/HI1/E2EM1/`。
任务书：主协调 2026-10-15 裁定（HI1_E2=13.36 / HI1_EM1=15.52 建在 R-脯氨酸几何，与 10-14 纠正后的 (S) 题源为非对映体 → 本道重算；新值验证前不动旧值）。
方法（**本批 Gaussian 16**）：B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight + SCRF=(CPCM,Solvent=DMSO)，q0 / m1；能垒 = 纯电子能差，相对**同一 (S) HI1_I1 极小值**。
引擎差异口径：历史值来自 ORCA 6.1.1（RIJCOSX/def2-J/TightSCF），本机无 ORCA；**不得**与历史值相减（BRIEF §3）。

## 0 lane3 接续交接（2026-10-15 19:0x；上一位 lane3 会话 as_3509ff4f56ea402c = failed，产物全部在磁盘）

**非 QM 准备已完成（全部为本道本机产出，可复核）**

| 产物 | 路径（相对 `gold_finish_20261015/HI1/E2EM1/`） | sha256 |
|---|---|---|
| 通道 A 种子 provenance | `build/TS_SEED_PROVENANCE_E2.md` | `121ac600f960b933bd56e7a055bcdaaa021a8f46af884bf9779cabe6e2c93b07` |
| 通道 B 种子 provenance | `build/TS_SEED_PROVENANCE_EM1.md` | `73ee4aa81a4f31c120dbbd5dc9c41abe71164d7852f9d404fb4e297b26c3ec5b` |
| 原子序 ↔ map ↔ watch pair 换算表 | `build/ATOM_ORDER_AND_WATCHPAIRS.md` | `6820379bec23fe0c7e2e79f91020a2e81a2a989d7d7e251606152d41ed1d9957` |
| 种子重排脚本（source 序 → 绑定序） | `build/reorder_guess_by_permutation.py` | `30e39ec7f499e684f0eed7d70d77cbc3858915485b8c2b503d02403a9e87bfa5` |
| E2 种子几何体检 Z-matrix | `evidence/geomcheck_TS_guess_E2.zmat` | 见下方证据清单 |
| EM1 种子几何体检 Z-matrix | `evidence/geomcheck_TS_guess_EM1.zmat` | 见下方证据清单 |

**几何体检（internal_coordinates analyze，本道 2026-10-15 复核；不是 QM 证据）**
- **E2 种子**：C15H21NO4 / 41 原子 / 3 分片 / 40 键；RDKit 判定唯一手性中心 **C8 = S**；r(C1–C29)=**2.275 Å** forming_candidate；C2–N4=1.358 Å、C2–C1=1.380 Å（键级 2）、O28–C29=1.242 Å（键级 2）；异常键 3（C1···C29 forming、O10–H26=1.915 Å、H27–O28=1.775 Å 两个显式水氢键）、异常角 2（N4 锥角 125.8°/122.6°）。
- **EM1 种子**：同式 / 41 原子 / 3 分片；**C8 = S**；r(C1–C29)=**2.800 Å**（far，未成键）；0 异常键；异常角 2（N4 124.6°/121.9°）。
- 结论：两种子均无原子重叠、无异常环、手性中心仅 C8=S；E2 种子的“椅式”由**显式水桥**（O10···H26、H27···O28）维持，不是 COOH···O=C。
- 镜像可复算性：两种子与其 ORCA 源帧（job_58 f7 / job_59 f9）z→−z 镜像 **maxdev = 0.000000 Å**，未镜像时 10.999726 / 7.805166 Å（详见各自 provenance 文件）。

## 0b 验收清单（lane3，(S) 体系；缺一项即未通过）

| # | 项 | 判据 | 证据 |
|---|---|---|---|
| 1 | **参考极小值** | **job 924**（(S)-HI1_I1 Opt+Freq，输入 `runs/I1_optfreq/I1_S_optfreq.gjf`）：0 虚频、3 分片、Cα（1-based 原子 8）RDKit 3D 实测 = **S** | 原生 log 绝对路径 + sha256 + 原始行能量 |
| 2 | TS | 恰 1 虚频，且虚频模以 **C3–C6**（work 序 1–29）主导 | log_parser（绑定序换算后的 watch_pairs）|
| 3 | IRC | **双向**真实到达 (S)-I1 与 I2（A）/ M1（B），给方向区间端点归属 | 原生 IRC log + 端点几何 |
| 4 | 两端点 | 无约束 Opt+Freq、**0 虚频**；**I2 map6 = S / M1 map6 = R**、两处 Cα = S | 原生 log + RDKit 实测 CIP |
| 5 | **能垒** | **E(TS) − E(job 924)**，纯电子能（无 ZPE/热校正）、同批 Gaussian 16 同程序相减。**禁止**改用 job 907（E1 的 (S)-RC，物种不同：907 = 脯氨酸+丙酮+苯甲醛，924 = 烯胺+水+苯甲醛）；**禁止**用工作流自身的 reactant 端点替代 924。只有 924 未过验收（0 虚频 且 Cα=S）才另议，且必须先报包 Coordinator 并写明替代 provenance | 原始行能量 + 算式 |
| 6 | ΔΔ | E(TS_minor) − E(TS_major)，与历史 2.16 **如实对比（含符号）** | 同上 |
| 7 | 原生日志 | **不改写** + 绝对路径 + sha256；能量只取自日志原始行 | 证据清单 |

**报告格式（每通道一行）**：边 | 通道 | E(TS)/Eh（原始行） | E(924)/Eh（原始行） | ΔE‡ kcal/mol | 虚频数/频率 | IRC 双向端点归属 | 两端 CIP（I2 map6=S / M1 map6=R、两处 Cα=S） | TS log 绝对路径 + sha256

**两条通道一律串行**，本包同刻 ≤2 个作业（含排队）；手工提交 priority 0；队深 ≥6 时只提关键路径作业。

## 1 通道状态（一行一通道）

| 边 | 通道 | 状态 | 值 | 缺测 / 缺什么 |
|---|---|---|---|---|
| HI1_E2 | major_face → HI1_I2 (map6=S) | **缺测（平台故障阻塞，尚未提交）** | — | TS(1 虚频, C3–C6 主导) / 双向 IRC / 两端 Opt+Freq / 能垒 全部缺；缺的是 QM 机时，不是方法或几何 |
| HI1_EM1 | minor_face → HI1_M1 (map6=R) | **缺测（同上）** | — | 同上 |
| （共同基线）(S) HI1_I1 极小值 | — | **缺测** | — | Opt+Freq 输入已生成待提交：`runs/I1_optfreq/I1_S_optfreq.gjf`（8c/8GB）。若 lane1 (as_4c9dafe225a84580) 的 (S) I1 先生效，优先复用（同方法同引擎，须写明来源 + 与我的重算交叉核对） |

**阻塞原因**：2026-10-15 16:55 起 compute.db 写锁故障（主协调广播 + 直接令）：submit_compute_job 返回 `database is locked`，job_id=-1，**未创建作业记录**。主协调令：暂停提交、不重投、不撤排队作业。本道已遵守；本道 running/queued = 0。恢复后立即按 §4 提交。
**阻塞不会改变科学结论**：以下 §2 的非 QM 结果不依赖 QM。

## 2 非 QM 准备（已完成，可复核）

### 2.1 起点几何（(S) 身份已复核）
- `build/I1_S_from_job59.xyz`（我造的第二构象 (S) 起点，= job_59 scan_minor_clean.001.xyz 的 z 镜像；d(C3–C6)=6.000 Å）sha256 `22f730d231bc91c39f73851e62b9d8eba0db6357a7aaeeddab6484226df2e697`
- 复用 E1 道 (S) 起点：`gold_finish_20261015/HI1/E1/build/I1_S_start.xyz` sha256 `c9d59aeab418c248629922ee37d4ea3822c64b7128dd63b3034d3c8c5ec2df3d`（我逐原子核对 = ORCA job_51 rc_clean_np8.xyz 的 z 镜像，maxdev = 0；Cα 三重积 −5.026 → +5.026 = S）
- **CIP 实测（RDKit，脚本 `build/dbg_cip_adduct.py`）**：两个 (S) 起点脯氨酸 Cα（1-based 原子 8 = map16）均为 **S**。

### 2.2 TS 种子（来自本地 ORCA 弛豫扫描链，镜像成 S；**只作几何种子，能量一律不用**）
PLAN §3 未列的两个本地素材：`gold_compute/grant_materials_20261001/raw/HI1/job_58/`（major 目录名扫描链 d(C3–C6)=4.3→1.6 Å，9 帧）、`job_59/`（minor 目录名扫描链 6.0→2.4 Å，10 帧）。
| 文件（`build/`） | 来源帧 | d(C3–C6)/Å | d(C2–N20)/Å | 预测 aldol C (map6) CIP | sha256 |
|---|---|---|---|---|---|
| TS_guess_E2_j58f7.xyz | job_58 f7 | 2.275 | 1.358 | **S** | 9e5ccc2f… |
| TS_guess_E2_j58f6.xyz | job_58 f6 | 2.612 | 1.372 | S | 8d072e25… |
| TS_guess_E2_j58f8.xyz | job_58 f8 | 1.938 | 1.330 | S | 5024997e… |
| TS_guess_EM1_j59f9.xyz | job_59 f9 | 2.800 | 1.388 | **R** | a7b50b7c… |
| TS_guess_EM1_j59f8.xyz | job_59 f8 | 3.200 | 1.405 | R | 43b2eb3f… |
| TS_guess_EM1_j59f10.xyz | job_59 f10 | 2.400 | 1.370 | R | 72258b85… |
（全部 41 原子，ORCA job_51 原子序：1=C3(map3 β-C)、2=C2(map2)、3=C1(map1 CH3)、4=N20、8=Cα(map16)、28=O5(map5)、29=C6(map6)、25–27=水 O,H,H。）

预测方式：把帧几何按 map 拓扑强加成加成物连接（C3–C6 单键 + iminium C2=N20+ + alkoxide C6–O5−），RDKit `AssignStereochemistryFrom3D` + rdCIPLabeler 读 C29（=map6）的 `_CIPCode`。
**这是几何预测，不是 QM 结论**；最终以 TS 端点的实测 CIP 为准。
自洽性：镜像(job_58 链) → map6=S（题源声明的 HI1_I2/major_face）；镜像(job_59 链) → map6=R（题源声明的 HI1_M1/minor_face）→ 与题源 face↔产物 CIP 声明一致。
附带解释：**未镜像**的原始帧同一测算显示 job_58 链（目录名 major_spec）→ map6=R、job_59 链（目录名 minor_spec）→ map6=S，即目录名与声明通道相反——这解释了 hard_hi1_2026-10-01.md 的 “directory and working face names do not define the declared channel”。本道按最终 CIP 而非目录名分配通道。


### 2.2b 可复现命令与原始输出（每条 CIP 结论绑定到实际运行）
脚本（两条均已修好 2026-10-15 的拓扑 bug：adduct 模式保留 C6–O5 单键，否则 aldol 碳只有 3 个邻居）：
- `build/dbg_cip_adduct.py` sha256 `8e7f852f43432519f7c646b32c04a0f4f09a3381bc827ec028de279c7ea47762`（**基准脚本**；打印 1-based 原子号 8=Cα(map16)、29=aldol C(map6) 的 `_CIPCode`）
- `build/check_cip_lane3.py` sha256 `c3153ee0306865c4167ae1a31c2f5c6f95c79f189897693c739387a3535b5d1d`（打补丁后与基准脚本结论一致；打印 0-based RDKit idx：(7)=Cα、(28)=aldol C；(8) 是 COOH 碳被几何畸变误标为潜在中心，应忽略）

命令 A（基准脚本，原始 ORCA 帧 + 镜像种子）：
```
cd /home/ly/Cloudra-mechanism-agent && python3 gold_finish_20261015/HI1/E2EM1/build/dbg_cip_adduct.py \
  gold_compute/grant_materials_20261001/raw/HI1/job_58/scan_clean_np8.00{6,7,8}.xyz \
  gold_compute/grant_materials_20261001/raw/HI1/job_59/scan_minor_clean.0{08,09,10}.xyz \
  gold_finish_20261015/HI1/E2EM1/build/TS_guess_E2_j58f{6,7,8}.xyz \
  gold_finish_20261015/HI1/E2EM1/build/TS_guess_EM1_j59f{8,9,10}.xyz \
  gold_finish_20261015/HI1/E1/build/I1_S_start.xyz gold_finish_20261015/HI1/E2EM1/build/I1_S_from_job59.xyz
```
输出（节选，完整输出见本目录 hub 帖 evt_db318b7373ce45b4 与复核方复现）：
```
scan_clean_np8.006/007/008.xyz  {8: ..., 'R'), 29: ..., 'R')}      # R-Pro + R-aldol
scan_minor_clean.008/009/010.xyz {8: ..., 'R'), 29: ..., 'S')}     # R-Pro + S-aldol
TS_guess_E2_j58f6/7/8.xyz        {8: ..., 'S'), 29: ..., 'S')}     # S-Pro + S-aldol = 题源 HI1_E2/I2
TS_guess_EM1_j59f8/9/10.xyz      {8: ..., 'S'), 29: ..., 'R')}     # S-Pro + R-aldol = 题源 HI1_EM1/M1
I1_S_start.xyz                   {8: ..., 'S'), 29: ..., 'S')}     # 起点 Cα=S（d(C3-C6)=4.354 时 aldol C 判定无化学意义，仅记录）
I1_S_from_job59.xyz              {8: ..., 'S'), 29: ..., 'R')}     # 起点 Cα=S（d=6.0，同上）
```
命令 B（补丁后脚本，同文件集）：`python3 .../build/check_cip_lane3.py x <同一文件集>` → 逐行结论同命令 A（`(7,'S/R')` = Cα、`(28,'S/R')` = aldol C）。
**限定（重要）**：以上全部是**几何预测**——把帧几何按加成物拓扑（C3–C6 成键 + iminium C2=N20⁺ + alkoxide C6–O5⁻）强制连接后由 3D 坐标定 CIP；它**不是** QM 端点证据，也不能替代 TS/IRC/端点验收。最终判定以本批 Gaussian 16 的 TS 与两端点实测 CIP 为准。

### 2.3 几何体检（internal_coordinates analyze）
- TS_guess_E2_j58f7：3 键异常（C1···C29=2.275 forming；O10–H26=1.915、H27–O28=1.775 为**显式水**同时氢键到羧基 O 与苯甲醛 O——该帧的“椅式”由水桥维持，不是 COOH···O=C），2 角度异常（N4 锥角 125.8/122.6°，iminium 化正常）。
- TS_guess_EM1_j59f9：0 键异常，2 角度异常（N4 锥角 124.6/121.9°）。
两个种子均无原子重叠、无异常环，手性中心仅 C8=S。


### 2.4 镜像对应关系与 ΔΔ 的先验（非 QM 推理，供对照，不作证据）
历史 ORCA 记录（hard_hi1_2026-10-01.md）：R-脯氨酸体系 E2/13.36 → 产物 C8R/**C29S**（= R-Pro + S-aldol），EM1/15.52 → C8R/**C29R**（= R-Pro + R-aldol）。
本道同一 RDKit 测算（§2.2）给出：**未镜像**的 job_58 链 → C8R/C29**R**、job_59 链 → C8R/C29**S**。
→ 历史 E2(13.36) 对应 **job_59 链**，EM1(15.52) 对应 **job_58 链**（与“目录名不可信”一致）。
镜像后（题源 = (S)-脯氨酸）：
- mirror(job_59 链) = S-Pro + **R**-aldol = 题源声明的 **HI1_EM1 / M1**（minor_face）
- mirror(job_58 链) = S-Pro + **S**-aldol = 题源声明的 **HI1_E2 / I2**（major_face）
因此按镜像对称（对映体能量相同，同方法同溶剂）**先验预期**：在 (S) 体系里 E(TS_M1) ≈ 13.36-equiv < E(TS_I2) ≈ 15.52-equiv，即
**ΔΔ = E(TS_minor) − E(TS_major) ≈ −2.16 kcal/mol（与历史 2.16 反号）**。
⚠ 这只是先验对照：题源 favored=true 挂在 HI1_E2（S-aldol）上，若本道重算复现负号 ΔΔ，则与题源 favored 声明相反——**本道不改图、不改 favored**，只如实报数并交主协调裁决。所有结论以本批 Gaussian 16 实算为准。

## 3 关键结构处置
- 41 原子体系 = 烯胺(C8H13NO2) + 显式水 + 苯甲醛，q0/m1。**保留显式水**（历史 job_51 模型一致；水是 E1 步的离去水，且在 seed 中参与氢键）。
- map ↔ 本批原子序（1-based，ORCA job_51 序）：map1↔3、map2↔2、map3↔1、map4↔25、map5↔28、map6↔29、map7–12↔30–35、map13↔10、map14↔9、map15↔11、map16↔8、map17–19↔5–7、map20↔4、map21/22↔26/27（水两 H）、map22（原 C3–H）在 I1 中属于水。
- 键变化（题源）：break [[2,3],[5,6]] → 本序 break [[2,1],[28,29]]；form [[2,20],[3,6]] → 本序 form [[2,4],[1,29]]。

## 4 下一步（lane3 接续，2026-10-15 19:0x 起；不改口径）
0. 非 QM 准备已完成（见 §0 / §0b）：两份种子 provenance、原子序↔map↔watch pair 换算表、重排脚本、两种子几何体检。
1. 等 **job 924**（(S)-HI1_I1 Opt+Freq，已在队列）出结果 → 核验 **0 虚频 / Cα=S / 3 分片**（log_parser + `shared/tools/hi1_cip_tools.py`）；**不通过则先报包 Coordinator**，不得自行替换基线（禁止 907、禁止工作流 reactant 端点，见 §0b 第 5 项）。
2. 924 通过、且本包在手作业数降到 ≤1、队深允许时，启**通道 A**：`ts_prepare`（engine=gaussian，8c/8192MB；conformers.reactant = file `gold_finish_20261015/HI1/E1/build/I1_S_start.xyz` + `build/I1_S_start_ref.mol`）**第一次不带 guess** → `ts_inspect` 读绑定序 + `source_to_canonical` → `build/reorder_guess_by_permutation.py` 重排 `build/TS_guess_E2_j58f7.xyz` 并同步换算 reaction_center → `ts_resume`（带 reason + 该 run 的 revision；权威 revision 在 `ts/<run>/process.json`）。
3. 通道 A 收工（terminal/blocked）后再启**通道 B**（同法；种子 `build/TS_guess_EM1_j59f9.xyz`，conformers.reactant = `build/I1_S_from_job59.xyz` + `.mol`）——两通道**串行**，同刻在包作业 ≤2（含排队）、手工 priority 0。
3. 验收清单（缺一项即未通过）：TS 恰 1 虚频且 C3–C6 主导（log_parser watch_pairs=[[1,29]]）；IRC 双向区间端点归属；端点 0 虚频 + CIP（I2 map6=S、M1 map6=R、两处 Cα=S）；能垒 = E(TS)−E(同一 (S) I1)，本批 Gaussian 同程序相减；ΔΔ = E(TS_minor) − E(TS_major) 并与历史 2.16 如实对比。
4. 原生日志不改写，路径 + sha256 + 原始行能量记入 `evidence/`。

## 5 provenance 与方法一句（computed_by_us）
本道全部数值（完成时）将来自 computed_by_us=True 的本机 **Gaussian 16**（`/home/ly/g16/g16`）单一批次，输入为上述 41 原子几何；历史 ORCA 6.1.1 的 job_51/52/54/58/59/64 几何**只作几何种子/身份参考，其能量一律不参与任何差值**。与历史 13.36/15.52 的对比只是叙述性对照，不作标答继承。

## 6 lane3 续（2026-10-17，接管会话；run 已解锁并在跑���

**run/作业实读（ts_inspect，2026-10-17 06:4x）**
- 通道 A：`ts_0009`（`ts/ts_0009`）revision 20，status=waiting，stage=build，blocked=null，result.outcome=null；
  waiting_for=[job 993 candidate_opt，8c/8192MB，input `ts/ts_0009/jobs/declaration_0004/candidate_opt/seed-opt.gjf`]（管线自动作业）。
- 通道 B：`ts_0012`（`ts/ts_0012`，本会话经 ts_prepare 新建）revision 5，status=waiting，stage=build，blocked=null；
  waiting_for=[job 1000 candidate_opt，8c/10240MB，input `ts/ts_0012/jobs/declaration_0001/candidate_opt/seed-opt.gjf`]。
- 两通道在飞作业 = 2（≤2 上限）。方法统一 `lane3_g16_dmso` = Gaussian16 B3LYP/def2SVP + EmpiricalDispersion=GD3BJ +
  Int(UltraFine) + SCF=Tight + SCRF=(CPCM,Solvent=DMSO)，q0/m1。

**#180 未复现**：ts_0009 的 ts_resume 被平台接受（receipt.status="accepted"，原文）：
`tc_cafbf2fec2e14c24`（rev12→13：atom_map/product_smiles/reaction_center/方法）、`tc_a1d1eaf0bdec40b1`（rev16→17：显式 heavy_atom_binding）。
另两次失败为**输入校验/并发保护**，不是 owner 拒绝：(a) `ts_resume: active compute jobs prevent input revisions`（job 993 在跑）；
(b) product 身份不符（见下）。

**已修复的平台输入校验问题（证据 `evidence/BINDING_AND_MAP_VERIFICATION_20261017.md` sha256 3432e7c19a685859ff37aef1140c1e4b293150c5e067066300c77bd981aea67a）**
1) product 声明缺 C2=N4 E/Z。平台原文："ts_resume: product: inherited heavy-atom binding is invalid: ... Declared identity:
   CC(C[C@H]([O-])c1ccccc1)=[N+]1CCC[C@H]1C(=O)O.O; concrete identity: C/C(C[C@H]([O-])c1ccccc1)=[N+]1\CCC[C@H]1C(=O)O.O.
   Changing binding indices cannot repair this identity mismatch." → 改为 concrete canonical 串（RDKit 复核逐字一致）。
2) reactant heavy-atom binding 不唯一。平台原文："reactant: The concrete structure has 2 symmetric heavy-atom bindings;
   without concrete atom-map labels the binding is not unique."（needs=[conformers.reactant]）→ 用显式 H 数消歧，声明显式 indices。

**绑定序 / map（本 run bound 序 = ORCA job_51 序，1-based）**
- atom_map = 恒等（product 第 i 原子 ↔ reactant 第 i 原子）；reaction_center = `[[1,29],[2,4],[2,1],[28,29]]`
  （平台内部 0-based 回读 `[[0,28],[1,3],[1,0],[27,28]]`）；生成中的 C3–C6 = 原子 **1 与 29**。
- 通道 A：reactant binding `[3,2,1,4,5,6,7,8,9,10,11,25,28,29,30,31,32,33,34,35]`；
  product binding `[3,2,1,29,28,30,31,32,33,34,35,4,5,6,7,8,9,10,11,25]`。
- 通道 B（新造，本会话）：`build/I1_S_from_job59_bonded.mol`（原 `I1_S_from_job59.mol` 只有坐标无键块）
  sha256 0a8bed4bb738aca52ad5a3aee3f38a22ef9b902fa32be66c89294a476c642e49；`build/TS_guess_EM1_j59f9_adduct.mol`
  sha256 f25e6cbc6c45b646b001762f76ef337de559376ca698a81d6e0f7dcf4369929a；脚本 `build/make_mol_EM1_lane3.py`
  （fac51f609bcd66e13fcdb6e693ab602b8ec5db036c51088c656e52d2e7b4a8be）、`build/verify_channelB_lane3.py`（94d543d68869d1b081cd4ef0007c1e01a8ceb8d55ececa23f4e8c05e074ac714）。
  RDKit 3D 读数（几何预测，非 QM 结论）：Cα(concrete 8)=S、aldol C(29)=**R**、C2=N4 STEREOCIS；声明 SMILES 与 concrete canonical 串一致（IDENTITY MATCH: True）。

**几何种子（只作几何，能量一律不用）**：A `build/TS_guess_E2_j58f7.xyz` sha256 9e5ccc2f…（d(C1–C29)=2.275 Å）；
B `build/TS_guess_EM1_j59f9.xyz` sha256 a7b50b7c…（d(C1–C29)=2.800 Å）。两者与各自 bound reactant 同为 ORCA job_51 序
（重排 = 恒等），已作为 `guess.kind=provided` 声明（A 待 job 993 结束后补声明）。

**基线（不变）**：job 924 `runs/I1_optfreq/I1_S_optfreq.log` sha256 6ecf06238ee6e1e976ba30eb15faf655f3ebe5a0126ed37d0dfe9b687dea6a87，
line 20025 raw " SCF Done:  E(RB3LYP) =  -939.308218263     A.U. after    6 cycles"（line 22238 同值）。

**当前缺口（不变）**：E2/EM1 的 TS（1 虚频 + C3–C6 主导）、双向 IRC、两端 Opt+Freq(0 虚频)、CIP、ΔE‡、ΔΔ **全部缺测**；
不填任何数字，不改写原生 log。**模型口径（供交付说明）**：CPCM(DMSO) 隐式溶剂 + 保留 1 个显式水；q0/m1；无抗衡离子、
无显式 DMSO、无温度/浓度校正；加成物为 N⁺/O⁻ 内盐（净电荷 0）。引擎 = 本机 Gaussian 16（历史 ORCA 6.1.1，禁相减）。

**下一步**：job 993（A）结束 → ts_resume 补 E2 seed → 流水线自动 candidate_opt→TS→freq→IRC→两端点；
job 1000（B）结束 → 同一链路自动推进（guess 已声明）；逐阶段 ts_inspect + log_parser 复核；A/B 值齐后按验收清单 (a)-(f) 出终帖。

## 7 2026-10-17 08:1x 关键读数：通道 B 的 candidate_opt 落点 ≠ job 924 基线（**同一物种、不同构象**）

**原始读数**
- job 1000（ts_0012 candidate_opt，input `ts/ts_0012/jobs/declaration_0001/candidate_opt/seed-opt.gjf`）：
  log `ts/ts_0012/jobs/declaration_0001/candidate_opt/seed-opt.log`
  line **40743** raw " SCF Done:  E(RB3LYP) =  -939.302926757     A.U. after    7 cycles"；
  line **41130** " Optimization completed."；line **42210** " Normal termination of Gaussian 16 at Sat Oct 17 08:07:09 2026."
- job 993（ts_0009 candidate_opt）落在 **-939.308218263**，与 job 924 几何逐位一致（Kabsch RMSD = 0.000 Å）。

**同一物种（几何/连接性判定，非 QM 结论）**：两者均 41 原子 C15H21NO4、3 分片、Cα(1-based 8)=S、无其他手性中心；
d(C2–N4)=1.375 / 1.397 Å、d(C28=O29)=1.226 / 1.224 Å。

**不同构象**：通道 B 落点为伸展构象 d(C1–C29)=**7.293 Å**（种子 `I1_S_from_job59.xyz` 本身 d=6.000 Å），
而 924 / 通道 A 为紧凑构象 d(C1–C29)=**4.316 Å**；水氢键网络不同（924：O10···H26 = 1.886 Å；通道 B 落点：5.986 Å）。
Kabsch RMSD（41 原子）= **3.658 Å**，最大单原子偏差 6.649 Å。

**能量差（同批 Gaussian 16，纯电子能）**：−939.302926757 − (−939.308218263) = **+0.005291506 Ha = +3.32 kcal/mol**（通道 B 落点更高）。

**口径（不变）**：ΔE‡ = E(TS) − E(job 924)，**不得**用工作流自身 reactant 端点替换 924；若该端点落在 −939.3029，
交付时必须显式写明两者关系（哪一个是该步参考态、差 3.32 kcal/mol）。该构象差**不影响** ΔΔ = E(TS_B) − E(TS_A)（同批 TS 纯电子能差）。

**待办**：ts_0012 的 ts_opt（job 1013）出结果后，说明伸展构象起点是否影响通道 B 的连通性判据（IRC 反方向落在哪个构象）。

## 8 2026-10-17 09:1x 通道 B ts_opt（job 1013）读数：驻点在**反应物侧**，不是 C3–C6 加成 TS

**原始证据**：`ts/ts_0012/jobs/declaration_0001/ts_opt/refine.log`，sha256 **75f58eddb19c537e981949a6decf7df4ac3b4ab3b8a854dba625b08ea7fa7cb5**
- L24138 raw " SCF Done:  E(RB3LYP) =  -939.293671629     A.U. after    8 cycles"（L22374 -939.293669435、L23261 -939.293672375）
- L24507 " Optimization completed."；L24508 "    -- Stationary point found."；L25604 " Normal termination of Gaussian 16 at Sat Oct 17 09:08:23 2026."

**末帧几何**（format_converter 导出 `evidence/TS_B_job1013_last.xyz`，41 原子，元素序 = bound 序）实测：
- d(C1–C29) = **3.198 Å**（形成中的 C3–C6 未成键）；d(C1=C2) = 1.355 Å；d(C2–N4) = 1.388 Å；d(C28=O29) = 1.216 Å。
- 对照 924 末帧反应物：1.362 / 1.375 / 1.226 Å；生成物（E2 种子）：C1–C29 2.275、C2=N4 1.358、C1–C2 1.380。
⇒ 该驻点的电子结构仍是**烯胺 + 苯甲醛**（C=C、C=O 完好，C2–N4 为烯胺型单键），**不是**生成 C3–C6 的加成 TS。
其能量比 924 高 +0.014546634 Ha = **+9.13 kcal/mol**（纯电子能），但**不得**把它当 TS 能量、**不得**回填。

**原因**：通道 B 的 provided 种子 `build/TS_guess_EM1_j59f9.xyz`（d(C3–C6)=2.800 Å、C2–N4=1.388 Å）本身是**反应物侧**几何
（job_59 约束扫描帧），无约束 opt=(TS,calcfc,noeigen) 因此滑回反应物侧驻点。

**待 job 1021（frequency, ready）读数判定**：
- 0 虚频 ⇒ 极小值（非鞍点）；1 虚频但模不属于 C3–C6 ⇒ pseudo-saddle（issue #190 口径），均不得当 TS/回填。
- 恰 1 虚频且为 C3–C6 靠近模 ⇒ 仍需双向 IRC 确认是否真连 (S)-I1 与 M1。

**备选（等 1021 读数后报写权会话批准再提交，不抢跑）**：① 对通道 B 用 `guess.kind=scan` 沿 d(C1–C29)（1-based 原子对 [1,29]）做受约束/弛豫扫描取峰；
② 以通道 A 已验证 TS 为模板、绕 C1···C29 轴翻转苯甲醛进攻面（Re/Si）构造反对映面种子。
（通道 A 的 ts_opt job 1008 至 09:09 仍在跑。）

## 9 2026-10-17 09:3x 通道 B 第 1 次尝试：**未取得合格鞍点**（pseudo-saddle，逐项登记）

**run/job**：ts_0012 rev23，stage=refine，status=waiting，blocked=null，result.outcome=null。
- job **1013**（ts_opt）：`ts/ts_0012/jobs/declaration_0001/ts_opt/refine.log`（sha256 75f58eddb19c537e981949a6decf7df4ac3b4ab3b8a854dba625b08ea7fa7cb5），
  末次 L24138 " SCF Done:  E(RB3LYP) =  -939.293671629     A.U. after    8 cycles"；L24507 Optimization completed.；L25604 Normal termination 09:08:23。
- job **1021**（frequency）：`ts/ts_0012/jobs/declaration_0001/frequency/frequency.log`，sha256
  **a70f1e784e0a30d4598d68e45907bc0f520b6a571af0c4a2a9177c5e3834b54c**；39 个 `Frequencies --` 块 = **117 模 = 3N−6**；
  L1516 raw " Frequencies --    -27.9419                18.4738                33.3528" ⇒ **恰 1 个虚频 −27.9419 cm⁻¹**；L5319 " Normal termination of Gaussian 16 at Sat Oct 17 09:34:32 2026."
- **投影（log_parser, watch_pairs=[[1,29],[2,4],[1,2],[28,29]]）**：watch_pair_fraction = **0.000776（0.078%）**；
  分对 1–29 = 0.0322、2–4 = 0.0138、1–2 = 0.0029、28–29 = 0.0082；heavy_atom_fraction = **0.3221**；
  位移前几对 (12,24) 0.436、(4,41) 0.433、(18,24) 0.412 —— 由水/羧基 H 主导。

**判读 = pseudo-saddle（集体软模，H 主导），不是本步合格 TS**（按 issue #190：**不得回填**）。三条依据：
1) 虚频模对生成中的 C3–C6（work 原子对 1–29）的投影 ≈ 0.078%，位移不在成键方向；
2) heavy_atom_fraction 仅 0.32，位移前几对集中在水中 H / 羧基 H（原子 24 = 羧基 O，配 H 位移）的集体软模；
3) 几何本身不是成键鞍点：d(1,29) = 3.198 Å（未成键）、d(1,2) = 1.355（C=C 完好）、d(28,29) = 1.216（C=O 完好）、d(2,4) = 1.388（烯胺型），
   而能量已比 924 高 +0.014546634 Ha = **+9.13 kcal/mol**。
（候选 ΔE‡ = −939.293671629 − (−939.308218263) = +0.014546634 Ha = +9.13 kcal/mol，仅作 candidate_only 记录，不写入任何交付物。）

**IRC（job 1026，irc.gjf，state=ready）不得作为连通性证据**：它建立在上述已判不合格的驻点上，其"双向端点"不构成 (S)-I1 ↔ M1 的连通性证据。

**candidate_opt（job 1000 = −939.302926757，比 924 高 +3.32 kcal/mol）的判定（供主协调裁定 EM1 路线）**：
**同一物种的另一构象**——同物种证据：41 原子 C15H21NO4、3 分片、Cα(1-based 8)=S、仅 Cα 一个手性中心、连接性一致；
构象差异证据：d(1,29) = 7.293 Å（伸展）vs 924 的 4.316 Å（紧凑），水氢键网络不同（924：O10···H26 = 1.886 Å 水桥接羧基；伸展构象 5.986 Å），
Kabsch RMSD(41 原子) = 3.658 Å、最大单原子偏差 6.649 Å。⇒ 通道 B 的 provided 种子（job_59 链 2.800 Å 帧）落在**伸展构象**一侧，
其无约束 TS 优化滑回**反应物侧驻点**。后续 EM1 路线（受约束/弛豫扫描，或以通道 A 已验证 TS 为模板翻转苯甲醛进攻面）由主协调裁定后执行。

**通道 A（E2）不受影响**：ts_0009 rev33，ts_opt job 1008 仍在跑（09:37 检查），按验收链正常推进。

## 10 2026-10-17 10:1x 通道 B 第 2 次尝试种子：**已备、已批准、待 job 1026 终态提交**（非挂起；阻塞原因 = 平台并发保护，非资源裁定）

**裁定依据（两位协调者 2026-10-17 10:0x 一致）**：R36「本轮不再追加 TS 搜索/换 seed」只点名 **E1/E2/E3**，**EM1 不在其中**；EM1 通道 B 第 2 次尝试是更早已批授权，当前唯一阻塞是平台并发保护（ts_0012 上 job 1026 未终态 ⇒ 逐字 `ts_resume: active compute jobs prevent input revisions; use ts_inspect`，call_id tc_f74238b0861f47af，主协调已提 issue #194）。
写权会话先前按保守口径要求「本轮不提交」，主协调随即澄清「EM1 授权仍有效」⇒ 本条状态定稿为：**已批准、待 job 1026 终态立即提交**（不是挂起，也不因资源被撤）。

**种子档位 = ②（反对映面种子；机器构造，不含任何 QM 能量）**
- 待提交种子（绝对路径）：
  `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2EM1/build/TS_guess_EM1_j58f8_faceflip.xyz`
  sha256 **9f4d651aff4c75ef7ec9e582184c2581f4f22873d73b06b18e868cdd554ea10b**（41 原子，元素序与绑定 reactant 一致）
- 来源模板：`.../build/TS_guess_E2_j58f8.xyz` sha256 5024997e6eea53a91fa4b7ec4a92ab36916ca7c5f67deb0ef4263835c174cb40（取自原生日志 ORCA job_58 轨迹的 TS-like 帧并镜像到 (S)/通道-B 侧，d(C1–C29)=1.938 Å；**只用几何，不用其能量**）
- 构造方式（机器构造）：脚本 `.../build/make_flip_seed_lane3.py` sha256 ca89afd705d2d09aa1d3b08c38235b41a23c7a7d48caa4ebea444690596054ff —— 把苯环 C30–C35 与醛基 H36 关于 **C29/O28/C1 平面精确镜面反射**（不做坐标旋转），其余原子不动，元素序不改。
- 校验输出摘要（原始输出见 evidence/CHANNEL_B_RETRY_SEED_20261017.md）：RDKit CIP(1-based) 由 {(8,'S'),(29,'S')} → **{(8,'S'),(29,'R')}**（= 通道 B 要求：Cα=S、aldol 碳=R）；d(1,29) 1.937500 → 1.937500 Å（保持）；无新增短接触（minsep 0.972 Å 为既有 O–H 键）；element order unchanged = True。
- 已弃用中间件（**不得使用**）：`.../build/TS_guess_EM1_j58f8_flip.xyz` sha256 6625991c39131a33e5c716920ea6a75e60421d5416ed55f0e5d6a2c09fb9062a —— 绕 C29–O28 轴 180° 旋转只翻转了几何手性体积，RDKit 3D 感知仍报 (29,'S')。
- 拟用 `evidence_refs`（三份 provenance，sha256 已复核）：
  `.../evidence/CHANNEL_B_RETRY_SEED_20261017.md` = 9ec11790bc1c78189dbf33bd7bc573cb7369ec5924d42ece9785d5d37ae37010；
  `.../build/TS_SEED_PROVENANCE_EM1.md` = 73ee4aa81a4f31c120dbbd5dc9c41abe71164d7852f9d404fb4e297b26c3ec5b；
  `.../evidence/BINDING_AND_MAP_VERIFICATION_20261017.md` = 3432e7c19a685859ff37aef1140c1e4b293150c5e067066300c77bd981aea67a。
- **状态声明**：此刻该种子只是「待用件」，**不是任何结论的证据**，未经过任何 QM 计算；§9 末段「备选 ①/②（等批准再提交）」由本条取代。
- 提交载荷规划：`ts_resume(run_id='ts_0012')`，changes **只含 guess 组**（provided = 上述种子 + 三份 evidence_refs），不重声明 reaction_center / conformers / atom_map。

**阻塞作业读数（2026-10-17 10:07，工具回读）**：job **1026**（purpose=irc，input `ts/ts_0012/jobs/declaration_0001/irc/irc.gjf`）state=**running**，start_timestamp 1792202480.38（= **10:01:20**）；`irc/irc.log` 已 853 行，尚无 `Normal termination of Gaussian`；ts_0012 **rev23 / status=waiting / stage=refine**（waiting_for = 1026 irc running）。

**EM1 定稿口径（一句话，可直接引用）**：**EM1 = 缺测（未取得已验收一阶鞍点）+ 已证伪**（ts_0012 的 ts_opt 收敛但为 pseudo-saddle：恰 1 虚频 −27.9419 cm⁻¹、watch_pair_fraction 0.078%、H 主导软模、成键 C1–C29 = 3.198 Å；候选 ΔE‡ +9.13 kcal/mol 仅 candidate_only；job 1026 的 IRC 建在无效驻点上，不作连通性证据）。

**通道 A（E2）**：ts_0009 rev33，ts_opt job **1008** 在 10:07 仍在跑（`ts/ts_0009/jobs/declaration_0005/ts_opt/refine.log` 无 `Normal termination`；最后一次判据行 line 68393 raw " Maximum Force            0.001299     0.000450     NO "），外漂读数 d(1,29) 2.646 → 4.75 Å（67 步）。按 R36 裁定本轮**不补作业**，1008 终态后只登记终态判据与末帧几何。

## 11 2026-10-17 10:4x 通道 B 第 2 次尝试**已提交**（ts_0012 rev 26→27 / input rev 1→2，新作业 job 1032）

**触发（job 1026 IRC 失败，非鞍点上的 IRC）**：`ts/ts_0012/jobs/declaration_0001/irc/irc.log` sha256 **0670edd201ea6347ca9cbc202e61cdb8ae5e3856b241f8f7e51f03c601d19a0f**，13596 行；
- L13591 raw "   Delta-x Convergence NOT Met"；L13592 raw "Maximum number of corrector steps exceded."；L13593 raw "Error termination via Lnk1e in /home/ly/g16/l123.exe at Sat Oct 17 10:37:21 2026."（同 log 另有 9 处 Delta-x 未收敛：L8209 / L8815 / L9409 / L10015 / L10597 / L11203 / L11797 / L12403 / L12985）。
- 判读：该 IRC 建立在 §9 已判 **pseudo-saddle** 的驻点上，失败形态（Delta-x 反复不收敛 → l123 corrector 超限）与「虚频模 0.078% 投影、H 主导软模」一致；**其任何端点读数一律不作连通性证据**。

**ts_resume 回执（逐字）**
- request_key **tc_a8a157a2432141a7**；request_digest f6be0b42494dd8b8ae8c2c9fe253f8e65ea524cc2b449d2b974a1f448741ea62
- previous_revision **26** → revision **27**；previous_input_revision **1** → input_revision **2**
- changes = ["guess.evidence_refs","guess.xyz_path"]（**只含 guess 组**，未触碰 reaction / reaction_center / atom_map / conformers / calculations）
- retained = [{declaration_revision 1, stage_key "candidate_opt", attempt 1, job_id **1000**}]
- invalidated = [{1,"ts_opt",1,**1013**},{1,"frequency",1,**1021**},{1,"irc",1,**1026**}]
- status = **accepted**；ts_inspect(ts_0012) 顶层 readback：revision **33**、status=waiting、stage=refine、result=null

**新作业**：**job 1032**（purpose=ts_opt，state=ready，8 cpus / 10240 MB，input `ts/ts_0012/jobs/declaration_0002/ts_opt/refine.gjf`，source_input_revision=2）。

**绑定种子校验（本刻实测，非记忆值）**
- `ts/ts_0012/path/input_0002/provided.xyz` sha256 **9f4d651aff4c75ef7ec9e582184c2581f4f22873d73b06b18e868cdd554ea10b**（与 `…/build/TS_guess_EM1_j58f8_faceflip.xyz` **逐字节相同**），n=41，d(1,29)=**1.9375 Å**。
- `declaration_0002/ts_opt/refine.gjf`：41 原子，与种子坐标最大单原子偏差 **0.0000 Å**，d(1,29)=1.9375 Å，元素序同绑定 reactant（元素序列实测一致）。
- route 原文：`#p opt=(TS,calcfc,noeigen) B3LYP/def2SVP empiricaldispersion=gd3bj int(ultrafine) scf=tight scrf=(cpcm,solvent=dmso)`。

**下一步（门禁不变）**：1032 终态后先做 gjf 元素序 vs 末个 Standard orientation 元素序对比（索引安全），再取 117 模（band 表）、imaginary 行与波数、watch_pair_fraction / [1,29] 单对占比 / heavy_atom_fraction / 前 5 位移原子；虚频模必须由 [1,29] 主导，否则按 pseudo-saddle **只记证伪、不回填**（反例基线 −27.9419 cm⁻¹ / 0.078%）。ΔE‡ 恒以 job 924 = −939.308218263 Eh 为参考。

## 12 2026-10-17 12:0x 通道 B 第 2 次尝试 ts_opt（**job 1032**）收敛：几何为 C3–C6 成键型驻点；候选 ΔE‡ = +15.36 kcal/mol（仅 candidate_only，待频率门禁）

- log（绝对路径）：`/home/ly/Cloudra-mechanism-agent/ts/ts_0012/jobs/declaration_0002/ts_opt/refine.log`；sha256 **66691e0e68e9044d7d10e45e8953e6c5468efee3d361713d3e34d7bfbb2b4241**；25650 行。
- L24549 raw " Optimization completed."；L24550 raw "    -- Stationary point found."；L25650 raw " Normal termination of Gaussian 16 at Sat Oct 17 12:00:41 2026."；L24270 raw " Step number  25 out of a maximum of  239"；末次 SCF L24183 raw " SCF Done:  E(RB3LYP) =  -939.283734374     A.U. after    6 cycles"。
- 末帧几何：`format_converter(refine.log → evidence/TS_B_job1032_last.xyz)`（frame 24），41 原子，sha256 **663fe23166bb54de96c2698a43ae3d6207457be7b61d55a10a5972d8f29a3fce**；元素序 = gjf 元素序（索引安全已核：末个 Standard orientation 的 Center Number 严格 1..41 递增、原子序序列与 gjf 逐位相同）。
- 几何读数（1-based 绑定序号）：**d(1,29) = 1.879 Å**（C3–C6 正在形成）、d(1,2) = **1.429**（C1=C2 由 1.355 拉长）、d(2,4) = **1.328**（C2–N4 由 1.388 缩短）、d(28,29) = **1.292**（C=O 由 1.216 拉长）、d(1,3) = 2.461；C29 的最近重原子只有 O28 1.292 / C30 1.517 / **C1 1.879**（其余 ≥2.52）⇒ 无其它短接触。
- 候选能差（**candidate_only，不是验收值**）：E(1032) − E(924) = −939.283734374 − (−939.308218263) = **+0.024483889 Ha = +15.36 kcal/mol**（1 Eh = 627.5095 kcal/mol）。必须等频率门禁通过后才可作为 ΔE‡。
- 管线随后自动提交 frequency **job 1036**（input `jobs/declaration_0002/frequency/frequency.gjf`，12:00:41 起 running，8c/10240MB）；ts_0012 rev**37**、status=waiting、stage=refine。
- 下一步（门禁）：见 §11 末段口径 —— 117 模（band 表）→ imaginary 行与波数 → watch_pair_fraction / [1,29] 单对占比 / heavy_atom_fraction / 前 5 位移原子；虚频模非 [1,29] 主导即 pseudo-saddle(#190)，只记证伪不回填。

## 13 2026-10-17 12:0x 通道 A ts_opt **job 1008 终态**：收敛到**反应物侧松散驻点**（d(1,29)=5.118 Å），不是 C3–C6 加成 TS

- log（绝对路径）：`/home/ly/Cloudra-mechanism-agent/ts/ts_0009/jobs/declaration_0005/ts_opt/refine.log`；sha256 **9147c670be38bab077c3c93698abf7aa25549ba9355e491d0a24a7205c304f4c**；152453 行。
- L151370 raw " Optimization completed."；L151371 raw "    -- Stationary point found."；L152453 raw " Normal termination of Gaussian 16 at Sat Oct 17 12:04:35 2026."；L151365 raw " Maximum Force            0.000011     0.000450     YES"；L151092 raw " Step number 164 out of a maximum of  226"；末次 SCF L151004 raw " SCF Done:  E(RB3LYP) =  -939.304388002     A.U. after    6 cycles"。
- 末帧几何：`evidence/TS_A_job1008_last.xyz`（frame 163），41 原子，sha256 **e8a13808d70d288e7f78e8d3110f9a2a94821c04c759d7e21db7b6a4f3c40c85**；元素序 = gjf。
- 几何读数（1-based）：**d(1,29) = 5.118 Å**、d(1,2) = 1.357、d(2,4) = 1.381、d(28,29) = 1.221、d(1,3) = 2.496；C29 最近重原子 O28 1.221 / C30 1.471 / C31 2.480 / C35 2.504 / **C3 3.696** ⇒ C3–C6 完全未成键、烯胺 + 醛基未反应型。
- 候选能差（candidate_only）：E(1008) − E(924) = −939.304388002 − (−939.308218263) = **+0.003830261 Ha = +2.40 kcal/mol**。
- 判读：该 ts_opt 从 2.646 Å 一路**外漂**（4.75 Å @step67 → **5.118 Å** @step164）后停在反应物侧松散驻点；**不是** C3–C6 成键鞍点。它是否为一阶鞍点由管线自动提交的 frequency **job 1037**（`jobs/declaration_0005/frequency/frequency.gjf`，12:04:41 起 running）判定；若虚频模非 [1,29] 主导 ⇒ 与通道 B 第一次同类的 pseudo-saddle(#190)，只记证伪。
- 按 R36 裁定：**不补作业、不 ts_resume**；等 1037 读数后只登记。

## 14 2026-10-17 12:2x 通道 B frequency（**job 1036**）门禁：**通过** —— 117 模、恰 1 虚频 **−314.2861 cm⁻¹**，虚频模由 [1,29]（C3–C6）主导；管线 IRC job 1039 已起跑

- log（绝对路径）：`/home/ly/Cloudra-mechanism-agent/ts/ts_0012/jobs/declaration_0002/frequency/frequency.log`；sha256 **a471aa7b6c2b34b7ccff44a98bbcd0dee7c4ae5f436653fe79f094f44fe53a65**；5340 行；L5340 raw " Normal termination of Gaussian 16 at Sat Oct 17 12:19:43 2026."。
- 模数（只看 band 表）：39 个 `Frequencies --` 块 ⇒ **117 模 = 3N−6**（N=41）。
- 虚频：L1541 raw " ******    1 imaginary frequencies (negative Signs) ******"；L1550 raw " Frequencies --   -314.2861                33.5499                44.0361" ⇒ **恰 1 个虚频 −314.2861 cm⁻¹**（L1539 的 Low frequencies 行首 −314.2862 只是投影行，不作独立证据；L3479 " 1 imaginary frequencies ignored." 不是模数）。
- 索引安全：frequency.log 末个 Standard orientation（L474 起）Center Number 严格 1..41 递增，原子序序列与 `frequency.gjf` 元素序**逐位相同** ⇒ 1-based 原子号可用。
- 能量：L857 raw " SCF Done:  E(RB3LYP) =  -939.283734374     A.U. after   15 cycles" —— 与 ts_opt L24183 同值，确认频率作业就在同一驻点上（同批 Gaussian 16）。
- 虚频模投影（`log_parser(properties=['frequencies'], watch_pairs=[[1,29],[2,4],[2,1],[28,29]])`）：
  - **watch_pair_fraction = 0.024878（2.49%）**；分对 1–29 = **1.1094**、2–4 = 0.0700、1–2 = 0.1657、28–29 = 0.1770 ⇒ [1,29] 占被观注对的 **72.9%**，是**主导项**；
  - **heavy_atom_fraction = 0.6951**（重原子主导，非 H 软模）；
  - 位移前 5 对：(1,29) 1.1094、(13,29) 0.7866、(1,28) 0.6377、(15,29) 0.5921、(1,27) 0.5497。
- 对照反例基线（job 1021 pseudo-saddle）：watch_pair_fraction 0.000776（0.078%）、[1,29] 分对 0.0322、heavy_atom_fraction 0.3221、位移首位为水/羧基 H 对 (12,24) 0.436 ⇒ 本次与第 1 次**不同类**，是真正的 C3–C6 成键虚频模。
- **结论（仅就频率门禁）**：job 1032 的驻点通过「恰 1 虚频 + [1,29] 主导」检查；ΔE‡（同一驻点、同批）= −939.283734374 − (−939.308218263) = **+0.024483889 Ha = +15.36 kcal/mol**（15.3639）。**仍属候选**，须 IRC 双向连通性 + 两端 Opt+Freq(0 虚频) + CIP 核验后才可写入交付。
- 管线已自动提交 IRC **job 1039**（`jobs/declaration_0002/irc/irc.gjf`，12:19:46 起 running，8c/10240MB）；ts_0012 rev**41**、status=waiting、stage=refine。旧 job 1026 的 IRC 仍**不可**作连通性证据。

## 15 2026-10-17 12:2x 通道 A frequency（**job 1037**）门禁：**未通过** —— 恰 1 虚频但为 H 主导软模（pseudo-saddle，#190），C3–C6 未参与

- log（绝对路径）：`/home/ly/Cloudra-mechanism-agent/ts/ts_0009/jobs/declaration_0005/frequency/frequency.log`；sha256 **185d01fa41677507e672e29953892f8f11b92a839ac02bc6f5b3e8c9d1e114d4**；5316 行；L5316 raw " Normal termination of Gaussian 16 at Sat Oct 17 12:25:15 2026."。
- 模数：39 个 `Frequencies --` 块 ⇒ **117 模 = 3N−6**；虚频标记 L1507 raw " ******    1 imaginary frequencies (negative Signs) ******"；首个 band 行 L1516 raw " Frequencies --    -32.6774                15.9782                25.0955" ⇒ **恰 1 个虚频 −32.6774 cm⁻¹**（L1505 的 Low frequencies 行首 −32.7637 只是投影行）。
- 索引安全：末个 Standard orientation（L474 起）Center Number 1..41 递增、原子序序列与 `frequency.gjf` 元素序逐位相同。
- 能量：L819 raw " SCF Done:  E(RB3LYP) =  -939.304388002     A.U. after   13 cycles"（与 ts_opt L151004 同值）。
- 虚频模投影（watch_pairs=[[1,29],[2,4],[2,1],[28,29]]）：**watch_pair_fraction = 0.001854（0.19%）**；分对 1–29 = **0.0838**、2–4 = 0.0004、1–2 = 0.0070、28–29 = 0.0050；**heavy_atom_fraction = 0.2549**；位移前 5 对 (17,41) 0.3853、(18,41) 0.3643、(5,41) 0.3597、(12,37) 0.3450、(20,41) 0.3384（原子 37/41 为 H）。
- **判读 = pseudo-saddle（#190）**：与 job 1021（−27.9419 cm⁻¹ / 0.078% / heavy 0.3221）同类，虚频模由 H 位移主导、C3–C6（1–29）分对仅 0.0838；且 job 1008 末帧 d(1,29) = 5.118 Å（§13）本就说明该驻点不是成键鞍点。⇒ **通道 A 本轮未取得合格一阶鞍点**；按 R36 不补作业、不 ts_resume，只登记证伪。
- 通道 A 候选能差（不可作 ΔE‡）：−939.304388002 − (−939.308218263) = +0.003830261 Ha = +2.40 kcal/mol（松散反应物侧驻点）。
- 管线随后自动提交通道 A 的 IRC **job 1040**（`ts/ts_0009/jobs/declaration_0005/irc/irc.gjf`，start_timestamp 1792211117.98 = 12:25:18，running）；ts_0009 rev**41**、status=waiting、stage=refine。由于它建立在上述 pseudo-saddle 上，其端点读数与 job 1026 同性质：**只作失败/一致性登记，不作连通性证据**。
- job 1040 终态（13:02:47 读）：`/home/ly/Cloudra-mechanism-agent/ts/ts_0009/jobs/declaration_0005/irc/irc.log` sha256 **5479aa7945951dce0ef590cb0b4eca6864bf794b7c106098d56c7d22b9c71682**，13499 行；L13494 raw "   Delta-x Convergence NOT Met"、L13495 raw "Maximum number of corrector steps exceded."、L13496 raw "Error termination via Lnk1e in /home/ly/g16/l123.exe at Sat Oct 17 13:02:30 2026."（另有 L12306、L12888 两处 Delta-x 未收敛）⇒ **通道 A 的 IRC 亦失败**，与 job 1026 完全同型（建在 H 主导软模驻点上，IRC 无法收敛）。**不提供任何连通性证据**；通道 A 至此只有「未取得合格鞍点 + IRC 失败」两项证伪记录。

## 16 2026-10-17 13:2x 通道 B IRC（**job 1039**）**失败**（l123）：**双向连通性未取得**；ts_0012 已 blocked。频率门禁 + CIP 仍有效，ΔE‡ 保持 candidate

- log（绝对路径）：`/home/ly/Cloudra-mechanism-agent/ts/ts_0012/jobs/declaration_0002/irc/irc.log`；sha256 **dfc4d3ec2bba6c84e634eeb7105fb48fe0481969c7e61b73413fb2ed47ff31e3**；25169 行。
- L25164 raw "   Delta-x Convergence NOT Met"；L25165 raw "Maximum number of corrector steps exceded."；L25166 raw "Error termination via Lnk1e in /home/ly/g16/l123.exe at Sat Oct 17 13:25:23 2026."（另有 L19377–L24521 共 9 处 Delta-x 未收敛）。
- ts_inspect(ts_0012)：rev**44**、status=**blocked**、stage=refine；blocked.failure_class="job_failed"，原文要点 "refinement job 1039 (irc) ended as 'failed'; plain per-engine failure classes come from the log below — the run is stopped, not silently retried"；needs = ["verification.irc","execution","reaction.reaction_center"]；result=null。
- **IRC 轨迹（Input orientation 块逐点实测，1-based）**：
  - Path 1：Point 0 d(1,29)=**1.938**（起始）→ Point 1 1.998 → 2.058 → 2.117 → 2.174 → 2.230 → 2.284 → 2.338 → 2.389 → Point 9 **2.438**（C1=C2 1.370、C2–N4 1.364、C=O 1.235）⇒ 沿**断键方向**（回到反应物侧）走了 9 步，尚未到达 (S)-I1 极小。
  - Path 2：Point 1 d(1,29)=**1.765**、Point 2 **1.717**（C1=C2 1.455、C2–N4 1.318、C=O 1.319）⇒ 沿**成键方向**只走了 2 步，远未到 M1。
  - 此后 corrector 反复在两个近似构型间摆动（1.718 / 1.727 交替 20 余次），Bulirsch–Stoer "Delta-x Convergence NOT Met" → l123 终止。
- **结论（连通性）**：**双向连通性未取得**，两端 Opt+Freq 也因管线在 IRC 失败即停止而**未运行**。按 §9 替代口径（受约束单峰 + 端点身份 + 端点松弛）需要新作业，本轮**不做**（主协调已冻结交付、禁新增手工作业）。
- **仍有效的验收项（同批 Gaussian 16）**：
  1) 频率门禁：117 模、恰 1 虚频 **−314.2861 cm⁻¹**、虚频模由 [1,29] 主导（见 §14）。
  2) CIP（RDKit `rdDetermineBonds.DetermineBonds(charge=0, embedChiral=True)` + `AssignStereochemistryFrom3D` 于 `evidence/TS_B_job1032_last.xyz` sha256 **663fe231…**）：**(8,'S')、(29,'R')** ⇒ 符合通道 B 要求（Cα=S、aldol 碳=R）；同时感知到 1–29 单键、2=4 双键、28–29 单键（TS 处的产物侧键型分布）。
  3) 能量：E(TS) = −939.283734374 Eh（ts_opt L24183 与 frequency L857 一致）⇒ ΔE‡ = **+15.36 kcal/mol**（相对 job 924 = −939.308218263 Eh），**仍为 candidate_only**（缺连通性 + 端点证据）。
- **EM1 本轮最终状态**：**局部成功 + 连通性缺测** —— 已取得「频率合格的一阶鞍点候选 + CIP 正确 + ΔE‡ +15.36 kcal/mol」，但**缺**双向连通性与两端 Opt+Freq；不可回填为完整交付。

## 17 2026-10-17 13:3x 主协调裁定入档：EM1 本轮定性 = 「频率合格的一阶鞍点候选 + CIP 正确 + ΔE‡ +15.36（candidate_only），连通性与两端缺测」；**不授权任何新作业**

- 裁定：选 (a) 认作窗口外补录 + (c) 维持 11:20 CST 冻结交付；**不授权**替代口径新作业、**不授权**改 IRC corrector/步长或放宽约束；ts_0012 **保持 blocked、不 retry、不 ts_resume**；此后本 lane 只写 STATUS，除非出现新的非预期技术性失败。
- 理由（原文要点）：①交付已冻结，13:25 的 IRC 失败属窗口外事件；②本体系两次 IRC（job 1026、job 1039）均以 l123 corrector 失败，且 IRC 步长/算法在声明层无入口（issue #184）⇒ 受约束单峰 + 端点身份 + 端点松弛的替代口径需要**新轮次预算与新声明**；③不改方法层参数绕过失败。
- 入档验收现状（与报告正文一致，**不改盘**）：✅ 频率门禁（117 模、恰 1 虚频 −314.2861 cm⁻¹、[1,29] 占被观注对 72.9%、heavy 0.6951）；✅ CIP **(8,'S')/(29,'R')**；✅ E(TS) = −939.283734374 Eh、ΔE‡ = **+15.36 kcal/mol**（相对 job 924，同批同驻点）；❌ 双向连通性（job 1039 l123；job 1026 永不采用）；❌ 两端 Opt+Freq；❌ dDelta。⇒ EM1 仍 **result=null、未验收**，+15.36 只作 candidate_only（与终稿 §10.3 写法一致）。
- 通道 A 同轮结论（照录）：job 1008 松散驻点（d(1,29)=5.118 Å、+2.40 kcal/mol）；job 1037 虚频 −32.6774 cm⁻¹ 为 H 主导软模（watch_pair_fraction 0.001854、[1,29] 0.0838、heavy 0.2549）⇒ pseudo-saddle(#190)；IRC job 1040 亦 l123 ⇒ 通道 A 本轮无合格 TS、无 ΔE‡。
- **ts_0012 blocked 原文（留档）**：rev**44**、status=**blocked**、stage=refine；blocked.failure_class = `job_failed`；message = `refinement job 1039 (irc) ended as 'failed'; plain per-engine failure classes come from the log below — the run is stopped, not silently retried`；needs = `["verification.irc","execution","reaction.reaction_center"]`；result = null。**保持 blocked，不 retry、不 ts_resume。**
- 新轮次建议（非本轮承诺）：先建立连通性替代口径的方法学（受约束单峰 + 端点 Opt+Freq 0 虚频 + 身份/CIP），或按 issue #184 向平台索取 IRC 步长/算法入口，再把 +15.36 升为 ΔE‡。

## 18 2026-10-17 14:0x 任务转换：旁观组分（苯甲酸/苯甲酸根）作废 → 执行 EM1 **替代口径连通性**（受约束弛豫扫描，job 1049 已起）
- 上游裁定：苯甲酸、苯甲酸根两项**作废**（前提错误）；苯甲醛由 lane1 **job 1045** 覆盖，**我未提交**（我 13:57 生成的输入件 `spectator/benzaldehyde_optfreq.gjf` sha256 **676d3e8f…** 留作备份，从未提交）。
- **我的独立核实（支持前提错误结论）**：`HI1/verify/E3_ts0011_freq1029_geom_from_log.xyz`（sha256 62eea585…，另 job999 末帧同构）= **41 原子 C15H21NO4**；芳环侧 C30–C35 环（1.40 Å）+ H37–H41、C30–**C29 1.512**、**C29–O28 1.404**、**O28–H24 0.984**（羟基）、C29–H36 1.100、**C29–C1 1.587**（加合物键）；**唯一羧基在吡咯烷 C9**（O10 1.254 / O11 1.250 = COO⁻）；另 O25 = 水（H26 0.969/H27 0.994）⇒ 芳环片段是 **Ph–CH(OH)–**，帧内**不存在 C7H6O2**。
- **新任务输入（起点 = job 1032 ts_opt 末帧）**：`evidence/TS_B_job1032_last.xyz` sha256 **663fe231…**（d(1,29)=1.879 Å）。
  - `spectator/scan_down_c1c29.gjf` sha256 **ff001abea410204b45f3f35eb9a7a4aedd5391f200ded3fb31293444f74caac8**，扫描行 `B 1 29 S 11 -0.050`（1.879 → 1.329 Å）。
  - `spectator/scan_up_c1c29.gjf` sha256 **d7545a6e51a4d02fb96c93d2fa3a7637a1bc12e4b734a4084ab335e14afe6d01**，扫描行 `B 1 29 S 14 0.050`（1.879 → 2.579 Å）。
  - 两条 route 均 `#p opt=modredundant B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=DMSO)`，%nproc=8 / %mem=10240MB，q0/m1。
- **已提交作业 1049**（scan down，state=ready，job_dir `…/HI1/E2EM1/spectator`）；上扫等待空槽（全局仅 1 空槽）。端点 Opt+Freq 待槽位。
- **平台限制记录**：`qm_input_writer` 拒绝生成 relaxed scan，逐字返回 "qm_input_writer refused: a Gaussian 'scan' task writes the bare `scan` route, which is a RIGID potential-surface scan. RELAXED scans use structured scan_prepare coordinates."；故两份 .gjf 由脚本**逐行复制** job 1032 末帧坐标（未改动任何数值，元素序=gjf 序）生成，sha256 已登记。
- **措辞纪律**：补齐后只能写「verified（替代口径：无 IRC）」，**不得**写「IRC 已双向到达端点」；job 1026 的失败 IRC 永不作连通性证据；补齐前 **+15.36 kcal/mol 保持 candidate_only**，ΔE‡ 分母固定 job 924 = −939.308218263（log `runs/I1_optfreq/I1_S_optfreq.log` sha256 6ecf0623…，L20025/L22238）。

## 19 2026-10-17 19:1x 通道 B 下扫 **job 1049 失败**：逐点能量**非单调**（1.6791 Å 处比 TS 低 0.27 kcal/mol）且第 9 点约束失效 ⇒ 1D 受约束扫描不能作为连通性替代口径

- log（绝对路径）：`/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2EM1/spectator/scan_down_c1c29.log`；sha256 **e269ece2283eefd2434dcbb21df17238d28acff7da6d5ff5dc06ebdc4be0dc5e**；275858 行。
- 失败原文：L274784 raw " Optimization stopped."；L274785 raw "   -- Number of steps exceeded,  NStep= 246"；L275854 raw " Error termination request processed by link 9999."；L275855 raw " Error termination via Lnk1e in /home/ly/g16/l9999.exe at Sat Oct 17 19:16:53 2026."（Gaussian 在 l9999 前的固定文本 "PERICLES, SOPHOCLES, ... H2SO4." 亦出现）。
- **逐点表**（受约束点在每个扫描点的末次 SCF；能量为同批 RB3LYP/def2SVP 电子能，ΔE 相对 job 1032 TS = −939.283734374）：

| 点 | R(1,29)/Å | E/Eh | 行号 | ΔE vs TS |
|---|---|---|---|---|
| 1 | 1.8291 | −939.283546038 | L2844 | +0.12 |
| 2 | 1.7791 | −939.283825209 | L16141 | −0.06 |
| 3 | 1.7291 | −939.284104954 | L21921 | −0.23 |
| 4 | **1.6791** | **−939.284170099** | L25891 | **−0.27**（沿该坐标的极小） |
| 5 | 1.6291 | −939.283742777 | L33508 | −0.01 |
| 6 | 1.5791 | −939.282461186 | L38379 | +0.80 |
| 7 | 1.5291 | −939.279871188 | L42392 | +2.42 |
| 8 | 1.4791 | −939.275406184 | L46407 | +5.23 |
| 9 | 目标 1.4291，实际停在 **1.4791** | −939.275014642 | L274426 | +5.47 |

- **两点判读**：
  1) **非单调 ⇒ 单峰判据不成立**：沿 R(1,29) 从 TS 的 1.8791 收紧，受约束能量在 **1.6791 Å 处比 TS 低 0.27 kcal/mol**，因此 **TS 在 R(1,29) 上不是极大**；并集「单一极大 + 两侧单调」在产物侧已被否证（与 up-scan 无关）。
  2) **约束失效（job 962 先例）**：第 9 点目标 1.4291 Å 但末帧 R 仍为 1.4791（= 第 8 点值），L274796 raw " ! R4    R(1,29)                 1.4791         -DE/DX =    0.0557              !"，NStep 达 246 上限 ⇒ l9999 终止。**末帧 d(1,29)=1.4791**。
- **按裁定处置**：判失败、**不重扫、不改步长**；1D 受约束扫描（刚性 C1–C29）**不足以**充当连通性替代口径 —— 该虚频模含 C1–C29 伸缩 + 桥接水/甲基 H 协同，单坐标约束把体系推到别的方向。
- **连带影响**：拟定「产物端种子 = 1049 外端帧（1.329 Å）」**不存在**（扫描最远只到 1.4791 Å）。产物端 Opt+Freq 的种子需写权会话重新裁定（候选：历史 ORCA job_58 产物侧帧 d=1.600 Å，仅几何；或第 8 点帧 1.4791 Å 松弛；或本轮不跑）。
- **EM1 状态不变**：**candidate_only、result=null**；+15.36 kcal/mol 不得作为 ΔE‡ 写入；四项升格条件（并集单峰 / 两端 0 虚频 / 端点身份 / 端点松弛）现缺「并集单峰」这一项。
- **扫描起点数字澄清（写权会话 19:2x 要求，逐项实测）**：① 驻点自身 R(1,29) = **1.8791 Å**（`ts/ts_0012/jobs/declaration_0002/ts_opt/refine.log`（sha256 66691e0e…）**最后一个 Input orientation 在 L24793**，41 原子实算）；② 扫描初始约束值 = **1.8791 Å**（本扫描 log **L237** raw " ! R4    R(1,29)                 1.8791         Scan                            !"），与该驻点一致（差 **0.0000 Å**）；③ 第一个扫描点 pt1 实算 R = **1.8291 Å**（本扫描 log **L2283** 的 Input orientation 实算），即 pt1 不是驻点、已内移 **0.0500 Å**；④ 剖面起点能量 = 驻点能量 **−939.283734374 Eh**（本扫描 log **L1116**，即初始几何上的第一次 SCF），pt1 能量 −939.283546038 Eh（L2844）。⇒ 正文「由 1.8791 收紧」与表 pt1 = 1.8291 并不矛盾：1.8791 是起点/驻点，1.8291 是第一个受约束点。
- **判据措辞定稿（写权会话给定）**：「沿 R(1,29) 的受约束剖面在 1.6791 Å 处比该驻点低 0.27 kcal/mol；受约束点能量是真实能量的上界，故真实能量只会更低 ⇒ 该驻点沿此坐标不是极大；单峰判据在产物侧被否证（下界论证，非仅观察）」。
- **裁定登记（写权会话 19:2x）**：(c) 本轮**不跑**产物端 Opt+Freq（理由：判据已不可能过关 / 产物身份由频率验证的 P（job 1061）覆盖 / 交付已 partial 冻结 / ORCA 1.600 Å 帧跨引擎身份问题 / 第 8 点帧信息量同 P）；(b) **up-scan 不跑**（并集为全称条件，一侧否证即不成立；槽位留给 1069/1071）。未提交任何作业。

## 20 2026-10-17 19:3x **post-freeze asset / non-delivery evidence**：EM1 候选驻点虚模（−314.2861 cm⁻¹）的可复核分解表（零算力、只读）

- 来源：`/home/ly/Cloudra-mechanism-agent/ts/ts_0012/jobs/declaration_0002/frequency/frequency.log`；sha256 **a471aa7b6c2b34b7ccff44a98bbcd0dee7c4ae5f436653fe79f094f44fe53a65**；5340 行。
  首个 band 行 **L1550** raw " Frequencies --   -314.2861                33.5499                44.0361"；模矢表头 **L1554** " Atom  AN      X      Y      Z ..."；**模 1 的 41 行位移表 = L1555–L1595**（脚本按每行 11 字段解析：Atom, AN, 3 个模 × 3 分量）。
- **归一化口径（两条都报）**：① **未加权**：对全部 3N = 123 个笛卡尔分量归一，实测 Σ|d|²（41 原子求和）= **1.004900**（≈1，与 Gaussian 打印的归一化一致）；② **质量加权**：Σ mᵢ|dᵢ|²（m: C 12.011 / N 14.007 / O 15.999 / H 1.008）归一。下表两列并列，避免口径歧义。

| 分组（1-based 原子） | 原子数 | Σ|d|² | 未加权占比 | 质量加权占比 |
|---|---|---|---|---|
| **[1,29] 两原子合计** | 2 | 0.619200 | **61.62 %** | **84.39 %** |
| 其中 原子 1 (C1) | 1 | 0.329800 | 32.82 % | 44.95 % |
| 其中 原子 29 (C29) | 1 | 0.289400 | 28.80 % | 39.44 % |
| 桥接水 O25/H26/H27 | 3 | 0.047100 | 4.69 % | 1.24 % |
| 甲基 H（C3 上的 H14/H15/H16） | 3 | 0.096400 | 9.59 % | 1.10 % |
| 其余重原子（合并项） | 17 | 0.075200 | 7.48 % | 11.36 % |
| 其余 H（合并项） | 16 | 0.167000 | 16.62 % | 1.91 % |

- 位移最大的 8 个原子（未加权占比）：**C1 32.82 %、C29 28.80 %、H13 9.74 %**、H15 5.04 %、H14 3.42 %、C2 2.50 %、H26 2.44 %、O28 2.21 %。
- **观察（只写观察）**：该虚模是 **C1–C29 伸缩主导**（[1,29] 合计未加权 61.6 % / 质量加权 84.4 %），并伴随 **C1 上的 H13（9.7 %）与 C3 甲基 H（合计 9.6 %）的再杂化位移**；**桥接水贡献仅 4.7 %**（H26 单原子 2.4 %）⇒ **不构成质子转移主导的协同模**。因此 [1,29] 单坐标可代表该模的 **约 62 %（未加权）/ 84 %（质量加权）**，剩余 ~38 % / ~16 % 落在 H 与骨架弛豫上 —— 这与 §19 中「单坐标刚约束不足以表达反应坐标」的判读一致。
- **性质声明**：本条为 **post-freeze asset / non-delivery evidence**，不改变 EM1 的 **candidate_only / result=null**，不进入任何 ΔE‡ 计算。

## 21 2026-10-17 19:3x **post-freeze asset / non-delivery evidence**：扫描第 4 点 vs 候选驻点 = **同一物种**（无 H 迁移、无键变），并因此修正「2D + 质子转移」的解释

- 比较对象：**pt4**（下扫第 4 点，R(1,29)=1.6791 Å，E=−939.284170099，末帧几何 `spectator/scan_down_c1c29.log` **L25341**）vs **候选驻点**（`ts/ts_0012/jobs/declaration_0002/ts_opt/refine.log`（sha256 66691e0e…）**末帧几何 L24793**，R(1,29)=1.8791 Å）。两帧均 41 原子、元素序相同。
- 逐项实算（Å）：

| 指标 | pt4 (L25341) | 驻点 (L24793) |
|---|---|---|
| C1–C29 [1,29] | **1.679** | **1.879** |
| C1–H13 [1,13] | 1.095 | 1.093 |
| C1–C2 [1,2] | 1.454 | 1.429 |
| C2–N4 [2,4] | 1.319 | 1.328 |
| C29–O28 [29,28] | 1.320 | 1.292 |
| C2···O28 [2,28] | 2.902 | 2.977 |
| O25–H26 / O25–H27（桥接水） | 0.969 / 1.000 | 0.970 / 0.993 |
| C1–C3 [1,3] | 2.471 | 2.461 |

- **H13 的最近重原子**：pt4 = C1 1.095 / C2 2.163 / C29 2.265；驻点 = C1 1.093 / C2 2.166 / C29 2.420。对杂原子 **O25 4.363 / O28 3.394 / N4 2.668**（驻点 4.406 / 3.450 / 2.686）⇒ **H13 始终是 C1 上的 C–H，未发生任何质子转移**。甲基 H 亦然（H14 最近 O28 1.946 Å 为既有 C3–H 几何邻近，H15/H16 最近均为 C2）。
- **重原子 Kabsch RMSD（20 个重原子，去整体转动）= 0.057 Å**；最大单原子偏差 **0.110 Å** ⇒ 骨架几乎不动，唯一显著变化是 C1–C29 由 1.879 缩到 1.679 Å。
- **几何感知键表差异（RDKit `rdDetermineBonds(charge=0)`，两帧同法）**：**「仅 pt4 有」= 空、「仅驻点有」= 空** ⇒ 41 原子的**键表完全相同，无成键/断键**。
- **逐点趋势（同一物种在整段上的连续演化）**：R(1,29) 1.8291→1.4791 各点 C1–H13 = 1.093/1.093/1.094/1.095/1.095/1.096/1.097/1.098/1.099；H13···O25 = 4.406→4.316；H13···O28 = 3.450→3.320；H13···N4 = 2.686→2.632 —— 全部**单调微变**，无跳变。
- **判定（观察层）**：**同一物种**（same species）；无 H 迁移、无键变，只有 C1–C29 距离变化 + 骨架 ≤0.11 Å 弛豫。
- **由此修正两处解释（不改变否证结论）**：
  1) 「需要 2D（C1–C29 + 水质子转移）」**不成立**：桥接水仅占该虚模 4.7 %、H13 距 O25 达 4.36 Å，模内不存在质子转移通道；若将来做 2D，第二坐标应取 **H13 / C3 甲基 H 再杂化**相关坐标。
  2) 但「驻点沿 R(1,29) 不是极大」**不变**，且**不能**再用「中段换了物种」解释（本条已排除）：1.6791 Å 处受约束能量比驻点低 0.27 kcal/mol 是该**曲线约束路径**本身的特征（受约束点是真实能量上界），而非物种变化。
- **性质声明**：**post-freeze asset / non-delivery evidence**；不改变 EM1 的 candidate_only / result=null，不进入任何 ΔE‡ 计算。

## 22 2026-10-17 19:2x **定档改写（覆盖 §19 与 §21 的结论句，写权会话给定）**

- **否证对象 = 1D 坐标 C1–C29，而不是驻点本身**：沿 R(1,29) 的受约束剖面为「浅峰 ≈1.82 Å（+0.12 kcal/mol）+ 阱 1.679 Å（−0.27 kcal/mol）」，极大**不在**驻点（R=1.8791 Å）处 ⇒ **C1–C29 不是该驻点的反应坐标**；因此它既不能代表该虚模（质量加权仅 84.4 %，残余 15.6 % 落在其他方向，见 §20），也不能用于「并集单峰」判据。
- **驻点本身未被否证**：其频率仍为 **117 模、恰 1 个虚频 −314.2861 cm⁻¹**（frequency.log sha256 a471aa7b…，L1550）；EM1 缺的是**连通性**与**端点**，不是驻点性。
- **故 §19 末段「单峰判据在产物侧被否证」与 §21「不能用换物种解释」两句，按本条口径读**：否证的是坐标选择，不是鞍点存在性；§20/§21 的数值与观察全部保持有效。
- **下一窗口建议（仅供参考，授权在主协调，本条不含任何提交）**：放弃 1D/2D 扫描路线，改为从该驻点做**双向 IRC 并显式给足 maxpoints**（E3a 的 irc 曾用默认 maxpoints=10 被截断，属前车之鉴）；IRC 无需预先猜反应坐标，是唯一能在不猜坐标前提下补齐连通性与端点证据的路径。**我未做准备性提交。**
- **性质声明**：post-freeze asset / non-delivery evidence；EM1 维持 candidate_only / result=null；13.36 / 15.36 / 15.52 均不作 ΔE‡。


- **写权会话 14:1x 追加边界（逐条遵守）**：① 该 standalone 扫描**不是** ts_prepare 管理的证据、**不得**当 IRC；② 只有「双向都扫 + 单调单峰 + 两端 Opt+Freq 0 虚频 + 端点身份核对」齐备才可写「**verified（替代口径：无 IRC）**」；③ job 1026 的失败 IRC 永不作连通性证据；④ +15.36 保持 candidate_only，ΔE‡ 分母固定 job 924；⑤ **上扫 `scan_up_c1c29.gjf`（sha d7545a6e…）暂不提交**，等 1049 出结果后由写权会话排槽；⑥ 若 1049 逐点能量**非单调/双峰** ⇒ 直接判失败并如实登记（不重扫、不改步长再试），并把逐点能量表交出。









