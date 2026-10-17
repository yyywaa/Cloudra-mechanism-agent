# HI1 包计划 · 2026-10-15（包 Coordinator）

工作根目录：`/home/ly/Cloudra-mechanism-agent`
本包目录：`gold_finish_20261015/HI1/`

## 1 目标（不扩大范围）

关闭 hard 题 HI1 的两条缺口边并回填标答；除此之外**不改任何题源、不改图、不动别的包**。

| 边 | 声明内容（题源） | 现状 |
|---|---|---|
| HI1_E1 | 脯氨酸烯胺缩合，**合并边**：脯氨酸 N20 进攻丙酮羰基 C2 → 断 C2=O4、断 N20–H21、断 C3–H22，成 C2–N20 与 C2=C3 π，两质子经羧基接力转到离去的 O4 成水 → 烯胺 + 水（carbinolamine/亚胺不单独成节点） | barrier=null；历史把“第一子步 carbinolamine”结果回填整体边被否；旧 19.2 作废 |
| HI1_E3 | iminium-aldolate 水解：水 O4 进攻亚胺 C2 → 成 C2=O4，断 C2–N20，断 O4–H21/O4–H22，成 N20–H21（脯氨酸再生）、成 O5–H22（醇盐质子化）→ (S)-aldol + (S)-脯氨酸 | barrier=null；历史 114–120 链有 1 虚频 −658.38 cm⁻¹、两端零虚频（−938.741308 / −938.761777 Ha），判 candidate_only；旧 16.9/19.2 作废 |

题面条件：DMSO、电荷 0、单重态，催化剂中心（map16）**全程 S**。
题源：`cloudra/benchmark/hard_registry/hi.py`（I1 条目）、`ideapool/tasks/hard/HI1.json`、`ideapool/reaction_candidates/hard.md` 的 I1 行。

HI1.json 中 HI1_E1 的 bond_changes（1-based map 号）：
- break `[[2,4],[3,22],[20,21]]`；form `[[2,3],[2,20],[4,21],[4,22]]`
HI1_E3 的 bond_changes：break `[[2,20],[4,21],[4,22]]`；form `[[2,4],[20,21],[5,22]]`

## 2 引擎与口径（BRIEF §3）

- 本机无 ORCA；统一 **Gaussian 16（`/home/ly/g16/g16`）**：
  `B3LYP/def2SVP` + `EmpiricalDispersion=GD3BJ` + `Int(UltraFine)` + `SCF=Tight` + `SCRF=(CPCM,Solvent=DMSO)`，q0 / m1。
  报告里必须写“computed_by_us=True + 方法与引擎一句”。
- TS/IRC 只能走 **ts_prepare / ts_resume**（手工 TS/IRC 提交被禁用）；引擎声明用 gaussian。
- **同程序能量才可相减**：一条边的 TS/端点/起点极小值必须全部来自本包本批 Gaussian 作业；旧 ORCA 数值（含 −938.xxx）**只能作几何起点/身份参考，绝不相减**。
- 能垒 = 纯电子能差（无 ZPE/热校正），相对**该步自身起点的极小值**。E1 起点 = 反应物复合物 RC（脯氨酸+丙酮+苯甲醛，41 原子）；E3 起点 = HI1_I2 极小值。

## 3 可复用的本地几何起点（只作起点，先核身份）

| 文件（绝对路径） | sha256 | 内容 |
|---|---|---|
| `/home/ly/Cloudra-mechanism-agent/gold_compute/grant_materials_20261001/raw/HI1/job_51/rc_clean_np8.xyz` | `5b7b7aa2df9466c456614c9af3ddfe4e264339fd1b39a2dadd58690fb5f9b594` | 41 原子，ORCA job51 = 烯胺 + 水 + 苯甲醛（= HI1_I1 物种），E=−938.760019066499 Ha（旧值，参考） |
| `.../job_64/ts2_np8.xyz` | `26b53f25a511c050fe71d6fb566fb74b995de9465655f159ec0e90ece3b1031b` | 41 原子，ORCA major-face C–C 加成 TS 几何（= HI1_TS2 近似） |
| `.../job_52/rc_shared_opt.xyz` | `460aa78fde5def3d42741f0c6ad6b6b47ec5c7e29edeeb4ce1bae87931ba5f8d` | 41 原子，烯胺+水+苯甲醛另一构象（同物种） |
| `.../job_54/minor_rc_opt.xyz` | `1bed5958e8826676044a1b83d256542b5ad93641f02e120d0b7791e1864ebdb8` | 41 原子，副面预复合物（同物种） |

