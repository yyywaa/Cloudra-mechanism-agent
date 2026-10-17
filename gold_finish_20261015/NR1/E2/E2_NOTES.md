# NR1_E2 笔记（结论/证据/待裁决）

> 本文件随计算推进更新。所有能量只能来自**本道同一批 Gaussian 16** 原生日志；不得与旧 ORCA/Gaussian 数值混减；ΔE‡ 为纯电子能差（无 ZPE/热校正），相对本步自身起点极小值。

## 0 目标与口径
- 边：NR1_E2 = NR1_I1 → NR1_I2，bond_changes break [[4,6]]（C4–O6 断裂），form []。
- 体系：气相、q=+1、m=1、26 原子 C6H17O3（频哪醇 C6H14O2 + H3O+）。
- 正式级别：Gaussian 16 `/home/ly/g16/g16`，B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight（无 SCRF）。
- 起点 I1 = `O.CC(C)(O)C(C)(C)[OH2+]`（质子化频哪醇＋水，质子必须落在离去氧 O6 上）；产物 I2 = `O.O.C[C+](C)C(C)(C)O`（叔碳正离子＋2 H2O）。
- 本道全原子映射与原子序对照表见 `E2_PREP_PROVENANCE.md` §3/§4；反应坐标 (row5,row7) = 题面 (map4,map6)。

## 1 竞争假设
- **E2a（有独立鞍点）**：I1 → I2 存在一阶鞍点（C4–O6 拉伸为主），ΔE‡ > 0。
- **E2b（无独立鞍点/与 E3 耦合）**：C4–O6 异裂无内部峰（或起点本身坍缩/产物不是极小值），需交扫描原始证据 + E2/E3 合并裁决问题。
- **风险 R1（起点坍缩）**：I1 优化后质子回到旁观水 → 得 R 复合物（E1 声明起点），则 E2 起点不成立。

## 2 准备结果（非 QM，详见 E2_PREP_PROVENANCE.md）
- I1 候选 3 个（MMFF 4.4385/4.4385/4.5857 kcal）；conformer_search 复核 3 簇（rel 0.000/0.234/4.544 kcal，Boltzmann 59.7/40.3/0.0%）→ 低能取向 ≥2 个。
- I2 候选 9 个（MMFF −22.01 … −17.23 kcal），C+ sp2 身份明确。
- TS 初猜：刚性拉伸 1.8/2.2/2.6 Å（局限已记录）+ IDPP 12 帧（C4–O6 1.4261→4.6140 Å 单调）。

## 3 QM 记录
### 3.1 job 911 · E2 起点 I1 无约束 Opt+Freq
- 输入：`logs/E2_I1_optfreq_c000.gjf.tmp`（源几何 structures/build_I1/assembly/complex_candidate_000.xyz，sha256 b5e3d673e9a6c5f190f074cde41232d14abf3ee655b756afffbe42acf95ac186）
- 状态：**已提交，未终态**（提交时 state=ready，节点 node-local，12 cpus / 13312 MB）
- 待核验：normal termination、opt converged、虚频数=0、O6–H 归属、片段数=2、r(C4–O6) 优化值（供扫描 scan_start 用）

## 4 缺测 / 已证伪 / 待裁决
- 缺测（截至现在）：TS 及其虚频证据、IRC 双向端点、I1/I2 的 DFT 极小值能量、ΔE‡。**不填 0、不编造**。
- 已证伪：暂无。
- 待裁决：①题面正文 21 原子产物示意 vs 题图/registry 26 原子节点（是否守恒）；②若最终无独立鞍点，E2 是否与 E3 合并。

## 5 裁决记录（主协调 as_53d43419a24c485b，2026-10-15）

- **裁决 A（我提出的问题③ · E2 产物原子数）**：按 **26 原子**做，正确，无需改图。理由（主协调）：题源 `ru.py` R1 steps[1].out = `[OH2:1].[OH:6][H:2].[CH3:3][C+:4]([CH3:5])[C:7]...[O:10][H:11]` = 水(O1)+水(O6/H2)+叔碳正离子(C6H13O+) = 26 原子；`NR1.json` 的 `NR1_I2` 节点 smiles `O.O.C[C+](C)C(C)(C)O` 同为 26 原子；与 E1 产物（质子化频哪醇＋水）原子数守恒一致。题面正文那句 `O.C[C+](C)C(C)(C)O` 只是**净反应式/示意**（整体反应物 `[OH3+].CC(C)(O)C(C)(C)O` → 整体产物 `[OH3+].CC(=O)C(C)(C)C.O`），不是中间体节点定义。→ 本道按 26 原子推进，不提案改图。
- **裁决 B（风险① 质子归属/起点坍缩）**：处理方式正确。I1 Opt/Freq 后必须显式核验 O6–H 与 O1–H 归属；若质子回到水侧导致坍缩，那是 H3 的原始证据（记录起点/终点/步数/能量/末帧距离），并把它作为"待裁决问题"上报，**不自行改图**。
- **裁决 C**：ISO/编号独立建结构正确；ts_prepare 用 scan 沿 d(C4–O6) 且 scan_start 取优化后实测值正确；provided/端点 seed 的 `evidence_refs` 必须是**已存在的真实文件路径**。
- **裁决 D（资源）**：本包合计 ≤2 个运行中作业（当前 903/906 属 E1 道）；job 911 排队属正常，不重复提交、不调 priority。
- **裁决 E（无鞍点时的交付口径）**：交"**无约束**优化 + 原生弛豫扫描"的数值证据 + "是否与 E3 合并 / 是否记为无垒"的裁决问题 + 建议值（作为裁决请求，不自行回填、绝不填 0）。

