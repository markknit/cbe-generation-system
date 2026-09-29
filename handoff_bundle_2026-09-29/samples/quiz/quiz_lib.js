// Quiz-only outputs per lesson (presentations deferred):
//   <prefix>_L<n>_QuickCheck.pptx  (+ .pdf via LibreOffice)  -- student-facing, projectable or printable
//   <prefix>_L<n>_AnswerKey.html   (+ .pdf via LibreOffice)  -- teacher-only
// Input: a lesson "quiz" array per the schema in the handoff:
//   { prompt, choices[4], correctIndex, rationale, phase, placement }
// Everything grade/subject-specific comes from `meta`; nothing is hardcoded.
const pptxgen = require("pptxgenjs");

const C = { darkBlue: "1F3864", teal: "1F6B75", lightTeal: "D9EEF1", white: "FFFFFF", quiz: "6A4C93", quizCard: "7C5CAA", ink: "1A1A1A" };
const FONT = "Arial";
const L = ["A", "B", "C", "D"];
// Attribution text comes from config/attribution.yaml (never hardcoded).
const ATTR_PATH = process.env.ATTRIBUTION_YAML || require("path").join(__dirname, "../../config/attribution.yaml");
function attribution() {
  const a = require("js-yaml").load(require("fs").readFileSync(ATTR_PATH, "utf8"));
  const year = a.year === "auto" ? String(new Date().getFullYear()) : String(a.year);
  const fill = (t) => t.replace(/\{YEAR\}/g, year);
  return { year, footer: fill(a.lesson_footer), license: a.license, header: a.substrand_header.map(h => ({ label: h.label, text: fill(h.text) })) };
}
const PHASE_LABEL = { predict: "Predict phase", observe: "Observe phase", explain: "Explain phase", dqb: "DQB phase", model: "Model Building phase", end: "End of lesson" };

