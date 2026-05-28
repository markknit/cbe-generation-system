# Session Handoff — 2026-05-25
## Kenya CBE Lesson Plan Generation System

> Written for a future Claude session to read and pick up from.
> Companion documents: PROJECT_CONTEXT.md (durable project record), CLAUDE.md (operational instructions).

---

## State at End of This Session

### What Was Accomplished

1. **ARES content index built** — 1.55M items across three sources (web, Kiwix, Kolibri) indexed into a SQLite database at `data/ares_index/ares_content.db`

2. **Whisper transcription completed** — 4,067 videos transcribed (KICD Educhannel 481, Kolibri priority 3,601, ARES Web 425). All transcripts linked into the index DB. Language forced to English (`--language en`) after initial runs produced garbled output from incorrect Swahili detection.

3. **ARES recommendation engine working** — `scripts/ares/query_ares_index.py recommend` produces ranked content recommendations for any lesson topic/phase. Tested and validated for Biology Cell Structure sub-strand.

4. **Ready to integrate** — The recommendation engine is ready to be wired into the lesson plan generator. This is the next task.

---

## ARES Content Index — Key Facts

### Database location
```
/home/markk/ares/cbe-generation-system/data/ares_index/ares_content.db
```

### Content sources (all via symlinks matching original ARES paths)
| Source | Path | Items |
|---|---|---|
| ARES Web | `/mnt/sda3/var/www/modules` | 1,457,051 |
| KICD Educhannel | `/mnt/sda3/var/www/KICD_Educhannel` | 481 videos |
| Kiwix ZIMs | `/mnt/sda3/var/Downloads2/Data/Currentcontent` | 17 ZIM archives |
| Kolibri | `/mnt/sda3/Kolibri_Data-current` | 126,023 content nodes |

