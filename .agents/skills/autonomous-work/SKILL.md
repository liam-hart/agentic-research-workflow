---
name: autonomous-work
description: Show, prepare, refresh, or execute persistent project-owned autonomous workload cards. Use when the user says “start working through autonomous tasks”, “show autonomous work across my projects”, or asks to prepare more eligible agent work. Ordinary task prioritization stays with plan-my-day or triage.
---

# Autonomous Work

Turn a finite project workload into verified deliverables. Cards describe execution contracts; boards and task notes retain status, dates, priority, and acceptance authority. Eligibility never grants permission.

## Resolve the request

Read the current project's AGENTS and live state first. Unqualified execution means the current project's declared queue. A portfolio show is read-only across registered projects; portfolio execution needs that explicit session scope. Resolve paths through your project registry (for example `operations/agent-config/autonomous-projects.toml`) and project manifests, never through old handoffs or filename assumptions. An unavailable checkout or remote authority stays unavailable.

This skill assumes your own queue engine and registry (a script that reads cards, claims them, and records receipts). Locate its root from a stable path rather than from where a bridge happens to link the skill. For cards/schema and command examples, read [the execution contract](references/contract.md).

## Show and refresh

Run a bounded live refresh, then summarize effective eligibility, last successful refresh, coverage, unavailable/stale inputs, active claims, and latest delivery evidence. Mechanical refresh records observations; it never stamps semantic readiness or turns tasks into Ready cards. If source fingerprints change, re-read the affected authority before revalidating. Do not reuse cached remote state after a failed request.

## Prepare

Inspect current tasks, decisions, review state, evidence, tools, and resource ownership. Propose or update cards by stable ID/source identity. Use exact write ownership, a finite deliverable, meaningful acceptance and verification, satisfied dependencies, and explicit non-goals. Ready requires all inputs available and no unresolved decision inside the slice. Unknown priority and dates are omitted. Keep preparation/blocked cards useful by naming the missing input or decision. Retire superseded cards with a reason; never silently delete them. Write through the engine's revision check after rereading the queue.

## Execute

1. Refresh; independently recheck session authorization and project policy. Persistent authority profiles refer to rules; they cannot replay a past session's grant. Never execute a card merely because its readiness says Ready.
2. Save a finite selected snapshot and any user limit. Default to its eligible items, serially. Discovered work stays in preparation for a later run.
3. Recheck each selected card immediately before starting. Atomically claim its card, exact write paths, and required resources with session/worktree identity. Project locks (for example a rig or bench lock file) remain authoritative. A conflict blocks that card; do not steal stale claims.
4. Checkpoint the intended deliverable and baseline before editing. Use bounded delegation under the project's rules, with explicit file ownership. Compare actual files with the checkpoint before every resumed mutation and use revision checks for queue writes. Preserve concurrent edits; investigate any unexpected diff.
5. Execute and run the card's verification. Checkpoint meaningful milestones and heartbeat during long work. Distinguish verified artifact, local commit, PR, merge, publication, and rig evidence. Record the actual state and remaining human gate; a delivered slice does not automatically close its parent task.
6. Finish the run with evidence and reconcile its card by revision check; refresh affected cards and closeout coverage, then release ownership. Record a card-level blocker and continue independent selected cards. Shared auth/policy/data-integrity failures stop that domain. No new task execution is scheduled automatically.

An empty queue gets one bounded preparation pass, then a report. Stop at snapshot exhaustion, requested limit, user stop, or no independent runnable items; never manufacture work or poll indefinitely.

## Recovery and closeout

On interruption, read the existing claim/checkpoints, actual diff, source/task state, test artifacts, and any authorized remote delivery state. Verify owner liveness before an explicit recovery or supersession. Preserve artifacts and never declare success from progress prose. Engine recovery requires a review acknowledgement; it does not substitute for inspection.

At closeout, record evidence in the project queue and its existing handoff authority. Refresh even when eligibility did not change, naming checked sources/cards and why. Run workload receipt coverage and the project's validators. Use your own closeout validator, for example `operations/scripts/<your-closeout-validator>.py`. Scheduled health/discovery is report-only: no new substantive cards, task edits, claims, executions, commits, or remote mutations.
