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

const howTo = (opts) => [
  H2('How to read this journal'),
  P((opts && opts.intro) || 'Every change made to the Grade 10 lesson plans is listed here, grouped by sub-strand. The same change is also visible as a Word tracked change in the matching "_TRACKED.docx" file, so you can accept or reject it there.'),
  P('Each row gives: where the change is (document, lesson, phase and field), exactly what changed (BEFORE in red strike-through, AFTER in green underline), why it was changed and which of the 14 lesson-plan guidelines it serves, and for science corrections a reference that supports the fix. References are named sources, to be verified by a reviewer (page numbers are not given).'),
  P([tr('Items that need YOUR attention are marked and shaded: ', { bold: true }), tr('ORANGE rows carry [FLAG]: a problem or question where no text was changed and you must decide what to do. YELLOW rows carry [DECISION]: Claude proposed a change that depends on a judgement call, please confirm it. To jump to them, press Ctrl+F and search for  [FLAG]  or  [DECISION] , or use the "Needs your attention" list at the top of each sub-strand (click an item number to jump to it). A separate document, Flagged_Items_<Subject>.docx, lists ONLY these items so you can read them together, and it has the same ACCEPT / EDIT boxes: answer the [FLAG] and [DECISION] items there (or here, but not both; if you answer in both and they differ, the Flagged Items document is used). Answer every other item in this journal.')]),
  P([tr('How to respond (every item, in the last column): ', { bold: true }), tr('click ONE box, ACCEPT or EDIT. If you choose EDIT, type the change you want in the space under it. Save the file under the same name and send it back. Every item carries its sub-strand name, and each section has the sub-strand in the page header, so please keep the items in this document.')]),
];

function volume(title, modules, opts) {
  const kids = [P([new TextRun({ text: title, font: FONT, size: 40, bold: true, color: '1F3864' })], { after: 60 }),
    P((opts && opts.sub) || 'Revision journal. Grade 10. First revision 14 October 2026; rebuilt 10 November 2026 with all Round 2 changes. This is the complete record (including items teachers already answered). Prepared by Claude (AI), proposed for teacher review.', { size: 20, after: 140 }), ...howTo(opts)];
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
    P([tr('How to answer: ', { bold: true }), tr(`answer HERE, in the last column of each item: click ONE box, ACCEPT or EDIT, and if you choose EDIT type your requested change in the space below. You do not need to answer these items again in the journal (Journal_${title.replace(/ /g, '_')}.docx); use the journal for all the other items. Save the file under the same name and send it back.`)], { after: 120 }),
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
      ks.push(table([1300, 1200, 1700, 7100, 2380], ['Journal item', 'Type', 'Where', 'Issue / what you are asked to decide, and Claude\'s proposal', 'Teacher response'],
        a.map((it) => {
          const k = attnOf(it.members); const fill = ATTN_FILL[k];
          const r = it.members.find((x) => x.kind === 'flag' || x.teacher_decision) || it.root;
          const head = it.root.group_headline ? it.root.group_headline + ' ' : '';
          const proposal = r.kind === 'flag' ? 'No text was changed. The suggestion, if any, is in the issue text above.' : clip(it.root.kind === 'set' ? it.root.new : (it.root.new || r.new), 700);
          return [
            { __cell: true, o: { fill }, content: [P([tr(IDOF(it.root) + (it.members.length > 1 ? ` (+${it.members.length - 1} related edits)` : ''), { bold: true })])] },
            { __cell: true, o: { fill }, content: [P([tr(k === 'flag' ? '[FLAG]' : '[DECISION]', { bold: true, color: ATTN_COLOR[k] })])] },
            { __cell: true, o: { fill }, content: [P(it.root.where || '')] },
            { __cell: true, o: { fill }, content: [...(head ? [P([tr(head, { bold: true })])] : []), P(r.why),
              P([tr('CLAUDE\'S PROPOSAL', { bold: true, size: 15, color: '666666' })], { before: 60, after: 20 }), P([tr(proposal, { color: r.kind === 'flag' ? '666666' : '1B6B1B', italics: r.kind === 'flag' })])] },
            teacherCell(IDOF(it.root), fill),
          ];
        }), false));
    }
    sections.push({ properties: PAGE,
      headers: { default: new Header({ children: [new Paragraph({ shading: { fill: 'D5E8F0', type: ShadingType.CLEAR, color: 'auto' }, children: [new TextRun({ text: tag, font: FONT, size: 20, bold: true, color: '1F3864' })] })] }) },
      footers: { default: foot(tag) }, children: ks });
  }
  return new Document({ styles: { default: { document: { run: { font: FONT, size: 17 } } } }, sections });
}


