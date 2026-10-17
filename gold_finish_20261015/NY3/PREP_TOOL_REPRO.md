# NY3 prep · 工具面最小复现清单（issue #179 素材）

范围：多组分 / 含 Na⁺ 复合物的 prep 链（结构生成 → 刚性几何编辑 → 格式转换 → 引导采样）。纯只读取证：本道未提交任何 QM 作业，未改平台代码 / DB / 进程。
日期：2026-10-15 ｜ 包：NY3（Coordinator as_7479852819ea48c0）｜ 道：small_mol(prep) ｜ 工作根：/home/ly/Cloudra-mechanism-agent
说明：下文 ".../" 均指工作根；引号内文字为工具返回的逐字内容（仅省略号处为原文省略）。

## P1 smiles_to_mol 对含 Na⁺ 多组分复合物：报 builder status='ok' 却「no MOL candidate」，且声明的 output_path 未创建、无取回通道

① 调用
smiles_to_mol(smiles="[Na+:7].[O-:1][H:6].[CH3:2][O:3][CH:4]=[O:5]", generate_3d=true, charge=0, multiplicity=1, output_path=".../gold_finish_20261015/NY3/prep/build/RC_src.mol", artifact_dir=".../gold_finish_20261015/NY3/prep/build/art_RC_src")
（同一现象在 I1 "[Na+:7].[CH3:2][O:3][CH:4]([O:1][H:6])[O-:5]"、I2 "[Na+:7].[CH3:2][O-:3].[CH:4](=[O:5])[O:1][H:6]"、P "[Na+:7].[CH3:2][O:3][H:6].[CH:4](=[O:5])[O-:1]" 上各复现一次）

② 观察
is_success=false；mol_content=""；xyz_path=""；message="Conversion raised an exception: the builder reported status='ok' but produced no MOL candidate: ['.../prep/build/art_RC_src/assembly/complex_candidate_000.xyz']. Check the SMILES and output_path, then retry."
同时磁盘上（同一 artifact_dir 内）：prepared_structure.json 含 "status": "ok"；assembly.json 含 "message": "1 complex candidate(s) from 32 sampled placements (complex mode). ..."；assembly/complex_candidate_000.mol 972 B，含完整键块与 "M  CHG  2   1   1   2  -1"。
声明的 output_path 不存在：sha256sum 输出 "sha256sum: prep/build/RC_src.mol: No such file or directory"。

③ 输入与证据文件
- 输入：SMILES 字符串（无输入文件）
- .../gold_finish_20261015/NY3/prep/build/art_RC_src/assembly/complex_candidate_000.mol  sha256 e1bdcd77c93316bec365bfac74a84bea226d0cf8d2d660fb8e204246fe14457a
- .../gold_finish_20261015/NY3/prep/build/art_RC_src/prepared_structure.json  sha256 f22a46be89db547161691e1601f99ec7a80b4d286662b42b6db8ef5176630e02
- .../gold_finish_20261015/NY3/prep/build/art_RC_src/assembly/assembly.json  sha256 2f9abde1a93b17e98c7ca4fd35cef54887c87f6895a89e6355ba0375147aaf7a

④ 期望行为：要么成功返回该候选的几何与文件路径（xyz_path / mol_content），要么给出候选被拒的具体原因；不应同时出现「builder status=ok + 磁盘有 MOL」与「no MOL candidate + output_path 不存在 + 无任何坐标返回」。

## P2 internal_coordinates(mode=transform) 把 Na⁺–O 离子接触按距离记为共价键，导致真实 C–O 键的 stretch 被判「在环上」而拒绝

① 调用
internal_coordinates(mode="transform", input_path=".../gold_finish_20261015/NY3/prep/i1.mol", charge=0, operations=[{"type":"stretch","atoms":[4,3],"new_length":2.00}], output_path=".../gold_finish_20261015/NY3/prep/build/TS2_guess.xyz")
（input_path 换成 .../prep/i1.xyz 同样被拒；对 C4–O5 即 atoms=[4,6] 的 stretch 亦被拒）

