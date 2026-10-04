---
name: academic-writing
description: Draft, revise, or audit evidence-bound empirical manuscripts and theses. Use when working on manuscript prose, argument structure, section conventions, or claim-level academic revision; use hierarchical-draft for a new long-form draft that needs gated architecture first.
---

# Academic Writing

Produce manuscript structure and prose in which every claim is bound to evidence and written to the conventions of its section. This skill owns that structure and prose; it does not invent methodological or statistical decisions: obtain approved design content from `experiment-design`, measurement content from `methods`, and quantitative content from `statistics`.

Use this skill for empirical manuscripts, dissertation chapters, journal responses, and research statements. Work from the live canonical draft and its project status surface; do not invent citations, results, or decisions.

Read your own authorial-voice rule (for example `.agents/rules/writing-style-academic.md`, which you write yourself) as the canonical authorial-voice layer before drafting or revising. This skill controls evidence, stage, and craft procedure; the rule controls the researcher-specific cadence, proportional language, and the search-and-destroy blacklist.

The craft guidance below is distilled from the source texts in `references/` and attributed inline so every rule is traceable and the full treatment is one read away. When a task turns on a rule, open the cited source — don't work from the summary alone. The **Source index** at the end maps needs to files.

> The source texts are other people's published work, so this kit does not ship them. Get your own copies, save them under `academic-writing/references/` with the file names in the Source index, and the pointers below will resolve. Until then, work from the summaries.

## Start by identifying the stage

1. **Outline / early drafting:** establish the contribution, section map, and evidence needed before drafting prose. **For a new long-form document drafted from scratch** — a manuscript section, dissertation chapter, study proposal, or grant aim — use `.agents/skills/hierarchical-draft/SKILL.md` instead of drafting here. It runs this stage as a gated three-stage protocol (architecture → claim/evidence grounding → prose), with the researcher confirming each gate, and defers to this skill for all craft rules. Stages 2–5 below stay here.
2. **Evidence integration:** verify the paper locally first (LLM Wiki source note, then trimmed MinerU); make one precise claim per citation and distinguish results from interpretation.
3. **Revision:** preserve the canonical source, state the target paragraph and revision purpose, then edit for argument rather than surface polish alone.
4. **Advisor-review reconciliation:** Markdown is canonical outside an open Word review round. Preserve sent Word artifacts, merge accepted changes back to Markdown, and log provenance before derived exports.
5. **Submission QA:** verify citations, figures/tables, reporting, journal requirements, and blinded/unblinded artifacts. Do not represent an unchecked gate as complete.

For a whole-manuscript or submission pass, also run a consistency sweep across canonical terminology and abbreviations, units and notation, headline values and numerical precision, participant/exclusion counts, and agreement among prose, tables, figures, captions, and supplements. Return proposed corrections with locations; do not bulk-normalize text or resolve a scientific discrepancy by choosing the most common value.

When data, code, or materials availability is in scope, inventory only the outputs needed to support the manuscript's claims: raw/restricted data, shareable processed data, figure source data, analysis code, reused data/materials, and documentation. Map each to a confirmed access route or `AUTHOR_INPUT_NEEDED`. Current consent, privacy, repository, and journal authorities control what can be released; never invent a repository, accession, embargo, or availability promise.

## Required orientation

- Read the project status/checklist and the canonical draft before editing.
- For literature claims, use the local LLM Wiki evidence layer before external search. Treat preprints explicitly as preprints.
- Preserve user and coauthor decisions; flag conflicts rather than silently reconciling them.

## Revision workflow

For each substantive edit, identify:

| Element | Requirement |
|---|---|
| Claim | Specific, supportable, and calibrated to the cited evidence |
| Function | Gap, rationale, method, result, interpretation, limit, or transition |
| Scope | What the study establishes—and what it does not |
| Citation | Correct source, year, and evidence type; no placeholder citation claims |
| Traceability | Update the project log/status task when the edit resolves tracked work |

