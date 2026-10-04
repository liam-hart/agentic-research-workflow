# Figure style kit

Conventions for figures built with the shared kit:
`<kit-root>/operations/templates/figure-kit.typ` (Typst/CeTZ) and
`figure-kit.R` (plotted panels), both reading `theme-colors.typ`. The code is canonical. When a
convention changes, change the kit and this file in the same pass, then recompile
`Figure Gallery.typ` and inspect it.

## Stack

| Layer | Tool | Why |
|---|---|---|
| Composition, photo overlays, labels, keys, panel letters | Typst 0.15.1 + CeTZ 0.5.2 (`figure-kit.typ`) | Same palette and compiler as the decks; the overlay is data in the source, not hand-dragged marks |
| Plotted panels (predictions or data) | R/ggplot2 (`figure-kit.R`), vector PDF via `cairo_pdf` | Analysis code is in R; Typst places the PDF with its fonts embedded |
| Illustrator, image models | Not in the pipeline | A hand edit to an export is lost at the next compile; conceptual art only on explicit request |

## Colour

- Colours come from `theme-colors.typ`: `cat` (Okabe–Ito) for data marks, `ink` tokens for ink. Never type a hex into a figure file; declare a genuine exception with `// lint-ok: <what it encodes>`. `figure-kit.R` reads `cat` and its ink tokens from the same file.
- Colour is never the only cue. Every path kind pairs a hue with a line style:

| Path kind (`GAZE` key) | Hue | Line | Used for |
|---|---|---|---|
| `kind-a` | `cat.blue` #0072B2 | solid | first path category (for example dwell on one object); its plot line |
| `kind-b` | `cat.vermillion` #D55E00 | dashed 4 / 2.4 pt | second path category (for example hops between landmarks); its plot line |
| `kind-c` | `cat.reddish-purple` #CC79A7 | dash-dot | third path category (for example a later revisit) |
| `gaze` | `P.text-primary` (neutral ink) | solid | gaze with no construct attached, e.g. two people's paths told apart by direct labels |

- Blue and vermillion are 1.34:1 apart in greyscale. `check_figure.py --pair "#0072B2,#D55E00"` warns on this pair by design, and the solid/dashed distinction carries it.
- Structure marks use neutral ink (`P.text-headline`): target = solid ring, anchor = dashed ring, surface boundary = dotted outline, empty location = dotted ring with a light fill, object in hand = solid ring.

## Marks

- **Fixation:** filled circle, 70% opaque, hue outline. Area is proportional to dwell: radius = `FIX-R` · √(dwell / 300 ms), `FIX-R` = 4 pt.
- **Saccade:** 1.1 pt line trimmed to the fixation edges, with a small filled arrowhead at the landing fixation.
- **Ghost path:** an earlier scanpath drawn under a later one (`scanpath(.., ghost: true)`): faint, thin, 0.6× fixations, no arrowheads.
- **Casing:** every mark over a photo sits on a white casing (80% opaque, +1.2 pt), so it survives a busy background.
- **Labels:** chips (7.5 pt ink on 90% white) with 0.5 pt cased leaders that stop at the ring edge. Anchor a chip on the side that faces its leader's target.
- **Labels stay on the photo.** `pov-panel` clips at the photo edge, so a stray label shows up cut in the render instead of silently shifting the panel.
- **Tags vs. key:** `tag(kind)[gloss]` labels a path in the image (swatch, bold kind, short gloss). `key-row(kind)[..]` builds a separate key. Prefer tags when a key costs height the page does not have.

## Type

- Font: the host document's body font. The default is the deck stack, Inter → Helvetica Neue → Arial. Set it once in `figure-page(font: ..)` and `fk_load(kit_dir, family = ..)`.
- Sizes at final physical size: panel letter 10 pt bold; labels and keys 7.5 pt; nothing below 6.5 pt. A venue minimum overrides these when it is larger.
- Sentence case, no all-caps, no letterspacing (your slide linter's rules apply to kit files too).

## Sizes and exports

- A figure file is one page at its final width: `#show: figure-page.with(width: ..)`, with auto height.
- Verified widths (`WIDTH`):
  - `grant-text` = 6.9 in (letter with 0.8 in margins, from the host document's `main.tex`);
  - `slide` = 841.89 pt (the deck canvas).
- Add a journal width only after reading that journal's current instructions, and record the date beside it.
- Exports: a vector PDF for LaTeX or Typst placement, plus a 600 ppi PNG for slides, Word, and previews.

## Honesty conventions

- **Illustrations.** A hand-placed scanpath is an illustration. Its caption opens "Illustration, not data." A figure meant to travel without its caption (slides) also carries the phrase inside the figure.
- **Predictions.** Plot the estimand the analysis tests (`statistics`): bare axes, no numeric ticks, a "Predicted" tag. Leave out uncertainty ribbons, which imply precision that was estimated. The R script documents the plotted values as placements, not effect sizes.
- **Stand-ins.** Pass `stand-in: true` to `pov-panel` for any stand-in frame. The build then fails unless it is compiled with `--input draft=1`, which stamps "DRAFT · stand-in frame" across the panel.
