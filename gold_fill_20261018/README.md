# gold 边填充 · 2026-10-18（Coordinator 工作台账）

## 0 用户指令（2026-10-18 03:0x，本会话直接回答）
「能算的都要算掉除了没有意义的边，算不出来就换题」。
- 能算的 gold 边：补算到验收标准后回填题源（registry → 生成 JSON → 守卫测试）。
- 算不出来：如实写「不可计算 + 已证伪 + 还缺什么」，然后按用户已批准的四道替换题换题，不用旧 ID 装新反应。
- 不回填对象：NB1_E2、NQ5_E2（既定 PT 豁免）；impossible 12 题（accessible=false，性质/不可达边，不属于本轮填充）。

## 1 待填边（现盘 null，2026-10-18 02:5x 直读）
| 边 | 步骤 | 现状 | 归属 / lane |
|---|---|---|---|
| HI1_E1 | 半缩胺生成（N20 进攻 C2=O4） | null | HI1 lane（待认领确认） |
| HI1_E2 | 半缩胺脱水 → 烯胺 + H2O | null | HI1 lane（待认领确认） |
| HI1_E4 | 水加成到亚铵（I2 侧） | null | HI1 lane（待认领确认） |
| HI1_E5 | 半缩胺坍缩 → aldol + 脯氨酸 | null | HI1 lane（待认领确认） |
| NR1_E1 | H3O+ → 频哪醇 OH 质子转移 | null | small_mol as_dc9158f550bd4e01 |
| NR1_E2 | 质子化频哪醇脱水 | null | small_mol as_dc9158f550bd4e01 |
| NY3_E1 | Na+ 模型 OH- 加成 | null | small_mol as_f636e5bc837f46ee |
| NY3_E2 | Na+ 模型甲氧基消除 | null | small_mol as_f636e5bc837f46ee |
| NY3_E3 | Na+ 模型甲酸→甲氧基 PT | null | small_mol as_f636e5bc837f46ee |

已填（不在本轮范围）：NI5_E1=0.93、HL1_E1=0.0（含约定口径）；HL1_E2=23.13 等历史值保留。

## 2 统一方法与证据标准
- 引擎：Gaussian 16 /home/ly/g16/g16（本机无 ORCA）；B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight；溶剂按题源（HI1=CPCM(DMSO)、NY3=CPCM(Water)、NR1=气相）。
- 能垒 = 纯电子能差（SCF Done，无 ZPE/热校正），相对该步自身起点极小值；同批同程序相减。
- 验收链：TS 恰 1 虚频且模以声明键对为主 → 双向 IRC 到达声明两端 → 两端 Opt+Freq 0 虚频 + 身份（质子/CIP/分片）→ ΔE‡。缺任一项不填数值。
- 无独立鞍点的边：只有给出可复核剖面/种子坍缩证据时才可按既有约定记 0.0，并写明「无独立鞍点、参考态为接触离子对」，不得写成算出的 0 垒 TS。

## 3 回填面（BRIEF §6 属主划分，单方写入）
- hard：cloudra/benchmark/hard_registry/hi.py（HI1）、jl.py（HL1）
- normal：ru.py（NR1）、ai.py（NI5）、yo.py（NY3）
- 生成：python -m cloudra.benchmark.gen_hard_tasks / gen_normal_tasks；守卫 pytest tests/test_benchmark.py -k regenerate_identically
- md 只改自己那一行；不提交 git，等用户决定。

## 4 协作
- 另一 coordinator：只读盘点 + 替换题 TaskSpec 草案（hub 主题 "gold 边填充 · 双协调分工"）。
- 进度以各 lane 的 STATUS.md 与 hub 终态 finding 为准；本文件只记归属与状态，不复制日志读数。

## 5 题库基线（用户 2026-10-18 03:0x 提醒「题库有更新，不要盲信现在的文件」）
- 远端 master 权威提交 = **68231b4b**「bench: sync NI5 gold and hand off replacement and impossible calculations」（03:00 用 gh api 核对，远端无更新提交）。该提交只改 NI5：ai.py E1 barrier=0.93、NI5.json 同步、tests 断言 [0.93,3.59,31.2]、新增 queue_20261018 交接文档与 PR199 评估。
- 工作区相对 master 的 gold 值差异只有两处且均未提交：HI1 拆 5 步（HI1.json E2 13.36→null、E3→13.36）、HL1_E1=0.0。HI1 五步模型属本地修订，不是官方题库字节；按五步回填时必须在交付里单列该差异。
- 回填纪律：每次改前重取现盘 sha；JSON 是生成物，只改 registry 后重生成，不手改 JSON；md 只改自己那一行。

## 6 替换题 TaskSpec 草案（writer lane，2026-10-18 03:01，只写文档不含 gold 数值）
- gold_compute/queue_20261018/specs/TASKSPEC_N_FORMAMIDE.md（196 行 / sha256 ebcd27a4daec8a18bcf5f545d1b7c6970d9cbcfdddbe0f5c19b1ea18c74b8e29）
- gold_compute/queue_20261018/specs/TASKSPEC_N_HNCO_HYDROLYSIS.md（197 行 / sha256 facd0b91de9dec94c68fb3f334a44f12ec73da0b996eb3fe9fac26338fc5c9ca）
- 可复用结论：bond_changes 用映射 SMILES 的 1-based atom-map 编号；break=键级下降、form=键级上升；构象步双空表 + registry "conformational": True；含 H 转移必须在 mapped SMILES 显式写 [H:n]，否则边表会静默变空。

## 7 平台问题处置（用户 2026-10-18 03:0x 指令）
遇到平台/工具面问题不询问用户：先只读取证（ps/pgrep、.rwf mtime、process.json、队列），整理可复现证据报 Coordinator，由 Coordinator 开 GitHub issue（仓库 yyyywaa/Cloudra-mechanism-agent）并登记台账；不自行改平台代码、不杀进程、不重启服务。