### 3.1a ⚠️ job 911 失败（技术性，非科学失败）—— 已定位并已修好输入
- 原生日志：`/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NR1/E2/logs/E2_I1_optfreq_c000.gjf.log`
  sha256 = `7fe675d584560ba11bb72453aa5168f88b0e03f7916ddb99ef523ebf1a208ea0`（87 行，**无 "Normal termination"**，未做任何 SCF）。
- 原始行（file:line）：
  - L81 `%chk=gold_finish_20261015/NR1/E2/logs/E2_I1_optfreq_c000.chk`
  - L85 `fname=gold_finish_20261015/NR1/E2/logs/E2_I1_optfreq_c000.chk fd = -1`
  - L87 `open-new-file`
  - 计算器侧记录：`calculator 退出码 1；%mem=13GB | fname=...chk fd = -1 | open-new-file`（job 911 state=failed）
- **诊断**：作业的工作目录 = 输入文件所在目录（日志显示 `Input=/home/ly/.../E2/logs/E2_I1_optfreq_c000.gjf.tmp`，CWD = `.../E2/logs/`）。`qm_input_writer` 把我给的**绝对** `chk_name` 渲染成了**相对路径**，该相对路径只在工作根目录下成立；以 logs/ 为 CWD 时目录不存在 → Gaussian 在 Link 0 打开 chk 失败并退出，**没有进入任何计算**。这不是 SCF/化学/资源问题。
- **修复**：新输入 `logs/E2_I1_optfreq_c000_r2.gjf`（8c/10GB，sha256 `359e83717722c4adf5c95b2941105a194da3f80cd1fae0ad19de2b8922950484`），`%chk` 改为**裸文件名** `E2_I1_optfreq_c000_r2.chk`（相对 CWD=logs/ → 有效）。方法/几何/电荷自旋与 911 相同。
- 状态：**修好但尚未提交**（平台故障期暂停提交，等主协调宣布恢复）。旧失败日志保留不改写。
- 同类风险提示（已发 hub）：任何 `chk_name/fchk_name` 都不要给绝对路径；给裸文件名，或干脆省略。


### 3.1b ✅ job 915 · E2 起点 I1 无约束 Opt+Freq = **已确认 0 虚频极小值**（起点身份通过）
- 输入：`logs/E2_I1_optfreq_c000_r2.gjf`（8c/10GB，sha256 359e83717722c4adf5c95b2941105a194da3f80cd1fae0ad19de2b8922950484；`%chk` 裸文件名）
- 原生日志：`/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NR1/E2/logs/E2_I1_optfreq_c000_r2.log`
  sha256 = `c8db123fce61fc35f1e668f8a2d328b46f9673630e58ca6f1058d2c0e01dacaf`
- 原生判据：`normal_termination=true`、`opt_converged=true`、job_types=[opt, freq]；**72 个实频、虚频 0 个**（3N−6=72），最低频 23.2523 cm⁻¹（`Frequencies --` 首行 = file:line **logs/E2_I1_optfreq_c000_r2.log:19194**，共 24 个 Frequencies 行）。
- 能量（原始行，file:line）：**logs/E2_I1_optfreq_c000_r2.log:18766 `SCF Done:  E(RB3LYP) =  -463.999955035     A.U.`**（优化末次 17421 行同值 −463.999955035；第一次 16866 行 −463.999955028）。
  → **E(I1 极小值) = −463.999955035 Hartree**（纯电子能，同批 Gaussian 16 B3LYP-D3BJ/def2SVP 气相）。
- 优化后末帧几何（format_converter log→xyz 第 29 帧）：`structures/I1_opt_c000_r2.xyz` sha256 `34ed0b5daec97d1d061badbc7981fd4061fee771b5cc9837f0aacbe03fbd2257`。
- 身份/几何核验（internal_coordinates analyze, charge=+1）：C6H17O3、26 原子、24 键、**2 片段**、总电荷 +1；
  **r(C4–O6) = 1.544 Å**（row5–row7，氧鎓 C–O）；
  **质子归属：H18 在 O6(row7) 上（r(O7–H18) = 1.046 Å），到 O1(row1) 距离 1.451 Å**；另一 H19 是 O6 自身 H（r=0.974 Å，到 O1 2.924 Å）；r(O1···O7) = 2.494 Å。
  → **质子仍留在离去氧 O6 一侧 → 起点未坍缩成 R（H3 风险未发生）；I1 是真实极小值。**
