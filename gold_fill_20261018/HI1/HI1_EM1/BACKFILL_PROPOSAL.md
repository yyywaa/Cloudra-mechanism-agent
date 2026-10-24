# HI1_EM1 回填提案（BACKFILL_PROPOSAL）· 2026-10-18

> 本文件是**回填提案模板 + 当前进度**，不是回填值。任何数值在 (c) 交付判据三环齐备前都不得写入
> 题源（hi.py / HI1.json）；hi.py 的回填由主协调统一写，本 lane 只提供证据与算式。
> 现盘状态：**未回填，result = candidate_only**。

## 0 回填影响面（⑧，先读；本 lane 未改动任何交付面文件）

| 面 | 文件（现盘读 sha，不许用旧快照） | 回填时要改成什么 |
|---|---|---|
| registry | `cloudra/benchmark/hard_registry/hi.py` 的 `I1.competing[0].barrier`（现 15.52 = 旧程序/旧模型 L2 身份值，节点文本已注明「非本模型实测」） | 改成新 ΔE‡（kcal/mol，2 位小数），并把 type 文本里的「15.52 是 legacy」说明改为本批口径（G16、B3LYP/def2SVP+GD3BJ、CPCM(DMSO)、纯电子能、参考 job 924） |
| task json | `ideapool/tasks/hard/HI1.json`（**生成物，禁止手改**） | 由 registry 重新生成（`python -m cloudra.benchmark.gen_hard_tasks`） |
| 题源 md | `hard.md` 第 112 行区间（competing 条目） | 只改本边那一行的数值与脚注（旧值 → 新值、程序口径、参考态） |
| tests | `tests/test_benchmark.py` | 若断言里含 15.52，改成本批值；守卫 `pytest tests/test_benchmark.py -k regenerate_identically` 必须通过 |

其它影响面（必须声明，非本 lane 写）：HI1 五步模型是**本地修订、未提交**（远端 master 仍三步图），
回填时必须单列「本地修订与 master 差异」；本 lane 只做 HI1_EM1 一条边。

## 1 边与任务标识（①）

| 项 | 值 |
|---|---|
| task id | **HI1**（H/I 族 hard 题，I1 脯氨酸 aldol，selectivity 锚点） |
| edge id | **HI1_EM1**（`I1.competing[0]`，from_step=2 → 烯胺装配体；minor_face 通道；产出 (R)-亚铵-醇盐 M1） |
| 反应 | `[CH3:1][C:2](=[CH2:3])[N:20]...COOH . H2O . O=CH-Ph` → `...C@@H:6(O-)Ph . H2O`（C6 由非手性 → R） |
| durable run | **ts/ts_0025**（本 lane 新建；旧 ts_0012 不属本授权工程，无法 resume） |

## 1b 当前状态（2026-10-18 04:38 更新）

- **ts_opt 已收敛**：job 1095（ts/ts_0025/jobs/declaration_0003/ts_opt/refine.log，sha256 57cb84396d5a26e80308d102707a071671a84ee9d0a6aebaf29863d49e089912，4114 行）：L3002 `Optimization completed.`、L3003 `-- Stationary point found.`、收敛表 L2996–3001 四项 YES、L2625 末 SCF **E = −939.283734386**、L4114 Normal termination（04:28:56）。该几何与 ts/ts_0012/jobs/declaration_0002 的 TS 帧同一驻点（maxdev 0.0017 Å、能量差 1.2e-8 Eh；注意 job 1032 = declaration_0001，E = −939.293671629、虚频 −27.9419，**不是**这一帧）。
- **freq 已自动起跑**：job **1103**（ts/ts_0025/jobs/declaration_0003/frequency/frequency.gjf，04:29:00 起，4c/6144，CPCM(DMSO)），截至 04:37 仍在解析 Hessian 链条，**尚无虚频段**。
- **判读口径（先定，事后不改）**：恰 1 虚频 → (a)/(b) 用新几何重算后继续 IRC；**0 虚频 → #1095 是极小、本 guess 作废换 seed**；≥2 虚频 → 换 seed。
- 现值仍 **null**：ΔE‡ 未取得，分母锁 job 924 = −939.308218263（另一批次，仅身份/几何参照）。
- 更正留痕：本条原写「1095 末能量 −939.283734374 与 job 924 参考极小同值」——**错**，924 是 −939.308218263；−939.2837… 是 TS 驻点值，两者相差 15.36 kcal/mol（纯算术，不作 ΔE‡）。

