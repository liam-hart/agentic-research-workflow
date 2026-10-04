# AGENTS.md

Operating instructions for AI agents in this project. Replace the examples with your own; keep the file short, because every agent reads all of it at the start of every session.

**Owner:** you
**Updated:** YYYY-MM-DD

## How this file is organised

- This file holds invariants, authority, and pointers. Procedures live in skills (`.agents/skills/`), and rules for particular paths or task kinds live in `.agents/rules/`, routed by `.agents/rules/README.md`.
- Orient from `operations/STATE.md` (gates, blockers, next pickups), then the latest note in `operations/handoffs/`.
- When a workflow changes, update the skill or rule that owns it. Update this file only when an invariant or a pointer changes.

## What needs asking

- Structure, tool or library choices, anything hard to undo, and matters of taste come back to the owner as a short decision with options and a recommendation. Where one standard answer exists, apply it and say so.
- Ask before deleting files, changing more than a handful of notes in one pass, or creating a new top-level folder.
- Never send email or messages, and never write to shared drives or calendars, without explicit approval in the current session.

## Evidence

- Cite what you read. Never present a summary of a source as verified unless you opened the source.
- Keep raw evidence (PDF text, full tables, annotations) out of synthesis notes; link to it.
- Before naming a person or an organisation, check the project's own roster. If they are not there, ask.

## Execution and delegation

- One lead agent owns judgment, architecture, and interpretation. It hands bounded, checkable pieces to subagents and verifies their output before relying on it. See `.agents/rules/delegation.md`.

## Commits

- Commit verified changes at the end of a completed pass, staging files by name. Never `git add .` or `git commit -a`.
- Never commit credentials. Never push without explicit approval in the current session.

## Closing a session

- Run the project's checks and say plainly what was not checked. Compiling is not verification, and an agent's summary of its own work is not evidence.
- Write a handoff in `operations/handoffs/YYYY-MM-DD-HHMM.md` with a `## Walkthrough & Verification` section: what was asked and done, files changed and why, the commands run and their output, and what is still open. End it with the sign-off line described in `.agents/rules/handoff-signoff.md`.
- If a gate cleared or a blocker changed, update `operations/STATE.md` in the same pass.
