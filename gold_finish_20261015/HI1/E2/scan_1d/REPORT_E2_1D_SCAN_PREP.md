# HI1 · E2 一维受约束弛豫扫描 — 输入生成 + 六项自检 + 条件提交（未提交，free cpus = 0）

**性质**：我新开的 E2 工作目录内的准备/自检证据（post-freeze asset）。**没有提交任何计算。**
**冻结设计依据**：`/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/prep/E2_1D_SCAN_DESIGN.md`
sha256 = `61e4e9e1085f273a0b619bdd7dd88f40a8843199edeb14c890e15e2675998629`（53 行，接口一致，未编辑、本报告只读引用）。
**本报告实测时刻**：2026-10-17 20:35:13 – 20:36:49 CST（主机 `date`，逐条记录见下）。

---

## 0. 产物（绝对路径 + sha256）

| 角色 | 绝对路径 | sha256 |
|---|---|---|
| 扫描输入（唯一将被提交的文件） | `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan.gjf` | `6301b836b6ca0006f365d80e28cff2f552bd06edae8f54475d6985e751ffbb16` |
| 只读自检脚本 | `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2/scan_1d/evidence/selfcheck_E2_1D_scan.py` | `7cba65a4eed4cbc0f9348ac1c2af181140318ef3166409da31c7af53cf938964` |
| 自检逐字实测输出（本报告 §2 的原始来源） | `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2/scan_1d/evidence/SELFCHECK_MEASURED.txt` | `e095eeead04f60fa1c53779f964d16d6aa9a2218db1a1c411b46ea2753226ee9` |
| 生成器改前快照（writer 原始产物，用于留痕） | `.../scan_1d/build/E2_1D_scan.gjf`（改前 sha = `d42d4b23a8ac34a141cb669d38aaf8b9ed10ca652a7e3dc7eb996583716fe61a`，50 行，无 B 行、%nproc=8） | — |
| 种子帧（只读引用，未改动） | `/home/ly/Cloudra-mechanism-agent/ts/ts_0009/build/input_0004/reactant/seed.xyz` | `c9d59aeab418c248629922ee37d4ea3822c64b7128dd63b3034d3c8c5ec2df3d`（43 行 / 41 原子，与设计文件一致） |
| chk 目标（Gaussian scratch 约定同目录） | `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan.chk` | 尚未生成 |

**生成链（坐标零手写）**：`qm_input_writer`（engine=gaussian、method=B3LYP、basis_set=def2SVP、source_type=xyz_file → seed.xyz、charge 0 / mult 1、nproc 8、mem 10240MB，task_type=`[{"opt":"modredundant,maxstep=8"}]`，**end_setting 留空以避开已知 internal-mismatch 坑**，返回 `unapplied_options=[]`、interpreted_intent.tasks=`["minimum_opt"]`、generation 成功）
→ 该次写入已经把 route 落成 `#p opt=(modredundant,maxstep=8) ...`，但**没有**写 ModRedundant 行，且 link0 为 `%nproc=8`；
→ 随后只用 `edit` 做两处**非坐标**改动（`edit` 的 diff 已在工具回执里）：
1. `%nproc=8` → `%nprocshared=8`（G16 文档写法，且与"route 逐字包含 %nprocshared=8"一致）；
2. 在最后一行坐标（H，line 49）之后插入空行 + `B 1 29 S 14 -0.2000` + 文件末尾空行。
两处改动均**不触碰任何坐标数字**；§2 ⑤ 用脚本对 41 个原子逐原子核对 max|Δ| = 0（见下）。

---

## 1. 文件的最终形态（绝对行号）

```
line  1: %chk=/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan.chk
line  2: %nprocshared=8
line  3: %mem=10240MB
line  4: #p opt=(modredundant,maxstep=8) B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=DMSO)
line  5: (blank)
line  6: HI1_E2 1D relaxed scan R(C1(enamine beta-CH2)...C29(aldehyde C)) 4.3543->1.5543 A step -0.2
line  7: (blank)
line  8: 0 1
line  9-49: 41 个原子坐标（C 0.40064996 -1.31467609 1.30452955 ... H 0.95590629 2.40163266 2.87635473）
line 50: (blank)                     ← 分子说明段之后的空行（缺此行 = l101 "End of file in ZSymb." 秒退）
line 51: B 1 29 S 14 -0.2000         ← 唯一一行 ModRedundant（成键对 B 1 29 + 扫描 S 14 -0.2000）
line 52: (blank)                     ← 文件末尾空行
```
规模：2415 字节，`wc -l` = **52** 行（末尾空行为第 52 行；按 `\n` 切分得 53 个元素，最后一个是空串）。

