---
name: restart
description: Re-ground a session against actual current state before continuing work. Re-reads STATUS.md's Active Threads, CLAUDE.md, and WORKFLOW.md, then runs WORKFLOW.md's Step 0 live checks and reports any drift. Use when continuing a session, at the start of a work day, after a server reset, or whenever you are about to act on state that was established earlier and may have gone stale. Does not discard conversation history.
---

# /restart — Continuity Verification Checkpoint

## Purpose

Forces a fresh read of the project's control documents plus a live
verification pass, so a session can confirm it is still aligned with
actual current state before continuing — rather than operating on
assumptions that were true earlier in this session, or in a prior one.

This is a **verification checkpoint, not a memory wipe.** It does not
discard conversation history or in-session decisions. It re-grounds
them against current disk/repo state and flags anything that no longer
matches.

`/restart` and `/update` are complementary, not overlapping:
`/update` records new state into `STATUS.md` after work is done.
`/restart` checks existing state before continuing.

## When to use

- At the start of a work day, before continuing prior work
- Before any operation with real consequences (bulk generation, git
  push, deployment) if the session has been running a while
- Any time something in this conversation seems to conflict with what
  was just said or done
- On demand, whenever drift is suspected

## What /restart does (Claude Code)

1. **Re-read control documents from disk, not memory:**
   - `STATUS.md` — full "Active Threads" table
   - `CLAUDE.md` — in full
   - `WORKFLOW.md` — Environment Reference table specifically

2. **Check for a recent `HANDOFF_*.md`** in the repo root (see
   `HANDOFF_TEMPLATE.md` for the shape). If one exists and isn't clearly
   superseded (a session-log entry in `STATUS.md` marking its work done),
   read it in full and treat its "Locked decisions" section as binding for
   this session unless the user says otherwise.

3. **Run WORKFLOW.md's Step 0 verification block:**
   ```bash
   git branch --show-current
   git log --oneline -3
   git status
   grep -h "outputDir" generators/data/*.js | sort -u
   which soffice
   ```
   **Known gap (2026-08-18):** no numbered "Step 0" section currently
   exists in `WORKFLOW.md` or `docs/WORKFLOW.md` despite this and other
   docs citing one — run the commands above directly; don't go looking
   for a section that isn't there yet. See `STATUS.md` Known Issues.

4. **Compare against this session's operating assumptions.** Check
   whether anything said or planned so far in this session conflicts
   with:
   - The current git branch / latest commit
   - The current `outputDir` value(s)
   - Any Active Threads item status the session assumed was still
     accurate
   - Any file path, hostname, or naming convention referenced earlier
     in this session
   - Anything in a `HANDOFF_*.md` read in step 2

5. **Report, don't silently proceed:**
   - Everything matches → state alignment is confirmed, in one or two
     lines, and continue with the task at hand.
   - Something doesn't match → stop, name the specific mismatch (old
     value vs. current value, with source), and ask how to proceed
     before taking further action. Do not quietly patch over it.

## What /restart does NOT do

- Does not forget or discard the conversation so far.
- Does not run generation, deployment, or any content-producing
  commands — verification only.
- Is not a substitute for reading `STATUS.md`'s Active Threads at the
  start of a session — that's still mandatory. `/restart` is for
  re-checking mid-session or day-to-day, not a replacement for it.

## Claude.ai chat equivalent

Typed as `/restart` in a Claude.ai conversation in this project:

1. Re-fetch `STATUS.md` and `CLAUDE.md` from GitHub `main` (same URLs
   fetched at conversation start), even if already fetched earlier in
   this conversation. If a `HANDOFF_*.md` is referenced from `STATUS.md`
   as still open, fetch and read that too.
2. Compare against anything assumed earlier in this chat.
3. Report any drift found.
4. Explicitly note that live verification (git log, branch,
   `outputDir` grep) requires shell access this interface doesn't
   have. If the task at hand depends on current git/filesystem state,
   ask Mark to run WORKFLOW.md's Step 0 block on jhm-spark and paste
   the output before proceeding.
