// Generator 2 of 3: Final Explanation document.
// Produces: Biology_GaseousExchangePlants_FinalExplanation.docx
//
// Note for the 6-lesson test bundle: in a full sub-strand this document would
// contain a complete answer to the driving question after all 22 lessons.
// For the 6-lesson bundle, the worked exemplar is deliberately limited to the
// material covered in Lessons 1-6 (gas-exchange sites, anatomy, photosynthetic
// theory). The Final Explanation will be expanded in the full production run.

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
// CONTENT - exemplar student answer covering Lessons 1-6 only.
// In the full 22-lesson run, this would be a complete answer.
// ============================================================

const sections = [
  {
    title: "SECTION 1: WHAT DO LEAVES DIPPED IN WARM WATER ACTUALLY DO?",
    prompt: "Describe what students observe when fresh leaves are placed in warm water. State where the bubbles come from on the leaf, and why a plant exchanges gases with its environment at all.",
    answer: "When fresh leaves of maize, Tradescantia, and other plants are submerged in warm water at about 40 degrees Celsius, fine streams of bubbles begin to rise from the leaves within a minute. The bubbles come specifically from the underside of each leaf, not from the upper surface. The warmer the water, the faster the bubbles appear. Plants exchange gases with their environment because they are living organisms whose cells need oxygen for respiration and carbon dioxide for photosynthesis. Like all living organisms, plants must continuously exchange gases to stay alive. The bubbles in the warm-water demonstration are visible evidence of this exchange happening.",
  },
  {
    title: "SECTION 2: WHERE ON THE LEAF DOES GAS EXCHANGE HAPPEN?",
    prompt: "Name and describe the four sites of gaseous exchange in plants. Explain why bubbles in the warm-water demonstration came specifically from the underside of the leaves.",
    answer: "Plants have four sites of gaseous exchange. (1) Stomata are small mouth-shaped openings on leaves and green stems, flanked by paired guard cells; they are the primary site of gas exchange. (2) The cuticle is a waxy layer on the leaf surface that allows only very limited gas exchange and exists mainly to reduce water loss. (3) Lenticels are small openings on woody stems and bark, used by plants such as trees whose stems are no longer green. (4) Pneumatophores are aerial roots in mangroves and other waterlogged-soil plants such as the Avicennia marina mangroves at Mida Creek on the Kenyan coast - they emerge above the mud to bring oxygen to roots growing in oxygen-poor mud. The bubbles in the Lesson 1 demonstration came from the underside of the leaves because stomata are concentrated on the underside. This placement reduces water loss (the underside is shaded and cooler) while still allowing efficient gas exchange.",
  },
  {
    title: "SECTION 3: HOW ARE GAS-EXCHANGE STRUCTURES ADAPTED TO DIFFERENT ENVIRONMENTS?",
    prompt: "Compare gas-exchange adaptations in three plants from different environments: a terrestrial maize plant, an aquatic water lily, and a Kenyan coastal mangrove. Use at least one Kenyan example.",
    answer: "Different environments demand different gas-exchange adaptations even though all plants need to exchange the same gases. (1) Maize, a terrestrial monocot grown widely in Kenya, has stomata concentrated on the underside of its leaves and a waxy cuticle on the upperside; both adaptations reduce water loss in dry terrestrial conditions. (2) The water lily, an aquatic plant, has stomata on the upper surface of its floating leaves (the surface in contact with air, not water) and aerenchyma - air-filled tissue - that connects the leaves to submerged roots, allowing oxygen to reach root tissues. (3) The Kenyan coastal mangrove (e.g. Avicennia marina at Mida Creek and the Tana Delta) uses pneumatophores - aerial roots that grow upward out of waterlogged mud at low tide. These act as snorkels, allowing oxygen to reach the buried root system through internal air spaces. Mangroves are vital to Kenyan coastal ecosystems, supporting over 60 percent of commercial fish species during their juvenile stage, protecting the coast from erosion, and storing carbon. Their loss to charcoal harvesting and salt-pan construction is a national environmental concern. The same biological function (gas exchange) is achieved through three very different structural solutions, each matched to its environment.",
  },
  {
    title: "SECTION 4: WHAT DO STOMATA LOOK LIKE, AND HOW DO THEY OPEN AND CLOSE?",
    prompt: "Describe what stomata look like under a microscope. Compare guard-cell shape in different plants. Explain the three classical theories of stomatal opening, and evaluate the photosynthetic theory in particular.",
    answer: "Under a light microscope, stomata appear as small mouth-shaped pores flanked by two guard cells. In dicots such as Tradescantia and kale, the guard cells are kidney-shaped; in grasses such as maize, they are dumbbell-shaped. The dumbbell shape is more mechanically efficient and allows opening with less water movement, making it useful in drier conditions - relevant to maize as a Kenyan staple crop. Stomatal density varies between species but is typically several hundred per square millimetre on the leaf underside. Three classical theories explain how stomata open and close: (1) the photosynthetic theory, which proposes that light triggers photosynthesis in the guard-cell chloroplasts, raising sugar concentration, lowering water potential, drawing water in by osmosis, and swelling the cells to open the pore; (2) the starch-sugar interconversion theory, which proposes that stored starch in guard cells is enzymatically converted to sugar at dawn, achieving the same osmotic effect; (3) the potassium ion theory, which proposes that K+ ions are actively pumped into guard cells from neighbouring cells, lowering water potential and again drawing water in by osmosis. All three theories converge on the same final step: water enters by osmosis, the guard cells swell, and the pore opens. The photosynthetic theory is partially supported - guard cells uniquely contain chloroplasts (supporting evidence) and stomata generally open in light (supporting evidence), but stomata can also open in CO2-free air where photosynthesis would be limited (contradicting evidence). This shows that the photosynthetic theory captures part of the truth but not all of it; another mechanism must also be operating.",
  },
  {
    title: "SECTION 5: WHY DOES THIS BIOLOGY MATTER FOR KENYA?",
    prompt: "Explain the practical importance of understanding plant gas exchange and stomatal mechanism for Kenyan agriculture, food security, and environmental conservation. Include at least two Kenyan examples.",
    answer: "Understanding plant gas exchange and stomatal mechanism has direct practical implications for Kenyan agriculture, food security, and environmental conservation. (1) Maize agriculture: maize is Kenya's staple crop. Its dumbbell-shaped guard cells are an adaptation for efficient stomatal control in variable rainfall conditions. Knowledge of how stomata respond to water availability informs drought-resistant breeding programmes at KARLO (the Kenya Agricultural and Livestock Research Organisation). (2) Mangrove conservation: Kenyan mangroves at Mida Creek, Lamu, and the Tana Delta depend on pneumatophores for root oxygenation. Loss of mangroves to charcoal-making and salt-pan construction destroys nursery habitat for fish, weakens coastal protection from erosion, and removes a significant carbon sink. Conservation policy in Kenya draws on the biology of pneumatophore function. (3) Career connections: the field supports careers in plant physiology, agricultural science, environmental science, and biotechnology - areas central to Vision 2030. The bubble phenomenon we investigated in Lesson 1 is therefore not merely a classroom curiosity. It is the visible evidence of biological processes that underpin Kenyan food security, coastal ecosystem health, and the careers many of you will enter as future scientists and farmers.",
  },
];