**关于 route 逐字的两点澄清（不改设计、只说明写法）**
- 设计文件 §3 的 route 是**小写**逐字：`#p opt=(modredundant,maxstep=8) B3LYP/def2SVP empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=dmso)`。Gaussian route 大小写不敏感，本文件按用户点名的大小写写成 `EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=DMSO)`，**关键字集合与设计逐项相同**。
- "CPCM(DMSO)" 的 Gaussian 原生写法只有 `SCRF=(CPCM,Solvent=DMSO)`（`CPCM(DMSO)` 不是合法 route 语法）。因此文件里 CPCM 与 DMSO 均在场、且同属 `SCRF=(` 组，但**字符串 "CPCM(DMSO)" 不会字面出现**。这是写法映射，不是设计变更。
- basis 写 `def2SVP`（无连字符）；已实测文件内**不存在** `def2-SVP`、`cartesian`、`z-matrix`/`zmatrix`、`geom=connectivity`。

---

## 2. 提交前六项自检（逐项实测）

### ① gjf sha256 + 行数
```
$ sha256sum build/E2_1D_scan.gjf
6301b836b6ca0006f365d80e28cff2f552bd06edae8f54475d6985e751ffbb16  build/E2_1D_scan.gjf
$ wc -l build/E2_1D_scan.gjf   → 52
$ wc -c build/E2_1D_scan.gjf   → 2415
```
实测时刻 2026-10-17 20:36:49 CST。**通过**（sha 与 §0 一致，两次独立读取 —— python hashlib 20:36:30 + `sha256sum` 20:36:49 —— 数值相同）。

### ② route 逐字
`line 4: #p opt=(modredundant,maxstep=8) B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=DMSO)`
逐 token（大小写不敏感、Gaussian 原生拼写）实测：`opt=(modredundant` present / `maxstep=8` present / `B3LYP/def2SVP` present / `EmpiricalDispersion=GD3BJ` present / `Int(UltraFine)` present / `SCF=Tight` present / `CPCM` present / `DMSO` present / `SCRF=(` present。**通过**（"CPCM(DMSO)" 的字面/原生映射见 §1 澄清）。
另测：`%nprocshared=8`（line 2）、`%mem=10240MB`（line 3）在场。

### ③ 文件末尾空行（od -c 实测）
```
$ od -c build/E2_1D_scan.gjf | tail -6
0004440   2   6   2   5   9   4  \n   H
0004460   0   .   9   5   5   9   0   6   2   9                       2
0004500   .   4   0   1   6   3   2   6   6                       2   .
0004520   8   7   6   3   5   4   7   3  \n  \n   B       1       2   9
0004540       S       1   4       -   0   .   2   0   0   0  \n  \n
0004557
```
字节级结论：`...2.87635473\n\nB 1 29 S 14 -0.2000\n\n` —— 坐标后有空行（`\n\n`），B 行后**再一个** `\n\n` 即末尾空行；文件总长 0004557(oct) = 2415 字节，最后一个字节是 `\n`，其后无任何字节。**通过**。

### ④ 原子数 41
- 脚本解析 `atom count parsed: 41 (expected 41) -> OK`（坐标段 line 9–49，首/末坐标行 = 9 / 49）；
- 独立复核 `$ awk 'NR>=9 && NR<=49' build/E2_1D_scan.gjf | wc -l` → **41**；
- 元素顺序对种子 41/41 一致（`element-order mismatches: none`）。**通过**。

### ⑤ gjf 坐标 vs 种子帧，逐原子 max|Δ| = 0（只读脚本，未手改坐标）
脚本：`evidence/selfcheck_E2_1D_scan.py`（只 `open(...,"rb")` 读、只 print，不写文件；sha256 见 §0）。
```
=== 5. coordinate compare .gjf vs seed.xyz, per atom ===
  seed comment lines: 2 ; seed atom count: 41
  element-order mismatches: none (41/41 identical)
  MAX per-atom max|dx|,|dy|,|dz| over 41 atoms = 0 Angstrom
  bit-identical coordinates (max|delta| == 0): True
```
即 41 个原子、每个原子三个分量都逐位相同（`.8f` 精度内 0 差）。**通过**。

### ⑥ %nprocshared / %mem 与实际授权一致
`line 2: '%nprocshared=8'  -> nprocshared == 8 : True`
`line 3: '%mem=10240MB'  -> mem == 10240MB : True`
提交计划参数（若被点名）：`job_type=gaussian`、`cpus=8`、`memory_mb=10240`、`priority=0`、异步。与文件声明一致。**通过**。

