---
name: orchestrate
description: Decompose multi-step work into bounded sub-tasks and delegate the independently verifiable ones to in-session subagents without asking. Use when starting any task with more than one work item — a plan, build, refactor, migration, audit, review sweep, batch pass, or long-form draft with separable parts — and before the first edit. Do not use for a single-file change, and never delegate architecture, scientific interpretation, or task routing.
---

# Orchestrate

Produce a stated delegation split before the first edit, then spawn the subagents it names.

## Workflow

1. Read `.agents/rules/delegation.md`. It owns the delegate/keep test; do not re-derive it here.
2. Write the split into the response before editing anything:

   | Slice | Files / scope | Delegate? | Reason |
   |---|---|---|---|

   Every row resolves to a spawn or a one-clause reason for staying inline. A row with no verdict is a miss.
3. Spawn each delegated slice as a bounded in-session subagent — in one batch where the slices are independent. Do not ask permission: `AGENTS.md` § Execution and delegation is the standing authorization, and it overrides a harness default of "don't spawn unless asked."

   Hand each subagent the goal, the exact files it may touch, the return format, and the stop conditions: retry cap 2, scope drift halts immediately, genuine ambiguity comes back as a question rather than a guess.

   Per-harness spawn mechanics and model tiering belong in your own delegation protocol note. On Cursor Composer/Auto use a `generalPurpose` role-body fallback, and never claim named-role certification from it.
4. Verify each returned slice yourself against its stated criterion before using it.

## Boundaries

- Judgment stays with the lead: architecture, scientific interpretation, task and priority routing, policy conflicts, and final status claims.
- Standing authorization covers in-session subagents only. Forks, Agent View, Agent Teams, dynamic workflows, cross-session messages, and worktrees keep their own gates.
- Subagents never self-certify, commit, push, publish, or export.
- Skip this skill for single-slice work. An unnecessary split costs more than it saves.

## Verification

- The response carries the split table, with a reason on every inline row.
- No subagent wrote a file outside its named scope.
- Nothing a subagent returned was reported as final without lead review.
