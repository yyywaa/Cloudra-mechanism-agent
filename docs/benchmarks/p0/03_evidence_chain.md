# P0-3 证据链、fallback 与评分公平性审计

> 任务：`task-3`（P0 工程验收与公平性审计，零正式预算）
> 审计对象：`A=benchmark/arm-guided`、`B=benchmark/arm-record`、`C=benchmark/arm-standard`、`D=benchmark/arm-guided-brief-errors`
> 工作库：`/home/ly/cloudra-bench-20261019`（共享 repo，未切分支，当前分支 `docs/p0-acceptance`；本报告是唯一写入文件）
> 四个 arm checkout：`/home/ly/cloudra-arm-{guided,record,standard,brief-errors}`（均 clean，仅未跟踪 `run.sh`）
> 现有正式数据：`/home/ly/cloudra-bench-run6-20261021`、`/home/ly/cloudra-bench-full-20261022`（只读，本审计未写入）
> 探针数据：`/home/ly/cloudra-p0-probe/p0-evidence/`（仅此目录；无 LLM、无付费、无远端计算）
> 审计方法：`git cat-file` 取分支头文件哈希；AST 级函数哈希；分支间 `git diff`；只读 SQLite；no-model 评分器一致性/回放探针
> 审计日期：2026-10-24

**结论先行：`scorer identical = YES`。** 六个评分器文件中 5 个在四臂逐字节相同；`runner.py` 的差异仅为“本分支 arm 接线/来源记录”，评分函数（`score_sandbox`、`derived_barrier_graph`、`_apply_declared_barriers`、`run_task`）函数级哈希四臂完全一致；用真实已完成交付物做跨臂回放，四臂给出与历史 `benchmark.db` 完全相同的分数。**未发现影响评分的差异，不构成 fairness violation。**

---

## 0. 冻结快照与审计边界

### 0.1 版本快照（2026-10-24 01:41 采样）

| 对象 | 分支 | HEAD commit |
| --- | --- | --- |
| 共享 repo | `docs/p0-acceptance`（不切换） | `1e6d953f998848b2499f7a5e69df22842c3fd869`（= master） |
| A 完整版 | `benchmark/arm-guided` | `e67ef30abd8807297a7c4f095836eee3ee04bb77` |
| B 记录版 | `benchmark/arm-record` | `058fdc82907bc6f4a0dbf60a62dbc11e8865c701` |
| C 标准/判定模糊化版 | `benchmark/arm-standard` | `79ca80bf8c3c2ea7a48e2cab1f8455a2fcccd55d` |
| D 简略报错完整版 | `benchmark/arm-guided-brief-errors` | `0b81c2625fbf9a62e221deebe1b62ce74bd2330e` |

- 四臂两两 `merge-base` 均为 master `1e6d953f...`；四臂均包含计划中声明的共同产品基线 `8c568ca6753ecf2cd40a90a8f0f8b5c8e19dd1d2`（见 `ideapool/cloudra_four_arm_experiment_plan.md` §0/§9）。四臂并行合并了 master 的两个 IDPP 修复（`e28d45e0`、`1e6d953f`），即**产品基线一致**。
- 四臂 checkout 与对应分支头 commit 完全一致、工作树 clean（只有未跟踪 `run.sh`）。正式运行仍须记录 `git rev-parse HEAD` 与 `git status`；`run.sh` 不入库，冻结时应单独登记内容或删除。

### 0.2 只读约束

- 共享 repo 未切分支、未改产品代码；四个 arm checkout 只读访问；现有正式数据目录只读（SQLite 以 `mode=ro` 打开）。
- 探针脚本位于 `/mnt/c/Users/ly/bench/`（`p0_scorer_parity.py`、`p0_replay_parity.py`、`scorer_*` 等）；全部无模型、无付费、无网络远端计算调用。
- 唯一写入的仓库文件：本报告。

---

## 1. 评分器身份（scorer identity）

### 1.1 六文件 sha256（分支头，`git cat-file -p <branch>:<path> | sha256sum`）

| 文件 | A guided | B record | C standard | D brief-errors | 一致? |
| --- | --- | --- | --- | --- | --- |
| `cloudra/benchmark/accuracy.py` | `fa0676a97def2118…` | `fa0676a97def2118…` | `fa0676a97def2118…` | `fa0676a97def2118…` | 是 |
| `cloudra/benchmark/selfconsistency.py` | `42144630396896f7…` | `42144630396896f7…` | `42144630396896f7…` | `42144630396896f7…` | 是 |
| `cloudra/benchmark/evidence_search.py` | `a5b382e4bd9d6ff8…` | `a5b382e4bd9d6ff8…` | `a5b382e4bd9d6ff8…` | `a5b382e4bd9d6ff8…` | 是 |
| `cloudra/benchmark/integrity.py` | `d2b8404149a2b4ab…` | `d2b8404149a2b4ab…` | `d2b8404149a2b4ab…` | `d2b8404149a2b4ab…` | 是 |
| `cloudra/benchmark/delivery_evidence.py` | `1dd5631e408807ec…` | `1dd5631e408807ec…` | `1dd5631e408807ec…` | `1dd5631e408807ec…` | 是 |
| `cloudra/benchmark/runner.py` | `0dfee4319be85134…` | `29d0b4db6d291592…` | `a007d133aa4c6c85…` | `7aef6234029b51bc…` | **否（仅接线/来源记录）** |

完整 64 位哈希见附录 A。

### 1.2 `runner.py` 差异逐 hunk 判定

四臂 `runner.py` 的差异只有以下 5 类（A→B/C/D、master→各臂均已核对）：

| 差异 | A | B | C | D | 是否影响评分 |
| --- | --- | --- | --- | --- | --- |
| `ABLATION_ARM` 常量（本分支臂） | `DAG_GUIDED` | `DAG_RECORD` | `STANDARD` | `DAG_GUIDED` | 否，是实验处理本身 |
| `provenance_config()["experiment_arm"]` | `benchmark/arm-guided` | `benchmark/arm-record` | `benchmark/arm-standard` | `benchmark/arm-guided-brief-errors` | 否，批次来源元数据 |
| `provenance_config()["error_feedback"]` | `full` | `full` | `full` | `brief` | 否，批次来源元数据 |
| `provenance_config()["scientific_feedback"]` | 无键 | 无键 | `neutralized_public_verdicts` | 无键 | 否，批次来源元数据 |
| `RunResult.orchestration_mode` 来源 | `ABLATION_ARM.value` | 同 | 同 | 同 | 否，行级标签；评分不读该字段 |

另外一处注释改动（`orchestration_mode` 字段注释）与新增 `from cloudra.runtime_v2.schemas import OrchestrationMode` 均无行为影响。master→各臂的 `task_project_settings` 把 `orchestration_mode` 从 `task.prompt.orchestration_mode` 改为 baked `ABLATION_ARM.value`，属于“实验处理固定到分支”的必要接线，不是评分改动。

### 1.3 评分相关函数的 AST 级哈希（消除“hunk 看起来无害”的主观性）

对四臂 `runner.py` 用 `ast` 提取函数源码后 sha256 前 16 位：

