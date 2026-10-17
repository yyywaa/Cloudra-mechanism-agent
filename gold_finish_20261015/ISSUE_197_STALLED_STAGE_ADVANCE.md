# ISSUE 197 — TS workflow stage does not advance after its dependency job finishes (waiting_for a job that is already done)

**发现会话**：as_ec848a7673b74e35（gold-finish HI1 写权会话）；**记录会话**：as_a341823c436e47ed（主协调）
**发现时刻**：2026-10-17 14:50:21 CST（本机时钟实测）
**严重度**：高（TS 管线停摆，需要人工绕过或等待；若用 ts_resume 走 retry 语义可能重跑已收敛阶段、产生重复作业）

## 现象
run `ts_0015`（E1a 的 TS，reactant = acetone + proline 27 原子子系统）的 ts_opt 作业 **job 1055 已正常完成**（scheduler state=done、ended_at 14:45:42；guard-1055.log 退出码 0；refine.log L11399 Normal termination @14:45:41，L10723 Optimization completed / L10724 Stationary point found），但：

- `process.json`：revision **11**、stage **refine**、status waiting、`waiting_for = [{job 1055, purpose ts_opt, state done}]`、next.action = **wait_for_system**、blocked = null、failed_attempt = null；
- process.json 的 mtime 仍是 **14:36:37**（提交后未再被驱动写盘）；
- `jobs/declaration_0001/` 下只有 `ts_opt/`，**没有 frequency 目录**；
- ts_inspect 自带说明：该阶段依赖既有 compute 通知路径推进、本阶段从不轮询也不发事件。

## 期望
作业终态通知到达后，阶段应从 refine 推进到 ts_freq（生成 jobs/declaration_0001/frequency 并提交 freq 作业）。

## 对照（机制本身可用）
`ts/ts_0011/jobs/declaration_*/` 下存在 ts_opt / frequency / irc / reactant_opt / reactant_frequency / product_opt / product_frequency 七个阶段目录 ⇒ 自动推进路径在其他 run 上工作正常，本 run 属**停滞**，不是设计缺阶。

## 影响面
- 任何"阶段依赖作业完成通知推进"的 run 都可能永久挂在 waiting_for 一个已经 done 的 job 上；
- 现场只有两条绕行路径，都有代价：等平台补发通知（不确定）；或 `ts_resume`（文档语义是 retry，可能重跑已收敛的 ts_opt，产生重复作业并浪费一个 8c 槽）。

## 建议
1) 阶段推进逻辑在检查 waiting_for 时，应容忍"依赖作业已处于终态但通知丢失"的情形（按 job 状态而非事件推进）；
2) 或在 ts_inspect / ts_resume 上提供"幂等推进（advance-if-ready）"入口，明确不重跑已完成阶段；
3) 若保留 retry 语义，请在回执中显式说明本次会重跑哪些阶段。

## 现场留档
- run: `ts/ts_0015`，process.json sha256 **a738311f…**（mtime 14:36:37）
- ts_opt 输入：`ts/ts_0015/jobs/declaration_0001/ts_opt/refine.gjf` sha256 **d40325e042b9596e7f86ce2271e48e1acd1d9be958e1960fd94082765f8fecf6**
- ts_opt 日志：refine.log sha256 **0023847fe5b2e2961f9914d7a4f7a694ae11a9d826bd892b190866274f0a430b**，11,399 行
- 相关既有 issue：#194（ts_resume 被未起跑排队作业阻塞）
