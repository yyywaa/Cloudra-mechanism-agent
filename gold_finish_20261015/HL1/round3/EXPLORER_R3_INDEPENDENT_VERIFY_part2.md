<!-- 落盘说明（HL1 Coordinator as_0cbe3c2ee0ed460d，2026-10-15）：本文件正文 = explorer 会话 as_0c20c4751ebc4ca0 在 agent_hub 主题 gold-finish-20261015 的终版续帖 evt_74ecf69f2b3c48d3（§5–§10）逐字内容；其 §0–§4 见同目录 EXPLORER_R3_INDEPENDENT_VERIFY.md（正文 = 帖 evt_7f57430b6bd7474f）。explorer 无 write 权限，由 Coordinator 原样落盘，未改一字。 -->

to: as_0cbe3c2ee0ed460d (HL1)

[HL1 包 · explorer 只读复核 R3 · 终版 · 续（§5–§10）]（上一帖 evt_7f57430b6bd7474f 为 §0–§4）

## 5 搜索充分性清单（逐条给输入文件路径 + route/扫描行 + 是否真跑）

### 5.1 A 形（质子留 O1）未约束 Opt+Freq 种子族
| # | 输入 | route/种子 | 是否运行（日志） | 结局 |
| --- | --- | --- | --- | --- |
| 1 | gold_finish_20261015/HL1/ts_run/jobs/A_RC_optfreq.gjf（sha 我实测 339108576666454a6eadaa583aff77ee1a66a1db480920756ed61dce06c142ac；A_PC_optfreq.gjf = 239bad2a8832713ba86c9d609294ffd46a564b56f854e20fa8d72ba8a3f1ee77） | `#p opt freq B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight`；2.60 Å 单齿 / PC 种子 | 904（dd273678…）、905（f62601ab…） | **坍缩到 B** |
| 2 | jobs/C2_RC3A_optfreq.gjf（sha f10a2c7a1bce3a744d8b8db2441cd9df0a0c07071c0fedc457cc8645fcbc00e8） | 3.00 Å A 种子 | 920（01c7b36f…） | **坍缩到 B**（§2） |
| 3 | jobs/E2_RC35A_optfreq.gjf（sha 5748a44528e2a8680c31196100c3eab4bf298a7fda2a5c473ea190f80832cd17） | 3.50 Å A 种子（起始帧 @L341 我自算 R(1,9)=3.5000、R(2,9)=2.5123、R(1,2)=0.9877） | **965**（E2_RC35A_optfreq.log，sha **48da3dcb0ca8e2bce3e9e3d67a15bf7d46bb6abcc963b0296b1499776302a384**，29346 行；2×Normal termination L29346=23:19:45；L28850 Stationary point found；51 模、Low freq L28103/28104、最低实频 27.5308、0 虚频；末 SCF L27774 = **-364.295777129**） | **坍缩**，落到**第二个** O-质子化极小值 B'（末帧 @L27675：R(1,2)=1.3878/R(2,9)=1.0740/R(1,9)=2.4601），比 B 高 0.000188173 Eh = **0.118 kcal/mol** |
| 4 | jobs/E2_RCbi_optfreq.gjf（sha 6ab9b94e67c7f9c18b020149f1a86ab74965e506617f5da04b62eabc013b7670） | 双齿螯合（起始帧 @L347 我自算 R(2,9)=1.6223、R(1,9)=2.6100；种子 RC_bi_seed.xyz sha 3874b0eeb18752dd471ecd043e63d02c96729bddc16f1a523b5203d579731319） | **966**（E2_RCbi_optfreq.log，sha **a4d182472ff195ac8c1e6bbc3a2c5a57e8daa67b29a45fee470c4a235d6e0dcf**，32706 行；2×Normal termination L32706=23:20:28；51 模 0 虚频，最低实频 27.1012；末 SCF L31128 = **-364.295965301**） | **坍缩到 B**（末帧 @L31029：1.3811/1.0774/2.4568） |
| 5 | jobs/E2_RC42A_optfreq.gjf（sha ec9dcdc5e1b285e66fe73fec30a31439be5c15c9e95abaf5a89a451d496a0ac9） | 4.20 Å A 种子 | **从未运行（无 .log）** | 缺口 |
| 6 | 已建未跑（均无 .log）：jobs/RC_seedB_optfreq.gjf、PC_seedB_optfreq.gjf、C_RC3A_optfreq.gjf、C2_sideN_optfreq.gjf、C_sideN_optfreq.gjf、E2_assem_optfreq.gjf、E2_H3O_optfreq.gjf、E2_oxime_optfreq.gjf、D_H3O_optfreq.gjf、D_oxime_optfreq.gjf、N_side_optfreq.gjf，以及 jobs/probe_2.gjf（route `#p scan …`，L28 `B 1 9 S 20 0.05`） | — | 无 | 缺口 |

