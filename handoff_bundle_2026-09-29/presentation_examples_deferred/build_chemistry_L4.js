// Illustrative v3: Chemistry G10, Sub-Strand 3.1 Acids and Bases, Lesson 4
// "Differences Between Acids and Bases Using Commercial Indicators".
// Content from data/outputs/v2/Chemistry/SS3.1_Acids_and_Bases/*_data.json (LESSONS[3]).
const fs = require("fs");
const { makeDeck, answerKeyHtml, C } = require("./lib_v3");
const src = JSON.parse(fs.readFileSync("/home/claude/Chemistry_L4.json", "utf8"));
const rl = src.lesson.resourceLinks.predict;

const d = makeDeck("Chemistry G10 - Acids and Bases - Lesson 4 (illustrative v3)");

d.title("CHEMISTRY \u2014 GRADE 10  |  ACIDS AND BASES", "Reading the Colours",
  "Telling acids and bases apart with commercial indicators",
  "Can we use colour to reliably sort the cups from the school canteen?",
  "Sub-Strand 3.1: Acids and Bases   |   Lesson 4   |   80 minutes");

d.panel({ tag: "predict", kicker: "Predict First", headline: "Seven liquids from home. Acid, base, or neutral?",
  fill: C.grey, panelH: 2.9,
  items: [
    "Lemon juice \u2022 Vinegar (siki) \u2022 Baking soda solution \u2022 Liquid soap solution \u2022 Tap water \u2022 Black tea (chai) \u2022 Cow\u2019s milk",
    "In your prediction table, write acid, base or neutral for each liquid.",
    "Then predict the colour each indicator will turn. Compare with your partner.",
  ], note: "In Lesson 3, universal indicator gave us a rainbow. Will today\u2019s indicators tell the same story?" });

d.defs({ tag: "observe", kicker: "Today\u2019s Tools", headline: "Three commercial indicators",
  rowH: 1.1, termW: 3.0, termSize: 18,
  rows: [
    { term: "Litmus paper", def: "Comes in two colours, red and blue. Dip a strip and watch whether its colour flips." },
    { term: "Phenolphthalein", def: "A colourless liquid indicator. Add 2 drops to the test liquid in a spotting tile." },
    { term: "Methyl orange", def: "An orange liquid indicator. Add 2 drops to the test liquid in a spotting tile." },
  ], note: "An indicator is a substance that changes colour depending on whether a solution is acidic or basic." });

d.panel({ tag: "observe", kicker: "Safety First", headline: "Before anyone opens a bottle",
  fill: C.lightOrange, panelH: 3.4, fontSize: 16,
  items: [
    "Phenolphthalein is dissolved in ethanol, which burns. No open flames. Use dropper bottles only.",
    "Lemon juice and vinegar sting eyes. Keep hands away from your face; wash hands afterwards.",
    "Never taste any laboratory solution \u2014 even ones you know from home.",
    "Rinse used solutions down the sink with plenty of water.",
    "Report broken glassware. Your teacher sweeps it up, not you.",
  ] });

d.defs({ tag: "observe", kicker: "Experiment 1: Procedure", headline: "Testers test. Recorders record. Swap halfway.",
  rowH: 0.95, termW: 1.4, termSize: 22, defSize: 15,
  rows: [
    { term: "1", def: "Place a strip of red litmus and a strip of blue litmus on the white tile. Add 2\u20133 drops of the liquid to each." },
    { term: "2", def: "Record the colour immediately and again after 30 seconds." },
    { term: "3", def: "Put 5 drops of the liquid in a tile well. Add 2 drops of phenolphthalein. Record. Repeat with methyl orange in a new well." },
    { term: "4", def: "Repeat for all seven liquids. Write exact colours: \u201cturned pale pink\u201d, not \u201cchanged\u201d." },
  ], note: "Be a scientist, not a poet: what exact colour do you see?" });

d.quick({ placement: "Procedure (recording observations)",
  prompt: "Which of these is the most useful observation to record?",
  short: "Which is the most useful observation to record?",
  choices: ["\u201cIt changed.\u201d", "\u201cIt looked interesting.\u201d", "\u201cBlue litmus turned bright red within 5 seconds.\u201d", "\u201cIt was probably an acid.\u201d"],
  correct: 2, rationale: "A useful observation states the indicator, the exact colour change, and the timing. Option D is an interpretation, not an observation. Matches the lesson's 'scientist, not a poet' prompt." });

d.table({ tag: "explain", kicker: "The Pattern", headline: "What each indicator tells us",
  header: ["Indicator", "In an ACID", "In a BASE", "In a NEUTRAL solution"],
  colW: [3.1, 3.0, 3.0, 3.0], rowH: 0.62, fontSize: 15,
  rows: [
    ["Blue litmus", "turns red", "stays blue", "stays blue"],
    ["Red litmus", "stays red", "turns blue", "stays red"],
    ["Phenolphthalein", "colourless", "pink", "colourless"],
    ["Methyl orange", "red", "yellow", "yellow"],
  ], note: "Write a Pattern Statement for each indicator: \u201cAn acid turns ___ from ___ to ___; a base turns it from ___ to ___.\u201d", noteY: 5.4 });

