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
  ShadingType, BorderStyle, HeadingLevel, Footer, Header, PageNumber, PageBreak, CheckBox, Bookmark, InternalHyperlink,
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
function table(widths, header, rows, keepRows = false) {
  const head = new TableRow({ tableHeader: true, cantSplit: true, children: header.map((h, i) => cell(h, widths[i], { bold: true, fill: 'D5E8F0' })) });
  const body = rows.map((r) => new TableRow({ cantSplit: keepRows, children: r.map((c, i) => (c && c.__cell ? cell(c.content, widths[i], c.o) : cell(c, widths[i]))) }));
  return new Table({ width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA }, columnWidths: widths, rows: [head, ...body] });
}
const paras = (s) => String(s || '').split('\n');
const BOX = '☐';
const moduleOf = (r) => r.id.replace(/-[^-]*$/, '');
const IDOF = (r) => (r.group ? `${moduleOf(r)} ${r.group}` : r.id);

// attention level of a journal item: 'flag' (no change made, teacher must decide), 'decision' (change proposed, teacher must confirm) or null
const attnOf = (members) => (members.some((r) => r.kind === 'flag') ? 'flag' : members.some((r) => r.teacher_decision) ? 'decision' : null);
const ATTN_FILL = { flag: 'F8CBAD', decision: 'FFF2CC' };
const ATTN_BADGE = { flag: '[FLAG] NO CHANGE MADE: YOUR DECISION NEEDED', decision: '[DECISION] CHANGE PROPOSED: PLEASE CONFIRM' };
const ATTN_COLOR = { flag: 'C00000', decision: 'C55A11' };
const anchorOf = (r) => 'i_' + IDOF(r).replace(/[^A-Za-z0-9]/g, '_');
const idPara = (r, extra = '') => P([new Bookmark({ id: anchorOf(r), children: [tr(IDOF(r) + extra, { bold: true })] })]);
const SSTAG = (r) => { const mt = meta(moduleOf(r)); return `SUB-STRAND ${mt.substrand_id} ${mt.substrand_name}`.toUpperCase(); };

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


// ---------- teacher response cell: two real Word checkboxes + a typing area ----------
const cb = (label) => new Paragraph({ spacing: { before: 40, after: 40 }, children: [
  new CheckBox({ checked: false, checkedState: { value: '2612', font: 'MS Gothic' }, uncheckedState: { value: '2610', font: 'MS Gothic' } }),
  new TextRun({ text: ' ' + label, font: FONT, size: 18, bold: true })] });
const teacherCell = (id, fill) => ({ __cell: true, o: { fill }, content: [
  P([tr('Tick ONE:', { size: 14, color: '666666' })], { after: 20 }),
  cb('ACCEPT'), cb('EDIT'),
  P([tr('If EDIT, type your requested change here:', { size: 14, color: '666666' })], { before: 80, after: 20 }),
  P(' ', { after: 400 }), P(' ', { after: 400 }),
  P([tr('Item ' + id, { size: 12, color: '999999' })], { after: 0 }),
] });

function recordRow(r) {
  const flagBits = [];
  if (r.severity === 'substantial') flagBits.push('SUBSTANTIAL');
  const attn = attnOf([r]);
  if (attn) flagBits.push(ATTN_BADGE[attn]);
  const fill = attn ? ATTN_FILL[attn] : undefined;
  return [
    { __cell: true, content: [P([tr(SSTAG(r), { bold: true, size: 14, color: '1F3864' })], { after: 20 }), idPara(r), ...flagBits.map((b) => P([tr(b, { bold: true, size: b.startsWith('[') ? 16 : 14, color: b.startsWith('[') ? ATTN_COLOR[attn] : 'C55A11' })], { after: 10 }))], o: { fill } },
    { __cell: true, content: [P([tr(DOC[r.target] || r.target, { bold: true })], { after: 30 }), P(r.where || '')], o: { fill } },
    { __cell: true, content: changeCell(r), o: { fill } },
    { __cell: true, content: whyCell(r), o: { fill } },
    { __cell: true, content: [P(r.reference || (r.category === 'science' ? '(none given)' : '—'), { size: 16 })], o: { fill } },
    teacherCell(IDOF(r), fill),
  ];
}


