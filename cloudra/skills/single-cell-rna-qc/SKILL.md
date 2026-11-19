---
name: single-cell-rna-qc
description: Performs quality control on single-cell RNA-seq data (.h5ad or .h5 files) using scverse best practices with MAD-based filtering and comprehensive visualizations. Use when users request QC analysis, filtering low-quality cells, assessing data quality, or following scverse/scanpy best practices for single-cell analysis.
license: Apache-2.0
metadata:
  source: "https://github.com/anthropics/knowledge-work-plugins/tree/b4c9a4e1de4b42868b74a6fe30ac766f64e43a3e/bio-research/skills/single-cell-rna-qc"
  upstream-commit: "b4c9a4e1de4b42868b74a6fe30ac766f64e43a3e"
  upstream-license: "Apache-2.0"
  adapted-by: "Cloudra"
---

# Single-Cell RNA-seq Quality Control

Automated QC workflow for single-cell RNA-seq data following scverse best practices.

## When to Use This Skill

Use when users:
- Request quality control or QC on single-cell RNA-seq data
- Want to filter low-quality cells or assess data quality
- Need QC visualizations or metrics
- Ask to follow scverse/scanpy best practices
- Request MAD-based filtering or outlier detection

**Supported input formats:**
- `.h5ad` files (AnnData format from scanpy/Python workflows)
- `.h5` files (10X Genomics Cell Ranger output)

**Default recommendation**: Use Approach 1 (complete pipeline) unless the user has specific custom requirements or explicitly requests non-standard filtering logic.

## Cloudra Tooling & Biomedical Knowledge Integration

Anchor single-cell QC execution and biological verification in Cloudra's native tools and biomedical MCP servers:

- **Script execution (`bash`)**: Run the bundled QC script under `cloudra/skills/single-cell-rna-qc/scripts/qc_analysis.py` or custom Python scripts in the active environment.
- **Visual & report inspection (`read`)**: Directly inspect generated diagnostic PNG figures (`qc_metrics_before_filtering.png`, `qc_filtering_thresholds.png`, `qc_metrics_after_filtering.png`) and text logs with `read` to verify that MAD bounds and MT% cutoffs are biologically sound before proceeding.
- **Custom script authoring (`write` / `edit`)**: Author or revise custom QC scripts built on `scripts/qc_core.py` and `scripts/qc_plotting.py` using `write` and `edit` (never shell redirection or `sed`).
- **Detailed methodology (`get_skill`)**: Load the bundled scverse guidelines via `get_skill(skill_name="single-cell-rna-qc", reference="scverse_qc_guidelines.md")`.
- **Threshold confirmation (`ask_user`)**: Confirm species/tissue-specific exceptions (such as higher MT% cutoffs for neurons, cardiomyocytes, or tumor biopsies) with `ask_user` when dataset metadata is ambiguous.
- **Literature & gene-nomenclature verification (MCP + `search`)**:
  - Use `mcp__pubmed__search_articles`, `mcp__pubmed__get_article_metadata`, `mcp__pubmed__get_full_text_article`, or `mcp__biorxiv__search_preprints` (or native `search` with `source=openalex`/`web`) to check tissue-specific mitochondrial fraction norms and published QC criteria for a specific cohort or protocol.
  - Use `mcp__tooluniverse__find_tools` and `mcp__tooluniverse__execute_tool` when verifying species gene-prefix conventions or downstream cell-type marker sets.

## Approach 1: Complete QC Pipeline (Recommended for Standard Workflows)

For standard QC following scverse best practices, run the convenience script `scripts/qc_analysis.py` via `bash` (located in `cloudra/skills/single-cell-rna-qc/scripts/qc_analysis.py`):

```bash
python3 cloudra/skills/single-cell-rna-qc/scripts/qc_analysis.py input.h5ad
# or for 10X Genomics .h5 files:
python3 cloudra/skills/single-cell-rna-qc/scripts/qc_analysis.py raw_feature_bc_matrix.h5
```

The script automatically detects the file format and loads it appropriately.