Revision is re-vision, not proofreading, and should take longer than drafting (Simons; Bem). For a structural pass, outline the finished draft one phrase per paragraph: if a paragraph resists a one-line summary, it holds more than one idea and must be split (Simons; Gabbay's "one paragraph = one idea"). Proofread for typos only after the structure is settled. For a full sentence-and-word cleanup pass, run the **revision worksheet at the end of `simons-2019-writing-guide.md`** — its search-and-destroy list is the concrete checklist this section abstracts.

### Section checks

Grounded in Bem's *Writing the Empirical Journal Article* unless noted.

- **Overall shape:** an article is an hourglass — broad opening, narrowing to the specific study, broadening again in the discussion; the discussion's topic order often mirrors the introduction (Bem).
- **Introduction:** open with people or a problem, not a literature list — lead the reader from familiar terms to the technical construct (Bem's opening-statement rules; Simons: entice the reader, establish a controversy/mystery). Move through the four novelty moves — significance → status quo → gap ("however…") → how this study fills it (CMU novelty moves). Review only the literature that motivates the question; keep researcher names in citations, not the narrative, except where the argument depends on a specific name (Simons). Every thread raised here must resurface later with parallel emphasis (Simons). End with a brief overview of the present study.
- **Methods:** report design, participants, materials/apparatus, procedure, exclusions, and analytic decisions so another researcher could reproduce them. Lead the reader through the sequence as a participant would experience it; give groups and variables memorable operational labels ("the \$1 group"), not empty codes ("Treatment 3") (Bem).
- **Results:** write in prose, not a dump of numbers — forest before trees: state the central finding first, then elaborate or qualify (Bem). For each result, follow the sequence: (1) restate the conceptual question, (2) restate the operation/measure, (3) **give the answer in plain English**, (4) *then* the numbers (estimand, test/model, uncertainty, effect size), (5) qualify, (6) summarize where things stand, (7) transition. Never report a statistic without interpreting it substantively; reorganize output to fit the narrative rather than being "a prisoner of ANOVA" (Bem). Keep result separate from interpretation.
- **Results sufficiency:** retain the shortest evidence chain that establishes and bounds the claim. Flag duplicated reporting across prose, captions, tables, and figures. After reviewer-driven material is added, check whether it should replace, compress, or relocate existing text before appending another account of the same result; the manuscript and venue authorities control final placement.
- **Discussion:** lead with the answer — support or non-support of each question — then convergence/divergence with prior work, alternatives, limits, and bounded implications. Do not dwell on every flaw or spin pretzel theories for every hiccup; there is a −.73 correlation between the clarity of results and the length of the discussion (Bem). End with a bang, not a "further research is needed" whimper.
- **Abstract:** contain only what is in the manuscript; match sample, outcomes, direction, and moderation language exactly. Empirical abstract ≤120 words covering problem, participants, method, findings *with* significance levels, and implication (Bem).
- **Title:** fully explanatory when standing alone, ~10–12 words, carrying the variables/issue and retrieval keywords (Bem; Gabbay on title keywords). No subtitles. Question titles are acceptable only for research proposals and talks; manuscripts and all other outputs use claim or descriptive titles.

## Style

- **Reader expectations govern clarity** (Gopen & Swan): keep subject and verb close; put old/linking information in the topic position (sentence start) and the new, emphasis-worthy information in the stress position (sentence end); express the action of a clause in its verb; give context before asking the reader to consider anything new. Misplaced old/new information is the single most common structural fault. Pinker's compact form: old information first, new information last; save the heaviest phrase for last.
- **Active voice and strong verbs** (Simons): rewrite passives — the "insert *by zombies*" test flags them — and cut forms of "to be" in favor of a real verb. Let verbs be verbs: "appear," not "make an appearance" (Pinker).
- **Omit needless words** (Bem/Strunk; Cranford's "kill your darlings"): every word should tell. After a first draft, cut ~10–30% (Cranford: 10–15%; Bem: aim for 30%). For wordy sentences, box prepositions, circle "to be" verbs, underline nominalizations, then put agent + action at the front and prune (CMU concise-sentences method).
- **No metacomments** (Bem): don't narrate the paper ("Having discussed X, we now turn to Y"); let a transition sentence carry the reader and summarize as it moves. If you feel the need to signpost, the plot line is probably too cluttered.
- **Repetition and parallel construction over elegant variation** (Bem): reuse the same term for the same concept; a synonym signals a new meaning. Hold the grammar of compared clauses rigidly parallel — only the variables vary.
- **Concrete, non-meta language** (Pinker): prose is a window onto the world — prefer visual, concrete nouns; minimize meta-concepts ("approach," "framework," "process," "variable"); use examples liberally; beware the Curse of Knowledge — what is obvious to you is not obvious to the reader (Gabbay: "you are not your reader").
- **One paragraph = one idea** (Gabbay; Simons): the point belongs in the first sentence or two, not buried mid-paragraph.
- **Hedge to reflect evidence strength, not as decoration** (Simons); cut empty qualifiers ("very," "certain," "specific," "various," "clear," "obvious") and stock AI phrasing ("crucially," "moreover," "it is important to note"). These are the same search-and-destroy targets in Simons' worksheet — apply that list.
- **Slide copy is not prose.** On presentation slides, text that works as something said aloud (transitions, headline restatements, summaries) belongs in the companion explainer; the bottom band holds only a context line that adds information. Follow `presentations` § 3b-i.
- **Person-first, inclusive, APA-consistent language** unless a field-standard term or participant preference warrants otherwise; drop the data, not the subjects (Simons); use gender-neutral phrasing (phrasebank note).

## Citation and source discipline

- Use the manuscript's existing citation format and reference manager contract; never mix in Obsidian-only citation syntax unless the target document calls for it.
- For every new source, record complete bibliographic details or flag the entry as awaiting Zotero/import rather than guessing.
- Do not cite a review as evidence for an unverified primary result when the primary source is available.
- Criticize the work, not the investigators — ad hominem framing offends the reviewers you may draw (Bem; Simons; Gabbay). Frame contribution positively ("While X pioneered Y, this work extends…") rather than "X neglected/failed/ignored" (CMU novelty moves).

## Handoff and verification

- Report the exact files and paragraphs changed, claim-level rationale, and any unresolved evidence or author decision.
- Verify the changed passages and run the project's lightweight citation/reference checks when available.

## Source index

Load the relevant source for the task rather than working from the summaries above.

| Need | Read |
|---|---|
| Empirical article structure; Results/Discussion sequencing; abstract & title; omit-needless-words | `references/bem-2003-empirical-journal-article.md` |
| Full revision worksheet + search-and-destroy word list; active voice; structure/flow | `references/simons-2019-writing-guide.md` |
| Sentence-level clarity: subject–verb, topic/stress positions, old→new information, logical gaps | `references/gopen-swan-1990-science-of-scientific-writing.md` |
| Concrete language, "don't go meta," reader-focused style rules | `references/pinker-sense-of-style-rules.md` |
| Introductions, paragraphs, comparing your work with others', "you are not your reader" | `references/gabbay-notes-on-academic-writing.md` |
| Establishing novelty/gap in an introduction (significance→status quo→gap→fill) | `references/cmu-establish-novelty-four-moves.md` |
| Fixing a specific wordy/convoluted sentence (prepositions, "to be," nominalizations) | `references/cmu-creating-concise-sentences.md` |
| Writer mindset: read/write/edit habit, story-first, cutting a draft | `references/cranford-2020-editorial-tips.md` |
| Ready-made phrasing by rhetorical move | `references/phrasebank - <function>.md` (e.g. `reporting results`, `discussing findings`, `being cautious`, `being critical`, `referring to sources`, `defining terms`, `compare and contrast`, `explaining causality`, `signalling transition`, `writing conclusions`) |
| Phrasebank sections without a split file (abstracts, acknowledgements, punctuation/style notes, confused-words lists) | `references/manchester-academic-phrasebank-full.md` |
| Generic sentence openers | `references/starter-phrases-academic-writing.md` |
| Grant-application craft | `references/grant-application-craft.md` |
