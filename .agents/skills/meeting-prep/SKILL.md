---
name: meeting-prep
description: "Create a grounded one-on-one or lab-group meeting prep note in the vault inbox. Use when the user asks to prepare for a meeting; use meeting-prep-auto only for the scheduled unattended routine."
---

# Meeting Prep

Produce a filled prep note for an upcoming meeting in `inbox/meetings/`, linked from the meeting-day daily note when that note exists. The user may provide a lot of context or just a sentence. Handle both.

---

## 1. Detect Meeting Type

From the user's description, determine:

- **1-on-1** — advisor check-in, collaborator meeting, mentor conversation, any two-person or small focused meeting
- **Lab group** — lab meeting, group presentation, team update, multi-person group session

If ambiguous, ask: "Is this a 1-on-1 or a group/lab meeting?"

---

## 2. Gather Context

**People resolution (required):** Read your people dictionary (for example `areas/People Dictionary.md`) when resolving the meeting person or attendees. Use the canonical name and aliases; if the person is missing or marked TBD and identity matters for the prep note, ask the researcher for a one-liner — do not invent surnames.

Extract from the user's message (ask only for what's missing):

**For 1-on-1:**
- Who is the meeting with? (advisor name, collaborator, etc.)
- Date (derive the current local date when unspecified)
- What are the 2–4 things they need to cover? (priorities, updates, decisions, open questions)
- Current project status in one sentence (if research-related)
- Any blocker or decision point?

**For lab group:**
- Project or team name
- Date
- Their 2–3 updates to share
- Any major decision or blocker needing alignment
- Who else is presenting / team members (if known)
- Deliverable deadlines (if known)

Do not ask for every field. Infer what you can. Ask one follow-up if critical context is missing, not multiple questions.

---

## 3. Fill the Template

Templates live at:
- `operations/templates/Meeting Prep - 1-on-1.md`
- `operations/templates/Meeting Prep - Lab Group.md`

Read the appropriate template, then fill every `[PLACEHOLDER]` field with real content from the user's description. Follow these rules:

- **THINGS TO COVER / PRE-MEETING PREP:** Convert the user's priorities into concrete, action-oriented bullet points (do NOT use checkboxes `- [ ]` as they pollute the Tasks dashboard). Each item should be specific enough to act on — not "discuss Project B" but "get feedback on the analysis plan for Project B Experiment 1."
- **BACKGROUND / CONTEXT:** Write tight, factual prose. One sentence per field. Don't pad.
- **AGENDA + KEY TALKING POINTS (lab):** Frame talking points as the user would actually say them in the meeting — direct, confident, concise. Each point should have a "why it matters" that serves as the framing sentence for that topic.
- **POST-MEETING NOTES / TO-DOS:** Leave these blank or with one placeholder — these are filled after the meeting.
- Replace `[DATE]` with the actual date (format: YYYY-MM-DD).
- Replace `[ADVISOR/PERSON]` or `[PROJECT/TEAM NAME]` with the real name.
- Do not include the template frontmatter `---` block in the output file.

---

## 4. Save the Prep Note

Write the filled note to:

```
inbox/meetings/YYYY-MM-DD [Name or Topic] Meeting Prep.md
```

Example: `inbox/meetings/YYYY-MM-DD Advisor Meeting Prep.md`.

Frontmatter for the saved note:
```yaml
---
tags: [type/meeting-prep, area/meetings]
type: meeting-prep
date: YYYY-MM-DD
daily_note_date: YYYY-MM-DD
daily_note_surface: pending
daily_note_surface_at:
person: [name if 1-on-1, else omit]
format: [one-on-one or lab-group]
outcome_captured: pending
---
```

`outcome_captured: pending` marks this note as eligible for your meeting-sync routine to append the post-meeting outcome summary into this same file (see your meeting-sync routine's merge-or-create step) rather than creating a separate outcome note. Keep the template's `## Meeting Outcome` section and its `<!-- meeting-outcome: pending -->` anchor intact when filling the note — do not remove or fill that section yourself; it is your meeting-sync routine's write surface, not yours.

### Surface the prep note in the meeting-day daily note

Every prep note must include the `daily_note_date`, `daily_note_surface` (`pending` or `done`), and `daily_note_surface_at` fields shown in the frontmatter above.

After saving, check whether the target daily note exists at `inbox/daily notes/YYYY-MM-DD.md`:

- If it exists, append a forward wikilink under its `## Meetings` section, set `daily_note_surface: done`, and set `daily_note_surface_at: YYYY-MM-DD HH:MM`.
- If it does not exist, set `daily_note_surface: pending` and do not create or edit any daily note. Your daily-note routine will surface the link when the daily note exists.

```
- [[YYYY-MM-DD [Name or Topic] Meeting Prep]] — [one-on-one prep | lab-group prep]
```

- If the `## Meetings` section does not exist, create it before the final `### Voice Notes` heading (it is present in the standard template directly above the project sections).
- This is the **only** edit allowed to a daily note by this skill — a single wikilink line. Do not modify any other daily-note content.

---

## 5. Output to User

After saving, respond with:

1. A clickable link to the saved file: `[YYYY-MM-DD Name Meeting Prep](inbox/meetings/...)`
2. A brief (3–5 bullet) summary of the key talking points — scannable, no fluff
3. One sentence flagging anything that seems underspecified or worth thinking through before the meeting

Do not reproduce the full template in chat. The file is the deliverable; chat output is the digest.

---

## 6. Boundaries

- The only daily-note write allowed is a single forward wikilink under the target daily note's `## Meetings` section (see "Surface the prep note in the meeting-day daily note"). Never touch any other daily-note content.
- If the target daily note does not exist, leave the prep note marked `daily_note_surface: pending`; do not create a daily note and do not append the link to an older daily note.
- Save to `inbox/meetings/` only — not `inbox/messages/` (that's for email/messages).
- If the user gives very little context, make reasonable research-PhD-appropriate inferences and fill what you can — then flag what you assumed.
- Post-meeting fields (notes, to-dos) stay blank or minimally placeholder. Don't invent outcomes.

---

## 7. Verification

- The note is saved as `inbox/meetings/YYYY-MM-DD [Name or Topic] Meeting Prep.md` with the frontmatter from § 4.
- No `[PLACEHOLDER]` remains outside the post-meeting fields, and the `## Meeting Outcome` section and its anchor are intact.
- `daily_note_surface` matches what happened: `done` with one wikilink under `## Meetings`, or `pending` with no daily-note edit.
- Assumptions made from thin context are flagged in the chat summary.
