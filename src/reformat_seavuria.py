"""
Reformat Seavuria Lesson Plan documents into the locked Biology Plant Nutrition format.

Produces 9 output files (3 doc types × 3 subjects):
  - CBE_LessonSequence.docx  — per-lesson 5-table blocks (A SLOs, B Materials,
                                C 6-col implementation, D Reflection, E Summary Prompt)
  - FinalExplanation.docx    — 8-table student document
  - SummaryTable.docx        — 3-table student tracking document

Reference format: data/outputs/docx/Grade 10 Bio/Bio 2.1 Plant Nutrition/docx/
"""

import re
from pathlib import Path
from typing import Optional

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.text.paragraph import Paragraph as DocxParagraph
from docx.table import Table as DocxTable

# ── paths ─────────────────────────────────────────────────────────────────────
SRC_DIR = Path("data/raw/Seavuria Lesson Plans")
OUT_DIR = Path("data/outputs/Seavuria_Reformatted")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── color constants ───────────────────────────────────────────────────────────
C_NAVY      = "1F3864"   # titles, phase col header, Table A banner
C_TEAL      = "1F6B75"   # subtitles, Table B / resource / sensemaking headers
C_MED_BLUE  = "2E75B6"   # learner exp / teacher actions / assessment headers
C_PURPLE    = "7030A0"   # Table E header, summary DQB col header
C_ORANGE    = "C55A11"   # Table D header
C_LT_BLUE   = "D5E8F0"   # SLO labels, key inquiry bg, summary lesson# col
C_TEAL_LT   = "D9EEF1"   # Observe phase row
C_GREEN_LT  = "E2EFDA"   # Explain phase row
C_PURPLE_LT = "EAD1F5"   # Predict phase row, Table E row labels, DQB col
C_ORANGE_LT = "FCE4D6"   # DQB phase row, Table D content
C_LT_GRAY   = "F2F2F2"   # alternating content rows
C_WHITE     = "FFFFFF"

PHASE_FILLS = [C_PURPLE_LT, C_TEAL_LT, C_GREEN_LT, C_ORANGE_LT, C_LT_BLUE]
PHASE_NAMES = ["Predict", "Observe", "Explain", "DQB", "Model Building"]

FONT = "Calibri"

