---
name: scvi-tools
description: Deep learning for single-cell analysis using scvi-tools. Use when users need (1) data integration and batch correction with scVI/scANVI, (2) ATAC-seq analysis with PeakVI, (3) CITE-seq multi-modal analysis with totalVI, (4) multiome RNA+ATAC analysis with MultiVI, (5) spatial transcriptomics deconvolution with DestVI, (6) label transfer and reference mapping with scANVI/scArches, (7) RNA velocity with veloVI, or (8) cross-technology integration with sysVI.
license: Apache-2.0
metadata:
  source: "https://github.com/anthropics/knowledge-work-plugins/tree/b4c9a4e1de4b42868b74a6fe30ac766f64e43a3e/bio-research/skills/scvi-tools"
  upstream-commit: "b4c9a4e1de4b42868b74a6fe30ac766f64e43a3e"
  upstream-license: "Apache-2.0"
  adapted-by: "Cloudra"
---

# scvi-tools Deep Learning Skill

This skill provides guidance for deep learning-based single-cell analysis using `scvi-tools`, the leading framework for probabilistic models in single-cell genomics.

## How to Use This Skill

1. Identify the appropriate workflow from the model/workflow tables below.
2. Load the corresponding reference file with `get_skill(skill_name="scvi-tools", reference="<filename>")` for detailed steps and code.
3. Run the modular scripts in `cloudra/skills/scvi-tools/scripts/` via `bash` (or `submit_compute_job` for GPU training) to avoid rewriting boilerplate code.
4. For installation or GPU issues, load `get_skill(skill_name="scvi-tools", reference="environment_setup.md")`.
5. For debugging convergence or data issues, load `get_skill(skill_name="scvi-tools", reference="troubleshooting.md")`.

## Cloudra Tooling & Biomedical Knowledge Integration

Anchor scvi-tools modeling and biological interpretation in Cloudra's native tools and biomedical MCP servers:

- **Validation & lightweight processing (`bash`)**: Run `validate_adata.py`, `prepare_data.py`, `cluster_embed.py`, and `differential_expression.py` under `cloudra/skills/scvi-tools/scripts/` via `bash`.
- **Heavy / GPU model training (`submit_compute_job` / `query_compute_job`)**: For large datasets or GPU-accelerated training (`train_model.py`, `integrate_datasets.py`, `transfer_labels.py`), write a shell wrapper script with `write` and submit asynchronously via `submit_compute_job(job_type="shell", is_async=True)`, then monitor via `query_compute_job`.
- **Custom workflows (`write` / `edit`)**: Author or adjust Python analysis scripts importing `scripts/model_utils.py` using `write` and `edit` (never shell redirection or `sed`).
- **Result & figure inspection (`read`)**: Use `read` to inspect UMAP/clustering PNG figures, training loss logs, and differential expression CSV outputs (`de.csv`).
- **On-demand references (`get_skill`)**: Load any bundled reference guide via `get_skill(skill_name="scvi-tools", reference="<file>.md")` (and run `get_skill(skill_name="single-cell-rna-qc")` first if input `.h5ad` files have not yet undergone QC).
- **Experimental design confirmation (`ask_user`)**: Confirm `batch_key`, `labels_key`, target model choice, and reference atlas selection with `ask_user` when not explicitly specified.
- **Marker interpretation, literature & target discovery (MCP + `search`/`browser`)**:
  - Use `mcp__pubmed__search_articles`, `mcp__pubmed__get_article_metadata`, `mcp__pubmed__get_full_text_article`, and `mcp__biorxiv__search_preprints` (plus native `search` with `source=openalex`/`web` or `browser` for `docs.scvi-tools.org`) to validate cell-type marker genes, tissue signatures, and model benchmarks.
  - Use `mcp__opentargets__search_entities` and `mcp__opentargets__query_open_targets_graphql` to link differentially expressed genes or disease-enriched cell-state markers to target-disease associations and tractability.
  - Use `mcp__chembl__target_search`, `mcp__chembl__get_bioactivity`, and `mcp__tooluniverse__find_tools` / `mcp__tooluniverse__execute_tool` to query bioactive compounds, pathway annotations, or complementary single-cell knowledge bases for candidate markers.

