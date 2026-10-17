# HI1_E1 / lane1 — 提供几何 provenance（ts_0004 修订依据）

方法一句：Gaussian 16（`/home/ly/g16/g16`）B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight + SCRF=(CPCM,Solvent=DMSO)，q0/m1（本机无 ORCA；能量只用本批 Gaussian 日志内部相减，绝不与历史 ORCA 相减）。

> 性质声明：本文件记录**两个几何输入的来源与绑定序换算**。`TS_guess_merged.xyz` 是**几何构造的初猜，不是鞍点**；RC 是 job 907（本批 Gaussian）已验证的极小值。TS 是否合格必须由 ts_0004 自己的 OptTS/freq/IRC 日志判定。

## 1 产物（绝对路径 + sha256）

| 文件 | sha256 | 说明 |
|---|---|---|
| /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/build/RC_start.xyz | f4eb0ba6f085114c97cb13bcdbe03a8613a2f95262782bcb5fb9da5c6d9b93c0 | job 907 的**输入**几何（41 原子，job_51/ORCA 序），人工建预复合物 |
| /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/runs/RC_optfreq/RC_optfreq.log | fa28545612332f69c60c0b778cd5dd1907b22b8ad36f6b1da7811da1295563ba | job 907：RC 极小值，0 虚频，E(RB3LYP)=−939.308829219 Eh，Cα=S |
| /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/build/TS_guess_merged.xyz | 74d3d3e12d6c48398857a986a29034546b9fb93ace4388fe2a2d4fbbcc87fe13 | 合并边单 TS **初猜**（job_51 序，Cα=S） |
| /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/build/build_ts_guess.py | 330d0397bb175480f527d74cd63101680ee4bb579ac4f8541ba41432bb197686 | 初猜生成脚本（纯几何约束，无 QM） |
| /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/lane1/make_lane1_binding_order.py | 49cb48632e9c61c95020ab5ef59ce3d982935b41197911c2109fe947e831eefe | 本文件所述绑定序换算脚本（只换原子顺序，不动坐标） |
| /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/lane1/RC_S_canonical.xyz | 71b23e07b73a7241e19c3c94e927040f5f113f815184bfa44387d58bbc0e6597 | **提交给 ts_0004 的 reactant 构象**（canonical 绑定序） |
| /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/lane1/RC_S_canonical.mol | cbdb052b5e49b7ac3872df703b7b4e6e7ee1ade61d6cfad0232986fb56c2459c | 同上，含键表（41 原子/40 键，3 组分） |
| /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/lane1/TS_guess_merged_canonical.xyz | a2c0fa28667eb5afd814d8b876f40dd5873967c8a63973ff89bf9b0d0b980c4c | **提交给 ts_0004 的 provided TS 初猜**（canonical 绑定序） |
| /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/lane1/TS_guess_merged_canonical.mol | 0257e635797cdff23f7c155a505535a5d7955b94d3e784dd24096a201d317279 | 同上，含键表 |
| /home/ly/Cloudra-mechanism-agent/ts/ts_0004/build/input_0001/reactant/generated_seed.mol | c540005626db7787861aa56695c4306ce7c81f6387b1442884532ee0d5b321e0 | run 自己的 canonical 序参照（41 原子/40 键） |

## 2 canonical 绑定序的定义（ts_0004 rev5 实测）

41 原子 = 20 重原子（按声明 reactant SMILES 书写序，即 map 号序 1,2,4,3,5…20）+ 21 个氢（按 RDKit AddHs 顺序，逐重原子升序追加）。
由 run 自己的 `generated_seed.mol` 键表实测确认：canonical 1 带 H5,H6,H7；canonical 4 带 H8,H9,H10；canonical 2–3 双键；canonical 28 带 H34（stereo parity 字段=6）且键 28–29、28–32、26–28；canonical 32 带 H41。

## 3 map 号 → canonical 绑定序 → job_51 序 换算表（41 行，双射）

