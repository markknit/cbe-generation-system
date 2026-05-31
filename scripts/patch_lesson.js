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

module.exports = { META, UNIT, LESSONS, FINAL_EXPLANATION, SUMMARY_TABLE };
`;

fs.writeFileSync(dataPath, output, 'utf8');
console.log(`✓ ${outName} lesson ${lessonNum} patched (${lessonData.title || 'ok'})`);