## When to Use This Skill

- When `scvi-tools`, scVI, scANVI, or related models are mentioned
- When deep learning-based batch correction or integration is needed
- When working with multi-modal data (CITE-seq, multiome)
- When reference mapping or label transfer is required
- When analyzing ATAC-seq or spatial transcriptomics data
- When learning latent representations of single-cell data

## Model Selection Guide

| Data Type | Model | Primary Use Case |
|-----------|-------|------------------|
| scRNA-seq | **scVI** | Unsupervised integration, DE, imputation |
| scRNA-seq + labels | **scANVI** | Label transfer, semi-supervised integration |
| CITE-seq (RNA+protein) | **totalVI** | Multi-modal integration, protein denoising |
| scATAC-seq | **PeakVI** | Chromatin accessibility analysis |
| Multiome (RNA+ATAC) | **MultiVI** | Joint modality analysis |
| Spatial + scRNA reference | **DestVI** | Cell type deconvolution |
| RNA velocity | **veloVI** | Transcriptional dynamics |
| Cross-technology | **sysVI** | System-level batch correction |

## Workflow Reference Files

Load any file below with `get_skill(skill_name="scvi-tools", reference="<filename>")`:

| Workflow | Reference File | Description |
|----------|---------------|-------------|
| Environment Setup | [references/environment_setup.md](references/environment_setup.md) | Installation, GPU, version info |
| Data Preparation | [references/data_preparation.md](references/data_preparation.md) | Formatting data for any model |
| scRNA Integration | [references/scrna_integration.md](references/scrna_integration.md) | scVI/scANVI batch correction |
| ATAC-seq Analysis | [references/atac_peakvi.md](references/atac_peakvi.md) | PeakVI for accessibility |
| CITE-seq Analysis | [references/citeseq_totalvi.md](references/citeseq_totalvi.md) | totalVI for protein+RNA |
| Multiome Analysis | [references/multiome_multivi.md](references/multiome_multivi.md) | MultiVI for RNA+ATAC |
| Spatial Deconvolution | [references/spatial_deconvolution.md](references/spatial_deconvolution.md) | DestVI spatial analysis |
| Label Transfer | [references/label_transfer.md](references/label_transfer.md) | scANVI reference mapping |
| scArches Mapping | [references/scarches_mapping.md](references/scarches_mapping.md) | Query-to-reference mapping |
| Batch Correction | [references/batch_correction_sysvi.md](references/batch_correction_sysvi.md) | Advanced batch methods |
| RNA Velocity | [references/rna_velocity_velovi.md](references/rna_velocity_velovi.md) | veloVI dynamics |
| Troubleshooting | [references/troubleshooting.md](references/troubleshooting.md) | Common issues and solutions |

## CLI Scripts

Modular scripts for common workflows live in `cloudra/skills/scvi-tools/scripts/`. Chain them together via `bash` or wrap them in a job script submitted through `submit_compute_job`.

### Pipeline Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `prepare_data.py` | QC, filter, HVG selection | `python scripts/prepare_data.py raw.h5ad prepared.h5ad --batch-key batch` |
| `train_model.py` | Train any scvi-tools model | `python scripts/train_model.py prepared.h5ad results/ --model scvi` |
| `cluster_embed.py` | Neighbors, UMAP, Leiden | `python scripts/cluster_embed.py adata.h5ad results/` |
| `differential_expression.py` | DE analysis | `python scripts/differential_expression.py model/ adata.h5ad de.csv --groupby leiden` |
| `transfer_labels.py` | Label transfer with scANVI | `python scripts/transfer_labels.py ref_model/ query.h5ad results/` |
| `integrate_datasets.py` | Multi-dataset integration | `python scripts/integrate_datasets.py results/ data1.h5ad data2.h5ad` |
| `validate_adata.py` | Check data compatibility | `python scripts/validate_adata.py data.h5ad --batch-key batch` |

### Example Workflow