d.quick({ placement: "The pattern table (litmus)",
  prompt: "A few drops of a liquid turn blue litmus paper red. What does this tell you?",
  short: "Blue litmus turns red. What does this tell you?",
  choices: ["The liquid is a base", "The liquid is an acid", "The liquid is neutral", "The litmus paper is faulty"],
  correct: 1, rationale: "Acids turn blue litmus red. Bases turn red litmus blue. A neutral liquid causes no change to either strip." });

d.quick({ placement: "The pattern table (phenolphthalein)",
  prompt: "In which kind of solution does phenolphthalein turn pink?",
  short: "In which kind of solution does phenolphthalein turn pink?",
  choices: ["An acid", "A base", "A neutral solution", "Any solution containing water"],
  correct: 1, rationale: "Phenolphthalein is colourless in acids and neutral solutions and turns pink in bases." });

d.twoCol({ tag: "explain", kicker: "Why Use More Than One?", headline: "One indicator can\u2019t always tell you the whole story.",
  cols: [
    { h: "Methyl orange", b: "Yellow in a base \u2026 but also yellow in a neutral solution. On its own, it can\u2019t tell water from soap." },
    { h: "Phenolphthalein", b: "Colourless in an acid \u2026 but also colourless in a neutral solution. On its own, it can\u2019t tell lemon juice from water." },
  ], cardH: 2.6, note: "That is why we classify using evidence from ALL the indicators together." });

d.quick({ placement: "Why use more than one indicator",
  prompt: "A liquid turns methyl orange yellow. Can you be sure it is a base?",
  short: "Methyl orange turns yellow. Can you be sure it is a base?",
  choices: ["Yes, yellow always means a base", "No, a neutral solution also turns methyl orange yellow, so test with another indicator",
    "Yes, but only if the liquid is clear", "No, yellow means the liquid is an acid"],
  correct: 1, rationale: "Methyl orange is yellow in both neutral and basic solutions. Red litmus (turns blue only in a base) or phenolphthalein (pink only in a base) is needed to decide." });

d.table({ tag: "explain", kicker: "Class Consensus", headline: "Sorting the liquids from home",
  header: ["Liquid", "Litmus", "Phenolphthalein", "Methyl orange", "Class"],
  colW: [2.7, 2.6, 2.3, 2.2, 2.3], rowH: 0.44, fontSize: 13,
  rows: [
    ["Lemon juice", "blue \u2192 red", "colourless", "red", "Acid"],
    ["Vinegar (siki)", "blue \u2192 red", "colourless", "red", "Acid"],
    ["Liquid soap", "red \u2192 blue", "pink", "yellow", "Base"],
    ["Baking soda solution", "red \u2192 blue", "faint pink", "yellow", "Base (weak)"],
    ["Tap water", "no change", "colourless", "yellow", "Neutral"],
    ["Black tea (chai)", "little or no change", "colourless", "yellow", "Weakly acidic"],
    ["Cow\u2019s milk", "little or no change", "colourless", "yellow", "About neutral"],
  ], note: "Expected results. Compare with your group\u2019s data and discuss any differences \u2014 especially milk and tea.", noteY: 5.75 });

d.quick({ placement: "Class consensus table",
  prompt: "Which liquid from today would you expect to turn methyl orange red?",
  short: "Which liquid would turn methyl orange red?",
  choices: ["Liquid soap solution", "Tap water", "Baking soda solution", "Vinegar"],
  correct: 3, rationale: "Methyl orange turns red in acids. Vinegar is an acid. Soap and baking soda are bases (yellow); tap water is neutral (yellow)." });

d.modelDqb(
  "Take out your model of the eight canteen cups. Label each cup ACID, BASE or NEUTRAL using today\u2019s evidence. Show that \u201csomething in the liquid\u201d is causing the colour change. Finish: \u201cMy model still cannot explain ___.\u201d",
  "Move any earlier question that today\u2019s experiment answered into the SOLVED zone, with the evidence on the back.\nAdd one new question, e.g. How do we measure HOW acidic something is? What do acids actually DO when they react?");

d.resources([
  { icon: "\u25B6", label: "VIDEO", title: rl.video.title, url: rl.video.direct_url, sub: "PhET \u2022 Partial match: introduces pH, which this unit covers in Lesson 8. Use as extension.", status: "weak" },
  { icon: "\u2261", label: "READING", title: rl.reading.title, url: rl.reading.direct_url, sub: "CK-12 \u2022 Good match for properties of acids", status: "ok" },
  { icon: "\u{1F50D}", label: "SEARCH", title: "Search ARES: acids, bases, indicators", url: rl.fallback_search_url || rl.video.search_url, sub: "Opens an ARES search for related videos and notes", status: "ok" },
]);

d.summary();

d.save("/home/claude/proto/pptx/Chemistry_G10_AcidsBases_L4_illustrative_v3.pptx").then(() => {
  fs.writeFileSync("/home/claude/proto/pptx/AnswerKey_Chemistry_AcidsBases_L4.html",
    answerKeyHtml({ title: "Chemistry G10, Acids and Bases, Lesson 4", subtitle: "Differences Between Acids and Bases Using Commercial Indicators" }, d.quizLog));
  console.log("chemistry done, questions:", d.quizLog.length);
});
