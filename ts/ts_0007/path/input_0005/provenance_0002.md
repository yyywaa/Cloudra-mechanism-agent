# NY3 / E1（RC→I1 O1–C4 加成）TS 初猜候选 · provenance

生成时刻（本机）：2026-10-17T08:19+08:00 ｜ 作者：small_mol 道 as_f99001ff9213455c
范围：**仅几何初猜**。本文件不含任何能量/能垒数字；候选几何**不是**松弛剖面点，除 job 1015（GFN2-xTB/ALPB 受约束扫描）与（若获批）1 个受约束预优化之外没有任何松弛证据。

## 0 原子序（1-based，与 ts_0007 工作序一致；全部 11 原子，q0/m1，C2H5NaO3）
1 Na ｜ 2 O1（羟基 O，带 H6）｜ 3 H6 ｜ 4 C2（甲氧基 CH3 的 C）｜ 5 O3（甲氧基 O）｜ 6 C4（羧基 C）｜ 7 O5（羰基 O）｜ 8/9/10 H(Me) ｜ 11 H(C4)

## 1 源结构（绝对路径 + sha256）
- RC 极小值（job 967）：`gold_finish_20261015/NY3/E1/rc_dft_min_working_order.xyz` sha256 `449cad42aa779d00dd0f454c5b0eb93a9b4bdb771d6de8772cf9912aa7adef68`
  （取自 ts/ts_0007/jobs/declaration_0001/candidate_opt/optimized_seed.xyz sha256 `fb6f29c5bbc098007632979c3b1361194e1efc1ee827fc2c83827a0d49cafa7d`，E = −466.986564979）
- IDPP 帧：`gold_finish_20261015/NY3/E1/interp/img_04.xyz` sha256 `44b4495200a345189e1402fe600332465b60ef741f6620bab99458fa9d7496fb`

## 2 测量方法（可复算）
- 距离/键角/二面角由 xyz 坐标按公式自算（欧氏距离；键角 = 两键向量夹角；二面角 i-j-k-l = atan2 约定，−180…+180）；BD 角定义 = ∠O1–C4–O5（顶点 C4）。
- 交叉核对：`internal_coordinates(mode=analyze)` 的成键距离与 Rotatable Dihedrals（本文件 §4 引用其原文数值），以及 `internal_coordinates(mode=transform)` 的 `operations_applied` 回执。
- 符号约定：本文件用自算约定给 D(8,4,5,6) = −60.4°（RC）；**工具 analyze 对同一构象报 τ = +60.4°**（同一取向，仅约定不同），两者等价，勿当成漂移。

## 3 候选表（全部 1-based 工作序；长度 Å，角度 °）
| 文件 | sha256 | 构造 | d(O1···C4) | C4–O3 | C4=O5 | O1–H6 | Na–O1 | Na–O5 | Na–O3 | BD | D(8,4,5,6) | D(1,2,3,11) | ∠Na-O1-H6 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RC（基准） | 449cad42… | job 967 DFT 极小值 | 2.803 | 1.329 | 1.222 | 0.965 | 2.093 | 2.409 | 4.258 | 96.1 | −60.4 | −152.4 | 145.4 |
| `e1_tsguess_rigid_swing_d230.xyz` | `523392c1735a83f670566401e3e18a51387b13899d254fb3c4aceabc82ff6e36` | RC + 绕 Na 刚性摆动 {O1,H6}，Δθ = 14.12° | **2.300** | 1.329 | 1.222 | 0.965 | 2.093 | 2.409 | 4.258 | 98.5 | −60.4 | −156.5 | 145.4 |
| `e1_tsguess_rigid_swing_d220.xyz` | `95b766605cd12732924e1b39fe446017b36a71aa83da7a9eec629ed0f2d69877` | 同上，Δθ = 16.87° | **2.200** | 1.329 | 1.222 | 0.965 | 2.093 | 2.409 | 4.258 | 98.8 | −60.4 | −157.3 | 145.4 |
| `e1_tsguess_img04_retorsion.xyz` | `3af1c8c22961c181dec377b735d12dc102c4dae035a112065bc27a4861a6d98a` | img_04 骨架 + 甲基/羟基二面角复位到 RC（工具 transform） | 2.230 | 1.386 | 1.249 | 0.967 | 2.732 | 2.246 | 3.922 | 110.3 | −60.4 | −152.4 | 102.9 |
| （别名副本）`e1_tsguess_img04_retorsion_tool.xyz` | `2a03d85bf258aff509c67156b743274e59f0e9be434c6167db7c54a92eecfcae` | 同上、字节级内容相同（仅注释行不同） | 2.230 | 1.386 | 1.249 | 0.967 | 2.732 | 2.246 | 3.922 | 110.3 | −60.4 | −152.4 | 102.9 |

### 3.1 逐项对判据（协调道确认的择优阈值）
硬判据 ① d(O1···C4) ∈ 2.10–2.40 Å；② |ΔD_Me| ≤ 10° **且** |ΔD_OH| ≤ 15°（同时）；③ Na–O1 ≤ 2.60 Å 且 |Δ∠Na-O1-H6| ≤ 25°；参考 BD ∈ 100–115°。

| 候选 | ① d | ② ΔD_Me / ΔD_OH | ③ Na–O1 / Δ∠ | BD（参考） | 判定 |
|---|---|---|---|---|---|
| rigid_swing_d230 | 2.300 ✔ | 0.0 / **+4.1** ✔✔ | 2.093 ✔ / 0.0 ✔ | 98.5（低于区间 1.5） | **①②③ 全满足**，仅 BD 偏低 |
| rigid_swing_d220 | 2.200 ✔ | 0.0 / **+4.9** ✔✔ | 2.093 ✔ / 0.0 ✔ | 98.8（低 1.2） | **①②③ 全满足**，仅 BD 偏低 |
| img04_retorsion | 2.230 ✔ | 0.0 / **0.0** ✔✔ | **2.732 ✗** / **42.5 ✗** | 110.3 ✔ | **①②满足，③不满足** |

