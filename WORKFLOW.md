# Operational Workflow Guide

## Standard Workflow: Generating a New Subject/Sub-Strand

### Step 1 — Environment setup
```bash
cd /home/markk/ares/cbe-generation-system
source venv/bin/activate
```

### Step 2 — Submit batch (required beyond pilot-scale)

**Rule, not a preference (added 2026-07-30):** `--batch` is the default for
anything past a 1-3 sub-strand pilot/spot-check. `--run` (live/sync mode) is
2x the per-token price of batch mode and is reserved for those small pilot
runs only. A session resuming or extending prior generation work should not
silently continue in `--run` mode for bulk work just because that's how the
interrupted session happened to be running — check which mode is appropriate
for the actual remaining scope before continuing.

```bash
# Single sub-strand
python3 src/generate_substrand.py \
  --subject chemistry \
  --substrand 1.4 \
  --output chem_1_4 \
  --lessons 8 \
  --batch

# Multiple sub-strands — submit all, then collect later
for ss in 1.2 1.3 1.4 1.5 2.1 2.2; do
  python3 src/generate_substrand.py \
    --subject chemistry \
    --substrand $ss \
    --output chem_${ss//./_} \
    --lessons 8 \
    --batch
done
```

Each submission takes ~30 seconds (UNIT generation only). Batch results arrive within 24 hours, typically under 1 hour.

### Step 3 — Collect results
```bash
# Wait for first batch, then collect remainder (likely already done)
python3 src/generate_substrand.py --collect chem_1_2 --wait --run
python3 src/generate_substrand.py --collect chem_1_3 --run
python3 src/generate_substrand.py --collect chem_1_4 --run
# ... etc.
```

### Step 4 — Check for stubs
```bash
# Create the check script (if not in /tmp/)
cat > /tmp/check_data.js << 'EOF'
var names = ['chem_1_2','chem_1_3','chem_1_4','chem_1_5','chem_2_1','chem_2_2'];
names.forEach(function(name) {
  try {
    var d = require('/home/markk/ares/cbe-generation-system/generators/data/' + name + '_data.js');
    var stubs = d.LESSONS.filter(function(l) { return !l.overview || l.overview.length < 50; });
    var hasFE = d.FINAL_EXPLANATION && d.FINAL_EXPLANATION.sections && d.FINAL_EXPLANATION.sections.length > 0;
    var hasST = d.SUMMARY_TABLE && d.SUMMARY_TABLE.lessons && d.SUMMARY_TABLE.lessons.length > 0;
    var stubNums = stubs.map(function(l){ return l.number; }).join(',');
    console.log(name + ': ' + (d.LESSONS.length - stubs.length) + '/' + d.LESSONS.length + ' lessons OK' +
      (stubs.length ? ' | STUBS: ' + stubNums : '') +
      (hasFE ? '' : ' | NO FE') +
      (hasST ? '' : ' | NO ST'));
  } catch(e) { console.log(name + ': ERROR - ' + e.message); }
});
EOF

node /tmp/check_data.js
```

### Step 5 — Repair stubs (if any)

**For stub lessons:**
```bash
# The JSON was saved to /tmp/ during collect
node scripts/patch_lesson.js chem_1_4 3 /tmp/chem_1_4_lesson3.json

# If /tmp/ file was lost, regenerate it via repair_stubs.py
# Edit the REPAIRS dict in scripts/repair_stubs.py first, then:
python3 scripts/repair_stubs.py
```

**For missing Final Explanation:**
```bash
node scripts/patch_fe.js chem_1_4 /tmp/chem_1_4_fe.json
```

**If /tmp/ files are lost and you need to regenerate:**
- Edit `REPAIRS` in `scripts/repair_stubs.py` with the correct stubs
- Run `python3 scripts/repair_stubs.py` — it regenerates and saves to /tmp/
- Then apply with `patch_lesson.js` / `patch_fe.js`

### Step 6 — Regenerate docx
```bash
# Single sub-strand
node generators/generate.js chem_1_4

# All sub-strands at once
node generators/generate.js --all
```

### Step 6b — Generate PDFs (teacher distribution copies)

`.docx` is the working/master format: it's what the partner's contract
checker validates, and it's the editable source of record. Teachers
accessing lesson plans — via the web or as a download — need a
fixed-layout, offline-friendly, annotatable format instead, which is why
this step produces PDFs as a separate distribution artifact rather than
serving `.docx` directly. Full rationale in `docs/PDF_GENERATION.md`.

