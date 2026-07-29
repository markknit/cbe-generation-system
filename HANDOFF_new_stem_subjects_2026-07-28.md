# HANDOFF — New Grade 10 STEM Subjects (General Science, Core Mathematics, Essential Mathematics)

**Revision:** 2 (2026-07-28, same day as Revision 1 — see changelog below)
**Supersedes:** `HANDOFF_new_stem_subjects_2026-07-08.md` (never committed, lost) and
Revision 1 of this document (extraction was still pending; Phase 2 had a manual review gate)
**Execution target:** Claude Code on `jhm-spark`, `/home/markk/ares/cbe-generation-system`
**Prepared for:** Mark (markk@areseducation.org)

### Changelog since Revision 1
- Extraction and deduplication of all three curriculum sources is **done** — see §6.
  Phase 0 is now a verification step, not an extraction step.
- The Phase 2→3 manual review gate ("stop here and show Mark the pilots") is **removed**
  per Mark's direction. Replaced with an automated pass/fail quality gate (§8, §12) that lets
  execution proceed straight into full batch generation without waiting for a check-in.
- New §12: exact initiation instructions for Claude Code on jhm-spark.

---

## 0. Why this document exists

A prior session (2026-07-08) produced a handoff for this same work. It was written to a
throwaway sandbox and never reached the server or the repo. A status verification run on
2026-07-28 confirmed **none of Phase 0–2 was ever executed**. This document (now at Revision 2)
replaces it and **must be committed to `main`** — that failure mode is exactly why Revision 1
opened with a commit instruction, and it still applies.

```bash
cd /home/markk/ares/cbe-generation-system
# place this file at repo root, overwriting the Revision 1 copy if present, then:
git add HANDOFF_new_stem_subjects_2026-07-28.md
git commit -m "Handoff rev 2: extraction complete, direct-to-generation plan"
git push origin main
```

---

## 1. Verified starting state (as of 2026-07-28)

| Item | State |
|---|---|
| Phase 0 — extraction and dedup | ✅ **Done** (this session, off-server — see §6). Not yet committed to jhm-spark. |
| Phase 0 — sub-strand numbering pinned | ✅ Done — see §3 |
| Phase 1 — pipeline wiring | ❌ Not started |
| Phase 2/3 — pilot + full generation | ❌ Not started |
| Source PDFs in `CBE_Curriculums/Grade 10/STEM/` | ✅ Present (Core Mathematics copy is superseded — see §6.1) |
| Replacement Core Mathematics PDF | Supplied by Mark 2026-07-28; commit alongside the originals |
| `STATUS.md` on `main` | Still does not mention these subjects — add an Active Threads row |

---

## 2. Decisions locked

1. **All three subjects in scope:** General Science, Core Mathematics, Essential Mathematics
   (Grade 10, KICD July 2025).
2. **Uniform 8 lessons per sub-strand**, all three subjects. 43 sub-strands × 8 = **344 lessons**,
   ≈ **$15** in batch mode.
3. **No teacher templates for any of these.** Claude authors phenomenon, storyline and lesson
   breakdown itself — established precedent from Bio 1.2/2.2/2.3/3.1/3.2/3.3.
4. **General Science gets fully independent content** — not reused/adapted from Biology/
   Chemistry/Physics. See §9 for why name-matching between General Science and existing
   sub-strands is unreliable.
5. **Core Mathematics: generate all 14 sub-strands**, including 2.2/2.3/2.4, which duplicate
   the topics of the existing legacy `math_2_2`/`math_2_3`/`math_2_4`. Saved to a separate
   output path (§5) specifically so teachers can compare the two generations side by side.
6. **The legacy `math_*` corpus is untouched**, pending teacher consultation on how the March
   2025 and July 2025 Math documents relate.
7. **NEW — proceed straight to full generation.** No manual pause between the pilot sub-strands
   and the full 43-sub-strand batch. An automated quality gate (§8 Phase 2, §12) replaces the
   human check-in. Rationale: Mark wants to review actual generated output with teachers, not
   review 3 pilots before generating the rest.

---

## 3. Verified sub-strand inventories

Read directly from the KICD source documents, cross-checked against Appendix 1 where available.
Use these; do not re-derive from OCR without diffing against this table.

### 3.1 General Science — 16 sub-strands

