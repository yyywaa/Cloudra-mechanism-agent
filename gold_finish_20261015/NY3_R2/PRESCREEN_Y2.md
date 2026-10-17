# NY3-R2 预筛报告：候选 Y2 = 甲酸甲酯酸催化水解 AAC2（可算性预筛）

生成（第一阶段，方法 + 在飞状态）：2026-10-17 14:05 CST｜执行会话：as_6fdd1a4300b74a9f（small_mol）
工作目录：`gold_finish_20261015/NY3_R2/`（旧包 `gold_finish_20261015/NY3/` 只读，未改动）

> 本文件先落「方法 + 在飞状态 + 已核实的结构事实」；log 终态后的判读数字（行号、sha、扫描逐点表）在 §5–§7 补齐。
> 状态所有权说明：两个预筛作业（1048 RC Opt+Freq、1050 O6–C4 扫描）由主协调会话 as_a396e35616564357 提交，本会话**不重复提交**、不改写 `STATUS.md`。

## 0. 体系与计算级别（逐字）
- 总反应：甲酸甲酯 + H₃O⁺ + H₂O → 甲酸 + 甲醇 + H₃O⁺（酸催化 AAC2）
- reactant SMILES `[OH3+].COC=O.O`；product `[OH3+].O=CO.CO`；**charge = +1，multiplicity = 1**；**15 原子**
- route（两个作业一致，逐字）：
  `#p opt freq B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=Water)`（1048）
  `# opt=(modredundant,maxstep=10) B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=Water)`（1050）
  **def2SVP 无连字符**（连字符写法会 l1 QPErr）；8 cpus / 10000 MB / priority 0。
- 声明反应中心（映射 SMILES `[OH3+:1]([H:10]).[CH3:2][O:3][CH:4]=[O:5].[OH2:6]([H:11])[H:12]`）：本步预筛键对 **O6(水)→C4(羰基碳)**，相邻质子转移 O1–H10→O5。

## 1. RC 复合物种子几何的构造方法（provenance）
1. 三个组分用 `smiles_to_mol(generate_3d=True)`（共享 builder：RDKit 嵌入 + MMFF94）分别建 3D：
   `build/art_mf/prepared.xyz`（`COC=O`）、`build/art_w/prepared.xyz`（`O`）、`build/art_h3o/prepared.xyz`（`[OH3+]`，charge +1）。
2. 组装脚本：`build/build_rc3.py`（前身 `build/build_rc.py`、`build/build_rc2.py`，均在 `build/`）。以羰基碳 C4 为极点建立局部正交基：
   `e1 = unit(C4→O5)`，`e2 = unit[(C4→O3) − ((C4→O3)·e1)e1]`（酯平面内、指向甲氧基），`e3 = e1×e2`。
3. **水分子摆放**：`O6 = C4 + 2.90·[cosθ·e1 + sinθ·(cosφ·(−e2) + sinφ·e3)]`，θ=∠(O6–C4=O5) 为进攻角，φ 为离平面角；−e2 指背离甲氧基方向以避让 CH₃O，取 θ=80°、φ=35°。
   水分子 3D 取向用 **8×10⁴ 随机 SO(3) 采样**搜索（评分 = H···O5 距离 + ∠H–O5–C4 偏离 120° 的罚 + 与酯/水/H₃O⁺ 的最小非键距离罚），选出「一个水 H 指向羰基 O」的取向。
4. **H₃O⁺ 摆放**：O1 置于 O5 半径 2.65 Å 的球面上 + 8×10⁴ 随机取向搜索，评分目标 H···O5≈1.72 Å、∠H–O5–C4≈125°、无 <2.2 Å 原子重叠。
5. 复核（工具证据，非目测）：`internal_coordinates(mode=analyze, charge=+1)` → C2H9O4、**15 原子 / 12 键 / 3 片段 / 总电荷 +1**、无异常键角；唯一 bond anomaly 是 O5···H=1.72 Å `forming_candidate`（距离启发式）；`C2–O3–C4–O5 τ=0.0°`（Z 型酯，符合加成前构象）。
6. 原子顺序统一为：1=O(H₃O⁺)、2=C(甲氧基 CH₃)、3=O(甲氧基)、4=C(羰基)、5=O(羰基)、6=O(水)、7–9=甲基 H、10=H₃O⁺ 转移质子、11–12=水 H、13–14=H₃O⁺ 其余两个 H、15=甲酰基 H ⇒ 与声明的映射号 1/2/3/4/5/6/10/11/12 一一对应，扫描坐标可直接写 `B 6 4`。

