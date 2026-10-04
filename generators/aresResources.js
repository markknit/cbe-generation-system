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

const { execFileSync } = require('child_process');
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
function getPhaseResources({ substrand, topic, subject = '', phase = 'observe', title = '' }) {
  const out = _callPython([
    '--title',     title,
    '--db',        DB_PATH,
    '--substrand', substrand,
    '--topic',     topic,
    '--subject',   subject,
    '--phase',     phase,
  ]);
  delete out._diagnostics;
  return out;
}

/**
 * Fetch all 5 phases at once (one subprocess call — more efficient).
 * Returns { predict, observe, explain, dqb, model }
 */
function getAllPhaseResources({ substrand, topic, subject = '', title = '' }) {
  const out = _callPython([
    '--db',        DB_PATH,
    '--substrand', substrand,
    '--topic',     topic,
    '--title',     title,
    '--subject',   subject,
    '--all-phases',
  ]);
  // Match diagnostics never enter the contract JSON; they are collected here
  // and written to logs/link_matching/<filePrefix>.json by build_docs.run().
  const diag = out._diagnostics;
  delete out._diagnostics;
  _DIAGNOSTICS.push({ title, substrand, subject, ...diag });
  // How the independent judge rated each pick (fits / partial / unjudged). Attached
  // NON-enumerable so it reaches the docx label but never the strict contract JSON.
  for (const ph of Object.keys(out)) {
    for (const k of ['video', 'reading']) {
      const r = out[ph] && out[ph][k];
      const slot = diag && diag.slots && diag.slots[`${ph}.${k}`];
      if (r && slot && slot.fit) Object.defineProperty(r, '_fit', { value: slot.fit, enumerable: false });
    }
  }
  return out;
}

// Shown under a link the independent judge rated 'partial' (right area, not the exact topic).
const RELATED_NOTE = 'Related topic: not an exact match for this lesson.';
const _DIAGNOSTICS = [];
/** Return and clear the diagnostics collected since the last call. */
function takeDiagnostics() {
  return _DIAGNOSTICS.splice(0, _DIAGNOSTICS.length);
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
    if (v._fit && v._fit !== 'fits') paras.push(_italicPara(RELATED_NOTE));
    if (v.source) paras.push(_metaPara(`Source: ${v.source}`));
    paras.push(_searchLinkPara('🔍 Search ARES for similar videos', v.search_url));
  } else {
    paras.push(..._noMatchParas('video', fallback));
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
    if (r._fit && r._fit !== 'fits') paras.push(_italicPara(RELATED_NOTE));
    if (r.source) paras.push(_metaPara(`Source: ${r.source}`));
    paras.push(_searchLinkPara('🔍 Search ARES for similar readings', r.search_url));
  } else {
    paras.push(..._noMatchParas('reading', fallback));
  }

  return paras;
}

/**
 * "No confident match" block. Says so plainly rather than showing a weak link
 * as if it were a good one, and prints the search terms visibly (printed
 * copies lose hyperlinks; the full search URL is ~600 characters, so the terms
 * are what a teacher can actually type into ARES search).
 */
function _noMatchParas(kind, fallback) {
  const terms = _searchTermsFromUrl(fallback);
  const paras = [_italicPara(`No closely matching ${kind} in the ARES library for this activity.`)];
  paras.push(_searchLinkPara(`🔍 Search ARES for ${kind}s`, fallback));
  if (terms) paras.push(_metaPara(`Search terms: ${terms}`));
  return paras;
}

function _searchTermsFromUrl(url) {
  const m = /[?&]searchstring=([^&]*)/.exec(url || '');
  return m ? decodeURIComponent(m[1].replace(/\+/g, ' ')) : '';
}

/** Italic grey note line */
function _italicPara(text) {
  return new Paragraph({
    spacing: { before: 0, after: 20 },
    children: [new TextRun({ text, italics: true, size: 16, font: 'Arial', color: META_COLOUR })],
  });
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

// Fails loudly. This used to swallow every error and return empty resources
// with fallback_search_url '' — which rendered as blank Resource cells and
// violates the partner contract (fallback_search_url must be a URL). A failed
// lookup must stop the render, not ship silently empty links.
function _callPython(argsList) {
  let raw;
  try {
    raw = execFileSync(PYTHON, [RECOMMENDER_SCRIPT, ...argsList.map(String)],
                       { timeout: TIMEOUT_MS, encoding: 'utf8' });
  } catch (err) {
    throw new Error(`[aresResources] recommender failed: ${(err.stderr || err.message || '').toString().trim()}`);
  }
  return JSON.parse(raw.trim());
}

// ---------------------------------------------------------------------------
// Exports
// ---------------------------------------------------------------------------

module.exports = { getPhaseResources, getAllPhaseResources, buildResourceParagraphs, takeDiagnostics, DB_PATH };

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
