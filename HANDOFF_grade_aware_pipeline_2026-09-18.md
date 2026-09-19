# HANDOFF — Grade-Aware Pipeline (Kenya CBE Lesson Plan Generation System)

**Revision:** 1 (2026-09-18)
**Supersedes:** nothing — new work
**Execution target:** Claude Code on `jhm-spark`, `/home/markk/ares/cbe-generation-system`
**Prepared for:** Mark (markk@areseducation.org)

```bash
cd /home/markk/ares/cbe-generation-system
# place this file, and the two .patch files that came with it, at repo root, then
# work through §7 below. Do not skip Phase 0.
```

---

## 0. Why this document exists

A partner's Claude agent (building a separate "Lesson3" editor app that vendors a
read-only copy of this repo's generator code) flagged three hardcoded `GRADE 10`
strings in `build_docs.js`. Tracing that report back to this repo (via a public
clone, verified against `main` at commit `3ca9f25`) showed it was the visible tip
of a much larger problem: **the entire content-generation pipeline assumes Grade
10 everywhere**, because only Grade 10 existed when it was written. Nobody put
that assumption there carelessly — it just was never revisited.

This document scopes and delivers the fix: making `generate_substrand.py` and
`build_docs.js` grade-aware, as a self-contained plumbing change that does **not**
require the actual Grade 11 curriculum content to be ready (confirmed explicitly
with Mark — see §4). Populating real Grade 11 data is intentionally left as a
separate, later phase (§7 Phase 4).

**The single highest-severity finding, worth reading even if nothing else is:**
`SUBSTRAND_NAMES` was keyed by subject only, not by grade. Since Mark confirmed
Grade 11 reuses Grade 10's exact strand/sub-strand numbering, a Grade 11 run for
e.g. `biology 2.1` would have **silently** pulled Grade 10's name for that slot
("Plant Nutrition") instead of Grade 11's actual topic ("Reproduction in
Plants") — confirmed against the real KICD source PDF, not hypothetical. That
name would have gone straight into the content-generation prompt. The result
would not have been a wrong label; it would have been a full lesson sequence
about the wrong topic, confidently labeled "GRADE 11." This is fixed in the
attached patch by nesting every subject/substrand lookup by grade first.

---

## 1. Verified starting state (as of 2026-09-18, off-server)

| Item | State |
|---|---|
| `build_docs.js` 3-line `GRADE 10` hardcode | Root cause confirmed against live `main`. Fix drafted and smoke-tested off-server. **Not yet applied to jhm-spark** — apply via `build_docs_grade_fix.patch`, §3. |
| `generate_substrand.py` Grade-10 assumptions | Traced through: `SYSTEM_PROMPT`, five per-call prompt strings, one `gradeLevel` JSON-template literal, `META` construction (both the batch-submit and sync code paths), `SUBSTRAND_NAMES` / `LESSON_COUNTS` / `CURRICULUM_PDF_MAP` / `CURRICULUM_TEXT_MAP`, and `_v2_output_dir()`. Fix drafted, `ast.parse`-checked, and functionally smoke-tested off-server (see §5 for what was tested). **Not yet applied to jhm-spark** — apply via `generate_substrand_grade_aware.patch`, §5. |
| No `--grade` CLI argument existed | Confirmed — the argparse block had no such flag at all before this patch. |
| Grade 11 curriculum sources | **Already present** in the repo at `CBE_Curriculums/Grade 11/STEM/` for all six STEM subjects: Biology, Chemistry, Physics, General Science, Core Mathematics, Essential Mathematics. Confirmed today by direct inspection (title pages + a mid-document content sample for Biology). All six are single giant-page screenshot PDFs (`pdffonts` shows zero embedded fonts — no text layer), all watermarked "DRAFT." None have been OCR-extracted into `data/raw/curriculum_text/` yet. |
| Biology Grade 11 PDF specifically | Mark separately uploaded a copy to the chat that produced this handoff. Confirmed identical file size (7,119,891 bytes) to the copy already in `CBE_Curriculums/Grade 11/STEM/Biology Grade 11 - October 2025.pdf` — different MD5 (almost certainly just a different export timestamp embedded in the PDF metadata), same content. **Nothing new needs to be brought over for Biology.** |
| Output directory structure | Still flat (`v2/<Subject>/...`, no grade segment) for all existing Grade 10 output on disk. The patch makes newly-generated output grade-segmented (`v2/Grade{N}/<Subject>/...`); migrating the *existing* Grade 10 output to match is a separate, **not yet executed** step — §6. |
| Lesson3's vendored copy of `build_docs.js` | Confirmed with Mark: it's a straight, unmaintained copy. The partner replicates whatever fix lands in this repo themselves. No coordination action needed here beyond fixing this repo and telling Mark once it's done. |
| GitHub connector for direct chat-based write access | Checked — not available in this Anthropic workspace's connector directory (searched multiple keyword variants, none returned). This is why this work is being handed to Claude Code on jhm-spark instead. |
| `LESSON_COUNTS` | Defined, but **not read anywhere else in the current code** (confirmed via grep across the whole file) — only `biology` has entries; every other subject's lesson count comes from `--lessons N` directly. Nested by grade in this patch for future-proofing, not because it's live-wired to anything today. **Re-verify this is still true on jhm-spark** before assuming it's inert — code can drift between sessions. |

