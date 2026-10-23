# 04 · P0 冻结清单（题库 / 评估器 / 失败分类 / 重试规则 / 模型配置 / 正式数据布局）

> 状态：**只读代码审计 + 只读数据盘点**，不含任何 LLM/付费调用、不含任何 QM 计算。
> 审计对象：`/home/ly/cloudra-bench-20261019`（分支 `docs/p0-acceptance`，HEAD `1e6d953f`）
> 与四个 arm checkout：`/home/ly/cloudra-arm-{guided,record,standard,brief-errors}`。
> 写入范围：**只有本文件**。未切换分支、未改产品代码、未向任何正式数据目录写入。
> 相关文档：`00_lead_checks.md`（Lead 自查）、`01_arm_behavior.md`、`02_bc_diff.md`、`03_evidence_chain.md`
> （01–03 由并行任务产出；本文件的哈希/结论口径与 00 一致，重叠处已在文中互引）。
> 计划依据：`ideapool/cloudra_four_arm_experiment_plan.md` §3.1（第 64–69 行）、§四（第 83–97 行）、
> §六（第 126–162 行）、§八（第 170–178 行）、§九（第 180–207 行）。

---

## 0. 口径与基线

### 0.1 基线 commit（不是同一个 commit）

| 对象 | 分支 | HEAD commit | 说明 |
|---|---|---|---|
| 共享仓库 / master | `docs/p0-acceptance` = `master` | `1e6d953f998848b2499f7a5e69df22842c3fd869` | master tip；docs/p0-acceptance 与其同点 |
| 共同产品基线（计划 §九） | — | `8c568ca6753ecf2cd40a90a8f0f8b5c8e19dd1d2` | 四臂都包含该 commit（`git merge-base --is-ancestor` 全部为 true） |
| 计划落盘 commit | — | `0e4a840f739ef2d8e6b09a091ae8f6918faf7afd` | 仅新增四臂计划文档 |
| A `benchmark/arm-guided` | arm checkout | `e67ef30abd8807297a7c4f095836eee3ee04bb77` | 含 merge `1e6d953f` |
| B `benchmark/arm-record` | arm checkout | `058fdc82907bc6f4a0dbf60a62dbc11e8865c701` | 含 merge `1e6d953f` |
| C `benchmark/arm-standard` | arm checkout | `79ca80bf8c3c2ea7a48e2cab1f8455a2fcccd55d` | 含 merge `1e6d953f` |
| D `benchmark/arm-guided-brief-errors` | arm checkout | `0b81c2625fbf9a62e221deebe1b62ce74bd2330e` | 含 merge `1e6d953f` |

**结论（重要）**：共享仓库 HEAD、四个 arm HEAD 是**五个不同的 commit**；正式运行必须逐臂记录
`git rev-parse HEAD`（计划 §九第 182 行），不能用共享仓库 HEAD 代替。四臂工作树均**干净**
（`git status --porcelain` 只有未跟踪的 `run.sh`，下述）。

### 0.2 arm 身份不是题目 JSON 里的 `mode`

- 50 道题的 `prompt.orchestration_mode` **全部是 `"dag_guided"`**（历史标签，见 §1.5），
  不能当作实验组身份。
- 每臂在 `cloudra/benchmark/runner.py:221` 烘焙常量 `ABLATION_ARM`，并覆盖所有 spawn/记录点：
  - `cloudra/benchmark/runner.py:221` `ABLATION_ARM = OrchestrationMode.<ARM>`
  - `runner.py:224-232` `task_project_settings()` 用 `ABLATION_ARM.value`
  - `runner.py:241-247` `provenance_config()` 写 `experiment_arm` / `error_feedback` /（C 专有）`scientific_feedback`
  - `backend.py:195`、`batch.py:339/393/506/522` 的 spawn settings 与 `RunResult.orchestration_mode`
- 各臂取值：A `DAG_GUIDED`、B `DAG_RECORD`、C `STANDARD`、D `DAG_GUIDED`（D 只改错误反馈，
  与 A 同 mode，符合计划表格）。`OrchestrationMode` 定义见 `cloudra/runtime_v2/schemas.py:48-51`。

### 0.3 环境实况

| 项 | 值 | 证据 |
|---|---|---|
| OS/解释器 | WSL Ubuntu，Python `3.12.3`（`/home/ly/cloudra-bench-20261019/.venv`） | `.venv/bin/python --version` |
| 评分依赖 | rdkit `2026.09.1`、networkx `3.7`、pydantic `2.14.1`、openai `3.35.1`、numpy `2.5.4`、pandas `3.0.6` | `.venv/bin/python` 导入探测 |
| 锁文件 | `uv.lock` sha256 `7412dc94e8767b474a61cefeb2a685064e6107d312d6cac9ecdea263e1add9e1` | `sha256sum uv.lock` |
| 计算环境 | `g16` 包装脚本 `/home/ly/bin/g16`、`xtb 6.5.0`（`/home/ly/xtb-6.5.0/bin/xtb`）；**ORCA 未安装**（`command -v orca` 空） | 需在 arm `run.sh` 的 PATH 下才可见（见 §6.5） |
| 磁盘 | `/home/ly` 所在卷 984G，已用 229G，**可用 714G** | `df -h /home/ly` |

> 计算环境只在 arm `run.sh` 设置的 PATH 下可见（`/mnt/c/.../bench` 里没有 g16/xtb）；
> 直接 `wsl bash -lc` 默认 PATH 下 `which g16` 为空，这是审计时容易误判的一点。

---

## 1. 题库冻结（Task bank）

### 1.1 规模与 task id

| tier | 目录 | 数量 | task ids |
|---|---|---|---|
| easy | `ideapool/tasks/easy` | **20** | D1, D3, D4, E1, F1, F4, G2, G3, L1, L2, M1, M14, M15, M16, M17, M3, M8, P2, P3, X1 |
| normal | `ideapool/tasks/normal` | **10** | NB1, NI1, NI5, NQ1, NQ5, NR1, NU3, NU5, NU6, NY3 |
| hard | `ideapool/tasks/hard` | **10** | HA1, HA6, HA8, HB1, HB10, HD2, HF1, HH1, HI1, HL1 |
| impossible | `ideapool/tasks/impossible` | **10** | IA1, IA5, IA7, IA9, IB9, IC3, ID2, IE2, IF3, IG8 |
| **合计** | | **50** | 无跨档重复 task_id；目录名与题内 `tier` 字段 100% 一致；50 个文件全部被 git 跟踪 |

### 1.2 内容哈希（题库身份）

哈希定义固定为下列两种，二者都在审计中复算过，任选一种即可复现题库身份：

```bash
# (H1) 排序文件清单哈希：对 sha256sum 输出（含路径）再取 sha256
cd /home/ly/cloudra-bench-20261019
find ideapool/tasks -name '*.json' | sort | xargs sha256sum | sha256sum
# -> 5db51268e1cf605d693151db2a60bbff17891a80f2d4ba77cf216ff0c4a66aa6
```

| 范围 | H1（排序清单 sha256） | H2（canonical：`相对路径\0文件sha256\n` 排序拼接） |
|---|---|---|
| easy | `f9e07656083764174ca5bd6efd065e9b99d0c0bad093f0456e75607ac57a82f6` | `fec921b1377ba6e4eb2ac7622245992ad51c9e7fe80f3dcb3f59d28fc2f2b1da` |
| normal | `82a046418320acad5e697dc811f4082fe949eff69123d3cf457d3d4d430a94f5` | `f0209a509595c4757b6536d7cd6f05f9e75b29d685adeffc187772582c605a8a` |
| hard | `ea95f9651b1b5315ba0f38a8ecd7b056e029742a196ed608fc67f82dc088f3df` | `277c1d371e8918bb17490a00d1c6cf1fe34bdf23e45327e83feaac3486e3d24e` |
| impossible | `1975c22de99f9be27474730e4aa8ff9cbbd794b4778c5ff5a7548230e5059402` | `061c68f877140f489640c91c6a75298be36c1b673a7cc31d662ccba3afaa687b` |
| **全库** | **`5db51268e1cf605d693151db2a60bbff17891a80f2d4ba77cf216ff0c4a66aa6`** | **`a9a9b17a36c4bfc6d4df7fd46e20512f496c3bb06398a576280582f5d103ad18`** |

正式运行的 `arm.json` 必须记录 **H2 全库值**（`task_bank.sha256`，见 §6.4）；H1 便于 shell 复算。

### 1.3 git 口径

- 最近一次改动题库的 commit：`24d059d7fcc571d168a46caa9939145cb65d0ec7`（2026-10-22 05:25:05 +0800，
  `fix(benchmark): one-to-one step matching, runs insert, and simpler HH1`）。