// ---------- grouping: one journal item per root fix, knock-on edits listed beneath it ----------
const clip = (t, n) => { t = String(t || '').replace(/\s+/g, ' ').trim(); return t.length > n ? t.slice(0, n - 1) + '…' : t; };
function journalItems(rs) {
  const items = []; const seen = new Map();
  for (const r of rs.slice().sort((a, b) => (a.kind === 'flag') - (b.kind === 'flag') || natural(a.id, b.id))) {
    if (!r.group) { items.push({ root: r, members: [r] }); continue; }
    if (seen.has(r.group)) { seen.get(r.group).members.push(r); continue; }
    const it = { group: r.group, root: r, members: [r] }; seen.set(r.group, it); items.push(it);
  }
  for (const it of items) if (it.group) it.root = it.members.find((r) => r.group_headline) || it.members[0];
  return items;
}
const needsDecision = (it) => it.members.some((r) => r.teacher_decision || r.kind === 'flag');
function itemRow(it) {
  if (!it.group || it.members.length === 1) return recordRow(it.root);
  const r = it.root, ms = it.members;
  const td = ms.some((x) => x.teacher_decision), sub = ms.some((x) => x.severity === 'substantial');
  const attn = attnOf(ms);
  const fill = attn ? ATTN_FILL[attn] : undefined;
  const bits = [`${ms.length} EDITS`, ...(sub ? ['SUBSTANTIAL'] : []), ...(attn ? [ATTN_BADGE[attn]] : [])];
  const crit = [...new Set(ms.flatMap((x) => x.criteria || []))].sort((a, b) => a - b).map((c) => `${c}. ${CRITERIA[c] || ''}`).join('; ');
  const ref = ms.map((x) => x.reference).find(Boolean);
  const what = [P([tr(r.group_headline || r.why, { bold: true })], { after: 60 }), ...changeCell(r)];
  const rest = ms.filter((x) => x !== r);
  if (rest.length) {
    what.push(P([tr(`Related edits made for consistency (${rest.length}). Exact wording is in the tracked-change document.`, { bold: true, size: 15, color: '666666' })], { before: 60, after: 20 }));
    for (const x of rest) what.push(P([tr(`${x.where}: `, { bold: true, size: 15 }), tr(x.kind === 'flag' ? '(flag, no text changed) ' + clip(x.why, 140) : clip(x.new, 150), { size: 15, color: '1B6B1B' })], { after: 20 }));
  }
  return [
    { __cell: true, content: [P([tr(SSTAG(r), { bold: true, size: 14, color: '1F3864' })], { after: 20 }), idPara(r, ' (group)'), ...bits.map((b) => P([tr(b, { bold: true, size: b.startsWith('[') ? 16 : 14, color: b.startsWith('[') ? ATTN_COLOR[attn] : 'C55A11' })], { after: 10 }))], o: { fill } },
    { __cell: true, content: [P([tr(DOC[r.target] || r.target, { bold: true })], { after: 30 }), P(r.where || ''), P(`and ${rest.length} related place${rest.length === 1 ? '' : 's'}`, { italics: true, size: 15 })], o: { fill } },
    { __cell: true, content: what, o: { fill } },
    { __cell: true, content: [P([tr(r.why)], { after: 40 }), P([tr('Guideline: ' + crit + '  |  Type: ' + r.category, { italics: true, size: 15, color: '555555' })])], o: { fill } },
    { __cell: true, content: [P(ref || (r.category === 'science' ? '(none given)' : '—'), { size: 16 })], o: { fill } },
    teacherCell(IDOF(r), fill),
  ];
}
const keyChanges = (items) => items.filter((it) => (it.group && it.members.length > 1) || it.members.some((r) => r.severity === 'substantial'))
  .map((it) => P([tr('• ' + (it.root.group_headline || it.root.why), { size: 17 }), tr(`  [guideline ${[...new Set(it.members.flatMap((x) => x.criteria || []))].sort((a, b) => a - b).join(', ')}${it.members.some((x) => x.teacher_decision) ? '; teacher decision' : ''}]`, { size: 15, color: '666666' })], { after: 30 }));

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
  P([tr('Items that need YOUR attention are marked and shaded: ', { bold: true }), tr('ORANGE rows carry [FLAG]: a problem or question where no text was changed and you must decide what to do. YELLOW rows carry [DECISION]: Claude proposed a change that depends on a judgement call, please confirm it. To jump to them, press Ctrl+F and search for  [FLAG]  or  [DECISION] , or use the "Needs your attention" list at the top of each sub-strand (click an item number to jump to it). A separate document, Flagged_Items_<Subject>.docx, lists ONLY these items so you can read them together; record your answer (ACCEPT or EDIT) in the journal, next to the same item number, not in the summary.')]),
  P([tr('How to respond (every item, in the last column): ', { bold: true }), tr('click ONE box, ACCEPT or EDIT. If you choose EDIT, type the change you want in the space under it. Save the file under the same name and send it back. Every item carries its sub-strand name, and each section has the sub-strand in the page header, so please keep the items in this document.')]),
];