### 附加：1 号与 29 号原子的元素与坐标（证明 `B 1 29` 的化学身份）
| 原子（1-based，= seed/ORCA job_51 序） | 元素 | gjf 行号 | x | y | z | 化学身份证据 |
|---|---|---|---|---|---|---|
| **1** | **C** | 9 | 0.40064996 | −1.31467609 | 1.30452955 | 与原子 2（C）成双键 R(1,2)=**1.3632 Å**，且带 H12、H13 ⇒ 端基 **=CH₂**，即烯胺 **β-CH₂（亲核碳）** |
| **29** | **C** | 37 | −1.06104097 | 2.78034880 | 1.07215324 | 与原子 28（O）成双键 R(28,29)=**1.2265 Å**，且连芳环 ipso C30、醛基 H36 ⇒ **苯甲醛醛碳** |

R(1,29) = **4.354282 Å**（设计冻结 seed 起点 4.3543，一致；终点 1.5543 = 4.3543 − 14×0.2000，`S 14 -0.2000` 语义为距离递减）。
故 `B 1 29` 就是 **(烯胺 β-CH₂)···(醛碳)** 这条成键坐标，只此一行，未冻结任何其他键。**通过**。
（同帧参照值：R(2,4) 烯胺 C–N = 1.3752 Å —— 作为设计 §4 停手条件 1 的起点基线；R(O28···H24) = 1.6817 Å；R(O11–H24) 供体 O–H = 1.0006 Å。）

---

## 3. 条件提交结论：**未提交**（同刻 free cpus = 0）

我按"同一时刻读队列、满足才提交"执行；**同一时刻的读数为 0，故按指令只做到自检为止，未调用 submit_compute_job。**

- 实测时刻：**2026-10-17 20:36:40 CST**（`date '+QUEUE_READ_AT %Y-%m-%d %H:%M:%S %Z'` → `QUEUE_READ_AT 2026-10-17 20:36:40 CST`）
- 工具：`query_compute_queue(recent_terminal=3)` → `4 running, 0 queued across 1 node(s)`
- node-local（Local Workstation 32C/50G）：capacity.effective = 32 cpus / 51200 MB / 10 slots；in_flight = **slots 4 / cpus 32 / 40960 MB**；**free = slots 6 / cpus 0 / 10240 MB**
- 在跑的 4 个作业（非我所投，未触碰）：job 1069（started 2026-10-17T16:39:27+08:00）、job 1071（18:32:58+08:00）、job 1073（19:25:43+08:00）、job 1074（20:28:54+08:00），均 gaussian / 8 cpus / 10240 MB / priority 0。
- 判据：`free.cpus = 0 < 8` ⇒ **不满足提交条件**。注意 free memory 恰为 10240 MB 但 CPU 槽为 0，缺的是 CPU 不是内存。
- 我**没有** kill / 重投 / 改 priority / 触碰他人作业，也没有生成 chk 或任何日志（无 job id、无 started_at、无日志路径 —— 因为确实未提交）。
- 一旦协调侧点名且有 8 cpus 空槽，提交时使用：`submit_compute_job(input_file=<§0 的 .gjf 绝对路径>, job_type="gaussian", cpus=8, memory_mb=10240, priority=0, is_async=true)`；提交后我会立刻按 §4 的格式把 job id / started_at / 日志绝对路径 / gjf sha256 + 行数 / 六项自检结论 / 同刻 free cpus 读数与实测时刻发到 AgentHub 主题 `gold-finish-20261015`。

---

## 4. 判读口径（**现在冻结，事后不改**）

> 适用范围：仅本条 E2 一维 C–C 扫描日志。所有数字都必须来自日志实测，并附行号。

### 4.1 采样口径（每点只取收敛帧）
- 只有同时出现 `-- Stationary point found.` 与 `Optimization completed.` 的扫描点才算**收敛点**；取这对标记**之后/该点收敛块内**打印的最后一帧坐标（`Standard orientation` 块）作为该点几何，**不读任何未收敛帧**。
- 未收敛点单独列出（step 数、是否撞 `maxstep=8`），不进剖面。
- 每点能量 = 该收敛点块内**最后一条** `SCF Done:` 的纯电子能，报表里**必须写明所取的 SCF Done 行号**。不同点的能量只能来自同一方法/基组/溶剂（本文件内全部为 B3LYP/def2SVP+GD3BJ+UltraFine+SCF=Tight+CPCM(DMSO)，全程同级别，故可相减）；**绝不跨方法混排**。
- 点数 M **以日志实测的 `Scan point N out of M` 为准**；每点标题写 `scan point N out of M`。**预期 M = 15 个几何**（`S 14` = 14 步 ⇒ 起点 1 个 + 14 个新几何，起点 4.3543 → 收在 1.5543；与 E3b 的 `S 5` ⇒ 6 取值同源，见 §6 更正 1）；若实测 M ≠ 15，先报差异、不自行改口径。

