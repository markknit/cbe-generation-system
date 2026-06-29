# HANDOFF — Grade 10 CBE Full Generation Run

**Audience:** the Claude Code session running this from jhm-spark.
**Date this brief was written:** 2026-06-28.
**Repo state assumed:** `main` at or after commit `dd827ba` (Section C 5-column + integer-number fix).

Read this file in full before doing anything. Sections labelled **DECIDE** mean the user has already decided — don't relitigate. Sections labelled **JUDGE** mean it's left to your judgement during the run.

---

## What you're doing

Generating full Grade 10 CBE lesson plan content for **42 sub-strands** across **Biology / Chemistry / Physics / Maths**. Each sub-strand produces three documents: **Lesson Sequence**, **Final Explanation**, **Summary Table**.

The user has been iterating this project for months. This is the production run.

---

## DECIDE: the user's locked decisions

1. **Templates win.** For each sub-strand, the v2 owner-inventory has a folder. If a template exists for one of the three documents (lesson, FE, ST), use it as input. If missing, generate from scratch with the same general conditions.
2. **Audience matters in prompts.** Final Explanation is for **students**; Summary Table is for **teachers**. Make sure the generator prompts say this explicitly.
3. **Dynamic lesson count.** The old 6-lesson constraint is dropped. The unit generator should propose the number from curriculum + template + topic complexity. Band: **6–14 lessons**, target average ~**8–10**. Templates that declare a lesson count win.
4. **Batch mode.** Cost matters less than power-loss safety. The existing batch infrastructure in `src/generate_substrand.py` is the right path.
5. **Four batches: one per subject.** Smoke test first: one sub-strand per subject (4 total), review, then submit the remaining 38.
6. **Progress tracking: HTML dashboard on jhm-spark.** A static page that reads a `progress.json` the orchestrator updates. Auto-refresh, color-coded, per-sub-strand status.
7. **Templates ARE committed to the repo** under `data/raw/CBE LESSON TEMPLATES/v2_owner_inventory/` (this commit). Use this path, NOT the older `data/raw/CBE LESSON TEMPLATES/` files (legacy set, kept for reference).

## DECIDE: what NOT to change

- The Section C 5-column layout (already in main as of `dd827ba`).
- The lesson `number` field being an integer (already fixed).
- The contract schema (`docs/SCHEMA.md`) — the colleague's drift checker reads this.
- The general lesson-plan template structure (POE cycles, DQB, model building, sensemaking strategies, NGSS SEPs, KICD competencies/values).

---

## The templates: what's in this bundle

Under `data/raw/CBE LESSON TEMPLATES/v2_owner_inventory/`, organized as `<Subject>/SSx.y_Topic/`. Total 77 docx, no stubs, every sub-strand has at least a lesson template.

**17 sub-strands have COMPLETE sets** (lesson + FE + ST already exist) — these came from prior generation work (some from this pipeline, some from an external tool called SciSpace several months ago). The user has confirmed all 17 should be used as **input** to the new run and then **replaced** by the new output. Do not preserve them.

**25 sub-strands have LESSON template only** — generate FE and ST from scratch using the same patterns.

**0 sub-strands are missing the lesson template.**

### Numbering reconciliation (IMPORTANT)

The owner's numbering in the v2 inventory differs from STATUS.md's old numbering for several sub-strands. **Adopt the owner's numbering as canonical** — that's what the folder names use. Key differences:

| Subject | Topic | Old STATUS # | Owner # (use this) |
|---|---|---|---|
| Biology | Chemicals of Life | 1.4 | **1.2** |
| Biology | Cell Structure | 1.3 | **1.1** |
| Biology | Cell Biology | (not tracked) | **1.3** |
| Chemistry | Pressure series | varies | use folder numbers |
| Physics | Electrostatics | 3.1 | **3.4** |
| Physics | Temperature/Thermal | (not tracked) | **1.3** |
| Physics | Moments of Equilibrium | (not tracked) | **1.5** |
| Physics | Current Electricity | (not tracked) | **3.2** |
| Maths | Congruence | 2.2 | **1.4** |
| Maths | Rotation | 2.3 | **3.2** |
| Maths | Trigonometry I | 2.4 | **3.1** |
| Maths | Probability | 3.2 | **4.2** |
| Maths | Vectors I, Linear Motion, Statistics I | (not tracked) | **3.3, 3.4, 4.1** |

Update STATUS.md to reflect the v2 numbering as part of run setup. The colleague's contract schema does NOT key on sub-strand number, so this is safe. (But check the contract before pushing.)

### One open question for the user

**Biology Cell Structure (1.1) vs Cell Biology (1.3)** — these are two folders in the v2 inventory with files that have different content but suspiciously similar filenames. The user has flagged this for confirmation but hasn't resolved it yet. If you encounter ambiguity during generation, **ask before guessing** — don't merge them.

