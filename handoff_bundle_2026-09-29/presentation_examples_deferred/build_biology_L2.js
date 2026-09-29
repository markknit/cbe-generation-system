// Illustrative v3 (upgraded): Biology G10, Sub-Strand 2.1 Plant Nutrition, Lesson 2
// "Leaf Structure: The Architecture of a Photosynthetic Machine".
// Content from data/outputs/v2/Biology/SS2.1_Plant_Nutrition/*_data.json (LESSONS[1]).
const fs = require("fs");
const { makeDeck, answerKeyHtml, C } = require("./lib_v3");
const src = JSON.parse(fs.readFileSync("/home/claude/Biology_L2.json", "utf8"));
const rl = src.lesson.resourceLinks.predict;

const d = makeDeck("Biology G10 - Plant Nutrition - Lesson 2 (illustrative v3)");

d.title("BIOLOGY \u2014 GRADE 10  |  PLANT NUTRITION", "Leaf Structure",
  "The architecture of a photosynthetic machine",
  "Today we find the first real evidence for why our sukuma wiki wilts.",
  "Sub-Strand 2.1: Plant Nutrition   |   Lesson 2   |   80 minutes");

d.panel({ tag: "predict", kicker: "Before We Look Inside", headline: "What\u2019s actually inside a leaf?",
  fill: C.grey, panelH: 2.9,
  items: [
    "Take a fresh mango or bean leaf and a hand lens. Look at both surfaces. Feel them.",
    "Without cutting it, sketch what you think a cross-section (a slice through the middle) would look like.",
    "Label any layers you think are there, and write one sentence on why you think they are there.",
  ], note: "Compare with your partner: one similarity, one difference. We come back to your sketch at the end." });

d.defs({ tag: "observe", kicker: "The Outer Layers", headline: "A leaf must let light in \u2014 without drying out.",
  rowH: 1.4, termW: 2.6,
  rows: [
    { term: "Cuticle", def: "A waxy, transparent, waterproof layer on the outer surface. Light passes through it, but it slows water loss from the leaf." },
    { term: "Epidermis", def: "A single layer of tightly packed, transparent cells under the cuticle. It protects the leaf. It has almost no chloroplasts, so light passes straight through to the cells below." },
  ], note: "Activity: with your hand lens, find the shinier side of the leaf. That is the upper surface \u2014 thicker cuticle, facing the sun." });

d.quick({ placement: "The outer layers (cuticle and epidermis)",
  prompt: "Why is it useful that the cuticle is both waxy and transparent?",
  short: "Why is the cuticle both waxy and transparent?",
  choices: ["It lets light in while reducing water loss", "It traps carbon dioxide inside the leaf",
    "It makes food for the leaf", "It carries water to the leaf cells"],
  correct: 0, rationale: "Transparent lets light reach the chloroplast-rich cells below; waxy slows water loss. The cuticle does not photosynthesise or transport water." });

d.twoCol({ tag: "observe", kicker: "Where the Work Happens", headline: "Two layers of cells, two different jobs.",
  cols: [
    { h: "Palisade mesophyll", b: "Tall cells packed tightly just under the upper epidermis, full of chloroplasts. Most photosynthesis happens here: tight packing puts the most chloroplasts where the light is strongest.", fill: C.lightGreen },
    { h: "Spongy mesophyll", b: "Loosely packed, irregular cells with large air spaces between them. The air spaces let carbon dioxide and oxygen move easily to and from every cell." },
  ], cardH: 3.0, note: "Microscope (100\u00D7): sketch one palisade cell and one spongy cell. Which has more green chloroplasts?" });

d.quick({ placement: "Palisade and spongy mesophyll",
  prompt: "Which layer is packed tightly with chloroplasts to capture the most light?",
  short: "Which layer is packed with chloroplasts to capture the most light?",
  choices: ["Lower epidermis", "Palisade mesophyll", "Spongy mesophyll", "Cuticle"],
  correct: 1, rationale: "Palisade cells are tall and tightly packed under the upper epidermis, where light is strongest. Spongy mesophyll is loosely packed for gas movement." });

d.panel({ tag: "observe", kicker: "The Key Structure", headline: "Stomata: tiny pores that do two jobs at once.",
  fill: C.lightPurple, panelH: 3.4,
  items: [
    "Stomata are tiny pores, found mostly in the lower epidermis. Look for them under the microscope.",
    "Each stoma sits between two guard cells, which control how wide the pore opens.",
    "When a stoma is open, carbon dioxide enters for photosynthesis and oxygen leaves.",
    "But an open pore works both ways: water vapour also escapes through it. This water loss is called transpiration.",
  ] });

