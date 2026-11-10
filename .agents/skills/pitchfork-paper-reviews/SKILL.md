---
name: pitchfork-paper-reviews
description: Review an empirical paper, preprint, draft abstract, methods section, protocol, or data-quality report as either a pretentious 2000s Pitchfork album review with a 0.0–10.0 score (Mode 1) or a Gordon Ramsay Kitchen Nightmares hygiene inspection of the raw data, blinks, sampling rates, and preprocessing (Mode 2), each ending in plain-language liner notes of real strengths and problems. Use when the researcher asks for a Pitchfork review, a Ramsay roast, a satirical journal-club recap, or a comic pre-submission read of a paper or draft. Do not use for a sober claim-level revision (use academic-writing) or a formal peer review.
---

# Pitchfork Paper Reviews

Two comic voices over one honest read. The satire is the wrapper; the **Liner Notes** at the
end are the deliverable. A review whose jokes are not anchored to something in the text has
failed, however funny it is.

## Mode selection

| The researcher says | Mode |
|---|---|
| "Pitchfork review", "rate this paper", "Best New Manuscript?", journal-club recap | **Mode 1: Pitchfork** |
| "Gordon Ramsay", "roast", "kitchen nightmares", "inspect the data", a data-quality or preprocessing report | **Mode 2: Ramsay** |
| Ambiguous | Mode 1 for theory, framing, abstracts, and whole papers; Mode 2 for methods, data pipelines, and QC. State the choice in one line and offer the other. |

The researcher may ask for both; write Mode 1, then Mode 2, then one shared set of Liner Notes.

## Workflow

1. Read the whole input before writing. For a vault paper, follow
   `.agents/rules/literature.md` (local wiki and trimmed MinerU first; never copy raw text).
2. List 3–6 real observations first, numbered O1, O2, …: strengths, weaknesses, and anything
   missing (no power analysis, sampling rate unstated, blinks not handled). Every joke must hang
   on one of these; tag it inline as `[O#]` when the link is not obvious. When the input defers a
   topic to another note ("see the Eye-Tracking Data Standard"), follow that link one hop before
   calling the topic Missing.
3. Write the review in the selected voice, then the Liner Notes.

## Mode 1: The 2000s Pitchfork Review

```markdown
# <First author> et al.: *<Title>*
**Label/Journal:** <real venue, or "Self-released on Overleaf" for a draft> · **Year:** <year or "Unreleased"> · **Length:** <pages or words>
**Score:** `<0.0–10.0>` · **Genre:** <invented subgenre, e.g. Post-Behavioral Psychophysics / Neuro-Indie>
<optional badge: **Best New Manuscript** (≥ 8.5) · **Preregistration of the Year** (a real prereg) · **Reissue** (replication)>

> *"<one pull-quote linking an ordinary methods choice to the human condition>"*

### The Review
<P1: a wandering, atmospheric opening (memory and late-capitalist attention, the sorrow of
forgetting) that arrives at the paper's real topic by the last sentence.>

<P2: methods and results as instrumentation. Linear mixed models have "acoustic warmth";
over-specified Bayesian priors are "glossy overproduction"; a 30 Hz tracker is "lo-fi."
Every metaphor maps to a real observation from step 2.>

<P3: the verdict, a backhanded compliment placing the work in the field's discography.>
```

**The score is real.** It reflects the step-2 read, not comic timing:

| Score | Meaning |
|---|---|
| 9.0–10.0 | Claims follow from the design; methods transparent; few or no Major issues |
| 7.0–8.9 | Sound core, one or two Major issues fixable in revision |
| 5.0–6.9 | Interesting, but a Major issue undercuts a headline claim |
| 3.0–4.9 | Conclusions outrun the evidence in several places |
| 0.0–2.9 | Reserve for work with fatal flaws; never for the researcher's own draft in progress without saying why |

Use one decimal place, and never a round number when an uneven one is honest (7.4, not 7.5).

## Mode 2: Gordon Ramsay Kitchen Nightmares

```markdown
# 🔪 KITCHEN NIGHTMARES: <Paper, dataset, or pipeline name>
**Establishment:** <lab, venue, or repo> · **Health inspection grade:** <A / B / C / SHUT IT DOWN>

### 🚪 Walk-in
<Ramsay enters and sees the first problem. Short sentences. ALL-CAPS outbursts, slammed lab
benches, and food metaphors aimed at the data and code, never at people.>

### 🧊 The Freezer (raw data inspection)
- **<Hygiene item>:** "<in-character line>" → <the real problem in one plain sentence>

### 🍳 The Pass (what is actually good)
<one grudging, sincere compliment; Ramsay always finds the one dish worth saving>

### 📋 Relaunch Menu
1. <concrete fix, most urgent first>
```

When the input describes data handling rather than containing data (a protocol, standard, or
analysis plan), inspect what it *requires* to be reported or done, say so in one line under the
header, and grade the provisions: **C** then means a gap that would let a main-outcome problem
pass unreported.

Inspect the hygiene items the input actually exposes:

- **Sampling and timing:** sampling rate stated and adequate for the measure (saccades vs.
  fixations), timestamp alignment between eye tracker, headset, and task events, dropped frames.
- **Blinks and track loss:** blink detection and padding, interpolation limits, track-loss
  thresholds, the share of trials or samples excluded.
- **Calibration:** validation accuracy and precision reported, recalibration policy, drift.
- **Preprocessing degrees of freedom:** fixation-detection algorithm and thresholds, AOI
  definitions fixed before analysis, filtering choices.
- **Exclusions and missingness:** rules stated in advance, counts per group (older vs. younger
  adults), missingness that differs by condition.
- **Model hygiene:** centering, random-effects structure, singular fits, outcome family.

Grade: **A** = no Major issues; **B** = Major issues with clear fixes; **C** = a Major issue
that affects the main outcome; **SHUT IT DOWN** = the data cannot support the stated analysis.
Catchphrase calibration: *"This sampling rate is RAW! It's still BLINKING!"*,
*"Look at this covariance matrix. It's FROZEN SOLID!"*, *"You haven't centered your Level-1
predictors, you DOUGHNUT!"* The insult lands on the predictor, not the author.

## Liner Notes (required, both modes)

Out of character, after the review:

```markdown
### 🎧 Liner Notes (the real review)
| ID | Observation | Type | Where | Suggested action |
|---|---|---|---|---|
| O1 | <plain statement> | Strength / Major / Minor / Missing | <section or line> | <what to do, or "keep"> |
```

## Boundaries

- Quote or paraphrase only what the input says. Never invent numbers, sample sizes, or results;
  an absent value is a "Missing" observation.
- Never fabricate a citation, quote, or real Pitchfork score. Real papers named in the notes
  come from local evidence.
- Satire targets the work. For external authors, mock choices, not people; for lab members'
  drafts, keep it affectionate and say so if a joke depends on an in-joke.
- These are internal artifacts. Do not post, send, or publish a review of someone else's work;
  if the researcher wants to share one outside the lab, flag that it should read as clearly comic and
  keep the Liner Notes attached.
- Scientific judgment calls the read surfaces (which model, which exclusion rule) go to
  `statistics` or `methods`; the review names them without deciding them.

## Verification

- The mode is stated or obvious from the header.
- Every metaphor or outburst traces to an observation in the Liner Notes.
- Mode 1 has a decimal score consistent with the score table; Mode 2 has a grade consistent
  with the grade rules.
- No number, citation, or quote appears that the input or local evidence does not contain.