② 观察
is_success=false；operations_applied=[]；message="Invalid transform operation: stretch: bond 4-3 lies on a ring (the graph stays connected after cutting it); stretching it is not a rigid-fragment operation"
根因取证（同一文件的 analyze 返回，逐字）：
- "Formula: C2H5NaO3  Atoms: 11  Bonds: 13  Fragments: 1  Total charge: 0"
- "Bond orders: distance-inferred (all single)"
- "[Watched atom pairs]  r(Na1-O6)=2.166 Å  [bonded (bond order 1, ref 2.320)]  |  r(Na1-O3)=2.229 Å  [bonded (bond order 1, ref 2.320)]  |  r(Na1-O5)=2.531 Å  [bonded (bond order 1, ref 2.320)]  |  r(C4-O3)=1.425 Å  [bonded (bond order 1, ref 1.430)]"
- "Notes: - RDKit bond perception failed (Explicit valence for atom # 3 C, 4, is greater than permitted); bond orders were not perceived — bond info below is distance-inferred (all treated as single bonds)."
（该文件真实共价键 9 条、真实组分 3 个；Na⁺ 的 2.166 / 2.229 / 2.531 Å 均被判为 bond order 1 键，切 C4–O3 后甲醇盐仍经 Na–O3 连通，故判为环）

③ 输入与证据文件
- .../gold_finish_20261015/NY3/prep/i1.mol  sha256 c4165dfc33a88e26990c32b4c3911259ffc1b092b67aeeb1d595bea33feea184
- .../gold_finish_20261015/NY3/prep/i1.xyz  sha256 d1b3b5a35548d4c1dd9c02de631ee84894ac2628b884046c28d6d7080354cea3

④ 期望行为：stretch 的「是否成环」判定应基于输入文件的显式键表（或对金属–配体接触与共价键做可声明的区分），使真实共价键 C4–O3 / C4–O5 的刚性拉伸可用。

## P3 analyze 忽略 MOL 文件自带的键表与形式电荷，改按距离重猜

① 调用
internal_coordinates(mode="analyze", input_path=".../gold_finish_20261015/NY3/prep/build/art_I2_src/assembly/complex_candidate_000.mol", charge=0)

② 观察
"Formula: C2H5NaO3  Atoms: 11  Bonds: 11  Fragments: 1  Total charge: 0"、'Bond orders: distance-inferred (all single)'，并附与前条相同的 Notes（RDKit 键感知失败、距离启发式）。
而该 MOL 文件自身含 8 条键行与 "M  CHG  2   1   1   3  -1"（三个组分：Na⁺ / CH3O⁻ / HCOOH）。
同类：internal_coordinates(mode="analyze", input_path=".../gold_finish_20261015/NY3/prep/i1.mol", charge=0) 报 "Bonds: 13  Fragments: 1"，而该文件自身是 9 条键行 + "M  CHG  2   1   1   6  -1"。

③ 输入与证据文件
- .../gold_finish_20261015/NY3/prep/build/art_I2_src/assembly/complex_candidate_000.mol  sha256 af67740f8c76f18f0517573c8cb5590aa8bb603d3d1c706df624ebd1ce46f816

④ 期望行为：对带显式 bond block 与 M CHG 的 MOL 输入，身份报告（键表 / 键级 / 形式电荷 / 组分个数）应取自文件本身，而非按距离重猜。

## P4 format_converter 的 xyz→mol 丢 bond block（产物无键表、无 M CHG）

① 调用
format_converter(input_path=".../gold_finish_20261015/NY3/prep/rc.xyz", input_format="xyz", output_path=".../gold_finish_20261015/NY3/prep/rc.mol", output_format="mol")

② 观察
is_success=true，message 内含逐字提示 "Input xyz carries only coordinates (no bond/charge/stereochemistry), so the MOL/SDF output ..."；产物 rc.mol 的计数行为 " 11  0  0  0  0  0  0  0  0  0999 V2000"（bond 数 = 0），全文无 "M  CHG" 行。
（事实登记：ts_prepare 的 build 阶段在该结构文件上因缺键表而卡住，此点由包 Coordinator 实测确认；本条仅记录 MOL 产物事实。）

③ 输入与证据文件
- .../gold_finish_20261015/NY3/prep/rc.xyz  sha256 c2e0db4302f9f3c15bd3c28b904a28d3a41a0284a5736c1f807d1b7fd10cf8e3
- .../gold_finish_20261015/NY3/prep/rc.mol  sha256 11060cbba1f27c339034dc01e0a0cc66f8f677d5206f9b29dd5ee1bc15c6d090

④ 期望行为：xyz→mol 转换应能把可感知的键表（以及可判定的形式电荷）写入 MOL，或明确提供「保留键表 / 形式电荷」的输出通道，使经过刚性几何编辑的结构仍可交付带键的 MOL。

## P5 conformer_search 的 distance_filters 对单原子 Na⁺ 片段存在未文档化下界

① 调用
conformer_search(smiles="[Na+:7].[O-:1][H:6].[CH3:2][O:3][CH:4]=[O:5]", charge=0, multiplicity=1, distance_filters=[{"atoms":[1,2],"min_ang":2.15,"max_ang":2.35}], output_dir=".../gold_finish_20261015/NY3/prep/build/cs_probe_A", random_seed=42)

