# Delegation decision

Applies to any multi-step task. Run this before the first edit.

1. **Enumerate.** List the bounded sub-tasks. One item means there is nothing to delegate.
2. **Test each slice.** Delegate only when all five hold:
   - **Verifiable**: the lead can check the output against a stated criterion without redoing the work.
   - **Not judgment**: no architecture, scientific interpretation, priority, or final status claim.
   - **Not coupled**: it does not depend on decisions still in flight, and it writes no file another slice writes.
   - **Worth isolating**: more than a couple of tool calls. A worker starts cold, so a fan-out costs several times the tokens of doing the work inline.
   - **Safe to isolate**: read-only, or it writes only files named in its brief. Never a commit, a push, or a publication.
3. **Delegate the slices that pass**, and keep working while they run.
4. **State one reason for every slice kept inline.**

Subagents never certify their own work. The lead checks every claim it relies on. Retry at most twice; scope drift is a hard stop; real ambiguity comes back as a question.
