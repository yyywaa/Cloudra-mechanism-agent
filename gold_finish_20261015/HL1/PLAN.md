# HL1 包 · 计划与口径（2026-10-15）

包 Coordinator：as_e9e07289de3d4c62。唯一目标边：**HL1_E1**。
工作根目录：`/home/ly/Cloudra-mechanism-agent`；本包目录：`gold_finish_20261015/HL1/`。

## 1 科学定义（题源口径，不得改图）

- 反应：`[OH3+].CC/C(=N/O)/C` → `O.CC/C(C)=N/[OH2+]`（(E)-丁酮肟 + H3O+ → O-质子化肟 + 水）。
- 图：registry `cloudra/benchmark/hard_registry/jl.py` L1 的 `steps[0]` = HL1_E1，节点 `HL1_R → HL1_I1`，via `HL1_TS1`。
  - 题源 mapped SMILES：`[O+:1]([H:2])([H:9])[H:10].[CH3:11][CH2:5]/[C:4](=[N:6]/[O:7][H:8])/[CH3:3]`
  - bond_changes：break `[[1,2]]`（H3O+ 的 O1–H2），form `[[2,7]]`（H2–肟 O7）。**O-质子化，不是 N-质子化。**
  - 原子：19（C4H12NO2+），电荷 +1，多重度 1，气相，单重态。
- 参考极小值：题面（HL1.json prompt）明定 **bimolecular 步的起点极小值 = RC 预反应络合物（ion–dipole complex）**，不是分离物种。
  → **ΔE‡ = E(TS1) − E(RC 络合物极小值)**，纯电子能（无 ZPE/热校正），同程序同批相减。
- 历史事实（只引用，不重算）：95 参考优化失败；104/105 路径准备无候选；107 受约束扫描第 9 点达原生上限未收敛 + PROPERTIES SHARK 读临时输入失败、质子移向 N、第 8 点比第 7 点高 0.3766 kcal/mol；旧 Gaussian 单调扫描 0 作废，"candidate barrierless" 已撤回。
- **本地核对：supplement_20261002/ 只有文字交接与 task_sources，95/104/105/107 原生日志本地不存在。**

## 2 方法（本轮统一偏离，必须显式写出）

Gaussian 16（`/home/ly/g16/g16`）：`B3LYP/def2SVP` + `EmpiricalDispersion=GD3BJ` + `Int(UltraFine)` + `SCF=Tight`，**气相（不写 SCRF）**、q+1/m1。
本机无 ORCA。**不得**与历史 ORCA 的 23.13 / 10.44 / 13.46 混减；那三条边不动。
TS/IRC 只走 durable `ts_prepare` / `ts_resume`（手工 TS/IRC 被禁用）。普通 Opt/Freq/探索扫描可用。

## 3 验收链（逐项，缺一即未通过）

1. TS Opt 原生正常结束并收敛；eig 恰 1 个虚频，且虚频位移以转移质子（O1–H2–O7）为主（log_parser watch_pairs 占比）。
2. 双向 IRC 有真实外帧，两端无约束 Opt+Freq 为收敛的零虚频极小值，物种/质子归属核验。
3. ΔE‡ = E(TS1) − E(RC min)，纯电子能，同批同程序。
4. 原生日志不改写，记录绝对路径 + sha256，能量取自日志原始行。
5. 写回题源（只改本包文件）→ 重新生成题面 → 守卫测试通过。

## 4 文件归属（只改这些）

| 文件 | 动作 |
| --- | --- |
| `cloudra/benchmark/hard_registry/jl.py` | 只给 L1 steps[0] 加 `barrier` + 必要注释 |
| `ideapool/tasks/hard/HL1.json` | 由生成器重生（不手改） |
| `ideapool/reaction_candidates/hard.md` | 只改 L1 那一行（改前重取 sha256，用 edit） |

⚠ 注意 anchor 校验：hard.md L1 行能垒格必须等于 registry 的 `max(逐边 barrier)`（非 parallel 分支）。
若 E1 值 > 23.13，必须同步改 md 行能垒格；若 < 23.13 则 md 锚点保持 23.13。

## 5 分工

- small_mol（HL1 计算 owner）：建 RC/产物络合物与 TS 初猜 + 全原子映射，独占 ts_prepare/ts_resume 跑整条链。
- explorer（HL1 复核）：历史证据与已证伪清单；对计算 owner 返回的链做只读独立复核（log_parser 能量、虚频模式、IRC 端点身份）；在 O 侧失败时整理裁决证据包。

## 6 资源

本包同时 **只 1 个 QM 作业**；单作业 ≤12 cpus / 14000 MB（`%nprocshared=12`、`%mem=14GB`）。不设非原生上限、不杀别人作业、不重复提交。
