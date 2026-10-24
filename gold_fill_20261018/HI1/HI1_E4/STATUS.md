# HI1_E4（旧称 E3a「水加成到亚铵」）· QM 执行道状态

工作目录：gold_fill_20261018/HI1/HI1_E4/（新产物全部在此；历史 ts/ts_0016、gold_finish_20261015 只读引用）
方法（全道固定）：Gaussian 16 /home/ly/g16/g16，B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight + SCRF=(CPCM,Solvent=DMSO)，q0/m1，41 原子。

## 0 分母（本步自身起点极小值）= 亚铵-醇盐 41 原子 I2
- 原生日志：gold_finish_20261015/HI1/E3/runs/I2_optfreq/I2_optfreq.log
  sha256 = 63dda25e04529e65920526304fb88755db9393e9c22bd3a6efb76eeee0af0d0e（24001 行；job 961）
- E(RB3LYP) = **-939.320655479 Ha**（L16950 opt 末步 = L19183 freq 前 SCF）
- freq 链：L19879 起 `Frequencies --`，共 **117 模**，负频 **0**（`Low frequencies` L19869/L19870）
- 几何：runs/I2_optfreq/I2_min_v5.xyz（sha 9a6203ff…ef2b，41 原子，工作序）
- 实测成键：C2=N4 1.299（亚铵 C=N）；C9-O10 1.254 / C9-O11 1.250（羧酸根对称）；C29-O28 1.403 + O28-H24 0.984（醇羟基已带质子）；O25(H26 0.966)(H27 0.990)，H27…O10 1.717（水氢键羧基）
  ⇒ 模型物种 = 两性离子亚铵/羧酸根 + 醇 OH + 游离水（与先前 E3 STATUS B.1 的 q0 描述一致）。

## 1 已有合格单虚频驻点（只读引用）
- ts/ts_0016/jobs/declaration_0007/frequency/frequency.log
  sha256 = c5ac84026e43c5155f2bf6e20787885f77662666e737ad4783e16036ae7291b9
  L1501 `1 imaginary frequencies`；L1510 首组 = **-783.7914 / 23.6787 / 35.9094 cm-1**；E = **-939.295152015081**（L785）；41 原子，Input orientation L219
- 该驻点的虚频模成分（本道 analysis/mode_analysis.py 解析 Input orientation + mode 1 矢）：
  | 项 | 数值 |
  |---|---|
  | 声明反应中心原子对（C2-O25 + C2-N4）归一化份额 | **0.0714** |
  | 模内全部重原子份额 | **0.0420** |
  | 最大单原子份额 | **0.8939 @ atom 27 (H)** |
  ⇒ 最大份额落在 **H27 = 水 O25 ↔ 羧基 O10 之间的转移质子**（TS 上 O25-H27 1.1636、O10-H27 1.2466，几乎等距）；属 soft-mode-dominated 的质子穿梭，不是甲基转动/水取向等纯 spectator。
- 方向（需先做全局符号归一，模式矢符号任意）：把 (2,25) 取缩短方向后，dR(2,25)=-0.2525（成键✓）、dR(2,4)=+0.0650（C=N 拉长✓）；即 C-O 成键与 C=N 断裂同向耦合。
  但 (28,24)/(25,24) 在几何上不成立：TS 上 O28-H24 = 0.9674（共价 O-H），O25…H24 = 4.54 Å。

## 2 关键发现：题库声明的质子对在 41 原子工作序里错位一个原子
- registry（hi.py 第 4 步）atom-map 序：form (2,4)、(5,22)；break (2,20)、(4,22) → map22 是水的一个 H，map5 是醇盐 O。
- 平台把 map22 译成工作序 **atom 24**，但工作序里 atom 24 是**醇羟基的 H**（反应物极小值里 O28-H24 = 0.984 Å，且与 O25 相距 4.5 Å）；真正的穿梭质子是 **atom 27**，终点是**羧基 O10**（产物 P 上 O10-H27 = 0.995，C9-O10 = 1.33 = C-OH，C9-O11 = 1.214 = C=O）。
- 平台校验直接把它判死：ts_prepare 返回 `reaction_center_distance_out_of_range`（run ts_0024 rev 38）。修正后的申报对 = form (2,25)、break (2,4)、form (10,27)、break (25,27)。
- 化学含义：与 registry 文字（水加成、水的第二个质子转移）是**同一基元步**，只是转移受体质子化位点由「醇盐 O」改写为「羧基 O」——registry 注释本身已承认这是羧基/醇盐质子共振的等价表示。

