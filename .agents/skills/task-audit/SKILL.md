---
name: task-audit
description: "Audit the open-checkbox backlog for tasks already completed in practice, confirm them in batched interactive review, and reconcile the confirmed ones. Use when the user asks to audit, reconcile, or clean up open tasks. Do not use for the #needs-triage queue (that is triage) or for today's ranked work list (that is plan-my-day)."
---

# Task Audit

Close the gap between what the vault says is open and what is actually done. The
backlog is usually large; most of it is fine, a minority are stale records of
finished work, and only a human can tell which.

Evidence ranks. The researcher confirms. The script applies. Never collapse those steps.

## Workflow

1. **Gather.** Run `python3 operations/scripts/audit-tasks.py --scope <scope>`
   (read-only; add `--no-write` to skip the report file). Useful filters:
   `--priority high`, `--size quick,short`, `--file <prefix>`, `--group-by
   section|file|none`. Read the report, not the whole vault.

2. **Review in batches.** Work the `evidenced` partition only, one group at a
   time, at most 15 items. For each item show its `fingerprint`, the task text,
   a clickable `[file:line](file://…)` link, and the named evidence with its
   strength. Then stop and wait.

   The researcher replies in this syntax, using fingerprints:

   ```
   Done: a1b2c3d4, e5f6a7b8
   Check: 9c0d1e2f
   Not done: 3a4b5c6d
   Reschedule: 7e8f9a0b -> 2026-10-01
   ```

   Any id the researcher does not name is left untouched. Silence is never consent.

   **Review page (default for interactive batches).** Save the gather run as
   `--format json` to the scratchpad, put your own per-item findings in a
   `{fingerprint: text}` JSON file, then run
   `operations/scripts/audit-tasks-review-page.py <audit.json> --notes <notes.json>
   --out <scratchpad>/<name>.html` (filters: `--bucket`, `--due-before`,
   `--fingerprints`) and `open` it. Keep the page local rather than publishing it,
   since it contains private task text. The researcher clicks decisions and pastes back the
   reply text in the syntax above. The page leaves unanswered items out and never
   puts `Check:` items into its decisions JSON. Treat the pasted reply exactly
   like a typed one.

3. **Verify `Check:` items.** Investigate properly — read the referenced file,
   the commit, the artifact. Report what you found and ask again. A `Check:`
   item is never applied on the first pass.

4. **Apply.** Write the confirmed decisions to a JSON or TSV file, then run
   `audit-tasks.py --apply-decisions <file>` to preview and
   `--apply-decisions <file> --write` to land them. Report every refusal; a
   refusal means the script declined to guess, which is correct behavior, not a
   failure to work around.

5. **Hand off.** The report's quick-win section is a handoff, not a worklist for
   this skill. Name it and stop.

## Boundaries

- **This skill does not execute tasks.** It ends at reconciliation. An audit
  that also does the work has no clean boundary between what it verified and
  what it changed. Route execution to `plan-my-day` or a direct request.
- **Never propose `Done` for an item with no evidence.** Items in `no-signal`
  were not reviewed and this skill makes no claim about them. A lone `weak`
  signal (an artifact exists) is not grounds either: a written draft does not
  mean the task was to write it.
- **Agent-executable vs human-only is your judgment, not the script's.** A
  headset trial, physical gear, or a meeting cannot be agent-completed. The
  script offers no determination here.
- **Neighbouring skills.** `triage` owns the `#needs-triage` queue and assigns
  missing priority, due date, and size. `plan-my-day` owns today's ranked list,
  read-only. This skill owns retrospective reconciliation of the existing
  backlog, and bulk-rescheduling stale `📅` dates on tasks that already carry
  metadata.
- **Writes are the researcher's call.** `--write` runs only on decisions the researcher stated in this
  session. Never infer a decision from a previous batch or a plan document.
- Daily notes are never a write target. Commits and pushes are out of scope.

## Resources

- Engine and full safety contract: `operations/scripts/audit-tasks.py` (its
  module docstring is the authority on refusal behavior).
- Shared checkbox grammar and matching thresholds: `operations/scripts/task_lib.py`.

## Verification

- The apply run reports every decision as applied or refused, and exits non-zero
  if anything was refused.
- Re-running the audit after a write shows the reconciled items gone from the
  `evidenced` partition.
- `python3 -m unittest operations/scripts/test_audit_tasks.py` covers the
  refusal paths: unknown fingerprint, line edited underneath, parent with an
  open child, invalid reschedule date, and daily-note write attempts.
