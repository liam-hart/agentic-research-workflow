---
name: audit-research
description: "Audit the research vault read-only for structural integrity and return prioritized findings. Use when the user asks to audit the vault's links, tags, tasks, dashboards, handoffs, routines, or file placement; never repair during the audit."
---

# Research vault audit (/audit-research)

Produce a prioritized, read-only list of structural findings for the research vault. When this skill is invoked, audit only the research vault at `<vault>`. Do not audit the literature wiki except when a vault file explicitly points to it and the check is needed to validate that reference.

## Workflow

### 1. Load required session context

Read, in order:

- `AGENTS.md`
- latest active handoff in `operations/handoffs/`
- today's daily note in `inbox/daily-notes/`
- yesterday's daily note in `inbox/daily-notes/`

### 2. Run deterministic validators

Run only validators whose current help or documentation confirms a read-only or `--no-write` mode. Capture `git status --short` before and after and require byte-identical tracked state. For example, when supported:

```bash
python3 operations/scripts/validate-vault.py --no-write
python3 operations/scripts/lint-tags.py --no-write
python3 operations/scripts/audit-handoffs.py --no-write
```

If a script is missing, fails, or lacks a verified read-only interface, do not run its writing mode. Report the unavailable check; raise severity when it blocks a required invariant.

### 3. Check vault structure invariants

Verify the constraints in `AGENTS.md`, especially:

- daily-note write boundaries and processed markers
- literature notes are read-only except link wrapping and persist-block updates
- no raw PDF or bulk extracted text in the vault
- email and message drafts live under `inbox/messages/`
- handoffs use `operations/handoffs/`
- project, area, and resource files remain within the vault's declared folder structure

Use targeted searches rather than broad content dumps.

### 4. Check task and dashboard health

Inspect `inbox/Tasks.md` if present and sample current daily/project task references for:

- broken task-source links
- completed tasks that should be archived
- unresolved routed tasks duplicated in daily notes and project/area files

### 5. Check routine and script reference drift

Compare routine and script names in `AGENTS.md` against files under `operations/scripts/`, `operations/`, and active handoff notes. Flag missing scripts, stale routine names, and conflicting schedule descriptions.

## Output Format

Report findings as a flat prioritized action list. No prose preamble.

```unknown
HIGH
- [issue] — [file reference or count]

MEDIUM
- [issue] — [file reference or count]

LOW
- [issue] — [file reference or count]

CLEAN
- Checks passed: [list]
```

Use exact file paths and line numbers where available.

## Boundaries

`audit-research` proposes only; it never fixes, moves, deletes, or rewrites files unless the user explicitly approves a separate fix pass.

## Verification

- `git status --short` is byte-identical before and after the audit (step 2).
