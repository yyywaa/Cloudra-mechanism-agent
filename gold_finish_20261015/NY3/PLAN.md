# NY3 包 · 计划与进度（Na⁺ 中性模型整图重算）

包 Coordinator：as_bf15af420101498f ｜ 主题：gold-finish-20261015 ｜ 工作根：/home/ly/Cloudra-mechanism-agent
依据：gold_finish_20261015/BRIEF.md、gold_compute/supplement_20261002/HANDOFF_UNFINISHED_20261004.md §3「NY3 三条边」、
gold_compute/agent_hint_dead_ends_2026-09-26.md（NY3 行）、gold_compute/library_audit_20261002/open_edges.csv。

## 1 题源与待办边
- registry（唯一属主）：cloudra/benchmark/normal_registry/yo.py 的 "Y3"（sha256 dc58b4f5a01738c96001c32fcf913899d79cd00098e30909cfc83716ad0aefc8）。
- 题面：ideapool/tasks/normal/NY3.json（sha256 6f1db98ad8c9ae312477d4f1ec36ddae6d29e398e3aed874cabf5d35e06d348f）；md：ideapool/reaction_candidates/normal.md 第 65 行（Y3 行）。
- 三条边（gold.mechanism_graph 现有定义，barrier_kcal_mol 均为 null）：
  - NY3_E1 R → I1：OH⁻ 加成到羰基碳；bond_changes break [4,5]，form [1,4]。
  - NY3_E2 I1 → I2：甲氧基消除、C=O π 复原；break [3,4]，form [4,5]。
  - NY3_E3 I2 → P：质子转移 H6 O1→O3；break [1,6]，form [3,6]。
- 用户裁决（2026-09-25，yo.py 注释）：裸 OH⁻ 无对离子 → CPCM 下加成无垒（模型失真），改为 **Na⁺ 制衡的中性模型**（总电荷 0、CPCM(Water)、单重态）重算全图；Na⁺ 作游离组分 map 7、不参与键变化，真实配位位置由计算自决。
- 旧值全部作废：15.5（文献 ΔG，Pliego & Riveros 2002）、12.5（裸离子自算 E2）、0.0（裸离子 E3）。

## 2 口径（本机现实）
- 本机无 ORCA。统一 **Gaussian 16（/home/ly/g16/g16）**：B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight + SCRF=(CPCM,Solvent=Water)。
- 能量 = 纯电子能差（无 ZPE/热校正），相对该步自身起点极小值；同一条边的 TS/端点/起点必须同一程序同一批作业。
- TS/IRC 只能走 ts_prepare / ts_resume（手工 TS/IRC 提交被禁用；ts_guess 只用于探索）。
- 资源：同一时刻 1 个 QM 作业、单作业 ≤6 cpus / ≤10000 MB；提交前查队列。

## 3 模型定义（待 prep 落地，写成图前的准备证据）
原子映射（1-based，来自 yo.py mapped_reactants [Na+:7].[O-:1][H:6].[CH3:2][O:3][CH:4]=[O:5]）：
Na=7；O1（氢氧根 O）、H6（氢氧根 H）、C2（甲氧基甲基 C）、O3（酯 O）、C4（羰基 C）、O5（羰基 O）；C2 上 3 个 H，C4 上 1 个 H。**总原子数 11 = NaC2H5O3**（Na + OH + 甲酸甲酯 C2H4O2），重原子 6，与 NY3.json max_heavy_atoms=6 一致。（勘误：本文件初稿误写 12 / C3H4O2，由 explorer 只读复核 evt_85b4f68394a3421c 指出，2026-10-15 更正。）
四个节点的化学身份：
- RC  ：[Na+].[OH-].COC=O  —— Na⁺ 桥联氢氧根 O1 与羰基 O5 的离子-偶极复合物（Na–O1、Na–O5 均配位），O1 对准 C4。
- I1  ：[Na+].COC([O-])O  —— 四面体烷氧盐；Na⁺ 配位烷氧 O5（及 O1 次配位）。
- I2  ：[Na+].C[O-].O=CO  —— 甲酸 + 甲醇盐离子对；Na⁺ 桥联甲酸 O1 与甲醇盐 O3。
- P   ：O=C[O-].[Na+].CO  —— 甲酸根 + 甲醇；Na⁺ 配位甲酸根 O1（及 O5）。
六元环假设（历史疑点，来自 9/26 复盘审计）：E2 与 E3 可能耦合为 **Na⁺ 桥联六元环 Na–O5–C4–O3···H6–O1**（甲氧基离去与 O1→O3 质子转移协同）。若计算证实耦合：只报证据 + 具体图裁决问题，**不合并边、不改图**（BRIEF §7）。

## 4 执行计划
1. prep：Na⁺ 配位/六元环模型的结构与身份证据（XYZ/MOL + 距离表 + RDKit/映射核验），落在本目录 prep/。
2. 逐边 ts_prepare → （必要时 ts_resume 修订 guess/端点）→ ts_inspect 读权威状态。
3. 每边验收：TS 恰 1 虚频且模以声明 watch pair 为主；IRC 双向到达声明两端；两端 Opt/Freq 零虚频；纯电子能差相对本步起点。
4. 回填 yo.py（steps[].barrier）+ ideapool/tasks/normal/NY3.json（edge barrier_kcal_mol）+ normal.md Y3 行；跑 gen_normal_tasks.py 生成与 tests/test_benchmark.py -k regenerate_identically 守卫。
5. 交付：本目录 STATUS.md（逐边一行 + 日志绝对路径 + sha256 + 方法一句）、证据清单、agent_hub 开工帖与逐边终态帖。
6. 缺测就写「缺什么 + 已证伪什么 + 待裁决问题」，不填 0、不改图。

## 5 上轮遗留核对（本轮开始时）
- gold_finish_20261015/ 在本轮开工前只有 BRIEF.md，**没有 NY3/ 目录**；本机全盘 find 无 NY3 命名的运行目录 → 上轮「一次准备写入因工具异常失败」的产物在本地不存在。仍需在 prep 记录中给出核验命令与结论（文件不存在/不完整）。

## 5b 口径核定（explorer 只读复核 evt_85b4f68394a3421c，2026-10-15）
- ts_prepare 的 QmCalculation（本包自读契约核实）：engine=gaussian、method=b3lyp、basis_set=def2svp、keywords="empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=water)"、end_setting=""。Gaussian 无"尾部方法设置"，任务记号不在 QmCalculation 里（explorer §2 提到的 task_type 属 qm_input_writer 口径，ts_prepare 契约中无此键，不采用）。
- 流程：先发一次声明 → ts_inspect(run_id).structures 拿权威 1-based 完整坐标表（含显式 H）→ 用它换算 reaction_center / guidance.ring_order / distance_filters / guess.scans 的原子下标 → ts_resume 修订。**map 号 ≠ 结构下标**；yo.py/NY3.json 的 bond_changes 用 map 号，ts_prepare 结构引用用完整坐标 1-based。
- 六元环适用的边：E2（起点 I1 里 C4–O3 仍成键，环 Na–O5–C4–O3···H6–O1 成立）；E3 起点 I2 里 C4–O3 已断，应改用环 O1–C4–O5–Na–O3···H6。

## 6 进度日志
- 2026-10-15：开工，读完 BRIEF/交接/复盘/题源，队列空（0 running/0 queued），确认上轮准备产物不存在。
