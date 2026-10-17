# HI1_E3 · ts_prepare 声明草稿与绑定序/验收判据（lane2, 2026-10-15）

> 本文件是"等 job 925 → I2 极小值"期间的非 QM 准备产物；**不含任何计算结论**。
> 方法口径（全包统一，不得改）：Gaussian 16 `/home/ly/g16/g16`，`B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight + SCRF=(CPCM,Solvent=DMSO)`，q0/m1。

## 1 ts_prepare 反应声明（待 I2 极小值就绪后提交）

| 字段 | 值 | 来源 |
|---|---|---|
| reactant_smiles | `CC(C[C@H]([O-])c1ccccc1)=[N+]1CCC[C@H]1C(=O)O.O` | 题源 HI1_I2（10-14 纠正后，(S)/(S)） |
| product_smiles | `CC(=O)C[C@H](O)c1ccccc1.O=C(O)[C@@H]1CCCN1` | 题源 HI1_P（(S)-aldol + (S)-脯氨酸） |
| charge / multiplicity | 0 / 1 | 题面 |
| atom_map | `E3/prep/I2_P_atom_map.json` → `product_atom_map`（product 坐标序，值为 reactant 1-based 序，覆盖 41 个原子各一次） | 手工推导 + 本文件 §2 逐原子核对 |
| reaction_center | `[[2,4],[2,25],[25,26],[25,27],[4,26],[28,27]]`（reactant 1-based 工作序） | E3/STATUS §C.2 |
| conformers.reactant | I2 极小值 xyz（job 925 末端 → 无约束 Opt+Freq 产物） | S1 |
| conformers.product | `E3/prep/structure_build_P/assembly/complex_candidate_000.xyz`（RDKit 实测 2 分片、aldol C=S、Cα=S，见 §4） | 本道核验 |
| guess | `E3/prep/ts_guess_*/…_ts_candidate.xyz`（ts_guess interpolate/scan 产物）+ provenance | S2 |
| calculations.std | engine=gaussian, method=B3LYP, basis_set=def2SVP, keywords=`EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=DMSO)` | BRIEF §3 |
| execution | 8 cpus / 10240 MB（本包同刻手工 ≤2；手工一律 priority 0） | 调度政策 |

## 2 绑定序换算表（map 号 ↔ 本批工作原子序，1-based；I2 与 P 共用构件序）

| 工作序(I2) | 元素 | map | 角色 | E3 动作 |
|---|---|---|---|---|
| 1 | C | 3 | 烯胺端 CH2 | 无（连接 C2–C29 的桥） |
| 2 | C | 2 | 亚胺/iminium C | 断 2–4(N20)；成 2–25(水 O4) |
| 3 | C | 1 | CH3 | 无 |
| 4 | N | 20 | 脯氨酸 N | 断 2–4；成 4–26(H21) |
| 5,6,7 | C | 17,18,19 | 吡咯烷 CH2 | 无 |
| 8 | C | 16 | 脯氨酸 Cα（**目标 S**） | 无（身份核验点） |
| 9,10,11,24 | C,O,O,H | 14,13,15,(H) | 羧基 | 无 |
| 25 | O | 4 | 水 O（最终成产物酮 O） | 成 2–25；断 25–26、25–27 |
| 26 | H | 21 | 水 H（约定 → N20） | 断 25–26；成 4–26 |
| 27 | H | 22 | 水 H（约定 → 醇盐 O5） | 断 25–27；成 28–27 |
| 28 | O | 5 | 醇盐 O（产物 aldol OH O） | 成 28–27 |
| 29 | C | 6 | aldol C（**目标 S**） | 无（身份核验点） |
| 30–35 | C | 7–12 | 苯基 | 无 |
| 36 | H | — | aldol C–H | 无 |

watch pairs（1-based 工作序，与 §1 reaction_center 同）：

| pair | 语义 | 声明动作 |
|---|---|---|
| (2, 4) | C2–N20 | break |
| (2, 25) | C2–O4(水 O) | form |
| (25, 26) | O4–H21 | break |
| (25, 27) | O4–H22 | break |
| (4, 26) | N20–H21 | form |
| (28, 27) | O5(醇盐 O)–H22 | form |