- **独立交叉印证**：与 10-05 只读证据里旧作业 112（另一程序）的末帧数值几乎逐项一致（O1–H 1.452 / O6–H 1.0465 / O1···O6 2.494 Å vs 本道 1.451 / 1.046 / 2.494 Å）→ 同一物种、同一极小型式，跨程序一致（能量本身不混减）。
- 供后续使用的关键量：**ts_prepare 的 scan_start（d(C4–O6)）= 1.544 Å**。


### 3.2 ✅ job 916 · E2 产物 I2 无约束 Opt+Freq = **已确认 0 虚频极小值**
- 输入 `logs/E2_I2_optfreq_c000_r2.gjf`（8c/10GB，裸 %chk，sha256 4c34f863283ace75b6c7c11828a2283d093506d4fbb1dc41987cd17413c2bea0）
- 原生日志：`/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NR1/E2/logs/E2_I2_optfreq_c000_r2.log`
  sha256 = `e89f464f0712f44ea7e5520d0052a5b9b8a2b8cde86e1bbcb0cfc0dd8e828eee`
- 判据：normal_termination=true、opt_converged=true、**0 虚频**（72 实频，最低 33.9981 cm⁻¹，`Frequencies --` 首行 = 该日志:29057）
- 能量原始行（file:line）：**该日志:27292 `SCF Done:  E(RB3LYP) =  -463.981552572     A.U.`**（freq 段 28626 同值）→ **E(I2) = −463.981552572 Hartree**
- 身份（internal_coordinates analyze, charge=+1）：C6H17O3、26 原子、23 键、**3 片段**、+1；
  C8(=题面 map4, C4+) 三个键角 119.4 / 120.9 / 119.7°（sp2 叔碳正离子）；
  **r(C4···O6) = r(C8–O4) = 4.035 Å**（E2 产物判据 ≥2.6 Å 通过）；附带 r(C8–O13)=2.413 Å（分子内 C+···OH 接触，几何正常）。
- 末帧 xyz：`structures/I2_opt_c000_r2.xyz` sha256 `555f5f49ad73558433f37e39b7a6d43aaec010fb808e923636e32df746139696`
- **同批纯电子能差（供参考，非能垒）**：E(I2) − E(I1) = −463.981552572 − (−463.999955035) = **+0.018402463 Ha = +11.55 kcal/mol** → 气相异裂成离子对吸热。若 C4–O6 存在鞍点，ΔE‡ 必 ≥ 约 11.5 kcal/mol（否则 TS 不可能连通 I2）。

### 3.3 job 917 · C4–O6 弛豫扫描（探索层，判"内部峰 vs 单调"）
- 输入：`logs/E2_scan_C4O6.gjf`（8c/10GB，sha256 `1ed02fd7158ddce840fe5b6f2c8a08736abd0c3c2b80b3fe3af8c7ee6c83e70c`）
  `opt=(modredundant,maxstep=10) b3lyp/def2svp empiricaldispersion=gd3bj scf=tight int=ultrafine`；`B 5 7 S 13 0.181231`；起点 = I1 优化几何（r(C4–O6)=1.544 Å，原始值），终点 3.900 Å，共 14 点；title 里写了 `smiles: O.CC(C)(O)C(C)(C)[OH2+]`（提交前写入，非事后追加）。
- 说明：扫描放在 ts_prepare **之外**是为了用我自己的几何行序避免坐标基错位；扫描只作判据，**TS/IRC 仍只走 ts_prepare**。
- 状态：已提交（job 917，state=ready），未终态。


### 3.3a job 917 逐点权威表（13/14 点已收敛；pt14 未终态）

点分界判据：Gaussian 松弛扫描每收敛一个点会打印 `Optimization completed. / -- Stationary point found.`（本日志 file:line = 1778, 19393, 22857, 28830, 32697, 38276, 45552, 54038, 57898, 61746, 65639, 69960, 74707）。**一个点的能量 = 该分界线之前最后一个 `SCF Done` 行**（点内每次 Berny 步都打印 SCF Done，所以按 "Berny optimization." 分块会把"步"当"点"）。
参考态 E(I1 极小值) = −463.999955035 Ha（E2_I1_optfreq_c000_r2.log:18766）。

