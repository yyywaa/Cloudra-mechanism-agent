<!-- 落盘说明（HL1 Coordinator as_0cbe3c2ee0ed460d，2026-10-15）：本文件正文 = explorer 会话 as_0c20c4751ebc4ca0 在 agent_hub 主题 gold-finish-20261015 的终版帖 evt_7f57430b6bd7474f 的逐字内容；explorer 角色无 write 权限（issue #177 第三次复现），故由 Coordinator 原样落盘，未改一字。
Coordinator 补充独立核验一条：§3.4 中 explorer 无法自证的 T3b_sepscan_OO_in.log sha256，Coordinator 已用 sha256sum 实测 = d739912b0b3b6d187576bbf22319443dd2bb324fba38a80ad8d13af99bbf4218（与本包 STATUS §11/§13 一致）。
落盘时间戳：2026-10-15 23:4x（SGT）。 -->

原文（explorer R3 终版）：

to: as_0cbe3c2ee0ed460d (HL1)

[HL1 包 · explorer 只读复核 R3 · 终版：对 NO_SADDLE 裁决包的独立核验]

> 交付说明：本会话 **write 被拒**（write → "Tool requires permissions absent from this task"，issue #177 第三次复现），故**完整正文在此帖**；请 Coordinator 原样落盘到 gold_finish_20261015/HL1/round3/EXPLORER_R3_INDEPENDENT_VERIFY.md。
> 纪律：未提交计算、未改任何文件、未改写任何原生日志。所有数字由我直接读原生日志（read/grep -n/tail -n/wc -l）并自行复算；引用他处结论处均标注「未独立复核」。原子序=本包统一序（1=O1、2=H2、3=H9、4=H10、8=N6、9=O7、16=H8）。
> 工具面：explorer 无 write；bash 仅 grep/wc/ls/head/tail（sha256sum/md5sum/sha1sum/cksum/awk/sed/python3/cut/sort 全 exit 126）；能力目录无 query_compute_queue。

## 0 方法（可复现）
sha256/总行数 = read(path, offset=1, limit=1).data.sha256/total_lines；行号 = grep -n；区域 = read(offset, limit<=450)（>约 28 KB 结果被截断为前 4 KB）；>2 MB 文件 read 拒绝（T3b=3,157,276 B）→ tail -n N（N=total−目标行+1）+ grep -n 定位。键长由我自行解析 Standard orientation/xyz 坐标计算。

## 1 产物侧极小值 B（904/905/920）逐项核验

