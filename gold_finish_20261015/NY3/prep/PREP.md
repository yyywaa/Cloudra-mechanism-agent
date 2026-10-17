# NY3 prep · 结构与身份证据（Na⁺ 中性模型，prep 阶段）

包：NY3（Coordinator as_bf15af420101498f）｜主题：gold-finish-20261015｜工作根：/home/ly/Cloudra-mechanism-agent
目录：`gold_finish_20261015/NY3/prep/`｜日期：2026-10-15
任务来源（唯一属主）：`cloudra/benchmark/normal_registry/yo.py` 的 "Y3"；题面 `ideapool/tasks/normal/NY3.json`

## 0 结论摘要

1. 四个物种 + 两个 TS 初猜的几何已落盘（每个 11 原子，分子式 C2H5NaO3，总电荷 0，单重态）。
   命名按包 Coordinator 要求：`rc`/`i1`/`i2`/`p`/`ts_e1_guess`/`ts_e23_guess`（.xyz + .mol），另附 6 个 .zmat。
2. 所有 Na⁺ 都是**真实配位**（不是游离的远处对离子）：
   - rc：Na–O1 2.276 / Na–O5 2.274，O1···C4 2.792（O1 已对准羰基碳，O1–C4···O5 = 104.6°，Bürgi–Dunitz 方向）。
   - i1：Na–O5(烷氧) 2.166（次配位 Na–O1 2.531）。
   - i2：Na–O1 2.524 / Na–O3 2.427（桥联甲酸的 O1 与甲醇盐 O3；Na–O5 3.463 不配位）。
   - p：Na–O1(甲酸根) 2.433 / Na–O5 2.091。
3. 身份核验通过（§4）：以 builder 原生 MOL 的 bond block + `M  CHG` 为准，与注册表 mapped SMILES 的 1-based map 号逐原子对应；键表与形式电荷见 §4.2。
4. **口径差异**：任务书写的"总原子数 12"与题源不符。按 registry `mapped_reactants` = `[Na+:7].[O-:1][H:6].[CH3:2][O:3][CH:4]=[O:5]`，Na1 + OH(2) + HCOOCH3(8) = **11 原子**（Na1 C2 O3 H5）。四物种与两个 TS 初猜都是 11 原子；本报告全按 11 原子口径。
5. **本阶段没有做任何几何优化**（未提交 Gaussian/ORCA/xTB，见 §1 边界）。所有几何是 RDKit/MMFF94 组装 + `internal_coordinates` 刚性变换产物，属于"待 QM 优化的起始结构"，不是极小值/鞍点。
6. 上轮"一次准备写入因工具异常失败"：本轮用真实 `ls`/`test -f`/`sha256sum` 核对，**当时本地不存在任何 NY3 准备产物**（§8）。

## 1 方法与边界（本道做了什么、没做什么）

工具链（全部为化学/结构工具，无 QM 提交）：
- `smiles_to_mol` / `conformer_search`（backend=rdkit）：共享结构构建器，多组分输入按"approved complex assembly"（刚性摆放采样 + 碰撞排除 + MMFF94 松弛）给出复合物候选；带 `distance_filters` 时为受约束的预组织搜索（guided assembly），输出可含 bond block 的原生 MOL。
- `internal_coordinates` mode=transform：对已有几何施加**刚性**旋转（绕两原子定义的轴）/拉伸（沿键平移 j 侧片段），不改共价拓扑；mode=analyze 用于键/角异常与 Z-matrix 导出。
- `format_converter`：xyz ↔ mol/sdf。
- 只读 python（numpy/math）脚本：测量距离/角度、搜索旋转参数。**坐标本身一律由工具产生，未手工键入任何坐标块。**

边界遵守：
- 未提交任何 QM 作业（Gaussian/ORCA/xTB 皆无），本包同一时刻 1 个 QM 作业的规则由 Coordinator 统一排队（本道不参与）。
- 只在 `gold_finish_20261015/NY3/` 内写文件；未改动其它包文件、未 git、未注册节点。
- 未做 xTB/CREST（虽然本机有 `/home/ly/xtb-6.5.0/bin/xtb`、`/home/ly/bin/crest`）——按边界属于禁用范围。

## 2 文件清单与 sha256（`cd gold_finish_20261015/NY3/prep`）

