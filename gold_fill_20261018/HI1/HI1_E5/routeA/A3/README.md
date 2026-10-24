# A3 目录使用须知

本目录在 A1 收敛前**不产生任何合法输入**。

- start_A3.xyz 目前是旧版残留（scan#17 的几何，R(2,4)=2.2248），**不得**据此建 A3；那样得到的是 A1 的重复件。
- A3 的唯一合法起点 = A1（job #1096）收敛几何的最后一个 Standard orientation 块，取到后做 0.2 Å 的 C2–N4 刚性位移到 R(2,4)=2.6248、R(25,26) 保持 1.4693，再建输入。
- A3 输入的头部注释必须写：起点 = A1 收敛几何、A1 job id、A1 的 E 值与日志行号、A1 日志 sha256、来源扫描日志 /home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/runs/e3b_scan2d_c2n4_o25h26.log 与行号。
- 依据：gold_fill_20261018/HI1/HI1_E5/GRID_PLAN_A.md（69 行，sha256 728470ccb158f891830aa4886d637508ebdfb435127b3d63e8686ad55bf398b2）第 3 节与 4.1 节。
