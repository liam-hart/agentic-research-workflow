---
name: when2meet
description: "Extract, analyze, or compare participant availability from a When2meet poll URL or event ID, find mutual meeting windows for teams or subsets of participants, and generate Obsidian availability notes. Use when the user shares a When2meet link, asks to check group or individual availability, or needs to schedule meetings based on a poll."
---

# When2meet Availability

Extract, parse, and analyze participant availability from When2meet polls into structured data, executive summaries, or Obsidian Markdown notes with canonical person wikilinks.

## Workflow

1. **Fetch & Parse Poll Data:**
   - Run `operations/scripts/extract_when2meet.py` with the poll URL or event ID:
     ```bash
     python3 operations/scripts/extract_when2meet.py "<URL_OR_ID>" --format summary
     ```
   - For machine-readable downstream tasks, use `--format json`.
   - For tabular exports, use `--format csv`.

2. **Query Subsets & Specific Attendees (Optional):**
   - When scheduling for specific people (e.g. 1-on-1s, sub-teams, domain leads):
     ```bash
     python3 operations/scripts/extract_when2meet.py "<URL_OR_ID>" --participants "Alex,Sam,Jordan" --format summary
     ```
   - The script resolves nicknames and first names (e.g. "Alex", "Sam", "Jordan") against your people dictionary (`areas/People Dictionary.md`). A participant counts as resolved only when the dictionary maps the name *and* the canonical stub note exists on disk, so the script never emits a dangling link. Markdown vault-note generation fails closed for unknown names; use `--allow-unresolved` only when plain-text names are intentional and review the printed diagnostic.

3. **Materialize in Vault Destinations:**
   - **Semester/Recurring Lab Availability:** Save to `areas/lab/Lab Availability - [Term].md`.
   - **Ad-hoc / Specific Meeting Polls:** Save to `inbox/meetings/YYYY-MM-DD When2meet - [Topic].md`.
   - Command to generate note:
     ```bash
     python3 operations/scripts/extract_when2meet.py "<URL_OR_ID>" --format markdown > "areas/lab/Lab Availability - [Term].md"
     ```

4. **Connect to Meeting Prep & Scheduling:**
   - Cross-reference optimal meeting windows with your lab meeting protocol note or use during `meeting-prep` workflows.

## Boundaries

- When2meet exposes unauthenticated public data embedded in client JavaScript. Never send private credentials or passwords through When2meet queries.
- Do not invent surnames or affiliations. The extractor resolves names only against your people dictionary; unknown names halt Markdown vault-note generation unless the explicit `--allow-unresolved` override emits them as plain text.

## Resources

- Script: `operations/scripts/extract_when2meet.py` (your own script; it does not ship with this kit)
- People authority: your people dictionary (`areas/People Dictionary.md`)
- Lab operations protocol: your lab meeting protocol note

## Verification

- Confirm script returns exit code 0 on target URL or ID.
- Check that active respondents and 0-slot respondents are correctly categorized.
- Confirm person links match canonical names in the people dictionary.
