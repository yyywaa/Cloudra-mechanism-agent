# NY3 · E2/E3 端点极小值与声明配对 provenance

作者：NY3 包整合 Coordinator **as_a396e35616564357**（本包唯一写权会话）｜时间：2026-10-17 07:2x +08:00
用途：为 **E2（I1→I2）** 与 **E3（I2→P）** 两条 durable TS run 提供**端点几何/身份/序配对**的可复核证据。
引擎口径：**Gaussian 16**（/home/ly/g16/g16），B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight + SCRF=(CPCM,Solvent=Water)，charge 0 / multiplicity 1。能量只在**同批日志**内相减；**不得**与历史 ORCA 值混减。

## 1 四条参考极小值（同批 G16 纯电子能）
| 物种 | job | 原生日志（工作根相对） | log sha256 | E(RB3LYP)/Ha（行号） | 0 虚频 |
|---|---|---|---|---|---|
| RC（E1 起点） | 967 | ts/ts_0007/jobs/declaration_0001/candidate_opt/seed-opt.log | 730caaa08baa079eeac78ab5cc40bcfed285eda1044f578b281ce4a4f202f53f | −466.986564979（@L14762） | 待 ts_0007 反应物端点 Opt+Freq |
| I1（E1 终点 / E2 起点） | 985 | ts/ts_0007/jobs/declaration_0001/product_seed_opt/seed-opt.log | 56e90cc4eea1dd7c5c1cd96e62a8db22ff2e7627ee190fc06eb9fa39720d3fe2 | −467.004842485（@L14872） | 待 ts_0007 产物端点 Opt+Freq |
| I2（E2 终点 / E3 起点） | 990（几何 = job 971 末帧） | gold_finish_20261015/NY3/E2E3/freq_i2_candA/i2_candA_freq.log | df2548644fc22ac7b64b0da08bded3f44e1ecc9f4db1c5e2015aa2ed954e598b | −466.986020418（@L512） | **✓** 27 模全实、无 imaginary 行（@L1470 Normal termination） |
| P（E3 终点） | 994 | gold_finish_20261015/NY3/E2E3/p_optfreq/p_ref_optfreq.log | ff7ecb5aab3724bd2574c37c9a78b309e45f7eabfeb5ec9ec703c53860f816df | −467.045937735（@L10443） | **✓** 27 模全实、`Stationary point found.` @L10592 |

极小值间差值（**不是能垒**）：I1 − RC = −11.47｜I2 − I1 = **+11.81**｜I2 − RC = +0.34｜P − I2 = **−37.60**｜P − I1 = −25.79 kcal/mol。

### 身份实测（几何判据，1-based；坐标文件见 §2）
- I1（i1 序：1 Na｜2 C2｜3 O3｜4 C4｜5 O1｜6 O5｜7-9 H(Me)｜10 H(C4)｜11 H6）：C4–O1 1.427 / C4–O5 1.291（阴离子 O）/ C4–O3 1.503 / O1–H6 0.965 ⇒ 四面体中间体，**H6 仍在 O1**，阴离子在 O5（与 yo.py 第 1 步产物式 `[CH:4]([O:1][H:6])[O-:5]` 一致）。
- I2（i2 序：1 Na｜2 C2｜3 O3｜4-6 H(Me)｜7 C4｜8 O5｜9 O1｜10 H(C4)｜11 H6）：O1–H6 0.972 / C4–O1 1.326 / C4=O5 1.209 / **C4···O3 4.568（已断）** / O3···H6 5.056 / Na–O3 2.047 / Na–O5 2.312 Å ⇒ 甲酸 + 甲醇盐 + Na⁺，**H6 在 O1**（与 yo.py 第 2 步产物式一致）。**我（as_a396e35616564357）独立复算，与道报数逐位一致。**
- P（i2 序）：O3–H6 1.009 / O1···H6 1.605 / C4–O1 1.257 / C4=O5 1.253 / C4···O3 3.217 / Na–O3 2.287 / Na–O5 2.242 Å ⇒ 甲酸根 + 甲醇 + Na⁺，**H6 在 O3**（与 yo.py 第 3 步产物式一致）。

