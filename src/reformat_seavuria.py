"""
Reformat Seavuria Lesson Plan documents into standard CBE format.

Reads the 3 COMPLETE source documents and produces one .docx per sub-strand
in the standard 5-section, 5-column-table CBE format.

Standard format per lesson:
  A. Specific Learning Outcomes
  B. Overview (Key Inquiry Question, Purpose, Materials, Safety)
  C. Lesson Implementation Framework (5-column landscape table, 2 periods)
  D. Teacher Reflection Prompts
  E. Summary Table Prompt
"""

import re
import copy
from pathlib import Path
from typing import Optional
from lxml import etree

from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ── paths ────────────────────────────────────────────────────────────────────
SRC_DIR  = Path("data/raw/Seavuria Lesson Plans")
OUT_DIR  = Path("data/outputs/Seavuria_Reformatted")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SOURCE_FILES = {
    "chemistry": SRC_DIR / "Chemistry_Chemical_Bonding_CBE_LessonSequence_COMPLETE.docx",
    "mathematics": SRC_DIR / "Mathematics_Quadratic_Equations_CBE_LessonSequence_COMPLETE.docx",
    "physics": SRC_DIR / "Physics_Temperature_Thermal_Expansion_CBE_LessonSequence_COMPLETE.docx",
}

OUTPUT_FILES = {
    "chemistry":    OUT_DIR / "Chemistry_10_SubStrand1.4_ChemicalBonding_CBE_Reformatted.docx",
    "mathematics":  OUT_DIR / "Mathematics_10_SubStrand1.3_QuadraticEquations_CBE_Reformatted.docx",
    "physics":      OUT_DIR / "Physics_10_SubStrand1.4_TemperatureThermalExpansion_CBE_Reformatted.docx",
}

META = {
    "chemistry": {
        "subject": "Chemistry",
        "grade": "Grade 10",
        "strand": "Strand 1.0: Inorganic Chemistry",
        "substrand": "Sub-Strand 1.4: Chemical Bonding",
        "lessons": 13,
        "periods": 26,
        "phenomenon": 'A diamond and a graphite pencil tip are both made of pure carbon — yet diamond is the hardest natural substance and graphite is soft enough to write with. How can the same element behave so differently?',
        "driving_question": '"How do the bonds between atoms determine the properties and uses of substances?"',
    },
    "mathematics": {
        "subject": "Mathematics",
        "grade": "Grade 10",
        "strand": "Strand 1.0: Numbers and Algebra",
        "substrand": "Sub-Strand 1.3: Quadratic Expressions and Equations",
        "lessons": 7,
        "periods": 14,
        "phenomenon": 'A harambee group plans to raise Ksh 12,000. Members share the cost equally, but 3 members fail to show up — so the remaining members each pay Ksh 200 more. How many people were originally in the group?',
        "driving_question": '"How can we use quadratic equations to model, solve, and make sense of real-life problems in our communities?"',
    },
    "physics": {
        "subject": "Physics",
        "grade": "Grade 10",
        "strand": "Strand 1.0: Mechanics and Thermal Physics",
        "substrand": "Sub-Strand 1.4: Temperature and Thermal Expansion",
        "lessons": 6,
        "periods": 12,
        "phenomenon": 'A tightly sealed metal sufuria lid that won\'t budge — but after running hot water over it for 10 seconds, it opens easily. Also: a glass bottle full of water placed in a freezer cracks overnight.',
        "driving_question": '"Why do materials change size when temperature changes — and how do engineers use this to keep us safe?"',
    },
}

# ── notes collected during processing ────────────────────────────────────────
NOTES: list[str] = []


# ── helpers: document element iteration ─────────────────────────────────────
def iter_block_items(doc):
    """Yield (type, obj) for every paragraph and table in document order."""
    body = doc.element.body
    for child in body:
        tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        if tag == "p":
            from docx.text.paragraph import Paragraph
            yield "paragraph", Paragraph(child, doc)
        elif tag == "tbl":
            from docx.table import Table
            yield "table", Table(child, doc)


def is_impl_table(table) -> bool:
    """True if this is a 5-column implementation table."""
    if len(table.columns) != 5:
        return False
    header = table.rows[0].cells[0].text.strip()
    return "Learner" in header or "Experience" in header


def cell_text(cell) -> str:
    return "\n".join(p.text for p in cell.paragraphs if p.text.strip()).strip()


