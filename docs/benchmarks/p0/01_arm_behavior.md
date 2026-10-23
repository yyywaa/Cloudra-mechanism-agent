# P0-1 四组实际行为清单（A / B / C / D）

> 审计对象：Cloudra 四组对照实验的**实际代码行为**（不是分支文档的声明）。
> 基准文件：`ideapool/cloudra_four_arm_experiment_plan.md` §二表格（行 22–25）、§八五个代码点、§九冻结清单（行 182）。
> 审计时点：2026-10-24 01:40–02:00（Asia/Shanghai）。只读审计：未切换任何 checkout 分支、未修改任何产品代码、未发起模型/LLM 调用、未运行正式 benchmark、未写入两个正式数据目录。
> 探针目录：`/home/ly/cloudra-p0-probe/p0-behavior/`（纯导入 + 临时 SQLite + 纯函数探针，无模型、无付费计算）。
> 相关分册：`00_lead_checks.md`（Lead 自查）、`02_bc_diff.md`（B/C 差集与残余回流）、`03_evidence_chain.md`（证据链）、`04_freeze.md`（冻结清单）。
> 证据编号 `E1…E20` 与文末“附录 A 证据索引”对应。

---

## 0. 结论摘要

- **强制模式**：四臂都通过 `cloudra/benchmark/runner.py` 的 `ABLATION_ARM` 常量把**所有** benchmark 任务强制到本臂模式；题库 50 题 JSON 里的旧标签（50/50 为 `dag_guided`）被覆盖。A/D=`dag_guided`，B=`dag_record`，C=`standard`。（E2）
- **DAG 工具面**：A/D 对 coordinator 暴露全部 19 个 `dag_*`；B 暴露 13 个、隐藏 6 个 Supervisor 裁决工具；C 隐藏全部 19 个。四臂都因 `unattended=True` 隐藏 `ask_user`。默认 JavaScript 协议下顶层 wire 只有 `js_exec` + direct 工具，`dag_*` 经 JS guest 调用。（E3、E4）
- **独立校验**：A/B/D 的 `ts_guess` 保留 `verify`/`strict` 执行路径；C 在 `ts_guess` 入口直接返回失败（`ts_guess.py:1355-1362`），但**输入 schema 与工具描述仍宣传 verify**（已由 C 分支文档披露，属残余）。（E5）
- **Supervisor**：A/D 在线（懒启动：机理草案/显式送审/退出审查触发；另有独立 final reviewer）；B/C 离线——B 的 DAG_RECORD 模式在通知钩子处直接 return，C 根本不创建 `DagController`。（E6）
- **结算门**：A/D 是 guided 门禁——`complete` 需要 IRC 方向证明 + 交付物一致性 + 覆盖通过，再交 Supervisor 最终审查；`partial` 也必须 Supervisor 接受；同一缺口被拒 3 次后 run 以 failed 结束。B 是 advisory——`complete`/`partial` 一律 `allow_final`（`declared` / `partial_recorded`），不要求覆盖、交付物或端点证据。C 无 DAG 门禁，缺省 `allow_final(declared)`。（E7、E8、E9、E10）
- **partial**：A/D 走 Supervisor 终审（basis `supervisor_approved`，completion 标签 `partial`），并写 `dag_delivery_dispositions` 行与 `.cloudra/mechanism_evidence.json` 端点证据；B 写 disposition 行但 basis 是 `partial_recorded`，无端点证据；C 只有模型声明，无 disposition 行、无端点证据。（E11）
- **反馈详细度**：A/B 为 full；C 只把**公开的 TS 科学判定**中性化（结构化字段→`null`，固定模板→`Scientific judgment not provided.` / `?`），执行失败/数值/路径/DB 权威记录保留；D 把**诊断文本**压缩（失败上下文的 `message/reason/detail/next_action` 等→`Diagnostic details omitted.`），状态、类别、数值、路径保留。（E12、E13）
- **Provenance**：`batches.config` 记录 `experiment_arm` / `error_feedback`（C 另有 `scientific_feedback`）/ `orchestration_modes` / `models{coordinator,follower}` / `plugins`；`runs` 行记录 `orchestration_mode`。**不记录 git SHA、模型采样参数、Supervisor 模型/角色消耗**。（E15）
- **计划表核对**：A 符合；B 符合（另有 4 项行为细节需登记）；D 符合（另有 2 项审计口径注记）；**C 部分符合**——四项核心意图实现，但有 4 项已确认残余/不一致（中性文本为英文、verify 仍被 schema 宣传、公共 role prompt 仍指示 DAG 工具、结算记录比 B 更弱）。（§5）
- **最需要 P0 处理的两点**：① 计划 §九声明的共同基线 `8c568ca` 已过期——四臂实际共同产品基点是 master `1e6d953f`（含 `ts_guess.py` +120/−16 的两次 master 提交）；② 在线 `undelivered` 标志唯一来源是 A/D guided 交付路径写出的 `.cloudra/mechanism_evidence.json`，B/C 没有写入路径，因此 B/C 的 runs 行将**恒为 undelivered=1**——这是交付协议产物，不是科学失败，报告交付率时不可当作四臂同口径指标。（E17、E18）

---

## 1. 审计对象、基线与方法

### 1.1 四臂 checkout 与 HEAD（E1）

| 臂 | 分支 | checkout 路径 | `git rev-parse HEAD` | 与 `origin/benchmark/*` 一致 | 工作区状态 |
|---|---|---|---|---|---|
| A | `benchmark/arm-guided` | `/home/ly/cloudra-arm-guided` | `e67ef30abd8807297a7c4f095836eee3ee04bb77` | 是 | 干净，仅 `?? run.sh`（未跟踪） |
| B | `benchmark/arm-record` | `/home/ly/cloudra-arm-record` | `058fdc82907bc6f4a0dbf60a62dbc11e8865c701` | 是 | 干净，仅 `?? run.sh` |
| C | `benchmark/arm-standard` | `/home/ly/cloudra-arm-standard` | `79ca80bf8c3c2ea7a48e2cab1f8455a2fcccd55d` | 是 | 干净，仅 `?? run.sh` |
| D | `benchmark/arm-guided-brief-errors` | `/home/ly/cloudra-arm-brief-errors` | `0b81c2625fbf9a62e221deebe1b62ce74bd2330e` | 是 | 干净，仅 `?? run.sh` |

补充：

- 共享仓库 `/home/ly/cloudra-bench-20261019` 全程停留在 `docs/p0-acceptance`（HEAD `1e6d953f998848b2499f7a5e69df22842c3fd869`，与 `master` 相同）；本审计只在该仓库执行 `git show` / `git diff` / `git for-each-ref`，**未切分支**。
- 四个 `run.sh` 内容逐字节相同（`PYTHONPATH` 指本 checkout，解释器用共享仓库 `.venv`），但**均未提交**，因此不在任何 provenance 里。
- `__pycache__` 在审计前已存在（mtime 2026-10-22），本审计探针均带 `PYTHONDONTWRITEBYTECODE=1`，未新增/修改产品文件。

### 1.2 共同产品基线与分支差异（E18）

**实际共同产品基点 = master `1e6d953f`**：四臂都包含 `1e6d953f` 作为祖先（`git merge-base --is-ancestor` 全部为 YES，merge-base 即 `1e6d953f`）。计划 §九行 182 声明的共同基线 `8c568ca6753ecf2cd40a90a8f0f8b5c8e19dd1d2` 已过期：`8c568ca..1e6d953f` 之间还有两个**产品代码**提交（`e28d45e0`、`1e6d953f`，只改 `cloudra/tools/Chemtool/ts_guess.py`，+120/−16），另有 `0e4a840f`、`f5299b0a` 两个只改计划文档的提交。四臂在同步时都合并了这个最新 master（分支上可见“Merge light IDPP convergence metadata fix …”）。→ **冻结时必须写实际基点 `1e6d953f`（或四臂各自 HEAD），不能照抄 8c568ca。**

各臂相对 master 的整树差异（`git diff --stat master..<arm>`）：

| 臂 | 变更文件数 | 产品代码变更文件 | 说明 |
|---|---|---|---|
| A | 6 | `cloudra/benchmark/{runner,backend,batch}.py` | 仅 arm 接线 + provenance，无产品行为改动 |
| B | 11 | 上述 3 个 + `cloudra/dag/models.py` + `cloudra/dag/stop_audit.py` | B 的真实实验处理 = 模式常量 + record 结算放行 + 记录模式指引改写 |
| C | 21 | 12 个（`runner.py` + 11 个反馈/TS 相关） | 判定中性化实现 + verify 禁用 + 输出文档投影 |
| D | 19 | 12 个（`runner.py` + 11 个诊断投影接入点） | 只改公开反馈投影，结算/阈值/工具行为零改动 |

