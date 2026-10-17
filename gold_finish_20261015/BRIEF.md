# gold 缺口收口战役 · 2026-10-15（主协调：Coordinator as_current）

> 本文件是本次战役所有包 Coordinator 的共享前置事实与方法约束。**先读它，再读自己包的任务书。**
> 工作根目录（绝对路径）：`/home/ly/Cloudra-mechanism-agent`

## 1 目标（用户指令：快点把标答算完）

把题库里 **9 条"无参考值且无豁免记录"的 gold 边**算成合格标答并回填题源：

| tier | task | edge | 步骤 | 溶剂 / 电荷 / 重数 |
|---|---|---|---|---|
| hard | HI1 | HI1_E1 | 脯氨酸烯胺缩合（题源是"合并边"，历史上有拆步争议） | CPCM(DMSO) / 0 / 1 |
| hard | HI1 | HI1_E3 | iminium-aldolate 水解 | CPCM(DMSO) / 0 / 1 |
| hard | HL1 | HL1_E1 | Beckmann：肟 O-质子化（历史证据指向 N 侧） | 气相 / +1 / 1 |
| normal | NI5 | NI5_E1 | 水溶液亚胺形成：C–N 加成 | CPCM(Water) / 0 / 1 |
| normal | NR1 | NR1_E1 | 频哪醇 OH 质子化 | 气相 / +1 / 1 |
| normal | NR1 | NR1_E2 | 质子化频哪醇脱水 | 气相 / +1 / 1 |
| normal | NY3 | NY3_E1 | Na⁺ 中性模型：OH⁻ 加成 | CPCM(Water) / 0 / 1 |
| normal | NY3 | NY3_E2 | Na⁺ 中性模型：甲氧基消除 | CPCM(Water) / 0 / 1 |
| normal | NY3 | NY3_E3 | Na⁺ 中性模型：甲酸→甲氧基 PT | CPCM(Water) / 0 / 1 |

**不要动**其余边：2 条 PT 豁免（NB1_E2、NQ5_E2）、8 条 impossible 档 TS 不可达边、4 条性质/态变化边。

## 2 已确认的前置事实（不要重复劳动）

- 全库 52 题 / 81 边，58 边已有数值（重算于 2026-10-15）。
- 独立审计：`gold_compute/library_audit_20261002/README.md` + `open_edges.csv`（10 条缺口来源与依据）。
- 逐边历史交接（**必读**）：`gold_compute/supplement_20261002/HANDOFF_UNFINISHED_20261004.md`——含每条边旧尝试、已封顶路线、可复用产物、失败原因。
- 10-05 本地链：`gold_compute/supplement_20261002/LOCAL_RUN_20261005.md`（NU5_E2 已关闭 = 1.5440；NR1 作业 112 实为"质子化频哪醇＋水"，不能当 E1 起点）。
- 旧值一律作废，**不得回填**：HI1_E1 19.2、HI1_E3 16.9、NY3 15.5/12.5/0.0、NR1 0、HL1 0。
- 题源 md（历史锚点与已裁决记录）：`ideapool/reaction_candidates/hard.md`、`ideapool/reaction_candidates/normal.md`。

## 3 引擎现实与口径（重要偏差，必须如实记录）

- 既定口径是 **ORCA 6.1.1 B3LYP-D3(BJ)/def2-SVP（RIJCOSX、def2/J、TightSCF）**。
- **本机没有 ORCA**（`which orca` 为空；PATH 里只有 xtb-6.5.0 与 Gaussian 16）。因此本战役统一改用
  **Gaussian 16（`/home/ly/g16/g16`）**：`B3LYP/def2SVP` + `EmpiricalDispersion=GD3BJ` + `Int(UltraFine)` + `SCF=Tight`，
  溶剂按上表用 `SCRF=(CPCM,Solvent=...)`（HL1/NR1 为气相，不写 SCRF）。
  这保持"泛函＋基组＋色散＋溶剂模型"与既有 gold 同级；程序差异必须在证据里显式写出。
