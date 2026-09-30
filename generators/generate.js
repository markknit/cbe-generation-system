#!/usr/bin/env node
/**
 * generate.js — Universal entry point for CBE lesson plan generation
 * ==================================================================
 * Usage:
 *   node generators/generate.js <data_module_name>
 *
 * Examples:
 *   node generators/generate.js bio_1_3           # loads generators/data/bio_1_3_data.js
 *   node generators/generate.js bio_2_1
 *   node generators/generate.js math_2_2
 *
 * The data module must export: META, UNIT, LESSONS, FINAL_EXPLANATION, SUMMARY_TABLE
 * See generators/data/bio_1_3_data.js for the schema.
 *
 * To generate all sub-strands at once:
 *   node generators/generate.js --all
 *
 * Every rendered sub-strand is gated by scripts/check_resource_links.py
 * (answer/exam material, wrong-subject matches, dead links, contract shape).
 * A hard failure makes the run exit non-zero. LINK_CHECK=warn reports
 * failures without failing the run (for diagnosis only — never for shipping).
 */
'use strict';

const path = require('path');
const fs   = require('fs');
const { run } = require('./lib/build_docs');
const { execFileSync } = require('child_process');

const ROOT = path.join(__dirname, '..');
const LINK_CHECK = path.join(ROOT, 'scripts', 'check_resource_links.py');
// The venv python carries jsonschema (full partner-contract validation).
const CHECK_PYTHON = fs.existsSync(path.join(ROOT, 'venv', 'bin', 'python3'))
  ? path.join(ROOT, 'venv', 'bin', 'python3') : 'python3';
const linkFailures = [];

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.error('Usage: node generators/generate.js <data_module_name>');
    console.error('       node generators/generate.js --all');
    process.exit(1);
  }

  const dataDir = path.join(__dirname, 'data');

  if (args[0] === '--all') {
    // Generate all data modules found in generators/data/
    const files = fs.readdirSync(dataDir)
      .filter(f => f.endsWith('_data.js'))
      .map(f => f.replace('_data.js', ''));

    console.log(`Generating ${files.length} sub-strands...`);
    for (const name of files) {
      console.log(`\n─── ${name} ───`);
      await generateOne(dataDir, name);
    }
  } else {
    await generateOne(dataDir, args[0]);
  }

  if (linkFailures.length) {
    console.error(`\nResource-link check FAILED for ${linkFailures.length} sub-strand(s): ${linkFailures.join(', ')}`);
    if (process.env.LINK_CHECK !== 'warn') process.exit(1);
    console.error('LINK_CHECK=warn set: not failing the run.');
  }
}

function checkLinks(name, jsonPath) {
  try {
    const out = execFileSync(CHECK_PYTHON, [LINK_CHECK, '--quiet', jsonPath], { encoding: 'utf8' });
    const summary = out.split('\n').find(l => l.includes('hard failures')) || '';
    console.log(`  Link check: PASS ${summary.trim()}`);
  } catch (err) {
    console.error(`  Link check: FAIL\n${(err.stdout || err.message).toString()}`);
    linkFailures.push(name);
  }
}

async function generateOne(dataDir, name) {
  // Accept either a name (loads *_data.js) or a direct path to a .json file
  let dataPath;
  let dataModule;

  if (name.endsWith('.json') && fs.existsSync(name)) {
    // Direct JSON file path supplied (e.g. from teacher editing workflow)
    dataPath = name;
    try {
      dataModule = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
      // Derive output name from filePrefix for logging
      name = (dataModule.META && dataModule.META.filePrefix) || path.basename(dataPath, '_data.json');
    } catch (e) {
      console.error(`Failed to parse JSON ${dataPath}: ${e.message}`);
      process.exit(1);
    }
  } else {
    // Standard: load *_data.js module
    dataPath = path.join(dataDir, `${name}_data.js`);
    if (!fs.existsSync(dataPath)) {
      console.error(`Data file not found: ${dataPath}`);
      process.exit(1);
    }
    try {
      dataModule = require(dataPath);
    } catch (e) {
      console.error(`Failed to load ${dataPath}: ${e.message}`);
      process.exit(1);
    }
  }

  const { META } = dataModule;
  console.log(`Generating ${META.subject} — ${META.titleDoc}`);
  console.log(`  Output: ${META.outputDir}`);

  const start = Date.now();
  const files = await run(dataModule);
  const elapsed = ((Date.now() - start) / 1000).toFixed(1);

  console.log(`Done! ${files.length} file(s) in ${elapsed}s`);
  const jsonOut = files.find(f => f.endsWith('_data.json'));
  if (jsonOut) checkLinks(name, jsonOut);
}

main().catch(e => { console.error(e); process.exit(1); });
