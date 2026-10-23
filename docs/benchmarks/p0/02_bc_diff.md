# P0-2 · B/C 真实差集与残余回流验收

- 审计对象：B = `benchmark/arm-record` @ `058fdc82907bc6f4a0dbf60a62dbc11e8865c701`；C = `benchmark/arm-standard` @ `79ca80bf8c3c2ea7a48e2cab1f8455a2fcccd55d`；共同祖先（merge-base）= `1e6d953f`（= `docs/p0-acceptance` 当前 HEAD）。
- 共享仓库 `/home/ly/cloudra-bench-20261019` 未切分支；所有跨分支读取用 `git show <branch>:<path>` / 臂克隆 `/home/ly/cloudra-arm-record`、`/home/ly/cloudra-arm-standard` 完成。
- 代码引用格式：`文件:行号`（默认指两臂中变化处；未注明分支且该文件两臂同文时，行号通用）。全程只读，未跑 LLM/付费计算，未改产品代码。
- 本文只回答四件事：① 差集是什么；② C 还能从哪里把判定漏出来；③ 除“验证工具”外还有哪些混杂；④ 哪些差异本不该存在。

---

## 0. 结论摘要（先给判定）

1. **差集不是“一处开关”，而是一个六类内容打包的臂差**：编排模式常量（DAG_RECORD→STANDARD）、DAG 工具可见面（C 隐藏 19/19，B 只隐藏 6/19）、结算语义（B 有 DAG 咨询式审计并落 disposition；C 无 DAG 审计、仅 runner 兜底 `declared`）、独立 `ts_guess` verify/strict（B 可用 / C 硬拒）、公共科学判定投影层（C 独有 `scientific_feedback.py` 及其 6 个出口 hook）、以及 prompt/通知差异。另有 4 处 C-only 运行时路径改动（见 §5）。
2. **B-vs-C 不能解释为纯“科学验证工具”消融**。可归因给该包的因素只有：(a) 独立 `ts_guess` verify/strict 的可用性；(b) 自动科学结论是否公开反馈（这是反馈通道处理，不是工具；C 内部自动判定仍在跑）。其余至少 5 项（DAG 工具面、DAG 内建科学校验反馈、结算/partial/后台等待、模式提示与工具契约、C-only 运行时改动）不可归因。计划表的文字必须按“包比较”改写（C 自己的 `docs/benchmark/SCIENTIFIC_FEEDBACK_ABLATION.md:62-66` 也只承认 DAG 混杂，未列全）。
3. **C 的官方出口大体被封堵，但不是“盲化”**。`verified/candidate_only/pass/fail` 在工具上下文、JS ToolResponse、通知渲染、process.json 导出、get_tool_docs 输出契约、非 user 消息这几条正式通道上被置空/改写（§3.1 有中性化代码）；但 raw DB / event log / 旧 process.json / 子 agent 文本 / YOLO 审批上下文 / 未知混合文本 / scan_parse 判定 / `structures.binding_status` 仍能回流判定或判定线索；bash 无路径围栏 + arm 环境变量/源码目录可进一步暴露臂身份（§3.2、§3.3）。
4. **不存在模型配置、任务 prompt、评分代码的意外差异**：23 个差异文件全部为臂处理/测试/文档；`ideapool/tasks/**` 零 diff；`cloudra/benchmark/runner.py` 只有 3 增 2 删（模式常量与 provenance）；config 类文件零 diff；`cloudra/benchmark/` 下除 runner.py 无 diff（§5.1）。
5. **发现 4 处“本该不存在/需复核”的差异**：C 工具契约里出现实验身份文本（`In this C experiment...` / `...in this arm`）、C 改了 DAG_RECORD 引导但 C 实际从不使用 DAG_RECORD（死代码 diff）、`load_record` 由文件权威改为 DB 权威（执行语义变更，超出“公共展示”范围）、JS 双编码 + 非 user 消息全量内容投影（行为/性能副作用）（§5.2）。provenance 增加 `scientific_feedback` 标记属预期，不算意外。

---

## 1. 差集的证据口径

```text
$ git -C /home/ly/cloudra-bench-20261019 diff --name-status benchmark/arm-record..benchmark/arm-standard
M ABLATION_ARM.md
M cloudra/benchmark/runner.py
M cloudra/dag/models.py
M cloudra/dag/stop_audit.py
M cloudra/runtime_v2/agent_runner.py
M cloudra/runtime_v2/invocation.py
M cloudra/runtime_v2/js_protocol.py
M cloudra/runtime_v2/notices.py
A cloudra/runtime_v2/scientific_feedback.py
M cloudra/runtime_v2/tool_catalog.py
M cloudra/services/ts_pipeline_store.py
M cloudra/tools/Chemtool/ts_guess.py
M cloudra/tools/Chemtool/ts_search_process.py
M cloudra/tools/core/ts_process.py
M cloudra/tools/documentation.py
A docs/benchmark/SCIENTIFIC_FEEDBACK_ABLATION.md
...（tests/ 共 7 个文件）
```

关键“同文”事实（差集由模式驱动，而非拷贝代码）：

- `cloudra/runtime_v2/tool_catalog.py` 的 `_mode_hidden_tools`、`cloudra/tools/capabilities.py`、`cloudra/tools/registry.py`、`cloudra/runtime_v2/policies/dag_stage.py`、`cloudra/runtime_v2/policies/schedule_stage.py`、`cloudra/runtime_v2/supervision.py`、`cloudra/runtime_v2/completion.py` **两臂字节一致**（不在 diff 列表；逐文件 `diff -q` 已验证）。工具面差异完全来自 `agent.settings.orchestration_mode` 的取值。
- 两臂各自合并了 master/light-IDPP 修复（B 的合并点 `93583c2d`/`c0ae7798`/`058fdc82`，C 的 `a4cc273c`/`062bace1`/`79ca80bf`），但最终树差异被限制在上述 23 个文件内 → **无无关 master 内容差异**。差异提交：B 独有 `0e84212b benchmark(arm-record): DAG as an advisory tool` + 三个 merge；C 独有 `ab4e2119 benchmark(arm-standard): tools without chemistry verdicts`、`ebdbdfb7 benchmark(C): neutralize public scientific conclusions without changing evidence` + merge。

---

## 2. 精确差集 B vs C

### 2.1 模式常量与 provenance（根因）

| 项 | B（arm-record） | C（arm-standard） |
|---|---|---|
| 编排模式常量 | `cloudra/benchmark/runner.py:221` `ABLATION_ARM = OrchestrationMode.DAG_RECORD` | `cloudra/benchmark/runner.py:221` `ABLATION_ARM = OrchestrationMode.STANDARD` |
| 每任务注入 | `runner.py:226-231` `settings["orchestration_mode"] = ABLATION_ARM.value`（项目创建、root spawn、子 agent 继承、batch 混入、结果行都用它；`backend.py:195`、`batch.py:339/393/506/522`、`runner.py:416/554`） | 同上，值改为 `standard` |
| batch provenance arm 名 | `runner.py:244` `"experiment_arm": "benchmark/arm-record"` | `runner.py:244` `"experiment_arm": "benchmark/arm-standard"` |
| provenance 额外标记 | 无 | `runner.py:246` `"scientific_feedback": "neutralized_public_verdicts"` |

