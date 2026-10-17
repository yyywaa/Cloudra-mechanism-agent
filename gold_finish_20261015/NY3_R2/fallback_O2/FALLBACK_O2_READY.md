# FALLBACK O2 READY（只落盘、未提交）

生成：2026-10-17 14:1x CST，会话 as_6fdd1a4300b74a9f（small_mol）
目录：`gold_finish_20261015/NY3_R2/fallback_O2/`　→ **本目录内没有任何作业被提交**（`submit_compute_job` 未调用，job 账本里没有本目录的输入）。

## 0. 体系与级别
- 反应：**DMDO + 乙烯 协同氧转移**：`CC1(C)OO1.C=C >> CC(C)=O.C1CO1`（二甲基二氧杂环丙烷 + 乙烯 → 丙酮 + 环氧乙烷）
- **charge 0 / mult 1**；C5H10O2；**17 原子**（DMDO C3H6O2 = 11 + C2H4 = 6），7 个重原子。
- route（逐字，与主任务一致）：`B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=Water)`（**def2SVP 无连字符**）；8 核 / 10000 MB / chk 为绝对路径。

## 1. 文件清单（sha256 | 行数）
| 文件 | sha256 | 行数 | 用途 |
| --- | --- | --- | --- |
| `o2_seed.xyz` | `d7f812f89274c1ffc3a5deb1f0501bfb35a04d1e46b9bc0ea6ae18895675d4c4` | 19 | 复合物种子（17 原子 + 注释行 + 计数行） |
| `o2_optfreq.gjf` | `8e31a124124f8142584b3bc863618932a169672cd0119df249ad6afd8aef9151` | 28 | **受约束** Opt+Freq（O4–C1 冻结 2.800 Å） |
| `o2_optfreq_free.gjf` | `ed08db95604079ed7497f3bfb993c592f857381a51913652c3b4df347c108069` | 26 | 无约束 Opt+Freq（对照，可能撞平坐标） |
| `o2_scan.gjf` | `0e99d7b2743494ed0b244bc0a6b40fd5140e7ee79304eeade162bbae2adcc28b` | 28 | 受约束弛豫扫描 O4–C1 2.80→1.90 Å |
| `o2_scan_2d.gjf` | `f98aed823a28221f1395b5d77cb7b23bac511c92ae0145dca3e395ac72594f8b` | 30 | **2D 网格扫描**（O4–C1 + O4–C2 各 2.80→1.90，10×10 点，见 §7） |
| `build/build_o2.py` | `0df9b69913fdea877ddcd92589ac7f0370e8d9d4c3f03e81aacb008d285fdeda` | 101 | 组装脚本（可复现种子） |

三个 `.gjf` 的电荷行均为 **`0 1`**（已核对，不是默认误写的别的电荷）。

## 2. 原子序（1-based，元素序列表）
| # | 元素 | 归属 | # | 元素 | 归属 |
| --- | --- | --- | --- | --- | --- |
| 1 | C | 乙烯 C_a | 10 | H | 乙烯（C2） |
| 2 | C | 乙烯 C_b | 11 | H | 乙烯（C2） |
| 3 | C | DMDO 环碳 C3 | 12 | H | 甲基 C6 |
| 4 | **O** | **过氧 O_a（转移 O，进攻原子）** | 13 | H | 甲基 C6 |
| 5 | O | 过氧 O_b（→ 丙酮 C=O） | 14 | H | 甲基 C6 |
| 6 | C | 甲基 C6 | 15 | H | 甲基 C7 |
| 7 | C | 甲基 C7 | 16 | H | 甲基 C7 |
| 8 | H | 乙烯（C1） | 17 | H | 甲基 C7 |
| 9 | H | 乙烯（C1） | | | |

反应中心（本预筛只扫一根键）：**过氧 O4 → 乙烯 C1**；耦合键：O4–C2（另一侧成环）、O4–O5 与 C3–O4 断裂、C3=O5 生成。

