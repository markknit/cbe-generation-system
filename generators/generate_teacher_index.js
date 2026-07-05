'use strict';

const fs = require('fs');
const path = require('path');

// ---- Config ----
const PDF_ROOT = path.join(__dirname, '..', 'data', 'outputs', 'v2', 'PDF');
const OUTPUT_FILE = path.join(PDF_ROOT, 'index.html');

// Preferred subject display order; anything not listed falls back to
// alphabetical and is appended after these.
const SUBJECT_ORDER = ['Biology', 'Chemistry', 'Physics', 'Maths', 'English'];

// Recognised document types, in display order, with their badge colour.
// Colours match the palette already used inside the documents themselves
// (see SYSTEM_OVERVIEW.md "Colour Palette") so the index and the opened
// PDF feel like one product.
const DOC_TYPES = [
  { suffix: '_CBE_LessonSequence.pdf', label: 'Lesson Sequence', abbr: 'LP', color: '#1F3864' },
  { suffix: '_FinalExplanation.pdf', label: 'Final Explanation', abbr: 'FE', color: '#B8620A' },
  { suffix: '_SummaryTable.pdf', label: 'Summary Table', abbr: 'ST', color: '#6B3FA0' },
];

// ---- Step 1: walk PDF_ROOT and group files by Subject -> SubStrand ----
function versionCompare(a, b) {
  const pa = a.split('.').map(Number);
  const pb = b.split('.').map(Number);
  for (let i = 0; i < Math.max(pa.length, pb.length); i++) {
    const na = pa[i] || 0, nb = pb[i] || 0;
    if (na !== nb) return na - nb;
  }
  return 0;
}

function humanize(name) {
  return name.replace(/_/g, ' ').trim();
}

if (!fs.existsSync(PDF_ROOT)) {
  console.error(`PDF_ROOT not found: ${PDF_ROOT} — run generate_pdfs.js first.`);
  process.exit(1);
}

const subjects = {}; // { Biology: [ { number, name, folder, docs: [{label,abbr,color,href}] } ] }
let totalDocs = 0;

for (const subjectEntry of fs.readdirSync(PDF_ROOT, { withFileTypes: true })) {
  if (!subjectEntry.isDirectory()) continue;
  const subjectName = subjectEntry.name;
  const subjectDir = path.join(PDF_ROOT, subjectName);
  const substrands = [];

  for (const ssEntry of fs.readdirSync(subjectDir, { withFileTypes: true })) {
    if (!ssEntry.isDirectory()) continue;
    const match = ssEntry.name.match(/^SS([\d.]+)_(.+)$/);
    const number = match ? match[1] : null;
    const name = match ? humanize(match[2]) : humanize(ssEntry.name);
    const ssDir = path.join(subjectDir, ssEntry.name);

    const docs = [];
    for (const file of fs.readdirSync(ssDir)) {
      const type = DOC_TYPES.find(t => file.endsWith(t.suffix));
      if (!type) continue;
      docs.push({
        label: type.label,
        abbr: type.abbr,
        color: type.color,
        href: `${encodeURIComponent(subjectName)}/${encodeURIComponent(ssEntry.name)}/${encodeURIComponent(file)}`,
        order: DOC_TYPES.indexOf(type),
      });
      totalDocs++;
    }
    docs.sort((a, b) => a.order - b.order);
    if (docs.length > 0) substrands.push({ number: number || '—', name, docs });
  }

  substrands.sort((a, b) => versionCompare(a.number, b.number));
  if (substrands.length > 0) subjects[subjectName] = substrands;
}

const orderedSubjectNames = [
  ...SUBJECT_ORDER.filter(s => subjects[s]),
  ...Object.keys(subjects).filter(s => !SUBJECT_ORDER.includes(s)).sort(),
];

if (orderedSubjectNames.length === 0) {
  console.log('No PDF content found under v2/PDF — nothing to index.');
  process.exit(0);
}

// ---- Step 2: render HTML ----
function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

const generatedAt = new Date().toISOString().replace('T', ' ').slice(0, 16) + ' UTC';
const substrandCount = orderedSubjectNames.reduce((n, s) => n + subjects[s].length, 0);

const navHtml = orderedSubjectNames
  .map(s => `<a href="#${escapeHtml(s)}" class="navpill">${escapeHtml(s)}</a>`)
  .join('\n      ');

const sectionsHtml = orderedSubjectNames
  .map(subjectName => {
    const cards = subjects[subjectName]
      .map(ss => {
        const docLinks = ss.docs
          .map(
            d => `<a class="doclink" href="${d.href}" style="--doc-color:${d.color}">
            <span class="doc-badge">${escapeHtml(d.abbr)}</span>
            <span class="doc-label">${escapeHtml(d.label)}</span>
          </a>`
          )
          .join('\n          ');
        return `<article class="card" data-search="${escapeHtml((ss.number + ' ' + ss.name).toLowerCase())}">
          <div class="card-head">
            <span class="ss-badge">${escapeHtml(ss.number)}</span>
            <h3>${escapeHtml(ss.name)}</h3>
          </div>
          <div class="doclinks">
          ${docLinks}
          </div>
        </article>`;
      })
      .join('\n        ');
    return `<section id="${escapeHtml(subjectName)}" class="subject-section">
        <h2>${escapeHtml(subjectName)}</h2>
        <div class="card-grid">
        ${cards}
        </div>
      </section>`;
  })
  .join('\n\n      ');

