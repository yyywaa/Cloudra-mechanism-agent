# HL1_E1 端点复核清单（本 lane 内部作业规范，2026-10-18）

来源：与 coordinator 逐条确认的口径（本文件只是防压缩失效的落盘副本，不替代其裁决）。


> **限定语（全局）**：本文件出现的所有数值阈值均为**约定阈值（自设，非文献界、非统计界）**，未经实测分布检验；引用时必须带这层限定。
>
> **边界**：本文件只是本 lane 的内部作业规范，**不替代 coordinator 裁决**；涉及「该边是否可算 / 是否回填 0.0 口径」的判断一律报 coordinator 并留证据路径。

## 0. 数据来源与只读边界
- IRC 源：`ts/ts_0022/jobs/declaration_0004/irc/irc.log`，sha256 `b2f2974677120745f1e060dcb286a7ce524749f1c96d0a4eaa39903212e741c8`，Normal termination @ L9413。
- ts_0022 目录一律只读；不写其文件、不改 run 状态、不撤不抢。
- #1100 = 平台 reactant_opt（种子 = IRC REV pt10 帧，RMS 0.000）；#1101 = 我的 rev_outer Opt（同种子、同方法、同资源 ⇒ 重复），**仅作复现证据，不单独计入**，不得用于新建结论。

## 1. 取帧三级核对（硬/软判据）
1. 硬：`grep -n "Path Number"` 定位路径号+步号，与工具注释 `point=… path=…`、以及 `Summary of reaction path following` 的带符号 RxCoord 侧别三者自洽。
2. 软：改用**相对能**与 summary 表比（以起点 −364.290279158 为零点），1e-5 Eh 内一致；差到 1e-4 才判"取错帧"。绝对能第 6–7 位差异属打印精度，不报警。
3. 坑：`format_converter(log→xyz)` 的 "final frame" = Path 1 末点，**不是**日志末尾帧。

## 2. 主/辅判据（阈值均为约定阈值：自设，非文献界/非统计界）
- 主（分类只用这四个）：H2 归属（H2–O1 vs H2–O9）、H4 归属（O1–H4 vs H4–N8）。
- 辅：O1···O9 三档**自设约定阈值**（≤2.6 接触离子对 / 2.6–3.5 松散 / >3.5 分离），非文献界、非统计界，只作补充描述。
- 阈值（自设）：H4–N8>1.3 且 H2 转移完成 ⇒ 真转移；O1–H4 保持 ~1.0 且 H4–N8 1.7–2.0 ⇒ 仅氢键（该端即反应物侧）；H4–N8<1.15 且 O1–H4>1.3 ⇒ N-质子化。

## 3. 参照几何（只作身份比对，不跨批次相减）
- B = −364.295965289（O-质子化产物，属 FWD 侧）：O1–H2 1.3812、H2–O9 1.0774、O1–H4 0.9703、H4–N8 3.2842、O9–H16 0.9779。
- job 978 = −364.326887674（N-质子化肟+水，另一程序批次，仅几何参照）。
- 反应物侧参照：RC_3A_seed、#1100 落点。

## 4. 每个端点必须报的字段
- Opt：末次收敛表行号 + Max Force / RMS Force / Max Displacement / RMS Displacement 与 YES/NO；"Stationary point found" 行号；Normal termination 行号。
- **Freq 能量与 Opt 末帧能量一致性**：差 <1e-6 Ha；不一致 ⇒ 先查 Freq 用的几何，不得直接把 Freq 能量当极小能量。
- Freq：虚频个数 + 最低模数值；0 虚频 ⇒ 本级别极小；有虚频 ⇒ 只写"该端未达极小"，不给分类、不给 ΔE‡。
- 键长全表：O1–H2 / H2–O9 / O1–H4 / H4–N8（主）+ O1–H3 / H2–N8 / O9–H16 / O1···O9（辅）。
- 若 "Optimization stopped"/NStep 用尽/末次仍 NO ⇒ 逐字写「该端未达极小」。

## 5. 必带的三句限制语（逐字）
- 「连接性未由 IRC 证明（默认 10 点/方向亦未达端点）」
- 「SP 端点能差不可当 ΔE‡」
- 「端点几何收敛性只作描述、不外推极小存在性」

## 6. 分母口径（能量差不含 ZPE/热校正；口径变更须报 coordinator）
- 若 FWD Opt 落 B（能量差 <1 kcal 且五基准键长 ±0.05 Å 内）⇒ 正向端由既有 B 极小值独立复核，不再单设正向分母；**分母取 REV 极小**，ΔE‡ = E(TS) − E(REV 极小)，TS 能量 −364.290279158（frequency.log）。

## 7. 计算口径
Gaussian 16，B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight，**气相无 SCRF**，q1/m1，4c/6144，priority 0，串行一次一条；产物目录 `gold_fill_20261018/HL1/HL1_E1/irc_endpoints/`。
