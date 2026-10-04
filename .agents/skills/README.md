# Skills

Each folder here is one skill in the [Agent Skills](https://github.com/agentskills/agentskills) format: a `SKILL.md` with a `name`, a `description` that tells an agent when to load it, and the instructions. Some skills also carry `references/`, `scripts/`, or `assets/`.

These are de-identified copies of the skills used in the research setup this kit comes from:

- Other people are not named, and the author appears as "the researcher". Projects, labs, and journals are placeholders such as "Project A".
- Many skills name scripts, folders, and notes from the original setup (for example `operations/scripts/...` or a literature wiki). Those do not ship here. Read such a skill as a worked example of how to write one, and point it at your own files.
- A few reference files were left out because they are other people's published work. The skill still names them, so you can add your own copies.

New skills start from `operations/templates/Skill Template.md`. The full list is generated in `docs/reference/skills.md`; after adding or renaming a skill, run `python3 tools/list_skills.py`.
