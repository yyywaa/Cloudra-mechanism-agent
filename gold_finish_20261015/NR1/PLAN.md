# NR1 包作战计划（package Coordinator as_53d43419a24c485b）

> 依据：gold_finish_20261015/BRIEF.md（含 2026-10-15 算力更新）、HANDOFF_UNFINISHED_20261004.md §3「NR1_E1 与 NR1_E2」、LOCAL_RUN_20261005.md「NR1 的新只读证据」、library_audit_20261002/README.md、ideapool/tasks/normal/NR1.json、cloudra/benchmark/normal_registry/ru.py。

## 1 目标边与题面事实
- 体系：频哪醇重排，气相、q=+1、m=1、26 原子（C6H17O3 = pinacol C6H14O2 + H3O+）。
- 原子映射（题源 NR1.json，1-based，含显式 H）：1=H3O+ 的 O，2=酸性 H；3/5=C4 上两个甲基，4=离去侧碳，6=离去用 OH 的 O；7=保留侧碳，8=迁移甲基，9=保留甲基，10=保留侧 OH 的 O，11=其 H。未映射原子：水 O1 上另 2 个 H、O6 上的 H、4 个甲基共 12 个 H。
- NR1_E1：断裂 (1,2)、成键 (2,6) —— H3O+ 把质子给频哪醇 O6（离去基活化）。R=[OH3+].pinacol；I1=质子化频哪醇＋水。
- NR1_E2：断裂 (4,6) —— 质子化频哪醇脱水成叔碳正离子/水离子对（I2）。
- NR1_E3=5.16（1,2-甲基迁移）、NR1_E4=5.74（去质子）**不得改动**；旧 NR1_E1=0 一律作废，不回填。
- 关键约束（10-02 独立审计）：分子内互变 PT 规则**不自动适用**于 NR1 的分子间酸活化 → E1 不能靠 PT 豁免关边；必须给出数值，或"正式豁免申请 + 数值证据"。

## 2 起步事实（只读核对）
- 上一轮 gold 证据所在路径 `gold_compute/jobs/NR1_*`（computed/NR1.json 里引用的 112/R_confs/E1_scan/I1_opt/I2_freq/P_freq 等）在**本工作区不存在**（find 无 NR1 命名运行目录、无对应 .log）。本包必须从零建立结构、极小值与 TS 证据。
- 本机引擎：Gaussian 16 `/home/ly/g16/g16`；无 ORCA。正式级别：B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight，气相不写 SCRF。
- 队列：node-local 32C/50G，10 槽；2026-10-15 早间 0 running / 0 queued。
- TS/IRC 只能走 ts_prepare/ts_resume（durable）。手工 TS/IRC 提交被禁用。

## 3 竞争假设（必须用证据区分）
- H1（有垒）：存在"质子仍在 H3O+ 一侧"的极小值（离子-偶极/氢键复合物），其与质子化产物之间存在真正的一阶鞍点，E1 有非零 ΔE‡。
- H2（无垒）：气相 ΔPA(pinacol) ≫ ΔPA(water)，PT 沿反应坐标单调放热（旧 Gaussian 13 点扫描曾报单调下降），**不存在独立鞍点** → E1 只能按"缺测 + 正式豁免申请（附扫描/极小值/坍缩证据）+ 图裁决问题"交付，不得填 0。
- H3（起点身份）：题源声明的 R 复合物在 B3LYP-D3(BJ)/def2-SVP 气相可能不是一个极小值点（优化会坍缩到质子化形态）；则需要给出"声明的 R 是否稳定存在"的数值证据，并把裁决问题写给主协调。
- E2 竞争假设：E2a 存在独立 C4–O6 解离鞍点；E2b 无独立鞍点（异裂与 1,2-迁移耦合）→ 给出扫描/搜索证据 + 是否与相邻步（E3）合并的裁决问题。

## 4 分道（同刻只 1 个 QM 作业）
- E1 lane（small_mol）：E1 起点极小值 + TS + IRC 双向 + 两端 Opt/Freq + ΔE‡（相对本步起点极小值）。
- E2 lane（small_mol）：E2 起点极小值（质子化频哪醇＋水）+ 脱水 TS + IRC + 两端 Opt/Freq + ΔE‡；QM 必须等 E1 lane 结束的放行后开始。
- verify lane（explorer/small_mol 只读）：独立复核（虚频个数与位移方向、IRC 端点方向区间、能量算术、日志原生行、sha256），并负责本包证据清单与 STATUS.md 的独立数字复核。

## 5 交付与口径
- 证据清单：原生日志绝对路径 + sha256（不改写原生日志）；能量取日志原始行。
- 回填只在 `cloudra/benchmark/normal_registry/ru.py` R1 的 E1/E2 barrier 字段、`ideapool/tasks/normal/NR1.json` 的 NR1_E1/NR1_E2，以及 `ideapool/reaction_candidates/normal.md` R1 那一行。
- 生成题面 + 守卫测试（tests/test_benchmark.py -k regenerate_identically 相关）。
- agent_hub 主题 gold-finish-20261015 发开工帖与终态帖；终报交给 role_id=coordinator。
