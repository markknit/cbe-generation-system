#!/usr/bin/env python3
"""
reformat_may18.py — CBE Document Generator for May 18 Scheme of Work Templates

Generates 12 output files (3 per subject × 4 subjects) from source planning docs.
Generated/AI-suggested content is rendered in italic in all outputs.
Source content (from the Scheme of Work docs) is rendered in normal font.

Subjects:
  biology    → Biology 10 — Sub-Strand 2.2: Transport System in Plants (22 lessons)
  physics    → Physics 10 — Sub-Strand 1.5: Moments and Equilibrium (6 lessons)
  chemistry  → Chemistry 10 — Sub-Strand 1.5: The Periodicity (7 lessons)
  maths      → Mathematics 10 — Sub-Strand 2.1: Similarity and Enlargement (12 lessons)
"""

import sys
import re
from pathlib import Path

# ── Import shared builders from reformat_seavuria ─────────────────────────────
sys.path.insert(0, str(Path(__file__).parent))
import reformat_seavuria as _sv

# Re-export everything we need
_cell_para        = _sv._cell_para
_cell_para_lines  = _sv._cell_para_lines
_cell_para_auto   = _sv._cell_para_auto
_build_table_A    = _sv._build_table_A
_build_table_B    = _sv._build_table_B
_build_table_C_period = _sv._build_table_C_period
_build_table_D    = _sv._build_table_D
_build_table_E    = _sv._build_table_E
_build_table0_overview = _sv._build_table0_overview
_build_section_table   = _sv._build_section_table
_set_page_landscape    = _sv._set_page_landscape
_doc_title        = _sv._doc_title
_doc_subtitle     = _sv._doc_subtitle
_add_page_break   = _sv._add_page_break
_tbl_no_spacing   = _sv._tbl_no_spacing
_new_table        = _sv._new_table
_merge_row        = _sv._merge_row
_shade            = _sv._shade
_col_widths       = _sv._col_widths
_text_to_rich     = _sv._text_to_rich
_prose_to_bullets = _sv._prose_to_bullets
_enrich_content   = _sv._enrich_content
parse_framework_sections = _sv.parse_framework_sections
parse_doc_sections       = _sv.parse_doc_sections

# Color constants
C_NAVY     = _sv.C_NAVY
C_TEAL     = _sv.C_TEAL
C_MED_BLUE = _sv.C_MED_BLUE
C_PURPLE   = _sv.C_PURPLE
C_ORANGE   = _sv.C_ORANGE
C_LT_BLUE  = _sv.C_LT_BLUE
C_TEAL_LT  = _sv.C_TEAL_LT
C_GREEN_LT = _sv.C_GREEN_LT
C_PURPLE_LT = _sv.C_PURPLE_LT
C_ORANGE_LT = _sv.C_ORANGE_LT
C_LT_GRAY  = _sv.C_LT_GRAY
C_WHITE    = _sv.C_WHITE
C_MED_BLUE = _sv.C_MED_BLUE

from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent
SRC_DIR  = BASE_DIR / "data" / "raw" / "CBE_Templates_May_18"
OUT_DIR  = BASE_DIR / "data" / "outputs" / "May18_Reformatted"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SOURCE = {
    "biology":   SRC_DIR / "BIOLOGY TRANSPORT SYSTEM IN PLANT  SCHEME OF WORK  (1).docx",
    "physics":   SRC_DIR / "Grade 10 1.5 Moments and equilibrium (1).docx",
    "chemistry": SRC_DIR / "The periodicity.docx",
    "maths":     SRC_DIR / "maths _ Geometry and measurement;Similarity and enlargement.docx",
}

OUTPUTS = {
    "biology": {
        "lesson_seq":  OUT_DIR / "Biology_10_SubStrand2.2_TransportSystemInPlants_CBE_LessonSequence.docx",
        "final_exp":   OUT_DIR / "Biology_10_SubStrand2.2_TransportSystemInPlants_FinalExplanation.docx",
        "summary_tbl": OUT_DIR / "Biology_10_SubStrand2.2_TransportSystemInPlants_SummaryTable.docx",
    },
    "physics": {
        "lesson_seq":  OUT_DIR / "Physics_10_SubStrand1.5_MomentsEquilibrium_CBE_LessonSequence.docx",
        "final_exp":   OUT_DIR / "Physics_10_SubStrand1.5_MomentsEquilibrium_FinalExplanation.docx",
        "summary_tbl": OUT_DIR / "Physics_10_SubStrand1.5_MomentsEquilibrium_SummaryTable.docx",
    },
    "chemistry": {
        "lesson_seq":  OUT_DIR / "Chemistry_10_SubStrand1.5_Periodicity_CBE_LessonSequence.docx",
        "final_exp":   OUT_DIR / "Chemistry_10_SubStrand1.5_Periodicity_FinalExplanation.docx",
        "summary_tbl": OUT_DIR / "Chemistry_10_SubStrand1.5_Periodicity_SummaryTable.docx",
    },
    "maths": {
        "lesson_seq":  OUT_DIR / "Mathematics_10_SubStrand2.1_SimilarityEnlargement_CBE_LessonSequence.docx",
        "final_exp":   OUT_DIR / "Mathematics_10_SubStrand2.1_SimilarityEnlargement_FinalExplanation.docx",
        "summary_tbl": OUT_DIR / "Mathematics_10_SubStrand2.1_SimilarityEnlargement_SummaryTable.docx",
    },
}

# ── Helper: mark content as AI-generated (renders italic) ────────────────────

def _G(text: str) -> list:
    """Convert text to gen_* rich-content tuples (renders italic in output)."""
    return [("gen_" + k, v) for k, v in _text_to_rich(text)]


def _gc(cell, text: str, size_pt: int = 9):
    """Write AI-generated text into a cell (italic)."""
    _cell_para_lines(cell, _G(text), size_pt=size_pt)


# ── Phase row helper ──────────────────────────────────────────────────────────

def _pr(learner, resource, teacher, sensemaking, assessment):
    """5-tuple for one Table C phase row."""
    return (learner, resource, teacher, sensemaking, assessment)


# ═══════════════════════════════════════════════════════════════════════════════
# META — Biology
# ═══════════════════════════════════════════════════════════════════════════════

_BIO_SLO_K = (
    "a) Relate structures of the plant transport system to their functions in plants\n"
    "b) Illustrate the arrangement of vascular tissues in monocotyledonous and dicotyledonous plants\n"
    "c) Demonstrate the uptake of water and mineral salts from roots to leaves\n"
    "d) Demonstrate factors that affect the rate of transpiration in plants\n"
    "e) Describe the translocation of manufactured food in plants"
)
_BIO_SLO_S = (
    "- Conduct investigations on plant transport, transpiration and translocation\n"
    "- Draw and label diagrams of plant transport structures\n"
    "- Collect, record and interpret experimental data\n"
    "- Apply knowledge of transport to real farming challenges"
)
_BIO_SLO_A = (
    "- Appreciate the importance of plant transport systems to food security and farming\n"
    "- Show curiosity and care when handling living plant materials\n"
    "- Value teamwork and honest recording in investigations"
)

def _bio_lesson(num, title, inquiry, know, skills, attit, purpose, materials, safety, p1, p2=None):
    return {
        "number": num, "title": title,
        "inquiry_question": inquiry,
        "slo_knowledge": know, "slo_skills": skills, "slo_attitudes": attit,
        "overview_purpose": purpose,
        "materials": materials, "safety": safety,
        "period1_heading": "Period 1 (40 minutes)",
        "period1_table": p1,
        "period2_heading": "Period 2 (40 minutes)",
        "period2_table": p2 if p2 else [],
        "reflections": [],
    }

