---
name: vault-export
description: Export a lab-facing document from canonical vault Markdown to Word on an authorized OneDrive destination (export-clean-docx.py) or to Google Docs (export_gdoc.py), and pull a Google Doc back as Markdown for comparison. Use when the user explicitly authorizes the export in the current session; do not use for general document editing or unapproved external writes.
---

# Vault Export Skill

Controlled export of vault-side Markdown (hypothesis documents, SOPs, statements, standards) to the two external targets collaborators read: Word on OneDrive and Google Docs. The targets are equal. Choose by where the reader works: OneDrive Word for lab-canonical documents and anything with live reference-manager citations, Google Docs for collaborators who work there.

Both targets share one front end: your export script's Markdown cleaning and its hard gate. A source with raw Zotero citekeys, unresolved Obsidian wikilinks, or stray tags is refused by either exporter.

- The gate excludes fenced code blocks from tag/citekey/wikilink detection. If a false positive still occurs in prose, check whether the source genuinely contains a stray tag-like pattern and fix it there; never mutate code examples to work around the regex.
- Because fenced code is excluded from the gate, anything inside a fence reaches the export unchecked. Read fenced content before exporting.
- A refused citekey must be resolved to a proper APA citation by hand in the Markdown source. The scripts do not resolve authors automatically.

## Word on OneDrive

1. **Use your export script,** e.g. `operations/scripts/export-clean-docx.py <input_file.md> <output_file.docx>`.
2. **OneDrive destinations:** Take the destination from the project's own reference note, never from memory. Examples of the shape (replace with your project's paths):
    - **Project A:** `~/Library/CloudStorage/OneDrive-<org>/<shared-folder>/project-a/`
    - **Project B:** `~/Library/CloudStorage/OneDrive-<org>/<shared-folder>/project-b/`
3. **Export font:** Exports use a single declared font (the script's `EXPORT_FONT` constant) rather than the vault's internal display font. A `.docx` is editable, so the declared font must exist on the recipient's machine; otherwise Word substitutes silently while keeping the name, which mixes typefaces once a collaborator types and shifts page breaks between readers.
4. **Bookmarks:** Remove pandoc's per-heading bookmarks, which Word draws as grey brackets, and keep any that an internal link or field targets.

## Google Docs

A second script, e.g. `operations/scripts/export_gdoc.py`, drives Google's Workspace CLI, `gws`. Writes are dry runs until `--apply` is passed.

- **`create <source.md> --title T [--folder ID]`:** a new Doc in your Drive, in the same format as the Word export. The script builds the formatted `.docx` and Drive converts it, so both targets share one formatter. Use a font Google Docs has. Uploading raw Markdown instead gives Google's default look, which is looser and can push a one-page document onto a second page.
- **`append <source.md> <doc URL or ID>`:** adds the note to the end of an existing Doc on a new page. Headings become bold lines in the destination's body font, so the addition matches a document that does not use heading styles, and line spacing is set explicitly. It renders headings and plain paragraphs with bold or italic only and refuses everything else, so simplify the source rather than work around a refusal. In a Doc with several tabs it writes to the first tab.
- **`pull <doc> [--diff source.md] [--out PATH]`:** exports the Doc as Markdown with Google's escapes removed. `--diff` compares it with the gated vault note. `--out` refuses any path inside the vault.

**Copies first.** `append` refuses a Doc your account does not own. To add to a collaborator's document, copy it into your Drive and append to the copy. Editing the original needs an explicit override flag and the user's authorization for that specific document.

**Setup.** Install the Workspace CLI, add a Desktop OAuth client, and log in with the Drive and Docs scopes only. Agents never copy, read, or print the credential files.

**Known limits.** Prose, headings, lists, tables, footnotes, and inline code survive Markdown to Doc to Markdown. Code fences and callouts are flattened, local images do not upload, and citations are plain text with no live reference-manager fields. Comments and suggestions are not read back by `pull`.

## Boundaries

- **Vault Markdown is the single source of truth.** Never author an export from scratch, never restore the vault from a DOCX or a Doc, and never automate a merge of collaborator edits. `pull --diff` reports; the user decides what enters the vault.
- **Read-only by default.** Agents have read-only access to OneDrive and to collaborators' Google Docs. These two scripts are the narrow, explicit-authorization exception. Do not write to either target outside them, and do not use a chat connector or third-party MCP server to edit a Google Doc in their place.

## Verification

- **Post-export review is mandatory for both targets.** Re-open the exported DOCX, or read the Doc back with `pull`, and inspect the text and rendered pages. Check for AI-process commentary, decision-log framing, internal provenance, unresolved placeholders, broken citations, and layout problems the exporter cannot detect.
- **Page limits:** when a document has one, export a PDF and count pages. A Doc's default paragraph style can differ from its visible paragraphs, and a PDF exported through the Drive API can begin with an extra page holding only the tab title, which a download from the Google Docs menu does not add.
