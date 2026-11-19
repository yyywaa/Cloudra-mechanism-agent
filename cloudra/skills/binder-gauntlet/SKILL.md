---
name: binder-gauntlet
description: Validation and developability gauntlet for de novo designed protein binders and miniproteins against any protein target. Use this skill when designed binders are scored only by structure-predictor confidence (ipSAE, ipTM, pAE) and you must validate binding with independent re-prediction, pose agreement (DockQ) and controls, profile developability and sequence liabilities, check specificity and cross-reactivity, and write a validation dossier before ranking, filtering, or finalising binder designs, and at every selection round of a design campaign to steer it.
license: Apache-2.0
metadata:
  original-skill: "binder-gauntlet"
  source: "https://github.com/anthropics/life-sciences/tree/0d38fe5c0a50d711ebe6ecd85dc84b98660579d0/binder-gauntlet"
  upstream-commit: "0d38fe5c0a50d711ebe6ecd85dc84b98660579d0"
  adapted-by: "Cloudra"
  upstream-license: "Apache-2.0"
---

# Binder Gauntlet: Validate and Profile Designed Binders Before Ordering DNA

A structure predictor's interface confidence is the field's standard first filter, and it is only that. This skill defines the rest of the computational diligence a protein-engineering or pharma team expects to see next to a table of designed binders: (A) evidence the binding claim survives checks the design loop did not optimise against, with controls; (B) a developability profile of each design; (C) an honest dossier that states what was not checked. It is target-agnostic and tool-agnostic — use whatever structure predictors and structural-biology libraries are installed — while naming common open tools and literature thresholds (see `references/thresholds.md`). Budget compute explicitly: time one complex prediction per predictor and multiply — A1 for 30 designs × 2 predictors × 3 seeds is ≈180 complex predictions plus monomer refolds and controls; A6–A9 on 10 leads roughly doubles that; Part B takes CPU-minutes.

## Before You Start (Cloudra Toolchain Mapping)

- **Bundled sequence-profiling script (`bash`)**: `scripts/sequence_profile.py` (Python standard library only, no network required) turns one or many sequences (a FASTA file, or `--seq`) into Part B's sequence-level table: size, pI and net charge, GRAVY, A280 measurability, cysteines, liability motifs with positions, hydrophobic and charged windows, and candidate protease sites (CSV or `--json`). Run it on the shortlist every round via `bash` instead of re-deriving motif rules. Locate it dynamically from Cloudra's skill directory and verify on first use:
  ```bash
  SEQ_PROF=$(python3 -c "import os, cloudra.base.skill_class as s; print(os.path.join(s.skill_loader.base_path, 'binder-gauntlet', 'scripts', 'sequence_profile.py'))")
  python3 "$SEQ_PROF" --self-test
  ```
  The self-test must end with `self-test passed`.
- **Where to write (`write`, `edit`, `read`)**: Write all round outputs, CSV tables, and Markdown dossiers into a working folder in the user's workspace (e.g., `gauntlet/<target>/round_<n>/`). **Never write into the skill's own folder.**
- **Reference guides (`get_skill`)**: Load bundled references on demand via `get_skill`:
  - `get_skill(skill_name="binder-gauntlet", reference="thresholds.md")` — literature pass marks and provenance
  - `get_skill(skill_name="binder-gauntlet", reference="developability-checks.md")` — how to compute each Part B descriptor with open Python libraries (`biopython`, `freesasa`, `DSSP`)
  - `get_skill(skill_name="binder-gauntlet", reference="dossier-template.md")` — Part C nine-topic dossier and per-design CSV schema
  - `get_skill(skill_name="binder-gauntlet", reference="honest-limits.md")` — exact limits language to include in the dossier
- **Structure inspection, visualization & optional MD (Cloudra native tools)**:
  - Use `pdb_inspect` / `pdb_clean` to check receptor structures for missing segments, heteroatoms, disulfides, and alternate conformations; `format_converter` for geometry conversions; `pymol_render` to visually inspect designed interfaces, clash zones, and termini placement.
  - If running optional short MD red-flag checks (A10), pair with `get_skill(skill_name="molecular-dynamics-simulation")` and Cloudra's `md_box`, `md_trajectory`, `md_rmsd`, and `md_rmsf`.
- **GPU and batch job dispatch (`submit_compute_job`, `query_compute_job`, `query_compute_queue`, `bash`)**:
  - Dispatch heavy Part A GPU structure-prediction runs (complex re-predictions, monomer refolds, co-folds, and controls) asynchronously through `submit_compute_job` (`is_async=True`) or remote SSH/Slurm/Kubernetes batch scripts via `bash`, monitoring with `query_compute_job` / `query_compute_queue`. Keep Part B sequence/surface scripts, structural superpositions, and dossier assembly in the local session via `bash`, `read`, and `write`.