### 5.2 剖面通道
| # | 输入 | 扫描定义（.gjf 原文 / 日志回显） | 是否运行 | 结局 |
| --- | --- | --- | --- | --- |
| 7 | jobs/B_sepscan_OO.gjf | `B 1 9 S 20 0.050000`（2.457→3.457，21 点） | 912 | 10 点收敛、单调上坡无内峰；第 11 点 l9999（§3.1） |
| 8 | jobs/T3b_sepscan_OO_in.gjf | `B 1 9 S 18 -0.100`（4.200→2.400，19 点，外向→内向） | 930 | scan point 1 走满 88 步 l9999，0 点（§3.4） |
| 9 | jobs/T3a_ptscan_O1H2.gjf | `B 1 2 S 20 0.050`（0.988→2.088，21 点，不冻任何坐标） | 921 | scan point 1 第 20 步 l103 FormBX，0 点（§3.3） |
| 10 | jobs/B_ptscan_frozenOO.gjf | `B 1 2 S 12 0.100000` + `B 1 9 F`（且冻 O···O=3.00） | 913 | scan point 1 第 12 步 l103 Error imposing constraints，0 点（§3.2） |
| 11 | jobs/T3b_sepscan_OO_long.gjf | `B 1 9 S 25 0.100`（2.457→4.957，未提交草稿） | 无 | 被 912 第 11 点停滞取代（设计文件自述） |
| 12 | 已建未跑（均无 .log）：jobs/T3c_revscan_H2O9.gjf（`B 2 9 S 25 0.100`，反向单坐标 H2–O9）、jobs/T3d_scan_H2N8.gjf（`B 2 8 S 16 -0.125`，N 侧受体）、jobs/T3e_scan_H3O9.gjf（`B 3 9 S 16 -0.150`，H3O+ 的另一个 H） | — | 无 | **缺口：两条替代 PT 通道与反向剖面均只有输入** |

### 5.3 TS 搜索（T4）
13. **截至我核时（23:5x），project ts/ 下 ts_0001–ts_0009 中没有任何 run 提到 HL1**（`grep -rl HL1 ts/ts_0007 ts/ts_0008 ts/ts_0009` 无命中；ts_0007/declare.json 我实读为 NY3：reactant `[Na+].[OH-].COC=O`）→ **HL1 的 ts_prepare 尚未落盘，T4 未开始**。已备好材料：ts_run/t4_interp/img_00..08.xyz（9 帧 IDPP）+ prep/TS1_guess_provenance.md（sha 6aaf09e1…）+ round3/T4_INPUT_ORDER_PROVENANCE.md（sha a97f0467…）。我独立复核 guess：`gold_finish_20261015/HL1/ts_run/jobs/../t4_interp/img_06.xyz` sha **99749b1630e3e654e1523df8cc9726134bfe58b42d59a948082dd1563110fe2d**（= 文件所记），19 原子、元素序 O,H,H,H,C,C,C,N,O,C,H×9，我自算 R(1,2)=**1.2804**、R(2,9)=**1.3061**、R(1,9)=2.5836、R(2,8)=2.3191、R(9,16)=0.9784（与 provenance 一致）。
14. 我核：jobs/.cloudra 下最新为 calc-965/calc-966（= E2_RC35A/E2_RCbi，均已 done），**无 calc-967+ 锁**→ 无其它在飞作业痕迹（但本角色无 query_compute_queue，无法正面核队列）。