## 2 旧值与新值（②）

| 项 | 值 | 状态 |
|---|---|---|
| 旧值 | **15.52** kcal/mol（旧程序/旧模型 L2 身份值，非本轮实测；节点文本已注明） | 现盘 registry 值 |
| 旧值是否 null | 否（数值 15.52） | — |
| 新值 ΔE‡ | **待定（留空）** —— 必须等 ts/ts_0025 的 freq 原始 `SCF Done` 行 + 双向 IRC + 两端 Opt/Freq 齐备 | 未取得 |

## 3 (a)(b)(c) 逐项结论（③）

**以下 (a)(b) 是基于旧 run ts_0012 的 freq（几何 = ts/ts_0012/jobs/declaration_0002 的 TS 收敛帧，E = -939.283734374、虚频 -314.2861；注意 job 1032 是 declaration_0001，E = -939.293671629、虚频 -27.9419，两者差 6.24 kcal/mol，不是同一帧）；ts/ts_0025 的 freq 出来后必须用同一脚本重算一遍再定稿。**

| 环 | 判据 | 结论 | 依据 |
|---|---|---|---|
| a1 | 虚频模在声明 watch pair 上方向与 gold bond_changes 同向 | **过** | C3–C6(1,29) 净投影 **−1.109（缩短）**；C2=C3(2,1) **+0.166（拉长）**；C6=O5(28,29) **+0.177（拉长）**；与题源同向（另 C2=N20 −0.070 缩短） |
| a2 | 恰 1 虚频 | **过** | freq.log L1541 `1 imaginary frequencies`；L1550 = −314.2861 |
| b1 | 反应中心对份额 | **0.6665** | 原子 {1,2,4,28,29} 的平方位移份额和（无阈值） |
| b2 | 该模重原子份额 | **0.6951** | 20 个 C/N/O |
| b3 | 最大单原子份额 + 落在哪个自由度 | **原子 1（C3）= 0.3282**，落在**反应中心** | ⇒ **非 soft-mode-dominated，BRIEF ① 不缺口** |
| c1 | TS 恰 1 虚频（**新 run** 原生 log） | 待跑 | `ts/ts_0025/jobs/declaration_0001/frequency/frequency.log` |
| c2 | 双向 IRC 到达声明两端 | 待跑 | maxpoints=140/侧、stepsize=5、recalc=20；旧 IRC 正向点耗尽 L8405 / 反向 l123 L25166 永不作证据 |
| c3 | 两端 Opt+Freq 0 虚频 | 待跑 | `.../reactant_opt`、`.../reactant_frequency`、`.../product_opt`、`.../product_frequency` |
| c4 | CIP 身份 | 种子已核：Cα(8) S / C6(29) R | 两端几何待核（**strip atom-map 后判定**） |
| c5 | 分片/质子归属与主面 I2 比对 | 待核 | 3 分片；亚铵 C2=N20⁺、醇盐 O28、水 O25 带 2H |

## 4 TS 证据（④）

| 项 | 值 |
|---|---|
| TS freq 日志（**新 run，待生成**） | `/home/ly/Cloudra-mechanism-agent/ts/ts_0025/jobs/declaration_0001/frequency/frequency.log`（sha/行号待填） |
| 现可用的同几何 freq（旧 run） | `/home/ly/Cloudra-mechanism-agent/ts/ts_0012/jobs/declaration_0002/frequency/frequency.log`，sha256 **a471aa7b6c2b34b7ccff44a98bbcd0dee7c4ae5f436653fe79f094f44fe53a65** |
| 虚频值 | L1550 `Frequencies --   -314.2861   33.5499   44.0361`；L1539 `Low frequencies --- -314.2862 ...`；L1541 `****** 1 imaginary frequencies (negative Signs) ******` |
| 模矢（原子 1 与 29） | L1551 起 `Atom AN X Y Z` 块：原子 1 (0.24, −0.11, 0.51)；原子 29 反相（见 `build/analyze_mode.py` 复算，净投影 −1.109） |
| TS 能量 | L857 `SCF Done:  E(RB3LYP) =  -939.283734374`（旧 run；新 run 待填） |
| 几何来源 | `.../ts_opt/refine.log` sha256 **66691e0e68e9044d7d10e45e8953e6c5468efee3d361713d3e34d7bfbb2b4241**，L24549/L24550 收敛、L24183 末次 SCF −939.283734374、L25650 正常终止 |
| 117 模 | 39 个 `Frequencies --` 行（3 模/行）；L5340 正常终止 |

