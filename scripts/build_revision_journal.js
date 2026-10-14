#!/usr/bin/env node
/**
 * build_revision_journal.js — teacher-facing journal of every change in the revised corpus
 *   node scripts/build_revision_journal.js [--only MODULE,MODULE]
 * Reads <REV>/change_records/*.json (written by scripts/revise_apply.py); writes
 * <REV>/journal/Journal_<Subject>.docx (one per subject) and Journal_00_Master_Index.docx.
 * Each change: what changed and how (exact before/after), why, where, and for science changes a reference.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, AlignmentType,
  ShadingType, BorderStyle, HeadingLevel, Footer, PageNumber, PageBreak,
} = require('docx');

const ROOT = path.resolve(__dirname, '..');
const REV = process.env.CBE_REVISED_DIR || path.join(ROOT, 'data', 'revised_2026-10');
const FONT = 'Arial';
const only = (() => { const i = process.argv.indexOf('--only'); return i > 0 ? new Set(process.argv[i + 1].split(',')) : null; })();

const CRITERIA = {
  1: 'Storyline and phenomenon', 2: 'KICD alignment', 3: 'Time and pacing', 4: 'Sequence logic',
  5: 'Student thinking', 6: 'Models and analogies', 7: 'Sensemaking scaffolds', 8: 'Practical feasibility and safety',
  9: 'Local and cultural accuracy', 10: 'Summative assessment', 11: 'Resources and links', 12: 'Inclusion',
  13: 'Teacher usability', 14: 'Consistency',
};
const SUBJECTS = [['bio', 'Biology'], ['chem', 'Chemistry'], ['phys', 'Physics'], ['math', 'Mathematics'],
  ['coremath', 'Core Mathematics'], ['essmath', 'Essential Mathematics'], ['gensci', 'General Science']];
const subjOf = (m) => SUBJECTS.find(([p]) => m.startsWith(p + '_'));
const DOC = { lesson: 'Lesson Sequence', final_explanation: 'Final Explanation (student copy and teacher key)', unit: 'Lesson Sequence, unit overview' };

// ---------- docx helpers ----------
const border = { style: BorderStyle.SINGLE, size: 4, color: '999999' };
const borders = { top: border, bottom: border, left: border, right: border };
const tr = (t, o = {}) => new TextRun({ text: t, font: FONT, size: o.size || 17, bold: o.bold, italics: o.italics, color: o.color, strike: o.strike, underline: o.underline ? {} : undefined });
const P = (kids, o = {}) => new Paragraph({ spacing: { before: o.before || 0, after: o.after ?? 60 }, alignment: o.align, keepNext: o.keepNext,
  children: Array.isArray(kids) ? kids : [tr(kids, o)] });
const H1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 200, after: 100 }, keepNext: true, children: [new TextRun({ text: t, font: FONT, size: 30, bold: true, color: '1F3864' })] });
const H2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 260, after: 80 }, keepNext: true, children: [new TextRun({ text: t, font: FONT, size: 24, bold: true, color: '2E75B6' })] });
function cell(content, width, o = {}) {
  const paras = (Array.isArray(content) ? content : [content]).map((c) => (typeof c === 'string' ? P(c, o) : c));
  return new TableCell({ borders, width: { size: width, type: WidthType.DXA }, margins: { top: 50, bottom: 50, left: 80, right: 80 },
    shading: o.fill ? { fill: o.fill, type: ShadingType.CLEAR, color: 'auto' } : undefined, children: paras });
}
function table(widths, header, rows) {
  const head = new TableRow({ tableHeader: true, cantSplit: true, children: header.map((h, i) => cell(h, widths[i], { bold: true, fill: 'D5E8F0' })) });
  const body = rows.map((r) => new TableRow({ children: r.map((c, i) => (c && c.__cell ? cell(c.content, widths[i], c.o) : cell(c, widths[i]))) }));
  return new Table({ width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA }, columnWidths: widths, rows: [head, ...body] });
}
const paras = (s) => String(s || '').split('\n');
const BOX = '☐';

function changeCell(r) {
  if (r.kind === 'flag') return [P([tr('Flagged for teacher review. No text was changed.', { bold: true })])];
  const out = [];
  const label = (t) => P([tr(t, { bold: true, size: 15, color: '666666' })], { after: 20 });
  out.push(label('BEFORE'));
  for (const l of paras(r.old)) out.push(P([tr(l, { color: 'C00000', strike: true })], { after: 30 }));
  out.push(label('AFTER'));
  for (const l of paras(r.new)) out.push(P([tr(l, { color: '1B6B1B', underline: true })], { after: 30 }));
  return out;
}
function whyCell(r) {
  const crit = (r.criteria || []).map((c) => `${c}. ${CRITERIA[c] || ''}`).join('; ');
  const out = [P([tr(r.why)], { after: 40 }), P([tr('Guideline: ' + crit + '  |  Type: ' + r.category, { italics: true, size: 15, color: '555555' })])];
  return out;
}

function recordRow(r) {
  const flagBits = [];
  if (r.severity === 'substantial') flagBits.push('SUBSTANTIAL');
  if (r.teacher_decision) flagBits.push('TEACHER DECISION');
  if (r.kind === 'flag') flagBits.push('FLAG');
  const fill = r.teacher_decision || r.kind === 'flag' ? 'FFF2CC' : undefined;
  return [
    { __cell: true, content: [P([tr(r.id.split('-').pop(), { bold: true })]), ...flagBits.map((b) => P([tr(b, { bold: true, size: 14, color: 'C55A11' })], { after: 10 }))], o: { fill } },
    { __cell: true, content: [P([tr(DOC[r.target] || r.target, { bold: true })], { after: 30 }), P(r.where || '')], o: { fill } },
    { __cell: true, content: changeCell(r), o: { fill } },
    { __cell: true, content: whyCell(r), o: { fill } },
    { __cell: true, content: [P(r.reference || (r.category === 'science' ? '(none given)' : '—'), { size: 16 })], o: { fill } },
    { __cell: true, content: [P(BOX, { size: 22, align: AlignmentType.CENTER }), P('Accept / reject / edit', { size: 13, align: AlignmentType.CENTER })], o: { fill } },
  ];
}

// ---------- load ----------
const recs = {};
for (const f of fs.readdirSync(path.join(REV, 'change_records')).filter((x) => x.endsWith('.json'))) {
  const h = JSON.parse(fs.readFileSync(path.join(REV, 'change_records', f), 'utf8'));
  if (only && !only.has(h.module)) continue;
  recs[h.module] = h.records;
}
const meta = (m) => { try { return require(path.join(REV, 'modules', `${m}_data.js`)).META; } catch { return { substrand_id: '', substrand_name: m }; } };
const natural = (a, b) => a.localeCompare(b, undefined, { numeric: true });
const stats = (rs) => ({
  total: rs.length, edits: rs.filter((r) => r.kind !== 'flag').length, flags: rs.filter((r) => r.kind === 'flag').length,
  science: rs.filter((r) => r.category === 'science').length, substantial: rs.filter((r) => r.severity === 'substantial').length,
  decide: rs.filter((r) => r.teacher_decision || r.kind === 'flag').length,
});

const howTo = () => [
  H2('How to read this journal'),
  P('Every change made to the Grade 10 lesson plans is listed here, grouped by sub-strand. The same change is also visible as a Word tracked change in the matching "_TRACKED.docx" file, so you can accept or reject it there.'),
  P('Each row gives: where the change is (document, lesson, phase and field), exactly what changed (BEFORE in red strike-through, AFTER in green underline), why it was changed and which of the 14 lesson-plan guidelines it serves, and for science corrections a reference that supports the fix. References are named sources, to be verified by a reviewer (page numbers are not given).'),
  P('Rows shaded yellow need a teacher decision (a judgement call or a flag with no change made). Tick the box in the last column and write any note beside the row.'),
];

function volume(title, modules) {
  const kids = [P([new TextRun({ text: title, font: FONT, size: 40, bold: true, color: '1F3864' })], { after: 60 }),
    P('Revision journal. Grade 10, 14 October 2026 revision. Prepared by Claude (AI), proposed for teacher review.', { size: 20, after: 140 }), ...howTo()];
  const srows = modules.map((m) => { const s = stats(recs[m]); const mt = meta(m); return [`${mt.substrand_id} ${mt.substrand_name}`, String(s.edits), String(s.science), String(s.substantial), String(s.decide)]; });
  const tot = stats(modules.flatMap((m) => recs[m]));
  srows.push(['Total', String(tot.edits), String(tot.science), String(tot.substantial), String(tot.decide)]);
  kids.push(H2('Summary'));
  kids.push(table([6000, 1800, 1800, 2000, 2080], ['Sub-strand', 'Changes made', 'Science corrections', 'Substantial', 'Need a teacher decision'], srows));
  for (const m of modules) {
    const mt = meta(m);
    kids.push(new Paragraph({ children: [new PageBreak()] }));
    kids.push(H2(`${mt.substrand_id} ${mt.substrand_name}   (${m})`));
    const order = recs[m].slice().sort((a, b) => (a.kind === 'flag') - (b.kind === 'flag') || natural(a.id, b.id));
    kids.push(table([800, 2200, 4700, 3200, 1900, 880], ['#', 'Where', 'What changed', 'Why', 'Reference (science)', 'Teacher'], order.map(recordRow)));
  }
  return new Document({ styles: { default: { document: { run: { font: FONT, size: 17 } } } }, sections: [{
    properties: { page: { size: { width: 12240, height: 15840, orientation: 'landscape' }, margin: { top: 900, bottom: 900, left: 1080, right: 1080 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: `${title}: revision journal  |  page `, font: FONT, size: 16, color: '666666' }), new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16, color: '666666' })] })] }) },
    children: kids }] });
}

(async () => {
  const jdir = path.join(REV, 'journal');
  fs.mkdirSync(jdir, { recursive: true });
  const bySubj = {};
  for (const m of Object.keys(recs).sort(natural)) { const s = subjOf(m); if (s) (bySubj[s[1]] = bySubj[s[1]] || []).push(m); }
  const written = [];
  for (const [name, mods] of Object.entries(bySubj)) {
    const f = path.join(jdir, `Journal_${name.replace(/ /g, '_')}.docx`);
    fs.writeFileSync(f, await Packer.toBuffer(volume(`${name}`, mods)));
    written.push(f);
  }
  // master index
  const all = Object.values(recs).flat();
  const kids = [P([new TextRun({ text: 'Revision journal: master index', font: FONT, size: 40, bold: true, color: '1F3864' })], { after: 60 }),
    P('Grade 10 lesson plans, 14 October 2026 revision. One journal per subject; this page totals them and lists the items needing a teacher decision.', { size: 20, after: 140 }), ...howTo()];
  kids.push(H2('Totals by subject'));
  const rows = Object.entries(bySubj).map(([n, mods]) => { const s = stats(mods.flatMap((m) => recs[m])); return [n, String(mods.length), String(s.edits), String(s.science), String(s.substantial), String(s.decide)]; });
  const t = stats(all);
  rows.push(['Total', String(Object.keys(recs).length), String(t.edits), String(t.science), String(t.substantial), String(t.decide)]);
  kids.push(table([4200, 1700, 1800, 1800, 1800, 2380], ['Subject', 'Sub-strands revised', 'Changes made', 'Science corrections', 'Substantial', 'Need a teacher decision'], rows));
  kids.push(H2('Changes by guideline'));
  const byC = {};
  for (const r of all) for (const c of r.criteria || []) byC[c] = (byC[c] || 0) + 1;
  kids.push(table([900, 9000, 3780], ['#', 'Guideline', 'Changes'], Object.keys(CRITERIA).map((c) => [c, CRITERIA[c], String(byC[c] || 0)])));
  kids.push(H2('Items needing a teacher decision'));
  const dec = Object.entries(recs).flatMap(([m, rs]) => rs.filter((r) => r.teacher_decision || r.kind === 'flag').map((r) => [m, r]));
  kids.push(table([2200, 3200, 6580, 1700], ['Sub-strand', 'Where', 'What and why', 'Journal'], dec.map(([m, r]) => {
    const mt = meta(m); const s = subjOf(m);
    return [`${mt.substrand_id} ${mt.substrand_name}`, r.where || '', (r.kind === 'flag' ? '' : 'Suggested change: ') + r.why, s ? `Journal_${s[1].replace(/ /g, '_')}` : ''];
  })));
  const fm = path.join(jdir, 'Journal_00_Master_Index.docx');
  fs.writeFileSync(fm, await Packer.toBuffer(new Document({ styles: { default: { document: { run: { font: FONT, size: 17 } } } }, sections: [{
    properties: { page: { size: { width: 12240, height: 15840, orientation: 'landscape' }, margin: { top: 900, bottom: 900, left: 1080, right: 1080 } } }, children: kids }] })));
  written.push(fm);
  console.log(written.map((f) => path.basename(f)).join('\n'));
})();