_BIO_LESSONS = [
    _bio_lesson(
        1, "Introduction to the Phenomenon",
        "Why do some crops like spinach wilt quickly on hot windy days while mango trees stay green?",  # SOURCE
        "- Recall that plants contain internal structures involved in water movement\n- Identify the unit driving question",
        "- Observe and record plant wilting; draw an initial model of water movement inside a plant",
        "- Show curiosity about how plants respond to their environment",
        "Launches the unit phenomenon. Students encounter wilting crops, generate questions, and produce initial models of water movement inside plants.",
        "Wilted spinach or sukuma wiki; fresh mango branch; Driving Question Board poster; blank A4 paper",
        "Handle live plant material with care; wash hands after touching soil.",
        [
            _pr("Observe wilted spinach alongside fresh mango branch; record observations",
                "Live plant samples or time-lapse video of wilting and recovery",
                "Show samples/video without explanation; ask 'What do you notice? What are you wondering?'",
                "Think–Pair–Share: individual → partner → whole-class share-out",
                "Exit ticket: list 2 observations and 1 question about wilting plants"),
            _pr("Draw 'what is happening inside the plant?' diagram showing roots, stem, leaves and water arrows",
                "Blank A4 paper; large class diagram for reference",
                "Prompt: 'Draw what you think is happening inside the plant when it wilts and when it recovers'",
                "Pair-share diagrams; identify what students agree and disagree on",
                "Collect initial model diagrams for formative reference"),
            _pr("Contribute questions to the class Driving Question Board",
                "Driving Question Board (poster or whiteboard section); sticky notes",
                "Facilitate DQB creation; group student questions by theme",
                "Model 'I notice … I wonder …' sentence stems",
                "Count and categorise student questions to inform lesson sequence"),
            _pr("Discuss: what do we already know about plant structure?",
                "Textbook diagrams or large poster of a whole plant",
                "Elicit prior knowledge; accept all ideas without correction at this stage",
                "Record prior knowledge on a KWL chart (Know–Want to know–Learned)",
                "Oral probe: 'Name one structure inside a plant and guess its job'"),
            _pr("Draw 'My Plant Model — Start of Unit': roots, stem, leaves, water movement arrows",
                "Model template or blank paper",
                "Explain that models will be updated each lesson as understanding grows",
                "Students share initial models with partners; note what is uncertain",
                "Collect models; note common misconceptions for future lessons"),
        ],
    ),
    _bio_lesson(
        2, "What Do Plants Need to Survive?",
        "What substances do plants need to survive, and how do they obtain them?",
        "- List the substances plants need: water, mineral salts, carbon dioxide, light\n- Explain why each substance is essential",
        "- Sort plant needs by category; link each need to a transport process",
        "- Appreciate that plants, like humans, have basic survival needs",
        "Establishes prior knowledge of plant needs and creates the link to why a transport system is necessary.",
        "Cards with plant needs written on them; sorting mats; textbook or chart",
        "No specific hazards.",
        [
            _pr("Brainstorm: what do plants need to survive? Record ideas individually then share",
                "Blank cards; markers for brainstorm",
                "Pose question; accept all responses; record on board without evaluation",
                "Think–Pair–Share; create class mind-map",
                "Quick class poll: thumbs up/down for each suggested need"),
            _pr("Sort plant needs into categories: from soil, from air, from sunlight",
                "Sorting cards and sorting mat",
                "Facilitate sorting activity; ask 'How does the plant get each one?'",
                "Group discussion; justify sorting decisions",
                "Exit ticket: 'Draw an arrow showing where water enters a plant'"),
            _pr("Link each need to a transport process: water via roots, minerals via roots, sugars via phloem",
                "Simple diagram of plant showing roots, stem, leaves",
                "Guided discussion: 'If plants need water at every cell, how does it travel from soil to leaf?'",
                "Connect to driving question: 'This is why plants have a transport system'",
                "Oral check: can students identify which structure transports water vs. food?"),
            _pr("Update Driving Question Board: add question 'How do plants get water from the soil?'",
                "Driving Question Board",
                "Guide students to connect plant needs to the phenomenon (wilting = lack of water)",
                "Re-read driving question together and discuss what we need to find out next",
                "Check that DQB links to upcoming lessons"),
            _pr("Update plant model: add arrows showing where water, minerals and CO₂ enter",
                "Initial model from Lesson 1",
                "Model how to add labels and arrows to an existing diagram",
                "Pair discussion: 'What did you change in your model?'",
                "Observe model updates; note which students include mineral salts vs. only water"),
        ],
    ),
    _bio_lesson(
        3, "Overview of Plant Transport System",
        "What are xylem and phloem, and what does each transport?",
        "- Name xylem and phloem as the two main transport vessels\n- State that xylem transports water and minerals upward; phloem transports sugars",
        "- Label xylem and phloem on a whole-plant diagram\n- Distinguish between the two vessels by function",
        "- Show interest in how microscopic structures enable a whole plant to function",
        "Introduces the two main transport vessels by name and function, providing a framework for the detailed lessons that follow.",
        "Large whole-plant diagram or poster; coloured pencils (blue for xylem, green for phloem)",
        "No specific hazards.",
        [
            _pr("Examine a large labelled diagram of a whole plant; identify xylem and phloem by colour",
                "Large poster or projected diagram of plant cross-section",
                "Introduce xylem and phloem as 'transport tubes'; avoid full structural detail at this stage",
                "Analogy: xylem = water pipes, phloem = sugar delivery system",
                "Oral check: 'Which vessel carries water? Which carries food?'"),
            _pr("Colour-code a blank plant diagram: blue for xylem pathway, green for phloem pathway",
                "Blank plant diagrams; blue and green pencils/pens",
                "Circulate; ensure students trace the correct continuous pathway",
                "Think-aloud: trace a water molecule from root hair to stomata",
                "Collect diagrams; check that pathways are correctly direction-labelled"),
            _pr("Discuss: why does a plant need two separate transport systems?",
                "Completed colour-coded diagrams",
                "Pose question; guide discussion without giving answer; accept hypotheses",
                "Connect to human circulatory system as an analogy (arteries/veins)",
                "Exit ticket: 'Give one reason why xylem and phloem must be separate'"),
            _pr("Update DQB: 'What is the difference between xylem and phloem?'",
                "Driving Question Board",
                "Add teacher-generated question if students have not raised it",
                "Revisit phenomenon: 'When spinach wilts, which vessel is most affected?'",
                "Students predict the answer; record predictions to revisit later"),
            _pr("Update plant model: label xylem and phloem in correct positions",
                "Running plant model diagram",
                "Emphasise: 'Your model should now show two distinct pathways'",
                "Compare Lesson 1 model vs Lesson 3 model; discuss what changed",
                "Note which students now include directionality (up vs. up and down)"),
        ],
    ),
    _bio_lesson(
        4, "Root Structure and Function",
        "How does the structure of root hair cells help plants absorb water and minerals?",
        "- Describe the structure of a root hair cell (large surface area, thin wall, vacuole)\n- Explain how root hairs are adapted for absorption (Obj a)",
        "- Observe real roots or a diagram; identify root hair zone\n- Draw and label a root hair cell",
        "- Appreciate the link between microscopic cell structure and whole-plant function",
        "Examines root structure in detail, establishing the site and mechanism of water entry — essential foundation for Lesson 13.",
        "Germinated bean seeds with visible roots; hand lens or microscope; root diagram",
        "Wash hands after handling soil or roots; handle seeds gently.",
        [
            _pr("Observe germinated bean roots with a hand lens; record observations of root structure",
                "Germinated bean seeds; hand lens; diagram of root tip and root hair zone",
                "Distribute seeds; guide observation: 'Look at the fuzzy zone near the tip — what do you see?'",
                "Think-aloud: 'Each fuzzy strand is a root hair cell — one single cell'",
                "Quick sketch of root with annotations"),
            _pr("Examine diagram of root hair cell; identify: cell wall, cell membrane, large vacuole, cytoplasm",
                "Labelled diagram of root hair cell",
                "Use guided labelling: display unlabelled diagram, students suggest labels",
                "Connect structure to function: 'Why is the vacuole large? Why is the wall thin?'",
                "Exit ticket: list 3 adaptations of root hair cells and their functions"),
            _pr("Calculate: if 1 cm of root has 100 root hairs, how many per metre? Discuss why this matters",
                "Calculators or mental maths",
                "Guide calculation; emphasise that large surface area increases absorption rate",
                "Real-world link: 'After rain, why do plants recover quickly?'",
                "Students explain in writing why root hairs increase absorption efficiency"),
            _pr("Update DQB: 'How does water get from the soil into the root?'",
                "Driving Question Board",
                "Connect today's learning to the phenomenon: wilting is loss of water from cells",
                "Foreshadow Lesson 13: 'We will see exactly how water crosses the root hair membrane'",
                "Students vote on the most important question still unanswered"),
            _pr("Update plant model: add root hair cells at the base of the root with arrows showing water entry",
                "Running plant model diagram",
                "Model how to zoom in on part of a diagram to show cellular detail",
                "Discuss: 'Your model is getting more accurate — what else do you need to show?'",
                "Compare with partner's model; share one improvement idea"),
        ],
    ),
    _bio_lesson(
        5, "Stem Structure",
        "What does the inside of a stem look like, and how is it organised for transport?",
        "- Describe the internal structure of a herbaceous stem\n- Identify epidermis, cortex, vascular bundle (xylem + phloem), pith (Obj a)",
        "- Observe and sketch a stem cross-section\n- Identify vascular bundles in a real or prepared stem",
        "- Show curiosity about the hidden internal organisation of familiar plants",
        "Reveals the internal arrangement of a stem, connecting macroscopic structure to the transport functions already introduced.",
        "Fresh celery stalks or young bean stems; sharp blade (teacher-only); hand lens; red food dye solution",
        "Only teacher cuts with the blade; students handle pre-cut sections only.",
        [
            _pr("Predict: 'Draw what you think the inside of a stem looks like if you cut it across'",
                "Blank paper; pencils",
                "Do NOT show stem cross-section yet; let students predict based on prior lessons",
                "Think-aloud: 'I expect to see … because …'",
                "Collect predictions; note whether students include xylem/phloem from Lesson 3"),
            _pr("Observe pre-cut stem cross-sections with a hand lens; identify the visible 'dots' (vascular bundles)",
                "Pre-cut celery or bean stem sections; hand lens",
                "Circulate; guide students to find the ring of vascular bundles",
                "Compare prediction with observation: 'What is the same? What is different?'",
                "Annotated sketch of observed cross-section"),
            _pr("Compare prediction diagrams with actual cross-section diagram; label epidermis, vascular bundle, pith",
                "Labelled diagram of herbaceous stem cross-section",
                "Guided labelling activity",
                "Connect to previous lessons: 'Which part of the vascular bundle is xylem? Which is phloem?'",
                "Exit ticket: draw and label a stem cross-section from memory"),
            _pr("Dye demonstration: place celery stalk in red food dye; predict where the dye will travel",
                "Celery stalk in red dye solution (set up in advance); pre-cut sections showing dye",
                "Show cross-section stained with dye; ask 'Which tissue absorbed the dye and why?'",
                "Connect to xylem structure: hollow dead cells ideal for water flow",
                "Students record observation and explain using xylem function knowledge"),
            _pr("Update plant model: add clear labels for xylem and phloem within the stem cross-section",
                "Running plant model diagram",
                "Compare model progression from Lesson 1 to Lesson 5",
                "Pair discussion: 'How has your understanding of the stem changed?'",
                "Model update check: does diagram show xylem inside phloem (correct for dicot)?"),
        ],
    ),
    _bio_lesson(
        6, "Leaf Structure and Transport Role",
        "How do the veins and stomata of a leaf connect to the plant's transport system?",
        "- Identify veins (vascular bundles), stomata, guard cells and mesophyll in a leaf\n- Explain how leaf structure supports both transport and gas exchange (Obj a)",
        "- Observe a leaf, locate veins; use a microscope or diagram to identify stomata and guard cells",
        "- Appreciate how multiple structures work together to support the life functions of a leaf",
        "Completes the organ-level structural overview (roots, stem, leaf) and connects leaf structure to both water transport and transpiration.",
        "Fresh leaves; hand lens; diagram of leaf cross-section; microscope or prepared slides (if available)",
        "Handle sharp edges of leaves with care; wash hands after handling plant material.",
        [
            _pr("Hold a leaf up to light; trace the veins; predict what the veins contain",
                "Fresh leaves of different sizes",
                "Guide observation: 'The vein network is the transport highway of the leaf'",
                "Connect to stems: 'Veins are continuous with the vascular bundles in the stem'",
                "Quick sketch of leaf vein network"),
            _pr("Examine diagram of leaf cross-section; identify palisade and spongy mesophyll, upper/lower epidermis, stomata",
                "Labelled leaf cross-section diagram; microscope/prepared slide if available",
                "Guided labelling; emphasise guard cells flanking each stoma",
                "Question: 'Where does water leave the leaf? Where does CO₂ enter?'",
                "Students label an unlabelled leaf cross-section diagram"),
            _pr("Discuss: why are most stomata on the underside of the leaf? Link to transpiration",
                "Completed cross-section diagrams",
                "Pose question; accept hypotheses before explaining",
                "Connect to driving question: 'Stomata are where water vapour escapes — this is transpiration'",
                "Exit ticket: state the function of guard cells"),
            _pr("Update DQB: 'How does water leave the plant through the leaf?'",
                "Driving Question Board",
                "Foreshadow Lesson 16 on transpiration",
                "Revisit phenomenon: 'When wind blows over spinach leaves, what happens at the stomata?'",
                "Students predict whether open or closed stomata cause more wilting"),
            _pr("Update plant model: add leaf detail showing veins connecting to stem xylem, and stomata on underside",
                "Running plant model diagram",
                "Model: 'Zoom in on the leaf — show the last stop before water exits the plant'",
                "Compare models with partner; share one new insight",
                "Note: students should now have a complete organ-level model (root→stem→leaf)"),
        ],
    ),
    _bio_lesson(
        7, "Xylem — Structure and Function",
        "Why is xylem described as 'dead' tissue, and how does this make it ideal for water transport?",
        "- Describe the structure of xylem: hollow dead cells, thickened lignified walls, no end walls\n- Explain how each structural feature is an adaptation for water transport (Obj a)",
        "- Draw a labelled xylem vessel diagram\n- Explain how lignification provides strength while the hollow lumen allows flow",
        "- Appreciate that even dead cells serve vital functions in living organisms",
        "Examines xylem at the cellular level, establishing the structural basis for water transport and cohesion-tension.",
        "Xylem vessel diagrams; cross-section diagram showing lignified walls; model kit or drinking straw analogy",
        "No specific hazards.",
        [
            _pr("Predict: 'What would the ideal tube for transporting water look like?' — sketch your design",
                "Blank paper; pencils",
                "Students design their ideal water transport tube before seeing xylem structure",
                "Think-aloud: 'What properties should it have? Strong walls? Open ends?'",
                "Compare student designs with a partner"),
            _pr("Examine labelled xylem vessel diagram; identify: hollow lumen, lignified wall, no end walls, pits",
                "Labelled xylem vessel diagram",
                "Guided labelling; compare student's predicted design with actual xylem",
                "Question: 'Why is it an advantage that xylem cells are dead?'",
                "Exit ticket: label an unlabelled xylem vessel and state one adaptation + function"),
            _pr("Straw analogy: blow through a drinking straw to feel resistance; discuss how xylem diameter affects flow rate",
                "Drinking straws of different diameters",
                "Demonstrate flow through narrow vs. wide straw; connect to xylem vessel diameter",
                "Introduce term: transpiration stream — continuous column of water from root to leaf",
                "Students write one sentence explaining why wide xylem vessels are more efficient"),
            _pr("Update DQB: 'How does water move continuously up the xylem against gravity?'",
                "Driving Question Board",
                "Foreshadow Lesson 14: cohesion-tension theory",
                "Students vote: 'Is it pressure from below, pull from above, or both?'",
                "Record predictions to revisit in Lesson 14"),
            _pr("Update plant model: show xylem as continuous tube from root to leaf; add lignified wall label",
                "Running plant model diagram",
                "Emphasise the continuous nature of the xylem column",
                "Discuss: 'Your model is now showing why xylem must be continuous — one break stops all flow'",
                "Model update check: does student show xylem as one unbroken pathway?"),
        ],
    ),
    _bio_lesson(
        8, "Phloem — Structure and Function",
        "How does phloem differ from xylem in structure, and why does it transport food rather than water?",
        "- Describe phloem: living sieve tube cells, companion cells, sieve plates\n- Compare xylem and phloem structures and functions (Obj a)",
        "- Draw and compare xylem and phloem diagrams\n- Explain why phloem must be living (active transport of sugars)",
        "- Appreciate that two complementary systems are needed for a plant to function fully",
        "Completes the structural study of vascular tissue by examining phloem, reinforcing the contrast with xylem through comparison.",
        "Phloem diagram; xylem diagram for comparison; comparison table template",
        "No specific hazards.",
        [
            _pr("Recall xylem features from Lesson 7; predict: 'How might the sugar transport tube differ?'",
                "Xylem diagram from Lesson 7",
                "Elicit prior knowledge; focus on: xylem is dead — should phloem be dead or living and why?",
                "Pair discussion: justify prediction",
                "Quick written prediction before revealing phloem diagram"),
            _pr("Examine phloem diagram; identify sieve tube cells, sieve plates, companion cells",
                "Labelled phloem diagram",
                "Guided labelling; emphasise sieve plates (perforated end walls allow flow) and living cells",
                "Question: 'Why do companion cells supply energy to sieve tubes?'",
                "Label an unlabelled phloem diagram"),
            _pr("Complete a comparison table: xylem vs. phloem (cells alive/dead, walls, direction of flow, substance transported)",
                "Blank comparison table template",
                "Pairs complete table; class discussion to agree correct answers",
                "Connect: 'Sugar flows in both directions in phloem — why might this be useful?'",
                "Exit ticket: state two differences between xylem and phloem"),
            _pr("Update DQB: 'Why do plants need to move sugars as well as water?'",
                "Driving Question Board",
                "Connect to translocation (foreshadow Lesson 21)",
                "Real-world link: 'Sucrose from leaves must reach growing roots, fruits, and seeds'",
                "Students predict what would happen if phloem was blocked"),
            _pr("Update plant model: add phloem alongside xylem; show bidirectional arrows for sugar flow",
                "Running plant model diagram",
                "Key addition: phloem arrows point BOTH up and down; xylem arrows point only UP",
                "Compare with previous model; discuss what changed",
                "Check: does student's model distinguish xylem (upward) from phloem (bidirectional)?"),
        ],
    ),
    _bio_lesson(
        9, "Introduction to Monocots and Dicots",
        "What are the key differences between a maize plant (monocot) and a bean plant (dicot)?",
        "- Define monocotyledon and dicotyledon\n- Identify visible differences: leaf venation, root type, number of cotyledons (Obj b)",
        "- Examine and compare monocot and dicot plants; record differences in a table",
        "- Appreciate the diversity of plant life and its organisation into meaningful categories",
        "Introduces the monocot/dicot distinction that will be examined at the tissue level in Lessons 10–12.",
        "Maize and bean seeds (germinated and dry); whole plant specimens or photos; comparison chart",
        "Handle seeds carefully; wash hands after handling plant material.",
        [
            _pr("Examine maize and bean plants side by side; list as many differences as possible",
                "Maize and bean specimens or photos; observation recording sheet",
                "Allow free observation first; then guide: focus on leaves, roots, seeds",
                "Think-Pair-Share observations",
                "Quick list: how many differences did each pair find?"),
            _pr("Focus on leaf venation: trace veins on a monocot leaf (parallel) and dicot leaf (net-like)",
                "Fresh maize and bean leaves; pencils for tracing",
                "Demo: hold leaf to light to show vein pattern clearly",
                "Question: 'What might parallel vs. net venation tell us about internal structure?'",
                "Students sketch both venation patterns with labels"),
            _pr("Focus on seeds: count cotyledons in bean (2) and maize (1); connect name to definition",
                "Bean and maize seeds soaked overnight (easily split)",
                "Students carefully split seeds and count seed leaves",
                "Etymology: 'mono' = one, 'di' = two — helps students remember",
                "Exit ticket: define monocot and dicot using the cotyledon criterion"),
            _pr("Update DQB: 'Are xylem and phloem arranged differently in monocots and dicots?'",
                "Driving Question Board",
                "Foreshadow Lessons 10–11: vascular arrangement in stems and roots",
                "Students predict based on what they already know about vascular bundles",
                "Record predictions for verification in Lessons 10–11"),
            _pr("Update plant model: annotate with M (monocot) and D (dicot) features observed",
                "Running plant model (or new diagram focused on monocot vs. dicot)",
                "Introduce concept of two model types for this sub-strand",
                "Pair share: 'What is one thing you would now change about your original model?'",
                "Observation check: do students link venation pattern to internal vascular arrangement?"),
        ],
    ),
    _bio_lesson(
        10, "Vascular Arrangement in Stems",
        "How is the vascular tissue arranged differently in monocot and dicot stems?",
        "- Describe and illustrate the arrangement of vascular bundles in monocot stems (scattered) vs. dicot stems (ring) (Obj b)",
        "- Observe, sketch and compare stem cross-sections from a monocot and a dicot",
        "- Appreciate how internal organisation at the cellular level relates to the plant's overall structure",
        "Examines the vascular arrangement in stems at the tissue level, directly fulfilling Objective b.",
        "Pre-cut cross-sections of maize stem (monocot) and bean/sunflower stem (dicot); hand lens; diagrams",
        "Only teacher cuts stems with a blade; students handle pre-cut sections only.",
        [
            _pr("Revisit Lesson 5 stem cross-section diagram; predict: will monocot and dicot stems look the same inside?",
                "Lesson 5 diagram; blank prediction sketch",
                "Elicit predictions; do not reveal answer",
                "Pair discussion; justify prediction",
                "Record predictions — to be verified during observation"),
            _pr("Observe pre-cut monocot (maize) and dicot (bean) stem cross-sections with a hand lens",
                "Pre-cut stem cross-sections; hand lens",
                "Guide observation: 'Where are the vascular bundles? Are they in a ring or scattered?'",
                "Compare: 'Point to the main difference between the two stems'",
                "Annotated sketch of both cross-sections"),
            _pr("Compare observations with labelled diagrams; confirm: scattered (monocot) vs. ring (dicot)",
                "Labelled comparative diagram of monocot vs. dicot stem cross-sections",
                "Guided labelling; emphasise epidermis, cortex, vascular bundle positions, pith",
                "Question: 'Why might a scattered arrangement give extra strength to a grass stem?'",
                "Exit ticket: draw and label monocot and dicot stem cross-sections from memory"),
            _pr("Update DQB: confirm earlier prediction about monocot vs. dicot differences",
                "Driving Question Board",
                "Tick off any confirmed answers; update any wrong predictions",
                "Connect to prior lessons: 'Same xylem and phloem — just differently arranged'",
                "Students write a 'Prediction vs. Finding' statement"),
            _pr("Update plant models: draw TWO versions — monocot stem and dicot stem cross-sections with labels",
                "Running plant model (now branches into monocot and dicot versions)",
                "Students create a side-by-side comparison in their models",
                "Compare with partner: identify at least one correct and one to-improve feature",
                "Model check: correct positioning of scattered vs. ring bundles"),
        ],
    ),
    _bio_lesson(
        11, "Vascular Arrangement in Roots",
        "How does the arrangement of vascular tissue in roots compare between monocots and dicots?",
        "- Describe the arrangement of xylem and phloem in monocot roots (alternating) vs. dicot roots (central xylem star with phloem between arms) (Obj b)",
        "- Compare root and stem cross-sections; observe the continuity of vascular tissue",
        "- Appreciate that structural patterns at the microscopic level reflect evolutionary adaptation",
        "Completes the vascular tissue arrangement study by examining roots, reinforcing Objective b.",
        "Prepared diagrams of monocot and dicot root cross-sections; comparison with stem diagrams from Lesson 10",
        "No specific hazards for diagram-based lesson.",
        [
            _pr("Recall stem vascular arrangements; predict: will root arrangements be similar or different?",
                "Stem cross-section diagrams from Lesson 10",
                "Elicit predictions; accept all hypotheses",
                "Focus question: 'In a root, which tissue is at the centre and why?'",
                "Written prediction before examining root diagrams"),
            _pr("Examine labelled diagrams of monocot and dicot root cross-sections; compare to stem",
                "Labelled monocot and dicot root cross-section diagrams",
                "Guided observation: point out central xylem star (dicot) vs. alternating xylem/phloem (monocot)",
                "Comparison table: root vs. stem arrangement for monocot and dicot",
                "Label an unlabelled root cross-section diagram"),
            _pr("Discuss: why might xylem be at the centre of a dicot root? Connect to function (strength for anchorage)",
                "Completed diagrams and comparison table",
                "Guide discussion: 'Roots are pulled and pushed by the soil — where should strength be?'",
                "Connect to xylem's lignified walls from Lesson 7",
                "Exit ticket: state one difference between monocot and dicot root cross-sections"),
            _pr("Update DQB: mark vascular arrangement questions as answered",
                "Driving Question Board",
                "Consolidate: 'We now know how xylem and phloem are arranged in both types of plant'",
                "Connect forward to Lesson 13: water now needs to cross from root to xylem",
                "Students summarise key differences between monocot and dicot in one paragraph"),
            _pr("Update plant models: add root cross-section detail showing xylem and phloem arrangement",
                "Running plant model",
                "Students add a 'zoom-in' box on the root showing tissue arrangement",
                "Compare monocot and dicot model versions",
                "Check: student models now show correct tissue positions in both stem and root"),
        ],
    ),
    _bio_lesson(
        12, "Practical Classification of Local Plants",
        "Can we identify whether a local plant is a monocot or a dicot by examining its observable features?",
        "- Apply knowledge of monocot/dicot differences to classify unfamiliar local plants\n- Justify classification using observable evidence (Obj b)",
        "- Classify at least 5 local plant specimens; record evidence for each classification",
        "- Appreciate the relevance of biology to identifying familiar plants in their local environment",
        "Applies the monocot/dicot knowledge to authentic local context through a practical classification activity.",
        "5–8 local plant specimens (grasses, crops, weeds); classification recording sheet; hand lens",
        "Wash hands after handling plants; do not handle plants with thorns without gloves.",
        [
            _pr("Receive 5 labelled plant specimens; predict monocot or dicot for each before closer examination",
                "Local plant specimens (labelled A–E); prediction sheet",
                "Guide: 'Use only external features for your initial prediction'",
                "Individual prediction then pair comparison",
                "Record predictions on sheet before investigation"),
            _pr("Examine each specimen; record evidence: leaf venation, root type (if visible), seed cotyledons",
                "Specimens; hand lens; recording sheet",
                "Circulate; prompt: 'What evidence supports your classification?'",
                "Pair discussion; record in structured evidence table",
                "Evidence table: specimen name, feature observed, conclusion"),
            _pr("Compare findings with class; discuss any disagreements; agree final classifications",
                "Class data on board; completed evidence tables",
                "Facilitate discussion of disagreements; model scientific reasoning",
                "Question: 'When two features give different answers, which should you trust more?'",
                "Exit ticket: classify one additional specimen shown on the board with justification"),
            _pr("Update DQB: confirm understanding of monocot and dicot differences",
                "Driving Question Board",
                "Celebrate: 'You can now classify plants based on scientific evidence — not just guessing'",
                "Connect to farming: 'Knowing plant type helps farmers choose appropriate techniques'",
                "Students add one real-world application to their DQB"),
            _pr("Update plant models: annotate model with local examples of monocots and dicots",
                "Running plant model",
                "Students label: 'Maize = monocot, Bean = dicot' with supporting features",
                "Pair share: compare which local examples each chose",
                "Check: correct classification with at least two pieces of supporting evidence"),
        ],
    ),
    _bio_lesson(
        13, "How Water Enters the Root — Osmosis and Diffusion",
        "How does water cross from the soil into the root hair, and then move toward the xylem?",
        "- Define osmosis and diffusion\n- Explain how water enters root hair cells by osmosis down a water potential gradient (Obj c)",
        "- Set up and interpret an osmosis demonstration\n- Trace the pathway of water from soil to xylem",
        "- Develop patience and precision in setting up experiments and recording observations accurately",
        "Introduces osmosis as the mechanism for water uptake, directly fulfilling Objective c.",
        "Dialysis tubing; sucrose solution; beakers; water; ruler; string; coloured water option",
        "Handle glassware carefully; wipe up any spills promptly.",
        [
            _pr("Predict: if you put a bag of sugar-water into plain water, what will happen to the bag?",
                "Blank prediction sheet; diagram of dialysis tubing setup",
                "Do not show result yet; elicit range of predictions",
                "Pair discussion: justify prediction using particle model of diffusion",
                "Record written predictions for comparison after demonstration"),
            _pr("Observe dialysis tubing osmosis demonstration (pre-set up by teacher); measure change in volume/mass",
                "Dialysis tubing setup in beakers; rulers or balance",
                "Show results; ask: 'What happened? Why did water move into the bag?'",
                "Connect to root hair: 'Root hair cell contents are more concentrated than soil water'",
                "Students record and explain the result"),
            _pr("Apply osmosis to root hair cell: trace water pathway from soil → root hair → cortex → xylem",
                "Diagram of root cross-section showing pathway",
                "Guided tracing: 'At each step, water moves from dilute to concentrated solution'",
                "Question: 'What happens to water potential at each step?'",
                "Exit ticket: draw an arrow showing the direction of water movement by osmosis in a root"),
            _pr("Update DQB: mark 'How does water enter the root?' as answered",
                "Driving Question Board",
                "Celebrate progress: 'You can now explain the first step in the water transport journey'",
                "Connect forward to Lesson 14: now water is in the xylem — how does it get to the leaves?",
                "Students write one sentence explaining water entry using the word 'osmosis'"),
            _pr("Update plant model: add osmosis arrows from soil to root hair and from root hair to xylem",
                "Running plant model",
                "Students add concentration gradient labels to their model",
                "Compare with Lesson 1 model: 'Look how much detail you have now'",
                "Model check: correct direction of osmosis arrows and concentration labels"),
        ],
    ),
    _bio_lesson(
        14, "Movement of Water Up the Plant",
        "What forces drive water from the roots all the way up to the leaves against gravity?",
        "- Describe the cohesion-tension theory (simplified): transpiration pull, cohesion of water molecules, adhesion to xylem walls\n- Explain why water moves upward as a continuous column (Obj c)",
        "- Demonstrate water column continuity using model or analogy\n- Explain the role of each force",
        "- Appreciate that physical forces, not a pump, drive water movement in plants",
        "Explains the mechanism driving water up the xylem, completing the water transport pathway from root to leaf.",
        "Paper towels or capillary tubes for capillarity demo; diagram of transpiration stream",
        "No specific hazards.",
        [
            _pr("Discuss: how can water climb 30 metres up a tree against gravity with no pump?",
                "Image of a tall tree; question on board",
                "Elicit ideas; accept all; emphasise there is no heart/pump in plants",
                "Pair discussion: propose a mechanism",
                "Record proposed mechanisms for class comparison"),
            _pr("Capillary rise demonstration: paper towel in water, or narrow tube vs. wide tube",
                "Paper towels; coloured water; capillary tubes of different widths",
                "Demo: water climbs higher in narrower tube — adhesion and surface tension",
                "Connect: xylem vessels are narrow, favouring capillary rise",
                "Students record observation and propose connection to xylem"),
            _pr("Introduce transpiration pull and cohesion-tension: water lost from leaves pulls the column upward",
                "Diagram of transpiration stream in xylem",
                "Analogy: chain of magnets — pulling the top pulls the whole chain",
                "Explain: cohesion keeps water molecules connected; adhesion prevents column collapse",
                "Exit ticket: state two forces that help water move up the xylem"),
            _pr("Update DQB: mark 'What forces drive water up the plant?' as answered",
                "Driving Question Board",
                "Revisit phenomenon: 'When wind dries the leaf surface, transpiration increases — what happens to the pull?'",
                "Connect: faster transpiration = stronger pull = faster water uptake from roots",
                "Students explain wilting using transpiration pull in one paragraph"),
            _pr("Update plant model: add upward arrows along xylem labelled 'transpiration pull'; add cohesion labels",
                "Running plant model",
                "Students draw a 'chain' analogy inside the xylem column",
                "Compare model with partner",
                "Check: student model shows unbroken column with forces labelled"),
        ],
    ),
    _bio_lesson(
        15, "Demonstration of Water Transport — Coloured Water Experiment",
        "Can we see water moving through xylem? How does the dye experiment show xylem function?",
        "- Describe the coloured water experiment and explain what it demonstrates\n- Interpret results to confirm xylem is the water transport vessel (Obj c)",
        "- Set up and observe a coloured water experiment; record and explain results",
        "- Appreciate that scientific demonstrations provide visible evidence for invisible processes",
        "Provides direct observable evidence that xylem transports water, consolidating Lessons 13–14.",
        "White carnations or celery stalks; red/blue food dye; water; beakers; sharp blade (teacher only); timer",
        "Only teacher uses the blade; students observe and record.",
        [
            _pr("Predict: if we put a white flower in red dye water, what will happen and why?",
                "White flowers or celery stalks; prediction sheet",
                "Do not show result; elicit predictions with reasoning",
                "Students connect to xylem knowledge: 'Where should the dye appear?'",
                "Record predictions with reasons before experiment"),
            _pr("Set up experiment: place flowers/celery in dye; observe after 30 minutes (or examine pre-prepared results)",
                "Dye-soaked specimens prepared in advance; fresh setup for class to observe over lesson",
                "Direct observation: which parts are stained? What does this tell us?",
                "Cross-section cut by teacher: show dye concentrated in xylem",
                "Students record: observation, conclusion, connection to xylem"),
            _pr("Discuss: what would happen if we cut the stem half-way and put two different colours in each half?",
                "Diagram of split-stem experiment (or actual demonstration)",
                "Pose extension question; accept hypotheses",
                "Reinforce: dye only travels in xylem — confirms xylem's role",
                "Students write: 'This experiment shows that … because …'"),
            _pr("Update DQB: mark 'How can we see water moving through the plant?' as answered",
                "Driving Question Board",
                "Celebrate: visible proof of xylem function",
                "Connect forward to Lessons 16–20: what happens to water once it reaches the leaves?",
                "Students suggest how transpiration connects to what they just observed"),
            _pr("Update plant model: add experimental evidence label — 'Confirmed by dye experiment'",
                "Running plant model",
                "Emphasise: models should be supported by evidence, not just theory",
                "Peer review: partner checks model for accuracy and evidence labels",
                "Check: model now includes evidence-based annotations"),
        ],
    ),
    _bio_lesson(
        16, "What is Transpiration?",
        "Why do plants lose water vapour through their leaves, and why is this useful?",
        "- Define transpiration: loss of water vapour from a plant, mainly through stomata\n- Explain the importance of transpiration: cooling, mineral uptake, maintaining turgor (Obj d)",
        "- Identify the route of water loss; explain the importance of transpiration for plant function",
        "- Appreciate that what seems like water 'waste' is actually a vital plant process",
        "Introduces transpiration as the driving force behind water transport, directly beginning Objective d.",
        "Diagrams of leaf with stomata; thermometer for temperature analogy; water-logged soil sample",
        "No specific hazards.",
        [
            _pr("Observe a plastic bag wrapped around a leafy branch (set up the day before); record observations",
                "Pre-prepared plant with plastic bag showing water droplets inside",
                "Ask: 'Where did the water come from? How did it get inside the bag?'",
                "Think-Pair-Share: connect to leaf structure and stomata from Lesson 6",
                "Students draw and annotate observation"),
            _pr("Define transpiration; trace the pathway of water vapour: root → xylem → leaf → stomata → air",
                "Diagram of transpiration pathway",
                "Guided diagram labelling; students add directional arrows",
                "Analogy: sweating in humans keeps us cool; stomata opening drives the water column upward",
                "Exit ticket: define transpiration in one sentence"),
            _pr("Discuss three reasons transpiration matters: cooling, mineral flow, turgor maintenance",
                "Board list of three reasons",
                "For each reason: connect to a real-world plant function",
                "Question: 'What would happen if a plant could not transpire at all?'",
                "Students rank the three reasons by importance and justify their choice"),
            _pr("Update DQB: 'What is transpiration and why does it matter?'",
                "Driving Question Board",
                "Connect to phenomenon: 'When spinach wilts, transpiration still continues but water is not replaced'",
                "Foreshadow Lessons 17–18: factors that affect transpiration rate",
                "Students predict which conditions cause fastest transpiration"),
            _pr("Update plant model: add transpiration labels at leaf stomata; show water vapour exiting",
                "Running plant model",
                "Students complete the water pathway from root to atmosphere in their model",
                "Compare full model with original Lesson 1 model",
                "Reflection: 'How has your model changed? What are you most proud of adding?'"),
        ],
    ),
    _bio_lesson(
        17, "Demonstrating Transpiration — Plastic Bag Experiment",
        "How can we use a simple plastic bag experiment to measure transpiration?",
        "- Describe the plastic bag method for demonstrating transpiration\n- Explain how mass loss provides evidence for transpiration rate (Obj d)",
        "- Set up experiment, record mass before and after, calculate water lost; interpret results",
        "- Develop accuracy in measurement and honest recording of experimental data",
        "Provides hands-on experimental evidence for transpiration, preparing students for the variables investigation in Lesson 19.",
        "Small pot plants or leafy branches; clear plastic bags; elastic bands; balance; timer",
        "Tie bags carefully; do not leave bags on plants for extended periods in full sun.",
        [
            _pr("Predict: if we cover a plant with a plastic bag, what will appear inside and why?",
                "Prediction sheet; diagram of setup",
                "Do not reveal result; elicit predictions with reasoning",
                "Connect to transpiration definition from Lesson 16",
                "Written prediction with reasoning"),
            _pr("Set up experiment: bag a plant, record mass, wait 20 minutes, record mass again; observe condensation",
                "Plant specimens; plastic bags; elastic bands; balance",
                "Students take measurements; record carefully in results table",
                "Circulate to ensure accurate reading of balance",
                "Results table: time, mass before, mass after, change in mass"),
            _pr("Calculate water lost; compare results across groups; explain why results vary",
                "Completed results tables",
                "Guided calculation; class data comparison on board",
                "Question: 'Why did some groups have more water loss than others?'",
                "Students identify possible reasons for variation — foreshadow Lesson 18"),
            _pr("Update DQB: 'How do we know transpiration is happening?'",
                "Driving Question Board",
                "Consolidate: direct evidence from experiment confirms transpiration",
                "Connect to phenomenon: 'In a drought, plants cannot replace the water lost through transpiration'",
                "Students explain wilting using transpiration rate in one sentence"),
            _pr("Update plant model: add quantitative note — 'Up to 98% of absorbed water is lost through transpiration'",
                "Running plant model",
                "Students add this statistic as an annotation",
                "Pair discussion: 'Does this surprise you? What are the implications for farming?'",
                "Check: model now includes experimental evidence and quantitative data"),
        ],
    ),
    _bio_lesson(
        18, "Factors Affecting Transpiration",
        "How do temperature, wind, light, and humidity affect how fast a plant loses water?",
        "- Identify four factors that affect transpiration rate: temperature, wind speed, light intensity, humidity (Obj d)\n- Explain the effect of each factor on stomatal aperture and evaporation",
        "- Predict the effect of changing one factor; justify predictions using scientific reasoning",
        "- Appreciate why transpiration is higher during hot, windy, sunny days — connecting to the phenomenon",
        "Explains why wilting is worse on hot, windy days, directly connecting to the anchoring phenomenon.",
        "Cards describing different weather conditions; transpiration rate data table; textbook or projected data",
        "No specific hazards.",
        [
            _pr("Sort weather condition cards (hot/cold, windy/calm, bright/dark, humid/dry) by predicted effect on transpiration",
                "Weather condition cards; sorting mat; prediction sheet",
                "Individual prediction then pair discussion",
                "Guide: 'Think about what makes water evaporate faster in everyday life'",
                "Record sorted cards as starting predictions"),
            _pr("Examine data table or graph showing transpiration rate under different conditions; identify trends",
                "Data table or graph of transpiration rate vs. each factor",
                "Guided graph reading: identify trends for each factor",
                "Question: 'Which factor has the greatest effect? How can you tell?'",
                "Students summarise each factor's effect in one sentence"),
            _pr("Explain the mechanism: high temperature → more evaporation; high wind → removes humid air; high light → opens stomata wider; low humidity → steeper gradient",
                "Annotated diagram showing stomata and moisture gradient",
                "Explain one factor at a time; connect to driving question",
                "Real-world link: 'This is why spinach wilts faster than mango on a hot windy day'",
                "Exit ticket: choose one factor and explain its effect on transpiration"),
            _pr("Revisit the phenomenon: explain why spinach wilts faster than mango on hot windy days",
                "Phenomenon description from Lesson 1; student initial models",
                "Whole-class discussion: use today's knowledge to construct an explanation",
                "Connect to Lesson 20: how can farmers use this knowledge?",
                "Students write a partial explanation of the phenomenon using transpiration factors"),
            _pr("Update plant model: add labels showing 4 factors and their effect on stomatal aperture",
                "Running plant model",
                "Add a weather condition box linking to the leaf diagram",
                "Compare: 'Your model can now explain the phenomenon!'",
                "Check: model includes all 4 factors with correct effect direction"),
        ],
    ),
    _bio_lesson(
        19, "Investigation Activity — Testing One Factor Affecting Transpiration",
        "Does a plant in direct sunlight lose more water than one in the shade?",
        "- Design and conduct a simple investigation to test one factor affecting transpiration\n- Use variables correctly: independent, dependent, controlled (Obj d)",
        "- Conduct investigation; collect data; interpret results; evaluate method",
        "- Develop scientific inquiry skills: hypothesis, fair test, data collection, evaluation",
        "Applies Lesson 18 knowledge through a student-designed investigation, developing scientific process skills.",
        "Two identical potted plants or leafy branches in bags; balance; light source or sunlit window; ruler",
        "Do not leave plants in extreme heat; ensure bags are securely fastened.",
        [
            _pr("Write a hypothesis: 'I predict that the plant in sunlight will lose MORE/LESS water because …'",
                "Hypothesis writing frame",
                "Guide: hypothesis must state direction of effect and reason",
                "Pair share hypotheses; check that reasoning connects to Lesson 18",
                "Written hypothesis before investigation begins"),
            _pr("Set up experiment: place two identical plants in sun vs. shade; record mass every 10 minutes for 30 minutes",
                "Identical plants in bags; balance; timer; results table",
                "Students take measurements and record; teacher circulates for accuracy",
                "Guided: 'What are you keeping the same? What are you changing? What are you measuring?'",
                "Results table with at least 3 time points"),
            _pr("Interpret results: did the data support the hypothesis? Calculate water loss for each condition",
                "Completed results tables; class data compilation",
                "Guided interpretation: connect data pattern to mechanism from Lesson 18",
                "Question: 'What are the limitations of this investigation?'",
                "Written conclusion: results + explanation + one limitation"),
            _pr("Update DQB: confirm answer to 'What factors affect transpiration rate?'",
                "Driving Question Board",
                "Celebrate: 'You designed and conducted a scientific investigation!'",
                "Connect forward to Lesson 20: how can farmers use this knowledge?",
                "Students identify one improvement to their experimental design"),
            _pr("Update plant model: annotate with 'Confirmed by investigation' for the light factor",
                "Running plant model",
                "Emphasise evidence-based science: model claims should be supported by data",
                "Compare investigation results with data from Lesson 18",
                "Check: student can identify IV, DV, and CVs in their own investigation"),
        ],
    ),
    _bio_lesson(
        20, "Application to Farming — Managing Transpiration",
        "How can farmers use knowledge of transpiration to protect their crops from wilting?",
        "- Describe how mulching, windbreaks, shade nets, and irrigation timing reduce water loss\n- Connect transpiration knowledge to practical farming strategies (Obj d)",
        "- Evaluate farming techniques using transpiration knowledge; suggest improvements for a local farm scenario",
        "- Value the practical application of biology to food security in their local context",
        "Connects the science of transpiration directly to the anchoring phenomenon (wilting crops) and to real farming practice.",
        "Photos of mulched/unmulched crops; diagrams of windbreak and shade net; local farming scenario card",
        "No specific hazards.",
        [
            _pr("Scenario: a local farmer's spinach wilts every afternoon despite watering in the morning — what advice would you give?",
                "Scenario description card; local farm photo if available",
                "Pose the scenario; do not give answers",
                "Pair discussion: use knowledge from Lessons 16–19 to generate advice",
                "Record advice before class discussion"),
            _pr("Examine photos of mulching, windbreaks, shade nets, drip irrigation; identify how each reduces transpiration",
                "Photos or diagrams of each technique",
                "Guided discussion: for each technique, ask 'Which factor does this control?'",
                "Connect to Lesson 18 factors: mulch reduces temperature; windbreak reduces wind speed",
                "Summary table: technique → factor controlled → effect on transpiration"),
            _pr("Evaluate which technique is most suitable for a smallholder farmer in a semi-arid area",
                "Cost and practicality considerations for each technique",
                "Small group discussion; each group presents their recommended technique with justification",
                "Teacher adds: no single solution — context determines best approach",
                "Exit ticket: choose one technique and justify using transpiration science"),
            _pr("Revisit the phenomenon: complete explanation of why spinach wilts faster than mango on hot windy days",
                "Phenomenon from Lesson 1; student explanation attempts from Lesson 18",
                "Class builds a complete explanation on the board",
                "Check: explanation includes stomata, transpiration pull, xylem, factors",
                "Students write their personal complete explanation of the phenomenon"),
            _pr("Update plant model: add 'farming interventions' box showing techniques that reduce transpiration rate",
                "Running plant model",
                "Final model should now connect biology to farming practice",
                "Compare Lesson 1 model with Lesson 20 model side by side",
                "Reflection: 'What is the single most important thing you have learned about plant transport?'"),
        ],
    ),
    _bio_lesson(
        21, "Movement of Food in Plants — Translocation",
        "How does the food made in leaves reach all other parts of the plant?",
        "- Define translocation: movement of dissolved food (sucrose) through phloem from source to sink\n- Identify sources (leaves) and sinks (roots, fruits, growing tips) (Obj e)",
        "- Trace the pathway of sucrose from source to sink; interpret ringing experiment evidence",
        "- Appreciate the complexity of plant physiology and how each system supports the others",
        "Directly fulfils Objective e and completes the transport system overview by adding the food transport pathway.",
        "Diagram of source/sink model; ringing experiment diagram; labelled phloem diagram from Lesson 8",
        "No specific hazards.",
        [
            _pr("Recall from Lesson 8: phloem transports sugar. Pose question: 'Where is sugar made? Where does it need to go?'",
                "Lesson 8 xylem/phloem comparison table",
                "Elicit: sugar made in leaves by photosynthesis; must reach roots, growing tips, fruits",
                "Introduce source (where sugar is made) and sink (where sugar is used)",
                "Students draw a simple source-to-sink diagram for one plant"),
            _pr("Introduce translocation and the ringing experiment: removing a ring of bark (phloem) blocks food transport",
                "Diagram of ringing experiment showing swelling above and withering below",
                "Explain: bark includes phloem; removal blocks sugar but NOT water (xylem is deeper)",
                "Question: 'Why does the tissue ABOVE the ring swell while the root withers?'",
                "Students explain the ringing experiment result using source/sink/phloem knowledge"),
            _pr("Trace translocation pathway: leaf → phloem → stem → root/fruit/growing tip",
                "Whole-plant diagram showing source and sink with phloem pathway",
                "Emphasise: phloem carries sugar in BOTH directions (up to growing tips AND down to roots)",
                "Compare with xylem: 'Xylem goes only up; phloem goes both ways — why?'",
                "Exit ticket: state the definition of translocation and name one source and two sinks"),
            _pr("Update DQB: mark 'How does food move in the plant?' as answered",
                "Driving Question Board",
                "Connect translocation to xylem transport: both needed for a fully functioning plant",
                "Real-world link: sugar translocation to fruits is what makes them edible and sweet",
                "Students write a comparison: 'Xylem transports … Phloem transports … Both are similar in that …'"),
            _pr("Update plant model: add phloem pathway with source and sink labels; show bidirectional sugar flow",
                "Running plant model",
                "Students complete the food transport pathway in their model",
                "Final model should now show BOTH water transport (xylem) and food transport (phloem)",
                "Pair review: check both pathways are correctly drawn and labelled"),
        ],
    ),
    _bio_lesson(
        22, "Unit Summary and Assessment",
        "How do xylem and phloem work together to keep a plant alive — and how does this explain our phenomenon?",
        "- Summarise all five learning objectives: structures (Obj a), monocot/dicot (Obj b), water uptake (Obj c), transpiration (Obj d), translocation (Obj e)\n- Construct a complete explanation of the anchoring phenomenon",
        "- Present or write a complete explanation linking the whole transport system to the phenomenon\n- Self-assess against unit objectives",
        "- Reflect on how scientific understanding developed through the unit; appreciate the integration of all systems",
        "Summative lesson: students return to the phenomenon and construct a full evidence-based explanation using all unit knowledge.",
        "Student running plant models; Summary Table; unit notes; assessment sheet",
        "No specific hazards.",
        [
            _pr("Return to Lesson 1 initial model: compare with current model; identify growth in understanding",
                "Lesson 1 model and current model side by side",
                "Students reflect: 'What is in my current model that was not in my Lesson 1 model?'",
                "Class discussion: celebrate how far understanding has developed",
                "Quick inventory: can students name all 5 objectives?"),
            _pr("Write a complete explanation of the phenomenon using all five objectives",
                "Phenomenon description from Lesson 1; writing frame with 5 sentence starters",
                "Students write independently for 15 minutes",
                "Circulate: check for use of key vocabulary (osmosis, transpiration, xylem, phloem, translocation)",
                "Collect as summative assessment piece"),
            _pr("Present explanation to a partner; partner gives feedback using a checklist",
                "Peer feedback checklist linked to 5 objectives",
                "Structured peer review: 'I can see … I think you should add …'",
                "Students revise explanation based on feedback",
                "Final self-assessment: rate confidence on each objective (1–3)"),
            _pr("Update DQB: mark all questions as answered; identify any remaining uncertainties",
                "Driving Question Board",
                "Class celebration: 'We answered the driving question!'",
                "Acknowledge remaining questions as areas for future study",
                "Students add one new question that the unit raised for them"),
            _pr("Submit final updated plant model with all pathways, labels and evidence annotations",
                "Running plant model (final version)",
                "Final model should show: root hair absorption, xylem pathway, leaf stomata, transpiration factors, phloem pathway, source/sink",
                "Teacher collects models for portfolio assessment",
                "Reflection: 'Which lesson most changed your thinking and why?'"),
        ],
    ),
]

