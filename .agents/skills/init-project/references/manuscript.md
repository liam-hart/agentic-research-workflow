# Manuscript archetype procedure

`init_project.py --archetype manuscript` copies the payload from `operations/templates/manuscript_pipeline/` (declared in `archetypes/manuscript/archetype.toml`). The steps below cover what the engine cannot decide or verify. The templates are covered end to end by `tests/sandbox_manuscript/run_tests.sh`; run it before and after changing anything under `manuscript_pipeline/`.

## Pre-flight (ask before scaffolding)

1. Target directory: is it an existing git repo, or does it need `git init`?
2. Zotero library (user or group) and citation style. Default: APA 7, `biblatex-apa`. If a citekey exists in more than one library, the export needs `ZOTERO_FLAGS="--zotero-library <groupID>"`.
3. LaTeX engine. Default: `xelatex` via `latexmk`.
4. Structure: single file, or multi-file with `sections/` includes.

## After the engine runs

1. Fill in `main.tex`:
   - `\title{}`, `\shorttitle{}`, `\author{}`, `\affiliation{}`, `\authornote{}`
   - the section outline
   - the class option: `man` for a double-spaced manuscript, `jou` for a typeset journal look
2. Keep `apa7_config.tex` unless the target system needs other fonts. It falls back from Times New Roman to TeX Gyre Termes.
3. Replace the starter `references.bib` with a Better BibTeX export of the project's Zotero collection, with pinned citation keys.
4. `make reference-doc` generates `apa7_reference.docx`.
5. `manuscript_review_state.json` ships in the `canonical_tex` state. `CONVERSION_LOG.md` is created by the reconcile script on first use.

## Verification

1. `make check`: all active citation-audit tiers pass.
2. `make bib-check`: no duplicate keys, and no entries missing title, author, or journal (biblatex `journaltitle` and `date` count).
3. `make pdf`: clean compile.
4. `make docx`: a valid DOCX whose citations are **linked** to the Zotero library (the export says `linked N items`). It aborts if a citation cannot become a field, a key does not resolve to one library item, or Pandoc drops content.
5. `make roundtrip`: the DOCX Zotero fields match the `.tex` position by position.
6. `make retention`: every number the PDF shows is in the DOCX (`retention_report.md`).

`make preflight` lists missing dependencies: Python 3.10+, Pandoc 3.x, TeX Live/MacTeX with `latexmk`, `biber`, `apa7.cls`, `biblatex-apa`, Poppler (`pdftotext`, `pdftoppm`), and `python-docx`.

## Review lifecycle

Once scaffolded, the `sync-docs` skill owns the advisor review round:
`canonical_tex` → `make review-open` → `word_review_open` → advisor edits → `make review-reconcile` → place skipped edits → `make review-close` → `canonical_tex`.

## Migration gate (retrofit)

Read the existing manuscript's `AGENTS.md`, review-state file, latest handoff, and canonical-source declaration. The engine refuses `--apply` while a review round is open. After the round closes:
1. Scaffold alongside the current source.
2. Do a one-time conversion.
3. Compare the rendered and extracted outputs.
4. Decommission the old canonical path only with explicit project authority, using the destination repo's archive convention.