| 文件 | 原子数 | sha256 | 说明 |
|---|---|---|---|
| rc.xyz | 11 | c2e0db4302f9f3c15bd3c28b904a28d3a41a0284a5736c1f807d1b7fd10cf8e3 | RC：Na⁺ 桥联 O1/O5 且 O1 对准 C4 |
| rc.mol | 11 | 11060cbba1f27c339034dc01e0a0cc66f8f677d5206f9b29dd5ee1bc15c6d090 | format_converter 从 rc.xyz 生成（**无 bond block**，见 §4.4） |
| i1.xyz | 11 | d1b3b5a35548d4c1dd9c02de631ee84894ac2628b884046c28d6d7080354cea3 | I1：四面体烷氧盐 |
| i1.mol | 11 | c4165dfc33a88e26990c32b4c3911259ffc1b092b67aeeb1d595bea33feea184 | builder 原生 MOL（**含 bond block + M CHG**） |
| i2.xyz | 11 | 579e33e5ca1404a844e49f9d3c3385ec1b801ec19ee09ee732066c7860b4f665 | I2：甲酸 + 甲醇盐离子对，Na⁺ 桥联 O1/O3 |
| i2.mol | 11 | 6968448519c870a6415b67090bfabafe98f3b016c6c6944771e08d6339d25718 | 由 i2.xyz 生成（无 bond block） |
| p.xyz | 11 | 64b5ac9b3fb41718ff88ec882c1e88974b14186828c394f8ac7bd8ec5f78e796 | P：甲酸根 + 甲醇 + Na⁺ |
| p.mol | 11 | 165702ab64bcccbe6b7434b2b0a3a66379ed88deb4eab34d20bd1d729dcedf09 | builder 原生 MOL（含 bond block + M CHG） |
| ts_e1_guess.xyz | 11 | 7115db0d0cb184317a0de03eb1847a0658d043f8e0e2adc6904fafd2a4f0a25d | E1 四元环（Na–O1···C4–O5）TS 初猜 |
| ts_e1_guess.mol | 11 | 47ddf41ea7b39cd81ccf69d8895f5f1297e1614a171e7b0412068c9bba9f9f97 | 由 xyz 生成（无 bond block） |
| ts_e23_guess.xyz | 11 | 8c651f44ae7a7f5bc4b187109c1b4bfaf2f48c86a1899c7154fdedce6ae30399 | E2+E3 耦合六元环 Na–O5–C4–O3···H6–O1 TS 初猜 |
| ts_e23_guess.mol | 11 | 1b7ffab710d6b549186ce138dbc8414422b7de0c8304ca3a1b761886821fe84c | 由 xyz 生成（无 bond block） |
| rc.zmat | 11 | fa91a3cdd3546bbaa1e5b9e11f949fdd922d5b643c154ac49620b3bc03b34fba | internal_coordinates analyze 导出的 Z-matrix（几何同上） |
| i1.zmat | 11 | 8fcec13322660420553de31664c58d51e3737c052cb2bf9b9a9579ee3d1a6133 | 同上 |
| i2.zmat | 11 | 6e868c442daee7a2b44ed5527b1d1443d52fc45fccbb10dcb5d1d300d5545f1a | 同上 |
| p.zmat | 11 | 4be40d87482bebfaed39519ff668c7d95727780372db160991db92a55babc15d | 同上 |
| ts_e1_guess.zmat | 11 | d6fa8a3e4bbd59fb335a754c2de001840b3172ac51aea45d5e9e858e3aa1955d | 同上 |
| ts_e23_guess.zmat | 11 | 1b5fe55d853321428c87d8a81a8affd3599c663bbd778334704d83b7f443c18e | 同上 |
| build/ … | — | — | 全部源产物与中间几何（builder 候选、guided assembly、轨迹），见 §5 |

注：同目录下 `GUESS_PROVENANCE.md`（sha256 c217a93790128a09718ec2e97facedd67777eb38e4cce8b31fb1c9f53ba1af23）由包 Coordinator 道写入，用于 ts_prepare 的 evidence_refs，不是本道产物；其引用的 rc/i1/p/ts_e1 的 sha256 与本表一致。

## 3 原子序列表（1-based，含显式 H）与关键距离/角度

文件原子顺序 = **注册表 SMILES 的原子出现顺序**（隐式 H 按组分补在其重原子之后）。这是共享构建器的输出顺序，工具链没有重排原子的接口，故本表给出"文件序 → map 号"对应关系；建议的 canonical 顺序见 §4.3。

