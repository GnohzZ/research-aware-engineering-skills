---
name: research-ledger
description: Maintain the long-term research ledger for a workitem, including evidence inventory, decision log, novelty evolution, claim status, and next actions. Automatically use after prior-art scouting, evidence extraction, method transfer, novelty audit, experiment planning, claim writing, experiment results, or major engineering changes when a research/workitems path exists.
---

# Research Ledger

Your job is to keep research state persistent and audit-friendly.


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

- workitem directory;
- evidence cards;
- novelty matrix;
- experiment plan;
- decisions log;
- code changes and experiment outputs if available.

## Auto-trigger rule

Use this skill automatically whenever a previous research-aware skill changed or produced any of:

- `candidates.csv`, `evidence_cards/`, `novelty_matrix.md`, `experiment_plan.md`, `decisions.md`, or `ledger.md`;
- a method-transfer decision, claim-risk judgment, baseline choice, or experiment result;
- a major code change that affects the proposal, claims, baselines, metrics, or evidence status.

If there is no workitem path, ask for or infer the target workitem before updating files.

## Subagent use

Keep ledger writes centralized. Use subagents only for read-only summarization when a workitem has many artifacts.

- Evidence inventory subagent: summarize new or changed evidence cards.
- Claim-status subagent: compare `novelty_matrix.md`, `experiment_plan.md`, and claim drafts for stale status.
- Experiment-result subagent: summarize result files or logs if present.

The main agent must write `ledger.md`, `decisions.md`, `candidates.csv`, and SQLite updates. Do not let multiple subagents edit ledger files concurrently.

## Required updates

Update or create:

- `ledger.md`;
- `decisions.md`;
- `candidates.csv` status fields if relevant;
- `novelty_matrix.md` summaries if evidence changed;
- local SQLite index if `research_tools/scripts/research_db.py` exists.

## Required output

```markdown
# Ledger Update

## Workitem
<path>

## Changes recorded
- evidence:
- decisions:
- novelty:
- experiments:

## Current claim status
| claim | status | evidence | risk |
|---|---|---|---|

## Next actions
1. ...
2. ...
```

## Decision log format

Append rows to `decisions.md`:

```markdown
| YYYY-MM-DD | decision | evidence ids | reason | follow-up |
```

## SQLite index

If available, run:

```bash
python research_tools/scripts/research_db.py ingest --root . --workitem <workitem>
```

Do not delete old evidence. If a judgment changes, append an update explaining why.