| canonical | 元素 | map | 角色 | job_51 序 |
|---|---|---|---|---|
| 1 | C | 1 | 丙酮甲基 A | 3 |
| 2 | C | 2 | 丙酮羰基 C（C2） | 2 |
| 3 | O | 4 | 丙酮羰基 O（O4，离去成水） | 25 |
| 4 | C | 3 | 丙酮甲基 B（失 H22 后成 C2=C3） | 1 |
| 5 | H | — | 甲基 A–H | 14 |
| 6 | H | — | 甲基 A–H | 15 |
| 7 | H | — | 甲基 A–H | 16 |
| 8 | H | — | 甲基 B–H | 12 |
| 9 | H | — | 甲基 B–H | 13 |
| 10 | H | 22 | 甲基 B–H = **H22**（转移质子） | 27 |
| 11 | O | 5 | 苯甲醛 O（旁观） | 28 |
| 12 | C | 6 | 苯甲醛 CHO 碳 | 29 |
| 13 | C | 7 | 芳环 ipso | 30 |
| 14 | C | 8 | 芳环 CH | 31 |
| 15 | C | 9 | 芳环 CH | 32 |
| 16 | C | 10 | 芳环 CH | 33 |
| 17 | C | 11 | 芳环 CH | 34 |
| 18 | C | 12 | 芳环 CH | 35 |
| 19 | H | — | CHO–H | 36 |
| 20–24 | H | — | 芳环 H（canon20→j51 37, 21→38, 22→39, 23→40, 24→41） | 37–41 |
| 25 | O | 13 | 羧基 C=O | 10 |
| 26 | C | 14 | 羧基 C | 9 |
| 27 | O | 15 | 羧基 OH O | 11 |
| 28 | C | 16 | **Cα** | 8 |
| 29 | C | 17 | 环 CH2（邻 Cα） | 7 |
| 30 | C | 18 | 环 CH2 | 6 |
| 31 | C | 19 | 环 CH2（邻 N） | 5 |
| 32 | N | 20 | **N20** | 4 |
| 33 | H | 15 | 羧基 O–H | 24 |
| 34 | H | 16 | Cα–H | 23 |
| 35,36 | H | — | canal29 的 2H（j51 21,22） | 21,22 |
| 37,38 | H | — | canal30 的 2H（j51 19,20） | 19,20 |
| 39,40 | H | — | canal31 的 2H（j51 17,18） | 17,18 |
| 41 | H | 21 | **H21**（N–H 质子） | 26 |

换算依据：`build_ts_guess.py` 自带注释与几何（其内部 C2=X[1]、O4=X[24]、C1=X[2]、C3=X[0]、N20=X[3]、H21=X[25]、H22=Y[26]）与上述 job_51↔canonical 对应一致；并经受键长体检（见 §6）。

## 4 关键距离（实测，取自本包重排后的文件；单位 Å）

| 对 | canonical 对 | RC（job 907 起点几何） | TS 初猜 |
|---|---|---|---|
| C2–N20 | 2–32 | 4.008（未成键） | 1.950 |
| C2=O4 | 2–3 | 1.230 | 1.550（部分断裂） |
| C2–C3 | 2–4 | 1.505 | 1.400（部分双键） |
| C3–H22 | 4–10 | 1.094 | 1.093 |
| N20–H21 | 32–41 | 1.020 | 1.020 |
| O4···H21 | 3–41 | 1.898（N–H···O=C 预络合） | 1.437（桥接） |
| O4···H22 | 3–10 | 2.519 | 1.713（H22 转向 O4） |

## 5 立体身份（RDKit 3D 实测，本包重跑）

`MolFromXYZFile → DetermineBonds(charge=0) → AssignStereochemistryFrom3D → AssignCIPLabels`：

- `RC_S_canonical.xyz`：`[(28, 'C', 'S')]` → **唯一立体中心 = canonical 28 = Cα = S** ✓
- `TS_guess_merged_canonical.xyz`：`[(28, 'C', 'S')]` → Cα = S ✓

（与 PLAN §3 一致：job_51/52/54/64 历史几何的脯氨酸中心是 R，本包 S 几何由 z 镜像/重建得到；job 907 实测 Cα=S。）

## 6 换算体检（脚本输出，可复现）

- 元素一致性：41/41 匹配，0 处不一致。
- 键长体检：重排后按 run 自己的键表逐键测距，RC 最长键 1.527 Å（键 29–30），TS 初猜最长键 1.550 Å（键 2–3，即 C2–O4 的构造距离）→ 置换正确、无错位原子。
- 置换为双射（1..41 全出现一次）。

## 7 本步向 ts_0004 声明的 reaction_center（canonical = 绑定序，1-based）

break：(2,3)=C2=O4、(4,10)=C3–H22、(32,41)=N20–H21
form：(2,4)=C2=C3 π、(2,32)=C2–N20、(3,41)=O4–H21、(3,10)=O4–H22

（对应题源 map 号 bond_changes break [[2,4],[3,22],[20,21]] / form [[2,3],[2,20],[4,21],[4,22]]，共 7 对。）

## 8 本文件不主张的事

- 不主张 TS 初猜是鞍点（无 QM 证据）。
- 不主张能垒数值（需 ts_0004 自身 TS/端点日志）。
- 不主张 (S)-I1 端点身份（IRT 端点需 IRC + 端点 Opt/Freq 证据）。
