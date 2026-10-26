#!/usr/bin/env node
/**
 * patch_lesson.js — Replace a stub lesson in a data file
 * Usage: node scripts/patch_lesson.js <output_name> <lesson_num> <json_file> [--force]
 * Example: node scripts/patch_lesson.js bio_1_2 3 /tmp/bio_1_2_lesson3.json
 *
 * By default this refuses to overwrite a lesson that already has real content
 * (the stub-repair guard). `--force` skips ONLY that guard — it is for
 * deliberately regenerating a lesson whose content is wrong rather than absent
 * (e.g. the 2026-08-02 chem_1_2/math_2_3 phase-composition repairs).
 * `--force` never skips the contract validation below.
 */
'use strict';
const fs   = require('fs');
const path = require('path');

const ROOT      = '/home/markk/ares/cbe-generation-system';
const args      = process.argv.slice(2);
const force     = args.includes('--force');
const positional = args.filter(a => a !== '--force');
const outName   = positional[0];
const lessonNum = parseInt(positional[1]);
const jsonFile  = positional[2];

if (!outName || !lessonNum || !jsonFile) {
  console.error('Usage: node scripts/patch_lesson.js <output_name> <lesson_num> <json_file> [--force]');
  process.exit(1);
}

const dataPath = path.join(ROOT, 'generators', 'data', outName + '_data.js');

// Load new lesson content
const newLesson = JSON.parse(fs.readFileSync(jsonFile, 'utf8'));
// Handle {lesson: {...}} wrapper if present
const lessonData = newLesson.lesson || newLesson;

// ── Contract validation ───────────────────────────────────────────────────────
// The repair path sends a prompt-string schema with no enforcement, unlike
// src/generate_substrand.py which uses a strict tool schema. Two defects reached
// the corpus that way (2026-07-30 repair pass, found by a partner's checker
// 2026-08-02): 35 lessons got a `safety<N>otes` key from a stray placeholder
// replacement in repair_stubs.py, and 2 lost summaryTablePrompt.explained.
// Both render as SILENTLY EMPTY docx cells — sections.js and build_docs.js read
// these fields with `undefined`/`|| ''` fallbacks, so nothing errors.
// This gate is the chokepoint: repair_stubs.py and the manual Quick Start
// workflow both write lessons through here.

const { checkLesson } = require('../generators/lib/lesson_contract');

// The shared contract plus the one check only a single-lesson patch can make.
function validateLesson(l, expectedNum) {
  const errs = checkLesson(l);
  if (l && typeof l === 'object' && l.number !== expectedNum) {
    errs.push(`lesson.number is ${JSON.stringify(l.number)}, expected ${expectedNum}`);
  }
  return errs;
}

const errors = validateLesson(lessonData, lessonNum);
if (errors.length) {
  console.error(`✗ Refusing to patch ${outName} lesson ${lessonNum} — `
              + `${errors.length} contract violation(s) in ${jsonFile}:`);
  for (const e of errors) console.error(`    - ${e}`);
  console.error('  Nothing was written. Fix the source JSON and re-run.');
  process.exit(1);
}

// Load and eval the data module to get current LESSONS array
const mod = require(dataPath);
const lessons = mod.LESSONS;

// Find and replace the stub
const idx = lessons.findIndex(l => l.number === lessonNum);
if (idx === -1) {
  console.error(`Lesson ${lessonNum} not found in ${outName}`);
  process.exit(1);
}

const old = lessons[idx];
if (old.overview && old.overview.length > 50) {
  if (!force) {
    console.log(`Lesson ${lessonNum} already has content (${old.overview.length} chars) — skipping`);
    console.log('  (pass --force to replace it deliberately; validation still applies)');
    process.exit(0);
  }
  console.log(`--force: replacing existing lesson ${lessonNum} `
            + `(${old.overview.length} chars of overview)`);
}

lessons[idx] = lessonData;

// Serialize the modified data back to JS
const meta  = JSON.stringify(mod.META,              null, 2);
const unit  = JSON.stringify(mod.UNIT,              null, 2);
const less  = JSON.stringify(lessons,               null, 2);
const fe    = JSON.stringify(mod.FINAL_EXPLANATION, null, 2);
// The Summary Table is derived from the lessons (title + summaryTablePrompt):
// refresh this lesson's row so the repair cannot leave it describing the old
// lesson (scripts/validate_consistency.py ST-TITLE / ST-TEXT).
if (mod.SUMMARY_TABLE && Array.isArray(mod.SUMMARY_TABLE.lessons)) {
  const stp = lessonData.summaryTablePrompt || {};
  mod.SUMMARY_TABLE.lessons[idx] = {
    number: lessonData.number, title: lessonData.title,
    observed: stp.observed || '', learned: stp.learned || '', explained: stp.explained || '',
  };
}
const st    = JSON.stringify(mod.SUMMARY_TABLE,     null, 2);

const output = `'use strict';
/**
 * ${outName}_data.js
 * Patched by patch_lesson.js (lesson ${lessonNum} updated)
 */

const META = ${meta};

const UNIT = ${unit};

const LESSONS = ${less};

const FINAL_EXPLANATION = ${fe};

const SUMMARY_TABLE = ${st};
${mod.schemaVersion ? `\nconst schemaVersion = '${mod.schemaVersion}';\n` : ''}
module.exports = { ${mod.schemaVersion ? 'schemaVersion, ' : ''}META, UNIT, LESSONS, FINAL_EXPLANATION, SUMMARY_TABLE };
`;

fs.writeFileSync(dataPath, output, 'utf8');
console.log(`✓ ${outName} lesson ${lessonNum} patched (${lessonData.title || 'ok'})`);
