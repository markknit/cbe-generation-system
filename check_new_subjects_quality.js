#!/usr/bin/env node
/**
 * check_new_subjects_quality.js
 *
 * Automated pass/fail gate for the three pilot sub-strands, so full batch
 * generation (43 sub-strands) can proceed without waiting on a manual
 * review of the pilots first.
 *
 * Run from the repo root on jhm-spark:
 *   node check_new_subjects_quality.js
 *
 * Exit code 0  -> all pilots pass, safe to launch Phase 3 full batch
 * Exit code 1  -> at least one check failed, DO NOT launch full batch
 *
 * Checks per pilot:
 *   1. No stub lessons (overview >= 50 chars, same threshold as check_data.js)
 *   2. FINAL_EXPLANATION.sections is non-empty
 *   3. SUMMARY_TABLE.lessons is non-empty
 *   4. Every framework[].phase is one of the five locked labels, verbatim -
 *      catches numbered-prefix contract violations (e.g. "1 - PREDICT (10 min)")
 *   5. META.schemaVersion is present (known past gap - see SCHEMA.md)
 */

const path = require('path');

const PILOTS = [
  { name: 'gensci_1_3',   label: 'General Science 1.3 Nutrition in Animals' },
  { name: 'coremath_2_2', label: 'Core Mathematics 2.2 Reflection and Congruence' },
  { name: 'essmath_2_8',  label: 'Essential Mathematics 2.8 Commercial Arithmetic 1' },
];

const LOCKED_PHASES = [
  'Predict Phase',
  'Observe Phase',
  'Explain Phase',
  'Driving Question Board Creation',
  'Model Building Phase',
];

const DATA_DIR = path.join(__dirname, 'generators', 'data');

let anyFailure = false;

for (const pilot of PILOTS) {
  const modPath = path.join(DATA_DIR, `${pilot.name}_data.js`);
  console.log(`\n--- ${pilot.label}  (${pilot.name}_data.js) ---`);

  let mod;
  try {
    delete require.cache[require.resolve(modPath)];
    mod = require(modPath);
  } catch (e) {
    console.log(`  FAIL  could not load data file: ${e.message}`);
    anyFailure = true;
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

  // 5. schemaVersion
  if (!mod.META || !mod.META.schemaVersion) {
    console.log('  FAIL  META.schemaVersion missing (see SCHEMA.md known gap)');
    ok = false;
  } else {
    console.log(`  ok    schemaVersion = ${mod.META.schemaVersion}`);
  }

  if (!ok) anyFailure = true;
  console.log(`  ${ok ? 'PASS' : 'FAIL'} overall for ${pilot.name}`);
}

console.log('\n' + '='.repeat(60));
if (anyFailure) {
  console.log('RESULT: FAIL - at least one pilot has issues.');
  console.log('Do NOT launch the Phase 3 full batch. Fix the pilot(s) above,');
  console.log('regenerate, and re-run this check before proceeding.');
  process.exit(1);
} else {
  console.log('RESULT: PASS - all three pilots are clean.');
  console.log('Safe to launch Phase 3 full batch generation now.');
  process.exit(0);
}
