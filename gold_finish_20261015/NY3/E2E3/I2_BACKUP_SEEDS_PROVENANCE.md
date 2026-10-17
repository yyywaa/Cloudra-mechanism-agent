# I2_BACKUP_SEEDS_PROVENANCE — NY3 I2 备用构象种子（供 ts_0013/ts_0014 的端点或第三次收敛尝试）

背景：ts_0014 的 candidate_opt（**job 1007**）从 E2E3/i2_min_candA.xyz 出发 l9999（`-- Number of steps exceeded, NStep= 42` @ ts/ts_0014/jobs/declaration_0001/candidate_opt/seed-opt.log:18771；`Error termination via Lnk1e ... l9999.exe` @:19001；末次 SCF −466.984880863 @:18644）。同一几何的既有尝试 job 971（NStep=48 @L21877）与 job 981（NStep=51 @L23035，起点是另一个"紧凑接触对"）也都没有收敛声明。**这只是"从该点出发在步数上限内不收敛"，不是"I2 不存在"的证据**（job 990 已证明该几何 0 虚频）。

**序（所有文件，1-based = i2 序）**：1 Na｜2 C2(甲基 C)｜3 O3(甲醇盐/甲醇 O)｜4,5,6 H(甲基)｜7 C4(甲酸 C)｜8 O5(甲酰 O)｜9 O1(羟基 O)｜10 H(C4)｜11 H6
（下列所有键长均为 awk 直接读文件实测，非转述。）

## A 备用种子一览（sha256 + 实测键长 / Å）

| 文件（均在 gold_finish_20261015/NY3/E2E3/） | sha256 | O1–H6 | O3···H6 | C4···O3 | C4–O5 | C4–O1 | Na–O3 | Na–O5 | Na–O1 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| i2_min_candA.xyz（**当前声明起点，勿再同款重跑**） | 1715f6d7d77e93bb5200a71b23db31fc84cb45564b1d48f6bbab2e7ee3c0ef85 | 0.972 | 5.056 | 4.568 | 1.209 | 1.326 | 2.047 | 2.312 | 3.381 | job 971 末帧（力判据达标、位移判据未达；job 990 判 0 虚频） |
| i2_seed_candB_methoxide_out.xyz | bc2477926f83aa4b25cf004b70b372c276fb8e41e2a425fef0f5e7c559b1b870 | 1.009 | 2.497 | 3.873 | 1.224 | 1.341 | **3.600** | 3.463 | 2.524 | prep/i2.xyz → 刚性 stretch [1,3] Na–O3 2.427→3.600 |
| i2_seed_candC_combined.xyz | 3cb504218c690d904a612b1f72e316c1e3056aa12ce921ab81c4184d40859dce | 1.009 | 4.296 | 3.873 | 1.224 | 1.341 | 3.600 | 3.463 | 2.524 | candB + rotate [11] 绕轴 [9,7] 180° |
| i2_seed_candD_classB.xyz | 78448225332a095326025a2c3beaa891c287746889656f7cba6d83bd4856c840 | 0.979 | 5.540 | 5.295 | 1.204 | 1.305 | 3.300 | 2.111 | 2.528 | candA_xtbmin → stretch [1,3] 1.876→3.300（Na⁺ 双齿甲酸根） |
| i2_seed_candA_H6away_syn.xyz | f580e848eaf4b7cea43df59646f0ae719fada82accd4d4edc9213bab1c607120 | 1.009 | 3.552 | 3.254 | 1.224 | 1.341 | 2.427 | 3.463 | 2.524 | prep/i2.xyz → rotate [11] 绕 [9,7] 180° |
| i2_seed_candA_H6away_xtbmin.xyz（job 971/981 的真实起点，**已用过**） | 422b79e6cd1cd3d7648c7d7bad4f94c122187572c0890aee7442b108837cedb4 | 0.979 | 4.459 | 4.018 | 1.204 | 1.305 | 1.876 | 2.111 | 2.528 | candA_syn 经 xtb --ohess（GFN2/ALPB water） |
| **i2_seed_xtb_na3_p11.xyz**（本轮新交付） | **10177bfad77af2cee20e8b3191c7265ad271c29bd5ff7471f63bd3b222568e44** | 0.981 | 2.731 | 3.908 | 1.210 | 1.291 | **1.887** | 2.043 | 3.377 | job 1003（E3 反向扫描）frame point_0011 |
| **i2_seed_xtb_na3_p12.xyz**（本轮新交付） | **f5be86f6102d80c1c4395246f6b1917b2d568f7e9c920ee7954fd0fe7de38043** | 0.980 | 2.899 | 3.994 | 1.210 | 1.292 | **1.883** | 2.044 | 3.446 | job 1003 frame point_0012 |