---

## JUDGE: what you decide during the run

- **Exact lesson count per sub-strand.** Use the curriculum input + template content + topic complexity to propose. Honor a number the template explicitly declares. Stay in 6–14, target 8–10. Document your reasoning in the run log.
- **Whether to use the existing template's FE/ST when the lesson template is enough.** If FE/ST templates exist, use them as structural and content guidance. They came from various sources of varying quality.
- **How to handle template content that's clearly incomplete or off-topic.** Use judgement. The user has reviewed all templates and accepts them — but if something is obviously broken at generation time, log it and use curriculum as the primary input.
- **Whether to commit intermediate state.** Commit after the smoke test, after each subject batch completes, and at the end. Don't commit the `.batch_id` checkpoint files (already gitignored or should be).

---

## The plan

### Phase 0 — Pre-flight (don't skip)

1. Pull latest `main`; verify `git status` clean.
2. Read this whole file, then read in this order:
   - `docs/STATUS.md` — current state and numbering (will need updating)
   - `docs/SCHEMA.md` — the contract; do not violate
   - `docs/WORKFLOW.md` — the standard workflow
   - `docs/SYSTEM_OVERVIEW.md` — pipeline architecture
   - `src/generate_substrand.py` — the generator you'll be extending (it already has batch mode, checkpointing, resume)
3. Verify templates are in place: `ls "data/raw/CBE LESSON TEMPLATES/v2_owner_inventory/"` should show `Biology/ Chemistry/ Maths/ Physics/`.
4. Verify the API key is set: `echo $ANTHROPIC_API_KEY | head -c 10` should print 10 chars.

### Phase 1 — Pipeline extensions (small, deliberate)

These changes need to land in `src/generate_substrand.py` before any batch goes out. Each is a targeted edit, not a rewrite:

**1a. Three-template lookup.** Currently `--template` resolves a single file. Extend to find up to three files per sub-strand from the v2 inventory: `*LessonSequence*.docx` or unsuffixed bare file → lesson template; `*FinalExplanation*.docx` or `*Final_Explanation*.docx` → FE template; `*SummaryTable*.docx` or `*Summary_Table*.docx` → ST template. Each optional, each fed to its respective generation step.

The lookup directory should be:
```python
template_dir = PROJECT_ROOT / 'data' / 'raw' / 'CBE LESSON TEMPLATES' / 'v2_owner_inventory'
# Then walk to the sub-strand's SSx.y_* folder
```

Glob pattern by sub-strand: match the folder by `SS{ss}_*` (e.g. `SS1.2_*`).

**1b. Audience-specific prompts.** In the existing FE and ST generation prompts, add explicit audience framing at the top:
- FE prompt prefix: "This Final Explanation document is for STUDENTS to use as a model for answering the driving question. Use clear, student-accessible language. Write in second person when appropriate."
- ST prompt prefix: "This Summary Table is a TEACHER REFERENCE — a pre-filled answer key for use while teaching. Write in third-person teacher voice; include pedagogical notes a teacher would find helpful."

**1c. Dynamic lesson count.** The existing `--lessons` is `default=None`. When None, the current code falls back to `LESSON_COUNTS[subject][substrand]` defaulting to 8. **Change this** to do a quick pre-pass: a small Claude call (`max_tokens=512`) that takes curriculum + template excerpt and returns an integer lesson count in 6–14. Cache the result in the checkpoint. Templates that explicitly state a count (often visible in the template header as "X lessons" or "X periods") should override the pre-pass — try regex extraction first, fall back to the pre-pass call.

**1d. (Optional, only if needed)** Refine `build_batch_requests()` to include the three-template inputs in each request.

### Phase 2 — Orchestrator + dashboard

Build these together because the dashboard reads the orchestrator's state file.

**Orchestrator:** `scripts/run_full_generation.py`. Crash-safe state in `scripts/.run_state.json`. Phases: smoke test (4 sub-strands), then 4 subject batches sequentially. Each phase: submit → poll → collect → assemble → verify → mark complete. On crash/restart, re-read state and resume at the next pending phase.

State file shape:
```json
{
  "started_at": "2026-06-28T...",
  "phase": "smoke|biology|chemistry|physics|maths|done",
  "batches": {
    "smoke": {"status": "complete|submitted|collecting|...", "batch_id": "...", "substrands": [...], "submitted_at": "...", "completed_at": "..."},
    "biology": {...},
    ...
  },
  "substrands": {
    "biology/1.1": {"status": "queued|generating|complete|failed", "lesson_count": 8, "cost_estimate_usd": ..., "files": [...], "log": "..."},
    ...
  },
  "totals": {"cost_estimate_usd": ..., "lessons_generated": ...}
}
```

