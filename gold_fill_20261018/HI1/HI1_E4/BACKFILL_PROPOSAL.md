# HI1_E4（旧称 E3a「水加成到亚铵」）· 回填/归档提案

**结论：不回填（题目按用户 05:0x 指令被替换，HI1 线全部停止）。** 本文按主协调 04:0x 的 8 项格式留档，供归档与将来重启时复用；所有数值均标注「本 run 自证」或「只读历史证据」。

---

## ① 边 id 与 task id
- 边 id：**HI1_E4**（台账旧称 **E3a「水加成到亚铵」**）
- task id：**HI1**（hard 题库，(S)-脯氨酸催化丙酮+苯甲醛 aldol），本边 = `cloudra/benchmark/hard_registry/hi.py` 的 I1 **第 4 步**（"water addition to the iminium"），当前 `barrier: None`。
- 模型：41 原子，q0/m1，CPCM(DMSO)；**无旁观组分**。

## ② 旧值 / 新值
- 旧值：**null**（未回填）。
- 新值：**不回填**。若将来重启此边，唯一候选 ΔE‡ = **16.00 kcal/mol**，且必须标明它是「旧只读日志同程序同方法相减」的候选值，**不是本 run 自证据**（见 ⑥）。

## ③ (a)(b)(c) 逐项结论
### (a) 方向（硬闸门）——基于只读旧驻点 + 三帧几何
- 旧驻点虚频模（mode 1，-783.7914 cm⁻¹）的模矢需先做全局符号归一（本征矢符号任意）。归一后：
  - **C2–O25：dR = −0.2525（缩短 = 成键方向 ✓）**
  - **C2–N4：dR = +0.0650（拉长 = π 键断裂方向 ✓）**
- 三帧距离单调（PROVENANCE.md 第 2/3 节，本道 `analysis/geom_table.py` 可复跑）：

| frame | R(2,25) | R(2,4) | R(10,27) | R(25,27) | R(28,24) | R(25,24) |
|---|---|---|---|---|---|---|
| I2 min（job 961 末帧，分母） | 3.160 | 1.299 | 1.717 | 0.990 | 0.984 | 4.651 |
| 旧 TS（freq.log L219 末块） | 1.861 | 1.343 | 1.247 | 1.164 | 0.967 | 4.536 |
| P（hemiaminal，job 1028 末帧） | 1.473 | 1.425 | 0.995 | 1.634 | 0.967 | 4.216 |

⇒ 四项距离在 I2→TS→P 上全部单调、方向一致：**不是 pseudo-saddle**。
- **但 (a) 只在「修正后的 watch pair」上成立**：题库把 map22 译成工作序 atom 24 是错位一个原子（atom 24 = 醇羟基 H，全程 O28–H24 0.967–0.984 Å 共价、距 O25 4.2–4.7 Å；真正的穿梭质子是 atom 27 → 羧基 O10）。平台已以 `reaction_center_distance_out_of_range` 拒收原申报（run ts_0024 rev 38）。工作序等价申报 = form (2,25)、break (2,4)、form (10,27)、break (25,27)。

### (b) 成分（记录项，不设阈值）
| 份额 | 数值 |
|---|---|
| 声明反应中心对（C2-O25 + C2-N4 两对原子）归一化份额 | **0.0714** |
| 该模内全部重原子份额 | **0.0420** |
| 最大单原子份额 | **0.8939 @ atom 27 (H)** |

- 最大份额落在 **H27 在水 O25 与羧基 O10 之间的转移自由度**（TS 上 O25–H27 1.1636 / O10–H27 1.2466，几乎等距）。
- 判定：**soft-mode-dominated**（质子穿梭主导），但**不是 spectator**（不是甲基转动/水取向）——它是本步化学必需的电荷补偿质子转移，只是不在题库的 watch pair 里。记录数值，不设阈值。

### (c) 交付链（同程序同方法同模型、纯电子能差、TS 与两端点皆原生日志）
- **未完成**。逐项：
  - TS 恰 1 虚频：有（**只读历史**，本 run 未产出）。
  - 双向 IRC 到达声明两端点：**无**（旧 run 双向各 10 点被 maxpoints 截断：irc.log sha 0f9679f9…，L9503 前向 / L18200 反向 `Maximum number of steps reached`，L18232 `Total number of points: 20`；本 run 的 IRC 阶段从未提交）。
  - 两端 Opt+Freq 0 虚频 + 身份：**历史上两端都有 0 虚频日志**（I2 = job 961；P = job 1028），但**本 run 未重算**，且产物端的新生手性中心 C2 的 CIP 未与题库声明比对。
- ⇒ 按主协调判定口径：**(a) 过、(b) 记录、(c) 未过 ⇒ candidate_only，不回填**（本边最终因题目被替换而整条归档）。

## ④ TS 日志绝对路径 + sha256 + 行号（只读历史证据）
- `/home/ly/Cloudra-mechanism-agent/ts/ts_0016/jobs/declaration_0007/frequency/frequency.log`
  sha256 = `c5ac84026e43c5155f2bf6e20787885f77662666e737ad4783e16036ae7291b9`
  - L1501 `****** 1 imaginary frequencies (negative Signs) ******`
  - L1510 `Frequencies --  -783.7914  23.6787  35.9094`（首组；Red. masses L1511 = 1.5559）
  - L1512 起为 mode 1 的 41 行原子位移矢量（AN + X/Y/Z）
  - E(RB3LYP) = **-939.295152015081 Ha**（L785）
  - 41 原子 / q0 m1（L107/L108）；Input orientation 末块起始 **L219**