**⚠ 2026-10-15 独立审计新增事实（必须遵守）**：上表四个几何经本地 3D 手性核验，**脯氨酸中心全部是 R**（job_51/52/54/64 的 Cα 手性三重积 T≈−8.39…−8.48），而题源要求 **map16 全程 S**（10-01 声明图快照写 `[C@@H]`=R，现行 HI1.json 写 `[C@H]`=S，差异即 10-14 那次纠正）。
→ 这四条几何**只能当骨架/构象起点**；直接作为 RC/I1/I2/TS 种子会把 R-脯氨酸静默带进作业。任何沿用它构建的物种，必须在 Opt/Freq 之后对**实际几何**实测 CIP（map16=S；I2/P 的 aldol 碳 map6 目标 S），并在证据里给出 map↔本地原子序号对照。

**历史几何本地缺失（已用真实 ls/find 核过）**：`gold_compute/remote_backups/` 不在本机，job 82 的 I2（`em1_epF_optfreq.xyz`，原 sha `a618fd1dcebb32b536c7fbb63a18e2fa8ccebb9538dd437bf9dd8c63583af10f`）、job 71/72/83 端点、E1 的 94/100/102 产物**都不在本地**。因此：
- E3 起点必须**从题源重建**（题源 HI1_I2 SMILES），并在证据里显式写明与历史起点的差异（历史 job82 为 ORCA 几何、C8R/R-脯氨酸；本包按 10-14 纠正后的题源用 (S)-脯氨酸 map16）；
- 不得改用 RC51 充当 I2（RC51 是烯胺+水+苯甲醛 = I1 物种）。

## 4 验收链（缺一项即未通过）

1. TS 恰好 1 个虚频，且该虚频模以声明的成键/断键原子对为主；
2. IRC **双向**真实到达声明的两个端点（方向区间证据，不强求跑到 native 上限）；
3. 两端点 Opt+Freq = 0 虚频极小值，且物种/质子位置/立体身份（CIP）核验通过（E1 还要核 H21/H22 归属：两端各在哪个原子上；E3 要核 O4/O5/N20 与 C2/C6 立体，尤其历史拒收提到的“产物立体/atom 27 问题”对应到我们工作原子序号的哪个原子）；
4. 能垒 = 纯电子能差，相对该步自身起点极小值；
5. 原生日志不改写，记录绝对路径 + sha256，能量取自日志原始行；
6. 写回题源 → 重新生成题面 → 守卫测试通过（由包 Coordinator 执行，子代理不要改 hi.py / HI1.json / hard.md）。

## 5 资源与 QM lane 互斥（硬约束，2026-10-15 巡检 1 更新）

- **每包最多 2 个并发 Gaussian 作业**（新提交优先 **8 cpus / ≤10 GB**，确有需要才 12c；硬上限仍 ≤12 cpus / ≤14000 MB）。
- 本包现有 **3 条道**（lane1=E1、lane2=E3、lane3=E2/EM1 的 (S) 重算）共用 **2 个槽位**：见 `qm_slots/README.md`。提交任何 Gaussian（含 ts_prepare/ts_resume 自动作业）前先 `mkdir qm_slots/slot1`，失败再试 `slot2`，两个都失败就不提交（等或先做非 QM 准备）；整条 run 结束（terminal/blocked/idle）后立刻 `rmdir` 释放。
- `qm_lane/` 仅作历史记录，不再是锁。
- lane 令牌目录：`/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/qm_lane/`
  - 提交任何 Gaussian（含 ts_prepare/ts_resume 触发的自动作业）**之前**先 `mkdir` 该目录（原子操作）；失败=别人持有，等；跑完（run 进入 terminal/blocked）后 `rmdir` 释放。
  - 只在 lane 里写 `holder.txt`（谁 + 时间 + run_id）。陈旧判定：持有 >120 min 且无 g16 进程 → 可破锁，但必须记录破锁证据。
- 提交前做防撞双查（`query_compute_queue` + 运行进程）；排队时不要重复提交、不调 priority、不杀别人作业。
- 不设非原生 MaxIter/MaxSteps/超时。xtb（GFN2/ALPB-DMSO）只允许用于几何准备，不能作能垒证据。

## 6 输出与汇报

- 每条边在自己的目录留：`STATUS.md`（一行终态）、`evidence/` 清单（日志绝对路径 + sha256）、run 目录。
- 结论同时写 hub 主题 `gold-finish-20261015`（`to_agent=coordinator`）。
- 合格值 → 交给包 Coordinator 回填 hi.py / HI1.json；缺测 → 写清“缺什么 + 已证伪什么 + 待裁决问题”，不得填 0、不得擅自改图。
