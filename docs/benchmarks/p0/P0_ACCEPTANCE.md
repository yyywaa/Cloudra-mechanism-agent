# P0 验收报告（已缩小口径）

> **P0 的唯一标准已改为：源数据是否完整到可以复原一切。**
> 具体只有三类数据：**config、context、计算日志（沙箱内容）**。
> 判定与证据见 [`P0_SOURCE_DATA.md`](P0_SOURCE_DATA.md)。

## 结论

- **context**：完整（`runtime/runtime-v2.db` 事件流，run6 共 146,563 条，含完整消息与工具结果）。
- **计算日志**：完整（`sandboxes/`，run6 2.7G、full-20261022 1.2G）。
- **config**：缺一份快照，已用 `run_arm.sh` 在跑前补齐（脱敏 config + commit/arm 记录，不改产品代码）。

## 其它文档的地位

- `00_lead_checks.md`、`01_arm_behavior.md`、`02_bc_diff.md`、`03_evidence_chain.md`、`04_freeze.md`：
  **仅作参考**，不再作为跑前门槛，也不再列 blocking 项。
- 模型/预算/api-pool/重复次数等运行参数按用户裁决执行：`deepseek-v4-flash`（1017）、预算不设上限、不用 api-pool、全量 `r=1` + 四档各一题 `r=3`。
