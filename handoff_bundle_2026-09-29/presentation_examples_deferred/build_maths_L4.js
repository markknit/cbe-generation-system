// Illustrative v3: Mathematics G10, Sub-Strand 3.1 Trigonometry I, Lesson 4
// "Tangent and the Sine-Cosine-Tangent Relationship: Solving the Mango-Tree Problem".
// Content from data/outputs/v2/Maths/SS3.1_Trigonometry_I/*_data.json (LESSONS[3]).
const fs = require("fs");
const { makeDeck, answerKeyHtml, C } = require("./lib_v3");
const src = JSON.parse(fs.readFileSync("/home/claude/Maths_L4.json", "utf8"));
const rl = src.lesson.resourceLinks.predict;

const d = makeDeck("Mathematics G10 - Trigonometry I - Lesson 4 (illustrative v3)");
const { pres, FONT } = d;

// Right triangle: right angle at bottom-right (tree), angle theta at bottom-left (shadow tip).
function triangle(s, x, y, w, h, labels) {
  s.addShape(pres.ShapeType.rtTriangle, { x, y, w, h, flipH: true, fill: { color: "EAF3FB" }, line: { color: C.darkBlue, width: 2 } });
  s.addShape(pres.ShapeType.rect, { x: x + w - 0.3, y: y + h - 0.3, w: 0.3, h: 0.3, fill: { type: "none" }, line: { color: C.darkBlue, width: 1.25 } });
  const t = (txt, tx, ty, tw, opts) => s.addText(txt, Object.assign({ x: tx, y: ty, w: tw, h: 0.45, fontFace: FONT, fontSize: 16, color: C.darkBlue, bold: true, isTextBox: true, margin: 0 }, opts || {}));
  t(labels.theta, x + 0.25, y + h - 0.5, 1.4);
  t(labels.opp, x + w + 0.15, y + h / 2 - 0.45, 1.9, { h: 0.9 });
  t(labels.adj, x + w / 2 - 1.3, y + h + 0.1, 2.6, { align: "center" });
  t(labels.hyp, x + w / 2 - 2.2, y + h / 2 - 0.75, 2.2, { align: "right" });
}

d.title("MATHEMATICS \u2014 GRADE 10  |  TRIGONOMETRY I", "The Tangent Ratio",
  "Solving the mango-tree problem",
  "Today we calculate the height of the Kisumu mango tree for the first time.",
  "Sub-Strand 3.1: Trigonometry I   |   Lesson 4   |   80 minutes");

