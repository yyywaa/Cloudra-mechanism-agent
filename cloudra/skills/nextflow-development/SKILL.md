---
name: nextflow-development
description: Run nf-core bioinformatics pipelines (rnaseq, sarek, atacseq) on sequencing data. Use when analyzing RNA-seq, WGS/WES, or ATAC-seq data—either local FASTQs or public datasets from GEO/SRA. Triggers on nf-core, Nextflow, FASTQ analysis, variant calling, gene expression, differential expression, GEO reanalysis, GSE/GSM/SRR accessions, or samplesheet creation.
license: Apache-2.0
metadata:
  source: "https://github.com/anthropics/knowledge-work-plugins/tree/b4c9a4e1de4b42868b74a6fe30ac766f64e43a3e/bio-research/skills/nextflow-development"
  upstream-commit: "b4c9a4e1de4b42868b74a6fe30ac766f64e43a3e"
  upstream-license: "Apache-2.0"
  adapted-by: "Cloudra"
---

# nf-core Pipeline Deployment

Run nf-core bioinformatics pipelines on local or public sequencing data.

**Target users:** Bench scientists and researchers without specialized bioinformatics training who need to run large-scale omics analyses—differential expression, variant calling, or chromatin accessibility analysis.

## Cloudra Tooling & Biomedical Knowledge Integration

Anchor Nextflow / nf-core execution, decision checkpoints, and study verification in Cloudra's native tools and biomedical MCP servers:

- **Helper scripts & quick checks (`bash`)**: Invoke scripts under `cloudra/skills/nextflow-development/scripts/` (`sra_geo_fetch.py`, `check_environment.py`, `detect_data_type.py`, `generate_samplesheet.py`, `manage_genomes.py`). Because Cloudra's `bash` tool runs non-interactively, inspect groups first (`sra_geo_fetch.py groups`) and pass `--subset "<GROUP>"` instead of `-i`, and pass `--no-interactive` to `generate_samplesheet.py`.
- **Long-running pipeline execution (`submit_compute_job` / `query_compute_job`)**: Full `nextflow run nf-core/<pipeline>` runs, test profiles, and large FASTQ downloads should be written into a shell script via `write` and launched asynchronously with `submit_compute_job(job_type="shell", is_async=True)`, then tracked with `query_compute_job`.
- **Decision points (`ask_user`)**: Confirm every workflow `DECISION POINT` (GEO sample subset, pipeline choice, reference genome, aligner/caller/read-length options, and tumor/normal pairing) with the user via `ask_user`.
- **File creation & inspection (`write` / `edit` / `read`)**: Use `write`/`edit` for `samplesheet.csv`, `design.csv`, custom `nextflow.config`, and run scripts; use `read` to inspect `.nextflow.log`, `samplesheet.csv`, `study_info.json`, gene count/TPM tables, and MultiQC summaries.
- **Reference guides (`get_skill`)**: Load bundled guides via `get_skill(skill_name="nextflow-development", reference="<path>")` (e.g., `geo-sra-acquisition.md`, `installation.md`, `troubleshooting.md`, `pipelines/rnaseq.md`, `pipelines/sarek.md`, `pipelines/atacseq.md`).
- **Online docs (`browser` / `search`)**: Check nf-core release notes, parameter documentation (`https://nf-co.re/`), or GEO/SRA web records when needed.
- **Study provenance & downstream biological annotation (P0 MCP)**:
  - Use `mcp__pubmed__search_articles`, `mcp__pubmed__get_article_metadata`, `mcp__pubmed__get_full_text_article`, and `mcp__biorxiv__search_preprints` to look up the original publication for a GEO/SRA study (`GSE*` / BioProject) and verify experimental design, strandedness, and clinical metadata.
  - Use `mcp__opentargets__search_entities` / `mcp__opentargets__query_open_targets_graphql` and `mcp__tooluniverse__find_tools` / `mcp__tooluniverse__execute_tool` to annotate differentially expressed genes (`rnaseq`), somatic/germline variants (`sarek`), or differential accessibility peaks (`atacseq`) against target-disease and functional genomics databases.

