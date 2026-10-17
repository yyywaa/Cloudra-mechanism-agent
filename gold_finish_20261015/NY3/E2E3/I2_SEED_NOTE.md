# I2_SEED_NOTE — NY3 E2/E3：I2（甲酸+甲醇盐+Na⁺）是否为本战役级别的真极小值

道：NY3 包 I2/E2E3 委派任务（E2E3 道）｜工作根：/home/ly/Cloudra-mechanism-agent｜目录：`gold_finish_20261015/NY3/E2E3/`
日期：2026-10-15 23:5x｜边界：只写 NY3/ 内文件；未动 `ts/`（只读引用）、未改平台代码/DB/进程、未 git。
口径（本战役级别，逐字）：Gaussian 16，`B3LYP/def2SVP` + `EmpiricalDispersion=GD3BJ` + `Int(UltraFine)` + `SCF=Tight` + `SCRF=(CPCM,Solvent=Water)`，charge 0 / multiplicity 1，8 核 / 10GB（%mem=10GB），priority 0。
半经验势面探索口径：xtb 6.5.0，`GFN2-xTB` + `--alpb water`，OMP_NUM_THREADS=1。

## 0 状态（本文件会随 DFT 作业落地更新）

- **xTB 势面探索已完成**（5 个起点，全部收敛 + 全部 0 虚频），结果见 §3。
- **DFT 验证进行中**：job **971**（主候选 candA_H6away 的 GFN2 极小值，Opt+Freq）、job **981**（对照候选 candA_H6away_syn 紧凑接触对，Opt+Freq）。两者均已提交、排队中；结果落地后回填 §4/§5。
- **ts_e3_guess.xyz 已交付**（§6）。

## 1 科学问题与判据

Q：I2（registry 定义 `[Na+].[CH3][O-].[CH(O)O]`，即 H6 键在 O1、甲氧基独立、Na⁺ 在侧）= 本级别是否存在 0 虚频的真极小值？
判据（本任务给定）：DFT Opt 收敛 + 频率全实（0 虚频）+ H6 仍在 O1（r(O1-H6) ≈ 1.0 Å）且甲氧基 O3 未与 C4 成键（C4···O3 ≈ I2 值，不是 I1 的 1.43 Å）。
据此判定 E2（断 C4-O3、成 C4=O5 π）与 E3（H6: O1→O3）是**分步**（存在 I2 极小值，E3 从该极小值起步）还是**协同步**（不存在 I2 极小值，PT 顺流而下）。

既有反证（本包已落盘、只读引用）：`ts/ts_0003/jobs/declaration_0001/product_seed_opt/seed-opt.log`
sha256 `3ae4dccbe8ca3119d3fa0853b3bc5ac3743ba3abc3fa52a3314e3858048de8be`（job 922，NStep=44 超步数终止 l9999）：
从 `prep/i2.xyz` 出发的自由 Opt 里 H6 从 O1 迁到 O3（R(O3-H6) 1.674→1.010 Å、R(O1···H6) 1.009→1.596 Å）、末态 C4-O8 1.2535 / C4-O9 1.2572 Å（甲酸根等价双氧）⇒ 该起点**顺流而下到 P**。
直接原因：`prep/i2.xyz` 里 H6 已经预转移（d(O3···H6)=1.674 Å、d(O1-H6)=1.009 Å），种子本身就落在 PT 过渡区。**这只能说明"那个构象不是极小值"，不能说明"所有 I2 构象都不是极小值"** —— 所以本轮按构象分类重新采样。

## 2 候选种子（两类要求 → 5 个起点）

原子序一律 = `prep/i2.xyz` 顺序：**1 Na ｜ 2 C2 ｜ 3 O3 ｜ 4,5,6 H(甲基) ｜ 7 C4 ｜ 8 O5 ｜ 9 O1 ｜ 10 H(C4) ｜ 11 H6**。
所有几何由 `internal_coordinates mode=transform`（刚性内坐标操作）从真实文件产生，未手键坐标；距离由 `internal_coordinates mode=analyze` 实测。

