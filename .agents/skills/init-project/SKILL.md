---
name: init-project
description: Scaffold a new repository, or non-destructively retrofit an existing one, with the agent orientation quintet (AGENTS.md, ROADMAP.md, STATE.md, docs/DECISIONS.md, docs/PROJECT_HISTORY.md), harness adapters, and an archetype payload for a data pipeline, Unity/VR experiment, LaTeX manuscript, or reusable package. Use when initializing a project repository or auditing one for missing agent-orientation layers; use sync-docs for an already scaffolded manuscript's review round.
---

# Initialize Project

This skill leaves a repository with the same five-file orientation layer that agents can trust, plus a project-owned `AUTONOMOUS_WORK.md` companion. `STATE.md` says what to pick up next. `ROADMAP.md` gives the phases and what is out of scope. `docs/DECISIONS.md` records what is already settled. `docs/PROJECT_HISTORY.md` captures the project's epochal development arc. `AGENTS.md` sets the rules. The workload companion holds bounded agent execution cards and never replaces the board or task authority. Your `check_orientation.py` validator keeps the enabled contract honest after setup. The template contract is `operations/templates/init-project/README.md`.

## Choose the mode and archetype

| Archetype | Use for | Default board |
|---|---|---|
| `pipeline` | Scientific data, ETL, or modeling code | project board |
| `vr-experiment` | Unity/VR experiment with rig verification | project board |
| `manuscript` | LaTeX-canonical paper with a Word/Zotero review roundtrip | none |
| `package` | Reusable tool or library (no Unity UPM variant yet) | none |

Choose one primary archetype per repo. Do not scaffold into a notes vault; the engine refuses one.

## Workflow

1. **Authorize.** Writing to any repo other than the one you are working in needs the researcher's authorization in the current session. Read the target's nearest `AGENTS.md` for its commit, branch, and worktree policy. Its rules win over this skill.
2. **Greenfield** (new or empty directory):
   `python3 operations/scripts/init_project.py <target> --archetype <a> --greenfield [--name N] [--board-url URL | --board none] [--github-templates org|local]`
   Use `--github-templates local` only for repos that do not inherit organisation-level issue templates. A local `.github/ISSUE_TEMPLATE/` shadows every org default.
3. **Retrofit** (existing repo). Always run it in this order:
   1. Branch or worktree per the target's policy.
   2. Run `init_project.py <target> --archetype <a> --retrofit --report-path <scratch>/retrofit-report.md`. This writes nothing.
   3. Show the researcher the report. Every **conflict** row is the researcher's decision: `local` AGENTS blocks, adapters that carry policy, templates that shadow org defaults, and README prose that looks like roadmap or status. Do not resolve a conflict by editing. If the researcher declines a missing AGENTS block, pass `--skip-block <id>`. The manifest records it as `skipped_blocks`, so later runs never append that block.
   4. After approval, rerun with `--apply`, then again with `--apply` to confirm idempotence (zero diff).
   5. If the report says the decisions log lacks an index, run `operations/scripts/decisions_index.py <path> --write`.
   6. Open a PR.
   For a safe workload-only adoption that avoids unrelated quintet conflicts, use the
   same report-first sequence with `--workload-only`. It reports and applies only the
   workload companion, its marked `AGENTS.md` pointer, and a missing v1 capability.
   It adopts an existing document only when it already satisfies the workload contract;
   a generic TODO is never an equivalent queue.
4. **Manuscript archetype.** Before scaffolding, follow [the manuscript procedure](references/manuscript.md): pre-flight choices, Zotero export, build verification.
5. **Fill the first STATE.** Replace the template focus items with 1–3 real, anchored ones. Set `verified_against` to the `main` SHA you checked.
6. **Install the local gate** (not committed; see Verification).

## Boundaries

- The engine can only create files, record existing equivalent files in the manifest, or append marked blocks. Never hand-edit an existing file to force it into shape; propose the change instead.
- Never touch serialized engine assets (`Assets/`, `ProjectSettings/`, `Packages/`, `.unity`, `.prefab`, `.asset`, `.meta`).
- Item status lives on the project board. Never copy it into STATE or ROADMAP. STATE carries its own `## Open work` list only when `board = none`.
- Scientific decisions (exclusions, model families, protocol) stay in their own authority note outside the repo. A repo's decision log records implementation only.
- The engine never runs git write operations. Commits, pushes, and PRs follow the target's policy and the researcher's authorization.
- A queue's Ready state is eligibility evidence, not permission. Refresh source state,
  dependencies, tools, authority, and protected resources before execution; retain each
  project's review and rig gates.

## Verification

- After setup, `python3 operations/scripts/check_orientation.py --repo <target>` reports no FAIL.
- Legacy manifests receive an autonomous-work adoption warning until `[autonomous_work] capability = "v1"` is explicitly present. Enabled v1 queues are validated through the shared local engine when available.
- Retrofit: running `--apply` a second time produces no diff, and every original file's bytes are an exact prefix of its new version.
- Local gate: write `<target>/.git/hooks/commit-msg` as:
  ```sh
  #!/bin/sh
  exec python3 "<tooling-root>/operations/scripts/check_orientation.py" --repo "$(git rev-parse --show-toplevel)" --staged --commit-msg-file "$1"
  ```
  Then run `chmod +x` on it. When a triggered STATE update is genuinely unnecessary, the commit carries `State-Unchanged: <reason>`.
- CI does not enforce this unless the validator is available to the repo's CI. Where it is not, the gate is the local hook plus review.