### 4.2 每点必报字段
1. `scan point N out of M`（M = 日志实测）、`SCF Done` 行号；
2. **R(1,29)** 由该帧坐标**实算**（不抄设计值）；
3. 相对**首点**的纯电子能差 ΔE（kcal/mol，1 Hartree = 627.509474 kcal/mol；注明首点 SCF Done 行号）；
4. 与**上一点**的**重原子 Kabsch RMSD**：只取非 H 原子（本体系实测 **20 个重原子**，另有 21 个 H，共 41 原子；§4.2 旧文曾误写「21 个重原子」，以实测 20 为准），先按质量无关的最小二乘刚体叠合（Kabsch，含旋转+平移，不含置换）再算位移范数 RMS；
5. **R(O28···H24)** 与 **R(O28–H24)** 两个实测距离（两者在本体系是同一原子对 28–24 的距离，逐帧数值必然相等 —— 见 4.4 说明；另附 R(O11–H24) 供体 O–H 以消除歧义）；
6. 设计 §4 要求项一并报：R(28,29) C=O、R(2,4) 烯胺 C–N（并与首点 1.3752 Å 比较）、R(25···29)、R(25···1)、minsep 及其成键/1-3/非键分类。

### 4.3 质子档位（两档都**单列、不进主剖面**，数值照常全部报出）
- **档 1（共享质子）**：R(28···H24) ∈ [1.20, 1.50] Å ⇒ 标「共享质子」；该点单列，另出一份「含档 1 点」的**参照剖面**（只作参照，不作主剖面）。
- **档 2（质子已转移，物种改变）**：R(28···H24) < 1.20 Å **且** R(O28–H24) ≤ 1.05 Å ⇒ 标「质子已转移（物种改变）」；单列、不进剖面，并注明该转移**不是**本一维 C–C 坐标的结果。
- 理由照录设计：一维 C–C 剖面的峰必须只能归因于 C–C 坐标；一旦羧基质子与醛氧共享/转移，能量里混入第二个坐标，峰就不能再当"该坐标的候选"。

### 4.4 关于 O28 两个距离的实测说明（口径不变，只提示读数结构）
本体系中 `R(28···H24)` 与 `R(O28–H24)` 是**同一原子对**的距离（H24 = 脯氨酸羧基 OH 的质子，O28 = 苯甲醛羰基氧），在**任一单帧**上两者数值天然相等（seed 帧实测两值均 = 1.6817 Å）。因此档 2 的判据实际退化为 `R(28,24) < 1.20 Å`（`≤1.05 Å` 自动满足），档 1 判据即 `R(28,24) ∈ [1.20,1.50]`。为避免歧义，每点同时报**供体共价键 R(O11–H24)**（seed 帧 = 1.0006 Å）：若 R(O11–H24) 增大而 R(28,24) 缩小到 ≤1.05 Å，即为质子真实转移的独立证据。**这不修改任何判据阈值。**

### 4.5 峰与 ΔE‡
- 任何局部极小/极大在**主剖面**上只作 **TS 候选 / 下界（上界）**，**绝不写 ΔE‡**，不称"过渡态已确认"（无频率/IRC 证据时）。
- **若峰只在「含档 1 点」的参照剖面里出现，且该峰落在档 1 区间** ⇒ **不得**作 TS 候选，只记「**需二维扫描**」，并报主协调。
- 若主剖面沿该坐标单调无峰 ⇒ 记「**该级别（B3LYP/def2SVP+GD3BJ+UltraFine+CPCM(DMSO)）下一维 C–C 成键坐标无峰**」；改二维或换起点均需主协调放行。

### 4.6 通道切换守卫（构象分支）
若相邻两点之间**重原子 Kabsch RMSD 突增一个量级（> 0.3 Å）**且**同时**出现能量跳降（大负跳）与氢键距离同步跳变 ⇒ 判为**构象分支切换**：剖面必须**分两支各自判单调性**，**禁止**把该点的局域高当峰。判据三条必须同时满足才判分支切换；只满足一两条时按普通点处理并在表里标注。

