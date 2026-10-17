## 背景
2026-10-15 的一次 gold 回填战役里同时用了 5 个 `coordinator` 包 + 各自的 `small_mol` / `explorer` / `writer` 子代理（10+ 并发会话，Gaussian 16 批量作业）。以下是**工具面/角色面**发现的三个缺口，都不影响结论正确性但明显拖慢协作。

## 1. `explorer` / `writer` 角色没有写文件权限，只读道的产出无法落盘
- 现象：`explorer` 会话调用 `write` 返回 `Tool requires permissions absent from this task`；用 `bash` 建目录返回 `exit 126`（`No permission to run this command`）。`writer` 角色同样：`bash` 被拒（exit 126），且 `read` 只能读确切路径、不能列目录。
- 复现：HL1、HI1、NR1、NI5 四个包的 explorer 都复现同一现象。
- 影响：只读复核结论只能贴在 agent_hub 正文里，再由包 Coordinator 代写文件（多一次往返、正文与文件易不一致）；`writer` 角色事实上无法独立交付文档，与角色名不符。
- 建议：给 explorer/writer 一个受限写路径（例如各自工作目录）或明确说明它们的设计意图与替代做法。

## 2. 排队中的计算作业没有取消入口
- 现象：`submit_compute_job` 只有提交；`query_compute_job` 只读；`mark_compute_job_failed` 面向"卡在 running"的作业（文档明确不用于排队作业）。
- 影响：我按"把排队中 12c 作业改 8c 以提高节点并行度（32 核只能并行 2 个 12c 作业，而 8c 能并行 4 个）"下达优化指令时，各包**无法执行**——没有取消入口，重新提交就会变成双份计算。最终只能撤回该指令。
- 建议：提供"取消排队中的作业"入口（或在 `submit_compute_job` 支持修改排队作业的资源声明）。

## 3. `ts_prepare` 失败只报 `tool_exception: Tool execution failed internally`
- 现象：本次 `ts_prepare` 在任何最小声明下（reaction-only / 加 calculations / 加 conformer 文件）都返回 `tool_exception: Tool execution failed internally`，**没有 run_id、没有 run 目录、没有作业**（call_id 例 `tc_81d1fd610acd4957`）。
- 影响：该异常的真实原因是 compute.db 写锁（见同期 issue：compute.db 持久写锁导致队列冻结），但报错把底层原因吃掉了，导致我们把"平台 DB 故障"误报成"独立工具 bug"、走了半轮排查弯路。
- 建议：把底层异常（DB/OS 错误）原样带出，或至少给出 error_class + 是否需要写库。

## 记录位置
- 战役台账：`gold_finish_20261015/LEDGER.md`（工作区未提交）；相关只读证据散见各包 `gold_finish_20261015/*/STATUS.md`。
