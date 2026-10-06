#!/usr/bin/env node
/**
 * build_teacher_review_docx.js — printable teacher review handout (Grade 10 + 11)
 * Sources: TEACHER_REVIEW_LIST_2026-10-04.md (lesson items), logs/final_explanation_issues/*.json
 * (Final Explanation findings, status needs_review), META of generators/data/*_data.js, plus the
 * hand-kept GRADE11_EXTRA / TEMPLATE_PROBLEMS / SPOT_CHECK lists below.
 *   node scripts/build_teacher_review_docx.js [OUT.docx]
 */
'use strict';
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, AlignmentType,
  ShadingType, BorderStyle, HeadingLevel, Footer, PageNumber, PageBreak,
} = require('docx');

const ROOT = path.resolve(__dirname, '..');
const OUT = process.argv[2] || path.join(ROOT, 'TEACHER_REVIEW_HANDOUT_Grade10-11_2026-10-05.docx');
const FONT = 'Arial';
const W = 13680; // landscape Letter, 0.75" margins

// ---------- data ----------
const SUBJECTS = [
  ['bio', 'Biology (Grade 10)'], ['g11_bio', 'Biology (Grade 11)'], ['chem', 'Chemistry'],
  ['phys', 'Physics'], ['math', 'Mathematics'], ['coremath', 'Core Mathematics'],
  ['essmath', 'Essential Mathematics'], ['gensci', 'General Science'],
];
const subjOf = (m) => SUBJECTS.find(([p]) => m.startsWith(p + '_'))?.[0];
const subjName = (p) => SUBJECTS.find(([q]) => q === p)[1];

function metaName(mod) {
  try {
    const m = require(path.join(ROOT, 'generators/data', `${mod}_data.js`));
    return m.META.substrand_name || mod;
  } catch { return mod; }
}
const label = (mod) => {
  const m = require(path.join(ROOT, 'generators/data', `${mod}_data.js`)).META;
  return `${m.substrand_id || ''} ${m.substrand_name || ''}`.trim();
};

const TYPE_LABEL = {
  'science — needs rewrite': 'Science error: needs rewrite',
  'structural': 'Structural',
  'teaching choice': 'Teaching choice',
  'science': 'Science check',
  'science (unclassified)': 'Science check',
};
const TYPE_ORDER = ['Science error: needs rewrite', 'Science check', 'Structural', 'Teaching choice'];

// lesson items from the markdown list
function parseLessonItems() {
  const txt = fs.readFileSync(path.join(ROOT, 'TEACHER_REVIEW_LIST_2026-10-04.md'), 'utf8');
  const out = {};
  let mod = null;
  for (const ln of txt.split('\n')) {
    let m = ln.match(/^## ([a-z0-9_]+)(?: —|\s*\()/);
    if (m && !ln.startsWith('## Template')) { mod = m[1]; out[mod] = out[mod] || []; continue; }
    m = ln.match(/^- \*\*\[([^\]]+)\]\*\* (.*)$/);
    if (m && mod) {
      const rest = m[2];
      const i = rest.indexOf(' — ');
      const topic = i > 0 ? rest.slice(0, i) : rest;
      const detail = i > 0 ? rest.slice(i + 3) : '';
      out[mod].push({ type: TYPE_LABEL[m[1]] || m[1], topic, detail });
    }
  }
  return out;
}

