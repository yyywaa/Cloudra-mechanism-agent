# NY3 E1 · TS 初猜 v2 溯源（ts_resume 用）

日期 2026-10-17｜包 NY3（Coordinator as_a0ffef5393594045）｜run **ts_0007**（rev 22, status=blocked / stage=refine / failure_class=job_failed）
工作根 /home/ly/Cloudra-mechanism-agent｜口径 Gaussian 16 B3LYP/def2SVP + GD3BJ + Int(UltraFine) + SCF=Tight + SCRF=(CPCM,Solvent=Water)，charge 0 / mult 1，8c/10000MB

## 1 为什么换初猜（旧初猜已被证伪为「不可用」，不是「无鞍点」）
- 旧初猜 = gold_finish_20261015/NY3/prep/ts_e1_guess.xyz（sha256 `7115db0d0cb184317a0de03eb1847a0658d043f8e0e2adc6904fafd2a4f0a25d`，FF 受约束组装的「四元环」Na–O1...C4–O5）。
- ts_0007 第一次 ts_opt（job 987）以它为输入，在 46 步上限截断（l9999 @L21945）；末帧 O1...C4 = 2.351 Å（比初猜 2.192 更远）、Na–O1 2.072、O1–H6 0.964 ⇒ 优化朝 RC 侧漂移、未达驻点。
  日志：`ts/ts_0007/jobs/declaration_0001/ts_opt/refine.log` sha256 `36b3a6ad5cf75f560b6eca71ba07997636f0584f909861b370a4fde6441de105`（失败原文与末帧几何见 NY3/STATUS.md §3b）。
- 故按平台口径改用「已映射端点插值」重建初猜，不再手工组装。

## 2 新初猜
- 文件：`gold_finish_20261015/NY3/E1/interp/img_05.xyz`，sha256 `fecd47be40ed93445b1778b74fe63a84670fda0b428b88d6b4e5674094b64afb`
- 构造：ts_guess(mode='interpolate', engine='gaussian', interp_method='idpp', n_images=11, atom_map=[1,4,5,6,2,7,8,9,10,11,3]（product 序 → reactant 序，1-based）, watch_pairs=[[2,6],[6,7],[2,3]], output_dir=gold_finish_20261015/NY3/E1/interp)
- 两个端点均为本 run ts_0007 内、同批 G16 同口径的实测极小值：
  - reactant = `ts/ts_0007/jobs/declaration_0001/candidate_opt/optimized_seed.xyz` sha256 `fb6f29c5bbc098007632979c3b1361194e1efc1ee827fc2c83827a0d49cafa7d`（job 967 末帧，E(RB3LYP) = -466.986564979，@L14762）
  - product = `ts/ts_0007/jobs/declaration_0001/product_seed_opt/optimized_seed.xyz` sha256 `b7e835859f231194f6b3a967d44d53861c9dc8b971769c5e79fe08a8ff97b7eb`（job 985 末帧，E(RB3LYP) = -467.004842485，@L14872）
- IDPP 距离表（Å；原子序 = reactant 序：1 Na|2 O1|3 H6|4 C2|5 O3|6 C4|7 O5|8-10 H|11 H）：

  | frame | O2-C6 (O1...C4) | C6-O7 (C4=O5) | O2-H3 |
  |---|---|---|---|
  | 0 | 2.8030 | 1.2217 | 0.9654 |
  | 1 | 2.6413 | 1.2271 | 0.9656 |
  | 2 | 2.4962 | 1.2337 | 0.9658 |
  | 3 | 2.3608 | 1.2410 | 0.9662 |
  | 4 | 2.2301 | 1.2485 | 0.9668 |
  | 5 | 2.0858 | 1.2564 | 0.9671 |
  | 6 | 1.9405 | 1.2638 | 0.9670 |
  | 7 | 1.8129 | 1.2696 | 0.9672 |
  | 8 | 1.6857 | 1.2757 | 0.9686 |
  | 9 | 1.5571 | 1.2825 | 0.9701 |
  | 10 | 1.4271 | 1.2908 | 0.9710 |

- 选中帧 = img_05（工具判定 ts_candidate_index=5；watched pair O2-C6 越过两端中点）。

## 3 旁证：弛豫扫描（不作为能垒，只说明该区能量确实在上升）
- job 989：输入 `gold_finish_20261015/NY3/E1/E1_scan_O1C4.gjf` sha256 `8e2a37eb4e745d4d8196899d96183a67aa08ee3057c78615577424794cb0a1cf`；日志 `gold_finish_20261015/NY3/E1/E1_scan_O1C4.log` sha256 `62ac90e3732663dc82de1339fe1623b3e3457a4528d2d1f92d8bf3748442dca4`。
- route `#p opt=modredundant b3lyp/def2svp empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=water)`，起点 = job 967 的 RC 极小值，扫描键 B 2 6（O1...C4）2.803 → 1.603 Å（步长 -0.1，13 点）。
- 逐点（各点末次 SCF Done，行号取原生日志）：pt1 2.803 E=-466.984281494 @L2793｜pt2 2.703 E=-466.982790247 @L9805｜pt3 2.603 E=-466.979565357 @L14540｜pt4 2.503 E=-466.974209173 @L20129；pt5（2.403）在 45 步上限内未收敛，作业 l9999 终止（@L40682）。
- 读法：沿该变量能量单调上升，**扫描区间内没有峰顶**（峰在更短距离处）；且 1D 约束路径的逐点收敛性差（Na+ 与甲基自由度很软）⇒ 不用扫描峰做初猜，改用端点插值帧。

## 4 边界
- 本初猜**不是鞍点、不是能垒证据**。E1 的 ΔE‡ 只能取本 run 通过验收的 TS（恰 1 虚频且模属声明键对 + 双向 IRC 达端点 + 两端点 Opt+Freq 0 虚频与身份核验）之纯电子能，相对本步起点极小值（RC）。
