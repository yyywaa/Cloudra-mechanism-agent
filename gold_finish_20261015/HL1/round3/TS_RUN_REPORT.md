# HL1_E1 · T4 ts_prepare 运行报告（round3，原始记录）

作者：HL1 TS 道 small_mol（session as_6ede162e1cc94641）；时间：2026-10-15 23:5x（SGT）。
范围：**只做 T4 = 至少跑一次 ts_prepare（provided guess），留 run_id / process.json / result.outcome 原文**。
本文件不改写任何原生日志、不改 registry/题面、不下「有无鞍点」的最终裁决。

## 0 结论先行（截至本文件落盘）

| 项 | 值 |
| --- | --- |
| ts_prepare run | **已建立**：run_id **ts_0010** |
| run_dir | `/home/ly/Cloudra-mechanism-agent/ts/ts_0010` |
| revision / export_revision | 11 / 11 |
| status / stage | **waiting** / **refine** |
| result | **null（尚无 verdict；因此 result.outcome 暂无可抄录原文）** |
| 在跑/排队作业 | job **975**（purpose=ts_opt，gaussian，8c/10240MB），state=ready→排队（队列在 971-974 之后） |
| 已尝试输入 | provided guess = ts_run/t4_interp/img_06.xyz；端点 = RC_3A_seed.xyz（reactant）/ round3/product_endpoint_seed_B_prodorder.xyz（product，A_RC_last.xyz 的行置换） |
| 是否需要人工动作 | 否（`next.action = wait_for_system`）；pipeline 自行推进 → freq → IRC → 两端 Opt/Freq |

> 因此本 run **尚未**给出 `search_failed` 或任何 outcome；「无鞍点」结论的原始记录须等 verdict 出现后在本文件续记（见 §6）。

## 1 ts_prepare 调用参数（实际发送，逐字）

```jsonc
reaction = {
  reactant_smiles: "[O+:1]([H:2])([H:9])[H:10].[CH3:11][CH2:5]/[C:4](=[N:6]/[O:7][H:8])/[CH3:3]",   // = jl.py L1 step1 mapped_reactants 原文
  product_smiles:  "[O:1]([H:9])[H:10].[CH3:11][CH2:5]/[C:4](=[N:6]/[O+:7]([H:8])[H:2])/[CH3:3]",  // = jl.py L1 step1 out 原文（水 + O-质子化肟）
  charge: 1, multiplicity: 1,
  atom_map: [1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,2,17,18,19],   // product 坐标序 → reactant 1-based 序
  reaction_center: [[1,2],[2,9]]                                 // break O1-H2 / form H2-O7
}
calculations = { formal: { engine:"gaussian", method:"B3LYP", basis_set:"def2SVP",
                 keywords:"EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight" } }
conformers = { reactant: {kind:"file", xyz_path:.../prep/RC_3A_seed.xyz, mol_path:.../prep/build_RCmap/assembly/complex_candidate_000.mol,
                          optimization:null, heavy_atom_binding:{indices:[1,5,6,7,8,9,10]}},
               product:  {kind:"file", xyz_path:.../round3/product_endpoint_seed_B_prodorder.xyz,
                          mol_path:.../prep/build_PCmap/assembly/complex_candidate_000.mol,
                          optimization:null, heavy_atom_binding:{indices:[1,4,5,6,7,8,9]}} }
guess = { kind:"provided", xyz_path:"gold_finish_20261015/HL1/ts_run/t4_interp/img_06.xyz",
          evidence_refs:[TS1_guess_provenance.md, RC_3A_seed.xyz, A_RC_last.xyz, A_RC_optfreq.log] }
ts_optimization = {ref:"formal"}
verification = { frequency:{ref:"formal"}, irc:{ref:"formal"},
                 reactant_endpoint:{optimization:{ref:"formal"}, frequency:{ref:"formal"}},
                 product_endpoint:{seed:{kind:"file", xyz_path:.../round3/product_endpoint_seed_B_prodorder.xyz,
                                         mol_path:.../prep/build_PCmap/assembly/complex_candidate_000.mol,
                                         evidence_refs:[A_RC_last.xyz, A_RC_optfreq.log, T4_INPUT_ORDER_PROVENANCE.md]},
                                   optimization:{ref:"formal"}, frequency:{ref:"formal"}} }
execution = { cpus: 8, memory_mb: 10240 }        // 未设任何非原生 MaxIter/MaxSteps/超时
```

方法口径：engine=gaussian（本机无 ORCA）、method=B3LYP、basis_set=`def2SVP`（Gaussian 原生 token，
= 任务书要求的 def2-SVP；BRIEF §3 与本批所有 .gjf 同写法，平台渲染逐字为 `#p ... B3LYP/def2SVP empiricaldispersion=gd3bj scf=tight int=ultrafine`）、
keywords=EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight、气相（不写 SCRF）、q=+1/m=1。

## 2 ⚠ 平台/工具面事件：无 concretely-bound 端点结构时 ts_prepare 抛 tool_exception（可复现）

