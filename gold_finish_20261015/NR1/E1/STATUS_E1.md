# NR1_E1 · STATUS 片段（E1 计算道）

状态（2026-10-15 16:15 SGT）：**计算完成 = 否 / 验收通过 = 否**。进行中，无 ΔE‡ 值。

| 边 | 状态 | run_id / run_dir | 原生日志 + sha256 | 方法 | 下一步 |
|---|---|---|---|---|---|
| NR1_E1 | 缺测（进行中）：起点结构已自建；形式级别 PT 剖面扫描 A/B 已提交 | 暂无 durable run（ts_prepare 未启动） | 903 → /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NR1/E1/scan/pt_scan_R_01.log（运行中，完成后记 sha256）；906 → .../scan_P/pt_scan_P_01.gjf（排队） | Gaussian16 B3LYP/def2SVP + GD3BJ + Int(UltraFine) + SCF=Tight，气相 q+1 m1 | 读 A/B 扫描剖面 → R 侧无约束 Opt+Freq（H3）→ 有鞍点走 ts_prepare 正式链；无鞍点整理豁免材料 |

缺什么：正式 TS（1 虚频 + 模式判据）、双向 IRC 方向区间、两端 0 虚频极小值、ΔE‡。
已证伪什么：暂无（尚未有结论）。
待裁决问题：暂无。旧 `gold_compute/jobs/NR1_*` 日志在本工作区不存在（已核实），本道从零建证据。
