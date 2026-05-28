// Generator 1 of 3: the main Lesson Sequence document.
// Produces: Biology_GaseousExchangePlants_CBE_LessonSequence_L1-6.docx

const fs = require("fs");
const path = require("path");
const H = require("./_helpers.js");
const data = require("./biology_2_3_data.js");
const {
  docx, C, PHASE_COLOURS, CONTENT_WIDTH_DXA,
  run, para, bulletPara, emptyPara, cell,
  sectionHeaderRow, lessonHeaderParagraph, labelContentRow,
} = H;
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, AlignmentType, HeadingLevel, ShadingType,
} = docx;

// ============================================================
// SECTION 1: TITLE BLOCK
// ============================================================
function buildTitleBlock() {
  return [
    new Paragraph({
      children: [run(
        `${data.meta.subject.toUpperCase()} ${data.meta.grade.toUpperCase()}: GASEOUS EXCHANGE AND RESPIRATION (PLANTS)`,
        { bold: true, size: H.TITLE_SIZE, color: C.darkBlue }
      )],
      alignment: AlignmentType.LEFT,
      spacing: { before: 0, after: 120 },
    }),
    new Paragraph({
      children: [run(
        `CBE Phenomenon-Driven Lesson Sequence — Sub-Strand 2.3 (${data.meta.lessonsInThisBundle} of ${data.meta.totalLessonsInSubStrand} Lessons — Test Bundle)`,
        { italic: true, size: H.SUBTITLE_SIZE, color: C.teal }
      )],
      alignment: AlignmentType.LEFT,
      spacing: { before: 0, after: 240 },
    }),
    new Paragraph({
      children: [run(data.meta.testBundleNote,
        { italic: true, size: H.BODY_SIZE, color: "707070" })],
      alignment: AlignmentType.LEFT,
      spacing: { before: 0, after: 360 },
    }),
  ];
}

// ============================================================
// SECTION 2: SUB-STRAND OVERVIEW TABLE (17 rows)
// ============================================================
function buildSubStrandOverview() {
  const ov = data.overview;
  const m = data.meta;

  const rows = [
    // Header row
    new TableRow({
      children: [
        new TableCell({
          children: [new Paragraph({
            children: [run("SUB-STRAND OVERVIEW",
              { bold: true, color: C.white, size: 22 })],
            alignment: AlignmentType.LEFT,
            spacing: { before: 40, after: 40 },
          })],
          width: { size: CONTENT_WIDTH_DXA, type: WidthType.DXA },
          margins: { top: 80, bottom: 80, left: 120, right: 120 },
          borders: H.allBorders(),
          shading: { type: ShadingType.CLEAR, color: "auto", fill: C.darkBlue },
          columnSpan: 2,
        }),
      ],
    }),

    labelContentRow("Grade Level", m.grade),
    labelContentRow("Subject", m.subject),
    labelContentRow("Strand", m.strand),
    labelContentRow("Sub-Strand", m.subStrand),
    labelContentRow("Total Duration",
      `${m.totalLessonsInSubStrand} lessons × ${m.minutesPerLesson} minutes = ${m.totalLessonsInSubStrand * m.minutesPerLesson} minutes total`),
    labelContentRow("Sub-Strand Content", ov.subStrandContent, { contentBullets: true }),
    labelContentRow("Learning Outcomes",
      ["By the end of the sub-strand, the learner should be able to:", ...ov.learningOutcomes]),
    labelContentRow("Core Competencies", ov.coreCompetencies, { contentBullets: true }),
    labelContentRow("Core Values", ov.coreValues, { contentBullets: true, labelFill: C.lightGreen }),
    labelContentRow("Pertinent & Contemporary Issues (PCIs)", ov.pcis, { contentBullets: true, labelFill: C.lightOrange }),

    // PROVISIONAL rows
    labelContentRow("Science and Engineering Practices",
      ov.sciencePractices, { contentBullets: true, labelFill: C.lightTeal }),
    labelContentRow("Career Connections",
      ov.careerConnections, { contentBullets: true, labelFill: C.lightTeal }),
    labelContentRow("Focus for Lessons",
      ov.focusForLessons, { labelFill: C.lightTeal }),

    labelContentRow("Key Inquiry Questions",
      ov.keyInquiryQuestions, { contentBullets: true, labelFill: C.lightPurple }),
    labelContentRow("Anchoring Phenomenon",
      ov.anchoringPhenomenon, { labelFill: C.lightPurple }),
    labelContentRow("Driving Question",
      ov.drivingQuestion, { labelFill: C.lightPurple }),
    labelContentRow("Storyline Thread",
      ov.storylineThread, { labelFill: C.lightTeal }),
  ];

  return new Table({
    rows,
    width: { size: CONTENT_WIDTH_DXA, type: WidthType.DXA },
    columnWidths: [3200, CONTENT_WIDTH_DXA - 3200],
    borders: H.tableBorders(),
  });
}

