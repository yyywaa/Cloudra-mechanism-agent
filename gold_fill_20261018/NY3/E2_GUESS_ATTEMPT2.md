# NY3_E2 · TS 初猜 attempt 2（线性插值 t=0.60）

## 为什么换初猜
- attempt 1 = `gold_finish_20261015/NY3/E2E3/ts_e2_guess.xyz`（sha256 8bbc6dbb866df8619b5a150b6c3ea196c575d3b0b9e1398a89b9497de32e9ea0，IDPP 帧，r(C4–O3)=2.417 Å）。
- 其 ts_opt（本会话 **job 1081**，run ts_0021 declaration_0002，输入 `ts/ts_0021/jobs/declaration_0002/ts_opt/refine.gjf`）以 **l103 FormBX** 终止：
  - 原生日志 `ts/ts_0021/jobs/declaration_0002/ts_opt/refine.log`；
  - 终止行 `Error termination via Lnk1e in /home/ly/g16/l103.exe at Sun Oct 18 03:00:50 2026`（L10785），原因行 `FormBX had a problem.`（L10784），平台记录的原文原因 `Tors failed for dihedral 9-2-3-1`（甲基 H–C2–O3–Na 扭转退化）；
  - 末帧（最后一个 `Input orientation` 块，L10484 起）实测：**r(C4–O3) = 3.308 Å**（起点 2.417 → 向产物侧下滑）、r(C4–O5) 1.210、r(C4–O1) 1.323、O1–H6 0.977、Na–O3 2.057、Na–O5 2.322 Å；末 SCF −466.987210759（L10726）。
  - 判读：attempt 1 的几何落在**产物侧**（r 已过脊线），不是鞍点；l103 属技术性失败，**不作「E2 无鞍点」证据**。

## attempt 2 构造（机器生成，无手敲坐标）
- 端点 A = I1 参考极小值 `E2E3/i1_dft_min_ref.xyz`（sha256 b7e835859f231194f6b3a967d44d53861c9dc8b971769c5e79fe08a8ff97b7eb，r(C4–O3)=1.503 Å）；
- 端点 B = attempt 1 的 IDPP 帧 `E2E3/ts_e2_guess.xyz`（r(C4–O3)=2.417 Å）；
- 同一原子序（i1 序）逐原子线性插值，t = 0.60 ⇒ 本文件 `gold_fill_20261018/NY3/e2_guess_i1_interp_t060.xyz`；
- 插值后实测：**r(C4–O3) = 2.044**、r(C4–O5) 1.243、r(C4–O1) 1.398、O1–H6 0.959、Na–O3 2.247、Na–O5 2.194 Å（Na⁺ 仍桥联甲氧基 O3 + 酯氧 O5，与 I1/I2 同一支）。
- 选择依据：attempt 1 从 2.417 Å **向产物侧**下滑 ⇒ 脊线在更短 r 一侧；2.044 Å 落在 I1(1.503) 与 2.417 之间、且明显偏离两端极小值。

## 声明侧同步更正
- reaction_center 由 1-based 改为化学正确的 [[4,3],[4,6]]（C4–O3 断 / C4–O5 π 成）。attempt 1 误写成 [[3,2],[3,5]]（被平台按 1-based 读成 O3–C2 / O3–O1），仅影响模式归属判据，不影响几何。
