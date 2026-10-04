---
name: session-closeout
description: Reconcile evidence-backed completion in a research vault, including canonical authorities, validation, one handoff, and remaining gates. Use when substantive work ends or the user explicitly requests closeout; use walkthrough only to format the final evidence section.
---

# Session Closeout

Treat closeout as evidence-backed reconciliation, not a declaration that work is done. Follow the live project `AGENTS.md`.

## Reconcile once

1. Inspect `git status --short`, the focused diff, the active handoff, and the canonical project or area authority for each changed claim, task, decision, or status.
2. Make the smallest supported authority update. Leave external or unverified work open. Do not use an aggregate dashboard as the task-status source.
3. Update the roadmap only when a cross-project priority, gate, dependency, deadline, or completion state changed.
4. Update policy or routine references only when the session changed their governed behavior.
5. Reconcile affected autonomous workload cards by revision check, recording actual delivery and remaining human gates. Refresh the registered project receipt even when eligibility is unchanged; it records checked task/input/contract fingerprints and the reason for no change. The workload receipt gate reports missed coverage; it never repairs tasks or promotes readiness.
6. Create one session handoff. Use `walkthrough` only to format its `## Walkthrough & Verification` section and verified sign-off; do not run a second reconciliation workflow.

Do not infer completion, invent tasks, choose priority or dates, edit guarded daily-note surfaces, or change external workspaces without authority.

## Verification

Run task-specific checks, then the live closeout checks:

```bash
python3 operations/scripts/validate-agent-closeout.py --phase session
git diff --check
```

When another concurrent session has a newer handoff, pass `--handoff operations/handoffs/<this-session>.md`; it must exist in that directory. This selects the receipt, never narrows the changed-file checks.

The session check scopes to the working tree and falls back to `HEAD`'s commit when the tree is clean, so a post-commit closeout cannot pass vacuously; `--base <ref>` scopes it to an explicit starting ref. It prints the scope it used, and a PASS over zero paths is not evidence. Test-only edits under `operations/scripts/` do not trip the governance gate.

Use `--phase release` only when release readiness is in scope. Report implementation success separately from dirty, unpushed, external, or approval-gated state.

## Boundaries

Commit under the project commit policy (here: verified changes at the end of a completed pass), staging only explicit files. Push, send, release, upload, or guarded external edits each require separate authorization. If no content changed, do not manufacture a handoff or commit.
