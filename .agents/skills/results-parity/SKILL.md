---
name: results-parity
description: Audit every reported number in a manuscript, abstract, table, deck, or poster against the code output that produced it and against every other place the same number appears. Use when checking quantitative consistency before a submission or presentation; use reference-verification for bibliographic metadata and statistics for whether the analysis itself is appropriate.
---

# Results Parity

Produce a report-only audit showing whether each reported quantitative result matches its source output. Do not edit the manuscript, tables, figures, analysis code, or outputs during the audit.

## Establish the target

Identify the reporting surfaces in scope (manuscript sections, tables, supplement, abstract, slides, poster) and the analysis outputs that are the source of truth: saved model objects, result tables, logs, or a re-run of the named script. Record a snapshot identifier for each: a commit, content hash, or output timestamp.

When no source output exists for a reported number, the number is `UNMATCHED`. Never re-run an analysis with changed data, code, or settings to produce a match. A re-run is allowed only on the unchanged committed pipeline, and must be stated in the report.

## Two directions

- **Vertical:** each reported value against the output that produced it.
- **Horizontal:** each result against every other surface that reports it, such as the abstract against the results against the table against the slide. Build a claim list first, giving each result an ID and the locations where it appears.

Cover sample sizes and exclusion counts, descriptive statistics, test statistics and degrees of freedom, estimates and standard errors or confidence intervals, p-values, effect sizes, and percentages.

## Matching rule

A value matches when the source output, rounded to the precision reported, equals the reported value. Degrees of freedom, sample sizes, and counts must match exactly. A p-value reported as a threshold (`p < .001`) matches when the source value satisfies it. Any other tolerance is a statistical decision owned by `statistics`; do not invent one.

## Outcomes

- `PASS`: matches its source and every other appearance.
- `FAIL`: differs from its source or from another appearance.
- `EXPLAINED`: a difference with a concrete, named cause, such as a different sample, model specification, or rounding convention stated in the text. A vague or unverified cause stays `FAIL`.
- `UNMATCHED`: no source output could be located.

**Two-strikes rule:** when the same claim returns `FAIL` or `EXPLAINED` in two successive audit rounds, stop proposing text patches. Escalate it to the researcher as a structural question, because either the pipeline or the reporting is inconsistent.

## Report

Return summary counts and a compact table:

| ID | Result | Location | Reported | Source value | Source and snapshot | Outcome | Note or proposed correction |
|---|---|---|---|---|---|---|---|

## Boundaries

- No edits to manuscript text, tables, figures, code, or outputs. A proposed correction is not repair authority; the researcher approves a separate pass through `academic-writing` or `coding`.
- Parity is not validity. A matching number can come from the wrong model or the wrong exclusions; route those concerns to `statistics`.
- An open Word review round permits read-only auditing only.
- Report the surfaces and sources inspected, anything unreadable, and files left byte-identical.
