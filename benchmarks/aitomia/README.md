# Aitomia 原始 Benchmark 题目

本目录收录 Jinming Hu 等作者公开发布的 Aitomia Benchmark 第一张题表，共 47 题：27 道 Low、11 道 Medium、9 道 High。每题原报告运行 10 次。这些分类衡量原题要求的自主程度，不等同于 Cloudra 机理题的难度分级。

## 在 Cloudra 上运行

在仓库根目录使用已安装 Cloudra 依赖的 Python：

```bash
# 查看原题及坐标附件要求，不调用模型
python -m cloudra.benchmark.aitomia --list

# 准备全部题目，不调用模型：24题可准备，23题标记缺原始输入
python -m cloudra.benchmark.aitomia --data-dir benchmark_smoke_data/aitomia

# 真实运行一题；保留原题的气相 wB97X/Def2-SVP 方法要求
python -m cloudra.benchmark.aitomia --only MED.RXN.RXN5 --run --data-dir benchmark_smoke_data/aitomia

# 取得原始坐标后绑定附件；没有 --run 时仍只准备输入
python -m cloudra.benchmark.aitomia --only SP.PBE0 --input 'SP.PBE0=/absolute/path/official-h2.xyz'
```

`--only` 可用逗号选择多题；省略时选择全部47题。`--input TASK_ID=FILE.xyz` 可重复；原文件复制到该题目录后使用。默认只准备，显式 `--run` 才会调用模型和计算软件。默认输出根目录是 `aitomia_benchmark_data`，建议像示例一样显式选取独立目录。

每次调用建立新的运行目录，保存 `run.json`；每题有独立的 `case-NN` 目录，包含实际发送的 `request.json`、运行收据 `result.json`、最终回复 `answer.md`，以及 Agent 生成的原始计算输入和输出。整批事件与会话快照在 `runtime/runtime-v2.db`，计算账本也由该运行目录下的隔离配置寻址；不会把此次运行写入现有 Web 服务的数据目录，也不会保存更改到用户配置文件。

执行模式使用 Cloudra 现有 `standard` Agent 及计算调度，不要求交付机理图，不注入 CloudraBench 方法白名单。题目指定的科学方法和程序以原文为准。缺少指定软件时，最终回复和原始日志用于判断阻塞原因，不能把换方法的计算算作原题复现。

结果字段的含义：

| 字段 | 类型与取值 |
| --- | --- |
| `execution_status` | 字符串：`prepared`、`blocked_input`、`running`、`finished` 或 `error` |
| `scientific_status` | 字符串，始终先记为 `unreviewed`，等待独立科学审查 |
| `score` | `null`；没有自行建立评分标准 |
| `runtime` | 实际执行后记录项目编号、会话编号、Agent 终态及最终回复 |

`finished` 仅表示运行内核结束，不能视为计算科学通过。`--run` 存在缺输入或运行错误时退出码为1；即使退出码为0，也必须检查原始证据和原题方法要求。原作者报告的成功率和 tokens 仅作为来源元数据保留在 `run.json`，不加入发给 Agent 的题目。

## 文件与来源

