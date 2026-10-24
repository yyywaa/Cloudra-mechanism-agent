# NY3 补算 · 输入来源登记（gold_fill_20261018/NY3）

能量口径：只在本批 Gaussian 16 内相减。G16 `/home/ly/g16/g16`，route = `#p` + B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight + SCRF=(CPCM,Solvent=Water)，q=0/m=1，%nproc=8、%mem=14336MB、priority 0。无 ORCA；xTB/GFN2 数值不参与任何差值。

## 1 端点参考几何（只读复用，未改动）
| 物种 | 文件（工作根相对） | sha256 | 原始证据 |
|---|---|---|---|
| I1（E2 起点） | gold_finish_20261015/NY3/E2E3/i1_dft_min_ref.xyz | b7e835859f231194f6b3a967d44d53861c9dc8b971769c5e79fe08a8ff97b7eb | job 985（E=−467.004842485）；同序 MOL prep/i1.mol（c4165dfc33a88e26990c32b4c3911259ffc1b092b67aeeb1d595bea33feea184） |
| I2（E2 终点 / E3 起点） | gold_finish_20261015/NY3/E2E3/i2_min_candA.xyz | 1715f6d7d77e93bb5200a71b23db31fc84cb45564b1d48f6bbab2e7ee3c0ef85 | job 990 固定几何 freq 0 虚频（E=−466.986020418）；同序带键 MOL prep/build/art_I2_src/assembly/complex_candidate_000.mol（af67740f8c76f18f0517573c8cb5590aa8bb603d3d1c706df624ebd1ce46f816，8 键 + M CHG Na+1/O3−1） |
| P（E3 终点） | gold_finish_20261015/NY3/E2E3/p_min_ref_pmol_order.xyz | bca75d0ac100298d955b3826fc8ade3bc1413783ed905d5dca62d57a83486d8b | job 994 Opt+Freq 0 虚频（E=−467.045937735）；同序 MOL prep/p.mol（165702ab64bcccbe6b7434b2b0a3a66379ed88deb4eab34d20bd1d729dcedf09） |
| RC（E1 起点参考） | gold_finish_20261015/NY3/E1/rc_dft_min_working_order.xyz | 449cad42aa779d00dd0f454c5b0eb93a9b4bdb771d6de8772cf9912aa7adef68 | job 967（−466.986564979）工作序副本；job 1031 同侧 0 虚频参照（−466.986564213，带近简并 caveat） |

## 2 TS 初猜（只读复用）
| 边 | 文件 | sha256 | 备注 |
|---|---|---|---|
| E2 | E2E3/ts_e2_guess.xyz | 8bbc6dbb866df8619b5a150b6c3ea196c575d3b0b9e1398a89b9497de32e9ea0 | IDPP 帧，r(C4–O3)=2.417 Å，i1 序 |
| E3 | E2E3/ts_e3_guess_v2.xyz | 3ccf834e473dc4f6f0e19b1ad1502d9e0f026ea602d8957b3c5b4fdc4fbfa43f | i2 序；O1–H6 1.536 / O3–H6 1.409 / O1···O3 2.808 Å |
| E1 候选 a | E1/e1_tsguess_revscan_p5_reactantorder.xyz | 14e096487c4d6113ff1c0c4d3ad1d6c8d532ab1612fb53beb8e0d2de8afb2fc7 | job 1023 p5（支-I1，r(O1···C4)=2.027，约束极大，E=−466.969423982） |
| E1 候选 b | E1/e1_tsguess_attempt2_o1shift_reactantorder.xyz | 4327d465d70c1dd926f1f564739c0225059253a2f65223b8e3d2856888e65b75 | p6 把 O1+H6 沿 C4→O1 轴推到 2.1271 Å（支-RC，从未提交） |
| E1 候选 c | E1/e1_tsguess_revscan_p6_reactantorder.xyz | 9ee4e84748af8b4c1e78af813b7eb5de64164530ab06c724cc627117942b5b66 | job 1023 p6（支-RC，2.1771 Å；ts_0007 尝试 1 已用并失败） |

## 3 关键既有失败（技术性，不作为「无鞍点」证据）
见 gold_finish_20261015/NY3/STATUS.md §19/§33.2/§38/§39：E1 job 1004→1010（甲基转子 pseudo-saddle −98.2487 cm⁻¹，甲基 H 99.49%）、job 1027（羟基 H 扭转 −134.4181 cm⁻¹，H 98.87%）、job 1034（NStep=45，末帧退回 2.383 Å）；E2/E3 的 build 阶段 conformer 预优化（job 1007/1011/1012/1016/1019/1024/1025）全为 NStep/l9999 截断。

## 4 本会话作业清单
逐条追加到 STATUS.md §2（job id / 输入 / 原生日志 / sha256 / 行号 / 读数）。
