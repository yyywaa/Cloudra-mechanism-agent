# NI5_E1 数值自检（独立复核 lane）

- 复核对象：NI5_E1 = CPCM(Water) / q0 / m1，CH2O + CH3NH2 + 1 显式接力水的 C–N 加成
- 复核范围：任务书指定的 19 个原生日志（TS 链 declaration_0005 七件 + 本包 RC/中间体/扫描/分离组分 12 件，含 2 个失败作业）
- 复核者：NI5 包 数值自检子代理（独立复核 lane）
- 复核日期：2026-10-15 ｜ 工作根目录：/home/ly/Cloudra-mechanism-agent
- 被复核声明：gold_finish_20261015/NI5/STATUS.md §11/§12（该文件 sha256 = 20db813bce606e7cd625e81a6f112a417d8ccd92210277ec04f829bb0ca2e053，198 行）
- 纪律遵守：本页只读原生日志；未改写任何原生日志/输入；未提交任何 QM 作业；未提交 git；未改平台代码/数据库；只写本文件。
- 本页只给"从原生日志读到的数"与"与 STATUS §12 的逐条差异"，不写裁决性结论。每条数字都可按"绝对路径 + 行号"回查。
- 换算：1 Eh = 627.5095 kcal/mol（任务书指定常数）。

## 0 速览（本页复算值）

| 量 | 复算值（Eh） | 复算值（kcal/mol） | 来源（原生日志 + 行号） |
|---|---|---|---|
| E(RC-A, 任务书指定参考起点) | -286.605711743 | — | rc/job08_well_3496/job08_well_3496_optfreq.log 行 6698 |
| E(加合物·H2O) | -286.613531375 | — | rc/job01_rc_optfreq/rc_optfreq_m13.log 行 19092 |
| E(TS) | -286.604225293 | — | ts/ts_0006/jobs/declaration_0005/ts_opt/refine.log 行 3706 |
| ΔE‡ = E(TS) − E(RC-A=job08) | +0.001486450 | **+0.9328** | 上三行相减 |
| ΔE‡ = E(TS) − E(IRC 端点 A=job955) | +0.001486664 | +0.9329 | 955 行 3415 |
| 步反应能 E(加合物) − E(RC-A) | -0.007819632 | **-4.9069** | 902 行 19092 − 932 行 6698 |
| E_sum = E(CH2O)+E(CH3NH2)+E(H2O) | -286.580238688 | — | 926 行 1659 / 935 行 2151 / 938 行 1495 |
| TS − E_sum | -0.023986605 | **-15.0518** | |
| RC-A − E_sum | -0.025473055 | **-15.9846** | |
| 加合物 − E_sum | -0.033292687 | **-20.8915** | |
| TS 唯一虚频 | — | -164.4792 cm-1 | 953 行 802 |
| sha256 与 STATUS §12/§3 声明 | **全部一致**（9/9，见 §7 第 23 条） | | |

## 1 日志清单（sha256 为 sha256sum 实读；engine/normal_termination/opt_converged/频率数为 log_parser 返回值）

TS 链 run_id=ts_0006（绝对前缀 /home/ly/Cloudra-mechanism-agent/ts/ts_0006/jobs/declaration_0005/）；job_id 由 ts_inspect(ts_0006).available_results 的 job_id 与 artifact 路径逐字核对：

| # | 日志（绝对路径） | job_id | sha256 | engine | normal_termination | opt_converged | 频率个数 | imaginary_frequencies |
|---|---|---|---|---|---|---|---|---|
| 1 | .../declaration_0005/ts_opt/refine.log | 952 | 8a3a3c98554b606071335680f939737a336dd68c3848244329117cc38f8c055d | gaussian | true | true | 0 | null |
| 2 | .../declaration_0005/frequency/frequency.log | 953 | 28983faf81628e3e5f65048c6e29afa9bbc3779a18a5c8ac9977b7d1c9beaedd | gaussian | true | null | 36（=frequencies_cm 35 + 1 虚频） | [-164.4792] |
| 3 | .../declaration_0005/irc/irc.log | 954 | f56ea88312e9567404d63d326b9a9625d0d1bcad30bfe4c3fa27d7d1b73e702b | gaussian | true | true（IRC 双向收敛） | 0 | null |
| 4 | .../declaration_0005/reactant_opt/reactant_opt.log | 955 | 93b6d480a4d2287866802ce34c7f9f3ac4df332db987831b622dcb20c72a38c1 | gaussian | true | true | 0 | null |
| 5 | .../declaration_0005/reactant_frequency/reactant_frequency.log | 956 | 7bc76f5c7dd684156952cdd6816d5a52bc085f7f0739bd1fd707b3262bc8ab73 | gaussian | true | null | 36 | [] |
| 6 | .../declaration_0005/product_opt/product_opt.log | 957 | c253e7254c7250de6e1f5d983b5c508b8ec7dbb968dd3dc0da402d2fb00b0c0b | gaussian | true | true | 0 | null |
| 7 | .../declaration_0005/product_frequency/product_frequency.log | 958 | 28ecf5cac878983823f61fe4a8d08deea758a844c245ebee9ffdb3123fb6e9d6 | gaussian | true | true | 36 | [] |

NI5 包（绝对前缀 /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NI5/）；job_id 由同目录 .cloudra/guard-<id>.log 的 task_id 行确认：

