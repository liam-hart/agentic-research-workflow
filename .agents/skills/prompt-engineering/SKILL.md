---
name: prompt-engineering
description: Design, revise, or evaluate reusable prompts and agent instructions for a defined task and harness. Use when prompt behavior, model calibration, or prompt evaluation is the deliverable; do not use for ordinary task execution that merely needs a clear request.
---

# Prompt Engineering

Produce a small, testable prompt contract that improves a named workflow without silently changing its authority, side effects, or definition of success. Treat prompts as versioned operational artifacts, not as a substitute for repository policy, tool permissions, or evaluation.

## Trigger boundaries

Use this skill for:

- A system, developer, user, reusable API, skill, or agent-role prompt that must be created, revised, migrated, or diagnosed.
- A request to calibrate a task across models or harnesses, reduce prompt drift, define an output contract, or build a representative prompt evaluation.
- A prompt that controls tools, delegation, context, safety boundaries, or structured outputs.

Do not use this skill for:

- Completing the underlying research, writing, coding, or vault task when no reusable prompt behavior is being designed. Use the domain skill instead.
- Changing model defaults, sandbox approvals, API parameters, client configuration, or tool permissions. Those are harness/configuration decisions, not prompt edits.
- Inventing a model capability, availability, version, or effort setting. Read current harness documentation when that fact matters.

## Authority and setup

1. Identify the owner of the task facts: repository `AGENTS.md`, a project authority, API schema, live harness configuration, or the supplied artifact. Prompt text may restate a constraint for the task, but it cannot grant permission or override that authority.
2. Define the observable target before drafting: representative input, desired artifact or answer, allowed evidence/tools, prohibited side effects, failure/stop behavior, and how success will be checked.
3. Separate durable behavior from task specifics. Put stable role, tone, safety, and output conventions in the system/developer or repository layer; put the immediate goal, supplied evidence, and requested deliverable in the user/task layer. Keep secrets out of both.
4. Inspect the active model and harness from live status/configuration. A prompt should not assume that an API feature is exposed by a CLI, or that a CLI capability is an API guarantee.

For local policy and model adaptation, read your own per-model prompting notes and delegation protocol, if you keep them. Those notes own local policy; the mirrored official pages below are dated evidence, not a claim about current availability.

## Construct the prompt

Use the smallest structure that makes the task testable. Usually include only the components that resolve a real ambiguity:

1. **Goal and deliverable** — name the outcome, audience, scope, and response shape.
2. **Grounded context** — supply authoritative facts or file paths, label uncertain material, and delimit quoted/input data from instructions.
3. **Constraints and authority** — state side-effect limits, source requirements, non-negotiable safety rules, and what remains a user decision.
4. **Method only when needed** — specify a sequence when ordering is required or a fragile procedure must be followed; otherwise request outcome and criteria rather than micromanaging hidden reasoning.
5. **Tools and delegation** — name a tool only when its use is necessary, state what it may access, and give each subagent a bounded, independently verifiable slice. A prompt never expands authorization for external writes, commits, publication, forks, or nested delegation.
6. **Output and stop contract** — specify schema, length, citations, uncertainty reporting, and the condition that requires a question rather than a guess.

For a lead-tier model, use a lightweight Lead Brief: state the outcome, authoritative context paths, real constraints, and open questions, but do not micromanage architecture, prescribe a file-by-file execution sequence, or pre-resolve an uncovered decision. Sol, Opus, Fable, or Pro retains lead judgment; bounded worker prompts are appropriate only after the approach is settled.

Use compact positive examples when the requested pattern is hard to specify. Make examples representative, inspectable, and consistent with the current schema; do not smuggle unrelated policy into them. For structured data, use the harness's schema/structured-output mechanism when available and validate the returned data independently.

Prefer direct declarative constraints over emphatic repetition. Preserve explicit language for irreversible or silent-failure safeguards (for example, a write boundary or source-provenance requirement); remove generic “always verify,” blanket tool defaults, and repeated urgency that merely causes over-triggering.

## Calibration matrix

The labels in this table are **workspace calibration labels** unless the cited local official mirror verifies the exact version. They are not model-availability claims. “Cursor Agent” is a harness label, not a model. Before selecting a current model, capability, effort level, tool setting, or API parameter, consult its current harness/model documentation and report an unverified value as unverified.