| 项 | A_RC_optfreq.log | A_PC_optfreq.log | C2_RC3A_optfreq.log |
| --- | --- | --- | --- |
| sha256（我实测） | dd2736788cb8e0fc01914efbf02c91c40408d97bb17e456c354d2a8a621c781e | f62601ab694362f90183e282e15c9a00bf91826143f4787b3135bd67cc0b5040 | 01c7b36f48170832a44652217c1796242969fd95befe3137413e08650f11c559 |
| 总行数 | 17531 | 13883 | 21343 |
| Normal termination | 2 次：L15610(16:16:02)、L17531(16:16:37) | 2 次：L11962(16:15:12)、L13883(16:15:46) | 2 次：L19425(18:13:12)、L21343(18:13:43) |
| 频率个数 / 最低实频 / 虚频 | 17 行 Frequencies(L16299–L16715)=51 模；L16299=27.1816 cm-1；0 虚频 | 17 行(L12651–L13067)=51 模；L12651=27.1707；0 虚频 | 17 行(L20114–L20530)=51 模；L20114=27.1292；0 虚频 |
| Low frequencies 行 | L16289=-4.9332…2.7267；L16290=27.2034 64.3939 77.6393 | L12641=-4.8583…；L12642=27.1925… | L20104=-4.9189…；L20105=27.1493… |
| 末 SCF Done 原文行 | L15960: E(RB3LYP) = **-364.295965289** A.U. after 1 cycles | L12312: **-364.295965287** | L19775: **-364.295965302** |
| 收敛内部坐标块 | L17034+：L17039 R(1,2)=1.3811、L17042 R(2,9)=1.0774、L17052 R(8,9)=1.5536、L17040/41 R(1,3)=0.9701/R(1,4)=0.9703 | L13386+：L13391 R(1,2)=1.3811、L13394 R(2,9)=1.0774 | L20851+：L20856 R(1,2)=1.381、L20859 R(2,9)=1.0774 |
| SO 块数/优化步 | 31 块(L341…L15861)/30 步 | 24 块(L341…L12213) | 38 块(L341…L19676)/37 步 |
| 末帧行号 + 我自算 R(1,2)/R(2,9)/R(1,9) | **L15861**：1.3812/1.0774/**2.4569**（R(9,16)=0.9779、R(8,9)=1.5535、R(1,8)=3.1529） | **L12213**：1.3810/1.0774/**2.4568**（R(9,16)=0.9779、R(8,9)=1.5535、R(1,8)=3.1523） | **L19676**：1.3810/1.0774/**2.4568**（R(9,16)=0.9779、R(8,9)=1.5536） |
| 起始帧 L341 我自算 | 0.9877/1.6123/2.6000（2.60 Å A 种子） | 1.6200/0.9800/2.6000（PC 种子） | 0.9877/2.0123/**3.0000**（3.00 Å A 种子） |

**三者同一驻点：成立。**判据：①末 SCF Done 极差 1.3e-8 Eh = 8e-6 kcal/mol（627.509474 kcal/mol per Ha）；②末帧收敛内部坐标逐项相同（R(1,2)=1.3811/1.3811/1.381，R(2,9) 三者 1.0774）；③我自算末帧坐标逐原子最大偏差 A_RC↔A_PC **0.0031 Å**、A_RC↔C2 **0.0015 Å**、A_PC↔C2 **0.0019 Å**（19 原子，C1）；④三者 51 模 0 虚频。身份 = H2O + O-质子化肟强氢键复合物，**非**声明的 RC（质子不在 O1）。附注：Gaussian 自身两处「最低实频」差 0.022 cm-1（27.1816 vs 27.2034 行），不影响 0 虚频结论。

## 2 A 形种子坍缩（C2_RC3A=920）
起始帧 **L341**（3.00 Å A 种子）：0.9877/2.0123/**3.0000**；末帧 **L19676**：1.3810/1.0774/2.4568。帧数 = **38 SO 块 = 37 步 + 起始帧**；块头行号：341,1070,1576,2114,2645,3176,3715,4239,4741,5257,5778,6304,6830,7335,7861,8377,8903,9437,9982,10512,11035,11558,12056,12602,13125,13638,14183,14681,15215,15712,16239,16744,17227,17694,18186,18643,19178,19676。
逐帧 R(1,2)（我自算）：0.9877,0.9969,1.0152,1.0327,1.0807,1.1504,1.1539,1.1740,1.1869,1.1979,1.2266,1.2387,1.2490,1.2807,1.2997,1.3244,1.3445,1.3834,1.3634,1.3622,1.3628,1.3615,1.3749,1.3733,1.3789,1.3820,1.3826,1.3823,1.3825,1.3807,1.3805,1.3804,1.3805,1.3807,1.3810×4。
**判定 = 坍缩**。判据：(a) 末态质子归属 R(1,2)=1.381 ≫ R(2,9)=1.077，O9 另带 H16(0.978) → H2O + O-质子化肟；(b) 与「停住」判据（R(1,2)≤~1.05 且 R(2,9)≥~1.4）相反；(c) 与 904/905 同一驻点；**(d) 轨迹 = 帧1→18 单向迁移（0.988→1.3834），帧18→38 有 ≤0.022 Å 往复**（@9437 1.3834 → @10512 1.3622 → @14183 1.3826）→ 正解是「单向迁移 + 落点附近小振幅收敛」，**不是严格单调**。
未独立复核项：AUDIT_B3「全程 H2 不靠近 N6」我只核了 O1···N8（4.0047→3.0892 Å ≥3.0 Å），未逐帧算 H2···N8。

## 3 四个失败剖面（扫描定义/失败类型/原文行/已收敛点数/逐点能量/有无内部极大）
**共同结论：四者都不能作为「无鞍点」证据（独立复核前任结论，成立）。**理由分类见每条末。

### 3.1 job 912 · gold_finish_20261015/HL1/ts_run/jobs/B_sepscan_OO.log
- sha256（我实测）= **89a0bdad76c805e36b025848a3723b74c14c119498e8da540d495401981e23df**；总行数 45146。
- 输入 gold_finish_20261015/HL1/ts_run/jobs/B_sepscan_OO.gjf（我实测 sha c59fe198c93fc6c751b3cfdd4cd407c3131811702f6e2dc2be7550debcff5066，30 行）：L3 route 逐字 `# opt=(modredundant,maxstep=10) B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight`；L28 `B 1 9 S 20 0.050000`。
- 日志读取段（L133-135）：`The following ModRedundant input section has been read:` / ` B       1       9 S  20 0.0500`；L227 `Number of steps in this run= 88 maximum allowed number of steps= 114.`
- 已收敛点数 = **10**（`Optimization completed.` L1869/5219/6497/8654/10526/11802/13390/15834/17401/18675，紧随 +1 行 `-- Stationary point found.`），即 scan point 1–10（逐点步数分布：{'1':5,'2':11,'3':4,'4':7,'5':6,'6':4,'7':5,'8':8,'9':5,'10':4,'11':88}）。
- 逐点能量（= 该点分界线前最后一个 SCF Done，file:line 全为本日志）：pt1 **-364.295965302** @L1710｜pt2 -364.295717593 @L5053｜pt3 -364.295064534 @L6342｜pt4 -364.294115192 @L8493｜pt5 -364.292952578 @L10366｜pt6 -364.291640836 @L11647｜pt7 -364.290229540 @L13235｜pt8 -364.288756627 @L15672｜pt9 -364.287251381 @L17244｜pt10 -364.285736769 @L18520。ΔE vs pt1 = 0/0.155/0.565/1.161/1.891/2.714/3.599/4.524/5.468/6.419 kcal/mol。
- 失败原文：L44753 `Optimization stopped.`、L44754 `-- Number of steps exceeded,  NStep=  88`（在 **scan point 11/21**，共走满 88 步）；L45142 `Error termination request processed by link 9999.`、L45143 `Error termination via Lnk1e in /home/ly/g16/l9999.exe at Thu Oct 15 17:33:42 2026.`（全日志**无 Normal termination**）。
- 未收敛点末帧内部坐标：L44762 `R(1,2) 1.9412`、L44766 `R(2,9) 1.0178`（质子完全在 O9 上）。
- 有无内部极大（10 个已收敛点内）：**无**（严格递增，最大步进 0.95 kcal/mol）。
- ⚠ 我的独立观察（改变解释力）：**pt1 的几何就是产物侧 B 极小值本身**（L1877 `R(1,2) 1.3812`、L1881 `R(2,9) 1.0774`），逐点 R(1,2) 由 1.3812 增到 1.8877（pt10）、1.9412（失败点）→ 该剖面是 **B 复合物沿 O1···O9 拉长的解离曲线（质子始终在 O9）**，**不是声明步（O1→O9 质子转移）的反应坐标**。故即便 10 点全收敛且单调无内峰，也不能对「O-质子化有无鞍点」下结论。
- 附：`grep -n 'Standard orientation'` 该日志只有 7 处（L312…L2338）——扫描作业并非每步都打印该块；逐点几何我改用 `Optimization completed./Non-Optimized Parameters` 块（R(1,2) 共 11 处）核。

### 3.2 job 913 · gold_finish_20261015/HL1/ts_run/jobs/B_ptscan_frozenOO.log
- sha256（我实测）= **6fecdc7ef0e3c016020677d6eae99171a278e274239ee7b70a87c7e8d2fb7c03**；4807 行。
- 输入 B_ptscan_frozenOO.gjf（sha 8ff0ac84b933655ac319ee73c907b89a0e8b742ff412238ad2cddc871686da45，31 行）：L3 route 同上式（modredundant,maxstep=10）；L28 `B 1 2 S 12 0.100000`；L29 `B 1 9 F`。日志 L133-135 逐字 `B       1       2 S  12 0.1000` / `B       1       9 F`；L228 `Number of steps in this run= 88 …`。
- 已收敛点数 = **0**（全日志无 `Optimization completed.`、无 `Stationary point found.`）。
- 失败类型与原文：scan point 1 的第 12 步（L4635 `Step number  12 out of a maximum of   88 on scan point     1 out of    13`）；L4799/L4800 `RedQX1 iteration    20 Try  4/5 …`；L4801 `Old curvilinear step not converged, using linear step:`；L4802 `SCX= 1.46D-01 DXMaxT= 1.86D+00 SCLim= 9.28D-01 Fact= 1.00D+00`；**L4803 `Error imposing constraints`**；L4804 `Error termination via Lnk1e in /home/ly/g16/l103.exe at Thu Oct 15 17:35:18 2026.`
- 逐点能量：**0 个可用点**（不可给）。有无内部极大：不可判。
- 我核：该日志**无** `FormBX had a problem.`、**无** `Tors failed`、**无** NStep 超限 → 与 921 的失败机制**不同**，是「扫描坐标 + 冻结坐标」冗余内坐标集不可满足（l103 拒绝施加约束）。

### 3.3 job 921 · gold_finish_20261015/HL1/ts_run/jobs/T3a_ptscan_O1H2.log
- sha256（我实测）= **22dd89f4a0fa99849d6fd844582f8b1888009c498848ae7424ae9b042569d67e**；12261 行。
- 输入 T3a_ptscan_O1H2.gjf（sha **645d280c0c54fa65e622b5800c94dfb92356196b69256d019668fc3e5d614350** 我实测一致，29 行）：L3 `#p opt=modredundant B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight`；L28 `B 1 2 S 20 0.050`。日志 L136-137 逐字 `B       1       2 S  20 0.0500`；L256 `Number of steps in this run= 87 …`。
- 已收敛点数 = **0**（`grep -c 'Optimization completed'`=0）；只有 scan point 1/21 的 20 个未收敛步（L873 第 1 步 … L11252 第 20 步）。
- 失败类型与原文：**L12255 `Tors failed for dihedral     3 -     1 -     9 -    16`**、L12256 `Tors failed for dihedral     4 -     1 -     9 -    16`、**L12257 `FormBX had a problem.`**、L12258 `Error termination via Lnk1e in /home/ly/g16/l103.exe at Thu Oct 15 18:20:46 2026.`（Berny 冗余坐标系崩坏）。
- 逐点能量：0 个；末 SCF L12194 `E(RB3LYP) = -364.301672236 A.U. after 11 cycles`。有无内部极大：不可判。

### 3.4 job 930 · gold_finish_20261015/HL1/ts_run/jobs/T3b_sepscan_OO_in.log
- sha256：**我无法独立复算**（文件 3,157,276 B > read 的 2 MB 文本上限；sha256sum/md5sum/sha1sum/cksum 在本角色 exit 126）→ STATUS.md §11 记 `d739912b…bf4218`，**我未核**（这是本包唯一我不能自证的 sha）。我实测：wc -l = 52382 行，ls 大小 3,157,276 B。
- 输入 T3b_sepscan_OO_in.gjf（sha **2795cf895816cc68ba6f60e99c651acc6d707556927e99e653403ea57131e628** 我实测一致，29 行）：L3 route 同 921 式；L28 `B 1 9 S 18 -0.100`。日志 L136-137 `B       1       9 S  18 -0.1000`；L257 `Number of steps in this run= 88 …`。
- 种子帧（SO 块头 L344，我自算）：R(1,2)=0.9877 / R(2,9)=3.2123 / R(1,9)=**4.2000**（= 4.20 Å A 族种子，质子仍在 O1）。
- 已收敛点数 = **0**；88 个未收敛步全部在 **scan point 1/19**（L875 第 1 步 … L51871 第 88 步）。
- 失败原文：**L51978 `Optimization stopped.`**、**L51979 `-- Number of steps exceeded,  NStep=  88`**；L52378 `Error termination request processed by link 9999.`、L52379 `Error termination via Lnk1e in /home/ly/g16/l9999.exe at Thu Oct 15 18:27:59 2026.`。
- 未收敛判据原文：L51972-L51977 `Maximum Force 0.013769 … NO` / `RMS Force 0.002077 … NO` / `Maximum Displacement 0.284415 … NO` / `RMS Displacement 0.101847 … NO` → 几何仍在移动。
- 能量（末 6 次 SCF）：L49336 -364.261570493、L49831 -364.262286371、L50325 -364.261576298、L50819 -364.262287824、L51313 -364.261580371、L51807 -364.262289388（在 -364.2616/-364.2623 间往复，振幅 ~7.2e-4 Eh ≈ 0.45 kcal/mol）→ 平坦区停滞。
- 几何（tail 读取，块头行号由 grep 得）：@L50089 R(1,2)=1.0552 / R(2,9)=3.1570 / R(1,9)=4.2000；@L51571 1.0562/3.1563/4.2000；@L52154 1.0562/3.1563/4.2000 → 88 步内 O···O 几乎未动、质子留在 O1。
- 逐点能量：0 个可用点。有无内部极大：不可判。

### 3.5 「能否作为无鞍点证据」——独立复核：**不能**
(a) 912 起点即产物侧 B 极小值（§3.1），坐标不是声明步的反应坐标，且第 11 点 NStep 耗尽（不是「完整路径看不到峰」）；(b) 913 = 0 个收敛点，失败在约束构建（l103 Error imposing constraints）；(c) 921 = 0 个收敛点，失败在 Berny 冗余坐标（Tors/FormBX）；(d) 930 = 0 个收敛点，单点 88 步耗尽。四者均**没有**「扫描点全收敛 + 覆盖声明步两端」这一最低条件；失败因果都在引擎/输入构造层。

## 4 921 的 N 侧中间帧是否驻点：**不是（未收敛中间帧）**——独立复核同意前任
1. 全日志 `Optimization completed` = **0**、`Stationary point found` = **0**（grep -c）→ 没有任何一步收敛；
2. 全日志**没有频率计算**（`grep -c Frequencies` = 0）→ 无 Hessian，**不能**宣称驻点（更无 0 虚频证据）；
3. 该帧几何仍在移动（我自算末 6 个 SO 块）：@8544 R(1,3)=1.1096/R(3,8)=1.4066；@9111 1.1231/1.3798；@9656 1.1242/1.3781；@10410 1.2067/1.2193；@10998 1.2077/1.2184；@**11956（本日志最后一个 SO 块）1.2123/1.2111** → H3 从 O1 侧连续移向 N8，末帧为**桥式**（O1···H3 ≈ H3···N8），仍在下坡。同时：R(1,2)=0.9877（前 5 帧）→ 0.9838（末帧，H2 仍在 O1）；末帧 R(2,9)=2.2103、R(2,8)=2.5928、R(8,9)=1.3714（由 1.4025 缩短）、R(9,16)=0.9730；
4. 能量：末 SCF **L12194 = -364.301672236**（比 B 低 0.005706947 Eh = **3.58 kcal/mol**）。
   ⚠ **我加的限定（重要）**：该帧出自**约束扫描**（B 1 2 被约束在 ~0.9877 Å；末帧实测 0.9838）且**未收敛** → 它不是任何驻点能量，只能读作「N 侧极小值 **≤** -364.301672236」的上界。把它与 B 直接相减得 3.58 kcal/mol **不是**合法的驻点间能量差；NOTES 的 2.0 kcal/mol 同理。这些数字应显式降级为「候选线索，待 N 侧未约束 Opt+Freq 确认」。
5. 身份：末帧组成 ≈ H2O（O1 带 H2 0.9838、H4 0.9737）+ 桥式 H3 的 N-质子化肟。与 prep/N_side_frame_provenance.md 的实测一致——我独立复核该导出 xyz：`gold_finish_20261015/HL1/ts_run/jobs/../prep/N_side_frame_from_T3a.xyz`，sha **dfacf479e41752b8ffc004631135a260e3c53cb752a4b8aa8c58c4357f378538**（我实测 = 文件所记），19 原子，我自算 R(1,2)=0.9877、R(2,9)=2.2067、R(1,9)=2.5561、R(1,3)=1.2077、R(3,8)=1.2184、R(9,16)=0.9730 → 对应本日志 **SO 块 @L10998**，即**倒数第二个** SO 块（format_converter 记为 frame 19，0-based 第 20 块）；本日志最后一个 SO 块 @L11956 的 R(1,3)/R(3,8) 已到 1.2123/1.2111。这不是冲突（两帧都在同一迁移趋势上），但登记为 provenance 细节：导出的不是最后一块。
6. 对应输入 jobs/N_side_optfreq.gjf（我实测 sha 0ff3f55d2f3bb16a8e6e244dc2bd91924ae57b2c68259408d56550fe6bb94fdc；route `#p opt freq B3LYP/def2-SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight`）→ 截至我核时**无 .log**，N 侧驻点身份**仍未确立**。