### 3.1 rc.xyz / ts_e1_guess.xyz（同一顺序）

| 文件序 | 元素 | 角色（map 号） | 备注 |
|---|---|---|---|
| 1 | Na | Na⁺（7） | 桥联 O1/O5 |
| 2 | O | O1（1） | 氢氧根 O |
| 3 | H | H6（6） | 氢氧根 H |
| 4 | C | C2（2） | 甲氧基甲基 C |
| 5 | O | O3（3） | 酯 O |
| 6 | C | C4（4） | 羰基 C |
| 7 | O | O5（5） | 羰基 O |
| 8,9,10 | H | H(C2) ×3 | 甲基 H |
| 11 | H | H(C4) | 甲酰 H |

关键距离（Å）与角度（°，由真实文件测出）：

| 量 | rc.xyz | ts_e1_guess.xyz | 目标窗口（任务书） |
|---|---|---|---|
| Na–O1 | 2.276 | 2.279 | 2.1–2.4 ✔ |
| Na–O5 | 2.274 | 2.252 | 2.1–2.4 ✔ |
| O1···C4 | 2.792 | 2.192 | rc 2.6–3.0 ✔ / TS-E1 2.0–2.2 ✔ |
| O1–H6 | 0.982 | 0.982 | ≈0.96 ✔ |
| C4=O5 | 1.228 | 1.231 | （酯羰基） |
| C4–O3 | 1.357 | 1.361 | （酯 C–O） |
| C2–O3 | 1.426 | 1.425 | |
| C4–H(C4) | 1.102 | 1.103 | |
| O1–C4···O5 | 104.6 | 104.7 | Bürgi–Dunitz 方向 |
| Na–O1–C4 | 64.0 | 76.9 | |
| Na–O5–C4 | 97.5 | 102.0 | |
| C4–O1–H6 | 120.8 | 112.6 | |
| 非键最小距离（除 Na） | 2.18 | 2.14 | 无重叠 |

### 3.2 i1.xyz（= ts_e23_guess.xyz 的原子序）

| 文件序 | 元素 | 角色（map 号） |
|---|---|---|
| 1 | Na | Na⁺（7） |
| 2 | C | C2（2） |
| 3 | O | O3（3） |
| 4 | C | C4（4）四面体 |
| 5 | O | O1（1）（OH） |
| 6 | O | O5（5）（烷氧 O⁻） |
| 7,8,9 | H | H(C2)×3 |
| 10 | H | H(C4) |
| 11 | H | H6（6）（在 O1 上） |

i1.xyz：Na–O5 **2.166**（烷氧配位）/ Na–O1 2.531 / Na–O3 2.229 / C4–O1 1.407 / C4–O5 1.309 / C4–O3 1.425 / O1–H6 0.976 / O1···O3 2.271；角 Na–O5–C4 88.6 / O5–C4–O3 105.1 / O5–C4–O1 99.8 → C4 为四面体中心 ✔

### 3.3 i2.xyz

| 文件序 | 元素 | 角色（map 号） |
|---|---|---|
| 1 | Na | Na⁺（7） |
| 2 | C | C2（2）（甲醇盐 CH3） |
| 3 | O | O3（3）（甲醇盐 O⁻） |
| 4,5,6 | H | H(C2)×3 |
| 7 | C | C4（4）（甲酸碳） |
| 8 | O | O5（5）（甲酰 =O） |
| 9 | O | O1（1）（甲酸 –OH） |
| 10 | H | H(C4) |
| 11 | H | H6（6）（在 O1 上） |

距离（Å）：**Na–O1 2.524 / Na–O3 2.427**（桥联请求的 O1 与 O3）/ Na–O5 3.463（不配位）/ Na···H6 2.106 / O1···O3 2.671 / O1–H6 1.009 / O3···H6 1.674（甲酸→甲醇盐氢键）/ C4=O5 1.224 / C4–O1 1.341 / C2–O3 1.325。
角度（°）：Na–O1···O3 55.6 / Na–O3···O1 59.1 / O1–H6···O3 168.5。

### 3.4 p.xyz

