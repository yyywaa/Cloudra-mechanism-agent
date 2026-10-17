# NY3_E1 · provided-guess provenance（relaxed scan, job 989）

- 作者：NY3 包整合 Coordinator **as_a396e35616564357**（本包唯一写权会话）｜时间：2026-10-17 06:5x +08:00
- 目的：为 ts_0007（NY3_E1 = RC → I1，OH⁻ 加成）提供**新的 TS 初猜**，替换 job 987 失败的 prep 初猜。

## 1 扫描作业（手工提交，非平台管线）
| 项 | 值 |
|---|---|
| job_id | 989（node-local，priority 0，8c / 10000 MB） |
| 输入 | /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NY3/E1/E1_scan_O1C4.gjf，sha256 `8e2a37eb4e745d4d8196899d96183a67aa08ee3057c78615577424794cb0a1cf` |
| 原生日志（只读，未改写） | /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NY3/E1/E1_scan_O1C4.log，sha256 `62ac90e3732663dc82de1339fe1623b3e3457a4528d2d1f92d8bf3748442dca4`（40686 行） |
| route | `#p opt=modredundant b3lyp/def2svp empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=water)`，0 1 |
| 起点 | job 967（ts_0007 candidate_opt 末帧）= RC 极小值，E(RB3LYP) = −466.986564979 |
| 扫描坐标 | `B 2 6 S 12 -0.1` = d(O1···C4) 2.803 → 1.603 Å，13 点（1-based 反应物序：2 = O1，6 = C4） |
| 终止 | **Error termination via Lnk1e in /home/ly/g16/l9999.exe**（L40683）；原因行 `-- Number of steps exceeded, NStep=  45`（L40448）即**第 5 个扫描点优化步数耗尽** |

**纪律声明**：这是 Gaussian 自身的收敛失败（l9999），**不构成「NY3_E1 无鞍点」证据**；与 job 987（ts_opt l9999，NStep=46）同类，属「初猜/搜索未收敛」。

## 2 已收敛扫描点（判据 = `Optimization completed.`，能量取该点前最后一个 `SCF Done`）
| 点 | d(O1···C4)/Å | E(RB3LYP)/Ha | 能量行 | ΔE vs RC/(kcal/mol) | 坐标块行 |
|---|---|---|---|---|---|
| 1 | 2.803 | −466.986565136 | L1513 附近（该点末次 SCF） | +0.00 | L2076–2086 |
| 2 | 2.703 | −466.986190365 | 点 2 末次 SCF | +0.24 | L9061–9071 |
| 3 | 2.603 | −466.984669315 | 点 3 末次 SCF | +1.19 | L13810–13820 |
| 4 | 2.503 | **−466.981571100** | 点 4 末次 SCF | **+3.13** | **L19384–19394** |
| 5（**未收敛**） | 2.403（末帧） | −466.984727401（末次 SCF，非驻点） | L40314 | +1.15（**不作证据**） | L40543–40553 |

- 收敛点计数 = 4（`Optimization completed.` @L2418 / L9429 / L14164 / L19754）；第 5 点以 NStep=45 截断。
- 剖面形态：沿 d(O1···C4) 缩短方向上，**已收敛区间单调上升**（+0.24 → +1.19 → +3.13），第 5 点未收敛帧回落（+1.15）⇒ 在 **≈2.40–2.55 Å** 区间存在鞍点区间的迹象；未经 TS 优化不得当作能垒值。
- 能量口径：纯电子能（无 ZPE/热校正），**同一批 Gaussian 16 作业内部相减**；RC 参考 = job 967 末帧 −466.986564979（本扫描第 1 点独立复现为 −466.986565136，差 1.6e-7 Ha）。
- 引擎偏差：本批用 **Gaussian 16**（B3LYP/def2SVP + GD3BJ + Int(UltraFine) + SCF=Tight + CPCM(Water)）替代既有 gold 档的 ORCA，**不得与历史 ORCA 值混减**。

## 3 provided guess 的取法
- 取**能量最高的已收敛点**（第 4 点，d = 2.503 Å，ΔE = +3.13 kcal/mol）之末帧坐标（日志 L19384–19394）作为 TS 搜索起点：
  - 文件：`gold_finish_20261015/NY3/E1/guess_scan_p04_d2503.xyz`（11 原子）
  - 原子序（1-based，**与 ts_0007 当前 reactant 结构序一致**）：1 Na｜2 O1｜3 H6｜4 C2｜5 O3｜6 C4｜7 O5｜8-10 H(Me)｜11 H(C4)
- 该几何**本身不是 TS**、也不是极小值之外的任何结论点：它只作 OptTS 的起始结构；其能量不得作为能垒。
- 生成方式：坐标直接取自原生日志 Standard orientation 块（未手键、未插值）；guess 文件与日志块逐位一致。

## 4 证据链与后续
- ts_resume(ts_0007) 只改 guess（provided，xyz_path = 上面的 guess，evidence_refs = 本文件 + 原生日志）→ 管线自动推进 ts_opt → freq → IRC → 两端点 Opt+Freq。
- E1 参考极小值登记：起点 RC = job 967 末帧 E = −466.986564979（0 虚频待端点 Opt+Freq 确认）；产物端 I1 = job 985 末帧 E = −467.004842485（0 虚频待确认）。