模式在运行时的作用点（两臂同文）：

- 工具投影：`cloudra/runtime_v2/tool_catalog.py:177-182` `hidden = _mode_hidden_tools(agent.settings.orchestration_mode) | ...`；JS guest 侧同类过滤 `tool_catalog.py:151` + `:139-158`。
- DAG 控制器：`cloudra/runtime_v2/policies/dag_stage.py:58-61`，`if mode.value == "standard": return None` → **STANDARD 下整个 DAG 策略阶段为空转**（`audit_run_end` 返回 None、`on_run_end` 不提交、`before_llm` 只 `unpin("dag")`、`after_tool` 不观察工具调用）。DAG_RECORD 下则构造 `DagController(mode=DAG_RECORD)` 并进入 `StopAuditMixin`。

### 2.2 工具可见面（`_mode_hidden_tools` + capability groups）

定义（两臂同文，B/C 行号相同）：

- `cloudra/runtime_v2/tool_catalog.py:45-59`：

```python
def _mode_hidden_tools(orchestration_mode) -> frozenset[str]:
    mode = OrchestrationMode(orchestration_mode)
    if mode is OrchestrationMode.STANDARD:
        return dag_tools()                     # C：隐藏全部 19 个 DAG 工具
    if mode is OrchestrationMode.DAG_RECORD:
        return dag_review_decision_tools()     # B：只隐藏 6 个 Supervisor 裁决工具
    return frozenset()
```

- capability 组：`cloudra/tools/capabilities.py:106-116` `dag_tools()` = `module.startswith("cloudra.tools.Plantool.dag_tools.")` 的 19 个；`:119-129` `dag_review_decision_tools()` = `supervisor_access == "review_decision"` 的 6 个；`:60-81` `config_disabled_tools()`（flower/email 门，两臂相同）；`:89-103` `role_hidden_tools()`（两臂相同）；`:132-139` `is_direct_only`。
- registry 中 19 个 DAG 工具与 6 个 `review_decision` 标记：`cloudra/tools/registry.py:362-508`（如 `dag_view:363-369`、`dag_delivery_report:370-377`、`dag_bind_evidence:415-421`、`dag_submit_step_evidence:429-435`、`dag_submit_species_evidence:436-442`、`dag_review_evidence:475-482`、`dag_message_supervisor:499-508`）。两臂 registry 字节一致。

| 层面 | B（DAG_RECORD） | C（STANDARD） |
|---|---|---|
| hidden 集合 | 6 个（`dag_review_step`、`dag_review_species`、`dag_accept_mechanism`、`dag_review_call`、`dag_review_evidence`、`dag_set_coverage_contract`） | 19 个（全部 `dag_*`） |
| 模型可见的 DAG 工具 | **13 个**：`dag_view`、`dag_delivery_report`、`dag_add_species`、`dag_add_step`、`dag_update_delivery_element`、`dag_remove_edge`、`dag_remove_node`、`dag_bind_evidence`、`dag_propose_mechanism`、`dag_submit_step_evidence`、`dag_submit_species_evidence`、`dag_view_evidence`、`dag_message_supervisor` | **0 个** |
| wire 投影 | `wire_tool_schemas` 过滤（JS 模式下业务工具不进 wire，仅进 `javascript_instructions` 的 capability manifest：`tool_catalog.py:218-223,259-260,269-277`） | 同机制；manifest 少 13 行 |
| guest 可调用 | `guest_tool_names`（`tool_catalog.py:139-158`）含 13 个 DAG 工具 | 不含 |
| 执行层兜底 | 6 个裁决工具若被调用会因 supervised-only 硬拒（`supervision.py:78-80` 的 `DAG_GUIDED` 门） | 19 个 DAG 工具若被调用硬拒：`cloudra/tools/Plantool/dag_tools/_common.py:294-295` `"disabled in standard orchestration mode"`，入口处 `dag_view.py:66-68` / `dag_delivery_report.py:41-42` 等 |
| unattended 门 | `ask_user` 隐藏（`tool_catalog.py:62-71`），两臂相同 | 相同 |

> 注意：C 的可见工具数少 13 个，但**业务化学工具完全一致**（除 `ts_guess` verify/strict 行为，见 2.5），未隐藏任何 `ts_*`、`log_parser`、`qm_input_writer`、`submit_compute_job`。

### 2.3 结算路径（stop_audit / runner / schedule）

| 项 | B | C |
|---|---|---|
| DAG 阶段是否参与运行结束门禁 | 是（DAG_RECORD 控制器） | 否（`dag_stage.py:58-61` 标准模式直接 None；`audit_run_end:106-108` 返回 None） |
| 咨询式提前放行 | `cloudra/dag/stop_audit.py:275-281`：`if self.mode is DAG_RECORD: ... allow_final ... reason='record arm: DAG is advisory; delivery is not gated'`, basis=`declared`/`partial_recorded` | 该分支被删除（C 文件 `:275-290` 直接进入完整 DAG 审计逻辑）；但对 C 的 STANDARD 运行**不可达**，真正原因是模式 |
| 结算提交（落 disposition） | `stop_audit.py:501-515`：DAG_RECORD 下 `commit_stop` 走 `store.record_delivery_disposition(...)`，写 `dag_delivery_dispositions` 后返回 | 无 C-DAG 提交（`on_run_end` 无控制器）；C 的 `:496-506` 已无 record 分支 |
| 实际运行结束判定 | `AuditRunEnd` 收集各 stage 判定，取最保守（`agent_runner.py:814-826`）：B 得到 DagPolicyStage 的 `allow_final/declared`（reason 见上），事件 `source="dag"` | 仅剩 fallback：`agent_runner.py:827-838` `StopGate(action="allow_final", ..., basis="declared")`，事件 `source="declared"`、reason=“no completion gate applies to this agent; the run ends as an agent-declared result (not independently verified)”。`ScheduleStage`（`schedule_stage.py:126-163`）默认 `schedule_mode=False`（`schemas.py:133`），对 coordinator 无判定；仅非 coordinator 且有 owned compute 时返回 `wait_background` |
| 后台等待 | `stop_audit.py:199-219` `_has_pending_background()`：项目级 compute jobs + running siblings + reminders，任一真则 `wait_background`（`:260-273`） | coordinator 无此检查（`_owned_compute_pending` 对 coordinator 直接 False，`schedule_stage.py:165-175`）；只有 benchmark watcher `backend.py:236-248` 在 run 结束后兜底 |
| completion basis 记录 | `basis=declared`（complete）或 `partial_recorded`（partial）；`cloudra/runtime_v2/completion.py:30-37` → `verification_label` | `basis=declared`；partial 声明**不产生** `partial_recorded`，`verification_label` 只会是 `unverified` |
| partial 语义 | B：partial 也放行且**落库**（`stop_audit.py:277-281`，另 `:337-344` 是 non-guided 通用 partial 路径，被前面的 record 短路先命中）；`commit_stop` 写 disposition | C：`stop` 工具的 `delivery_disposition` 参数仅被 `DagPolicyStage.audit_run_end` 读取；C 无控制器 → 参数对结算**零作用**；`stop` 工具本身只返回回执（`cloudra/tools/Stoptool/stop_tool.py:62-71`），`stop_tool.py:18-26` 的 DAG 语义描述对 C 不成立 |

