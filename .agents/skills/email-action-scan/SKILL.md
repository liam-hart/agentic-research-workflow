---
name: email-action-scan
description: "Scheduled-only, unattended local scan of a work mailbox via Apple Mail for genuine action items and privacy-safe task routing. Use when the authorized email-action-scan routine launches on this Mac; do not invoke interactively or from cloud sessions."
---

# Email Action Scan — scheduled routine

Reads work-mailbox metadata plus the extractor's bounded plain-text body excerpt via `operations/scripts/email-action-scan-extract.py`, then applies judgment to surface genuine action items. The excerpt exists only in untracked scratch output and may inform classification and a short paraphrase. Body text must never enter tracked state, tasks, reports, handoffs, or logs. Setup and privacy authority: your email-integration note (for example `docs/Email Integration.md`).

**This is a local routine, not a cloud routine.** AppleScript/Mail.app access only works on the local Mac — do not attempt to invoke this from a cloud session; it will fail.

---

## 1. Run Stage A

```bash
python3 operations/scripts/email-action-scan-extract.py
```

This reads the tracked state file (`operations/state/email-action-scan-state.json`) read-only to skip already-seen message ids, scans the in-scope mailboxes (all except the technical/noise folders — junk, deleted, sent, drafts, outbox, RSS, conversation history, archive, conflicts, sync/local/server failures, tasks, notes), and writes new-message metadata to an **untracked** scratch file under `operations/state/.email-scan-cache/`. If Stage A exits non-zero or reports 0 new messages, stop here — do not write anything, do not touch the state file.

## 2. Filter — conservative by default (no user to ask)

For each message, use sender, subject, mailbox, and the bounded scratch-only body excerpt to decide whether it contains a genuine request, deadline, reply obligation, or decision for the researcher. Never reproduce body sentences in tracked output.

- **Flag as action item** — subject/context makes clear this needs a reply, a decision, or contains an explicit deadline or request directed at the researcher (e.g. "Can you...", "Please send...", "RSVP by...", a form/deadline notification, a direct question from an advisor or collaborator).
- **Skip, do not flag** — FYI/announcement/listserv content, newsletters, automated notifications with no ask (calendar invites already covered by `calendar-mirror`, shared-document notifications with no accompanying request, receipts, "FW:" forwards with no visible ask in the subject itself).
- **Genuinely ambiguous** after the bounded excerpt is considered — default to **skip**, not flag. Record only a short non-quoting disposition.

Log every message from the scratch file in the per-run report (step 5) with its disposition — flagged, skipped, or ambiguous-skipped — so the decision is visible even though most won't route anywhere.

## 3. Route flagged items

For each flagged item, apply your vault's task-routing contract. Do not depend on a harness-specific command file:

- Determine the best-matching project or area file. Use the mailbox name as a strong hint (for example a mailbox named for a project routes to that project's files, `Funding` to a funding area, `Classes` to teaching, `Journal` to the relevant manuscript project) but confirm against the sender and subject rather than trusting the mailbox alone.
- If no confident destination exists, fall back to the "Needs Triage" section of a standalone task board (for example `inbox/Task Boards/Standalone & Triage.md`).
- Append with a date-stamp and a short synthesized one-line gist — **never quote the subject verbatim into the vault beyond what's needed to identify the item**; paraphrase the ask. This keeps the routine aligned with the vault's no-raw-text constraint even though subject lines aren't bulk text.
- When resolving a sender's name, consult your people dictionary (for example `areas/People Dictionary.md`) and prefer canonical forms; if the sender is unrecognized, use their name/affiliation as it appears in the email — do not invent a surname or role (the same rule `meeting-prep-auto` follows).
- **Tasks-plugin metadata — never guess.** Emit a due date (📅 YYYY-MM-DD) only from an explicit calendar date, or from a relative date ("by Friday", "next week") resolved against the email's sent date. Never set priority (🔺⏫🔼🔽⏬) from urgency words such as "URGENT". Always append `#needs-triage`.

## 4. Update the tracked state file

Append an entry per scratch-file message (flagged, skipped, and ambiguous-skipped alike — every message Stage A surfaced) to `operations/state/email-action-scan-state.json`:

```json
{
  "items": {
    "<message_id>": {
      "disposition": "routed | skipped | needs_triage",
      "first_seen": "<ISO timestamp>",
      "routed_to": "<path or null>",
      "mailbox": "<mailbox name>"
    }
  }
}
```

**Never store subject or sender text here** — this file is tracked in git. Message id is opaque and non-sensitive; that's the point of using it as the sole dedup key. Only write this file after routing succeeds — if the run fails partway, leave the state file untouched so the next run re-surfaces the same messages from Stage A rather than silently losing them (same "truth lives in the destination, not the log" principle as `meeting-prep-auto`'s glob-first dedup).

## 5. Write the per-run report

`operations/reports/email-action-scan/YYYY-MM-DD-HHMM.md` — this is the one place a short subject/sender reference is allowed, for human audit only, never copied further:

```markdown
# Email Action Scan — YYYY-MM-DD HH:MM

**Scanned:** N messages · **Flagged:** N · **Skipped:** N · **Ambiguous (skipped):** N

## Routed
- [Mailbox] "Short paraphrase of the ask" — from Sender → routed to `path/to/file.md`

## Needs triage
- [Mailbox] "Short paraphrase" — from Sender → routed to `path/to/file.md` (#needs-triage, no researcher-stated priority)

## Skipped / ambiguous (not routed)
- [Mailbox] Subject line — reason
```

## 6. Surface in the daily note — exactly one line

Re-read today's daily note (`inbox/daily notes/YYYY-MM-DD.md`) immediately before writing, per the vault's voice-note-preservation rule — never write from a stale snapshot. If nothing was routed this run, do not touch the daily note at all.

If at least one item was routed: append a single forward wikilink under a `## Email Action Items` section (create it after `## Meetings` if present, otherwise before `### Voice Notes`, if the section doesn't already exist today) pointing to this run's report:

```markdown
## Email Action Items
- [[operations/reports/email-action-scan/YYYY-MM-DD-HHMM|N email action item(s) routed]]
```

Do not duplicate a link if one from an earlier run today already points to a report — append a new line only if this run produced a new report. Exactly one line per run; never touch `### Processed`, `<!-- briefs -->`, `## Meetings`, or `### Voice Notes`.

## 7. Boundaries

- Never ask the user a question — this is unattended. Default to skipping ambiguous items (see step 2), not flagging them.
- No subagents. One fresh session per scheduled fire.
- Read body excerpts only from Stage A's bounded untracked scratch file. Never copy or retain body text in tracked state, tasks, reports, handoffs, or logs.
- Never store subject/sender text in the tracked state file — only in the per-run report.
- Exactly one daily-note edit per run: the single `## Email Action Items` forward-link, and only when something was actually routed.
- Read-only against Mail.app — this routine (and Stage A) must never send, move, delete, or mark-read any message.

## 8. Verification

- Every message in the scratch file appears in the per-run report with a disposition.
- The tracked state file holds one entry per scratch-file message and no subject, sender, or body text.
- Each routed task carries `#needs-triage`, no priority emoji, and a due date only where the email states one.
- The daily note gained at most one line, and only when something was routed.
- If Stage A failed or found nothing, the run wrote nothing and the state file is untouched.