// ============================================================
// RUBRIC (5 criteria, 4 levels each)
// ============================================================
const rubric = [
  {
    criterion: "Description of the warm-water phenomenon (Section 1)",
    excellent: "Accurately describes the bubble phenomenon, locates bubbles on the leaf underside, identifies temperature dependence, and frames gas exchange as essential to life.",
    proficient: "Accurately describes the phenomenon and locates the bubbles, with a brief explanation of why plants exchange gases.",
    developing: "Describes the phenomenon but misses the underside location or the temperature link.",
  },
  {
    criterion: "Four gas-exchange sites and the underside-bubble explanation (Section 2)",
    excellent: "All four sites named and described with location and function. Includes the Mida Creek mangrove example. Clear explanation linking stomatal density to underside bubbling.",
    proficient: "Three or four sites named with brief description. Underside explanation present.",
    developing: "Fewer than three sites named, or underside explanation missing or vague.",
  },
  {
    criterion: "Adaptation comparison across three environments (Section 3)",
    excellent: "All three case studies (maize, water lily, mangrove) covered with structure-environment matching. At least one Kenyan example developed in detail.",
    proficient: "Three case studies covered. Kenyan example present but less detailed.",
    developing: "Only one or two case studies, or Kenyan context missing.",
  },
  {
    criterion: "Stomatal observation and the three theories (Section 4)",
    excellent: "Microscope observation accurately described. All three theories named with their mechanisms. Photosynthetic theory evaluated with both supporting and contradicting evidence.",
    proficient: "Microscope observation present. All three theories named. Photosynthetic theory evaluated with at least one piece of evidence on each side.",
    developing: "Microscope observation vague, fewer than three theories named, or evaluation one-sided.",
  },
  {
    criterion: "Kenyan relevance and career connection (Section 5)",
    excellent: "At least two Kenyan examples developed in detail (e.g. maize agriculture and mangrove conservation). Career connection explicit. Vision 2030 link or similar civic framing.",
    proficient: "Two Kenyan examples present with brief development. Career connection mentioned.",
    developing: "Only one Kenyan example, or career connection missing.",
  },
];