| # | 日志（绝对路径） | job_id | sha256 | engine | normal_termination | opt_converged | 频率个数 | imaginary_frequencies |
|---|---|---|---|---|---|---|---|---|
| 8 | rc/job08_well_3496/job08_well_3496_optfreq.log（RC-A） | 932 | 3af31534b147b6eb10f7995f44b7c16c6bb320db36580e3258c3abfa8bf205e5 | gaussian | true | true | 36 | [] |
| 9 | rc/job01_rc_optfreq/rc_optfreq_m13.log（加合物 902） | 902 | e82ba58586b95764240844bc3ed60fc9484c63b616a35cf062d46bf0824d4eb9 | gaussian | true | true | 36 | [] |
| 10 | rc/job03_cand000/job03_cand000_optfreq.log（RC-B） | 939 | 00876d20f963ca170885024f4224d7ca05da84691bc7d706d5922cfad40424a0 | gaussian | true | true | 36 | [] |
| 11 | rc/job04_cand001/job04_cand001_optfreq.log | 943 | 0c4274b4f7bf714ee1abb1a4e0af4c8ae1f6e91085add73a4d31e7bc2d00f739 | gaussian | true | true | 36 | [] |
| 12 | rc/job06_cand005/job06_cand005_optfreq.log（RC-C） | 947 | 8adcdb3d5601296abb1704575441c00f4353c1e7f6e8287b99bac36d82ffccb5 | gaussian | true | true | 36 | [] |
| 13 | intermediate/job02_zwitterion_optfreq/zwitterion_optfreq_m13.log | 909 | f50c3b8076584e51345eebbc005d6474d0de8a41717b1d03a141aca0372f9c7a | gaussian | true | true | 36 | [] |
| 14 | ts/scan02_inner_C1N6/scan02_inner_C1N6.log（内区扫描，17 点） | 923 | 10a2b71efead3a4ea57d62f8fd14172611fb3106f6e4b53de8901f3fbd1d5346 | gaussian | true | true（每点收敛） | 0 | null |
| 15 | seeds/spec_CH2O/spec_CH2O.log | 926 | 9826cc8ac2c67399e6625a5c663c219422f757983edcf2527ce552921f7887ad | gaussian | true | true | 6 | [] |
| 16 | seeds/spec_CH3NH2/spec_CH3NH2.log | 935 | 138dbe04924483fad3d027ee5e9698c024df0744dbb65b8761f09759f4334528 | gaussian | true | true | 15 | [] |
| 17 | seeds/spec_H2O/spec_H2O.log | 938 | 0953cd8acba991547cc379b443ecb007fbb76c59f211280745217b457b326347 | gaussian | true | true | 3 | [] |
| 18 | rc/job05_cand004/job05_cand004_optfreq.log（已知失败） | 959 | a19cf9ae98b37914d926730f53b179aa4bbb85c6d7fd832097478e39e3f0e675 | gaussian | **false** | **false** | 0 | null |
| 19 | rc/job07_cand006/job07_cand006_optfreq.log（已知失败） | 960 | 1f5c569facf4fe3c8b28a3d413d545a622b4b657d78ccd2cd75a57c3f289f825 | gaussian | **false** | null | 0 | null |

- job_id 对照来源：ts_inspect(run_id='ts_0006') → available_results 逐项给出 stage/job_id/artifacts（952 ts_opt、953 frequency、954 irc、955 reactant_opt、956 reactant_frequency、957 product_opt、958 product_frequency，artifact 路径与上表逐字一致）。
- ts_0006 权威状态：revision = 75，status = ended，stage = verdict，result.outcome = verified、result.verified = true。
- 使用方法：所有日志 route 行均为 B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight + SCRF=(CPCM,Solvent=Water)，q0/m1（例：902 输入行 3、行 116；952 输入行 3、行 116）。ts 链的 opt/freq/irc 输入 %nproc=8、%mem=10000MB。

## 2 关键原生行（行号 + 行文本）

### 2.1 TS 链（declaration_0005）
1. ts_opt/refine.log（952）
   - 行 3706：SCF Done:  E(RB3LYP) =  -286.604225293     A.U. after    8 cycles
   - 行 4162：Normal termination of Gaussian 16 at Thu Oct 15 19:20:38 2026.
   - 行 3850：Optimization completed. ／ 行 3851：   -- Stationary point found.
   - 行 139：NAtoms=     14 NQM=       14 NQMF=       0 NMMI=      0 NMMIF=      0 ／ 行 116：Charge =  0 Multiplicity = 1
2. frequency/frequency.log（953）
   - 行 517：SCF Done:  E(RB3LYP) =  -286.604225293     A.U. after   11 cycles
   - 行 1552：Normal termination of Gaussian 16 at Thu Oct 15 19:21:02 2026.
   - 无 "Optimization completed." / "Stationary point found."；尾段原生力收敛表行 1278–1283（行 1279：Maximum Force            0.000033     0.000450     YES）
   - 12 个频率块行 802–1033（见 §4）
3. irc/irc.log（954）
   - 行 169：Maximum points per path      =  10 ／ 行 170：Step size                    =   0.100 bohr ／ 行 176：Initial Hessian              = CalcFC
   - 行 802：Point Number:   0          Path Number:   1 ／ 行 1230：Point Number:   1          Path Number:   1（FORWARD）／ 行 1705：Point Number:   1          Path Number:   2（REVERSE）
   - 行 1252：CHANGE IN THE REACTION COORDINATE =    0.11932 ／ 行 1727：CHANGE IN THE REACTION COORDINATE =    0.11931
   - 行 1257 / 1732：PES minimum detected on this side of the pathway.
   - 行 1742–1744（Summary of reaction path following）：1  -0.00001  -0.11931 ／ 2   0.00000   0.00000 ／ 3  -0.00001   0.11932
   - 行 1747：Total number of points:                    2
   - 行 517 / 1111 / 1586（该日志 3 条 SCF Done）：-286.604225293 / -286.604232504 / -286.604231896
   - 行 1971：Normal termination of Gaussian 16 at Thu Oct 15 19:21:37 2026.