**搜索充分性结论**：O1–H2/O1···O9 通道的 A 形极小值搜索已在 2.60 / 3.00 / 3.50 Å 与双齿共 **4 个独立种子**上全部坍缩（每例均 Normal termination + 51 模 0 虚频），但 (i) 4.20 Å 未跑、(ii) 两条替代 PT 通道（H2→N8、H3→O9）与反向剖面（H2–O9）只有输入无结果、(iii) **一次真实 TS 搜索都没做** → **搜索尚未穷尽**，因此现在**还不能**宣布「无鞍点」；这也正是「912/913 不能当证据」的正确外延。

## 6 与前三次只读复核（AUDIT.md / AUDIT_B2.md / AUDIT_B3.md）的异同
**一致（我独立复算通过）**：AUDIT.md/AUDIT_B2.md 的 A_RC/A_PC 末 SCF（-364.295965289/-364.295965287）、51 模 0 虚频（min 27.1816/27.1707）、末帧 R(1,2)=1.3812/1.381、R(2,9)=1.0774、R(1,9)=2.4569/2.4568、R(8,9)=1.5535，「两者同一驻点」——全部一致（我另给逐原子 maxdev 0.0031 Å）。AUDIT_B3.md 的帧↔行号映射（341/1055/1569/2087/2630/…/15861）与我的 SO 行号表一致；抽样数值一致（341:0.988/1.612/2.600；2630:1.168 vs 我 1.1677；11013:1.378 vs 我 1.3778；15861:1.381/1.077/2.457）。
AUDIT_B2.md §2 的「912/913 在文件系统里不存在、别当在跑」是 16:5x 的正确快照；两作业随后 17:33/17:35 真实运行并以 l9999/l103 失败（§3.1/§3.2）→ 属**时间差**，不是结论冲突。
**不同/需更正**：
1. **AUDIT_B3 的「逐帧单调」表述过强**。我实测：A_RC 的 R(2,9) 帧5(@2630)=1.1791 → 帧7(@3684)=1.2069 回升；R(8,9) 1.4025→1.4282→1.4541→1.4679→1.4668→1.4617→… 有回落；C2_RC3A 的 R(1,2) 帧18(@9437)=1.3834 → 帧20(@10512)=1.3622 回落。正确表述 = **「单向迁移 + 落点附近 ≤0.02 Å 往复、无中途驻留」**。
2. AUDIT_B3 的「O9–N8 单调拉长到 1.554 Å」应改为「总体拉长（1.403→1.554），中间有 1.462–1.468 Å 的非单调小回落」。
3. AUDIT_B3 的「全程没有任何一帧 H2 靠近 N6」**我未独立复核**（只核 O1···N8 = 4.005→3.089 Å ≥3.0 Å）→ 标为「未独立复核」。
4. AUDIT.md/AUDIT_B2.md 未涵盖 912 的**关键结构事实**：912 的 pt1 本身就是产物侧 B 极小值（L1877/1881：R(1,2)=1.3812、R(2,9)=1.0774）→ 该剖面是 B 的解离曲线而非声明步坐标。这条把 912 的解释力从「覆盖区间不足（只到 2.96 Å）」进一步降为「**坐标选错**」。
5. STATUS/NOTES 把 921 中间帧的 -364.301672236 与 B 直接相减得 3.6/2.0 kcal/mol——按 §4.4 应降级为「候选线索（约束 + 未收敛帧的上界）」。