| 函数 | A | B | C | D | 一致? |
| --- | --- | --- | --- | --- | --- |
| `score_sandbox`（评分入口：读图+日志→四层流水线） | `9a12a2cc2c998d1c` | `9a12a2cc2c998d1c` | `9a12a2cc2c998d1c` | `9a12a2cc2c998d1c` | 是 |
| `run_task`（沙箱批次目录→后端→打分→落库） | `31e5d434a56c8929` | 同 | 同 | 同 | 是 |
| `_run_one_guarded`（单题异常落零分行） | `b3125bbe220d079d` | 同 | 同 | 同 | 是 |
| `derived_barrier_graph`（节点能量推边能垒） | `d33b21eaac9ff4ad` | 同 | 同 | 同 | 是 |
| `_apply_declared_barriers`（把推导能垒带入 barrier evidence） | `c22bdce325da6243` | 同 | 同 | 同 | 是 |
| `task_project_settings`（任务设置，文本同、常量值按臂） | `194df705933c1dec` | 同 | 同 | 同 | 是（文本）；常量值按臂是处理 |
| `provenance_config`（批次来源） | `6505d82747bd931a` | `4a5fd106954ed74f` | `802bbd01fd711c90` | `26134704f6a2d449` | 否（元数据，见 1.2） |

模块级评分常量四臂相同：`W_GRAPH=0.1`、`W_SELFCONSISTENCY=0.3`、`W_ACCURACY=0.6`（`cloudra/benchmark/runner.py:151-153`；`score_sandbox` 里 `final` 公式与零证据倒扣、fail-loud 短路逻辑也都在该同哈希函数内）。

### 1.4 评分包与题库的全量一致性

- `cloudra/benchmark/` 全目录共 38 个文件：**除 `runner.py` 外，四臂逐文件 sha256 全部相同**；`backend.py`（`e08a73d3…`）与 `batch.py`（`a6da71d4…`）四臂相同（相对 master 有接线差异，但四臂之间无差异）。
- 题库 `ideapool/tasks/`：四臂均 50 个文件，整包 `bank_sha256=260c1ddc448bbda22fa5d2d316308fa9cf1e2fa3948c3337ee21aac593854ea2`，**四臂完全相同**。
- 结论：任务输入、评分代码、评分常量、评分数据通道在四臂间没有除“臂接线”之外的不同。

### 1.5 经验性一致性探针（no-model，可复现）

**(a) 合成分数一致性**（`/mnt/c/Users/ly/bench/p0_scorer_parity.py`；数据在 `/home/ly/cloudra-p0-probe/p0-evidence/scorer-parity/<arm>/`）
对 E1 构造 4 种**四臂逐字节相同**的沙箱，用各自 checkout 的评分器评分：

| 沙箱变体 | A/B/C/D 结果是否相同 | graph | selfcons | undelivered | accuracy | final |
| --- | --- | --- | --- | --- | --- | --- |
| `empty`（空沙箱） | 是（notes 也逐条相同） | 0.0 | false | 1 | 0.0 | -1.0 |
| `gold_graph`（写入 gold 图，无日志） | 是 | 0.0 | false | 1 | 0.0 | -1.0 |
| `gold_marker`（gold 图 + 最小 `.cloudra/mechanism_evidence.json`） | 是 | 0.0 | false | **0** | 0.0 | -1.0 |
| `nodes_only`（gold 图去掉 edges，模拟 partial 交付） | 是 | 0.0 | false | 1 | 0.0 | -1.0 |

四臂 JSON summary 规范化后 `sha256 = d87288fa271911d5cbe454bbfb52d1439e11fbe703c3ead33aa696f34c7769ef`（四臂相同）。

**(b) 真实交付物跨臂回放**（`/mnt/c/Users/ly/bench/p0_replay_parity.py`；数据在 `.../p0-evidence/replay-parity/<arm>/`）
取 run6 已完成的 A 臂 E1 沙箱（`/home/ly/cloudra-bench-run6-20261021/sandboxes/E1/batch_d7fbb0b92b284ce4`，802 文件，历史行 `final=1.0/graph=1.0/selfcons=1/accuracy=0.9999726…`），硬链接复制后分别用四臂评分器重算：

| 变体 | 四臂结果 | graph | selfcons | selfcons_score | undelivered | accuracy | final |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `as_is`（带 `.cloudra/mechanism_evidence.json`） | 完全相同 | 1.0 | true | 1.0 | false | 0.999972638934 | **1.0** |
| `no_publish`（删除该文件，模拟 B/C 不发布） | 完全相同 | 1.0 | true | 1.0 | **true** | 0.999972638934 | **1.0** |

- 四臂 summary 规范化 `sha256 = 5a198d1542df567151d35748fdcc6eaa5de8ff85f58d90da76d70dee7fda868c`（四臂相同）。
- `as_is` 与 run6 历史 DB 行**逐字段一致**（`graph_score=1.0`、`selfconsistency_passed=1`、`accuracy_score=0.9999726389344515`、`final=1.0`），证明离线评估链可复现、且回放没有引入偏差。
- 该结果同时证明：删除 `.cloudra/mechanism_evidence.json` 后，`selfconsistency` 仍为 1.0（原生日志 fallback 接管），分数不变，只翻转 `undelivered` 标签（见 §3、§4）。

### 1.6 Verdict（item 1）

**PASS（无 fairness violation）。**
- 5/6 评分器文件四臂逐字节相同；`runner.py` 仅 arm 接线/来源记录差异，且评分函数与常量函数级同哈希。
- 两个独立探针（合成 & 真实交付物回放）都给出四臂逐字段相同的结果。
- 需在论文/冻结清单披露的**非评分差异**：`provenance_config()` 的 `experiment_arm`/`error_feedback`/`scientific_feedback` 字段按臂不同（这是实验来源，不是评分逻辑）；**A 与 D 的 `runs.orchestration_mode` 都是 `dag_guided`**，离线分臂归因必须读 `batches.config.experiment_arm` 或按独立数据目录，不能只看 `runs` 表。

---

## 2. 各臂证据保留 / 发布路径

### 2.1 证据 writer 代码定位（先看“谁写”，再看“哪臂写”）

| 证据产物 | 写入代码 | 写入时机 |
| --- | --- | --- |
| `mechanism_graph.json`（沙箱根） | **agent 自写**（`write`/`edit` 工具；任务 prompt 要求维护，如 `cloudra/benchmark/schema.py:191` 与 `gen_*_tasks.py`） | agent 任意时机（所有臂都有 write 权限/工具） |
| `.cloudra/evidence/<sha16>_<name>`（内容寻址不可变快照，含 IRC sidecar bundle） | `cloudra/dag/evidence_ingest.py:83-114` `snapshot_evidence_file()` | 由 DAG 证据提交工具、TS pipeline 调用（见 2.2） |
| `.cloudra/mechanism_evidence.json`（程序编写的 per-step endpoint 绑定） | `cloudra/benchmark/delivery_evidence.py:76-86` `write_step_endpoint_evidence()`；**唯一调用点** `cloudra/dag/stop_audit.py:535-538`（guided settlement） | 只有 guided 结算 `commit_stop()` 成功时 |
| 原始 QM 日志（`.log/.out`）、输入（`.gjf/.com/.inp`）、chk/xyz、`.cloudra/calc-*.out.log`、`guard-*.log` | 计算执行器按 `workdir`（= workspace 内输入文件所在目录）写入：`cloudra/runtime/monitor.py:616-645`、`cloudra/infra/compute_utils.py:126-142` | 计算运行即写；**benchmark 包无删除代码**（`cloudra/benchmark/` 内 `rmtree/os.remove/unlink` 零命中），沙箱按 batch 子目录 append-only（`runner.py:9-16`、`393-397`、`524-530`） |
| `runs`/`batches` 行（评分结果与来源） | `runner.py:255-338` `BenchmarkDB` | 每题结束；append-only |
| runtime 事件/会话/DAG 账本 | `<data-dir>/runtime/runtime-v2.db`、`<data-dir>/runtime/conversations/<project>/tasks/database.db`、`<data-dir>/runtime/compute.db`、`<data-dir>/runtime/artifacts/`（`benchmark/__main__.py:56-72`；`persistence/paths.py`） | 运行即写；backend 事件持久化 `benchmark/backend.py:106-125` |