| pt | r(C4–O6) (Å) | 末步 SCF Done (Ha) + file:line（E2_scan_C4O6.log） | Δ vs 上一点 (kcal/mol) | 相对 I1 (kcal/mol) |
| --- | --- | --- | --- | --- |
| 1 | 1.5440 | −463.999955036 @1556 | — | 0.00 |
| 2 | 1.7252 | −463.995461789 @19158 | +2.82 | +2.82 |
| 3 | 1.9064 | −463.988453724 @22633 | +4.40 | +7.22 |
| 4 | 2.0876 | −463.982890277 @28602 | +3.49 | +10.71 |
| 5 | 2.2689 | −463.978089300 @32470 | +3.01 | +13.72 |
| 6 | 2.4501 | −463.974694375 @38044 | +2.13 | +15.85 |
| **7** | **2.6313** | **−463.974050154 @45321** | **+0.40** | **+16.26 ← 内部极大** |
| 8 | 2.8125 | −463.975475554 @53805 | −0.89 | +15.36 |
| 9 | 2.9938 | −463.975756168 @57669 | −0.18 | +15.19 |
| 10 | 3.1750 | −463.975127683 @61516 | +0.39 | +15.58 |
| 11 | 3.3562 | −463.974083180 @65412 | +0.66 | +16.23 |
| 12 | 3.5374 | −463.973198234 @69731 | +0.56 | +16.79 |
| 13 | 3.7186 | −463.972591463 @74470 | +0.38 | +17.17 |
| 14 | 3.8998 | (未收敛，末次 SCF ≈ −463.97210) | (~+0.38) | (≈ +17.5) |

**判据回答：存在"内部极大（先升后降）"= 是**，位置 r≈2.63 Å（pt7，+16.26 kcal/mol），其后 pt8/pt9 明确下降（+15.36/+15.19），r>3.0 又回升。
**与主协调粗读的差异**：−463.992913809 / −463.995461789 / −463.982890277 分别是 **pt2 的第一步 / pt2 收敛点 / pt4 收敛点**，不是 pt1/pt2/pt3；pt1 = −463.999955036（= I1 极小值本身，扫描起点即已优化几何）。
**交叉校验（重要）**：扫描在 r=3.72–3.90 为 +17.2…+17.5 kcal/mol，而**无约束优化的 I2 极小值在 r=4.035 Å 只有 +11.55 kcal/mol** → 1D 约束面在大 r 侧不是通向 I2 极小值的那条松弛路径（需要水取向/位置重排），大 r 侧扫描能量系统性偏高。故"有内部极大"稳健，但**峰的绝对高度与它是否就是通往 I2 的 TS，必须由无约束 OptTS 判定**（scan peak ≠ TS）。


### 3.3b job 917 终态（done）+ 峰帧
- 日志 `logs/E2_scan_C4O6.log`，**终结时 sha256 = c2d093fc91b7c0a88246b75e19785cd30fcf7292fe2d6a897deaf80af57aff3c**，normal_termination=true；14 点，扫描坐标序列 1.54446→3.90046 Å（每步 0.18123 Å）。
- log_parser 报 `scan_has_internal_peak=true`，scan_peak = point 7（pt7，+16.26 kcal/mol 相对首点）。ts_guess scan_parse 给出唯一内部候选帧 = frame 6 (point 7)，落盘 `seeds/scan917_peak.xyz`（sha256 60ab2f2c978e04dcda41625e41603598c832588f929a5af45d30755e38030315）。
- scan_parse 附注（重要，须在结论里带上）：①frames 1→2 能量跳变 4.40 kcal/mol（中位 0.66）→ 提示可能的谷滑/不连续；②**全局能量最大在扫描边界（frame 13, r=3.719 Å）**，故"内部峰"只是相对候选；③perceived connectivity：frames 1→2 判 C5–O7 "broken"（距离启发式，非真实断键事件）；frames 6→7 判 **C5–O11 "formed"**。
- **峰帧（pt7）几何核验（internal_coordinates analyze，charge=+1）**：26 原子、C6H17O3、**3 片段**（离去水已断开）、+1；
  r(C4–O6)=r(C5–O7)=**2.632 Å**；**r(C4···O10)=r(C5–O11)=1.930 Å**（保留侧 OH 的氧已明显靠近阳离子中心！）；r(O1···O6)=2.731 Å；r(O6–H18)=0.981 / r(O6–H19)=0.966 Å（离去水仍持两个 H，即中性水）；C4+ 键角 117.6/120.1/122.3°（近 sp2）。
  → **该"峰"不是纯 C4–O6 断裂的干净鞍点**：约束扫描在峰处已把 C4···O10 拉到 1.93 Å，所以正式 OptTS 可能收敛到"C4–O6 断裂 + O10 配位"的耦合鞍点、或滑向极小值。这一点必须由无约束 OptTS + 虚频模式 + 双向 IRC 判定，判不出来就不填数字。

