# Shared bench lock

How several agent sessions share one checkout that a live application holds, such as a game-engine editor. Only one session at a time may switch branches or edit there.

## When you need it

Use it when two things are true:

- more than one agent session works on the same project at once, and
- one checkout is held open by a live application, so a branch switch or a file write under it affects everyone.

Call that checkout the bench. Work that does not need the live application happens in a separate git worktree and needs no lock. See `docs/principles.md` and `docs/architecture.md` for why the work is split this way.

## The tools

Both tools live in `tools/`. Both need `CLAUDE_CODE_SESSION_ID`. Claude Code sets it. Another harness must export its own stable session id under that name.

`bench-lock` has four commands:

| Command | What it does |
|---|---|
| `bench-lock take --purpose "..."` | Takes the lock in one atomic step. Exits 1 if another session holds it. Also takes `--branch` and `--owner`. |
| `bench-lock wait --purpose "..." [--timeout S] [--poll S]` | Waits until the bench is free, then takes it. Exits 3 on timeout. Run it in the background; its exit is the signal. |
| `bench-lock release [--force]` | Deletes the lock if this session holds it, and prints where to return the bench to. `--force` is only for a lock the bench owner says is abandoned. |
| `bench-lock status` | Prints `free`, `yours`, or `held by another chat` (exit 1). |

`chat-name` labels the session so the lock shows who holds it:

- `chat-name "short name"` sets the name (40 characters at most).
- `chat-name --get` prints it.
- `chat-name --clear` removes it.

Set a name before you take the lock. The name is stored in `${TMPDIR:-/tmp}/ghostty-pane-<session id>.name`, so a status-line script can read it.

## What the lock file holds

`.bench-lock` sits at the root of the main checkout. It is found through the shared `.git`, so the tools work from any worktree. It is not tracked by git, so add it to `.gitignore`. It has seven keys:

- `owner`, `session`, `name`: who holds it.
- `branch`, `purpose`: what they are doing.
- `acquired`: when, in UTC.
- `return_to`: the branch and commit the bench was on, so the next session can put it back.

Nobody writes the lock file by hand. Use `take`, `wait`, and `release`, because only they do the atomic check and keep the format other sessions read.

The tools never switch branches. After `release`, check `git status --short` before you check anything out.

## Install

Put both tools on `PATH`. For example, from the root of this repository:

```sh
ln -s "$PWD/tools/bench-lock" ~/.local/bin/bench-lock
ln -s "$PWD/tools/chat-name" ~/.local/bin/chat-name
```

`bench-lock` calls `chat-name` by name, so both must be found on `PATH`. The tests are in `tools/test_bench_lock.py`.