- 该 commit 之后题库内容未再变化：`git status --porcelain -- ideapool/tasks` 为空；
  共享仓库 HEAD（`1e6d953f`）中的题库 = 该 commit 内容。
- 四臂 HEAD 都包含 `1e6d953f`，且 `git diff --name-only master..benchmark/arm-* -- ideapool/tasks` **全部为空**。

### 1.4 四臂共享同一题库（可复核）

在 5 个 checkout 分别复算 H1，结果**完全相同**：

| checkout | task json 数 | H1 | 工作树内 tasks 改动 |
|---|---|---|---|
| `/home/ly/cloudra-bench-20261019` | 50 | `5db51268…6aa6` | 0 |
| `/home/ly/cloudra-arm-guided` | 50 | `5db51268…6aa6` | 0 |
| `/home/ly/cloudra-arm-record` | 50 | `5db51268…6aa6` | 0 |
| `/home/ly/cloudra-arm-standard` | 50 | `5db51268…6aa6` | 0 |
| `/home/ly/cloudra-arm-brief-errors` | 50 | `5db51268…6aa6` | 0 |

**结论：没有任何 arm 分支修改题库 JSON（四个 `git diff` 均为空），四臂题库可证明同源。**
四臂唯一未跟踪文件是各自的 `run.sh`（逐臂 sha256 相同，见 §6.5），不影响题库/评分代码。

### 1.5 题库组成细节（冻结时必须知道）

- 每道题的评分 rubric **内嵌在题 JSON 里**（`rubric.{integrity,self_consistency,graph_similarity,accuracy}`），
  因此 §2.3 的 sigma / 权重一旦改动题库文件，哈希即变化——"改 rubric = 改题库"，不能悄悄改。
- `accuracy.enabled = true`：50/50。
- `sigma_kcal_mol`：**3.0** 共 30 题（easy 20 + impossible 10）；**2.0** 共 20 题（normal 10 + hard 10）。
- hard 档 10 题 `stereo_tier_rule = "hard_stereo_costly"`；其余 40 题 `easy_normal_stereo_free`。
- 带 hard 定性选择性锚点（`gold.selectivity.favored_channel`）的题：**HA1, HA6, HB1, HF1**
  （这 4 题 accuracy 槽位评分被"定性选择性"替代，见 §2.2；barrier 数值只记录不计分）。
- 负目标/不可达题：impossible 10 题都含 `accessible=false` 节点；其中 **ID2** 的 gold 图 0 条边
  （纯负向断言评分路径，`accuracy.py:423-453`）。
- 本冻结题库**没有任何题使用 `gold.reference_properties`（性质锚点模式）**；
  accuracy 实际只走三条路径：能垒高斯、负目标断言、hard 定性选择性
  （`runner.py:447-472`）。
- 边数量分布：1 边 31 题、2 边 13 题、3 边 4 题、4 边 1 题、0 边 1 题（ID2）。
- HL1/HI1 的 gold 节点 `properties.evidence_log` 里带 `gold_compute/evidence/...` 审计路径；
  这只是 gold 溯源元数据，**评分器不会解析 gold 的 `evidence_log`**（`integrity.py:452-499` 只读交付图
  节点属性），因此评分不依赖 gitignored 的 Drive 证据包；但做 gold 溯源审计时仍需 Drive 包。

---

## 2. 评估器冻结（Evaluator）

### 2.1 评分链路

评分只读**沙箱交付物**（`mechanism_graph.json` + 原生 QM 日志 + `.cloudra/mechanism_evidence.json`），
不读模型散文（`runner.py:1-17, 404-405`）：

```
层1 完整性/证据绑定   integrity.py       audit_integrity()            -> 图可解析性 + 逐节点绑定质量
层2 物理自洽         selfconsistency.py  audit_self_consistency()    -> TS 一阶鞍点 + IRC 双向连接
    证据发现/回退    evidence_search.py  discover_edge_proof()        -> 在沙箱内主动找 IRC→Opt→Freq 链
层3 准确性           barrier_evidence.py collect_barrier_evidence()
                     accuracy.py         score_accuracy()             -> 逐 gold 边高斯/负目标/选择性
复合                runner.py           score_sandbox()              -> final = 0.1·图 + 0.3·自洽 + 0.6·accuracy
```

### 2.2 权重与公式（frozen）

| 常量 | 值 | 位置 |
|---|---|---|
| `W_GRAPH` | **0.1** | `cloudra/benchmark/runner.py:150` |
| `W_SELFCONSISTENCY` | **0.3** | `cloudra/benchmark/runner.py:151` |
| `W_ACCURACY` | **0.6** | `cloudra/benchmark/runner.py:152` |

```text
final = 0.1·graph_score + 0.3·selfconsistency_score + 0.6·accuracy_score          # runner.py:509-514
```

短路/特例（全部 frozen）：
- 图缺失/不可解析 → `final = -no_evidence_penalty`（默认 -1.0），倒扣机制见 `runner.py:474-481`；
- 有 accessible 节点但无任何节点绑定证据 → 同样 `-no_evidence_penalty`（`runner.py:482-499`）；
  全部节点声明 `accessible=false` 是合法交付，不触发；
- accuracy `fail_loud`（声明无据/与日志冲突）→ 自洽与 accuracy 清零，`final` 只保留图分
  （`runner.py:500-508`；`accuracy.py:89-90, 610-619`）；
- 后端崩溃/未评分行记 0.0，而不是 `no_evidence_penalty`（基建失败不是 agent 的锅，
  `runner.py:536-537` 注释 + `_run_one_guarded`）。
- 计划 §四第 87 行的 `weighted = 0.9` 指连续加权分（graph+selfcons 部分），**不是**科学成功率；
  本报告沿用代码权重口径 0.1/0.3/0.6。

### 2.3 rubric 默认值与 sigma（frozen）

定义：`cloudra/benchmark/schema.py`。

| 字段 | 默认值 | 位置 |
|---|---|---|
| `IntegrityRubric.match_threshold` | **0.2** | `schema.py:261` |
| `IntegrityRubric.protonation_partial_quality` | **0.7** | `schema.py:262` |
| `IntegrityRubric.no_evidence_penalty` | **1.0** | `schema.py:267` |
| `SelfConsistencyRubric.ts_first_order_saddle` | **true**（n_imag == 1） | `schema.py:281` |
| `SelfConsistencyRubric.irc_connects_endpoints` | **true** | `schema.py:282` |
| `GraphSimilarityRubric.stereo_tier_rule` | `easy_normal_stereo_free`（hard 题内覆盖为 costly） | `schema.py:288-290` |
| `AccuracyRubric.sigma_kcal_mol` | **3.0**（题内覆盖 2.0 见 §1.5） | `schema.py:307` |
| `AccuracyRubric.max_penalty_fraction` | **0.3** | `schema.py:310` |
| `AccuracyRubric.small_barrier_threshold_kcal` | **10.0** | `schema.py:312` |
| `AccuracyRubric.small_barrier_sigma_kcal` | **5.0** | `schema.py:312`（≤10 kcal 的边放宽到 5.0，`accuracy.py:106-111`） |

性质锚点 sigma（本冻结题库未使用，但代码路径存在）：`_PROPERTY_SIGMAS`（`accuracy.py:66-72`）：
`bond_length_angstrom → 0.02`、`cm-1 → 50.0`、`kcal_mol → 2.0`；表外数值键 fail-loud（`accuracy.py:114-123`）。
“答案定义差异”逐边固定记分 `_DEFINITION_MISMATCH_EDGE_SCORE = 0.9`（`accuracy.py:75`）。

### 2.4 一对一匹配（frozen）

- `accuracy.py:333-386` `_assign_matching_steps()`：**最大基数、最小化学代价的一对一匹配**
  （`nx.min_weight_matching`），代价 = bond-change 对称差 × bond_scale + 端点物种替换代价；
  平局按 gold 图顺序与交付 id 稳定排序，不看数值接近程度、不看私有 gold id 顺序。
- 每 gold 边先经 `_rank_matching_steps()`（`accuracy.py:291-330`）按
  `species_substitution_cost ≤ match_threshold(0.2)` 过滤候选；多通道 gold 边要求 channel 一致
  （`accuracy.py:358`）。
- 匹配后逐边打分（`accuracy.py:455-631`）：带参考值边 → 高斯分；不带参考的 accessible 边记 1.0；
  不可达目标按最终负声明正确记 1.0、误报/漏交记 0.0；`max_penalty_fraction=0.3` 只封顶
  "带参考值边"的罚分（`accuracy.py:619-625`）。

### 2.5 证据发现 / fallback（frozen）