```bash
SCRIPTS="cloudra/skills/scvi-tools/scripts"

# 1. Validate input data
python "$SCRIPTS/validate_adata.py" raw.h5ad --batch-key batch --suggest

# 2. Prepare data (QC, HVG selection)
python "$SCRIPTS/prepare_data.py" raw.h5ad prepared.h5ad --batch-key batch --n-hvgs 2000

# 3. Train model (submit via submit_compute_job on GPU for large datasets)
python "$SCRIPTS/train_model.py" prepared.h5ad results/ --model scvi --batch-key batch

# 4. Cluster and visualize
python "$SCRIPTS/cluster_embed.py" results/adata_trained.h5ad results/ --resolution 0.8

# 5. Differential expression
python "$SCRIPTS/differential_expression.py" results/model results/adata_clustered.h5ad results/de.csv --groupby leiden
```

### Python Utilities

`scripts/model_utils.py` provides importable functions for custom workflows:

| Function | Purpose |
|----------|---------|
| `prepare_adata()` | Data preparation (QC, HVG, layer setup) |
| `train_scvi()` | Train scVI or scANVI |
| `evaluate_integration()` | Compute integration metrics |
| `get_marker_genes()` | Extract DE markers |
| `save_results()` | Save model, data, plots |
| `auto_select_model()` | Suggest best model |
| `quick_clustering()` | Neighbors + UMAP + Leiden |

## Critical Requirements

1. **Raw counts required**: scvi-tools models require integer count data
   ```python
   adata.layers["counts"] = adata.X.copy()  # Before normalization
   scvi.model.SCVI.setup_anndata(adata, layer="counts")
   ```

2. **HVG selection**: Use 2000–4000 highly variable genes
   ```python
   sc.pp.highly_variable_genes(adata, n_top_genes=2000, batch_key="batch", layer="counts", flavor="seurat_v3")
   adata = adata[:, adata.var['highly_variable']].copy()
   ```

3. **Batch information**: Specify `batch_key` for integration
   ```python
   scvi.model.SCVI.setup_anndata(adata, layer="counts", batch_key="batch")
   ```

## Quick Decision Tree

```
Need to integrate scRNA-seq data?
├── Have cell type labels? → scANVI (references/label_transfer.md)
└── No labels? → scVI (references/scrna_integration.md)

Have multi-modal data?
├── CITE-seq (RNA + protein)? → totalVI (references/citeseq_totalvi.md)
├── Multiome (RNA + ATAC)? → MultiVI (references/multiome_multivi.md)
└── scATAC-seq only? → PeakVI (references/atac_peakvi.md)

Have spatial data?
└── Need cell type deconvolution? → DestVI (references/spatial_deconvolution.md)

Have pre-trained reference model?
└── Map query to reference? → scArches (references/scarches_mapping.md)

Need RNA velocity?
└── veloVI (references/rna_velocity_velovi.md)

Strong cross-technology batch effects?
└── sysVI (references/batch_correction_sysvi.md)
```

## Key Resources

- [scvi-tools Documentation](https://docs.scvi-tools.org/)
- [scvi-tools Tutorials](https://docs.scvi-tools.org/en/stable/tutorials/index.html)
- [Model Hub](https://huggingface.co/scvi-tools)
- [GitHub Issues](https://github.com/scverse/scvi-tools/issues)

## Attribution & License

Adapted for Cloudra from Anthropic's `knowledge-work-plugins` (`bio-research/skills/scvi-tools`, commit `b4c9a4e1de4b42868b74a6fe30ac766f64e43a3e`) under the **Apache License 2.0** (see bundled `LICENSE.txt`). Modifications for Cloudra include native tool/compute-job mappings (`bash`, `submit_compute_job`, `read`, `write`, `get_skill`, `ask_user`) and biomedical MCP integration guidance.

## Applicable Scenarios

- Integrating multi-batch or cross-technology single-cell RNA-seq atlases (scVI/sysVI) and performing Bayesian differential expression or imputation on raw UMI counts.
- Transferring cell-type annotations and mapping new query datasets onto pre-trained reference atlases via scANVI and scArches.
- Analyzing single-cell chromatin accessibility (PeakVI), paired multi-modal CITE-seq (totalVI) or RNA+ATAC multiome (MultiVI), spatial transcriptomics deconvolution (DestVI), and RNA velocity (veloVI).
- Connecting scvi-tools cluster markers and DE signatures to literature and drug-target evidence using Cloudra's PubMed, Open Targets, ChEMBL, and ToolUniverse MCP servers.