- 全部满足 I2 判据（**H6 在 O1**、甲氧基与 C4 已断、C4–O1 ≈ C4=O5 分列甲酸的单/双键侧）。
- 两个新文件是**工具产物**：由 `internal_coordinates(mode="transform")` 施加零度旋转（rotate, axis_atoms [9,7], atoms [11], degrees 0.0，纯 no-op）写出，坐标与 `xtb_scan_e3/native_scan_runs/native_scan_0001/point_0011.xyz`（sha 8450fe82906ae88cae16a4904221e17b02146914a95a158f78df27e081b222e0）/`point_0012.xyz`（sha 84c287b4f6acfdf1997d9c4833fe844d222d01049876576f9a9e209974c06416）逐位相同。

## B 三类 Na⁺ 配位模式（选种子的依据）

| 类 | Na⁺ 配位 | 代表种子 | 备注 |
|---|---|---|---|
| (a) 桥联 O3/O5 | Na–O3 ≈ 1.88–2.05、Na–O5 ≈ 2.04–2.31 | **i2_min_candA.xyz**（DFT, Na–O3 2.047）、i2_seed_candA_H6away_xtbmin、**新 p11/p12** | DFT 侧 I2_min 属于此类的 DFT 版本 |
| (b) 双齿甲酸根 O1/O5 | Na–O1 ≈ 2.53、Na–O5 2.111 | i2_seed_candD_classB.xyz | 电荷上最"合理"的一类（阳离子贴住甲酸根阴离子） |
| (c) 只剩 O1（甲醇盐脱配位） | Na–O3 3.60 | i2_seed_candB/C | 阳离子离开甲氧基阴离子 ⇒ 静电上不利，**建议最后才试** |

**若 job 1012 仍不收敛，建议按 (b) → (a) → (c) 顺序换种子**（每个都附了现成路径与 sha256）。

## C 比换种子更可能一次成功：用 job 990 的解析 Hessian 起步

- job 990 的频率作业**就是在这个几何上算的**（核对方式：freq 日志末帧与 i2_min_candA.xyz 逐位 diff 只差注释行），因此它的 chk 里存有该几何的**解析 Hessian**：
  **gold_finish_20261015/NY3/E2E3/freq_i2_candA/i2_candA_freq.chk**｜sha256 **343c0fd5576fdf3c491e98e1933e0a60b9cbd3582bb60f656a8c2521005b8f17**（4689920 B）
- 更稳的做法：把该 chk 复制到新目录，route 用
  `#p opt=(readfc,maxcycles=200) freq b3lyp/def2svp empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=water)`
  **坐标块仍送 i2_min_candA.xyz 的同一几何**（readfc 要求 chk 内几何与输入几何一致；两者已逐位相同）。这样 Berny 从**精确 Hessian** 起步（而不是靠模型 Hessian 反复更新，这正是 job 971/981/1007 反复"力收敛但位移不收敛"的典型成因），通常 2–5 步给出 `Stationary point found`。
  job 1012 用的 `calcfc`（起点重算 Hessian）在数学上等效、只是多花一次 Hessian 时间；**两者不要同时占配额**。

## D 声明
1. 这些种子**只作几何起点**；xTB（GFN2/ALPB water）来源帧的能量**不得**与本批 DFT 能量混减、不得作能垒证据。
2. 本文件不改写任何原生日志；键长全部由 awk 读文件本体实测，sha256 见上表。
3. 本道**未**对 i2_min_candA.xyz 发起任何新的 opt/opt+freq（遵守 Coordinator 的"勿重复优化"）。