## Workflow Checklist

```
- [ ] Step 0: Acquire data (if from GEO/SRA)
- [ ] Step 1: Environment check (MUST pass)
- [ ] Step 2: Select pipeline (confirm with user via ask_user)
- [ ] Step 3: Run test profile (MUST pass)
- [ ] Step 4: Create samplesheet
- [ ] Step 5: Configure & run (confirm genome with user via ask_user)
- [ ] Step 6: Verify outputs
```

---

## Step 0: Acquire Data (GEO/SRA Only)

**Skip this step if user has local FASTQ files.**

For public datasets, fetch from GEO/SRA first. Load [references/geo-sra-acquisition.md](references/geo-sra-acquisition.md) via `get_skill(skill_name="nextflow-development", reference="geo-sra-acquisition.md")` for the full workflow.

**Quick start (via `bash`; non-interactive safe):**

```bash
SCRIPTS="cloudra/skills/nextflow-development/scripts"

# 1. Get study info and sample groups
python "$SCRIPTS/sra_geo_fetch.py" info GSE110004
python "$SCRIPTS/sra_geo_fetch.py" groups GSE110004

# 2. After confirming subset with ask_user, download non-interactively
python "$SCRIPTS/sra_geo_fetch.py" download GSE110004 -o ./fastq --subset "RNA-Seq:PAIRED"

# 3. Generate samplesheet
python "$SCRIPTS/sra_geo_fetch.py" samplesheet GSE110004 --fastq-dir ./fastq -o samplesheet.csv
```

**DECISION POINT:** After fetching study info (and optionally checking the study paper with `mcp__pubmed__search_articles`), confirm with the user via `ask_user`:
- Which sample subset to download (if multiple data types)
- Suggested genome and pipeline

Then continue to Step 1.

---

## Step 1: Environment Check

**Run first via `bash`. Pipeline will fail without passing environment.**

```bash
python cloudra/skills/nextflow-development/scripts/check_environment.py
```

All critical checks must pass. If any fail, provide fix instructions:

### Docker issues

| Problem | Fix |
|---------|-----|
| Not installed | Install from https://docs.docker.com/get-docker/ |
| Permission denied | `sudo usermod -aG docker $USER` then re-login |
| Daemon not running | `sudo systemctl start docker` |

### Nextflow issues

| Problem | Fix |
|---------|-----|
| Not installed | `curl -s https://get.nextflow.io \| bash && mv nextflow ~/bin/` |
| Version < 23.04 | `nextflow self-update` |

### Java issues

| Problem | Fix |
|---------|-----|
| Not installed / < 11 | `sudo apt install openjdk-11-jdk` |

**Do not proceed until all checks pass.** For HPC/Singularity, load [references/troubleshooting.md](references/troubleshooting.md) via `get_skill(skill_name="nextflow-development", reference="troubleshooting.md")`.

---

## Step 2: Select Pipeline

**DECISION POINT: Confirm with user via `ask_user` before proceeding.**

| Data Type | Pipeline | Version | Goal |
|-----------|----------|---------|------|
| RNA-seq | `rnaseq` | 3.22.2 | Gene expression |
| WGS/WES | `sarek` | 3.7.1 | Variant calling |
| ATAC-seq | `atacseq` | 2.1.2 | Chromatin accessibility |

Auto-detect from data:
```bash
python cloudra/skills/nextflow-development/scripts/detect_data_type.py /path/to/data
```

For pipeline-specific details (load via `get_skill(skill_name="nextflow-development", reference="pipelines/<name>.md")`):
- [references/pipelines/rnaseq.md](references/pipelines/rnaseq.md)
- [references/pipelines/sarek.md](references/pipelines/sarek.md)
- [references/pipelines/atacseq.md](references/pipelines/atacseq.md)

---

## Step 3: Run Test Profile