// Grade 11 Biology items found 2026-10-05 (not in the 2026-10-04 list)
const GRADE11_EXTRA = {
  g11_bio_2_1: [
    { type: 'Science check', topic: 'Lone avocado/pawpaw "sets no fruit"', detail: 'Lessons say a lone tree cannot set fruit. Avocado is protogynous and can set some fruit alone. Decide whether to qualify the statement.' },
  ],
  g11_bio_2_3: [
    { type: 'Science check', topic: 'Guttation fluid called a "waste" route', detail: 'Guttation fluid is mainly xylem sap. The curriculum frames it as a way plants lose water/solutes. Keep the framing or add a note.' },
  ],
  g11_bio_3_1: [
    { type: 'Science error: needs rewrite', topic: 'Lesson 4: "rising progesterone and oestrogen inhibit FSH"', detail: 'Progesterone is low in the follicular phase; rising oestrogen (and inhibin) reduces FSH. The Final Explanation repeats the wording and also uses a "furthest-ahead follicle" idea that is never taught.' },
    { type: 'Science check', topic: '"Snake is ovoviviparous"; oxytocin role', detail: 'Many snakes are oviparous. Oxytocin is described only for labour; its milk-ejection role is omitted.' },
  ],
  g11_bio_1_3: [
    { type: 'Teaching choice', topic: 'Loose animal counts (Lesson 5 "eight", Lesson 6 "7", Lesson 7 an 8-card list with "tilapia or goat")', detail: 'Counts are not clearly wrong but are inconsistent in wording.' },
    { type: 'Structural', topic: 'Fungi/kingdoms and viruses', detail: 'Lesson 8 assumes learners know fungi, but no lesson teaches them. The viruses paragraph never says whether viruses are living.' },
  ],
  g11_bio_1_1: [
    { type: 'Teaching choice', topic: 'Final Explanation Part 2(b): ranks for maize', detail: 'Never names real taxonomic ranks for maize. Design nitpick.' },
  ],
};

const TEMPLATE_PROBLEMS = [
  ['bio_2_1 (Plant Nutrition)', 'The template filed here is actually the "2.2 Transport System in Plants" plan (wilting spinach). Provide the correct Plant Nutrition template.'],
  ['math_3_3 (Vectors I)', 'The template filed here is the Physics "Temperature and Thermal Expansion" plan (Okello). Provide the correct Vectors template.'],
  ['chem_2_1 (Salts)', 'Scheme-of-work template with suggested activities but no real phenomenon. Teachers please supply a phenomenon.'],
  ['math_2_2 (Area of Polygons)', 'Scheme-of-work template with suggested activities but no real phenomenon. Teachers please supply a phenomenon.'],
];

const SPOT_CHECK = [
  'Grade 10 sub-strands judged to use the same phenomenon as the teachers\' template (20, not checked by hand). Lower confidence: phys_1_3, phys_3_1, phys_4_1, phys_4_2.',
];

// Final Explanation findings
function loadFE() {
  const dir = path.join(ROOT, 'logs/final_explanation_issues');
  const out = {};
  for (const f of fs.readdirSync(dir).filter((x) => x.endsWith('.json'))) {
    const d = JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8'));
    if (d.status !== 'needs_review') continue;
    out[d.name] = (d.unresolved || []).filter((u) => (u.kind || 'final_explanation') === 'final_explanation');
  }
  return out;
}
// Grade 11: an agent triaged these 2026-10-05; only items left for a human are listed
const FE_G11_HUMAN = {
  g11_bio_1_1: ['Whole Final Explanation: 1 real fix and 2 false positives were handled 2026-10-05; read once and clear.'],
  g11_bio_1_2: ['1 real fix and 5 false positives handled 2026-10-05; read once and clear.'],
  g11_bio_1_3: ['3 false positives; read once and clear.'],
  g11_bio_1_4: ['2 real fixes and 3 false positives handled 2026-10-05; read once and clear.'],
  g11_bio_2_3: ['3 real fixes and 2 false positives handled 2026-10-05; read once and clear. Guttation "waste" framing: see lesson items.'],
  g11_bio_3_1: ['1 real fix handled. Left for you: the exemplar repeats "rising progesterone and oestrogen reduce FSH" and the untaught "furthest-ahead follicle" idea (see lesson items); "snake is ovoviviparous" and oxytocin milk ejection omitted.'],
  g11_bio_3_3: ['1 real fix and 4 false positives handled 2026-10-05; read once and clear.'],
};

// ---------- docx helpers ----------
const border = { style: BorderStyle.SINGLE, size: 4, color: '999999' };
const borders = { top: border, bottom: border, left: border, right: border };
const run = (t, o = {}) => new TextRun({ text: t, font: FONT, size: o.size || 18, bold: o.bold, italics: o.italics, color: o.color });
const P = (t, o = {}) => new Paragraph({
  spacing: { before: o.before || 0, after: o.after ?? 80 }, alignment: o.align,
  children: Array.isArray(t) ? t : [run(t, o)], keepNext: o.keepNext,
});
const H1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 240, after: 120 }, keepNext: true,
  children: [new TextRun({ text: t, font: FONT, size: 30, bold: true, color: '1F3864' })] });
