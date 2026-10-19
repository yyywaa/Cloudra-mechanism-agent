# E1 原始证据包（IRC 外帧 → 端点 Opt 链接）

- 题目：`E1`（easy，F⁻ + CH₃CH₂Cl → C₂H₄ + HF + Cl⁻）
- 批次：`batch_62c7ba4977e247fc`，运行数据目录 `/home/ly/cloudra-bench-run2-20261019`
- 代码版本：`origin/master` @ `42eda240`
- 来源路径：`sandboxes/E1/batch_62c7ba4977e247fc/`
- 打包日期：2026-10-19
- 计算引擎：Gaussian 16 Rev C.01（`/home/ly/g16`），B3LYP-D3(BJ)/def2-SVP，气相，q=-1，mult=1

## 目录内容

```
calc/ts1.gjf, calc/ts1.log               TS 优化+频率（1 虚频 -299.6111 cm-1，E=-639.002077473）
calc/irc1.gjf, calc/irc1.log             IRC 尝试 1（失败的早期尝试，保留原始字节）
calc/irc2.gjf, calc/irc2.log             IRC 尝试 2
calc/irc3.gjf, calc/irc3.log             双向 IRC（本条争议的原始日志；141 forward / 39 reverse）
calc/irc4_fwd.gjf, calc/irc4_fwd.log     单向前向 IRC 复算
calc/irc4_rev.gjf, calc/irc4_rev.log     单向反向 IRC 复算
calc/endpoint_rev5.gjf/.log              反向最外帧的端点 Opt+Freq（0 虚频，E=-639.003420924）
calc/endpoint_rev6.gjf/.log              反向端点重复
calc/endpoint_fwd5.gjf/.log              正向最外帧的端点 Opt+Freq（0 虚频，E=-639.022951022）
calc/endpoint_fwd6.gjf/.log              正向端点重复
calc/rc2.gjf, calc/rc2.log               反应物复合物极小值（0 虚频，E=-639.003420935）
mechanism_graph.json                     交付的机制图（graph revision 20）
tool_calls/dag_tool_calls_E1.json        E1 的 88 条 DAG/TS 工具调用（入参 + 原始结构化返回）
tool_calls/seq_4761.json                 seq 4736（请求）/ seq 4761（返回）这一对
notes/failure_notes.json                 benchmark 侧 E1 的 127 条 notes（final=0.0667, graph=0.667, sc=0, acc=0）
SHA256SUMS                               全部文件校验和
```

## 争议点：同一 IRC 点的两份原生打印

`calc/irc3.log` 中 Point 39 / REVERSE 被打印两次：

| 行号 | 段 | F 原子坐标 |
|---|---|---|
| 63351（以及收尾的 63875） | `Input orientation` | `-2.622372  -0.561443  -0.000012` |
| 63656 | IRC 块 `CURRENT STRUCTURE`（Point Number: 39, Path Number: 2） | `-2.622381  -0.561450  -0.000012` |

- `irc_endpoint_geometries(irc3.log)` 取 `CURRENT STRUCTURE` 版本
- `calc/endpoint_rev5.gjf` 的初始几何用的是 `Input orientation` 版本
- 逐原子最大 \|Δ\|：反向 3.7e-5 Å，正向 9.0e-6 Å；原子序一致（F,C,C,Cl,H×5）
- `same_geometry` 容差 `√3×1e-6 ≈ 1.73e-6 Å`

`calc/endpoint_rev5.log` 由该 `Input orientation` 几何起算，收敛末帧 0 虚频、E=-639.003420924（与 `calc/rc2.log` -639.003420935 相差 1.1e-8 Ha）；`calc/endpoint_fwd5.log` 同理，末帧 E=-639.022951022、0 虚频。

DAG 侧 `dag_submit_step_evidence`（seq 4761 返回）对 `short_irc` 的判定：

```
The actual IRC outer frames are not connected to both declared zero-imaginary
minima by converged optimization logs; geometric interval agreement alone is
not direction proof.
```

