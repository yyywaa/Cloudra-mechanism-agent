# P0 Lead 自查记录（§八 五个代码点）

> 目的：在四组正式运行前，用只读代码审计 + 空后端探针核对"实际行为与配置"。
> 本记录只代表 Lead 已亲手核对的条目；其余条目见 `01_arm_behavior.md`、`02_bc_diff.md`、`03_evidence_chain.md`、`04_freeze.md`。
> 所有探针写入 `/home/ly/cloudra-p0-probe/<arm>/`，未触碰任何正式数据目录。

## 1. 入口与 arm 固定

- 四臂 `./run.sh --help` 输出 **逐字节一致**（`diff` 为空）：同一 CLI 入口，不传 `--mode/--model/预算`。
- 每臂 `cloudra/benchmark/runner.py` 顶部有 `ABLATION_ARM = OrchestrationMode.<ARM>`，`task_project_settings()` 用它覆盖题目 JSON 里的旧 mode 标签（`runner.py:220-227`）。
- 空后端批次 `config` 已记录真实 arm：
  - guided：`experiment_arm=benchmark/arm-guided`, `error_feedback=full`, `orchestration_modes={E1: dag_guided}`
  - record：`experiment_arm=benchmark/arm-record`, `error_feedback=full`, `orchestration_modes={E1: dag_record}`
  - standard：`experiment_arm=benchmark/arm-standard`, `error_feedback=full`, `scientific_feedback=neutralized_public_verdicts`, `orchestration_modes={E1: standard}`
  - brief-errors：`experiment_arm=benchmark/arm-guided-brief-errors`, `error_feedback=brief`, `orchestration_modes={E1: dag_guided}`

结论：**arm 可通过批次配置与 runs 行反查，不依赖题目 JSON 里的旧标签。**

## 2. 题库一致

```
git diff --stat master..benchmark/arm-{guided,record,standard,guided-brief-errors} -- ideapool/tasks
```

四个 diff 全部为空：四臂共享同一冻结题库（easy 20 / normal 10 / hard 10 / impossible 10）。

## 3. 评分器一致（sha256）

`cloudra/benchmark/` 下评分相关文件的 sha256：

| 文件 | guided | record | standard | brief-errors |
|---|---|---|---|---|
| `accuracy.py` | `fa0676…` | `fa0676…` | `fa0676…` | `fa0676…` |
| `selfconsistency.py` | `421446…` | `421446…` | `421446…` | `421446…` |
| `evidence_search.py` | `a5b382…` | `a5b382…` | `a5b382…` | `a5b382…` |
| `integrity.py` | `d2b840…` | `d2b840…` | `d2b840…` | `d2b840…` |
| `delivery_evidence.py` | `1dd563…` | `1dd563…` | `1dd563…` | `1dd563…` |
| `runner.py` | `0dfee4…` | `29d0b4…` | `a007d1…` | `7aef62…` |

`runner.py` 每臂不同，但 `git diff master..<arm> -- cloudra/benchmark/runner.py` 的差异仅为：
- `ABLATION_ARM` 常量与 import；
- `task_project_settings()` / `RunResult.orchestration_mode` / `provenance_config()` 的 arm 覆盖；
- C 额外记录 `scientific_feedback`，D 额外记录 `error_feedback=brief`。

**权重（0.1/0.3/0.6）、accuracy 公式、自洽评分、发现式检索均未改动。**

结论：评分算法四臂一致；差异仅限 arm 接线与反馈投影（后者由 C/D 单独审计）。

## 4. 空沙箱探针

四臂各跑一次：

```bash
./run.sh --backend none --tasks-dir ideapool/tasks/easy --only E1 \
  --data-dir /home/ly/cloudra-p0-probe/<arm>/probe
```

- 四臂均 `rc=0`，都生成 `benchmark.db` + `sandboxes/`；
- 评分结果一致：`E1 final=-1.000, graph=0.000, selfcons=0, accuracy=0.000, undelivered=1`。

