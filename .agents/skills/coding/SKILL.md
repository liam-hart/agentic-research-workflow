---
name: coding
description: "Implement, debug, review, or refactor readable and reproducible research software, analysis pipelines, vault automation, or Unity/C# experiment code. Use when the task changes or evaluates code; use statistics, methods, or experiment-design for unresolved scientific choices."
---

# Coding

Produce code that is correct, readable, and reproducible, or a technical review held to the same standard. Read the nearest `AGENTS.md` and project documentation before acting; those sources own repository-specific paths, tools, versions, scientific contracts, and authorization boundaries.

## Priorities

Optimize in this order:

1. Correctness and data integrity
2. Readability and transparency
3. Reproducibility
4. Maintainability and collaborator familiarity
5. Performance

Prefer the simplest conventional solution that satisfies the actual requirements. Do not introduce a lower-level language, performance-oriented library, custom framework, or clever abstraction without a demonstrated need. Profile before optimizing, and preserve a clear implementation unless measured performance makes a more complex one necessary.

## Language and package choices

Follow an established repository's stack. For new work, prefer mature, widely documented tools that cognitive-neuroscience students and collaborators are likely to recognize:

- **Python:** Default for automation, file parsing, preprocessing, array-oriented calculations, and general-purpose research tooling. Prefer `pandas`, `numpy`, `scipy`, `statsmodels`, `matplotlib`, and `seaborn` when they fit. Use `uv` with `pyproject.toml` for environments when practical.
- **R:** Default for tidy tabular analysis, statistical workflows, and publication-oriented figures when the project is not already committed to Python. Prefer `tidyverse` idioms and packages such as `readr`, `dplyr`, `tidyr`, `purrr`, `stringr`, `forcats`, and `ggplot2`; use `here` for project-relative paths and `renv` for reproducible environments when practical.
- **C#:** Use for Unity experiment logic and Unity-facing tooling. Follow the live project's architecture and package versions rather than assumptions embedded in this skill.
- **Shell:** Keep to small, legible orchestration tasks. Move substantial parsing or business logic into Python, R, or the repository's established language.

Do not choose Rust, C++, Polars, `data.table`, dense base R, or another less familiar alternative merely because it may be faster. Use one when the user requests it, the repository already relies on it, or profiling/technical constraints establish a meaningful benefit. Minimize dependencies, but do not reimplement a well-supported package solely to avoid adding one.

Choose packages based on fit, maturity, documentation, interoperability, and existing project use—not novelty. Verify current APIs and repository constraints before adding or upgrading dependencies.

## Human-readable implementation

- Use descriptive names drawn from the study and data model.
- Keep functions focused, with explicit inputs and outputs; separate I/O, transformation, analysis, and presentation where that improves clarity.
- Prefer clear intermediate variables and readable pipelines over nested expressions, metaprogramming, or compressed one-liners.
- Comment scientific intent, assumptions, units, and non-obvious decisions. Do not narrate obvious syntax.
- Add docstrings or equivalent documentation to reusable and public functions.
- Replace unexplained literals with named constants or configuration. Never hardcode participant identifiers, credentials, machine-specific paths, or protocol values that belong in configuration.
- Avoid speculative abstractions. Generalize after a repeated need is visible, not in anticipation of one.
- Match the surrounding style unless it is unsafe or conflicts with an explicit requirement.

## Research-data safeguards

- Treat raw data as immutable. Separate raw, interim, processed, and output artifacts according to project authority.
- Make participant, session, block, trial, condition, and provenance identifiers explicit where relevant.
- Validate pipeline boundaries: required columns, types, units, allowed values, uniqueness, row counts, join cardinality, missingness, and factor/category levels.
- Make exclusions and transformations explicit, countable, and reproducible. Never silently discard, repair, impute, or relabel observations.
- Represent an undefined statistic as missing, never as zero or another plausible value. A standard deviation, z-score, or proportion computed from too few observations is `NA`/`None`, so it cannot silently pass or trip a threshold downstream.
- Set and document random seeds when randomness affects reproducibility. In Python, pass an explicit generator (`np.random.default_rng(seed)`) through the functions that need it rather than seeding global state.
- Scripts that delete or overwrite outputs refuse unless the target resolves inside the expected output directory. Check containment on resolved paths, not string prefixes, before the first mutation, and never let a rebuild path reach raw data.
- Prefer human-inspectable CSV for small exchange and audit surfaces. Use Parquet or another typed format when schema preservation, scale, or an established pipeline justifies it.
- Keep private or identifiable data, credentials, and generated bulk data out of version control.

## Silent-failure traps in R and Python

These idioms turn common silent data errors into loud ones. Confirm the project's installed package versions before relying on a version-gated argument.