4. reactant_opt/reactant_opt.log（955）
   - 行 3415：SCF Done:  E(RB3LYP) =  -286.605711957     A.U. after    6 cycles
   - 行 3884：Normal termination of Gaussian 16 at Thu Oct 15 19:22:09 2026.
   - 行 3570：Optimization completed. ／ 行 3571：   -- Stationary point found.
5. reactant_frequency/reactant_frequency.log（956）
   - 行 518：SCF Done:  E(RB3LYP) =  -286.605711957     A.U. after   11 cycles
   - 行 1548：Normal termination of Gaussian 16 at Thu Oct 15 19:22:31 2026.
   - 无 "Optimization completed." / "Stationary point found."；力收敛表行 1274–1279（行 1275：Maximum Force            0.000038     0.000450     YES；行 1277 Maximum Displacement 0.004793 0.001800 NO；行 1278 RMS Displacement 0.002055 0.001200 NO）
   - 12 个频率块行 802–1033
6. product_opt/product_opt.log（957）
   - 行 2083：SCF Done:  E(RB3LYP) =  -286.613531483     A.U. after    7 cycles
   - 行 2552：Normal termination of Gaussian 16 at Thu Oct 15 19:22:55 2026.
   - 行 2236：Optimization completed. ／ 行 2237：   -- Stationary point found.
7. product_frequency/product_frequency.log（958）
   - 行 534：SCF Done:  E(RB3LYP) =  -286.613531483     A.U. after   12 cycles
   - 行 1572：Normal termination of Gaussian 16 at Thu Oct 15 19:23:23 2026.
   - 行 1290：Optimization completed. ／ 行 1291：   -- Stationary point found.（力收敛表行 1284–1289，Maximum Force 0.000077 YES）
   - 12 个频率块行 818–1049

### 2.2 NI5 包日志
8. rc/job08_well_3496/job08_well_3496_optfreq.log（932，RC-A）
   - 行 6698：SCF Done:  E(RB3LYP) =  -286.605711743     A.U. after    1 cycles
   - 行 6353 / 7808：Normal termination of Gaussian 16 at Thu Oct 15 18:39:54 2026. / ... 18:40:18 2026.
   - 行 6046：Optimization completed. ／ 行 6047：   -- Stationary point found.
   - 行 138：NAtoms=     14 ...；行 117：Charge =  0 Multiplicity = 1；12 个频率块行 6982–7213
9. rc/job01_rc_optfreq/rc_optfreq_m13.log（902，加合物）
   - 行 19092：SCF Done:  E(RB3LYP) =  -286.613531375     A.U. after    1 cycles
   - 行 18749 / 20182：Normal termination of Gaussian 16 at Thu Oct 15 16:05:16 2026. / ... 16:05:36 2026.
   - 行 19856：Optimization completed. ／ 行 19857：   -- Stationary point found.（另 opt 段行 18443）
   - 行 137 / 116（NAtoms / Charge）；12 个频率块行 19376–19607
10. rc/job03_cand000/job03_cand000_optfreq.log（939，RC-B）
   - 行 22639：SCF Done:  E(RB3LYP) =  -286.610034975     A.U. after    1 cycles
   - 行 22290 / 23748：Normal termination ...；行 23414：Optimization completed. ／ 行 23415：-- Stationary point found.
   - 12 个频率块行 22923–23154
11. rc/job04_cand001/job04_cand001_optfreq.log（943）
   - 行 22700：SCF Done:  E(RB3LYP) =  -286.610034965     A.U. after    1 cycles
   - 行 22351 / 23804：Normal termination ...；行 22035：Optimization completed. ／ 行 22036：-- Stationary point found.
   - 12 个频率块行 22984–23215
12. rc/job06_cand005/job06_cand005_optfreq.log（947，RC-C）
   - 行 28768：SCF Done:  E(RB3LYP) =  -286.608664920     A.U. after    1 cycles
   - 行 28409 / 29891：Normal termination ...；行 28088：Optimization completed. ／ 行 28089：-- Stationary point found.
   - 12 个频率块行 29052–29283
13. intermediate/job02_zwitterion_optfreq/zwitterion_optfreq_m13.log（909）
   - 行 9318：SCF Done:  E(RB3LYP) =  -286.612267390     A.U. after    1 cycles
   - 行 8949 / 10456：Normal termination ...；行 8616：Optimization completed. ／ 行 8617：-- Stationary point found.
   - 12 个频率块行 9602–9833
14. ts/scan02_inner_C1N6/scan02_inner_C1N6.log（923）
   - 行 38600：SCF Done:  E(RB3LYP) =  -286.605632908     A.U. after    8 cycles（末条）
   - 行 39282：Normal termination of Gaussian 16 at Thu Oct 15 18:48:30 2026.
   - 17 个扫描点各有自己的 "   -- Stationary point found."（行 1439 / 4036 / 5485 / 6658 / 7832 / 9282 / 10455 / 11905 / 13356 / 14805 / 15979 / 17709 / 18609 / 20345 / 23211 / 25511 / 38737）
   - 扫描行：行 148  ! R4    R(1,6)                  1.6413         Scan                            !
   - 逐点收敛态能量与 R(1,6)：见 §3.4
