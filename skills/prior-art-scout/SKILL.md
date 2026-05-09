---
name: prior-art-scout
description: Find candidate prior art for an engineering idea without making final novelty claims. Use before implementation or novelty audit for algorithms, systems, performance optimizations, benchmarks, or research-like engineering proposals.
---

# Prior Art Scout

Your job is to discover candidate sources. You must not make final claims about novelty or equivalence. Treat all search results as leads until evidence cards are created.


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


## Inputs to seek

- `problem.md` or user task description.
- `proposal.md` if available.
- current repository context if relevant.
- constraints: domain, system setting, datasets/workloads, metrics, deployment constraints.

If some inputs are missing, proceed with best effort and state assumptions.

## Search strategy

Search in this order when available:

1. Local evidence database: `research/local_index/evidence.sqlite` and existing `research/workitems/**/evidence_cards`.
2. Official docs and standards for the relevant framework/system.
3. Academic sources: arXiv, conference proceedings, Semantic Scholar, OpenReview, ACM/IEEE pages where accessible.
4. Code: GitHub/GitLab official repos, artifact repos, benchmark repos.
5. Engineering blogs only as low-trust leads, unless they are official project documentation.

Generate diverse query classes:

- exact mechanism query;
- broader problem query;
- system-setting query;
- metric/failure-mode query;
- negative query designed to disprove novelty;
- code query with likely function/module terms.

## Subagent use

Use parallel subagents for broad prior-art search when the task is `STANDARD` or `DEEP`, or when multiple source classes are needed.

- Academic scout: papers, preprints, proceedings, OpenReview/Semantic Scholar/arXiv queries.
- Code/artifact scout: official repos, artifact repos, benchmark implementations, license notes.
- Docs/standards scout: official framework docs, standards, API behavior, existing local evidence database.
- Negative scout: deliberately search for sources that could weaken or falsify the proposed novelty.

Give each subagent a disjoint search surface and require: queries tried, candidate IDs, URLs/paths, why relevant, current evidence level, and evidence still needed.

The main agent must merge results, deduplicate candidates, assign final IDs, and update `search_queries.yaml`, `candidates.csv`, and `decisions.md`. Subagents must not make final novelty/equivalence claims.

## Candidate types

Use IDs:

- `P#`: paper or preprint.
- `R#`: code repository or artifact.
- `D#`: official doc or standard.
- `B#`: benchmark or dataset.
- `X#`: other source.

## Required output

```markdown
# Prior Art Scout

## Problem decomposition
- task:
- domain:
- mechanism keywords:
- system keywords:
- metric/failure keywords:
- likely closest communities:

## Search queries tried
| query | target | reason |
|---|---|---|

## Candidate sources
| id | type | title | year | source | why relevant | current evidence level | evidence needed |
|---|---|---:|---|---|---|---|---|

## Immediate engineering leads
- direct baseline candidates:
- official docs/APIs to check:
- code repositories to inspect:

## Not enough evidence yet
List sources that are related but only E0/E1.

## Next step
Run `$evidence-extractor` on: <ids>
```

## File updates

If a workitem exists, update:

- `search_queries.yaml`
- `candidates.csv`
- `decisions.md` with a short log entry

Use `research_tools/scripts/research_db.py query` before external search if available:

```bash
python research_tools/scripts/research_db.py query --root . --text "<query>"
```

## Ledger handoff

After updating candidate sources or search decisions for a workitem, automatically run `$research-ledger` to record the search state, candidate status, and next evidence-extraction actions.

## Forbidden output

Do not write:

- "P1 already solved this";
- "this idea is not novel";
- "this is the same method";
- "the literature has done X".

Allowed alternatives:

- "P1 is a candidate closest work; method-level evidence is needed.";
- "R1 may provide an implementable baseline; inspect files/functions first.";
- "D1 constrains implementation but does not determine novelty.".
