# O2 (c) 分离反应物基准 —— 两份单体 Opt+Freq 结果追记

落盘：2026-10-17 15:39 CST（会话 **as_6fdd1a4300b74a9f**，small_mol）
性质：**追记文件**（report §R72 起引用），**不回填 NY3 任何值**、不改 §14 / yo.py / NY3.json。

> 口径声明（必读）
> 1. **(c) 分离基准 = −346.618015209 Ha（纯电子能、无热校正）** = E(DMDO,min) + E(C2H4,min)。
> 2. **不得与 (a) 受约束复合物口径混用/换算**；(a) 的基准点是受约束点、非极小，两套数值不可互相转换或拼接。
> 3. **本项目未进入 `ts_opt`**（`ts_0018` 在 `candidate_opt` 阶段 NStep=91 截断后 blocked）⇒ **没有 TS 能量 ⇒ 本轮 ΔE‡ 不可给**。

## 1. 乙烯 C2H4（job 1065）
- log：`/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NY3_R2/fallback_O2/monomers/ethene_optfreq.log`
  - **sha256 `14871fc8fae6da46ff0b5fbc67e5279c0a59e1a0e9eaa198a5f156a2807576b1`**，**2805 行**
- 输入：`…/monomers/ethene_optfreq.gjf` sha256 `12eb10f47316a9c235a90115fc0bd183e1e38a7ddecccebb980267c3b3a96633`（15 行）
- 关键行号：
  - opt 完成/驻点：**L1738** `Optimization completed.`、**L1739** `-- Stationary point found.`
  - opt 终止：**L1910** `Normal termination of Gaussian 16 at Sat Oct 17 15:37:15 2026.`
  - freq 段：**L2685** `Optimization completed.`、**L2686** `Stationary point found.`、**L2805** `Normal termination … 15:37:23`
  - 末判据（表头 **L2679**）：**L2680** Max Force 0.000018/0.000450 YES；**L2681** RMS Force 0.000010/0.000300 YES；**L2682** Max Disp 0.000047/0.001800 YES；**L2683** RMS Disp 0.000030/0.001200 YES
  - `Frequencies --` **4 组 = 12 模 = 3N−6（N=6）**：**L2379 / L2392 / L2405 / L2418**
  - **无 `imaginary` 行 ⇒ 0 虚频**；最低真实振动模 **819.5592 cm⁻¹（L2379）**，L2370 `Low frequencies --- 819.5592 962.9676 974.9181`
  - **E(C2H4) = −78.5365637480 Ha**：**L2169** `SCF Done: E(RB3LYP) = -78.5365637480 A.U. after 1 cycles`（L1601 同值）

## 2. DMDO C3H6O2（job 1066）
- log：`/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NY3_R2/fallback_O2/monomers/dmdo_optfreq.log`
  - **sha256 `092b044648a3e760b2231ab30f21cbe512f0b405769a5b8d86aa2d44c213a7aa`**，**4032 行**
- 输入：`…/monomers/dmdo_optfreq.gjf` sha256 `4d689d467118f2c96dda2a7f5d0b851a1ca1cddc855474cbdb4564fff55007cd`（20 行）
- 关键行号：
  - opt 完成/驻点：**L2441** `Optimization completed.`、**L2442** `-- Stationary point found.`
  - opt 终止：**L2700** `Normal termination … 15:38:07`
  - freq 段：**L3772** `Optimization completed.`、**L3773** `Stationary point found.`、**L4032** `Normal termination … 15:38:26`
  - 末判据（表头 **L3766**）：**L3767** Max Force 0.000041/0.000450 YES；**L3768** RMS Force 0.000009/0.000300 YES；**L3769** Max Disp 0.000453/0.001800 YES；**L3770** RMS Disp 0.000189/0.001200 YES
  - `Frequencies --` **9 组 = 27 模 = 3N−6（N=11）**：**L3271 / L3289 / L3307 / L3325 / L3343 / L3361 / L3379 / L3397 / L3415**
  - **无 `imaginary` 行 ⇒ 0 虚频**；最低真实振动模 **162.6075 cm⁻¹（L3271）**
  - ⚠️ **L3261** `Low frequencies --- -15.7561 -11.9517 -7.9761 -0.0012 -0.0012 0.0005` 是 Gaussian 固定的 **6 个平动/转动探针**，**不是振动模、不是虚频**（勿误读）
  - **E(DMDO) = −268.081451461 Ha**：**L3019** `SCF Done: E(RB3LYP) = -268.081451461 A.U. after 1 cycles`（opt 末帧 **L2304** 同值）

## 3. (c) 分离基准合计
| 项 | Ha | 行号 |
| --- | --- | --- |
| E(DMDO, min) | −268.081451461 | dmdo L3019 (= L2304) |
| E(C2H4, min) | −78.5365637480 | ethene L2169 (= L1601) |
| **E(分离基准) = 两者之和** | **−346.618015209** | 需在同一级别内相减 |
- 级别（两份逐字相同）：`B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=Water)`，charge 0 / mult 1
- 用法：`ΔE‡ = E(TS) − (−346.618015209 Ha)`；**本轮无 TS 能量，故 ΔE‡ 不可给**。

## 4. 仅供比对、不得引用为结论
- `ts_0018` 的 `candidate_opt`（job 1064，**NStep=91 截断，未收敛**）末 SCF = **−346.621069819 Ha（seed-opt.log L51807）**，比分离基准低 **−0.00305461 Ha = −1.9168 kcal·mol⁻¹** ⇒ 只说明弱复合物有 ~1.9 kcal/mol 色散束缚，**该几何未收敛，不作任何数值结论**。
- `ts_0018` 现态：**blocked / rev 11 / `conformer_optimization_failed` / needs `conformers.reactant`**，**未进入 `ts_opt`**；`ts_0017` 废弃、零作业。
