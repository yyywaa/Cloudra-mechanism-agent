# HL1_E1 历史证据与已证伪清单（explorer A 段）
> 来源：agent_hub post evt_3a72b6b9764f4033（作者 session as_b0db9add78de47e3，explorer，只读复核），2026-10-15。本文件由 HL1 包 Coordinator 指派 writer 原样落盘；正文中「B 段状态」一节是写作时快照，B 段结论另见 AUDIT.md。

[HL1 包 · explorer A 段交付：历史证据与已证伪清单] 目标文件应落在 `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HL1/HISTORY.md`。
⚠ **本会话（explorer）的 write 权限被拒**（write 返回 "Tool requires permissions absent from this task"），所以我把完整内容贴在这里，请包 Coordinator 或 small_mol 原样保存为该路径的文件（内容自包含，无需再加工）。

一句话结论：E1 题源声明的是**分子间 O-质子化**（break O1–H2 / form H2–O7；barrier=null）；本地**不存在** HL1_E1 的任何原始产物（95/104/105/107 的输入与 `.cloudra/calc-*.out.log` 全部缺失，`gold_compute/campaign/` 与 `gold_compute/remote_backports` 亦不存在）；已撤回=旧 Gaussian 约束扫描的 0；已证伪=job 531（−1791.63）当 O-质子化 TS；未验收=95/104/105/107；**107 的扫描坐标/约束在本地材料中不足以确证**。

---
# HL1_E1 历史证据与「已证伪清单」（只读复核）

- 复核人角色：HL1 包 explorer（只读）；日期 **2026-10-15**；工作根 `/home/ly/Cloudra-mechanism-agent`
- 任务范围：仅 `HL1_E1`（(E)-丁酮肟 Beckmann 第①步：H3O+ 把肟 OH 的 **O** 质子化）。不碰 HI1/NR1/NI5/NY3。
- 方法纪律：**只信真实读取**（`find`/`ls`/`stat`/`read` 返回的 sha256）。不采信任何「变化流 / 删除报告 / 交接转述」作为文件存在性的证据；转述只作为「历史记录」引用并标明其身份。
- 本文件是 A 段产物；B 段（对 `gold_finish_20261015/HL1/ts_run/` 原生日志的独立复算）见 `AUDIT.md`，**当前尚未开始：截至本日 `gold_finish_20261015/HL1/` 下只有 `PLAN.md`，owner（small_mol `as_e24133cbb8374c2f`，directory 状态 running）还没有任何产物。**

---

## 0 速览（先看这 8 条）

1. 题源声明的 E1 是**分子间 O-质子化**：`break [[1,2]]`（H3O+ 的 O1–H2）、`form [[2,7]]`（H2–肟 O7）；`barrier_kcal_mol = null`。**不是** N-质子化。
2. 本地**不存在** HL1_E1 的任何原始产物：95 的 `HL1_E1_RC_optfreq.inp`、104/105 的 `path-task.json`、107 的 `scan.inp`，以及 `calc-95/104/105/107.out.log` 全部缺失。
3. 本地也**不存在**历史复核所引用的 ORCA 日志：`gold_compute/campaign/` 整个目录不存在（REVIEW_chem/modes_HL1 引用的 calc-531/528/529/645 路径本地不可达）；`gold_compute/remote_backups/` 也不存在（只在清单索引里出现）。
4. 唯一能**间接**证明 95/104/105/107 终态的本地文件是账本快照 status_20261002_0327.json（账本状态 ≠ 科学证据，且不含扫描坐标）。
5. 已**撤回**：`gold_compute/edge_barriers/computed/HL1.json` 里 HL1_E1 `barrier_kcal_mol = 0`（旧 Gaussian/WSL 的 13 点约束扫描，「candidate barrierless」）。2026-09-30 先改 null，2026-10-04 明确撤回措辞。
6. 已**证伪**（有本地记录、但证据本体本地缺失）：把 job **531** 的 −1791.63 cm⁻¹ 鞍点当成 E1 的 O-质子化 TS —— 它是 **O5→N4 分子内质子转移**，不符合声明步。
7. 仍**未验收**：95（RC 优化撞 MaxIter 失败）、104/105（path 准备 done 但无可用候选）、107（第 9 点未收敛 + PROPERTIES/SHARK 读临时输入失败；据交接终点落在 N 侧）。
8. 仍**有效**（未验收的约束性事实，不是数值）：E1 的化学定义、起点参考 = RC 复合物、E1 现值 null、以及「107 只能否定它自己那条路线，不能证明 O 路线无鞍点」。

---

## 1 逐来源一行清单（含日期与状态）

**（a）`gold_compute/supplement_20261002/HANDOFF_UNFINISHED_20261004.md` §2/§3「HL1_E1 O 质子化」**
内容日期 **2026-10-04**（文件末尾另有 2026-10-05 更新段，与 HL1 无关）；sha256 `b8a1d57cb2cec4cdba2f11d503df29077d8f5b0647cdf5c1235b480af63141a7`。