const H2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 200, after: 80 }, keepNext: true,
  children: [new TextRun({ text: t, font: FONT, size: 24, bold: true, color: '2E75B6' })] });
const H3 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_3, spacing: { before: 140, after: 60 }, keepNext: true,
  children: [new TextRun({ text: t, font: FONT, size: 20, bold: true, color: '333333' })] });

function cell(content, width, o = {}) {
  const paras = (Array.isArray(content) ? content : [content]).map((c) =>
    typeof c === 'string' ? new Paragraph({ spacing: { after: 40 }, children: [run(c, o)] }) : c);
  return new TableCell({
    borders, width: { size: width, type: WidthType.DXA }, margins: { top: 50, bottom: 50, left: 80, right: 80 },
    shading: o.fill ? { fill: o.fill, type: ShadingType.CLEAR, color: 'auto' } : undefined, children: paras,
  });
}
function table(widths, header, rows) {
  const head = new TableRow({ tableHeader: true, cantSplit: true,
    children: header.map((h, i) => cell(h, widths[i], { bold: true, fill: 'D5E8F0', size: 17 })) });
  const body = rows.map((r) => new TableRow({ cantSplit: true, children: r.map((c, i) => cell(c, widths[i], { size: 17 })) }));
  return new Table({ width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA }, columnWidths: widths, rows: [head, ...body] });
}
const clip = (s, n = 650) => (s.length > n ? s.slice(0, n - 1).trimEnd() + '…' : s);
const BOX = '☐';

// ---------- build ----------
const items = parseLessonItems();
for (const [m, extra] of Object.entries(GRADE11_EXTRA)) items[m] = (items[m] || []).concat(extra);
const fe = loadFE();
for (const m of Object.keys(FE_G11_HUMAN)) fe[m] = null; // g11 handled separately

const kids = [];
const total = Object.values(items).reduce((a, v) => a + v.length, 0);
const feG10 = Object.entries(fe).filter(([m, v]) => v);
const feCount = feG10.reduce((a, [, v]) => a + v.length, 0);

// cover / how to use
kids.push(new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: 'Teacher Review Handout', font: FONT, size: 44, bold: true, color: '1F3864' })] }));
kids.push(P('Kenya CBE lesson plans, Grade 10 and Grade 11 Biology. Compiled 5 October 2026.', { size: 22, after: 160 }));
kids.push(H2('What we are asking you to do'));
for (const t of [
  'Part A: four sub-strand templates that need an owner\'s decision.',
  'Part B: lesson-plan items grouped by subject. Tick the box when you have decided, and write the fix or decision in the last column.',
  'Part C: Final Explanations that a named person must read and clear before the documents can be released.',
  'Part D: an optional spot check.',
]) kids.push(P('•  ' + t, { after: 40 }));
kids.push(H2('Key to item types'));
kids.push(table([3200, 10480], ['Type', 'What it means and what we need from you'], [
  ['Science error: needs rewrite', 'A real error. Fixing it changes an activity, dataset or worked answer, so an author must rewrite it.'],
  ['Science check', 'Probably acceptable, but please confirm the science is right for the level.'],
  ['Structural', 'Lessons overlap, are in the wrong order, or use an activity that no lesson contains. Decide how to reorder or what to add.'],
  ['Teaching choice', 'Two acceptable explanations exist. Pick one, or accept both.'],
]));
kids.push(P('', { after: 120 }));
kids.push(H2('Counts'));
const rows = [];
for (const [p, n] of SUBJECTS) {
  const li = Object.entries(items).filter(([m]) => subjOf(m) === p);
  const fi = p === 'g11_bio' ? Object.keys(FE_G11_HUMAN).length : feG10.filter(([m]) => subjOf(m) === p).length;
  rows.push([n, String(li.length), String(li.reduce((a, [, v]) => a + v.length, 0)), String(fi)]);
}
rows.push(['Total', String(Object.keys(items).length), String(total), String(feG10.length + Object.keys(FE_G11_HUMAN).length)]);
kids.push(table([5000, 2900, 2900, 2880], ['Subject', 'Sub-strands with lesson items', 'Lesson items', 'Final Explanations to clear'], rows));
kids.push(P('Fixed items have been removed. Items the reviewer raised that proved to be false alarms are not listed.', { italics: true, size: 16, before: 100 }));