// ============================================================
// SECTION 3: PER-LESSON TABLES
// ============================================================

// Section A: Specific Learning Outcomes (7 rows)
function buildSectionA(lesson) {
  const a = lesson.sectionA;
  const rows = [
    sectionHeaderRow("A. SPECIFIC LEARNING OUTCOMES", C.darkBlue),
    labelContentRow("Purpose", a.purpose),
    labelContentRow("Knowledge", a.knowledge, { contentBullets: true }),
    labelContentRow("Skills", a.skills, { contentBullets: true }),
    labelContentRow("Attitudes", a.attitudes, { contentBullets: true }),
    labelContentRow("Key Inquiry Question", a.keyInquiryQuestion, { labelFill: C.lightPurple }),
    labelContentRow("Purpose in Storyline", a.purposeInStoryline, { labelFill: C.lightTeal }),
    labelContentRow("Safety Notes", a.safetyNotes, { labelFill: C.lightOrange }),
  ];
  return new Table({
    rows,
    width: { size: CONTENT_WIDTH_DXA, type: WidthType.DXA },
    columnWidths: [3200, CONTENT_WIDTH_DXA - 3200],
    borders: H.tableBorders(),
  });
}

// Section B: Lesson Overview (single-cell prose, with coloured header)
function buildSectionB(lesson) {
  const rows = [
    sectionHeaderRow("B. LESSON OVERVIEW", C.teal),
    new TableRow({
      children: [
        cell({
          width: CONTENT_WIDTH_DXA,
          text: lesson.sectionB,
        }),
      ],
    }),
  ];
  return new Table({
    rows,
    width: { size: CONTENT_WIDTH_DXA, type: WidthType.DXA },
    columnWidths: [CONTENT_WIDTH_DXA],
    borders: H.tableBorders(),
  });
}

