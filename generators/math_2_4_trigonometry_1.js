'use strict';
/**
 * Generator: Mathematics Grade 10 — Sub-Strand 2.4: Trigonometry 1
 *
 * Phenomenon: A Kenya National Highways Authority (KeNHA) survey crew measuring the
 *   height of a new bridge support column before erecting scaffolding — using only a
 *   tape measure, a clinometer, and a known horizontal distance.
 *   Secondary: students build their own clinometer from a protractor and straw
 *   (per KICD PCI) and measure trees/buildings on the school compound.
 *
 * Outputs (3 formats each):
 *   data/outputs/docx/Grade 10 Math/Math 2.4 Trigonometry 1/docx/
 *   data/outputs/docx/Grade 10 Math/Math 2.4 Trigonometry 1/html/
 *   data/outputs/docx/Grade 10 Math/Math 2.4 Trigonometry 1/gfm/
 */

const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, AlignmentType, ShadingType, VerticalAlign, BorderStyle,
  PageOrientation, TableLayoutType,
} = require('docx');
const fs   = require('fs');
const path = require('path');
const { getAllPhaseResources, buildResourceParagraphs } = require('./aresResources');

const BASE     = path.join(__dirname, '..', 'data', 'outputs', 'docx', 'Grade 10 Math', 'Math 2.4 Trigonometry 1');
const OUT_DOCX = path.join(BASE, 'docx');
const OUT_HTML = path.join(BASE, 'html');
const OUT_GFM  = path.join(BASE, 'gfm');
for (const d of [OUT_DOCX, OUT_HTML, OUT_GFM]) {
  if (!fs.existsSync(d)) fs.mkdirSync(d, { recursive: true });
}

// ─── Colours ──────────────────────────────────────────────────────────────────
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
const W = 13680, FONT = 'Arial', SZ = 18, SZ_H = 22, SZ_T = 28;