d.quick({ placement: "Stomata and guard cells",
  prompt: "What controls how wide a stoma opens?",
  short: "What controls how wide a stoma opens?",
  choices: ["The cuticle", "The two guard cells around it", "The palisade cells", "The xylem vessels"],
  correct: 1, rationale: "Each stoma is surrounded by two guard cells that change shape to open or close the pore. HOW they do this is left as a DQB question for later in the unit." });

d.twoCol({ tag: "observe", kicker: "The Plumbing", headline: "Vascular bundles: the leaf\u2019s delivery pipes.",
  cols: [
    { h: "Xylem", b: "Carries water (and dissolved minerals) up from the roots into the leaf, where every cell needs it.", fill: C.lightTeal },
    { h: "Phloem", b: "Carries the food made in the leaf (sugars) away to the rest of the plant." },
  ], cardH: 2.5, note: "The veins you can see on the leaf are vascular bundles. Find one in your cross-section." });

d.quick({ placement: "Vascular bundles (xylem and phloem)",
  prompt: "Which tissue carries water from the roots up into the leaf?",
  short: "Which tissue carries water up into the leaf?",
  choices: ["Phloem", "Xylem", "Palisade mesophyll", "Epidermis"],
  correct: 1, rationale: "Xylem carries water and minerals up from the roots. Phloem carries sugars made in the leaf to the rest of the plant." });

d.panel({ tag: "explain", kicker: "Putting It Together", headline: "So why does the sukuma wiki wilt at midday?",
  fill: C.darkBlue, panelH: 3.4, numbered: true,
  items: [
    "Xylem keeps delivering water from the roots to the leaf cells.",
    "In bright midday light, stomata open wide for gas exchange, so water vapour escapes faster.",
    "When water leaves faster than xylem can replace it, the cells lose water and go soft \u2014 the leaf wilts.",
    "At night stomata close, water loss slows, the xylem catches up, and the plant recovers by morning.",
  ], note: "Jigsaw: your group explains ONE structure in 60 seconds \u2014 what it looks like, what it does, and how it links to wilting." });

d.quick({ placement: "Putting it together (the wilting explanation)",
  prompt: "Using today\u2019s evidence, why does the sukuma wiki wilt at midday even though the soil is moist?",
  short: "Why does the sukuma wiki wilt at midday even though the soil is moist?",
  choices: ["The soil dries out faster in strong sunlight", "Water vapour leaves through open stomata faster than xylem can replace it",
    "The roots stop absorbing water when it is hot", "Chlorophyll breaks down in direct sunlight"],
  correct: 1, rationale: "The lesson's payoff: open stomata in bright light lose water vapour faster than the xylem resupplies it, so cells lose water and the leaf droops. The soil stays moist, so A and C do not fit the phenomenon." });

d.modelDqb(
  "Add a leaf cross-section to your Lesson 1 model: cuticle, epidermis, palisade, spongy mesophyll, stoma with guard cells, and a vascular bundle. Draw arrows for light in, water up the xylem, and water vapour out of the stoma. Finish: \u201cMy model still cannot explain ___\u201d and circle it in red.",
  "Yellow note: one NEW question today raised (e.g. What makes guard cells open or close?).\nGreen note: one question from Lesson 1 you can now partly answer \u2014 write the partial answer.");

d.resources([
  { icon: "\u25B6", label: "VIDEO", title: rl.video.title, url: rl.video.direct_url, sub: "TED-Ed \u2022 Unclear match: this generic title appears in 20 lessons across the corpus. Preview before using.", status: "weak" },
  { icon: "\u2261", label: "READING", title: rl.reading.title, url: rl.reading.direct_url, sub: "CK-12 \u2022 Partial match: about leaf pigments, not leaf structure", status: "weak" },
  { icon: "\u{1F50D}", label: "SEARCH", title: "Search ARES: leaf structure, stomata", url: rl.fallback_search_url || rl.video.search_url, sub: "Best option for this lesson until the link fix lands", status: "ok" },
]);

d.summary();

d.save("/home/claude/proto/pptx/Biology_G10_PlantNutrition_L2_illustrative_v3.pptx").then(() => {
  fs.writeFileSync("/home/claude/proto/pptx/AnswerKey_Biology_PlantNutrition_L2.html",
    answerKeyHtml({ title: "Biology G10, Plant Nutrition, Lesson 2", subtitle: "Leaf Structure: The Architecture of a Photosynthetic Machine" }, d.quizLog));
  console.log("biology done, questions:", d.quizLog.length);
});