- 一行：95 未给出合格参考极小值 → **未验收**（对旧 ORCA 路线）。
- 一行：104、105 是路径准备作业，执行完成不代表有可用 TS；105 提高路径细化次数后仍无可用候选 → **未验收**。
- 一行：107 前 1–8 个受约束优化点收敛，第 9 点达原生上限未收敛，整体没有 ORCA 正常终止标记，PROPERTIES 阶段 SHARK 读临时输入失败 → **未验收（技术失败 + 未收敛）**。
- 一行：第 8 点比第 7 点高约 0.3766 kcal/mol，不能写成全程单调 → **证伪「全程单调」这一表述**（对旧扫描的叙述）。
- 一行：质子实际移向肟 N，不是声明的 O；不能据此证明 O 路线无垒或参考物种不存在 → **未确证 O 路线**（该文件自己就声明不能外推）。
- 一行：最后更正已撤回「candidate barrierless」；当前结论为 O 质子化缺测，107 路线封顶 → **已撤回**（旧结论作废），并保留「路线封顶」。
- ⚠ 注意：本文件对上述观测（第 9 点、0.3766、移向 N）没有给出扫描坐标、约束原子或日志行号，是**转述**。其原始日志本地不存在（见 §2）。

**（b）`gold_compute/supplement_20261002/prior_reviews/hard_hl1_2026-10-01.md`（= `gold_compute/hard_hl1_2026-10-01.md`，同 sha）**
内容日期 **2026-10-01**；sha256 `51132be526a2824479c1f76df43bf715b7d4822c8147ce42e0e19a8123a15bed`。文首自述「本记录取代 2026-09-30 的下游合并边说明」。

- 一行：E1 保持 **null** → **仍有效**（与最新审计一致）。
- 一行：E2 的旧 23.13 kcal/mol 与部分 IRC caveat 保留，本轮没有重新验证 E2 → **未验收**（但不是 E1 的问题）。
- 一行：全部相减能量来自同一 ORCA 6.1.1 方法，不与旧 ORCA 5 / Gaussian 能量混减 → **仍有效的口径约束**（对本轮同样成立：不得与历史能量混减）。
- ⚠ 易混点：该文「原子映射与证据位置」段写的「进攻水 O1 带 H9/H10，腈鎓 C4/N6」是 **E3/E4** 的原子角色（那一步的 O1 是进攻水）；**E1 的 O1 是 H3O+ 的 O，带 H2/H9/H10**。引用时不要串。

**（c）`gold_compute/archive/REVIEW_chem_HL1.md`**
自述「只读，未跑 QM 生产作业」；内容针对 2026-09-23 前后那批 ORCA 日志；git 末次提交 **2026-09-20 19:12:28 +0800**；sha256 `c474c14ea572fe0074beb492154242e69e442e479ee7cd6f94659bdffa96d014`。

- 一行：`HL1_E1`（calc-531）最终块 **1 imag，−1791.63 cm⁻¹**；几何感知为断 N4–H18（1.191 Å）、H12→O16 形成（1.499 Å），即 **O→N 质子转移**鞍点，**非**声明的 H3O+→oxime-O → **已证伪「531 ⟹ E1 的 O-质子化 TS」**（判定本身仍有效）。
- 一行：该文明确「与 JSON note 完全吻合：E1=null + 该鞍点为证据（即不采用）」 → **仍有效**。
- 一行：其引用的日志路径 `gold_compute/campaign/runs/HL1/E1/e1/.cloudra/calc-531.out.log` 本地**不存在** → 本地**不可复算**，只能作为历史复核记录引用。

**（d）`gold_compute/archive/REVIEW_modes_HL1.md`**
自述日期 **2026-09-18**；git 末次提交 **2026-09-20 19:12:28 +0800**；sha256 `6bd2ddfbe4805e77745a124e9cbff3a1a58b609980be216c7e90d852da713ae5`。

- 一行：`HL1_E1 (job 531)` — 最终块 1 imag，−1791.63 cm⁻¹；位移 H18 **99%**（距 N4 1.19 Å、O5 1.24 Å，桥接 O5/N4），N4 1%，其余 <0.5% → 「O5→N4 质子转移（肟 O→N 互变异构），**不是**声明的 H3O+→肟-O 质子化 → 判不符」 → **已证伪**（同一结论，位移口径更细）。
- 一行：该文补充「该鞍点最终未被用于势垒（HL1.json 把 E1 记为 barrierless=0），故不影响 E1 记录值，但它确实不能充当 O-质子化 TS」 → **已撤回**（前半个说法随 0 一起作废；后半个仍然有效）。
- 一行：其截图路径同样指向不存在的 `gold_compute/campaign/...` → 本地不可复算。
- 一行：该组其它边（HL1_E2 −304.17 符合、HL1_E5 −653.06 旁观 H3O+ 软模）**与 E1 无关**，本包不引用其数值。

**（e）`gold_compute/supplement_20261002/prior_reviews/agent_hint_dead_ends_2026-09-26.md`**
内容日期 **2026-09-26**（文末另有 2026-09-27 跟进段）；sha256 `e89fe5d5eb21e62130dae3428427847025dd56a9fef2a373982b004de04b3b51`。

