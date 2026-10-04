---
name: feedback-reconcile
description: >-
  Reconcile advisor markup, reviewer comments, or collaborator feedback into the project's canonical task authority. Use when project-level feedback arrives and must be classified, routed, superseded, or escalated; use cover-letter to draft the outward response.
---

# Feedback Reconcile

**Purpose:** turn a pile of incoming feedback into routed, prioritized, correctly-placed project tasks — without duplicating raw text, without guessing metadata, and without escalating to the roadmap for things that aren't gates.

**Interactive only.** This routine asks the researcher for priority and due dates (see § 3). It cannot run unattended or as a cloud routine.

**Not a drafting tool.** This skill reconciles feedback into task state. Drafting the *reply* — an R&R cover letter or a point-by-point response-to-reviewers — belongs to the `cover-letter` skill. Hand off there; do not duplicate it here.

---

## 0. Orient before reading feedback

1. Read the latest handoff in `operations/handoffs/` and the project's canonical authority note (see [references/project-routing.md](references/project-routing.md)). Feedback is frequently *already partly reconciled* by an earlier round or by other work. Routing an item that was applied three commits ago is the main failure mode of this routine.
2. If the feedback references an external workspace (a shared drive or a collaborator's repository), read it there. Treat it as **read-only** — never write to it.
3. Note the feedback's **base version**. Feedback written against a stale copy may already be moot. Record the base (commit, date, or filename) in the run report.

---

## 1. Ingest and classify

Read the raw feedback from wherever it lives: a `.docx` comment digest, pasted review text, an email in `inbox/messages/`, or a Markdown markup file.

> [!danger] Zero raw text
> Never copy feedback text verbatim into any tracked file. Paraphrase every item into one sentence of your own words. This applies to reviewer comments, advisor comments, and email bodies alike. Quote only where an exact phrase is the thing under discussion (for example, a disputed sentence in the manuscript), and then only that fragment.

Classify every item into exactly one **section bucket**:

| Bucket | Covers |
|---|---|
| Theoretical Framing | Introduction, motivation, literature positioning, hypotheses as stated |
| Methods/Design | Participants, materials, procedure, preregistration, analysis plan |
| Results/Stats | Models, effect sizes, tables, figures, statistical reporting |
| Discussion | Interpretation, limitations, implications, tie-backs |
| Formatting/Citations | Reference list, citation fields, style, front matter, journal formatting |

And an **urgency** call, which is a proposal until the researcher confirms (§ 3):

| Urgency | Meaning |
|---|---|
| 🔺 Highest | Blocks submission/return, or the feedback is factually wrong in the current draft |
| ⏫ High | Substantive content change the reviewer expects to see addressed |
| 🔼 Medium | Real but self-contained; won't block the round |
| 🔽 Low | Polish, optional, or parked for a future paper |

Also record a **disposition** per item — this is what keeps the routine idempotent across rounds:

- `applied` — already in the canonical source; do not route
- `already-resolved` — independently fixed by other work; do not route, but note it
- `open` — needs action; **this is the only disposition that becomes a task**
- `needs-decision` — needs the researcher's judgment before it can even be scoped; route to `## Open Decisions` (or the project's equivalent), not to a task list
- `rejected` — deliberately not doing it; record the reason where the decision lives
- `no-disposition-recorded` — surfaced in the feedback but never dispositioned anywhere. Flag these loudly; an undispositioned advisor comment tends to get silently dropped.

---

## 2. Route into the project authority

**Check which pattern the project actually uses.** Read [references/project-routing.md](references/project-routing.md), then verify the live file and headings before every write. The reference contains conditional examples, not authority.

> [!danger] Verify the heading before inserting — do not trust the examples
> Projects can share *filenames* without sharing *structure*. One project's `Tasks.md` may have a single project-scoped heading where another has three topic headings; assuming symmetry misroutes the task or fails the insert outright. Heading layouts also drift as projects evolve, and any routing table will go stale.
>
> Before writing any item: `grep -nE "^#+ " "<target file>"` and confirm the destination heading exists **as written**.
>
> **If the exact heading is absent, you have no autonomous fallback.** Do not pick the nearest-looking heading and note it in the report — a plausible-but-wrong destination is the failure this guard exists to prevent, and it is *less* visible than a failed insert, not more. A task filed under a heading the researcher doesn't associate with it is one they will never find.
>
> Instead, stop and put it to the researcher, batched with the § 3 metadata questions:
> 1. show the target file's **actual** heading list, as printed by the grep;
> 2. name the destination you would have used and why it doesn't exist;
> 3. propose a specific heading from that list, marked as a proposal;
> 4. write only what they confirm. Route nothing on silence.
>
> **Never create a new heading in a project authority note to make a route work** — that is a structural edit, and § 6 requires approval first.
>
> The single exception, requiring no confirmation: a project whose routing row and headings you have verified unchanged this session, for a heading you have already confirmed by grep.

