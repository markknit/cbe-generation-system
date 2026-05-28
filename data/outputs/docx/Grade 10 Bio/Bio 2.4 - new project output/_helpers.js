// Shared formatting helpers for CBE lesson plan generators.
// Implements the standards in CLAUDE.md:
//   - Arial throughout, body 18 (=9pt)
//   - US Letter, 0.75" margins (1080 DXA), content width 9360 DXA
//   - 6-column Section C, all DXA widths
//   - Visible single-line borders on all table cells
//   - Plant Nutrition colour palette

const docx = require("docx");
const {
  Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, BorderStyle, ShadingType, AlignmentType,
  HeightRule, VerticalAlign,
} = docx;

// ============================================================
// COLOUR PALETTE (per CLAUDE.md, matches Plant Nutrition exemplar)
// ============================================================
const C = {
  darkBlue:    "1F3864",
  medBlue:     "2E75B6",
  lightBlue:   "D5E8F0",
  teal:        "1F6B75",
  lightTeal:   "D9EEF1",
  green:       "375623",
  lightGreen:  "E2EFDA",
  orange:      "C55A11",
  lightOrange: "FCE4D6",
  purple:      "7030A0",
  lightPurple: "EAD1F5",
  grey:        "F2F2F2",
  white:       "FFFFFF",
};

// Phase-row colour map (Section C, column 1)
const PHASE_COLOURS = {
  "Predict Phase": C.lightPurple,
  "Observe Phase": C.lightTeal,
  "Explain Phase": C.lightGreen,
  "Driving Question Board (DQB) Creation": C.lightOrange,
  "Model Building Phase": C.lightBlue,
};

// ============================================================
// LAYOUT CONSTANTS
// ============================================================
// All documents now use LANDSCAPE US Letter (15840 x 12240 DXA)
// with 0.75" margins (1080 DXA) -> content width = 15840 - 2*1080 = 13680
const CONTENT_WIDTH_DXA = 13680;
const FONT = "Arial";
const BODY_SIZE = 18;            // 9pt in docx-js half-point units
const HEADING_SIZE = 28;         // 14pt
const TITLE_SIZE = 36;           // 18pt
const SUBTITLE_SIZE = 22;        // 11pt

// ============================================================
// BORDER HELPERS
// ============================================================
function singleBorder(color = "808080", size = 4) {
  return { style: BorderStyle.SINGLE, size, color };
}

function allBorders(color = "808080", size = 4) {
  const b = singleBorder(color, size);
  return { top: b, bottom: b, left: b, right: b };
}

function tableBorders(color = "808080", size = 4) {
  const b = singleBorder(color, size);
  return {
    top: b, bottom: b, left: b, right: b,
    insideHorizontal: b, insideVertical: b,
  };
}

// ============================================================
// TEXT RUN HELPERS
// ============================================================
function run(text, opts = {}) {
  return new TextRun({
    text: text,
    font: FONT,
    size: opts.size || BODY_SIZE,
    bold: opts.bold || false,
    italics: opts.italic || false,
    color: opts.color || "000000",
  });
}

function para(text, opts = {}) {
  return new Paragraph({
    children: [run(text, opts)],
    alignment: opts.align || AlignmentType.LEFT,
    spacing: { before: opts.spaceBefore || 0, after: opts.spaceAfter || 80 },
  });
}

// Bullet paragraph using en-dash (per CLAUDE.md - no unicode bullet chars
// without numbering config; en-dash matches the Plant Nutrition exemplar)
function bulletPara(text) {
  return new Paragraph({
    children: [run("\u2013  " + text)],
    spacing: { before: 0, after: 60 },
  });
}

function emptyPara() {
  return new Paragraph({
    children: [run("")],
    spacing: { before: 0, after: 80 },
  });
}