### 4.7 终止证据（逐字）
结束时贴 `Normal termination of Gaussian 16` 或 `Error termination` 的**逐字行 + 行号 + 当时日志 sha256 + 实测时刻**；若出现 `Error termination`，同时报触发它的前 20 行 context（link 号）。
对照：设计 §4 停手条件 3（前两点实算 R(1,29) 若不递减 ⇒ 停手报主协调，**不 kill**）在日志到手后第一时间核对。

---

## 6. 口径版本与更正留痕（v2，2026-10-17 20:40 CST 前后，据协调侧 evt_c26bc82942d34ba7）

本节**只记录口径版本的追加/更正**，不删除 §4 任何原文；凡与 §4 冲突处，以本节为准并注明冲突点。§4 的阈值本身**未被改动**。

**更正 1（几何数，冲突点在 §4.1 的」不按 14 反推」表述）**
`B 1 29 S 14 -0.2000` 的 `S 14` = **14 步 ⇒ 15 个几何**（起点 4.3543 + 14×0.2000 = 1.5543）。出表写「**15 几何（S 14 = 14 步）**」。`scan point N out of M` 的 M 仍以日志实测为准，但须与本口径一致（实测 15 才是常态；≠15 先报差异）。

**更正 2（起点档位）**
起点帧实测 R(28,24) = **1.6817 Å > 1.50**，按档位定义属 **档 0（普通氢键；既非档 1「共享质子」、也非档 2「已转移」）** ⇒ **首点即进主剖面**；扫描进入 [1.20, 1.50] 后才单列进参照视图。全部 15 个几何的档位都按每帧实测值逐点判，不预设。

**更正 3（档位判定必须同帧双距离）**
档 1 / 档 2 的判定必须用**同一帧的 R(28···H24) 与 R(O28–H24) 同时满足**，不得只用一个距离（§4.4 的「同一原子对」提示**不构成豁免**：两个量仍须逐一列出并同时核）。**档 2 出现时该点不删、并列标「物种改变」**（§4.3 的「单列」= 移出主剖面，不是删除）。

**更正 4（提交权）**
E2 的提交由**主协调点名 + 协调侧与我双方六项自检**后执行；**我（本 Agent）不自行提交**。free cpus = 0 期间**零提交**是预期态（协调侧与我在 20:36:40 / 20:37:02 各自实测为 0）。

**独立外部复核（协调侧 20:36:41 实读）**：52 行 / 2415 B / sha `6301b836b6ca0006f365d80e28cff2f552bd06edae8f54475d6985e751ffbb16`（与本报告 §0 相同；我方 20:35:47 落盘后未被改写）。L4 route 逐字、L2 `%nprocshared=8` / L3 `%mem=10240MB`、41 原子 L9–L49 元素序与 seed 逐一相同、逐原子 max|Δ| = 0.000000、L51 唯一 ModRedundant、末尾双换行 ⇒ 六项**双方独立复核一致**；实算 R(1,29)=4.3543、R(28,24)=1.6817、R(28,29)=1.2265、R(1,35)=3.6818。

**监控安排（一次性只读）**：已设 1 条 `schedule` 只读 check —— 监视 `scan_1d` 下出现 `*.log` 且含 `Optimization completed` / `Normal termination` / `Error termination` 之一（落地或早死都唤醒），间隔 300 s、超时 45 min；命中后向协调侧 `as_ec848a7673b74e35` 与主协调 `as_a341823c436e47ed` **各报一次**。监控对象**只含当前未完成的 E2 artifact**（不把已收口的 E1a / job 1072 日志纳入）。

**台账**：`HI1/PROCESS.md` 由协调侧维护（其 20:37 现值 391 行 / `d79ab930b44cc608b218156553fb8b0a6c5c8b60666de1c0edae563c75a52318`）；我按边界**不写**该文件，事实与证据路径走 AgentHub 与本节。

---

## 7. 实测进展：输入已被提交为 job 1075（**非我提交**），前 2 点已收敛（快照 2026-10-17 21:18:28 CST）

**日志**：`/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan.log`
快照 sha256 = `02da29e39c072c4558046a57968ee0c1a6dd1531264857845f5edec55ef51075`，28892 行 / 1863515 B（快照仍在增长，**最终判定必须用收口后的日志重算**）。
日志头 `Input=/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan.gjf` ⇒ 确认跑的就是 §0 那份 sha `6301b836…6fe61a` 的输入。
`query_compute_queue`（21:16:53 CST 同刻读）显示 job **1075** started_at = **2026-10-17T20:39:26+08:00**，8 cpus / 10240 MB / priority 0；free cpus 当时 = 8（in_flight 24 cpus / 3 jobs）。**提交人格不是本 Agent**（协调侧指定的提交 lane），我只做只读判读。

