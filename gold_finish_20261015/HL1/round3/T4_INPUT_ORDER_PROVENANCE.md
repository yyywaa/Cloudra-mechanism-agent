# HL1_E1 · T4 ts_prepare 输入顺序与 product endpoint seed 的 provenance

用途：为 ts_prepare(run HL1_E1 / T4) 的 `reaction.atom_map`、`guess.xyz_path` 与
`verification.product_endpoint.seed` 记录「具体原子序」的判定依据。**本文件不改写任何原生日志。**

## 1 依据：平台自身构建器的具体原子序（可复核）
对 NR1 包已成功的 ts_prepare run（`/home/ly/Cloudra-mechanism-agent/ts/ts_0005`，owner 为 NR1 包）
逐步反推，得到规则并在该 run 上**逐位重现**了平台自己的 atom_map：

规则：**具体序 = 按 SMILES 书写顺序的组分；每个组分内先列重原子（书写顺序），
再按「母重原子顺序」追加该母原子上的 H（书写顺序的显式 H 会被剥离并重新加回此块）。**
验证：按此规则重建 NR1 reactant 具体序 (26 原子, /home/ly/Cloudra-mechanism-agent/ts/ts_0005/build/input_0002/reactant/seed.xyz)
与 product 具体序 (/home/ly/Cloudra-mechanism-agent/ts/ts_0005/build/input_0002/product/seed.mol, 键表已核)，
再按 SMILES 的 :N map 标签导出 product→reactant 映射，得到
[1,2,3,7,18,19,4,5,6,8,9,10,11,12,13,14,15,16,17,20,21,22,23,24,25,26]，
与 ts_0005/process.json 的 map 阶段权威 `atom_map` **逐位一致**（该文件 sha256 19140d1b11ae9b8a2cdd7a80aeb370d8093f6dd72a296dfb4c9e7a2878e601c9）。

同一规则应用到本包 registry 原文 SMILES（cloudra/benchmark/hard_registry/jl.py L1 第 1 步）：

- reactant `[O+:1]([H:2])([H:9])[H:10].[CH3:11][CH2:5]/[C:4](=[N:6]/[O:7][H:8])/[CH3:3]`
  → 具体序 = O1 | H(1),H(1),H(1) | C11,C5,C4,N6,O7,C3 | H(C11)x3 | H(C5)x2 | H(O7)x1 | H(C3)x3
  → 1=O1, 2..4=H(O1), 5=C11, 6=C5, 7=C4, 8=N6, 9=O7, 10=C3, 11-13=H(C11), 14-15=H(C5), 16=H(O7)=H8, 17-19=H(C3)
- product `[O:1]([H:9])[H:10].[CH3:11][CH2:5]/[C:4](=[N:6]/[O+:7]([H:8])[H:2])/[CH3:3]`
  → 1=O1, 2-3=H(O1), 4=C11, 5=C5, 6=C4, 7=N6, 8=O7, 9=C3, 10-12=H(C11), 13-14=H(C5), 15-16=H(O7), 17-19=H(C3)

**结论 1（guess）**：`HL1/ts_run/t4_interp/img_06.xyz`（sha256 99749b1630e3e654e1523df8cc9726134bfe58b42d59a948082dd1563110fe2d）
的元素行序 O,H,H,H,C,C,C,N,O,C,H*9 与本包 reactant 具体序**逐位相同**（重原子落在 1,5,6,7,8,9,10），
其第 2 行 H 即桥式转移质子（r(O1-H2)=1.280 Å、r(H2-O7)=1.306 Å，与 provenance 文件一致）→ 无需重排，可直接作 provided guess。

**结论 2（atom_map）**：product 坐标序 → reactant 1-based 序
`[1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,2,17,18,19]`
（H2 落到 product 第 16 位；O7 上两个 H 同母原子，若平台内部把两者次序反置，仅是同母 H 互换，不影响任何能量/身份。）

## 2 本文件产生的重排文件（product endpoint seed）
- 原始产物侧极小值 B：`gold_finish_20261015/HL1/ts_run/jobs/A_RC_last.xyz`
  sha256 303ec8b48b90fdb1369e31e5eb667b1d222098e29a87a91f11ff6598ffb5afe6（未修改）
  该文件用的是 **reactant 具体序**（元素行序 O,H,H,H,C,C,C,N,O,C,H*9），不是 product 具体序。
- 本目录 `product_endpoint_seed_B_prodorder.xyz`：仅做**行置换**（保留 8 位小数原值，未改任何坐标/元素/注释化学含义）：
  新区行 = 旧行 [1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,2,17,18,19]
  即 O1 | H(旧3) | H(旧4) | C11 | C5 | C4 | N6 | O7 | C3 | H(C11)x3(旧11-13) | H(C5)x2(旧14-15) |
  H8(旧16, r(O7-H)=0.978 Å) | H2(旧2, r(O7-H)=1.077 Å) | H(C3)x3(旧17-19)
- 顺序定义 MOL（平台自身产物组装件，19 原子、product 连接、product 具体序）：
  `gold_finish_20261015/HL1/ts_run/prep/build_PCmap/assembly/complex_candidate_000.mol`
  sha256 be642363f6a401c5497bff287deead802422913a1dbc09e9861c2d85410ac770（未修改）

## 3 方法/资源（本 run 与包内口径一致）
Gaussian 16 B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight；气相；q=+1, m=1；
8 cpus / 10240 MB。basis_set 用 Gaussian 原生 token `def2SVP`（= 要求的 def2-SVP；BRIEF §3 与
本批所有 .gjf 均用此写法，ts_0005 渲染结果逐字为 `#p ... B3LYP/def2SVP empiricaldispersion=gd3bj scf=tight int=ultrafine`）。