```bash
node generators/generate_pdfs.js
```

This scans `data/outputs/v2/` for every `_CBE_LessonSequence.docx`,
`_FinalExplanation.docx`, and `_SummaryTable.docx` file, converts each via
headless LibreOffice, and writes the PDFs into a parallel `v2/PDF/` tree
that mirrors the `Subject/SubStrand/` folder structure exactly:

```
data/outputs/v2/Biology/SS2.1_Plant_Nutrition/Biology_Plant_Nutrition_CBE_LessonSequence.docx
data/outputs/v2/PDF/Biology/SS2.1_Plant_Nutrition/Biology_Plant_Nutrition_CBE_LessonSequence.pdf
```

**Behaviour to know before running at scale:**
- Conversions run in batches (150 files per LibreOffice invocation), not
  one process per file — LibreOffice's headless startup cost is real, and
  batching avoids paying it hundreds or thousands of times over.
- A dedicated LibreOffice profile is used (`-env:UserInstallation=...`) so
  this script can never collide with a LibreOffice window opened manually
  on jhm-spark for visual QA of layout.
- **Failures are logged, not fatal.** If a file fails to convert, it's
  added to a `Failed conversions` list printed at the end and the run
  continues — a single bad `.docx` should never block the rest of a
  2,000-lesson batch. Review the failed list and re-run individually.
- Filename collisions across different sub-strand folders (same basename,
  different folder) are converted one-at-a-time as a safety fallback,
  since batch conversion assumes unique basenames within a batch.