# ── META — subject metadata ───────────────────────────────────────────────────
META = {
    "chemistry": {
        "subject":    "Chemistry",
        "grade":      "Grade 10",
        "strand":     "Strand 1.0: Inorganic Chemistry",
        "substrand":  "Sub-Strand 1.4: Chemical Bonding",
        "lessons":    13,
        "driving_question": "How do the bonds between atoms determine the properties and uses of substances?",
        "phenomenon": (
            "A diamond and a graphite pencil tip are both made of pure carbon — "
            "yet diamond is the hardest natural substance and graphite is soft enough to write with. "
            "How can the same element behave so differently?"
        ),
        "substrand_overview_rows": [
            ("Subject",           "Chemistry"),
            ("Grade",             "Grade 10"),
            ("Strand",            "Strand 1.0: Inorganic Chemistry"),
            ("Sub-Strand",        "Sub-Strand 1.4: Chemical Bonding"),
            ("Number of Lessons", "13"),
            ("Number of Periods", "26"),
            ("Anchoring Phenomenon",
             "A diamond and a graphite pencil tip are both made of pure carbon — yet diamond is the "
             "hardest natural substance and graphite is soft enough to write with. How can the same element behave so differently?"),
            ("Driving Question",  "How do the bonds between atoms determine the properties and uses of substances?"),
            ("Sub-Strand SLOs: Knowledge",
             "Explain ionic, covalent, dative covalent, metallic, hydrogen, and Van der Waals bonding; "
             "describe the structures and properties of substances formed by each bond type."),
            ("Sub-Strand SLOs: Skills",
             "Draw Lewis dot diagrams; construct and interpret models of bonding; "
             "predict properties from structure; solve problems involving bonding and properties."),
            ("Sub-Strand SLOs: Attitudes & Values",
             "Appreciate how atomic-level bonding determines the macroscopic properties and uses of materials; "
             "connect chemistry to everyday Kenyan life."),
            ("Assessment",        "Formative: observation, discussion, models, summary table.\nSummative: Final Explanation document."),
            ("Core Values",       "Curiosity, critical thinking, connection to context"),
            ("Resources",         "Periodic table, molecular model kits, samples of ionic/covalent/metallic substances"),
            ("Notes",             ""),
        ],
        "final_explanation_sections": [
            (
                "Section 1: Why Do Atoms Form Bonds?",
                "What makes an atom stable or unstable?\n"
                "What are valence electrons and why are they important?\n"
                "What is the octet rule? When does the duplet rule apply?\n"
                "How does bonding help atoms achieve stability?",
            ),
            (
                "Section 2: How Do Ionic Bonds Form and What Properties Do They Give Substances?",
                "How do ionic bonds form through electron transfer?\n"
                "What types of atoms form ionic bonds?\n"
                "How can we represent ionic bonding using Lewis diagrams?\n"
                "What properties do ionic compounds have (melting point, conductivity, solubility, brittleness)?\n"
                "Why do ionic compounds have these properties?",
            ),
            (
                "Section 3: How Do Covalent Bonds Form and What Structures Do They Create?",
                "How do covalent bonds form through electron sharing?\n"
                "What is the difference between simple molecular and giant covalent structures?\n"
                "How do diamond and graphite differ in structure despite both being carbon?\n"
                "What properties do simple molecular substances have vs. giant covalent structures?\n"
                "Draw Lewis diagrams for simple molecules (H₂, H₂O, CO₂, CH₄).",
            ),
            (
                "Section 4: What Are Dative Covalent, Metallic, Hydrogen, and Van der Waals Bonds?",
                "What is a dative covalent bond and how does it differ from a regular covalent bond?\n"
                "How do metallic bonds form and what properties do they give?\n"
                "What are hydrogen bonds and when do they form?\n"
                "What are Van der Waals forces and how do they affect properties?",
            ),
            (
                "Section 5: How Does Bond Type Explain Physical Properties and Real-Life Uses?",
                "Create a comparison table of ionic, simple molecular, giant covalent, and metallic substances "
                "(covering melting point, conductivity, hardness, solubility).\n"
                "Choose at least 4 substances and explain how their bonding and structure make them suitable for their uses "
                "(e.g. NaCl, diamond, graphite, copper, water).\n"
                "Answer the driving question: How do the bonds between atoms determine the properties and uses of substances?",
            ),
        ],
        "final_explanation_rubric": {
            "headers": ["Criterion", "Beginning (1)", "Developing (2)", "Proficient (3)", "Advanced (4)"],
            "rows": [
                ("1. Completeness",
                 "Fewer than 3 sections addressed; major gaps",
                 "4 sections with some key concepts missing",
                 "All 5 sections addressed with all key concepts",
                 "All 5 sections comprehensively with depth and connections"),
                ("2. Scientific Accuracy",
                 "Multiple significant errors in bonding concepts",
                 "Some minor errors; 2–3 misconceptions",
                 "Scientifically accurate; no significant errors",
                 "Accurate with nuanced understanding; addresses exceptions"),
                ("3. Explanation Quality",
                 "Mostly describes without explaining why; limited cause-effect",
                 "Some explanations but reasoning incomplete or unclear",
                 "Clearly explains using cause-and-effect throughout",
                 "Deep, sophisticated explanations with multiple lines of reasoning"),
                ("4. Structure-Property Connections",
                 "Does not connect atomic structure to macroscopic properties",
                 "Some connections but superficial or incomplete",
                 "Consistently connects structure to properties across bond types",
                 "Sophisticated connections; compares and contrasts multiple substances"),
                ("5. Diagrams & Communication",
                 "Missing diagrams; vague language; poor organization",
                 "Some diagrams; inconsistent vocabulary; some errors",
                 "Appropriate labeled diagrams; scientific vocabulary used correctly",
                 "Excellent diagrams; precise vocabulary; polished, engaging communication"),
            ],
        },
        "summary_table_headers": [
            "Lesson # and Title",
            "What did I observe or investigate?",
            "What did I learn?",
            "How does this help explain the diamond/graphite phenomenon?",
            "DQB and Model Update",
        ],
        "summary_table_rows": [
            (
                "Lesson 1: Phenomenon Launch and Atomic Stability",
                "Observed diamond (hard, transparent) and graphite (soft, black) — both pure carbon but very different. "
                "Investigated atomic structure and electron arrangements.",
                "Atoms bond to achieve stable electron configurations. Carbon has 4 valence electrons and needs 4 more. "
                "The bonding pattern determines properties.",
                "Both are carbon, so the difference must come from how atoms are bonded/arranged, not from different atoms.",
                "DQB Started: Why are diamond and graphite so different? How do atoms stick together?\n"
                "Initial Model: Carbon atoms connecting — unclear how or why differently.",
            ),
        ] + [
            (f"Lesson {n}:", "", "", "", "DQB Updated:\nModel Revised:")
            for n in range(2, 13)
        ] + [
            (
                "Lesson 13: Final Explanation and Model",
                "",
                "",
                "",
                "DQB Completed: Answered driving question with evidence from all lessons.\n"
                "Final Model: Comprehensive model showing how atomic bonding determines substance properties.",
            ),
        ],
        "summary_instructions": (
            "Complete one row after each lesson. Be specific and use evidence from investigations. "
            "Track your Driving Question Board (DQB) — note new questions and when questions get answered. "
            "Update your models progressively as new evidence changes your thinking."
        ),
    },

    "mathematics": {
        "subject":    "Mathematics",
        "grade":      "Grade 10",
        "strand":     "Strand 1.0: Numbers and Algebra",
        "substrand":  "Sub-Strand 1.3: Quadratic Expressions and Equations",
        "lessons":    7,
        "driving_question": "How can we use quadratic equations to model, solve, and make sense of real-life problems in our communities?",
        "phenomenon": (
            "A harambee group plans to raise Ksh 12,000. Members share the cost equally, but 3 members fail to show up — "
            "so the remaining members each pay Ksh 200 more. How many people were originally in the group?"
        ),
        "substrand_overview_rows": [
            ("Subject",           "Mathematics"),
            ("Grade",             "Grade 10"),
            ("Strand",            "Strand 1.0: Numbers and Algebra"),
            ("Sub-Strand",        "Sub-Strand 1.3: Quadratic Expressions and Equations"),
            ("Number of Lessons", "7"),
            ("Number of Periods", "14"),
            ("Anchoring Phenomenon",
             "A harambee group plans to raise Ksh 12,000. Members share the cost equally, but 3 members fail to show up — "
             "so the remaining members each pay Ksh 200 more. How many people were originally in the group?"),
            ("Driving Question",
             "How can we use quadratic equations to model, solve, and make sense of real-life problems in our communities?"),
            ("Sub-Strand SLOs: Knowledge",
             "Define and identify quadratic expressions; state and derive the three quadratic identities; "
             "explain factorisation methods; describe the zero product property; "
             "form quadratic equations from real-world contexts."),
            ("Sub-Strand SLOs: Skills",
             "Expand and factorise quadratic expressions; solve quadratic equations by factorisation; "
             "interpret solutions in context; model real-life problems with quadratic equations."),
            ("Sub-Strand SLOs: Attitudes & Values",
             "Appreciate mathematics as a tool for solving real community problems; "
             "develop persistence and systematic problem-solving habits."),
            ("Assessment",        "Formative: classwork, summary table, problem sets.\nSummative: Final Explanation document."),
            ("Core Values",       "Curiosity, perseverance, community connection"),
            ("Resources",         "Graph paper, area model tiles, calculators"),
            ("Notes",             ""),
        ],
        "final_explanation_sections": [
            (
                "Section 1: What is a Quadratic Expression and How Do We Form One?",
                "What is the standard form ax² + bx + c and what do a, b, c represent?\n"
                "Give three examples of quadratic expressions from real-life Kenyan contexts "
                "(e.g. shamba area, harambee contributions, matatu revenue).\n"
                "Explain how the harambee problem leads to a quadratic relationship.",
            ),
            (
                "Section 2: What Are the Three Quadratic Identities and How Are They Derived from Area?",
                "State and prove all three identities using area diagrams:\n"
                "  (a + b)² = a² + 2ab + b²\n"
                "  (a - b)² = a² - 2ab + b²\n"
                "  (a + b)(a - b) = a² - b²\n"
                "Use a numerical example for each identity (e.g. calculate 103², 97², and 103 × 97).",
            ),
            (
                "Section 3: How Do We Factorise Quadratic Expressions?",
                "Explain the method for factorising when a = 1 (find two numbers that multiply to c and add to b).\n"
                "Explain the splitting method for factorising when a ≠ 1.\n"
                "Apply both methods with worked examples.\n"
                "Identify and factorise perfect square trinomials and differences of two squares.",
            ),
            (
                "Section 4: How Do We Form and Solve a Quadratic Equation?",
                "State the four steps to solve a quadratic equation by factorisation.\n"
                "Solve the harambee textbook fund problem completely, showing all steps:\n"
                "  — define variable, form equation, simplify to standard form, factorise, "
                "apply zero product property, interpret, verify.\n"
                "Explain why one solution is rejected and what the answer means in context.",
            ),
            (
                "Section 5: How Do Quadratic Equations Help Us Solve Real-Life Problems?",
                "Solve at least two of the following problems, showing all working:\n"
                "  — Shamba area problem (farmer with 100m fencing)\n"
                "  — Classroom foundation dimensions\n"
                "  — Matatu fare optimization\n"
                "  — Pythagorean theorem application\n"
                "For each: define variable, form equation, solve, interpret solution, verify answer.",
            ),
        ],
        "final_explanation_rubric": {
            "headers": ["Criterion", "Below Expectation", "Approaches Expectation", "Meets Expectation", "Exceeds Expectation"],
            "rows": [
                ("1. Understanding Quadratic Concepts",
                 "Cannot identify quadratic expressions; explanations unclear or with major misconceptions",
                 "Identifies quadratics; states identities but struggles to explain derivations",
                 "Solid understanding; explains standard form, derives identities from area, describes zero product property",
                 "Deep understanding; uses multiple representations; makes connections across concepts"),
                ("2. Factorisation Skills",
                 "Cannot reliably factorise; attempts lack clear method; frequent errors",
                 "Factorises simple (a=1) cases with some success; struggles with a≠1",
                 "Factorises most expressions correctly; handles a=1 and a≠1; recognizes some special cases",
                 "Factorises all types accurately and efficiently; explains strategy; recognizes patterns; checks by expanding"),
                ("3. Problem-Solving and Equation Solving",
                 "Cannot set up equations from word problems; misapplies zero product property",
                 "Solves simple equations with guidance; struggles to set up from word problems",
                 "Solves equations correctly; defines variables; interprets solutions; shows steps",
                 "Excellent equation solving with clear variable definition, all steps shown, context interpretation, and verification"),
                ("4. Real-World Application and Communication",
                 "Does not connect maths to real-world contexts; communication unclear; no units",
                 "Some connections but superficial; communication unclear in places; inconsistent notation",
                 "Connects equations to real-world contexts; communicates clearly; uses correct notation and units",
                 "Strong connections with reflection on meaning; polished communication; organized presentation"),
            ],
        },
        "summary_table_headers": [
            "Lesson # and Title",
            "What did I investigate or work on?",
            "What did I learn?",
            "How does this help solve the harambee problem?",
            "DQB and Model Update",
        ],
        "summary_table_rows": [
            (
                "Lesson 1: Introduction to Quadratic Expressions",
                "Exploring patterns in area models; recognizing expressions with squared terms; sorting algebraic expressions.",
                "A quadratic expression contains a term with a variable squared (x²) written as ax² + bx + c. "
                "Quadratics model situations involving area, growth, and non-linear relationships.",
                "The harambee problem involves a relationship between contributions and total amount. "
                "Recognizing this as a quadratic situation is the first step.",
                "DQB Started: Posted harambee problem and initial questions.\n"
                "Model: Identified variables — let x = original number of members.",
            ),
            (
                "Lesson 2: Expanding Quadratic Expressions",
                "Practicing the distributive property; expanding products like (x + 3)(x + 5) using area models.",
                "Expanding means multiplying out brackets to write a quadratic in standard form. "
                "Used FOIL and area diagrams.",
                "If I set up an equation for the harambee problem, I may need to expand brackets to simplify it.",
                "DQB Updated: Added 'How do we expand quadratic expressions?'\n"
                "Model: Practiced expanding expressions to prepare for equation setup.",
            ),
            (
                "Lesson 3: Factorising Quadratic Expressions",
                "Breaking down quadratic expressions into products of binomials; finding factor pairs; using the ac method.",
                "Factorising is the reverse of expanding. Find two numbers that multiply to give ac and add to give b, "
                "then rewrite and group. Factorising helps solve equations.",
                "Once I form a quadratic equation from the harambee problem, factorising will allow me to find the possible values.",
                "DQB Updated: Added 'How do we factorise quadratics?'\n"
                "Model: Explored factorising sample equations.",
            ),
            (
                "Lesson 4: Solving Quadratic Equations by Factorising",
                "Setting equations equal to zero; factorising; applying the zero-product property.",
                "To solve: (1) rearrange to standard form, (2) factorise, (3) set each factor to zero, "
                "(4) solve for the variable. Must check solutions in context.",
                "This is the key method I'll use to solve the harambee equation.",
                "DQB Updated: Added 'How do we solve quadratic equations?'\n"
                "Model: Practiced solving and checking for extraneous solutions.",
            ),
            (
                "Lesson 5: Formation of Quadratic Equations from Real-World Contexts",
                "Translating word problems into algebraic equations; defining variables; writing equations from context.",
                "Forming equations requires: (1) define a variable, (2) express other quantities in terms of it, "
                "(3) use relationships to write an equation, (4) simplify to standard form.",
                "This lesson directly addresses the harambee problem. "
                "Equation: 12000/(x−3) − 12000/x = 200.",
                "DQB Updated: Added 'How do we translate real-world problems into equations?'\n"
                "Model Revised: Let x = original members. Set up the harambee equation.",
            ),
            (
                "Lesson 6: Solving and Interpreting Quadratic Equations in Context",
                "Solving equations formed in Lesson 5; interpreting solutions; rejecting non-viable answers.",
                "Not all mathematical solutions make sense in real life. Must check against context and reject "
                "impossible values (negative people, fractional members).",
                "After solving the harambee equation, found x = 15 or x = −12. Rejected x = −12.",
                "DQB Updated: Added 'How do we interpret and validate solutions?'\n"
                "Model Revised: Solved harambee equation — original number = 15 members.",
            ),
            (
                "Lesson 7: Reflection and Application",
                "Reviewing entire process from problem to solution; presenting the harambee solution; "
                "exploring extensions and new applications.",
                "Quadratic equations are powerful tools for modelling real-world situations. "
                "The process — define, model, solve, interpret — applies across many contexts.",
                "Solved the harambee problem: 15 original members, each paying Ksh 800. "
                "After 3 left, 12 members each paid Ksh 1,000. Difference = 200. ✓",
                "DQB Completed: Answered driving question with full solution.\n"
                "Final Model: Verified 12,000/15 = 800, 12,000/12 = 1,000, difference = 200 ✓",
            ),
        ],
        "summary_instructions": (
            "Complete one row after each lesson. Be specific in your reflections. "
            "Column 2: describe the main activity or concept explored. "
            "Column 3: summarize key mathematical ideas in your own words. "
            "Column 4: explain how this lesson helps understand or solve the harambee problem. "
            "Column 5: note progress on your Driving Question Board or mathematical model."
        ),
    },

    "physics": {
        "subject":    "Physics",
        "grade":      "Grade 10",
        "strand":     "Strand 1.0: Mechanics and Thermal Physics",
        "substrand":  "Sub-Strand 1.4: Temperature and Thermal Expansion",
        "lessons":    6,
        "driving_question": "Why do materials change size when temperature changes — and how do engineers use this to keep us safe?",
        "phenomenon": (
            "A tightly sealed metal sufuria lid won't budge — but after running hot water over it for 10 seconds, it opens easily. "
            "Also: a glass bottle full of water placed in a freezer cracks overnight."
        ),
        "substrand_overview_rows": [
            ("Subject",           "Physics"),
            ("Grade",             "Grade 10"),
            ("Strand",            "Strand 1.0: Mechanics and Thermal Physics"),
            ("Sub-Strand",        "Sub-Strand 1.4: Temperature and Thermal Expansion"),
            ("Number of Lessons", "6"),
            ("Number of Periods", "12"),
            ("Anchoring Phenomena",
             "1. A tightly sealed metal sufuria lid won't budge — but after running hot water over it for 10 seconds, it opens easily.\n"
             "2. A glass bottle full of water placed in a freezer cracks overnight."),
            ("Driving Question",
             "Why do materials change size when temperature changes — and how do engineers use this to keep us safe?"),
            ("Sub-Strand SLOs: Knowledge",
             "Define temperature and thermal energy; describe temperature scales and conversion; "
             "explain thermal expansion in solids, liquids, and gases; describe anomalous expansion of water; "
             "explain engineering applications of thermal expansion."),
            ("Sub-Strand SLOs: Skills",
             "Measure temperature using different thermometers; calculate linear expansion using ΔL = α × L₀ × ΔT; "
             "apply thermal expansion principles to explain real phenomena; "
             "analyze engineering solutions involving thermal expansion."),
            ("Sub-Strand SLOs: Attitudes & Values",
             "Appreciate the connection between particle-level behavior and everyday phenomena; "
             "recognize how physics knowledge enables engineers to design safer structures."),
            ("Assessment",        "Formative: observation, particle diagrams, calculations, summary table.\nSummative: Final Explanation document."),
            ("Core Values",       "Curiosity, safety awareness, connection to Kenyan context"),
            ("Resources",         "Thermometers, metal ball-and-ring, bimetallic strip, materials samples"),
            ("Notes",             ""),
        ],
        "final_explanation_sections": [
            (
                "Section 1: What is Temperature and How is it Measured?",
                "What is temperature at the particle level (how does it relate to kinetic energy)?\n"
                "What are the Celsius and Kelvin scales and how do we convert between them (K = °C + 273)?\n"
                "What types of thermometers exist and how does each one work?\n"
                "Which thermometer would be best for measuring the hot water used on the sufuria lid? Why?",
            ),
            (
                "Section 2: What Happens to Particles When Temperature Changes?",
                "How do particles behave differently in solids, liquids, and gases?\n"
                "What happens to particle motion when temperature increases?\n"
                "How does increased particle motion lead to expansion?\n"
                "Do all states of matter expand equally? Why or why not?\n"
                "Connect to phenomenon: What is happening to the particles in the metal lid and glass bottle?",
            ),
            (
                "Section 3: How Do We Calculate Thermal Expansion?",
                "What is linear expansivity (α) and what are its units?\n"
                "Apply the formula ΔL = α × L₀ × ΔT with a fully worked example (show all 5 steps: "
                "identify given values, identify unknown, write formula, substitute with units, calculate).\n"
                "Choose ONE: (A) A 50 m steel railway rail at 20°C rises to 45°C (α = 12 × 10⁻⁶ °C⁻¹). "
                "OR (B) An aluminum sufuria lid, diameter 20 cm, heats from 25°C to 95°C (α = 24 × 10⁻⁶ °C⁻¹).\n"
                "Connect your calculation to the sufuria lid phenomenon.",
            ),
            (
                "Section 4: Why Does Water Behave Unusually When It Freezes?",
                "How does water behave differently from most substances when it freezes (anomalous expansion)?\n"
                "At what temperature is water most dense? What happens between 4°C and 0°C?\n"
                "Explain using hydrogen bonding and the hexagonal ice crystal structure why water expands by ~9% on freezing.\n"
                "Explain step-by-step why the glass bottle cracked: what happened from room temperature to fully frozen?",
            ),
            (
                "Section 5: How Do Engineers Use Thermal Expansion to Keep Us Safe?",
                "What problems does thermal expansion cause in structures (railway tracks, bridges, roads, pipelines, power lines)?\n"
                "Explain with diagrams how expansion joints work and where they are used.\n"
                "Explain how bimetallic strips work and name three applications (thermostat, fire alarm, circuit breaker).\n"
                "Give at least three specific Kenya examples (e.g. Thika Superhighway, SGR railway, mabati roofing, JKIA runway).\n"
                "Connect to phenomenon: How does this knowledge prevent problems like the cracked bottle?",
            ),
        ],
        "final_explanation_rubric": {
            "headers": ["Criterion", "Beginning (1)", "Developing (2)", "Proficient (3)", "Advanced (4)"],
            "rows": [
                ("1. Phenomenon Connection",
                 "Rarely refers to anchoring phenomena; explanation disconnected from observation",
                 "Mentions phenomena but connections superficial",
                 "Regularly connects concepts to phenomena; explanation grounded in observation",
                 "Seamlessly integrates phenomena throughout; makes additional real-world connections"),
                ("2. Scientific Accuracy & Vocabulary",
                 "Multiple scientific errors; misuses key terms",
                 "Some errors; mostly accurate; some terms used incorrectly",
                 "Scientifically accurate; correct use of terminology throughout",
                 "Highly accurate and precise; sophisticated scientific language; nuanced understanding"),
                ("3. Particle-Level Reasoning",
                 "Little or no particle-level explanation; stays at macroscopic level",
                 "Attempts particle reasoning but gaps or errors; unclear link to macroscopic",
                 "Clearly explains particle behavior and links to macroscopic observations",
                 "Sophisticated particle reasoning; explicit microscopic-to-macroscopic connections"),
                ("4. Mathematical Application",
                 "Calculation missing, incomplete, or major errors; no method shown",
                 "Calculation present but errors in setup, substitution, or arithmetic",
                 "Calculation correct; all steps shown; appropriate units and significant figures",
                 "Calculation exemplary; method crystal clear; result interpreted in context"),
                ("5. Engineering Applications & Completeness",
                 "Fewer than 3 sections; few or no engineering examples",
                 "3–4 sections; some engineering mentions but explanations vague",
                 "All 5 sections; multiple engineering applications with Kenya examples",
                 "All 5 sections comprehensively; rich Kenya examples; design reasoning discussed"),
            ],
        },
        "summary_table_headers": [
            "Lesson # and Title",
            "What did I observe or investigate?",
            "What did I learn?",
            "How does this explain the sufuria lid and frozen bottle phenomenon?",
            "DQB and Model Update",
        ],
        "summary_table_rows": [
            (
                "Lesson 1: Introduction to Temperature and Heat",
                "Measured temperature of different objects using thermometers. "
                "Discussed what 'hot' and 'cold' mean and shared everyday experiences.",
                "Temperature measures the average kinetic energy of particles. "
                "Heat is energy transferred from hotter to cooler objects. They are related but different.",
                "This sets the foundation: when we run hot water over the sufuria lid, heat transfers to the lid "
                "and increases its temperature. But we don't yet know why this makes it easier to open.",
                "DQB Started: Why do things expand when heated? What happens to particles when temperature increases?\n"
                "Initial Model: Particles in a solid vibrate but stay in place.",
            ),
            (
                "Lesson 2: Particle Model of Matter and Temperature",
                "",
                "",
                "",
                "DQB Updated:\nModel Revised:",
            ),
            (
                "Lesson 3: Thermal Expansion in Solids",
                "Heated a metal ball until it no longer fit through a ring. Observed a bimetallic strip bend when heated. "
                "Measured change in length of a metal rod with a dial gauge.",
                "Thermal expansion: most solids expand when heated because particles vibrate more vigorously and need more space. "
                "Different metals have different coefficients of linear expansion (α). "
                "Engineers use expansion joints to accommodate this.",
                "Sufuria lid: the metal lid expands when heated with hot water, breaking the tight seal and making it easier to twist off. "
                "Frozen bottle: we know solids usually expand when heated — water may behave differently (anomaly to investigate).",
                "DQB Updated: Answered 'Why does the lid open when heated?' (differential expansion breaks the seal.)\n"
                "New question: Does water expand or contract when it freezes?\n"
                "Model Revised: Added arrows showing particles moving further apart when heated.",
            ),
            (
                "Lesson 4: Thermal Expansion in Liquids",
                "",
                "",
                "",
                "DQB Updated:\nModel Revised:",
            ),
            (
                "Lesson 5: Anomalous Expansion of Water",
                "",
                "",
                "",
                "DQB Updated:\nModel Revised:",
            ),
            (
                "Lesson 6: Engineering Applications and Design Challenge",
                "",
                "",
                "",
                "DQB Completed: Answered driving question with evidence-based explanation.\n"
                "Final Model: Complete model explaining thermal expansion in solids and liquids, "
                "including water's anomalous behavior, with engineering applications.",
            ),
        ],
        "summary_instructions": (
            "Complete one row after each lesson. "
            "Column 2: describe what you observed, measured, or investigated. "
            "Column 3: summarize key scientific concepts using precise vocabulary "
            "(e.g. thermal expansion, kinetic energy, linear expansivity). "
            "Column 4: connect your learning to the anchoring phenomena (sufuria lid or frozen bottle). "
            "Column 5: update your Driving Question Board and scientific model sketch."
        ),
    },
}

