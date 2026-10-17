# NI5_E1 · 原生日志证据清单（small_mol as_0093ab74272a41da）

> 规则：这里只记**实际跑出来的原生日志**：绝对路径 + sha256 + job_id + 提交时 cpus/memory_mb + 从日志读到的关键量。
> 原始日志一律不改写；能量取自日志原始行文本。所有输入文件都带 `smiles:` 注释。

## 作业 902 — RC 候选（conformer_search complex candidate 002）无约束 Opt+Freq
- 目的：建立"加成前水接力物种组合"的无约束零虚频极小值（**未通过该目的**，见结论）
- 输入：`/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NI5/rc/job01_rc_optfreq/rc_optfreq_m13.gjf`
  - sha256 = `bdf1f480a7980e555741b35415edff77acd55b51e98803b03099ed10b0c85d4a`
  - 路由：`#p opt freq B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=Water)`
  - 标题（smiles 注释）：`smiles: C=O.CN.O | NI5_E1 relay-water RC (CH2O + CH3NH2 + H2O) unconstrained Opt+Freq`
  - 起点几何：`gold_finish_20261015/NI5/rc/build/assembly/complex_candidate_002.xyz`
    sha256 = `86bb894ce0db87bb315aef92b9b79623d45cb036871661b40082f56b6afbee23`
- 日志：`/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NI5/rc/job01_rc_optfreq/rc_optfreq_m13.log`
  - sha256 = `e82ba58586b95764240844bc3ed60fc9484c63b616a35cf062d46bf0824d4eb9`
- job_id = 902；cpus = 12；memory_mb = 13312（%mem=13GB）；q0/m1；local 后端
- log_parser 关键量：engine=gaussian；job_types=[opt, freq]；normal_termination=true；opt_converged=true；
  frequencies_cm 个数 = 36；**imaginary_frequencies = [] （零虚频）**；scf_energy_hartree = -286.613531375
- 原始行（grep -n 行号）：
  - 18282: ` SCF Done:  E(RB3LYP) =  -286.613531375     A.U. after    7 cycles`
  - 19092: ` SCF Done:  E(RB3LYP) =  -286.613531375     A.U. after    1 cycles`（freq 步）
  - 18442/18443: ` Optimization completed.` / `    -- Stationary point found.`
  - 19376: ` Frequencies --     98.1897               169.5593               204.1019`（36 个频率全为正值；无负号频率行）
  - 18691: ` Sum of Mulliken charges =  -0.00000`
- 优化轨迹（SCF Done 序列，Eh，行号:能量）：597:-286.594525389 … 18282:-286.613531375（共 ~35 步单调下降，约 -11.9 kcal/mol 全程下坡，无上坡步）
- **几何核验（internal_coordinates，optimized frame 由 format_converter log→xyz 导出：rc/job01_rc_optfreq/rc_optfreq_m13_last.xyz）**：
  r(C1–N6)=1.641 Å（已成键）、r(C1–O2)=1.297 Å、r(C1–H3)=1.119、r(C1–H4)=1.122、
  r(O2···H13)=1.597 Å、r(O12–H13)=1.018 Å、r(O12···H10)=1.864 Å、r(N6–O12)=2.775 Å、
  r(N6–C5)=1.472、r(N6–H10)=1.043、r(N6–H11)=1.024；分子式 C2H9NO2，14 原子，2 片段，总电荷 0
- **结论（计算完成 vs 验收通过）**：计算完成（正常终止、收敛、零虚频）**但不满足任务定义的 RC**（要求 C1···N6 > 2.8 Å、水接力桥接、无质子转移）。
  该极小值是 C–N 已成键的两性离子·H2O 加合物（水仍在 O2 与 N–H10 之间接力成氢键），即**加成中间体侧**。
  含义：以 candidate_002（r(C1···N6)=3.150 Å）为起点，B3LYP-D3(BJ)/def2-SVP+CPCM(Water) 上无约束优化**一路下坡成键**，
  该起点不在加成前络合物的盆内（与旧 ORCA 91 "几何朝 C–N 成键滑落"同一现象）。
  这**不能**证明鞍点不存在，只能说明该起点不在 RC 盆内 → 需要 (a) 受约束扫描判定 E(r) 是否存在内部极大、(b) 更远距离/其它水拓扑的加成前组合存在性判定。

## 作业 909 — 加成中间体 [O-]CH2-NH2(+)(H)CH3 · H2O 无约束 Opt+Freq
- 输入：`/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NI5/intermediate/job02_zwitterion_optfreq/zwitterion_optfreq_m13.gjf`
  - 标题：`smiles: C[NH2+]C[O-].O | NI5_E1 C-N addition intermediate [O-]CH2-NH2(+)(H)CH3 + H2O unconstrained Opt+Freq`
  - 起点几何：`gold_finish_20261015/NI5/intermediate/build/assembly/complex_candidate_000.xyz`（smiles_to_mol 3D 构建）
- job_id = 909；cpus = 12；memory_mb = 13312；q0/m1；local 后端；提交时 state=ready（排队中）
- 状态：**待终态**（结果尚未产生，不得先行声明）

## 作业 914 — C1–N6 受约束松弛扫描（外推/解离方向 3.1496 → 5.1496 Å，+0.2 × 10）
- 输入：`/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NI5/ts/scan01_C1N6/scan01_up_C1N6.gjf`
  - sha256 = `db077c996a46f9e186337d5ddb792708fbb612277c0502a7b8f5538f45bcadfd`
  - 由 ts_guess(mode=scan_prepare, engine=gaussian) 生成，随后仅在**提交前**补 `%mem=13GB`、绝对 %chk 路径与 `smiles:` 标题行
  - 路由：`# opt=(modredundant,maxstep=10) B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=Water)`
  - 扫描行：`B 1 6 S 10 0.200000`；起点几何同 candidate_002.xyz（r(C1–N6)=3.1496 Å）
  - 说明：`opt=(modredundant,maxstep=10)` 是 ts_guess 工具生成的扫描输入默认设置，非本执行者自行加的参数；如需可裁决是否改用 Gaussian 默认步长
- job_id = 914；cpus = 12；memory_mb = 13312；q0/m1；local 后端；提交时 state=ready（排队中）
- 状态：**待终态**

## 工具限制记录（供修复/裁决）
- `ts_guess(scan_prepare)` 拒绝 `scan_start != 当前几何值`：
  原文 `start_geometry_mismatch: bond [1, 6]: requested scan_start=4.0 but the current geometry value is 3.1496. A Gaussian modredundant scan starts from the CURRENT geometry value and only applies the increment — generate the target start geometry first (e.g. a constrained optimization to the requested start value) instead of merely adjusting scan_start.`
  → 因此"4.0 Å 起步"的扫描必须先有 r=4.0 的几何。改用两段扫描（均自当前 r=3.1496 起步）覆盖 1.6→5.15 Å。

## 902 优化轨迹逐点表（只读分析；frame 取自 format_converter log→csv，38 帧）
- CSV：`gold_finish_20261015/NI5/rc/job01_rc_optfreq/rc_optfreq_m13_traj.csv`（由 rc_optfreq_m13.log 导出）
- 每帧几何经 internal_coordinates 复核（input_text=该帧 xyz，watch_pairs 同前）：
| frame | E(RB3LYP)/Eh | r(C1–O2)/Å | r(C1···N6)/Å | r(O2···H13)/Å | r(O12–H13)/Å | r(N6–H10)/Å |
|---|---|---|---|---|---|---|
| 0  | -286.594525389 | 1.229 | 3.150 | 1.769 | 0.984 | 1.035 |
| 5  | -286.602705286 | 1.218 | 2.443 | 1.810 | 0.979 | 1.023 |
| 10 | -286.603551563 | 1.233 | 2.166 | 1.850 | 0.977 | 1.025 |
| 15 | -286.606189877 | 1.258 | 1.812 | 1.819 | 0.986 | 1.021 |
| 20 | -286.608754010 | 1.280 | 1.701 | 1.664 | 0.995 | 1.031 |
| 25 | -286.612579883 | 1.290 | 1.674 | 1.597 | 1.014 | 1.036 |
| 30 | -286.613514735 | 1.296 | 1.641 | 1.608 | 1.015 | 1.042 |
| 35 | -286.613531027 | 1.297 | 1.641 | 1.598 | 1.018 | 1.043 |
| 37 | -286.613531375 | 1.297 | 1.641 | 1.597 | 1.018 | 1.043 |
- **判读**：E 与 r(C1–N6) 在整条路径上**同步单调**（E 单调下降、r 单调缩短 3.150→1.641 Å），无任何上坡步；
  该轨迹只能证明"以 candidate_002 为起点、沿这条松弛路径无垒/无内部极大"，**不能**证明 r ≥ 3.15 Å 一侧无峰（那需要 UP 扫描）。

