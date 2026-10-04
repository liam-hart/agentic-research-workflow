---
name: scientific-figures
description: Design, build, revise, or audit evidence-bound scientific figures and legends for behavioral and cognitive-neuroscience manuscripts, grants, and talks, including illustrative scanpath overlays on VR frames built with the shared figure kit. Use when a task concerns a quantitative or predicted plot, a multi-panel figure, a paradigm or scanpath illustration, figure source-data mapping, or rendered figure QA; use presentations for slide layout and imagegen only for explicitly requested conceptual bitmap art.
---

# Scientific Figures

Create figures that make one bounded scientific claim legible without changing the analysis that supports it. Work from the live manuscript, approved analysis, source data, and target output contract.

## Ownership

- `statistics` owns unresolved estimands, models, contrasts, uncertainty, multiplicity, and the unit of analysis.
- `coding` owns implementation and reproducibility of plotting code.
- `academic-writing` owns Results prose and the wording and style of figure legends.
- This skill owns figure-level evidence architecture, the legend's scientific content contract, visual encoding, source-data traceability, and rendered QA.

Do not infer missing scientific choices from a plotting convention. Return unresolved choices to the owning authority before drawing a figure that would silently encode them.

## Figure contract

Before plotting or restructuring, record:

- the Results-level question and one-sentence figure claim;
- the observation and analysis units, comparison, and approved uncertainty display;
- each panel's distinct role in establishing, qualifying, bounding, or testing the claim;
- the canonical data and plotting-code locations, plus any exclusions and before/after counts;
- target medium, physical size, required formats, and current venue instructions;
- likely reviewer or interpretation risks.

For a multi-panel figure, read [multipanel-evidence.md](references/multipanel-evidence.md). Do not grow a dashboard by repeating the same result with interchangeable metrics. Recommend relocation or removal, but do not change manuscript scope without approval.

## Data and encoding safeguards

- Preserve all valid observations unless an approved scientific or statistical rule says otherwise. Never silently sample, aggregate, drop missing rows, or transform invalid values to make a plot render.
- When the scientific comparison is paired or repeated, preserve that dependence in the display where it materially aids interpretation.
- Use colorblind-accessible, semantically stable encodings. Color cannot be the only cue. Avoid rainbow/jet maps for quantitative magnitude.
- Make axes, units, transformations, reference lines, uncertainty, and sample definitions explicit. Never add a significance mark without the comparison and multiplicity convention that authorize it.
- Position annotations from data or uncertainty envelopes rather than unexplained hard-coded coordinates when geometry may change.

## Production

Build figures with a shared figure kit (your own; it does not ship here), so grants, manuscripts, and decks share one palette, type scale, and gaze-mark grammar. The kit has two halves:
- `figure-kit.typ` (Typst/CeTZ) handles composition, photo overlays, labels, and keys.
- `figure-kit.R` handles plotted panels.

Both live in `<kit-root>/operations/templates/` and read `theme-colors.typ`.

- Procedure, bundle layout, frame capture, vendoring into other repositories, and a worked example: [production.md](references/production.md).
- Palette, gaze grammar, marks, type, widths, and honesty conventions: [style-kit.md](references/style-kit.md).
- Gate commands: [rendered-qa.md](references/rendered-qa.md) § Gate commands.
- A hand-placed scanpath is an illustration, not data, and its caption says so.
- Mark a stand-in frame `stand-in: true`. The kit then refuses to build it without `--input draft=1`, so a stand-in cannot ship.

## Legend and source-data contract

The legend should let a reader decode the figure without guessing: define panels, conditions, units, `n`, analysis/replicate unit, centre and uncertainty, statistical comparison, and relevant tests or models. Adapt the form to the actual venue; do not impose a generic Nature template.

Maintain a panel-to-source map containing the plotted variables, transformations, exclusions, and canonical source-data location. A source-data table is a traceability artifact, not authority to release restricted participant data.

## Rendered QA

After every material change, inspect the exported artifact at its final physical size. Read [rendered-qa.md](references/rendered-qa.md) for multi-panel, typography, collision, accessibility, and export checks.

Automated geometry or PDF checks are advisory unless the project explicitly makes a check blocking. They do not establish scientific correctness, accessibility, or visual acceptance. Record every unavailable check and every intentional exception rather than claiming a pass.

## Boundaries

- Verify current journal dimensions, format, legend, source-data, accessibility, and AI-image policies for the exact target; do not reuse remembered limits.
- Do not generate conceptual or mechanism art unless explicitly requested; route bitmap generation to `imagegen` and preserve disclosure/provenance gates.
- Do not use third-party figure galleries or templates unless reuse rights and semantic compatibility are confirmed.
- Preserve editable source and reproducible code. Do not treat a raster preview or diagnostic overlay as the canonical figure.

## Verification and handoff

Report the figure claim, panels, source-data mapping, files produced, checks actually run, exceptions, and unresolved scientific or venue gates. Distinguish code execution, automated rendered QA, manual final-size inspection, and author acceptance.
