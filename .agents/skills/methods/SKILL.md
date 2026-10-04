---
name: methods
description: "Evaluate measurement validity, apparatus and acquisition tradeoffs, calibration, data quality, preprocessing principles, and methodological evidence. Use when the user is choosing or auditing how a construct is measured or a signal is acquired; use statistics for inferential models and experiment-design for study architecture."
---

# Methods

Use this skill for measurement and apparatus questions: whether a signal represents the intended construct, how acquisition choices affect validity, how to assess calibration and data quality, and how preprocessing choices alter the usable signal.

## Workflow

1. Read the live project protocol, preregistration, device documentation, and adopted quality rules before proposing values.
2. Define the construct, sensor or behavioral measure, units, timing reference, and expected artifact sources.
3. Separate validation from recalibration, artifact detection from exclusion, and preprocessing from inferential modeling.
4. Evaluate tradeoffs using the device, task, population, and scientific question. Treat thresholds and windows as project decisions requiring evidence and approval.
5. Preserve raw data and record transformations, quality flags, missingness, and provenance so alternative defensible pipelines can be compared.

Do not infer approval from a synthesis note, integration note, candidate analysis, prior study, or isolated search hit. A project-specific baseline, blink rule, interpolation gap, or analysis window is settled only when the live canonical protocol or analysis authority explicitly adopts it. If the request does not identify the project or the canonical authority is silent, present the decision criteria and stop for project approval without selecting numeric values.

For eye-tracking or pupillometry, read [references/eye-tracking-and-pupillometry.md](references/eye-tracking-and-pupillometry.md).

## Boundaries

- `experiment-design` owns manipulation, sampling, assignment, counterbalancing, and study architecture.
- `statistics` owns estimands, outcome and model families, inferential diagnostics, multiplicity, and sensitivity interpretation.
- `coding` implements approved acquisition and preprocessing contracts using current repository APIs.
- `academic-writing` drafts Methods prose from approved authorities.
- Evidence retrieval and full source ingestion belong to `zotero-manager` and LLM Wiki `$ingest`, respectively.

Do not freeze device APIs, sampling rates, calibration schedules, blink limits, interpolation gaps, baselines, analysis windows, AOIs, exclusions, or model formulas in reusable guidance. If the live authority is silent, identify the decision and evidence needed rather than choosing a universal default.

## Verification

- Each recommended value or rule cites the live protocol, preregistration, or device documentation that adopts it; anything else is presented as an open project decision.
- The construct, measure, units, timing reference, and expected artifact sources are stated.
- Raw data are preserved, and transformations, quality flags, missingness, and provenance are recorded.