**Validates environment with small data. MUST pass before real data.**

```bash
nextflow run nf-core/<pipeline> -r <version> -profile test,docker --outdir test_output
```

| Pipeline | Command |
|----------|---------|
| rnaseq | `nextflow run nf-core/rnaseq -r 3.22.2 -profile test,docker --outdir test_rnaseq` |
| sarek | `nextflow run nf-core/sarek -r 3.7.1 -profile test,docker --outdir test_sarek` |
| atacseq | `nextflow run nf-core/atacseq -r 2.1.2 -profile test,docker --outdir test_atacseq` |

Verify via `bash` and inspect logs with `read`:
```bash
ls test_output/multiqc/multiqc_report.html
grep "Pipeline completed successfully" .nextflow.log
```

If the test fails, load [references/troubleshooting.md](references/troubleshooting.md).

---

## Step 4: Create Samplesheet

### Generate automatically

```bash
python cloudra/skills/nextflow-development/scripts/generate_samplesheet.py /path/to/data <pipeline> -o samplesheet.csv --no-interactive
```

The script:
- Discovers FASTQ/BAM/CRAM files
- Pairs R1/R2 reads
- Infers sample metadata
- Validates before writing

**For sarek:** With `--no-interactive`, unrecognized samples default to normal (`0`). Inspect `samplesheet.csv` with `read`, confirm tumor (`1`) / normal (`0`) status with the user via `ask_user`, and update the `status` column with `edit`.

### Validate existing samplesheet

```bash
python cloudra/skills/nextflow-development/scripts/generate_samplesheet.py --validate samplesheet.csv <pipeline>
```

### Samplesheet formats

**rnaseq:**
```csv
sample,fastq_1,fastq_2,strandedness
SAMPLE1,/abs/path/R1.fq.gz,/abs/path/R2.fq.gz,auto
```

**sarek:**
```csv
patient,sample,lane,fastq_1,fastq_2,status
patient1,tumor,L001,/abs/path/tumor_R1.fq.gz,/abs/path/tumor_R2.fq.gz,1
patient1,normal,L001,/abs/path/normal_R1.fq.gz,/abs/path/normal_R2.fq.gz,0
```

**atacseq:**
```csv
sample,fastq_1,fastq_2,replicate
CONTROL,/abs/path/ctrl_R1.fq.gz,/abs/path/ctrl_R2.fq.gz,1
```

---

## Step 5: Configure & Run

### 5a. Check genome availability

```bash
python cloudra/skills/nextflow-development/scripts/manage_genomes.py check <genome>
# If not installed:
python cloudra/skills/nextflow-development/scripts/manage_genomes.py download <genome>
```

Common genomes: `GRCh38` (human), `GRCh37` (legacy), `GRCm39` (mouse), `R64-1-1` (yeast), `BDGP6` (fly)

### 5b. Decision points

**DECISION POINT: Confirm with user via `ask_user`:**

1. **Genome:** Which reference to use
2. **Pipeline-specific options:**
   - **rnaseq:** aligner (`star_salmon` recommended, `hisat2` for low memory)
   - **sarek:** tools (`haplotypecaller` for germline, `mutect2` for somatic)
   - **atacseq:** `read_length` (`50`, `75`, `100`, or `150`)

### 5c. Run pipeline

For production runs, save the command in a wrapper script via `write` and launch via `submit_compute_job(job_type="shell", is_async=True)` (or run directly via `bash` for small datasets):

```bash
nextflow run nf-core/<pipeline> \
    -r <version> \
    -profile docker \
    --input samplesheet.csv \
    --outdir results \
    --genome <genome> \
    -resume
```

**Key flags:**
- `-r`: Pin version
- `-profile docker`: Use Docker (or `singularity` for HPC)
- `--genome`: iGenomes key
- `-resume`: Continue from checkpoint

**Resource limits (if needed):**
```bash
--max_cpus 8 --max_memory '32.GB' --max_time '24.h'
```

---