// ============================================================
// CELL BUILDER
// ============================================================
function cell(opts) {
  const {
    width,
    fill,
    children,        // array of Paragraph
    text,            // shortcut: single string -> single para
    bullets,         // shortcut: array of strings -> bullet paras
    bold = false,
    italic = false,
    color = "000000",
    size = BODY_SIZE,
    align = AlignmentType.LEFT,
    columnSpan,
    verticalAlign = VerticalAlign.TOP,
  } = opts;

  let kids;
  if (children) {
    kids = children;
  } else if (bullets) {
    kids = bullets.map(b => bulletPara(b));
  } else {
    kids = [
      new Paragraph({
        children: [run(text || "", { bold, italic, color, size })],
        alignment: align,
        spacing: { before: 0, after: 60 },
      }),
    ];
  }

  const cellOpts = {
    children: kids,
    width: { size: width, type: WidthType.DXA },
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    borders: allBorders(),
    verticalAlign: verticalAlign,
  };
  if (fill) {
    cellOpts.shading = { type: ShadingType.CLEAR, color: "auto", fill: fill };
  }
  if (columnSpan) {
    cellOpts.columnSpan = columnSpan;
  }
  return new TableCell(cellOpts);
}

// ============================================================
// SECTION HEADER PARAGRAPH (e.g. "A. SPECIFIC LEARNING OUTCOMES")
// Used as a single-cell row inside a table, with coloured fill.
// ============================================================
function sectionHeaderRow(text, fillColour = C.darkBlue, columnWidth = CONTENT_WIDTH_DXA) {
  return new TableRow({
    children: [
      new TableCell({
        children: [
          new Paragraph({
            children: [run(text, { bold: true, color: C.white, size: 22 })],
            alignment: AlignmentType.LEFT,
            spacing: { before: 40, after: 40 },
          }),
        ],
        width: { size: columnWidth, type: WidthType.DXA },
        margins: { top: 80, bottom: 80, left: 120, right: 120 },
        borders: allBorders(),
        shading: { type: ShadingType.CLEAR, color: "auto", fill: fillColour },
        columnSpan: 1,
      }),
    ],
  });
}

// ============================================================
// LESSON HEADER ROW (e.g. "LESSON 1: The Bubble Mystery (40 minutes)")
// Used to introduce each per-lesson table.
// Pass pageBreakBefore: true to start the lesson on a fresh page.
// ============================================================
function lessonHeaderParagraph(lessonNumber, lessonTitle, minutes = 40, opts = {}) {
  const { pageBreakBefore = false } = opts;
  return new Paragraph({
    children: [
      run(`LESSON ${lessonNumber}: ${lessonTitle} (${minutes} minutes)`,
          { bold: true, size: HEADING_SIZE, color: C.darkBlue }),
    ],
    spacing: { before: 360, after: 120 },
    alignment: AlignmentType.LEFT,
    pageBreakBefore: pageBreakBefore,
  });
}

// ============================================================
// TWO-COLUMN LABEL/CONTENT ROW
// (Standard pattern for sub-strand overview, Section A, Section E)
// Default label width 3200 DXA (~2.2") suits landscape layout.
// ============================================================
function labelContentRow(label, content, opts = {}) {
  const {
    labelWidth = 3200,
    contentWidth = CONTENT_WIDTH_DXA - 3200,
    labelFill = C.lightBlue,
    contentBullets = false,
  } = opts;

  const labelCell = cell({
    width: labelWidth,
    fill: labelFill,
    text: label,
    bold: true,
  });

  let contentCell;
  if (contentBullets && Array.isArray(content)) {
    contentCell = cell({
      width: contentWidth,
      bullets: content,
    });
  } else if (Array.isArray(content)) {
    // Multiple paragraphs (each an item)
    contentCell = cell({
      width: contentWidth,
      children: content.map(c => para(c, { size: BODY_SIZE })),
    });
  } else {
    contentCell = cell({
      width: contentWidth,
      text: content,
    });
  }

  return new TableRow({ children: [labelCell, contentCell] });
}

// ============================================================
// EXPORTS
// ============================================================
module.exports = {
  docx,
  C, PHASE_COLOURS,
  CONTENT_WIDTH_DXA, FONT, BODY_SIZE, HEADING_SIZE, TITLE_SIZE, SUBTITLE_SIZE,
  singleBorder, allBorders, tableBorders,
  run, para, bulletPara, emptyPara,
  cell,
  sectionHeaderRow, lessonHeaderParagraph, labelContentRow,
};