### 2.4 Supervisor

| 项 | B | C |
|---|---|---|
| 是否创建 Supervisor | 否。`supervisor` 角色只属于 `dag_guided`：`cloudra/runtime_v2/roles.py:92-108`（description 明说 guided；default settings 钉 `DAG_GUIDED`）；唯一 spawn 点 `supervision.py:220-264`（`:252` 显式 `settings={"orchestration_mode": "dag_guided"}`），只从 guided 路径被调用（`dag_stage.py:205-230` guided 分支、`stop_audit.py:366-368` guided wait_review、`compute_notify.py:287-290` guided observation、`supervision.py:334+` 的 notify）。B/C 都不满足 | 同左（也不创建） |
| DAG 事件/通知钩子 | `supervision.py:78-80` `if self.mode is not DAG_GUIDED: return`；通知/复核全部 guided-only | 同 |
| 对模型的 supervisor 提示 | B 的 `DAG_RECORD` 模式横幅写 “Supervisor is offline”（`cloudra/dag/models.py:972-973`） | C 无横幅（DAG 投影从不 pin） |
| 可见的 Supervisor 工具 | 6 个 `review_decision` 工具被隐藏（见 2.2） | 19 个全隐藏 |

> 结论：supervisor 不是 B/C 差异项（都没有），但工具面差异把本应“guided-only”的 6 个裁决工具在 B 中隐藏、在 C 中随 19 个一起消失——属同一 mode 机制。

### 2.5 `ts_guess` verify/strict 可用性

| 项 | B | C |
|---|---|---|
| `mode` 输入枚举 | `cloudra/tools/Chemtool/ts_guess.py:199-215`：含 `"verify"`（且描述仍宣传 verify=frequency+IRC 验证） | **同样含 `"verify"`（未改）**，见 `ts_guess.py:199-215` |
| `strict` 字段 | `ts_guess.py:340-346`，默认 `False`，描述 strict verify 的 pass/fail 语义 | **同样保留**（`:340-346`） |
| 工具入口门控 | 无。`tool_call` 直接 `if user_input.run_id is not None: ...`（`ts_guess.py:1352-1357`） | 新增 `ts_guess.py:1352-1362`：`if user_input.mode == "verify" or bool(user_input.strict): return TsGuess_output_schema(is_success=False, message="Verification is disabled in this ablation arm. Inspect the native frequency/IRC logs yourself.")` |
| 其他模式 | 不变 | 不变（`interpolate`/`xtb_path`/`scan_prepare`/`scan_parse`/`provided` 全可用；`scan_parse` 等仍返回自动扫描判定） |
| 内部自动 TS 管线的判定 | 不变 | **不变**：`cloudra/tools/core/ts_process.py:3200-3343` `_verdict()` 照旧计算 `verified`/`candidate_only` 四态，`ts_guess` 工具门控不经过该路径（内部只调 `TsGuess()._scan_prepare/_scan_parse`，`ts_process.py:1243/1301`） |
| 输出文档契约 | 原始 schema 渲染（`tool_catalog.py:346` `_json_schema(output_schema)`；`documentation.py:78` raw `model_json_schema()`） | 中立化契约：`tool_catalog.py:350-369` `public_tool_output_schema()` 把 `TsVerdict.verified` 改为 `type:null`、`outcome` 枚举限定 `search_failed/invalid_input/null`，`TsGuess_output_schema.verification_status` 枚举 `["", None]`、`imag_mode_aligned: null`；`documentation.py:67,78` 同步使用 |

### 2.6 C 独占：公共科学判定投影层（`scientific_feedback.py`）与 6 个接缝

新文件 `cloudra/runtime_v2/scientific_feedback.py`（368 行，C 独有），核心语义：

- 识别三类已知 schema：`_is_view`（`:31-33`，TsProcessView：`{run_id, revision, run_dir, stage, status, result}`）、`_is_record`（`:35-37`，process 导出）、`_is_guess`（`:39-40`，`{is_success, verification_status, verdict, n_imag, imag_freqs}`）。
- `_SCIENTIFIC_OUTCOMES = {"verified","candidate_only"}`（`:17`）；`_JUDGMENT_WORDS = {verified,candidate_only,candidate,pass,fail,inconclusive,unlikely,aligned,misaligned,undecidable}`（`:18-21`）→ 文本命中整词时替换为 `"?"`，schema 字段置 `None`；`_RAW_FIELDS`（`:22-28`）含 `input/arguments/content/stdout/stderr/declarations/native_output/.../structures/geometry/coordinates/methods/calculation/method_contract/method_checks/diagnostics`，这些子树**原样保留**（“声明、原生物料、原始证据不是公开诊断”）。
- `_observed_text`（`:43-216`）只改写**仓库自有固定模板**（frequency/IRC/endpoint/advisory 等约 30 条精确串），未知混合散文原样返回（`:216` `return text`）。
- 出口 hook（C-only）：
  1. 传统工具上下文：`cloudra/runtime_v2/invocation.py:125-127` `summary = project_scientific_tool_result(result).summary`（B 为 `:126` `summary = result.summary`）。
  2. JS guest ToolResponse：`cloudra/runtime_v2/js_protocol.py:219-235` 先按原始帧做协议校验，再 `result = project_scientific_tool_result(result)`，再编码（B 无投影，`:219-230`）。
  3. 通知渲染：`cloudra/runtime_v2/notices.py:37` 引入 `project_scientific_notice`；在 `render_current:232-239`、`_render_change:243-267`、`collect_batch:269-349`（fresh 全量 `:284-296`、增量 `:320-346`）统一投影；事件里存的仍是原文。
  4. TS process 工具输出（prepare/resume/inspect/stop 共用 `TsProcess_output_schema` → `TsProcessView`）：由出口 1/2 统一投影；`_to_output` 走 `inspect_process`（`ts_search_process.py:70-77`）。
  5. 持久导出 process.json：`cloudra/tools/core/ts_process.py:343-348`（save_record）、`cloudra/services/ts_pipeline_store.py:112-120`（revision export）、`:343-346`（stop_process）→ `public_scientific_record`（B 分别写 raw：`ts_process.py:344`、`ts_pipeline_store.py:116`、`:341`）。
  6. 公共工具文档：`cloudra/tools/documentation.py:67,78` + `tool_catalog.py:350-369`。