| tag | 文件 | sha256 | 构造（ops，1-based） | 实测距离（Å） |
|---|---|---|---|---|
| candA_H6away_syn（类 a） | i2_seed_candA_H6away_syn.xyz | f580e848eaf4b7cea43df59646f0ae719fada82accd4d4edc9213bab1c607120 | prep/i2.xyz → rotate [11] 绕轴 [9,7] 180° | O1-H6 1.009 / O3···H6 **3.552** / O1···O3 2.671 / C4···O3 3.254 / C4-O1 1.341 / C4=O5 1.224 / Na-O1 2.524 / Na-O3 2.427 / Na···H6 3.045 |
| candA_H6away_xtbmin（类 a，主候选） | i2_seed_candA_H6away_xtbmin.xyz | 422b79e6cd1cd3d7648c7d7bad4f94c122187572c0890aee7442b108837cedb4 | 上者经 xtb `--ohess` 优化（run_candA/xtbopt.xyz，仅补注释行） | O1-H6 0.979 / O3···H6 4.459 / O1···O3 3.778 / C4···O3 4.018 / C4-O1 1.305 / C4=O5 1.204 / C2-O3 1.349 / Na-O1 2.528 / Na-O3 1.876 / Na-O5 2.111 |
| candB_methoxide_out（类 b） | i2_seed_candB_methoxide_out.xyz | bc2477926f83aa4b25cf004b70b372c276fb8e41e2a425fef0f5e7c559b1b870 | prep/i2.xyz → stretch [1,3]（Na→O3 平移甲氧基 2.427→3.600） | O1-H6 1.009 / O3···H6 2.497 / O1···O3 **3.424** / C4···O3 3.873 / Na···O3 3.600 / Na···H6 2.106 |
| candC_combined（a+b） | i2_seed_candC_combined.xyz | 3cb504218c690d904a612b1f72e316c1e3056aa12ce921ab81c4184d40859dce | candB 的甲氧基外移 + rotate [11] 绕 [9,7] 180° | O1-H6 1.009 / O3···H6 4.296 / O1···O3 3.424 / C4···O3 3.873 / Na···O3 3.600 |
| candD_classB（类 b，Na⁺ 双齿甲酸根） | i2_seed_candD_classB.xyz | 78448225332a095326025a2c3beaa891c287746889656f7cba6d83bd4856c840 | candA 的 xtb 极小值 → stretch [1,3] Na···O3 1.876→3.300 | O1-H6 0.979 / O3···H6 5.540 / O1···O3 **4.996** / C4···O3 5.295 / Na-O1 2.528 / **Na-O5 2.111（双齿甲酸根）** / Na···O3 3.300 |

两类要求覆盖情况：
- 类 (a)「H6 仍键在 O1、d(O3···H6) ≥ 2.2 Å、Na⁺ 桥联 O1/O3」→ candA（syn 与 xtb 极小值两个版本：3.552 / 4.459 Å）。
- 类 (b)「甲氧基离甲酸 OH 更远、d(O1···O3) ≥ 3.2 Å」→ candB（3.424，Na 仍靠近 O1 但已脱离 O3）、candC（3.424 + H 转离）、candD（4.996，Na⁺ 双齿甲酸根 O1/O5，甲氧基外移）。

## 3 xTB（GFN2-xTB/ALPB water）势面筛选 —— 5 个起点，全部 Opt+数值 Hessian

日志目录：`E2E3/xtb/run_<tag>/xtb_ohess.log`（起点坐标同目录 `start.xyz`，末态 `xtbopt.xyz`）。