# Biology summary table rows (source: lesson titles; detail: generated)
_BIO_SUMMARY_ROWS = [
    ("Lesson 1: Introduction to the Phenomenon",
     "Observed wilting spinach; drew initial models of water movement inside plants; posted questions on Driving Question Board",
     "Plants need water for survival; when water is lost faster than absorbed, cells lose turgor and the plant wilts",
     "The phenomenon shows what happens when the transport system cannot keep up with water loss",
     "DQB Started: Why do some crops wilt quickly? Initial Model: Water moves from roots to leaves — unclear how"),
    ("Lesson 2: What Do Plants Need to Survive?",
     "Sorted plant needs into categories; linked each need to a transport process; updated initial model",
     "Plants need water, mineral salts, CO₂ and light; water and minerals must be transported from soil to all cells",
     "Transport is essential because plant cells everywhere need water, not just roots",
     "DQB Updated: 'How do plants get water from soil?' Model Revised: Added entry points for water and minerals"),
    ("Lesson 3: Overview of Plant Transport System",
     "Colour-coded whole-plant diagram with xylem (blue) and phloem (green) pathways",
     "Xylem transports water and minerals upward; phloem transports sugars in both directions",
     "The plant has two separate transport vessels, each with a different role in keeping all cells supplied",
     "DQB Updated: 'What is the difference between xylem and phloem?' Model Revised: Added two distinct pathways"),
    ("Lesson 4: Root Structure and Function",
     "Observed germinated bean roots; drew and labelled root hair cell; calculated surface area advantage",
     "Root hair cells have a large surface area, thin walls and large vacuole — all adaptations for rapid water absorption",
     "The root hair design maximises the rate of water uptake, which is critical when plants are losing water through leaves",
     "DQB Updated: 'How does water enter the root?' Model Revised: Added root hair cells with absorption arrows"),
    ("Lesson 5: Stem Structure",
     "Observed stem cross-sections; identified vascular bundles; watched dye travel through xylem",
     "The stem contains vascular bundles with xylem (innermost) and phloem; xylem is continuous from root to leaf",
     "The stem's internal transport highway connects root absorption to leaf use — disrupting it would kill the plant",
     "DQB Updated: 'Where exactly is xylem in the stem?' Model Revised: Added stem cross-section with vascular bundle ring"),
    ("Lesson 6: Leaf Structure and Transport Role",
     "Examined leaf cross-sections; identified veins, stomata and guard cells; linked to transpiration",
     "Leaves have veins (extensions of vascular bundles) and stomata (controlled pores) where water vapour exits",
     "The leaf is where water exits the plant — stomata are the gateway between the plant's transport system and the atmosphere",
     "DQB Updated: 'How does water leave the plant through the leaf?' Model Revised: Added stomata on leaf underside"),
    ("Lesson 7: Xylem — Structure and Function",
     "Drew labelled xylem vessel; compared with student-designed ideal water tube; discussed lignification",
     "Xylem vessels are dead, hollow, lignified cells with no end walls — perfectly adapted for continuous water flow",
     "Xylem structure explains why water can travel continuously from root to leaf without leaking or collapsing",
     "DQB Updated: 'How does water move up against gravity?' Model Revised: Added lignified walls and hollow lumen labels"),
    ("Lesson 8: Phloem — Structure and Function",
     "Drew phloem diagram; completed xylem vs. phloem comparison table",
     "Phloem has living sieve tube cells and companion cells; sugar transport requires living cells with active processes",
     "Unlike xylem, phloem must be alive because sugar loading and unloading requires energy — this is active transport",
     "DQB Updated: 'Why do plants need to move sugars too?' Model Revised: Added phloem with bidirectional arrows"),
    ("Lesson 9: Introduction to Monocots and Dicots",
     "Compared maize and bean specimens; identified differences in venation, root type and cotyledon number",
     "Monocots have one cotyledon, parallel leaf venation; dicots have two cotyledons, net-like venation",
     "Both monocots and dicots have xylem and phloem — but their arrangement differs, which will affect transport efficiency",
     "DQB Updated: 'Are xylem and phloem arranged differently in monocots and dicots?' Model Revised: Two model types started"),
    ("Lesson 10: Vascular Arrangement in Stems",
     "Observed pre-cut monocot (maize) and dicot (bean) stem cross-sections; compared and sketched both",
     "Monocot stems have vascular bundles scattered throughout; dicot stems have vascular bundles in a ring",
     "The different arrangements reflect different evolutionary strategies — both still successfully transport water and food",
     "DQB Updated: Confirmed monocot/dicot stem differences. Model Revised: Added correct vascular arrangement to both stem types"),
    ("Lesson 11: Vascular Arrangement in Roots",
     "Compared monocot and dicot root cross-sections using diagrams; linked position of xylem to function",
     "Dicot roots have a central xylem star with phloem between the arms; monocot roots have alternating xylem and phloem",
     "Central xylem in dicot roots provides structural strength for anchorage — form follows function",
     "DQB Updated: Confirmed monocot/dicot root differences. Model Revised: Added root cross-section with correct tissue positions"),
    ("Lesson 12: Practical Classification of Local Plants",
     "Examined 5+ local plant specimens; classified each as monocot or dicot using observable evidence",
     "Local plants can be classified as monocots or dicots using venation, root type and cotyledon evidence",
     "Classification skills allow farmers and scientists to predict plant behaviour and apply appropriate management techniques",
     "DQB Updated: Added application question. Model Revised: Annotated with local plant examples"),
    ("Lesson 13: How Water Enters the Root",
     "Observed osmosis demonstration; traced water pathway from soil to xylem; applied osmosis to root hair cells",
     "Water enters root hair cells by osmosis down a water potential gradient; it moves from dilute soil water to concentrated cell contents",
     "Osmosis is the mechanism that drives the first step in water transport — without it, the entire system stops",
     "DQB Updated: Marked 'How does water enter the root?' as answered. Model Revised: Added osmosis arrows and concentration gradients"),
    ("Lesson 14: Movement of Water Up the Plant",
     "Observed capillary rise; explained transpiration pull and cohesion-tension theory",
     "Transpiration pull, cohesion between water molecules and adhesion to xylem walls drive the continuous upward flow of water",
     "The driving force for water transport is at the TOP of the plant (leaves), not the bottom — this explains how trees can be so tall",
     "DQB Updated: Marked 'What forces drive water upward?' as answered. Model Revised: Added force labels along xylem column"),
    ("Lesson 15: Demonstration of Water Transport",
     "Set up and observed coloured water experiment; cross-sectioned dye-stained stems to confirm xylem transport",
     "The coloured water experiment provides direct evidence that xylem (and only xylem) transports water through the stem",
     "Visible evidence reinforces the model: xylem is the water highway, and it runs continuously from root to leaf",
     "DQB Updated: 'How can we see water moving through the plant?' answered. Model Revised: Added 'Confirmed by dye experiment' label"),
    ("Lesson 16: What is Transpiration?",
     "Observed condensation in plastic bag experiment; defined transpiration; explained its importance",
     "Transpiration is the loss of water vapour from a plant mainly through stomata; it drives water uptake and cools the plant",
     "Transpiration explains why plants continuously need water — it is the engine that pulls water upward through the whole plant",
     "DQB Updated: 'What is transpiration?' answered. Model Revised: Completed the water pathway from root to atmosphere"),
    ("Lesson 17: Demonstrating Transpiration",
     "Set up plastic bag experiment; measured and calculated water loss; compared results across groups",
     "Transpiration can be measured by recording mass loss; rate varies between plants and conditions",
     "Quantitative evidence shows that plants lose significant amounts of water through transpiration — critical in drought conditions",
     "DQB Updated: Added quantitative data on transpiration rate. Model Revised: Added 'Up to 98% of water is lost through transpiration'"),
    ("Lesson 18: Factors Affecting Transpiration",
     "Examined data on transpiration rate under different conditions; explained mechanism of each factor",
     "Higher temperature, increased light, stronger wind and lower humidity all increase the transpiration rate",
     "These factors explain exactly why spinach wilts faster on hot, windy days — the conditions accelerate water loss beyond what roots can replace",
     "DQB Updated: 'What conditions increase transpiration?' answered — directly explains the phenomenon. Model Revised: Added 4-factor weather box"),
    ("Lesson 19: Investigation Activity",
     "Designed and conducted experiment testing effect of light on transpiration; collected and interpreted data",
     "Scientific investigation skills: hypothesis, variable control, data collection, interpretation and evaluation",
     "Students tested the connection between the transpiration factor (light) and the phenomenon (wilting in sun) experimentally",
     "DQB Updated: Light factor confirmed by student data. Model Revised: Added 'Confirmed by investigation' for light factor"),
    ("Lesson 20: Application to Farming",
     "Analysed farming techniques (mulching, windbreaks, shade nets); linked each to a transpiration factor",
     "Mulching, windbreaks and shade nets reduce transpiration by controlling temperature, wind speed and light intensity",
     "Knowledge of transpiration allows farmers to protect crops from wilting — directly solving the problem in the phenomenon",
     "DQB Updated: Phenomenon fully explained. Model Revised: Added farming interventions box connecting biology to practice"),
    ("Lesson 21: Movement of Food in Plants",
     "Introduced translocation; interpreted ringing experiment; traced sucrose from source to sink",
     "Translocation is the movement of dissolved sugars through phloem from source (leaves) to sink (roots, fruits, growing tips)",
     "While xylem transports water for survival, phloem transports food for growth — both systems are essential for a complete plant",
     "DQB Updated: 'How does food move in the plant?' answered. Model Revised: Added phloem source/sink labels and bidirectional arrows"),
    ("Lesson 22: Unit Summary and Assessment",
     "Compared initial and final plant models; wrote complete explanation of phenomenon; presented to peers",
     "The complete plant transport system: osmosis (water entry) + xylem (water pathway) + transpiration (water exit) + phloem (food transport)",
     "The phenomenon is fully explained: spinach wilts because transpiration in hot, windy conditions exceeds the rate of water uptake via xylem",
     "DQB Complete: All questions answered. Final Model: Shows complete dual transport system from soil to atmosphere with all mechanisms labelled"),
]