function buildQuizDeck(meta, quiz, file) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  pres.title = `${meta.subject} Grade ${meta.grade} - ${meta.substrandName} - Lesson ${meta.lessonNumber} Quick Check`;

  // Title
  let s = pres.addSlide(); s.background = { color: C.darkBlue };
  s.addText(`${meta.subject.toUpperCase()} \u2014 GRADE ${meta.grade}  |  ${meta.substrandName.toUpperCase()}`, { x: 0.8, y: 1.8, w: 11.7, h: 0.5, fontFace: FONT, fontSize: 16, bold: true, color: "AFC8E8", charSpacing: 2, isTextBox: true, margin: 0 });
  s.addText("Quick Check", { x: 0.8, y: 2.35, w: 11.7, h: 1.0, fontFace: FONT, fontSize: 40, bold: true, color: C.white, isTextBox: true, margin: 0 });
  s.addText(`Lesson ${meta.lessonNumber}: ${meta.lessonTitle}`, { x: 0.8, y: 3.35, w: 11.7, h: 1.0, fontFace: FONT, fontSize: 20, color: C.lightTeal, valign: "top", isTextBox: true, margin: 0 });
  s.addText(`${quiz.length} multiple-choice questions  \u2022  choose A, B, C or D`, { x: 0.8, y: 4.5, w: 11.7, h: 0.5, fontFace: FONT, fontSize: 16, italic: true, color: "AFC8E8", isTextBox: true, margin: 0 });
  s.addText(`Sub-Strand ${meta.substrandId}: ${meta.substrandName}   |   Lesson ${meta.lessonNumber}`, { x: 0.8, y: 5.9, w: 11.7, h: 0.4, fontFace: FONT, fontSize: 13, color: "AFC8E8", isTextBox: true, margin: 0 });
  const A = attribution();
  s.addText(A.footer, { x: 0.8, y: 6.45, w: 11.7, h: 0.75, fontFace: FONT, fontSize: 9, color: "8FA8C8", valign: "top", isTextBox: true, margin: 0 });

  // One slide per question
  quiz.forEach((q, i) => {
    s = pres.addSlide(); s.background = { color: C.quiz };
    s.addText(`QUESTION ${i + 1} OF ${quiz.length}`, { x: 0.6, y: 0.4, w: 7, h: 0.4, fontFace: FONT, fontSize: 13, bold: true, color: "E0D6F0", charSpacing: 2, isTextBox: true, margin: 0 });
    // Teacher cue: which lesson-plan phase this question follows.
    s.addShape(pres.ShapeType.roundRect, { x: 8.9, y: 0.35, w: 3.8, h: 0.4, rectRadius: 0.06, fill: { color: "5A3F80" }, line: { type: "none" } });
    s.addText(`Use after: ${PHASE_LABEL[q.phase] || q.phase}`, { x: 8.9, y: 0.35, w: 3.8, h: 0.4, align: "center", valign: "middle", fontFace: FONT, fontSize: 11, italic: true, color: "E0D6F0", isTextBox: true, margin: 0 });
    s.addText(q.prompt, { x: 0.6, y: 0.95, w: 12.1, h: 1.35, fontFace: FONT, fontSize: 23, bold: true, color: C.white, valign: "middle", isTextBox: true, margin: 0 });
    q.choices.forEach((c, j) => {
      const y = 2.5 + j * 1.0;
      s.addShape(pres.ShapeType.roundRect, { x: 0.8, y, w: 11.7, h: 0.8, rectRadius: 0.08, fill: { color: C.quizCard }, line: { type: "none" } });
      s.addText(L[j], { x: 1.0, y, w: 0.6, h: 0.8, valign: "middle", fontFace: FONT, fontSize: 18, bold: true, color: C.white, isTextBox: true, margin: 0 });
      s.addText(c, { x: 1.7, y, w: 10.6, h: 0.8, valign: "middle", fontFace: FONT, fontSize: 17, color: C.white, isTextBox: true, margin: 0 });
    });
    s.addText(String(i + 2), { x: 12.6, y: 7.05, w: 0.5, h: 0.3, fontFace: FONT, fontSize: 10, color: "C9B8E0", align: "right", isTextBox: true, margin: 0 });
  });

  // Close (no collection method assumed)
  s = pres.addSlide(); s.background = { color: C.darkBlue };
  s.addText("All done", { x: 0.8, y: 2.4, w: 11.7, h: 0.9, fontFace: FONT, fontSize: 34, bold: true, color: C.white, isTextBox: true, margin: 0 });
  s.addText("Ask your teacher how to submit your answers today (for example, on a paper answer slip).", { x: 0.8, y: 3.4, w: 11.7, h: 0.8, fontFace: FONT, fontSize: 18, color: C.lightTeal, isTextBox: true, margin: 0 });
  return pres.writeFile({ fileName: file });
}