- **结论：该文件不含任何 HL1 / HL1_E1 / 肟 O-质子化 的说法**（`grep -n 'HL1'` 零命中）。它记录的是 **normal 档** NI1/NU5/NY3/NU8 的四个用户提示案例，外加 NR4/NR1/NQ1/NQ5 的边界说明。
- 唯一可迁移的是它的**跨题教训**（「扫描只盯指定坐标、没有逐帧核对实际反应」「把机理图当清单而非假设」），与 107 的失败形态同类——但这是**类比**，不是关于 HL1_E1 的证据。
- 状态：**与 HL1_E1 无关（作为冲突源无效）**。

**（f）未点名但为分清状态所必需的三份（补读）**

- `gold_compute/hard_swap_2026-09-30.md`，内容日期 **2026-09-30**（文首自述「已于 2026-10-01 更新」被 (b) 取代）；git 末次提交 2026-10-01 03:17:08 +0800；sha256 `2132f2e31c5fd4c8ce00e259e11ef91596d8e813f6e525a11a1838685e7ed69f`。
  一行：**「E1 质子转移没有找到鞍点，旧 0.0 改为 null。」** → **已撤回**（0 → null 的第一次正式记账，日期 2026-09-30）。
- `gold_compute/edge_barriers/computed/HL1.json`，git 末次提交 2026-09-20 16:08:18 +0800；sha256 `e9d456f338e93f1442219d13e42a4c74eebff94db535cc826cc032befca52e39`。
  一行：`HL1_E1.barrier_kcal_mol = 0`，`frame = "HL1_E1rev_scan (13-pt constrained scan d(O8-H16) 1.0744->1.6980)"`，方法 `Gaussian16 via WSL gold_queue (4c/8GB each); gas phase`，note 写「13-pt constrained relaxed scan … rises MONOTONICALLY from I1 … 从剖面极大值出发的无约束优化收敛到 0-imag 极小值 → 峰就是 R 极小值，不是鞍点」，并自述依据 supervisor ruling `evt_919a9c5abb7c44f5` 条件 (a)–(d)「never report Ea=0.000 as a computed saddle - this is a barrierless endergonic PT edge」 → **这就是「旧 Gaussian 单调扫描 0」的出处；已作废，不得回填**。
- `gold_compute/edge_barriers/HL1.json`，sha256 `729b69ddadebd28541776cd470215dbe54814c332876971d17ceab1c498afc30`。
  一行：`HL1_E1: barrier_kcal_mol = null, verification = "unverified", note = "oxime O protonation PT; ~barrierless; compute"` → **仍有效**（现值 null；注意 note 里的「~barrierless」是**文献/直觉描述**，不是本地算出的结论）。

**（g）最新官方口径（冲突时以它为准）**

- `gold_compute/library_audit_20261002/open_edges.csv` 第 4 行（sha256 `d1bc2fb3a1f743357504accef9d0eb03468342882bd641b5ca7f041f9a440f83`，2026-10-02）：
  逐字：「`hard,HL1,HL1_E1,Beckmann：肟 OH 质子化,,最新源保持 null；旧 Gaussian 的无鞍点扫描与 ORCA 错位 PT 候选均不是现行合格回填。未见正式豁免/放弃。`」
- `gold_compute/library_audit_20261002/README.md` 第 36/45 行（sha256 `e7d5688dbe5b18cccee5ba286fff603d0e23cf66fabef97dd473da43716ba23a`）：同口径，并注「HL1_E1 仍是存量完整图的参考垒缺口」。
- `gold_finish_20261015/BRIEF.md` §2（2026-10-15，sha256 `30be36baed564aee136039a144e6d31c1d6504abb5a3fc755cf7972ed9af205f`）：逐字「旧值一律作废，**不得回填**：HI1_E1 19.2、HI1_E3 16.9、NY3 15.5/12.5/0.0、NR1 0、**HL1 0**。」

**冲突仲裁顺序（新 → 旧，冲突时取新）**
1. BRIEF 2026-10-15 / library_audit 2026-10-02（E1 = null，状态 open）——**权威口径**
2. HANDOFF §2/§3 2026-10-04（含「candidate barrierless」撤回）
3. hard_hl1 2026-10-01 + hard_swap 2026-09-30（E1 = null）
4. REVIEW_chem_HL1 / REVIEW_modes_HL1 2026-09-18~20（job 531 = O→N PT，非声明步）
5. edge_barriers/computed/HL1.json（Gaussian 0，最旧，**已作废**）
（`agent_hint_dead_ends_2026-09-26.md` 不含 HL1，不参与仲裁。）

---

## 2 真实文件系统核实（逐项「存在 / 不存在」）

核实命令与范围：`find /home/ly -maxdepth 8 -name 'calc-95.out.log'` 等、`find /home/ly -iname '*HL1*'`、`find . -name 'calc-*.out.log'`、`ls`、`stat -c %s`、`read`（取 sha256），cwd = `/home/ly/Cloudra-mechanism-agent`。

### 2.1 任务书面要求核实的 4 个作业

