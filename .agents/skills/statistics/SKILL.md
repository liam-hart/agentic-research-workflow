---
name: statistics
description: "Guide estimand-first statistical design, diagnostics, uncertainty, sensitivity, power or precision, and quantitative interpretation for behavioral and cognitive-neuroscience research. Use when the user must choose, evaluate, or interpret an estimand, model, contrast, diagnostic, exclusion consequence, or quantitative claim."
---

# Statistics

Produce an estimand-first statistical recommendation or interpretation for a behavioral or cognitive-neuroscience analysis: the model, contrast, diagnostics, and reporting that fit the design. The focus is on transparent, reproducible quantitative science aligned with open-science best practices.

## Guidelines

### 1. Estimand and model specification

Before naming a test or model, define the population, units, outcome, exposure or manipulation, comparison, and estimand. Identify sampling, assignment, repeated measures, nesting or crossing, and the outcome's support. Distinguish within-person from between-person questions. Do not choose a procedure from the number of groups or a single assumption-test p-value. Counts and continuous-positive response times do not automatically share a model family.

Questions that contrast a trial-level or within-person association with a person-level or between-person association are statistical estimand questions. Use `statistics` as the primary skill even when the variables are theory-laden constructs; use `theory` only as a companion when the request also asks what mechanisms mean.

### 2. Reporting standards

Match the report to the estimand, fitted model, venue, and audience. Usually report the estimate or contrast, its uncertainty, the scale on which it is expressed, and enough model information to reproduce the claim. Include test statistics, degrees of freedom, exact *p*-values, standardized effects, variance components, descriptive summaries, or model-fit quantities when they are meaningful for that analysis—not as a fixed checklist. State interval level and correction conventions explicitly.

Treat effect magnitude and uncertainty as primary evidence. Do not let a thresholded *p*-value substitute for quantitative interpretation, and do not force every design into a test-to-effect-size lookup table.

For a figure or legend reporting audit, explicitly reconcile the observation and analysis units, biological/participant versus technical replication, exact `n` and exclusions, paired or repeated status, centre and uncertainty/error-bar definition, model/test and contrast, multiplicity convention, and the source-data mapping. Missing design or reporting facts become `AUTHOR_INPUT_NEEDED`; do not fill them from visual convention. Use `scientific-figures` for panel architecture, encoding, and rendered QA after the quantitative contract is settled.

### 3. Researcher Degrees of Freedom (Simmons et al., 2011)

- **Pre-register** outcomes, covariates, and exclusion criteria before data collection.
- Distinguish *a priori* confirmatory analyses from post-hoc exploratory analyses explicitly in the paper.
- Report all DVs collected, not just significant ones.
- Define the family of claims before choosing a multiplicity strategy; Bonferroni, FDR, hierarchical modeling, or no adjustment may be appropriate in different decision contexts.
- Never selectively report subsets of the data to sharpen a *p*-value.

### 4. Assumption Checks

Diagnose the fitted model and measurement process rather than applying a universal checklist. Use outcome-appropriate residual or predictive checks, influence assessment, convergence and singularity checks, and plausible alternative specifications. Treat extreme observations according to provenance and validity; never delete valid observations by a universal SD or IQR rule. Use sensitivity analyses when defensible choices could change inference.

### 5. Eye-Tracking & Physiological Data

`methods` owns measurement validity and preprocessing principles for pupillometry and gaze. This skill evaluates their inferential consequences and chooses an outcome and dependence model only after the estimand and measurement structure are known.

### 6. Drafting Quantitative Findings

Build a results sentence around the scientific contrast:
> "[Outcome] was estimated to be [direction and magnitude] under [comparison], [estimate and interval on the stated scale]; [model or test quantity] where it helps the reader evaluate the claim."

Do not infer absence from a large p-value. Use intervals, equivalence tests, or model-comparison reasoning when scientifically justified. Plan sample size from the smallest effect or precision that matters, the actual dependence structure, attrition or missingness, and uncertainty in those inputs; never report observed post-hoc power.

### 7. Multilevel Modeling (MLM / LME) Guidelines

Represent dependence supported by sampling and assignment. Separate within- and between-cluster estimands only when the question requires it; centering is an interpretive choice, not a universal recipe. Use design, intended generalization, convergence, singularity, predictive or residual checks, and sensitivity analyses to assess random-effects and distributional choices. Read [multilevel_modeling.md](references/multilevel_modeling.md) for the conditional decision guide.

### 8. Signal detection

Recognition sensitivity is commonly \(d' = z(HR)-z(FAR)\). Rates of exactly 0 or 1 require an explicit correction convention appropriate to the design; surface and document that choice before implementation. Keep response bias or criterion separate from sensitivity.

## Boundaries

`experiment-design` owns manipulation, sampling feasibility, assignment, and counterbalancing. `methods` owns measurement and preprocessing validity. `coding` implements approved specifications and must return unresolved scientific choices. `academic-writing` owns prose.

## Verification

- The estimand, population, units, and comparison are stated before any model or test is named.
- The estimate or contrast is reported with its uncertainty and scale, and with enough model information to reproduce the claim.
- Diagnostics match the fitted model, and sensitivity analyses are used where defensible choices could change the inference.
- Confirmatory and exploratory analyses are labelled as such.
- In a figure or legend reporting audit, missing design or reporting facts are marked `AUTHOR_INPUT_NEEDED`, not filled in.

---

## Resources

Read only the reference needed for the current decision:

- [multilevel_modeling.md](references/multilevel_modeling.md) — estimand, dependence, diagnostics, and sensitivity guide for multilevel models.

The papers below are other people's published work and do not ship with this kit. Add your own copies under `references/` with these file names.

- `references/cumming-2013-the-new-statistics.pdf` — "The New Statistics" (Cumming, 2013): effect sizes, CIs, and meta-analytic thinking as core paradigm.
- `references/simmons-et-al-2011-false-positive-psychology.pdf` — False-Positive Psychology (Simmons et al., 2011): researcher degrees of freedom and pre-registration rationale.
- `references/fpsyg-04-00863.pdf` — Open Science collaboration paper on reproducibility.
- `references/nrn3475.pdf` — Statistical power and reproducibility in neuroscience.
- `references/quant-table-*.pdf` — Quick-reference quantitative decision tables (effect sizes, tests, thresholds).