---

## 2. Decisions locked (from conversation with Mark, 2026-09-18)

1. **Grade is a required, explicit parameter everywhere — no silent default**, not even to 10. Mark's plan is 10 → 11 → 12 → then backfilling lower grades; a convenient default is exactly the failure mode being fixed here, and it would just recreate the same bug at whichever grade gets defaulted-to next.
2. **Grade 11 reuses Grade 10's strand/sub-strand numbering scheme**, subject by subject. Confirmed by Mark directly, and independently verified against the source PDFs: Biology `2.1` is "Plant Nutrition" at Grade 10 but "Reproduction in Plants" at Grade 11; Core Mathematics gains an entirely new **Strand 4.0 (Calculus)** at Grade 11 with no Grade 10 equivalent at all. Do not assume names *or* strand/sub-strand counts carry over just because the numbering scheme does.
3. **Output directory: same naming convention, repeated per grade** (Mark's words) — applied consistently, including retroactively to the existing Grade 10 output tree, not special-cased as a legacy exception.
4. **Lesson3's vendored copy is not this repo's responsibility** — fix here, they replicate on their end.
5. **The "DRAFT" watermark is permanent** per KICD's own process (a grade stays labeled DRAFT until the *next* grade level's curriculum is also complete) — it is not a signal to wait for a "final" version that will never arrive. The real quality gate is source extractability (native text vs. screenshot), not the label.
6. **Execution moves to Claude Code on jhm-spark** for this work, since no GitHub connector exists for direct chat-based write access.

---

## 3. The `build_docs.js` fix — ready to apply