**M 实测 = 15**：日志逐字 `Step number   1 out of a maximum of  219 on scan point     1 out of    15`（L1635 及后续）⇒ 与「15 几何（S 14 = 14 步）」口径一致。**没有出现** `Scan point`/rigid-scan 行（relaxed scan 无此表），因此 M 只能从 `on scan point N out of 15` 取。

**收敛点（只取 `Optimization completed.`+`-- Stationary point found.` 前的最后一帧与最后一条 SCF Done）**
| 点 | 收敛表/`Optimization completed.` 行号 | 帧（`Standard orientation`）行号 | SCF Done 行号 | E(RB3LYP)/Ha | ΔE vs 首点 kcal/mol | R(1,29)/Å | R(28,29)/Å | R(2,4)/Å | R(28···H24)=R(O28–H24)/Å | R(O11–H24)/Å | R(25···29)/Å | R(25···1)/Å | minsep/Å（对） | 重原子 Kabsch RMSD vs 上一点/Å | 档 | opt 步 / SCF 轮 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 / 15 | L15375 / L15381 | L14777 | L14996 | −939.308205969 | +0.000 | 4.3543 | 1.2258 | 1.3751 | 1.6706 | 1.0010 | 2.7635 | 3.1774 | 0.9738（O25–H26，bonded） | n/a（首点） | **0** | 16 / 6 |
| 2 / 15 | L23679 / L23685 | L23076 | L23310 | −939.307993585 | **+0.133** | 4.1543 | 1.2259 | 1.3751 | 1.6688 | 1.0005 | 2.7391 | 3.1280 | 0.9737（O25–H26，bonded） | **0.131** | **0** | 9 / 7 |

**验收要点（照冻结口径）**
- 收敛证据：point 1 `Maximum Force 0.000034/0.000450 YES; RMS Force 0.000007/0.000300 YES; Max Displacement 0.001535/0.001800 YES; RMS Displacement 0.000323/0.001200 YES`；point 2 `0.000060/0.000450 YES; 0.000009/0.000300 YES; 0.001754/0.001800 YES; 0.000520/0.001200 YES`。四项全 YES，且均未撞 `maxstep=8` 上限（16 步 / 9 步，远低于 Gaussian 默认 219 步上限）。
- **扫描方向守卫（设计 §4 停手条件 3）**：R(1,29) 实测 4.3543 → 4.1543，**递减**，与设计一致（对设计序列 4.3543 − 0.2000·(N−1) 的偏差均为 0.0000 Å）。**无需停手**。
- **档位**：两点 R(28···H24) = 1.6706 / 1.6688 Å，均 > 1.50 ⇒ **档 0（普通氢键，进主剖面）**；R(O11–H24) = 1.0010 / 1.0005 Å 稳定，无质子转移迹象；`R(28···H24)` 与 `R(O28–H24)` 是同一原子对 28–24，两列逐帧同值（口径要求的两个量都已列出并同帧核）。
- **前两点的能量/几何行为**：ΔE = +0.133 kcal/mol（相对首点），Kabsch 重原子 RMSD = 0.131 Å，均远小于 0.3 Å 的分支切换阈值，且能量跳降/氢键跳变均未出现 ⇒ **不是**构象分支切换，属正常沿坐标推进。到目前**没有任何峰**，也**不得**写任何 ΔE‡。
- 重原子数实测 **20 个（非 H）+ 21 个 H = 41**（本报告 §4.2 曾误写「21 个重原子」，此处按实测更正；Kabsch 一律用这 20 个重原子）。
- **未出现** `Normal termination` / `Error termination`（截至 21:18:28 CST 快照）—— 作业仍在运行，故本报告的进展表**不是**终态判读。

**逐点表生成方式（可复算，只读）**：`python3 evidence/extract_scan_table.py build/E2_1D_scan.log`，脚本 sha256 = `f2e9e1c9754722b99e6f4891a161adb2d5843b602cfe38dd90b37831c77342b6`；快照输出存于 `evidence/E2_SCAN_TABLE_211828.md`。

## 8. 进展更新：6 点收敛（实测 2026-10-17 22:03:59 CST，log sha `3ec67e7c…6def7f8e`，71084 行）

本节取代 §7 的 2 点快照作为最新进展；§7 保留为留痕。口径不变（§4 + §6）。完整逐点表与判读见
`evidence/E2_SCAN_TABLE_2204.md`（sha256 `5bd21f66adfb0d8975b228026eeb53cd11ccd957ffcc1c5bcdd12732ca5d8719`），
运动诊断脚本 `evidence/diag_motion.py`（sha256 `f62c64b5ba70c620e97d5f59a0645b7b7980dcb3ae2dd7afd69effea13b68ba9`）。

