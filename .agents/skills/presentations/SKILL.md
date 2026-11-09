---
name: presentations
description: "Draft native Touying (Typst) research presentations from a user-approved narrative arc using assertion-evidence headlines, sparse audience-facing copy, and per-slide script comments. Use when creating research talks, journal clubs, and synthesis decks; use a document skill for PowerPoint or native Google Slides artifacts."
---

# Presentations

Produce a native Touying research deck, built from literature, project material, or synthesis notes on a narrative arc the user has approved, in which each slide states one assertion and shows its evidence. Native Touying `.typ` source is canonical; PDF is a generated export. Existing Marp decks are historical artifacts, not templates for new work.

## 1. Select the Touying template

Templates live in `operations/templates/` as `Touying Presentation - <Type>.typ`:

| Type | Use for |
|---|---|
| Research Talk | One assertion and one primary item of evidence per slide |
| Journal Club | One paper, background through critique |
| Synthesis | A multi-paper lineage landing on a gap, proposal, or critical test |
| Conference Talk | 12–15 minutes of results on the full hypothesis spine |
| Lightning Talk | 5 minutes, 4–6 slides, one hypothesis and one result |
| Prelim Talk | Prelim or committee: framework, aims, a map per aim, timeline |
| Lab Update | 5–10-minute lab check-in; no spine (lab-internal) |
| Lab Meeting | Full lab slot on one project: recap, changes, open problems (lab-internal) |

**Lab-internal talks** (Lab Update, Lab Meeting) skip the acknowledgements slide, may take a casual title, use a lighter spine with `section-tag` footers, and may headline an open-problem slide with a genuine question. External talks keep every rule below. Read [references/deck-templates.md](references/deck-templates.md) for each template's full shape and the exact exemptions.

All of them import `operations/templates/deck-kit.typ`, the shared slide geometry, helpers, and layouts promoted from a delivered talk deck. The CeTZ figure pieces live in `operations/templates/deck-figures.typ`, which a deck imports only when it needs them. Change shared layout there, never by copying a divergent helper into one deck. `operations/templates/Touying Gallery.typ` renders every layout and figure piece on its own slide: open its PDF as the visual menu when drafting.

Ask which presentation type the user wants only when the request and source material do not resolve it.

## 2. Narrative arc first

Do not generate slides immediately. Follow a two-phase workflow:

### Phase 1: narrative arc
1. Read the supplied sources and identify the audience, purpose, time limit, and evidential boundary.
2. **Theory before method.** Name the major theoretical frameworks the talk engages and the tension between them: what each predicts, and where they disagree. A literature beat earns its slide by feeding a framework or a tension, not by being relevant in general. If the project cannot yet name its frameworks, say so to the researcher as a project gap rather than papering over it with a longer methods section.
3. **Draft the hypothesis map** (§ 2b) before any slide: the research question in one sentence, and each hypothesis as a chain of framework → prediction → measure → the result that would count against it.
4. **Map every method and result beat to a hypothesis.** A beat that tests no hypothesis is cut or moved to backup. This holds for proposal talks too: they may be methods-heavy when methods feedback is the goal, but every method still answers "which prediction needs this?"
5. Propose a one-page Markdown outline that tells a story rather than listing facts, with the hypothesis map at its head and the beat-to-hypothesis mapping visible.
6. For a synthesis deck, make each evidence beat close with what it leaves unresolved so the next beat is motivated.
7. Wait for the user to approve or revise the arc and the map.

## 2a. Story shape and slide budget

The researcher's rules. However short the talk, it tells a story with five elements: background and motivation, the questions or objectives, the challenges overcome, the data behind the findings, and conclusions or next steps.

**Agents never estimate timing.** Do not estimate speaking time or minutes per section, ask time-budget questions, or cut or park content for time. The researcher manages timing. The table below applies only when the researcher gives a speaking time and asks for a slide budget.