| Model or harness label | Prompt posture | Delegation and context | Calibration caution |
|---|---|---|---|
| Claude Fable 5.1 | Say what "done" is and that the scope is the deliverable. For unattended runs, use the page's autonomy block, because it may stop at "Next, I'll…". Ask for targeted edits and plain, non-mannered prose. | Escalation lead for hours-long or hardest-reasoning sessions. Let it keep working while background workers run. | Verified live 2026-09-29. Default effort `high`; searches less at `low`; rewrites whole files more readily; costs 2.5× Opus 5.5 per token. |
| Claude Opus 5.5 | State the outcome and real guardrails plainly; drop legacy emphasis, "think carefully" lines, and self-check scaffolding. On loose tasks, name the sources to read before acting. | Default lead. Pass workers a zero-context spec and artifact-backed state, and verify their load-bearing claims. | Verified live 2026-09-29. Default effort `medium`, which matches or beats Opus 5 at `high`. Opus 5 prompts carry over unchanged. |
| Claude Sonnet 5.5 | Give a complete first-turn scope with an explicit stop condition. Limit extras ("don't add tests, docs, or files that weren't asked for"), and require evidence for each claim. | Default worker (explorer `medium`, implementer `medium`, reviewer `high`) through the Claude roles in `.claude/agents/`. | Verified live 2026-09-29. Levels are recalibrated from Sonnet 5. At `low` it can skip verification; at `xhigh`/`max` it may spawn reviewer subagents. |
| OpenAI Codex GPT-5 Sol | Prompt for goal, constraints, evidence, side-effect limits, and completion criteria; do not prescribe every intermediate thought. | Workspace lead tier for complex coupled work. Keep current state in files and verify subagent output in the lead session. | “Sol” is a workspace tier label; inspect the active Codex runtime for exact model and effort. |
| OpenAI Codex GPT-5 Terra | Use the same explicit outcome contract, narrowed to an owned implementation or substantive review slice. | Default workspace worker tier for a settled, non-overlapping task. | “Terra” is a workspace tier label, not official OpenAI model nomenclature in these mirrors. |
| OpenAI Codex GPT-5 Luna | Make the scope short, read-only where possible, and return findings in a fixed concise format. | Use for low-risk exploration or repetitive checks; keep interpretation and final claims with the lead. | “Luna” is a workspace tier label; do not infer capability or availability from its name. |
| Gemini 3.8 Flash | Use clear headings/delimiters, precise task parameters, and explicit output length/schema; place large context before the final request. | Decompose independent operations only when results can be aggregated without policy judgment. | The local official Gemini mirror names 3.6 Flash, not 3.8 Flash: treat 3.8 as an unverified workspace calibration label and check live docs. |
| Gemini 3.8 Pro Antigravity | Separate exploration, plan, and execution; name the verification loop and enabled capabilities. Keep stable repo policy in rule files and interaction-specific behavior in the system instruction. | Restrict tools and network to task need; use read-only exploration before editing. | “3.8 Pro” is unverified in local official mirrors; “Antigravity” denotes a harness whose preview names and capabilities may change. |
| Cursor Agent | Prompt the actual selected model and the Cursor role separately. Provide the role body plus a bounded file list when named task roles are unavailable. | Prefer readonly explorer/reviewer roles; only a bounded worker edits explicitly named, non-overlapping files. | Cursor is a harness. Confirm whether project roles are discovered and whether the effective model override is exposed. |

## Context and delegation

- Supply only evidence that changes the decision. Reference canonical files directly rather than pasting stale summaries; state a cutoff or freshness requirement when time-sensitive facts matter.
- Delimit untrusted input, retrieved text, and instructions. Do not let quoted material redefine permissions or output requirements.
- Keep state in durable artifacts, not transient chat summaries. In multi-step work, establish the authority and acceptance criteria before assigning implementation.
- Delegate only slices that are independently specifiable, verifiable, non-judgmental, non-coupled, worthwhile, and safe to isolate. The lead retains architecture, scientific interpretation, policy conflicts, integration, and final status.
- Give a worker one goal, named file/scope boundaries, inputs, constraints, check, retry cap of two, hard stop on scope drift, and a concise return format. A genuine uncovered decision returns as a question.

## Evaluate and revise

1. Build a small representative set that includes a normal case, an edge/ambiguous case, and a safety or refusal boundary when relevant. Keep the expected outcome or scoring rubric outside the prompt.
2. Test the baseline and proposed prompt on the same cases. Evaluate task correctness, constraint adherence, schema/format validity, groundedness, tool/side-effect behavior, latency/cost where material, and failure behavior.
3. Diagnose the smallest cause: missing task fact, conflicting instruction layer, insufficient context, unclear output contract, unsupported harness capability, or model mismatch. Revise that component rather than accumulating universal rules.
4. Re-run the affected cases, inspect the produced artifact or side effect, and record the model/harness/version as observed. Do not claim a prompt is portable beyond the models and cases actually tested.

For API-oriented prompt design, read the vendors' current guides (save local copies if you want them offline): OpenAI Prompt Engineering, OpenAI Reasoning-Model Prompting, and Codex Agent Configuration. For Claude, read Prompting Best Practices, Prompting Claude Opus 5, and Prompting Claude Sonnet 5. Local copies go stale, so also read the live [Fable 5.1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1), [Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5), and [Sonnet 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5) pages for those models. For Gemini and Antigravity, read Gemini API Prompt Design and Antigravity Best Practices. For Claude Code harness features, consult Skills and Sub-agents.

## Verification and handoff

- Confirm the skill/prompt triggers on the intended request and does not trigger on its nearest confusing non-use case.
- Check that every claimed constraint has an owner, every local link resolves, and the prompt neither grants permissions nor assumes unverified runtime features.
- Run the applicable syntax/schema validator and the representative evaluation cases. For a new skill, run `python3 operations/scripts/verify-agent-parity.py` when parity integration is in scope; this skill author does not edit parity bridges unless explicitly assigned.
- Report the prompt location, intended model/harness, tested cases, observed verification, unresolved capability facts, and any approval gate. Stop rather than guessing when a missing decision would materially change behavior.