## 已预写、待解禁后按优先级提交的输入（均 8 cpus / 10240 MB，含 smiles: 注释与绝对 %chk）
| 优先级 | 目的 | 输入绝对路径 | 起点几何 provenance |
|---|---|---|---|
| 1 | UP 段扫描（已提交 job 914，排队中） | gold_finish_20261015/NI5/ts/scan01_C1N6/scan01_up_C1N6.gjf (sha256 db077c99…) | candidate_002.xyz |
| 2 | DOWN 段扫描 3.1496→1.6 Å（未提交） | 待生成（ts_guess scan_prepare，同方法/8c） | candidate_002.xyz |
| 3 | 开链拓扑加成前组合（水接胺 N，N–H 直接对羰基 O） | gold_finish_20261015/NI5/rc/job03_cand000/job03_cand000_optfreq.gjf | complex_candidate_000.xyz |
| 4 | 开链拓扑镜像 | gold_finish_20261015/NI5/rc/job04_cand001/job04_cand001_optfreq.gjf | complex_candidate_001.xyz |
| 5 | 水同时捐给羰基 O 与胺 N（N 被占、r(C1···N6)=5.34 Å） | gold_finish_20261015/NI5/rc/job05_cand004/job05_cand004_optfreq.gjf | complex_candidate_004.xyz |
| 6 | 水只在羰基一侧、r(C1···N6)=3.21 Å | gold_finish_20261015/NI5/rc/job06_cand005/job06_cand005_optfreq.gjf | complex_candidate_005.xyz |
| 7 | 水只在羰基一侧、r(C1···N6)=6.72 Å | gold_finish_20261015/NI5/rc/job07_cand006/job07_cand006_optfreq.gjf | complex_candidate_006.xyz |
| 8 | 三分离组分参考（CH2O / CH3NH2 / H2O） | gold_finish_20261015/NI5/seeds/spec_CH2O/spec_CH2O.gjf、spec_CH3NH2/spec_CH3NH2.gjf、spec_H2O/spec_H2O.gjf | smiles_to_mol 3D |
全部**未提交**（平台 compute.db 锁故障期间遵守"暂停提交新的 QM 作业"纪律；仅在解禁后按优先级提交，不重复提交）。

## 平台故障期核查（只读）
- 903 = /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NR1/E1/scan/pt_scan_R_01.gjf（NR1 包）、906 = …/NR1/E1/scan_P/pt_scan_P_01.gjf（NR1 包）→ **非本包**。
- 本包 909（intermediate/job02_zwitterion_optfreq/）与 914（ts/scan01_C1N6/）目录内只有 .gjf、**无 .log** → 从未启动。
- `pgrep -a g16` 在本机返回空（核查时刻无 g16 进程）。

## 902 vs 909 身份对照（2026-10-15，NI5 包独立核验；只读，不改动任何原生日志）

**口径**：两帧几何都取自各自 Opt+Freq 日志的末帧（format_converter log→xyz 导出的坐标 artifact），几何量由坐标直接计算；
能量取日志末条 `SCF Done`（同一批 Gaussian 16、同方法、同 q0/m1、同 CPCM(Water)）。

| 项 | 902（rc/job01_rc_optfreq） | 909（intermediate/job02_zwitterion_optfreq） |
|---|---|---|
| 日志 sha256 | e82ba58586b95764240844bc3ed60fc9484c63b616a35cf062d46bf0824d4eb9 | f50c3b8076584e51345eebbc005d6474d0de8a41717b1d03a141aca0372f9c7a |
| 末条 SCF Done / Eh | -286.613531375 | -286.612267390 |
| 频率数 / 虚频 | 36 / 0（最低 98.19 cm⁻¹） | 36 / **0**（最低 120.86 cm⁻¹） |
| normal termination / opt converged | true / true | true / true |
| 末帧导出 xyz | rc/job01_rc_optfreq/rc_optfreq_m13_last.xyz（sha256 11474dff0e6d18ac3f8fa9fe61b968963f25606367ea7aef7b72cc8666285032） | intermediate/job02_zwitterion_optfreq/zwitterion_optfreq_m13_last.xyz |
| r(C–N) / r(C–O) / r(N–Cme) | 1.641 / 1.297 / 1.472 | 1.638 / 1.295 / 1.470 |
| 质子归属 | 烷氧 O 上无 H；N 上 2 个 H（H10 1.043、H11 1.024） | 同（N 上 2 个 H） |
| 水接力氢键 | O2···H13 1.597、O12–H13 1.018、O12···H10 1.864、O12–H14 0.968；O–H13···Ow 160.3° | O1···H13 1.587、O12–H13 1.020、O12···H8 1.860、O12–H14 0.968；O–H13···Ow 160.6° |
| 重原子关键距离 | C···Cme 2.584、O···Cme 2.962、Cme···Ow 3.544 | C···Cme 2.646、**O···Cme 3.726**、Cme···Ow 3.896 |
| 接力环三距 | C···Ow 2.965 / O···Ow 2.578 / N···Ow 2.775 | C···Ow 2.965 / O···Ow 2.571 / N···Ow 2.779 |
| 骨架二面角 O–C–N–Cme | +63.2° | −173.4° |
| ΔE(902 − 909) | −0.001263985 Eh = **−0.79 kcal/mol（902 更低）** | — |

**结论（只作口径用；不改动任何已有原生日志）**：两者是**同一物种的不同构象**——都是 C–N 已成键的
两性离子·水加合物（烷氧负离子 + 铵 + 1 个完整水，6 元接力氢键环 O⁻···H–O(w)···H–N）；
差异集中在 C1–N6 键轴的**骨架/甲基转动**（O–C–N–Cme 二面角相差 ~123°，O···Cme 相差 0.76 Å），
而接力氢键环三距与水的取向在两位构象中一致到 ≤0.008 Å。**不是镜像**（重原子距阵在 O···Cme 上明显不同）。
→ explorer 的"同一物种另一构象、902 低 0.79 kcal/mol"判断**成立**；902 作 E1 产物/E2 起点，909 不作独立中间体。

## 本轮新提交（2026-10-15，内区扫描关键路径）

- **作业 923 = 内区上行松弛扫描**：输入 `gold_finish_20261015/NI5/ts/scan02_inner_C1N6/scan02_inner_C1N6.gjf`
  sha256 = f6ea803a7935d3017a76356e54dc247b9a6a12e4c46130ad860d5befb54b7444
  （ts_guess scan_prepare 生成，仅补 %mem=10GB 与绝对 %chk、smiles 标题；路由保留工具默认
  `opt=(modredundant,maxstep=10) B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=Water)`；
  扫描行 `B 1 6 S 16 0.099998` = r(C1–N6) 1.6413 → 3.2413 Å，步长 0.1 Å）
  起点几何 = 902 末帧（rc/job01_rc_optfreq/rc_optfreq_m13_last.xyz）；cpus=8 / memory_mb=10240；提交时 state=ready（排队）
- **作业 926 = 分离组分 CH2O**：输入 `gold_finish_20261015/NI5/seeds/spec_CH2O/spec_CH2O.gjf`
  （本轮只把 `%nproc=12/%mem=13GB` 改为 `%nprocshared=8/%mem=10GB` 以符合本包预算；路由/几何/标题未变）
  sha256 = 6cc08f02eea102b7278c1831c98b77465390b647ea00815ad231315d56990bce；cpus=8 / memory_mb=10240；state=ready（排队）
- 同批改了 seeds/spec_CH3NH2（sha256 120ff9440aea154e48e27c76dc1e4a101ea838ecaa208b0831cddd84986f7562）
  与 seeds/spec_H2O（sha256 99dd32dc4fa8cad5ffd84fbca7d80f4dd862eca661ad6184c4fb4256c2e5ffdf）的 %nprocshared/%mem，待提交。
