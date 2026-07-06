---
name: update
description: Force an update to STATUS.md's Active Threads table and session log right now, capturing current project state before a session ends, a server resets, or work switches to a different tool. Use whenever continuity might otherwise be lost — end of day, before closing a session, before a risky operation.
---

# /update — Force a continuity update to STATUS.md

When this command is invoked, do the following, in order:

1. **Review this session's actual work** — files changed, commands run,
   decisions made, problems found, anything still unresolved. Don't rely
   on summarizing from memory alone; check `git status` / `git diff` /
   `git log` if there's any uncertainty about what actually changed.

2. **Update the `Active Threads` table** near the top of `STATUS.md`:
   - Mark completed items as done, with enough detail that someone with
     zero context could tell what "done" means without re-deriving it.
   - Update in-progress items' status honestly — "blocked," "in
     progress," and "not started" are meaningfully different; don't
     round up to "in progress" just because something was touched.
   - Add any new items surfaced during this session that aren't yet
     tracked.
   - Remove items only when they're genuinely finished with no follow-up
     risk — otherwise leave them and note why they're not fully closed.

3. **Append a dated session-log entry** at the bottom of `STATUS.md`,
   following the existing `## Updates — YYYY-MM-DD` format. Include what
   was done, what's still open, and anything a future session would need
   to know to avoid re-deriving work already done today (e.g. "checked X,
   confirmed Y — don't re-check unless something changed").

4. **If anything discovered today fits the "Known Issues / Lessons
   Learned" pattern** (a fact that was true and silently went stale, a
   surprising root cause, a mistake worth not repeating) — add it there
   too, not just in the session log. The session log is chronological
   noise after enough time passes; Known Issues is where lasting lessons
   belong.

5. **Commit the update.** If this session already has uncommitted related
   work, include the `STATUS.md` update in that same commit. If the
   related work is already committed, commit `STATUS.md`'s update on its
   own with a clear message (e.g. `"STATUS.md: continuity update"`).

6. **Report back concisely** — a short summary of what changed in
   `STATUS.md`, not a restatement of the whole file.

**Do this even if the session feels incomplete or the work isn't fully
finished.** The entire point of this command is to capture real,
possibly-messy current state — including "blocked" or "half-done" — so
that a lost session, a server reset, or a switch to a different tool
doesn't lose context that only existed in this conversation.
