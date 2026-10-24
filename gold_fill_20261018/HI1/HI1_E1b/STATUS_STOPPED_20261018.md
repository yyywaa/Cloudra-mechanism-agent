# HI1_E1b（HI1_E2）· 本道状态：**调度终止归档**（2026-10-18 05:0x）

## 终止依据
用户 05:0x 指令（经主协调 evt_1368eb1b076741ac 广播）：HI1 作为被替换题（“被换掉的题可以杀了”），其剩余作业与 durable run 一律停止，把核让给两道新题（N_FORMAMIDE / N_HNCO）。

- 本道执行：`ts_stop("ts_0026")` → run status = **stopped**，job 1092 state = **cancel_requested**。
- 本道未删除、未覆盖任何几何/日志/provenance；以下文件全部原样保留为归档证据。
- **这是调度终止，不是科学失败结论**：没有取得已验证鞍点，ΔE‡ 不存在（不得回填、不得引用任何数值）。

## 终止时 ts_0026 的状态
- run 目录：`ts/ts_0026`（revision 23，stage=refine，status=stopped）
- ts_opt = job 1092：`ts/ts_0026/jobs/declaration_0003/ts_opt/refine.gjf`
  sha256 `658b0cc3e836d8ef929f2e634aa30376dbe65bdfb157119db91af67ad3df51c7`
  route `#p opt=(TS,calcfc,noeigen) b3lyp/def2svp empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=dmso)`（%nproc=4 / %mem=6144MB）
- 日志：`ts/ts_0026/jobs/declaration_0003/ts_opt/refine.log`
  sha256 `a27d5f147487f099e7938798bd63a96bd61ae4c0b405d3b33de5de9a5af6099d`（1,519,164 B，被终止于计算中途）
- 进度快照（仅过程记录，无结论）：已走到 `Step number  33 out of a maximum of  153`（L23848）；末三次 SCF L22387 −593.860566723 / L23080 −593.858263717 / L23775 −593.859284599 Eh；日志末尾是第 34 步的 SCF Cycle 1，被调度终止切断，**没有** Stationary point / Normal termination。
- 与分母（−593.929762803 Eh，INT1_27）相比，第 33 步仍在 +44 kcal/mol 量级；这符合「协同四中心 guess 处在很陡的上升面」的预期，但**既不能当能垒上界、也不能当鞍点证据**。

## 已完成的、可复用的模型工作（归档，不构成交付）
1. 27 原子子系统原子序/分子图核对完毕（见 [TS_GUESS_PROVENANCE.md](TS_GUESS_PROVENANCE.md) §1）：1=C1、2=C2、3=O4、4=C3、10=H22、18=N20、27=H21，C8H15NO3 q0/m1，与 `hi.py` 第 2 步 reaction_center（工作序 form (2,4)/(3,10)、break (4,10)/(2,3)）逐条对上。
2. 分母原生日志：`gold_finish_20261015/HI1/E1/split/INT1_27_optfreq.log` sha `c03e0a82…`，E = −593.929762803（L26615/L28142），L26904 Stationary point，75 模 0 虚频（L28588-28589）。
3. TS guess（`build/ts_guess_27.xyz`，构建脚本 `build/build_final.py`）：r(C2-O4)=2.200、r(C2-C3)=1.440、ang(C3-C2-O4)=90.0°、r(C3-H22)=1.355、r(O4-H22)=1.351、C2···H22=1.595、C3-H22···O4=152.8°，每个 H 距母原子 0.97–1.10 Å，无 <0.5 Å 撞原子。
4. 产物端起点几何 `build/product_start_27.xyz`（烯胺 + 水，同原子序；**不是**极小值，需 Opt+Freq 才能用）。
5. 频率模分析脚本 `build/analyze_freq_mode.py`（已在 `INT1_27_optfreq.log` 上验证可解析 75 模；输出三份额 + watch pair 沿键净位移方向），供将来任何 lane 直接复用。

## 追加（05:0x 之后）：终止已落地 + 一处登记缺陷的状态更新

- **job 1092 已进入终态 = `cancelled`**（compute 事件原文：`Job 1092, state=cancelled. TS ts_0026: refine / ts_opt.`），不是 failed、不是 Error termination；日志里也没有任何 `Normal termination` / `Error termination` 行 ⇒ 未收敛、未进 freq、无任何虚频数据。
- **reaction_center 现在是对的（1-based）**：该事件回显 `centres (1-based): 2-4, 3-10, 4-10, 2-3`，与声明 bond_changes（form C2–C3 / O4–H22，break C3–H22 / C2–O4）一致。此前 [E1B_STATUS_AND_EVIDENCE.md](E1B_STATUS_AND_EVIDENCE.md) §5 登记的「declare 里写成 0-based `[[1,3],[2,9],[3,9],[1,2]]`」是更早的 revision 状态，已由后续 ts_resume（revision 21 → 22 期间一并重写 reaction 组）修正；§5 保留为过程记录，不再代表当前声明。freq 从未起跑，因此「frequency_analysis 用错配对」的风险没有实际发生。
- **归档完整性**：本目录新增文件只有 `STATUS_STOPPED_20261018.md`（本文件）与既有 `E1B_STATUS_AND_EVIDENCE.md`、`TS_GUESS_PROVENANCE.md`、`build/`、`analysis/`；`ts/ts_0026/` 下所有作业输入、日志、chk、process.json 未做任何改动，均按 `ts_stop` 后原样保留（不覆盖、不删除）。

## 若要重新接这条边（给后续 lane 的交接）

- 不可 ts_resume ts_0026（已 stopped，且题已被替换）；需要重新 ts_prepare 建新 run。
- 关键未解问题：**协同四中心（O4 直接夺取 alpha-H）在几何上高度张紧**（C2 距 C3···O4 直线仅 0.86–1.2 Å，转移 H 必然贴近 C2）。下一个假设应优先检验分步路径（先断 C2–O4 → 亚铵/烯胺，再由水/羧基取质子），或把羧基穿梭纳入模型（本 27 原子模型里羧基距 H22 有 5.4 Å，帮不上）。
- 分母口径：参考态必须用本步自身起点极小值 INT1_27（−593.929762803），不要用 RC_27（−593.934532807，那是 E1a 的参考态）。
