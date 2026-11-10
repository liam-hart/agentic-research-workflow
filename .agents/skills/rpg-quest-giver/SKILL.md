---
name: rpg-quest-giver
description: Turn lab backlog tasks, GitHub issues, and RA assignments into RPG bounty-board quest cards with a rank, target class, lore briefing, binary main objectives, non-goals, a verification step, bonus objectives, and loot. Use when the researcher asks to turn a task into a quest, make a quest board for a sprint, or dress up an RA or undergrad assignment for Slack, Discord, or a kickoff. Do not use to create, prioritize, or route the underlying task (use triage), or to write a plain GitHub issue (use the repository's issue form).
---

# RPG Quest Giver

The lore makes the task fun to pick up; the objectives make it impossible to misread. A quest
card is a well-formed task spec in costume: strip the flavor and what remains must still meet
the binary acceptance-criteria standard in
`04 resources/notes/GitHub Issue and Project Task Formulation Standards.md`.

## Modes

- **Single Quest** (default): one card for a DM, Slack thread, or issue comment.
- **Guild Bounty Board:** 3–5 cards under one board header, for a sprint kickoff or lab
  meeting. Sort by rank, hardest first. When the researcher gives more than five tasks, ask which
  five, or split into boards.

## Workflow

1. **Read the real task.** Quote its source: the checkbox line and file, the GitHub issue
   number, or the researcher's message. Read the linked issue, plan, or project note when the task points
   to one, so objectives reflect the actual scope rather than the one-line summary.
2. **Resolve people.** Check assignee names against
   `03 areas/vault-system/People Dictionary.md`. Never invent a surname, role, or skill level.
   With no named assignee, write `Open to any adventurer`.
3. **Extract the contract.** Before writing any lore, write down: the deliverable, how to tell
   it is done, what is out of scope, the verification step, and any real deadline or
   dependency. If you cannot state a binary done-check, ask the researcher one clickable question rather
   than inventing scope. For a judgment or opinion task ("say whether X feels comparable"), the
   default deliverable is a short written verdict sent to the quest giver. When nobody can answer
   (unattended or subagent run), use that default or the narrowest plausible reading and mark it
   `*(Assumption: …)*` on the card.
4. **Assign rank and class** from the real effort and skill, not from drama (table below). Use
   the task's `#size/*` tag; with none, infer size from the action itself per
   `.agents/rules/task-metadata.md` (anchor 4) and append *(size inferred)* to the rank. Rank
   describes effort, not priority, so it never implies urgency.
5. **Write the card**, then re-read it with the flavor removed: could a new RA finish it and
   know they are done without asking anything?

## Rank and reward table

| Rank | Real size (`task-metadata` sizes) | Level | XP | Typical work |
|---|---|---|---|---|
| **Common** | `#size/quick` — under an hour | 1–10 | 25–50 | a reply, a rename, filling a form |
| **Uncommon** | `#size/short` — one sitting | 11–20 | 75–150 | a draft, a bounded fix, an SOP section, trying a task and reporting back |
| **Rare** | `#size/day` — a day or more | 21–35 | 200–400 | an analysis, a build, an asset pass |
| **Legendary** | multi-day, multi-person, or gate-critical | 36–50 | 500+ | a pilot run, a protocol overhaul |
| **World Event** | needs the whole lab at once | — | lab morale | scheduling, lab-wide data collection |

Within a rank, pick Level and XP by the skill the quest needs: low end when a newcomer could do
it from the card alone, high end when it needs rig access, code review, or domain expertise.
Class names describe that skill (`Code Paladin` for C#/Python, `Data Alchemist` for analysis,
`Literature Scout` for reading, `Eye-Tracker Monk` for rig and calibration work, `Scribe of the
IRB` for protocol and compliance). Quest Giver is whoever wrote the source task: the researcher for their
daily notes and boards, the Elder Council for a lab-meeting decision, the Archmage for the PI.

## Card format

```markdown
### 📜 <Quest Title>
- **Quest Rank:** <rank> · **Target Class:** Level <n> <class>
- **Assigned Adventurer(s):** <names, or "Open to any adventurer">
- **Quest Giver:** <the researcher / the Elder Council (lab meeting) / the Archmage (PI)>
- **Deadline:** <real date from the source, or "No deadline set">
- **Source:** <file:line, issue #N, or "the researcher's message">

#### ⚔️ The Lore & Briefing
<2–3 sentences framing the real friction as a fantasy crisis. Name the real artifact (repo
path, form, dataset) inside the lore so the briefing still points at the work.>

#### 🎯 Main Objectives
- [ ] <binary deliverable: an observable artifact or state, not an activity>
- [ ] <second deliverable if needed>

#### 🚫 Forbidden Paths (Non-Goals)
- <what not to touch or attempt, e.g. "do not edit Unity scene YAML by hand">

#### 🔍 Proof of Victory (Verification)
- <the exact command, file to open, or person who signs off, e.g. `python3 -m pytest tests/`, "PR passes local gates", "the researcher confirms on the lab's VR PC">

#### ✨ Bonus Objectives (Side Quests)
- [ ] <optional stretch goal; never required for completion>

#### 🏆 Loot & Rewards
- `+<n> XP in <real skill area>`
- `<one flavor item>`
```

A board wraps the cards:

```markdown
## 🗺️ GUILD BOUNTY BOARD — <sprint or week>
*Posted by <quest giver>. Claim a quest by replying with its title.*
<cards>
```

## Objective rules

- Each main objective is binary and observable: "`Assets/_Project/Prefabs/` contains 32 CC-BY
  models with `Z_min = 0` pivots," not "work on the prefabs."
- At most four main objectives. More means the quest should split.
- Non-goals are mandatory, even if only one line. Agent-facing quests also carry the
  verification command from the standard's Agent Contract. Human tasks with no command name
  the artifact to hand over and the person who checks it ("the researcher receives the written verdict").
- Real constraints stay literal inside the flavor: dates, file paths, IRB rules, safety and
  participant-data handling are never rephrased into lore that obscures them.

## Boundaries

- Output goes to chat for the researcher to post. Do not post to Slack, Discord, or GitHub, and do not
  create, edit, re-prioritize, or complete the source task.
- Checkboxes inside a card are fine in chat, Slack, and GitHub. If the researcher asks to save a board
  into the vault, write objectives as plain bullets unless each one is the researcher's own task (vault
  checkbox rule).
- Never add a deadline, priority, or assignee the source does not state.
- Loot is flavor. Do not promise real rewards (credit, authorship, pay) unless the researcher stated them.
- Tone stays affectionate. Lore never mocks the assignee, and participant data or names never
  appear in a card.

## Verification

- Every card names its source and has at least one binary main objective, a non-goal, and a
  verification step.
- Stripped of lore, the card still states what to do, what not to do, and how to prove it.
- Rank matches the size table; no invented dates, people, or rewards.
