'use strict';
/**
 * lesson_contract.js — the per-lesson contract, in ONE place.
 *
 * Used by scripts/validate_corpus.js (after the fact, every data file) and
 * scripts/patch_lesson.js (before writing one lesson). Each used to carry its
 * own copy of these lists; a contract change applied to only one copy would
 * have made the two gates silently disagree (2026-10-26).
 *
 * Every rule here exists because a missing/misnamed field renders as a
 * SILENTLY EMPTY docx cell or a wrong ARES bucket: sections.js and
 * build_docs.js read these fields with `undefined`/`|| ''` fallbacks.
 *
 * Not covered here (other copies of the same facts, different languages or
 * jobs): the phase-label enum in src/generate_substrand.py's tool schema, the
 * prompt schema in scripts/repair_stubs.py, phase shading in sections.js /
 * docx_kit.js, and the partner's ares-contract.schema.json.
 */

const SLO_KEYS  = ['purpose', 'knowledge', 'skills', 'attitudes',
                   'keyInquiry', 'purposeInStoryline', 'safetyNotes'];
const TOP_KEYS  = ['number', 'title', 'duration', 'substrand', 'slo', 'overview',
                   'framework', 'teacherReflection', 'summaryTablePrompt'];
const TEXT_KEYS = ['title', 'duration', 'substrand', 'overview', 'teacherReflection'];
const STP_KEYS  = ['observed', 'learned', 'explained'];
const PHASES    = ['Predict Phase', 'Observe Phase', 'Explain Phase',
                   'Driving Question Board (DQB) Creation', 'Model Building Phase'];
const CELL_KEYS = ['learnerExperience', 'teacherMoves',
                   'sensemakingStrategy', 'formativeAssessment'];
const STUB_OVERVIEW_CHARS = 50;

const nonEmpty = v => typeof v === 'string' && v.trim().length > 0;

/** Contract errors for one lesson object, as message strings ([] = valid). */
function checkLesson(l) {
  const errs = [];
  if (typeof l !== 'object' || l === null) return ['lesson is not an object'];

  for (const k of TOP_KEYS) if (!(k in l)) errs.push(`missing top-level "${k}"`);
  for (const k of TEXT_KEYS) {
    if (k in l && !nonEmpty(l[k])) errs.push(`"${k}" is empty`);
  }
  // Stub check is shared so patch_lesson.js --force can't write a stub either.
  if (nonEmpty(l.overview) && l.overview.trim().length < STUB_OVERVIEW_CHARS) {
    errs.push(`stub lesson — overview only ${l.overview.trim().length} chars`);
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
              ? ' — placeholder-replacement corruption of "safetyNotes"'
                + ' (see scripts/repair_stubs.py LESSON_SCHEMA)' : ''));
      }
    }
  }

  // summaryTablePrompt: all three cells required and non-empty.
  const stp = l.summaryTablePrompt;
  if (typeof stp !== 'object' || stp === null) {
    errs.push('"summaryTablePrompt" is not an object');
  } else {
    for (const k of STP_KEYS) {
      if (!(k in stp)) errs.push(`summaryTablePrompt missing "${k}" — Summary Table cell renders blank`);
      else if (!nonEmpty(stp[k])) errs.push(`summaryTablePrompt."${k}" is empty`);
    }
    for (const k of Object.keys(stp)) {
      if (!STP_KEYS.includes(k)) errs.push(`summaryTablePrompt has unexpected key "${k}"`);
    }
  }

  // framework: exactly the 5 canonical phases, in order. sections.js keys ARES
  // resource-category matching and row shading off these exact strings.
  const fw = l.framework;
  if (!Array.isArray(fw)) {
    errs.push('"framework" is not an array');
  } else if (fw.length !== PHASES.length) {
    errs.push(`framework has ${fw.length} entries, expected ${PHASES.length}`);
  } else {
    fw.forEach((p, j) => {
      if (typeof p !== 'object' || p === null) { errs.push(`framework[${j}] is not an object`); return; }
      if (p.phase !== PHASES[j]) {
        errs.push(`framework[${j}].phase is ${JSON.stringify(p.phase)}, expected `
          + `${JSON.stringify(PHASES[j])} — wrong ARES resource bucket + default grey shading`);
      }
      for (const k of CELL_KEYS) {
        if (!nonEmpty(p[k])) errs.push(`framework[${j}]."${k}" is missing or empty`);
      }
    });
  }
  return errs;
}

module.exports = { SLO_KEYS, TOP_KEYS, TEXT_KEYS, STP_KEYS, PHASES, CELL_KEYS,
                   STUB_OVERVIEW_CHARS,
                   nonEmpty, checkLesson };
