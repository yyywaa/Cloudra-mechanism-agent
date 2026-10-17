# NY3 E2 TS 初猜溯源（ts_prepare 的 provided guess 用）

日期：2026-10-15 ｜ 包：NY3（Coordinator as_7479852819ea48c0）｜ 工作根：/home/ly/Cloudra-mechanism-agent
本文件存在的理由：ts_prepare 的 provided guess 要求 evidence_refs 指向真实存在的 artifact 文件；本文件即 E2 初猜几何的落盘记录（本包 Coordinator 实测，不转述）。

## 文件
| 项 | 值 |
|---|---|
| 路径 | gold_finish_20261015/NY3/prep/build/TS2_step1.xyz |
| 原子数 | 11 |
| sha256 | 8ef368f357b7ea43b4f777a6e1aa758e0a25db194afdc68500754db5e4687114（2026-10-15 18:4x 由本包 Coordinator 用 sha256sum 实测） |
| 原子序 | 与 prep/i1.xyz 相同：1 Na ｜ 2 C2 ｜ 3 O3 ｜ 4 C4 ｜ 5 O1 ｜ 6 O5 ｜ 7,8,9 H(C2) ｜ 10 H(C4) ｜ 11 H6 |

## 实测关键距离（Å；括注为同序 i1.xyz 的值）
C4-O3 2.011（1.425）｜ C4-O1 1.407（1.407）｜ C4-O5 1.309（1.309）｜ O1-H6 0.976（0.976）｜ O3···H6 3.534（3.005）｜ C2-O3 1.426（1.426）｜ Na-O5 2.166（2.166）｜ Na-O1 2.531（2.531）｜ Na-O3 2.383（2.229）

## 语义
= I1 中把甲氧基（C2-O3 及 3 个甲基 H）绕 C4-O3 轴转出、C4-O3 拉长到 2.011 Å，其余骨架（O1-H6、C4=O5、Na-O5/O1 配位）与 i1 逐值一致 ⇒ 这是 E2「甲氧基脱离（C4-O3 断）、质子仍留在 O1」的非协同步 TS 初猜（与 ts_e23_guess.xyz 的协同步六元环初猜相对照）。

## 出处与边界
- 该文件由 NY3 prep 道于 2026-10-15 16:25 生成（mtime）；PREP.md §5 的构造链表未收录它，故本文件不声称知道其确切变换 ops，只记录对落盘文件的实测数字。
- 它是初猜，不是鞍点/能垒证据；虚频个数、虚频模归属、IRC 双向方向、两端极小值身份一律由 ts_prepare 的 OptTS/Freq/IRC 判定。
