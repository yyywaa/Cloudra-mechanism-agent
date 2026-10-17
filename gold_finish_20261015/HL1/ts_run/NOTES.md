# HL1_E1 计算运行记录（small_mol owner）

工作目录：/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HL1/ts_run/
方法（全线统一）：Gaussian 16；B3LYP/def2SVP + EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight；气相；q=+1,m=1。
资源：新作业按主协调 16:35/16:47 政策用 %nproc=8 / %mem=10GB（旧 12c/13GB 的 A_* 已跑完，不再重投）。

## 原子序（本包所有文件统一，1-based）
1=O1(H3O+ 的 O)、2=H2(转移质子)、3=H9、4=H10、5=C11(乙基 CH3)、6=C5(CH2)、7=C4、8=N6、9=O7(肟 O)、10=C3(甲基)、11-13=H(C11)、14-15=H(C5)、16=H8(肟 OH 的 H)、17-19=H(C3)。
↔ 题面 mapped SMILES：本序 1↔1、2↔2、3↔9、4↔10、5↔11、6↔5、7↔4、8↔6、9↔7、10↔3、16↔8。反应中心：本序 break [1,2] / form [2,9] ≡ 题面 [[1,2]] / [[2,7]]。

## 作业台账（以 query_compute_queue 的实际归属为准）
| job | 输入 | 状态 | 结果 / 备注 |
|---|---|---|---|
| 904 | jobs/A_RC_optfreq.gjf（12c） | done 16:16 | 正常结束、opt 收敛、51 modes、0 虚频；E=-364.295965289；末帧=共享质子复合物（H2-O7 1.077、O1-H2 1.381、O1···O7 2.457、N6-O7 1.554） |
| 905 | jobs/A_PC_optfreq.gjf（12c） | done 16:15 | 同上，E=-364.295965287；与 904 末帧逐原子最大偏差 0.003 Å（同一极小值） |
| 912 | jobs/B_sepscan_OO.gjf（12c） | **failed 17:33** | 松弛扫描 d(O1···O7) 2.457→3.457（20×0.05，21 点）：前 10 点收敛、逐点单调上坡；第 11 点（2.957 Å）走满 88 步 → l9999 Error termination（平坦区收敛停滞）。日志 sha256 89a0bdad76c805e36b025848a3723b74c14c119498e8da540d495401981e23df |
| 913 | jobs/B_ptscan_frozenOO.gjf（12c） | **failed 17:35** | `B 1 2 S 12 0.1` + 冻结 `B 1 9 F`：scan point 1 第 12 步 l103 "Error imposing constraints"，**零个可用点**（输入设计问题：扫描坐标+冻结坐标冗余）。日志 sha256 6fecdc7ef0e3c016020677d6eae99171a278e274239ee7b70a87c7e8d2fb7c03 |
| 920 | jobs/C2_RC3A_optfreq.gjf（8c/10GB） | done 18:13 | **T1 结论=滑落**：3.00 Å 松态 A 种子未约束 Opt 收敛到与 904/905 完全相同的驻点（E=-364.295965302、51 modes、0 虚频、Normal termination）；末帧 R(1,2)=1.381、R(2,9)=1.077、R(1,9)=2.457、R(2,8)=2.073 Å。日志 sha256 见下表 |
| 921 | jobs/T3a_ptscan_O1H2.gjf（8c/10GB） | running 18:05→ | T3a 主 PT 剖面（松弛扫描 d(O1-H2) 0.988→2.088，20×0.05，不冻结任何坐标） |
| 930 | jobs/T3b_sepscan_OO_in.gjf（8c/10GB） | running 18:15→ | T3b 长程剖面（松弛扫描 d(O1···O9) 4.200→2.400，18×−0.100，由外向内，种子 prep/RC_42A_seed.xyz） |
| — | jobs/C2_sideN_optfreq.gjf（8c） | 未提交 | （可选通道，被 T3d 取代） |
| — | jobs/C2_sideN_optfreq.gjf（8c） | 同上 | 同上 |
| — | jobs/E2_RCbi / E2_assem / E2_RC35A / E2_RC42A / E2_H3O / E2_oxime（8c） | 已生成，待放行 | 平台锁解除后按 C2_RC3A → 3.5/4.2 Å → 双齿 → 单体 顺序提 |