| 文件序 | 元素 | 角色（map 号） |
|---|---|---|
| 1 | Na | Na⁺（7） |
| 2 | C | C2（2）（甲醇 CH3） |
| 3 | O | O3（3）（甲醇 O） |
| 4,5,6 | H | H(C2)×3 |
| 7 | H | H6（6）（在 O3 上，即甲醇 OH） |
| 8 | C | C4（4）（甲酸根碳） |
| 9 | O | O5（5）（甲酸根 C=O） |
| 10 | O | O1（1）（甲酸根 O⁻） |
| 11 | H | H(C4) |

距离（Å）：**Na–O1 2.433 / Na–O5 2.091**（Na⁺ 配位甲酸根，双齿）/ O1···H6 1.614（甲酸根···H–O3 氢键）/ O3–H6 1.002 / C4=O5 1.265 / C4–O1 1.263（甲酸根两端 C–O 近等长，离域特征）/ C2–O3 1.421；角 O1···H6–O3 144.8 / O5=C4–O1 122.2。

### 3.5 ts_e23_guess.xyz（E2+E3 耦合六元环；原子序同 i1.xyz）

六元环 Na–O5–C4–O3···H6–O1（闭环边 O1···Na）距离（Å）：
Na–O5 **2.166** | O5–C4 1.309 | C4–O3 **2.011** | O3···H6 **1.372** | H6–O1 **1.380** | O1···Na 2.531
其他：C4–O1 1.407 | Na–O3 2.383 | O1···O3 2.752 | O5···O3 2.79 | 角 Na–O5–C4 88.6 / O5–C4–O3 106.2 / O5–C4–O1 99.8 / **O1···H6···O3 179.6**（H6 基本在 O1–O3 连线上，等距夹在两者之间 ✔）。
与任务书要求对照：C4–O3 2.011 ∈ 1.9–2.1 ✔；H6 夹在 O1/O3 之间 ✔；Na⁺ 同时配位 O5 与 O1 ✔。

## 4 身份核验

### 4.1 化学身份结论（与 registry `steps[].out` SMILES 一致）

| 节点 | registry SMILES（step out） | 本文件实测身份 |
|---|---|---|
| RC | `[Na+:7].[O-:1][H:6].[CH3:2][O:3][CH:4]=[O:5]` | Na⁺ + 氢氧根 + 甲酸甲酯（离子-偶极复合物，O1 未成键到 C4：2.792 Å） |
| I1 | `[Na+:7].[CH3:2][O:3][CH:4]([O:1][H:6])[O-:5]` | 四面体烷氧盐 C4(O1H)(O3Me)(O5⁻)(H)，Na⁺ 在 O5 |
| I2 | `[Na+:7].[CH3:2][O-:3].[CH:4](=[O:5])[O:1][H:6]` | 甲酸 + 甲醇盐离子对，Na⁺ 桥联 O1(甲酸) 与 O3(甲醇盐) |
| P | `[Na+:7].[CH3:2][O:3][H:6].[CH:4](=[O:5])[O-:1]` | 甲酸根 + 甲醇 + Na⁺（Na⁺ 在甲酸根 O1/O5 侧，甲醇通过 O1···H6–O3 氢键相连） |

### 4.2 权威键表与形式电荷（来源：builder 原生 MOL 的 V2000 bond block + `M  CHG`）

- **RC 源 MOL** = `build/g_RC_w283/guided_assembly/assembly/complex_candidate_000.mol`（与 rc.xyz 同几何的原始产物；rc.xyz 是其刚性旋转版，拓扑不变）
  键：O1–H6；C2–O3；O3–C4；C4=O5（双键）；C2–H ×3；C4–H。`M  CHG  2   1   1   2  -1` → 原子1(Na)=+1、原子2(O1)=−1 ⇒ 三个组分 [Na⁺]、[OH⁻]、[CH3OCHO]，与 `[Na+:7].[O-:1][H:6].[CH3:2][O:3][CH:4]=[O:5]` 完全一致。
- **i1.mol**：键 C2–O3；O3–C4；C4–O1；C4–O5；O1–H6；C2–H ×3；C4–H。`M  CHG  2   1   1   6  -1` → Na=+1、O5(烷氧)=−1 ✔ 四面体中心 C4。
- **I2 源 MOL** = `build/art_I2_src/assembly/complex_candidate_000.mol`（i2.xyz 由它刚性旋转 Na 得到）
  键：C2–O3；C4=O5；C4–O1；O1–H6；C2–H ×3；C4–H。`M  CHG  2   1   1   3  -1` → Na=+1、O3(甲醇盐)=−1 ✔
