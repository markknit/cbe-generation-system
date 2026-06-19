'use strict';
/**
 * backfill_contract.js — bring existing *_data.js files up to ares-contract v1.0.0
 *
 * Idempotent. Run from repo root:  node scripts/backfill_contract.js
 *
 * Adds (only where missing):
 *   - top-level  schemaVersion: '1.0.0'   (all files)
 *   - UNIT.content                         (bio_1_1, bio_1_3, bio_1_4)
 *   - META.substrand_id / substrand_name   (bio_1_3)
 *
 * Edits are anchored on unique lines and matched to each block's own
 * quote style; the module is require()'d first so we only touch what's
 * actually missing.
 */
const fs = require('fs');
const path = require('path');

const SCHEMA_VERSION = '1.0.0';
const DATA_DIR = path.join(__dirname, '..', 'generators', 'data');

// Faithful sub-strand content, derived from each file's own lessons + KICD scope.
const CONTENT = {
  bio_1_1: [
    'Meaning and importance of Biology as a science',
    'Branches and fields of study in Biology (e.g. botany, zoology, microbiology, genetics, ecology)',
    'Application of Biology in everyday life: agriculture, medicine, industry, and the environment',
    'Career opportunities related to Biology and the work of Kenyan scientists',
    'Biology and technology: modern tools used to solve real-world problems',
  ],
  bio_1_3: [
    'Microscopy: comparison of the light microscope and the electron microscope (magnification and resolution)',
    'Preparation and observation of temporary slides of plant cells',
    'Cell structure: organelles and their functions as seen under the electron microscope',
    'Comparison of plant and animal cells',
    'Cell specialisation: how the structure of specialised plant and animal cells serves their function',
    'Levels of organisation: cell, tissue, organ, organ system, organism',
  ],
  bio_1_4: [
    'Biomolecules: carbohydrates, proteins, and lipids — composition, properties, and functions',
    'Food tests for detecting biomolecules in Kenyan foods (reducing sugars, starch, proteins, lipids)',
    'Enzymes: nature, properties, and factors affecting enzyme activity',
    'Water and mineral salts: their roles in living organisms',
    'Energy requirements and the energy value of food',
  ],
};

function esc(s) { return s.replace(/\\/g, '\\\\').replace(/'/g, "\\'"); }

function contentBlock(bullets) {
  const lines = bullets.map((b, i) =>
    "    '\u2022 " + esc(b) + (i < bullets.length - 1 ? "\\n' +" : "'"));
  return "  content:\n" + lines.join("\n") + ",\n";
}

let touched = 0;
const files = fs.readdirSync(DATA_DIR).filter(f => f.endsWith('_data.js')).sort();

for (const file of files) {
  const stem = file.replace(/_data\.js$/, '');
  const full = path.join(DATA_DIR, file);
  const mod = require(full);
  let src = fs.readFileSync(full, 'utf8');
  const before = src;
  const actions = [];

  // 1) schemaVersion (all files)
  if (mod.schemaVersion === undefined) {
    if (!/module\.exports\s*=\s*\{\s*schemaVersion/.test(src)) {
      src = src.replace(
        /module\.exports = \{ META,/,
        `const schemaVersion = '${SCHEMA_VERSION}';\n\nmodule.exports = { schemaVersion, META,`
      );
      actions.push('schemaVersion');
    }
  }

  // 2) UNIT.content (only the three that lack it)
  if (CONTENT[stem] && (mod.UNIT && mod.UNIT.content === undefined)) {
    const m = src.match(/^(\s*substrand:\s*'[^']*',)\s*$/m);
    if (m) {
      src = src.replace(m[0], m[0] + "\n" + contentBlock(CONTENT[stem]).replace(/\n$/, ''));
      actions.push('UNIT.content');
    } else {
      actions.push('!! could not anchor UNIT.content');
    }
  }

  // 3) META.substrand_id / substrand_name (bio_1_3)
  if (mod.META && mod.META.substrand_id === undefined) {
    // Insert before META's closing brace, matching bare-key single-quote style.
    src = src.replace(
      /(const META = \{[\s\S]*?)(\n\};)/,
      (whole, body, close) => {
        const id = mod.META.substrand_id !== undefined ? null
          : (mod.UNIT.substrand.match(/Sub-Strand\s+([\d.]+)/) || [, ''])[1];
        const name = mod.META.substrand_name !== undefined ? null
          : mod.META.titleDoc.replace(/^BIOLOGY GRADE 10:\s*/i, '')
              .toLowerCase().replace(/\b\w/g, c => c.toUpperCase())
              .replace(/\bAnd\b/g, 'and');
        const add = `  substrand_id: '${id}',\n  substrand_name: '${esc(name)}',`;
        return body + (body.trimEnd().endsWith(',') ? '\n' : ',\n') + add + close;
      }
    );
    actions.push('META.substrand_id + substrand_name');
  }

  if (src !== before) {
    fs.writeFileSync(full, src, 'utf8');
    touched++;
    console.log(`  ${file}: ${actions.join(', ')}`);
  } else {
    console.log(`  ${file}: already conformant (no change)`);
  }
}
console.log(`\nDone. ${touched} file(s) modified.`);