| Strand | Sub-strands |
|---|---|
| 1.0 Life Science | 1.1 Introduction to General Science · 1.2 The Cell · 1.3 Nutrition in Animals · 1.4 Transport in Plants · 1.5 Respiration · 1.6 Plant Growth and Development · 1.7 Microorganisms |
| 2.0 Matter and Chemical Reactions | 2.1 The Periodic Table · 2.2 Chemical Families · 2.3 Chemical Bonding · 2.4 Acids, Bases and Salts · 2.5 Rates of Reactions |
| 3.0 Natural Physical Science | 3.1 Turning Effect of Force · 3.2 Linear Motion · 3.3 Waves · 3.4 Magnetism and Electromagnetic Induction |

### 3.2 Core Mathematics — 14 sub-strands

| Strand | Sub-strands |
|---|---|
| 1.0 Numbers and Algebra | 1.1 Real Numbers · 1.2 Indices and Logarithms · 1.3 Quadratic Expressions and Equations |
| 2.0 Measurements and Geometry | 2.1 Similarity and Enlargement · 2.2 Reflection and Congruence · 2.3 Rotation · 2.4 Trigonometry 1 · 2.5 Area of Polygons · 2.6 Area of a Part of a Circle · 2.7 Surface Area and Volume of Solids · 2.8 Vectors · 2.9 Linear Motion |
| 3.0 Statistics and Probability | 3.1 Statistics I (KICD notes 16 lessons) · 3.2 Probability I (KICD notes 12 lessons) |

> KICD's own lesson notes for 3.1/3.2 are for reference only — we use **uniform 8** per decision 2.

### 3.3 Essential Mathematics — 13 sub-strands

| Strand | Sub-strands |
|---|---|
| 1.0 Numbers and Algebra | 1.1 Real Numbers · 1.2 Indices · 1.3 Quadratic Equations |
| 2.0 Measurements and Geometry | 2.1 Similarity and Enlargement · 2.2 Reflection · 2.3 Trigonometry · 2.4 Area of Polygons · 2.5 Area of Part of a Circle · 2.6 Surface Area of Solids · 2.7 Volume and Capacity · 2.8 Commercial Arithmetic 1 |
| 3.0 Statistics and Probability | 3.1 Statistics 1 · 3.2 Probability I |

**Total: 43 sub-strands.**

---

## 4. Critical finding — sub-strand numbers collide across Maths subjects

| ID | Legacy `math_*` (March 2025) | Core Mathematics (July 2025) | Essential Mathematics (July 2025) |
|---|---|---|---|
| 2.2 | Reflection and Congruence | Reflection and Congruence | **Reflection** |
| 2.3 | Rotation | Rotation | **Trigonometry** |
| 2.4 | Trigonometry 1 | Trigonometry 1 | **Area of Polygons** |

**Legacy `math_*` matches Core Mathematics exactly** on all three — evidence the March 2025
document is the Core Mathematics precursor, but evidence only. The teacher consultation still
decides. Sub-strand IDs must never be displayed or matched without the subject name attached —
document titles and JSON `substrand` fields must carry the subject qualifier.

---

## 5. Naming, slugs and output paths

The `math_` prefix is fully occupied (`math_1_1` … `math_4_2`, 14 files).

| Subject | CLI slug | Data file pattern | `_SUBJECT_FOLDER` value |
|---|---|---|---|
| General Science | `general_science` | `gensci_1_1_data.js` | `General_Science` |
| Core Mathematics | `core_mathematics` | `coremath_2_2_data.js` | `Core_Mathematics` |
| Essential Mathematics | `essential_mathematics` | `essmath_1_1_data.js` | `Essential_Mathematics` |

```
v2/General_Science/SS1.3_Nutrition_in_Animals/
v2/Core_Mathematics/SS2.2_Reflection_and_Congruence/
v2/Essential_Mathematics/SS1.1_Real_Numbers/
```

Core Mathematics 2.2 stays physically separate from legacy `math_2_2` — this is what makes the
teacher comparison in decision 5 possible.

---

## 6. Source documents and extraction — DONE

Extraction and cleanup for all three subjects are complete as of this session. The output is a
`curriculum_text/` folder (README + 3 deduped `.txt` + 3 `.raw.txt` audit copies, 468 KB total)
that needs to be **placed at `data/raw/curriculum_text/` in the repo and committed** — it does
not exist on jhm-spark yet.

### 6.1 Source documents