| 项 | 应然路径（远端，来自题/账本） | 本地 | 证据 |
|---|---|---|---|
| 95 输入 | `/data/cloudra/workspace/hard_resume_20260930/supplement_20261002/HL1_E1/HL1_E1_RC_optfreq.inp` | **不存在** | 仓库内外 `find -iname '*HL1*'` 无此文件；仓库内 HL1 命名文件仅 §2.4 所列 |
| 95 日志 | 同目录 `.cloudra/calc-95.out.log` | **不存在** | 全仓库 `find . -name 'calc-*.out.log'` 仅命中 23 个文件，全在 `research_runs/NU3-open-to-ring-20261015-26734223/`（NU3 包） |
| 104 输入 | `.../HL1_E1/ts/ts_0001/jobs/declaration_0002/path/path-task.json` | **不存在** | 无 `HL1_E1` 目录（`find . -type d -name 'HL1_E1'` 空） |
| 104 日志 | `.../declaration_0002/path/.cloudra/calc-104.out.log` | **不存在** | 同上 |
| 105 输入 | `.../declaration_0003/path/path-task.json` | **不存在** | 同上 |
| 105 日志 | `.../declaration_0003/path/.cloudra/calc-105.out.log` | **不存在** | 同上 |
| 107 输入 | `.../declaration_0004/scan/scan.inp` | **不存在** | 同上 |
| 107 日志 | `.../declaration_0004/scan/.cloudra/calc-107.out.log` | **不存在** | 同上 |

### 2.2 关键目录缺失

- `gold_compute/campaign/`：**不存在**（`ls` 报 `No such file or directory`）。→ REVIEW_chem_HL1 / REVIEW_modes_HL1 引用的 `gold_compute/campaign/runs/HL1/E1/{e1,e2,e5}/.cloudra/calc-{531,528,529}.out.log` 等**本地不可达**，其结论本地**不可复算**。
- `gold_compute/remote_backups/`：**不存在**。它只出现在 `gold_compute/organized_data/hard_20261001/08_integrity/raw_inventory.json`（远端 tar 的目录索引）里；`grep -c 'HL1_E1'` = 0、`grep -c 'supplement_20261002'` = 0 → **该清单根本没有收录本轮 95/104/105/107 那条链**。
- 全仓库无 `*.tar`/`*.zip`/`*.tar.gz`（除 `.venv` 内第三方包），**没有任何本地归档可以解出历史日志**。

### 2.3 ⚠ 名称冲突（重要：避免被同名文件误导）

- **存在** `/home/ly/Cloudra/CCsp2sp3_new_isomer_2026-10-02/CCsp2sp3_new_isomer_2026-10-02/runs/pm7_p2/.cloudra/calc-{95,104,105,107}.out.log`，但：
  - 大小仅 **83 / 84 / 1062 / 84 字节**（`stat -c %s`）；
  - `grep -c 'oxime\|N-O\|HL1'` = **0**；
  - 目录里是 `p_00_0*_D*.gjf/.log/.chk` 一批 **CCsp2sp3 异构体 PM7** 作业。
  → 与 HL1 无关，**不得**当作 HL1 原始产物。
- `raw_inventory.json` 第 114067 行的 `.../2026-09-23/G2/.cloudra/calc-107.out.log` 是 **2026-09-23 的 G2 作业号 107**，与 HL1_E1 的作业 107 是不同东西（同理第 107315 行 `calc-95` 属于 D1）。`raw_inventory` 是**远端清单索引**，不是本地文件。

### 2.4 本地**确实存在**的 HL1 相关产物（供对照，均非 E1）

- `gold_compute/organized_data/hard_20261001/02_calculations/HL1/jobs/job{009,010,016,017,030,031,037,042,043,044,046,047}/`：每个含 `input.inp` + `ledger.json` + **空的** `run_directory/`（如 job017/run_directory 列目录为空）→ 2026-09-29/30 那批 ORCA 作业（对应 E2/E3/E4 的 17/30/9/37/42/43/44/46/47 等），**没有 `.cloudra/calc-*.out.log`**。
- `gold_compute/grant_materials_20261001/raw/HL1/job_{9,16,17,30,31,37,42,43,44,46,47}/`：ORCA `.inp` + 引擎 sidecar（`.xyz`/`.hess`/`_trj.xyz`，例：`job_17/TS669_ORCA6.xyz`），同样**无原生日志**。
- `gold_compute/structures/HL1_2026-10-01/P_lower_job46.xyz`（仅一个几何）。
- 结论：**本地有 HL1 下游（E2/E3/E4）的输入与几何 sidecar，没有 native ORCA 日志；HL1_E1 的原始输入与日志 0 份。**

### 2.5 本地**间接**证据：账本快照（不是科学证据）

`gold_compute/supplement_20261002/monitoring/status_20261002_0327.json`（`utc: 2026-10-01T19:27:01Z` = SGT 2026-10-02 03:27；sha256 `b89b921cad7177cf0334fec1adcb06102a809d611a0b9b0c2c5a0cbacb9058d4`）逐条：

- `"id": 95, "session_id": "as_0af3d08a16c94d6a", "state": "failed", "path": ".../HL1_E1/HL1_E1_RC_optfreq.inp", "last_error": "ORCA 几何优化未收敛（达到最大优化步数），结果不可信"`
- `"id": 104, "state": "done", "path": ".../HL1_E1/ts/ts_0001/jobs/declaration_0002/path/path-task.json"`
- `"id": 105, "state": "done", "path": ".../HL1_E1/ts/ts_0001/jobs/declaration_0003/path/path-task.json"`
- `"id": 107, "state": "failed", "path": ".../HL1_E1/ts/ts_0001/jobs/declaration_0004/scan/scan.inp", "req_cpus": 8, "req_memory_mb": 4096, "last_error": "... ERROR (SHARK): Failed to read input file (.../declaration_0004/scan/scan.SHARKINP.tmp) ..."`