SOURCE_COMPLETE = {
    "chemistry":  SRC_DIR / "Chemistry_Chemical_Bonding_CBE_LessonSequence_COMPLETE.docx",
    "mathematics": SRC_DIR / "Mathematics_Quadratic_Equations_CBE_LessonSequence_COMPLETE.docx",
    "physics":    SRC_DIR / "Physics_Temperature_Thermal_Expansion_CBE_LessonSequence_COMPLETE.docx",
}

OUTPUT_FILES = {
    "chemistry": {
        "lesson_seq":    OUT_DIR / "Chemistry_10_SubStrand1.4_ChemicalBonding_CBE_LessonSequence.docx",
        "final_exp":     OUT_DIR / "Chemistry_10_SubStrand1.4_ChemicalBonding_FinalExplanation.docx",
        "summary_table": OUT_DIR / "Chemistry_10_SubStrand1.4_ChemicalBonding_SummaryTable.docx",
    },
    "mathematics": {
        "lesson_seq":    OUT_DIR / "Mathematics_10_SubStrand1.3_QuadraticEquations_CBE_LessonSequence.docx",
        "final_exp":     OUT_DIR / "Mathematics_10_SubStrand1.3_QuadraticEquations_FinalExplanation.docx",
        "summary_table": OUT_DIR / "Mathematics_10_SubStrand1.3_QuadraticEquations_SummaryTable.docx",
    },
    "physics": {
        "lesson_seq":    OUT_DIR / "Physics_10_SubStrand1.4_ThermalExpansion_CBE_LessonSequence.docx",
        "final_exp":     OUT_DIR / "Physics_10_SubStrand1.4_ThermalExpansion_FinalExplanation.docx",
        "summary_table": OUT_DIR / "Physics_10_SubStrand1.4_ThermalExpansion_SummaryTable.docx",
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# LOW-LEVEL DOCX HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def _shade(cell, hex_color: str):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    # Remove existing shd if any
    for old in tcPr.findall(qn("w:shd")):
        tcPr.remove(old)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)


def _cell_para(cell, text: str, bold=False, size_pt=10, color_hex=None,
               align=WD_ALIGN_PARAGRAPH.LEFT, italic=False):
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(2)
    _apply_run(p, text, bold=bold, size_pt=size_pt, color_hex=color_hex, italic=italic)
    return p


def _add_para(cell, text: str, bold=False, size_pt=10, color_hex=None,
              align=WD_ALIGN_PARAGRAPH.LEFT):
    p = cell.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after  = Pt(1)
    _apply_run(p, text, bold=bold, size_pt=size_pt, color_hex=color_hex)
    return p


def _apply_run(para, text: str, bold=False, size_pt=10, color_hex=None, italic=False):
    if not text:
        return
    run = para.add_run(text)
    run.font.name  = FONT
    run.font.size  = Pt(size_pt)
    run.font.bold  = bold
    run.font.italic = italic
    if color_hex:
        run.font.color.rgb = RGBColor(
            int(color_hex[0:2], 16),
            int(color_hex[2:4], 16),
            int(color_hex[4:6], 16),
        )
    else:
        run.font.color.rgb = RGBColor(0x00, 0x00, 0x00)


def _white_run(para, text, bold=False, size_pt=10):
    _apply_run(para, text, bold=bold, size_pt=size_pt, color_hex=C_WHITE)


def _merge_row(table, row_idx):
    """Merge all cells in a row."""
    row = table.rows[row_idx]
    if len(row.cells) < 2:
        return row.cells[0]
    a = row.cells[0]
    for c in row.cells[1:]:
        a.merge(c)
    return a


def _col_widths(table, widths_inches):
    """Set column widths. widths_inches is a list of floats."""
    tbl = table._tbl
    tblGrid = tbl.find(qn("w:tblGrid"))
    if tblGrid is None:
        tblGrid = OxmlElement("w:tblGrid")
        tbl.insert(0, tblGrid)
    # Clear existing gridCols
    for gc in tblGrid.findall(qn("w:gridCol")):
        tblGrid.remove(gc)
    for w in widths_inches:
        gc = OxmlElement("w:gridCol")
        gc.set(qn("w:w"), str(int(w * 1440)))
        tblGrid.append(gc)
    # Set each cell width
    for row in table.rows:
        cells = row.cells
        for i, cell in enumerate(cells):
            if i < len(widths_inches):
                tc = cell._tc
                tcPr = tc.get_or_add_tcPr()
                tcW = tcPr.find(qn("w:tcW"))
                if tcW is None:
                    tcW = OxmlElement("w:tcW")
                    tcPr.append(tcW)
                tcW.set(qn("w:w"), str(int(widths_inches[i] * 1440)))
                tcW.set(qn("w:type"), "dxa")


def _set_page_landscape(doc):
    """Set US Letter Landscape, 0.75\" margins."""
    sec = doc.sections[0]
    sec.page_width    = Inches(11.0)
    sec.page_height   = Inches(8.5)
    sec.left_margin   = Inches(0.75)
    sec.right_margin  = Inches(0.75)
    sec.top_margin    = Inches(0.75)
    sec.bottom_margin = Inches(0.75)


def _doc_title(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(4)
    _apply_run(p, text, bold=True, size_pt=14, color_hex=C_NAVY)


def _doc_subtitle(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(6)
    _apply_run(p, text, bold=False, size_pt=11, color_hex=C_TEAL)


def _tbl_no_spacing(doc):
    """Add a 0-height spacer paragraph to keep tables adjacent (no extra space)."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(0)
    pPr = p._p.get_or_add_pPr()
    spacing = OxmlElement("w:spacing")
    spacing.set(qn("w:before"), "0")
    spacing.set(qn("w:after"),  "0")
    spacing.set(qn("w:line"),   "240")
    spacing.set(qn("w:lineRule"), "auto")
    pPr.append(spacing)


def _set_tbl_border(table):
    """Apply thin black borders to all cells."""
    tbl = table._tbl
    tblPr = tbl.find(qn("w:tblPr"))
    if tblPr is None:
        tblPr = OxmlElement("w:tblPr")
        tbl.insert(0, tblPr)
    tblBorders = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        b = OxmlElement(f"w:{side}")
        b.set(qn("w:val"),   "single")
        b.set(qn("w:sz"),    "4")
        b.set(qn("w:space"), "0")
        b.set(qn("w:color"), "000000")
        tblBorders.append(b)
    # Remove existing tblBorders
    for old in tblPr.findall(qn("w:tblBorders")):
        tblPr.remove(old)
    tblPr.append(tblBorders)


def _new_table(doc, rows, cols):
    tbl = doc.add_table(rows=rows, cols=cols)
    tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
    _set_tbl_border(tbl)
    return tbl


# ═══════════════════════════════════════════════════════════════════════════════
# SOURCE DOCUMENT PARSING  (unchanged from working version)
# ═══════════════════════════════════════════════════════════════════════════════

def iter_block_items(doc):
    body = doc.element.body
    for child in body:
        tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        if tag == "p":
            yield "paragraph", DocxParagraph(child, doc)
        elif tag == "tbl":
            yield "table", DocxTable(child, doc)


def is_impl_table(table) -> bool:
    if len(table.columns) != 5:
        return False
    header = table.rows[0].cells[0].text.strip()
    return "Learner" in header or "Experience" in header


def _cell_text(cell) -> str:
    return "\n".join(p.text for p in cell.paragraphs if p.text.strip()).strip()


def parse_source(doc_path: Path) -> list[dict]:
    doc = Document(doc_path)
    lessons = []
    current: Optional[dict] = None
    section = None
    impl_tables_for_current = []
    buffer: list[str] = []

    LESSON_HEADING_RE = re.compile(r"^LESSON\s+(\d+)\s*[:–—]\s*(.*)", re.IGNORECASE)
    SECTION_RE        = re.compile(r"^([A-E])\.\s+(.*)")

    def flush_buffer():
        return "\n".join(buffer).strip()

    def save_section():
        nonlocal buffer, section
        if current is None or section is None:
            buffer = []
            return
        text = flush_buffer()
        if section == "A":
            parts = re.split(r"\n(?=Knowledge:|Skills:|Attitudes?:)", text, flags=re.IGNORECASE)
            for part in parts:
                part = part.strip()
                if re.match(r"Knowledge:", part, re.I):
                    current["slo_knowledge"] += "\n" + part[10:].strip()
                elif re.match(r"Skills:", part, re.I):
                    current["slo_skills"] += "\n" + part[7:].strip()
                elif re.match(r"Attitudes?:", part, re.I):
                    current["slo_attitudes"] += "\n" + re.split(r"Attitudes?:", part, flags=re.I, maxsplit=1)[-1].strip()
                elif part and not re.match(r"By the end", part, re.I):
                    current["slo_knowledge"] += "\n" + part
        elif section == "B":
            lines = text.split("\n")
            for i, ln in enumerate(lines):
                if re.match(r"Key Inquiry Question", ln, re.I):
                    inline = ln.split(":", 1)[1].strip() if ":" in ln else ""
                    if inline:
                        current["inquiry_question"] = inline
                    else:
                        next_ln = lines[i+1].strip() if i+1 < len(lines) else ""
                        if next_ln and not re.match(r"(Purpose|Safety|Materials|Duration|Supporting)", next_ln, re.I):
                            current["inquiry_question"] = next_ln
                elif re.match(r"Purpose in Storyline|Purpose:", ln, re.I):
                    purpose_lines = []
                    for j in range(i+1, len(lines)):
                        if re.match(r"(Safety|Materials|Duration|Supporting)", lines[j], re.I):
                            break
                        if lines[j].strip():
                            purpose_lines.append(lines[j].strip())
                    current["overview_purpose"] = " ".join(purpose_lines)
                elif re.match(r"Safety", ln, re.I):
                    safety_lines = []
                    for j in range(i+1, len(lines)):
                        if re.match(r"(Materials|Purpose|Key Inquiry)", lines[j], re.I):
                            break
                        if lines[j].strip():
                            safety_lines.append(lines[j].strip())
                    current["safety"] = " ".join(safety_lines)
                elif re.match(r"Materials?", ln, re.I) and ":" in ln:
                    mat_lines = []
                    for j in range(i+1, len(lines)):
                        if re.match(r"(Safety|Purpose|Duration|Key Inquiry)", lines[j], re.I):
                            break
                        if lines[j].strip():
                            mat_lines.append(lines[j].strip())
                    current["materials"] = " ".join(mat_lines)
        elif section == "D":
            lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
            current["reflections"] = lines
        elif section == "E":
            if text:
                current["summary_prompt"] = text
        buffer = []

    def save_impl_tables():
        if current is None:
            return
        for tbl in impl_tables_for_current:
            rows = []
            for row in tbl.rows[1:]:
                rows.append(tuple(_cell_text(c) for c in row.cells))
            if not current["period1_table"]:
                current["period1_table"] = rows
            else:
                current["period2_table"] = rows

    def new_lesson(number, title):
        nonlocal current, section, impl_tables_for_current
        if current is not None:
            save_section()
            save_impl_tables()
            lessons.append(current)
        impl_tables_for_current = []
        current = {
            "number": int(number),
            "title":  title.strip(),
            "inquiry_question": "",
            "slo_knowledge":    "",
            "slo_skills":       "",
            "slo_attitudes":    "",
            "overview_purpose": "",
            "materials":        "",
            "safety":           "",
            "period1_table":    [],
            "period2_table":    [],
            "period1_heading":  "Period 1 (40 minutes)",
            "period2_heading":  "Period 2 (40 minutes)",
            "reflections":      [],
            "summary_prompt":   "",
        }
        section = None

    for kind, obj in iter_block_items(doc):
        if kind == "paragraph":
            text = obj.text.strip()
            if not text:
                continue
            style_l = (obj.style.name if obj.style else "").lower()
            is_heading = "heading" in style_l

            m = LESSON_HEADING_RE.match(text)
            if m and is_heading:
                save_section()
                new_lesson(m.group(1), m.group(2))
                section = None
                buffer = []
                continue

            sm = SECTION_RE.match(text)
            if sm and current is not None and is_heading:
                save_section()
                section = sm.group(1).upper()
                buffer = []
                continue

            if "heading 4" in style_l and current is not None:
                if "PERIOD 1" in text.upper():
                    current["period1_heading"] = text
                elif "PERIOD 2" in text.upper():
                    current["period2_heading"] = text
                continue

            if current is not None and section is None and "Supporting Driving Question" in text:
                q = text.split(":", 1)[-1].strip() if ":" in text else ""
                if q:
                    current["inquiry_question"] = q
                continue

            if current is not None and section is not None:
                buffer.append(text)

        elif kind == "table":
            if is_impl_table(obj) and current is not None:
                save_section()
                impl_tables_for_current.append(obj)
                section = None
                buffer = []

    if current is not None:
        save_section()
        save_impl_tables()
        lessons.append(current)

    return lessons


# ═══════════════════════════════════════════════════════════════════════════════
# LESSON SEQUENCE BUILDER
# ═══════════════════════════════════════════════════════════════════════════════

def _build_table0_overview(doc, meta):
    """Sub-strand overview table (15r × 2c)."""
    rows_data = meta["substrand_overview_rows"]
    t = _new_table(doc, len(rows_data), 2)
    _col_widths(t, [2.0, 7.5])
    for ri, (label, value) in enumerate(rows_data):
        _shade(t.rows[ri].cells[0], C_LT_BLUE)
        _shade(t.rows[ri].cells[1], C_WHITE)
        _cell_para(t.rows[ri].cells[0], label, bold=True, size_pt=9)
        _cell_para(t.rows[ri].cells[1], value, size_pt=9)


def _build_table_A(doc, lesson):
    """Table A — SLOs + Overview (9r × 2c), total 9.5\"."""
    t = _new_table(doc, 9, 2)
    _col_widths(t, [2.0, 7.5])

    # R0: merged navy banner — LESSON N: Title
    c = _merge_row(t, 0)
    _shade(c, C_NAVY)
    _cell_para(c, f"LESSON {lesson['number']}: {lesson['title']}",
               bold=True, size_pt=11, color_hex=C_WHITE,
               align=WD_ALIGN_PARAGRAPH.LEFT)

    # R1: merged teal — A. Specific Learning Outcomes
    c = _merge_row(t, 1)
    _shade(c, C_TEAL)
    _cell_para(c, "A. Specific Learning Outcomes",
               bold=True, size_pt=10, color_hex=C_WHITE)

    # R2–R4: SLO rows
    slo_rows = [
        ("Knowledge:",        lesson["slo_knowledge"].strip()),
        ("Skills:",           lesson["slo_skills"].strip()),
        ("Attitudes & Values:", lesson["slo_attitudes"].strip()),
    ]
    for ri, (label, value) in enumerate(slo_rows, start=2):
        _shade(t.rows[ri].cells[0], C_LT_BLUE)
        _shade(t.rows[ri].cells[1], C_WHITE)
        _cell_para(t.rows[ri].cells[0], label, bold=True, size_pt=9)
        _cell_para(t.rows[ri].cells[1], value or "—", size_pt=9)

    # R5: merged teal — B. Lesson Overview
    c = _merge_row(t, 5)
    _shade(c, C_TEAL)
    _cell_para(c, "B. Lesson Overview", bold=True, size_pt=10, color_hex=C_WHITE)

    # R6: Key Inquiry Question (purple-lt label)
    _shade(t.rows[6].cells[0], C_PURPLE_LT)
    _shade(t.rows[6].cells[1], C_WHITE)
    _cell_para(t.rows[6].cells[0], "Key Inquiry Question:", bold=True, size_pt=9)
    _cell_para(t.rows[6].cells[1], lesson["inquiry_question"] or "—", size_pt=9)

    # R7: Purpose in Storyline (teal-lt label)
    _shade(t.rows[7].cells[0], C_TEAL_LT)
    _shade(t.rows[7].cells[1], C_WHITE)
    _cell_para(t.rows[7].cells[0], "Purpose in Storyline:", bold=True, size_pt=9)
    _cell_para(t.rows[7].cells[1], lesson["overview_purpose"] or "—", size_pt=9)

    # R8: Safety (orange-lt label)
    _shade(t.rows[8].cells[0], C_ORANGE_LT)
    _shade(t.rows[8].cells[1], C_WHITE)
    _cell_para(t.rows[8].cells[0], "Safety:", bold=True, size_pt=9)
    _cell_para(t.rows[8].cells[1], lesson["safety"] or "None noted.", size_pt=9)


def _build_table_B(doc, lesson):
    """Table B — Materials (2r × 1c)."""
    t = _new_table(doc, 2, 1)
    _col_widths(t, [9.5])

    _shade(t.rows[0].cells[0], C_TEAL)
    _cell_para(t.rows[0].cells[0], "Materials", bold=True, size_pt=10, color_hex=C_WHITE)

    _shade(t.rows[1].cells[0], C_WHITE)
    _cell_para(t.rows[1].cells[0], lesson["materials"] or "As directed by teacher.", size_pt=9)


def _build_table_C(doc, lesson, period_num: int, source_rows: list):
    """Table C — 6-col Implementation Framework (7r × 6c), total 9.5\"."""
    # Col widths: Phase=1.0, Learner Exp=2.5, Resource=1.0,
    #             Teacher Actions=2.0, Sensemaking=1.5, Assessment=1.5
    COL_W = [1.0, 2.5, 1.0, 2.0, 1.5, 1.5]
    COL_HEADER_FILLS = [C_NAVY, C_MED_BLUE, C_TEAL, C_MED_BLUE, C_TEAL, C_MED_BLUE]
    COL_HEADERS = ["Phase", "Learner Experience", "Resource",
                   "Teacher Actions", "Sensemaking Strategy", "Assessment Strategy"]

    t = _new_table(doc, 7, 6)
    _col_widths(t, COL_W)

    # R0: merged title — C. Lesson Implementation Framework — Period N (40 min)
    period_label = lesson.get(f"period{period_num}_heading", f"Period {period_num} (40 minutes)")
    c = _merge_row(t, 0)
    _shade(c, C_TEAL)
    _cell_para(c,
               f"C. Lesson Implementation Framework — {period_label}",
               bold=True, size_pt=10, color_hex=C_WHITE)

    # R1: col headers
    for ci, (cell, hdr, fill) in enumerate(zip(t.rows[1].cells, COL_HEADERS, COL_HEADER_FILLS)):
        _shade(cell, fill)
        _cell_para(cell, hdr, bold=True, size_pt=9, color_hex=C_WHITE,
                   align=WD_ALIGN_PARAGRAPH.CENTER)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    # R2–R6: 5 phase rows
    for ri in range(5):
        row = t.rows[ri + 2]
        phase_fill = PHASE_FILLS[ri]
        phase_name = PHASE_NAMES[ri]

        # Phase cell (col 0)
        _shade(row.cells[0], phase_fill)
        _cell_para(row.cells[0], phase_name, bold=True, size_pt=9,
                   align=WD_ALIGN_PARAGRAPH.CENTER)
        row.cells[0].vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        # Source data: (Learner Exp, Resource, Teacher Moves, Sensemaking, Assessment)
        if ri < len(source_rows):
            src = source_rows[ri]
            # src cols: [0]=Learner Exp, [1]=Resource, [2]=Teacher Moves,
            #           [3]=Sensemaking, [4]=Assessment
            content_vals = [
                src[0] if len(src) > 0 else "",
                src[1] if len(src) > 1 else "",
                src[2] if len(src) > 2 else "",
                src[3] if len(src) > 3 else "",
                src[4] if len(src) > 4 else "",
            ]
        else:
            content_vals = [""] * 5

        # Content cells col 1–5, alternating white/lt-gray
        content_fills = [C_WHITE, C_LT_GRAY, C_WHITE, C_LT_GRAY, C_WHITE]
        for ci, (cell, val, fill) in enumerate(zip(row.cells[1:], content_vals, content_fills)):
            _shade(cell, fill)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
            _cell_para(cell, val, size_pt=9)


def _build_table_D(doc, lesson):
    """Table D — Teacher Reflection (2r × 1c)."""
    t = _new_table(doc, 2, 1)
    _col_widths(t, [9.5])

    _shade(t.rows[0].cells[0], C_ORANGE)
    _cell_para(t.rows[0].cells[0], "D. Teacher Reflection",
               bold=True, size_pt=10, color_hex=C_WHITE)

    _shade(t.rows[1].cells[0], C_ORANGE_LT)
    refl_text = "\n".join(lesson["reflections"]) if lesson["reflections"] else \
        "Reflect on student engagement with the phase-based framework.\nWhich phase generated most discussion?"
    _cell_para(t.rows[1].cells[0], refl_text, size_pt=9)


def _build_table_E(doc):
    """Table E — Summary Table Prompt (4r × 2c)."""
    t = _new_table(doc, 4, 2)
    _col_widths(t, [2.5, 7.0])

    # R0: merged purple header
    c = _merge_row(t, 0)
    _shade(c, C_PURPLE)
    _cell_para(c, "E. Summary Table Prompt", bold=True, size_pt=10, color_hex=C_WHITE)

    prompts = [
        "What did I observe?",
        "What did I learn?",
        "How does this explain the phenomenon?",
    ]
    for ri, prompt in enumerate(prompts, start=1):
        _shade(t.rows[ri].cells[0], C_PURPLE_LT)
        _shade(t.rows[ri].cells[1], C_WHITE)
        _cell_para(t.rows[ri].cells[0], prompt, bold=True, size_pt=9)
        _cell_para(t.rows[ri].cells[1], "", size_pt=9)


def build_lesson_sequence_docx(subject_key: str, lessons: list[dict]) -> Document:
    meta = META[subject_key]
    doc  = Document()
    _set_page_landscape(doc)

    # Title + subtitle
    _doc_title(doc,
               f"{meta['subject']} | {meta['grade']} | {meta['substrand']}")
    _doc_subtitle(doc,
                  f"CBE Lesson Sequence  ·  {meta['lessons']} Lessons  ·  "
                  f"{meta['lessons'] * 2} Periods")

    # Sub-strand overview table
    _build_table0_overview(doc, meta)

    for lesson in lessons:
        # Spacer paragraph between sub-strand table and first lesson,
        # or between lessons
        _tbl_no_spacing(doc)

        _build_table_A(doc, lesson)
        _build_table_B(doc, lesson)

        # Period 1
        _build_table_C(doc, lesson, 1, lesson["period1_table"])
        # Period 2
        _build_table_C(doc, lesson, 2, lesson["period2_table"])

        _build_table_D(doc, lesson)
        _build_table_E(doc)

    return doc


# ═══════════════════════════════════════════════════════════════════════════════
# FINAL EXPLANATION BUILDER
# ═══════════════════════════════════════════════════════════════════════════════

def build_final_explanation_docx(subject_key: str) -> Document:
    meta = META[subject_key]
    doc  = Document()
    _set_page_landscape(doc)

    title_text = f"{meta['subject']} | {meta['grade']} | {meta['substrand']}"
    _doc_title(doc, title_text)
    _doc_subtitle(doc, "Final Explanation Document")

    # ── Table 0: Header block (5r × 2c) ──────────────────────────────────────
    t0 = _new_table(doc, 5, 2)
    _col_widths(t0, [2.5, 7.0])

    c = _merge_row(t0, 0)
    _shade(c, C_NAVY)
    _cell_para(c, title_text, bold=True, size_pt=11, color_hex=C_WHITE)

    c = _merge_row(t0, 1)
    _shade(c, C_TEAL)
    _cell_para(c, "Final Explanation Document", bold=True, size_pt=10, color_hex=C_WHITE)

    for ri, label in enumerate(["Student Name:", "Class:", "Date:"], start=2):
        _shade(t0.rows[ri].cells[0], C_LT_BLUE)
        _shade(t0.rows[ri].cells[1], C_WHITE)
        _cell_para(t0.rows[ri].cells[0], label, bold=True, size_pt=9)
        _cell_para(t0.rows[ri].cells[1], "", size_pt=9)

    _tbl_no_spacing(doc)

    # ── Table 1: Instructions (2r × 1c) ─────────────────────────────────────
    t1 = _new_table(doc, 2, 1)
    _col_widths(t1, [9.5])

    _shade(t1.rows[0].cells[0], C_TEAL)
    _cell_para(t1.rows[0].cells[0], "Instructions", bold=True, size_pt=10, color_hex=C_WHITE)

    instructions = (
        f"This Final Explanation is your opportunity to demonstrate deep understanding of "
        f"{meta['substrand']}. "
        f"Driving Question: {meta['driving_question']}\n\n"
        "Address all sections below using evidence from investigations, discussions, and models "
        "from across this unit. Use scientific vocabulary accurately. Include labeled diagrams "
        "where appropriate. Show all calculations. Connect your explanations back to the "
        "anchoring phenomenon throughout."
    )
    _shade(t1.rows[1].cells[0], C_WHITE)
    _cell_para(t1.rows[1].cells[0], instructions, size_pt=9)

    _tbl_no_spacing(doc)

    # ── Tables 2–6: One per section (3r × 1c each) ──────────────────────────
    sections = meta["final_explanation_sections"]
    for i, (section_title, prompts) in enumerate(sections):
        t = _new_table(doc, 3, 1)
        _col_widths(t, [9.5])

        _shade(t.rows[0].cells[0], C_MED_BLUE)
        _cell_para(t.rows[0].cells[0], section_title, bold=True, size_pt=10, color_hex=C_WHITE)

        _shade(t.rows[1].cells[0], C_LT_BLUE)
        _cell_para(t.rows[1].cells[0], prompts, size_pt=9)

        _shade(t.rows[2].cells[0], C_WHITE)
        cell = t.rows[2].cells[0]
        cell.paragraphs[0].paragraph_format.space_before = Pt(2)
        cell.paragraphs[0].paragraph_format.space_after  = Pt(60)
        _apply_run(cell.paragraphs[0], "[Write your response here]",
                   italic=True, size_pt=9, color_hex="999999")

        if i < len(sections) - 1:
            _tbl_no_spacing(doc)

    _tbl_no_spacing(doc)

    # ── Table 7: Rubric (rows = 1 header + len(rubric_rows), 5c) ────────────
    rubric = meta["final_explanation_rubric"]
    rub_rows = rubric["rows"]
    total_rows = 1 + len(rub_rows)
    t7 = _new_table(doc, total_rows, len(rubric["headers"]))
    _col_widths(t7, [2.0, 1.875, 1.875, 1.875, 1.875])

    # R0: merged navy header
    c = _merge_row(t7, 0)
    _shade(c, C_NAVY)
    _cell_para(c, "Assessment Rubric", bold=True, size_pt=11, color_hex=C_WHITE,
               align=WD_ALIGN_PARAGRAPH.CENTER)

    # R1 would be col headers — but we merged R0. Insert a proper header row.
    # Actually we need header row at R0 merged, then col headers at R1.
    # Let's rebuild: 2 + len(rub_rows) rows.
    t7 = _new_table(doc, 2 + len(rub_rows), len(rubric["headers"]))
    _col_widths(t7, [2.0, 1.875, 1.875, 1.875, 1.875])

    c = _merge_row(t7, 0)
    _shade(c, C_NAVY)
    _cell_para(c, "Assessment Rubric", bold=True, size_pt=11, color_hex=C_WHITE,
               align=WD_ALIGN_PARAGRAPH.CENTER)

    # Col header row
    hdr_fills = [C_MED_BLUE, C_TEAL, C_MED_BLUE, C_TEAL, C_MED_BLUE]
    # Trim to actual number of cols
    hdr_fills = hdr_fills[:len(rubric["headers"])]
    for ci, (cell, hdr, fill) in enumerate(zip(t7.rows[1].cells, rubric["headers"], hdr_fills)):
        _shade(cell, fill)
        _cell_para(cell, hdr, bold=True, size_pt=9, color_hex=C_WHITE,
                   align=WD_ALIGN_PARAGRAPH.CENTER)

    # Data rows
    for ri, row_data in enumerate(rub_rows):
        row = t7.rows[ri + 2]
        _shade(row.cells[0], C_LT_BLUE)
        _cell_para(row.cells[0], row_data[0], bold=True, size_pt=9)
        alt = [C_WHITE, C_LT_GRAY, C_WHITE, C_LT_GRAY]
        for ci, (cell, val, fill) in enumerate(zip(row.cells[1:], row_data[1:], alt)):
            _shade(cell, fill)
            _cell_para(cell, val, size_pt=9)

    return doc


# ═══════════════════════════════════════════════════════════════════════════════
# SUMMARY TABLE BUILDER
# ═══════════════════════════════════════════════════════════════════════════════

def build_summary_table_docx(subject_key: str) -> Document:
    meta = META[subject_key]
    doc  = Document()
    _set_page_landscape(doc)

    title_text = f"{meta['subject']} | {meta['grade']} | {meta['substrand']}"
    _doc_title(doc, title_text)
    _doc_subtitle(doc, "Summary Table")

    # ── Table 0: Header block (4r × 2c) ──────────────────────────────────────
    t0 = _new_table(doc, 4, 2)
    _col_widths(t0, [2.5, 7.0])

    c = _merge_row(t0, 0)
    _shade(c, C_NAVY)
    _cell_para(c, title_text, bold=True, size_pt=11, color_hex=C_WHITE)

    c = _merge_row(t0, 1)
    _shade(c, C_TEAL)
    _cell_para(c, "Summary Table", bold=True, size_pt=10, color_hex=C_WHITE)

    _shade(t0.rows[2].cells[0], C_LT_BLUE)
    _shade(t0.rows[2].cells[1], C_WHITE)
    _cell_para(t0.rows[2].cells[0], "Sub-Strand:", bold=True, size_pt=9)
    _cell_para(t0.rows[2].cells[1], meta["substrand"], size_pt=9)

    _shade(t0.rows[3].cells[0], C_LT_BLUE)
    _shade(t0.rows[3].cells[1], C_WHITE)
    _cell_para(t0.rows[3].cells[0], "Driving Question:", bold=True, size_pt=9)
    _cell_para(t0.rows[3].cells[1], meta["driving_question"], size_pt=9)

    _tbl_no_spacing(doc)

    # ── Table 1: Instructions (2r × 1c) ─────────────────────────────────────
    t1 = _new_table(doc, 2, 1)
    _col_widths(t1, [9.5])

    _shade(t1.rows[0].cells[0], C_TEAL)
    _cell_para(t1.rows[0].cells[0], "Instructions", bold=True, size_pt=10, color_hex=C_WHITE)

    _shade(t1.rows[1].cells[0], C_WHITE)
    _cell_para(t1.rows[1].cells[0], meta["summary_instructions"], size_pt=9)

    _tbl_no_spacing(doc)

    # ── Table 2: Main summary table (N+1 rows × 5c) ──────────────────────────
    # Col widths: 0.833 | 2.167 | 2.167 | 2.167 | 2.167 (total 9.501")
    COL_W = [0.833, 2.167, 2.167, 2.167, 2.167]
    HDR_FILLS = [C_NAVY, C_MED_BLUE, C_TEAL, C_MED_BLUE, C_PURPLE]

    data_rows = meta["summary_table_rows"]
    t2 = _new_table(doc, 1 + len(data_rows), 5)
    _col_widths(t2, COL_W)

    # Header row
    headers = meta["summary_table_headers"]
    for ci, (cell, hdr, fill) in enumerate(zip(t2.rows[0].cells, headers, HDR_FILLS)):
        _shade(cell, fill)
        _cell_para(cell, hdr, bold=True, size_pt=9, color_hex=C_WHITE,
                   align=WD_ALIGN_PARAGRAPH.CENTER)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    # Data rows
    for ri, row_data in enumerate(data_rows):
        row = t2.rows[ri + 1]
        alt_fill = C_WHITE if ri % 2 == 0 else C_LT_GRAY

        # Lesson # col — always lt blue
        _shade(row.cells[0], C_LT_BLUE)
        _cell_para(row.cells[0], row_data[0] if row_data else "", bold=True, size_pt=9)
        row.cells[0].vertical_alignment = WD_ALIGN_VERTICAL.TOP

        # Middle cols
        for ci in range(1, 4):
            _shade(row.cells[ci], alt_fill)
            _cell_para(row.cells[ci], row_data[ci] if len(row_data) > ci else "", size_pt=9)
            row.cells[ci].vertical_alignment = WD_ALIGN_VERTICAL.TOP

        # DQB col — always purple lt
        _shade(row.cells[4], C_PURPLE_LT)
        _cell_para(row.cells[4], row_data[4] if len(row_data) > 4 else "", size_pt=9)
        row.cells[4].vertical_alignment = WD_ALIGN_VERTICAL.TOP

    return doc


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    for key in ("chemistry", "mathematics", "physics"):
        meta = META[key]
        print(f"\n{'='*60}")
        print(f"Processing: {meta['subject']} — {meta['substrand']}")

        # ── Parse source ──────────────────────────────────────────────────────
        src_path = SOURCE_COMPLETE[key]
        lessons  = parse_source(src_path)
        print(f"  Parsed {len(lessons)} lessons (expected {meta['lessons']})")
        if len(lessons) != meta["lessons"]:
            print(f"  WARNING: lesson count mismatch!")

        for lesson in lessons:
            p1 = len(lesson["period1_table"])
            p2 = len(lesson["period2_table"])
            print(f"    Lesson {lesson['number']:2d}: {lesson['title'][:50]!r}"
                  f"  P1={p1} P2={p2}")

        # Fill missing inquiry questions
        for lesson in lessons:
            if not lesson["inquiry_question"]:
                lesson["inquiry_question"] = lesson["title"]

        # ── Build & save 3 documents ─────────────────────────────────────────
        out = OUTPUT_FILES[key]

        doc_ls = build_lesson_sequence_docx(key, lessons)
        doc_ls.save(str(out["lesson_seq"]))
        print(f"  ✓ Saved: {out['lesson_seq'].name}")

        doc_fe = build_final_explanation_docx(key)
        doc_fe.save(str(out["final_exp"]))
        print(f"  ✓ Saved: {out['final_exp'].name}")

        doc_st = build_summary_table_docx(key)
        doc_st.save(str(out["summary_table"]))
        print(f"  ✓ Saved: {out['summary_table'].name}")

    print(f"\n{'='*60}")
    print(f"Done. 9 files written to {OUT_DIR}/")


if __name__ == "__main__":
    main()
