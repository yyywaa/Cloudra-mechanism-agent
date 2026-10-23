# P0 验收报告：四组 Cloudra 对照实验

> 依据：`ideapool/cloudra_four_arm_experiment_plan.md` §六 P0 与 §八 五个代码点。
> 范围：只做工程验收与公平性审计；不调用付费模型、不跑正式 benchmark。
> 证据分册：`00_lead_checks.md`、`01_arm_behavior.md`、`02_bc_diff.md`、`03_evidence_chain.md`、`04_freeze.md`。
> 审计时点：2026-10-24 凌晨（Asia/Shanghai）；共享仓库停在 `docs/p0-acceptance`（`1e6d953f`），未切分支、未改产品代码、未写正式数据目录。

## 0. 结论摘要

P0 四项审计全部完成。核心结论：

1. **四臂是四个可复现的不同版本**：题库同源（50 题，H1 `5db51268…`）、评分器同源（12 个评分文件 sha256 一致，评分函数 AST 哈希一致）、模型/任务 prompt/评分无意外差异。
2. **评分公平性通过**：同一批沙箱在四臂重打分逐字节一致；run6 的 E1 真实交付沙箱 replay 精确复现历史行（final 1.0）。
3. **四臂行为**：A/D 符合计划表；B 符合（附 4 项登记）；**C 部分符合**（4 项残余：英文中性文本、verify 仍被 schema 宣传、公共 prompt 仍指示 DAG 工具、结算记录比 B 更弱）。
4. **B vs C 不是单因子"科学验证工具"消融**，而是六类因素打包的臂比较；可归因的只有 verify/strict 可用性与公开判定反馈，其余（DAG 工具面、DAG 内建科学校验、结算/partial/后台等待、prompt/契约、C-only 运行时改动）不可归因。
5. **C 的公开判定基本封堵但不是盲化**：16 条残余通道（3 高 5 中），含 raw DB/event log、子 agent 文本、YOLO 审批、`scan_parse`、`structures.binding_status`。
6. **三个必须写进冻结清单的高优先级事实**：① 计划 §九的基线 `8c568ca` 已过期，实际共同基点是 `1e6d953f`（含两次 `ts_guess.py` 改动）；② 在线 provenance 不记录 git SHA/采样参数/Supervisor 消耗；③ `undelivered` 只由 A/D 的交付文件决定，B/C 结构性恒为 1，不可跨臂比较。
7. **正式运行仍有 5 个阻塞项**（模型版本、预算、重复次数、配置/凭据冻结、api-pool）和 3 个待冻结口径（成功/partial/假成功判定、交付状态抽取、run.sh 登记）。

**P0 判定：未通过（不能进入 P2 全量）。** 完成 §7 的阻塞项、S1–S3 冻结与 A1/A2 处理后，可进入 P1 小规模四组通跑。

## 1. 计划 P0 清单

| # | 检查项 | 状态 | 证据 |
|---|---|---|---|
| 1 | 四组实际行为清单（模型、角色、工具、DAG/结算、错误呈现） | **完成** | `01_arm_behavior.md`（376 行，4×9 矩阵 + 逐臂 verdict） |
| 2 | B/C 真实差集与残余回流验收 | **完成** | `02_bc_diff.md`（366 行，16 通道泄漏表 + 混杂表） |
| 3 | 四组原始证据保存、交付状态、fallback、独立评估链 | **完成** | `03_evidence_chain.md`（505 行） |
| 4 | 题库/评估器/失败分类/重试规则冻结；模型与预算确认 | **完成（含阻塞项）** | `04_freeze.md`（721 行） |
| 5 | 五组代码点（§八） | **通过** | `00_lead_checks.md` |

## 2. §八 五个代码点

| # | 检查点 | 结论 | 证据 |
|---|---|---|---|
| 1 | 实际 arm 与配置入口一致 | **通过** | 四臂 `--help` 逐字节一致；`ABLATION_ARM` 强制模式；50/50 题旧标签被 project settings + root spawn + 子 agent 继承 + 结果行覆盖；批次 config 记录 `experiment_arm` / `orchestration_modes` / `error_feedback` / `scientific_feedback` |
| 2 | Supervisor / 结算调用链 | **通过** | A/D Supervisor 在线（懒启动 + 退出审查）；B/C 离线；A/D guided 门禁（IRC+交付物+覆盖+督导终审，3 次无进展→failed）；B advisory `allow_final(declared/partial_recorded)`；C 无 DAG 门禁（`allow_final(declared)`，无 disposition 行） |
| 3 | 科学工具边界 | **通过（有混杂）** | coordinator 可见 dag_*：A/D 19/19、B 13/19（隐藏 6 监理裁决工具）、C 0/19；ask_user 四臂隐藏；C 入口硬拒 verify/strict（`ts_guess.py:1352-1362`） |
| 4 | D 的错误呈现与审计隔离 | **通过（有残余）** | `brief_errors.py` 8 个投影点；D 只压缩诊断文本，结算/阈值/工具/权限零改动（`git diff A D -- cloudra/dag cloudra/prompts ideapool` 为空） |
| 5 | 独立评分与证据发现 | **通过** | 12 个评分文件 sha256 四臂一致；四臂重打分逐字节一致；fallback 在评分器侧同实现 |

