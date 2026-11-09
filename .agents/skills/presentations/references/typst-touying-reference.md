# Typst, Touying, and colour reference

The detail behind `presentations` § 4 and § 4a. Section numbers below refer to `SKILL.md`.

## Versions

Pin the deck import to `@preview/touying:0.8.0`. The supported compiler baseline is Typst 0.15.1. An older delivered deck may stay pinned to its original Touying version as a historical record.

## Touying 0.8.0 features in use

- **Handout export.** `--input export-mode=handout` collapses every animation to its final state, one page per slide. It is the version to share after a talk. `export_deck.py` (§ 6) writes it alongside the presentation PDF.
- **Speaker notes for Pympress.** `#speaker-note[..]` is invisible on the slide. `--input notes=pympress` (which `deck-kit.typ` reads) draws each slide's notes on the right half of a doubled page, the layout the Pympress presenter app splits between laptop and projector. See § 5 for what belongs in a note.
- **Parked slides.** Label a heading `<touying:never>` to keep a cut or draft slide out of every export without commenting out its markup. Backup slides after the discussion stay live.
- **Overflow is not a compiler signal.** With Touying 0.8.0 and Typst 0.15.1, a body taller than the slide silently continues onto extra pages, a box wider than the slide is silently clipped at the page edge, and an over-long `#speaker-note` is silently clipped on the Pympress page. All three compile with exit 0 and no warning, so neither the compile step nor `export_deck.py` catches them. Only the rendered-PDF inspection in § 6 does.

Not adopted: article mode (it linearizes the deck into a rough A4 document; per-slide script comments are the prose surface), and the new animation entry points (`animate`, `touying-render`, element-level `touying-recall`), which solve nothing current. The hypothesis map uses a kit function rather than `touying-recall` because each recall changes its focus.

## Colour tokens (§ 4a)

Every deck draws colour from `operations/templates/theme-colors.typ`, a contrast-first token set generated as a function of background and a target WCAG 2.1 ratio, not chosen by hand. `deck-kit.typ` imports it and exposes `THEME` and the palette `P`; decks compile with `--root .` and switch to a dark room with `--input theme=dark`, which re-solves every token against the dark canvas.

Each token sits at a fixed tier: `surface-subtle` ≥ 1.1:1, `border-element` ≥ 3:1, `text-secondary` ≥ 4.5:1, `text-primary` ≥ 7:1, `text-headline` ≥ 10.5:1, with accent hues (`blue teal orange purple red`) supplied at matched 3:1 / 4.5:1 / 7:1 variants. Headlines use `text-headline` so the assertion survives degraded projection and reduced audience contrast sensitivity.

Categorical data marks use the Okabe–Ito set (`cat`) verbatim; any mark in `cat-needs-outline-on-light` carries a 0.75pt `text-primary` outline, and every categorical encoding is doubled by a non-colour channel — marker shape, dash pattern, or a direct label.

A contrast linter (for example `operations/scripts/contrast_lint.py`, § 6) parses the live `theme-colors.typ` and fails a token below its tier floor, a categorical mark below 3:1 on the light canvas that `cat-needs-outline-on-light` does not declare, a declaration naming no `cat` mark, or a mark below 3:1 on the dark canvas. It audits the palette file only. It cannot see whether a deck actually draws the 0.75pt outline on a declared mark, or how legible a colour is on a surface other than its canvas (for example, text on a `container` fill).

Regenerate tokens with your palette generator script; never hand-edit a hex.
