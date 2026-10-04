---
name: hierarchical-draft
description: >-
  Build a new long-form academic draft through architecture, claim-level evidence grounding, and prose synthesis gates. Use when drafting a manuscript section, dissertation chapter, study proposal, or grant aim from scratch; use academic-writing directly for revision or polishing of existing prose.
---

# Hierarchical Draft

**Purpose:** stop a long-form draft from being produced in one pass. A one-shot draft loses the macro argument, argues superficially, and invents evidence. Three gates force the argument to exist before the citations, and the citations to exist before the prose.

**Interactive only.** Gates 1 and 2 require the researcher's confirmation (§ 1, § 2). This cannot be scheduled or run unattended.

**Scope boundaries — hand off rather than duplicate:**

| This is not | Use instead |
|---|---|
| Revising or polishing an existing draft | `academic-writing` (§ Revision workflow) |
| Replying to reviewers or writing a cover letter | `cover-letter` |
| Routing incoming feedback into task state | `feedback-reconcile` |
| A slide deck | `presentations` |

`academic-writing` remains the craft authority throughout. This skill never restates its rules — it says *when* to load them.
Load your authorial-voice rule with it (for example `.agents/rules/writing-style-academic.md`, which you write yourself) so Stage 3 also receives the researcher's canonical voice and blacklist rules.

---

## 0. Orient before drafting

Complete the live repository and `academic-writing` orientation, then establish the document type, venue, audience, word budget, scope, and authorized working location. This skill does not duplicate repository policy or prose rules; it owns only the three gated stages. Stop when the live authority marks the target as read-only or a review round blocks drafting.

The working draft carries its own gate state, so a session boundary doesn't lose it:

```yaml
---
type: working-draft
target: <what this becomes, e.g. Project C — Introduction>
draft_stage: 1          # 1 | 2 | 3
stage_1_approved:       # YYYY-MM-DD — set only when the researcher confirms Gate 1
stage_2_approved:       # YYYY-MM-DD — set only when the researcher confirms Gate 2
---
```

Never set an `approved` field from your own judgment. It records a decision the researcher made.

---

## 1. Stage 1 — Architecture and narrative arc

Write into the working draft under `## Stage 1 — Architecture`. No prose paragraphs at this stage; no citations beyond naming what evidence a paragraph will need.

**1. Thesis.** One sentence: the single claim the document exists to establish. If it needs two sentences, the document has two theses and one of them is a different paper.

**2. Novelty.** Four moves in four lines — significance → status quo → gap → how this work fills it (`academic-writing/references/cmu-establish-novelty-four-moves.md`). Frame the gap positively; never "X failed to."

**3. Section map.** Sections in order, one line of purpose each. An empirical article is an hourglass — broad, narrowing to this study, broadening again (Bem, via `academic-writing` § Section checks).

**4. Paragraph plan.** One row per paragraph. This table is the spine of the whole protocol:

| # | Section | Function | Purpose (one phrase) | Evidence required |
|---|---|---|---|---|
| 1 | Intro | significance | why spatial memory decline matters behaviorally | population-level effect, 1–2 sources |

`Function` is one of: significance · status quo · gap · rationale · method · result · interpretation · limit · transition.

> [!warning] One paragraph = one idea
> If a row's Purpose needs the word "and," it is two paragraphs. Split it now — a paragraph that resists a one-phrase summary will resist a clean draft (Gabbay; Simons).

**5. Thread register.** Every thread the introduction opens must resurface later with parallel emphasis (Simons). List `thread → opened at ¶n → resolved at ¶m`. An unresolved row is a defect to fix here, not in prose.

> [!danger] Gate 1 — no claims, no citations, no prose until the arc is confirmed
> Present the thesis, novelty moves, section map, paragraph plan, and thread register as one batch. Ask what needs to change. **Wait.**
>
> Silence is not approval. Do not draft Stage 2 claims "for just one section" to demonstrate progress — an approved arc is what makes Stage 2 cheap, and pre-empting it is how the protocol quietly degrades into the one-shot draft it exists to prevent.
>
> On confirmation: set `stage_1_approved` and `draft_stage: 2`.

---

## 2. Stage 2 — Claims and evidence grounding

Under `## Stage 2 — Claims & Evidence`, expand each approved paragraph row into bulleted claims — the argument in point form, in your own words. Then bind every empirical claim to a local evidence file.

### Citation form in this vault

> [!warning] Backtick citekeys, not wikilinks
> Write `` `author2022topic` ``, never `[[author2022topic]]`. LLM Wiki is a separate vault, so a citekey wikilink resolves nowhere and `validate-vault.py` reports it broken; and `export-clean-docx.py` refuses to export (exit 2) on any surviving `[[` or raw citekey.
>
> Add a `[[Vault Note Title]]` wikilink **only** where an in-vault note genuinely exists for that source — e.g. `` `author2018topic` `` + `[[Overview of the topic (Author et al 2018)]]`.
>
> Real APA author-year citations are written in Stage 3, not here.

### Evidence table

One row per claim. This is what makes Gate 2 checkable rather than a judgment call:

| ¶ | Claim (your paraphrase) | Type | Anchor | Local file | Verified |
|---|---|---|---|---|---|
| 3 | Schema pull warps recall only when the verbatim trace is weak | empirical | `author2022topic` | `wiki/sources/author2022topic.md` | file |

- **Type:** `empirical` · `theoretical` · `methodological` · `interpretive` · `assumption`.
- **Local file:** confirm by glob against `LLM Wiki/wiki/sources/{citekey}.md`, then `LLM Wiki/.raw/zotero/{citekey}.md`. Record which one you found.
- **Verified:** `file` (you read the local note) · `missing` (no local file) · `n-a` (interpretive/assumption — no citation owed).