| 机制 | 位置 | 说明 |
|---|---|---|
| 图文件探索 | `integrity.py:156-170` | 先 `sandbox/mechanism_graph.json`，否则递归找可解析为图形状的 `*.json` |
| 沙箱证据扫描 | `integrity.py:287-333` | 后缀白名单 `.gjf/.com/.inp/.xyz/.log/.out/.sdf/.mol/.json`，只接受 sandbox 内（含 symlink 目标）文件，排除交付图自身 |
| 原生日志 SMILES 绑定 | `integrity.py:242-276` | 从日志注释/title 的 `smiles:` 行提取物种，作为绑定锚点 |
| 绑定质量 | `integrity.py:401-534` | 指纹/哈希命中质量 1.0；仅质子化/电荷变体按 0.7 部分记分；未绑定按代价 1.0 记账并入图分 |
| 评分侧链发现 | `evidence_search.py:1-15, 31-33, 178+` | 沙箱内主动找 `IRC→Opt→Freq` 链；分级计分 saddle 0.35 + IRC 起始鞍点 0.15 + 端点 lineage 0.50（单侧连接 0.25）= 满分 1.0 |
| 自洽层回退 | `selfconsistency.py:444-484` | 绑定证据不足时不判失败，继续 `discover_edge_proof()` 找链；仅接受 `verify_short_irc_direction(...) == True` |
| 最小见证回退 | `selfconsistency.py:144-160` 等 | 从绑定 anchor 在沙箱日志池里找频率/极小值见证 |
| 声明能垒推导 | `runner.py:89-147` | 交付图缺边能垒时，用节点 `energy_hartree` 差值推导（仍要求日志支撑，accuracy 层核对） |
| 交付端点绑定 | `delivery_evidence.py:76-102` | 程序写入/读回 `.cloudra/mechanism_evidence.json`（`read_step_endpoint_evidence`）；缺失时 `undelivered=True`（`runner.py:412`） |

**结论：发现/回退链在评分器侧（`cloudra/benchmark/`），四臂同一份代码；不在 DAG/Agent 侧，
因此 arm 差异不改变 fallback 行为（符合计划 §八第 5 点）。**

### 2.6 评估器跨臂一致性（核心结论）

评分代码文件 sha256（**main 与四臂逐字节对比**；完整 64 位值）：

| 文件 | sha256 | 四臂一致？ |
|---|---|---|
| `cloudra/benchmark/accuracy.py` | `fa0676a97def21189ce48e3f773bcd8de8f1e55ac6531da891cd234daf1bf5c7` | ✅ 全同 |
| `.../selfconsistency.py` | `42144630396896f7b64547c3b3db0696a1b06c2c3e9dca2c8350d3f060a2d026` | ✅ |
| `.../graph_similarity.py` | `ba9d7e8a5131af9914ccabf84a8c28e20be1aff0295645b48f767605f4c6d9b5` | ✅ |
| `.../schema.py` | `9a1f51b30da140200c081d7324873b46df7a06202adc1f2ac18f9bb1ad99ca8f` | ✅ |
| `.../integrity.py` | `d2b8404149a2b4ab85923c96ba3a1a63e862ac4d1eeb28c0629da554057c14cb` | ✅ |
| `.../evidence_search.py` | `a5b382e4bd9d6ff87945e24764d0f07ad5255259f4902d11ef7837d1ac1ca066` | ✅ |
| `.../delivery_evidence.py` | `1dd5631e408807ec128e769ca0b2b9ee4f4acb62880bd5ecade4662f1086c29e` | ✅ |
| `.../barrier_evidence.py` | `67db6ba183f50e1d115317870cd49a95c108403b1fca79b1c7c0fb0fe6d009a6` | ✅ |
| `.../watch.py` | `9bdee6ff2d9ab1953609f465f265dfe475c672c2a99f44099456c417f30721ff` | ✅ |
| `.../__main__.py` | `a877c0532dadc0179a8c91304a0993e9816c77e62d540a3446d2eeda5b02816b` | ✅ |
| `.../api_pool.py` | `9f0205a6502a94a94f07d75585d8c3746bedba390f892c1df889f6092dd2d511` | ✅ |
| `.../method_policy.py` | `f9891c9375b5ca14ce2958809c6b4825c252bbe1f6cd5c22b2861c5c5b33578d` | ✅ |
| `.../query_builder.py` | `1f6d749e3c442c4bf8cfc2af1974a1f614686c95619b32bdd5a82556adbee329` | ✅ |
| `.../batch.py` | main `89a93abf3cf1e0142845e4f20d9cea276a496dc246fc4a17517e179410b66eff`；四臂 `a6da71dbff692b374c189e3ef7aed51de09d9eaa5cdd4d3c82971e16b79f33e5` | ✅ 四臂同；与 main 差 arm 接线 |
| `.../backend.py` | main `3b9862c9d252bc8284142d235afafe9809e6bcb740741aa6328d63dc967ebdb9`；四臂 `e08a73d32b18f7452af6c6f9e7728ad81c32da589042b7d1bd42d6d719ebebf3` | ✅ 四臂同；与 main 差 arm 接线 |
| `.../runner.py` | main `3cdbdf2796beab036ca5c299964e44f949949c5d8ac01beb619c373a8e3e2186`<br>A `0dfee4319be851347d65b2ca6b90626bf1440bcf5911468c8c2047292807a7d9`<br>B `29d0b4db6d291592ba1e58886972a9cb683a3314eddda17bb0fb098e8fc0112d`<br>C `a007d133aa4c6c85f642b5008bf435a86ba459dd37583c00ec725718bac44415`<br>D `7aef6234029b51bc7b4581a29658d50428ecee328ac2c59beb4e93115c015eb2` | ❌ **四臂不同**，差异已核为 arm 接线 |

`runner.py` 跨臂差异的完整清单（`diff` 逐行核对）**只有**：
1. `import ABLATION_ARM` / `ABLATION_ARM = OrchestrationMode.<ARM>`（`runner.py:221`）；
2. `task_project_settings()`、`RunResult.orchestration_mode`（两处）、`provenance_config()` 的 arm 覆盖；
3. `provenance_config()` 增加 `experiment_arm` / `error_feedback`（A/B/D）或再加 `scientific_feedback`（C）；
4. 注释文字。
**权重、accuracy 公式、自洽评分、图分、发现式检索、rubric 默认值均未改动。**

评分器依赖（`cloudra/benchmark` 之外的导入闭包）四臂 sha256 也全部相同：
`cloudra/tools/core/irc_evidence.py` `cfb1eb0e…`、`irc_path.py` `4b25f7bd…`、`qm_log_facts.py` `5d2fdbde…`、
`species_identity.py` `7cbf952e…`、`orca_frames.py` `77dc7f76…`、`qm_engine.py` `3a96ad46…`、
`cloudra/runtime_v2/schemas.py` `fef34d31…`、`cloudra/infra/config.py` `de870da1…`、
`cloudra/persistence/paths.py` `7656d416…`。

### 2.7 评估器运行环境（⚠ pending）

- 四臂的 `run.sh` 用**共享仓库的** `.venv` 解释器（`/home/ly/cloudra-bench-20261019/.venv/bin/python`），
  而 `.venv` 里 cloudra 是 **editable 安装**，`cloudra.__file__` 当前指向
  `/home/ly/cloudra-bench-20261019/cloudra/__init__.py`。
- arm `run.sh` 用 `export PYTHONPATH="$HERE"` 强制 arm 代码优先（PYTHONPATH 在 site-packages 之前），
  所以**必须**用各臂 `./run.sh` 启动；若绕过它直接 `.venv/bin/python -m cloudra.benchmark`，会
  跑到共享仓库代码 → 臂代码/评分接线错位。**冻结要求**：正式运行前必须验证
  `python -c "import cloudra; print(cloudra.__file__)"` 指向对应 arm 目录，并把结果写进 `arm.json`。
- `.venv` 是共享可变依赖：任何人 `pip install`/`uv sync` 都会改变评分环境。
  → 待办：记录 `.venv` 依赖快照 + `uv.lock` sha256（§0.3），并把"运行期间不得改动 .venv"写入运行纪律；
  更稳的做法是给每臂复制独立 venv（待裁决，见 §7）。

---

## 3. 失败分类（Failure taxonomy）

### 3.1 分层模型

一次 benchmark 运行可能终止在 4 个层次，标签互不等价，**不能混成一个"失败"**：

```
(runtime 层) run.finished.outcome / failure_kind
      ↓
(agent 层)   AgentState = succeeded | failed | cancelled | waiting_input | waiting_approval
      ↓
(watcher 层) done / cancel(reason) / resume / reconcile
      ↓
(benchmark 层) batch.status + task row (runs.notes / undelivered / final_score) —— 或"从未评分"
```

`AgentState` 定义：`cloudra/runtime_v2/schemas.py:68-75`；
`RunFailureKind` 定义：`cloudra/runtime_v2/failures.py:17-32`。

### 3.2 终态/标签清单与产生位置