**这是本 run 的前置事实，必须如实登记。**

1. **第 1 次调用**（上面声明的**初版**：只有 reaction/calculations/guess/ts_optimization/verification/execution，**没有 conformers**）：
   js_exec 程序在 ts_prepare 处被内部错误打断（程序失败，未取到 call_id）。
   只读取证（未动平台代码/数据库/进程）：
   - `ls -la /home/ly/Cloudra-mechanism-agent/ts` → 只有 ts_0001..ts_0009，无新目录；
   - 对 ts_0007/0008/0009 的 declare.json/process.json `grep -c "O+:"` → **0**（即三者都不是本包 run，分别是 NY3 / HI1）；
   → 本次调用**没有产生 run、没有副作用**（不是重复提交）。
2. **第 2 次调用**（**同输入**，try/catch 捕获）→ 可复现同一错误，原文：
   ```
   ToolCallError { code: "tool_exception", tool_name: "ts_prepare",
                   call_id: "tc_1418efb683964e2b", effect_state: "unknown",
                   message: "Tool execution failed internally. The error was logged; report the tool call instead of inspecting application source." }
   ```
3. **处置（未绕过工作流）**：对比本机所有**已成功**的 ts run（ts_0005/0006/0007/0008）——它们**都**声明了 `conformers.* = kind:"file"`（带 mol_path）。
   于是仅**补齐 concretely-bound 端点结构**（conformers.reactant/product = file + mol_path + heavy_atom_binding；**未改** registry SMILES、未改 guess、未改方法），
   第 3 次调用即成功建 run（call_id `tc_91e760555fee49c4`，is_success=true）。
4. **保守归因（只读取证支持，不作定论）**：疑似 ts_prepare 在「缺少 file 型端点结构、需由 registry 两组分 SMILES 自行组装」这条路上失败；
   同一 SMILES 用 `smiles_to_mol`(3D, charge=+1) 也报同类异常，原文：
   ```
   "Conversion raised an exception: the builder reported status='ok' but produced no MOL candidate:
    ['.../rc_build/assembly/complex_candidate_000.xyz', '.../rc_build/assembly/complex_candidate_001.xyz']."
   ```
   （即组装出候选但无法落 MOL）→ 与 issue #179 P1/P4 同类；本包建议主协调把本条（含 call_id `tc_1418efb683964e2b`）并入 #176/#179 台账。

## 3 具体原子序与 atom_map 的平台复核（本包最关键的防雷项）

判定依据与逐位验证过程见 `round3/T4_INPUT_ORDER_PROVENANCE.md`（sha256 a97f0467a46bbcade4e900135be57aa32f2d9269e77e951bd3e8adc57aed3d24）。
要点：用 NR1 已成功 run `ts/ts_0005` 的具体坐标表逐位**重现**了平台自身的 atom_map，得到规则
「按 SMILES 书写顺序的组分；组分内先列重原子（书写序），再按母重原子顺序追加其 H（写明的显式 H 会被剥离并加回此块）」。

**本 run 的平台复核结果（权威原文取自 ts_0010/process.json 的 map 阶段）**：

- `"binding_status": "complete"`、`"binding_source": "concrete"`、
  `"reactant_identity": "match"`、`"product_identity": "match"`
- 权威 `"atom_map": [1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,2,17,18,19]` → **与我声明的值逐位一致**
- `reaction_center` 存储为 0-based `[[0,1],[1,8]]` ≡ 声明 `[[1,2],[2,9]]`
- `binding_diagnostics`: `["reactant: Explicit heavy-atom binding accepted against the concrete graph.", "product: Explicit heavy-atom binding accepted against the concrete graph."]`
- bound structures：reactant `xyz_sha256=18dd830d…`(= prep/RC_3A_seed.xyz)、`heavy_atom_indices=[1,5,6,7,8,9,10]`；
  product `xyz_sha256=5b03a2ea…`(= round3/product_endpoint_seed_B_prodorder.xyz)、`heavy_atom_indices=[1,4,5,6,7,8,9]`；
  两者 `smiles_heavy_atoms` 逐位给出 map label `1,11,5,4,6,7,3` → 与本包统一序（1=O1、5=C11、6=C5、7=C4、8=N6、9=O7、10=C3）一致。
- 19 个原子表元素序：reactant `O,H,H,H,C,C,C,N,O,C,H×9`（= 本包序，= img_06.xyz 原序，**guess 无需重排**）；
  product `O,H,H,C,C,C,N,O,C,H×10`（= 我对 A_RC_last.xyz 做的行置换结果）。

## 4 run_dir 产物与 sha256（快照，随 pipeline 推进会变）

