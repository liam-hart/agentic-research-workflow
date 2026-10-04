# Agent Skill Template

Use this template to author a portable Agent Skills `SKILL.md`. It follows the [Agent Skills specification](https://github.com/agentskills/agentskills); `skills-ref validate` from that repository checks the front matter. Copy the fenced block, replace every instructional placeholder, and remove sections the skill does not need. A short self-contained skill is preferable to an elaborate empty scaffold.

```markdown
---
name: skill-name
description: Perform a concrete capability and produce its useful outcome. Use when the user asks for the relevant task or supplies the relevant artifact. Do not use for the nearest commonly confused workflow.
---

# Skill Name

State the outcome this skill enables and the smallest amount of non-obvious context needed to use it well.

## Workflow

1. Read the live authority or input that owns task-specific facts.
2. Perform the work at the level of specificity justified by risk.
3. Verify observable outcomes and report unresolved decisions or gates.

## Boundaries

- State only constraints that materially change execution.
- Separate authority, permission, and scientific or editorial judgment.
- Stop when a missing decision would change the result; do not invent it.

## Resources

- For the conditional case, read [the focused reference](references/example.md).
- For repeatable deterministic mechanics, run `scripts/example.py`.

## Verification

- Name the checks that demonstrate the outcome rather than matching generated wording.
```

## Authoring contract

### Tier 1 — discovery metadata

- `name` is 1–64 lowercase letters, digits, and single hyphens; it matches the directory name.
- `description` says what the skill does and when it should activate. Add one exclusion only when it prevents a likely routing error.
- Keep automatic discovery unless the workflow is explicitly routine-only or helper-only in your skill registry. A sensitive action still belongs behind an execution-time authorization gate, not a hidden skill.
- Add optional `compatibility`, `metadata`, or `allowed-tools` only when a supported client and real requirement justify them. Do not add version or ownership metadata by habit.

### Tier 2 — activated instructions

- Include the desired outcome, live authority route, non-obvious workflow, real constraints, failure or stop behavior, and verification.
- Do not restate generic agent competence or repository policy already loaded from `AGENTS.md`.
- Use fixed steps only for fragile, safety-critical, or deterministic workflows. For judgment-heavy work, state decision criteria and gates.
- Keep the entrypoint under 500 lines and about 5,000 tokens. These are ceilings, not targets. Move detail that only some runs need into `references/`, and keep gotchas the agent must see before it hits them in `SKILL.md`.

### Tier 3 — conditional resources

- `references/` holds focused documentation, schemas, detailed modes, and substantial examples.
- `scripts/` holds repeatable deterministic mechanics with clear dependencies and errors.
- `assets/` holds material copied into output, not instructions for the model.
- `agents/` holds supported client metadata such as `openai.yaml`.
- Other directories are allowed when one of the four does not fit; prefer the four.
- Link resources directly from `SKILL.md` by a path relative to the skill root, and say when to read or run each one. Avoid reference chains deeper than one hop.
- Do not create placeholder directories, README files, or duplicate quick references.

## Workflow variants

- **Self-contained:** omit `Resources` when the complete useful contract is already short.
- **Routed:** keep mode selection in `SKILL.md`; load only the selected mode reference.
- **Interactive-gated:** name the decision the researcher must approve and stop until confirmation.
- **Routine-only:** state that the skill is unattended, cannot ask questions, and must use explicit fallback and no-write behavior from its routine authority.

## Review checklist

- Test a positive trigger and the nearest confusing negative trigger.
- Confirm permissions did not expand, project values remain in live authorities, and supporting files are still reachable.
- Run `python3 tools/list_skills.py`, your own registry check if you keep one, and task-specific behavioral checks.
