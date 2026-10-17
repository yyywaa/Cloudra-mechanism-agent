# NR1_E2 · ts_prepare 声明草案 v2（预写就绪，**平台故障期不提交**）

v2 修订（按主协调 2026-10-15 复核意见 1–4）：①明确"kind=file 绑定 → 用我的序 → 保留现行 atom_map"并加 ts_inspect 核对步骤，备选 (b) 只写判据不硬编码；②evidence_refs 全部换成**已落盘存在的文件**（去掉尚不存在的 .log 与临时 .gjf.tmp）；③scan_start/坐标基说明；④备选兜底的触发判据 + 一次只改一处。
状态：草案。等 compute.db 写锁故障解除且主协调宣布恢复提交后再交。作者：E2 道 small_mol as_3554137d6af74102。
口径：气相（不写 SCRF）、charge=+1、multiplicity=1、26 原子 C6H17O3；正式级别 Gaussian 16 **B3LYP/def2SVP + EmpiricalDispersion=GD3BJ + Int(UltraFine) + SCF=Tight**；execution = **8 cpus / 10240 MB**。

## 0 坐标基与映射（复核意见 1 的落实）

- **主路线（a）= 用 `kind="file"` 的 conformers 绑定我自己的 xyz + mol_path**：runtime 以我 mol 定义的行序为绑定序，因此
  - `atom_map` 沿用我在**本道文件序**上用 `reaction_mapping` 得到的 26 项（binding_status=complete、binding_source=concrete、两端 identity 均 match）：
    `[1,2,3,7,18,19,4,5,6,8,9,10,11,12,13,14,15,16,17,20,21,22,23,24,25,26]`（product 行序 → reactant 行序）；
  - `reaction_center = [[5,7]]`（= 本道 I1 文件序 row5=C4=题面 map4、row7=O6=题面 map6，即题源 `break [[4,6]]`）。
  - 我两端文件的**逐行映射表**见 `E2_PREP_PROVENANCE.md` §3/§4（I1 row4=map3、row6=map5、row9=map8、row10=map9 由"按映射号书写的 SMILES token 序 + reaction_mapping 的 complete-label 唯一映射"确定，不是从坐标猜）。
- **提交后必做（关键）**：立即 `ts_inspect(run_id)` 读 `structures` 的 1-based 当前原子表，核对 (5,7) 是否确为 C4/O6、以及两端组分/元素计数 = 26 原子 / C6H17O3 / 电荷 +1 / 自旋 1。**若与我的序不同**：只用 `ts_resume` 改 `reaction.atom_map` 与 `reaction.reaction_center`（一次只改这一处，reason 写"按 ts_inspect 的当前原子表重算映射"）。watch pair 错会在唯一虚频的模式相关性上暴露。
- **备选（b）= 若 runtime 明确拒收我的 file 绑定并要求用 SMILES 建结构**：改用未映射的复杂体 SMILES（`O.CC(C)(O)C(C)(C)[OH2+]` / `O.O.C[C+](C)C(C)(C)O`），此时 **atom_map 必须按 reactant/product SMILES 的派生 token 序重算**——我不手数，而是对"runtime 实际绑定的两个具体结构文件"再跑一次 `reaction_mapping`（concrete binding）取回 `atom_map`，再用 `ts_resume` 一次性替换。
- **触发判据（复核意见 4）**：只有在工具返回明确错误（映射/结构不匹配、provided/invalid、或 ts_inspect 显示结构序与我的表不符）时才走 (b)；**同一次 ts_resume 只改一处**（要么只换 guess，要么只换 reaction 映射），保证失败可归因。

## 1 TsPrepareArgs 草案（主路线 a）

