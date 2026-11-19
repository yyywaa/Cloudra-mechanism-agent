---
name: scientific-problem-selection
description: Structured conversational framework for scientific research problem selection, project ideation, troubleshooting stuck projects, and strategic decision-tree navigation based on Fischbach & Walsh (Cell, 2024). Use when scientists want to pitch a new research idea, assess project assumptions and risks, choose an optimization function, calibrate fixed vs. floating parameters, troubleshoot a stalled project, invert an obstacle, or synthesize an evidence-backed research plan.
license: Apache-2.0
metadata:
  original-skill: "scientific-problem-selection"
  source: "https://github.com/anthropics/life-sciences/tree/0d38fe5c0a50d711ebe6ecd85dc84b98660579d0/scientific-problem-selection"
  upstream-commit: "0d38fe5c0a50d711ebe6ecd85dc84b98660579d0"
  adapted-by: "Cloudra"
  upstream-license: "Apache-2.0"
---

# Scientific Problem Selection Skills

A conversational framework for systematic scientific problem selection based on Fischbach & Walsh's "Problem choice and decision trees in science and engineering" (*Cell*, 2024).

## Cloudra Toolchain & Evidence Integration

Combine structured Socratic dialogue with Cloudra's native tools and biomedical MCP servers so every novelty, feasibility, and impact judgment is grounded in real evidence:

- **Load detailed skill modules (`get_skill`)**: Pull individual playbooks on demand with `get_skill(skill_name="scientific-problem-selection", reference="<filename>")` (see the 9 reference files below). Pair with `get_skill(skill_name="literature-search")` for full retrieval chains or `get_skill(skill_name="peer-review-standards")` for adversarial critique of assumptions.
- **Structured dialogue & deliverables (`ask_user`, `write`, `edit`, `read`)**: Use concise conversational prompts (or `ask_user` for structured choices) to gather constraints, and save tangible 1–2 page Markdown deliverables (Problem Ideation Document, Risk Matrix, Impact Assessment, Parameter Strategy, Decision Tree Map, Adversity Playbook, Problem Inversion Analysis, Integrated Project Plan) into the user's workspace with `write` / `edit`.
- **Literature & preprint grounding (Skills 1, 2, 3, 4, 6, 8)**:
  - Peer-reviewed biomedical literature: `mcp__pubmed__search_articles`, `mcp__pubmed__get_article_metadata`, `mcp__pubmed__find_related_articles`, `mcp__pubmed__lookup_article_by_citation`, and `mcp__pubmed__get_full_text_article`.
  - Frontier preprints and competition/scoop checks: `mcp__biorxiv__search_preprints`, `mcp__biorxiv__get_preprint`, and `mcp__biorxiv__search_published_preprints`.
  - Cross-disciplinary literature, citation metrics, and OA PDFs: Cloudra native `search` (`source=openalex` / `arxiv` / `web`), `browser`, and `read`.
- **Target, pharmacology & clinical-precedent calibration (biomedical/translational scoping in Skills 1–3)**:
  - Target genetics & disease associations: `mcp__opentargets__search_entities`, `mcp__opentargets__query_open_targets_graphql`, and `mcp__opentargets__get_open_targets_graphql_schema`.
  - Known chemical probes, bioactivity & mechanisms: `mcp__chembl__target_search`, `mcp__chembl__compound_search`, `mcp__chembl__get_bioactivity`, `mcp__chembl__get_mechanism`, and `mcp__chembl__drug_search`.
  - Clinical trials & endpoint precedents: `mcp__c_trials__search_trials`, `mcp__c_trials__get_trial_details`, and `mcp__c_trials__analyze_endpoints`.
  - Broad specialized scientific databases: `mcp__tooluniverse__find_tools`, `mcp__tooluniverse__get_tool_info`, and `mcp__tooluniverse__execute_tool`.

---

## Getting Started

Present users with three entry points:

**1) Pitch an idea for a new project** — to work it up together

**2) Share a problem in a current project** — to troubleshoot together

**3) Ask a strategic question** — to navigate the decision tree together

This conversational entry meets scientists where they are and establishes a collaborative tone.

---

## Option 1: Pitch an Idea

### Initial Prompt
Ask: **"Tell me the short version of your idea (1-2 sentences)."**

### Response Approach
After the user shares their idea, return a quick summary (no more than one paragraph) demonstrating understanding. Note the general area of research and rephrase the idea in a way that highlights its kernel—showing alignment and readiness to dive into details.

### Follow-up Prompt
Then ask for more detail: "Now give me a bit more detail. You might include, however briefly or even say where you are unsure:
1. What exactly you want to do
2. How you currently plan to do it
3. If it works, why will it be a big deal
4. What you think are the major risks"

### Workflow
From there, guide the user through the early stages of problem selection and evaluation:
- **Skill 1: Intuition Pumps** — Refine and strengthen the idea
- **Skill 2: Risk Assessment** — Identify and manage project risks
- **Skill 3: Optimization Function** — Define success metrics
- **Skill 4: Parameter Strategy** — Determine what to fix vs. keep flexible