## 2 几何文件与 mol 配对（xyz 与 mol **必须同序**；重排均已逐位核对）
| 用途 | xyz（sha256） | mol（sha256） | 序说明 |
|---|---|---|---|
| E2 反应物 = I1 极小值 | E2E3/i1_dft_min_ref.xyz `b7e835859f231194f6b3a967d44d53861c9dc8b971769c5e79fe08a8ff97b7eb` | prep/i1.mol `c4165dfc33a88e26990c32b4c3911259ffc1b092b67aeeb1d595bea33feea184`（bonds 2-3、3-4、4-5、4-6、2-7/8/9、4-10、**5-11**；CHG 1=+1、6=−1） | 两者同为 i1 序（Na, C2, O3, C4, **O1(H)=5**, **O5(−)=6**, H(Me)×3, H(C4), H6） |
| E2 产物 = I2 极小值 | E2E3/i2_min_candA.xyz `1715f6d7d77e93bb5200a71b23db31fc84cb45564b1d48f6bbab2e7ee3c0ef85` | prep/build/art_I2_src/assembly/complex_candidate_000.mol `af67740f8c76f18f0517573c8cb5590aa8bb603d3d1c706df624ebd1ce46f816`（bonds 2-3、2-4/5/6、**7-8 双键**、7-9、7-10、**9-11**；CHG 1=+1、**3=−1**） | 两者同为 i2 序（Na, C2, O3, H(Me)×3, C4, O5, O1, H(C4), H6） |
| E3 反应物 = I2 极小值 | 同上（i2_min_candA.xyz） | 同上（art_I2_src … mol） | 同上 |
| E3 产物 = P 极小值 | E2E3/p_min_ref_pmol_order.xyz `bca75d0ac100298d955b3826fc8ade3bc1413783ed905d5dca62d57a83486d8b`（由 p_min_ref.xyz `f69ef3c9215d95fe31a17d4cfecc9a2a0bf111fd932894bf0f236a985348f4ea` **按 p.mol 序重排**：原 1..6,11,7,8,9,10） | prep/p.mol `165702ab64bcccbe6b7434b2b0a3a66379ed88deb4eab34d20bd1d729dcedf09`（bonds 2-3、2-4/5/6、**3-7**、8-9 双键、8-10、8-11；CHG 1=+1、**10=−1**） | p.mol 序 = Na, C2, O3, H(Me)×3, **H(O3)=7**, C4=8, O5=9, O1(−)=10, H(C4)=11；重排后 xyz 与该序逐位一致（H(O3)–O3 = 1.009 Å 已核） |

## 3 两步的声明要点（1-based，与 ts_0003 的已成功声明样式一致）
- **E2**：reactant `[Na+].CO[C@H]([O-])O`（I1），product `[Na+].C[O-].C(=O)O`（I2）；`atom_map`（product 序 → reactant 序）= **[1,2,3,7,8,9,4,6,5,10,11]**；`reaction_center` = **[[4,3],[4,6]]**（断 C4–O3；C4=O5 π 变化）；heavy_atom_binding：reactant [1,2,3,4,6,5]、product [1,2,3,7,8,9]。
  （对照：孤儿 run ts_0003 的同化学声明存储值 0-based = atom_map [0,1,2,6,7,8,3,5,4,9,10]、reaction_center [[3,2],[3,5]] ⇒ 本声明 1-based 写法正确。）
- **E3**：reactant `[Na+].C[O-].C(=O)O`（I2），product `[Na+].CO.C(=O)[O-]`（P）；`atom_map` = **[1,2,3,4,5,6,11,7,8,9,10]**（H6 在 product 序的 7 位 ↔ reactant 序 11 位）；`reaction_center` = **[[9,11],[3,11]]**（断 O1–H6、成 O3–H6）；heavy_atom_binding：reactant [1,2,3,7,8,9]、product [1,2,3,8,9,10]。
- TS 初猜（provided，1-based 与各自 reactant 序一致）：E2 = E2E3/ts_e2_guess.xyz `8bbc6dbb866df8619b5a150b6c3ea196c575d3b0b9e1398a89b9497de32e9ea0`（i1 序；C4–O3 2.417 / C4=O5 1.262 / O1–H6 0.969）；E3 = E2E3/ts_e3_guess_v2.xyz `3ccf834e473dc4f6f0e19b1ad1502d9e0f026ea602d8957b3c5b4fdc4fbfa43f`（i2 序；O1–H6 1.536 / O3–H6 1.409）。
- **声明纪律**：初猜几何只作 OptTS 起点，其能量不作任何能垒证据；ΔE‡ 一律取管线 TS 的 E(TS) − **该步自身起点极小值**（E2: I1；E3: I2），全部同批 G16 纯电子能。
- 端点身份以**管线产出的 IRC 两端点 Opt+Freq（0 虚频）**为正式证据；job 990 / 994 的 0 虚频只作预判（job 990 的几何来自 job 971 末帧，位移判据未达、无 `Stationary point found`）。