## Step 6: Verify Outputs

### Check completion

```bash
ls results/multiqc/multiqc_report.html
grep "Pipeline completed successfully" .nextflow.log
```

Inspect `.nextflow.log` and key result summaries with `read`.

### Key outputs by pipeline

**rnaseq:**
- `results/star_salmon/salmon.merged.gene_counts.tsv` - Gene counts
- `results/star_salmon/salmon.merged.gene_tpm.tsv` - TPM values

**sarek:**
- `results/variant_calling/*/` - VCF files
- `results/preprocessing/recalibrated/` - BAM files

**atacseq:**
- `results/macs2/narrowPeak/` - Peak calls
- `results/bwa/mergedLibrary/bigwig/` - Coverage tracks

---

## Quick Reference

For common exit codes and fixes, load [references/troubleshooting.md](references/troubleshooting.md).

### Resume failed run

```bash
nextflow run nf-core/<pipeline> -resume
```

---

## References

Load any bundled reference via `get_skill(skill_name="nextflow-development", reference="<path>")`:

- [references/geo-sra-acquisition.md](references/geo-sra-acquisition.md) - Downloading public GEO/SRA data
- [references/troubleshooting.md](references/troubleshooting.md) - Common issues and fixes
- [references/installation.md](references/installation.md) - Environment setup
- [references/pipelines/rnaseq.md](references/pipelines/rnaseq.md) - RNA-seq pipeline details
- [references/pipelines/sarek.md](references/pipelines/sarek.md) - Variant calling details
- [references/pipelines/atacseq.md](references/pipelines/atacseq.md) - ATAC-seq details

---

## Disclaimer

This skill integrates three core nf-core bioinformatics pipelines (`rnaseq`, `sarek`, and `atacseq`) into Cloudra automated analysis workflows for research and educational use. Users are responsible for verifying that their compute environment meets pipeline requirements and for independently validating all computational bioinformatics outputs before drawing scientific or clinical conclusions. This skill is not officially endorsed by or affiliated with the nf-core community.

## Attribution & Licenses

Adapted for Cloudra from Anthropic's `knowledge-work-plugins` (`bio-research/skills/nextflow-development`, commit `b4c9a4e1de4b42868b74a6fe30ac766f64e43a3e`) under the **Apache License 2.0** (see bundled `LICENSE.txt`). Modifications for Cloudra include native tool/scheduler mappings (`bash`, `submit_compute_job`, `read`, `write`, `edit`, `ask_user`, `get_skill`), non-interactive CLI guidance, and biomedical MCP integration.

When publishing results, cite the appropriate pipeline. Citations are available in each nf-core repository's `CITATIONS.md` file (e.g., https://github.com/nf-core/rnaseq/blob/3.22.2/CITATIONS.md).

- **Skill source:** Apache License, Version 2.0 (`LICENSE.txt`)
- **nf-core pipelines:** MIT License (https://nf-co.re/about)
- **Nextflow:** Apache License, Version 2.0 (https://www.nextflow.io/about-us.html)
- **NCBI SRA Toolkit:** Public Domain (https://github.com/ncbi/sra-tools/blob/master/LICENSE)

## Applicable Scenarios

- Reanalyzing published NCBI GEO/SRA sequencing datasets (`GSE`/`GSM`/`SRR` accessions) from raw FASTQ acquisition through validated samplesheet creation and pipeline execution.
- Deploying reproducible containerized `nf-core/rnaseq`, `nf-core/sarek` (germline/somatic WGS/WES), or `nf-core/atacseq` workflows on local FASTQ/BAM/CRAM files using Docker or HPC Singularity profiles.
- Performing pre-flight environment checks (Nextflow, Java, container runtime), mandatory test-profile validation, iGenomes reference management, and `-resume` checkpoint recovery.
- Verifying study design from linked PubMed/bioRxiv publications and connecting pipeline outputs (counts, variants, peaks) to downstream biological interpretation via Open Targets and ToolUniverse MCP tools.
