// Shared helpers for the v3 illustrative decks (content-first, process-integrated,
// inline quick checks). Same visual system as the Biology Lesson 2 example.
const pptxgen = require("pptxgenjs");

const C = {
  darkBlue: "1F3864", medBlue: "2E75B6", teal: "1F6B75",
  lightOrange: "FCE4D6", lightPurple: "EAD1F5", lightTeal: "D9EEF1", lightGreen: "D9F0DA",
  grey: "F2F2F2", white: "FFFFFF", ink: "1A1A1A", muted: "44546A",
  quiz: "6A4C93", quizCard: "7C5CAA",
};
const FONT = "Arial";

function makeDeck(title) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  pres.title = title;
  let n = 0;
  const quizLog = [];

  const base = (fill) => { const s = pres.addSlide(); s.background = { color: fill || C.white }; n++; return s; };
  const num = (s) => s.addText(String(n), { x: 12.6, y: 7.05, w: 0.5, h: 0.3, fontFace: FONT, fontSize: 10, color: "9AA5B1", align: "right", isTextBox: true, margin: 0 });
  const kicker = (s, t, color) => s.addText(t.toUpperCase(), { x: 0.6, y: 0.35, w: 10, h: 0.4, fontFace: FONT, fontSize: 13, bold: true, color: color || C.medBlue, charSpacing: 2, isTextBox: true, margin: 0 });
  const tag = (s, t) => {
    s.addShape(pres.ShapeType.roundRect, { x: 10.9, y: 0.35, w: 1.8, h: 0.35, rectRadius: 0.06, fill: { color: C.lightTeal }, line: { type: "none" } });
    s.addText(t, { x: 10.9, y: 0.35, w: 1.8, h: 0.35, align: "center", valign: "middle", fontFace: FONT, fontSize: 10, italic: true, color: C.teal, isTextBox: true, margin: 0 });
  };
  const headline = (s, t, size) => s.addText(t, { x: 0.6, y: 0.9, w: 12.1, h: 0.9, fontFace: FONT, fontSize: size || 26, bold: true, color: C.ink, valign: "middle", isTextBox: true, margin: 0 });
  const note = (s, t, y) => s.addText(t, { x: 0.6, y: y || 6.2, w: 12.1, h: 0.6, fontFace: FONT, fontSize: 15, italic: true, color: C.muted, isTextBox: true, margin: 0 });
  const box = (s, x, y, w, h, fill, line) => s.addShape(pres.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.08, fill: { color: fill }, line: line || { type: "none" } });

  function title(subjectLine, lessonTitle, subtitle, hook, footer) {
    const s = base(C.darkBlue);
    s.addText(subjectLine, { x: 0.8, y: 1.8, w: 11.7, h: 0.5, fontFace: FONT, fontSize: 16, color: "AFC8E8", bold: true, charSpacing: 2, isTextBox: true, margin: 0 });
    s.addText(lessonTitle, { x: 0.8, y: 2.35, w: 11.7, h: 1.0, fontFace: FONT, fontSize: 38, color: C.white, bold: true, isTextBox: true, margin: 0 });
    s.addText(subtitle, { x: 0.8, y: 3.35, w: 11.7, h: 0.6, fontFace: FONT, fontSize: 22, color: C.lightTeal, isTextBox: true, margin: 0 });
    s.addText(hook, { x: 0.8, y: 4.05, w: 11.7, h: 0.6, fontFace: FONT, fontSize: 15, italic: true, color: "AFC8E8", isTextBox: true, margin: 0 });
    s.addText(footer, { x: 0.8, y: 6.6, w: 11.7, h: 0.4, fontFace: FONT, fontSize: 13, color: "AFC8E8", isTextBox: true, margin: 0 });
    return s;
  }

  // Generic content slide: headline + panel with bullets or numbered steps.
  function panel(opts) {
    const s = base(C.white);
    if (opts.tag) tag(s, opts.tag);
    kicker(s, opts.kicker);
    headline(s, opts.headline, opts.headlineSize);
    const h = opts.panelH || 3.6;
    box(s, 0.6, 2.0, 12.1, h, opts.fill || C.grey);
    const dark = opts.fill === C.darkBlue;
    s.addText(opts.items.map((t, i) => ({
      text: opts.numbered ? `${i + 1}. ${t}` : t,
      options: { bullet: !opts.numbered, breakLine: i < opts.items.length - 1, color: dark ? C.white : C.ink, fontSize: opts.fontSize || 17 },
    })), { x: 1.0, y: 2.2, w: 11.3, h: h - 0.4, fontFace: FONT, isTextBox: true, margin: 0, paraSpaceAfter: 10, valign: "top" });
    if (opts.note) note(s, opts.note, 2.0 + h + 0.25);
    num(s);
    return s;
  }

  // Two cards side by side.
  function twoCol(opts) {
    const s = base(C.white);
    if (opts.tag) tag(s, opts.tag);
    kicker(s, opts.kicker);
    headline(s, opts.headline, opts.headlineSize);
    const h = opts.cardH || 3.2;
    opts.cols.forEach((c, i) => {
      const x = 0.6 + i * 6.15;
      box(s, x, 2.0, 5.85, h, c.fill || (i === 0 ? C.lightTeal : C.lightOrange));
      s.addText(c.h, { x: x + 0.35, y: 2.2, w: 5.2, h: 0.5, fontFace: FONT, fontSize: 19, bold: true, color: C.darkBlue, isTextBox: true, margin: 0 });
      s.addText(c.b, { x: x + 0.35, y: 2.8, w: 5.2, h: h - 1.0, fontFace: FONT, fontSize: c.size || 15, color: C.ink, valign: "top", isTextBox: true, margin: 0 });
    });
    if (opts.note) note(s, opts.note, 2.0 + h + 0.25);
    num(s);
    return s;
  }

  // Term/definition rows.
  function defs(opts) {
    const s = base(C.white);
    if (opts.tag) tag(s, opts.tag);
    kicker(s, opts.kicker);
    headline(s, opts.headline, opts.headlineSize);
    const rowH = opts.rowH || 1.3, gap = 0.2;
    opts.rows.forEach((r, i) => {
      const y = 2.0 + i * (rowH + gap);
      box(s, 0.6, y, 12.1, rowH, i % 2 === 0 ? C.lightTeal : C.grey);
      s.addText(r.term, { x: 1.0, y: y + 0.12, w: opts.termW || 2.8, h: rowH - 0.24, fontFace: FONT, fontSize: opts.termSize || 18, bold: true, color: C.darkBlue, valign: "middle", isTextBox: true, margin: 0 });
      const dx = 1.0 + (opts.termW || 2.8) + 0.2;
      s.addText(r.def, { x: dx, y: y + 0.12, w: 12.3 - dx, h: rowH - 0.24, fontFace: FONT, fontSize: opts.defSize || 15, color: C.ink, valign: "middle", isTextBox: true, margin: 0 });
    });
    if (opts.note) note(s, opts.note, 2.0 + opts.rows.length * (rowH + gap) + 0.05);
    num(s);
    return s;
  }

  // Grid table (e.g. indicator results, verification table).
  function table(opts) {
    const s = base(C.white);
    if (opts.tag) tag(s, opts.tag);
    kicker(s, opts.kicker);
    headline(s, opts.headline, opts.headlineSize);
    const rows = [opts.header.map((h) => ({ text: h, options: { bold: true, color: C.white, fill: { color: C.darkBlue }, align: "center" } }))]
      .concat(opts.rows.map((r, ri) => r.map((c, ci) => ({ text: c, options: { color: C.ink, fill: { color: ri % 2 ? C.white : C.grey }, bold: ci === 0, align: ci === 0 ? "left" : "center" } }))));
    s.addTable(rows, { x: 0.6, y: 2.0, w: 12.1, colW: opts.colW, fontFace: FONT, fontSize: opts.fontSize || 15, border: { type: "solid", pt: 1, color: "D0D5DD" }, rowH: opts.rowH || 0.5, valign: "middle" });
    if (opts.note) note(s, opts.note, opts.noteY || 6.1);
    num(s);
    return s;
  }

  // Inline quick check. Answer key is NOT placed in the deck or notes.
  function quick(q) {
    const s = base(C.quiz);
    quizLog.push(q);
    s.addText(`QUICK CHECK ${quizLog.length}`, { x: 0.6, y: 0.4, w: 12.1, h: 0.4, fontFace: FONT, fontSize: 13, bold: true, color: "E0D6F0", charSpacing: 2, isTextBox: true, margin: 0 });
    s.addText(q.prompt, { x: 0.6, y: 0.95, w: 12.1, h: 1.35, fontFace: FONT, fontSize: q.promptSize || 23, bold: true, color: C.white, valign: "middle", isTextBox: true, margin: 0 });
    ["A", "B", "C", "D"].forEach((L, i) => {
      const y = 2.5 + i * 1.0;
      box(s, 0.8, y, 11.7, 0.8, C.quizCard);
      s.addText(L, { x: 1.0, y, w: 0.6, h: 0.8, valign: "middle", fontFace: FONT, fontSize: 18, bold: true, color: C.white, isTextBox: true, margin: 0 });
      s.addText(q.choices[i], { x: 1.7, y, w: 10.6, h: 0.8, valign: "middle", fontFace: FONT, fontSize: 17, color: C.white, isTextBox: true, margin: 0 });
    });
    s.addText("Answer key is teacher-side only, in a separate file.", { x: 0.6, y: 6.6, w: 12.1, h: 0.4, fontFace: FONT, fontSize: 12, italic: true, color: "C9B8E0", isTextBox: true, margin: 0 });
    return s;
  }

  // Model update + DQB, combined on one slide.
  function modelDqb(modelText, dqbText) {
    const s = base(C.white);
    tag(s, "model + dqb");
    kicker(s, "Before We Finish");
    headline(s, "Update your model. Add one new question.");
    box(s, 0.6, 2.0, 5.85, 3.4, C.lightTeal);
    s.addText("UPDATE YOUR MODEL", { x: 0.85, y: 2.15, w: 5.4, h: 0.4, fontFace: FONT, fontSize: 13, bold: true, color: C.teal, isTextBox: true, margin: 0 });
    s.addText(modelText, { x: 0.85, y: 2.6, w: 5.4, h: 2.7, fontFace: FONT, fontSize: 15, color: C.ink, valign: "top", isTextBox: true, margin: 0 });
    box(s, 6.65, 2.0, 6.05, 3.4, "FFF6D9", { color: "E8D68A", width: 1 });
    s.addText("DRIVING QUESTION BOARD", { x: 6.9, y: 2.15, w: 5.6, h: 0.4, fontFace: FONT, fontSize: 13, bold: true, color: "8A6D00", isTextBox: true, margin: 0 });
    s.addText(dqbText, { x: 6.9, y: 2.6, w: 5.6, h: 2.7, fontFace: FONT, fontSize: 15, color: "5A4A00", valign: "top", isTextBox: true, margin: 0 });
    num(s);
    return s;
  }

  // Resources with real, clickable ares.local links. status: "ok" | "weak"
  function resources(items) {
    const s = base(C.white);
    kicker(s, "Resources for Today");
    headline(s, "From the ARES offline library", 24);
    items.forEach((it, i) => {
      const y = 1.95 + i * 1.45;
      const weak = it.status === "weak";
      box(s, 0.6, y, 12.1, 1.25, weak ? "FFF3E0" : C.grey);
      s.addText(it.icon, { x: 0.9, y: y + 0.15, w: 0.7, h: 0.95, fontFace: FONT, fontSize: 24, color: weak ? "C77700" : C.medBlue, valign: "middle", isTextBox: true, margin: 0 });
      const runs = [
        { text: it.label + "  ", options: { bold: true, color: C.darkBlue, fontSize: 13 } },
        { text: it.title, options: { color: C.teal, fontSize: 16, underline: true, hyperlink: { url: it.url }, breakLine: true } },
        { text: it.sub, options: { color: weak ? "8A5300" : "6B7280", fontSize: 12, italic: true } },
      ];
      s.addText(runs, { x: 1.7, y: y + 0.12, w: 10.8, h: 1.0, fontFace: FONT, isTextBox: true, margin: 0, valign: "middle" });
    });
    s.addText("Links open only on the school network (ares.local). Click to open during the lesson.", { x: 0.6, y: 6.5, w: 12.1, h: 0.4, fontFace: FONT, fontSize: 12, italic: true, color: "6B7280", isTextBox: true, margin: 0 });
    num(s);
    return s;
  }

  function summary() {
    const s = base(C.darkBlue);
    kicker(s, "Today's Quick Checks", "AFC8E8");
    s.addText(`${quizLog.length} questions asked during class today`, { x: 0.8, y: 1.0, w: 11.7, h: 0.7, fontFace: FONT, fontSize: 26, bold: true, color: C.white, isTextBox: true, margin: 0 });
    s.addText(quizLog.map((q, i) => ({ text: `${i + 1}. ${q.short || q.prompt}`, options: { breakLine: i < quizLog.length - 1 } })),
      { x: 0.8, y: 1.9, w: 11.7, h: 3.6, fontFace: FONT, fontSize: 16, color: "DCE6F2", isTextBox: true, margin: 0, paraSpaceAfter: 8, valign: "top" });
    s.addText("Ask your teacher how to submit your answers today (for example, on a paper answer slip).", { x: 0.8, y: 5.9, w: 11.7, h: 0.6, fontFace: FONT, fontSize: 15, italic: true, color: C.lightTeal, isTextBox: true, margin: 0 });
    return s;
  }

  function save(file) { require("fs").writeFileSync(file.replace(/\.pptx$/, "_quiz.json"), JSON.stringify(quizLog, null, 1)); return pres.writeFile({ fileName: file }); }

  return { pres, C, FONT, base, num, kicker, tag, headline, note, box, title, panel, twoCol, defs, table, quick, modelDqb, resources, summary, save, quizLog };
}