## 3. 四组行为对照（详见 01）

| 臂 | HEAD | 模式 | DAG 工具 | verify/strict | Supervisor | 结算 | partial | 反馈 | verdict |
|---|---|---|---|---|---|---|---|---|---|
| A | `e67ef30a` | dag_guided | 19/19 | 可用 | 在线 | guided 门禁 + 督导终审 | 督导接受，写 disposition + 端点证据 | full | **符合** |
| B | `058fdc82` | dag_record | 13/19 | 可用 | 离线 | advisory `allow_final(declared/partial_recorded)` | 写 disposition，无端点证据 | full | **符合**（附 4 项登记） |
| C | `79ca80bf` | standard | 0/19 | 入口禁用（schema 仍宣传） | 离线（更彻底） | 无 DAG 门禁，`declared`，无 disposition | 仅模型声明 | 公开 TS 判定中性化（英文） | **部分符合**（4 项残余） |
| D | `0b81c262` | dag_guided | 19/19 | 可用 | 在线 | 同 A | 同 A | brief（诊断压缩） | **符合**（附 2 项注记） |

C 的 4 项残余：① 中性文本是英文 `Scientific judgment not provided.` / `?`（计划写"未提供判定"）；② verify 仍被输入 schema/描述宣传；③ 公共 role prompt 仍指示 DAG 工具、`stop` 工具描述仍是 guided 语义；④ 无 disposition 行，交付记录比 B 更弱（计划"C 同 B"只是近似）。

## 4. B/C 差集与混杂（详见 02）

**差集 = 六类臂包**：① 模式常量 `DAG_RECORD→STANDARD`；② DAG 工具面 B 13/19 vs C 0/19；③ 结算语义（B advisory + disposition，C 无 DAG 审计）；④ Supervisor 两臂均无（非差异项）；⑤ C 硬拒 verify/strict；⑥ C 独有 `scientific_feedback.py` 投影层（6 出口）。

**可归因给"独立验证工具"的只有**：verify/strict 可用性 + 公开结论反馈。其余 C1–C6 全部不可归因。

**C 的 16 条残余回流（3 高 5 中）**：raw `tool.result_recorded` / `compute.db`、arm 身份（env/PYTHONPATH/源码）、子 agent/hub 文本、YOLO 审批看到 terminal、`scan_parse`、`structures.binding_status`、file-only 旧 process.json 等。

**4 处意外差异**：A1 C 契约含实验身份文本（`ts_search_process.py:52`、`tool_catalog.py:356-364`，建议删）；A2 C 改了永不执行的 DAG_RECORD 引导（`dag/models.py:985-986`，建议回退）；A3 `load_record` DB 权威化（登记）；A4 非 user 消息投影 + JS 双编码（登记）。

**判定**：按"臂包比较"报告，不得把 B/C 分数差写成验证工具的因果效应；若要该结论需 B′/C′ 干净臂。

## 5. 证据链与评分公平性（详见 03）

- **评分器一致**：5/6 评分文件四臂逐字节相同；`runner.py` 仅 arm 接线；评分函数 AST 哈希一致；权重 0.1/0.3/0.6 一致。
- **实证一致**：合成沙箱 + run6 E1 真实沙箱在四臂重打分逐字节相同，E1 replay 复现历史行（final 1.0）。
- **证据保留**：原始 QM 日志/`mechanism_graph.json`/`.cloudra/evidence` 四臂都保留；`mechanism_evidence.json` 仅 A/D 发布；删除它分数不变，只有 `undelivered` 翻转。
- **回退链**：`discover_edge_proof`、原生日志回退、节点能量反推都在评分器侧，四臂同哈希。
- **`undelivered` FLAG**：仅文件存在性，评分器不读；B/C 恒 True，禁止跨臂比较；交付状态轴用 `completion_gate.basis` + `dag_delivery_dispositions`，臂归属用 `batches.config.experiment_arm`（A/D 的 mode 都是 dag_guided）。
- **partial vs complete**：离线评估器无交付状态输入、无 success 布尔 → partial 不可能被算成完整成功。
- **判定：评分公平性通过（identical scorer = YES）**。