- **p.mol**：键 C2–O3；O3–H6；C4=O5；C4–O1；C2–H ×3；C4–H。`M  CHG  2   1   1  10  -1` → Na=+1、O1(甲酸根)=−1 ✔
- **两个 TS 初猜**：几何来自 rc（ts_e1）与 i1（ts_e23）的拓扑，键表同上；TS 文件本身只含坐标（.mol 由 xyz 转换而来）。

### 4.3 原子来源与建议的 canonical 顺序

- 每个重原子都能按 §3 的表对上 registry `mapped_reactants`/`steps[].out` 的 1-based map 号（O1=1、C2=2、O3=3、C4=4、O5=5、H6=6、Na=7；C2 上 3 H、C4 上 1 H 未编号）。
- **建议的 canonical（map）顺序**：1=O1, 2=C2, 3=O3, 4=C4, 5=O5, 6=H6, 7=Na, 8–10=H(C2), 11=H(C4)。
  交付文件**不是**这个顺序，而是"注册表 SMILES 原子出现顺序"（Na 在组分中的位置、H 补在各组分重原子之后）。原因：共享构建器按组分顺序输出，工具链（smiles_to_mol / conformer_search / internal_coordinates / format_converter）没有重排原子序的接口；为可审计性选择"顺序 = 注册表 SMILES 顺序"这一确定规则。若下游需要 map 顺序，可用 §3 的表逐原子重排（不需要重新生成几何）。

### 4.4 一个必须写明的工具局限

`internal_coordinates` / `format_converter` 的 RDKit 键感知对**含 Na⁺ 的复合物会失败**：analyze 对 6 个文件都报
`Formula: C2H5NaO3  Atoms: 11  Bonds: 11–13  Fragments: 1  Bond orders: distance-inferred (all single)`，
并在 Notes 里给出 `RDKit bond perception failed (Unable to determine valence of atom 1 ...)`。因此：
- 上表的"Fragments: 1"、Na–O 被算成键是**距离启发式**的结果，不是真实共价连接；真实拓扑是 2–3 个离子组分（见 §4.2 的 bond block）。
- 由 `format_converter` 从 xyz 生成的 .mol（rc.mol / i2.mol / ts_*.mol）只含坐标 + 元素，**bond block = 0**、无 `M  CHG`（工具明确提示 "Input xyz carries only coordinates (no bond/charge/stereochemistry)"）；i1.mol / p.mol 是 builder 原生 MOL，**有** bond block + `M  CHG`。身份核验因此以 §4.2 的 bond block 为准。

## 5 构造链（可审计）

| 最终文件 | 源产物（本目录内） | 施加的操作（internal_coordinates，1-based；不改拓扑） |
|---|---|---|
| rc.xyz | `build/g_RC_w283/guided_assembly/assembly/complex_candidate_000.xyz`（guided assembly 最近候选，Na–O1 2.02 / Na–O5 2.31 / O1···C4 2.98） | rotate [7,10]×[2,3] −21° → rotate [7,9]×[1] −19° → rotate [9,10]×[2,3] −4° → rotate [4,8]×[1] +3° → rotate [1,11]×[2,3] −8° |
| ts_e1_guess.xyz | `build/g_TS1_w21/closest_attempt.xyz`（引导搜索把 O1 拉到 C4 侧，最近 2.54 Å） | rotate [7,10]×[2,3] −12° → rotate [4,9]×[1] −9° → rotate [1,11]×[2,3] +12° → rotate [3,5]×[1] −2° → rotate [5,8]×[2,3] −2° |
| i1.xyz / i1.mol | `build/art_I1_src/assembly/complex_candidate_000.{xyz,mol}` | 直接复制（无变换） |
| i2.xyz | `build/art_I2_src/assembly/complex_candidate_000.mol`（bond-block MOL，保证不把 Na–O 当共价键） | rotate [4,7]×[1] +89°（把 Na⁺ 转到 O1/O3 之间） |
| p.xyz / p.mol | `build/art_P_src/assembly/complex_candidate_000.{xyz,mol}` | 直接复制（无变换） |
| ts_e23_guess.xyz | `prep/i1.mol` | rotate [7,8]×[3,2,7,8,9] +18°（甲醇盐离开 C4 到 2.01 Å）→ stretch [5,11]→1.38 Å → rotate [5,2]×[11] +26° → rotate [5,6]×[11] +167°（把 H6 摆到 O1···O3 连线上） |