- **同一程序的能量差才能相减**：一条边的 TS/端点/参考极小值必须全部来自 Gaussian 16 同一批作业；**不得**与旧 ORCA/Gaussian 数值混减，不得把扫描峰或未收敛点当能垒。
- 报告里 `computed_by_us=True` 必须附一句方法与引擎说明。

## 4 验收链（每条边缺一不可，缺任一项即"未通过"）

1. **TS**：恰好 1 个虚频，且该虚频模以声明的成键/断键原子对（watch pair）为主；
2. **IRC 双向**都真实到达声明的两个端点（方向区间证据，不强求全轨迹跑完 native 上限）；
3. **两端点 Opt+Freq**：0 虚频极小值，物种/质子位置/立体身份（含 CIP）核验；
4. **能垒 = 纯电子能差**（无 ZPE/热校正），相对**该步自身起点的极小值**；多步网络逐步各算各的起点；
5. 原生日志**不改写**，路径 + sha256 记录，能量取自日志原始行；
6. 写回题源 → 重新生成题面 → 守卫测试通过（见 §6）。

若有一步被证伪（找不到鞍点、质子走错侧、优化滑落），**如实记录"该边缺测 + 缺什么 + 已证伪什么"**，不要编值、不要改图、不要宣布不可达。

## 5 计算资源（硬约束，避免互相踩）

- **2026-10-15 算力放开（用户指令）**：本机 node-local：32 核 / 51200 MB / 10 槽。单作业上限 **≤12 cpus / ≤14000 MB**（`%nprocshared=12`、`%mem=14GB`，按此声明）。
- **并发（16:10 更新）**：每包最多 **2 个** QM 作业同时在跑（优先关键路径；若你的分道彼此独立，例如 E1 道/E2 道，可并行）。节点总容量由调度器按余量排队，看到排队是正常的，不要为了"清空队列"提高 priority 或重复提交。
- 若借调高斯/ORCA 之外的计算资源（如用户提供的 HPC/Slurm 节点），先与主协调确认，不要自行注册节点或改 nodes.json。
- 节点总容量由调度器按余量排队：排队时**不要**重复提交、不要调 priority、不要杀别人的作业。
- 提交前用 `query_compute_queue` 查余量；不要设置非原生超时/MaxIter/MaxSteps；不要杀别人的运行作业；旧封顶路线不因接手自动解除。
- TS/IRC 必须走 durable 工作流 **ts_prepare / ts_resume**（手工 TS/IRC 提交当前被禁用）；先读它们的契约文档。
- 每次提交前做防撞双查（队列 + 运行作业），作业目录独立，禁止共用同一目录。

## 6 回填与文件归属（严格按包划分，防止并发写冲突）

| 包 | registry（唯一属主） | 生成题面 | 允许改的 md 行 |
|---|---|---|---|
| HI1 | `cloudra/benchmark/hard_registry/hi.py` | `ideapool/tasks/hard/HI1.json` | `hard.md` 中 HI1 那一行 |
| HL1 | `cloudra/benchmark/hard_registry/jl.py` | `ideapool/tasks/hard/HL1.json` | `hard.md` 中 HL1 那一行 |
| NR1 | `cloudra/benchmark/normal_registry/ru.py` | `ideapool/tasks/normal/NR1.json` | `normal.md` 中 R1 那一行 |
| NI5 | `cloudra/benchmark/normal_registry/ai.py` | `ideapool/tasks/normal/NI5.json` | `normal.md` 中 I5 那一行 |
| NY3 | `cloudra/benchmark/normal_registry/yo.py` | `ideapool/tasks/normal/NY3.json` | `normal.md` 中 Y3 那一行 |

- 只改自己包的 `barrier` 字段（或补上该键）与必要注释；**不要**改生成器、评分规则、其它题、其它边。
- md 只改自己那一行：改前重取 `read` 的 sha256，用 `edit`；冲突就停下并在 hub 报。
- **不要提交 git**：改动留在工作区，由主 Coordinator 汇总后统一决定。
- 重新生成题面：用仓库现成生成入口（`cloudra/benchmark/gen_normal_tasks.py` / `gen_hard_tasks.py`，与各自 `__main__` 用法一致），然后跑 `tests/test_benchmark.py -k regenerate_identically` 相关守卫；若有预先存在的 mismatch，先说明它在你改动前就存在。

