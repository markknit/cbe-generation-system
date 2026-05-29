# Data Module Schema
## Kenya CBE Lesson Plan Generator

Each sub-strand data module (`generators/data/<name>_data.js`) exports five objects:

### META
Configuration and output settings.

```javascript
const META = {
  subject:     'Biology',              // Biology | Chemistry | Physics | Mathematics
  grade:       10,
  outputDir:   'Grade 10 Bio/Bio 1.3', // relative to data/outputs/docx/
  filePrefix:  'Biology_CellStructure', // prefix for output filenames
  titleDoc:    'BIOLOGY GRADE 10: CELL STRUCTURE AND SPECIALISATION',
  subtitleDoc: 'CBE Phenomenon-Driven Lesson Sequence — Sub-Strand 1.3 (8 Lessons)',
  // Optional Section C column header overrides:
  col3Label:   'Teacher Moves',                    // default: 'Teacher Moves'
  col5Label:   'Formative Assessment Strategy',    // default: 'Formative Assessment Strategy'
  // Optional differentiation rows (3 default rows used if omitted):
  differentiationRows: [
    { need: '...', support: '...', extension: '...' },
  ],
};
```

### UNIT
Sub-strand overview data (maps to the top-of-document overview table).

```javascript
const UNIT = {
  gradeLevel:          'Grade 10',
  subject:             'Biology',
  strand:              'Strand 1.0: Cells',
  substrand:           'Sub-Strand 1.3: Cell Structure and Specialisation',
  duration:            '8 lessons × 40 minutes = 320 minutes total',
  content:             '– Cell theory\n– Organelles\n– ...',   // \n-separated bullets
  outcomes:            'a) identify...\nb) describe...',        // \n-separated
  competencies:        '– Critical Thinking...',
  values:              '– Responsibility...',
  pcis:                '– Safety...',
  careerConnections:   '...',   // optional
  focusForLessons:     '...',   // optional
  keyInquiryQuestions: '1. Why do plant and animal cells differ?\n2. How are cells specialised?',
  phenomenon:          'A salamander grows from a single fertilised cell...',
  drivingQuestion:     'How does a single cell become a complex organism?',
  storylineThread:     'L1: Phenomenon introduction...\nL2: ...',
};
```

### LESSONS
Array of lesson objects (one per lesson).

```javascript
const LESSONS = [
  {
    number:       1,
    title:        'Why Study Cells? — Phenomenon, Microscopy and the Basics',
    duration:     '40 minutes',
    substrand:    'Cell Structure and Specialisation',  // for ARES lookup
    aresKeywords: 'cell structure organelles eukaryotic biology', // ARES search terms

    slo: {
      purpose:            'Students observe...',
      knowledge:          '– Recall that cells...\n– Identify...',
      skills:             '– Observe...\n– Generate...',
      attitudes:          '– Curiosity...',
      keyInquiry:         'How does a single cell become a complex organism?',
      purposeInStoryline: 'This lesson launches the mystery...',
      safetyNotes:        'No hazards.',
    },

    overview: 'The lesson opens with a 2-minute time-lapse video...',

    framework: [
      {
        phase:               'Predict Phase',
        learnerExperience:   'Before we watch: write your prediction...',
        teacherMoves:        '"Do not evaluate yet..."\nWAIT TIME: 30 seconds.',
        sensemakingStrategy: 'Surfacing prior knowledge...',
        formativeAssessment: 'Teacher circulates and reads...',
      },
      { phase: 'Observe Phase',   ... },
      { phase: 'Explain Phase',   ... },
      { phase: 'Driving Question Board (DQB) Creation', ... },
      { phase: 'Model Building Phase', ... },
    ],

    teacherReflection: '1. What initial explanations did students give...',

    summaryTablePrompt: {
      observed:  'Watched time-lapse of salamander...',
      learned:   'Cells are the basic unit of life...',
      explained: 'The salamander grows because...',
    },
  },
  // ... more lessons
];
```

### FINAL_EXPLANATION
Data for the student assessment document.

```javascript
const FINAL_EXPLANATION = {
  subjectLabel:  'CELL STRUCTURE AND SPECIALISATION',
  instructions:  'You have completed all 8 lessons...',
  sections: [
    {
      title:    'SECTION 1: WHAT IS A CELL?',
      prompt:   'Describe the cell theory...',
      exemplar: 'The cell theory states that all living things...',
    },
    // ...
  ],
  rubric: [
    {
      criterion:  'Cell Theory',
      excellent:  'All three components stated correctly with evidence...',
      proficient: 'Two components stated...',
      developing: 'One or fewer components...',
    },
  ],
};
```

### SUMMARY_TABLE
Data for the teacher reference summary table.

```javascript
const SUMMARY_TABLE = {
  subStrand:       'Sub-Strand 1.3: Cell Structure and Specialisation',
  drivingQuestion: 'How does a single cell become a complex organism?',
  lessons: [
    {
      number:    1,
      title:     'Why Study Cells?',
      observed:  'Watched salamander time-lapse...',
      learned:   'Cells are the basic unit of life...',
      explained: 'The salamander phenomenon shows...',
    },
    // ...
  ],
};
```
