---
name: meeting-prep-auto
description: "Scheduled-only, unattended meeting preparation from current calendar and vault context with mandatory deduplication. Use when the authorized meeting-prep-auto routine launches; never ask questions or replace manual meeting-prep."
---

# Meeting Prep Auto — scheduled routine

This is the unattended counterpart to `meeting-prep`. Obtain cadence, trigger, execution platform, and look-ahead window only from `operations/routines-reference.md`; this skill carries no schedule authority and must never block waiting on user input.

---

## 1. Orient

- Read today's date section of `areas/Calendar Context.md`. If today has no section or no events, exit immediately — this should be the common case and should cost almost nothing.
- Read today's daily note (`inbox/daily notes/YYYY-MM-DD.md`) for its `## Meetings` section and any prose context (e.g., "For meeting with X: ...") the user may have already written for specific meetings — reuse this the same way the manual skill does.
- When resolving person or attendee names from calendar titles, consult your people dictionary and prefer canonical forms/aliases. If a name is absent, keep the calendar string as-is and do not invent a surname (unattended — no user Q&A).

## 2. Determine which events need prep — dedup is mandatory and file-glob is the authority

For each run, use the look-ahead window documented in `operations/routines-reference.md` and process calendar entries in that window:

1. `Glob "inbox/meetings/YYYY-MM-DD*"` (today's date) and check whether an existing filename already corresponds to this event (matching person name or event title, case-insensitively, allowing for the same normalization the manual skill uses — e.g., "Weekly Project Meeting" → "Project Meeting Prep"). **This glob check is the dedup authority.** If a matching file exists, skip this event — do not regenerate or duplicate it, and do not touch the file.
2. Only after the glob check passes (no existing file), optionally cross-check `operations/state/meeting-prep-auto-state.json` — this is a secondary/audit record, never the sole reason to skip or proceed.
3. **Relevance filter:** For each event surviving the dedup check, decide `needs_prep: yes/no` before generating anything:
   - **Skip** — personal errands/appointments (tailor, dry cleaning, haircut, dentist/doctor, DMV, personal shopping), purely social/community events with no research agenda (socials, mixers, parties, happy hours), and calendar entries that aren't actually meetings (imperative-phrased reminders like "Reach out to X re: Y" with no attendee/call format — these are tasks that leaked into the calendar mirror, not events to prep for).
   - **Prep** — 1-on-1s with advisors/collaborators/lab members, lab-group meetings, journal clubs, presentations, and admin/funding/logistics meetings with clear work content (e.g. a conference-reimbursement help session still qualifies — substantive even though not research).
   - **Ambiguous** (bare title, no description or location context, e.g. a first-name-only entry at a coffee shop) → default to **prep**. Same conservative-inference principle as the rest of this skill: unattended runs can't ask, so the safer default is over-prepping a possible work contact, not under-prepping one.
   - Log every **skip** to `operations/state/meeting-prep-auto-state.json` with a one-line reason (`{date, event_title, skipped: true, reason}`) so the decision is visible and reversible — never silently drop an event with no record.

**Note on git freshness:** This routine does not pull or rebase against the remote immediately before the dedup check. A stale remote cannot be fixed by pulling from it, and a pull would only help if a push landed mid-run, which a clone-per-run model makes unlikely. Adding a pull step would risk false confidence that the gap is closed. The required fix is an explicitly authorized deployment policy that publishes relevant committed state from interactive sessions to the remote before the routine's dedup check relies on it; this is not an unconditional interactive-agent push requirement.

If nothing needs prep after this check, exit — do not write anything, do not touch the state file.

## 3. Classify and gather context (no user interaction)

For each event needing prep:

- **Classify 1-on-1 vs. lab-group** by heuristic, since there's no user to ask: a title with a single other name or an "X / researcher" pattern → 1-on-1; a title suggesting a group/team/lab/journal-club session → lab-group. Default to 1-on-1 if genuinely ambiguous — it's the more common case in this calendar and the lighter template.
- Pull context the same way the manual skill's step 2 would, but from files only, never from asking:
  - Today's and yesterday's daily notes (prose already written about this meeting, if any — reuse verbatim where the user has clearly pre-written meeting context, same as the manual skill does)
  - The relevant project's task authority, matched by person/topic keyword (for example `projects/<project>/Tasks.md` and `projects/<project>/Decision Log.md`; if a project has no task file, never invent one)
  - `inbox/messages/` — glob for filenames matching the attendee(s)' canonical name/alias (per People Dictionary) or the meeting's topic keyword, within the last 30 days. Read each match's frontmatter `status:` field before treating its content as fact: `sent` means it reached the recipient, `draft` means it has not — never describe draft-status content as "sent" or as something recipients have seen/acted on. This is the vault's canonical outgoing-correspondence log and is frequently the *only* real source of what a lab-group meeting's substantive agenda actually is. Do not skip it in favor of the thinner daily-note/Action-Items sources.
- **Source-trace every claim.** Every specific, non-generic factual statement written into the note (a date, a named deliverable, "email sent," a task assignment, a numeric detail) must trace back to something actually read in this step — a daily note line, a task-authority entry, or a message file. If you cannot point to the source line for a claim, do not write the claim.
- If no usable context is found for a field after checking all three sources above, leave it visibly minimal — a generic placeholder bullet such as "No prior written context found for this meeting — confirm live: [topic implied by calendar title]" — rather than inventing plausible-sounding specifics (dates, sent/received status, deliverable names). This is expected to be lower-quality than interactive runs — that's what the review flag is for; a vague-but-honest bullet is strictly preferable to a fabricated-but-specific one.

When no source supports a detail, the routine must remain minimal rather than infer a plausible date, deliverable, or message status.

## 4. Fill and save the note

Same template rules as `meeting-prep` steps 3–4 (read `operations/templates/Meeting Prep - 1-on-1.md` or `Meeting Prep - Lab Group.md`; same filename convention `inbox/meetings/YYYY-MM-DD [Name or Topic] Meeting Prep.md`; same bullet-not-checkbox rule).

Frontmatter — same as `meeting-prep`, plus two additional fields required only on auto-generated notes:

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
auto_generated: true
reviewed: false
---
```

`reviewed: false` is a **manual-only** flag. Nothing in this routine or elsewhere ever sets it to `true` automatically — there is no detection of the user opening or reading the note. It exists purely so the user (or a future interactive session) can flip it once they've actually looked at the note. Do not build or claim any auto-flip behavior for this field.

`outcome_captured: pending` marks this note as eligible for your meeting-sync routine to append the post-meeting outcome summary into this same file rather than creating a separate outcome note (see your meeting-sync routine's merge-or-create step). Keep the template's `## Meeting Outcome` section and its `<!-- meeting-outcome: pending -->` anchor intact — that section is your meeting-sync routine's write surface, not this routine's.

## 5. Surface in the daily note

Identical mechanism to `meeting-prep` step 4's "Surface the prep note in the meeting-day daily note": append a single forward wikilink under today's `## Meetings` section (creating the section before `### Voice Notes` if missing — it is present in the standard template directly above the project sections), set `daily_note_surface: done` and `daily_note_surface_at`. This is the same daily-note edit boundary as the manual skill — exactly one wikilink line per note, nothing else. Do not duplicate a link that's already present (check before appending).

## 6. Update the state file

After processing, append `{date, event_title, prep_file_path, processed_at}` entries to `operations/state/meeting-prep-auto-state.json` for everything just generated, plus `{date, event_title, skipped: true, reason, processed_at}` entries for everything the step 2 relevance filter skipped. Secondary record only — the glob check in step 2 remains the real dedup mechanism on every run.

## 7. Boundaries

- Never ask the user a question. If something is genuinely ambiguous, make the most conservative reasonable inference and let `reviewed: false` carry the "sanity-check this" signal — do not block.
- Exactly one daily-note edit per prep note: the single wikilink. Never touch any other daily-note content, including sections owned by other routines (`### Processed`, `<!-- briefs -->`, Voice Notes).
- Do not regenerate or overwrite an existing prep note for the same event, ever — the glob dedup check in step 2 is mandatory before any write.
- No subagents. One fresh session per scheduled fire. Target near-zero token cost on no-op polls (the common case).
- Apply the relevance filter in step 2; do not maintain a separate allowlist or denylist.

## 8. Verification

- No prep note existed for the event before this run (the step 2 glob check), and no existing note changed.
- Every specific claim in a new note traces to a line read in step 3.
- Each new note carries `auto_generated: true` and `reviewed: false`.
- Each new note added exactly one wikilink to the daily note, and nothing else there changed.
- The state file records every generated note and every skip with its reason.
- If nothing needed prep, no file changed.