| 文件 | 绝对路径 | sha256（本快照） |
| --- | --- | --- |
| run state / export | `/home/ly/Cloudra-mechanism-agent/ts/ts_0010/process.json` | `e71d581024fa68e775c8f5e77a25ef0e65dac34c6f76f242c9c6437912297de9` (rev 11) |
| 声明回执 | `/home/ly/Cloudra-mechanism-agent/ts/ts_0010/declare.json` | `1ca9f56d3ecccd1601c115402ade296fe1cf34f55d085d26d4905afa0fc54621` |
| TS 优化原生输入 | `/home/ly/Cloudra-mechanism-agent/ts/ts_0010/jobs/declaration_0001/ts_opt/refine.gjf` | 见 §5 逐条 sha256 |
| TS 优化原生日志 | `/home/ly/Cloudra-mechanism-agent/ts/ts_0010/jobs/declaration_0001/ts_opt/refine.log` | **尚未生成** |
| bound reactant 表 | `/home/ly/Cloudra-mechanism-agent/ts/ts_0010/build/atom_tables/reactant_1_06df001d0abb.json` | — |
| bound product 表 | `/home/ly/Cloudra-mechanism-agent/ts/ts_0010/build/atom_tables/product_1_29a928b56597.json` | — |

## 5 管线自动提交的 job 台账

| job | purpose | engine | 资源 | 状态 | 原生输入路径 |
| --- | --- | --- | --- | --- | --- |
| **975** | ts_opt（OptTS,calcfc,noeigen） | gaussian | 8c / 10240 MB | ready → 排队（971-974 之后） | `/home/ly/Cloudra-mechanism-agent/ts/ts_0010/jobs/declaration_0001/ts_opt/refine.gjf` |

`refine.gjf` 路由行逐字（本 run 实际方法证据）：

```
#p opt=(TS,calcfc,noeigen) B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight
```

commit 阶段的 planned/actual 一致性原文：`"contract": {..., "source": "stage_declaration", "differences": [], "matched": true}`，
即 ts_opt 的实际配置 = 声明配置（gaussian / B3LYP / def2SVP / EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight）。

已提交阶段（available_results 原文 detail）：
- declare: "reaction declared; each calculation requires its own method"
- build: "both endpoints built"
- map: "19 atoms mapped; concrete endpoint identities bound to input revision 1"
- assemble: "2 reaction-centre pair(s) guide the assembly"
- guess: "Provided candidate bound; formal optimization and verification remain required."
- validate: "internal validation passed"
- submit: "refinement job 975 submitted as 'ready' (gaussian, B3LYP); the scheduler daemon claims it and its terminal state arrives through the existing compute notification path"

## 6 ts_inspect(run_id="ts_0010") 复核原文要点（call_id tc_cc49caef58474ed6）

```
run_id = "ts_0010"; revision = 11; run_dir = "/home/ly/Cloudra-mechanism-agent/ts/ts_0010"
status = "waiting"; stage = "refine"; result = null
waiting_for = [{job_id: 975, purpose: "ts_opt", state: "ready", req_cpus: 8, req_memory_mb: 10240,
                input_path: ".../jobs/declaration_0001/ts_opt/refine.gjf", job_type: "gaussian"}]
blocked = null; failed_attempt = null
next = {action: "wait_for_system", required_inputs: [], editable_groups: []}
message = "waiting for job 975 (ts_opt) to reach a terminal state; the existing compute notification path
           advances the system driver, so this stage never polls and emits no event"
```

→ 与 ts_prepare 返回一致；**还没有 verdict**，所以 `result.outcome` **暂无原文可抄录**（不是缺测）。

## 7 后续与「无鞍点」记录方式（本文件的续记位）

1. 等 job 975 收尾（pipeline 自动推进 freq → IRC → reactant/product 端点 Opt+Freq；端点声明如上）。
2. verdict 出现后在本节**原样抄录**：`result.outcome` / `verified` / `reason` / `evidence_refs`，
   以及每一步 job 的 job_id + 原生 `.log` 绝对路径 + sha256 + 关键行（虚频数值、该模位移组成/占比、IRC 双向端点、两端点 0 虚频与身份）。
3. 若 `outcome = search_failed`（无峰）：逐条给出无峰原文 + 已尝试输入（本 run 的 guess 与端点即「已尝试输入」），
   并在本文件登记，供 HL1 Coordinator 作为「无独立鞍点」原始记录使用。**本道不下化学裁决、不填 0、不改图。**

## 8 边界与未做事项

- 未改写任何原生日志（A_RC_optfreq.log / C2_RC3A_optfreq.log / 912/913 等一律未动）；未改 registry/题面；未提交 git；未手工提交 OptTS/IRC。
- `round3/product_endpoint_seed_B_prodorder.xyz` 是对原生 `ts_run/jobs/A_RC_last.xyz` 的**行置换**（置换表见 provenance 文件）；
  write 工具给出「suspected handwritten coordinates」告警——该文件仅作端点 seed 的**顺序载体**，原始 `A_RC_last.xyz` 与其日志仍是主证据（未被修改）。
- 未杀任何人作业、未改 priority、未重复提交（判定依据见 §2 只读取证）。
- 本报告只覆盖 T4（ts_prepare 一次）这一交付面。
