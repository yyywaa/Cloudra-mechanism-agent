# NR1 包 · 回填与守卫链可执行性核查（由包 Coordinator 代只读复核道落盘）

来源：explorer 复核道 session as_844cd0926754475a（只读读码结论，本轮未执行生成器）。

## 1 重新生成题面

`cd /home/ly/Cloudra-mechanism-agent && .venv/bin/python -m cloudra.benchmark.gen_normal_tasks`
默认 `--src ideapool/reaction_candidates/normal.md`、`--out ideapool/tasks/normal`。
- **`--only` 不能用于落盘**（main 里 assert len(tasks)==10；只有 --check 免断言）→ 落盘会重写全部 10 个 normal 题面（NB1 NI1 NI5 NY3 NR1 NU3 NU5 NU6 NQ1 NQ5），不碰 hard/easy/impossible。**建议先 --out 到 scratch 目录 diff 再落盘**（跨包并发写风险）。
- 生成器数据真源是 `cloudra/benchmark/normal_registry/ru.py` 的 step['barrier']；NR1.json 由它生成。

## 2 守卫测试

`python -m pytest tests/test_benchmark.py -k regenerate_identically`（4 个：easy/normal/hard/impossible 的 regenerate_identically）。

## 3 ⚠ 守卫与目标冲突（本包必须裁决）

tests/test_benchmark.py:2015 `test_pinacol_dehydration_and_migration_are_separate_edges`（约 L2021）写死：
```
assert [e.barrier_kcal_mol for e in edges] == [None, None, 5.16, 5.74]
```
一旦回填 E1/E2 的 barrier，该断言必失败 → 必须随包同步更新该期望列表（保留 [4,6]/[7,8]/[4,8]/[C+] 等结构断言不变）。
同类问题存在于别的包：如 NI5 的 `assert [e.barrier_kcal_mol for e in aqueous_edges] == [None, 3.59, 31.2]`（NI5_E1 回填后也会失败）→ 建议由主协调统一裁定 tests/test_benchmark.py 的编辑权归属，避免多包并发改同一文件互相覆盖。
本包建议：只改 R1/NR1 相关那一行期望，用 edit(path=..., expected_sha256=<最新 sha>) 保证并发安全。

## 4 md 能垒格解析约束

gen_normal_tasks.py **完全不解析** md 第 6 格能垒格（无 _parse_barrier；_parse_barrier 仅存在于 gen_easy_tasks.py:237）。故"只改 R1 行"的解析约束只有：
- 行首匹配 `^\|\s*([A-Z]\d+)\s*\|`（即 `| R1 |`）；
- cells 数 ≥8（不得增删竖线）；
- cells[2] 保持 SMILES_RE 格式、cells[6] 保持 'C,H,O；9 重原子' 风格；
- 数值真源在 ru.py 的 step['barrier']；md 只是人读文档（scripts/gen_normal_tagging.py 会读第 6 格生成 normal_tagging.html，改 md 后该 html 会变旧，需知悉）。