| # | 标签（枚举字符串） | 层 | 产生位置（file:line） | 持久化位置 | 对评分的影响 |
|---|---|---|---|---|---|
| 1 | `completion_no_progress` | run | `cloudra/runtime_v2/agent_runner.py:430`（`finish_run(outcome="failed", failure_kind=...)`）；判定与计数 `:405-431`、`:858-877`；默认 `max_exit_strikes=3` 于 `:73` | runtime 事件 `run.finished.failure_kind`（`agent_runner.py:840` 写 `agent.completion_gate`）；agent 变 `FAILED` | 不是 benchmark 行标签；沙箱**仍会被评分**（watcher 对终态返回 done，见 #11），通常 `undelivered=True` → 可能 -1.0 或部分分 |
| 2 | 退出审批拒绝（gate rejection，非终态） | run | 门禁四态 `continue_work / wait_background / wait_review / allow_final`：`agent_runner.py:8-9, 412-470, 785-846`；DAG 退出审计 `cloudra/dag/stop_audit.py:42-62`（`StopGate`）、`:221`（`audit_stop`）；硬拦截接线 `cloudra/runtime_v2/policies/dag_stage.py:127,136`；`cloudra/dag/completion.py:51`（`evaluate_delivery`） | `agent.completion_gate` 事件（`agent_runner.py:840`）；DAG 裁决落 `dag_review_decisions`（`cloudra/dag/store.py:691-713`）；Supervisor 裁决通知 `call_verdict`/`draft_verdict`（`cloudra/runtime_v2/supervision.py:478-505`） | 非终态：run 继续（反馈下一轮）或挂起；连续 3 次无进展 → 转 #1 `completion_no_progress`；A/D 专属的 stop 门禁拒绝**不是** benchmark 失败行 |
| 3 | `cancelled by batch stop` | benchmark 行 | CLI：`cloudra/benchmark/runner.py:549`（`_run_one_guarded`；`BenchmarkStopped` 抛点 `:521,526,529`）；Web 批次：`cloudra/benchmark/batch.py:520`（`_cancelled_result`）、`:523-531`（`_mark_cancelled`，`st.status="cancelled"`） | `runs.notes` = `["cancelled by batch stop"]`，`final_score=0.0`（占位，**未评分**） | **未评分**：不得当 0 分/科学失败；见 §3.3 |
| 4 | `undelivered` | benchmark 列 | 置位 `cloudra/benchmark/runner.py:412`（`not (sandbox/".cloudra"/"mechanism_evidence.json").is_file()`）；列/行 `runner.py:171,187,200,213` | `runs.undelivered = 0/1` | **已评分行的交付状态**，不是科学零分（计划 §四第 95 行）；仍按图分/自洽/accuracy 计算，可能 -1.0（无图/无证据）或部分分 |
| 5 | 模型/网络失败：`provider_transient_exhausted`、`provider_permanent` | run | 枚举 `failures.py:27-28`；分类 `failures.py:63-79`；retryable 判定 `failures.py:46-60`；run 内 turn 重试 `agent_runner.py:345-373`（`run.retry` 事件，`max_turn_retries=5` 于 `:101`，backoff `(2,4,8,15,30)` 于 `:102`）；client 层重试 `cloudra/infra/llm_client.py:285`（`max_retries=4`）、`:644-664`；API pool 429 换端点 `cloudra/benchmark/api_pool.py:1-13, 68-111` | runtime 事件 `run.finished.outcome="failed"` + `failure_kind`；agent `FAILED`；`run.retry`/`llm_retry` 事件计数 | 不是 benchmark 行标签；agent 终态后沙箱仍评分（同 #1）。**规则上按"模型/网络错误"计数、不重跑**（§4） |
| 6 | 预算类失败（token/context、JS 工具请求） | run | token 预算超限 `agent_runner.py:1055-1080`（`Configured token budget exceeded`），压缩重试 `:1064`；JS 程序工具请求预算 `cloudra/runtime_v2/js_runtime.py:454`；子 agent 重试预算耗尽提示 `cloudra/runtime_v2/child_manifest.py:36-39` | runtime 事件/消息；agent 终态 | 同 #5：计数不重跑；**注意：CLI 没有"整题总预算"硬参数**（§5.5 B2） |
| 7 | `infrastructure failure: ...` | benchmark 行（Web 批次） | `cloudra/benchmark/batch.py:496-512`（`_mark_infra_failure`）；触发点 `:280-293`（沙箱有 live 计算/沙箱准备 OSError）、`:432-434`（题目异常） | `runs.notes` = `["infrastructure failure: ..."]`，`final_score=0.0`（未评分）；`st.status="error"` | **未评分**；按 §4 规则可"同配置重试一次" |
| 8 | `task crashed: ...` | benchmark 行（CLI） | `cloudra/benchmark/runner.py:549`（`_run_one_guarded` except；打印 `:541`） | `runs.notes` = `["task crashed: <exc>"]`，`final_score=0.0`（未评分） | **未评分**；Python 异常而非科学结论 |
| 9 | `benchmark watcher: ...` | benchmark 行（Web 批次） | `cloudra/benchmark/batch.py:379-400`（`wait_error`；`st.status="error"`，不评分）；reason 来源 `cloudra/benchmark/watch.py:244-251`（等 Supervisor 裁决无 Supervisor / `agent stuck in <state> with nobody to answer`）；`watch.py:271`（批次停止） | `runs.notes` = `["benchmark watcher: ..."]`，`final_score=0.0`（未评分） | **未评分**；其中"无人裁决的挂起取消"属**未决/工程失败**，需单独报告 |
| 10 | 批次状态 | batch 行 | Web：`idle|running|stopping|done|error`（`batch.py:156`），收尾三态 `:254-261`；CLI：`error|stopped|done`（`cloudra/benchmark/__main__.py:102-108`），退出码 `117`（`128+SIGINT/SIGTERM`） | `batches.status` | 批次级完整性：`stopped` = 人工/信号中断，未完成全题集，**不能当完整实验批** |
| 11 | agent 终态直接进评分（无独立标签） | watcher→benchmark | `watch.py:183-192`（`FAILED/CANCELLED` → `done`）；CLI `backend.py:283-292` 仅在 watcher 返回错误时抛异常 | 无专门 notes 标签；由 `undelivered`/分数体现 | **关键**：`completion_no_progress`/provider 失败等 run 级标签在 benchmark 行里**不可见**；必须保留 `runtime/`（runtime-v2.db + conversations）才能事后分类 |
| 12 | 评分侧"零证据"标签 | benchmark 分数 | `runner.py:477-499`（`final = -no_evidence_penalty`，notes：`no parseable mechanism graph -> no evidence possible; penalty applied` / `... unsupported claims; penalty applied`）；`runner.py:431`（`no delivered graph to compare`） | `runs.notes` + `final_score` | 是**评分标签**（-1.0），不是运行失败；报告必须与"未评分"分开（§3.3） |

### 3.3 三类行的语义（报告口径，必须写进分析脚本）

`runs` 表里同一列 `final_score` 承载三种完全不同的语义，冻结后必须按 `notes` 前缀分类：

| 行类别 | 判定条件 | 语义 | 报告处理 |
|---|---|---|---|
| **未评分（not scored）** | `notes` 含 `cancelled by batch stop` / `infrastructure failure:` / `task crashed:` / `benchmark watcher:`；或本行由 `_cancelled_result`/`_mark_infra_failure` 生成 | 运行/工程终态，`final_score=0.0` 是**默认占位，不是测量值** | 计入"计划题数/启动题数/未评分题数"分母；**不得**进入分数均值、**不得**当科学失败或成功率分母 |
| **已评分但未交付** | 已评分（`score_sandbox` 正常返回）且 `undelivered=1` | 交付状态；图/证据可能仍被评分器从沙箱恢复 | 单独报告"交付状态"轴；-1.0 时说明是评分规则而非化学结论（计划 §四第 95 行） |
| **已评分** | 其余 | 正常三轴测量（图/自洽/accuracy 或负目标/选择性） | 主结果矩阵；报告所有 50×4 配对 |

判据代码事实：`RunResult` 默认 `final_score=0.0`（`runner.py:165-178`）；`_cancelled_result`（`batch.py:514-521`）与
`_run_one_guarded` 的异常分支（`runner.py:534-550`）都**不调用 `score_sandbox`**；而 `undelivered` 只在
`score_sandbox` 内设置（`runner.py:412`）——所以"有 undelivered 值"的行一定是已评分行。

### 3.4 既有正式数据中的真实样例（只读核对）

- `/home/ly/cloudra-bench-full-20261022/benchmark.db`：`batches.status="stopped"`，
  50 行中 **46 行** `notes=["cancelled by batch stop"]`、`final_score=0.0`；仅 4 行真正评分。
  → 典型的"未评分行"样例，**均值为 0.06 是没有意义的**，绝不能作为该批成绩。
