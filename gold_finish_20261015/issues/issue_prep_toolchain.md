## 背景
NY3（normal 档，"Na⁺ 制衡的中性模型"皂化题）的准备道在准备一个 3 组分、含 Na⁺ 的复合物时，连续撞到 5 处工具面问题。全部为只读取证 + 最小复现；未改平台代码/DB/进程。

## P1 `smiles_to_mol`：报错与事实矛盾，且多组分复合物在文档化路径上取不回
- 输入：`[Na+:7].[O-:1][H:6].[CH3:2][O:3][CH:4]=[O:5]`（charge 0 / m1 / 3D）。
- 返回：`the builder reported status=ok but produced no MOL candidate`。
- 但同一次调用把文件落盘了：`art_RC_src/assembly/complex_candidate_000.mol` 存在且带完整 bond block 与 `M  CHG  2 1 1 2 -1`，`prepared_structure.json` 也是 `status=ok`。
- 且返回里没有文档化的取回通道（无 `xyz_path` / `mol_content`）。
- 影响：agent 明明拿到了正确产物，却被报错误导成"准备失败"，会重复调用。

## P2 `internal_coordinates` transform 的 stretch 拒绝真实共价键
- 输入：`prep/i1.mol` + `ops=[{type:stretch, atoms:[4,3], new_length:2.00}]`。
- 返回：`bond 4-3 lies on a ring (the graph stays connected after cutting it)`。
- 根因（Notes 自述）：`analyze` 用距离启发式把 **Na–O5 2.166 Å、Na–O1 2.531 Å、Na–C2 2.84 Å** 当成了键（"RDKit bond perception failed"），于是切掉 C4–O3 后，甲醇盐仍经 **Na···O3 2.23 Å** 与主片连通 → 判成环。
- 影响：E2 类 **C–O 断裂方向**的刚体拉伸根本做不到（本次被迫改用大角度旋转），而这类拉伸正是 E2/E3 的候选生成手段。

## P3 `analyze` 对带 bond block 的 MOL 也按距离重猜
- `analyze(build/art_I2_src/assembly/complex_candidate_000.mol)` → `Bonds: 11  Fragments: 1  distance-inferred`，而文件本身是 **8 键 / 3 组分 / Na⁺1、O3⁻1**。
- 即"文件身份"与"工具身份"相反：工具忽略了文件里的键表与 `M CHG`。

## P4 `format_converter` xyz→mol 丢键表
- 提示"Input xyz carries only coordinates..."，产物 bond 数 = 0、无 `M CHG`。
- 与 P2/P3 合起来的净效果：**工具面不存在"保留键表/形式电荷 + 只改几何"的路径**，本次 `rc/i2/ts_*` 的 `.mol` 只能是无键表坐标文件（已预期在 PREP.md 里用 bond block 表替代）。

## P5 `conformer_search` 的 distance_filters 对单原子 Na⁺ 片段有未文档化下界
- `{atoms:[1,2], min:2.15, max:2.35}` → `incompatible guided bounds ... no search was run`；改成 2.4–2.9 即被接受。
- 而 Na–O 的合理配位区间 2.1–2.4 Å 恰好落在被拒范围，文档未提该下界与拒绝条件。

## 复现与证据
- 最小复现清单（每例的输入、返回原文、落盘路径 + sha256）由 NY3 准备道整理中，随后会以 comment 追加到本 issue。
- 相关落盘：`gold_finish_20261015/NY3/prep/`（rc/i1/i2/p/ts_e1_guess/ts_e23_guess 的 xyz+mol+zmat、PREP.md）。

## 影响面
任何需要**多组分复合物 + 金属对离子 + 键表敏感**的任务（本战役里 NY3 是典型；同类还有需要显式桥水/对离子的 NI5/NR1/HL1）。目前只能用"无键表坐标 + 手工维护 bond block 表"绕过，既易错也难以让复核者机械核验。
