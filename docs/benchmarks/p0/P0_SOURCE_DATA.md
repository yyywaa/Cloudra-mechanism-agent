# P0：源数据完整性（唯一标准）

> 目标只有一个：**保存到能复原一切的数据**。具体是三类——config、context、计算日志（沙箱内容）。其它文档、指标、分类都不作为门槛。

## 检查结果

| # | 源数据 | 现状 | 证据 |
|---|---|---|---|
| 1 | **config** | **缺失（需补快照）** | 数据目录里没有配置快照。`benchmark.db` 的 `batches.config` 只有 `provider/model`、`orchestration_modes`、`tasks_dirs`、`task_ids`、`concurrency`；缺 temperature/max_tokens/timeout/base_url、prompts 版本、git HEAD。全局配置在 `~/.config/cloudra/config.yaml`，未复制。 |
| 2 | **context** | **正确** | `runtime/runtime-v2.db` 的 `events` 表：run6 共 **146,563** 条。`context.appended` 保存完整消息（最近 200 条样本：system 45 / user 36 / assistant 146 / tool 136）；`tool.result_recorded` 保存完整工具结果；`agent.thinking`、`program.*` 同样在库。`runtime/conversations/` 另有项目目录。 |
| 3 | **计算日志（沙箱）** | **正确** | `sandboxes/` 完整保留：run6 **2.7G**（20 题）、full-20261022 **1.2G**；含 QM 输入/输出、`.cloudra/evidence` 快照；`runtime/compute.db` 保存作业记录。 |

## 修复（config）

启动脚本 `~/bin/run_arm.sh`：

- 跑前把 `~/.config/cloudra/config.yaml` 复制为 `<data>/config.snapshot.yaml`，并把 `key/token/secret` 脱敏（实测 67 行、5 处脱敏、0 个裸 `sk-`）；
- 写 `<data>/commit.txt`（臂 HEAD）与 `<data>/arm.txt`（arm、clone、tasks、开始/结束时间、python 版本）；
- 其余数据（DB、sandboxes、runtime）由 benchmark 自己落在同一目录。

**不改产品代码。**

## 结论

- context 与沙箱：**已经正确、完整**；
- config：**差一份快照**，用 `run_arm.sh` 补上即可；
- 之前的 01–04 报告只作参考，不再作为跑前门槛。