- `/home/ly/cloudra-bench-run6-20261021/benchmark.db`：`status="done"`，20 行全部评分，
  `final_score` 0.0667–1.0（均值 0.8032）。注意该库是**旧 schema**（见 §6.1）。

---

## 4. 重试与排除规则（预注册草案，frozen 前需 Lead/用户确认）

### 4.1 计划约束（原文要点）

- §3.1 第 64–69 行：同一冻结题库/方法政策/计算环境/评估器；同一模型与预算规则；
  独立干净工作区；**"基础设施故障的重试与排除规则在看主结果前固定，不只重跑某组失败样本"**；
  **"正式运行冻结版本。若发现影响结论的修复，先标记受影响运行，再按统一规则重跑受影响的配对任务；
  不将修复前后的轨迹静默拼接。"**
- §六 P1 第 156 行：Pilot 与正式结果分开标记，不事后择优混入。
- §四第 90 行：明确分母（计划任务/实际启动/成功交付/可独立评估），不能只给可评分样本的高分。

### 4.2 现有实现事实（决定规则边界）

| 行为 | 现状 | 位置 |
|---|---|---|
| 批次级自动重试 | **没有**。基建失败只落一行 error 并继续下一题 | `batch.py:496-512`；CLI `runner.py:534-550` |
| run 内瞬态重试 | 有：turn 级最多 5 次（backoff 2/4/8/15/30s）+ client 级最多 4 次；4xx（非 408/429）不重试 | `agent_runner.py:73,101-102,345-373`；`failures.py:46-60`；`llm_client.py:285,644-664` |
| 429 换端点 | 有：`--api-pool` 时每次调用随机端点，429 failover（同一调用内不重复端点） | `api_pool.py:1-13,68-111` |
| 退出审批重试 | 有：同指纹连续 3 次无进展 → `completion_no_progress` | `agent_runner.py:73,858-877,412-431` |
| 人工停止 | SIGINT/SIGTERM → `stop_event` → 未完成题落 `cancelled`，批次 `stopped` | `__main__.py:89-108,117`；`runner.py:517-529,549` |
| 沙箱复用 | 禁止：每批新目录 `sandboxes/<task>/<batch_id>`，从不删除旧交付 | `runner.py:386-390`；`batch.py:440-442` |
| 数据删除 | 框架从不删除 benchmark 行/沙箱（append-only） | `runner.py:283-291` |

**注意**：既有的 run 内重试属于"系统行为"（四臂完全相同），不是"排除规则"；冻结后不得调参。
**批次级"基建失败重试一次"目前没有实现**，需要运行脚本/规则表承载（见 §4.4）。

### 4.3 冻结规则集（R1–R10）

> 以下为**预注册草案**；写入正式运行 SOP 后即为 frozen。所有阈值/分类必须在看主结果前固定。

| 编号 | 规则 |
|---|---|
| **R1**（基建失败重试一次） | 仅当失败属于**基建/环境类**（进程崩溃、沙箱创建失败、live 计算占用拒绝、DB/磁盘/OSError、机器重启；即 #7/#8 中非科学、非模型原因，由运行日志判定）时，允许**同臂、同 commit、同配置、同题集**整体重跑 **1 次**。重跑必须使用**新的 batch_id**，`arm.json.attempts` 记录 attempt=2 及原因；旧 batch 的行**不删除**。同一题最多 2 次尝试；仍失败则记为"基建未完成"，进入分母，不再重试。 |
| **R2**（模型/网络错误计数不重跑） | 模型/provider/网络类错误（`provider_transient_exhausted`、`provider_permanent`、budget 类 #5/#6）**一律计数、不整题重跑**；run 内已有的 turn/client 重试是系统固有行为，四臂一致，不视为"额外重试"。若整批因 provider 故障大面积失败（如致命认证/额度错误），该批作废（记为无效批次），修正环境后按 R1 的整体重跑规则处理，不得只补跑部分题。 |
| **R3**（禁止单臂选择性重跑） | 任何"重跑/补跑"必须对**同一题集 × 全部四臂**执行，绝不允许只重跑某组/某题的失败样本（计划 §3.1 第 68 行）。不允许按结果挑题重跑。 |
| **R4**（任务级失败不排除） | 任务级结局——`completion_no_progress`、预算耗尽、gate 拒绝导致的不完成、`undelivered`、IMP 错误断言、partial——**全部保留在矩阵**，不排除、不替换、不"再给一次机会"。 |
| **R5**（冻结后修复） | 冻结版本后若发现影响结论的缺陷：①先在 `INVALIDATIONS.jsonl` 登记受影响 `(batch_id, task_id, arm)` 与证据；②修复必须同一补丁合入**四个 arm** 并重新冻结 commit/hash；③在新日期根目录重跑受影响题 × 四臂（旧目录原样保留）；④报告同时给"修复前/修复后"矩阵并注明配对关系，**不得静默拼接**（计划 §3.1 第 69 行）。 |
| **R6**（平衡运行顺序） | 预先固定每次 campaign 的臂顺序（拉丁方轮换，见 §4.5）；同机单进程跑（一次只跑一个臂，`--concurrency` 四臂相同且记录）；固定任务枚举顺序（同一 seed 洗牌或按 tier 排序，四臂一致）；记录每臂 start/end、并发、队列等待与资源差异（计划 §3.1 第 68 行）。 |
| **R7**（人工停止批不算完整批） | 被 SIGINT/人工 `stop` 的批：目录原样保留、`batches.status=stopped`、未完成题 = `cancelled`；**不得**把它当正式结果批（不得补跑后与原批混算）。需重跑时按 R1 整体重跑并记录原因。 |
| **R8**（同一任务集/同一版本） | 正式矩阵 = 50 题 × 4 臂；任何 `--only` 子集只能用于 P0/P1 探针（`/home/ly/cloudra-p0-probe/`），**不得**作为正式数据。正式数据必须 4 臂各含全部 50 题（或明确声明缺题及原因，并进入分母）。 |
| **R9**（工作区隔离） | 每题独立沙箱、每批独立 batch_id、每臂独立目录；禁止共享 sandbox/中间结果/记忆；正式运行期间禁止其他 cloudra 进程（尤其 Web benchmark 面板）写同一数据目录（计划 §3.1 第 67 行）。 |
| **R10**（数据不可删/不可混） | 正式数据 append-only；不删除、不覆盖、不移动；探针/测试数据只允许在 `/home/ly/cloudra-p0-probe/`；任何"清理"必须由用户显式执行（`runner.py:284-285` 的既有纪律）。 |

### 4.4 执行缺口（⚠ pending，正式开跑前必须补齐）

1. **批次级 R1 重试没有代码实现**——需要正式运行 SOP/脚本（建议放在 `/mnt/c/Users/ly/bench/` 或
   `/home/ly/cloudra-p0-probe/` 之外的运行工具目录，例如 `/home/ly/cloudra-formal-<date>/tools/`），
   并在 `arm.json` 记录 attempt。
2. **基建/模型/任务失败的三分类没有机器可读标签**——批次行只有 notes 文本；建议运行后由只读分析脚本
   （读 `benchmark.db` + `runtime/runtime-v2.db` 事件）生成 `failure_taxonomy.json`，分类规则 = §3.2/§4.3。
3. **重跑/失效登记表**（`INVALIDATIONS.jsonl`）需要模板与只增不改纪律。

### 4.5 平衡顺序（预注册模板）

- 若重复数 `r = 4`（待定，见 §5.5 B3），轮次顺序用拉丁方轮换，例如：
  `R1: A→B→C→D`，`R2: B→C→D→A`，`R3: C→D→A→B`，`R4: D→A→B→C`；
  每个臂在每个时间位置各出现一次，抵消时间漂移。
- 每轮开跑前记录：臂、commit、开始时间、并发、机器负载；跑完记录 end/batch_id。
- 任务顺序：4 臂使用同一排序（建议先按 tier easy→normal→hard→impossible，tier 内按 task_id 排序；
  或四臂共享同一 seed 的洗牌），确保同题在四臂间的排队位置可比。
- 同机串行（一次一个臂），避免 4 臂并发争抢 Gaussian/xTB/LLM 额度导致不可比；若用户选择并发多臂，
  必须先做资源隔离评估并把结论写进 `arm.json`（当前默认建议**串行**）。

---

## 5. 模型配置与预算

### 5.1 配置来源链（代码事实）

