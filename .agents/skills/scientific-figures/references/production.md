# Figure production

The build procedure for figures made with the shared kit. Run it after the figure contract in
`SKILL.md` is recorded. Conventions are in [style-kit.md](style-kit.md); gate commands are in
[rendered-qa.md](rendered-qa.md). Kit root:
`<kit-root>/operations/templates/` (`figure-kit.typ`, `figure-kit.R`,
`theme-colors.typ`, starter templates, `Figure Gallery.typ`).

## 1. Make a bundle

One folder per figure. The editable source sits beside every export.

```text
<bundle>/
  <slug>.typ           composition and overlay coordinates: the editable source
  <slug>-<panel>.R     one script per plotted panel (optional)
  frames/              source rasters; provenance recorded in the .typ header
  kit/                 vendored kit (outside the kit repository only)
  <slug>.pdf  <slug>.png   exports
```

- **In the kit's own repository:** use `resources/diagrams/<slug>/`, import `../../operations/templates/figure-kit.typ`, and compile from the repository root with `--root .`. Link the bundle from the owning project's figure reference (for example `projects/<project>/Figure Reference.md`).
- **In another repository:** vendor the kit so the repository builds anywhere. Typst cannot import across a project root. Copy the files side by side with a provenance first line:

  ```sh
  KIT="<kit-root>/operations/templates"
  SHA=$(git -C "$KIT/../.." rev-parse --short HEAD)   # the kit must be committed first
  mkdir -p figures/kit
  for f in figure-kit.typ theme-colors.typ; do
    { echo "// vendored from kit@$SHA operations/templates/$f"; cat "$KIT/$f"; } > "figures/kit/$f"
  done
  { echo "# vendored from kit@$SHA operations/templates/figure-kit.R"; cat "$KIT/figure-kit.R"; } > figures/kit/figure-kit.R
  ```

  Re-vendor instead of editing `figures/kit/`. A kit change belongs in the kit repository first.
- **Start from a template:** `Figure - POV Scanpath.typ` for a photo with an overlay, and `Figure - Plotted Panel.R` for a plotted panel. `Figure Gallery.typ` renders every kit piece as a visual menu.

## 2. Get frames

- Take frames from the headset recording losslessly, and record the video path and timestamp in the `.typ` header:
  `ffmpeg -ss 00:01:23.4 -i <video> -frames:v 1 frames/<name>.png`.
- Frames from the researcher's own run-through are stimulus screenshots. Never pull illustration frames from a participant session.
- Ask for exactly what the figure needs. For a POV surface figure:
  - stand at head height about 1.5 m back, with the surface in the middle third;
  - keep the target, anchors, and every edge visible;
  - turn debug overlays off;
  - hold still for 2–3 s per view;
  - use one standing spot for every view of the same surface.
- Never hand-edit scene files for a capture. Say what to capture.
- Until frames exist, prototype on an existing frame. Pass `stand-in: true` to `pov-panel` and compile with `--input draft=1`: the kit refuses a non-draft build of a stand-in, and the draft carries a stamp.

## 3. Place the overlay

1. Compile with `--input grid=1`. Read the target, anchors, and boundary polygon as full-frame fractions (origin top-left).
2. Hand-place fixations as `(x, y, dwell-ms)`. The path's shape carries the pattern, and the values are not data. A path that dwells on one object reads as a tight cluster of long fixations inside the target ring. A path that surveys the layout reads as short hops from the target to the anchors and edges.
3. `crop` is a view onto the full frame. Changing it never moves a mark, so crop last, to fit the page.
4. Place label chips on the photo, anchored on the side facing their leader.

## 4. Plotted panels

- Source the kit and follow the pattern in `Figure - Plotted Panel.R`: `fk_load(kit_dir, family)`, `fk_theme(fk)`, then `fk_save(plot, stem, width_in, height_in, family)`. That writes a vector PDF and a 600 ppi PNG.
- Match the panel's height to the neighbouring photo panel. The photo height is `width × crop-height-fraction / crop-width-fraction × frame aspect`.
- A prediction panel plots the estimand the analysis actually tests. Confirm it with `statistics` before drawing.

## 5. Compose and export

```sh
typst compile [--root .] <slug>.typ <slug>.pdf
typst compile [--root .] --format png --ppi 600 <slug>.typ <slug>.png
```

Any compiler warning fails the build. Commit the source, the plotted-panel scripts, the frames, and both exports together. Export stand-in builds as `<slug>.draft.pdf|png`. A repository can ignore `*.draft.*`; otherwise commit at most a stamped draft PDF.

## 6. Gates

Run the gate commands in [rendered-qa.md](rendered-qa.md), then its checklist. Record every check run, every check not run, and every intentional exception. Author acceptance comes last, and only from the author.

## 7. Captions

`academic-writing` owns the wording, and this skill owns what the caption must decode.
- Give the claim first.
- Say what is illustrative.
- Define any encoding the figure does not label itself.
- Obey the venue's length limit; if it allows only brief captions, use one or two sentences each.

## Worked example: a two-panel scanpath figure

Claim: viewers who inspect one object closely and viewers who survey the room produce visibly different paths. Panel A is a first-person frame of a room with a hand-placed overlay; panel B is a plotted prediction.

1. Make the bundle `figure-room-paths/` with `figure-room-paths.typ` and `figure-room-paths-b.R`.
2. Capture one frame at head height, then place the frame under `frames/` and record its source in the `.typ` header. While no real frame exists, pass `stand-in: true` and compile with `--input draft=1`.
3. Compile with `--input grid=1`, read the target and anchor positions, and place two paths: a tight cluster of long fixations in the target ring, and short hops from the target to the anchors and edges. Each path pairs a hue with a line style.
4. Build panel B with `fk_load`, `fk_theme`, and `fk_save`, at the same height as the photo panel. Plot the estimand the analysis tests, with bare axes and a "Predicted" tag.
5. Compose both panels in the `.typ`, caption it "Illustration, not data." plus the claim, and run the gate commands in [rendered-qa.md](rendered-qa.md).
