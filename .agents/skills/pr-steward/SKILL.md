---
name: pr-steward
description: Act as the merge steward for a repository where parallel agents keep opening pull requests, reviewing each with a fresh independent reviewer, running the repo's local gates, merging what passes one at a time, holding only what the owner reserves, and re-sweeping as new pull requests arrive. Use when the owner asks to review and merge open pull requests, clear or watch the PR queue, or merge PRs as they come in, especially while CI cannot run. Do not use to review a single diff without merging (use code-review), or for an autonomous run merging its own pull request.
---

# PR Steward

The researcher starts this skill when several agents are opening pull requests in parallel and nobody is merging them. A common trigger is CI that cannot run, for example when the organisation's Actions minutes are used up. The steward reviews every open pull request and merges what passes, on the owner's authority. It holds only what the Authority list reserves, with the review already done, so the owner's decision on a held PR takes a minute. It keeps sweeping until the owner stops it.

## Relation to /ship

Claude Code's `/ship` and `/steward` cover the author's side of the same pipeline. On one branch they commit, push and open the PR (`/ship` also runs `/code-review` first), then fix CI failures, conflicts and review comments for up to 7 days. They never merge. Only a line the user types starts them, so this skill cannot invoke either one. The split:

- The owner types `/ship` on a clean feature branch to get one PR to merge-ready. The steward stays the only thing that merges.
- The author-side `/code-review` does not replace the steward's independent reviewer.
- `/ship` commits and pushes uncommitted changes wholesale, so never suggest it on a worktree that holds unrelated changes, or where only named files may be staged.
- The steward never pushes to a branch a `/ship` or `/steward` session is watching (step 5).

## Authority

- The owner's request in the current session authorizes this skill for **the named repository, for this session only**. Within the merge scope below, it may push to PR branches, edit PR descriptions, post PR comments and merge. It never pushes to `main` directly, never merges in another repository, never pushes its own edits to governance files, and never adds or removes a veto label such as `No auto-merge`.
- If the repo has a merge rule (for example `docs/agents/AUTO_MERGE.md`) and an `AGENTS.md`, read both before the first merge for their gates and tracking requirements. Never edit the merge rule.
- **Merge** a PR when all of these hold at its head SHA:
  - A fresh independent reviewer approves the content.
  - Every decision the PR needs from the owner is answered on the issue or PR.
  - The local gates pass (step 6), and any manual or hardware verification the repo requires before merge has passed.
- **Held, not merged:**
  - Draft PRs, and any PR carrying the owner's veto label.
  - Any PR with a CI job that ran and failed.
  - Any edit to the merge rule or the decision log.
  - Governance files (`AGENTS.md`, `CLAUDE.md`, `.claude/`, `.agents/`, `.github/`, `CONTRIBUTING.md`), unless the owner asked for that change on record.
  - Dependency manifests and lock files; data, participant or raw files; secrets and config holding credentials.
  - Any change to what is recorded, an output schema, randomization, exclusion or validation thresholds, or participant-visible behaviour or timing.
  - Any PR still owed a decision, or still at `changes` after the fix round.

## Subagents

Run reviewers and fix workers on a mid-tier model at medium effort, not the lead's flagship model: a queue of PRs multiplies the cost. Where two model families are available, review one family's PRs with the other, so their blind spots do not line up. The steward keeps the judgment calls: classification, holds and merges.

## Each pass

1. **Inventory.** `gh pr list --state open --json number,title,isDraft,headRefName,headRefOid,mergeStateStatus,labels,changedFiles,files`.
   - If `changedFiles` exceeds the length of `files`, the list was truncated. Hold the PR, so a reserved file cannot hide past the cap.
   - Skip any head SHA that already has a `pr-steward` verdict comment.
2. **Classify** each new head SHA as *held* or *mergeable* from the Authority list and the PR's live file list, never from its description.
3. **Review in parallel.** For each PR, make a temporary worktree at the head SHA and spawn one fresh read-only reviewer. Give it the repo and PR number, the head SHA, the worktree path, the repo's `AGENTS.md` and merge rule, the denylist, and the linked issue's acceptance criteria, but never the author's summary. It labels each finding **Important** (a bug the change adds or makes worse, or a broken repo rule), **Pre-existing** (already on `main`), or **Nit**, the scale `/code-review` uses. Only an Important finding makes the verdict `changes`. It returns `approve`, `changes` or `escalate`, with a per-condition checklist naming the head SHA. Review held PRs too, so the verdict is waiting for the owner. Run each PR head's own gate scripts inside its worktree, and never run a gate script the PR itself modifies.
4. **One fix round.** On `changes`, post the findings as a `pr-steward` comment, then fix them on the branch yourself or through a bounded worker, but only if the branch is idle (step 5). A *different* fresh reviewer re-reviews. A second `changes` holds the PR. Never fix by weakening, deleting or skipping a test.
5. **Stale and busy branches.**
   - A branch is idle when it has had no new commit for at least 15 minutes. Otherwise skip it until the next pass.
   - A branch a live `/ship` or `/steward` session is watching is never idle. Treat it as watched when a local session is listed on it, or when the author has replied to a review thread or pushed a fix in the last 24 hours. Post the findings as a comment and push nothing.
   - On `BEHIND` with an idle branch, merge `origin/main` into it in a temporary worktree and push normally. Never rewrite a pushed branch.
   - Any push voids the approval; the new SHA gets a fresh review and fresh gates.
6. **Merge serially**, one PR at a time against the newest `main`. Immediately before each merge:
   - `mergeable` is `MERGEABLE`. `mergeStateStatus` is `CLEAN`, or `UNSTABLE` only because checks never started. On `DIRTY` or `BLOCKED` hold; on `UNKNOWN` retry next pass.
   - `git merge-base --is-ancestor origin/main <sha>` holds, and the approval and the gates name that same SHA.
   - The local gates are the commands the repo's `AGENTS.md` names, plus `git diff --check`.
   - CI (`gh pr checks <n>`): if jobs never started, note it and rely on the local gates; if a job ran and failed, hold; if CI works again, require it green.
   - Merge with `gh pr merge <n> --squash --match-head-commit <sha>`, unless the repo names another method. Then post the reviewer's checklist, the gate output and the CI note on the PR.
7. **After each merge**, confirm the merge commit is on `main` and set the linked issue's status as the repo's tracking rules require. A merged PR is not evidence that anything was verified outside the gates.
8. **Hold** by posting a `pr-steward` comment with the head SHA, the reason and the reviewer's checklist. End it with `Blocked by: <gate>. To merge, reply: <exact phrase>`. Do not change labels and do not push to a held PR.
9. **Report** in two or three lines per pass: merged (PR and merge SHA), held (PR and its `Blocked by:` line), waiting on a busy branch, and still under review.

## Pacing

Where the harness has a wakeup timer (Claude Code `/loop` with `ScheduleWakeup`), schedule the next pass at the end of each sweep: about 5–10 minutes while PRs are arriving, 20–30 minutes once the queue is empty. Without one, run one sweep and stop. Never end a waiting turn with nothing armed. Stop after two empty passes when the owner asked for a single clear-out rather than a watch.

## Stop and ask

- `AGENTS.md` names a merge rule that `origin/main` does not have: hold everything and ask.
- Another session is merging in the same repo and the merges race (a `--match-head-commit` rejection or a rejected push more than twice): stop and report.
- Two retries fail on the same PR: hold it with the evidence and move on.

## Closeout

The session handoff lists every PR merged with its merge SHA, every PR held with its `Blocked by:` line, and any PR left waiting on a busy branch.
