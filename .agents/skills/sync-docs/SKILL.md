---
name: sync-docs
description: "Manage the two-way lifecycle between canonical LaTeX source and advisor or collaborator Word reviews with live Zotero citation fields. Use when opening, diffing, reconciling, or closing an existing Word review round; use init-project (manuscript archetype) to scaffold the repository first."
---

# Sync Docs

Run a Word review round on a LaTeX-canonical manuscript: export a DOCX the
advisor can edit, then bring their tracked changes back into the `.tex`
without losing or misplacing any of them. The scripts and their design live in
`operations/templates/manuscript_pipeline/README.md` (your own template; it
does not ship with this kit); this skill is the procedure.

## State machine

`manuscript_review_state.json` (beside the main `.tex`) holds `canonical_tex`
(sources editable) or `word_review_open` (sources frozen; `make pdf` refuses).
A project without the file is not using the state machine: nothing is gated,
and reconcile warns that double application and stale sources go undetected.

```
canonical_tex ──make review-open──▶ word_review_open ──make review-close──▶ canonical_tex
                                     (reconcile happens here)
```

## Procedure

1. **Open.** `make review-open REVIEWER="Name"`
   - Checks the state first, so a second open can never overwrite the DOCX
     already sent.
   - Runs the citation audit, builds the PDF, exports the DOCX, verifies every
     citation position by position (`roundtrip`) and every number against the
     PDF (`retention`). Any failure stops the round.
   - Fingerprints and snapshots every source file the manuscript `\input`s,
     and records the sent DOCX and the retention verdict.
   - Tell the reviewer to keep **Track Changes on**: edits made with it off are
     reported, never applied.
2. **Look.** `make review-diff REVIEW_DOCX="returned.docx"` writes
   `review_diff_report.md`: edits (adjacent revisions merged), moves,
   formatting and paragraph-structure changes, and comments with replies.
3. **Reconcile.** `make review-reconcile REVIEW_DOCX="returned.docx"` applies
   every edit it can place exactly and writes `review_reconcile_report.md` plus
   a `CONVERSION_LOG.md` entry. Then review the result with
   `git diff --word-diff` and revert what you disagree with.
   - `RECONCILE_FLAGS=--interactive` confirms each edit; `--dry-run` writes
     nothing; `--redo` restores the frozen sources and reconciles again (the
     sources it replaces are backed up into the round snapshot first).
   - Inserted Zotero citations become `\autocite{key}`. If the reviewer cited
     something not in the `.bib`, reconcile names the keys: re-export the
     `.bib` from Zotero before building.
4. **Place what was skipped.** Work through the report's *Skipped* and
   *Unhandled* sections and the *Text changed outside Track Changes* section.
   Each entry carries the Word context and, where located, `file:line`. A
   skipped edit is the reviewer's intent not yet applied — never a no-op.
   Comments are listed with their source location.
5. **Close.** `make review-close` rebuilds the PDF and re-runs the audit while
   the round is still open, then closes it. If the build fails, fix the source
   (or `make review-reconcile … RECONCILE_FLAGS=--redo`) and close again. A
   round with nothing to apply closes with `CLOSE_FLAGS=--no-changes`.
6. **Commit** the reconciled sources, `CONVERSION_LOG.md`, and the state file
   with a message naming the review round.

## When a gate fails

- **Round trip** mismatch: a citation changed between `.tex` and DOCX. Fix the
  source; never hand-edit the DOCX.
- **Retention** deficit: the report shows each missing number with its PDF
  context. Usually a LaTeX construct Pandoc cannot read — simplify it, or
  extend `word_path_normalize.py` in the template. If the gate is wrong about a
  specific token (layout, not content), excuse exactly that token:
  `RETENTION_FLAGS="--allow-tokens 22 34"`. The override is recorded in the
  round state; never excuse a token you have not looked at in the PDF.
- **Zotero linking**: a citekey missing from the library, or present in more
  than one library, fails the export. Fix the key, or choose the library with
  `ZOTERO_FLAGS="--zotero-library <groupID>"`. `--unlinked` exports frozen
  citations and should be a conscious choice.

## Safety rules

1. Never edit the sources while a round is open. Reconcile refuses sources
   that changed since `open`.
2. Never reconcile twice without `--redo` — it would apply every edit twice.
   Reconcile refuses.
3. Review the applied edits (`git diff --word-diff`) before closing. Advisor
   edits can change scientific claims.
4. Treat every *Skipped*, *Unhandled*, and *outside Track Changes* entry as
   open work.
5. Commit after closing; the close does not auto-commit.

## Dependencies

Same as the `init-project` manuscript archetype
(`.agents/skills/init-project/references/manuscript.md`): Python 3.10+, Pandoc
3.x, TeX Live/MacTeX, Poppler, optionally `python-docx` and Zotero 7 with
Better BibTeX.

## Interaction with other skills

- **`init-project`** (`--archetype manuscript`) sets up the project that
  `sync-docs` operates on.
- **`academic-writing`** governs prose in the `.tex` files.
- **`feedback-reconcile`** routes the *substance* of advisor feedback into task
  tracking; `sync-docs` handles the mechanical round trip.
- **`hierarchical-draft`** may drive major revisions between rounds, only in
  `canonical_tex`.
- **`zotero-manager`** maintains the Zotero library and `.bib` exports.