function volume(title, modules) {
  const kids = [P([new TextRun({ text: title, font: FONT, size: 40, bold: true, color: '1F3864' })], { after: 60 }),
    P('Revision journal. Grade 10, 14 October 2026 revision. Prepared by Claude (AI), proposed for teacher review.', { size: 20, after: 140 }), ...howTo()];
  const srows = modules.map((m) => { const s = stats(recs[m]); const mt = meta(m); const its = journalItems(recs[m]); return [`${mt.substrand_id} ${mt.substrand_name}`, String(s.edits), String(its.length), String(s.science), String(s.substantial), String(its.filter(needsDecision).length)]; });
  const tot = stats(modules.flatMap((m) => recs[m]));
  const allIts = modules.flatMap((m) => journalItems(recs[m]));
  srows.push(['Total', String(tot.edits), String(allIts.length), String(tot.science), String(tot.substantial), String(allIts.filter(needsDecision).length)]);
  kids.push(H2('Summary'));
  kids.push(table([5000, 1700, 1700, 1700, 1700, 1880], ['Sub-strand', 'Edits made', 'Journal items (fixes)', 'Science corrections', 'Substantial', 'Items needing a teacher decision'], srows));
  const PAGE = { page: { size: { width: 12240, height: 15840, orientation: 'landscape' }, margin: { top: 1100, bottom: 900, left: 1080, right: 1080 } } };
  const foot = (label) => new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: `${label}  |  page `, font: FONT, size: 16, color: '666666' }), new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16, color: '666666' })] })] });
  const sections = [{ properties: PAGE, footers: { default: foot(`${title}: revision journal`) }, children: kids }];
  for (const m of modules) {
    const mt = meta(m);
    const tag = `SUB-STRAND ${mt.substrand_id} ${mt.substrand_name} (${m})`;
    const ks = [H2(`${mt.substrand_id} ${mt.substrand_name}   (${m})`)];
    const items = journalItems(recs[m]);
    const kc = keyChanges(items);
    if (kc.length) { ks.push(P([tr('Key changes at a glance', { bold: true, size: 20, color: '1F3864' })], { before: 60, after: 60, keepNext: true })); ks.push(...kc); ks.push(P('', { after: 80 })); }
    const att = items.filter((it) => attnOf(it.members));
    if (att.length) {
      const nf = att.filter((it) => attnOf(it.members) === 'flag').length;
      ks.push(P([tr(`Needs your attention: ${att.length} items (${nf} [FLAG], ${att.length - nf} [DECISION])`, { bold: true, size: 20, color: 'C00000' })], { before: 60, after: 60, keepNext: true }));
      ks.push(table([2300, 2300, 3300, 5780], ['Item (click to jump)', 'Type', 'Where', 'What'], att.map((it) => {
        const a = attnOf(it.members); const r = it.members.find((x) => x.kind === 'flag' || x.teacher_decision) || it.root;
        const fill = ATTN_FILL[a];
        return [
          { __cell: true, o: { fill }, content: [new Paragraph({ spacing: { after: 40 }, children: [new InternalHyperlink({ anchor: anchorOf(it.root), children: [tr(IDOF(it.root), { bold: true, color: '0563C1', underline: true })] })] })] },
          { __cell: true, o: { fill }, content: [P([tr(a === 'flag' ? '[FLAG] no change made' : '[DECISION] change proposed', { bold: true, color: ATTN_COLOR[a] })])] },
          { __cell: true, o: { fill }, content: [P(clip(it.root.where || '', 90))] },
          { __cell: true, o: { fill }, content: [P(clip((it.root.group_headline ? it.root.group_headline + '. ' : '') + r.why, 260))] },
        ];
      }), true));
      ks.push(P('', { after: 120 }));
    }
    ks.push(table([1300, 1700, 4100, 2700, 1500, 2380], ['#', 'Where', 'What changed', 'Why', 'Reference (science)', 'Teacher response'], items.map(itemRow)));
    sections.push({ properties: PAGE,
      headers: { default: new Header({ children: [new Paragraph({ shading: { fill: 'D5E8F0', type: ShadingType.CLEAR, color: 'auto' }, children: [new TextRun({ text: tag, font: FONT, size: 20, bold: true, color: '1F3864' })] })] }) },
      footers: { default: foot(tag) }, children: ks });
  }
  return new Document({ styles: { default: { document: { run: { font: FONT, size: 17 } } } }, sections });
}


