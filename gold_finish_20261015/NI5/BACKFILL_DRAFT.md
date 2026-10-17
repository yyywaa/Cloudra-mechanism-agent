# NI5_E1 回填预演（流程与守卫 lane）· 草稿

> **状态：已应用（APPLIED，2026-10-15）** —— 主协调裁定（hub 回执 evt_e97930be7dc046ff）授权后已落盘；回填后守卫全绿。§1–§9 保留预演阶段的「未应用」语境与改动前基线证据，**实际落盘记录、四个文件的新 sha256、命令输出与 git status 见 §10**。
> 作者：NI5 包 Coordinator 子代理（回填预演 lane）· 日期 2026-10-15
> 前置：gold_finish_20261015/BRIEF.md §4/§6（+ §9 政策更新）、gold_finish_20261015/LEDGER.md「追加裁定（2026-10-15 16:30 巡检）」第 3 条、durable TS 链 ts/ts_0006（revision 75 / status=ended / result.verified=true）

## 0 结论摘要

| 项 | 结论 |
|---|---|
| 基线 a) 生成器校验 | **exit 0**，"check passed: 10 tasks"（无预先 mismatch） |
| 基线 b) regenerate_identically 守卫 | **exit 0**，4 passed（无预先 mismatch） |
| Patch 1（ai.py barrier + 注释） | 文本已备好，**可直接喂 edit**（old_string 已验证在文件内唯一）；占位符故意非数值 → 必须拿到裁决数字后一次落盘 |
| Patch 2（normal.md 第 55 行脚注） | 文本已备好，可直接喂 edit；**对生成产物影响 = 0**（barrier 来自 registry，不来自 md） |
| 应用 Patch 1 后是否影响其它生成产物 | **不影响任何其它生成产物**（只有 ideapool/tasks/normal/NI5.json 变内容）；**但会打挂 1 个既有测试断言** tests/test_benchmark.py:1991 —— 该文件不在本包归属表内，需主协调授权 |

---

## 1 题面重新生成链：确切命令、写盘行为、守卫语义（读码结论）

### 1.1 确切命令（与 __main__ 用法一致）

- 生成器入口：cloudra/benchmark/gen_normal_tasks.py（sha256 = ca3e95a88fda4da487380b5e36a7d5c577e0b4be4acee60b9a93963141ec738d，473 行）
- docstring 第 31 行的用法串（与 argparse 448–451 行一致）：

~~~
Usage:  python -m cloudra.benchmark.gen_normal_tasks [--out DIR] [--only A1 ...] [--check]
~~~

- **真正重新生成题面（会写盘）**：

~~~
cd /home/ly/Cloudra-mechanism-agent && python -m cloudra.benchmark.gen_normal_tasks
~~~

- **只校验不落盘**（本任务基线 a）：

~~~
cd /home/ly/Cloudra-mechanism-agent && python -m cloudra.benchmark.gen_normal_tasks --check
~~~

- 参数（448–451 行）：--src（默认 75 行 ideapool/reaction_candidates/normal.md）、--out（默认 76 行 ideapool/tasks/normal）、--only、--check。

### 1.2 是否会写盘 / 会写哪些文件

- --check：**不写盘**。main() 455–459 行打印 "OK <task_id>: N nodes, M steps" 后 return，早于任何 mkdir/write。
- 不带 --check：**会写盘** —— 462 行 args.out.mkdir(parents=True, exist_ok=True)；463–468 行对每题 write_text(json.dumps(task.model_dump(mode="json", by_alias=True), ensure_ascii=False, indent=2))；469 行打印 "wrote 10 tasks to <out>"。
- 写入文件**固定 10 个**（文件名 pattern 见 464 行 args.out / f"{t.task_id}.json"；名单见 90–92 行 TASK_IDS）。实测（只读 dry-run，未写盘）打印的目标路径：

~~~
TARGET_FILES:
  /home/ly/Cloudra-mechanism-agent/ideapool/tasks/normal/NB1.json
  /home/ly/Cloudra-mechanism-agent/ideapool/tasks/normal/NI1.json
  /home/ly/Cloudra-mechanism-agent/ideapool/tasks/normal/NI5.json
  /home/ly/Cloudra-mechanism-agent/ideapool/tasks/normal/NY3.json
  /home/ly/Cloudra-mechanism-agent/ideapool/tasks/normal/NR1.json
  /home/ly/Cloudra-mechanism-agent/ideapool/tasks/normal/NU3.json
  /home/ly/Cloudra-mechanism-agent/ideapool/tasks/normal/NU5.json
  /home/ly/Cloudra-mechanism-agent/ideapool/tasks/normal/NU6.json
  /home/ly/Cloudra-mechanism-agent/ideapool/tasks/normal/NQ1.json
  /home/ly/Cloudra-mechanism-agent/ideapool/tasks/normal/NQ5.json
~~~

- 语义提醒：**非 check 一次重写全部 10 个 normal JSON**（内容不变的 9 个只是字节相同的重写，mtime 会变）。想只生成一题要用 --only，但 **--only 只能配 --check**：非 check 路径 461 行有 assert len(tasks) == 10，--only 必然 SystemExit；该 assert 也在 mkdir 之前 → 不会留半成品。
- 校验失败语义：parse_normal_md 内逐题 _validate_task（380–383 行收集），末尾 436–438 行 raise SystemExit("registry 校验失败：" + 换行 + 逐条) → **在 461 行 assert / 462 行 mkdir 之前中止，校验失败时不会写盘**。

### 1.3 -k regenerate_identically 守卫到底比较什么

