# HI1 E2EM1 · lane3 · 提交方案（解禁后照此执行）

## 0 方法块（两通道四阶段逐字相同，engine 差异见 STATUS.md §5）
```json
{"engine":"gaussian","method":"B3LYP","basis_set":"def2SVP",
 "keywords":"EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=DMSO)",
 "end_setting":""}
```
注意：**keywords 只放方法层**（色散/积分格/SCF/溶剂）；opt/freq/irc 由 ts 工作流自动加，声明侧重复会 l101 硬失败。end_setting 必须为空串。

## 1 通道 A：HI1_E2（major_face → HI1_I2，map6=S）
```json
{"reaction":{"reactant_smiles":"C=C(C)N1CCC[C@H]1C(=O)O.O.O=Cc1ccccc1",
             "product_smiles":"CC(C[C@H]([O-])c1ccccc1)=[N+]1CCC[C@H]1C(=O)O.O",
             "charge":0,"multiplicity":1},
 "calculations":{"m":{"engine":"gaussian","method":"B3LYP","basis_set":"def2SVP",
    "keywords":"EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=DMSO)","end_setting":""}},
 "conformers":{"reactant":{"kind":"file","/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/build/I1_S_start.xyz",
              "mol_path":"/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2EM1/build/I1_S_start_ref.mol"}},
 "guess":{"kind":"provided","xyz_path":"/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2EM1/build/TS_guess_E2_j58f7.xyz","evidence_refs":["/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2EM1/build/TS_SEED_PROVENANCE_E2.md"]},
 "ts_optimization":{"ref":"m"},"verification":{"frequency":{"ref":"m"},"irc":{"ref":"m"},
    "reactant_endpoint":{"optimization":{"ref":"m"},"frequency":{"ref":"m"}},
    "product_endpoint":{"optimization":{"ref":"m"},"frequency":{"ref":"m"}}},
 "execution":{"cpus":8,"memory_mb":8192}}
```

## 2 通道 B：HI1_EM1（minor_face → HI1_M1，map6=R）
同上，仅两处不同：
- `product_smiles` = `"CC(C[C@@H]([O-])c1ccccc1)=[N+]1CCC[C@H]1C(=O)O.O"`
- `conformers.reactant` = `build/I1_S_from_job59.xyz`（mol_path = `build/I1_S_from_job59.mol`），`guess.xyz_path` = `build/TS_guess_EM1_j59f9.xyz`，`guess.evidence_refs` = `["<abs>/gold_finish_20261015/HI1/E2EM1/build/TS_SEED_PROVENANCE_EM1.md"]`

## 2b 素材绝对路径（已落盘，sha256 见 STATUS.md）
- 起点 A：(S) I1 起点 = gold_finish_20261015/HI1/E1/build/I1_S_start.xyz（sha c9d59aea…，= job_51 rc_clean_np8.xyz 的 z 镜像，maxdev=0，Cα=S）；本目录另存 mol 序参照 build/I1_S_start_ref.mol
- 起点 B：gold_finish_20261015/HI1/E2EM1/build/I1_S_from_job59.xyz（sha 22f730d2…，= job_59 scan_minor_clean.001.xyz 的 z 镜像，Cα=S）
- TS 种子：build/TS_guess_E2_j58f{6,7,8}.xyz（map6 预测 S）、build/TS_guess_EM1_j59f{8,9,10}.xyz（map6 预测 R）
- CIP 脚本：build/dbg_cip_adduct.py（基准，sha 8e7f852f…）、build/check_cip_lane3.py（已修，sha c3153ee0…）

## 3 两阶段落地（避免原子序猜错）
1. **第一次调用不传 guess**（只传 reaction/calculations/conformers）→ 工作流建好绑定的 reactant/product 结构并停在可检查点；此时**不消耗 QM**（若它仍提交作业，立即 ts_inspect 读状态并判断）。
2. `ts_inspect(run_id)` 读 `structures`（1-based 原子表）→ 把我方 ORCA 序的 guess 重排成它的当前序（element+连通性对照，用 build/ 里同一分子的 mol 文件核对）→ `ts_resume(run_id, changes={guess:{...}, reaction_center:[[i_C3,i_C6],[i_C2,i_N20],[i_C2,i_C3],[i_O5,i_C6]]}, reason="add provided TS seed in current atom order")`。
3. TS/IRC 由工作流自动推进；每个阶段结束后 ts_inspect 读 `available_results`（**原生日志绝对路径**）→ log_parser 独立复核（normal termination / opt_converged / 虚频数与 watch_pairs）。

