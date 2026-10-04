---
name: experiment-design
description: "Design behavioral or cognitive-neuroscience study architecture, including manipulation, sampling, assignment, counterbalancing, validity threats, feasibility, and preregistration decisions. Use when the user is choosing or evaluating how a study is structured; use methods for measurement and statistics for estimands or models."
---

# Experiment Design

Use this skill to turn a theoretical question into a feasible study architecture. Keep it separate from measurement engineering and statistical model selection.

## Guidelines

### 1. Study Design Principles

- Choose within-, between-, mixed-, or other assignment structures from carryover, contamination, learning, burden, variability, and feasibility; no design is universally preferred.
- **Between-subjects** factors (e.g., Age group: Young vs. Older Adults) require randomization across counterbalancing conditions to prevent confounds.
- **Factorial designs:** explicitly specify all factors (e.g., 2 Age × 2 Condition × 3 Trial-Type) and whether each is within or between subjects.
- Design randomization and counterbalancing around the actual nuisance dimensions. Verify balance, constraints, and failure behavior with simulation when useful.

### 2. Scientific interfaces

Coordinate with `theory` on the critical test, `methods` on whether apparatus and measures resolve the construct, and `statistics` on estimands, precision, dependence, and analysis assumptions. Route implementation to `coding` only after scientific choices are approved.

### 3. Validity and feasibility

Identify construct, internal, external, and statistical-conclusion validity threats. Specify manipulation checks and controls where informative. Evaluate recruitment, burden, accessibility, staffing, hardware, attrition, and failure recovery.

### 4. Ethics and preregistration

- Determine the applicable ethics, registration, repository, and timing requirements from the live institution, venue, protocol, or project authority. OSF is one possible host, not a universal requirement.
- Record adopted hypotheses, outcomes, sampling logic, assignment, exclusions, stopping rules, and deviations in the live protocol or preregistration. `statistics` owns quantitative planning assumptions; do not freeze power or alpha defaults here.

## Boundaries

This skill does not own device APIs, acquisition settings, calibration or preprocessing thresholds, inferential models, effect-size conventions, d-prime scoring, code, or manuscript prose.

## Verification

- Every factor is named with its levels and its within- or between-subjects status.
- Each randomization or counterbalancing choice names the nuisance dimension it controls.
- Validity threats and feasibility limits are stated, with a manipulation check or control where one is informative.
- Ethics, registration, and timing requirements come from a named live authority.
- Nothing owned by `theory`, `methods`, `statistics`, or `coding` was decided here.
- For a complete proposed study, the design review checklist was applied.

---

## Resources

- For a complete proposed study, read [references/design-review-checklist.md](references/design-review-checklist.md).
