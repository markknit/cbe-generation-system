# Round 2 brief: apply teacher journal decisions to one revised module

Repo: /home/markk/ares/cbe-generation-system. Workspace (the REVISED copy): data/revised_2026-10_full.
Always run with `export CBE_REVISED_DIR=/home/markk/ares/cbe-generation-system/data/revised_2026-10_full`.
Never edit generators/data/, never commit, push, sync or call any API. Edit ONLY through `python3 scripts/revise_apply.py apply MODULE RECORDS.json` (use `--dry-run` first; see the docstring at the top of that script for the record format). Use /home/markk/ares/cbe-generation-system/venv/bin/python. Put scratch files in your own scratchpad subfolder.

## What happened
Round 1 (2026-10-17) revised each module. Its edits are already in modules/<m>_data.js, logged in change_records/<m>.json (kind=edit/set = changed; kind=flag = NO change made, teacher to decide). Teachers then reviewed journals. Their decisions for your module are in
`data/revised_2026-10_full/round2/slices/<m>.json`, keyed by journal item id (a record id like `bio_1_1-014`, or a group like `bio_1_1 G3`; a group stands for all records with that `group` key).
Read also data/revised_2026-10_full/REVIEWER_BRIEF.md and GUIDELINES_14.md (the rules the round-1 reviewers followed), the journal text for context in journal/Journal_<Subject>.docx or journal/Flagged_Items_<Subject>.docx if useful (use `venv/bin/python -I` with lxml; do not modify), and the audit/<m>.md file.

Decision meanings: ACCEPT / UNMARKED / ACCEPT+COMMENT = teacher accepts the round-1 change, or, for a kind=flag item, accepts the flag's suggestion. EDIT = teacher wants the change adjusted; `typed` holds their instruction. EDIT? = typed text with no box ticked: treat as an edit request if it is a concrete change, otherwise as a note.

## What to do
1. Accepted edits need nothing (already in the module). For an accepted kind=flag item whose "why" proposes a concrete fix, apply that fix as a new record (kind=edit/set) with the flag's group/why noted.
2. For every EDIT / EDIT? item: apply the teacher's typed instruction to the module through new records (reference the journal item id in `why`; cite the teacher). Change the module consistently: if a lesson's duration or content changes, update every field and the totals that depend on it (the Summary Table is re-derived by apply).
3. SCIENCE/FACT SAFETY: teachers are the authority on Kenyan curriculum and classroom practice, but if a requested change states a scientific/mathematical fact you cannot verify, or contradicts the KICD PDF (data/raw/curriculum_pdfs/), do NOT write it as fact: record a kind=flag with the request and your concern. Never invent KICD wording, page numbers or quotes: check the PDF (pdftotext) or flag.
4. FOUR-LEVEL RUBRIC: teachers asked for four CBE levels (Exceeds, Meets, Approaches, Below Expectations). The partner contract only has three fields; this is on hold pending the partner. Make NO rubric structure change; list those items as "deferred: rubric" in your report. Do keep any level-name wording round 1 already put in descriptors.
5. Items that are notes ("verify before teaching", "check with the teacher") rather than changes: no edit; list them in the report.
6. Requests you cannot do (need KICD source you cannot find, contradict another teacher request, need a decision, or need a new resource): record a kind=flag, and list under "needs input".
7. After applying, run `python3 scripts/revise_build.py` for your module only if that script accepts a module argument (read its usage first); check the output validates (node scripts/validate_corpus.js if it can take the revised dir, otherwise report what you could not run).

## Report (max 25 lines), exactly:
MODULE; counts (accepted-no-change / edits applied / flags added / deferred rubric / notes / needs-input); then bullet list of each needs-input item with item id, what the teacher wrote (quote), and the specific question. Report any rejected apply edits. Do not paste diffs.