→ 与 HANDOFF §3 的叙述**一致**（95 失败 / 104、105 done / 107 SHARK 失败）。但账本行**不含**扫描坐标、约束原子或能量，故它支持「这些作业确实存在过、终态如何」；**不支持**任何关于「质子移向 N」的几何结论。

---

## 3 题源侧核实（逐字引用）

**（1）`cloudra/benchmark/hard_registry/jl.py`** — sha256 `7ed4e63a720ee6fced06cad5bd46811d59214732133b56220d76a75e56cc805c`（全文 52 行，`grep -n 'HL1'` 零命中：登记键是 **"L1"**，生成器再加前缀得到 task_id `HL1`）：

逐字引用 `steps[0]`（即 HL1_E1）：

```python
# [OH3+].CC/C(=N/O)/C>>CCNC(C)=[OH+].O  (+1/1)  (E)-丁酮肟 Beckmann
# 四步骨架：OH 质子化、anti 乙基迁移、水加成、O→N 质子转移。
# 映射：1=H3O+ 的 O，2=迁移质子，9/10=H3O+ 其余 H；3=肟碳上的甲基（不迁移），
# 4=肟 C，5/11=anti 迁移乙基（CH2/CH3），6=N，7=肟 OH 的 O，8=其 H。
...
        "mapped_reactants": "[O+:1]([H:2])([H:9])[H:10].[CH3:11][CH2:5]/[C:4](=[N:6]/[O:7][H:8])/[CH3:3]",
        "steps": [
            {
                # PT：H3O+ 质子化肟 OH
                "out": "[O:1]([H:9])[H:10].[CH3:11][CH2:5]/[C:4](=[N:6]/[O+:7]([H:8])[H:2])/[CH3:3]",
                "type": "proton transfer from H3O+ to the oxime OH (leaving-group activation)",
            },
```

→ **`steps[0]` 没有 `barrier` 键**（生成 `barrier_kcal_mol: null`）；产物映射里 **H2 从 O1 移到 O7**，N6 不带质子 → **O-质子化，分子间，PT**。

**（2）`ideapool/tasks/hard/HL1.json`** — sha256 `38081ed09c86db4acbf0e5e57d5cb65728d81dd0c15d44e0e4814b1f955384ae`（279 行），`gold.mechanism_graph` 中 HL1_E1 逐字：

```json
{"id": "HL1_E1", "from": "HL1_R", "to": "HL1_I1", "via": "HL1_TS1",
 "step_type": "proton transfer from H3O+ to the oxime OH (leaving-group activation)",
 "bond_changes": {"break": [[1, 2]], "form": [[2, 7]]},
 "accessible": true, "barrier_kcal_mol": null, "weight": 1.0,
 "channel": null, "favored": null}
```

节点逐字：`"HL1_R" → smiles ["[OH3+].CC/C(=N/O)/C"]`；`"HL1_I1" → smiles ["O.CC/C(C)=N/[OH2+]"]`；`"HL1_TS1" → smiles []`（role=transition_state）。
另：prompt 逐字「Barriers are electronic energy differences (ΔE‡) in kcal/mol, without ZPE or thermal corrections, each relative to that step's own starting minimum: **for a bimolecular reaction that minimum is the reactant complex** (e.g. the ion-dipole complex)」→ **E1 的参考极小值 = RC 离子–偶极络合物**。
系统项：`"charge": 1, "multiplicity": 1, "closed_shell": true, "max_heavy_atoms": 7`。

**（3）`ideapool/reaction_candidates/hard.md`** — sha256 `4ca22fc3d99339dfec73a59669a3e9cb742861da018f2af56e44c650b0cf903f`（220 行；文件头自述「日期：2026-08-31；v3 重配 2026-09-09」），**L1 行 = 第 145 行**，逐字关键字段：

- 反应式格：`[OH3+].CC/C(=N/O)/C>>CCNC(C)=[OH+].O`（(E)-肟经 RDKit 核对，乙基 anti 迁移 → O-质子化 N-乙基乙酰胺＋水），+1/1
- 机理格逐字：「**① 肟 OH 质子化**；② N–O 断裂与 anti 乙基迁移协同生成腈鎓离子；③ 水加成生成稳定的 O-质子化亚胺酸＋水 I3′；④ O→N 质子转移生成 O-质子化 N-乙基乙酰胺＋水。新气相计算已验证 I3′ 极小值及两条下游一阶鞍点，故撤销先前的净水合边，拆为两步；采用 IRC 得到的较低 P 构象（比原 P 低 1.89 kcal/mol）。」
- 能垒格逐字：「自算电子 ΔE‡ **23.13 kcal/mol（E2）** 保留旧一阶 Beckmann 迁移鞍点值及部分 IRC 连通 caveat；E3 水加成 **10.44**（相对 I2 络合物），E4 O→N 质子转移 **13.46**（相对 I3′ 络合物）。… **E1 保持 null**；孤立中性亚胺酸 28.46 不回填。证据见 `gold_compute/hard_hl1_2026-10-01.md`。」