### 1.3 审计方法与证据等级

1. **代码直读**：直接读四个 checkout 的产品文件（非文档），所有结论附 `文件:行号`。
2. **git 只读比对**：在共享仓库用 `git diff <armA> <armB> -- <path>` / `git diff master <arm> -- <path>` 确认“哪些代码真的不同”。因 B/C/D 都基于 A 的共同提交，A↔B/C/D 的成对 diff 能精确定位处理因素。
3. **纯导入探针**（无模型、无网络）：
   - `tool_surface_probe.py`：打印 `ABLATION_ARM`、`_mode_hidden_tools()` 三模式集合、`dag_tools()` / `dag_review_decision_tools()`、`provenance_config()`；
   - `wire_visibility_probe.py` / `traditional_wire_probe.py`：构造 coordinator `AgentSession`，用真实 `wire_tool_schemas()` 与 `guest_tool_names()` 统计可见 `dag_*`；
   - `settlement_probe.py`：用临时 SQLite 构造真实 `DagController`，对 `complete`/`partial` 调 `audit_stop()` 与 `commit_stop()`，记录 action/basis/disposition 行；
   - `projection_probe.py`：直接调 C 的 `scientific_feedback` 与 D 的 `brief_errors` 投影函数，看输入→输出。
   输出均只写到 `/home/ly/cloudra-p0-probe/p0-behavior/`。
4. **聚焦用例（静态引用，未复跑）**：环境 `.venv` 无 `pytest`、系统也无 `pytest`，本次**没有复跑**任何测试；下列测试文件只作为“该分支自带的聚焦验收存在”的证据：A `tests/test_benchmark_arm_wiring.py`、B `tests/test_benchmark_record_advisory.py`、C `tests/test_benchmark_standard_tools.py` + `test_scientific_feedback_projection.py` + `test_c_feedback_boundaries.py`、D `tests/test_brief_error_projection.py`。这些用例的通过与否**不能替代本报告的代码结论**。

---

## 2. 四臂行为矩阵

### 2.1 主矩阵（每臂一行；证据编号见附录 A）

| 臂 | 分支 / HEAD（短） | 强制模式 `ABLATION_ARM` | DAG 工具可见（coordinator） | `ts_guess` verify/strict | Supervisor | 结算门实际行为（stop 审计） | partial 处理 | 错误/反馈详细度 | Provenance tag |
|---|---|---|---|---|---|---|---|---|---|
| **A** | `arm-guided` / `e67ef30a` | `DAG_GUIDED`（`dag_guided`）`runner.py:221` | **19/19 可见**（含 6 个 Supervisor 裁决工具，执行层按 actor 拒绝） | **可用**（`_verify`、strict 路径） | **在线**：草案/送审/退出审查触发；退出审查另有独立 final reviewer | `complete` 需 IRC 方向证明 + 交付物 + 覆盖，再交 Supervisor 终审（`wait_review`）；缺覆盖/IRC → `continue_work`；连续 3 次无进展 → run failed；`partial` 也需 Supervisor 接受 | Supervisor 接受后 basis=`supervisor_approved` → 标签 `partial`；写 disposition 行 + `.cloudra/mechanism_evidence.json` | full（原始诊断、完整修复引导、督导理由） | `experiment_arm=benchmark/arm-guided`、`error_feedback=full`；runs 行 `dag_guided` |
| **B** | `arm-record` / `058fdc82` | `DAG_RECORD`（`dag_record`）`runner.py:221` | **13/19 可见**；隐藏 6 个裁决工具（`dag_review_step/species/call/evidence`、`dag_accept_mechanism`、`dag_set_coverage_contract`） | **可用**（与 A 同一份 `ts_guess.py`） | **离线**：通知钩子在非 guided 直接 return；草案自动接受；无退出审查 | **advisory**：`complete`/`partial` 一律 `allow_final`（basis `declared` / `partial_recorded`），不检查覆盖/交付物/端点证据；保留后台未竟挂起与真实 user stop 校验 | 直接 `allow_final(partial_recorded)` → 标签 `partial`；写 disposition 行（report 如实保留缺口）；无交付物/端点证据 | full（与 A 同一套文本通道；但本臂没有督导裁决/退出审查消息） | `experiment_arm=benchmark/arm-record`、`error_feedback=full`；runs 行 `dag_record` |
| **C** | `arm-standard` / `79ca80bf` | `STANDARD`（`standard`）`runner.py:221` | **0/19 可见**（全部 `dag_*` 隐藏） | **禁用**：入口直接 `is_success=False`（`ts_guess.py:1355-1362`）；但输入 schema/描述仍宣传 verify | **离线**（比 B 更彻底：不创建 `DagController`、不加载 DAG 引擎） | **无 DAG 门禁**：stop 直接按模型声明结束，缺省 `allow_final(declared)`；无 disposition 行 | 仅模型声明；completion 标签 `unverified`；无 disposition/端点证据；评分仍按交付物独立进行 | 普通输出保留；TS **公开科学判定**中性化（`verified`/`outcome`→`null`，固定模板→`Scientific judgment not provided.`/`?`）；执行失败/数值/路径/DB 权威记录保留 | `experiment_arm=benchmark/arm-standard`、`error_feedback=full`、**`scientific_feedback=neutralized_public_verdicts`**；runs 行 `standard` |
| **D** | `arm-guided-brief-errors` / `0b81c262` | `DAG_GUIDED`（`dag_guided`）`runner.py:221` | **19/19 可见**（同 A） | **可用**（同 A） | **在线**（同 A） | **同 A**（结算/阈值/工具/权限零改动，仅投影模型可见文本） | **同 A**（Supervisor 终审后 basis=`supervisor_approved`，写 disposition 行 + 端点证据） | brief：失败上下文的 `error/message/reason/detail/next_action` 等 → `Diagnostic details omitted.`；保留 category/status/failure_class/数值/路径/native output；完成门反馈保留 gap 名/action/strike、删修复建议 | `experiment_arm=benchmark/arm-guided-brief-errors`、**`error_feedback=brief`**；runs 行 `dag_guided` |

补充口径：

- **强制注入点（四臂相同）**：`runner.ABLATION_ARM` → `task_project_settings()` 写入 project settings（`runner.py:224-231`）；CLI 后端 root spawn 与 Web 批次 root spawn 都显式传 `orchestration_mode=ABLATION_ARM.value`（`backend.py:186-200`、`batch.py:330-344`）；子 agent 继承父 agent 的 `orchestration_mode`（`child_settings.py:31-38,97-117`）；评分结果行与失败/取消行也写 `ABLATION_ARM.value`（`runner.py:411-417,550-558`、`batch.py:389-394,503-508,519-524`）。题目 JSON 的 `prompt.orchestration_mode`（`benchmark/schema.py:198`）在所有模式下都不再被产品代码读取（grep 无使用点），A 的 wiring 用例也断言了这一点（`tests/test_benchmark_arm_wiring.py:34-49`）。
- **DAG 工具“可见”的口径**：默认 `InvocationProtocol.JAVASCRIPT`（`schemas.py:139,212`）下，顶层 wire 只有 `js_exec` + direct 工具；`dag_*` 是 guest-callable 业务工具，因此“可见”= 能通过 `js_exec` 调用。传统协议下 wire 直接列出同样的 19/13/0 个。两种协议由探针实测一致。
- **A/D 的 6 个 Supervisor 裁决工具**虽然对 coordinator 可见，但执行层有第二道门：非 `DAG_GUIDED` 直接拒、非 `GraphActor.SUPERVISOR` 拒绝（`dag_review_step.py:55-61`；`_common.py:286-303`）。这是 A/D 共有的 master 行为，不影响 A/D 对比，但应在“工具集合”里登记。

### 2.2 DAG 工具可见性明细（E3、E4）

19 个 `dag_*` 来自 `cloudra/tools/registry.py:363-508`；6 个裁决工具由 `dag_review_decision_tools()` 定义（`capabilities.py:119-129`）。模式隐藏规则在 `cloudra/runtime_v2/tool_catalog.py:45-59`：`STANDARD → dag_tools()`（19 个）；`DAG_RECORD → dag_review_decision_tools()`（6 个）；`DAG_GUIDED → ∅`。`ask_user` 由 `_UNATTENDED_HIDDEN_TOOLS` 在 `unattended=True` 时隐藏（`tool_catalog.py:62-71`；benchmark 在 `runner.py:230` 固定 `unattended=True`）。