### 3.4 ts_prepare 运行记录（durable 链）
- **run_id = ts_0005**，run_dir = `/home/ly/Cloudra-mechanism-agent/ts/ts_0005`（项目根下，非本道目录）。
- 首次 ts_prepare（status=**blocked**，stage=map，failure_class=input_identity_unconfirmed）：端点绑定不唯一（reactant 4 个、product 8 个对称重原子绑定），needs = conformers.reactant/product.heavy_atom_binding。
  → 用 `ts_resume(run_id="ts_0005", changes={conformers.reactant.heavy_atom_binding.indices=[1,4,5,6,7,8,9,10,11], conformers.product.heavy_atom_binding.indices=[1,4,7,8,9,10,11,12,13]}, reason=…)` 修订（与我用 reaction_mapping 验证过的 concrete binding 完全一致）。receipt rev=6，只改这两个字段。
- 修订后：status=**waiting**，stage=**refine**，**job 933 = ts_opt**（8c/10240MB，输入 `ts/ts_0005/jobs/declaration_0002/ts_opt/refine.gjf`，来自 provided guess = seeds/scan917_peak.xyz）。
- 全部声明：reaction=I1(映射 SMILES)→I2(映射 SMILES)、charge=1、mult=1、atom_map=26 项、reaction_center=[[5,7]]；calculations.formal = gaussian/B3LYP/def2SVP + keywords "empiricaldispersion=gd3bj scf=tight int=ultrafine"（气相，无 SCRF）；conformers = structures/I1_opt_c000_r2.xyz（+build_I1 mol，binding [1,4,5,6,7,8,9,10,11]）与 structures/I2_opt_c000_r2.xyz（+build_I2 mol，binding [1,4,7,8,9,10,11,12,13]）；verification = freq/irc + 两端 endpoint seed（同一 formal profile）；execution = 8 cpus / 10240 MB。
- 参考能：E(I1) = −463.999955035 Ha（915 日志:18766）→ ΔE‡ 的分母/起点。


### 3.5 attempt 1（guess = 917 峰帧）结果：**软鞍点，IRC 积分失败 → 不满足 E2 判据**
- **job 933 ts_opt（done）**：`ts/ts_0005/jobs/declaration_0002/ts_opt/refine.log`，sha256 `72a641896e37d8ea5378cc874cd1959c64337638e9137d52b8d45bb880ac3a66`；route `#p opt=(TS,calcfc,noeigen) B3LYP/def2SVP empiricaldispersion=gd3bj scf=tight int=ultrafine`；normal termination 有、opt_converged=true；末帧能量 **refine.log:3987 SCF Done −463.974034272 Ha**（相对 I1 = **+16.26 kcal/mol**，与 917 扫描峰 +16.26 一致）；末帧几何 structures/TS_ts0005_refine.xyz：r(C4–O6)=2.597 Å、r(C4···O10)=1.961 Å、3 片段、离去水为中性。
- **job 936 frequency（done）**：`.../declaration_0002/frequency/frequency.log`，sha256 `c5b0e878123f74420937b997d5d13520e73ba3421aba30f38b8c052752f241d6`；normal termination 有；E 同 −463.974034272；
  **虚频恰 1 个：−74.5623 cm⁻¹**（`Frequencies --` 行 = 该日志:1010；"1 imaginary frequencies (negative Signs)" = 日志:1001）。
  **但该模为 H 主导的软模**（原始位移块 file:line 1013–1040）：最大位移原子是甲基 H（原子 12 ≈0.40、17 ≈0.40、13 ≈0.34、16 ≈0.33）与离去水 H19（0.35），C4(原子 5) 0.18、O6(原子 7) 0.23；
  log_parser(watch_pairs=[[5,7],[5,11],[7,18],[1,7]]) 报 `heavy_atom_fraction = 0.127`、`top_displaced_pairs = [(12,19,0.586),(7,12,0.506),(5,19,0.461),(15,19,0.454),(17,20,0.450)]`、`watch_pair_fraction = {fraction: 0.0232, pair_projections: {"5-7": 0.384, "5-11": 0.208, "7-18": 0.0001, "1-7": 0.026}}`。
  → **判据结论：(5,7) 是最大的重原子对投影（0.384），但不是最大位移原子对，聚合 watch-pair 占比仅 2.3%** → 按复核道"watch pair 必须是最大位移对且占比 ≥0.30"的口径 **不通过**；这是典型的 loose/soft pseudo-saddle 特征（H 主导 + 极低虚频）。