15. seeds/spec_CH2O/spec_CH2O.log（926）：行 1659 SCF Done = -114.421603513；行 1425/2171 Normal termination；行 1282/1283 Optimization completed./Stationary point found.；频率块行 1857–1868（6 模）
16. seeds/spec_CH3NH2/spec_CH3NH2.log（935）：行 2151 SCF Done = -95.7931237609；行 1892/2878 Normal termination；行 2711/2712；频率块行 2368–2424（15 模）
17. seeds/spec_H2O/spec_H2O.log（938）：行 1495 SCF Done = -76.3655114143；行 1267/1938 Normal termination；行 1839/1840；频率块行 1685（3 模）
18. rc/job05_cand004/job05_cand004_optfreq.log（959，失败）：见 §6
19. rc/job07_cand006/job07_cand006_optfreq.log（960，失败）：见 §6

## 3 关键能量复算

### 3.1 定义
- 所有能量均为日志中"末条 SCF Done:  E(RB3LYP)"的原生值，未作任何额外加减；无 ZPE/热校正。
- 同批同程序（Gaussian 16 /home/ly/g16/g16）、同 route、同 q0/m1；不与任何 ORCA 数值相减。

### 3.2 能垒与步反应能
- ΔE‡（任务书指定口径：TS − RC-A(job08)）= (-286.604225293) − (-286.605711743) = +0.001486450 Eh = **+0.9328 kcal/mol**
- 同一 TS 减去 IRC 端点 A（job 955）= (-286.604225293) − (-286.605711957) = +0.001486664 Eh = +0.9329 kcal/mol
- 步反应能（加合物 902 − RC-A 932）= (-286.613531375) − (-286.605711743) = -0.007819632 Eh = **-4.9069 kcal/mol**
- 用 IRC 端点对（957 − 955）= (-286.613531483) − (-286.605711957) = -0.007819526 Eh = -4.9068 kcal/mol
- 端点-参考极小值的一致性：955 − 932 = -2.14e-7 Eh（-1.34e-4 kcal/mol）；957 − 902 = -1.08e-7 Eh（-6.8e-5 kcal/mol）

### 3.3 相对三分离碎片（E_sum）
- E(CH2O) = -114.421603513（926 行 1659）
- E(CH3NH2) = -95.7931237609（935 行 2151）
- E(H2O) = -76.3655114143（938 行 1495）
- E_sum = **-286.580238688 Eh**（14 原子配平；三片段各自为 0 虚频极小值，非复合物）
- E(TS) − E_sum = -0.023986605 Eh = **-15.0518 kcal/mol**
- E(RC-A) − E_sum = -0.025473055 Eh = **-15.9846 kcal/mol**
- E(加合物) − E_sum = -0.033292687 Eh = **-20.8915 kcal/mol**
- 其余加成前极小值相对 RC-A：RC-B（939）-2.7129 kcal/mol、RC-C（947）-1.8531 kcal/mol；若以 RC-B 为参考且鞍点相同：TS − RC-B = +3.6456 kcal/mol（**未测**，仅供对照）
- 909 相对 902：+0.7932 kcal/mol（同一物种另一构象）

### 3.4 scan02 内区受约束剖面（job 923，口径：'Optimization completed.' 前紧邻的 SCF Done）
| 点 | R(1,6)/Å（行号） | 收敛态 E/Eh（行号） | 相对点 1（kcal/mol） | 相对 RC-A 932（kcal/mol） | -DE/DX（行号） |
|---|---|---|---|---|---|
| 1 | 1.6413（行 1449） | -286.613531480（行 1312） | 0.0000 | -4.9070 | 0.0 |
| 2 | 1.7413（行 4046） | -286.612963147（行 3902） | +0.3566 | -4.5503 | -0.0048 |
| 3 | 1.8413（行 5496） | -286.612046074（行 5359） | +0.9321 | -3.9749 | -0.0044 |
| 4 | 1.9413（行 6669） | -286.611378810（行 6532） | +1.3508 | -3.5561 | -0.0027 |
| 5 | 2.0413（行 7843） | -286.610904177（行 7706） | +1.6487 | -3.2583 | -0.0025 |
| 6 | 2.1413（行 9293） | -286.610426688（行 9154） | +1.9483 | -2.9587 | -0.0026 |
| 7 | 2.2413（行 10466） | -286.609947490（行 10329） | +2.2490 | -2.6580 | -0.0026 |
| 8 | 2.3413（行 11916） | -286.609440581（行 11777） | +2.5671 | -2.3399 | -0.0028 |
| 9 | 2.4413（行 13367） | -286.608877838（行 13228） | +2.9202 | -1.9868 | -0.0031 |
| 10 | 2.5413（行 14816） | -286.608238410（行 14679） | +3.3215 | -1.5855 | -0.0036 |
| 11 | 2.6413（行 15990） | -286.607545769（行 15853） | +3.7561 | -1.1509 | -0.0037 |
| 12 | 2.7413（行 17720） | -286.606836898（行 17579） | +4.2009 | -0.7060 | -0.0038 |
| 13 | 2.8413（行 18620） | -286.606114383（行 18481） | +4.6543 | -0.2527 | -0.0037 |
| 14 | 2.9413（行 20356） | -286.605448503（行 20215） | +5.0721 | +0.1652 | -0.0033 |
| 15 | 3.0413（行 23222） | -286.604854217（行 23075） | +5.4451 | +0.5381 | -0.0029 |
| 16 | 3.1413（行 25522） | -286.604343399（行 25378） | **+5.7656** | **+0.8586** | -0.0025 |
| 17 | 3.2413（行 38747） | -286.605632908（行 38600） | +4.9564 | +0.0495 | +0.0012 |
- 点 1 收敛态 -286.613531480 与 902 加合物 -286.613531375 差 -1.05e-7 Eh（-6.6e-5 kcal/mol）。
- 点 17 的 -DE/DX 由负转正 ⇒ 受约束剖面的极大必落在 (3.1413, 3.2413) Å 区间内（行 25522 / 38747 原生符号）。
- 点 17 相对点 16 的回落 = -0.001289509 Eh = -0.8092 kcal/mol（二者均在原生行 25511/38736 收敛，无 NStep 超限）。
- 观测（不作判读）：TS（952）末帧的 r(C1–N6) = 3.1251 Å 在该区间之外；E(TS) − E(点 16) = +0.000118106 Eh = +0.0741 kcal/mol（TS 更高）。

