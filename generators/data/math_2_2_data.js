'use strict';
/**
 * math_2_2_data.js — Sub-strand data for universal generator
 * Auto-extracted from math_2_2_reflection_congruence.js
 * Run: node generators/generate.js math_2_2
 */

const META = {
  subject: 'Mathematics',
  grade: 10,
  outputDir: 'Grade 10 Math/Math 2.2 Reflection Congruence',
  filePrefix: 'Math_Reflection_Congruence',
  col3Label: 'Teacher Actions',
  col5Label: 'Assessment Strategy',
};

const UNIT = {
  gradeLevel:  'Grade 10',
  subject:     'Mathematics',
  strand:      'Strand 2.0: Measurement and Geometry',
  substrand:   'Sub-Strand 2.2: Reflection and Congruence',
  duration:    '6 lessons × 4 periods × 40 minutes = 960 minutes total',
  content:
    '• Lines of symmetry in plane figures\n' +
    '• Properties of reflection using objects and images\n' +
    '• Drawing images given an object and a mirror line (plane surface and Cartesian plane)\n' +
    '• Determining the equation of the mirror line given an object and its image\n' +
    '• Congruence tests for triangles (SSS, SAS, ASA, AAS)\n' +
    '• Real-life applications of reflection and congruence',
  learningOutcomes:
    'By the end of the sub-strand, the learner should be able to:\n' +
    'a) identify lines of symmetry in plane figures\n' +
    'b) determine the properties of reflection in different situations\n' +
    'c) draw an image given an object and a mirror line on a plane surface and Cartesian plane\n' +
    'd) determine the equation of the mirror line given an object and its image\n' +
    'e) carry out congruence tests for triangles\n' +
    'f) promote use of reflection and congruence in real life situations',
  coreCompetencies:
    '• Communication and Collaboration: sharing mathematical reasoning in groups\n' +
    '• Critical Thinking and Problem Solving: deducing properties from observations\n' +
    '• Digital Literacy: using GeoGebra and graphing tools\n' +
    '• Learning to Learn: connecting new reflection rules to prior transformation knowledge\n' +
    '• Self-Efficacy: building confidence through hands-on mirror and folding activities\n' +
    '• Creativity and Innovation: applying symmetry in design contexts',
  values:
    '• Respect: valuing different approaches to the same mathematical problem\n' +
    '• Integrity: showing all construction steps accurately\n' +
    '• Excellence: striving for precision in geometric drawings\n' +
    '• Responsibility: care for shared measuring equipment\n' +
    '• Unity: collaborating in group investigations',
  pcis:
    '• Environmental Education: symmetry patterns in Kenyan flora and fauna\n' +
    '• Citizenship: Kenyan architecture and cultural textile design',
  keyInquiry:
    'How does reflection create the balance, beauty, and precision we see in structures, ' +
    'patterns, and nature around us?',
  phenomenon:
    'Students observe photographs of the Kenyatta International Convention Centre (KICC) dome, ' +
    'flamingo flocks at Lake Nakuru forming mirror-image patterns on the water, and Kanga textile ' +
    'designs. Each image shows perfect bilateral symmetry.\n' +
    'Anchor question: "What mathematical rule explains why one half of these objects is a perfect ' +
    'copy of the other — and can we use that rule to create our own?"',
  drivingQuestion:
    'How does reflection create balance, beauty, and precision in the world around us — ' +
    'and how can we use reflection rules to design and construct accurate images?',
  storylineThread:
    'L1: Discover symmetry everywhere in Kenya → build initial model of "mirror rules"\n' +
    'L2: Investigate reflection properties using mirrors and folded paper → update model\n' +
    'L3: Apply rules to draw reflections on plane figures → model becomes procedural\n' +
    'L4: Move to Cartesian plane → reflection rules become algebraic\n' +
    'L5: Work backwards — find the mirror line from object + image → model reaches full form\n' +
    'L6: Congruence tests + real-world design challenge → complete explanation written',
};