// Section C: Lesson Implementation Framework (6-column table)
function buildSectionC(lesson) {
  // Column widths summing to 9360
  // Phase column = 1100, then 5 equal data columns of 1652
  const phaseW = 1100;
  const dataW = Math.floor((CONTENT_WIDTH_DXA - phaseW) / 5);  // 1652
  const lastDataW = CONTENT_WIDTH_DXA - phaseW - (dataW * 4);  // 1652 (handles rounding)
  const columnWidths = [phaseW, dataW, dataW, dataW, dataW, lastDataW];

  // Header row of column titles
  const headerRow = new TableRow({
    tableHeader: true,
    children: [
      cell({ width: phaseW, fill: C.darkBlue, text: "Phase",
             bold: true, color: C.white, size: 18 }),
      cell({ width: dataW, fill: C.medBlue, text: "Learner Experience",
             bold: true, color: C.white, size: 18 }),
      cell({ width: dataW, fill: C.teal, text: "Resource",
             bold: true, color: C.white, size: 18 }),
      cell({ width: dataW, fill: C.medBlue, text: "Teacher Actions",
             bold: true, color: C.white, size: 18 }),
      cell({ width: dataW, fill: C.teal, text: "Sensemaking Strategy",
             bold: true, color: C.white, size: 18 }),
      cell({ width: lastDataW, fill: C.darkBlue, text: "Assessment Strategy",
             bold: true, color: C.white, size: 18 }),
    ],
  });

  // One row per phase
  const phaseRows = lesson.sectionC.map((phase, idx) => {
    const phaseFill = PHASE_COLOURS[phase.phase] || C.lightBlue;
    const altFill = idx % 2 === 0 ? C.white : C.grey;
    return new TableRow({
      children: [
        cell({ width: phaseW, fill: phaseFill, text: phase.phase, bold: true }),
        cell({ width: dataW, fill: altFill, text: phase.learner }),
        cell({ width: dataW, fill: C.white, text: phase.resource }),
        cell({ width: dataW, fill: altFill, text: phase.teacher }),
        cell({ width: dataW, fill: C.white, text: phase.sensemaking }),
        cell({ width: lastDataW, fill: altFill, text: phase.assessment }),
      ],
    });
  });

  return [
    // Section header (separate full-width table for the header bar)
    new Table({
      rows: [sectionHeaderRow("C. LESSON IMPLEMENTATION FRAMEWORK", C.teal)],
      width: { size: CONTENT_WIDTH_DXA, type: WidthType.DXA },
      columnWidths: [CONTENT_WIDTH_DXA],
      borders: H.tableBorders(),
    }),
    // The 6-column body
    new Table({
      rows: [headerRow, ...phaseRows],
      width: { size: CONTENT_WIDTH_DXA, type: WidthType.DXA },
      columnWidths: columnWidths,
      borders: H.tableBorders(),
    }),
  ];
}

// Section D: Teacher Reflection (single-cell prose)
function buildSectionD(lesson) {
  const rows = [
    sectionHeaderRow("D. TEACHER REFLECTION", C.orange),
    new TableRow({
      children: [
        cell({
          width: CONTENT_WIDTH_DXA,
          text: lesson.sectionD,
        }),
      ],
    }),
  ];
  return new Table({
    rows,
    width: { size: CONTENT_WIDTH_DXA, type: WidthType.DXA },
    columnWidths: [CONTENT_WIDTH_DXA],
    borders: H.tableBorders(),
  });
}

// Section E: Summary Table Prompt (3 rows)
function buildSectionE(lesson) {
  const e = lesson.sectionE;
  const rows = [
    sectionHeaderRow("E. SUMMARY TABLE PROMPT (pre-filled example for this lesson)", C.purple),
    labelContentRow("What did I observe?", e.observe, { labelFill: C.lightPurple, labelWidth: 3200 }),
    labelContentRow("What did I learn?", e.learn, { labelFill: C.lightPurple, labelWidth: 3200 }),
    labelContentRow("How does this explain the phenomenon?", e.explain, { labelFill: C.lightPurple, labelWidth: 3200 }),
  ];
  return new Table({
    rows,
    width: { size: CONTENT_WIDTH_DXA, type: WidthType.DXA },
    columnWidths: [3200, CONTENT_WIDTH_DXA - 3200],
    borders: H.tableBorders(),
  });
}

// One full lesson = header + 5 sections
function buildLesson(lesson, isFirstLesson = false) {
  const elements = [];
  // Page break before every lesson EXCEPT the first - the first lesson
  // follows naturally from the sub-strand overview.
  elements.push(lessonHeaderParagraph(
    lesson.number, lesson.title, data.meta.minutesPerLesson,
    { pageBreakBefore: !isFirstLesson }
  ));
  elements.push(buildSectionA(lesson));
  elements.push(emptyPara());
  elements.push(buildSectionB(lesson));
  elements.push(emptyPara());
  // Section C returns an array of two tables (header + 6-col body)
  const sectionC = buildSectionC(lesson);
  for (const t of sectionC) {
    elements.push(t);
  }
  elements.push(emptyPara());
  elements.push(buildSectionD(lesson));
  elements.push(emptyPara());
  elements.push(buildSectionE(lesson));
  return elements;
}