选中 4 个测试（tests/test_benchmark.py 1923 / 1935 / 2029 / 2140 行），与本包相关的是 **1935 行 test_normal_tasks_regenerate_identically**（文件 sha256 = e86446ddcfb42b513ec4b847fcf5a0ad8f6ff92b3038576dba39716787a0cd8a，4193 行）：

- 1941 行：现场从 **md + registry** 重新生成对象（不读盘）—— tasks = gen_normal_tasks.parse_normal_md(gen_normal_tasks.DEFAULT_SRC)；
- 1942 行：assert len(tasks) == 10；
- 1944 行：committed = gen_normal_tasks.DEFAULT_OUT / f"{t.task_id}.json"；
- 1945 行：assert committed.is_file(), f"missing committed task file: {committed}" —— 缺文件时提示里**带完整路径**；
- 1946 行：regenerated = json.loads(json.dumps(t.model_dump(mode="json", by_alias=True)))；
- **1947 行（核心）：assert json.loads(committed.read_text(encoding="utf-8")) == regenerated** —— 即「现算对象」与「磁盘上 ideapool/tasks/normal/ 下逐题 10 个 JSON（含 NI5.json）」**全字段 JSON 等值**：query 字符串、gold 图（节点/边/bond_changes/barrier_kcal_mol/weight）、rubric、method_policy 全比；
- 1949 行：assert t.method_policy.allowed_methods == ["xtb", "pm7", "b3lyp/def2svp"]。
- 失败提示：1947 行是**裸 assert（无 message）** → pytest 只给 AssertionError + 两个 dict 的差异片段，**不会**说明「哪个字段漂了」（对比 1945 行会打印路径）。所以回填时"哪一处不一致"要靠自己看 diff。

- 关键注意：**--check 不与磁盘比对**（§1.2），所以 --check 绿 ≠ 无漂移；唯一能发现磁盘漂移的是这个守卫。

### 1.4 预先存在的 mismatch

**没有。** 改动前两条命令全绿（§2），并且三个相关文件相对 HEAD 无任何改动（§2.3）。

---

## 2 基线（改动前，原样输出）

工作目录 /home/ly/Cloudra-mechanism-agent；解释器 = 仓库 venv（/home/ly/Cloudra-mechanism-agent/.venv/bin/python，Python 3.12.3，rdkit ok）。命令带 2>&1 合并 stderr，末尾回显 exit code；__EXIT__ 行是回显标记，不是程序输出。

### 2.1 a) 生成器校验

命令：

~~~
cd /home/ly/Cloudra-mechanism-agent && python -m cloudra.benchmark.gen_normal_tasks --check 2>&1; echo "__EXIT__=$?"
~~~

原样输出：

~~~
OK NB1: 5 nodes, 2 steps
OK NI1: 5 nodes, 2 steps
OK NI5: 7 nodes, 3 steps
OK NY3: 7 nodes, 3 steps
OK NR1: 9 nodes, 4 steps
OK NU3: 7 nodes, 3 steps
OK NU5: 7 nodes, 3 steps
OK NU6: 5 nodes, 2 steps
OK NQ1: 5 nodes, 2 steps
OK NQ5: 5 nodes, 2 steps
check passed: 10 tasks
__EXIT__=0
~~~

**退出码 0**；NI5 = 7 nodes / 3 steps，与 registry 的结构（1 加成 + 1 接力成羟胺 + 1 脱水）一致。

### 2.2 b) 回填守卫

命令：

~~~
cd /home/ly/Cloudra-mechanism-agent && pytest tests/test_benchmark.py -k regenerate_identically -q 2>&1; echo "__EXIT__=$?"
~~~

原样输出：

~~~
....                                                                     [100%]
__EXIT__=0
~~~

**退出码 0**；4 个测试（easy / normal / hard / impossible）= 4 个点全过，**无预先存在的 mismatch**。

### 2.3 补充只读证据（供判断，非基线命令）

~~~
$ git status --porcelain | head -20
?? gold_finish_20261015/
?? structure.zmat
?? ts/
$ git diff --stat -- cloudra/benchmark/normal_registry/ai.py ideapool/reaction_candidates/normal.md ideapool/tasks/normal/
（空输出）
~~~

→ 三个回填相关文件相对 HEAD **无任何修改**，工作区只有本战役新增的未跟踪目录/文件。这是「我改动前就是绿的」的直接依据。

另一条只读 dry-run（在内存里给 I5 第 1 步塞不同 barrier 值，调真校验函数，**不落盘**）：

~~~
TARGET_FILES:
  /home/ly/Cloudra-mechanism-agent/ideapool/tasks/normal/NB1.json
  ... （10 个，同 §1.2）
PLACEHOLDER -> ["could not convert string to float: '__NI5_E1_BARRIER__'"]
NUMERIC 0.93 -> []
NUMERIC 250 -> ['第 1 步 barrier 数值非法: 250.0']
~~~

→ 占位符会**硬失败**（不是静默忽略）；换成数字（如 0.93）校验通过；超 200 会被 _validate_task 231–233 行的范围检查拒绝。

---

## 3 Patch 1：cloudra/benchmark/normal_registry/ai.py 补 I5 第 1 步 barrier + 注释

改前文件 sha256（read 取）= **9ea97538e94e49953395d10675066ef845d605f3af5ca0f4cfa5bfdb58cbc330**（145 行）。

### 3.1 改前该段行号

