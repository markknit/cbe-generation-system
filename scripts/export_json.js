#!/usr/bin/env node
/**
 * export_json.js — Export _data.json files for all existing sub-strands
 * ======================================================================
 * Reads each _data.js module and writes a _data.json file alongside the
 * existing .docx files in data/outputs/docx/.
 *
 * Usage:
 *   node scripts/export_json.js           # all sub-strands in generators/data/
 *   node scripts/export_json.js bio_1_4   # single sub-strand
 */
'use strict';

const fs   = require('fs');
const path = require('path');

const ROOT     = path.resolve(__dirname, '..');
const DATA_DIR = path.join(ROOT, 'generators', 'data');
const OUT_BASE = path.join(ROOT, 'data', 'outputs', 'docx');

// Determine which modules to export
const args = process.argv.slice(2);
let names;

if (args.length === 0) {
  // All _data.js files
  names = fs.readdirSync(DATA_DIR)
    .filter(f => f.endsWith('_data.js'))
    .map(f => f.replace('_data.js', ''));
} else {
  names = args;
}

console.log(`Exporting JSON for ${names.length} sub-strand(s)...\n`);

let ok = 0;
let failed = 0;

for (const name of names) {
  const dataPath = path.join(DATA_DIR, `${name}_data.js`);

  if (!fs.existsSync(dataPath)) {
    console.log(`  SKIP: ${name}_data.js not found`);
    failed++;
    continue;
  }

  try {
    // Load the data module
    const mod = require(dataPath);
    const { META, UNIT, LESSONS, FINAL_EXPLANATION, SUMMARY_TABLE } = mod;

    if (!META || !META.outputDir || !META.filePrefix) {
      console.log(`  SKIP: ${name} — missing META.outputDir or META.filePrefix`);
      failed++;
      continue;
    }

    // Resolve output directory
    const outDir = path.join(OUT_BASE, META.outputDir);

    if (!fs.existsSync(outDir)) {
      fs.mkdirSync(outDir, { recursive: true });
    }

    // Write JSON file
    const jsonPath = path.join(outDir, `${META.filePrefix}_data.json`);
    const payload  = JSON.stringify(
      { META, UNIT, LESSONS, FINAL_EXPLANATION, SUMMARY_TABLE },
      null, 2
    );

    fs.writeFileSync(jsonPath, payload, 'utf8');

    const kb = Math.round(Buffer.byteLength(payload, 'utf8') / 1024);
    console.log(`  ✓ ${name} → ${META.filePrefix}_data.json  (${kb} KB)`);
    ok++;

  } catch (e) {
    console.log(`  ERROR: ${name} — ${e.message}`);
    failed++;
  }
}

console.log(`\nDone. ${ok} exported, ${failed} skipped/failed.`);