| 臂 | 生效模式 | 模式隐藏集合 | guest 可见 `dag_*` | 传统 wire 可见 `dag_*` | 隐藏的 6 个裁决工具 |
|---|---|---|---|---|---|
| A | `dag_guided` | ∅ | 19 | 19 | 无（可见但 actor 拒） |
| B | `dag_record` | 6 个裁决工具 | 13 | 13 | `dag_accept_mechanism`、`dag_review_call`、`dag_review_evidence`、`dag_review_species`、`dag_review_step`、`dag_set_coverage_contract` |
| C | `standard` | 全部 19 | 0 | 0 | 全部 |
| D | `dag_guided` | ∅ | 19 | 19 | 无（可见但 actor 拒） |

`ask_user` 在四臂的 wire 与 guest 都不可见（`unattended=True` + direct-only 双重原因）。C/D 的对比因此是“19 个 DAG 工具 vs 0”的整包差异；B/C 则是“13 个工具 + 独立 verify + 公开判定反馈”三因素整包差异——与计划 §二行 33 的混杂披露一致。

### 2.3 结算路径实测（E7、E19；`settlement_probe.py` 临时 DB 真实调用）

| 臂 | `audit_stop("complete")` | basis | `audit_stop("partial")` | basis | `commit_stop()` | `dag_delivery_dispositions` 行 |
|---|---|---|---|---|---|---|
| A | `continue_work`（report.complete=False, unresolved=1） | — | `wait_review`（已入退出审查队列） | — | 无（门禁未放行） | 0 |
| B | `allow_final`（report.complete=False 也放行） | `declared` | `allow_final` | `partial_recorded` | ok | 1（complete）/ 1（partial） |
| C | `allow_final`（report=None） | `declared` | `allow_final`（report=None） | `declared` | ok（无 pending，等价 no-op） | 0 |
| D | 同 A | — | 同 A | — | 无 | 0 |

说明：探针用空图 + 空沙箱验证“门禁判定与记录路径”，不涉及真实科学证据；A/D 在真实缺覆盖时同样走 `continue_work`，缺 IRC 时在 `stop_audit.py:279-289` 更早拦截。B/C 的“放行”不依赖图内容，这是其设计意图（advisory / 无 DAG），不是探针缺陷。

### 2.4 Provenance 字段明细（E15）

两处落库（CLI 与 Web 共用 `provenance_config()` 与 `BenchmarkDB`）：

1. `batches.config`（每批次一行）：`backend`、`experiment_arm`、`error_feedback`、C 另有 `scientific_feedback`、`orchestration_modes={task_id: mode}`、`models{coordinator:{provider,model}, follower:{provider,model}}`、`plugins`；CLI/Web 再补 `tasks_dirs`、`task_ids`、`concurrency`。
2. `runs`（每题一行）：`task_id/sandbox/graph_score/selfconsistency.../undelivered/final_score/notes/ts/batch_id/orchestration_mode`。

| 臂 | `experiment_arm` | `error_feedback` | `scientific_feedback` | `orchestration_modes`（50 题） | `runs.orchestration_mode` | 批次/行落库代码 |
|---|---|---|---|---|---|---|
| A | `benchmark/arm-guided` | `full` | — | 全部 `dag_guided` | `dag_guided` | `runner.py:244-246`；CLI `__main__.py:74-88`；Web `batch.py:160-165,186-189` |
| B | `benchmark/arm-record` | `full` | — | 全部 `dag_record` | `dag_record` | `runner.py:244-246`（B 值 `DAG_RECORD`） |
| C | `benchmark/arm-standard` | `full` | `neutralized_public_verdicts` | 全部 `standard` | `standard` | `runner.py:244-247`（C 多一行） |
| D | `benchmark/arm-guided-brief-errors` | `brief` | — | 全部 `dag_guided` | `dag_guided` | `runner.py:244-246`（D 值 `brief`） |

**缺项（P0 需在冻结清单补）**：无 git SHA/分支名自动落库（`experiment_arm` 是代码里的硬编码字符串）；无模型采样参数（temperature/reasoning_effort/max_tokens/context window）；无 Supervisor 独立模型记录；无任务文件哈希。见 §6 第 2 条。

### 2.5 C/D 反馈投影渠道对照（E12、E13）

| 模型可见通道 | 基线 A/B | C（科学判定中性化） | D（诊断文本压缩） |
|---|---|---|---|
| 传统协议 tool context | 原文 | `summary` 经 `project_scientific_tool_result`（`invocation.py:116-127`） | `summary`+`data` 经 `project_tool_result`（`invocation.py:116-128`） |
| JS guest ToolResponse | 原文 | 整个 result 投影（`js_protocol.py:219-235`） | 整个 result 投影，且先按原 payload/frame 做限额校验（`js_protocol.py:219-240`） |
| JS tool_error / 运行期错误 | 原文 | 不投影（执行错误保留） | `project_feedback(diagnostic=True)`（`js_protocol.py:243-250`；`js_runtime.py:295-297,571-574`） |
| 固定通知/pin/重放 | 原文 | `project_scientific_notice`（`notices.py:37,236,245,286,291,322`） | `project_notice`（`notices.py:35,236,245,286,291,322`） |
| 子 agent 完成报告 | 原文 | 不投影 | `project_feedback`+`project_notice`（`child_manifest.py:209-214`） |
| wait_approval / policy_blocked 文案 | 原文 | 不投影 | `brief_text`（`turn_pipeline.py:628-643`） |
| DAG 投影 payload | 原文 | C 无 DAG 投影 | `project_feedback(payload)`（`dag/models.py:1114-1117`） |
| `process.json` 导出 | 原文 | 投影副本（`ts_pipeline_store.py:109-119,306-346`；`ts_process.py:326-347`） | 投影副本（同位置改用 `public_process_record`） |
| 工具文档/声明 | 原文 | `public_tool_output_schema` 中性化 ts_guess/ts_process 输出声明（`tool_catalog.py:334-369`；`documentation.py:67,78`） | 不投影 |
| `ts_guess` verify 模式 | 可执行 | 入口拒绝 | 可执行 |

保留边界（审计用）：C 的未知混合科学散文不猜测、不改写（`scientific_feedback.py:43-45,216`）；纯文件权威记录（无 pipeline_id）不重写（`:365-368`）；D 的 native `bash/read/log_parser` 输出、`arguments/input/stdout/stderr/content` 等不压缩（`brief_errors.py:29-31,130`）；DAG evidence、退出审查 handshake manifest 保留（`brief_errors.py:88-90`）。残余可读通道见 `02_bc_diff.md` 与各分支 `docs/benchmark/*ABLATION.md`。

---

## 3. 逐臂证据与推导

### 3.0 四臂共用：强制模式、结算框架、评分输入

- **强制模式**：`ABLATION_ARM` 常量只出现在 `runner.py:221`；唯一注入链见 §2.1 补充口径。`task_project_settings()`（`runner.py:224-231`）同时固定 `benchmark_task_id`、`method_policy`、`defaults={yolo:true, unattended:true, clean_context:true}`。四臂的 `backend.py` / `batch.py` 逐字节相同（`git diff` 为空），A 的 `tests/test_benchmark_arm_wiring.py` 覆盖“题目 conflict 模式被覆盖、CLI/Web spawn、子 agent 继承、失败/取消行、provenance”（`:33-49,52-75,78-113,116-145,148-187`）。
- **结算框架**（四臂同一份代码路径）：runner 在收尾前统一调 `_evaluate_completion_gate()`（`agent_runner.py:785-856`），各 stage 的 `audit_run_end` 返回 `StopGate`；多域取最保守（`wait_background > wait_review > continue_work > allow_final`，`:824-826`）；无任何门禁意见时缺省 `allow_final(basis="declared")`（`:827-838`）。结论写 `agent.completion_gate` 事件（`:839-855`），completion 标签只由 basis 决定（`completion.py:30-37,69-77`）：`dag_verified→verified`、`supervisor_supported→supervisor_reviewed`、`supervisor_approved→partial`、`partial_recorded→partial`、其它→`unverified`。
- **评分输入**：四臂评分器代码相同（Lead 已核对 sha256，`00_lead_checks.md` §3）；`RunResult.orchestration_mode` 只记录不参与公式；`undelivered` 仅记录 `.cloudra/mechanism_evidence.json` 是否存在（`runner.py:419`），不参与 final 公式。
- **模型**：四臂无任何模型/配置代码差异（`git diff armA..armX -- cloudra/infra cloudra/cli.py config*` 为空）；模型来自运行时 config 槽位，provenance 只记 provider+model 名。coordinator 角色取 `config.coordinator` 槽，其他角色（含 supervisor）取 `config.follower` 槽（`adapters.py:84-108`）。

