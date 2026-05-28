'use strict';
/**
 * Generator: Biology Grade 10 — Sub-Strand 1.3: Cell Structure and Specialisation
 *
 * Outputs (in data/outputs/docx/):
 *   1. Biology_CellStructure_CBE_LessonSequence.docx   (SoW — teacher-facing)
 *   2. Biology_CellStructure_FinalExplanation.docx     (student-facing assessment)
 *   3. Biology_CellStructure_SummaryTable.docx         (student portfolio)
 *
 * Format: US Letter Landscape, 0.75" margins, Arial, docx v9
 */

const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, AlignmentType, ShadingType, VerticalAlign, BorderStyle,
  PageOrientation, HeadingLevel, TableLayoutType,
} = require('docx');
const fs   = require('fs');
const path = require('path');
const { getAllPhaseResources, buildResourceParagraphs } = require('./aresResources');

// ─── Output directory ────────────────────────────────────────────────────────
const OUT = path.join(__dirname, '..', 'data', 'outputs', 'docx', 'Grade 10 Bio', 'Bio 1.3');
if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });

// ─── Colour palette ──────────────────────────────────────────────────────────
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

// Phase → row colour for Section C column 1
const PHASE_COLOUR = {
  'Predict Phase':               C.lightPurple,
  'Observe Phase':               C.lightTeal,
  'Explain Phase':               C.lightGreen,
  'Driving Question Board (DQB) Creation': C.lightOrange,
  'Model Building Phase':        C.lightBlue,
};

// ─── Page / typography constants ─────────────────────────────────────────────
const W = 13680;          // content width DXA (landscape Letter minus 2×1080)
const FONT = 'Arial';
const SZ   = 18;          // 9 pt body (docx half-points)
const SZ_H = 22;          // 11 pt section headers
const SZ_T = 28;          // 14 pt title

// ─── Low-level helpers ───────────────────────────────────────────────────────

/** Single-run Paragraph */
function para(text, opts = {}) {
  return new Paragraph({
    alignment: opts.align || AlignmentType.LEFT,
    spacing: { after: opts.after ?? 60, before: opts.before ?? 0 },
    children: [new TextRun({
      text,
      font: FONT,
      size: opts.size || SZ,
      bold:   opts.bold   || false,
      color:  opts.color  || '000000',
      italics: opts.italic || false,
    })],
  });
}

/** Paragraph with multiple runs (for mixed bold/normal inline) */
function mixedPara(runs, opts = {}) {
  return new Paragraph({
    alignment: opts.align || AlignmentType.LEFT,
    spacing: { after: opts.after ?? 60, before: opts.before ?? 0 },
    children: runs.map(r => new TextRun({
      text: r.text,
      font: FONT,
      size: r.size || opts.size || SZ,
      bold:    r.bold    || false,
      italics: r.italic  || false,
      color:   r.color   || '000000',
    })),
  });
}

/** Bullet paragraph (manual bullet using em-dash, avoid unicode bullets) */
function bullet(text, opts = {}) {
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { after: 30, before: 0 },
    indent: { left: 360, hanging: 180 },
    children: [new TextRun({
      text: '\u2013  ' + text,
      font: FONT,
      size: opts.size || SZ,
      bold:   opts.bold  || false,
      color:  opts.color || '000000',
      italics: opts.italic || false,
    })],
  });
}

/** Create a shaded TableCell */
function cell(content, opts = {}) {
  const {
    fill   = C.white,
    w      = null,           // width in DXA (null = auto)
    span   = 1,
    vAlign = VerticalAlign.TOP,
    bold   = false,
    color  = '000000',
    size   = SZ,
    align  = AlignmentType.LEFT,
    italic = false,
  } = opts;

  // content can be string, Paragraph, or Paragraph[]
  let children;
  if (typeof content === 'string') {
    if (content === '') {
      children = [para('', { size })];
    } else {
      // Split on newlines → separate paragraphs
      children = content.split('\n').map(line => {
        if (line.startsWith('• ') || line.startsWith('- ')) {
          return bullet(line.slice(2), { size, bold, color });
        }
        return para(line, { size, bold, color, align, italic, after: 40 });
      });
    }
  } else if (Array.isArray(content)) {
    children = content;
  } else {
    children = [content];
  }

  const cellDef = {
    verticalAlign: vAlign,
    shading: { type: ShadingType.CLEAR, color: 'auto', fill },
    margins: { top: 60, bottom: 60, left: 120, right: 120 },
    children,
  };
  if (w !== null) cellDef.width = { size: w, type: WidthType.DXA };
  if (span > 1)   cellDef.columnSpan = span;
  return new TableCell(cellDef);
}

/** Full-width spanning header row (dark background, white bold text) */
function fullHeader(text, fill, textColor = 'FFFFFF', size = SZ_H, numCols = 2) {
  return new TableRow({
    children: [cell(text, { fill, color: textColor, bold: true, size, align: AlignmentType.CENTER, span: numCols, w: W })],
  });
}

/** Standard 2-column label | content row */
function labelRow(label, content, labelW = 3000, opts = {}) {
  const contentW = W - labelW;
  return new TableRow({
    children: [
      cell(label, { fill: opts.labelFill || C.lightBlue, bold: true, w: labelW, size: SZ }),
      cell(content, { fill: opts.contentFill || C.white, w: contentW, size: SZ }),
    ],
  });
}

/** Create a simple bordered table from rows.
 *  columnWidths: array of DXA values, one per column — MUST be provided for Word to render correctly.
 */
function makeTable(rows, columnWidths = [W]) {
  const tableW = columnWidths.reduce((a, b) => a + b, 0);
  return new Table({
    width: { size: tableW, type: WidthType.DXA },
    layout: TableLayoutType.FIXED,
    columnWidths,
    borders: {
      top:          { style: BorderStyle.SINGLE, size: 4, color: 'AAAAAA' },
      bottom:       { style: BorderStyle.SINGLE, size: 4, color: 'AAAAAA' },
      left:         { style: BorderStyle.SINGLE, size: 4, color: 'AAAAAA' },
      right:        { style: BorderStyle.SINGLE, size: 4, color: 'AAAAAA' },
      insideH:      { style: BorderStyle.SINGLE, size: 2, color: 'CCCCCC' },
      insideV:      { style: BorderStyle.SINGLE, size: 2, color: 'CCCCCC' },
    },
    rows,
  });
}

/** Spacer paragraph */
const SPACE = () => para('', { after: 120 });

// ─── Section builders ────────────────────────────────────────────────────────

/** Document title block */
function titleBlock(title, subtitle) {
  return [
    para(title, { bold: true, size: SZ_T, color: C.darkBlue, align: AlignmentType.CENTER, after: 80 }),
    para(subtitle, { size: SZ_H, color: C.teal, align: AlignmentType.CENTER, after: 160 }),
  ];
}

/** Sub-Strand Overview table (Section A of the document) */
function subStrandOverview(unit) {
  const LW = 3000;
  const CW = W - LW;
  const rows = [
    fullHeader('SUB-STRAND OVERVIEW', C.darkBlue, 'FFFFFF', SZ_H, 2),
    labelRow('Grade Level',   unit.gradeLevel, LW),
    labelRow('Subject',       unit.subject, LW),
    labelRow('Strand',        unit.strand, LW),
    labelRow('Sub-Strand',    unit.substrand, LW),
    labelRow('Learning Outcomes', unit.learningOutcomes, LW, { labelFill: C.lightBlue }),
    labelRow('Core Competencies', unit.coreCompetencies, LW, { labelFill: C.lightBlue }),
    labelRow('Values',             unit.values, LW, { labelFill: C.lightGreen }),
    labelRow('Science & Engineering Practices', unit.sep, LW, { labelFill: C.lightTeal }),
    labelRow('Pertinent & Contemporary Issues (PCIs)', unit.pcis, LW, { labelFill: C.lightOrange }),
    labelRow('Career Connections', unit.careers, LW, { labelFill: C.lightBlue }),
    labelRow('Focus for Lessons',  unit.focus, LW),
    labelRow('Total Duration',     unit.totalDuration, LW),
    labelRow('Anchoring Phenomenon', unit.phenomenon, LW, { labelFill: C.lightPurple }),
    labelRow('Supporting Phenomena', unit.supportingPhenomena, LW, { labelFill: C.lightPurple }),
    labelRow('Storyline Thread',     unit.storyline, LW, { labelFill: C.lightTeal }),
    labelRow('Key Inquiry Questions / Driving Question', unit.drivingQuestion, LW, { labelFill: C.lightPurple }),
  ];
  return makeTable(rows, [LW, CW]);
}

/** Lesson section A: Specific Learning Outcomes */
function sectionA(lesson) {
  const LW = 2400;
  const CW = W - LW;
  const rows = [
    fullHeader(`LESSON ${lesson.number} (${lesson.duration}): ${lesson.title}`, C.darkBlue, 'FFFFFF', SZ_H, 2),
    fullHeader('A. SPECIFIC LEARNING OUTCOMES', C.teal, 'FFFFFF', SZ_H, 2),
    new TableRow({ children: [
      cell('Category', { fill: C.medBlue, bold: true, color: 'FFFFFF', w: LW, size: SZ }),
      cell('Specific Learning Outcomes', { fill: C.medBlue, bold: true, color: 'FFFFFF', w: CW, size: SZ }),
    ]}),
    labelRow('Purpose',    lesson.slo.purpose,   LW, { labelFill: C.lightBlue }),
    labelRow('Knowledge',  lesson.slo.knowledge,  LW, { labelFill: C.lightBlue }),
    labelRow('Skills',     lesson.slo.skills,     LW, { labelFill: C.lightBlue }),
    labelRow('Attitudes',  lesson.slo.attitudes,  LW, { labelFill: C.lightGreen }),
    labelRow('Key Inquiry Question',   lesson.slo.keyInquiry,   LW, { labelFill: C.lightPurple }),
    labelRow('Purpose in Storyline',   lesson.slo.purposeInStoryline, LW, { labelFill: C.lightTeal }),
    labelRow('Safety Notes', lesson.slo.safetyNotes, LW, { labelFill: C.lightOrange }),
  ];
  return makeTable(rows, [LW, CW]);
}

/** Lesson section B: Overview (2-paragraph prose) */
function sectionB(lesson) {
  const rows = [
    fullHeader('B. LESSON OVERVIEW', C.teal, 'FFFFFF', SZ_H, 1),
    new TableRow({ children: [
      cell(lesson.overview, { fill: C.white, w: W, size: SZ }),
    ]}),
  ];
  return makeTable(rows, [W]);
}

/** Lesson section C: Implementation Framework */
function sectionC(lesson) {
  // Column widths: Phase 900 | 5 content cols × 2556
  const cw = [900, 2556,  870, 3242, 2556, 2556];

  const headerRow = new TableRow({ children: [
    cell('Phase',                      { fill: C.darkBlue, bold: true, color: 'FFFFFF', w: cw[0], size: SZ }),
    cell('Learner Experience',         { fill: C.medBlue,  bold: true, color: 'FFFFFF', w: cw[1], size: SZ }),
    cell('Resource',                   { fill: C.teal,     bold: true, color: 'FFFFFF', w: cw[2], size: SZ }),
    cell('Teacher Moves',              { fill: C.medBlue,  bold: true, color: 'FFFFFF', w: cw[3], size: SZ }),
    cell('Sensemaking Strategy',       { fill: C.teal,     bold: true, color: 'FFFFFF', w: cw[4], size: SZ }),
    cell('Formative Assessment Strategy', { fill: C.medBlue, bold: true, color: 'FFFFFF', w: cw[5], size: SZ }),
  ]});

  const aresTopic = lesson.aresKeywords || lesson.title || '';
  const aresRes = getAllPhaseResources({
    substrand: lesson.substrand || 'Cell Structure and Specialisation',
    topic:     aresTopic,
    subject:   'Biology',
  });

  const PHASE_KEY = {
    'Predict Phase':                         'predict',
    'Observe Phase':                         'observe',
    'Explain Phase':                         'explain',
    'Driving Question Board (DQB) Creation': 'dqb',
    'Model Building Phase':                  'model',
  };

  const phaseRows = lesson.framework.map(ph => {
    const phaseKey  = PHASE_KEY[ph.phase] || 'observe';
    const aresParas = buildResourceParagraphs(aresRes[phaseKey], phaseKey);
    return new TableRow({ children: [
      cell(ph.phase,                { fill: PHASE_COLOUR[ph.phase] || C.grey, bold: true, w: cw[0], size: SZ }),
      cell(ph.learnerExperience,    { fill: C.white, w: cw[1], size: SZ }),
      cell(aresParas,               { fill: C.grey,  w: cw[2] }),
      cell(ph.teacherMoves,         { fill: C.white, w: cw[3], size: SZ }),
      cell(ph.sensemakingStrategy,  { fill: C.grey,  w: cw[4], size: SZ }),
      cell(ph.formativeAssessment,  { fill: C.white, w: cw[5], size: SZ }),
    ]});
  });

  const rows = [
    fullHeader('C. LESSON IMPLEMENTATION FRAMEWORK', C.teal, 'FFFFFF', SZ_H, 6),
    headerRow,
    ...phaseRows,
  ];
  return makeTable(rows, cw);
}

/** Lesson section D: Teacher Reflection */
function sectionD(lesson) {
  const rows = [
    fullHeader('D. TEACHER REFLECTION', C.orange, 'FFFFFF', SZ_H, 1),
    new TableRow({ children: [
      cell(lesson.teacherReflection, { fill: C.lightOrange, w: W, size: SZ }),
    ]}),
  ];
  return makeTable(rows, [W]);
}

/** Lesson section E: Summary Table Prompt */
function sectionE(lesson) {
  const LW = 3000;
  const CW = W - LW;
  const rows = [
    fullHeader('E. SUMMARY TABLE PROMPT  (pre-filled example for this lesson)', C.purple, 'FFFFFF', SZ_H, 2),
    new TableRow({ children: [
      cell('What did I observe?',                    { fill: C.lightPurple, bold: true, w: LW, size: SZ }),
      cell(lesson.summaryTablePrompt.observed,       { fill: C.white, w: CW, size: SZ }),
    ]}),
    new TableRow({ children: [
      cell('What did I learn?',                      { fill: C.lightPurple, bold: true, w: LW, size: SZ }),
      cell(lesson.summaryTablePrompt.learned,        { fill: C.white, w: CW, size: SZ }),
    ]}),
    new TableRow({ children: [
      cell('How does this explain the phenomenon?',  { fill: C.lightPurple, bold: true, w: LW, size: SZ }),
      cell(lesson.summaryTablePrompt.explained,      { fill: C.white, w: CW, size: SZ }),
    ]}),
  ];
  return makeTable(rows, [LW, CW]);
}

