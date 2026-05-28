/**
 * INTEGRATION PATCH — How to wire ARES resources into an existing generator
 * =========================================================================
 * This file shows the DIFF-style changes needed in any existing generator
 * script (e.g. biology_1_3_cell_structure.js).
 *
 * Apply these changes to each generator script.  The changes are minimal:
 *   1. Require the aresResources module at the top.
 *   2. For each lesson, call getAllPhaseResources() once before building tables.
 *   3. Replace hardcoded resource text in Section C cells with
 *      buildResourceParagraphs(phaseResources[phase]).
 *
 * The rest of the generator (formatting, colours, structure) is unchanged.
 */

'use strict';

// ==========================================================================
// CHANGE 1 — Add require() near the top of the generator, after other requires
// ==========================================================================

// BEFORE (typical top of generator):
//   const { Document, Packer, ... } = require('docx');
//   const fs = require('fs');

// AFTER — add this line:
const { getAllPhaseResources, buildResourceParagraphs } = require('./aresResources');
// (adjust path if aresResources.js is in generators/ alongside the generator script)


// ==========================================================================
// CHANGE 2 — Add a lesson-level resource lookup function
// ==========================================================================

/**
 * Returns resource recommendations for all 5 phases of a lesson.
 * Call this once per lesson before building the Section C table.
 *
 * @param {object} lesson  - lesson data object from your LESSONS array
 * @param {string} substrand - sub-strand name (e.g. "Cell Structure and Specialisation")
 * @param {string} subject   - subject name  (e.g. "Biology")
 * @returns {object}  keyed by phase: { predict, observe, explain, dqb, model }
 */
function getLessonResources(lesson, substrand, subject) {
  // Compose a topic string from the lesson title and key content
  const topic = [
    lesson.title || '',
    lesson.keyContent || '',
    lesson.phenomenon || '',
  ].filter(Boolean).join(' ');

  return getAllPhaseResources({ substrand, topic, subject });
}


// ==========================================================================
// CHANGE 3 — Use resources in Section C table rows
// ==========================================================================

// BEFORE (typical Section C phase row, Resource column):
/*
new TableCell({
  ...cellStyle(colWidths[1]),
  children: [
    new Paragraph({ children: [new TextRun({ text: "MATERIAL: Science notebooks, pens\nDIGITAL: Pumpkin time-lapse video", ... })] })
  ]
})
*/

// AFTER — replace the hardcoded children array with buildResourceParagraphs():

function buildSectionCRow(phaseKey, phaseLabel, learnerExp, teacherMoves, sensemaking, assessment, phaseResources, colWidths, colors) {
  // phaseResources is the full { predict, observe, ... } object from getLessonResources()
  // phaseKey is one of: 'predict' | 'observe' | 'explain' | 'dqb' | 'model'

  const resources = phaseResources[phaseKey] || { video: null, reading: null };

  return new TableRow({
    children: [
      // Column 1: Phase label  (if using 6-column layout with label column)
      // new TableCell({ ...labelCell, children: [phaseLabel] }),

      // Column 1 (5-col layout) / Column 2 (6-col layout): Learner Experience
      new TableCell({
        // ...your existing cell style...
        children: learnerExp,   // array of Paragraphs — unchanged
      }),

      // Column 2 / 3: Resource — NOW POPULATED FROM ARES
      new TableCell({
        // ...your existing cell style...
        children: buildResourceParagraphs(resources, phaseKey),
        // ^^^ This replaces whatever was here before
      }),

      // Column 3 / 4: Teacher Moves
      new TableCell({
        // ...your existing cell style...
        children: teacherMoves,
      }),

      // Column 4 / 5: Sensemaking Strategy
      new TableCell({
        // ...your existing cell style...
        children: sensemaking,
      }),

      // Column 5 / 6: Formative Assessment
      new TableCell({
        // ...your existing cell style...
        children: assessment,
      }),
    ],
  });
}


// ==========================================================================
// CHANGE 4 — Wire into the per-lesson generation loop
// ==========================================================================

// BEFORE (typical lesson generation):
/*
function generateLesson(lesson) {
  const sectionC = buildSectionCTable(lesson);
  // ...
}
*/

// AFTER:
/*
function generateLesson(lesson, substrand, subject) {

  // Fetch ARES resources for this lesson (one DB call for all 5 phases)
  const phaseResources = getLessonResources(lesson, substrand, subject);

  const sectionC = buildSectionCTable(lesson, phaseResources);
  // pass phaseResources into buildSectionCTable, then into each row builder
}
*/


// ==========================================================================
// CHANGE 5 — Update the main generation call
// ==========================================================================

// Find the line where you call generateLesson() or equivalent and add the
// substrand and subject parameters.

// Example — in the LESSONS.forEach loop:
/*
const SUBSTRAND = "Cell Structure and Specialisation";
const SUBJECT   = "Biology";

LESSONS.forEach((lesson, i) => {
  console.log(`Generating lesson ${i + 1}: ${lesson.title} ...`);
  const lessonContent = generateLesson(lesson, SUBSTRAND, SUBJECT);
  allContent.push(...lessonContent);
});
*/


// ==========================================================================
// TESTING — Run this file directly to verify the bridge works
// ==========================================================================

if (require.main === module) {
  console.log('Testing ARES resource bridge...\n');

  const res = getAllPhaseResources({
    substrand: 'Cell Structure and Specialisation',
    topic:     'organelles electron microscope thylakoid',
    subject:   'Biology',
  });

  for (const [phase, pair] of Object.entries(res)) {
    console.log(`\n=== ${phase.toUpperCase()} ===`);
    console.log('Video:  ', pair.video   ? `${pair.video.title} (${pair.video.source})`   : 'None');
    console.log('Reading:', pair.reading ? `${pair.reading.title} (${pair.reading.source})` : 'None');

    const paras = buildResourceParagraphs(pair, phase);
    console.log(`  → ${paras.length} paragraphs built`);
  }

  console.log('\nBridge test complete.');
}
