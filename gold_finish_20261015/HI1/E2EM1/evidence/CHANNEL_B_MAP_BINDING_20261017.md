# lane3 通道 B（HI1_EM1, minor_face -> HI1_M1 map6=R）· map / binding / 身份证据 · 2026-10-17

用途：记录 durable run **ts_0012**（`/home/ly/Cloudra-mechanism-agent/ts/ts_0012`，本会话 2026-10-17 经
`ts_prepare` 新建）的 41 原子 atom_map、reaction_center、两端 heavy_atom_binding 与声明 SMILES，
全部附本机逐元素复核的原始输出。**这不是 QM 化学证据**（不含任何鞍点/能垒结论）。

## 1 声明（ts_prepare 实际提交，run ts_0012 revision 5, status=waiting, stage=build）

- reactant_smiles（标签 = 题源 map 号）：
  `[CH3:1][C:2](=[CH2:3])[N:20]2[CH2:19][CH2:18][CH2:17][C@H:16]2[C:14](=[O:13])[OH:15].[O:4]([H:21])([H:22]).[O:5]=[CH:6][c:7]1[cH:8][cH:9][cH:10][cH:11][cH:12]1`
- product_smiles：
  `[CH3:1]/[C:2]([CH2:3][C@@H:6]([O-:5])[c:7]1[cH:8][cH:9][cH:10][cH:11][cH:12]1)=[N+:20]1\[C@H:16]([C:14](=[O:13])[OH:15])[CH2:17][CH2:18][CH2:19]1.[OH2:4]`
  （[C@@H:6] = 通道 B 的 aldol 碳 map6 = R；C2=N4 的 E/Z 以 / \ 明确写出，否则平台身份校验拒绝，见 §4）
- charge 0 / multiplicity 1 / electronic_character closed_shell
- atom_map = 恒等 `[1,2,...,41]`（product 第 i 原子 ↔ reactant 第 i 原子，含全部 H）
- reaction_center = `[[1,29],[2,4],[2,1],[28,29]]`（bound 序 1-based；生成中的 C3–C6 = 原子 **1 与 29**）

## 2 绑定的具体结构（bound 序 = ORCA job_51 序；本道三个文件元素序列逐一致）

| 角色 | 路径 | sha256 |
|---|---|---|
| reactant xyz | gold_finish_20261015/HI1/E2EM1/build/I1_S_from_job59.xyz | 22f730d231bc91c39f73851e62b9d8eba0db6357a7aaeeddab6484226df2e697 |
| reactant mol（**本会话新造**；原 `I1_S_from_job59.mol` 只有坐标、无键块） | gold_finish_20261015/HI1/E2EM1/build/I1_S_from_job59_bonded.mol | 0a8bed4bb738aca52ad5a3aee3f38a22ef9b902fa32be66c89294a476c642e49 |
| product/TS seed xyz | gold_finish_20261015/HI1/E2EM1/build/TS_guess_EM1_j59f9.xyz | a7b50b7c23031e9c527ecaad4e08961bcfcec26880cac834b93f6bbfd5f214be |
| product mol（**本会话新造**，加成物拓扑） | gold_finish_20261015/HI1/E2EM1/build/TS_guess_EM1_j59f9_adduct.mol | f25e6cbc6c45b646b001762f76ef337de559376ca698a81d6e0f7dcf4369929a |
| 生成脚本 | gold_finish_20261015/HI1/E2EM1/build/make_mol_EM1_lane3.py | fac51f609bcd66e13fcdb6e693ab602b8ec5db036c51088c656e52d2e7b4a8be |
| 校验脚本 | gold_finish_20261015/HI1/E2EM1/build/verify_channelB_lane3.py | 94d543d68869d1b081cd4ef0007c1e01a8ceb8d55ececa23f4e8c05e074ac714 |

拓扑（脚本内声明，仅键表；坐标一律取自现有 xyz）：加成物 = C3–C6 成键 + iminium C2=N20⁺ + alkoxide C6–O5⁻，
苯环 Kekulé 双键 (30,31),(32,33),(34,35)；生成物 = 41 原子 / 41 键 / 2 分片；反应物 = 41 原子 / 40 键 / 3 分片。

