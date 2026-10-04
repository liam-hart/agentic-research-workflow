---
name: audit-wiki
description: "Audit the literature wiki read-only for lint errors, unaudited work, count drift, orphan concepts, and state-log inconsistencies. Use when the user asks for a wiki audit; never repair during the audit."
---

# Literature Wiki Audit Skill (/audit-wiki)

Produce a prioritized, read-only list of findings for the literature wiki: lint errors, unaudited batches, count drift, orphan notes, and state-log drift. When this skill is invoked, audit only the literature wiki at `<wiki>`. Do not audit the research vault except for the normal session context and handoff logging required by `AGENTS.md`.

## Workflow

### 1. Run the linter

```bash
python3 "<wiki>/operations/scripts/wiki-lint.py" --no-write
```

Use the stdout report. Never generate or update a tracked lint report. If `--no-write` is unavailable, stop this check and report that the required read-only interface is missing.

### 2. Check for unaudited batches

Read `wiki/hot.md`. Inspect the batch table or latest audit-state section. Identify any batch where a source has been ingested but the audit column is blank or marked incomplete. Flag each unaudited batch by number and size.

### 3. Ingested count discrepancy

- From `wiki/index.md`, extract the total ingested/source-note count.
- From the lint report and file counts, extract the ingested/source-note count.
- If they differ, flag as HIGH with both numbers and the delta.

### 4. Concept count discrepancy

- From `wiki/index.md`, extract the managed corpus count block.
- Count actual `.md` files across the wiki's concept folders (for example `wiki/constructs/`, `wiki/theories/`, `wiki/methods/`), excluding any `_index.md` files.
- Skip any legacy concept directory that the wiki no longer uses.
- Compare the live total to the managed count block. Use the lint report's missing-concept-page and index-membership findings for link coverage.
- If counts differ, flag as MEDIUM unless the mismatch breaks links, in which case flag as HIGH.

### 5. Orphan concept notes

Read the lint report for any HIGH-severity orphan concept notes: concepts with no backlinks or source references. List each orphan by filename.

### 6. Log / hot.md drift

- Read the top entry of `wiki/log.md`.
- Read the latest action/current-state section of `wiki/hot.md`.
- If they describe different work, dates, counts, or batch state, flag as MEDIUM.

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

Use exact file paths and line numbers where available. If a section has no issues, omit it entirely and include the check under CLEAN.

## Verification

- Capture the wiki's tracked state (and the research vault's, if touched for context) before and after and require it to remain byte-identical.