### 3.5 色散项（GD3BJ）原生行（仅登记，不作判读）
| 日志 | 末个 R6Disp 行（行号） | D3(BJ) 能量/Eh |
|---|---|---|
| 932 RC-A | 行 6583 | -0.0116377174 |
| 952 TS | 行 3503 | -0.0126276620 |
| 902 加合物 | 行 18977 | -0.0153965584 |
| 909 | 行 9203 | -0.0149945209 |
| 939 RC-B | 行 22524 | -0.0135530196 |
| 947 RC-C | 行 28653 | -0.0143013910 |
- 每行 R6Disp 后紧跟原生行 "Nuclear repulsion after empirical dispersion term = ..."（例如 902 行 320/321、952 行 328/329）。
- TS − RC-A 的 D3 差 = -0.0009899446 Eh = -0.6212 kcal/mol；本页**未验证** "SCF Done 值是否已内含该 D3 项" → 列入 §8 未复核项。

## 4 0 虚频证据（频率块原生行号 + 最低频率）

| 日志 | 频率块行号范围 | 频率块行数 | 频率个数 | 最低频率/cm-1 | 虚频 |
|---|---|---|---|---|---|
| 956 reactant_frequency | 802–1033 | 12 | 36 | 35.1857（行 802） | 无（全正） |
| 958 product_frequency | 818–1049 | 12 | 36 | 98.2438（行 818） | 无（全正） |
| 932 RC-A | 6982–7213 | 12 | 36 | 35.1281（行 6982） | 无（全正） |
| 902 加合物 | 19376–19607 | 12 | 36 | 98.1897（行 19376） | 无（全正） |
| 939 RC-B | 22923–23154 | 12 | 36 | 42.3479（行 22923） | 无（全正） |
| 943（RC-B 复算） | 22984–23215 | 12 | 36 | 42.2919（行 22984） | 无（全正） |
| 947 RC-C | 29052–29283 | 12 | 36 | 69.1738（行 29052） | 无（全正） |
| 909 中间体 | 9602–9833 | 12 | 36 | 120.8575（行 9602） | 无（全正） |
| 926 CH2O | 1857–1868 | 2 | 6 | 1202.8855（行 1857） | 无（全正） |
| 935 CH3NH2 | 2368–2424 | 5 | 15 | 322.8889（行 2368） | 无（全正） |
| 938 H2O | 1685 | 1 | 3 | 1640.6810（行 1685） | 无（全正） |
| 953 TS frequency | 802–1033 | 12 | 36 | 60.9584（行 802 第 2 值） | **1 个：-164.4792（行 802 第 1 值）** |

- 953 的虚频模（log_parser，watch_pairs=[[1,6]]）：frequency = -164.4792 cm-1；heavy_atom_fraction = 0.033111926241697245；watch pair 1-6 fraction = 0.01619887164758128（pair_projection 0.16976383600416484）；top_displaced_pairs = [4,7,0.7359]、[4,8,0.7249]、[4,5,0.6644]、[3,11,0.5979]、[4,9,0.5873]。
- 953 / 956 日志中**没有** "Optimization completed." / "Stationary point found." 行（原生尾段只有力/位移收敛表：953 行 1278–1283、956 行 1274–1279）；958 有（行 1290/1291）。三个 freq 任务的力判据均为 YES，位移判据在 953/956 为 NO。
- 本页对以上日志只用 "Frequencies --" 行的符号与数值判定虚频，未做模式归属判读。

## 5 身份核验

### 5.1 组成 / 电荷 / 原子数（原生行）
- 全部 14 原子日志：NAtoms=     14（例 902 行 137、932 行 138、952 行 139；ts 链 955 行 135、956 行 125、957 行 133、958 行 125、953 行 124），Charge =  0 Multiplicity = 1（例 902 行 116、932 行 117）。
- 原子序列表（由输入/日志逐字读出，1..14）：6, 8, 1, 1, 6, 7, 1, 1, 1, 1, 1, 8, 1, 1 → **C2H9NO2**（2 C、1 N、2 O、9 H）。
- 分离组分：926 = 4 原子（C,H,H,O = CH2O）；935 = 7 原子（C,H,H,H,N,H,H = CH3NH2）；938 = 3 原子（O,H,H = H2O）。