Budget by **speaking time**, not slot length. A 30-minute seminar slot with 15–20 minutes of discussion is a 10–15-minute talk. The 5- and 10-minute rows are the researcher's. The longer rows extend the same pattern: about one slide per speaking minute, background about a fifth of the talk, one questions slide, data and discussion about three fifths, then the conclusion. The upper bound is a cap, not a target. More than about one slide per speaking minute risks running out of time before the closing slides.

| Speaking time | Slides, no more | Background | Questions / hypotheses | Data + discussion | Conclusion |
|---|---|---|---|---|---|
| 5 min | 4–6 | 1 big-picture | 1 | 1–3 quick | 1, with contact info |
| 10 min | 9–12 | 2 big-picture | 1 | 6 | 1 |
| 15 min | 13–17 | 3 | 1 | 9–11 | 1 |
| 20 min | 18–22 | 4 | 1 | 12–15 | 1 |
| 30 min | 26–32 | 6 | 1 | 18–22 | 1–2 |
| 45 min | 40–48 | 9 | 1 | 27–33 | 2 |
| 60 min | 52–64 | 12 | 1 | 36–44 | 2 |

- **What counts.** Acknowledgements (§ 2b) sit outside the budget. Hypothesis-map recalls count toward data + discussion, one per section. In a 5- or 10-minute talk, the hypothesis map is the questions slide and the footer tag replaces recalls.
- **Proposal talks.** Before there are data, "data + discussion" means methods, predictions, and the method-justification slide, each mapped to a hypothesis (§ 2).
- **Challenges overcome.** This story element lives inside data + discussion, not in a separate section.
- **Backup slides** after the discussion slide are outside the budget. Parked slides (`<touying:never>`) do not render.

## 2b. Fixed opening and the hypothesis spine

If the hypotheses first appear late, after the methods, the methods are heard without knowing what they test.

**Fixed opening.** Title → **acknowledgements** → 1–2 motivation slides → theoretical tension → hypothesis map. Acknowledgements always follow the title so they cannot be skipped for time. The map lands within the first ~20% of the talk. Lab-internal talks skip the acknowledgements and use the lighter spine (§ 1).

**The spine.** The hypothesis map is the talk's recurring anchor, built with the kit's `hypothesis-map(HYPOTHESES, question: ..)` so every appearance is identical:

1. **First showing** (`focus: none`): research question plus every hypothesis with its framework and measure.
2. **Recall at each section break** (`focus: "H2"`): the tested hypothesis at full contrast, the others dimmed. The recall replaces a bare section divider.
3. **Footer tag.** After a recall, every slide's footer reads "Tests H2 · <name>" until the next recall. Use `#tests("H1", "H3")` on a slide that serves a different hypothesis than its section.
4. **Close** (`focus: "close"`): all hypotheses restored, narrated as what each possible outcome would mean. The footer tag clears for the discussion.

Emphasis on the map is contrast tier and weight, never accent colour: accents stay reserved for the empirical conditions the deck tracks. Headline each map slide declaratively ("Three hypotheses organize the study"); the research question sits on the slide, not in the headline.

**Method justification.** When a paradigm departs from the field's standard (for example, naturalistic stimuli or free exploration), give one slide on what it makes observable that the standard paradigm controls away, and which hypothesis needs that. "Ecologically valid" alone does not persuade a research audience; the answer that works is what the paradigm makes observable (for example, self-selected input that a constrained task removes).

### Phase 2: slide draft

1. After approval, draft native Touying `.typ` slides from the matching template.
2. Save the canonical deck in `resources/presentations/` or the relevant project presentation folder. Generated PDFs belong in `resources/presentations/exports/`.
3. Apply the `academic-writing` skill's current prose and title guidance. This skill owns slide architecture, narrative sequencing, and density.
4. Put only audience-facing material on slides. Short delivery cues go in `#speaker-note[..]`; the script and context go in the slide's `// SCRIPT:` comment (§ 5). Never put decision-log, issue, or study-log IDs (`D-123`, `#612`, `S-045`) in audience-facing text; they belong in comments only.
5. Use descriptive relative asset paths and preserve source provenance in comments without turning those comments into presenter notes.

