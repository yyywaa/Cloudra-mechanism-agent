# NR1 包 · 生成/守卫 基线核查（包 Coordinator 执行，2026-10-15 17:2x SGT）

目的：在**任何回填之前**确认生成链与守卫链的健康状态，并排除『预先存在的 mismatch』（BRIEF §6 要求）。全部命令在 /home/ly/Cloudra-mechanism-agent 下执行，使用仓库自带虚拟环境。

## 1 生成器复现（非破坏性：--out 到本包 scratch 目录）
命令：`.venv/bin/python -m cloudra.benchmark.gen_normal_tasks --out gold_finish_20261015/NR1/gen_scratch`
结果：`wrote 10 tasks to gold_finish_20261015/NR1/gen_scratch`；随后逐文件与已提交题面 diff：

| 文件 | 结果 |
|---|---|
| NB1/NI1/NI5/NQ1/NQ5/NR1/NU3/NU5/NU6/NY3 .json（全部 10 个） | **SAME（逐字节一致）** |

→ **基线无预先存在的 mismatch**：当前 registry（含 ru.py 的 R1）与 normal.md 生成的 10 个 normal 题面与仓库已提交文件完全一致。
→ 副作用范围确认：该命令一次重写**全部 10 个** normal 题面（--only 落盘被 main 的 len==10 断言挡住），因此本包回填时应**先 --out 到 scratch diff、再决定是否整体落盘**，避免覆盖其它包正在改的 NI5/NY3 题面。

## 2 守卫测试基线（回填前）
命令与结果：
- `.venv/bin/python -m pytest tests/test_benchmark.py -k regenerate_identically -q` → **4 passed**（exit 0）
- `.venv/bin/python -m pytest tests/test_benchmark.py -k 'pinacol or normal' -q` → **2 passed**（exit 0）

因此 `tests/test_benchmark.py::test_pinacol_dehydration_and_migration_are_separate_edges` 的断言 `[e.barrier_kcal_mol for e in edges] == [None, None, 5.16, 5.74]` 现在**通过**；一旦把 E1/E2 的 barrier 回填成非 None，该断言必然失败，需同步改该期望行（编辑权待主协调裁定，见 verify/GUARD_PLAN.md §3）。

## 3 结论
- 生成链与守卫链本身健康（非破坏性复现 + 基线全绿）。
- NR1 的回填风险只有一处：若填 E1/E2 的值，必须同步更新 tests/test_benchmark.py:2015–2022 里 R1 相关的那一行期望（并保留结构断言）。
- 本包的 scratch 产物不属于交付物，仅作基线证据：gold_finish_20261015/NR1/gen_scratch/*.json。
