# TS_E2_GUESS_XTB_PROVENANCE — NY3 E2 备用 TS 初猜（GFN2-xTB/ALPB water 弛豫扫描峰区帧）

- **文件**：gold_finish_20261015/NY3/E2E3/ts_e2_guess_xtb.xyz
- **sha256**：74fa12bc12d95e9d4250c20e9b0ce7dc96ad1f49e021230e80afb3bfeeb42986（11 原子）
- **序（1-based）= 反应物/I1 序**：1 Na｜2 C2｜3 O3｜4 C4｜5 O1｜6 O5｜7,8,9 H(Me)｜10 H(C4)｜11 H6（与 prep/i1.xyz、E2E3/i1_dft_min_ref.xyz、E2E3/ts_e2_guess.xyz 同序）
  i2 序置换（本文件序 → i2 序）= [1,2,3,7,8,9,4,6,5,10,11]

## 来源（run / job / 日志行）

- **job 1001**（chem_task = 类型化 xTB scan manifest），作业目录 gold_finish_20261015/NY3/E2E3/xtb_scan_e2/
- manifest：xtb_scan_e2/scan_e2_manifest.json｜sha256 **508b2fde599e1b2be1877caa9f3aa8b66bb714fdba40b2f5bc7676dbe8dc89f1**
  扫描输入 = E2E3/i1_dft_min_ref.xyz（sha b7e835859f231194f6b3a967d44d53861c9dc8b971769c5e79fe08a8ff97b7eb，i1 序）；约束 = manifest `scan.scans[0].atoms = [3,2]`（0-based）= i1 序的 **C4–O3**；scan_start 1.55 → scan_end 3.90 Å，13 点；force_constant 0.5；solvation = alpb/water
- 原生日志：**xtb_scan_e2/native_scan_runs/native_scan_0001/engine.out**（382871 B），程序调用行（:85）：
  `xtb .../input.xyz --gfn 2 --opt --input .../scan.inp --parallel 1 --chrg 0 --uhf 0 --verbose --alpb water` ⇒ **GFN2-xTB + ALPB water 已生效**
- 帧文件：…/native_scan_0001/point_0001.xyz … point_0013.xyz（本文件取自 **point_0006.xyz**）

## 索引基准实测（消歧结论）

以 i1 序 1-based 原子编号逐帧实测（awk，直接读帧文件）：

| 帧 | C4–O3 (4-3) | O3–C2 (3-2) | C4–O5(烷氧) (4-6) | C4–O1 (4-5) | O1–H6 (5-11) | Na–O3 (1-3) |
|---|---|---|---|---|---|---|
| point_0001 | **1.542** | 1.418 | 1.283 | 1.385 | 0.970 | 2.122 |
| point_0006 | **2.525** | 1.364 | 1.215 | 1.297 | 0.981 | 1.897 |
| point_0011 | **3.508** | 1.354 | 1.210 | 1.290 | 0.982 | 1.877 |
| point_0013 | **3.900** | 1.353 | 1.211 | 1.290 | 0.982 | 1.875 |

⇒ **只有 C4–O3 跟着扫描值走（1.542→3.900，与 1.55→3.90 的点值一致），O3–C2 全程不动（1.35–1.42）**；
⇒ 结论：**manifest 的 `atoms` 字段按 0-based 被 runner 消费**（= 我声明的 1-based [4,3] 减 1），化学目标是 **C4–O3**，**没有扫错键**。另一假设（按 1-based 读 → 扫 O3–C2）被本实测证伪。
（E3 侧同样成立：见 I2_DFT_VERDICT.md §8 的 O3–H6 逐帧表。）

## GFN2/ALPB water 约束弛豫扫描剖面（**半经验、非 DFT；约束扫描峰 ≠ ΔE‡**）

```
point  d(C4-O3)/Å   E(GFN2)/Eh        rel/kcal
  1      1.542      -19.326578408       0.0
  2      1.74       -19.318917772       4.8
  3      1.93       -19.309835786      10.5
  4      2.13       -19.302334147      15.2
  5      2.33       -19.296883359      18.6
  6      2.525      -19.293243800      20.9
  7      2.72       -19.291102693      22.3
  8      2.92       -19.290061898      22.9
  9      3.12       -19.289663913      23.2
 10      3.31       -19.289545506      23.2
 11      3.508      -19.289542667      23.2   ← 工具判定的内部峰
 12      3.70       -19.289657068      23.2
 13      3.900      -19.289782119      23.1
```
（点 11–13 与 I2 型 GFN2 极小值 -19.289398 同区；栅栏极平：2.5–3.9 Å 全部落在峰顶 2.3 kcal/mol 内。工具另报一条诊断"frames 1→2 能量跳 5.70 kcal/mol，可能有谷滑移"，已记录。）

## 选帧与理由（本文件 = point_0006）

- **point_0006**：C4–O3 = 2.525｜C4–O5(烷氧→C=O) = 1.215｜C4–O1 = 1.297｜**O1–H6 = 0.981（H6 仍在 O1）**｜Na–O3 1.897，处在约束扫描峰顶 2.3 kcal/mol 内，且是**对约束弛豫过的**（不是刚性内插）几何 ⇒ 比刚性 IDPP 帧更接近真实鞍点邻域。
- 构造方式：`internal_coordinates(mode="transform")` 施加**零度旋转**（rotate, axis_atoms [4,3], atoms [4], degrees 0.0，纯 no-op）写出交付文件 ⇒ 坐标与 point_0006.xyz 逐位相同（几何来自 xTB，**无手键坐标**）。
- 备选：**point_0011.xyz** = 工具给出的正式峰帧（C4–O3 3.508｜C4–O5 1.210｜C4–O1 1.290），位置偏产物侧；point_0007/0008 亦在峰顶 2.3 kcal/mol 内。全部在 xtb_scan_e2/native_scan_runs/native_scan_0001/。

## 声明与关系

1. **本文件只作 ts_prepare 的备用 TS 初猜**；GFN2-xTB 的能量**不作**任何能垒/ΔE‡ 证据（本战役级别能垒只能取同批 Gaussian 的 0 虚频鞍点 + 双向 IRC）。
2. **主交付仍是 E2E3/ts_e2_guess.xyz**（sha 8bbc6dbb…，IDPP frame 3，C4–O3 2.417 Å）——它已被 run **ts_0013** 用作 provided guess。本文件是同一 TS 区域的**独立第二来源**（xTB 弛豫 vs 刚性插值）：若 ts_0013 的 ts_opt 失败或无鞍点，建议改用本文件重试。
3. 两个几何的差别（同一反应、同一序）：C4–O3 2.417 vs 2.525；C4–O5 1.262 vs 1.215；C4–O1 1.390 vs 1.297 ⇒ xTB 弛豫帧更"产物侧"。