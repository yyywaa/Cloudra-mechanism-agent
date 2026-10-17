# lane3 通道 B (HI1_EM1) 第 2 次尝试种子 provenance · 2026-10-17

本文件记录通道 B 重试种子的**构造过程与逐项校验**。它只是几何种子 provenance，**不是 QM 化学证据**：
不代表鞍点、不代表能垒，也不能替代 TS/IRC/端点验收。

## 0 背景（为什么换种子）

- **第 1 次尝试已判 pseudo-saddle**（ts_0012 rev23）：job 1013 ts_opt 驻点 E = -939.293671629 Eh，
  frequency job 1021 恰 1 虚频 **-27.9419 cm⁻¹**（frequency.log sha256 a70f1e78…），
  虚频模对 C3–C6(work 1–29) 的 watch_pair_fraction 仅 **0.078%**，heavy_atom_fraction 0.322（H 主导软模），
  且几何为反应物侧（d(1,29)=3.198 Å、C1=C2 1.355、C=O 1.216 完好）⇒ 见 E2EM1/STATUS.md §8/§9。
- **通道 A 的 ts_opt（job 1008，种子 job_58 f7 d=2.275 Å）同时在漂离**：d(1,29) 从 2.646 Å（step 1）单调增大到 4.75 Å（step 67），
  电子结构始终烯胺型（C1=C2 1.358、C2–N4 1.381）⇒ 该种子所在区域的最软模不是 C–C 成键方向。
- **历史 ORCA 素材几何复核（本会话亲测，仅取几何）**：
  | 素材 | d(1,29) | d(1,2) | d(2,4) | d(28,29) | 性质 |
  |---|---|---|---|---|---|
  | job_64/ts2_np8.xyz（"E2 major OptTS"） | 3.364 | 1.359 | 1.380 | 1.223 | 反应物侧松散驻点（与我们的伪鞍点同型） |
  | job_58 链 2.275 Å 点（= 本 run 的 A 种子） | 2.275 | 1.381 | 1.358 | 1.242 | 仍偏反应物侧 |
  | **job_58 链 1.938 Å 点（帧 #234–252）** | **1.938** | **1.422** | **1.330** | **1.279** | **TS-like（部分成键）** |
  | job_58 链 1.600 Å 点 | 1.600 | 1.479 | 1.308 | 1.338 | 生成物型（iminium–aldolate） |
  | job_59 链 + job_65 续扫（"EM1 minor CONTINUATION 2.4→1.6"） | 2.2–2.4（最低 2.2） | 1.383 | 1.365 | 1.239 | 仍反应物型 ⇒ **通道 B 无历史 TS-like 帧** |
  （镜像关系：job_58 链 z→−z 后为 (S)-脯氨酸 + S-aldol = 通道 A；job_59/65 链 z→−z 后为 S-aldol? 否，为 R-aldol = 通道 B。）

## 1 构造（机器构造；本批无 compute record）

- 模板：`gold_finish_20261015/HI1/E2EM1/build/TS_guess_E2_j58f8.xyz`
  sha256 `5024997e6eea53a91fa4b7ec4a92ab36916ca7c5f67deb0ef4263835c174cb40`
  （= z 镜像后的 ORCA job_58 弛豫扫描点 1.938 Å；41 原子，元素序 = 本 run bound 序）
- 操作：把苯甲醛取代基（苯基 C30–C35 + 醛 H36）对 **C29/O28/C1 平面做镜面反射**（Re/Si 面翻转）。
  保留全部键长；d(C1···C29) 严格不变。这正是把"同面进攻"变成"另一面进攻"的立体化学操作。
- 产物：`gold_finish_20261015/HI1/E2EM1/build/TS_guess_EM1_j58f8_faceflip.xyz`
  sha256 `9f4d651aff4c75ef7ec9e582184c2581f4f22873d73b06b18e868cdd554ea10b`
- 脚本：`gold_finish_20261015/HI1/E2EM1/build/make_flip_seed_lane3.py` sha256 `ca89afd705d2d09aa1d3b08c38235b41a23c7a7d48caa4ebea444690596054ff`

原始输出（RDKit，加成物拓扑 C1–C29 成键 / C2=N4⁺ / C28–O29⁻）：

    source .../build/TS_guess_E2_j58f8.xyz n= 41 CIP: [(8, 'S'), (29, 'S')] minsep=0.972
    flipped  CIP: [(8, 'S'), (29, 'R')] minsep=0.972
    d(1,29): 1.937500 -> 1.937500 (preserved)
    element order unchanged: True

（minsep 0.972 Å 来自原有的 O–H 键，未新增原子重叠；CIP 1-based：8 = Cα，29 = aldol C = map6。
通道 B 要求 Cα = S、map6 = R ⇒ 与产物声明一致。）

## 2 方法学记录：为什么用反射而不是 180° 旋转

- 绕 C29–O28 轴 180° 旋转（几何手性体积 2.5724 → −2.5724，中心确实反演）后，**RDKit 3D 感知仍报 (29,'S')**；
- 精确交换 C30/H36 坐标（同样反演手性体积）时 RDKit 报 (29,'R')；
⇒ 对该畸变（C1–C29 仅 1.94 Å 的"半成键"）几何，RDKit 的 3D 手性标签对"绕轴 180° 旋转"这一构造失配。
为保证与流程/端点的 RDKit 身份判据一致，采用**反射**构造。
被取代的中间文件 `build/TS_guess_EM1_j58f8_flip.xyz`（sha256 `6625991c39131a33e5c716920ea6a75e60421d5416ed55f0e5d6a2c09fb9062a`）**不得使用**。

## 3 备选（若本种子仍失败）

- tier ②：以 `[1,29]`（bound 1-based）为坐标做受约束/弛豫扫描（例如 2.2 → 1.4 Å），取脊线峰帧作 guess；
- tier ③：沿声明 `atom_map` 做 IDPP 插值帧。
两者都需写权会话/主协调批准后再提交。