**If you hit a syntax error immediately on the first line when creating a
new script by pasting into a heredoc** (`cat > file.js << 'EOF' ...`),
check for stray bytes before assuming the code is wrong:
```bash
head -c 20 <file> | xxd
```
Long pastes over SSH can corrupt or truncate mid-transfer. If this
happens, use the `python3` stdin method instead, which doesn't depend on
the shell recognizing a terminator line:
```bash
python3 -c "import sys; open('/tmp/out.js','w').write(sys.stdin.read())"
# paste the file body, then press Ctrl-D
```
Always verify with `node -c <file>` (syntax-check only, doesn't execute)
before running a freshly-pasted script for real.

### Step 6c — Generate the teacher-facing index page
```bash
node generators/generate_teacher_index.js
```
Scans `data/outputs/v2/PDF/` and writes `data/outputs/v2/PDF/index.html` —
a single self-contained static page (no external fonts/scripts/CDN calls)
listing every subject and sub-strand with links to its PDFs. Safe to
re-run any time; it fully regenerates from whatever is currently on disk,
with no incremental state to get out of sync. Full design rationale in
`docs/PDF_GENERATION.md`. Always run this **after** Step 6b, since it
indexes whatever PDFs already exist — running it first just produces an
empty or stale page.

### Step 7 — Commit and sync
```bash
# jhm-spark
git add -A
git commit -m "Chemistry sub-strands 1.2–2.2 generated (8 lessons each)"
git push origin main

# Windows
git pull
```

### Step 8 — Sync to Google Drive (Windows)

Two separate robocopy jobs mirror `.docx` and PDF outputs to Google Drive
independently, since they serve different audiences: the `.docx` job
targets `G:\My Drive\CBE Outputs` (partner/editable master); the PDF job
targets `G:\My Drive\CBE Outputs\PDF` (teacher-facing distribution copy,
including `index.html` — note the PDF job's file mask must include
`*.html`, not just `*.pdf`, or the index page silently never syncs). Full
`.bat` listing and rationale in `docs/PDF_GENERATION.md`.

**Note (2026-07-04): Drive is confirmed as the current sync destination,
not yet the end of the chain.** How content reaches each school's offline
mesh-network appliance from here — Drive, `git pull` directly, or
something else — is still an open question; see `docs/PDF_GENERATION.md`.

---

## Repairing a Specific Lesson

When `check_data.js` shows a stub:

```bash
# Check what lesson numbers are stubs
node /tmp/check_data.js

# If the JSON file exists in /tmp/:
node scripts/patch_lesson.js <output_name> <lesson_num> /tmp/<output_name>_lesson<num>.json

# Example:
node scripts/patch_lesson.js bio_2_3 3 /tmp/bio_2_3_lesson3.json

# Then regenerate docx:
node generators/generate.js bio_2_3
```

---

## Repairing a Missing Final Explanation

```bash
# If JSON is in /tmp/:
node scripts/patch_fe.js <output_name> /tmp/<output_name>_fe.json
node generators/generate.js <output_name>
```

If the file needs to be regenerated (see `scripts/gen_bio33_fe.py` as a template):
- Keep the prompt short — pre-fill section titles, only ask Claude to fill content
- Use `max_tokens=3000` (not 5000) to avoid truncation
- Use `node scripts/patch_fe.js` to apply — never use Python regex to patch FE

---

## Adding a New Sub-Strand Manually

For cases where the pipeline needs custom handling:

1. Copy the nearest data file as a template:
```bash
cp generators/data/bio_1_4_data.js generators/data/chem_1_4_data.js
```

2. Edit META, UNIT, LESSONS in the new file

3. Run the generator:
```bash
node generators/generate.js chem_1_4
```

---

## Checking Output Quality

After generating, spot-check the docx:
1. Open `*_CBE_LessonSequence.docx` — verify Lesson 1 has non-empty content in all 5 phases
2. Check the Resource column — should contain ARES hyperlinks (not placeholder text)
3. Check the Sub-Strand Overview table — phenomenon, driving question, and storyline should be filled
4. Open `*_FinalExplanation.docx` — should have 4-5 sections with exemplar text
5. Open `*_SummaryTable.docx` — should have one row per lesson with observed/learned/explained

**Red flags:**
- Section C rows with empty Learner Experience cells
- "FILL" placeholder text anywhere
- Lesson titles like "Lesson 3" with no subtitle (indicates stub)
- Sub-strand overview rows that are blank

---

## Git Sync Reference

| Action | Command |
|---|---|
| Push from jhm-spark | `git add -A && git commit -m "..." && git push origin main` |
| Pull to Windows | `git pull` |
| First-time pull after force push | `git fetch origin && git reset --hard origin/main` |
| Check for large files before push | `find . -size +50M -not -path './.git/*' -not -path './venv/*'` |

---

## Model and Cost Reference

| Model | Input | Output | Use case |
|---|---|---|---|
| `claude-sonnet-4-6` (sync) | $3/MTok | $15/MTok | Testing, single lessons |
| `claude-sonnet-4-6` (batch) | $1.50/MTok | $7.50/MTok | **Bulk generation — use this** |
| `claude-opus-4-8` | $5/MTok | $25/MTok | Quality comparison only |

**Typical cost per sub-strand (8 lessons, batch mode):** ~$0.35
**Full 2,000-lesson target (batch mode):** ~$114 for clean, zero-defect generation.

**Repair-pass contingency (added 2026-07-30):** the estimate above assumes
every lesson generates cleanly on the first try. It doesn't. This project's
own Known Issues section documents JSON-truncation stub lessons as a
recurring failure mode, and the 2026-07-30 General Science run hit it at
scale — 34 stub lessons + 1 missing Final Explanation across 344 lessons
(~10%), each repaired via an individual **live** API call (2x batch pricing,
since a 1-2 lesson repair isn't worth batch overhead). Budget a **15-20%
contingency on top of the clean-generation estimate** for any run of
comparable scale, and treat that contingency as expected cost, not overrun —
the "$114 for 2,000 lessons" figure should be quoted alongside "+15-20% likely
repair cost," not alone.

**Track actual spend, don't just estimate it.** `generate_substrand.py` logs
cumulative token usage and estimated cost for every run to
`logs/api_cost_log.md` (see the script's `--collect`/`--run`/`--batch` output
for the per-run summary). Check that log against the estimate above
periodically — if actual spend is consistently running higher than the
15-20% contingency accounts for, the estimate itself needs revising, not
just the contingency margin.

---

## Environment Reference

| Item | Value |
|---|---|
| Server | jhm-spark |
| User | markk |
| Project root | `/home/markk/ares/cbe-generation-system` |
| Python venv | `source venv/bin/activate` |
| Node version | v22.x |
| API model | `claude-sonnet-4-6` |
| Git branch | `main` |
| GitHub remote | `https://github.com/markknit/cbe-generation-system.git` |
| ARES content DB | `data/ares_index/ares_content.db` (630MB, jhm-spark only, gitignored) |
| Curriculum PDFs | `data/raw/curriculum_pdfs/` |
| Teacher templates | `data/raw/CBE LESSON TEMPLATES/` |
| Output documents (docx, master) | `data/outputs/v2/<Subject>/<SubStrand>/` |
| Output documents (PDF, teacher distribution) | `data/outputs/v2/PDF/<Subject>/<SubStrand>/` |
