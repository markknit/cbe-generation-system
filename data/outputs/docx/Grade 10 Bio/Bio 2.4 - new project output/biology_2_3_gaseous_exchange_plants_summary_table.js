// Generator 3 of 3: Summary Table teacher-reference document.
// Produces: Biology_GaseousExchangePlants_SummaryTable.docx

const fs = require("fs");
const path = require("path");
const H = require("./_helpers.js");
const data = require("./biology_2_3_data.js");
const {
  docx, C, CONTENT_WIDTH_DXA,
  run, para, bulletPara, emptyPara, cell,
  sectionHeaderRow, labelContentRow,
} = H;
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, AlignmentType, ShadingType,
} = docx;

// ============================================================
// TITLE BLOCK
// ============================================================
function buildTitleBlock() {
  return [
    new Paragraph({
      children: [run(
        "SUMMARY TABLE: BIOLOGY GRADE 10 — GASEOUS EXCHANGE AND RESPIRATION (PLANTS)",
        { bold: true, size: H.TITLE_SIZE, color: C.darkBlue }
      )],
      alignment: AlignmentType.LEFT,
      spacing: { before: 0, after: 120 },
    }),
    new Paragraph({
      children: [run(
        "Sub-Strand 2.3 — Teacher Reference (Lessons 1-6 Test Bundle)",
        { italic: true, size: H.SUBTITLE_SIZE, color: C.teal }
      )],
      alignment: AlignmentType.LEFT,
      spacing: { before: 0, after: 360 },
    }),
  ];
}

// ============================================================
// HEADER TABLE (Sub-Strand and Driving Question)
// ============================================================
function buildHeaderTable() {
  const labelW = 3200;
  const contW = CONTENT_WIDTH_DXA - labelW;
  const rows = [
    sectionHeaderRow(
      "SUMMARY TABLE: BIOLOGY GRADE 10 — GASEOUS EXCHANGE AND RESPIRATION (PLANTS)",
      C.darkBlue, CONTENT_WIDTH_DXA
    ),
    labelContentRow("Sub-Strand", "2.3: Gaseous Exchange and Respiration (Plants)",
      { labelWidth: labelW, contentWidth: contW }),
    labelContentRow("Driving Question", data.overview.drivingQuestion,
      { labelFill: C.lightPurple, labelWidth: labelW, contentWidth: contW }),
  ];
  return new Table({
    rows,
    width: { size: CONTENT_WIDTH_DXA, type: WidthType.DXA },
    columnWidths: [labelW, contW],
    borders: H.tableBorders(),
  });
}

// ============================================================
// INSTRUCTIONS TABLE
// ============================================================
function buildInstructionsTable() {
  const text =
    "FOR TEACHERS: This is the teacher reference version - each row is pre-filled with expected " +
    "student responses. Use it to assess student Summary Tables, identify gaps, and prepare discussion " +
    "questions. The student version (with blank cells) can be derived from this template. " +
    "Note: This is a 6-lesson test bundle. The full Summary Table for the 22-lesson sub-strand will " +
    "include rows for respiration, fermentation, and synthesis lessons.";
  const rows = [
    sectionHeaderRow("INSTRUCTIONS", C.purple, CONTENT_WIDTH_DXA),
    new TableRow({
      children: [cell({ width: CONTENT_WIDTH_DXA, text: text })],
    }),
  ];
  return new Table({
    rows,
    width: { size: CONTENT_WIDTH_DXA, type: WidthType.DXA },
    columnWidths: [CONTENT_WIDTH_DXA],
    borders: H.tableBorders(),
  });
}