### 2.2 各臂实际写/不写

| 产物 | A guided | B record | C standard | D brief-errors |
| --- | --- | --- | --- | --- |
| `mechanism_graph.json`（agent 自写） | 可写（工具/权限都在） | 可写 | 可写（DAG 工具被隐藏，但 agent 仍被 prompt 要求手写该文件） | 可写 |
| `.cloudra/evidence/` 快照 | 写：`dag_submit_*_evidence.py:109-114/144-192`（guided 提交）+ `tools/core/ts_process.py:2608/2769/3211`（TS pipeline 阶段） | 写：record 模式提交仍执行 `snapshot_evidence_file`（`dag_submit_species_evidence.py:122`、`dag_submit_step_evidence.py:157/219` record 分支只跳过“失败拒绝/送审”，快照照做） | 写：DAG 工具隐藏、`dag_submit_*` 不可用；但 TS pipeline 的 `snapshot_evidence_file` 调用未改（A→C `ts_process.py` diff 中无 snapshot 行） | 写：同 A（`stop_audit.py`、`ts_process.py` 快照代码与 A 相同） |
| `.cloudra/mechanism_evidence.json` | **写**（guided settlement：`stop_audit.py:522-538`，artifact 非空时） | **不写**：audit 在 `stop_audit.py:277-281` 提前 `allow_final`，commit 在 `511-515` 记录 disposition 后直接 return，永不调用 artifact/publication | **不写**：`dag_stage.py:58-61` 在 standard 模式 `_controller()` 返回 `None`，`audit_run_end` 返回 `None`（`87-108`）；`DagController.enabled=False`（`controller.py:64-66`）— 根本没有 DAG 结算路径 | **写**（同 A：`stop_audit.py` 与 A 同哈希 `282db1f3…`，仅错误文本投影不同） |
| DAG 交付状态记录 | `dag_delivery_dispositions` 行（含 artifact snapshot_path） | 记录 disposition + coverage report，但无 artifact（`stop_audit.py:511-515`；`dag/store.py:242-281`） | **无** DAG disposition 行 | 同 A |
| `undelivered`（benchmark 行） | 有 publication 时 false | **结构上恒为 true** | **结构上恒为 true** | 同 A |

补充：
- B/C 的“跳过发布”是**设计行为**且只跳过 guided 结算的“endpoint 绑定发布”这一步；B 仍通过 DAG record 工具写 `.cloudra/evidence/` 快照与 DB evidence 行（`dag_submit_*` record 分支），C 仍可通过 TS pipeline 写快照。**没有任何一臂丢失原始 QM 日志或 agent 手写的 `mechanism_graph.json`。**
- A/D 在 `user_terminated` 结算、崩溃/取消、或 artifact 为 `None`（如图不存在）时也不会写 `mechanism_evidence.json`；因此“没有该文件”≠“没有交付”。旧数据中 run6 20 题有 16 题该文件存在（D4/G2/G3/L2 缺失），full 50 题只有 4 题存在（该目录是早期只跑 10 个题目的尝试），这就是该语义的经验例证。

### 2.3 离线可读性（“这条链在磁盘上剩下什么”）

正式四臂运行建议数据布局（与 `benchmark/__main__.py` 一致）下，B/C 跳过发布后**仍可离线审计**的内容：

