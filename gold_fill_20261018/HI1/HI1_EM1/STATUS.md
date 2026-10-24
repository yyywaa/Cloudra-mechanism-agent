# HI1_EM1（副面通道）状态 · 2026-10-18

会话：本 lane（QM 执行道）。工作目录：`gold_fill_20261018/HI1/HI1_EM1/`。
边 = **HI1_EM1**（HI1 的 competing / minor_face 通道：烯胺装配体 → (R)-亚铵-醇盐 M1）。只做这一条。

## 一句话

TS 候选（job 1032 收敛驻点）在方向上成立：(a) 过、(b) 过；**(c) 未过** —— 双向 IRC 与两端 Opt+Freq 尚未完成。
新 durable run **ts_0025 / job 1095（ts_opt，4 cpus / 6144 MB，ready 排队；原 job 1088 已按主协调 04:0x 降配令 ts_stop 撤回为 cancelled）**；ΔE‡ 仍未取得，驻点仍 **candidate_only**。

## 逐环（边 → job id → 卡在哪一环）

| 环 | job / run | 状态 | 卡在哪 |
|---|---|---|---|
| 候选 TS（上一轮） | job 1032 ts_opt（`ts/ts_0012/jobs/declaration_0002/ts_opt/refine.log`） | done，收敛驻点 | — |
| 候选 TS 频次（上一轮） | job 1036（`.../frequency/frequency.log`） | done，恰 1 虚频 −314.2861 | — |
| 候选 TS 判定 (a)(b) | — | **过**：方向与声明同向；份额见下 | — |
| 旧 IRC | job 1039（`.../irc/irc.log`） | failed | G16 默认 MaxPoints=10/方向被截断 + 反向 l123 Delta-x 不收敛 ⇒ 无连通性结论，永不作证据 |
| 新 run ts_opt | **job 1095**（`ts/ts_0025/jobs/declaration_0003/ts_opt/refine.gjf`，4c/6144）；job 1088 已 cancelled（从未起跑） | ready / 排队 | 等容量 |
| 新 run ts_opt（1095，declaration_0003） | job 1095（`ts/ts_0025/jobs/declaration_0003/ts_opt/refine.log`） | **done 04:28:56 CST**：L3002 `Optimization completed.`、L3003 `-- Stationary point found.`、末次 SCF **−939.283734386**（L2625）、L4114 `Normal termination`；日志 sha256 **57cb84396d5a26e80308d102707a071671a84ee9d0a6aebaf29863d49e089912** | — |
| 新 run freq | **job 1103**（`ts/ts_0025/jobs/declaration_0003/frequency/frequency.log`） | **running 04:29:00 起（4c/6144，管线自动提交）** | 等终态 |
| 新 run 双向 IRC | 未生成 | 未跑 | maxpoints=140/侧、stepsize=5、recalc=20 已写进 verification.irc |
| 两端 Opt+Freq | 未生成 | 未跑 | 等 IRC |
| ΔE‡ | — | 未取得 | 需 TS 与 job 924 同程序纯电子能，且 IRC 到达两端 |

## 判定口径现状（裁决 1）

- (a) 方向硬闸门 **过**：由 freq 模向量重算（`build/analyze_mode.py`）——
  C3–C6(1,29) 净投影 **−1.109（缩短）**、C2=C3(2,1) **+0.166（拉长）**、C6=O5(28,29) **+0.177（拉长）**，
  与题源 bond_changes 同向；C2=N20(2,4) −0.070（缩短，成亚铵 π）。
- (b) 成分（记录项，无阈值）：反应中心原子 {1,2,4,28,29} 合计 **0.6665**、heavy 20 原子 **0.6951**、
  最大单原子 = 原子 1（C3）**0.3282** ⇒ 最大份额落在**反应中心**，不是 spectator（不是 soft-mode-dominated）。
- (c) 交付：**未过**（缺双向 IRC + 两端 0 虚频 Opt/Freq）。

## 关键原生日志（只读，绝对路径 + sha256）

| 用途 | 路径 | sha256 | 关键行 |
|---|---|---|---|
| TS 几何（收敛驻点） | `/home/ly/Cloudra-mechanism-agent/ts/ts_0012/jobs/declaration_0002/ts_opt/refine.log` | 66691e0e68e9044d7d10e45e8953e6c5468efee3d361713d3e34d7bfbb2b4241 | L24549/L24550 收敛；L24183 SCF −939.283734374；L25650 正常终止 |
| TS 频次 | `.../declaration_0002/frequency/frequency.log` | a471aa7b6c2b34b7ccff44a98bbcd0dee7c4ae5f436653fe79f094f44fe53a65 | L1541 1 imaginary；L1550 −314.2861/33.5499/44.0361；L857 E；L5340 正常终止 |
| 旧 IRC（失败，不作证据） | `.../declaration_0002/irc/irc.log` | dfc4d3ec2bba6c84e634eeb7105fb48fe0481969c7e61b73413fb2ed47ff31e3 | L8405 正向点耗尽；L25166 l123 |
| 参考极小值（分母） | job 924 的 I1 Opt+Freq 日志（历史，只读引用；E = −939.308218263 Eh） | — | 由主协调台账登记 |