## 3 校验原始输出（`python3 build/verify_channelB_lane3.py`，2026-10-17）

    reactant(B) mol: atoms=41 bonds=40 fragments=3 -> .../I1_S_from_job59_bonded.mol
    reactant(B) chiral centres (0-based idx, CIP): [(7, 'S')]
    adduct(B) mol: atoms=41 bonds=41 fragments=2
    adduct(B) chiral centres (0-based idx, CIP): [(7, 'S'), (28, 'R')]
      stereo bond (1-based): 2 4 DOUBLE STEREOCIS
    === reactant(B) declared heavy: 20 concrete heavy: 20 indices: 20
      element/H/graph check: OK
    === product(B) declared heavy: 20 concrete heavy: 20 indices: 20
      element/H/graph check: OK
    declared product(B) canonical : C/C(C[C@@H]([O-])c1ccccc1)=[N+]1/CCC[C@H]1C(=O)O.O
    concrete  product(B) canonical: C/C(C[C@@H]([O-])c1ccccc1)=[N+]1/CCC[C@H]1C(=O)O.O
    IDENTITY MATCH: True
    declared reactant(B) canonical: C=C(C)N1CCC[C@H]1C(=O)O.O.O=Cc1ccccc1
    concrete  reactant(B) canonical: C=C(C)N1CCC[C@H]1C(=O)O.O.O=Cc1ccccc1
    ALL: True

（校验内容：对每个 SMILES 重原子比对元素、**显式 H 数**与重原子成键图；仅反应中心键级变化。）

heavy_atom_binding（1-based 本文件坐标序，按声明 SMILES 重原子顺序）：

    reactant = [3,2,1,4,5,6,7,8,9,10,11,25,28,29,30,31,32,33,34,35]
    product  = [3,2,1,29,28,30,31,32,33,34,35,4,8,9,10,11,7,6,5,25]

几何读数（RDKit 3D，0-based idx；+1 = 1-based）：Cα(7+1=8)=S、aldol C(28+1=29)=**R** ⇒ 与题源
HI1_M1 (map6=R) 一致。**这是镜像/几何预测，不是 QM 端点结论。**

## 4 平台输入校验口径（本道踩坑记录）

- 声明 SMILES 必须与 concrete 图谱**一致（含 C2=N4 的 E/Z）**，否则：
  "ts_resume: product: inherited heavy-atom binding is invalid: The concrete structure's molecular graph or
  stereochemistry differs from the declared SMILES. ... Changing binding indices cannot repair this identity mismatch."
- 若只给"标签但不含 concrete 对应"，平台可能报
  "reactant: The concrete structure has 2 symmetric heavy-atom bindings; without concrete atom-map labels
  the binding is not unique." → 用显式 `heavy_atom_binding.indices`（H 数逐一核对）消歧。
- 通道 A 的同类修复见 `evidence/BINDING_AND_MAP_VERIFICATION_20261017.md`（sha256 3432e7c1…）。

## 5 ts_prepare 回读（原文节选）

    run_id ts_0012, revision 5, status waiting, stage build, blocked null
    waiting_for [{job_id:1000, purpose:candidate_opt, state:ready, req_cpus:8, req_memory_mb:10240,
                  input_path:/home/ly/Cloudra-mechanism-agent/ts/ts_0012/jobs/declaration_0001/candidate_opt/seed-opt.gjf}]
    reactant bound: ts/ts_0012/build/input_0001/reactant/seed.xyz sha256 22f730d231bc91c39f73851e62b9d8eba0db6357a7aaeeddab6484226df2e697
                    ts/ts_0012/build/input_0001/reactant/seed.mol sha256 0a8bed4bb738aca52ad5a3aee3f38a22ef9b902fa32be66c89294a476c642e49

## 6 方法（本 run 声明）

`lane3_g16_dmso` = Gaussian 16（/home/ly/g16/g16）B3LYP / **def2SVP（无连字符，issue #189）** +
EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight + SCRF=(CPCM,Solvent=DMSO)；q0/m1；8c / 10240 MB / priority 0。
ΔE‡ 参考态固定为 job 924（`runs/I1_optfreq/I1_S_optfreq.log`，-939.308218263 Eh，行 20025/22238）。
判虚频只看 band 表 + imaginary 行；`Low frequencies` 行首负值不是振动模。

## 7 限定

本文件只证明**输入声明与已核验几何一致**；鞍点性、能垒、IRC 连通性与端点 CIP 一律以 ts_0012 本批
Gaussian 16 的原生日志为准（尚未产生 ⇒ 目前该边为"缺测"）。