| run | 起点 | sha256(log) | 优化收敛 | E(GFN2/ALPB, Eh) | 虚频数 | 末态身份实测（Å） |
|---|---|---|---|---|---|---|
| run_origA | prep/i2.xyz（H6 已预转移） | 16e6c29086b4908461fa93a325d8000b08f4a4763aa57bb16de7ded1e5f217eb | 103 步 | -19.339225 | **0** | **P 型**：H 在 O3（O3-H6 0.969、O1···H6 5.012）、C4-O1 1.236 ≈ C4-O5 1.235（甲酸根等价）、C2-O3 1.423（甲醇）、Na-O1 2.113 / Na-O3 2.087 / Na-O5 2.115（Na⁺ 三配位） |
| run_candB | candB（甲氧基外移 3.42） | ae6f8c677df834f4bb87fe962c5ff340e3543d4230805d3f646f32996f74e4d0 | 104 步 | -19.339238 | **0** | **P 型**（与 run_origA 同一极小值能量差 0.008 kcal/mol）：甲氧基回到 Na⁺（Na-O3 2.087），H 迁到 O3 |
| run_candA | candA_H6away_syn（主候选） | 0fc67132b22508555bc154a0cdd3af3b19f1912aff1cd1e535ee69217420e6f5 | 28 步 | -19.289398 | **0** | **I2 型**：O1-H6 0.979、O3···H6 4.459、C4-O1 1.305 / C4=O5 1.204（甲酸）、C2-O3 1.349（甲醇盐）、Na-O1 2.528 / Na-O3 1.876 / Na-O5 2.111 |
| run_candC | candC（外移 + H 转离） | 68172c7298b11660029958e7c5b0d855d9e91c52232a14587149f91ef40ee816 | 20 步 | -19.289324 | **0** | **I2 型**（同一极小值，与 run_candA 差 0.05 kcal/mol）：O1-H6 0.979、O1···O3 3.800、C4-O1 1.305 |
| run_candD | candD_classB（Na⁺ 双齿甲酸根、甲氧基 3.30） | 580abdbbd5ede8ed40feffafc13f8c181fe037265efe6c407937fc745187e371 | 18 步 | -19.289370 | **0** | **回到同一 I2 型极小值**：Na-O3 1.874（Na⁺ 重新抓住甲醇盐 O3）、O1-H6 0.979、O1···O3 4.033、C4-O1 1.305 |

要点（xTB 层面）：
1. **只要 H6 转离 O3（类 a），GFN2/ALPB 下存在一个真正的 I2 极小值**（0 虚频，O1-H6 0.98、O3···H6 ≥ 4.4 Å、C4-O3 ≥ 4.0 已断）；从两个不同起点（candA、candC）与一个"类 b"起点（candD）都落到它，说明它是一个确定的小盆地。
2. **只要 H6 仍指向 O3（即 registry 的 prep/i2.xyz 构象，O3···H6 = 1.67 Å）**，无论甲氧基起始多远（candB），优化都直接顺流到 P（H 落到 O3、甲酸根等价化）。
3. 能量差（**仅 GFN2/ALPB 层，不得与本批 DFT 混排**）：I2 型 − P 型 = -19.289398 −(-19.339238) = +0.04984 Eh ≈ **+31.3 kcal/mol**（I2 型为高能中间体）。

## 4 DFT（本战役级别）Opt+Freq 作业

| job | 起点种子 | 输入 | 日志 | 状态 |
|---|---|---|---|---|
| 971 | i2_seed_candA_H6away_xtbmin.xyz（sha 422b79e6…） | E2E3/i2_candA_optfreq.gjf（sha 5784defb127e7aeb660662866436e87f2397aafc773bf388cf6cd69bdf22c590） | 待落盘 | 已提交（ready/排队），route 单行 100 字符、未被折行、GD3BJ 完整 |
| 981 | i2_seed_candA_H6away_syn.xyz（sha f580e848…） | E2E3/i2_candA_compact_optfreq.gjf（sha a44ac24b12f0cd0745d08991fbfca8e8b5c41800d21c773d03d1da4df0540888） | 待落盘 | 已提交（ready/排队） |

**待回填（每个 DFT 结果必须报的字段）**：job_id、日志绝对路径、sha256、Normal/Error termination、虚频个数与最低几个模（cm⁻¹）、d(O1-H6)/d(O3···H6)、C4-O1/C4-O5/C4-O3、Na 配位距离、末态身份（甲酸 vs 甲酸根：C-O 双/单键长）。

