# NR1 包 · 基线冻结（由包 Coordinator 代只读复核道落盘）

来源：explorer 复核道 session as_844cd0926754475a，2026-10-15 首轮 finding（该会话角色只读，write 被拒，故由包 Coordinator 按其报告原文落盘，未改动被复核文件）。
命令均为真实文件系统读取（read/ls/find/grep/sha256sum/git status），非变更流。

## 1 三个待改文件基线（git status --porcelain 仅 `?? gold_finish_20261015/`，三文件相对 HEAD 干净）

| 文件 | sha256 | 行数 | 关键内容 |
|---|---|---|---|
| cloudra/benchmark/normal_registry/ru.py | 6a20f6a7d088c8b15999c2b9def83383a46e8b4f3589188394af71604dd315de | 134 | R1 step①(=E1) L20-24、step②(=E2) L25-29 **没有 barrier 键**（契约缺省 None，不是显式 null）；step③(=E3) barrier 5.16 + weight 0.5（L34/L35）；step④(=E4) barrier 5.74（L41）。契约见 normal_registry/__init__.py：可选键 barrier，缺省 None = 无参考值不评分 |
| ideapool/tasks/normal/NR1.json | a6a17e2e53812c029cd3166b4331a04d659f9808e5e74a40d63610c57fda6920 | 262 | E1 L154 null / E2 L175 null / E3 L205 5.16 / E4 L231 5.74 |
| ideapool/reaction_candidates/normal.md | 29d55bcabdee34b3edb9c10f9a1f1368e628c9b4726a159e9bd4d099b47ea269 | 221 | R1 行 = 第 106 行（104 表头 / 105 分隔行）；能垒格现状："自算 ΔE‡ E1/E2 = null（…），E3 = 5.16 kcal/mol（…）；迁移 TS 相对质子化频哪醇起点为 20.21…"；该行引用的 "gold 工作区 NR1/REPORT.md" 本地不存在 |

## 2 既有产物清查（只有账本/题源副本，没有任何 NR1 原生日志）

- gold_compute/edge_barriers/NR1.json sha256=cbd9999a1e000b4fa58e4079afc21ccb7d10c95d9c0d3b7bf06c88c080b87982（旧 3 边口径：E1 null / E2 26.2 Yamabe2007 文献 / E3 null=去质子）
- gold_compute/edge_barriers/computed/NR1.json sha256=b5afb8f6b2ce89e2d601c73df7f0afed44902c6e7231f65bbed481006479fff2 —— ⚠ 旧 3 边编号：其 NR1_E1=0 已作废；其 NR1_E3=5.74 实际对应**现行 E4 槽**。回填/复核切勿按 id 对号入座。
- gold_compute/supplement_20261002/task_sources/NR1.json sha256=451299296d12a711162cd3ab9909bb27ee22e87f2c51713ff63714a92daa7e8c（旧版题面，261 行）
- library_audit_20261002/source_snapshot/published/… 内的旧副本：ru.py e3662f4b799bf8c027085ba52f3dde47b4943dc501b9b895964174dc01a77920(132 行) / normal.md 90b6d360ad84d8969c0125962e7e8c07d18fbfe167dcbd02af20dbe9dcd9d70f / NR1.json 451299296… / computed/NR1.json b5afb8f6…

用真实文件系统读确认**不存在**：
- `ls gold_compute/jobs` → exit=2 No such file or directory；`find . -maxdepth 2 -name jobs` 空。
- computed/NR1.json 引用的 NR1_E1_scan / NR1_R_confs / NR1_R_opt / NR1_R_freq / NR1_I1_opt / NR1_I2_freq / NR1_P_freq / NR1_E3_ts3 / NR1_E3_irc* 等：grep -rIl 只命中账本与其审计快照 → 只在账本里作为字符串存在。
- 作业 112 产物（state_112.json / *_112* / rc_build / NR1_*）：唯一命中 .venv 的 ChEMBL_11265_actives.smi（无关）。
- .cloudra 只有 tool_output；无 .cloudra/local-20261005（Mac 私有目录不在本工作区）；无 gold_compute/remote_backups。
- raw_inventory.csv 里 NR1 仅 2 行且都是 remote_backups 里的题源 json；grep 'jobs/NR1|NR1_E1_scan|state_112' → 无匹配(exit=1)。
- `find . -name REPORT.md` 只有 HI1/HG2/HL1/HE3，无 NR1。
- 全仓 NR1 的 .log/.out/.fchk 只在 tests/fixtures/** 与 research_runs/NU3-*（NU3），无 pinacol 计算输出。

=> 旧 E1=0 无法复核（支撑日志 NR1_E1_scan.log 不存在）；E1/E2 只能从零建证据，与 BRIEF §2 一致。

## 3 待产基线文件

verify/BASELINE.md（本文件）、verify/GUARD_PLAN.md 由包 Coordinator 代落盘；原要求的撰写者是 explorer 道（因角色只读被拒，已记录）。
