# HI1 非 QM 准备产物登记（交付引用用；2026-10-15 18:1x，包 Coordinator as_84bdf87a0f94416c）

> 规则：本文件只登记**已存在**的文件（路径 + sha256，均为 2026-10-15 当晚真实 sha256sum 输出）；待产出项明确标"待产出 + 属主"。sha256 在下一次改动该文件后即失效，交付时须重取。

## A 共享基线与工具（包 Coordinator）
| 文件（项目相对路径） | sha256 | 内容 |
|---|---|---|
| `gold_finish_20261015/HI1/shared/SHARED_I1_identity_20261015.md` | `e76550cd38368acf039af4fb94430fa9e5140978cff02225aee4dfdcbd8c2b29` | 907/908/924 身份核验、可复现命令（L20–30）与原始输出（L34–42） |
| `gold_finish_20261015/HI1/shared/I1_identity_20261015.json` | `cf70ece70225eae4264ad8820403abe8992d777573f8cfb4998948b04a248ef0` | 同上机读版 |
| `gold_finish_20261015/HI1/shared/tools/hi1_cip_tools.py` | `fd3ec2ed09fab5b211d88e4b525c8afc4a62ba738ffe9ef2da2c1a8e148a09f8` | 从 Gaussian log 取最后一个 Standard orientation + RDKit 实测 CIP（首版 `6c508d55…`，其后仅加 .gjf 读取分支） |

## B E1 合并边（lane1 = small_mol as_99941bb328454a0c；durable run `/home/ly/Cloudra-mechanism-agent/ts/ts_0004`）
- **声明的成断键对（map 号，取自 `cloudra/benchmark/hard_registry/hi.py` I1.steps[0]）共 7 对**（主协调来函写"6 个"，实为 3 断 + 4 成）：
  break `(2,4)` C2=O4、`(3,22)` C3–H22、`(20,21)` N20–H21；form `(2,3)` C2=C3 π、`(2,20)` C2–N20、`(4,21)` O4–H21、`(4,22)` O4–H22。
- 几何（均已 RDKit 3D 实测 Cα=S）：
  - `gold_finish_20261015/HI1/E1/build/RC_start.xyz` sha256 `f4eb0ba6f085114c97cb13bcdbe03a8613a2f95262782bcb5fb9da5c6d9b93c0`（(S) 反应物复合物起点；job 907 的起点，907 极小值 E=−939.308829219 Eh）
  - `gold_finish_20261015/HI1/E1/build/I1_S_start.xyz` sha256 `c9d59aeab418c248629922ee37d4ea3822c64b7128dd63b3034d3c8c5ec2df3d`（(S)-I1 起点）
  - `gold_finish_20261015/HI1/E1/build/TS_guess_merged.xyz` sha256 `74d3d3e12d6c48398857a986a29034546b9fb93ace4388fe2a2d4fbbcc87fe13`（合并边 TS 初猜，d(C2–N20)=1.95 Å）
- 待产出（属主 lane1）：`E1/TS_GUESS_PROVENANCE.md`（provided guess 的 evidence_refs 必须是真实文件路径）、`E1/LANE1_STATUS.md`、**绑定序**（ts/ts_0004 `structures`）+ map→绑定序对照表、TS freq 的原生 `Frequencies --` 行与 watch_pair_fraction 判据。

## C HI1_E3 水解（lane2 = small_mol as_7da73f2d3f6d40a9；job 925 → I2 极小值 → 水解 TS）
- `gold_finish_20261015/HI1/E3/prep/I2_prep_cons180_v3.gjf` sha256 `4f8c4851b8ba74013c1cc162c1158ce7d826ac93a1637fe446ce1bc5b0c292c3`（按原输入重提；只补空行 + 8c/8GB）
- `gold_finish_20261015/HI1/E3/prep/I2_P_atom_map.json` sha256 `33912bbd415bc424da1f086bc61c696cd6b9eac5f4f2aa7c8b550cd3ce3a980e`（I2→P 的 41 原子 concrete atom_map）
- `gold_finish_20261015/HI1/E3/plans/E3_execution_plan.json` sha256 `65cdb818ec42be10b72fdb4ba916159d6b054a3e52a9444325ba6212d9e24c30`
- **声明的 6 个 watch pair（E3 工作序）**：break `(2,4)` C2–N20、`(25,26)` O4–H21、`(25,27)` O4–H22；form `(2,25)` C2–O4、`(4,26)` N20–H21、`(28,27)` O5–H22。
- 待产出（属主 lane2）：job 925 的约束末端几何 → 无约束 Opt+Freq（I2 极小值，0 虚频 + 原子 8/29 CIP 核验）、TS guess provenance、`E3/STATUS.md` 更新（含上轮 candidate_only 缺口清单）。