1. `<data>/sandboxes/<task>/<batch>/`：`mechanism_graph.json`（若有）、全部原始 QM 日志/输入/chk、`.cloudra/evidence/` 快照、`.cloudra/calc-*.out.log`、`guard-*.log`、TS `process.json`/`declare.json`、`PROCESS.md`。
2. `<data>/runtime/runtime-v2.db`：全量事件（除 `llm.chunk`），含 `agent.completion_gate`（action/source/**basis**）、工具事件、通知事件 — 这是 B/C 交付状态的主要离线事实源。
3. `<data>/runtime/conversations/<project>/tasks/database.db`：DAG store（`dag_graphs/dag_nodes/dag_edges/dag_evidence`、`dag_delivery_dispositions` 等）；A/B/D 有 disposition 行，C 无。
4. `<data>/runtime/compute.db`：计算作业与 TS pipeline 的内部科学账本（C/D 的投影只改公开副本，不改该库）。
5. `<data>/runtime/artifacts/`：媒体/工具产物快照。
6. `<data>/benchmark.db`：评分行（`graph_score`/`selfconsistency_*`/`undelivered`/`accuracy_score`/`final_score`/`notes`/`batch_id`/`orchestration_mode`）+ `<data>/benchmark.log`。

**注意**：评分器只接受沙箱内证据（`integrity.py:278 evidence_within_sandbox()`；`evidence_search.py:36-45 irc_evidence_within_sandbox()`）。若把日志/交付图移出沙箱，离线评分会视为“无证据”；证据保留的一线要求是“日志始终留在任务沙箱内”。

### 2.4 现有正式数据的经验基线（只读抽样，非四臂数据）

| 数据目录 | 运行数 | 臂 | `mechanism_graph.json` | `.cloudra/mechanism_evidence.json` | 原始 QM 日志 | runtime conversations / artifacts |
| --- | --- | --- | --- | --- | --- | --- |
| `run6-20261021` | 20 | 全部 `dag_guided`（旧单臂） | 20/20 | 16/20 | 1183 | 20 / 1852 |
| `full-20261022` | 50 | 全部 `dag_guided`（旧单臂） | 9/10（10 个沙箱） | 4/10 | 572 | 10 / 700 |

- 两个目录都早于四臂基线（`run6` 的 `runs` 表甚至没有 `undelivered`/`selfconsistency_score` 列），**不能作为四臂证据保留证据**，只能作为“guided 路径产物长什么样”的基线；四臂证据保留必须等 P1 实跑后按同样口径复核。
- `run6` schema 旧：若用新代码打开该 DB，`BenchmarkDB._init`（`runner.py:269-288`）会**重建表并迁移**——即一次写操作。审计/工具读旧数据必须用 SQLite 只读连接（本审计即如此），正式运行不得复用旧数据目录。

### 2.5 Verdict（item 2）

**PASS（保留能力）；附两点披露。**
- A/D 走 guided settlement，写 endpoint 证据文件；B/C **按设计跳过该 publication**，但原始日志、agent 交付图、`.cloudra/evidence/` 快照、runtime 事件与 DAG/计算账本仍保留、可离线审计；回放探针证明缺少该文件**不丢分**。
- 必须披露（1）`.cloudra/mechanism_evidence.json` 是 **guided settlement 的发布协议产物**，不是科学证据本体，也不是所有科学交付的必要条件；（2）B/C 的 `undelivered` 由此结构性恒真，不能当跨臂交付率比较（见 §4）。

---

## 3. fallback 链（scorer 侧，四臂同一套）

### 3.1 `discover_edge_proof` 沙箱发现

- 位置：`cloudra/benchmark/evidence_search.py`（四臂同哈希 `a5b382e4…`）。
  - `SandboxEvidence`（`:116-169`）对沙箱 `rglob` 所有 `.log/.out`，一次性建索引（仅正常终止日志；每文件一次解析；IRC/opt 几何懒解析）。
  - `discover_edge_proof()`（`:178-290`）先按声明的 TS 能量锚定一阶鞍点（无声明时扫描单虚频候选，绝不替换无关鞍点），再找 “IRC 起点几何匹配鞍点” 的 IRC，最后用 `verify_short_irc_direction()` 验证 IRC→Opt→Freq 端点链；**只有 `passed` 才接受**，分级分：saddle 0.35 + IRC 0.15 + 端点 0.5。
- 调用点：`cloudra/benchmark/selfconsistency.py:469-484` — 当绑定的证据链未覆盖该 edge 时，兜底调用 discovery，覆盖成功即 `chk.covered=True`、`score=1.0`。

### 3.2 绑定不完整时的原生日志 fallback

在 `cloudra/benchmark/selfconsistency.py`（四臂同哈希 `4214463039…`）的逐边判定里：

1. 先读 `.cloudra/mechanism_evidence.json`：`read_step_endpoint_evidence()`（`:313-324`）；文件缺失返回 `{}`（**不报错、不判失败**），内容陈旧/校验失败也只是 `endpoint_error` 提示，随后继续。
2. `_strict_irc_proof()`（`:163-287`）：`endpoint_evidence` 为 `None` 时用 `endpoint_candidates(from_files/to_files)` 从已绑定文件反推端点候选；`ts_candidates` 用 `ts_witness()` 从 pool 里找“同几何的一阶鞍点”；pool 含全部 QM 路径（`:418-427`），因此“绑错槽位/未绑定”不阻断原生日志链重建；绑定不完整时 `status=absent` 只写 note。
3. 若仍不覆盖 → 走 §3.1 的 `discover_edge_proof`（`:469-484`）。
4. 每个 edge 的分数在未覆盖时取 `discovery.score`（分级），不因“没绑定”直接判零。

### 3.3 节点能量推边能垒

- `cloudra/benchmark/runner.py:90-118 derived_barrier_graph()`：对没有 `barrier_kcal_mol` 的边，用声明的 `properties.energy_hartree`（TS − source）× 哈特里→kcal 推导；`_apply_declared_barriers()`（`:121-148`）再把推导值作为 declared 声明带入 `collect_barrier_evidence` 的 barrier 证据（因为该函数会重新读沙箱 `mechanism_graph.json`）。
- `cloudra/benchmark/barrier_evidence.py` 四臂同哈希 `67db6ba1…`；accuracy 层仍要求日志支持声明值（`accuracy.py` 四臂同哈希）。

### 3.4 一致性确认

1. **代码位置**：以上全部位于 `cloudra/benchmark/`（scorer 包），不在 `cloudra/dag/` 或 runtime 处理路径中；四臂对 `cloudra/benchmark/` 的差异只有 `runner.py` 接线（§1），fallback 相关文件逐字节相同。
2. **函数级**：`derived_barrier_graph`、`_apply_declared_barriers` 四臂同哈希（§1.3）。
3. **经验验证**：真实交付物回放的 `no_publish` 变体（删除 `.cloudra/mechanism_evidence.json`）在四臂都得到 `selfconsistency_passed=true / score=1.0 / final=1.0`，与带该文件的 `as_is` 完全一致 → 原生日志 fallback 在“没有发布文件”的臂上仍然完整可达，且四臂行为一致。
4. **边界**：fallback 只补“证据发现”，不改变科学标准；`discover_edge_proof` 明确“never accept a mere match”，且锚定声明能量时不替换无关鞍点（`evidence_search.py:193-207`）。

### 3.5 Verdict（item 3）

**PASS。** fallback 链完全在 scorer 侧、四臂同一实现、同一行为；生产臂（A/D）的发布产物只是让 scorer 少走一段发现路径，不会产生评分差异（回放已证）。

---

## 4. `undelivered` 语义

### 4.1 在哪里设置

- 唯一设置点：`cloudra/benchmark/runner.py:419`（C 分支为 `:420`，因 C 多一行 `scientific_feedback` 键）：

  ```python
  res.undelivered = not (Path(sandbox) / ".cloudra" / "mechanism_evidence.json").is_file()
  ```

- 写入 `runs` 表列 `undelivered INTEGER`（`runner.py:172/188/198-204/214`）。
- 全仓库 grep 确认：`undelivered` 只出现在 `cloudra/benchmark/runner.py` 的定义、落库与上述赋值；**评分流水线没有任何地方读取它**（`score_sandbox`、`accuracy`、`selfconsistency`、`integrity`、`delivery_evidence` 均不读）。

### 4.2 它是什么（精确语义）

- 它只是“**guided 结算发布产物是否存在**”的协议/交付状态标签：`True` = 沙箱里没有 `.cloudra/mechanism_evidence.json`。
- 它**不是**“没有交付最终答案”“没有机制图”“没有计算”“科学零分”的同义词：
  - B（record）与 C（standard）在设计中永不走 guided publication → 即使交付了完整 gold 级机制图+全套日志，`undelivered` 仍为 `True`；
  - A/D 也只有当 guided `commit_stop()` 真的发布成功（artifact 非空、且 `disposition != user_terminated`）时才为 `False`；
  - partial 结算也可能发布成功（`undelivered=False`），所以它也不是“complete 专用”标志。
- 分支文档与计划已一致声明该口径：C 文档 `docs/benchmark/SCIENTIFIC_FEEDBACK_ABLATION.md`（“`undelivered` is an artifact/protocol metric, not automatically scientific zero”）；计划 §4 特别风险条。

### 4.3 这样的运行还能审计/评分吗

**能，且探针已证。** 评分输入只有沙箱交付物（`runner.score_sandbox` 只读 `mechanism_graph.json` 与日志；`integrity.py` 头注释“Pure filesystem + parsing; no LLM, no DB”），与 `undelivered` 无关：

| 证据 | 内容 |
| --- | --- |
| 回放 `no_publish` | 删除发布文件后 `undelivered=True`，但 `graph=1.0/selfconsistency=1.0/accuracy=0.999972638934/final=1.0`，与 `as_is` 完全相同（四臂一致） |
| 合成探针 | 同样交付物下，有无发布文件只翻转 `undelivered`，其余分数（-1.0）不变 |
| 代码 | `undelivered` 无 reader；`score_sandbox` 不接收 RunResult 之外的交付状态；`runs` 表无 disposition/complete 列 |

离线审计入口（按优先级）：
1. `sandboxes/<task>/<batch>/`（原始产物，最权威）；
2. `<data>/runtime/runtime-v2.db` 的 `agent.completion_gate`（`action`/`source`/`basis`）与 `run.finished`；
3. `<data>/runtime/conversations/<project>/tasks/database.db` 的 `dag_delivery_dispositions`（A/B/D 有；C 无）与 DAG evidence 表；
4. `benchmark.db` 的 `notes` 与分项分数。

### 4.4 跨臂可比性：FLAG（不是评分公平性，但是分析陷阱）

- 因为 publication 只存在于 guided settlement，`undelivered` 的**预期基线**本身随臂不同：A/D 可能两者都有，B/C 结构上恒为 `True`。**禁止**用 `undelivered` 率做跨臂“交付成功率”比较，也禁止把它当科学失败率。
- 论文中如需“运行与交付状态”轴，应使用结构化 basis/verification label：`cloudra/runtime_v2/completion.py:31-37/69-77` 把 `agent.completion_gate.basis` 映射为 `dag_verified→verified`、`supervisor_supported→supervisor_reviewed`、`supervisor_approved/partial_recorded→partial`、其余（含 C 的 `declared`）→`unverified`。该 basis 事件已持久化在 `runtime-v2.db`（`backend.py:119-125`，除 `llm.chunk` 全量落库）。
- 注意 `benchmark.db` 本身**不含** delivery disposition/basis；离线分析必须 join runtime 事件（或 conversation DB），冻结时应把这一步脚本化并纳入评估器清单。

### 4.5 Verdict（item 4）

**PASS（语义与评分独立性）；同时 FLAG（跨臂比较无效）。**
- 诚实性通过：`undelivered=True` 不会自动扣分/判零、不会被当成 complete；评分仍从沙箱证据重新判定。
- 但它是臂相关的“发布协议”指标：正式论文**不得**用它做跨臂或跨题交付率对比；需要交付状态轴时必须用 `completion_gate.basis` + `dag_delivery_dispositions`。

---

## 5. partial vs complete：per-arm `stop_audit` 行为与离线评分

### 5.1 各臂 `stop_audit.py` 差异与结算行为

文件哈希：A=`282db1f3…`、C=`282db1f3…`、D=`282db1f3…`（三者相同）；B=`6333b822…`（仅 +10 行，两处 record 早退）。

| 行为 | A | B | C | D |
| --- | --- | --- | --- | --- |
| 是否启用 DAG stop 门禁 | 是（DAG_GUIDED） | 是但 advisory（DAG_RECORD） | **否**（STANDARD：`_controller` 返回 None） | 是（DAG_GUIDED，同 A） |
| `complete` 结算条件 | 覆盖率通过 + **required IRC direction proof**（`stop_audit.py:279-297`）+ 交付 artifact 校验（`:290-302`）→ 无 coverage 直接 `continue_work`（`:324-330`）；DAG_GUIDED 下还需 Supervisor exit review（`:348-373`） | **不设门槛**：`stop_audit.py:277-281` 直接 `allow_final`，basis=`declared`（complete）/`partial_recorded`（partial），**不校验** artifact/coverage | 无门禁：`dag_stage.py:87-108` 无 DAG 裁决 → `agent_runner.py:827-838` 落 basis=`declared` 直接放行 | 同 A（整文件同哈希） |
| `partial` 结算条件 | DAG_GUIDED：需 Supervisor 接受（`supervisor_approved`，`stop_audit.py:424-467`）；未接受则 `wait_review` | 直接 `allow_final` + `partial_recorded`（`:277-281`） | 无审计（`declared`） | 同 A |
| 结算发布 `.cloudra/mechanism_evidence.json` | 写（`commit_stop()` `:522-538`） | **不写**（`commit_stop()` `:511-515` 记录 disposition 后 return） | **不写**（无 commit_stop 调用） | 写（同 A） |
| 交付状态落库 | `dag_delivery_dispositions`（含输出 artifact 快照路径） | `dag_delivery_dispositions`（有 coverage report，无 artifact） | 无 DAG 行；仅 runtime 事件 `agent.completion_gate` | 同 A |
| `verification_label` 投影（`completion.py`） | complete 通过：`verified`/`supervisor_reviewed`/`scope_completed`；partial：`supervisor_approved→partial` | complete：`declared→unverified`；partial：`partial_recorded→partial` | `declared→unverified` | 同 A |

B 的诚实性有代码内测试背书：`tests/test_benchmark_record_advisory.py:20-49` 明确把 `prepare_delivery_artifact` 与 `write_step_endpoint_evidence` monkeypatch 成“禁止调用”，仍要求 `allow_final`、basis 正确、disposition 落库、`_delivery_artifact is None`；并要求不完整科学覆盖的 report 保持 `complete=False`（`:41-42`）。

C 的差异：`DagPolicyStage._controller()` 对 `standard` 返回 None（`cloudra/runtime_v2/policies/dag_stage.py:58-61`），`audit_run_end` 直接返回 None（`:106-108`）；`DagController.enabled=False`（`cloudra/dag/controller.py:64-66`）。另 C 的 `ts_guess` 独立验证被硬拒（`cloudra/tools/Chemtool/ts_guess.py:1353-1362`，verify/strict 模式返回 is_success=False），DAG 工具在 wire 上被隐藏（`cloudra/runtime_v2/tool_catalog.py:45-59`，STANDARD 隐藏 `dag_tools()`）。

### 5.2 离线评估器为什么不会把 partial 当 complete success

1. **评分器不含“交付状态”输入**：`score_sandbox(task, sandbox)` 只接收任务规范与沙箱路径（`runner.py:411-522`）；不读 DB、不读 disposition、不读 completion 事件。`undelivered` 只是事后写入的行字段，无 reader（§4.1 的 grep 证据）。
2. **评分器没有 complete/success 布尔输出**：`runs` 表字段是 `graph_score/selfconsistency_passed/selfconsistency_score/undelivered/accuracy_score/final_score/notes`（`runner.py:198-204`）；没有 `complete`、`delivered`、`success` 列，也没有把 `selfconsistency_passed` 当任务成功的逻辑。
3. **分数是连续科学量**：`final = 0.1·graph + 0.3·selfconsistency + 0.6·accuracy`，`selfconsistency_passed` 的含义是“交付图中的每个 accessible 元素都有原生证据覆盖”（`selfconsistency.py:498-536`），不是“任务完整成功”；`accuracy` 是逐 gold 边加权连续分（`accuracy.py:1-45`）。
4. **partial 交付在评分中没有升格通道**：缺边/缺证据只会降低 graph/accuracy/selfconsistency；不存在“因为在线结算写了 complete 就加分”或“写了 partial 就扣分”的代码路径。回放探针里同一批交付物无论发布文件是否存在、无论用哪一臂的评分器，分数完全相同，直接证明评分对“在线结算标签”不敏感。
5. **反向也成立**：A/D 的在线拦截只影响“这次 run 以什么 basis 结束”，不影响离线用沙箱重算的科学判定；`score_sandbox` 也不把 A/D 的拦截结果当标准答案（计划 §3.2 的要求由该架构直接满足）。

### 5.3 需要冻结的缺口（不是当前违规，是论文可操作化缺口）

- 当前评分器只产出连续指标，**没有显式的“独立科学成功/有效 partial/假成功”分类器**。计划 §4 要求按冻结任务契约与 Gold 判定“独立科学成功/有效 partial/假成功”；这必须在 P0 冻结时落成确定性规则（例如：`graph==1.0 且 selfconsistency_passed 且 accuracy==1.0`？还是逐题契约人工/半自动复核？），否则不同臂的“成功率”无法在论文中一致计算。
- 另：不可把 `weighted=0.9` 之类连续分数当成功率（计划 §4 已有此约束），也不能把 `selfconsistency_passed` 当任务成功。

### 5.4 Verdict（item 5）

**PASS（partial 不会被离线评估器当 complete success）。** 四臂的在线结算语义不同且与设计一致（A/D 强门禁、B advisory、C 无 DAG），这些差异不会注入离线评分。**附冻结行动**：P0 必须把“独立科学成功/有效 partial/假成功”的判定规则与数据提取脚本冻结进评估器清单。

---

## 6. C/D 反馈残余渠道与 shell/审计隔离边界

> 本节回答“即使做了投影，完整科学/诊断文本还能从哪些通道到达模型”，以及“shell 不是操作系统级隔离”的实际边界。C/D 的分支文档（C：`docs/benchmark/SCIENTIFIC_FEEDBACK_ABLATION.md`；D：`docs/benchmark/BRIEF_ERROR_ABLATION.md`）与代码一致；以下为代码级清单。

### 6.1 C（standard）已投影的公开通道

| 通道 | 投影代码（C 分支） |
| --- | --- |
| 传统 tool result（data/summary） | `cloudra/runtime_v2/invocation.py:122-127` `project_scientific_tool_result` |
| JS guest ToolResponse（先验原始帧限长，再投影） | `cloudra/runtime_v2/js_protocol.py:227-235` |
| 通知/pin（guidance/compute 渲染） | `cloudra/runtime_v2/notices.py:233-236, 244-246, 283-290` |
| 非 user 消息的模型上下文准备 | `cloudra/runtime_v2/agent_runner.py:952-960` `project_scientific_notice` |
| TS prepare/resume/inspect 与嵌套 ts_guess process 视图 | `cloudra/tools/core/ts_process.py:344-350` `public_scientific_record` |
| `process.json` 展示副本（revision/stop 写盘） | `cloudra/services/ts_pipeline_store.py:113-120, 338-346` |
| `load_record`/restart（从权威 DB 解析，校验 run/workspace） | `cloudra/tools/core/ts_process.py:357-370` |
| 工具输出 schema / 公共工具文档（`verified`→null、`outcome` 中性） | `cloudra/runtime_v2/tool_catalog.py:343-365`；`cloudra/tools/documentation.py:64-80` |
| 独立 `ts_guess verify/strict` 禁用（执行层硬拒） | `cloudra/tools/Chemtool/ts_guess.py:1353-1362` |

### 6.2 C 仍会泄漏科学判定/诊断的残余渠道（论文必须披露）

1. **保留字段原样透传**：`scientific_feedback.py:22-28 _RAW_FIELDS`（`input/arguments/content/stdout/stderr/declarations/native_output/structures/geometry/coordinates/methods/calculation/diagnostics` 等）不投影；数值/几何/证据路径本就不应删，但其中可能含判断性文本。
2. **混合模板“只去外壳”**：`_observed_text()` 对固定模板保留内层（如 `scientific_feedback.py:100-134` 的 separated-product/IRC outer-frame observations、`:180-216` 的 mode/频率模板）；`ts_guess` 的 `checks`/`verdicts` 列表逐条只做模板投影（`:292-294`），未知混合解释原样保留。旧版“纯文件权威记录”不就地改写（`:365-368`，无 `pipeline_id` 直接返回）。
3. **原生日志与 shell 读取不经投影**：`read`/`bash` 的文本不做扫描；Gaussian/ORCA 日志标题、内部 TS 决策、几何启发式、未知混合输出仍可自行判读（C 文档 §“Deliberate boundaries and residual feedback”第 1/4/5 条）。
4. **内部账本完整可读**：`compute.db`（TS pipeline 权威记录）、`runtime-v2.db`（事件）、conversation DB（DAG 证据）不经公开投影；agent 有 shell/read 权限即可读（见 6.5）。
5. **工具 schema 的残余提示**：C 只把 `TsVerdict.verified/outcome`、`TsGuess.verification_status` 等公共字段改为 null/中性；输入 schema 仍列出 `verify`（执行层拒绝），公共任务 prompt 仍提到 DAG binding（C `ABLATION_ARM.md` 已列此已知差异）。
6. **安全审批与 YOLO**：审批仍接收真实风险事实（YOLO 审批反馈是潜在科学信息回流通道；`yolo=True` 时审批由 guard 处理）。
7. **DAG 混杂**：C 隐藏全部 DAG 工具而 B 保留 DAG（`tool_catalog.py:45-59`），因此 **B/C 是“包比较”而非纯“独立校验工具”消融**，必须在论文中按真实差集解释。

### 6.3 D（brief-errors）已投影的公开通道

| 通道 | 投影代码（D 分支） |
| --- | --- |
| 传统 tool result context（按 tool_name 区分 native） | `cloudra/runtime_v2/invocation.py:113-127`（`tool_result_context_content` → `project_tool_result`） |
| JS guest result/error 帧（先验原始 payload/frame limits，再缩短） | `cloudra/runtime_v2/js_protocol.py:217-250`；`js_runtime.py:292-300, 530-575` |
| 通知/pin/mailbox（固定通知格式） | `cloudra/runtime_v2/notices.py:233-290`；agent_runner 的非 user 消息准备 `agent_runner.py:952-960` |
| DAG 提示副本（payload 投影后再渲染） | `cloudra/dag/models.py:1115-1117` |
| 子任务报告 | `cloudra/runtime_v2/child_manifest.py:211-213` |
| `process.json` 展示副本（只对有 `pipeline_id` 的记录投影） | `cloudra/services/ts_pipeline_store.py:113-120, 338-346` |
| 审批/策略阻断文本 | `cloudra/runtime_v2/turn_pipeline.py:626-645`；`js_runtime.py:292-300` |
| 计算通知（失败时保留 state/outcome，删 advisory/next/process 细节） | `brief_errors.py:184-218` `project_compute_notice` |

### 6.4 D 仍会泄漏完整诊断/科学解释的残余渠道（论文必须披露）

1. **native 工具豁免**：`brief_errors.py:130` `native = tool_name in {'bash', 'read', 'log_parser'}` —— 这三类工具的结果不做投影；`_OPAQUE`（`:28-31` `arguments/input/content/stdout/stderr/structures/coordinates/frequencies`）也原样保留。原始日志、read 内容、bash 输出（含长输出 offload 文件）仍完整可见。
2. **混合科学字段保留**：`checks`/`verdicts` 里混有测量+建议的条目只删一条已知独立的 IRC repair 指令，其余保留（`:100-107`）；普通 scan/candidate 摘要中的混合事实与建议也保留。
3. **file-only 记录完整**：`public_process_record()`（`:221-225`）对无 `pipeline_id` 的记录 `deepcopy` 原样返回；老 workspace 的独立 `process.json` 仍是完整记录。
4. **exit-review handshake 原样保留**：`manifest`（kind=exit_review_decision）不投影（`:88-90`），可含完整裁决理由/final answer；不过同时权威记录本就在 DB/事件里，经 shell 可读。
5. **成功输出基本不投影**：只有失败上下文触发诊断缩短；成功结果的普通数据（含嵌在字符串里的科学描述）通常原样通过；只有显式失败容器（`_CONTEXTS`）递归。
6. **非规范 JSON summary 保留原文**：重编码会变长时用原文（`:143-147`），因此个别完整诊断文本可能以原始 summary 到达模型。
7. **历史上下文不清洗**：既有 DB/事件、旧 model-context 历史未删；正式运行必须全新会话（D 文档要求 clean workspace）。
8. **DAG/监督者仍在**：D 是 guided 全功能臂，只缩短错误文本；Supervisor 仍在线，其正常输出/裁决文本只按固定通知模板缩短。

### 6.5 shell / 审计隔离边界（四臂相同，是“非 OS 级”隔离）

- `bash` 工具：`cloudra/tools/Bashtool/bash.py:172-177` 用 `asyncio.create_subprocess_shell(command, cwd=working_directory)` 执行——**只有 cwd，无 chroot/bwrap/namespace/路径白名单**；权限由命令分类 + 角色 permission 决定（`:87-137`），对 `cat/grep/head` 等读命令只要角色有 READ 就允许。
- benchmark 里 coordinator 任务（task JSON `prompt.role=coordinator`）拥有全权限：`cloudra/runtime_v2/roles.py:24` `PermissionSet(read=True, write=True, manage=True, script=True, destructive=True)`；benchmark 任务设置 `yolo=True, unattended=True`（`cloudra/benchmark/runner.py:230`）→ 无人审批，命令可执行。
- 文件工具是 workspace 受限的：`read` 只接受工作区内文件（`cloudra/tools/Searchtool/read.py:86-93`），`write`/`edit` 经 `workspace_for_tool`/Workspace 服务限界；但 `bash` 不受此限。
- **因此**：工作区外的审计数据（`<data>/runtime/**`、其它 checkout、共享 repo 里的题库/gold `ideapool/tasks/*.json`、C/D 的文档与代码）在这台机器上对 agent 的 `bash` 是**可读**的。四臂完全相同（没有为任何臂削弱/新增权限或沙箱体系），所以不构成臂间公平性差异；但属于必须披露的基准有效性/隔离假设，并且需要 P1 记录实际是否发生读取。
- 评分侧的强制约束正好相反：scorer 只接受**沙箱内**证据（`integrity.py:278`、`evidence_search.py:36-45`），因此“把证据移到工作区外再宣称离线可审计”不成立；离线审计者只能读沙箱与数据目录内的产物。

### 6.6 论文必须披露的清单（最小集）

1. C/D 是**公开反馈投影**，不是信息盲化/文件隔离；原生日志、`read`/`bash`、审计 DB/事件、file-only 记录、混合字段仍可回流完整科学判断。
2. **shell 不是 OS 级隔离**：工作区外审计数据、题库/gold、其它 arm 代码在原理上可读；本实验未新增权限/沙箱体系。必须披露隔离假设，并在 Pilot 记录是否发生完整诊断/答案回流。
3. C 的“自动判定模糊化”只对公开 TS 判定字段生效；独立 verify/strict 被禁用，但计算、原始数值、内部账本与离线评估不变；`null` 不等于 fail/pass。
4. C 仍隐藏 DAG 工具而 B 保留 → B/C 对比是**包比较**，不能归因为单一“校验工具”效应。
5. C 的输入 schema 仍列出 `verify`（执行层拒绝）、公共 prompt 仍提 DAG binding → 存在“调用失败/提示”层面的残余反馈。
6. D 只缩短诊断文本：错误类别/状态码/阈值/工具/成功输出/科学证据/partial 语义不变；混合 `checks/verdicts`、native outputs、正常 guidance/SOP、exit-review manifest 保留。
7. `undelivered` 是 guided publication 协议指标，不是科学零分，也不是跨臂交付率；交付状态轴用 `completion_gate.basis` + `dag_delivery_dispositions`。
8. A 与 D 的 `runs.orchestration_mode` 同为 `dag_guided`；分臂归因必须用 `batches.config.experiment_arm`（或独立数据目录）。
9. 未冻结前不得把连续分（`weighted`）当成功率；独立科学成功/有效 partial/假成功的判定规则需随评估器一起冻结。

### 6.7 Verdict（item 6）

**PASS（残余渠道已识别、与代码一致、可进入论文披露），但不是“完全盲化”。**
- C/D 分支文档已列残余并明确“不是完全盲化/不是 OS 隔离”；本审计用代码逐通道核对，未发现文档漏报的“高价值”通道（发现的补充点：C 输入 schema 仍列 verify；D 的 manifest/成功输出/非规范 summary 保留；shell 可读仓库与数据目录）。
- P1 必须实际记录 C/D 残余回流（计划 §六 P1 要求），不能仅凭代码投影声称“已屏蔽”。

---

## 7. 总结论

### 7.1 Verdict 汇总

| # | 审计项 | Verdict | 关键证据 |
| --- | --- | --- | --- |
| 1 | 评分器身份（6 文件） | **PASS** | 5/6 逐字节相同；`runner.py` 仅接线/来源差异；评分函数 AST 同哈希；合成+真实回放四臂逐字段一致 |
| 2 | 各臂证据保留 | **PASS**（附披露） | 原始日志/图/`.cloudra/evidence` 保留；A/D 发布 endpoint 证据，B/C 按设计跳过；回放证明不缺分 |
| 3 | fallback 链（发现/原生日志/能量推能垒） | **PASS** | 全在 `cloudra/benchmark/`；四臂同文件/同函数哈希；`no_publish` 回放仍 `selfcons=1.0/final=1.0` |
| 4 | `undelivered` 语义 | **PASS**（语义/评分独立）；**FLAG** 跨臂不可比 | 唯一设置点 `runner.py:419`；无评分 reader；回放仅翻转标签；B/C 结构恒真 |
| 5 | partial vs complete | **PASS**（不会被当 complete 计成功）；需冻结成功判定 | 评分器无 disposition/complete 输入；四臂 `stop_audit` 语义与设计一致；B 有针对性测试 |
| 6 | C/D 反馈残余 | **PASS**（已枚举/可披露）；**非完全盲化** | 通道-代码映射表 + 残余清单 + shell/隔离边界；P1 需实测回流 |
| — | **总体公平性（评分链一致）** | **PASS：identical scorer = YES，无 fairness violation** | 见 §1、§3、§5；四臂评分链与 fallback 完全同一实现 |

### 7.2 公平性结论

- **评分公平性：通过。** 四臂执行的是同一套离线评分代码/常量/fallback；唯一文件差异是 `runner.py` 中“本分支跑哪个臂”的接线与批次来源字段，评分入口 `score_sandbox()` 四臂同哈希。
- **实验处理差异（预期、已披露）：** A/D=guided（含完整 Supervisor/结算门）；B=record（advisory 结算）；C=standard（无 DAG + 独立验证禁用 + 公开判定模糊化）；D 仅简略错误文本。D 与 A 的差异经代码确认只在错误投影模块（`brief_errors.py` 及其调用点），结算/发布/评分不变（`stop_audit.py` 同哈希）。
- **不构成 fairness violation 但必须在论文交代的“非评分差异”：** 批次 provenance 字段、`orchestration_mode` 行标签、`undelivered` 语义、C 的 DAG 混杂与 D 的反馈混杂。

### 7.3 开放问题与冻结前行动项

1. **`undelivered` 跨臂比较禁用**：论文交付状态轴改用 `agent.completion_gate.basis`（runtime-v2.db）+ `dag_delivery_dispositions`（conversation DB）；P0 冻结时提供统一提取脚本。
2. **科学成功判定规则未冻结**：评分器只有连续指标；需在 P0/P1 前冻结“独立科学成功/有效 partial/假成功”的确定性判定（gold 契约 + 阈值/人工复核流程），否则四臂成功率不可比。
3. **shell 隔离与数据布局**：正式运行前决定是否把题库/gold/审计数据置于 agent 不可读路径或容器；至少 P1 记录 shell/read 对工作区外路径的实际访问（审计数据、gold、其它臂）。四臂权限一致，不影响臂间公平，但影响基准有效性声明。
4. **C/D 残余回流实测**：P1 按计划记录实际发生的完整诊断/科学判定回流；发生即披露并按冻结规则做敏感性分析，不能包装成完全盲化。
5. **旧正式数据目录处理**：`run6-20261021`（旧 schema，无 `undelivered`/`selfconsistency_score`）与 `full-20261022`（旧单臂 guided）不得混入四臂结果；新代码打开旧 DB 会触发表重建（`BenchmarkDB._init`），离线分析必须只读/只复制。
6. **四臂 checkout 未跟踪文件**：`run.sh` 不在库里；冻结时登记其内容/哈希或删除，确保四臂运行环境可复现。
7. **四臂正式数据尚未存在**：本报告全部证据是代码级 + no-model 探针；P1 实跑后必须用同一套探针（scorer-parity/replay-parity）在真实四臂运行上复核，并把哈希/摘要写入 P1 验收。

---

## 附录 A：评分器六文件完整 sha256（分支头）

```
branch benchmark/arm-guided (A)
  runner.py             0dfee4319be851347d65b2ca6b90626bf1440bcf5911468c8c2047292807a7d9
  accuracy.py           fa0676a97def21189ce48e3f773bcd8de8f1e55ac6531da891cd234daf1bf5c7
  selfconsistency.py    42144630396896f7b64547c3b3db0696a1b06c2c3e9dca2c8350d3f060a2d026
  evidence_search.py    a5b382e4bd9d6ff87945e24764d0f07ad5255259f4902d11ef7837d1ac1ca066
  integrity.py          d2b8404149a2b4ab85923c96ba3a1a63e862ac4d1eeb28c0629da554057c14cb
  delivery_evidence.py  1dd5631e408807ec128e769ca0b2b9ee4f4acb62880bd5ecade4662f1086c29e

branch benchmark/arm-record (B)
  runner.py             29d0b4db6d291592ba1e58886972a9cb683a3314eddda17bb0fb098e8fc0112d
  accuracy.py           fa0676a97def21189ce48e3f773bcd8de8f1e55ac6531da891cd234daf1bf5c7
  selfconsistency.py    42144630396896f7b64547c3b3db0696a1b06c2c3e9dca2c8350d3f060a2d026
  evidence_search.py    a5b382e4bd9d6ff87945e24764d0f07ad5255259f4902d11ef7837d1ac1ca066
  integrity.py          d2b8404149a2b4ab85923c96ba3a1a63e862ac4d1eeb28c0629da554057c14cb
  delivery_evidence.py  1dd5631e408807ec128e769ca0b2b9ee4f4acb62880bd5ecade4662f1086c29e

branch benchmark/arm-standard (C)
  runner.py             a007d133aa4c6c85f642b5008bf435a86ba459dd37583c00ec725718bac44415
  accuracy.py           fa0676a97def21189ce48e3f773bcd8de8f1e55ac6531da891cd234daf1bf5c7
  selfconsistency.py    42144630396896f7b64547c3b3db0696a1b06c2c3e9dca2c8350d3f060a2d026
  evidence_search.py    a5b382e4bd9d6ff87945e24764d0f07ad5255259f4902d11ef7837d1ac1ca066
  integrity.py          d2b8404149a2b4ab85923c96ba3a1a63e862ac4d1eeb28c0629da554057c14cb
  delivery_evidence.py  1dd5631e408807ec128e769ca0b2b9ee4f4acb62880bd5ecade4662f1086c29e

branch benchmark/arm-guided-brief-errors (D)
  runner.py             7aef6234029b51bc7b4581a29658d50428ecee328ac2c59beb4e93115c015eb2
  accuracy.py           fa0676a97def21189ce48e3f773bcd8de8f1e55ac6531da891cd234daf1bf5c7
  selfconsistency.py    42144630396896f7b64547c3b3db0696a1b06c2c3e9dca2c8350d3f060a2d026
  evidence_search.py    a5b382e4bd9d6ff87945e24764d0f07ad5255259f4902d11ef7837d1ac1ca066
  integrity.py          d2b8404149a2b4ab85923c96ba3a1a63e862ac4d1eeb28c0629da554057c14cb
  delivery_evidence.py  1dd5631e408807ec128e769ca0b2b9ee4f4acb62880bd5ecade4662f1086c29e
```

其他证据链相关文件（四臂一致）：

```
cloudra/dag/delivery_artifact.py                    6235320bae74f3c01d01dd192becce54c577cc83946fed901d8a6cf1aed94285
cloudra/persistence/paths.py                        7656d4166c4db28e1cacd81a30d5476ade15217ce31b75590501b5fb40bcf0f7
cloudra/benchmark/barrier_evidence.py               67db6ba183f50e1d115317870cd49a95c108403b1fca79b1c7c0fb0fe6d009a6
cloudra/dag/evidence_ingest.py                      988785294e907faf3280d2beb67ca5acf9a4c565f8dd8cf6abc44a4a24acafe6
cloudra/dag/file_science.py                         47d02d763dce8fadcab4bae799fe167cd4533eca8b0c6ede8276e6094f281c19
cloudra/tools/Plantool/dag_tools/dag_submit_step_evidence.py    c33494470996852ce7bfce64b71ec2b3d24cf11b651e795ee4e14aef14386f0c
cloudra/tools/Plantool/dag_tools/dag_submit_species_evidence.py de4d286aa67ea7ee8c9c5cb4217021537ffd49b5c174f5e4fe36edd6535be39d
```

按臂不同的证据链相关文件（设计差异，非评分差异）：

```
cloudra/dag/stop_audit.py     A/C/D = 282db1f3ad8f0cce21c0de6b96c4a6b224b77d86ff1ea36f3d7b451290aecf97
                              B     = 6333b822f3cc1a28394991d8ddf443a8a5fea684fe1254f15b3fafe26bfc8edd
cloudra/dag/models.py         A/C   = 84bfb36fbceb599f34af23b87dd03b4e5ba94bd0f58e698b4c76e6a7bd5c1e7f
                              B     = b5cfe49ba57810787c215b91a967d99076e55c29fa1d79587990b6ea705f8bc5
                              D     = 6bf19a262a3a1605e66410907c5914c8adaf1c0752a017f367d2221605a053bd
cloudra/tools/core/ts_process.py          A/B = cefd2799278dc5249b6a328347da899fbd6ef461a34f5ff233a39f2a3d9a1d74
                                          C   = c9a8608d2186e892d49d892db9e1688172f2167e87522f2c5994ed2d39b3df29
                                          D   = d504b9a3b9ca1c4c67ea45957f89b5bd6fa0e585d6c822affeac82113a665f2f
cloudra/services/ts_pipeline_store.py     A/B = de7057ca6aac1310fb6d07b48184817d6ee58f50f2a2a82a2bbd18305dbc02b5
                                          C   = a2f0c9a812dc149718463c007a01f70e3a3287a92d9920528160f4b0bb14dc6d
                                          D   = f69427a6272256b518df352f7dd568ce521f7f5addfb09b929d64aa10815a397
```

`ts_process.py` / `ts_pipeline_store.py` 的 C/D 差异仅为：
- `process.json` 展示副本投影（C：`public_scientific_record`；D：`public_process_record`，均只对 `pipeline_id` 记录生效；权威 DB 不改）；
- C 额外：`load_record` 对带 `pipeline_id` 的记录回查权威 DB。

差异均**不含** `snapshot_evidence_file()` 调用行（`git diff | grep snapshot_evidence_file` 零命中），即 `.cloudra/evidence/` 写入行为四臂一致。

## 附录 B：探针复现与产物路径

1. 评分器合成一致性：`/mnt/c/Users/ly/bench/p0_scorer_parity.py` + `run_scorer_parity.sh`
   - 产物：`/home/ly/cloudra-p0-probe/p0-evidence/scorer-parity/<A_guided|B_record|C_standard|D_brief>/summary.json`
   - 四臂 summary 规范化 sha256：`d87288fa271911d5cbe454bbfb52d1439e11fbe703c3ead33aa696f34c7769ef`
2. 真实交付物回放：`/mnt/c/Users/ly/bench/p0_replay_parity.py` + `run_replay_parity.sh`
   - 源沙箱：`/home/ly/cloudra-bench-run6-20261021/sandboxes/E1/batch_d7fbb0b92b284ce4`（只读；硬链接复制，未改源）
   - 产物：`/home/ly/cloudra-p0-probe/p0-evidence/replay-parity/<arm>/summary.json`
   - 四臂 summary 规范化 sha256：`5a198d1542df567151d35748fdcc6eaa5de8ff85f58d90da76d70dee7fda868c`
   - 历史行对照：run6 `runs` 表 E1 = `(graph 1.0, selfconsistency_passed 1, accuracy 0.9999726389344515, final 1.0)`
3. 评分器哈希/差异：`/mnt/c/Users/ly/bench/scorer_hash.sh`、`scorer_diff.sh`、`scorer_diff2.sh`、`scorer_fns2.sh`、`evidence_hashes.sh`、`probe_writers.sh`
4. 版本与分支：`/mnt/c/Users/ly/bench/probe_arms.sh`、`arm_diffs.sh`
5. 只读数据检查：`/mnt/c/Users/ly/bench/probe_db.sh`、`probe_db2.sh`、`probe_evidence_presence.sh`、`probe_run6_detail.sh`

所有探针均无 LLM/付费调用；未写入 `run6-20261021`、`full-20261022` 或任何 arm checkout 的受跟踪文件。
