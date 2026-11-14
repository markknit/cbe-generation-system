'use strict';
module.exports = {
  "schemaVersion": "1.1.0",
  "META": {
    "subject": "Core Mathematics",
    "grade": 10,
    "substrand_id": "3.2",
    "substrand_name": "Probability I",
    "outputDir": "v2/Core_Mathematics/SS3.2_Probability_I",
    "filePrefix": "Codex_Core_Mathematics_Probability_I",
    "titleDoc": "CORE MATHEMATICS GRADE 10: PROBABILITY I",
    "subtitleDoc": "OpenAI-only evaluation • Sub-Strand 3.2 • 12 lessons • teacher review copy"
  },
  "UNIT": {
    "strand": "3.0 Statistics and Probability",
    "substrand": "Sub-Strand3.2: Probability I",
    "sep": "Experiment,record,generate event spaces,test relationships and justify weighted calculations.",
    "careers": "Illustrative data/model/game-design practices;no gambling or risk certification.",
    "focus": "Actual safe coin/die experiments,probability range,weighted sample spaces,exclusive/independent distinctions,addition/multiplication and independent trees.",
    "phenomenon": "A fictional game report assumes four terminal outcomes are equally weighted and that a losing streak makes a win due.",
    "supportingPhenomena": "Actual traycoin/die records,ordered coin/die spaces,disjoint/overlapping die events,replacement comparisons,weighted trees and no-stakes games.",
    "drivingQuestion": "How do honest trials and explicit event weights support probability claims? KICD: How is probability applied in real-life situations?",
    "storylineThread": "Range → coin → die → space → addition → independence → replacement → fairtree → weightedtree → game → application → independent evidence.",
    "content": "Experimental probability; Probability space; Mutually exclusive and independent events; Laws of Probability; Probability tree diagrams",
    "coreCompetencies": "Communication and collaboration: the learner carries out experiments such as tossing coins or throwing dice to illustrate experimental probability.\nCitizenship: the learner acknowledges Kenyan currency as they carry out experiments of tossing coins.\nSelf-efficacy: the learner appreciates his/her ability to play games related to probability.",
    "values": "Responsibility: the learner carefully tosses coins or throws dice to illustrate experimental probability.\nSocial justice: the learner plays games where they accept there is winning or losing and acknowledging honest outcomes.",
    "pcis": "Social Cohesion: the learner interacts with others freely as they discuss, create and play games related to probability.\nLife skills and values education: the learner uses different experimental events and lists down all the possible outcomes which assist in decision making.\nRoad safety: the learner discusses with peers the probability of getting pedestrians crossing the roads at undesignated areas and highlighting its dangers for public awareness.",
    "gradeLevel": "10",
    "subject": "Core Mathematics",
    "totalDuration": "12 lessons × 40 minutes = 480 minutes",
    "learningOutcomes": "perform experiments involving probabilities in different situations,\nidentify the range of probability in different situations,\ngenerate probability space of different events,\ndetermine the probability of mutually exclusive and independent events,\napply the laws of probability in different situations,\ndetermine the probability of independent events using tree diagrams,\nappreciate the application of probability in real-life situations."
  },
  "LESSONS": [
    {
      "number": 1,
      "title": "What probabilities can a model assign?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand3.2: Probability I",
      "aresKeywords": "probability experiment sample space independent mutually exclusive tree diagram",
      "slo": {
        "purpose": "Identify possible probability values and distinguish outcomes from assigned weights.",
        "knowledge": "A probability lies between0and1;counting equally likely outcomes requires an explicit model.",
        "skills": "Define events,sample space and range with reasons.",
        "attitudes": "Accept honest outcomes,share roles fairly,care for materials and avoid inventing results to fit expectations.",
        "keyInquiry": "What probabilities can a model assign?",
        "purposeInStoryline": "A fictional game team confuses outcomes with weights and claims a win is due;the class compares honest experiments with explicit probability models.",
        "safetyNotes": "Use approved clean coins/large tokens/dice in shallow trays on stable tables;gentle low tosses only,no mouth/eye contact,high throws,wagers or money/prize stakes. No roadside observation,crossing experiments or personal risk data."
      },
      "overview": "Use separate actual coin/die/game records and supplied mathematical cases. Record invalid attempts and unperformed individual actions honestly;no supplied-data performance claim.\nMaterials: PI1. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Predict whether a possible event must have probability1/2.",
          "teacherMoves": "4 minutes. Elicit an individual prediction and its probability-model assumption.",
          "sensemakingStrategy": "Commit a reasoned prediction.",
          "formativeAssessment": "Prediction states a model/event assumption."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Complete PI1 event probabilities and a labelled0to1line.",
          "teacherMoves": "16 minutes. Use16minutes for supplied/actual task;keep complete raw work without doing the learner’s reasoning.",
          "sensemakingStrategy": "Retain complete named task/trial evidence.",
          "formativeAssessment": "Raw evidence distinguishes actual,fictional and not-observed actions."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Explain impossible,certain and weighted-versus-listed outcomes.",
          "teacherMoves": "10 minutes. Use10minutes to check event sets,weights,totals and limits.",
          "sensemakingStrategy": "Connect calculation to explicit sets,weights and assumptions.",
          "formativeAssessment": "Counts,weights,branch sums and event meanings agree."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Ask what an actual coin record can establish.",
          "teacherMoves": "4 minutes. Use4minutes for a warranted next question or model limit.",
          "sensemakingStrategy": "Identify a supported next question or limit.",
          "formativeAssessment": "Claim stays within the available evidence."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Give an individual range/model explanation.",
          "teacherMoves": "6 minutes. Use6minutes to collect an individual explanation/action record.",
          "sensemakingStrategy": "Explain an individual conclusion or actual action.",
          "formativeAssessment": "Individual response/action record supports only the actual scope."
        }
      ],
      "teacherReflection": "Check each learner’s actual experiment/game contribution,raw counts/invalid policy,sample-space completeness,branch weights and independence assumptions. Confirm tray/tool access and40minute pacing;written fictional data alone cannot certify outcome a.",
      "summaryTablePrompt": {
        "observed": "Identify possible probability values and distinguish outcomes from assigned weights.",
        "learned": "A probability lies between0and1;counting equally likely outcomes requires an explicit model.",
        "explained": "Define events,sample space and range with reasons."
      }
    },
    {
      "number": 2,
      "title": "What does an honest coin experiment show?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand3.2: Probability I",
      "aresKeywords": "probability experiment sample space independent mutually exclusive tree diagram",
      "slo": {
        "purpose": "Perform a safe20valid-toss experiment and calculate actual relative frequency.",
        "knowledge": "Finite observed frequencies need not equal theoretical weights or determine the next trial.",
        "skills": "Toss,record,check valid denominator and retain invalid attempts separately.",
        "attitudes": "Accept honest outcomes,share roles fairly,care for materials and avoid inventing results to fit expectations.",
        "keyInquiry": "What does an honest coin experiment show?",
        "purposeInStoryline": "A fictional game team confuses outcomes with weights and claims a win is due;the class compares honest experiments with explicit probability models.",
        "safetyNotes": "Use approved clean coins/large tokens/dice in shallow trays on stable tables;gentle low tosses only,no mouth/eye contact,high throws,wagers or money/prize stakes. No roadside observation,crossing experiments or personal risk data."
      },
      "overview": "Use separate actual coin/die/game records and supplied mathematical cases. Record invalid attempts and unperformed individual actions honestly;no supplied-data performance claim.\nMaterials: PI2. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Predict whether20tosses must produce10heads.",
          "teacherMoves": "4 minutes. Elicit an individual prediction and its probability-model assumption.",
          "sensemakingStrategy": "Commit a reasoned prediction.",
          "formativeAssessment": "Prediction states a model/event assumption."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Carry out PI2 with actual named roles and ordered raw results.",
          "teacherMoves": "16 minutes. Use16minutes actual trials/design/play and10minutes checking across phases2–3;teacher approves trays/tokens and observes named individual toss/roll/record/check roles.",
          "sensemakingStrategy": "Retain complete named task/trial evidence.",
          "formativeAssessment": "Raw evidence distinguishes actual,fictional and not-observed actions."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Compare actual frequency with a fair-coin model without forcing agreement.",
          "teacherMoves": "10 minutes. Use10minutes to check event sets,weights,totals and limits.",
          "sensemakingStrategy": "Connect calculation to explicit sets,weights and assumptions.",
          "formativeAssessment": "Counts,weights,branch sums and event meanings agree."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Ask whether another experimental situation gives the same type of evidence.",
          "teacherMoves": "4 minutes. Use4minutes for a warranted next question or model limit.",
          "sensemakingStrategy": "Identify a supported next question or limit.",
          "formativeAssessment": "Claim stays within the available evidence."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Keep individual action evidence and honest observed/not-observed scope.",
          "teacherMoves": "6 minutes. Use6minutes to collect an individual explanation/action record.",
          "sensemakingStrategy": "Explain an individual conclusion or actual action.",
          "formativeAssessment": "Individual response/action record supports only the actual scope."
        }
      ],
      "teacherReflection": "Check each learner’s actual experiment/game contribution,raw counts/invalid policy,sample-space completeness,branch weights and independence assumptions. Confirm tray/tool access and40minute pacing;written fictional data alone cannot certify outcome a.",
      "summaryTablePrompt": {
        "observed": "Perform a safe20valid-toss experiment and calculate actual relative frequency.",
        "learned": "Finite observed frequencies need not equal theoretical weights or determine the next trial.",
        "explained": "Toss,record,check valid denominator and retain invalid attempts separately."
      }
    },
    {
      "number": 3,
      "title": "Do die frequencies prove a model fair?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand3.2: Probability I",
      "aresKeywords": "probability experiment sample space independent mutually exclusive tree diagram",
      "slo": {
        "purpose": "Perform a different actual probability experiment and reconcile frequencies.",
        "knowledge": "A complete frequency table preserves all valid trials;finite records do not prove fairness.",
        "skills": "Roll,record,tally and compare model/observed frequencies.",
        "attitudes": "Accept honest outcomes,share roles fairly,care for materials and avoid inventing results to fit expectations.",
        "keyInquiry": "Do die frequencies prove a model fair?",
        "purposeInStoryline": "A fictional game team confuses outcomes with weights and claims a win is due;the class compares honest experiments with explicit probability models.",
        "safetyNotes": "Use approved clean coins/large tokens/dice in shallow trays on stable tables;gentle low tosses only,no mouth/eye contact,high throws,wagers or money/prize stakes. No roadside observation,crossing experiments or personal risk data."
      },
      "overview": "Use separate actual coin/die/game records and supplied mathematical cases. Record invalid attempts and unperformed individual actions honestly;no supplied-data performance claim.\nMaterials: PI3. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Predict whether30rolls must give five of every face.",
          "teacherMoves": "4 minutes. Elicit an individual prediction and its probability-model assumption.",
          "sensemakingStrategy": "Commit a reasoned prediction.",
          "formativeAssessment": "Prediction states a model/event assumption."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Perform PI3 actual die trials and six-frequency check.",
          "teacherMoves": "16 minutes. Use16minutes actual trials/design/play and10minutes checking across phases2–3;teacher approves trays/tokens and observes named individual toss/roll/record/check roles.",
          "sensemakingStrategy": "Retain complete named task/trial evidence.",
          "formativeAssessment": "Raw evidence distinguishes actual,fictional and not-observed actions."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Compare even relative frequency with1/2and another group’s honest record.",
          "teacherMoves": "10 minutes. Use10minutes to check event sets,weights,totals and limits.",
          "sensemakingStrategy": "Connect calculation to explicit sets,weights and assumptions.",
          "formativeAssessment": "Counts,weights,branch sums and event meanings agree."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Ask how to list a combined coin/die sample space.",
          "teacherMoves": "4 minutes. Use4minutes for a warranted next question or model limit.",
          "sensemakingStrategy": "Identify a supported next question or limit.",
          "formativeAssessment": "Claim stays within the available evidence."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Retain named actual trial/check evidence and one model limit.",
          "teacherMoves": "6 minutes. Use6minutes to collect an individual explanation/action record.",
          "sensemakingStrategy": "Explain an individual conclusion or actual action.",
          "formativeAssessment": "Individual response/action record supports only the actual scope."
        }
      ],
      "teacherReflection": "Check each learner’s actual experiment/game contribution,raw counts/invalid policy,sample-space completeness,branch weights and independence assumptions. Confirm tray/tool access and40minute pacing;written fictional data alone cannot certify outcome a.",
      "summaryTablePrompt": {
        "observed": "Perform a different actual probability experiment and reconcile frequencies.",
        "learned": "A complete frequency table preserves all valid trials;finite records do not prove fairness.",
        "explained": "Roll,record,tally and compare model/observed frequencies."
      }
    },
    {
      "number": 4,
      "title": "How can a complete sample space prevent double counting?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand3.2: Probability I",
      "aresKeywords": "probability experiment sample space independent mutually exclusive tree diagram",
      "slo": {
        "purpose": "Generate all ordered coin/die outcomes and compute specified event probabilities.",
        "knowledge": "Sample-space completeness and weights jointly support probability calculations.",
        "skills": "List pairs,select events and count a union once.",
        "attitudes": "Accept honest outcomes,share roles fairly,care for materials and avoid inventing results to fit expectations.",
        "keyInquiry": "How can a complete sample space prevent double counting?",
        "purposeInStoryline": "A fictional game team confuses outcomes with weights and claims a win is due;the class compares honest experiments with explicit probability models.",
        "safetyNotes": "Use approved clean coins/large tokens/dice in shallow trays on stable tables;gentle low tosses only,no mouth/eye contact,high throws,wagers or money/prize stakes. No roadside observation,crossing experiments or personal risk data."
      },
      "overview": "Use separate actual coin/die/game records and supplied mathematical cases. Record invalid attempts and unperformed individual actions honestly;no supplied-data performance claim.\nMaterials: PI4. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Predict whether coin+die has8or12ordered outcomes.",
          "teacherMoves": "4 minutes. Elicit an individual prediction and its probability-model assumption.",
          "sensemakingStrategy": "Commit a reasoned prediction.",
          "formativeAssessment": "Prediction states a model/event assumption."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "List every PI4 pair and compute both events under stated assumptions.",
          "teacherMoves": "16 minutes. Use16minutes for supplied/actual task;keep complete raw work without doing the learner’s reasoning.",
          "sensemakingStrategy": "Retain complete named task/trial evidence.",
          "formativeAssessment": "Raw evidence distinguishes actual,fictional and not-observed actions."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Explain overlapping tail/die6case and possible unequal weights.",
          "teacherMoves": "10 minutes. Use10minutes to check event sets,weights,totals and limits.",
          "sensemakingStrategy": "Connect calculation to explicit sets,weights and assumptions.",
          "formativeAssessment": "Counts,weights,branch sums and event meanings agree."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Ask when event probabilities may simply add.",
          "teacherMoves": "4 minutes. Use4minutes for a warranted next question or model limit.",
          "sensemakingStrategy": "Identify a supported next question or limit.",
          "formativeAssessment": "Claim stays within the available evidence."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Submit one checked event set and probability.",
          "teacherMoves": "6 minutes. Use6minutes to collect an individual explanation/action record.",
          "sensemakingStrategy": "Explain an individual conclusion or actual action.",
          "formativeAssessment": "Individual response/action record supports only the actual scope."
        }
      ],
      "teacherReflection": "Check each learner’s actual experiment/game contribution,raw counts/invalid policy,sample-space completeness,branch weights and independence assumptions. Confirm tray/tool access and40minute pacing;written fictional data alone cannot certify outcome a.",
      "summaryTablePrompt": {
        "observed": "Generate all ordered coin/die outcomes and compute specified event probabilities.",
        "learned": "Sample-space completeness and weights jointly support probability calculations.",
        "explained": "List pairs,select events and count a union once."
      }
    },
    {
      "number": 5,
      "title": "When does the addition law need overlap?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand3.2: Probability I",
      "aresKeywords": "probability experiment sample space independent mutually exclusive tree diagram",
      "slo": {
        "purpose": "Determine disjoint/overlapping event probabilities with the correct union rule.",
        "knowledge": "Mutual exclusivity means empty intersection;general addition subtracts overlap.",
        "skills": "List events,find intersections and compute unions.",
        "attitudes": "Accept honest outcomes,share roles fairly,care for materials and avoid inventing results to fit expectations.",
        "keyInquiry": "When does the addition law need overlap?",
        "purposeInStoryline": "A fictional game team confuses outcomes with weights and claims a win is due;the class compares honest experiments with explicit probability models.",
        "safetyNotes": "Use approved clean coins/large tokens/dice in shallow trays on stable tables;gentle low tosses only,no mouth/eye contact,high throws,wagers or money/prize stakes. No roadside observation,crossing experiments or personal risk data."
      },
      "overview": "Use separate actual coin/die/game records and supplied mathematical cases. Record invalid attempts and unperformed individual actions honestly;no supplied-data performance claim.\nMaterials: PI5. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Predict whether even or prime on one die equals1/2+1/2.",
          "teacherMoves": "4 minutes. Elicit an individual prediction and its probability-model assumption.",
          "sensemakingStrategy": "Commit a reasoned prediction.",
          "formativeAssessment": "Prediction states a model/event assumption."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Complete PI5 two event-pair cases with explicit sets.",
          "teacherMoves": "16 minutes. Use16minutes for supplied/actual task;keep complete raw work without doing the learner’s reasoning.",
          "sensemakingStrategy": "Retain complete named task/trial evidence.",
          "formativeAssessment": "Raw evidence distinguishes actual,fictional and not-observed actions."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Explain disjoint versus overlap and the positive-event independence distinction.",
          "teacherMoves": "10 minutes. Use10minutes to check event sets,weights,totals and limits.",
          "sensemakingStrategy": "Connect calculation to explicit sets,weights and assumptions.",
          "formativeAssessment": "Counts,weights,branch sums and event meanings agree."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Ask how independence differs from no shared outcome.",
          "teacherMoves": "4 minutes. Use4minutes for a warranted next question or model limit.",
          "sensemakingStrategy": "Identify a supported next question or limit.",
          "formativeAssessment": "Claim stays within the available evidence."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Give an individual union calculation with its overlap check.",
          "teacherMoves": "6 minutes. Use6minutes to collect an individual explanation/action record.",
          "sensemakingStrategy": "Explain an individual conclusion or actual action.",
          "formativeAssessment": "Individual response/action record supports only the actual scope."
        }
      ],
      "teacherReflection": "Check each learner’s actual experiment/game contribution,raw counts/invalid policy,sample-space completeness,branch weights and independence assumptions. Confirm tray/tool access and40minute pacing;written fictional data alone cannot certify outcome a.",
      "summaryTablePrompt": {
        "observed": "Determine disjoint/overlapping event probabilities with the correct union rule.",
        "learned": "Mutual exclusivity means empty intersection;general addition subtracts overlap.",
        "explained": "List events,find intersections and compute unions."
      }
    },
    {
      "number": 6,
      "title": "Are independent events the same as exclusive events?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand3.2: Probability I",
      "aresKeywords": "probability experiment sample space independent mutually exclusive tree diagram",
      "slo": {
        "purpose": "Test independence with joint probability versus the product.",
        "knowledge": "Independence is a relationship between event weights,not a synonym for disjointness.",
        "skills": "Compare coin-stage and one-die event sets.",
        "attitudes": "Accept honest outcomes,share roles fairly,care for materials and avoid inventing results to fit expectations.",
        "keyInquiry": "Are independent events the same as exclusive events?",
        "purposeInStoryline": "A fictional game team confuses outcomes with weights and claims a win is due;the class compares honest experiments with explicit probability models.",
        "safetyNotes": "Use approved clean coins/large tokens/dice in shallow trays on stable tables;gentle low tosses only,no mouth/eye contact,high throws,wagers or money/prize stakes. No roadside observation,crossing experiments or personal risk data."
      },
      "overview": "Use separate actual coin/die/game records and supplied mathematical cases. Record invalid attempts and unperformed individual actions honestly;no supplied-data performance claim.\nMaterials: PI6. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Predict whether different event names guarantee independence.",
          "teacherMoves": "4 minutes. Elicit an individual prediction and its probability-model assumption.",
          "sensemakingStrategy": "Commit a reasoned prediction.",
          "formativeAssessment": "Prediction states a model/event assumption."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Complete PI6 sample spaces,joints and products.",
          "teacherMoves": "16 minutes. Use16minutes for supplied/actual task;keep complete raw work without doing the learner’s reasoning.",
          "sensemakingStrategy": "Retain complete named task/trial evidence.",
          "formativeAssessment": "Raw evidence distinguishes actual,fictional and not-observed actions."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Explain why positive-probability disjoint events fail independence.",
          "teacherMoves": "10 minutes. Use10minutes to check event sets,weights,totals and limits.",
          "sensemakingStrategy": "Connect calculation to explicit sets,weights and assumptions.",
          "formativeAssessment": "Counts,weights,branch sums and event meanings agree."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Ask what replacement changes in repeated bag draws.",
          "teacherMoves": "4 minutes. Use4minutes for a warranted next question or model limit.",
          "sensemakingStrategy": "Identify a supported next question or limit.",
          "formativeAssessment": "Claim stays within the available evidence."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Submit one verified independent and one dependent example.",
          "teacherMoves": "6 minutes. Use6minutes to collect an individual explanation/action record.",
          "sensemakingStrategy": "Explain an individual conclusion or actual action.",
          "formativeAssessment": "Individual response/action record supports only the actual scope."
        }
      ],
      "teacherReflection": "Check each learner’s actual experiment/game contribution,raw counts/invalid policy,sample-space completeness,branch weights and independence assumptions. Confirm tray/tool access and40minute pacing;written fictional data alone cannot certify outcome a.",
      "summaryTablePrompt": {
        "observed": "Test independence with joint probability versus the product.",
        "learned": "Independence is a relationship between event weights,not a synonym for disjointness.",
        "explained": "Compare coin-stage and one-die event sets."
      }
    },
    {
      "number": 7,
      "title": "Which multiplication rule fits replacement?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand3.2: Probability I",
      "aresKeywords": "probability experiment sample space independent mutually exclusive tree diagram",
      "slo": {
        "purpose": "Apply multiplication with/without replacement and distinguish conditional stage weights.",
        "knowledge": "Multiplying marginal probabilities requires independence;general stage multiplication uses conditional weights.",
        "skills": "Calculate ordered paths and distinguish exactly one from at least one.",
        "attitudes": "Accept honest outcomes,share roles fairly,care for materials and avoid inventing results to fit expectations.",
        "keyInquiry": "Which multiplication rule fits replacement?",
        "purposeInStoryline": "A fictional game team confuses outcomes with weights and claims a win is due;the class compares honest experiments with explicit probability models.",
        "safetyNotes": "Use approved clean coins/large tokens/dice in shallow trays on stable tables;gentle low tosses only,no mouth/eye contact,high throws,wagers or money/prize stakes. No roadside observation,crossing experiments or personal risk data."
      },
      "overview": "Use separate actual coin/die/game records and supplied mathematical cases. Record invalid attempts and unperformed individual actions honestly;no supplied-data performance claim.\nMaterials: PI7. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Predict whether removing a red token leaves the next red chance unchanged.",
          "teacherMoves": "4 minutes. Elicit an individual prediction and its probability-model assumption.",
          "sensemakingStrategy": "Commit a reasoned prediction.",
          "formativeAssessment": "Prediction states a model/event assumption."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Complete PI7 replacement calculations and the one without-replacement comparison.",
          "teacherMoves": "16 minutes. Use16minutes for supplied/actual task;keep complete raw work without doing the learner’s reasoning.",
          "sensemakingStrategy": "Retain complete named task/trial evidence.",
          "formativeAssessment": "Raw evidence distinguishes actual,fictional and not-observed actions."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Explain uniform blind draw/remixing and changing conditional probability.",
          "teacherMoves": "10 minutes. Use10minutes to check event sets,weights,totals and limits.",
          "sensemakingStrategy": "Connect calculation to explicit sets,weights and assumptions.",
          "formativeAssessment": "Counts,weights,branch sums and event meanings agree."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Ask how a tree could display every stage/path.",
          "teacherMoves": "4 minutes. Use4minutes for a warranted next question or model limit.",
          "sensemakingStrategy": "Identify a supported next question or limit.",
          "formativeAssessment": "Claim stays within the available evidence."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Give a correctly justified product and model limit.",
          "teacherMoves": "6 minutes. Use6minutes to collect an individual explanation/action record.",
          "sensemakingStrategy": "Explain an individual conclusion or actual action.",
          "formativeAssessment": "Individual response/action record supports only the actual scope."
        }
      ],
      "teacherReflection": "Check each learner’s actual experiment/game contribution,raw counts/invalid policy,sample-space completeness,branch weights and independence assumptions. Confirm tray/tool access and40minute pacing;written fictional data alone cannot certify outcome a.",
      "summaryTablePrompt": {
        "observed": "Apply multiplication with/without replacement and distinguish conditional stage weights.",
        "learned": "Multiplying marginal probabilities requires independence;general stage multiplication uses conditional weights.",
        "explained": "Calculate ordered paths and distinguish exactly one from at least one."
      }
    },
    {
      "number": 8,
      "title": "Why do paths multiply and terminal alternatives add?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand3.2: Probability I",
      "aresKeywords": "probability experiment sample space independent mutually exclusive tree diagram",
      "slo": {
        "purpose": "Draw a full independent two-coin probability tree and combine selected paths.",
        "knowledge": "Independent stages can generate mutually exclusive terminal outcomes;the ideas describe different relationships.",
        "skills": "Label all branches/paths and calculate exactly/atleast/no cases.",
        "attitudes": "Accept honest outcomes,share roles fairly,care for materials and avoid inventing results to fit expectations.",
        "keyInquiry": "Why do paths multiply and terminal alternatives add?",
        "purposeInStoryline": "A fictional game team confuses outcomes with weights and claims a win is due;the class compares honest experiments with explicit probability models.",
        "safetyNotes": "Use approved clean coins/large tokens/dice in shallow trays on stable tables;gentle low tosses only,no mouth/eye contact,high throws,wagers or money/prize stakes. No roadside observation,crossing experiments or personal risk data."
      },
      "overview": "Use separate actual coin/die/game records and supplied mathematical cases. Record invalid attempts and unperformed individual actions honestly;no supplied-data performance claim.\nMaterials: PI8. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Predict whether two-stage outcomes are all mutually exclusive or all independent.",
          "teacherMoves": "4 minutes. Elicit an individual prediction and its probability-model assumption.",
          "sensemakingStrategy": "Commit a reasoned prediction.",
          "formativeAssessment": "Prediction states a model/event assumption."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Construct PI8 full tree with branch/path labels.",
          "teacherMoves": "16 minutes. Use16minutes for supplied/actual task;keep complete raw work without doing the learner’s reasoning.",
          "sensemakingStrategy": "Retain complete named task/trial evidence.",
          "formativeAssessment": "Raw evidence distinguishes actual,fictional and not-observed actions."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Explain node sums,path products and disjoint-path sums.",
          "teacherMoves": "10 minutes. Use10minutes to check event sets,weights,totals and limits.",
          "sensemakingStrategy": "Connect calculation to explicit sets,weights and assumptions.",
          "formativeAssessment": "Counts,weights,branch sums and event meanings agree."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Ask what changes if branch weights are unequal.",
          "teacherMoves": "4 minutes. Use4minutes for a warranted next question or model limit.",
          "sensemakingStrategy": "Identify a supported next question or limit.",
          "formativeAssessment": "Claim stays within the available evidence."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Submit one tree-supported complement/union calculation.",
          "teacherMoves": "6 minutes. Use6minutes to collect an individual explanation/action record.",
          "sensemakingStrategy": "Explain an individual conclusion or actual action.",
          "formativeAssessment": "Individual response/action record supports only the actual scope."
        }
      ],
      "teacherReflection": "Check each learner’s actual experiment/game contribution,raw counts/invalid policy,sample-space completeness,branch weights and independence assumptions. Confirm tray/tool access and40minute pacing;written fictional data alone cannot certify outcome a.",
      "summaryTablePrompt": {
        "observed": "Draw a full independent two-coin probability tree and combine selected paths.",
        "learned": "Independent stages can generate mutually exclusive terminal outcomes;the ideas describe different relationships.",
        "explained": "Label all branches/paths and calculate exactly/atleast/no cases."
      }
    },
    {
      "number": 9,
      "title": "How do unequal branch weights change a tree?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand3.2: Probability I",
      "aresKeywords": "probability experiment sample space independent mutually exclusive tree diagram",
      "slo": {
        "purpose": "Draw a weighted independent bag tree and compare two event definitions.",
        "knowledge": "A complete list of four outcomes does not imply equal terminal weights.",
        "skills": "Construct a weighted tree and verify total/complement.",
        "attitudes": "Accept honest outcomes,share roles fairly,care for materials and avoid inventing results to fit expectations.",
        "keyInquiry": "How do unequal branch weights change a tree?",
        "purposeInStoryline": "A fictional game team confuses outcomes with weights and claims a win is due;the class compares honest experiments with explicit probability models.",
        "safetyNotes": "Use approved clean coins/large tokens/dice in shallow trays on stable tables;gentle low tosses only,no mouth/eye contact,high throws,wagers or money/prize stakes. No roadside observation,crossing experiments or personal risk data."
      },
      "overview": "Use separate actual coin/die/game records and supplied mathematical cases. Record invalid attempts and unperformed individual actions honestly;no supplied-data performance claim.\nMaterials: PI9. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Predict whether three of four bag paths means probability3/4.",
          "teacherMoves": "4 minutes. Elicit an individual prediction and its probability-model assumption.",
          "sensemakingStrategy": "Commit a reasoned prediction.",
          "formativeAssessment": "Prediction states a model/event assumption."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Draw PI9 full tree and compute at least/exactly one red.",
          "teacherMoves": "16 minutes. Use16minutes for supplied/actual task;keep complete raw work without doing the learner’s reasoning.",
          "sensemakingStrategy": "Retain complete named task/trial evidence.",
          "formativeAssessment": "Raw evidence distinguishes actual,fictional and not-observed actions."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Check path total1and agreement between direct sum and complement.",
          "teacherMoves": "10 minutes. Use10minutes to check event sets,weights,totals and limits.",
          "sensemakingStrategy": "Connect calculation to explicit sets,weights and assumptions.",
          "formativeAssessment": "Counts,weights,branch sums and event meanings agree."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Ask how a declared chance model can define a no-stakes game.",
          "teacherMoves": "4 minutes. Use4minutes for a warranted next question or model limit.",
          "sensemakingStrategy": "Identify a supported next question or limit.",
          "formativeAssessment": "Claim stays within the available evidence."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Give a tree calculation and a rejected equal-weight shortcut.",
          "teacherMoves": "6 minutes. Use6minutes to collect an individual explanation/action record.",
          "sensemakingStrategy": "Explain an individual conclusion or actual action.",
          "formativeAssessment": "Individual response/action record supports only the actual scope."
        }
      ],
      "teacherReflection": "Check each learner’s actual experiment/game contribution,raw counts/invalid policy,sample-space completeness,branch weights and independence assumptions. Confirm tray/tool access and40minute pacing;written fictional data alone cannot certify outcome a.",
      "summaryTablePrompt": {
        "observed": "Draw a weighted independent bag tree and compare two event definitions.",
        "learned": "A complete list of four outcomes does not imply equal terminal weights.",
        "explained": "Construct a weighted tree and verify total/complement."
      }
    },
    {
      "number": 10,
      "title": "Can we make and play an honest modelled game?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand3.2: Probability I",
      "aresKeywords": "probability experiment sample space independent mutually exclusive tree diagram",
      "slo": {
        "purpose": "Create and play a safe no-stakes game with declared rules and honest results.",
        "knowledge": "A theoretical win chance and an actual short-run record answer different questions.",
        "skills": "Define outcomes,play/record/check and reject the due-win fallacy.",
        "attitudes": "Accept honest outcomes,share roles fairly,care for materials and avoid inventing results to fit expectations.",
        "keyInquiry": "Can we make and play an honest modelled game?",
        "purposeInStoryline": "A fictional game team confuses outcomes with weights and claims a win is due;the class compares honest experiments with explicit probability models.",
        "safetyNotes": "Use approved clean coins/large tokens/dice in shallow trays on stable tables;gentle low tosses only,no mouth/eye contact,high throws,wagers or money/prize stakes. No roadside observation,crossing experiments or personal risk data."
      },
      "overview": "Use separate actual coin/die/game records and supplied mathematical cases. Record invalid attempts and unperformed individual actions honestly;no supplied-data performance claim.\nMaterials: PI10. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Predict whether a losing streak makes a win certain next.",
          "teacherMoves": "4 minutes. Elicit an individual prediction and its probability-model assumption.",
          "sensemakingStrategy": "Commit a reasoned prediction.",
          "formativeAssessment": "Prediction states a model/event assumption."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Design and play PI10 actual12valid rounds with rotating named roles.",
          "teacherMoves": "16 minutes. Use16minutes actual trials/design/play and10minutes checking across phases2–3;teacher approves trays/tokens and observes named individual toss/roll/record/check roles.",
          "sensemakingStrategy": "Retain complete named task/trial evidence.",
          "formativeAssessment": "Raw evidence distinguishes actual,fictional and not-observed actions."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Compare theoretical/observed win frequencies without altering outcomes.",
          "teacherMoves": "10 minutes. Use10minutes to check event sets,weights,totals and limits.",
          "sensemakingStrategy": "Connect calculation to explicit sets,weights and assumptions.",
          "formativeAssessment": "Counts,weights,branch sums and event meanings agree."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Ask how useful probability claims should state risk/assumptions.",
          "teacherMoves": "4 minutes. Use4minutes for a warranted next question or model limit.",
          "sensemakingStrategy": "Identify a supported next question or limit.",
          "formativeAssessment": "Claim stays within the available evidence."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Record actual design/play contribution and one reasoned benefit/limit.",
          "teacherMoves": "6 minutes. Use6minutes to collect an individual explanation/action record.",
          "sensemakingStrategy": "Explain an individual conclusion or actual action.",
          "formativeAssessment": "Individual response/action record supports only the actual scope."
        }
      ],
      "teacherReflection": "Check each learner’s actual experiment/game contribution,raw counts/invalid policy,sample-space completeness,branch weights and independence assumptions. Confirm tray/tool access and40minute pacing;written fictional data alone cannot certify outcome a.",
      "summaryTablePrompt": {
        "observed": "Create and play a safe no-stakes game with declared rules and honest results.",
        "learned": "A theoretical win chance and an actual short-run record answer different questions.",
        "explained": "Define outcomes,play/record/check and reject the due-win fallacy."
      }
    },
    {
      "number": 11,
      "title": "Which probability applications respect their limits?",
      "duration": "40 minutes",
      "substrand": "Sub-Strand3.2: Probability I",
      "aresKeywords": "probability experiment sample space independent mutually exclusive tree diagram",
      "slo": {
        "purpose": "Check an application/addition/tree claim and communicate a safe bounded message.",
        "knowledge": "Probability reasoning needs evidence and model assumptions;unknown risk is not zero.",
        "skills": "Verify a source/model claim and explain a useful limited application.",
        "attitudes": "Accept honest outcomes,share roles fairly,care for materials and avoid inventing results to fit expectations.",
        "keyInquiry": "Which probability applications respect their limits?",
        "purposeInStoryline": "A fictional game team confuses outcomes with weights and claims a win is due;the class compares honest experiments with explicit probability models.",
        "safetyNotes": "Use approved clean coins/large tokens/dice in shallow trays on stable tables;gentle low tosses only,no mouth/eye contact,high throws,wagers or money/prize stakes. No roadside observation,crossing experiments or personal risk data."
      },
      "overview": "Use separate actual coin/die/game records and supplied mathematical cases. Record invalid attempts and unperformed individual actions honestly;no supplied-data performance claim.\nMaterials: PI5; PI8; PI11. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 10 min, Driving Question Board (DQB) Creation 4 min, Model Building 6 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Predict whether a guessed small risk justifies an unsafe crossing.",
          "teacherMoves": "4 minutes. Elicit an individual prediction and its probability-model assumption.",
          "sensemakingStrategy": "Commit a reasoned prediction.",
          "formativeAssessment": "Prediction states a model/event assumption."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Complete PI11 application/source check with PI5orPI8as the test case.",
          "teacherMoves": "16 minutes. Use16minutes application/source work and10minutes claim verification across phases2–3;approved digital access only,PI5/PI8printedbackup with digitalNOTOBSERVEDif unavailable.",
          "sensemakingStrategy": "Retain complete named task/trial evidence.",
          "formativeAssessment": "Raw evidence distinguishes actual,fictional and not-observed actions."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Explain an addition/tree claim and reject invented numerical road-risk conclusions.",
          "teacherMoves": "10 minutes. Use10minutes to check event sets,weights,totals and limits.",
          "sensemakingStrategy": "Connect calculation to explicit sets,weights and assumptions.",
          "formativeAssessment": "Counts,weights,branch sums and event meanings agree."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Prepare final procedure only;withhold PI12data and keys.",
          "teacherMoves": "4 minutes. Use4minutes for a warranted next question or model limit.",
          "sensemakingStrategy": "Identify a supported next question or limit.",
          "formativeAssessment": "Claim stays within the available evidence."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Give a useful application,assumption and safe evidence limit.",
          "teacherMoves": "6 minutes. Use6minutes to collect an individual explanation/action record.",
          "sensemakingStrategy": "Explain an individual conclusion or actual action.",
          "formativeAssessment": "Individual response/action record supports only the actual scope."
        }
      ],
      "teacherReflection": "Check each learner’s actual experiment/game contribution,raw counts/invalid policy,sample-space completeness,branch weights and independence assumptions. Confirm tray/tool access and40minute pacing;written fictional data alone cannot certify outcome a.",
      "summaryTablePrompt": {
        "observed": "Check an application/addition/tree claim and communicate a safe bounded message.",
        "learned": "Probability reasoning needs evidence and model assumptions;unknown risk is not zero.",
        "explained": "Verify a source/model claim and explain a useful limited application."
      }
    },
    {
      "number": 12,
      "title": "Independent probability model and evidence",
      "duration": "40 minutes",
      "substrand": "Sub-Strand3.2: Probability I",
      "aresKeywords": "probability experiment sample space independent mutually exclusive tree diagram",
      "slo": {
        "purpose": "Independently interpret frequencies,generate weighted outcomes and apply addition/tree laws.",
        "knowledge": "Written fictional data do not certify experimental performance;terminal weights and event relationships must be justified.",
        "skills": "List,draw,calculate and bound an application claim.",
        "attitudes": "Accept honest outcomes,share roles fairly,care for materials and avoid inventing results to fit expectations.",
        "keyInquiry": "Independent probability model and evidence",
        "purposeInStoryline": "A fictional game team confuses outcomes with weights and claims a win is due;the class compares honest experiments with explicit probability models.",
        "safetyNotes": "Use approved clean coins/large tokens/dice in shallow trays on stable tables;gentle low tosses only,no mouth/eye contact,high throws,wagers or money/prize stakes. No roadside observation,crossing experiments or personal risk data."
      },
      "overview": "Use separate actual coin/die/game records and supplied mathematical cases. Record invalid attempts and unperformed individual actions honestly;no supplied-data performance claim.\nMaterials: PI12. Use the companion Student Materials and Teacher Materials Key. Pacing: Predict 4 min, Observe 16 min, Explain 12 min, Driving Question Board (DQB) Creation 4 min, Model Building 4 min.",
      "framework": [
        {
          "phase": "Predict Phase",
          "learnerExperience": "Read independent instructions and arrange PI12and blank paper.",
          "teacherMoves": "4 minutes. 4minutes procedure only;no worked final probability example.",
          "sensemakingStrategy": "Work independently without hints or peer feedback.",
          "formativeAssessment": "Prediction states a model/event assumption."
        },
        {
          "phase": "Observe Phase",
          "learnerExperience": "Complete sections1–2 independently.",
          "teacherMoves": "16 minutes. 16minutes independent sections1–2;no teacher content hints.",
          "sensemakingStrategy": "Work independently without hints or peer feedback.",
          "formativeAssessment": "Raw evidence distinguishes actual,fictional and not-observed actions."
        },
        {
          "phase": "Explain Phase",
          "learnerExperience": "Complete section3 weighted tree/event calculations independently.",
          "teacherMoves": "12 minutes. 12minutes independent section3;no shared tree or peer comparison.",
          "sensemakingStrategy": "Work independently without hints or peer feedback.",
          "formativeAssessment": "Counts,weights,branch sums and event meanings agree."
        },
        {
          "phase": "Driving Question Board (DQB) Creation",
          "learnerExperience": "Complete section4 application/performance evidence limits independently.",
          "teacherMoves": "4 minutes. 4minutes independent section4;no feedback on risk/application.",
          "sensemakingStrategy": "Work independently without hints or peer feedback.",
          "formativeAssessment": "Claim stays within the available evidence."
        },
        {
          "phase": "Model Building Phase",
          "learnerExperience": "Hand in all labelled individual work.",
          "teacherMoves": "4 minutes. 4minutes checking/collection;keys and teaching cards withheld.",
          "sensemakingStrategy": "Work independently without hints or peer feedback.",
          "formativeAssessment": "Individual response/action record supports only the actual scope."
        }
      ],
      "teacherReflection": "Check each learner’s actual experiment/game contribution,raw counts/invalid policy,sample-space completeness,branch weights and independence assumptions. Confirm tray/tool access and40minute pacing;written fictional data alone cannot certify outcome a.",
      "summaryTablePrompt": {
        "observed": "Independently interpret frequencies,generate weighted outcomes and apply addition/tree laws.",
        "learned": "Written fictional data do not certify experimental performance;terminal weights and event relationships must be justified.",
        "explained": "List,draw,calculate and bound an application claim."
      }
    }
  ],
  "FINAL_EXPLANATION": {
    "subjectLabel": "PROBABILITY I",
    "instructions": "Lesson12,40minutes:4procedure,16sections1–2,12section3,4section4,4checking/collection. Work independently with PI12only,calculator if approved and blank paper. No coins/dice/game,teaching cards,peers,hints or media. Show event sets,tree branches,path weights and assumptions. Fictional data do not certify actual experiment performance.",
    "sections": [
      {
        "title": "1. Experimental frequency and probability range",
        "prompt": "For FinalAcalculate Hrelativefrequency using the declared valid-trial denominator;state how the invalid attempts are reported. Explain what this finite record can and cannot establish about a fair-coin model or the next toss. State the probability range and distinguish impossible,certain and possible-with-unspecified-weight events.",
        "exemplar": "18/30=3/5=0.6;2invalidattemptsreportedseparately,notreclassifiedvalid. Finitefrequencydoesnotprovefairness,bias,nextresultorcompensation.0≤P≤1;impossible0,certain1underdefinedspace;possiblealonedoesnotassignnumericweight. Writtenrecordisnotperformedexperiment."
      },
      {
        "title": "2. Event space,exclusivity and independence",
        "prompt": "For FinalB,list the six-face space,E,F,intersection and union;calculate their probabilities. Are EandFmutually exclusive? Are they independent? Justify with joint probability and product. State the general addition rule and why no overlap subtraction is needed here.",
        "exemplar": "Space1–6,E2/4/6,F1/3,intersectionempty,Pjoint0,union1/2/3/4/6,Punion5/6. P(E)1/2,P(F)1/3,product1/6not0;disjointpositiveeventsnotindependent. P(EorF)=P(E)+P(F)-P(EandF);intersectionzerohere."
      },
      {
        "title": "3. Independent weighted probability tree",
        "prompt": "Draw FinalCfull two-stage tree,with all branch/path probabilities. Generate all ordered terminal outcomes and show their total probability. Calculate P(HorR)and P(exactly one of H,R);show selected paths or overlap reasoning. Explain why counting three of the four outcomes as equally likely would be invalid.",
        "exemplar": "CoinH/T1/2;eachspinnernodeR2/3,B1/3. HR1/3,HB1/6,TR1/3,TB1/6,total1. H orR=HR+HB+TR=5/6;also1/2+2/3-1/3=5/6. ExactlyoneHB+TR=1/2. Terminalweightsunequal;independentstagesdifferfromdisjointterminalpaths."
      },
      {
        "title": "4. Application and separate performed evidence",
        "prompt": "Explain one useful probability application with a model assumption and a limitation. Explain why no numerical road-crash probability follows from a fictional awareness discussion,and why uncertainty must not justify unsafe crossing. Name one actual individual observation needed to certify your probability-experiment performance.",
        "exemplar": "Accept fairgame/planning/samplingusewithsample/weight/independencelimit. No actualexposure/outcomerecordorvalidatedriskmodelmeansnocrashprobabilityassigned;unknownisnotzeroanddoesnotexcuserisk. Teacherneedsactualnamedtoss/roll/record/checkwithrawvalid/invalidrecordinF2/F3,supportedbyartifact;writtenfictionalinterpretationaloneisnotoutcomea. Reasonedbenefitisnotpersistentattitudecertification."
      }
    ],
    "rubric": [
      {
        "criterion": "Interpret experimental evidence and range",
        "excellent": "Correct valid-denominator result/range and precise invalid-trial/model/next-outcome limits.",
        "proficient": "Correct frequency/range and valid distinctions between finite evidence and model claims.",
        "developing": "Some correct interpretation but denominator,range or fairness/next-outcome claim needs correction.",
        "belowExpectations": "Needs guided event/weight/evidence questions to build a supported conclusion."
      },
      {
        "criterion": "Generate events and apply addition/independence",
        "excellent": "Complete event sets/probabilities with precise disjointness,product and overlap reasoning.",
        "proficient": "Correct event probabilities and justified exclusivity/independence/addition distinctions.",
        "developing": "Some valid sets/results but overlap,event relationship or law needs correction.",
        "belowExpectations": "Needs guided event/weight/evidence questions to build a supported conclusion."
      },
      {
        "criterion": "Construct a weighted independent tree",
        "excellent": "Complete labelled tree/all weights,total1,both event results and clear unequal-weight/stage-versus-path reasoning.",
        "proficient": "Correct full tree,path weights and selected event probabilities with valid assumptions.",
        "developing": "Some valid branches/results but weight,selection,total or relationship needs correction.",
        "belowExpectations": "Needs guided event/weight/evidence questions to build a supported conclusion."
      },
      {
        "criterion": "Explain useful application and evidence limits",
        "excellent": "Specific useful conditional application with careful road-risk/evidence reasoning and actual-action requirement.",
        "proficient": "Useful application/limit and correct separate performed-evidence and safe-awareness distinctions.",
        "developing": "Application plausible but assumption,risk or actual-action evidence needs correction.",
        "belowExpectations": "Needs guided event/weight/evidence questions to build a supported conclusion."
      }
    ]
  },
  "SUMMARY_TABLE": {
    "subStrand": "Sub-Strand3.2: Probability I",
    "drivingQuestion": "How do honest trials and explicit event weights support probability claims? KICD: How is probability applied in real-life situations?",
    "lessons": [
      {
        "number": 1,
        "title": "What probabilities can a model assign?",
        "observed": "Identify possible probability values and distinguish outcomes from assigned weights.",
        "learned": "A probability lies between0and1;counting equally likely outcomes requires an explicit model.",
        "explained": "Define events,sample space and range with reasons."
      },
      {
        "number": 2,
        "title": "What does an honest coin experiment show?",
        "observed": "Perform a safe20valid-toss experiment and calculate actual relative frequency.",
        "learned": "Finite observed frequencies need not equal theoretical weights or determine the next trial.",
        "explained": "Toss,record,check valid denominator and retain invalid attempts separately."
      },
      {
        "number": 3,
        "title": "Do die frequencies prove a model fair?",
        "observed": "Perform a different actual probability experiment and reconcile frequencies.",
        "learned": "A complete frequency table preserves all valid trials;finite records do not prove fairness.",
        "explained": "Roll,record,tally and compare model/observed frequencies."
      },
      {
        "number": 4,
        "title": "How can a complete sample space prevent double counting?",
        "observed": "Generate all ordered coin/die outcomes and compute specified event probabilities.",
        "learned": "Sample-space completeness and weights jointly support probability calculations.",
        "explained": "List pairs,select events and count a union once."
      },
      {
        "number": 5,
        "title": "When does the addition law need overlap?",
        "observed": "Determine disjoint/overlapping event probabilities with the correct union rule.",
        "learned": "Mutual exclusivity means empty intersection;general addition subtracts overlap.",
        "explained": "List events,find intersections and compute unions."
      },
      {
        "number": 6,
        "title": "Are independent events the same as exclusive events?",
        "observed": "Test independence with joint probability versus the product.",
        "learned": "Independence is a relationship between event weights,not a synonym for disjointness.",
        "explained": "Compare coin-stage and one-die event sets."
      },
      {
        "number": 7,
        "title": "Which multiplication rule fits replacement?",
        "observed": "Apply multiplication with/without replacement and distinguish conditional stage weights.",
        "learned": "Multiplying marginal probabilities requires independence;general stage multiplication uses conditional weights.",
        "explained": "Calculate ordered paths and distinguish exactly one from at least one."
      },
      {
        "number": 8,
        "title": "Why do paths multiply and terminal alternatives add?",
        "observed": "Draw a full independent two-coin probability tree and combine selected paths.",
        "learned": "Independent stages can generate mutually exclusive terminal outcomes;the ideas describe different relationships.",
        "explained": "Label all branches/paths and calculate exactly/atleast/no cases."
      },
      {
        "number": 9,
        "title": "How do unequal branch weights change a tree?",
        "observed": "Draw a weighted independent bag tree and compare two event definitions.",
        "learned": "A complete list of four outcomes does not imply equal terminal weights.",
        "explained": "Construct a weighted tree and verify total/complement."
      },
      {
        "number": 10,
        "title": "Can we make and play an honest modelled game?",
        "observed": "Create and play a safe no-stakes game with declared rules and honest results.",
        "learned": "A theoretical win chance and an actual short-run record answer different questions.",
        "explained": "Define outcomes,play/record/check and reject the due-win fallacy."
      },
      {
        "number": 11,
        "title": "Which probability applications respect their limits?",
        "observed": "Check an application/addition/tree claim and communicate a safe bounded message.",
        "learned": "Probability reasoning needs evidence and model assumptions;unknown risk is not zero.",
        "explained": "Verify a source/model claim and explain a useful limited application."
      },
      {
        "number": 12,
        "title": "Independent probability model and evidence",
        "observed": "Independently interpret frequencies,generate weighted outcomes and apply addition/tree laws.",
        "learned": "Written fictional data do not certify experimental performance;terminal weights and event relationships must be justified.",
        "explained": "List,draw,calculate and bound an application claim."
      }
    ]
  }
};