// ---------- flagged-items summary: one document per subject, only [FLAG] and [DECISION] items ----------
function flaggedDoc(title, modules) {
  const PAGE = { page: { size: { width: 12240, height: 15840, orientation: 'landscape' }, margin: { top: 1100, bottom: 900, left: 1080, right: 1080 } } };
  const foot = (label) => new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: `${label}  |  page `, font: FONT, size: 16, color: '666666' }), new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16, color: '666666' })] })] });
  const perMod = modules.map((m) => [m, journalItems(recs[m]).filter((it) => attnOf(it.members))]);
  const all = perMod.flatMap(([, a]) => a);
  const nFlag = all.filter((it) => attnOf(it.members) === 'flag').length;
  const kids = [
    P([new TextRun({ text: `${title}: flagged items`, font: FONT, size: 40, bold: true, color: '1F3864' })], { after: 60 }),
    P('Summary of ONLY the items that need a teacher\'s attention. Prepared by Claude (AI), proposed for teacher review.', { size: 20, after: 140 }),
    P([tr('[FLAG] (orange): ', { bold: true, color: 'C00000' }), tr('a problem or question where no text was changed; you decide what should happen. ')]),
    P([tr('[DECISION] (yellow): ', { bold: true, color: 'C55A11' }), tr('Claude proposed a change that rests on a judgement call (for example local knowledge, a timetable choice, or unverified Kiswahili terms); please confirm it or ask for a different version.')]),
    P([tr('How to answer: ', { bold: true }), tr(`open the journal (Journal_${title.replace(/ /g, '_')}.docx), find the item by the same item number, and tick ACCEPT or EDIT there (type your requested change in the box). Please do not answer in this summary.`)], { after: 120 }),
    H2('Summary'),
    table([6000, 2400, 2400, 2880], ['Sub-strand', 'Items needing attention', '[FLAG]', '[DECISION]'],
      [...perMod.map(([m, a]) => { const mt = meta(m); const f = a.filter((it) => attnOf(it.members) === 'flag').length; return [`${mt.substrand_id} ${mt.substrand_name}`, String(a.length), String(f), String(a.length - f)]; }),
        ['Total', String(all.length), String(nFlag), String(all.length - nFlag)]]),
  ];
  const sections = [{ properties: PAGE, footers: { default: foot(`${title}: flagged items`) }, children: kids }];
  for (const [m, a] of perMod) {
    const mt = meta(m);
    const tag = `SUB-STRAND ${mt.substrand_id} ${mt.substrand_name} (${m})`;
    const ks = [H2(`${mt.substrand_id} ${mt.substrand_name}   (${m})`)];
    if (!a.length) ks.push(P('No items need a teacher decision in this sub-strand.'));
    else {
      ks.push(P([tr(`${a.length} items. Journal item numbers are shown in the first column.`, { size: 18, color: '555555' })], { after: 80 }));
      ks.push(table([1500, 1500, 2100, 4780, 3800], ['Journal item', 'Type', 'Where', 'Issue / what you are asked to decide', 'Claude\'s proposal'],
        a.map((it) => {
          const k = attnOf(it.members); const fill = ATTN_FILL[k];
          const r = it.members.find((x) => x.kind === 'flag' || x.teacher_decision) || it.root;
          const head = it.root.group_headline ? it.root.group_headline + ' ' : '';
          const proposal = r.kind === 'flag' ? 'No text changed. See the suggestion in the issue text.' : clip(it.root.kind === 'set' ? it.root.new : (it.root.new || r.new), 500);
          return [
            { __cell: true, o: { fill }, content: [P([tr(IDOF(it.root) + (it.members.length > 1 ? ` (+${it.members.length - 1} related edits)` : ''), { bold: true })])] },
            { __cell: true, o: { fill }, content: [P([tr(k === 'flag' ? '[FLAG]' : '[DECISION]', { bold: true, color: ATTN_COLOR[k] })])] },
            { __cell: true, o: { fill }, content: [P(it.root.where || '')] },
            { __cell: true, o: { fill }, content: [...(head ? [P([tr(head, { bold: true })])] : []), P(r.why)] },
            { __cell: true, o: { fill }, content: [P(proposal)] },
          ];
        }), true));
    }
    sections.push({ properties: PAGE,
      headers: { default: new Header({ children: [new Paragraph({ shading: { fill: 'D5E8F0', type: ShadingType.CLEAR, color: 'auto' }, children: [new TextRun({ text: tag, font: FONT, size: 20, bold: true, color: '1F3864' })] })] }) },
      footers: { default: foot(tag) }, children: ks });
  }
  return new Document({ styles: { default: { document: { run: { font: FONT, size: 17 } } } }, sections });
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
    const ff = path.join(jdir, `Flagged_Items_${name.replace(/ /g, '_')}.docx`);
    fs.writeFileSync(ff, await Packer.toBuffer(flaggedDoc(name, mods)));
    written.push(ff);
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
  const dec = Object.entries(recs).flatMap(([m, rs]) => journalItems(rs).filter(needsDecision).map((it) => [m, it]));
  kids.push(table([2200, 3200, 6580, 1700], ['Sub-strand', 'Where', 'What and why', 'Journal'], dec.map(([m, it]) => {
    const mt = meta(m); const s = subjOf(m); const r = it.members.find((x) => x.teacher_decision || x.kind === 'flag') || it.root;
    return [`${mt.substrand_id} ${mt.substrand_name}`, (it.root.where || '') + (it.members.length > 1 ? ` (+${it.members.length - 1} related)` : ''), (r.kind === 'flag' ? '' : 'Suggested change: ') + (it.root.group_headline ? it.root.group_headline + '. ' : '') + r.why, s ? `Journal_${s[1].replace(/ /g, '_')}` : ''];
  })));
  const fm = path.join(jdir, 'Journal_00_Master_Index.docx');
  fs.writeFileSync(fm, await Packer.toBuffer(new Document({ styles: { default: { document: { run: { font: FONT, size: 17 } } } }, sections: [{
    properties: { page: { size: { width: 12240, height: 15840, orientation: 'landscape' }, margin: { top: 900, bottom: 900, left: 1080, right: 1080 } } }, children: kids }] })));
  written.push(fm);
  console.log(written.map((f) => path.basename(f)).join('\n'));
})();
