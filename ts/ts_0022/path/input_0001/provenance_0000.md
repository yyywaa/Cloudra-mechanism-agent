# HL1_E1 鞍点归属补算 · guess provenance（2026-10-18）

工作目录：gold_fill_20261018/HL1/HL1_E1/。只做 HL1_E1 这一条边；不读不写 NR1/NY3/HI1。

## 1. 本次 ts_prepare 的输入口径
- 引擎/方法：Gaussian 16（/home/ly/g16/g16），B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight，**气相**（不写 SCRF），q=+1 / m=1，19 原子 C4H12NO2+，51 模。
- reaction_center（本包统一 1-based 原子序）：break [1,2]（O1-H2）、form [2,9]（H2-O7 肟氧）。
- 原子序（1-based）：1=O1(H3O+/水的 O)、2=H2(声明转移质子)、3=H3、4=H4、5=C11、6=C5、7=C4、8=N6、9=O7(肟 O)、10=C3、11-13=H(C11)、14-15=H(C5)、16=H8(肟 OH 的 H)、17-19=H(C3)。

## 2. guess 文件与其来源（只读引用，未改动）
- guess：/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HL1/round4/T3_scan_peak_pt8_ts_guess.xyz
  sha256 = 7018f6880a335c7ccd013a47d44fcf8599c3e9f5842bfa872571ae33f9a014ac（本次调用前实测一致）
- 来源日志：/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HL1/round4/T3_ptscan_H2O9_relaxed.log
  sha256 = 40ce3be2c6d07120b36d7bf8ce9580aad6becaee16cdf8d1b2c3cb0ab0e60c07，69007 行
  该点最后一次 SCF：**L17400** `SCF Done:  E(RB3LYP) =  -364.290279321     A.U.`；曲线汇总 **L68993**（第 5 个值 −364.2902793）。
- 剖面表：gold_finish_20261015/HL1/round4/T3_scan_curve.csv，frame=7（0-based）行：`7,,1.42738,-364.29028,...`，
  即受约束弛豫剖面上 R(H2···O7)=1.42738 Å 的内部极大帧（本包文档称 pt8，序号按 1-based 数点）。
- guess 身份（未做 QM 优化、无能量、不是驻点）：**接触离子对（氢鎓式 O1 + 中性肟）**，
  R(1,2)=1.076 Å、R(2,9)=1.427 Å、R(1,9)=2.399 Å；O1 另有 H3=0.975、H4=1.003 Å $Rightarrow$ H3O+ 型；
  肟 OH (O9-H16)=0.977 Å 完整；N6 上无近距 H。
- 该帧相对产物侧极小值 B（-364.295965289 Ha）高 +3.568 kcal/mol，**仅为受约束剖面上界（下界口径的剖面值）**，不构成鞍点证据。

## 3. 端点绑定用的既有结构（只读引用，与历史 run 同序，本文件不改动）
- 反应物侧 seed：gold_finish_20261015/HL1/ts_run/prep/RC_3A_seed.xyz（sha256 18dd830d…，d(O1···O9)=3.0 Å）
  + MOL：gold_finish_20261015/HL1/ts_run/prep/build_RCmap/assembly/complex_candidate_000.mol（19 原子，本包原子序）
- 产物侧 seed：gold_finish_20261015/HL1/round3/product_endpoint_seed_B_prodorder.xyz（sha256 5b03a2ea…）
  + MOL：gold_finish_20261015/HL1/ts_run/prep/build_PCmap/assembly/complex_candidate_000.mol
- 说明：这些只是**绑定/坐标系种子**，不是参考态。ΔE‡ 的起点取 **IRC 反向后收敛到的接触离子对极小值**（本 run 自己的 Opt+Freq），不使用不存在的旧 RC（A_RC_optfreq 实际落在 B）。

## 4. 判定口径（主协调裁决 1，逐条执行，不用百分比阈值）
(a) 硬闸门：虚频模在 watch pair 上的净位移方向须与 bond_changes 同向（R(1,2) 拉长、R(2,9) 缩短）。
(b) 记录项：报三个归一化份额（声明反应中心对 / 该模内所有重原子 / 最大单原子），并指出最大份额落在哪个自由度。
(c) 交付：同程序同方法同模型、TS（恰 1 虚频）与本步自身起点极小值的纯电子能差；TS 一虚频 + 双向 IRC 到端点 + 两端 Opt/Freq 0 虚频。
