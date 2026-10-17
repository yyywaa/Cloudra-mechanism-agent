# 证据 · job 924 = (S)-HI1_I1 极小值（lane3 能垒参考态 · 2026-10-15）

复核人：lane3 接续会话 `as_bc146127755a404d`（本机亲验，非转述）。
用途：两条通道（HI1_E2 / HI1_EM1）的能垒口径 `ΔE‡ = E(TS) − E(job 924)` 的**唯一**参考态。

## 1 文件与哈希（原生日志不改写）

| 文件 | 绝对路径 | sha256 |
|---|---|---|
| 输入 | `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2EM1/runs/I1_optfreq/I1_S_optfreq.gjf` | `8b843b95bb55f46921f9aa23f9c172d906261b881e433db4c419605913cef0a9` |
| 原生日志 | `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2EM1/runs/I1_optfreq/I1_S_optfreq.log` | `6ecf06238ee6e1e976ba30eb15faf655f3ebe5a0126ed37d0dfe9b687dea6a87` |
| 末帧几何（本道导出，**仅坐标 artefact**，不作为收敛/频率证据） | `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2EM1/evidence/I1_S_optfreq_last.xyz` | `d74675dbaef346363f58c7f5fa435707f5ef62587d976012428c7f3f32c8e1c5` |

日志总行数 27032（`wc -l`）。

## 2 逐项数值（绝对路径 + 行号）

命令（在 `gold_finish_20261015/HI1/E2EM1/` 下）：

    grep -n "Normal termination" runs/I1_optfreq/I1_S_optfreq.log
    grep -n "SCF Done" runs/I1_optfreq/I1_S_optfreq.log | tail -2
    grep -n "Optimization completed" runs/I1_optfreq/I1_S_optfreq.log
    grep -c "^ Frequencies" runs/I1_optfreq/I1_S_optfreq.log

| 项 | 值 | 行号 |
|---|---|---|
| 电荷/自旋 | `Charge =  0 Multiplicity = 1` | 119（第一段）、21496（频率段） |
| opt 段 Normal termination | `Normal termination of Gaussian 16 at Thu Oct 15 19:01:11 2026.` | **21468** |
| 总 Normal termination | `Normal termination of Gaussian 16 at Thu Oct 15 19:11:18 2026.` | **27032** |
| 优化收敛 | `Optimization completed.` | 20393 |
| 原始能量行 | `SCF Done:  E(RB3LYP) =  -939.308218263     A.U. after    6 cycles` | **20025** |
| 原始能量行（频率段重算，同值） | `SCF Done:  E(RB3LYP) =  -939.308218263     A.U. after    1 cycles` | **22238** |
| Frequencies 块数 | 39（= 117 模） | 首块 22931，末块 24755 |
| 最低实频 | 24.6404 cm-1 | 22931 |
| 最高频 | 3710.4654 cm-1 | 24755 |
| 虚频 | **0**（`log_parser` 返回 imaginary_frequencies = []） | — |

`log_parser(log_path=..., properties=["energy","frequencies","convergence","job_type","thermochemistry"])` 原始返回（节选）：
`{"scf":-939.308218263,"nfreq":117,"imag":[],"minfreq":24.6404,"normal":true,"optconv":true,"types":["freq","opt"],"engine":"gaussian","zpe":0.341676,"gibbs":-939.017818}`

**E(job 924) = -939.308218263 Eh（纯电子能，原始行 20025 / 22238 同值）。**

## 3 身份核验（Cα 手性）

命令（工作根目录）：

    cd /home/ly/Cloudra-mechanism-agent && python3 gold_finish_20261015/HI1/E2EM1/build/check_cip_lane3.py x \
      gold_finish_20261015/HI1/E2EM1/evidence/I1_S_optfreq_last.xyz

原始输出（react 模式 = 声明的烯胺+水+苯甲醛拓扑）：

    I1_S_optfreq_last.xyz  react  [(7, 'S')] {'d(C3-C6)': 4.316, 'd(C2-N20)': 1.375, 'd(C28-O29)': 1.226}

RDKit 0-based idx 7 = 1-based 原子 8 = 脯氨酸 Cα（map16）→ **S**。几何上 C3···C6 = 4.316 Å（加成前），
C2–N20 = 1.375 Å、C28=O29 = 1.226 Å。

> 方法学说明（本道发现并记录）：`build/check_cip_lane3.py` 与 `build/dbg_cip_adduct.py` 的键表
> **缺少苯环的 Kekulé 双键**，直接据此写 MOL 会得到 C15H27NO4 的伪饱和环（多 6 个 H）。对 Cα 的 3D CIP 判定无影响
> （Cα 为 sp3、与苯环无关），故本表结论不变；但任何**构建 MOL / 供工作流使用的结构文件**必须用修好的键表：
> `build/make_mol_and_binding_lane3.py`（sha256 `d0d86755f264ba627401ab12968900067e9dece84fb0bdc855b626fbcca315ed`，苯环双键 (30,31),(32,33),(34,35)），
> 生成的 `build/I1_S_start_bonded.mol` 分子式 `C15H21NO4`、40 键、3 分片，与题源一致。

## 4 结论

job 924 通过 lane3 验收清单第 1 项：**0 虚频 / opt 收敛 / 两条 Normal termination / Cα = S / q0 m1**，
故 `E(job 924) = -939.308218263 Eh` 作为两条通道 ΔE‡ 的参考态固定使用。
不得改用 job 907（物种不同：脯氨酸+丙酮+苯甲醛），不得用工作流自身 reactant 端点替换。