// ---------- post-process: valid, unique bookmark ids and explicitly identified checkboxes ----------
const JSZip = require('jszip');
async function finalize(buf) {
  const zip = await JSZip.loadAsync(buf);
  let xml = await zip.file('word/document.xml').async('string');
  let b = 0; let e = 0; let c = 0;
  xml = xml.replace(/<w:bookmarkStart ([^>]*?)w:id="\d+"/g, (m, pre) => `<w:bookmarkStart ${pre}w:id="${++b}"`);
  xml = xml.replace(/<w:bookmarkEnd w:id="\d+"/g, () => `<w:bookmarkEnd w:id="${++e}"`);
  xml = xml.replace(/<w:sdtPr><w14:checkbox>/g, () => { c++; const kind = c % 2 === 1 ? 'ACCEPT' : 'EDIT'; return `<w:sdtPr><w:alias w:val="${kind}"/><w:tag w:val="cb${c}"/><w:id w:val="${700000 + c}"/><w14:checkbox>`; });
  zip.file('word/document.xml', xml);
  return zip.generateAsync({ type: 'nodebuffer', compression: 'DEFLATE' });
}


// ---------- Round 2 teacher summary: PART A (closest review, journal format) + PART B (optional list of verified fixes) ----------
const isA = (r) => /^R2-LES-(PROPOSED|CLOSE)-/.test(r.group || '');
const isB = (r) => /^R2-LES-(AUTO|TRIAGE|FINAL)$/.test(r.group || '') || r.group === 'R2-FE-AUTO' || r.group === 'R2-VERIFY-FIX';
function round2Doc() {
  const PAGE = { page: { size: { width: 12240, height: 15840, orientation: 'landscape' }, margin: { top: 1100, bottom: 900, left: 1080, right: 1080 } } };
  const foot = (label) => new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: `${label}  |  page `, font: FONT, size: 16, color: '666666' }), new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16, color: '666666' })] })] });
  const mods = Object.keys(recs).sort(natural).filter((m) => subjOf(m) && ['bio', 'chem', 'phys', 'math'].includes(subjOf(m)[0]));
  const A = Object.fromEntries(mods.map((m) => [m, recs[m].filter(isA)]));
  const B = Object.fromEntries(mods.map((m) => [m, recs[m].filter((r) => isB(r) && !isA(r))]));
  const aItems = Object.fromEntries(mods.map((m) => [m, journalItems(A[m])]));
  const nA = mods.reduce((n, m) => n + aItems[m].length, 0);
  const nB = mods.reduce((n, m) => n + B[m].length, 0);
  const kids = [
    P([new TextRun({ text: 'Round 2 lesson check: summary for teacher review', font: FONT, size: 40, bold: true, color: '1F3864' })], { after: 60 }),
    P('Grade 10 Biology, Chemistry, Physics and Mathematics. Prepared by Claude (AI), proposed for teacher review.', { size: 20, after: 140 }),
    H2('What this document is'),
    P('After your journal responses were applied, Claude checked every lesson against the other lessons in its sub-strand (cross-references, numbers, timings, names, science) and then checked that each Final Explanation still agrees with its lessons. Problems were fixed automatically only when the fix agreed with your earlier responses, with KICD, and was scientifically correct, and a second, independent check agreed. A few problems needed a real choice: for each of those Claude wrote a proposed answer and has already built it into the lesson, so you can keep it or edit it in place.'),
    H2('What you are asked to do'),
    P([tr('PART A: please review closely (' + nA + ' items). ', { bold: true, color: 'C00000' }), tr('These are the items where a teacher\'s judgement matters most: (1) proposed answers to choices Claude could not settle alone, such as phase timings, version numbering, how a model or dataset is used, and cross-lesson wording; (2) automatic fixes that involve a judgement call on timing or wording; (3) fixes that state a science fact. They appear in the same format as the journal, shaded YELLOW with [DECISION]. For each, click ONE box: ACCEPT (keep what is built in) or EDIT (and type the change you want). If you skip an item it stays as written.')]),
    P([tr('PART B: read only if you wish (' + nB + ' edits). ', { bold: true, color: '1F3864' }), tr('Small fixes that passed all three tests (agree with your earlier responses, agree with KICD, scientifically correct) and a second independent check. Examples: a lesson reference that pointed to the wrong lesson, two lessons giving different numbers for the same thing, a Final Explanation number that did not match the lesson. They are already made and need no answer. They are listed so you can spot-check a few. If you disagree with one, write its item number and what you want in the last column.')]),
    P([tr('How to send it back: ', { bold: true }), tr('save the file under the same name and return it. Every item carries its sub-strand name and its item number, so Claude can read your answers back and apply them.')], { after: 120 }),
    H2('Where the items are'),
    table([5200, 2200, 2200, 2380], ['Sub-strand', 'PART A items (closest review)', 'PART B edits (optional)', 'Where'],
      mods.filter((m) => aItems[m].length || B[m].length).map((m) => { const mt = meta(m); return [`${mt.substrand_id} ${mt.substrand_name} (${m})`, String(aItems[m].length), String(B[m].length), aItems[m].length ? 'PART A, then B' : 'PART B only']; })
        .concat([['Total', String(nA), String(nB), '']])),
  ];
  const sections = [{ properties: PAGE, footers: { default: foot('Round 2 lesson check: summary') }, children: kids }];
  const hdr = (tag) => ({ default: new Header({ children: [new Paragraph({ shading: { fill: 'D5E8F0', type: ShadingType.CLEAR, color: 'auto' }, children: [new TextRun({ text: tag, font: FONT, size: 20, bold: true, color: '1F3864' })] })] }) });
  sections.push({ properties: PAGE, footers: { default: foot('PART A') }, children: [H1('PART A: please review closely'), P('Yellow rows. Tick ACCEPT or EDIT in the last column; if EDIT, type what you want. The proposed answer is already in the lesson (AFTER, green). The alternative Claude suggested, if any, is in the Why column.')] });
  for (const m of mods) {
    const its = aItems[m]; if (!its.length) continue;
    const mt = meta(m); const tag = `SUB-STRAND ${mt.substrand_id} ${mt.substrand_name} (${m})`;
    const ks = [H2(`${mt.substrand_id} ${mt.substrand_name}   (${m})   PART A`), P([tr(`${its.length} items to review closely.`, { bold: true, size: 20, color: 'C00000' })], { after: 80 })];
    ks.push(table([1300, 1700, 4100, 2700, 1500, 2380], ['#', 'Where', 'What changed', 'Why (and the alternative)', 'Reference (science)', 'Teacher response'], its.map(itemRow)));
    sections.push({ properties: PAGE, headers: hdr(tag), footers: { default: foot(tag) }, children: ks });
  }
  const bKids = [H1('PART B: verified fixes, read only if you wish'), P('Already made. No answer needed. If you disagree with one, write the item number and what you want in the last column.')];
  for (const m of mods) {
    const rs = B[m]; if (!rs.length) continue;
    const mt = meta(m);
    bKids.push(H2(`${mt.substrand_id} ${mt.substrand_name}   (${m})   PART B`));
    bKids.push(table([1900, 1900, 3700, 3700, 2480], ['Item', 'Where', 'Before', 'After', 'If you disagree'],
      rs.map((r) => [
        { __cell: true, content: [P([tr(r.id, { bold: true, size: 15 })], { after: 20 }), P([tr(r.kind === 'set' ? 'Final Explanation (follows the lesson)' : (r.category || ''), { size: 14, color: '666666' })])] },
        r.where || (r.target === 'lesson' ? `Lesson ${r.lesson}, ${r.path}` : `${r.target}, ${r.path || ''}`),
        { __cell: true, content: [P([tr(clip(r.kind === 'set' ? JSON.stringify(r.old === undefined ? '' : r.old) : r.old, 320), { color: 'C00000', size: 15 })])] },
        { __cell: true, content: [P([tr(clip(r.kind === 'set' ? JSON.stringify(r.new === undefined ? r.value : r.new) : r.new, 320), { color: '1B6B1B', size: 15 })], { after: 30 }), P([tr('Why: ' + clip(r.why, 200), { size: 14, color: '555555', italics: true })])] },
        { __cell: true, content: [P(' ', { after: 300 })] },
      ]), false));
  }
  sections.push({ properties: PAGE, footers: { default: foot('PART B') }, children: bKids });
  return new Document({ styles: { default: { document: { run: { font: FONT, size: 17 } } } }, sections });
}

