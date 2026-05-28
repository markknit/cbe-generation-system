/**
 * aresResources.js — ARES Resource Recommendation Bridge
 * ========================================================
 * Calls ares_recommender.py and converts results into docx Paragraph arrays
 * for the Section C Resource column.
 *
 * Each Resource cell contains:
 *   📹 VIDEO: <title as embedded hyperlink>
 *      Source: <source name>
 *      Search: <full Kolibri search URL as plain text>  ← for offline fallback
 *      Search terms: "<terms>"
 *
 *   📖 HTML/PDF: <title as embedded hyperlink>
 *      Source: <source name>
 *      Search: <full Kolibri search URL as plain text>
 *      Search terms: "<terms>"
 *
 * Requires: docx v9.x  (ExternalHyperlink support)
 */

'use strict';

const { execSync } = require('child_process');
const path         = require('path');
const {
  Paragraph, TextRun, ExternalHyperlink, AlignmentType,
} = require('docx');

// ---------------------------------------------------------------------------
// Config
// ---------------------------------------------------------------------------

const PROJECT_ROOT       = process.env.CBE_PROJECT_ROOT
                           || '/home/markk/ares/cbe-generation-system';
const DB_PATH            = process.env.ARES_DB_PATH
                           || path.join(PROJECT_ROOT, 'data/ares_index/ares_content.db');
const RECOMMENDER_SCRIPT = process.env.ARES_RECOMMENDER_SCRIPT
                           || path.join(PROJECT_ROOT, 'src/ares_recommender.py');
const PYTHON             = process.env.PYTHON_BIN || 'python3';
const TIMEOUT_MS         = 20_000;

// ---------------------------------------------------------------------------
// Colour constants (match generator palette)
// ---------------------------------------------------------------------------
const LINK_COLOUR  = "2E75B6";   // medium blue — matches column header colour
const LABEL_COLOUR = "1F3864";   // dark blue
const META_COLOUR  = "595959";   // dark grey for source/search lines

// ---------------------------------------------------------------------------
// Core API
// ---------------------------------------------------------------------------

/**
 * Fetch video + reading for ONE phase.
 */
function getPhaseResources({ substrand, topic, subject = '', phase = 'observe' }) {
  return _callPython([
    '--db',        DB_PATH,
    '--substrand', substrand,
    '--topic',     topic,
    '--subject',   subject,
    '--phase',     phase,
  ]);
}

/**
 * Fetch all 5 phases at once (one subprocess call — more efficient).
 * Returns { predict, observe, explain, dqb, model }
 */
function getAllPhaseResources({ substrand, topic, subject = '' }) {
  return _callPython([
    '--db',        DB_PATH,
    '--substrand', substrand,
    '--topic',     topic,
    '--subject',   subject,
    '--all-phases',
  ], /* allPhases= */ true);
}

// ---------------------------------------------------------------------------
// docx paragraph builder
// ---------------------------------------------------------------------------

/**
 * Build Resource cell paragraphs from a { video, reading, fallback_search_url }
 * object returned by the recommender.
 *
 * @param {object} resources  - structured recommendation object
 * @param {string} [phase]    - used in fallback text only
 * @returns {Paragraph[]}
 */
function buildResourceParagraphs(resources, phase = '') {
  const fallback = (resources && resources.fallback_search_url) || '';
  const paras    = [];

  // ── VIDEO block ──────────────────────────────────────────────────────────
  const v = resources && resources.video;
  paras.push(_labelPara('📹 VIDEO:'));
  if (v) {
    const vUrl = v.direct_url || v.exact_search_url || fallback;
    paras.push(_linkPara(v.title, vUrl));
    if (v.source) paras.push(_metaPara(`Source: ${v.source}`));
    paras.push(_searchLinkPara('🔍 Search ARES for similar videos', v.search_url));
  } else {
    paras.push(_searchLinkPara('🔍 Search ARES for videos', fallback));
  }

  // Spacer
  paras.push(_spacerPara());

  // ── READING block ─────────────────────────────────────────────────────────
  const r = resources && resources.reading;
  const readingLabel = r ? `📖 ${(r.content_type || 'READING').toUpperCase()}:` : '📖 READING:';
  paras.push(_labelPara(readingLabel));
  if (r) {
    const rUrl = r.direct_url || r.exact_search_url || fallback;
    paras.push(_linkPara(r.title, rUrl));
    if (r.source) paras.push(_metaPara(`Source: ${r.source}`));
    paras.push(_searchLinkPara('🔍 Search ARES for similar readings', r.search_url));
  } else {
    paras.push(_searchLinkPara('🔍 Search ARES for readings', fallback));
  }

  return paras;
}