- 修正前文件说明：`## 作业 909` 一节写"待终态"；现已终态并核验（见下）。

## 作业 909 终态核验（补充）
- 日志 `gold_finish_20261015/NI5/intermediate/job02_zwitterion_optfreq/zwitterion_optfreq_m13.log`
  sha256 = f50c3b8076584e51345eebbc005d6474d0de8a41717b1d03a141aca0372f9c7a；
  log_parser：engine=gaussian；job_types=[opt, freq]；normal_termination=true；opt_converged=true；
  36 个频率、imaginary_frequencies=[]（零虚频，最低 120.8575 cm⁻¹）；scf_energy_hartree=-286.612267390。
- 该结果为**加成中间体侧**（C–N 已成键 1.638 Å）的 0 虚频极小值，与 902 同物种不同构象（见上表）。

## 914 逐点复核与口径更正（2026-10-15，NI5 包独立解析）
- 日志 sha256 = 4bca52fa38168c9eab4def118f52c57f44329025faedfbaca3f8a627243eeac9（未改动）
- 解析：`awk '/Step number/{sp=$0} /SCF Done/{e=$5} /Optimization completed/{print NR, e, sp}'`
  取**每个 scan point 收敛时刻的末条 SCF Done**（8 个点均出现 `Optimization completed` + 4 项收敛判据 YES；
  点 9 只在 4.7496 Å 处振荡到 `Number of steps exceeded, NStep= 58`，无收敛点）。
- **口径更正**：协调者给出的"每点末条 SCF Done"数列（p1 -286.605427601 … p8 -286.600071272）实际取到的是
  **上一点收敛之后、下一个 scan point 第一步的 SCF**（例如 -286.605427601 出现在第 10738 行，紧跟第 10772 行
  `Step number 1 … on scan point 2` 之前，属 scan point 2 的未松弛起点），故整条数列**错位一个点**；
  由于位移量随 R 单调变化，错位后看起来"单调升高"。松弛后正确数列如下（r 取自各点收敛时 `R(1,6)` 行）：

| scan point | R(1,6)/Å | 收敛末条 SCF Done/Eh | ΔE vs p1/(kcal·mol⁻¹) | 收敛时 -DE/DX |
|---|---|---|---|---|
| 1 | 3.1496 | -286.605325567 | 0.000 | +0.0024 |
| 2 | 3.3496 | **-286.605703511** | **-0.237** | -0.0003 |
| 3 | 3.5496 | -286.605254172 | +0.045 | -0.0019 |
| 4 | 3.7496 | -286.604385105 | +0.590 | -0.0024 |
| 5 | 3.9496 | -286.603372588 | +1.226 | -0.0027 |
| 6 | 4.1496 | -286.602365200 | +1.858 | -0.0026 |
| 7 | 4.3496 | -286.601432704 | +2.443 | -0.0022 |
| 8 | 4.5496 | -286.600689561 | +2.909 | -0.0016 |
| 9 | 4.7496 | 未收敛（第 58 步 SCF -286.599695968 后 l9999 终止） | (+3.53，仅参考) | — |

- **判读**：
  1. 松弛剖面在 **R≈3.35 Å 有浅极小**（p2 比 p1 低 0.237 kcal/mol，且收敛时 -DE/DX 由 p1 的 +0.0024 变为 p2 的 ≈0，
     即沿 R 的梯度变号）；此后到 4.55 Å **单调升高 3.2 kcal/mol**，该窗口内**确实没有内部极大**（协调者主结论成立）。
  2. 关键新信息：p1（R=3.1496，= 902/candidate_002 起点的 R 值）处 -DE/DX=+0.0024 ⇒ dE/dR<0，即**沿 R 向内收缩时 E 升高**；
     而同一级别的加合物极小值（902 末帧，R=1.641）比 p1 低 **5.15 kcal/mol**。若该松弛剖面在两 basin 之间连续，
     则 **(1.64, 3.15) Å 区间内必存在一个内部极大**（鞍点候选）——这正是 job 923 内区扫描要直接测量的对象。
     **注：这是剖面形状推断，不是鞍点证据**；且 902 的无约束下坡路径（3.15→1.64 单调降）走的是另一条坐标方向，
     不能替代松弛剖面。
  3. 结论仍区分口径：914 只能说明 3.15–4.55 Å 无内峰（且其中 4.75 Å 点未收敛）。

## P2 起点几何（914 扫描第 2 点收敛帧）provenance（2026-10-15）
- 原生日志：gold_finish_20261015/NI5/ts/scan01_C1N6/scan01_up_C1N6.log
  sha256 = 4bca52fa38168c9eab4def118f52c57f44329025faedfbaca3f8a627243eeac9（未改动）
- 帧表：gold_finish_20261015/NI5/ts/scan01_C1N6/scan01_up_C1N6_frames.csv（format_converter log→csv，142 帧）
  → 第 53 帧：E=-286.605703511 Eh（与原生 `SCF Done` 行 15183 一致，即 scan point 2 / R(1,6)=3.3496 Å 的收敛帧）
- 落盘 xyz：gold_finish_20261015/NI5/rc/job08_well_3496/well_3496_seed.xyz
  sha256 = b78c56f4d854f9f82d4377a6e1457d2ad83d5f53b7564257296b52bc64e79ecd
  （坐标逐字取自上述 CSV；write 工具提示 "suspected handwritten coordinates" —— 属工具面缺口：无"导出任意指定帧为 xyz"的入口，
  已按 BRIEF §7.5 报主协调，未改平台）
- internal_coordinates 复核：C2H9NO2、14 原子、**3 片段**；r(C1–O2)=1.214 Å（键级 2 = C=O）；
  r(C1–N6)=3.350 Å（far，未成键）；N6 中性（C5 1.458、H10 1.026、H11 1.021）；
  水接力氢键 O2···H13 1.842（forming_candidate）、O12···H10 2.058。→ 即题面 RC 物种（中性三分量 + 接力水，无质子转移）。
- 输入（待空槽提交）：rc/job08_well_3496/job08_well_3496_optfreq.gjf
  sha256 = e00826dc13e897ef934c6f7cae242b17e842f43da0e4447a7dfb65821fcdf3c6；8 cpus / 10240 MB；
  路由 `#p opt freq B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=Water)`
- 目的：判定该浅凹（E=-286.605703511 Eh，比 902 高 4.91 kcal/mol）是否为真实 0 虚频加成前极小值。

## 作业 926 — 分离组分 CH2O 无约束 Opt+Freq（done，本次新结果）
- 输入：`gold_finish_20261015/NI5/seeds/spec_CH2O/spec_CH2O.gjf`，sha256 = 6cc08f02eea102b7278c1831c98b77465390b647ea00815ad231315d56990bce
  （原 `%nproc=12/%mem=13GB` 已改为 `%nprocshared=8/%mem=10GB` 以符合本包预算，路由/几何/标题未变）
- 日志：`gold_finish_20261015/NI5/seeds/spec_CH2O/spec_CH2O.log`，sha256 = 9826cc8ac2c67399e6625a5c663c219422f757983edcf2527ce552921f7887ad
- job_id = 926；cpus = 8；memory_mb = 10240；q0/m1；完成时刻 2026-10-15 18:35
- log_parser：engine=gaussian；job_types=[opt, freq]；normal_termination=true；opt_converged=true；
  频率 6 个（4 原子 → 3N−6 = 6）、**imaginary_frequencies = []（零虚频）**；末条 SCF Done **E = -114.421603513 Eh**
- 原始行：1185 `SCF Done:  E(RB3LYP) =  -114.421603513  A.U. after 8 cycles`；1425/2171 `Normal termination of Gaussian 16`；
  1857/1868 `Frequencies -- 1202.8855 1263.3949 1524.6998` / `1838.1337 2899.2340 2967.3187`（全正）
- 用途：14 原子配平的"三分离碎片能量和"中的第一项（CH2O）。**计算完成 ≠ 验收通过**（尚未做与其它两片的配平求和）。

## 作业 932 — P2：3.3496 Å 浅凹是否为真实加成前极小值（已提交，排队）
- 输入：`gold_finish_20261015/NI5/rc/job08_well_3496/job08_well_3496_optfreq.gjf`
  sha256 = e00826dc13e897ef934c6f7cae242b17e842f43da0e4447a7dfb65821fcdf3c6
  起点几何 = `rc/job08_well_3496/well_3496_seed.xyz`（sha256 b78c56f4…9ecd；= 914 日志第 53 帧）
