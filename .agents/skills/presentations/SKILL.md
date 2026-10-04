---
name: presentations
description: "Draft native Touying (Typst) research presentations from a user-approved narrative arc using assertion-evidence headlines, sparse audience-facing copy, and a paired companion explainer when needed. Use when creating research talks, journal clubs, and synthesis decks; use a document skill for PowerPoint or native Google Slides artifacts."
---

# Presentations

Produce a native Touying research deck, built from literature, project material, or synthesis notes on a narrative arc the user has approved, in which each slide states one assertion and shows its evidence. Native Touying `.typ` source is canonical; PDF is a generated export. Existing Marp decks are historical artifacts, not templates for new work.

## 1. Select the Touying template

- `operations/templates/Touying Presentation - Research Talk.typ` — one assertion and one primary item of evidence per slide.
- `operations/templates/Touying Presentation - Journal Club.typ` — one-paper background, question, methods, results, interpretation, and critique.
- `operations/templates/Touying Presentation - Synthesis.typ` — a multi-paper lineage that lands on a gap, proposal, or critical test.
- `operations/templates/Touying Presentation - Conference Talk.typ` — 12–15 minutes of results: the full hypothesis spine, weighted toward figures, closing on one contribution.
- `operations/templates/Touying Presentation - Lightning Talk.typ` — 5 minutes, 4–6 slides: one hypothesis, one key result, a take-home with contact.
- `operations/templates/Touying Presentation - Prelim Talk.typ` — prelim or committee: a framework, an aims overview, a hypothesis map per aim, a timeline, and committee questions.
- `operations/templates/Touying Presentation - Lab Update.typ` — lab-meeting progress: status, one result or demo, the next milestone, and asks. No spine.

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

**Fixed opening.** Title → **acknowledgements** → 1–2 motivation slides → theoretical tension → hypothesis map. Acknowledgements always follow the title so they cannot be skipped for time. The map lands within the first ~20% of the talk.

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
4. Put only audience-facing material on slides. Short delivery cues may go in `#speaker-note[..]` (§ 5); extended explanation belongs in the companion document.
5. Use descriptive relative asset paths and preserve source provenance in comments without turning those comments into presenter notes.

## 3. Assertion-evidence contract

- Each substantive slide headline is a complete declarative sentence stating the takeaway. Use a neutral descriptive sentence when the evidence does not support a stronger claim.
- Do not use rhetorical questions, teasers, colloquial titles, em-dash punchlines, self-congratulation, or stock AI phrasing.
- Keep a headline concise enough to remain on one line when practical (about 10–12 words or 80 characters).
- Keep audience-facing explanatory copy below 20 words per slide whenever the evidence can carry the argument. Labels, citations, table cells, and axis text do not count toward that budget.
- Prefer one primary chart, diagram, image, comparison, or formal table over bullet-heavy prose.
- The rhetorical-question ban above applies to slide headlines, not to the deck title.

## 3a. Typographic and layout anti-patterns

A recurring set of stock visual habits makes a deck read as marketing collateral rather
than as academic evidence. Your slide linter (for example `operations/scripts/slide_lint.py`) should fail closed on them; a deck
that trips it does not ship.

### Banned outright

| Pattern | Why it fails here |
|---|---|
| **Eyebrow / kicker headers** — small, all-caps, letterspaced, accent-coloured micro-text above a title or column | A SaaS landing-page device. It adds a perceptual element (Naegle Rule 4) that carries no spoken beat, and it puts the *least* important text in the *most* saturated colour. No `label-head`-style helper, ever. |
| **`upper()` / all-caps** for labels or body | Capitals slow reading by removing word-shape cues; Naegle Rule 7 names ALL CAPS explicitly. Sentence case, or title case for a proper noun. |
| **`tracking:` letterspacing** | Decoration with no semantic job. |
| **Emoji** | Not an academic register, and it renders unpredictably. |
| **Hardcoded hex in a deck** | Bypasses the contrast contract. Every colour resolves through `theme-colors.typ`. |

### Constrained, not banned

- **Borders.** A stroked box must have a real containment job — an image well, a nested
  table, a quoted definition. Grouping by whitespace, grid gutter, and alignment is the
  default; a border is what you reach for when whitespace has already failed. When a box is
  warranted, it takes a `0.5pt` hairline at `P.border-element`, not an accent.