## 3. Assertion-evidence contract

- Each substantive slide headline is a complete declarative sentence stating the takeaway. Use a neutral descriptive sentence when the evidence does not support a stronger claim.
- Do not use rhetorical questions, teasers, colloquial titles, em-dash punchlines, self-congratulation, or stock AI phrasing. The one exception is an open-problem slide in a lab-internal talk, which may ask the genuine question (§ 1).
- Keep a headline concise enough to remain on one line when practical (about 10–12 words or 80 characters).
- Keep audience-facing explanatory copy below 20 words per slide whenever the evidence can carry the argument. Labels, citations, table cells, and axis text do not count toward that budget.
- Prefer one primary chart, diagram, image, comparison, or formal table over bullet-heavy prose.
- The rhetorical-question ban above applies to slide headlines, not to the deck title.

## 3a. Typographic and layout anti-patterns

A recurring set of stock visual habits makes a deck read as marketing collateral rather
than as academic evidence. Your slide linter (for example `operations/scripts/slide_lint.py`) should fail closed on them; a deck
that trips it does not ship.

- **Banned outright:** eyebrow or kicker headers (no `label-head`-style helper, ever),
  `upper()` or all-caps, `tracking:` letterspacing, emoji, and hardcoded hex in a deck.
- **Constrained:** a border needs a real containment job and takes a `0.5pt`
  `P.border-element` hairline, never an accent. Accent colour encodes only an empirical
  condition, hypothesis, or factor the audience tracks, always doubled by a text label; it
  never tags furniture or varies hue per panel. Unboxed panels are the default; a card is
  one archetype slot.
- **Hierarchy:** rank by size, weight, and position; colour encodes, it does not rank. A
  panel heading is never smaller than body copy.

Read [references/typographic-anti-patterns.md](references/typographic-anti-patterns.md)
for the rationale behind each ban and the size/weight/token table for every text role.

## 3b. Slide archetype catalog

Compose a slide by filling the slots of one archetype. Two archetypes on one slide means
two ideas, which Naegle Rule 1 splits into two slides. Each takes a headline and, where the
evidence needs it, an optional `context-line` (§ 3b-i).

Read [references/slide-archetypes.md](references/slide-archetypes.md) when choosing an archetype or composing a slide. It holds the catalogue (when to use each archetype and its slots), the kit layouts with their calls, and the figure pieces.

Anything that does not fit an archetype is a signal to reconsider the slide, not to invent
a new visual device. Propose a catalog addition before building one.

## 3b-i. Context line

The bottom band under the evidence is a **context line**, not a takeaway. It is optional.
It earns its place only when it carries information the audience cannot get from the
headline, the figure, or the narration:

- a design choice or its rationale
- a key parameter
- provenance (the literature or paradigm an idea comes from)
- what a null or alternative result would look like
- a caveat that changes how the slide should be read

If a line works as something the presenter would say aloud (a transition, a restatement
of the headline, a summary, a motivational sentence), it belongs in the slide's `// SCRIPT:` comment, not on the slide. If nothing qualifies, leave the band empty.

| Keep | Cut (move to narration) |
|---|---|
| "Stimuli are sized to fill the screen so every item is equally visible." (design rationale) | "Rather than controlling for this variability, we use it." (spoken framing) |
| "Predicted, not observed. Two flat, parallel lines would be the null result." (null pattern) | "We carry this logic to the next experiment." (transition) |
| "The fine-grained scale connects to high-similarity lure tests in the pattern-separation literature." (provenance) | "One continuous session: study twice, then test three ways." (restates the timeline) |

The helper is `context-line(body)`.

## 3c. Deck and talk titles

The researcher's approved preferences. The deck title is also the title submitted to seminar organizers, so the same rules apply to both. A lab-internal talk (§ 1) may instead use a casual title in the presenter's own words.

