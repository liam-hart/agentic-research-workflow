---
name: reviewer-2-boss-fight
description: Run a turn-based boss fight against "Reviewer 2, The Unappeasable Archmage of Small Effect Sizes" that stress-tests a manuscript section, abstract, specific aims, hypothesis, or talk argument, and ends each turn with a genuine methodological diagnostic. Use when the researcher asks to fight Reviewer 2, simulate hostile peer review, battle-test aims or an abstract, or harden a talk for Q&A. Do not use to draft a real response to reviewers (use cover-letter) or for a sober claim-level revision (use academic-writing).
---

# Reviewer 2 Boss Fight

Satire on top, real critique underneath. Reviewer 2 attacks in bad faith; the diagnostic
under every attack names the legitimate concern a fair reviewer would raise, where it bites
in the text, and what would fix it. The fight is worth running only if the diagnostics are
specific enough to act on.

## Inputs

- **Required:** the text under attack (pasted, or a vault path). Read all of it before the
  first volley. Every attack must quote or point to a specific line, claim, or omission.
- **Helpful:** target venue or audience (journal, fellowship panel, brown bag), and any analysis
  plan or preregistration the text relies on. Read a linked plan when the text cites it.
- With no text, ask for it. Never fight a summary of a document you have not read.

## Boss card

Print once at the start:

```markdown
## ⚔️ BOSS ENCOUNTER: Reviewer 2, The Unappeasable Archmage of Small Effect Sizes
**HP:** 10,000 / 10,000 · **Armor:** 99 (Immune to p < .05)
**Target:** <document or section> · **Arena:** <venue or audience>
**Known weaknesses:** a preregistered analysis plan; a power analysis with a stated SESOI; citing their own 2006 conference proceeding
```

HP is a progress bar for the researcher, not a score of the science. Total HP equals 1,000 × the number
of non-Cosmetic diagnostics found in Phase 1 (cap 10,000), so defeating the boss means every
real issue got a credible answer. A diagnostic is **Resolved** after a HIT or CRITICAL HIT;
anything less leaves it **Open**.

## The 3-phase turn loop

### Phase 1 — Boss Opening Volley

Launch 2–3 attacks per turn, strongest real vulnerability first. Draw flavor from the move
set below, but each attack carries a hidden diagnostic. Format:

```markdown
### 🔥 <Move name>
> "<In-character attack, quoting or pointing at the exact text>"

**🩻 Diagnostic (out of character):** <the legitimate concern> · **Where:** <section/line> · **Severity:** Fatal / Major / Minor
```

Severity: **Fatal** = the stated conclusion does not follow from the design or analysis as
written; **Major** = a panel or editor would require a change; **Minor** = clarity or
reporting. Scan at least these vulnerability classes and attack the ones the text actually has:

- **Estimand and inference:** the claim outruns the design (causal verbs on correlational data,
  between-person evidence for a within-person claim, mediation without temporal ordering).
- **Model structure:** omitted random slopes for within-subject predictors, uncentered Level-1
  predictors, unhandled nesting or crossed random effects, singular-fit risk.
- **Power and effect size:** no SESOI, power computed for an effect larger than the field's
  typical one, small-N interaction claims, multiplicity across many outcomes.
- **Covariates and exclusions:** covariates without a causal justification, post-treatment
  covariates, unstated exclusion rules, flexible preprocessing (researcher degrees of freedom).
- **Measurement validity:** gaze, accuracy, or RT measures standing in for a construct without
  the inference marked; reliability or calibration not reported.
- **Theory:** a competing account that predicts the same pattern; no result that would count
  against the hypothesis.
- **Feasibility (aims and proposals):** aims that depend on each other's success, timelines
  that ignore recruitment of older adults, missing pilot evidence.

Bad-faith flavor is allowed only on top of a real hit. An attack with no real diagnostic
underneath ("why not 7T fMRI on macaques?") is a **Cosmetic** move: label it Cosmetic, deal no
damage when it is parried, and use it at most once per turn for comic relief.

### Phase 2 — Player Action Menu

Offer the menu as a clickable choice (AskUserQuestion) when the harness supports it; otherwise
as a numbered list. Always include a free-text option for a real rebuttal.

| Action | What the researcher is actually doing | When it works |
|---|---|---|
| 🛡️ **Preregistration Shield** | Point to a prereg or analysis plan that fixed the choice in advance | Only if the plan exists and covers the attacked choice |
| 📜 **Cite Advisor's 2019 Paper** | Ground the choice in prior evidence or lab precedent | Only if the cited work actually supports the specific choice; stuns for 1 turn |
| 🙇 **Placation Hedge** | Concede and add a caveat or limitation | Partial damage for Minor issues; near zero against Fatal ones |
| 💥 **Table S1 Supplement Blast** | Add a robustness check, sensitivity analysis, or supplementary table | Full damage when the analysis would answer the concern |
| ✍️ **Free-text rebuttal** | The researcher's own argument | Judged on substance like any other move |

