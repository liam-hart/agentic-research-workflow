# Video and animation

The detail behind `presentations` § 4b. Section numbers below refer to `SKILL.md`.

## Why a PDF cannot carry motion

A PDF cannot reliably play motion. Typst keeps only frame 0 of a GIF and rejects video files. Preview and Skim ignore media annotations, and `pdfpc` on macOS shows only the still. Pympress and `pdfpc` play in-slide video through GStreamer's `gtksink`, which the benchmark reports as broken under macOS Quartz. Beamer `media9` (Flash) and `animate` (Acrobat-only JavaScript) are dead ends.

## Choose a tier by how much of the talk moves

- **Tier 1, the default (1–3 clips):** `linked-still` (§ 3b). The best frame is the slide and the handout; a click opens the clip in QuickTime over the Pympress session, and `Cmd+W` returns. Use `local:` for project files so the kit builds the encoded absolute `file://` URL, and `badge: true` when the still alone does not read as playable. For a short animation that must survive any viewer, use a `repeat:` flipbook (Gallery).
- **Tier 2, high-stakes talks needing in-slide loops:** `export_deck.py --keynote` builds `exports/<stem>.key` in Keynote, with no manual staging. Each build step becomes a slide with its 300-ppi PNG as the background. Every local link to a `.mp4`, `.mov`, `.m4v`, or `.gif` becomes a native looping movie, fitted at its own aspect inside the linked still. Presenter notes come only from `#speaker-note`, repeated on each build step; `// SCRIPT:` blocks stay out of Keynote because they carry provenance. So author Tier 2 clips exactly as Tier 1: a still wrapped in a link. A bare `image("x.gif")` is not detected, because Typst keeps only its first frame. The export fails if a linked clip is missing or the target `.key` is open in Keynote. The Typst source stays canonical; the `.key` is a generated, gitignored delivery artefact that every export rebuilds, so settings made in Keynote (start on click, trims) are redone after the final export. `--png` alone still writes just the PNGs.
- **Tier 3, video-dominated talks (more than half the content):** Quarto Reveal.js. This leaves the Touying contract, so agree on it with the researcher first.

## Presenting from another computer

A `local:` link points to a path on your own machine and breaks on a podium computer. Present from your own laptop. If that is impossible, the stills still carry the talk, so keep the clips on a USB stick as the fallback.