### 2.7 Prompt / 通知差异（对模型可见）

| 通道 | B | C |
|---|---|---|
| 每轮 DAG 图投影 pin | `dag_stage.py:239-258` 在 `before_llm` 里 `controller.prompt_projection()` 后 `notices.pin(agent.id,"dag",projection)`；内容 = `models.py:1099-1126` 模式横幅 + stage glossary + 图投影（`completion.py:441-484` `build_projection`：`delivery_gaps` 含 gate code/detail、`pending_reviews`、`recent_mutations`）。B 的模型**每轮**都能看到科学缺口明细（如 “evidence level is X”“requires Y, found Z”、short_irc 检查失败原因） | 无：`dag_stage.py:244-249` 控制器 None → `notices.unpin(agent.id,"dag")`；模型看不到任何 DAG/覆盖信息 |
| 模式横幅 | `models.py:972-988` DAG_RECORD 横幅（“DAG is recorded by the system; Supervisor is offline… dag_delivery_report records scientific coverage…completion is not scientific verification”） | 无任何模式横幅（STANDARD 不在 `_MODE_GUIDANCE`，且无投影出口） |
| 工具清单/manifest | `javascript_instructions`（`tool_catalog.py:205-266`）的 capability manifest 含 13 个 DAG 工具名称+用途 | 不含 DAG 工具 |
| TS 输出契约 | 原始 schema（含 `verified: boolean`、`outcome: verified|candidate_only|...`） | 中立契约（`verified: null`；`outcome` 仅 execution 失败类；描述含实验身份文本，见 §5.2） |
| 通知 | 原文渲染（B 无投影层） | 渲染时投影：`Physical Reality: outcome=…; verified=…` / `NEXT: …verified…` / `Advisory from ts_guess: …` / 科学 reflection 前缀被改写（`scientific_feedback.py:323-362`；细节见 §3） |
| 非 user 消息 | 原样 | `cloudra/runtime_v2/agent_runner.py:947-962` `_prepare_inbox_messages`：`if item.get("sender") != "user" ...: content = project_scientific_notice(content)`（只处理通知模板） |
| 任务 prompt | `ideapool/tasks/**` 两臂**零 diff**（见 §5.1）；同一 prompt 里仍写 “Bind the unchanged native evidence logs through DAG…”（如 `ideapool/tasks/easy/D3.json` 的 `prompt.query`），B 能照做、C 做不到 → 属“prompt 与臂不匹配”的行为混杂，而非 prompt 内容差 |

### 2.8 其它 C-only 代码改动（与“展示中立化”相关但超出展示）

| 文件 | B | C | 说明 |
|---|---|---|---|
| `cloudra/tools/core/ts_process.py:355-373` | `load_record` 只校验 `format_version` 后 `model_validate` 文件 | 若 `pipeline_id` 存在则**改为从 DB 取权威 record**，校验 run_id/workspace，否则 ValueError；file-only 记录仍可读（`ts_process.py:360-372`） | 防止把“展示副本”当执行检查点；但改变了重启/外来回放的行为与失败模式 |
| `cloudra/runtime_v2/js_protocol.py:230-234` | 单次 `_encode` | 先按原始帧 `_encode` 一次（保留原协议拒收/大小上限语义），投影后再 `_encode` | 双重校验/两次序列化，行为等价、成本增加 |
| `cloudra/runtime_v2/agent_runner.py:947-962` | 仅收集/规范化消息 | 对所有非 user 消息 content 做 `project_scientific_notice` 重写 | 消息内容被 C 侧改写的唯一位置（仅固定模板命中才变） |
| `cloudra/dag/models.py:985-986` | DAG_RECORD 引导写 “dag_delivery_report ... In this record experiment, complete and partial both end the run without required scientific coverage…” | 改为标准引导 “Check dag_delivery_report before stop(...); selected delivery targets must satisfy…” | C 实际从不使用 DAG_RECORD（模式=STANDARD），纯死代码差异（见 §5.2） |

---

## 3. C 的残余回流审计

### 3.1 汇总表（判定：能否漏出 verified / candidate_only / pass / fail）

