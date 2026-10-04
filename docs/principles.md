# Principles

**What the agents know is written down in the project.** Each project has an `AGENTS.md` at its root that every agent reads first. It holds the rules, the prohibitions, and what needs asking. Procedures live in skills: short instruction files an agent loads before a particular kind of task. A skill carries the traps the code does not show. If a lesson is not in a file, the next agent learns it the hard way.

**Agents propose; people decide.** Structure, tool choices, anything hard to undo, and matters of taste come back to a person as a short decision with options and a recommendation. Where one standard answer exists, the agent applies it and says so.

**Nothing counts until it is checked.** Compiling is not verification, and an agent's summary of its own work is not evidence. Agents run the tests and validators, cite what they ran, and say plainly what they did not check.

**Big jobs get split.** The lead agent keeps the judgment calls and hands bounded, checkable pieces to subagents, then checks their output before relying on it.

**Every session leaves a trail.** A handoff note records what changed, how it was checked, and what is still open, so the next person or agent can pick the work up cold.