// ============================================================
// MAIN SUMMARY TABLE (5 columns, one row per lesson)
// ============================================================
function buildMainTable() {
  // Landscape content width = 13680. Wider columns for content.
  const lessonW = 1800;
  const dqbW = 1800;
  const contentW = Math.floor((CONTENT_WIDTH_DXA - lessonW - dqbW) / 3);  // ~3360
  const lastContentW = CONTENT_WIDTH_DXA - lessonW - dqbW - (contentW * 2);
  const columnWidths = [lessonW, contentW, contentW, lastContentW, dqbW];

  const headerRow = new TableRow({
    tableHeader: true,
    children: [
      cell({ width: lessonW, fill: C.darkBlue, text: "Lesson # and Title",
             bold: true, color: C.white, size: 18 }),
      cell({ width: contentW, fill: C.medBlue, text: "What did I observe?",
             bold: true, color: C.white, size: 18 }),
      cell({ width: contentW, fill: C.teal, text: "What did I learn?",
             bold: true, color: C.white, size: 18 }),
      cell({ width: lastContentW, fill: C.purple, text: "How does this explain the phenomenon?",
             bold: true, color: C.white, size: 18 }),
      cell({ width: dqbW, fill: C.orange, text: "DQB Tracking",
             bold: true, color: C.white, size: 18 }),
    ],
  });

  const dataRows = data.lessons.map((lesson, idx) => {
    const altFill = idx % 2 === 0 ? C.white : C.grey;
    const lessonLabel = `Lesson ${lesson.number}\n${lesson.title}`;
    return new TableRow({
      children: [
        cell({
          width: lessonW,
          fill: C.lightBlue,
          children: [
            new Paragraph({
              children: [run(`Lesson ${lesson.number}`, { bold: true })],
              spacing: { before: 0, after: 40 },
            }),
            new Paragraph({
              children: [run(lesson.title, { bold: true, size: 16 })],
              spacing: { before: 0, after: 60 },
            }),
          ],
        }),
        cell({ width: contentW, fill: altFill, text: lesson.sectionE.observe }),
        cell({ width: contentW, fill: altFill, text: lesson.sectionE.learn }),
        cell({ width: lastContentW, fill: altFill, text: lesson.sectionE.explain }),
        cell({ width: dqbW, fill: C.lightOrange, text: lesson.dqbTracking, italic: true }),
      ],
    });
  });

  return [
    // Header bar
    new Table({
      rows: [sectionHeaderRow("LESSON-BY-LESSON SUMMARY TABLE", C.darkBlue, CONTENT_WIDTH_DXA)],
      width: { size: CONTENT_WIDTH_DXA, type: WidthType.DXA },
      columnWidths: [CONTENT_WIDTH_DXA],
      borders: H.tableBorders(),
    }),
    new Table({
      rows: [headerRow, ...dataRows],
      width: { size: CONTENT_WIDTH_DXA, type: WidthType.DXA },
      columnWidths: columnWidths,
      borders: H.tableBorders(),
    }),
  ];
}

// ============================================================
// MAIN
// ============================================================
function buildDocument() {
  const children = [];
  for (const p of buildTitleBlock()) children.push(p);
  children.push(buildHeaderTable());
  children.push(emptyPara());
  children.push(buildInstructionsTable());
  children.push(emptyPara());
  for (const t of buildMainTable()) children.push(t);

  // Footer
  children.push(emptyPara());
  children.push(new Paragraph({
    children: [run(
      "Note: This 6-lesson test bundle covers Lessons 1-6 of the 22-lesson sub-strand. " +
      "In the full production run, this Summary Table will extend to all 22 lessons, with the final-lesson " +
      "row showing the complete answer to the driving question.",
      { italic: true, size: H.BODY_SIZE, color: "707070" }
    )],
    alignment: AlignmentType.LEFT,
    spacing: { before: 240, after: 240 },
  }));

  return new Document({
    creator: "CBE Generation System",
    title: "Biology Grade 10 Sub-Strand 2.3 Summary Table (L1-6 test bundle)",
    styles: {
      default: { document: { run: { font: H.FONT, size: H.BODY_SIZE } } },
    },
    sections: [{
      properties: {
        page: {
          size: { width: 15840, height: 12240 },  // LANDSCAPE - the 5-col table is wide
          margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 },
        },
      },
      children: children,
    }],
  });
}

async function main() {
  // Re-set CONTENT_WIDTH for landscape orientation
  // Landscape US Letter: 15840 wide minus 2*1080 margin = 13680 DXA
  // We'll keep the helper's 9360 for now since the tables work at that width;
  // actually we should override for landscape. Let's check by running first.
  const doc = buildDocument();
  const buffer = await Packer.toBuffer(doc);
  const outPath = path.join(__dirname, "..", "output",
    "Biology_GaseousExchangePlants_SummaryTable.docx");
  fs.writeFileSync(outPath, buffer);
  console.log("Wrote:", outPath, "(" + buffer.length + " bytes)");
}

main().catch(err => {
  console.error("ERROR:", err);
  process.exit(1);
});
