#!/usr/bin/env node
/**
 * build_quiz.js — render Quick Check quizzes from <prefix>_quiz.json
 * ===================================================================
 * Per lesson, into <sub-strand output dir>/quiz/ (grade-aware: follows the
 * sub-strand's own outputDir, flat for Grade 10, Grade<N>/ for later grades):
 *   <Subject>_G<grade>_SS<id>_<Name>_L<n>_QuickCheck.pptx   student-facing
 *   <Subject>_G<grade>_SS<id>_<Name>_L<n>_AnswerKey.html    teacher, second window
 *   <Subject>_G<grade>_SS<id>_<Name>_L<n>_AnswerKey.docx    teacher, printable
 * PDFs of the .pptx and .docx come from generate_pdfs.js (same LibreOffice
 * path as the lesson plans; LibreOffice's HTML->PDF is poor, hence the docx).
 * The .html is also copied into the PDF distribution tree for teachers.
 *
 * Answers never appear in the student deck, including speaker notes.
 * Every run is gated by scripts/validate_quiz.py: an invalid quiz is not rendered.
 * Attribution comes only from config/attribution.yaml (lib/attribution.js).
 * Reference design: handoff_bundle_2026-09-29/samples/quiz/.
 *
 * Usage:
 *   node generators/build_quiz.js                 # every *_quiz.json under data/outputs/v2
 *   node generators/build_quiz.js PATH/X_quiz.json [...]
 *   --lessons 2,4   only these lesson numbers
 *   --pdf           also convert this run's .pptx/.docx to PDF now (for review)
 */
'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');
const pptxgen = require('pptxgenjs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, BorderStyle, AlignmentType, ShadingType,
} = require('docx');
const { attribution, linkedRuns } = require('./lib/attribution');

const V2_ROOT = path.join(__dirname, '..', 'data', 'outputs', 'v2');
const PDF_ROOT = path.join(V2_ROOT, 'PDF');
const L = ['A', 'B', 'C', 'D'];
const FONT = 'Arial';
const C = { darkBlue: '1F3864', teal: '1F6B75', lightTeal: 'D9EEF1', white: 'FFFFFF',
            quiz: '6A4C93', quizCard: '7C5CAA' };
const PHASE_LABEL = { predict: 'Predict phase', observe: 'Observe phase', explain: 'Explain phase',
                      dqb: 'DQB phase', model: 'Model Building phase', end: 'End of lesson' };

const slug = s => String(s).replace(/[^A-Za-z0-9]+/g, '_').replace(/^_|_$/g, '');

function lessonMeta(qf, lesson) {
  const m = qf.meta;
  return { subject: m.subject, grade: m.grade, substrandId: m.substrandId, substrandName: m.substrandName,
           lessonNumber: lesson.number, lessonTitle: lesson.title,
           stem: `${slug(m.subject)}_G${m.grade}_SS${m.substrandId}_${slug(m.substrandName)}_L${lesson.number}` };
}

// Font size by length: LibreOffice (our PDF path) ignores PowerPoint auto-shrink.
const promptSize = t => (t.length > 260 ? 16 : t.length > 190 ? 18 : t.length > 120 ? 20 : 23);
const choiceSize = longest => (longest > 110 ? 13 : longest > 80 ? 15 : 17);

function footerTextRuns(size, color) {
  const A = attribution();
  const parts = A.footer.split(A.license.name);
  const runs = [];
  parts.forEach((p, i) => {
    if (p) runs.push({ text: p, options: { fontFace: FONT, fontSize: size, color } });
    if (i < parts.length - 1) {
      runs.push({ text: A.license.name, options: { fontFace: FONT, fontSize: size, color: 'AFC8E8',
                  underline: true, hyperlink: { url: A.license.url } } });
    }
  });
  return runs;
}

