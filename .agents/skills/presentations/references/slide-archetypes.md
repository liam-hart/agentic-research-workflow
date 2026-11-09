# Slide archetypes

The catalogue for `presentations` § 3b. Section numbers below refer to `SKILL.md`.

| Archetype | Use when | Slots |
|---|---|---|
| **Evidence hero** | One figure, table, or image carries the claim | dominant visual · optional narrow annotation column · optional `context-line` · `source-note` |
| **Split contrast** | Two accounts, conditions, or scales stand in parallel | two panels, each a heading + ≤ 3 fragments · optional shared `context-line`. Accent only when the two sides *are* the empirical contrast |
| **Factorial matrix** | A crossed design or a predicted 2×2 pattern | APA `table` with row-factor and column-factor headers · 4 cells · one note line |
| **Method progression** | An ordered pipeline or protocol timeline | 3–7 stages, each a name + one detail fragment, separated by `flow-arrow` · optional `context-line` |
| **Path model** | Predictor-to-outcome claims with matched and cross paths | per model: source · arrow · outcome, with the cross-domain path shown weaker (dashed, `text-secondary`) |
| **Predicted pattern** | Showing what the data would look like before there are data | a schematic matrix or a bare axes sketch · one reading note naming what is strong and what is weak |
| **Discussion grid** | Soliciting critique | 2–4 numbered prompts, each a short stem heading + one question. Numbers order them; colour does not |
| **Acknowledgements** | The slide after the title in external talks (§ 2b); lab-internal talks omit it (§ 1) | `acknowledgements(..)`: 3–5 `ack-person(name, role, photo:)` · optional lab roster panel · optional funding line. Take names and spellings from your own people reference |
| **Theoretical tension** | Naming the frameworks the hypotheses derive from | 2–3 panels, each a framework name + what it predicts + a secondary "Motivates H*n* · citation" line · optional `context-line` naming the observation that separates them |
| **Hypothesis map** | First showing, every section break, and the close (§ 2b) | `hypothesis-map(..)`: research question · 2–4 rows of id + short name + one-sentence claim · framework and measure line on the focused row. Exempt from the density budget |
| **Method justification** | A paradigm departs from the field standard | split contrast: what the standard paradigm controls away against what this one makes observable, naming the hypothesis that needs it |
| **Section divider** | Structural break in a talk without hypotheses | headline alone; exempt from the density budget. In a hypothesis-driven talk, use a hypothesis-map recall instead |

Further layouts (kit functions; see the gallery for each rendered):

| Archetype | Use when | Kit call |
|---|---|---|
| **Full-bleed image** | A still or photo carries the slide by itself (scene renders, apparatus) | `#full-bleed(image(.., fit: "cover"), [Headline], caption: ..)` in place of a `==` heading |
| **Big number** | One statistic is the finding (lightning talks, a headline effect) | `big-number(value, meaning, unit:, source:)` |
| **Prediction vs. result** | Comparing the predicted pattern with the data on matched axes | `prediction-vs-result(predicted, observed, note:)` |
| **Comparison panels** | 2–4 parallel images or figures (participants, conditions, rooms) | `comparison-panels(((label:, body:, detail:), ..))` |
| **Definition** | Naming what the talk means by a construct or framework (theory first) | `definition(term, body, source:)` |
| **Timeline** | Phases over time, with the current one marked | `timeline(((when:, label:, detail:), ..), current: n)` |
| **Status rows** | Lab updates: done, in progress, blocked, asks | `status-rows(((status, body), ..))` |
| **Aims overview** | Prelims: the hypothesis map one level up | `aims-overview(AIMS, focus:)` |

Lab-internal layouts (Lab Meeting and Lab Update decks, § 1):

| Archetype | Use when | Kit call |
|---|---|---|
| **Agenda rail** | Section divider in a long lab talk; replaces the hypothesis-map recall | `agenda-rail(PARTS, current: n, tag: [..])` under a `==` headline naming the part; `tag` sets the footer |
| **Linked still** | A demo, GIF, video, or external site. The PDF cannot play motion, so the best single frame carries the handout and a click opens the real thing | `linked-still(image(..), "https://..", label: [..])`, or `local: "operations/attachments/<clip>.mp4"` for a project file (kit encodes the `file://` URL); `badge: true` adds a ▶ chip on the still. Video tiers: SKILL.md § 4b and [video-and-animation.md](video-and-animation.md) |
| **Flipbook** | A short animation (scanpath steps, a rotation) that must survive any PDF viewer | `#slide(repeat: n, self => ..)` with one frame image per `self.subslide`; no helper needed |
| **Open problem** | Putting an unsolved design problem to the room; the headline may ask the genuine question | `open-problem([constraint], ((idea, trade-off), ..))` with 2–4 ideas |
| **Section tag** | Footer label for a talk part without a hypothesis | `section-tag([New since 16 Sep])` |

Figure pieces (`deck-figures.typ`, CeTZ 0.5.2): `annotated-figure` (numbered markers over an image with a key), `path-model` (nodes and arrows, weak paths dashed), `prediction-plot` (bare schematic axes labelled "Predicted", direct-labelled series), `design-matrix` (APA factorial table with condition-coded labels). Real data plots still come from R or Python scripts, not CeTZ.
