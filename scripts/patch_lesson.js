#!/usr/bin/env node
/**
 * patch_lesson.js — Replace a stub lesson in a data file
 * Usage: node scripts/patch_lesson.js <output_name> <lesson_num> <json_file>
 * Example: node scripts/patch_lesson.js bio_1_2 3 /tmp/bio_1_2_lesson3.json
 */
'use strict';
const fs   = require('fs');
const path = require('path');

const ROOT      = '/home/markk/ares/cbe-generation-system';
const outName   = process.argv[2];
const lessonNum = parseInt(process.argv[3]);
const jsonFile  = process.argv[4];

if (!outName || !lessonNum || !jsonFile) {
  console.error('Usage: node scripts/patch_lesson.js <output_name> <lesson_num> <json_file>');
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

const SLO_KEYS = ['purpose', 'knowledge', 'skills', 'attitudes',
                  'keyInquiry', 'purposeInStoryline', 'safetyNotes'];
const TOP_KEYS  = ['number', 'title', 'duration', 'substrand', 'slo', 'overview',
                   'framework', 'teacherReflection', 'summaryTablePrompt'];
const STP_KEYS  = ['observed', 'learned', 'explained'];
const PHASES    = ['Predict Phase', 'Observe Phase', 'Explain Phase',
                   'Driving Question Board (DQB) Creation', 'Model Building Phase'];
const PHASE_KEYS = ['phase', 'learnerExperience', 'teacherMoves',
                    'sensemakingStrategy', 'formativeAssessment'];

function validateLesson(l, expectedNum) {
  const errs = [];
  const nonEmpty = v => typeof v === 'string' && v.trim().length > 0;

  for (const k of TOP_KEYS) if (!(k in l)) errs.push(`missing top-level "${k}"`);
  if (l.number !== expectedNum) {
    errs.push(`lesson.number is ${JSON.stringify(l.number)}, expected ${expectedNum}`);
  }
  for (const k of ['title', 'duration', 'substrand', 'overview', 'teacherReflection']) {
    if (k in l && !nonEmpty(l[k])) errs.push(`"${k}" is empty`);
  }

  // slo: exact key set. Catches the safety<N>otes corruption and any other
  // placeholder damage to key names.
  const slo = l.slo;
  if (typeof slo !== 'object' || slo === null) {
    errs.push('"slo" is not an object');
  } else {
    for (const k of SLO_KEYS) {
      if (!(k in slo)) errs.push(`slo missing "${k}"`);
      else if (!nonEmpty(slo[k])) errs.push(`slo."${k}" is empty`);
    }
    for (const k of Object.keys(slo)) {
      if (!SLO_KEYS.includes(k)) {
        errs.push(`slo has unexpected key "${k}"`
          + (/^safety\d+otes$/.test(k)
              ? ' — placeholder-replacement corruption of "safetyNotes"' : ''));
      }
    }
  }

  // summaryTablePrompt: all three cells required and non-empty.
  const stp = l.summaryTablePrompt;
  if (typeof stp !== 'object' || stp === null) {
    errs.push('"summaryTablePrompt" is not an object');
  } else {
    for (const k of STP_KEYS) {
      if (!(k in stp)) errs.push(`summaryTablePrompt missing "${k}"`);
      else if (!nonEmpty(stp[k])) errs.push(`summaryTablePrompt."${k}" is empty`);
    }
    for (const k of Object.keys(stp)) {
      if (!STP_KEYS.includes(k)) errs.push(`summaryTablePrompt has unexpected key "${k}"`);
    }
  }

  // framework: exactly the 5 canonical phases, in order. sections.js keys ARES
  // resource-category matching and row shading off these exact strings, both
  // with silent fallbacks — a wrong label mis-buckets resources without erroring.
  const fw = l.framework;
  if (!Array.isArray(fw)) {
    errs.push('"framework" is not an array');
  } else if (fw.length !== PHASES.length) {
    errs.push(`framework has ${fw.length} entries, expected ${PHASES.length}`);
  } else {
    fw.forEach((p, i) => {
      if (typeof p !== 'object' || p === null) {
        errs.push(`framework[${i}] is not an object`);
        return;
      }
      if (p.phase !== PHASES[i]) {
        errs.push(`framework[${i}].phase is ${JSON.stringify(p.phase)}, `
                + `expected ${JSON.stringify(PHASES[i])}`);
      }
      for (const k of PHASE_KEYS.slice(1)) {
        if (!nonEmpty(p[k])) errs.push(`framework[${i}]."${k}" is missing or empty`);
      }
    });
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
  console.log(`Lesson ${lessonNum} already has content (${old.overview.length} chars) — skipping`);
  process.exit(0);
}

lessons[idx] = lessonData;

// Serialize the modified data back to JS
const meta  = JSON.stringify(mod.META,              null, 2);
const unit  = JSON.stringify(mod.UNIT,              null, 2);
const less  = JSON.stringify(lessons,               null, 2);
const fe    = JSON.stringify(mod.FINAL_EXPLANATION, null, 2);
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