## 7 支持 / 反对改机理的证据（Coordinator 追加要求；只给证据与缺口，不下裁定）
**支持「参考态重定 / 机理修订」**
(a) **声明的 RC（质子留 O1 的 O-侧络合物）在本级别气相不是极小值**：5 个独立起点（2.60 Å 单齿、3.00 Å、3.50 Å、双齿螯合、以及产物种子）无约束 Opt+Freq **全部坍缩**（§1/§2/§5.1；每例 Normal termination + 51 模 0 虚频）。
(b) 产物侧**不是单点**：存在两个 0 虚频 O-质子化极小值 —— B = -364.295965289/-287/-302（三日志同一驻点）与 B' = -364.295777129（3.50 Å 种子落点，比 B 高 0.118 kcal/mol，51 模 0 虚频）。机理/参考态描述必须写清用哪一个。
(c) N 侧候选（H3 桥 O1/N8 的中间帧）在**能量上至多**比 B 低 3.58 kcal/mol（但见 §4.4 限定），且几何上 H3 确实在向 N8 迁移（R(3,8) 1.4066→1.2111 连续 6 帧降）、R(8,9) 由 1.4025 缩到 1.3714（N–O 变短）→ 与「O-质子化活化 N–O 断裂」方向相反，属**另一条通道**（N-质子化），支持把它登记为独立节点/边（并说明它不是 Beckmann 离去基活化态、不导向迁移）。
**反对「现在就改判为 N 侧 / 现在就宣布无鞍点」**
(d) N 侧只有 **1 个未收敛、且受约束**的帧：无频率、无 0 虚频、无端点身份（jobs/N_side_optfreq.gjf 尚未运行）→ §7(c) 的数字**不足以**支撑「N 侧更优」的机理结论。
(e) 没有任何一条剖面对声明步是「两端完整 + 全收敛」（§3.5）；没有 IRC 双向；没有 ts_prepare 记录 → 「无独立鞍点」目前只有**必要条件**的部分证据，**没有充分证据**。
(f) 912（唯一 10 点收敛的剖面）因起点即 B，**不针对**声明步 → 不能用来论证「无垒 PT」。
**「无独立鞍点」若最终成立，需要的替代口径证据（缺口清单）**
1. ts_prepare 至少一次真实搜索（provided guess = 质子居中帧，如 img_06），留 run_id/process.json/result.outcome 原文（含「无候选/无峰」的原文）；端点必须用**实测极小值**并登记 job/日志/sha；
2. 声明步的**反应坐标**剖面：改用质子转移进度坐标（如 ΔR = R(O1–H2) − R(O9–H2)）或「分段短扫 + 逐点冻结 O···O / 逐点独立作业」，以避开 913/921 的冗余坐标崩坏；起点须是 B 的共轭方向或 A 形种子；
3. 至少一条**反面**通道跑完（H2→N8 或 H3→O9），否则「无鞍点」只对一条坐标成立；
4. 4.20 Å 与更远（如 4.96 Å 长程）的未约束 Opt+Freq 或长程剖面，排除更长距离处出现 A 形阱；
5. 替代口径的定量表述（「前平衡/无垒离子–分子 PT」的参考态=哪个几何、ΔE 记什么、与 B/B' 的电子能差），并解释为何不是「零的猜测值」；
6. 若走「改图」，N 侧通道必须先有 0 虚频 + 频率 + 身份（质子/CIP/碎片数）核验，并说明对 E2（N–O 断裂/乙基迁移）的影响面。

## 8 验收链缺口清单（逐条标注当前满足与否）
| 验收项 | 状态 | 依据 |
| --- | --- | --- |
| TS 恰好 1 虚频 + 模式归属 watch pair | **不满足**（本包不存在任何 OptTS/IRC 日志；ts/ 下无 HL1 run） | §5.3 |
| IRC 双向到声明的两个端点 | **不满足**（同上） | — |
| 两端点 Opt+Freq 0 虚频 + 身份核验 | **部分满足**：产物侧 B/B' 已 0 虚频 + 身份成立（§1/§5.1）；「反应物端」对应的 RC 极小值**不存在/未取得**（4 个 A 形种子全坍缩）→ 没有第二个端点 | §1/§2/§5.1 |
| 能垒 = 纯电子能差（相对本步起点极小值） | **不满足**（无 TS ⇒ 不能给；任何现有数字（0 点帧/未收敛帧）都不是合格 ΔE‡） | §3/§4 |
| 原生日志不改写 + 路径 + sha256 + 行号 | **满足（有限制）**：本包日志我按只读读取、未改动；A_RC/A_PC/C2/E2_RC35A/E2_RCbi 的 sha256 我独立复算一致；**930 的 sha256 我无法复算**（>2 MB + 本角色无哈希命令）→ 该一条为「仅 Coordinator 记录、未第二人复核」 | §0/§3.4 |
| 回填题源 + 重生成题面 + 守卫测试 | **未做**（registry/jl.py 与题面本轮 0 改动；本会话亦未提交 git） | — |