function buildDeck(meta, quiz, file) {
  const pres = new pptxgen();
  pres.layout = 'LAYOUT_WIDE';
  pres.title = `${meta.subject} Grade ${meta.grade} - ${meta.substrandName} - Lesson ${meta.lessonNumber} Quick Check`;

  let s = pres.addSlide();
  s.background = { color: C.darkBlue };
  s.addText(`${meta.subject.toUpperCase()} — GRADE ${meta.grade}  |  ${meta.substrandName.toUpperCase()}`,
    { x: 0.8, y: 1.6, w: 11.7, h: 0.5, fontFace: FONT, fontSize: 16, bold: true, color: 'AFC8E8', charSpacing: 2, margin: 0 });
  s.addText('Quick Check', { x: 0.8, y: 2.15, w: 11.7, h: 1.0, fontFace: FONT, fontSize: 40, bold: true, color: C.white, margin: 0 });
  s.addText(`Lesson ${meta.lessonNumber}: ${meta.lessonTitle}`,
    { x: 0.8, y: 3.15, w: 11.7, h: 1.2, fontFace: FONT, fontSize: meta.lessonTitle.length > 90 ? 16 : 20,
      color: C.lightTeal, valign: 'top', margin: 0 });
  s.addText(`${quiz.length} multiple-choice questions  •  choose A, B, C or D`,
    { x: 0.8, y: 4.5, w: 11.7, h: 0.5, fontFace: FONT, fontSize: 16, italic: true, color: 'AFC8E8', margin: 0 });
  s.addText(`Sub-Strand ${meta.substrandId}: ${meta.substrandName}   |   Lesson ${meta.lessonNumber}`,
    { x: 0.8, y: 5.75, w: 11.7, h: 0.4, fontFace: FONT, fontSize: 13, color: 'AFC8E8', margin: 0 });
  s.addText(footerTextRuns(9, '8FA8C8'), { x: 0.8, y: 6.3, w: 11.7, h: 0.9, valign: 'top', margin: 0 });

  quiz.forEach((q, i) => {
    s = pres.addSlide();
    s.background = { color: C.quiz };
    s.addText(`QUESTION ${i + 1} OF ${quiz.length}`,
      { x: 0.6, y: 0.4, w: 7, h: 0.4, fontFace: FONT, fontSize: 13, bold: true, color: 'E0D6F0', charSpacing: 2, margin: 0 });
    s.addShape(pres.ShapeType.roundRect, { x: 8.9, y: 0.35, w: 3.8, h: 0.4, rectRadius: 0.06,
      fill: { color: '5A3F80' }, line: { type: 'none' } });
    s.addText(`Use after: ${PHASE_LABEL[q.phase] || q.phase}`, { x: 8.9, y: 0.35, w: 3.8, h: 0.4, align: 'center',
      valign: 'middle', fontFace: FONT, fontSize: 11, italic: true, color: 'E0D6F0', margin: 0 });
    s.addText(q.prompt, { x: 0.6, y: 0.95, w: 12.1, h: 1.45, fontFace: FONT, fontSize: promptSize(q.prompt),
      bold: true, color: C.white, valign: 'middle', margin: 0 });
    const cs = choiceSize(Math.max(...q.choices.map(c => c.length)));
    q.choices.forEach((c, j) => {
      const y = 2.55 + j * 1.0;
      s.addShape(pres.ShapeType.roundRect, { x: 0.8, y, w: 11.7, h: 0.85, rectRadius: 0.08,
        fill: { color: C.quizCard }, line: { type: 'none' } });
      s.addText(L[j], { x: 1.0, y, w: 0.6, h: 0.85, valign: 'middle', fontFace: FONT, fontSize: 18, bold: true,
        color: C.white, margin: 0 });
      s.addText(c, { x: 1.7, y, w: 10.6, h: 0.85, valign: 'middle', fontFace: FONT, fontSize: cs, color: C.white, margin: 0 });
    });
    s.addText(String(i + 2), { x: 12.6, y: 7.05, w: 0.5, h: 0.3, fontFace: FONT, fontSize: 10, color: 'C9B8E0',
      align: 'right', margin: 0 });
  });

  s = pres.addSlide();
  s.background = { color: C.darkBlue };
  s.addText('All done', { x: 0.8, y: 2.4, w: 11.7, h: 0.9, fontFace: FONT, fontSize: 34, bold: true, color: C.white, margin: 0 });
  s.addText('Ask your teacher how to submit your answers today (for example, on a paper answer slip).',
    { x: 0.8, y: 3.4, w: 11.7, h: 0.8, fontFace: FONT, fontSize: 18, color: C.lightTeal, margin: 0 });
  return pres.writeFile({ fileName: file });
}

