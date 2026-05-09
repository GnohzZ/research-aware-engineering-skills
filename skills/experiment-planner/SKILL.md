---
name: experiment-planner
description: Design minimal publishable experiments for a research-aware engineering idea, including hypotheses, baselines, metrics, ablations, workloads, failure cases, and evidence needed for claims.
---

# Experiment Planner

Your job is to convert a potentially novel engineering method into a testable research plan.


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

- problem/proposal;
- novelty audit;
- method-transfer report;
- available baselines;
- codebase constraints;
- compute/time budget if provided.

## Subagent use

Use subagents when experiment design has separable concerns.

- Baseline planner: choose closest prior-art and engineering baselines from evidence cards.
- Metrics/workload planner: propose primary metrics, stress workloads, datasets, and resource measurements.
- Ablation planner: identify minimal ablations that isolate the mechanism.
- Failure-mode planner: propose diagnostics, negative controls, and falsification cases.

Require each subagent to map suggestions to specific claims and evidence gaps. The main agent merges the plan, removes infeasible items, and chooses the minimum publishable experiment set.

Do not let subagents expand scope without a clear claim-to-evidence reason.

## Required output

```markdown
# Experiment Plan

## Hypothesis
A falsifiable statement.

## Claim-to-evidence map
| claim | required evidence | current status |
|---|---|---|

## Baselines
| baseline | source/evidence | implementation path | why needed |
|---|---|---|---|

## Metrics
- primary metric:
- secondary metrics:
- cost/resource metrics:
- robustness metrics:

## Workloads / datasets

## Ablations
| ablation | isolates | expected interpretation |
|---|---|---|

## Failure cases and diagnostics

## Minimum publishable evidence
- table:
- figure:
- qualitative case:
- repeated-run/statistical requirement:

## Execution plan
- quick sanity experiment:
- main experiment:
- stress test:
- analysis artifacts:

## Risks
```

## Experiment principles

- Every ambitious claim needs a baseline and an ablation.
- If the idea is a system optimization, include overhead and failure modes.
- If the idea is an adaptation of prior art, include the closest prior method as baseline if possible.
- Prefer a minimal experiment that can falsify the hypothesis quickly.
- Record negative results; they may become empirical novelty or limitations.

## Ledger handoff

After creating or updating an experiment plan for a workitem, automatically run `$research-ledger` to record hypotheses, required evidence, baselines, metrics, ablations, and open risks.