### Grounding rules

- **Local evidence before external lookup**. Never web-search or call Zotero MCP for a paper that already exists locally.
- To read a paper through MCP, follow your literature-lookup rule. `zotero_get_item_fulltext` on a parent key silently returns PDF text instead of MinerU markdown.
- **Zero raw text**. The Claim column holds your sentence. Never paste source prose, tables, or annotation text into any tracked file.
- Do not cite a review as evidence for a primary result you have not verified.
- `interpretive` and `assumption` rows need no citekey, but must be labelled as such — an unlabelled assumption reads as a finding by Stage 3.
- A `missing` row has exactly three legal outcomes: ingest the source (`ingest paper`), weaken the claim to what local evidence actually supports, or mark it `unsupported — researcher's decision`.

> [!danger] Gate 2 — every empirical claim bound, or explicitly dispositioned
> Stage 3 cannot open while any `missing` row is undispositioned. Present as one batch: how many rows are `file`-verified, the `missing` list with a proposed outcome for each, and every `unsupported` row.
>
> The researcher decides. Write only what they confirm; leave anything unruled in the table rather than dropping it.
>
> On confirmation: set `stage_2_approved` and `draft_stage: 3`.

---

## 3. Stage 3 — Prose synthesis

Only now write paragraphs, under `## Stage 3 — Draft`. Keep Stages 1 and 2 in the file — they are the provenance for every sentence.

**Load the craft source for the move you are making** rather than working from memory. `academic-writing` § Source index is the full map (the source texts do not ship with this kit; see the note there); the ones that carry this stage:

| Move | Read |
|---|---|
| Introduction, gap, positioning | `references/cmu-establish-novelty-four-moves.md`, `references/gabbay-notes-on-academic-writing.md` |
| Results and Discussion sequencing, abstract, title | `references/bem-2003-empirical-journal-article.md` |
| Sentence-level clarity, topic/stress position | `references/gopen-swan-1990-science-of-scientific-writing.md` |
| Cutting the draft, search-and-destroy word list | `references/simons-2019-writing-guide.md` |
| Ready-made phrasing for a rhetorical move | `references/phrasebank - <function>.md` |

**APA 7th, with one vault-specific trap:**

> [!warning] Cross-check the byline before writing an in-text citation
> LLM Wiki `authors:` frontmatter can be incomplete. Read the byline in `.raw/zotero/{citekey}.md` before writing "et al." or a two-author citation. This is the same discipline `export-clean-docx.py` documents.

**The rule that makes the gates mean anything:**

> [!danger] No new claims in Stage 3
> If a paragraph needs a claim absent from the Stage 2 table, stop writing prose. Add the row, bind it, and disposition it. Prose that quietly acquires an ungrounded claim is the exact failure this protocol exists to prevent, and it is invisible once the sentence reads well.

Then apply `academic-writing` § Style in a cutting pass — active voice, old→new information order, no metacomments, no empty qualifiers or stock AI phrasing — and cut 10–30%.

---

## 4. Backtracking is a success, not a failure

Finding in Stage 2 that the arc is wrong, or in Stage 3 that a paragraph carries two ideas, means the protocol worked. Return to the stage that owns the problem, reset `draft_stage`, note what changed, and re-gate that stage. Never patch prose around a broken argument — that converts a structural defect into a stylistic one, where it becomes much harder to see.

---

## 5. Handing the prose onward

The vault working draft is not the manuscript.

- **Drafts kept in a shared workspace:** when the canonical draft lives in a shared drive that agents may not write to, treat it as read-only. Report that the prose is ready and where it sits; the researcher moves it.
- **Lab-facing `.docx`:** export via `operations/scripts/export-clean-docx.py`, and resolve every backtick citekey into a real APA citation in a temp copy first. The gate refuses on raw citekeys deliberately — resolving one requires checking the actual author list, which is human judgment.
- Update the project's canonical status/task surface in the same pass if this draft closed tracked work.

---

## 6. Delegation

Per `AGENTS.md` § Execution and delegation, delegate execution and keep judgment:

- **Orchestrator (do it yourself):** the thesis and arc, both gate conversations, deciding what a `missing` row should become, and any call about what the evidence actually supports.
- **Bounded worker:** locating local evidence and filling the `Local file` / `Verified` columns, checking one claim against a bounded source set, or drafting one already-approved and already-grounded paragraph. Use an authorized harness role with an exact source set and output contract; the lead verifies every returned citation and retains prose judgment.

If you judge a step unsuitable for delegation, say so in-session with the reason.

---

## 7. Safety rules

- **Daily notes are read-only.** This skill never writes to them.
- **Literature notes are read-only.**
- **External shared-drive workspaces are read-only** — read for context, never write.
- **Zero raw text.** Paraphrase everything; never bulk-paste source text into a tracked file.
- **Checkboxes are for the researcher's actionable tasks only** — not for this skill's stage lists or the working draft's internal tracking.
- **Never invent a person's name or affiliation.** Consult your people dictionary note.
- **Never fabricate a citation, a result, or a statistic.** A claim with no local evidence is a `missing` row, not a plausible-looking citekey.
- **Commits:** targeted `git add <file>` only, never `git add .`. No push without explicit authorization for the session.

---

## 8. Close out

Append a `## Walkthrough & Verification` section to the active handoff (`operations/handoffs/YYYY-MM-DD-HHMM.md`) with `[[wikilinks]]` to the working draft and every vault file touched (`[name](file:///path)` only for paths outside the vault), the stage the draft reached, any undispositioned evidence rows, and `Sign-off: <Model Name> (effort: <level>)`.