## 4 工具独立读数（`internal_coordinates(mode=analyze)`，各候选文件本体）
- rigid_swing_d230：`Fragments: 1`；`r(O2-C6)=2.300 Å [forming (distance heuristic)]`；`r(O2-H3)=0.965`；`r(O5-C6)=1.329`；`r(C6-O7)=1.222`；`r(Na1-O2)=2.093 [bonded]`；`r(Na1-O7)=2.409 [bonded]`；`r(Na1-O5)=4.258 [far]`；`H8-C4-O5-C6 τ=60.4°`；`Bond anomalies: 2  Angle anomalies: 8`（与 RC 同数：2/8）
- rigid_swing_d220：同上，唯 `r(O2-C6)=2.200 Å`；`Bond anomalies: 2  Angle anomalies: 8`
- img04_retorsion：`r(O2-C6)=2.230`；`r(Na1-O2)=2.732`；`r(Na1-O7)=2.246`；`H8-C4-O5-C6 τ=60.4°`；`Bond anomalies: 2  Angle anomalies: 5`

## 5 构造参数（供 ts_resume 的 evidence_refs 直接引用）
### 5.1 刚性摆动族（d230 / d220）
- 摆动轴：过 Na（原子 1）、方向 `n = unit((O1−Na) × (C4−Na))`，即 Na–O1–C4 平面法向；实测 `n = (0.0049, −0.0194, −1.0000)`（≈ −z；该分子在 RC 基本平面，全部原子方向与 n 的夹角 79.4–99.9°）。
- 摆动对象：原子 {2 O1, 3 H6} **整体刚体旋转**（Rodrigues，右手法则绕 n）；其余 9 个原子完全冻结 ⇒ Na–O1、Na–O5、Na–O3、C4–O3、C4=O5、O1–H6、甲基取向、羟基滚转、∠Na-O1-H6 全部逐位等于 RC。
- 角度由余弦定理求：r1 = |Na–O1| = 2.093、r2 = |Na–C4| = 2.931、θ = arccos((r1²+r2²−d²)/(2 r1 r2))。RC θ = 65.4° → d = 2.40/2.30/2.20/2.10 Å 对应 θ = 54.0/51.2/48.5/45.8°（Δθ = 11.36/14.12/16.87/19.61°）。
- 落到文件的只有 2.30（Δθ 14.12°）与 2.20 Å（Δθ 16.87°）两帧；2.40/2.10 只算未落盘。
- 副产物：因为摆的是 {O1,H6} 整体、且 H6 基本位于 Na–O1–C4 平面内，D(1,2,3,11) 只漂 +4.1/+4.9°（新值 −156.5/−157.3°），未单独复位。
### 5.2 img04_retorsion（工具原生）
`internal_coordinates(mode=transform, input_path=…/interp/img_04.xyz, output_path=…/e1_tsguess_img04_retorsion.xyz)`，operations 按序：
1. `{"type":"rotate","axis_atoms":[4,5],"atoms":[8,9,10],"degrees":−41.12564473990092}`（甲氧基甲基绕 C2–O3 轴复位）
2. `{"type":"rotate","axis_atoms":[2,1],"atoms":[3],"degrees":+56.21092622889552}`（H6 绕 O1→Na 轴滚转复位）
工具回执：`Applied 2 transform operation(s). Validation after transform: 2 bond anomalies, 5 angle anomalies (before: 2 bond, 5 angle); 0 new, 0 resolved.`
注意第 2 步的角度是**数值求解**得到的（该旋转角与 D(1,2,3,11) 不是 1:1；会话内先用 ±探头标定、再用扫描+二分求根，残差 < 0.01°）。

## 6 使用方式与已知局限（必须随候选一起引用）
1. 三个候选都只是 **TS 初猜几何**：没有 SCF、没有梯度、没有频率，**不得**引用任何能量；不得据此写 ΔE‡。
2. rigid_swing_* 两帧由**会话内刚体旋转代码**机器生成（参数见 §5.1；非手抄、非记忆转录），因此平台会给出 “suspected handwritten coordinates” 提示，且它们**没有 compute record** ⇒ 只能当 provided guess；若评审要求“坐标必须来自工具/compute record”，请改用 img04_retorsion（工具 native，有 operations_applied 回执）或等 job 1015 的原生帧。
3. 三帧都不是**松弛**剖面点：除反应坐标外其余自由度来自 RC（rigid 族）或 IDPP 插值（img04 族）⇒ 它们与真实 TS 的差别需由 1015 的受约束松弛帧或管线自身的 OptTS 来暴露。
4. BD 角：rigid 族 ≈98.5°（只比 RC 的 96.1° 开 2.4°）——因为摆动刻意保住了 Na 桥与羟基取向；IDPP 同距离帧是 110.3°。若 OptTS 需要更接近 Bürgi–Dunitz 区间的接近角，img04_retorsion 在这一项更优，但它牺牲了 ③（Na–O1 2.732、∠Na-O1-H6 102.9°）。
5. 未测量/不主张：E1 的 ΔE‡、E1 是否存在独立鞍点、以及这三个初猜哪个能收敛到真鞍点 —— 全部未知；job 1004/1010 的甲基转子 pseudo-saddle 只说明“2.503 Å 帧 + 该取向”不够，不构成“E1 无鞍点”。
6. 不与任何历史 ORCA 值、也不与 xTB 能量混用。