```json
{
  "input": {
    "reaction": {
      "reactant_smiles": "[OH2:1].[CH3:3][C:4]([CH3:5])([OH+:6][H:2])[C:7]([CH3:8])([CH3:9])[O:10][H:11]",
      "product_smiles": "[OH2:1].[OH:6][H:2].[CH3:3][C+:4]([CH3:5])[C:7]([CH3:8])([CH3:9])[O:10][H:11]",
      "charge": 1,
      "multiplicity": 1,
      "atom_map": [1,2,3,7,18,19,4,5,6,8,9,10,11,12,13,14,15,16,17,20,21,22,23,24,25,26],
      "reaction_center": [[5,7]]
    },
    "calculations": {
      "formal": {
        "engine": "gaussian",
        "method": "B3LYP",
        "basis_set": "def2SVP",
        "keywords": "empiricaldispersion=gd3bj scf=tight int=ultrafine"
      }
    },
    "conformers": {
      "reactant": {
        "kind": "file",
        "xyz_path": "gold_finish_20261015/NR1/E2/structures/build_I1/assembly/complex_candidate_000.xyz",
        "mol_path": "gold_finish_20261015/NR1/E2/structures/build_I1/assembly/complex_candidate_000.mol",
        "evidence_refs": [
          "gold_finish_20261015/NR1/E2/structures/build_I1/assembly/complex_candidate_000.xyz",
          "gold_finish_20261015/NR1/E2/structures/build_I1/assembly/complex_candidate_000.mol",
          "gold_finish_20261015/NR1/E2/logs/E2_I1_optfreq_c000.gjf"
        ],
        "optimization": {"ref": "formal"}
      },
      "product": {
        "kind": "file",
        "xyz_path": "gold_finish_20261015/NR1/E2/structures/build_I2/assembly/complex_candidate_000.xyz",
        "mol_path": "gold_finish_20261015/NR1/E2/structures/build_I2/assembly/complex_candidate_000.mol",
        "evidence_refs": [
          "gold_finish_20261015/NR1/E2/structures/build_I2/assembly/complex_candidate_000.xyz",
          "gold_finish_20261015/NR1/E2/structures/build_I2/assembly/complex_candidate_000.mol",
          "gold_finish_20261015/NR1/E2/logs/E2_I2_optfreq_c000.gjf"
        ],
        "optimization": {"ref": "formal"}
      }
    },
    "guess": {
      "kind": "scan",
      "calculation": {"ref": "formal"},
      "scans": [
        {"coord_type": "bond", "atoms": [5, 7], "scan_start": "<I1 优化后实测 r(C4–O6)>", "scan_end": 3.55, "scan_steps": 11}
      ],
      "freeze": []
    },
    "ts_optimization": {"ref": "formal"},
    "verification": {
      "frequency": {"ref": "formal"},
      "irc": {"ref": "formal"},
      "reactant_endpoint": {
        "seed": {
          "kind": "file",
          "xyz_path": "<I1 优化后末帧 xyz（job 911 终态后由 format_converter 从日志导出）>",
          "mol_path": "gold_finish_20261015/NR1/E2/structures/build_I1/assembly/complex_candidate_000.mol",
          "evidence_refs": ["gold_finish_20261015/NR1/E2/structures/build_I1/assembly/complex_candidate_000.xyz"]
        },
        "optimization": {"ref": "formal"},
        "frequency": {"ref": "formal"}
      },
      "product_endpoint": {
        "seed": {
          "kind": "file",
          "xyz_path": "<I2 优化后末帧 xyz>",
          "mol_path": "gold_finish_20261015/NR1/E2/structures/build_I2/assembly/complex_candidate_000.mol",
          "evidence_refs": ["gold_finish_20261015/NR1/E2/structures/build_I2/assembly/complex_candidate_000.xyz"]
        },
        "optimization": {"ref": "formal"},
        "frequency": {"ref": "formal"}
      }
    },
    "execution": {"cpus": 8, "memory_mb": 10240}
  }
}
```

