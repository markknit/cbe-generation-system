#!/usr/bin/env node
/**
 * validate_corpus.js — contract check across EVERY generators/data/*_data.js
 *
 * Why this exists (2026-08-02): a partner's import checker found two defects in
 * the General Science corpus that this project's own gates could not see —
 * `check_new_subjects_quality.js` covers only gensci_/coremath_/essmath_ files,
 * and nothing at all validated Biology/Chemistry/Physics/Maths. Both defects
 * render as SILENTLY EMPTY docx cells (sections.js reads `slo.safetyNotes` and
 * build_docs.js reads `summaryTablePrompt.explained` with undefined/`|| ''`
 * fallbacks), so no run ever errored and no output looked obviously wrong.
 *
 * Checks, per lesson:
 *   1. required top-level fields present and non-empty
 *   2. slo has EXACTLY the 7 canonical keys  (catches `safety<N>otes`)
 *   3. summaryTablePrompt has observed + learned + explained, all non-empty
 *   4. framework is the 5 canonical phases, in order, all cells non-empty
 *      (sections.js keys ARES resource buckets and row shading off these exact
 *       strings)
 *   5. lesson.number matches its array position sequence
 *   6. no stub lessons (overview suspiciously short)
 * and per module: every META / UNIT / FINAL_EXPLANATION / SUMMARY_TABLE field
 * the renderers print, META.subject === UNIT.subject, one Summary Table row per
 * lesson, and (stricter than rendering) FINAL_EXPLANATION / SUMMARY_TABLE must exist. All of it lives in generators/lib/lesson_contract.js checkModule(),
 * which build_docs.js run() also calls: a module that fails here won't render.
 *
 * Usage:
 *   node scripts/validate_corpus.js            # all files
 *   node scripts/validate_corpus.js gensci_    # only files matching a prefix
 *   CBE_DATA_DIR=data/revised_2026-10_full/modules node scripts/validate_corpus.js
 *                                              # another data dir (same variable as generate.js)
 *
 * Exit 0 = clean, 1 = at least one ERROR. Warnings never fail the run.
 */
'use strict';
const fs = require('fs');
const path = require('path');

const DATA_DIR = process.env.CBE_DATA_DIR
  ? path.resolve(process.env.CBE_DATA_DIR)
  : path.join(__dirname, '..', 'generators', 'data');
const filter = process.argv[2] || '';

// All errors come from the shared contract, the same check build_docs.js run()
// makes before rendering and patch_lesson.js makes before writing a lesson.
const { nonEmpty, checkModule } = require('../generators/lib/lesson_contract');

function checkFile(file) {
  const errors = [], warnings = [];
  const name = file.replace(/_data\.js$/, '');
  let mod;
  try {
    mod = require(path.join(DATA_DIR, file));
  } catch (e) {
    return { name, errors: [`${name}: failed to load — ${e.message}`], warnings, lessons: 0 };
  }

  for (const e of checkModule(mod, { requireDocs: true })) errors.push(`${name} ${e}`);

  const lessons = Array.isArray(mod.LESSONS) ? mod.LESSONS : [];
  lessons.forEach((l, i) => {
    if (l && typeof l === 'object' && !nonEmpty(l.aresKeywords)) {
      warnings.push(`${name} L${l.number !== undefined ? l.number : `@${i}`}: `
                  + 'aresKeywords missing or empty (falls back to the title for the ARES lookup)');
    }
  });
  return { name, errors, warnings, lessons: lessons.length };
}

const files = fs.readdirSync(DATA_DIR)
  .filter(f => f.endsWith('_data.js'))
  .filter(f => f.startsWith(filter))
  .sort();

if (files.length === 0) {
  console.error(`No *_data.js files matched "${filter}" in ${DATA_DIR}`);
  process.exit(1);
}

let allErrors = [], allWarnings = [], totalLessons = 0, badFiles = 0;
for (const f of files) {
  const r = checkFile(f);
  totalLessons += r.lessons;
  if (r.errors.length) badFiles++;
  allErrors.push(...r.errors);
  allWarnings.push(...r.warnings);
}

console.log(`Validated ${files.length} data files / ${totalLessons} lessons`
          + (filter ? ` (filter: "${filter}")` : ''));

if (allWarnings.length) {
  console.log(`\nWARNINGS (${allWarnings.length}) — not failures:`);
  for (const w of allWarnings) console.log(`  ! ${w}`);
}

if (allErrors.length) {
  console.log(`\nERRORS (${allErrors.length}) across ${badFiles} file(s):`);
  for (const e of allErrors) console.log(`  ✗ ${e}`);
  console.log(`\nFAIL — ${allErrors.length} contract violation(s).`);
  process.exit(1);
}

console.log('\nPASS — no contract violations.');
