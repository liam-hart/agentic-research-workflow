---
name: walkthrough
description: Format the evidence and verified sign-off section for a CLI session walkthrough. Use when session-closeout delegates final walkthrough formatting or the user explicitly requests a walkthrough artifact; do not reconcile authorities or create a second closeout.
---

# Walkthrough

Use this skill only to format an evidence-bound walkthrough and verified sign-off. `session-closeout` owns authority reconciliation, validation selection, and the single handoff; this skill must not run a second closeout workflow.

## Execution Instructions by Agent Harness

- **Antigravity CLI (`agy`)**:
  Create `<appDataDir>/brain/<conversation-id>/walkthrough.md` as a user-facing artifact (`user_facing: true`) using `write_to_file`, and provide a concise summary with a clickable `file:///...` link in chat.
- **Claude Code / Codex CLI / Cursor Agent CLI**:
  Append or write a `## Walkthrough & Verification` section to the active session handoff (`operations/handoffs/YYYY-MM-DD-HHMM.md`) or write a standalone closeout markdown file to disk. Inside vault notes, handoffs included, link vault files as `[[wikilinks]]` and use `[basename](file:///path)` only for paths outside the vault; chat replies keep clickable `file:///` links.

## Verified Model Sign-off

End every walkthrough with `Sign-off: <Model Name> (effort: <level>)`. `.agents/rules/handoff-signoff.md` owns the live-metadata lookup order, the controlled model-name vocabulary, and the effort values; follow it rather than a copy here. Never take either value from a UI label or a previous session.

Before writing the sign-off, compare it once against the authority used. If an existing sign-off is wrong, correct it explicitly; do not preserve or repeat the guessed value.

---

## Required Structure

```markdown
## Walkthrough & Verification

### Executive Summary
Provide a 2–3 sentence high-level summary of what was requested, planned, and accomplished during the session.

### Changes Made
List every modified, created, or deleted file with a link and brief rationale. Link vault files as `[[wikilinks]]`; use `[name](file:///path)` only for paths outside the vault:
- [[Note Name]]: Description of note update.
- [`file_basename.py`](file:///absolute/path/outside/vault/file_basename.py): Description of changes made.

### Verification & Testing
Document the exact verification commands executed and their output:
- **Command**: `python3 path/to/script.py`
- **Output**: Clean exit code 0 / passing test suite results.
- **Manual Verification**: Detailed steps or UI verification performed.

### Next Steps & Handoff
- List any user review gates, follow-up actions, or next-session prerequisites.
```
