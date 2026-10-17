# HI1_E1 / lane1 — product 端点 (I1) 构象源 provenance（ts_0008 补齐 conformers.product 的依据）

方法一句：Gaussian 16（`/home/ly/g16/g16`）B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight + SCRF=(CPCM,Solvent=DMSO)，q0/m1（本机无 ORCA；能量只在本批 Gaussian 原生日志内相减）。

> 性质声明：本文件只记录**产物端点显式构象源**的来源、原子序/键表核验与 heavy_atom_binding 换算。
> 它**不主张** I1 是 IRC 终点、不主张任何能垒数值、不主张本步几何是极小值（极小值须由工作流自身 product_endpoint 的 Opt+Freq 日志判定）。

## 1 产物（绝对路径 + sha256）

| 文件 | sha256 | 说明 |
|---|---|---|
| /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/build/I1_S_start.xyz | c9d59aeab418c248629922ee37d4ea3822c64b7128dd63b3034d3c8c5ec2df3d | 41 原子产物起点几何（job_51 序；来源见 E1/build/I1_start_from_job51.xyz） |
| /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2EM1/build/I1_S_start_bonded.mol | 69de27c2a3319074932fb4bb6e2107431e11608f240df8948bb549b8b7921fd9 | 上游（lane3）已建含键表 MOL；本次**逐原子复核后**逐字节复制 |
| /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/build/I1_S_start_bonded.mol | 69de27c2a3319074932fb4bb6e2107431e11608f240df8948bb549b8b7921fd9 | 本 lane 自持副本（内容与上行逐字节相同，避免跨 lane 文件被改动） |
| /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/verify_product_endpoint.py | 47dbadaddfa471928cbe933f800ae6fc40eaeaf85f344bd4e341a177c3bdcc68 | 本文件所述核验脚本（Read-only，无 QM） |

注：平台 `format_converter` 的 xyz→mol 会丢键表（issue #179），故未使用；键表直接采用已核验的 V2000 键块。

## 2 核验命令与输出（可复现）

```
cd /home/ly/Cloudra-mechanism-agent && python3 gold_finish_20261015/HI1/E1/verify_product_endpoint.py
```

关键输出（逐字）：

- `given MOL atom order+coords identical to xyz (max dev 2e-4 A): True`（41/41 原子元素 + 坐标一致，无重排）
- `bond tables identical after Kekulize-normalisation (xyz-perceived vs given MOL): True`
- `canonical SMILES identical: True C=C(C)N1CCC[C@H]1C(=O)O.O.O=Cc1ccccc1`
- `n_atoms = 41  n_fragments = 3`，`formula = C15H21NO4`（= 声明 reactant_smiles 的同分异构公式）
  - frag0 (24 原子) = `C=C(C)N1CCC[C@H]1C(=O)O` = 烯胺（N-异丙烯基脯氨酸）
  - frag1 (3 原子) = `O` = 水
  - frag2 (14 原子) = `O=Cc1ccccc1` = 苯甲醛
  → 与声明 product_smiles `[CH3:1][C:2](=[CH2:3])[N:20]2[CH2:19][CH2:18][CH2:17][C@H:16]2[C:14](=[O:13])[OH:15].[O:4]([H:21])([H:22]).[O:5]=[CH:6][c:7]1[cH:8][cH:9][cH:10][cH:11][cH:12]1` 的**片段组成与连接性一致**
- 形式电荷：全部 0（xyz 键级感知结果），总电荷 0 → 与 reaction.charge=0 一致
- 关键键（1-based，文件序，Kekulé）：`1-2:2`（C2=C3 双键，canonical 2=map2、1=map3）、`2-3:1`、`2-4:1`（**C2–N20 已成键**，canonical 2=map2、4=map20）、`4-8:1`、`8-9:1`、`9-10:2`（Cα–COOH）、`11-24:1`（O15–H）、`25-26:1`、`25-27:1`（水 O–H×2）
- CIP（RDKit AssignStereochemistryFrom3D + AssignCIPLabels）：
  - I1 文件：`[(8, 'C', 'S')]` → 唯一立体中心 = 文件原子 8 = Cα = **S**
  - 声明 product_smiles：`[(7, 16, 'S')]` → map16 = **S**；声明 reactant_smiles：`[(15, 16, 'S')]` → map16 = **S**
  - `chirality-consistent substructure match present: True` → 声明 product_smiles 的立体标记与本几何一致

（同时复核 RC 侧：`RC file CIP (3D): [(28, 'C', 'S')]`，与 job 907 的 Cα=S 一致。）

## 3 heavy_atom_binding 换算（本次提交值）

声明 product_smiles 的重原子书写序（RDKit 读回 map 号）：`[1, 2, 3, 20, 19, 18, 17, 16, 14, 13, 15, 4, 5, 6, 7, 8, 9, 10, 11, 12]`

→ 按该序列出 I1_S_start.xyz 的 1-based 原子号（`GetSubstructMatch` 重原子匹配 + 反查原 41 原子序号）：

```
[3, 2, 1, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 29, 30, 31, 32, 33, 34, 35]
```

- 双射核验：`bijection (20 distinct): True`
- 元素逐位核验：`element-wise match: True`（声明序符号 C,C,C,N,C,C,C,C,C,O,O,O,O,C,C,C,C,C,C,C = 文件对应位符号）
- 与 reactant 侧同一约定（文件序 = canonical 绑定序，重原子在前 20 位不成立——产物文件的重原子散布在 1–11、25、28–35）。

## 4 本文件不主张的事

- 不主张 I1_S_start.xyz 已是极小值（需 product_endpoint Opt+Freq 判定）。
- 不主张 rc→I1 存在单个鞍点（需 TS freq + IRC 证据）。
- 不主张任何 ΔE‡ 数值。