# ── parse a source document ───────────────────────────────────────────────────
def parse_source(doc_path: Path) -> list[dict]:
    """
    Returns a list of lesson dicts:
      {
        number, title, inquiry_question,
        slo_knowledge, slo_skills, slo_attitudes,
        overview_purpose, materials, safety,
        period1_table, period2_table,   ← list of (col0..col4) row tuples
        reflections,                    ← list of strings
        summary_prompt,                 ← string
        summary_table_rows,             ← list of row tuples from 4-col summary table
      }
    """
    doc = Document(doc_path)
    lessons = []
    current: Optional[dict] = None
    section = None
    impl_tables_for_current = []
    summary_tables_for_current = []
    buffer: list[str] = []

    # Only match headings that are clearly lesson banners (all-caps LESSON or numbered)
    LESSON_HEADING_RE = re.compile(r"^LESSON\s+(\d+)\s*[:–—]\s*(.*)", re.IGNORECASE)
    SECTION_RE = re.compile(r"^([A-E])\.\s+(.*)")

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
                    # Try inline first (e.g. "Key Inquiry Question: <text>")
                    inline = ln.split(":", 1)[1].strip() if ":" in ln else ""
                    if inline:
                        current["inquiry_question"] = inline
                    else:
                        # Try next line, but only if it doesn't look like a new label
                        next_ln = lines[i+1].strip() if i+1 < len(lines) else ""
                        if next_ln and not re.match(r"(Purpose|Safety|Materials|Duration|Supporting)", next_ln, re.I):
                            current["inquiry_question"] = next_ln
                elif re.match(r"Purpose in Storyline", ln, re.I) or re.match(r"Purpose:", ln, re.I):
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
                rows.append(tuple(cell_text(c) for c in row.cells))
            if not current["period1_table"]:
                current["period1_table"] = rows
            else:
                current["period2_table"] = rows
        # also save summary (4-col) tables
        for tbl in summary_tables_for_current:
            rows = []
            for row in tbl.rows[1:]:  # skip header
                rows.append(tuple(cell_text(c) for c in row.cells))
            if rows:
                current["summary_table_rows"] = rows

    def new_lesson(number, title):
        nonlocal current, section, impl_tables_for_current, summary_tables_for_current
        if current is not None:
            save_section()
            save_impl_tables()
            lessons.append(current)
        impl_tables_for_current = []
        summary_tables_for_current = []
        current = {
            "number": int(number),
            "title": title.strip(),
            "inquiry_question": "",
            "slo_knowledge": "",
            "slo_skills": "",
            "slo_attitudes": "",
            "overview_purpose": "",
            "materials": "",
            "safety": "",
            "period1_table": [],
            "period2_table": [],
            "period1_heading": "Period 1 (40 minutes)",
            "period2_heading": "Period 2 (40 minutes)",
            "reflections": [],
            "summary_prompt": "",
            "summary_table_rows": [],
        }
        section = None

    def is_summary_table(table) -> bool:
        """4-column table with lesson summary structure."""
        if len(table.columns) != 4:
            return False
        h0 = table.rows[0].cells[0].text.strip().lower()
        return "lesson" in h0 or "what we learned" in h0

    for kind, obj in iter_block_items(doc):
        if kind == "paragraph":
            text = obj.text.strip()
            if not text:
                continue
            style = obj.style.name if obj.style else ""
            style_l = style.lower()

            # Only trigger new_lesson on actual heading styles
            is_heading = "heading" in style_l
            m = LESSON_HEADING_RE.match(text)
            if m and is_heading:
                save_section()
                new_lesson(m.group(1), m.group(2))
                section = None
                buffer = []
                continue

            # Section headings (A. / B. / C. / D. / E.) within a lesson
            sm = SECTION_RE.match(text)
            if sm and current is not None and is_heading:
                save_section()
                section = sm.group(1).upper()
                buffer = []
                continue

            # Period headings (Heading 4)
            if "heading 4" in style_l and current is not None:
                if "PERIOD 1" in text.upper() or "Period 1" in text:
                    current["period1_heading"] = text
                elif "PERIOD 2" in text.upper() or "Period 2" in text:
                    current["period2_heading"] = text
                continue

            # Supporting driving question on lesson opener
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
            elif is_summary_table(obj) and current is not None and section == "E":
                summary_tables_for_current.append(obj)

    # finalise last lesson
    if current is not None:
        save_section()
        save_impl_tables()
        lessons.append(current)

    return lessons