### 3.1 A（`benchmark/arm-guided`，full）

**推导过程**：先证明“A 只改接线、不改产品行为”——`git diff master..benchmark/arm-guided` 仅 6 个文件：`ABLATION_ARM.md`、`cloudra/benchmark/{runner,backend,batch}.py`、两个测试；`cloudra/benchmark/runner.py` 的差异只包含 import、`ABLATION_ARM`、把 `task.prompt.orchestration_mode.value` 替换为 `ABLATION_ARM.value`、加 `experiment_arm`/`error_feedback` 两个 provenance 字段。其余产品文件与 master 逐字节相同，因此 **A 的行为 = master 行为 + 强制模式**。

- **强制模式**：`ABLATION_ARM = OrchestrationMode.DAG_GUIDED`（`runner.py:221`）；注入点见 §2.1。
- **DAG 工具**：probe 显示 `_mode_hidden_tools(DAG_GUIDED)=∅`，guest/wire 可见 19 个（`tool_catalog.py:45-59`；`capabilities.py:106-129`；`registry.py:363-508`）。6 个裁决工具对 coordinator 可见但执行层 actor 拒绝（`dag_review_step.py:55-61`、`_common.py:286-303`）；Supervisor 自己的可见面走 `supervisor_tool_names()`（`agent_host.py:368-375`、`capabilities.py:157-186`）。
- **verify/strict**：`ts_guess.py:1390` 把 `"verify"` 映射到 `_verify`；`_verify` 实现于 `:2414-2492`（strict 分支 `:2474`），无模式门。
- **Supervisor**：通知触发点统一在 `dag/supervision.py:78-79`（非 guided 直接 return）；真实 spawn 在 `runtime_v2/supervision.py:220-264`（role=`supervisor`，settings 显式钉 `dag_guided`），退出审查走 `:306-331`，普通待办/笔记走 `:334-388`；Supervisor 不持有 `DagController`（`dag_stage.py:63-69`）；role 定义 `roles.py:93-109`。基准 watcher 对 `wait_review` 有专用存活判定（`watch.py:230-248`）。
- **结算门**：`stop_audit.py:243-265` 拒绝伪造 user stop；`:267-273` 后台未竟则挂起；`:279-289` complete 需满足短 IRC 方向证明；`:292-301` 交付物必须与 DAG 一致；`:324-330` 覆盖不完整则 `continue_work`；`:332-339` 的 partial 直通只对非 guided 生效，因此 guided 的 partial 落到 `:348-373` 退出审查（`wait_review`）；`:424-467` 复用已批准的退出裁决（partial 标签 basis `supervisor_approved`，`:451`）；`:496-539` commit 时复核状态/审批/交付物并写 disposition 与端点证据。runner 层：`continue_work` 连续 3 次无进展（`DEFAULT_MAX_EXIT_STRIKES=3`，`agent_runner.py:73,412-433`）→ run 以 failed 结束；`wait_review` → agent 进入 `WAITING_APPROVAL`（`:445-454`）。
- **partial**：见上；探针实测 partial=`wait_review`。commit 后写 `dag_delivery_dispositions`（表结构 `database.py:1113-1122`；写入 `store.py:242`）并在存在 delivery artifact 时写 `.cloudra/mechanism_evidence.json`（`stop_audit.py:535-538`；`delivery_evidence.py:76-86`；路径 `paths.py:60-62`）。
- **反馈**：full——A 未接任何投影；tool context 原文（`invocation.py:116-145`），通知原文（`notices.py` 无投影），完成门反馈含缺口+修复建议（`agent_runner.py:894-909`）。
- **Provenance**：见 §2.4。
- **计划表核对**：见 §5.1。

### 3.2 B（`benchmark/arm-record`，DAG advisory）

**推导过程**：B 相对 A 只有 3 个产品文件差异（`git diff A B -- cloudra/` 全部输出仅三处）：`runner.py` 两个常量字符串、`dag/models.py` 记录模式指引文案、`dag/stop_audit.py` 新增 `DAG_RECORD` 提前放行与 commit 分支。因此 B 的行为 = A 的 DAG_RECORD 模式 + 两处结算/指引改写。**注意：master 的 DAG_RECORD 原本仍会在 `complete` 时做覆盖审计**（A 的 `stop_audit.py:302-330` 在非 guided 时按覆盖通过/不足分别放行/continue），B 才把 record 变成真正 advisory；所以 B 不是“只换一个 mode 常量”。

- **强制模式**：`ABLATION_ARM = OrchestrationMode.DAG_RECORD`（`runner.py:221`）。
- **DAG 工具**：`_mode_hidden_tools(DAG_RECORD)` 隐藏 6 个裁决工具（`tool_catalog.py:57-58`；`capabilities.py:119-129`）；实测 guest/wire 各 13 个。`dag_propose_mechanism` 在 record 下**自动接受**（`drafts.py:499-510`），记录 actor `harness:auto`；`dag_accept_mechanism` 硬拒（`drafts.py:536-539`）。`dag_submit_step/species_evidence` 在 record 下由 HARNESS actor 直接挂快照、不建 review（`dag_submit_step_evidence.py:219-250`）；且对 TS 虚频数多做一道工具级校验（`:157-163`）。`dag_message_supervisor` **仍可见可调用**（`registry.py:499-508`；执行 `dag_message_supervisor.py:93-147`），但在 record 下只落 ReviewRequest、无人消费（`dag/supervision.py:78` 通知口关闭）——这是 B 的“死信通道”，不构成结算门，但应登记。
- **verify/strict**：与 A 逐字节相同的 `ts_guess.py`（`git diff A B -- cloudra/tools/Chemtool/ts_guess.py` 为空；`_verify` 在 `:2416`）。
- **Supervisor**：无。所有通知触发（提案/显式送审/笔记/退出审查）都在 `dag/supervision.py:78-79` 或 `stop_audit` 的 record 提前 return 处被切断；`_spawn_supervisor` 不会被调用。probe 的结算实验也证明了 record 分支不会产生退出审查请求。
- **结算门**：`stop_audit.py:267-273` 后台未竟仍 `wait_background`；`:243-265` 真实 user stop 校验保留；`:275-281` 对 `DAG_RECORD` **无条件 allow_final**，basis 为 `partial_recorded`（partial）或 `declared`（complete），**不执行** IRC 检查、交付物准备、覆盖判断；`:511-515` commit 只复核状态指纹并写 disposition，**不准备交付物、不写端点证据**。`complete` 时 report 里的缺口仍如实保留（探针显示 `report.complete=False` 也放行）。A 的 `tests/test_benchmark_record_advisory.py:18-49` 用 monkeypatch 证明 record 结算“不读科学证明/不建交付物/不写端点证据”；`:53-68` 证明保留后台挂起、真实 user stop 与并发状态保护。
- **partial**：`allow_final(partial_recorded)` → completion 标签 `partial`（`completion.py:35`）；disposition 行写入（探针 1 行）；无交付物/端点证据。
- **反馈**：full（与 A 同一套文本通道）；差异是**没有**督导裁决/退出审查这些消息（Treatment 的必然结果）。
- **Provenance**：`experiment_arm=benchmark/arm-record`、`error_feedback=full`、`orchestration_modes=dag_record`、runs 行 `dag_record`。
- **计划表核对**：见 §5.2。

### 3.3 C（`benchmark/arm-standard`，独立校验禁用 + 公开判定模糊化）

**推导过程**：C 相对 A 有 12 个产品文件差异，分三组：① `runner.py`（mode/provenance）；② **独立校验禁用**：`ts_guess.py:1352-1362` 在 `tool_call` 最前面拦截 `mode=="verify"` 或 `strict=True`，返回 `is_success=False`（`tests/test_benchmark_standard_tools.py:9-18` 静态证明 verifier 不会被调用，且 `interpolate/xtb_path/scan_parse` 仍可分发）；③ **公开判定中性化**：新增 `cloudra/runtime_v2/scientific_feedback.py`，并在 6 类出口接入（见 §2.5）。`git diff A C -- cloudra/dag/` 为空，`git diff A C -- cloudra/dag/{stop_audit,supervision}.py` 为空——C 没有改结算代码，它的“无结算”来自 mode=standard 使 `DagController` 根本不创建（`dag_stage.py:58-61`；`controller.enabled` 在 `STANDARD` 为 False，`controller.py:64-66`；`stop_audit.py:235-236` 是第二道兜底）。