| 行号 | 内容 |
|---|---|
| 114–115 | I5 的族注释（水溶液对偶版来源） |
| 116 | "I5": { |
| 117–120 | name_en / conditions_en / smiles_schematic / mapped_reactants |
| **121–125** | I5 头部注释块（含"文献两水辅助 ≈ 26.7"，见 §7 选项 B） |
| **126** | "steps": [ |
| **127** |             {  ← 第 1 步（= 边 NI5_E1）开始 |
| **128** | "out": "[O-:2][CH2:1][N+:3]([H:5])([H:6])[CH3:4]", |
| **129** | "type": "amine addition to the carbonyl -> zwitterionic C-N addition intermediate (relay water omitted from schematic SMILES)", |
| **130** |             },  ← 该步**没有** barrier 键（契约默认 None → 生成物里是 null） |
| 131–135 | 第 2 步（barrier 3.59） |
| 136–140 | 第 3 步（barrier 31.2） |

「steps」键在同文件多处出现，所以 old_string 必须含第 1 步的 out/type 两行才唯一（实测：zwitterionic C-N addition intermediate 与 [O-:2][CH2:1][N+:3] 在 ai.py 内各只出现 1 次）。

### 3.2 精确 patch 文本（old_string → new_string）

**old_string**（ai.py 第 126–130 行，逐字）：

~~~
        "steps": [
            {
                "out": "[O-:2][CH2:1][N+:3]([H:5])([H:6])[CH3:4]",
                "type": "amine addition to the carbonyl -> zwitterionic C-N addition intermediate (relay water omitted from schematic SMILES)",
            },
~~~

**new_string**（逐字；占位符带引号，理由见 §3.4）：

~~~python
        "steps": [
            {
                # E1（C–N 加成）自算能垒：本战役引擎为 Gaussian 16（/home/ly/g16/g16）——
                # B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight
                # + SCRF=(CPCM,Solvent=Water)，q0/m1；本值是纯电子能（不含 ZPE/热校正），
                # 相对本步自身起点极小值 = 题面声明的六元接力环 RC-A（E = -286.605711957 Eh，
                # 36 模 0 虚频，同一批 Gaussian 16）。
                # 引擎差异（必须写明）：本机无 ORCA，本步数值由 Gaussian 16 得到，与紧随其后的
                # ORCA 5.0.2 值（E2 3.59 / E3 31.2）不是同一程序，不可跨程序混减；
                # 相减两端（TS 与 RC-A）均取自同一批 Gaussian 16 日志。
                # 证据：durable 链 ts/ts_0006（revision 75 / status=ended / result.verified=true）——
                # TS 优化 job 952（ts_opt/refine.log，E = -286.604225293 Eh）、频率 job 953
                # （frequency/frequency.log，恰 1 虚频 -164.4792 cm^-1）、IRC job 954 双向、
                # 两端点 955/956 与 957/958 均 36 模 0 虚频。
                # 数值待主协调裁决后填入（裁决项：参考态 RC-A vs RC-B/分离碎片；
                # BRIEF §4 第 1 条：虚频模是否须以重原子/watch pair 为主）。
                "out": "[O-:2][CH2:1][N+:3]([H:5])([H:6])[CH3:4]",
                "type": "amine addition to the carbonyl -> zwitterionic C-N addition intermediate (relay water omitted from schematic SMILES)",
                "barrier": "__NI5_E1_BARRIER__",
            },
~~~

### 3.3 edit 工具调用参数

**首次应用 Patch 1**（改前 sha256 直接填）：

~~~json
{
  "path": "cloudra/benchmark/normal_registry/ai.py",
  "expected_sha256": "9ea97538e94e49953395d10675066ef845d605f3af5ca0f4cfa5bfdb58cbc330",
  "edits": [
    {"old_string": "<§3.2 的 old_string>", "new_string": "<§3.2 的 new_string>"}
  ]
}
~~~

**裁决数字到手后**：推荐把 §3.2 new_string 里的 "__NI5_E1_BARRIER__" 直接换成数字（例：0.93），一次应用；若已先落了占位符版本，用下面两步 edit：

~~~json
{
  "path": "cloudra/benchmark/normal_registry/ai.py",
  "expected_sha256": "<应用 Patch 1 后用 read 重取的 sha256>",
  "edits": [
    {"old_string": "\"barrier\": \"__NI5_E1_BARRIER__\",", "new_string": "\"barrier\": 0.93,"}
  ]
}
~~~

### 3.4 为什么占位符要加引号（重要）

- 写成 "barrier": "__NI5_E1_BARRIER__",（**字符串**）：ai.py 仍可 import（不会 NameError），失败被限制在 **registry 校验**这一层，报错文本可读（I5: could not convert string to float: '__NI5_E1_BARRIER__'，实测见 §2.3）；而且生成器在写盘前就中止（§1.2），**不会污染 ideapool/tasks/**。
- 若写成不带引号的裸名字 __NI5_E1_BARRIER__：import / REGISTRY 构建时直接 **NameError**，normal 档 10 题全部打不开（不只是 I5）。
- 结论：**用带引号版本**（§3.2 给的就是带引号版本）。

### 3.5 patch 可应用性判定

- old_string 已在文件内验证唯一（§3.1），缩进/标点/破折号逐字取自 read 输出 → **可直接喂 edit**。
- 但**不能与占位符一起长期驻留**：占位符在盘上时 --check、非 check 生成、regenerate_identically 都会失败（§2.3 实测）。建议按 §6 序列：**裁决数字到手 → Patch 1 带数字一次应用 → 生成 → 守卫**。

---

## 4 Patch 2：ideapool/reaction_candidates/normal.md 第 55 行（I5 行）脚注更正

依据：gold_finish_20261015/LEDGER.md「追加裁定（2026-10-15 16:30 巡检）」第 3 条 —— **批准**把「文献两水辅助 26.7」从加成（E1）语境挪到脱水/质子转移语境，并把加成步锚到 3.5 kcal/mol（Hall & Smith 1998 JPCA 102, 4930, DOI 10.1021/jp9810825）；**限改该行文字，不改数值/SMILES/图**。

### 4.1 改前 sha256

- read 返回的**整文件** sha256（应用 edit 时填的 expected_sha256）：**29d55bcabdee34b3edb9c10f9a1f1368e628c9b4726a159e9bd4d099b47ea269**（221 行）。
- **第 55 行单行** sha256（命令 sed -n '55p' … | sha256sum，含行尾换行）：**452d7e3a12aa5dda263b9fcecb78ad0393dd115b13ac54001636a35bb38e8c37**。
- 该行即 I5 行，位于「## I. 羰基-胺缩合与缩醛化学」表（表头 49 / 分隔 50 / I1 51 / I2 52 / I3 53 / I4 54 / **I5 55**）；行末列是「I1 的水溶液对偶题（2026-09-25 新收；原 I1 气相版保留）」。

### 4.2 精确 patch 文本

只替换该行「gold 能垒锚点」格里**最后一句文献脚注**；该行其它字符（含 3.59 / 31.2 两个数值、SMILES、NI1/REPORT.md 引用、C,H,N,O 格）一律不动。

**old_string**（文件内唯一；唯一性锚点 加成尚无 在 normal.md 只出现 1 次，实测）：

~~~
文献两水辅助约 26.7（Hall & Smith 1998 J. Phys. Chem. A 102, 4930, DOI 10.1021/jp9810825）；E1 C–N 加成尚无无约束 TS 能垒，暂缺测
~~~

**new_string**（逐字）：

~~~
文献对照（注意语境归属）：两水辅助约 26.7 kcal/mol 属羟胺→亚胺的分子内质子转移/脱水步（非 C–N 加成步；G2(MP2,SVP)、气相、2 显式水、相对 MA+FA+2H₂O 复合物、电子能；Hall & Smith 1998 J. Phys. Chem. A 102, 4930, DOI 10.1021/jp9810825）；C–N 加成步的文献锚为 3.5 kcal/mol（同一文献：complex→羟胺整体最低垒，含 C–N 成键与质子转移；该文摘要未给单独成键步垒值；与本处 CPCM(水) 自算口径不可直接相减）；E1 C–N 加成尚无无约束 TS 能垒，暂缺测
~~~

要点核对：① 26.7 明确归到脱水/质子转移步；② 加成步锚 3.5 kcal/mol 且注明出处；③ 保留原句尾「E1 C–N 加成尚无无约束 TS 能垒，暂缺测」（与 explorer 的文献核对一致，见 §8）；④ 未改任何数字/SMILES/图表列。

### 4.3 edit 工具调用参数

~~~json
{
  "path": "ideapool/reaction_candidates/normal.md",
  "expected_sha256": "29d55bcabdee34b3edb9c10f9a1f1368e628c9b4726a159e9bd4d099b47ea269",
  "edits": [
    {"old_string": "<§4.2 的 old_string>", "new_string": "<§4.2 的 new_string>"}
  ]
}
~~~

### 4.4 对生成产物的影响：**零**

gen_normal_tasks.py 从 md 只取 4 处：354 行 ROW_RE 匹配行、363 行 cells[2]（SMILES 格 → 反应物/产物/电荷/重数）、371 与 373 行 cells[6]（元素/重原子数）；**barrier 一律来自 registry**（276 行 barrier_kcal_mol=step.get("barrier")，231 行校验），**从不解析 md 的「能垒锚点」格（cells[5]）**。所以改第 55 行的脚注文字，NI5.json 与任何生成产物**逐字节不变**。这条 patch 是纯文档更正。

---

## 5 应用 Patch 1（ai.py barrier）后的影响面

### 5.1 会变的生成产物：只有 ideapool/tasks/normal/NI5.json 一处

- 依据：边 id 带题目前缀、由该题自己的 registry 条目生成 —— _build_graph 258–276 行循环 entry["steps"]，边 id 为 N{tid}_E{k}，barrier_kcal_mol=step.get("barrier")（276 行）；每题一个输出文件（463–468 行）。
- 具体差别：ideapool/tasks/normal/NI5.json **第 136 行 "barrier_kcal_mol": null**（边 NI5_E1，id 在第 116 行）→ 变成裁决数字；其它行不变。
- **不会**变的同文件内容（都是"依据行号"可查的）：
  - 第 7 行 query：barrier_enabled = any(e.barrier_kcal_mol is not None for e in graph.edges)（386 行）在本改动**前后都是 True**（E2=3.59 / E3=31.2 早已有值），故 require_node_energies=barrier_enabled（409 行）不变 → 「Declare every barrier you actually compute …」那段契约句**本来就已在该 query 里**（NI5.json 第 7 行原文可见），prompt 文本零变化；
  - 第 220 行 "enabled": true（rubric.accuracy，来源 430 行 enabled=barrier_enabled）前后不变；
  - 图结构、SMILES、bond_changes、weight、method_policy 全不变（只改 barrier 一个键）。

### 5.2 其它生成产物：不受影响（含依据行号）

- **其它 9 个 normal JSON**（NB1/NI1/NY3/NR1/NU3/NU5/NU6/NQ1/NQ5）：内容不受影响（各自由自己的 registry 条目与各自的 md 行决定，258–276 行）；唯一副作用是**非 check 生成会把 10 个文件全部重写一遍**（463–468 行）→ 未变的 9 个字节相同、mtime 变化。
- **easy / hard / impossible 档 JSON**：由各自 md + gen_easy_tasks / gen_hard_tasks / impossible 生成器产出；normal_registry 只被 gen_normal_tasks 使用（58 行 from cloudra.benchmark.normal_registry import REGISTRY）→ 不受影响。
- **历史快照**：gold_compute/library_audit_20261002/source_snapshot/published/ideapool/tasks/normal/NI5.json 是**冻结的历史副本**，生成器不写它 → 保持不变（历史留痕）。
- **池内未定稿条目**：TASK_IDS（90–92 行）不含 I5 以外的本次相关项；本次只动 I5 条目内的一个键。

### 5.3 会被打挂的**测试**（不是生成产物，但必须一并处置）

| 位置 | 内容 | 影响 |
|---|---|---|
| tests/test_benchmark.py:1947 | normal regenerate_identically：磁盘 NI5.json == 现算对象 | 应用 Patch 1 后、**未重新生成前**必失败（磁盘仍 null）；重新生成后通过 |
| **tests/test_benchmark.py:1991** | assert [e.barrier_kcal_mol for e in aqueous_edges] == [None, 3.59, 31.2]（测试 test_aqueous_imine_barrier_stays_separate_from_gas_phase_task，1980 行 def） | **硬编码把 E1 期望为 None** → 一旦回填数字，该测试**必失败**；须同步把列表首项改成裁决数字，否则 pytest tests/test_benchmark.py 整体不绿 |
| tests/test_benchmark.py:1987 | gas 版 NI1 期望 [27.9, 57.67] | 不受影响（I1 条目未动） |

⚠ tests/test_benchmark.py **不在** BRIEF §6 的包文件归属表（该表只给 registry / 生成题面 / md 行）→ 改这一行需要主协调明确授权。这是「一键回填」闭环的最后一块。

---

## 6 裁决数字到手后的「一键回填」序列（建议；本 lane 本轮不执行）

~~~bash
cd /home/ly/Cloudra-mechanism-agent
# 1) 应用 Patch 1（§3.2 old→new，把 __NI5_E1_BARRIER__ 换成裁决数字）
#    应用 Patch 2（§4.2）—— 纯文档，可同时做
# 2) 重新生成 normal 题面（重写 10 个 JSON；只有 NI5.json 内容变化）
python -m cloudra.benchmark.gen_normal_tasks
# 3) registry 层校验
python -m cloudra.benchmark.gen_normal_tasks --check
# 4) 更新 tests/test_benchmark.py:1991 的期望列表首项（需主协调授权）
# 5) 守卫
pytest tests/test_benchmark.py -k regenerate_identically -q
pytest tests/test_benchmark.py -k aqueous_imine -q
# 6) 留证：NI5.json barrier 行号 + sha256、两条测试输出写入本包 STATUS/EVIDENCE
~~~

---

## 7 风险、依赖与待裁决

1. **数值依赖（硬阻塞）**：__NI5_E1_BARRIER__ 是故意非数值的占位符 → 盘上驻留即校验失败（§2.3 实测）。**不要单独应用 Patch 1 的占位符版本**；要么等数字，要么按 §6 一次做完。
2. **裁决项（决定"数字本身"）**：
   - **参考态**：题面声明起点 RC-A（-286.605711957 Eh）vs 本轮另测到的更低络合物 RC-B（-286.610034975 Eh，比 RC-A 低 2.713 kcal/mol）vs 三分离碎片。改参考态则数字随之变（相对 RC-B 约 +2.713 量级）。
   - **BRIEF §4 第 1 条虚频模口径**：ts_0006 的 -164.4792 cm^-1 模由醛基 H 主导（重原子占比 15.3%、质量加权约 32%、C1+N6 未加权位移各 ~0.02–0.03 Å），explorer 记为 pseudo-saddle 风险项；这一条直接决定「+0.93 能不能当 ΔE‡ 回填」。
   - **IRC 原生早停**（每向 1 帧、ΔE≈0.006 kcal/mol）是否需更大步长重跑。
   - **政策更新（BRIEF §9 / hub 帖 evt_8d124365e7e345cb）**：包内现在可按证据自行决定机理/参考态。本 lane 不自行拍板，只据此说明：若沿用 RC-A 口径，数字即已算出的 +0.93；若改参考态或剔除 pseudo-saddle，需重新给数。
3. **测试文件不在归属表内**：tests/test_benchmark.py:1991 必须同步改（§5.3）。请裁决由谁改、改前是否重取该文件 sha256。
4. **同文件另一处 26.7 语境（选项 B，未获批准，勿单独应用）**：ai.py 第 121–125 行的 I5 头部注释同样把「文献两水辅助 ≈ 26.7」写在 I5 步列表正上方，语义与 md 第 55 行原句同错位。裁定 3 只批了 md 行；是否同步更正 ai.py 注释（属 BRIEF §6 允许的"必要注释"范围）请主协调一句话裁定。若批准，patch 为：old_string = 「# 由 smiles_schematic 和步类型声明；文献两水辅助 ≈ 26.7」 / new_string = 「# 由 smiles_schematic 和步类型声明；文献两水辅助 ≈ 26.7 属羟胺→亚胺的 PT/脱水步（加成步文献锚 3.5）」——仍只是注释，不改任何数值。
5. **「改前就存在的 mismatch」**：无（§1.4 / §2）。未来守卫若报 diff，先确认漂移是否落在本包 3 个文件之外。
6. **纪律遵守**：不改原生日志、不提交 QM 作业、不提交 git、不动平台代码/数据库、不杀进程；git status 里的 ?? gold_finish_20261015/ 等未跟踪项即战役产物，未 stage、未 commit。

---

## 8 证据与来源路径（可复核）

| 用途 | 路径 / 标识 |
|---|---|
| 生成器（读码） | cloudra/benchmark/gen_normal_tasks.py sha256 ca3e95a88fda4da487380b5e36a7d5c577e0b4be4acee60b9a93963141ec738d（用法串 31 行；--check 455–459；assert 461；写盘 462–469；md 解析 354/363/371/373；barrier 来源 231/276；barrier_enabled 386；query 409；rubric 430） |
| 守卫（读码） | tests/test_benchmark.py sha256 e86446ddcfb42b513ec4b847fcf5a0ad8f6ff92b3038576dba39716787a0cd8a（normal 守卫 1935–1949；NI5 断言 1980–1997，其中 1991 为硬编码期望） |
| Patch 1 目标 | cloudra/benchmark/normal_registry/ai.py sha256 9ea97538e94e49953395d10675066ef845d605f3af5ca0f4cfa5bfdb58cbc330（I5 条目 116–142；第 1 步 127–130） |
| Patch 2 目标 | ideapool/reaction_candidates/normal.md sha256 29d55bcabdee34b3edb9c10f9a1f1368e628c9b4726a159e9bd4d099b47ea269（I5 行 = 第 55 行；单行 sha256 452d7e3a12aa5dda263b9fcecb78ad0393dd115b13ac54001636a35bb38e8c37） |
| 生成产物（回填落点） | ideapool/tasks/normal/NI5.json（边 id NI5_E1 在 116 行、barrier null 在 136 行、3.59 在 162 行、31.2 在 196 行、rubric enabled 在 220 行）；**改前 sha256 = a9fb0d763142f52c6d283c95124b486f34dc84833c31d4f93331448cc55b14b5**（回填后应变化，可据此确认落盘） |
| NI5_E1 数值与 TS 链 | ts/ts_0006（revision 75 / status=ended / result.verified=true）；关键日志 ts/ts_0006/jobs/declaration_0005/{ts_opt/refine.log, frequency/frequency.log, irc/irc.log, reactant_opt/reactant_opt.log, reactant_frequency/reactant_frequency.log, product_opt/, product_frequency/} |
| 本轮数值口径 | TS -286.604225293 Eh；RC-A -286.605711957 Eh；产物（两性离子·H2O）-286.613531483 Eh；ΔE‡ = **+0.93 kcal/mol**（相对 RC-A，纯电子能，同批 Gaussian 16）；频率：TS 恰 1 虚频 -164.4792 cm^-1、两端 0 虚频 |
| 文献语境（3.5 vs 26.7） | gold_finish_20261015/NI5/notes/explorer_E1_review_20261015.md 第 10–11、17、39–40、70 行；hub 帖 evt_fd2f5caabcd2483e / evt_5b87c1940a754b04；Hall & Smith 1998 JPCA 102, 4930, DOI 10.1021/jp9810825；Liao 2007 DOI 10.1021/jp070130v（第二个 26.7，同属 1,3-PT/脱水步） |
| 裁决依据 | gold_finish_20261015/BRIEF.md §4/§6/§9；gold_finish_20261015/LEDGER.md「追加裁定 2026-10-15 16:30」第 3 条；hub 帖 evt_8d124365e7e345cb |

> **当前状态：Patch 1–4 已落盘（2026-10-15）；守卫全绿；四个文件 sha256 与命令输出见 §10。**
---

## 10 落盘记录（2026-10-15，主协调裁定 evt_e97930be7dc046ff 授权后执行）

执行者：本 lane（NI5 回填预演 lane）。**本节之前的一切「未应用」表述属历史记录；以本节为当前状态。**

### 10.1 四个文件的 sha256（改前 → 改后）

| 文件 | 改前 sha256 | 改后 sha256 |
|---|---|---|
| cloudra/benchmark/normal_registry/ai.py | 9ea97538e94e49953395d10675066ef845d605f3af5ca0f4cfa5bfdb58cbc330 | **ecfe72de64e23915ea76c8f6ca150caa3844440b1907902651871274e5d75c70** |
| ideapool/reaction_candidates/normal.md | 29d55bcabdee34b3edb9c10f9a1f1368e628c9b4726a159e9bd4d099b47ea269 | **6830cc15bbe490e3f4cdf0086a9847d03c9f474943eb095d435681ee1cf7e185** |
| tests/test_benchmark.py | e86446ddcfb42b513ec4b847fcf5a0ad8f6ff92b3038576dba39716787a0cd8a | **587768d6d9cfc6588b5209ed9e5afa95ec46fc32f8ccc72db11a34ebff472554** |
| ideapool/tasks/normal/NI5.json（生成产物） | a9fb0d763142f52c6d283c95124b486f34dc84833c31d4f93331448cc55b14b5 | **f76c4218b0286f2e35e60391fcfe122b1045e0cb14974829e37af0b9bd6b817b** |

做了什么（4 处，均在授权范围内）：
1. ai.py：I5 第 1 步补 "barrier": 0.93 + 注释（Gaussian 16 口径、相对 RC-A、纯电子能、引擎差异不可混减、ts_0006 证据、裁定依据）。
2. ai.py：I5 头部注释的文献语境更正（26.7 → 羟胺→亚胺的 PT/脱水步；加成步锚 3.5 kcal/mol）。
3. normal.md 第 55 行：同上的 md 脚注更正（未动任何数值/SMILES/图）。
4. tests/test_benchmark.py:1991：期望值 [None, 3.59, 31.2] → [0.93, 3.59, 31.2]（仅该行 + 3 行注释，其余测试逻辑不动）。
5. 重新生成 normal 题面（写盘）；NI5.json 第 136 行 "barrier_kcal_mol": null → 0.93（第 162 行 3.59、第 196 行 31.2 不变）。

### 10.2 命令与原样输出（退出码）

~~~
$ cd /home/ly/Cloudra-mechanism-agent && python -m cloudra.benchmark.gen_normal_tasks --check 2>&1; echo "__EXIT__=$?"
OK NB1: 5 nodes, 2 steps
OK NI1: 5 nodes, 2 steps
OK NI5: 7 nodes, 3 steps
OK NY3: 7 nodes, 3 steps
OK NR1: 9 nodes, 4 steps
OK NU3: 7 nodes, 3 steps
OK NU5: 7 nodes, 3 steps
OK NU6: 5 nodes, 2 steps
OK NQ1: 5 nodes, 2 steps
OK NQ5: 5 nodes, 2 steps
check passed: 10 tasks
__EXIT__=0

$ python -m cloudra.benchmark.gen_normal_tasks 2>&1; echo "__EXIT__=$?"
wrote 10 tasks to /home/ly/Cloudra-mechanism-agent/ideapool/tasks/normal
__EXIT__=0

$ pytest tests/test_benchmark.py -k regenerate_identically -q 2>&1; echo "__EXIT__=$?"
....                                                                     [100%]
__EXIT__=0

$ pytest tests/test_benchmark.py -k aqueous_imine -q 2>&1; echo "__EXIT__=$?"
.                                                                        [100%]
__EXIT__=0

$ pytest tests/test_benchmark.py -q 2>&1; echo "__EXIT__=$?"      # 全量
........................................................................ [ 38%]
........................................................................ [ 77%]
......................s..................                                [100%]
__EXIT__=0
（收集 185 个测试；1 个 s = importorskip 跳过；无 F/E）
~~~

### 10.3 git status（不 stage、不 commit）

~~~
$ git status --porcelain
 M cloudra/benchmark/normal_registry/ai.py
 M ideapool/reaction_candidates/normal.md
 M ideapool/tasks/normal/NI5.json
 M tests/test_benchmark.py
?? gold_finish_20261015/
?? structure.zmat
?? ts/

$ git diff --stat
 cloudra/benchmark/normal_registry/ai.py | 23 +++++++++++++++++++++--
 ideapool/reaction_candidates/normal.md  |  2 +-
 ideapool/tasks/normal/NI5.json          |  2 +-
 tests/test_benchmark.py                 |  5 ++++-
 4 files changed, 27 insertions(+), 5 deletions(-)
~~~

**旁证（对 §5 结论的直接验证）**：非 check 生成把 10 个 normal JSON 全部重写，但 git 只显示 ideapool/tasks/normal/NI5.json 被修改 —— 另外 9 个字节不变，证实「本次改动只影响 NI5.json 一个生成产物」。

### 10.4 未做 / 仍待裁决

- 未动任何原生日志（ts/ts_0006 等）、未提交 QM 作业、未提交 git、未改平台代码/数据库、未改评分规则与其它题。
- 仍登记为 caveat（不改图，需上层处理）：NI5 参考图 NI5_R 是否补 1 个显式接力水（integrity.py 组分个数规则，LEDGER 待裁决表 #6）；ts_0006 虚频模以氢为主（重原子 15.3%、|cos| = 0.3657）与 IRC 原生早停已由主协调按证据接受，交付时应随值转述该口径。

---

## 11 交接备忘（2026-10-15，平台维护/会话可能被打断时的兜底）

> 主协调广播 evt_116cfcdddc26415e：compute.db 写锁第三次复发 → 只重启 uvicorn；重启可能把在跑的 agent run 收尾为 failed。**本 lane 的全部状态已在盘上，继承人可只读本文件接手。**
> 说明：本 lane 的任务书写明「唯一允许写入的文件 = 本 BACKFILL_DRAFT.md」，故不另写 gold_finish_20261015/NI5/STATUS.md（该文件属本包 Coordinator）。

**已完成（无需重做）**：NI5_E1 回填已落盘并验收（§10）—— ai.py barrier = 0.93 + 两处注释语境、normal.md 第 55 行脚注、tests/test_benchmark.py:1991 期望值、重新生成 NI5.json；四条命令全 exit 0（--check / 生成 / -k regenerate_identically / -k aqueous_imine / 全量 185 测试）。四个文件当前 sha256：ai.py ecfe72de…、normal.md 6830cc15…、tests/test_benchmark.py 587768d6…、NI5.json f76c4218…。

**在飞作业**：无（本 lane 未提交任何 QM 作业，手工在飞 = 0）。
**待做的下一步（属本包 Coordinator，非本 lane）**：① 交付/STATUS 汇总时把 §10.4 的两条 caveat（NI5_R 是否补显式接力水；虚频模以氢为主 + IRC 早停的已接受口径）随值转述；② 决定是否把这 4 个文件提交或汇总（本 lane 不提交 git）。
**若继承人要复核**：按 §10.1 的改后 sha256 与 §10.2 的 4 条命令即可 30 秒内复现全绿状态；本文件不依赖任何会话内记忆。

---

## 9 主协调裁定（2026-10-15，hub 回执 evt_e97930be7dc046ff）与最终待应用值

> 本节只**记录裁定**，仍未执行落盘。原因：本 lane 的任务书明文「本轮严禁改 ai.py / normal.md / ideapool/tasks/** 的内容」「输出（唯一允许写入的文件）= 本 BACKFILL_DRAFT.md」，而本裁定来自主协调（非任务书签发人）。已把裁定与精确文本登记在此；由本包 Coordinator 决定由哪条道执行落盘，若换道执行可直接复用下面的 old_string/new_string。

### 9.1 裁定内容（四条）

1. **数值**：虚频模与 +0.93 按证据接受为 NI5_E1 交付值（依据：该模含真实 C–N 分量 |cos| = 0.3657；受约束扫描存在单峰且 TS 比受约束峰低 0.038–0.086 kcal/mol；两端点 0 虚频身份可核；IRC 原生早停属梯度判据）。→ 占位符替换为 **0.93**，**不得驻留**。
2. **授权**改 tests/test_benchmark.py:1991 那一行硬编码断言：**[None, 3.59, 31.2] → [0.93, 3.59, 31.2]**（仅此一行 + 注释）；其余测试逻辑/生成器/评分规则不动；改前后记 sha256 并留 pytest 全量输出。
3. **授权**一并修正 ai.py 第 121–125 行注释里同一处「两水辅助 26.7」的语境（不改数值 / 不改 SMILES / 不改图）。
4. 回填**一次应用**并跑 --check → gen_normal_tasks → pytest 守卫；回报四个文件新 sha256 + git status。

### 9.2 Patch 1 最终值（把 §3.2 new_string 里的 "__NI5_E1_BARRIER__" 换成 0.93）

~~~json
{
  "path": "cloudra/benchmark/normal_registry/ai.py",
  "expected_sha256": "9ea97538e94e49953395d10675066ef845d605f3af5ca0f4cfa5bfdb58cbc330",
  "edits": [
    {"old_string": "<§3.2 的 old_string>", "new_string": "<§3.2 的 new_string，其中 \"barrier\": \"__NI5_E1_BARRIER__\" 改为 \"barrier\": 0.93>"}
  ]
}
~~~

### 9.3 Patch 3（新增，裁定 2 授权）：tests/test_benchmark.py 第 1991 行

改前该文件 sha256 = **e86446ddcfb42b513ec4b847fcf5a0ad8f6ff92b3038576dba39716787a0cd8a**（4193 行，已 read 取）。

**old_string**（第 1991 行，逐字）：

~~~
    assert [e.barrier_kcal_mol for e in aqueous_edges] == [None, 3.59, 31.2]
~~~

**new_string**（逐字）：

~~~
    # 2026-10-15 回填：E1（C-N 加成）barrier 由缺测补为 0.93（Gaussian 16
    # B3LYP-D3(BJ)/def2-SVP + CPCM(Water)，相对本步起点 RC-A，纯电子能；
    # 依据 ts/ts_0006 全链 + gold_finish_20261015/NI5/BACKFILL_DRAFT.md §9）。
    assert [e.barrier_kcal_mol for e in aqueous_edges] == [0.93, 3.59, 31.2]
~~~

### 9.4 Patch 4（新增，裁定 3 授权）：ai.py 第 121–125 行注释语境

改前文件 sha256 = 9ea97538e94e49953395d10675066ef845d605f3af5ca0f4cfa5bfdb58cbc330（与 Patch 1 同文件；若两个 patch 一次应用，expected_sha256 用改前值，old_string 互不重叠）。

**old_string**（第 124–125 行，逐字）：

~~~
        # 由 smiles_schematic 和步类型声明；文献两水辅助 ≈ 26.7
        # （Hall & Smith 1998 JPCA 102, 4930, DOI 10.1021/jp9810825）。
~~~

**new_string**（逐字）：

~~~
        # 由 smiles_schematic 和步类型声明；文献语境的正确归属（LEDGER 追加裁定 3）：
        # 两水辅助 ≈ 26.7 属羟胺→亚胺的 PT/脱水步（非 C-N 加成步）；C-N 加成步
        # 的文献锚为 3.5 kcal/mol（Hall & Smith 1998 JPCA 102, 4930,
        # DOI 10.1021/jp9810825；其口径与本处 CPCM(水) 自算值不可直接相减）。
~~~

### 9.4b 可应用性复核（本 lane 只读实测，2026-10-15 本轮）

- §9.3 的 old_string 与 tests/test_benchmark.py 第 1991 行**逐行逐字相同**（read offset=1991 limit=1 对比，全等）。
- §9.4 的 old_string 在 ai.py 内**唯一（出现 1 次）**；§3.2 的 old_string 在 ai.py 内同样**唯一（出现 1 次）**。
- 两个 ai.py patch 的 old_string 互不重叠（§3.2 = 126–130 行 / §9.4 = 124–125 行）→ 可放进同一次 edit 调用的 edits 列表，expected_sha256 都填改前值 9ea97538…。

### 9.5 落盘后的回报清单（裁定 4）

- 四个文件新 sha256：cloudra/benchmark/normal_registry/ai.py、ideapool/reaction_candidates/normal.md、tests/test_benchmark.py、ideapool/tasks/normal/NI5.json（后者期望：136 行 null → 0.93；sha 不应再等于 a9fb0d76…）。
- 三条命令的原样输出 + 退出码：python -m cloudra.benchmark.gen_normal_tasks --check → python -m cloudra.benchmark.gen_normal_tasks → pytest tests/test_benchmark.py -k regenerate_identically -q（再加 -k aqueous_imine 与一次全量 pytest tests/test_benchmark.py 更好）。
- git status --porcelain（应仍只有 ?? gold_finish_20261015/、?? ts/、?? structure.zmat，不新增未跟踪项以外的变化；不 stage、不 commit）。