sha256：A_RC_optfreq.log dd2736788cb8e0fc01914efbf02c91c40408d97bb17e456c354d2a8a621c781e；A_PC_optfreq.log f62601ab694362f90183e282e15c9a00bf91826143f4787b3135bd67cc0b5040。

## 种子（构造脚本 + 几何，全部 1-based 本序）
- prep/csearch_RC2/guided_assembly/assembly/complex_candidate_000.xyz：conformer_search（mapped RC SMILES, q=1, rdkit, filters 2-9∈[1.3,2.7]/1-9∈[2.2,3.4]/2-8≥2.45）→ MMFF 预组织络合物（N/O 桥式）。
- prep/RC_seedB.xyz：刚体旋转 H3O+ 到 O7 面内孤对方向（anti N6）：O1-O7 2.600、H2-O7 1.612、H2-N6 2.700、O1-N6 3.622。
- prep/PC_seedB.xyz：同序，H2 置 O7 上 0.98。
- prep/RC_3A_seed.xyz / RC_35A_seed.xyz / RC_42A_seed.xyz：O1···O7 = 3.00 / 3.50 / 4.20，质子仍在 O1 上（单齿 A 种子族）。
- prep/RC_bi_seed.xyz：双齿螯合种子（H2-O7 1.622、H2-N6 1.744、O1-N6 2.505、O1-O7 2.610）。
- prep/monomer_H3O.xyz / monomer_oximeE.xyz：分离参考。

## 状态（区分观察/假设；不使用历史值）
- 观察：O-专一单齿姿态（O1···O7=2.60，质子仍在 O1）无约束优化**自发把质子转到 O7**，落到与产物起点相同的极小值（同一驻点）。→ 该距离下 A 形（质子留 O1）不是极小值。
- 假设 H1：A 阱在更长 O···O（3.0/3.5/4.2）或双齿螯合姿态下存在 → 待 C2_RC3A / E2_RC35A / E2_RC42A / E2_RCbi / E2_assem。
- 假设 H2：本级别气相单阱、无一阶鞍点 → 需要 (a) 多个 A 种子全坍缩、(b) 912/913 剖面无内部极大、(c) B 极小值身份+0 虚频、(d) ts_prepare 无鞍点记录。
- 未取：TS、IRC、ΔE‡、N 侧极小值（C2_sideN 被平台锁挡下，且主协调已降级为可选）。
- 平台状态：compute.db 写锁已解除（18:05 起成功提交 920/921/930）；仍遵守本包同刻 ≤2 个 QM 作业。

## 续做状态（2026-10-15 18:15 起，计算 owner）
- **T1 已判（job 920）**：3.00 Å 松态 A 种子未约束 Opt+Freq **滑落**到与 904/905 完全相同的驻点
  （E=-364.295965302 Eh，51 modes、0 虚频、Normal termination；末帧 R(1,2)=1.381、R(2,9)=1.077、R(1,9)=2.457、R(2,8)=2.073 Å）。
  → 3.00 Å 下 A 形（质子留 O1）仍不是极小值。日志 sha256 与逐条证据见下方「T1 原生日志」。
- **T3 设计与失败点逐项证据**：见 ts_run/T3_SCAN_DESIGN.md（sha256 d6f5a28814dfffa9b108c8eb6c28242c31c4da4ba2b172616967f3b93daa9ac7）。
- 观察（未定论，勿当结论）：T3a（job 921）scan point 1 把 d(O1-H2) 约束在 0.988 Å 时，中间帧出现
  **H3→N8 转移**（r(O1-H3)=1.124、r(H3-N8)=1.378、r(H16-O9)=0.972 Å），E 到 −364.29916 Eh，
  比 O-侧复合物（−364.29597）低约 2.0 kcal/mol → 提示可能存在更低的 **N-质子化复合物**通道；
  待 point 1 收敛后用该几何单独跑未约束 Opt+Freq 才能确认（尚未做）。
  该观察同时说明：只扫 d(O1-H2) 无法完全封锁其它质子通道（设计局限，已在 T3 设计文件记录）。
- 假设 H1 的现状：2.60 Å（904/905）与 3.00 Å（920）两代 A 种子均坍缩；3.5/4.2/双齿 待 E2_*（T2）。
- 待做：T3a/T3b（运行中）、T3c/T3d/T3e 扫描、T2（E2_RC35A/E2_RC42A/E2_RCbi + 单体参考）、T4 ts_prepare。