// ─── Helpers ──────────────────────────────────────────────────────────────────
function para(text, opts = {}) {
  return new Paragraph({
    alignment: opts.align || AlignmentType.LEFT,
    spacing: { after: opts.after ?? 60, before: opts.before ?? 0 },
    children: [new TextRun({ text, font: FONT, size: opts.size || SZ,
      bold: opts.bold || false, color: opts.color || '000000', italics: opts.italic || false })],
  });
}
function bullet(text, opts = {}) {
  return new Paragraph({
    alignment: AlignmentType.LEFT, spacing: { after: 30, before: 0 },
    indent: { left: 360, hanging: 180 },
    children: [new TextRun({ text: '\u2013  ' + text, font: FONT,
      size: opts.size || SZ, bold: opts.bold || false, color: opts.color || '000000' })],
  });
}
function cell(content, opts = {}) {
  const { fill = C.white, w = null, span = 1, bold = false,
          color = '000000', size = SZ, align = AlignmentType.LEFT, italic = false } = opts;
  let children;
  if (typeof content === 'string') {
    children = content === '' ? [para('', { size })]
      : content.split('\n').map(line =>
          (line.startsWith('• ') || line.startsWith('- '))
            ? bullet(line.slice(2), { size, bold, color })
            : para(line, { size, bold, color, align, italic, after: 40 }));
  } else if (Array.isArray(content)) { children = content; }
  else { children = [content]; }
  const def = {
    verticalAlign: VerticalAlign.TOP,
    shading: { type: ShadingType.CLEAR, color: 'auto', fill },
    margins: { top: 60, bottom: 60, left: 120, right: 120 },
    children,
  };
  if (w !== null) def.width = { size: w, type: WidthType.DXA };
  if (span > 1)   def.columnSpan = span;
  return new TableCell(def);
}
function fullHeader(text, fill, textColor = 'FFFFFF', size = SZ_H, numCols = 2) {
  return new TableRow({ children: [cell(text, { fill, color: textColor, bold: true, size,
    align: AlignmentType.CENTER, span: numCols, w: W })] });
}
function labelRow(label, content, labelW = 3000, opts = {}) {
  return new TableRow({ children: [
    cell(label,   { fill: opts.labelFill   || C.lightBlue, bold: true, w: labelW, size: SZ }),
    cell(content, { fill: opts.contentFill || C.white,     w: W - labelW, size: SZ }),
  ]});
}
function makeTable(rows, columnWidths = [W]) {
  return new Table({
    width: { size: columnWidths.reduce((a, b) => a + b, 0), type: WidthType.DXA },
    layout: TableLayoutType.FIXED,
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
const PAGE_BREAK = () => new Paragraph({ pageBreakBefore: true, children: [] });
function titleBlock(title, subtitle) {
  return [
    para(title,    { bold: true, size: SZ_T, color: C.darkBlue, align: AlignmentType.CENTER, after: 80 }),
    para(subtitle, { size: SZ_H, color: C.teal, align: AlignmentType.CENTER, after: 160 }),
  ];
}

// ─── Unit Data ────────────────────────────────────────────────────────────────
const UNIT = {
  gradeLevel: 'Grade 10',
  subject:    'Mathematics',
  strand:     'Strand 2.0: Measurements and Geometry',
  substrand:  'Sub-Strand 2.4: Trigonometry 1',
  duration:   '15 lessons × 40 minutes = 600 minutes total',
  content:
    '• Trigonometric ratios of acute angles\n' +
    '• Sines and cosines of complementary angles\n' +
    '• Trigonometric ratios of special angles\n' +
    '• Application of trigonometric ratios',
  learningOutcomes:
    'By the end of the sub-strand, the learner should be able to:\n' +
    'a) determine the trigonometric ratios of acute angles from mathematical tables and calculators,\n' +
    'b) relate sines and cosines of complementary angles,\n' +
    'c) relate the sine, cosine and tangent of acute angles,\n' +
    'd) determine trigonometric ratios of special angles: 30°, 45°, 60° and 90° using triangles,\n' +
    'e) apply trigonometric ratios to angles of elevation and depression,\n' +
    'f) reflect on the use of trigonometry in real life situations.',
  coreCompetencies:
    '• Creativity and Imagination: the learner makes a simple clinometer using locally available material and uses it as a learning resource\n' +
    '• Critical Thinking and Problem Solving: the learner discusses and makes observations about the sine and cosine of complementary angles, and applies trigonometric ratios in the solution of triangles\n' +
    '• Digital Literacy: the learner uses digital devices and other resources such as books, manuals, and journals to learn more about trigonometric ratios',
  values:
    '• Responsibility: the learner takes care of mathematical tables and calculators used in determining trigonometric ratios\n' +
    '• Unity: the learner works in a group, for instance, when using an isosceles right-angled triangle and an equilateral triangle to generate the trigonometric ratios of special angles 30°, 45°, 60°, and 90°',
  pcis:
    '• Environmental Education and Protection: the learner identifies shapes in the immediate environment that have right-angled triangles, and makes a simple clinometer using materials from the immediate environment\n' +
    '• Parental Engagement and Empowerment: the learner gets support from parents/guardians to get resources to make a clinometer',
  keyInquiry:
    '1. What is trigonometry?\n' +
    '2. How do we use trigonometry in real-life situations?',
  phenomenon:
    'A Kenya National Highways Authority (KeNHA) survey crew needs to measure the height of a new ' +
    'bridge support column before erecting scaffolding. They cannot climb the column. They stand 30 m ' +
    'away and use a clinometer to measure the angle of elevation to the top: 62°. From this single ' +
    'measurement they calculate the exact height.\n' +
    'Secondary: students build their own clinometers from a protractor, straw, and plumb line, then ' +
    'walk outside to measure the height of the school flagpole, a tree, or the school building — ' +
    'never leaving the ground. Anchor question: "How can a single angle unlock a distance you can\'t measure directly?"',
  drivingQuestion:
    'How do surveyors, engineers, and builders in Kenya calculate heights and distances that are ' +
    'impossible to measure directly — using only an angle and a known distance?',
  storylineThread:
    'L1: Build a clinometer → measure the school flagpole → initial model: "What are the three sides/angle relationships?"\n' +
    'L2: Define sin, cos, tan for acute angles → build ratio tables from right-triangle measurements\n' +
    'L3: Use mathematical tables and calculators to find trig ratios → connect to Lesson 2 physical measurements\n' +
    'L4: Discover complementary angle relationship (sin θ = cos(90°−θ)) → model updated\n' +
    'L5: Derive special angle ratios (30°, 45°, 60°) from exact triangles → no tables needed\n' +
    'L6: Apply to angles of elevation and depression → KeNHA bridge challenge solved → Final Explanation',
};

// ─── Lessons ──────────────────────────────────────────────────────────────────
const LESSONS = [

  // ── LESSON 1 ──────────────────────────────────────────────────────────────
  {
    number: 1,
    aresKeywords: 'trigonometry right triangle angle ratio',
    title:    'What Is Trigonometry? Building a Clinometer',
    duration: '40 minutes',
    slo: {
      purpose:
        'Students encounter the central problem of trigonometry — measuring inaccessible heights — ' +
        'and build a clinometer to begin collecting real data.',
      knowledge:
        '• Describe trigonometry as the mathematics of right-angled triangles and angle–side relationships\n' +
        '• Identify the hypotenuse, opposite, and adjacent sides relative to a given acute angle\n' +
        '• Describe the function of a clinometer',
      skills:
        '• Construct a simple clinometer from a protractor, straw, string, and small weight\n' +
        '• Use the clinometer to measure the angle of elevation of a tall object\n' +
        '• Record angle and horizontal distance measurements',
      attitudes:
        '• Curiosity about how engineers solve real measurement problems\n' +
        '• Appreciation that mathematics is a practical tool used in Kenyan infrastructure projects',
      keyInquiry: 'What is trigonometry?',
      purposeInStoryline:
        'This lesson anchors the unit in the KeNHA phenomenon and gives students immediate experience ' +
        'of the measurement challenge that trigonometry solves. The clinometer is the physical embodiment of angle measurement.',
      safetyNotes:
        'When going outside to measure: stay within school boundaries, do not look directly at the sun ' +
        'through the clinometer straw, supervise students near tall structures.',
    },
    overview:
      'Teacher shows a KeNHA photograph: a survey crew measuring the height of a bridge column. ' +
      '"They are 30 m away. The angle to the top is 62°. How tall is the column? They never touched the column." ' +
      'Students discuss strategies. After establishing that they need a new mathematical tool, ' +
      'groups build clinometers from protractors, straws, string, and a small weight.\n\n' +
      'In the second half of the lesson, groups go outside and measure the angle of elevation of ' +
      'the school flagpole (or a tree/wall) from a known horizontal distance. Data is recorded for use in Lesson 2. ' +
      'The DQB is opened: "What is the relationship between the angle and the sides of the triangle?"',
    framework: [
      {
        phase: 'Predict Phase',
        learnerExperience:
          'Shown: KeNHA photograph of bridge column survey. Groups discuss and write: ' +
          '"How would you find the height of this column without climbing it? List at least two methods." ' +
          'Share predictions — class likely mentions: rope, shadow, estimate, special instrument.',
        resource:
          'MATERIAL: KeNHA bridge photograph (A4 printed or projected)\n' +
          'CONTEXT: Kenya National Highways Authority — builds and maintains national roads and bridges',
        teacherMoves:
          '"None of the survey crew touched the column. They used only a measuring tape (for distance) and one angle." \n' +
          '"What is the name of the angle from the ground up to the top of the column? (Angle of elevation.)"',
        sensemakingStrategy:
          'Real-world engineering problem creates immediate motivation. Insufficient current tools creates productive need.',
        formativeAssessment:
          'What strategies do students suggest? Do any already mention triangles or angles? ' +
          'This reveals prior knowledge from geometry units.',
      },
      {
        phase: 'Observe Phase',
        learnerExperience:
          'Build a clinometer (per KICD PCI):\n' +
          '1. Tape a protractor to a flat piece of card.\n' +
          '2. Thread a piece of string through the protractor centre hole; tie a small weight (bolt/coin) at one end.\n' +
          '3. Tape a straw along the flat edge (0°–180° baseline).\n' +
          '4. To measure: look through the straw at the top of a tall object. Read where the plumb string crosses the scale.\n' +
          '5. Angle of elevation = 90° − reading.\n' +
          'Calibration test: look horizontally — reading should be 90°, giving angle of elevation = 0°.',
        resource:
          'MATERIAL (per group): protractor, straw, 30 cm string, small bolt or coin, tape, card\n' +
          'PARENT NOTE: Students may bring these materials from home (Parental Engagement PCI)',
        teacherMoves:
          '"The string always hangs vertically — that is your reference. When you tilt the clinometer upward, the string reads less than 90°."\n' +
          '"Calibrate first: look at the horizon. What does the string read? Should be 90°."',
        sensemakingStrategy:
          'Physical construction of a scientific instrument gives students ownership of the measurement tool. ' +
          'Calibration builds precision habits.',
        formativeAssessment: 'Test each group\'s clinometer: look at a horizontal reference — string should read 90°.',
      },
      {
        phase: 'Explain Phase',
        learnerExperience:
          'Outside measurement:\n' +
          '1. Stand a known distance d from the base of a tall object (flagpole, tree, wall).\n' +
          '2. Use clinometer to measure the angle of elevation θ to the top.\n' +
          '3. Record: d = ___ m, θ = ___°.\n' +
          '4. Draw the right triangle formed: horizontal base = d, vertical side = height (unknown), angle at observer = θ.\n' +
          '5. Label the three sides: hypotenuse, opposite (height, unknown), adjacent (base, = d).',
        resource:
          'MATERIAL: Clinometer (built above), measuring tape, recording sheet\n' +
          'VOCAB: hypotenuse, opposite side, adjacent side, angle of elevation',
        teacherMoves:
          '"The opposite side is the side OPPOSITE the angle θ — that is the height we want to find."\n' +
          '"The adjacent side is NEXT TO the angle — that is the horizontal distance d."\n' +
          '"We know d and θ. We want the opposite side. Lesson 2 gives us the formula."',
        sensemakingStrategy:
          'Students leave with real data (d, θ) that needs a formula. This creates authentic motivation for Lesson 2.',
        formativeAssessment:
          'Check recorded triangles: are opposite, adjacent, and hypotenuse labelled correctly relative to angle θ?',
      },
      {
        phase: 'Driving Question Board (DQB) Creation',
        learnerExperience:
          'Open the DQB. Questions likely: "What is the formula for height?" "What is sin/cos/tan?" ' +
          '"Why is the hypotenuse always the longest?" "What if the angle is very small?" ' +
          'Categorise: RATIOS / SPECIAL ANGLES / APPLICATIONS.',
        resource: 'MATERIAL: DQB board, sticky notes',
        teacherMoves: '"By Lesson 6, you will answer every one of these questions — and solve the KeNHA bridge problem."',
        sensemakingStrategy: 'DQB makes the unit purpose explicit. Students are intellectually invested.',
        formativeAssessment: 'Questions reveal whether students already know "sin/cos/tan" vocabulary.',
      },
      {
        phase: 'Model Building Phase',
        learnerExperience:
          'Initial Model: Draw the flagpole triangle from today\'s measurement. Label all known values (d, θ). ' +
          'Write: "What formula or rule do I think connects the angle to the height?" ' +
          'No definition yet — this is a prediction.',
        resource: 'MATERIAL: Model Journal page (Lesson 1)',
        teacherMoves: '"Your model will change as you learn the ratios. Keep this first version — it shows your starting point."',
        sensemakingStrategy: 'Initial model as baseline. The unknown (height formula) creates intellectual suspense.',
        formativeAssessment: 'Do students draw the right triangle correctly? Any students who already write "tan θ = opposite/adjacent"?',
      },
    ],
    teacherReflection:
      'After teaching this lesson, reflect on:\n\n' +
      '1. Did the KeNHA photograph create genuine curiosity? What student comments showed engagement?\n\n' +
      '2. Clinometer construction: which groups had difficulty with calibration? What was the most common error?\n\n' +
      '3. Labelling opposite, adjacent, hypotenuse: did students consistently confuse "opposite" when the angle was relabelled?\n\n' +
      '4. Quality of outside measurement data: are angles reasonable (10°–70°) and distances practical (5–30 m)?\n\n' +
      '5. DQB: did students ask specifically about sin/cos/tan (showing prior exposure) or only about "the formula"?\n\n' +
      '6. What excitement or confusion do you want to carry forward into Lesson 2?',
    summaryTablePrompt: {
      observed:
        'KeNHA photograph: survey crew measuring bridge column height from 30 m away using angle of elevation 62°. ' +
        'Built a clinometer from protractor, straw, string, weight. ' +
        'Measured angle of elevation of school flagpole from a known horizontal distance. ' +
        'Drew the right triangle: labelled opposite, adjacent, hypotenuse relative to angle θ.',
      learned:
        'Trigonometry is the mathematics of right-angled triangles and the relationship between their angles and sides. ' +
        'An angle of elevation is measured from horizontal upward to the top of an object. ' +
        'In a right triangle: the hypotenuse is always opposite the right angle; opposite and adjacent depend on which acute angle you are working from.',
      explained:
        'The KeNHA surveyor has a right triangle: adjacent = 30 m (known), angle = 62° (measured), opposite = height (unknown). ' +
        'We have the angle and one side — but we still need the formula that connects these. That is what Lesson 2 reveals.',
    },
  },

  // ── LESSON 2 ──────────────────────────────────────────────────────────────
  {
    number: 2,
    aresKeywords: 'sine cosine tangent SOH CAH TOA ratios',
    title:    'Defining Sin, Cos, and Tan — Building Ratio Tables',
    duration: '40 minutes',
    slo: {
      purpose:
        'Students define the three trigonometric ratios from measurements of similar right triangles, ' +
        'discovering that ratios depend only on the angle, not the size of the triangle.',
      knowledge:
        '• Define sin θ = opposite/hypotenuse, cos θ = adjacent/hypotenuse, tan θ = opposite/adjacent\n' +
        '• Explain why the ratio is constant for a fixed angle regardless of triangle size\n' +
        '• State the relationship tan θ = sin θ / cos θ',
      skills:
        '• Measure right triangles of different sizes with the same angle and calculate the three ratios\n' +
        '• Construct a ratio table for angles 10°, 20°, 30°, 40°, 45°, 50°, 60°, 70°, 80°\n' +
        '• Apply the definitions to find unknown sides',
      attitudes:
        '• Wonder at the consistency of ratios — that size does not change the ratio\n' +
        '• Appreciation of the power of a simple definition',
      keyInquiry: 'What is trigonometry? How do we use trigonometry in real-life situations?',
      purposeInStoryline:
        'The three definitions are the mathematical engine of the unit. ' +
        'Deriving them from physical measurement ensures students understand them — not just memorise them.',
      safetyNotes: 'No specific safety notes.',
    },
    overview:
      'Teacher draws three different-sized right triangles on the board, all with the same angle θ = 40°. ' +
      'Students measure the sides of each and calculate opposite/hypotenuse for each. Discovery: the ratio ' +
      'is always the same (~0.643) regardless of triangle size. This is the definition of sin 40°.\n\n' +
      'Groups then construct a ratio table: draw right triangles for each angle, measure sides, calculate ' +
      'all three ratios. They compare their values to a calculator — confirming their experimental ratios.',
    framework: [
      {
        phase: 'Predict Phase',
        learnerExperience:
          '"I have two right triangles — both have an angle of 40°, but one is twice as large as the other. ' +
          'Will the ratio opposite/hypotenuse be the same or different? Predict and justify."',
        resource: 'MATERIAL: Two printed right triangles (same angle, different sizes)',
        teacherMoves: '"What do you know about similar triangles? If two triangles are similar, what is true about their ratios?"',
        sensemakingStrategy: 'Prediction connects to prior knowledge of similar triangles. Cognitive investment in the invariance result.',
        formativeAssessment: 'Do students predict the same ratio? This checks understanding of similarity.',
      },
      {
        phase: 'Observe Phase',
        learnerExperience:
          '1. Measure sides of three printed right triangles (all 40°): small, medium, large.\n' +
          '2. Calculate opposite/hypotenuse for each. Record.\n' +
          '3. Calculate adjacent/hypotenuse for each. Record.\n' +
          '4. Calculate opposite/adjacent for each. Record.\n' +
          '5. Compare the three values in each column — are they the same?',
        resource:
          'MATERIAL: Printed right triangle sheets (3 sizes, θ = 40°), rulers, calculators\n' +
          'RESULT: All three ratio columns should be approximately constant (~0.643, ~0.766, ~0.839)',
        teacherMoves:
          '"Small differences between rows are measurement error — the TRUE value is constant. Why?"\n' +
          '"Give these three ratios names: the first is called the SINE of 40°. The second is the COSINE. The third is the TANGENT."',
        sensemakingStrategy:
          'Empirical discovery of ratio invariance. Students NAME the ratios after discovering them — not before.',
        formativeAssessment:
          'Are ratios approximately equal across triangle sizes? Large variation (>0.02) indicates measurement error.',
      },
      {
        phase: 'Explain Phase',
        learnerExperience:
          'Formally define: sin θ = opp/hyp; cos θ = adj/hyp; tan θ = opp/adj. ' +
          'Derive: tan θ = sin θ / cos θ (from definitions).\n' +
          'Now apply to Lesson 1 flagpole data: ' +
          '"You measured θ and d (adjacent). You want height h (opposite). Which ratio connects opp and adj?"\n' +
          '→ tan θ = h/d → h = d × tan θ. Calculate the flagpole height.',
        resource:
          'MATERIAL: Lesson 1 flagpole data; calculators\n' +
          'MNEMONIC: SOH-CAH-TOA (optional: discuss cultural mnemonics, e.g., "Sokrates" in Swahili memory rhyme)',
        teacherMoves:
          '"tan θ = opposite/adjacent = height/distance. Rearrange to find height: h = d × tan θ."\n' +
          '"Now solve the KeNHA bridge: 62° elevation from 30 m. h = 30 × tan 62° = 30 × 1.880 = 56.4 m."',
        sensemakingStrategy:
          'Immediate application to Lesson 1 data closes the loop — students see the purpose was real.',
        formativeAssessment:
          'Can students correctly identify which ratio to use (tan) given adjacent and opposite? ' +
          'Common error: using sin when adjacent is known (not hypotenuse).',
      },
      {
        phase: 'Driving Question Board (DQB) Creation',
        learnerExperience:
          'Update DQB. "Ratios" questions are now answered. New questions: ' +
          '"Are there angles where sin and cos are the same?" "What happens at 90°?" "Can sin be greater than 1?"',
        resource: 'MATERIAL: DQB board',
        teacherMoves: '"The \'same sin and cos\' question is answered in Lesson 4. The \'sin > 1?\' question is explored in Lesson 5."',
        sensemakingStrategy: 'DQB continues to build curiosity.',
        formativeAssessment: 'New questions show students are thinking beyond definitions.',
      },
      {
        phase: 'Model Building Phase',
        learnerExperience:
          'Update Model: Add the three ratio definitions with the SOH-CAH-TOA triangle diagram. ' +
          'Add the flagpole calculation with all steps shown. Add the KeNHA bridge solution.',
        resource: 'MATERIAL: Model Journal page (Lesson 2 revision)',
        teacherMoves: '"Your model now has the formula. Does your initial prediction (Lesson 1) match?"',
        sensemakingStrategy: 'Model revision shows transition from prediction to defined knowledge.',
        formativeAssessment: 'Are definitions written correctly? Are opposite/adjacent relative to the angle (not the right angle)?',
      },
    ],
    teacherReflection:
      'After teaching this lesson, reflect on:\n\n' +
      '1. Did students genuinely discover the ratio invariance, or did they already know it? How did this affect the lesson dynamic?\n\n' +
      '2. Measurement error in ratio tables: how large was the variation? Did any group have ratios that differed by >0.05?\n\n' +
      '3. Identifying which ratio to use (sin/cos/tan): this is the most persistent error. What teaching move helped most?\n\n' +
      '4. KeNHA bridge calculation: did students understand why tan was used and not sin or cos?\n\n' +
      '5. DQB new questions: are students starting to think about edge cases (90°, complementary angles)?\n\n' +
      '6. How should you structure Lesson 3 (tables/calculators) given what you observed today?',
    summaryTablePrompt: {
      observed:
        'Measured sides of three right triangles — all with angle 40°, different sizes. ' +
        'Calculated opposite/hypotenuse for each: approximately 0.643 in every case. Same for adj/hyp (~0.766) and opp/adj (~0.839). ' +
        'Applied tan θ = opposite/adjacent to calculate flagpole height from Lesson 1 data.',
      learned:
        'Three trigonometric ratio definitions: sin θ = opp/hyp; cos θ = adj/hyp; tan θ = opp/adj. ' +
        'The ratio depends ONLY on the angle — not the size of the triangle. ' +
        'tan θ = sin θ / cos θ. ' +
        'To find an unknown side: choose the ratio that involves the known side and unknown side, then rearrange.',
      explained:
        'KeNHA bridge: 62° elevation, 30 m distance. tan 62° = height/30 → height = 30 × 1.880 = 56.4 m. ' +
        'The surveyor calculates the bridge column height without touching it — just one angle and one distance. ' +
        'That is the power of trigonometry.',
    },
  },

  // ── LESSON 3 ──────────────────────────────────────────────────────────────
  {
    number: 3,
    aresKeywords: 'trigonometry unknown sides right triangle',
    title:    'Using Mathematical Tables and Calculators',
    duration: '40 minutes',
    slo: {
      purpose:
        'Students learn to find trigonometric ratios accurately using mathematical tables and calculators, ' +
        'applying them to solve for unknown sides and angles.',
      knowledge:
        '• Explain how to read trigonometric values from four-figure mathematical tables\n' +
        '• State the inverse functions: sin⁻¹, cos⁻¹, tan⁻¹ (arcsin, arccos, arctan)\n' +
        '• Identify whether to use the ratio or its inverse based on what is known',
      skills:
        '• Use four-figure tables to find sin, cos, and tan values to 4 decimal places\n' +
        '• Use a calculator to find trigonometric ratios and inverse functions\n' +
        '• Solve right triangles given two sides or one side and one angle',
      attitudes:
        '• Responsibility: careful handling of mathematical tables\n' +
        '• Appreciation of the precision that tables and calculators provide',
      keyInquiry: 'How do we use trigonometry in real-life situations?',
      purposeInStoryline:
        'Tables and calculators unlock any angle — not just the ones students measured in Lesson 2. ' +
        'This lesson also introduces the inverse operation (finding the angle from a ratio).',
      safetyNotes: 'Handle mathematical table booklets carefully — do not write in them.',
    },
    overview:
      'Teacher demonstrates reading sin 27.4° from four-figure tables (main table + difference columns). ' +
      'Students practise reading 12 values. Then calculator use: MODE → sin/cos/tan key → angle. ' +
      'Inverse functions: if sin θ = 0.726, then θ = sin⁻¹(0.726).\n\n' +
      'Students solve six mixed problems: find unknown side (using ratio) and find unknown angle ' +
      '(using inverse ratio). Context problems drawn from KeNHA bridges, Nairobi building heights, ' +
      'and Mombasa lighthouse angles of depression.',
    framework: [
      {
        phase: 'Predict Phase',
        learnerExperience:
          '"In Lesson 2, you built a ratio table for 40°. Can you predict sin 62° without measuring a triangle? ' +
          'What do you expect its value to be — close to 0 or close to 1? Why?"',
        resource: 'MATERIAL: Lesson 2 ratio table (from student models)',
        teacherMoves: '"Looking at your table: as the angle increases from 0° to 90°, what happens to sin θ?"',
        sensemakingStrategy:
          'Pattern extrapolation from Lesson 2 data. Students expect sin to increase toward 1 as angle approaches 90°.',
        formativeAssessment:
          'Do students predict sin 62° ≈ 0.88? They should expect a high value (>0.8) based on their table patterns.',
      },
      {
        phase: 'Observe Phase',
        learnerExperience:
          'Four-figure table practice:\n' +
          '1. Teacher demonstrates reading sin 27.4°: find row 27, column 4 = 0.4602.\n' +
          '2. Reading to more decimal places: use difference column for 27.43° etc.\n' +
          '3. Students read 6 values from tables independently.\n' +
          'Calculator practice:\n' +
          '4. Enter: [sin] [62] [=] → 0.8829.\n' +
          '5. Find sin 27.4° on calculator → compare to table value.\n' +
          '6. Find θ: sin θ = 0.726 → [shift] [sin] [0.726] [=] → 46.6°.',
        resource:
          'MATERIAL: Four-figure mathematical tables booklets (one per student), scientific calculators\n' +
          'NOTE: Students should know their calculator\'s degree/radian mode — always use DEGREE mode here',
        teacherMoves:
          '"The table gives four significant figures — that is enough for all our calculations."\n' +
          '"The inverse key on your calculator may be labelled arcsin, sin⁻¹, or SHIFT sin — check your model."',
        sensemakingStrategy:
          'Calculator confirms table values — students trust both tools. Inverse function introduced naturally from a calculation need.',
        formativeAssessment:
          'Are students reading tables correctly? Common error: reading the wrong row/column. ' +
          'Check sin 35° = 0.5736 (not 0.5 — confusing with exactly 30°).',
      },
      {
        phase: 'Explain Phase',
        learnerExperience:
          'Six mixed problems (3 find-the-side, 3 find-the-angle):\n' +
          '• P1: Right triangle, θ = 38°, hyp = 15 m. Find opposite. (15 sin 38° = 9.23 m)\n' +
          '• P2: θ = 55°, adj = 7 m. Find hypotenuse. (7/cos 55° = 12.2 m)\n' +
          '• P3: opp = 9, hyp = 14. Find θ. (sin⁻¹(9/14) = 40.0°)\n' +
          '• P4–P6: Context problems (bridge, building, lighthouse)\n' +
          'For each: (1) draw the triangle, (2) label sides, (3) choose ratio, (4) solve, (5) check reasonableness.',
        resource:
          'MATERIAL: Problem worksheet (6 problems), calculators\n' +
          'CONTEXT: KeNHA bridge, Nairobi building, Mombasa lighthouse',
        teacherMoves:
          '"The five steps are NON-NEGOTIABLE — drawing the triangle is not optional. It is how you choose the right ratio."\n' +
          '"Is your answer reasonable? A bridge column of 560 m is impossible — you have made an error somewhere."',
        sensemakingStrategy:
          'Five-step method as a consistent procedure. Reasonableness checking builds mathematical judgment.',
        formativeAssessment:
          'P1–P3 accuracy; also check: do students draw and label the triangle (not just compute)?',
      },
      {
        phase: 'Driving Question Board (DQB) Creation',
        learnerExperience:
          'Update DQB. Move "tables/calculators" questions to ANSWERED. ' +
          'Review: "Are there angles where sin and cos are the same?" — preview for Lesson 4.',
        resource: 'MATERIAL: DQB board',
        teacherMoves: '"Lesson 4 answers the complementary angles question. Look at your table — what do you notice about sin 40° and cos 50°?"',
        sensemakingStrategy: 'Directed observation in the DQB creates anticipation for Lesson 4.',
        formativeAssessment: 'Do students notice that sin 40° = cos 50° from their Lesson 2 table?',
      },
      {
        phase: 'Model Building Phase',
        learnerExperience:
          'Update Model: add the five-step problem-solving procedure. ' +
          'Add the inverse function concept with a worked example.',
        resource: 'MATERIAL: Model Journal page (Lesson 3 revision)',
        teacherMoves: '"Your model is now a complete problem-solving toolkit for right triangles."',
        sensemakingStrategy: 'Model captures the procedural knowledge developed today.',
        formativeAssessment: 'Do models include both forward (find side) and inverse (find angle) operations?',
      },
    ],
    teacherReflection:
      'After teaching this lesson, reflect on:\n\n' +
      '1. Four-figure tables: did students find the reading process confusing? What was the most common error (wrong row, wrong column, difference column)?\n\n' +
      '2. Calculator degree/radian mode: did any student accidentally work in radians? How did you diagnose this?\n\n' +
      '3. Reasonableness checking: did students spontaneously check their answers, or only when prompted?\n\n' +
      '4. Did students draw the right triangle for every problem, or did some try to identify the ratio without a diagram?\n\n' +
      '5. Context problems (bridge, building, lighthouse): did the Kenyan contexts add relevance?\n\n' +
      '6. Are students ready for the abstract complementary angle relationship in Lesson 4?',
    summaryTablePrompt: {
      observed:
        'Read trigonometric values from four-figure mathematical tables for angles including 27.4°, 35°, 62°. ' +
        'Confirmed values on scientific calculator. Used inverse functions to find angles from ratios. ' +
        'Solved 6 mixed problems (find side + find angle) using five-step method.',
      learned:
        'Four-figure tables and calculators give trig ratios to 4 decimal places for any angle. ' +
        'Inverse function (sin⁻¹, cos⁻¹, tan⁻¹) finds the angle from a known ratio. ' +
        'Five-step method: draw triangle → label sides → choose ratio → solve equation → check reasonableness.',
      explained:
        'A KeNHA engineer can now find ANY height or distance in ANY right-triangle situation — ' +
        'not just the angles in our Lesson 2 table. ' +
        'As long as one side and one acute angle are known (or two sides), the full triangle can be solved.',
    },
  },

  // ── LESSON 4 ──────────────────────────────────────────────────────────────
  {
    number: 4,
    aresKeywords: 'trigonometry unknown angles inverse sine cosine',
    title:    'Complementary Angles — Sin and Cos Are Partners',
    duration: '40 minutes',
    slo: {
      purpose:
        'Students discover and explain the complementary angle relationship: sin θ = cos(90° − θ).',
      knowledge:
        '• State that sin θ = cos(90° − θ) and cos θ = sin(90° − θ)\n' +
        '• Explain the relationship using a right triangle with angles θ and (90° − θ)\n' +
        '• Apply the relationship to simplify trigonometric expressions and equations',
      skills:
        '• Verify the relationship for multiple angles using tables or calculators\n' +
        '• Apply the relationship to find unknown angles and simplify expressions\n' +
        '• Identify complementary angle pairs',
      attitudes:
        '• Appreciation of the elegant symmetry in mathematics\n' +
        '• Curiosity about why two seemingly different ratios are actually related',
      keyInquiry: 'What is trigonometry?',
      purposeInStoryline:
        'The complementary angle relationship completes students\' understanding of why sin and cos are paired. ' +
        'It also simplifies many calculation shortcuts — essential for Lesson 5 (special angles).',
      safetyNotes: 'No specific safety notes.',
    },
    overview:
      'Students look at their Lesson 2 ratio table and a standard trig table side-by-side. ' +
      'Teacher asks: "Compare sin 30° and cos 60°. Compare sin 40° and cos 50°. What do you notice?" ' +
      'After the pattern emerges, students draw a right triangle with angles θ and (90°−θ) and prove algebraically ' +
      'why sin θ = cos(90°−θ) — the "opposite" for θ is the "adjacent" for (90°−θ).\n\n' +
      'Application: if sin 72° = cos ?, solve equations like cos(2x+10°) = sin(3x−5°).',
    framework: [
      {
        phase: 'Predict Phase',
        learnerExperience:
          '"Without looking at any table: predict whether sin 30° equals cos 60°. ' +
          'Then predict: sin 25° = cos ?. Explain your reasoning."',
        resource: 'MATERIAL: Lesson 2 ratio table (student models)',
        teacherMoves: '"Look at your ratio table from Lesson 2. Find sin 40° and cos 50°. What do you observe?"',
        sensemakingStrategy: 'Data-driven prediction from Lesson 2 activates the pattern before formal proof.',
        formativeAssessment: 'Do students predict sin 25° = cos 65°? Can they generalise to any pair that adds to 90°?',
      },
      {
        phase: 'Observe Phase',
        learnerExperience:
          'Check 6 complementary pairs using calculator:\n' +
          '(30°, 60°), (25°, 65°), (48°, 42°), (71°, 19°), (5°, 85°), (45°, 45°)\n' +
          'Record: sin θ = ?, cos(90°−θ) = ?\n' +
          'For each pair: are the values equal?\n' +
          'Key observation: when θ = 45°, sin 45° = cos 45° — they ARE equal!',
        resource:
          'MATERIAL: Calculators, recording table\n' +
          'KEY RESULT: sin 45° = cos 45° = 0.7071... → previews the special angles in Lesson 5',
        teacherMoves:
          '"The 45° case is special — what does it mean that sin 45° = cos 45°?"\n' +
          '"Can you explain WHY this relationship holds for EVERY angle? Think about the triangle."',
        sensemakingStrategy:
          'Systematic verification across many pairs. The 45° special case creates a bridge to Lesson 5.',
        formativeAssessment: 'Are all six pairs confirmed equal? Does the 45° case surprise students?',
      },
      {
        phase: 'Explain Phase',
        learnerExperience:
          'Triangle proof:\n' +
          '1. Draw right triangle with angles θ, (90°−θ), and 90°.\n' +
          '2. Label sides: opposite to θ = a; adjacent to θ = b; hypotenuse = c.\n' +
          '3. sin θ = a/c (opposite/hyp for angle θ)\n' +
          '4. For angle (90°−θ): opposite = b, adjacent = a, hypotenuse = c.\n' +
          '   cos(90°−θ) = adjacent to (90°−θ) / hyp... wait — adjacent to (90°−θ) = a.\n' +
          '   cos(90°−θ) = a/c = sin θ ✓\n' +
          'Application problems: find x if sin(3x+10°) = cos(x+20°). → 3x+10° + x+20° = 90° → 4x = 60° → x = 15°.',
        resource: 'MATERIAL: Whiteboard, problem worksheet',
        teacherMoves:
          '"The key step: what is \'adjacent to angle (90°−θ)\'? It is the OPPOSITE to angle θ — same side, different label!"\n' +
          '"sin(A) = cos(B) means A + B = 90°. Use that to solve equations."',
        sensemakingStrategy:
          'Geometric proof makes the relationship logical, not magical. ' +
          'Equation-solving applies the relationship in a new context.',
        formativeAssessment:
          'Can students solve: sin(3x+10°) = cos(x+20°)? Correct: x = 15°. ' +
          'Common error: not using the "sum = 90°" property correctly.',
      },
      {
        phase: 'Driving Question Board (DQB) Creation',
        learnerExperience:
          'Update DQB. "Complementary angles" question answered. ' +
          'New question: "Are sin 30° = ½ and cos 60° = ½ exact values, or approximate?" ' +
          'Preview for Lesson 5.',
        resource: 'MATERIAL: DQB board',
        teacherMoves: '"Lesson 5 derives EXACT values for special angles — no calculator needed."',
        sensemakingStrategy: 'DQB preview builds anticipation for exact-value work.',
        formativeAssessment: 'Students should be curious about exact values after seeing sin 45° = 0.7071 (irrational).',
      },
      {
        phase: 'Model Building Phase',
        learnerExperience:
          'Update Model: add the complementary angle relationship with the triangle proof diagram. ' +
          'Add a summary: "sin θ = cos(90°−θ); applies to ALL acute angles."',
        resource: 'MATERIAL: Model Journal page (Lesson 4 revision)',
        teacherMoves: '"Does your model now explain WHY sin and cos are called co-sine? Co = complement."',
        sensemakingStrategy: 'Etymology of "cosine" (complement of sine) adds depth — model becomes richer.',
        formativeAssessment: 'Does the model show the proof diagram with both angles labelled?',
      },
    ],
    teacherReflection:
      'After teaching this lesson, reflect on:\n\n' +
      '1. Did students discover the pattern from their Lesson 2 tables before you asked, or only when directed?\n\n' +
      '2. The triangle proof — did students follow the "same side, different label" argument (adjacent to one angle = opposite to the other)?\n\n' +
      '3. Solving equations: sin(3x+10°) = cos(x+20°). Did students know to set the sum of angles to 90°?\n\n' +
      '4. The 45° special case (sin = cos): did students connect this to an isosceles right triangle?\n\n' +
      '5. Etymology of "cosine": did this historical note help students remember the relationship?\n\n' +
      '6. Are students ready for the exact-value derivations in Lesson 5?',
    summaryTablePrompt: {
      observed:
        'Compared sin and cos values for complementary pairs (e.g., sin 40° and cos 50°) — always equal. ' +
        'Discovered sin 45° = cos 45°. Drew a right triangle with angles θ and (90°−θ) and proved algebraically that sin θ = cos(90°−θ). ' +
        'Solved equations using sin(A) = cos(B) → A + B = 90°.',
      learned:
        'sin θ = cos(90°−θ) for all acute angles θ. Proof: in a right triangle, the "opposite" for angle θ is the "adjacent" for angle (90°−θ). ' +
        'Cosine is literally the "complement-sine" — the sine of the complementary angle. ' +
        'Special case: sin 45° = cos 45° (the only angle equal to its own complement).',
      explained:
        'The complementary relationship is a hidden symmetry in every right triangle. ' +
        'It means a surveyor\'s angle of elevation (θ) and angle of depression (90°−θ) are mathematically linked — ' +
        'sin and cos swap roles. This is why the KeNHA engineer only needs ONE table instead of two.',
    },
  },

  // ── LESSON 5 ──────────────────────────────────────────────────────────────
  {
    number: 5,
    aresKeywords: 'angles elevation depression trigonometry',
    title:    'Trigonometric Ratios of Special Angles: 30°, 45°, 60°, 90°',
    duration: '40 minutes',
    slo: {
      purpose:
        'Students derive exact values of trigonometric ratios for 30°, 45°, 60°, and 90° using two special triangles, ' +
        'without relying on tables or calculators.',
      knowledge:
        '• Derive sin 30° = ½, cos 30° = √3/2, tan 30° = 1/√3 from an equilateral triangle\n' +
        '• Derive sin 45° = cos 45° = 1/√2 from an isosceles right triangle\n' +
        '• State sin 90° = 1, cos 90° = 0, tan 90° = undefined',
      skills:
        '• Construct the two special triangles and derive the exact values\n' +
        '• Apply exact values to solve problems without a calculator\n' +
        '• Simplify expressions involving exact trig values',
      attitudes:
        '• Appreciation of the elegance of exact values — irrational numbers tell precise truths\n' +
        '• Confidence to work with surds (√2, √3) without a calculator',
      keyInquiry: 'What is trigonometry?',
      purposeInStoryline:
        'Exact values are the deepest part of the unit. They connect trigonometry to geometry (equilateral triangle, isosceles right triangle) ' +
        'and to surd arithmetic. Students see that mathematics can be exact where technology is approximate.',
      safetyNotes: 'No specific safety notes.',
    },
    overview:
      'Teacher introduces the two special triangles:\n' +
      'Triangle 1: equilateral triangle, side 2 — bisect it to get a 30-60-90 triangle with sides 1, √3, 2.\n' +
      'Triangle 2: isosceles right triangle, legs 1 — hypotenuse = √2.\n\n' +
      'Students derive all six values from first principles, then complete a Special Angles table. ' +
      'Applications: "A construction ramp makes a 30° angle with the ground. For every 1 m of horizontal distance, ' +
      'how high does it rise?" (tan 30° = 1/√3 — exact answer, no calculator.)',
    framework: [
      {
        phase: 'Predict Phase',
        learnerExperience:
          '"Without a calculator: what do you think sin 30° is? What is sin 90°? What is tan 90°? Predict and justify." ' +
          'Students recall: sin 90° should be 1 (maximum), tan 90° should be very large (→ undefined).',
        resource: 'MATERIAL: Lesson 2 ratio table',
        teacherMoves:
          '"Look at your Lesson 2 table: as the angle increases, sin increases. At 90° it should be ___?"\n' +
          '"What is tan 80°? What is tan 89°? What do you predict tan 90° will be? Does it even exist?"',
        sensemakingStrategy: 'Limit reasoning from table patterns. Builds intuition for boundary cases.',
        formativeAssessment: 'Do students correctly predict sin 90° = 1 and tan 90° → undefined? Why is it undefined?',
      },
      {
        phase: 'Observe Phase',
        learnerExperience:
          'Group construction (per KICD Core Competency — Unity):\n' +
          'Triangle 1 (30-60-90):\n' +
          '• Draw equilateral triangle, side = 2 cm.\n' +
          '• Draw the bisector of one vertex — creates two 30-60-90 right triangles.\n' +
          '• Bisector length = √(2²−1²) = √3 cm.\n' +
          '• Sides: hyp = 2, short leg = 1, long leg = √3.\n' +
          'Triangle 2 (45-45-90):\n' +
          '• Draw isosceles right triangle, legs = 1 cm.\n' +
          '• Hypotenuse = √(1²+1²) = √2 cm.\n' +
          'Derive all values for 30°, 60°, 45° from these triangles.',
        resource:
          'MATERIAL: Rulers, compasses (or set squares for 60°/45°), plain paper\n' +
          'RECALL: Pythagorean theorem for finding √3 and √2',
        teacherMoves:
          '"The equilateral triangle gives you 30° and 60° simultaneously — two for the price of one!"\n' +
          '"Leave your answers as exact surds: 1/√2, √3/2 — do not approximate with a calculator yet."',
        sensemakingStrategy:
          'Construction from first principles. Surds are the natural output — no approximation involved.',
        formativeAssessment:
          'Can students correctly derive the long leg of the 30-60-90 triangle as √3? ' +
          'Common error: getting the legs wrong for 30° vs 60°.',
      },
      {
        phase: 'Explain Phase',
        learnerExperience:
          'Complete the Special Angles table:\n\n' +
          '| Angle | sin    | cos    | tan    |\n' +
          '|-------|--------|--------|--------|\n' +
          '| 30°   | 1/2    | √3/2   | 1/√3   |\n' +
          '| 45°   | 1/√2   | 1/√2   | 1      |\n' +
          '| 60°   | √3/2   | 1/2    | √3     |\n' +
          '| 90°   | 1      | 0      | undef  |\n\n' +
          'Applications using exact values:\n' +
          '• A 30° ramp: for horizontal = 5 m, height = 5 × tan 30° = 5/√3 = 5√3/3 m\n' +
          '• A 45° roof pitch: for width = 8 m, height = 8 × tan 45° = 8 × 1 = 8 m\n' +
          '• A 60° ladder: for ladder = 4 m, height = 4 × sin 60° = 4 × √3/2 = 2√3 m',
        resource: 'MATERIAL: Special angles table handout, problem worksheet',
        teacherMoves:
          '"Rationalise the denominator: 1/√3 = √3/3. Kenyan exams often expect this form."\n' +
          '"Verify: tan 30° = sin 30°/cos 30° = (1/2)/(√3/2) = 1/√3. ✓"',
        sensemakingStrategy:
          'Table completion consolidates. Exact-value applications build confidence working without a calculator.',
        formativeAssessment:
          'Can students solve the ramp problem without a calculator, leaving answer in surd form? ' +
          'Correct: 5/√3 = 5√3/3.',
      },
      {
        phase: 'Driving Question Board (DQB) Creation',
        learnerExperience:
          'Update DQB. Move special angles questions to ANSWERED. ' +
          'Final remaining DQB category: "Applications — elevation and depression." Preview Lesson 6.',
        resource: 'MATERIAL: DQB board',
        teacherMoves: '"Lesson 6 is where all five lessons come together: tables, calculators, special angles, and complementary pairs."',
        sensemakingStrategy: 'DQB nearing completion signals unit convergence.',
        formativeAssessment: 'How many unanswered questions remain? Should be only application questions.',
      },
      {
        phase: 'Model Building Phase',
        learnerExperience:
          'Update Model: add the Special Angles table and the two construction triangles (30-60-90 and 45-45-90) with all labels.',
        resource: 'MATERIAL: Model Journal page (Lesson 5 revision)',
        teacherMoves: '"Your model now contains something a calculator cannot give you: exact, irrational values. That is deeper knowledge."',
        sensemakingStrategy: 'Model highlights the epistemological distinction between exact and approximate.',
        formativeAssessment: 'Does the model include both triangles with correct surd values?',
      },
    ],
    teacherReflection:
      'After teaching this lesson, reflect on:\n\n' +
      '1. Did students correctly construct the 30-60-90 triangle from an equilateral triangle? What was the hardest step?\n\n' +
      '2. Surds: are students comfortable leaving answers as 1/√3, √3/2 etc.? Or do they immediately approximate?\n\n' +
      '3. Rationalising the denominator (1/√3 = √3/3): is this a revision topic or new for most students?\n\n' +
      '4. The 45-45-90 triangle: did students connect this to the complementary angle discovery in Lesson 4?\n\n' +
      '5. tan 90° = undefined: did students understand the conceptual reason (opposite side would be infinite)?\n\n' +
      '6. How will you incorporate exact values into the Lesson 6 applications?',
    summaryTablePrompt: {
      observed:
        'Constructed a 30-60-90 triangle from a bisected equilateral triangle (sides 1, √3, 2). ' +
        'Constructed a 45-45-90 triangle from an isosceles right triangle (sides 1, 1, √2). ' +
        'Derived and tabulated exact trig values for 30°, 45°, 60°, 90°.',
      learned:
        'Exact values: sin 30° = ½, cos 30° = √3/2, tan 30° = 1/√3 (= √3/3); ' +
        'sin 45° = cos 45° = 1/√2 (= √2/2), tan 45° = 1; ' +
        'sin 60° = √3/2, cos 60° = ½, tan 60° = √3; sin 90° = 1, cos 90° = 0, tan 90° = undefined. ' +
        'No calculator needed for these angles.',
      explained:
        'A KeNHA engineer designing a 30° access ramp under a bridge gets the exact height: 5/√3 = 5√3/3 m — ' +
        'more precise than any calculator answer. Exact values are the pinnacle of trigonometric knowledge — ' +
        'derived from geometry, not technology.',
    },
  },

  // ── LESSON 6 ──────────────────────────────────────────────────────────────
  {
    number: 6,
    aresKeywords: 'trigonometry applications real life Kenya',
    title:    'Angles of Elevation and Depression — Solving the KeNHA Challenge',
    duration: '40 minutes',
    slo: {
      purpose:
        'Students apply all unit knowledge to angles of elevation and depression in real Kenyan contexts, ' +
        'and write their final explanation.',
      knowledge:
        '• Define angle of elevation (measured upward from horizontal) and angle of depression (measured downward from horizontal)\n' +
        '• State that angle of elevation from A to B = angle of depression from B to A (alternate angles)\n' +
        '• Explain the five-step method for solving elevation/depression problems',
      skills:
        '• Solve multi-step problems involving angles of elevation and depression\n' +
        '• Use exact values (special angles) and calculated values (tables/calculator) as appropriate\n' +
        '• Calculate heights of buildings, mountains, towers using measured angles and distances',
      attitudes:
        '• Confidence to solve real-world measurement problems independently\n' +
        '• Pride in applying school mathematics to professional engineering contexts',
      keyInquiry: 'How do we use trigonometry in real-life situations?',
      purposeInStoryline:
        'Unit closure. The KeNHA challenge (introduced Lesson 1) is now fully solved. ' +
        'The final explanation closes the driving question with evidence from all six lessons.',
      safetyNotes: 'No specific safety notes.',
    },
    overview:
      'The lesson opens by returning to the KeNHA bridge problem from Lesson 1. ' +
      'Students now solve it completely, showing all five steps. ' +
      'They then encounter a new challenge: two angles of elevation from different distances ' +
      '(a two-step problem requiring simultaneous equations or the tan subtraction formula).\n\n' +
      'Second half: students compare their Lesson 1 and Lesson 6 models and write their Final Explanation.',
    framework: [
      {
        phase: 'Predict Phase',
        learnerExperience:
          '"KeNHA problem from Lesson 1: angle of elevation = 62°, horizontal distance = 30 m. ' +
          'Before calculating — which ratio connects opposite (height) and adjacent (30 m)? ' +
          'What is your prediction for the height? Show reasoning."',
        resource: 'MATERIAL: Lesson 1 KeNHA photograph',
        teacherMoves:
          '"You have had 5 lessons to prepare for this. Which ratio? Which five steps? Go."',
        sensemakingStrategy: 'Closing the loop: the Lesson 1 problem is now fully solvable. Creates a satisfying sense of completion.',
        formativeAssessment: 'Can students immediately identify tan as the correct ratio without prompting?',
      },
      {
        phase: 'Observe Phase',
        learnerExperience:
          'Full solution of KeNHA problem:\n' +
          '1. Draw: right triangle, adjacent = 30 m, angle = 62°, opposite = h (unknown).\n' +
          '2. Label: opp = h, adj = 30, angle θ = 62°.\n' +
          '3. Choose ratio: tan θ = opp/adj → tan 62° = h/30.\n' +
          '4. Solve: h = 30 × tan 62° = 30 × 1.8807 = 56.4 m.\n' +
          '5. Check: reasonable for a bridge support column ✓.\n\n' +
          'Extension — angle of depression:\n' +
          'A lighthouse keeper at height 56.4 m looks down at a boat. Angle of depression = 28°. ' +
          'How far from the lighthouse base is the boat?\n' +
          '(Angle of depression = 28° → angle of elevation from boat = 28° (alternate). ' +
          'tan 28° = 56.4/d → d = 56.4/tan 28° = 56.4/0.5317 = 106 m.)',
        resource:
          'MATERIAL: KeNHA photograph; problem worksheet\n' +
          'NOTE: angle of elevation and angle of depression are alternate interior angles → equal',
        teacherMoves:
          '"The angle of depression from the lighthouse = the angle of elevation from the boat. Why? (Parallel horizontal lines, alternate angles.)"\n' +
          '"The bridge height 56.4 m is the same as the lighthouse height in the extension — I did that intentionally."',
        sensemakingStrategy:
          'The extension reuses the bridge height — students see how one answer feeds into the next problem. ' +
          'Alternate angles connection links trigonometry to geometry.',
        formativeAssessment:
          'Bridge: h = 56.4 m. Lighthouse boat: d = 106 m. ' +
          'Common error: confusing angle of depression with angle from vertical.',
      },
      {
        phase: 'Explain Phase',
        learnerExperience:
          'Three challenge problems:\n' +
          '• P1 (exact values): A 45° angle of elevation from 12 m. Find height. (12 × tan 45° = 12 × 1 = 12 m)\n' +
          '• P2 (complementary): Angle of elevation from A = 30°, from B (10 m closer) = 60°. Find height.\n' +
          '  (Two-equation system: h = d × tan 30° = (d−10) × tan 60°. Solve: d = 15, h = 15/√3 = 5√3 m)\n' +
          '• P3 (your data): Use the clinometer measurement from Lesson 1 to find the actual height of the school flagpole.\n' +
          'Present P2 and P3 solutions to the class.',
        resource:
          'MATERIAL: Problem worksheet; Lesson 1 clinometer data\n' +
          'DIGITAL: GeoGebra for P2 verification (optional)',
        teacherMoves:
          '"P2 uses both Lesson 5 (exact values for 30° and 60°) and algebra (simultaneous equations). It is the hardest problem we have done. Take your time."\n' +
          '"P3 is YOUR data — there is no \'right answer\' in the textbook. Does your answer match the actual flagpole height?"',
        sensemakingStrategy:
          'P2 integrates all unit content. P3 connects to Lesson 1 — completing the full unit circle.',
        formativeAssessment:
          'P1: trivial (12 m). P2: h = 5√3 ≈ 8.66 m. P3: varies by class data. ' +
          'Check P2 method — did students set up two equations correctly?',
      },
      {
        phase: 'Driving Question Board (DQB) Creation',
        learnerExperience:
          'Final DQB: all questions answered. Class writes one-sentence answers to the driving question. ' +
          'Best answer displayed permanently.',
        resource: 'MATERIAL: DQB board, class wall display space',
        teacherMoves: '"Six lessons ago we couldn\'t find the height of a column. Today we solved a two-stage lighthouse problem using only angles and one distance. Write that growth."',
        sensemakingStrategy: 'Unit narrative closed. The intellectual journey from clinometer to multi-step problems is acknowledged.',
        formativeAssessment: 'Quality of one-sentence answers shows conceptual depth.',
      },
      {
        phase: 'Model Building Phase',
        learnerExperience:
          'Final model comparison: Lesson 1 vs Lesson 6.\n' +
          '"What I thought / What I know now / Biggest surprise."\n' +
          'Begin Final Explanation draft. Must include: three ratio definitions; complementary relationship; ' +
          'special angles table; five-step procedure; at least two Kenyan contexts.',
        resource: 'MATERIAL: Model Journal (all pages), Final Explanation template',
        teacherMoves:
          '"Your Lesson 6 model should contain everything a KeNHA surveyor needs: definitions, tables, special values, and a problem-solving procedure."\n' +
          '"Does your model explain how to solve the bridge column problem step by step?"',
        sensemakingStrategy: 'Model comparison makes six-lesson learning growth visible and tangible.',
        formativeAssessment:
          'Lesson 6 model should contain: 3 ratio definitions, complementary relationship, special angles table, five-step method, angle of elevation/depression.',
      },
    ],
    teacherReflection:
      'After teaching this lesson, reflect on:\n\n' +
      '1. Did students solve the KeNHA bridge problem fluently and independently? Or was there still uncertainty about which ratio to use?\n\n' +
      '2. P2 (two-position problem): did any students set up the simultaneous equations without prompting? This is above-standard performance.\n\n' +
      '3. P3 (real flagpole): how close was the calculated height to the actual height? What sources of error were there?\n\n' +
      '4. Comparing Lesson 1 and Lesson 6 models: what was the most striking change in student thinking?\n\n' +
      '5. Alternate angles (elevation = depression from opposite end): was this link to prior geometry understood?\n\n' +
      '6. Reflecting on the full unit: which lesson had the highest engagement? Which needs the most revision for next time?',
    summaryTablePrompt: {
      observed:
        'Solved KeNHA bridge problem (tan 62° = h/30 → h = 56.4 m). ' +
        'Solved lighthouse angle of depression problem (d = 56.4/tan 28° = 106 m). ' +
        'Solved two-position elevation problem using simultaneous equations (h = 5√3 m). ' +
        'Used Lesson 1 clinometer data to calculate actual flagpole height.',
      learned:
        'Angle of elevation = measured upward from horizontal to object. ' +
        'Angle of depression = measured downward from horizontal to object. ' +
        'Angle of elevation from A to B = angle of depression from B to A (alternate angles). ' +
        'Five-step method applies to all right-triangle problems regardless of context.',
      explained:
        'COMPLETE ANSWER: Trigonometry gives surveyors, engineers, and builders in Kenya a way to measure heights and distances that are impossible to reach directly — ' +
        'using only an angle (measured with a clinometer) and a known horizontal distance. ' +
        'The three ratios (sin, cos, tan) connect angles to side lengths. ' +
        'Special angle values (30°, 45°, 60°) give exact answers. ' +
        'The complementary relationship links sin and cos. ' +
        'Together, these tools allow KeNHA engineers to build bridges, surveyors to measure Mt. Kenya, ' +
        'and students to measure their school flagpole — all without leaving the ground.',
    },
  },

]; // end LESSONS

// ─── Section builders ─────────────────────────────────────────────────────────
function overviewTable(unit) {
  const LW = 3000;
  return makeTable([
    fullHeader('SUB-STRAND OVERVIEW', C.darkBlue, 'FFFFFF', SZ_H, 2),
    labelRow('Grade Level',        unit.gradeLevel,       LW),
    labelRow('Subject',            unit.subject,          LW),
    labelRow('Strand',             unit.strand,           LW),
    labelRow('Sub-Strand',         unit.substrand,        LW),
    labelRow('Total Duration',     unit.duration,         LW),
    labelRow('Sub-Strand Content', unit.content,          LW, { labelFill: C.lightBlue }),
    labelRow('Learning Outcomes',  unit.learningOutcomes, LW, { labelFill: C.lightBlue }),
    labelRow('Core Competencies',  unit.coreCompetencies, LW, { labelFill: C.lightBlue }),
    labelRow('Core Values',        unit.values,           LW, { labelFill: C.lightGreen }),
    labelRow('PCIs',               unit.pcis,             LW, { labelFill: C.lightOrange }),
    labelRow('Key Inquiry Questions', unit.keyInquiry,    LW, { labelFill: C.lightPurple }),
    labelRow('Anchoring Phenomenon',  unit.phenomenon,    LW, { labelFill: C.lightPurple }),
    labelRow('Driving Question',   unit.drivingQuestion,  LW, { labelFill: C.lightPurple }),
    labelRow('Storyline Thread',   unit.storylineThread,  LW, { labelFill: C.lightTeal }),
  ]);
}
function secA(lesson) {
  const LW = 3000;
  return makeTable([
    fullHeader(`LESSON ${lesson.number}: ${lesson.title}`, C.darkBlue, 'FFFFFF', SZ_H, 2),
    fullHeader('A. SPECIFIC LEARNING OUTCOMES', C.teal, 'FFFFFF', SZ_H, 2),
    labelRow('Purpose',              lesson.slo.purpose,            LW, { labelFill: C.lightBlue }),
    labelRow('Knowledge',            lesson.slo.knowledge,          LW, { labelFill: C.lightBlue }),
    labelRow('Skills',               lesson.slo.skills,             LW, { labelFill: C.lightBlue }),
    labelRow('Attitudes',            lesson.slo.attitudes,          LW, { labelFill: C.lightBlue }),
    labelRow('Purpose in Storyline', lesson.slo.purposeInStoryline, LW, { labelFill: C.lightTeal }),
    labelRow('Safety Notes',         lesson.slo.safetyNotes,        LW, { labelFill: C.lightOrange }),
  ]);
}
function secB(lesson) {
  return makeTable([
    fullHeader('B. LESSON OVERVIEW', C.teal, 'FFFFFF', SZ_H, 1),
    new TableRow({ children: [cell(lesson.overview, { fill: C.white, w: W, size: SZ })] }),
  ], [W]);
}
function secC(lesson) {
  const CW = [900, 2300, 2556, 3324, 2300, 2300];
  const aresTopic = lesson.aresKeywords || lesson.title || '';
  const aresRes = getAllPhaseResources({
    substrand: lesson.substrand || 'Trigonometry 1',
    topic:     aresTopic,
    subject:   'Mathematics',
  });
  const PHASE_KEY = {
    'Predict Phase':                         'predict',
    'Observe Phase':                         'observe',
    'Explain Phase':                         'explain',
    'Driving Question Board (DQB) Creation': 'dqb',
    'Model Building Phase':                  'model',
  };
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
      cell(buildResourceParagraphs(aresRes[PHASE_KEY[f.phase] || 'observe'], f.phase),  { fill: C.grey,  w: CW[2] }),
      cell(f.teacherMoves,        { fill: C.white, w: CW[3], size: SZ }),
      cell(f.sensemakingStrategy, { fill: C.grey,  w: CW[4], size: SZ }),
      cell(f.formativeAssessment, { fill: C.white, w: CW[5], size: SZ }),
    ]})),
  ], CW);
}
function secD(lesson) {
  return makeTable([
    fullHeader('D. TEACHER REFLECTION', C.orange, 'FFFFFF', SZ_H, 1),
    new TableRow({ children: [cell(lesson.teacherReflection, { fill: C.lightOrange, w: W, size: SZ })] }),
  ], [W]);
}
function secE(lesson) {
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

// ─── Document builders ────────────────────────────────────────────────────────
async function buildSoW() {
  const body = [
    ...titleBlock('MATHEMATICS GRADE 10: TRIGONOMETRY 1',
                  'CBE Phenomenon-Driven Lesson Sequence — Sub-Strand 2.4 (6 Lessons)'),
    SPACE(), overviewTable(UNIT), SPACE(),
  ];
  for (const l of LESSONS) {
    body.push(PAGE_BREAK());
    body.push(secA(l), SPACE(), secB(l), SPACE(), secC(l), SPACE(), secD(l), SPACE(), secE(l), SPACE());
  }
  return new Document({ sections: [{ properties: { page: {
    size: { width: 12240, height: 15840, orientation: PageOrientation.LANDSCAPE },
    margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 },
  }}, children: body }] });
}
async function buildFinalExplanation() {
  const FLW = 3000, RW = Math.floor((W - FLW) / 3), RWr = W - FLW - RW * 2;
  const parts = [
    { title: 'PART 1: THREE TRIGONOMETRIC RATIOS',
      prompt: 'Define sin, cos, and tan. Draw and label a right triangle showing opposite, adjacent, and hypotenuse relative to angle θ. Show the derivation: why does tan θ = sin θ / cos θ?' },
    { title: 'PART 2: USING TABLES AND CALCULATORS',
      prompt: 'Describe the five-step method for solving a right-triangle problem. Apply it to find the height of a building if the angle of elevation is 48° from 25 m away. Show all working.' },
    { title: 'PART 3: COMPLEMENTARY ANGLES',
      prompt: 'State and prove the relationship sin θ = cos(90°−θ). Solve: if cos(2x+5°) = sin(3x−15°), find x.' },
    { title: 'PART 4: SPECIAL ANGLE VALUES',
      prompt: 'Derive the exact value of sin 60° using an equilateral triangle. Show all construction steps and the Pythagorean theorem calculation. Then find the exact length of the long leg of a 30-60-90 triangle with hypotenuse 10 cm.' },
    { title: 'PART 5: ELEVATION AND DEPRESSION',
      prompt: 'Explain the difference between angle of elevation and angle of depression. Why are they equal in magnitude for the same pair of points? Solve: a cliff is 80 m high. An observer at the top sees a boat at an angle of depression of 35°. How far is the boat from the cliff base?' },
    { title: 'PART 6: ANSWER THE DRIVING QUESTION',
      prompt: '"How do surveyors, engineers, and builders in Kenya calculate heights and distances that are impossible to measure directly?" Write your complete answer using evidence from all 6 lessons. Include the KeNHA bridge example and one other Kenyan context of your choice.' },
  ];
  const rubric = [
    ['Ratio Definitions', 'All three defined correctly with labelled triangle; tan = sin/cos derived.', 'Three definitions correct; derivation absent or partial.', 'Fewer than three definitions or incorrect labelling.'],
    ['Five-Step Method', 'All five steps applied correctly to building problem; exact answer.', 'Correct method, minor arithmetic error.', 'Fewer than five steps or incorrect ratio choice.'],
    ['Complementary Angles', 'Relationship proved from triangle; equation solved correctly (x=14°).', 'Relationship stated without proof; equation solved.', 'Relationship stated only; equation not solved.'],
    ['Special Angles', 'sin 60° = √3/2 derived with full triangle construction; long leg = 5√3 cm.', 'Value correct; derivation partially shown.', 'Value stated from memory without derivation.'],
    ['Real-World Application', 'Two Kenyan examples fully solved with all steps; elevation/depression distinction clear.', 'Two examples present; one solved fully, one partially.', 'Only one example or solution is incomplete.'],
  ];
  const body = [
    ...titleBlock('FINAL EXPLANATION: TRIGONOMETRY 1', 'Mathematics Grade 10 — Student Assessment Document'),
    SPACE(),
    makeTable([
      fullHeader('FINAL EXPLANATION: TRIGONOMETRY 1', C.darkBlue, 'FFFFFF', SZ_H, 2),
      fullHeader('Mathematics Grade 10 — Student Assessment Document', C.teal, 'FFFFFF', SZ_H, 2),
      labelRow('Student Name', '_______________________________________________', FLW),
      labelRow('Class', '_______________________________________________', FLW),
      labelRow('Date', '_______________________________________________', FLW),
    ], [FLW, W - FLW]),
    SPACE(),
    makeTable([
      fullHeader('INSTRUCTIONS', C.teal, 'FFFFFF', SZ_H, 1),
      new TableRow({ children: [cell(
        'You have completed all 6 lessons of Trigonometry 1. Write your COMPLETE EXPLANATION for the driving question:\n' +
        '"How do surveyors, engineers, and builders in Kenya calculate heights and distances that are impossible to measure directly?"\n\n' +
        'USE: Summary Table, Rotation Model, clinometer data, and all class activities.\n' +
        'MUST INCLUDE: three ratio definitions, five-step method, complementary relationship, special angles table, elevation/depression.\n' +
        'GRADING: 20 points total (rubric below).',
        { fill: C.white, w: W, size: SZ }
      )]}),
    ], [W]),
    SPACE(),
    ...parts.flatMap(p => [
      makeTable([
        fullHeader(p.title, C.medBlue, 'FFFFFF', SZ_H, 1),
        new TableRow({ children: [cell(p.prompt, { fill: C.lightBlue, w: W, size: SZ, italic: true })] }),
        new TableRow({ children: [cell('\n\n\n\n\n\n', { fill: C.white, w: W, size: SZ })] }),
      ], [W]),
      SPACE(),
    ]),
    makeTable([
      fullHeader('RUBRIC (20 points)', C.darkBlue, 'FFFFFF', SZ_H, 4),
      new TableRow({ children: [
        cell('Criterion',       { fill: C.medBlue, bold: true, color: 'FFFFFF', w: FLW, size: SZ }),
        cell('Excellent (4)',   { fill: C.medBlue, bold: true, color: 'FFFFFF', w: RW,  size: SZ }),
        cell('Proficient (3)',  { fill: C.teal,    bold: true, color: 'FFFFFF', w: RW,  size: SZ }),
        cell('Developing (1–2)',{ fill: C.medBlue, bold: true, color: 'FFFFFF', w: RWr, size: SZ }),
      ]}),
      ...rubric.map(([c, e, p, d]) => new TableRow({ children: [
        cell(c, { fill: C.lightBlue, w: FLW, size: SZ }),
        cell(e, { fill: C.white,     w: RW,  size: SZ }),
        cell(p, { fill: C.grey,      w: RW,  size: SZ }),
        cell(d, { fill: C.white,     w: RWr, size: SZ }),
      ]})),
    ], [FLW, RW, RW, RWr]),
  ];
  return new Document({ sections: [{ properties: { page: {
    size: { width: 12240, height: 15840, orientation: PageOrientation.LANDSCAPE },
    margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 },
  }}, children: body }] });
}
async function buildSummaryTable() {
  const SLW = 3000, TLW = 2400;
  const TC3 = Math.floor((W - TLW) / 3), TC3r = W - TLW - TC3 * 2;
  const body = [
    ...titleBlock('SUMMARY TABLE: TRIGONOMETRY 1', 'Mathematics Grade 10 — Teacher Reference'),
    SPACE(),
    makeTable([
      fullHeader('SUMMARY TABLE: TRIGONOMETRY 1', C.darkBlue, 'FFFFFF', SZ_H, 2),
      fullHeader('Mathematics Grade 10 — Teacher Reference (Pre-filled)', C.teal, 'FFFFFF', SZ_H, 2),
      labelRow('Sub-Strand', '2.4: Trigonometry 1', SLW),
      labelRow('Driving Question', UNIT.drivingQuestion, SLW),
    ], [SLW, W - SLW]),
    SPACE(),
    makeTable([
      new TableRow({ children: [
        cell('Lesson / Activity',                     { fill: C.darkBlue, bold: true, color: 'FFFFFF', w: TLW, size: SZ }),
        cell('What did I observe?',                   { fill: C.medBlue,  bold: true, color: 'FFFFFF', w: TC3, size: SZ }),
        cell('What did I learn?',                     { fill: C.teal,     bold: true, color: 'FFFFFF', w: TC3, size: SZ }),
        cell('How does this explain the phenomenon?', { fill: C.medBlue,  bold: true, color: 'FFFFFF', w: TC3r,size: SZ }),
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
      fullHeader('END-OF-UNIT REFLECTION QUESTIONS', C.orange, 'FFFFFF', SZ_H, 1),
      new TableRow({ children: [cell(
        '1. Can students identify which ratio (sin/cos/tan) to use given any combination of two known elements?\n\n' +
        '2. Do students understand the complementary relationship geometrically, or only as a formula?\n\n' +
        '3. Can students derive special angle values without a table (from the two triangles)?\n\n' +
        '4. Do students connect angle of elevation/depression to alternate angles from prior geometry?\n\n' +
        '5. How accurate were students\' real flagpole measurements (Lesson 1 → Lesson 6 comparison)?\n\n' +
        '6. Which lesson had the most authentic engagement? What drove that engagement?',
        { fill: C.lightOrange, w: W, size: SZ }
      )]}),
    ], [W]),
  ];
  return new Document({ sections: [{ properties: { page: {
    size: { width: 12240, height: 15840, orientation: PageOrientation.LANDSCAPE },
    margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 },
  }}, children: body }] });
}

// ─── HTML ─────────────────────────────────────────────────────────────────────
function buildHTML() {
  const hex = c => `#${c}`;
  const esc = s => (s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  const n2b = s => esc(s).replace(/\n/g, '<br>');
  const pc = { 'Predict Phase': hex(C.lightPurple), 'Observe Phase': hex(C.lightTeal),
    'Explain Phase': hex(C.lightGreen), 'Driving Question Board (DQB) Creation': hex(C.lightOrange),
    'Model Building Phase': hex(C.lightBlue) };
  let h = `<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n` +
    `<title>Math 2.4: Trigonometry 1 — CBE Lesson Sequence</title>\n<style>\n` +
    `body{font-family:Arial,sans-serif;font-size:11px;color:#222;max-width:1400px;margin:0 auto;padding:20px}\n` +
    `h1{color:${hex(C.darkBlue)};text-align:center;font-size:20px;margin-bottom:4px}\n` +
    `h2{color:${hex(C.teal)};text-align:center;font-size:14px;margin-top:0}\n` +
    `table{width:100%;border-collapse:collapse;margin-bottom:16px}\n` +
    `th,td{border:1px solid #ccc;padding:6px 8px;vertical-align:top;font-size:11px}\n` +
    `.hd{background:${hex(C.darkBlue)};color:white;font-weight:bold;text-align:center}\n` +
    `.ht{background:${hex(C.teal)};color:white;font-weight:bold;text-align:center}\n` +
    `.hb{background:${hex(C.medBlue)};color:white;font-weight:bold}\n` +
    `.ho{background:${hex(C.orange)};color:white;font-weight:bold;text-align:center}\n` +
    `.hp{background:${hex(C.purple)};color:white;font-weight:bold;text-align:center}\n` +
    `.lb{background:${hex(C.lightBlue)};font-weight:bold}\n` +
    `.lg{background:${hex(C.lightGreen)};font-weight:bold}\n` +
    `.lo{background:${hex(C.lightOrange)};font-weight:bold}\n` +
    `.lp{background:${hex(C.lightPurple)};font-weight:bold}\n` +
    `.lt{background:${hex(C.lightTeal)};font-weight:bold}\n` +
    `.bg{background:${hex(C.grey)}}\n` +
    `.bgo{background:${hex(C.lightOrange)}}\n` +
    `.bgp{background:${hex(C.lightPurple)}}\n` +
    `.pb{border-top:2px solid ${hex(C.darkBlue)};margin:24px 0 16px}\n` +
    `.lt2{background:${hex(C.darkBlue)};color:white;font-weight:bold;text-align:center;font-size:13px;padding:8px}\n` +
    `</style>\n</head>\n<body>\n` +
    `<h1>MATHEMATICS GRADE 10: TRIGONOMETRY 1</h1>\n` +
    `<h2>CBE Phenomenon-Driven Lesson Sequence — Sub-Strand 2.4 (6 Lessons)</h2>\n` +
    `<table>\n<tr><th class="hd" colspan="2">SUB-STRAND OVERVIEW</th></tr>\n` +
    `<tr><td class="lb">Grade Level</td><td>${esc(UNIT.gradeLevel)}</td></tr>\n` +
    `<tr><td class="lb">Subject</td><td>${esc(UNIT.subject)}</td></tr>\n` +
    `<tr><td class="lb">Strand</td><td>${esc(UNIT.strand)}</td></tr>\n` +
    `<tr><td class="lb">Sub-Strand</td><td>${esc(UNIT.substrand)}</td></tr>\n` +
    `<tr><td class="lb">Total Duration</td><td>${esc(UNIT.duration)}</td></tr>\n` +
    `<tr><td class="lb">Content</td><td>${n2b(UNIT.content)}</td></tr>\n` +
    `<tr><td class="lb">Learning Outcomes</td><td>${n2b(UNIT.learningOutcomes)}</td></tr>\n` +
    `<tr><td class="lb">Core Competencies</td><td>${n2b(UNIT.coreCompetencies)}</td></tr>\n` +
    `<tr><td class="lg">Core Values</td><td>${n2b(UNIT.values)}</td></tr>\n` +
    `<tr><td class="lo">PCIs</td><td>${n2b(UNIT.pcis)}</td></tr>\n` +
    `<tr><td class="lp">Key Inquiry Questions</td><td>${n2b(UNIT.keyInquiry)}</td></tr>\n` +
    `<tr><td class="lp">Anchoring Phenomenon</td><td>${n2b(UNIT.phenomenon)}</td></tr>\n` +
    `<tr><td class="lp">Driving Question</td><td>${esc(UNIT.drivingQuestion)}</td></tr>\n` +
    `<tr><td class="lt">Storyline Thread</td><td>${n2b(UNIT.storylineThread)}</td></tr>\n` +
    `</table>\n`;
  for (const l of LESSONS) {
    h += `<div class="pb"></div>\n<div class="lt2">LESSON ${l.number}: ${esc(l.title)}</div>\n` +
      `<table>\n<tr><th class="ht" colspan="2">A. SPECIFIC LEARNING OUTCOMES</th></tr>\n` +
      `<tr><td class="lb" style="width:22%">Purpose</td><td>${esc(l.slo.purpose)}</td></tr>\n` +
      `<tr><td class="lb">Knowledge</td><td>${n2b(l.slo.knowledge)}</td></tr>\n` +
      `<tr><td class="lb">Skills</td><td>${n2b(l.slo.skills)}</td></tr>\n` +
      `<tr><td class="lb">Attitudes</td><td>${n2b(l.slo.attitudes)}</td></tr>\n` +
      `<tr><td class="lt">Purpose in Storyline</td><td>${esc(l.slo.purposeInStoryline)}</td></tr>\n` +
      `<tr><td class="lo">Safety Notes</td><td>${esc(l.slo.safetyNotes)}</td></tr>\n</table>\n` +
      `<table>\n<tr><th class="ht">B. LESSON OVERVIEW</th></tr>\n<tr><td>${n2b(l.overview)}</td></tr>\n</table>\n` +
      `<table>\n<tr><th class="ht" colspan="6">C. LESSON IMPLEMENTATION FRAMEWORK</th></tr>\n` +
      `<tr><th class="hd" style="width:7%">Phase</th><th class="hb" style="width:18%">Learner Experience</th>` +
      `<th class="ht" style="width:18%">Resource</th><th class="hb" style="width:19%">Teacher Actions</th>` +
      `<th class="ht" style="width:19%">Sensemaking Strategy</th><th class="hb" style="width:19%">Assessment Strategy</th></tr>\n` +
      l.framework.map(f =>
        `<tr><td style="background:${pc[f.phase]||hex(C.lightBlue)};font-weight:bold">${esc(f.phase)}</td>` +
        `<td>${n2b(f.learnerExperience)}</td><td class="bg">${n2b(f.resource)}</td>` +
        `<td>${n2b(f.teacherMoves)}</td><td class="bg">${n2b(f.sensemakingStrategy)}</td>` +
        `<td>${n2b(f.formativeAssessment)}</td></tr>`).join('\n') +
      `\n</table>\n` +
      `<table>\n<tr><th class="ho">D. TEACHER REFLECTION</th></tr>\n<tr><td class="bgo">${n2b(l.teacherReflection)}</td></tr>\n</table>\n` +
      `<table>\n<tr><th class="hp" colspan="2">E. SUMMARY TABLE PROMPT</th></tr>\n` +
      `<tr><td class="lp" style="width:22%;font-weight:bold">What did I observe?</td><td>${esc(l.summaryTablePrompt.observed)}</td></tr>\n` +
      `<tr><td class="lp" style="font-weight:bold">What did I learn?</td><td>${esc(l.summaryTablePrompt.learned)}</td></tr>\n` +
      `<tr><td class="lp" style="font-weight:bold">How does this explain the phenomenon?</td><td>${esc(l.summaryTablePrompt.explained)}</td></tr>\n` +
      `</table>\n`;
  }
  h += `</body>\n</html>\n`;
  return h;
}

// ─── GFM ──────────────────────────────────────────────────────────────────────
function buildGFM() {
  let md = `# Mathematics Grade 10: Trigonometry 1\n## CBE Phenomenon-Driven Lesson Sequence — Sub-Strand 2.4 (6 Lessons)\n\n`;
  md += `## Sub-Strand Overview\n\n| Field | Detail |\n|---|---|\n`;
  for (const [k, v] of [['Grade Level', UNIT.gradeLevel],['Subject', UNIT.subject],
    ['Strand', UNIT.strand],['Sub-Strand', UNIT.substrand],['Duration', UNIT.duration],
    ['Driving Question', UNIT.drivingQuestion]])
    md += `| **${k}** | ${v.replace(/\n/g, ' ')} |\n`;
  md += `\n### Learning Outcomes\n${UNIT.learningOutcomes.replace(/\n/g,'  \n')}\n\n`;
  md += `### Phenomenon\n${UNIT.phenomenon.replace(/\n/g,'  \n')}\n\n---\n\n`;
  for (const l of LESSONS) {
    md += `## Lesson ${l.number}: ${l.title}\n\n**Duration:** ${l.duration}\n\n`;
    md += `### A. SLOs\n**Purpose:** ${l.slo.purpose}\n\n**Knowledge:**  \n${l.slo.knowledge.replace(/\n/g,'  \n')}\n\n`;
    md += `**Skills:**  \n${l.slo.skills.replace(/\n/g,'  \n')}\n\n`;
    md += `### B. Overview\n${l.overview.replace(/\n/g,'  \n')}\n\n`;
    md += `### C. Framework\n| Phase | Learner Exp | Resource | Teacher | Sensemaking | Assessment |\n|---|---|---|---|---|---|\n`;
    for (const f of l.framework) {
      const c = s => s.replace(/\n/g,' ').replace(/\|/g,'\\|');
      md += `| **${f.phase}** | ${c(f.learnerExperience)} | ${c(f.resource)} | ${c(f.teacherMoves)} | ${c(f.sensemakingStrategy)} | ${c(f.formativeAssessment)} |\n`;
    }
    md += `\n### D. Teacher Reflection\n${l.teacherReflection.replace(/\n/g,'  \n')}\n\n`;
    md += `### E. Summary Table\n| | |\n|---|---|\n| **Observed** | ${l.summaryTablePrompt.observed} |\n`;
    md += `| **Learned** | ${l.summaryTablePrompt.learned} |\n| **Explained** | ${l.summaryTablePrompt.explained} |\n\n---\n\n`;
  }
  return md;
}

// ─── Main ─────────────────────────────────────────────────────────────────────
async function main() {
  console.log('Generating Math 2.4 Trigonometry 1...\n');
  console.log('1/3 Building docx files...');
  fs.writeFileSync(path.join(OUT_DOCX, 'Math_Trigonometry1_CBE_LessonSequence.docx'),
    await Packer.toBuffer(await buildSoW()));
  fs.writeFileSync(path.join(OUT_DOCX, 'Math_Trigonometry1_FinalExplanation.docx'),
    await Packer.toBuffer(await buildFinalExplanation()));
  fs.writeFileSync(path.join(OUT_DOCX, 'Math_Trigonometry1_SummaryTable.docx'),
    await Packer.toBuffer(await buildSummaryTable()));
  console.log(`    Saved 3 docx files to ${OUT_DOCX}\n`);
  console.log('2/3 Building HTML...');
  fs.writeFileSync(path.join(OUT_HTML, 'Math_Trigonometry1_CBE_LessonSequence.html'), buildHTML(), 'utf8');
  console.log(`    Saved to ${OUT_HTML}\n`);
  console.log('3/3 Building GFM...');
  fs.writeFileSync(path.join(OUT_GFM, 'Math_Trigonometry1_CBE_LessonSequence.md'), buildGFM(), 'utf8');
  console.log(`    Saved to ${OUT_GFM}\n`);
  console.log('Done! All 5 files generated for Math 2.4.');
}
main().catch(err => { console.error(err); process.exit(1); });
