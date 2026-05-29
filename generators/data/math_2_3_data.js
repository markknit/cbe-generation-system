'use strict';
/**
 * math_2_3_data.js — Sub-strand data for universal generator
 * Auto-extracted from math_2_3_rotation.js
 * Run: node generators/generate.js math_2_3
 */

const META = {
  subject: 'Mathematics',
  grade: 10,
  outputDir: 'Grade 10 Math/Math 2.3 Rotation',
  filePrefix: 'Math_Rotation',
  col3Label: 'Teacher Actions',
  col5Label: 'Assessment Strategy',
};

const UNIT = {
  gradeLevel:  'Grade 10',
  subject:     'Mathematics',
  strand:      'Strand 2.0: Measurement and Geometry',
  substrand:   'Sub-Strand 2.3: Rotation',
  duration:    '6 lessons × 4 periods × 40 minutes = 960 minutes total',
  content:
    '• Centre, angle, and direction of rotation\n' +
    '• Rotation about the origin (90°, 180°, 270°, 360°)\n' +
    '• Rotation about any point\n' +
    '• Properties of rotation (distances and angles preserved)\n' +
    '• Determining the centre and angle of rotation given an object and its image\n' +
    '• Real-life applications of rotation',
  learningOutcomes:
    'By the end of the sub-strand, the learner should be able to:\n' +
    'a) identify the centre, angle, and direction of rotation\n' +
    'b) rotate a shape about the origin through given angles\n' +
    'c) rotate a shape about any given point\n' +
    'd) determine the centre and angle of rotation given an object and its image\n' +
    'e) state the properties of rotation\n' +
    'f) apply rotation in real-life situations',
  coreCompetencies:
    '• Critical Thinking and Problem Solving: deducing rotation rules from patterns\n' +
    '• Communication and Collaboration: presenting rotation constructions to peers\n' +
    '• Digital Literacy: using GeoGebra to explore rotation dynamically\n' +
    '• Learning to Learn: connecting rotation to prior knowledge of reflection and coordinates\n' +
    '• Self-Efficacy: building confidence with multi-step coordinate transformations\n' +
    '• Creativity and Innovation: designing rotating patterns for real applications',
  values:
    '• Respect: valuing diverse solution approaches\n' +
    '• Excellence: precision in geometric construction and coordinate calculations\n' +
    '• Integrity: showing all working steps clearly\n' +
    '• Responsibility: careful use of shared equipment\n' +
    '• Unity: collaborative group investigation',
  pcis:
    '• Environmental Education: wind energy and sustainable power in Kenya\n' +
    '• Technology: engineering applications of rotation (turbines, gears, clocks)',
  keyInquiry:
    'How does rotation — turning around a fixed point — create the motion and patterns that power machines, ' +
    'keep time, and generate energy in Kenya and beyond?',
  phenomenon:
    'The Ngong Hills Wind Farm (Lake Turkana Wind Power) has 365 wind turbines, each with 3 blades ' +
    'rotating about a central hub. A short time-lapse video shows one turbine blade tracing a full circle ' +
    'as it rotates 360°. Students observe: the blade tip travels in a circle; the hub (centre) stays fixed; ' +
    'different blades reach the same positions one after another.\n' +
    'Secondary: the second hand of a clock on the class wall makes exactly one rotation per minute. ' +
    'Anchor question: "What mathematical rules describe the journey of a point rotating around a fixed centre?"',
  drivingQuestion:
    'What mathematical rules describe how a point (or shape) moves when it rotates around a fixed centre — ' +
    'and how do engineers use these rules to design turbines, gears, and clocks?',
  storylineThread:
    'L1: Observe wind turbine rotation → identify centre, angle, direction → initial model\n' +
    'L2: Rotation about the origin — derive coordinate rules for 90°, 180°, 270°\n' +
    'L3: Rotation about any point — generalise using translation + origin rotation\n' +
    'L4: Properties of rotation — prove distances and angles are preserved\n' +
    'L5: Finding centre and angle of rotation — working backwards from object + image\n' +
    'L6: Real-world design challenge — turbine blade path, clock hands, gear ratios',
};