- job_id = 932；cpus = 8；memory_mb = 10240；priority = 0；提交时 state=ready（排队第 2 位）
- 目的：0 虚频 → 真实 0 虚频加成前极小值（E=-286.605703511 Eh，比 902 高 4.91 kcal/mol，本批 Gaussian 内相减）；
  滑落到两性离子·H₂O → 该浅凹不是极小值（本级别无加成前极小值）。

## 作业 923 — 内区上行松弛扫描（done，正常终止）→ **存在内部极大（内峰）**
- 输入：`gold_finish_20261015/NI5/ts/scan02_inner_C1N6/scan02_inner_C1N6.gjf` sha256 = f6ea803a7935d3017a76356e54dc247b9a6a12e4c46130ad860d5befb54b7444
  （路由 `# opt=(modredundant,maxstep=10) B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=Water)`；扫描行 `B 1 6 S 16 0.099998`）
- 日志：`gold_finish_20261015/NI5/ts/scan02_inner_C1N6/scan02_inner_C1N6.log`
  sha256 = 10a2b71efead3a4ea57d62f8fd14172611fb3106f6e4b53de8901f3fbd1d5346
- job_id = 923；cpus = 8；memory_mb = 10240；priority 0；q0/m1；**Normal termination（行 39282）/ Summary of Optimized Potential Surface Scan（行 38802）**
- 逐点（解析 = 每点 `Optimization completed` 前紧邻的那条 `SCF Done`；R 取该点收敛时的 `R4 R(1,6)`）：

| point | R(1,6)/Å | E/Eh | -DE/DX | ΔE vs p1/(kcal·mol⁻¹) |
|---|---|---|---|---|
| 1 | 1.6413 | -286.613531480 | 0.0 | 0.000 |
| 2 | 1.7413 | -286.612963147 | -0.0048 | 0.357 |
| 3 | 1.8413 | -286.612046074 | -0.0044 | 0.929 |
| 4 | 1.9413 | -286.611378810 | -0.0027 | 1.349 |
| 5 | 2.0413 | -286.610904177 | -0.0025 | 1.650 |
| 6 | 2.1413 | -286.610426688 | -0.0026 | 1.945 |
| 7 | 2.2413 | -286.609947490 | -0.0026 | 2.247 |
| 8 | 2.3413 | -286.609440581 | -0.0028 | 2.567 |
| 9 | 2.4413 | -286.608877838 | -0.0031 | 2.918 |
| 10 | 2.5413 | -286.608238410 | -0.0036 | 3.320 |
| 11 | 2.6413 | -286.607545769 | -0.0037 | 3.753 |
| 12 | 2.7413 | -286.606836898 | -0.0038 | 4.198 |
| 13 | 2.8413 | -286.606114383 | -0.0037 | 4.656 |
| 14 | 2.9413 | -286.605448503 | -0.0033 | 5.070 |
| 15 | 3.0413 | -286.604854217 | -0.0029 | 5.447 |
| **16** | **3.1413** | **-286.604343399** | **-0.0025** | **5.767（内峰所在点）** |
| 17 | 3.2413 | -286.605632908 | +0.0012 | 4.957 |

- 判读：E 从 p1 单调升高到 **p16（3.1413 Å）**，p17（3.2413 Å）回落 0.81 kcal/mol，且 p16 处 -DE/DX=-0.0025（仍在上坡）、p17 处 +0.0012（下坡）
  ⇒ **内峰位于 R∈(3.1413, 3.2413) Å**（受约束剖面）；相对 p1（= 两性离子·H₂O 加合物）峰高 **+5.767 kcal/mol**，
  相对同一级别无约束 RC 极小值（job 932，E=-286.605711743）为 **≥+0.859 kcal/mol**（p16 处，峰真实位置更高一点）。
  **这是受约束扫描的峰，不是 ΔE‡**；真值必须由 TS 优化 + 频率（ts_prepare 链）给出。
- **峰帧 xyz（真实落盘 artifact）**：`gold_finish_20261015/NI5/ts/scan02_inner_C1N6/scan02_peak_candidate.xyz`
  sha256 = f9db2f8c2fffc4d452710fcc80d986c7e32ffa90ec30fc01e5b84f6a7f91bb42
  （由 ts_guess(mode=scan_parse) 从 923 日志导出，frame 15 = point 16；ts_guess 字段：scan_has_internal_peak=true，barrier_kcal=5.7668（相对第一点））
- 923 的 p1（1.6413 Å，E=-286.613531480）与 902 末条 SCF Done（-286.613531375）一致到 1e-7 Eh → 两步同法自洽。

## 作业 935 — 分离组分 CH3NH2 无约束 Opt+Freq（done）
- 输入 `seeds/spec_CH3NH2/spec_CH3NH2.gjf`（sha256 120ff9440aea154e48e27c76dc1e4a101ea838ecaa208b0831cddd84986f7562，仅改 %nprocshared/%mem）
- 日志 `seeds/spec_CH3NH2/spec_CH3NH2.log` sha256 = 138dbe04924483fad3d027ee5e9698c024df0744dbb65b8761f09759f4334528
- job_id = 935；8 cpus / 10240 MB；normal termination；opt 收敛；15 个频率（7 原子 → 3N−6=15）**0 虚频**；末条 SCF Done **E = -95.7931237609 Eh**（行 1600）

## ts_prepare run ts_0006（C–N 加成 TS 全链，2026-10-15 启动）
- 依据：内峰（923）成立 + 真实 0 虚频 RC 极小值（932）成立 → 按 BRIEF §4 / 任务书第 4 条启动 durable 全链。
- run_id = **ts_0006**；run_dir = `/home/ly/Cloudra-mechanism-agent/ts/ts_0006`；启动时 revision=4，现 **revision=8，status=waiting，stage=build**
  （正在跑 job 937 `candidate_opt`，输入 `ts/ts_0006/jobs/declaration_0002/candidate_opt/seed-opt.gjf`，8 cpus / 10000 MB）
- 声明（全部真实 artifact）：
  - reaction：reactant_smiles `C=O.CN.O`、product_smiles `C[NH2+]C[O-].O`、charge 0 / mult 1 / closed_shell、reaction_center=[[1,6]]、atom_map=[1..14]（两文件同序，已由工具归一化确认）
  - calculations.dft = gaussian / B3LYP / def2SVP / `EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=Water)`
  - conformers.reactant = `rc/job08_well_3496/job08_well_3496_optfreq_last.xyz`（sha256 413752ab…50c6，evidence=`rc/job08_well_3496/job08_well_3496_optfreq.log`，components=3）
  - conformers.product = `rc/job01_rc_optfreq/rc_optfreq_m13_last.xyz`（sha256 11474dff…5032，evidence=`rc/job01_rc_optfreq/rc_optfreq_m13.log`）
  - guess = provided：`ts/scan02_inner_C1N6/scan02_peak_candidate.xyz`（sha256 f9db2f8c…bb42），evidence=`ts/scan02_inner_C1N6/scan02_inner_C1N6.log`
  - ts_optimization / verification.frequency / verification.irc / 两端点 opt+freq 全部 `{ref: dft}`
  - execution: cpus 8 / memory_mb 10000
- **第一次尝试的输入诊断（非科学限制）**：首次声明同时给了 `mol_path`（format_converter xyz→mol 写出的是**只含原子+坐标、无键**的 MOL），
  工具在 build 阶段拒绝：concrete identity 被感知为 `C.C.N.O.O.[HH]×9` ≠ 声明的 `C=O.CN.O`（failure_class=input_identity_unconfirmed）。
  → 用 `ts_resume(run_id='ts_0006', reason=...) `去掉 mol_path（改用 xyz-only 种子，连通性由几何感知）后通过（revision 8）。