const LESSONS = [

  // ── LESSON 1 ─────────────────────────────────────────────────────────────
  {
    number: 1,
    aresKeywords: 'reflection symmetry transformation geometry',
    title:    'Lines of Symmetry — What Makes a Shape Balanced?',
    duration: '4 periods / 160 minutes',
    slo: {
      purpose:
        'Students discover that many shapes and real objects have lines of symmetry, ' +
        'and begin building a model of what "reflection" means mathematically.',
      knowledge:
        '• Define a line of symmetry as a line that divides a shape into two congruent halves\n' +
        '• Identify the number of lines of symmetry in common plane figures (triangle, square, rectangle, circle, regular hexagon)\n' +
        '• Distinguish between shapes with and without symmetry',
      skills:
        '• Fold physical shapes to locate lines of symmetry\n' +
        '• Draw lines of symmetry accurately using a ruler\n' +
        '• Categorise Kenyan objects by number of lines of symmetry',
      attitudes:
        '• Appreciation of mathematical order in natural and man-made Kenyan objects\n' +
        '• Curiosity about why some shapes have more lines of symmetry than others',
      keyInquiry: 'How does reflection create balance, beauty, and precision in the world around us?',
      purposeInStoryline:
        'This lesson anchors the driving question in visible Kenyan contexts. ' +
        'Students move from informal notions of "balanced" to the precise mathematical idea of a line of symmetry. ' +
        'The DQB is opened; initial models of reflection are drawn.',
      safetyNotes: 'Use safety scissors only. Handle mirrors carefully — no glass mirrors; use polished metal or plastic mirrors.',
    },
    overview:
      'Students begin with a gallery walk: eight photographs pinned around the room — KICC dome, ' +
      'Lake Nakuru flamingos, kanga textile, a Kenyan flag, a butterfly, a starfish, the letter "A", ' +
      'and a freehand blob. Groups discuss: "Which of these has balance — and where exactly is the balance line?"\n\n' +
      'After sharing, the teacher introduces the term "line of symmetry" and students test their claims ' +
      'by folding cut-out shapes. The DQB is opened and students post their first questions. ' +
      'The lesson closes with each student drawing their initial model: "What is reflection?"',
    framework: [
      {
        phase: 'Predict Phase',
        learnerExperience:
          'Gallery walk with 8 photographs. Groups write YES/NO for symmetry and sketch where they think the balance line is. ' +
          'No definitions given — this is a prediction task.',
        resource:
          'MATERIAL: 8 printed photographs (A4), sticky notes, pencils\n' +
          'DIGITAL: GeoGebra Symmetry Explorer (optional)',
        teacherMoves:
          '"Look carefully before you say anything. What do you notice about the two halves?"\n' +
          '"Do NOT use the word \'symmetry\' yet — describe what you see in your own words."',
        sensemakingStrategy:
          'Eliciting prior knowledge through observation. Gallery walk externalises existing mental models ' +
          'before formal definitions are introduced.',
        formativeAssessment:
          'Which photographs cause disagreement? (Reveals: students may confuse rotational and reflective symmetry.) ' +
          'Listen for the word "mirror" — that is the conceptual anchor for Lesson 2.',
      },
      {
        phase: 'Observe Phase',
        learnerExperience:
          'Students receive cut-out shapes (equilateral triangle, square, rectangle, circle, scalene triangle, irregular quadrilateral). ' +
          'Task: fold each shape so both halves match exactly. Mark the fold line. Count the folds possible for each shape.',
        resource:
          'MATERIAL: Pre-cut paper shapes (one set per pair), pencils, rulers\n' +
          'REFERENCE: Textbook p.XX — Lines of Symmetry',
        teacherMoves:
          '"If both halves sit exactly on top of each other, the fold is a line of symmetry."\n' +
          '"How many different ways can you fold the square? What about the circle?"',
        sensemakingStrategy:
          'Hands-on manipulation creates embodied understanding of line of symmetry before abstract definition.',
        formativeAssessment:
          'Circulate: can students fold a rectangle correctly (only 2 lines, not the diagonal)? ' +
          'This is a common error — address it whole-class.',
      },
      {
        phase: 'Explain Phase',
        learnerExperience:
          'Groups share results. Class builds a "Symmetry Table" on the board: shape, number of lines, where they are. ' +
          'Students formally define: "A line of symmetry divides a shape into two congruent mirror-image halves."',
        resource:
          'MATERIAL: Whiteboard/chart paper\n' +
          'VOCAB: line of symmetry, congruent, bilateral symmetry',
        teacherMoves:
          '"Why does the scalene triangle have zero lines of symmetry?" (Build reasoning, not memorisation.)\n' +
          '"What pattern do you notice between the number of sides and lines of symmetry in regular polygons?"',
        sensemakingStrategy:
          'Data consolidation into a class table. Students move from concrete to abstract by constructing the definition themselves.',
        formativeAssessment:
          'Exit question (written): "Draw a shape with exactly 2 lines of symmetry. Label them."',
      },
      {
        phase: 'Driving Question Board (DQB) Creation',
        learnerExperience:
          'Students write questions on sticky notes: "What is a mirror line exactly?" ' +
          '"Can you reflect a shape and keep it the same size?" "How does reflection work on a graph?" ' +
          'Questions are posted on the DQB under categories: ABOUT SHAPE / ABOUT RULES / ABOUT GRAPHS.',
        resource: 'MATERIAL: Sticky notes (3 per student), DQB board/wall space',
        teacherMoves:
          '"Post your question even if you think it is obvious — all questions are valid at this stage."\n' +
          '"By Lesson 6, every question on this board will have an answer."',
        sensemakingStrategy:
          'DQB externalises curiosity and sets the intellectual agenda for the unit.',
        formativeAssessment: 'Review DQB after class — identify misconceptions and gaps to address in Lesson 2.',
      },
      {
        phase: 'Model Building Phase',
        learnerExperience:
          'Each student draws their Initial Model: "What is reflection, and what rules does it follow?" ' +
          'Can use diagrams, words, or equations — whatever they currently think is true.',
        resource: 'MATERIAL: Model Journal page (blank half-page with heading "My Reflection Model — Lesson 1")',
        teacherMoves:
          '"This is NOT a test. It is a snapshot of your current thinking. There are no wrong answers today — ' +
          'but there will be changes by Lesson 6!"\n' +
          '"You will revise this model every lesson. Keep ALL versions."',
        sensemakingStrategy:
          'Initial modelling as baseline. Students will compare Lesson 1 and Lesson 6 models to see their learning growth.',
        formativeAssessment:
          'Collect models: do students mention distance from mirror line? Angle? Size preservation? ' +
          'This informs Lesson 2 focus.',
      },
    ],
    teacherReflection:
      'After teaching this lesson, reflect on:\n\n' +
      '1. Which photographs generated the most disagreement in the gallery walk? What does this reveal about prior knowledge?\n\n' +
      '2. Did students confuse rotational symmetry with reflective symmetry? How will you address this in Lesson 2?\n\n' +
      '3. Rectangle folding: did students try to fold along the diagonal? How did you correct this?\n\n' +
      '4. Quality of DQB questions — are they mostly about shapes (surface), or are some asking about rules and graphs (deeper)?\n\n' +
      '5. How detailed were initial models? Any student who already knows the reflection rule (equal distance from mirror line)?\n\n' +
      '6. Pacing: was 160 minutes sufficient for gallery walk + folding + DQB + model? What would you cut or extend?',
    summaryTablePrompt: {
      observed:
        'Eight photographs of Kenyan objects and patterns with/without symmetry. ' +
        'Folded paper shapes to find lines of symmetry — rectangle has 2, square has 4, circle has infinite, scalene triangle has 0. ' +
        'DQB opened. Initial model drawn.',
      learned:
        'A line of symmetry divides a shape into two congruent mirror-image halves. ' +
        'Regular polygons have the same number of lines of symmetry as sides. ' +
        'Not all shapes are symmetric — a scalene triangle has no lines of symmetry.',
      explained:
        'The KICC dome and flamingo flock both show bilateral symmetry — one half mirrors the other exactly. ' +
        'But we do not yet know the MATHEMATICAL RULE that makes this work. That is what Lessons 2–5 will reveal.',
    },
  },

  // ── LESSON 2 ─────────────────────────────────────────────────────────────
  {
    number: 2,
    aresKeywords: 'reflection properties mirror line distance',
    title:    'Properties of Reflection — Discovering the Mirror Rules',
    duration: '4 periods / 160 minutes',
    slo: {
      purpose:
        'Students investigate and state the properties of reflection: equal distance from mirror line, ' +
        'perpendicular to mirror line, same size and shape, reversed orientation.',
      knowledge:
        '• State that object and image are equidistant from the mirror line\n' +
        '• State that the line joining any point to its image is perpendicular to the mirror line\n' +
        '• State that object and image are congruent (same size and shape)\n' +
        '• Explain that reflection reverses orientation (left-right flip)',
      skills:
        '• Use a plane mirror to locate the image of a point and measure distances\n' +
        '• Verify the perpendicularity property using a set square\n' +
        '• Record and tabulate experimental results',
      attitudes:
        '• Scientific curiosity: testing claims rather than assuming\n' +
        '• Precision: measuring distances accurately',
      keyInquiry: 'How does reflection create balance, beauty, and precision in the world around us?',
      purposeInStoryline:
        'Students shift from observing symmetry to discovering the mathematical rules that govern reflection. ' +
        'The four properties become the core content of the unit — all subsequent lessons apply these rules.',
      safetyNotes: 'Use plastic/polished-metal mirrors only. Ensure mirror edges are smooth.',
    },
    overview:
      'Students work in pairs with a plastic mirror and a printed worksheet showing points and shapes. ' +
      'They place the mirror on a drawn line and observe where the image appears. They measure distances from ' +
      'points to the mirror line and from images to the mirror line — discovering that these are always equal.\n\n' +
      'A second investigation tests perpendicularity: students connect each point to its image and check the ' +
      'angle with the mirror line. The class consolidates the four properties. DQB questions about "rules" ' +
      'are moved to ANSWERED. Models are updated.',
    framework: [
      {
        phase: 'Predict Phase',
        learnerExperience:
          'Pose: "If I place a point 3 cm from the mirror line — where will its image be? Predict and justify." ' +
          'Groups write predictions on mini-whiteboards before using mirrors.',
        resource: 'MATERIAL: Mini-whiteboards or A4 paper, markers',
        teacherMoves:
          '"Do not use the mirror yet. Commit to a prediction first."\n' +
          '"3 cm from the line — same side as the object? Other side? How far?"',
        sensemakingStrategy:
          'Prediction before observation creates cognitive investment in the outcome.',
        formativeAssessment: 'Listen for the "equal distance" idea — who already has this intuition?',
      },
      {
        phase: 'Observe Phase',
        learnerExperience:
          'Investigation with mirror and worksheet:\n' +
          '• Step 1: Mark point P at 3 cm from mirror line L. Place mirror on L. Mark image P\'.\n' +
          '• Step 2: Measure PP\' distance. Measure distance from P to L and from P\' to L.\n' +
          '• Step 3: Repeat for P at 1 cm, 5 cm, 7 cm. Record in table.\n' +
          '• Step 4: Draw line PP\'. Measure the angle it makes with L.',
        resource:
          'MATERIAL: Plastic mirrors, rulers, set squares, printed worksheets, pencils\n' +
          'DIGITAL: GeoGebra Reflection tool (for verification)',
        teacherMoves:
          '"Measure carefully — to the nearest millimetre."\n' +
          '"What is the angle between PP\' and L in every case? What word describes this?"',
        sensemakingStrategy:
          'Data collection from physical experiment. Repeated measurement across different distances builds inductive reasoning.',
        formativeAssessment:
          'Check tables: are students measuring perpendicular distances from point to line (not diagonal)? ' +
          'Common error: measuring along the page rather than perpendicularly.',
      },
      {
        phase: 'Explain Phase',
        learnerExperience:
          'Groups present findings. Class derives and writes the four properties of reflection:\n' +
          '1. Object distance = Image distance from mirror line\n' +
          '2. PP\' is perpendicular to the mirror line\n' +
          '3. Object and image are congruent (same size and shape)\n' +
          '4. Image is a lateral (left-right) inversion of the object',
        resource: 'MATERIAL: Whiteboard; student-made tables',
        teacherMoves:
          '"State each property as a rule using the word \'always\'."\n' +
          '"Which of these properties explains why a mirror writing looks reversed?"',
        sensemakingStrategy:
          'Inductive reasoning: from specific measurements to general rules. ' +
          'Students own the properties because they discovered them.',
        formativeAssessment:
          'Quick-check: "A point is 4.5 cm from the mirror line. How far is its image from the mirror line? ' +
          'How far is the image from the original point?"',
      },
      {
        phase: 'Driving Question Board (DQB) Creation',
        learnerExperience:
          'Review DQB from Lesson 1. Move "rules" questions to ANSWERED. ' +
          'Add new questions: "How do I reflect a SHAPE, not just a point?" ' +
          '"What if the mirror line is diagonal?" "Can the mirror line be y = x?"',
        resource: 'MATERIAL: DQB board, coloured sticky notes (new colour for Lesson 2 additions)',
        teacherMoves: '"Which questions from Lesson 1 can we now answer? Bring them to the front."',
        sensemakingStrategy: 'DQB curation shows students their own learning progression.',
        formativeAssessment: 'New questions preview Lessons 3–5 focus areas.',
      },
      {
        phase: 'Model Building Phase',
        learnerExperience:
          'Update Reflection Model: add the four properties discovered today. ' +
          'Draw a labelled diagram showing a point P, its image P\', the mirror line L, and the two equal distances.',
        resource: 'MATERIAL: Model Journal page (Lesson 2 revision)',
        teacherMoves:
          '"Your model must now include a diagram AND a written rule for each property."\n' +
          '"Compare your Lesson 1 and Lesson 2 models — what changed?"',
        sensemakingStrategy: 'Model revision makes learning visible and prepares students for Lessons 3–4.',
        formativeAssessment: 'Do models correctly show perpendicularity and equal distances?',
      },
    ],
    teacherReflection:
      'After teaching this lesson, reflect on:\n\n' +
      '1. Did the prediction-before-observation structure improve engagement? Did students genuinely commit to predictions?\n\n' +
      '2. Common measurement error: were students measuring diagonal distances instead of perpendicular? How did you address it?\n\n' +
      '3. Which of the four properties caused most confusion? (Often: perpendicularity and lateral inversion.)\n\n' +
      '4. Did GeoGebra help or distract? Would you use it earlier or later in the lesson?\n\n' +
      '5. How strong were student model revisions? Did they add all four properties or only the equal-distance rule?\n\n' +
      '6. Are DQB questions now pointing toward Lessons 3–5 topics (shape reflection, Cartesian plane)?',
    summaryTablePrompt: {
      observed:
        'Measured distances from points to mirror line and from their images to mirror line — always equal. ' +
        'Drew PP\' lines and measured the angle with the mirror line — always 90°. ' +
        'Confirmed that object and image are same size and shape (congruent) but laterally inverted.',
      learned:
        'Four properties of reflection: (1) equal distance from mirror line, (2) PP\' perpendicular to mirror line, ' +
        '(3) object ≅ image (congruent), (4) image is laterally inverted. ' +
        'These four rules ALWAYS hold — for any point, any mirror line.',
      explained:
        'The KICC dome is symmetric because every point on the left side is the mirror image of the corresponding point on the right — ' +
        'same distance from the central axis, perpendicular connection. ' +
        'The mathematical rules we discovered today are exactly what the architects used.',
    },
  },

  // ── LESSON 3 ─────────────────────────────────────────────────────────────
  {
    number: 3,
    aresKeywords: 'reflection plane figures drawing image',
    title:    'Reflection on Plane Figures — Drawing the Image',
    duration: '4 periods / 160 minutes',
    slo: {
      purpose:
        'Students apply the four reflection properties to draw the image of a geometric shape given an object and a mirror line.',
      knowledge:
        '• State the step-by-step procedure for reflecting a shape over a given mirror line\n' +
        '• Identify corresponding vertices in object and image\n' +
        '• Verify the image using the perpendicularity and equal-distance properties',
      skills:
        '• Draw the reflection of a triangle, quadrilateral, and irregular shape over a given mirror line\n' +
        '• Reflect shapes over horizontal, vertical, and diagonal mirror lines\n' +
        '• Use a ruler and set square accurately',
      attitudes:
        '• Precision and patience in geometric construction\n' +
        '• Confidence to attempt reflections over non-horizontal/vertical lines',
      keyInquiry: 'How does reflection create balance, beauty, and precision in the world around us?',
      purposeInStoryline:
        'Students transition from knowing the rules to applying them constructively. ' +
        'This lesson is procedural and skill-building — the foundation for Lesson 4 (Cartesian plane).',
      safetyNotes: 'Compass points are sharp — use with care and store with cover.',
    },
    overview:
      'Teacher models the step-by-step construction: (1) identify each vertex, (2) draw a perpendicular from each vertex to ' +
      'the mirror line, (3) extend the perpendicular an equal distance beyond the mirror line, (4) mark the image vertex, ' +
      '(5) connect image vertices in order.\n\n' +
      'Students then practise in three rounds: mirror line is horizontal → vertical → diagonal at 45°. ' +
      'A challenge extension: reflect a Kanga-inspired pattern tile over two lines to create a 2×2 symmetric tile.',
    framework: [
      {
        phase: 'Predict Phase',
        learnerExperience:
          'Shown a triangle ABC and a mirror line L. "Before drawing — where will the image be? Sketch your prediction." ' +
          'Focus on vertex A (closest to L), B (farthest), C (on L).',
        resource: 'MATERIAL: Printed worksheet with triangle and mirror line; pencils',
        teacherMoves:
          '"Pay attention to vertex C — it sits ON the mirror line. What happens to a point that is on the line?"',
        sensemakingStrategy: 'Predicting specific vertex positions activates the equal-distance property.',
        formativeAssessment: 'Check: do students correctly predict that C maps to itself (it is on the mirror line)?',
      },
      {
        phase: 'Observe Phase',
        learnerExperience:
          'Teacher-led demonstration of construction steps on the board. ' +
          'Students follow along on their own worksheet simultaneously. ' +
          'After teacher demonstration, students attempt a second triangle independently.',
        resource:
          'MATERIAL: Rulers, set squares, compasses (optional for marking equal distances)\n' +
          'VISUAL: Step-by-step construction poster on board',
        teacherMoves:
          '"I draw a perpendicular from A to L — I need my set square for this, not just a ruler."\n' +
          '"I measure 2.5 cm from A to L. I count 2.5 cm beyond L on the other side. That is A\'."',
        sensemakingStrategy:
          'Worked example followed immediately by independent practice (I Do → We Do → You Do).',
        formativeAssessment:
          'Circulate during independent practice. Common errors: not extending perpendicular far enough, ' +
          'measuring along a non-perpendicular path.',
      },
      {
        phase: 'Explain Phase',
        learnerExperience:
          'Three practice rounds:\n' +
          '• Round 1: Reflect quadrilateral PQRS over a horizontal mirror line\n' +
          '• Round 2: Reflect triangle DEF over a vertical mirror line\n' +
          '• Round 3: Reflect triangle GHI over a diagonal mirror line (45°)\n' +
          'Pairs check each other\'s work using the four properties.',
        resource:
          'MATERIAL: Printed practice sheets (3 rounds), rulers, set squares\n' +
          'EXTENSION: Kanga tile design challenge (optional)',
        teacherMoves:
          '"Use the four properties to VERIFY your answer — do not just assume your drawing is right."\n' +
          '"Round 3 is the hardest. What changes when the mirror line is diagonal?"',
        sensemakingStrategy:
          'Graduated difficulty: horizontal → vertical → diagonal. ' +
          'Peer verification reinforces the four properties as checking tools.',
        formativeAssessment:
          'Collect Round 3 drawings — accuracy here indicates readiness for Lesson 4.',
      },
      {
        phase: 'Driving Question Board (DQB) Creation',
        learnerExperience:
          'Update DQB. New questions likely: "How do we do this on a coordinate grid?" ' +
          '"Is there a formula?" "What if the shape overlaps the mirror line?"',
        resource: 'MATERIAL: DQB board',
        teacherMoves: '"Lesson 4 will answer the coordinate grid questions. Let us add them now."',
        sensemakingStrategy: 'DQB maintains forward momentum — each lesson creates appetite for the next.',
        formativeAssessment: 'New questions confirm students are ready for Cartesian plane work.',
      },
      {
        phase: 'Model Building Phase',
        learnerExperience:
          'Update Reflection Model: add a labelled example of a reflected shape with all five construction steps annotated.',
        resource: 'MATERIAL: Model Journal page (Lesson 3 revision)',
        teacherMoves: '"Your model should now show the PROCEDURE, not just the properties."',
        sensemakingStrategy: 'Procedural knowledge added to the model — connects rules to action.',
        formativeAssessment: 'Do models show all five steps in correct order?',
      },
    ],
    teacherReflection:
      'After teaching this lesson, reflect on:\n\n' +
      '1. Did students predict vertex C correctly (maps to itself)? If not, how did you clarify?\n\n' +
      '2. How accurate were Round 3 (diagonal mirror line) constructions? What is the most common error?\n\n' +
      '3. Was the I Do → We Do → You Do sequence effective, or did students need more scaffolding?\n\n' +
      '4. Did the Kanga challenge extension engage higher-ability students without losing others?\n\n' +
      '5. Peer verification: did students use the four properties to check, or did they just look visually?\n\n' +
      '6. What preparation do students still need before the Cartesian plane lesson?',
    summaryTablePrompt: {
      observed:
        'Practised five-step construction: draw perpendicular from vertex → measure distance to mirror line → ' +
        'extend equal distance beyond → mark image vertex → connect vertices. ' +
        'Reflected shapes over horizontal, vertical, and diagonal mirror lines.',
      learned:
        'The five-step procedure applies to any mirror line orientation. ' +
        'A point ON the mirror line maps to itself. ' +
        'The image is always congruent to the object — same size, reversed orientation.',
      explained:
        'The flamingo mirror image in Lake Nakuru water is created by the same five steps we used today — ' +
        'every point on the flamingo reflects equally to the water surface (the mirror line). ' +
        'We can now construct any reflected image precisely.',
    },
  },

  // ── LESSON 4 ─────────────────────────────────────────────────────────────
  {
    number: 4,
    aresKeywords: 'reflection Cartesian plane coordinates',
    title:    'Reflection on the Cartesian Plane',
    duration: '4 periods / 160 minutes',
    slo: {
      purpose:
        'Students extend reflection to the Cartesian plane, applying coordinate rules for reflection ' +
        'over the x-axis, y-axis, the line y = x, and the line y = -x.',
      knowledge:
        '• State coordinate rules: reflection over x-axis (x,y) → (x,−y); over y-axis → (−x,y); ' +
        'over y = x → (y,x); over y = −x → (−y,−x)\n' +
        '• Identify which axis or line is the mirror line from a plotted object and image',
      skills:
        '• Plot points and their images on the Cartesian plane\n' +
        '• Apply coordinate rules to reflect polygons\n' +
        '• Verify reflections using the four properties',
      attitudes:
        '• Appreciation that algebraic rules make geometric construction faster and more precise\n' +
        '• Confidence with coordinate geometry',
      keyInquiry: 'How does reflection create balance, beauty, and precision in the world around us?',
      purposeInStoryline:
        'The lesson bridges the geometric procedure of Lesson 3 with algebraic rules. ' +
        'Students see that the Cartesian plane gives us shortcuts — the coordinate rules replace the five-step construction.',
      safetyNotes: 'No specific safety notes.',
    },
    overview:
      'Students first plot a triangle on squared paper and reflect it over the x-axis using the Lesson 3 construction. ' +
      'They then record the coordinates of each vertex and its image, looking for the pattern. ' +
      'The four coordinate rules are derived from the data. Students then practise applying the rules directly — ' +
      'no construction needed, just the algebraic rule.\n\n' +
      'GeoGebra is used for self-checking and for exploring y = x and y = -x reflections.',
    framework: [
      {
        phase: 'Predict Phase',
        learnerExperience:
          'Given triangle A(2,3), B(5,1), C(4,5). "If you reflect over the x-axis, predict the coordinates of A\', B\', C\'." ' +
          'No grid provided — pure coordinate reasoning.',
        resource: 'MATERIAL: Blank paper for predictions, pencils',
        teacherMoves:
          '"What does the x-axis do to the y-coordinate of a point above it?"\n' +
          '"The x-axis is the mirror line. A is 3 units above it. Where will A\' be?"',
        sensemakingStrategy:
          'Numerical prediction connects the equal-distance property to coordinate arithmetic.',
        formativeAssessment: 'Do students predict (2,−3)? If not, they are not yet applying the equal-distance rule numerically.',
      },
      {
        phase: 'Observe Phase',
        learnerExperience:
          'On squared paper: plot A(2,3), B(5,1), C(4,5). Use Lesson 3 construction to reflect over x-axis. ' +
          'Record: A(2,3)→A\'(_,_), B(5,1)→B\'(_,_), C(4,5)→C\'(_,_). ' +
          'Repeat for reflection over y-axis. Record coordinates. ' +
          'Look for the pattern: what changes? What stays the same?',
        resource:
          'MATERIAL: Squared paper, rulers, pencils\n' +
          'DIGITAL: GeoGebra Cartesian Reflection (self-check after manual work)',
        teacherMoves:
          '"Fill in the table first — then look for the pattern."\n' +
          '"Don\'t tell me the rule yet. What do you NOTICE?"',
        sensemakingStrategy:
          'Pattern recognition from tabulated data. Students derive the algebraic rule inductively.',
        formativeAssessment:
          'Table completion: are coordinates correct to verify pattern? Check A\'(2,−3), B\'(5,−1), C\'(4,−5).',
      },
      {
        phase: 'Explain Phase',
        learnerExperience:
          'Class derives four rules from the table:\n' +
          '• Over x-axis: (x, y) → (x, −y) — y changes sign\n' +
          '• Over y-axis: (x, y) → (−x, y) — x changes sign\n' +
          '• Over y = x: (x, y) → (y, x) — coordinates swap\n' +
          '• Over y = −x: (x, y) → (−y, −x) — swap then negate both\n' +
          'Students practise 6 coordinate-rule exercises.',
        resource:
          'MATERIAL: Exercise worksheet with 6 problems\n' +
          'DIGITAL: GeoGebra for y = x and y = −x exploration',
        teacherMoves:
          '"The rule replaces the five-step construction. But you should understand WHY the rule works, not just what it is."\n' +
          '"Can you explain the y = x rule using the equal-distance property?"',
        sensemakingStrategy:
          'Algebraic generalisation. Students see that coordinate rules are the equal-distance property expressed algebraically.',
        formativeAssessment:
          'Worksheet completion: mark problems 5 and 6 (y = x and y = −x) — these are the hardest.',
      },
      {
        phase: 'Driving Question Board (DQB) Creation',
        learnerExperience:
          'Update DQB. New possible questions: "How do I find the mirror line equation from object + image?" ' +
          '"Can the mirror line be any line, like y = 2x?" Add these for Lesson 5.',
        resource: 'MATERIAL: DQB board',
        teacherMoves: '"Lesson 5 answers the \'find the mirror line\' questions."',
        sensemakingStrategy: 'DQB continues to drive curiosity forward.',
        formativeAssessment: 'New questions confirm conceptual readiness for Lesson 5.',
      },
      {
        phase: 'Model Building Phase',
        learnerExperience:
          'Update Reflection Model: add the four coordinate rules as a table. ' +
          'Show a worked example using coordinates.',
        resource: 'MATERIAL: Model Journal page (Lesson 4 revision)',
        teacherMoves: '"Your model is now algebraic AND geometric. That is powerful."',
        sensemakingStrategy: 'Model integrates geometric and algebraic representations.',
        formativeAssessment: 'Do models correctly state all four coordinate rules?',
      },
    ],
    teacherReflection:
      'After teaching this lesson, reflect on:\n\n' +
      '1. Did students make the connection between equal-distance property and coordinate arithmetic (e.g., y changes sign for x-axis reflection)?\n\n' +
      '2. The y = x rule (coordinates swap) is counterintuitive — how did students react? What explanation worked best?\n\n' +
      '3. Did GeoGebra accelerate understanding or become a distraction from working through the derivation manually?\n\n' +
      '4. Worksheet accuracy on y = −x problems — this is the hardest transformation. What errors did you see?\n\n' +
      '5. Did students connect this lesson back to the KICC phenomenon — e.g., "the central axis of KICC is the y-axis"?\n\n' +
      '6. How confident did students seem about Lesson 5 (finding the mirror line)? What do you need to pre-teach?',
    summaryTablePrompt: {
      observed:
        'Plotted triangles on Cartesian plane and reflected over x-axis and y-axis using the Lesson 3 construction. ' +
        'Tabulated coordinates of object and image points. Identified patterns → derived four coordinate rules. ' +
        'Used GeoGebra to explore y = x and y = −x reflections.',
      learned:
        'Four coordinate reflection rules: over x-axis → (x,y)→(x,−y); over y-axis → (−x,y); ' +
        'over y=x → (y,x); over y=−x → (−y,−x). ' +
        'These rules ARE the equal-distance property expressed algebraically.',
      explained:
        'The Kanga textile pattern uses exactly these rules — the designer reflects a tile over the x-axis and y-axis ' +
        'to create a four-fold symmetric pattern. We can now describe any reflection in coordinates.',
    },
  },

  // ── LESSON 5 ─────────────────────────────────────────────────────────────
  {
    number: 5,
    aresKeywords: 'mirror line working backwards reflection',
    title:    'Finding the Mirror Line — Working Backwards',
    duration: '4 periods / 160 minutes',
    slo: {
      purpose:
        'Students determine the equation of the mirror line given an object and its image, ' +
        'completing the full cycle of reflection understanding.',
      knowledge:
        '• State that the mirror line is the perpendicular bisector of the segment joining any point to its image\n' +
        '• Determine the equation of the mirror line given pairs of corresponding points',
      skills:
        '• Construct the perpendicular bisector of PP\' to find the mirror line\n' +
        '• Use midpoint and gradient methods to find the mirror line equation\n' +
        '• Verify the equation using at least two point pairs',
      attitudes:
        '• Persistence with multi-step problems\n' +
        '• Appreciation that working backwards is a powerful problem-solving strategy',
      keyInquiry: 'How does reflection create balance, beauty, and precision in the world around us?',
      purposeInStoryline:
        'The inverse problem — finding the mirror line — completes the model. ' +
        'Students can now both construct a reflection AND identify the rule from a given image. ' +
        'This makes the model fully two-directional.',
      safetyNotes: 'No specific safety notes.',
    },
    overview:
      'The lesson opens with an "unknown mirror" challenge: students are shown an object and image ' +
      'but NOT the mirror line. They must find it. This reverses all previous work.\n\n' +
      'Students recall that PP\' is always perpendicular to the mirror line and that the mirror line ' +
      'bisects PP\'. They construct the perpendicular bisector of at least two PP\' segments — ' +
      'these bisectors coincide to reveal the mirror line. The equation is then found using gradient and intercept.',
    framework: [
      {
        phase: 'Predict Phase',
        learnerExperience:
          'Shown: point P(1,2) and its image P\'(5,4). "Where is the mirror line? Predict its equation." ' +
          'No construction tools yet — just reasoning from the properties.',
        resource: 'MATERIAL: Squared paper, pencils',
        teacherMoves:
          '"What do you know about the relationship between PP\' and the mirror line?"\n' +
          '"If you knew the midpoint of PP\', what would that tell you?"',
        sensemakingStrategy: 'Problem-posing from inverse context. Students apply Lesson 2 properties in reverse.',
        formativeAssessment: 'Do students recall that the mirror line passes through the midpoint of PP\'?',
      },
      {
        phase: 'Observe Phase',
        learnerExperience:
          'Worked investigation:\n' +
          '1. Find midpoint M of PP\' (M = midpoint formula)\n' +
          '2. Find gradient of PP\' (m₁)\n' +
          '3. Mirror line gradient = −1/m₁ (perpendicular)\n' +
          '4. Use point-slope form with M to write the equation\n' +
          '5. Verify: reflect P over the equation found — do you get P\'?\n' +
          'Repeat with a second pair of points to confirm.',
        resource:
          'MATERIAL: Squared paper, rulers, scientific calculators\n' +
          'RECALL: Midpoint formula, gradient formula, perpendicular gradients (m₁ × m₂ = −1)',
        teacherMoves:
          '"Step 3 is the key — you learned perpendicular gradients in Strand 1. Use that now."\n' +
          '"Always verify with a second point pair. One match could be coincidence."',
        sensemakingStrategy:
          'Multi-step problem with explicit connection to prior algebra knowledge (gradients, midpoint, perpendicular lines).',
        formativeAssessment:
          'Check step 3: are students correctly applying m₁ × m₂ = −1? ' +
          'Common error: using m₁ not −1/m₁ for the mirror line.',
      },
      {
        phase: 'Explain Phase',
        learnerExperience:
          'Students present solutions to two challenge problems:\n' +
          '• Problem A: Object A(−2,1), B(0,4), C(3,2) and image A\'(4,1), B\'(2,4), C\'(−1,2) — find the mirror line\n' +
          '• Problem B: Object and image given on a Cartesian grid — identify mirror line from the graph\n' +
          'Class discussion: Is the mirror line y = x? y = 1? Some other line?',
        resource:
          'MATERIAL: Coordinate geometry exercise sheets\n' +
          'DIGITAL: GeoGebra for checking',
        teacherMoves:
          '"Explain your method step by step — not just your answer."\n' +
          '"Problem B has a trick: the mirror line does not pass through the origin."',
        sensemakingStrategy:
          'Worked problems in authentic context. Students apply multi-step algebraic reasoning.',
        formativeAssessment:
          'Problem A: correct answer is x = 1. Problem B: equation depends on grid. ' +
          'Students who get incorrect equations have errors in gradient or midpoint step.',
      },
      {
        phase: 'Driving Question Board (DQB) Creation',
        learnerExperience:
          'Almost all DQB questions should now be answerable. Class works through DQB systematically. ' +
          'Remaining questions (if any) are posted for Lesson 6 to answer.',
        resource: 'MATERIAL: DQB board, green sticky notes for "ANSWERED"',
        teacherMoves: '"Which questions from Lesson 1 can FINALLY be answered now?"',
        sensemakingStrategy: 'DQB completion creates a sense of intellectual closure and motivates the final lesson.',
        formativeAssessment: 'Any remaining unanswered questions reveal gaps for Lesson 6 to address.',
      },
      {
        phase: 'Model Building Phase',
        learnerExperience:
          'Major model revision: add the inverse procedure (finding the mirror line) to the model. ' +
          'Model should now show both directions: Object + Mirror → Image AND Object + Image → Mirror.',
        resource: 'MATERIAL: Model Journal page (Lesson 5 revision)',
        teacherMoves: '"Your model is now complete in BOTH directions. That is real mathematical understanding."',
        sensemakingStrategy: 'Bidirectional model represents full conceptual mastery.',
        formativeAssessment: 'Do models clearly show both directions of the reflection relationship?',
      },
    ],
    teacherReflection:
      'After teaching this lesson, reflect on:\n\n' +
      '1. Did students recall perpendicular gradients from prior learning? How much revision was needed?\n\n' +
      '2. The perpendicular bisector approach vs. the gradient/midpoint approach — which did students find more intuitive?\n\n' +
      '3. Problem A has mirror line x = 1 (vertical). Did students recognise this requires a different approach (no gradient)?\n\n' +
      '4. Did students verify their equations by testing a point? Or did they stop after finding the equation?\n\n' +
      '5. DQB: were all questions answered by the end of Lesson 5? What remained for Lesson 6?\n\n' +
      '6. How ready do students seem for the final explanation and congruence lesson?',
    summaryTablePrompt: {
      observed:
        'Given object and image, found the mirror line using: (1) midpoint formula on PP\', ' +
        '(2) perpendicular gradient (m × m₂ = −1), (3) point-slope equation. ' +
        'Solved two challenge problems. Completed DQB — almost all questions answered.',
      learned:
        'The mirror line is the perpendicular bisector of any segment PP\'. ' +
        'To find its equation: find midpoint of PP\', find perpendicular gradient, write equation. ' +
        'This is the INVERSE of reflection — working backwards from image to mirror line.',
      explained:
        'If we have a photograph of the KICC dome and we want to find the exact axis of symmetry, ' +
        'we can now calculate it — pick any two corresponding points, apply the perpendicular bisector method, ' +
        'and we have the equation of the mirror line. Reflection is now fully understood in both directions.',
    },
  },

  // ── LESSON 6 ─────────────────────────────────────────────────────────────
  {
    number: 6,
    title:    'Congruence Tests and Real-World Design Challenge',
    duration: '4 periods / 160 minutes',
    slo: {
      purpose:
        'Students learn the four triangle congruence tests, connect congruence to reflection, ' +
        'and complete a real-world design challenge applying all unit learning.',
      knowledge:
        '• State and distinguish the four congruence tests: SSS, SAS, ASA, AAS\n' +
        '• Explain that a reflected image is always congruent to its object\n' +
        '• Identify which congruence test applies to a given pair of triangles',
      skills:
        '• Apply congruence tests to determine if two triangles are congruent\n' +
        '• Design a symmetric pattern tile using reflection (Kanga/architectural design challenge)\n' +
        '• Write a final explanation connecting reflection, congruence, and the phenomenon',
      attitudes:
        '• Pride in creating an original design using mathematical principles\n' +
        '• Confidence to explain mathematical ideas clearly in writing',
      keyInquiry: 'How does reflection create balance, beauty, and precision in the world around us?',
      purposeInStoryline:
        'Congruence is the formal connection between reflection and equality. ' +
        'The design challenge applies all five lessons. The final explanation closes the unit narrative.',
      safetyNotes: 'No specific safety notes.',
    },
    overview:
      'Lesson opens by connecting reflection to congruence: "We know reflection preserves size and shape — ' +
      'that means object and image are CONGRUENT. Today we learn the four tests that PROVE congruence formally."\n\n' +
      'Students work through the four tests (SSS, SAS, ASA, AAS) with triangle card-matching activities. ' +
      'Then the design challenge: create a symmetric tile that could be used on a Kenyan wall or kanga textile. ' +
      'Students reflect a base unit over two axes to create a 2×2 tile and label all congruent parts. ' +
      'The lesson closes with each student writing their Final Explanation and comparing Lesson 1 and Lesson 6 models.',
    framework: [
      {
        phase: 'Predict Phase',
        learnerExperience:
          'Shown two triangles: "Are these congruent? How do you know?" Students write a justification before any instruction. ' +
          'Cases shown: (a) clearly congruent by SSS, (b) same angles but different sizes (similar but not congruent), ' +
          '(c) ambiguous — same two sides and an angle (SSA is NOT a congruence test).',
        resource: 'MATERIAL: Triangle comparison worksheet',
        teacherMoves:
          '"What information do you need to be CERTAIN two triangles are congruent?"\n' +
          '"Case (c) is a trick — can two triangles have the same SSA and NOT be congruent?"',
        sensemakingStrategy: 'Counterexample (SSA) creates productive cognitive conflict — why is SSA not sufficient?',
        formativeAssessment: 'Do students recognise case (b) as not congruent? This tests the definition of congruence.',
      },
      {
        phase: 'Observe Phase',
        learnerExperience:
          'Triangle card sort: 12 triangle cards with measurements. Sort into congruent pairs and identify the test used. ' +
          'SSS: all three sides equal. SAS: two sides and included angle. ASA: two angles and included side. AAS: two angles and non-included side.',
        resource:
          'MATERIAL: Triangle card sets (12 cards per group, pre-cut)\n' +
          'REFERENCE: Congruence test summary sheet',
        teacherMoves:
          '"Included angle means the angle BETWEEN the two sides. Which card pairs match each test?"\n' +
          '"Why is SSA not on the list? Draw a counterexample."',
        sensemakingStrategy:
          'Card sort is hands-on classification. Students discover the tests through sorting rather than memorising.',
        formativeAssessment: 'Check: are all four pairings correct? Are tests correctly identified?',
      },
      {
        phase: 'Explain Phase',
        learnerExperience:
          'Design challenge:\n' +
          '1. Design a base shape (triangle or quadrilateral) on a 4×4 grid\n' +
          '2. Reflect over the y-axis to create the right half\n' +
          '3. Reflect the top half over the x-axis to create the bottom half\n' +
          '4. Label all four congruent tiles, identifying the test that proves congruence\n' +
          '5. Colour and name the design\n' +
          'Display designs on the class wall.',
        resource:
          'MATERIAL: Squared paper, rulers, coloured pencils\n' +
          'INSPIRATION: Photographs of Kenyan kanga and kikoi textile patterns',
        teacherMoves:
          '"Your design must prove congruence — label the matching sides and angles."\n' +
          '"The four tiles are ALL congruent to each other — which test proves this?"',
        sensemakingStrategy:
          'Creative application integrates all unit content. Making something beautiful with mathematics is intrinsically motivating.',
        formativeAssessment: 'Design quality (accuracy of reflections) + congruence labelling (conceptual understanding).',
      },
      {
        phase: 'Driving Question Board (DQB) Creation',
        learnerExperience:
          'Final DQB review: all questions should be answered. Celebration activity — students physically move ' +
          'all remaining questions to ANSWERED. Class writes one-sentence answers to the driving question on the board.',
        resource: 'MATERIAL: DQB board, whiteboard markers',
        teacherMoves: '"What is your one-sentence answer to: How does reflection create balance, beauty, and precision?"',
        sensemakingStrategy: 'Unit closure through the DQB creates a sense of intellectual achievement.',
        formativeAssessment: 'Quality of one-sentence answers reveals depth of understanding.',
      },
      {
        phase: 'Model Building Phase',
        learnerExperience:
          'Final model revision and comparison:\n' +
          '• Place Lesson 1 model and Lesson 6 model side by side\n' +
          '• Write: "What I thought before / What I know now / What changed"\n' +
          '• Begin Final Explanation draft (to be completed as homework or in next assessment session)',
        resource: 'MATERIAL: Model Journal (all pages), Final Explanation template sheet',
        teacherMoves:
          '"Look at your Lesson 1 model. Were you right? What were you missing?"\n' +
          '"Your Final Explanation must answer the Driving Question using evidence from ALL 6 lessons."',
        sensemakingStrategy: 'Model comparison makes learning growth explicit and visible to the student.',
        formativeAssessment: 'Does the Lesson 6 model include: four properties, coordinate rules, inverse procedure, congruence connection?',
      },
    ],
    teacherReflection:
      'After teaching this lesson, reflect on:\n\n' +
      '1. Did students understand WHY SSA is not a valid congruence test? What counterexample worked best?\n\n' +
      '2. Were congruence tests connected to reflection (reflected images are always congruent) or treated as separate content?\n\n' +
      '3. Design challenge: did students apply reflection accurately, or did the creative element override the mathematical precision?\n\n' +
      '4. Comparing Lesson 1 and Lesson 6 models — what growth was most striking? What gaps remained?\n\n' +
      '5. Final Explanation quality: did students cite evidence from multiple lessons, or only Lesson 6?\n\n' +
      '6. Reflecting on the whole unit: what would you change about the lesson sequence? What worked best?',
    summaryTablePrompt: {
      observed:
        'Sorted triangle cards into congruent pairs using SSS, SAS, ASA, AAS tests. ' +
        'Created a symmetric 2×2 design tile by reflecting over x- and y-axes. ' +
        'DQB fully answered. Compared Lesson 1 and Lesson 6 models. Began Final Explanation.',
      learned:
        'Four congruence tests: SSS (three sides), SAS (two sides + included angle), ASA (two angles + included side), ' +
        'AAS (two angles + non-included side). SSA is NOT a valid test. ' +
        'Reflection always produces a congruent image — SAS test can prove this.',
      explained:
        'COMPLETE ANSWER: Reflection creates balance because every point on one side is equidistant from the mirror line, ' +
        'perpendicular to it, and congruent to its image. The KICC dome, Lake Nakuru flamingos, and kanga textiles all ' +
        'obey these exact mathematical rules. Reflection is not just beautiful — it is precise, calculable, and designable.',
    },
  },

];

// ── Final Explanation ──────────────────────────────────────────────────────
// TODO: extract from buildFinalExplanation() in the original generator
// See generators/data/SCHEMA.md for structure
const FINAL_EXPLANATION = null;  // fill in or extract manually

// ── Summary Table ──────────────────────────────────────────────────────────
// TODO: extract from buildSummaryTable() in the original generator
const SUMMARY_TABLE = null;  // fill in or extract manually

module.exports = { META, UNIT, LESSONS, FINAL_EXPLANATION, SUMMARY_TABLE };