> 注：水两个 H 化学等价；26/27 的 map 分工是记账约定（E3 声明只要求"一个 H→N20、另一个 H→O5"）。实测若为相反的物理 H 去向，按实测报告并说明标号可自洽互换。

## 3 验收判据（BRIEF §4 六项 → 本道判据）

1. **TS**：恰好 1 个虚频，且该虚频模以 §2 六个 watch pair 为主（`log_parser` 的 `imaginary_modes.watch_pair_fraction`）。
2. **IRC 双向**真实到达 I2 与 P（方向区间证据；不强求跑满 native 上限）→ 由 `ts_prepare` 的 verification.irc + 两端点 Opt+Freq 的身份核验确立"哪一侧 = I2、哪一侧 = P"。
3. **两端点 Opt+Freq = 0 虚频**，且实测：原子 8（map16）= **S**、原子 29（map6）= **S**、原子 4（N20）上有 H、原子 28（O5）上有 H；分片/物种身份正确（I2 侧 = iminium-alkoxide + 显式水；P 侧 = aldol + 脯氨酸）。
4. **能垒** ΔE‡ = E(TS) − E(I2 极小值)（纯电子能、同一批 Gaussian 16 日志内部相减）。
5. **原生日志不改写** + 绝对路径 + sha256 + 能量取自原始行。
6. 回填由包 Coordinator 执行（本道不改 hi.py / HI1.json / hard.md）。

### 3.1 I2 极小值判据（本道实测口径，已向主协调报备）
- I2 = `CC(C[C@H]([O-])c1ccccc1)=[N+]1CCC[C@H]1C(=O)O.O` → 化学上 **2 分片**（iminium-alkoxide 两性离子 + 显式水）；N20 为 iminium（3 个碳邻居、无 H）、O28 为醇盐（无 H）。
- 判据：Normal termination；Opt 收敛；**0 虚频**；q0/m1；RDKit 3D 实测原子 8 = S、原子 29 = S；各质子实测位置（预期 H24 在羧基 O11、H26/H27 在 O25）；能量取原始 `SCF Done` 行。
- （转达文本里"I2 = 3 分片 / H 在 N20 与 O5 上"两条经复核属 I1 预复合物与 P 产物的判据，见 hub 帖 evt_80e1550783bb43e1；按实测报告。）

## 4 已完成的非 QM 身份核验（可复核）

| 结构 | 文件绝对路径 | sha256 | 实测 |
|---|---|---|---|
| P 种子 | `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/prep/structure_build_P/assembly/complex_candidate_000.xyz` | `06161a1411edf1e1402620ee13ca448c14d2ac167846c10f1e56bf8ec175078a` | 41 原子、charge 0、2 分片；aldol C(idx5)=**S**、脯氨酸 Cα(idx28)=**S**；aldol O–H 在；脯氨酸 N–H 在；羧基完整 |
| I2 前体预复合物 | `…/prep/structure_build_I1S/assembly/complex_candidate_000.xyz` | — | 41 原子、3 分片（sha256 `0d308bd3fdd04afe2c212dee0cc614c9a5697236f50a60e130f494a4299ee9f3`）；脯氨酸 Cα(idx8)=**S**；C1···C29 = 4.675 Å |
| 映射坑复现 | — | — | `reaction_mapping`（两 SMILES + P 具体结构）返回 unique 但化学错的图映射，binding_status=inconclusive → 不采用 |

## 5 槽位与流程（调度政策 2026-10-15）

- 手工配额：`priority 0`；本包同刻手工作业 ≤2，且**在 924/925/928 全终态前不提交新手工**（925 为 I2 几何准备；928 为 ts_prepare 自动作业、无取消入口）。
- 流程：S1 I2 极小值 Opt+Freq（8c/8192MB，`E3/runs/I2_optfreq/`）→ S2 ts_guess interpolate（非 QM；不合格则 scan_prepare 或 xtb_path）→ S3 ts_prepare 全链（8c/10240MB）→ S4 验收链 → S5 失败时证伪记录 + 拆步裁决问题。