| # | 通道 | 能否漏判定 | 中性化/泄漏点（代码） | 残余 | 等级 |
|---|---|---|---|---|---|
| 1 | `ts_prepare`/`ts_resume`/`ts_inspect`/`ts_stop` 工具输出（TsProcessView） | **否（结构字段）**；**部分（文本）** | 出口 1/2 投影；`project_scientific_feedback:259-295` 对 `result.outcome/verified` 置 `None`、`result.reason`/`message`/`available_results[].detail`/`blocked`/`failed_attempt` 过 `_observed_text`；`_frequency` 清 `aligned/status` | 未知混合散文原样（`:216`）；`blocked.failure_class` 只清 `wrong_mode`/`endpoint_unconfirmed`（`:249-256`），`scan_no_candidate` 等诊断类别保留；`warnings`、`structures` 原样（`_RAW_FIELDS`）；`structures.*.binding_status` 可能是 `"unverified"`（`reaction_state.py:184`） | 中 |
| 2 | process.json 三种导出 | **基本否** | `ts_process.py:343-348`、`ts_pipeline_store.py:112-120`、`:343-346`；`public_scientific_record` 仅当 `pipeline_id` 存在才投影（`scientific_feedback.py:365-368`） | **file-only 旧记录**（无 `pipeline_id`）原样落盘，可读回原判定（C 文档 `SCIENTIFIC_FEEDBACK_ABLATION.md:52-54` 自认）；workspace 复用旧 run 时旧文件可读 | 中 |
| 3 | 计算完成通知（`Compute Event: Job ... TS ... Physical Reality/NEXT/Advisory`） | **基本否** | `compute_notify.py:362-452` 生成原文；渲染时 `project_scientific_notice:323-362` 清 `outcome=verified/candidate_only`、`verified=true/false`、`NEXT: ...verified...`、`Advisory from ts_guess`；“Physical Reality” 行仅在首行含 `" TS "` 且以 `Compute Event: Job ` 开头时处理（`:328-329`） | 未知 `reason` 散文保留；`_research_observation`（`:294-310`）含 `outcome/verified/failure_class`，但仅 `DAG_GUIDED` 生成（`:287-290`），C 不触发；guidance 中 `[Guidance] This TS optimization did not converge; ...`（`guidance.py`）非判定文本，保留 | 低 |
| 4 | Guidance / notice pins | **否（模板命中时）** | `scientific_feedback.py:325-327` 精确改写 `guidance-scientific-reflection:ts-process:` 键 + `"[Guidance] The target TS step remains unverified; "` 前缀 | 非 `wrong_mode` 的 blocked 走非收敛文案（数值/流程），不判定；`_TS_NOTICE` 两臂同文（产品引导，非运行判定） | 低 |
| 5 | JS guest（ToolResponse / error frame） | **否**（success 帧）；**低**（error 帧无投影） | `js_protocol.py:230-235` 投影 success 帧；`encode_tool_error_frame:238-241` **不投影** | 工具异常/校验错误通常不含判定；理论上传入的 error dict 若带 verdict 文本则漏 | 低 |
| 6 | 传统工具上下文 summary | **基本否（JSON）**；**可能（非 JSON）** | `invocation.py:125-127`；`_summary` 仅在 `json.loads` 成功且投影有变化时重写（`scientific_feedback.py:298-308`） | 业务工具 summary 实际为 `json.dumps(output)`（`adapters.py:1169`），可解析→被覆盖；非 JSON summary 原样 | 低 |
| 7 | `get_tool_docs` / JS 声明 / 工具描述 | **否（运行判定）**；**是（工具语义/实验身份）** | 输出契约中立化（`tool_catalog.py:350-369`、`documentation.py:67,78`） | **输入 schema 仍列 `verify`**（`ts_guess.py:199-215`）；`ts_guess` 工具描述仍宣传 verify 的 pass/fail 语义（`ts_guess.py:81-109`）；C 契约文本出现 “In this C experiment…/…in this arm”（`ts_search_process.py:52`、`tool_catalog.py:351,357,362`）→ 告诉模型臂身份，属 treatment 泄露而非判定泄露 | 中（偏盲化） |
| 8 | 子 agent 报告 / `agent_hub` / 跨 agent 消息 | **是** | 只有通知模板投影（`agent_runner.py:955-960`）；`hub_bridge.py`、`subagent_bridge.py`、`get_subagent_report.py` 无 `scientific_feedback` 引用（grep 为空） | 子 agent 的 LLM 文本、最终报告、hub 帖子、Coordinator 转述可含 `verified/candidate_only/pass/fail`；C 文档自认 “不重写子 agent 独立生成的科学结论”（`SCIENTIFIC_FEEDBACK_ABLATION.md:44/61`） | 高 |
| 9 | DB / event log / raw 事件 | **是** | 原始工具结果落 `tool.result_recorded`：`invocation.py:454-471`（`data` 为 detach 后的 raw，含 `result.verified`）；DB 路径 `runtime-v2.db`/`compute.db`（`paths.py:45-52`）；**bash 无路径围栏**（`bash.py:172-177` 仅 `cwd=working_directory`，命令字符串可 `cat/sqlite3/python` 任意路径） | agent 可 `sqlite3 ../../../runtime/compute.db` / `python -c ...` 读 `ts_pipeline_processes.record` 与 runtime 事件库 → 直接拿 raw terminal/verified；`read` 工具虽有沙箱（`Searchtool/read.py:76-93` 拒绝 workspace 外绝对路径），bash 不受此限 | 高 |
| 10 | 环境/源码/文档身份泄露 | **是（臂身份）** | 子进程继承 benchmark 进程环境：`run.sh` 导出 `PYTHONPATH=$HERE`（臂克隆路径含 `arm-record`/`arm-standard`）、`cloudra/benchmark/__main__.py:56-60` 设置 `CLOUDRA_DATA_DIR=<data-dir>/runtime`；bash 子进程不隔离 env（`bash.py:172` 无 `env=`） | `env`/`pwd` 即可识别臂；agent 还能读 `/home/ly/cloudra-arm-*/ABLATION_ARM.md`、`docs/benchmark/SCIENTIFIC_FEEDBACK_ABLATION.md`、共享仓库 P0 文档（bash 绝对路径可读）→ 得知“哪些判定被隐藏”，并可能读另一臂数据目录（若同机存在） | 高（盲化） |
| 11 | YOLO 审批反馈 | **可能** | `cloudra/infra/yolo_guard.py:176-197` 把 `workflow_review_context(pipeline_database(), ...)` 注入审批 LLM；该函数 `ts_pipeline_store.py:286-303` 查询并返回 `terminal`（`verified/candidate_only`）、`failure_class`、`run_id`、`run_dir` | 审批 LLM 可把 terminal 判定写进拒绝理由，返回给 agent（C 文档 `SCIENTIFIC_FEEDBACK_ABLATION.md:55-57` 列为残余）；另外审批本身是额外 LLM 调用（两臂都有） | 中 |
| 12 | scan_parse / 其他自动判定 | **部分** | `_is_guess` 只对 `verification_status/verdict/message/imag_mode_aligned/checks/verdicts` 生效；扫描判定字段 `scan_has_internal_peak`、`candidate`、`barrier_kcal`、`verdicts` 长文本在 C 仍公开（`ts_guess.py:440-459` 输入 schema / `log_parser.py:166-171`），`_observed_text` 只处理整词和固定模板 | scan_parse（`ts_guess` 未被 C 门控）会给出 “internal peak / candidate / not a validated TS” 类自动判定（`log_parser.py:166-171,522,535`）；不直接给 verified/pass，但属自动科学结论 | 中 |
| 13 | 原始 native 日志 | **否（自动判定）；是（可自行推断）** | 有意保留：C 的拒绝文案就直接让 agent “Inspect the native frequency/IRC logs yourself.”（`ts_guess.py:1359-1360`） | 频率值/IRC 点数/终止标志本身可让模型自行判断；C 文档明确 “A numerical observation can still let the agent form its own scientific judgment; that is intended”（`SCIENTIFIC_FEEDBACK_ABLATION.md:25-27`） | 设计内 |
| 14 | 工作区文件工具（read/write/edit） | **部分** | `read` 被限制在工作目录内（`Searchtool/read.py:76-93`，越界报错不读）；`write/edit` 同理在工作区 | workspace 里 `ts/<run>/process.json` 是投影副本（安全）；但若复用旧 workspace 或 file-only 旧 run，则旧 raw 文件可被 read 读到 | 中 |
| 15 | 会话快照 / contexts 文件 | **是（底层文件）** | `core.py:332-336` 把 `notices/pending/reminders/mailbox/...` 的 raw snapshot 放入核心快照；`persistence.py:958` 持久化 | 快照在 runtime DB 内（原始数据同 #9）；`contexts/*.json` 中的 `context.appended` 消息是投影后的（安全），但 raw 事件仍在 DB | 高（同 #9） |
| 16 | 评分 / UI completion | 不适用（非模型通道） | benchmark 评分只读交付物（`backend.py:202-203`；`runner.py` 评分函数无 diff）；`completion_summary/verification_label` 仅 API/UI（`completion.py:95`、`services/api_v2/views.py:35`） | B partial→`partial`、C 一律 `unverified`：只影响 UI 元数据，不影响 benchmark 分数 | — |

### 3.2 判定边界：C 到底“藏住了什么”