function answerKeyHtml(meta, quiz) {
  const A = attribution();
  const esc = t => String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const rows = quiz.map((q, i) => `
<div class="q">
  <div class="where">Use after: ${esc(PHASE_LABEL[q.phase] || q.phase)} — ${esc(q.placement)}</div>
  <div class="prompt">Q${i + 1}. ${esc(q.prompt)}</div>
  <ol type="A">${q.choices.map((c, j) => `<li${j === q.correctIndex ? ' class="right"' : ''}>${esc(c)}</li>`).join('')}</ol>
  <div class="answer">Correct answer: ${L[q.correctIndex]}</div>
  <div class="rationale">${esc(q.rationale)}</div>
</div>`).join('');
  const quick = quiz.map((q, i) => `<td><b>${i + 1}</b><br>${L[q.correctIndex]}</td>`).join('');
  const footer = esc(A.footer)
    .replace(esc(A.license.url), `<a href="${A.license.url}">${esc(A.license.url)}</a>`)
    .replace(esc(A.license.name), `<a href="${A.license.url}">${esc(A.license.name)}</a>`);
  return `<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Answer Key: ${esc(meta.subject)} G${meta.grade} ${esc(meta.substrandName)} L${meta.lessonNumber}</title>
<style>
 body{font-family:Arial,sans-serif;max-width:760px;margin:28px auto;padding:0 16px;color:#1A1A1A}
 h1{color:#1F3864;font-size:21px;margin-bottom:2px}.meta{color:#555;font-size:13px;margin:4px 0 14px}
 table.grid{border-collapse:collapse;margin:6px 0 18px}table.grid td{border:1px solid #BBB;padding:6px 14px;text-align:center;font-size:15px}
 .q{border:1px solid #D8D8D8;border-radius:6px;padding:12px 18px;margin-bottom:12px;page-break-inside:avoid}
 .where{font-size:11px;color:#1F6B75;text-transform:uppercase;letter-spacing:1px;margin-bottom:5px}
 .prompt{font-weight:bold;margin-bottom:4px}ol{margin:4px 0 6px}li.right{font-weight:bold;color:#2E7D4F}
 .answer{color:#2E7D4F;font-weight:bold}.rationale{color:#444;font-size:13px;margin-top:3px}
 .attr{margin-top:22px;border-top:1px solid #DDD;padding-top:8px;font-size:11px;color:#555}
</style></head><body>
<h1>Answer Key — ${esc(meta.subject)} Grade ${meta.grade}</h1>
<p class="meta">Sub-Strand ${esc(meta.substrandId)}: ${esc(meta.substrandName)} • Lesson ${meta.lessonNumber}: ${esc(meta.lessonTitle)}<br>
<b>Teacher reference only. Do not project or hand out.</b></p>
<p class="meta">Quick marking grid:</p>
<table class="grid"><tr>${quick}</tr></table>
${rows}
<p class="attr">${footer}</p>
</body></html>
`;
}

function buildAnswerKeyDocx(meta, quiz, file) {
  const P = (runs, opts) => new Paragraph(Object.assign({ children: runs, spacing: { after: 80 } }, opts || {}));
  const R = (t, o) => new TextRun(Object.assign({ text: t, font: FONT, size: 21 }, o || {}));
  const border = { style: BorderStyle.SINGLE, size: 4, color: 'BBBBBB' };
  const cellW = Math.floor(9360 / quiz.length);
  const gridRow = (vals, head) => new TableRow({ children: vals.map(v => new TableCell({
    width: { size: cellW, type: WidthType.DXA }, borders: { top: border, bottom: border, left: border, right: border },
    margins: { top: 60, bottom: 60, left: 80, right: 80 },
    shading: head ? { fill: 'D9EEF1', type: ShadingType.CLEAR } : undefined,
    children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [R(v, { bold: true })] })] })) });
  const children = [
    P([R(`Answer Key — ${meta.subject} Grade ${meta.grade}`, { bold: true, size: 32, color: '1F3864' })]),
    P([R(`Sub-Strand ${meta.substrandId}: ${meta.substrandName}  •  Lesson ${meta.lessonNumber}: ${meta.lessonTitle}`,
      { size: 20, color: '444444' })]),
    P([R('Teacher reference only. Do not project or hand out.', { bold: true, size: 20 })], { spacing: { after: 200 } }),
    P([R('Quick marking grid', { bold: true })]),
    new Table({ width: { size: cellW * quiz.length, type: WidthType.DXA }, columnWidths: quiz.map(() => cellW),
      rows: [gridRow(quiz.map((_, i) => `Q${i + 1}`), true), gridRow(quiz.map(q => L[q.correctIndex]))] }),
    P([R('')], { spacing: { after: 120 } }),
  ];
  quiz.forEach((q, i) => {
    children.push(P([R(`USE AFTER: ${(PHASE_LABEL[q.phase] || q.phase).toUpperCase()} — ${q.placement}`,
      { size: 16, color: '1F6B75' })], { spacing: { before: 200, after: 40 }, keepNext: true }));
    children.push(P([R(`Q${i + 1}. ${q.prompt}`, { bold: true })], { keepNext: true }));
    q.choices.forEach((c, j) => children.push(P([R(`${L[j]}.  ${c}`,
      j === q.correctIndex ? { bold: true, color: '2E7D4F' } : {})], { indent: { left: 360 }, spacing: { after: 20 }, keepNext: true })));
    children.push(P([R(`Correct answer: ${L[q.correctIndex]}. `, { bold: true, color: '2E7D4F' }),
      R(q.rationale, { color: '444444', size: 19 })], { spacing: { before: 60, after: 120 } }));
  });
  children.push(new Paragraph({ spacing: { before: 300 },
    border: { top: { style: BorderStyle.SINGLE, size: 4, color: 'BBBBBB', space: 4 } },
    children: linkedRuns(attribution().footer, { size: 16, font: FONT, color: '666666' }) }));
  const doc = new Document({ sections: [{ properties: { page: { size: { width: 12240, height: 15840 },
    margin: { top: 1080, bottom: 1080, left: 1440, right: 1440 } } }, children }] });
  return Packer.toBuffer(doc).then(b => fs.writeFileSync(file, b));
}