冻结副本（只读 444）：`evidence/refine_frozen.log`、`evidence/frequency_frozen.log`、`evidence/irc_frozen.log`（sha 同源）。

## 种子与产物端几何（本道产物，非 QM 证据）

| 文件 | 用途 | sha256 |
|---|---|---|
| `build/TS_EM1_job1032_final.xyz` | 新 run 的 guess（job 1032 收敛帧，41 原子，d(1,29)=1.8791 Å） | 663fe23166bb54de96c2698a43ae3d6207457be7b61d55a10a5972d8f29a3fce |
| `build/prod_seed_EM1_irc_rev_pt2.xyz` | 产物端备用种子（旧 IRC 反向 pt2 原帧，d(1,29)=1.767，CIP Cα S / C6 R） | d2252cbc313659a3b7efef2bae0113f669e36dd2b785e784311b4d7ae58c7115 |
| `build/prod_seed_EM1_ircfwd_pt10.xyz` | 反应物侧原帧（旧 IRC 正向 pt10，d(1,29)=2.438）—— 仅备查 | 92241c36a499c2bf3778628423b08aa5ddceb19be4589d3d3f5b86852ec29b0f |

CIP 口径：RDKit 3D 判定必须 **strip atom-map**（带 map 会把 Cα 判成 R，strip 后 S；见 provenance §6）。

## 方法 / 预算

Gaussian 16 B3LYP/def2SVP + GD3BJ + Int(UltraFine) + SCF=Tight + CPCM(DMSO)，q0/m1，纯电子能。
priority 0，同一时刻只一个在飞。**ts_opt / 端点 Opt+Freq 等辅助作业 4c/6144**；41 原子 freq / IRC 主作业可用 8c/10240，但全队列同一时刻只允许一条 8c 作业（须与 HI1_E4 道错开，提交前在 hub topic 声明占 8c）。

平台限制（本 lane 实测，原文见 provenance §8）：ts_resume 改 execution **只对今后新提交的作业生效**，不回改队列中的作业；排队/ready 作业降配必须 **ts_stop → ts_resume(changes={})**。本 run 走该路径后新作业 job 1095 = `req_cpus=4, req_memory_mb=6144`；job 1088 以 state=cancelled 结束（从未起跑、无日志/无锁）。

## 模型条件与边界（明确记录）

- 隐式 DMSO（CPCM）、电荷 0 / 单重态、C15H21NO4、41 原子、3 分片（烯胺 + 水 + 苯甲醛）；**无显式抗衡离子/助剂**；
  温度为 298 K 实验条件，但本口径只取纯电子能（无 ZPE/热校正），不建温度/浓度。
- 反应中心按题源 declare 口径：成 C3–C6、成 C2=N20 π、断 C2=C3 π、断 C6=O5 π。

## 归档 · 停止记录（用户 05:0x 指令「被换掉的题的任务可以杀了」+ 协调广播 evt_1368eb1b076741ac）

HI1 已被替换题（Cope 消除）替换 ⇒ **本道按指令停算，不再提交、不再 ts_resume**。证据一律原样保留，不删、不覆盖。

| 项 | 记录 |
|---|---|
| run | `ts/ts_0025`（本 lane 新建；停止后 status=**stopped**、revision 25、result=null） |
| 停止指令时刻 | 本机 `date -Is` = **2026-10-18T04:50:52 CST**（ts_stop 返回 stopped 时刻 04:51:01） |
| 在飞作业 | **job 1103（frequency，4c/6144，declaration_0003，04:29:00 起）→ state = cancel_requested**（平台安全撤停，本 lane 未自行 kill 进程） |
| 作业输入 | `ts/ts_0025/jobs/declaration_0003/frequency/frequency.gjf`（route `#p freq B3LYP/def2SVP empiricaldispersion=gd3bj int(ultrafine) scf=tight scrf=(cpcm,solvent=dmso)`） |
| 截断时日志 | `.../declaration_0003/frequency/frequency.log`，55113 B，sha256 **4ce6c6cf3e76e7728b57b8041ef3b4cb73b9829abbb5a52f554ab0eb20221b14**（截断于解析 Hessian/CPHF 阶段，**尚未输出任何频率**） |
| 已完成的合法环节 | job 1095（ts_opt）done 04:28:56：L3002/L3003 收敛、L2625 E=−939.283734386、L4114 正常终止（sha 57cb8439…）；几何与旧帧 maxdev 0.0017 Å |
| 性质 | **调度终止**（用户指令 + 协调裁决），**不是科学失败**；不得写成「TS 不成立」「IRC 不收敛」等结论 |
| 未完成 | 新 run freq（无频率输出）→ 双向 IRC → 两端 Opt+Freq → E(TS)/ΔE‡ 全部未取得 |
| 结果状态 | **HI1_EM1 = candidate_only（未回填）**；(a)(b) 仅由旧 run 同几何 freq 支持；(c) 从未满足 |

下游不再动作：不重提、不 ts_resume、不 kill 他人作业、不改 priority、不写题源。