被**明确封堵**的自动判定（模型经正式通道看不到）：

- `TsProcessView.result.outcome ∈ {verified, candidate_only}` → `None`；`result.verified` → `None`（`scientific_feedback.py:267-273`）。
- `TsProcessRecord.terminal ∈ {verified, candidate_only}` → `None`（`_record_parts:233-235`）。
- `TsGuess_output_schema.verification_status ∈ {pass,fail,candidate,inconclusive}` → `None`；`imag_mode_aligned` → `None`；`verdict/message/checks/verdicts` 只做模板清理（`:284-294`）。
- 已知 verdict 文本（约 30 条固定模板）→ 观测事实保留 + “Scientific judgment not provided.”/“?”（`_observed_text:43-216`、`_NOT_PROVIDED:16`）。
- 计算通知里的 `outcome=verified/candidate_only`、`verified=true/false`、`NEXT: ...verified...`、`Advisory from ts_guess` 判定句（`project_scientific_notice:323-362`）。
- 科学 reflection pin 的 “The target TS step remains unverified;” 前缀（`:325-327`）。

**没有藏住**或藏不住的：

1. **raw 存储层**（最高风险）：`tool.result_recorded` 事件、`compute.db` 的 `ts_pipeline_processes.record`、`dag_delivery_dispositions`（B 才有写入；C 无该表写入但若数据目录混用可读）、旧 `process.json`。C 的投影只作用于“渲染/导出副本”，不改权威记录（设计如此，C 文档 `SCIENTIFIC_FEEDBACK_ABLATION.md:55-60` 也承认 “raw DB/events remain for offline audit… this is not a guarantee that the agent can never read them”）。而 `bash` 工具会以工作目录为 `cwd` 但**不设文件系统沙箱**，`read` 工具则被围栏——两者组合使得“正规读文件被挡、bash 能读”的缝隙真实存在。
2. **子 agent/LLM 文本**：只有固定通知模板被投影，任何“人写的”判定句（子 agent 报告、hub 消息、模型自己的转述）原样传递。
3. **未知混合散文**：`_observed_text` 只处理精确模板；新模板/换措辞的判定句原样输出（C 文档 `SCIENTIFIC_FEEDBACK_ABLATION.md:47-51` 自认）。
4. **`blocked.failure_class` 白名单**：只清 `wrong_mode`/`endpoint_unconfirmed`（`scientific_feedback.py:249-256`）；`scan_no_candidate` 等仍是自动科学诊断类别。
5. **`_RAW_FIELDS` 豁免区**：`structures`（含 `binding_status: unverified`）、`warnings`、`methods`、`diagnostics` 等子树不做判定清理。
6. **YOLO 审批上下文**：审批 LLM 能看到 terminal，其拒绝理由回到 agent 上下文。
7. **scan_parse / log_parser 的自动判定**：未纳入中立化范围。
8. **arm 身份**：环境变量/源码/文档/数据目录名可被 bash 读出（#10），这会让模型知道“判定被隐藏”，从而改变行为——对“盲化”而言等同于泄露 treatment。

### 3.3 关键代码引文（中性化与泄漏点对照）

```python
# 中性化（C 独有）：scientific_feedback.py:267-273
if _is_view(value):
    verdict = out.get("result")
    if isinstance(verdict, dict) and {"outcome", "verified", "reason", "evidence_refs"} <= verdict.keys():
        if verdict["outcome"] in _SCIENTIFIC_OUTCOMES: verdict["outcome"] = None
        verdict["verified"] = None
        verdict["reason"] = _observed_text(verdict["reason"])
```

```python
# 未知文本不猜（C 文档化边界）：scientific_feedback.py:216
return text
# 豁免字段（可能含判定词）：scientific_feedback.py:22-28
_RAW_FIELDS = frozenset({..., "structures", ..., "diagnostics"})
# 只清两种 failure_class：scientific_feedback.py:249-256
if diagnostic.get("failure_class") in {"wrong_mode", "endpoint_unconfirmed"}:
    diagnostic["failure_class"] = None
```

```python
# 泄漏点：raw 工具结果先于任何投影落库（两臂相同）：invocation.py:454-471
recorded = await self._commit(self._draft("tool.result_recorded", ctx, {
    "tool_call_id": call.id, "tool_name": call.name, "execution_id": execution_id,
    "result": {"is_success": ..., "summary": result.summary,
               "data": _detach_json(result.data), ...}}))
```

```python
# 泄漏点：bash 无路径围栏（cwd 之外的绝对/相对路径不会被拒）：Bashtool/bash.py:172-177
process = await asyncio.create_subprocess_shell(command, cwd=getattr(self.subagent, "working_directory", None), ...)
# 对照：read 工具拒绝工作区外路径：Searchtool/read.py:86-93
try: path = absolute.relative_to(Path(root).resolve()).as_posix()
except ValueError: return self._fail(..., "outside the working directory ...")
```

```python
# 泄漏点：YOLO 审批看到 terminal（verified/candidate_only）：yolo_guard.py:176-197 → ts_pipeline_store.py:286-303
"json_extract(record,'$.terminal')" ...  # workflow_review_context 返回 outcome=row[5]
```

---

## 4. 混杂清单（B vs C 除“独立验证工具”外的所有因素）

