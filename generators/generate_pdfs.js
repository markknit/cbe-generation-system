'use strict';

const fs = require('fs');
const path = require('path');
const os = require('os');
const { spawnSync } = require('child_process');

// ---- Config ----
const DOCX_ROOT = path.join(__dirname, '..', 'data', 'outputs', 'v2');
const PDF_DIRNAME = 'PDF';
const PDF_ROOT = path.join(DOCX_ROOT, PDF_DIRNAME);
const FILE_PATTERN = /\.docx$/i;
const BATCH_SIZE = 150;
const LO_PROFILE = path.join(os.tmpdir(), 'lo_profile_pdfgen');

function findDocxFiles(dir, matches = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (full === PDF_ROOT) continue;
    if (entry.isDirectory()) findDocxFiles(full, matches);
    else if (entry.isFile() && FILE_PATTERN.test(entry.name)) matches.push(full);
  }
  return matches;
}

if (!fs.existsSync(DOCX_ROOT)) {
  console.error(`DOCX_ROOT not found: ${DOCX_ROOT}`);
  process.exit(1);
}

const allFiles = findDocxFiles(DOCX_ROOT);
console.log(`Found ${allFiles.length} docx file(s) matching ${FILE_PATTERN}`);
if (allFiles.length === 0) {
  console.log('Nothing to convert.');
  process.exit(0);
}

const seenBase = new Map();
const collisions = [];
for (const f of allFiles) {
  const base = path.basename(f);
  if (seenBase.has(base)) collisions.push(f);
  else seenBase.set(base, f);
}
const collidingSet = new Set(collisions);
if (collisions.length) {
  console.warn(`WARNING: ${collisions.length} filename collision(s) - converting these individually:`);
  collisions.forEach(f => console.warn(`  ${f}`));
}
const batchable = allFiles.filter(f => !collidingSet.has(f));
const individual = allFiles.filter(f => collidingSet.has(f));

const failed = [];
const converted = [];

function runSoffice(files, outdir) {
  const args = [
    `-env:UserInstallation=file://${LO_PROFILE}`,
    '--headless', '--norestore',
    '--convert-to', 'pdf',
    '--outdir', outdir,
    ...files,
  ];
  const result = spawnSync('soffice', args, { stdio: 'inherit', timeout: 10 * 60 * 1000 });
  if (result.error) console.error(`soffice failed to launch: ${result.error.message}`);
  return result.status === 0;
}

function chunk(arr, size) {
  const out = [];
  for (let i = 0; i < arr.length; i += size) out.push(arr.slice(i, i + size));
  return out;
}

for (const batch of chunk(batchable, BATCH_SIZE)) {
  const tmpOut = fs.mkdtempSync(path.join(os.tmpdir(), 'pdfgen-'));
  console.log(`Converting batch of ${batch.length} file(s)...`);
  runSoffice(batch, tmpOut);
  for (const src of batch) {
    const expected = path.join(tmpOut, path.basename(src, '.docx') + '.pdf');
    if (fs.existsSync(expected)) converted.push([src, expected]);
    else failed.push(src);
  }
}

for (const src of individual) {
  const tmpOut = fs.mkdtempSync(path.join(os.tmpdir(), 'pdfgen-single-'));
  runSoffice([src], tmpOut);
  const expected = path.join(tmpOut, path.basename(src, '.docx') + '.pdf');
  if (fs.existsSync(expected)) converted.push([src, expected]);
  else failed.push(src);
}

for (const [srcDocx, tmpPdf] of converted) {
  const relative = path.relative(DOCX_ROOT, srcDocx);
  const destPdf = path.join(PDF_ROOT, relative).replace(/\.docx$/i, '.pdf');
  fs.mkdirSync(path.dirname(destPdf), { recursive: true });
  fs.renameSync(tmpPdf, destPdf);
}

console.log(`\nDone. ${converted.length} converted, ${failed.length} failed.`);
if (failed.length) {
  console.warn('Failed conversions (review manually in LibreOffice):');
  failed.forEach(f => console.warn(`  ${f}`));
}
process.exit(0);