const LESSONS = [

  // ── LESSON 1 ─────────────────────────────────────────────────────────────
  {
    number: 1,
    aresKeywords: 'rotation centre angle transformation geometry',
    title:    'What Is Rotation? Centre, Angle, and Direction',
    duration: '4 periods / 160 minutes',
    slo: {
      purpose:
        'Students observe and describe rotation in Kenyan real-world contexts, ' +
        'identifying the three defining elements: centre of rotation, angle of rotation, and direction.',
      knowledge:
        '• Define rotation as a transformation that turns a shape around a fixed point\n' +
        '• Identify the centre of rotation, angle of rotation, and direction (clockwise/anticlockwise)\n' +
        '• Distinguish rotation from reflection and translation',
      skills:
        '• Identify the three rotation parameters in physical and photographic examples\n' +
        '• Estimate angles of rotation from visual inspection\n' +
        '• Use tracing paper to perform simple rotations',
      attitudes:
        '• Curiosity about the mathematics behind everyday rotating machines\n' +
        '• Appreciation of Kenya\'s renewable energy investment (Ngong Hills Wind Farm)',
      keyInquiry: 'How does rotation create the motion and patterns that power machines and keep time?',
      purposeInStoryline:
        'This lesson anchors the driving question in the wind turbine phenomenon. ' +
        'Students build intuitive understanding of the three rotation parameters before formal rules are introduced.',
      safetyNotes: 'Scissors for cutting tracing paper — use safety scissors.',
    },
    overview:
      'The lesson opens with a 90-second time-lapse video of the Ngong Hills Wind Farm at night ' +
      '(blades illuminated) and a close-up of a clock second hand. Students discuss: "What is the same about ' +
      'these two motions? What is different?" The class identifies: both have a fixed centre, both move through ' +
      'angles, both have a direction of spin.\n\n' +
      'Students then use tracing paper over printed diagrams to physically rotate shapes by given angles. ' +
      'The DQB is opened with questions about rotation rules, coordinate effects, and applications. ' +
      'Each student draws their initial model: "What is rotation and how does it work?"',
    framework: [
      {
        phase: 'Predict Phase',
        learnerExperience:
          'Watch the wind turbine video (or photograph). Groups discuss:\n' +
          '"Where is the fixed point? Through what angle does one blade move to reach the next blade\'s position? ' +
          'Is the rotation clockwise or anticlockwise (as seen from the front)?"\n' +
          'Record predictions before any teaching.',
        resource:
          'MATERIAL: Video/photograph of Ngong Hills turbine; clock on classroom wall\n' +
          'DIGITAL: YouTube — "Lake Turkana Wind Farm Kenya" (play first 60 seconds)',
        teacherMoves:
          '"There are THREE things you need to describe any rotation — what are they?"\n' +
          '"A turbine blade starts pointing straight up (12 o\'clock). Where is it after 120°? After 240°?"',
        sensemakingStrategy:
          'Phenomenon observation activates intuitive rotation knowledge. Three-parameter framework emerges from the context.',
        formativeAssessment:
          'Do students identify the hub (centre), angle, AND direction? Missing any of the three reveals a gap.',
      },
      {
        phase: 'Observe Phase',
        learnerExperience:
          'Tracing paper activity:\n' +
          '1. Place tracing paper over a printed shape. Trace the shape and mark the centre point with a pin/pencil.\n' +
          '2. Rotate the tracing paper 90° clockwise about the pin. Trace the new position — this is the image.\n' +
          '3. Repeat for 180° and 270° (both clockwise and anticlockwise).\n' +
          '4. Compare: 90° clockwise vs 270° anticlockwise — are they the same?',
        resource:
          'MATERIAL: Tracing paper, pencils, pins (or sharp pencil point), printed shape worksheets\n' +
          'OBSERVATION: 90° clockwise = 270° anticlockwise (equivalent rotations)',
        teacherMoves:
          '"Pin your pencil point exactly on the centre — if it slips, your image will be wrong."\n' +
          '"90° clockwise and 270° anticlockwise produce the same image. Why?"',
        sensemakingStrategy:
          'Embodied rotation using tracing paper makes the abstract concept physical and concrete.',
        formativeAssessment:
          'Do students correctly identify equivalent rotations (90° CW = 270° ACW)? ' +
          'Check tracing accuracy — does the image match where it should be?',
      },
      {
        phase: 'Explain Phase',
        learnerExperience:
          'Class discussion: formal definitions established.\n' +
          '• Centre of rotation: the fixed point that does not move\n' +
          '• Angle of rotation: the number of degrees turned\n' +
          '• Direction: clockwise (CW) or anticlockwise (ACW)\n' +
          'Students complete a "rotation vocabulary" card with definition + example for each term.\n' +
          'Comparison table: Rotation vs Reflection vs Translation — what stays fixed, what changes?',
        resource: 'MATERIAL: Vocabulary cards, whiteboard comparison table',
        teacherMoves:
          '"A rotation is fully described ONLY when you give all three: centre, angle, direction."\n' +
          '"Name one machine in your home or community that uses rotation. Identify its centre."',
        sensemakingStrategy:
          'Formal definition emerges from student observations. Comparison table prevents confusion between transformation types.',
        formativeAssessment:
          'Exit question: "Describe the rotation of the second hand of a clock from 12:00:00 to 12:00:20. ' +
          'Give centre, angle, and direction."',
      },
      {
        phase: 'Driving Question Board (DQB) Creation',
        learnerExperience:
          'Open the DQB. Students post questions: "What happens to the coordinates when you rotate?" ' +
          '"Can you rotate around a point that is NOT the origin?" "How do you find the centre if you only have the object and image?" ' +
          'Categorise under: COORDINATES / CENTRE / ANGLE / REAL LIFE.',
        resource: 'MATERIAL: DQB board, sticky notes',
        teacherMoves: '"Post any question — even if you think it is too hard. These will all be answered by Lesson 6."',
        sensemakingStrategy: 'DQB opens the intellectual agenda for the unit.',
        formativeAssessment: 'Review DQB after class — identifies what prior knowledge students are building on.',
      },
      {
        phase: 'Model Building Phase',
        learnerExperience:
          'Initial Model: "What is rotation and how does it work?" ' +
          'Draw the wind turbine (or any rotating object) and annotate: centre, angle, direction. ' +
          'Add any rules or patterns you already notice.',
        resource: 'MATERIAL: Model Journal page (Lesson 1)',
        teacherMoves:
          '"Your model is a snapshot of your thinking RIGHT NOW. Revise it each lesson."\n' +
          '"By Lesson 6, this model should contain coordinate rules, a centre-finding method, and real applications."',
        sensemakingStrategy: 'Initial model as baseline for growth tracking across 6 lessons.',
        formativeAssessment: 'Do students annotate all three rotation parameters on their model diagram?',
      },
    ],
    teacherReflection:
      'After teaching this lesson, reflect on:\n\n' +
      '1. Did the wind turbine video successfully anchor student curiosity? Which aspect generated most discussion — the centre, angle, or direction?\n\n' +
      '2. Tracing paper activity: were students able to keep the centre pin fixed accurately? What errors appeared?\n\n' +
      '3. Did students discover the equivalent rotation relationship (90° CW = 270° ACW) independently, or did you need to direct them?\n\n' +
      '4. Comparison table (Rotation vs Reflection vs Translation): which transformation caused most confusion?\n\n' +
      '5. DQB quality — are questions focused on coordinates (good — sets up Lesson 2) or only on the phenomenon (surface level)?\n\n' +
      '6. Initial models — do students distinguish rotation from spinning in place? Any who already know coordinate rules?',
    summaryTablePrompt: {
      observed:
        'Watched Ngong Hills wind turbine rotate — identified: hub is the centre (fixed point), blades sweep through 120° to reach the next position, ' +
        'rotation is anticlockwise as seen from the front. Rotated shapes using tracing paper through 90°, 180°, 270°. ' +
        'Discovered: 90° CW = 270° ACW. DQB opened.',
      learned:
        'Rotation is defined by THREE parameters: centre of rotation (fixed point), angle of rotation (degrees turned), and direction (CW or ACW). ' +
        'Equivalent rotations: 90° CW = 270° ACW; 180° CW = 180° ACW.',
      explained:
        'The wind turbine blade sweeps through 120° of rotation each time (360° ÷ 3 blades = 120°). ' +
        'The hub is the centre of rotation — it never moves. ' +
        'We can describe every blade position with just three numbers: centre, angle, direction. ' +
        'But we still need the COORDINATE RULE — that comes in Lesson 2.',
    },
  },

  // ── LESSON 2 ─────────────────────────────────────────────────────────────
  {
    number: 2,
    aresKeywords: 'rotation 90 180 degrees coordinate geometry',
    title:    'Rotation About the Origin — Coordinate Rules',
    duration: '4 periods / 160 minutes',
    slo: {
      purpose:
        'Students derive and apply coordinate rules for rotation about the origin through 90°, 180°, and 270°.',
      knowledge:
        '• State coordinate rules: 90° ACW → (x,y) → (−y,x); 180° → (−x,−y); 270° ACW → (y,−x)\n' +
        '• Explain why 90° CW gives the same image as 270° ACW\n' +
        '• State that 360° rotation maps every point to itself',
      skills:
        '• Apply coordinate rules to rotate points and polygons about the origin\n' +
        '• Plot images on the Cartesian plane and verify using tracing paper\n' +
        '• Identify the rotation from object and image coordinates',
      attitudes:
        '• Appreciation that algebraic rules make geometric transformations precise and fast\n' +
        '• Confidence with coordinate manipulation',
      keyInquiry: 'How does rotation create the motion and patterns that power machines and keep time?',
      purposeInStoryline:
        'The coordinate rules are the algebraic heart of rotation. Students move from the physical tracing-paper model ' +
        'to a precise mathematical rule that can be applied to any point without drawing.',
      safetyNotes: 'No specific safety notes.',
    },
    overview:
      'Students plot triangle A(1,2), B(3,1), C(2,4) on squared paper and rotate it 90° ACW about the origin using ' +
      'tracing paper. They record the image coordinates and look for the pattern. The rule (x,y)→(−y,x) is derived ' +
      'from the data. They then derive rules for 180° and 270° ACW by the same method.\n\n' +
      'GeoGebra is used to explore fractional and larger angles (e.g., 45°, 135°, 450°) as an extension. ' +
      'The turbine context is revisited: if a blade tip is at coordinates (0,5) — where is it after one-third turn (120°)?',
    framework: [
      {
        phase: 'Predict Phase',
        learnerExperience:
          'Point P(3,0) is on the positive x-axis. "If you rotate P 90° anticlockwise about the origin — where will it go? ' +
          'Predict the coordinates." Then predict for 180° and 270° ACW.',
        resource: 'MATERIAL: Blank paper, pencils',
        teacherMoves:
          '"Think about where P moves on a circle around the origin. 90° ACW from (3,0) — which quadrant?"\n' +
          '"Do not use the coordinate rule yet — sketch the circle and estimate."',
        sensemakingStrategy: 'Geometric prediction before algebraic rule makes the rule meaningful when it appears.',
        formativeAssessment: 'Do students predict (0,3) for 90° ACW? (−3,0) for 180°? (0,−3) for 270° ACW?',
      },
      {
        phase: 'Observe Phase',
        learnerExperience:
          'Squared paper investigation:\n' +
          '1. Plot triangle A(1,2), B(3,1), C(2,4).\n' +
          '2. Use tracing paper to rotate 90° ACW about origin. Mark and record image coordinates A\', B\', C\'.\n' +
          '3. Build a table: (x,y) and (x\',y\'). Find the pattern.\n' +
          '4. Repeat for 180° and 270° ACW.\n' +
          '5. Also rotate P(3,0) for all three angles — verify against predictions.',
        resource:
          'MATERIAL: Squared paper, tracing paper, rulers, pencils\n' +
          'DIGITAL: GeoGebra Rotation tool (for 45°/120° extension)',
        teacherMoves:
          '"Look at your table. The x-coordinate becomes ___? The y-coordinate becomes ___?"\n' +
          '"Test your rule on a fourth point you haven\'t plotted yet — does it work?"',
        sensemakingStrategy:
          'Inductive reasoning from tabulated coordinate data. Students own the rule because they discovered it.',
        formativeAssessment:
          'Check rule derivation: 90° ACW → (−y, x); 180° → (−x, −y); 270° ACW → (y, −x). ' +
          'Common error: confusing 90° CW with 90° ACW.',
      },
      {
        phase: 'Explain Phase',
        learnerExperience:
          'Consolidate three rules as a reference table:\n' +
          '| Rotation | Rule |\n' +
          '| 90° ACW (= 270° CW) | (x,y) → (−y, x) |\n' +
          '| 180° | (x,y) → (−x, −y) |\n' +
          '| 270° ACW (= 90° CW) | (x,y) → (y, −x) |\n' +
          '| 360° | (x,y) → (x, y) (identity) |\n' +
          'Apply rules to 6 practice problems. Wind turbine context: blade tip at (0, 5) after 120°? ' +
          '(Use GeoGebra or estimate — 120° is not a standard rule.)',
        resource:
          'MATERIAL: Practice worksheet (6 problems)\n' +
          'DIGITAL: GeoGebra for non-standard angles',
        teacherMoves:
          '"Memorising the table is less useful than understanding WHY x becomes −y. Draw the circle — does it make sense geometrically?"\n' +
          '"The 90° CW rule: (x,y) → (y,−x). How does this relate to the 270° ACW rule?"',
        sensemakingStrategy:
          'Rule consolidation with geometric justification. Students see the rules as logical consequences of circle geometry.',
        formativeAssessment: 'Practice problem accuracy. Can students explain the 90° ACW rule geometrically, not just apply it?',
      },
      {
        phase: 'Driving Question Board (DQB) Creation',
        learnerExperience:
          'Update DQB. Move "coordinates" questions to ANSWERED. New questions: ' +
          '"What if the centre is NOT the origin?" "How do I rotate around (2, 3)?" Add for Lesson 3.',
        resource: 'MATERIAL: DQB board',
        teacherMoves: '"Lesson 3 will give us the method for rotating around any point."',
        sensemakingStrategy: 'DQB maintains the unit narrative — each lesson closes some questions and opens new ones.',
        formativeAssessment: 'New questions confirm readiness for Lesson 3 content.',
      },
      {
        phase: 'Model Building Phase',
        learnerExperience:
          'Update Rotation Model: add the four coordinate rules table with a labelled worked example. ' +
          'Annotate the wind turbine diagram with coordinate positions for each blade at 0°, 120°, 240°.',
        resource: 'MATERIAL: Model Journal page (Lesson 2 revision)',
        teacherMoves: '"Your model should now show the ALGEBRAIC rules, not just the visual description."',
        sensemakingStrategy: 'Model integrates coordinate algebra with the turbine phenomenon.',
        formativeAssessment: 'Do models correctly state all four rules (including 360° identity)?',
      },
    ],
    teacherReflection:
      'After teaching this lesson, reflect on:\n\n' +
      '1. Did students predict the 90° ACW result correctly using geometric reasoning before the algebraic rule?\n\n' +
      '2. Most common error: confusing 90° CW (y,−x) with 90° ACW (−y,x). How did you address this?\n\n' +
      '3. Did students understand WHY (x,y)→(−y,x) for 90° ACW, or did they memorise it without understanding?\n\n' +
      '4. GeoGebra for non-standard angles (120° turbine blade): was this extension accessible to all, or only to stronger students?\n\n' +
      '5. How did the turbine context help connect Lesson 1 to Lesson 2?\n\n' +
      '6. What preparation do students need for Lesson 3 (rotation about any point)?',
    summaryTablePrompt: {
      observed:
        'Rotated triangle A(1,2), B(3,1), C(2,4) about the origin through 90°, 180°, 270° ACW using tracing paper. ' +
        'Tabulated object and image coordinates. Found patterns → derived three coordinate rules.',
      learned:
        'Three coordinate rules for rotation about the origin: ' +
        '90° ACW: (x,y)→(−y,x); 180°: (x,y)→(−x,−y); 270° ACW: (x,y)→(y,−x); 360°: (x,y)→(x,y). ' +
        '90° CW = 270° ACW (same result).',
      explained:
        'The wind turbine blade tip at (0,5) rotates 90° ACW to (−5,0) — pointing left. ' +
        'At 180° it is at (0,−5) — pointing down. At 270° ACW it is at (5,0) — pointing right. ' +
        'These are the exact positions seen in the time-lapse video.',
    },
  },

  // ── LESSON 3 ─────────────────────────────────────────────────────────────
  {
    number: 3,
    aresKeywords: 'rotation properties invariant point centre',
    title:    'Rotation About Any Point',
    duration: '4 periods / 160 minutes',
    slo: {
      purpose:
        'Students extend rotation to any centre point — not just the origin — ' +
        'using translation + origin rotation + translation back.',
      knowledge:
        '• Explain the three-step method: translate so centre becomes origin, rotate, translate back\n' +
        '• Apply the method to rotate a shape about any point\n' +
        '• Verify that the distance from each image vertex to the centre equals the distance from the object vertex',
      skills:
        '• Rotate a triangle about a centre point that is not the origin\n' +
        '• Apply the three-step coordinate method accurately\n' +
        '• Use tracing paper to verify results',
      attitudes:
        '• Persistence through multi-step calculations\n' +
        '• Appreciation that complex problems can be broken into simpler steps',
      keyInquiry: 'How does rotation create the motion and patterns that power machines and keep time?',
      purposeInStoryline:
        'Generalising from the origin to any centre is a key conceptual step. ' +
        'Students see that the origin rule is a special case of a general method.',
      safetyNotes: 'No specific safety notes.',
    },
    overview:
      'Teacher introduces the challenge: "Rotate triangle A(4,5), B(6,3), C(5,7) by 90° ACW about centre P(2,1)." ' +
      'Students attempt it directly — most will struggle or make errors. The teacher then reveals the three-step method: ' +
      '(1) translate so P becomes the origin (subtract P from all coordinates), ' +
      '(2) apply the 90° ACW origin rule, ' +
      '(3) translate back (add P to all coordinates).\n\n' +
      'Students practise with two further examples and verify with tracing paper. ' +
      'Context: the centre of a gear wheel is at (3,2) — rotate a tooth tip through 60°.',
    framework: [
      {
        phase: 'Predict Phase',
        learnerExperience:
          '"Rotate point Q(5,3) by 90° ACW about centre P(2,1). Predict Q\'." ' +
          'Students attempt using the origin rule directly (common error: forgetting to adjust for centre). ' +
          'Record predictions — these will likely be wrong and that is intentional.',
        resource: 'MATERIAL: Squared paper',
        teacherMoves:
          '"Try it with the rule (x,y)→(−y,x) directly. Does your answer feel right? Check with tracing paper."',
        sensemakingStrategy:
          'Structured failure: applying the origin rule directly to a non-origin centre produces an incorrect answer. ' +
          'This motivates the three-step method.',
        formativeAssessment: 'Verify: most predictions will be wrong. Use this as evidence that a new method is needed.',
      },
      {
        phase: 'Observe Phase',
        learnerExperience:
          'Teacher demonstrates the three-step method with Q(5,3) about P(2,1), 90° ACW:\n' +
          'Step 1: Translate — (5−2, 3−1) = (3,2) [P is now origin]\n' +
          'Step 2: Rotate 90° ACW about origin — (3,2) → (−2,3)\n' +
          'Step 3: Translate back — (−2+2, 3+1) = (0,4) = Q\'\n' +
          'Verify with tracing paper: pin on P, rotate 90° ACW — does Q land on (0,4)?\n' +
          'Students apply the same method to point R(6,5) about P(2,1), 90° ACW.',
        resource:
          'MATERIAL: Squared paper, tracing paper, rulers\n' +
          'WORKED EXAMPLE: Written on board with all three steps labelled',
        teacherMoves:
          '"The key insight: if we move P to the origin, we CAN use the Lesson 2 rules. Then we move back."\n' +
          '"What operation moves a point? Translation. What is the translation vector from P to origin?"',
        sensemakingStrategy:
          'Decomposition strategy: complex problem reduced to three familiar simpler operations.',
        formativeAssessment:
          'Check Step 1: are students subtracting the centre coordinates? ' +
          'Check Step 3: are they adding the centre coordinates back?',
      },
      {
        phase: 'Explain Phase',
        learnerExperience:
          'Apply the three-step method to rotate a full triangle:\n' +
          '• Problem A: Rotate triangle A(4,5), B(6,3), C(5,7) by 90° ACW about (2,1)\n' +
          '• Problem B: Rotate quadrilateral PQRS by 180° about centre (3,0)\n' +
          'Partners check each other\'s work. Class discusses: what is the same in every problem? ' +
          '(The three steps never change — only the centre and angle change.)',
        resource: 'MATERIAL: Coordinate geometry worksheet (2 problems)',
        teacherMoves:
          '"Generalise: write the three-step method as a formula using centre point (a,b):\n' +
          ' Step 1: (x−a, y−b) → Step 2: apply rule → Step 3: add (a,b) back."',
        sensemakingStrategy: 'Students move from specific examples to a generalised formula — algebraic abstraction.',
        formativeAssessment: 'Problem A answer: A\'(−2,3), B\'(0,5), C\'(−4,4) — check all three vertices.',
      },
      {
        phase: 'Driving Question Board (DQB) Creation',
        learnerExperience:
          'Update DQB. Move "rotation about any point" questions to ANSWERED. ' +
          'New questions: "How do I find the centre if I only have the before and after?" "Are the distances from centre preserved?"',
        resource: 'MATERIAL: DQB board',
        teacherMoves: '"The distance question is about PROPERTIES — that is Lesson 4."',
        sensemakingStrategy: 'DQB continues to build the unit narrative.',
        formativeAssessment: 'New questions about properties signal readiness for Lesson 4.',
      },
      {
        phase: 'Model Building Phase',
        learnerExperience:
          'Update Rotation Model: add the three-step method with a labelled worked example. ' +
          'Show that the Lesson 2 origin rules are a special case (when centre = origin, Steps 1 and 3 cancel out).',
        resource: 'MATERIAL: Model Journal page (Lesson 3 revision)',
        teacherMoves: '"Your model should now handle ANY centre. That is a generalisation — one of the most powerful ideas in mathematics."',
        sensemakingStrategy: 'Generalisation as the core mathematical move — specific (origin) becomes general (any point).',
        formativeAssessment: 'Do models correctly identify that origin rotation is a special case?',
      },
    ],
    teacherReflection:
      'After teaching this lesson, reflect on:\n\n' +
      '1. Did the structured failure (applying origin rule to non-origin centre) effectively motivate the three-step method?\n\n' +
      '2. Step 1 (subtracting centre) and Step 3 (adding centre back): did students understand WHY these steps work?\n\n' +
      '3. Most common error: subtracting the centre in Step 1 but forgetting to add it back in Step 3.\n\n' +
      '4. Could students generalise the method to a formula with centre (a,b)? Or did they need to work through concrete examples only?\n\n' +
      '5. Partner checking: did students correctly identify and fix each other\'s errors?\n\n' +
      '6. Did the gear wheel context (centre at (3,2)) add relevance, or was it confusing?',
    summaryTablePrompt: {
      observed:
        'Attempted (incorrectly) to rotate Q(5,3) about P(2,1) using the origin rule directly. ' +
        'Discovered the error via tracing paper. Learned the three-step method: translate to origin → rotate → translate back. ' +
        'Applied method to full triangle. Verified with tracing paper.',
      learned:
        'To rotate about any centre (a,b): Step 1 — subtract (a,b) from all coordinates to move centre to origin. ' +
        'Step 2 — apply the origin rotation rule. Step 3 — add (a,b) back. ' +
        'The Lesson 2 origin rules are the special case where (a,b) = (0,0).',
      explained:
        'The gear wheel at centre (3,2): a tooth tip rotates about (3,2), not the origin. ' +
        'With the three-step method, we can calculate the exact position of any tooth after any rotation — ' +
        'essential for engineers designing precise gear mechanisms.',
    },
  },

  // ── LESSON 4 ─────────────────────────────────────────────────────────────
  {
    number: 4,
    aresKeywords: 'rotational symmetry order centre shapes',
    title:    'Properties of Rotation',
    duration: '4 periods / 160 minutes',
    slo: {
      purpose:
        'Students investigate and prove the key properties of rotation: distances and angles are preserved, ' +
        'the centre is equidistant from object and image vertices.',
      knowledge:
        '• State that rotation preserves lengths (object and image are congruent)\n' +
        '• State that rotation preserves angles (angle between any two lines is preserved)\n' +
        '• State that the centre of rotation is equidistant from any object vertex and its corresponding image vertex\n' +
        '• Distinguish rotation from dilation (rotation preserves size; dilation does not)',
      skills:
        '• Measure distances from centre to object and image vertices\n' +
        '• Verify angle preservation using a protractor\n' +
        '• Use properties to identify whether a transformation is a rotation',
      attitudes:
        '• Mathematical rigour: proving properties rather than assuming them\n' +
        '• Appreciation that preserving distances and angles is what makes rotation useful in engineering',
      keyInquiry: 'How does rotation create the motion and patterns that power machines and keep time?',
      purposeInStoryline:
        'Properties confirm that rotation is a rigid transformation (isometry). ' +
        'This connects rotation to congruence (Lesson 2.2) and prepares for the centre-finding method (Lesson 5).',
      safetyNotes: 'Compass points are sharp — use with care.',
    },
    overview:
      'Students begin with a congruence question: "A turbine blade rotates 120°. Is the blade\'s shape and size preserved, ' +
      'or does rotation distort it?" The answer is yes — preserved. This motivates a formal investigation.\n\n' +
      'Groups measure distances from centre of rotation to object vertices (OA, OB, OC) and to image vertices ' +
      '(OA\', OB\', OC\'). They compare. They also measure object side lengths and image side lengths. ' +
      'The class derives: rotation is an isometry (rigid transformation). Finally, students learn to use ' +
      'the equidistance property to IDENTIFY the centre — by drawing circles around corresponding vertex pairs.',
    framework: [
      {
        phase: 'Predict Phase',
        learnerExperience:
          '"After rotating triangle ABC 90° ACW about origin O, is triangle A\'B\'C\' congruent to ABC? ' +
          'Which of the four congruence tests (from Lesson 2.2) would prove it? Predict before measuring."',
        resource: 'MATERIAL: Previously drawn rotation diagrams from Lesson 2 or 3',
        teacherMoves:
          '"Predict: are the side lengths the same? The angles? What do you expect from a \'turning\' transformation?"',
        sensemakingStrategy: 'Connecting rotation to congruence (prior unit) creates cross-topic coherence.',
        formativeAssessment: 'Do students predict congruence correctly? Do they suggest SSS as the test?',
      },
      {
        phase: 'Observe Phase',
        learnerExperience:
          'Measurement investigation:\n' +
          '1. On a rotation diagram (triangle rotated about O), measure: OA, OA\', OB, OB\', OC, OC\'.\n' +
          '2. Compare and tabulate.\n' +
          '3. Measure side lengths: AB, A\'B\', BC, B\'C\'.\n' +
          '4. Measure angles: ∠ABC and ∠A\'B\'C\'.\n' +
          '5. Conclusion: what is preserved?',
        resource:
          'MATERIAL: Protractors, rulers, rotation diagrams (printed, accurately constructed)\n' +
          'DIGITAL: GeoGebra to dynamically show that properties hold for ANY angle',
        teacherMoves:
          '"Measure to the nearest millimetre. Do OA and OA\' match exactly?"\n' +
          '"What word describes a transformation that preserves all lengths and angles?"',
        sensemakingStrategy:
          'Empirical verification of properties. Measurement confirms what coordinate algebra implies.',
        formativeAssessment:
          'Results: OA = OA\', OB = OB\', OC = OC\'; side lengths preserved; angles preserved. ' +
          'Deviations larger than 0.5 mm indicate construction errors.',
      },
      {
        phase: 'Explain Phase',
        learnerExperience:
          'Formally state three properties:\n' +
          '1. Distances preserved: |OP| = |OP\'| for every point P\n' +
          '2. Lengths preserved: |AB| = |A\'B\'| (rotation is an isometry)\n' +
          '3. Angles preserved: ∠ABC = ∠A\'B\'C\'\n' +
          'Isometry: a transformation that preserves all distances. (Rotation, reflection, and translation are all isometries.)\n' +
          'Application: use property 1 to identify the centre — the centre is the point equidistant from P and P\' for ALL corresponding pairs.',
        resource: 'MATERIAL: Whiteboard; student measurement tables',
        teacherMoves:
          '"The centre is the UNIQUE point equidistant from each object-image pair. How would you find it geometrically? (Hint: circles or perpendicular bisectors.)"',
        sensemakingStrategy: 'Formal statement of properties from empirical findings. Centre-finding hint previews Lesson 5.',
        formativeAssessment:
          '"True or false: rotation changes the size of a shape." (False — rotation is an isometry.) ' +
          '"True or false: rotation changes the orientation of a shape." (True — orientation is reversed for reflection, but for rotation it is preserved; clarify this common confusion.)',
      },
      {
        phase: 'Driving Question Board (DQB) Creation',
        learnerExperience:
          'Update DQB. Move "properties" questions to ANSWERED. ' +
          'Focus on remaining question: "How do I find the centre and angle if I only have object and image?"',
        resource: 'MATERIAL: DQB board',
        teacherMoves: '"That is exactly what Lesson 5 teaches. The equidistance property is the key."',
        sensemakingStrategy: 'DQB creates direct anticipation for Lesson 5.',
        formativeAssessment: 'Students should now be comfortable with isometry and ready for centre-finding.',
      },
      {
        phase: 'Model Building Phase',
        learnerExperience:
          'Update Rotation Model: add the three properties. ' +
          'Label the model diagram with: distance from centre to object vertex = distance from centre to image vertex.',
        resource: 'MATERIAL: Model Journal page (Lesson 4 revision)',
        teacherMoves: '"Your model should now prove that rotation preserves congruence — using SSS."',
        sensemakingStrategy: 'Model integrates isometry concept with congruence knowledge from prior unit.',
        formativeAssessment: 'Do models correctly state all three properties? Do they connect to congruence tests?',
      },
    ],
    teacherReflection:
      'After teaching this lesson, reflect on:\n\n' +
      '1. Did students connect rotation properties to congruence (Sub-Strand 2.2) effectively? Which congruence test did they apply?\n\n' +
      '2. Common confusion: "rotation changes orientation." In fact, rotation preserves orientation (unlike reflection). Did this arise? How did you clarify?\n\n' +
      '3. Were measurement results accurate enough to see that OA = OA\'? What precision issues arose?\n\n' +
      '4. GeoGebra: did the dynamic demonstration of properties help students trust the measurements?\n\n' +
      '5. The isometry concept — was this new vocabulary or did students know it from reflection?\n\n' +
      '6. Centre-finding hint: did students see how the equidistance property leads to a perpendicular bisector method?',
    summaryTablePrompt: {
      observed:
        'Measured distances from centre of rotation to object vertices (OA, OB, OC) and image vertices (OA\', OB\', OC\'): all equal. ' +
        'Measured side lengths and angles: all preserved. Verified using GeoGebra for dynamic confirmation.',
      learned:
        'Three properties of rotation: (1) distances from centre preserved (OA = OA\'), (2) side lengths preserved (isometry), ' +
        '(3) angles preserved. Rotation is an isometry — it does NOT change the size or shape of the figure.',
      explained:
        'A wind turbine blade must preserve its shape and size as it rotates — otherwise the blade would distort and fail. ' +
        'These three properties mathematically guarantee that every point on the blade stays exactly the same distance from the hub, ' +
        'sweeping a perfect circle. This is why rotation is used in engineering: it is predictable and precise.',
    },
  },

  // ── LESSON 5 ─────────────────────────────────────────────────────────────
  {
    number: 5,
    aresKeywords: 'rotation reflection combined transformation',
    title:    'Finding the Centre and Angle of Rotation',
    duration: '4 periods / 160 minutes',
    slo: {
      purpose:
        'Students determine the centre and angle of rotation given an object and its image, ' +
        'completing the full inverse problem of rotation.',
      knowledge:
        '• State that the centre of rotation lies on the perpendicular bisector of any segment PP\'\n' +
        '• Use two perpendicular bisectors to find the centre of rotation by intersection\n' +
        '• Calculate the angle of rotation using the angle ∠POP\'',
      skills:
        '• Construct perpendicular bisectors of at least two PP\' segments\n' +
        '• Find their intersection to locate the centre\n' +
        '• Use a protractor to measure ∠POP\' to find the angle of rotation',
      attitudes:
        '• Persistence with multi-step constructions\n' +
        '• Appreciation that inverse problems are as important as direct problems',
      keyInquiry: 'How does rotation create the motion and patterns that power machines and keep time?',
      purposeInStoryline:
        'The inverse problem — finding centre and angle — completes the rotation model. ' +
        'Students can now move in both directions: apply a rotation OR identify one from evidence.',
      safetyNotes: 'Compass use — sharp points, handle carefully.',
    },
    overview:
      'The lesson opens with an engineering challenge: "A gear tooth has moved from position A to position A\'. ' +
      'Find the centre of the gear wheel (the centre of rotation) and the angle it has turned."\n\n' +
      'Students recall the Lesson 4 property: the centre is equidistant from P and P\'. This means it lies on the ' +
      'perpendicular bisector of PP\'. Construct two perpendicular bisectors — their intersection IS the centre. ' +
      'Then measure ∠POP\' for the angle. Students apply the method to two challenge problems.',
    framework: [
      {
        phase: 'Predict Phase',
        learnerExperience:
          '"You are given triangle ABC and its image A\'B\'C\' but NOT the centre or angle. ' +
          'From what you know about rotation properties — how would you find the centre? Predict the METHOD before we derive it."',
        resource: 'MATERIAL: Printed diagrams showing object and image triangles',
        teacherMoves:
          '"Think about Lesson 4: the centre is equidistant from P and P\'. What geometric construction finds a point equidistant from two given points?"',
        sensemakingStrategy: 'Predicting the method activates Lesson 4 knowledge and creates ownership of the derivation.',
        formativeAssessment: 'Do students recall perpendicular bisector from Lesson 2.2? If not, brief revision needed.',
      },
      {
        phase: 'Observe Phase',
        learnerExperience:
          'Step-by-step construction:\n' +
          '1. Identify one corresponding pair: A and A\'.\n' +
          '2. Construct the perpendicular bisector of AA\'. (Centre lies somewhere on this line.)\n' +
          '3. Construct the perpendicular bisector of BB\'.\n' +
          '4. The intersection of the two perpendicular bisectors is the centre O.\n' +
          '5. Draw OA. Draw OA\'. Measure ∠AOA\' — this is the angle of rotation.\n' +
          '6. Verify: construct perpendicular bisector of CC\'. Does it also pass through O?',
        resource:
          'MATERIAL: Ruler, compass, protractor, printed diagrams\n' +
          'REMINDER: Perpendicular bisector construction from earlier geometry units',
        teacherMoves:
          '"Why do we need TWO perpendicular bisectors, not just one?"\n' +
          '"Step 6 is the verification step — if CC\' bisector also passes through O, our construction is correct."',
        sensemakingStrategy:
          'Multi-step geometric construction. Each step is justified by a property learned in Lesson 4.',
        formativeAssessment:
          'Check: are perpendicular bisectors accurately constructed (90° angle, equal distances)? ' +
          'Does the third bisector verify the intersection? Precision is critical.',
      },
      {
        phase: 'Explain Phase',
        learnerExperience:
          'Apply the method to two challenge problems:\n' +
          '• Problem A: Object and image given on Cartesian grid — find centre and angle\n' +
          '• Problem B: Object and image given as coordinates only — use coordinate method (midpoints + gradients) to find centre\n' +
          'Connect to Lesson 2.2 (mirror line finding was also a perpendicular bisector — the parallel structure!)',
        resource:
          'MATERIAL: Challenge worksheets (2 problems), rulers, compasses, protractors\n' +
          'DIGITAL: GeoGebra for verification',
        teacherMoves:
          '"Notice anything familiar? Reflection\'s mirror line finding used the SAME tool — perpendicular bisectors. ' +
          'Mathematics reuses its best ideas."',
        sensemakingStrategy:
          'Cross-topic connection: rotation centre finding = same perpendicular bisector approach as reflection mirror line. ' +
          'Highlights mathematical unity.',
        formativeAssessment:
          'Problem A: verify centre and angle are within 0.5 cm and 2° of correct values (geometric error tolerance). ' +
          'Problem B: algebraic method should be exact.',
      },
      {
        phase: 'Driving Question Board (DQB) Creation',
        learnerExperience:
          'DQB nearly complete. Move all centre/angle questions to ANSWERED. ' +
          'Only real-world application questions remain — for Lesson 6.',
        resource: 'MATERIAL: DQB board, green notes for ANSWERED',
        teacherMoves: '"Two lessons ago we couldn\'t find a centre. Now we can. That is genuine mathematical growth."',
        sensemakingStrategy: 'DQB review acknowledges and celebrates learning progression.',
        formativeAssessment: 'Only application questions remain — confirm readiness for Lesson 6.',
      },
      {
        phase: 'Model Building Phase',
        learnerExperience:
          'Major model revision: add the inverse method (centre + angle finding). ' +
          'Model should now show BOTH directions: given (centre, angle) → find image; AND given (object, image) → find centre and angle.',
        resource: 'MATERIAL: Model Journal page (Lesson 5 revision)',
        teacherMoves: '"Your model is now complete in BOTH directions — just like it was for reflection in Sub-Strand 2.2."',
        sensemakingStrategy: 'Bidirectional model represents full mastery. Parallel with reflection model reinforces curriculum coherence.',
        formativeAssessment: 'Do models show both directions clearly? Is the centre-finding procedure complete?',
      },
    ],
    teacherReflection:
      'After teaching this lesson, reflect on:\n\n' +
      '1. Did students recall perpendicular bisector construction from earlier work? Was revision necessary?\n\n' +
      '2. The parallel with Lesson 2.2 (reflection mirror line = perpendicular bisector) — did students make this connection themselves or need prompting?\n\n' +
      '3. Construction accuracy: were perpendicular bisectors correctly drawn (90°, bisecting exactly)? What errors appeared most?\n\n' +
      '4. Algebraic method (Problem B): were students comfortable using midpoint and gradient to find the centre algebraically?\n\n' +
      '5. Verification step (third perpendicular bisector through O): did students appreciate why this confirms the answer?\n\n' +
      '6. How ready do students seem for the Lesson 6 design challenge?',
    summaryTablePrompt: {
      observed:
        'Given object and image triangles without the centre or angle. Constructed perpendicular bisectors of two PP\' segments — ' +
        'their intersection is the centre O. Measured ∠AOA\' for the angle. Verified with a third PP\' bisector. ' +
        'Applied method to two challenge problems.',
      learned:
        'The centre of rotation lies on the perpendicular bisector of every segment PP\'. ' +
        'Two perpendicular bisectors intersect at the unique centre. ' +
        'Angle = ∠POP\'. Same perpendicular bisector tool used in Lesson 2.2 for reflection — mathematics reuses its best tools.',
      explained:
        'An engineer can photograph a gear tooth before and after one cycle — measure the two positions — ' +
        'and use perpendicular bisectors to find the exact centre and angle of rotation. ' +
        'No need to open the machine. Rotation is fully understood in both directions.',
    },
  },

  // ── LESSON 6 ─────────────────────────────────────────────────────────────
  {
    number: 6,
    aresKeywords: 'rotation transformation review assessment',
    title:    'Real-World Design Challenge — Turbines, Gears, and Clocks',
    duration: '4 periods / 160 minutes',
    slo: {
      purpose:
        'Students apply all rotation knowledge in a real-world engineering design challenge and write their final explanation.',
      knowledge:
        '• Connect all five lessons into a unified model of rotation\n' +
        '• Apply rotation rules to design a clock or turbine blade diagram\n' +
        '• Explain how rotation is used in real Kenyan engineering contexts',
      skills:
        '• Design a symmetric 3-blade turbine pattern using 120° rotations about the hub\n' +
        '• Calculate positions of all three blades at any time step\n' +
        '• Write a complete mathematical explanation answering the driving question',
      attitudes:
        '• Pride in applying mathematics to real engineering problems\n' +
        '• Appreciation of Kenya\'s renewable energy sector\n' +
        '• Confidence to explain complex mathematical ideas in writing',
      keyInquiry: 'How does rotation create the motion and patterns that power machines and keep time?',
      purposeInStoryline:
        'Unit closure. The design challenge applies all six lessons. ' +
        'The final explanation closes the driving question. ' +
        'Comparing Lesson 1 and Lesson 6 models shows full learning arc.',
      safetyNotes: 'No specific safety notes.',
    },
    overview:
      'The lesson presents two design challenges (students choose one):\n\n' +
      'CHALLENGE A (Turbine Design): Design a 3-blade wind turbine diagram. ' +
      'Blade 1 starts at position B₁(0,4). Find positions of all three blades (120° apart). ' +
      'Then calculate all blade positions after the turbine rotates 30°. ' +
      'Label all coordinates and state the rotation rules used.\n\n' +
      'CHALLENGE B (Clock Design): Design a clock face. Mark 12 hour positions as 30° rotation steps. ' +
      'Find the coordinates of the hour hand tip (length 3 units) at 12:00, 3:00, 6:00, 9:00, and 10:00. ' +
      'Verify using the appropriate rotation rules.\n\n' +
      'Both challenges require: coordinate calculations, rotation rules, and a written explanation. ' +
      'Lesson closes with model comparison and Final Explanation writing.',
    framework: [
      {
        phase: 'Predict Phase',
        learnerExperience:
          'Challenge A preview: "If Blade 1 is at (0,4), predict where Blade 2 and Blade 3 are." ' +
          'Challenge B preview: "If the hour hand points to 12 (0,3) — where does it point at 3:00? At 6:00?" ' +
          'Groups discuss and predict before calculating.',
        resource: 'MATERIAL: Challenge worksheets (A and B), squared paper',
        teacherMoves:
          '"For Challenge A: a full circle is 360°. Three blades equally spaced — each is how many degrees apart?"\n' +
          '"For Challenge B: 12 hours = 360°. One hour = how many degrees?"',
        sensemakingStrategy: 'Connecting rotation to real design contexts motivates precise calculation.',
        formativeAssessment: 'Do predictions use 120° spacing (Challenge A) and 30° per hour (Challenge B)?',
      },
      {
        phase: 'Observe Phase',
        learnerExperience:
          'Students work through their chosen challenge:\n' +
          'Challenge A:\n' +
          '• Blade 1: (0,4). Blade 2: rotate (0,4) by 120° ACW about origin.\n' +
          '  (0,4) → (−4sin60°, 4cos60°)... or use GeoGebra for non-standard angle.\n' +
          '  Exact: B₂ = (−4sin120°, 4cos120°) = (−2√3, −2) ≈ (−3.46, −2)\n' +
          '  B₃ = (2√3, −2) ≈ (3.46, −2)\n' +
          '• After 30° rotation: apply 30° rotation rule to all three blade tips.\n' +
          'Challenge B:\n' +
          '• 12:00 → (0,3); 3:00 → 90° CW → (3,0); 6:00 → 180° → (0,−3); 9:00 → 270° CW → (−3,0); 10:00 → 300° ACW.',
        resource:
          'MATERIAL: Challenge worksheets, squared paper, rulers\n' +
          'DIGITAL: GeoGebra for non-standard angles (30°, 120°)\n' +
          'REFERENCE: Rotation rules table from Lesson 2 model',
        teacherMoves:
          '"For 120° — you need GeoGebra or trigonometry. If you haven\'t done trig yet, estimate from the diagram."\n' +
          '"The standard rules (90°, 180°, 270°) are exact. 30° and 120° require trigonometry or technology."',
        sensemakingStrategy:
          'Open-ended challenge with differentiated pathways. Exact calculations use standard angles; GeoGebra handles non-standard.',
        formativeAssessment:
          'Challenge A: standard-angle students calculate 90°/180°/270° positions; GeoGebra students verify 120°/30° positions. ' +
          'Challenge B: students correctly apply CW rules for clockwise hour hand.',
      },
      {
        phase: 'Explain Phase',
        learnerExperience:
          'Present designs to class (2 minutes each). Must explain:\n' +
          '• Which rotation rules were used and why\n' +
          '• How the three rotation properties (distances/angles/isometry) appear in the design\n' +
          '• One real-world implication (turbine: equal blade spacing prevents vibration; clock: equal angle steps keep time)\n' +
          'Class votes on the most clearly explained and most accurately drawn design.',
        resource: 'MATERIAL: Completed challenge sheets for display',
        teacherMoves:
          '"Don\'t just show the diagram. Explain the MATHEMATICS behind each design choice."\n' +
          '"Why does a turbine need blades 120° apart? What would happen with 90° spacing (only 3 blades in a semicircle)?"',
        sensemakingStrategy:
          'Presentation makes mathematical reasoning explicit. Class feedback deepens understanding.',
        formativeAssessment: 'Quality of explanation (mathematical reasoning) + accuracy of diagram.',
      },
      {
        phase: 'Driving Question Board (DQB) Creation',
        learnerExperience:
          'Final DQB celebration. Every question from Lessons 1–6 is answered. ' +
          'Class writes one-sentence responses to the driving question. ' +
          'Students vote on the best one-sentence answer to display permanently.',
        resource: 'MATERIAL: DQB board, whiteboard',
        teacherMoves: '"What is your one-sentence answer to: How does rotation create motion, patterns, and power?"',
        sensemakingStrategy: 'DQB completion creates intellectual closure and celebrates student achievement.',
        formativeAssessment: 'Quality of one-sentence answers shows depth of unit understanding.',
      },
      {
        phase: 'Model Building Phase',
        learnerExperience:
          'Final model comparison: Lesson 1 vs Lesson 6.\n' +
          'Write: "What I thought before / What I know now / Biggest change in my thinking."\n' +
          'Begin Final Explanation (drafting the answer to the driving question with evidence from all 6 lessons).',
        resource: 'MATERIAL: Model Journal (all pages), Final Explanation template',
        teacherMoves:
          '"Your Lesson 6 model should contain: three rotation parameters, coordinate rules for 4 angles, ' +
          'three-step any-centre method, three properties, and the centre-finding method."\n' +
          '"Does your model now describe how the Ngong Hills turbine works mathematically?"',
        sensemakingStrategy: 'Model comparison makes learning growth explicit. Final explanation closes the unit narrative.',
        formativeAssessment: 'Does the Lesson 6 model contain all five components listed above?',
      },
    ],
    teacherReflection:
      'After teaching this lesson, reflect on:\n\n' +
      '1. Which challenge (A: turbine, B: clock) did most students choose? Was one better suited to the class?\n\n' +
      '2. Non-standard angles (120°, 30°) — did trigonometry knowledge (from other sub-strands) emerge, or did all students use GeoGebra?\n\n' +
      '3. Presentations: did students explain the MATHEMATICAL REASONING or just show the diagram?\n\n' +
      '4. Model comparison (Lesson 1 vs Lesson 6) — what growth was most striking? What content gaps remained?\n\n' +
      '5. Did students connect rotation to congruence (Sub-Strand 2.2)? This cross-topic link is important for the final exam.\n\n' +
      '6. Reflecting on the whole unit: what worked best in the 5-phase framework? What would you change?',
    summaryTablePrompt: {
      observed:
        'Completed turbine or clock design challenge using rotation rules. ' +
        'Calculated blade/hand positions using coordinate rules (90°/180°/270° standard; 30°/120° via GeoGebra). ' +
        'DQB fully answered. Compared Lesson 1 and Lesson 6 models. Began Final Explanation.',
      learned:
        'Rotation creates the periodic, predictable motion that engineers rely on — equal angle spacing prevents vibration ' +
        '(turbine), equal time steps create accurate timekeeping (clock). ' +
        'All six lesson tools (three parameters, coordinate rules, any-centre method, properties, centre-finding) work together ' +
        'to describe and design any rotation.',
      explained:
        'COMPLETE ANSWER: The Ngong Hills turbine blades rotate about a fixed hub (centre). ' +
        'Every point on a blade obeys the rotation coordinate rules — its position is calculable at any time. ' +
        'The three properties (distances, angles, isometry) guarantee no distortion. ' +
        'Engineers design the 120° blade spacing knowing that equal rotation angles create equal forces — ' +
        'the mathematics of rotation makes clean energy in Kenya possible.',
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