- **强制模式**：`ABLATION_ARM = OrchestrationMode.STANDARD`（`runner.py:221`）。
- **DAG 工具**：`_mode_hidden_tools(STANDARD)=dag_tools()`（19 个全隐藏，`tool_catalog.py:55-56`）；实测 guest/wire 均 0。C 没有任何 DAG store/投影/证据登记路径；`enqueue_compute_review` 对 standard 直接跳过（`evidence_inbox.py:1422-1455`，其中 `:1454-1455` 只在 `dag_record` 注册审计行）。
- **verify/strict**：入口拒绝（`ts_guess.py:1355-1362`）。**残余不一致**：`TsGuess_input_schema` 仍保留 `mode="verify"` 与 `strict` 字段（`ts_guess.py:329-343`），工具描述仍写 `verify: ... strict=True ...`（`:98-99`），`:383-384` 校验器仍要求 verify 需要 `freq_log`；也就是模型仍会被文档引导去调一个必然失败的模式。C 分支 `ABLATION_ARM.md:19-22` 已自曝此点。
- **Supervisor**：无（同 §3.0 框架；C 连 `DagController` 都没有，`dag_stage.py:58-61`；`notify_supervisor` 只在 guided 钩子/退出审查/笔记路径被调用，C 都不经过）。
- **结算门**：无。runner 收尾时 `DagPolicyStage.audit_run_end` 返回 None（`:106-108`），最终缺省 `allow_final(basis="declared")`（`agent_runner.py:827-838`）；探针实测 complete/partial 都是 `allow_final/declared`、`report=None`。**不写 `dag_delivery_dispositions`，不写 `.cloudra/mechanism_evidence.json`。**
- **判定中性化实现**（`scientific_feedback.py`）：
  - 语义：`null` = “未提供判定”，既不是通过也不是失败（`:1-7,16-21`）；只投影“已识别的 TS schema/仓库自有模板”，未知混合散文不改（`:43-45,216`）。
  - TS view：`result.outcome`∈{verified,candidate_only}→`None`、`result.verified`→`None`、`result.reason` 走模板映射（`:267-273`）；`frequency_analysis` 的 alignment 判定→`None`（`:219-230`）；`available_results[].detail` 走模板（`:278-280`）。
  - 记录/历史：`terminal`∈{verified,candidate_only}→`None`、stage detail 模板化（`:233-246`）；诊断 `failure_class` 仅隐藏 `wrong_mode/endpoint_unconfirmed` 的展示标签（`:249-256`）。
  - ts_guess：`verification_status`→`None`、`verdict/message/imag_mode_alignment` 模板化、`imag_mode_aligned`→`None`（`:284-294`）。
  - 固定通知：`[Guidance] The target TS step remains unverified; ...`→`[Guidance] Judgment not provided; ...`；`Compute Event:` 的 `Physical Reality: outcome=...; verified=...` 壳被去掉、`NEXT:` 引导改写、`Advisory from ts_guess:` 模板化（`:323-362`）。
  - 出口：见 §2.5 表（`invocation.py:116-127`、`js_protocol.py:219-235`、`agent_runner.py:947-974`、`notices.py:37/236/245/286/291/322`、`ts_pipeline_store.py:109-119,306-346`、`ts_process.py:326-347`、`tool_catalog.py:334-369`、`documentation.py:67,78`、`ts_search_process.py:52`）。`ts_process.load_record` 改为优先读权威 DB（`:355-372`）——但该函数当前只被测试引用（产品代码无调用者），对正式运行无影响。
  - **残余可读通道**：native `read/bash`、原生日志标题与内容、DB/事件审计、旧上下文、纯文件记录、YOLO 审批事实、内部 TS 管线真实判定都未改写（`:1-7,22-31,365-368`；C 分支 `docs/benchmark/SCIENTIFIC_FEEDBACK_ABLATION.md:45-70`）。探针实测：`verified:false→null`、`candidate_only→null`、模板 reason→`Scientific judgment not provided.`，而 `imag_freqs`、`evidence_refs`、`stdout`、未知 verdict 文本原样保留。
- **反馈详细度**：普通输出保留；只有“公开科学结论”被中性化。**中性文本是英文** `Scientific judgment not provided.` / `?`，不是计划中文表述的“未提供判定”（见 §6 第 4 条）。
- **Provenance**：`experiment_arm=benchmark/arm-standard`、`error_feedback=full`、`scientific_feedback=neutralized_public_verdicts`（`runner.py:244-247`）、runs 行 `standard`。
- **计划表核对**：见 §5.3。

### 3.4 D（`benchmark/arm-guided-brief-errors`，简略报错 full）

**推导过程**：D 相对 A 有 12 个产品文件差异，全部是“接入 `brief_errors.py` 投影 + 记录投影”；`git diff A D -- cloudra/dag/stop_audit.py cloudra/runtime_v2/supervision.py` 为空，`cloudra/prompts/`、`ideapool/tasks/` 也零差异 → **D 的规则、阈值、工具、权限、结算门与 A 完全相同**，只有模型可见文本不同。该结论可用 `tests/test_brief_error_projection.py` 的用例意图交叉印证（`test_projection_is_pure_idempotent_and_preserves_controls_and_measurements` 等 28 个用例，静态引用未复跑）。

- **强制模式**：`ABLATION_ARM = OrchestrationMode.DAG_GUIDED`（`runner.py:221`）。
- **DAG 工具**：同 A（19/19 可见；`tool_catalog.py:45-59`）。
- **verify/strict**：同 A（`ts_guess.py` 与 A 逐字节相同）。
- **Supervisor / 结算门 / partial**：同 A（`stop_audit.py` 与 A 逐字节相同；探针实测 complete=`continue_work`、partial=`wait_review`）。
- **错误呈现**（`brief_errors.py`）：
  - 失败对象里的 `message/msg/summary/reason/detail/next_action/recovery_hint/...`→`Diagnostic details omitted.`（`:15-25,108-110`）；`error/last_error/error_message/planned_error/reject_reason` 一律压缩（`:23,91-92`）；`blocked/unresolved_gaps/validation_errors/...` 上下文递归压缩（`:24-25,118-123`）。
  - 保留：`failure_class`、`code/status/state/verdict/action` 等类别与结构化字段（`:56-59`）；数值、坐标、频率、stdout/stderr、`arguments/input/content` 等 opaque 字段（`:29-31,88-90`）；IRC 退出审查 handshake manifest（`:88-90`）；native 工具 `bash/read/log_parser` 的 summary 不压缩（`:130`）。
  - 已知精确类别保留：`Invalid tool arguments.`（`:38-41`）、`protocol_error[<category>]`（`:42-45`）；短于 `"Diagnostic details omitted."` 的文本用 `-` 占位（`:46`）。
  - 固定通知：`[Supervisor call/draft verdict]`/`[Supervisor review decision]` 保留 head+verdict、reason→`Diagnostic details omitted.`（`:164-168`）；`[Review superseded]` 同理（`:169-170`）；`[Completion gate]` 保留 action+缺口名+`Exit attempt n/3`、删除修复建议（`:171-180`）；compute 通知仅在明确失败时压缩 `Physical Reality:/Advisory/NEXT`（`:184-192,200-218`）。
  - 接入点：§2.5 表（`invocation.py:116-128`、`js_protocol.py:219-250`、`js_runtime.py:295-297,571-574`、`notices.py:35/236/245/286/291/322`、`child_manifest.py:209-214`、`turn_pipeline.py:628-643`、`dag/models.py:1114-1117`、`ts_pipeline_store.py:109-119,306-346`、`ts_process.py:326-346`、`agent_runner.py:947-974`）。
  - **审计保留口径**：raw tool result 在任何后处理之前落 `tool.result_recorded` 事件（`invocation.py:455-472`，D 未改该文件此段）；JS `program.finished` 在 D 投影前写入（`js_runtime.py:561-575`）。唯一注记：`js_exec` 返回给上层的 `ToolResult.data.error` 已是投影后的文本（`:571-574`），原文只在 `program.finished` 事件里——离线审计应以 `program.finished` 为准。
  - 残余：native 日志/文件、`bash/read`、混有测量与建议的旧 `checks/verdicts`（只映射一条已知独立 IRC 修复指令，`:100-107`）、DAG projection 中非诊断字段都保留。属于“更简略反馈”而非“全盲”。
