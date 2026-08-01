Stage all changes, commit with a descriptive message, push to origin main, then record the session state in STATUS.md and push that too.

Steps:
1. Run `git status` and `git diff` to understand what changed
2. Check for oversized files before staging: `find . -size +50M -not -path './.git/*' -not -path './venv/*'`
   Never commit `data/ares_index/ares_content.db`, `venv/`, or `.env`
3. Stage all modified and new files with `git add -A`
4. Write a clear commit message summarising what changed and why
5. Commit and push to origin main
6. Update `STATUS.md` (not CLAUDE.md — status lives in STATUS.md by project rule):
   - Update the **Active Threads** table: what is in progress, blocked, or done
   - Append a dated session-log entry describing what changed this session
   - Update the Summary/per-subject coverage tables if lesson counts changed
7. Commit and push the updated STATUS.md to the same branch

Only update CLAUDE.md if a *durable* fact changed (repository layout, document
format standards, curriculum authority, ARES host/URL scheme, rigor level).
Current status must never be restated in CLAUDE.md — that duplication has
caused stale-fact incidents in this project.