构建器输入 SMILES（各节点 registry step SMILES，charge=0、multiplicity=1）：
rc `[Na+:7].[O-:1][H:6].[CH3:2][O:3][CH:4]=[O:5]`；i1 `[Na+:7].[CH3:2][O:3][CH:4]([O:1][H:6])[O-:5]`；
i2 `[Na+:7].[CH3:2][O-:3].[CH:4](=[O:5])[O:1][H:6]`；p `[Na+:7].[CH3:2][O:3][H:6].[CH:4](=[O:5])[O-:1]`。

## 6 已知偏差、风险与需要 Coordinator 知道的事

1. **RC 的 Na–O1 = 2.276 Å ✔**（在请求窗口内）；rc.xyz 是"Na 桥联 + O1 对准 C4"的合成几何，**不是 MMFF 最优**：builder 不经引导时的自然最小是 Na–O1 2.02 / Na–O5 2.31 / O1···C4 ≈ 3.0–4.6 Å（O1 不对准 C4）。若下游要"FF 自然几何"，用 §5 的源产物。
2. **I2 的 Na–O 偏长（2.52/2.43）且 Na···H6 = 2.106 Å 偏短**：原因是 I2 里 O1···O3 只有 2.671 Å（甲酸→甲醇盐氢键），把 Na⁺ 硬塞进这个口袋必然同时贴近 H6。MMFF 自身的偏好是 **Na⁺ 双齿 O3/O5（2.11 / 2.27）**，与任务书声明的"桥联 O1/O3"不同。这是"声明配位 vs FF 偏好"的分歧，**请在 QM 步骤里让优化自决**；我没有改声明。
   （若要避免 2.106 Å 的 Na···H 接触，可退让到 Na–O1 2.665 / Na–O3 2.567 / Na···H6 2.32 的变体，n=1 步旋转即可复现：rotate [4,10]×[1] +85° → rotate [3,11]×[1] −32°。）
3. **ts_e23_guess 的 C4–O5 = 1.309 Å** 继承 I1 的 MMFF 值（未额外收紧到 ~1.27）。TS 搜索会重整；若需要更"产物侧"的初猜可再调。
4. **TS 初猜的键级异常**是距离启发式的正常产物：ts_e23 报 2 个 bond anomalies（H6–O1 1.380、H6–O3 1.372 的"拉长/形成"对；C4–O3 2.011 的"断裂候选"），ts_e1 报 0 个 bond anomaly（O1···C4 2.192 被判为形成候选）。
5. **没有做几何优化**：本阶段所有数字是"准备几何"的距离，不是能量、不是极小值/鞍点。TS 的性质（虚频个数、IRC 双向）必须由 ts_prepare 的 OptTS/Freq/IRC 判定。
6. **原子数口径**：11（见 §0.4）。若题面/下游脚本按 12 原子校验，需要按 11 修正。

## 7 需要什么计算 + 为什么 + 预计规模（申请，不自行提交）

- 本阶段**不需要**为了"可用结构"而先做 xTB/DFT 优化：六个几何的身份与配位都可核验，可直接作为 QM 起点。
- 但下列计算建议尽早排给包 Coordinator（不属本道权限）：
  a. **四个物种的最小值**：Opt + Freq，B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight + SCRF=(CPCM,Solvent=Water)，charge 0 / singlet，11 原子。目的：确认 Na⁺ 在**中性模型 + CPCM(水)**下的真实配位位置（尤其 I2 的 Na⁺ 是"桥联 O1/O3"还是"双齿 O3/O5"），并给每条边的起点极小值（纯电子能）。
  b. **两条边的 TS**：E1 从 rc.xyz/ts_e1_guess.xyz 出发、E2+E3 从 i1.xyz/i2.xyz 与 ts_e23_guess.xyz 出发，走 ts_prepare（OptTS,calcfc,freq → IRC 双向）。E2+E3 是否真的耦合（六元环）需要在 TS 与 IRC 上判定；若判定耦合，按 BRIEF §7 只报证据 + 图裁决问题，不合并边。
  c. 规模：单作业 11 原子、≤12 cpus/≤14000 MB（按主协调 16:35 建议，**建议 8 cpus/≤10 GB** 以提高吞吐）。每条边 TS+IRC+两端 Opt/Freq 约 3–4 个作业。
