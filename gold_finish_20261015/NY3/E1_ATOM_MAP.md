# NY3_E1 · ts_0007 声明中的 atom_map 推导（第三任 Coordinator，2026-10-15 23:3x）

## 为什么有这份文件
durable TS run 对创建会话绑定（owner），上一任会话 as_7479852819ea48c0 建的 ts_0002（rev13 卡在 stage=map，failure_class=**atom_map_missing**）与 ts_0003 对本继承会话**拒绝续跑**：
ts_resume(run_id="ts_0002", changes={reaction:{atom_map:[...]}}) → "ts_resume: TS process belongs to a different project or owner"
（同型先例：上一任对 ts_0001 的报错 call_id = tc_6ab2ff0cecea459d；已并入 GitHub issue #180）。
处置（沿 ts_0002 替代 ts_0001 的先例）：**新建 ts_0007**，用同一批 prep 输入 + **补齐缺失的 atom_map** 重新起链。

## ts_0007 声明要点（E1 = RC → I1，OH⁻ 加成）
- reaction：reactant_smiles `[Na+].[OH-].COC=O`；product_smiles `[Na+].CO[C@H]([O-])O`；charge 0；multiplicity 1；electronic_character closed_shell
- **atom_map = [1,4,5,6,2,7,8,9,10,11,3]**（文档口径：product-coordinate order，每个值是 1-based 的 reactant 原子号，含显式 H）
- reaction_center = **[[2,6],[6,7]]**（文档口径 1-based：成 O1–C4；断 C4=O5 π）
  ※ 旧声明里的 [[1,5],[5,6]] 只在 0-based 读法下化学正确 ⇒ 属声明偏差，新 run 按文档改为 1-based（本包记为一处勘误）。
- conformers/guess/方法/资源与 ts_0002 逐字相同（见 ts/ts_0007/declare.json 及 ts/ts_0002/declare.json 对照）：
  reactant = prep/rc.xyz + prep/build/g_RC_w283/guided_assembly/assembly/complex_candidate_000.mol（builder 原生 MOL，含 bond block + M CHG）
  product  = prep/i1.xyz + prep/i1.mol；guess = prep/ts_e1_guess.xyz（provided，evidence_refs = prep/GUESS_PROVENANCE.md）
  engine=gaussian / b3lyp / def2svp / "empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=water)" / execution 8c·10000MB

## 映射推导（元素逐一核对，不是距离启发式）
reactant 端点（built，component-wise；与 prep/rc.xyz 同序）：
1 Na（M CHG +1）｜2 O = O1 氢氧根 O｜3 H = H6（键在 O1）｜4 C = C2 甲基 C｜5 O = O3 甲氧基 O｜6 C = C4 羰基 C｜7 O = O5 羰基 O（C4=O5 双键）｜8,9,10 H 甲基 H｜11 H 甲酰 H（键在 C4）

product 端点（built）：
1 Na（M CHG +1）｜2 C = C2 甲基 C（键 O3 + 3H）｜3 O = O3 甲氧基 O｜4 C = C4 四面体 C｜5 O = O1（键 C4 + H11）｜6 O = O5 烷氧 O⁻（M CHG −1）｜7,8,9 H 甲基 H｜10 H 键在 C4 上（甲酰 H）｜11 H 键在 O5(=O1) 上

⇒ 映射：p1←r1, p2←r4, p3←r5, p4←r6, p5←r2, p6←r7, p7←r8, p8←r9, p9←r10, p10←r11, **p11←r3**
（化学判据：OH⁻ 的 O/H 保持成键并接到 C4；羰基 O 变成烷氧 O⁻；元素多重集一致、双射。）

证据来源（本包实测 sha256；均为原生日志/原生构建文件，不改写）：
- gold_finish_20261015/NY3/prep/rc.xyz（sha c2e0db4302f9…）、prep/i1.xyz（sha d1b3b5a35548…）、prep/i1.mol（sha c4165dfc33a8…，含 bond block + M CHG）
- 同批 ts_0002 的 built 端点（与 ts_0007 同输入文件）：ts/ts_0002/build/input_0001/reactant/seed.mol（sha 05528d3d1333…，键表 2-3/4-5/5-6/6-7 双/4-8/4-9/4-10/6-11，M CHG 1=+1, 2=−1）、ts/ts_0002/build/input_0001/product/seed.mol（sha c4165dfc33a8… = prep/i1.mol，键表 2-3/3-4/4-5/4-6/2-7/2-8/2-9/4-10/5-11，M CHG 1=+1, 6=−1）
- ts_0007 build 完成后须复核其 built 端点原子序与上表一致（本包下一步）。

## 关联
- ts_0002 的 blocking 原文："no atom_map was declared: the reactant→product atom correspondence is ambiguous..."，其 atom_details 给出 reactant atoms 1=Na,2=O,3=H,4=C,5=O,6=C,7=O,8=H,9=H,10=H,11=H；product atoms 1=Na,2=C,3=O,4=C,5=O,6=O,7=H,8=H,9=H,10=H,11=H（与上表一致）。
- 与该映射一致的声明细化：product_smiles 的 CIP [C@H]（C4 为真实立体中心，来源 prep/PREP.md §4.2 与 i1.mol 的 RDKit 判定）——声明细化，不是改图。
