/**
 * aresResources.js — ARES Resource Recommendation Bridge
 * ========================================================
 * Called from lesson plan generator scripts to get resource recommendations
 * for each lesson phase.  Spawns the Python recommender as a subprocess and
 * returns structured JSON.
 *
 * Usage:
 *   const { getPhaseResources, buildResourceParagraphs } = require('./aresResources');
 *
 *   // In your phase table cell:
 *   const res = getPhaseResources({
 *     substrand: "Cell Structure and Specialisation",
 *     topic:     "organelles electron microscope",
 *     subject:   "Biology",
 *     phase:     "observe",
 *   });
 *   const paragraphs = buildResourceParagraphs(res);
 *   // paragraphs is an array of docx Paragraph objects ready for TableCell children
 *
 * Requirements:
 *   - Python 3 available as `python3`
 *   - ares_recommender.py at RECOMMENDER_SCRIPT path (see constant below)
 *   - ares_content.db at DB_PATH (see constant below, or pass via env var)
 */

'use strict';

const { execSync }  = require('child_process');
const path          = require('path');
const {
  Paragraph, TextRun, AlignmentType,
} = require('docx');

// ---------------------------------------------------------------------------
// Config — adjust these paths for the jhm-spark environment
// ---------------------------------------------------------------------------

const PROJECT_ROOT     = process.env.CBE_PROJECT_ROOT
                         || '/home/markk/ares/cbe-generation-system';
const DB_PATH          = process.env.ARES_DB_PATH
                         || path.join(PROJECT_ROOT, 'data/ares_index/ares_content.db');
const RECOMMENDER_SCRIPT = process.env.ARES_RECOMMENDER_SCRIPT
                         || path.join(PROJECT_ROOT, 'src/ares_recommender.py');
const PYTHON           = process.env.PYTHON_BIN || 'python3';
const TIMEOUT_MS       = 15_000;   // 15 s — DB queries should be fast

// ---------------------------------------------------------------------------
// Fallback content when DB is unavailable
// ---------------------------------------------------------------------------

const FALLBACK = {
  video:   null,
  reading: null,
};

function _fallbackParagraphs(phase) {
  return [
    _makeParagraph('📹 VIDEO:', true),
    _makeParagraph(`ARES: Search "${phase}" in Khan Academy or KICD Educhannel`),
    _makeParagraph(''),
    _makeParagraph('📖 READING:', true),
    _makeParagraph('ARES: Search CK-12 or Wikipedia for this topic'),
  ];
}

// ---------------------------------------------------------------------------
// Core API
// ---------------------------------------------------------------------------

/**
 * Fetch video + reading recommendations for ONE phase.
 *
 * @param {object} opts
 * @param {string} opts.substrand  - e.g. "Cell Structure and Specialisation"
 * @param {string} opts.topic      - e.g. "organelles electron microscope"
 * @param {string} [opts.subject]  - e.g. "Biology"
 * @param {string} [opts.phase]    - predict | observe | explain | dqb | model | final
 * @returns {{ video: object|null, reading: object|null }}
 */
function getPhaseResources({ substrand, topic, subject = '', phase = 'observe' }) {
  try {
    const args = [
      RECOMMENDER_SCRIPT,
      '--db',        _shellEscape(DB_PATH),
      '--substrand', _shellEscape(substrand),
      '--topic',     _shellEscape(topic),
      '--subject',   _shellEscape(subject),
      '--phase',     phase,
      '--json',
    ].join(' ');

    const raw = execSync(`${PYTHON} ${args}`, {
      timeout: TIMEOUT_MS,
      encoding: 'utf8',
    });

    return JSON.parse(raw.trim());
  } catch (err) {
    // Silently degrade — lesson generation must not be blocked by ARES errors
    if (process.env.ARES_DEBUG) {
      console.error(`[aresResources] Warning: ${err.message}`);
    }
    return FALLBACK;
  }
}

/**
 * Fetch recommendations for ALL 5 phases in one subprocess call.
 * More efficient than calling getPhaseResources() 5 times.
 *
 * @returns {{ predict, observe, explain, dqb, model }}
 *   Each value is { video: object|null, reading: object|null }
 */
function getAllPhaseResources({ substrand, topic, subject = '' }) {
  try {
    const args = [
      RECOMMENDER_SCRIPT,
      '--db',         _shellEscape(DB_PATH),
      '--substrand',  _shellEscape(substrand),
      '--topic',      _shellEscape(topic),
      '--subject',    _shellEscape(subject),
      '--all-phases',
      '--json',
    ].join(' ');

    const raw = execSync(`${PYTHON} ${args}`, {
      timeout: TIMEOUT_MS * 3,
      encoding: 'utf8',
    });

    return JSON.parse(raw.trim());
  } catch (err) {
    if (process.env.ARES_DEBUG) {
      console.error(`[aresResources] Warning (all-phases): ${err.message}`);
    }
    return {
      predict: FALLBACK, observe: FALLBACK,
      explain: FALLBACK, dqb:     FALLBACK, model: FALLBACK,
    };
  }
}

// ---------------------------------------------------------------------------
// docx paragraph builder
// ---------------------------------------------------------------------------

/**
 * Convert a { video, reading } recommendation object into an array of
 * docx Paragraph objects suitable for a TableCell's `children` array.
 *
 * @param {{ video: object|null, reading: object|null }} resources
 * @param {string} [phase]  - used for fallback text only
 * @returns {Paragraph[]}
 */
function buildResourceParagraphs(resources, phase = '') {
  if (!resources || (!resources.video && !resources.reading)) {
    return _fallbackParagraphs(phase);
  }

  const paras = [];

  // ---- Video block ----
  if (resources.video) {
    const v = resources.video;
    paras.push(_makeParagraph(`📹 VIDEO: ${v.title}`, false, true));
    if (v.source) {
      paras.push(_makeParagraph(`   Source: ${v.source}`));
    }
    paras.push(_makeParagraph(`   ARES search: "${v.search_terms}"`));
  } else {
    paras.push(_makeParagraph('📹 VIDEO: Search Khan Academy or KICD Educhannel on ARES.', false, true));
  }

  // Spacer
  paras.push(_makeParagraph(''));

  // ---- Reading block ----
  if (resources.reading) {
    const r = resources.reading;
    paras.push(_makeParagraph(`📖 READING: ${r.title}`, false, true));
    if (r.source) {
      paras.push(_makeParagraph(`   Source: ${r.source}`));
    }
    paras.push(_makeParagraph(`   ARES search: "${r.search_terms}"`));
  } else {
    paras.push(_makeParagraph('📖 READING: Search CK-12 or Wikipedia on ARES.', false, true));
  }

  return paras;
}

// ---------------------------------------------------------------------------
// Internal helpers
// ---------------------------------------------------------------------------

function _makeParagraph(text, bold = false, label = false) {
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { before: 0, after: label ? 20 : 0 },
    children: [
      new TextRun({
        text,
        bold,
        size: 16,   // 8pt — small but readable in resource cells
        font: 'Arial',
      }),
    ],
  });
}

function _shellEscape(str) {
  // Wrap in single quotes and escape any embedded single quotes
  return `'${String(str).replace(/'/g, "'\\''")}'`;
}

// ---------------------------------------------------------------------------
// Exports
// ---------------------------------------------------------------------------

module.exports = {
  getPhaseResources,
  getAllPhaseResources,
  buildResourceParagraphs,
};