## 4 回退方案（仅在 provided guess 失败时）
- 退一步用 `guess.kind="scan"`：Gaussian 弛豫扫描 d(C3–C6) 由 3.6 → 1.7 Å、7 步，起点用对应通道的 (S) 前复合物；扫描**能量不作证据**，只取内峰帧当 TS 种子。注意历史 job_58/job_59 都在 ~2.6–2.9 Å 处发生氢键断裂/分支跳变（discontinuous scan58），故扫描必须检查每帧的 O5···H24 与二面角，别把跳变点当鞍点。
- 备用种子：E2 → TS_guess_E2_j58f6/f8；EM1 → TS_guess_EM1_j59f8/f10。

## 5 验收清单（每通道，缺一项即未通过）
| # | 项 | 判据 | 证据 |
|---|---|---|---|
| 1 | 起点 (S) HI1_I1 | 无约束 Opt+Freq、0 虚频、3 分片、脯氨酸 5 元环 + 苯基 6 元环、Cα CIP=S | 原生 .log + sha256 + 原始行能量 |
| 2 | TS | 恰 1 虚频；虚频模以 C3–C6（本序 1–29）为主导（附 C2=C3 与 C6=O5 的 π 变化）；给出主导原子对与数值 | log_parser watch_pairs=[[1,29],[2,4],[2,1],[28,29]] |
| 3 | IRC | 双向真实到达 I1 与 I2（resp. M1），给方向区间端点归属 | 原生 IRC 日志 + 端点几何 |
| 4 | 两端点 | 无约束 Opt+Freq、0 虚频；I2 map6=S / M1 map6=R、两处 Cα=S（RDKit 实测 + map↔原子序对照） | 原生 .log + dbg_cip_adduct.py 输出 |
| 5 | 能垒 | E(TS)−E(同一 (S) I1 极小值)，纯电子能差（无 ZPE/热校正），本批 Gaussian 16 同程序相减 | 原始行能量 + 算式 |
| 6 | ΔΔ | E(TS_minor)−E(TS_major)，与历史 2.16 如实对比（差异显著就写差异） | 同上 |

### 5b 交付级硬约束（主协调 2026-10-15 19:1x 确认；lane3 接续执行）

- **能垒基线固定为 job 924**（(S)-HI1_I1 极小值，输入 `runs/I1_optfreq/I1_S_optfreq.gjf`）：两通道交付能垒一律 = **E(TS) − E(924)**，纯电子能、同批 Gaussian 16。
- **禁止**改用 job 907（E1 的 (S)-RC，物种不同：907 = 脯氨酸+丙酮+苯甲醛，924 = 烯胺+水+苯甲醛）；**禁止**用工作流自身的 reactant 端点替代 924。
- 仅当 924 未通过验收（**0 虚频 且 Cα=S**）才另议替代，且必须先报包 Coordinator（as_84bdf87a0f94416c）并写明替代 provenance（哪个极小值、为什么、能量原始行）。
- `guess.evidence_refs` **必须是真实存在的 artifact 文件路径**（prose 会被 ts_prepare 以 provided_guess_invalid 拒）：
  - 通道 A → `build/TS_SEED_PROVENANCE_E2.md`（sha `121ac600…`）
  - 通道 B → `build/TS_SEED_PROVENANCE_EM1.md`（sha `73ee4aa8…`）
- run 的权威 revision 在 `ts/<run>/process.json`（**不是** declare.json）；`ts_resume` 必须带 `reason` + 从 `ts_inspect` 读到的 revision，并核 `receipt.changes`。
- 绑定序换算与 watch pair 表：`build/ATOM_ORDER_AND_WATCHPAIRS.md`；重排脚本：`build/reorder_guess_by_permutation.py`（identity 往返实测 maxdev=0.000000 Å）。
- 资源：本包同刻 ≤2 个作业（含排队）；手工提交 **priority 0**；队深 ≥6 时只提关键路径作业；两通道**串行**。
- 报告格式（每通道一行）：边 | 通道 | E(TS)/Eh（原始行） | E(924)/Eh（原始行） | ΔE‡ kcal/mol | 虚频数/频率 | IRC 双向端点归属 | 两端 CIP | TS log 绝对路径+sha256。

## 6 纪律
不改 hi.py / HI1.json / hard.md / 生成器 / 评分规则；不改图；缺测写缺不填 0；不设非原生 MaxIter；不取消/重投排队作业、不调 priority；每次提交前 qm_slots 取槽，整条 run 结束 rmdir；原生日志不改写。