## 最小复算命令

在仓库根目录、已安装依赖的 venv 下，从本目录执行：

```bash
.venv/bin/python - <<'PY'
from pathlib import Path
from cloudra.tools.core.irc_evidence import irc_endpoint_geometries
from cloudra.tools.core.irc_path import same_geometry
from cloudra.tools.core.qm_log_facts import read_qm_log

root = Path('evidence/e1-irc-20261019')

# 1) 提取器看到的两个外帧
ends = irc_endpoint_geometries(root / 'calc/irc3.log')
print('frame[0]:', ends[0][0], ends[0][1][0])
print('frame[1]:', ends[1][0], ends[1][1][0])

# 2) 端点 Opt 的首帧（.gjf）与收敛末帧（.log）
import re
def gjf_first_geometry(path):
    lines = Path(path).read_text().splitlines()
    for i, line in enumerate(lines):
        if re.fullmatch(r'\s*-?\d+\s+\d+\s*', line):
            syms, pos = [], []
            for l2 in lines[i + 1:]:
                if not l2.strip():
                    break
                p = l2.split()
                syms.append(p[0]); pos.append([float(x) for x in p[1:4]])
            return syms, pos
    raise ValueError('no geometry')

rev_in = gjf_first_geometry(root / 'calc/endpoint_rev5.gjf')
fwd_in = gf = gjf_first_geometry(root / 'calc/endpoint_fwd5.gjf')
print('same_geometry(frame0, endpoint_rev5 input):', same_geometry(ends[0], rev_in))
print('same_geometry(frame1, endpoint_fwd5 input):', same_geometry(ends[1], fwd_in))

# 3) 数值差
import numpy as np
for name, frame, inp in (('rev', ends[0], rev_in), ('fwd', ends[1], fwd_in)):
    d = np.abs(np.array(frame[1], dtype=float) - np.array(inp[1], dtype=float)).max()
    print(f'{name}: max |delta| = {d:.3e} A')

# 4) 端点是否真是 0 虚频极小值
for f in ('calc/endpoint_rev5.log', 'calc/endpoint_fwd5.log'):
    facts = read_qm_log(root / f)
    n_imag = sum(1 for x in (facts.frequencies_cm or []) if x < 0) if facts.frequencies_cm else None
    print(f, 'normal=', facts.normal_termination, 'n_imag=', n_imag, 'E=', facts.electronic_energy_hartree)
PY
```

预期（本机实测）：

```
same_geometry(frame0, endpoint_rev5 input): False
same_geometry(frame1, endpoint_fwd5 input): False
rev: max |delta| = 3.700e-05 A
fwd: max |delta| = 9.000e-06 A
calc/endpoint_rev5.log normal= True n_imag= 0 E= -639.003420924
calc/endpoint_fwd5.log normal= True n_imag= 0 E= -639.022951022
```

## 透明度说明

打包过程中 `calc/ts1.log` 被一次错误的 `cp -p ts1.gjf ts1.log` 覆盖（687 B）。已从同一沙箱内的原始归档副本恢复：

```
.ccloudra/evidence/d3b57587ec8fa3ed_ts1.log
calc/.cloudra/execution-5/results/ts1.log
runtime/artifacts/art_3cf55d6406064b07a705ffcbbbf9eae1/ts1.log
```

三份副本 sha256 完全一致（`d3b57587ec8fa3ed0c4c46f29f64abd9c5c46f4fabdf2bc2600945b76299eacb`，843,916 B），恢复后重新解析仍为 `normal_termination=True, n_imag=1, opt_converged=True, E=-639.002077473`。文件内容与原字节一致；其 mtime 为原日志写入时间（20:03）。

## 备注

- 本分支只用于取证，不合并 `master`。
- `calc/irc1.log`、`calc/irc2.log` 是早期失败尝试，保留原始字节以便核对候选筛选逻辑。
