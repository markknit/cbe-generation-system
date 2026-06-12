#!/usr/bin/env python3
"""
patch_json_io.py
================
Two patches:
  1. build_docs.js  — adds JSON export to run() (future generations)
  2. generate.js    — adds JSON file input support (local regeneration)

Run from project root:
    python3 scripts/patch_json_io.py
"""
import re

# ── Patch 1: build_docs.js — add JSON export ─────────────────────────────────

path1 = 'generators/lib/build_docs.js'
with open(path1) as f:
    src1 = f.read()

# Check if already patched
if '_data.json' in src1:
    print(f"SKIP: {path1} already has JSON export")
else:
    old1 = '  return files;\n}'
    new1 = '''  // 4. JSON export — canonical structured data for downstream tools
  const jsonPath = path.join(outBase, `${META.filePrefix}_data.json`);
  fs.writeFileSync(jsonPath, JSON.stringify(
    { META, UNIT, LESSONS, FINAL_EXPLANATION, SUMMARY_TABLE },
    null, 2
  ));
  files.push(jsonPath);
  console.log(`    Saved: ${jsonPath}  (${Math.round(fs.statSync(jsonPath).size / 1024)} KB)`);

  return files;
}'''

    if old1 in src1:
        src1 = src1.replace(old1, new1)
        with open(path1, 'w') as f:
            f.write(src1)
        print(f"✓ {path1} — JSON export added to run()")
    else:
        print(f"ERROR: {path1} — could not find insertion point")
        print("Last 10 lines:")
        print('\n'.join(src1.split('\n')[-10:]))


# ── Patch 2: generate.js — add JSON input support ────────────────────────────

path2 = 'generators/generate.js'
with open(path2) as f:
    src2 = f.read()

# Check if already patched
if 'endsWith' in src2 and 'JSON.parse' in src2:
    print(f"SKIP: {path2} already has JSON input support")
else:
    old2 = '''async function generateOne(dataDir, name) {
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
  }'''

    new2 = '''async function generateOne(dataDir, name) {
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
  }'''

    if old2 in src2:
        src2 = src2.replace(old2, new2)
        with open(path2, 'w') as f:
            f.write(src2)
        print(f"✓ {path2} — JSON input support added")
    else:
        print(f"ERROR: {path2} — could not find target block")

print("\nAll patches applied.")
print("\nUsage after patching:")
print("  # Export JSON for all existing Biology sub-strands:")
print("  node scripts/export_json.js")
print("")
print("  # Future generations automatically produce JSON:")
print("  node generators/generate.js bio_1_4")
print("")
print("  # Regenerate from an edited JSON file (no AI needed):")
print('  node generators/generate.js "data/outputs/docx/Grade 10 Biology/Bio 1.4/Biology_Chemicals_of_Life_data.json"')
