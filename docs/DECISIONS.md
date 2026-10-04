# Decisions

Decisions about this repository, newest last. Each has the choice and the reason.

| # | Decision | Choice | Reason |
|---|---|---|---|
| 1 | Home | A public repository | A method meant to be shared; public also keeps the private/public boundary clean |
| 2 | Primary reader | Other researchers, or anyone adopting the method | Project contributors are covered by each project's own onboarding |
| 3 | Content model | A skeleton with example pages, not a copy of the source setup | Readers clone it and start; the canonical versions of the skills stay in the private source, and this repository follows them |
| 4 | Layout | The skeleton sits at the repository root; the method is explained under `docs/` | A clone is a working project |
| 5 | Format | Plain Markdown | A documentation site can be added later without changing the files |
| 6 | Skill list | Generated into `docs/reference/skills.md` by `tools/list_skills.py` from each shipped `SKILL.md` | The list describes only what is in this repository, and CI fails when it is out of date |
| 7 | Prose | Written and edited in this repository | Generated output never overwrites prose |
| 8 | Hand edits to generated files | `tools/list_skills.py --check` fails in CI when the list differs from the skills | Edit the skill's description, then regenerate |
| 9 | Privacy | Two layers: a private gate with a deny-list before anything is copied here, and a generic check in this repository's CI | This repository never holds the deny-list |
| 10 | Skills | All of them ship as de-identified copies, aligned to one template | The skills are the method |
| 11 | Names | Other people are rewritten to roles; the author appears as "the researcher" in skills | No real name is published |
| 12 | Skill format | Agent Skills (<https://github.com/agentskills/agentskills>) | An open format that several clients load |
| 13 | Licence | CC BY 4.0 for prose, MIT for code, templates, and skills | Standard and permissive |