// ============================================================
// BUILDERS
// ============================================================
function buildTitleBlock() {
  return [
    new Paragraph({
      children: [run(
        "FINAL EXPLANATION: GASEOUS EXCHANGE AND RESPIRATION (PLANTS)",
        { bold: true, size: H.TITLE_SIZE, color: C.darkBlue }
      )],
      alignment: AlignmentType.LEFT,
      spacing: { before: 0, after: 120 },
    }),
    new Paragraph({
      children: [run(
        "Biology Grade 10 — Student Assessment Document (Lessons 1-6 Test Bundle)",
        { italic: true, size: H.SUBTITLE_SIZE, color: C.teal }
      )],
      alignment: AlignmentType.LEFT,
      spacing: { before: 0, after: 360 },
    }),
  ];
}

function buildIdentificationTable() {
  const rows = [
    sectionHeaderRow("FINAL EXPLANATION: GASEOUS EXCHANGE AND RESPIRATION (PLANTS)", C.darkBlue),
    labelContentRow("Student Name", "_______________________________________________"),
    labelContentRow("Class", "_______________________________________________"),
    labelContentRow("Date", "_______________________________________________"),
  ];
  return new Table({
    rows,
    width: { size: CONTENT_WIDTH_DXA, type: WidthType.DXA },
    columnWidths: [3200, CONTENT_WIDTH_DXA - 3200],
    borders: H.tableBorders(),
  });
}

function buildInstructions() {
  const instructionText =
    "You have completed Lessons 1-6 of Plant Gaseous Exchange and Respiration. Write your COMPLETE EXPLANATION " +
    "for the driving question: \"Why do leaves dipped in warm water produce bubbles, and what does this tell us " +
    "about how plants breathe and live?\" USE: Your Summary Table, Plant Gas-Exchange Model, microscope observations, " +
    "and the Mida Creek mangrove case study. " +
    "YOUR EXPLANATION MUST INCLUDE: the warm-water phenomenon and underside bubble location; the four gas-exchange " +
    "sites; comparison of adaptations across terrestrial, aquatic, and mangrove plants; what stomata look like under " +
    "the microscope; the three classical theories of stomatal opening; evaluation of the photosynthetic theory; at " +
    "least TWO Kenyan examples; a career connection. " +
    "GRADING: 20 points total (see rubric below). Minimum 400 words. " +
    "Note: This is a 6-lesson test bundle. The full Final Explanation will incorporate respiration, fermentation, " +
    "and a complete model of the bubble phenomenon when all 22 lessons are taught.";

  const rows = [
    sectionHeaderRow("INSTRUCTIONS FOR STUDENTS", C.purple),
    new TableRow({
      children: [cell({ width: CONTENT_WIDTH_DXA, text: instructionText })],
    }),
  ];
  return new Table({
    rows,
    width: { size: CONTENT_WIDTH_DXA, type: WidthType.DXA },
    columnWidths: [CONTENT_WIDTH_DXA],
    borders: H.tableBorders(),
  });
}