- 本道不会提交这些作业。

## 8 上轮"一次准备写入因工具异常失败"的核对（真实命令与结果）

在本轮开始时（2026-10-15 15:58）的真实观察：`ls -la gold_finish_20261015/` 只有 `BRIEF.md`、`LEDGER.md` 与包目录（HI1/NR1/NY3），`gold_finish_20261015/NY3/` 下**只有 PLAN.md**，没有 prep/ 目录、没有任何结构文件。
本轮末尾复跑的核验命令与结果（命令原文，输出摘录）：

```
# CMD1 ls -la --time-style=full-iso gold_finish_20261015/
drwxr-xr-x 7 ly ly 4096 2026-10-15 16:29:53 HI1/ HL1/ NI5/ NR1/ NY3/ BRIEF.md LEDGER.md
# CMD2 ls -la --time-style=full-iso gold_finish_20261015/NY3/
-rw-r--r-- 1 ly ly 5951 2026-10-15 16:16:27.132802147 +0800 PLAN.md
drwxr-xr-x 3 ly ly 4096 2026-10-15 16:29:36.367495999 +0800 prep
# CMD3 find gold_finish_20261015/NY3 -maxdepth 1 -type f -printf '%T+ %s %p
' | sort
2026-10-15+16:16:27.1328021470 5951 gold_finish_20261015/NY3/PLAN.md     <- 唯一顶层文件；无任何上轮结构产物
# CMD4 test -f ...
ABSENT  gold_finish_20261015/NY3/prep/PREP.md      (本次交付才创建)
PRESENT gold_finish_20261015/NY3/prep/rc.xyz 554   (本道 16:16 生成)
PRESENT gold_finish_20261015/NY3/prep/i1.xyz 709   (本道 16:17 生成)
ABSENT  gold_finish_20261015/NY3/STATUS.md
# CMD5 find <root> -iname '*NY3*' -not -path '*/gold_finish_20261015/*'
ideapool/tasks/normal/NY3.json
gold_compute/edge_barriers/NY3.json
gold_compute/edge_barriers/computed/NY3.json
gold_compute/supplement_20261002/task_sources/NY3.json
gold_compute/library_audit_20261002/source_snapshot/published/ideapool/tasks/normal/NY3.json
# CMD6 sha256sum PLAN.md BRIEF.md
50f3149c6278e3923c148c440f8108bc09131a786abc8ab154032e99788bf01e  gold_finish_20261015/NY3/PLAN.md
2ad56671338110fe9cf203315d0c44f15de0c70363151eb3676ba030af8457b3  gold_finish_20261015/BRIEF.md
# CMD7 find gold_finish_20261015/NY3/prep -maxdepth 1 -type f -printf '%T+ %s %p
' | sort | head
最早文件 = 2026-10-15+16:16:55 gold_finish_20261015/NY3/prep/rc.xyz（本道本轮产物）
```

**结论**：上轮那次"准备写入"在本机文件系统里**没有留下任何 NY3 准备产物**（无 prep 目录、无结构文件、无 STATUS.md，全盘也没有 NY3 命名的运行目录/日志）。本轮 prep 的全部文件 mtime 均 ≥ 2026-10-15 16:16，可为对照。因此本轮的 prep **是从零建立**的，不存在与上轮残留混用的问题；上轮失败的具体原因无法从本机文件判定（无日志残留）。

## 9 与 PLAN 的差异 / 给 Coordinator 的要点

1. **原子数 11（不是 12）**——见 §0.4。
2. **I2 的 Na⁺ 位置存在"声明 vs FF 偏好"分歧**（§6.2）——建议在 E2/E3 的起点极小值优化里让 QM 自决，并在图上记录实际配位。
3. **E2+E3 耦合六元环假设**：ts_e23_guess.xyz 提供了与之相符的几何（Na–O5–C4–O3···H6–O1，C4–O3 2.011、H6 等距 1.38/1.37、O1···H6···O3 179.6°）；但**这只是初猜**，耦合与否必须由 TS/IRC 判定。
4. 所有交付文件的构造链与源产物路径都在 §5，任何数字都能用 §2 的 sha256 + 文件本身复核；本报告没有写入任何"手动键入的坐标"。
