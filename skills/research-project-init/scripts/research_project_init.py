#!/usr/bin/env python3
"""Initialize Research-Aware Engineering Toolkit files in a repository."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

RESEARCH_SKILLS = [
    "research-project-init",
    "research-gate",
    "prior-art-scout",
    "evidence-extractor",
    "method-transfer",
    "novelty-auditor",
    "experiment-planner",
    "claim-writer",
    "research-ledger",
]

MARKER_BEGIN = "<!-- RAE-TOOLKIT-BEGIN -->"
MARKER_END = "<!-- RAE-TOOLKIT-END -->"

AGENTS_BLOCK = f"""{MARKER_BEGIN}
# Research-Aware Engineering Protocol

For algorithmic, architectural, performance, evaluation, benchmark, robustness, or publishable engineering work, route through the research-aware workflow before making novelty or priority claims.

Use these skills as needed:

- `$research-gate`: classify whether the task needs research handling.
- `$prior-art-scout`: collect candidate prior art without final novelty claims.
- `$evidence-extractor`: create auditable evidence cards from papers, docs, or code.
- `$method-transfer`: turn evidence into implementation or baseline plans.
- `$novelty-auditor`: compare proposal claims against evidence cards.
- `$experiment-planner`: design baselines, metrics, ablations, and failure cases.
- `$claim-writer`: write conservative contribution claims from evidence and results.
- `$research-ledger`: maintain decisions, claim status, and long-term research state.

Evidence discipline:

- Do not treat search snippets, abstracts, related work, or AI summaries as proof that prior work already implements an idea.
- Label statements as `source explicitly says`, `source implies`, `assistant inference`, or `unsupported`.
- Prefer `research_tools/scripts` for deterministic workitem, evidence-card, database, and novelty-matrix operations.
{MARKER_END}
"""

TEMPLATES = {
    "problem.md": "# Problem\n\n## Context\n\n## Goal\n\n## Constraints\n",
    "proposal.md": "# Proposal\n\n## Mechanism\n\n## Expected benefit\n\n## Risks\n",
    "search_queries.yaml": "queries: []\n",
    "candidates.csv": "id,type,title,year,source,why_relevant,current_evidence_level,evidence_needed,status\n",
    "evidence_card.yaml": (
        "source_id: \"\"\n"
        "title: \"\"\n"
        "evidence_level: E0\n"
        "claim: \"\"\n"
        "quote: \"\"\n"
        "relation: unknown\n"
        "actionability: unknown\n"
    ),
    "novelty_matrix.md": "# Novelty Matrix\n\n| claim | closest evidence | overlap | risk | next action |\n|---|---|---|---|---|\n",
    "experiment_plan.md": "# Experiment Plan\n\n## Baselines\n\n## Metrics\n\n## Ablations\n\n## Failure cases\n",
    "decisions.md": "# Decisions\n\n| date | decision | evidence ids | reason | follow-up |\n|---|---|---|---|---|\n",
    "ledger.md": "# Research Ledger\n\n## Evidence inventory\n\n## Claim status\n\n## Next actions\n",
}


def copytree_merge(src: Path, dst: Path, overwrite: bool) -> tuple[int, int]:
    copied = 0
    skipped = 0
    if not src.exists():
        raise FileNotFoundError(src)
    for item in src.rglob("*"):
        rel = item.relative_to(src)
        target = dst / rel
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        if target.exists() and not overwrite:
            skipped += 1
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, target)
        copied += 1
    return copied, skipped


def write_if_missing(path: Path, text: str, overwrite: bool = False) -> str:
    if path.exists() and not overwrite:
        return "exists"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return "written"


def update_agents(repo: Path, overwrite_block: bool) -> str:
    target = repo / "AGENTS.md"
    if not target.exists():
        target.write_text(AGENTS_BLOCK + "\n", encoding="utf-8")
        return "created"

    existing = target.read_text(encoding="utf-8")
    has_begin = MARKER_BEGIN in existing
    has_end = MARKER_END in existing
    if has_begin and has_end:
        if not overwrite_block:
            return "already-marked"
        before = existing.split(MARKER_BEGIN, 1)[0].rstrip()
        after = existing.split(MARKER_END, 1)[1].lstrip()
        target.write_text((before + "\n\n" if before else "") + AGENTS_BLOCK + ("\n\n" + after if after else "\n"), encoding="utf-8")
        return "replaced-block"

    target.write_text(existing.rstrip() + "\n\n" + AGENTS_BLOCK + "\n", encoding="utf-8")
    return "appended"


def prune_project_skills(repo: Path) -> None:
    for name in RESEARCH_SKILLS:
        target = repo / ".agents" / "skills" / name
        if target.exists():
            shutil.rmtree(target)
            print(f"Removed project skill: {target}")


def copy_project_skills(repo: Path, overwrite: bool) -> None:
    global_skills = Path.home() / ".agents" / "skills"
    for name in RESEARCH_SKILLS:
        src = global_skills / name
        dst = repo / ".agents" / "skills" / name
        if not src.exists():
            print(f"Missing global skill, skipped: {name}")
            continue
        copied, skipped = copytree_merge(src, dst, overwrite)
        print(f"Skill {name}: copied {copied}, skipped {skipped}")


def init_repo(
    repo: Path,
    overwrite: bool,
    copy_skills: bool,
    skills_only: bool,
    no_agents: bool,
    overwrite_agents_block: bool,
    prune_skills: bool,
) -> None:
    repo = repo.resolve()
    if not repo.exists():
        raise FileNotFoundError(repo)
    if not repo.is_dir():
        raise NotADirectoryError(repo)

    home = Path.home()
    global_tools = home / ".codex" / "research-aware-engineering-toolkit" / "research_tools"

    print(f"Repository: {repo}")

    if prune_skills:
        prune_project_skills(repo)

    if copy_skills:
        copy_project_skills(repo, overwrite)
    else:
        print("Project skills: skipped; using global ~/.agents/skills to avoid duplicate Codex completions")

    if skills_only:
        print("Skipped research_tools, research folders, and AGENTS.md due to --skills-only")
        return

    copied, skipped = copytree_merge(global_tools, repo / "research_tools", overwrite)
    print(f"research_tools: copied {copied}, skipped {skipped}")

    for rel in ["research/workitems", "research/local_index", "research/templates"]:
        d = repo / rel
        d.mkdir(parents=True, exist_ok=True)
        keep_status = write_if_missing(d / ".gitkeep", "", overwrite=False)
        print(f"{rel}: ready ({keep_status} .gitkeep)")

    for name, text in TEMPLATES.items():
        status = write_if_missing(repo / "research" / "templates" / name, text, overwrite=overwrite)
        print(f"template {name}: {status}")

    if no_agents:
        print("AGENTS.md: skipped due to --no-agents")
    else:
        print(f"AGENTS.md: {update_agents(repo, overwrite_agents_block)}")

    print("Done. Start with: $research-gate <task description>")


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize Research-Aware Engineering Toolkit files in a repository.")
    parser.add_argument("--repo", type=Path, default=Path("."), help="Target repository path. Defaults to current directory.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite copied skills, tools, and templates.")
    parser.add_argument("--copy-skills", action="store_true", help="Also copy research skills into the repo. Off by default to avoid duplicate Codex completions when global skills are installed.")
    parser.add_argument("--skills-only", action="store_true", help="Only copy or prune research skills; requires --copy-skills or --prune-project-skills to do work.")
    parser.add_argument("--no-agents", action="store_true", help="Do not create or modify AGENTS.md.")
    parser.add_argument("--overwrite-agents-block", action="store_true", help="Replace an existing marked Research-Aware Engineering block.")
    parser.add_argument("--prune-project-skills", action="store_true", help="Remove project-local research-aware skills that duplicate global skills.")
    args = parser.parse_args()
    init_repo(
        args.repo,
        args.overwrite,
        args.copy_skills,
        args.skills_only,
        args.no_agents,
        args.overwrite_agents_block,
        args.prune_project_skills,
    )


if __name__ == "__main__":
    main()