/** Differentiation & Inclusion table (end of document) */
function differentiationTable() {
  const LW = 3000;
  const HW = (W - LW) / 2;  // half of remaining = 5340
  const rows = [
    fullHeader('DIFFERENTIATION AND INCLUSION', C.darkBlue, 'FFFFFF', SZ_H, 3),
    new TableRow({ children: [
      cell('Learner Need',       { fill: C.medBlue, bold: true, color: 'FFFFFF', w: LW, size: SZ }),
      cell('Support Strategies', { fill: C.teal,    bold: true, color: 'FFFFFF', w: HW, size: SZ }),
      cell('Extension Strategies', { fill: C.medBlue, bold: true, color: 'FFFFFF', w: HW, size: SZ }),
    ]}),
    new TableRow({ children: [
      cell('English Language Learners / emerging literacy', { fill: C.lightBlue, w: LW, size: SZ }),
      cell(
        '• Provide labelled diagrams of cell organelles with bilingual captions (English/Swahili)\n' +
        '• Use visual models and realia (actual microscope slides)\n' +
        '• Pair with a peer who can explain in Swahili\n' +
        '• Sentence starters: "I observe that…", "I think this means…"',
        { fill: C.white, w: HW, size: SZ }),
      cell(
        '• Research additional specialised cell types not covered in class\n' +
        '• Write a bilingual glossary of cell biology terms\n' +
        '• Create labelled comparison posters of plant vs animal cells',
        { fill: C.grey, w: HW, size: SZ }),
    ]}),
    new TableRow({ children: [
      cell('Learners with visual impairment', { fill: C.lightBlue, w: LW, size: SZ }),
      cell(
        '• Provide 3D tactile cell models (clay, Styrofoam) for organelle identification\n' +
        '• Use audio descriptions of microscope images\n' +
        '• Allow verbal responses instead of written diagrams',
        { fill: C.white, w: HW, size: SZ }),
      cell(
        '• Verbally describe and debate cell specialisation differences\n' +
        '• Lead group discussions on levels of organisation',
        { fill: C.grey, w: HW, size: SZ }),
    ]}),
    new TableRow({ children: [
      cell('Learners who need additional time / support with abstract concepts', { fill: C.lightBlue, w: LW, size: SZ }),
      cell(
        '• Use analogy cards: cell = factory (nucleus = manager, mitochondria = power plant…)\n' +
        '• Chunk tasks: complete one organelle at a time\n' +
        '• Provide partially-completed diagrams to fill in\n' +
        '• Allow extended time for model drawing',
        { fill: C.white, w: HW, size: SZ }),
      cell(
        '• Design their own cell analogy (school, city, sports team…)\n' +
        '• Investigate cutting-edge research: CRISPR, stem cells, cancer cells',
        { fill: C.grey, w: HW, size: SZ }),
    ]}),
    new TableRow({ children: [
      cell('Advanced learners', { fill: C.lightBlue, w: LW, size: SZ }),
      cell(
        '• Peer-teach organelle functions to partners\n' +
        '• Act as lab assistants during practical lessons',
        { fill: C.white, w: HW, size: SZ }),
      cell(
        '• Investigate disease caused by organelle malfunction (e.g., mitochondrial disease)\n' +
        '• Research current Kenyan biomedical research involving cell biology\n' +
        '• Model a full organism from cell to organ system level in a diagram',
        { fill: C.grey, w: HW, size: SZ }),
    ]}),
  ];
  return makeTable(rows, [LW, HW, HW]);
}

// ─── Unit Data ───────────────────────────────────────────────────────────────

const UNIT = {
  gradeLevel: '10',
  subject: 'Biology',
  strand: 'Strand 1.0: Cell Biology and Biodiversity',
  substrand: 'Sub-Strand 1.3: Cell Structure and Specialisation',
  learningOutcomes:
    'By the end of this sub-strand, the learner should be able to:\n' +
    '• a) Differentiate between light and electron microscopes as used in the study of cell structure\n' +
    '• b) Describe the structure and function of plant and animal cells as observed in an electron microscope\n' +
    '• c) Prepare temporary slides for observation and estimation of cell size using a light microscope\n' +
    '• d) Relate the structure of specialised cells in plants and animals to their functions\n' +
    '• e) Appreciate the cell as the basic unit of life',
  coreCompetencies:
    '• Communication and Collaboration — group discussions, peer teaching, shared model building\n' +
    '• Critical Thinking and Problem Solving — comparing microscope types, inferring organelle function from structure\n' +
    '• Digital Literacy — using online simulations (LabXchange, Khan Academy), video analysis\n' +
    '• Learning to Learn — tracking understanding on the Summary Table, revising models\n' +
    '• Self-Efficacy — successfully preparing temporary slides, identifying organelles\n' +
    '• Citizenship — understanding the cell as the basis of all life; appreciating biodiversity\n' +
    '• Creativity and Innovation — designing own cell analogy, model building',
  values:
    '• Nationalism — appreciating Kenyan scientists contributing to cell biology research\n' +
    '• Responsibility — safe handling of microscopes, glass slides, iodine/methylene blue stains\n' +
    '• Integrity — honest reporting of microscope observations and experimental results\n' +
    '• Respect — valuing diverse ideas during DQB and model-sharing activities\n' +
    '• Unity — collaborative group investigations and shared model construction\n' +
    '• Excellence — striving for clear, accurate diagrams and explanations',
  sep:
    '• Asking Questions — generating DQB questions from the phenomenon\n' +
    '• Developing and Using Models — initial cell model, revised through all lessons\n' +
    '• Planning and Carrying Out Investigations — preparing temporary slides, estimating cell size\n' +
    '• Analyzing and Interpreting Data — comparing EM images, reading microscope scales\n' +
    '• Constructing Explanations — explaining how specialised cells enable complex organism development\n' +
    '• Obtaining, Evaluating and Communicating Information — research on cell types, peer presentations',
  pcis:
    '• Health and Hygiene — understanding disease at the cellular level (cancer = abnormal cell division)\n' +
    '• Safety — safe use of glass slides, sharp instruments, chemical stains in practical work\n' +
    '• Life Skills — microscope use as a transferable laboratory skill\n' +
    '• Science and Technology — modern microscopy and its role in Kenyan medical research',
  careers:
    '• Medical Doctor / Pathologist — diagnosing disease through cell analysis (histology)\n' +
    '• Biomedical Scientist / Laboratory Technician — blood cell and tissue analysis\n' +
    '• Botanist / Plant Scientist — studying plant cell structures and agricultural improvement\n' +
    '• Oncologist — understanding cancer as a disease of uncontrolled cell division\n' +
    '• Pharmacologist — developing drugs that act on specific cell structures\n' +
    '• Genetic Counsellor — advising on inherited cell-level conditions',
  focus:
    'This unit helps students understand that all living organisms are built from cells, ' +
    'and that the internal structure of a cell determines what it can do. Through observation ' +
    'of a salamander developing from a single fertilised egg, students are driven to ask: ' +
    'How does one cell become billions of different cell types? Evidence is gathered through ' +
    'microscopy, slide preparation, EM image analysis, and research — culminating in a ' +
    'complete explanation of cell specialisation and levels of organisation.',
  totalDuration: '8 lessons (approximately 20 periods × 40 minutes = 800 minutes)',
  phenomenon:
    'A SALAMANDER GROWS FROM A SINGLE FERTILISED CELL\n\n' +
    'In a remarkable National Geographic time-lapse video, we watch a salamander develop from ' +
    'one fertilised egg into a complex organism with eyes, a heart, limbs, and skin — ' +
    'hundreds of millions of specialised cells, all from ONE starting cell. ' +
    'This is puzzling: how does one cell know to become a nerve cell? A red blood cell? ' +
    'A muscle cell? The answer lies in cell STRUCTURE.',
  supportingPhenomena:
    '• Why does onion skin look completely different under a light microscope vs the naked eye?\n' +
    '• Why can we see bacteria in a blood smear with an electron microscope but not with a light microscope?\n' +
    '• Why does a red blood cell look like a squashed disc — what does its shape tell us about its job?\n' +
    '• Why does a root hair cell have such a long thin extension — and how does that help the plant survive?',
  storyline:
    'Lesson 1: Students observe the salamander time-lapse and generate questions. They draw initial models of what they think a "cell" looks like and post questions on the DQB.\n\n' +
    'Lesson 2: Students discover that the type of microscope matters — light vs electron — and why each reveals different levels of detail about cell structure.\n\n' +
    'Lesson 3: Students make their own temporary slides and observe real plant cells through a light microscope, estimating cell size. Model updated.\n\n' +
    'Lesson 4: Students study EM images of plant and animal cells, identifying and mapping the major organelles and their functions.\n\n' +
    'Lesson 5: Students systematically compare plant and animal cells — identifying structures unique to each. Model revised.\n\n' +
    'Lesson 6: Students investigate specialised cells in plants (root hair, guard cell, xylem, phloem) — connecting structure to function.\n\n' +
    'Lesson 7: Students investigate specialised cells in animals (RBC, sperm, egg, nerve, muscle) — connecting structure to function. DQB updated.\n\n' +
    'Lesson 8: Students map the levels of organisation (cell → tissue → organ → organ system → organism) and write their final explanation of how the salamander became complex.',
  drivingQuestion:
    'DRIVING QUESTION: How does a single cell become a complex, specialised organism — and what does the internal structure of a cell reveal about what it can do?\n\n' +
    'KICD KEY INQUIRY QUESTIONS:\n' +
    '1. Why do plant and animal cells differ?\n' +
    '2. How are cells specialised?',
};

// ─── Lesson Data ─────────────────────────────────────────────────────────────