# ── formatting helpers ────────────────────────────────────────────────────────
FONT_NAME  = "Calibri"
FONT_SIZE  = Pt(10)
HEAD_SIZE  = Pt(11)
TITLE_SIZE = Pt(13)

BLUE  = RGBColor(0x1F, 0x49, 0x7D)   # dark blue for section headings
TEAL  = RGBColor(0x1F, 0x7A, 0x8C)   # teal for period subheadings
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
DARK  = RGBColor(0x1F, 0x49, 0x7D)   # header row fill

COL_WIDTHS = [Inches(2.8), Inches(1.6), Inches(2.2), Inches(2.2), Inches(1.9)]  # total ~10.7" landscape
TOTAL_WIDTH = sum(COL_WIDTHS)


def _set_font(run, bold=False, size=None, color=None, name=FONT_NAME):
    run.font.name = name
    run.font.size = size or FONT_SIZE
    run.font.bold = bold
    if color:
        run.font.color.rgb = color


def _para_font(para, bold=False, size=None, color=None, align=None):
    for run in para.runs:
        _set_font(run, bold=bold, size=size, color=color)
    if align:
        para.alignment = align


def set_landscape(section):
    """Set a document section to landscape A4."""
    section.page_width  = Cm(29.7)
    section.page_height = Cm(21.0)
    section.left_margin   = Cm(1.27)
    section.right_margin  = Cm(1.27)
    section.top_margin    = Cm(1.27)
    section.bottom_margin = Cm(1.27)


