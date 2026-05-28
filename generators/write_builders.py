#!/usr/bin/env python3
builders = r"""
// ─── Docx section builders ───────────────────────────────────────────────────

function subStrandOverview(unit) {
  const LW = 3000, CW = W - LW;
  return makeTable([
    fullHeader('SUB-STRAND OVERVIEW', C.darkBlue, 'FFFFFF', SZ_H, 2),
    labelRow('Grade Level',        unit.gradeLevel,        LW),
    labelRow('Subject',            unit.subject,           LW),
    labelRow('Strand',             unit.strand,            LW),
    labelRow('Sub-Strand',         unit.substrand,         LW),
    labelRow('Total Duration',     unit.duration,          LW),
    labelRow('Sub-Strand Content', unit.content,           LW, { labelFill: C.lightBlue }),
    labelRow('Learning Outcomes',  unit.learningOutcomes,  LW, { labelFill: C.lightBlue }),
    labelRow('Core Competencies',  unit.coreCompetencies,  LW, { labelFill: C.lightBlue }),
    labelRow('Core Values',        unit.values,            LW, { labelFill: C.lightGreen }),
    labelRow('Pertinent & Contemporary Issues (PCIs)', unit.pcis, LW, { labelFill: C.lightOrange }),
    labelRow('Key Inquiry Question', unit.keyInquiry,      LW, { labelFill: C.lightPurple }),
    labelRow('Anchoring Phenomenon', unit.phenomenon,      LW, { labelFill: C.lightPurple }),
    labelRow('Driving Question',   unit.drivingQuestion,   LW, { labelFill: C.lightPurple }),
    labelRow('Storyline Thread',   unit.storylineThread,   LW, { labelFill: C.lightTeal }),
  ]);
}

function sectionA(lesson) {
  return makeTable([
    fullHeader('LESSON ' + lesson.number + ': ' + lesson.title, C.darkBlue, 'FFFFFF', SZ_H, 2),
    fullHeader('A. SPECIFIC LEARNING OUTCOMES', C.teal, 'FFFFFF', SZ_H, 2),
    labelRow('Purpose',              lesson.slo.purpose,            3000, { labelFill: C.lightBlue }),
    labelRow('Knowledge',            lesson.slo.knowledge,          3000, { labelFill: C.lightBlue }),
    labelRow('Skills',               lesson.slo.skills,             3000, { labelFill: C.lightBlue }),
    labelRow('Attitudes',            lesson.slo.attitudes,          3000, { labelFill: C.lightBlue }),
    labelRow('Key Inquiry Question', lesson.slo.keyInquiry,         3000, { labelFill: C.lightPurple }),
    labelRow('Purpose in Storyline', lesson.slo.purposeInStoryline, 3000, { labelFill: C.lightTeal }),
    labelRow('Safety Notes',         lesson.slo.safetyNotes,        3000, { labelFill: C.lightOrange }),
  ]);
}

function sectionB(lesson) {
  return makeTable([
    fullHeader('B. LESSON OVERVIEW', C.teal, 'FFFFFF', SZ_H, 1),
    new TableRow({ children: [cell(lesson.overview, { fill: C.white, w: W, size: SZ })] }),
  ], [W]);
}

function sectionC(lesson) {
  const CW = [900, 2556, 2556, 2556, 2556, 2556];
  return makeTable([
    fullHeader('C. LESSON IMPLEMENTATION FRAMEWORK', C.teal, 'FFFFFF', SZ_H, 6),
    new TableRow({ children: [
      cell('Phase',                { fill: C.darkBlue, bold: true, color: 'FFFFFF', w: CW[0], size: SZ }),
      cell('Learner Experience',   { fill: C.medBlue,  bold: true, color: 'FFFFFF', w: CW[1], size: SZ }),
      cell('Resource',             { fill: C.teal,     bold: true, color: 'FFFFFF', w: CW[2], size: SZ }),
      cell('Teacher Actions',      { fill: C.medBlue,  bold: true, color: 'FFFFFF', w: CW[3], size: SZ }),
      cell('Sensemaking Strategy', { fill: C.teal,     bold: true, color: 'FFFFFF', w: CW[4], size: SZ }),
      cell('Assessment Strategy',  { fill: C.medBlue,  bold: true, color: 'FFFFFF', w: CW[5], size: SZ }),
    ]}),
    ...lesson.framework.map(f => new TableRow({ children: [
      cell(f.phase,               { fill: PHASE_COLOUR[f.phase] || C.lightBlue, bold: true, w: CW[0], size: SZ }),
      cell(f.learnerExperience,   { fill: C.white, w: CW[1], size: SZ }),
      cell(f.resource,            { fill: C.grey,  w: CW[2], size: SZ }),
      cell(f.teacherMoves,        { fill: C.white, w: CW[3], size: SZ }),
      cell(f.sensemakingStrategy, { fill: C.grey,  w: CW[4], size: SZ }),
      cell(f.formativeAssessment, { fill: C.white, w: CW[5], size: SZ }),
    ]})),
  ], CW);
}

function sectionD(lesson) {
  return makeTable([
    fullHeader('D. TEACHER REFLECTION', C.orange, 'FFFFFF', SZ_H, 1),
    new TableRow({ children: [cell(lesson.teacherReflection, { fill: C.lightOrange, w: W, size: SZ })] }),
  ], [W]);
}

function sectionE(lesson) {
  const LW = 3000, CW = W - LW;
  return makeTable([
    fullHeader('E. SUMMARY TABLE PROMPT  (pre-filled example for this lesson)', C.purple, 'FFFFFF', SZ_H, 2),
    new TableRow({ children: [
      cell('What did I observe?',                   { fill: C.lightPurple, bold: true, w: LW, size: SZ }),
      cell(lesson.summaryTablePrompt.observed,      { fill: C.white,       w: CW,     size: SZ }),
    ]}),
    new TableRow({ children: [
      cell('What did I learn?',                     { fill: C.lightPurple, bold: true, w: LW, size: SZ }),
      cell(lesson.summaryTablePrompt.learned,       { fill: C.white,       w: CW,     size: SZ }),
    ]}),
    new TableRow({ children: [
      cell('How does this explain the phenomenon?', { fill: C.lightPurple, bold: true, w: LW, size: SZ }),
      cell(lesson.summaryTablePrompt.explained,     { fill: C.white,       w: CW,     size: SZ }),
    ]}),
  ], [LW, CW]);
}

// ─── Document builders ───────────────────────────────────────────────────────

async function buildSoW() {
  const body = [
    ...titleBlock(
      'BIOLOGY GRADE 10: PLANT NUTRITION',
      'CBE Phenomenon-Driven Lesson Sequence -- Sub-Strand 2.1 (12 Lessons)'
    ),
    SPACE(),
    subStrandOverview(UNIT),
    SPACE(),
  ];
  for (const lesson of LESSONS) {
    body.push(PAGE_BREAK());
    body.push(sectionA(lesson), SPACE());
    body.push(sectionB(lesson), SPACE());
    body.push(sectionC(lesson), SPACE());
    body.push(sectionD(lesson), SPACE());
    body.push(sectionE(lesson), SPACE());
  }
  return new Document({
    sections: [{
      properties: {
        page: {
          size: { width: 12240, height: 15840, orientation: PageOrientation.LANDSCAPE },
          margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 },
        },
      },
      children: body,
    }],
  });
}

async function buildFinalExplanation() {
  const FLW = 3000, FCW = W - FLW;
  const RW = Math.floor((W - FLW) / 3);
  const RWr = W - FLW - RW * 2;

  const headerRows = [
    fullHeader('FINAL EXPLANATION: PLANT NUTRITION', C.darkBlue, 'FFFFFF', SZ_H, 2),
    fullHeader('Biology Grade 10 -- Student Assessment Document', C.teal, 'FFFFFF', SZ_H, 2),
    labelRow('Student Name', '_______________________________________________', FLW),
    labelRow('Class',        '_______________________________________________', FLW),
    labelRow('Date',         '_______________________________________________', FLW),
  ];

  const instrRows = [
    fullHeader('INSTRUCTIONS FOR STUDENTS', C.teal, 'FFFFFF', SZ_H, 1),
    new TableRow({ children: [cell(
      'You have completed all 12 lessons of Plant Nutrition. Write your COMPLETE EXPLANATION for the driving question:\n' +
      '"How does a tiny seed become a massive plant -- where do all the materials and energy come from, and how does the process that powers plant growth sustain all life on Earth?"\n\n' +
      'USE: Your Summary Table, Plant Nutrition Model, class experiments (Elodea, chromatography, Calvin cycle card-sort), and research presentations.\n\n' +
      'YOUR EXPLANATION MUST INCLUDE:\n' +
      '• The difference between autotrophic and heterotrophic nutrition\n' +
      '• Chloroplast structure and the function of each component\n' +
      '• Light-dependent reactions (photolysis, ATP, NADPH, O2)\n' +
      '• Light-independent reactions (Calvin cycle, CO2 fixation, glucose synthesis)\n' +
      '• Why most plant mass comes from CO2, not soil\n' +
      '• At least TWO Kenyan examples\n\n' +
      'GRADING: 20 points total (see rubric below). Minimum 300 words.',
      { fill: C.white, w: W, size: SZ }
    )]}),
  ];

  const parts = [
    {
      title: 'SECTION 1: HOW DO PLANTS OBTAIN MATERIALS TO GROW?',
      prompt: 'Explain the difference between autotrophic and heterotrophic nutrition. State how the pumpkin (from the phenomenon) obtains its materials. Write the overall word equation for photosynthesis and identify the raw materials and products.',
      answer:
        'Autotrophic nutrition: the organism synthesises its own organic food from inorganic raw materials using an external energy source (sunlight). Heterotrophic nutrition: the organism obtains organic food by consuming or absorbing it from other organisms.\n\n' +
        'The pumpkin is autotrophic -- it uses photosynthesis to make glucose from carbon dioxide and water using light energy and chlorophyll.\n\n' +
        'Word equation: Carbon dioxide + Water -> Glucose + Oxygen (requires: light energy and chlorophyll)\n' +
        'Chemical equation: 6CO2 + 6H2O + light energy -> C6H12O6 + 6O2\n\n' +
        'Raw materials: carbon dioxide (from the air, absorbed through stomata), water (from the soil, absorbed by roots), light energy (from the sun, absorbed by chlorophyll).\n' +
        'Products: glucose (stored as starch, used for respiration and growth), oxygen (released as a by-product through stomata).\n\n' +
        'KEY INSIGHT: most of the pumpkin\'s 300 kg dry mass consists of carbon atoms that were originally present in atmospheric CO2. The pumpkin literally built itself from air.',
    },
    {
      title: 'SECTION 2: HOW DOES THE CHLOROPLAST MAKE PHOTOSYNTHESIS POSSIBLE?',
      prompt: 'Describe the structure of the chloroplast. Explain how each component (outer/inner membrane, thylakoids, grana, stroma) contributes to photosynthesis. What is chlorophyll and why does it appear green?',
      answer:
        'Chloroplast structure and function:\n\n' +
        'Outer membrane: smooth outer boundary; controls entry and exit of molecules into the chloroplast.\n' +
        'Inner membrane: controls exchange between cytoplasm and chloroplast interior.\n' +
        'Thylakoid membranes: flattened membrane sacs containing chlorophyll molecules; site of light-dependent reactions. The large surface area of the thylakoid membranes maximises light capture.\n' +
        'Grana (singular: granum): stacks of thylakoids. Stacking increases the surface area for light absorption without increasing the chloroplast\'s overall size.\n' +
        'Stroma: the fluid-filled space surrounding the thylakoids; site of light-independent reactions (Calvin cycle); contains the enzymes (including RuBisCO) needed for CO2 fixation.\n\n' +
        'Chlorophyll: a green pigment embedded in the thylakoid membranes. It absorbs red light (~680 nm) and blue light (~450 nm) and reflects green light -- which is why leaves appear green. Multiple pigments (chlorophyll a, chlorophyll b, xanthophylls, carotene) work together to absorb a broader range of wavelengths, as shown by paper chromatography in Lesson 3.',
    },
    {
      title: 'SECTION 3: WHAT HAPPENS DURING THE LIGHT STAGE?',
      prompt: 'Describe the light-dependent reactions of photosynthesis. Where do they occur? What are the inputs and outputs? Explain photolysis. Reference the Elodea experiment as evidence.',
      answer:
        'The light-dependent reactions occur in the thylakoid membranes of the chloroplast.\n\n' +
        'Inputs: light energy, water (H2O), ADP, Pi (inorganic phosphate), NADP+.\n' +
        'Outputs: ATP, NADPH, oxygen (O2).\n\n' +
        'Process:\n' +
        '1. Chlorophyll molecules in the thylakoid membranes absorb light energy. This excites electrons to a higher energy level.\n' +
        '2. Photolysis of water: light energy is used to split water molecules: 2H2O -> 4H+ + 4e- + O2. The electrons replace those lost from chlorophyll. Oxygen is released as a by-product.\n' +
        '3. The excited electrons pass through an electron transport chain in the thylakoid membrane. Their energy is used to synthesise ATP (from ADP + Pi) -- photophosphorylation.\n' +
        '4. NADP+ accepts hydrogen ions and electrons, becoming NADPH -- a high-energy electron carrier.\n\n' +
        'Summary: Light energy + 2H2O + ADP + Pi + NADP+ -> ATP + NADPH + O2\n\n' +
        'Evidence from the Elodea experiment (Lesson 4): the aquatic plant Elodea produced more oxygen bubbles at higher light intensities, confirming that the light stage produces O2 at a rate proportional to light intensity. The glowing splint test confirmed the gas was oxygen. At very low light intensities, almost no bubbles were produced -- showing that light is essential for the light stage reactions.',
    },
    {
      title: 'SECTION 4: WHAT HAPPENS DURING THE DARK STAGE (CALVIN CYCLE)?',
      prompt: 'Describe the light-independent reactions of photosynthesis (Calvin cycle). Where do they occur? What are the inputs and outputs? Explain CO2 fixation. Explain why most plant mass comes from CO2, not soil.',
      answer:
        'The light-independent reactions (Calvin cycle) occur in the stroma of the chloroplast. They are called light-independent because they do not directly require light -- but they DO require the ATP and NADPH produced in the light stage.\n\n' +
        'Inputs: carbon dioxide (CO2), ATP (from light stage), NADPH (from light stage).\n' +
        'Outputs: glucose (C6H12O6), ADP, Pi, NADP+ (recycled to light stage), water.\n\n' +
        'Process (simplified Calvin cycle):\n' +
        '1. CO2 fixation: each CO2 molecule is attached to a 5-carbon acceptor molecule (RuBP), forming an unstable 6-carbon compound that immediately splits into two 3-carbon molecules (3PG). The enzyme RuBisCO catalyses this step.\n' +
        '2. Reduction: ATP and NADPH from the light stage convert 3PG into glyceraldehyde-3-phosphate (G3P), a 3-carbon sugar.\n' +
        '3. Regeneration: most G3P is used to regenerate RuBP (using ATP), keeping the cycle running. A fraction of G3P is used to synthesise glucose.\n' +
        '4. Six turns of the cycle fix 6 CO2 molecules and produce enough G3P to synthesise one glucose molecule (C6H12O6).\n\n' +
        'Complete equation: 6CO2 + 6H2O + light energy -> C6H12O6 + 6O2\n\n' +
        'WHY MASS COMES FROM CO2: the 6 carbon atoms in each glucose molecule all came from CO2 gas absorbed from the air. When millions of glucose molecules are linked into starch and cellulose, they form the solid bulk of the plant. A pumpkin\'s dry mass is approximately 45% carbon -- and every carbon atom was once CO2 floating in the atmosphere. The soil provides water and minerals, but these account for very little of the plant\'s actual mass.',
    },
    {
      title: 'SECTION 5: WHY DOES PHOTOSYNTHESIS MATTER BEYOND THE PLANT?',
      prompt: 'Explain the significance of photosynthesis to (a) food chains, (b) atmospheric oxygen, (c) the carbon cycle, and (d) food security in Kenya. Use at least TWO Kenyan examples.',
      answer:
        '(a) Food chains: photosynthesis is the process of primary production -- it converts solar energy into chemical energy stored in organic compounds. Almost all ecosystems depend on this energy. Without photosynthesising organisms (plants, algae, phytoplankton), the base of every food chain would collapse. In Kenya, every food chain from the Maasai Mara to Lake Victoria begins with photosynthesis.\n\n' +
        '(b) Atmospheric oxygen: virtually all atmospheric oxygen on Earth is a product of photosynthesis. Photolysis of water has been releasing O2 for approximately 2.7 billion years -- creating the oxygen-rich atmosphere that makes aerobic life possible. Every breath contains oxygen produced by photosynthesis.\n\n' +
        '(c) Carbon cycle: photosynthesis removes CO2 from the atmosphere and fixes it into organic compounds. Respiration, decomposition, and combustion return CO2 to the atmosphere. Fossil fuels represent ancient photosynthate -- burning them releases CO2 that was fixed millions of years ago, disrupting the balance and contributing to climate change.\n\n' +
        '(d) Food security in Kenya -- two examples:\n' +
        '• Kenyan tea (Kericho/Kisii): Kenya is one of the world\'s largest tea exporters. Tea plants in Kericho\'s cool, moist highlands operate near optimal photosynthesis conditions -- abundant water, moderate temperatures, and cloud cover providing diffuse light. The entire tea export economy depends on efficient photosynthesis.\n' +
        '• Striga (witchweed) and maize: Striga infests over 50% of maize fields in parts of western Kenya, reducing yields by up to 80% by parasitising maize roots and stealing the water and minerals needed for photosynthesis. Controlling Striga -- through resistant varieties, hand-weeding, and trap crops -- directly improves maize photosynthesis efficiency and food production for millions of Kenyans.',
    },
  ];

  const rubricRows = [
    fullHeader('FINAL EXPLANATION RUBRIC (20 points)', C.darkBlue, 'FFFFFF', SZ_H, 4),
    new TableRow({ children: [
      cell('Criterion',        { fill: C.medBlue, bold: true, color: 'FFFFFF', w: FLW, size: SZ }),
      cell('Excellent (4)',    { fill: C.medBlue, bold: true, color: 'FFFFFF', w: RW,  size: SZ }),
      cell('Proficient (3)',   { fill: C.teal,    bold: true, color: 'FFFFFF', w: RW,  size: SZ }),
      cell('Developing (1-2)',{ fill: C.medBlue, bold: true, color: 'FFFFFF', w: RWr, size: SZ }),
    ]}),
    ...[
      ['Autotrophic vs Heterotrophic', 'Clear definitions; pumpkin correctly identified as autotrophic; word and chemical equations accurate.', 'Definitions present; equation partially correct.', 'Missing definitions or incorrect equations.'],
      ['Chloroplast Structure', 'All 5 components named and linked to function; chlorophyll absorption/reflection explained accurately.', '3-4 components; function links partial.', 'Fewer than 3 components or no function links.'],
      ['Light Stage', 'Thylakoid location stated; photolysis explained; ATP and NADPH as outputs; O2 source correctly identified as H2O; Elodea evidence cited.', 'Correct location and outputs; O2 source or Elodea evidence missing.', 'Incorrect location or missing key outputs.'],
      ['Dark Stage (Calvin Cycle)', 'Stroma location stated; CO2 fixation explained; glucose synthesis described; KEY INSIGHT (mass from CO2) clearly stated.', 'Correct location and process; key insight partial.', 'Incorrect location or missing CO2 fixation.'],
      ['Significance + Kenyan Examples', 'Two specific Kenyan examples with photosynthesis mechanism connection; all 4 significance points (food chains, O2, carbon cycle, food security) addressed.', 'Two Kenyan examples present; 3-4 significance points addressed.', 'Only one example or fewer than 3 significance points.'],
    ].map(([crit, exc, prof, dev]) => new TableRow({ children: [
      cell(crit, { fill: C.lightBlue, w: FLW, size: SZ }),
      cell(exc,  { fill: C.white,     w: RW,  size: SZ }),
      cell(prof, { fill: C.grey,      w: RW,  size: SZ }),
      cell(dev,  { fill: C.white,     w: RWr, size: SZ }),
    ]})),
  ];

  const body = [
    ...titleBlock('FINAL EXPLANATION: PLANT NUTRITION', 'Biology Grade 10 -- Student Assessment Document'),
    SPACE(),
    makeTable(headerRows, [FLW, FCW]),
    SPACE(),
    makeTable(instrRows,  [W]),
    SPACE(),
    ...parts.flatMap(p => [
      makeTable([
        fullHeader(p.title, C.medBlue, 'FFFFFF', SZ_H, 1),
        new TableRow({ children: [cell(p.prompt, { fill: C.lightBlue, w: W, size: SZ, italic: true })] }),
        new TableRow({ children: [cell(p.answer, { fill: C.white, w: W, size: SZ })] }),
      ], [W]),
      SPACE(),
    ]),
    makeTable(rubricRows, [FLW, RW, RW, RWr]),
  ];

  return new Document({
    sections: [{
      properties: {
        page: {
          size: { width: 12240, height: 15840, orientation: PageOrientation.LANDSCAPE },
          margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 },
        },
      },
      children: body,
    }],
  });
}

async function buildSummaryTable() {
  const SLW = 1200, SC1 = 3120, SC2 = 3120, SC3 = 3120, SC4 = 3120;
  // columns: [1200, 3120, 3120, 3120, 3120] sum = 13680

  const lessonTitles = [
    { col1: 'Lesson 1\nThe Pumpkin Mystery',     dqb: 'DQB Opened -- initial questions posted' },
    { col1: 'Lesson 2\nTypes of Nutrition',      dqb: 'DQB: photosynthesis equation added' },
    { col1: 'Lesson 3\nChloroplast Structure',   dqb: 'DQB: chlorophyll questions answered' },
    { col1: 'Lesson 4\nLight Stage',             dqb: 'DQB: O2 source answered' },
    { col1: 'Lesson 5\nDark Stage (Calvin Cycle)',dqb: 'DQB: mass from CO2 -- KEY INSIGHT' },
    { col1: 'Lesson 6\nFactors',                 dqb: 'DQB: limiting factors answered' },
    { col1: 'Lesson 7\nAdaptations',             dqb: 'DQB: ecosystem questions added' },
    { col1: 'Lesson 8\nHeterotrophic Plants',    dqb: 'DQB: Striga questions answered' },
    { col1: 'Lesson 9\nSignificance',            dqb: 'DQB: near-complete' },
    { col1: 'Lesson 10\nResearch',               dqb: 'DQB: Kenyan application questions added' },
    { col1: 'Lesson 11\nSynthesis',              dqb: 'DQB: Complete -- all answered' },
    { col1: 'Lesson 12\nFinal Explanation',      dqb: 'DQB: Final reflection card added' },
  ];

  const headerTable = makeTable([
    fullHeader('SUMMARY TABLE: BIOLOGY GRADE 10 -- PLANT NUTRITION', C.darkBlue, 'FFFFFF', SZ_H, 2),
    fullHeader('Sub-Strand 2.1: Nutrition -- Teacher Reference (Pre-filled)', C.teal, 'FFFFFF', SZ_H, 2),
    labelRow('Sub-Strand', '2.1: Nutrition', SLW + SC1),
    labelRow('Driving Question', UNIT.drivingQuestion, SLW + SC1),
  ], [SLW + SC1, SC2 + SC3]);

  const instrTable = makeTable([
    fullHeader('INSTRUCTIONS', C.teal, 'FFFFFF', SZ_H, 1),
    new TableRow({ children: [cell(
      'FOR TEACHERS:\n' +
      'This is the teacher reference version -- each row is pre-filled with expected student responses. ' +
      'Use it to assess student Summary Tables, identify gaps, and prepare discussion questions. ' +
      'The student version has blank cells for students to complete after each lesson.',
      { fill: C.white, w: W, size: SZ }
    )]}),
  ], [W]);

  const mainTable = makeTable([
    new TableRow({ children: [
      cell('Lesson # and Title',                    { fill: C.darkBlue, bold: true, color: 'FFFFFF', w: SLW, size: SZ }),
      cell('What did I observe?',                   { fill: C.medBlue,  bold: true, color: 'FFFFFF', w: SC1, size: SZ }),
      cell('What did I learn?',                     { fill: C.teal,     bold: true, color: 'FFFFFF', w: SC2, size: SZ }),
      cell('How does this explain the phenomenon?', { fill: C.medBlue,  bold: true, color: 'FFFFFF', w: SC3, size: SZ }),
      cell('DQB Tracking',                          { fill: C.purple,   bold: true, color: 'FFFFFF', w: SC4, size: SZ }),
    ]}),
    ...LESSONS.map((l, i) => {
      const isOdd = i % 2 === 0;
      const rowFill = isOdd ? C.white : C.grey;
      const lt = lessonTitles[i];
      // Only L1 is pre-filled
      if (i === 0) {
        return new TableRow({ children: [
          cell(lt.col1,  { fill: C.lightBlue, bold: true, w: SLW, size: SZ }),
          cell(l.summaryTablePrompt.observed,  { fill: rowFill, w: SC1, size: SZ }),
          cell(l.summaryTablePrompt.learned,   { fill: rowFill, w: SC2, size: SZ }),
          cell(l.summaryTablePrompt.explained, { fill: rowFill, w: SC3, size: SZ }),
          cell(lt.dqb,   { fill: C.lightPurple, w: SC4, size: SZ }),
        ]});
      }
      return new TableRow({ children: [
        cell(lt.col1, { fill: C.lightBlue, bold: true, w: SLW, size: SZ }),
        cell('',      { fill: rowFill, w: SC1, size: SZ }),
        cell('',      { fill: rowFill, w: SC2, size: SZ }),
        cell('',      { fill: rowFill, w: SC3, size: SZ }),
        cell(lt.dqb,  { fill: C.lightPurple, w: SC4, size: SZ }),
      ]});
    }),
  ], [SLW, SC1, SC2, SC3, SC4]);

  const body = [
    ...titleBlock('SUMMARY TABLE: BIOLOGY GRADE 10 -- PLANT NUTRITION', 'Sub-Strand 2.1: Nutrition -- Teacher Reference'),
    SPACE(),
    headerTable,
    SPACE(),
    instrTable,
    SPACE(),
    mainTable,
  ];

  return new Document({
    sections: [{
      properties: {
        page: {
          size: { width: 12240, height: 15840, orientation: PageOrientation.LANDSCAPE },
          margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 },
        },
      },
      children: body,
    }],
  });
}

// ─── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  const [sow, fe, st] = await Promise.all([buildSoW(), buildFinalExplanation(), buildSummaryTable()]);
  await Promise.all([
    Packer.toBuffer(sow).then(b => fs.writeFileSync(path.join(OUT_DOCX, 'Biology_PlantNutrition_CBE_LessonSequence_L1-12.docx'), b)),
    Packer.toBuffer(fe).then(b => fs.writeFileSync(path.join(OUT_DOCX, 'Biology_PlantNutrition_FinalExplanation.docx'), b)),
    Packer.toBuffer(st).then(b => fs.writeFileSync(path.join(OUT_DOCX, 'Biology_PlantNutrition_SummaryTable.docx'), b)),
  ]);
  console.log('Done: Biology 2.1 Plant Nutrition -- all 3 docx files written.');
}
main().catch(console.error);
"""

with open('C:/users/mrkni/cbe-generation-system/generators/biology_2_1_plant_nutrition.js', 'a') as f:
    f.write(builders)
print("Builders written")