→ md 锚点能垒格 = 23.13 = E2 值；**E1 无值**，故任何 E1 新值只需按 anchor 规则与 23.13 比较（>23.13 才需同步改 md 行）。

**（4）题源与历史的链接**：`gold_compute/library_audit_20261002/all_edges.csv` 第 40 行（sha256 `73650e9a8f18866a51c8bb4a17fec66aa6798b69116fdbaf6c5a8ce4abe13b16`）确认：`HL1_E1 … barrier 空 / weight 1.0 / status "open" / "缺测且未明确放弃"`；`gold_compute/organized_data/hard_20261001/01_results/edge_gold.csv` 第 20 行显示发布版 TaskSpec（`3ec62c55c8e3…`）里 HL1_E1 值为**空**（`HL1,HL1_E1,,`）。

---

## 4 「107 质子移向 N」是否针对本题声明的 O-质子化步？旧 Gaussian 单调扫描 0 的作废依据

### 4.1 107 的扫描坐标 / 约束 / 目标原子

**本地材料不足以确证。** 理由逐条：

1. 107 的输入文件（`.../declaration_0004/scan/scan.inp`）与日志（`calc-107.out.log`）本地**不存在**（§2.1）。无法读出它扫描的距离/角度、约束了哪些原子。
2. 本地唯一写「质子移向 N」的句子在 HANDOFF §3，逐字：「第 8 点比第 7 点高约 0.3766 kcal/mol，不能写成全程单调。**质子实际移向肟 N，不是声明的 O**；也不能据此证明 O 路线无垒或参考物种不存在。」——它是**转述**，未给出坐标/约束/原始行号；文件自身也只声明「不能据此外推」。
3. 本地账本行（status_20261002_0327.json 的 id 107）只给路径与 SHARK 报错，无坐标字段（§2.5）。
4. 因此本地**可以**确证的是：「107 这条路线据记录没有给出声明的 O-质子化结果」；本地**不能**确证的包括：107 扫描的到底是 `d(O7–H2)` 还是 `d(N6–H2)`；「移向 N」是指**扫描完成后的终点几何**、还是指**约束把质子往 N 拉**；107 前 8 点相对 107 自身起点的绝对值。
5. 要确证需要（远端，本机没有）：`.../HL1_E1/ts/ts_0001/jobs/declaration_0004/scan/scan.inp` + 同目录 `.cloudra/calc-107.out.log`，以及 `HL1_E1/HANDOFF.md` 末尾更正与 `REPORT.md`。**建议 owner 或主协调若日后拿到该归档，优先核对这一项。**

> 与题源对照的**逻辑**关系（可确证的部分）：E1 的 watch pair 是 **O1–H2 断 / H2–O7 成**（§3），质子必须落在肟的 **O7** 上。若 107 的终点把质子交给了 **N6**，则该终点对应的是 **HL1_I1 之外的物种**（N-质子化肟 + 水，即 `computed/HL1.json` 里提到过的 `-364.30370338` 那类 N-质子化组成），**与 E1 的产物节点 `HL1_I1 = O.CC/C(C)=N/[OH2+]` 不同**。这可以解释「107 不能作为 O 路线证据」，但**不能**解释成「O 路线无鞍点」。

### 4.2 「旧 Gaussian 单调扫描 0」的作废依据（本地可确证部分）

出处 = `gold_compute/edge_barriers/computed/HL1.json` 的 `HL1_E1: barrier_kcal_mol = 0`（方法 `Gaussian16 via WSL gold_queue … gas phase`，frame `HL1_E1rev_scan (13-pt constrained scan d(O8-H16) 1.0744->1.6980)`）。作废依据按时间：

1. **该文件自述**已写明 0 不是鞍点：逐字「Per supervisor ruling `evt_919a9c5abb7c44f5` conditions (a)-(d): never report Ea=0.000 as a computed saddle - this is a barrierless endergonic PT edge.」
2. **2026-09-30** `gold_compute/hard_swap_2026-09-30.md` 第 26 行：逐字「E1 质子转移没有找到鞍点，旧 0.0 改为 null。」
3. **2026-10-01** `gold_compute/hard_hl1_2026-10-01.md`：逐字「E1 保持 null；… 历史 `edge_barriers/HL1.json` 及 `edge_barriers/computed/HL1.json` 保持原貌，**不作为当前图的边值来源**。」
4. **2026-10-02** `gold_compute/library_audit_20261002/README.md` / `open_edges.csv`：逐字「旧 Gaussian 的无鞍点扫描与 ORCA 错位 PT 候选均不是现行合格回填。」
5. **2026-10-04** HANDOFF §3：逐字「最后更正已撤回"candidate barrierless"。当前结论为 O 质子化缺测，107 路线封顶。」
6. **2026-10-15** BRIEF §2：逐字「旧值一律作废，**不得回填**：… **HL1 0**。」

→ **作废本身无争议**（0 ≠ 合格能垒：无 TS、无 IRC、且是约束坐标上的能量跨度，不满足 BRIEF §4 验收链 1–4）。

