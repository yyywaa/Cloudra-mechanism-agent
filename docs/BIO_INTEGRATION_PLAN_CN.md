# Cloudra 生信整合方案（路线图 v3）

> 状态：**草案（bio-integration-plan 分支）** · 调研日期：2026-11-18
> 目标：将 Cloudra 从计算化学 Agent 扩展为覆盖结构生物学、组学、药物发现的自动科研平台。
> 结论先行：MCP 配置 ~8 个 + Skill 移植 ~5 份 + 自研工具封装 ~9 个 + 验收基准 1 个。

---

## 1. 设计原则

1. **不自建已有免费轮子**：数据查询/文献层全部走 MCP（零代码接入），SOP 层移植 Anthropic 开源 skills。
2. **自研只做两类事**：① 重型 GPU 推理（结构预测/设计），走 `submit_compute_job` 调度；② 高频薄封装（Agent 需要 JS 协议直接编排的原语）。
3. **长尾工具不封装**：装进运行环境 + 写 SKILL.md 教 Agent 用 bash 调用（fastp、seqkit、MAFFT 等）。
4. **合规优先**：引入任何数据源先审 license（见 §9）。

## 2. 现状盘点（已有的生信底座）

| 已有能力 | 位置 | 生信用途 |
|---|---|---|
| `pdb_inspect` / `pdb_clean` / `pymol_render` / `format_converter` | `cloudra/tools/` | 蛋白结构查看已具雏形 |
| 全套 MD（RMSD/RMSF/RDF/MSD） | registry | 蛋白-配体结合、构象分析下游 |
| QM/TS/IRC/NEB + DAG 机理图 | `cloudra/dag/` | 酶催化机理、反应能垒的验证层 |
| `molecular-docking` skill | `cloudra/skills/` | P4 方向 SOP 已在，缺工具封装 |
| `search`（OpenAlex/arXiv 后端） | `cloudra/tools/Searchtool/` | 文献检索，缺 PubMed 专精后端 |
| 四种扩展点：工具注册表 / Python 插件 / MCP / SKILL.md | `cloudra/tools/registry.py`、`cloudra/runtime_v2/plugins.py`、`cloudra/tools/mcp.py`、`cloudra/skills/` | 本方案的落点 |
| chem-kb 知识插件（SQLite KG + 证据等级卡片） | `cloudra/knowledge/plugin.py` | bio-kb 的镜像模板 |

## 3. 四层接入架构

```
┌─ 验收层：BixBench（custom_rollout 接入）
├─ 工具层：自研 ~9 个封装（GPU 件走 scheduler）
├─ SOP 层：移植 Anthropic skills ~5 份（SKILL.md 同构，改工具语法）
└─ 数据层：MCP ~8 个（config.yaml 零代码）
```

## 4. 阶段计划

| 阶段 | 内容 | 交付物 | 工作量 |
|---|---|---|---|
| **P0 数据层** | 6 个 MCP 接入 + 验证 Agent 可调用 | config.yaml + 连通性测试 | 零代码 |
| **P1 SOP 层** | 移植 5 份 Anthropic skills | `cloudra/skills/` 新增 5 目录 | 低 |
| **P2 结构漏斗** | ESMFold（粗筛）→ ColabFold（精算）→ Boltz-2（复合物+亲和力），走 scheduler | `structure_predict` 等工具 | 中（需 GPU） |
| **P3 组学** | Scanpy/scvi-tools 封装 + PyDESeq2 + decoupler | 组学分析工具组 | 中 |
| **P4 对接/药物** | Vina/DiffDock 封装 + DeepPurpose 活性 | 对接工具组（skill 已在） | 中 |
| **P5 设计闭环** | RFdiffusion + ProteinMPNN + binder-gauntlet 验收 SOP | design→predict→validate 闭环 | 高（需 GPU） |
| **P6 验收** | BixBench 子集跑分 + 报告 | `cloudra/benchmark/` 适配器 | 低 |
| backlog | 文献层 PaperQA2 嵌入、bio-kb 证据卡片、MS 谱图、成像（cellpose/Squidpy）、Synapse/Consensus | 按需启动 | — |

## 5. P0：MCP 数据层（立即可接，实测 2026-11-18）

