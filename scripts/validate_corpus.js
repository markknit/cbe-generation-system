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
 *       strings, with silent fallbacks)
 *   5. lesson.number matches its array position sequence
 *   6. META.subject === UNIT.subject; FINAL_EXPLANATION / SUMMARY_TABLE present
 *   7. no stub lessons (overview suspiciously short)
 *
 * Usage:
 *   node scripts/validate_corpus.js            # all files
 *   node scripts/validate_corpus.js gensci_    # only files matching a prefix
 *
 * Exit 0 = clean, 1 = at least one ERROR. Warnings never fail the run.
 */
'use strict';
const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(__dirname, '..', 'generators', 'data');
const filter = process.argv[2] || '';

const SLO_KEYS = ['purpose', 'knowledge', 'skills', 'attitudes',
                  'keyInquiry', 'purposeInStoryline', 'safetyNotes'];
const TOP_KEYS = ['number', 'title', 'duration', 'substrand', 'slo', 'overview',
                  'framework', 'teacherReflection', 'summaryTablePrompt'];
const STP_KEYS = ['observed', 'learned', 'explained'];
const PHASES   = ['Predict Phase', 'Observe Phase', 'Explain Phase',
                  'Driving Question Board (DQB) Creation', 'Model Building Phase'];
const CELL_KEYS = ['learnerExperience', 'teacherMoves',
                   'sensemakingStrategy', 'formativeAssessment'];
const STUB_OVERVIEW_CHARS = 50;

const nonEmpty = v => typeof v === 'string' && v.trim().length > 0;

function checkLesson(l, i, errors, warnings, where) {
  const at = `L${l && l.number !== undefined ? l.number : `@${i}`}`;
  const err = m => errors.push(`${where} ${at}: ${m}`);
  const warn = m => warnings.push(`${where} ${at}: ${m}`);

  if (typeof l !== 'object' || l === null) { err('lesson is not an object'); return; }

  for (const k of TOP_KEYS) if (!(k in l)) err(`missing top-level "${k}"`);
  for (const k of ['title', 'duration', 'substrand', 'overview', 'teacherReflection']) {
    if (k in l && !nonEmpty(l[k])) err(`"${k}" is empty`);
  }
  if (nonEmpty(l.overview) && l.overview.trim().length < STUB_OVERVIEW_CHARS) {
    err(`stub lesson — overview only ${l.overview.trim().length} chars`);
  }
  if (!nonEmpty(l.aresKeywords)) warn('aresKeywords missing or empty (no ARES resource lookup)');

  const slo = l.slo;
  if (typeof slo !== 'object' || slo === null) {
    err('"slo" is not an object');
  } else {
    for (const k of SLO_KEYS) {
      if (!(k in slo)) err(`slo missing "${k}"`);
      else if (!nonEmpty(slo[k])) err(`slo."${k}" is empty`);
    }
    for (const k of Object.keys(slo)) {
      if (!SLO_KEYS.includes(k)) {
        err(`slo has unexpected key "${k}"`
          + (/^safety\d+otes$/.test(k)
              ? ' — placeholder-replacement corruption of "safetyNotes"'
                + ' (see scripts/repair_stubs.py LESSON_SCHEMA)' : ''));
      }
    }
  }

  const stp = l.summaryTablePrompt;
  if (typeof stp !== 'object' || stp === null) {
    err('"summaryTablePrompt" is not an object');
  } else {
    for (const k of STP_KEYS) {
      if (!(k in stp)) err(`summaryTablePrompt missing "${k}" — Summary Table cell renders blank`);
      else if (!nonEmpty(stp[k])) err(`summaryTablePrompt."${k}" is empty`);
    }
    for (const k of Object.keys(stp)) {
      if (!STP_KEYS.includes(k)) err(`summaryTablePrompt has unexpected key "${k}"`);
    }
  }

  const fw = l.framework;
  if (!Array.isArray(fw)) {
    err('"framework" is not an array');
  } else if (fw.length !== PHASES.length) {
    err(`framework has ${fw.length} entries, expected ${PHASES.length}`);
  } else {
    fw.forEach((p, j) => {
      if (typeof p !== 'object' || p === null) { err(`framework[${j}] is not an object`); return; }
      if (p.phase !== PHASES[j]) {
        err(`framework[${j}].phase is ${JSON.stringify(p.phase)}, expected `
          + `${JSON.stringify(PHASES[j])} — wrong ARES resource bucket + default grey shading`);
      }
      for (const k of CELL_KEYS) {
        if (!nonEmpty(p[k])) err(`framework[${j}]."${k}" is missing or empty`);
      }
    });
  }
}

function checkFile(file) {
  const errors = [], warnings = [];
  const name = file.replace(/_data\.js$/, '');
  let mod;
  try {
    mod = require(path.join(DATA_DIR, file));
  } catch (e) {
    return { name, errors: [`${name}: failed to load — ${e.message}`], warnings, lessons: 0 };
  }

  if (!Array.isArray(mod.LESSONS) || mod.LESSONS.length === 0) {
    errors.push(`${name}: LESSONS missing or empty`);
    return { name, errors, warnings, lessons: 0 };
  }
  if (!mod.FINAL_EXPLANATION) errors.push(`${name}: FINAL_EXPLANATION is null/missing`);
  if (!mod.SUMMARY_TABLE)     errors.push(`${name}: SUMMARY_TABLE is null/missing`);

  const ms = mod.META && mod.META.subject, us = mod.UNIT && mod.UNIT.subject;
  if (ms && us && ms !== us) {
    errors.push(`${name}: META.subject (${ms}) !== UNIT.subject (${us}) `
              + '— UNIT.subject feeds the "Subject:" row in the Lesson Sequence docx');
  }
  if (!mod.META || !nonEmpty(mod.META.outputDir)) {
    warnings.push(`${name}: META.outputDir missing`);
  }

  mod.LESSONS.forEach((l, i) => checkLesson(l, i, errors, warnings, name));

  const nums = mod.LESSONS.map(l => l && l.number);
  const expected = nums.map((_, i) => i + 1);
  if (JSON.stringify(nums) !== JSON.stringify(expected)) {
    errors.push(`${name}: lesson numbers are [${nums}], expected [${expected}]`);
  }
  return { name, errors, warnings, lessons: mod.LESSONS.length };
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