(async () => {
  if (process.argv.includes('--r2journal')) {
    // Round 2 journal: per subject, only the changes teachers have NOT yet seen or answered (Round 2 lesson/FE changes, proposed answers,
    // verification fixes, and Round 2 flags). Excludes the Round 1 items, the Round 2 applications of earlier teacher answers (numeric ids)
    // and the mechanical four-level rubric records.
    const PIPE = new Set(JSON.parse(fs.readFileSync(path.join(REV, 'round2', 'pipeline_flags.json'), 'utf8')).ids);
    const keep = (r) => r.kind === 'flag' ? ((r.applied_at || '') >= '2026-11-09' && !PIPE.has(r.id)) : (/-r2-/.test(r.id) && !/-r2-rub-/.test(r.id) && !/-r2-\d+$/.test(r.id));
    const jdir = path.join(REV, 'journal'); fs.mkdirSync(jdir, { recursive: true });
    const OPEN = process.argv.includes('--open-only');
    for (const m of Object.keys(recs)) {
      recs[m] = recs[m].filter(keep);
      if (OPEN) { // keep only items (groups or single records) that are ORANGE (flag) or YELLOW (teacher_decision)
        const gk = (r) => r.group || r.id;
        const att = new Set(recs[m].filter((r) => r.kind === 'flag' || r.teacher_decision).map(gk));
        recs[m] = recs[m].filter((r) => att.has(gk(r)));
      }
    }
    const bySubj = {};
    for (const m of Object.keys(recs).sort(natural)) { const s = subjOf(m); if (s && ['bio', 'chem', 'phys', 'math'].includes(s[0]) && recs[m].length) (bySubj[s[1]] = bySubj[s[1]] || []).push(m); }
    const opts = OPEN ? { sub: 'Round 2 OPEN ITEMS, 10 November 2026. Only the ORANGE [FLAG] and YELLOW [DECISION] items from Round 2 that need a teacher answer. Routine changes (white) are not listed here; they remain in the Round 2 journal. Prepared by Claude (AI), proposed for teacher review.',
      intro: 'This document lists ONLY the open items from Round 2. ORANGE [FLAG] items: a problem or question where no text was changed. Each carries a PROPOSED ANSWER from Claude; please ACCEPT it or EDIT it. YELLOW [DECISION] items: Claude already made a change that depends on a judgement call; please confirm or edit it. Ordinary changes are not listed.' } : { sub: 'Round 2 journal, updated 10 November 2026. Only the changes made since the teachers last reviewed (items you have already answered are not repeated). Prepared by Claude (AI), proposed for teacher review.',
      intro: 'This journal lists only the NEW changes from Round 2: automatic lesson-check fixes, the answers built in for earlier open questions, Final Explanation changes, and the small corrections from the final three-part check (teacher request, KICD, science). Each is grouped by sub-strand. The same changes are visible as Word tracked changes in the matching "_TRACKED.docx" file. The full history of all changes is in the Journal_<Subject>.docx file.' };
    for (const [name, mods] of Object.entries(bySubj)) {
      const f = path.join(jdir, `${OPEN ? 'Round2_OpenItems_' : 'Round2_Journal_'}${name.replace(/ /g, '_')}.docx`);
      fs.writeFileSync(f, await finalize(await Packer.toBuffer(volume(name + (OPEN ? ': Round 2 open items' : ': Round 2'), mods, opts))));
      console.log(path.basename(f), mods.reduce((n, m) => n + journalItems(recs[m]).length, 0), 'items;', mods.reduce((n, m) => n + journalItems(recs[m]).filter(needsDecision).length, 0), 'orange/yellow');
    }
    return;
  }
  if (process.argv.includes('--round2')) {
    const jdir = path.join(REV, 'journal'); fs.mkdirSync(jdir, { recursive: true });
    const f = path.join(jdir, 'Round2_Lesson_Check_Review.docx');
    fs.writeFileSync(f, await finalize(await Packer.toBuffer(round2Doc())));
    console.log(path.basename(f)); return;
  }
  const jdir = path.join(REV, 'journal');
  fs.mkdirSync(jdir, { recursive: true });
  const bySubj = {};
  for (const m of Object.keys(recs).sort(natural)) { const s = subjOf(m); if (s) (bySubj[s[1]] = bySubj[s[1]] || []).push(m); }
  const written = [];
  for (const [name, mods] of Object.entries(bySubj)) {
    const f = path.join(jdir, `Journal_${name.replace(/ /g, '_')}.docx`);
    fs.writeFileSync(f, await finalize(await Packer.toBuffer(volume(`${name}`, mods))));
    written.push(f);
    const ff = path.join(jdir, `Flagged_Items_${name.replace(/ /g, '_')}.docx`);
    fs.writeFileSync(ff, await finalize(await Packer.toBuffer(flaggedDoc(name, mods))));
    written.push(ff);
  }
  // master index
  const all = Object.values(recs).flat();
  const kids = [P([new TextRun({ text: 'Revision journal: master index', font: FONT, size: 40, bold: true, color: '1F3864' })], { after: 60 }),
    P('Grade 10 lesson plans, first revision 14 October 2026, rebuilt 10 November 2026 with Round 2. One journal per subject; this page totals them and lists the items needing a teacher decision.', { size: 20, after: 140 }), ...howTo()];
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