**本地无法确证的部分（诚实登记）**：该扫描「是否真的单调」「是否真的没有鞍点」所依赖的原生日志（`HL1_E1rev_scan/HL1_E1rev_scan.log`、`HL1_E1_ts/HL1_E1_ts.log`、`HL1_R_opt5.log`、`HL1_I1_opt2.log`）在本机**不存在**。因此：0 被作废的依据（未经独立复核/不满足验收链 → 不得作为 gold）成立；但「那条 Gaussian 曲线是错的」目前只有 **流程性依据 + 单一自述**，**不是**本地可复算结论。引用时请写成「已作废（不得回填）」，不要写成「已被本地复算证伪」。

---

## 5 状态归类总表

| 归类 | 条目 | 支撑（本地） |
|---|---|---|
| **已撤回** | HL1_E1 `barrier = 0`（旧 Gaussian/WSL 13 点约束扫描的「candidate barrierless」） | computed/HL1.json 自述 + hard_swap 2026-09-30 + hard_hl1 2026-10-01 + library_audit 2026-10-02 + HANDOFF 2026-10-04 + BRIEF 2026-10-15 |
| **已撤回** | 「E1 无垒/近无垒（~barrierless）」作为**结论** | 同上；且 edge_barriers/HL1.json 的「~barrierless」只是 note 描述 |
| **已证伪** | job **531**（−1791.63 cm⁻¹）可当作 E1 的 O-质子化 TS | REVIEW_chem_HL1（2026-09-20 提交）+ REVIEW_modes_HL1（2026-09-18）：位移 H18 99%，桥接 O5/N4 → O→N 分子内 PT，非声明步 |
| **已证伪** | 「旧扫描全程单调」这一表述 | HANDOFF §3：第 8 点比第 7 点高 ~0.3766 kcal/mol（转述） |
| **未验收** | 95 RC Opt/Freq（ORCA 优化撞 MaxIter，未收敛） | status_20261002_0327.json id 95 failed + HANDOFF §3 |
| **未验收** | 104 / 105 路径准备（done 但无可用 TS 候选） | status 快照 id 104/105 done + HANDOFF §3 |
| **未验收** | 107 受约束扫描（第 9 点未收敛 + PROPERTIES/SHARK 失败；据记录终点在 N 侧） | status 快照 id 107 failed + HANDOFF §3 |
| **未验收** | 旧 Gaussian 13 点约束扫描（原生日志本地缺失，无法复核） | computed/HL1.json 自述 |
| **仍有效** | E1 化学定义：`break [[1,2]]` O1–H2、`form [[2,7]]` H2–O7，分子间 O-质子化，gas/q+1/m1，19 原子 C4H12NO2+ | jl.py / HL1.json / hard.md §3 |
| **仍有效** | 参考极小值 = **RC 离子–偶极络合物**（bimolecular 步） | HL1.json prompt 逐字 |
| **仍有效** | E1 现值 = `null`（open，未豁免未放弃） | edge_barriers/HL1.json + library_audit 2026-10-02 + edge_gold.csv |
| **仍有效** | 「107 只能否定它自己那条路线，不足以证明 O 路线无鞍点 / 参考物种不存在」 | HANDOFF §3 逐字 |
| **仍有效** | 能量不得跨程序/跨批混减（本轮 Gaussian 不得与历史 ORCA 23.13/10.44/13.46 相减） | hard_hl1 2026-10-01 + BRIEF §3 |
| **本地材料不足以确证** | 107 的确切扫描坐标/约束/目标原子；「移向 N」的原始几何证据 | §4.1 |
| **本地材料不足以确证** | 旧 Gaussian 扫描的原始日志与其「单调/无鞍点」自述 | §4.2 |
| **与 HL1_E1 无关** | agent_hint_dead_ends_2026-09-26.md（只写 normal 档 NI1/NU5/NY3/NU8） | 全文 grep HL1 零命中 |

---

## 6 对计算 owner（small_mol `as_e24133cbb8374c2f`）的防雷提示

1. **虚频身份是最大的坑**：历史上那条 −1791.63 cm⁻¹ 的鞍点「恰好也是 1 个虚频 + 几乎纯质子位移」，但它是 **O5→N4 分子内互变异构**。本轮的 O-质子化 TS 虚频同样会以质子为主 → **只看「1 个虚频」不够**，必须在同一日志里核 watch pair（O1–H2 / H2–O7，按该 run 实际 1-based 编号）占比，并报告重原子占比。
2. **起点要核氢键方向**：RC 必须是 H3O+ 与肟的氢键络合物，且要核 H3O+ 的 H 指向的是肟 **O7（O-侧）** 还是 **N6（N-侧）**。历史上 107 很可能就死在这里；若 RC 本身是 N-侧络合物，则「质子移向 N」只是起点错，不构成对 O 路线的否证。
3. **不要引用任何历史数值**（ORCA 23.13/10.44/13.46、Gaussian 0、28.46），也不要与它们相减；E1 只需相对**本批** RC 极小值自洽。
4. 若本轮最终仍拿不到合格 O-质子化 TS，**不要填 0、不要改图**；按 BRIEF §4 写「缺测 + 缺什么 + 已证伪什么」，并说明与 107 的差别（附本轮 RC 氢键方向证据）。
5. 产物落地后请把路径 + sha256 发到 `gold-finish-20261015`（本复核 B 段会从原生日志独立取数，不采用报告里的转述数字）。