**When to use this approach:**
- Standard QC workflow with adjustable thresholds (all cells filtered the same way)
- Batch processing multiple datasets
- Quick exploratory analysis
- User wants the "just works" solution

**Requirements:** `anndata`, `scanpy`, `scipy`, `matplotlib`, `seaborn`, `numpy`

**Parameters:**

Customize filtering thresholds and gene patterns using command-line parameters:
- `--output-dir` - Output directory
- `--mad-counts`, `--mad-genes`, `--mad-mt` - MAD thresholds for counts/genes/MT%
- `--mt-threshold` - Hard mitochondrial % cutoff
- `--min-cells` - Gene filtering threshold
- `--mt-pattern`, `--ribo-pattern`, `--hb-pattern` - Gene name patterns for different species

Use `--help` to see current default values.

**Outputs:**

All files are saved to `<input_basename>_qc_results/` directory by default (or to the directory specified by `--output-dir`):
- `qc_metrics_before_filtering.png` - Pre-filtering visualizations
- `qc_filtering_thresholds.png` - MAD-based threshold overlays
- `qc_metrics_after_filtering.png` - Post-filtering quality metrics
- `<input_basename>_filtered.h5ad` - Clean, filtered dataset ready for downstream analysis
- `<input_basename>_with_qc.h5ad` - Original data with QC annotations preserved

Inspect the generated PNG files directly with `read` to verify distributions and thresholds, and report the exact output file paths in the workspace to the user.

### Workflow Steps

The script performs the following steps:

1. **Calculate QC metrics** - Count depth, gene detection, mitochondrial/ribosomal/hemoglobin content
2. **Apply MAD-based filtering** - Permissive outlier detection using MAD thresholds for counts/genes/MT%
3. **Filter genes** - Remove genes detected in few cells
4. **Generate visualizations** - Comprehensive before/after plots with threshold overlays

## Approach 2: Modular Building Blocks (For Custom Workflows)

For custom analysis workflows or non-standard requirements, write a workspace script with `write` that imports the modular utility functions from `scripts/qc_core.py` and `scripts/qc_plotting.py`, then execute it via `bash`:

```python
import sys
sys.path.insert(0, "cloudra/skills/single-cell-rna-qc/scripts")

import anndata as ad
from qc_core import calculate_qc_metrics, detect_outliers_mad, filter_cells
from qc_plotting import plot_qc_distributions  # Only if visualization needed

adata = ad.read_h5ad('input.h5ad')
calculate_qc_metrics(adata, inplace=True)
# ... custom analysis logic here
```

**When to use this approach:**
- Different workflow needed (skip steps, change order, apply different thresholds to subsets)
- Conditional logic (e.g., filter neurons differently than other cells)
- Partial execution (only metrics/visualization, no filtering)
- Integration with other analysis steps in a larger pipeline
- Custom filtering criteria beyond what command-line params support

**Available utility functions:**

From `qc_core.py` (core QC operations):
- `calculate_qc_metrics(adata, mt_pattern, ribo_pattern, hb_pattern, inplace=True)` - Calculate QC metrics and annotate adata
- `detect_outliers_mad(adata, metric, n_mads, verbose=True)` - MAD-based outlier detection, returns boolean mask
- `apply_hard_threshold(adata, metric, threshold, operator='>', verbose=True)` - Apply hard cutoffs, returns boolean mask
- `filter_cells(adata, mask, inplace=False)` - Apply boolean mask to filter cells
- `filter_genes(adata, min_cells=20, min_counts=None, inplace=True)` - Filter genes by detection
- `print_qc_summary(adata, label='')` - Print summary statistics

From `qc_plotting.py` (visualization):
- `plot_qc_distributions(adata, output_path, title)` - Generate comprehensive QC plots
- `plot_filtering_thresholds(adata, outlier_masks, thresholds, output_path)` - Visualize filtering thresholds
- `plot_qc_after_filtering(adata, output_path)` - Generate post-filtering plots

**Example custom workflows:**

