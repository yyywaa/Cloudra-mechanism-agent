# HI1 共享基线：I1 / RC 端点身份核验与 (S)-I1 基线裁定

（2026-10-15 18:20，包 Coordinator as_84bdf87a0f94416c；用途：lane1=E1、lane2=E3、lane3=E2/EM1 共用）

## 1 结论（一条一行）

| 作业 | 原生日志（绝对路径） | 物种 | Cα（map16）实测 CIP | 虚频 | E(RB3LYP)/Eh | 结论 |
|---|---|---|---|---|---|---|
| 907 | `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/runs/RC_optfreq/RC_optfreq.log` | (S)-脯氨酸 + 丙酮 + 苯甲醛（3 分片，41 原子）反应物复合物 RC 极小值 | **S** | 0 | −939.308829219 | **E1 起点/参考极小值，可用** |
| 908 | `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/runs/I1_optfreq/I1_optfreq.log` | 烯胺 + 水 + 苯甲醛（3 分片，41 原子）I1 极小值 | **R ✗** | 0 | −939.308218263 | **不是 (S)：不可作 lane3 共享基线、不可作 E1 产物端点** |
| 924 | `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2EM1/runs/I1_optfreq/I1_S_optfreq.log`（排队中） | (S)-I1（起点 = E1/build/I1_S_start.xyz） | 起点几何 S（待成品核验） | 待核验 | 待核验 | **(S)-I1 基线（唯一候选）；lane1 的产物端点与 lane3 的参考极小值都用它** |

- 907 sha256 = `fa28545612332f69c60c0b778cd5dd1907b22b8ad36f6b1da7811da1295563ba`
- 908 sha256 = `d35b0abfdb25154e54d848bdbcf2bd7af387fb63a7f4a2229325d557d1d933eb`
- 908 输入 `E1/runs/I1_optfreq/I1_optfreq.gjf` sha256 = `fb9db8b79c78d333a32d2986f4d114e090b4e5e6d631f6a4c0855f1e26355b0f`；其坐标与 `gold_compute/grant_materials_20261001/raw/HI1/job_51/rc_clean_np8.xyz` **逐原子 maxdev = 0.0000 Å**（即用了历史 R 几何，尽管 gjf 注释声明 S）。
- 924 输入 `E2EM1/runs/I1_optfreq/I1_S_optfreq.gjf` sha256 = `8b843b95bb55f46921f9aa23f9c172d906261b881e433db4c419605913cef0a9`（= job_51 几何的 z 镜像，Cα=S 实测）。

## 2 可复现命令与原始输出（真实执行，2026-10-15 18:0x）

```
cd /home/ly/Cloudra-mechanism-agent
python3 gold_finish_20261015/HI1/shared/tools/hi1_cip_tools.py \
  gold_finish_20261015/HI1/E1/runs/I1_optfreq/I1_optfreq.log \
  gold_finish_20261015/HI1/E1/runs/RC_optfreq/RC_optfreq.log \
  gold_finish_20261015/HI1/E1/runs/I1_optfreq/I1_optfreq.gjf \
  gold_finish_20261015/HI1/E1/build/RC_start.xyz \
  gold_finish_20261015/HI1/E1/build/I1_S_start.xyz \
  gold_finish_20261015/HI1/E1/build/I1_start_from_job51.xyz \
  gold_compute/grant_materials_20261001/raw/HI1/job_51/rc_clean_np8.xyz
```

输出（原样）：

```
I1_optfreq.log        natoms=41 frags=3 CIP[8C=R(nb 7C,4N,9C,23H)]
RC_optfreq.log        natoms=41 frags=3 CIP[8C=S(nb 7C,4N,9C,23H)]
I1_optfreq.gjf        natoms=41 frags=3 CIP[8C=R(nb 7C,4N,9C,23H)]
RC_start.xyz          natoms=41 frags=3 CIP[8C=S(nb 7C,4N,9C,23H)]
I1_S_start.xyz        natoms=41 frags=3 CIP[8C=S(nb 7C,4N,9C,23H)]
I1_start_from_job51.xyz natoms=41 frags=3 CIP[8C=R(nb 7C,4N,9C,23H)]
rc_clean_np8.xyz      natoms=41 frags=3 CIP[8C=R(nb 7C,4N,9C,23H)]
  maxdev I1_optfreq.gjf vs I1_start_from_job51.xyz = 0.0000 A
  maxdev I1_optfreq.gjf vs rc_clean_np8.xyz        = 0.0000 A
  maxdev I1_start_from_job51.xyz vs rc_clean_np8.xyz = 0.0000 A
  maxdev I1_optfreq.gjf vs I1_S_start.xyz          = 10.9831 A
```

方法：脚本取 log 最后一个 `Standard orientation` 块（优化后几何）→ RDKit `rdDetermineBonds.DetermineBonds(charge=0)` 判连接与分片 → `AssignStereochemistryFrom3D` + `AssignCIPLabels` 读实测 CIP。
工具 sha256：`shared/tools/hi1_cip_tools.py`（首版 `6c508d554c99d46ea22f72886c1a7713d00005b9baa52972621fe9871bd1dfc5`，其后仅增加 .gjf 读取分支）。

## 3 对三条道的直接后果
1. **lane1（E1）**：RC(907)=S 与 I1(908)=R 互为对映体，R↔S 不是基元步 → 不能在这两个端点之间找 TS/跑 IRC。E1 的产物端点必须用 924（(S)-I1）；E1 链 run = `/home/ly/Cloudra-mechanism-agent/ts/ts_0004`。
2. **lane2（E3）**：E3 起点 I2 自建（job 925 重提），与本表无关，但**不得**用 908 的任何几何当 I2/I1 身份参考。
3. **lane3（E2/EM1）**：共享参考极小值改为 **924**（不是 908）；两通道能垒都相对它相减。