- **Target context, native annotations, known binders & literature grounding (MCP + native retrieval)**:
  - **Target UniProt/PDB records, isoforms, glycosylation sites, paralogs/orthologs (A3, A6, A9)**: Use `mcp__tooluniverse__find_tools` / `mcp__tooluniverse__get_tool_info` / `mcp__tooluniverse__execute_tool` to query UniProt/RCSB/sequence tools, `mcp__opentargets__search_entities` & `mcp__opentargets__query_open_targets_graphql` for target biology and expression/safety context, or `browser` / `bash` when fetching public UniProt/PDB records directly.
  - **Known binders, pharmacological mechanisms & clinical precedent (A3, B8/B9 context)**: Query `mcp__chembl__target_search`, `mcp__chembl__get_bioactivity`, and `mcp__chembl__get_mechanism` for known ligands/targets, and `mcp__c_trials__search_trials__7dc25e7d1366` / `mcp__c_trials__get_trial_details__5b3ae6375c74` for clinical-stage modalities against the target.
  - **Threshold & methodology literature verification**: Query `mcp__pubmed__search_articles` / `mcp__pubmed__get_article_metadata` / `mcp__pubmed__get_full_text_article`, `mcp__biorxiv__search_preprints` / `mcp__biorxiv__get_preprint`, or Cloudra native `search` (`source=openalex`/`arxiv`/`web`) + `browser` + `read`.
  - **Offline fallback**: All core sequence checks (`scripts/sequence_profile.py`) and local structure calculations run completely offline without network or MCP calls. Whenever external target annotations or paralog sequences are unavailable, log them transparently in dossier Topic 9 ("Not checked, and why").

## Principles

1. **Independence.** A check only adds evidence if the design loop did not optimise against it. Prefer predictors, seeds, and physics terms outside your design objective; explicitly state which checks are independent and which are not.
2. **Same pipeline for controls and designs.** Every validation protocol is first run on positive and negative controls; report their numbers beside the designs'. A pipeline that cannot separate a known binder from a scrambled sequence is not evidence.
3. **Not run ≠ passed.** Anything you did not check is listed as not checked, with the reason.
4. **Pass/fail only where the literature gives a threshold; otherwise report values against references.** There is no validated computational developability gauntlet for miniproteins (antibody rules such as TAP do not transfer); show descriptors, compare to reference proteins if available, and do not invent cut-offs.
5. **Reject in the open.** Candidates dropped on this evidence are part of the deliverable, with the reason.

## Run It in the Loop, Not Only at the End

These checks are for steering design, not just for documenting it. At every selection or refinement round, run the cheap checks on the current shortlist and use the results to decide what to keep, drop, mutate, or redesign:
- **Every round (CPU-minutes)**: sequence liabilities (above all labile motifs inside the interface), A280 measurability, pI and charge patches, hydrophobic patch on the free (non-interface) face, low-complexity or poly-residue runs, self-association co-fold, designability/sequence recovery (A8, B1–B4, B7, B8).
- **Every round on current top N**: out-of-objective re-prediction with pose agreement, monomer refold, and the partner-superposition blocker test (A1, A2, A5 — N × predictors × seeds complex predictions; budget compute explicitly).
- **Leads before final pick**: full paralog/ortholog/decoy panel (A6), binding-dead mutants (A7), full-length-target refolds (A9), and optional MD red-flag screen (A10).
- **Controls early**: Run controls (A3) early and again through each protocol the first time you use it, so every later number has a reference. Keep a running "set aside, and why" log from round one (becomes dossier Topic 8).
- **Manage objective leakage (Principle 1)**: A predictor you select on joins your objective. State the A4 consensus rule before the first round, hold at least one predictor or protocol back for the final pass, and record in dossier Topic 1 which checks steered selection and which remained independent.

## Part A — Binding-Validation Gauntlet (Per Design Unless Noted)

