---
name: calendar-schedule
description: "Extract, validate, and conflict-check calendar events and, when authorized, write them to macOS Calendar.app. Use when the user asks to extract, conflict-check, add, modify, or delete calendar events; requires explicit event-level authority for live Calendar.app writes."
---

# Calendar Scheduling

Extract, validate, conflict-check, and (when authorized) write events into macOS Calendar.app while keeping Calendar Context truthful. This skill is scoped to the vault that holds the calendar scripts.

## Workflow

1. Extract exact title, start/end (`YYYY-MM-DD HH:MM`), location, notes, and target calendar. Route institutional commitments to your default calendar; use a named Google or iCloud calendar only when the source and the researcher's instruction establish it.
2. Inspect Calendar Context and run the merged-calendar check by default:

   ```bash
   python3 operations/scripts/calendar_manager.py check-conflicts \
     --start "YYYY-MM-DD HH:MM" --end "YYYY-MM-DD HH:MM" --json
   ```

   Each result includes its calendar and either `overlap` or `tight_transition`. Surface both. For example, an event ending at one building at 10:45 AM before an 11:00 AM event across town is a tight-transition warning even when it is not a strict temporal overlap. Use `--calendar "Calendar"` only to deliberately narrow review.
3. Present a verification table listing every proposed event, target calendar, location, conflicts, duplicates, and commute/tight-transition risks. Obtain confirmation before every live write unless the researcher's current instruction explicitly lists and authorizes those exact events. A single event is not automatic authority.
4. After confirmation, use an explicit target calendar and `--sync`:

   ```bash
   python3 operations/scripts/calendar_manager.py add \
     --calendar "Calendar" --title "<Title>" \
     --start "YYYY-MM-DD HH:MM" --end "YYYY-MM-DD HH:MM" \
     --location "<Location>" --notes "<Notes>" --sync --json
   ```

   For batches, validate the complete JSON payload before writing:

   ```bash
   python3 operations/scripts/calendar_manager.py add-batch \
     --input events.json --calendar "Calendar" --sync --json
   ```

   A non-zero sync failure means the event already exists but the mirror was not confirmed refreshed; the command reports the affected event UIDs and exits non-zero. Record them and do not claim synchronization. Every write command, including `delete`, accepts `--dry-run` for a no-write preview.
5. For delete or modification, resolve and show the exact target and obtain explicit confirmation every time. Delete requires an explicit single-calendar `--calendar` or `--all-calendars` scope; calendar-scoped deletion is the default:

   ```bash
   python3 operations/scripts/calendar_manager.py delete \
     --uid "<UID>" --calendar "Calendar" --sync --json
   ```

   `--all-calendars` is conspicuous and never implicit. If it finds more than one UID match it fails closed unless `--confirm-multiple` is supplied after reviewing the targets. Batch runtime failures report created UIDs and calendar-scoped rollback outcomes; preserve that report in the handoff.

## Boundaries

- Calendar writes, deletes, and changes are live external operations. Never act without the authority stated above.
- Never hand-edit your generated calendar-context note; it is an atomic generated mirror.

## Resources

- Run `operations/scripts/calendar_manager.py` (your own script; it does not ship with this kit) for every conflict check and live write; the commands are in Workflow.
- Read Calendar Context before the conflict check in step 2.
- Read `operations/scripts/calendar-mirror.py` (your own script; it does not ship with this kit), which generates that mirror, when a refresh fails.
- Read Calendar Integration when the calendar setup itself is in question.

## Verification

- Confirm the all-calendar conflict report includes overlaps and tight transitions.
- Confirm a live write returns a valid UID and reports a successful mirror refresh before calling the context synchronized.