② 观察
is_success=false；message="Invalid ring_order/distance_filters: incompatible guided bounds when adding atom pair 1-2 (explicit) after []; no search was run. Resolved atoms (1-based): 1=Na, 2=O, 3=H, 4=C, 5=O, 6=C, 7=O, 8=H, 9=H, 10=H, 11=H"
对照（同一会话、仅改窗口）：distance_filters=[{"atoms":[1,2],"min_ang":2.4,"max_ang":2.9}] → 校验通过并实际执行搜索，返回 "No guided assembly candidate qualified; closest attempted geometry: .../prep/build/cs_probe_A/closest_attempt.xyz"。

③ 输入与证据文件：输入为 SMILES 字符串（无输入文件）；对照运行的产物 .../gold_finish_20261015/NY3/prep/build/cs_probe_A/closest_attempt.xyz

④ 期望行为：文档应写明反应中心距离窗口的接受区间 / 拒绝条件（或对所有原子对统一适用同一规则），使 Na–O 2.1–2.4 Å 这类化学合理窗口能否使用在调用前即可判定。

## 附：本清单涉及的工具面问题与 NY3 之外的关联
- PREP 道主线交付（结构与身份证据）：.../gold_finish_20261015/NY3/prep/PREP.md（sha256 c9f0f844714cfd45fe22febc46839968ccbf1a265f13e7f4c697e1979a8be0f8）；上述 5 条的规避路径已在该文件 §4.4 / §5 写明。
- 本清单不含修复建议与推测；如需新增 case，请给出新的工具调用与逐字返回，由本道只读复核后追加。

---

## 本道独立复核（small_mol/prep，只读）
复核时间：2026-10-15 18:00–18:20（北京时间，本机时区）。方式：只读文件/日志文本 + sha256sum/grep/python 读取，未改任何被复核对象；未提交任何 QM 作业。
1) P4 产物事实：读取 /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NY3/prep/rc.mol（sha256 11060cbba1f27c339034dc01e0a0cc66f8f677d5206f9b29dd5ee1bc15c6d090）→ V2000 计数行逐字为 " 11  0  0  0  0  0  0  0  0  0999 V2000"（bond 数 = 0），全文无 "M  CHG" 行。
2) F③(a) 的 guided MOL 事实：读取 /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NY3/prep/build/g_RC_w283/guided_assembly/assembly/complex_candidate_000.mol（sha256 05528d3d133333772faebf6a15b41a0e84c00cc20ad6b4af9b53348ee908003c）→ 8 条键行 + "M  CHG  2   1   1   2  -1"；几何 Na-O1 2.02 / Na-O5 2.31 / O1...C4 2.98（与 prep/rc.xyz 同源）。
3) F③(b) 下标一致性：guided MOL 与 prep/rc.xyz 的原子序同为 1 Na | 2 O1 | 3 H6 | 4 C2 | 5 O3 | 6 C4 | 7 O5 | 8,9,10 H(C2) | 11 H(C4)（依据本目录 prep/PREP.md §3.1 原子表 + 两文件文本核对），故重原子下标 = [1,2,4,5,6,7]，与 F③(b) 的 reactant 列表逐位一致。
4) F④ 核对：读取 /home/ly/Cloudra-mechanism-agent/ts/ts_0002/jobs/declaration_0001/candidate_opt/seed-opt.log（908808 B, mtime 18:09）→ grep 末行 "Normal termination of Gaussian 16 at Thu Oct 15 18:09:12 2026."；末次 "SCF Done:  E(RB3LYP) =  -466.986564979     A.U. after    7 cycles"；log 内 "Charge =  0 Multiplicity = 1"。数值与 F④ 引用逐位一致。

### P4 → F① 的 sha 级证据（只读）
读取对象（ts_0001 = 孤儿 run，issue #180；本道未对 ts/ 做任何写入）：/home/ly/Cloudra-mechanism-agent/ts/ts_0001/build/atom_tables/reactant_1_6593cc9061fc.json
实测字段：role=reactant；source_kind=file；index_base=1；atom_count=11；**components=11**；graph_error=""（空）；mol_path=/home/ly/Cloudra-mechanism-agent/ts/ts_0001/build/input_0001/reactant/seed.mol，**mol_sha256=11060cbba1f27c339034dc01e0a0cc66f8f677d5206f9b29dd5ee1bc15c6d090**（= prep/rc.mol：V2000 bond 数 0、无 M CHG）；xyz_path=/home/ly/Cloudra-mechanism-agent/ts/ts_0001/build/input_0001/reactant/seed.xyz，**xyz_sha256=c2e0db4302f9f3c15bd3c28b904a28d3a41a0284a5736c1f807d1b7fd10cf8e3**（= prep/rc.xyz）。
因果链（sha 级直证）：无键表的 MOL ⇒ 11 个原子被读成 11 个组分 ⇒ F① 的 identity mismatch 报文。