## 5 两端点证据（⑤，全部待生成）

| 端点 | 日志路径 | sha256 | 行号 | 虚频数 | 身份 |
|---|---|---|---|---|---|
| 反应物端 `reactant_frequency` | `ts/ts_0025/jobs/declaration_0001/reactant_frequency/`（待） | 待 | 待 | 须 0 | Cα(8)=S，3 分片 |
| 产物端 `product_frequency` | `ts/ts_0025/jobs/declaration_0001/product_frequency/`（待） | 待 | 待 | 须 0 | C6(29)=**R**、Cα(8)=S，2 分片 |
| 产物端备用种子 | `gold_fill_20261018/HI1/HI1_EM1/build/prod_seed_EM1_irc_rev_pt2.xyz` | d2252cbc313659a3b7efef2bae0113f669e36dd2b785e784311b4d7ae58c7115 | — | — | d(1,29)=1.767 Å，CIP S/R |

## 6 ΔE 算式（⑥）

```
ΔE‡ = 627.509474 kcal/mol per Eh × [ E(TS) − E(参考极小值) ]
E(TS)            = <待填，ts/ts_0025 freq 原始 SCF Done 行，绝对路径 + sha + 行号>
E(参考极小值)     = -939.308218263 Eh   (job 924 = (S)-HI1_I1 Opt+Freq；三个独立 Opt+Freq 收敛到同一值，差 ~1e-9)
```
- **同程序同方法同模型**：Gaussian 16（/home/ly/g16/g16），B3LYP/def2SVP + EmpiricalDispersion=GD3BJ +
  Int(UltraFine) + SCF=Tight + SCRF=(CPCM,Solvent=DMSO)，q0/m1，纯电子能（无 ZPE/热校正）。
- 参考态锁定 job 924；**禁止**用工作流自身 reactant 端点、禁止 job 1000（−939.302926757，伸展构象）、
  禁止与历史 15.52（旧程序）相减或混用。

## 7 仍缺哪一环（⑦，当前）

**缺：新 run ts/ts_0025 的 freq → 双向 IRC → 两端 Opt+Freq（c1/c2/c3/c4/c5 五环），加 E(TS) 与 ΔE‡ 两个空值。**

## 8 判定分支（锁死，防事后改口）

- (a)(b) 过 + IRC 未到端点 ⇒ **candidate_only，不回填**（当前状态）。
- (a) 不过（方向相反）⇒ **pseudo-saddle，永不回填**。
- IRC 产物侧再次 l123 Delta-x 不收敛 ⇒ 不许写「双向到达」；走**替代口径（受约束弛豫扫描 + 两端 Opt+Freq）**，
  且必须显式标「**替代口径：无 IRC**」。
- 端点 Opt 收敛回 TS 或漂到别的构象 ⇒ 端点身份不成立，不回填。

## 9 CIP 判定口径（全项目统一：strip atom-map 后再判）

**所有 CIP 判定一律先 strip atom-map 再判；带 map 的判定只作诊断、不入证据。**
理由（本 lane 实测）：同一几何、同一拓扑，保留 atom-map 号时 RDKit 3D 判定把 Cα(8) 判成 **R**，
strip 后为 **S**；atom-map 号是题源标记、不是立体化学信息。

调用方式（`cip_check.py` 默认 strip，`--keep-maps` 只用于诊断对照）：

