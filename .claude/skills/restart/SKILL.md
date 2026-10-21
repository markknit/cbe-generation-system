---
name: restart
description: Re-ground a new, resumed, or long-running session against actual current state before doing anything else — re-read CLAUDE.md, STATUS.md, WORKFLOW.md and any recent HANDOFF doc from disk, run live Step 0 checks, and report drift. Use when the user types /restart, at the start of a session or work day, after a break, reboot or server reset, before a consequential operation (bulk generation, push, deploy), or whenever earlier assumptions may have gone stale. Does not discard conversation history.
---

# /restart — Continuity verification checkpoint

This is a **verification checkpoint, not a memory wipe.** It keeps the
conversation and the decisions already made in this session. It re-checks
them against the current state of the disk and repo, and flags anything that
no longer matches.

`/restart` and `/update` complement each other. `/update` records new state
into `STATUS.md` after work is done. `/restart` checks existing state before
work continues. Neither replaces the other.

Verification only: `/restart` never runs generation, deployment, pushes, or
any other command that produces content or changes state.

## 1. Re-read the control documents from disk, not memory

Read these fresh, even if you read them earlier in this session:

- **`CLAUDE.md`**, in full: operating standards, working practices, and the
  **rigor level** in effect (e.g. a "Project Rigor Assessment" section).
- **`STATUS.md`**: the full **Active Threads** table, the latest session-log
  entries, and **Known Issues / Lessons Learned**. This is the source of
  truth for current state. Training data, this session's assumptions, and
  summaries carried over from other conversations are not.
- **The branch's own status file, if any.** If `CLAUDE.md` names a different
  status file for the current branch (e.g. `STATUS_<NAME>.md`), read it in
  full as well; it is the source of truth for that branch's work. Also read
  `main`'s current `STATUS.md` (`git show main:STATUS.md`), because work on
  `main` since the branch last merged it can change what this branch is
  building on.
- **`WORKFLOW.md`**, if present: in particular the **Environment Reference**
  table (branch, paths, hostnames, sync destinations), which wins over any
  other document that restates those values.
- **The most recent `HANDOFF_*.md`**, if one exists and is still active (not
  marked superseded or complete in `STATUS.md`). Treat its "Locked
  decisions" as binding unless the user says otherwise, and note which
  phase or gate it was stopped at.

## 2. Run the Step 0 live checks

- **Project Step 0 block:** if `WORKFLOW.md` (or `CLAUDE.md`) contains a
  Step 0 verification block, run it as written.
- **Missing block:** if the docs *refer* to a Step 0 block but you can't
  find one, that is drift in itself. Report it in step 4. Don't skip
  verification because of it.
- **Baseline checks:** always run these, whether or not a project block
  exists:
  ```bash
  git branch --show-current
  git log --oneline -5
  git status
  git fetch --quiet && git status -sb   # ahead/behind remote; skip if offline
  ```
- **On a branch other than `main`:** also run
  `git rev-list --count HEAD..main` to see how many `main` commits the
  branch hasn't merged yet. If `CLAUDE.md` says to merge `main` in at the
  start of each session, report the count and propose the merge. Don't run
  it unasked, because `/restart` only verifies.
- **Expected branch:** compare the current branch with the one the
  Environment Reference table expects *for this working folder*, not with
  `main` by default.
- **Spot-check volatile facts:** check anything the Environment Reference
  table or the next task depends on (an output path, a hostname, a tool
  such as `soffice`, a data file the task will read) against the real
  filesystem.

## 3. Compare against this session's operating assumptions

Check whether anything said, planned, or assumed earlier in this session, or
in the handoff or summary it was resumed from, conflicts with:

- the current branch, the latest commit, and the ahead/behind state;
- any Active Threads status the session took as still accurate (for
  example, something the session thinks is "in progress" that is now
  marked done, blocked, or on hold);
- file paths, output directories, hostnames, model names, or naming
  conventions referenced earlier;
- uncommitted changes that this session doesn't know the origin of;
- the date and content of the latest session-log entry, which shows
  whether another session or tool has worked here since.

## 4. Report before acting

Before proposing any next action, report briefly:

- current state, what's in progress, and what's blocked (and on what);
- the rigor level in effect;
- the active handoff, if any, and where it stopped;
- the result of the checks.

Then:

- **Everything matches:** confirm alignment in a line or two and carry on
  with the task.
- **Something doesn't match:** stop. Name each mismatch as old value vs
  current value, with the source of each, and ask how to proceed. Don't
  quietly patch over it.
- **A control document is stale** (contradicted by what Step 0 just found):
  flag it explicitly and treat fixing it as the first task, following the
  Known Issues / Documentation Drift Log pattern, including the structural
  fix. Don't continue on a document known to be stale.

## Claude.ai chat equivalent (no shell access)

When `/restart` is typed in a claude.ai conversation for the project:

1. Re-fetch `STATUS.md` and `CLAUDE.md` (and `WORKFLOW.md` if the task
   depends on it) from GitHub `main`, even if they were already fetched in
   this conversation. A fetched copy can lag behind the most recent push.
2. Compare them against anything assumed earlier in the chat, and report any
   drift, as in steps 3–4.
3. Say explicitly that the live checks (branch, log, status, paths) need
   shell access this interface doesn't have. If the task depends on current
   git or filesystem state, ask the user to run the Step 0 block on the
   server and paste the output before going further.
