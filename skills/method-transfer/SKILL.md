---
name: method-transfer
description: Translate prior-art evidence into concrete engineering implementation plans, baselines, adaptations, or rejections. Use after evidence-extractor and before coding or experiment planning.
---

# Method Transfer

Your job is to bridge the gap between research claims and engineering implementation. Do not merely summarize papers; decide what can be built, adapted, used as a baseline, or rejected.


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

If `research_tools/scripts` exists in the repository, prefer using those scripts for deterministic file creation. If scripts are unavailable, perform the workflow manually and create the same files.


## Inputs

- current repository/code context;
- workitem `problem.md` and `proposal.md`;
- evidence cards;
- engineering constraints: latency, memory, runtime, hardware, data, deployment, interfaces, testing requirements.

## Transfer labels

Use exactly one label per source/component:

- `COPY`: can be implemented directly with minimal adaptation.
- `ADAPT`: concept is usable but needs nontrivial modification.
- `BASELINE`: should be implemented or run as comparison, not necessarily adopted.
- `REJECT`: not appropriate for this engineering setting.
- `UNKNOWN`: evidence insufficient.

## Subagent use

Use subagents when transfer requires independent codebase or baseline analysis.

- Codebase mapper: inspect current modules, extension points, configs, tests, metrics, and constraints.
- Baseline feasibility checker: inspect whether candidate prior-art methods can be implemented, approximated, or run as baselines.
- Risk checker: inspect license, dependency, runtime, hardware, or data constraints for third-party methods.

Keep write ownership with the main agent. Subagents return findings and suggested transfer labels; the main agent decides final `COPY` / `ADAPT` / `BASELINE` / `REJECT` / `UNKNOWN` and writes the transfer plan.

Do not ask subagents to implement code during method transfer unless the user explicitly asks for implementation work and file ownership is disjoint.

## Required output

```markdown
# Method Transfer Plan

## Current engineering constraints
- code modules:
- runtime constraints:
- data/workload constraints:
- evaluation constraints:

## Source method assumptions
| source/card | assumptions | mismatch with current setting | evidence level |
|---|---|---|---|

## Transfer decisions
| source/card | decision | reason | implementation action |
|---|---|---|---|

## Concrete implementation sketch
- files to modify:
- new interfaces:
- algorithm/data structures:
- configuration:
- tests:
- metrics/logging:

## Baseline plan
- baseline 1:
- baseline 2:

## Risks and missing details
- ...
```

## Engineering rules

- If actionability is `insufficient_detail`, do not invent missing algorithmic details. Either mark `UNKNOWN` or propose a clearly labeled approximation baseline.
- If using a third-party repository, inspect license before copying code.
- Never run downloaded code automatically.
- Prefer small, testable implementation increments.

## Ledger handoff

After making transfer decisions for a workitem, automatically run `$research-ledger` to record baseline choices, rejected sources, implementation assumptions, and missing details.
