---
name: collaborate
description: Keep the researcher in the loop on key decisions — architecture, data models, tool or library choice, hard-to-reverse actions, precedent-setting conventions, and matters of taste — with a teaching decision card, clickable choices, or a generated HTML decision page. Use when work reaches such a decision, or when the researcher invokes /collaborate to be walked through a session. Do not use for choices with one clear standard answer, or in unattended runs.
---

# Collaborate

The researcher makes the decisions that shape the work and learns the concepts behind them. Your job at those moments is to frame the choice well: name the concept, lay out real options and their trade-offs, recommend one, and collect a precise answer.

## Decision or Note

- **Decision — stop and wait:** structure (module boundaries, data models or schemas, file formats, folder layout); tool, library, or service choice; anything expensive or hard to reverse; conventions that set precedent; matters of taste (visual, naming, wording).
- **Note — don't stop:** when one standard answer exists, apply it and say so in one line: the standard, why, and "say if you want otherwise."
- Check the project's decision log first. A recorded decision is not re-asked.

## The decision card

What is being decided, the concept name, 2–4 real options with a one-line trade-off each, and your recommendation with its reason. Depth is offered, not dumped: *why this matters*, *what most teams do*, *what goes wrong if we choose badly*. Every option must be one a competent engineer would defend; never pad the list.

## Delivering the question

Use the harness's clickable choice tool whenever it has one. Typed letters are the fallback, never the default.

| Harness | Tool |
|---|---|
| Claude Code | `AskUserQuestion`: 2–4 options, "Other" is automatic; recommended option first, labelled `(Recommended)`; depth goes in option descriptions and code or layout comparisons in `preview`; up to 4 related decisions per call |
| Codex CLI | `request_user_input`: 1–3 short questions (verified 2026-09-30 in installed codex-cli 0.158.0). The binary says it is "only available in" certain collaboration modes (likely Plan mode; the `default_mode_request_user_input` feature flag exists but is untested) and never in `codex exec`. Where it is unavailable, use typed choices |
| Cursor Agent | `ask_question`: structured options with a skip choice (verified 2026-09-30 in installed cursor-agent 2026.09.18) |
| Antigravity CLI | `ask_question`: structured options (verified 2026-09-30 in installed agy 1.2.14) |

## Escalate to a decision page

Build a page when a Decision has four or more options, the candidates are visual, or five or more related decisions are pending.

1. Write a spec JSON in the scratchpad or beside the work ([spec format](references/spec-format.md)).
2. Render it: `python3 .agents/skills/collaborate/scripts/render_decision_page.py render <spec.json>`. This writes `.decision-pages/<id>.html` (a folder git ignores) and opens it.
3. Tell the researcher the page is open and that either button works: **Copy for chat** (paste the text back) or **Save file**.
4. Read the answer, always passing `--spec` so a stale page is caught:
   - Pasted: save the paste to a scratch file, then run `read <file> --spec <spec.json>`.
   - Saved: `read "$(ls -t ~/Downloads/decisions-<id>*.json | head -1)" --spec <spec.json>`.

   Exit code 2 means the page was stale: re-render and ask again. Treat notes as part of the answer.

## Modes

- **Default:** the Decision triggers above.
- **Turned up (`/collaborate`):** for the rest of the session, treat reasonable-but-debatable choices as Decisions too. Before each question, give a short tutor explanation of the concept and check "does this make sense?"

## Recording

Record each Decision in the project's decision log once the researcher has answered: `docs/DECISIONS.md`, a numbered decision record under that repository's own rules, or the canonical project authority. If there is none, use the session handoff. One line each: the decision, the chosen option, the reason, and the date. Notes stay in chat.

## Boundaries

- Unattended or scheduled runs never block. Pick the most reasonable option and record the assumption.
- A recommendation is not an answer. A choice is the researcher's only once the researcher has given it.
