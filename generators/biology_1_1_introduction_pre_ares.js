'use strict';
/**
 * Generator: Biology Grade 10 — Sub-Strand 1.1: Introduction to Biology
 *
 * No teacher template exists — phenomenon and storyline invented from KICD curriculum.
 * Phenomenon: The fall armyworm (Spodoptera frugiperda) invasion of Kenya (2017–present).
 *
 * Outputs (in data/outputs/docx/):
 *   1. Biology_Introduction_CBE_LessonSequence.docx   (SoW — teacher-facing)
 *   2. Biology_Introduction_FinalExplanation.docx     (student-facing assessment)
 *   3. Biology_Introduction_SummaryTable.docx         (student portfolio)
 */

const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, AlignmentType, ShadingType, VerticalAlign, BorderStyle,
  PageOrientation,
} = require('docx');
const fs   = require('fs');
const path = require('path');

const OUT = path.join(__dirname, '..', 'data', 'outputs', 'docx', 'Grade 10 Bio', 'Bio 1.1');
if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });

// ─── Colours ────────────────────────────────────────────────────────────────
const C = {
  darkBlue:    '1F3864',
  medBlue:     '2E75B6',
  lightBlue:   'D5E8F0',
  teal:        '1F6B75',
  lightTeal:   'D9EEF1',
  green:       '375623',
  lightGreen:  'E2EFDA',
  orange:      'C55A11',
  lightOrange: 'FCE4D6',
  purple:      '7030A0',
  lightPurple: 'EAD1F5',
  grey:        'F2F2F2',
  white:       'FFFFFF',
};

const PHASE_COLOUR = {
  'Predict Phase':                         C.lightPurple,
  'Observe Phase':                         C.lightTeal,
  'Explain Phase':                         C.lightGreen,
  'Driving Question Board (DQB) Creation': C.lightOrange,
  'Model Building Phase':                  C.lightBlue,
};

// ─── Page / type constants ───────────────────────────────────────────────────
const W    = 13680;
const FONT = 'Arial';
const SZ   = 18;
const SZ_H = 22;
const SZ_T = 28;

// ─── Helpers ─────────────────────────────────────────────────────────────────

function para(text, opts = {}) {
  return new Paragraph({
    alignment: opts.align || AlignmentType.LEFT,
    spacing:   { after: opts.after ?? 60, before: opts.before ?? 0 },
    children:  [new TextRun({
      text, font: FONT, size: opts.size || SZ,
      bold: opts.bold || false, color: opts.color || '000000', italics: opts.italic || false,
    })],
  });
}

function bullet(text, opts = {}) {
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { after: 30, before: 0 },
    indent:  { left: 360, hanging: 180 },
    children: [new TextRun({
      text: '\u2013  ' + text, font: FONT,
      size: opts.size || SZ, bold: opts.bold || false, color: opts.color || '000000',
    })],
  });
}

function cell(content, opts = {}) {
  const { fill = C.white, w = null, span = 1, vAlign = VerticalAlign.TOP,
          bold = false, color = '000000', size = SZ, align = AlignmentType.LEFT, italic = false } = opts;
  let children;
  if (typeof content === 'string') {
    children = content === ''
      ? [para('', { size })]
      : content.split('\n').map(line =>
          (line.startsWith('• ') || line.startsWith('- '))
            ? bullet(line.slice(2), { size, bold, color })
            : para(line, { size, bold, color, align, italic, after: 40 })
        );
  } else if (Array.isArray(content)) {
    children = content;
  } else {
    children = [content];
  }
  const def = {
    verticalAlign: vAlign,
    shading: { type: ShadingType.CLEAR, color: 'auto', fill },
    margins: { top: 60, bottom: 60, left: 120, right: 120 },
    children,
  };
  if (w !== null) def.width = { size: w, type: WidthType.DXA };
  if (span > 1)   def.columnSpan = span;
  return new TableCell(def);
}

function fullHeader(text, fill, textColor = 'FFFFFF', size = SZ_H, numCols = 2) {
  return new TableRow({
    children: [cell(text, { fill, color: textColor, bold: true, size, align: AlignmentType.CENTER, span: numCols, w: W })],
  });
}

function labelRow(label, content, labelW = 3000, opts = {}) {
  const cw = W - labelW;
  return new TableRow({ children: [
    cell(label,   { fill: opts.labelFill   || C.lightBlue, bold: true, w: labelW, size: SZ }),
    cell(content, { fill: opts.contentFill || C.white,     w: cw,      size: SZ }),
  ]});
}

function makeTable(rows, columnWidths = [W]) {
  const tableW = columnWidths.reduce((a, b) => a + b, 0);
  return new Table({
    width: { size: tableW, type: WidthType.DXA },
    columnWidths,
    borders: {
      top:     { style: BorderStyle.SINGLE, size: 4, color: 'AAAAAA' },
      bottom:  { style: BorderStyle.SINGLE, size: 4, color: 'AAAAAA' },
      left:    { style: BorderStyle.SINGLE, size: 4, color: 'AAAAAA' },
      right:   { style: BorderStyle.SINGLE, size: 4, color: 'AAAAAA' },
      insideH: { style: BorderStyle.SINGLE, size: 2, color: 'CCCCCC' },
      insideV: { style: BorderStyle.SINGLE, size: 2, color: 'CCCCCC' },
    },
    rows,
  });
}

const SPACE = () => para('', { after: 120 });

// ─── Section builders ────────────────────────────────────────────────────────

function titleBlock(title, subtitle) {
  return [
    para(title,    { bold: true, size: SZ_T, color: C.darkBlue, align: AlignmentType.CENTER, after: 80 }),
    para(subtitle, { size: SZ_H, color: C.teal, align: AlignmentType.CENTER, after: 160 }),
  ];
}

function subStrandOverview(unit) {
  const LW = 3000, CW = W - 3000;
  return makeTable([
    fullHeader('SUB-STRAND OVERVIEW', C.darkBlue, 'FFFFFF', SZ_H, 2),
    labelRow('Grade Level',   unit.gradeLevel, LW),
    labelRow('Subject',       unit.subject, LW),
    labelRow('Strand',        unit.strand, LW),
    labelRow('Sub-Strand',    unit.substrand, LW),
    labelRow('Learning Outcomes', unit.learningOutcomes, LW, { labelFill: C.lightBlue }),
    labelRow('Core Competencies', unit.coreCompetencies, LW, { labelFill: C.lightBlue }),
    labelRow('Values',            unit.values,            LW, { labelFill: C.lightGreen }),
    labelRow('Science & Engineering Practices', unit.sep, LW, { labelFill: C.lightTeal }),
    labelRow('Pertinent & Contemporary Issues (PCIs)', unit.pcis, LW, { labelFill: C.lightOrange }),
    labelRow('Career Connections', unit.careers, LW, { labelFill: C.lightBlue }),
    labelRow('Focus for Lessons',  unit.focus,   LW),
    labelRow('Total Duration',     unit.totalDuration, LW),
    labelRow('Anchoring Phenomenon',   unit.phenomenon,          LW, { labelFill: C.lightPurple }),
    labelRow('Supporting Phenomena',   unit.supportingPhenomena, LW, { labelFill: C.lightPurple }),
    labelRow('Storyline Thread',       unit.storyline,           LW, { labelFill: C.lightTeal }),
    labelRow('Key Inquiry Questions / Driving Question', unit.drivingQuestion, LW, { labelFill: C.lightPurple }),
  ], [LW, CW]);
}

function sectionA(lesson) {
  const LW = 2400, CW = W - LW;
  return makeTable([
    fullHeader(`LESSON ${lesson.number} (${lesson.duration}): ${lesson.title}`, C.darkBlue, 'FFFFFF', SZ_H, 2),
    fullHeader('A. SPECIFIC LEARNING OUTCOMES', C.teal, 'FFFFFF', SZ_H, 2),
    new TableRow({ children: [
      cell('Category', { fill: C.medBlue, bold: true, color: 'FFFFFF', w: LW, size: SZ }),
      cell('Specific Learning Outcomes', { fill: C.medBlue, bold: true, color: 'FFFFFF', w: CW, size: SZ }),
    ]}),
    labelRow('Purpose',              lesson.slo.purpose,           LW, { labelFill: C.lightBlue }),
    labelRow('Knowledge',            lesson.slo.knowledge,         LW, { labelFill: C.lightBlue }),
    labelRow('Skills',               lesson.slo.skills,            LW, { labelFill: C.lightBlue }),
    labelRow('Attitudes',            lesson.slo.attitudes,         LW, { labelFill: C.lightGreen }),
    labelRow('Key Inquiry Question', lesson.slo.keyInquiry,        LW, { labelFill: C.lightPurple }),
    labelRow('Purpose in Storyline', lesson.slo.purposeInStoryline,LW, { labelFill: C.lightTeal }),
    labelRow('Safety Notes',         lesson.slo.safetyNotes,       LW, { labelFill: C.lightOrange }),
  ], [LW, CW]);
}

function sectionB(lesson) {
  return makeTable([
    fullHeader('B. LESSON OVERVIEW', C.teal, 'FFFFFF', SZ_H, 1),
    new TableRow({ children: [cell(lesson.overview, { fill: C.white, w: W, size: SZ })] }),
  ], [W]);
}