说明：
- `conformers.*.xyz_path` 直接用**我的候选 xyz**（已存在）；job 911 / I2 终态后，我会把 `xyz_path` 换成"优化后末帧导出的 xyz"（新文件，仍是同一行序），并在 `evidence_refs` 里补上对应的**已存在**的 .log 绝对路径；端点 seed 同理。**任何指向尚不存在文件的 evidence_refs 一律不放**（复核意见 2）。
- `guess.kind="scan"` 的坐标号 = 绑定结构序 1-based（Gaussian 与结构同基）；`scan_start` **必须等于 I1 优化后 r(C4–O6) 的实测值**（用 log_parser + internal_coordinates 在优化几何上量），否则会触发 start_geometry_mismatch（E1 道实测提示）。`scan_end` 视实测值定：目标覆盖 1.5→3.55 Å 区间（约 0.2 Å 步长）。

### 1.1 evidence_refs 对应的真实文件 + sha256（全部**已落盘**可校验）

| 文件（绝对路径前缀 /home/ly/Cloudra-mechanism-agent/） | sha256 |
| --- | --- |
| gold_finish_20261015/NR1/E2/structures/build_I1/assembly/complex_candidate_000.xyz | b5e3d673e9a6c5f190f074cde41232d14abf3ee655b756afffbe42acf95ac186 |
| gold_finish_20261015/NR1/E2/structures/build_I1/assembly/complex_candidate_000.mol | b0f848c7953ff9e06066d1fca08a77dc36373f7301e63007e93e4a9eb87e7e3b |
| gold_finish_20261015/NR1/E2/structures/build_I2/assembly/complex_candidate_000.xyz | 5ecc2aae54a681669eb2d345af4dcfa36fa39ec97a2e68eac21e1dfc119d12ba |
| gold_finish_20261015/NR1/E2/structures/build_I2/assembly/complex_candidate_000.mol | 6d2ef839a3c743bce48b9d425fa9d5492956e92acec77a7c8c286328ebdcfeab |
| gold_finish_20261015/NR1/E2/logs/E2_I1_optfreq_c000.gjf | f2515d42dc458090cd384d00c83672b62945bfb0067cd4e5ff097720335728b5 |
| gold_finish_20261015/NR1/E2/logs/E2_I2_optfreq_c000.gjf | 4a12461e5e9df5d3dac4b979624b7f8792a6d7acf6d3a0de01eddc7c173305aa |
| gold_finish_20261015/NR1/E2/seeds/seed_stretch_C4O6_1.8A.xyz | 736e2e640c972d679571624421036a345fa4827d716372c0d7caf3158a64a79c |
| gold_finish_20261015/NR1/E2/seeds/seed_stretch_C4O6_2.2A.xyz | 1186e8710abc3031f8de0c68528fe9c8a72e86406e65caa95e8ae59360129948 |
| gold_finish_20261015/NR1/E2/seeds/seed_stretch_C4O6_2.6A.xyz | 7c58885349be5f262dc813d213729ba4252a15443e23eb438abbef0513a7e7a3 |
| gold_finish_20261015/NR1/E2/seeds/interp_idpp/img_05.xyz | f33cd60e1e19202139d93d9f693244d4ace5544f8f8530841f072d9b2d9bd431 |
| gold_finish_20261015/NR1/E2/seeds/interp_idpp/img_06.xyz | beed5516e2bfeda8748260ec89e6ad1df8125edcc870a01f7e44c47c2f2517ab |
| gold_finish_20261015/NR1/E2/seeds/interp_idpp/img_07.xyz | f7ef8b275e5845a6aa9e8549ed8febd08ea3e1fdf7748b8ae1515b3eb722cde8 |

`.log`（`logs/E2_I1_optfreq_c000.gjf.log`、`logs/E2_I2_optfreq_c000.gjf.log`）**当前不存在**，只在 job 911 / I2 终态后加入 evidence_refs（届时给出绝对路径 + sha256）。`E2_I1_optfreq_c000.gjf.tmp`（临时名，1567 B）不用作 evidence。

