# T3 剖面设计记录（HL1_E1，气相 B3LYP-D3BJ/def2SVP，q=+1,m=1）

本文件只记录**输入设计与失败点证据**；逐点能量与结论写入 `ts_run/NOTES.md`（避免两处数字冲突）。
所有原子序为**本包 1-based 本序**（见 NOTES.md）：1=H3O+ 的 O1，2=转移质子 H2，3/4=H3O+ 另两个 H，
8=肟 N，9=肟 O(O7)，16=肟 OH 的 H。反应中心：break [1,2] / form [2,9]。

资源与方法：Gaussian 16，`#p ... B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight`，气相（无 SCRF），
%nprocshared=8 / %mem=10GB；本包同刻最多 2 个 QM 作业；不设非原生 MaxIter/MaxSteps。

## 1. 松弛扫描（opt=modredundant）输入清单

（所有输入文件绝对路径前缀 = /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HL1/ts_run/jobs/）

| 标签 | 输入文件 | 扫描坐标（本序） | 区间 / 步长 | 起点几何（种子） | 目的 |
|---|---|---|---|---|---|
| T3a | T3a_ptscan_O1H2.gjf（sha256 645d280c0c54fa65e622b5800c94dfb92356196b69256d019668fc3e5d614350） | `B 1 2` d(O1–H2) | 0.988→2.088 Å，20×0.05（21 点） | prep/RC_3A_seed.xyz（d(O1···O9)=3.000，H2 在 O1） | 主 PT 剖面：把质子从 O1 侧推到 O9 侧，O1···O9 **不冻结**，看有无内部极大 |
| T3b | T3b_sepscan_OO_in.gjf（sha256 2795cf895816cc68ba6f60e99c651acc6d707556927e99e653403ea57131e628） | `B 1 9` d(O1···O9) | 4.200→2.400 Å，18×−0.100（19 点，**由外向内**） | prep/RC_42A_seed.xyz（d=4.20，H2 在 O1 指向 O9） | 长程剖面 ≥4.0 Å：有无第二极小值/浅阱 |
| T3c | T3c_revscan_H2O9.gjf（sha256 f16801286becbd16f7fde94d3e6fe42fc320d334c9d351320c9c14668e31297c） | `B 2 9` d(H2–O9) | 1.077→3.577 Å，25×0.100（26 点） | jobs/A_RC_last.xyz（sha256 303ec8b48b90fdb1369e31e5eb667b1d222098e29a87a91f11ff6598ffb5afe6，产物型复合物极小值） | 反向单坐标剖面（H2–O7 单坐标）+ 顺带拉长 O···O |
| T3d | T3d_scan_H2N8.gjf（sha256 730b19963cdf2631c08fe5d703fd9a7e39541bd5cff45f75d4faaf84a845be3c） | `B 2 8` d(H2–N8) | 3.068→1.068 Å，16×−0.125（17 点） | prep/RC_3A_seed.xyz | 另一条 PT 通道：N 侧受体 |
| T3e | T3e_scan_H3O9.gjf（sha256 4b78b90368b7da3f9e7c867bae2065841da156715025e3b83401cfe7fdd22311） | `B 3 9` d(H3–O9) | 3.420→1.020 Å，16×−0.150（17 点） | prep/RC_3A_seed.xyz | 另一条 PT 通道：H3O+ 的另一个氢 |

- 扫描输入由 qm_input_writer 生成（坐标直接取自种子 xyz），再以 edit 追加 `B …` 扫描行
  （qm_input_writer 对「opt=modredundant + end_setting 含 S」会报内部 mismatch，故分两步；坐标仍来自工具输出）。
- T3a–T3e 全部**只扫一个坐标、不冻结任何坐标**：这是为了避免 913 的冗余坐标（l103）失败。
- 未提交草稿：jobs/T3b_sepscan_OO_long.gjf（sha256 8fb94fc5109a6f43c8900958f67b6f0ad104bfab2a99c3753585ef45de7e0fa7，原 2.457→4.957 外向扫描）——
  因 912 在第 11 点（d=2.957）外向行走时已发生平坦区收敛停滞（见 §3），改用 T3b（由外向内）覆盖同一区间。

## 2. 旧失败点逐项证据（原文行号；既有原生日志未被改动）