Load `01-intuition-pumps.md`, `02-risk-assessment.md`, `03-optimization-function.md`, and `04-parameter-strategy.md` via `get_skill(skill_name="scientific-problem-selection", reference="...")` for detailed guidance.

---

## Option 2: Troubleshoot a Problem

### Initial Prompt
Ask: **"Tell me a short version of your problem (1-2 sentences or whatever is easy)."**

### Response Approach
After the user shares their problem, return a quick summary (no more than one paragraph) demonstrating understanding. Note the context of the project where the problem occurred and rephrase the problem—highlighting its core essence—so the user knows the situation is understood. Also raise additional questions that seem important to discuss.

### Follow-up Prompt
Then ask: "Now give me a bit more detail. You might include, however briefly:
1. The overall goal of your project (if we have not talked about it before)
2. What exactly went wrong
3. Your current ideas for fixing it"

### Workflow
From there, guide the user through troubleshooting and decision tree navigation:
- **Skill 5: Decision Tree Navigation** — Plan decision points and navigate between execution and strategic thinking
- **Skill 4: Parameter Strategy** — Fix one parameter at a time, let others float
- **Skill 6: Adversity Response** — Frame problems as opportunities for growth
- **Skill 7: Problem Inversion** — Strategies for navigating around obstacles

Always include workarounds that might be useful whether or not the problem can be fixed easily.

Load `05-decision-tree.md`, `06-adversity-planning.md`, `07-problem-inversion.md`, and `04-parameter-strategy.md` via `get_skill(skill_name="scientific-problem-selection", reference="...")` for detailed guidance.

---

## Option 3: Ask a Strategic Question

### Initial Prompt
Ask: **"Tell me the short version of your question (1-2 sentences)."**

### Response Approach
After the user shares their question, return a quick summary (no more than one paragraph) demonstrating understanding. Note the broader context and rephrase the question—highlighting its crux—to confirm alignment with their thinking.

### Follow-up Prompt
Then ask: "Now give me a bit more detail. You might include, however briefly:
1. The setting (i.e., is this about a current or future project)
2. A bit more detail about what you're thinking"

### Workflow
From there, draw on the specific modules from the problem choice framework most appropriate to the question:
- **Skills 1-4** for future project planning (ideation, risk, optimization, parameters)
- **Skills 5-7** for current project navigation (decision trees, adversity, inversion)
- **Skill 8** for communication and synthesis
- **Skill 9** for comprehensive workflow orchestration

Load any needed module from `references/` via `get_skill`.

---

## Core Framework Concepts

### The Central Insight
**Problem Choice >> Execution Quality**

Even brilliant execution of a mediocre problem yields incremental impact. Good execution of an important problem yields substantial impact.

### The Time Paradox
Scientists typically spend:
- **Days** choosing a problem
- **Years** solving it

This imbalance limits impact. These skills help invest more time choosing wisely.

### Evaluation Axes
**For Evaluating Ideas:**
- **X-axis:** Likelihood of success
- **Y-axis:** Impact if successful

Skills help move ideas rightward (more feasible) and upward (more impactful).

### The Risk Paradox
- Don't avoid risk—befriend it
- No risk = incremental work
- But: Multiple miracles = avoid or refine
- **Balance:** Understood, quantified, manageable risk

### The Parameter Paradox
- Too many fixed = brittleness
- Too few fixed = paralysis
- **Sweet spot:** Fix ONE meaningful constraint

