---
name: vault-onedrive
description: Export a lab-facing DOCX from canonical vault Markdown to an authorized OneDrive destination using export-clean-docx.py. Use when the user explicitly authorizes the export in the current session; do not use for general document editing or unapproved external writes.
---

# Vault to OneDrive Sync Skill

This skill handles the controlled export of vault-side Markdown documents (like hypothesis documents, SOPs, and reference-manager standards) to their canonical, lab-facing OneDrive destinations as `.docx` files.

## Workflow

1. **Use `export-clean-docx.py`:** Always use your export script, e.g. `operations/scripts/export-clean-docx.py <input_file.md> <output_file.docx>` to perform the conversion.
2. **Review before export:** The script enforces a hard gate—it will refuse to export if there are raw Zotero citekeys or unresolved Obsidian wikilinks/tags.
    - The script automatically excludes fenced code blocks from tag/citekey/wikilink detection. If a false-positive still occurs in prose (not code), investigate whether the source text genuinely contains a stray tag-like pattern and fix it there — never mutate code examples to work around the regex.
    - If the script fails due to unresolved citekeys, you must resolve them to proper APA citations manually in the Markdown source first, as the script doesn't attempt to resolve authors automatically.
3. **OneDrive Destinations:** Take the destination from the project's own reference note, never from memory. Examples of the shape (replace with your project's paths):
    - **Project A:** `~/Library/CloudStorage/OneDrive-<org>/<shared-folder>/project-a/`
    - **Project B:** `~/Library/CloudStorage/OneDrive-<org>/<shared-folder>/project-b/`
4. **Export font:** Exports use a single declared font (the script's `EXPORT_FONT` constant) rather than the vault's internal display font. A `.docx` is editable, so the declared font must exist on the recipient's machine; otherwise Word substitutes silently while keeping the name, which mixes typefaces once a collaborator types and shifts page breaks between readers.

## Boundaries

- **Never create raw `.docx` from scratch:** Only use the vault's Markdown files as the single source of truth for these exports.
- **Read-Only OneDrive Rules:** Remember that agents generally have read-only access to these OneDrive paths, and this script provides the narrow, explicit-authorization exception for writing lab-facing documents. Do not write to OneDrive outside of this script.

## Verification

- **Post-export review is mandatory:** Re-open the exported DOCX and inspect its extracted text and rendered pages. Check for AI-process commentary, decision-log framing, internal provenance, unresolved placeholders, broken citations, and layout problems the exporter cannot detect. The vault Markdown remains canonical.
