# Execution contract and commands

Engine: `operations/scripts/autonomous_work.py`, your own queue engine (it does not ship with this kit; the commands below show the interface the method assumes). Runtime requires Python 3.11+ (`tomllib`) and existing PyYAML; claims use POSIX `flock`. No arbitrary command executor is installed: the agent uses the card's appropriate tools under session authority.

## Cards

A level-3 stable-ID heading plus fenced `yaml` record is canonical. The common schema example is unheaded and ignored. Required fields are `id`, `title`, `source`, `readiness`, `readiness_reason`, `scope`, `non_goals`, `inputs`, `dependencies`, `decisions`, `acceptance`, `verification`, `delivery`, `human_gate`, `authority_profile`, `checked_at`, `checked_against`, `evidence`, and `last_run`. Add exact project-relative `write_scope` paths (no traversal), plus optional `tools`, `resources`, and `worktree_required`.

Local sources are `path#stable heading or exact task identity`; GitHub issue sources may use human or API URLs. Inputs are project-relative file paths or explicit GitHub issue URLs. GitHub repositories must be explicitly registered in `github_repositories`; a board URL alone never authorizes unrelated issues. Closed/unavailable remote sources block work.

Ready requires complete live hashes, a fresh authored `checked_at`, meaningful fields, delivered dependencies, and available tools. Observed hashes include `contract:<id>` for substantive scope/decision/verification changes. Keep the card in needs-preparation while collecting hashes; after semantic revalidation only, stamp the complete `inspect_project(config)['cards'][i]['hashes']` through `stamp_card`; it preserves readiness. Then promote by a separate revision-checked card update. Mechanical refresh never stamps or promotes. A timestamp alone is insufficient.

Readiness is `ready`, `needs-preparation`, `blocked`, `delivered`, or `retired`. Claims have separate `claimed`/`running`/`verified`/`blocked`/`interrupted` run states. Evidence and local delivery remain separate from owner review, PR, merge, publication, and rig proof.

## CLI

From the project root (set `--registry` to its absolute path elsewhere):

```sh
python3 operations/scripts/autonomous_work.py refresh --registry operations/agent-config/autonomous-projects.toml --project my-project --json
python3 operations/scripts/autonomous_work.py select --registry operations/agent-config/autonomous-projects.toml --project my-project --limit 2 --json
python3 operations/scripts/autonomous_work.py claim --registry operations/agent-config/autonomous-projects.toml --project my-project --card CARD --owner SESSION --run-id RUN --authority-acknowledged --json
python3 operations/scripts/autonomous_work.py checkpoint --registry operations/agent-config/autonomous-projects.toml --project my-project --card CARD --run-id RUN --evidence 'Baseline or verified milestone with artifact references' --json
python3 operations/scripts/autonomous_work.py finish --registry operations/agent-config/autonomous-projects.toml --project my-project --card CARD --run-id RUN --delivery 'Tested local artifact' --verification-evidence operations/reports/VERIFICATION.md --json
python3 operations/scripts/autonomous_work.py next --registry operations/agent-config/autonomous-projects.toml --project my-project --card CARD --json
```

Inspect `show`/`health` without writes; `refresh` writes only a derived local receipt. Selection is finite and cannot overwrite an active selection. Record a blocker with `finish --outcome blocked --delivery 'Exact missing prerequisite'`, then advance to an independent selected item. `--outcome interrupted` preserves the claim and its artifacts for recovery.

A verified finish requires persisted verification evidence, not merely a started checkpoint. It hashes evidence and final owned files. The lead still must verify that the evidence demonstrates the acceptance contract; software cannot judge scientific/editorial acceptance.

## Concurrent work and recovery

Every registered project uses an ignored runtime directory. The portfolio registry uses one shared claim directory for cross-project aliases/resources; claims carry project/card/session/run identity and resolved owned paths. Queue updates use `load_queue` revision followed by `update_card(config,id,updates,expected_revision)` or `replace_queue`; a stale revision fails. Cooperating agents use the same locks; reread before mutation and preserve unexpected human edits.

`recover --card CARD` reports owner heartbeat/liveness, current input eligibility, changed paths since checkpoint, and preserved write hashes. Never automatically reap a stale claim. Inspect diffs, test artifacts, task/remote state, and owner session. Save the reviewed `preserved_write_hashes` mapping to a local JSON file; `resume --reviewed-hashes FILE --owner NEW_SESSION` resumes only if those current hashes still match and the owner is no longer live. Preserve the original run and checkpoints; do not start another run over partial work.

CLI process IDs are diagnostic; the session identity and heartbeat remain necessary because a short-lived CLI process can end while its agent continues. A stale heartbeat alone grants no permission to steal work. A rig or bench lock file always wins.

## Closeout and maintenance

Reconcile delivered/blocker cards by CAS, revalidate affected readiness, and refresh the project even for no-change closeout. Receipts contain queue/input/contract hashes, checked sources, card results, last successful refresh, and the observation reason. `check_closeout(registry,changed_paths,project_id)` detects missing/expired/changed receipt coverage for affected queue inputs. Your session validator should invoke it for queues the project owns.

`python3 operations/scripts/autonomous_health.py --weekly` refreshes derived portfolio/health reports and a bounded source-inventory proposal. `--no-write` inspects without mutations. A scheduled daily job is report-only; a weekly run adds the inventory. It never promotes cards, edits tasks, claims work, executes queues, commits, or publishes. Semantic discovery stays an explicit `prepare more autonomous work` request.