- `benchmark.xlsx`：未经修改的官方工作簿，保留供逐格复核。
- [`catalog.json`](../../cloudra/benchmark/aitomia/catalog.json)：供安装包读取，仅从 `aitomia_benchmark` 工作表第 3–49 行导出的 47 个题目及来源元数据。
- 原始补充材料：[Figshare v1，10.6084/m9.figshare.31727860.v1](https://doi.org/10.6084/m9.figshare.31727860.v1)。
- [原始工作簿下载](https://ndownloader.figshare.com/files/62791333)。SHA-256：`400abc267cbc95d1ffa44dddb42c8ca840314e395a3548e128de19d049ab82e5`。
- [原始 SI PDF 下载](https://ndownloader.figshare.com/files/63093163)：381 页，主要包含回答与运行截图；未复制进本目录。
- 对应论文：Jinming Hu et al., *Aitomia: An Agentic Framework for AI-Driven Atomistic and Quantum Chemical Simulations*, J. Chem. Theory Comput. (2026), [10.1021/acs.jctc.6c00591](https://doi.org/10.1021/acs.jctc.6c00591)。

## 归属与许可

题表及补充材料归原作者所有，按 [Creative Commons Attribution 4.0 International（CC BY 4.0）](https://creativecommons.org/licenses/by/4.0/) 复用。请保留上述作者归属、来源 DOI 和许可链接。`catalog.json` 是工作簿的数据转写；原始 `query` 和 `notes` 逐字符保留，分类单元格向下继承。`task_id` 仅删除原单元格首尾空格，`source_task_id` 保留原值，题号内部空格不变。此许可不替代计算软件、模型权重或其他依赖各自的使用条件，也不表示原作者认可 Cloudra 的评测。

## 数据字段

顶层 `source` 记录标题、版本 DOI、网页、许可、下载地址、工作簿 SHA-256 和工作表名；`cases` 按原始行序排列。

| 字段 | 含义 |
| --- | --- |
| `task_id` / `source_task_id` | 可选择的题号 / 原单元格题号；后者保留尾空格 |
| `level` | 原表的 Low、Medium 或 High；继承 B 列分类 |
| `query` | D 列原始提问，保留方法、程序及路径占位 |
| `provided_xyz` | 依据 I 列说明判断原实验是否提供 XYZ；不表示本目录包含该附件 |
| `notes` / `source_row` | I 列原说明 / 原始 Excel 行号 |
| `reported_success_rate` / `reported_runs` | 原作者报告的成功率与运行次数；不是 Cloudra 实测结果 |
| `reported_tokens` / `source_type` | G、H 列原值；`seen/unseen` 指原作者开发时是否接触题目 |

## 输入是否齐备

**23 题原实验提供了 XYZ，但这个正式 Figshare 版本没有发布独立 XYZ 输入文件。** 工作簿自身没有嵌入坐标文件或外部输入下载链接。不能静默生成新坐标并声称重现这些原始输入。`OPT.AIQM1_GEOMETRIC`（第 9 行）虽然在提问中漏了 `[xyzfile]`，说明列仍明确写着提供 XYZ，因此 `provided_xyz` 保持 `true`。其他 22 道提供坐标题的提问保留 `[xyzfile]`。

**24 题原本不提供 XYZ**：Low 中的 `OPT.AIQM2_GAUSSIAN`、`UVVIS.SPC.OM2`、`UVVIS.SPC.TD-WB97XD`、`UVVIS.SPC.DIRCHECK`，以及全部 11 道 Medium 和 9 道 High。这些题按原意由 Agent 获取或生成分子结构，无需缺失的原始附件；实际能否执行仍取决于题目要求的计算后端是否已安装。

运行时只需将 `[working_dir]` 替换为本次运行的独立目录；取得官方坐标后，才能把 `[xyzfile]` 替换为对应文件。不要因本地缺少软件而改写原题的方法或指定程序。

### 18 题不强制 AIQM、OMNI 等特定模型

其中 4 题已经指定常规 DFT 方法：

- `UVVIS.SPC.TD-WB97XD`：乙烯 UV/vis，wB97XD/Def2SVP，明确使用 Gaussian。
- `MED.RXN.RXN3`：氨的质子亲和能，wB97X/Def2-SVP。
- `MED.RXN.RXN4`：乙烷原子化能，B3LYP/6-31G*。
- `MED.RXN.RXN5`：甲烷均裂为甲基自由基与氢自由基的反应能，wB97X/Def2-SVP。

另外 14 题未指定固定方法；导入时保留原题的选择空间，不新增统一方法：

- `MED.CONJ`
- `MED.TAUT`
- `MED.ΔGdeprot`
- `MED.AxPref.StereoElec`
- `MED. EWG`（题号中原有的内部空格保留）
- `HIGH.RXN.RXN7`
- `HIGH.RXN.RXN8`
- `HIGH.RXN.RXN9`
- `HIGH.RXN.RXN10`
- `HIGH.Gas.Vibrational`
- `HIGH.StericVsStereoelectronic`
- `HIGH.AminoSubstitution`
- `HIGH.FunctionalGroupEffect`
- `HIGH.CONF.HB-vs-nHB`

### 6 题不需 XYZ 附件，但要求特定模型

- `OPT.AIQM2_GAUSSIAN`
- `UVVIS.SPC.OM2`（包括 AIQM2 优化）
- `UVVIS.SPC.DIRCHECK`（OMNI-P2x）
- `MED.RXN.RXN1`（AIQM2）
- `MED.RXN.RXN2`（AIQM1）
- `MED.RXN.RXN6`（AIQM2）

这些方法的安装与许可应分别确认。Gaussian 在部分题目中只是优化或频率驱动程序，不能把底层 AIQM 方法替换为普通 DFT 后仍称原题运行。

## 参考证据与评分限制

导入包没有补写数值 Gold、参考结构、容差或科学评分规则。原题表只包含问题与原作者统计，没有逐题机器可用的人工参考数值、原生参考日志或自动评分程序。SI 的截图可辅助人工复核，不等同于完整参考计算产物。运行完成或工具成功不能据此自动标记科学通过；也不能把 Cloudra 的原有综合分直接与作者成功率比较。

第二张工作表 `benchmark_RUN` 不用于构造题目：它包含只在运行表出现的 `SP.INDEPENDENT`、重复的 `THERMOCHEM.ANI1CCX_GAUSSIAN`，并缺少第一表中的 `THERMOCHEM.M062X_GAUSSIAN`、`UVVIS.SPC.DIRCHECK`。SI 部分示例也与题表描述不同；例如 `HIGH.FunctionalGroupEffect` 在题表中比较 diphenylethene/azobenzene，而 SI 示例 S 比较 formaldehyde/溴代物。本目录以明确版本的第一张题表为准，不用截图覆盖原问题或填充参考答案。
