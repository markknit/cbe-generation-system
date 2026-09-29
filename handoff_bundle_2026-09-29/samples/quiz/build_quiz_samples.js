// Builds the quiz-only sample outputs for the four illustrative lessons.
// Questions are reused from the full-presentation examples; each gets a `phase`
// tied to the lesson plan's own framework phases (where it is used in class).
const fs = require("fs");
const { buildQuizDeck, answerKeyHtml, buildAnswerKeyDocx } = require("./quiz_lib");
const OUT = "/home/claude/proto/quiz_samples";
fs.mkdirSync(OUT, { recursive: true });

const lessons = [
  { src: "Biology_G10_PlantNutrition_L2_illustrative_v3_quiz.json", prefix: "Biology_G10_SS2.1_Plant_Nutrition_L2",
    meta: { subject: "Biology", grade: 10, substrandId: "2.1", substrandName: "Plant Nutrition", lessonNumber: 2, lessonTitle: "Leaf Structure: The Architecture of a Photosynthetic Machine" },
    phases: ["observe", "observe", "observe", "observe", "explain"],
    placements: ["Step 1: whole leaf under the hand lens (upper vs lower surface)", "Step 2: cross-section under the microscope", "Step 4: locating stomata on the lower epidermis", "Step 3: labelling the layers on the outline diagram (vascular bundle)", "Jigsaw function statements and the synthesis question"] },
  { src: "Physics_G10_Pressure_L2_illustrative_v3_quiz.json", prefix: "Physics_G10_SS1.2_Pressure_L2",
    meta: { subject: "Physics", grade: 10, substrandId: "1.2", substrandName: "Pressure", lessonNumber: 2, lessonTitle: "What Is Pressure? Measuring the Invisible Push" },
    phases: ["explain", "observe", "explain", "explain", "model"],
    placements: ["Formal definition P = F/A, after the book vs pencil demonstration", "Part B: shoe-pressure investigation (cm\u00B2 to m\u00B2 conversion)", "Problem 1: maize bag on a pallet (Eldoret warehouse)", "Problem 2: rungu vs crutch", "Revising the jerrycan force diagram"],
    prompts: { 2: "A maize bag on a pallet pushes 225 N onto each leg. Each leg touches the floor over 0.0025 m\u00B2, so the pressure is 90 000 ____. Which unit completes the answer?" } },
  { src: "Chemistry_G10_AcidsBases_L4_illustrative_v3_quiz.json", prefix: "Chemistry_G10_SS3.1_Acids_and_Bases_L4",
    meta: { subject: "Chemistry", grade: 10, substrandId: "3.1", substrandName: "Acids and Bases", lessonNumber: 4, lessonTitle: "Differences Between Acids and Bases Using Commercial Indicators" },
    phases: ["observe", "explain", "explain", "explain", "explain"],
    placements: ["Experiment 1: recording observations", "Pattern statements (litmus)", "Pattern statements (phenolphthalein)", "Pattern statements: comparing what each indicator can and cannot show", "Class consensus results table"] },
  { src: "Maths_G10_Trigonometry_L4_illustrative_v3_quiz.json", prefix: "Mathematics_G10_SS3.1_Trigonometry_I_L4",
    meta: { subject: "Mathematics", grade: 10, substrandId: "3.1", substrandName: "Trigonometry I", lessonNumber: 4, lessonTitle: "Tangent and the Sine-Cosine-Tangent Relationship: Solving the Mango-Tree Problem" },
    phases: ["observe", "observe", "explain", "explain", "explain"],
    placements: ["Part A: algebraic derivation of tan \u03B8", "Part B: numerical verification with mathematical tables", "Discussion Q2: which side is the 9.0 m shadow?", "Part B: mango-tree height calculation", "After the mango-tree calculation (new application problem)"],
    prompts: { 2: "The sun makes a 53\u00B0 angle with the ground and a tree casts a 9.0 m shadow. Relative to the 53\u00B0 angle, the shadow is the triangle\u2019s \u2026" } },
];

(async () => {
  for (const l of lessons) {
    const raw = JSON.parse(fs.readFileSync(l.src, "utf8"));
    // Map to the production schema field names.
    const quiz = raw.map((q, i) => ({ prompt: (l.prompts && l.prompts[i]) || q.prompt, choices: q.choices, correctIndex: q.correct, rationale: q.rationale, phase: l.phases[i], placement: l.placements[i] }));
    fs.writeFileSync(`${OUT}/${l.prefix}_quiz.json`, JSON.stringify({ meta: l.meta, quiz }, null, 1));
    await buildQuizDeck(l.meta, quiz, `${OUT}/${l.prefix}_QuickCheck.pptx`);
    fs.writeFileSync(`${OUT}/${l.prefix}_AnswerKey.html`, answerKeyHtml(l.meta, quiz));
    await buildAnswerKeyDocx(l.meta, quiz, `${OUT}/${l.prefix}_AnswerKey.docx`);
    console.log("built", l.prefix, quiz.length);
  }
})();
