---
name: workflow-overview
description: Regenerate and republish a shareable AI-workflow overview page (and generated reference lists) from the skill registry, the rules README, and a hand-written story. Use when your parity check reports an overview as out of date, or when asked to refresh or publish the overview. Do not use to author or change the skills and rules the page describes.
---

# Workflow Overview

An overview page shows how a team or person works with agents. Each page has an id (for example `project` for a project contributor guide, `vault` for a research vault page). A generator script, `operations/scripts/workflow-overview.py` (yours; this skill describes the method), builds each page as a committed markdown file and a self-contained HTML page for publishing. A page can also carry reference outputs: generated-only lists written under `docs/reference/` of a public repository. Every generated file records a hash of its own body on its second comment line, so the script can tell a hand edit from a change in the sources.

## Resources

Sources, in the order a change usually lands:

- `operations/agent-config/workflow-overview.json`: page settings (title, eyebrow, an optional per-page `intro`, `reference_outputs`), skill groups, one decision per skill and rule (a group, or `hidden` with a reason readers see), the public-repository source and `protected_trees`, and each page's `published` URL and fingerprint.
- A privacy deny-list file beside the config: terms the privacy gate refuses. It stays private and is never copied into a public repository.
- A shared intro note, and each page's story (a hand-written note per page). Marker comments such as `<!-- overview:skills -->`, `<!-- overview:rules -->`, and `<!-- overview:not-included -->` mark where generated sections go.
- Your skill registry (for example `agent-parity.json`), each `SKILL.md` description, and `.agents/rules/README.md`.
- `operations/templates/workflow-overview.html`, the page design. It is part of each page's published fingerprint, so a template change marks the web page out of date.

## Workflow

1. Run `python3 operations/scripts/workflow-overview.py check` and read its notes. A hand-edited output is reported separately from an out-of-date one; reconcile it (below) before rendering.
2. **Undecided skills or rules** are left off every page until the config has a decision for them. Placing a new skill in its obvious group is fine; whether a page shows or hides something is the owner's call, so ask before hiding or showing anything they haven't already decided.
3. **Vault page.** `render --page vault --write --html <scratchpad>/vault.html`, then review the diff of the generated markdown.
4. **Project page.** If its markdown lives in a separate repository, regenerate it in a worktree on a feature branch, never on a shared working copy: `render --page project --project-tree <worktree> --write --html <scratchpad>/project.html`. The script refuses a protected path. Commit the generated file there and open a pull request under that repository's own rules. The page's out-of-date note clears only after the PR merges, because `check` reads that repository at `main`.
5. **Publish** each HTML file with your publishing tool. The template has no `<title>`, so pass one explicitly. The first publish creates the page; every later one passes the page's `published.url` from the config so the link already shared keeps working.
6. Record it: `mark-published --page <id> --url <url>`, adding `--project-tree <worktree>` for the project page, so the fingerprint matches what was published.
7. **Reference outputs.** `render --page vault --public-tree <clone>` writes the page's `reference_outputs` into a clone of the public repository and nothing else. It reads neither the intro nor the story. Pushing that repository needs the owner's approval of the exact files.
8. Commit the config and the generated note with targeted `git add`.

## Reconciling a hand edit

`render` refuses to overwrite a generated file whose body no longer matches its recorded hash, and it checks every target before writing any of them. Fold the edit into the source that owns it, then regenerate:

1. Diff the file against a fresh render: `render --page <id>` prints the primary page; for a reference output, render into a scratch copy of the clone.
2. Find the owner of each changed line. Prose belongs to the intro or the page's story. A skill or rule line belongs to its `summary` in the config. A group heading or blurb belongs to `groups`. A "not included" line belongs to a `hidden` reason. Layout belongs to the template. A change that would alter a skill's or rule's own description belongs in that skill or rule, which is outside this skill.
3. Make the change there. Whether to keep an edit someone else made is the owner's call; ask when the intent is unclear.
4. Render again. The refusal clears once the regenerated text carries the edit.

`--force` is for an edit that is being discarded on purpose. It first saves the edit as a diff under `operations/state/workflow-overview-hand-edits/` and prints the path.

## Summary overrides

A `summary` replaces a skill's description or a rule's purpose on the page, so a later change to that source would otherwise go unseen. `summary_source_sha256` beside it records the source the summary was written from. When `check` says a summary may be stale, compare the two, fix the summary if needed, then run `record-summaries <name>`. `record-summaries` with no names only enrols summaries that have no hash yet.

## Boundaries

- A published page starts private. The owner decides who gets the link; never share it or change its sharing.
- A privacy gate with a private deny-list runs on every render. It also refuses user paths, email addresses, home-relative paths, and wikilinks in anything bound for the public repository. Remove the text from its source; never work around the gate. In `check`, a deny-list hit is a note, because a draft marker in a private note is work in progress; rendering still refuses it. The gate cannot catch a disclosure nobody listed, so a person reads the public files before a push.
- Edit the story or the config and regenerate. Never edit a generated file by hand.
- The script writes only a page's own output, files under `docs/reference/` of an `--public-tree` clone, and the config. It refuses every tree in `protected_trees` and an `--public-tree` inside the vault. If one write of several fails, the files already written are put back.

## Verification

- `check` shows no out-of-date note for the vault page, and for the project page once its PR has merged.
- Your skill-parity check passes.
- Open each published page once and confirm the skill groups, rules, and intro rendered.