function buildSection(idx, sec) {
  const rows = [
    sectionHeaderRow(sec.title, C.darkBlue),
    new TableRow({
      children: [cell({
        width: CONTENT_WIDTH_DXA,
        text: sec.prompt,
        italic: true,
      })],
    }),
    new TableRow({
      children: [cell({
        width: CONTENT_WIDTH_DXA,
        text: sec.answer,
      })],
    }),
  ];
  return new Table({
    rows,
    width: { size: CONTENT_WIDTH_DXA, type: WidthType.DXA },
    columnWidths: [CONTENT_WIDTH_DXA],
    borders: H.tableBorders(),
  });
}

function buildRubric() {
  const colW = Math.floor(CONTENT_WIDTH_DXA / 4);
  const lastColW = CONTENT_WIDTH_DXA - (colW * 3);

  const headerRow = new TableRow({
    tableHeader: true,
    children: [
      cell({ width: colW, fill: C.darkBlue, text: "Criterion",
             bold: true, color: C.white, size: 18 }),
      cell({ width: colW, fill: C.green, text: "Excellent (4)",
             bold: true, color: C.white, size: 18 }),
      cell({ width: colW, fill: C.medBlue, text: "Proficient (3)",
             bold: true, color: C.white, size: 18 }),
      cell({ width: lastColW, fill: C.orange, text: "Developing (1-2)",
             bold: true, color: C.white, size: 18 }),
    ],
  });

  const dataRows = rubric.map((r, idx) => {
    const altFill = idx % 2 === 0 ? C.white : C.grey;
    return new TableRow({
      children: [
        cell({ width: colW, fill: C.lightBlue, text: r.criterion, bold: true }),
        cell({ width: colW, fill: altFill, text: r.excellent }),
        cell({ width: colW, fill: altFill, text: r.proficient }),
        cell({ width: lastColW, fill: altFill, text: r.developing }),
      ],
    });
  });

  return [
    new Table({
      rows: [sectionHeaderRow("FINAL EXPLANATION RUBRIC (20 points)", C.darkBlue)],
      width: { size: CONTENT_WIDTH_DXA, type: WidthType.DXA },
      columnWidths: [CONTENT_WIDTH_DXA],
      borders: H.tableBorders(),
    }),
    new Table({
      rows: [headerRow, ...dataRows],
      width: { size: CONTENT_WIDTH_DXA, type: WidthType.DXA },
      columnWidths: [colW, colW, colW, lastColW],
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
  children.push(buildIdentificationTable());
  children.push(emptyPara());
  children.push(buildInstructions());
  children.push(emptyPara());
  for (let i = 0; i < sections.length; i++) {
    children.push(buildSection(i, sections[i]));
    children.push(emptyPara());
  }
  for (const t of buildRubric()) children.push(t);

  return new Document({
    creator: "CBE Generation System",
    title: "Biology Grade 10 Sub-Strand 2.3 Final Explanation",
    styles: {
      default: { document: { run: { font: H.FONT, size: H.BODY_SIZE } } },
    },
    sections: [{
      properties: {
        page: {
          size: { width: 15840, height: 12240 },  // LANDSCAPE
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
    "Biology_GaseousExchangePlants_FinalExplanation.docx");
  fs.writeFileSync(outPath, buffer);
  console.log("Wrote:", outPath, "(" + buffer.length + " bytes)");
}

main().catch(err => {
  console.error("ERROR:", err);
  process.exit(1);
});
