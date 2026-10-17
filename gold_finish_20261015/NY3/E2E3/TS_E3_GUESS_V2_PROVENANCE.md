# TS_E3_GUESS_V2_PROVENANCE — NY3 E3（I2 → P）质子转移 TS 初猜

- **文件**：gold_finish_20261015/NY3/E2E3/ts_e3_guess_v2.xyz
- **sha256**：3ccf834e473dc4f6f0e19b1ad1502d9e0f026ea602d8957b3c5b4fdc4fbfa43f（11 原子，txt/xyz）
- **序（1-based）= i2 序**：1 Na｜2 C2（甲基 C）｜3 O3（甲醇/甲醇盐 O）｜4,5,6 H(甲基)｜7 C4（甲酸 C）｜8 O5（甲酰 O）｜9 O1（羟基 O）｜10 H(C4)｜11 H6
  = 与 prep/i2.xyz、E2E3/*.gjf、E2E3/i2_min_candA.xyz、E2E3/p_min_ref.xyz **同序**
  i1 序对照（prep/i1.xyz、E2E3/i1_dft_min_ref.xyz）：1 Na｜2 C2｜3 O3｜4 C4｜5 O1｜6 O5｜7,8,9 H(Me)｜10 H(C4)｜11 H6
  对应关系：Na=i2#1=i1#1；C2=i2#2=i1#2；O3=i2#3=i1#3；C4=i2#7=i1#4；O5=i2#8=i1#6；O1=i2#9=i1#5；甲基 H=i2#4,5,6=i1#7,8,9；H(C4)=i2#10=i1#10；H6=i2#11=i1#11

## 来源与构造链（run / job / 日志行）

- **无 QM 作业**：由化学工具 `ts_guess(mode="interpolate", interp_method="idpp", n_images=11, atom_map=[1..11])` 生成 IDPP 图像路径。
- 端点 A（reactant，I2 端）：E2E3/i2_min_candA.xyz｜sha256 **1715f6d7d77e93bb5200a71b23db31fc84cb45564b1d48f6bbab2e7ee3c0ef85**
  = 本轮判定的 DFT **I2 极小值**（job 990：0 虚频，Normal termination @ gold_finish_20261015/NY3/E2E3/freq_i2_candA/i2_candA_freq.log:1470，E = -466.986020418 @同文件:512）
- 端点 B（product，P 端）：E2E3/p_min_ref.xyz｜sha256 **f69ef3c9215d95fe31a17d4cfecc9a2a0bf111fd932894bf0f236a985348f4ea**
  = DFT **P 极小值**（job 994：Optimization completed/Stationary point found @ gold_finish_20261015/NY3/E2E3/p_optfreq/p_ref_optfreq.log:10591-10592，0 虚频，E = -467.045937735 @同文件:10443）
- atom_map = [1,2,3,4,5,6,7,8,9,10,11]（两端点同为 i2 序，恒等映射）；watch_pairs（i2 序）= [[9,11],[3,11],[7,3],[9,3]]
- IDPP 图集目录：E2E3/ts_interp_e3/（img_00.xyz … img_10.xyz，各 575 B）

## 选帧依据（实测距离表，ts_guess 返回原文）

```
frame        O9-H11        O3-H11         O3-C7         O3-O9
   0        0.9723        5.0558        4.5677        4.1936
   1        1.0354        4.6799        4.4372        4.0230
   2        1.0988        4.2643        4.3033        3.8567
   3        1.1620        3.8548        4.1703        3.6996
   4        1.2252        3.4455        4.0346        3.5451
   5        1.2883        3.0361        3.9003        3.3930
   6        1.3513        2.6259        3.7640        3.2432
   7        1.4139        2.2179        3.6319        3.0967
   8        1.4757        1.8124        3.5000        2.9534
   9        1.5356        1.4094        3.3692        2.8077
  10        1.6053        1.0092        3.2170        2.6078
```

- 工具默认候选 = **img_06**（口径："watched pair O3–H11 跨过端点中点"，即 O3–H6 从 5.056 到 1.009 的中点 ≈ 3.03）。**本交付不采用 img_06**。
- 本任务要求"H6 在 O1/O3 之间"⇒ 取 `|r(O1–H6) − r(O3–H6)|` 最小的帧：
  **frame 9 = 0.127**（1.536 / 1.409），对比 frame 8 = 0.336、frame 10 = 0.596、frame 6 = 1.275。
- 构造链：`ts_interp_e3/img_09.xyz`（sha256 **3b264cc7f22f3f2731f6bda49e1fe09cfa7a4246e8a272e160394a6fd40f3068**）
  → `internal_coordinates(mode="transform")` 施加**零度旋转**（rotate, axis_atoms [9,7], atoms [11], degrees 0.0，纯 no-op，仅为让工具写出交付文件）
  ⇒ 本文件坐标与 img_09.xyz 逐位相同（几何全部来自工具，**无手键坐标**）。

## 目标键长（对交付文件实测，Å）

| 量 | 值 | 说明 |
|---|---|---|
| **O1–H6** | **1.536** | 转移中（未成键） |
| **O3–H6** | **1.409** | 转移中（未成键） |
| O1···O3 | 2.808 | 比 P 极小值（2.608）长；OptTS 需自行收缩 |
| **C4···O3** | **3.369** | 甲氧基仍与 C4 断开 ✓ |
| C4–O1 / C4=O5 | 1.263 / 1.248 | 甲酸根等价双氧（产物侧特征） |
| C2–O3 | 1.402 | 甲醇盐/甲醇 |
| Na–O3 / Na–O5 | 2.261 / 2.244 | Na⁺ 双齿，∠O3-Na-O5 = 93.4° |
| 身份 | H6 与两个 O 距离相近（1.536/1.409），甲氧基已断，Na⁺ 双齿 O3/O5 | 与"E3 = I2→P 独立步、质子居中"相容 |

## 声明与局限

1. **本文件只作 ts_prepare 的 TS 初猜几何**。IDPP 插值**不产生任何能量**；其键长/角度**不作能垒、ΔE‡ 或机理论证**证据。E3 的 ΔE‡ 必须来自 OptTS（恰 1 虚频 + 虚频模归属 watch pair）+ 双向 IRC + 两端点 Opt/Freq（0 虚频 + 身份核验）。
2. `C4···O3 = 3.369 Å` 与两端点（I2 4.568 / P 3.217）满足"甲氧基已脱离 C4"，因此该几何不会被误判为 E2 的候选。
3. IDPP 是距离插值：E3 在真实势面上可能同时需要 O1···O3 收缩到 ≈2.5–2.6 Å（P 侧 2.608），OptTS 需自行重整；若失败，建议改用 `xtb_scan_e3`（GFN2-xTB/ALPB water 从 P 端反向沿 O3–H6 的弛豫扫描，job 1003）的峰帧对照。
4. **与 v1 的关系**：E2E3/ts_e3_guess.xyz（sha256 de8d737cb13cc95a6916cbd55ac00104207da1d5f395e68ea8b2f212335c00e1，见 I2_SEED_NOTE.md §6）的起点是 **prewarped 的 prep/i2.xyz**（O3···H6 1.674、O1···O3 2.671），与本轮 job 990 判定的 I2 极小值（O1···O3 4.194）不是同一个盆地；**v2 才与"分步"结论自洽**，v1 只作历史记录。