- **Provenance**：`experiment_arm=benchmark/arm-guided-brief-errors`、`error_feedback=brief`、`orchestration_modes=dag_guided`、runs 行 `dag_guided`。
- **计划表核对**：见 §5.4。

---

## 4. 模型与提示差异登记（计划 §3.1 要求）

### 4.1 模型配置

- 四臂**没有**任何模型/配置代码差异：`git diff A..{B,C,D} -- cloudra/infra/ cloudra/cli.py cloudra/prompts/ ideapool/` 全部为空。模型来自运行时 `get_config()` 的 `coordinator` / `follower` 两个槽位（`adapters.py:84-108`：coordinator 角色用 coordinator 槽，其他角色含 supervisor 用 follower 槽）。
- benchmark 只把 `{provider, model}` 记入批次 provenance（`runner.py:247-250`）；**采样参数（temperature/reasoning_effort/max_tokens/context_window/timeout）不进 provenance**；Supervisor 无独立模型配置，也不单独记录。
- 当前环境探针读到的 config 值为 `deepseek / deepseek-v4-flash`（coordinator 与 follower 两槽相同）——这只是本机当前配置，**不是分支冻结值**；正式运行必须由冻结清单（`04_freeze.md`）锁定并记录。
- 计划要求的“同一模型及版本、推理设置”在代码层不会被分支强制，只靠运行时 config 一致；这是 P0 冻结项，不是代码缺陷。

### 4.2 提示/文档差异表

| 差异 | 是否处理因素 | 实际实现 | 备注/残余 |
|---|---|---|---|
| 记录模式行为指引 | B 处理因素 | B 改写 `_MODE_GUIDANCE[DAG_RECORD]`：明确“complete/partial 都可在缺科学覆盖/交付物/督导批准时结束；completion 不是科学验证”（`dag/models.py:972-988`；A 对应位置 `:972-987` 原文是“stop 前检查 dag_delivery_report、必须满足 required stages”） | 属必要提示差异，已登记；但计划表未提及 B 的 prompt 文案变化 |
| DAG 投影 | A/D 有，C 无 | `DagProjection.to_prompt_text()`（`dag/models.py:1098-1125`）；C 的 `DagPolicyStage.before_llm` 因 controller=None 直接 unpin（`dag_stage.py:244-249`），`prompt_projection` 不会生成 | 必要差异（C 无 DAG 工具）；但**公共 role prompt 仍指示 DAG 工具**（见下） |
| C 工具输出文档 | C 处理因素 | `public_tool_output_schema()` 把 ts_guess/ts_process 的 `verified/outcome/verification_status/imag_mode_aligned` 文档改成 `null`/中性（`tool_catalog.py:350-369`；`documentation.py:67,78`；`ts_search_process.py:52`） | 工具*输入* schema 未改（verify 仍在） |
| D 诊断文本 | D 处理因素 | DAG 投影 payload 与所有通知/工具结果边界压缩（§3.4） | 必要差异 |
| 公共 role prompt | 无处理 | `cloudra/prompts/` 四臂完全相同：`coordinator.md:15,17,19` 仍要求“In DAG mode, use dag_propose_mechanism / dag_submit_*_evidence / dag_delivery_report”；`small_mol.md:9,20` 仍要求“In DAG mode, bind completed evidence…” | **C/B 的提示不一致**：B 保留这些工具（仍可执行，一致）；C 隐藏全部 DAG 工具却仍有这些指引（模型会尝试不可用工具） |
| `stop` 工具描述 | 无处理 | `stop_tool.py:18-25` 描述仍是 guided 语义（“complete must pass evidence-derived coverage and final Supervisor review in dag_guided”） | B/C 下描述与真实结算不符（B/C 无 coverage/无督导），属残余提示差异 |
| 题目 JSON | 无处理 | `ideapool/tasks/**/*.json` 四臂相同，50/50 题 `prompt.orchestration_mode="dag_guided"`、`role="coordinator"`；该字段已不被产品读取（`schema.py:198` 仅定义） | 已由 arm 接线覆盖；但若有人用非 arm checkout 直接跑，标签会错 |

**必须登记的“必要提示差异”**：B 的 record 指引改写；C 的“无 DAG 投影 + 工具输出文档中性化”；D 的全文投影。**必须同时披露的“残余提示不一致”**：C 的公共 role prompt 仍指示 DAG 工具；C 的 `ts_guess` 仍宣传 verify；B/C 的 `stop` 工具描述仍是 guided 语义。计划 §3.1 只要求“必要差异单独登记、不暗中加入替代性指导”——以上差异没有暗中加替代指导，但需要在论文/P0 记录里写明。

---

## 5. 与计划 §二表格的核对结论（逐臂 verdict）

计划表原文语义（`ideapool/cloudra_four_arm_experiment_plan.md:22-25`）：A 完整版（校验工具保留、Supervisor/科学结算强拦截保留、原完整诊断）；B 无强制干预版（校验工具保留可自主调用、去掉 Supervisor 拦截且不因科学校验强行阻止结算）；C 独立校验禁用/判定模糊化版（独立 verify/strict 禁用、保留计算与原始数值、公开自动科学结论中性化、同 B 但 DAG 工具仍隐藏）；D 简略报错完整版（校验/结算同 A，只简化错误解释与修复引导）。行 27 明确“表内是实验目标，不是断言，必须用实际注册工具、角色启动、结算路径和 Agent 可见消息核验”。

### 5.1 A：**符合（Yes）**

- 校验工具：保留（verify/strict 可执行），工具面 19 个 DAG 工具全可见 → 符合“完整版”。
- Supervisor/强拦截：在线 + guided 结算门（IRC/交付物/覆盖 + 退出审查）+ 3 次无进展失败 → 符合“保留”。
- 错误反馈：full → 符合“原完整诊断与引导”。
- 唯一“意外”是**计划表没写、但属 master 共同行为**：A 的 coordinator 可见 6 个 Supervisor 裁决工具（执行层拒绝）；不影响 A 与 D 的对比，但要登记。
- 基线注记：A 产品行为 = master `1e6d953f`（含 ts_guess 的两次 post-8c568ca 提交），不是计划 §九的 8c568ca（§6 第 1 条）。

### 5.2 B：**符合（Yes，行为层面）——附 4 项需登记细节**

符合项：verify/strict 保留且可自主调用（与 A 同一份 `ts_guess.py`）；Supervisor 离线（`dag/supervision.py:78`；无退出审查）；不因科学覆盖强行阻止结算（`stop_audit.py:277-281`）；其余行为与 A 对齐（结算/评分/工具文档均同一套）。

需登记/非计划表字面：
1. B 的真实代码处理 = `ABLATION_ARM=dag_record` + **`stop_audit.py` 新增 record 提前放行** + **`models.py` record 指引改写**；不是“只换 mode 常量”。冻结 diff 时必须把这两个文件算进 B 的处理变量。
2. B 保留后台未竟挂起、真实 user stop 校验、并发状态保护（`stop_audit.py:243-273,507-510`），与计划“不把无强拦截扩大为无错误处理”（§八第 2 点）一致。
3. `dag_message_supervisor` 仍可见可调用，但无督导消费 → 只产生 ReviewRequest 审计行（死信）；`dag_submit_step_evidence` 在 record 下额外校验 TS 虚频数（`:157-163`），这是工具级校验、不是结算门。
4. B 的 prompt 增加“complete/partial 都可在缺覆盖时结束、completion 不是验证”的直言（`models.py:985-987`）——属必要提示差异，需登记。

### 5.3 C：**部分符合（Partially / Conditional）**——4 项残余

符合核心意图的 4 项：① 独立 verify/strict 禁用（`ts_guess.py:1355-1362`，且测试证明 verifier 不会执行）；② 计算与原始数值保留（C 只做展示投影，内部 `ts_process`/`scientific_feedback` 保留真实值；探针确认频率/证据路径/未知文本保留）；③ 公开自动科学结论中性化（`null`/`Scientific judgment not provided.`/`?`，探针确认）；④ DAG 工具隐藏、无 Supervisor、无强制结算（探针确认 `allow_final(declared)`）。