- **Accent colour.** `P.accent.*` encodes an empirical condition, hypothesis, or
  experimental factor the audience must track across slides — condition A versus condition B,
  one model against its alternative. It does not tag generic furniture ("Where this goes
  next", "Open question", "Our study"), and it never assigns a different hue per panel to
  make a grid look varied. Rainbow category tagging teaches the audience that colour means
  nothing, which spends the one channel that should have meant something. Every accent
  encoding is doubled by a text label, per § 4a.
- **Cards.** Unboxed panels are the default. A `card`/`container` is one archetype slot,
  not the wrapper for every thought on the slide. Three bordered boxes in a row is a grid
  with extra ink.

### Typographic hierarchy

Rank by size, weight, and position. Colour is not a hierarchy device; it is an encoding
device.

| Role | Size | Weight | Token |
|---|---|---|---|
| Slide headline | 1.1em (set by the `heading.where(level: 2)` rule) | bold | `P.text-headline` |
| Panel / column heading | **≥ 1em** — body size or larger, never smaller | bold | `P.text-headline` |
| Body copy | ≤ 0.85em | regular | `P.text-primary` |
| Caption, qualifier, citation | ~0.7em | regular | `P.text-secondary` |
| Condition label (accent-carrying) | matches its neighbour's tier | bold | `P.accent.<hue>.emphasis` |

A subheading reads as a subheading because of weight and position. If it needs capitals,
letterspacing, and colour to be legible as a heading, it is too small.

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
of the headline, a summary, a motivational sentence), it belongs in the companion
explainer's spoken narrative, not on the slide. If nothing qualifies, leave the band empty.

| Keep | Cut (move to narration) |
|---|---|
| "Stimuli are sized to fill the screen so every item is equally visible." (design rationale) | "Rather than controlling for this variability, we use it." (spoken framing) |
| "Predicted, not observed. Two flat, parallel lines would be the null result." (null pattern) | "We carry this logic to the next experiment." (transition) |
| "The fine-grained scale connects to high-similarity lure tests in the pattern-separation literature." (provenance) | "One continuous session: study twice, then test three ways." (restates the timeline) |

The helper is `context-line(body)`.

## 3c. Deck and talk titles

The researcher's approved preferences. The deck title is also the title submitted to seminar organizers, so the same rules apply to both.

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

Pin the deck import to `@preview/touying:0.8.0`. The supported compiler baseline is Typst 0.15.1. An older delivered deck may stay pinned to its original Touying version as a historical record.

Touying 0.8.0 features in use:

- **Handout export.** `--input export-mode=handout` collapses every animation to its final state, one page per slide. It is the version to share after a talk. `export_deck.py` (§ 6) writes it alongside the presentation PDF.
- **Speaker notes for Pympress.** `#speaker-note[..]` is invisible on the slide. `--input notes=pympress` (which `deck-kit.typ` reads) draws each slide's notes on the right half of a doubled page, the layout the Pympress presenter app splits between laptop and projector. See § 5 for what belongs in a note.
- **Parked slides.** Label a heading `<touying:never>` to keep a cut or draft slide out of every export without commenting out its markup. Backup slides after the discussion stay live.
- **Overflow is not a compiler signal.** With Touying 0.8.0 and Typst 0.15.1, a body taller than the slide silently continues onto extra pages, a box wider than the slide is silently clipped at the page edge, and an over-long `#speaker-note` is silently clipped on the Pympress page. All three compile with exit 0 and no warning, so neither the compile step nor `export_deck.py` catches them. Only the rendered-PDF inspection in § 6 does.

Not adopted: article mode (it linearizes the deck into a rough A4 document; the companion explainer stays the prose surface), and the new animation entry points (`animate`, `touying-render`, element-level `touying-recall`), which solve nothing current. The hypothesis map uses a kit function rather than `touying-recall` because each recall changes its focus.

## 4a. Colour authority