`cloudra/infra/config.py:1-12` 的优先级（高→低）：CLI 参数 → 配置文件（`~/.config/cloudra/config.yaml`）
→ 环境变量（`CLOUDRA_*` 与 legacy `COORDINATOR_*`/`FOLLOWER_*`）→ 当前工作目录 `.env` → 默认值。
细节：`CloudraConfig` 的 `env_prefix="CLOUDRA_"`、嵌套分隔 `__`、`env_file=".env"`
（`config.py:216-225`）；`config_file` 字段默认 `~/.config/cloudra/config.yaml`（`config.py:229`，
可用 `CLOUDRA_CONFIG_FILE` 覆盖——HANDOVER.md 第 174 行给出用法）；legacy env 读取
`config.py:278-296`；单例入口 `get_config()` 于 `config.py:529-531`。

**benchmark CLI 的隔离行为**：`--data-dir` 固定后，`__main__.py:52-60` 会
`os.environ["CLOUDRA_DATA_DIR"] = <data-dir>/runtime` 并 `get_config().data_dir = isolated`，
因此模型/数据目录不会被 YAML 里旧 `data_dir` 带偏；**但模型名/端点/推理参数仍来自上述配置链**。

### 5.2 当前生效值（审计快照；**本报告不复制任何凭据**）

来源：`/home/ly/.config/cloudra/config.yaml`（1380 B，mtime 2026-10-18 02:53:30，
sha256 `4b3ca993128cc73c26405a8f331d045412ceffdcb1bd531d3d0fd441fae9078c`；
文件含 API key，**哈希可公开用于核对，明文不得进入报告/arm.json/commit**）：

| 槽位 | provider | model | url | context_window | timeout | reasoning_effort |
|---|---|---|---|---|---|---|
| coordinator | `deepseek` | **`deepseek-v4-flash`** | `https://api.deepseek.com` | 400000 | 300 s | `minimal` |
| follower | `deepseek` | **`deepseek-v4-flash`** | `https://api.deepseek.com` | 400000 | 300 s | `minimal` |

另：`/home/ly/bench_web_config.yaml`（sha256 `f7dba78290069a60d65c7b58a03f2a06c8896754746d9d76c587ee103172d4a4`）
是 **Web 看板专用**配置（`data_dir` 指向 `/home/ly/cloudra-bench-run-20261019/runtime`，该目录当前不存在）。
它**不是** benchmark CLI 的配置源；正式运行不得用它，也不得让 Web 面板以任何方式写正式目录（见 §6.5）。

### 5.3 provenance 记录现状（代码会写什么）

`runner.provenance_config()`（`cloudra/benchmark/runner.py:229-245`）与 CLI 批次记录
（`__main__.py:74-88`；`record_batch` 于 `runner.py:293-301`）写入 `batches.config`：

| 字段 | 现状 | 四臂差异 |
|---|---|---|
| `backend` | `"cli"` 或 `"web"` | 同 |
| `orchestration_modes` | `{task_id: mode}` | **逐臂不同**（A/D=`dag_guided`，B=`dag_record`，C=`standard`）— 唯一的真实 arm 证据 |
| `models` | 只有 `provider` + `model`（coordinator/follower） | 同 |
| `plugins` | 列表 | 同 |
| `experiment_arm` | 分支名（arm 接线新增） | 逐臂不同 |
| `error_feedback` | `full` / `brief` | A/B/C vs D |
| `scientific_feedback` | `neutralized_public_verdicts` | 仅 C |
| `tasks_dirs` / `task_ids` / `concurrency` | CLI 批次追加 | 同结构 |
| `runs` 行 | `batch_id`、`orchestration_mode`；另有 `undelivered`、各层分数、notes | — |

`provenance_config()` 源码注释写明"只记 provider/模型名，绝不记 API key"（`runner.py:230-232`）。

### 5.4 provenance 缺口（正式运行必须由 `arm.json` 补齐）

现有代码**不记录**：git commit、branch、模型版本/快照、base_url、context_window、timeout、
reasoning_effort、`--api-pool` 使用情况、任务集哈希、评估器哈希、Python/依赖版本、开始/结束的
"臂级"时间（只有 batch 时间）、运行命令。→ 全部由 §6.4 的 `arm.json` 承载。

### 5.5 未决项（**BLOCKING**）

| 编号 | 未决项 | 为什么阻塞 | 建议裁决 |
|---|---|---|---|
| **B1** | **模型版本未固定** | 当前只有模型名 `deepseek-v4-flash`，provider 侧可能滚动更新；计划要求"同一模型及版本"（§3.1 第 65 行），未固定则四臂不可比、无法复现 | 用户确认可锁定的模型 ID/快照；在 `arm.json` 记录模型名 + 提供方声明的版本；若无法锁定 → 必须在四臂同一天连续跑完并披露"版本可能漂移"风险 |
| **B2** | **预算未定** | 计划 §九第 205 行明确：当前 CLI **无任务总费用/计算资源硬上限参数**；`__main__.py:26-38` 只有 backend/only/concurrency。无预算规则 = 四臂成本不可比 | 用户给出：单题 token 上限/墙钟上限/计算资源上限/总金额上限之一或组合；并确定如何在无代码硬限的前提下执行（运行脚本监控 + 超限 kill 规则需预注册） |
| **B3** | **重复次数未定** | 计划 §3.1 第 65 行/§四第 88、97 行：重复次数在预算确定后定稿；不先承诺显著性 | 用户确定每题重复次数 `r`（建议 r≥3 并预注册平衡顺序 §4.5）；同时确定"重复运行不伪装为新增独立题"的统计口径 |
| **B4** | **凭据/配置冻结方式未定** | 配置文件含 API key；不能进 git/报告；但四臂必须用**同一份**模型配置 | 采用"redacted 快照 + `CLOUDRA_CONFIG_FILE` 指向快照 + key 从环境变量注入"方案；快照哈希写 `arm.json` |
| **B5** | **`--api-pool` 策略未定** | 若使用 pool，CLI **不记录** pool 文件/端点集合（`__main__.py:62-65` 只传给 backend，不写 batch config），四臂可复现性受损 | 裁决：正式运行**禁用** `--api-pool`（推荐），或四臂使用同一 pool 文件并把端点 label 集合（不含 key）写入 `arm.json` |

> 以上 5 项在解决前，**不得启动正式（付费）实验**；可用空后端/无成本探针继续做工程验收。

---

## 6. FORMAL DATA LAYOUT（用户强制要求：正式数据必须完整，且不得与任何其他数据混合）

### 6.1 必须原样保留、不得触碰的既有正式目录

用户明确点名的两个目录（**READ ONLY**；本审计只读打开，未写入一个字节）：

| 目录 | 大小 | 批次 / 状态 | 内容 | 风险与注意 |
|---|---|---|---|---|
| `/home/ly/cloudra-bench-run6-20261021` | 3.6 G | `batch_d7fbb0b92b284ce4`，`done`，2026-10-21 16:34 → 2026-10-22 04:30 | 20 easy 题（D1…X1）；`benchmark.db` 20 行全评分（final 0.0667–1.0，均值 0.8032）；`sandboxes/` 2.7 G；`runtime/`（runtime-v2.db **536 MB**、compute.db、artifacts、conversations 20 个）；`benchmark.log` 404 KB | **旧 schema**：`runs` 缺 `selfconsistency_score`/`undelivered` 列。当前代码 `BenchmarkDB._init()` 检测列集不同会**重建 runs 表**（`runner.py:262-281`）——用可写连接打开即等于改写正式数据。**只能** `sqlite3 file:...?mode=ro&immutable=1` 只读查询，或先复制再打开 |
| `/home/ly/cloudra-bench-full-20261022` | 1.5 G | `batch_a7fef4e786b84d55`，**`stopped`**，2026-10-22 16:38 → 20:49 | 50 题全量批次（4 个 tasks-dir）；50 行中 **46 行 `cancelled by batch stop`（未评分）、4 行评分**；`runtime/` 完整 | 该批被人工停止，**不是完整实验批**；均值无意义（§3.3）。同样只读打开；其 `benchmark.db` 是当前 schema |

补充（不属于四臂正式矩阵，但同样**不得删除/移动**，仅作历史与探针隔离）：
`/home/ly/cloudra-bench-run4-20261020`（1.9 G）、`/home/ly/cloudra-bench-run5-20261021`（33 M）、
`/home/ly/cloudra-bench-run7-20261022`（4.0 M）、`/home/ly/cloudra-bench-dryrun-20261021`（196 K）。

**这两个既有正式目录与四臂实验的关系**：它们的 `experiment_arm` 均为空、`orchestration_mode` 只有
`dag_guided`（历史单臂标签），**不能**被追认为 A/B/C/D 任一组正式数据；四臂正式数据必须另建目录（§6.2）。
既有目录只作为"历史证据/回归参照"，任何新实验不得写入其中（包括 benchmark.db、runtime、日志）。

### 6.2 提议的正式数据布局