- 本 run（ts_0024）**没有** TS 证据：ts_opt 在 declaration_0012 起跑，只有 7 个 SCF Done 点、无 `Stationary point found`、无 `Normal termination`，refine.log 476,368 B，最后写入 04:50，随后按 05:0x 指令 `ts_stop`（job 1094 `cancel_requested`）。

## ⑤ 两端点日志 + sha256 + 行号 + 虚频数（只读历史证据）
| 端点 | 日志 | sha256 | 能量行 | 模式数 / 虚频 |
|---|---|---|---|---|
| 起点极小值 I2（分母） | `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/runs/I2_optfreq/I2_optfreq.log` | `63dda25e04529e65920526304fb88755db9393e9c22bd3a6efb76eeee0af0d0e` | E = **-939.320655479**（L19183；opt 末步 L16950 同值） | **117 模 / 0 虚频**（`Frequencies --` 首行 L19879；Low frequencies L19869/70） |
| 产物 P（hemiaminal） | `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/runs/interm_c160/interm_c160_optfreq.log` | `1ec7e4c6388415d0859939238f4f96ec7739c0bbf1f985a28f4dd3c23b7dcec1` | 末 SCF L19117（-939.312626605） | **117 模 / 0 虚频** |
- 几何文件：I2 = `I2_min_v5.xyz` sha `9a6203ff67d9f0d95ad774e78b17bc397b22992f24cbcdf448f8c5558142ef2b`；P = `hemiaminal_1028_lastframe.xyz` sha `be789d5fd013d11ec84b295f4249c61616a8e4de21e129e319c13497faab572d`。
- 方法口径（三者一致）：Gaussian 16 `/home/ly/g16/g16`，`#p opt freq B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=DMSO)`。

## ⑥ ΔE 算式（纯电子能，无 ZPE/热校正）
```
E(TS)          = -939.295152015081 Ha   (frequency.log L785)
E(I2, 分母)    = -939.320655479    Ha   (I2_optfreq.log L19183)
ΔE‡ = E(TS) - E(I2) = +0.025503463919 Ha = +16.00 kcal/mol  (×627.5095)
```
- 同程序（G16）、同方法（B3LYP/def2SVP+GD3BJ+UltraFine+SCF=Tight+CPCM(DMSO)）、同 41 原子模型、同批次（2026-10-15）。
- **注意**：这两个能量都来自**旧只读日志**；本 run 未产出自己的 TS/freq，因此该值只作「候选值/量级」，不具备 (c) 项要求的「TS 与两端点皆原生日志 + 双向 IRC」支撑。

## ⑦ 仍缺哪一环（逐条，缺一不批）
1. **声明修正**：题库把转移质子写成 map22 → 工作序 atom 24，实际应为 atom 27（受体是羧基 O10，不是醇盐 O）。平台已在 rev38 拒收；主协调已落盘 `DECLARATION_FIX.md`（45 行，sha fde5f915…），题源侧由主协调改。
2. **本 run 自证 TS**：ts_prepare 的 ts_opt 未收敛（7 个 SCF 点后被调度终止）⇒ 无本 run 的恰 1 虚频 + 模归属。
3. **双向 IRC 到端点**：从未跑成。旧 run 是默认 maxpoints=10/侧被截断（缺的是点数，不是步长）；本 run 计划 40 点/侧 + stepsize=10，未执行。
4. **两端点 Opt+Freq（本批次）**：未重算，0 虚频与身份（CIP、质子归属、水是否完整）只由旧日志支撑。
5. **产物端 CIP 比对**：新生手性中心 C2 的构型需与题库声明核对（题库 out 字符串未指定 C2 构型，需先定声明口径）。
6. **回填动作**：按用户 05:0x 指令，HI1 被替换 ⇒ 本边不再回填，registry/JSON/md/tests 一律不动。

## ⑧ 回填影响面
- **本边不动**：`cloudra/benchmark/hard_registry/hi.py` 第 4 步 `barrier` 保持 `None`；HI1 task JSON 不重生成；md 不改；`tests/test_benchmark.py` 不动。
- 若将来重启并回填，影响面为：hi.py 第 4 步 `barrier` → 16.00（待本 run 自证后确认）、重生成 HI1.json、题源 md 对应行、守卫测试期望值——由主协调统一下笔，本道不写题库。

## 附：本道产物清单（归档）
- `gold_fill_20261018/HI1/HI1_E4/STATUS.md`（全道状态与时间线）
- `gold_fill_20261018/HI1/HI1_E4/PROVENANCE.md`（帧/距离表 + 平台限制证据第 6 节）
- `gold_fill_20261018/HI1/HI1_E4/analysis/mode_analysis.py`（虚频模 → 方向 + 三份额）
- `gold_fill_20261018/HI1/HI1_E4/analysis/geom_table.py`（三帧关键距离）
- `gold_fill_20261018/HI1/HI1_E4/analysis/smi_check.py`（申报 SMILES 身份自检）
- run 目录 `ts/ts_0024/`（declaration_0010 / declaration_0012 的输入与 refine.log，原样保留，不删不覆盖）