# Biology final explanation sections
_BIO_FE_SECTIONS = [
    (
        "SECTION 1: HOW DO PLANTS OBTAIN AND TRANSPORT WATER?",
        "How does water enter a plant from the soil?\n"
        "What is osmosis and how does it apply to root hair cells?\n"
        "What forces drive water up the xylem from root to leaf?\n"
        "How is the structure of xylem adapted for water transport?",
        "Water enters the plant through root hair cells by osmosis. Root hair cells have a large surface area, thin walls and a vacuole containing a more concentrated solution than the surrounding soil water. Water moves by osmosis from the dilute soil solution into the concentrated cell contents, across the semi-permeable membrane.\n\n"
        "Once inside the root, water moves toward the xylem through the cortex cells. It then enters the xylem and travels upward in a continuous column. The driving force is transpiration pull: as water evaporates from leaf cells through stomata, it creates tension that pulls the water column upward. Water molecules remain connected (cohesion) and adhere to xylem walls (adhesion), preventing the column from breaking.\n\n"
        "Xylem vessels are perfectly adapted for this role: dead cells form a hollow, continuous tube; lignified walls provide strength; absence of end walls allows unobstructed flow."
    ),
    (
        "SECTION 2: HOW IS VASCULAR TISSUE ARRANGED IN MONOCOTS AND DICOTS?",
        "What is the difference between monocotyledonous and dicotyledonous plants?\n"
        "How are vascular bundles arranged in a monocot stem compared to a dicot stem?\n"
        "How is the arrangement in roots different from stems?\n"
        "Draw and label cross-sections of monocot and dicot stems and roots.",
        "Monocots (e.g. maize) have one cotyledon, parallel leaf venation and fibrous root systems. Dicots (e.g. bean, sunflower) have two cotyledons, net-like venation and a tap root system.\n\n"
        "In monocot stems, vascular bundles are scattered throughout the ground tissue. In dicot stems, vascular bundles are arranged in a ring near the outside. In both cases, each vascular bundle contains xylem (inner) and phloem (outer).\n\n"
        "In dicot roots, xylem forms a central star shape with phloem positioned between the arms. In monocot roots, xylem and phloem alternate around the centre. The central xylem in dicot roots provides structural strength for anchorage."
    ),
    (
        "SECTION 3: WHAT FACTORS AFFECT TRANSPIRATION AND WHY DOES IT MATTER?",
        "What is transpiration and where does it occur?\n"
        "What four environmental factors affect the rate of transpiration?\n"
        "Explain the mechanism by which each factor increases or decreases transpiration.\n"
        "How can farmers use knowledge of transpiration to protect crops?",
        "Transpiration is the loss of water vapour from a plant, mainly through stomata in the leaf surface. It drives the upward movement of water through xylem and helps cool the plant.\n\n"
        "Four factors affect transpiration rate:\n"
        "• Temperature: higher temperature increases the kinetic energy of water molecules, increasing evaporation rate.\n"
        "• Wind speed: moving air removes the humid layer around stomata, maintaining a steep water potential gradient and increasing evaporation.\n"
        "• Light intensity: light causes stomata to open wider, allowing more water vapour to escape.\n"
        "• Humidity: lower humidity outside the leaf creates a steeper water potential gradient, increasing the rate of water vapour loss.\n\n"
        "Farmers can reduce transpiration by: mulching (reduces soil temperature), windbreaks (reduce wind speed), shade nets (reduce light intensity and temperature), and timing irrigation to early morning or evening when transpiration is lowest."
    ),
    (
        "SECTION 4: HOW IS FOOD TRANSPORTED IN PLANTS?",
        "What is translocation and which vessel carries it out?\n"
        "Define source and sink in the context of translocation.\n"
        "How does the ringing experiment provide evidence for phloem transport?\n"
        "How does phloem structure support translocation?",
        "Translocation is the movement of dissolved organic substances (mainly sucrose) through phloem from sources to sinks. Sources are regions of sugar production or release (mainly leaves carrying out photosynthesis). Sinks are regions of sugar use or storage (roots, growing tips, developing fruits and seeds).\n\n"
        "The ringing experiment provides evidence: removing a ring of bark (which includes phloem) from a stem causes swelling above the ring (sugars accumulate) and withering below (sugars cannot reach the roots). The xylem below the ring is unaffected because xylem lies deeper in the stem.\n\n"
        "Phloem sieve tube cells are living (unlike xylem), with sieve plates at their ends allowing sugar solution to flow. Companion cells supply the energy needed to actively load sugar into the phloem. Unlike xylem, phloem transports in both directions — up to growing tips and down to roots."
    ),
    (
        "SECTION 5: HOW DOES THE PLANT TRANSPORT SYSTEM EXPLAIN WILTING?",
        "Explain the complete pathway of water from soil to atmosphere.\n"
        "Why do some plants wilt faster than others under the same conditions?\n"
        "Connect all five learning objectives to explain the anchoring phenomenon.\n"
        "How does the transport system enable a plant to survive in varying conditions?",
        "The complete water pathway: Soil → (osmosis) → Root hair cells → (osmosis/diffusion) → Cortex → Xylem → (transpiration pull/cohesion-tension) → Stem xylem → Leaf xylem → Mesophyll cells → (evaporation) → Stomata → Atmosphere.\n\n"
        "Spinach wilts faster than mango because: spinach has large, thin leaves with many stomata exposed to wind and sun (high transpiration rate); its shallow root system reaches less soil water; mango has a deep tap root and waxy leaves with fewer stomata (lower transpiration rate).\n\n"
        "When transpiration rate exceeds the rate of water uptake through roots, cells lose turgor pressure and the plant wilts. In severe cases, stomata close to reduce water loss, but this also stops photosynthesis.\n\n"
        "The complete transport system (xylem for water, phloem for food) enables every cell to receive water and nutrients regardless of its distance from the soil or leaves — making the plant an integrated, coordinated organism."
    ),
]