```bash
cd /home/ly/Cloudra-mechanism-agent
.venv/bin/python gold_fill_20261018/HI1/HI1_EM1/build/cip_check.py \
    gold_finish_20261015/HI1/E2EM1/build/TS_guess_EM1_j59f9_adduct.mol \
    gold_fill_20261018/HI1/HI1_EM1/build/TS_EM1_job1032_final.xyz 8 29
# 输出：atom 8 C -> CIP S ; atom 29 C -> CIP R
# 注（04:36 标注核对）：文件名的 job1032 是历史误名，其几何经 RMS 核对（逐原子，无旋转）
# 与 ts/ts_0012/jobs/declaration_0002/ts_opt/refine.log 末帧 rms 0.0000 Å 一致、
# 与 declaration_0001 末帧 rms 3.6413 Å 不一致 ⇒ 内容是 declaration_0002 的 TS 帧（E = -939.283734374、虚频 -314.2861）。
# 文件名不改（已在多处引用），但引用时必须标 declaration_0002。
# 对照（诊断，不入证据）：加 --keep-maps 会把 atom 8 判成 R
```

## 10 当前卡点与作业

- **job 1088（ts/ts_0025 ts_opt）ready 排队**（position 3）。不重提、不抢槽、不 kill 他人作业。
- 降配尝试：ts_resume 改 execution.cpus/memory_mb 被**接受**（revision 11→12、input_revision 1→2、
  changes = execution.cpus + execution.memory_mb），但**已存在的 ready 作业 1088 未被撤回/重发**，
  队列里仍是 8c/10240 → 该作业实际不会降配。run 级 execution 现为 4c/6144，后续自动创建的作业按此执行。
- 报告格式（一行）：`HI1_EM1 | 结论 | job id | 缺哪一环`。

## 9 平台观察记录：ts_0025 / job 1095 长驻 l703（结论：在算，不是卡死）

- **现象**：作业 04:11 起 running；refine.log（sha256 a9d48961…，1795 行）只有 1 次 SCF（L1125，E = -939.283734374，15 圈 SCF）、0 个收敛步；日志 mtime 停在 04:17:00；平台任务目录 /home/ly/g16/scratch/cloudra_g16_task1095_1884176 为空（mtime 03:44）。
- **实测**：Gaussian 的 -scrdir 指向 /home/ly/g16/scratch，真正的现场文件是 Gau-1884245.rwf（793,980,928 B，mtime 04:17:00）与 Gau-1884245.skr（524,288 B）⇒ 平台 task 目录为空是常态，不能当「无写入」判据。
- **04:25:47 实测**：/proc/1884245 cpu 增量 11,241 ticks / 30 s ≈ 112.4 s CPU ≈ 3.7 核；State = R，Threads = 4；进程为 l703.exe。
- **日志尾部定位**：L1199 Leave Link 1002（cpu 3884.0 s、elap 1073.4 s）、L1781 Leave Link 601、L1784 Leave Link 702、其后进入 l703「Compute integral second derivatives … FoFJK」，至今无 Leave Link 703 ⇒ 正处于 opt=(TS,calcfc,noeigen) 的解析二阶导积分阶段（calcfc）。输入头 L2/L3 = %nproc=4 / %mem=6144MB。
- **判读（D20 补充）**：calcfc 阶段整段日志静默属正常（模块只在退出时打印 Leave Link 行）；判活应以「CPU 增量 + 已在盘上的 rwf 体积」为主，辅以当前 Link 名。「空 task 目录 + 日志静默」不能单独判卡死。
- **复核条件**：若 rwf mtime 冻结状态下 l703 持续 > 60 min 且仍无 Leave Link 703，则重新评估；届时撤单只能由主协调走账本 cancel 通道（本 lane 无撤单通道），重提须用新 declaration 目录并保留本目录已产出帧。
- **不得引用的数**：L1125 那 1 次 SCF 不是收敛值，不作结果。**更正（04:35）**：本条原写「E = -939.283734374 与 job 924 参考极小同值属巧合」——错。job 924 的参考极小是 **-939.308218263 Eh**（见本文件第 78 行），而 -939.283734386 是 ts/ts_0012/jobs/declaration_0002 同一 TS 驻点的复现值（不是 job 1032；1032 = declaration_0001，E = -939.293671629、虚频 -27.9419）（几何 maxdev 0.0017 Å、能量差 1.2e-8 Eh）；两者相差 0.024483877 Eh ≈ 15.36 kcal/mol。故不存在「TS 与极小同值」的冲突。
