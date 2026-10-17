# NR1 第三边（E3 = I2→P）· 方案 C 准备清单（**未授权**；本文件不构成任何已提交作业）

状态：主协调 2026-10-17 裁定 **A（维持现状）**；C 登记为「可选增强项」，**本轮不授权**，仅当关键路径全部落定、槽位释放后由主协调授权。本文件只做一次性可执行准备，**未提交任何作业**。

## 1 假设与依据
- 假设：在本气相模型（Gaussian16 B3LYP/def2SVP + empiricaldispersion=gd3bj + scf=tight + int=ultrafine，q=+1/m=1，26 原子）下，I2→P 为「1,2-甲基迁移 + 去质子」协同单步。
- 依据（job 998 受约束剖面）：logs/E2b_scan_migration_C4C8.log（sha256 f78e4486391235001b1f3d02075e97383f1949d91e2fe207b7f4b32f2f63ba81）沿 r(C4-C8) 2.457→1.522 Å 只有一个内部极大（pt6，r=2.0674，**+3.77 kcal/mol vs I2**），峰后 12.10 kcal/mol 换谷并同时完成 C=O 成键（C7-O10 1.240）与 O10→O1 质子转移，末帧即 P（频哪醇酮 + H3O+ + H2O，-29.44 vs I2）。
- 口径（主协调）：+3.77 是**受约束扫描下界**（0.078 Å 网格未分辨极大 + pt6→pt7 换谷），**不是 ΔE‡**，既不支持也不否定独立鞍点；**不得**写成「IRC 已双向到达端点」。

## 2 端点 / guess 文件与 sha256（全部在 lane 内、未被改写）
| 角色 | 文件（相对 gold_finish_20261015/NR1/E2/） | sha256 | 关键几何（本道 I2 序） |
| --- | --- | --- | --- |
| reactant（I2 极小值） | structures/I2_opt_c000_r2.xyz（job 916，E=-463.981552572，0 虚频） | e89f464f0712f44ea7e5520d0052a5b9b8a2b8cde86e1bbcb0cfc0dd8e828eee（原生日志 logs/E2_I2_optfreq_c000_r2.log） | 3 片段；C4···O6 4.035；C4-C8 2.457、C7-C8 1.551、C7-O10 1.397 |
| reactant mol_path | structures/build_I2/assembly/complex_candidate_000.mol | 6d2ef839a3c743bce48b9d425fa9d5492956e92acec77a7c8c286328ebdcfeab（见 E2_PREP_PROVENANCE.md §2） | heavy_atom_binding = [1,4,7,8,9,10,11,12,13] |
| guess（唯一内部峰帧） | seeds/scan998_peak.xyz | 76a474e8605ebc0baf07fb056a1b4e0e5ad2b17e32c753d8b02c31ea03e4d62a | 23 键、3 片段；C4-C8 2.067、C7-C8 1.611、C4-C7 1.446、C7-O10 1.380、O10-H26 0.998 |
| product 候选 seed（末帧） | structures/judg_998_end.xyz | 8c21b97e08814f26db7ca4029bf5e76f595bb3173a4201fe0756f1e9b37f310d | 23 键、3 片段；C4-C8 1.522、C7-C8 2.458、C7-O10 1.240（C=O）、O10-H26 1.293（离去）、O1 收质子 |

## 3 需要先补的两端 0 虚频极小值（授权后按序提交：手工在飞 ≤2、priority 0、8c/10240MB）
1. **P 端点**（本批尚无）：用 smiles_to_mol(generate_3d=true, charge=1, multiplicity=1) 构建 [OH2+:1][H:11].[OH:6][H:2].[CH3:3][C:4]([CH3:5])([CH3:8])[C:7](=[O:10])[CH3:9]（= registry step4 的 out）→ 用 qm_input_writer（engine=gaussian、method=B3LYP、basis_set=def2SVP、keywords empiricaldispersion=gd3bj scf=tight int=ultrafine、task_type 用 [{opt: null}, {freq: null}] 形式、charge 1 / multiplicity 1、chk_name 用**裸文件名**、mem 10GB、nproc 8）→ submit_compute_job。验收：0 虚频、3 片段（pinacolone + H3O+ + H2O）、C7-O10 约 1.20-1.25 Å。
2. **交叉核对（可选）**：对 structures/judg_998_end.xyz 直接做同级别 Opt+Freq；与 1 的落点比较（同批纯电子能差 ≤0.02 kcal/mol 且键连表一致 ⇒ 同一极小值；容差判据同 E2_E23_VERDICT.md 开头）。
3. **第二步假设的反证（可选）**：构建 I3 = 质子化频哪醇酮 + 2H2O，SMILES [OH2:1].[OH:6][H:2].[CH3:3][C:4]([CH3:5])([CH3:8])[C:7](=[O+:10][H:11])[CH3:9]（= registry step3 的 out）→ Opt+Freq；若落到 P 或落到 992 型换水物种 ⇒ 两步（I2→I3→P）描述在本模型被证伪，直接回到协同单步声明。

## 4 ts_prepare 声明字段（一次性 grouped input，授权后执行）
- reaction：I2（映射 SMILES）→ P（映射 SMILES）的全原子映射（26 项，由 reaction_mapping 的 concrete binding 生成）+ reaction_center = 迁移键对（本道 I2 序 8-11 = 题面 map4-map8 的 C4-C8）；charge 1 / mult 1。
- calculations：单一 formal profile = engine gaussian / method B3LYP / basis_set def2SVP / keywords empiricaldispersion=gd3bj scf=tight int=ultrafine（气相，无 SCRF）。
- conformers.reactant = structures/I2_opt_c000_r2.xyz（mol_path = structures/build_I2/assembly/complex_candidate_000.mol，binding [1,4,7,8,9,10,11,12,13]）；conformers.product = P 的 xyz（授权后由 §3.1 得到，附其 build mol 与 binding）。
- guess.kind = provided，guess.xyz_path = seeds/scan998_peak.xyz（evidence_refs 必须指向**已存在**的文件路径）。
- verification：freq + irc + 两端 endpoint seed（同一 formal profile）。
- execution：{cpus: 8, memory_mb: 10240}。
- 主协调补充口径：授权后若再扫描，约束方向改用**断裂方向**（r(C7-C8) 增大；job 998 的 ts_guess 帧索引把它写作 C10-C11），以避开 pt6→pt7 的换谷歧义。

## 5 验收链（拿到数据后逐项判定）
1. ts_opt 收敛；2. 频率恰 1 虚频且该模以 C4-C8 迁移/断裂为主（附位移块 file:line 与重原子占比）；3. IRC 双向端点**或**替代连通性口径（受约束单峰 + 虚频模 ± 位移落点 + 两端点 0 虚频身份），**不得**写「IRC 已双向到达端点」；4. 两端 Opt+Freq 均 0 虚频且身份分别为 I2 与 P（键连表/片段数/质子归属）；5. ΔE‡ = E(TS) - E(I2 极小值)（同批纯电子能，禁止跨程序/跨批次混减）。

## 6 ETA（授权后、队列空闲时）
- P 端点 build + Opt+Freq：约 20-30 min（单作业）；ts_prepare 链（ts_opt + freq + IRC + 两端点）：约 1.5-3 h；合计 **2-4 h**。若同时跑 I3 反证：再 +20-30 min。

## 7 边界
- 本文件不构成科学结论；+3.77 仍是受约束扫描下界。本文件不提交作业、不改 registry/题面/tests/生成器、不复制坐标（只引用路径 + sha256）。