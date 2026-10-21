This project covers presentation generation for the Kenya CBE lesson plans.
The work happens on the `presentations` branch of
`markknit/cbe-generation-system`, run on jhm-spark through Claude Code.
Lesson-plan work continues on `main`, which belongs to the separate project
"Kenya CBE Lesson Plan Development".

At the start of every conversation, before answering anything substantive,
fetch these to get current state. Don't rely on project knowledge files or
earlier chat summaries for these facts, because they go stale:

https://raw.githubusercontent.com/markknit/cbe-generation-system/presentations/STATUS_PRESENTATIONS.md
https://raw.githubusercontent.com/markknit/cbe-generation-system/presentations/HANDOFF_presentations_2026-10-21.md
https://raw.githubusercontent.com/markknit/cbe-generation-system/presentations/docs/presentations/OVERRIDES.md
https://raw.githubusercontent.com/markknit/cbe-generation-system/presentations/docs/presentations/BUILD_MANUAL.md
https://raw.githubusercontent.com/markknit/cbe-generation-system/main/STATUS.md
https://raw.githubusercontent.com/markknit/cbe-generation-system/main/CLAUDE.md

If a newer HANDOFF_presentations_*.md exists on the branch, STATUS_PRESENTATIONS.md
will name it; fetch that one instead.

STATUS_PRESENTATIONS.md's Active Threads table is the source of truth for
presentation work. Main's STATUS.md is the source of truth for the lesson
plans the presentations are built from. Main's CLAUDE.md, in particular
"Branch Policy — presentations", holds the binding rules. The HANDOFF holds
the locked decisions and the phased plan. BUILD_MANUAL.md is the teachers'
design spec; where it conflicts with CLAUDE.md or OVERRIDES.md, OVERRIDES.md
wins. A fetched copy can lag a few minutes behind the latest push.

Standing rules (details are in the HANDOFF; if this list and the fetched
files disagree, the files win and you should say so):
- Presentations teach the topic, not the process, while still using the
  Predict / Observe / DQB / Model structure. The speaker notes must let a
  teacher run the lesson even without a projector.
- ARES links go on the slides as a clickable icon (no visible long URL),
  with alt text and a label; the plain URL goes in the speaker notes. Only
  ares.local links, taken from the lesson data; no placeholders.
- Footer and credit text come only from config/attribution.yaml
  (`slide_footer` on every slide, the full `lesson_footer` on the title and
  last slides). Never hardcode attribution.
- Science errors, outdated terms and inconsistencies are flagged in the
  build log, never fixed in the deck. Lesson content changes only on main.
- Never propose regenerating or editing lesson-plan content from this
  project, and never change shared pipeline files or control documents from
  the presentations branch.
- Decks and PDFs are not committed to git; they are shared through Drive.
  Only a small sample set goes in data/outputs/presentations/_samples/.
- Scope: Grade 10 Biology, Chemistry and Physics first. Mathematics last.
  Teacher review of the example decks does not gate the generator build.
- Keep everything compatible with the partner contract
  (ares-contract.schema.json).

/update: summarize this conversation's work as paste-ready additions to
STATUS_PRESENTATIONS.md (Active Threads rows and a dated session-log entry),
following that file's format, for Mark to commit on jhm-spark. List any
needed change to a control document (CLAUDE.md, WORKFLOW.md, STATUS.md,
attribution.yaml) as an open item for main.
/restart: re-fetch the six files above, compare them with anything assumed
earlier in this chat, and report drift. Live git checks need jhm-spark; ask
Mark to paste the Step 0 output if the task depends on it.
