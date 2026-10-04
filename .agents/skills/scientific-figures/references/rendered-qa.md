# Rendered figure QA

Inspect the final export at the size readers will encounter. Keep automated, visual, and scientific checks distinct.

## Panel and layout

- Comparable panels have intentionally aligned plot areas, repeated gutters, label anchors, and scale treatment.
- Unequal widths, insets, color bars, and free-positioned panels have a scientific or explanatory reason.
- Panel labels follow reading order and cannot be mistaken for data labels.
- Legends, annotations, uncertainty, and significance marks do not collide with data or each other.

## Typography and accessibility

- Text remains readable at final size, including superscripts, subscripts, inset labels, and color-bar ticks.
- Meaning survives grayscale and common color-vision deficiencies; shape, line style, direct labels, or position provide redundant cues.
- Labels use canonical terminology, capitalization, units, and numerical precision from the manuscript.

## Scientific reading

- Axes and transformations do not visually exaggerate or conceal the comparison.
- The displayed observations, summaries, and uncertainty match the approved analysis and legend.
- Paired, nested, or repeated observations are not presented as independent by implication.
- Every panel supports the stated figure claim, and the claim remains bounded by the weakest necessary evidence.

## Export and provenance

- The canonical editable source, plotting code, environment/dependencies, output dimensions, and panel source-data map are identifiable.
- Required vector/raster formats, fonts, resolution, transparency, and color space are checked against current venue instructions.
- Diagnostic overlays and previews are labelled as QA artifacts and excluded from the submission package.

Record automated checks by command and result. A missing parser, unsupported PDF, or unauditable layout is `not checked`, never a pass.


## Gate commands (figure-kit builds)

Run all of these on the final export. A blocking step must pass before the figure ships. Some are enforced by a tool and some only by the author:
- `pov-panel` enforces step 6.
- `check_figure.py` enforces step 2, exiting 1.
- The author enforces steps 1 and 5.

Steps 3 and 4 produce evidence for the manual checklist above.

1. **Blocking (author): compile clean.** `typst compile` exits 0 with no `warning:` line, and every R panel script exits 0.
2. **Blocking (tool): size.**
   `python3 "<kit-root>/operations/scripts/check_figure.py" <export.pdf|png> --width-in <final width>`
   - FAILs for a PNG under 300 ppi at its final width.
   - FAILs for a PDF page more than 0.05 in off the target width, because a figure placed at text width would rescale its type.
3. **Colour evidence.** The same run writes greyscale and protan/deutan/tritan images and a contact sheet to `$TMPDIR/figure-qa/<stem>-<ext>/`. Open the sheet: every path kind and structure mark must stay decodable in every tile.
   - For a figure that uses both scanpath hues, add `--pair "#0072B2,#D55E00"`. Its greyscale WARN is expected. The manual check is that line style still separates the pair.
4. **Vendored-kit drift** (other repositories): add `--kit-dir figures/kit --canonical-dir "<kit-root>/operations/templates"`.
   - DRIFT means re-vendor, never hand-merge.
   - `--strict-drift` makes DRIFT a FAIL.
   - A missing directory or a single flag FAILs.
   - The gate compares `.typ` files only, so diff a vendored `figure-kit.R` by eye.
5. **Blocking (author): host document.** Build the host document (for example `make check`) and render the page holding the figure at 150 dpi (`pdftoppm -r 150 -png -f N -l N`). Inspect it at 100%:
   - labels legible and uncut (a chip cut at a photo edge means it sits off the photo);
   - no collisions;
   - caption intact;
   - no float or overflow warning.
6. **Blocking (tool): stand-ins.** Every stand-in frame is passed with `stand-in: true`, and `pov-panel` then refuses to compile it without `--input draft=1`. Before release, compile once without the flag. It must succeed.

`check_figure.py` never certifies accessibility or visual acceptance. Report its output verbatim, alongside what was inspected by eye.
