# HI1_EM1（副面通道）· 新 TS run 的种子 provenance（job 1032 收敛鞍点几何）

日期：2026-10-18 03:0x CST。本文件只是**几何种子 provenance**（+ 频次读数登记），不是 QM 验收；
不代表已回填、不代表 IRC 连通性、不代表端点身份。所有原生文件只读引用，未改写。

## 1 本 run 的原子序种（写清）

**工作序 = ts/ts_0012/declaration_0002 的 bound 序（41 原子，1-based，含显式氢）**。
它与 ORCA job_51 的 source 序逐位一致（元素序列 C C C N C C C C C O O + 13H + O H H + O C + 苯环C×6 + H + 5H，
见 `gold_finish_20261015/HI1/E2EM1/build/ATOM_ORDER_AND_WATCHPAIRS.md` §2；实测：
`build/TS_EM1_job1032_final.xyz` 与 `gold_finish_20261015/HI1/E2EM1/build/I1_S_from_job59.xyz` 元素序列完全相同）。

关键原子（1-based 工作序 → 题源 atom-map 标签）：
| 工作序 | 元素 | 身份 | map |
|---|---|---|---|
| 1 | C | C3 烯胺 β-碳 | map3 |
| 2 | C | C2（烯胺/亚铵碳） | map2 |
| 4 | N | 脯氨酸 N20 | map20 |
| 8 | C | 脯氨酸 Cα（须 S） | map16 |
| 25 | O | 水 O | map4 |
| 28 | O | O5（苯甲醛羰基 O = 醇盐 O） | map5 |
| 29 | C | C6（苯甲醛羰基 C = aldol 手性碳，本通道须 R） | map6 |

（题源 declare 口径的存储序 = 工作序 − 1（0-based）：`reaction_center = [[0,28],[1,3],[1,0],[27,28]]`，
与 `ts/ts_0012/process.json` input.reaction.reaction_center 逐字节一致。本次提交按 ts_prepare 契约用
1-based 申报：`[[1,29],[2,4],[2,1],[28,29]]`，两者为同一组键对。）

## 2 种子几何来源（只读原生日志）

| 项 | 值 |
|---|---|
| 来源日志 | `ts/ts_0012/jobs/declaration_0002/ts_opt/refine.log` |
| sha256 | `66691e0e68e9044d7d10e45e8953e6c5468efee3d361713d3e34d7bfbb2b4241` |
| 收敛证据 | L24549 `Optimization completed.`、L24550 `-- Stationary point found.`（第 24 步，上限 239） |
| 末帧能量 | L24183 `SCF Done:  E(RB3LYP) =  -939.283734374` |
| 正常终止 | L25650 `Normal termination of Gaussian 16 at Sat Oct 17 12:00:41 2026` |
| 导出产物 | `gold_fill_20261018/HI1/HI1_EM1/build/TS_EM1_job1032_final.xyz`（41 原子，"opt step=24" 帧） |
| xyz sha256 | `663fe23166bb54de96c2698a43ae3d6207457be7b61d55a10a5972d8f29a3fce` |
| 冻结副本 | `evidence/refine_frozen.log`（sha 同上，只读 444） |

## 3 对应频次读数（只作方向/份额登记，验收另算）

`ts/ts_0012/jobs/declaration_0002/frequency/frequency.log`，sha256
`a471aa7b6c2b34b7ccff44a98bbcd0dee7c4ae5f436653fe79f094f44fe53a65`（冻结副本 `evidence/frequency_frozen.log`）：

- L857 `SCF Done:  E(RB3LYP) =  -939.283734374`（= ts_opt 末次 SCF，几何一致）
- L1539/1540 `Low frequencies --- -314.2862 -8.6958 -6.4812 -0.0010 -0.0007 -0.0001` / `5.8163 33.6702 44.0403`
- L1541 `******    1 imaginary frequencies (negative Signs) ******`（恰 1 虚频）
- L1550 `Frequencies --   -314.2861   33.5499   44.0361`；共 39 个 Frequencies 行 = 117 模
- L5340 `Normal termination of Gaussian 16 at Sat Oct 17 12:19:43 2026`
- q0 / m1（L111），NAtoms=41

虚频模（-314.2861 cm-1）方向与份额（`build/analyze_mode.py` 由上述日志重算，1-based 工作序）：
- 方向（沿键轴净位移投影，负 = 缩短）：C3–C6(1,29) **−1.109 → 缩短**；C2=C3(2,1) **+0.166 → 拉长**；
  C6=O5(28,29) **+0.177 → 拉长**；C2=N20(2,4) −0.070 → 缩短。与题源 bond_changes 同向。
- 份额：声明反应中心原子 {1,2,4,28,29} 合计 **0.6665**；heavy（20 个 C/N/O）**0.6951**；
  最大单原子 = 原子 1（C3）**0.3282**（落在反应中心，不是 spectator）；第 2 位原子 29（C6）0.2880。
- 该驻点 d(1,29)=1.8791 Å、d(2,1)=1.4291、d(28,29)=1.2917、d(2,4)=1.3284 Å。

## 4 本 run 之前的 IRC 失败（只读，不作证据）

`ts/ts_0012/jobs/declaration_0002/irc/irc.log` sha256
`dfc4d3ec2bba6c84e634eeb7105fb48fe0481969c7e61b73413fb2ed47ff31e3`：
正向只跑完 10 点（G16 默认 MaxPoints=10/方向）L8405 `Maximum number of steps reached.`；
反向第 3 点起 `Delta-x Convergence NOT Met` 连续 20 次，L25166 `Error termination via Lnk1e in l123.exe`。
⇒ 原 run 的 IRC 无连通性结论；本次新 run 在 verification.irc 里显式给 MaxPoints/StepSize。

## 5 本 run 的方法口径（与 ts_0012 同一 profile）

Gaussian 16（/home/ly/g16/g16）；B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) +
SCF=Tight + SCRF=(CPCM,Solvent=DMSO)；q0/m1；8 cpu / 10240 MB；纯电子能（无 ZPE/热校正）。
ΔE‡ 参考态固定 **job 924 = (S)-HI1_I1 极小值 −939.308218263 Eh**（不得用工作流自身 reactant 端点替代，
也不得用 job 1000 的伸展构象 −939.302926757）。
