## 观察

两个独立的 Gaussian 16 作业，route 都写 `maxcycles=200`，Link1 头也回显 `1/6=200`，但优化器从第 1 步起就打印 `Step number 1 out of a maximum of 100`，并在第 100 步以 `-- Number of steps exceeded,  NStep= 100` + `Error termination via Lnk1e ... l9999.exe` 结束。

## 证据（原生日志 + 行号，本机实测）

**1) job 1016（readfc 版 I2 极小值重优化）**
- 输入 `gold_finish_20261015/NY3/E2E3/i2_min_readfc_optfreq/i2_min_readfc.gjf` sha256 `d87d2480b9cd34b34af444f637bfc336c0ec8cdc4ded5ad74bc096495e383802`
- route（L87）：`#p opt=(readfc,maxcycles=200) freq b3lyp/def2svp empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=water)`
- 日志 `.../i2_min_readfc.log`：Link1 旗标 L90/L97/L105 = `1/6=200`；`Step number 1 out of a maximum of 100` @L735（其后每步均为 100）；共 100 个 Step、100 条 `SCF Done`；`-- Number of steps exceeded,  NStep= 100` @L43634；`Error termination request processed by link 9999.` @L43864；`Error termination via Lnk1e in /home/ly/g16/l9999.exe at Sat Oct 17 08:42:15 2026` @L43865。

**2) job 1012（同物种 calcfc 版）**
- 输入 `gold_finish_20261015/NY3/E2E3/i2_min_conv_optfreq/i2_min_conv.gjf`（route 同为 `opt=(...,maxcycles=200)`）
- 日志 L1096 = `Step number 1 out of a maximum of 100`；同样在 `NStep= 100` 处 l9999（08:19:32）。

**3) 失败型态一致**：两次都是「力判据接近达标、位移判据不达标」的软模振荡到第 100 步 —— job 1016 末次 Max Force 0.013265 NO / RMS Force 0.002429 NO / Max Disp 0.030493 NO；job 1012 末次 0.013017 / 0.002370 / 0.033467 / 0.013825（全 NO）。

## 问题

1) `maxcycles` 是否被输入生成层/平台覆盖（例如固定注入 100 或做上限裁剪）？还是 Gaussian Link1 的 `1/6` 与 opt 模块的步预算本来就不同源？若是后者，请给出真正提高步预算的合法字段（本战役需要 >100 步的软模优化）。
2) 在共享节点上这意味每个未收敛的软模优化最多可白耗 100 步 × 8 cpus。若 route 的 `maxcycles` 不生效，建议生成层显式校验该字段，或至少在输入回显里标注「真实步预算 = N」。

## 影响

本战役 NY3 的 E2/E3 端点修复链因此两次在同一处失败（job 1012、job 1016），被迫改走「换构象 + 整批重算参考能量」。这是平台行为问题，不构成任何化学结论。

## 复现

`grep -nE '1/6=|out of a maximum of|Number of steps exceeded' <log>`