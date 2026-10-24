# N_FORMAMIDE · 状态（B3LYP-D3BJ/def2-SVP，气相，纯电子能）

方法口径：G16 /home/ly/g16/g16；B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight；
气相（无 SCRF）；q=0 / m=1 闭壳层；%nproc=4 %mem=6144MB priority 0。
能量只用同批 G16 "SCF Done" 纯电子能相减，无 ZPE/热校正，不跨程序混减。

## 原子序（每个物种一份，1-based 文件序 = gjf 内顺序）
| 物种 | 文件 | 顺序 |
|---|---|---|
| R_syn | geom/build_R/prepared.xyz | 1=N(map3) 2=C(map1) 3=O(map2) 4=H_N(anti,map6) 5=H_N(syn,map5) 6=H_C(map4) |
| I1 | geom/build_I/prepared.xyz | 1=N(map3) 2=C(map1) 3=O(map2) 4=H_N(map6) 5=H_C(map4) 6=H_O(map5) |
| I2 | geom/I2_seed.xyz | 同上（I1 的 O-H 绕 C-O 转 180°） |
| I3 | geom/I3_seed.xyz | 同上 + N-H(map6) 绕 C=N 转 180° |
| P | geom/build_P/assembly/complex_candidate_000.xyz | 1=C(map1) 2=N(map3) 3=H_C(map4) 4=O(map2) 5=H(map5) 6=H(map6) |

## 逐边状态
（待日志回来后填；格式：边 id｜ΔE‡｜起点极小值 路径+sha256+SCF 行号+能量｜TS 日志｜IRC｜身份核验）

E1 / E2 / E3 / E4：进行中。


## 作业记账（本 lane，提交记录）
| job | 输入 | 用途 | 状态 |
|---|---|---|---|
| 1106 | inputs/R_syn_optfreq.gjf | R syn 极小值 opt+freq（E1 分母） | ready/排队 |
| 1107 | inputs/I1_optfreq.gjf | I1 极小值（E2 分母） | ready/排队 |
| 1108 | inputs/I2_optfreq.gjf | I2 极小值（E3 分母） | ready/排队 |
| 1109 | inputs/I3_optfreq.gjf | I3 极小值（E4 分母 ★） | ready/排队 |
| 1110 | inputs/P_complex_optfreq.gjf | P（HCN···H2O 复合物） | ready/排队 |
| 1113 | inputs/E1_scan_H5toO2.gjf | E1 探索性松弛扫描 B 3 5 S 8 -0.1885（2.508→1.00） | ready/排队 |
| 1114 | inputs/E2_scan_dihedral.gjf | E2 探索性二面角扫描 D 6 3 2 1 S 8 22.5（0→180） | ready/排队 |

预算：22（协调者已批）。已用 7。计划：E3/E4 扫描 2、TS1–TS4 各 ts_opt+freq+IRC = 12 ⇒ 21–22。

## 下一步（恢复用）
1. 5 个极小值收敛后：log_parser/analysis/extract.py 取 SCF Done + 频率（0 虚频）+ 二面角实测；
   若 I1/I2/I3 实测二面角与草案节点表不符 → 发 hub 请 spec 作者改节点表（附路径+行号）。
2. E3（I2→I3，d2 O2-C1-N3-H6 180→0）、E4（I3→P，O2-H6 2.24→1.00）各一条探索性扫描。
3. ts_guess scan_parse 取峰 → ts_prepare 建 4 条 TS run：
   reaction: 端点 smiles（含显式 [H:n]），reaction_center 用 bound reactant 全坐标序；
   calculations:{g16:{engine gaussian, method B3LYP, basis_set def2SVP, keywords "EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight"}}；
   guess provided=peak xyz；ts_optimization/verification.frequency/verification.irc 用 {ref:g16}；execution 4c/6144。
4. 每边证据：TS freq 恰 1 虚频 + 模矢在 watch pair 上的方向 + 双向 IRC + 两端 0 虚频 + 身份核验。
5. ΔE‡ = E(TS) − E(该边起点极小值)，纯电子能。

## 极小值实测（G16，纯电子能 SCF Done，Ha）
| 节点 | job | 日志（绝对路径） | sha256 | SCF 行 | E (Ha) | 虚频 | Δ vs R (kcal/mol) | 关键二面角 |
|---|---|---|---|---|---|---|---|---|
| R_syn | 1106 | inputs/R_syn_optfreq.log | 59eafef585723f1e241afd4cfa24cd6c0a570f06abcb8efaccaf1709e45e87f2 | L2690 | -169.772982663 | 0（最低 264.6965） | 0.00 | H5–N3–C1=O2 = 0.02°（H5 syn ✓）；H6–N3–C1=O2 = -179.99° |
| I1 | 1107 | inputs/I1_optfreq.log | 5a287065c4857e334de76477284b5565096236f099fadad2ba2655cc57fca247 | L2347 | -169.751090026 | 0（最低 590.7833） | +13.74 | d1 H5–O2–C1–N3 = 0.0°；d2 O2–C1–N3–H6 = 180.0° |
| I2 | 1108 | inputs/I2_optfreq.log | 671ff1e2b4c33ce608d1f285740846bc04525845bdae3b9eae107ec9f17cd6c7 | L2388 | -169.741299893 | 0（最低 397.0438） | +19.88 | d1 = 180.0°；d2 = 180.0° |
| I3 | 1109 | inputs/I3_optfreq.log | f75427f63512f0aba47004df18c0a48fdb22c253f8f56b3f437060d45d0a36fc | L2063 | -169.744844814 | 0（最低 409.7628） | +17.66 | d1 = 180.0°；**d2 = 0.0°**（H6 指向 O2，r(O2···H6)=2.399 Å）|
| P (HCN···H2O) | 1110 | inputs/P_complex_optfreq.log | d3018f15d26c8f66821917371b53aeea0ac9fb1ff8db684f3494b9a582b43d8f | L5735 | -169.720742486 | 0（最低 47.4812） | +32.79（反应能） | 氢键复合物 N3···H–O2 = 2.09 Å，平面 |

全部 5 个极小值均为 Optimization completed + Stationary point found + Normal termination，0 虚频。
原子序：R_syn = 1N 2C 3O 4H_N(anti) 5H_N(syn) 6H_C；I1/I2/I3 = 1N 2C 3O 4H_N 5H_C 6H_O；P = 1C 2N 3H_C 4O 5H 6H。

**节点身份与草案一致**：I1 = INT-1a（O–H 与 C=N 同侧）；I2 = INT-1b（O–H 转离，d1 180°）；I3 = INT-1c 由 C1=N3 几何翻转实现（d2 180°→0°），使 H6 指向 O2 以满足 E4 的 1,3-H 迁移几何。无需改节点表；上述二面角可作入库身份核验值。

**R 的 syn/anti（需协调者裁定）**：R_syn 中 4/5 号 N–H 对称等价（dihedral -179.99°/0.02°），绕 C–N 转 180° 只是 H5/H6 角色互换，几何与键级不变 ⇒ 不是独立极小值，再做一遍 opt+freq 只会得到同一能量。故本轮只给 R_syn 一个分母（H5 syn，O2···H5 = 2.558 Å），并如实声明「anti 版无独立极小值」。