const LESSONS = [

  // ── LESSON 1 ──────────────────────────────────────────────────────────────
  {
    number: 1,
    title: 'The Salamander Phenomenon — Why Do We Study Cells?',
      aresKeywords: 'cell structure organelles eukaryotic biology',
    duration: '2 periods / 80 minutes',
    slo: {
      purpose: 'Launch the unit with a compelling, puzzling phenomenon. Activate prior knowledge. Create initial models. Start the Driving Question Board.',
      knowledge:
        '• State that all living organisms are made of cells (cell theory)\n' +
        '• Recognise that one cell can give rise to a complex multi-cellular organism\n' +
        '• Name the cell as the basic structural and functional unit of life',
      skills:
        '• Observe a time-lapse video and identify key events\n' +
        '• Generate scientific questions from a stimulus\n' +
        '• Draw an initial model showing their current understanding of cell structure',
      attitudes:
        '• Wonder and curiosity about cell complexity\n' +
        '• Openness to revising ideas as evidence is gathered\n' +
        '• Appreciation for the complexity of living organisms',
      keyInquiry: 'What is a cell, and why does studying cells help us understand how living things work?',
      purposeInStoryline:
        'This lesson LAUNCHES the unit. Students confront the anchoring phenomenon (salamander time-lapse), ' +
        'surface their prior knowledge (right or wrong), generate questions for the DQB, and create a ' +
        'first rough model of a cell. All subsequent lessons will return to this model and these questions.',
      safetyNotes: 'No laboratory practical in this lesson. Standard classroom safety applies.',
    },
    overview:
      'Students open the unit by watching the National Geographic time-lapse showing a salamander developing ' +
      'from a single fertilised egg into a complex organism. The video is shown without commentary — students ' +
      'are asked simply, "What do you notice? What do you wonder?" After individual thinking time, students ' +
      'share observations in pairs, then the class, and questions are posted on the Driving Question Board. ' +
      'Students then draw their initial model of what they THINK a cell looks like inside, labelling any ' +
      'structures they already know. These models are deliberately saved — they will be revised in every ' +
      'subsequent lesson.\n\n' +
      'The lesson ends with a short direct-instruction moment introducing the cell theory (all living things ' +
      'are made of cells; cells come from pre-existing cells; the cell is the basic unit of structure and ' +
      'function). This gives students a shared vocabulary anchor, while the phenomenon and their own questions ' +
      'provide the motivation to learn more.',
    framework: [
      {
        phase: 'Predict Phase',
        learnerExperience:
          'Students watch the salamander time-lapse video (2 min) in silence. ' +
          'Then individually write: (1) What do I notice? (2) What puzzles me? (3) What do I think a cell looks like inside?',
        resource:
          'VIDEO: "See a Salamander Grow From a Single Cell" — National Geographic Short Film Showcase\n' +
          'TYPE: Video (available on Rachel/offline cache or YouTube)\n' +
          'MATERIALS: Student notebooks, pencils',
        teacherMoves:
          '"Before we start, I want you to notice everything — do not look away."\n' +
          'Play video. Remain SILENT during video.\n' +
          'After video: "Take 60 seconds. Write what you noticed. Write what puzzles you."\n' +
          'WAIT TIME: 60 seconds minimum before calling on anyone.',
        sensemakingStrategy:
          'POE — PREDICT:\n' +
          'Students predict what a cell looks like before any instruction. These predictions are ' +
          'recorded and KEPT — wrong ideas are valuable data that we revisit throughout the unit.',
        formativeAssessment:
          'Teacher circulates and reads student written responses.\n' +
          'Check: Do students see the connection between ONE cell and MANY cells?\n' +
          'Note: What prior knowledge do students have? What misconceptions?\n' +
          'Quick poll: "Hands up — have you ever looked through a microscope before?"',
      },
      {
        phase: 'Observe Phase',
        learnerExperience:
          'Think-Pair-Share: Students discuss their written observations with a partner. ' +
          'Then pairs share with the class. Teacher records ALL observations on the board ' +
          '(no evaluation — just listing). Teacher asks "What is puzzling about this video?"',
        resource:
          'MATERIALS: Large chart paper or whiteboard for recording student ideas\n' +
          'TYPE: Discussion materials\n' +
          'OPTION: Display still images from the time-lapse at different stages',
        teacherMoves:
          '"Share with your partner what you wrote. Partner listens without interrupting."\n' +
          'After 2 min: "What did your partner notice that surprised you?"\n' +
          'Cold-call 4–5 pairs. Record observations WITHOUT judging them.\n' +
          '"What is the most puzzling thing about what we just watched?"',
        sensemakingStrategy:
          'Think-Pair-Share:\n' +
          'THINK (60 sec) → PAIR (2 min) → SHARE (5 min)\n' +
          'Surfacing prior knowledge — teacher records ALL ideas including incorrect ones without correction.',
        formativeAssessment:
          'Listen for misconceptions (e.g., "cells are tiny circles", "only animals have cells").\n' +
          'Note which students already know cell parts vs those with little prior knowledge.\n' +
          'These ideas guide Lesson 2 emphasis.',
      },
      {
        phase: 'Explain Phase',
        learnerExperience:
          'Class discussion: "How many cells does a salamander have at the start of the video? At the end?" ' +
          'Teacher introduces the 3 parts of Cell Theory. Students add "Cell Theory" as a DQB answer: ' +
          '"We now know: all living things are made of cells."',
        resource:
          'VISUAL: Cell Theory summary (3 points) displayed on board or printed card\n' +
          'LINK: Khan Academy — Introduction to cells (offline on Rachel)\n' +
          'TYPE: Digital resource / printed summary',
        teacherMoves:
          '"So at the start there was ONE cell. How many cells does an adult salamander have — guess!"\n' +
          'WAIT TIME: 15 seconds.\n' +
          'After responses: "About 10 billion cells. All from ONE."\n' +
          '"Scientists worked for 200 years to understand this. Here is what they agreed on: Cell Theory."\n' +
          'Present 3 points. Ask: "Which of your questions does this answer? Which does it NOT answer?"',
        sensemakingStrategy:
          'Connecting to Prior Knowledge:\n' +
          'Students identify which of their prior observations/predictions the cell theory confirms or challenges.\n' +
          'This creates cognitive dissonance — the cell theory answers "what is a cell?" but NOT "why are cells different?"',
        formativeAssessment:
          'Exit check: "Tell me ONE thing cell theory says, in your own words."\n' +
          'Quick written response — 1 sentence.\n' +
          'Collect to check before Lesson 2.',
      },
      {
        phase: 'Driving Question Board (DQB) Creation',
        learnerExperience:
          'Each student writes 1–3 questions on sticky notes: "What do I want to figure out?" ' +
          'Questions are posted on the class DQB poster under categories: ' +
          'WHAT (knowledge) / HOW (process) / WHY (reasoning). ' +
          'Class reviews posted questions together.',
        resource:
          'MATERIALS: Sticky notes (3 colours if possible), large poster paper, markers\n' +
          'DQB POSTER: Pre-labelled with 3 question categories\n' +
          'TYPE: Class artefact (stays on wall throughout the unit)',
        teacherMoves:
          '"Now write YOUR questions. What do you still want to figure out about cells? One question per sticky note."\n' +
          'WAIT TIME: 3 minutes for writing.\n' +
          'Students come up and post. Teacher reads some aloud.\n' +
          '"We are going to answer ALL of these questions by the end of this unit. Which ones do you think we answer first?"',
        sensemakingStrategy:
          'Driving Question Board (DQB):\n' +
          'Students own their questions. Teacher does NOT evaluate or remove any questions.\n' +
          'The DQB is a living artefact — questions get answered and new ones added across all 8 lessons.\n' +
          'Organise questions by type, not by "correctness."',
        formativeAssessment:
          'Quality of DQB questions reveals depth of thinking.\n' +
          'Look for: questions about structure ("what is inside?"), function ("why?"), and process ("how?").\n' +
          'Note: students with no questions may need more scaffolding in Lesson 2.',
      },
      {
        phase: 'Model Building Phase',
        learnerExperience:
          'Students draw their INITIAL MODEL of a cell — what they THINK is inside, right now, ' +
          'before any further instruction. Models are labelled with whatever the student already knows. ' +
          'Models are dated and stored in the student\'s notebook/portfolio. ' +
          '"Do NOT look anything up — draw what YOU think right now."',
        resource:
          'MATERIALS: Blank A4 paper, coloured pencils, student notebooks\n' +
          'MODEL PROMPT (on board): "Draw what you think is INSIDE a cell. Label anything you know."\n' +
          'TYPE: Student artefact (kept for revision throughout the unit)',
        teacherMoves:
          '"This model is NOT graded. It shows your CURRENT thinking. Wrong ideas are fine — we will improve the model together."\n' +
          'Circulate and observe (do NOT correct). Note what students include.\n' +
          '"Write the date on your model. Put your name. Keep it safe — we will come back to it in every lesson."\n' +
          '"Share your model with the person next to you. Explain what you drew."',
        sensemakingStrategy:
          'Initial Modelling:\n' +
          'Students externalise their current mental model — making thinking visible.\n' +
          'This "first draft" becomes a baseline for measuring conceptual growth across all 8 lessons.\n' +
          'Sharing models allows students to see the range of ideas in the class.',
        formativeAssessment:
          'Teacher photographs or collects initial models (or notes key features).\n' +
          'Check: Do students show any internal structures? Do they distinguish animal from plant cells?\n' +
          'These models guide differentiation in Lesson 4 (organelles).',
      },
    ],
    teacherReflection:
      'After teaching this lesson, reflect on these questions:\n\n' +
      '1. What prior knowledge did students reveal during Think-Pair-Share? Were there surprising ideas — correct or incorrect?\n\n' +
      '2. Did the salamander time-lapse generate genuine curiosity? How engaged were students — scale of 1–5?\n\n' +
      '3. Quality of DQB questions: Were they mostly factual ("What is the nucleus?") or deeper ("Why do cells look different?")? What does this tell you about readiness?\n\n' +
      '4. How complete/detailed were the initial cell models? Did any students already know organelles? Did any draw only a circle?\n\n' +
      '5. What misconceptions were revealed that need addressing in Lesson 2? (Common: "cells are just blobs", "only living things you can see have cells")\n\n' +
      '6. What would you change about the pacing or questioning sequence if you taught this again?',
    summaryTablePrompt: {
      observed:
        'A salamander growing from ONE fertilised egg into a complete organism with eyes, limbs, and organs. ' +
        'The video showed rapid cell division — one cell becoming many. ' +
        'DQB started with class questions. Initial model drawn.',
      learned:
        'All living things are made of cells (Cell Theory). ' +
        'The cell is the basic unit of life. ' +
        'Cells come from pre-existing cells. ' +
        'One cell can divide many times to form all the different cells in an organism.',
      explained:
        'Not yet explained — the phenomenon is still puzzling! ' +
        'We know the salamander starts as ONE cell, but HOW does that one cell produce so many DIFFERENT cells? ' +
        'That is what we will figure out in the next lessons.',
    },
  },

  // ── LESSON 2 ──────────────────────────────────────────────────────────────
  {
    number: 2,
    title: 'Tools of the Trade — Light Microscope vs Electron Microscope',
      aresKeywords: 'light microscope electron microscope magnification biology',
    duration: '2 periods / 80 minutes',
    slo: {
      purpose: 'Equip students with understanding of microscopy tools so they can access cell structure evidence in subsequent lessons.',
      knowledge:
        '• State the differences between light and electron microscopes (light source, magnification, resolution, specimen type)\n' +
        '• Identify the main parts of a light microscope and state the function of each\n' +
        '• Explain why electron microscopes reveal more detail than light microscopes',
      skills:
        '• Use a light microscope correctly (coarse and fine adjustment, objective lenses, stage)\n' +
        '• Calculate total magnification (eyepiece × objective)\n' +
        '• Compare light vs electron microscope images of the same specimen',
      attitudes:
        '• Appreciate microscopy as a technological breakthrough that transformed biology\n' +
        '• Patience and care in handling precision laboratory instruments\n' +
        '• Curiosity about what increased magnification reveals',
      keyInquiry: 'What tools do scientists use to study cells, and why does the type of microscope matter?',
      purposeInStoryline:
        'Before students can gather cell structure evidence in Lessons 3–5, they need to know HOW cells are observed. ' +
        'This lesson gives them the tools. They also revisit the DQB question "Can you see inside a cell?" ' +
        'and begin to answer it: "It depends on the microscope."',
      safetyNotes:
        '• Handle microscopes with both hands at all times\n' +
        '• Never force objective lenses — rotate gently\n' +
        '• Always start with the lowest power (4×) objective\n' +
        '• Keep electrical cords away from water\n' +
        '• Report any damaged slides or cracked lenses immediately',
    },
    overview:
      'This lesson establishes the two main tools students will use to gather cell structure evidence throughout the unit. ' +
      'Students begin by examining a light microscope, identifying its parts, and practising basic operation. ' +
      'They calculate magnification and observe a prepared slide (letter "e" or a thin cross-section). ' +
      'The class then examines electron microscope (EM) images of the same specimens, directly comparing ' +
      'what each microscope reveals. Students are guided to ask: "What CANNOT the light microscope show us?" ' +
      'This creates the motivation for Lesson 4, where EM images of organelles will be examined in detail.\n\n' +
      'By the end of this lesson, students can identify light microscope parts, use it safely, and articulate ' +
      'why electron microscopes were a revolutionary scientific development. The DQB is updated with at least ' +
      'one answer: "We can now answer the question: How do we study cells?"',
    framework: [
      {
        phase: 'Predict Phase',
        learnerExperience:
          'Students look at a side-by-side image: light microscope photo of a cell vs electron microscope photo of the same cell. ' +
          '"What differences do you notice? Why do you think they look different?" ' +
          'Individual written response, then pair discussion.',
        resource:
          'IMAGE: LM vs EM comparison of a plant cell (printed or projected)\n' +
          'SOURCE: Khan Academy Biology — Microscopy section (offline on Rachel)\n' +
          'TYPE: Visual stimulus',
        teacherMoves:
          '"Look at these two images of the SAME type of cell. What do you notice?"\n' +
          'WAIT TIME: 30 seconds of silent looking.\n' +
          '"Write down THREE differences you observe."\n' +
          'WAIT TIME: 60 seconds for writing.\n' +
          '"Turn to your partner — compare your lists."',
        sensemakingStrategy:
          'Close Reading of Images:\n' +
          'Students treat the images like data — observing systematically before receiving explanation.\n' +
          'This builds the habit of evidence-based reasoning.',
        formativeAssessment:
          'Listen for students identifying: level of detail, colour (LM can use stains, EM is black-and-white), ' +
          'visible structures. Note who already uses vocabulary like "organelles" or "resolution."',
      },
      {
        phase: 'Observe Phase',
        learnerExperience:
          'Practical: Each group receives a light microscope. Students identify parts (eyepiece, objective lenses, stage, ' +
          'coarse/fine adjustment, condenser, mirror/light source, arm, base). They observe a prepared slide and ' +
          'calculate total magnification. Teacher demonstrates correct focusing technique first.',
        resource:
          'EQUIPMENT (per group): Light microscope, prepared slide (letter "e" or Spirogyra cross-section)\n' +
          'HANDOUT: Labelled microscope diagram (blank version for students to fill in)\n' +
          'REFERENCE: Microscope parts and functions table\n' +
          'TYPE: Laboratory practical',
        teacherMoves:
          'Full class demo first: "Watch me — I will show you how to find the specimen."\n' +
          'Key steps to model: start at lowest power, look from the side when lowering, use coarse then fine.\n' +
          '"Now your group\'s turn. Take turns — everyone must look through the eyepiece."\n' +
          'Circulate every 2 minutes. Common error: students look with both eyes open — gently correct.',
        sensemakingStrategy:
          'Lab Roles Rotation:\n' +
          'Assign roles: Focuser, Observer, Recorder, Reporter. Roles rotate every 5 minutes.\n' +
          'Each Observer must describe what they see before the next person looks.',
        formativeAssessment:
          'Spot-check: Point to any part — "What is this called? What does it do?"\n' +
          'Check magnification calculation: "Your eyepiece is ×10 and you are on the ×40 objective — what is total magnification?"\n' +
          'Expected answer: 400×.',
      },
      {
        phase: 'Explain Phase',
        learnerExperience:
          'Class builds a comparison table: Light Microscope vs Electron Microscope. ' +
          'Compare: light source, magnification (up to ×2,000 vs ×2,000,000), resolution, ' +
          'specimen (living vs dead), cost, uses. ' +
          'Students annotate the EM image from the opening activity with newly-learned vocabulary.',
        resource:
          'HANDOUT / BOARD: Blank comparison table (LM vs EM) for students to complete\n' +
          'VIDEO (optional): "How does an electron microscope work?" — 2 min clip\n' +
          'TYPE: Note-taking structure',
        teacherMoves:
          '"Based on the practical and what you observed — what CAN a light microscope show? What can it NOT show?"\n' +
          'Build the table together, asking students for each row: "What do you think? Does anyone disagree?"\n' +
          '"Electron microscopes show structures as small as 1 nanometre. A light microscope: 200 nanometres minimum."\n' +
          '"Why does that difference matter for studying cells?"',
        sensemakingStrategy:
          'Structured Comparison (T-Table):\n' +
          'Students complete the comparison table collaboratively — each group contributes one row.\n' +
          'Connecting new information to the opening image.',
        formativeAssessment:
          'Whiteboards / notebook check: "Draw the comparison table. Fill in the magnification row."\n' +
          'Quick scan of student tables to check accuracy before moving on.',
      },
      {
        phase: 'Driving Question Board (DQB) Creation',
        learnerExperience:
          'Students revisit the DQB. They identify questions from Lesson 1 that TODAY\'s lesson answers. ' +
          'They move answered sticky notes to the "ANSWERED" section of the DQB. ' +
          'They add new questions that arose from the microscopy activity.',
        resource:
          'MATERIALS: DQB poster (from Lesson 1), additional sticky notes\n' +
          'MARKER pens for writing new questions\n' +
          'TYPE: Class artefact',
        teacherMoves:
          '"Look at our DQB. Which questions from Lesson 1 can we answer now?"\n' +
          'WAIT TIME: 30 seconds.\n' +
          '"Move those sticky notes to ANSWERED. Write the brief answer on the back."\n' +
          '"Did today\'s lesson raise any NEW questions? Add them."',
        sensemakingStrategy:
          'DQB Update — metacognitive strategy:\n' +
          'Students track their own growing understanding. ' +
          'Moving questions to "answered" is explicitly reinforcing that they are figuring things out.',
        formativeAssessment:
          'Quality and quantity of questions moved to "answered" shows lesson comprehension.\n' +
          'New questions added show productive inquiry direction.',
      },
      {
        phase: 'Model Building Phase',
        learnerExperience:
          'Students retrieve their Lesson 1 initial model. They add ONE update: ' +
          '"I now know that a microscope reveals _____ that I cannot see with my naked eye." ' +
          'Students annotate their model with the question: "What structures will an electron microscope reveal?"',
        resource:
          'MATERIALS: Student Lesson 1 initial model, pencil/pen\n' +
          'PROMPT: "What can you ADD to your model now? What do you still not know?"\n' +
          'TYPE: Student portfolio artefact',
        teacherMoves:
          '"Take out your model from Lesson 1. Do not erase — only ADD."\n' +
          '"Write today\'s date next to any new addition."\n' +
          '"Look at it: what question does your model still NOT answer?" Students write that question on their model.',
        sensemakingStrategy:
          'Progressive Model Revision:\n' +
          'Students see that science knowledge builds incrementally. ' +
          'Each lesson adds detail to the model — this is how scientific models work.',
        formativeAssessment:
          'Circulate and observe model updates. Ask: "What did you add? Why?"\n' +
          'Students who add nothing may need to be asked: "What did you learn today that would change your model?"',
      },
    ],
    teacherReflection:
      'After teaching this lesson, reflect on:\n\n' +
      '1. Were students able to correctly identify all parts of the light microscope? Which parts caused confusion?\n\n' +
      '2. Did students successfully focus the microscope and observe the specimen? How many groups needed direct help?\n\n' +
      '3. Could students calculate total magnification accurately? What errors were made?\n\n' +
      '4. How well did students articulate the difference between LM and EM? Did they understand WHY EM reveals more detail (resolution, not just magnification)?\n\n' +
      '5. Which DQB questions were answered? Were any new questions more interesting than the original ones?\n\n' +
      '6. Were there any safety concerns during the practical? What would you adjust for next time?',
    summaryTablePrompt: {
      observed:
        'Practised using a light microscope — identified parts (eyepiece, objective lenses, stage, coarse and fine adjustment). ' +
        'Observed a prepared slide at ×100 and ×400 magnification. ' +
        'Compared a light microscope image vs an electron microscope image of the same cell.',
      learned:
        'Light microscopes use visible light and can magnify up to ×2,000 (living specimens possible). ' +
        'Electron microscopes use electron beams, magnify up to ×2,000,000, but specimens must be dead. ' +
        'Total magnification = eyepiece magnification × objective magnification. ' +
        'EM reveals organelles that LM cannot resolve.',
      explained:
        'To study the INSIDE of a cell (to figure out the salamander phenomenon) we need an electron microscope. ' +
        'The light microscope shows us cells exist, but the electron microscope shows us what is INSIDE — which organelles make cells different from each other.',
    },
  },

  // ── LESSON 3 ──────────────────────────────────────────────────────────────
  {
    number: 3,
    title: 'Preparing Temporary Slides — Observing Real Plant Cells',
      aresKeywords: 'temporary slides plant cells onion microscope staining',
    duration: '3 periods / 120 minutes',
    slo: {
      purpose: 'Students gather first-hand evidence of cell structure by preparing and observing their own temporary slides.',
      knowledge:
        '• Describe the steps to prepare a temporary slide (specimen, water/stain, cover slip)\n' +
        '• State the purpose of staining (iodine for starch/cell wall; methylene blue for nuclei)\n' +
        '• Describe what is visible in onion epidermal cells under a light microscope (cell wall, cytoplasm, nucleus, vacuole)',
      skills:
        '• Prepare a temporary slide of onion epidermis and a kale/spinach leaf section\n' +
        '• Apply a stain correctly (iodine solution) and observe colour change\n' +
        '• Estimate cell size using the field of view diameter and number of cells per field\n' +
        '• Draw a labelled diagram of cells observed',
      attitudes:
        '• Patience and care in laboratory work\n' +
        '• Accurate and honest observation and recording\n' +
        '• Appreciation for the skill of scientific drawing',
      keyInquiry: 'What can we see inside a real plant cell using a light microscope, and how do we prepare a specimen?',
      purposeInStoryline:
        'Students now make their OWN observations — gathering personal evidence about cell structure. ' +
        'Seeing real cells under a microscope connects the phenomenon (salamander cells) to tangible evidence. ' +
        'This lesson answers DQB questions like "Can we actually SEE cells?" and "Do all cells look the same?"',
      safetyNotes:
        '• Iodine solution stains skin and clothing — wear lab coat/apron, handle carefully\n' +
        '• Glass cover slips are fragile — handle from edges, never apply pressure directly\n' +
        '• Scalpel/blade used by teacher only for cutting sections\n' +
        '• Wash hands after handling iodine\n' +
        '• Report any broken glass immediately — do not pick up broken glass',
    },
    overview:
      'Students prepare temporary slides of onion epidermal cells, staining with dilute iodine solution ' +
      'to reveal the cell wall, nucleus, and vacuole. They observe under ×100 and ×400 magnification, ' +
      'make labelled diagrams, and estimate cell size using the field of view method. ' +
      'A second specimen — kale or spinach leaf cross-section — reveals palisade cells with visible chloroplasts. ' +
      'This introduces the idea that different cells in the SAME plant look different: the first glimpse ' +
      'of cell specialisation.\n\n' +
      'Students record their observations using the scientific drawing conventions (sharp outline, no shading, ' +
      'labels with horizontal lines, magnification stated). The lesson ends with students discussing: ' +
      '"Your onion cell and your kale cell look different. Why? What do you predict we will discover ' +
      'when we look at cells with an ELECTRON microscope?"',
    framework: [
      {
        phase: 'Predict Phase',
        learnerExperience:
          'Students look at three images: (1) a whole onion bulb, (2) a single onion cell diagram, (3) an electron micrograph of a plant cell. ' +
          '"These are all onion — at different scales. What structures do you expect to SEE when you make your own slide today?"',
        resource:
          'IMAGES: Onion bulb photo → light micrograph of onion cells → EM of plant cell (projected or printed)\n' +
          'TYPE: Visual scale sequence\n' +
          'LINK: CK-12 Biology — Plant Cell Structure (available offline on Rachel)',
        teacherMoves:
          '"Look carefully at these three images. These are all showing you the SAME organism — at different levels."\n' +
          '"Today you will see what IMAGE 2 looks like in real life. Before you start: what do you predict you will see?"\n' +
          'WAIT TIME: 45 seconds. Students write predictions.',
        sensemakingStrategy:
          'Scale Sequence — students move from macroscopic (whole onion) to microscopic (EM) so they ' +
          'understand that today\'s practical sits at the MIDDLE level.',
        formativeAssessment:
          'Predictions should name at least one structure. Students naming only "cells" need prompting: ' +
          '"What do you think is INSIDE the cell?"',
      },
      {
        phase: 'Observe Phase',
        learnerExperience:
          'PRACTICAL: Students prepare temporary slides in pairs.\n' +
          'Step 1: Peel a thin layer of onion epidermis. Place on slide. Add 2 drops of iodine. Lower cover slip at 45°.\n' +
          'Step 2: Focus at ×40, then ×100, then ×400.\n' +
          'Step 3: Draw what you see at ×100 — label cell wall, vacuole, cytoplasm, nucleus.\n' +
          'Step 4: Count cells across the field of view. Estimate cell width in micrometres.\n' +
          'Step 5 (if time): Observe kale palisade cells — note chloroplasts.',
        resource:
          'EQUIPMENT (per pair): Microscope, glass slide, cover slip, forceps, dropper bottle with dilute iodine, onion, blade (teacher pre-cuts sections)\n' +
          'OPTIONAL: Kale/spinach leaf cross-sections (teacher pre-cut)\n' +
          'HANDOUT: Blank scientific drawing frame, cell size estimation table\n' +
          'TYPE: Laboratory practical',
        teacherMoves:
          'Full class demonstration of slide preparation first (5 minutes).\n' +
          'Circulate every 3 minutes. Key correction: "Make your cover slip lower SLOWLY at an angle — you get fewer bubbles."\n' +
          '"Once you have found your cells, STOP moving the stage. Observe."\n' +
          '"Call me over before you draw — I want to confirm you have focused correctly."',
        sensemakingStrategy:
          'Lab Observation Protocol:\n' +
          'Students follow a structured sequence: observe → draw → annotate → estimate size.\n' +
          'Scientific drawing rules are applied: outlines only, no shading, labels with horizontal lines.',
        formativeAssessment:
          'Check drawings: Are cells drawn correctly (rectangular, not round)?\n' +
          'Are labels accurate (cell wall is the outermost boundary)?\n' +
          'Cell size estimation: expected range 50–100 micrometres for onion cells.',
      },
      {
        phase: 'Explain Phase',
        learnerExperience:
          'Class sharing: Groups project or hold up their drawings. ' +
          '"What did you see? What surprised you?" ' +
          'Teacher compares student drawings to a reference diagram and EM image. ' +
          'Class discusses: "Why does iodine make some structures visible?" ' +
          'Students annotate their drawings with explanation of WHY each structure is there.',
        resource:
          'REFERENCE: Labelled onion cell LM diagram (for comparison)\n' +
          'RESOURCE: EM image of plant cell showing all organelles (for comparison and connection to Lesson 4)\n' +
          'TYPE: Reference materials',
        teacherMoves:
          '"Compare your drawing to this reference diagram. What did you get right? What is different?"\n' +
          '"Who saw the nucleus clearly? Who struggled to see it — why might that be?"\n' +
          '"Now look at this EM image of a plant cell. What structures can YOU not see that the EM reveals?"\n' +
          '"Add the structures you CANNOT see with LM to your diagram — mark them as \'Too small for LM\'."',
        sensemakingStrategy:
          'Compare-and-Connect:\n' +
          'Students compare THEIR observations to (1) a reference diagram, and (2) an EM image.\n' +
          'This naturally motivates Lesson 4 — they can see what they are MISSING.',
        formativeAssessment:
          'Accurate labelled drawing = main formative assessment for this lesson.\n' +
          'Check: (1) correct cell shape, (2) correct labels, (3) magnification stated, (4) scale bar or cell count.',
      },
      {
        phase: 'Driving Question Board (DQB) Creation',
        learnerExperience:
          'Students review DQB. Which questions can they now answer from today\'s practical? ' +
          '"Can you see cells?" → YES (move to answered). ' +
          '"Do all cells look the same?" → Partially — kale cells had chloroplasts, onion cells did not! ' +
          'Students add new question: "Why do some plant cells have chloroplasts and others do not?"',
        resource:
          'MATERIALS: DQB poster, sticky notes, markers\n' +
          'TYPE: Class artefact',
        teacherMoves:
          '"We answered some questions today. Let\'s move them to \'Answered.\'" (2 minutes)\n' +
          '"But we created a NEW question — write it on a sticky note and add it to the board."\n' +
          '"The kale palisade cells had green organelles. The onion cells did not. Why the difference?"\n' +
          '"We will investigate this in Lesson 4."',
        sensemakingStrategy:
          'DQB Update — students recognise that evidence from today\'s practical both answers old questions AND creates new ones.\n' +
          'This models authentic science.',
        formativeAssessment:
          'Quality of new questions added shows depth of observation and curiosity.',
      },
      {
        phase: 'Model Building Phase',
        learnerExperience:
          'Students retrieve their model and UPDATE it with structures they observed today: ' +
          'cell wall, vacuole, cytoplasm, nucleus, and the NOTE "chloroplasts only in green cells." ' +
          'They date the update and write: "Evidence from: temporary slide practical, Lesson 3."',
        resource:
          'MATERIALS: Student model (from Lesson 1), pencil\n' +
          'PROMPT: "Add only what you SAW today with evidence. Label the source of evidence."\n' +
          'TYPE: Student portfolio',
        teacherMoves:
          '"Take out your model. Add ONLY the structures you observed today."\n' +
          '"Write \'Evidence: LM slide, Lesson 3\' next to each new addition."\n' +
          '"Your model should now be more detailed than after Lesson 1. Compare them."',
        sensemakingStrategy:
          'Evidence-Linked Modelling:\n' +
          'Students explicitly link each model addition to its evidence source. ' +
          'This practises scientific reasoning: conclusions must be evidence-based.',
        formativeAssessment:
          'Students should be able to say which structures they SAW (cell wall, vacuole, cytoplasm, nucleus) ' +
          'vs which they have NOT yet seen (mitochondria, ribosomes, Golgi — EM required).',
      },
    ],
    teacherReflection:
      'After teaching this lesson, reflect on:\n\n' +
      '1. How successfully did students prepare their temporary slides? What were the most common difficulties?\n\n' +
      '2. Were the cell drawings accurate and properly labelled? What drawing conventions were students struggling with?\n\n' +
      '3. Did students successfully estimate cell size? What errors occurred in the calculation?\n\n' +
      '4. Were students surprised by what they saw? Did the kale/spinach chloroplasts generate productive new questions?\n\n' +
      '5. What questions were added to the DQB from this lesson? Do they point toward cell specialisation (Lessons 6–7)?\n\n' +
      '6. How did you manage the practical — rotation, timing, safety? What would you change?',
    summaryTablePrompt: {
      observed:
        'Prepared a temporary slide of onion epidermal cells — peeled thin layer, applied iodine stain, observed under LM. ' +
        'Saw: cell wall (outermost boundary), large central vacuole, cytoplasm, nucleus. ' +
        'Kale palisade cells had visible green chloroplasts — onion cells did not. ' +
        'DQB updated: answered "Can we see cells?" Added question "Why do kale cells have chloroplasts but onion cells do not?"',
      learned:
        'Iodine stains cell walls and makes them visible. ' +
        'Plant cells are rectangular with a cell wall, large vacuole, cytoplasm, and nucleus. ' +
        'Different plant cells (onion vs kale) look DIFFERENT — this is the first evidence of specialisation. ' +
        'Cell size estimated at 50–100 micrometres.',
      explained:
        'The salamander phenomenon becomes more interesting: if different cells look different even in a simple onion, ' +
        'then the salamander\'s many cell types must also look different. ' +
        'But WHY? We cannot see the full answer with a light microscope — we need the electron microscope next.',
    },
  },

  // ── LESSON 4 ──────────────────────────────────────────────────────────────
  {
    number: 4,
    title: 'Inside the Cell — Organelles Under the Electron Microscope',
      aresKeywords: 'organelles electron microscope cell structure eukaryotic',
    duration: '2 periods / 80 minutes',
    slo: {
      purpose: 'Students study EM images to identify the major organelles of plant and animal cells and relate each structure to its function.',
      knowledge:
        '• Name and describe the following organelles: nucleus, cell membrane, cell wall (plants), mitochondria, ribosomes, endoplasmic reticulum (rough and smooth), Golgi body, chloroplast (plants), vacuole, cytoplasm\n' +
        '• State the function of each organelle listed above\n' +
        '• Describe how the organelles work together in the secretory pathway (ER → Golgi → cell membrane)',
      skills:
        '• Identify organelles from EM images using given photographs\n' +
        '• Match organelle structure to function using evidence from EM images\n' +
        '• Annotate a cell diagram with organelle names and brief functions',
      attitudes:
        '• Appreciation for the complexity and organisation within a cell\n' +
        '• Systematic approach to learning many structures at once\n' +
        '• Connection between structure and function as a biological principle',
      keyInquiry: 'What structures can be found inside a cell, and what does each structure do?',
      purposeInStoryline:
        'This is the CORE knowledge lesson. Students now have the evidence they need: the internal structures ' +
        'of cells. This answers many DQB questions from Lesson 1. It also sets up Lesson 5 (plant vs animal ' +
        'differences) and Lessons 6–7 (why specialised cells have particular organelles).',
      safetyNotes: 'No practical in this lesson. EM image analysis and research activity only.',
    },
    overview:
      'Students receive a set of annotated EM images showing a plant cell and an animal cell. ' +
      'In a jigsaw activity, expert groups each become specialists in 2–3 organelles, then teach ' +
      'the rest of the class. Each student builds a complete organelle reference table. ' +
      'The lesson closes with a whole-class discussion using the "factory analogy" — ' +
      'the cell as a factory, each organelle with a specific job — connecting structure to function.\n\n' +
      'By the end of this lesson, every student should be able to label a blank cell diagram with ' +
      'all major organelles and give a one-sentence function for each. The DQB questions about ' +
      '"what is inside a cell?" and "what does the nucleus do?" are answered and moved.',
    framework: [
      {
        phase: 'Predict Phase',
        learnerExperience:
          'Students look at their current model (from Lessons 1–3). ' +
          '"What do you think is missing? What structures have you NOT yet put into your model?" ' +
          'Students circle areas of uncertainty. ' +
          'Then: a blank cell outline is provided — "From memory, label everything you currently know."',
        resource:
          'MATERIALS: Student model notebook, blank cell outline diagram\n' +
          'TYPE: Memory recall prompt',
        teacherMoves:
          '"Look at your model. In 60 seconds, write all the organelles you currently know — go."\n' +
          'After 60 seconds: "Today we are going to fill ALL the gaps. Ready?"',
        sensemakingStrategy:
          'Retrieval Practice — students recall prior knowledge before new information is presented. ' +
          'This strengthens memory and shows students what they do and do not yet know.',
        formativeAssessment:
          'Quick check: How many organelles can students name from memory? ' +
          'Expected at this point: 3–5 (cell wall, nucleus, vacuole, cytoplasm, possibly mitochondria).',
      },
      {
        phase: 'Observe Phase',
        learnerExperience:
          'JIGSAW ACTIVITY:\n' +
          'Phase 1 — Expert Groups (15 min): Each group is assigned 2–3 organelles from EM images. ' +
          'They study the images, complete an "Expert Card" (name, appearance in EM, function, memory tip).\n' +
          'Phase 2 — Home Groups (15 min): Experts return to mixed groups and teach their organelles.\n' +
          'Each student completes a full organelle table from the group teaching.',
        resource:
          'EM IMAGE CARDS (printed): nucleus, mitochondria, ribosomes, RER, SER, Golgi body, chloroplast, vacuole, cell wall, cell membrane\n' +
          'HANDOUT: Expert Card template + full organelle table\n' +
          'LINK: LabXchange — Cell organelles interactive (offline on Rachel)\n' +
          'TYPE: Collaborative research activity',
        teacherMoves:
          'Setup: Assign expert groups carefully (mix abilities).\n' +
          'During Expert Phase: Circulate to each group. Ask: "Can you describe what it looks like in the EM image?"\n' +
          'During Home Phase: "I will call on any group member randomly to explain one organelle — be ready."\n' +
          'After jigsaw: Cold-call 6 students: "What is the function of the [organelle]?"',
        sensemakingStrategy:
          'Jigsaw Cooperative Learning:\n' +
          'Every student becomes an expert and a learner. ' +
          'Teaching requires deeper understanding than simply receiving information.',
        formativeAssessment:
          'Expert Card quality: Is the function accurate? Is the appearance description correct?\n' +
          'Home group: Can every student fill in the full organelle table accurately?\n' +
          'Random cold-call after jigsaw reveals gaps.',
      },
      {
        phase: 'Explain Phase',
        learnerExperience:
          'Whole-class synthesis: Teacher presents the "secretory pathway" — how proteins are made at ribosomes (RER), ' +
          'packaged in Golgi, and secreted through the cell membrane. ' +
          'Students trace the pathway on their organelle diagram with arrows. ' +
          'Class discusses: "The cell is like a factory — what department does each organelle represent?"',
        resource:
          'DIAGRAM: Secretory pathway (ER → Golgi → cell membrane) — drawn live on board or pre-printed\n' +
          'ANALOGY CARD: Cell = factory (nucleus = CEO/manager, mitochondria = power plant, ribosomes = production line…)\n' +
          'TYPE: Conceptual synthesis',
        teacherMoves:
          '"I want you to trace a protein\'s journey. It starts at the nucleus. Where is it made? Where is it packaged? Where does it go?"\n' +
          'Students draw arrows. Teacher checks.\n' +
          '"Think about the cell as a factory. What is the mitochondria? What is the nucleus? What is the cell membrane?"\n' +
          'WAIT TIME: 15 seconds before taking responses.',
        sensemakingStrategy:
          'Analogy Mapping:\n' +
          'Cell-as-factory analogy makes abstract organelle functions concrete.\n' +
          'Students create their own analogy (cell = school, city, sports team) for homework.',
        formativeAssessment:
          'Students correctly trace the secretory pathway on their diagram.\n' +
          'Exit ticket: "Name the organelle AND its function" for any 3 organelles (teacher selects).',
      },
      {
        phase: 'Driving Question Board (DQB) Creation',
        learnerExperience:
          'Students move many Lesson 1 questions to "ANSWERED": "What is inside a cell?", "What does the nucleus do?" etc. ' +
          'New question added: "If all cells have the same organelles, why do they look so different?" ' +
          'This question drives Lessons 5–7.',
        resource:
          'MATERIALS: DQB poster, sticky notes, markers\n' +
          'TYPE: Class artefact',
        teacherMoves:
          '"How many of our original questions can we answer now? Let\'s go through them one by one."\n' +
          '(Spend 5 minutes reviewing DQB — moving answered questions.)\n' +
          '"But here is a new puzzle: If ALL cells have a nucleus, mitochondria, and ribosomes — why does a nerve cell look NOTHING like a red blood cell?"',
        sensemakingStrategy:
          'DQB Transition: from "what is inside?" to "why are cells different?" — this transition marks ' +
          'a shift in the storyline from knowledge-gathering to explanation-building.',
        formativeAssessment:
          'Quality of discussion during DQB review shows depth of understanding.',
      },
      {
        phase: 'Model Building Phase',
        learnerExperience:
          'MAJOR MODEL UPDATE: Students redraw their model (or heavily annotate it) to include ALL major organelles. ' +
          'This is the most significant model update of the unit. ' +
          'Students compare Lesson 1 model to today\'s model: "How has your thinking changed?"',
        resource:
          'MATERIALS: Student model portfolio, blank A4 paper for revised model, coloured pencils\n' +
          'REFERENCE: Completed organelle table\n' +
          'TYPE: Student portfolio',
        teacherMoves:
          '"Redraw your cell model — include EVERY organelle from today\'s table. Label them."\n' +
          '"Add a box in the corner: \'Evidence source: EM images, Lesson 4\'"\n' +
          'After 10 minutes: "Hold your Lesson 1 model next to your Lesson 4 model. Tell your partner: what changed? WHY?"',
        sensemakingStrategy:
          'Model Comparison — students explicitly reflect on growth in understanding.\n' +
          'This is a high-leverage sensemaking strategy: metacognitive reflection on conceptual change.',
        formativeAssessment:
          'Lesson 4 model completeness: Does it include all major organelles correctly positioned and labelled?\n' +
          'Student comparison statement: Can they articulate what changed in their understanding?',
      },
    ],
    teacherReflection:
      'After teaching this lesson, reflect on:\n\n' +
      '1. Did the jigsaw activity work effectively? Were all students able to teach their organelles confidently?\n\n' +
      '2. Which organelles caused most confusion? (Common difficulties: RER vs SER, Golgi body function)\n\n' +
      '3. Could students trace the secretory pathway correctly? Did the factory analogy help?\n\n' +
      '4. How significantly did students\' models change from Lesson 1? What does this reveal about learning?\n\n' +
      '5. Which DQB questions were resolved? What is the most important remaining question for Lessons 5–7?\n\n' +
      '6. Was 80 minutes enough for the jigsaw + model update? What would you trim or expand?',
    summaryTablePrompt: {
      observed:
        'Studied EM images of plant and animal cells. Identified organelles: nucleus, cell membrane, cell wall, ' +
        'mitochondria, ribosomes, RER, SER, Golgi body, chloroplast, large vacuole, cytoplasm. ' +
        'Traced the secretory pathway: ribosome (RER) → Golgi → cell membrane. ' +
        'Major model update — model now shows all major organelles. ' +
        'DQB: answered "What is inside a cell?" Added "Why do cells look different if they all have the same organelles?"',
      learned:
        'Every cell has a set of organelles, each with a specific function. ' +
        'The nucleus is the control centre (contains DNA). Mitochondria produce energy (ATP). ' +
        'Ribosomes make proteins. Golgi body packages and distributes proteins. ' +
        'Chloroplasts (in plant cells only) photosynthesise.',
      explained:
        'The salamander embryo has the DNA to make ALL types of cells. ' +
        'Each cell type uses a DIFFERENT set of organelles — or has MORE of a particular organelle. ' +
        'A muscle cell has MANY mitochondria (needs lots of energy). A secretory cell has a large Golgi body. ' +
        'STRUCTURE determines FUNCTION. This is the key insight!',
    },
  },

  // ── LESSON 5 ──────────────────────────────────────────────────────────────
  {
    number: 5,
    title: 'Plant vs Animal Cells — Key Differences',
      aresKeywords: 'plant animal cell differences chloroplast cell wall vacuole',
    duration: '2 periods / 80 minutes',
    slo: {
      purpose: 'Students systematically distinguish plant and animal cells, connecting differences to the functions of whole plants and animals.',
      knowledge:
        '• State the structures present in plant cells but NOT animal cells: cell wall, chloroplast, large permanent central vacuole\n' +
        '• State the structures present in animal cells but NOT plant cells: centrioles, small temporary vacuoles\n' +
        '• Explain WHY these differences exist, linking to the different lifestyles of plants and animals',
      skills:
        '• Construct a comparison table of plant vs animal cell features\n' +
        '• Annotate EM images correctly to distinguish plant from animal cells\n' +
        '• Explain, using evidence, which cell type (plant or animal) is shown in an unknown image',
      attitudes:
        '• Appreciation for diversity at the cellular level\n' +
        '• Systematic approach to identifying differences\n' +
        '• Connecting cell-level knowledge to whole-organism biology',
      keyInquiry: 'Why do plant and animal cells differ — and what do these differences tell us about how each organism lives?',
      purposeInStoryline:
        'The DQB question from Lesson 4 ("Why do cells look different?") begins to be answered here — ' +
        'first at the kingdom level (plant vs animal). This prepares students for Lessons 6–7 ' +
        'where they see specialisation within a single organism.',
      safetyNotes: 'No practical in this lesson. Image analysis and research activity.',
    },
    overview:
      'Students receive unlabelled EM images of a plant cell and an animal cell. Without prior labelling, ' +
      'they must identify which is which and justify their answer. This "identify the mystery cell" challenge ' +
      'drives the core investigation of this lesson. Groups share their reasoning, and the class builds ' +
      'a structured comparison table together.\n\n' +
      'The lesson includes a brief simulation or video showing how chloroplasts and cell walls give plants ' +
      'their rigid structure — connecting to students\' experience of why plant stems stand upright without ' +
      'a skeleton. The lesson ends with a model revision and an updated DQB with the question: ' +
      '"If plant and animal cells differ, do all plant cells look the same? Do all animal cells?"',
    framework: [
      {
        phase: 'Predict Phase',
        learnerExperience:
          '"Here are two EM images. One is a plant cell. One is an animal cell. Which is which? ' +
          'Write your answer and give THREE pieces of evidence from the image." ' +
          'Individual work, then pair discussion.',
        resource:
          'IMAGE CARDS: Unlabelled EM image of plant cell vs animal cell (printed, one per pair)\n' +
          'TYPE: Evidence-based identification challenge',
        teacherMoves:
          '"Do NOT look anything up. Use what you already know from Lesson 4 to identify these cells."\n' +
          'WAIT TIME: 3 minutes of silent individual work.\n' +
          '"Now discuss with your partner. Did you agree or disagree? Who has stronger evidence?"',
        sensemakingStrategy:
          'Claim-Evidence-Reasoning:\n' +
          'Students make a CLAIM (this is a plant cell), provide EVIDENCE (from the image), and REASONING (because…).',
        formativeAssessment:
          'Can students use organelle presence/absence as evidence?\n' +
          'Expected evidence: cell wall = rigid outer boundary; chloroplasts = green circular organelles; large central vacuole.',
      },
      {
        phase: 'Observe Phase',
        learnerExperience:
          'Groups present their identifications and reasoning to the class. ' +
          'Teacher facilitates discussion: "Group 1 says cell A is plant. Group 3 says cell A is animal. ' +
          'Who has stronger evidence?" ' +
          'Class collaboratively builds the comparison table: structures present in plant / absent in animal, and vice versa.',
        resource:
          'BOARD / PROJECTED TABLE: Blank plant vs animal cell comparison table\n' +
          'REFERENCE: Student organelle tables from Lesson 4\n' +
          'LINK: Khan Academy — Plant vs Animal Cells (offline Rachel)\n' +
          'TYPE: Structured discussion and table-building',
        teacherMoves:
          'Cold-call one group per image: "Read your evidence."\n' +
          'Ask opposing groups: "Do you agree? What is your counter-argument?"\n' +
          '"What is our BEST evidence for plant cells? Compile the table together."\n' +
          'Teacher fills the shared table based on student responses (not pre-filled).',
        sensemakingStrategy:
          'Socratic Seminar — student-led evidence comparison. Teacher facilitates, does not lecture.',
        formativeAssessment:
          'Accuracy of completed comparison table.\n' +
          'Key check: students correctly identify cell wall + chloroplast + large central vacuole as plant-only.',
      },
      {
        phase: 'Explain Phase',
        learnerExperience:
          '"WHY do plant cells have a cell wall?" Discussion: plants do not have a skeleton — the cell wall provides ' +
          'mechanical support. "WHY do plant cells have chloroplasts?" Discussion: plants make their own food. ' +
          '"WHY do plant cells have a large central vacuole?" Discussion: stores water — keeps cells rigid (turgor pressure). ' +
          'Students write a 3-sentence explanation connecting each difference to the plant\'s lifestyle.',
        resource:
          'VIDEO (2 min): Time-lapse of plant wilting when dehydrated, becoming turgid when watered\n' +
          'LINK: SciShow — Why are plants green? (Rachel / YouTube)\n' +
          'TYPE: Video stimulus for discussion',
        teacherMoves:
          '"Why does a plant not fall over without bones?" WAIT TIME: 15 seconds.\n' +
          '"Connect your answer to the CELL WALL."\n' +
          '"Why does a wilted plant perk up when you water it?" WAIT TIME: 15 seconds.\n' +
          '"Connect your answer to the VACUOLE."',
        sensemakingStrategy:
          'Structure-Function Connection:\n' +
          'Students connect organelle presence to whole-organism function. ' +
          'This is the key biological principle of this lesson.',
        formativeAssessment:
          '3-sentence written explanation: Does it correctly link cell wall → support, chloroplast → photosynthesis, vacuole → turgor?',
      },
      {
        phase: 'Driving Question Board (DQB) Creation',
        learnerExperience:
          'DQB update: "We now know WHY plant and animal cells differ." Move relevant questions to answered. ' +
          'Add new question: "Do all plant cells have chloroplasts? Do all animal cells look the same?" ' +
          '(This directly sets up Lessons 6–7.)',
        resource:
          'MATERIALS: DQB poster, sticky notes\n' +
          'TYPE: Class artefact',
        teacherMoves:
          '"We answered why plant and animal cells differ. Great. But now — new question."\n' +
          '"Does EVERY plant cell have chloroplasts?" (Answer: no — root cells do not!)\n' +
          '"Does EVERY animal cell look the same?" (Answer: no — look at a neuron vs RBC.)\n' +
          '"Why? We explore this in Lessons 6 and 7."',
        sensemakingStrategy:
          'Problematising — teacher deliberately creates a new puzzle to motivate the next lessons.',
        formativeAssessment:
          'Student responses to "do all plant cells have chloroplasts?" reveal depth of understanding.',
      },
      {
        phase: 'Model Building Phase',
        learnerExperience:
          'Students draw TWO models: (1) a generalised plant cell with all distinctive structures labelled, ' +
          '(2) a generalised animal cell with all distinctive structures labelled. ' +
          'Models are placed side-by-side in portfolio. ' +
          '"Write one sentence on each: what does this cell type\'s structure tell us about how it lives?"',
        resource:
          'MATERIALS: Student model portfolio, blank A4 paper, coloured pencils\n' +
          'TYPE: Student portfolio',
        teacherMoves:
          '"Draw your best plant cell AND your best animal cell. Side by side."\n' +
          '"Label EVERY organelle — not just the ones that are different."\n' +
          '"Write your explanation sentence under each model. I will check these at the end of class."',
        sensemakingStrategy:
          'Comparative Modelling — drawing both types side by side makes differences explicit.',
        formativeAssessment:
          'Models should correctly show: cell wall, chloroplasts, large central vacuole (plant only); ' +
          'centrioles, small temporary vacuoles (animal only).',
      },
    ],
    teacherReflection:
      'After teaching this lesson, reflect on:\n\n' +
      '1. Could students correctly identify plant vs animal cell from EM images using evidence? What evidence did they cite?\n\n' +
      '2. Did students understand the WHY behind differences (cell wall for support, chloroplasts for photosynthesis)?\n\n' +
      '3. Were students surprised that not all plant cells have chloroplasts? Did this effectively create the problem for Lesson 6?\n\n' +
      '4. How accurate and complete are the dual plant/animal cell models?\n\n' +
      '5. What misconceptions remained about plant vs animal cells?\n\n' +
      '6. What would you change about the "mystery cell" identification challenge?',
    summaryTablePrompt: {
      observed:
        'Analysed unlabelled EM images to identify plant vs animal cells using evidence. ' +
        'Built comparison table: plant cells have cell wall, chloroplasts, large central vacuole; ' +
        'animal cells have centrioles, small temporary vacuoles. ' +
        'Watched video of plant wilting and recovering — connected to vacuole and turgor pressure.',
      learned:
        'Plant cells have cell wall (support), chloroplasts (photosynthesis), and large central vacuole (water storage/turgor). ' +
        'Animal cells have centrioles and small temporary vacuoles. ' +
        'These differences reflect the different lifestyles of plants (stationary, self-feeding) and animals (mobile, consumer).',
      explained:
        'The salamander cells are animal cells — no cell walls or chloroplasts. ' +
        'But plant and animal cells are just TWO types. The deeper question remains: ' +
        'within a salamander (one animal), why do its BILLIONS of cells look so different from each other? ' +
        'That is what Lessons 6 and 7 explain.',
    },
  },

  // ── LESSON 6 ──────────────────────────────────────────────────────────────
  {
    number: 6,
    title: 'Specialised Cells in Plants — Structure Serves Function',
      aresKeywords: 'specialised cells plants xylem phloem guard cells',
    duration: '2 periods / 80 minutes',
    slo: {
      purpose: 'Students investigate plant cell specialisation — connecting the unique structure of each cell type to its specific function in the plant.',
      knowledge:
        '• Describe the structure and function of root hair cells (long extension, no chloroplasts, thin wall)\n' +
        '• Describe the structure and function of guard cells (bean-shaped, chloroplasts, unequal wall thickness)\n' +
        '• Describe the structure and function of xylem vessels (no cytoplasm, lignified walls, hollow — for water transport)\n' +
        '• Describe the structure and function of phloem sieve tube cells (sieve plates, companion cells — for food transport)',
      skills:
        '• Identify specialised plant cells from diagrams and micrographs\n' +
        '• Match specific structural adaptations to the function they serve\n' +
        '• Explain why a root hair cell does NOT need chloroplasts',
      attitudes:
        '• Appreciation for the elegant match between cell structure and function in living organisms\n' +
        '• Curiosity about how plants maintain water balance\n' +
        '• Connecting cellular biology to whole-plant physiology',
      keyInquiry: 'How are plant cells specialised to carry out specific functions — and how does structure relate to function?',
      purposeInStoryline:
        'This lesson directly addresses the core question "How are cells specialised?" (KICD Key Inquiry Q2). ' +
        'Students begin to see that specialisation = having MORE or FEWER of certain organelles, ' +
        'or having a modified shape. This connects directly back to the salamander: ' +
        'its cells specialise by the SAME principle.',
      safetyNotes:
        'If optional practical (observing cross-sections): standard microscope safety (see Lesson 2). ' +
        'Handle prepared slides with care. Iodine stain available for root hair cell observation.',
    },
    overview:
      'Students are presented with four "mystery plant jobs": water absorption from soil, ' +
      'opening and closing leaf pores, water transport from roots to leaves, and sugar transport from leaves. ' +
      'In groups, they research which cell type does each job and HOW its structure makes it suited for that job. ' +
      'This research-then-share approach builds both content knowledge and scientific communication skills.\n\n' +
      'The lesson connects back to the phenomenon: the salamander grows different cell types to perform ' +
      'different jobs. Plants do the same thing. The principle of specialisation — modifying structure ' +
      'to serve function — is universal in living organisms.',
    framework: [
      {
        phase: 'Predict Phase',
        learnerExperience:
          '"A plant needs to: (1) absorb water from soil, (2) control gas exchange at leaves, ' +
          '(3) transport water from roots to leaves, (4) transport sugar from leaves to roots. ' +
          'Predict: what would the IDEAL cell for each job LOOK LIKE?" ' +
          'Students sketch a "dream cell" for Job 1 and Job 2 before any instruction.',
        resource:
          'PROMPT CARD: 4 plant jobs listed, with empty cell outlines for students to sketch "ideal cell"\n' +
          'TYPE: Structured prediction task',
        teacherMoves:
          '"Before we look at real cells, design your own. What would YOU include if you were designing a water-absorbing cell?"\n' +
          'WAIT TIME: 3 minutes.\n' +
          '"Now compare your design to your partner\'s. What did you both include? What is different?"',
        sensemakingStrategy:
          'Structured Prediction / Design Thinking:\n' +
          'Students apply structure-function reasoning from Lesson 4 to invent a specialised cell — ' +
          'then compare their design to the real thing.',
        formativeAssessment:
          'Do student designs show understanding that function drives structure? ' +
          '(e.g., water-absorbing cell should have large surface area)',
      },
      {
        phase: 'Observe Phase',
        learnerExperience:
          'JIGSAW — Expert groups each study one plant cell type:\n' +
          'Group A: Root hair cells | Group B: Guard cells | Group C: Xylem vessels | Group D: Phloem sieve tubes\n' +
          'Each group receives: a diagram, a micrograph, a written description, and a function statement. ' +
          'Expert Card to complete: appearance, adaptations, functions, connection to the plant.',
        resource:
          'RESOURCE PACK (per group): Diagram + micrograph + written description for their cell type\n' +
          'SOURCE: CK-12 Biology, Khan Academy Plant Biology (offline on Rachel)\n' +
          'EXPERT CARD: Printed template for each student\n' +
          'TYPE: Differentiated jigsaw research',
        teacherMoves:
          '"Each group becomes the class EXPERT on one cell. You will need to TEACH the rest of us."\n' +
          '"Focus on: (1) what makes it look different? (2) how does that difference help it do its job?"\n' +
          'Circulate and prompt: "Why does a root hair cell NOT have chloroplasts?" WAIT TIME: 15 seconds.',
        sensemakingStrategy:
          'Jigsaw — Expert Teaching:\n' +
          'Teaching others requires deeper understanding than listening. ' +
          'Each student is both expert and learner.',
        formativeAssessment:
          'Expert Card accuracy: Is the adaptation-function link clear? ' +
          '(Root hair: long extension = more surface area for absorption; no chloroplasts = underground, no light)',
      },
      {
        phase: 'Explain Phase',
        learnerExperience:
          'Home groups reconvene — each expert teaches their cell. ' +
          'All students complete a class summary table: Cell Type | Location | Structural Adaptations | Functions. ' +
          'Groups compare their "predicted design" from the opening with the actual cell — ' +
          '"How did nature\'s design compare to yours? What was the same? What was different? Why?"',
        resource:
          'HANDOUT: Full summary table for all 4 plant cell types\n' +
          'REFERENCE: Student\'s own prediction sketches from the opening activity\n' +
          'TYPE: Synthesis and comparison',
        teacherMoves:
          '"Compare: YOUR designed cell vs the REAL cell. Describe ONE similarity and ONE difference."\n' +
          'Cold-call 4 students (one per cell type) to summarise adaptations.\n' +
          '"What is the MOST important adaptation for each cell type? Why?"',
        sensemakingStrategy:
          'Design vs Reality Comparison:\n' +
          'Students connect their own reasoning to real biological design — ' +
          'this reinforces the structure-function principle.',
        formativeAssessment:
          'Completed summary table accuracy. ' +
          'Can students explain WHY each adaptation exists (not just name it)?',
      },
      {
        phase: 'Driving Question Board (DQB) Creation',
        learnerExperience:
          'DQB update: Move "How are cells specialised?" to ANSWERED (for plant cells). ' +
          'Add connection to the driving question: "If plant cells specialise by modifying structure, ' +
          'do animal cells use the SAME principle?" Post as a bridge question to Lesson 7.',
        resource:
          'MATERIALS: DQB poster, sticky notes\n' +
          'TYPE: Class artefact',
        teacherMoves:
          '"We have answered HOW plant cells specialise. Move that question."\n' +
          '"But — does the salamander follow the same rule? Write that question on a sticky note and post it."',
        sensemakingStrategy:
          'Bridge Question — students make the connection between plant and animal specialisation before Lesson 7.',
        formativeAssessment:
          'Quality of bridge question shows readiness to transfer learning.',
      },
      {
        phase: 'Model Building Phase',
        learnerExperience:
          'Students ADD four plant specialist cells to their portfolio — each drawn and labelled with adaptations. ' +
          'They annotate: "Specialisation principle: MODIFIED STRUCTURE = SPECIFIC FUNCTION." ' +
          'Students connect this to the salamander: "The salamander also has specialised cells. Predict what two of them might look like."',
        resource:
          'MATERIALS: Student model portfolio, blank A4 paper\n' +
          'TYPE: Student portfolio addition',
        teacherMoves:
          '"Add the four plant specialist cells to your portfolio. Label their key adaptations."\n' +
          '"Write the specialisation principle at the top of this page."\n' +
          '"Predict: what two types of specialised animal cells do you expect we will study in Lesson 7?"',
        sensemakingStrategy:
          'Predictive Extension — using plant cell patterns to predict animal cell patterns.',
        formativeAssessment:
          'Student predictions for animal cells show transfer of the specialisation principle.',
      },
    ],
    teacherReflection:
      'After teaching this lesson, reflect on:\n\n' +
      '1. Could students articulate the structure-function link for each plant cell type?\n\n' +
      '2. Which specialised cell was hardest to understand? (Often: xylem — students struggle with "dead cell with no cytoplasm")\n\n' +
      '3. Did the "design your own cell" prediction activity help students appreciate the real cells?\n\n' +
      '4. Were student predictions for animal specialised cells (end of lesson) reasonable? What does this show about transfer?\n\n' +
      '5. Were there any misconceptions about chloroplasts being in all plant cells?\n\n' +
      '6. How effective was the jigsaw format for this lesson?',
    summaryTablePrompt: {
      observed:
        'Studied four specialised plant cell types: root hair cells (long extensions, no chloroplasts), ' +
        'guard cells (bean-shaped, unequal wall thickness, control stomata opening), ' +
        'xylem (hollow tubes, lignified walls, dead at maturity), phloem (sieve plates, living companion cells). ' +
        'Compared "ideal cell designs" to real cells.',
      learned:
        'Specialisation = modifying cell structure to optimise function. ' +
        'Root hair cells maximise surface area for water absorption. ' +
        'Guard cells change shape to open/close stomata. ' +
        'Xylem is hollow and dead — perfect for water transport. ' +
        'Phloem uses sieve plates to move dissolved sugars.',
      explained:
        'Plants specialise their cells the same way the salamander does — by modifying structure for function. ' +
        'The specialisation principle is UNIVERSAL in living organisms. ' +
        'Next: animal cells use this same principle — the salamander\'s nerve cells, muscle cells, and blood cells all have modified structures for their specific jobs.',
    },
  },

  // ── LESSON 7 ──────────────────────────────────────────────────────────────
  {
    number: 7,
    title: 'Specialised Cells in Animals — Connecting Back to the Salamander',
      aresKeywords: 'specialised cells animals nerve muscle red blood cell',
    duration: '2 periods / 80 minutes',
    slo: {
      purpose: 'Students investigate animal cell specialisation, directly connecting to the anchoring phenomenon (salamander) and completing the explanation of how one cell produces many different types.',
      knowledge:
        '• Describe the structure and function of red blood cells (biconcave disc, no nucleus, haemoglobin — oxygen transport)\n' +
        '• Describe the structure and function of sperm cells (head with acrosome, midpiece with mitochondria, long flagellum — fertilisation)\n' +
        '• Describe the structure and function of nerve cells/neurones (long axon, dendrites, myelin sheath — fast signal transmission)\n' +
        '• Describe the structure and function of muscle cells/fibres (many mitochondria, myofibrils — contraction)\n' +
        '• Describe the structure and function of egg cells (large, yolk for nutrition, jelly coat — fertilisation)',
      skills:
        '• Match specialised animal cell structures to their specific functions\n' +
        '• Construct an explanation using multiple cell types as evidence\n' +
        '• Revise the DQB to show the unit\'s driving question is now answerable',
      attitudes:
        '• Appreciation for the elegance of biological specialisation\n' +
        '• Connecting cell biology to human health and reproduction\n' +
        '• Wonder at the fact that one salamander egg cell eventually produces all these different types',
      keyInquiry: 'How are animal cells specialised — and how does this explain how a single fertilised egg becomes a complex organism?',
      purposeInStoryline:
        'This lesson DIRECTLY answers the driving question for the first time. ' +
        'Students can now explain the salamander phenomenon: one cell divides and differentiates, ' +
        'with different cells switching on different genes to produce different organelle combinations. ' +
        'The salamander time-lapse is shown AGAIN at the end — students should be able to narrate it now.',
      safetyNotes:
        '• Prepared microscope slides of blood smear or nerve tissue can be viewed if available\n' +
        '• Standard microscope safety applies (see Lesson 2)\n' +
        '• If using blood smear slides: treat as biological material — wash hands after use',
    },
    overview:
      'Students review their Lesson 6 plant cell specialisation work, then immediately investigate five ' +
      'animal cell types using the same approach: examine structure, identify adaptations, explain function. ' +
      'A red blood cell is the opening focus — its loss of nucleus is striking and memorable. ' +
      'The lesson builds toward the key moment: the salamander time-lapse is shown again and students ' +
      'narrate what is happening in terms of cell differentiation. "In Week 1 of development, all the cells ' +
      'look the same. By Week 4, you can see different cell types forming. Why? Because different cells ' +
      'start expressing different genes and making different organelle combinations."\n\n' +
      'This lesson closes the main evidential arc of the unit. The DQB is now largely answered.',
    framework: [
      {
        phase: 'Predict Phase',
        learnerExperience:
          '"From Lesson 6, you know the specialisation PRINCIPLE: structure is modified for function. ' +
          'Now apply it: predict what a cell that transports oxygen would look like. ' +
          'Predict what a cell that must travel long distances in the body would look like." ' +
          'Individual sketches, then pair comparison.',
        resource:
          'PROMPT CARD: "Design a cell that: (1) carries oxygen, (2) travels through blood vessels, ' +
          '(3) carries a lot of haemoglobin" — what would it look like?\n' +
          'TYPE: Transfer prediction',
        teacherMoves:
          '"You know the RULE now: structure follows function. Apply it to these animal cells."\n' +
          'WAIT TIME: 3 minutes for sketching.\n' +
          '"Share your prediction — what did you include? Why?"',
        sensemakingStrategy:
          'Transfer Application:\n' +
          'Students apply the specialisation principle learned in Lesson 6 to predict animal cell features before observation.',
        formativeAssessment:
          'Do student predictions show transfer of the specialisation principle? ' +
          '(e.g., "no nucleus — more room for haemoglobin"; "disc shape — more surface area for oxygen loading")',
      },
      {
        phase: 'Observe Phase',
        learnerExperience:
          'CARD SORT INVESTIGATION:\n' +
          'Groups receive image cards + description cards for 5 cell types (RBC, sperm, nerve, muscle fibre, egg cell). ' +
          'Task: Match image → description → function → KEY adaptation. ' +
          'Then each student draws and labels each cell type in their notebook.',
        resource:
          'CARD SORT SET: Images + descriptions + function statements for 5 animal cell types\n' +
          'OPTIONAL: Prepared blood smear slide for microscope observation\n' +
          'LINK: Khan Academy — Specialised animal cells (offline Rachel)\n' +
          'TYPE: Card sort + optional practical observation',
        teacherMoves:
          '"Lay out all cards. Do NOT read the descriptions first — match image to image first, then add descriptions."\n' +
          '"Why does the red blood cell have NO nucleus?" WAIT TIME: 15 seconds.\n' +
          'After matching: "Cold-call time. Group 3 — explain the sperm cell adaptations."',
        sensemakingStrategy:
          'Card Sort — physical manipulation forces active processing of relationships between features.',
        formativeAssessment:
          'Accuracy of card sort matching.\n' +
          'Quality of explanations during cold-call.',
      },
      {
        phase: 'Explain Phase',
        learnerExperience:
          'SALAMANDER REVISIT: Show the time-lapse again (2 min). ' +
          'This time, students narrate: "At 0:30, those cells are all the same — undifferentiated. ' +
          'By 2:00, you can see nerve cells forming in the spine region. By 4:00, muscle cells in the tail." ' +
          '"Using what you know about cell specialisation — explain how ONE cell became all of those."',
        resource:
          'VIDEO: Salamander time-lapse (same as Lesson 1 — full circle!)\n' +
          'PROMPT: "Narrate what you see. Use cell biology vocabulary you have learned."\n' +
          'TYPE: Return to anchoring phenomenon',
        teacherMoves:
          '"We are watching the same video as Lesson 1. But now you understand what is happening."\n' +
          '"Narrate to your partner as you watch — what is happening at the cell level?"\n' +
          'After video: "Now write a 3-sentence explanation: HOW does one cell become many different types?"',
        sensemakingStrategy:
          'Return to Phenomenon — full-circle moment. Students use ALL accumulated knowledge to explain ' +
          'what they could not explain in Lesson 1. This is the unit\'s key sensemaking payoff.',
        formativeAssessment:
          '3-sentence explanation: Does it include (1) cell division, (2) differentiation / different genes activated, (3) different organelle combinations → different functions?\n' +
          'This is the formative check for the whole unit\'s driving question.',
      },
      {
        phase: 'Driving Question Board (DQB) Creation',
        learnerExperience:
          'MAJOR DQB REVIEW: Students walk through EVERY question on the DQB from Lesson 1. ' +
          '"Can we answer this now?" Move all answerable questions to ANSWERED. ' +
          'Celebrate: the driving question can now be answered. ' +
          'Any remaining questions become the "future inquiry" section.',
        resource:
          'MATERIALS: DQB poster, markers\n' +
          'TYPE: Class synthesis activity',
        teacherMoves:
          '"Let\'s go through every question. Can we answer it? I will read each one."\n' +
          'Class votes: answered or not answered.\n' +
          '"Look at how many questions we answered across this unit. That is science — evidence by evidence."',
        sensemakingStrategy:
          'DQB Final Review — metacognitive celebration of learning and progress.\n' +
          'Students see the arc of the unit from first question to final explanation.',
        formativeAssessment:
          'Are the major questions answered? Can students give evidence-based answers?\n' +
          'Questions that remain unanswered point to areas for further study or Lessons 8 extension.',
      },
      {
        phase: 'Model Building Phase',
        learnerExperience:
          'Students draw the five specialised animal cells in their portfolio. ' +
          'They annotate: "ALL the same DNA → DIFFERENT genes activated → DIFFERENT organelle combinations → DIFFERENT functions." ' +
          'Students compare their Lesson 1 model to their Lesson 7 model side by side: ' +
          '"Write 3 sentences about how your understanding of cells has changed."',
        resource:
          'MATERIALS: Student model portfolio, blank A4 paper, coloured pencils\n' +
          'TYPE: Portfolio capstone entry (for this lessons-1-7 arc)',
        teacherMoves:
          '"Draw the five animal cell types — label key adaptations for each."\n' +
          '"Then compare Lesson 1 vs Lesson 7 model. Write 3 sentences — \'My thinking has changed because...\'"',
        sensemakingStrategy:
          'Reflective Model Comparison — most powerful metacognitive strategy of the unit. ' +
          'Students see concrete evidence of their own conceptual growth.',
        formativeAssessment:
          'Quality of 3-sentence reflection: Does it show genuine conceptual change?\n' +
          'Lesson 7 models: Are animal cell adaptations correctly drawn and explained?',
      },
    ],
    teacherReflection:
      'After teaching this lesson, reflect on:\n\n' +
      '1. When students watched the salamander time-lapse the SECOND time — was their narration using cell biology vocabulary? How rich was it compared to Lesson 1?\n\n' +
      '2. Could students write a clear 3-sentence explanation of how ONE cell becomes MANY different types?\n\n' +
      '3. Which animal cell type was most memorable or surprising for students?\n\n' +
      '4. Was the DQB final review celebration effective? Did students feel a sense of accomplishment?\n\n' +
      '5. What gaps remain that Lesson 8 (levels of organisation) should address?\n\n' +
      '6. How would you strengthen the connection between this lesson and the original phenomenon if you taught it again?',
    summaryTablePrompt: {
      observed:
        'Card sort investigation of 5 animal cell types: ' +
        'RBC (biconcave disc, no nucleus, filled with haemoglobin), ' +
        'sperm (head with acrosome, mitochondria-packed midpiece, long flagellum), ' +
        'neurone (long axon, branching dendrites, myelin sheath), ' +
        'muscle fibre (many mitochondria, myofibrils), ' +
        'egg cell (large, yolk store, jelly coat). ' +
        'Watched salamander time-lapse AGAIN and narrated using cell biology vocabulary. ' +
        'DQB major review — most questions now answered.',
      learned:
        'Animal cells specialise by modifying structure for function — same principle as plant cells. ' +
        'RBC loses its nucleus to carry maximum haemoglobin. ' +
        'Nerve cells have long axons for distance signal transmission. ' +
        'One fertilised egg → billions of specialised cells because different genes are activated in different cells (differentiation).',
      explained:
        'THE PHENOMENON IS NOW EXPLAINED: The salamander starts as ONE cell with a full set of DNA. ' +
        'As the cell divides, different daughter cells activate different genes. ' +
        'This makes them produce different combinations of organelles. ' +
        'Different organelle combinations → different structures → different functions. ' +
        'That is how ONE cell becomes eyes, heart, muscles, nerves, and skin.',
    },
  },

  // ── LESSON 8 ──────────────────────────────────────────────────────────────
  {
    number: 8,
    title: 'Levels of Organisation — From Cell to Organism',
      aresKeywords: 'levels organisation cell tissue organ organism biology',
    duration: '3 periods / 120 minutes',
    slo: {
      purpose: 'Students complete the unit by understanding how specialised cells form tissues, organs, and organ systems — giving the whole organism its capabilities.',
      knowledge:
        '• Define and give examples of: cell, tissue, organ, organ system, organism\n' +
        '• Give examples of tissues formed by specialised cells in plants (xylem tissue, phloem tissue, epidermis) and animals (blood, muscle tissue, nervous tissue)\n' +
        '• Give examples of organs (heart, leaf, stem, brain, stomach) and organ systems (circulatory, digestive, respiratory)\n' +
        '• Explain why organisation at multiple levels is necessary for large, complex organisms',
      skills:
        '• Construct a hierarchy diagram: cell → tissue → organ → organ system → organism\n' +
        '• Write a complete explanation of the anchoring phenomenon (salamander development) using all unit vocabulary\n' +
        '• Evaluate initial models against final models and articulate conceptual growth',
      attitudes:
        '• Appreciation for the elegant organisation of life at multiple scales\n' +
        '• Sense of achievement at completing a complex unit of learning\n' +
        '• Understanding that individual cells contributing to a larger whole is a metaphor for community',
      keyInquiry: 'How do specialised cells work together to form a living, functioning organism?',
      purposeInStoryline:
        'This lesson is the CAPSTONE. Students zoom out from the cell level to see how specialised cells ' +
        'create the larger-scale structures that make the salamander (and all organisms) functional. ' +
        'The unit ends with students writing a complete evidence-based explanation of the driving question — ' +
        'the Final Explanation assignment is introduced here.',
      safetyNotes: 'No practical in this lesson. Research, discussion, and writing activity.',
    },
    overview:
      'The lesson opens with a scale image sequence: cell → tissue → organ → organ system → whole organism. ' +
      'Students build a hierarchy diagram for both a plant (root hair cell → root epidermis tissue → root → ' +
      'root system → plant) and an animal (muscle cell → muscle tissue → heart → circulatory system → human). ' +
      'Groups then present their diagrams. The lesson closes with students writing their final explanation ' +
      'of the salamander phenomenon — connecting all 8 lessons of evidence into a coherent explanation.\n\n' +
      'The Final Explanation and Summary Table student documents are distributed, and the teacher ' +
      'explains the rubric. Students understand that their evidence from all 8 lessons should be ' +
      'referenced in their final explanation.',
    framework: [
      {
        phase: 'Predict Phase',
        learnerExperience:
          '"Look at your Lesson 7 model — specialised animal cells. ' +
          'Predict: if many nerve cells work together, what structure do they form? ' +
          'If many muscle cells work together? If many RBCs work together with plasma?" ' +
          'Students predict names and functions of these grouped structures.',
        resource:
          'PROMPT CARD: "Predict: many of these cells working together form a _____ with function _____"\n' +
          'TYPE: Structured prediction',
        teacherMoves:
          '"You know individual cells. Zoom out: what happens when thousands of identical specialised cells group together?"\n' +
          'WAIT TIME: 2 minutes.\n' +
          '"Share. What did you call these groupings?"',
        sensemakingStrategy:
          'Zoom-Out Prediction — students infer tissue/organ structure from cell knowledge.',
        formativeAssessment:
          'Do students already know the term "tissue"? What prior knowledge exists about organs?',
      },
      {
        phase: 'Observe Phase',
        learnerExperience:
          'SCALE SEQUENCE investigation: Students receive 5 images at different scales for one plant and one animal. ' +
          'They arrange them in order (cell → tissue → organ → organ system → organism) and label each level. ' +
          'Class builds two hierarchy diagrams on the board — one for plant, one for animal — using student contributions.',
        resource:
          'IMAGE SET: 5-image scale sequence for plant (root hair → root epidermis → root → root system → whole plant) ' +
          'and 5-image scale sequence for animal (muscle cell → muscle tissue → heart → circulatory system → human body)\n' +
          'TYPE: Image-sorting and hierarchy-building activity',
        teacherMoves:
          '"Arrange the images from smallest to largest. Label each level: cell, tissue, organ, organ system, organism."\n' +
          '"Now — what TISSUE is formed by xylem cells? By phloem cells? By root hair cells?" ' +
          'Build class hierarchy diagram collaboratively on the board.',
        sensemakingStrategy:
          'Hierarchical Organisation:\n' +
          'Students see that complexity at the organism level EMERGES from organisation at lower levels.',
        formativeAssessment:
          'Can students correctly order and label all 5 levels for both plant and animal?\n' +
          'Can they give a specific example at each level?',
      },
      {
        phase: 'Explain Phase',
        learnerExperience:
          'FINAL EXPLANATION WRITING: Students draft their complete explanation of the driving question: ' +
          '"How does a single cell become a complex, specialised organism?" ' +
          'Using: Summary Table (all 8 lessons), model portfolio, DQB answers. ' +
          'Explanation must include: cell division, differentiation, organelle combinations, specialisation, levels of organisation.',
        resource:
          'STUDENT DOCUMENTS: Final Explanation template + Summary Table (distribute today)\n' +
          'RUBRIC: Final Explanation rubric (20 points)\n' +
          'STUDENT REFERENCE: Own model portfolio, DQB, Summary Table entries\n' +
          'TYPE: Extended writing activity',
        teacherMoves:
          '"Now you have everything you need to answer the driving question. Use your Summary Table. Use your model. Reference specific lessons."\n' +
          '"Your explanation needs 5 parts: (1) cell division, (2) differentiation, (3) organelle combinations, (4) specialisation examples, (5) levels of organisation."\n' +
          'Allow 30 minutes for writing. Circulate and prompt struggling students.',
        sensemakingStrategy:
          'Synthesis Writing:\n' +
          'Writing forces integration of all prior learning. ' +
          'The structured 5-part template supports students while the content is entirely student-generated.',
        formativeAssessment:
          'Walk the room during writing. Check: Are students citing specific lesson evidence? ' +
          'Are they connecting to the phenomenon? ' +
          'Final Explanation is a summative assessment (using the 20-point rubric).',
      },
      {
        phase: 'Driving Question Board (DQB) Creation',
        learnerExperience:
          'FINAL DQB CELEBRATION: Every student writes one sentence on a card: ' +
          '"I can now answer the driving question. The answer is..." ' +
          'Cards are posted on the DQB. Teacher reads several aloud. ' +
          'Students reflect: "In Lesson 1, I could not answer this. Now I can. What evidence did I use?"',
        resource:
          'MATERIALS: Index cards, DQB poster\n' +
          'TYPE: Celebratory metacognitive reflection',
        teacherMoves:
          '"This is the moment. Write your one-sentence answer to the driving question."\n' +
          'Read 4–5 cards aloud. Ask: "What evidence from the unit supports this?"\n' +
          '"From the salamander Lesson 1 to today — you have built this understanding together. That is science."',
        sensemakingStrategy:
          'DQB Culmination — the DQB has been the thread through the entire unit. ' +
          'Closing it intentionally gives students a sense of closure and accomplishment.',
        formativeAssessment:
          'Quality of one-sentence driving question answers reveals whether students can articulate the full explanation.',
      },
      {
        phase: 'Model Building Phase',
        learnerExperience:
          'FINAL MODEL PORTFOLIO ENTRY: Students draw their FINAL model — a complete, labelled diagram showing: ' +
          '(1) a generalised cell with organelles, (2) arrow to specialised cell types, (3) arrow to tissue, ' +
          '(4) arrow to organ, (5) arrow to organism. ' +
          'They compare Final Model to Lesson 1 Initial Model: ' +
          '"Write a reflection: What did you think before? What do you know now? What changed and why?"',
        resource:
          'MATERIALS: Student model portfolio, blank A4 paper, coloured pencils\n' +
          'TYPE: Capstone portfolio entry',
        teacherMoves:
          '"Your final model should show the full journey: from one cell to a whole organism."\n' +
          '"Place your Lesson 1 and Lesson 8 models side by side. Write your reflection on the back of the Lesson 8 model."\n' +
          '"This portfolio is yours. You built this understanding through 8 lessons of investigation."',
        sensemakingStrategy:
          'Portfolio Reflection — most powerful capstone activity: explicit comparison of beginning and ending understanding.',
        formativeAssessment:
          'Final model completeness: Does it show the full hierarchy (cell → organism) with specialisation?\n' +
          'Reflection quality: Does it show genuine understanding of how their thinking changed?',
      },
    ],
    teacherReflection:
      'After teaching this lesson, reflect on:\n\n' +
      '1. Could students accurately construct the cell → tissue → organ → organ system → organism hierarchy for both plants and animals?\n\n' +
      '2. How strong were the Final Explanation drafts? Did students reference evidence from all 8 lessons or only recent ones?\n\n' +
      '3. Was the DQB celebration effective? Did students express a genuine sense of achievement?\n\n' +
      '4. How significantly did the Lesson 8 final models differ from the Lesson 1 initial models? What does this difference reveal?\n\n' +
      '5. Were the Final Explanation templates and rubric clear to students? Any confusion about expectations?\n\n' +
      '6. Looking across the whole unit: what worked best? What would you restructure?',
    summaryTablePrompt: {
      observed:
        'Arranged scale image sequences for plants and animals: cell → tissue → organ → organ system → organism. ' +
        'Built class hierarchy diagrams for root (root hair cell → epidermis → root → root system → plant) ' +
        'and heart (muscle cell → cardiac muscle tissue → heart → circulatory system → human). ' +
        'Drafted Final Explanation of the driving question. ' +
        'DQB final celebration — wrote one-sentence answers to the driving question.',
      learned:
        'Specialised cells group into TISSUES (e.g., muscle tissue, nervous tissue, xylem tissue). ' +
        'Tissues combine into ORGANS (e.g., heart, leaf, brain). ' +
        'Organs work together in ORGAN SYSTEMS (e.g., circulatory, digestive, root system). ' +
        'This hierarchy is why organisms can be large and complex.',
      explained:
        'COMPLETE EXPLANATION: The salamander starts as ONE fertilised egg. ' +
        'It divides (mitosis) → many identical cells. ' +
        'Different genes are activated in different cells (differentiation). ' +
        'Each cell type makes specific organelle combinations → different structures → different functions. ' +
        'Specialised cells group into tissues → organs → organ systems → the whole salamander organism. ' +
        'ONE cell. BILLIONS of specialised descendants. All organised. All connected. That is life.',
    },
  },

]; // end LESSONS array

