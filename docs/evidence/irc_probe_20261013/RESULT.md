# IRC 可行性实测（正向支 ts/ts_0006）— 2026-10-13 07:52 起

由 DSH 会话以 bash 直接调用 Gaussian 16 完成，**未经过 Cloudra 平台提交**（服务当时起不来），
亦**未改动项目任何文件**：ts/ts_0006 零触碰、无声明改动、无交付层写入。

## 结论：IRC 能算。卡住的是仓库写入器的关键字重复，不是化学。

### 探针 A —— 与平台生成件逐字一致（含重复 irc=）
- 输入：ts/ts_0006/jobs/declaration_0002/irc/irc.gjf（cmp 判定 identical）
- route: `#p irc=calcfc b3lyp/def2svp irc=(calcfc,maxpoints=40,stepsize=10) ...`
- 内部选项行：`1/10=3,19=13,38=1,39=10,42=40,172=1/1,7;`  ← **无 `44=3`**（IRC 任务标志未注册）
- Gaussian 日志：`Wanted an integer as input.` → `Error termination via Lnk1e in /home/ly/g16/l101.exe at Tue Oct 13 07:52:18 2026`
- 进程退出码 1，`Point Number` = 0；stderr 另有 `Error: segmentation violation ... Aborted (core dumped)`（l101）
- 本次实测耗时约 173 s（该机启动 + 首轮 SCF 到 l101 报错）

### 探针 B —— 只删掉重复的 `irc=calcfc`（其余逐字不变）
- route: `#p irc=(calcfc,maxpoints=40,stepsize=10) b3lyp/def2svp empiricaldispersion=gd3bj int=ultrafine scf=(tight,novaracc)`
- 内部选项行：`1/10=4,18=10,26=4,38=1,39=10,42=40,44=3,172=1/1,23;`  ← **`44=3` 已注册**
- 里程碑（Gaussian 自述，原文）：
  - `Initial Hessian              = CalcFC`
  - `Standard basis: def2SVP (5D, 7F)`
  - 08:22:21 进入 l123：
    `******** Start new reaction path calculation ********`
    `Current Structure is TS -> form Hessian eigenvectors.`
    `Supplied step size of   0.1000 bohr.`
    `Integration on MW PES will use step size of   0.2710 sqrt(amu)*bohr.`
    `Point Number:   0          Path Number:   1`
    `Point Number  1 in FORWARD path direction.`
    `Using LQA Reaction Path Following.`
  - 体系 `C26H19BrO5`，`Deg. of freedom   147` = 3N−6（51 原子）✓
- 时间：07:52 启动 → 08:22:21 出第一个 IRC 点（初始 SCF + CalcFC Hessian ≈ 30 min，
  与 job 872 频率件的 29m53s 一致）。双向 maxpoints=40 ⇒ 预计还需数小时至十几小时。

### 与项目已有记录的关系
- 完全坐实 runs/rc1_ts_work/ISSUE_irc_task_keyword_duplication.md 的判断：
  “the parameter block itself is fine; ONLY the duplication kills the job”。
- 该 ISSUE 的证据是水分子 / HF-STO-3G 级别的 8 个探针（M/N 正常终止）；
  本次是**首次在真实 51 原子体系、真实泛函/基组上**验证同一条结论。

### 这意味着什么
正向支本来可以拿到真正的 IRC 方向证明（→ 升为 verified），
不必长期依赖“±0.080 Å RMS 双向补偿连通性 + 链 A/B 剖面”这套补偿。
修点在工具侧：`cloudra/tools/core/qm_input_writer.py:457-458`（Gaussian）/
`:537-538`（ORCA）把 `extra_keywords` 原样拼接、**未去重**；
ISSUE 已给出三处建议修法（写入前扫描 task 关键字 / 注入前合并参数 / 声明里暴露合并后的任务行）。

## 文件
- probeA_asis.gjf / probeA_asis.log（Gaussian 日志）/ probeA.log（stderr 重定向）
- probeB_dedup.gjf / probeB_dedup.log（运行中）/ scratchB/
- runB.sh（后台启动脚本）

## 停止方式
- `pkill -f probeB_dedup.gjf`  或  `kill <g16 launcher PID>`
- 当前占用 4 核（%nproc=4、%mem=8192MB，与项目既定口径一致）