## 三分离组分参考态 + 渐近参考（判据 ③，2026-10-15）
- 同批同法（Gaussian 16 / B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight + SCRF=(CPCM,Solvent=Water)），各自无约束 Opt+Freq，**全部 0 虚频**：
  | 组分 | job | 日志 | 日志 sha256 | E(末条 SCF Done)/Eh | 频率数/虚频 |
  |---|---|---|---|---|---|
  | CH2O | 926 | `gold_finish_20261015/NI5/seeds/spec_CH2O/spec_CH2O.log` | 9826cc8ac2c67399e6625a5c663c219422f757983edcf2527ce552921f7887ad | -114.421603513 | 6 / 0 |
  | CH3NH2 | 935 | `gold_finish_20261015/NI5/seeds/spec_CH3NH2/spec_CH3NH2.log` | 138dbe04924483fad3d027ee5e9698c024df0744dbb65b8761f09759f4334528 | -95.7931237609 | 15 / 0 |
  | H2O | 938 | `gold_finish_20261015/NI5/seeds/spec_H2O/spec_H2O.log` | 0953cd8acba991547cc379b443ecb007fbb76c59f211280745217b457b326347 | -76.3655114143 | 3 / 0 |
- **14 原子配平的三分离碎片能量和 E_sum = -286.580238688 Eh**（纯电子能；本批 Gaussian 内相加，可相减）
- 相对 E_sum（kcal/mol，纯电子能、不含 ZPE）：

| 物种 | E/Eh | ΔE vs 分离碎片/(kcal·mol⁻¹) |
|---|---|---|
| RC 极小值（job 932，0 虚频，3 片段） | -286.605711743 | **-15.985** |
| 内区扫描 p1（= 902 加合物，R=1.6413 Å） | -286.613531480 | -20.892 |
| 内区扫描 p16（内峰所在点，R=3.1413 Å） | -286.604343399 | **-15.126** |
| 内区扫描 p17（R=3.2413 Å） | -286.605632908 | -15.935 |
| 加成中间体·H₂O（902，0 虚频，2 片段） | -286.613531375 | -20.891 |

- **判读**：以分离反应物为参考，RC 稳定化 -15.99 kcal/mol；受约束内峰仅比 RC 高 0.86 kcal/mol，且**仍低于分离反应物 15.13 kcal/mol**
  ⇒ 按 Louie 2015 惯例这是**沉没垒（sunk barrier）**；相对 RC 的加成为放热 **-4.907 kcal/mol**。
  **注意：内峰 ≠ ΔE‡；真值待 ts_prepare 的 TS 优化 + 频率给出。** 能量只在本批 Gaussian 内相减，绝不与 ORCA 的 3.59/31.2 相减。

## ts_prepare run ts_0006 推进（2026-10-15 晚）
- revision 12 / status=waiting / stage=build；已完成 candidate_opt（job 937），当前 job 940 = `product_seed_opt`（管线自动提交，不占本包手工配额）。
- 下一步：TS opt → freq → IRC → 两端点 Opt+Freq；读取用 `ts_inspect(run_id='ts_0006')`。

## 作业 939 — 其它拓扑加成前络合物候选 rc/job03_cand000（done）→ **存在第二个、更低的加成前络合物（开链拓扑 RC-B）**
- 输入 `rc/job03_cand000/job03_cand000_optfreq.gjf`（sha256 6ad5bc4b08dcc5dd5929cb1948cb64cb8183033be1466902abafef90a97d5625；8c/10240MB；priority 0）
- 日志 `rc/job03_cand000/job03_cand000_optfreq.log` sha256 = 00876d20f963ca170885024f4224d7ca05da84691bc7d706d5922cfad40424a0；末帧 xyz `rc/job03_cand000/job03_cand000_optfreq_last.xyz` sha256 = c5f279ed0068efa51c0800ea926c3616d4dd387c1a6a69b8665596a49efd1f96
- job_id = 939；**normal termination；Stationary point found；36 个频率 0 虚频**（最低 42.35 cm⁻¹）；末条 SCF Done **E = -286.610034975 Eh**
- 末帧几何（internal_coordinates）：C2H9NO2、14 原子、**3 片段**；r(C1–O2)=1.210 Å（键级 2 = C=O）、r(C1···N6)=**3.393 Å（far，未成键）**、N6 中性；
  氢键拓扑与 RC-A（job08 的六元接力环）**不同**：**N6···H14(水) = 1.766 Å**（水捐 H 给胺 N）、O2···H10 = 2.330 Å（弱 N–H···O=C）、O2···H13 = 3.271 Å（无）
- **能量（本批 Gaussian 内相减）**：E = -286.610034975 Eh
  → 比 RC-A（job 932，-286.605711743）**低 2.713 kcal/mol**；比 902 加成中间体高 2.194 kcal/mol；比三分离碎片和（-286.580238688）低 **18.697 kcal/mol**
- **判读**：这是**第二个加成前极小值 RC-B（开链拓扑：水–H···N + N–H···O=C）**，能量低于本任务声明的接力环拓扑 RC-A。
  本步（E1）能垒仍按 BRIEF §4 报"相对**该步自身起点的极小值**"；本包的扫描/TS 链建立在 RC-A 上（六元接力环拓扑），
  故 ΔE‡ 将相对 RC-A 报；RC-B 的存在与相对能量作为**机理 caveat** 记录（若两者汇入同一鞍点，则相对 RC-B 的垒高 = 相对 RC-A 的垒高 + 2.713 kcal/mol；
  两者是否汇入同一鞍点未测）。




## 作业 932 — P2：3.3496 Å 浅凹的无约束 Opt+Freq（done）→ **真实 0 虚频加成前极小值成立**
- 输入：`gold_finish_20261015/NI5/rc/job08_well_3496/job08_well_3496_optfreq.gjf`
  sha256 = e00826dc13e897ef934c6f7cae242b17e842f43da0e4447a7dfb65821fcdf3c6；8 cpus / 10240 MB；priority 0；q0/m1
- 日志：`gold_finish_20261015/NI5/rc/job08_well_3496/job08_well_3496_optfreq.log`
  sha256 = 3af31534b147b6eb10f7995f44b7c16c6bb320db36580e3258c3abfa8bf205e5
- 末帧 xyz（同 RC 序 C,O,H,H,C,N,H,H,H,H,H,O,H,H）：`rc/job08_well_3496/job08_well_3496_optfreq_last.xyz`
  sha256 = 413752ab9793c43ba6f04d77f5e2c49d975ab8a636a85313519fc91e354150c6
- 关键原生行 / log_parser：`Normal termination of Gaussian 16`（行 6353/7808）；`-- Stationary point found.`（行 6047）；
  优化只走 2 步（行 6483 `Number of steps in this run= 2`）；36 个频率、**imaginary_frequencies = []（0 虚频）**，最低 35.13 cm⁻¹；
  末条 SCF Done **E = -286.605711743 Eh**（行 5890/6698）
- 末帧几何（internal_coordinates）：C2H9NO2、14 原子、**3 片段**；r(C1–O2)=1.214 Å（键级 2，C=O）、r(C1···N6)=**3.323 Å（far，未成键）**、
  N6 中性（H10 1.026、H11 1.021）、水接力氢键 O2···H13 1.841、O12···H10 2.057、O12–H14 0.968
- **验收状态**：计算完成 ✔（正常终止 + 收敛 + 0 虚频）→ 该浅凹**是真实极小值**，即题面定义的 **RC（加成前络合物：CH2O + CH3NH2 + 1 显式接力水，无质子转移）**。
- **能量口径（本批 Gaussian 内相减）**：E(RC) = -286.605711743 Eh；E(加成中间体·H₂O, 902) = -286.613531375 Eh
  → ΔE(RC → 中间体) = **-4.907 kcal/mol**（中间体更低）。**纯电子能差、不含 ZPE；不得与 ORCA 值相减。**
- 含义：RC 极小值存在 ⇒ 结合 914 剖面"3.1496 Å 处沿 R 向内上坡（dE/dR<0；E(3.1496)=-286.605325567 高于 E(RC)）"，
  则 **(1.64, 3.15) Å 区间内必存在内部极大**（鞍点候选）→ 由 job 923 内区扫描直接定位。