**Tag-filtered boards need the tag.** If a project's board is a live task query that filters by tag (for example `not done` / `tags include #project/<name>`), a routed task without that tag never surfaces. Check the board's query in the live file and apply its tag to every task routed there.

### Task line format

```
- [ ] ⏫ 📅 YYYY-MM-DD One-sentence paraphrase of the ask. #project/<name>
```

Priority emoji first, then due date, then text, then tag. Omit the priority emoji entirely for normal priority — no emoji *is* the default. Add a short `(Round 2, reviewer)` style provenance marker where the source isn't obvious from context.

### Superseding stale items

When new feedback overrides an existing item, resolve it in place — do not delete it. Git history is the recovery layer, and a silently deleted line erases a real record.

- **Checkbox tasks** resolve by checking the box: `- [x] task text ✓ Superseded YYYY-MM-DD — reason`
- **Non-checkbox bullets** resolve with strikethrough: `- ~~item~~ ✓ Superseded YYYY-MM-DD — reason`
- Never wrap a checkbox in strikethrough — the archiver won't match it and Tasks queries still see an open `[ ]`.

---

## 3. Metadata — ask, never guess

> [!warning] Binding constraint
> Project policy: *interactive sessions ask the researcher for priority and due date before finalizing a new task; never guess.*

This routine **proposes** priority and due dates; it does not set them. For each batch of open items:

1. Present the classified items with a **proposed** priority and due date and the one-line reason for each.
2. Wait for the researcher to confirm, adjust, or decline.
3. Write only what they confirm.
4. For anything they don't rule on, route it **without** priority/due metadata and tag it `#needs-triage`. An untriaged task is recoverable; a task with an invented deadline quietly corrupts the board's sort order.

Batch the questions — one round of proposals for the whole set, not one prompt per item. Fold any § 2 destination questions into this same round, so the researcher answers metadata and unresolved routing together.

**The two gates differ in what silence means.** An item the researcher doesn't rule on for *metadata* still gets routed, bare and tagged `#needs-triage` — the destination is known, only its priority isn't. An item whose *destination* is unresolved is **not written at all**; it stays in the run report as unrouted. Never fall back to `#needs-triage` in some default file to force an unrouted item into the vault — that turns a question about where something belongs into a task nobody is looking for.

---

## 4. Gate escalation — the test

Most feedback does **not** touch a gate. Escalate to the cross-project roadmap (for example `roadmap.md`) only if at least one is true:

- it **changes a target date** on a gate row, or invalidates one;
- it **adds or removes a blocker** named in a gate row;
- it **changes a dependency-register row** — for example *"manuscript feedback and final co-author sign-off"* or *"protocol and measurement freeze"*;
- it **changes readiness** for a primary gate (for example submission readiness or data-collection readiness).

Otherwise the project authority is the only file that changes. A typo list is not a gate event.

If a gate does change, the same-pass rule in the project's agent instructions applies, in this order:

1. Update the **canonical project authority** first (§ 2).
2. Then the roadmap — the headings in the example layout are `## Current gates` and `## Cross-project decision and dependency register`. Correct the superseded row rather than appending a new one alongside it.
3. Then the **active handoff**, in the same pass.

---

## 5. Run report

Write a per-run report to `operations/reports/feedback-reconcile-<project>-<YYYY-MM-DD>.md` covering:

- source of the feedback, its base version, and the reviewer
- the full classified inventory — every item with bucket, urgency, disposition, and its paraphrase
- what was routed and to which file/section
- what was **not** routed and why (applied / already-resolved / rejected)
- **unrouted — destination unresolved**: items whose target heading was absent and whose placement the researcher has not yet confirmed. List the actual headings found and the proposal put to the researcher. These are the only items that end a run neither written nor closed, so they must be impossible to miss in the report.
- any `no-disposition-recorded` items
- the gate-escalation decision and its reasoning, including a "no gate change" verdict

Report every item, including the ones that went nowhere. An item that was consciously skipped and an item that was overlooked look identical six weeks later.

---

## 6. Safety rules

Repository policy in `AGENTS.md` applies unchanged and is not repeated here: daily-note write surfaces, read-only external workspaces, the checkbox rule, any people dictionary, and commit and push policy. The zero-raw-text rule is stated in § 1. Three rules are specific to this skill:

- **Never route a task into a daily note.** Tasks go to the project authority (§ 2).
- **Literature notes are read-only.**
- **Propose, then execute** for structural edits. Adding tasks under an existing heading is routine; restructuring a project authority note needs approval first.

---

## 7. Close out

Append the `## Walkthrough & Verification` section and sign-off to the active handoff (per `AGENTS.md`). Link the run report (§ 5) and every vault file touched as `[[wikilinks]]`; use `[name](file:///path)` only for paths outside the vault.
