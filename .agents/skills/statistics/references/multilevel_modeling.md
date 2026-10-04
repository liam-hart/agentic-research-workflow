# Multilevel-modeling decision guide

This is the active distillation of the course materials you keep in this directory. Use it when clustered, longitudinal, crossed, or otherwise dependent observations are central to the request. Consult the course PDFs only when deeper explanation or provenance is needed; they are not a source of universal decision rules.

## Begin with design and estimand

- Identify how units were sampled, assigned, and repeatedly observed.
- Distinguish nested from crossed structures and record participant, item, session, site, wave, or other grouping factors that can induce dependence.
- State the target level for each contrast. A time-varying predictor can encode a within-cluster association, a between-cluster association, or both.
- Confirm that the design and observed variation identify the intended comparison before fitting a complex model.

## Within- and between-cluster effects

Centering is an interpretive choice, not a universal preprocessing rule. If within- and between-cluster associations are both relevant, represent them explicitly, often with a cluster-relative component and a cluster mean. Raw, grand-mean-centered, or cluster-mean-centered predictors can each be valid depending on the estimand, meaningful zero, and data structure.

For longitudinal or three-level data, do not mechanically repeat centering at every level. Define the comparison at each level, explain the intercept and slopes under the chosen coding, and verify that each component has adequate variation.

## Random effects and covariance

Use sampling, assignment, repeated-measure structure, and intended generalization to propose random intercepts, slopes, crossed effects, and covariance terms. Then assess whether the data support that structure using:

- convergence and optimizer diagnostics;
- singularity or boundary estimates;
- parameter uncertainty and stability;
- residual or predictive behavior; and
- sensitivity across scientifically defensible specifications.

Do not add or remove random effects solely because a likelihood-ratio or Wald-test p-value crosses a threshold. A converged model can still be weakly identified or scientifically inappropriate.

## Outcome family and link

Match the conditional outcome distribution to its support and generating process. Binary, count, ordinal, bounded, zero-inflated, continuous-positive, and approximately Gaussian outcomes require separate consideration. Inspect empirical and predictive behavior rather than applying a single family to all measures from the same task.

## Longitudinal structure

Treat time coding as part of the estimand. Decide whether change is linear, nonlinear, piecewise, event-centered, or otherwise structured from theory, design, and observed coverage. Separate within-person change from cohort or stable between-person differences where those comparisons matter. Account for sessions or waves only when the sampling and measurement structure support that level.

## Missing data

Describe missingness by outcome, predictor, cluster, occasion, and condition where relevant. Consider why values are missing and how that mechanism relates to the estimand. Complete-case analysis, likelihood-based estimation, multiple imputation, weighting, and joint or pattern-mixture approaches are conditional choices. Preserve auxiliary variables and missingness indicators needed for diagnosis, and use sensitivity analysis for assumptions that cannot be verified from observed data.

## Diagnostics and sensitivity

- Inspect outcome-appropriate residual and posterior or predictive checks.
- Examine influential observations and clusters without treating influence as automatic grounds for deletion.
- Check model calibration across scientifically important conditions and covariate ranges.
- Compare consequential choices involving coding, covariance, random effects, outcome family, missingness, and exclusions.
- Distinguish numerical problems from substantive model misspecification.

## Power and precision

Base planning on the target estimand, smallest scientifically meaningful effect or desired precision, numbers of units at each level, cluster-size imbalance, correlations, missingness, and uncertainty in those inputs. Simulation is often preferable when analytic formulas cannot represent the design. Report assumptions and ranges; do not use a universal power target or observed post-hoc power.

## Reporting

Report the estimand, fixed-effect coding, grouping structure, sample sizes at relevant levels, random-effects and covariance specification, outcome family and link, estimation method, software, convergence information, diagnostics, uncertainty, missing-data handling, and sensitivity results. Syntax belongs to the approved analysis implementation, not this reusable guide.