```text
/home/ly/cloudra-formal-<YYYYMMDD>/                  # 一次冻结 campaign 的根（日期取实际开跑日）
├── MANIFEST.md                                      # campaign 说明、冻结 commit 表、运行顺序、批准记录
├── MANIFEST.sha256                                  # 根级关键文件哈希（arm.json/commit.txt/config 快照…）
├── INVALIDATIONS.jsonl                              # 只增：冻结后失效/重跑登记（R5）
├── config.snapshot.redacted.yaml                    # 模型配置快照（去掉 key；key 走环境变量）
├── tools/                                           # 只读运行/分析脚本（可复用，不含数据）
│   ├── launch_arm.sh                                # 记录 arm.json 的统一启动器（待建，见 §4.4）
│   └── analyze_rows.py                              # 只读：按 §3.3 分类行、输出 failure_taxonomy.json
│
├── A/                                               # = benchmark/arm-guided
│   ├── arm.json                                     # 见 §6.4（commit/mode/model/batch/时间/task-set hash…）
│   ├── commit.txt                                   # git rev-parse HEAD + branch + git status 摘要
│   ├── benchmark.db                                 # append-only；每 attempt 一个 batch
│   ├── benchmark.log                                # 该臂运行 stdout/stderr（含启动命令与时间）
│   ├── sandboxes/<task_id>/<batch_id>/…             # 代码生成：按批分目录，永不复用/删除
│   ├── runtime/                                     # 代码生成：runtime-v2.db, compute.db, conversations/, artifacts/
│   └── environment.json                             # python/依赖/rdkit/uv.lock/cloudra.__file__/PATH/版本
├── B/  …（同上，= benchmark/arm-record）
├── C/  …（同上，= benchmark/arm-standard）
└── D/  …（同上，= benchmark/arm-guided-brief-errors）
```

要点：
- **一臂一目录**，目录名 A/B/C/D 与分支名映射写死在 `MANIFEST.md`；
- `.benchmark.pid` 由启动脚本写，属运行态文件，可保留（不影响审计）；
- `runtime/` 不是可选项：`agent.completion_gate`、`run.finished.failure_kind`、失败分类证据都在
  `runtime/runtime-v2.db`（`backend.py:60-63,117-125` 只做 append 持久化），没有它就无法重建
  §3.2 的 #1/#2/#5/#6 标签；
- 探针/测试**绝不**放进 `cloudra-formal-*`（见 §6.6）。

### 6.3 命名/复用规则（不可协商）

1. 每个 campaign 新开 `/home/ly/cloudra-formal-<date>/`；**已存在的目录不复用、不覆盖**；
2. 每个臂一个子目录；**禁止把两个臂写进同一目录**，禁止把探针数据、旧 run 数据、手工文件拷入正式目录；
3. 目录内 **append-only**：允许同一臂追加新的 attempt/batch（`benchmark.db` 追加行、沙箱按 batch 分目录），
   **禁止**删除/改写既有行、既有沙箱、既有日志；
4. campaign 结束后 `chmod -R a-w` 冻结（保留可读）；需要再次运行时开新日期目录；
5. 任何"清理/压缩/迁移"必须由用户显式执行（代码纪律见 `runner.py:284-285`、`batch.py:440-442,471-474`）；
6. 只读复核本目录时：`sqlite3` 用 `?mode=ro&immutable=1`，**不要**用项目代码里会触发 DDL 迁移的
   `BenchmarkDB` 打开正式库（§6.1 风险）。

### 6.4 `arm.json` 必备字段（provenance）

由启动器在开跑前写 baseline 部分、结束时补 final 部分；**每次 attempt 一条**：

```json
{
  "schema_version": 1,
  "campaign": "p0-formal-<YYYYMMDD>",
  "arm": "A",
  "experiment_arm": "benchmark/arm-guided",
  "branch": "benchmark/arm-guided",
  "commit": "<git rev-parse HEAD，40 位>",
  "git_dirty": false,
  "git_status_short": "<除 run.sh 外应为空>",
  "mode": "dag_guided",
  "orchestration_modes": {"D1": "dag_guided", "...": "..."},
  "error_feedback": "full",
  "scientific_feedback": null,
  "backend": "runtime_v2",
  "model": {
    "coordinator": {"provider": "deepseek", "model": "deepseek-v4-flash",
                    "base_url_host": "api.deepseek.com", "context_window": 400000,
                    "timeout_s": 300, "reasoning_effort": "minimal"},
    "follower": {"provider": "deepseek", "model": "deepseek-v4-flash",
                 "base_url_host": "api.deepseek.com", "context_window": 400000,
                 "timeout_s": 300, "reasoning_effort": "minimal"}
  },
  "config_file": "config.snapshot.redacted.yaml",
  "config_sha256_used": "<实际读取文件的 sha256>",
  "api_pool": null,
  "concurrency": 6,
  "only": null,
  "task_bank": {
    "tasks_dirs": ["ideapool/tasks/easy", "ideapool/tasks/normal",
                   "ideapool/tasks/hard", "ideapool/tasks/impossible"],
    "counts": {"easy": 20, "normal": 10, "hard": 10, "impossible": 10, "total": 50},
    "sha256": "a9a9b17a36c4bfc6d4df7fd46e20512f496c3bb06398a576280582f5d103ad18",
    "sha256_h1": "5db51268e1cf605d693151db2a60bbff17891a80f2d4ba77cf216ff0c4a66aa6"
  },
  "evaluator": {
    "composite_weights": {"graph": 0.1, "self_consistency": 0.3, "accuracy": 0.6},
    "files_sha256": {"cloudra/benchmark/accuracy.py": "fa0676…", "…": "…"},
    "rubric_source": "task JSON (embedded)"
  },
  "environment": {
    "host": "<hostname>", "os": "Ubuntu (WSL)", "python": "3.12.3",
    "rdkit": "2026.09.1", "uv_lock_sha256": "7412dc94…",
    "cloudra_module": "/home/ly/cloudra-arm-guided/cloudra/__init__.py",
    "entrypoint_run_sh_sha256": "0501ea24a42519cfacb929aeb45708e438bfa8e5b5b5c87bbe6f81bf7a55be66",
    "path": "<g16/xtb PATH；含 /home/ly/bin:/home/ly/g16:/home/ly/xtb-6.5.0/bin>",
    "g16_binary": "/home/ly/bin/g16", "xtb_binary": "/home/ly/xtb-6.5.0/bin/xtb",
    "orca": "absent"
  },
  "command": "<完整启动命令（已脱敏）>",
  "started_at": "2026-10-24T02:00:00+08:00",
  "finished_at": "2026-10-26T10:00:00+08:00",
  "batch_ids": ["batch_..."],
  "attempts": [
    {"attempt": 1, "batch_id": "batch_...", "started_at": "...", "finished_at": "...",
     "status": "done", "rows_scored": 50, "rows_not_scored": 0},
    {"attempt": 2, "batch_id": "batch_...", "reason": "infra failure: ...", "…": "…"}
  ],
  "supersedes": null
}
```

必含（任务书要求的最小集 + 审计必需）：
`commit`、`experiment_arm`、`mode`（含 `orchestration_modes` 全量映射）、`model`（含 provider/model/
上下文/超时/推理强度）、`concurrency`、`batch_id`（可多个）、`started_at/finished_at`、**task-set 哈希**、
`evaluator.files_sha256`、`environment`（python/依赖/`cloudra.__file__`/入口脚本哈希/PATH/计算后端）、
`attempts`。凭据类字段（API key、完整 token）**禁止**出现。

### 6.5 正式运行纪律（与布局配套）

1. **唯一入口**：`/home/ly/cloudra-arm-<arm>/run.sh`（四臂同一脚本，sha256
   `0501ea24a42519cfacb929aeb45708e438bfa8e5b5b5c87bbe6f81bf7a55be66`；未跟踪文件，故必须
   copy/hash 进正式目录，否则 commit 里没有它）。
2. **启动前检查**（写进 `arm.json`）：
   - `git -C <arm> rev-parse HEAD` = 冻结 commit；`git status --porcelain` 只有 `run.sh`；
   - `python -c "import cloudra; print(cloudra.__file__)"` 指向该臂目录（防 PYTHONPATH 失效）；
   - `python -m cloudra.benchmark --help` 四臂输出逐字节一致（已由 `00_lead_checks.md` §1 验证）；
   - 题库 H2 哈希 = §1.2 值；
   - 评分文件 sha256 表 = §2.6 值；
   - **无其他 cloudra 进程**占用（`pgrep -af cloudra.benchmark`；Web 面板可用独立数据目录，但不得指向正式目录）。
3. **配置**：`CLOUDRA_CONFIG_FILE=<campaign>/config.snapshot.redacted.yaml`；key 从环境变量注入
   （`COORDINATOR_KEY`/`FOLLOWER_KEY` 或 `CLOUDRA_*`）；`arm.json.config_sha256_used` 记录实际文件哈希。