### 5.2 键长（由各日志末个 Standard orientation 块复算，Å；原子序为 RC 输入序 1..14）
| 结构（日志） | 末块起始行 | r(C1–O2) | r(C1–N6) | r(C5–N6) | r(N6–H10) | r(N6–H11) | r(O12–H13) | r(O12–H14) | r(O2···H13) |
|---|---|---|---|---|---|---|---|---|---|
| RC-A（932） | 6546 | 1.2140（C=O） | **3.3234（未成键）** | 1.4584 | 1.0261 | 1.0209 | 0.9805 | 0.9683 | 1.8409 |
| TS（952） | 3974 | 1.2120 | **3.1251** | 1.4578 | 1.0251 | 1.0207 | 0.9798 | 0.9682 | 1.8426 |
| 端点 A（955） | 3691 | 1.2139 | 3.3229 | 1.4582 | 1.0261 | 1.0210 | 0.9805 | 0.9683 | 1.8412 |
| 加合物（902） | 18940 | 1.2970（C–O 单键） | **1.6414（已成键）** | 1.4720 | 1.0431 | 1.0245 | 1.0177 | 0.9682 | 1.5975 |
| 端点 B（957） | 2366 | 1.2970 | 1.6414 | 1.4719 | 1.0431 | 1.0245 | 1.0177 | 0.9682 | 1.5975 |
| RC-B（939） | 22487 | 1.2103 | 3.3929 | 1.4632 | 1.0221 | 1.0206 | 0.9676 | 1.0000 | 3.2714 |
| RC-C（947） | 28616 | 1.2398 | **2.0598（半成键）** | 1.4644 | 1.0218 | 1.0214 | 0.9675 | 0.9897 | 3.0117 |
| 909 中间体（自有原子序 O1,C2,N3,C4,…） | 9166 | r(C2–O1)=1.2954 | r(C2–N3)=1.6381 | r(N3–C4)=1.4700 | r(N3–H7)=1.0251 | r(N3–H8)=1.0438 | r(O12–H13)=1.0202 | r(O12–H14)=0.9682 | r(H13···O1)=1.5873 |

### 5.3 质子归属（哪个 O 上有 H、N 上几个 H）
- RC-A（932）/TS（952）/端点 A（955）：**O2 上无 H**（O2 只与 C1 成键，与 H13 的距离 1.84 Å 为氢键）；**水 O12 带 2 个 H**（0.98 / 0.97 Å）；**N6 带 2 个 H**（1.026 / 1.021 Å）→ 反应物侧 = CH2O + CH3NH2 + H2O，无质子转移。
- 加合物（902）/端点 B（957）：**C1–N6 已成键（1.641 Å）**、C1–O2 = 1.297 Å（单键）；**O2 上仍无共价 H**（O2···H13 = 1.5975 Å，同时 O12–H13 = 1.0177 Å 略被拉长）；**N6 上仍为 2 个 H**（1.0431 / 1.0245，其中 H10 与 O12 距离 1.8639 Å）→ 即两性离子 [O-]CH2[NH2+](CH3) 与 H2O 经双向氢键（O12–H13···O2、N6–H10···O12）桥连；无 N–H → O–H 质子转移。
- 909 中间体：N3 上 2 个 H（1.0251 / 1.0438）、O1 上无共价 H（H13···O1 = 1.5873 Å），C2–N3 = 1.6381 Å → 与 902 同一拓扑的另一构象。
- 片段数（按共价键计数）：RC-A/TS/955 = **3 片段**（{C1,O2,H3,H4} / {C5,N6,H7,H8,H9,H10,H11} / {O12,H13,H14}）；902/957/909 = **2 片段**（两性离子 + 水，经氢键相连）；RC-B(939) 与 RC-C(947) 亦各为 3 片段（水分别位于羰基侧/远端，见 5.2 的 r(O2···H13)/r(N6···H14)）。

### 5.4 模型原子 1..14 与题源 map 号的对应
- 题源（只读核对）：cloudra/benchmark/normal_registry/ai.py 行 116–141 的 I5 条目；行 120 mapped_reactants = [CH2:1]=[O:2].[CH3:4][N:3]([H:5])([H:6])；E1 步 = 行 127–130（out = [O-:2][CH2:1][N+:3]([H:5])([H:6])[CH3:4]，**无 barrier 键** → 契约缺省 None）；行 119 smiles_schematic: True。
- **判定 1：模型原子 1 = map1（羰基 C）成立。** 依据：902/932/952/923/955/957 全部日志的 1 号原子 Z=6，与 2 号原子（Z=8）距离 1.214（RC）/1.297（加合物）Å，并与两个 H（3、4 号）各约 1.11 Å → C=O / C–O 的羰基碳；且 1 号是全链唯一满足"map1=C 羰基碳"的原子。
- **判定 2：模型原子 6 = map3（N）成立。** 依据：6 号原子 Z=7，与 5 号（Z=6，甲基碳）1.4584 Å、与 10/11 号 H（1.0261 / 1.0209 Å）成键（胺 NH2），与 1 号原子的距离沿链 3.3234（RC-A）→ 3.1251（TS）→ 1.6414（加合物）单调缩短并最终成键 = 声明中的 "C1–N3" 成键对。权威 declare.json（ts/ts_0006，revision 75）reaction_center = [[0,5]]（0-based）= 1-based (1,6) = 模型 1 与 6，与 map1–map3 一致。
- **map4（甲基 C）= 模型 5**（C5–N6 = 1.4584 Å，C5 带 3 个 H：7/8/9 号，1.10 Å 量级）。
- **map5 / map6（N 上两个 H）= 模型 {10, 11}**（1.0261 / 1.0209 Å）。**一一对应未定**：原生日志只给坐标顺序与键长，RC-A 中两个 N–H 近等价（1.0261 vs 1.0209），本页无法仅凭几何把 map5 固定到 10 或 11（也未在题源/declare 中找到把 map5/map6 钉到具体原子序的原文）。
- **模型原子 2 = map2（羰基 O）**：Z=8，与 1 号 1.2140/1.2970 Å，RC-A 中不带 H。
- 模型原子 12（Z=8）、13/14（Z=1）= **显式接力水**；题面 schematic SMILES 不含该水（ai.py 行 119 与行 121–125 注释："接力水未画入净反应式"）。

## 6 失败作业 959 / 960（只记录终止原因原生行；能量不可引用）