与计划表/验收口径的差异（需登记）：
1. **中性文本是英文**：代码用 `Scientific judgment not provided.` / `?` / `null`，计划写“`null` 或‘未提供判定’文本”。语义等价，但若验收脚本/论文口径按中文 grep 会对不上（§6 第 4 条）。
2. **verify 仍被文档宣传**：输入 schema/描述/校验器仍保留 verify 与 strict（`ts_guess.py:98-99,329-343,383-384`），只有执行层拒绝；模型可能浪费调用。C 分支 `ABLATION_ARM.md:19-22` 已披露，但计划表未列。
3. **公共提示不一致**：隐藏了全部 DAG 工具，但 `coordinator.md:15,17,19` 仍指示使用 `dag_propose_mechanism`/`dag_submit_*`/`dag_delivery_report`；`stop` 工具描述仍是 guided 语义（`stop_tool.py:18-25`）——B/C 共有，C 更严重（工具不可用）。
4. **结算记录比 B 更弱**：计划表说 C“同 B，但 DAG 工具仍隐藏”，实际 C 连 disposition 行都没有（无 `DagController`），completion 只有 `declared`/`unverified`；B 至少写 disposition 行并如实记 report。比较 B/C 的“交付状态/partial 记录”时不能假设同口径。
5. 混杂：C 与 B 的差集是“独立 verify + 公开判定投影 + DAG 工具整包”，计划行 33 已明确不能作为纯工具消融——与实际一致，需写入论文限制。

### 5.4 D：**符合（Yes）——附 2 项审计口径注记**

符合项：`git diff A D` 证明结算代码/督导/工具/阈值/权限/partial/评分零改动；`cloudra/prompts/` 与 `ideapool/tasks/` 零改动；仅 §2.5 的模型可见文本被压缩；`tests/test_brief_error_projection.py` 的用例意图覆盖“纯函数、控制项与测量不变、成功数据不变、JS 原限额先校验、审计 SQLite 保留”。

注记：
1. D 的投影也作用于 **Supervisor 裁决通知**与 **DAG 投影 payload** 里的诊断细节（`brief_errors.py:164-168`；`dag/models.py:1114-1117`）。这属于“错误解释与修复引导”，符合计划 §D 段的描述（`plan:43-57`），但论文需说明 D 的“简略”包括督导反馈，而不只是工具报错。
2. `js_exec` 的程序错误在返回给上层的 `ToolResult.data.error` 里已是压缩文本，原文只保留在 `program.finished` 事件（`js_runtime.py:561-575`）；离线审计与“原文可读”口径应以此事件为准（D 分支 `BRIEF_ERROR_ABLATION.md:39-46` 的“program events retain full diagnostics”成立，但 `tool.result_recorded` 里的 js_exec 结果不含原始诊断）。

### 5.5 汇总

| 臂 | 与计划表 | 主要差异/需登记 |
|---|---|---|
| A | **符合** | 共同基线应为 1e6d953f；coordinator 可见 6 个 supervisor 裁决工具（共同行为） |
| B | **符合** | 处理变量含 2 个 DAG 文件；`dag_message_supervisor` 死信通道；submit-step 工具级虚频校验；record 指引文案 |
| C | **部分符合** | 英文中性文本；verify 仍被 schema 宣传；公共 prompt 仍指示 DAG；比 B 更弱的结算记录；DAG 混杂（计划已披露） |
| D | **符合** | 督导/DAG 诊断也被压缩；js_exec 错误原文仅在 `program.finished` |

---

## 6. 差异、混杂与开放问题清单（P0 待处理）

按优先级排列；带“建议归属”的分册。

1. **[高] 计划声明的共同基线过期。** 计划 §九行 182 写 `8c568ca`，四臂实际共同产品基点是 master `1e6d953f`（`e28d45e0`+`1e6d953f` 两次提交改 `cloudra/tools/Chemtool/ts_guess.py`，+120/−16）。冻结清单必须写四臂各自 HEAD + 实际共同祖先 `1e6d953f`，并确认这些 ts_guess 改动属于“共同基线”而非某臂处理因素。建议归属：`04_freeze.md`（本报告给出事实）。
2. **[高] 在线 provenance 不自动记录 git SHA、模型采样参数、Supervisor 模型/消耗。** `experiment_arm` 是代码常量；`models` 只有 provider/model 名；无 temperature/reasoning_effort/max_tokens；Supervisor 用 follower 槽、无独立记录；`build_orchestration_config()`（`dag/models.py:1160-1174`）虽会构造 supervisor_model/prompt revision，但**当前没有任何调用者**（死代码），不会落库。正式运行前须由冻结清单补齐（外部记录），或 P0 决定加代码（本任务禁止改产品代码）。建议归属：`04_freeze.md` + `03_evidence_chain.md`。
3. **[中] C 的 verify/strict 只在执行层禁用，文档层未收口。** 输入 schema、工具描述、`@model_validator` 仍宣传 verify（`ts_guess.py:98-99,329-343,383-384`）；公共 role prompt 仍指示 DAG 工具（`coordinator.md:15,17,19`；`small_mol.md:9,20`）；C 的 `stop` 工具描述仍是 guided 语义（`stop_tool.py:18-25`）。这是残余提示不一致，需在 C 的行为说明与论文限制里登记；若 P0 要求“干净处理因素”，需评估是否改文档（当前不在任务范围）。建议归属：`02_bc_diff.md` + 本报告。
4. **[中] C 中性文本口径与计划措辞不一致。** 代码输出英文 `Scientific judgment not provided.` / `?`（`scientific_feedback.py:16,48`），计划写“`null` 或‘未提供判定’文本”。语义等价；需在验收脚本/论文中按实际英文文本核对，不要 grep 中文。建议归属：本报告 + `03_evidence_chain.md`。
5. **[中] B 的 `dag_message_supervisor` 是可见但无人消费的通道。** B 无督导（`dag/supervision.py:78` 关闭通知），但工具仍可见（`registry.py:499-508`）且可写 ReviewRequest（`dag_message_supervisor.py:93-147`）；这些请求在离线审计里是死信，不改变结算。需在 B 行为说明/论文中登记为“记录型副作用”，并检查是否有 agent 实际使用（Pilot 轨迹统计）。建议归属：`02_bc_diff.md`。
6. **[中] `undelivered` 标志不可跨臂同口径比较。** 唯一写入 `.cloudra/mechanism_evidence.json` 的路径是 A/D 的 guided `commit_stop`（`stop_audit.py:535-538`）→ B（提前 return）与 C（无 controller）永不写该文件；而 `undelivered` 正由该文件是否存在决定（`runner.py:419`）。因此 B/C 的 runs 行恒为 `undelivered=1`，与“是否诚实交付/是否有科学内容”无关。同时 A/D 的端点证据文件给 `selfconsistency.py:313-321` 提供 authored endpoint bindings（B/C 只能走 `discover_edge_proof` fallback，`:441-484`；缺失索引按 hint 处理、不判科学失败，`:443-445`）。报告“交付率/证据链”时必须按臂区分口径，或离线统一从交付物重新判定。建议归属：`03_evidence_chain.md`（本报告给事实）。
7. **[低] 四臂 `run.sh` 未提交但四份相同。** 作为实际启动入口（固定 PYTHONPATH/解释器/环境变量），建议把其内容与 sha256 纳入冻结清单，或改用已提交的启动方式。建议归属：`04_freeze.md`。
8. **[低] 计划表与实测的“C 同 B”是近似。** C 没有 disposition 行，B 有；C 的 completion basis 只有 `declared`，B 有 `declared`/`partial_recorded`。比较 B/C 交付状态时需说明。建议归属：`02_bc_diff.md`。
9. **[低] A/D 的 coordinator 可见 6 个 Supervisor 裁决工具。** 执行层 actor 校验会拒绝（`dag_review_step.py:55-61`），但模型会看到这些 schema；影响 prompt 长度/误调用率。属 master 共同行为，需在工具清单登记；若 P0 要求“干净工具面”，可评估隐藏（当前不改产品代码）。建议归属：本报告。
10. **[低] 题库 JSON 的旧 mode 标签未清理。** 50/50 题写 `dag_guided`；虽然 arm 接线覆盖了它，但任何从非 arm checkout（如 master/docs）启动的运行都会把它们当真实模式，且 provenance 会记错。建议在冻结说明中显式声明“必须从对应 arm checkout 启动”。建议归属：`04_freeze.md`。

---

## 7. 附录

### 附录 A：证据索引（E1–E20）

