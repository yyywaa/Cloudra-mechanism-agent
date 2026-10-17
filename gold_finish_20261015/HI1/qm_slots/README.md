# HI1 包 QM 槽位协议（2026-10-15 起，3 道共用 2 槽）

主协调硬约束：每包同一时刻最多 2 个 QM 作业（新提交优先 8 cpus / ≤10 GB，确有需要才 12c）。
本包现在有 3 条道：lane1 = E1（as_4c9dafe225a84580）、lane2 = E3（as_3b1f55fa9f7743a9）、lane3 = E2/EM1 (S) 重算（新会话）。

## 取槽（提交前必须）
1. `mkdir /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/qm_slots/slot1` —— 成功即持有 slot1。
2. 若 slot1 已存在，试 `mkdir .../qm_slots/slot2`；成功即持有 slot2。
3. 两个都失败 = 包内已满 2 个在飞作业 → **不要提交**；等（可 sleep 轮询）或先做非 QM 的准备工作。
4. 持有槽位期间在 `qm_slots/slotN/holder.txt` 写：道名/会话/run_id 或 job_id/提交时间。

## 释放
- 作业（或 ts_prepare/ts_resume 整条 run）进入 terminal / blocked / 明确 idle 后立刻 `rmdir .../qm_slots/slotN` 释放。
- 陈旧槽位（持有 >120 min 且 `pgrep -f g16` 为空、且队列无本包作业）可破：先在 `qm_slots/BREAK_LOG.txt` 追加破锁证据，再 rmdir。

## 注意
- ts_prepare/ts_resume 会自动连续提交多个作业：**整条 run 期间一直持有该槽**，run 结束再释放。
- 不要取消/重投已在排队的作业；不要调 priority；不要杀别人的作业。
- 缺测不填 0；不改题源/图（registry/HI1.json/hard.md 只有包 Coordinator 能改）。