- **job 941 IRC（failed）**：`.../declaration_0002/irc/irc.log`，sha256 `d57877020625971602fb4d6dda7d1260aa5d0169d3c08e6577683ccc510a8039`（输入 irc.gjf sha256 d5ed1173ce6b2377ad8c62d04644e29c9f9e78a47aadbed2a911876c409f86ef，route `#p irc=calcfc B3LYP/def2SVP ...`）；原生报错（file:line，irc.log）：`WARNING: Bulirsch-Stoer Method is not Converging`、`Delta-x Convergence NOT Met`、`Maximum number of corrector steps exceded.`、`Error termination via Lnk1e in /home/ly/g16/l123.exe`（≈日志:9980）。日志里只有 `Point Number: 0` 与 `Point Number 1 in FORWARD path direction` 两条（日志:1002/1004）→ **没有任何可用双向端点区间证据**。
- **工具面限制（已取证）**：想用更小 IRC 步长重试时，ts_prepare 只能通过 `verification.irc.keywords` 传设置，而工作流路由里已自带 `irc=calcfc`；我用 qm_input_writer 复现了同一生成路径，结果 route 变成 `#p irc=calcfc B3LYP/def2SVP ... irc=(calcfc,stepsize=5)`（**重复 irc 关键字**）→ 声明层无法安全改动 IRC 步长/算法。（证书：logs/_test_irc_A.gjf / _test_irc_B.gjf 与工作流 irc.gjf 同格式。）
- **attempt 2（已提交）**：ts_resume 只改 `guess.xyz_path/evidence_refs` → provided = `seeds/interp_idpp/img_06.xyz`（r(C4–O6)=3.181 Å、C4···O10=2.242 Å、两水均已脱离）→ **job 948 = ts_opt**（declaration_0003；receipt rev=27，前次 933/936/941 保留但被标为 invalidated）；触发理由写清：IRC 积分失败 + attempt 1 鞍点为软模，换结构区域检验是否存在"更干净的"鞍点。
- 备注：所有 IDPP 帧（img_04…img_08）都带 C4···O10 = 2.11–2.32 Å 的接触 → "阳离子被保留侧 OH 稳定"是该离子对区域的固有特征，不是扫描独有的假象。


### 3.6 attempt 2（guess = IDPP img_06）结果：**未收敛，滑落到更低能量的"换水"构型 → 离子对区极平坦**
- **job 948 ts_opt failed**：`ts/ts_0005/jobs/declaration_0003/ts_opt/refine.log`，sha256 `fa7f1f5571106e74210dfb404defb53fd3e670ddab095c4935565a6ee6ff39cd`。
- 原生事实（file:line）：跑到 **`Step number 134 out of a maximum of  134`** → `Optimization stopped.`（**refine.log:84124**）→ `Error termination request processed by link 9999` / `Error termination via Lnk1e in l9999.exe`（:84705/:84706）；**未收敛**（不是 SCF 失败：最后一次 SCF 已收敛，83884 行 `SCF Done: E(RB3LYP) = -464.017399243 A.U.`）。CPU 4 h 4 min / 墙钟 30 min 44 s。
- **末帧几何（format_converter 第 133 帧 → structures/attempt2_last_frame.xyz；internal_coordinates，charge=+1）**：C6H17O3、26 原子、**24 键、2 片段**（＝仍是"质子化频哪醇＋水"这一物种，非新分子）；
  **r(C4–O1) = 1.498 Å（新成键！）**、r(C4–O6) = 3.230 Å（原反应坐标键已断）、r(C7–O10) = 1.465 Å（未迁移）、r(C7–C8) = 1.527 Å（甲基未迁移）；
  H 键网络：**r(O1···O6) = 2.403 Å、r(O6···O10) = 2.498 Å、r(O1···O10) = 2.899 Å**（水桥接"氧鎓 O1"与"中性 OH O10"形成三中心 H 键网；异常键：O1–H2 1.310 / H2–O7 1.118 elongated；O11–H18 1.532）。
  → **即：从离子对一侧出发，体系没有停在碳正离子上，而是被"另一个水"（O1）捕获，落到比我的 I1 极小值低 10.95 kcal/mol 的构型**（−464.017399243 vs −463.999955035）。该构型在题面映射下 C4–O6 已断，**不是** mapped-I1（mapped-I1 要求 C4–O6 成键、H2 在 O6），属"换水/异构化"产物侧构型。
- 物理解读（证据支持、非推测结论）：**离子对区非常平坦，两个水在 C4 上几乎等价，碳正离子会被任一水迅速捕获**；这也解释了 1D 约束扫描在大 r 侧的"谷滑/多分支"与 attempt 1 鞍点为何是极软模式（−74.6 cm⁻¹、H 主导）。

### 3.7 **E2 终态结论（截至 2026-10-15 20:00）：无合格独立鞍点，ΔE‡ 不填（按 §3.2a）**
判据链逐项：①TS 恰 1 虚频 → 达成（attempt 1，−74.5623 cm⁻¹）；②该虚频模**以 C4–O6 断裂为主** → **未达成**（H 主导，heavy_atom_fraction 0.127，(5,7) 非最大位移对，聚合 watch-pair 占比 0.023）；③双向 IRC 真实到达 I1 与 I2 → **未达成**（job 941 积分失败，无路径）；④两端 Opt/Freq 0 虚频 → 两端极小值本身已由 **job 915/916 独立建立**（−463.999955035 / −463.981552572，均 0 虚频），但**这不构成 E2 的连通性证明**。
→ **因此 E2 不给任何数值。已证伪/已确立的清单见 STATUS.md 与 hub 帖；待裁决问题见下。**