## 7 汇报与协作

- 每个包在自己目录 `gold_finish_20261015/<TASK>/` 留 `STATUS.md`：每条边一行状态（已回填值/缺测+缺什么）、日志绝对路径 + sha256、方法一句、下一步。
- `agent_hub` 主题 **gold-finish-20261015**：开工帖 → 每条边终态帖 → 阻塞/裁决请求帖；地址 `to_agent=coordinator`（主协调）。别人的包不要重算，先 `agent_hub search` 查是否已有人做过。
- 结论必须区分"计算完成"与"验收通过"。
- 需要人类裁决的（HI1_E1 合并边是否拆步、HL1 O 路线 vs N 路线、NY3 图定义），给出证据 + 具体裁决问题，**不要擅自改图**。

## 7.5 平台问题的标准流程（2026-10-15 用户指令）
- 遇到**平台/工具面**问题，先只读取证（ps/pgrep、作业 guard 日志、真实文件系统读），把可复核证据 + 复现步骤报给主协调，**不自行改平台代码/数据库、不杀进程、不重启服务**；由主协调提 GitHub issue（仓库 yyywaa/Cloudra-mechanism-agent）并在 LEDGER 登记。
- 已提 issue：#176 compute.db 持久写锁（作业卡 running 占容量 + ts_prepare tool_exception）；#177 工具面/角色面缺口（explorer·writer 无写权限、排队作业无取消入口、ts_prepare 异常不可诊断）；#178 integrity.py 组分个数规则在 schematic SMILES 题面下的评分缝隙。
- 恢复手段（仅主协调执行）：只 TERM uvicorn API（scheduler 不是持有者），启动器按原 --port 8000 拉起；恢复后 scheduler 会用 adopt 收尾卡死行；副作用是会打断在跑的 agent run。

## 8 边界

- 不改动平台服务、不重启 web/scheduler、不动数据库、不碰别人的包与文件。
- 不扩大范围：只做自己包里的边；发现别的边也在缺，报给主 Coordinator。
## 9 机理选择政策（用户 2026-10-15 指令；覆盖此前不改图/不改值的限制）

用户原话：标答都没有验证过，所以不具有任何权威性，有更好的机理就选择。

执行口径：
1. 题源参考图与既有 gold 值均不具权威性。不得为了让结果对齐标答而迁就不可信的历史几何、旧值或旧命名。
2. 当本批计算证据支持更好的机理时，按证据选择：可改参考态（用真实极小值）、改质子化位点/通道归属、拆步或合并节点与边、替换身份可疑的旧值。这类改动现在被授权，但必须同时满足：
   - 证据充分：同批原生日志绝对路径 + sha256 + 行号；能量只能同程序同批相减；关键驻点要 0 虚频或恰 1 虚频并核身份（CIP/质子归属/分片）；
   - 写明改了什么、依据什么、与旧图的差别、影响哪些边；
   - 同步更新本包题源（registry + 生成器输入）与自己那一行 md，并跑生成器 + pytest tests/test_benchmark.py -k regenerate_identically 守卫，原样留证。
3. 验收链的科学性不变：有鞍点就必须恰 1 虚频 + 模式归属说明 + 双向 IRC + 两端点 0 虚频与身份核验；虚频模若不在声明键对上（pseudo-saddle），必须如实标注并按技能/playbook 口径处理，不得硬当 TS。
4. 无合格鞍点不是失败：可记无独立鞍点，但必须给证据（扫描/弛豫剖面无内峰、未约束优化坍缩、ts_prepare 原文）与替代口径（如相对分离反应物的沉没垒、或按前平衡步记 0 并注明依据）。不得凭空填数。
5. 交付时单列一节证据驱动的机理修订：旧图/旧值 -> 新图/新值 + 依据 + 影响面。
