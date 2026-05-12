---
name: experiment-planner
description: Design rigorous experiment plans for research-aware engineering ideas, including objectives, comparison methods, controlled variables, benchmarks, metrics, ablations, failure cases, and evidence needed for claims.
---

<objective>
Convert a research or engineering idea into a rigorous, testable experiment plan.

The plan must follow standard experimental thinking:
- define what question the experiment answers;
- define which methods are compared;
- define which variables are controlled;
- define the platform, benchmark, dataset, or workload;
- define how result quality is judged.

The final answer must explicitly output these five items. Do not finish with only a generic proposal, todo list, or high-level research direction.
</objective>

<evidence_discipline>
Always distinguish evidence status:
- `source explicitly says`: exact statement from paper, documentation, or code.
- `source implies`: cautious interpretation with supporting evidence.
- `assistant inference`: your own reasoning, labeled explicitly.
- `unsupported`: no evidence yet.

Evidence levels:
- E0: search result, title, second-hand summary, AI summary.
- E1: abstract, introduction, or related-work high-level description.
- E2: method section with explicit mechanism.
- E3: algorithm, formula, pseudocode, parameters, complexity, ablation, or reproducible detail.
- E4: official or reproducible code with file/function/commit, or directly runnable implementation.

Never use search snippets, abstracts, introductions, related-work summaries, or AI summaries as proof that prior work already implements the user's idea. Treat E0/E1 as leads until method-level or code-level evidence exists.

If `research_tools/scripts` exists in the repository, prefer using those scripts for deterministic workitem, evidence-card, database, and novelty-matrix operations. If scripts are unavailable, perform the workflow manually and create equivalent artifacts only when the user asked for files.
</evidence_discipline>

<required_inputs>
Collect or infer these inputs before producing the final plan:
- experiment goal: research question, target claim, hypothesis, and falsification condition;
- methods to compare: proposed method, strongest prior-art baseline, engineering baseline, naive baseline if useful, and upper/lower bound if available;
- controlled variables: datasets, workload size, hardware/software platform, random seeds, training/search budget, implementation version, hyperparameters, preprocessing, stopping criteria, and measurement procedure;
- platform or benchmark: dataset, benchmark suite, simulator, hardware, environment, workload generator, task scale, and representativeness;
- result criteria: primary metric, secondary metrics, cost/resource metrics, robustness metrics, statistical method, pass/fail threshold, and known failure cases;
- constraints: compute budget, time budget, available code, available data, reproducibility requirements, and publication target if relevant.
</required_inputs>

<user_confirmation_policy>
Ask the user to confirm missing details when the answer materially changes the experiment design or the validity of the conclusions.

Prioritize confirmation for:
- the main claim or hypothesis;
- which baseline is considered the strongest comparison;
- the benchmark or dataset used as evidence;
- the primary metric and success threshold;
- compute/time budget constraints.

When a detail is missing but a conservative default is obvious, proceed with the default and label it under `Assumptions / Defaults`. Do not block on minor details that can be safely specified as assumptions.

When using a UI or tool that supports multiple-choice questions, ask concise choices. Otherwise ask direct, minimal questions in the user's language.
</user_confirmation_policy>

<planning_process>
Follow this process:

1. Restate the experiment goal as a falsifiable hypothesis.
2. Map each intended claim to the evidence needed to support it.
3. Choose comparison methods:
   - proposed method;
   - closest prior-art baseline supported by E2+ evidence when available;
   - practical engineering baseline from the codebase or common implementation;
   - simple naive baseline if it clarifies the gain;
   - upper/lower bound only when meaningful and feasible.
4. Define controlled variables so method differences, not hidden confounders, explain the result.
5. Select benchmarks, datasets, workloads, or platforms that directly exercise the claim.
6. Define metrics:
   - one primary metric used for the main conclusion;
   - secondary metrics for tradeoffs;
   - resource metrics for compute, memory, latency, energy, cost, or engineering overhead;
   - robustness metrics for stress, scale, distribution shift, or failure modes.
7. Specify ablations that isolate the proposed mechanism. Every ambitious claim needs at least one baseline and one ablation.
8. Specify failure cases, diagnostics, negative controls, and sanity checks.
9. Define statistical and analysis requirements: repeated runs, seeds, confidence intervals or variance reporting, significance tests when appropriate, and visualization/table artifacts.
10. Reduce scope to the minimum experiment set that can falsify the hypothesis quickly, then add optional extensions separately.
</planning_process>

<subagent_policy>
Use delegation only when the environment and user explicitly allow it. If delegation is allowed, split only separable concerns:
- baseline selection;
- metrics and workload design;
- ablation design;
- failure-mode diagnostics.

Require every delegated suggestion to map back to a specific claim, evidence gap, or controlled variable. Remove scope expansion that does not strengthen the claim-to-evidence chain.
</subagent_policy>

<final_output_requirements>
The final response must be a concrete experiment plan in the user's language. It must explicitly include these sections:

```markdown
# Experiment Plan

## 1. 实验目标
- research question:
- hypothesis:
- target claim:
- falsification condition:

## 2. 对比方法
| method | role | evidence/source | implementation notes | why included |
|---|---|---|---|---|

## 3. 控制变量
| variable | controlled value/procedure | reason | risk if uncontrolled |
|---|---|---|---|

## 4. 实验平台 / Benchmark
- dataset/workload:
- platform/simulator/hardware:
- environment:
- scale:
- representativeness:

## 5. 结果评价标准
- primary metric:
- secondary metrics:
- resource/cost metrics:
- robustness metrics:
- success threshold:
- failure threshold:

## 6. 实验矩阵
| experiment | methods compared | workload | metrics | expected evidence |
|---|---|---|---|---|

## 7. 统计与分析方法
- repeated runs/seeds:
- variance/confidence reporting:
- significance or comparison method:
- tables/figures to produce:

## 8. 风险、失败案例与诊断
- likely failure cases:
- diagnostics:
- negative controls/sanity checks:

## 9. 最小可发表证据
- required table:
- required figure:
- required ablation:
- required reproducibility artifact:

## Assumptions / Defaults
- list every important default chosen without user confirmation.
```

If the user asks for English output, translate the section titles while preserving the same nine required sections and the five mandatory experiment-design items.
</final_output_requirements>

<quality_bar>
The plan is acceptable only if:
- the hypothesis is falsifiable;
- every main claim has at least one baseline and one metric;
- controlled variables are specific enough for another researcher or engineer to reproduce the comparison;
- the benchmark/platform directly exercises the claimed mechanism;
- the primary metric can decide whether the method is better or worse;
- resource and robustness tradeoffs are not hidden;
- failure cases and diagnostics are included;
- assumptions are labeled instead of silently invented.
</quality_bar>

<ledger_handoff>
After creating or updating an experiment plan for a research workitem, use `$research-ledger` when available or requested to record hypotheses, required evidence, baselines, metrics, ablations, assumptions, and open risks.
</ledger_handoff>