// Predict slide with the scenario and diagram
{
  const s = d.base(C.white);
  d.tag(s, "predict");
  d.kicker(s, "The Problem");
  d.headline(s, "How tall is the mango tree?");
  triangle(s, 0.9, 2.2, 4.6, 3.3, { theta: "53\u00B0", opp: "tree height\nh = ?", adj: "shadow  9.0 m", hyp: "sun ray" });
  d.box(s, 7.9, 2.0, 4.8, 3.8, C.grey);
  s.addText([
    { text: "A student in Kisumu measures:", options: { bold: true, breakLine: true } },
    { text: "\u2022 Sun angle: 53\u00B0", options: { breakLine: true } },
    { text: "\u2022 Tree\u2019s shadow: 9.0 m", options: { breakLine: true } },
    { text: "\u2022 From last lesson: sin 53\u00B0 \u2248 0.799, cos 53\u00B0 \u2248 0.602", options: { breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "Predict: which ratio will help most? Estimate the height.", options: { italic: true } },
  ], { x: 8.15, y: 2.2, w: 4.35, h: 3.4, fontFace: FONT, fontSize: 15, color: C.ink, valign: "top", isTextBox: true, margin: 0, paraSpaceAfter: 6 });
  d.note(s, "Write your prediction silently (2 minutes), then share with your partner.", 6.2);
  d.num(s);
}

// Recall sine and cosine
{
  const s = d.base(C.white);
  d.tag(s, "observe");
  d.kicker(s, "What We Already Know");
  d.headline(s, "Sine and cosine compare sides with the hypotenuse.");
  triangle(s, 0.9, 2.2, 4.8, 3.0, { theta: "\u03B8", opp: "Opposite (O)", adj: "Adjacent (A)", hyp: "Hypotenuse (H)" });
  d.box(s, 7.9, 2.0, 4.8, 3.6, C.lightTeal);
  s.addText([
    { text: "sin \u03B8 = O / H", options: { bold: true, fontSize: 24, breakLine: true } },
    { text: " ", options: { fontSize: 10, breakLine: true } },
    { text: "cos \u03B8 = A / H", options: { bold: true, fontSize: 24, breakLine: true } },
    { text: " ", options: { fontSize: 10, breakLine: true } },
    { text: "Opposite: the side facing the angle. Adjacent: the side next to the angle (not the hypotenuse).", options: { fontSize: 14 } },
  ], { x: 8.2, y: 2.25, w: 4.3, h: 3.2, fontFace: FONT, color: C.darkBlue, valign: "top", isTextBox: true, margin: 0 });
  d.note(s, "Problem: the hypotenuse is the sun ray. We can\u2019t measure it with a tape measure. We need a ratio that skips it.", 6.1);
  d.num(s);
}

d.panel({ tag: "observe", kicker: "Derivation", headline: "Divide sine by cosine and watch H disappear.",
  fill: C.darkBlue, panelH: 3.3, numbered: true, fontSize: 21,
  items: [
    "sin \u03B8 \u00F7 cos \u03B8  =  (O/H) \u00F7 (A/H)",
    "=  (O/H) \u00D7 (H/A)       (dividing by a fraction = multiplying by its reciprocal)",
    "=  O / A       (the H\u2019s cancel)",
    "So  tan \u03B8 = sin \u03B8 / cos \u03B8  =  Opposite / Adjacent",
  ], note: "Copy each step and draw arrows showing where H cancels. Memory aid: TOA \u2014 Tan = Opposite / Adjacent." });

d.quick({ placement: "Derivation of tan \u03B8",
  prompt: "In a right-angled triangle, which ratio equals tan \u03B8?",
  short: "Which ratio equals tan \u03B8?",
  choices: ["Opposite / Hypotenuse", "Adjacent / Hypotenuse", "Opposite / Adjacent", "Hypotenuse / Opposite"],
  correct: 2, rationale: "tan \u03B8 = O/A. O/H is sin \u03B8 and A/H is cos \u03B8. It follows from sin \u03B8 \u00F7 cos \u03B8 with H cancelling." });

d.table({ tag: "observe", kicker: "Check It With Tables (pairs)", headline: "Does sin \u03B8 \u00F7 cos \u03B8 really equal tan \u03B8?",
  header: ["\u03B8", "sin \u03B8", "cos \u03B8", "sin \u03B8 \u00F7 cos \u03B8", "tan \u03B8 (tables)", "Match?"],
  colW: [1.5, 2.0, 2.0, 2.4, 2.4, 1.8], rowH: 0.6, fontSize: 16,
  rows: [
    ["30\u00B0", "0.5000", "0.8660", "0.5774", "0.5774", "\u2713"],
    ["40\u00B0", "0.6428", "0.7660", "0.8391", "0.8391", "\u2713"],
    ["60\u00B0", "", "", "", "", ""],
    ["70\u00B0", "", "", "", "", ""],
  ], note: "Your turn: complete the rows for 60\u00B0 and 70\u00B0 using your mathematical tables. Small differences in the last digit come from rounding.", noteY: 5.3 });

d.quick({ placement: "Verification table (60\u00B0 row)",
  prompt: "sin 60\u00B0 = 0.8660 and cos 60\u00B0 = 0.5000. Use tan \u03B8 = sin \u03B8 / cos \u03B8 to find tan 60\u00B0.",
  short: "sin 60\u00B0 = 0.8660, cos 60\u00B0 = 0.5000. Find tan 60\u00B0.",
  choices: ["0.5774", "1.7320", "0.4330", "1.3660"],
  correct: 1, rationale: "0.8660 \u00F7 0.5000 = 1.7320, which matches tan 60\u00B0 in the tables (1.7321 to four decimal places). 0.5774 is the reciprocal (cos \u00F7 sin); 0.4330 is the product." });

d.twoCol({ tag: "explain", kicker: "Think, Then Discuss", headline: "Back to the mango tree",
  cols: [
    { h: "Which side is 9.0 m?", b: "Stand at the shadow tip and look at the 53\u00B0 angle. Is the shadow the side facing the angle, or the side next to it?" },
    { h: "What are we looking for?", b: "The tree height h faces the 53\u00B0 angle. Which ratio uses both the side we know and the side we want \u2014 without the hypotenuse?" },
  ], cardH: 2.7, note: "30 seconds of silent thinking, then discuss in groups of four." });

d.quick({ placement: "Discussion: labelling the mango-tree triangle",
  prompt: "Relative to the 53\u00B0 angle, the 9.0 m shadow is the triangle\u2019s \u2026",
  short: "Relative to the 53\u00B0 angle, the 9.0 m shadow is the \u2026",
  choices: ["Opposite side", "Adjacent side", "Hypotenuse", "It depends on how tall the tree is"],
  correct: 1, rationale: "The shadow lies next to the 53\u00B0 angle and is not the hypotenuse, so it is the adjacent side. The tree height is opposite; the sun ray is the hypotenuse." });

{
  const s = d.base(C.white);
  d.tag(s, "explain");
  d.kicker(s, "Solve It");
  d.headline(s, "The mango tree is about 12 metres tall.");
  d.box(s, 0.6, 2.0, 6.0, 3.6, C.lightTeal);
  s.addText([
    { text: "Method 1: tangent ratio", options: { bold: true, fontSize: 18, breakLine: true } },
    { text: "tan 53\u00B0 = h / 9.0", options: { breakLine: true } },
    { text: "h = 9.0 \u00D7 tan 53\u00B0", options: { breakLine: true } },
    { text: "h = 9.0 \u00D7 1.3270", options: { breakLine: true } },
    { text: "h \u2248 11.94 m", options: { bold: true } },
  ], { x: 0.9, y: 2.2, w: 5.5, h: 3.2, fontFace: FONT, fontSize: 17, color: C.darkBlue, valign: "top", isTextBox: true, margin: 0, paraSpaceAfter: 6 });
  d.box(s, 6.8, 2.0, 5.9, 3.6, C.lightGreen);
  s.addText([
    { text: "Method 2: similar triangles (earlier lessons)", options: { bold: true, fontSize: 18, breakLine: true } },
    { text: "Student: 1.6 m tall, 1.2 m shadow", options: { breakLine: true } },
    { text: "Ratio height \u00F7 shadow = 1.6 \u00F7 1.2 \u2248 1.333", options: { breakLine: true } },
    { text: "h = 9.0 \u00D7 1.333", options: { breakLine: true } },
    { text: "h \u2248 12.0 m", options: { bold: true } },
  ], { x: 7.1, y: 2.2, w: 5.4, h: 3.2, fontFace: FONT, fontSize: 17, color: C.darkBlue, valign: "top", isTextBox: true, margin: 0, paraSpaceAfter: 6 });
  d.note(s, "Both methods agree (to rounding). tan \u03B8 is the height-to-shadow ratio for that sun angle \u2014 it is the same for every object at the same time of day.", 5.85);
  d.num(s);
}

d.quick({ placement: "Solving the mango-tree height",
  prompt: "tan 53\u00B0 = h / 9.0. Which step correctly finds h?",
  short: "tan 53\u00B0 = h / 9.0. Which step finds h?",
  choices: ["h = 9.0 \u00F7 tan 53\u00B0", "h = 9.0 \u00D7 tan 53\u00B0", "h = tan 53\u00B0 \u00F7 9.0", "h = 9.0 + tan 53\u00B0"],
  correct: 1, rationale: "Multiply both sides by 9.0 to get h = 9.0 \u00D7 tan 53\u00B0. The lesson plan flags h = 9.0 \u00F7 tan 53\u00B0 as the common error." });

d.panel({ tag: "explain", kicker: "Apply It", headline: "Why is tan so useful for measuring heights in Kenya?",
  fill: C.lightPurple, panelH: 2.6,
  items: [
    "tan uses the opposite and adjacent sides \u2014 a height you want and a ground distance you can pace or tape.",
    "No hypotenuse needed: you never have to measure along a sun ray or up a slope.",
    "Surveyors, builders and farmers use this with one angle and one ground measurement.",
  ], note: "Try it: a flagpole casts a 10 m shadow when the sun angle is 40\u00B0 (tan 40\u00B0 = 0.8391). How tall is it?" });

d.quick({ placement: "Apply it: flagpole problem",
  prompt: "A flagpole casts a 10 m shadow when the sun angle is 40\u00B0. tan 40\u00B0 = 0.8391. How tall is the flagpole?",
  short: "Flagpole: 10 m shadow, sun angle 40\u00B0 (tan 40\u00B0 = 0.8391). Height?",
  choices: ["0.84 m", "8.39 m", "10.84 m", "11.92 m"],
  correct: 1, rationale: "h = 10 \u00D7 tan 40\u00B0 = 10 \u00D7 0.8391 = 8.39 m. 11.92 m comes from dividing (10 \u00F7 0.8391), the same error as in Quick Check 4." });

d.modelDqb(
  "On your trigonometry model triangle: label \u03B8 = 53\u00B0, adjacent = 9.0 m (shadow), opposite = h (tree). Write tan 53\u00B0 = h / 9.0 inside it. Add a \u201cratio web\u201d linking sin \u03B8, cos \u03B8 and tan \u03B8 with the identity tan \u03B8 = sin \u03B8 / cos \u03B8.",
  "Three columns on the board:\nANSWERED TODAY: \u201cWe can now find the tree\u2019s height because \u2026\u201d\nSTILL WONDERING: e.g. what if we know the height but not the angle?\nCONNECTIONS: how does tan link to Lessons 1\u20133?");

d.resources([
  { icon: "\u25B6", label: "VIDEO", title: rl.video.title, url: rl.video.direct_url, sub: "CK-12 \u2022 Good match: right-triangle word problems", status: "ok" },
  { icon: "\u2261", label: "READING", title: rl.reading.title, url: rl.reading.direct_url, sub: "CK-12 \u2022 Good match: worked examples using tan, sin and cos", status: "ok" },
  { icon: "\u{1F50D}", label: "SEARCH", title: "Search ARES: trigonometry, tangent ratio", url: rl.fallback_search_url || rl.video.search_url, sub: "Opens an ARES search for related videos and notes", status: "ok" },
]);

d.summary();

d.save("/home/claude/proto/pptx/Maths_G10_Trigonometry_L4_illustrative_v3.pptx").then(() => {
  fs.writeFileSync("/home/claude/proto/pptx/AnswerKey_Maths_Trigonometry_L4.html",
    answerKeyHtml({ title: "Mathematics G10, Trigonometry I, Lesson 4", subtitle: "Tangent and the Sine-Cosine-Tangent Relationship: Solving the Mango-Tree Problem" }, d.quizLog));
  console.log("maths done, questions:", d.quizLog.length);
});