### jobs/B_sepscan_OO.log（job 912，sha256 89a0bdad76c805e36b025848a3723b74c14c119498e8da540d495401981e23df，45146 行）
- 扫描定义：`B 1 9 S 20 0.050`（松弛扫描 d(O1···O9) 2.457→3.457，21 个扫描点）；`# opt=(modredundant,maxstep=10) B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight`，%nprocshared=12。
- 行 227 原文：` Number of steps in this run=     88 maximum allowed number of steps=    114.`
- 前 10 个扫描点收敛（`Optimization completed.` 出现在行 1869/5219/6497/8654/10526/11802/13390/15834/17401/18675），
  第 11 点（d=2.957）走满 88 步未收敛：
  - 行 45142–45143 原文：` Error termination request processed by link 9999.` / ` Error termination via Lnk1e in /home/ly/g16/l9999.exe at Thu Oct 15 17:33:42 2026.`
- 失败分类：**引擎自身收敛失败（NStep 耗尽）**，非平台/语法问题。最后数次 SCF 在
  −364.283966789 / −364.283915337 / −364.283967285 / −364.283915934 Eh 间往复（振幅 ~5×10⁻⁵ Eh ≈ 0.03 kcal/mol），
  即能量已平坦、几何判据不满足的**平坦区停滞**。
- 该点末帧（format_converter 导出 jobs/B_sepscan_OO_last.xyz，internal_coordinates 判定）：
  r(O1–H2)=1.941 Å、r(H2–O9)=1.018 Å、r(O1···O9)=2.957 Å、r(H2–N8)=2.118 Å，感知为 2 个片段，
  即质子已完全在 O9 上、体系是正在解离的 H2O···H-O-肟⁺ 复合物，而不是第二个极小值。

### jobs/B_ptscan_frozenOO.log（job 913，sha256 6fecdc7ef0e3c016020677d6eae99171a278e274239ee7b70a87c7e8d2fb7c03，4807 行）
- 扫描定义：`B 1 2 S 12 0.100` **并冻结** `B 1 9 F`（d(O1···O9)=3.00）；`# opt=(modredundant,maxstep=10) …`，%nprocshared=12。
- 行 4802–4804 原文：` SCX= 1.46D-01 DXMaxT= 1.86D+00 SCLim= 9.28D-01 Fact= 1.00D+00` / ` Error imposing constraints` / ` Error termination via Lnk1e in /home/ly/g16/l103.exe at Thu Oct 15 17:35:18 2026.`
- 发生时点：scan point 1 的第 12 个优化步（行 4635：`Step number  12 out of a maximum of   88 on scan point     1 out of    13`），
  且行 4799–4801 先出现 ` RedQX1 iteration 20 Try 5 … XScale= 0.60680190` / ` Old curvilinear step not converged, using linear step:`。
- 失败分类：**输入设计问题**——“同时扫 1–2 并冻结 1–9”的冗余内坐标集在质子被拉离 O1 时不可满足/病态，l103 拒绝施加约束；
  **零个可用扫描点**。→ 后续设计一律避免“扫描坐标 + 冻结坐标”组合。

## 3. 912 已收敛的 10 个扫描点（本批日志内部相减）

参考最低点 = 第 1 点 E = −364.295965302 Eh（= 904/905 同一驻点 −364.295965289，Δ≈2×10⁻⁹ Eh）。

| 扫描点 | d(O1···O9)/Å | E/Eh | ΔE/(kcal·mol⁻¹) |
|---|---|---|---|
| 1 | 2.4569 | -364.295965302 | 0.000 |
| 2 | 2.5069 | -364.295717593 | 0.155 |
| 3 | 2.5569 | -364.295064534 | 0.565 |
| 4 | 2.6069 | -364.294115192 | 1.161 |
| 5 | 2.6569 | -364.292952578 | 1.891 |
| 6 | 2.7069 | -364.291640836 | 2.714 |
| 7 | 2.7569 | -364.290229540 | 3.599 |
| 8 | 2.8069 | -364.288756627 | 4.524 |
| 9 | 2.8569 | -364.287251381 | 5.468 |
| 10 | 2.9069 | -364.285736769 | 6.419 |

- 逐点单调上坡（最大步进 0.95 kcal/mol），**前 10 点无内部极大、无第二个极小值**；
  伴随质子逐步定位到 O9（d(1,2): 1.381→1.834 Å，d(2,9): 1.077→1.029 Å），即 H 键复合物沿解离方向单调升能。

## 4. 判定口径（写死，供审计复核）
- 「内部极大」= 逐点 E 序列中存在 i 使 E(i) > E(i−1) 且 E(i) > E(i+1)（并给出相对该剖面最低点的 ΔE）。
- 「第二个极小值」= 除全局最低点外存在 j 使 E(j) < E(j−1) 且 E(j) < E(j+1)。
- 能量只在本批 Gaussian 日志之间相减；不得混入历史 ORCA（23.13/10.44/13.46）或旧 Gaussian 0 的数值。
- 只把「约束优化在每个扫描点收敛（Optimization completed.）」的点计入剖面；未收敛点单独列出并标明。
