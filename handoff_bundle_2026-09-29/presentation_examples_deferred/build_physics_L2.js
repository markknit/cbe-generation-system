// Illustrative v3: Physics G10, Sub-Strand Pressure, Lesson 2
// "What Is Pressure? Measuring the Invisible Push". Content from
// data/outputs/v2/Physics/SS1.1_Pressure/*_data.json (LESSONS[1]).
const fs = require("fs");
const { makeDeck, answerKeyHtml, C } = require("./lib_v3");
const src = JSON.parse(fs.readFileSync("/home/claude/Physics_L2.json", "utf8"));
const rl = src.lesson.resourceLinks.predict;

const d = makeDeck("Physics G10 - Pressure - Lesson 2 (illustrative v3)");

d.title("PHYSICS \u2014 GRADE 10  |  PRESSURE", "What Is Pressure?",
  "Measuring the invisible push: force per unit area",
  "Today we get our first tool for explaining the crushed jerrycan.",
  "Sub-Strand 1.2: Pressure   |   Lesson 2   |   80 minutes");

d.panel({ tag: "predict", kicker: "Look Again at the Jerrycan", headline: "Something pushed hard enough to crush it.",
  fill: C.grey, panelH: 3.4,
  items: [
    "Look at the crushed jerrycan from last lesson. List every force you think is acting on it right now, and show its direction with an arrow.",
    "Why do you think the outside of the jerrycan \u201cwon\u201d against the plastic?",
    "Write silently for 1 minute, then compare with your partner.",
  ], note: "Draw your arrows now. We will check them at the end of the lesson." });

d.twoCol({ tag: "predict", kicker: "Predict", headline: "Same force. Same mass. Will they feel the same?",
  cols: [
    { h: "A flat textbook", b: "Pressed onto your palm with a firm push." },
    { h: "A sharpened pencil", b: "Same mass as the book, pressed onto your palm with exactly the same push." },
  ], cardH: 2.3, note: "Write a 2-sentence prediction before your teacher demonstrates. Which will feel like more of a \u201cpush\u201d, and why?" });

d.panel({ tag: "explain", kicker: "The Big Idea", headline: "Pressure is force spread over an area.",
  fill: C.darkBlue, panelH: 3.0, fontSize: 20,
  items: [
    "Pressure  =  Force \u00F7 Area          P = F / A",
    "Force (F) is measured in newtons (N). Area (A) is measured in square metres (m\u00B2).",
    "Pressure is measured in pascals (Pa).  1 Pa = 1 N/m\u00B2",
    "The pencil hurts more because the same force is squeezed onto a tiny area, so the pressure is much bigger.",
  ] });

d.quick({ placement: "The Big Idea (P = F/A)",
  prompt: "A book and a pencil are pressed onto your palm with the same force. Why does the pencil tip hurt more?",
  short: "Why does the pencil tip hurt more than the book?",
  choices: ["The pencil is heavier than the book", "The same force acts on a much smaller area, so the pressure is greater",
    "The pencil pushes with a bigger force", "The book spreads the force over a smaller area"],
  correct: 1, rationale: "P = F/A. With F the same, a smaller contact area gives a larger pressure. The masses and forces were deliberately kept equal." });

d.defs({ tag: "observe", kicker: "Investigation: Pressure Under Your Shoe", headline: "How much pressure do you put on the floor?",
  rowH: 0.95, termW: 1.4, termSize: 22, defSize: 15,
  rows: [
    { term: "1", def: "Stand on the bathroom scale. Record your mass in kg. Convert to weight in newtons: W = m \u00D7 10  (g = 10 N/kg)." },
    { term: "2", def: "Stand on graph paper with ONE shoe. Your partner traces around the sole." },
    { term: "3", def: "Count the 1 cm\u00B2 squares inside the outline. Count a part-square only if more than half of it is inside." },
    { term: "4", def: "Force on one foot = half your weight. Convert area: cm\u00B2 \u00F7 10 000 = m\u00B2. Then P = F / A." },
  ], note: "Record your shoe type, area, force and pressure. Post them on the class data wall." });

d.panel({ tag: "observe", kicker: "Worked Example", headline: "A 60 kg student in school shoes",
  fill: C.lightTeal, panelH: 2.3, numbered: true, fontSize: 18,
  items: [
    "Weight = 60 kg \u00D7 10 N/kg = 600 N.   One foot carries half: F = 300 N.",
    "Sole outline = 200 squares = 200 cm\u00B2.   A = 200 \u00F7 10 000 = 0.02 m\u00B2.",
    "P = F / A = 300 N \u00F7 0.02 m\u00B2 = 15 000 Pa.",
  ], note: "Most common mistake: forgetting to change cm\u00B2 into m\u00B2 before dividing. Check yours!" });

d.quick({ placement: "Shoe investigation / worked example",
  prompt: "A shoe sole covers 150 cm\u00B2. What is this area in square metres?",
  short: "Convert 150 cm\u00B2 to m\u00B2.",
  choices: ["1.5 m\u00B2", "0.15 m\u00B2", "0.015 m\u00B2", "15 m\u00B2"],
  correct: 2, rationale: "1 m\u00B2 = 10 000 cm\u00B2, so 150 \u00F7 10 000 = 0.015 m\u00B2. This conversion is the error the lesson plan flags as most common." });

d.twoCol({ tag: "explain", kicker: "Look at the Class Data", headline: "Which shoes press hardest on the floor?",
  cols: [
    { h: "Large contact area", b: "Flat sandals and sports trainers spread your weight over a big area \u2192 lower pressure.", fill: C.lightGreen },
    { h: "Small contact area", b: "Heels and narrow soles put your weight on a small area \u2192 higher pressure. That is why a heel can dent a soft floor.", fill: C.lightOrange },
  ], cardH: 2.6, note: "Same person, different shoes: the force stays the same, only the area changes." });

