# PDF Generation — Rationale and Reference

*Added 2026-07-04. Distribution section last updated 2026-07-04 (same day
— PDF sync destination confirmed after initial draft; mesh-network
delivery to schools still open, see below).*

## Why PDF exists as a third output format

The pipeline already produces two formats per sub-strand document:

- **`.docx`** — the editable master. This is what the partner's automated
  contract checker validates against `ares-contract.schema.json`, and
  what anyone doing manual content edits works from.
- **`.html`** (dashboard only) — used for the internal generation-progress
  dashboard on jhm-spark. Not teacher-facing, not a document format.

Neither is right for the actual job of getting a finished lesson plan into
a teacher's hands, whether on the ARES website or as a download:

| Requirement | `.docx` | HTML | PDF |
|---|---|---|---|
| Renders in a browser without a plugin/viewer | No | Yes | Partial (native in most browsers, but not universally) |
| Fixed layout (landscape, 5-column table, page breaks) guaranteed identical on every device | Yes, but only inside Word/LibreOffice | No — reflows per screen/browser | **Yes** |
| Opens and displays correctly with zero network connection, on any device, using the device's built-in viewer | Requires Word/LibreOffice installed | Requires the full page saved correctly (fragile) | **Yes — single self-contained file** |
| Native annotation/highlighting support in common readers (Adobe, Preview, Google PDF viewer, browser PDF viewers) without installing anything | No | No | **Yes** |
| Editable by teachers (not wanted here — see below) | Yes | Yes | No |

The decision (see full discussion in project chat, 2026-07-04): **PDF is
the format teachers see and download.** `.docx` stays internal — partner
validation input and the editable master — and is never routed to
teachers directly. A thin HTML layer exists only for *browsing/finding*
the right document on the ARES website; clicking through always lands on
a PDF, never an inline-rendered docx or a raw HTML lesson plan.