# Biology META
_BIO_META = {
    "subject":    "Biology",
    "grade":      "Grade 10",
    "strand":     "2.0 Anatomy and Physiology of Plants",
    "substrand":  "2.2 Transport System in Plants",
    "lessons":    22,
    "author":     "Jackline Mwambere",
    "driving_question": (
        "Why do some crops like spinach wilt quickly during dry, windy days, "
        "while others like mango trees remain fresh and green?"
    ),
    "phenomenon": (
        "Spinach and sukuma wiki plants in a village garden wilt quickly on hot, "
        "windy days — even after being watered. Nearby mango and cassava plants "
        "remain green and upright under the same conditions."
    ),
    "substrand_overview_rows": [
        ("Subject",            "Biology"),
        ("Grade",              "Grade 10"),
        ("Strand",             "2.0 Anatomy and Physiology of Plants"),
        ("Sub-Strand",         "2.2 Transport System in Plants"),
        ("Author",             "Jackline Mwambere"),
        ("Number of Lessons",  "22"),
        ("Number of Periods",  "44"),
        ("Anchoring Phenomenon",
         "Spinach and sukuma wiki plants wilt quickly on hot, windy days even after watering, "
         "while nearby mango and cassava plants remain fresh. Why?"),
        ("Driving Question",
         "Why do some crops like spinach wilt quickly during dry, windy days, "
         "while others like mango trees remain fresh and green?"),
        ("Learning Outcomes: Knowledge",
         "a) Relate structures of the plant transport system to their functions\n"
         "b) Illustrate vascular tissue arrangement in monocots and dicots\n"
         "c) Demonstrate water and mineral uptake from roots to leaves\n"
         "d) Demonstrate factors affecting transpiration rate\n"
         "e) Describe translocation of manufactured food"),
        ("Learning Outcomes: Skills",
         "- Conduct investigations on transport, transpiration and translocation\n"
         "- Draw and label diagrams of plant transport structures\n"
         "- Collect, record and interpret experimental data\n"
         "- Apply knowledge to real farming challenges"),
        ("Learning Outcomes: Attitudes",
         "- Appreciate the importance of plant transport to food security\n"
         "- Show curiosity and care with living materials\n"
         "- Value teamwork and honest recording in investigations"),
        ("Core Competencies",
         "Digital literacy · Collaboration/Communication · Critical thinking · "
         "Self-efficacy · Learning to learn"),
        ("Core Values",
         "Curiosity · Responsibility · Respect · Care and Compassion · "
         "Excellence"),
        ("Assessment",
         "Formative: observation, discussion, diagrams, practical reports, summary table\n"
         "Summative: Final Explanation document"),
        ("Resources",
         "Live plant specimens (spinach, maize, bean, mango leaf); microscopes/hand lens; "
         "dialysis tubing; food dye; Khan Academy videos; PhET simulations"),
    ],
    "summary_table_headers": [
        "Lesson", "Learner Activities", "Key Understanding Built",
        "Connection to Driving Question", "DQB / Model Evolution"
    ],
    "summary_table_rows": _BIO_SUMMARY_ROWS,
    "summary_instructions": (
        "Use this table to track your learning journey across all 22 lessons. "
        "For each lesson, record: what you did, what you understood, how it connects "
        "to the driving question, and how your Driving Question Board and plant model evolved. "
        "Your completed Summary Table is evidence of your scientific thinking."
    ),
    "final_explanation_sections": _BIO_FE_SECTIONS,
    "final_explanation_rubric": {
        "headers": ["Criterion", "Beginning (1)", "Developing (2)", "Proficient (3)", "Advanced (4)"],
        "rows": [
            ("1. Water Transport",
             "Names xylem but cannot explain how water moves",
             "Describes osmosis and xylem but links are incomplete",
             "Explains osmosis, transpiration pull and cohesion-tension correctly",
             "Connects all forces with clear diagrams and accurate scientific vocabulary"),
            ("2. Vascular Structure",
             "Cannot distinguish monocot from dicot",
             "Identifies one difference between monocot and dicot",
             "Accurately describes vascular arrangement in stems and roots for both types",
             "Draws labelled cross-sections with correct tissue positions and explains why arrangements differ"),
            ("3. Transpiration",
             "Defines transpiration but cannot identify factors",
             "Lists factors but explanations are partial",
             "Explains mechanism of each factor correctly; links to phenomenon",
             "Includes quantitative reasoning; connects to farming applications and phenomenon"),
            ("4. Translocation",
             "Confuses xylem and phloem functions",
             "States that phloem carries sugar but cannot explain source/sink",
             "Explains source, sink, and ringing experiment evidence correctly",
             "Integrates translocation with water transport to show the complete dual-system model"),
            ("5. Phenomenon Explanation",
             "Cannot connect transport system to wilting",
             "Makes partial connection to wilting but misses key factors",
             "Explains why spinach wilts faster using transpiration and xylem concepts",
             "Complete, evidence-based explanation using all 5 objectives; proposes farming solutions"),
        ],
    },
    "lessons_data": _BIO_LESSONS,
}

