# NY3 E1 · 反向扫描 pt6（帧 A）provenance —— ts_0007 候选 guess，尝试 1
生成者：NY3 写权会话（as_a396e35616564357）；生成时刻：2026-10-17 09:51:51 CST

## 1 来源（原生日志、未改写）
- 日志 `gold_finish_20261015/NY3/E1/E1_revscan_O1C4.log` sha256 **caf70be3011b1b5c05aabbb4eee4f7838b1ef980ed1c7f3e13cd91a04accfb26**（51866 行，`Normal termination of Gaussian 16 at Sat Oct 17 09:48:15 2026.` @L51866；**9/9 点全部 `Optimization completed.`**）
- 输入 `E1/E1_revscan_O1C4.gjf` sha256 **7c6f8bc99918eac42567b2960b9610ee762411464124c51c43f32487673a5f21**；job 1023（主协调提交），route `opt=modredundant b3lyp/def2svp empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=water)`，扫描 `B 4 5 S 8 0.15`（1.4271→2.6271 Å）
- **本帧点 pt6**：约束行 `! R9 R(4,5) 2.1771` @**L44344**；`Optimization completed.` @**L44328**（四项判据 @L44323–44326 全 YES）；**E = −466.987210589 Ha @L44170**
- 几何抽取：该点收敛末帧 `Input orientation:` 块（块首 @**L43915**）——**索引安全口径**（输入原子序；不使用 Standard orientation 的声明索引）
- 抽取脚本：`coord_export_revscan_frame_v2.py` sha256 **91b28f0cf5f82471478ed9b15b5647bac4571d2bab033dc87601d4e5b1411019**（v2：注释中的约束值由几何 d(4,5) 反算，非硬编码）
- **本帧 = 受约束弛豫扫描点的收敛几何；非内插、非手工构造、未手改数值。**

## 2 Na⁺ 分支切换事实（job 1023 剖面）
- **支-I1 = p1–p5（含产物 I1）**：Na–O1 = 3.802 / 3.867 / 3.893 / 3.944 / 4.023 Å（Na⁺ 远离羟基 O）；Na–O3 = 2.294→2.395、Na–O5 = 2.206→2.277（Na⁺ 桥联甲氧基 O3 + 羰基 O5）。
- **支-RC = p6–p9（RC 属此支）**：Na–O1 = 2.151 / 2.136 / 2.129 / 2.123；Na–O5 = 2.307 / 2.343 / 2.380 / 2.425；Na–O3 = 3.545 / 3.544 / 3.540 / 3.528（Na⁺ 桥联羟基 O1 + 羰基 O5）。
- RC（job 967 末帧 `E1/rc_dft_min_working_order.xyz`，sha 449cad42aa779d00dd0f454c5b0eb93a9b4bdb771d6de8772cf9912aa7adef68）：Na–O1 2.093 / Na–O5 2.409 / Na–O3 4.258 ⇒ **与 pt6 同支（支-RC）**。
- ⇒ p5→p6 是**同一约束值区间的 Na⁺ 配位分支切换**，不是连续脊线；**支-I1 的峰（p5，+22.232 vs I1 / +10.756 vs RC）不是 RC→I1 的 ΔE‡**。
- 命名口径（主协调统一）：支-I1（p1–p5）/ 支-RC（p6–p9）；本会话早前 p5 provenance 中的「支 A / 支 B」分别对应「支-I1 / 支-RC」。

## 3 导出件（同一几何、两套原子序）
| 文件 | 原子序 | sha256 |
|---|---|---|
| `E1/e1_tsguess_revscan_p6_reactantorder.xyz` | reactant/工作序（guess 用；= ts_0007 规范序 1 Na,2 O1,3 H6,4 C2,5 O3,6 C4,7 O5,8-10 H(Me),11 H(C4)） | **9ee4e84748af8b4c1e78af813b7eb5de64164530ab06c724cc627117942b5b66** |
| `E1/e1_tsguess_revscan_p6_productorder.xyz` | job .gjf / product 序 | **07ce886fc97dd0bf97f29c965e8f09769a5c333508b755f0f9c0da6d248081a3** |
- 映射 r2p = [1,5,11,2,3,4,6,7,8,9,10]（= atom_map [1,4,5,6,2,7,8,9,10,11,3]）；两序互查逐原子最大偏差 0.00e+00 Å；d(O1–C4) = 2.177138（两序一致）、Na–O1 = 2.151408（两序一致）。

## 4 关键读数（与主协调 / E1 道对「帧 A」的描述逐项一致）
C4–O1 = **2.177138 Å**；Na–O1 = **2.151408**；Na–O5 = **2.307**；O1–H6 = **0.967**；E = −466.987210589 Ha = **+11.062 vs I1 / −0.409 vs RC**（kcal/mol）。

## 5 口径（主协调 R26.3/R26.5/本封要求）
- (a) **pt6 是帧 A 上的受约束扫描点**；其 −0.409 kcal/mol（vs RC）只是**同一约束值下的约束点能量**，**不是能垒、也不是「存在更低 RC 型极小值」的证据**（需独立未约束 Opt+Freq，本轮未授权）。
- (b) E1 = RC→I1，ΔE‡ 只相对**声明的起点极小值 RC = job 967（−466.986564979）**，同程序同批（Gaussian 16 / B3LYP/def2SVP GD3BJ CPCM(water)）；job 1023 剖面任何点（含 pt6、p5）都只是**候选/下界**；不与 xTB 或历史 ORCA 值混减。
- (c) 支路结论：pt6 与 RC 同支（支-RC：Na⁺ 桥联羟基 O1 + 羰基 O5；H 归属 H6 在 O1 不变：O1–H6 0.965 vs 0.967；羟基二面角 D(H6-O1-C4-O3) RC 18.10° vs pt6 119.21°，属同一配位型的不同构象）⇒ **同一中间体的另一构象/相邻约束点，非旁路支**。

## 6 来源帖
`evt_85d4fc1e589c45bf`（E1 道分支分析）、`evt_750afe4d10194b5f`（主协调：帧 A 优先、p5 作第二次）、本会话对 p5 帧的登记（`E1_REVSCAN_P5_FRAME_PROVENANCE.md` sha 73469a5ff77ea59d972bfb0409fff2cb69c4fc469b11c6b57ba551ada3d5d724，保留作尝试 2 材料）。

## 7 用途与限制
- 用作 ts_0007 候选 guess（`kind=provided`，reactant 序 xyz），主协调授权的**尝试 1**（两次上限）。
- 不构成 ΔE‡；不构成「鞍点存在 / 不存在」的结论。