## 作业 943 — 其它拓扑候选 rc/job04_cand001（done）→ 与 job 939 **同一极小值（RC-B 镜像标记）**
- 输入 `rc/job04_cand001/job04_cand001_optfreq.gjf`（sha256 66a6aa1438722a7c00051c5464d6a6d6e188fe24b537e5dec7d8812355244196；8c/10240MB；priority 0）
- 日志 `rc/job04_cand001/job04_cand001_optfreq.log` sha256 = 0c4274b4f7bf714ee1abb1a4e0af4c8ae1f6e91085add73a4d31e7bc2d00f739；末帧 xyz sha256 = 6e4927a1fe8b684138200b1a33609d019354164c35e05a9b18954fdc4e592d06
- job_id = 943；**normal termination；Stationary point found；36 个频率 0 虚频**（最低 42.29 cm⁻¹）；末条 SCF Done **E = -286.610034965 Eh**（行 21868）
- 几何：r(C1–O2)=1.210 Å（C=O 键级 2）、r(C1···N6)=3.393 Å（未成键）、水 O–H13···N6 = 1.766 Å、N–H11···O2 = 2.330 Å
- **判读**：与 job 939 **同一极小值**（E 差 1×10⁻⁸ Eh；键长逐一相符，仅 H 标记镜像）⇒ 候选 000/001 是同一开链拓扑 RC-B 的两个镜像标记，**不构成独立物种**。

## ts_prepare run ts_0006 推进（第二阶段）
- 管线在 map 后重新装配（declaration_0003），此前声明的 provided guess 因端点 digest 变化被判失效（guess 阶段 failure_class=missing_input）
  → 已 `ts_resume(run_id='ts_0006', changes={guess:{kind:'provided', xyz_path:…/ts/scan02_inner_C1N6/scan02_peak_candidate.xyz, evidence_refs:[…/ts/scan02_inner_C1N6/scan02_inner_C1N6.log]}}, reason=…)`
  （峰帧与当前 build reactant 同为 1C 2O 3H 4H 5C 6N 7H 8H 9H 10H 11H 12O 13H 14H，逐位一致）→ **revision 37 / stage=refine**，
  管线自动提交 **job 946 = ts_opt（running）**。已完成阶段：declare → build → map → assemble → candidate_opt(942) → product_seed_opt(944)。
- 手工另提交 **job 947**（rc/job06_cand005，第四个拓扑判定；8c/10240MB；priority 0）。

## 作业 947 — 其它拓扑候选 rc/job06_cand005（done）→ **第三个加成前极小值 RC-C（C–N 半成键 2.06 Å，水只在羰基侧）**
- 输入 `rc/job06_cand005/job06_cand005_optfreq.gjf`（sha256 e8a051c0f12f91ee795b1b3014512d7303f0792e7db6b8c627618cca9ef4c78f；起点 r(C1···N6)=3.212 Å；8c/10240MB；priority 0）
- 日志 `rc/job06_cand005/job06_cand005_optfreq.log` sha256 = 8adcdb3d5601296abb1704575441c00f4353c1e7f6e8287b99bac36d82ffccb5
  末帧 xyz sha256 = 2a368b4503aa6b77b4e752e86d8f8545fcdedffb474c2cf9b08061c47d52323f
- job_id = 947；**normal termination；opt 收敛；36 个频率 0 虚频**（最低 69.17 cm⁻¹）；末条 SCF Done **E = -286.608664920 Eh**
- 几何：r(C1–N6)=**2.060 Å**（forming_candidate，非成键）、r(C1–O2)=1.240 Å（介于 C=O 1.21 与 C–O 1.30 之间）、
  O2···H14 = 1.731 Å（水捐 H 给羰基 O）、O12–H13 = 0.968、N6···O12 = 3.969 Å（水远离 N）→ **3 片段、C–N 半成键的浅极小**
- 能量（本批 Gaussian 内相减）：比 RC-A 低 **1.853**、比 RC-B 高 **0.860**、比 902 加成中间体高 **3.054** kcal/mol
  ⇒ 本级别至少存在 **三个**加成前极小值：RC-A（题面接力环，-286.605711743）/ RC-B（开链，-286.610034975，0 虚频，000=001 同一）/ RC-C（半成键，-286.608664920，0 虚频）。
- **口径不变**：E1 的 ΔE‡ 相对**本步自身起点极小值**报；本包 TS 链建在 **RC-A**（题面声明的接力环拓扑）上，RC-B/RC-C 作机理 caveat。

## ts_prepare run ts_0006 状态（复读）
- revision 37 / status=waiting / stage=refine；**job 946 = ts_opt running**（管线自动提交，不占手工配额）。
  已完成阶段：declare / build / map / assemble / guess / validate / submit / candidate_opt / product_seed_opt。

## ts_0006 首次 ts_opt 失败（attempt 4:ts_opt:946，nonconvergence）与重定位计划
- 管线 job 946 ts_opt 路由 = `#p opt=(TS,calcfc,noeigen) B3LYP/def2SVP EmpiricalDiSPersion=GD3BJ…`（即 `opt=(TS,calcfc,noeigen)` + dft 关键字），输入 `ts/ts_0006/jobs/declaration_0004/ts_opt/refine.gjf`（起点 = scan02_peak_candidate.xyz 坐标）
- 日志 `ts/ts_0006/jobs/declaration_0004/ts_opt/refine.log`；终止行 `Optimization stopped. -- Number of steps exceeded, NStep= 62` → `Error termination … l9999.exe`（**nonconvergence，非科学反证**）
- 末帧（frame 61，导出 `refine_last.xyz` sha256 196feef096c9b4279f538a6e59bd99a922806b403e8c746337f0958d137e7449）：
  r(C1–N6)=**3.316 Å**、r(C1–O2)=1.214、O2···H13=1.841、O12···H10=2.053、N6–H10=1.026 ⇒ **已滑回 RC-A 盆**；末条 SCF Done E=-286.605679079 Eh（比 RC-A −286.605711743 高 0.02 kcal/mol）
- **判读**：从 p16（3.1413 Å，受约束收敛点但沿 R 仍有梯度）出发，Berny TS 搜索在极平剖面上"过冲"进 RC 盆并震荡到步数上限。
  按 guidance：**TS 猜测失败不证明该步无鞍点**；这只能说明该 guess 不可直接使用。
- 峰位重估（用 923 的三个收敛点 p15/p16/p17 = 3.0413 / 3.1413 / 3.2413 Å，ΔE = +5.447 / +5.767 / +4.957 kcal/mol 相对 p1 的抛物线拟合）：
  **极大在 R ≈ 3.120 Å，峰高 ≈ +5.79 kcal/mol（相对加合物端点 p1）**；相对 RC-A 极小值 ≈ **+0.88 kcal/mol**（受约束估计，非 ΔE‡）。
- **下一步**：job 949 = 细网格松弛扫描 3.1413 → 3.0413 Å（0.02 Å × 5，向内，起点 = p16 帧）→ 用 ts_guess(scan_parse) 取精细峰帧，
  再以该帧为新的 `guess.kind=provided` 提交 `ts_resume` 重试 TS 优化；失败尝试自动保留。

## 细化扫描 949（向内 3.1413→3.0413 Å，0.02 Å×5）→ 内峰不在该区间
- 输入 `ts/scan03_fine_C1N6/scan03_fine_C1N6.gjf`（sha256 167e5d133d6e806d95d0514197b1556a4d91ca270c9cee0668870cc478768f67）；起点 = 923 的 p16 帧；路由同 923（`opt=(modredundant,maxstep=10)` + dft 关键字）
- 日志 `ts/scan03_fine_C1N6/scan03_fine_C1N6.log`；job_id = 949；**Normal termination**（ts_guess scan_parse: scan_has_internal_peak=**false**，剖面单调）
- 逐点收敛态：

| R(1,6)/Å | E/Eh | -DE/DX |
|---|---|---|
| 3.1413 | -286.604343398 | -0.0023 |
| 3.1213 | -286.604438683 | -0.0024 |
| 3.1013 | -286.604537356 | -0.0025 |
| 3.0813 | -286.604639019 | -0.0026 |
| 3.0613 | -286.604744608 | -0.0027 |
| 3.0413 | -286.604854345 | -0.0028 |

- 自洽：E(3.1413) 与 923 的 p16（-286.604343399）一致到 1e-9 Eh；E(3.0413) 与 923 的 p15（-286.604854217）一致到 1e-7 Eh。
- **判读**：3.0413 → 3.1413 Å 区间剖面单调升高（无极大）⇒ **内峰位于 (3.1413, 3.2413) Å 区间内**
  （923 的 0.1 Å 网格只有 p16=3.1413 是最高点、p17=3.2413 低 0.81 kcal/mol；两侧梯度符号相反）。
  峰高下界 = E(p16) = -286.604343399 Eh（相对加合物端点 +5.767 kcal/mol、相对 RC-A +0.86 kcal/mol）。