## 5 E2/E3 分步 or 协同步：证据化判断（DFT 结果落地后定稿）

目前的证据链（xTB 层已完成，DFT 待定）：
- 反证：registry 的 I2 种子构象（H6 指向 O3）在本级别 DFT 下确实"顺流而下"到 P（job 922 的 seed-opt.log）。
- 正证：把 H6 转离 O3 后，GFN2/ALPB 给出 0 虚频的 I2 型极小值；DFT 是否同样成立 = job 971 / 981。
- 若 job 971（或 981）给出 0 虚频且 H6 在 O1 ⇒ **I2 存在真极小值 ⇒ E2/E3 可以分步**；同时说明"协同步/顺流而下"只发生在 H6 预取向朝向 O3 的那个构象（质子转移在该取向屏障≈0）。
- 若两者都把 H6 送到 O3 ⇒ 只能写"未找到 I2 极小值（已试候选见 §2/§3）"，并保留逐候选的失败日志。

## 6 ts_e3_guess.xyz（E3 质子转移初猜）

- 文件：`E2E3/ts_e3_guess.xyz`，sha256 `de8d737cb13cc95a6916cbd55ac00104207da1d5f395e68ea8b2f212335c00e1`，11 原子，**原子序同 prep/i2.xyz**。
- 实测（`internal_coordinates mode=analyze`）：**d(O1-H6) = d(O3···H6) = 1.250 Å**（O1-H6-O3 共线，O1···O3 = 2.500 Å）；**C4···O3 = 3.254 Å（= prep/i2.xyz 的 I2 值，未被拉回 I1 的 1.43）**；C4-O1 1.341、C4=O5 1.224、C2-O3 1.325、Na-O1 2.524、Na-O3 2.427（与 prep/i2.xyz 一致）。
- 构造链（全部 `internal_coordinates mode=transform`，两步调用，因为没有手键坐标）：
  1. `prep/i2.xyz` → rotate [11] 绕轴 [9,7] −74°（把 H6 转离 Na⁺/O3，解除 Na1-O9-H11 三元环对"沿键平移"的限制）→ 中间文件；
  2. 中间文件 → stretch [9,11] → 1.25 Å；rotate [2,3,4,5,6] 绕轴 [1,7] −11.79°（甲氧基方位角改变，**保持 Na-O3 = 2.427 与 C4···O3 = 3.254 不变**，使 O1···O3 = 2.500）；rotate [11] 绕轴 [9,6] 174.765°（把 H6 摆到 O1···O3 连线上）。
  操作参数由脚本 `E2E3/tools/e3_guess_search7.py`/…_9.py（只读几何搜索，不写坐标）解出；几何本身由化学工具产生。
- 语义：H6 夹在 O1/O3 中间（1.250/1.250），甲氧基尚未回到 C4（C4···O3 3.254 = I2 值）⇒ 这是"甲氧基已离去、质子正在 O1→O3 转移"的 E3 TS 初猜（与 `prep/ts_e23_guess.xyz` 的 E2+E3 六元环耦合初猜相对照：后者 C4-O3 2.011 已拉回中间态）。**这是初猜，不是鞍点，也不是能垒证据。**

## 7 缺测 / 未决

- DFT 的频率与最终几何：job 971 / 981 落地后回填（见 §4）。
- 本文件不含任何能垒数值；I2↔P 的 DFT 能量差也待 §4 结果。
- xtb 层没有做 IRC/扫描（半经验势面探索仅用于筛构象）；TS/IRC 属 durable TS run，本道不碰 `ts/`。
- P 端参考：job 922 的 seed-opt.log 给出末态 E(RB3LYP) = -467.045443 Eh（同级别、纯电子能），**但其优化被 NStep=44 截断、且无频率** ⇒ 只能作为"P 端身份 + 同级别能量参考"，不能当作已验证极小值。