### Transcript coverage
- 4,067 transcripts linked (KICD Educhannel + priority Kolibri channels)
- Kolibri transcripts stored alongside MP4 files as `.json` (Whisper output)
- Kolibri transcripts linked via `kolibri_checksum` field (NOT `kolibri_id` — these don't match disk files)

### Critical DB notes
- Kolibri content on disk uses `content_file.checksum` as filename (NOT `content_contentnode.id`)
- The `kolibri_checksum` column was added by `fix_kolibri_checksums.py` — this bridges DB metadata to actual files
- Kolibri storage path: `/mnt/sda3/Kolibri_Data-current/Content/storage/<a>/<b>/<checksum>.mp4`
- Channel databases: `/mnt/sda3/Kolibri_Data-current/Content/databases/*.sqlite3`

---

## ARES Scripts — Location and Purpose

All scripts at `/home/markk/ares/cbe-generation-system/scripts/ares/`:

| Script | Purpose |
|---|---|
| `ares_scan_config.yaml` | All paths and config |
| `scan_ares_content.py` | Multi-source scanner (web/kiwix/kolibri) |
| `patch_kolibri_subjects.py` | Enriches subject tags from Kolibri metadata |
| `fix_kolibri_checksums.py` | Links Kolibri channel DB checksums to disk files |
| `index_transcripts.py` | Links Whisper transcripts into the DB |
| `query_ares_index.py` | **Main query/recommend tool — used by lesson generator** |
| `run_whisper_batch.py` | Batch Whisper transcription |
| `whisper_progress.py` | Progress tracker for Whisper batch |
| `list_modules_for_priority.py` | Lists modules with video counts for priority planning |

---

## Recommendation Engine — How It Works

### Command
```bash
python3 scripts/ares/query_ares_index.py \
    --config scripts/ares/ares_scan_config.yaml \
    recommend \
    --substrand "Cell Structure and Specialisation" \
    --topic "organelles electron microscope" \
    --subject Biology \
    --phase observe \
    --n 5
```

### Algorithm
1. Extracts individual keywords from substrand + topic + phase boost terms
2. Searches each keyword separately via FTS5, accumulates hit counts per content row
3. Ranks by: `(type+transcript) → title hits → total hits → subject match → module tier → FTS score`
4. Deduplicates by title

### Module tiers
- **Tier 0**: KICD Educhannel, Khan Academy EN, MIT Blossoms, PhET, TED-Ed, CK-12, TESSA, Kenya Curriculum Tools
- **Tier 1**: Kiwix/Wikipedia ZIMs
- **Tier 2**: ARES Web general content

### JSON output (for pipeline integration)
```bash
python3 scripts/ares/query_ares_index.py recommend \
    --substrand "..." --topic "..." --subject Biology --phase observe \
    --json
```

---

## Next Task: Wire ARES Recommendations into Lesson Plan Generator

### Goal
For each lesson phase (Predict, Observe, Explain, DQB, Model Building), the Resource column of Section C should contain:

**For projector teachers (video):**
```
📹 VIDEO: Organelles in eukaryotic cells
   Source: Khan Academy (English)
   ARES search: "organelles electron microscope"
```

**For non-projector teachers (reading):**
```
📖 READING: Cell Organelles
   Source: CK-12 Flexbook
   ARES search: "cell organelles CK-12"
```

### Architecture decision pending
The generation system currently has:
- **JS generators** (`generators/biology_1_3_cell_structure.js` etc.) — template-style, hardcoded content for the two existing sequences
- **Python `src/`** — Claude API orchestration layer for bulk generation

The integration goal is quality-first, technology-agnostic. The approach should:
1. Query `query_ares_index.py recommend --json` for each lesson phase
2. Select the best video recommendation AND best non-video recommendation separately
3. Format both into the Resource cell content
4. Pass into whichever generator is used

A Python module `src/ares_recommender.py` should wrap the DB query so the generator doesn't need to call the CLI tool — it queries SQLite directly.

### Key design principle
The resource recommendation must produce TWO items per phase:
1. A video (for projector use)
2. A non-video alternative (PDF/HTML reading for independent student use)

---

## Whisper Batch — Status and Remaining Work

### Completed
- KICD Educhannel: 481 videos ✓ (English forced with `--language en`)
- Khan Academy STEM: 3,434 videos ✓
- PhET: 53 videos ✓
- TED-Ed: 114 videos ✓

### Remaining (lower priority — do after generation starts)
- CK-12: 1,381 videos (not yet transcribed)
- Khan Academy Kiswahili: not needed (teachers teach in English)
- Ubongo Kids, Touchable Earth, Mother Goose Club: low priority

### To resume Whisper
```bash
cd /home/markk/ares/cbe-generation-system
source venv/bin/activate
tmux new -s whisper
python3 scripts/ares/run_whisper_batch.py --priority --model medium --language en
```

---

## Lesson Plan Generation — Current State

### Completed lesson sequences
- `Biology_CellStructure_CBE_LessonSequence_L1-3.docx` — Sub-strand 1.3, Lessons 1-3 of 20
- `Biology_ChemicalsOfLife_CBE_LessonSequence_L1-5.docx` — Sub-strand 1.4, Lessons 1-5 of 24

### Document format standards (do not change)
- Portrait, US Letter, 0.75" margins
- Font: Arial, body ~9pt
- Section C: 6 columns (phase label + 5 content columns)
- Phase colours: Predict=lightPurple, Observe=lightTeal, Explain=lightGreen, DQB=lightOrange, Model=lightBlue
- Generator: JavaScript + `docx` npm library

### Generation pipeline
The next step is to build a scalable pipeline that:
1. Reads KICD curriculum for each sub-strand
2. Calls Claude API to generate lesson content
3. Calls ARES recommender to get resource recommendations
4. Combines into JS generator input
5. Produces formatted `.docx` output
6. Scales to ~2,000 lessons across Biology, Physics, Chemistry, Mathematics

---

## Infrastructure Notes

### ARES USB drive mount on jhm-spark
The ARES drive is attached via USB. It mounts at:
```
/media/markk/bed8a47f-8df3-4582-a312-48a1d6969e7e/
```
The symlinks under `/mnt/sda3/` point into this mount. Always verify mount is active before running scans.

### Python environment
```bash
cd /home/markk/ares/cbe-generation-system
source venv/bin/activate
```
Key packages: anthropic, python-docx, pyyaml, pdfminer.six, libzim, torch, openai-whisper

### GPU (NVIDIA GB10 Blackwell)
- CUDA 12.8, Compute capability 12.1
- PyTorch works with CUDA ✓
- faster-whisper does NOT work (CTranslate2 has no ARM64 CUDA build)
- openai-whisper works with CUDA via PyTorch ✓
- ~20-25× realtime for English speech transcription

---

## Restoration Prompt for New Session

```
I am working on the Kenya CBE Lesson Plan Generation System on jhm-spark,
user markk, path /home/markk/ares/cbe-generation-system.

The ARES content recommendation engine is now working. The immediate next task
is to integrate ARES resource recommendations into the lesson plan generator,
so that Section C Resource column is automatically populated with:
  1. A video recommendation (with ARES search terms) for projector teachers
  2. A non-video reading recommendation for non-projector teachers

Read CLAUDE.md and session-handoff-2026-05-25.md for full context.
```