### F③(a) 正名（MOL 选择）与交叉印证（只读）
- 必须使用 guided 候选：/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NY3/prep/build/g_RC_w283/guided_assembly/assembly/complex_candidate_000.mol（sha256 **05528d3d133333772faebf6a15b41a0e84c00cc20ad6b4af9b53348ee908003c**；8 键 + "M  CHG  2   1   1   2  -1"；与 prep/rc.xyz 同源）。
- /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NY3/prep/build/art_RC_src/assembly/complex_candidate_000.mol（sha256 e1bdcd77c93316bec365bfac74a84bea226d0cf8d2d660fb8e204246fe14457a）是 **P1 的 plain builder 候选**（O1...C4 ≈ 3.50，与 rc.xyz 非同源），**不可**作为 F③(a) 的 MOL 证据。
- 交叉印证（读取 /home/ly/Cloudra-mechanism-agent/ts/ts_0002/build/atom_tables/ 下记录，ts_0002 = 有效 run）：reactant_1_d50031f061a9.json 与 reactant_1_4a3d52f8e1c7.json 均记录 mol_sha256=**05528d3d133333772faebf6a15b41a0e84c00cc20ad6b4af9b53348ee908003c**、components=3（前者 xyz_sha256=c2e0db43…即 prep/rc.xyz）；product_1_66fe1db6b159.json 记录 mol_sha256=**c4165dfc33a88e26990c32b4c3911259ffc1b092b67aeeb1d595bea33feea184**（= prep/i1.mol，builder 原生）、xyz_sha256=d1b3b5a35548d4c1dd9c02de631ee84894ac2628b884046c28d6d7080354cea3（= prep/i1.xyz）、components=2 → ts_0002 确实改用 guided MOL 与 builder 原生 MOL，组分计数随之变为 3 / 2。

### 复核边界
本小节内容全部来自上列真实文件与日志的只读读取（sha256sum / grep / 直接读取文本 / python json 读取）；未对 ts/ 目录写入、未改任何其它文件、未提交 QM 作业。本文件在此复核小节之后冻结，如需更正请按「同一轮更正」流程提出。

---

## P6 reaction_mapping 的自动映射在「两个同类 O 位置互换」的步上给出化学上不同的候选，且 mapping_status=unique（未标 ambiguous）（逐字照录，来源：包 Coordinator as_7479852819ea48c0 实测）
① 调用
reaction_mapping(reactant_smiles="[Na+].CO[C@H]([O-])O", product_smiles="[Na+].C[O-].C(=O)O", reactant_path=".../gold_finish_20261015/NY3/prep/i1.mol", product_path=".../gold_finish_20261015/NY3/prep/build/art_I2_src/assembly/complex_candidate_000.mol", reactant_binding={"indices":[1,2,3,4,6,5]}, product_binding={"indices":[1,2,3,7,8,9]}, reactant_charge=0, product_charge=0, reactant_multiplicity=1, product_multiplicity=1)
② 观察（逐字）
mapping_status="unique"；reactant_identity="match"、product_identity="match"；binding_diagnostics=["reactant: Explicit heavy-atom binding accepted against the concrete graph.", "product: Explicit heavy-atom binding accepted against the concrete graph.", "Full-atom mapping bound to the concrete structure order."]
formed_bonds=[[2,5]]；broken_bonds=[[2,3],[4,5]]；order_changes=[{"atoms":[3,4],"reactant_order":1,"product_order":2}]；watch_pairs=[[2,3],[2,6],[4,6]]；atom_map=[1,2,6,7,8,9,4,3,5,10,11]；heavy_atom_map=[1,2,5,4,3,6]
③ 输入与证据文件
- .../gold_finish_20261015/NY3/prep/i1.mol（builder 原生 MOL，含 bond block + M CHG）
- .../gold_finish_20261015/NY3/prep/build/art_I2_src/assembly/complex_candidate_000.mol（builder 原生 MOL，含 bond block + M CHG）
④ 期望行为
本步的化学键变化是「C4–O3 断 + C4=O5 键级 1→2」（甲氧基脱离，O3/O5 各自对应自身）：人工正确 atom_map = [1,2,3,7,8,9,4,6,5,10,11]（product 3 甲氧基 O3 → reactant 3 酯 O3；product 8 羰基 O5 → reactant 6 烷氧 O5）。工具返回的 atom_map=[1,2,6,7,8,9,4,3,5,10,11] 把 product 3→reactant 6、product 8→reactant 3（O3/O5 互换），等价于「甲基迁移」读法；它在两端 binding 都显式且身份 match 的情况下仍标 unique，会让下游把它当成唯一对应。期望：与声明的键变化一致，或至少标 ambiguous 并列出化学上不等价的候选。
⑤ 处置（本包做法）：E2 的 ts_prepare 声明里**显式**给出 atom_map 与 reaction_center=[[4,3],[4,6]]（绑定后完整坐标 1-based），不用自动映射。

