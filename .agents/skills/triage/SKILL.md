---
name: triage
description: >-
  Interactively cluster, route, prioritize, and resolve the #needs-triage task queue with the researcher's confirmation. Use when the user asks to triage tasks or process #needs-triage; use plan-my-day for read-only daily prioritization, and task-audit to reconcile already-completed tasks or bulk-reschedule stale dates.
---

# Triage

**Purpose:** Interactively audit, cluster, and route `#needs-triage` tasks using an upfront **Structural Sweep** (duplicate detection, task folding, and multi-part task decomposition) followed by interactive priority, due date, and sizing resolution.

## Context & Heuristics for Recommendations

Before presenting candidates, consult the current roadmap, development-plan or area authority, calendar context, and destination project task authority. Derive rankings and dates from those live sources; the examples below are not authority.
1. **Priority Hierarchy:**
   - Read the current ordering from the live development plan and roadmap; do not retain a ranking in this skill.
2. **Date Anchors:**
   - Immediate blockers: next 1–3 business days.
   - Sprint deliverables: upcoming Friday sprint check (e.g. `YYYY-MM-DD`).
   - Project milestones: only dates explicitly present in a current authority.
   - Calendar proximity, urgency inference, or a related meeting does not authorize a priority or due date. When the task's authority supplies neither, label both unspecified and ask the researcher rather than recommending values.
3. **Task Sizing Taxonomy (your tag dictionary):**
   - `#size/quick`: < 15 min, single small edit, no research needed.
   - `#size/short`: 15 min to 1 hour, one sitting.
   - `#size/day`: Half-day to full day of focused work.
   - `#size/multi-day`: Spans multiple sessions (primary candidate for splitting).

---

## Workflow

### Phase 1: Pre-Triage Structural Sweep

1. **Find Candidates:** Capture `git status --short`, then run `python3 operations/scripts/aggregate-needs-triage.py --no-write` to collect all `#needs-triage` task lines across `inbox/`, `projects/`, and `areas/`. Capture Git status again and require byte-identical tracked state before presenting the census; if discovery changed tracked state, stop and report the leak.
2. **Cross-Reference & Cluster:** Compare candidates against each other and against existing open tasks in primary destination authority notes (for example each project's `Tasks.md`, a build checklist, a manuscript status note, a lab-operations note, and a personal-notes note).
   - 🔍 **Duplicate / Redundancy Detection:** Identify candidates that duplicate an existing open task in the destination note or duplicate another candidate.
   - 🗂️ **Fold / Consolidation Clusters:** Identify related granular micro-tasks that belong under a single cohesive milestone or parent task.
   - ✂️ **Split / Decomposition Candidates:** Identify oversized tasks (multi-outcome deliverables, mixed dependencies across code/methods/IRB, or `#size/multi-day` items) that need breaking down into 2+ discrete atomic tasks.
   - 📌 **Standalone Candidates:** Single, well-scoped discrete actionable tasks.
3. **Display Initial Census:** Output a concise high-level summary to the researcher before launching the step-by-step loop (e.g., *"Found 28 candidates: 4 duplicate/fold candidates, 2 split candidates, 22 standalone candidates"*).

---

### Phase 2: Interactive Triage Loop

For each task (or task cluster):

1. **Daily Notes Check:** If the source file is under `inbox/daily notes/`, it is **out of scope** for in-place modification (your project's daily-note rule). State that it lives in a daily note and must be routed via `/process-daily-notes`, then move to the next candidate.
2. **Formulate Bundled Recommendation:**
   - **Target File & Section:** Canonical destination authority note.
   - **Priority Emoji & Due Date:** Aligned to plan/roadmap gates.
   - **Task Sizing:** `#size/quick`, `#size/short`, `#size/day`, or `#size/multi-day`.
   - **Structural Recommendation:**
     - *If Standalone:* Route with recommended metadata.
     - *If Duplicate/Fold:* Name the target task to fold into, moving specifics into sub-bullets or comments.
     - *If Split:* Propose 2–3 discrete subtasks with individual priorities, due dates, and sizing.
   - **Rationale:** 1-line grounding in project roadmap/plan context.

**Example AI prompt to user:**
```markdown
### Task X of Y
> **`- [ ] Task description text`**
> *Source:* `projects/<project>/SourceFile.md:line`
> *Context/Annotation:* `<!-- reconciled ... -->`

**Recommended Resolution:**
- **Target:** `projects/<project>/Tasks.md` (Section/Context)
- **Priority:** ⏫ High (`2` / goal 2 in the current plan — Project B critical path)
- **Due Date:** proposed only from a current explicit authority
- **Size:** `#size/short`
- **Structural Action:** Standalone / Fold into [Task] / Split into [Subtasks]
- **Rationale:** Cite the current authority and gate that justify the recommendation.

**Actions:**
- **A** (or Enter / "yes"): Accept recommendation as-is
- **B**: Accept target, but customize Priority (1–5), Due Date (`YYYY-MM-DD`), and/or Sizing
- **C**: Choose alternative target file/section
- **F**: Fold / Merge into target task (preserves provenance/sub-items)
- **S**: Split into proposed discrete subtasks
- **D**: Mark Completed in its current authority file
- **E**: Delete / Discard (remove completely)
```

**Wait for the user's response in the chat.** Do NOT process the next task until the user has responded.

---

### Phase 3: Execution & Metadata Hygiene

Once the researcher selects an action:
- **Accept (A) / Custom (B) / Retarget (C):**
  1. Remove the task from its source file.
  2. Append/place in the confirmed destination file under the appropriate section.
  3. Format with confirmed priority emoji, due date (`📅 YYYY-MM-DD`), sizing (`#size/*`), and area/project tag (`#project/*`, `#area/*`).
  4. Remove `#needs-triage`.
  5. Preserve all existing reconciliation comments (`<!-- reconciled ... -->`) and provenance headers (`> *From [[...]]:*`).
- **Fold / Merge (F):**
  1. Remove the redundant task from the source file.
  2. Update the destination task or append relevant sub-bullets/provenance notes to the parent task.
- **Split (S):**
  1. Remove the oversized task from the source file.
  2. Insert the confirmed atomic subtasks in the destination file, each with its own checkbox, priority, due date, sizing, and tags.
- **Mark Completed (D):** Check the task in its canonical authority using the vault completion convention. Leave movement to the canonical archiver.
- **Delete / Discard (E):**
  1. Remove the task from its source file completely.

---

## Boundaries

- **Audits propose; the researcher approves:** Never silently merge, delete, or decompose tasks without user confirmation.
- **One at a time:** Pause and wait for the researcher's input for each candidate (or candidate cluster).
- **Metadata Format:** Use standard Tasks plugin emoji format (`⏫ 📅 YYYY-MM-DD #tag #size/short`).
- **Preserve Provenance:** Retain HTML reconciliation comments and dated block headers across all moves and splits.
- **Destination safety:** If a documented target file or heading is missing or changed, propose the destination and stop; never invent a replacement heading.
- **Scope boundary with `task-audit`:** This skill assigns metadata to tasks that lack it. Reconciling tasks that are already done, and bulk-rescheduling stale `📅` dates on tasks that already carry priority and sizing, belong to `task-audit`.