### 1.1 改进版种子（当前 `build/rc_seed.xyz`，sha256 3f9396b60c18f9d055a2f65b63d7d647ae0f504c456f9fb790a337f05f83f128）
| 量 | 值 |
| --- | --- |
| O6–C4 | 2.900 Å |
| C4=O5 / O3–C4 | 1.220 / 1.356 Å |
| ∠O6–C4=O5 | 80.0° |
| O6···O5 | 2.944 Å |
| 水 H11···O5 | 2.139 Å（∠H11–O5–C4 = 88.2°） |
| 水 H12···O5 | 3.538 Å |
| H₃O⁺ H10···O5 | 1.720 Å（∠H10–O5–C4 = 118.1°），O1···O5 = 2.650 Å（∠O1–O5–C4 = 126.0°）|
| O1–H10 | 0.991 Å |

### 1.2 **在飞作业实际使用的几何（build_rc2.py 那一版）**——判读时必须按这一版
把 1048 输入 `rc_optfreq.gjf` 的坐标块经 `format_converter(gjf→xyz)` → `build/inflight_rc_seed.xyz`，再用 `internal_coordinates` 复核（15 原子、+1、12 键、3 片段、无异常键角）：

| 量 | 值 | 判定 |
| --- | --- | --- |
| O6–C4 | **2.900 Å** | 与要求 2.8–3.0 一致 |
| O6···O5 | 3.243 Å | 水的一侧偏外 |
| 水 H11···O5 | **2.881 Å** | 「水 H 指向羰基 O」方向性勉强成立，但是弱/长接触（不是真氢键） |
| 水 H12···O5 | 3.897 Å | — |
| H₃O⁺ **H13**···O5 | **1.720 Å** | 满足要求 1.6–1.9 Å（**注意：该文件里转移质子是原子 13，不是映射号 10**）|
| O1···O5 | 2.650 Å | — |
| C2–O3–C4–O5 | τ=0.0° | Z 型酯 |
| C4=O5 / O3–C4 | 1.220 / 1.356 Å | 正常 |

> **索引一致性提醒**：1048/1050 的坐标块按同一原子顺序写（1=O(H₃O⁺)、2=C(Me)、3=O(OMe)、4=C(羰基)、5=O(羰基)、6=O(水)、7–9=MeH、10=H₃O⁺(非转移)、11–12=水 H、13=H₃O⁺ 转移质子、14=H₃O⁺、15=甲酰基 H），因此 `B 6 4` 仍正是 O6–C4；但**映射号 H10 在该原子顺序下对应第 13 号原子**，频率模矢判读与质子转移描述要按实际原子号写。

## 2. 工具限制留档（供后续包避免同类陷阱）
- `qm_input_writer` **写不出 relaxed scan**：只要 `end_setting` 里带 `B 6 4 S …`，其写入后的自检把文件判为 `relaxed_scan`，却把声明的 `opt` 归一为 `minimum_opt`，直接拒写（`{"opt":"modredundant"}`、`{"scan":"relaxed"}` 都拒）。可行路径是 `ts_guess(mode="scan_prepare")` 生成后手工补 `%chk/%mem/%nprocshared` 与 `1 1` 电荷行（主协调即如此做）。
- `ts_guess(scan_prepare)` 顶层不接受 `charge/nproc/mem/multiplicity`（须嵌套形状），因此生成的扫描输入必须外部补电荷行（否则默认 0 1 会算错体系）。
- 本会话另存有一份等价的 Opt+Freq 输入 `A_rc_optfreq.gjf`（`qm_input_writer` 产出，route 逐字正确），**未被提交**，可删。

## 3. 作业标识 / 目录 / 绝对路径