# ═══════════════════════════════════════════════════════════════════════════════
# META — Physics: Moments and Equilibrium (6 lessons)
# ═══════════════════════════════════════════════════════════════════════════════

_PHY_SLO_K = (
    "- Define centre of gravity for regular and irregular objects\n"
    "- Identify the states of equilibrium (stable, unstable, neutral)\n"
    "- Explain the principle of moments\n"
    "- Describe moment of a force, torque, and couple\n"
    "- Explain moment about one and two points of support\n"
    "- State how forces are resolved in equilibrium situations\n"
    "- Outline applications of moments and stability in everyday life"
)
_PHY_SLO_S = (
    "- Determine the centre of gravity of regular and irregular objects through practical activities\n"
    "- Calculate the moment of a force about a point\n"
    "- Apply the principle of moments to solve numerical and practical problems\n"
    "- Demonstrate the turning effect of forces using simple apparatus\n"
    "- Carry out investigations to determine factors affecting the stability of objects"
)
_PHY_SLO_A = (
    "- Appreciate the importance of moments and stability in daily life (e.g., transport, structures)\n"
    "- Demonstrate curiosity and creativity during practical investigations\n"
    "- Show teamwork and collaboration when carrying out experiments\n"
    "- Develop honesty and integrity in recording and presenting results"
)