## 9 工具面缺口（只读，供 issue 参考）
1. explorer 无 write（本轮再次复现）；bash 仅 grep/wc/ls/head/tail（sha256sum/md5sum/sha1sum/cksum/awk/sed/python3/cut/sort 全 exit 126）→ **>2 MB 的日志在本角色无法自算 sha256**（930 即受影响）。建议开放 `sha256sum`（或 read 支持大文件哈希/流式）。
2. 能力目录无 `query_compute_queue` → explorer 无法核队列余量/在飞作业，只能靠 .cloudra 锁文件推断。
3. `read` 与 `bash` 的截断行为需在文档里写明：单结果 >约 28 KB 时只回前 ~4 KB（read 附 "Full output at .cloudra/tool_output/..."，bash 只回前 4000 字符）→ 大日志复核只能靠「grep -n 定位 + tail -n N 取窗口」的组合（本报告即如此完成）。

## 10 本轮顺带独立核验的新产物（R3 owner 23:19–23:30 产出）
1. jobs/E2_RC35A_optfreq.log 与 jobs/E2_RCbi_optfreq.log：sha256 分别为 **48da3dcb0ca8e2bce3e9e3d67a15bf7d46bb6abcc963b0296b1499776302a384**（29346 行）与 **a4d182472ff195ac8c1e6bbc3a2c5a57e8daa67b29a45fee470c4a235d6e0dcf**（32706 行）；均 2×Normal termination、51 模、**0 虚频**（最低实频 27.5308 / 27.1012）、末 SCF -364.295777129 / -364.295965301、末帧 R(1,2)/R(2,9)/R(1,9) = 1.3878/1.0740/2.4601 与 1.3811/1.0774/2.4568（我自算，分别 @L27675 / @L31029）。→ 3.50 Å 与双齿种子**都坍缩**，双齿直接落回 B，3.50 Å 落到 B'（+0.118 kcal/mol）。
2. round3/T4_INPUT_ORDER_PROVENANCE.md 的「product endpoint seed」置换：我独立核验 `gold_finish_20261015/HL1/ts_run/jobs/A_RC_last.xyz`（sha 303ec8b48b90fdb1369e31e5eb667b1d222098e29a87a91f11ff6598ffb5afe6，19 原子）与 `gold_finish_20261015/HL1/round3/product_endpoint_seed_B_prodorder.xyz`（sha 5b03a2ea2f136a59a08817b805733d188a9ded29213cea5695097f0a34a20fc6），按文件所声明的置换 `[1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,2,17,18,19]` 逐行比对：**坐标最大偏差 = 0.000e+0 Å、元素序列一致** → 「只做行置换、未改坐标」成立；置换后按 product 序读出的相关距离正确：O1–H2(new16)=1.3812、O9(new8)–H2=1.0774、O9–H8(new15)=0.9779、O1···O9=2.4569。
3. prep/N_side_frame_from_T3a.xyz（sha dfacf479…，见 §4.5）与 jobs/N_side_optfreq.gjf（sha 0ff3f55d…）核验一致，但该 Opt+Freq **尚未运行**。

（本节所有 sha256/行号/几何均为我本轮实读实算；未改动任何文件；未下任何化学裁定——改图/记 0/豁免由 HL1 Coordinator 汇总处理。）