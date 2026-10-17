# O2 分离反应物单体 Opt+Freq 备件 provenance（(c) 方案：以分离反应物为能垒基准）

生成：**2026-10-17 15:33:58 CST**（同轮 `date '+%H:%M:%S'` 实测 `15:33:58`）｜生成者：会话 **as_6fdd1a4300b74a9f**（small_mol）
链条：`smiles_to_mol(generate_3d=True)`（RDKit 嵌入 + MMFF94）→ `qm_input_writer`
**状态：只落盘，0 提交**（等主协调在主协调层最终裁定 (a)/(b)/(c)；本目录未调用 submit_compute_job）

## 1. 体系与级别
| 单体 | SMILES | 组成 | charge / mult |
| --- | --- | --- | --- |
| DMDO（二甲基二氧杂环丙烷） | `CC1(C)OO1` | C3H6O2，**11 原子** | **0 / 1** |
| 乙烯 | `C=C` | C2H4，**6 原子** | **0 / 1** |

- route（两份逐字相同）：`#p opt freq B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=Water)`（**def2SVP 无连字符**；**CPCM(Water)**，与 TS/扫描同级）
- `%nproc=8`、`%mem=10240MB`、chk 绝对路径、电荷行 **`0 1`**（已核：均在文件第 8 行）、文件以空行结尾（Gaussian 正常接受）
- 提交参数（届时）：`cpus=8, memory_mb=10240, priority=0`

## 2. 文件 / 路径 / sha256 / 行数
| 文件（绝对路径） | sha256 | 行数 |
| --- | --- | --- |
| `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NY3_R2/fallback_O2/monomers/dmdo_optfreq.gjf` | `4d689d467118f2c96dda2a7f5d0b851a1ca1cddc855474cbdb4564fff55007cd` | 20 |
| `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NY3_R2/fallback_O2/monomers/ethene_optfreq.gjf` | `12eb10f47316a9c235a90115fc0bd183e1e38a7ddecccebb980267c3b3a96633` | 15 |
| `…/monomers/art_dmdo/prepared.xyz`（DMDO 起点几何） | `27cecb8d4da4ef01e54c11bd583b38309b35dae247e93104855d31fd2a3dcfa9` | — |
| `…/monomers/art_ethene/prepared.xyz`（C2H4 起点几何） | `70a02c07220179690d715f075e18dd1c3f18c62a184277e501c89e87fd7acaad` | — |
| `…/monomers/dmdo.mol` / `ethene.mol`（带键级的 MOL） | 与 prepared 同源（builder 输出） | — |

## 3. 用途（(c) 口径，待裁定后执行）
- 两份单体各自 Opt+Freq ⇒ 各须 **0 虚频**（DMDO 3N−6 = **27 模 = 9 组 `Frequencies --`**；C2H4 3N−6 = **12 模 = 4 组**）
- **ΔE‡ = E(TS) − [E(DMDO,min) + E(C2H4,min)]**（纯电子能，全部来自同级别 B3LYP/def2SVP + GD3BJ + UltraFine + SCF=Tight + CPCM(Water) 的原生 log；**同一"批次/级别"内相减，不跨级别、不与受约束复合物数值混用**）
- 若主协调最终改选 (a)「受约束复合物」，则本备件仍可作**分离极限对照**，但报告必须写明 (a) 基准点是**受约束点、非极小**。

## 4. 未提交声明
本目录两份 `.gjf`（及 `art_*` 下全部 builder 产物）**均未提交**；本会话在 NY3 槽位当前只有 ts_0018 流程产生的作业（job 1064 等，由 `ts_prepare` 自行提交），未手工提交任何作业。