// ---------------------------------------------------------------------------
// Paragraph helpers
// ---------------------------------------------------------------------------

/** Bold coloured label line: "📹 VIDEO:" */
function _labelPara(text) {
  return new Paragraph({
    spacing: { before: 0, after: 20 },
    children: [new TextRun({
      text, bold: true, size: 16, font: 'Arial', color: LABEL_COLOUR,
    })],
  });
}

/** Title as an embedded blue hyperlink */
function _linkPara(title, url) {
  return new Paragraph({
    spacing: { before: 0, after: 20 },
    children: [
      new ExternalHyperlink({
        link: url,
        children: [new TextRun({
          text: title,
          size: 16,
          font: 'Arial',
          color: LINK_COLOUR,
          underline: { type: 'single', color: LINK_COLOUR },
        })],
      }),
    ],
  });
}

/** Plain (non-linked) title line */
function _plainPara(text) {
  return new Paragraph({
    spacing: { before: 0, after: 20 },
    children: [new TextRun({ text, size: 16, font: 'Arial' })],
  });
}

/** Small grey metadata line (Source, Search URL, search terms) */
function _metaPara(text) {
  return new Paragraph({
    spacing: { before: 0, after: 10 },
    indent: { left: 120 },
    children: [new TextRun({
      text, size: 14, font: 'Arial', color: META_COLOUR,
    })],
  });
}

/** Empty spacer between video and reading blocks */
function _spacerPara() {
  return new Paragraph({
    spacing: { before: 0, after: 40 },
    children: [new TextRun({ text: '', size: 14 })],
  });
}

/** Short labelled hyperlink for search URLs */
function _searchLinkPara(label, url) {
  return new Paragraph({
    spacing: { before: 0, after: 10 },
    indent: { left: 120 },
    children: [
      new ExternalHyperlink({
        link: url,
        children: [new TextRun({
          text: label,
          size: 14,
          font: 'Arial',
          color: META_COLOUR,
          underline: { type: 'single', color: META_COLOUR },
        })],
      }),
    ],
  });
}

// ---------------------------------------------------------------------------
// Python subprocess bridge
// ---------------------------------------------------------------------------

function _callPython(argsList, allPhases = false) {
  const EMPTY_PHASE = { video: null, reading: null, fallback_search_url: '' };
  const EMPTY_ALL   = {
    predict: EMPTY_PHASE, observe: EMPTY_PHASE,
    explain: EMPTY_PHASE, dqb:     EMPTY_PHASE, model: EMPTY_PHASE,
  };

  try {
    // Build arg string — shell-escape each value
    const args = argsList.map((a, i) =>
      // Flag args (start with --) passed as-is; values shell-escaped
      a.startsWith('--') ? a : `'${String(a).replace(/'/g, "'\\''")}'`
    ).join(' ');

    const cmd = `${PYTHON} '${RECOMMENDER_SCRIPT}' ${args}`;
    const raw = execSync(cmd, { timeout: TIMEOUT_MS, encoding: 'utf8' });
    return JSON.parse(raw.trim());
  } catch (err) {
    if (process.env.ARES_DEBUG) {
      console.error(`[aresResources] ${err.message}`);
    }
    return allPhases ? EMPTY_ALL : EMPTY_PHASE;
  }
}

// ---------------------------------------------------------------------------
// Exports
// ---------------------------------------------------------------------------

module.exports = { getPhaseResources, getAllPhaseResources, buildResourceParagraphs };

// ---------------------------------------------------------------------------
// Self-test
// ---------------------------------------------------------------------------

if (require.main === module) {
  console.log('Testing ARES resource bridge...\n');
  const res = getAllPhaseResources({
    substrand: 'Cell Structure and Specialisation',
    topic:     'organelles electron microscope',
    subject:   'Biology',
  });
  for (const [phase, pair] of Object.entries(res)) {
    console.log(`\n=== ${phase.toUpperCase()} ===`);
    console.log('Video:  ', pair.video   ? `${pair.video.title} → ${pair.video.direct_url}`   : 'None');
    console.log('Reading:', pair.reading ? `${pair.reading.title} → ${pair.reading.direct_url}` : 'None');
    const paras = buildResourceParagraphs(pair, phase);
    console.log(`  → ${paras.length} paragraphs built`);
  }
}