function answerKeyHtml(meta, quiz) {
  const esc = (t) => String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const rows = quiz.map((q, i) => `
<div class="q">
  <div class="where">Use after: ${esc(PHASE_LABEL[q.phase] || q.phase)} \u2014 ${esc(q.placement)}</div>
  <div class="prompt">Q${i + 1}. ${esc(q.prompt)}</div>
  <ol type="A">${q.choices.map((c, j) => `<li${j === q.correctIndex ? ' class="right"' : ""}>${esc(c)}</li>`).join("")}</ol>
  <div class="answer">Correct answer: ${L[q.correctIndex]}</div>
  <div class="rationale">${esc(q.rationale)}</div>
</div>`).join("");
  const quick = quiz.map((q, i) => `<td><b>${i + 1}</b><br>${L[q.correctIndex]}</td>`).join("");
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
</style></head><body>
<h1>Answer Key \u2014 ${esc(meta.subject)} Grade ${meta.grade}</h1>
<p class="meta">Sub-Strand ${esc(meta.substrandId)}: ${esc(meta.substrandName)} \u2022 Lesson ${meta.lessonNumber}: ${esc(meta.lessonTitle)}<br>
<b>Teacher reference only. Do not project or hand out.</b></p>
<p class="meta">Quick marking grid:</p>
<table class="grid"><tr>${quick}</tr></table>
${rows}
<p class="meta" style="margin-top:22px;border-top:1px solid #DDD;padding-top:8px;font-size:11px">${esc(attribution().footer).replace(/(https:\/\/creativecommons\.org\/licenses\/by-nc\/4\.0\/)/, '<a href="$1">$1</a>')}</p>
</body></html>`;
}

module.exports = { buildQuizDeck, answerKeyHtml, PHASE_LABEL, attribution };

// Printable answer key as .docx (converted to PDF with LibreOffice, same path the
// pipeline already uses for lesson plans).
function buildAnswerKeyDocx(meta, quiz, file) {
  const fs = require("fs");
  const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, BorderStyle, AlignmentType, ShadingType } = require("docx");
  const P = (runs, opts) => new Paragraph(Object.assign({ children: runs, spacing: { after: 80 } }, opts || {}));
  const R = (t, o) => new TextRun(Object.assign({ text: t, font: "Arial", size: 21 }, o || {}));
  const border = { style: BorderStyle.SINGLE, size: 4, color: "BBBBBB" };
  const cellW = Math.floor(9360 / quiz.length);
  const gridRow = (vals, bold) => new TableRow({ children: vals.map(v => new TableCell({
    width: { size: cellW, type: WidthType.DXA }, borders: { top: border, bottom: border, left: border, right: border },
    margins: { top: 60, bottom: 60, left: 80, right: 80 },
    shading: bold ? { fill: "D9EEF1", type: ShadingType.CLEAR } : undefined,
    children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [R(v, { bold: true })] })] })) });
  const children = [
    P([R(`Answer Key \u2014 ${meta.subject} Grade ${meta.grade}`, { bold: true, size: 32, color: "1F3864" })]),
    P([R(`Sub-Strand ${meta.substrandId}: ${meta.substrandName}  \u2022  Lesson ${meta.lessonNumber}: ${meta.lessonTitle}`, { size: 20, color: "444444" })]),
    P([R("Teacher reference only. Do not project or hand out.", { bold: true, size: 20 })], { spacing: { after: 200 } }),
    P([R("Quick marking grid", { bold: true })]),
    new Table({ width: { size: cellW * quiz.length, type: WidthType.DXA }, columnWidths: quiz.map(() => cellW),
      rows: [gridRow(quiz.map((_, i) => `Q${i + 1}`), true), gridRow(quiz.map(q => L[q.correctIndex]))] }),
    P([R("")], { spacing: { after: 120 } }),
  ];
  quiz.forEach((q, i) => {
    children.push(P([R(`USE AFTER: ${(PHASE_LABEL[q.phase] || q.phase).toUpperCase()} \u2014 ${q.placement}`, { size: 16, color: "1F6B75" })], { spacing: { before: 200, after: 40 }, keepNext: true }));
    children.push(P([R(`Q${i + 1}. ${q.prompt}`, { bold: true })], { keepNext: true }));
    q.choices.forEach((c, j) => children.push(P([R(`${L[j]}.  ${c}`, j === q.correctIndex ? { bold: true, color: "2E7D4F" } : {})], { indent: { left: 360 }, spacing: { after: 20 }, keepNext: true })));
    children.push(P([R(`Correct answer: ${L[q.correctIndex]}. `, { bold: true, color: "2E7D4F" }), R(q.rationale, { color: "444444", size: 19 })], { spacing: { before: 60, after: 120 } }));
  });
  children.push(P([R(attribution().footer, { size: 16, color: "666666" })], { spacing: { before: 300 } }));
  const doc = new Document({ sections: [{ properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1080, bottom: 1080, left: 1440, right: 1440 } } }, children }] });
  return Packer.toBuffer(doc).then(b => fs.writeFileSync(file, b));
}
module.exports.buildAnswerKeyDocx = buildAnswerKeyDocx;
