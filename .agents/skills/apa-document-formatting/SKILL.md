---
name: apa-document-formatting
description: Format the headings of a Word document, or any document with section headings, per APA 7th edition using direct paragraph formatting instead of Word's built-in Heading styles, with single line spacing. Use when creating a manuscript, review, memo, report, or letter for the researcher, unless they ask for a different format for that document.
---

# APA Document Formatting

The researcher's default for any Word document (or other document with structural headings) created for them: APA 7th edition headings built as directly formatted body text, single-spaced.

## Rules

Do not use Word's built-in Heading 1/2/3 paragraph styles. They pull template formatting (coloured, sans-serif, sized differently from body text) that is not APA-compliant. Build each heading paragraph as directly formatted body text instead: the same font and size as the rest of the document, black, with alignment, weight, and case signalling the level.

| Level | Format |
|---|---|
| 1 | Centered, Bold, Title Case |
| 2 | Left-aligned, Bold, Title Case |
| 3 | Left-aligned, Bold Italic, Title Case |
| 4 | Indented, Bold, Title Case, ending with a period; body text runs on immediately after the period, on the same line |
| 5 | Indented, Bold Italic, Title Case, ending with a period; body text runs on immediately after the period, on the same line |

**The researcher's one deviation from strict APA:** single line spacing throughout, not APA's standard double spacing. Everything else about APA structure (margins, font consistency between headings and body, title-case rules) still applies unless the researcher specifies otherwise for a given document.

**Body font:** Times New Roman 12pt unless the document specifies otherwise. A lab-facing export through `operations/scripts/export-clean-docx.py` (the `vault-export` skill) keeps that script's declared font; this skill does not override it.

## Implementation (docx via docx-js)

Do not pass `heading: HeadingLevel.HEADING_X` to a `Paragraph`; that invokes Word's built-in styles. Construct the paragraph directly: set `alignment` (CENTER for level 1, LEFT for levels 2 and 3, with indentation for levels 4 and 5), and set `bold`/`italics` on the `TextRun` per the table, matching the body font and size.

## Boundaries

- This governs document structural formatting only, not prose voice or style; `academic-writing` and the researcher's writing-style rules own those.
- A different format the researcher asks for on a specific document wins for that document.

## Verification

- No paragraph in the output uses a built-in Heading style.
- Heading font and size match the body; spacing is single throughout.