// ============================================================
// SECTION 4: DIFFERENTIATION AND INCLUSION TABLE
// ============================================================
function buildDifferentiationTable() {
  const colW = Math.floor(CONTENT_WIDTH_DXA / 3);
  const lastColW = CONTENT_WIDTH_DXA - (colW * 2);

  const headerRow = new TableRow({
    tableHeader: true,
    children: [
      cell({ width: colW, fill: C.darkBlue, text: "Learner Need",
             bold: true, color: C.white, size: 18 }),
      cell({ width: colW, fill: C.darkBlue, text: "Support Strategies",
             bold: true, color: C.white, size: 18 }),
      cell({ width: lastColW, fill: C.darkBlue, text: "Extension Strategies",
             bold: true, color: C.white, size: 18 }),
    ],
  });

  const dataRows = data.differentiation.map((row, idx) => {
    const altFill = idx % 2 === 0 ? C.white : C.grey;
    return new TableRow({
      children: [
        cell({ width: colW, fill: C.lightTeal, text: row.need, bold: true }),
        cell({ width: colW, fill: altFill, text: row.support }),
        cell({ width: lastColW, fill: altFill, text: row.extension }),
      ],
    });
  });

  return [
    // Header bar
    new Table({
      rows: [sectionHeaderRow("DIFFERENTIATION AND INCLUSION", C.darkBlue)],
      width: { size: CONTENT_WIDTH_DXA, type: WidthType.DXA },
      columnWidths: [CONTENT_WIDTH_DXA],
      borders: H.tableBorders(),
    }),
    // Body
    new Table({
      rows: [headerRow, ...dataRows],
      width: { size: CONTENT_WIDTH_DXA, type: WidthType.DXA },
      columnWidths: [colW, colW, lastColW],
      borders: H.tableBorders(),
    }),
  ];
}

// ============================================================
// MAIN
// ============================================================
function buildDocument() {
  const children = [];

  // Title block
  for (const p of buildTitleBlock()) children.push(p);

  // Sub-strand overview
  children.push(buildSubStrandOverview());
  children.push(emptyPara());

  // Lessons 1-6 (page break before each lesson except the first)
  for (let i = 0; i < data.lessons.length; i++) {
    for (const e of buildLesson(data.lessons[i], i === 0)) {
      children.push(e);
    }
  }
  children.push(emptyPara());

  // Differentiation
  for (const t of buildDifferentiationTable()) {
    children.push(t);
  }

  // Footer note re: provisional elements + Real Life Application
  children.push(emptyPara());
  children.push(new Paragraph({
    children: [run(
      "Note on this test bundle: This document contains Lessons 1-6 of a 22-lesson sub-strand. " +
      "Provisional sections (Career Connections, Focus for Lessons, Science and Engineering Practices in the " +
      "Sub-Strand Overview, and the Differentiation and Inclusion table at the end) are included pending teacher " +
      "consultant confirmation. The Real Life Application mini-table belongs in the final lesson of the full " +
      "sub-strand and is therefore not included in this 6-lesson bundle.",
      { italic: true, size: H.BODY_SIZE, color: "707070" }
    )],
    alignment: AlignmentType.LEFT,
    spacing: { before: 240, after: 240 },
  }));

  return new Document({
    creator: "CBE Generation System",
    title: "Biology Grade 10 Sub-Strand 2.3 Lesson Sequence (L1-6 test bundle)",
    styles: {
      default: {
        document: {
          run: { font: H.FONT, size: H.BODY_SIZE },
        },
      },
    },
    sections: [{
      properties: {
        page: {
          size: { width: 15840, height: 12240 },        // US Letter LANDSCAPE in DXA
          margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 },
        },
      },
      children: children,
    }],
  });
}

async function main() {
  const doc = buildDocument();
  const buffer = await Packer.toBuffer(doc);
  const outPath = path.join(__dirname, "..", "output",
    "Biology_GaseousExchangePlants_CBE_LessonSequence_L1-6.docx");
  fs.writeFileSync(outPath, buffer);
  console.log("Wrote:", outPath, "(" + buffer.length + " bytes)");
}

main().catch(err => {
  console.error("ERROR:", err);
  process.exit(1);
});