// Teacher-side answer key (open in a separate window while presenting).
function answerKeyHtml(meta, quizLog) {
  const esc = (t) => String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const L = ["A", "B", "C", "D"];
  const qs = quizLog.map((q, i) => `
<div class="q">
  <div class="where">Asked after: ${esc(q.placement)}</div>
  <div class="prompt">Q${i + 1}. ${esc(q.prompt)}</div>
  <ol type="A">${q.choices.map((c, j) => `<li${j === q.correct ? ' class="right"' : ""}>${esc(c)}</li>`).join("")}</ol>
  <div class="answer">Correct: ${L[q.correct]}</div>
  <div class="rationale">${esc(q.rationale)}</div>
</div>`).join("");
  return `<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Answer Key: ${esc(meta.title)}</title>
<style>
 body{font-family:Arial,sans-serif;max-width:760px;margin:32px auto;padding:0 16px;color:#1A1A1A;background:#FAFAF8}
 h1{color:#1F3864;font-size:22px;margin-bottom:4px}.meta{color:#666;font-size:13px;margin-bottom:24px}
 .q{background:#fff;border:1px solid #E0DCD0;border-radius:8px;padding:14px 20px;margin-bottom:14px}
 .where{font-size:12px;color:#1F6B75;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px}
 .prompt{font-weight:bold;margin-bottom:6px}ol{margin:6px 0 8px 0}li.right{font-weight:bold;color:#2E7D4F}
 .answer{color:#2E7D4F;font-weight:bold}.rationale{color:#555;font-size:14px;margin-top:4px}
</style></head><body>
<h1>Answer Key: ${esc(meta.title)}</h1>
<p class="meta">${esc(meta.subtitle)}<br>Teacher reference only. Keep this open in a separate window or tab while presenting. Do not project.</p>
${qs}
<p class="meta">Illustrative example, hand-built from the generated lesson data. Production versions would be generated from LESSONS[i].quiz.</p>
</body></html>`;
}

module.exports = { makeDeck, answerKeyHtml, C };