def _phy_lesson(num, title, inquiry, know, skills, attit, purpose, materials, safety, p1):
    return {
        "number": num, "title": title,
        "inquiry_question": inquiry,
        "slo_knowledge": know, "slo_skills": skills, "slo_attitudes": attit,
        "overview_purpose": purpose,
        "materials": materials, "safety": safety,
        "period1_heading": "Period 1 (40 minutes)",
        "period1_table": p1,
        "period2_heading": "Period 2 (40 minutes)",
        "period2_table": [],
        "reflections": [],
    }

_PHY_LESSONS = [
    _phy_lesson(
        1, "Introduction to the Phenomenon",
        "Why do some objects balance easily while others topple, even when they seem similar?",
        "- Recall that forces can cause objects to rotate or balance\n- Identify the driving question for the unit",
        "- Observe and record balance/toppling behaviour; draw an initial model showing where balance occurs",
        "- Show curiosity about balance and stability in everyday objects",
        "Launches the unit phenomenon. Students observe balance and toppling in real objects, generate questions, and produce initial models.",
        "Ruler; stones or small weights; a wheelbarrow or photograph of one; Driving Question Board; blank paper",
        "Ensure stones/weights are handled safely; no sharp edges on improvised pivots.",
        [
            _pr("Observe a ruler balanced at different points with a stone; record what happens when the stone moves",
                "Ruler and small stone or eraser as pivot; demonstration setup",
                "Pose the phenomenon: 'Why do some objects topple while others stay stable?' — show without explaining",
                "Think–Pair–Share: individual observation → partner discussion → whole-class share",
                "Exit ticket: 'One thing I observed about balance today and one question I still have'"),
            _pr("Draw initial model: where does balance occur and why does an object topple?",
                "Blank A4 paper; large class diagram for reference",
                "Prompt: 'Draw what you think is happening when the ruler balances and when it tips'",
                "Pair-share diagrams; identify agreements and disagreements about where balance occurs",
                "Collect initial model diagrams for formative comparison at end of unit"),
            _pr("Contribute questions to the Driving Question Board",
                "Driving Question Board (poster or whiteboard section); sticky notes",
                "Facilitate DQB creation; group questions by theme (balance, forces, everyday objects)",
                "Model 'I notice… I wonder…' sentence stems to scaffold question generation",
                "Count and categorise student questions to inform lesson sequence"),
            _pr("Discuss: what real-life situations involve balance? (wheelbarrows, ladders, vehicles)",
                "Photographs or sketches of wheelbarrow, ladder, tall vehicle, see-saw",
                "Elicit prior knowledge without correcting; accept all ideas at this stage",
                "Record on KWL chart; connect to driving question",
                "Oral probe: 'Name one situation where balance matters and guess why'"),
            _pr("Update initial model: add arrows showing forces and where weight seems to act",
                "Initial model from earlier in the lesson",
                "Explain models will be revised as evidence accumulates each lesson",
                "Students share updated models with partners; note what is uncertain",
                "Collect models; note common misconceptions for future lessons"),
        ],
    ),
    _phy_lesson(
        2, "Centre of Gravity",
        "Where is the balancing point of an object, and what determines it?",
        "- Define centre of gravity as the point where an object's entire weight appears to act\n- Locate the centre of gravity of regular shapes by symmetry\n- Determine the centre of gravity of irregular shapes by experiment",
        "- Balance objects on a pivot to find the centre of gravity\n- Use the plumb-line method for irregular cut-out shapes\n- Record and explain experimental results",
        "- Show patience and precision when locating balance points\n- Appreciate that the centre of gravity concept applies to all objects including the human body",
        "Students investigate the concept of centre of gravity through hands-on balancing activities with regular and irregular shapes.",
        "Ruler; pencil as pivot; cardboard cut-outs (regular and irregular); string; small weight (plumb bob); pins or needles; retort stand",
        "Take care with pins/needles; ensure retort stands are stable.",
        [
            _pr("Balance a regular cardboard rectangle on a pencil; mark the balance line; repeat from different direction to find COG",
                "Cardboard rectangles; pencil pivot; marker pen",
                "Demonstrate first; then guide students: 'Balance the shape — the point where all balance lines cross is the COG'",
                "Groups share COG locations; discuss: 'Is the COG always in the centre for regular shapes?'",
                "Quick check: can students predict COG of a square before testing?"),
            _pr("Use plumb-line method to find COG of irregular cardboard shapes",
                "Irregular cardboard cut-outs; string and small weight; pins; retort stand or clip",
                "Model the procedure: hang shape, draw plumb line; repeat from second point; intersection = COG",
                "Groups compare irregular COG locations; discuss: 'Is the COG always inside the object?'",
                "Observation: accuracy of plumb lines; can students explain the method in their own words?"),
            _pr("Investigate: can the COG be outside the object? (e.g., a ring shape or L-shape)",
                "L-shaped or ring-shaped cardboard cut-outs",
                "Challenge question: 'Draw where you think the COG is before testing — then test and compare'",
                "Discuss findings as a class; link to everyday objects (boomerangs, rings, hollow objects)",
                "Exit ticket: sketch a shape and mark its approximate COG, explain your reasoning"),
            _pr("Update model: mark COG on the initial balance model from Lesson 1",
                "Initial model diagrams from Lesson 1",
                "Prompt: 'Now that you know about COG, update your model to show where weight acts'",
                "Pair discussion: 'What changed in your model? What do you now understand that you didn't before?'",
                "Observe model updates; check that students connect COG to balance point"),
            _pr("Solve 2–3 practice problems: predict COG location for given shapes; verify by experiment",
                "Worksheet with shape diagrams; cardboard cut-outs to test predictions",
                "Circulate and ask probing questions; correct misconceptions individually",
                "Peer-check answers; discuss any disagreements as a class",
                "Written responses: 'Define COG in your own words and describe how to find it'"),
        ],
    ),
    _phy_lesson(
        3, "States of Equilibrium",
        "Why do some objects return to their original position after being tilted, while others fall?",
        "- Define stable, unstable, and neutral equilibrium\n- Explain why the position of the centre of gravity and the size of the base determine stability\n- Classify everyday objects by their state of equilibrium",
        "- Demonstrate all three states of equilibrium using simple objects\n- Relate stability to COG height and base area\n- Apply criteria to classify objects as stable, unstable, or neutral",
        "- Appreciate safety implications of stability in buildings, vehicles, and furniture\n- Show systematic thinking when classifying objects",
        "Students investigate the three states of equilibrium and connect stability rules to real-life objects.",
        "Wooden blocks of different base sizes; cone; ball; cylinder; ruler; pivot; photographs of vehicles and buildings",
        "No significant hazards; ensure blocks do not topple onto hands.",
        [
            _pr("Tilt a wide-based block slightly and release; then tilt a narrow-based block — observe and record what happens",
                "Wide-based and narrow-based wooden blocks; flat surface",
                "Ask: 'What will happen when I release this?' before each demonstration; elicit predictions",
                "Discuss: 'What is different about the two blocks? What causes one to return and the other to fall?'",
                "Oral questioning: can students describe what they observed using 'COG' and 'base'?"),
            _pr("Demonstrate neutral equilibrium using a ball on a flat surface; compare with stable and unstable examples",
                "Ball; cone (balanced on tip); cylinder on its side",
                "Guide students to see: stable returns, unstable topples, neutral stays in new position",
                "Three-way sort: students categorise given objects into stable/unstable/neutral with justification",
                "Exit ticket: sketch three objects and label each state; explain using COG and base area"),
            _pr("Investigate: how does base width affect stability? Change base area while keeping height constant",
                "Cardboard boxes with variable base inserts; weights to add to tops",
                "Challenge: 'Find the minimum base width needed to keep this object stable when tilted 20°'",
                "Groups share findings; build rule: wider base + lower COG = more stable",
                "Record rule in notebooks; teacher checks phrasing for scientific accuracy"),
            _pr("Examine photographs: identify states of equilibrium in vehicles, furniture, cranes, and human posture",
                "Printed photographs or projected images of wide-based trucks, tall cranes, gymnasts",
                "Prompt students to apply stability rules to each real-life case",
                "Class discussion: 'Why do double-decker buses not topple? Why do gymnasts lower their bodies?'",
                "Peer assessment: students swap notebooks and check each other's classifications"),
            _pr("Update DQB and model: add stability conditions to the initial balance diagram",
                "DQB poster; initial model diagrams",
                "Prompt: 'How does what we learned today help answer the driving question about toppling?'",
                "Students add sticky notes to DQB marking evidence gathered",
                "Review DQB as class; teacher notes which sub-questions have been answered"),
        ],
    ),
    _phy_lesson(
        4, "Moment of a Force",
        "What determines how easily a force can rotate an object about a pivot?",
        "- Define moment of a force (torque) as force × perpendicular distance from pivot\n- State the unit of moment (N·m)\n- Explain that increasing force or distance increases the turning effect",
        "- Calculate the moment of a force given force and perpendicular distance\n- Design investigations to show how distance affects turning effect\n- Construct and interpret moment equations",
        "- Appreciate the practical value of moments in tools (spanners, levers, door handles)\n- Show accuracy and care when measuring distances",
        "Students discover that turning effect depends on both force magnitude and distance from pivot through hands-on ruler investigations.",
        "Metre rule; pivot (knife edge or pencil); known weights (100 g, 200 g, 500 g); ruler for measuring distances; graph paper",
        "Ensure pivot is stable; weights should not be dropped.",
        [
            _pr("Attach a 200 g weight at different distances from pivot; observe and record turning effect",
                "Metre rule; knife-edge pivot; 200 g weight; ruler",
                "Demonstrate setup; ask: 'Where does the weight have the greatest turning effect?'",
                "Students record force, distance, and qualitative turning effect in results table",
                "Can students identify the trend: further = greater turning? Ask for explanation."),
            _pr("Calculate moment = force × distance for each position; record in table; identify pattern",
                "Results table; calculator",
                "Introduce formula: Moment (N·m) = F (N) × d (m); work through first example together",
                "Students complete calculations; compare values across positions",
                "Quick quiz: given F and d, calculate moment; given moment and d, find F"),
            _pr("Investigate: does the same moment result from different F × d combinations? (e.g., 2 N at 0.5 m = 4 N at 0.25 m)",
                "Various weights; metre rule and pivot",
                "Students design their own F × d combinations to achieve a target moment of 0.4 N·m",
                "Groups share their combinations; confirm that F × d = constant for same turning effect",
                "Written explanation: 'Why can a long spanner remove a tight bolt more easily than a short one?'"),
            _pr("Apply moments to door handles and lever tools: calculate force needed at various distances",
                "Photographs or diagrams of spanner, crowbar, door handle at different positions",
                "Pose problem: 'A bolt requires 12 N·m to loosen. What force is needed with a 0.3 m spanner?'",
                "Students solve 2–3 application problems; peer-check answers",
                "Exit ticket: word problem requiring moment calculation"),
            _pr("Update model: add moment arrows to the balance diagram; label F and d",
                "Initial model diagrams; ruler; pencil",
                "Prompt students to show on their diagrams where turning occurs and how it is calculated",
                "Pair-share updated models; identify improvements",
                "Collect updated models; assess whether moment concept is correctly applied"),
        ],
    ),
    _phy_lesson(
        5, "Principle of Moments",
        "What conditions must be met for an object to be perfectly balanced by unequal forces?",
        "- State the principle of moments: sum of clockwise moments = sum of anticlockwise moments for equilibrium\n- Apply the principle to solve problems involving one and two pivots",
        "- Set up a balanced beam with unequal weights at different distances\n- Calculate unknown forces or distances using the principle of moments\n- Verify the principle experimentally",
        "- Value precision in measurement as the key to verifying a scientific principle\n- Appreciate how the principle underpins weighing scales and balance beams",
        "Students discover the principle of moments by balancing unequal loads on a metre rule and verify it mathematically.",
        "Metre rule; knife-edge pivot; weights (100 g, 200 g, 500 g); ruler; string for suspending weights",
        "Ensure pivot is stable; do not lean over the balanced beam.",
        [
            _pr("Balance a 200 g weight on one side with a 400 g weight on the other; measure required distances",
                "Metre rule; knife-edge pivot; 200 g and 400 g weights",
                "Ask students to predict distances before experimenting; then test predictions",
                "Record clockwise moment and anticlockwise moment for each trial; compare",
                "Can students articulate why the heavier weight must be closer to the pivot?"),
            _pr("Tabulate results for 5 different weight combinations; calculate both moments; compare",
                "Results table; calculator",
                "Guide discovery: 'What do you notice about the two moment values each time?'",
                "Students state the principle of moments in their own words",
                "Quick written check: state the principle of moments using correct terminology"),
            _pr("Apply principle to solve: unknown weight problems and unknown distance problems",
                "Worksheet with 4 structured problems",
                "Model one example of each type; students complete remaining problems independently",
                "Peer-check solutions; discuss common errors",
                "Formative quiz: 3 problems covering F×d = F×d in varied contexts"),
            _pr("Investigate moments about two supports: beam resting on two pivots with central load",
                "Metre rule; two supports at different positions; central weight",
                "Challenge: 'If the beam has supports at 20 cm and 80 cm, and a 5 N weight is at 50 cm, find reaction forces'",
                "Groups work through guided steps; share solutions",
                "Exit ticket: sketch a balanced beam with two supports; label forces and distances"),
            _pr("Update DQB and model: show that balanced = equal moments; link to weighing scales",
                "DQB poster; model diagrams; photographs of a beam balance",
                "Prompt: 'How does a beam balance use the principle of moments to measure mass?'",
                "Students add new evidence to DQB; revise models to show moment arrows and balance condition",
                "Teacher reviews DQB with class; confirm which questions are now answered"),
        ],
    ),
    _phy_lesson(
        6, "Torque, Couple, and Applications of Stability",
        "How do engineers apply knowledge of moments and stability to design safe structures and tools?",
        "- Define torque as the turning effect of a force and couple as two equal, opposite, non-collinear forces\n- Explain how stability principles are applied in vehicles, buildings, and everyday tools\n- Construct a complete final model explaining the phenomenon",
        "- Identify couples in everyday objects (steering wheel, bottle cap, spanner)\n- Analyse stability of objects using COG and base area\n- Construct a complete written explanation linking all unit concepts",
        "- Appreciate the role of physics in engineering and safety design\n- Show confidence in applying unit concepts to unfamiliar real-life situations",
        "Consolidation lesson: students connect torque, couple, moments, and stability to solve real engineering problems and construct their final explanation.",
        "Photographs/models of wheelbarrow, vehicle, crane, steering wheel; student Summary Tables; DQB",
        "No specific hazards.",
        [
            _pr("Examine a steering wheel diagram and a bottle cap: identify the two forces forming a couple",
                "Diagram of steering wheel; bottle cap; pair of equal and opposite force arrows",
                "Introduce 'couple': two equal forces in opposite directions with different lines of action; no net force but net torque",
                "Students sketch their own couple example from daily life and label forces",
                "Can students distinguish between a single moment and a couple? Oral probe."),
            _pr("Analyse stability of given objects: double-decker bus, crane, wheelbarrow, standing human",
                "Photographs of each; worksheets with COG diagrams",
                "Guide analysis: 'Locate the COG, identify the base, determine if the object is stable under stated conditions'",
                "Groups present analysis to class; class gives feedback using stability criteria",
                "Written assessment: analyse a new object not previously discussed"),
            _pr("Revisit the driving question: 'Why do some objects balance easily while others topple?' — write a class explanation",
                "DQB poster; all model diagrams; Summary Table drafts",
                "Facilitate class construction of a complete explanation citing unit evidence",
                "Students evaluate the class explanation against the unit SLOs",
                "Individual written task: draft personal Final Explanation paragraph connecting COG, stability, moments, and couples"),
            _pr("Review Summary Table: ensure all 6 lessons are recorded with evidence and connections",
                "Individual Summary Tables",
                "Students complete any missing rows; teacher circulates to check accuracy",
                "Peer review Summary Tables for completeness and scientific accuracy",
                "Teacher reviews sample Summary Tables; provide written feedback"),
            _pr("Reflect on unit: what new understanding have you built? How will you approach the Final Explanation?",
                "Final Explanation task description; rubric",
                "Introduce the Final Explanation document and rubric; students self-assess readiness",
                "Class discussion: which section of the Final Explanation will be most challenging and why?",
                "Exit ticket: 'The most important thing I learned in this unit is… because…'"),
        ],
    ),
]

