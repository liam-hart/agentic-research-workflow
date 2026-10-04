---
name: plan-my-day
description: "Synthesize current handoffs, daily notes, deadlines, and project state into a ranked daily work list with human-only versus agent-executable actions. Use when the user asks to plan or prioritize the day; use triage to mutate the needs-triage queue."
---

# Plan My Day

Use this skill at the start of a session to synthesize recent context into a concrete, prioritized work list.

---

## 1. Context Gathering (read in this order)

1. **Strategic Compass:** Read your roadmap note (e.g. `areas/<area>/Roadmap.md`) for current priorities and gates; verify them against live project authorities.
2. **Upcoming & Overdue Tasks:** Run `python3 operations/scripts/aggregate-upcoming-tasks.py --days 14` to gather ground-truth deadlines, overdue items, and high-priority backlog tasks across the vault without manual file hunting.
3. **Latest handoff:** Run `ls -lt operations/handoffs/`, then read the newest timestamped handoff for active session momentum.
4. **Today's daily note:** `inbox/daily-notes/YYYY-MM-DD.md` (use today's date)
5. **Yesterday's daily note:** `inbox/daily-notes/YYYY-MM-DD.md` (use yesterday's date)
6. If study work is likely: read the relevant `Study Home.md` and its action-items note. (Archived frameworks are background only; active design decisions live in the study docs.)

Do NOT read all project files or audit the full vault. The scanner + roadmap + handoff + daily notes give full coverage.

If an automated email digest of the vault exists, treat it as facts only; this skill does all ranking, so never treat digest output as a to-do list.

---

## 2. Classification Pass

After gathering context, classify all open items into three buckets:

**Personal obligations** — real-world tasks (calls, errands, admin) that require the researcher, read from the daily note or a personal-tasks note. List these first, briefly, so they're not forgotten.

**Research work** — rank by:
1. **Strategic and Gate Alignment** — does this advance a currently documented project or roadmap gate?
2. **Imminent Deadlines / Overdue** — tasks flagged by the scanner due today or in the next 1–7 days.
3. **Momentum** — was this touched in the last session? Warm context = lower startup cost.
4. **Size** — short tasks (< 30 min) are worth surfacing even if lower priority, because they can fill gaps between longer work.

**Deferred items** — things that belong in a separate focused session. For each, provide a copy-paste initialization prompt (see Section 4).

---

## 3. Output Format

```
## Personal (do these yourself)
- [item]

## Research — This Session
Ranked list with one-line rationale and estimated time:
1. **[Task]** — [why now] | ~[time]
   An agent can: [specific actions]

## Deferred — Start a New Chat
- **[Task]**: [copy-paste prompt below]
```

Keep the output tight — a scan in under 30 seconds. No bullet-point dumps of everything from the handoff.

---

## 4. Deferred Chat Prompts

For each deferred task, provide a harness-neutral prompt the user can paste into a new agent session. Format:

```
> Paste into new agent session:
Use the `[relevant-skill]` skill.
[1–2 sentence task description including relevant file paths or citekeys]
```

Example:
```
> Paste into new agent session:
Use the `theory` skill.
Backfill evidence table claims for the Construct A and Construct B concept notes. Standard is 3–5 sentences with detailed methods and empirical grounding. Files: wiki/constructs/Construct A.md, wiki/constructs/Construct B.md
```

---

## 5. Boundaries

- Do not surface tasks that are already done (check if recent handoffs mark them complete).
- Do not recommend vault-wide audits as "quick tasks" — they are long tasks and should be deferred with a prompt.
- Personal obligations go first in the output but should not be ranked against research items — they are categorically different.
- If today's daily note is empty or missing, say so and synthesize only from the handoff and yesterday's note.
- Prefer recommending 2–3 focused items over a comprehensive list. Depth > breadth.

## 6. Verification

- No surfaced item is already marked complete in a recent handoff.
- Each deferred item has a paste-ready prompt.
- A missing or empty daily note is stated in the output.

---

## Resources

- Latest handoff: `operations/handoffs/` (always most recent)
- Today/yesterday daily notes: `inbox/daily-notes/`
- Active project trackers: `projects/`