| 项 | A) RC Opt+Freq | B) O6–C4 受约束弛豫扫描 |
| --- | --- | --- |
| job_id | **1048** | **1050** |
| 提交者 | 主协调会话 as_a396e35616564357 | 同上 |
| 起止（本机时钟） | 13:58:30 → 14:08:27 | 14:08:28 → （运行中） |
| 作业目录 | `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NY3_R2/` | 同左 |
| `.gjf` | `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NY3_R2/rc_optfreq.gjf` | `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NY3_R2/scan_O6C4.gjf` |
| `.log` | `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NY3_R2/rc_optfreq.log` | `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NY3_R2/scan_O6C4.log`（job 记录另指向 `.cloudra/calc-1050.out.log`） |
| 末状态 | 计算器退出码 1（G16 l9999 `Error termination`） | running |

## 4. sha256 + 行数（读取时刻 14:12–14:15）

| 文件 | sha256 | 行数 |
| --- | --- | --- |
| `rc_optfreq.gjf` | `431b368ab8080e97cfe9050b8e66b336121a7eac844664f261f577265f3eabfd` | 24 |
| `rc_optfreq.log` | `17cd832aeb62c3e3dd28ee3ca0e660c198a43c668b28a110331ce14be57da66f` | 29985 |
| `scan_O6C4.gjf` | `b784f4b6b28dad0f0af1e61f8082d95c82abca3c5e3de8a9fd74af0609f4967d` | 27 |
| `scan_O6C4.log` | `277665e2c934304e40f2dae050c910c693258f75eae62cb8948a6e325921e9eb` | 18354 |

## 5. A) RC Opt+Freq（job 1048）判读：**NStep=59 截断失败，未做频率**

- **末判据 4 行（行号 29661–29665）**：
  ```
  29661:         Item               Value     Threshold  Converged?
  29662:  Maximum Force            0.009134     0.000450     NO
  29663:  RMS     Force            0.001440     0.000300     NO
  29664:  Maximum Displacement     0.042291     0.001800     NO
  29665:  RMS     Displacement     0.012981     0.001200     NO
  ```
- `Optimization completed` 行：**不存在**；`Stationary point found` 行：**不存在**。
- 终止：`29667: Optimization stopped.`、`29668:    -- Number of steps exceeded,  NStep=  59`、`29981: Error termination request processed by link 9999.`、`29982: Error termination via Lnk1e in /home/ly/g16/l9999.exe at Sat Oct 17 14:08:17 2026`。**无 `Normal termination`**。
- 末 SCF 能量：**`29527: SCF Done:  E(RB3LYP) =  -382.080665240     A.U. after   10 cycles`**；首个 SCF `605: E(RB3LYP) =  -382.063942371` ⇒ 全程只降 **−0.016723 Ha = −10.49 kcal/mol**。
- 频率：**`Frequencies --` 行数 = 0**（3N−6 应为 **39**）；**无 `N imaginary frequencies` 行** ⇒ 本作业**根本没有进入 freq 阶段**，因此「0 虚频 / 1 虚频」都不能对本 RC 声明。虚频模矢组成：**不适用（无频率数据）**。
- 失败形态定量证据：`Maximum Force` 全程呈**2 周期振荡**（每步更新一次、方向来回过冲）：
  `0.028745 → 0.008995 → 0.030294 → 0.008486 → 0.029378 → 0.009328 → 0.029912 → 0.008863 → 0.029169 → 0.009647 → 0.029725 → 0.009134`（行号 24314…29662）；`Lowest energy point so far` 只出现 28 次/59 步。⇒ 这不是「稳步收敛中被打断」，而是**在极平/软坐标上的 Berny 步长极限环**（水取向 + H₃O⁺ 位置 + 弱氢键网络）。
- 失败类型归类：**NStep 截断（NStep=59）+ 软坐标极限环**；与旧包 NY3 同类陷阱（不含 Na⁺ 但仍是「无锚定氢键网络」）。

## 6. B) O6–C4 受约束弛豫扫描（job 1050）判读：**失败——扫描点 1 就撞 NStep=61，全程 0 个扫描点完成**

