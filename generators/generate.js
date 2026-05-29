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
 */
'use strict';

const path = require('path');
const fs   = require('fs');
const { run } = require('./lib/build_docs');

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
}

async function generateOne(dataDir, name) {
  const dataPath = path.join(dataDir, `${name}_data.js`);
  if (!fs.existsSync(dataPath)) {
    console.error(`Data file not found: ${dataPath}`);
    process.exit(1);
  }

  let dataModule;
  try {
    dataModule = require(dataPath);
  } catch (e) {
    console.error(`Failed to load ${dataPath}: ${e.message}`);
    process.exit(1);
  }

  const { META } = dataModule;
  console.log(`Generating ${META.subject} — ${META.titleDoc}`);
  console.log(`  Output: ${META.outputDir}`);

  const start = Date.now();
  const files = await run(dataModule);
  const elapsed = ((Date.now() - start) / 1000).toFixed(1);

  console.log(`Done! ${files.length} file(s) in ${elapsed}s`);
}

main().catch(e => { console.error(e); process.exit(1); });