Every deck draws colour from `operations/templates/theme-colors.typ`, a contrast-first token set generated as a function of background and a target WCAG 2.1 ratio, not chosen by hand. `deck-kit.typ` imports it and exposes `THEME` and the palette `P`; decks compile with `--root .` and switch to a dark room with `--input theme=dark`, which re-solves every token against the dark canvas. Each token sits at a fixed tier: `surface-subtle` ≥ 1.1:1, `border-element` ≥ 3:1, `text-secondary` ≥ 4.5:1, `text-primary` ≥ 7:1, `text-headline` ≥ 10.5:1, with accent hues (`blue teal orange purple red`) supplied at matched 3:1 / 4.5:1 / 7:1 variants. Headlines use `text-headline` so the assertion survives degraded projection and reduced audience contrast sensitivity. Categorical data marks use the Okabe–Ito set (`cat`) verbatim; any mark in `cat-needs-outline-on-light` carries a 0.75pt `text-primary` outline, and every categorical encoding is doubled by a non-colour channel — marker shape, dash pattern, or a direct label. Regenerate tokens with your palette generator script; never hand-edit a hex.

## 5. Companion explainer

A synthesis or method-narrative deck pairs with a Markdown explainer that mirrors the deck section by section. The deck comment header records `companion: "[[... — Explainer]]"`; the explainer frontmatter records `deck: "[[...]]"`. Research talks and journal clubs may also use companions when the slide density contract would otherwise be violated.

The companion is presenter-facing by design and may contain delivery notes, elaboration, source verification, and native Obsidian callouts that do not belong on slides.

**Speaker notes versus companion.** The companion holds the full spoken narrative and is where narration is drafted and reviewed. `#speaker-note[..]` holds only the short cue the researcher needs to glance at mid-talk in Pympress (a name to thank, a time check, the one point a slide must land, the hypothesis to name aloud). Keep each note to a line or two; never paste companion narration into a note.

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
```

Before delivery, also confirm the § 2b spine: acknowledgements are slide 2, the hypothesis map lands within the first ~20%, every section opens with a recall, and no method slide shows the short title in its footer where a hypothesis tag belongs.

Treat any warning or error as a failed verification. A deck with a failing token, an undeclared sub-3:1 categorical mark, or a § 3a anti-pattern does not ship. Where an accent border or a hardcoded value genuinely encodes an empirical condition, declare it with a `// lint-ok: <what it encodes>` comment rather than relaxing the rule. After any change to `deck-kit.typ` or `deck-figures.typ`, compile `operations/templates/Touying Gallery.typ` and every template, then render the gallery and inspect it. A clean compile only proves the shared layer still builds; it says nothing about layout.

**What each check covers.**

- **`check_decks.py`** is the compile gate. Session closeout runs it on every deck affected by the session's changes (the deck itself, or a kit, palette, figure-helper, or asset file it imports or reads), in default, handout, Pympress, and dark modes. `python3 operations/scripts/check_decks.py` sweeps every deck explicitly.
- **`typst compile` / `export_deck.py` / `check_decks.py`** catch syntax and code errors and compiler warnings. They do not catch overflow (§ 4): extra pages, right-edge clipping, and clipped speaker notes all compile cleanly.
- **`contrast_lint.py`** parses the live `theme-colors.typ` and fails a token below its tier floor, a categorical mark below 3:1 on the light canvas that `cat-needs-outline-on-light` does not declare, a declaration naming no `cat` mark, or a mark below 3:1 on the dark canvas. It audits the palette file only. It cannot see whether a deck actually draws the 0.75pt outline on a declared mark, or how legible a colour is on a surface other than its canvas (for example, text on a `container` fill).
- **`slide_lint.py`** catches the § 3a source anti-patterns and hardcoded hex in decks. It does not check layout, word budgets, or the § 2b spine.

**Rendered inspection is required for every finished deck**, because no automated check sees it:

- **Unintended extra pages.** The page count should equal the planned slides plus deliberate `uncover`/`pause` steps. An extra page that repeats a slide's headline and slide number is an overflowed body.
- **Clipping.** Nothing may be cut off at the right or bottom edge, including figures, tables, and wide grids.
- **Speaker notes.** Open the `— Pympress.pdf` and confirm each note ends inside its half-page.
- **Colour in context.** Outlines on declared low-contrast marks, legibility of text on filled containers, table rules, asset resolution, and the headline-evidence relationship.