- **One title, no subtitle.** Never add a colon-split title or a subtitle line unless a venue explicitly requires one. Agents overuse subtitles; do not propose them in brainstorms either.
- **Approved styles:**
  - *Genuine question* — the question the study actually tests, e.g. "Does How We Sort a Pantry Predict What We Find Later?" Question titles suit **talks and research proposals only**; never use them for manuscripts, posters, abstracts, or any other output.
  - *Claim* — one sentence stating the thesis; before data exist, word it as framing or hypothesis, not as a result.
  - *Descriptive* — names the variables and their relation in plain terms.
- **Not wanted:** metaphors, puns, teasers, scenario titles, audience-invitation titles, or contrast slogans.
- **Craft:** concrete nouns over abstractions; the new or emphasized idea last; verbs matched to the design (`predict`, not `shape` or `drive`, for observational work). Talk titles may be shorter than the ~10–12-word journal-article guidance in `academic-writing`.
- When brainstorming, load this skill and `academic-writing` first, and give a reasoned recommendation.

## 4. Native Typst and Touying layout

Use Typst primitives directly; do not recreate HTML/CSS layout conventions.

- Use `grid(columns: ..., gutter: ...)` for spatial composition and aligned comparisons.
- Use `#slide(composer: (...))[...][...]` when a Touying multi-column slide is clearer than a nested grid.
- Use `box` or `block` for bounded cards, definitions, and restrained callouts.
- Build APA-style tables with `table`, `table.header`, and explicit `table.hline` rules. Avoid vertical rules and decorative cell fills unless they encode meaning.
- Use CeTZ for cognitive flowcharts, timelines, spatial layouts, and diagrams that need nodes and edges. Keep simple comparisons in native `grid`. The kit's CeTZ pieces live in `operations/templates/deck-figures.typ`, pinned to `@preview/cetz:0.5.2`; a deck that draws its own CeTZ figure uses the same pin.
- Use relative paths with `image(...)`; never use Obsidian embeds or raw HTML in a `.typ` deck.
- Keep deck-specific helpers small and local. Shared helpers live in `operations/templates/deck-kit.typ`; propose an addition there before copying a helper across decks.

Pin the deck import to `@preview/touying:0.8.0` (compiler baseline Typst 0.15.1). Touying features in use: handout export (`--input export-mode=handout`), Pympress speaker notes (`--input notes=pympress`), and parked slides labelled `<touying:never>`. **Overflow is not a compiler signal:** an over-tall body spills onto extra pages, an over-wide box is clipped, and an over-long note is clipped, all with exit 0; only the rendered inspection in § 6 catches them. Read [references/typst-touying-reference.md](references/typst-touying-reference.md) for feature mechanics and features not adopted.

## 4a. Colour authority

Every colour comes from `operations/templates/theme-colors.typ` through the `P` palette that `deck-kit.typ` exposes; never hardcode or hand-edit a hex, and regenerate tokens with your palette generator script. Headlines use `P.text-headline`. Categorical marks use the Okabe–Ito `cat` set, outline any mark in `cat-needs-outline-on-light`, and double every colour encoding with shape, dash, or a direct label. Compile with `--root .`; `--input theme=dark` re-solves every token for a dark room. The token tiers and WCAG 2.1 ratios are in [references/typst-touying-reference.md](references/typst-touying-reference.md) § Colour tokens.

## 4b. Video and animation

A PDF cannot reliably play motion, so choose by how much of the talk moves:

- **Tier 1, the default (1–3 clips):** `linked-still` (§ 3b): the still is the slide and handout, a click opens the clip. A `repeat:` flipbook covers a short animation that must survive any viewer.
- **Tier 2, high-stakes talks needing in-slide loops:** `export_deck.py --keynote`, authored exactly as Tier 1.
- **Tier 3, video-dominated talks:** Quarto Reveal.js, which leaves the Touying contract; agree on it with the researcher first.

`local:` clip links break on a podium computer: present from your own laptop, with the clips on a USB stick as the fallback. Read [references/video-and-animation.md](references/video-and-animation.md) before adding any clip (player limits, QuickTime and Keynote mechanics, Tier 2 failure modes).

