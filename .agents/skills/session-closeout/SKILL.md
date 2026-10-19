---
name: session-closeout
description: Reconcile evidence-backed completion in a research vault, including canonical authorities, validation, one handoff, and remaining gates. Use when substantive work ends or the user explicitly requests closeout; use walkthrough only to format the final evidence section.
---

# Session Closeout

Treat closeout as evidence-backed reconciliation, not a declaration that work is done. Follow the live project `AGENTS.md`.

## Reconcile once

1. Fix this session's handoff first. Get the stamp from `date '+%Y-%m-%d-%H%M'`. Append only to a handoff of your own session that has no `Sign-off:` line yet; if the latest handoff is already signed off, start a new file. A handoff ends with exactly one sign-off.
2. Inspect `git status --short`, the focused diff, the active handoff, and the canonical project or area authority for each changed claim, task, decision, or status.
3. Make the smallest supported authority update. Leave external or unverified work open. Do not use an aggregate dashboard as the task-status source.
4. Update the roadmap only when a cross-project priority, gate, dependency, deadline, or completion state changed.
5. Update policy or routine references only when the session changed their governed behavior.
6. Reconcile affected autonomous workload cards by revision check, recording actual delivery and remaining human gates. Refresh the registered project receipt even when eligibility is unchanged; it records checked task/input/contract fingerprints and the reason for no change. The workload receipt gate reports missed coverage; it never repairs tasks or promotes readiness.
7. Write the handoff's walkthrough section. Use `walkthrough` only to format its `## Walkthrough & Verification` section and verified sign-off; do not run a second reconciliation workflow.

Do not infer completion, invent tasks, choose priority or dates, edit guarded daily-note surfaces, or change external workspaces without authority.

## Work in other repositories

Handoffs live in this project's `operations/handoffs/`, whichever repository the work touched. The other repository's own `AGENTS.md` names its closeout evidence (for example an issue or pull request with the commit, verification, and remaining gates); use it in addition to the handoff, and run that repository's own checks.

## Verification

Run task-specific checks, then the live closeout checks, passing this session's handoff:

```bash
python3 operations/scripts/validate-agent-closeout.py --phase session --handoff operations/handoffs/<this-session>.md
git diff --check
```

When another concurrent session has a newer handoff, pass `--handoff operations/handoffs/<this-session>.md`; it must exist in that directory. This selects the receipt, never narrows the changed-file checks.

The session check scopes to the working tree and falls back to `HEAD`'s commit when the tree is clean, so a post-commit closeout cannot pass vacuously; `--base <ref>` scopes it to an explicit starting ref. It prints the scope it used, and a PASS over zero paths is not evidence. Test-only edits under `operations/scripts/` do not trip the governance gate.

Use `--phase release` only when release readiness is in scope. Report implementation success separately from dirty, unpushed, external, or approval-gated state.

## Boundaries

Commit under the project commit policy (here: verified changes at the end of a completed pass), staging only explicit files. Push, send, release, upload, or guarded external edits each require separate authorization. If no content changed, do not manufacture a handoff or commit.
