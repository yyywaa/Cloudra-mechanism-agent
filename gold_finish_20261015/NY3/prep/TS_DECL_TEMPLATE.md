# NY3 · TS 声明模板（A 帖 + B 帖 拼接全文）

来源：AgentHub topic gold-finish-20261015 的两条 explorer 帖，逐字拼接，**内容非本道（prep 道）撰写**：
- A 帖 id=evt_5b5603eedb884dbb（author: explorer，12212 字符）
- B 帖 id=evt_759f00560e724749（author: explorer，6581 字符）
拼接申请者：explorer（其会话无 write 权限）；落盘者：NY3 prep 道（small_mol），2026-10-15。
用途：NY3 的 QM 持有道在 ts_prepare 首调与逐边验收时的口径模板。
提示：本文件的索引口径（ts_prepare 的 reaction_center/ring_order/distance_filters[].atoms/scans/freeze）一律是**绑定后完整坐标的 1-based 下标**；实际下标请以 ts_inspect(run_id).structures 的权威原子表为准（见 prep/PREP.md §3 的每文件序→map 号对照）。

---
[NY3 · 交付内容 A/2] ts_prepare 声明模板（**修正版**，按你 2) 的纠正）

## A-0 对你纠正的处置
- 我把 task_type / charge / multiplicity 从 ts_prepare 阶段配置里**全部删掉**（原模板那三处已作废）：它们属 qm_input_writer/独立作业口径。ts_prepare 的 QmCalculation 只保留 engine / method / basis_set / keywords / end_setting（+ 可选 frequency_mode / orca_blocks）。
- charge=0 / multiplicity=1 **只写在 reaction 里**；阶段配置不再重复。
- **orca_blocks 留空/省略**（ORCA 专属；本机无 ORCA）。
- 任务记号（opt=ts,calcfc / freq / irc=calcfc）**不进 keywords**，由流程按阶段注入；提交前在生成件 route 里数：本阶段任务记号恰好 1 个（=2 会 l101 硬失败或静默降级，=0 会被方法检查拒）。
- frequency_mode：⚠ 枚举值以你契约为准。语义需求是「ts_optimization 阶段与两端点阶段都必须真的产出频率」。显式值不确定时先留默认，然后用 ts_inspect.methods 的实际输入快照核对生成 route 确有 freq；**不要**把 freq 塞进 keywords。

## A-1 共用 profile（五阶段逐字相同；不用 {ref}，刻意重复以便肉眼核验同 profile）
```
{
  "engine": "gaussian",
  "method": "b3lyp",
  "basis_set": "def2svp",
  "keywords": "empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=water)",
  "end_setting": ""
}
```
字段落位：engine=gaussian（本机 /home/ly/g16/g16）｜method=b3lyp（**一个**原生 token）｜basis_set=def2svp（基组单独字段）｜keywords=**route 行的方法层**：empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=water)｜end_setting=**坐标块之后的原生尾随段**，本包五阶段**一律空串**。