See `build_docs_grade_fix.patch` (also: full corrected file `build_docs.js` provided
as a fallback if the patch doesn't apply cleanly). Summary of the change:

```diff
 async function buildFinalExplanation(META, FE) {
+  if (META.grade == null) {
+    throw new Error('buildFinalExplanation: META.grade is required but missing');
+  }
   ...
-      `FINAL EXPLANATION: ${META.subject.toUpperCase()} GRADE 10`,
+      `FINAL EXPLANATION: ${META.subject.toUpperCase()} GRADE ${META.grade}`,

 async function buildSummaryTable(META, ST) {
+  if (META.grade == null) {
+    throw new Error('buildSummaryTable: META.grade is required but missing');
+  }
   ...
-      `SUMMARY TABLE: ${META.subject.toUpperCase()} GRADE 10`,
+      `SUMMARY TABLE: ${META.subject.toUpperCase()} GRADE ${META.grade}`,
   ...
-    fullHeader(`SUMMARY TABLE: ${META.subject.toUpperCase()} GRADE 10`, ...)
+    fullHeader(`SUMMARY TABLE: ${META.subject.toUpperCase()} GRADE ${META.grade}`, ...)
```

Deliberately **no silent fallback** (e.g. `META.grade || 10`) — a missing grade
throws immediately instead of quietly printing a plausible-but-wrong grade on a
real assessment document. Smoke-tested off-server: throws on a `META` missing
`grade`; builds correctly for both `grade: 10` and `grade: 11`.

`buildSoW()` (the main Lesson Sequence document) needed no change — it already
used `META.titleDoc`, which is now correctly grade-aware via the
`generate_substrand.py` fix in §5.

---

## 4. Scope split — confirmed with Mark: this handoff needs no curriculum content

Everything in §3 and §5 is pure plumbing — argument parsing, prompt string
construction, dictionary structure, output-path construction. None of it
required the actual Grade 11 KICD content to be finalized, extracted, or even
present. What **does** require content, and is deliberately left to §7 Phase 4
rather than bundled into this patch:

- Populating real Grade 11 entries in `SUBSTRAND_NAMES[11][...]`
- Populating `CURRICULUM_TEXT_MAP[11][...]` (requires OCR extraction first —
  none of the six Grade 11 STEM PDFs have a text layer)
- Optionally, `LESSON_COUNTS[11][...]` (may not matter — see §1's note that
  this dict isn't currently read)

This split is intentional: it lets the structural fix land and get verified
independently of the curriculum-extraction work, which is a different kind of
task with different risks (OCR quality, hand-verification against rendered
pages, fuzzy-dedup tuning) — see `HANDOFF_new_stem_subjects_2026-07-28.md` §6
for the established method, which this same repo already used successfully for
General Science / Core Mathematics / Essential Mathematics at Grade 10.

---

## 5. Exact changes to `src/generate_substrand.py` — ready to apply

See `generate_substrand_grade_aware.patch` (355 lines changed; also provided as
a full corrected file, `generate_substrand.py`, as a fallback). Touch points:

| # | Location | Change |
|---|---|---|
| 1 | `argparse` block | Added `--grade` (`type=int`, no default), added to the required-args check alongside `--subject`/`--substrand`/`--output` |
| 2 | `SYSTEM_PROMPT` (was a module-level string) | Converted to `build_system_prompt(grade)`; module keeps a Grade-10 default at import time, but `main()` immediately overwrites it via `global SYSTEM_PROMPT` once `args.grade` is validated, before any API call |
| 3 | `SUBSTRAND_NAMES` | Nested by grade first (`{10: {...}, 11: {}}`) — **the core fix**, see §0 |
| 4 | `LESSON_COUNTS` | Nested by grade first, same structure, for the same reason (future-proofing — see §1 caveat) |
| 5 | `CURRICULUM_PDF_MAP` | Nested by grade first (native-text PDFs only — none of the Grade 11 sources qualify yet) |
| 6 | `CURRICULUM_TEXT_MAP` | Nested by grade first (OCR-extracted text — where Grade 11 STEM subjects will land once extracted) |
| 7 | Substrand-name resolution in `main()` | Now looks up `SUBSTRAND_NAMES[args.grade][args.subject][args.substrand]`; prints a visible `WARNING` (not a silent fallback) if the grade/subject/substrand combination isn't registered yet |
| 8 | Curriculum-source resolution in `main()` | Now checks `CURRICULUM_TEXT_MAP.get(args.grade, {})` / `CURRICULUM_PDF_MAP.get(args.grade, {})` before falling through to subject |
| 9 | `determine_lesson_count()` | Added a `grade` parameter, threaded from its one call site; its internal API pre-pass prompt now says `Grade {grade}` instead of a literal `Grade 10` |
| 10 | Five `f"Subject: {...} Grade 10\n"` prompt fragments (UNIT, lesson, and FE generation prompts, both sync and batch paths) | All five now read `Grade {args.grade}` |
| 11 | `"gradeLevel": "10"` literal in the UNIT-generation JSON-template prompt | Now `"gradeLevel": "{args.grade}"` |
| 12 | `_v2_output_dir()` | Added a `grade` parameter; now returns `v2/Grade{grade}/<Subject>/<SubStrand>` instead of `v2/<Subject>/<SubStrand>` |
| 13 | `META` construction, batch-submit path | `"grade": 10` → `"grade": args.grade`; `outputDir` call updated to pass `args.grade`; `titleDoc` f-string uses `{args.grade}` |
| 14 | `META` construction, sync path | Same three fixes as #13, in the second copy of this logic |
| 15 | One `print()` diagnostic line | Cosmetic — now reports the real grade instead of a hardcoded 10 |

**What was actually tested, off-server** (not just written — run):
- `python3 -c "import ast; ast.parse(open('src/generate_substrand.py').read())"` — passes
- Running the script with `--subject biology --substrand 2.1 --output test_out` and no `--grade` → argparse correctly rejects it (`error: the following arguments are required: --grade`)
- `build_system_prompt(10)` vs `build_system_prompt(11)` produce distinct, correct text
- `_v2_output_dir(10, 'biology', '2.1', 'Plant Nutrition')` → `v2/Grade10/Biology/SS2.1_Plant_Nutrition`; `_v2_output_dir(11, 'biology', '2.1', 'Reproduction in Plants')` → `v2/Grade11/Biology/SS2.1_Reproduction_in_Plants` — distinct paths, both correctly formed
- `SUBSTRAND_NAMES[10]['biology']['2.1']` → `'Plant Nutrition'`; `SUBSTRAND_NAMES[11]['biology'].get('2.1')` → `None` (correctly does **not** leak Grade 10's name)
- `LESSON_COUNTS` / `CURRICULUM_PDF_MAP` / `CURRICULUM_TEXT_MAP` all confirmed nested correctly with Grade 10's original data intact under the `10` key
- `determine_lesson_count` confirmed to accept a `grade` parameter

**What was not tested** (needs a real API key, appropriately so — not something
to run off-server): an actual end-to-end generation call. That's what Phase 2's
pilot run in §7 is for.

---

## 6. Output directory restructuring — not yet done, needs explicit action

The code now emits `v2/Grade{N}/...` for anything generated from this point
forward. The existing Grade 10 output on jhm-spark's disk is still at the old
`v2/<Subject>/...` path. To make the two consistent (per decision 3 in §2):

1. `git mv` every existing `data/outputs/v2/<Subject>/` directory to
   `data/outputs/v2/Grade10/<Subject>/`. Do this as **one commit**, separate
   from the pipeline-wiring commit, so it's independently revertable if
   something downstream breaks.
2. Update `scripts/sync_to_drive.bat` — its source paths need the `Grade10`
   segment inserted; check whether its Drive-side destination paths should
   also gain a `Grade10` segment or stay flat (Mark's call if this comes up —
   flag it rather than guessing).
3. Update `generators/generate_teacher_index.js` — it walks the `v2/PDF/` tree
   to build the teacher-facing browse page; confirm it still finds everything
   correctly with the new segment, and that the generated `index.html`
   sensibly reflects grade as a browsing dimension rather than just flattening
   past it.
4. **Lower risk than it might look:** `install.sh` (the ~100-school
   provisioning package) has not been live-tested on a real server yet per
   `STATUS.md` — there is no already-deployed fleet content to worry about
   breaking. The main thing needing a re-sync after the `git mv` is Google
   Drive.

---

## 7. Phased execution plan

### Phase 0 — Verify (do this before touching anything)
Per this project's own established Step 0 convention: confirm this document's
claims against jhm-spark's *actual current* state before applying anything.
```bash
cd /home/markk/ares/cbe-generation-system
git log --oneline -5
git status
grep -n "GRADE 10" generators/lib/build_docs.js src/generate_substrand.py
ls "CBE_Curriculums/Grade 11/STEM/"
```
If `main` has moved since commit `3ca9f25` (2026-08-02) in a way that conflicts
with the attached patches, **stop and report the mismatch** rather than force
either patch to apply — this project has a documented history of exactly this
kind of drift (`STATUS.md` "Known Issues").

### Phase 1 — Apply the `build_docs.js` fix
Apply `build_docs_grade_fix.patch` (or copy in the full `build_docs.js`
provided). `node -c generators/lib/build_docs.js`. Commit.

### Phase 2 — Apply the `generate_substrand.py` fix
Apply `generate_substrand_grade_aware.patch` (or copy in the full
`generate_substrand.py` provided). `python3 -c "import ast;
ast.parse(open('src/generate_substrand.py').read())"`. Commit.

### Phase 3 — Output directory migration
Per §6. Commit separately from Phase 2.

### Phase 4 — Curriculum extraction (can start immediately — source material already exists)
This does **not** need to wait on Mark bringing anything new — all six Grade 11
STEM curriculum PDFs are already sitting in `CBE_Curriculums/Grade 11/STEM/`.
Reuse the established method from `HANDOFF_new_stem_subjects_2026-07-28.md` §6.2
exactly (tesseract `--psm 4`, 200 dpi, sliced in 1,000-pt windows with 30-pt
overlap, fuzzy dedup via `difflib.SequenceMatcher` at a 0.92 threshold
restricted to blocks of 400+ characters — remember the pixel/point conversion
gotcha documented there: `pdftoppm`'s `-x -y -W -H` are in pixels at the render
resolution, not PDF points). Start with Biology alone as the pilot subject.

**Critical, per that same precedent doc's §6.5:** hand-verify strand/sub-strand
names and numbering by reading rendered page images directly — do not trust
OCR text as authoritative for names or counts. Already confirmed by direct
visual inspection in this session, for reference: Biology Strand 1.0 = "Cell
Biology and Biodiversity," Strand 2.0 = "Anatomy and Physiology of Plants"
(sub-strand 2.1 = "Reproduction in Plants"), Strand 3.0 = "Anatomy and
Physiology of Animals." This is a spot-check, not a complete inventory —
verify the rest the same way before entering anything into `SUBSTRAND_NAMES`.

Once verified, populate `SUBSTRAND_NAMES[11]['biology']` and
`CURRICULUM_TEXT_MAP[11]['biology']`, then run **one** pilot sub-strand
generation at Grade 11 end to end (`--grade 11 --subject biology --substrand
2.1 ...`). Inspect the actual output: does the Final Explanation genuinely say
"GRADE 11" now, and is the content actually about Reproduction in Plants (not
a repeat of Grade 10's Plant Nutrition unit)?

**Known defect to watch for:** Essential Mathematics Grade 11's source PDF
shows the same repeated-boilerplate pattern already documented as a defect in
Grade 10 Core Mathematics (`HANDOFF_new_stem_subjects_2026-07-28.md` §6.3) —
confirm and apply the same fuzzy-dedup handling if/when that subject is
extracted.

### Phase 5 — Stop and report before any bulk Grade 11 run
Unlike the STEM-subjects precedent's "no manual gate" (that work only added
new, isolated subjects), this change touches plumbing shared by every existing
Grade 10 subject too. Report back to Mark after Phase 4's single pilot,
before generating additional Grade 11 sub-strands or subjects in bulk. This
matches the Level 3 rigor `CLAUDE.md` itself calls for — a partner runs an
independent contract checker against this output, and mistakes here are
expensive to unwind after the fact.

### Phase 6 — Close out
Update `STATUS.md`'s Active Threads table and append a session-log entry per
the `/update` protocol. Commit and push everything.

---

## 8. Open / deferred

| Item | Status |
|---|---|
| Full strand/sub-strand inventory (names, KICD-suggested lesson counts) for Chemistry, Physics, General Science, Core Mathematics, Essential Mathematics at Grade 11 | Only title/TOC pages spot-checked so far for these five; only Biology has had a mid-document content sample reviewed. Needs the same hand-verification pass as Biology before any of them are populated into `SUBSTRAND_NAMES`. |
| Essential Mathematics Grade 11 boilerplate-duplication defect | Observed, not yet confirmed at the same depth as the Grade 10 Core Math precedent — treat as likely, verify before extraction. |
| `generators/generate.js` grade-visibility logging | Not implemented in this patch — a one-line console print of which grade each `*_data.js` is being built for would make future drift easier to spot visually during a run. Worth adding, not urgent. |
| Non-STEM Grade 11 sources (English, History and Citizenship) | Not found — `CBE_Curriculums/Grade 11/` only has a `STEM/` subfolder, no `General/` counterpart to Grade 10's. Out of scope for this handoff. |
| `sync_to_drive.bat` Drive-side destination structure | Needs Mark's input on whether Drive should mirror the new `Grade{N}` segment or stay flat — don't guess, ask. |
| Whether `LESSON_COUNTS` is genuinely dead code or read somewhere outside `generate_substrand.py` (e.g. a status-reporting script) | Confirmed unread within this file; not exhaustively checked against every script in the repo. |

---

## 9. First actions checklist

- [ ] Read this document in full before doing anything else
- [ ] Phase 0: verify state matches this document; report any mismatch before continuing
- [ ] Phase 1: apply `build_docs.js` fix, `node -c`, commit
- [ ] Phase 2: apply `generate_substrand.py` fix, `ast.parse`, commit
- [ ] Phase 3: output-directory migration, commit separately
- [ ] Phase 4: OCR-extract + hand-verify Grade 11 Biology, run one pilot, inspect real output
- [ ] Phase 5: stop and report to Mark before any bulk Grade 11 run
- [ ] Phase 6: update `STATUS.md`, commit, push

---

## 10. Initiation instructions for Claude Code on jhm-spark

**Step A — Mark does this first, outside Claude Code:**

1. Copy this file (`HANDOFF_grade_aware_pipeline_2026-09-18.md`) to the repo root.
2. Copy `build_docs_grade_fix.patch` and `generate_substrand_grade_aware.patch`
   to the repo root (full corrected files `build_docs.js` and
   `generate_substrand.py` are also provided as a fallback if either patch
   doesn't apply cleanly against jhm-spark's current state).

**Step B — paste this into a new Claude Code session on jhm-spark:**

```
Read HANDOFF_grade_aware_pipeline_2026-09-18.md at the repo root in full
before doing anything else.

Execute in order, stopping and reporting back if Phase 0 finds a mismatch,
or after Phase 4's single pilot (§7 Phase 5) — not before, and not for
routine progress updates in between:

1. Phase 0: run the verification commands in the handoff's §7. If main has
   moved in a way that conflicts with the attached patches, stop and report
   the mismatch rather than forcing either patch to apply.
2. Phase 1: apply build_docs_grade_fix.patch (or copy in build_docs.js).
   node -c generators/lib/build_docs.js. Commit.
3. Phase 2: apply generate_substrand_grade_aware.patch (or copy in
   generate_substrand.py). Syntax-check with ast.parse. Commit.
4. Phase 3: migrate existing Grade 10 output per handoff §6 (git mv into
   v2/Grade10/..., update sync_to_drive.bat and generate_teacher_index.js).
   Commit separately from Phase 2.
5. Phase 4: OCR-extract Grade 11 Biology from
   CBE_Curriculums/Grade 11/STEM/Biology Grade 11 - October 2025.pdf using
   the method in HANDOFF_new_stem_subjects_2026-07-28.md §6.2. Hand-verify
   strand/sub-strand names against rendered page images (not OCR text) —
   the handoff's §7 Phase 4 has a partial spot-check to start from. Populate
   SUBSTRAND_NAMES[11]['biology'] and CURRICULUM_TEXT_MAP[11]['biology'].
   Run one pilot: --grade 11 --subject biology --substrand 2.1. Inspect the
   actual generated Final Explanation and Summary Table documents — confirm
   they say GRADE 11 and are actually about Reproduction in Plants.
6. Stop here and report back to Mark with the pilot output before doing
   anything further with Grade 11 — do not generate additional sub-strands
   or subjects, and do not touch the other five Grade 11 STEM subjects'
   curriculum sources yet.
7. Once given the go-ahead: Phase 6 — update STATUS.md's Active Threads and
   session log per the /update protocol, commit, push.

Confirm account API access before Phase 4's pilot generation call.
```