- 已提交 **job 950**（`ts/scan04_fine_out_C1N6/`，向外 3.1413→3.2413 Å，0.02 Å×5）以 0.02 Å 分辨率定位峰帧。

## 细化扫描 950（向外 3.1413→3.2413 Å，0.02 Å×5）+ 峰帧替换 → ts_opt 第二次尝试
- 输入 `ts/scan04_fine_out_C1N6/scan04_fine_out_C1N6.gjf`（sha256 88960647d03a09ffbf9a83b3f96d6a47b65ea2ca42ffede64262566e859ba1e2）；起点 = 923 的 p16 帧
- 日志 `ts/scan04_fine_out_C1N6/scan04_fine_out_C1N6.log` sha256 = ffeef2d60e773d6fb98381eb880798297bc77c5d7b942ac5ee1d853941d9a65a；job_id = 950；**failed：第 4 点 `Number of steps exceeded, NStep= 63` → l9999**
- 收敛点：3.1413 = -286.604343398（与 923 p16 一致）；3.1613 = -286.604251935（+0.057 kcal/mol）；3.1813 = **-286.604164912**（+0.112 kcal/mol，本扫描最高收敛点）；
  第 4 点 3.2013 处 `-DE/DX = +0.0001`（**梯度变号**）且迭代 63 步未收敛（缓慢下坡式震荡，末条 SCF -286.604087842）
- **判读**：受约束剖面极大在 **R ≈ 3.20–3.21 Å**，峰高 ≈ **-286.6041 Eh** ⇒ 相对加合物端点 **+5.9 kcal/mol**、相对 RC-A 极小值 **≈ +1.0 kcal/mol**（受约束估计，非 ΔE‡）。
- 峰帧替换（ts_resume，revision 47）：用 **job 950 末帧**（`ts/scan04_fine_out_C1N6/scan04_last_frame.xyz`，sha256 fcf6035ff8d01644f8c5ba71221d40ac8207b28df8d1dd83cdb5d5764b3c1ec0；R(C1–N6)=3.201 Å、r(C1–O2)=1.226、继电器 O2···H13=1.848 / O12···H10=2.070 完好）
  作新的 `guess.kind=provided`（evidence = 950 日志），替换原先 3.1413 Å 的峰帧（后者位于真实极大内侧、导致 946 号 TS 搜索过冲回 RC-A 盆）。
- 管线已排 **job 952 = ts_opt**（第二次尝试）。

## ★ ts_prepare run ts_0006 全链**验收通过（verified）** — NI5_E1 的 TS 与能垒（2026-10-15）
- run_id = **ts_0006**；最终 **revision 75 / status=ended / stage=verdict**；
  `result = {outcome:"verified", verified:true, reason:"verified transition state: exactly one imaginary mode (-164.5 cm^-1), usable IRC geometries from both directions, and each IRC endpoint lies between the TS and the corresponding declared minimum (direct pairing; interval proof per irc_path.assign_irc_endpoints); optimized endpoint identities match the declared reactant and product"}`
- 管线路由（全部同批同法）：`#p ... B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=Water)`；TS 优化用 `opt=(TS,calcfc,noeigen)`；8 cpus / 10000 MB

| 阶段 | job | 日志（绝对路径） | 日志 sha256 | 关键量 |
|---|---|---|---|---|
| ts_opt（第 2 次，新峰帧） | 952 | /home/ly/Cloudra-mechanism-agent/ts/ts_0006/jobs/declaration_0005/ts_opt/refine.log | 8a3a3c98554b606071335680f939737a336dd68c3848244329117cc38f8c055d | normal + opt 收敛；**E(TS) = -286.604225293 Eh** |
| frequency（TS） | 953 | …/declaration_0005/frequency/frequency.log | 28983faf81628e3e5f65048c6e29afa9bbc3779a18a5c8ac9977b7d1c9beaedd | 36 模、**恰 1 个虚频 = -164.4792 cm⁻¹** |
| irc（双向） | 954 | …/declaration_0005/irc/irc.log | f56ea88312e9567404d63d326b9a9625d0d1bcad30bfe4c3fa27d7d1b73e702b | normal；双向均有有效几何，rx 范围 [-0.11931, +0.11932] |
| reactant_opt / reactant_frequency（端点 A） | 955 / 956 | …/declaration_0005/reactant_opt/reactant_opt.log、…/reactant_frequency/reactant_frequency.log | 93b6d480a4d2287866802ce34c7f9f3ac4df332db987831b622dcb20c72a38c1 / 7bc76f5c7dd684156952cdd6816d5a52bc085f7f0739bd1fd707b3262bc8ab73 | **E = -286.605711957 Eh**、36 模 **0 虚频** ⇒ RC（= job 932 的 RC-A，差 2.1e-7 Eh） |
| product_opt / product_frequency（端点 B） | 957 / 958 | …/declaration_0005/product_opt/product_opt.log、…/product_frequency/product_frequency.log | c253e7254c7250de6e1f5d983b5c508b8ec7dbb968dd3dc0da402d2fb00b0c0b / 28ecf5cac878983823f61fe4a8d08deea758a844c245ebee9ffdb3123fb6e9d6 | **E = -286.613531483 Eh**、36 模 **0 虚频** ⇒ 两性离子加合物（= job 902，差 1.1e-7 Eh） |

- **能垒（纯电子能、本批 Gaussian 内相减、不含 ZPE）**：ΔE‡ = E(TS) − E(该步自身起点极小值 RC)
  = (-286.604225293) − (-286.605711957) = 0.001486664 Eh = **+0.93 kcal/mol**
- **步反应能**：E(加合物) − E(RC) = -0.007819526 Eh = **-4.91 kcal/mol**（放热）
- **相对三分离碎片（E_sum = -286.580238688 Eh）**：TS **-15.05**、RC **-15.99**、加合物 **-20.89 kcal/mol** ⇒ 本步为**沉没垒（sunk barrier）**
- **TS 几何（job 952 末帧导出 `ts_opt/ts_last.xyz`，sha256 92fde61d472878e511717f49d4b62b2d53ec1ac4275a98c48f10fbc369b232a6）**：
  r(C1···N6)=**3.125 Å（尚未成键）**、r(C1–O2)=1.212（C=O）、继电器氢键 O2···H13=1.843、O12···H10=2.081、N6–H10=1.025
- **验收 vs 口径 caveat（必须随终报转述）**：
  1. 虚频模**以氢位移为主**：heavy_atom_fraction = 0.033；watch pair (1,6) 占 pair-projected 位移的 **1.6%**（pair projection 0.170）。
     即 BRIEF §4 第 1 条"虚频模以声明的成键/断键原子对为主"**并未字面满足**；本链的通过依据是管线记录的
     **IRC 双向区间证据 + 两端点 Opt+Freq 身份一致（0 虚频）**（TS 处 C–N 仍为 3.125 Å，C–N 成键发生在 IRC 之后的路段）。
  2. 能垒相对"该步自身起点极小值"= 题面声明的接力环拓扑 **RC-A**；本级别另有两个更低/相近的加成前极小值（RC-B -286.610034975、RC-C -286.608664920）。
     若改以 RC-B 为参考且鞍点相同（**未测**），ΔE‡ = **+3.65 kcal/mol**。
  3. IRC 每向仅推进很小区间（rx ≈ ±0.12），符合 BRIEF §4"方向区间证据、不强求跑完 native 上限"。

### 附：TS 虚频模（-164.4792 cm⁻¹）的原子位移明细（自行从 frequency 日志原生位移表读出，供口径裁决）
- 原始行：`…/declaration_0005/frequency/frequency.log` 第 802 行起（`Frequencies -- -164.4792 60.9584 68.0916`）+ 其后 `Atom AN X Y Z` 表
- 各原子笛卡尔位移模长 |d|：**H4(C1–H) 0.747、H3(C1–H) 0.584**、H11(N–H) 0.185、**C1 0.112、N6 0.110**、O2 0.085、H10 0.079、H13(水) 0.099、C5 0.030、O12 0.022 …
- 归一化占比：Σ|d| = 2.353，其中重原子 0.360（**15.3%**）、氢 1.993（84.7%）；按质量加权 Σm·d² 计重原子约 **32%**
  （log_parser 报的 `heavy_atom_fraction = 0.0331` 用的是另一种归一化口径）
