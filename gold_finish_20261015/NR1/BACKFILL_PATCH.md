# NR1 回填补丁计划（DRAFT · 未执行）

> 维护：NR1 包 Coordinator as_a2aa6951d46042ae（第三任）。本文件只是**计划与冲突记录**，未对 ru.py / NR1.json / normal.md / tests 做任何改动。
> 触发条件满足且跨文件冲突裁定后才执行；执行后本文件补上执行记录与新 sha。

## 1 目标文件与本人实测基线 sha256（2026-10-15 23:4x）

| 文件 | sha256 | 备注 |
| --- | --- | --- |
| cloudra/benchmark/normal_registry/ru.py | `6a20f6a7d088c8b15999c2b9def83383a46e8b4f3589188394af71604dd315de` | R1 step①(第 20-24 行)与 step②(第 25-29 行)**没有 barrier 键**（契约缺省 None = 无参考值不评分）；step③ 第 34-35 行 barrier 5.16 + weight 0.5；step④ 第 41 行 barrier 5.74 |
| ideapool/tasks/normal/NR1.json | `a6a17e2e53812c029cd3166b4331a04d659f9808e5e74a40d63610c57fda6920` | NR1_E1 的 `barrier_kcal_mol: null`；NR1_E2 同；E3=5.16、E4=5.74 |
| ideapool/reaction_candidates/normal.md | `2c919e2714815645bf34ca2ba6f45734c593df619e3858e2869906f6593af3f0` | R1 行 = 第 106 行。⚠ 该文件已被 NI5 包改过（其 I5 行），故与 17:04 explorer 记录的 `29d55bca…` 不同；本包**只改 R1 行** |
| tests/test_benchmark.py | `587768d6d9cfc6588b5209ed9e5afa95ec46fc32f8ccc72db11a34ebff472554` | 第 2020-2030 行 `test_pinacol_dehydration_and_migration_are_separate_edges` 硬断言 `[None, None, 5.16, 5.74]`；**不在本包可改范围**（BRIEF §6） |

## 2 改动前基线守卫（本人本轮实测，改动前）
- `python -m pytest tests/test_benchmark.py -k regenerate_identically -q` → `....`（4 passed）
- `python -m pytest tests/test_benchmark.py -k pinacol -q` → `.`（1 passed）

## 3 计划改动（按证据，条件执行）

### 3.1 NR1_E1（证据：无独立鞍点 + 声明的 R 非极小值）
- ru.py：step① dict 内 `"type"` 之后新增一行 `"barrier": 0.0,`，并把第 21 行注释改成：`# PT：H3O+ 质子化 4 号碳上的 OH；气相无独立鞍点（声明的 R 复合物非驻点），按无垒记 0.0（caveat 见 gold_finish_20261015/NR1/E1/E1_FINAL_EVIDENCE.md）`。
- normal.md 第 106 行：把「`自算 ΔE‡ E1/E2 = null（质子转移未确立非零垒，脱水未找到独立鞍点）`」与引擎句一起替换为：E1 = 0.0（无垒，声明的 R 复合物在本级别气相不是极小值，见证据）+ E2 的处置（见 3.2）+ Gaussian 16 B3LYP-D3BJ/def2SVP 引擎偏差声明 + 原生日志路径/sha256 指引。
- 证据锚（值必须能由这些行复核）：E1/opt_R/optfreq_R_d230.log:80267（Optimization completed）/ :81363（末次 SCF −464.000864850）；E1/scan_O/pt_scan_O_01.log:18417/…/47853（9 个收敛点）；E1/scan/pt_scan_R_01.log 与 E1/scan_P/pt_scan_P_01.log（各 11 点）；待补：细网格 pt_scan_fine_02 与定骨架 pt_scan_fixOO_02、以及 opt_pt9 判据结果。

### 3.2 NR1_E2（条件项）
- 若连通性替代证据成立（± 位移/外框 Opt 落点分别匹配 I1 与 I2）：ru.py step② 加 `"barrier": 16.26,`，注释写明『无约束 OptTS（ts_0005 attempt1, job 933/936）− I1 = +16.26 kcal/mol；软模 −74.5623 cm⁻¹；native IRC 因软模积分失败，连通性由位移下坡外框优化替代证明』。
- 若不成立或两端同盆地：step② 维持无 barrier 键，注释改为『**无合格独立鞍点**；候选 +16.26 未通过验收（软模 + IRC 失败），见 gold_finish_20261015/NR1/E2/E2_FINAL_EVIDENCE.md』，并在 normal.md 写明缺项与是否建议与 E3 合并。

## 4 跨文件冲突（**阻塞项，待主协调裁定**）
- `tests/test_benchmark.py::test_pinacol_dehydration_and_migration_are_separate_edges`（约第 2021 行）断言 `[e.barrier_kcal_mol for e in edges] == [None, None, 5.16, 5.74]`。填任何数值（0.0 或 16.26）都会使该断言失败。
- 该断言不在本包可改范围（BRIEF §6）。需要的最小改动 = 把首个 `None` 换成实际值（如 `[0.0, None, 5.16, 5.74]`），一行。已两次请主协调裁定（hub 帖 evt_36d0b03144a0417b / evt_f92062fc988348e9）。
- 我倾向：授权后填 E1=0.0（证据最强、先例 yo.py O3 与 NI1），E2 视连通性结果；若主协调选择豁免口径，则两个 barrier 键都不加，改为在 ru.py/normal.md 注释里写明证据与缺项。

## 5 执行流程（裁定后）
1. 重取 ru.py / normal.md 的 sha256（read），再 edit；
2. `python -m cloudra.benchmark.gen_normal_tasks`（DEFAULT_SRC→DEFAULT_OUT，与生成器 __main__ 一致）重生成 NR1.json；
3. `git diff --stat` 只看本包文件（不提交 git）；
4. `python -m pytest tests/test_benchmark.py -k regenerate_identically -q`（应通过）+ `-k pinacol`（若未获授权改断言则预期 FAIL，并原样记录给主协调）；
5. 把生成器输出与 pytest 输出**原样**贴进交付报告与 hub 终态帖。
