# Typographic and layout anti-patterns

The detail behind `presentations` § 3a. Section numbers below refer to `SKILL.md`.
Your slide linter (for example `operations/scripts/slide_lint.py`) should fail closed on the banned patterns; a deck that trips it
does not ship.

## Banned outright

| Pattern | Why it fails here |
|---|---|
| **Eyebrow / kicker headers** — small, all-caps, letterspaced, accent-coloured micro-text above a title or column | A SaaS landing-page device. It adds a perceptual element (Naegle Rule 4) that carries no spoken beat, and it puts the *least* important text in the *most* saturated colour. No `label-head`-style helper, ever. |
| **`upper()` / all-caps** for labels or body | Capitals slow reading by removing word-shape cues; Naegle Rule 7 names ALL CAPS explicitly. Sentence case, or title case for a proper noun. |
| **`tracking:` letterspacing** | Decoration with no semantic job. |
| **Emoji** | Not an academic register, and it renders unpredictably. |
| **Hardcoded hex in a deck** | Bypasses the contrast contract. Every colour resolves through `theme-colors.typ`. |

## Constrained, not banned

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

## Typographic hierarchy

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