function sectionC(lesson) {
  const cw = [900, 2556, 2556, 2556, 2556, 2556];
  return makeTable([
    fullHeader('C. LESSON IMPLEMENTATION FRAMEWORK', C.teal, 'FFFFFF', SZ_H, 6),
    new TableRow({ children: [
      cell('Phase',                         { fill: C.darkBlue, bold: true, color: 'FFFFFF', w: cw[0], size: SZ }),
      cell('Learner Experience',            { fill: C.medBlue,  bold: true, color: 'FFFFFF', w: cw[1], size: SZ }),
      cell('Resource',                      { fill: C.teal,     bold: true, color: 'FFFFFF', w: cw[2], size: SZ }),
      cell('Teacher Moves',                 { fill: C.medBlue,  bold: true, color: 'FFFFFF', w: cw[3], size: SZ }),
      cell('Sensemaking Strategy',          { fill: C.teal,     bold: true, color: 'FFFFFF', w: cw[4], size: SZ }),
      cell('Formative Assessment Strategy', { fill: C.medBlue,  bold: true, color: 'FFFFFF', w: cw[5], size: SZ }),
    ]}),
    ...lesson.framework.map(ph => new TableRow({ children: [
      cell(ph.phase,               { fill: PHASE_COLOUR[ph.phase] || C.grey, bold: true, w: cw[0], size: SZ }),
      cell(ph.learnerExperience,   { fill: C.white, w: cw[1], size: SZ }),
      cell(ph.resource,            { fill: C.grey,  w: cw[2], size: SZ }),
      cell(ph.teacherMoves,        { fill: C.white, w: cw[3], size: SZ }),
      cell(ph.sensemakingStrategy, { fill: C.grey,  w: cw[4], size: SZ }),
      cell(ph.formativeAssessment, { fill: C.white, w: cw[5], size: SZ }),
    ]})),
  ], cw);
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

function differentiationTable() {
  const LW = 3000, HW = (W - LW) / 2;
  return makeTable([
    fullHeader('DIFFERENTIATION AND INCLUSION', C.darkBlue, 'FFFFFF', SZ_H, 3),
    new TableRow({ children: [
      cell('Learner Need',         { fill: C.medBlue, bold: true, color: 'FFFFFF', w: LW, size: SZ }),
      cell('Support Strategies',   { fill: C.teal,    bold: true, color: 'FFFFFF', w: HW, size: SZ }),
      cell('Extension Strategies', { fill: C.medBlue, bold: true, color: 'FFFFFF', w: HW, size: SZ }),
    ]}),
    new TableRow({ children: [
      cell('Learners with limited literacy or English proficiency', { fill: C.lightBlue, w: LW, size: SZ }),
      cell(
        '• Use images and visual career cards instead of text-heavy research\n' +
        '• Provide a bilingual (English/Swahili) glossary of biology field names\n' +
        '• Allow group discussion in Swahili before presenting in English\n' +
        '• Pre-fill part of the career wheel with examples',
        { fill: C.white, w: HW, size: SZ }),
      cell(
        '• Research a Kenyan biologist and present a short biography to the class\n' +
        '• Write a persuasive essay: "Why every student should study Biology"',
        { fill: C.grey, w: HW, size: SZ }),
    ]}),
    new TableRow({ children: [
      cell('Learners who are uncertain about career choices', { fill: C.lightBlue, w: LW, size: SZ }),
      cell(
        '• Provide a career interest checklist with biology-related roles\n' +
        '• Focus on a single biology field per discussion (not all 12 at once)\n' +
        '• Use the armyworm case study as a concrete context for each career',
        { fill: C.white, w: HW, size: SZ }),
      cell(
        '• Map out a full career pathway: secondary school → university → career\n' +
        '• Interview a community member with a biology-related career',
        { fill: C.grey, w: HW, size: SZ }),
    ]}),
    new TableRow({ children: [
      cell('Advanced learners', { fill: C.lightBlue, w: LW, size: SZ }),
      cell(
        '• Peer-mentor groups during the career wheel activity\n' +
        '• Act as discussion facilitator during the resource person session',
        { fill: C.white, w: HW, size: SZ }),
      cell(
        '• Research the latest fall armyworm biological control methods in Kenya\n' +
        '• Design a "Biology Response Team" for a new pest or disease outbreak\n' +
        '• Investigate a Kenyan biology career not covered in class',
        { fill: C.grey, w: HW, size: SZ }),
    ]}),
  ], [LW, HW, HW]);
}

// ─── Unit Data ───────────────────────────────────────────────────────────────

const UNIT = {
  gradeLevel: '10',
  subject:    'Biology',
  strand:     'Strand 1.0: Cell Biology and Biodiversity',
  substrand:  'Sub-Strand 1.1: Introduction to Biology',
  learningOutcomes:
    'By the end of this sub-strand, the learner should be able to:\n' +
    '• a) Explain the application of Biology in everyday life\n' +
    '• b) Relate fields of study in Biology to career opportunities\n' +
    '• c) Illustrate the careers related to fields of study in Biology\n' +
    '• d) Appreciate the importance of Biology in everyday life',
  coreCompetencies:
    '• Imagination and Creativity — designing career wheels, visualising prospective fields and careers\n' +
    '• Self-Efficacy — developing self-awareness about personal strengths and career pathways\n' +
    '• Communication and Collaboration — group research, presentations, discussions\n' +
    '• Critical Thinking and Problem Solving — analysing how multiple biology fields address a real crisis\n' +
    '• Digital Literacy — searching for information from safe internet sources, using biology apps',
  values:
    '• Respect — appreciating diverse career ambitions and opinions during discussions\n' +
    '• Responsibility — using safe and reliable internet sources for biology research\n' +
    '• Integrity — honestly assessing personal interests and abilities in career planning\n' +
    '• Unity — collaborating in groups to research biology fields and present findings',
  sep:
    '• Asking Questions — generating DQB questions from the armyworm phenomenon\n' +
    '• Obtaining, Evaluating and Communicating Information — researching biology fields from multiple sources\n' +
    '• Constructing Explanations — explaining how biology fields collectively address real-world problems\n' +
    '• Engaging in Argument from Evidence — debating factors that should/should not influence career choice',
  pcis:
    '• Environmental Conservation — using locally available materials for career wheel; understanding biology\'s role in conservation\n' +
    '• Safety and Security — searching for information from safe internet sites only\n' +
    '• Food Security — understanding how biology (entomology, genetics, biochemistry) protects Kenya\'s food supply\n' +
    '• Gender and Inclusivity — challenging stereotypes that restrict career choices in biology',
  careers:
    '• Entomologist — studies insects; identified the fall armyworm and its life cycle\n' +
    '• Agricultural Scientist — develops crop-protection strategies for Kenyan farmers\n' +
    '• Ecologist — tracks how species spread across ecosystems\n' +
    '• Biochemist — develops and tests pesticides and biological control agents\n' +
    '• Microbiologist — develops Bt (Bacillus thuringiensis) biological controls\n' +
    '• Geneticist — studies pesticide resistance in armyworm populations\n' +
    '• Medical Doctor / Public Health Officer — links food security to human health\n' +
    '• Environmental Consultant — advises on sustainable pest management',
  focus:
    'This unit answers the question every new biology student asks: "Why do I need to study this?" ' +
    'Using the fall armyworm crisis as the anchoring context, students discover that biology is not ' +
    'a collection of facts to memorise — it is a toolkit for understanding and solving real problems ' +
    'that affect their families and communities. They explore the major fields of biology, the careers ' +
    'each field opens, and the factors that should (and should NOT) influence their own career choices.',
  totalDuration: '6 lessons (approximately 6 periods × 40 minutes = 240 minutes)',
  phenomenon:
    'THE FALL ARMYWORM INVASION OF KENYA\n\n' +
    'In 2017, the fall armyworm (Spodoptera frugiperda) — a moth caterpillar originally from the Americas — ' +
    'was detected in Kenya for the first time. Within months it had spread to all 47 counties, ' +
    'destroying maize crops across the country. Farmers who had grown maize for generations ' +
    'watched their fields disappear overnight. The Kenyan government declared a national emergency.\n\n' +
    'Stopping it required scientists from at least SIX different fields of biology working together:\n' +
    '• Entomologists identified the species and its life cycle\n' +
    '• Ecologists tracked how it spread across the continent\n' +
    '• Geneticists studied why some populations were resistant to pesticides\n' +
    '• Biochemists developed targeted control chemicals\n' +
    '• Microbiologists produced biological control agents (Bt bacteria)\n' +
    '• Agricultural scientists trained farmers on management strategies\n\n' +
    'This is why we study Biology.',
  supportingPhenomena:
    '• Why do maize plants turn brown and "shredded" from the inside — but the caterpillar hides inside the leaf whorl?\n' +
    '• Why did the same pesticides that worked in 2017 stop working by 2020? (Resistance — genetics)\n' +
    '• Why does spraying Bt bacteria on the crop kill the armyworm but NOT the birds that eat the dead caterpillars? (Specificity — microbiology)\n' +
    '• Why does the armyworm travel 500 km overnight? (Wind currents — ecology/meteorology)\n' +
    '• How does eating armyworm-damaged maize affect human nutrition? (Mycotoxins — biochemistry/public health)',
  storyline:
    'Lesson 1: Students observe images and video of armyworm damage. They cannot explain it yet. DQB launched. Initial model drawn: "What do I think biology is?"\n\n' +
    'Lesson 2: Students discover the 12 major fields of biology and map them to the armyworm problem — which field does which job?\n\n' +
    'Lesson 3: Students explore how biology appears in their own everyday lives — from the food they eat to the medicines they take.\n\n' +
    'Lesson 4: Students investigate careers in biology — real Kenyan scientists, what they studied, and how they ended up helping with the armyworm crisis. Challenge to gender/culture stereotypes.\n\n' +
    'Lesson 5: Students explore how technology amplifies biology — apps, biotechnology, data science — and how Kenyan farmers now use digital tools to report and manage armyworm.\n\n' +
    'Lesson 6: Students synthesise everything: map all 6+ biology fields that addressed the armyworm crisis, write their final explanation of "Why study Biology?", and present their career wheel.',
  drivingQuestion:
    'DRIVING QUESTION (invented): Why did a tiny caterpillar threaten Kenya\'s food supply — and what do biologists know that can help?\n\n' +
    'KICD KEY INQUIRY QUESTION:\n' +
    '1. Why is it important to study Biology?',
};

// ─── Lesson Data ─────────────────────────────────────────────────────────────

const LESSONS = [

  // ── LESSON 1 ──────────────────────────────────────────────────────────────
  {
    number: 1,
    title:    'The Armyworm Invasion — What is Biology and Why Does it Matter?',
    duration: '1 period / 40 minutes',
    slo: {
      purpose: 'Launch the unit with a compelling, real Kenyan crisis. Activate prior knowledge about biology. Create initial model. Start the DQB.',
      knowledge:
        '• State that Biology is the scientific study of living organisms\n' +
        '• Recognise that biology has many different fields, each with a different focus\n' +
        '• Name at least 3 real-world contexts where biology knowledge is applied',
      skills:
        '• Observe photographs and video of the armyworm invasion and make systematic observations\n' +
        '• Generate scientific questions from a real-world stimulus\n' +
        '• Draw an initial model showing current understanding of what biology is',
      attitudes:
        '• Curiosity about a real, unresolved problem affecting Kenya\n' +
        '• Openness to the idea that biology is relevant to everyday life\n' +
        '• Empathy for farmers affected by the armyworm crisis',
      keyInquiry: 'Why is it important to study Biology?',
      purposeInStoryline:
        'This lesson LAUNCHES the unit. The armyworm crisis makes the abstract question "Why study biology?" ' +
        'concrete and urgent. Students confront a real problem — one their families may have experienced — ' +
        'and quickly discover they cannot explain it without biology knowledge. The DQB captures their initial ' +
        'questions. These questions drive the next 5 lessons.',
      safetyNotes: 'No practical in this lesson. Internet searches should use approved sites only.',
    },
    overview:
      'Students open the unit by viewing a set of photographs showing: (1) a healthy Kenyan maize field, ' +
      '(2) the same field after armyworm attack — leaves shredded, crops destroyed, (3) a close-up of the ' +
      'fall armyworm caterpillar, and (4) a map showing its spread across all 47 Kenyan counties in 2017. ' +
      'No explanation is given. Students are asked simply: "What do you notice? What do you wonder? ' +
      'What do you know that could explain this?" They write individual responses, share in pairs, ' +
      'then post questions on the Driving Question Board.\n\n' +
      'The lesson ends with a direct-instruction moment: "The name for the scientific study of living ' +
      'things is Biology. The armyworm is a living thing. Every question on this DQB is a biology question. ' +
      'Over the next 6 lessons, we are going to learn what biologists know — and how they use that ' +
      'knowledge to protect Kenya\'s food supply."',
    framework: [
      {
        phase: 'Predict Phase',
        learnerExperience:
          'Students view the 4-image sequence in silence (healthy field → destroyed field → armyworm → spread map). ' +
          'Individually write: (1) What do I notice? (2) What is causing this? (3) What do I think biology is?',
        resource:
          'IMAGE SET: 4 printed or projected images (healthy maize, destroyed maize, armyworm caterpillar, spread map)\n' +
          'SOURCE: CIMMYT Kenya / FAO armyworm resources (available offline)\n' +
          'TYPE: Visual stimulus',
        teacherMoves:
          '"Look at these images. Do NOT talk yet. Just observe."\n' +
          'After 60 seconds: "Write what you notice. Write what you think is happening."\n' +
          'WAIT TIME: 90 seconds of silent writing.\n' +
          '"Now — has anyone in your family seen this in their maize? What happened?"',
        sensemakingStrategy:
          'POE — PREDICT:\n' +
          'Students must commit to a prediction before any instruction. ' +
          'Personal connection (family farming) makes the phenomenon emotionally real.',
        formativeAssessment:
          'Observe written responses: Do students connect the damage to a living thing (caterpillar)?\n' +
          'Note prior knowledge level — some students may know the armyworm by name.',
      },
      {
        phase: 'Observe Phase',
        learnerExperience:
          'Think-Pair-Share: Partners compare observations. ' +
          'Class shares — teacher records ALL ideas on board without evaluation. ' +
          '"What questions do you have?" Students generate questions freely.',
        resource:
          'MATERIALS: Board/chart paper for recording student ideas\n' +
          'OPTIONAL VIDEO: 2-min armyworm damage footage (FAO Africa Armyworm)\n' +
          'TYPE: Discussion',
        teacherMoves:
          '"Share one thing your partner noticed that you did not."\n' +
          'Cold-call 5 pairs. Record every idea.\n' +
          '"What question would you most want answered?"\n' +
          'Record questions separately — these will go on the DQB.',
        sensemakingStrategy:
          'Think-Pair-Share:\n' +
          'Surfacing prior knowledge WITHOUT judgment. Teacher records wrong ideas alongside right ones — all are valuable.',
        formativeAssessment:
          'Question quality: Are students asking about causes, solutions, biology mechanisms?\n' +
          'Watch for: "Why doesn\'t the government do something?" → connect to biology careers and solutions.',
      },
      {
        phase: 'Explain Phase',
        learnerExperience:
          'Teacher introduces: "This is called the fall armyworm. It came from the Americas. ' +
          'Scientists from SIX different areas of biology had to work together to understand and fight it. ' +
          'Let\'s look at what those areas are." Brief introduction: biology = scientific study of living things. ' +
          'Preview of 6 fields that helped: entomology, ecology, genetics, biochemistry, microbiology, agriculture.',
        resource:
          'VISUAL: Simple hexagonal diagram showing 6 biology fields around the armyworm image\n' +
          'TYPE: Teacher-created visual / whiteboard diagram',
        teacherMoves:
          '"Six different types of biologists worked on this problem. Here is what each one studies."\n' +
          'Point to each field. Ask: "Which of these sounds most interesting to you? Why?"\n' +
          'WAIT TIME: 15 seconds before responses.\n' +
          '"We will look at each of these in detail in Lessons 2 and 4."',
        sensemakingStrategy:
          'Preview Framework:\n' +
          'Students see the unit\'s whole arc from Lesson 1. This reduces cognitive load — ' +
          'they know where the unit is going.',
        formativeAssessment:
          'Show of hands: "Has anyone heard of any of these biology fields before?" ' +
          'Note which fields students already know — this informs Lesson 2 pacing.',
      },
      {
        phase: 'Driving Question Board (DQB) Creation',
        learnerExperience:
          'Each student writes 1–2 questions on sticky notes. ' +
          'Categories: WHY (the armyworm causes damage), HOW (biologists study/fight it), WHAT (biology fields/careers). ' +
          'Students post questions on the class DQB.',
        resource:
          'MATERIALS: Sticky notes (3 colours if available), large poster, markers\n' +
          'DQB POSTER: Pre-labelled with WHY / HOW / WHAT categories\n' +
          'TYPE: Class artefact (stays on wall for all 6 lessons)',
        teacherMoves:
          '"Write your two most burning questions about the armyworm or about biology. One per sticky note."\n' +
          'WAIT TIME: 2 minutes.\n' +
          '"Post them under the right category. Read your question aloud as you post it."\n' +
          '"We are going to answer EVERY one of these by Lesson 6."',
        sensemakingStrategy:
          'Driving Question Board:\n' +
          'Students own their questions. The DQB is a living document — questions get answered across all 6 lessons.',
        formativeAssessment:
          'Question richness: Do questions span WHY, HOW, and WHAT?\n' +
          'Very simple questions (e.g., "What is the armyworm?") = students need more scaffolding.\n' +
          'Complex questions (e.g., "Why are some armyworms resistant to pesticides?") = strong prior knowledge.',
      },
      {
        phase: 'Model Building Phase',
        learnerExperience:
          'Students draw their INITIAL MODEL: "What is Biology? What does a biologist do?" ' +
          'Label anything they know. Date the model. ' +
          '"This is your starting point. We will improve this model every lesson."',
        resource:
          'MATERIALS: Blank A4 paper, pencil/pen\n' +
          'PROMPT: "Draw: what is biology? Who is a biologist? What do they study?"\n' +
          'TYPE: Student portfolio artefact',
        teacherMoves:
          '"Do not look anything up. Draw what YOU think right now."\n' +
          '"You can use words, diagrams, or pictures — whatever makes sense to you."\n' +
          '"Share your model with your partner. Explain it in 20 seconds."',
        sensemakingStrategy:
          'Initial Modelling — externalising current mental model.\n' +
          'This is a baseline. Students will revise it after every lesson.',
        formativeAssessment:
          'What do students show biology as? (only plants/animals? only hospitals? just a book?)\n' +
          'This reveals the scope of their prior conception of biology.',
      },
    ],
    teacherReflection:
      'After teaching this lesson, reflect on:\n\n' +
      '1. Did the armyworm images generate genuine curiosity? Did students make a personal connection (family farmers)?\n\n' +
      '2. What biology knowledge did students already have? Were there surprises in their prior knowledge level?\n\n' +
      '3. Quality of DQB questions — are they biologically motivated or mostly about farming/government response?\n\n' +
      '4. What did initial models show? Did students have a narrow view of biology (only one field)?\n\n' +
      '5. Did the preview of 6 biology fields make students curious about specific fields? Which ones got the most reaction?\n\n' +
      '6. How would you adjust the pacing if students had strong prior knowledge of the armyworm?',
    summaryTablePrompt: {
      observed:
        'Images of Kenyan maize fields destroyed by fall armyworm. ' +
        'Spread map showing armyworm in all 47 counties by 2017. ' +
        'Six biology fields involved in responding: entomology, ecology, genetics, biochemistry, microbiology, agriculture. ' +
        'DQB started. Initial model of biology drawn.',
      learned:
        'Biology = the scientific study of living organisms. ' +
        'Biology has many specialised fields, each studying a different aspect of life. ' +
        'The armyworm crisis required MULTIPLE biology fields working together — no one field could solve it alone.',
      explained:
        'The armyworm is a LIVING THING — so biology is the right tool to understand it. ' +
        'But we do not know yet WHICH biology fields do WHAT, or how they helped. ' +
        'That is what Lessons 2–5 will reveal.',
    },
  },

  // ── LESSON 2 ──────────────────────────────────────────────────────────────
  {
    number: 2,
    title:    'Fields of Study in Biology — Who Studies What?',
    duration: '1 period / 40 minutes',
    slo: {
      purpose: 'Students learn the 12 major fields of biology and map each one to the armyworm crisis — making the abstract field list concrete and memorable.',
      knowledge:
        '• Name the 12 major fields of biology: Botany, Zoology, Taxonomy, Anatomy, Physiology, Ecology, Biochemistry, Biotechnology, Genetics, Parasitology, Microbiology, Entomology\n' +
        '• Describe the focus of each field in one sentence\n' +
        '• Match at least 6 fields to their contribution to the armyworm response',
      skills:
        '• Collaboratively research biology fields using print and digital sources\n' +
        '• Design a career wheel linking biology fields to careers\n' +
        '• Present findings clearly to peers',
      attitudes:
        '• Appreciation for the breadth and diversity of biology as a discipline\n' +
        '• Recognition that many career paths are connected to biology\n' +
        '• Curiosity about which field most matches personal interests',
      keyInquiry: 'Why is it important to study Biology?',
      purposeInStoryline:
        'Students move from the problem (armyworm crisis) to the tools (biology fields). ' +
        'The career wheel activity makes the connection between field and career tangible. ' +
        'The armyworm is the anchor — every field is introduced through its role in the crisis response.',
      safetyNotes: 'Safe internet searching applies. Use approved sites (Kenya government, FAO, universities).',
    },
    overview:
      'Students work in expert groups — each group is assigned 3–4 biology fields to research. ' +
      'They answer: "What does this field study?" and "How did this field help with the armyworm crisis?" ' +
      'Groups present their fields in a jigsaw, and the class builds a shared "Biology Fields Map" — ' +
      'a large visual showing all 12 fields connected to the armyworm in the centre.\n\n' +
      'The lesson closes with each student beginning a personal career wheel: a circular diagram showing ' +
      'biology fields radiating outward to careers. By Lesson 4, this wheel will be complete. ' +
      'The DQB is updated — questions like "What is entomology?" can now be moved to ANSWERED.',
    framework: [
      {
        phase: 'Predict Phase',
        learnerExperience:
          'Students receive 12 field name cards (Botany, Zoology, Taxonomy, etc.). ' +
          '"Before we research — just from the name, what do you THINK each field studies?" ' +
          'Groups sort cards and write brief guesses for each field.',
        resource:
          'MATERIAL: 12 pre-printed field name cards (one set per group)\n' +
          'TYPE: Card sort / vocabulary prediction',
        teacherMoves:
          '"Just from the word itself — what clues does each name give you?"\n' +
          '"Entomology — what does \'entomo\' remind you of? Microbiology — what is \'micro\'?"\n' +
          'WAIT TIME: 2 minutes for group prediction.',
        sensemakingStrategy:
          'Vocabulary Prediction:\n' +
          'Using word roots (Greek/Latin) to predict meanings before research. ' +
          'This builds vocabulary strategies alongside content.',
        formativeAssessment:
          'Which fields do groups correctly predict? (Botany, Zoology, Microbiology often correct.) ' +
          'Note fields with wrong predictions — these need more explicit coverage during jigsaw.',
      },
      {
        phase: 'Observe Phase',
        learnerExperience:
          'JIGSAW RESEARCH: Expert groups research their assigned fields (3–4 fields each). ' +
          'For each field: (1) What does it study? (2) Who in Kenya does this work? (3) How did it help with the armyworm?\n' +
          'Groups A: Botany, Zoology, Taxonomy | Groups B: Anatomy, Physiology, Ecology | ' +
          'Groups C: Biochemistry, Genetics, Microbiology | Groups D: Biotechnology, Parasitology, Entomology',
        resource:
          'SOURCES: Printed field description cards, Rachel offline resources, approved websites\n' +
          'OPTIONAL: Khan Academy Biology overview videos\n' +
          'TYPE: Research activity (15 min)',
        teacherMoves:
          '"You have 15 minutes. Answer all 3 questions for each of your fields."\n' +
          'Circulate. Prompt: "Can you give a Kenyan example for that field?"\n' +
          '"Who might have this career in Kenya — what would their workplace look like?"',
        sensemakingStrategy:
          'Expert Jigsaw:\n' +
          'Each group becomes expert in a set of fields, then teaches the rest of the class.\n' +
          'Anchoring to the armyworm gives every field a concrete example.',
        formativeAssessment:
          'Group expert cards: accuracy of field definitions and armyworm connections.\n' +
          'Check: Can students explain WHY each field was needed (not just what it is)?',
      },
      {
        phase: 'Explain Phase',
        learnerExperience:
          'Home groups reconvene — each expert teaches their fields. ' +
          'Class builds a shared Biology Fields Map: large paper with armyworm image in the centre, ' +
          '12 fields radiating outward, careers at the edges. ' +
          '"Which 6 fields do you think contributed most to solving the armyworm crisis?"',
        resource:
          'MATERIAL: Large sheet of paper (A1 or chart paper), markers\n' +
          'REFERENCE: Completed expert cards from research phase\n' +
          'TYPE: Collaborative mapping activity',
        teacherMoves:
          '"Each expert: teach your fields in 2 minutes. Focus on the armyworm connection."\n' +
          'After jigsaw: "Now let\'s map it. Who puts Entomology first? Justification?"\n' +
          'Build the map collaboratively. Ask: "Are any of these fields connected to each other?"',
        sensemakingStrategy:
          'Knowledge Mapping:\n' +
          'The visual map makes the relationships between fields and the crisis explicit. ' +
          'Students see that science is interconnected, not isolated subjects.',
        formativeAssessment:
          'Map completeness and accuracy.\n' +
          'Can students articulate the armyworm connection for each field?\n' +
          'Spot-check: "Why was genetics needed? What specifically did geneticists study?"',
      },
      {
        phase: 'Driving Question Board (DQB) Creation',
        learnerExperience:
          'DQB update: Move answered questions ("What is entomology?", "What fields study insects?") to ANSWERED. ' +
          'Add new questions from the jigsaw: "How do biochemists make pesticides?" "What is Bt bacteria?"',
        resource:
          'MATERIALS: DQB poster, sticky notes\n' +
          'TYPE: Class artefact update',
        teacherMoves:
          '"Which Lesson 1 questions can we answer now?" (Review DQB — 3 minutes.)\n' +
          '"What new questions did today\'s research raise? Post them."',
        sensemakingStrategy:
          'DQB Update — students see their knowledge growing: fewer unanswered questions, but also deeper questions arising.',
        formativeAssessment:
          'Are new questions more sophisticated than Lesson 1 questions? (They should be — moving from "What is biology?" to "How does X work?")',
      },
      {
        phase: 'Model Building Phase',
        learnerExperience:
          'Students UPDATE their initial biology model: add the 12 fields as "branches" of biology. ' +
          'Circle the 3 fields they find most interesting. ' +
          'Begin Career Wheel: draw a circle, add the 12 fields radiating outward. ' +
          'Leave space for careers to be added in Lesson 4.',
        resource:
          'MATERIALS: Student initial model, blank A4 paper for career wheel\n' +
          'TYPE: Student portfolio additions',
        teacherMoves:
          '"Update your model — biology is bigger than you thought, yes?"\n' +
          '"Start your career wheel. In Lesson 4, we add the careers. For now, just the 12 fields."\n' +
          '"Circle the field you find most interesting. Why that one?"',
        sensemakingStrategy:
          'Progressive Model Building — students see their model of biology expanding with each lesson.',
        formativeAssessment:
          'Career wheel accuracy: Are all 12 fields correctly placed?\n' +
          'Interest circles: What fields do students gravitate toward? (Informs differentiation in Lesson 4.)',
      },
    ],
    teacherReflection:
      'After teaching this lesson, reflect on:\n\n' +
      '1. Did the jigsaw work effectively? Were all groups able to explain their fields accurately to the class?\n\n' +
      '2. Which biology fields caused most confusion? (Common: Parasitology, Taxonomy, Biochemistry)\n\n' +
      '3. Could students articulate the specific armyworm connection for most fields?\n\n' +
      '4. What did students find most surprising about the range of biology fields?\n\n' +
      '5. Were there gender patterns in which fields students circled as "most interesting"? Did you address stereotypes?\n\n' +
      '6. Were 40 minutes enough for jigsaw + map + model update? What would you trim?',
    summaryTablePrompt: {
      observed:
        'Researched 12 fields of biology in expert groups: Botany, Zoology, Taxonomy, Anatomy, Physiology, Ecology, Biochemistry, Biotechnology, Genetics, Parasitology, Microbiology, Entomology. ' +
        'Built a class Biology Fields Map linking each field to the armyworm crisis. ' +
        'Started personal career wheel.',
      learned:
        'Biology has 12 major fields — each focuses on a different aspect of living organisms. ' +
        'Entomology = insects; Ecology = how organisms interact with their environment; Genetics = inherited traits; Biochemistry = chemical processes in cells. ' +
        'At least 6 fields were needed to respond to the armyworm crisis.',
      explained:
        'The armyworm problem could not be solved by ONE biology field alone. ' +
        'Each field contributed different knowledge. ' +
        'This is why biology has so many specialisations — each one gives scientists a different tool for understanding life.',
    },
  },

  // ── LESSON 3 ──────────────────────────────────────────────────────────────
  {
    number: 3,
    title:    'Biology in Everyday Life — From Farm to Clinic to Forest',
    duration: '1 period / 40 minutes',
    slo: {
      purpose: 'Students connect biology to contexts beyond the armyworm — showing that biology is present in food, medicine, the environment, and technology in their daily lives.',
      knowledge:
        '• Give at least 3 examples of biology applied in agriculture in Kenya\n' +
        '• Give at least 3 examples of biology applied in medicine/public health\n' +
        '• Give at least 2 examples of biology applied in environmental management\n' +
        '• Explain that biology knowledge underlies practices students experience every day',
      skills:
        '• Connect biology fields to real applications in Kenyan life\n' +
        '• Research examples from local context (food, health, environment)\n' +
        '• Present examples clearly with evidence',
      attitudes:
        '• Appreciation that biology is not an abstract school subject — it is in daily life\n' +
        '• Recognition that biology knowledge improves lives in Kenya\n' +
        '• Curiosity about the biological processes behind familiar things',
      keyInquiry: 'Why is it important to study Biology?',
      purposeInStoryline:
        'Students broaden from the armyworm (one application) to the full range of biology applications. ' +
        'This lesson answers: "But what if I don\'t want to work with armyworms?" — there are biology careers in every sector of Kenyan society.',
      safetyNotes: 'No practical in this lesson. Internet research: approved sources only.',
    },
    overview:
      'Students work in three thematic groups — Agriculture, Medicine & Health, Environment. ' +
      'Each group researches how biology is applied in their theme, specifically in Kenya. ' +
      'They then present to the class using the structure: "What is the application? What biology knowledge makes it possible? ' +
      'What would happen WITHOUT that biology knowledge?"\n\n' +
      'A class gallery walk follows: groups post their findings and rotate to read each other\'s work. ' +
      'The lesson closes with a whole-class synthesis: "In how many ways does biology affect your life ' +
      'between waking up and going to sleep on a typical school day in Kenya?"',
    framework: [
      {
        phase: 'Predict Phase',
        learnerExperience:
          '"Think about your morning today. From the moment you woke up to arriving at school — ' +
          'how many times did you interact with something that required biology knowledge to produce?" ' +
          'Individual brainstorm (2 minutes). Share with partner.',
        resource:
          'PROMPT CARD: "Think of: food you ate, medicine you take, water you drank, materials around you"\n' +
          'TYPE: Personal reflection prompt',
        teacherMoves:
          '"Your morning routine — how much of it depends on biology? Think carefully."\n' +
          'WAIT TIME: 2 minutes.\n' +
          '"Share: what did your partner come up with that you had not thought of?"',
        sensemakingStrategy:
          'Personal Connection:\n' +
          'Anchoring biology to the student\'s own morning makes the abstract concept of "application" tangible.',
        formativeAssessment:
          'Range of examples: Do students go beyond food to medicines, clothing (cotton), water treatment? ' +
          'This shows depth of conception of biology\'s reach.',
      },
      {
        phase: 'Observe Phase',
        learnerExperience:
          'GROUP RESEARCH: Three groups, each investigating biology applications in one sector:\n' +
          'GROUP A — Agriculture: crop improvement, pest management, animal husbandry, fisheries\n' +
          'GROUP B — Medicine & Health: disease treatment, vaccines, genetics, nutrition, public health\n' +
          'GROUP C — Environment: conservation, pollution management, invasive species, water treatment\n' +
          'Each group finds 5 specific Kenyan examples and answers: What biology field? What application? What impact?',
        resource:
          'SOURCES: Rachel offline content, printed article extracts, approved websites\n' +
          'SUGGESTED EXAMPLES:\n' +
          'Agriculture: tissue culture bananas (biotechnology), Bt maize (genetics), dairy improvement\n' +
          'Medicine: malaria treatment, Kenya\'s covid vaccine research, sickle cell screening\n' +
          'Environment: Lake Victoria water hyacinth management, Mara River conservation\n' +
          'TYPE: Group research (15 min)',
        teacherMoves:
          '"Find specifically KENYAN examples. Generic answers ("biology is used in medicine") are not enough."\n' +
          '"For each example: name the biology field, name the application, explain the impact on Kenyan people."\n' +
          'Circulate and prompt: "Who actually does this in Kenya? Is there a Kenyan institution involved?"',
        sensemakingStrategy:
          'Kenya-Contextualised Research:\n' +
          'Requiring Kenyan examples prevents students from copying generic content. ' +
          'It builds pride in Kenyan science and grounds biology in local reality.',
        formativeAssessment:
          'Specificity of examples: generic (low) vs. Kenyan-specific with institution/person named (high).\n' +
          'Biology field identified: Can students match their example to a specific field from Lesson 2?',
      },
      {
        phase: 'Explain Phase',
        learnerExperience:
          'GALLERY WALK: Each group posts their 5 examples on the wall. ' +
          'Groups rotate: read, add sticky note comments, mark their favourite example with a star. ' +
          'Whole-class debrief: "Which examples surprised you most? Which showed biology closest to your own life?"',
        resource:
          'MATERIALS: Group research posters/sheets, sticky notes for comments\n' +
          'TYPE: Gallery walk',
        teacherMoves:
          '"Walk around. Read every example. Write ONE comment on another group\'s poster."\n' +
          'After rotation: "What surprised you? What did you not know before?"\n' +
          '"Now — back to our armyworm. Which of these applications ALSO helped with the armyworm?"',
        sensemakingStrategy:
          'Gallery Walk + Armyworm Return:\n' +
          'The return to the armyworm connects the broad survey back to the unit\'s anchoring phenomenon.',
        formativeAssessment:
          'Sticky note quality: Do comments show understanding or just praise?\n' +
          'Discussion: Can students link gallery examples back to the armyworm crisis?',
      },
      {
        phase: 'Driving Question Board (DQB) Creation',
        learnerExperience:
          'DQB update: Are there any Lesson 1 questions about applications of biology that can now be answered? ' +
          'New questions: "How does Kenya produce tissue culture bananas?" "Who funds biology research in Kenya?"',
        resource:
          'MATERIALS: DQB poster, sticky notes\n' +
          'TYPE: Class artefact update',
        teacherMoves:
          '"Review the DQB — which questions about biology applications can we answer now?"\n' +
          '"What new questions arose from today\'s research? Post them."',
        sensemakingStrategy:
          'DQB Update — students see the breadth of biology applications reflected in their own questions.',
        formativeAssessment:
          'Are new questions moving toward careers and specific mechanisms? (Positive progression.)',
      },
      {
        phase: 'Model Building Phase',
        learnerExperience:
          'Students UPDATE their model of biology: add the three application sectors (Agriculture, Medicine, Environment) ' +
          'around the outside of the 12-field diagram. Draw arrows connecting fields to applications. ' +
          '"Add one personal example — something in YOUR life that biology explains."',
        resource:
          'MATERIALS: Student model portfolio\n' +
          'TYPE: Portfolio update',
        teacherMoves:
          '"Add the three application sectors to your model. Connect them to the fields that make them possible."\n' +
          '"Add your personal example — the most surprising thing from today."',
        sensemakingStrategy:
          'Personalised Model — students add something from their own life, making the model uniquely theirs.',
        formativeAssessment:
          'Personal example chosen: Does it show genuine understanding of biology\'s reach?',
      },
    ],
    teacherReflection:
      'After teaching this lesson, reflect on:\n\n' +
      '1. Were students able to find genuinely Kenyan examples? What resources were most useful?\n\n' +
      '2. Which sector (Agriculture/Medicine/Environment) generated the most engagement? Why?\n\n' +
      '3. Did students make the connection back to the armyworm phenomenon during the debrief?\n\n' +
      '4. What surprised students most — something they did not know had biology behind it?\n\n' +
      '5. Were students beginning to see biology as personally relevant, not just an academic subject?\n\n' +
      '6. What would you add or remove if you had more/less than 40 minutes?',
    summaryTablePrompt: {
      observed:
        'Researched biology applications in Agriculture, Medicine, and Environment — specifically in Kenya. ' +
        'Examples: tissue culture bananas (biotechnology), malaria treatment (pharmacology), ' +
        'Lake Victoria water hyacinth management (ecology). ' +
        'Gallery walk: read and commented on 10+ examples from other groups.',
      learned:
        'Biology is applied in agriculture (crop improvement, pest management, animal science), ' +
        'medicine (disease treatment, vaccines, genetics), and the environment (conservation, pollution control, invasive species). ' +
        'Every sector of Kenyan life depends on biology knowledge.',
      explained:
        'The armyworm crisis is just ONE example of biology in action. ' +
        'Biology is in the food Kenyans eat, the medicine they take, and the environment they live in. ' +
        'This is why studying biology matters — it is not abstract knowledge, it is the knowledge that keeps people alive and healthy.',
    },
  },

  // ── LESSON 4 ──────────────────────────────────────────────────────────────
  {
    number: 4,
    title:    'Careers in Biology — Kenyan Scientists Who Made a Difference',
    duration: '1 period / 40 minutes',
    slo: {
      purpose: 'Students investigate real biology careers — specifically profiling Kenyan scientists — and critically examine which factors should and should not determine career choice.',
      knowledge:
        '• Name at least 6 careers directly related to biology fields\n' +
        '• Identify factors that should influence career choice: interest, ability, opportunity\n' +
        '• Identify factors that should NOT influence career choice: gender, culture, disability, stereotypes',
      skills:
        '• Research a biology-related career using print and digital sources\n' +
        '• Complete a career wheel connecting 12 fields to specific job roles\n' +
        '• Communicate career information clearly through a brief presentation',
      attitudes:
        '• Appreciation that biology careers are open to all genders, cultures, and backgrounds\n' +
        '• Developing self-awareness about personal strengths and interests relevant to biology\n' +
        '• Inspiration from Kenyan scientists who have made a difference',
      keyInquiry: 'Why is it important to study Biology?',
      purposeInStoryline:
        'Students now see that "Why study biology?" has a personal dimension: it opens career paths. ' +
        'Using Kenyan scientists as models makes these paths real and attainable. ' +
        'The critical discussion of stereotypes ensures all students see themselves in these careers.',
      safetyNotes: 'Internet searches: approved sites only. Handle sensitive career/gender discussions with respect for all opinions.',
    },
    overview:
      'The lesson opens with brief profiles of 4 Kenyan scientists in biology-related careers: ' +
      'a female Kenyan entomologist who worked on the armyworm response, a male Kenyan oncologist, ' +
      'a Kenyan conservation biologist working in the Maasai Mara, and a Kenyan biochemist. ' +
      'Students discuss: "What path did each one take? What attracted them to their field?"\n\n' +
      'Students then research one additional career of their choice, complete their career wheel, ' +
      'and present it to a partner. The lesson includes a structured discussion on career choice factors — ' +
      'what SHOULD influence your choice (interest, ability) vs. what should NOT (gender, cultural stereotypes, ' +
      'peer pressure, disability). A resource person (if available) or their video testimony closes the lesson.',
    framework: [
      {
        phase: 'Predict Phase',
        learnerExperience:
          '"Without looking anything up — what biology career would YOU choose right now, if you had to?\n' +
          'Write it down. Write why. Write what you think you would do every day in that career."\n' +
          'Individual 60-second response.',
        resource:
          'MATERIALS: Student notebook\n' +
          'TYPE: Personal reflection',
        teacherMoves:
          '"No wrong answers. First instinct only. Go."\n' +
          'WAIT TIME: 60 seconds.\n' +
          '"What factors made you choose that career — not what is realistic, but what pulled you toward it?"',
        sensemakingStrategy:
          'Self-Efficacy Prompt:\n' +
          'Students articulate their own interest before external influences (peers, teacher) shape their response.',
        formativeAssessment:
          'Diversity of choices: Are students drawn to a wide range of careers or clustering?\n' +
          'Stated reasons: interest-based (good) vs. perceived earnings/status only (needs broadening).',
      },
      {
        phase: 'Observe Phase',
        learnerExperience:
          'KENYAN SCIENTIST PROFILES: Each group receives 1 scientist profile card:\n' +
          'Profile A: Dr. Esther Ngumbi — Kenyan entomologist, studied armyworm and plant-insect interactions at University of Illinois\n' +
          'Profile B: Dr. Farouk Mbaruk — Kenyan surgeon/medical scientist, cancer research at Aga Khan Hospital\n' +
          'Profile C: Female Kenyan conservation biologist (composite profile) — Maasai Mara wildlife monitoring\n' +
          'Profile D: Kenyan biochemist (composite profile) — develops pesticide formulations\n' +
          'Groups answer: What field? What did they study? How did they get there? What challenges?',
        resource:
          'MATERIAL: Printed scientist profile cards (teacher-prepared)\n' +
          'OPTIONAL: Short video testimony from a Kenyan biologist (2 min)\n' +
          'TYPE: Case study research',
        teacherMoves:
          '"Read the profile. Imagine this person\'s daily work. What would you find exciting? Challenging?"\n' +
          '"Notice: what subject did they study at secondary school? What degree? What job?"\n' +
          '"Did gender, ethnicity, or background stop any of them?"',
        sensemakingStrategy:
          'Role Model Profiling:\n' +
          'Research shows students are more likely to pursue careers where they see people like themselves. ' +
          'Kenyan-specific profiles are essential.',
        formativeAssessment:
          'Group understanding of career pathway: Can they explain how the scientist moved from secondary school to career?\n' +
          'Did students notice the diversity of gender/background in the profiles?',
      },
      {
        phase: 'Explain Phase',
        learnerExperience:
          'WHOLE CLASS: Career choice factors discussion.\n' +
          '"What factors SHOULD influence your biology career choice?"\n' +
          '"What factors should NOT?"\n' +
          'Class creates two columns on the board: SHOULD / SHOULD NOT.\n' +
          'Students complete their career wheel: 12 fields → specific careers written at the outer rim.',
        resource:
          'BOARD: Two-column chart (SHOULD / SHOULD NOT influence career choice)\n' +
          'STUDENT RESOURCE: Career wheel template (from Lesson 2)\n' +
          'TYPE: Class discussion + individual completion',
        teacherMoves:
          '"What should influence your career choice? Call out ideas."\n' +
          'Record: interest, ability, values, opportunity.\n' +
          '"What should NOT? What do you think society sometimes says, wrongly?"\n' +
          'Record: gender, culture, ethnicity, disability, stereotype.\n' +
          '"Why is it important to remove these barriers? Who does Kenya lose if we do not?"',
        sensemakingStrategy:
          'Structured Controversy:\n' +
          'Students examine cultural assumptions that may limit career choices. ' +
          'This is explicitly mandated by KICD as a PCI.',
        formativeAssessment:
          'Can students articulate WHY gender stereotypes in career choice are harmful (not just that they are wrong)?\n' +
          'Career wheel completeness: All 12 fields with at least one career each.',
      },
      {
        phase: 'Driving Question Board (DQB) Creation',
        learnerExperience:
          'DQB update: Move career-related questions from Lesson 1 to ANSWERED. ' +
          'Add new: "How do I become an entomologist in Kenya?" "Which universities offer ecology degrees?" ' +
          '"Can I combine biology and technology?"',
        resource:
          'MATERIALS: DQB poster\n' +
          'TYPE: Class artefact update',
        teacherMoves:
          '"Career questions from Day 1 — can we answer them now?"\n' +
          '"Add your new career questions. We might answer some in Lesson 5."',
        sensemakingStrategy:
          'DQB as Career Planning Tool — students begin to use the DQB for genuine self-exploration.',
        formativeAssessment:
          'Are new questions personal and specific ("How do I...") rather than generic? Positive development.',
      },
      {
        phase: 'Model Building Phase',
        learnerExperience:
          'Students COMPLETE their career wheel: 12 biology fields, careers at outer ring, ' +
          'personal STAR on the career they are most drawn to. ' +
          'Write beside the star: "I am drawn to this because..."',
        resource:
          'MATERIALS: Career wheel (in progress since Lesson 2)\n' +
          'TYPE: Portfolio artefact — completed career wheel',
        teacherMoves:
          '"Complete your career wheel today. This stays in your portfolio."\n' +
          '"Put a star on your top career. Write WHY. And — is there anything stopping you? Should it?"',
        sensemakingStrategy:
          'Self-Reflection Model: students articulate personal interest alongside any perceived barriers.',
        formativeAssessment:
          'Career wheel completeness and accuracy.\n' +
          'Star career and "why" statement: Is it interest-based?',
      },
    ],
    teacherReflection:
      'After teaching this lesson, reflect on:\n\n' +
      '1. Did the Kenyan scientist profiles inspire students? Which profile generated most discussion?\n\n' +
      '2. How was the career factors discussion? Did students feel safe enough to name gender stereotypes honestly?\n\n' +
      '3. Were there gendered patterns in the careers students starred? How did you address this?\n\n' +
      '4. Were all students able to complete their career wheel? What gaps remained?\n\n' +
      '5. If a resource person was available — what was the most impactful thing they said?\n\n' +
      '6. What do you wish you had more time to cover?',
    summaryTablePrompt: {
      observed:
        'Profiled 4 Kenyan scientists in biology careers: entomologist (Dr. Esther Ngumbi), medical scientist, conservation biologist, biochemist. ' +
        'Discussed career choice factors: interest and ability SHOULD guide choice; gender, culture, stereotypes should NOT. ' +
        'Completed career wheel — all 12 fields with careers at outer ring.',
      learned:
        'Biology opens many career paths in Kenya: entomologist, ecologist, biochemist, geneticist, medical scientist, conservation biologist, agricultural scientist, and more. ' +
        'Career choices should be guided by personal interest and ability — not gender, cultural stereotypes, or disability. ' +
        'Kenyan scientists are contributing to solving Kenya\'s biggest challenges.',
      explained:
        'The armyworm response involved Kenyan biologists in multiple career roles — entomologists, ecologists, biochemists. ' +
        'These are real career options, accessible regardless of gender or background. ' +
        'Studying biology is the first step toward any of these careers.',
    },
  },

  // ── LESSON 5 ──────────────────────────────────────────────────────────────
  {
    number: 5,
    title:    'Biology and Technology — Modern Tools for Modern Problems',
    duration: '1 period / 40 minutes',
    slo: {
      purpose: 'Students explore how technology amplifies biology — from digital field tools to biotechnology — making biology more powerful and opening new career paths.',
      knowledge:
        '• Define biotechnology as the use of living organisms or biological processes to develop products\n' +
        '• Give at least 3 examples of biotechnology in Kenya (tissue culture bananas, Bt crops, biological pest control)\n' +
        '• Name digital tools used by biologists (species ID apps, GPS tracking, satellite data)\n' +
        '• Explain how technology helped track and manage the armyworm invasion',
      skills:
        '• Use or demonstrate a biology digital tool (iNaturalist app or similar)\n' +
        '• Research one biotechnology application used in Kenya\n' +
        '• Evaluate: does this technology help or harm — who benefits, who might not?',
      attitudes:
        '• Appreciation that modern biology is inseparable from technology\n' +
        '• Critical thinking about the benefits and limitations of biotechnology\n' +
        '• Curiosity about technology-based biology careers',
      keyInquiry: 'Why is it important to study Biology?',
      purposeInStoryline:
        'The armyworm response used technology: satellite tracking, smartphone apps for farmer reporting, ' +
        'biotechnology for biological control. This lesson shows that biology careers in the 21st century ' +
        'require both biological knowledge AND technological skill — addressing DQB questions about modern careers.',
      safetyNotes: 'Internet access: approved sources only. Any discussion of GM crops should be balanced — present both scientific consensus and public debate.',
    },
    overview:
      'The lesson opens with the question: "How did Kenyan farmers report armyworm sightings to scientists ' +
      'across 47 counties so quickly in 2017?" Answer: a smartphone app and SMS reporting system. ' +
      'This launches a broader exploration of how technology connects with biology.\n\n' +
      'Students explore three technology areas: (1) Digital field tools — species identification apps, ' +
      'GPS, satellite monitoring; (2) Biotechnology — tissue culture, biological pest control with Bt bacteria, ' +
      'GM crops; (3) Data science in biology — how large datasets help track disease and species. ' +
      'The lesson includes a critical discussion: technology has benefits but also raises ethical questions, ' +
      'particularly around GM crops in Kenya.',
    framework: [
      {
        phase: 'Predict Phase',
        learnerExperience:
          '"In 2017, the armyworm spread across all 47 counties in weeks. How did scientists track it so quickly across such a large area? ' +
          'What technology could help? Predict 3 tools or technologies a biologist might use."',
        resource:
          'MATERIALS: Student notebook\n' +
          'TYPE: Prediction prompt',
        teacherMoves:
          '"Think: what technology do YOU use every day? Could any of that be used in biology?"\n' +
          'WAIT TIME: 90 seconds.\n' +
          '"Share predictions. I will record them — let\'s see which ones are correct."',
        sensemakingStrategy:
          'Technology Prediction:\n' +
          'Students transfer knowledge of familiar technology (smartphones, internet) to a biology context.',
        formativeAssessment:
          'Do students predict smartphones and apps? Satellite imagery? GPS? ' +
          'Note which tech tools students are already familiar with.',
      },
      {
        phase: 'Observe Phase',
        learnerExperience:
          'THREE STATIONS (rotate every 8 minutes):\n' +
          'Station 1 — Digital Tools: Explore the iNaturalist app (offline demo) and a GPS tracking example. ' +
          'How are these used in biology fieldwork?\n' +
          'Station 2 — Biotechnology: Read a case study on tissue culture bananas in Kenya and Bt (Bacillus thuringiensis) ' +
          'biological pest control used against armyworm.\n' +
          'Station 3 — Data Science: Look at a map of armyworm spread data collected from farmer SMS reports. ' +
          'How does data collection enable rapid scientific response?',
        resource:
          'Station 1: iNaturalist app (Rachel offline) or printed screenshots\n' +
          'Station 2: Printed case study — Kenya tissue culture banana programme (KARI)\n' +
          'Station 3: Printed armyworm spread map with data points from farmer reports\n' +
          'TYPE: Station rotation (24 min)',
        teacherMoves:
          'Brief intro at each station: "What is this tool? What biology question does it help answer?"\n' +
          'Circulate. Prompt: "Is this technology available to all Kenyan farmers? What are the barriers?"\n' +
          '"Who decides how this technology is used? Who benefits most?"',
        sensemakingStrategy:
          'Station Rotation:\n' +
          'Three different modalities (app demo, reading, data analysis) in one lesson. ' +
          'Students process technology from multiple angles.',
        formativeAssessment:
          'Station exit cards: one fact and one question per station.\n' +
          'Equity question: Did students consider who has access to technology?',
      },
      {
        phase: 'Explain Phase',
        learnerExperience:
          'Whole-class discussion: "Is biotechnology always good? Let\'s think about GM crops in Kenya."\n' +
          'Students hear both sides: scientific consensus (safe, productive) and public concerns (cultural, economic, environmental). ' +
          '"What biology knowledge do you need to evaluate this debate?"',
        resource:
          'REFERENCE: Short summary of GM crop debate in Kenya (balanced, 1 page)\n' +
          'TYPE: Structured debate discussion',
        teacherMoves:
          '"I want you to argue BOTH sides. Not what you personally believe — both sides."\n' +
          '"What would a geneticist say? What would an environmentalist say? What would a farmer say?"\n' +
          '"Biology knowledge is what lets you evaluate this debate properly. Without it, you cannot judge."',
        sensemakingStrategy:
          'Structured Academic Controversy:\n' +
          'Students argue both sides of a real Kenyan science debate. ' +
          'This develops critical thinking AND shows why biology knowledge matters for citizenship.',
        formativeAssessment:
          'Can students articulate at least one argument from EACH side?\n' +
          'Do they connect the debate back to biology knowledge as the tool for evaluating it?',
      },
      {
        phase: 'Driving Question Board (DQB) Creation',
        learnerExperience:
          'DQB update: Move technology-related questions to ANSWERED ("How did they track the armyworm?"). ' +
          'Add new: "Are GM crops safe for Kenya?" "What biology and tech careers can I combine?"',
        resource:
          'MATERIALS: DQB poster\n' +
          'TYPE: Class artefact update',
        teacherMoves:
          '"Which DQB questions can we now answer about technology and biology?"\n' +
          '"What new questions did today raise? Post the most important one."',
        sensemakingStrategy:
          'DQB Near-Completion: Students can see most original questions are answered — building confidence before Lesson 6 synthesis.',
        formativeAssessment:
          'Remaining unanswered questions — are they specific enough for Lesson 6 to address?',
      },
      {
        phase: 'Model Building Phase',
        learnerExperience:
          'Students add a "TECHNOLOGY LAYER" to their biology model: ' +
          'draw a ring around the 12-field diagram showing technologies connected to each field. ' +
          'Annotate career wheel: add "Tech Skills Needed" beside their starred career.',
        resource:
          'MATERIALS: Student model portfolio, career wheel\n' +
          'TYPE: Portfolio update',
        teacherMoves:
          '"Add technology to your model of biology. Biology does not work without technology any more — show that."\n' +
          '"On your career wheel: what tech skills would you need for your starred career?"',
        sensemakingStrategy:
          'Model Elaboration: Students see biology expanding to include technology — their model of the field grows more sophisticated.',
        formativeAssessment:
          'Technology connections: Are they specific (e.g., "Ecologists use GPS and satellite data") or generic ("technology is used")?',
      },
    ],
    teacherReflection:
      'After teaching this lesson, reflect on:\n\n' +
      '1. Did the station rotation manage student energy well? Was 8 minutes enough at each station?\n\n' +
      '2. Were students able to evaluate the GM crop debate from both sides? Did biology knowledge feel relevant to the debate?\n\n' +
      '3. Did students consider equity — who has access to technology and who does not?\n\n' +
      '4. Were students excited about tech-biology career combinations? Which ones were most popular?\n\n' +
      '5. What technology do students already use that could be biology-relevant (e.g., farming apps, health apps)?\n\n' +
      '6. What would you change about the station rotation structure?',
    summaryTablePrompt: {
      observed:
        'Explored three technology areas: digital field tools (iNaturalist, GPS), biotechnology (tissue culture bananas, Bt biological control), and data science (armyworm spread map from farmer SMS reports). ' +
        'Discussed GM crop debate — argued both sides. ' +
        'Added technology layer to biology model.',
      learned:
        'Biotechnology = using living organisms or biological processes to make products. ' +
        'Examples in Kenya: tissue culture bananas (disease-free planting material), Bt bacteria (biological armyworm control), farmer SMS reporting systems. ' +
        'Modern biology requires both biological knowledge AND technological skills.',
      explained:
        'Technology made the armyworm response faster and more effective: farmers reported sightings via SMS, scientists tracked spread via satellite, biological control (Bt) provided a safer alternative to chemical pesticides. ' +
        'Biology and technology together are more powerful than either alone.',
    },
  },

  // ── LESSON 6 ──────────────────────────────────────────────────────────────
  {
    number: 6,
    title:    'Final Synthesis — Why Study Biology? Answering the Driving Question',
    duration: '2 periods / 80 minutes',
    slo: {
      purpose: 'Students synthesise all 5 lessons of evidence to write a complete, evidence-based answer to the unit\'s driving question and present their career wheel.',
      knowledge:
        '• Articulate at least 5 specific reasons why biology is important, with Kenyan examples\n' +
        '• Name the 12 major fields of biology from memory\n' +
        '• Connect the armyworm crisis to at least 6 biology fields\n' +
        '• Explain what factors should and should not determine biology career choices',
      skills:
        '• Write a structured evidence-based explanation of why biology matters\n' +
        '• Present a completed career wheel clearly and confidently\n' +
        '• Synthesise evidence from all 5 lessons into a coherent argument',
      attitudes:
        '• A genuine sense of why biology is worth studying — connected to Kenya and to personal future\n' +
        '• Confidence in expressing a career direction\n' +
        '• Appreciation for the collective effort of multiple biology fields to solve real problems',
      keyInquiry: 'Why is it important to study Biology?',
      purposeInStoryline:
        'This lesson is the CAPSTONE. Students return to the armyworm images from Lesson 1 — ' +
        'they now have everything needed to explain what happened and why biology was essential. ' +
        'The DQB is closed. The career wheel is presented. The Final Explanation is written.',
      safetyNotes: 'No practical. Standard classroom conduct.',
    },
    overview:
      'The lesson opens with the Lesson 1 armyworm images — shown again without comment. ' +
      '"Look at these. What can you explain now that you could not explain in Lesson 1?" ' +
      'Students narrate: which biology fields are involved, what each one contributed, ' +
      'what technology was used, what careers exist in this response.\n\n' +
      'Students then write their Final Explanation (individual, structured writing) and present ' +
      'their career wheel to a partner. The DQB is reviewed one final time — every question answered. ' +
      'The lesson closes with a whole-class discussion: "One year from now, what will you remember ' +
      'about this unit? Why does biology matter to YOUR life?"',
    framework: [
      {
        phase: 'Predict Phase',
        learnerExperience:
          '"We are going back to where we started. Look at the armyworm images from Lesson 1."\n' +
          '"In 60 seconds — tell your partner EVERYTHING you now know about what is happening in these images."\n' +
          '"How much more can you say than in Lesson 1?"',
        resource:
          'IMAGES: Same 4 armyworm images from Lesson 1 (healthy field, destroyed field, caterpillar, spread map)\n' +
          'TYPE: Return to phenomenon — full-circle moment',
        teacherMoves:
          '"Same images. Different you. Go — narrate everything you know."\n' +
          'WAIT TIME: 60 seconds per pair.\n' +
          '"Who can explain what the spread map tells us — in biology terms?"',
        sensemakingStrategy:
          'Return to Phenomenon:\n' +
          'Students experience their own growth. The contrast between Lesson 1 confusion and now competence is motivating and memorable.',
        formativeAssessment:
          'Partner narration quality: Do students use biology field names? Career names? Technology names?\n' +
          'This is a quick formative check of the whole unit\'s learning.',
      },
      {
        phase: 'Observe Phase',
        learnerExperience:
          'FINAL EXPLANATION WRITING (30 minutes):\n' +
          'Students write a complete answer to "Why is it important to study Biology?" using:\n' +
          '• Their Summary Table (all 5 lessons)\n' +
          '• Their completed career wheel\n' +
          '• Their biology model (Lessons 1–5)\n' +
          '• Evidence from the armyworm case study\n' +
          'Structure: (1) What is biology? (2) Why does it matter for Kenya? (3) What careers does it open? (4) Personal reflection.',
        resource:
          'STUDENT RESOURCES: Summary Table, career wheel, biology model portfolio\n' +
          'WRITING PROMPT: Final Explanation template (distributed today)\n' +
          'TYPE: Individual extended writing',
        teacherMoves:
          '"Use everything. Reference lessons by name: \'In Lesson 3, I learned...\' \'The armyworm case shows...\'"\n' +
          '"This is not a test. It is your chance to show everything you understand."\n' +
          'Circulate. Prompt struggling students: "Tell me one reason biology matters in Kenya. Write that."',
        sensemakingStrategy:
          'Synthesis Writing:\n' +
          'Writing forces integration of all prior learning. ' +
          'The structured template (4-part) guides without constraining.',
        formativeAssessment:
          'Walking observation during writing: Are students citing lesson evidence specifically?\n' +
          'Are they using biology field names correctly?\n' +
          'Final Explanation = summative assessment for this sub-strand.',
      },
      {
        phase: 'Explain Phase',
        learnerExperience:
          'CAREER WHEEL PRESENTATIONS (pairs):\n' +
          'Each student presents their career wheel to a partner (2 minutes each):\n' +
          '"Here are the 12 fields. Here is the career I am most interested in. Here is why. ' +
          'Here is the biology knowledge and technology skill I would need."\n' +
          'Partner gives one piece of positive feedback and one question.',
        resource:
          'MATERIALS: Completed career wheel\n' +
          'TYPE: Peer presentation',
        teacherMoves:
          '"2 minutes to present. Partner: listen, then give feedback: one thing you found interesting, one question."\n' +
          'Circulate. Note interesting career choices for whole-class share.\n' +
          '"I am going to ask 3 of you to share your career and one reason with the whole class."',
        sensemakingStrategy:
          'Peer Teaching — presenting to a partner requires consolidation and articulation of understanding.',
        formativeAssessment:
          'Career wheel accuracy and completion.\n' +
          'Quality of "why" statement: interest-based and evidence-linked?',
      },
      {
        phase: 'Driving Question Board (DQB) Creation',
        learnerExperience:
          'FINAL DQB REVIEW:\n' +
          'Every student writes one card: "I can now answer the driving question. The answer is:..."\n' +
          'Cards posted on DQB. Teacher reads 4–5 aloud.\n' +
          'Every remaining question moved to ANSWERED.\n' +
          '"If there are questions still unanswered — those are invitations to study more biology."',
        resource:
          'MATERIALS: Index cards, DQB poster\n' +
          'TYPE: Culminating DQB celebration',
        teacherMoves:
          '"Write your one-sentence answer to \'Why is it important to study Biology?\' Be specific. Be Kenyan."\n' +
          'Read 5 cards aloud. Ask: "What evidence supports this answer?"\n' +
          '"Look at our DQB from Day 1. We answered them all. That is what biology does."',
        sensemakingStrategy:
          'DQB Culmination — closing the board gives students concrete evidence of their own learning journey.',
        formativeAssessment:
          'One-sentence answer quality: Does it cite specific biology knowledge, Kenya context, and personal connection?',
      },
      {
        phase: 'Model Building Phase',
        learnerExperience:
          'FINAL MODEL:\n' +
          'Students draw their FINAL model of biology — showing: ' +
          '12 fields, 3 application sectors, technology layer, careers, and their personal starred career. ' +
          'Compare to Lesson 1 initial model side by side.\n' +
          '"Write 3 sentences: My understanding of biology changed because..."',
        resource:
          'MATERIALS: Student model portfolio (all lessons), blank A4 paper for final model\n' +
          'TYPE: Portfolio capstone',
        teacherMoves:
          '"Draw your final model. It should look very different from Lesson 1. Show everything."\n' +
          '"Compare them side by side. Write your 3-sentence reflection."\n' +
          '"This portfolio is yours. What you built here is the beginning of your biology education."',
        sensemakingStrategy:
          'Model Comparison Reflection: Students explicitly see and articulate their own conceptual growth.',
        formativeAssessment:
          'Final model completeness vs. initial model.\n' +
          'Reflection quality: Does it show genuine understanding of how their view of biology changed?',
      },
    ],
    teacherReflection:
      'After teaching this unit, reflect on:\n\n' +
      '1. When students looked at the Lesson 1 armyworm images a second time — how much richer was their narration? Were you satisfied with the growth?\n\n' +
      '2. Quality of Final Explanations: Did students cite specific lesson evidence? Use biology field names correctly?\n\n' +
      '3. Career wheel presentations: Were students confident? Was there diversity in career choices? Did gender stereotypes emerge?\n\n' +
      '4. DQB final celebration: Did students feel a sense of accomplishment?\n\n' +
      '5. Looking across all 6 lessons: what was the strongest lesson? The weakest? What would you restructure?\n\n' +
      '6. Did the armyworm phenomenon work as an anchor? Would you use it again or choose a different phenomenon?',
    summaryTablePrompt: {
      observed:
        'Returned to armyworm images from Lesson 1 — narrated with full biology knowledge from 5 lessons. ' +
        'Wrote Final Explanation: "Why is it important to study Biology?" (using Summary Table, career wheel, model portfolio). ' +
        'Presented career wheel to partner. ' +
        'Final DQB review — every question answered.',
      learned:
        'Biology is important because: (1) it explains living organisms including pests, diseases, crops, and the human body; (2) it is applied in agriculture, medicine, and environmental management; (3) it opens diverse careers in Kenya; (4) it drives biotechnology and digital tools that address national challenges; (5) its many fields work together — no single field can solve complex problems alone.',
      explained:
        'COMPLETE ANSWER: The fall armyworm threatened Kenya\'s food supply because no one had the biology knowledge to understand or stop it at first. Once entomologists identified it, ecologists tracked it, geneticists studied its resistance, biochemists developed controls, microbiologists produced Bt, and agricultural scientists trained farmers — the outbreak was managed. This is why we study biology: it is Kenya\'s toolkit for understanding and protecting life.',
    },
  },

]; // end LESSONS

// ─── SoW Builder ─────────────────────────────────────────────────────────────

async function buildSoW() {
  const body = [
    ...titleBlock(
      'BIOLOGY GRADE 10: INTRODUCTION TO BIOLOGY',
      'CBE Phenomenon-Driven Lesson Sequence — Sub-Strand 1.1 (6 Lessons)'
    ),
    SPACE(),
    subStrandOverview(UNIT),
    SPACE(),
  ];
  for (const lesson of LESSONS) {
    body.push(
      SPACE(), sectionA(lesson),
      SPACE(), sectionB(lesson),
      SPACE(), sectionC(lesson),
      SPACE(), sectionD(lesson),
      SPACE(), sectionE(lesson),
      SPACE(),
    );
  }
  body.push(SPACE(), differentiationTable());

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

// ─── Final Explanation Builder ────────────────────────────────────────────────

async function buildFinalExplanation() {
  const FLW = 3000, FCW = W - FLW;
  const RW = Math.floor((W - FLW) / 3);
  const RWr = W - FLW - RW * 2;

  const headerRows = [
    fullHeader('FINAL EXPLANATION: INTRODUCTION TO BIOLOGY', C.darkBlue, 'FFFFFF', SZ_H, 2),
    fullHeader('Biology Grade 10 — Student Assessment Document', C.teal, 'FFFFFF', SZ_H, 2),
    labelRow('Student Name', '_______________________________________________', FLW),
    labelRow('Class',        '_______________________________________________', FLW),
    labelRow('Date',         '_______________________________________________', FLW),
  ];

  const instrRows = [
    fullHeader('INSTRUCTIONS FOR STUDENTS', C.teal, 'FFFFFF', SZ_H, 1),
    new TableRow({ children: [cell(
      'Now that you have completed all 6 lessons of Introduction to Biology, write your COMPLETE EXPLANATION ' +
      'of why biology is important — using the fall armyworm as your anchoring evidence.\n\n' +
      'WHAT TO USE:\n' +
      '• Your Summary Table (all 6 lessons)\n' +
      '• Your completed career wheel\n' +
      '• Your biology model (Lessons 1–6)\n' +
      '• Evidence from all class activities\n\n' +
      'YOUR EXPLANATION MUST INCLUDE:\n' +
      '• A clear definition of Biology\n' +
      '• At least 6 fields of biology with their focus described\n' +
      '• At least 4 specific examples of biology applied in Kenya (agriculture, medicine, environment, technology)\n' +
      '• At least 3 biology careers with pathways described\n' +
      '• A discussion of factors that should and should NOT influence career choice\n' +
      '• The armyworm case study as evidence connecting all of the above\n\n' +
      'GRADING: 20 points total (see rubric below).',
      { fill: C.white, w: W, size: SZ }
    )]}),
  ];

  const parts = [
    { title: 'PART 1: WHAT IS BIOLOGY?',
      prompt: 'Define biology. Explain why it is considered a science. Give 3 examples of living organisms studied by biologists in Kenya.' },
    { title: 'PART 2: FIELDS OF BIOLOGY',
      prompt: 'Name and describe at least 8 of the 12 major fields of biology. For each field, explain its focus and give a specific example of how it was needed in the armyworm response.' },
    { title: 'PART 3: BIOLOGY IN EVERYDAY KENYAN LIFE',
      prompt: 'Explain how biology is applied in: (a) Agriculture in Kenya, (b) Medicine and public health in Kenya, (c) Environmental management in Kenya. Give 2 specific examples for each sector.' },
    { title: 'PART 4: BIOLOGY CAREERS',
      prompt: 'Describe at least 4 biology careers available in Kenya. Explain: what the person studies, what they do at work, and how they contributed to solving the armyworm crisis. Include factors that SHOULD and SHOULD NOT influence career choice.' },
    { title: 'PART 5: BIOLOGY AND TECHNOLOGY',
      prompt: 'Explain how technology strengthens biology. Give 2 specific examples from Kenya (e.g., tissue culture, Bt biological control, digital tracking). What technology skills would you need in your chosen biology career?' },
    { title: 'PART 6: WHY IS IT IMPORTANT TO STUDY BIOLOGY? — Your Complete Answer',
      prompt: 'Using ALL the evidence from Parts 1–5, write your complete answer to: "Why is it important to study Biology?" Connect your answer to Kenya, to the armyworm case, and to your own future.' },
  ];

  const rubricRows = [
    fullHeader('FINAL EXPLANATION RUBRIC (20 points)', C.darkBlue, 'FFFFFF', SZ_H, 4),
    new TableRow({ children: [
      cell('Criterion',       { fill: C.medBlue, bold: true, color: 'FFFFFF', w: FLW, size: SZ }),
      cell('Excellent (4)',   { fill: C.medBlue, bold: true, color: 'FFFFFF', w: RW,  size: SZ }),
      cell('Proficient (3)',  { fill: C.teal,    bold: true, color: 'FFFFFF', w: RW,  size: SZ }),
      cell('Developing (1–2)',{ fill: C.medBlue, bold: true, color: 'FFFFFF', w: RWr, size: SZ }),
    ]}),
    ...[
      ['Fields of Biology Knowledge',   'Names and accurately describes 10–12 fields; links all to armyworm.', 'Names 7–9 fields with mostly correct descriptions.',            'Names fewer than 7 fields or significant errors.'],
      ['Kenya Applications Evidence',   'Gives 6+ specific Kenyan examples across all 3 sectors with biology field identified.', '4–5 examples, mostly Kenyan and specific.', 'Fewer than 4 examples or generic (not Kenya-specific).'],
      ['Careers and Career Factors',    'Describes 4+ careers with pathways; clearly states should/should not factors with reasoning.', '2–3 careers described; factors listed but not explained.', 'Fewer than 2 careers or missing career factors discussion.'],
      ['Phenomenon Integration',        'Armyworm case woven through ALL 5 parts with specific evidence from every lesson.', 'Armyworm referenced in 3–4 parts with some lesson evidence.', 'Armyworm mentioned only once or not at all.'],
      ['Scientific Reasoning',          'Clear, logical argument; accurate vocabulary; well-structured response; personal reflection included.', 'Mostly logical; some vocabulary errors; basic structure.', 'Unclear argument; limited vocabulary; poor structure.'],
    ].map(([crit, exc, prof, dev]) => new TableRow({ children: [
      cell(crit, { fill: C.lightBlue, w: FLW, size: SZ }),
      cell(exc,  { fill: C.white,     w: RW,  size: SZ }),
      cell(prof, { fill: C.grey,      w: RW,  size: SZ }),
      cell(dev,  { fill: C.white,     w: RWr, size: SZ }),
    ]})),
  ];

  const body = [
    ...titleBlock('FINAL EXPLANATION: INTRODUCTION TO BIOLOGY', 'Biology Grade 10 — Student Assessment Document'),
    SPACE(),
    makeTable(headerRows, [FLW, FCW]),
    SPACE(),
    makeTable(instrRows,  [W]),
    SPACE(),
    ...parts.flatMap(p => [
      makeTable([
        fullHeader(p.title, C.medBlue, 'FFFFFF', SZ_H, 1),
        new TableRow({ children: [cell(p.prompt, { fill: C.lightBlue, w: W, size: SZ, italic: true })] }),
        new TableRow({ children: [cell('\n\n\n\n\n\n', { fill: C.white, w: W, size: SZ })] }),
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

// ─── Summary Table Builder ────────────────────────────────────────────────────

async function buildSummaryTable() {
  const SLW = 3000, SCW = W - SLW;
  const TLW = 2400;
  const TC3 = Math.floor((W - TLW) / 3);
  const TC3r = W - TLW - TC3 * 2;

  const body = [
    ...titleBlock('SUMMARY TABLE: INTRODUCTION TO BIOLOGY', 'Biology Grade 10 — Student Learning Portfolio'),
    SPACE(),
    makeTable([
      fullHeader('SUMMARY TABLE: INTRODUCTION TO BIOLOGY', C.darkBlue, 'FFFFFF', SZ_H, 2),
      fullHeader('Biology Grade 10 — Student Learning Portfolio', C.teal, 'FFFFFF', SZ_H, 2),
      labelRow('Student Name', '_______________________________________________', SLW),
      labelRow('Class',        '_______________________________________________', SLW),
      labelRow('Date Started', '_______________________________________________', SLW),
      labelRow('Date Completed', '_____________________________________________', SLW),
    ], [SLW, SCW]),
    SPACE(),
    makeTable([
      fullHeader('INSTRUCTIONS', C.teal, 'FFFFFF', SZ_H, 1),
      new TableRow({ children: [cell(
        'FOR STUDENTS:\n' +
        'Complete this row after EACH lesson. Keep it in your portfolio. ' +
        'You will use it to write your Final Explanation in Lesson 6.\n\n' +
        'FOR TEACHERS:\n' +
        'Distribute at the start of Lesson 1. Allow 5 minutes at the end of each lesson for students to complete their row.',
        { fill: C.white, w: W, size: SZ }
      )]}),
    ], [W]),
    SPACE(),
    makeTable([
      new TableRow({ children: [
        cell('Lesson / Activity',                         { fill: C.darkBlue, bold: true, color: 'FFFFFF', w: TLW, size: SZ }),
        cell('What did I observe?',                       { fill: C.medBlue,  bold: true, color: 'FFFFFF', w: TC3, size: SZ }),
        cell('What did I learn?',                         { fill: C.teal,     bold: true, color: 'FFFFFF', w: TC3, size: SZ }),
        cell('How does this explain the phenomenon?',     { fill: C.medBlue,  bold: true, color: 'FFFFFF', w: TC3r,size: SZ }),
      ]}),
      // Example row
      new TableRow({ children: [
        cell('EXAMPLE: Lesson 1\n(Armyworm Invasion)', { fill: C.lightPurple, bold: true, w: TLW, size: SZ }),
        cell('Images of destroyed Kenyan maize fields. A caterpillar causing widespread crop damage across 47 counties.', { fill: C.white, w: TC3, size: SZ }),
        cell('Biology = scientific study of living things. The armyworm is a living thing — so biology is the tool to understand it.', { fill: C.grey, w: TC3, size: SZ }),
        cell('Still puzzling: HOW do biologists study it? WHICH biology field? That is what Lessons 2–5 will answer.', { fill: C.white, w: TC3r, size: SZ }),
      ]}),
      ...LESSONS.map(l => new TableRow({ children: [
        cell(`Lesson ${l.number}: ${l.title}`, { fill: C.lightBlue, bold: true, w: TLW, size: SZ }),
        cell(l.summaryTablePrompt.observed,    { fill: C.white, w: TC3,  size: SZ }),
        cell(l.summaryTablePrompt.learned,     { fill: C.grey,  w: TC3,  size: SZ }),
        cell(l.summaryTablePrompt.explained,   { fill: C.white, w: TC3r, size: SZ }),
      ]})),
    ], [TLW, TC3, TC3, TC3r]),
    SPACE(),
    makeTable([
      fullHeader('END-OF-UNIT REFLECTION QUESTIONS (complete after Lesson 6)', C.orange, 'FFFFFF', SZ_H, 1),
      new TableRow({ children: [cell(
        '1. Before this unit, what did you think biology was? How has that changed?\n\n\n\n' +
        '2. Which biology field interested you most? Why?\n\n\n\n' +
        '3. How did the armyworm crisis show that biology is important for Kenya?\n\n\n\n' +
        '4. What career in biology would you consider — and what should and should not influence that choice?\n\n\n\n' +
        '5. Name ONE way biology affects your everyday life that you did not notice before this unit.\n\n\n\n' +
        '6. What question about biology do you still want to explore?',
        { fill: C.lightOrange, w: W, size: SZ }
      )]}),
    ], [W]),
    SPACE(),
    makeTable([
      fullHeader('TEACHER NOTES (not for student distribution)', C.darkBlue, 'FFFFFF', SZ_H, 1),
      new TableRow({ children: [cell(
        '• Review Summary Tables after Lesson 3 to identify students who need support connecting examples to biology fields.\n\n' +
        '• Before Lesson 6: check that all students have a career wheel entry and at least 4 lesson rows completed.\n\n' +
        '• Common gap: students write "I learned about biology" without naming specific fields or Kenyan examples. Prompt: "Name the field. Name the example."',
        { fill: C.lightBlue, w: W, size: SZ }
      )]}),
    ], [W]),
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
  console.log('Generating Biology 1.1 Introduction to Biology documents...\n');

  console.log('1/3 Building SoW...');
  const sowBuf = await Packer.toBuffer(await buildSoW());
  const sowPath = path.join(OUT, 'Biology_Introduction_CBE_LessonSequence.docx');
  fs.writeFileSync(sowPath, sowBuf);
  console.log(`    Saved: ${sowPath}  (${(sowBuf.length / 1024).toFixed(0)} KB)\n`);

  console.log('2/3 Building Final Explanation...');
  const feBuf = await Packer.toBuffer(await buildFinalExplanation());
  const fePath = path.join(OUT, 'Biology_Introduction_FinalExplanation.docx');
  fs.writeFileSync(fePath, feBuf);
  console.log(`    Saved: ${fePath}  (${(feBuf.length / 1024).toFixed(0)} KB)\n`);

  console.log('3/3 Building Summary Table...');
  const stBuf = await Packer.toBuffer(await buildSummaryTable());
  const stPath = path.join(OUT, 'Biology_Introduction_SummaryTable.docx');
  fs.writeFileSync(stPath, stBuf);
  console.log(`    Saved: ${stPath}  (${(stBuf.length / 1024).toFixed(0)} KB)\n`);

  console.log('Done! All 3 documents generated.');
}

main().catch(err => { console.error('Generator failed:', err.message); process.exit(1); });