| # | 因素 | 证据（B/C 对照） | 对“科学验证工具”归因的影响 |
|---|---|---|---|
| C1 | DAG 工具可用性：B 可见 13/19，C 0/19 | §2.2；`tool_catalog.py:45-59` + 模式常量 | **不可归因**。B 多出 13 个编排/证据工具及对应行为空间 |
| C2 | DAG 内建科学校验反馈：B 的 `dag_submit_step_evidence` 在 record 模式下对频率数不合法直接拒绝并回 “TS was not verified/failed validation: …”（`dag_submit_step_evidence.py:151-163`）、species 同理（`dag_submit_species_evidence.py:120-123`）；`dag_delivery_report` 返回 `DeliveryReport`（`dag_delivery_report.py:44-52`），每轮图投影含 `delivery_gaps` 明细（`completion.py:456-459`、`models.py:1099-1126`）；`dag_view` 暴露 unresolved gaps / evidence_level 状态（`dag_view.py:109-115,83-92`） | **不可归因**。B 有第二套（非 ts_guess）自动科学判断/覆盖反馈，C 完全没有 |
| C3 | 结算语义：B 咨询式 `allow_final` + disposition 落库 + basis `declared/partial_recorded`；C 无 DAG 审计，fallback `declared`，partial 不落地 | §2.3；`stop_audit.py:275-281/501-515`、`agent_runner.py:814-838`、`completion.py:30-37` | **不可归因**。B/C 的“结束/partial/后台等待”行为不同 |
| C4 | 后台等待与 partial：B 在 stop 时检查项目级 compute/siblings/reminders（`stop_audit.py:199-219`，`:260-273`）；C coordinator 无检查（`schedule_stage.py:165-175`；`schedule_mode` 默认 False，`schemas.py:133`），只靠 benchmark watcher 事后兜底（`backend.py:236-248`） | **不可归因**。可能影响“何时结束/是否等子任务”，进而影响交付物完整度与分数 |
| C5 | Prompt/上下文差异：B 每轮 DAG 图投影+模式横幅+13 工具 manifest；C 无，且 C 的 TS 输出契约/描述被改写（含实验身份文本） | §2.7；`dag_stage.py:239-258`、`models.py:972-1126`、`tool_catalog.py:350-369`、`ts_search_process.py:52` | **不可归因**。模型看到的任务/工具/反馈文本不同，足以改变行为 |
| C6 | C-only 运行时路径改动：`load_record` 改 DB 权威（`ts_process.py:355-373`）、JS 双编码（`js_protocol.py:230-234`）、非 user 消息 content 重写（`agent_runner.py:947-962`）、process 导出多一次 JSON 序列化 | §2.8 | **不可归因**。执行/恢复/性能路径变化，可能影响可复现性 |
| C7 | provenance 标记 `scientific_feedback="neutralized_public_verdicts"` | `runner.py:246` | 仅元数据；不构成行为混杂，但必须与 commit 一起冻结、旧 C 数据不可混用 |
| C8 | 分支合并历史不同（B merge `93583c2d`；C merge `a4cc273c`；各自再并 light-IDPP） | `git log B..C`/`C..B`；`git diff --name-status` 仅 23 文件 | 最终树无无关差异 → **不构成内容混杂**；但冻结时须记录完整提交链 |
| C9 | Supervisor | 两臂都不创建（`roles.py:92-108`、`supervision.py:220-264` 仅 guided 调用）；supervisor 工具均不可用（B 隐藏 6，C 隐藏 19） | **不是差异项**；不要把它写成“B 有监督、C 没有” |
| C10 | 内部自动判定引擎 | `ts_process.py:3200-3343` `_verdict()` 两臂同文；C 仍在本机计算 verified/candidate_only，只是不公开输出 | **不是差异项**；因此“C 移除了科学验证”表述错误，准确说法是“C 移除了独立 verifier 工具并封堵了公开判定反馈” |

**明确判定（可归因 / 不可归因）**

- **可以**归因：B 相对 C 多出的“独立 `ts_guess` verify/strict 工具可用性”，以及“自动科学结论是否公开反馈到模型”。二者都是 B-vs-C 差分的一部分，但一个是工具、一个是反馈通道处理，不能合并成一个机制。
- **不可以**归因：上面 C1–C6 任一因素；尤其不能把 B/C 在分数、科学正确率、迭代轮数上的差异归因于“科学验证工具”，因为 DAG 工具面 + DAG 内建科学校验 + 结算/后台 + prompt 契约 + C-only 运行时改动与它同时变化。
- 若论文/报告必须回答“独立科学验证工具的价值”，需要补两个干净臂：(i) **B′ = B 保留 DAG、仅禁用 `ts_guess` verify/strict（且不中立化其它公共判定）**；或 (ii) **C′ = C 恢复 DAG 工具与 DAG 科学覆盖反馈、仍禁用 verify**。另需单独的“公开判定中立化”臂（D：保留 verify、只做投影），否则 (b) 也无法归因。
- C 自己的文档也只承认 “DAG confound remains… The B/C comparison is a package comparison, not an isolated verification-tool effect”（`docs/benchmark/SCIENTIFIC_FEEDBACK_ABLATION.md:62-66`）——本审计支持该自述，并要求把它扩展为 C1–C6 的显式清单。

---

## 5. 意外差异审计（本不该存在的差异）

### 5.1 已核实“无意外差异”的三类

1. **模型配置**：`cloudra/infra/config.py`、各配置文件、`.env` 类文件在两臂 `git diff` 中**零条目**；`provenance_config` 两臂同源读取 `get_config().coordinator/follower`（`runner.py` B:247-250 / C:248-251）；两个臂克隆的 `run.sh` 内容完全相同（同一个 `.venv`、同一 PATH、同一 `PYTHONPATH=$HERE` 形态）。→ 没有模型/提供方/参数差异。
2. **任务 prompt**：`git diff benchmark/arm-record..benchmark/arm-standard -- ideapool` 为空；`ideapool/tasks/**` 全部同文（但注意 §2.7 末行的“prompt 写 DAG 绑定、C 无 DAG 工具”的**错配**是两臂同文导致的臂间行为差，不是 prompt 内容差）。
3. **benchmark 评分代码**：`git diff ... -- cloudra/benchmark` 仅 `runner.py`（3 增 2 删，均为模式常量/provenance）；`runner.py` 中 `score_sandbox`、`_RUNS_COLS`、结果落库、`BenchmarkDB` 均未动；评分只读沙箱交付物（`cloudra/benchmark/backend.py:202-203`）。`completion_summary`/`verification_label`（`completion.py:95`、`services/api_v2/views.py:35`）只服务 UI/API，不进 benchmark 分数。→ 评分公平性未被直接改代码破坏。

### 5.2 需要复核/建议回退或显式豁免的差异

| # | 位置 | 差异 | 为什么算“本不该存在/需复核” | 建议 |
|---|---|---|---|---|
| A1 | C `cloudra/tools/Chemtool/ts_search_process.py:52`；C `cloudra/runtime_v2/tool_catalog.py:356-364` | 模型可见契约文本出现 “In this C experiment…”、“…in this arm…”、“Scientific acceptance is not provided in C…” | 这些文本会把 “C 实验/消融臂” 身份直接告诉被测模型，破坏盲化，也可能诱导模型行为（知道判定被抽走） | 改为中性事实描述（如 “public acceptance fields are not provided; execution failures/evidence remain visible”），删除 “C/in this arm/experiment” 字样；冻结前重跑一次契约渲染检查 |
| A2 | C `cloudra/dag/models.py:985-986` | DAG_RECORD 模式引导被改写为“check dag_delivery_report before stop… must satisfy…” | C 的 benchmark 恒为 STANDARD，DAG_RECORD 分支在 C 永远不可达 → 纯死代码 diff，扩大差集、制造审查噪音 | 回退该 Hunk（或注明“为保持分支一致而同步改动、对 C 运行无影响”） |
| A3 | C `cloudra/tools/core/ts_process.py:355-373` | `load_record` 从“文件权威”改为“DB 权威 + workspace/run 校验；无权威记录则 ValueError” | 超出“公共展示中立化”，改变重启/旧工作区/外来回放的行为与失败模式（原本可读的 file-only 记录仍可读，但 pipeline_id 存在而 DB 缺失/迁移时行为不同） | 在冻结文档中列为 C-only 执行路径变更并加回归测试；确认旧 workspace/迁移路径不会因此失败 |
| A4 | C `cloudra/runtime_v2/agent_runner.py:947-962`；C `cloudra/runtime_v2/js_protocol.py:230-234` | 所有非 user 消息 content 过模板投影；JS 结果帧双次 `_encode` | 前者是 C 侧唯一会改写 agent 间消息正文的代码（尽管只命中固定模板），后者增加每帧两次序列化/校验；均非计划表的“展示出口” | 明确记录为“实现附带差异”；若追求公平，可把消息投影限制到 sender=system/通知类，避免改写 agent 间消息 |
| A5 | C `cloudra/runtime_v2/scientific_feedback.py` 整文件；C `docs/benchmark/SCIENTIFIC_FEEDBACK_ABLATION.md` | 投影白名单/固定模板/`_RAW_FIELDS` 是 C-only 的新逻辑面 | 这是**预期**实现，不是意外；但其中“只清 2 个 failure_class”“仅精确模板”“structures/warnings 豁免”是残余泄漏来源，必须写进 P0 验收的“已知残余”而非“已完全盲化” | 在失败/残余清单中逐条登记（§3）；冻结时附本报告的通道表 |
| A6 | C `cloudra/benchmark/runner.py:246` | provenance 增加 `scientific_feedback` 标记 | 预期；但要求：C 数据目录/批次与该标记+commit 一起冻结，旧 C 结果不得与新 C 混用 | 在数据布局/冻结清单中记录 |

