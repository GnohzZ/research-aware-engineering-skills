---
name: claim-writer
description: Draft paper contribution statements from evidence cards, novelty matrix, and experiment plan. Use after novelty audit or when preparing related work, method motivation, contributions, limitations, or rebuttal language.
---

# Claim Writer

Your job is to draft claims that are proportional to evidence. Generate conservative, moderate, and ambitious versions, and state what evidence is required before using stronger claims.


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

- `ledger.md`;
- `novelty_matrix.md`;
- `experiment_plan.md`;
- evidence cards;
- experiment results if available.

## Subagent use

Use subagents for cold-reader review, not for inventing stronger claims.

- Reviewer-risk reader: flag phrases likely to trigger reviewer objections or unsupported priority claims.
- Related-work positioner: compare contribution language against closest evidence cards.
- Limitation reader: identify caveats that should be explicit before using moderate or ambitious claims.

The main agent drafts the final conservative, moderate, and ambitious versions. Subagents must cite evidence-card IDs or mark objections as unsupported.

## Required output

```markdown
# Claim Drafts

## Conservative claim
Safe with current evidence.

## Moderate claim
Usable if missing baselines/ablations are completed.

## Ambitious claim
Only usable after strong evidence. Avoid if evidence is missing.

## Required evidence before using ambitious claim
- missing prior-art coverage:
- missing baseline:
- missing ablation:
- missing statistical support:
- missing implementation/code detail:

## Related work positioning
| closest work | what it does | our difference | evidence cards |
|---|---|---|---|

## Contribution bullets
1. ...
2. ...
3. ...

## Limitations

## Reviewer-risk notes
```

## Language rules

Avoid unless justified by strong evidence:

- "first";
- "novel";
- "state-of-the-art";
- "solves";
- "general";
- "the literature has not".

Prefer safer phrasing:

- "we study ... under ... constraints";
- "we operationalize ... in ... setting";
- "we provide evidence that ...";
- "to our knowledge, under the examined setting ..." only after broad prior-art audit;
- "existing work provides related mechanisms, but lacks ... according to evidence cards ...".

## Ledger handoff

After drafting or revising claims for a workitem, automatically run `$research-ledger` to record the selected claim strength, required evidence for stronger claims, and reviewer-risk notes.