| Subject | File used | Geometry |
|---|---|---|
| General Science | `CBE_Curriculums/Grade 10/STEM/General Science Grade 10 - July 2025.pdf` | 1 page, 595×19,628 pt, image-only |
| Essential Mathematics | `CBE_Curriculums/Grade 10/STEM/Essential Mathematics Grade 10 - July 2025.pdf` | 1 page, 595×17,938 pt, image-only |
| Core Mathematics | **`KICD_Grade_10_Core_Mathematics.pdf`** (replacement, supplied by Mark 2026-07-28) | 28 pages, letter, one JPEG/page @ 242 ppi |

The original Core Mathematics copy in `CBE_Curriculums/` (21,691 pt single page) is superseded —
the replacement is what was actually OCR'd. **Get the replacement onto jhm-spark and commit it
alongside the original**, so the provenance is traceable.

### 6.2 Method

- General Science / Essential Mathematics: sliced at 200 dpi in 1,000-pt windows (30-pt overlap),
  OCR'd with `tesseract --psm 4`.
- Core Mathematics: embedded page images extracted losslessly with `pdfimages -j`, OCR'd the same way.
- ⚠ **`pdftoppm`'s `-x -y -W -H` are in pixels at the render resolution, not PDF points.**
  Convert with `y_px = y_points * dpi / 72`. Getting this wrong silently renders the wrong region
  and looks like missing content — this cost real time in this session.

### 6.3 Core Mathematics has a source-level duplication defect