_PHY_SUMMARY_ROWS = [
    (1, "Observed balance and toppling; drew initial model; posted questions on DQB",
        "All objects have a balance point; moving a load changes balance",
        "Introduces the phenomenon: why do objects topple?",
        "DQB created; initial model drawn showing balance point"),
    (2, "Located COG of regular and irregular shapes by balancing and plumb-line method",
        "COG is where all weight appears to act; can be outside the object for irregular shapes",
        "COG determines where an object balances — key to understanding toppling",
        "Model updated: COG marked on balance diagram"),
    (3, "Demonstrated stable, unstable, and neutral equilibrium; applied criteria to real objects",
        "Stability depends on COG height and base area; wider base and lower COG = more stable",
        "Explains why wide-based objects are stable and tall narrow ones topple",
        "DQB: evidence added; model updated with stability conditions"),
    (4, "Investigated turning effect at different distances; calculated moment = F × d",
        "Moment depends on force AND distance; longer lever = greater turning effect",
        "Turning effect of forces drives the physics of balance and toppling",
        "Model updated: moment arrows added with F and d labels"),
    (5, "Balanced unequal weights; verified principle of moments experimentally",
        "For equilibrium: total clockwise moments = total anticlockwise moments",
        "Principle of moments explains how unequal forces can maintain balance",
        "Model updated: moment balance condition shown; DQB sub-questions answered"),
    (6, "Identified couples; analysed stability of real objects; drafted Final Explanation",
        "Torque, couple, COG, and stability principles all link to explain the phenomenon",
        "Complete understanding: objects balance or topple depending on COG, base, and moments",
        "Final model complete; DQB fully answered; Summary Table reviewed"),
]

_PHY_FE_SECTIONS = [
    ("1. Centre of Gravity and Stability",
     "Explain what centre of gravity is, how it is determined, and how it relates to stability. "
     "Include the three states of equilibrium with diagrams.\n\n"
     "Guiding Questions:\n- How do you find the COG of a regular shape? An irregular shape?\n"
     "- What is the difference between stable, unstable, and neutral equilibrium?\n"
     "- How do COG position and base area determine stability?",
     "Every object has a centre of gravity — the point where its entire weight appears to act. "
     "For regular shapes this lies at the centre of symmetry; for irregular shapes it is found "
     "experimentally using the plumb-line method. An object is stable if, when slightly tilted, "
     "the COG falls back inside the base and the object returns to its original position. "
     "Unstable equilibrium occurs when any tilt moves the COG outside the base, causing toppling. "
     "Neutral equilibrium occurs when the COG stays at the same height regardless of position. "
     "Wider base and lower COG both increase stability."),
    ("2. Moment of a Force",
     "Define moment of a force and explain what factors affect its magnitude. Include worked calculations.\n\n"
     "Guiding Questions:\n- What is the formula for moment of a force?\n"
     "- How does increasing distance from the pivot affect the turning effect?\n"
     "- Give two real-life examples where moments are used to make work easier.",
     "The moment of a force is the turning effect produced by a force about a pivot. "
     "It is calculated as: Moment (N·m) = Force (N) × Perpendicular distance from pivot (m). "
     "Increasing either the force or the distance increases the moment. "
     "This is why a long spanner can loosen a tight bolt more easily than a short one — "
     "the same force applied at greater distance produces a larger moment. "
     "Door handles are placed far from the hinges for the same reason."),
    ("3. Principle of Moments",
     "State the principle of moments and apply it to solve a balance problem. Show your working.\n\n"
     "Guiding Questions:\n- State the principle of moments in words.\n"
     "- Show how the principle explains why a lighter person can balance a heavier person on a see-saw.\n"
     "- Solve: a 300 N force acts 0.4 m from a pivot. What force at 0.6 m balances it?",
     "For an object in equilibrium, the sum of all clockwise moments about any pivot equals "
     "the sum of all anticlockwise moments. This is the principle of moments. "
     "On a see-saw, a lighter person can balance a heavier one by sitting further from the pivot, "
     "increasing their moment. In beam balances, the principle allows unknown masses to be "
     "determined by adjusting distances. Solution: 300 × 0.4 = F × 0.6 → F = 120 ÷ 0.6 = 200 N."),
    ("4. Torque, Couple, and Engineering Applications",
     "Explain torque and couple. Describe how engineers use moments and stability principles in design.\n\n"
     "Guiding Questions:\n- What is a couple and how does it differ from a single moment?\n"
     "- Why are double-decker buses designed with heavy engines at the base?\n"
     "- Describe one engineering application of the principle of moments.",
     "Torque is the rotational effect of a force about an axis. A couple consists of two equal, "
     "opposite, non-collinear forces that produce rotation without translation. Steering wheels "
     "and bottle caps are opened using couples. Engineers lower the centre of gravity of vehicles "
     "by placing heavy components (engines, batteries) near the ground, widening the wheelbase, "
     "and designing low-profile bodies — all to increase the range of tilt before the COG falls "
     "outside the base. Cranes counterbalance heavy loads using the principle of moments."),
    ("5. Phenomenon Explanation",
     "Answer the driving question using all evidence gathered in this unit.\n\n"
     "Driving Question: Why do some objects balance easily while others topple, even when they seem similar?\n\n"
     "Use concepts: centre of gravity, states of equilibrium, moment of a force, principle of moments, couple.",
     "Objects balance or topple depending on the position of their centre of gravity relative to "
     "their base of support. When an object is tilted, if the vertical line through the COG "
     "falls within the base, the resulting moment restores the object to equilibrium. If the COG "
     "falls outside the base, the unbalanced moment causes toppling. Objects with a low COG and "
     "wide base are more stable. Two objects can look similar but have different COG heights due "
     "to the distribution of their mass — this is why a hollow cylinder tips more easily than a "
     "solid one of the same dimensions. Engineers exploit these principles in every structure "
     "they design: from wide-based stools and vehicles with lowered chassis to cranes whose "
     "counterweights apply equal and opposite moments to maintain equilibrium."),
]

_PHY_META = {
    "subject": "Physics",
    "grade": "Grade 10",
    "substrand": "Sub-Strand 1.5: Moments and Equilibrium",
    "lessons": 6,
    "driving_question": "Why do some objects balance easily while others topple, even when they seem similar?",
    "substrand_overview_rows": [
        ("Phenomenon", "A wheelbarrow, bicycle, or person carrying a heavy load unevenly — why do some objects balance while others topple?"),
        ("Driving Question", "Why do some objects balance easily while others topple, even when they seem similar?"),
        ("Sub-Strand SLOs — Knowledge", _PHY_SLO_K),
        ("Sub-Strand SLOs — Skills", _PHY_SLO_S),
        ("Sub-Strand SLOs — Attitudes/Values", _PHY_SLO_A),
        ("Number of Lessons", "6 lessons (12 periods of 40 minutes each)"),
        ("Core Competencies", "Communication and Collaboration · Critical Thinking and Problem Solving · Self-efficacy · Digital Literacy · Learning to Learn"),
        ("Core Values", "Curiosity · Responsibility · Integrity · Excellence · Teamwork"),
        ("Assessment", "Formative: observation, oral questioning, calculations, practical reports, summary table\nSummative: Final Explanation document"),
        ("Resources", "Metre rule; knife-edge pivot; weights (100–500 g); cardboard cut-outs; plumb bob; Khan Academy — Torque and Balance; PhET Balancing Act simulation"),
    ],
    "summary_table_headers": [
        "Lesson", "What I Did", "Key Understanding Built",
        "Connection to Driving Question", "Model / DQB Evolution"
    ],
    "summary_table_rows": _PHY_SUMMARY_ROWS,
    "summary_instructions": (
        "Use this table to track your learning across all 6 lessons. "
        "For each lesson record: what you did, what you understood, how it connects to the driving question, "
        "and how your model and DQB evolved. Your completed Summary Table is evidence of your scientific thinking."
    ),
    "final_explanation_sections": _PHY_FE_SECTIONS,
    "final_explanation_rubric": {
        "headers": ["Criterion", "Beginning (1)", "Developing (2)", "Proficient (3)", "Advanced (4)"],
        "rows": [
            ("1. Centre of Gravity",
             "Cannot define COG or locate it",
             "Defines COG but cannot explain how to find it experimentally",
             "Correctly defines COG, describes both methods, and links to stability",
             "Explains COG with labelled diagrams; connects to phenomenon with specific examples"),
            ("2. States of Equilibrium",
             "Cannot distinguish stable from unstable",
             "Names the three states but explanations are incomplete",
             "Correctly explains all three states with COG and base area criteria",
             "Applies all three states to novel real-life examples with full reasoning"),
            ("3. Moments and Principle",
             "Cannot define moment or apply formula",
             "States formula but makes errors in calculation or application",
             "Correctly calculates moments and applies the principle of moments to problems",
             "Solves multi-step problems; explains principle with worked examples and diagrams"),
            ("4. Torque, Couple and Applications",
             "Cannot describe torque or couple",
             "Describes torque but confuses couple with a single moment",
             "Correctly defines couple; gives two real-life engineering applications",
             "Analyses engineering designs using torque, couple, COG, and stability with quantitative reasoning"),
            ("5. Phenomenon Explanation",
             "Cannot connect unit concepts to the driving question",
             "Makes partial connection but misses key factors",
             "Explains the phenomenon using COG, stability, and moments correctly",
             "Complete evidence-based explanation covering all 5 objectives; proposes novel engineering solution"),
        ],
    },
    "lessons_data": _PHY_LESSONS,
}