## 3. 关键几何实测（`internal_coordinates(analyze, charge=0)`）
- 组成/拓扑：**C5H10O2，17 原子，16 键，2 片段，总电荷 0**；三员环 **C3–O4–O5**；**0 个 bond anomaly**。
- `C1=C2 = 1.336 Å`（要求 ≈1.33 ✓）
- `O4–O5 = 1.452 Å`（要求 ≈1.47 ✓，perceived ref 1.480）
- `C3–O4 = C3–O5 = 1.426 Å`；`C3–C6 = C3–C7 = 1.483 Å`
- **`O4···C1 = 2.800 Å`、`O4···C2 = 2.800 Å`**（两 C 等距 ⇒ 转移 O 位于 C=C 中垂面上，即 spiro 取向；要求 2.6–3.0 ✓）
- `∠C1–O4–C2 = 27.6°`（2.80 Å 处的正常取值；随扫描收紧到 1.9 Å 会升到 ~41°）
- `O5···C1 = 3.953 Å`、`O5···C2 = 3.508 Å`（丙酮侧 O 不参与进攻 ✓）
- 非键重叠检查：除两根**有意**的 O4···C 进攻接触（2.800 Å）外，最短乙烯–DMDO 跨片段接触为 **H9···O4 = 2.984 Å**、H11···O4 = 2.984 Å、H8/H10···O4 = 3.260 Å ⇒ **无 <2.0 Å 非键重叠**。
- 3 个 angle anomaly（C3–O4–O5 = C3–O5–O4 = 59.4°、O4–C3–O5 = 61.2°，相对四面体参考 −48~−50°）是**二氧杂环丙烷三员环固有张力**，非建模错误。
- 组分几何来源：`smiles_to_mol(generate_3d=True)`（RDKit + MMFF94），`build/art_dmdo/prepared.xyz`、`build/art_ethene/prepared.xyz`。

## 4. 摆放方法（可复现）
1. 取 DMDO 环碳 C3 与两条过氧 O 的键矢；定义进攻轴 `u = unit(O4 − C3)`（从环碳穿过转移 O 指向环外，使乙烯落在环外、不与甲基重叠）。
2. 令乙烯 C=C 中点 `M = O4 + L·u`，`L = sqrt(2.80² − (1.336/2)²) = 2.719 Å`；C=C 轴 `w ⊥ u`（保证两 C 等距 = spiro），再加绕 `w` 的乙烯自转 χ。
3. (ψ, χ) 网格搜索（ψ 每 3°、χ 每 10°，共 120×36 = 4320 个取向），评分 = 与 DMDO 的非键距离罚（H···H <1.95、其他 <2.45 罚）+ 乙烯 H 不得比 2.20 Å 更近 O4；取罚函数=0 的最小冲突解（ψ=0°, χ=0°，penalty=0）。

## 5. 输入构造方式与工具限制（照实留档）
- `o2_optfreq_free.gjf`：`qm_input_writer` 直接产出（`opt freq`）。
- `o2_optfreq.gjf` / `o2_scan.gjf`：同样先用 `qm_input_writer` 产出 base，再**用编辑工具**把 route 改成 `opt=(modredundant,maxcycle=100)` / `opt=(modredundant,maxstep=10)`，并在坐标块后（空行之后）追加 modredundant 段：
  - `o2_optfreq.gjf`：`B 4 1 S 1 0.0`（固定当前 2.800 Å，等价于受约束极小值）
  - `o2_scan.gjf`：`B 4 1 S 9 -0.100000`（2.800 → 1.900 Å，共 **10 点**）
  之所以手动补：`qm_input_writer` 会因为 end_setting 里出现 `B … S …` 把文件判成 relaxed_scan 而拒写。