// ─── SoW Document Builder ────────────────────────────────────────────────────

async function buildSoW() {
  const title = 'BIOLOGY GRADE 10: CELL STRUCTURE AND SPECIALISATION';
  const subtitle = 'CBE Phenomenon-Driven Lesson Sequence — Sub-Strand 1.3 (8 Lessons)';

  const body = [
    ...titleBlock(title, subtitle),
    SPACE(),
    subStrandOverview(UNIT),
    SPACE(),
  ];

  for (const lesson of LESSONS) {
    body.push(
      SPACE(),
      sectionA(lesson),
      SPACE(),
      sectionB(lesson),
      SPACE(),
      sectionC(lesson),
      SPACE(),
      sectionD(lesson),
      SPACE(),
      sectionE(lesson),
      SPACE(),
    );
  }

  body.push(SPACE(), differentiationTable());

  const doc = new Document({
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

  return doc;
}

// ─── Final Explanation Document ───────────────────────────────────────────────

async function buildFinalExplanation() {
  const FLW = 3000;          // label column width
  const FCW = W - FLW;      // content column width
  const RW3 = Math.floor((W - FLW) / 3);  // 3-way split for rubric
  const RW3r = W - FLW - RW3 * 2;         // remainder to avoid rounding gap

  const rows_instr = [
    fullHeader('FINAL EXPLANATION: CELL STRUCTURE AND SPECIALISATION', C.darkBlue, 'FFFFFF', SZ_H, 2),
    fullHeader('Biology Grade 10 — Demonstrating Complete Understanding', C.teal, 'FFFFFF', SZ_H, 2),
    labelRow('Student Name', '_______________________________________________', FLW),
    labelRow('Class',        '_______________________________________________', FLW),
    labelRow('Date',         '_______________________________________________', FLW),
  ];

  const rows_inst = [
    fullHeader('INSTRUCTIONS FOR STUDENTS', C.teal, 'FFFFFF', SZ_H, 1),
    new TableRow({ children: [cell(
      'Now that you have completed all 8 lessons of the Cell Structure and Specialisation unit, ' +
      'it is time to write your COMPLETE EXPLANATION of the salamander phenomenon.\n\n' +
      'WHAT TO USE:\n' +
      '• Your Summary Table (all 8 lessons)\n' +
      '• Your model portfolio (Lessons 1–8)\n' +
      '• Your DQB answers\n' +
      '• Your notes and drawings from all lessons\n\n' +
      'YOUR EXPLANATION SHOULD INCLUDE:\n' +
      '• What is a cell and why are cells the basic unit of life\n' +
      '• The difference between light and electron microscopes and what each reveals\n' +
      '• The structures and functions of major organelles in plant and animal cells\n' +
      '• How plant and animal cells differ (and why)\n' +
      '• Examples of specialised cells in plants and animals (at least 4 examples with structural adaptations)\n' +
      '• The levels of organisation: cell → tissue → organ → organ system → organism\n' +
      '• How ONE fertilised egg produces billions of different specialised cells (differentiation)\n\n' +
      'LENGTH: Aim for at least 4–5 pages (handwritten) or 3–4 pages typed.\n\n' +
      'GRADING: This explanation is assessed using the Final Explanation Rubric (20 points total):\n' +
      '• Cell structure and organelle knowledge (4 points)\n' +
      '• Specialised cells — structure and function evidence (4 points)\n' +
      '• Levels of organisation explanation (4 points)\n' +
      '• Phenomenon explanation using all unit evidence (4 points)\n' +
      '• Scientific reasoning and vocabulary (4 points)',
      { fill: C.white, w: W, size: SZ }
    )]}),
  ];

  const parts = [
    { title: 'PART 1: THE CELL — Basic Unit of Life',
      prompts: 'Explain: What is a cell? What is cell theory (3 points)? Why are cells the basic unit of life?\nEvidence to include: From Lesson 1 (cell theory introduction).\nWrite your explanation:' },
    { title: 'PART 2: MICROSCOPY — Tools for Studying Cells',
      prompts: 'Explain: What is a light microscope? What is an electron microscope? How do they differ? Why is the EM needed to study organelles?\nEvidence to include: From Lesson 2 (microscope comparison); Lesson 3 (temporary slide observations).' },
    { title: 'PART 3: CELL STRUCTURE — Organelles and Their Functions',
      prompts: 'Explain: Name and describe the function of each major organelle in plant and animal cells. Describe the secretory pathway.\nEvidence to include: From Lesson 4 (EM image analysis, jigsaw activity); Lesson 5 (plant vs animal comparison).' },
    { title: 'PART 4: PLANT vs ANIMAL CELLS — Key Differences',
      prompts: 'Explain: What structures are unique to plant cells? What structures are unique to animal cells? WHY are these differences there?\nEvidence to include: From Lesson 5 (comparison table, structure-function analysis).' },
    { title: 'PART 5: SPECIALISED PLANT CELLS',
      prompts: 'For EACH of these plant cell types, describe: (1) their structure/adaptations, and (2) their function.\nCells to include: root hair cell, guard cell, xylem vessel, phloem sieve tube.\nEvidence to include: From Lesson 6.' },
    { title: 'PART 6: SPECIALISED ANIMAL CELLS',
      prompts: 'For EACH of these animal cell types, describe: (1) their structure/adaptations, and (2) their function.\nCells to include: red blood cell, sperm cell, neurone, muscle fibre, egg cell.\nEvidence to include: From Lesson 7.' },
    { title: 'PART 7: LEVELS OF ORGANISATION',
      prompts: 'Explain: What are the five levels of biological organisation? Give one example at each level for a PLANT and one for an ANIMAL.\nEvidence to include: From Lesson 8 (hierarchy diagrams).' },
    { title: 'PART 8: EXPLAINING THE PHENOMENON — The Salamander',
      prompts: 'Use ALL of your evidence from this unit to explain:\n"How does a single fertilised cell become a complex, specialised organism?"\nYour explanation MUST include: cell division, differentiation, organelle combinations, specialisation, and levels of organisation.\nEvidence to include: From ALL 8 lessons.' },
  ];

  const rows_rubric = [
    fullHeader('FINAL EXPLANATION RUBRIC (20 points)', C.darkBlue, 'FFFFFF', SZ_H, 4),
    new TableRow({ children: [
      cell('Criterion', { fill: C.medBlue, bold: true, color: 'FFFFFF', w: FLW, size: SZ }),
      cell('Excellent (4)', { fill: C.medBlue, bold: true, color: 'FFFFFF', w: RW3, size: SZ }),
      cell('Proficient (3)', { fill: C.teal, bold: true, color: 'FFFFFF', w: RW3, size: SZ }),
      cell('Developing (1–2)', { fill: C.medBlue, bold: true, color: 'FFFFFF', w: RW3r, size: SZ }),
    ]}),
    new TableRow({ children: [
      cell('Cell Structure & Organelles', { fill: C.lightBlue, w: FLW, size: SZ }),
      cell('Names and accurately describes the function of 8+ organelles with correct structure-function links.', { fill: C.white, w: RW3, size: SZ }),
      cell('Names and describes 5–7 organelles correctly.', { fill: C.grey, w: RW3, size: SZ }),
      cell('Names fewer than 5 organelles or has significant function errors.', { fill: C.white, w: RW3r, size: SZ }),
    ]}),
    new TableRow({ children: [
      cell('Specialised Cells Evidence', { fill: C.lightBlue, w: FLW, size: SZ }),
      cell('Describes structural adaptations AND functions for 4+ plant AND 4+ animal specialised cells with clear evidence.', { fill: C.white, w: RW3, size: SZ }),
      cell('Describes 2–3 cell types from each kingdom with correct adaptations.', { fill: C.grey, w: RW3, size: SZ }),
      cell('Describes only 1 cell type or has significant errors in adaptations.', { fill: C.white, w: RW3r, size: SZ }),
    ]}),
    new TableRow({ children: [
      cell('Levels of Organisation', { fill: C.lightBlue, w: FLW, size: SZ }),
      cell('Correctly names all 5 levels with accurate examples for both plant and animal. Explains why levels are necessary.', { fill: C.white, w: RW3, size: SZ }),
      cell('Names 4 levels correctly with examples. Some errors or gaps.', { fill: C.grey, w: RW3, size: SZ }),
      cell('Names fewer than 4 levels or examples are inaccurate.', { fill: C.white, w: RW3r, size: SZ }),
    ]}),
    new TableRow({ children: [
      cell('Phenomenon Explanation', { fill: C.lightBlue, w: FLW, size: SZ }),
      cell('Fully explains the salamander phenomenon using evidence from all 8 lessons: division, differentiation, specialisation, organisation.', { fill: C.white, w: RW3, size: SZ }),
      cell('Explains most of the phenomenon using evidence from 5+ lessons.', { fill: C.grey, w: RW3, size: SZ }),
      cell('Partial explanation, limited evidence cited.', { fill: C.white, w: RW3r, size: SZ }),
    ]}),
    new TableRow({ children: [
      cell('Scientific Reasoning', { fill: C.lightBlue, w: FLW, size: SZ }),
      cell('Uses accurate scientific vocabulary throughout; reasoning is logical and evidence-based; well-structured explanation.', { fill: C.white, w: RW3, size: SZ }),
      cell('Uses some scientific vocabulary; mostly logical reasoning; some structural issues.', { fill: C.grey, w: RW3, size: SZ }),
      cell('Limited scientific vocabulary; reasoning is unclear or not evidence-based.', { fill: C.white, w: RW3r, size: SZ }),
    ]}),
  ];

  const body = [
    ...titleBlock('FINAL EXPLANATION: CELL STRUCTURE AND SPECIALISATION', 'Biology Grade 10 — Student Assessment Document'),
    SPACE(),
    makeTable(rows_instr, [FLW, FCW]),
    SPACE(),
    makeTable(rows_inst, [W]),
    SPACE(),
    ...parts.flatMap((p, i) => [
      makeTable([
        fullHeader(p.title, C.medBlue, 'FFFFFF', SZ_H, 1),
        new TableRow({ children: [cell(p.prompts, { fill: C.lightBlue, w: W, size: SZ, italic: true })] }),
        new TableRow({ children: [cell('\n\n\n\n\n\n', { fill: C.white, w: W, size: SZ })] }),
      ], [W]),
      SPACE(),
    ]),
    makeTable(rows_rubric, [FLW, RW3, RW3, RW3r]),
  ];

  const doc = new Document({
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

  return doc;
}

// ─── Summary Table Document ───────────────────────────────────────────────────

async function buildSummaryTable() {
  const SLW = 3000;           // label col width for header table
  const SCW = W - SLW;       // content col width
  const TLW = 2400;           // lesson col width for main table
  const TC3 = Math.floor((W - TLW) / 3);   // each of the 3 content cols
  const TC3r = W - TLW - TC3 * 2;          // remainder

  const headerRows = [
    fullHeader('SUMMARY TABLE: CELL STRUCTURE AND SPECIALISATION', C.darkBlue, 'FFFFFF', SZ_H, 2),
    fullHeader('Biology Grade 10 — Student Learning Portfolio', C.teal, 'FFFFFF', SZ_H, 2),
    labelRow('Student Name', '_______________________________________________', SLW),
    labelRow('Class',        '_______________________________________________', SLW),
    labelRow('Date Started', '_______________________________________________', SLW),
    labelRow('Date Completed', '_____________________________________________', SLW),
  ];

  const instrRows = [
    fullHeader('INSTRUCTIONS', C.teal, 'FFFFFF', SZ_H, 1),
    new TableRow({ children: [cell(
      'FOR STUDENTS:\n' +
      'This Summary Table is YOUR learning journal for the Cell Structure and Specialisation unit. ' +
      'After EACH lesson, take 5 minutes to complete the row for that lesson. This will help you:\n' +
      '• Track what you are learning\n' +
      '• See how your understanding grows across all 8 lessons\n' +
      '• Prepare for your Final Explanation\n' +
      '• Study for assessments\n\n' +
      'IMPORTANT: When you work on the Driving Questions Board (DQB) or revise your cell model, ' +
      'make a note in the "What did I observe?" column!\n\n' +
      'FOR TEACHERS:\n' +
      'Provide this template at the beginning of the unit. After each lesson, allocate 5 minutes ' +
      'for students to complete their row. Review tables after Lessons 4 and 8 to monitor understanding.',
      { fill: C.white, w: W, size: SZ }
    )]}),
  ];

  const tableHeaderRow = new TableRow({ children: [
    cell('Lesson / Activity', { fill: C.darkBlue, bold: true, color: 'FFFFFF', w: TLW, size: SZ }),
    cell('What did I observe?', { fill: C.medBlue, bold: true, color: 'FFFFFF', w: TC3, size: SZ }),
    cell('What did I learn?',   { fill: C.teal,    bold: true, color: 'FFFFFF', w: TC3, size: SZ }),
    cell('How does this explain the phenomenon?', { fill: C.medBlue, bold: true, color: 'FFFFFF', w: TC3r, size: SZ }),
  ]});

  const lessonRows = LESSONS.map(l => new TableRow({ children: [
    cell(`Lesson ${l.number}: ${l.title}`, { fill: C.lightBlue, bold: true, w: TLW, size: SZ }),
    cell(l.summaryTablePrompt.observed,    { fill: C.white, w: TC3,  size: SZ }),
    cell(l.summaryTablePrompt.learned,     { fill: C.grey,  w: TC3,  size: SZ }),
    cell(l.summaryTablePrompt.explained,   { fill: C.white, w: TC3r, size: SZ }),
  ]}));

  const exampleRow = new TableRow({ children: [
    cell('EXAMPLE: Lesson 1\n(Salamander Phenomenon)', { fill: C.lightPurple, bold: true, w: TLW, size: SZ }),
    cell(
      'Watched salamander grow from ONE cell into a complex organism (time-lapse). ' +
      'DQB Started. Initial cell model drawn.',
      { fill: C.white, w: TC3, size: SZ }),
    cell(
      'All living things are made of cells (cell theory). ' +
      'The cell is the basic unit of life. ' +
      'Cells come from pre-existing cells.',
      { fill: C.grey, w: TC3, size: SZ }),
    cell(
      'The salamander started as ONE cell. But HOW does one cell become many DIFFERENT cells? ' +
      'Still need to figure out!',
      { fill: C.white, w: TC3r, size: SZ }),
  ]});

  const reflectionRows = [
    fullHeader('END-OF-UNIT REFLECTION QUESTIONS (complete after Lesson 8)', C.orange, 'FFFFFF', SZ_H, 1),
    new TableRow({ children: [cell(
      '1. What was the most surprising thing you learned in this unit?\n\n\n\n' +
      '2. How did your model of a cell change from Lesson 1 to Lesson 8? What is the most important thing you added?\n\n\n\n' +
      '3. Choose ONE specialised cell. Explain how its structure makes it perfectly suited for its function.\n\n\n\n' +
      '4. In your own words, explain how a single fertilised egg cell (like the salamander egg) becomes a complex organism with many different cell types.\n\n\n\n' +
      '5. Which lesson gave you the most evidence? How did it help you explain the phenomenon?\n\n\n\n' +
      '6. What question do you still have about cells — something you are still curious about after this unit?',
      { fill: C.lightOrange, w: W, size: SZ }
    )]}),
  ];

  const teacherRows = [
    fullHeader('TEACHER NOTES (not for student distribution)', C.darkBlue, 'FFFFFF', SZ_H, 1),
    new TableRow({ children: [cell(
      'Use this section to record observations about student Summary Table quality:\n\n' +
      '• After Lesson 4 review: Which students have rich observations? Which need more support?\n\n' +
      '• After Lesson 7 review: Are students connecting evidence to the phenomenon?\n\n' +
      '• Before Final Explanation: Are all students\' Summary Tables complete enough to support the writing task?\n\n' +
      'Common issues: Students write "I learned about cells" without specifics — prompt them to name specific organelles/cells.\n' +
      'The "How does this explain the phenomenon?" column is hardest — model good answers explicitly in class after Lessons 2 and 4.',
      { fill: C.lightBlue, w: W, size: SZ }
    )]}),
  ];

  const body = [
    ...titleBlock('SUMMARY TABLE: CELL STRUCTURE AND SPECIALISATION', 'Biology Grade 10 — Student Learning Portfolio'),
    SPACE(),
    makeTable(headerRows, [SLW, SCW]),
    SPACE(),
    makeTable(instrRows, [W]),
    SPACE(),
    makeTable([tableHeaderRow, exampleRow, ...lessonRows], [TLW, TC3, TC3, TC3r]),
    SPACE(),
    makeTable(reflectionRows, [W]),
    SPACE(),
    makeTable(teacherRows, [W]),
  ];

  const doc = new Document({
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

  return doc;
}

// ─── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  console.log('Generating Biology 1.3 Cell Structure documents...\n');

  console.log('1/3 Building SoW...');
  const sow = await buildSoW();
  const sowBuf = await Packer.toBuffer(sow);
  const sowPath = path.join(OUT, 'Biology_CellStructure_CBE_LessonSequence.docx');
  fs.writeFileSync(sowPath, sowBuf);
  console.log(`    Saved: ${sowPath}  (${(sowBuf.length / 1024).toFixed(0)} KB)\n`);

  console.log('2/3 Building Final Explanation...');
  const fe = await buildFinalExplanation();
  const feBuf = await Packer.toBuffer(fe);
  const fePath = path.join(OUT, 'Biology_CellStructure_FinalExplanation.docx');
  fs.writeFileSync(fePath, feBuf);
  console.log(`    Saved: ${fePath}  (${(feBuf.length / 1024).toFixed(0)} KB)\n`);

  console.log('3/3 Building Summary Table...');
  const st = await buildSummaryTable();
  const stBuf = await Packer.toBuffer(st);
  const stPath = path.join(OUT, 'Biology_CellStructure_SummaryTable.docx');
  fs.writeFileSync(stPath, stBuf);
  console.log(`    Saved: ${stPath}  (${(stBuf.length / 1024).toFixed(0)} KB)\n`);

  console.log('Done! All 3 documents generated successfully.');
  console.log('\nFiles:');
  console.log(`  ${sowPath}`);
  console.log(`  ${fePath}`);
  console.log(`  ${stPath}`);
}

main().catch(err => {
  console.error('Generator failed:', err.message);
  process.exit(1);
});