**参考能量汇总（同批 Gaussian 16 / B3LYP-D3BJ/def2SVP / 气相 / q+1 / m1 / 26 原子）**
| 量 | 值 (Hartree) | 原始行 |
| --- | --- | --- |
| E(I1 极小值, 本道 915) | −463.999955035 | logs/E2_I1_optfreq_c000_r2.log:18766 |
| E(I2 极小值, 本道 916) | −463.981552572 | logs/E2_I2_optfreq_c000_r2.log:27292 |
| E(候选软鞍点, 933) | −463.974034272 | ts/ts_0005/jobs/declaration_0002/ts_opt/refine.log:3987（freq 段同值） |
| E(917 扫描峰 pt7) | −463.974050154 | logs/E2_scan_C4O6.log:45321 |
| E(attempt2 末帧, 未收敛) | −464.017399243 | ts/ts_0005/jobs/declaration_0003/ts_opt/refine.log:83884 |
参考差（非能垒）：E(I2)−E(I1) = +11.55 kcal/mol；E(软鞍点)−E(I1) = **+16.26 kcal/mol**（因②③未达成，**不能**作为 ΔE‡ 交付）。


### 3.8 追加：ts_guess(mode="verify") 对候选鞍点虚频模的独立判定（**修正 3.5/3.7 的表述**）
命令：`ts_guess(mode="verify", freq_log=…/declaration_0002/frequency/frequency.log, irc_log=…/declaration_0002/irc/irc.log, watch_pairs=[[5,7]], reactant_path=structures/I1_opt_c000_r2.xyz, product_path=structures/I2_opt_c000_r2.xyz)`
返回：
- `n_imag = 1`，`imag_freqs = [-74.56]`；
- **`imag_mode_aligned = true`** —— 原文：`"Imaginary mode is consistent with the declared reaction coordinate: watch_pairs max relative displacement 0.393 ≥ 0.50×global max 0.701 (max pair=(12,16))"`；check 明细：`"Atom pair (5,7) relative displacement=0.393 (threshold 0.50×0.701=0.350)"`；
- `verdict = inconclusive`，原因：`"IRC 日志缺少 'Summary of reaction path following' 汇总表，无法提取反应坐标与能量"`（即 IRC 失败导致无法取得端点）。
**含义（必须并列陈述，不能只取一方）**：
  1) 按 **工具口径**（watch pair 位移 ≥ 0.50×全局最大对位移）：**(5,7) 通过**（0.393 ≥ 0.350），模与 (5,7) 一致；但全局最大对是 **(12,16) = 同一甲基上两个 H（甲基转动）0.701**。
  2) 按 **复核道口径**（watch pair 必须是最大位移原子对且占比 ≥0.30）：**(5,7) 不是最大位移对**（0.393 < 0.701）→ 不通过。
  → 该鞍点的"模特征"是**边界情形**：确实是极软的 loose 鞍点（−74.6 cm⁻¹，含可观甲基转动成分），C4–O6 拉伸成分显著但不是唯一主成分。**决定性缺口仍是 IRC 连通性**（job 941 积分失败，工具也因缺汇总表无法给端点）。


### 3.9 **917 大 r 侧的真实结构：C4–O10 成键（新物种），扫描并未走向声明的 I2**
- 用 `format_converter(log→xyz)` 取 917 的**最后一个扫描帧**（第 13 帧，r(C4–O6)=3.900 Å）→ `seeds/scan917_last_frame_r390.xyz`（sha256 `749a88b97c45324458c77c1650234e4d83947646d0e74960e8bf30843cd08501`），internal_coordinates(charge=+1) 核验：
  C6H17O3、26 原子、**24 键、3 片段**；r(C4–O6)=**3.900 Å（断）**；**r(C4–O10)=1.551 Å（成键，bond order 1）**；r(O1···O6)=2.815 Å、r(O6–H18)=0.977 Å。
