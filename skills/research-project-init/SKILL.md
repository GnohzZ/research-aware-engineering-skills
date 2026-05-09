---
name: research-project-init
description: Initialize the Research-Aware Engineering Toolkit inside the current repository. Use when a user asks for project-level install, research folder setup, AGENTS.md integration, or making global research-aware skills work persistently in a repo.
---

# Research Project Init

Initialize a repository for the research-aware engineering workflow.

## When to use

Use this skill when the user asks to:

- install the Research-Aware Engineering Toolkit into a specific repo;
- create `research/`, `research_tools/`, or research workitem folders;
- make `$research-gate`, `$prior-art-scout`, evidence cards, novelty audits, or ledgers persistent in a repo;
- fix a repo where global research skills exist but project-level files are missing.

## What to do

1. Identify the target repo.
   - Default to the current working directory.
   - If the user names a path, use that path.
   - Do not initialize a directory that does not exist.

2. Run the bundled initializer:

```bash
python ~/.agents/skills/research-project-init/scripts/research_project_init.py --repo .
```

Use `--repo /path/to/repo` for another target.

3. If the repo already has `AGENTS.md`, preserve it.
   - The script appends a marked Research-Aware Engineering block if missing.
   - It does not replace existing project instructions unless `--overwrite-agents-block` is passed.

4. Report the files created or already present, and suggest using `$research-gate` as the next entrypoint.

By default, the initializer does **not** copy skills into the repo. It relies on global `~/.agents/skills` so Codex does not show duplicate skill completions.

## Subagent use

Do not use subagents for ordinary initialization. This skill is a deterministic filesystem operation.

For unusual migrations only, use one read-only subagent to inspect an existing repo-specific `AGENTS.md`, `.agents/skills`, or `research/` layout and report conflicts before running the initializer. The main agent must run the script and decide what to prune or preserve.

## Options

- `--no-agents`: do not create or modify `AGENTS.md`.
- `--copy-skills`: also copy research skills into `.agents/skills`; only use this for portable repos where global skills are unavailable.
- `--skills-only`: only copy or prune research skills; combine with `--copy-skills` or `--prune-project-skills`.
- `--prune-project-skills`: remove project-local research-aware skills that duplicate global skills.
- `--overwrite`: replace existing copied skill/toolkit files.
- `--overwrite-agents-block`: replace an existing marked Research-Aware Engineering block in `AGENTS.md`.

## Expected repo layout

```text
<repo>/
├── AGENTS.md
├── research_tools/
└── research/
    ├── workitems/
    ├── local_index/
    └── templates/
```

## After init

For a new research-like engineering task, start with:

```text
$research-gate <task description>
```

For an existing idea that already needs prior art:

```text
$prior-art-scout 针对 research/workitems/<id>/ 查找相关论文、系统和开源代码。
```
