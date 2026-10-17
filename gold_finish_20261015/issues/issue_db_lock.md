## 环境 / 时间
- 本机 node-local（32C/50G，WSL Ubuntu），服务：cloudra web pid 1642987 + uvicorn API pid 1642991 + scheduler pid 1642990，compute.db 位于 /home/ly/.local/share/cloudra/compute.db。
- 2026-10-15 16:15–17:20（+08:00）观测；期间有 10 个并发 agent 会话（5 个包 Coordinator + 各自子代理）在批量提交 Gaussian 作业。

## 现象（时间线）
1. 约 16:15 起，作业 guard 写库开始失败：`gold_finish_20261015/NR1/E1/scan/.cloudra/guard-903.log` 原文反复出现
   - `[guard] calculator 退出，退出码：0`
   - `[guard] 更新数据库失败：database is locked`
   - `[guard] 登记 guard_pid 失败（已忽略）: database is locked`
   906 的 guard 日志同样（`scan_P/.cloudra/guard-906.log`）。**计算本身是成功的**（原生 `pt_scan_R_01.log` / `pt_scan_P_01.log` 都有 Normal termination）。
2. 结果：903/906 的行状态**永久卡在 running**（"标 running 但无进程"），占位 8c+8c；随后 907 结束也卡住 → **28 核被空占**，队列里 908–914 七个作业全部无法启动（`waiting: not enough free cpus/memory`）。
3. 下游症状：`ts_prepare` 在任何最小声明下抛 `tool_exception: Tool execution failed internally`，**无 run_id、无 run 目录、无作业**（call_id 例 tc_81d1fd610acd4957）——因为 durable 工作流建 run 必须写库。最初被误判为独立工具 bug。
4. 独立的写锁验证：全新 python 连接对 compute.db 做 `BEGIN IMMEDIATE; ROLLBACK`，**busy timeout 20 s 仍 `OperationalError: database is locked`**；平台自身的 `mark_compute_job_failed(903/906)` 也同样返回 `mark failed: database is locked`（即"手工对账"这条官方逃生通道在当时也走不通）。

## 只读取证（不改库、不杀进程）
- `fuser -v compute.db`：持有者 = scheduler(1642990) + uvicorn API(1642991)；`runtime-v2.db` 仅被 API(1642991) 持有。
- `/proc/locks`：两个进程在 compute.db 的 WAL-index 区（offset 1073741826 起）持 POSIX ADVISORY **READ** 锁；未见其它写入者。
- `compute.db-wal` = 0 B（mtime 16:24）、`compute.db-shm` = 32 KB；**`runtime-v2.db-wal` = 954 MB**（主库 1.85 GB，mtime 持续增长）。
- `pgrep -cx g16` = 0/1：三个标 running 的作业**都没有真实 Gaussian 进程**（HL1 包独立复核一致）。

## 恢复动作与结果（可复现）
1. `kill -TERM` **scheduler** → web 巡检 3 秒内自动拉起新 scheduler（1781332），并自动为 903 派 adopt monitor(1781334) → **写锁仍在**（15 s 超时仍 locked）⇒ scheduler 不是持有者。
2. 只重启 **uvicorn API**（TERM → 启动器按原 `--port 8000` 拉起；脚本 `gold_finish_20261015/fix_db_lock.sh`，日志 `gold_finish_20261015/db_lock_recovery.log`）→ **恢复**：
   - compute.db 可写（`BEGIN IMMEDIATE` 0.0 s 成功）、`PRAGMA integrity_check` = **ok**（库**没有**被写坏）；
   - 新 scheduler 用 adopt 机制把 **903/906/907 正常收尾为 done**（无需人工 mark）；
   - 队列恢复流动（908、912 running；913/914 queued）。

## 副作用（恢复过程本身造成）
- **在跑的 agent run 被重启打断**：两个包 Coordinator 会话被标记 `runtime_interrupted`（HL1、NY3），必须重新派发唤醒才能续跑；同一批里有若干正在提交的作业被收尾为 failed（910 = HI1 的 E3 几何准备、911 = NR1 的 E2 I1 Opt+Freq），需要按原输入重提。
- 因此"重启 API"虽是有效恢复手段，但对**并发 agent 会话是有破坏性的**，建议平台提供更精细的恢复入口（见建议）。

## 建议（供 triage）
1. **guard 写库要有退避重试 + 明确失败面**：当前 calculator 退出码 0 而记账失败，日志只写"database is locked"，作业永久卡 running。
2. **orphan running 行自动对账**：对"无进程 + 无锁持有者"的 running 行定期收敛（现在只能靠重启 scheduler 触发 adopt，或人工 mark，而人工 mark 也会被同一把锁挡住）。
3. **SQLite 长事务/WAL 治理**：runtime-v2.db WAL 达到 954 MB 值得查（是否有长事务未提交、是否 checkpoint 被阻塞）；一次写锁能把整个计算队列冻死，建议隔离 compute.db 与 runtime-v2.db 的连接池/超时策略。
4. **ts_prepare 的异常要可诊断**：`tool_exception: Tool execution failed internally` 没有 run_id 也没有底层错误，导致被误报为独立工具 bug；建议把底层 DB 异常原样带出。
5. **恢复入口**：能否提供一个"重连/释放锁/重载 worker"的管理���作，避免重启 API 打断所有在跑的 agent 会话。

## 附件 / 原始证据位置
- guard 日志：`gold_finish_20261015/NR1/E1/scan/.cloudra/guard-903.log`、`gold_finish_20261015/NR1/E1/scan_P/.cloudra/guard-906.log`
- 恢复日志：`gold_finish_20261015/db_lock_recovery.log`、脚本 `gold_finish_20261015/fix_db_lock.sh`
- 未提交到仓库（工作区文件），按需提供。