### 6.1 job 959 = rc/job05_cand004/job05_cand004_optfreq.log（sha256 a19cf9ae…e675）
- 行 30932：   -- Number of steps exceeded,  NStep=  60
- 行 31218：Error termination request processed by link 9999.
- 行 31219：Error termination via Lnk1e in /home/ly/g16/l9999.exe at Thu Oct 15 19:32:37 2026.
- 全日志**无** "Normal termination"；无频率块（Frequencies -- 计数 0）；log_parser：normal_termination=false、opt_converged=false。
- 末条 SCF Done 行 30780 = -286.609163537（未收敛轨迹的中间几何）→ **不可引用**（不得作为极小值/参考态/能垒任何一项）。
- guard 日志：/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NI5/rc/job05_cand004/.cloudra/guard-959.log 末行 "数据库状态已更新: task_id=959, state=failed"。

### 6.2 job 960 = rc/job07_cand006/job07_cand006_optfreq.log（sha256 1f5c569f…f825）
- 行 29216：Error in internal coordinate system.
- 行 29217：Error termination via Lnk1e in /home/ly/g16/l103.exe at Thu Oct 15 19:32:46 2026.
- 全日志**无** "Normal termination"；无频率块；log_parser：normal_termination=false、opt_converged=null。
- 末条 SCF Done 行 29151 = -286.599707498 → **不可引用**。
- guard 日志 .../rc/job07_cand006/.cloudra/guard-960.log 末行 "state=failed"。

## 7 与 STATUS §12 一致性（逐条：声明值 vs 复算值）

| # | STATUS §12（或 §11/§3）声明 | 本页复算 | 判定 |
|---|---|---|---|
| 1 | TS E = -286.604225293 Eh（job 952，refine.log sha 8a3a3c98…） | -286.604225293 Eh（952 行 3706），sha256 8a3a3c98…055d | 一致 |
| 2 | TS r(C1···N6) = 3.125 Å | 3.1251 Å（952 末帧，块起始行 3974） | 一致（声明为截断值） |
| 3 | TS 恰 1 虚频 = -164.4792 cm-1 | 36 模、唯一虚频 -164.4792（953 行 802） | 一致 |
| 4 | heavy_atom_fraction = 0.033 | 0.033112（log_parser，watch_pairs=[[1,6]]） | 一致 |
| 5 | watch pair (1,6) 占 pair-projected 位移 1.6% | 0.016199（1.62%） | 一致 |
| 6 | IRC 原生 irc=calcfc、maxpoints=10、step 0.1 bohr、每向第 1 点停止、rx ∈ [-0.11931, +0.11932] | 行 169 / 170 / 176；Point 0→1（行 802/1230、1705）；rx 行 1252 / 1727；汇总表行 1742–1744 | 一致 |
| 7 | 端点 A（955/956）E = -286.605711957 Eh、36 模 0 虚频 | 955 行 3415；956 12 行频率块、最低 35.1857 | 一致 |
| 8 | 端点 B（957/958）E = -286.613531483 Eh、36 模 0 虚频 | 957 行 2083；958 12 行频率块、最低 98.2438 | 一致 |
| 9 | 端点 A 与 job 932 差 2.1e-7 Eh | 2.14e-7 Eh（= 1.34e-4 kcal/mol） | 一致 |
| 10 | 端点 B 与 job 902 差 1.1e-7 Eh | 1.08e-7 Eh（= 6.8e-5 kcal/mol） | 一致 |
| 11 | ΔE‡ = +0.93 kcal/mol（0.001486664 Eh） | 0.001486664 Eh = +0.9329（对 955）；对任务书指定 RC-A（job 932）= 0.001486450 Eh = **+0.9328** | 一致（两位小数）；差 ≤2e-4 kcal/mol，源于参考取 955 还是 932，**两边数字均列出** |
| 12 | 步反应能 -4.91 kcal/mol | -4.9069（902−932）；端点对 -4.9068 | 一致 |
| 13 | TS 相对三分离碎片 -15.05 | -15.0518 | 一致 |
| 14 | RC 相对三分离碎片 -15.99 | **-15.9846**（932）/ -15.9848（955） | **偏差 0.005 kcal/mol**：复算为 -15.98 |
| 15 | 加合物相对三分离碎片 -20.89 | -20.8915 | 一致 |
| 16 | RC-B -286.610034975 Eh（"jobs 939=943 同一"） | 939 = -286.610034975（行 22639）；943 = -286.610034965（行 22700）；差 1.0e-8 Eh = 6.3e-6 kcal/mol | 数值一致；"同一"在 10 位小数上不严格（列出两值） |
| 17 | RC-C -286.608664920 Eh（半成键 2.06 Å，job 947） | -286.608664920（行 28768）；r(C1–N6) = 2.0598 Å | 一致 |
| 18 | RC-B 低 2.713 / RC-C 低 1.853 kcal/mol | -2.7129 / -1.8531 | 一致 |
| 19 | 以 RC-B 为参考 ΔE‡ = +3.65（未测） | +3.6456 | 一致 |
| 20 | 内峰在 R≈3.20 Å；p16 R=3.1413 E=-286.604343399；p17 R=3.2413 回落 0.81 kcal/mol | 行 25522 / 25378 / 38747 / 38600；回落 0.8092 kcal/mol；-DE/DX 符号（行 25522 -0.0025、行 38747 +0.0012）给出极大区间 (3.1413, 3.2413) Å | 一致（"R≈3.20"落在区间内） |
| 21 | 峰高（受约束剖面）相对 902 加合物 +5.767 kcal/mol | **+5.7656**（p16 − p1，p1 = -286.613531480 行 1312；若用 902 值 -286.613531375 亦为 +5.7656） | **偏差 0.0014 kcal/mol**（复算 +5.766） |
| 22 | 峰高相对 RC 极小值 ≥ +0.859 kcal/mol | **+0.8586**（p16 − 932） | **偏差 0.0004 kcal/mol**（复算 0.8586） |
| 23 | sha256：TS 8a3a3c98…；freq 28983faf…；irc f56ea883…；902 e82ba585…；909 f50c3b80…；923 10a2b71e…d5346；902 末帧 xyz 11474dff…；932 末帧 xyz 413752ab…；923 峰帧 xyz f9db2f8c… | 9 项 sha256sum 实读**逐字一致** | 一致（**sha256 与 STATUS §12/§3 声明完全一致**） |
| 24 | §11.2 "guess = provided = scan02_peak_candidate.xyz + 923 日志" | 权威 declare.json（revision 75）guess.xyz_path = /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NI5/ts/scan04_fine_out_C1N6/scan04_last_frame.xyz，evidence_refs = .../ts/scan04_fine_out_C1N6/scan04_fine_out_C1N6.log | **叙述与现行声明不一致**（声明在后续 revision 已改用 scan04 峰帧）；scan03/scan04 原生日志不在本页审计清单 → §8 |
| 25 | （§12 未声明，本页新观测）TS 的 r(C1–N6)=3.1251 Å 落在受约束剖面推断的极大区间 (3.1413, 3.2413) Å 之外；E(TS) − E(点 16) = +0.000118106 Eh = +0.0741 kcal/mol（TS 更高） | 见 §3.4 | 仅登记，不作判读 |
| 26 | （§12 未声明，本页新登记）D3(BJ) 色散项原生行与 TS−RC-A 的 D3 差 -0.0009899446 Eh（-0.6212 kcal/mol）；"SCF Done 是否已含 D3"未验证 | 见 §3.5 | 仅登记，列入 §8 |