The "editable by teachers" row is deliberately weighted against `.docx`
and HTML here: full content editing is explicitly out of scope for this
distribution format and is being handled by a separate tool the partner
is building against the JSON/data layer, not against rendered documents.
PDF's inability to be edited is a feature for this use case, not a gap —
it keeps the distributed copy from silently diverging from the source of
truth. Annotation (highlighting, margin notes, freehand marks on a
teacher's own copy) is different from editing and is well-supported by
PDF; that's the annotation use case this format choice serves.

---

## Module: `generators/generate_pdfs.js`

**What it does:** scans `data/outputs/v2/` for every `.docx` file
(`_CBE_LessonSequence`, `_FinalExplanation`, `_SummaryTable` — all three
per sub-strand), converts each to PDF via headless LibreOffice, and
writes the result into a parallel `data/outputs/v2/PDF/` tree that
mirrors the source `Subject/SubStrand/` folder structure exactly:

```
data/outputs/v2/Biology/SS2.1_Plant_Nutrition/Biology_Plant_Nutrition_CBE_LessonSequence.docx
data/outputs/v2/Biology/SS2.1_Plant_Nutrition/Biology_Plant_Nutrition_FinalExplanation.docx
data/outputs/v2/Biology/SS2.1_Plant_Nutrition/Biology_Plant_Nutrition_SummaryTable.docx
data/outputs/v2/Biology/SS2.1_Plant_Nutrition/Biology_Plant_Nutrition_data.json

data/outputs/v2/PDF/Biology/SS2.1_Plant_Nutrition/Biology_Plant_Nutrition_CBE_LessonSequence.pdf
data/outputs/v2/PDF/Biology/SS2.1_Plant_Nutrition/Biology_Plant_Nutrition_FinalExplanation.pdf
data/outputs/v2/PDF/Biology/SS2.1_Plant_Nutrition/Biology_Plant_Nutrition_SummaryTable.pdf
```

**Design decisions and why:**

- **Separate script, run after `generate.js`, not embedded in it.**
  Headless LibreOffice has a real per-invocation startup cost. Embedding
  conversion inside the per-lesson generation loop would mean paying that
  cost once per file — 126 times today, 2,000+ at full target. Running it
  as a distinct pass lets LibreOffice convert many files in a single
  process invocation instead.
- **Batched invocation (150 files per `soffice` call).** LibreOffice
  accepts a list of input files in one headless call. Batching amortizes
  the startup cost across the whole batch rather than paying it per file.
  150 was chosen as a safe margin under typical shell/exec argument-length
  limits, not a hard technical ceiling — adjust `BATCH_SIZE` if needed.
- **Isolated LibreOffice profile
  (`-env:UserInstallation=file:///tmp/lo_profile_pdfgen`).** Headless LO
  instances lock a shared user profile by default. Without isolation, a
  batch run could collide with a LibreOffice window opened manually on
  jhm-spark for visual layout QA (throwing "another instance is already
  running"), or with a concurrent run of this same script.
- **Log-and-continue error handling, not fail-fast.** A conversion
  failure on one file is recorded in a `Failed conversions` list printed
  at the end of the run; it does not stop the batch. Chosen deliberately
  over halting like a schema-contract violation would, because a single
  malformed or oversized document shouldn't block PDF delivery for
  everything else in a 2,000-lesson run. Failures should be reviewed and
  re-run individually — see `WORKFLOW.md` Step 6b.
- **Filename-collision fallback.** If two different sub-strand folders
  happen to produce the same basename, those files are converted
  one-at-a-time outside the batch mechanism, since batch conversion
  assumes unique basenames within a single LibreOffice invocation.
- **Nested `v2/PDF/` rather than a fully separate top-level tree.**
  Chosen so that `.docx` and PDF outputs can be synced to different
  destinations independently (see Distribution section below) without
  the PDF tree being scattered relative to its source docx, and without
  needing path-remapping logic in the conversion script itself — the
  destination path is always the source path with `v2/` replaced by
  `v2/PDF/` and the extension changed.

**Usage:**
```bash
node generators/generate_pdfs.js
```
No arguments — it always processes the full `v2/` tree. Safe to re-run;
it will simply reconvert and overwrite existing PDFs (no incremental/skip
logic currently — worth adding if conversion time becomes a bottleneck at
full scale).

---

## Module: `generators/generate_teacher_index.js`

**What it does:** scans `data/outputs/v2/PDF/` and writes a single static
`index.html` at its root, listing every subject and sub-strand with
direct links to its PDFs.

**Design decisions and why:**

- **Plain static HTML, zero external dependencies** (no CDN fonts, no
  icon libraries, no framework). The page is served to schools over an
  offline mesh network to devices of unknown/mixed capability — anything
  requiring a network fetch to render (a Google Font, a CDN-hosted icon
  set) would simply fail to load in that environment. System font stacks
  only; a single inline `<style>` block; a single inline `<script>` block
  for the optional search filter.
- **Colour palette matches the documents themselves** (`darkBlue`
  `#1F3864`, plus accent colours for the three document-type badges),
  pulled from `SYSTEM_OVERVIEW.md`'s existing Colour Palette rather than
  a new palette — so the index and the PDF a teacher opens from it read
  as one product.
- **No CSS Grid, no flexbox `gap`.** Both were tried first; testing
  against an older WebKit-based renderer (wkhtmltoimage, used here purely
  as a stand-in for "an embedded/older browser engine," not a claim about
  what the actual school appliances run) showed real, visible spacing
  bugs with both. Rewritten to plain flexbox + margins, which has the
  broadest practical support of the layout techniques considered. Worth
  re-testing against whatever the actual appliance browser is once known.
- **Search filter is enhancement, not a dependency.** Implemented in
  plain JS with no libraries; every subject and sub-strand remains fully
  visible and clickable if JS is disabled or unsupported — the filter
  only ever hides/shows what's already rendered.
- **Grouping and titles are derived from folder/file names, not from
  `_data.json`.** The JSON export's exact nested structure (whether
  `META`/`UNIT` are nested objects or flattened keys) hasn't been
  confirmed against a real file, so the generator avoids depending on it.
  Folder names (`SS2.1_Plant_Nutrition`) and filename suffixes
  (`_CBE_LessonSequence.pdf` etc.) are the only inputs, and are already
  confirmed accurate from a real `ls` of the `v2/` tree. Richer per-lesson
  metadata (e.g. a phenomenon blurb) is a possible future enhancement
  once the JSON shape is confirmed — not attempted here to avoid another
  guessed-structure mistake like the `docx/` vs `v2/` path issue.
- **Pure function of what's on disk, no incremental state.** Safe to
  re-run any time after `generate_pdfs.js`; always fully regenerates.

**Usage:**
```bash
node generators/generate_teacher_index.js
```
Must run *after* `generate_pdfs.js` — it indexes whatever PDFs already
exist on disk at the time it runs.

---

## Distribution: two independent sync paths

`.docx` and PDF outputs are kept in physically separate destinations,
since they serve different audiences and different infrastructure:

- **`.docx`** → Google Drive (`G:\My Drive\CBE Outputs`), via the existing
  Windows robocopy job. Audience: Mark, the partner's contract checker
  (indirectly, via git), anyone doing manual content edits.
- **PDF** → Google Drive (`G:\My Drive\CBE Outputs\PDF`), via a second,
  independent robocopy job (confirmed 2026-07-04). Audience: teachers.
  This job's file mask is `*.pdf *.html` — **not** `*.pdf` alone — since
  `index.html` from `generate_teacher_index.js` must sync alongside the
  PDFs it links to; a `*.pdf`-only mask would silently leave it behind
  every time.

This is a deliberate split, not an oversight: keeping the master/editable
format and the read-only distribution format on separate sync paths means
a change to one destination (e.g. restructuring the Drive folder) can't
accidentally affect the other.

**Still genuinely open, as of 2026-07-04: how content actually reaches
each school's offline appliance.** Google Drive is confirmed as *a*
distribution point, but each school runs an identical codebase on a
mesh-network-connected local server, with data files "updated manually as
needed" (Mark's words) — the concrete mechanism behind that (USB drive
during a site visit, a periodic connectivity window, something else) has
not been described anywhere in this project's chat history or
documentation as of this writing. Until that's known, "synced" only
means as far as GitHub and Google Drive — **not** confirmed to mean "on a
teacher's screen at a school." Update this section once that mechanism is
identified, and cross-check that it actually picks up `v2/PDF/` (docx
tree, PDF tree, or both) rather than assuming it does.

---

## Related files

- `generators/generate_pdfs.js` — the docx→PDF conversion script
- `generators/generate_teacher_index.js` — the index page generator
- `WORKFLOW.md` Step 6b (PDF generation), Step 6c (index page), Step 8 (Drive sync)
- `SYSTEM_OVERVIEW.md` — Component Reference entries for both scripts + corrected output-path note
- `STATUS.md` — 2026-07-04 update entry
