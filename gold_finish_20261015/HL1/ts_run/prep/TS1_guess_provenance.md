# HL1_E1 / TS1 候选初猜 provenance（provided guess 证据文件）

用途：作为 ts_prepare(guess.kind="provided", xyz_path=t4_interp/img_06.xyz) 的 evidence_refs 之一，
证明该 TS 候选几何的来源、坐标系与原子序、以及授权文本。**本文件不改变任何原生日志。**

## 1. 授权与要求（原文摘录）
- 本包派单（HL1 包 · 计算 owner 任务 HL1_E1）：T4「若 T1 或 T3 给出任何鞍点候选几何 → 走 ts_prepare（provided guess，
  gaussian 引擎，B3LYP/def2SVP + EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight，charge +1/multiplicity 1，
  reaction_center = 本序 [1,2] 与 [2,9]，verification 含 frequency + IRC + 两端端点 Opt/Freq）；
  **若始终没有候选峰，也必须至少跑一次 ts_prepare（用最好的候选几何：例如剖面上能量最高点或 T1 起点插值）**」。
- 主协调补充口径（AgentHub gold-finish-20261015，post evt_97d70f5b24cc4065）：
  「provided guess 用**质子居中的过渡几何**（O1···O9 ~2.6–3.0 Å、R(1,2)≈R(2,9)≈1.2–1.5 Å，可从剖面最高帧取，
  或按 3.00 Å 种子把 H2 沿 O1→O9 内插到 ~1.35 Å）」。本文件即按「内插」法生成并选定。

## 2. 候选几何来源（工具与文件，全部绝对路径）
- 生成方式：`ts_guess(mode="interpolate", interp_method="idpp", n_images=9,
  reactant_path=.../ts_run/prep/RC_3A_seed.xyz, product_path=.../ts_run/jobs/A_RC_last.xyz,
  atom_map=[1..19]（恒等）, watch_pairs=[[1,2],[2,9],[1,9]], output_dir=.../ts_run/t4_interp/)`
  返回原文要点：`Generated 9 images (idpp) ... TS candidate frame: img_04.xyz (watched pair H2-O9 crosses the endpoint midpoint)`。
- 端点 A（反应物侧，H3O+ + 肟，d(O1···O9)=3.000 Å，质子仍在 O1）：
  /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HL1/ts_run/prep/RC_3A_seed.xyz
  sha256 = 18dd830da10d3cc81d9ed5072445e0da5df32d81b479eb7a3ed3e8bc5c2c5dc6
- 端点 B（产物侧，H2O + O-质子化肟复合物极小值；job 904/905/920 的末帧）：
  /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HL1/ts_run/jobs/A_RC_last.xyz
  sha256 = 303ec8b48b90fdb1369e31e5eb667b1d222098e29a87a91f11ff6598ffb5afe6
  （终点能量来源：jobs/A_RC_optfreq.log sha256 dd2736788cb8e0fc01914efbf02c91c40408d97bb17e456c354d2a8a621c781e，
   E=-364.295965289 Eh；jobs/C2_RC3A_optfreq.log sha256
   01c7b36f48170832a44652217c1796242969fd95befe3137413e08650f11c559，E=-364.295965302 Eh，同一驻点）
- IDPP 路径逐帧 watcher 距离（ts_guess 返回原文）：
```
frame         O1-H2         H2-O9         O1-O9
   0        0.9877        2.0123        3.0000
   1        1.0367        1.8866        2.9221
   2        1.0860        1.7636        2.8456
   3        1.1341        1.6458        2.7746
   4        1.1820        1.5320        2.7092
   5        1.2303        1.4200        2.6466
   6        1.2804        1.3061        2.5836
   7        1.3307        1.1919        2.5201
   8        1.3812        1.0774        2.4569
```

## 3. 选定 guess 与备选
- **选定 guess**：/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HL1/ts_run/t4_interp/img_06.xyz
  sha256 = 99749b1630e3e654e1523df8cc9726134bfe58b42d59a948082dd1563110fe2d
  几何（internal_coordinates 判定，**未做 QM 优化/无能量、不是驻点**）：
  r(O1-H2)=1.280 Å、r(H2-O9)=1.306 Å、r(O1···O9)=2.584 Å、r(H2-N8)=2.319 Å、r(H16-O9)=0.978 Å。
  选择理由：该帧在两个 watcher 上最接近**对称桥式**（Δr=0.026 Å），符合主协调「质子居中」口径。
- 备选（ts_guess 自动判定帧）：t4_interp/img_04.xyz，
  sha256 = 59a5bc8ebfc078b7e3f176dc636db03178b995fbc689ff6893234a28dfa7e1eb（r(O1-H2)=1.182、r(H2-O9)=1.532、O1···O9=2.709 Å）。
- 说明：这些内插帧**没有任何量化能量**，只是「质子在两氧之间的几何」；是否为鞍点必须由 ts_prepare 的 OptTS + freq + IRC 判定。

## 4. 坐标系与原子序对照（本包统一，1-based；与本包所有 xyz/gjf 一致）
1=O1（H3O+/水的 O）、2=H2（转移质子）、3=H3、4=H4（H3O+ 另两个 H）、5=C11(乙基 CH3)、6=C5(CH2)、7=C4、
8=N6（肟 N）、9=O7（肟 O）、10=C3(甲基)、11-13=H(C11)、14-15=H(C5)、16=H8(肟 OH 的 H)、17-19=H(C3)。
反应中心（本序）：break [1,2]、form [2,9]。题面 mapped SMILES 对应：本序 1↔1、2↔2、3↔9、4↔10、5↔11、6↔5、7↔4、8↔6、9↔7、10↔3、16↔8。
所有内插帧保持上述原子序（atom_map 恒等）。

## 5. 背景：为什么必须发这次 ts_prepare（存档用）
- job 920（C2_RC3A，d(O1···O9)=3.000 Å 的 A 形种子）未约束 Opt+Freq **滑落**到产物侧同一驻点（见 §2 sha/能量）。
- jobs/B_sepscan_OO.log（912）前 10 个扫描点逐点单调上坡、无内部极大；第 11 点 NStep 耗尽失败。
- jobs/B_ptscan_frozenOO.log（913）因「扫描坐标 + 冻结坐标」冗余 l103 失败，零可用点。
- 因此需要一个**人工给定的质子居中几何**来正式尝试一次 TS 搜索，以确保「无鞍点」结论有原始记录。