## 5. Script comments and speaker notes

Separate companion explainers are retired: a companion drifts out of date the moment the deck changes. The script now lives with its slide, in two channels:

- **`// SCRIPT:` comment block** directly above each slide's `==` heading. It never renders. It holds what an agent needs to edit the slide well and what the presenter wants to say: the talking points, the point the slide must land, sources and provenance, and decision IDs. Write it before the slide body; it is how agents keep slide copy sparse without losing context.
- **`#speaker-note[..]`** is what the presenter sees in Pympress. Keep it to 2–4 short bullets or lines drawn from the script. A note longer than about half a page is silently clipped (§ 4), so never paste the script into it.

## 6. Verification

Compile every new or edited deck before delivery, audit the palette, and lint the source:

```sh
python3 operations/scripts/check_decks.py "path/to/deck.typ"   # compile gate, 4 modes
python3 operations/scripts/contrast_lint.py
python3 operations/scripts/slide_lint.py
```

Export a finished deck with one command. It writes `<stem>.pdf` (animated), `<stem> — Handout.pdf` (one page per slide, for sharing), and `<stem> — Pympress.pdf` (slides plus notes) to `resources/presentations/exports/`, and fails on any compiler warning:

```sh
python3 operations/scripts/export_deck.py "path/to/deck.typ"
pympress "resources/presentations/exports/<stem> — Pympress.pdf"   # present with notes
python3 operations/scripts/export_deck.py "path/to/deck.typ" --png   # + 300-ppi PNGs only
python3 operations/scripts/export_deck.py "path/to/deck.typ" --keynote   # + <stem>.key with looping clips and notes (§ 4b)
```

Before delivery of an external talk, also confirm the § 2b spine: acknowledgements are slide 2, the hypothesis map lands within the first ~20%, every section opens with a recall, and no method slide shows the short title in its footer where a hypothesis tag belongs.

Treat any warning or error as a failed verification. A deck with a failing token, an undeclared sub-3:1 categorical mark, or a § 3a anti-pattern does not ship. Where an accent border or a hardcoded value genuinely encodes an empirical condition, declare it with a `// lint-ok: <what it encodes>` comment rather than relaxing the rule. After any change to `deck-kit.typ` or `deck-figures.typ`, compile `operations/templates/Touying Gallery.typ` and every template, then render the gallery and inspect it. A clean compile only proves the shared layer still builds; it says nothing about layout.

**What each check covers.**

- **`check_decks.py`** is the compile gate. Session closeout runs it, in default, handout, Pympress, and dark modes, on every deck the session's changes affect directly or through an imported kit, palette, figure, or asset file. `python3 operations/scripts/check_decks.py` sweeps every deck explicitly.
- **`typst compile` / `export_deck.py` / `check_decks.py`** catch code errors and compiler warnings, never overflow (§ 4).
- **`contrast_lint.py`** audits the palette file only: token tier floors and categorical-mark contrast on both canvases (full list in [references/typst-touying-reference.md](references/typst-touying-reference.md) § Colour tokens). It cannot see whether a deck draws the outline on a declared mark, or text legibility on a `container` fill.
- **`slide_lint.py`** catches the § 3a source anti-patterns and hardcoded hex in decks. It does not check layout, word budgets, or the § 2b spine.

**Rendered inspection is required for every finished deck**, because no automated check sees it:

- **Unintended extra pages.** The page count should equal the planned slides plus deliberate `uncover`/`pause` steps. An extra page that repeats a slide's headline and slide number is an overflowed body.
- **Clipping.** Nothing may be cut off at the right or bottom edge, including figures, tables, and wide grids.
- **Speaker notes.** Open the `— Pympress.pdf` and confirm each note ends inside its half-page.
- **Colour in context.** Outlines on declared low-contrast marks, legibility of text on filled containers, table rules, asset resolution, and the headline-evidence relationship.