| ID | 结论 | 证据（文件:行号 / 命令 / 探针） |
|---|---|---|
| E1 | 四臂 HEAD/分支/工作区 | `git -C <arm> rev-parse HEAD`、`git rev-parse origin/<branch>`、`git status --porcelain`（2026-10-24 实测，见 §1.1）；共享仓库 `git for-each-ref` |
| E2 | 强制模式常量与注入链 | `cloudra-arm-*/cloudra/benchmark/runner.py:221`（常量）、`:224-231`（project settings）、`:234-252`（provenance）、`:411-417,541-558`（结果行）；`backend.py:30,186-200`；`batch.py:32-40,330-344,389-394,503-508,519-524`；`child_settings.py:31-38,97-117`；`agent_host.py:311-335,343-355`；`benchmark/schema.py:198`；A `tests/test_benchmark_arm_wiring.py:33-49,52-75,78-113,116-145` |
| E3 | DAG 工具可见性 | `runtime_v2/tool_catalog.py:45-59,139-158,161-189`；`tools/capabilities.py:106-129`；`tools/registry.py:363-508`；探针 `wire_visibility_probe.py`、`traditional_wire_probe.py` |
| E4 | ask_user 隐藏 | `tool_catalog.py:62-71`；`benchmark/runner.py:230`（unattended=True）；探针输出 `wire_has_ask_user=false, guest_has_ask_user=false` |
| E5 | verify/strict | A/B/D：`Chemtool/ts_guess.py:1390,2414-2492`（strict `:2474`）、`registry.py:292-297`；C：`ts_guess.py:1352-1362`，输入 schema `:329-343`，描述 `:98-99`，校验器 `:383-384`；C `tests/test_benchmark_standard_tools.py:9-31` |
| E6 | Supervisor 在线/离线 | `dag/supervision.py:78-79`；`runtime_v2/supervision.py:220-264,306-331,334-388`；`roles.py:93-109`；`dag_stage.py:63-69`；`stop_audit.py:348-373`；`drafts.py:499-510,532-539`；C：`dag_stage.py:58-61` |
| E7 | 结算框架（共用） | `agent_runner.py:73,405-454,785-856,894-909`；`policies/dag_stage.py:87-145`；`runtime_v2/completion.py:30-37,59-77`；探针 `settlement_probe.py` |
| E8 | A/D guided 门禁 | `dag/stop_audit.py:221-236,243-265,267-273,275-346,348-373,424-467,496-539`；`benchmark/watch.py:230-253` |
| E9 | B advisory 结算 | `dag/stop_audit.py:267-281,511-515,507-510`；`dag/models.py:972-988`；B `tests/test_benchmark_record_advisory.py:18-68` |
| E10 | C 无 DAG 门禁 | `policies/dag_stage.py:58-61`；`dag/controller.py:64-66`；`dag/stop_audit.py:235-236`；探针 `settlement_probe.py` |
| E11 | partial/交付记录 | A/D `stop_audit.py:332-373,424-467,496-539`；B `:277-281,511-515`；C 无（见 E10）；`completion.py:30-37`；`persistence/database.py:1113-1122`；`dag/store.py:242`；`benchmark/runner.py:419` |
| E12 | C 判定中性化 | `runtime_v2/scientific_feedback.py:1-7,16-31,43-45,216,219-230,233-256,259-295,298-320,323-362,365-368`；接入点见 §2.5；探针 `projection_probe.py`（C 输出） |
| E13 | D 诊断压缩 | `runtime_v2/brief_errors.py:15-31,34-46,56-59,72-124,127-149,152-197,200-218,221-225`；接入点见 §2.5；探针 `projection_probe.py`（D 输出） |
| E14 | D 控制项不变 | `git diff benchmark/arm-guided benchmark/arm-guided-brief-errors -- cloudra/dag cloudra/prompts ideapool` 为空；`js_protocol.py:219-240`（先按原限额校验）；D `tests/test_brief_error_projection.py`（28 个用例，静态引用） |
| E15 | Provenance | `runner.py:198-217,234-252,290-316,340-366`；`__main__.py:74-88`；`batch.py:160-165,186-189`；`adapters.py:84-108`；`dag/models.py:1160-1174`（死代码）；本报告 §2.4 |
| E16 | 提示/模型差异 | `git diff A..{B,C,D} -- cloudra/prompts ideapool/tasks cloudra/infra cloudra/cli.py` 为空；B `dag/models.py:985-987`；C `dag_stage.py:58-61,244-249`；`prompts/coordinator.md:15,17,19`；`prompts/small_mol.md:9,20`；`tools/Stoptool/stop_tool.py:18-25`；`benchmark/schema.py:198` |
| E17 | 端点证据/`undelivered` 不对称 | `dag/stop_audit.py:535-538`（A/D 写）；B 提前 return（`:277-281`）不可达；C 无 controller；`benchmark/delivery_evidence.py:76-86`；`persistence/paths.py:60-62`；`benchmark/selfconsistency.py:313-321,441-484`；`benchmark/runner.py:419`；50/50 任务 rubric 开启 `irc_connects_endpoints`（统计 `ideapool/tasks/*/*.json`） |
| E18 | 共同基线 | `git merge-base --is-ancestor 1e6d953f HEAD`（四臂 YES）；`git log 8c568ca..1e6d953f`；`git diff --stat 8c568ca 1e6d953f -- cloudra/`（ts_guess.py +120/−16）；计划 `ideapool/cloudra_four_arm_experiment_plan.md:182` |
| E19 | 探针方法与输出 | `/home/ly/cloudra-p0-probe/p0-behavior/{tool_surface_probe,wire_visibility_probe,traditional_wire_probe,settlement_probe,projection_probe}.py`；§2.3 表；§3.3/§3.4 引用的投影输出 |
| E20 | 计划表原文 | `ideapool/cloudra_four_arm_experiment_plan.md:22-25`（表）、`:27`（不是断言）、`:29-33`（C 定义与混杂）、`:43-57`（D 边界）、`:143,146`（P0 清单）、`:182`（冻结基线） |

### 附录 B：探针命令（可复现，均无模型调用）

```bash
# 1) 四臂工具面 / 强制模式 / provenance（纯导入）
for arm in guided record standard brief-errors; do
  PYTHONPATH=/home/ly/cloudra-arm-$arm \
  CLOUDRA_DATA_DIR=/home/ly/cloudra-p0-probe/p0-behavior/probe-data \
  PYTHONDONTWRITEBYTECODE=1 \
  /home/ly/cloudra-bench-20261019/.venv/bin/python \
  /home/ly/cloudra-p0-probe/p0-behavior/tool_surface_probe.py
done
# 2) 真实 wire/guest 可见面（构造 coordinator AgentSession）
#    见 wire_visibility_probe.py（JS 协议）与 traditional_wire_probe.py（传统协议）
# 3) 结算门实测（临时 SQLite + 真实 DagController.audit_stop/commit_stop）
#    见 settlement_probe.py；输出即 §2.3 表
# 4) C/D 投影函数实测
#    见 projection_probe.py；C 输出：verified→null、candidate_only→null、
#    "fail: the strict check requires exactly one imaginary frequency."→
#    "Scientific judgment not provided."、imag_freqs/stdout 原样；
#    D 输出：失败上下文 message/reason/next_action→"Diagnostic details omitted."、
#    protocol_error category 保留、freq/路径原样、完成门保留 gap 名与 strike。
```

### 附录 C：未复跑项与限制

- **未跑 pytest**：共享 `.venv` 与系统 Python 均无 `pytest`（`python -m pytest` → `No module named pytest`）；为遵守“只读审计、不改环境”，未安装依赖、未复跑任何分支测试。文中所引测试仅证明“分支自带的聚焦验收存在”，不代表本次已通过。
- **未跑正式 benchmark / 空后端批次**：本报告的行为结论来自代码直读 + 纯导入/临时 DB 探针；Lead 的空后端批次结果见 `00_lead_checks.md` §4。
- **未做真实模型/计算观察**：四臂“实际行为”在本次审计中指代码路径行为；模型是否真的调用某工具、督导是否真的产生额外轮次，需要在 Pilot（P1）用轨迹验证（对应计划 §5.2 的“行为分析优先使用可审计事件”）。
- **未污染正式数据目录**：本审计未写入 `/home/ly/cloudra-bench-run6-20261021`、`/home/ly/cloudra-bench-full-20261022`；探针数据全部在 `/home/ly/cloudra-p0-probe/p0-behavior/`。
- **未切分支/未改产品代码**：共享仓库与四个 arm checkout 的分支/HEAD 均未改变；唯一写入的仓库文件是本报告。