### 5.3 差集与计划表“意图”的对照

- 计划表意图（DAG advisory vs no DAG tools；Supervisor 均无；结算不强制；verify/strict 在 C 关闭；公共结论中立）与代码**语义一致**：B 确有 advisory 结算并落 disposition；C 确无 DAG 工具、无 Supervisor、无强制结算、`ts_guess` verify/strict 被拒、公共判定被投影。
- 但计划表若把 B/C 写成“科学验证工具消融”的单因子对照，则**不成立**：差集实际包含 C1–C6（§4），且 B 有一整套 C 没有的 DAG 内建科学校验/覆盖反馈与图投影 prompt。**P0 验收结论：差集必须改写为“臂包比较（mode package）”；对外结论不得引用 B/C 分数差作为“验证工具”的因果效应。**

---

## 6. P0 验收对照与建议

| P0 验收项 | 状态 | 依据 |
|---|---|---|
| 列出 B/C 真实差集（非计划表口径） | ✅ 本报告 §2/§4 | 23 文件 diff + 同文文件的模式作用点 |
| 逐通道验证 C 残余回流 | ✅ §3 | 中性化代码 + 泄漏点代码；16 条通道，其中 3 条高、5 条中 |
| 明确“可归因/不可归因” | ✅ §4 | 可归因仅 (a) 独立 verifier 可用性、(b) 公共判定反馈；其余 C1–C6 不可归因 |
| 排查意外差异 | ✅ §5 | 无模型/config/prompt/评分差异；4 处需复核（A1–A4） |
| 冻结前建议阻断项 | ⚠️ 建议 | ① 去掉 C 契约中的实验身份文本（A1）；② 回退死代码 guidance diff（A2）；③ 登记 A3/A4；④ 若要“验证工具”结论，先造 B′/C′ 干净臂 |
| 数据/盲化风险 | ⚠️ 需在 P0 其余项处理 | bash 可读 raw DB/event log、可识别 arm（§3.2 #9/#10）；子 agent/hub 文本不投影（#8）；YOLO 审批（#11） |

**最终判定一句话**：B/C 差集与计划表的“臂语义”一致，但它是一个六类因素打包的差集，**不能作为“独立科学验证工具”的单因子消融**；C 的公共判定回流在正式通道上基本封堵，但“完全盲化”不成立（raw 存储/子 agent 文本/YOLO/实验身份文本仍可回流）。

---

## 附录 A · 复现命令（只读）

```bash
R=/home/ly/cloudra-bench-20261019
# 差集与提交
git -C $R diff --stat benchmark/arm-record..benchmark/arm-standard
git -C $R log --oneline benchmark/arm-standard..benchmark/arm-record
git -C $R log --oneline benchmark/arm-record..benchmark/arm-standard
# 同文文件核对
git -C $R diff --quiet benchmark/arm-record..benchmark/arm-standard -- \
  cloudra/tools/capabilities.py cloudra/tools/registry.py \
  cloudra/runtime_v2/policies/dag_stage.py cloudra/runtime_v2/policies/schedule_stage.py \
  cloudra/runtime_v2/supervision.py cloudra/runtime_v2/completion.py \
  ideapool cloudra/infra/config.py
# 关键差集（带上下文）
git -C $R diff -U8 benchmark/arm-record..benchmark/arm-standard -- \
  cloudra/runtime_v2/tool_catalog.py cloudra/dag/stop_audit.py \
  cloudra/tools/Chemtool/ts_guess.py cloudra/runtime_v2/scientific_feedback.py
# 工具面枚举（可用臂克隆）
python - <<'PY'
from cloudra.tools.capabilities import dag_tools, dag_review_decision_tools
print(len(dag_tools()), sorted(dag_tools()))
print(len(dag_review_decision_tools()), sorted(dag_review_decision_tools()))
PY
# 臂克隆未提交文件（仅 run.sh，两臂同文，属启动脚本而非产品代码）
git -C /home/ly/cloudra-arm-record status --short
git -C /home/ly/cloudra-arm-standard status --short
```

## 附录 B · 证据文件索引（差异文件）

| 文件 | B/C 角色 |
|---|---|
| `cloudra/benchmark/runner.py` | 模式常量 + provenance（§2.1） |
| `cloudra/runtime_v2/tool_catalog.py` | `_mode_hidden_tools`（同文）+ C 中立输出契约（§2.2/2.5） |
| `cloudra/dag/stop_audit.py` | B advisory 结算/提交（§2.3） |
| `cloudra/runtime_v2/policies/dag_stage.py`（同文） | STANDARD 下 DAG 阶段空转（§2.3） |
| `cloudra/runtime_v2/agent_runner.py` | 运行结束 fallback + C 消息投影（§2.3/2.6） |
| `cloudra/runtime_v2/invocation.py` / `js_protocol.py` / `notices.py` | 投影出口 1/2/3（§2.6） |
| `cloudra/runtime_v2/scientific_feedback.py` | C 投影实现（§2.6/3） |
| `cloudra/services/ts_pipeline_store.py` / `cloudra/tools/core/ts_process.py` | process 导出与 load_record（§2.6/2.8） |
| `cloudra/tools/Chemtool/ts_guess.py` / `ts_search_process.py` / `documentation.py` | verify 门控与契约文本（§2.5/2.7） |
| `cloudra/dag/models.py` | 模式横幅内容（§2.7/5.2 A2） |
| `docs/benchmark/SCIENTIFIC_FEEDBACK_ABLATION.md`（C） | C 自述残余边界（§3/§4） |