const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Grade 10 CBE Lesson Plans — ARES Teacher Resource Library</title>
<style>
  :root { color-scheme: light; }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    background: #F7F6F3;
    color: #1A1A1A;
    line-height: 1.5;
  }
  a { color: inherit; }
  header.top {
    background: #1F3864;
    color: #FFFFFF;
    padding: 28px 20px 20px;
  }
  header.top h1 {
    font-family: Georgia, 'Iowan Old Style', 'Palatino Linotype', serif;
    font-weight: 400;
    font-size: 28px;
    margin: 0 0 4px;
    letter-spacing: 0.2px;
  }
  header.top .subtitle {
    color: #9FC1E0;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin: 0 0 14px;
  }
  header.top .meta {
    font-size: 12px;
    color: #B7C6DB;
  }
  .searchbar {
    position: sticky;
    top: 0;
    z-index: 5;
    background: #FFFFFF;
    border-bottom: 1px solid #E2E0D8;
    padding: 12px 20px;
  }
  .searchbar input {
    width: 100%;
    max-width: 480px;
    padding: 10px 14px;
    font-size: 15px;
    border: 1px solid #C9C6BB;
    border-radius: 20px;
    outline-offset: 2px;
  }
  .searchbar input:focus-visible {
    outline: 2px solid #2E75B6;
  }
  nav.subjectnav {
    display: flex;
    flex-wrap: wrap;
    margin-top: 10px;
  }
  .navpill {
    display: inline-block;
    padding: 6px 14px;
    margin: 0 8px 8px 0;
    background: #EFEEE9;
    border-radius: 16px;
    font-size: 13px;
    text-decoration: none;
    color: #1F3864;
  }
  .navpill:hover, .navpill:focus-visible { background: #D9EEF1; }
  main { max-width: 980px; margin: 0 auto; padding: 24px 20px 60px; }
  .subject-section { margin-bottom: 40px; scroll-margin-top: 96px; }
  .subject-section h2 {
    font-family: Georgia, 'Iowan Old Style', 'Palatino Linotype', serif;
    font-weight: 400;
    font-size: 22px;
    color: #1F3864;
    border-bottom: 2px solid #D9EEF1;
    padding-bottom: 8px;
    margin-bottom: 16px;
  }
  .card-grid {
    display: flex;
    flex-wrap: wrap;
    margin: -7px;
  }
  .card {
    flex: 1 1 260px;
    min-width: 260px;
    margin: 7px;
    background: #FFFFFF;
    border: 1px solid #E2E0D8;
    border-radius: 10px;
    padding: 14px 16px;
  }
  .card-head { display: flex; align-items: flex-start; margin-bottom: 10px; }
  .ss-badge {
    flex-shrink: 0;
    margin-right: 10px;
    background: #1F3864;
    color: #FFFFFF;
    font-size: 12px;
    font-weight: 600;
    padding: 3px 8px;
    border-radius: 6px;
    font-variant-numeric: tabular-nums;
  }
  .card-head h3 { margin: 0; font-size: 15px; font-weight: 600; line-height: 1.3; }
  .doclinks { display: flex; flex-direction: column; }
  .doclink {
    display: flex;
    align-items: center;
    margin-bottom: 6px;
    padding: 7px 8px;
    border-radius: 6px;
    text-decoration: none;
    font-size: 13px;
    border: 1px solid #E2E0D8;
  }
  .doclink:last-child { margin-bottom: 0; }
  .doclink:hover, .doclink:focus-visible { background: #F7F6F3; }
  .doc-badge {
    flex-shrink: 0;
    margin-right: 8px;
    width: 26px;
    height: 20px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 4px;
    color: #FFFFFF;
    background: var(--doc-color);
    font-size: 10px;
    font-weight: 700;
  }
  .doc-label { color: #1A1A1A; }
  .empty-state { display: none; text-align: center; color: #78756B; padding: 40px 20px; }
  footer { text-align: center; font-size: 12px; color: #9A968A; padding: 20px; }
</style>
</head>
<body>
<header class="top">
  <h1>Grade 10 CBE Lesson Plans</h1>
  <p class="subtitle">ARES Teacher Resource Library</p>
  <p class="meta">${substrandCount} sub-strands · ${totalDocs} documents · generated ${generatedAt}</p>
</header>

<div class="searchbar">
  <input type="text" id="search" placeholder="Search by subject or sub-strand name…" autocomplete="off">
  <nav class="subjectnav">
      ${navHtml}
  </nav>
</div>

<main id="main">
      ${sectionsHtml}
  <p class="empty-state" id="empty-state">No sub-strands match your search.</p>
</main>

<footer>This page is generated automatically from the current lesson plan library. Do not edit directly.</footer>

<script>
(function () {
  var input = document.getElementById('search');
  var cards = Array.prototype.slice.call(document.querySelectorAll('.card'));
  var sections = Array.prototype.slice.call(document.querySelectorAll('.subject-section'));
  var emptyState = document.getElementById('empty-state');
  if (!input) return;
  input.addEventListener('input', function () {
    var q = input.value.trim().toLowerCase();
    var anyVisible = false;
    sections.forEach(function (section) {
      var sectionHasVisible = false;
      section.querySelectorAll('.card').forEach(function (card) {
        var match = !q || card.getAttribute('data-search').indexOf(q) !== -1;
        card.style.display = match ? '' : 'none';
        if (match) { sectionHasVisible = true; anyVisible = true; }
      });
      section.style.display = sectionHasVisible ? '' : 'none';
    });
    emptyState.style.display = anyVisible ? 'none' : 'block';
  });
})();
</script>
</body>
</html>
`;

fs.writeFileSync(OUTPUT_FILE, html, 'utf8');
console.log(`Wrote ${OUTPUT_FILE}`);
console.log(`${orderedSubjectNames.length} subject(s), ${substrandCount} sub-strand(s), ${totalDocs} document(s) indexed.`);
