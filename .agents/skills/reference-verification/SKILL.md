---
name: reference-verification
description: Audit a specified manuscript bibliography, BibTeX file, reference list, or Zotero export against authoritative bibliographic records and return field-level proposed corrections. Use when performing submission-stage reference metadata verification; use zotero-manager for library maintenance and academic-writing for claim-to-source suitability.
---

# Reference Verification

Produce a report-only audit of bibliographic identity and metadata. Do not mutate Zotero, BibTeX, Word fields, LaTeX, or manuscript references during the audit.

## Establish the target

Identify the canonical artifact, its review state, citation style, and the exact entries in scope. Record a content hash or other stable snapshot identifier so findings remain tied to what was inspected. An open Word-review round permits read-only auditing but blocks repairs to canonical source, Word fields, and Zotero.

This skill checks bibliographic metadata. It does not establish whether a cited source supports a manuscript claim; `academic-writing` and the local evidence workflow own that judgment.

## Authority order

Use the narrowest appropriate authoritative record:

1. DOI resolution plus the publisher or official proceedings record;
2. a discipline-specific authoritative index when applicable, such as PubMed or IEEE Xplore;
3. Crossref for DOI-target and metadata corroboration;
4. the local Zotero record for identity reconciliation, not as publication truth;
5. named web search only when authoritative routes are insufficient.

The final issue record can legitimately differ from online-first metadata. A DOI-embedded year is not automatically the publication year. When authorities conflict, report the conflict and do not merge values by intuition.

## Field audit

Compare each entry field by field: citekey or item key, author membership and order, title identity, publication type, journal or proceedings, year/status, volume, issue, pages or article number, and DOI.

For batch work or ambiguous fields, read [field-classification.md](references/field-classification.md). Absence from Crossref is not an error. Internal reports, theses, manuals, older records, and inaccessible sources may remain unverified.

## Outcomes

Use bibliographic outcomes that cannot be confused with scientific evidence certification:

- `confirmed against stated authority`;
- `proposed correction`;
- `needs human decision`;
- `conflict among authorities`;
- `not verified`.

Never label a reference or claim simply `verified`.

## Report

Return summary counts and a compact table:

| Key | Field | Artifact value | Authority value | Authority and stable identifier | Outcome | Proposed correction or question |
|---|---|---|---|---|---|---|

Preserve capitalization, abbreviation, and citation-style differences as non-substantive unless they alter identity or violate the target's established style. Any disagreement in a final citation field deserves classification; do not use a universal page-count or author-count threshold.

## Boundaries and handoff

- No automatic patches, Zotero update calls, direct database edits, credential-requiring writes, or citation-style normalization.
- A proposed correction is not repair authority. The researcher approves a separate bounded repair pass through the owning manuscript or Zotero workflow.
- Record unavailable sources and uncertainty. Do not turn failed lookup into evidence of error.
- Report the target snapshot, sources consulted, conflicts, proposed corrections, and files left byte-identical.