- 解读（有数据支撑）：**917 的 1D 约束面在大 r 侧走的是"C4 被相邻 OH 的 O10 分子内捕获"的另一条谷**（C4–O10 成键 → 环氧化物/氧鎓型物种 + 水），**不是**通往声明的 I2 离子对（I2 极小值：C4···O10 = 4.035 Å、未成键、E = −463.981552572）。这解释了大 r 侧扫描能量（+17.17/+17.5）**高于**真实 I2 极小值（+11.55 kcal/mol）的矛盾。
- 与 attempt 2 的呼应：attempt 2 从产物侧出发时体系被**另一个水 O1** 捕获（C4–O1 = 1.498 Å）。→ 两条独立证据一致指向：**C4–O6 异裂后，阳离子会被邻近的 O 供体（O10 分子内 / O1 分子间）迅速捕获；"自由离子对"在该气相模型里很可能不是一个可及的中间体**。
- 已准备（受平台写锁阻塞，未提交）：从该 3.90 Å 帧做**无约束 Opt+Freq**（`logs/E2_outframe_prod_optfreq.gjf` sha256 `f3ad355957632b9f59c2f28072077b30c2e3dc75998f29d832a428893354909c`，8c/10240MB）作为"产物侧外框优化"连通性测试：落到 I2（−463.981552572）还是落到 C4–O10 成键的新物种。
- 平台记录：23:2x 提交该作业两次均返回 `database is locked`（job_id=−1，无残留记录/无 lock 残留 → 无幻影占位），已上报协调者。


### 3.10 job 964（0.05 Å 细网格 2.632→2.032 Å，13 点）结果：**该窗口内单调下降、无窄垒**
- 日志 `logs/E2_scan_fine_C4O6.log`（normal termination；sha256 `59d77190f6c0c2c087db198f4e568615ebc77eee968975c68d1a551e591e890e`）；输入 `logs/E2_scan_fine_C4O6.gjf` sha256 07f05e66bfe8f2cce3797940e35f446d835701ce47e5b6046b5ec7b35b776939；`B 5 7 S 12 -0.050000`，起点 = 917 峰帧（2.632 Å，与 scan_start 相等）。
- 点分界 = `Optimization completed` 行（file:line = 2982, 10601, 16500, 21998, 25398, 28405, 30991, 34820, 47273, 51123, 53322, 57211, 62843）；每点能量 = 分界前最后一个 `SCF Done`：

| pt | r(C4–O6) Å | 末步 SCF Done (Ha) + file:line | Δ vs 上一点 (kcal/mol) | 相对 I1 |
|---|---|---|---|---|
| 1 | 2.632 | −463.974050240 (log:2759) | — | +16.26 |
| 2 | 2.582 | −463.974036734 (log:10371) | +0.01 | +16.26 |
| 3 | 2.532 | −463.974107555 (log:16271) | −0.04 | +16.22 |
| 4 | 2.482 | −463.974341042 (log:21768) | −0.15 | +16.07 |
| 5 | 2.432 | −463.974770527 (log:25176) | −0.27 | +15.80 |
| 6 | 2.382 | −463.975383358 (log:28180) | −0.38 | +15.42 |
| 7 | 2.332 | −463.976173084 (log:30770) | −0.50 | +14.92 |
| 8 | 2.282 | −463.977127414 (log:34595) | −0.60 | +14.32 |
| 9 | 2.232 | −463.978335773 (log:47039) | −0.76 | +13.57 |
| 10 | 2.182 | −463.979548805 (log:50892) | −0.76 | +12.81 |
| 11 | 2.132 | −463.980852711 (log:53099) | −0.82 | +11.99 |
| 12 | 2.082 | −463.982246049 (log:56977) | −0.87 | +11.11 |
| 13 | 2.032 | −463.983745086 (log:62611) | −0.94 | +10.17 |

- 判据：**单调下降、无内部极大、无肩** → 0.18 Å 网格可能漏掉的窄垒在该窗口被排除。scan_parse 的唯一内部候选 = frame 1（= 917 峰帧本身）。
- 合并 917（1.544→3.900）+ 964（2.632→2.032）：**1.54–3.90 Å 内沿 C4–O6 的约束极大只有一个，r≈2.63 Å、+16.26 kcal/mol**，两侧单调下行。964 的极大能量（−463.974050240）与无约束软鞍点（job 933，−463.974034272）在 ~0.001 kcal/mol 内自洽。
- 964 末帧（2.032 Å）几何：`seeds/scan964_last_frame_r203.xyz`（sha256 54ee76f87cd811a79d4faf5b29f47c63bebd91c1caa6007be7a06aa4c1d86a80）→ 3 片段、23 键、r(C4–O6)=2.032、r(C4–O10)=2.262、r(O6–H)=1.002；已用于"反应物侧外框 Opt+Freq"（`logs/E2_outframe_react_optfreq.gjf` sha256 83d4f16dcc9bba4458508823224dfd77a1e31ab9be305b9d2958cae6a28388f4）。
- 外框连通性测试作业：**job 976**（产物侧，从 917 末帧 3.900 Å / C4–O10 已成键 1.551 Å 出发，`logs/E2_outframe_prod_optfreq.gjf` sha256 f3ad355957632b9f59c2f28072077b30c2e3dc75998f29d832a428893354909c）+ 反应物侧（提交时遇 `database is locked`，稍后重试）。
