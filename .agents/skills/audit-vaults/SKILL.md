---
name: audit-vaults
description: "Run read-only structural audits of both the research vault and the literature wiki and merge prioritized findings. Use when the user explicitly asks to audit both; use the single-vault audit skill otherwise."
---

# Cross-Vault Audit Skill (/audit-vaults)

Produce one merged, prioritized list of read-only findings covering both the research vault and the literature wiki. When this skill is invoked, run both audit scopes:

1. `audit-research` for `<vault>`
2. `audit-wiki` for `<wiki>`

Keep findings labeled by vault when reporting and when appending to the active handoff.

## Workflow

### 1. Run the research vault audit

Follow `.agents/skills/audit-research/SKILL.md`.

### 2. Run the wiki audit

Follow `.agents/skills/audit-wiki/SKILL.md`.

### 3. Merge findings

Combine both reports under one HIGH/MEDIUM/LOW/CLEAN structure. Prefix each finding with `[Vault]` or `[Wiki]`.

## Output Format

```unknown
HIGH
- [Vault] [issue] — [file reference or count]
- [Wiki] [issue] — [file reference or count]

MEDIUM
- [Vault] [issue] — [file reference or count]
- [Wiki] [issue] — [file reference or count]

LOW
- [Vault] [issue] — [file reference or count]
- [Wiki] [issue] — [file reference or count]

CLEAN
- [Vault] Checks passed: [list]
- [Wiki] Checks passed: [list]
```

## Boundaries

`audit-vaults` is a thin router. It proposes only and never mixes repair into the audit. Any fix requires a separate approved pass.

## Verification

- Both tracked worktrees remain byte-identical before and after the audit.