## D lane3 HI1_E2 / HI1_EM1（as_2f1b7321a5e042c8）
- 共享基线 = **job 924**（(S)-I1 Opt+Freq）：输入 `gold_finish_20261015/HI1/E2EM1/runs/I1_optfreq/I1_S_optfreq.gjf` sha256 `8b843b95bb55f46921f9aa23f9c172d906261b881e433db4c419605913cef0a9`；**硬约束：交付值 = E(TS) − E(job 924 极小值)**。
- TS 种子（几何预测：按加成物拓扑 3D 定 CIP；非 QM 证据）：
  - `gold_finish_20261015/HI1/E2EM1/build/TS_guess_E2_j58f7.xyz` sha256 `9e5ccc2fe5dde2e4c1900ad53cc8c1ddbae0e654a618c138adaffa58dd522e38`（通道 A major_face→I2，预测 map6=S）
  - `gold_finish_20261015/HI1/E2EM1/build/TS_guess_EM1_j59f9.xyz` sha256 `a7b50b7c23031e9c527ecaad4e08961bcfcec26880cac834b93f6bbfd5f214be`（通道 B minor_face→M1，预测 map6=R）
  - `gold_finish_20261015/HI1/E2EM1/build/I1_S_from_job59.xyz` sha256 `22f730d231bc91c39f73851e62b9d8eba0db6357a7aaeeddab6484226df2e697`（第二 (S) 起点，Cα=S）
- CIP 工具：`gold_finish_20261015/HI1/E2EM1/build/dbg_cip_adduct.py` sha256 `8e7f852f43432519f7c646b32c04a0f4f09a3381bc827ec028de279c7ea47762`（基准）；`.../build/check_cip_lane3.py` sha256 `c3153ee0306865c4167ae1a31c2f5c6f95c79f189897693c739387a3535b5d1d`（已修拓扑 bug，与基准一致）
- 待产出（属主 lane3）：每通道 TS seed provenance（真实文件）、绑定序换算表、CIP 绑定（I2 map6=S / M1 map6=R、两处 Cα=S 的实测输出）、`E2EM1/STATUS.md` 更新。



## F 2026-10-15 18:2x 各道新登记（我逐一真实 sha256sum 复核，与各道自报一致）
| 文件 | sha256 | 属主 / 用途 |
|---|---|---|
| `gold_finish_20261015/HI1/E1/TS_GUESS_PROVENANCE.md` | `d7a82f39e7d068400a0da60d4b59b7679c66441fd13cf885bb25f909f37a3276` | lane1：E1 merged-edge TS 初猜 provenance（provided guess 的 evidence_refs 应指向它） |
| `gold_finish_20261015/HI1/E1/lane1/RC_S_canonical.xyz` + `.mol` | 交付时重取（lane1 产出，2026-10-15 18:21） | lane1：RC (S) 的**绑定序**几何 + MOL（含 bond block），供 conformers.reactant=(file) 用 |
| `gold_finish_20261015/HI1/E1/lane1/TS_guess_merged_canonical.xyz` + `.mol` | 同上 | lane1：TS 初猜的绑定序版本（重排后），供 guess=(provided) 用 |
| `gold_finish_20261015/HI1/E1/lane1/make_lane1_binding_order.py` | 同上 | lane1：绑定序生成脚本（可复现） |
| `gold_finish_20261015/HI1/E2EM1/build/TS_SEED_PROVENANCE_E2.md` | `121ac600f960b933bd56e7a055bcdaaa021a8f46af884bf9779cabe6e2c93b07` | lane3 通道 A 种子 provenance（含源帧 job_58/scan_clean_np8.007.xyz sha `e662627f…`、镜像 maxdev=0.000000 Å、dbg_cip_adduct 原始输出 {8:'S',29:'S'}） |
| `gold_finish_20261015/HI1/E2EM1/build/TS_SEED_PROVENANCE_EM1.md` | `73ee4aa81a4f31c120dbbd5dc9c41abe71164d7852f9d404fb4e297b26c3ec5b` | lane3 通道 B 种子 provenance（源帧 job_59/scan_minor_clean.009.xyz sha `ae2ca403…`、镜像 maxdev=0.000000 Å、原始输出 {8:'S',29:'R'}） |
| `gold_finish_20261015/HI1/E2EM1/build/ATOM_ORDER_AND_WATCHPAIRS.md` | `6820379bec23fe0c7e2e79f91020a2e81a2a989d7d7e251606152d41ed1d9957` | lane3：41 原子 work idx ↔ 元素 ↔ 题源 map 全表 + source 序 reaction_center = [[1,29],[2,4],[2,1],[28,29]] |
| `gold_finish_20261015/HI1/E2EM1/build/reorder_guess_by_permutation.py` | `30e39ec7f499e684f0eed7d70d77cbc3858915485b8c2b503d02403a9e87bfa5` | lane3：按 ts_inspect 的 source_to_canonical 重排种子（identity 往返 maxdev=0.000000） |

**工具面观察（登记，待主协调提单）**：lane3 回报 `agent_hub call` 到包 Coordinator 会话 `as_84bdf87a0f94416c` 被拒（"[dispatch rejected] Delegation would grant permissions absent from the caller: manage"）；而 `post` 用 `to_agent="coordinator"` 被解析到**别的协调会话** `as_7479852819ea48c0`（NY3 包 Coordinator），不是本包。⇒ 各道回报统一改为：**post 到主题 `gold-finish-20261015`，正文首行写明 `to: as_84bdf87a0f94416c`**（本包 Coordinator 每轮会读主题帖）。

## E 交付时重取 sha 的命令
```
cd /home/ly/Cloudra-mechanism-agent && sha256sum <上表各路径>
```