function toPdf(files) {
  const byDir = new Map();
  for (const f of files) {
    const dest = path.join(PDF_ROOT, path.relative(V2_ROOT, path.dirname(f)));
    if (!byDir.has(dest)) byDir.set(dest, []);
    byDir.get(dest).push(f);
  }
  const profile = path.join(os.tmpdir(), 'lo_profile_pdfgen');
  for (const [dest, list] of byDir) {
    fs.mkdirSync(dest, { recursive: true });
    const r = spawnSync('soffice', [`-env:UserInstallation=file://${profile}`, '--headless', '--norestore',
      '--convert-to', 'pdf', '--outdir', dest, ...list], { stdio: 'ignore', timeout: 10 * 60 * 1000 });
    if (r.status !== 0) throw new Error(`soffice failed for ${dest}`);
  }
}

async function main() {
  const argv = process.argv.slice(2);
  const opt = n => { const i = argv.indexOf(n); return i >= 0 ? argv[i + 1] : null; };
  const lessonsWanted = opt('--lessons') ? new Set(opt('--lessons').split(',').map(Number)) : null;
  const skip = new Set([opt('--lessons')]);
  let inputs = argv.filter(a => !a.startsWith('--') && !skip.has(a));
  if (!inputs.length) {
    const walk = d => fs.readdirSync(d, { withFileTypes: true }).flatMap(e => {
      const f = path.join(d, e.name);
      if (f === PDF_ROOT) return [];
      return e.isDirectory() ? walk(f) : (/_quiz\.json$/.test(e.name) ? [f] : []);
    });
    inputs = walk(V2_ROOT);
  }
  // Gate: never render a quiz that fails validation (scripts/validate_quiz.py).
  const py = fs.existsSync(path.join(__dirname, '..', 'venv', 'bin', 'python3'))
    ? path.join(__dirname, '..', 'venv', 'bin', 'python3') : 'python3';
  const v = spawnSync(py, [path.join(__dirname, '..', 'scripts', 'validate_quiz.py'), ...inputs], { encoding: 'utf8' });
  const summary = (v.stdout || '').split('\n').filter(l => /validate_quiz:|answer letters|failure/.test(l)).join('\n');
  console.log(summary);
  if (v.status !== 0) {
    console.error((v.stdout || '').split('\n').filter(l => l.includes('FAIL')).join('\n'));
    console.error('Quiz validation FAILED; nothing rendered.');
    process.exit(1);
  }
  const made = [];
  for (const qfPath of inputs) {
    const qf = JSON.parse(fs.readFileSync(qfPath, 'utf8'));
    const outDir = path.join(path.dirname(qfPath), 'quiz');
    fs.mkdirSync(outDir, { recursive: true });
    const pdfDir = path.join(PDF_ROOT, path.relative(V2_ROOT, outDir));
    for (const lesson of qf.lessons) {
      if (lessonsWanted && !lessonsWanted.has(lesson.number)) continue;
      const meta = lessonMeta(qf, lesson);
      const base = path.join(outDir, meta.stem);
      await buildDeck(meta, lesson.quiz, `${base}_QuickCheck.pptx`);
      const html = answerKeyHtml(meta, lesson.quiz);
      fs.writeFileSync(`${base}_AnswerKey.html`, html);
      fs.mkdirSync(pdfDir, { recursive: true });
      fs.writeFileSync(path.join(pdfDir, `${meta.stem}_AnswerKey.html`), html);
      await buildAnswerKeyDocx(meta, lesson.quiz, `${base}_AnswerKey.docx`);
      made.push(`${base}_QuickCheck.pptx`, `${base}_AnswerKey.docx`);
      console.log(`  built ${path.relative(V2_ROOT, base)} (${lesson.quiz.length} questions)`);
    }
  }
  if (argv.includes('--pdf') && made.length) {
    toPdf(made);
    console.log(`  converted ${made.length} file(s) to PDF under ${path.relative(process.cwd(), PDF_ROOT)}`);
  }
}

main().catch(e => { console.error(e); process.exit(1); });