> **更正（主协调实测口径，已复现）**：`ts_guess(mode="scan_prepare")` 是**可用**的，**必须给 `output_path`**（缺它才报 `Invalid tool arguments: arguments: invalid value`），且顶层**不收 `charge`/`multiplicity`/`nproc`/`mem`**（本会话先前误把它们当必填，导致同一报错）。按 `{mode,engine,input_path,scans,method,basis_set,keywords,output_path}` 这 8 个键可成功生成（本目录 `o2_scan_2d.gjf` 即由它直接生成，仅补了 % 行与绝对 chk）。
坐标块本身仍由工具生成，任何文件都未手打坐标。

## 6. RC 类型声明（会进终稿口径）
- **`o2_optfreq.gjf` 是「受约束复合物」**：O4–C1 用 `B 4 1 S 1 0.0` 冻结在 **2.800 Å**，只优化其余自由度；因此它的频率里**不应出现** O4···C1 软模（该自由度被投影掉），但**低频谱仍可能含 DMDO 环/甲基扭转与两片段相对取向**，判 0 虚频时要看模矢。
- `o2_optfreq_free.gjf` 是**无约束对照**：DMDO 与乙烯之间只有色散/偶极作用，很可能在极平坐标上摆动（Y2 同类陷阱），**只能作对照，不能默认当 RC**。
- 二者都**不是**「自由分子的无约束极小值」意义上的 RC；若要无约束 RC，需要先做片段相对取向的构象扫描再加约束释放。

## 7. 双坐标（2D）扫描输入 `o2_scan_2d.gjf`（只落盘，未提交）
- sha256 `f98aed823a28221f1395b5d77cb7b23bac511c92ae0145dca3e395ac72594f8b`｜**30 行**｜charge 行 `0 1` ✓｜`%nprocshared=8 / %mem=10000MB / %chk=<绝对>`
- route：`# opt=(modredundant,maxstep=10) B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=Water)`
- modredundant 段（坐标块之后）：
  ```
  B 4 1 S 9 -0.100000
  B 4 2 S 9 -0.100000
  ```
  ⇒ O4–C1 与 O4–C2 **同时**各自 2.800 → 1.900 Å（9 步、步长 −0.10）；Gaussian 对两条带步长的 B 坐标执行**二维独立网格**扫描 ⇒ **10 × 10 = 100 个受约束点**。
- 生成方式：`ts_guess(mode="scan_prepare", engine="gaussian", input_path=o2_seed.xyz, scans=[两条 bond], method/basis_set/keywords, output_path=…)` **直接产出**（工具写的 `%nprocshared=4`、相对 chk `scan.chk` 由我用编辑工具改成 8 核/10000 MB/绝对路径；坐标与 `B` 行未手打）。
- **成本提示**：100 个受约束弛豫点，按 Y2 同类 15–17 原子作业 ≈ 2–5 min/点 ⇒ **3–8 h**，远超 90 min 预筛预算；若只想知道「是否存在单峰」，建议先用 **0.15 Å / 6 步（7×7 = 49 点）** 的粗网格定位峰区，再局部加密。需要粗网格版本告诉我，我再落盘一份。
- 何时用它：**单坐标 `o2_scan.gjf` 若不成单峰（或峰位落在 O4 同时靠近两个 C 的区域）**，换 2D 网格看是否真有鞍点；2D 峰几何才是 `ts_prepare` 的好种子。
- 仍未提交：本目录全部输入文件（含 `o2_scan_2d.gjf`）**0 次提交**。

## 8. 后续使用注意
- 扫描只收紧一根 O4–C1 键时，另一根 O4–C2 会自然闭合（O4 处在中垂面上），若曲线不成单峰，正确做法是**双坐标（O4–C1 + O4–C2）联合/协同扫描**再看峰，而不是把单坐标曲线当 ΔE‡。
- 本文件的峰几何只是后续 `ts_prepare` 的种子；不得当作已验证过渡态。
- 未提交声明：本目录 4 个输入/种子 + 1 个脚本**均未提交**，NY3-R2 在飞配额未被我占用。