d.panel({ tag: "explain", kicker: "Apply It: Eldoret Warehouse", headline: "A 90 kg maize bag sits on a pallet with 4 legs.",
  fill: C.grey, panelH: 2.3, numbered: true, fontSize: 18,
  items: [
    "Weight of bag = 90 kg \u00D7 10 N/kg = 900 N, shared by 4 legs \u2192 225 N per leg.",
    "Each leg base = 25 cm\u00B2 = 25 \u00F7 10 000 = 0.0025 m\u00B2.",
    "Pressure under each leg = 225 N \u00F7 0.0025 m\u00B2 = 90 000 Pa.",
  ] });

d.quick({ placement: "Apply it: Eldoret warehouse answer",
  prompt: "The pressure under each pallet leg is 90 000 ____. Which unit completes the answer?",
  short: "The pressure under each pallet leg is 90 000 ____. Which unit?",
  choices: ["Newtons (N)", "Pascals (Pa), which are N/m\u00B2", "Kilograms (kg)", "Square metres (m\u00B2)"],
  correct: 1, rationale: "Pressure = force \u00F7 area, so its unit is N/m\u00B2, called the pascal (Pa). Newton is force, kg is mass, m\u00B2 is area." });

d.twoCol({ tag: "explain", kicker: "Your Turn (groups of 3)", headline: "Same 150 N push. Which is safer on a soft floor?",
  cols: [
    { h: "A rungu", b: "A Maasai elder leans on a rungu. The handle tip touches the floor over just 2 cm\u00B2." },
    { h: "A crutch", b: "A patient at Kenyatta National Hospital leans on a crutch with a flat base of 50 cm\u00B2." },
  ], cardH: 2.3, note: "Calculate both pressures on your mini-whiteboard. Then explain which is safer, and why." });

d.quick({ placement: "Apply it: rungu vs crutch problem",
  prompt: "A rungu tip (2 cm\u00B2) and a crutch base (50 cm\u00B2) each press down with 150 N. Which statement is correct?",
  short: "Rungu (2 cm\u00B2) vs crutch (50 cm\u00B2), both 150 N: which is correct?",
  choices: ["They exert the same pressure because the force is the same", "The crutch exerts higher pressure because it is larger",
    "The rungu exerts higher pressure because its area is smaller", "Neither exerts pressure because they are not moving"],
  correct: 2, rationale: "Rungu: 150 \u00F7 0.0002 = 750 000 Pa. Crutch: 150 \u00F7 0.005 = 30 000 Pa. Same force, smaller area, much higher pressure. So the crutch is safer on a soft floor." });

d.panel({ tag: "explain", kicker: "Back to the Jerrycan", headline: "Air pushes on every surface, from every direction.",
  fill: C.lightPurple, panelH: 3.2,
  items: [
    "The air above us has weight. That weight presses on every surface it touches: this is atmospheric pressure.",
    "It pushes on ALL faces of the jerrycan \u2014 top, bottom and all four sides \u2014 always pointing inward.",
    "Air inside the jerrycan pushes outward. While the two pushes balance, the jerrycan keeps its shape.",
    "Next lesson we find out how big atmospheric pressure really is, and what happened when the balance broke.",
  ] });

d.quick({ placement: "Back to the jerrycan (atmospheric pressure)",
  prompt: "In which directions does atmospheric pressure push on the jerrycan?",
  short: "In which directions does atmospheric pressure push on the jerrycan?",
  choices: ["Only downward, on the top", "Only on the sides", "Inward on every surface: top, bottom and all sides", "Outward from the inside only"],
  correct: 2, rationale: "Atmospheric pressure acts on every exposed surface, from all directions. The lesson plan flags students who draw arrows only on top as holding a key misconception." });



d.modelDqb(
  "Redraw your jerrycan. Add arrows on ALL six faces pointing inward (air outside), and arrows pointing outward from inside. Finish the sentence: \u201cThe full jerrycan did not collapse because ___.\u201d Circle what changed since Lesson 1 in green.",
  "Yellow note: What do I now THINK is crushing the jerrycan? Use the words pressure, force and area.\nBlue note: What am I still WONDERING? For example: how strong is atmospheric pressure? Does water push the same way?");

d.resources([
  { icon: "\u25B6", label: "VIDEO", title: rl.video.title, url: rl.video.direct_url, sub: "Khan Academy \u2022 Good match for force, area and pressure", status: "ok" },
  { icon: "\u2261", label: "READING", title: rl.reading.title, url: rl.reading.direct_url, sub: "CK-12 \u2022 Weak match: about gas pressure and temperature, not P = F/A. Review before using.", status: "weak" },
  { icon: "\u{1F50D}", label: "SEARCH", title: "Search ARES: pressure, force, unit area", url: rl.fallback_search_url || rl.video.search_url, sub: "Opens an ARES search for related videos and notes", status: "ok" },
]);

d.summary();

d.save("/home/claude/proto/pptx/Physics_G10_Pressure_L2_illustrative_v3.pptx").then(() => {
  fs.writeFileSync("/home/claude/proto/pptx/AnswerKey_Physics_Pressure_L2.html",
    answerKeyHtml({ title: "Physics G10, Pressure, Lesson 2", subtitle: "What Is Pressure? Measuring the Invisible Push" }, d.quizLog));
  console.log("physics done, questions:", d.quizLog.length);
});
