#!/usr/bin/env node
/**
 * check_new_subjects_quality.js
 *
 * Automated pass/fail gate for General Science / Core Mathematics / Essential
 * Mathematics sub-strand data files.
 *
 * Originally hardcoded to the 3 Phase-2 pilots only, on the theory that a
 * pilot pass was sufficient signal to launch Phase 3's full batch. That left
 * this gate blind to the 40 sub-strands Phase 3 actually generated - a
 * schema-consistency bug and 34 stub lessons across those files went
 * undetected until a manual, ad-hoc scan was run in a later session.
 * Rewritten 2026-07-30 to glob every gensci_/coremath_/essmath_ data file
 * instead of naming a fixed list, so "PASS" always means the full corpus was
 * actually checked, not just whichever files someone remembered to name.
 *
 * Run from the repo root on jhm-spark:
 *   node check_new_subjects_quality.js
 *
 * Exit code 0  -> every matching file passes, safe to proceed
 * Exit code 1  -> at least one file failed a check - do not proceed
 *
 * Checks per file:
 *   1. No stub lessons (overview >= 50 chars, same threshold as check_data.js)
 *   2. FINAL_EXPLANATION.sections is non-empty
 *   3. SUMMARY_TABLE.lessons is non-empty
 *   4. Every framework[].phase is one of the five locked labels, verbatim -
 *      catches numbered-prefix contract violations (e.g. "1 - PREDICT (10 min)")
 *   5. Top-level schemaVersion is present (see docs/SCHEMA.md)
 *   6. META.subject and UNIT.subject match exactly (catches the
 *      "Core_mathematics" vs "Core Mathematics" class of label bug, where a
 *      partial retroactive patch fixed one copy of the field but not the
 *      other)
 */

const fs = require('fs');
const path = require('path');

const LOCKED_PHASES = [
  'Predict Phase',
  'Observe Phase',
  'Explain Phase',
  'Driving Question Board (DQB) Creation',
  'Model Building Phase',
];

const DATA_DIR = path.join(__dirname, 'generators', 'data');

const NAME_PATTERN = /^(gensci|coremath|essmath)_.*_data\.js$/;

const files = fs.readdirSync(DATA_DIR)
  .filter(f => NAME_PATTERN.test(f))
  .map(f => f.replace(/_data\.js$/, ''))
  .sort();

if (files.length === 0) {
  console.log('No gensci_/coremath_/essmath_ data files found under ' + DATA_DIR + ' - nothing to check.');
  process.exit(1);
}

console.log(`Scanning ${files.length} sub-strand data file(s): ${files.join(', ')}\n`);

let anyFailure = false;
let failedCount = 0;

for (const name of files) {
  const modPath = path.join(DATA_DIR, `${name}_data.js`);
  console.log(`--- ${name}_data.js ---`);

  let mod;
  try {
    delete require.cache[require.resolve(modPath)];
    mod = require(modPath);
  } catch (e) {
    console.log(`  FAIL  could not load data file: ${e.message}`);
    anyFailure = true;
    failedCount++;
    continue;
  }

  let ok = true;

  // 1. stub lessons
  const lessons = mod.LESSONS || [];
  if (lessons.length === 0) {
    console.log('  FAIL  LESSONS array is empty');
    ok = false;
  } else {
    const stubs = lessons.filter(l => !l.overview || l.overview.length < 50);
    if (stubs.length > 0) {
      console.log(`  FAIL  ${stubs.length}/${lessons.length} stub lesson(s): ` +
        stubs.map(l => l.number).join(', '));
      ok = false;
    } else {
      console.log(`  ok    ${lessons.length}/${lessons.length} lessons have content`);
    }
  }

  // 2. Final Explanation
  const feSections = mod.FINAL_EXPLANATION && mod.FINAL_EXPLANATION.sections;
  if (!feSections || feSections.length === 0) {
    console.log('  FAIL  FINAL_EXPLANATION.sections missing or empty');
    ok = false;
  } else {
    console.log(`  ok    FINAL_EXPLANATION has ${feSections.length} section(s)`);
  }

  // 3. Summary Table
  const stLessons = mod.SUMMARY_TABLE && mod.SUMMARY_TABLE.lessons;
  if (!stLessons || stLessons.length === 0) {
    console.log('  FAIL  SUMMARY_TABLE.lessons missing or empty');
    ok = false;
  } else {
    console.log(`  ok    SUMMARY_TABLE has ${stLessons.length} row(s)`);
  }

  // 4. Phase labels - exact match against the five locked values
  const badPhases = [];
  for (const lesson of lessons) {
    for (const row of (lesson.framework || [])) {
      if (!LOCKED_PHASES.includes(row.phase)) {
        badPhases.push(`lesson ${lesson.number}: "${row.phase}"`);
      }
    }
  }
  if (badPhases.length > 0) {
    console.log(`  FAIL  ${badPhases.length} non-conforming phase label(s):`);
    badPhases.slice(0, 5).forEach(b => console.log(`          ${b}`));
    ok = false;
  } else {
    console.log('  ok    all phase labels match the five locked values exactly');
  }

  // 5. schemaVersion (top-level export per docs/SCHEMA.md, not nested under META)
  if (!mod.schemaVersion) {
    console.log('  FAIL  schemaVersion missing (see docs/SCHEMA.md)');
    ok = false;
  } else {
    console.log(`  ok    schemaVersion = ${mod.schemaVersion}`);
  }

  // 6. META.subject / UNIT.subject consistency
  const metaSubject = mod.META && mod.META.subject;
  const unitSubject = mod.UNIT && mod.UNIT.subject;
  if (metaSubject !== unitSubject) {
    console.log(`  FAIL  META.subject ("${metaSubject}") != UNIT.subject ("${unitSubject}")`);
    ok = false;
  } else {
    console.log(`  ok    META.subject and UNIT.subject both = "${metaSubject}"`);
  }

  if (!ok) { anyFailure = true; failedCount++; }
  console.log(`  ${ok ? 'PASS' : 'FAIL'} overall for ${name}\n`);
}

console.log('='.repeat(60));
if (anyFailure) {
  console.log(`RESULT: FAIL - ${failedCount}/${files.length} file(s) have issues.`);
  console.log('Do NOT proceed with docx/PDF generation for the affected file(s).');
  console.log('Fix what is flagged above, regenerate, and re-run this check.');
  process.exit(1);
} else {
  console.log(`RESULT: PASS - all ${files.length} file(s) clean.`);
  process.exit(0);
}