来源：Anthropic [bio-research 插件](https://github.com/anthropics/knowledge-work-plugins/tree/main/bio-research) + Harvard ToolUniverse。全部经 MCP `initialize` 握手实测。

### 立即可接（无账号无 key）

```yaml
mcp_servers:
  pubmed:          # PubMed 文献（Anthropic 托管，NCBI E-utilities 前端）
    url: https://pubmed.mcp.claude.com/mcp
  biorxiv:         # bioRxiv/medRxiv 预印本（deepsense.ai 构建，Anthropic 托管）
    url: https://hcls.mcp.claude.com/biorxiv/mcp
  chembl:          # ChEMBL v34 化合物/活性数据 —— 化学侧最有价值
    url: https://hcls.mcp.claude.com/chembl/mcp
  c-trials:        # ClinicalTrials.gov API v2
    url: https://hcls.mcp.claude.com/clinical_trials/mcp
  opentargets:     # 靶点-疾病关联（官方 platform-mcp，Apache-2.0）
    url: https://mcp.platform.opentargets.org/mcp
  tooluniverse:    # Harvard Zitnik lab，2700+ 工具 + 153 skills，极活跃
    command: uvx
    args: ["--refresh", "tooluniverse"]
    env:
      PYTHONIOENCODING: "utf-8"
```

注意：远程连接只写 `url`（可选 `headers`），本地连接只写 `command/args/env/cwd`，**无 `type` 字段**（见 `docs/CONFIGURATION_CN.md` 与 `cloudra/infra/config.py` 的 `MCPStdioServerConfig | MCPHTTPServerConfig`，均 `extra="forbid"`）。需安装 `cloudra[mcp]` 依赖。

### 次级（有免费账号即接）

| 服务 | 接入 | 备注 |
|---|---|---|
| Synapse（Sage Bionetworks） | 本地 stdio + `SYNAPSE_PAT`（[synapse-mcp](https://github.com/Sage-Bionetworks/synapse-mcp)，MIT） | 70+ 工具；ToS 禁数据再分发，走本地 PAT |
| Consensus | http + `Authorization: Bearer $KEY` | 免费档可用，超额 $0.05/次；headless 用 API key |

### 排除（需商业账号或不可用）

Benchling（插件内 URL 为空占位）、Owkin（端点 403，疑 WAF）、10x txg-mcp（需 10x 云订阅）、Wiley / BioRender（商业订阅）。BioRender 仅科研插画需要，可跳过。

### 依赖风险

`*.mcp.claude.com` 四个端点由 Anthropic 托管，**非我方基础设施**，SLA 无承诺（已知偶发不可用：anthropics/healthcare#40）。云端点不可用时降级路径：BioMCP（[genomoncology/biomcp](https://github.com/genomoncology/biomcp)，可 stdio 自托管，覆盖 PubMed/ClinicalTrials/变异）+ ToolUniverse 的多源文献工具。

## 6. P1：SKILL 移植层

Cloudra 的 `cloudra/skills/<name>/SKILL.md`（frontmatter：`name`/`description`/`license`/`metadata`）与 Anthropic Agent Skills 同构，移植 = 拷目录 + 把正文工具调用改为 Cloudra 原生工具（`bash`/`read`/`write`/MCP 工具）。

| Skill | 来源 | 内容 | 对应阶段 |
|---|---|---|---|
| single-cell-rna-qc | bio-research 插件 | scanpy MAD 质控 SOP | P3 |
| scvi-tools | bio-research 插件 | scVI/scANVI/totalVI 整合/批次校正/多模态 | P3 |
| nextflow-development | bio-research 插件 | 用 nf-core（rnaseq/sarek/atacseq）跑 GEO/SRA 公共数据 | P3 可选 |
| binder-gauntlet | [anthropics/life-sciences](https://github.com/anthropics/life-sciences) | de novo binder 独立复测/developability/dossier | P5 验收 |
| scientific-problem-selection | anthropics/life-sciences | 科研选题方法论（Cell 2024） | 立项增强，可与 research-pipeline 流程互补 |

移植时在 frontmatter 加 `metadata.source` 标注上游 commit，便于同步。

## 7. P2-P5：自研工具层（~9 个封装）

### P2 结构三级漏斗（走 `submit_compute_job`，需 GPU）

| 工具 | 引擎 | 定位 |
|---|---|---|
| `structure_predict_quick` | ESMFold | 秒级粗筛，免 MSA |
| `structure_predict` | ColabFold (AF2) | 精算，含配体模式 |
| `complex_predict` | [Boltz-2](https://github.com/jwohlwend/boltz) | 蛋白/DNA/RNA/小分子共折叠 + **结合亲和力**（喂给 DAG 机理图当证据） |

### P4 对接/药物发现

| 工具 | 引擎 | 备注 |
|---|---|---|
| `dock_ligand` | AutoDock Vina / DiffDock | `molecular-docking` skill 已在 |
| `activity_predict` | DeepPurpose | 配合 chembl MCP 的活性数据 |

### P5 设计闭环

| 工具 | 引擎 | 备注 |
|---|---|---|
| `protein_backbone_generate` | RFdiffusion | 需 GPU（Mac 本地跑不动，走 SSH/SLURM 远程节点） |
| `protein_sequence_design` | ProteinMPNN | 闭环：生成→序列→Boltz-2 复测→binder-gauntlet 验收 |

### P3 组学 + 文献增强（backlog 优先级最高项）

| 项 | 引擎 | 备注 |
|---|---|---|
| 组学工具组 | Scanpy/scvi-tools/PyDESeq2/decoupler | 薄封装核心步骤，其余走 SKILL.md + bash |
| `paper_qa` | [PaperQA2](https://github.com/Future-House/paper-qa)（Apache-2.0） | 可嵌入 Python 库，本地 PDF 语料带引用问答；LiteLLM 可接自有端点；**pin 版本**（v5 有破坏性变更，CalVer 迭代快） |

## 8. P6：验收基准（BixBench）

- [BixBench](https://github.com/Future-House/BixBench)（Apache-2.0）：205 题 / 60 个真实已发表论文的 Jupyter capsules，数据在 HuggingFace `futurehouse/BixBench`。
- 接入点：实现 `generate_trajectories.py` 的 `custom_rollout`，输出其 JSON trajectory 格式，`postprocessing.py` 打分。
- 执行环境复用其 Docker 镜像 `futurehouse/bixbench:aviary-notebook-env`（内置常用生信包），可同时充当 Cloudra 生信工具沙箱底座。
- **策略**：先跑 zero-shot 子集（全量 agentic 评测 24-48h + 大额 API 费），作为"生信自动研究能力"的量化基线，与文献公开分数对比（参考：Claude Code 在 Verified-50 子集 65.3%，注意各厂商分数互不可比，只用同题集同协议自比）。

## 9. License 与合规清单

| 资产 | License | 注意 |
|---|---|---|
| ToolUniverse | Apache-2.0 | 无 |
| BixBench / PaperQA2 / ChEMBL 数据 | Apache-2.0 / EMBL-EBI 开放 | 无 |
| [snap-stanford/Biomni](https://github.com/snap-stanford/Biomni) | 代码 Apache-2.0，**数据湖有雷** | DisGeNET/miRTarBase/miRDB 等仅限非商用（NC-only），COSMIC/OMIM 等需商用授权；只借代码思想（`tool_description` 元数据格式、`create_mcp_server` 反向暴露、`commercial_mode` 过滤开关），**不引数据湖** |
| Synapse 数据 | 平台 ToS | 禁再分发，仅本地分析 |
| Anthropic skills | 各 skill 目录内标注 | 移植时保留 attribution |
| `*.mcp.claude.com` 端点 | Anthropic 托管 | 非合同承诺，留降级路径 |

## 10. 调研排雷记录（避免误信）

1. **Biomni "BixBench 88.7%" 是营销数字**：出自其商业衍生公司 Phylo 自建的 50 题子集（BixBench-Verified-50）自报；同一产品在完整版 BixBench 上仅 52.2%。引用分数时注明题集版本。
2. **BiomniGEM 不存在**：为吉林大学 iGEM 2025 团队项目的撞名。
3. **FutureHouse 平台 agent（Crow/Falcon/Owl/Wren/Kosmos）全部闭源**；开源的只有库与基准（paper-qa、BixBench、Finch、aviary/ldp）。
4. **ether0**（FutureHouse，Apache-2.0）：开放权重的化学推理模型，化学侧微调的候选底座，仓库不含训练代码。
5. Anthropic [life-sciences 市场](https://github.com/anthropics/life-sciences) 已移除的 4 个 skills（scvi-tools、single-cell-rna-qc、nextflow、allotrope）仍存活于 bio-research 插件，无需 git 考古。

## 11. 参考

- [Claude for Life Sciences 公告](https://www.anthropic.com/news/healthcare-life-sciences) · [bio-research 插件](https://github.com/anthropics/knowledge-work-plugins/tree/main/bio-research) · [anthropics/life-sciences](https://github.com/anthropics/life-sciences)
- [ToolUniverse](https://github.com/mims-harvard/tooluniverse)（[论文](https://arxiv.org/abs/2509.23426)）· [Open Targets MCP](https://github.com/opentargets/platform-mcp) · [synapse-mcp](https://github.com/Sage-Bionetworks/synapse-mcp)
- [PaperQA2](https://github.com/Future-House/paper-qa)（[超人文献综合论文](https://arxiv.org/abs/2409.13740)）· [BixBench](https://github.com/Future-House/BixBench)（[论文](https://arxiv.org/abs/2503.00096)）
- [Boltz-2](https://github.com/jwohlwend/boltz) · [Biomni](https://github.com/snap-stanford/Biomni)（[license 说明](https://github.com/snap-stanford/Biomni/blob/main/license_info.md)）
