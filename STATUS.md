# Generation Status — Kenya CBE Grade 10 Lesson Plans

*Last updated: 2026-07-31*

---

## How this file is used — read this first

This file is the **single source of truth for project continuity** across
sessions, tools, and resets (Claude.ai, Claude Code, or a fresh person
picking this up cold). If you're starting a new session, **read the
Active Threads table below before doing anything else** — do not assume
you know current state from memory, training data, or a prior
conversation's summary.

**When this file gets updated — not optional, not "when convenient":**
- As part of finishing any real unit of work (a fix, a migration, a
  decision) — updating Active Threads and appending a session-log entry
  is part of what "done" means for that task, not a separate step to
  remember afterward.
- On demand, via the `/update` skill (Claude Code: `.claude/skills/update/`)
  or by typing `/update` in a Claude.ai session in this project — forces
  an update right now, e.g. at the end of a day, before a server reset,
  or before switching tools, so nothing is lost between sessions.

**Before trusting this file, re-verify it — don't just read it:** the
`/restart` skill (Claude Code: `.claude/skills/restart/`) or typing
`/restart` in a Claude.ai session re-reads this file plus `CLAUDE.md`
(and, in Claude Code, runs `WORKFLOW.md`'s Step 0 live checks) and
reports any drift before continuing. `/update` is the write side of
continuity; `/restart` is the read/verify side — use it at the start of
a work day or any time something feels stale.

**Why this exists:** this project has had multiple documented incidents
(see "Known Issues / Lessons Learned" below) where a fact was true when
written and silently went stale because nothing forced a re-check.
Continuity information is exactly as vulnerable to this as any other
fact — arguably more so, since "what's currently in progress" changes
every session. This file's job is to make "what's actually going on
right now" checkable in one place, not reconstructed from memory.

---

## Active Threads

| Item | Status | Notes |
|---|---|---|
| `ares.local` mDNS alias + nginx `server_name` fix | Done (jhm-spark + tsavo3 test server) | Verified: `ping ares.local` resolves; nginx reload succeeded |
| `resourceLinks` field in JSON export | Done | Verified across all 126 JSON files, 13,440 `ares.local` URLs, 0 remaining `ares.edu` |
| Full corpus regeneration (`ARES_HOST=ares.local`) | Done | All 42 sub-strands, 126 docx, 126 PDFs, teacher index — committed `5071ea4` |
| Provisioning script for ~100 school servers (`install.sh`) | Built, not yet tested live | Includes mDNS service, nginx patch, PDF deploy, `generate_teacher_index.js`, `index.htmlf` — Mark to test on one ARES server before wide rollout |
| Avahi/internet-dependency for `install.sh` | **Resolved — no reinstall needed** | `dpkg.log` history on `tsavo3` confirms `avahi-daemon`/`avahi-utils` present since Dec 2024, routinely updated since — baked into the Clonezilla golden image, not a live-internet install. Script has zero internet dependency as written. |
| Partner heads-up on `resourceLinks` schema impact | Message drafted, sent to partner by Mark | Awaiting partner's schema check — not blocking distribution |
| Tracking/attribution for the Grade 10 module link + PDF resource links | Not started | Deliberately scoped as a separate task, not bundled into today's work |
| Continuity protocol (`STATUS.md` + `/update` skill + `/restart` skill) | **Done — confirmed** | `CLAUDE.md`/`STATUS.md` continuity fixes confirmed pushed (`git log`/`git status` on jhm-spark, 2026-07-06: `HEAD`/`main`/`origin/main` all at `b477ef1`, clean tree). `/restart` skill added (`33ceab5`) and documented in `CLAUDE.md` (`222d681`, spacing fix `aa54484`) and this file (`68e7b47`). Tested live — see 2026-07-06 session-log entry below. |
| `.gitignore` scoped to allow `.claude/skills/` | Done, committed `2c7c938` | Was blanket-excluding all of `.claude/`; narrowed to `.claude/settings.local.json` only |
| Lesson-count table below (Summary + per-subject tables) | **Known stale — gap now much wider than previously noted** | Tables claim 12/33 sub-strands across 4 subjects; disk (`grep outputDir generators/data/*.js`, 2026-07-31) shows **85 sub-strands across 7 subjects** — Biology, Chemistry, Physics, Maths, Core_Mathematics, Essential_Mathematics, General_Science. Still a separate refresh task; do not improvise partial corrections. |
| Session-tooling commits `8d3fe16` / `1f4f6f8` / `9937ed3` | Done, recorded 2026-07-31 | Token-optimizer marketplace, tooling-defect fixes, code-review-graph install. Were pushed to `origin/main` without a STATUS.md entry — caught by `/restart` on 2026-07-31, see session log + Known Issues below. |
| code-review-graph CLAUDE.md wording — "ALWAYS use graph tools before Grep/Glob/Read" | **Done — scoped 2026-07-31** | Rewritten against measured coverage, not assumption: graph indexes exactly the 183 tracked `.js`/`.py`/`.sh` files and **0 of 52 tracked `.md` files**; all 85 `*_data.js` are bare `File` nodes (object-literal exports, no functions to graph). Section now states explicitly that reading `STATUS.md` is a plain `Read` no graph tool substitutes for, and that data-file inspection is `Read`/`grep` work. Two installer claims corrected: `semantic_search_nodes_tool` is FTS-only here (0 nodes embedded), and `tests_for` coverage checks are meaningless (1 Test node repo-wide). |
| `.claude/settings.json` Read deny rules | Done, `1f4f6f8` — with a known limit | 6 narrow rules (ares_index DB, `venv/`, `.env`, docx/pdf under `data/outputs`, archived `data/outputs/docx`). **Gate the Read tool only, not bash** — a recursive `grep` over `data/outputs/` still lands in context. Deliberately excludes `*_data.json` and `data/raw/curriculum_pdfs`. |
| Kenyan-terminology wording pass | Blocked | Waiting on example lessons from reviewing teachers |
| Grade 11 STEM expansion | Not started | Planned after terminology pass + initial distribution |
| Non-STEM subject expansion | Not started | Planned after Grade 11 |
| New Grade 10 STEM subjects (General Science, Core Mathematics, Essential Mathematics) | **Done — Phase 3 complete, committed `f6d6fab`** | All 43 sub-strands / 344 lessons generated, docx+PDF regenerated, teacher index rebuilt, pushed to `origin/main`. Handoff: `HANDOFF_new_stem_subjects_2026-07-28.md` (Rev 2). See 2026-07-30 session-log entry below for the bugs found/fixed along the way (subject-label bug, 34 stub lessons, 1 missing FE). Replacement Core Mathematics source PDF referenced in the handoff was never supplied but generation proceeded — flag if a full curriculum-text re-check against it is still wanted. Summary/per-subject tables below still need the separate full refresh already flagged as stale. |

---

## Summary

| Subject | Sub-strands complete | Sub-strands remaining | Lessons generated |
|---|---|---|---|
| Biology | 9 / 9 | 0 | 72 (8 per sub-strand) |
| Chemistry | 0 / 7 | 7 | 0 |
| Physics | 0 / 8 | 8 | 0 |
| Mathematics | 3 / 9 | 6 | 24 (8 per sub-strand) |
| **Total** | **12 / 33** | **21** | **~96 initial lessons** |

> **Stale as of 2026-07-05 — see "Known Issues" below.** Commit history
> confirms a full 42-sub-strand, 384-lesson production run completed
> after this table was last accurate. Do not trust these numbers; they're
> kept here only until someone does the refresh.

---

## Biology Grade 10 — COMPLETE

All 9 sub-strands generated. Teacher review in progress.

| Sub-strand | Name | KICD lessons | Generated | Files | Notes |
|---|---|---|---|---|---|
| 1.1 | Introduction to Biology | 6 | 8 | ✅ SoW + FE + ST | Existing (pre-pipeline) |
| 1.2 | Specimen Collection and Preservation | 14 | 8 | ✅ SoW + FE + ST | No teacher template |
| 1.3 | Cell Structure and Specialisation | 20 | 8 | ✅ SoW + FE + ST | Teacher template used |
| 1.4 | Chemicals of Life | 24 | 6 | ✅ SoW + FE + ST | Teacher template used; exemplar sub-strand |
| 2.1 | Nutrition in Plants | 12 | 12 | ✅ SoW + FE + ST | Teacher template used |
| 2.2 | Transport in Plants | 22 | 8 | ✅ SoW + FE + ST | No teacher template |
| 2.3 | Gaseous Exchange and Respiration in Plants | 22 | 8 | ✅ SoW + FE + ST | Teacher template used |
| 3.1 | Nutrition in Animals | 12 | 8 | ✅ SoW + FE + ST | No teacher template |
| 3.2 | Transport in Animals | 24 | 8 | ✅ SoW + FE + ST | No teacher template |
| 3.3 | Gaseous Exchange and Respiration in Animals | 24 | 8 | ✅ SoW + FE + ST | No teacher template |

**Output path:** `data/outputs/v2/Biology/` — corrected 2026-07; this doc
previously said `data/outputs/docx/Grade 10 Biology/`, which is a stale
path from an earlier pipeline restructure (see `SYSTEM_OVERVIEW.md`'s
output-path correction note). PDFs for teacher distribution are generated
into the parallel `data/outputs/v2/PDF/Biology/` tree — see
`docs/PDF_GENERATION.md`.

> **This document's completion tables (Summary, per-subject tables above)
> have not been reconciled against actual repo state as of 2026-07** and
> are known to undercount — commit history shows a full 42-sub-strand,
> 384-lesson production run (`Phase 3-5: full production run`, June 2026)
> across Biology, Chemistry, Physics, and Mathematics, well beyond what's
> reflected here. Treat the counts/checkmarks above as historical
> (May 2026) rather than current. A full refresh of this file is a
> separate open task — flagging here rather than guessing at corrected
> numbers.

---

## Chemistry Grade 10 — NOT STARTED

Teacher templates available for all sub-strands in `data/raw/CBE LESSON TEMPLATES/`.

| Sub-strand | Name | KICD lessons | Template file |
|---|---|---|---|
| 1.2 | The Atom | — | Chemistry 10.1.2 ATOM.docx |
| 1.3 | The Periodic Table | — | Chemistry 10.1.3 The periodic table.docx |
| 1.4 | Chemical Bonding | — | Chemistry 10.1.4 Chemical bonding.docx |
| 1.5 | Periodicity | — | Chemistry 10.1.5 The periodicity.docx |
| 2.1 | Acids, Bases and Salts | — | Chemistry 10.2.1 Acids and Bases.docx |
| 2.2 | Salts | — | Chemistry 10.2.2 Salts.docx |

**Batch submission command:**
```bash
for ss in 1.2 1.3 1.4 1.5 2.1 2.2; do
  python3 src/generate_substrand.py \
    --subject chemistry --substrand $ss \
    --output chem_${ss//./_} --lessons 8 --batch
done
```

---

## Physics Grade 10 — NOT STARTED

Teacher templates available for all sub-strands.

| Sub-strand | Name | KICD lessons | Template file |
|---|---|---|---|
| 1.2 | Pressure | — | Physics 10.1.2 PRESSURE Scheme of Work Template Grade 10.docx |
| 1.3 | Mechanical Properties of Materials | — | Physics 10.1.3 Mechanical properties of Materials.docx |
| 1.6 | Energy, Work, Power and Machines | — | Physics 10.1.6 Energy,work,power and machines.docx |
| 2.1 | Properties of Waves | — | Physics 10.2.1 Properties of Waves.docx |
| 2.2 | Radioactivity and Stability of Isotopes | — | Physics 10.2.2 Radioactivity and Stability of Isotopes.docx |
| 3.1 | Electrostatics | — | Physics 10.3.1 Electrostatics.docx |
| 3.3 | Introduction to Electronics | — | Physics 10.3.3 Introduction to electronics.docx |
| 4.1 | Greenhouse Effect and Climate Change | — | Physics 10.4.1 Green house effect and Climate change.docx |
| 4.2 | Introduction to Space Physics | — | Physics 10.4.2 Introduction to space physics.docx |

**Batch submission command:**
```bash
for ss in 1.2 1.3 1.6 2.1 2.2 3.1 3.3 4.1 4.2; do
  python3 src/generate_substrand.py \
    --subject physics --substrand $ss \
    --output phys_${ss//./_} --lessons 8 --batch
done
```

---

## Mathematics Grade 10 — PARTIAL

| Sub-strand | Name | KICD lessons | Generated | Files | Notes |
|---|---|---|---|---|---|
| 1.1 | Real Numbers | — | 0 | ❌ | Template exists |
| 1.2 | Indices and Logarithms | — | 0 | ❌ | Template exists |
| 1.3 | Quadratic Equations | — | 0 | ❌ | Template exists |
| 2.1 | Similarity and Enlargement | — | 0 | ❌ | Template exists |
| 2.2 | Reflection and Congruence | — | 8 | ✅ SoW + FE + ST | Pre-pipeline (legacy generator) |
| 2.3 | Rotation | — | 8 | ✅ SoW + FE + ST | Pre-pipeline (legacy generator) |
| 2.4 | Trigonometry 1 | — | 8 | ✅ SoW + FE + ST | Pre-pipeline (legacy generator) |
| 2.5 | Area of Polygons | — | 0 | ❌ | Template exists |
| 2.6 | Area of a Part of a Circle | — | 0 | ❌ | Template exists |
| 2.7 | Surface Area and Volume of Solids | — | 0 | ❌ | Two templates exist |
| 3.2 | Probability | — | 0 | ❌ | Template exists |

**Note:** Math 2.2, 2.3, 2.4 were generated by legacy per-subject generators (pre-refactor). They also produce `.html` and `.gfm` outputs in addition to `.docx`.

---

## Known Issues / Lessons Learned

### Batch API — JSON truncation
Claude occasionally generates JSON that is truncated or contains apostrophes in string values, causing parse failures. This results in stub lessons (empty content). **Standard practice:**
1. After every batch collect, run `node /tmp/check_data.js` to identify stubs
2. Use `scripts/patch_lesson.js` and `scripts/patch_fe.js` to repair

### Final Explanation generation
FE prompts with long context (full lesson titles + detailed instructions) can exceed output token limits. Use the short-prompt approach in `scripts/gen_bio33_fe.py` as a template — pre-fill section structure and ask Claude to fill content only.

### Git and large files
`data/ares_index/ares_content.db` (630MB) is gitignored. It lives on jhm-spark only. Always check for large files before pushing:
```bash
find . -size +50M -not -path './.git/*' -not -path './venv/*'
```

### Sub-strand naming in batch collect
The `--collect` command requires `--subject`, `--substrand`, `--output` to be omitted (it reads from the checkpoint file). If the checkpoint was not saved (e.g. script crashed after submit), manually create `.{name}_batch_id.txt` and `.{name}_batch_id.json` before collecting.

### Documentation drift — stated facts going stale silently (2026-07-04)
Two independent incidents, same root cause, same day:
1. `SYSTEM_OVERVIEW.md`, `WORKFLOW.md`, and `STATUS.md` all stated
   `data/outputs/docx/` as the output path — true when written, but
   superseded by `data/outputs/v2/` at some prior restructure. Nothing
   flagged the mismatch; it was only caught by manually grepping
   `outputDir` across every `*_data.js` file and cross-checking against
   the real filesystem.
2. `WORKFLOW.md` stated the git branch as
   `claude/setup-cbe-generation-ZKiIi` in four separate places. That
   branch no longer exists on the remote; `main` has for some time. Same
   pattern: a value copied forward as fact, never re-verified, repeated
   in multiple places so partial fixes could leave it inconsistent.

**Neither was caused by carelessness reading the docs** — a careful
reader would copy the stated value exactly, because nothing in the text
distinguished "true when written" from "true now." The fix is structural,
not a request for more vigilance:
- `WORKFLOW.md` now opens with a **Step 0** verification block
  (`git branch --show-current`, a live `outputDir` grep, a `soffice`
  check) to be run before any task touching git, paths, or sync — with
  an explicit rule that a mismatch against the Environment Reference
  table gets fixed immediately, not deferred.
- `WORKFLOW.md`'s **Environment Reference table is now the single source
  of truth** for branch name, output paths, and Drive sync destinations.
  Other docs (`SYSTEM_OVERVIEW.md`, `PDF_GENERATION.md`, this file) point
  back to it instead of restating the values independently.
- The Windows Drive-sync `.bat` file is now committed as
  `scripts/sync_to_drive.bat`, so its actual configured destinations are
  `grep`-able from jhm-spark instead of only checkable by someone
  physically at the Windows machine.

### `resourceLinks` in JSON export (2026-07-05)
- New field added to every lesson object in the JSON export, populated
  from `getAllPhaseResources()` output (`sections.js`, one new line —
  `lesson.resourceLinks = aresRes;` — placed just after the resource
  lookup call, exploiting JS object-reference semantics rather than
  requiring any change to `build_docs.js`'s serialization).
- Full corpus regenerated and verified: all 126 JSON files contain the
  field, 0 missing.
- **Partner impact not yet confirmed** — if `ares-contract.schema.json`
  uses `additionalProperties: false` near the lesson object, this new
  field could cause their checker to reject every document. Flagged to
  partner; check not yet done as of this writing.

### `ares.edu` → `ares.local` hostname migration (2026-07-05)
- Root cause: `ares.edu` only ever resolved via a local DNS server
  (`dnsmasq`) that requires this box to control DHCP — works when a box
  is its own hotspot, silently fails when plugged into an existing
  school router (which doesn't hand out this box as the DNS server).
  mDNS (`.local`) resolves via broadcast regardless of who runs DHCP,
  which is why `ares.local` works in both deployment modes.
- Fix: `src/ares_recommender.py`'s `ARES_HOST` env var (already existed,
  previously unused) set to `ares.local`; full corpus regenerated.
  `nginx`'s `server_name` directive updated to include `ares.local`
  alongside `ares.edu`/`www.ares.edu` (config lives in whichever file is
  actually symlinked in `sites-enabled/` — confirmed to vary in name
  across at least one box, don't assume a filename like `default`).
- A persistent mDNS alias requires a systemd service
  (`ares-mdns-alias.service`, publishes `ares.local` via `avahi-publish`
  and re-publishes on IP change) — a one-off `avahi-publish` command
  does NOT survive reboot and will silently regress if treated as done.
- **Discovered mid-fix, unrelated to hostnames:** `ares.edu` was also
  never actually reachable via mDNS in the first place — mDNS resolvers
  only ever resolve `.local` names by protocol; no configuration could
  have made `ares.edu` work over mDNS.
- Deployment to the ~100 school servers is via a provisioning script
  (`install.sh`, distributed as a zip with the PDF payload) rather than
  git — those servers aren't running this repo directly.

### Lesson-count discrepancy — Bio 2.1 Plant Nutrition (clarified 2026-07-05)
- `STATUS.md` said 12 lessons; actual current content has 10, under a
  different phenomenon (sukuma wiki, not the uploaded pumpkin reference
  doc) and a different filename convention (no `_L1-12` suffix).
- **Confirmed intentional, not corruption:** commit `02da69b`'s message
  explicitly states dynamic, non-hardcoded lesson counts as a deliberate
  design change; a current teacher template for the sukuma wiki version
  exists (`v2_owner_inventory/Biology/SS2.1_Plant_Nutrition`). The
  uploaded pumpkin reference document is from the superseded
  `data/outputs/docx/` tree.
- Lesson counts across all 42 sub-strands now range 6–13 (confirmed via
  direct inspection of every `*_data.js` file) — this is expected, not a
  bug, per the same intentional design.
- This is exactly why the Summary/per-subject tables above are flagged
  stale rather than corrected in place: the real counts are now known
  file-by-file, but a full authoritative refresh of this document hasn't
  been done yet, and shouldn't be improvised from a partial check.

### `generate_teacher_index.js` — two legitimate deployed copies (2026-07-05)
- One copy lives in this repo (`generators/generate_teacher_index.js`),
  using a relative `PDF_ROOT` path — correct for jhm-spark's own
  `data/outputs/v2/PDF/` tree.
- A second copy is bundled in the school-server provisioning package
  with `PDF_ROOT = __dirname` instead — correct because that copy always
  sits directly inside the deployed `PDF/` folder on every server.
- This is a real, permanent difference (not a mistake to unify) — but it
  means any future logic change to this script must be applied in both
  places manually. No automated sync between them exists.

### `CLAUDE.md` UTF-16 encoding + terminal-paste corruption (2026-07-05/06)
- `CLAUDE.md` was discovered saved as **UTF-16LE**, not UTF-8 — cause
  unknown; worth watching whether other project docs are similarly
  affected if this happens again. Converted and re-saved as plain UTF-8,
  no BOM, LF line endings.
- While fixing stale content in the same pass, two independent
  terminal-paste failure modes surfaced when transferring the corrected
  file via `python3 -c "...sys.stdin.read()"` + manual paste:
  1. **Long pastes can be silently truncated** by the terminal's paste
     buffer — a ~245-line paste landed as 60 lines with no error.
  2. **Box-drawing Unicode characters (`├ │ └`) are excluded from this
     chat interface's "Copy" button**, forcing manual reconstruction —
     which itself is error-prone (in one instance, the reconstruction
     accidentally included a command line from the surrounding
     instructions as if it were file content).
  3. Separately, at least one paste attempt resulted in the target file
     being fully truncated to 0 bytes — exact cause not diagnosed
     (suspected: a `'w'`-mode write with no actual stdin content, e.g.
     Ctrl-D pressed before pasting).
- **Resolution:** stopped using terminal copy-paste for this file
  entirely. Replaced the Repository Layout and output-file-listing tree
  diagrams with plain ASCII (full relative paths, no box-drawing
  characters), and delivered the corrected file as a direct download for
  transfer via `scp`/SFTP instead of paste.
- **Going forward:** for any file long enough to risk truncation, or
  containing special/Unicode characters, prefer direct file
  download + `scp`/SFTP transfer over terminal paste, chunked or
  otherwise. Chunking with placeholder blank-line markers
  (`%%%BLANK%%%`, converted back with `sed` after paste) is a viable
  fallback if direct transfer isn't available, but verify line count
  after every single chunk, not just at checkpoints — this incident
  involved two different corruption modes in adjacent attempts.

### Continuity rule held for content work, lapsed for tooling work (2026-07-31)

Three commits (`8d3fe16`, `1f4f6f8`, `9937ed3`) landed on `origin/main`
between 2026-07-30 and 2026-07-31 with **no Active Threads row and no
session-log entry** — the first time this file has fallen behind `main`
since the continuity protocol was established. Caught only because
`/restart` compares `git log` against this file; nothing else would have
surfaced it.

**The pattern worth noting:** the rule ("update STATUS.md as part of
finishing the work") has been followed reliably for *generation* work —
sub-strands, repairs, corpus runs — and silently skipped for *tooling*
work — settings, skills, MCP servers, plugin installs. Plausibly because
tooling changes don't feel like they change "project status," and because
some of them are performed by an installer rather than typed out. But
`9937ed3` appended a mandatory behavioral instruction to `CLAUDE.md`
telling every future session to prefer graph tools over `Grep`/`Read` —
that is a change to how sessions operate, and it went unrecorded.

Two follow-on consequences of the same lapse:
- `CLAUDE.md`'s header still read *Last updated: 2026-07-05* while
  carrying a section added 2026-07-31, and its Repository Layout section
  lists neither `.claude/skills/restart/` nor any of the four
  graph skills. A reader trusting the header would date the MCP section
  three weeks earlier than it is.
- This file's own header said *Last updated: 2026-07-05* despite two
  2026-07-30 entries. Fixed in the same pass.

**Takeaway:** "files changed" in the continuity rule means *any* tracked
file, including `.claude/`, `.mcp.json`, and `.gitignore` — not just
`generators/data/` and `data/outputs/`. Installer-generated changes count,
and arguably need *more* recording than hand-made ones, since nobody
composed a rationale for them at the time.

### Third-party installers can append behavioral instructions to `CLAUDE.md` (2026-07-31)

`code-review-graph install --platform claude-code` (`9937ed3`) modified
six tracked files, including appending an "ALWAYS use graph tools before
Grep/Glob/Read" section to `CLAUDE.md` and adding `PostToolUse`/
`SessionStart` hooks to `.claude/settings.json`. The settings merge was
additive and left the `1f4f6f8` deny rules intact — verified, not assumed.

The `CLAUDE.md` wording is unreviewed third-party text now carrying the
same authority as hand-written project rules, and it is overbroad here:
this project's most-read files are Markdown control documents and
`*_data.js` content modules, which a code-structure graph does not index
usefully. Left in place for now and tracked in Active Threads rather than
edited blind. **Lesson for future installs: diff what an installer wrote
into `CLAUDE.md` and `.claude/settings.json` before committing, and treat
any instruction text it adds as a proposal, not as project policy.**

---

## Cost Tracking

| Run | Sub-strands | Lessons | Mode | Approx. cost |
|---|---|---|---|---|
| Bio 1.4 (test) | 1 | 6 | Synchronous | ~$0.70 |
| Bio 1.4 (batch) | 1 | 6 | Batch | ~$0.35 |
| Bio 1.2, 2.2, 2.3, 3.1, 3.2, 3.3 | 6 | 8 each | Batch | ~$2.10 |
| **Biology total** | **9** | **~72** | Mixed | **~$5–8** |
| **Projected remaining** | **24** | **~192** | Batch | **~$14** |
| **Full 2,000-lesson target** | **~110** | **~2,000** | Batch | **~$114** |

---
## Updates — 2026-06-18

### Data file fixes (all committed to main)
- `bio_1_4_data.js`: UNIT block was empty (`{}`); fully populated with phenomenon, driving question, storyline thread, learning outcomes, competencies, values, SEP, PCIs, careers, focus, totalDuration
- All 9 Biology + 3 Math data files: UNIT-level `duration` → `totalDuration` (bio_2_1, math_2_2, math_2_3, math_2_4 patched)
- All 9 Biology data files: `storyline` / `"storyline"` → `storylineThread` (8 files patched; bio_2_1 and math files were already correct)

### New documentation
- `docs/SCHEMA.md` created — canonical field name reference and contract for colleague's JSON editing tool

### Remaining known inconsistency (cosmetic, non-functional)
- JSON-quoted keys (`"totalDuration":`) in bio_1_2, bio_2_2, bio_2_3, bio_3_1, bio_3_2, bio_3_3 — these work correctly but don't match the bare JS key style convention. Deferred to future cleanup.

---
## Updates — 2026-07-04

### New module: PDF generation for teacher distribution
- `generators/generate_pdfs.js` added — converts every `.docx` under
  `data/outputs/v2/` (Lesson Sequence, Final Explanation, Summary Table)
  to PDF via headless LibreOffice, batched for efficiency, logging and
  continuing past individual failures rather than halting the run.
- Output lands in a parallel `data/outputs/v2/PDF/` tree, mirroring the
  `Subject/SubStrand/` structure of the source docx exactly.
- `generators/generate_teacher_index.js` added — generates a static,
  self-contained `index.html` at the root of `v2/PDF/` listing every
  subject/sub-strand with links to its PDFs, for browsing on the offline
  ARES appliance over the school mesh network.
- Both `.docx` and PDF outputs now sync to Google Drive via separate
  robocopy jobs, tracked in `scripts/sync_to_drive.bat` (see
  `WORKFLOW.md` Environment Reference for current destinations — not
  restated here, see the Known Issues entry below for why). **How content
  moves from Drive to each school's offline appliance is still
  unresolved** — flagged as an open item in `docs/PDF_GENERATION.md`.
- Rationale, design decisions, and open items are documented in
  `docs/PDF_GENERATION.md`.
- Corrected stale `data/outputs/docx/` path references in this file and
  in `SYSTEM_OVERVIEW.md` / `WORKFLOW.md` — the current, authoritative
  output root is `data/outputs/v2/`, per each data file's `outputDir`.

---
## Updates — 2026-07-05

### Hostname migration + resource-link improvements
- Migrated all Resource-column links from `ares.edu` to `ares.local`
  across the entire corpus (42 sub-strands, 384 lessons, 126 docx, 126
  PDFs) — see "Known Issues" for full rationale. Zero `ares.edu`
  references remain; verified via full-corpus grep.
- Added `resourceLinks` field to the JSON export (every lesson, every
  phase) — see "Known Issues" for shape and partner-schema caveat.
- `nginx` `server_name` updated (jhm-spark test box) to accept
  `ares.local`; `ares-mdns-alias.service` created for persistent mDNS
  advertisement surviving reboots.
- `generators/generate_teacher_index.js` added to this repo (previously
  existed only as a standalone deployment on the ARES test server,
  which was itself a gap — see "Known Issues").

### Provisioning package for school-wide deployment
- Built `install.sh` + payload structure for deploying the `ares.local`
  mDNS fix, nginx config change, PDF content, and updated module landing
  page (`index.htmlf`) to ~100 independently-managed school servers.
- Not yet tested on real hardware as of this writing — Mark testing on
  one server before wide rollout.

### Continuity protocol established
- This file is now the designated single source of truth for project
  continuity (see "How this file is used" at the top).
- Added an `Active Threads` table (top of this file) and a `/update`
  skill (Claude Code: `.claude/skills/update/`) to force a continuity
  update on demand, independent of task completion.

### Still open going into next session
- `install.sh` live-tested on one real server
- Partner's `ares-contract.schema.json` checked against `resourceLinks`
- Tracking/attribution for the lesson-plan module link (scoped as
  separate task, not started)
- Full refresh of this file's Summary/per-subject lesson-count tables
- Kenyan-terminology wording pass (blocked on teacher-provided examples)
- Grade 11 STEM expansion, then non-STEM subject expansion (both not started)

---
## Updates — 2026-07-06 (triggered by `/update`)

### `CLAUDE.md` corrected and continuity protocol committed
- `CLAUDE.md` fixed: UTF-16 → UTF-8, stale content updated (branch,
  paths, `ares.edu` → `ares.local`), new "FIRST: Read STATUS.md's Active
  Threads" instruction added, box-drawing tree diagrams replaced with
  plain ASCII after terminal-paste corruption — full incident in "Known
  Issues" above.
- `.claude/skills/update/SKILL.md` and a `.gitignore` fix (was
  blanket-excluding `.claude/`, narrowed to `.claude/settings.local.json`)
  committed as `2c7c938`.
- Confirmed avahi-daemon/avahi-utils has been part of the Clonezilla
  golden image since at least December 2024 (routine version-upgrade
  history in `dpkg.log`), not something installed live — `install.sh`
  has no internet dependency for any of its ~100 target servers.
- **Not yet confirmed by this session:** whether the corrected
  `CLAUDE.md` and this `STATUS.md` update have actually been
  `git commit`/`git push`ed on jhm-spark. Verify with `git log --oneline
  -3` before treating this entry as fully closed.

---
## Updates — 2026-07-06 (second session, triggered by `/update`)

### Verified: continuity protocol commit/push (previously unconfirmed)
- Ran `git log --oneline -5` and `git status` on jhm-spark. Confirmed
  `HEAD`, `main`, `origin/main`, `origin/HEAD` all at `b477ef1`
  ("STATUS.md: continuity update via /update"), on top of
  `a0f40fe`/`2c7c938`. Working tree clean. Closes the item flagged
  unconfirmed at the end of the previous `/update` entry.

### New skill: `/restart` — continuity verification checkpoint
- Added `.claude/skills/restart/SKILL.md` (commit `33ceab5`) — re-reads
  `STATUS.md`/`CLAUDE.md`/`WORKFLOW.md`'s Environment Reference, runs
  WORKFLOW.md's Step 0 live checks, and reports drift before continuing,
  without discarding session context. Complementary to `/update`:
  `/update` is the write side of continuity, `/restart` is the
  read/verify side.
- Also usable by typing `/restart` in a Claude.ai session in this
  project (paragraph added to project custom instructions).
- Documented in `CLAUDE.md` (`222d681`, spacing fix `aa54484`) and in
  this file's "How this file is used" section (`68e7b47`).

### `/restart` tested live — found real drift, plus one operational caveat
- Triggered `/restart` in a Claude.ai chat. It correctly re-fetched
  `STATUS.md`/`CLAUDE.md` from GitHub and flagged that the Active
  Threads continuity-protocol row was still worded as unconfirmed, and
  that no session-log entry existed yet for today's `/restart` work —
  both real gaps, both closed by this `/update`.
- **Caveat surfaced:** `raw.githubusercontent.com` (used for the
  Claude.ai auto-fetch at conversation start, and for `/restart`) lags
  behind `git push` by a CDN cache interval — the fetch returned
  pre-push content (`Last updated: 2026-07-05`, no `/restart` mentions)
  even after four confirmed commits landed on `origin/main`. Expected
  CDN behavior, not a bug in `/restart` or the repo — but worth knowing:
  **if a Claude.ai session's `/restart` shows no drift right after a
  push, that isn't proof the push isn't reflected yet; cross-check with
  a live `git log` on jhm-spark if the timing is tight.**

### Still open going into next session
- `install.sh` live-tested on one real server
- Partner's `ares-contract.schema.json` checked against `resourceLinks`
- Tracking/attribution for the lesson-plan module link (scoped as
  separate task, not started)
- Full refresh of this file's Summary/per-subject lesson-count tables
- Kenyan-terminology wording pass (blocked on teacher-provided examples)
- Grade 11 STEM expansion, then non-STEM subject expansion (both not started)

---
## Updates — 2026-07-30 — New STEM subjects Phase 3 completed (resumed after interruption)

A prior session had gotten partway through `HANDOFF_new_stem_subjects_2026-07-28.md`
Phase 3 (full-batch generation of General Science / Core Mathematics / Essential
Mathematics, 43 sub-strands / 344 lessons) and was interrupted mid-flight. This
session used `/restart` to reconstruct exactly where it had left off from git
history, file mtimes, and the handoff document, then finished the phase.

### What the interrupted session had already done
- Phase 2 pilots (`gensci_1_3`, `coremath_2_2`, `essmath_2_8`) generated and
  passing `check_new_subjects_quality.js`.
- A real bug found and fixed in `src/generate_substrand.py`: `args.subject
  .capitalize()` mangled `general_science` → `General_science` instead of
  `General Science`. Fixed via a new `_subject_display()` helper.
- A retroactive patch (`/tmp/fix_subject_labels.js`, not committed — ad hoc)
  had corrected the 3 pilots' `META.subject`/`filePrefix`/`titleDoc`, but
  **missed the nested `UNIT.subject` field**, which feeds the "Subject:" row
  in the Lesson Sequence docx (`generators/lib/sections.js`).
- Because `filePrefix` changed, the pilots' old docx/json were deleted in
  prep for regeneration but `generate.js` was never re-run — they had zero
  output files at the point of interruption.
- Phase 3 had already run live generation for the remaining ~40 sub-strands,
  all of which inherited the same `UNIT.subject` bug.
- One sub-strand (`gensci_1_6`) had a leftover, already-`ended`
  (9/9 succeeded) batch checkpoint from an earlier abandoned batch attempt,
  superseded by a live run.

### What this session found and fixed on top of that
- **`UNIT.subject` bug**: extended the fix to all 43 data files (source of
  truth: each file's already-correct `META.subject`). Quality gate re-ran
  clean afterward.
- **`gensci_1_6` missing Final Explanation entirely** (`FINAL_EXPLANATION`
  absent) — generated via the API and patched with `scripts/patch_fe.js`.
- **34 stub lessons across 14 General Science sub-strands** (`gensci_1_2`,
  `1_4`, `1_5`, `1_6` [all 8 lessons], `1_7`, `2_1`–`2_5`, `3_1`–`3_4`) —
  the documented "Batch API — JSON truncation" failure mode, at larger
  scale than previously seen. Core Mathematics and Essential Mathematics
  were completely unaffected. Repaired all 34 via the `patch_lesson.js`
  workflow (individual API calls per stub, same pattern as
  `scripts/repair_stubs.py`).
- Removed the orphaned `.gensci_1_6_batch_id.{json,txt}` checkpoint files
  (batch already collected).

### Verification before commit
- Full stub/FE/ST scan across all 43 new sub-strand data files: clean —
  no stubs, FE and ST present for all.
- `node check_new_subjects_quality.js`: PASS.
- `node generators/generate.js --all`: 0 errors, all 43 new sub-strands
  produced 4 files each (docx ×3 + json).
- `node generators/generate_pdfs.js`: 255 converted, 0 failed.
- `node generators/generate_teacher_index.js`: 7 subjects, 85 sub-strands,
  255 documents indexed.

### Committed and pushed
- `f6d6fab` on `main` (649 files: all General Science / Core Mathematics /
  Essential Mathematics docx+json+PDF, the fixed `generators/data/*.js`
  files, `src/generate_substrand.py`). Confirmed pushed to `origin/main`.

### Still open going into next session
- Full refresh of this file's Summary/per-subject lesson-count tables
  (already stale before this session; now further behind since it doesn't
  reflect the new subjects at all)
- Whether to formally verify the 43 sub-strand names against the
  replacement Core Mathematics PDF referenced in the handoff (never
  supplied to jhm-spark) — generation proceeded on the original curriculum
  text without it
- Everything else listed in the previous session's "still open" list above
  (install.sh live test, partner schema check, terminology pass, Grade 11
  expansion, etc.) — untouched by this session

---
## Updates — 2026-07-30 (continued) — Process retrospective and fixes

Mark asked for a retrospective on three concerns from the session above:
the resume-and-repair work took much longer than expected, API cost ran
well over the documented estimate, and the session needed more approval
round-trips than felt warranted. Root cause in all three cases: the one
automated gate this project had (`check_new_subjects_quality.js`) only ever
checked the 3 Phase-2 pilots, so it reported "PASS, safe to proceed" while
structurally blind to the 40 sub-strands Phase 3 actually generated. Fixes:

- **`check_new_subjects_quality.js` rewritten** (commit `bb0faf9`) to glob
  every `gensci_`/`coremath_`/`essmath_` data file instead of naming a fixed
  list, plus a new check (#6: `META.subject` == `UNIT.subject`) added to
  catch the exact partial-patch bug this session hit earlier. Widening the
  gate immediately proved the point: it surfaced a real, previously
  undetected defect — **39/43 files had non-canonical phase-label formats**
  (e.g. `"Phase 1 — PREDICT (15 minutes)"` instead of the locked
  `"Predict Phase"`). Not cosmetic: `generators/lib/sections.js` keys ARES
  resource-category matching and row-color lookups off that exact string,
  both with silent fallbacks — so 1195 rows across the new corpus were
  silently getting the wrong ARES resource bucket and default grey shading.
  Fixed as a zero-cost deterministic remap (verified safe: every lesson's
  framework array has exactly 5 entries, self-numbered 1-5 matching array
  position in all 344 lessons) — no regeneration/API cost needed, just
  docx/PDF re-render. Committed and pushed as part of `bb0faf9`.
- **`WORKFLOW.md`** (commit `9d0d373`): `--batch` is now a hard default
  beyond a 1-3 sub-strand pilot (was "preferred") — `--run` is 2x batch
  pricing and a resumed session can otherwise silently inherit whatever
  mode the interrupted session was using. Added a 15-20% repair-pass
  contingency to the cost estimate table, since the documented ~$114
  figure assumed zero-defect generation and this run's actual defect rate
  (34 stub lessons + 1 missing FE + 1195 mislabeled rows, all repaired via
  extra live-mode calls) was well above zero.
- **`src/generate_substrand.py`** (commit `9d0d373`): now tracks real token
  usage (sync and batch) per run and logs it with an estimated cost to the
  new `logs/api_cost_log.md`, so future cost estimates can be checked
  against this pipeline's actual observed spend instead of a generic table.
- **`CLAUDE.md`** (commit `9d0d373`): added an "Autonomy checkpoints" policy
  to the Project Rigor Assessment section — for resume/repair/extend tasks,
  ask once up front whether to keep fixing-and-regenerating on standing
  authorization vs. check in per discovery, instead of re-asking separately
  each time a new problem of the same kind turns up. Level 2/3 phase-
  boundary checkpoints are unaffected by this.

### Still open going into next session
- Whether actual spend on the next bulk run tracks the new 15-20%
  contingency, or whether the estimate itself needs further revision
  (check `logs/api_cost_log.md` once there's another real run to compare)
- Everything else already listed above (Summary/per-subject table refresh,
  Core Mathematics replacement-PDF verification, install.sh live test,
  partner schema check, terminology pass, Grade 11 expansion)

---
## Updates — 2026-07-31 (triggered by `/restart`, then `/update`)

No generation, repair, or content work this session. A `/restart` was run
to re-ground a fresh session; it found real drift, and this entry closes it.

### `/restart` live checks — all clean, don't re-run without cause
- Branch `main`; working tree clean; `HEAD` == `origin/main` == `9937ed3`.
- `soffice` present at `/usr/bin/soffice`.
- `outputDir` across all 85 `generators/data/*.js` files: every value under
  `v2/<Subject>/<SubStrand>`. No stale `data/outputs/docx/` paths remain in
  any data file.
- `WORKFLOW.md` Environment Reference (line 315) matches all of the above.

### Drift found and fixed by this entry
- Three commits were on `origin/main` with no record in this file:
  `8d3fe16` (token-optimizer plugin marketplace, project scope),
  `1f4f6f8` (tooling-defect fixes: stale `.claude/commands/commit.md`
  rewritten — it was carried over from an unrelated project and told
  sessions to put status in `CLAUDE.md`, directly contradicting this
  project's rule; missing YAML frontmatter added to
  `.claude/skills/restart/SKILL.md`; 6 narrow Read deny rules added),
  and `9937ed3` (code-review-graph 2.3.7 installed, MCP server + 4 skills
  + `CLAUDE.md` section + hooks). All three now have Active Threads rows.
- Both `STATUS.md` and `CLAUDE.md` had `Last updated: 2026-07-05` headers
  despite carrying much newer content. This file's header corrected to
  2026-07-31; `CLAUDE.md`'s corrected in the same commit, along with its
  Repository Layout section, which listed neither `.claude/skills/restart/`
  nor the four graph skills.
- Two Known Issues entries added — see "Continuity rule held for content
  work, lapsed for tooling work" and "Third-party installers can append
  behavioral instructions to `CLAUDE.md`."

### Still open going into next session
- **Scope the code-review-graph `CLAUDE.md` wording** (new this session) —
  "ALWAYS use graph tools before Grep/Glob/Read" is unreviewed third-party
  text and is wrong for `.md` control docs and `*_data.js` modules.
- **Full refresh of the Summary/per-subject lesson-count tables** — now
  quantified: tables say 12/33 across 4 subjects, disk has 85 across 7.
  Longest-standing open item in this file (flagged since 2026-07-05).
- Whether actual spend on the next bulk run tracks the new 15–20%
  contingency (`logs/api_cost_log.md` — no new run since it was added).
- Core Mathematics replacement-PDF verification (PDF never supplied).
- `install.sh` live test on one real ARES server.
- Partner's `ares-contract.schema.json` checked against `resourceLinks`.
- Kenyan-terminology wording pass (blocked on teacher-provided examples).
- Tracking/attribution for the Grade 10 module link.
- Grade 11 STEM expansion, then non-STEM expansion.

---
## Updates — 2026-07-31 (second entry) — code-review-graph wording scoped

Closed the "needs scoping" item opened earlier today. No code or content
changed; `CLAUDE.md` + `STATUS.md` only.

### Measured graph coverage — verified, don't re-derive
- Indexed: **exactly the 183 tracked `.js`/`.py`/`.sh` files** (`git ls-files
  '*.js' '*.py' '*.sh' | wc -l` == 183 == graph `files_count`).
- **0 of 52 tracked `.md` files indexed** — languages are python/bash/
  javascript only. Every control document in this project is invisible to
  the graph.
- All 85 `generators/data/*_data.js` are indexed as bare `File` nodes with
  no contained functions — they export object literals, so there is no call
  graph to build. The graph knows these files exist and nothing about what
  is in them.
- `embeddings_count` == 0, so `semantic_search_nodes_tool` silently falls
  back to FTS keyword matching (`search_mode: "fts"` in its own response).
  It is a symbol lookup, not concept search.
- 1 `Test` node repo-wide. `query_graph_tool` pattern="tests_for" cannot
  function as a coverage signal here in either direction.

### What changed in `CLAUDE.md`
- The blanket "ALWAYS use graph tools BEFORE Grep/Glob/Read" replaced with
  a scoped rule: prefer the graph for executable-code questions, and a
  "What the graph does not cover" section listing the three blind spots
  above. Explicitly states that reading `STATUS.md`'s Active Threads — this
  project's mandatory first action — is a plain `Read` with no graph
  substitute, which the original wording implicitly discouraged.
- Notes that past data-integrity bugs (stub lessons, `UNIT.subject`
  mismatch, phase-label drift) were all found by `Read`/`grep` over data
  files, precisely the reads the original wording deprioritized.
- Workflow step 4 (`tests_for` coverage check) struck through with a
  pointer to the caveat.
- A short provenance banner marks the section as installer-generated and
  hand-scoped, so a future reader doesn't mistake it for original policy.

### Still open going into next session
- **Full refresh of the Summary/per-subject lesson-count tables** — now the
  longest-standing open item (flagged 2026-07-05); 12/33 across 4 subjects
  on paper vs. 85 across 7 on disk.
- Everything else from this morning's entry is unchanged: cost-contingency
  check against `logs/api_cost_log.md`, Core Mathematics replacement-PDF
  verification, `install.sh` live test, partner schema check, terminology
  pass, module-link tracking, Grade 11 expansion.