def shade_cell(cell, hex_color: str):
    """Fill a table cell with a hex background color."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)


def set_col_widths(table, widths):
    for i, col in enumerate(table.columns):
        if i < len(widths):
            for cell in col.cells:
                cell.width = widths[i]


def add_impl_table(doc, period_heading: str, rows: list, notes_out: list, lesson_num: int, period_num: int):
    """Add a 5-column implementation table to the document."""
    HEADERS = ["Learner Experience", "Key Resources", "Teacher Moves", "Sensemaking Strategy", "Formative Assessment"]
    COL_COLORS = ["1F497D"] * 5  # all header cells same blue

    # Period subheading
    ph = doc.add_paragraph()
    ph.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = ph.add_run(period_heading)
    _set_font(r, bold=True, size=Pt(10), color=TEAL)
    ph.paragraph_format.space_before = Pt(4)
    ph.paragraph_format.space_after  = Pt(2)

    tbl = doc.add_table(rows=1, cols=5)
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.LEFT

    # Header row
    hdr_row = tbl.rows[0]
    for i, (cell, hdr) in enumerate(zip(hdr_row.cells, HEADERS)):
        shade_cell(cell, "1F497D")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(hdr)
        _set_font(r, bold=True, size=Pt(9), color=WHITE)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    # Data rows
    for r_idx, row_data in enumerate(rows):
        tr = tbl.add_row()
        bg = "EBF3FB" if r_idx % 2 == 0 else "FFFFFF"
        for c_idx, (cell, text) in enumerate(zip(tr.cells, row_data)):
            shade_cell(cell, bg)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(text)
            _set_font(run, size=Pt(9))
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after  = Pt(1)

            # flag empty implementation cells
            if c_idx == 0 and not text.strip():
                notes_out.append(
                    f"  Lesson {lesson_num}, Period {period_num}, row {r_idx+1}: "
                    "Learner Experience cell is EMPTY — content may need to be added."
                )

    set_col_widths(tbl, COL_WIDTHS)
    doc.add_paragraph()  # spacing after table


def add_heading(doc, text, level, color=BLUE):
    p = doc.add_paragraph()
    p.style = doc.styles["Normal"]
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after  = Pt(2)
    r = p.add_run(text)
    size = {1: TITLE_SIZE, 2: HEAD_SIZE, 3: Pt(10)}.get(level, Pt(10))
    _set_font(r, bold=True, size=size, color=color)
    return p


def add_body(doc, text, bullet=False):
    if not text or not text.strip():
        return
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    for ln in lines:
        # strip leading dash/bullet chars
        clean = re.sub(r"^[-•–—]\s*", "", ln)
        p = doc.add_paragraph(style="Normal")
        if bullet or ln.startswith(("-", "•", "–")):
            p.paragraph_format.left_indent = Inches(0.25)
            run = p.add_run("• " + clean)
        else:
            run = p.add_run(clean)
        _set_font(run, size=FONT_SIZE)
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after  = Pt(1)


def add_kv(doc, label, value):
    if not value or not value.strip():
        return
    p = doc.add_paragraph(style="Normal")
    r1 = p.add_run(label + ": ")
    _set_font(r1, bold=True, size=FONT_SIZE)
    r2 = p.add_run(value.strip())
    _set_font(r2, size=FONT_SIZE)
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after  = Pt(2)


def add_divider(doc):
    p = doc.add_paragraph("─" * 80, style="Normal")
    for r in p.runs:
        r.font.color.rgb = RGBColor(0xCC, 0xCC, 0xCC)
        r.font.size = Pt(8)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(2)


# ── build one output document ─────────────────────────────────────────────────
def build_docx(subject_key: str, lessons: list[dict], notes_out: list):
    meta = META[subject_key]
    doc  = Document()

    # Page layout — landscape throughout
    set_landscape(doc.sections[0])

    # ── Cover block ───────────────────────────────────────────────────────────
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = title_p.add_run(
        f"{meta['subject'].upper()}  |  {meta['grade']}  |  {meta['substrand']}"
    )
    _set_font(r, bold=True, size=Pt(14), color=BLUE)
    title_p.paragraph_format.space_after = Pt(4)

    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = sub_p.add_run(
        f"CBE Lesson Sequence  ·  {meta['lessons']} Lessons  ·  {meta['periods']} Periods"
    )
    _set_font(r, size=Pt(10), color=RGBColor(0x44, 0x44, 0x44))

    doc.add_paragraph()

    # Anchoring phenomenon + driving question box
    add_kv(doc, "Anchoring Phenomenon", meta["phenomenon"])
    add_kv(doc, "Main Driving Question", meta["driving_question"])
    add_divider(doc)

    # ── Lessons ───────────────────────────────────────────────────────────────
    for lesson in lessons:
        n   = lesson["number"]
        ttl = lesson["title"]

        # Lesson banner
        add_heading(doc, f"LESSON {n}:  {ttl}", level=1)
        if lesson["inquiry_question"]:
            add_kv(doc, "Key Inquiry Question", lesson["inquiry_question"])
        add_divider(doc)

        # ── A. Specific Learning Outcomes ─────────────────────────────────────
        add_heading(doc, "A.  Specific Learning Outcomes", level=2)

        if lesson["slo_knowledge"].strip():
            add_heading(doc, "Knowledge", level=3, color=TEAL)
            add_body(doc, lesson["slo_knowledge"])
        if lesson["slo_skills"].strip():
            add_heading(doc, "Skills", level=3, color=TEAL)
            add_body(doc, lesson["slo_skills"])
        if lesson["slo_attitudes"].strip():
            add_heading(doc, "Attitudes & Values", level=3, color=TEAL)
            add_body(doc, lesson["slo_attitudes"])

        # flag empty SLOs
        if not any([lesson["slo_knowledge"], lesson["slo_skills"], lesson["slo_attitudes"]]):
            notes_out.append(f"  Lesson {n} ({ttl}): All SLO sections (A) appear empty — check source parsing.")

        # ── B. Overview ────────────────────────────────────────────────────────
        add_heading(doc, "B.  Lesson Overview", level=2)
        if lesson["overview_purpose"]:
            add_kv(doc, "Purpose in Storyline", lesson["overview_purpose"])
        if lesson["materials"]:
            add_kv(doc, "Materials Needed", lesson["materials"])
        if lesson["safety"]:
            add_kv(doc, "Safety Considerations", lesson["safety"])

        # ── C. Implementation Framework ────────────────────────────────────────
        add_heading(doc, "C.  Lesson Implementation Framework", level=2)

        if lesson["period1_table"]:
            add_impl_table(
                doc,
                lesson.get("period1_heading", "Period 1 (40 minutes)"),
                lesson["period1_table"],
                notes_out, n, 1
            )
        else:
            notes_out.append(f"  Lesson {n} ({ttl}): Period 1 implementation table NOT FOUND in source.")
            p = doc.add_paragraph("[Period 1 implementation table not extracted — check source document]")
            p.runs[0].font.color.rgb = RGBColor(0xCC, 0x00, 0x00)

        if lesson["period2_table"]:
            add_impl_table(
                doc,
                lesson.get("period2_heading", "Period 2 (40 minutes)"),
                lesson["period2_table"],
                notes_out, n, 2
            )
        else:
            notes_out.append(f"  Lesson {n} ({ttl}): Period 2 implementation table NOT FOUND in source.")
            p = doc.add_paragraph("[Period 2 implementation table not extracted — check source document]")
            p.runs[0].font.color.rgb = RGBColor(0xCC, 0x00, 0x00)

        # ── D. Teacher Reflection ─────────────────────────────────────────────
        add_heading(doc, "D.  Teacher Reflection Prompts", level=2)
        if lesson["reflections"]:
            for line in lesson["reflections"]:
                add_body(doc, line, bullet=True)
        else:
            notes_out.append(f"  Lesson {n} ({ttl}): Teacher Reflection section (D) is empty.")

        # ── E. Summary Table Prompt ────────────────────────────────────────────
        add_heading(doc, "E.  Summary Table Prompt", level=2)
        has_e_content = False
        if lesson["summary_prompt"]:
            add_body(doc, lesson["summary_prompt"])
            has_e_content = True
        if lesson["summary_table_rows"]:
            # Render example completed row as a 4-column table
            hdrs = ["Lesson", "What We Learned", "Evidence We Gathered", "How This Helps Explain the Phenomenon"]
            stbl = doc.add_table(rows=1, cols=4)
            stbl.style = "Table Grid"
            for ci, (cell, hdr) in enumerate(zip(stbl.rows[0].cells, hdrs)):
                shade_cell(cell, "2E7D8C")
                p = cell.paragraphs[0]
                r = p.add_run(hdr)
                _set_font(r, bold=True, size=Pt(9), color=WHITE)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for row_data in lesson["summary_table_rows"]:
                tr = stbl.add_row()
                for cell, text in zip(tr.cells, row_data):
                    shade_cell(cell, "F0FAF9")
                    p = cell.paragraphs[0]
                    run = p.add_run(text)
                    _set_font(run, size=Pt(9))
            # Set column widths for 4-col table
            w4 = [Inches(1.5), Inches(3.0), Inches(3.0), Inches(3.2)]
            for ci, col in enumerate(stbl.columns):
                if ci < len(w4):
                    for cell in col.cells:
                        cell.width = w4[ci]
            doc.add_paragraph()
            has_e_content = True
        if not has_e_content:
            p = doc.add_paragraph(
                "Students add a row to their Summary Table after this lesson. "
                "Columns: Lesson | What We Learned | Evidence We Gathered | "
                "How This Helps Explain the Phenomenon."
            )
            _para_font(p, color=RGBColor(0x55, 0x55, 0x55))
            notes_out.append(
                f"  Lesson {n} ({ttl}): Section E — no summary table example found in source; "
                "generic prompt inserted."
            )

        add_divider(doc)
        doc.add_paragraph()  # breathing room between lessons

    return doc


# ── main ─────────────────────────────────────────────────────────────────────
def main():
    for key, src_path in SOURCE_FILES.items():
        meta = META[key]
        print(f"\n{'='*60}")
        print(f"Processing: {meta['subject']} — {meta['substrand']}")
        print(f"  Source: {src_path.name}")

        notes: list[str] = []

        lessons = parse_source(src_path)
        print(f"  Parsed {len(lessons)} lessons")

        if len(lessons) != meta["lessons"]:
            notes.append(
                f"MISMATCH: Expected {meta['lessons']} lessons, found {len(lessons)}. "
                "Some lessons may not have been detected correctly."
            )

        for lesson in lessons:
            p1 = len(lesson["period1_table"])
            p2 = len(lesson["period2_table"])
            print(f"    Lesson {lesson['number']:2d}: '{lesson['title'][:50]}' "
                  f"| P1 rows={p1} P2 rows={p2}")
            if not lesson["inquiry_question"]:
                notes.append(f"  Lesson {lesson['number']}: inquiry_question not found — filled from title.")
                lesson["inquiry_question"] = lesson["title"]

        doc = build_docx(key, lessons, notes)

        out_path = OUTPUT_FILES[key]
        doc.save(str(out_path))
        print(f"  Saved → {out_path.name}")

        if notes:
            NOTES.extend([f"\n[{meta['subject']} — {meta['substrand']}]"] + notes)
        else:
            NOTES.append(f"\n[{meta['subject']}]: No issues found.")

    # ── Print all notes ───────────────────────────────────────────────────────
    print("\n" + "="*60)
    print("NOTES / ISSUES / CORRECTIONS")
    print("="*60)
    for n in NOTES:
        print(n)

    # Save notes to file
    notes_path = OUT_DIR / "REFORMATTING_NOTES.txt"
    notes_path.write_text("\n".join(NOTES))
    print(f"\nNotes saved to: {notes_path}")


if __name__ == "__main__":
    main()
