# Round 2 brief: fix Final Explanation (FE) issues found by the review pass

Repo: /home/markk/ares/cbe-generation-system. Workspace (the REVISED copy): data/revised_2026-10_full.
Always set `export CBE_REVISED_DIR=/home/markk/ares/cbe-generation-system/data/revised_2026-10_full` IN THE SAME SHELL COMMAND as every revise_apply / revise_build call (otherwise an old workspace is used silently). Use `/home/markk/ares/cbe-generation-system/venv/bin/python`. Never edit generators/data/, never commit, push, sync, or call any API. Edit ONLY through `scripts/revise_apply.py apply MODULE RECORDS.json` (always `--dry-run` first; record format = the docstring at the top of that script). Scratch files go in your own scratchpad subfolder.

## Background
Round 2 changed lessons (40-minute trims, splits, replaced lessons, science/fact fixes) and, for Mathematics, replaced the FE rubric by the KICD rubric. A review-only pass (an independent model reviewer, no edits made) compared each module's FE with its revised lessons. Its findings per module: `data/revised_2026-10_full/fe_review/<module>.json` = {"issues": [{"where","problem","kind"}]}.
- kind `final_explanation`: a defect the FE's author can fix (wrong arithmetic, prompt that contains its own answer, FE disagrees with the lessons, scratch text, science/maths error, inconsistent numbers).
- kind `lesson_sequence`: the LESSONS contradict each other or contain an impossible figure.
The reviewer is a model: roughly a third of its findings are false positives or style nitpicks. Do not trust it; verify each one yourself.

## For each module assigned to you
1. `venv/bin/python scripts/revise_apply.py dump MODULE /your/scratch/MODULE.json`, read the FE (sections[i].prompt / exemplar / instructions) and the relevant lessons.
2. For EACH issue of kind `final_explanation`: check it yourself (recompute the arithmetic; compare with the lessons; check whether the prompt really contains its answer). Then decide:
   - REAL and the fix is clear (a number, a sentence, a wording): write a `kind: "edit"` record (target `final_explanation`, path like `sections[2].prompt` or `sections[2].exemplar`, exact `old` text that occurs ONCE, `new` text). Keep the student prompt free of answers; keep prompt and exemplar consistent with each other and with the lessons; change the minimum; never touch `rubric`.
   - NOT real / style / reviewer error: no edit; list it in your report with one line why.
   - REAL but fixing needs a science/maths fact you cannot verify, or a decision about what the teachers want, or a rewrite larger than a few sentences: write a `kind: "flag"` record (why = the problem and your suggested fix).
3. Issues of kind `lesson_sequence`: do NOT edit lessons. Write ONE `kind: "flag"` record per issue (target `lesson`, `lesson`: the number named, path `title` is fine for the location; why = the issue).
4. Every record: `id` = `<module>-r2-fe-NNN` (NNN continues from 001, unique), `criteria` [14] (consistency) or [6] for science errors, `category` "consistency" (or "science" with a `reference` for science errors), `severity` "minor" or "substantial", `teacher_decision` true, `group` "R2-FE-REVIEW" with a one-line `group_headline` on the first record of the module, `why` = the reviewer's finding in plain words + what you changed and why. Cite the KICD/known fact for a science change; if you cannot, make it a flag.
5. Dry-run, apply, then `venv/bin/python scripts/revise_build.py MODULE` (must show no PROBLEMS) and `CBE_DATA_DIR=data/revised_2026-10_full/modules node scripts/validate_corpus.js MODULE` (PASS).

## Report (max 20 lines)
Per module: issues by reviewer / edits applied / flags added / dismissed as not real (one-line why each) / lesson_sequence flags. Then any rejected apply edits and anything that needs Mark or the teachers. Do not paste diffs.
