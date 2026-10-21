---
name: update
description: Force a STATUS.md continuity update right now — refresh the Active Threads table, append a dated session-log entry, record lasting lessons, and commit. Use whenever the user types /update, at the end of a work session or day, before a risky operation, a server reset or reboot, or before switching tools or accounts — any time context that exists only in this session could be lost.
---

# /update — Force a continuity update to STATUS.md

Run this even if the session feels incomplete or the work is half-done. The
point is to capture real, possibly messy current state, including "blocked"
and "half-done", so that a lost session, a reboot, or a switch to another
tool doesn't lose context that only exists in this conversation. If nothing
changed, still write the entry and say so, so a future reader knows the
update ran and found nothing, rather than not knowing whether it ran at all.

Work through these steps in order.

## 1. Re-read the status file in full, now

**Which file:** usually `STATUS.md`. If `CLAUDE.md` names a different status
file for the current branch (e.g. a long-running feature branch with its own
`STATUS_<NAME>.md`), that file is the one this skill updates, and everything
below that says `STATUS.md` means that file. Follow `CLAUDE.md`'s rules about
which control documents may be edited on that branch. If it says they are
edited only on `main`, don't touch them here; list any needed change as an
open item instead.

Don't assume its content from earlier in the session. It may have been
changed by another session, another tool, or a `git pull`. If you are working
from a fetched copy rather than the file on disk (for example
`raw.githubusercontent.com`), note that it can lag behind the latest push.

## 2. Establish what actually changed — from evidence, not memory

- In a repo: check `git status`, `git diff`, and `git log` since the last
  session-log entry. Count every tracked file, including tooling and config
  (`.claude/`, settings files, `.gitignore`, MCP/plugin config), not just
  content and code. Installer-made changes count too, and need recording
  *more*, because nobody wrote down why at the time.
- List decisions made, problems found, tasks completed, tasks newly blocked,
  and anything discovered but not yet tracked.
- Re-derive any numbers you plan to record (files done, items remaining,
  counts) from the files on disk. Don't copy running tallies from the
  conversation; they drift.

## 3. Update the Active Threads table

- **Done** only when verified. Write the evidence, not "should be done":
  the command that confirmed it, the commit hash, the count it produced.
  Never record something as done, built, committed, or tested unless you
  have confirmed it in this session. A task wrongly recorded as done is
  worse than one left open, because it suppresses the re-check that would
  catch it.
- Make each "done" understandable to someone with zero context, without
  them re-deriving it.
- **Be honest about in-progress status.** "Blocked", "in progress", "not
  started", and "written but untested" mean different things. Don't round
  up to "in progress" just because something was touched. Name what a
  blocked item is waiting on, and who.
- Add any new items surfaced this session.
- Remove an item only when it is genuinely finished with no follow-up risk.
  Otherwise keep it and say why it isn't fully closed.
- Correct any existing row you now know to be stale or wrong, and say what
  changed, rather than leaving it to contradict the new entry.

## 4. Append a dated session-log entry

- Follow the file's existing heading format (e.g. `## Updates — YYYY-MM-DD`)
  and its date order.
- Summarize outcomes, not the conversation: what was done, what's still
  open, and decisions with their reasons.
- Include anything a future session needs to avoid redoing today's work
  (e.g. "checked X, confirmed Y; don't re-check unless Z changes").
- End with a short "Still open" list.

## 5. Record lasting lessons separately

If anything this session fits the Known Issues / Lessons Learned pattern (a
fact that was true when written and silently went stale, a surprising root
cause, a mistake worth not repeating), add it there, not only in the session
log, which becomes chronological noise. If the project's `CLAUDE.md` has a
documentation-drift log and the lesson is about a stale stated fact, record
it there. Always include the structural fix, not just what went wrong.

## 6. Keep headers and cross-references true

- Update the file's "Last updated" date (and `CLAUDE.md`'s, if you touched it).
- If this session changed something another control document states (paths,
  branch names, commands, file inventories), update that document too, or
  record the mismatch as an open item. Don't leave two documents disagreeing.

## 7. Check the write landed intact

Re-read the file after writing. Confirm it isn't truncated or emptied, the
new entry and table rows are present, and the encoding is still plain UTF-8.

## 8. Commit, or hand over paste-ready text

- **With repo write access:** commit `STATUS.md` (and `CLAUDE.md` or other
  documents if touched). If related work is still uncommitted, include the
  update in that same commit. If the work is already committed, commit the
  update on its own (e.g. `STATUS.md: continuity update`). Don't leave it
  staged. Push only if the project's rules or the user say to; some projects
  deliberately hold pushes.
- **Without write access** (e.g. a chat session with no repo connection):
  present the updated sections ready to paste: the full new or changed
  Active Threads rows, the complete session-log entry, and any Known Issues
  addition, with a note on where each goes.

## 9. Report back concisely

A short summary of what changed in `STATUS.md` (rows added, closed, or
corrected; the entry's headline; whether it was committed), not a restatement
of the whole file.
