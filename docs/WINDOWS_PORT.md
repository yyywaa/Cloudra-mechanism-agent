# Windows 移植分支

## 定位与政策

- **master 是纯 POSIX 目标**（2026-09-20 起）：不接收 Windows 兼容补丁，
  存量容忍补丁也已整体清除（master commit `017835ec`）。**Windows 兼容层
  归本分支独有**——flocks msvcrt 后端、js_runtime/run_dirs 进程组降级、
  monitor is_posix 守卫、web_launcher `cmd /c`、JS host 环境继承全部住
  在这里，merge master 时若被删必须以本分支版本为准恢复（首个实例见
  merge `39db651b` 后的恢复提交）。
- Windows 相关 PR 一律以 `windows` 为 base；master 只接受「对 POSIX 行为
  零影响且不属于平台兼容」的改动。

## 同步节奏

定期 `git merge master`（不是 rebase——分支已推送，重写历史会让协作者
掉队）。flocks / js_runtime / shutdown / monitor 是已知的永久 merge 面，
合并 master 后先跑 CI 再推。

## 诚实护栏

`.github/workflows/ci.yml` 的 `windows-smoke` job 在真实 Windows runner 上
跑平台敏感面。**每个 Windows 兼容修复必须连带把对应测试加进 smoke 列表**，
否则兼容会在下一次 master 合并时悄悄腐烂（先例：shutdown 升级路径引入
lsof + SIGKILL，两天内就再造了两个 POSIX-only 构件）。

## 剩余 POSIX 依赖清单（移植工作面，按阻塞度排序）

1. **计算执行链是 bash**（决定性阻塞）：`calculator.sh` 与 guard 的引擎
   调用全靠 shell 脚本（`infra/compute_utils.py` 构建命令、`runtime/monitor.py`
   拉起）。Windows 原生无 bash——要么提供 PowerShell/Python calculator
   通道，要么明确计算节点只走「远端 Linux/Slurm」、Windows 只做控制面。
   **建议先定这条路线的架构方向再动手。**
2. `services/shutdown.py` 升级路径：`lsof` 不存在（`_port_listener_pid`
   返回 None → 升级失效但不炸）；`SIGTERM`/`SIGKILL` 在 Windows 经
   `os.kill` 都映射 TerminateProcess（立即死、无优雅期，语义可接受）。
   候选修法：API 进程写 pidfile（app lifespan 内），stop 读 pidfile 取代
   lsof——顺带比端口反查更稳。
3. 测试套件本身：`conftest.py` 与部分用例的 POSIX 探测/skip 口径未审计；
   smoke 之外的测试在 Windows 上的红绿状态未知，按需逐个解锁进 smoke。
4. Slurm：天然 Linux 集群事项，Windows 上按「不可用」处理即可，不算工作项。

## 已完成（在本分支）

- JS host 环境继承（PR #47，node.exe 缺 SystemRoot/TEMP 启动即 abort）
- flocks msvcrt.locking 后端（config mutate / 守护互斥可用）
- js_runtime 进程组降级（Windows 无 killpg → 单进程 terminate/kill）
- run_dirs 进程组终止降级（单进程 terminate → kill 并回收）
- monitor nice preexec 守卫（`is_posix()`）
- web_launcher npm `cmd /c`

- 主线同步至 `2b261d6a`：保留兼容层；Web 启动使用平台原生 `PYTHONPATH` 分隔符，回归已纳入 windows-smoke。
