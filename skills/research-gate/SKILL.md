---
name: research-gate
description: Decide whether an engineering task needs research handling, prior-art search, evidence extraction, novelty audit, or experiment planning. Use for algorithmic, architectural, performance, evaluation, benchmark, robustness, or potentially publishable engineering work.
---

# Research Gate

You are the routing layer for research-aware engineering. Your job is not to judge novelty. Your job is to decide whether the current engineering task should enter the research workflow and what the next skill should be.


## Global evidence discipline

Always distinguish:

- `source explicitly says`: exact statement from paper/doc/code.
- `source implies`: cautious interpretation with supporting evidence.
- `assistant inference`: your own reasoning; label it explicitly.
- `unsupported`: no evidence yet.

Never use search snippets, abstracts, introductions, related-work summaries, or AI summaries as proof that prior work already implements the user's idea. Treat them as E0/E1 leads until method-level or code-level evidence exists.

Evidence levels:

- E0: search result, title, second-hand summary, AI summary.
- E1: abstract/introduction/related work high-level description.
- E2: method section with explicit mechanism.
- E3: algorithm, formula, pseudocode, parameters, complexity, ablation, or reproducible detail.
- E4: official or reproducible code with file/function/commit, or directly runnable implementation.

If `research_tools/scripts` exists in the repository, prefer using those scripts for deterministic file creation. If scripts are unavailable and project-level persistence is desired, route to `$research-project-init` before creating workitems manually.


## Trigger conditions

Use this skill when the task involves any of the following:

- algorithm design or modification;
- system architecture, scheduling, caching, batching, indexing, routing, memory management, parallelism, compiler/runtime behavior;
- training, inference, model behavior, data processing strategy;
- performance optimization where the solution may generalize;
- evaluation protocol, benchmark, metric, or ablation design;
- robustness, failure modes, debugging insight that may become a finding;
- the user asks whether something is innovative, publishable, or paper-worthy;
- a solution receives a name, has a reusable mechanism, or may justify experiments.

Do not trigger for ordinary syntax fixes, trivial refactors, formatting, one-off API wiring, or mechanical implementation unless the user asks for research relevance.

## Classification

Classify into exactly one:

- `NONE`: ordinary implementation; no research handling needed.
- `LIGHT`: quick check of official docs, existing libraries, or obvious engineering patterns.
- `STANDARD`: prior-art scout plus evidence extraction needed.
- `DEEP`: likely paper contribution; novelty audit and experiment plan needed.

## Subagent use

Use subagents only for non-blocking context gathering, not for the final routing decision.

- For large or unfamiliar codebases, spawn one explorer subagent to map relevant modules, interfaces, metrics, and existing experiments while you classify the task.
- For broad `DEEP` tasks, optionally spawn one researcher subagent to identify likely research communities and search keywords.
- Do not let subagents decide novelty, publishability, or claim safety. The main agent must make the final `NONE` / `LIGHT` / `STANDARD` / `DEEP` decision.
- Subagents should return concise evidence, paths, and uncertainty; the main agent writes the workitem and next-skill instructions.

## Required output

Produce this structure:

```markdown
# Research Gate Decision

## Engineering task
<precise restatement>

## Research intensity
NONE | LIGHT | STANDARD | DEEP

## Why
<bullet list, concise>

## Workitem
- required: yes/no
- path: research/workitems/<YYYY-MM-DD-short-slug>/

## Next skill
- $prior-art-scout / $evidence-extractor / $novelty-auditor / $experiment-planner / none

## Immediate instructions for implementation
<what to do before coding, while coding, and after coding>
```

## Workitem creation

For `STANDARD` or `DEEP`, create a workitem if one does not exist:

```bash
python research_tools/scripts/research_new_workitem.py "<short-slug>" --intensity <STANDARD|DEEP> --root .
```

If the script is unavailable, first suggest initializing the repo:

```text
$research-project-init
```

If initialization is declined or not possible, manually create:

```text
research/workitems/<YYYY-MM-DD-short-slug>/
├── problem.md
├── proposal.md
├── search_queries.yaml
├── candidates.csv
├── evidence_cards/
├── novelty_matrix.md
├── experiment_plan.md
├── decisions.md
└── ledger.md
```

## Important limits

Do not say:

- "this is novel";
- "prior work already did this";
- "this can be published".

Instead route to the next skill.