**Example 1: Only calculate metrics and visualize, don't filter yet**
```python
adata = ad.read_h5ad('input.h5ad')
calculate_qc_metrics(adata, inplace=True)
plot_qc_distributions(adata, 'qc_before.png', title='Initial QC')
print_qc_summary(adata, label='Before filtering')
```

**Example 2: Apply only MT% filtering, keep other metrics permissive**
```python
adata = ad.read_h5ad('input.h5ad')
calculate_qc_metrics(adata, inplace=True)

# Only filter high MT% cells
high_mt = apply_hard_threshold(adata, 'pct_counts_mt', 10, operator='>')
adata_filtered = filter_cells(adata, ~high_mt)
adata_filtered.write('filtered.h5ad')
```

**Example 3: Different thresholds for different subsets**
```python
adata = ad.read_h5ad('input.h5ad')
calculate_qc_metrics(adata, inplace=True)

# Apply type-specific QC (assumes cell_type metadata exists)
neurons = adata.obs['cell_type'] == 'neuron'
other_cells = ~neurons

# Neurons tolerate higher MT%, other cells use stricter threshold
neuron_qc = apply_hard_threshold(adata[neurons], 'pct_counts_mt', 15, operator='>')
other_qc = apply_hard_threshold(adata[other_cells], 'pct_counts_mt', 8, operator='>')
```

## Best Practices

1. **Be permissive with filtering** - Default thresholds intentionally retain most cells to avoid losing rare populations
2. **Inspect visualizations** - Always inspect before/after plots with `read` to ensure filtering makes biological sense
3. **Consider dataset-specific factors** - Some tissues naturally have higher mitochondrial content (e.g., neurons, cardiomyocytes)
4. **Check gene annotations** - Mitochondrial gene prefixes vary by species (`mt-` for mouse, `MT-` for human)
5. **Iterate if needed** - QC parameters may need adjustment based on the specific experiment or tissue type

## Reference Materials

For detailed QC methodology, parameter rationale, and troubleshooting guidance, load [references/scverse_qc_guidelines.md](references/scverse_qc_guidelines.md) via `get_skill(skill_name="single-cell-rna-qc", reference="scverse_qc_guidelines.md")`. This reference provides:
- Detailed explanations of each QC metric and why it matters
- Rationale for MAD-based thresholds and why they're better than fixed cutoffs
- Guidelines for interpreting QC visualizations (histograms, violin plots, scatter plots)
- Species-specific considerations for gene annotations
- When and how to adjust filtering parameters
- Advanced QC considerations (ambient RNA correction, doublet detection)

Load this reference when users need deeper understanding of the methodology or when troubleshooting QC issues.

## Next Steps After QC

Typical downstream analysis steps:
- Ambient RNA correction (SoupX, CellBender)
- Doublet detection (scDblFinder)
- Normalization (log-normalize, scran)
- Feature selection and dimensionality reduction
- Deep learning integration, batch correction, and label transfer (load `get_skill(skill_name="scvi-tools")`)
- Clustering and cell type annotation

## Attribution & License

Adapted for Cloudra from Anthropic's `knowledge-work-plugins` (`bio-research/skills/single-cell-rna-qc`, commit `b4c9a4e1de4b42868b74a6fe30ac766f64e43a3e`) under the **Apache License 2.0** (see bundled `LICENSE.txt`). Modifications for Cloudra include native tool mappings (`bash`, `read`, `write`, `edit`, `get_skill`, `ask_user`) and biomedical MCP integration guidance.

## Applicable Scenarios

- Performing standard scverse/scanpy MAD-based quality control and low-quality cell/gene filtering on `.h5ad` or 10X Genomics `.h5` scRNA-seq matrices.
- Auditing count depth, detected genes, and mitochondrial/ribosomal/hemoglobin fractions across samples with pre- and post-filtering visual diagnostics.
- Building tissue- or cell-type-specific filtering scripts (e.g., higher MT% tolerance for neurons or cardiomyocytes) using modular Python utilities (`qc_core.py`, `qc_plotting.py`).
- Preparing clean, raw-count-preserved AnnData objects for downstream doublet removal, normalization, or deep-learning integration (`scvi-tools`).