---

## 7 B 段状态（截至本文件写作时）

- `gold_finish_20261015/HL1/` 下 **只有 `PLAN.md`**（`ls -R` 仅 1 个文件）；**没有 `ts_run/`**。
- owner `as_e24133cbb8374c2f`（small_mol，parent = HL1 coordinator `as_e9e07289de3d4c62`）在 agent_hub directory 里状态 **running**；主题 `gold-finish-20261015` 内**尚无 HL1 包 small_mol 的产物帖**（唯一 HL1 相关帖是 coordinator 的开工帖 seq 4048）。
- → **B 段（`AUDIT.md`：log_parser 虚频模式、原生日志能量 ΔE‡、IRC 双向端点、RC 几何）暂缓，待产物出现后执行。**

---

## 8 引用文件的 sha256 与日期

| 文件（项目相对路径） | sha256 | 日期（内容 / git 末次提交） |
|---|---|---|
| `gold_finish_20261015/BRIEF.md` | `30be36baed564aee136039a144e6d31c1d6504abb5a3fc755cf7972ed9af205f` | 2026-10-15 |
| `gold_finish_20261015/HL1/PLAN.md` | `3284882c579dd53b329e6fcc5edb180c62dbc1df93581b91257a710c673aa29c` | 2026-10-15 |
| `gold_compute/supplement_20261002/HANDOFF_UNFINISHED_20261004.md` | `b8a1d57cb2cec4cdba2f11d503df29077d8f5b0647cdf5c1235b480af63141a7` | 2026-10-04（+10-05 段） |
| `gold_compute/supplement_20261002/prior_reviews/hard_hl1_2026-10-01.md` | `51132be526a2824479c1f76df43bf715b7d4822c8147ce42e0e19a8123a15bed` | 2026-10-01 |
| `gold_compute/hard_hl1_2026-10-01.md` | `51132be5…`（与上同一内容） | git 2026-10-01 03:17 +0800 |
| `gold_compute/archive/REVIEW_chem_HL1.md` | `c474c14ea572fe0074beb492154242e69e442e479ee7cd6f94659bdffa96d014` | git 2026-09-20 19:12 +0800 |
| `gold_compute/archive/REVIEW_modes_HL1.md` | `6bd2ddfbe4805e77745a124e9cbff3a1a58b609980be216c7e90d852da713ae5` | 自述 2026-09-18；git 2026-09-20 19:12 +0800 |
| `gold_compute/supplement_20261002/prior_reviews/agent_hint_dead_ends_2026-09-26.md` | `e89fe5d5eb21e62130dae3428427847025dd56a9fef2a373982b004de04b3b51` | 2026-09-26（+09-27 段） |
| `gold_compute/hard_swap_2026-09-30.md` | `2132f2e31c5fd4c8ce00e259e11ef91596d8e813f6e525a11a1838685e7ed69f` | 2026-09-30；git 2026-10-01 03:17 +0800 |
| `gold_compute/edge_barriers/computed/HL1.json` | `e9d456f338e93f1442219d13e42a4c74eebff94db535cc826cc032befca52e39` | git 2026-09-20 16:08 +0800 |
| `gold_compute/edge_barriers/HL1.json` | `729b69ddadebd28541776cd470215dbe54814c332876971d17ceab1c498afc30` | — |
| `cloudra/benchmark/hard_registry/jl.py` | `7ed4e63a720ee6fced06cad5bd46811d59214732133b56220d76a75e56cc805c` | — |
| `ideapool/tasks/hard/HL1.json` | `38081ed09c86db4acbf0e5e57d5cb65728d81dd0c15d44e0e4814b1f955384ae` | — |
| `ideapool/reaction_candidates/hard.md` | `4ca22fc3d99339dfec73a59669a3e9cb742861da018f2af56e44c650b0cf903f` | 2026-08-31（v3 2026-09-09） |
| `gold_compute/library_audit_20261002/open_edges.csv` | `d1bc2fb3a1f743357504accef9d0eb03468342882bd641b5ca7f041f9a440f83` | 2026-10-02 |
| `gold_compute/library_audit_20261002/README.md` | `e7d5688dbe5b18cccee5ba286fff603d0e23cf66fabef97dd473da43716ba23a` | 2026-10-02 |
| `gold_compute/library_audit_20261002/all_edges.csv` | `73650e9a8f18866a51c8bb4a17fec66aa6798b69116fdbaf6c5a8ce4abe13b16` | 2026-10-02 |
| `gold_compute/supplement_20261002/monitoring/status_20261002_0327.json` | `b89b921cad7177cf0334fec1adcb06102a809d611a0b9b0c2c5a0cbacb9058d4` | 2026-10-01T19:27Z（SGT 10-02 03:27） |
| `gold_compute/organized_data/hard_20261001/01_results/edge_gold.csv` | `eabc693b7ca7650f4904d2bd7896842eed86c297def11ec71516ba43ef7a54a9` | published TaskSpec `3ec62c55c8e3…` |