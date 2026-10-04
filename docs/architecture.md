# Architecture

The setup has five kinds of file. Each one has one job.

| Piece | Where | Job | Loaded |
|---|---|---|---|
| Instruction file | `AGENTS.md` | Invariants, authority, what needs asking, pointers | Every session, in full |
| Rules | `.agents/rules/` | Constraints for a path or a kind of task | When the path or task matches |
| Skills | `.agents/skills/<name>/SKILL.md` | The procedure for one kind of task | Only the description, until the task calls for it |
| State | `operations/STATE.md` | Gates, blockers, next pickups | At the start of a session |
| Handoffs | `operations/handoffs/` | What a session did and how it was checked | The latest one, at the start of a session |

## Why it is split this way

- **Always-loaded text is expensive**, because an agent reads it before every task. Keep `AGENTS.md` to what is true for every task and move procedures into skills.
- **A skill loads in stages.** An agent sees only each skill's name and description until a task matches; then it reads the body; then any reference file the body points to. Write the description so it says what the skill does and when to use it. The format is specified at <https://github.com/agentskills/agentskills>.
- **State and handoffs are different things.** State is the current picture and is overwritten. A handoff is a dated receipt and is never edited afterwards.

## Working across agents

`AGENTS.md` is read by most coding agents. For clients that look for their own file, add a one-line pointer (this kit ships `CLAUDE.md` containing `@AGENTS.md`). Keep one canonical copy of each rule and skill, and link or generate the client-specific copies from it.

## Playbooks

Task-specific practice lives in `docs/playbooks/`.
