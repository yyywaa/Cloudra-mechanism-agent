## 摘要

在本战役（NY3 的 E1 边：RC → I1 的分子内 C4–O1 成键，11 原子中性模型含 Na⁺）尝试用 `ts_guess(mode='xtb_path', ...)` 做无偏路径搜索以定位鞍点，**两次都拿不到可用 guess**。

## 复现 1：传 atom_map ⇒ 工具面直接拒绝

调用（1-based，product 序 → reactant 序，与同一 run 的 ts_resume 使用同一映射）：
`ts_guess(mode='xtb_path', reactant_path=<job 967 RC 末帧>, product_path=<job 985 I1 末帧>, atom_map=[1,4,5,6,2,7,8,9,10,11,3])`

返回：`Invalid tool arguments: arguments: invalid value; check the field type and constraints in the tool schema`
⇒ 该分支的 `atom_map` 形参在工具面上不可用（schema 视其为 unknown / 类型不符）。

## 复现 2：不传 atom_map ⇒ 进入执行但 invalid_endpoints

最小参数调用能进入执行，持久目录 `/home/ly/Cloudra-mechanism-agent/ts_path/xtb_path_runs/guess_0001/`：

- `command.txt`（sha256 `edd35a645f37f782350461f467ae5cd1d00e52050d54f6ecbc2bd09b70596907`）：`xtb reactant.xyz --path product.xyz --input path.inp --chrg 0 --uhf 0`
- `path.inp`（sha `e05790886cb999461d9f80ca04537c0f9f398dedd2a32935c11ad9596438ba24`）：`$path / nrun=100 / $end`
- `versions.txt`（sha `f365b5d54ba760a31ed901cb11386518c3095ae28705090b626d68fe9e574a15`）：xtb 6.5.0 (746241f)
- `reactant.xyz`（sha `48bfb0929cd03e2c216d62e84abbe449d9d903fcc0e3de1b96068ad12c929f54`）/ `product.xyz`（sha `7f2ac9cd075be8f393ad338ba7574e6ee10c1682090cbef21292352b5786138b`）：11 原子

返回 `termination=invalid_endpoints`，未产生 guess。

注意：这两个端点是**同一体系的 RC 与 I1 极小值**（同批 Gaussian 16 B3LYP-D3(BJ)/def2SVP 优化帧、同样 3 分片含 Na⁺），不是物种不同的异构体 ⇒ 「端点无效」的判据为何触发需要说明（元素/顺序/电荷不一致？xtb PATH 是否要求额外约束？）。

## 影响

`ts_guess(mode='xtb_path')` 对本战役不可用 ⇒ 无法获得无偏初始路径 guess，只能退回「会话内几何构造的 provided guess」或「受约束弛豫扫描」（后者已作为 job 1023 提交），guess 质量依赖人工构造。与 #177（工具面/角色面）、#184（ts_prepare 无法设 IRC 步长/算法）同族：**TS 搜索前端的可调入口不足**。

## 建议

1) 修 schema：让 `xtb_path` 分支接受 `atom_map`，或明确声明它不支持；
2) `invalid_endpoints` 时回传**具体判据**（哪个原子对不上、缺哪个元素、是否要求原子数/电荷一致）；
3) 文档补充该分支对「多分片 / 含金属离子」体系的支持范围。