- **R joins (dplyr ≥ 1.1):** declare the expected cardinality with `relationship = "one-to-one"` or `"many-to-one"`, and use `unmatched = "error"` when every key must match, so a duplicated participant or trial key fails instead of multiplying rows.
- **R grouping (dplyr ≥ 1.1):** prefer per-operation `.by =` to a persistent `group_by()`, so a forgotten `ungroup()` cannot leak grouping into later steps.
- **R missing values:** pass `na.rm = TRUE` explicitly at each call where dropping missing values is intended. Do not load packages or set options that change `NA` defaults globally, because that hides an exclusion decision.
- **R name masking:** make masked functions explicit with `pkg::fun()` or a visible `conflicted::conflicts_prefer()` block at the top of the script.
- **pandas input:** declare `dtype=` and `usecols=` at the read boundary, and parse dates with `pd.to_datetime(..., format=...)` so malformed values raise rather than stay as strings.
- **pandas assignment:** assign through `.loc[mask, "col"]`. Chained assignment (`df[mask]["col"] = x`) does not modify the original frame under Copy-on-Write.

## Statistical boundary

Use the `statistics` skill when the task requires choosing, changing, or interpreting models, estimands, contrasts, random-effects structures, transformations, exclusion criteria, assumption checks, multiplicity corrections, effect sizes, or inferential reporting.

The coding skill may faithfully implement an already authorized analysis and test that implementation. It must not silently make scientific choices to resolve a coding problem. When the specification is ambiguous, surface the decision rather than encoding an arbitrary default.

Implementation requests remain owned by `coding` when the claimed approved specification or target repository cannot be found. Treat the missing authority as a stop condition: report what was searched and request the specification or repository without inventing, reopening, or silently transferring ownership of the implementation.

Use `methods` when implementation exposes an unresolved acquisition, measurement-validity, calibration, or preprocessing choice. Use `experiment-design` when it exposes an unresolved manipulation, assignment, counterbalancing, or trial-structure choice. Package names above are illustrations, never project requirements; current repository authorities and verified APIs prevail.

## Exploration and pipelines

- Use notebooks or interactive sessions for exploration. Move finalized preprocessing, scoring, models, tables, and figures into scripts or reusable functions when they become part of the reproducible pipeline.
- Prefer a simple documented entry point using the repository's existing runner; use a `Makefile` or equivalent only when it genuinely clarifies a multi-step workflow.
- Make failures informative and early. Preserve enough context to diagnose malformed inputs without exposing sensitive data.
- Keep generated outputs separate from source code and document which outputs are reproducible versus manually curated.

## Verification

Match verification to the risk and the repository's existing tooling:

- Test research-critical logic such as condition assignment, counterbalancing, scoring, exclusions, trial matching, centering, aggregation, and missing-data behavior with small synthetic fixtures and boundary cases.
- Before trusting a regression test, reintroduce the defect it guards and confirm the test fails, then restore the fix. For a guard or threshold, break it in both directions: it never fires, and it fires too often.
- Compare floating-point results with tolerances (`np.testing.assert_allclose`, `pd.testing.assert_frame_equal`, `testthat::expect_equal`), not exact equality.
- For Python, run repository-configured linting/formatting and `pytest` or the existing test framework. When Ruff is configured, run `ruff check` and `ruff format --check` on the relevant scope. If Ruff is unavailable, state that clearly and do not claim lint passed.
- New Python files must be lint-clean and format-clean. For existing files, compare before/after Ruff diagnostics: introduce no new findings, but do not turn pre-existing findings into an unrelated cleanup requirement. Never automatically reformat an existing script; report formatting opportunities and wait for explicit authorization.
- Ruff fixes require an explicitly bounded scope and focused diff review. Unsafe fixes are prohibited by default. A clean Ruff result does not establish semantic correctness, research-data integrity, or scientific validity.
- For R, parse or source changed scripts and use `testthat` for reusable or research-critical transformations when appropriate. Use project-configured formatting or linting if present.
- For Unity/C#, verify compilation and run the relevant EditMode/PlayMode tests or documented project checks. Do not hand-edit Unity serialized YAML.
- Check expected outputs and scientific invariants, not only exit codes. Review the focused diff and preserve unrelated work.
- Run focused checks first. Do not impose whole-repository cleanup or require a tool that the project does not use merely to complete a bounded change.

Before closeout, report what was verified, what was not, and any remaining scientific or runtime gate. Follow the repository's commit, push, documentation, and handoff rules; this skill grants no additional authority.

## Resources

- If the environment's instructions route shell commands through a token-saving proxy, follow that tool's own usage notes.