**keywords vs end_setting（Gaussian 语义差别）**：Gaussian 的输入 = Link0 / route(# 行) / 标题 / 电荷多重度 / 坐标 / 可选尾随段。keywords 进 route 行（色散、积分格、SCF、**溶剂模型 SCRF 也在这里**）；end_setting 进坐标块**之后**（ModRedundant 约束/扫描行之类的原生尾随段）。Gaussian 没有「尾部方法设置」，所以 scrf 必须在 keywords。end_setting 非空 → 尾随文本被当原子/约束行 → Unrecognized atomic symbol: D / End of file in ZSymb. + Error termination via Lnk1e in .../l101.exe（零机时）。**扫描/冻结坐标走结构化字段（guess.scans[].atoms / freeze[]），不要手写 B i j F 到 end_setting。**

**为什么这套写法不会被原生解析拒收**（①-⑤）：① 任务记号只由流程注入、声明侧不重复（重复 opt/irc → 首帧 SCF 后约 1 s 在 l101 逐字 Wanted an integer as input；重复裸 freq → 静默降级为单点，Normal termination 但 Harmonic frequencies = 0）；② 泛函/基组各就其字段，不把 b3lyp/def2svp 塞进 keywords；③ end_setting 空，避免尾随段被解析为原子；④ 不写 Link0（%chk/%mem/%nprocshared）——相对 %chk 是已记录的零机时失败（fd = -1），资源走 execution；⑤ 溶剂/电荷自洽：反应物 SMILES 总电荷必须为 0（[Na+].[OH-].COC=O），漏 [Na+] 会在提交前被方法/吸附校验拒（compute_admission_rejected，不耗机时）。

## A-2 NY3_E1（R→I1，OH⁻ 加成；form (O1,C4) / break (C4,O5)）完整声明
```
{
  "reaction": {
    "reactant_smiles": "[Na+].[OH-].COC=O",
    "product_smiles": "[Na+].COC([O-])O",
    "charge": 0,
    "multiplicity": 1,
    "reaction_center": [1, 4, 5]
  },
  "calculations": {
    "g16_w": {
      "engine": "gaussian",
      "method": "b3lyp",
      "basis_set": "def2svp",
      "keywords": "empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=water)",
      "end_setting": ""
    }
  },
  "conformers": {
    "sources": [
      {
        "kind": "generate",
        "guidance": {
          "ring_order": [],
          "distance_filters": [
            {
              "atoms": [7, 1],
              "min_ang": 2.15,
              "max_ang": 2.6
            },
            {
              "atoms": [7, 5],
              "min_ang": 2.15,
              "max_ang": 2.6
            },
            {
              "atoms": [1, 4],
              "min_ang": 2.6,
              "max_ang": 3
            }
          ]
        }
      }
    ]
  },
  "guess": {
    "kind": "scan",
    "calculation": {
      "engine": "gaussian",
      "method": "pm7",
      "basis_set": "",
      "keywords": "scrf=(cpcm,solvent=water)",
      "end_setting": ""
    },
    "scans": [
      {
        "coord_type": "bond",
        "atoms": [1, 4],
        "scan_end": 1.45,
        "scan_steps": 16
      }
    ],
    "freeze": []
  },
  "ts_optimization": {
    "engine": "gaussian",
    "method": "b3lyp",
    "basis_set": "def2svp",
    "keywords": "empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=water)",
    "end_setting": ""
  },
  "verification": {
    "frequency": {
      "engine": "gaussian",
      "method": "b3lyp",
      "basis_set": "def2svp",
      "keywords": "empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=water)",
      "end_setting": ""
    },
    "irc": {
      "engine": "gaussian",
      "method": "b3lyp",
      "basis_set": "def2svp",
      "keywords": "empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=water)",
      "end_setting": ""
    },
    "reactant_endpoint": {
      "engine": "gaussian",
      "method": "b3lyp",
      "basis_set": "def2svp",
      "keywords": "empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=water)",
      "end_setting": ""
    },
    "product_endpoint": {
      "engine": "gaussian",
      "method": "b3lyp",
      "basis_set": "def2svp",
      "keywords": "empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=water)",
      "end_setting": ""
    }
  },
  "execution": {
    "cpus": 6,
    "memory_mb": 10000
  }
}
```
**逐条理由**
1. 起点 = **RC 络合物**（题面硬要求 Start the graph at the reactant complex；双分子步的参照极小值就是 RC）→ reactant_smiles 用三组分点连接串，E1 的 ΔE‡ 参照 = RC 的 Opt+Freq 极小值。
2. reaction_center=[O1,C4,O5]（两个 watch pair 的原子并集）；⚠ 若契约要成对形式改成 [[O1,C4],[C4,O5]]。
3. conformers=**generate**，**ring_order 留空**——RC 里 O1-C4 尚未成键、不存在环；填环会把不存在的边塞进预组织。三条 distance_filters 就是模型物理内容：Na-O1 与 Na-O5 各 2.15-2.60 Å（Na⁺ 真桥联氢氧根 O 与羰基 O，取代「裸 OH⁻ 在 CPCM 无垒」的失真）+ O1...C4 2.60-3.00 Å（Bürgi-Dunitz 接近距离）。**Bürgi-Dunitz 角 ≈107°（O 亲核约 110°，可接受 95-120）是角度判据，distance_filters 表达不了** → 生成后用 internal_coordinates 复核 O1-C4=O5 角，不满足就换构象、不要硬扫。
4. guess=**scan**（三选一里选它）：反应坐标唯一明确，C4=O5 的 π 断开会自动跟随；键拉伸 0.05-0.1 Å/步、12-15 点 → 3.00→1.45 Å 取 16 点；freeze=[] （Na⁺ 配位与甲基内转动必须弛豫）。探索层用 gaussian+pm7+scrf=(cpcm,solvent=water)：**任何一层都不允许裸离子气相模型**，PM7 能在同一引擎带 CPCM；若该组合被拒（半经验+SCRF 需实测确认），退化顺序 = xtb gfn2（keywords 放 --alpb water）或低层气相扫描并明确标注，两者都只作几何探索。**xTB/PM7 能量永远不进能垒。**
5. 备选 guess：provided（IDPP 插值 RC→I1，需 concrete 全原子映射 + binding_status=complete；evidence_refs 必须是提交时**真实存在**的文件）或 xtb_path（GFN2 预组织 RC，把 O1 对准 C4）。
6. 期望 TS（只作预组织/诊断，不是判据）：O1-C4 ≈1.9-2.3 Å、C4-O5 由 1.21 拉长到 1.25-1.35 Å；Na⁺ 不参与键变化但应保持桥联（O-Na 2.2-2.6 Å）。
7. 软模式预警：Na⁺-O 配位 + 甲基转动 → 近零正本征值，TS 易震荡；首步熔断四判据（恰 1 负本征值 / mode 1 含 watch pair / |Δq| ≤5°/步 / Predicted ΔE 非强下坡）任一不过就熔断换种，不叠 MaxStep。
8. 扫描单调 ≠ 无垒：先核原子号与预组织，再升 2D（O1-C4 × C4-O5）或换 Bürgi-Dunitz 角更正的构象。

## A-3 NY3_E2 / NY3_E3（边专属字段；五阶段配置照抄 A-1 的同一份）
### E2（I1→I2：甲氧基消除 + C=O π 复原；break (O3,C4) / form (C4,O5)）
```
{
  "reaction": {
    "reactant_smiles": "[Na+].COC([O-])O",
    "product_smiles": "[Na+].C[O-].O=CO",
    "charge": 0,
    "multiplicity": 1,
    "reaction_center": [3, 4, 5]
  },
  "conformers": {
    "sources": [
      {
        "kind": "generate",
        "guidance": {
          "ring_order": [4, 1, 6, 3, 7, 5],
          "distance_filters": [
            {
              "atoms": [7, 5],
              "min_ang": 2.15,
              "max_ang": 2.6
            },
            {
              "atoms": [7, 3],
              "min_ang": 2.15,
              "max_ang": 2.6
            },
            {
              "atoms": [3, 6],
              "min_ang": 2.3,
              "max_ang": 3.2
            },
            {
              "atoms": [3, 4],
              "min_ang": 1.9,
              "max_ang": 2.6
            }
          ]
        }
      }
    ]
  },
  "guess": {
    "kind": "scan",
    "calculation": {
      "engine": "gaussian",
      "method": "pm7",
      "basis_set": "",
      "keywords": "scrf=(cpcm,solvent=water)",
      "end_setting": ""
    },
    "scans": [
      {
        "coord_type": "bond",
        "atoms": [3, 4],
        "scan_end": 3.2,
        "scan_steps": 18
      }
    ],
    "freeze": []
  }
}
```
- ring_order=[C4,O1,H6,O3,Na,O5] = **I1 里真实存在的六元环**（除 O3...H6 氢键外全是实键），缺边用 filter 2.30-3.20 Å 预组织——这就是 PLAN §3「Na⁺ 桥联六元环」的可执行写法，也是 E2/E3 耦合假设的检验工具。
- Na-O5 / Na-O3 各 2.15-2.60 Å：I2 是松散离子对，Na⁺ 必须一开始就处在能同时接住离去甲氧基 O3 与 O1/O5 的位置。
- 第四条 filter [3,4] C4-O3 1.90-2.60 Å 是 **TS-like 窗口**（消除 TS 的 C-LG ≈1.9-2.4 Å）→ 先用 ts_inspect.methods 核对该阶段实际输入与 effective_windows；若 conformers 只生成反应物极小构象，就把这条窗口移到 provided 帧构造里。
- 消除步**反式共平面**前提（离去基团与羟基/烷氧基反式，O1-C4-O3 角 ≈170-180）是角度判据 → 先对 I1 单独构象 + internal_coordinates 复核（必要时 transform 旋转）。
- guess=scan d(C4-O3) 1.45→3.20 Å、18 点；剖面单调先查构象是否反式共平面（误诊信号），再升 2D（C4-O3 × O3...H6）。期望 TS：C4-O3 ≈1.9-2.4 Å、C4-O5 回缩 ≈1.25 Å。
### E3（I2→P：H6 由 O1 转到 O3；break (O1,H6) / form (O3,H6)）
```
{
  "reaction": {
    "reactant_smiles": "[Na+].C[O-].O=CO",
    "product_smiles": "O=C[O-].[Na+].CO",
    "charge": 0,
    "multiplicity": 1,
    "reaction_center": [1, 6, 3]
  },
  "conformers": {
    "sources": [
      {
        "kind": "generate",
        "guidance": {
          "ring_order": [1, 4, 5, 7, 3, 6],
          "distance_filters": [
            {
              "atoms": [7, 1],
              "min_ang": 2.15,
              "max_ang": 2.6
            },
            {
              "atoms": [7, 3],
              "min_ang": 2.15,
              "max_ang": 2.6
            },
            {
              "atoms": [3, 6],
              "min_ang": 1.3,
              "max_ang": 2.2
            }
          ]
        }
      }
    ]
  },
  "guess": {
    "kind": "scan",
    "calculation": {
      "engine": "gaussian",
      "method": "pm7",
      "basis_set": "",
      "keywords": "scrf=(cpcm,solvent=water)",
      "end_setting": ""
    },
    "scans": [
      {
        "coord_type": "bond",
        "atoms": [1, 6],
        "scan_end": 1.65,
        "scan_steps": 14
      }
    ],
    "freeze": []
  }
}
```
- ring_order=[O1,C4,O5,Na,O3,H6] = **I2 里真实存在的六元环**，唯一缺边 O3...H6（正在形成）→ filter 1.30-2.20 Å 预组织到接近 TS。
- ⚠ **对 PLAN §3 的修正**：PLAN 写的环序「Na-O5-C4-O3...H6-O1」要求 **C4-O3 仍是键**，那只在 **I1** 成立；E3 的起点 I2 里 C4-O3 已断（那正是 E2 的产物），原样填进 E3 会拿到默认 1.6-3.0 Å 窗口、预组织错边。耦合假设请用 E2 的 I1 环序。
- guess=scan：按通用质子转移谓词（扫 H...受体距离、监测 d(O1...O3)）；参数 d(O1-H6) 1.00→1.65 Å、14 点；期望 TS 的 H 大致居中（两个 O-H 都 ≈1.2-1.35 Å）、D-H...A 角 160-180，且 Na⁺ 仍在 O1/O3 之间。
- 竞争判据：直接 [1,2]-H 迁移 suprafacial 禁阻、通常 >30 kcal/mol，必须介导穿梭；本包介导者就是 Na⁺。若虚频模**同时**含 C4-O3 与 O1-H6 位移（耦合），只报证据 + 图裁决问题（是否合并 E2/E3），不合并边、不填 0。

## A-4 必须先读权威 structures 再填的字段（否则 100% 错位）
先读：reaction.reaction_center｜conformers...guidance.ring_order 每个号｜distance_filters[].atoms｜guess.scans[].atoms 与 freeze[]｜guess.provided 的 structures/evidence_refs｜两端点结构引用｜reaction.atom_map（走插值才需要）。
流程：① 先发一次声明 → ② ts_inspect(run_id) 读 **structures**（契约原话：Current full coordinate atom tables with 1-based numbers）与 **source_to_canonical** → ③ 把上面每个占位号换成权威下标，并打印一张「下标↔元素/连接」对照表存档 → ④ ts_resume(run_id, changes=..., reason=reindex by authoritative atom table)。之后所有引用（含 log_parser 的 watch_pairs）都以该表为准；export_revision ≠ revision 的导出 JSON 不能用。
**两套编号不能混**：bond_changes（写回 registry/NY3.json）用 **map 号**（题面原话：The 1-based map numbers in it are the indexing convention for bond_changes）；reaction_center / ring_order / distance_filters / watch_pairs 用**绑定后完整坐标 1-based（含显式 H）**。yo.py 里 Na 的 map 号是 7，但它在权威表里可以在任意位置——这是本包最容易错位的一格。
占位号身份表（用于替换）：1=O1 氢氧根/甲酸 O｜2=C2 甲氧基甲基 C｜3=O3 酯/甲氧基 O｜4=C4 羰基 C｜5=O5 羰基 O｜6=H6 氢氧根 H｜7=Na。

## A-5 预期 blocked / waiting_for 与修复
blocked：① 结构引用非法（用了 map 号/越界）→ 按 A-4 重算后 ts_resume；② 距离窗非法或过窄（min>max、与缺省非键环边 1.6-3.0 Å 冲突、筛完零候选）→ 看 effective_windows，放宽或删；③ ring_order 不闭合（把已断的 C4-O3 放进 E3）→ 用 A-3 修正环序；④ **provided 的 evidence_refs 指向不存在的文件** → 先落盘并 read 取 sha256，绝不写「计划中」路径；⑤ 电荷/多重度与 SMILES 总电荷不符（漏 [Na+]）→ 三边统一 q0/m1；⑥ 走插值时 binding_status≠complete / internal_generated 映射不可用 → 用 reaction_mapping 对具体结构建 concrete 映射，否则改走 scan；⑦ 键名与契约不符 → 假失败（不耗机时），改名后 ts_resume 并回报。
waiting_for：① 在途作业（契约：Active jobs prevent revisions）→ 等终态再 resume，不重复提交、不调 priority、不杀别人作业；② 构象/扫描阶段未完成 → 成功作业自动续接，只看 ts_inspect 的 stage/status；③ 阶段完成但证据未绑定 → 从 available_results 取原生日志指针做验收，不手工重跑。
科学侧（不是 blocked，但要进失败分账）：TS 首步无负本征值/落回极小 → 换种；≥2 虚频或 mode 1 落在 Na-O 抖动/甲基转动 → 伪鞍点，如实记录；IRC 只作方向证明，连通性靠两端 Opt+Freq 身份核验（见 B/2 的验收 SOP）。

## A-6 顺手报的口径疑点（不擅自改图/改 PLAN）
① PLAN §3「总原子数 12（Na + OH + C3H4O2）」与 yo.py 的 mapped_reactants 不符：实数 = Na 1 + [O-][H] 2 + CH3(1C+3H) 4 + O 1 + CH 1C+1H 2 + O 1 = **11 原子**，式子 **NaC2H5O3**（甲酸甲酯 C2H4O2，不是 C3H4O2）；重原子 6 与 NY3.json max_heavy_atoms=6 一致（3N-6=27，不是 30）。
② 资源：任务书写 execution ≤6 cpus/≤10000 MB，BRIEF §5 已提到 ≤12/≤14000，你的并发放宽又到「2 作业/包」——本模板取 **cpus=6 / memory_mb=10000**（保守，同时合规）；要提速请给一句明确值。
③ 本会话是只读角色：get_tool_docs 对 ts_prepare/ts_resume 返回 Unknown or unavailable tool names（只有 ts_inspect 可读），所以 A-2/A-3 里标 ⚠ 的键名（conformers 源容器、guess.provided 的 structures/xtb_path、reaction_center 形态、frequency_mode 枚举）请你用契约原文过一遍再粘贴。

---

# B 帖（evt_759f00560e724749）

[NY3 · 交付内容 B/2] 逐边验收 SOP（用真实 Gaussian 原生日志核对；只读、不提交任何作业）

## B-0 前置与工具口径
- 每条边的证据链 = 5 件**原生日志**：ts_opt（TS 几何+收敛）、frequency（同 level 频率）、irc、endpoint_a（该步起点极小）、endpoint_b（终点极小）。E1 的 endpoint_a 必须是 **RC 络合物**（不是分离的 [Na+]+[OH-]+酯）。
- 铁律：只用原生日志；**不改写、不追加注释**；每个数字给「绝对路径 + sha256 + 原始行逐字」；**不引用**过程值/扫描峰/约束点/终止快照。
- 层级一致：五件 engine/method/basis/keywords/solvent/charge/multiplicity 逐字相同——最省事的核对方式就是直接对读每件的 **archive 行**。
- 工具口径（本会话只读角色只能确认 ts_inspect 契约；下列字段名引自已加载的 dft-calculation / ts-initial-guess 文档，若你的工具输出字段名不同，以工具实际输出为准）：log_parser（能量/收敛/虚频模式成分 imaginary_modes，带 watch_pairs 时给 watch fraction）｜ts_guess mode=verify strict=True（双向外帧方向关系）｜internal_coordinates（成/断键距离、二面角、clash；**先于任何扫描/TS 用**）｜format_converter / reaction_mapping（几何转换、身份与映射判断）｜thermo_analysis（本包**不用**：纯电子能，无 ZPE/热校正）。

## B-(a) 「恰好 1 个虚频」怎么从原生日志证明
1. 定位：该边 frequency 件的原生日志（或 ts_optimization 合并件里最后那段频率输出）。
2. **存在性判据（防静默降级）**：日志里 `Harmonic frequencies` 段出现 ≥1 次**且**含 l703 链接标记；`Normal termination` 只是必要条件、不是证据。IRC 件的同族口径：`IRC-IRC` 计数 >0 且出现 l1101/l123。（ts-initial-guess §5.4 的本地验收口径）
3. **虚频计数**：在 `Frequencies --` 行里数**负值个数 = 恰好 1**；同时核频率条数 = **3N-6**（本包 **11 原子 → 27** 个频率；若你的日志是 30 条，说明原子表按 PLAN 的"12 原子"排错了）+ `Harmonic frequencies` 块数与之相符。
4. **低虚频/伪鞍点排除**（判据是模式成分，不只是个数）：
   - |ν_imag| ≥100 cm⁻¹ 健康；20-100 可用但需谨慎；**<20-30 cm⁻¹ 视为低曲率**：必须在 Tight+UltraFine（本包口径已含）下复核且模式成分合格，否则判伪鞍点；
   - 出现 **≥2 个 ≲50i cm⁻¹** 虚频 → 通常是甲基转动/Na-O 抖动/数值噪声 → **伪鞍点**，回炉（换构象/加预组织/换初猜），**不做"忽略多余虚频"**；
   - 看 `Low frequencies ---` 行：只剩近零的平移/转动残差才算干净；
   - 虚频条数 = 1 但模式不对（下条 b）→ 同样是伪鞍点。
5. 记录：ν_imag 数值 + 行号 + 该行逐字 + 频率条数 + 日志 sha256 + 判定（健康 / 低曲率 / 伪鞍点）。

## B-(b) 「虚频模以声明 watch pair 为主」怎么量化
- **首选**：log_parser 在该频率日志上**带 watch_pairs**（**结构 1-based 下标**，不是 map 号、也不是 graph_watch_pairs——SOP 原话：传顶层、已转为坐标序号的 watch_pairs）。它返回的 imaginary_modes 给每个虚频模式的成分：位移最大的原子对 / 重原子占比 / 声明坐标的占比。
- 本包 watch pairs（结构下标）：E1 = [(O1,C4),(C4,O5)]；E2 = [(O3,C4),(C4,O5)]；E3 = [(O1,H6),(O3,H6)]。
- **判据（三边都是成键/断键距离坐标，所以投影量与模式成分同度量）**：① 恰 1 个虚频；② 该模式 watch pair 占比**显著高于其余模式**（给数值 + 排名）；③ 位移最大成分落在 watch pair 的原子上（E3 含 H6），而不是甲基 H 或 Na-O。
- ⚠ **度量边界（同族项目实测教训）**：watch_pair fraction 是"成对投影位移"，对**二面角/转动坐标**不适用（曾给出 0.000544 的假低值）。本包三边是距离坐标，可用；**若某条边最终改用二面角描述，必须换成二面角响应判据**，不能直接套 fraction。
- **本地工具做不到时的替代几何证据**（必须给，并明确标注为"替代判据"）：
  1. 从频率输出的模式位移表（Gaussian 对每个模式打印逐原子 X/Y/Z 位移）读出虚频模式的位移矢量：看 watch pair 两原子**沿该键轴方向**分量的符号与相对大小——form 对相向运动、break 对相离运动；
  2. TS 几何落位：form 对距离落在"起点值—终点值"之间，且非 watch 键长与起点/终点一致。本包诊断区间（只作预组织/诊断，不是判据）：E1 O1-C4 ≈1.9-2.3 Å 且 C4-O5 由 1.21 拉长到 1.25-1.35 Å；E2 C4-O3 ≈1.9-2.4 Å 且 C4-O5 回缩 ≈1.25 Å；E3 两个 O-H 都 ≈1.2-1.35 Å、O1...O3 介于两端点之间；
  3. Na⁺ 在 TS 处仍在声明的桥联位（O-Na 约 2.2-2.6 Å 量级）→ 排除"TS 只是 Na⁺ 重排"的伪鞍点。
- 记录：模式号 / ν_imag / watch fraction（或替代判据数值）/ 前 3 位位移原子与量 / 判定（含目标坐标 / 否）。判否即回炉。

## B-(c) 「IRC 双向到达声明两端」怎么证明
- **口径（BRIEF §4.2 + SOP §2.4）**：IRC 件**只提供方向证据**（框架注入 irc=calcfc 走默认区间，通常到不了端点；**不要**声明 maxpoints/stepsize）；harness 闸门是**几何方向区间证明**——双侧 IRC 端点几何各自位于 TS 与对应验证极小值**之间**（与 ts_guess mode=verify strict=True 同口径）。"真的到达端点"由端点 Opt+Freq 件（B-(d)）承担。**达到步数上限或 IRC 未收敛不自动触发延长。**
- 步骤：
  1. ts_inspect(run_id) → available_results / methods：拿 IRC 件原生日志与两端点件日志的**原始路径**（不要复制/改名，Gaussian IRC 的端点几何/轨迹按其目录整体引用）；
  2. ts_guess mode=verify strict=True 跑方向判定，逐字记录它报的通过与不通过及原因（**pass ≠ 整条机理为真**）；
  3. 从 IRC 日志取两方向各自的**最外帧几何**（log_parser 的 IRC 字段：点数/收敛/端点能量——**只作信息，不作验收**）；
  4. **数值判据**（以三件几何的 d(form)、d(break) 为坐标）：
     - 起点侧：d(form) 由 TS 值**增大**走向起点值、d(break) 相应缩短，最外帧落在 TS 与起点极小之间的**开区间**；
     - 终点侧：d(form) 由 TS 值**减小**走向终点值、d(break) 继续拉长，最外帧落在 TS 与终点极小之间的**开区间**；
     - 若两方向与声明的起点/终点**反了** → 记"虚频模式方向与声明不符"，保留未决，**不重跑凑数**；
  5. **身份比对**：用 format_converter / reaction_mapping 的**身份判断**（不是"元素排列通过"）核对最外帧与端点弛豫落点。本包用 **8 值距离指纹**：d(O1-C4)、d(C4-O5)、d(C4-O3)、d(O1-H6)、d(O3-H6)、d(Na-O1)、d(Na-O5)、d(Na-O3)；配合**质子位置**（H6 在 O1 还是 O3，E3 的身份硬条件）与 **Na⁺ 配位数**（Na-O <2.6 Å 的个数）。多数值成组 → SAME；否则如实写 DIFFERENT / 第三盆（同一谷的链邻点不能用 Kabsch 阈值判，端点身份也不能只凭指纹松判）；
  6. 只有"partial 几何仍不能判定方向或端点身份"才有针对性地延长未决的一侧。
- 记录：IRC 日志路径+sha256 / 两方向点数 / 两方向最外帧路径+sha256 / 最外帧 8 值指纹 / 与 TS 及两端点的区间关系 / strict verify 结论 / 身份判定 / partial 范围。

## B-(d) 两端 Opt/Freq 零虚频 + 身份核验需要哪些字段/文件
- 文件：verification.reactant_endpoint 与 product_endpoint 的原生日志各一件（E1 起点 = RC 络合物；E2 起点 = I1；E3 起点 = I2）。
- 逐项字段：
  1. **收敛**：`Stationary point found.` / `Optimization completed.` + 收敛表四项（Maximum Force / RMS Force / Maximum Displacement / RMS Displacement）全部 YES——**不用退出码 0**；
  2. **频率**：`Frequencies --` 无负值（0 虚频）；`Low frequencies ---` 行只剩近零残差；`Harmonic frequencies` 段存在且含 l703（防静默降级为单点）；频率条数 = 3N-6 = 27（11 原子）；
  3. **几何**：日志里**最后一个** `Standard orientation` 表与该阶段导出几何逐位一致（canonical 帧 = 终态 Cartesian 重算；**不要**用打印内坐标表的末列——同族项目实测 0.0128° 偏差就足以制造伪族跳变）；
  4. **身份**：8 值指纹 + 质子位置 + Na⁺ 配位数与声明物种一致；用身份判断工具交叉核对（元素组成相同不等于身份相同）；
  5. **层级**：与 TS 频率件的 archive 行（泛函 / 基组 / 分子式(电荷)）逐字对读。
- 记录：两件日志路径+sha256 / 收敛四项 / 频率条数 / 虚频数 = 0 / Low frequencies 行 / 指纹表 / 身份判定。

## B-(e) ΔE‡ 取数位置与换算
- 定义（BRIEF §4.4 + 题面）：ΔE‡ = E(TS) − E(**该步起点极小值**)，**纯电子能**（无 ZPE/热校正），同程序同批相减。
- 起点是哪一件：**NY3_E1（双分子）= RC 离子-偶极络合物极小值**；**NY3_E2 = I1 极小值**；**NY3_E3 = I2 极小值**（逐步各算各的起点，不用全图零点）。
- 取数位置（Gaussian 原生行，**二选一并注明用了哪个**）：
  1. **archive 行**：`1\1\GINC-...\Freq\RB3LYP\Def2SVP\C2H5O3Na1(0)\...\HF=-xxx.xxxxxxx\RMSD=...` 里的 `HF=` = 该件**最终几何**的电子能（CPCM 下即溶剂化 SCF 能）；同一行的泛函 / 基组 / 分子式(电荷) 字段顺手做层级一致性核对；
  2. 该件**最后一次** `SCF Done:  E(RB3LYP) = -xxx.xxxxxxx     A.U. after N cycles`（必须是收敛终态那一次，**不是**优化中间步的过程值）。
  - TS 件必须取**收敛 TS 几何**对应的值（若 ts_optimization 是 opt+freq 合并件，archive 给的就是 TS 几何的能量）；**不得**取扫描峰帧 / 约束点 / 步中值 / 终止快照。
- **换算**：ΔE‡[kcal/mol] = (E_TS − E_start)[Hartree] × **627.509474**，保留 2 位小数。
- **硬门槛（任一不过就不出数）**：五件 engine/method/basis/keywords/solvent/charge/multiplicity 逐字相同；archive 行的方法/基组/分子式(电荷) 一致；全部来自本轮 Gaussian 16，**不与旧 ORCA 值相减**（NI5 的 3.59 教训）；只报 ΔE‡、不报 ΔG‡。
- **E1 特别提醒**：若 RC 存在多个构象（Na⁺ 在 O1/O5 之间的滑移很常见），必须写明用的是哪一个 RC 构象及其能量——不同 RC 构象直接改变 E1 的垒高。

## B-(f) 逐边验收票（可直接填）
| 项 | E1 | E2 | E3 |
| --- | --- | --- | --- |
| TS 日志绝对路径 + sha256 | | | |
| TS 收敛标记（Stationary point found + 四项 YES） | | | |
| 频率条数 = 3N-6 = 27 / Harmonic frequencies + l703 | | | |
| 虚频个数 = 1；ν_imag (cm⁻¹) | | | |
| watch fraction（或替代判据数值） | | | |
| Low frequencies 行 | | | |
| IRC 日志 + sha256；两方向点数 | | | |
| 两方向最外帧 + 8 值指纹 | | | |
| 方向区间证明（strict verify） | | | |
| 起点件（RC / I1 / I2）0 虚频 + 身份 | | | |
| 终点件（I1 / I2 / P）0 虚频 + 身份 | | | |
| E_TS (Hartree) / E_start (Hartree) | | | |
| ΔE‡ (kcal/mol) | | | |
| 判定（verified / candidate_only / partial） | | | |

## B-(g) 结论计数口径
只写两栏：**计算完成** 与 **验收通过**（result.verified=true 才算通过）。candidate_only（伪鞍点/模式不符）、search_failed（优化落回极小）、partial（IRC 方向或端点身份未决）**如实写**，并把"缺什么、已证伪什么"写清；缺测不填 0、不改图。
