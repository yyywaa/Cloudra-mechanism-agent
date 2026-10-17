# O2 product 端点 provenance（丙酮 + 环氧乙烷，**只落盘，待槽提交**）

生成：2026-10-17 **15:10:14 CST**（同轮 `date '+%Y-%m-%d %H:%M:%S %Z'` 实测输出为 `2026-10-17 15:10:14 CST`）
生成者：会话 **as_6fdd1a4300b74a9f**（small_mol），工具链 `smiles_to_mol(generate_3d=True)`（共享 builder：RDKit 嵌入 + MMFF94）→ `qm_input_writer`。**未手写坐标、未编造几何。**

## 1. 产物来源 SMILES（两片段都完整）
- 未映射：**丙酮 `CC(C)=O` + 环氧乙烷 `C1CO1`**（dot-joined 复合物 `CC(C)=O.C1CO1`）
- 映射（与 DESIGN_O2.md 一致）：`[CH3:1][C:2](=[O:5])[CH3:3].[CH2:6]1[O:4][CH2:7]1`
- 总电荷 **0**、多重度 **1**（C5H10O2，17 原子）

## 2. 写入 / 输出路径 + sha256
| 文件（绝对路径） | sha256 | 行数 |
| --- | --- | --- |
| `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NY3_R2/fallback_O2/build/art_prod/assembly/complex_candidate_000.xyz`（端点起点几何，17 原子） | `4bdc98e0137fbd51b1b0bf7fb513cc207b56711230d0c6505ec0a37a1a10c45a` | 19 |
| `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NY3_R2/fallback_O2/o2_product.mol`（带键级/形式电荷的 MOL） | `7b788f55cdbeb4f40cd169b5f6050c63437dbe91fee32c9b9f44ee5578409466` | 38 |
| `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NY3_R2/fallback_O2/build/art_prod/prepared_structure.json`（builder 记录） | `82692fb7c3e98f1ea6a244a513396f985feb5ff9f80e46ac589c13fd19b8a946` | — |
| `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NY3_R2/fallback_O2/o2_product_optfreq.gjf`（Opt+Freq 输入） | `6197876b95aba5ca45eec5829c0e2e0238e914c17bb92d1455512317eb06a845` | 26 |
| chk（运行时写入） | `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NY3_R2/fallback_O2/o2_product_optfreq.chk` | — |

## 3. 计算级别（与扫描/TS **完全一致**，逐字）
- route 首行：`#p opt freq B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=Water)`
- `%nproc=8`、`%mem=10240MB`、chk 绝对路径；电荷行 `0 1`
- **溶剂口径（项目级）**：NY3 全链 = **CPCM(Water)**；HI1 = CPCM(DMSO)。**不同题不同溶剂，禁止跨题混引数值/级别。**

## 4. 产物身份核对（`internal_coordinates(analyze, charge=0)`，非目测）
- C5H10O2，**17 原子 / 16 键 / 2 片段 / 总电荷 0**
- 三员环 **C11–C12–O13 = 环氧乙烷** ✓；C2=O4 羰基 + C1/C3 两个甲基 = **丙酮** ✓
- **0 个 bond anomaly**；3 个 angle anomaly 全是环张力（C12–C11–O13 = 58.4°、C11–C12–O13 = 58.4°、C11–O13–C12 = 63.1°，相对四面体 −46~−51°）⇒ 建模正确
- 关联的 `reaction_mapping.product` 指纹 = `fcd1b47431c97af674a2d627ab551a445b68ee9204404900bcec1c2c83fab272`，`product_identity = match`

## 5. 提交状态与门禁
- **当前状态：未提交**（`query_compute_queue` 15:10 实读 free cpus = **0**，running = 1049/1059/1061/1062）。按主协调口径：**只在 free cpus ≥ 8 时提交**，cpus=8 / memory_mb=10240 / priority=0，不抢槽、不 kill、不调优先级。
- 提交后本文件将补：job id、日志绝对路径 + sha256 + 行数、`Frequencies --` 组数（应 15 组 = 45 模）、`N imaginary frequencies` 行与行号、末判据 4 行行号、末 SCF 能量。