### 1.2 备选 guess（仅当 scan 无峰或被拒时，一次只改这一处）
- `{"kind":"provided", "xyz_path":"gold_finish_20261015/NR1/E2/seeds/interp_idpp/img_06.xyz", "evidence_refs":["gold_finish_20261015/NR1/E2/seeds/interp_idpp/img_06.xyz","gold_finish_20261015/NR1/E2/seeds/interp_idpp/img_05.xyz","gold_finish_20261015/NR1/E2/seeds/interp_idpp/img_07.xyz"]}`（IDPP 第 6 帧，r(C4–O6)=3.1809 Å；**坐标插值初猜，不是鞍点**）。
- 或 `seeds/seed_stretch_C4O6_2.2A.xyz`（刚性拉伸 2.2 Å；局限：两水被压到 ~2.2 Å）。

## 2 恢复后的执行顺序（8 cpus / 10240 MB，每包同刻 1 个本道作业）

1. **job 911**（I1 无约束 Opt+Freq，12c 排队中，保持原样）终态 → log_parser：`normal_termination`、`opt_converged`、`imaginary_frequencies`；internal_coordinates(analyze, charge=1)：O6(row7)–H ≤1.15 Å、O1(row1)···H ≥1.35 Å（**质子须留在 row7 侧，否则起点坍缩 → 记录步数/能量/末帧距离并上报待裁决，不擅自改图**）、片段数=2、r(C4–O6) 实测值；format_converter(log→xyz) 导出末帧。
2. **I2 无约束 Opt+Freq**（logs/E2_I2_optfreq_c000.gjf，8c/10GB，尚未提交）：核 0 虚频、3 片段、C+ sp2、r(C4–O6) ≥2.6 Å；若 C–O 重新成键/坍缩回 I1 → 如实记录（关键证据）。
3. **ts_prepare**（§1 草案；scan_start = 步骤 1 实测值）→ 自动推进 scan → OptTS(+CalcFC) → TS Freq → 双向 IRC → 两端 Opt/Freq；提交后立即 ts_inspect 核对 structures 原子表。
4. 核验链：TS 恰 1 虚频且位移以 (5,7) 为主（watch_pair_fraction ≥0.30）→ IRC 双向各有帧、自 TS 单调下降、r(C4–O6) 单调演化 → 两端 0 虚频、身份 O–H ≤1.15 / 另一侧 ≥1.35 Å、产物 r(C4–O6) ≥2.6 Å → **ΔE‡ = E(TS) − E(I1 极小值)**（纯电子能；只用本批本程序日志 "SCF Done" 原始行 + file:line）。
5. 若扫描单调无内部峰或 OptTS 反复坍缩：按裁决 E 交付 = 无约束优化 + 原生弛豫扫描原始数值证据 + "E2 是否与 E3 合并 / 是否记为无垒"裁决问题 + 建议值（**不回填、不填 0、不改图**）。

## 3 I1 起点候选推荐（非 QM，基于已有文件）

- builder MMFF94 排序：**candidate_000 = 0.000（推荐）**、candidate_001 = 0.000（对称等价取向）、candidate_002 = +0.147（甲基旋转异构）。
- 独立复核（`conformer_search` 复杂体装配 32 取向 → 3 簇）：rel 0.000（Boltzmann 59.7%）/ +0.234（40.3%）/ +4.544（0.0%）；前两簇水 H 键均挂在**质子化 O6**（r(O1···O)=2.49 Å，即 I1 所需 motif），第三簇为水同时靠近两个 OH 的桥式取向（2.47/2.90 Å）→ 起点 motif 稳健。
- **推荐 I1 起点 = complex_candidate_000.{xyz,mol}**（最低 MMFF、r(C4–O6)=1.426 Å、水−质子化 O6 H 键 2.479 Å），次选 candidate_002 作甲基构象检验；I2 推荐 candidate_000（−22.010 kcal，C+ sp2，r(C4···O6)=4.614 Å）。
