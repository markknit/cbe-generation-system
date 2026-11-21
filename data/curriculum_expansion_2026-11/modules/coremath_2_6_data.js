'use strict';
module.exports = {
  "schemaVersion": "1.1.0",
  "META": {
    "subject": "Core Mathematics",
    "grade": 10,
    "substrand_id": "2.6",
    "substrand_name": "Area of a Part of a Circle",
    "outputDir": "v2/Core_Mathematics/SS2.6_Area_of_a_Part_of_a_Circle",
    "filePrefix": "Codex_Core_Mathematics_Area_of_a_Part_of_a_Circle",
    "titleDoc": "CORE MATHEMATICS GRADE 10: AREA OF A PART OF A CIRCLE",
    "subtitleDoc": "OpenAI-only evaluation • Sub-Strand 2.6 • 12 lessons • teacher review copy"
  },
  "UNIT": {
    "strand": "2.0 Measurements and Geometry",
    "substrand": "Sub-Strand 2.6: Area of a Part of a Circle",
    "sep": "Decompose plane regions, justify proportional area models, calculate and verify geometry.",
    "careers": "Illustrative applications in design, material planning and landscape layout; no qualification claims.",
    "focus": "Identify annuli, sectors, annular sectors, segments and circle overlaps, then justify their areas.",
    "phenomenon": "A paper design team gets conflicting area estimates because each person shades a different region.",
    "supportingPhenomena": "Ring paths, sector allocations, chord-cut segments and intersecting-circle designs.",
    "drivingQuestion": "How can we identify the exact region before choosing an area calculation? KICD: How do we use the concept of the area of a part of a circle in real life?",
    "storylineThread": "Annulus → applications → sectors → reverse angle → annular sector → minor/major segments → equal/unequal overlap → project → critique → independent transfer.",
    "coreCompetencies": "Creativity and Imagination: the learner makes an improvised dartboard of different numbers of concentric circles.\nLearning to Learn: the learner draws illustrations of two intersecting circles to identify the common area/part between the two circles.\nCommunication and collaboration: the learners engage to improvise locally available materials to make dartboards and beaded necklaces.",
    "values": "Responsibility: the learner makes dartboard of different numbers of concentric circles from the immediate environment\nUnity: the learner collaborates in a group and uses paper cutouts to make sectors of circles to determine their areas as part of a circle",
    "pcis": "Parental Engagement and Empowerment: the learner engages parents in using locally available materials for making improvised beaded necklaces.\nEnvironmental Education: the learner sources locally available materials to make necklaces and dartboards.\nLearner Support Programmes (Peer Education): the learner works with others to make necklaces using beading techniques of different coloured annular sectors.",
    "content": "Area of an annulus; Area of a sector of a circle; Area of an annular sector; Area of a segment; Area of common region between two intersecting circles; Application on the use of the area of a part of a circle",
    "gradeLevel": "10",
    "subject": "Core Mathematics",
    "totalDuration": "12 lessons × 40 minutes = 480 minutes",
    "learningOutcomes": "determine the area of an annulus in different situations,\nwork out the area of a sector of a circle in real-life situations,\ndetermine the area of an annular sector in different situations,\nwork out the area of a segment of a circle,\ndetermine the area of common region between two intersecting circles,\napply the area of a part of a circle in real-life situations,\nexplore the use of the area of a part of a circle in real-life situations."
  },
  "LESSONS": [
    {
      "number": 1,
      "title": "Which part of the circle is the ring?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand 2.6: Area of a Part of a Circle",
      "aresKeywords": "Area of a Part of a Circle",
      "slo": {
        "purpose": "Determine annulus area by removing the inner disk.",
        "knowledge": "Concentric ring area is the difference of two disk areas, not a disk of ring thickness.",
        "skills": "Label radii, shade a region and check an area difference.",
        "attitudes": "Record evidence honestly, listen respectfully and revise a claim when warranted.",
        "keyInquiry": "What must be removed from the outer disk?",
        "purposeInStoryline": "The design team begins by agreeing which region is being priced.",
        "safetyNotes": "Use printed tasks and calculators; keep personal information private and walkways clear."
      },
      "overview": "The design team begins by agreeing which region is being priced.\nMaterials: CM21. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Predict between 33π and 9π for the CM21 ring.",
          "teacherMoves": "4 minutes. Ask learners to shade the claimed region and retain initial choices.",
          "sensemakingStrategy": "Commit to an initial claim before comparing reasons.",
          "formativeAssessment": "Prediction names the included/excluded area."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Complete the circle/triangle diagnostic, then calculate CM21.",
          "teacherMoves": "16 minutes. Use 4 minutes diagnostic,8 ring work and 4 comparison; provide radius/diameter support before new work if needed.",
          "sensemakingStrategy": "Record evidence before discussing explanations.",
          "formativeAssessment": "Outer 49π,inner 16π anddifference 33π with square units."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Explain why thickness alone is insufficient.",
          "teacherMoves": "10 minutes. Compare the drawn ring with a radius 3 disk; factorR²−r² if helpful but preserve the geometric explanation.",
          "sensemakingStrategy": "Connect a claim to evidence and identify its limits.",
          "formativeAssessment": "Individual explanation identifies both squared radii."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Add questions about diameter and unknown radius to the board.",
          "teacherMoves": "4 minutes. Keep dimensions and inverse problems for Lesson 2.",
          "sensemakingStrategy": "Sort questions into answered, partly answered and still open.",
          "formativeAssessment": "A question identifies needed data."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Create a region → decomposition → formula → unit → check model.",
          "teacherMoves": "6 minutes. Collect each learner’s shaded/labelled solution; note prerequisite support needs.",
          "sensemakingStrategy": "Preserve the first model and annotate a justified revision.",
          "formativeAssessment": "Exit: verify ring+inner disk equals outer disk."
        }
      ],
      "teacherReflection": "Inspect the named learner evidence before the next lesson. Record the misconception, whose work shows it, and the next support or extension; do not infer individual mastery from a group product.",
      "summaryTablePrompt": {
        "observed": "Removing the radius 4 disk leaves the radius 7 ring.",
        "learned": "Annulus area subtracts squared radii.",
        "explained": "The ring 33π is smaller than 49π and restores the full disk with 16π."
      }
    },
    {
      "number": 2,
      "title": "Can the given dimensions really be used as radii?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand 2.6: Area of a Part of a Circle",
      "aresKeywords": "Area of a Part of a Circle",
      "slo": {
        "purpose": "Apply annulus reasoning to diameters and an unknown radius.",
        "knowledge": "Diameters must be halved; inverse area reasoning can recover a missing radius.",
        "skills": "Translate dimensions, solve and verify an inverse problem.",
        "attitudes": "Record evidence honestly, listen respectfully and revise a claim when warranted.",
        "keyInquiry": "How can we check a ring estimate against its dimensions?",
        "purposeInStoryline": "The team tests three differently worded ring specifications.",
        "safetyNotes": "Use printed tasks and calculators; keep personal information private and walkways clear."
      },
      "overview": "The team tests three differently worded ring specifications.\nMaterials: CM22. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Predict the radii of the 10 m/6 m diameter path.",
          "teacherMoves": "4 minutes. Ask learners to label a diameter across a whole circle before calculation.",
          "sensemakingStrategy": "Commit to an initial claim before comparing reasons.",
          "formativeAssessment": "Radii 5 and 3 are distinguished from diameters."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Solve CM22 A–C, annotating each change of dimensions.",
          "teacherMoves": "16 minutes. Allow 10 minutes solutions and 6 comparing checks; scaffold 169−r²=25 without giving r.",
          "sensemakingStrategy": "Record evidence before discussing explanations.",
          "formativeAssessment": "Areas 16π and 33π; unknown radius 12 and thickness 1."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Explain the inverse solution and its physical checks.",
          "teacherMoves": "10 minutes. Require 0<inner<outer and substitution into the original area.",
          "sensemakingStrategy": "Connect a claim to evidence and identify its limits.",
          "formativeAssessment": "Each learner justifies the positive geometric root."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Add questions about part-rings rather than full rings.",
          "teacherMoves": "4 minutes. Retain angle questions for the sector lessons.",
          "sensemakingStrategy": "Sort questions into answered, partly answered and still open.",
          "formativeAssessment": "An open question refers to a portion of 360°."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Revise the model to include dimension interpretation and assumptions.",
          "teacherMoves": "6 minutes. Collect one individual inverse solution and a diameter warning.",
          "sensemakingStrategy": "Preserve the first model and annotate a justified revision.",
          "formativeAssessment": "Exit: state the planar/concentric assumption for the path."
        }
      ],
      "teacherReflection": "Inspect the named learner evidence before the next lesson. Record the misconception, whose work shows it, and the next support or extension; do not infer individual mastery from a group product.",
      "summaryTablePrompt": {
        "observed": "Diameter and width descriptions can conceal the actual radii.",
        "learned": "Interpretation precedes annulus calculation.",
        "explained": "Substitution and dimensional bounds verify an inverse solution."
      }
    },
    {
      "number": 3,
      "title": "How much of the disk does a sector occupy?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand 2.6: Area of a Part of a Circle",
      "aresKeywords": "Area of a Part of a Circle",
      "slo": {
        "purpose": "Derive and apply sector area as an angular fraction.",
        "knowledge": "With a fixed radius, area scales with central angle; with fixed angle it scales with radius squared.",
        "skills": "Connect central-angle fractions to area and compare scale changes.",
        "attitudes": "Record evidence honestly, listen respectfully and revise a claim when warranted.",
        "keyInquiry": "Does twice the radius mean twice the sector area?",
        "purposeInStoryline": "The design now divides a disk into wedges.",
        "safetyNotes": "Use printed tasks and calculators; keep personal information private and walkways clear."
      },
      "overview": "The design now divides a disk into wedges.\nMaterials: CM23. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Predict the fraction represented by 120°.",
          "teacherMoves": "4 minutes. Show the full 360° disk and ask for a fraction before an area formula.",
          "sensemakingStrategy": "Commit to an initial claim before comparing reasons.",
          "formativeAssessment": "Learner states 1/3 of a whole disk."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Solve CM23 and compare the two 60° sectors.",
          "teacherMoves": "16 minutes. Allow 8 minutes fractions/areas,4 labelled sketches and 4 paired scaling explanation.",
          "sensemakingStrategy": "Record evidence before discussing explanations.",
          "formativeAssessment": "12π area; scaling radii 3→6 gives factor 4."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Explain the sector formula and distinguish area from arc length.",
          "teacherMoves": "10 minutes. Buildθ/360×whole-disk area from proportional reasoning; retain degree units forθ.",
          "sensemakingStrategy": "Connect a claim to evidence and identify its limits.",
          "formativeAssessment": "An individual can name the whole from which the fraction is taken."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Add reverse-angle questions to the board.",
          "teacherMoves": "4 minutes. Ask what information an area alone would still need.",
          "sensemakingStrategy": "Sort questions into answered, partly answered and still open.",
          "formativeAssessment": "Learners identify radius as necessary."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Add sector fraction and a radius-squared scaling check to the area model.",
          "teacherMoves": "6 minutes. Collect a labelled 90° example with square units.",
          "sensemakingStrategy": "Preserve the first model and annotate a justified revision.",
          "formativeAssessment": "Exit: explain why the 60° radius 6 sector is four times the radius 3 one."
        }
      ],
      "teacherReflection": "Inspect the named learner evidence before the next lesson. Record the misconception, whose work shows it, and the next support or extension; do not infer individual mastery from a group product.",
      "summaryTablePrompt": {
        "observed": "The 120° sector is one third of a disk.",
        "learned": "Sector area is the central-angle fraction ofπr².",
        "explained": "Doubling radius quadruples area at fixed angle."
      }
    },
    {
      "number": 4,
      "title": "Can an area determine the angle?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand 2.6: Area of a Part of a Circle",
      "aresKeywords": "Area of a Part of a Circle",
      "slo": {
        "purpose": "Use sector area in a context and recover a central angle.",
        "knowledge": "The area fraction equalsθ/360 at fixed radius; area and length have different units.",
        "skills": "Rearrange a relationship and interpret a planar design.",
        "attitudes": "Record evidence honestly, listen respectfully and revise a claim when warranted.",
        "keyInquiry": "What information does an area estimate actually provide?",
        "purposeInStoryline": "A planting design needs both an area and a defensible angle.",
        "safetyNotes": "Use printed tasks and calculators; keep personal information private and walkways clear."
      },
      "overview": "A planting design needs both an area and a defensible angle.\nMaterials: CM24. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Predict whether the flower sector is less than a quarter disk.",
          "teacherMoves": "4 minutes. Ask learners to compare 75° with 90° before multiplying.",
          "sensemakingStrategy": "Commit to an initial claim before comparing reasons.",
          "formativeAssessment": "Prediction gives a magnitude bound."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Solve both CM24 sectors and critique the supplier’s units.",
          "teacherMoves": "16 minutes. Allow 10 minutes calculations and 6 diagram/unit checking.",
          "sensemakingStrategy": "Record evidence before discussing explanations.",
          "formativeAssessment": "30π m²,60° and a clear area/arc distinction."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Explain angle recovery as an area ratio rather than a memorised rearrangement.",
          "teacherMoves": "10 minutes. Use 24π/144π=1/6 of a disk; ask what a price estimate would additionally require.",
          "sensemakingStrategy": "Connect a claim to evidence and identify its limits.",
          "formativeAssessment": "Each learner justifies 60° with a fraction check."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Record unknowns about real purchasing estimates.",
          "teacherMoves": "4 minutes. Keep price, waste and measurement assumptions open instead of inventing them.",
          "sensemakingStrategy": "Sort questions into answered, partly answered and still open.",
          "formativeAssessment": "A practical question names a missing datum."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Extend the area model with a reverse calculation and unit check.",
          "teacherMoves": "6 minutes. Collect an individual corrected supplier explanation.",
          "sensemakingStrategy": "Preserve the first model and annotate a justified revision.",
          "formativeAssessment": "Exit: distinguish metres from square metres."
        }
      ],
      "teacherReflection": "Inspect the named learner evidence before the next lesson. Record the misconception, whose work shows it, and the next support or extension; do not infer individual mastery from a group product.",
      "summaryTablePrompt": {
        "observed": "A sector area fraction can determine its angle.",
        "learned": "Reverse sector reasoning uses the same whole-disk relationship.",
        "explained": "An area quantity is not an arc length or a complete purchasing quote."
      }
    },
    {
      "number": 5,
      "title": "What if the sector has a circular hole?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand 2.6: Area of a Part of a Circle",
      "aresKeywords": "Area of a Part of a Circle",
      "slo": {
        "purpose": "Determine annular-sector area by subtracting matching sectors.",
        "knowledge": "Only matching angles/common centres justify the simple sector difference.",
        "skills": "Decompose an annular sector and test angle scaling.",
        "attitudes": "Record evidence honestly, listen respectfully and revise a claim when warranted.",
        "keyInquiry": "Which portions share the same angular fraction?",
        "purposeInStoryline": "The team removes a hole from its wedge design.",
        "safetyNotes": "Use printed tasks and calculators; keep personal information private and walkways clear."
      },
      "overview": "The team removes a hole from its wedge design.\nMaterials: CM25. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Predict whether ring thickness squared gives the shaded CM25 area.",
          "teacherMoves": "4 minutes. Require a sketch of both removed and retained sectors.",
          "sensemakingStrategy": "Commit to an initial claim before comparing reasons.",
          "formativeAssessment": "Initial claim identifies the two radii and common angle."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Calculate both sector areas, subtract and compare the wrong expression.",
          "teacherMoves": "16 minutes. Allow 9 minutes decomposition/calculation,4 comparison and 3 double-angle check.",
          "sensemakingStrategy": "Record evidence before discussing explanations.",
          "formativeAssessment": "12.8π cm²; wrong 3.2π;144° gives 25.6π."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Explain why the angle fraction multiplies the whole annulus difference.",
          "teacherMoves": "10 minutes. Check same bounding rays and centre; ask what fails with different angles.",
          "sensemakingStrategy": "Connect a claim to evidence and identify its limits.",
          "formativeAssessment": "Each learner states the conditions for the formula."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Add questions about curved regions cut by a chord.",
          "teacherMoves": "4 minutes. Keep the segment question distinct from ring/sector shapes.",
          "sensemakingStrategy": "Sort questions into answered, partly answered and still open.",
          "formativeAssessment": "A learner describes a chord rather than a radius."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Add annular-sector model and its conditions to the reference sheet.",
          "teacherMoves": "6 minutes. Collect an individual labelled equation and magnitude check.",
          "sensemakingStrategy": "Preserve the first model and annotate a justified revision.",
          "formativeAssessment": "Exit: explain what stays fixed when only the angle doubles."
        }
      ],
      "teacherReflection": "Inspect the named learner evidence before the next lesson. Record the misconception, whose work shows it, and the next support or extension; do not infer individual mastery from a group product.",
      "summaryTablePrompt": {
        "observed": "The annular sector subtracts two sectors of the same angle.",
        "learned": "Area=(θ/360)π(R²−r²).",
        "explained": "Ring thickness squared models the wrong region."
      }
    },
    {
      "number": 6,
      "title": "What lies between a chord and its arc?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand 2.6: Area of a Part of a Circle",
      "aresKeywords": "Area of a Part of a Circle",
      "slo": {
        "purpose": "Derive minor-segment area as sector minus triangle.",
        "knowledge": "A chord cuts off a segment; a central triangle occupies part of the sector.",
        "skills": "Identify a chord region, calculate two areas and subtract.",
        "attitudes": "Record evidence honestly, listen respectfully and revise a claim when warranted.",
        "keyInquiry": "Why does a segment need more than the sector formula?",
        "purposeInStoryline": "The design’s curved edge now meets a straight chord.",
        "safetyNotes": "Use printed tasks and calculators; keep personal information private and walkways clear."
      },
      "overview": "The design’s curved edge now meets a straight chord.\nMaterials: CM26. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Shade the segment on a copy before using the supplied shading.",
          "teacherMoves": "4 minutes. Ask learners to distinguish chord AB from radii OA/OB.",
          "sensemakingStrategy": "Commit to an initial claim before comparing reasons.",
          "formativeAssessment": "Shading identifies the region outside the triangle within the sector."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Calculate CM26 sector, triangle and minor segment.",
          "teacherMoves": "16 minutes. Allow 10 minutes area work and 6 sketch/check comparison; use the chord extension only after core work.",
          "sensemakingStrategy": "Record evidence before discussing explanations.",
          "formativeAssessment": "16π−32 cm²≈18.265; positive and less than the sector."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Explain each term and its units.",
          "teacherMoves": "10 minutes. Use a cut-and-reassemble paper explanation or diagram; distinguish chord 8√2 from arc 4π.",
          "sensemakingStrategy": "Connect a claim to evidence and identify its limits.",
          "formativeAssessment": "Each learner identifies exactly what the subtraction removes."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Add questions about non-right central triangles and major segments.",
          "teacherMoves": "4 minutes. Keep these as the next lesson’s questions rather than apply a right-triangle formula everywhere.",
          "sensemakingStrategy": "Sort questions into answered, partly answered and still open.",
          "formativeAssessment": "A learner notes which 90° fact made the triangle simple."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Add chord/arc and minor-segment decomposition to the model.",
          "teacherMoves": "6 minutes. Collect a labelled sketch and expression, not just a decimal.",
          "sensemakingStrategy": "Preserve the first model and annotate a justified revision.",
          "formativeAssessment": "Exit: explain why 16π alone is too large."
        }
      ],
      "teacherReflection": "Inspect the named learner evidence before the next lesson. Record the misconception, whose work shows it, and the next support or extension; do not infer individual mastery from a group product.",
      "summaryTablePrompt": {
        "observed": "The sector contains both the triangle and the minor segment.",
        "learned": "Minor-segment area is sector area minus central-triangle area.",
        "explained": "The right central triangle removes 32 cm² from 16π cm²."
      }
    },
    {
      "number": 7,
      "title": "How does the major segment differ?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand 2.6: Area of a Part of a Circle",
      "aresKeywords": "Area of a Part of a Circle",
      "slo": {
        "purpose": "Calculate a 60° minor segment and its complementary major segment.",
        "knowledge": "Triangle area can use included-angle sine or an equilateral height; a major segment is a disk complement.",
        "skills": "Use exact radical values and verify complementary areas.",
        "attitudes": "Record evidence honestly, listen respectfully and revise a claim when warranted.",
        "keyInquiry": "Which region should receive the triangle area?",
        "purposeInStoryline": "The team discovers that “major” changes the decomposition.",
        "safetyNotes": "Use printed tasks and calculators; keep personal information private and walkways clear."
      },
      "overview": "The team discovers that “major” changes the decomposition.\nMaterials: CM27. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Predict whether the minor 60° segment is smaller than its sector.",
          "teacherMoves": "4 minutes. Require a labelled sketch of the minor and major regions.",
          "sensemakingStrategy": "Commit to an initial claim before comparing reasons.",
          "formativeAssessment": "Initial model locates the central triangle."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Solve CM27 with the equilateral-height or sine route.",
          "teacherMoves": "16 minutes. Allow 10 minutes calculations and 6 comparing routes. Supply the height derivation if trig is insecure; document the support.",
          "sensemakingStrategy": "Record evidence before discussing explanations.",
          "formativeAssessment": "Minor 50π/3−25√3;major 250π/3+25√3."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Explain why major sector plus triangle is needed, or use full disk minus minor.",
          "teacherMoves": "10 minutes. Ask learners to reconstruct 100π from the two segment areas; check degree mode.",
          "sensemakingStrategy": "Connect a claim to evidence and identify its limits.",
          "formativeAssessment": "Each learner rejects the incorrect major-sector-minus-triangle rule with a diagram."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "List questions about two overlapping disks.",
          "teacherMoves": "4 minutes. Introduce the common chord idea without assuming equal segment areas.",
          "sensemakingStrategy": "Sort questions into answered, partly answered and still open.",
          "formativeAssessment": "Learners distinguish a segment in one disk from an overlap inside two."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Update the model with complementary-area and exact/approximate checks.",
          "teacherMoves": "6 minutes. Collect an individual major-segment explanation.",
          "sensemakingStrategy": "Preserve the first model and annotate a justified revision.",
          "formativeAssessment": "Exit: show minor+major=100π cm²."
        }
      ],
      "teacherReflection": "Inspect the named learner evidence before the next lesson. Record the misconception, whose work shows it, and the next support or extension; do not infer individual mastery from a group product.",
      "summaryTablePrompt": {
        "observed": "The same chord creates complementary minor and major segments.",
        "learned": "The major segment includes the triangle with the major sector.",
        "explained": "Complementing the minor segment avoids subtracting the wrong region."
      }
    },
    {
      "number": 8,
      "title": "Why does an overlap contain two segments?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand 2.6: Area of a Part of a Circle",
      "aresKeywords": "Area of a Part of a Circle",
      "slo": {
        "purpose": "Determine the common area of two equal intersecting circles.",
        "knowledge": "The common chord separates the lens into two congruent minor segments in this geometry.",
        "skills": "Decompose overlap and justify doubling using symmetry.",
        "attitudes": "Record evidence honestly, listen respectfully and revise a claim when warranted.",
        "keyInquiry": "What is inside both disks rather than either disk?",
        "purposeInStoryline": "A two-circle ornament introduces a common region.",
        "safetyNotes": "Use printed tasks and calculators; keep personal information private and walkways clear."
      },
      "overview": "A two-circle ornament introduces a common region.\nMaterials: CM28. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Shade the points inside both circles and predict the pieces needed.",
          "teacherMoves": "4 minutes. Contrast intersection with the union of disks; show no worked area.",
          "sensemakingStrategy": "Commit to an initial claim before comparing reasons.",
          "formativeAssessment": "Shading matches the lens rather than two whole disks."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Use CM28 dimensions and 90° angles to calculate each piece.",
          "teacherMoves": "16 minutes. Allow 10 minutes calculations and 6 comparing decompositions. Ask why the pieces are congruent.",
          "sensemakingStrategy": "Record evidence before discussing explanations.",
          "formativeAssessment": "Overlap 25π/2−25≈14.270 cm² with two triangles removed."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Explain what permits doubling and check against one disk.",
          "teacherMoves": "10 minutes. Trace both minor arcs and the common chord; ask whether unequal radii would preserve the argument.",
          "sensemakingStrategy": "Connect a claim to evidence and identify its limits.",
          "formativeAssessment": "Each learner names equal corresponding segment areas as the reason."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Add the unequal-circle question to the board.",
          "teacherMoves": "4 minutes. Do not generalise the symmetric shortcut without evidence.",
          "sensemakingStrategy": "Sort questions into answered, partly answered and still open.",
          "formativeAssessment": "An open question identifies symmetry as a condition."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Add an overlap-as-segment-sum diagram to the reference model.",
          "teacherMoves": "6 minutes. Collect the labelled decomposition and less-than-one-disk check.",
          "sensemakingStrategy": "Preserve the first model and annotate a justified revision.",
          "formativeAssessment": "Exit: explain why adding whole circle areas cannot isolate overlap."
        }
      ],
      "teacherReflection": "Inspect the named learner evidence before the next lesson. Record the misconception, whose work shows it, and the next support or extension; do not infer individual mastery from a group product.",
      "summaryTablePrompt": {
        "observed": "The common chord divides the overlap into two equal segments.",
        "learned": "Equal-circle symmetry permits twice one segment here.",
        "explained": "The intersection is 25π/2−25, smaller than either 25π disk."
      }
    },
    {
      "number": 9,
      "title": "What changes when the circle radii differ?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand 2.6: Area of a Part of a Circle",
      "aresKeywords": "Area of a Part of a Circle",
      "slo": {
        "purpose": "Calculate an unequal-circle overlap from sufficient intersection geometry.",
        "knowledge": "Each circle contributes its own segment; the corresponding areas need not match.",
        "skills": "Use supplied angles, degree mode and a kite-area check.",
        "attitudes": "Record evidence honestly, listen respectfully and revise a claim when warranted.",
        "keyInquiry": "Can we reuse the equal-circle shortcut?",
        "purposeInStoryline": "The ornament supplier now uses two different circle sizes.",
        "safetyNotes": "Use printed tasks and calculators; keep personal information private and walkways clear."
      },
      "overview": "The ornament supplier now uses two different circle sizes.\nMaterials: CM29. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Predict whether the two segment areas in CM29 are equal.",
          "teacherMoves": "4 minutes. Ask learners to identify the two radii and central angles before any calculation.",
          "sensemakingStrategy": "Commit to an initial claim before comparing reasons.",
          "formativeAssessment": "Initial claim refers to the actual geometry."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Calculate sector areas and subtract the two central triangles using full precision.",
          "teacherMoves": "16 minutes. Allow 12 minutes organised calculation and 4 partner checks; angles are supplied so inverse-trig derivation is an extension.",
          "sensemakingStrategy": "Record evidence before discussing explanations.",
          "formativeAssessment": "Triangle areas 4.32 and 7.68; final overlap≈6.642 cm²."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Explain the segment-sum method and verify triangle sum by the right-triangle kite.",
          "teacherMoves": "10 minutes. Compare 2×(1/2×3×4)=12 with 4.32+7.68; do not double just one curved segment.",
          "sensemakingStrategy": "Connect a claim to evidence and identify its limits.",
          "formativeAssessment": "Each learner explains why the two independent segment calculations are needed."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Audit what information an unfamiliar overlap problem must supply.",
          "teacherMoves": "4 minutes. Record radii plus sufficient intersection geometry/angles; a picture alone is insufficient.",
          "sensemakingStrategy": "Sort questions into answered, partly answered and still open.",
          "formativeAssessment": "A learner names a missing-data risk."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Add unequal-sector decomposition and full-precision rules to the model.",
          "teacherMoves": "6 minutes. Collect a labelled two-column calculation with units and a magnitude check.",
          "sensemakingStrategy": "Preserve the first model and annotate a justified revision.",
          "formativeAssessment": "Exit: identify an invalid doubling assumption."
        }
      ],
      "teacherReflection": "Inspect the named learner evidence before the next lesson. Record the misconception, whose work shows it, and the next support or extension; do not infer individual mastery from a group product.",
      "summaryTablePrompt": {
        "observed": "Unequal circles contribute unequal segment areas.",
        "learned": "Overlap is the sum of the appropriate two segment areas.",
        "explained": "The kite check verifies the total triangle subtraction of 12 cm²."
      }
    },
    {
      "number": 10,
      "title": "Can we make a useful and safe circular design?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand 2.6: Area of a Part of a Circle",
      "aresKeywords": "Area of a Part of a Circle",
      "slo": {
        "purpose": "Apply part-circle area in a paper project and communicate its limits.",
        "knowledge": "A design model can guide area estimation while omitting real material waste/thickness.",
        "skills": "Create a labelled model and supply individual calculations.",
        "attitudes": "Record evidence honestly, listen respectfully and revise a claim when warranted.",
        "keyInquiry": "How can geometric area inform a practical design?",
        "purposeInStoryline": "The team turns its reference model into a safe paper design.",
        "safetyNotes": "Paper-only project: no darts or throwing, no risky object measurements. Use pre-cut paper or an accurate drawing; adult-supervised scissors only under school policy. Home/family participation optional and ungraded. Full-size circle diameter 24 cm needs suitable paper; use the CM210 1:2 drawing option if needed and retain original dimensions for calculations."
      },
      "overview": "The team turns its reference model into a safe paper design.\nMaterials: CM210. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Predict the angle and area fraction of one of eight equal ring pieces.",
          "teacherMoves": "4 minutes. Ask for division of 360° before construction; show prepared paper and compass/protractor/ruler or cut pieces, with the CM210 scaled-drawing option.",
          "sensemakingStrategy": "Commit to an initial claim before comparing reasons.",
          "formativeAssessment": "Each learner predicts 45° and one-eighth of the ring."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Make a model/diagram and calculate the ring and one piece.",
          "teacherMoves": "16 minutes. Allow 8 minutes construction,5 calculation and 3 comparisons; use pre-cut or drawn alternatives. Record individual work.",
          "sensemakingStrategy": "Record evidence before discussing explanations.",
          "formativeAssessment": "Ring 80π;onepiece 10π cm², with radii 12 and 8."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Explain one use, a waste implication and a model limitation.",
          "teacherMoves": "10 minutes. Ask how eight pieces reconstruct the ring; distinguish collaboration evidence from individual area reasoning.",
          "sensemakingStrategy": "Connect a claim to evidence and identify its limits.",
          "formativeAssessment": "Each learner connects a number to a proposed use and a limitation."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Record unanswered real-material questions.",
          "teacherMoves": "4 minutes. Keep thickness, cutting loss and joining allowance as missing data rather than invent values.",
          "sensemakingStrategy": "Sort questions into answered, partly answered and still open.",
          "formativeAssessment": "A practical question identifies an omitted physical factor."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Submit the group design with a separate individual calculation/reflection.",
          "teacherMoves": "6 minutes. Assess geometry independently of decoration or home resources; collect evidence of participation separately.",
          "sensemakingStrategy": "Preserve the first model and annotate a justified revision.",
          "formativeAssessment": "Individual evidence includes a calculation, use and limitation."
        }
      ],
      "teacherReflection": "Inspect the named learner evidence before the next lesson. Record the misconception, whose work shows it, and the next support or extension; do not infer individual mastery from a group product.",
      "summaryTablePrompt": {
        "observed": "Eight annular sectors reconstruct a ring.",
        "learned": "Area models can support design choices with explicit assumptions.",
        "explained": "Each 10π cm² piece is a planar estimate, not a full manufacturing specification."
      }
    },
    {
      "number": 11,
      "title": "Which decomposition deserves our confidence?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand 2.6: Area of a Part of a Circle",
      "aresKeywords": "Area of a Part of a Circle",
      "slo": {
        "purpose": "Critique incorrect area models and justify a safe local application.",
        "knowledge": "The correct formula depends on the shaded region and supplied geometric conditions.",
        "skills": "Diagnose errors, state assumptions and communicate a model.",
        "attitudes": "Record evidence honestly, listen respectfully and revise a claim when warranted.",
        "keyInquiry": "What should we check before trusting an area answer?",
        "purposeInStoryline": "The team audits its reference sheet before an independent commission.",
        "safetyNotes": "Use printed tasks and calculators; keep personal information private and walkways clear."
      },
      "overview": "The team audits its reference sheet before an independent commission.\nMaterials: CM211. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Mark each CM211 claim provisionally true/false with a region sketch.",
          "teacherMoves": "4 minutes. Require a geometric reason rather than a vote or familiar formula.",
          "sensemakingStrategy": "Commit to an initial claim before comparing reasons.",
          "formativeAssessment": "Initial classifications are supported by a marked region."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Correct A/D, verify B/C and outline a safe local/drawn application.",
          "teacherMoves": "16 minutes. Allow 8 minutes claim audit and 8 modelling; no excursions or dangerous measurements.",
          "sensemakingStrategy": "Record evidence before discussing explanations.",
          "formativeAssessment": "A56π;B4π;C4π−8;Drequires appropriate segment geometry and symmetry to double."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Defend the chosen decomposition, units, check and limitation.",
          "teacherMoves": "10 minutes. Ask peers to test one stated assumption; distinguish a drawn plan from evidence of actual measuring.",
          "sensemakingStrategy": "Connect a claim to evidence and identify its limits.",
          "formativeAssessment": "Each learner gives enough dimensions/conditions to make the model solvable."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Review board questions and retain genuinely unresolved practical issues.",
          "teacherMoves": "4 minutes. Close only questions supported by completed evidence; note prerequisite or access support still required.",
          "sensemakingStrategy": "Sort questions into answered, partly answered and still open.",
          "formativeAssessment": "At least one limit is recorded honestly."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Produce an individual final reference model with a corrected claim and application.",
          "teacherMoves": "6 minutes. Collect for formative feedback; remove these teaching sheets before independent assessment.",
          "sensemakingStrategy": "Preserve the first model and annotate a justified revision.",
          "formativeAssessment": "Exit: explain a useful area application and the data it requires."
        }
      ],
      "teacherReflection": "Inspect the named learner evidence before the next lesson. Record the misconception, whose work shows it, and the next support or extension; do not infer individual mastery from a group product.",
      "summaryTablePrompt": {
        "observed": "Some correct-looking formulas describe the wrong region.",
        "learned": "A defensible model starts with region and conditions.",
        "explained": "Dimension, decomposition, unit and magnitude checks work together."
      }
    },
    {
      "number": 12,
      "title": "Independent part-circle design commission",
      "duration": "40 minutes",
      "substrand": "Sub-Strand 2.6: Area of a Part of a Circle",
      "aresKeywords": "Area of a Part of a Circle",
      "slo": {
        "purpose": "Independently calculate and justify unfamiliar part-circle areas.",
        "knowledge": "Region decomposition remains essential when formulas are provided.",
        "skills": "Solve new geometric tasks and explain application limits.",
        "attitudes": "Record evidence honestly, listen respectfully and revise a claim when warranted.",
        "keyInquiry": "Can I defend my area model without a partner?",
        "purposeInStoryline": "A new paper-design commission uses unfamiliar dimensions.",
        "safetyNotes": "Use printed tasks and calculators; keep personal information private and walkways clear."
      },
      "overview": "A new paper-design commission uses unfamiliar dimensions.\nMaterials: CM212. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 3 min, Observe 18 min, Explain 13 min, Driving Question Board (DQB) Creation 2 min, Model Building 4 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Read instructions, formula support and diagram data.",
          "teacherMoves": "3 minutes. Distribute CM212 and final task prompts; answer only procedural/access questions.",
          "sensemakingStrategy": "Individual work only; no comparison, hints or answer discussion before collection.",
          "formativeAssessment": "Each learner understands diagram dimensions rather than print measurement."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Complete annulus, sector and annular-sector tasks independently.",
          "teacherMoves": "18 minutes. Allow 18 minutes; no hints about the subtraction or angle fraction.",
          "sensemakingStrategy": "Individual work only; no comparison, hints or answer discussion before collection.",
          "formativeAssessment": "Individual diagrams, expressions and square units are visible."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Complete segment, overlap and application explanations independently.",
          "teacherMoves": "13 minutes. Allow 13 minutes; observe degree-mode use without coaching a calculation.",
          "sensemakingStrategy": "Individual work only; no comparison, hints or answer discussion before collection.",
          "formativeAssessment": "Collected work provides independent decomposition reasoning."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Identify one remaining check or model limitation privately.",
          "teacherMoves": "2 minutes. Allow 2 minutes; no group question-board discussion during the task.",
          "sensemakingStrategy": "Individual work only; no comparison, hints or answer discussion before collection.",
          "formativeAssessment": "A limit refers to the actual model or use."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Check units, region labels and completion; submit.",
          "teacherMoves": "4 minutes. Allow 4 minutes and collect all sheets before discussing answers.",
          "sensemakingStrategy": "Individual work only; no comparison, hints or answer discussion before collection.",
          "formativeAssessment": "Independent work is secured before any exemplar is shown."
        }
      ],
      "teacherReflection": "Inspect the named learner evidence before the next lesson. Record the misconception, whose work shows it, and the next support or extension; do not infer individual mastery from a group product.",
      "summaryTablePrompt": {
        "observed": "New dimensions reveal individual area-model reasoning.",
        "learned": "Teacher records demonstrated skills after collection.",
        "explained": "Feedback follows the collected decompositions and checks, not group project appearance."
      }
    }
  ],
  "FINAL_EXPLANATION": {
    "subjectLabel": "AREA OF A PART OF A CIRCLE",
    "instructions": "Lesson 12,40 minutes including 3 minutes procedure and 4 minutes final checking. Work independently with CM212 and a scientific calculator in degree mode. Show a labelled region/decomposition and an exact area expression; approximate to 3 decimal places where requested. Formula support on CM212 is allowed; no teaching cards. Use square units. Project participation/use exploration also has formative evidence in Lessons 10–11; this written task does not certify physical making skills.",
    "sections": [
      {
        "title": "1. Ring area and a check",
        "prompt": "Find annulus A area exactly. Explain why the difference of squared radii is appropriate and verify by recombining with the inner disk.",
        "exemplar": "π(8²−5²)=39π cm²;39π+25π=64π restores the outer disk. Both circular boundaries share a centre; subtract the inner disk, not a disk of radius 8−5."
      },
      {
        "title": "2. Sector and annular-sector comparison",
        "prompt": "Find B and C areas exactly and explain the difference between the two decompositions. Check that adding C to the matching radius 6 sector restores B.",
        "exemplar": "B=(80/360)π9²=18π cm². C=(80/360)π(81−36)=10π cm². Matching radius 6 sector 8π;10π+8π=18π. The hole removes the smaller sector with the same centre and angle."
      },
      {
        "title": "3. Minor segment",
        "prompt": "Find D’s minor-segment area exactly and approximately. Explain the triangle subtraction and check that the result is positive and less than the sector.",
        "exemplar": "Sector 25π cm²; right central triangle 50 cm²; segment 25π−50≈28.540 cm². The chord bounds a region outside the triangle but within the 90° sector.0<25π−50<25π."
      },
      {
        "title": "4. Intersecting-circle overlap",
        "prompt": "Find E’s common area exactly and approximately. Explain why two segment areas are added and why doubling is valid in this case. State a size check.",
        "exemplar": "Each segment(60/360)π36−(1/2)36 sin 60°=6π−9√3. Overlap 12π−18√3≈6.522 cm². The common chord divides the lens into congruent segments because equal radii/central angles give equal geometry. It is positive and less than one 36π cm² disk."
      },
      {
        "title": "5. Explore a safe design use",
        "prompt": "Choose A or C as a proposed paper ornament. Explain what its computed area would estimate, one benefit of that estimate and one further datum/assumption needed for real material planning. Describe one safe next step to explore the proposed use. This is a written plan; no physical making is required.",
        "exemplar": "For C,10π cm² estimates the planar area of one ornament piece. It can help compare intended material quantities, but cutting waste, joining allowance and thickness are not included. A safe next step is a labelled paper template using the stated radii/angle with teacher-approved tools. Accept a similarly justified annulus example. Do not infer actual practical skill from the written plan."
      }
    ],
    "rubric": [
      {
        "criterion": "Determine and explain annulus, sector and annular-sector areas",
        "excellent": "All three exact areas, matching-region explanations and recombination checks are correct and clearly labelled.",
        "proficient": "Correct areas and decompositions with valid recombination checks and square units.",
        "developing": "Some correct model/area work but a radius, angle fraction, subtraction or unit needs correction.",
        "belowExpectations": "Needs guided region identification before selecting a formula."
      },
      {
        "criterion": "Determine and justify a minor-segment area",
        "excellent": "Correct exact/approximate result, triangle explanation and both size checks, supported by a clear diagram.",
        "proficient": "Correct sector-minus-triangle result and explanation with a valid size check.",
        "developing": "Identifies the sector/triangle but a calculation, subtraction or explanation is incomplete.",
        "belowExpectations": "Needs guided support to distinguish the segment from the sector or triangle."
      },
      {
        "criterion": "Determine and justify the common area of intersecting circles",
        "excellent": "Correct exact/approximate area with a clear two-segment decomposition, valid symmetry explanation and size check.",
        "proficient": "Correct overlap calculation and explanation of why the two equal segments can be doubled here.",
        "developing": "Some correct segment reasoning but calculation, symmetry condition or interpretation needs correction.",
        "belowExpectations": "Needs guided work to identify the intersection and its component segments."
      },
      {
        "criterion": "Explain and explore a practical use with limits",
        "excellent": "Connects the selected area to a specific benefit, relevant omitted factor and safe concrete next step without overclaiming the model.",
        "proficient": "Explains a relevant use, benefit, limitation and safe exploration step.",
        "developing": "A relevant use is proposed but the quantity, limitation or next step is vague.",
        "belowExpectations": "Needs prompts to connect the planar area to a usable design estimate."
      }
    ]
  },
  "SUMMARY_TABLE": {
    "subStrand": "Sub-Strand 2.6: Area of a Part of a Circle",
    "drivingQuestion": "How can we identify the exact region before choosing an area calculation? KICD: How do we use the concept of the area of a part of a circle in real life?",
    "lessons": [
      {
        "number": 1,
        "title": "Which part of the circle is the ring?",
        "observed": "Removing the radius 4 disk leaves the radius 7 ring.",
        "learned": "Annulus area subtracts squared radii.",
        "explained": "The ring 33π is smaller than 49π and restores the full disk with 16π."
      },
      {
        "number": 2,
        "title": "Can the given dimensions really be used as radii?",
        "observed": "Diameter and width descriptions can conceal the actual radii.",
        "learned": "Interpretation precedes annulus calculation.",
        "explained": "Substitution and dimensional bounds verify an inverse solution."
      },
      {
        "number": 3,
        "title": "How much of the disk does a sector occupy?",
        "observed": "The 120° sector is one third of a disk.",
        "learned": "Sector area is the central-angle fraction ofπr².",
        "explained": "Doubling radius quadruples area at fixed angle."
      },
      {
        "number": 4,
        "title": "Can an area determine the angle?",
        "observed": "A sector area fraction can determine its angle.",
        "learned": "Reverse sector reasoning uses the same whole-disk relationship.",
        "explained": "An area quantity is not an arc length or a complete purchasing quote."
      },
      {
        "number": 5,
        "title": "What if the sector has a circular hole?",
        "observed": "The annular sector subtracts two sectors of the same angle.",
        "learned": "Area=(θ/360)π(R²−r²).",
        "explained": "Ring thickness squared models the wrong region."
      },
      {
        "number": 6,
        "title": "What lies between a chord and its arc?",
        "observed": "The sector contains both the triangle and the minor segment.",
        "learned": "Minor-segment area is sector area minus central-triangle area.",
        "explained": "The right central triangle removes 32 cm² from 16π cm²."
      },
      {
        "number": 7,
        "title": "How does the major segment differ?",
        "observed": "The same chord creates complementary minor and major segments.",
        "learned": "The major segment includes the triangle with the major sector.",
        "explained": "Complementing the minor segment avoids subtracting the wrong region."
      },
      {
        "number": 8,
        "title": "Why does an overlap contain two segments?",
        "observed": "The common chord divides the overlap into two equal segments.",
        "learned": "Equal-circle symmetry permits twice one segment here.",
        "explained": "The intersection is 25π/2−25, smaller than either 25π disk."
      },
      {
        "number": 9,
        "title": "What changes when the circle radii differ?",
        "observed": "Unequal circles contribute unequal segment areas.",
        "learned": "Overlap is the sum of the appropriate two segment areas.",
        "explained": "The kite check verifies the total triangle subtraction of 12 cm²."
      },
      {
        "number": 10,
        "title": "Can we make a useful and safe circular design?",
        "observed": "Eight annular sectors reconstruct a ring.",
        "learned": "Area models can support design choices with explicit assumptions.",
        "explained": "Each 10π cm² piece is a planar estimate, not a full manufacturing specification."
      },
      {
        "number": 11,
        "title": "Which decomposition deserves our confidence?",
        "observed": "Some correct-looking formulas describe the wrong region.",
        "learned": "A defensible model starts with region and conditions.",
        "explained": "Dimension, decomposition, unit and magnitude checks work together."
      },
      {
        "number": 12,
        "title": "Independent part-circle design commission",
        "observed": "New dimensions reveal individual area-model reasoning.",
        "learned": "Teacher records demonstrated skills after collection.",
        "explained": "Feedback follows the collected decompositions and checks, not group project appearance."
      }
    ]
  }
};