Stop and wait for the researcher's move. Never play his turn for him. In a non-interactive request
("just run the whole fight"), lift the 2–3 attack cap: attack every diagnostic once, give each
the single best honest defense, label the round **Simulated**, and still produce the
diagnostic table. A simulated defense proves nothing, so every simulated row stays **Open**
with its fix written as the condition for closing it; only a move the researcher actually makes can mark
a row Resolved. The Preregistration Shield works only when the text cites the plan or the researcher
names it; never assume a preregistration exists.

### Phase 3 — Damage Calculation & Methodological Diagnostic

Judge the move against the diagnostic, not the flavor:

```markdown
### 🎲 Damage Roll
**Move:** <action> · **Result:** CRITICAL HIT / HIT / GLANCING BLOW / MISS / BACKFIRE
**Damage:** <n> · **Boss HP:** <remaining> / <total>

**Why:** <one or two sentences on whether the defense resolves the concern>
**Joke aside:** <the concrete fix: the analysis to run, the sentence to change, the citation to verify>
```

- **CRITICAL HIT (1,000):** the defense fully resolves the concern and the fix is concrete.
- **HIT (600):** resolves it, but the text still needs the stated change.
- **GLANCING BLOW (200):** a hedge or partial answer; the concern survives for a sharper panel.
- **MISS (0):** the defense does not address the concern.
- **BACKFIRE (boss heals 300):** the defense creates a new vulnerability (a cited paper that
  contradicts the claim, a robustness check that would invite multiplicity).

Then the boss counterattacks with the next real vulnerability. End the fight when every
diagnostic has been answered, the boss reaches 0 HP, or the researcher retreats.

## Victory or retreat screen

Always end with the actionable record, out of character:

```markdown
## 🏆 VICTORY (or 🏳️ TACTICAL RETREAT)
| # | Diagnostic | Severity | Where | Status | Revision to make |
|---|---|---|---|---|---|
| 1 | <concern> | Major | <section> | Resolved / Open | <specific change> |

**Loot:** <one line of flavor> · **Next skill:** statistics / experiment-design / theory / academic-writing, if an Open item needs one
```

## Boundaries

- **Never fabricate a real citation.** Reviewer 2's self-citations use the fictional
  "Abernathy, Jenkins, & Abernathy (2004, 2006, 2011)" and are marked *(fictional)* on first use.
  Any real paper named in a diagnostic must come from the vault, LLM Wiki, or Zotero per
  `.agents/rules/literature.md`; otherwise say "check the literature on X" without a citation.
- Diagnostics report what the text says. Do not invent results, Ns, or effect sizes the text
  does not contain; an absent number is itself a diagnostic ("no power analysis reported").
- Hostility targets the manuscript, never the researcher, his collaborators, or named lab members.
- The output is a rehearsal artifact. Do not edit the source document; route accepted
  revisions to `academic-writing` or the owning project note when the researcher asks.
- Unresolved statistical or design choices go to `statistics` or `experiment-design`; the fight
  surfaces them but does not decide them.

## Move set (flavor library)

- **The Self-Citation Barrage** — the paper ignores the reviewer's own framework. Real hit
  underneath: missing a genuinely relevant literature or competing account.
- **The Impossible Apparatus Shift** — demands 7T fMRI, intracranial recordings, or a chin rest
  in VR. Real hit underneath: a measurement-validity or calibration gap, or usually Cosmetic.
- **The Ecological Paradox** — too artificial to be real memory, too realistic to be
  controlled. Real hit underneath: the confound the design does not rule out.
- **The Unmotivated Spline Demand** — zero-inflated GAMM with crossed random slopes on cubic
  splines. Real hit underneath: a mis-specified random-effects structure or outcome family.
- **The Small-Effect Curse** — "an effect this small cannot exist." Real hit underneath:
  power, SESOI, or precision of the estimate.
- **The Fourteen-Day Resubmission** — "revise within 14 days." Real hit underneath:
  feasibility or timeline in aims.

## Verification

- Every non-Cosmetic attack has a diagnostic with a location and severity.
- Every damage roll states why the defense did or did not resolve the concern.
- The fight ends with the diagnostic table; no real citation appears that was not checked
  against local evidence.