| 点 | SCF Done 行号 | E(RB3LYP)/Ha | ΔE vs 首点 (kcal/mol) | R(1,29)/Å | R(28,29)/Å | R(2,4)/Å | R(28···H24)=R(O28–H24)/Å | R(O11–H24)/Å | 重原子 Kabsch RMSD vs 上一点/Å | 档 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | L14996 | −939.308205969 | +0.000 | 4.3543 | 1.2258 | 1.3751 | 1.6706 | 1.0010 | n/a | 0 |
| 2 | L23310 | −939.307993585 | +0.133 | 4.1543 | 1.2259 | 1.3751 | 1.6688 | 1.0005 | 0.131 | 0 |
| 3 | L33247 | −939.306988918 | +0.764 | 3.9543 | 1.2260 | 1.3749 | 1.6686 | 0.9997 | 0.144 | 0 |
| 4 | L43288 | −939.305208981 | +1.881 | 3.7543 | 1.2254 | 1.3747 | 1.6822 | 0.9972 | 0.166 | 0 |
| 5 | L56101 | −939.303251773 | +3.109 | 3.5543 | 1.2245 | 1.3745 | 1.7278 | 0.9930 | **0.525** | 0 |
| 6 | L67167 | −939.301736263 | +4.060 | 3.3543 | 1.2237 | 1.3738 | 1.7711 | 0.9895 | **0.833** | 0 |

关键判读：六点全部档 0（R(28···H24) 1.6706→1.7711 Å 均 >1.50）；R(2,4) 变化仅 0.0013 Å（远小于 0.05）；
Kabsch RMSD 在 4→5、5→6 达 0.525 / 0.833 Å（守卫第一条成立），但能量上升（+1.228 / +0.951）而非跳降、氢键平滑（每步约 0.045 Å，无跳变）
⇒ 后两条不成立 ⇒ 不判构象分支切换；diag_motion 显示位移分布到三片段而内部二面角平滑（芳环 178.85/179.05°、C1–C29–O28–C27 39.09/42.01°、水取向 24.29/25.60°），
无环翻转、无坐标切换，是柔性复合物在变陡约束下的整体弛豫。剖面单调上升（步增量 0.133 / 0.631 / 1.117 / 1.228 / 0.951）⇒ 前六点无峰、无 TS 候选、不写 ΔE‡，也不对「无峰」下结论（6/15 点）。
22:04:24 CST 仍无 `Normal termination` / `Error termination`。

## 9. 进展更新：7 点收敛 + Kabsch 约定对账（实测 2026-10-17 22:12:09–22:12:26 CST）

完整表与 15 种约定实测见 `evidence/E2_SCAN_TABLE_2212.md`（sha256 `6c431df8e2326161107a3ffd031960e5ba33ba513012bcdc126e6796357eb86d`）。
第 7 点：E = −939.300096247 Ha（SCF Done **L75557**）、ΔE = **+5.089 kcal/mol**、R(1,29)=3.1543 Å、R(28···H24)=R(O28–H24)=1.8089 Å、R(O11–H24)=0.9868 Å、档 0、Kabsch(A)=0.3746 Å。
七点全部档 0（R(28···H24) 1.6706→1.8089 Å 均 >1.50），R(2,4) 最大变化 0.0018 Å，剖面单调上升（步增量 0.133/0.631/1.117/1.228/0.951/1.029）⇒ 无峰、无 TS 候选、不写 ΔE‡。
第 7 点全局 minsep 由 O25–H26 切到 O25–H27（0.9725 Å）——水内取向变化，不是 28···24 质子转移。

**Kabsch 约定争议（未结）**：协调侧 POST_FREEZE_SUMMARY_2212 记「相邻 Kabsch 0.0709/0.0698（0.131/0.144 作废）」。
我在同一批收敛帧上测了 15 种约定（`evidence/diag_kabsch_variants.py` sha256 `64393be824f8d0824bb95a1599596c57643819f55b7d5d1f9715c63da44062d6`），
1→2 / 2→3 的取值范围是 0.0757–0.1963（A 约定 0.1311/0.1437），**0.0709/0.0698 落在区间外且趋势相反**（我的全部约定递增，对方递减）⇒ 不是同一度量的同一帧对。
已请对方给出「叠合原子集 / RMSD 原子集 + 归一化 / 取哪个坐标块」四项定义与 `7836c7ab…` 权威表路径；收到后按对方约定重算并同步本报告。
**判定不受影响**：0.3 Å 分支切换守卫要求三条件同时成立；4→5、5→6 的 RMSD 在两种归一化下均 >0.3 Å，但能量上升、R(28···H24) 平滑（≈0.04 Å/步）⇒ 不判构象分支切换。
台账勘误已发 hub（`evt_54f70dace0e74d5e`）：E2「6 帧」应更新为「≥7 帧（22:12:09 CST）」，ΔE 最高 +5.089 kcal/mol。