`-1.0` 不是哨兵，而是评分规则：无可解析机理图 → `final = -no_evidence_penalty`（`runner.py:470-480`）；有 accessible 节点但无任何证据绑定 → 同样倒扣（`runner.py:483-494`）。notes 明确写 `no parseable mechanism graph -> no evidence possible; penalty applied`。

**P0 需记录的口径**：空沙箱/未交付运行的分数是 **负分（-1.0）**，不是 0；报告时必须区分"未交付"与"科学错误"，不能把 -1 当成化学结论。

补充（与 `04_freeze.md` 对齐）：**未评分/被取消的行**（如批次 kill 时写入的 `cancelled by batch stop`）`final_score=0.0` 是占位值，**不是 0 分**；只有真正走过评分器的行才有分数。`full-20261022` 里 46/50 行是这种占位行，**不能用来算均值**。

另：`run6` 的 DB 是旧 schema，用可写连接打开会触发 `runs` 表重建（`runner.py:262-281`）；只允许 `?mode=ro&immutable=1` 只读访问。

## 5. 数据隔离

- 探针目录：`/home/ly/cloudra-p0-probe/<arm>/`（独立、可删）；
- 正式数据目录未被写入：
  - `/home/ly/cloudra-bench-run6-20261021`
  - `/home/ly/cloudra-bench-full-20261022`
- 正式运行的数据布局与保留规则见 `04_freeze.md` 第 6 节。

## 6. §八 第 2–4 点的快速核对（细节见 01/02/03 报告）

**点 2：Supervisor / 结算调用链**
- `DagController.enabled` 只在 `STANDARD` 为假（`cloudra/dag/controller.py:65-66`）→ C 根本不加载 DAG 引擎；
- Supervisor 只在 `DAG_GUIDED` 启动（`cloudra/dag/supervision.py:78`）→ B/C 无 Supervisor；
- 结算：A/D 走 guided 门禁，B 走 advisory 结算，C 无 DAG（stop 直接 `declared`）。

**点 3：科学工具边界**
- `tool_catalog._mode_hidden_tools`（`cloudra/runtime_v2/tool_catalog.py:44-58`）：
  - `STANDARD` → 隐藏全部 `dag_tools()`；
  - `DAG_RECORD` → 只隐藏 `dag_review_decision_tools()`（Supervisor 裁决工具）；
  - `DAG_GUIDED` → 不隐藏。
- C 的独立校验关闭点：`cloudra/tools/Chemtool/ts_guess.py:1359`（verify/strict 直接拒绝）。
- B 的校验工具保留（与 A 同一套），C 的差集 = 全部 DAG 工具 + 独立 verify/strict + 公开判定投影。

**点 4：D 的错误呈现**
- `cloudra/runtime_v2/brief_errors.py` 在 8 处接入：`js_protocol.py`、`invocation.py`、`js_runtime.py`、`notices.py`、`turn_pipeline.py`、`child_manifest.py`、`agent_runner.py`；投影函数为 `project_tool_result` / `project_feedback` / `project_notice` / `brief_text`。
- 是否覆盖全部模型可见通道、是否保留结构化字段，由 `02_bc_diff.md` 与 `03_evidence_chain.md` 逐通道核验。

**点 5：独立评分与证据发现**
- 评分文件哈希四臂一致（见第 3 节）；`runner.py` 差异仅为 arm 接线；
- 证据发现/回退（`discover_edge_proof`、节点能量反推）位于评分器侧，四臂同一份代码。

## 待补

- [ ] B/C 真实差集与残余回流（`02_bc_diff.md`）
- [ ] 四臂行为清单（`01_arm_behavior.md`）
- [ ] 证据链与评分公平性（`03_evidence_chain.md`）
- [ ] 冻结清单与数据布局（`04_freeze.md`）
- [ ] 汇总判定（`P0_ACCEPTANCE.md`）