- 输入 `B 6 4 S 14 -0.100000`（2.900 → 1.500 Å，15 点），`opt=(modredundant,maxstep=10)`；`scan_O6C4.log` sha256 **`277665e2c934304e40f2dae050c910c693258f75eae62cb8948a6e325921e9eb`**、**18354 行**；`scan_O6C4.gjf` sha256 `b784f4b6b28dad0f0af1e61f8082d95c82abca3c5e3de8a9fd74af0609f4967d`（27 行）。
- 起止：14:08:28 → 14:17:39（≈9.2 min **全部耗在扫描点 1**）。
- `17957: Step number  61 out of a maximum of   61 on scan point     1 out of    15`；点 1 末判据在 **18049–18054**：`Maximum Force 0.000658 NO` / `RMS Force 0.000168 YES` / `Maximum Displacement 0.034593 NO` / `RMS Displacement 0.009977 NO`（4 项只有 1 项达标）。
- 终止：`18055: Optimization stopped.`、`18056:    -- Number of steps exceeded,  NStep=  61`、`18350: Error termination request processed by link 9999.`、`18351: Error termination via Lnk1e in /home/ly/g16/l9999.exe at Sat Oct 17 14:17:32 2026`；**无 `Normal termination`、无 `Stationary point found`**。
- **逐点表 = 空**：log 里 `on scan point` 只出现「1 out of 15」这一个点号，point 2…15 从未开始 ⇒ **没有 ΔE 曲线、没有峰值、也无法做「0.1 Å 内 >6 kcal/mol 跳变」检查**（不是「峰不成形」，而是**曲线根本不存在**）。
- 点 1 为何打不完（软坐标直接证据）：`17341: E= -382.082675746`、`17624: E= -382.082679255`、`17921: E= -382.082684135` ⇒ 连续三步电子能总变化 **< 0.01 kcal/mol**（0.0053 kcal/mol），而 Max/RMS 位移仍 0.035/0.010 Å ⇒ 能量面对「水取向 / H₃O⁺ 位置」极平，优化器原地踏步，与 A) 的 2 周期振荡同源。
- 失败类型归类：**NStep 截断（扫描点 1，NStep=61）⇒ 零个扫描点完成**；根因是软坐标（松散氢键网络），**不是换通道/断键**。

## 7. 结论：Y2（AAC2）可算性预筛 **未通过**（两条判据均失败，且都不是「换通道」型失败）

| 判据 | 结果 | 证据 |
| --- | --- | --- |
| RC Opt+Freq 是否为 0 虚频极小值 | **无法判定 ⇒ 判失败** | NStep=59 截断（行 29667/29668），`Frequencies --` 行数 = **0**，无 `N imaginary frequencies` 行 |
| 扫描是否单一极大峰、峰高 ≤~35 kcal/mol | **不成立（无曲线）** | 扫描点 1 撞 NStep=61（行 17957 / 18056），**0 个扫描点完成** |

- 失败类型：**NStep 截断 + 软坐标极限环**（不是多虚频、不是峰不成形、不是换通道）。
- 科学结论（不夸大）：在 `B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=Water)` 下，**以 §1.2 这一 RC 起点**（水与 O5 只有 2.88–3.24 Å 松散接触、H₃O⁺/水的取向自由度未锚定）**未能在 90 min 预算内得到收敛的 RC 极小值与能量曲线**。这不等于「AAC2 不可算」——被否掉的是**这个起点 + 这套约束/优化设置**。
- 若要在同一候选上再试（**本会话未执行、需新预算裁定**）：① 换 §1.1 改进版种子（水 H···O5 = 2.14 Å）重建 RC；② 先对水取向/H₃O⁺ 位置做构象扫描再优化；③ `opt=CalcFC` 或减小初始步长 + `maxcycle=200`；④ 只做刚性扫描定位峰区再放开。
- 退路：O2（DMDO + 乙烯，中性、无质子转移、**RC 已按「受约束复合物」写法备好**，正对本次失败根因）见 `fallback_O2/FALLBACK_O2_READY.md`。
- 最终采用哪条路由主协调裁定；本文件只登记实测证据。