## 6. 冻结与数据布局（详见 04）

- **题库**：50 题（20/10/10/10）；H1 `5db51268…` / H2 `a9a9b17a…`；四臂 `git diff -- ideapool/tasks` 全空。
- **评估器**：权重 0.1/0.3/0.6；12 个评分文件四臂 sha256 相同；sigma 3.0（easy/impossible）、2.0（normal/hard）。
- **四臂 HEAD**：A `e67ef30a` / B `058fdc82` / C `79ca80bf` / D `0b81c262`；**实际共同基点 `1e6d953f`**（不是计划 §九写的 `8c568ca`；两版之间含 `ts_guess.py` +120/−16 的两次 master 提交）。
- **失败分类**：12 类；未评分/取消行 `final_score=0.0` 是占位，不是 0 分。
- **数据布局**：`/home/ly/cloudra-formal-<date>/{A,B,C,D}/`，每臂 `arm.json` + `commit.txt` + `benchmark.db` + `benchmark.log` + `sandboxes/` + `runtime/`；append-only；campaign 结束 `chmod -R a-w`；探针只允许 `/home/ly/cloudra-p0-probe/`。
- **现有正式数据**：run6（3.6G）与 full-20261022（1.5G）保持只读（DB mtime 仍为 10-22）；run6 是旧 schema，只能 `?mode=ro&immutable=1` 读。

## 7. 阻塞项与放行条件

**用户已裁决（2026-10-24）**
- **B1 模型**：`deepseek-v4-flash`（按名称记录；四臂同日连续跑，降低供应商滚动风险）。
- **B2 预算**：不设硬上限，按实际消耗记账（用户承诺充值）；`arm.json` 记录用量。
- **B5 `--api-pool`**：正式运行**不使用**（固定单端点；如必须使用，需把 pool 标签写入 `arm.json`）。

**仍需裁决/确认**
- **B3 重复次数**：建议 `r=1` 全量四臂（配对比较）+ `r=3` 仅在 easy 的 5 题小子集做方差标定；待确认。
- **B4 配置/凭据冻结**：redacted 配置快照 + key 走环境变量；待确认。

**付费开跑前必须裁决（B1–B5）**
- B1 模型版本未固定（provider 可能滚动）；
- B2 预算未定（CLI 无费用/资源硬上限）；
- B3 重复次数 r 未定；
- B4 配置/凭据冻结方式未定（建议 redacted 快照 + 环境变量）；
- B5 `--api-pool` 策略未定（建议正式运行禁用）。

**冻结清单必须补齐（H1–H3）**
- H1 基线改写：记录四臂各自 HEAD + 实际共同基点 `1e6d953f`；`ts_guess.py` 的两次提交属共同基线，不是处理因素；
- H2 provenance 补外部记录：git SHA、模型采样参数、Supervisor 模型/消耗（`build_orchestration_config()` 是死代码，不会落库）；
- H3 `undelivered` 口径：只作 A/D 参考；交付率另用 `completion_gate.basis` + `dag_delivery_dispositions`；B/C 恒为 1 不得当科学失败。

**待冻结口径（S1–S3）**
- S1 独立科学成功 / 有效 partial / 假成功的判定规则（评分器只有连续分）；
- S2 交付状态抽取与 join 的 SQL/脚本；
- S3 四臂未跟踪 `run.sh` 的登记（内容四份相同，建议纳入冻结哈希）。

**建议修复（A1/A2）**
- A1 删除 C 契约中的实验身份文本；
- A2 回退 C 的死代码 diff（或显式豁免）。

**放行条件**：B1–B5 裁决 + H1–H3 记录 + S1–S3 冻结 + A1/A2 处理 → P1（在真实四臂运行上复核评分 parity/replay 探针）。

## 8. 结论

**P0 未通过（暂不允许 P2 全量）。** 工程侧四臂可复现、题库/评分同源、评分公平性实证通过、数据纪律明确；但 B/C 只能作为臂包比较、C 的盲化仍有残余、`undelivered`/成功判定/交付状态三个口径未冻结、模型/预算/重复次数尚未裁决。

按计划，下一步是：修 A1/A2 → 冻结 H1–H3、S1–S3 → 裁决 B1–B5 → 进入 P1 小规模四组通跑。
