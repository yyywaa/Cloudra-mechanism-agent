# lane3 (HI1_E2/EM1) · 绑定/map 校验证据 · 2026-10-17

本文件记录 ts_0009（通道 A = HI1_E2, major_face -> HI1_I2 map6=S）的 41 原子 atom_map、
reaction_center 与两端 heavy_atom_binding 的**逐元素**校验过程与原始输出。
它是平台输入声明（ts_resume）的证据引用，不是 QM 化学证据。

## 1 绑定的具体结构（本 run 的 bound geometry，1-based 序 = ORCA job_51 序）

| 角色 | 路径 | sha256 |
|---|---|---|
| reactant xyz | ts/ts_0009/build/input_0003/reactant/seed.xyz（= gold_finish_20261015/HI1/E1/build/I1_S_start.xyz） | c9d59aeab418c248629922ee37d4ea3822c64b7128dd63b3034d3c8c5ec2df3d |
| reactant mol | ts/ts_0009/build/input_0003/reactant/seed.mol（= E2EM1/build/I1_S_start_bonded.mol） | 69de27c2a3319074932fb4bb6e2107431e11608f240df8948bb549b8b7921fd9 |
| product xyz | ts/ts_0009/build/input_0002/product/seed.xyz（= E2EM1/build/TS_guess_E2_j58f7.xyz） | 9e5ccc2fe5dde2e4c1900ad53cc8c1ddbae0e654a618c138adaffa58dd522e38 |
| product mol | ts/ts_0009/build/input_0002/product/seed.mol（= E2EM1/build/TS_guess_E2_j58f7_adduct.mol） | 8135b32285871a17ae14a25574bb3ac20ec062e54ceeb11b2b8e6737010a1dfa |

## 2 reaction.atom_map = 恒等（product 序，1-based 指向 reactant 原子）

`[1,2,3,...,41]`（product 第 i 个原子 ↔ reactant 第 i 个原子）

理由（本机 RDKit 逐元素复核，2026-10-17）：
- 两文件元素序列完全一致（41 原子：1-3 C,C,C; 4 N; 5-9 C; 10,11 O; 12-24 H; 25 O; 26,27 H; 28 O; 29-35 C; 36-41 H）。
- 在恒等映射下，只有反应中心的键级改变：reactant C1=C2 / C2-N4 / O28=C29（无 C1-C29）；
  product C1-C29（新增）/ C2=N4 / C28-C29。其余重原子连接性完全相同。
- 41 个 H 的重原子归属在恒等映射下逐一相同（H12,13->C1; H14-16->C3; H17,18->C5; H19,20->C6;
  H21,22->C7; H23->C8; H24->O11; H26,27->O25; H36->C29; H37-41->C31-C35）。

reaction_center（bound 序 1-based）= `[[1,29],[2,4],[2,1],[28,29]]`
（平台内部 0-based 存储为 `[[0,28],[1,3],[1,0],[27,28]]`，已回读确认一致。）
生成中的 C3-C6 键 = bound 原子 **1 与 29**。

## 3 heavy_atom_binding（1-based 本文件坐标序，按声明 SMILES 重原子顺序）

**reactant**（declared: `[CH3:1][C:2](=[CH2:3])[N:20]2[CH2:19][CH2:18][CH2:17][C@H:16]2[C:14](=[O:13])[OH:15].[O:4]([H:21])([H:22]).[O:5]=[CH:6][c:7]1[cH:8][cH:9][cH:10][cH:11][cH:12]1`）

    indices = [3,2,1,4,5,6,7,8,9,10,11,25,28,29,30,31,32,33,34,35]

**product**（declared: `C/C(C[C@H]([O-])c1ccccc1)=[N+]1\CCC[C@H]1C(=O)O.O`）

    indices = [3,2,1,29,28,30,31,32,33,34,35,4,5,6,7,8,9,10,11,25]

校验脚本（本机 RDKit，2026-10-17）：对每个 SMILES 重原子检查元素、显式 H 数、以及重原子成键图映射。
原始输出：

    reactant smiles heavy: 20  concrete heavy: 20  idx: 20
      heavy-graph+H-check: OK
    product smiles heavy: 20  concrete heavy: 20  idx: 20
      heavy-graph+H-check: OK
    ALL: True

（脚本内容：用 Chem.AddHs(Chem.MolFromSmiles(declared)) 逐位比对 concrete mol 的元素与 H 数，
并把 SMILES 的每条重原子键映射到 concrete mol 中检查存在性与键级。）

## 4 平台拒绝样本（issue 证据，逐字）

(a) product 身份校验（is_success=false）：

    ts_resume: product: inherited heavy-atom binding is invalid: The concrete structure's molecular graph or stereochemistry differs from the declared SMILES.
    Declared identity: CC(C[C@H]([O-])c1ccccc1)=[N+]1CCC[C@H]1C(=O)O.O;
    concrete identity: C/C(C[C@H]([O-])c1ccccc1)=[N+]1\CCC[C@H]1C(=O)O.O.
    Changing binding indices cannot repair this identity mismatch.

根因：声明缺 C2=N4 的 E/Z。RDKit 复核：

    ts/ts_0009/build/input_0002/product/seed.mol canonical isomeric SMILES =
    C/C(C[C@H]([O-])c1ccccc1)=[N+]1\CCC[C@H]1C(=O)O.O   （与 concrete identity 逐字一致）
    3D CIP: 1-based 原子 8 = S（Cα）, 原子 29 = S（aldol C, map6）; stereo bond 2-4 DOUBLE STEREOCIS

（注意：这是**几何预测/身份读数**，不是 QM 端点结论；通道 A 的最终 CIP 以 TS/端点 log 为准。）

(b) reactant 绑定不唯一（rev 16: status=blocked, stage=build, failure_class=input_identity_unconfirmed）：

    reactant: The concrete structure has 2 symmetric heavy-atom bindings; without concrete atom-map labels the binding is not unique.

根因：遗产标签 SMILES 中 [CH3:1]/[CH2:3] 与 concrete 原子 3(CH3)/1(CH2) 之间的对应未固定，重原子匹配有 2 解；
本文件 §3 的显式 indices 用显式 H 数消除了该歧义。

## 5 限定

以上全部是本道本机（Gaussian 16 批次之外）的**输入/身份校验**：它只证明声明的 map/binding 与已核验的几何一致，
不证明任何鞍点、能垒、IRC 连通性或 CIP 的 QM 结论；那些只来自本批 Gaussian 16 的原生日志。