**Confirmed as a defect in the KICD document itself**, present in both the repo copy and the
replacement upload — not an extraction artifact. Large boilerplate blocks (e.g. "THE SENIOR
SCHOOL IN THE COMPETENCY BASED CURRICULUM") repeated verbatim ~20 times before OCR.

### 6.4 Deduplication — fuzzy, and one bug worth knowing about

Exact-match dedup does not work: OCR renders each repeat with slightly different character
errors, so identical source blocks never produce identical strings. Fuzzy comparison
(`difflib.SequenceMatcher`, 0.92 threshold) is required.

**A first pass was too aggressive and deleted real content** — an Appendix 1 row ("Area of a
Part of a Circle") was removed because appendix rows differ from their siblings only in the
topic name, and fuzzy matching treated that as a duplicate. This was caught by diffing marker
counts against the raw (undeduped) text, not by inspection — **always keep and diff against the
`.raw.txt` copies when touching this pipeline.**

Fix: dedup is now restricted to blocks of 400+ characters. Only long boilerplate prose is
eligible; short table rows are always kept regardless of similarity. Cost: some smaller repeated
table fragments survive (harmless redundancy). Benefit: zero content loss, verified by exact
marker-count match against raw text for all 43 sub-strands.

| Subject | Raw lines | Deduped lines | Main boilerplate block |
|---|---:|---:|---|
| General Science | 1,652 | 1,652 | none found (no dedup needed) |
| Core Mathematics | 1,839 | 1,534 | 20 occurrences → 2 |
| Essential Mathematics | 1,496 | 1,496 | none found (no dedup needed) |

### 6.5 Caveats that still apply

1. This is OCR, not clean extraction — table structure is flattened, columns run together.
2. The `DRAFT` watermark drops occasional characters. Verify anything numeric against the
   source PDF before relying on it.
3. **These text files are not the authority on sub-strand inventories** — §3 was read by hand
   from rendered page images and is the reference. If OCR text and §3 disagree, §3 wins.

### 6.6 `extract_curriculum_pdf()` will not work on these — branch required

It's pdfminer-based and silently fails on all three sources (no text layer). Add a
`CURRICULUM_TEXT_MAP` and a branch that reads pre-extracted text when a subject has one:

```python
CURRICULUM_TEXT_MAP = {
    'general_science':       'data/raw/curriculum_text/general_science.txt',
    'core_mathematics':      'data/raw/curriculum_text/core_mathematics.txt',
    'essential_mathematics': 'data/raw/curriculum_text/essential_mathematics.txt',
}
```

---

## 7. Pipeline wiring (Phase 1)

Exact touch points, verified against current `main`:

| # | File | Change |
|---|---|---|
| 1 | `src/generate_substrand.py:826` `CURRICULUM_PDF_MAP` | No change needed for these three — they use `CURRICULUM_TEXT_MAP` instead (§6.6) |
| 2 | `src/generate_substrand.py` (near line 826) | Add `CURRICULUM_TEXT_MAP` per §6.6, and branch the extraction call to prefer it when present for a subject |
| 3 | `src/generate_substrand.py:1238` `choices=[...]` | Extend to include `general_science`, `core_mathematics`, `essential_mathematics` |
| 4 | `src/generate_substrand.py:844` `_SUBJECT_FOLDER` | Add the three folder names per §5 |
| 5 | `src/generate_substrand.py` `LESSON_COUNTS` | No change — only `biology` has entries; uniform 8 comes from `--lessons 8` |
| 6 | `src/generate_substrand.py` `find_v2_templates()` | Confirm graceful degradation with no template (verify, don't assume, even though Bio precedent suggests it works) |
| 7 | `scripts/ares/ares_scan_config.yaml` → `subject_keywords:` (line 82) | Add blocks for the three subjects. **Edit only `scripts/ares/ares_scan_config.yaml`** — stale copies exist at `scripts/ares/files3/` and `scripts/ares/Old_files/` |
| 8 | `src/ares_recommender.py` `PHASE_BOOST` | Terms are science-flavoured; fine for General Science, review/extend for both Maths subjects |

`aresResources.js` and `ares_recommender.py` are otherwise subject-agnostic (read
`config.subject`) — no structural changes needed there.

---

## 8. Phased execution plan — direct to generation, no manual gate

### Phase 0 — Verify (extraction already done)
- Place `curriculum_text/` at `data/raw/curriculum_text/`; commit.
- Place the replacement Core Mathematics PDF next to the original; commit.
- Spot-check: confirm the 43 sub-strand names in §3 are each findable in the corresponding
  `.txt` file (they were, as of this session — re-verify after the files land on jhm-spark in
  case anything got mangled in transit).

### Phase 1 — Pipeline wiring
- Apply all changes in §7.
- Patches as Python scripts with exact-match guards (abort if match count ≠ 1), per house style.
- `python3 -c "import ast; ast.parse(open('src/generate_substrand.py').read())"` before running anything.
- Commit.

### Phase 2 — Pilots + automated quality gate (no manual stop)
One pilot per subject, chosen to exercise something distinct:

| Subject | Pilot | Why |
|---|---|---|
| General Science | 1.3 Nutrition in Animals | Tests "broad science, own phenomenon" — no B/C/P equivalent to lean on |
| Core Mathematics | 2.2 Reflection and Congruence | Directly comparable against legacy `math_2_2` |
| Essential Mathematics | 2.8 Commercial Arithmetic 1 | Unique to Essential Maths |

```bash
cd /home/markk/ares/cbe-generation-system
source venv/bin/activate
python3 src/generate_substrand.py --subject general_science       --substrand 1.3 --output gensci_1_3   --lessons 8 --run
python3 src/generate_substrand.py --subject core_mathematics      --substrand 2.2 --output coremath_2_2 --lessons 8 --run
python3 src/generate_substrand.py --subject essential_mathematics --substrand 2.8 --output essmath_2_8  --lessons 8 --run
node generators/generate.js gensci_1_3
node generators/generate.js coremath_2_2
node generators/generate.js essmath_2_8
```

Then run the automated gate (`check_new_subjects_quality.js` — provided alongside this handoff):

```bash
node check_new_subjects_quality.js
```

- **Exit 0 (PASS):** proceed immediately to Phase 3. No approval message needed.
- **Exit 1 (FAIL):** stop. Fix whatever the script flagged (stub lesson, missing FE/ST,
  non-conforming phase label, missing `schemaVersion`), regenerate the affected pilot, re-run
  the gate. Do not submit Phase 3 while this is failing.

This replaces the "stop and show Mark" step from Revision 1. Mark's review now happens on the
full generated output with the teachers, not on the three pilots beforehand.

### Phase 3 — Full batch generation (40 remaining sub-strands)
Runs automatically once Phase 2's gate passes — see §12 for the exact commands.

---

## 9. Context worth carrying forward

**General Science is not a lighter Biology/Chemistry/Physics — it's compressed, not
simplified.** Verified with a direct side-by-side comparison:

- **Name matches are misleading.** Biology 3.1 "Nutrition" covers insect mouthparts and bird
  beaks. General Science 1.3 "Nutrition in Animals" covers the human digestive system, enzyme
  action by region, and food tests. Same name, zero content overlap. Do not assume any General
  Science sub-strand maps to an existing one on the strength of its title.
- **Scope per sub-strand is much wider.** General Science 1.5 Respiration (6 outcomes,
  including respiratory quotient) covers ground Biology splits across 2.3 Gaseous Exchange and
  Respiration in Plants (22 lessons) and 3.3 in Animals (24 lessons) — 46 lessons total.
- **Implication for generation:** the risk is not pitching content too high, it's being too
  granular. Eight lessons must cover a General Science sub-strand's full breadth, so storylines
  need to move faster and cover more ground per lesson than the Biology equivalents do.

---

## 10. Open / deferred

| Item | Status |
|---|---|
| Relationship between March 2025 unified Maths and July 2025 Core/Essential split | **Blocked** on teacher consultation. §4 evidence is suggestive, not decisive. |
| Whether legacy `math_*` should eventually be retired in favour of `coremath_*` | Deferred — depends on the above and on the teacher comparison enabled by decision 5 |
| Biology sub-strand 1.4 addition | Deferred by Mark (pre-existing) |
| Grade 11 STEM curriculum documents (already in `CBE_Curriculums/Grade 11/STEM/`) | Out of scope here |
| `STATUS.md` Active Threads entry for this work | **Must be added** |

---

## 11. First actions checklist

- [ ] Commit this handoff (Revision 2) to `main`, overwriting Revision 1 if present
- [ ] Add an Active Threads row in `STATUS.md`
- [ ] Place `curriculum_text/` at `data/raw/curriculum_text/`; commit
- [ ] Place the replacement Core Mathematics PDF in the repo; commit
- [ ] Place `check_new_subjects_quality.js` at repo root; commit
- [ ] Begin Phase 1

---

## 12. Initiation instructions for Claude Code on jhm-spark

**Step A — Mark does this first, outside Claude Code:**

1. Copy the `curriculum_text/` folder (from this chat's outputs) into
   `/home/markk/ares/cbe-generation-system/data/raw/curriculum_text/`.
2. Copy the replacement `KICD_Grade_10_Core_Mathematics.pdf` into
   `/home/markk/ares/cbe-generation-system/CBE_Curriculums/Grade 10/STEM/` (alongside, not
   replacing, the original).
3. Copy `check_new_subjects_quality.js` into the repo root.
4. Copy this handoff document into the repo root.

**Step B — paste this into a new Claude Code session on jhm-spark:**

```
Read HANDOFF_new_stem_subjects_2026-07-28.md at the repo root in full before doing
anything else. It is Revision 2 and supersedes any earlier version.

Execute in order, without stopping for approval between phases unless something fails:

1. Commit the handoff, the data/raw/curriculum_text/ folder, the replacement Core
   Mathematics PDF, and check_new_subjects_quality.js to main (§0, §11).
2. Add an Active Threads row to STATUS.md for this work - it currently has none.
3. Phase 0: verify the 43 sub-strand names in handoff §3 are each findable in the
   corresponding curriculum_text/*.txt file. Report any mismatch before continuing.
4. Phase 1: wire the three new subjects into the pipeline per handoff §7. Syntax-check
   generate_substrand.py before running anything. Commit.
5. Phase 2: generate the three pilot sub-strands per handoff §8 Phase 2, then run
   node check_new_subjects_quality.js.
   - If it exits 0, continue immediately to step 6. Do not wait for my sign-off.
   - If it exits 1, stop, fix what it flagged, regenerate that pilot, re-run the
     check, and only continue once it passes.
6. Phase 3: submit the remaining 40 sub-strands in batch mode (all of General Science,
   Core Mathematics, and Essential Mathematics except the three already generated as
   pilots), following the WORKFLOW.md batch pattern. Collect with --wait, check for
   stubs with the existing check_data.js pattern extended to these subjects, repair
   any stubs found (WORKFLOW.md "Repairing a Specific Lesson"), then run
   node generators/generate.js --all.
7. Commit and push everything, then update STATUS.md's Active Threads and session log
   per the /update protocol.

Confirm the account's batch API access and Anthropic non-profit pricing status before
starting step 6, given this run is 344 lessons.
```

**What this buys you:** one Claude Code session takes this from "nothing wired" to "344
lessons generated and committed," with the only human-facing pause being an actual failure —
not a scheduled check-in. The teachers get real, full-corpus output to react to, not three
sample sub-strands.