- **A1. Out-of-objective re-prediction and pose agreement.** Re-predict each binder–target complex from sequence with at least one predictor not used in design or scoring — two if available — (e.g., AF2-multimer with target template ± initial guess, Boltz, Chai, Protenix/AF3-class, or single-sequence predictors that support complexes), across several seeds each. Record interface confidence (ipTM, interface pAE, ipSAE) and agreement with the designed pose (DockQ, interface RMSD, binder RMSD after target superposition). Literature pass marks: interface pAE < 10 (calibrated for AF2 initial-guess; for other predictors report values beside controls rather than applying 10 as a pass line); DockQ ≥ 0.49 "medium", ≥ 0.23 "acceptable"; binder Cα RMSD to design ≲ 2 Å. A confident prediction in a different pose is a **failure**, not a pass. If only one independent predictor is available, run more seeds and label section 1 "single-predictor"; if none is available, say so and report A2/A3/A5/A9 with the design-time predictor marked not independent.
- **A2. Monomer refold.** Fold the binder alone (no target); require high pLDDT (> 80) and RMSD to the designed monomer ≲ 1–2 Å (≤ 3.5 Å bound-vs-unbound is BindCraft's filter). Flag fold-on-binding designs explicitly.
- **A3. Controls through the identical protocol.** Positives: a natural partner or known binder of the target extracted from a deposited complex if one exists (and an engineered high-affinity variant if public). Negatives: composition-preserving scrambles of several designs; a well-folded unrelated protein of similar size; and a *decoy target* (fold designs against an unrelated protein of the same fold class as the target). Report score distributions and where each design falls; a design scoring with the negatives fails this check.
- **A4. Consensus rule.** State a rule before looking (e.g., "every independent predictor run — at least one held back from selection — reproduces the designed pose at DockQ ≥ 0.49 and its interface confidence falls in the positive-control range") and apply it uniformly; note that once used for selection it is no longer independent.
- **A5. Function/epitope test by superposition.** Superpose the natural partner's complex onto each predicted design complex; report steric clash with the partner and fraction of the partner's footprint covered → `predicted blocker: yes/no`. Footprint overlap alone is weaker than steric clash.
- **A6. Specificity and cross-reactivity panel** (when sequences are available or retrieved via MCP/UniProt): co-fold each design against the target's closest human paralogs, same-family domains, and 1–2 unrelated same-fold decoys (want low confidence), and against mouse/cynomolgus orthologs (cross-reactivity is usually wanted for animal models — report it explicitly as such). State clearly that co-folding confidence discriminates on- from off-target only roughly.
- **A7. Binding-dead control mutants.** For top designs, propose 2–3-residue hotspot knockouts or charge reversals at the designed interface and re-predict; expect confidence/pose to collapse. Single-Ala changes rarely move co-folding scores — do not present this as a ΔΔG scan (that requires Rosetta/FoldX). Output: a named binding-dead control mutant per lead for wet-lab validation.
- **A8. Self-association.** Co-fold two copies of each binder; a confident homodimer, especially one burying the binding face, is a flag (designed binders have turned out dimeric by SEC-MALS).
- **A9. Native-context checks.** From the target's UniProt entry (staged locally or retrieved via `mcp__tooluniverse__execute_tool` / `browser`): check N-glycosylation sequons and annotated glycosites, disulfides, natural variants, and isoform boundaries near the footprint — a design made against a bare, truncated crystal construct can target a surface that is glycan-covered or absent on the cell. Re-predict leads against the full extracellular region (or full domain architecture), not just the truncated construct, and verify approach direction relative to the membrane or neighbouring domains.
- **A10. Pose persistence.** Across seeds, predictors, and (optionally) short MD (`md_box`/`md_trajectory`/`md_rmsd`/`md_rmsf`), report interface-contact persistence and pose RMSD spread; treat MD as a red-flag screen only — there is no published evidence that MD improves wet-lab hit rates beyond A1-type filters.
- **A11. Physics-lite interface metrics** (label uncalibrated if no Rosetta/FoldX): buried SASA, shape complementarity, interface H-bonds/salt bridges, buried unsatisfied polar atoms, and interface hydrophobic fraction.

## Part B — Developability Profile (CPU; Per Design)

Load `references/developability-checks.md` via `get_skill(skill_name="binder-gauntlet", reference="developability-checks.md")` for motif lists and open-tool recipes (`scripts/sequence_profile.py`, `biopython`, `freesasa`, `DSSP`).

- **B1. Chemical liabilities** with solvent exposure and interface membership: deamidation (`NG` ≫ `NS` > `NT`/`NN`/`NH`), Asp isomerisation (`DG`, `DS`), acid-labile `DP`, exposed `Met`/`Trp` (oxidation), `N-X-[S/T]` (`X ≠ P`) sequons, free/odd `Cys`, N-terminal `Gln`/`Glu`.
- **B2. Charge**: pI, net charge at pH 7.4, largest positive and negative surface patches; interface `His` count (pH sensitivity).
- **B3. Hydrophobic surface**: largest hydrophobic patch and SAP-like score, reported separately for the binding face and the free (non-interface) surface (the interface may be hydrophobic; the free surface should not be).
- **B4. Aggregation-prone stretches**: sliding-window hydrophobicity/β-propensity heuristic (or Aggrescan3D/CamSol/TANGO/NetSolP if installed and licensed where required) plus low-complexity/poly-ion runs.
- **B5. Protease exposure**: canonical trypsin/chymotrypsin/Asp-N/Glu-C sites sitting in DSSP loops with high relative SASA (> 30 %).
- **B6. Stability proxies**: monomer pLDDT, design-vs-refold RMSD, inverse-folding/LM log-likelihood, helix capping and buried polar sanity; note de novo miniproteins are typically hyperstable (Tm > 70–90 °C), so treat this as a sanity check rather than a ranking metric.
- **B7. Designability**: sequence recovery of the designed backbone by an inverse-folding model (e.g., ProteinMPNN/SolubleMPNN) and fraction of alternative sequences that refold to the backbone.
- **B8. Format and manufacturability**: which terminus is solvent-exposed and ≥ 15–20 Å from the interface (tag / Fc / albumin-binder attachment); implied expression host (Cys-free, no glycosylation → *E. coli*); A280 measurability (`Trp`/`Tyr` present?); gene-synthesis complexity of a codon-optimised CDS (GC %, repeats, homopolymers); intended therapeutic/imaging format and PK implication — an unmodified protein < 30–50 kDa is renally filtered (half-life of minutes–hours); half-life comes from format (Fc, albumin binding, PEG/polypeptide fusion), not sequence. Do not claim a sequence-derived PK beyond this.
- **B9. Immunogenicity**: if an HLA-II epitope predictor (NetMHCIIpan, IEDB, MixMHC2pred) is installed and licensed where required, report predicted epitope density vs reference proteins; otherwise list under "not checked". "Humanness" is undefined for de novo sequences; aggregation and epitope content are the computable levers, and decisive evaluation is in vitro.
- **B10. What must go to the lab regardless**: expression/solubility/SEC, affinity and kinetics, specificity panel, Tm, protease/serum stability, experimental complex structure, in-vitro immunogenicity, and PK.

## Part C — Reporting

Use `write` to generate a Markdown validation dossier in the working folder covering all nine topics (`get_skill(skill_name="binder-gauntlet", reference="dossier-template.md")`):
1. Binding evidence beyond the objective + controls + consensus call
2. Function / predicted blocker status
3. Specificity and species cross-reactivity
4. Robustness (pose persistence, self-association, monomer refold, binding-dead mutants for leads)
5. Native context (glycosylation, disulfides, variants, full-length target refold, membrane geometry)
6. Developability per design
7. Interface metrics (uncalibrated unless Rosetta/FoldX used)
8. Candidates set aside and why
9. Not checked, and why

Also write one per-design CSV keyed by the binder sequence (first column) plus control rows tagged with a `role` column (`design` / `positive_control` / `scramble` / `decoy`). Include the limits statements from `references/honest-limits.md` verbatim or closely paraphrased: co-folding models share training data (correlated evidence); controls show the pipeline is not trivially fooled, not that designs bind; confidence filters raise lab hit rates but do not predict affinity; developability descriptors are shown against references, not as pass/fail.

## Order of Work When Time Is Short

Controls first (A3), and through each new protocol as it is introduced → every design round: B1–B4, B7, B8, and A8 on the shortlist (minutes) plus A1/A2/A5 on the current top N, dropping or redesigning on the results → before final pick: complete A1/A2 on everything still kept (including the held-out predictor) and apply the A4 rule, then A9 and A6/A7 on leads → remaining items (A10, A11, B5, B6, B9) → write up dossier and CSV, always leaving time for Topic 9. If invoked only at the end of a campaign, run in this order on the final set and state explicitly in the dossier that validation was applied post hoc.

---

*Attribution & Modification Notice: Adapted from `binder-gauntlet` in [anthropics/life-sciences](https://github.com/anthropics/life-sciences/tree/0d38fe5c0a50d711ebe6ecd85dc84b98660579d0/binder-gauntlet) (Apache-2.0; full license retained in `LICENSE.txt`). Modified by Cloudra to map script execution, reference loading, batch compute dispatch, structure inspection, and external database queries to Cloudra native tools and MCP servers.*

## Applicable Scenarios (适用场景)

- 从头设计蛋白结合剂或迷你蛋白（如 RFdiffusion / ProteinMPNN / BindCraft 产出）后的独立复测、构象一致性（DockQ）与正负对照验收。
- 多轮蛋白设计迭代中，每轮快速筛查序列化学修饰风险、表面电荷/疏水斑块、自聚倾向与表达可制造性以指导突变和淘汰。
- 候选分子送湿实验合成 DNA 前，需要排查靶点原生糖基化/异构体遮蔽、人源同源蛋白脱靶与鼠/食蟹猴交叉反应并设计失活对照突变体。
- 为蛋白工程或药物发现项目生成可审计的 9 模块验证档案（Validation Dossier）及按序列主键对齐的 CSV 汇总表，明确区分已验证项与未检项。
