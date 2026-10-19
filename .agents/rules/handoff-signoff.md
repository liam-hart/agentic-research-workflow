# Handoff sign-off

Every session appends a `## Walkthrough & Verification` section to its handoff and closes it with a sign-off as the final non-empty line:

```
Sign-off: <Model Name> (effort: <level>)
```

Read the model and effort from the live session's own status. Write `unknown` when you cannot verify a value. Never infer either one from how hard the task was or how thorough the work felt.

Use the model's display name, spelled the same way every time, so the trail stays searchable.

In Claude Code, read effort from the `/effort` output in the conversation or the status bar, never from the saved default in `settings.json`. A handoff carries one sign-off, at the end: if the latest handoff is already signed off, start a new file instead of appending.