// Part A
kids.push(new Paragraph({ children: [new PageBreak()] }));
kids.push(H1('Part A. Template problems (owner decision)'));
kids.push(P('These are not errors in the generated lessons. The teacher template supplied for the sub-strand is the wrong one or has no phenomenon.', { after: 100 }));
kids.push(table([600, 3600, 6280, 3200], [BOX, 'Sub-strand', 'Problem', 'Decision / who'],
  TEMPLATE_PROBLEMS.map(([a, b]) => [BOX, a, b, ''])));

// Part B
kids.push(new Paragraph({ children: [new PageBreak()] }));
kids.push(H1('Part B. Lesson-plan items by subject'));
let first = true;
for (const [p, n] of SUBJECTS) {
  const mods = Object.keys(items).filter((m) => subjOf(m) === p).sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
  if (!mods.length) continue;
  if (!first) kids.push(new Paragraph({ children: [new PageBreak()] }));
  first = false;
  kids.push(H2(n));
  for (const m of mods) {
    kids.push(H3(`${m}  —  ${label(m)}`));
    const its = items[m].slice().sort((a, b) => TYPE_ORDER.indexOf(a.type) - TYPE_ORDER.indexOf(b.type));
    kids.push(table([500, 2000, 3900, 4380, 2900], [BOX, 'Type', 'Where / what', 'Detail', 'Decision / fix'],
      its.map((it) => [BOX, it.type, it.topic, clip(it.detail), ''])));
  }
}

// Part C
kids.push(new Paragraph({ children: [new PageBreak()] }));
kids.push(H1('Part C. Final Explanations to read and clear'));
kids.push(P('The student Final Explanation and its teacher key are held back until a named person reads them and clears them. Each finding below is a reviewer\'s claim: check it against the document. Many are mild; some are real. Sign the line under each sub-strand when satisfied, and give the signed sheet to Mark.', { after: 100 }));
let firstC = true;
for (const [p, n] of SUBJECTS) {
  const mods = (p === 'g11_bio' ? Object.keys(FE_G11_HUMAN) : feG10.filter(([m]) => subjOf(m) === p).map(([m]) => m))
    .sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
  if (!mods.length) continue;
  if (!firstC) kids.push(new Paragraph({ children: [new PageBreak()] }));
  firstC = false;
  kids.push(H2(n));
  for (const m of mods) {
    kids.push(H3(`${m}  —  ${label(m)}`));
    if (p === 'g11_bio') {
      kids.push(table([500, 13180], [BOX, 'Triage note'], FE_G11_HUMAN[m].map((t) => [BOX, t]).concat([['', 'Cleared by: ______________________   Date: ____________   Notes: ____________________']])));
    } else {
      kids.push(table([500, 3300, 9880], [BOX, 'Where', 'Reviewer\'s finding'],
        fe[m].map((u) => [BOX, u.where || '', clip(u.problem || '', 800)]).concat([['', 'Cleared by / date', '________________________________    ______________    Notes: ______________________']])));
    }
    kids.push(P('', { after: 100 }));
  }
}

// Part D
kids.push(new Paragraph({ children: [new PageBreak()] }));
kids.push(H1('Part D. Optional spot check'));
for (const t of SPOT_CHECK) kids.push(P(BOX + '  ' + t, { after: 80 }));
kids.push(P('To clear a Final Explanation (Mark runs this): python3 scripts/rebuild_consistency.py --clear MODULE --by "Name" --note "..."', { italics: true, size: 16, before: 160 }));

const doc = new Document({
  styles: { default: { document: { run: { font: FONT, size: 18 } } } },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840, orientation: 'landscape' }, margin: { top: 1080, bottom: 1080, left: 1080, right: 1080 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [
      new TextRun({ text: 'Teacher Review Handout, Grade 10 and 11  |  page ', font: FONT, size: 16, color: '666666' }),
      new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16, color: '666666' })] })] }) },
    children: kids,
  }],
});
Packer.toBuffer(doc).then((b) => {
  fs.writeFileSync(OUT, b);
  console.log(`wrote ${OUT}: ${total} lesson items in ${Object.keys(items).length} sub-strands, ${feG10.length + Object.keys(FE_G11_HUMAN).length} Final Explanations`);
});