4. **一次一个臂**（建议），`--concurrency` 四臂固定（如 6），`--only` 为空（全 50 题）。
5. 结束后：写 `commit.txt`、补 `arm.json`、`chmod -R a-w <arm 目录>`；`MANIFEST.sha256` 更新。
6. 崩溃/中断：保留目录与日志；按 §4.3 R1/R7 处理；禁止清空重跑目录。

### 6.6 探针 / 测试数据（只允许在这里）

- 探针根目录：**`/home/ly/cloudra-p0-probe/`**。
- 现存（本 P0 会话产生，均为 `--backend none` 无模型空后端探针，可随时清理，但**永不并入正式目录**）：
  `cloudra-p0-probe/{guided,record,standard,brief-errors}/probe/{benchmark.db,sandboxes/}` + `probe.log`，
  以及并行 P0 任务的 `cloudra-p0-probe/p0-behavior/`。E1 探针结果四臂一致：
  `final=-1.000, graph=0.000, selfcons=0, accuracy=0.000, undelivered=1`（见 `00_lead_checks.md` §4）。
- 探针/单测/冒烟（`--backend none`、`--only`、`--concurrency 1`）一律不得写 `cloudra-formal-*`；
  正式目录里出现任何非正式批行/沙箱，即视为数据污染。

### 6.7 容量估算

- 参考：run6（20 easy 题）整目录 3.6 G，其中 sandbox 2.7 G、runtime-v2.db 0.54 G；
- 单臂全 50 题（含 hard/IMP 的 QM 日志）粗估 **8–15 G**；四臂 **32–60 G**；
- 当前 `/home/ly` 可用 **714 G**，够用；但正式 campaign 前应记录 `df` 快照并预留 ≥2× 估算空间。

### 6.8 报告统计口径（必须与数据分类绑定）

报告至少给两套分母（计划 §四第 90 行）：
1. **完整性分母**：计划题数 50 × 4 臂 = 200；实际启动、已交付、未评分、可独立评估各多少；
2. **评分分母**：仅"已评分行"（§3.3 第三/二类）进入分数统计；**未评分行单列**，不得以 0 分混入均值；
3. 另列"重复轮次"矩阵（r 轮 × 200 配对），重复不冒充新题。

---

## 7. 冻结检查表（Freeze checklist）

| # | 冻结项 | 状态 | 证据 |
|---|---|---|---|
| 1 | 题库：50 题、id/计数、H1+H2 哈希、git commit | **frozen** | §1.1–1.4；`24d059d7`；H2 `a9a9b17a…`；四臂 H1 全同 |
| 2 | 题库：四臂无改动（`git diff` 空） | **frozen** | §1.4 |
| 3 | 评分代码：accuracy/selfconsistency/graph_similarity/schema/integrity/evidence_search/delivery_evidence/barrier_evidence | **frozen** | §2.6 哈希表（四臂全同） |
| 4 | 评分接线 `runner.py`：逐臂 `ABLATION_ARM` + provenance | **frozen（逐臂哈希已记录）** | §2.6；四臂 4 个不同哈希，diff 仅接线 |
| 5 | 复合权重 0.1/0.3/0.6、短路规则、fail-loud | **frozen** | §2.2；`runner.py:150-152,474-514` |
| 6 | rubric 默认值 / sigma / 1-1 匹配 / 发现回退 | **frozen** | §2.3–2.5；`schema.py:253-325`；`accuracy.py:280-386`；`evidence_search.py:28-33` |
| 7 | 评估器运行环境（python/rdkit/依赖/uv.lock/`cloudra.__file__` 校验） | **pending** | §2.7：共享 editable `.venv` + PYTHONPATH 纪律；需写入 launch 检查并记录 |
| 8 | 失败分类（全部终态/标签 + file:line） | **frozen** | §3.2–3.3（12 类映射，均为只读代码事实） |
| 9 | 行分类口径（未评分 vs 已评分未交付 vs 已评分） | **frozen** | §3.3；§6.8 |
| 10 | 重试/排除规则 R1–R10 | **pending（草案已冻结文字，待批准 + 工具）** | §4.3；§4.4 执行缺口 |
| 11 | 平衡运行顺序（拉丁方模板） | **pending（需用户确认 r 后定稿）** | §4.5 |
| 12 | 模型配置：当前取值与来源链 | **frozen（现状快照）** | §5.1–5.2；config sha256 `4b3ca993…` |
| 13 | 模型版本固定 | **blocked — B1** | §5.5 |
| 14 | 预算规则（金额/资源/单题停止） | **blocked — B2** | §5.5；CLI 无预算参数（`__main__.py:26-38`；计划 §九第 205 行） |
| 15 | 重复次数 r | **blocked — B3** | §5.5 |
| 16 | 配置/凭据冻结方式（redacted 快照 + env key） | **blocked — B4** | §5.5 |
| 17 | `--api-pool` 使用策略 | **blocked — B5（建议禁用）** | §5.5；provenance 缺口 |
| 18 | provenance 记录（现有 batches/runs 字段） | **frozen（已知范围）** | §5.3 |
| 19 | `arm.json`/`commit.txt`/`environment.json` 补齐现有 provenance 缺口 | **pending（模板已定义，启动器待建）** | §6.4；§4.4 |
| 20 | 正式数据布局（一臂一目录、append-only、不可混） | **frozen（本文件定义）** | §6.2–6.3 |
| 21 | 既有正式数据保护（run6 / full-20261022） | **frozen（只读清单 + 旧 schema 风险）** | §6.1 |
| 22 | 探针隔离（`/home/ly/cloudra-p0-probe/`） | **frozen（现状已隔离）** | §6.6；本会话未写入任何正式目录 |
| 23 | 计算环境快照（g16/xtb/ORCA；PATH；版本） | **pending** | §0.3：g16 包装脚本/xtb 6.5.0/ORCA absent；Gaussian revision 未记录，需 `environment.json` 采集 |
| 24 | 失败分类聚合脚本（只读分析 benchmark.db + runtime-v2.db） | **pending** | §4.4；否则 §3.2 的 run 级标签无法批量复算 |

### 7.1 阻塞项汇总（开跑前必须解除）

| 阻塞 | 内容 | 解除条件 |
|---|---|---|
| **B1** | 模型版本未固定 | 用户/Lead 给出可锁定模型版本或明确"不可锁定 + 同日连续跑"替代方案 |
| **B2** | 预算（金额/资源/单题停止）未定 | 用户给出预算规则；并确定无代码硬限下的执行方式 |
| **B3** | 重复次数 r 未定 | 用户给出 r；据 §4.5 定稿顺序与统计口径 |
| **B4** | 配置/凭据冻结方式未定 | 批准 redacted 快照 + `CLOUDRA_CONFIG_FILE` + env key 方案 |
| **B5** | `--api-pool` 策略未定 | 裁决禁用或"同 pool + 记录 label 集合" |

### 7.2 建议的下一步（不消耗模型/算力）

1. Lead 批准 §4.3 规则与 §6.2 布局 → 本文件升为 frozen；
2. 编写 `tools/launch_arm.sh`（记录 arm.json/environment.json/commit.txt、启动前自检、结束后 chmod）与
   `tools/analyze_rows.py`（§3.3 分类、失败分类聚合、分母统计）；
3. 空后端探针跑通新布局（仍只写 `/home/ly/cloudra-p0-probe/`，先验证脚本，再建正式目录）；
4. 用户裁决 B1–B5 后，按 §4.5 顺序启动正式 campaign。

---

## 8. 复现命令（只读）

```bash
# 题库身份（H1）
cd /home/ly/cloudra-bench-20261019
find ideapool/tasks -name '*.json' | sort | xargs sha256sum | sha256sum

# 四臂题库/评分哈希对比（只读）
for d in /home/ly/cloudra-bench-20261019 /home/ly/cloudra-arm-{guided,record,standard,brief-errors}; do
  ( cd "$d" && find ideapool/tasks -name '*.json' | sort | xargs sha256sum | sha256sum )
done

# 正式数据只读查询（禁止可写打开！）
python3 - <<'PY'
import sqlite3
db = "/home/ly/cloudra-bench-run6-20261021/benchmark.db"
con = sqlite3.connect(f"file:{db}?mode=ro&immutable=1", uri=True)
print(con.execute("select batch_id,status from batches").fetchall())
print(con.execute("select count(*) from runs").fetchall())
PY
```

**审计边界声明**：本报告只读核对代码与数据；未切换分支、未改产品代码、未运行 LLM/QM 任务、
未向 `/home/ly/cloudra-bench-run6-20261021`、`/home/ly/cloudra-bench-full-20261022` 或任何正式目录
写入任何内容；唯一写入是本文件。