**Dashboard:** `dashboards/progress.html`, served by a simple Python `http.server` on jhm-spark (`python3 -m http.server 8080 --directory dashboards/`). The HTML reads `scripts/.run_state.json` via fetch and renders:
- Per-subject progress bars
- Per-sub-strand status grid (color: gray=queued, blue=generating, green=complete, red=failed, yellow=needs review)
- Running cost estimate
- Last 20 log lines (tail `scripts/run.log`)
- Auto-refresh every 30s

User opens this at `http://jhm-spark:8080/progress.html` (or `localhost:8080` if SSH-forwarding).

### Phase 3 — Smoke test (gate)

Pick one sub-strand per subject. Suggested:
- Biology: 2.2 Plant Transport (template-only, exercises FE+ST generation)
- Chemistry: 2.1 Introduction to Salts (template-only)
- Physics: 1.4 Energy, Work, Power & Machines (template-only)
- Maths: 1.4 Congruence (template-only)

Submit as one batch of 4 sub-strands. After collection:
- Verify all 12 documents (4 × 3 docs) generate without schema errors
- Manually spot-check: open one of each type, confirm audience tone is right, Section C is 5-column, lesson count is reasonable
- **STOP and report to user before proceeding to Phase 4.**

### Phase 4 — Production batches

Four batches, sequential. Each is a single submit/poll/collect cycle:
- Biology batch: 8 remaining sub-strands (1.1, 1.2, 1.3, 2.1, 2.3, 3.1, 3.2, 3.3)
- Chemistry batch: 6 remaining
- Physics batch: 11 remaining
- Maths batch: 13 remaining

After each batch completes: verify, regenerate docx, commit with a message that names the subject, push. Update STATUS.md as you go.

### Phase 5 — Final verification + commit

- Spot-check 1-2 sub-strands per subject for quality
- Verify all 42 × 3 = 126 docx files exist and open cleanly
- Update STATUS.md to final state
- Final commit + push

---

## Power-loss / crash recovery

**Already handled by existing infrastructure** (`_save_checkpoint`, `_load_checkpoint`, batch IDs persisted in `.batch_id.txt` files). What you add:
- Orchestrator state file (`scripts/.run_state.json`) — also crash-safe (write to `.tmp` then atomic rename)
- A `--resume` flag on the orchestrator that reads state and continues
- For an in-progress batch: Anthropic stores batch results for 29 days, so a 12-hour power outage costs nothing

**If you restart and find a batch in 'submitted' state:** call the API to check status; if 'ended', collect immediately. If still processing, continue polling.

**If a single sub-strand fails inside a batch:** Anthropic returns per-request errors. Mark that one as 'failed' in state, continue with the rest, then re-submit the failures as a tiny batch.

---

## What to commit and when

- **Now (this commit, before you start):** templates under `data/raw/CBE LESSON TEMPLATES/v2_owner_inventory/`, this `HANDOFF.md`, the updated STATUS.md numbering.
- **After Phase 1:** pipeline extensions, separately, with tests.
- **After Phase 2:** orchestrator + dashboard.
- **After smoke test passes:** review checkpoint commit.
- **After each subject batch:** subject-named commit (`Biology generation complete (8 sub-strands)`).
- **At end:** final STATUS update.

Push to `main` after each commit. Branch `claude/setup-cbe-generation-ZKiIi` is dead; do not use it (the project moved to `main` weeks ago).

---

## Reporting back to the user

The user is **Mark** (markk@areseducation.org). His partner reviews outputs and runs drift/schema validation on her own Claude.ai project; she **cannot read markdown** — give her `.docx` reports.

After the smoke test, send Mark a status update with:
- Number of lessons generated per smoke-test sub-strand
- Sample output (one each of lesson/FE/ST)
- Any anomalies
- Cost so far
- Estimated total cost for the full run

After the full run completes, give him a final report (`.docx`) suitable for forwarding to the partner.

---

## Things that have bitten this project before

- **Don't trust earlier-session memory or doc claims when the repo says otherwise.** Fetch the code, evaluate it, then act.
- **Patches over manual edits.** Use `git apply` with `--check` first; do not edit-by-hand from instructions.
- **Heredocs truncate.** Write scripts to `/tmp/script.py` then execute separately.
- **Google Doc share-link downloads fail silently when unauthenticated.** Anything sourced from Drive must be verified — `file <name>.docx` should say "Microsoft Word 2007+", not "HTML document".
- **`git apply` from `~` fails if the file isn't in `$HOME`.** Use `./filename.patch` from the repo root when in doubt.

---

## You have everything you need

The repo is at `main`. Templates are committed. The existing pipeline already supports batch mode, checkpointing, and resume — you're extending, not rewriting. The user is patient but tired of half-completed work, so finish cleanly: smoke test → review → batches → final report.

Good luck.
