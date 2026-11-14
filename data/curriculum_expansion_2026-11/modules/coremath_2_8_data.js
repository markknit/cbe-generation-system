'use strict';
module.exports = {
  "schemaVersion": "1.1.0",
  "META": {
    "subject": "Core Mathematics",
    "grade": 10,
    "substrand_id": "2.8",
    "substrand_name": "Vectors I",
    "outputDir": "v2/Core_Mathematics/SS2.8_Vectors_I",
    "filePrefix": "Codex_Core_Mathematics_Vectors_I",
    "titleDoc": "CORE MATHEMATICS GRADE 10: VECTORS I",
    "subtitleDoc": "OpenAI-only evaluation • Sub-Strand 2.8 • 13 lessons • teacher review copy"
  },
  "UNIT": {
    "strand": "2.0 Measurements and Geometry",
    "substrand": "Sub-Strand2.8: Vectors I",
    "sep": "Represent directed change,compare geometric and component models,and verify invariants.",
    "careers": "Illustrative mapping,design and motion modelling;paper routes are not traffic instructions or professional navigation qualifications.",
    "focus": "Magnitude and direction,notation,equivalence,addition,scaling,columns,position,magnitude,midpoints and translations with a declared origin/scale.",
    "phenomenon": "Two campus route arrows have equal lengths but point differently;another team mistakes half a displacement for the location of a collection point.",
    "supportingPhenomena": "Grid arrows,head-to-tail routes,origin changes,translated shapes and a halfway-point audit.",
    "drivingQuestion": "How can a vector model describe a route or design change precisely? KICD: What are vectors? Where are vectors used in real-life situations?",
    "storylineThread": "Quantity → notation → equivalent arrows → addition → components → scaling → position → magnitude → midpoint → translation → route application → audit → independent evidence.",
    "coreCompetencies": "Learning to learn: As the learner uses charts and grids to practise addition of vectors.\nSelf-efficacy: As the learner shares and uses resources from the immediate environment such as plane figures or flip charts to demonstrate equivalent vectors.",
    "values": "Responsibility: As the learner uses resources from the immediate environment such as plane figures, flip charts and relate equivalent vectors.\nUnity: As the learner searches and brainstorms on the meaning of the terms vector and scalar quantities and illustrates giving examples.",
    "pcis": "Education for Sustainable Development - Environmental education as learners practice addition of vectors using charts and grids made from resources in the immediate environment.\nRoad safety: as the learner discusses the meaning of arrows and lines on roads and road signs in relation to movement on the roads to enhance safety.",
    "content": "Vector and scalar quantities.; Vector notation; Representation of vectors; Equivalent vectors; Addition of vectors; Multiplication of vectors by scalar; Column vectors; Position vectors; Magnitude of a vector; Midpoint of a vector; Translation vector",
    "gradeLevel": "10",
    "subject": "Core Mathematics",
    "totalDuration": "13 lessons × 40 minutes = 520 minutes",
    "learningOutcomes": "explain vector and scalar quantities with illustrations\nuse vector notations in different ways\nrepresent vectors geometrically in different situations\nidentify equivalent vectors in different situations\nadd vectors in different situations\nmultiply vectors by scalars\ndetermine column vectors in different situations\ndetermine position vectors in different situations\nwork out magnitude of a vector in different situations\ndetermine the midpoint of a vector in different situations\ndetermine translation vector as a transformation\nappreciate the use of vectors in real-life situations"
  },
  "LESSONS": [
    {
      "number": 1,
      "title": "When is a number without direction insufficient?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand2.8: Vectors I",
      "aresKeywords": "vectors column vectors notation displacement",
      "slo": {
        "purpose": "Distinguish scalar and vector quantities with annotated illustrations.",
        "knowledge": "A vector quantity needs magnitude and direction;distance and displacement describe different things.",
        "skills": "Classify,draw scaled arrows and explain a round trip.",
        "attitudes": "Listen respectfully,share/reuse materials responsibly and revise a model when evidence warrants it.",
        "keyInquiry": "Do opposite arrows of equal length describe the same change?",
        "purposeInStoryline": "The route team identifies what each report actually measures.",
        "safetyNotes": "Paper scenarios only;do not enter roads or move around traffic. Provide ruler,pencil,accessible equal-unit grid and spare paper. Approved optional devices require teacher supervision,no personal-data/account entry;record actual actions honestly."
      },
      "overview": "Use paper reports and arrows rather than movement in a live road environment.\nMaterials: VX1. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Predict whether speed4m/s determines where an object is moving.",
          "teacherMoves": "4 minutes. Ask which information is missing before giving names.",
          "sensemakingStrategy": "Commit a quantity-based prediction.",
          "formativeAssessment": "Learner names direction rather than a larger number."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Classify VX1 and draw the opposite4m arrows;compare the round trip.",
          "teacherMoves": "16 minutes. Give10minutes classification/drawing and6for individual distance/displacement reasons.",
          "sensemakingStrategy": "Compare what each report can establish.",
          "formativeAssessment": "Five scalars,three vectors;round trip distance6m,displacement0."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Explain magnitude,direction and equivalent-vector requirements.",
          "teacherMoves": "10 minutes. Explain that the zero vector has no unique direction;this is different from a compass angle of zero.",
          "sensemakingStrategy": "Connect an arrow model to the quantity it represents.",
          "formativeAssessment": "Each learner explains why equal length is insufficient."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Post questions about naming arrows and recording change.",
          "teacherMoves": "4 minutes. Retain point-versus-arrow questions for notation.",
          "sensemakingStrategy": "Sort questions by information required.",
          "formativeAssessment": "Question distinguishes location from movement."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Build a quantity/units/direction checklist.",
          "teacherMoves": "6 minutes. Collect an individual annotated example and counterexample.",
          "sensemakingStrategy": "Revise the original prediction with evidence.",
          "formativeAssessment": "Exit contrasts speed with velocity."
        }
      ],
      "teacherReflection": "Inspect individual diagrams/components and the named exit evidence. Record the specific sign,reference,scale or interpretation error and a targeted next support;do not infer mastery from a shared chart.",
      "summaryTablePrompt": {
        "observed": "Opposite directions can accompany equal magnitudes.",
        "learned": "Scalars and vectors encode different information.",
        "explained": "A round trip can have positive distance and zero displacement."
      }
    },
    {
      "number": 2,
      "title": "How can the same vector be named three ways?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand2.8: Vectors I",
      "aresKeywords": "vectors column vectors notation displacement",
      "slo": {
        "purpose": "Translate between directed-arrow,bold-letter and column notation.",
        "knowledge": "Column entries represent signed horizontal/vertical changes;point coordinates give locations relative to an origin.",
        "skills": "Plot endpoints,subtract coordinates and label arrow direction.",
        "attitudes": "Listen respectfully,share/reuse materials responsibly and revise a model when evidence warrants it.",
        "keyInquiry": "Why is AB not generally the coordinate pair of B?",
        "purposeInStoryline": "A map needs an unambiguous notation key.",
        "safetyNotes": "Paper scenarios only;do not enter roads or move around traffic. Provide ruler,pencil,accessible equal-unit grid and spare paper. Approved optional devices require teacher supervision,no personal-data/account entry;record actual actions honestly."
      },
      "overview": "The supplied blank equal-unit grid supports four endpoint plots.\nMaterials: VX2. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Predict AB from the listed endpoints without plotting.",
          "teacherMoves": "4 minutes. Ask learners to record both start and finish.",
          "sensemakingStrategy": "Make a checkable component claim.",
          "formativeAssessment": "Working shows endpoint minus startpoint."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Plot VX2 points,draw AB,BA,DE and write each column.",
          "teacherMoves": "16 minutes. Provide grid copies/rulers;allow10minutes plotting and6notation comparison.",
          "sensemakingStrategy": "Compare the geometric arrow with signed changes.",
          "formativeAssessment": "AB=DE=[5;3],BA=[−5;−3]."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Explain arrow-over-AB,bold b and vertical column notation.",
          "teacherMoves": "10 minutes. Define one bold letter consistently and contrast point B with vector AB.",
          "sensemakingStrategy": "Represent one meaning in several forms.",
          "formativeAssessment": "Learner explains why B(3,4) differs from AB."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Ask how arrows in different places can represent one vector.",
          "teacherMoves": "4 minutes. Keep startpoint questions for equivalence.",
          "sensemakingStrategy": "Identify which properties notation preserves.",
          "formativeAssessment": "Question names both components or direction/length."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Add a notation key to the map.",
          "teacherMoves": "6 minutes. Collect an independent reverse-vector calculation.",
          "sensemakingStrategy": "Use a representation to check another representation.",
          "formativeAssessment": "Exit reverses both component signs,not just one."
        }
      ],
      "teacherReflection": "Inspect individual diagrams/components and the named exit evidence. Record the specific sign,reference,scale or interpretation error and a targeted next support;do not infer mastery from a shared chart.",
      "summaryTablePrompt": {
        "observed": "Different notation can describe the same directed change.",
        "learned": "A column records endpoint differences in a fixed axis system.",
        "explained": "A point and a displacement answer different questions."
      }
    },
    {
      "number": 3,
      "title": "Can an arrow move without changing its vector?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand2.8: Vectors I",
      "aresKeywords": "vectors column vectors notation displacement",
      "slo": {
        "purpose": "Represent and identify equivalent vectors using geometry and components.",
        "knowledge": "Equivalent free vectors have equal magnitude and direction,even with different tails.",
        "skills": "Plot,copy parallel arrows and compare signed differences.",
        "attitudes": "Listen respectfully,share/reuse materials responsibly and revise a model when evidence warrants it.",
        "keyInquiry": "What evidence distinguishes equivalence from equal length?",
        "purposeInStoryline": "Several signs on the map appear alike but only two encode the same change.",
        "safetyNotes": "Paper scenarios only;do not enter roads or move around traffic. Provide ruler,pencil,accessible equal-unit grid and spare paper. Approved optional devices require teacher supervision,no personal-data/account entry;record actual actions honestly."
      },
      "overview": "Three arrows isolate location,direction and magnitude.\nMaterials: VX3. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Predict which VX3 arrows are equivalent from endpoints.",
          "teacherMoves": "4 minutes. Record a reason before pair discussion.",
          "sensemakingStrategy": "Separate a claim from a visual impression.",
          "formativeAssessment": "Prediction refers to signed change."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Plot all arrows and compare AB,CD,EF and BA.",
          "teacherMoves": "16 minutes. Require equal axis scales and visible arrowheads;use a ruler to copy a parallel arrow.",
          "sensemakingStrategy": "Compare component and geometric evidence.",
          "formativeAssessment": "AB=CD=[4;2],EF=[4;−2],BA=[−4;−2]."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Explain why shifting a free arrow preserves its vector.",
          "teacherMoves": "10 minutes. Contrast a specified position vector with a free-vector representative.",
          "sensemakingStrategy": "State what changes and what is invariant.",
          "formativeAssessment": "Learner rejects same-length opposite/reflected arrows as equivalent."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Ask how two displacements can combine.",
          "teacherMoves": "4 minutes. Retain tail/head questions for addition.",
          "sensemakingStrategy": "Connect unanswered questions to the route problem.",
          "formativeAssessment": "Question identifies the final endpoint."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Revise the map's equivalence rule.",
          "teacherMoves": "6 minutes. Collect an individual drawing at a different tail with the same components.",
          "sensemakingStrategy": "Test a rule with a counterexample.",
          "formativeAssessment": "Exit gives both magnitude and direction conditions."
        }
      ],
      "teacherReflection": "Inspect individual diagrams/components and the named exit evidence. Record the specific sign,reference,scale or interpretation error and a targeted next support;do not infer mastery from a shared chart.",
      "summaryTablePrompt": {
        "observed": "Equal vector changes can start at different points.",
        "learned": "Free-vector equivalence preserves direction and magnitude.",
        "explained": "Equal arrow lengths alone do not establish equivalence."
      }
    },
    {
      "number": 4,
      "title": "Where does a head-to-tail route end?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand2.8: Vectors I",
      "aresKeywords": "vectors column vectors addition",
      "slo": {
        "purpose": "Add vectors geometrically and verify the resultant by components.",
        "knowledge": "Head-to-tail addition connects the initial tail to the final head;the parallelogram diagonal gives the same resultant.",
        "skills": "Copy directed arrows and compare two addition orders.",
        "attitudes": "Listen respectfully,share/reuse materials responsibly and revise a model when evidence warrants it.",
        "keyInquiry": "Why does adding two arrow lengths fail for a turning route?",
        "purposeInStoryline": "The team combines two map instructions.",
        "safetyNotes": "Paper scenarios only;do not enter roads or move around traffic. Provide ruler,pencil,accessible equal-unit grid and spare paper. Approved optional devices require teacher supervision,no personal-data/account entry;record actual actions honestly."
      },
      "overview": "VX4 supports head-to-tail and parallelogram constructions on equal-unit grids.\nMaterials: VX4. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Predict the final point after a then b.",
          "teacherMoves": "4 minutes. Require direction as well as component values.",
          "sensemakingStrategy": "Commit an endpoint prediction.",
          "formativeAssessment": "Learner distinguishes resultant from path length."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Draw both orders and a parallelogram for VX4.",
          "teacherMoves": "16 minutes. Allocate6minutes per order and4for the parallelogram;check arrows are copied without rotation.",
          "sensemakingStrategy": "Use three constructions to test one result.",
          "formativeAssessment": "Both orders end(2,3),resultant[2;3]."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Explain why moving an equivalent copy is legitimate.",
          "teacherMoves": "10 minutes. Trace the resultant from the initial tail;reserve numeric lengths for Lesson8.",
          "sensemakingStrategy": "Connect construction to component addition.",
          "formativeAssessment": "Learner points to the correct diagonal and its arrowhead."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Ask how signed components can shorten a drawing calculation.",
          "teacherMoves": "4 minutes. Record signed-addition questions for Lesson5.",
          "sensemakingStrategy": "Link geometric evidence to an algebraic method.",
          "formativeAssessment": "Question identifies horizontal and vertical totals separately."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Add head-to-tail and parallelogram methods to the map key.",
          "teacherMoves": "6 minutes. Collect one individual resultant drawing with a component check.",
          "sensemakingStrategy": "Resolve a disagreement using endpoints.",
          "formativeAssessment": "Exit explains why magnitudes alone do not determine the sum."
        }
      ],
      "teacherReflection": "Inspect individual diagrams/components and the named exit evidence. Record the specific sign,reference,scale or interpretation error and a targeted next support;do not infer mastery from a shared chart.",
      "summaryTablePrompt": {
        "observed": "Two addition orders reach the same endpoint.",
        "learned": "The resultant is the direct arrow from initial tail to final head.",
        "explained": "Vector addition respects direction,not just arrow lengths."
      }
    },
    {
      "number": 5,
      "title": "Can signed columns check a route drawing?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand2.8: Vectors I",
      "aresKeywords": "vectors column vectors addition",
      "slo": {
        "purpose": "Add signed column vectors and check a multi-stage route.",
        "knowledge": "Corresponding components add independently;different groupings produce the same total.",
        "skills": "Compute,sketch and check a closing displacement.",
        "attitudes": "Listen respectfully,share/reuse materials responsibly and revise a model when evidence warrants it.",
        "keyInquiry": "Which return vector closes the route?",
        "purposeInStoryline": "A three-stage route needs an independent arithmetic audit.",
        "safetyNotes": "Paper scenarios only;do not enter roads or move around traffic. Provide ruler,pencil,accessible equal-unit grid and spare paper. Approved optional devices require teacher supervision,no personal-data/account entry;record actual actions honestly."
      },
      "overview": "The same route is solved using grouped columns and arrows.\nMaterials: VX5. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Predict whether the route returns to its starting point.",
          "teacherMoves": "4 minutes. Ask for a sign-based reason before drawing.",
          "sensemakingStrategy": "Commit a closure claim.",
          "formativeAssessment": "Prediction states total horizontal and vertical change."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Complete VX5 sums,groupings,sketch and closing vector.",
          "teacherMoves": "16 minutes. Allow8minutes arithmetic and8drawing/checking;do not require radical path lengths here.",
          "sensemakingStrategy": "Compare endpoint and component evidence.",
          "formativeAssessment": "u+v=[2;2],total[1;0],return[−1;0]."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Explain why regrouping preserves each component sum.",
          "teacherMoves": "10 minutes. Show the return vector makes both total components zero.",
          "sensemakingStrategy": "Connect associativity with a geometric route.",
          "formativeAssessment": "Learner distinguishes resultant1m east from distance travelled."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Ask how reversing or repeating a displacement is represented.",
          "teacherMoves": "4 minutes. Keep negative/zero scaling questions for Lesson6.",
          "sensemakingStrategy": "Extend the route model to repeated instructions.",
          "formativeAssessment": "Question distinguishes a sign change from an added stage."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Add a closure test to the route checklist.",
          "teacherMoves": "6 minutes. Collect an individual component sum and check.",
          "sensemakingStrategy": "Use an independent method to find a sign error.",
          "formativeAssessment": "Exit explains how zero total components test closure."
        }
      ],
      "teacherReflection": "Inspect individual diagrams/components and the named exit evidence. Record the specific sign,reference,scale or interpretation error and a targeted next support;do not infer mastery from a shared chart.",
      "summaryTablePrompt": {
        "observed": "Signed additions agree with the final plotted endpoint.",
        "learned": "Component sums combine multi-stage displacements.",
        "explained": "A return vector is the negative of the resultant."
      }
    },
    {
      "number": 6,
      "title": "What do positive,negative and zero scalars do?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand2.8: Vectors I",
      "aresKeywords": "vectors column vectors scalar multiplication",
      "slo": {
        "purpose": "Interpret and compute scalar multiples,including negative,fractional and zero cases.",
        "knowledge": "Magnitude scales by the absolute scalar;negative scalars reverse direction and zero has no unique direction.",
        "skills": "Scale components,draw arrows and test a distributive relation.",
        "attitudes": "Listen respectfully,share/reuse materials responsibly and revise a model when evidence warrants it.",
        "keyInquiry": "Does multiplying by−2 give a negative length?",
        "purposeInStoryline": "Route instructions are repeated,reversed and halved.",
        "safetyNotes": "Paper scenarios only;do not enter roads or move around traffic. Provide ruler,pencil,accessible equal-unit grid and spare paper. Approved optional devices require teacher supervision,no personal-data/account entry;record actual actions honestly."
      },
      "overview": "Five multiples and a distributive check expose sign and direction distinctions.\nMaterials: VX6. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Predict the length/direction of−2a and0a.",
          "teacherMoves": "4 minutes. Ask learners to separate component signs from magnitude.",
          "sensemakingStrategy": "State a conditional prediction.",
          "formativeAssessment": "Zero direction is recorded as not defined."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Draw/compute VX6 multiples and both doubled sums.",
          "teacherMoves": "16 minutes. Supply half-unit marking guidance;allow10minutes multiples and6distributive check.",
          "sensemakingStrategy": "Compare a scalar rule with actual endpoints.",
          "formativeAssessment": "3a=[6;−3],−2a=[−4;2],a/2=[1;−0.5],both doubled sums[2;4]."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Explain absolute-factor length scaling and opposite vectors.",
          "teacherMoves": "10 minutes. Define u−v as u+(−v) rather than subtracting magnitudes.",
          "sensemakingStrategy": "Generalise from signed component evidence.",
          "formativeAssessment": "Learner predicts direction correctly for a negative scalar."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Ask how a displacement is related to positions measured from an origin.",
          "teacherMoves": "4 minutes. Retain subtraction/reference questions for Lesson7.",
          "sensemakingStrategy": "Link reverse vectors to endpoint differences.",
          "formativeAssessment": "Question names a specified origin."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Add scaling conditions to the map key.",
          "teacherMoves": "6 minutes. Collect an individual negative-scalar drawing and column.",
          "sensemakingStrategy": "Check algebraic signs against direction.",
          "formativeAssessment": "Exit avoids assigning a compass direction to the zero vector."
        }
      ],
      "teacherReflection": "Inspect individual diagrams/components and the named exit evidence. Record the specific sign,reference,scale or interpretation error and a targeted next support;do not infer mastery from a shared chart.",
      "summaryTablePrompt": {
        "observed": "Negative scaling reverses an arrow without creating a negative length.",
        "learned": "Scalar multiplication changes components consistently.",
        "explained": "The zero vector has magnitude zero and no unique direction."
      }
    },
    {
      "number": 7,
      "title": "Which vectors change when the origin changes?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand2.8: Vectors I",
      "aresKeywords": "vectors column vectors midpoint position vectors",
      "slo": {
        "purpose": "Distinguish position vectors from displacements using two reference points.",
        "knowledge": "PQ=OQ−OP;translation of the origin changes position coordinates but not displacement PQ.",
        "skills": "Compute endpoint differences and annotate a triangle relation.",
        "attitudes": "Listen respectfully,share/reuse materials responsibly and revise a model when evidence warrants it.",
        "keyInquiry": "Does moving the reference point move the object?",
        "purposeInStoryline": "Two teams use different map origins but should agree on the route.",
        "safetyNotes": "Paper scenarios only;do not enter roads or move around traffic. Provide ruler,pencil,accessible equal-unit grid and spare paper. Approved optional devices require teacher supervision,no personal-data/account entry;record actual actions honestly."
      },
      "overview": "VX7 compares the same points relative to O and R.\nMaterials: VX7. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Predict whether PQ changes when R replaces O.",
          "teacherMoves": "4 minutes. Ask what physically moved and what was merely relabelled.",
          "sensemakingStrategy": "Commit an invariant claim.",
          "formativeAssessment": "Prediction distinguishes reference from motion."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Compute/plot all VX7 vectors relative to both origins.",
          "teacherMoves": "16 minutes. Allow8minutes per origin;require endpoint-minus-start working.",
          "sensemakingStrategy": "Compare coordinate descriptions of the same segment.",
          "formativeAssessment": "PQ=[6;−4]from both[4;−1]−[−2;3]and[3;−2]−[−3;2]."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Explain the triangle relation OP+PQ=OQ.",
          "teacherMoves": "10 minutes. Use adding the opposite vector to justify subtraction.",
          "sensemakingStrategy": "Connect algebra to an anchored geometric path.",
          "formativeAssessment": "Learner labels which vectors depend on the chosen origin."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Ask how to express the length of a signed column.",
          "teacherMoves": "4 minutes. Keep perpendicular-component questions for Lesson8.",
          "sensemakingStrategy": "Identify information not given by a position name alone.",
          "formativeAssessment": "Question distinguishes components from magnitude."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Add origin labels and endpoint checks to the map.",
          "teacherMoves": "6 minutes. Collect one independent reference-change explanation.",
          "sensemakingStrategy": "Test an invariant with a second representation.",
          "formativeAssessment": "Exit states that changing coordinates need not mean physical movement."
        }
      ],
      "teacherReflection": "Inspect individual diagrams/components and the named exit evidence. Record the specific sign,reference,scale or interpretation error and a targeted next support;do not infer mastery from a shared chart.",
      "summaryTablePrompt": {
        "observed": "Position columns change with the chosen origin.",
        "learned": "Displacement is endpoint position minus startpoint position.",
        "explained": "Both reference systems give the same P-to-Q change."
      }
    },
    {
      "number": 8,
      "title": "How can signed components give a nonnegative magnitude?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand2.8: Vectors I",
      "aresKeywords": "vectors column vectors magnitude",
      "slo": {
        "purpose": "Derive and apply the magnitude formula on orthogonal equal-unit axes.",
        "knowledge": "Pythagoras gives sqrt(p²+q²);path distance and displacement magnitude differ.",
        "skills": "Construct a right triangle,calculate and interpret units.",
        "attitudes": "Listen respectfully,share/reuse materials responsibly and revise a model when evidence warrants it.",
        "keyInquiry": "Why does changing both component signs preserve length?",
        "purposeInStoryline": "The team needs a direct-distance check for its route.",
        "safetyNotes": "Paper scenarios only;do not enter roads or move around traffic. Provide ruler,pencil,accessible equal-unit grid and spare paper. Approved optional devices require teacher supervision,no personal-data/account entry;record actual actions honestly."
      },
      "overview": "VX8 connects geometric lengths to a computable magnitude.\nMaterials: VX8. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Predict whether−v can have magnitude−5.",
          "teacherMoves": "4 minutes. Record a length interpretation before calculation.",
          "sensemakingStrategy": "Commit a sign/magnitude claim.",
          "formativeAssessment": "Prediction recognises nonnegative length."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Draw right triangles and compute all VX8 magnitudes and route distances.",
          "teacherMoves": "16 minutes. Allow10minutes magnitudes and6distance/displacement comparison;calculators check square roots after the setup.",
          "sensemakingStrategy": "Compare square sums with geometric lengths.",
          "formativeAssessment": "Magnitudes5,5,10,13,0;route distance7m versus resultant5m."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Derive the formula and explain its equal-unit perpendicular-axis assumptions.",
          "teacherMoves": "10 minutes. Contrast a negative component with a negative length;retain exact radicals where needed.",
          "sensemakingStrategy": "State the conditions of a mathematical model.",
          "formativeAssessment": "Learner includes squared components and correct units."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Ask where halfway along a directed segment is located.",
          "teacherMoves": "4 minutes. Keep location-versus-half-change questions for Lesson9.",
          "sensemakingStrategy": "Connect length to a new position question.",
          "formativeAssessment": "Question identifies both endpoints."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Add a magnitude and unit check to the route sheet.",
          "teacherMoves": "6 minutes. Collect an individual formula explanation and opposite-vector comparison.",
          "sensemakingStrategy": "Use geometry to check arithmetic.",
          "formativeAssessment": "Exit distinguishes distance from displacement magnitude."
        }
      ],
      "teacherReflection": "Inspect individual diagrams/components and the named exit evidence. Record the specific sign,reference,scale or interpretation error and a targeted next support;do not infer mastery from a shared chart.",
      "summaryTablePrompt": {
        "observed": "Opposite vectors have the same magnitude.",
        "learned": "Perpendicular components determine length through Pythagoras.",
        "explained": "A turning route can be longer than its net displacement."
      }
    },
    {
      "number": 9,
      "title": "Is half a displacement the midpoint's position?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand2.8: Vectors I",
      "aresKeywords": "vectors column vectors midpoint position vectors",
      "slo": {
        "purpose": "Locate segment midpoints using endpoint averages and half-displacement.",
        "knowledge": "OM=(OA+OB)/2=OA+(AB/2);halfAB alone is a displacement from A.",
        "skills": "Average coordinates,plot fractional values and verify equal halves.",
        "attitudes": "Listen respectfully,share/reuse materials responsibly and revise a model when evidence warrants it.",
        "keyInquiry": "What startpoint is missing from the claim midpoint=AB/2?",
        "purposeInStoryline": "A collection-point proposal confuses change with location.",
        "safetyNotes": "Paper scenarios only;do not enter roads or move around traffic. Provide ruler,pencil,accessible equal-unit grid and spare paper. Approved optional devices require teacher supervision,no personal-data/account entry;record actual actions honestly."
      },
      "overview": "Two segments,including fractional coordinates,expose the missing startpoint.\nMaterials: VX9. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Predict the midpoint of the first VX9 segment.",
          "teacherMoves": "4 minutes. Ask learners to label whether their result is a point or a vector.",
          "sensemakingStrategy": "Commit a location claim.",
          "formativeAssessment": "Initial claim retains the specified origin."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Compute both midpoints by two methods and verify AM=MB or CM=MD.",
          "teacherMoves": "16 minutes. Allow8minutes per segment;provide half-unit grid marks.",
          "sensemakingStrategy": "Compare average-position and half-change constructions.",
          "formativeAssessment": "M(1,3),second midpoint(−0.5,1.5),equal half-displacements."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Explain why the startpoint must be added to halfAB.",
          "teacherMoves": "10 minutes. Clarify source wording:midpoint here means the midpoint of a displayed directed segment,not a location attached to a free vector alone.",
          "sensemakingStrategy": "Distinguish a quantity from its reference-dependent interpretation.",
          "formativeAssessment": "Learner contrasts halfAB=[3;2]with OM=[1;3]."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Ask how a whole shape moves by a specified displacement.",
          "teacherMoves": "4 minutes. Retain corresponding-vertex questions for translation.",
          "sensemakingStrategy": "Extend a point relation to a shape.",
          "formativeAssessment": "Question requires the same shift for every vertex."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Correct the collection-point proposal with both methods.",
          "teacherMoves": "6 minutes. Collect an independent midpoint/location explanation.",
          "sensemakingStrategy": "Use two calculations to test a positional claim.",
          "formativeAssessment": "Exit includes the startpoint in A+AB/2."
        }
      ],
      "teacherReflection": "Inspect individual diagrams/components and the named exit evidence. Record the specific sign,reference,scale or interpretation error and a targeted next support;do not infer mastery from a shared chart.",
      "summaryTablePrompt": {
        "observed": "Half a segment's displacement need not be its midpoint position.",
        "learned": "Endpoint averages and startpoint-plus-half-change agree.",
        "explained": "A midpoint location requires a specified representative segment/origin."
      }
    },
    {
      "number": 10,
      "title": "What makes a whole-shape translation consistent?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand2.8: Vectors I",
      "aresKeywords": "vectors column vectors translation",
      "slo": {
        "purpose": "Translate a triangle and recover a consistent transformation vector.",
        "knowledge": "Every corresponding point receives the same displacement;corresponding side vectors remain equal.",
        "skills": "Plot image vertices,calculate differences and audit a proposed image.",
        "attitudes": "Listen respectfully,share/reuse materials responsibly and revise a model when evidence warrants it.",
        "keyInquiry": "Is checking one vertex enough to verify a triangle image?",
        "purposeInStoryline": "A copied map symbol has one incorrectly moved vertex.",
        "safetyNotes": "Paper scenarios only;do not enter roads or move around traffic. Provide ruler,pencil,accessible equal-unit grid and spare paper. Approved optional devices require teacher supervision,no personal-data/account entry;record actual actions honestly."
      },
      "overview": "VX10 uses three vertices and a separate incorrect point claim.\nMaterials: VX10. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Predict image A' under[3;−2].",
          "teacherMoves": "4 minutes. Ask for horizontal and vertical change separately.",
          "sensemakingStrategy": "Commit a coordinate prediction.",
          "formativeAssessment": "Prediction uses+3and−2in the correct positions."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Plot the original/image,check all matched shifts and audit D'.",
          "teacherMoves": "16 minutes. Allow10minutes plotting and6difference checks.",
          "sensemakingStrategy": "Compare vertex and side invariants.",
          "formativeAssessment": "Image(2,−1),(5,−1),(3,1);all shifts[3;−2];D'claim fails."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Explain why a common translation preserves corresponding side vectors.",
          "teacherMoves": "10 minutes. Compare AB and A'B'and distinguish this operation from rotation/enlargement.",
          "sensemakingStrategy": "Justify a transformation using invariants.",
          "formativeAssessment": "Learner checks every vertex rather than a single attractive sketch."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Ask how translation and route vectors help a real planning decision.",
          "teacherMoves": "4 minutes. Keep scale/road-sign limitations for the paper application.",
          "sensemakingStrategy": "Link a model to its intended use.",
          "formativeAssessment": "Question identifies a required scale or context."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Build an image-verification checklist.",
          "teacherMoves": "6 minutes. Collect an individual matched-point recovery of t.",
          "sensemakingStrategy": "Check a model from its outputs.",
          "formativeAssessment": "Exit recovers the same vector from two different pairs."
        }
      ],
      "teacherReflection": "Inspect individual diagrams/components and the named exit evidence. Record the specific sign,reference,scale or interpretation error and a targeted next support;do not infer mastery from a shared chart.",
      "summaryTablePrompt": {
        "observed": "Every vertex shifts by one common vector.",
        "learned": "Translation preserves corresponding displacement vectors.",
        "explained": "A complete image needs consistent vertex-by-vertex evidence."
      }
    },
    {
      "number": 11,
      "title": "What can a scaled campus route model establish?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand2.8: Vectors I",
      "aresKeywords": "vectors column vectors notation displacement",
      "slo": {
        "purpose": "Apply vectors,magnitude and midpoint reasoning to a scaled paper route.",
        "knowledge": "Grid components must be converted with the declared scale;road arrows alone do not supply quantitative magnitude.",
        "skills": "Calculate,convert units,locate a midpoint and explain a model's limits.",
        "attitudes": "Listen respectfully,share/reuse materials responsibly and revise a model when evidence warrants it.",
        "keyInquiry": "Why does a traffic arrow not determine a safe measured journey?",
        "purposeInStoryline": "The team evaluates a collection-point and route proposal.",
        "safetyNotes": "Paper scenarios only;do not enter roads or move around traffic. Provide ruler,pencil,accessible equal-unit grid and spare paper. Approved optional devices require teacher supervision,no personal-data/account entry;record actual actions honestly."
      },
      "overview": "A fictional campus map combines earlier skills with road-safety interpretation.\nMaterials: VX11. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Predict distance versus resultant length for the campus route.",
          "teacherMoves": "4 minutes. Ask which numbers are grid units and which are metres.",
          "sensemakingStrategy": "Commit a scale-aware prediction.",
          "formativeAssessment": "Initial working states1unit=10m."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Solve VX11 displacements,total distance,resultant and collection point.",
          "teacherMoves": "16 minutes. Allow8minutes sums/distance and8magnitude/midpoint;keep the whole activity on paper.",
          "sensemakingStrategy": "Cross-check component,geometric and unit evidence.",
          "formativeAssessment": "Distance90m;resultant[10;40]m,length10sqrt17m;midpoint grid(0.5,2)."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Explain a vector benefit and the limits of direction-only signs.",
          "teacherMoves": "10 minutes. Reject any suggestion that a shortest mathematical route overrides physical obstacles/traffic rules.",
          "sensemakingStrategy": "Bound the model to its assumptions.",
          "formativeAssessment": "Each learner cites one calculated result and one missing real-world condition."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Add unresolved accessibility,obstacle or scale questions.",
          "teacherMoves": "4 minutes. Separate mathematical answers from unprovided map facts.",
          "sensemakingStrategy": "Identify information needed before an actual decision.",
          "formativeAssessment": "Question does not invent safe access from a paper arrow."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Revise the collection-point proposal with units.",
          "teacherMoves": "6 minutes. Collect one individual practical-use explanation;teacher checks actual pupil route changes.",
          "sensemakingStrategy": "Use evidence to support a limited conclusion.",
          "formativeAssessment": "Exit distinguishes a direction symbol from a measured displacement."
        }
      ],
      "teacherReflection": "Inspect individual diagrams/components and the named exit evidence. Record the specific sign,reference,scale or interpretation error and a targeted next support;do not infer mastery from a shared chart.",
      "summaryTablePrompt": {
        "observed": "Grid units and physical distances require an explicit conversion.",
        "learned": "Vectors support checked route and midpoint calculations.",
        "explained": "A useful model does not establish real road access or safety by itself."
      }
    },
    {
      "number": 12,
      "title": "Can another team reproduce our vector audit?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand2.8: Vectors I",
      "aresKeywords": "vectors column vectors notation displacement",
      "slo": {
        "purpose": "Audit vector claims and communicate a reproducible addition/translation model.",
        "knowledge": "Equivalence,magnitude,midpoint and translation require distinct checks.",
        "skills": "Diagnose,repair,plot and explain a peer-checkable model.",
        "attitudes": "Listen respectfully,share/reuse materials responsibly and revise a model when evidence warrants it.",
        "keyInquiry": "Which check catches each kind of vector error?",
        "purposeInStoryline": "The team tests its full map-method sheet before independent evidence.",
        "safetyNotes": "Paper scenarios only;do not enter roads or move around traffic. Provide ruler,pencil,accessible equal-unit grid and spare paper. Approved optional devices require teacher supervision,no personal-data/account entry;record actual actions honestly."
      },
      "overview": "Four short audits precede one small shared chart;an approved digital plot is optional and recorded honestly.\nMaterials: VX12. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Choose a VX12 claim and predict a revealing check.",
          "teacherMoves": "4 minutes. Collect an individual claim before group discussion.",
          "sensemakingStrategy": "Name a test rather than guess agreement.",
          "formativeAssessment": "Prediction selects signed components,position or magnitude evidence."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Audit all four claims and produce one small paired chart.",
          "teacherMoves": "16 minutes. Use8minutes audits and8charting;prepare approved device/tool beforehand if available,otherwise use reused squared paper.",
          "sensemakingStrategy": "Preserve original claims beside corrections.",
          "formativeAssessment": "Rejects A,B,Dwith correct reasons;confirms common translation C."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Explain one correction individually and compare the chart with its components.",
          "teacherMoves": "10 minutes. Record actual tool/input/output only if observed;paper charts do not imply digital action.",
          "sensemakingStrategy": "Give evidence-based respectful critique.",
          "formativeAssessment": "Each learner supplies a checkable explanation;teacher notes observed/not-observed device work."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Review the question board and retain genuine model limitations.",
          "teacherMoves": "4 minutes. Keep final VX13 and prompts unreleased;do not practise their numerical answers.",
          "sensemakingStrategy": "Distinguish established methods from missing context.",
          "formativeAssessment": "A learner names a specific useful vector operation and limit."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Complete and close the shared method sheet.",
          "teacherMoves": "6 minutes. Collect an individual diagnostic and plan procedural/access support only for the final.",
          "sensemakingStrategy": "Consolidate a method without sharing final answers.",
          "formativeAssessment": "Exit chooses the correct check for midpoint versus magnitude."
        }
      ],
      "teacherReflection": "Inspect individual diagrams/components and the named exit evidence. Record the specific sign,reference,scale or interpretation error and a targeted next support;do not infer mastery from a shared chart.",
      "summaryTablePrompt": {
        "observed": "Different vector claims fail different checks.",
        "learned": "A reproducible model labels origin,scale,arrowheads and operations.",
        "explained": "Independent reasoning is needed even when a shared chart is correct."
      }
    },
    {
      "number": 13,
      "title": "Independent vector model audit",
      "duration": "40 minutes",
      "substrand": "Sub-Strand2.8: Vectors I",
      "aresKeywords": "vectors column vectors notation displacement",
      "slo": {
        "purpose": "Demonstrate vector representations,operations,location and transformation reasoning independently.",
        "knowledge": "The same origin,scale and operation conditions apply to fresh coordinates.",
        "skills": "Represent,compute,plot,verify and explain a practical limit.",
        "attitudes": "Listen respectfully,share/reuse materials responsibly and revise a model when evidence warrants it.",
        "keyInquiry": "Can I justify a complete vector model without a shared sheet?",
        "purposeInStoryline": "A fresh map dataset tests individual reasoning.",
        "safetyNotes": "Paper scenarios only;do not enter roads or move around traffic. Provide ruler,pencil,accessible equal-unit grid and spare paper. Approved optional devices require teacher supervision,no personal-data/account entry;record actual actions honestly."
      },
      "overview": "Independent assessment uses only VX13,a blank grid and final prompts.\nMaterials: VX13. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 12 min, Explain 16 min, Driving Question Board (DQB) Creation 4 min, Model Building 4 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Read procedure and the isolated VX13 dataset.",
          "teacherMoves": "4 minutes. Allow4minutes for access/procedure,without working an example.",
          "sensemakingStrategy": "Individual work only;no comparison,hints or answer discussion before collection.",
          "formativeAssessment": "Teaching cards and keys remain unavailable."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Complete sections1–2 independently.",
          "teacherMoves": "12 minutes. Allow12minutes;clarify notation/procedure only,not operations or answers.",
          "sensemakingStrategy": "Individual work only;no comparison,hints or answer discussion before collection.",
          "formativeAssessment": "Original representations,component work and vector drawing are visible."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Complete section3 midpoint and translation tasks independently.",
          "teacherMoves": "16 minutes. Allow16minutes;provide spare blank grids without mathematical guidance.",
          "sensemakingStrategy": "Individual work only;no comparison,hints or answer discussion before collection.",
          "formativeAssessment": "Endpoint/midpoint reasoning and matched-vertex checks are collected."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Write section4's private use/limit explanation.",
          "teacherMoves": "4 minutes. Allow4minutes;no shared question-board discussion before collection.",
          "sensemakingStrategy": "Individual work only;no comparison,hints or answer discussion before collection.",
          "formativeAssessment": "A concrete claim is linked to a checked result."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Check units,labels and working;submit every sheet.",
          "teacherMoves": "4 minutes. Allow4minutes and collect before feedback.",
          "sensemakingStrategy": "Individual work only;no comparison,hints or answer discussion before collection.",
          "formativeAssessment": "Teacher retains individual evidence for criterion feedback."
        }
      ],
      "teacherReflection": "Inspect individual diagrams/components and the named exit evidence. Record the specific sign,reference,scale or interpretation error and a targeted next support;do not infer mastery from a shared chart.",
      "summaryTablePrompt": {
        "observed": "Fresh coordinates reveal individual model and operation choices.",
        "learned": "Teacher records demonstrated skills from collected work.",
        "explained": "Feedback separates representation,operation,location and context errors."
      }
    }
  ],
  "FINAL_EXPLANATION": {
    "subjectLabel": "VECTORS I",
    "instructions": "Lesson13,40minutes:4procedure,12sections1–2,16section3,4section4,4checking/collection. Work independently using VX13 and blank squared paper only. [p;q] means a vertical column with p above q. Label origin,equal scale,units and arrowheads. Calculator may check square roots after a shown setup. No teaching cards,worked examples,hints or peer discussion before collection.",
    "sections": [
      {
        "title": "1. Quantity,notation and equivalent arrows",
        "prompt": "Classify mass5kg and displacement4m west as scalar/vector with a reason. Plot and draw directed AB,CD and BA from VX13. Write AB using arrow notation,a defined bold letter and a vertical column. Decide whether AB and CD are equivalent and explain. Write OB and explain why it differs from AB.",
        "exemplar": "Mass scalar:only magnitude/unit;displacement vector:specified magnitude and direction. AB=CD=[4;3]m,equivalent equal changes;BA=[−4;−3]m reverses direction. A defined bold a and arrow-over-AB can name the same vector. OB=[3;5]m is position relative to O,whereas AB starts at A(−1,2). Drawings show listed endpoints,equal axes and arrowheads."
      },
      {
        "title": "2. Operations and magnitude",
        "prompt": "Using VX13,find u+v,−2u and u−v as columns. Show u+v by a head-to-tail drawing from O and compare the endpoint with the component result. Calculate |u−v| with a reasoned formula. Explain the direction and magnitude effect of the negative scalar−2.",
        "exemplar": "u+v=[1;2],−2u=[−4;2],u−v=[3;−4]. Head-to-tail O→(2,−1)→(1,2),resultant O→(1,2). Magnitude sqrt(3²+(−4)²)=5m. Negative scalar reverses direction and doubles magnitude,not a negative length."
      },
      {
        "title": "3. Midpoint and translation",
        "prompt": "Find midpoint M of AB by endpoint averages and by A+(1/2)AB;verify AM=MB and distinguish halfAB from OM. Translate triangle PQR by t,plot all three image vertices,and recover t from each matched pair. Compare PQ with P'Q' as a check.",
        "exemplar": "M(1,3.5);A+[2;1.5]=(1,3.5),AM=MB=[2;1.5]m. HalfAB is change from A;OM=[1;3.5]m is position. P'(1,−1),Q'(3,−1),R'(2,1);all matched differences[3;−1]m. PQ=P'Q'=[2;0]m;diagram preserves arrow direction,scale and orientation."
      },
      {
        "title": "4. Use and limits",
        "prompt": "Explain one concrete benefit of vector reasoning using a checked result above. Explain why a direction arrow on a road sign alone cannot specify a measured displacement or establish that a route is safe. Name one additional real-route fact needed before acting on a map model.",
        "exemplar": "A common translation vector consistently moves all vertices,or a head-to-tail/component check verifies a net movement;accept another specific supported benefit. A sign may convey traffic direction without a quantitative magnitude/scale;obstacles,permissions,crossings/accessibility or current traffic conditions are missing. Paper arithmetic does not justify entering a road or establish practical navigation competence or lasting appreciation."
      }
    ],
    "rubric": [
      {
        "criterion": "Represent and distinguish vector quantities",
        "excellent": "All classifications,notations,arrows,equivalence and position-versus-displacement explanations are correct and clearly linked to origin/scale.",
        "proficient": "Correctly classifies,represents and compares the vectors with valid arrow/column notation and the OB/AB distinction.",
        "developing": "Some correct representations but a direction,notation,equivalence or reference distinction needs correction.",
        "belowExpectations": "Needs guided support to connect magnitude,direction,endpoints and column entries."
      },
      {
        "criterion": "Compute and justify vector operations",
        "excellent": "All columns,head-to-tail construction,magnitude setup/result and negative-scalar explanation agree and independently check one another.",
        "proficient": "Correctly adds,scales,subtracts and finds magnitude with an appropriate drawing and sign/direction explanation.",
        "developing": "Some operations are correct but a sign,construction,magnitude formula or negative-scalar interpretation is incomplete.",
        "belowExpectations": "Needs guided component or geometric support to carry out and interpret the operations."
      },
      {
        "criterion": "Locate and verify midpoint and translated images",
        "excellent": "Both midpoint methods,equal halves,reference distinction,all image vertices and recovered shifts/side checks are correct and well justified.",
        "proficient": "Correctly locates the midpoint,distinguishes its position from half-displacement and verifies all translated vertices with a valid side check.",
        "developing": "A valid method is present but a midpoint location,reference,vertex or transformation check needs correction.",
        "belowExpectations": "Needs guided support to connect endpoint positions,half-change or a common vertex shift."
      },
      {
        "criterion": "Explain a practical use and model limit",
        "excellent": "Gives a specific benefit supported by a checked result and clearly distinguishes direction-only signs,quantitative scale and relevant real-route safety/access facts.",
        "proficient": "Explains a supported benefit and a valid limitation/additional fact before using a route model.",
        "developing": "Gives a plausible use but its supporting result or the missing route information is vague or incomplete.",
        "belowExpectations": "Needs prompts to relate a vector calculation to a useful decision and its limitations."
      }
    ]
  },
  "SUMMARY_TABLE": {
    "subStrand": "Sub-Strand2.8: Vectors I",
    "drivingQuestion": "How can a vector model describe a route or design change precisely? KICD: What are vectors? Where are vectors used in real-life situations?",
    "lessons": [
      {
        "number": 1,
        "title": "When is a number without direction insufficient?",
        "observed": "Opposite directions can accompany equal magnitudes.",
        "learned": "Scalars and vectors encode different information.",
        "explained": "A round trip can have positive distance and zero displacement."
      },
      {
        "number": 2,
        "title": "How can the same vector be named three ways?",
        "observed": "Different notation can describe the same directed change.",
        "learned": "A column records endpoint differences in a fixed axis system.",
        "explained": "A point and a displacement answer different questions."
      },
      {
        "number": 3,
        "title": "Can an arrow move without changing its vector?",
        "observed": "Equal vector changes can start at different points.",
        "learned": "Free-vector equivalence preserves direction and magnitude.",
        "explained": "Equal arrow lengths alone do not establish equivalence."
      },
      {
        "number": 4,
        "title": "Where does a head-to-tail route end?",
        "observed": "Two addition orders reach the same endpoint.",
        "learned": "The resultant is the direct arrow from initial tail to final head.",
        "explained": "Vector addition respects direction,not just arrow lengths."
      },
      {
        "number": 5,
        "title": "Can signed columns check a route drawing?",
        "observed": "Signed additions agree with the final plotted endpoint.",
        "learned": "Component sums combine multi-stage displacements.",
        "explained": "A return vector is the negative of the resultant."
      },
      {
        "number": 6,
        "title": "What do positive,negative and zero scalars do?",
        "observed": "Negative scaling reverses an arrow without creating a negative length.",
        "learned": "Scalar multiplication changes components consistently.",
        "explained": "The zero vector has magnitude zero and no unique direction."
      },
      {
        "number": 7,
        "title": "Which vectors change when the origin changes?",
        "observed": "Position columns change with the chosen origin.",
        "learned": "Displacement is endpoint position minus startpoint position.",
        "explained": "Both reference systems give the same P-to-Q change."
      },
      {
        "number": 8,
        "title": "How can signed components give a nonnegative magnitude?",
        "observed": "Opposite vectors have the same magnitude.",
        "learned": "Perpendicular components determine length through Pythagoras.",
        "explained": "A turning route can be longer than its net displacement."
      },
      {
        "number": 9,
        "title": "Is half a displacement the midpoint's position?",
        "observed": "Half a segment's displacement need not be its midpoint position.",
        "learned": "Endpoint averages and startpoint-plus-half-change agree.",
        "explained": "A midpoint location requires a specified representative segment/origin."
      },
      {
        "number": 10,
        "title": "What makes a whole-shape translation consistent?",
        "observed": "Every vertex shifts by one common vector.",
        "learned": "Translation preserves corresponding displacement vectors.",
        "explained": "A complete image needs consistent vertex-by-vertex evidence."
      },
      {
        "number": 11,
        "title": "What can a scaled campus route model establish?",
        "observed": "Grid units and physical distances require an explicit conversion.",
        "learned": "Vectors support checked route and midpoint calculations.",
        "explained": "A useful model does not establish real road access or safety by itself."
      },
      {
        "number": 12,
        "title": "Can another team reproduce our vector audit?",
        "observed": "Different vector claims fail different checks.",
        "learned": "A reproducible model labels origin,scale,arrowheads and operations.",
        "explained": "Independent reasoning is needed even when a shared chart is correct."
      },
      {
        "number": 13,
        "title": "Independent vector model audit",
        "observed": "Fresh coordinates reveal individual model and operation choices.",
        "learned": "Teacher records demonstrated skills from collected work.",
        "explained": "Feedback separates representation,operation,location and context errors."
      }
    ]
  }
};