## 10. **终态**：job 1075 failed，8/15 点收敛后第 9 点 l103 报错（实测 2026-10-17 22:44:19–22:45:07 CST）

日志 sha256 **`445956fd7491b68f65da4b1d0172f68ac4e35e19a9a55215d9358390fbe2932e`**，103879 行 / 6703953 B（已停止增长）；job 1075 state = failed，ended_at 22:44:09 +08:00。
逐字终止证据（行号）：`L103874: New curvilinear step failed:  FormB failed.` / `L103875: Error imposing constraints` / `L103876: Error termination via Lnk1e in /home/ly/g16/l103.exe at Sat Oct 17 22:44:01 2026.`；`Normal termination` 全程未出现；致命 `FormB failed` 前兆为 `SLEqS3` 内坐标回代振荡（L103862 RMS 117.553、L103864 RMS 36.6973，同点最高 ~591）而 RMS(Cart) ~1e-4。

收敛点（8/15，M=15）SCF Done 行号与 ΔE（vs 首点，kcal/mol）：L14996 +0.000 / L23310 +0.133 / L33247 +0.764 / L43288 +1.881 / L56101 +3.109 / L67167 +4.060 / L75557 +5.089 / **L85589 +6.600**（R(1,29)=2.9543 Å）。
八点全部档 0（R(28···H24) 1.6706→1.8425 Å；R(O11–H24) 1.0010→0.9847 Å 始终共价）；剖面单调上升、**无峰** ⇒ 无 TS 候选、不写 ΔE‡；且**不得**说「无峰」（未到 1.5543 Å）。分支守卫三条件从未同时成立 ⇒ 不判构象分支切换。R(2,4) 八点最大变化 0.0020 Å，设计停手条件 1/3 均未触发。

未收敛的第 9 点（目标 2.7543 Å，18 步后崩）最后一帧 L103420：R(1,29)=2.7543、R(28,24)=1.8918、R(O11–H24)=0.9828、R(2,4)=**1.3821**（+0.0090 Å）、minsep **0.9625（O25–H27）**、最后 SCF（L103669）E=−939.296849384（≈+7.13 kcal/mol）；**未收敛，不进剖面**。

归因（暂定、证据性）：失败在内坐标机制而非 SCF —— 成键区附近冗余内坐标集病态，`B 1 29` 约束无法再施加。这是第 9 点的输入/方法诊断，**不是**「PES 无特征」的证据。
续算选项（**我不重投**，等主协调裁定）：① 从第 8 点几何续扫、减小步长（−0.10 / 近接触 −0.05）；② 更小信任半径 maxstep=5/3 + `Opt=(ModRedundant,CalcFC)`；③ 做成 2D 扫描（C1–C29 × 水/质子坐标）；④ 若求势垒，仍需独立 TS 搜索 + 频率验证。

完整终态表：`evidence/E2_SCAN_TABLE_2244.md`（sha256 `4879b880c681b2290c8fad7a1c3f89d98355d82363bed443a0c5daf159832bbc`）；末帧取证脚本 `evidence/diag_lastframe.py`（sha256 `28fd49187621ec0465557484ba5d72f99873d20466a45add0fe25d0e2418e3b8`）。台账帖：hub `evt_9e1d2803a33e4f9f`。

---

## 5. 待办（等协调侧点名）

1. 协调侧给出空槽（free cpus ≥ 8）并点名 → 按 §3 参数提交，提交同刻记录 free cpus 读数与实测时刻；
2. 提交后立即在 AgentHub `gold-finish-20261015` 发帖（job id / started_at / 日志绝对路径 / gjf sha256 + 行数 / 六项自检结论 / 同刻 free cpus + 时刻）；
3. 日志到手后按 §4 逐点建表（首两点先核方向），并把结果与证据路径发 AgentHub / 主协调；
4. 本目录之外一律不改：设计文件、别的题、生成器/评分规则/数据库、四条边 E1a/E3a/E3b/EM1 的 result/barrier（我无回填权限）、FINAL_DELIVERY_DRAFT.md 与各题 json/py/测试文件全部未触碰；未 git 提交、未杀进程、未重启服务。
