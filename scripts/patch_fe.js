#!/usr/bin/env node
/**
 * patch_fe.js — Replace FINAL_EXPLANATION in a data file
 * Usage: node scripts/patch_fe.js <output_name> <json_file>
 * Example: node scripts/patch_fe.js bio_3_2 /tmp/bio_3_2_fe.json
 */
'use strict';
const fs   = require('fs');
const path = require('path');

const ROOT    = '/home/markk/ares/cbe-generation-system';
const outName = process.argv[2];
const jsonFile = process.argv[3];

if (!outName || !jsonFile) {
  console.error('Usage: node scripts/patch_fe.js <output_name> <json_file>');
  process.exit(1);
}

const dataPath = path.join(ROOT, 'generators', 'data', outName + '_data.js');

// Load new FE content
const newFE = JSON.parse(fs.readFileSync(jsonFile, 'utf8'));

// Load the data module
const mod = require(dataPath);

// Serialize everything back cleanly
const output = `'use strict';
/**
 * ${outName}_data.js
 * Patched by patch_fe.js (Final Explanation updated)
 */

const META = ${JSON.stringify(mod.META, null, 2)};

const UNIT = ${JSON.stringify(mod.UNIT, null, 2)};

const LESSONS = ${JSON.stringify(mod.LESSONS, null, 2)};

const FINAL_EXPLANATION = ${JSON.stringify(newFE, null, 2)};

const SUMMARY_TABLE = ${JSON.stringify(mod.SUMMARY_TABLE, null, 2)};

module.exports = { META, UNIT, LESSONS, FINAL_EXPLANATION, SUMMARY_TABLE };
`;

fs.writeFileSync(dataPath, output, 'utf8');
console.log(`✓ ${outName} Final Explanation patched`);