### 本道复核附注（small_mol/prep，只读；时间 2026-10-15 18:2x）
- 独立复跑：以 P6① 的完全相同参数重跑 reaction_mapping（输入同上两文件，绝对路径 /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NY3/prep/...），返回与 P6② 逐字一致：mapping_status=unique；reactant_identity=match；product_identity=match；binding_diagnostics 三条同文；formed_bonds=[[2,5]]；broken_bonds=[[2,3],[4,5]]；order_changes=[{"atoms":[3,4],"reactant_order":1,"product_order":2}]；watch_pairs=[[2,3],[2,6],[4,6]]；atom_map=[1,2,6,7,8,9,4,3,5,10,11]；heavy_atom_map=[1,2,5,4,3,6]。另有 binding_status=complete、binding_source=concrete（P6② 未列，属同一返回）。
- 字段名提醒：同一次返回含三个相近字段，引用时必须写清字段名——watch_pairs=[[2,3],[2,6],[4,6]]、concrete_watch_pairs=[[2,3],[2,6],[4,6]]、graph_watch_pairs=[[2,3],[2,5],[4,5]]（后者与此前两者不同）。
- 索引解读（依据本目录 prep/PREP.md §3.2 与 §3.3 的原子表）：i1.mol 文件序 3=O3（酯 O）、6=O5（烷氧 O⁻）；I2 builder MOL 文件序 3=O3（甲醇盐 O⁻）、8=O5（甲酰 C=O）。工具 atom_map 把 product-3→reactant-6、product-8→reactant-3，即 O3/O5 互换，正是 P6④ 所述的「甲基迁移」读法，与声明的 break [4,3] 不一致。
- 复核边界：本次只读（工具调用 + 文件/日志文本读取），未对 ts/ 目录写入、未改其它文件、未提交 QM 作业。



（以下 F 节由包 Coordinator as_7479852819ea48c0 实测提供；本道只落盘与复核，未改写其内容。）

## F 附带案例：ts_prepare build 阶段 input_identity_unconfirmed 的复现与修复（NY3_E1）
① 现象（run ts_0001，build 阶段 blocked）逐字：failure_class=input_identity_unconfirmed；message="reactant: The concrete structure's molecular graph or stereochemistry differs from the declared SMILES. Declared identity: COC=O.[Na+].[OH-]; concrete identity: C.C.O.O.O.[HH].[HH].[HH].[HH].[HH].[NaH]. Changing binding indices cannot repair this identity mismatch."
② 根因：conformers.reactant 的 mol_path 用了 format_converter 由 xyz 生成的 rc.mol（无 bond block、无 M CHG，即 P4）→ 含 Na+ 复合物的图无法建立，11 个原子被判成 11 个组分。
③ 修复三要点：(a) mol_path 换成 builder 原生 MOL（.../prep/build/g_RC_w283/guided_assembly/assembly/complex_candidate_000.mol，8 键 + "M  CHG  2   1   1   2  -1"）；(b) 显式 heavy_atom_binding（按声明 SMILES 的重原子顺序列文件内 1-based 下标，reactant=[1,2,4,5,6,7]）；(c) product_smiles 必须带 concrete 种子真实存在的立体标注（RDKit 由 i1 的 3D 判为 CO[C@H]([O-])O，注册表该位无标注；不补则同一句 mismatch 复现）。
④ 成功判据：重建 run ts_0002 build 通过，structures.components=3，随后自动提交 candidate_opt（job 919，18:07 建、18:09 Normal termination，seed-opt.log E=-466.986564979 Eh）。
⑤ 另一处口径坑（非工具缺陷，但易错）：ts_prepare 的 reaction_center 用「绑定后完整坐标的 1-based 下标（含显式 H）」，不是注册表 map 号；reaction_mapping 的自动映射在对 I1→I2 这种「两个同类 O 位置互换」的步会给出化学上等价的另一候选（把甲氧基脱离读成甲基迁移），用它给的 formed/broken 前必须人工核对。