## 3 新 run：ts_0024（durable 工作流）
- run_dir：ts/ts_0024；guess = ts/ts_0016/path/input_0007/provided.xyz（sha e3748c2c…1b9e，41 原子，S2 插值 λ=0.5306，R(C2-O25)=1.82）
- 反应物种子 = I2_min_v5.xyz；产物种子 = gold_finish_20261015/HI1/E3/prep/hemiaminal_1028_lastframe.xyz（sha be789d5f…572d，41 原子 hemiaminal）
- 两端口径：reactant_endpoint / product_endpoint 各自 Opt+Freq（g16 同方法）以便自证 0 虚频
- IRC 段计算档 g16irc：keywords 追加 `irc=(calcfc,maxpoints=40,stepsize=10)`（目标每侧 ≥30 点；旧 run 默认 10 点/侧被截断）
- 状态：**job 1090 = ts_opt（ready 排队中）**，输入 ts/ts_0024/jobs/declaration_0010/ts_opt/refine.gjf（route 行已核：opt=(TS,calcfc,noeigen) + 方法口径一致）

## 4 待办
1. 1090 收敛 → freq：确认恰 1 虚频并复算 (a) 方向 / (b) 三份额（新 run 自己的 dev 证据）
2. IRC：确认生成的 irc 路由里 maxpoints 是否真的生效（若框架叠加 irc=calcfc 造成重复关键字 → 记平台限制）
3. 双向末帧 vs 声明端点的 RMSD + 关键距离；两端 Opt+Freq 0 虚频 + 身份（CIP、质子归属、水是否完整）
4. ΔE‡ = E(TS) − E(I2) 纯电子能差；三项验收；BACKFILL_PROPOSAL.md

## 5 04:0x 主协调指令执行记录
- **降配试验（job 1090）**：`ts_resume` 只改 execution{cpus:4, memory_mb:6144} 被接受（revision 49，receipt.changes = ["execution.cpus","execution.memory_mb"]），但**已排队**的 job 1090 仍显示 `req_cpus=8 / req_memory_mb=10240 / state=ready`（ts_inspect 读回）⇒ 工具只对**今后新提交**生效，不回改已在队列里的作业。为不重复提交抢槽，保持 8c，未强制重提。队列实测：running 1074/1080/1082/1085（各 8c），queued 1086/1087/1088/1089/1090（各 8c）+ 1092（4c），free cpus=0。
- reaction_center 标签错位：主协调已落盘 gold_fill_20261018/HI1/HI1_E4/DECLARATION_FIX.md（45 行，sha fde5f915…），并独立复核 R(28,24)=0.9842 / R(24,25)=4.6512 / R(25,27)=0.9895 / R(27,10)=1.7171。题源侧由主协调改，我不改 hi.py；本 run 用等价工作序申报 [[2,25],[2,4],[10,27],[25,27]]。
- BACKFILL_PROPOSAL.md 必须含 8 项（边/task id、旧值与新值、a/b/c 逐项、TS 日志+sha+行号、两端日志+sha+行号+虚频数、ΔE 算式、仍缺哪环、回填影响面）。

## 7 04:2x 主协调裁决（预占位获批 + 排队口径）
- **批准**把 execution 预置成 8c/10240（run ts_0024 rev 58），理由：durable 流水线的 freq 自动提交，没有人为拦截点；「同刻只有一条 8c」由调度器 FIFO 保证，排队不等于失败。
- 约束 1：8c 的 freq 排队 >30 min 且 4c 槽空闲时，可 ts_resume 把 execution 改回 4c/6144 让它先跑，改前在 topic 报一句。
- 约束 2：EM1 道（as_fae50a6580774668）也可能预置 8c，撞上按 FIFO，先起跑者先跑完。
- 容量现状（主协调观测）：job **1074** 冻在某 SCF 迭代（末行 RMSU/CP，02:28 起 45 min 无进展），主协调在决定是否终止；在它让出 8 cpus 前，1094 这类 4c 作业也起不来 —— 记录为**容量等待，不是失败**，不重提、不 kill。

## 8 终止确认（05:0x 指令执行完毕）
- 平台事件确认：**job 1094 state = cancelled**（ts_0024 / refine / ts_opt），原因原文 = 「User 05:0x / coordinator directive: HI1 is replaced as a benchmark task ... archived mid-flight: ts_opt attempt ... is the only stage that ran; no freq/IRC/endpoint evidence exists for this run.」
- 归档证据路径（原样保留，未删未覆盖）：`ts/ts_0024/jobs/declaration_0012/ts_opt/refine.log`（476,368 B，7 个 SCF Done，无 Stationary point / 无 Normal termination，最后写入 04:50）、`ts/ts_0024/jobs/declaration_0012/ts_opt/.cloudra/calc-1094.out.log`、`ts/ts_0024/process.json`、`ts/ts_0024/jobs/declaration_0010/`（更早已 cancelled 的 1090）。
- 判定口径：**调度终止 ≠ 科学失败**；本 run 无任何科学结论，未回填。
- 最终交付：`gold_fill_20261018/HI1/HI1_E4/BACKFILL_PROPOSAL.md`（8 项全）+ `PROVENANCE.md` + `STATUS.md` + `analysis/*.py`。