- **化学判读**：该虚频模是 **C1 上 CH₂ 的面外翻转（sp²→sp³ 预组织）+ C1···N6 相互靠近**（C1/N6 各 0.11 Å 量级、watch pair (1,6) 投影 0.170），
  即"形成 C–N 键所必需的重组"；只是振幅集中在轻的 H 上，故按重原子占比看起来很小。→ 这是"模是否以 C1–N6 为主"的裁决关键材料。

## 补强作业 959 / 960（其它拓扑 sweep 的剩余两个）——**均失败，不作证据**
| job | 目的 | 输入 | 日志 + sha256 | 结果 |
|---|---|---|---|---|
| 959 | rc/job05_cand004（水同时捐给 O2 与 N6，起点 r(C1···N6)=5.339 Å）Opt+Freq | `rc/job05_cand004/job05_cand004_optfreq.gjf`（sha256 496cc23ccd86d378aa93ba23a018ee80216bb6f060704f8e1dbc26f0b0b5a903） | `rc/job05_cand004/job05_cand004_optfreq.log`，sha256 a19cf9ae98b37914d926730f53b179aa4bbb85c6d7fd832097478e39e3f0e675 | **failed**：`Optimization stopped. -- Number of steps exceeded, NStep= 60`（原生步数上限；末段 SCF 在 -286.60914…-286.60916 Eh 平台震荡）⇒ **未收敛，不构成极小值证据**，其能量不得引用 |
| 960 | rc/job07_cand006（水只在羰基侧，起点 r(C1···N6)=6.715 Å）Opt+Freq | `rc/job07_cand006/job07_cand006_optfreq.gjf`（sha256 7da47229a131f49e525feaa93e2587298d8b4810887e3f0fff24cf73a8dfee13） | `rc/job07_cand006/job07_cand006_optfreq.log`，sha256 1f5c569facf4fe3c8b28a3d413d545a622b4b657d78ccd2cd75a57c3f289f825 | **failed（引擎/输入面）**：l103 `Error in internal coordinate system.`（`NTrRot= -1 NTRed= 48 NAtoms= 14 NSkip= 12`）⇒ 属输入坐标系统诊断，非科学结论 |
- 影响评估：判据 ④（2–3 个其它拓扑 Opt+Freq）已由**成功的** jobs 939（cand000）、943（cand001）、947（cand005）满足
  （结论：本级别至少三个加成前极小值 RC-A / RC-B / RC-C）；959/960 属超出要求的补强扫描，其失败**不影响** E1 结论，
  也**不得**据此宣称任何"不存在"，且不得引用其能量。

## ★ 重要更正（2026-10-15，explorer 复核引起，已自行核实）：ts_0006 的"连通性证据"被高估
**被更正的说法**：我在一页式结论（hub evt_4e6c0cb197864ff4）里写"IRC 双向第 1 点几何分别无约束优化到 RC 与加合物（身份与能量均对上）"。**这条不成立**。
- 自行核实（只读）：`ts/ts_0006/jobs/declaration_0005/reactant_opt/endpoint_source.json` = `{"kind":"species_reference","source_path":"…/reactant_source.xyz","irc_job_id":null,"irc_log_sha256":null}`；
  product 侧同形（`product_source.xyz`，`irc_job_id=null`）。
  ⇒ 端点 opt/freq（955/957）是**用声明端点几何本身作种子**跑的（reactant_source.xyz 的 r(C1–N6)=3.323 Å = RC-A；product_source.xyz = 1.641 Å = 加合物），
  "optimized endpoint identities match the declared reactant and product" 属**重优化后与声明自比**，**不能当作 IRC 连通性证据**；`irc_job_id=null` 也说明 IRC 端帧没有接到这两步上。
- IRC 实际位移极小：TS 帧 r(C1–N6)=3.1251 Å，两个方向第 1 帧 3.1162 / 3.1341 Å（**每向仅动 ~0.01 Å**），能量表 ≈ -0.00001/0.00000/-0.00001 Ha（≈0.006 kcal/mol）。
  ⇒ 该 run 的 "interval proof" 在这种情形下会**平凡通过**；它给出的"方向证据"实质只是"TS 几何 ±0.01 Å"的方向。
**虚频模口径（同意 explorer）**：−164.4792 cm⁻¹ 模以 C1 上两个 H 的位移为主（H4 0.747、H3 0.584 Å），C1/N6 各仅 0.11 Å；
  watch pair (1,6) 投影 0.170、占 pair-projected 位移 1.6%，log_parser heavy_atom_fraction=0.0331（我自算 Σ|d| 重原子占 15.3%、质量加权约 32%）。
  按技能/验收口径（"虚频模位移落在声明的成键重原子上"）该驻点属 **pseudo-saddle**，**不得当作已验收的 TS**。
**修正后的 NI5_E1 证据状态（务请按此引用）**：
1. **有驻点、它不是合格 TS**：TS 驻点 E = -286.604225293 Eh、r(C1···N6)=3.125 Å、恰 1 虚频 −164.4792 cm⁻¹，但**模式归属不通过**（H 主导）⇒ pseudo-saddle（如实标注）。
2. **连通性证据不足**：IRC 每向仅 ~0.01 Å、"到达端点"由声明端点自比给出，**不构成** TS↔两端点的连接证明。
3. **可用替代口径（仍属受约束/驻点估计，不是合格 ΔE‡）**：受约束松弛扫描 923/949/950 的剖面极大在 R≈3.20 Å，
   相对 RC-A ≈ **+1.0 kcal/mol**、相对加合物端点 +5.9 kcal/mol；pseudo-saddle 给出 +0.93 kcal/mol。二者一致 ⇒
   本级别"加成垒"的**最佳可用估计 ≈ +0.93 kcal/mol（相对 RC-A）**，但必须同时标注上述 1/2 两条限制。
4. 端点身份本身仍然成立（RC-A：job 932/955+956，0 虚频；加合物：job 902/957+958，0 虚频），只是**不能**用来证明与 TS 相连。
**未做/可补强（供裁决者选择）**：① 加大 IRC 步长/点数重跑（native `irc=calcfc` 在极平势面第 1 点即自行停止，maxpoints=10 未用尽）——会新建 revision；
② 冻住软模（甲胺/水取向、醛基 H 摇摆）后只沿 R(C1–N6) 搜索以尝试拿到重原子主导的鞍点；
③ 若两者都拿不到，按政策 (4) 记"本级别无合格独立鞍点 + 替代口径（受约束剖面 / pseudo-saddle ≈ +0.9 kcal/mol）"。

## 平台限制（新，属工具面缺口；建议并入 issue #177 类目）
**ts_prepare/ts_resume 无法设置 IRC 的步长/点数**：尝试 `verification.irc={replace:{… keywords:"… irc=(calcfc,stepsize=30,maxpoints=30)"}}` 时被准入检查拒绝：
`failure_class=compute_admission_rejected`，原文 `keywords: expected ['empiricaldispersion=gd3bj','int(ultrafine)','irc=(calcfc,stepsize=30,maxpoints=30)','scf=tight','scrf=(cpcm,solvent=water)']; actual ['empiricaldispersion=gd3bj','int(ultrafine)','scf=tight','scrf=(cpcm,solvent=water)']`
⇒ 管线自行写死 `irc=calcfc`（默认 step 0.1 bohr / maxpoints=10），且会从声明 keywords 中剔除 `irc=` token。
**后果**：在极平势面上 native IRC 第 1 点即按原生判据停止（见"★ 重要更正"节）时，**无法**通过工作流加大步长/点数来获得更长的 IRC 轨迹。
**处置记录**：该次修订（rev 78）被拒后阻塞；随后已用同一写法把 verification.irc 还原为标准 dft 配置（不含 `irc=` token）。
（另注：还原调用一度返回工具内部异常 `Tool execution failed internally`，但 run 已推进到 rev 79/running —— 与 issue #176/#177 描述的 ts_prepare 异常不可诊断症状同类。）
