### The Adversity Principle
- Crises are inevitable (don't be surprised)
- Crises are opportune (don't waste them)
- **Strategy:** Fix problem AND upgrade project simultaneously

---

## The 9 Skills Overview

| Skill | Purpose | Output | Time |
|-------|---------|--------|------|
| 1. Intuition Pumps | Generate high-quality research ideas | Problem Ideation Document | ~1 week |
| 2. Risk Assessment | Identify and manage project risks | Risk Assessment Matrix | 3-5 days |
| 3. Optimization Function | Define success metrics | Impact Assessment Document | 2-3 days |
| 4. Parameter Strategy | Decide what to fix vs. keep flexible | Parameter Strategy Document | 2-3 days |
| 5. Decision Tree Navigation | Plan decision points and altitude dance | Decision Tree Map | 2 days |
| 6. Adversity Response | Prepare for crises as opportunities | Adversity Playbook | 2 days |
| 7. Problem Inversion | Navigate around obstacles | Problem Inversion Analysis | 1 day |
| 8. Integration & Synthesis | Synthesize into coherent plan | Project Communication Package | 3-5 days |
| 9. Meta-Framework | Orchestrate complete workflow | Complete Project Package | 1-6 weeks |

---

## Skill Workflow

```
SKILL 1: Intuition Pumps
         | (generates idea)
         v
SKILL 2: Risk Assessment
         | (evaluates feasibility)
         v
SKILL 3: Optimization Function
         | (defines success metrics)
         v
SKILL 4: Parameter Strategy
         | (determines flexibility)
         v
SKILL 5: Decision Tree
         | (plans execution and evaluation)
         v
SKILL 6: Adversity Planning
         | (prepares for failure modes)
         v
SKILL 7: Problem Inversion
         | (provides pivot strategies)
         v
SKILL 8: Integration & Communication
         | (synthesizes into coherent plan)
         v
SKILL 9: Meta-Skill
         (orchestrates complete workflow)
```

---

## Key Design Principles

1. **Conversational Entry** — Meet users where they are with three clear starting points
2. **Thoughtful Interaction** — Ask clarifying questions; low confidence prompts additional input
3. **Evidence Integration** — Use PubMed, bioRxiv, Open Targets, ChEMBL, ClinicalTrials, and OpenAlex searches at strategic points for validation
4. **Concrete Outputs** — Every skill produces tangible 1-2 page documents saved via `write`
5. **Building Specificity** — Progressive detail emerges through targeted questions
6. **Flexibility** — Skills work independently, sequentially, or iteratively
7. **Scientific Rigor** — Claims about generality and feasibility should be evidence-based

---

## Who Should Use These Skills

### Graduate Students (Primary Audience)
- **When:** Choosing thesis projects, qualifying exams, committee meetings
- **Focus:** Skills 1-3 (ideation, risk, impact) + Skill 9 (complete workflow)
- **Timeline:** 2-4 weeks for comprehensive planning

### Postdocs
- **When:** Starting new position, planning independent projects, fellowship applications
- **Focus:** All skills, emphasizing independence and risk management
- **Timeline:** 1-2 weeks intensive planning

### Principal Investigators
- **When:** New lab, new direction, mentoring trainees, grant cycles
- **Focus:** Skills 1, 3, 4, 6 (ideation, impact, parameters, adversity)
- **Timeline:** Ongoing, integrate into lab culture

### Startup Founders
- **When:** Company inception, pivot decisions, investor pitches
- **Focus:** Skills 1-4 (ideation through parameters) + Skill 8 (communication)
- **Timeline:** 1-2 weeks for initial planning, revisit quarterly

---

## Reference Materials

Detailed skill documentation is available in `references/` and loadable via `get_skill(skill_name="scientific-problem-selection", reference="<file>")`:

| File | Content | Search Patterns |
|------|---------|-----------------|
| `01-intuition-pumps.md` | Generate research ideas | `Intuition Pump #`, `Trap #`, `Phase [0-9]` |
| `02-risk-assessment.md` | Risk identification | `Risk.*1-5`, `go/no-go`, `assumption` |
| `03-optimization-function.md` | Success metrics | `Generality.*Learning`, `optimization`, `impact` |
| `04-parameter-strategy.md` | Parameter fixation | `fixed.*float`, `constraint`, `parameter` |
| `05-decision-tree.md` | Decision tree navigation | `altitude`, `Level [0-9]`, `decision` |
| `06-adversity-planning.md` | Adversity response | `adversity`, `crisis`, `ensemble` |
| `07-problem-inversion.md` | Problem inversion strategies | `Strategy [0-9]`, `inversion`, `goal` |
| `08-integration-synthesis.md` | Integration and synthesis | `narrative`, `communication`, `story` |
| `09-meta-framework.md` | Complete workflow | `Phase`, `workflow`, `orchestrat` |

---

## Expected Outcomes

### Immediate (After Completing Workflow)
- Clear project vision
- Honest risk assessment
- Contingency plans
- Communication materials ready
- Confidence in problem choice

### 6-Month
- Faster decisions (have framework)
- Productive adversity handling
- No existential crises (risks mitigated)

### 2-Year
- Published results or strong progress
- Avoided dead-end projects
- Career aligned with goals
- **Time well-spent** (ultimate measure)

---

## Foundational Reference

**Fischbach, M.A., & Walsh, C.T. (2024).** "Problem choice and decision trees in science and engineering." *Cell*, 187, 1828-1833.

Based on course BIOE 395 taught at Stanford University.

---

*Attribution & Modification Notice: Adapted from `scientific-problem-selection` in [anthropics/life-sciences](https://github.com/anthropics/life-sciences/tree/0d38fe5c0a50d711ebe6ecd85dc84b98660579d0/scientific-problem-selection) (Apache-2.0; full license retained in `LICENSE.txt`). Modified by Cloudra to replace platform-specific references with Cloudra native tools and P0 biomedical MCP workflows.*

## Applicable Scenarios (适用场景)

- 新课题立项、博士/博士后开题或基金申报前的系统化选题构思、关键假设拆解与早期 Go/No-Go 实验设计。
- 科研项目推进受阻或实验陷入瓶颈时，通过决策树“高度切换”、参数解绑与问题倒置寻找高价值转向或替代方案。
- 在基础研究、技术平台开发与转化应用之间明确评价优化函数，避免与导师、审稿人或评审专家的价值标准错位。
- 结合 PubMed、bioRxiv、Open Targets、ChEMBL、ClinicalTrials 与 OpenAlex 检索，在投入重型计算或湿实验前完成有据可查的可行性与竞争态势评估。
