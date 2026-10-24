# HI1_E4 · 几何量与证据溯源（PROVENANCE）

生成脚本：`analysis/geom_table.py`（读 Input orientation / xyz，不做任何单位或坐标系变换；距离单位 Å）
产生时间：2026-10-18 03:5x（等待 ts_opt job 1090 期间完成，freq 一出即可直接判方向）

## 1 帧与来源

| 帧 | 文件 | 说明 |
|---|---|---|
| TS_old_decl0007 | ts/ts_0016/jobs/declaration_0007/frequency/frequency.log，Input orientation 块起始 **L219**（末块），sha256 **c5ac84026e43c5155f2bf6e20787885f77662666e737ad4783e16036ae7291b9** | 旧 run 的单虚频驻点（L1501 `1 imaginary frequencies`，L1510 = -783.7914 cm-1），E = -939.295152015081（L785） |
| guess_provided | ts/ts_0016/path/input_0007/provided.xyz，sha256 **e3748c2c6c96af915c63d1fa8972187214916321999720667a68c9b2dd561b9e** | 本 run ts_0024 的 TS guess（41 原子，S2 插值 λ=0.5306，R(C2-O25)=1.82） |
| I2_min_job961 | gold_finish_20261015/HI1/E3/runs/I2_optfreq/I2_min_v5.xyz，sha256 **9a6203ff67d9f0d95ad774e78b17bc397b22992f24cbcdf448f8c5558142ef2b**；日志 I2_optfreq.log，sha256 **63dda25e04529e65920526304fb88755db9393e9c22bd3a6efb76eeee0af0d0e** | 本步分母（起点极小值）：E = **-939.320655479 Ha**（L19183），117 模 0 虚频（`Frequencies --` 首行 L19879，Low frequencies L19869/19870） |
| P_hemiaminal_job1028 | gold_finish_20261015/HI1/E3/prep/hemiaminal_1028_lastframe.xyz，sha256 **be789d5fd013d11ec84b295f4249c61616a8e4de21e129e319c13497faab572d**；日志 interm_c160_optfreq.log，sha256 **1ec7e4c6388415d0859939238f4f96ec7739c0bbf1f985a28f4dd3c23b7dcec1** | 声明产物 P（41 原子 hemiaminal），117 模 0 虚频 |

## 2 关键距离表（Å）

```
frame                             R(2,25)     R(2,4)   R(10,27)   R(25,27)   R(28,24)   R(25,24)   R(25,26)   R(10,11)
TS_old_decl0007_freqL219           1.861      1.343      1.247      1.164      0.967      4.536      0.969      2.225
guess_provided.xyz                 1.817      1.349      1.247      1.279      0.975      4.295      0.963      2.140
I2_min_job961                      3.160      1.299      1.717      0.990      0.984      4.651      0.966      2.249
P_hemiaminal_job1028               1.473      1.425      0.995      1.634      0.967      4.216      0.969      2.208
```

## 3 读数结论（几何级，非能量级）

1. **R(2,25)**: I2 3.160 → TS 1.861 → P 1.473，单调缩短 ⇒ TS 处在"水 O 走近亚铵 C2"的半途 ✓（声明 form (2,25)）
2. **R(2,4)**: I2 1.299 → TS 1.343 → P 1.425，单调拉长 ⇒ 亚铵 C=N π 键在半途断裂 ✓（声明 break (2,4)）
3. **R(25,27)**: I2 0.990 → TS 1.164 → P 1.634，单调拉长 ⇒ 水的一根 O-H 在断（声明 break (25,27)）
4. **R(10,27)**: I2 1.717 → TS 1.247 → P 0.995，单调缩短 ⇒ 该质子落到羧基 O10 上（声明 form (10,27)）
5. **R(28,24)** = 0.967~0.984（全路径恒定共价 O-H），**R(25,24)** = 4.22~4.65 Å（全程不接触）⇒ 题库把 map22 译成工作序 atom 24 是错位；atom 24 是醇羟基氢，不参与本步任何键变化。平台在 rev38 以 `reaction_center_distance_out_of_range` 拒收原申报，与此表一致。
6. R(10,11) = 2.14~2.25 Å（羧基两个 O 间距基本不变，两性离子→COOH 只换质子不换骨架）。

## 4 待补充（freq 出结果后填）
- 新 run ts_0024 的 TS 能量、虚频、三项份额
- IRC 双向末帧与 I2/P 的 RMSD、maxpoints 是否生效
- 两端 Opt+Freq 的 0 虚频与身份（CIP / 质子归属 / 水是否完整）

## 6 平台限制证据：ts_resume 改 execution 不回改已排队作业（2026-10-18 04:1x）
- 时间顺序（均为 ts_inspect / process.json 直读，非转述）：
  1. ts_resume(仅 execution.cpus=4, execution.memory_mb=6144) 被接受：run ts_0024 **revision 49**，`receipt.changes = ["execution.cpus","execution.memory_mb"]`。
  2. 但已排队作业未被改小，ts_inspect 读回 waiting 项原文仍是：
     `{"job_id": 1090, "purpose": "ts_opt", "state": "ready", "req_cpus": 8, "req_memory_mb": 10240, "start_timestamp": -1, "source_input_revision": 10, "attempt": 1, "input_path": "ts/ts_0024/jobs/declaration_0010/ts_opt/refine.gjf"}`
  3. 队列实测（query_compute_queue）：running 1074/1080/1082/1085 各 8c；queued 1086/1087/1088/1089/1090 各 8c + 1092 4c；free cpus=0。
  4. 按主协调裁决走 ts_stop → ts_resume(changes={})：job 1090 变 **cancelled**，同一 declaration 重提为 **job 1094，req_cpus=4，req_memory_mb=6144**（declaration_revision 12，输入 ts/ts_0024/jobs/declaration_0012/ts_opt/refine.gjf）；receipt.invalidated = [{declaration_revision:10, stage_key:"ts_opt", attempt:1, job_id:1090}]，retained=[]。
- 结论：**execution 改动只对今后新提交生效；排队中的作业要降配只能撤回重提**（ts_stop → ts_resume）。ts_resume 单改 execution 不会报错，但排队作业保留原 req_cpus —— 静默不生效，需以 ts_inspect 的 waiting 项核对，不要以 receipt 判断。