## 8 未复核项（明确清单）

1. ts/scan01_C1N6（job 914）、ts/scan03_fine_C1N6（job 949）、ts/scan04_fine_out_C1N6（job 950）三个扫描日志、其 .gjf 与峰帧**未复核**（本页只复核任务书清单内的 scan02/923）。已知 guard 状态：914 = failed、950 = failed、949 = done，均未在本页读原生日志。
2. ts/ts_0006/jobs/declaration_0002、declaration_0003、declaration_0004 下的 seed-opt / ts_opt 日志（937、940、942、944、946 等）**未复核**；其中 declaration_0004/ts_opt/refine.log（job 946，31163 行，末帧 r(C1–N6)=3.3159 Å）只是顺带读了一个几何量，未做完整审计。
3. 除 909 之外没有其它"加成中间体"日志；RC-B / RC-C / 909 的完整身份判读（片段划分理由、CIP/立体、与水取向的关系）**未复核**——本页对它们只给几何量与频率符号。
4. ts/ts_0006/verdict/irc_end_a.xyz（sha256 7fc97e9459bc52ac56e1d08e33ddda4c6feb6d9d458a6fc1671f5e88ade7af57）与 irc_end_b.xyz（effa287b70c0965c71c4a82f5ff0d878d66b245a69616ca85c58e9c3ac2bc850）**未复核**；IRC 端点与 TS/极小值的配对算术（管线内部 irc_path.assign_irc_endpoints 的区间证明）**未复核**；只复算了端点 opt/freq 的能量与频率。
5. ZPE / 热焓 / 自由能校正与 ΔG‡ **未复核**（本页只复算纯电子能；STATUS §12 也只声明纯电子能）。
6. **未判定** "SCF Done: E(RB3LYP) 值是否已内含 GD3BJ 色散项"（§3.5 只登记原生 R6Disp 行与差值）；未做任何验证性单点计算。
7. log_parser 的两处工具面数值**未复核**：(a) scan_peak.energy_hartree 返回 -0.60434（原生 p16 为 -286.604343399，疑字段截断）；(b) relative_to_first_point_kcal 返回 5.7668，本页由原生行复算为 5.7656（差 0.0012 kcal/mol）。
8. STATUS §12 未列出、本页未复核的其它数值：优化轨迹能量序列、Mulliken/APT 电荷、HOMO/LUMO、偶极（如 state_952.json 中的 atomcharges/moenergies）；也未复核 state_*.json 与 guard 日志的完整字段。
9. 题源其它边（NI5_E2 = 3.59、NI5_E3 = 31.2，均为旧 ORCA 值）**未复核、未参与任何相减**；本页不涉及跨程序数值。
10. .cloudra/calc-*.out.log 控制台输出与数据库行（task 表）**未复核**；本页以命名日志（.log）+ guard 日志为准。
11. 除任务书枚举到的作业号之外的重复提交/重投历史**未复核**。
12. 本页未对"是否满足验收链（恰 1 虚频模式归属 + 双向 IRC + 端点身份）"作任何裁决性判断。

## 附 复核方法（可复现）
- sha256：sha256sum <日志绝对路径>
- log_parser：对每个日志调用一次，properties 覆盖 energy / frequencies / convergence / job_type（扫描另加 scan；IRC 另加 irc）；TS 虚频另调用 watch_pairs=[[1,6]]。
- 原生行：grep -n 'SCF Done' / 'Normal termination' / 'Stationary point found' / 'Optimization completed' / 'Frequencies --' / 'Error termination' / 'Number of steps exceeded' <日志>
- 扫描逐点：awk '/Step number/{sp=$0} /SCF Done/{e=$5;l=NR} /Optimization completed/{print NR"  scfLine="l"  "e"  "sp}' <scan02 日志>
- 几何：由每个日志末个 Standard orientation 块（awk 取 NF==6 的原子行）复算原子对距离；块起始行即表中标注的行号。
- 权威状态：ts_inspect(run_id='ts_0006')（revision 75 / ended / verified / job_id 与 artifact 逐项）。
