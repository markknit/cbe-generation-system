"""
Production CBE Lesson Generator - FIXED VERSION
Ensures Section C is always generated with proper validation
"""
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
from dotenv import load_dotenv
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import json
import time
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

try:
    from resource_manager import ResourceManager
except ImportError:
    print("⚠ Resource manager not found - run update_resources.sh first!")
    sys.exit(1)

load_dotenv()


class ProductionLessonGenerator:
    """Complete production-ready lesson generator with validation"""
    
    def __init__(self):
        print("\n" + "="*70)
        print("PRODUCTION CBE LESSON GENERATOR - FIXED VERSION")
        print("="*70 + "\n")
        
        self.resources = ResourceManager()
        
        validation = self.resources.validate_resources()
        if not all(validation.values()):
            print("\n⚠ Warning: Some resources missing!")
            for check, passed in validation.items():
                if not passed:
                    print(f"  ✗ {check.replace('_', ' ').title()}")
            print("\nContinuing anyway...\n")
        else:
            print("✓ All resources validated\n")
        
        self.config = self.resources.get_config()
        
        print("→ Initializing Claude API...")
        import anthropic
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.anthropic_key:
            raise ValueError("Missing ANTHROPIC_API_KEY in .env file")
        self.claude = anthropic.Anthropic(api_key=self.anthropic_key)
        print("✓ Claude API initialized\n")
        
        print("→ Loading template examples...")
        self.template_content = self._load_template_content()
        print(f"✓ Template loaded\n")
    
    def _load_template_content(self) -> str:
        primary_template = self.resources.get_primary_template()
        if not primary_template:
            return "Follow CBE lesson structure"
        return f"Reference template: {primary_template.name}"
    
    def generate_substrand_overview(self, subject: str, grade: str, 
                                    strand: str, substrand: str) -> str:
        """Generate sub-strand overview section"""
        
        curriculum_pdf = self.resources.get_curriculum_pdf(subject, grade)
        
        prompt = f"""Generate a Sub-Strand Overview for Kenya CBC curriculum.

Subject: {subject}
Grade: {grade}
Strand: {strand}
Sub-Strand: {substrand}
{f'Curriculum Reference: {curriculum_pdf.name}' if curriculum_pdf else ''}

Create overview with these components. Return in this EXACT format:

===SUB-STRAND OVERVIEW===
SubStrand: {substrand}
TotalLessons: [number]

Component: Specific Learning Outcomes
Content: [List a-f of learning outcomes for entire sub-strand, each on new line]

Component: Key Inquiry Questions  
Content: [2-3 key questions]

Component: Core Competencies
Content: [List of competencies]

Component: Values
Content: [List of values]

Component: PCIs
Content: [List of PCIs]"""

        response = self.claude.messages.create(
            model=self.config['generation']['model'],
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
    
    def generate_lesson_content(self, subject: str, grade: str, strand: str,
                                substrand: str, topic: str, number: int,
                                phenomenon: str = None, total_lessons: int = 22,
                                retry_count: int = 0, max_retries: int = 3) -> str:
        """Generate lesson content with validation and retry logic"""
        
        curriculum_pdf = self.resources.get_curriculum_pdf(subject, grade)
        
        # ENHANCED PROMPT with explicit Section C requirements
        prompt = f"""Generate a COMPLETE CBE lesson plan for Kenya. This lesson plan MUST include ALL 5 sections: A, B, C, D, and E.

**LESSON DETAILS:**
- Subject: {subject}
- Grade: {grade}
- Strand: {strand}
- Sub-Strand: {substrand}
- Topic: {topic}
- Lesson Number: {number} of {total_lessons}
- Phenomenon: {phenomenon or 'N/A'}
{f'- Curriculum Reference: {curriculum_pdf.name}' if curriculum_pdf else ''}

**CRITICAL REQUIREMENTS:**
1. You MUST generate ALL 5 sections (A, B, C, D, E)
2. Section C is THE MOST IMPORTANT section - it contains the 7-row implementation framework
3. DO NOT skip Section C under any circumstances
4. Each section must start with exactly: ===SECTION X:=== where X is A, B, C, D, or E

**EXACT FORMAT TO FOLLOW:**

===SECTION A: LEARNING OUTCOMES===
Knowledge:
- [Point 1]
- [Point 2]
- [Point 3]

Skills:
- [Point 1]
- [Point 2]

Attitudes:
- [Point 1]
- [Point 2]

Practices:
- [Point 1]
- [Point 2]

===SECTION B: OVERVIEW===
KeyQuestion: [The key inquiry question for this lesson]
Purpose: [Purpose in the storyline - 2-3 sentences]
Safety: [Safety notes or "n/a"]

===SECTION C: FRAMEWORK===

**CRITICAL: This section MUST have exactly 7 rows. Do not skip this section!**

ROW 1 - PREDICT:
Experience: [40+ words describing PREDICT phase of POE cycle - what students DO]
Resources: [List with [ARES VIDEO: ...] placeholders]
Teacher: [Facilitation questions - include "PROBING: ...", "WAIT TIME: 10 seconds"]
Sensemaking: [Think-Pair-Share format with timing]
Assessment: [Checkboxes ☐ and criteria]

ROW 2 - OBSERVE:
Experience: [40+ words describing OBSERVE phase]
Resources: [List with [ARES SIMULATION: ...] placeholders]
Teacher: [Facilitation - "PROBING: ...", "WAIT TIME: 10 seconds"]
Sensemaking: [Data collection, Think-Pair-Share]
Assessment: [☐ Observation criteria]

ROW 3 - EXPLAIN:
Experience: [40+ words describing EXPLAIN phase - students build understanding]
Resources: [List with [ARES VIDEO: ...] placeholders]
Teacher: [NO LECTURING! Questions only - "PROBING: ...", "WAIT TIME: 15 seconds"]
Sensemaking: [Think-Pair-Share, class consensus building]
Assessment: [☐ Explanation quality, Exit Ticket question]

ROW 4 - DQB:
Experience: [Class generates questions about {topic}. Teacher creates visible Driving Questions Board.]
Resources: [Large poster/chart paper, Markers, DQB template, [ARES VIDEO: Intro to DQB]]
Teacher: [Establishing DQB: "What questions do you have about {topic}?", "PROBING: What do you wonder...?", "WAIT TIME: Allow thinking", Recording: Write ALL questions]
Sensemaking: [Question Generation - list 4-5 example student questions about {topic}. Teacher posts all questions on visible DQB]
Assessment: [DQB Started: ☐ Students generate questions, ☐ Questions posted visibly, ☐ Students understand DQB purpose. Note: Add "DQB Started" to Summary Table]

ROW 5 - INITIAL MODEL:
Experience: [Students draw their current model of how {topic} works. What do they think is happening?]
Resources: [Drawing materials, Model template, Colored pencils, [ARES SIMULATION: {topic} Model]]
Teacher: [Facilitating Modeling: "Draw what you think is happening with {topic}.", "PROBING: What components are involved?", "WAIT TIME: Allow creative thinking", "There are no wrong models at this stage!", Emphasizing: "We'll revise this model as we gather evidence."]
Sensemaking: [Initial Model Creation - Students draw individual models showing key components and processes. Think-Pair-Share: Share models with partner, discuss similarities/differences]
Assessment: [Model Quality: ☐ Attempts to draw process, ☐ Shows creative thinking, ☐ Labels parts (if any). Note: "Initial Model Created" goes in Summary Table. Collect models for comparison later]

ROW 6 - KENYA CONTEXT:
Experience: [Class discussion: How does understanding {topic} help Kenya? Include: relevant ministries/organizations (like KPLC for electricity), costs in KSh, applications in Kenyan context, careers]
Resources: [Kenya context materials, Posters, Cost examples (KSh), Photos of local applications, [ARES VIDEO: {topic} in Kenya]]
Teacher: [Facilitating Kenya Connection: "How is {topic} relevant in Kenya?", "PROBING: What careers involve this?", "WAIT TIME: 8 seconds", Discussing Real Issues with Kenyan examples]
Sensemaking: [Think-Pair-Share on Kenya Applications: Students discuss specific Kenyan organizations, cost awareness (KSh), local applications, safety/ethics, careers. Patriotism: Understanding {topic} helps Kenya develop!]
Assessment: [Kenya Connection Quality: ☐ Identifies Kenyan organizations/context, ☐ Discusses 2+ Kenya applications, ☐ Shows awareness of local relevance, ☐ Recognizes career connections. Quick Check: "How is {topic} important in Kenya? Give 2 reasons."]

ROW 7 - MODEL REVISION:
Experience: [Students return to their initial models from ROW 5 and revise based on new evidence from the lesson. Revised models should show: key components, processes, connections, evidence-based improvements]
Resources: [Students' initial models from earlier, Fresh paper for revisions (or revise on original), Colored pencils/markers, Comparison template: Before/After]
Teacher: [Facilitating Model Revision: "Look at your first model. What did you think then?", "PROBING: What evidence do you have now to improve it?", "WAIT TIME: Allow creative thinking (10 sec)", "PROBING: How can you show what you learned?", Emphasizing Scientific Practice: "Scientists revise models as they learn - that's how science works!"]
Sensemaking: [Model Revision Activity - Students revise to show: 1. Key components with labels, 2. Processes/relationships, 3. Evidence from today's lesson, 4. Clear improvements from initial version. Written Reflection: "I revised my model because I learned that...". Think-Pair-Share: Compare before/after models, explain improvements]
Assessment: [Model Revision Quality: ☐ Shows clear improvements from initial model, ☐ Labels components accurately, ☐ Explains changes made in writing, ☐ Uses evidence from today's lesson, ☐ More sophisticated than initial model. Note for Summary Table: "Model Revised - evidence: [key learning]". Collect both initial and revised models]

===SECTION D: REFLECTION===
1. [Teacher reflection question about POE cycle effectiveness]
2. [Teacher reflection about probing questions and wait time]
3. [Teacher reflection about DQB visibility and future use]
4. [Teacher reflection about what initial models revealed]
5. [Teacher reflection about Kenyan context connections]
6. [Teacher reflection about key learning or misconceptions]
7. [Student Feedback prompt: "What surprised you most?" - record 5-10 responses]

===SECTION E: SUMMARY PROMPT===
Teacher says to class: "Add Lesson {number} to your Summary Table. This tracks your learning throughout the unit."

Prompt for students:
- What did I observe? (Key observations, patterns. IMPORTANT: Note DQB Started, Initial Model Created, Model Revised)
- What did I learn? (Key concepts about {topic})
- How does this explain the phenomenon? (Connection to {phenomenon if phenomenon else topic}. What questions remain?)

**NOW GENERATE THE COMPLETE LESSON:**
Remember: ALL 5 sections required, especially Section C with all 7 rows!"""

        # Generate content
        response = self.claude.messages.create(
            model=self.config['generation']['model'],
            max_tokens=self.config['generation']['max_tokens'],
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.content[0].text
        
        # VALIDATION: Check if Section C is present
        if '===SECTION C:' not in content and retry_count < max_retries:
            print(f"  ⚠ Section C missing! Retrying... (attempt {retry_count + 1}/{max_retries})")
            time.sleep(2)  # Brief pause before retry
            return self.generate_lesson_content(
                subject, grade, strand, substrand, topic, number,
                phenomenon, total_lessons, retry_count + 1, max_retries
            )
        
        if '===SECTION C:' not in content:
            print(f"  ✗ ERROR: Section C still missing after {max_retries} retries!")
            print(f"  Generated content length: {len(content)} characters")
            # Save failed content for debugging
            debug_file = f"debug_missing_section_c_{topic.replace(' ', '_')}.txt"
            with open(debug_file, 'w') as f:
                f.write(content)
            print(f"  Debug content saved to: {debug_file}")
        
        return content
    
    def create_word_document(self, content: str, overview_content: str,
                            subject: str, grade: str, substrand: str,
                            topic: str, number: int, total_lessons: int) -> str:
        """Create formatted Word document"""
        
        doc = Document()
        
        # LANDSCAPE with NARROW margins
        section = doc.sections[0]
        section.orientation = 1
        section.page_width = Inches(11)
        section.page_height = Inches(8.5)
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)
        
        style = doc.styles['Normal']
        style.font.name = 'Calibri'
        style.font.size = Pt(11)
        
        # Add overview
        if overview_content:
            self._add_substrand_overview(doc, overview_content, substrand)
            doc.add_page_break()
        
        # Add lesson
        self._add_lesson(doc, content, subject, grade, substrand, topic, number, total_lessons)
        
        # Save
        output_dir = Path(self.config['paths']['output_docx'])
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"Lesson_{number:03d}_{topic.replace(' ', '_')}.docx"
        filepath = output_dir / filename
        
        doc.save(str(filepath))
        return str(filepath)
    
    def _add_substrand_overview(self, doc, content: str, substrand: str):
        """Add sub-strand overview page"""
        title = doc.add_heading(f'SUB-STRAND: {substrand.upper()}', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        title.runs[0].font.color.rgb = RGBColor(0, 70, 135)
        
        subtitle = doc.add_paragraph('Sub-Strand Overview')
        subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
        subtitle.runs[0].font.italic = True
        
        doc.add_paragraph()
        
        table = doc.add_table(rows=1, cols=2)
        table.style = 'Light Grid Accent 1'
        
        hdr = table.rows[0].cells
        hdr[0].text = 'Component'
        hdr[1].text = 'Description'
        for cell in hdr:
            cell.paragraphs[0].runs[0].font.bold = True
        
        components = [
            'Specific Learning Outcomes',
            'Key Inquiry Questions',
            'Core Competencies',
            'Values',
            'PCIs'
        ]
        
        for component in components:
            if f'Component: {component}' in content:
                row = table.add_row()
                row.cells[0].text = component
                
                start = content.find(f'Component: {component}') + len(f'Component: {component}')
                end = content.find('Component:', start)
                if end == -1:
                    end = content.find('===', start)
                if end == -1:
                    end = len(content)
                
                text = content[start:end].strip()
                text = text.replace('Content:', '').strip()
                row.cells[1].text = text
    
    def _add_lesson(self, doc, content: str, subject: str, grade: str,
                   substrand: str, topic: str, number: int, total_lessons: int):
        """Add complete lesson"""
        
        title = doc.add_heading(f'LESSON {number}: {topic.upper()}', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        title.runs[0].font.color.rgb = RGBColor(0, 70, 135)
        
        subtitle = doc.add_paragraph(f'{grade} {subject} - {substrand} - Lesson {number} of {total_lessons}')
        subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
        subtitle.runs[0].font.italic = True
        
        doc.add_paragraph()
        
        sections = content.split('===SECTION')
        
        for section in sections[1:]:
            if 'A:' in section:
                self._add_section_a(doc, section)
            elif 'B:' in section:
                self._add_section_b(doc, section)
            elif 'C:' in section:
                self._add_section_c(doc, section)
            elif 'D:' in section:
                self._add_section_d(doc, section)
            elif 'E:' in section:
                self._add_section_e(doc, section)
    
    def _add_section_a(self, doc, section_text):
        """Add Learning Outcomes table"""
        doc.add_heading('A. Specific Learning Outcomes', 2)
        
        table = doc.add_table(rows=5, cols=2)
        table.style = 'Light Grid Accent 1'
        
        hdr = table.rows[0].cells
        hdr[0].text = 'Category'
        hdr[1].text = 'Outcomes'
        for c in hdr:
            c.paragraphs[0].runs[0].font.bold = True
        
        categories = ['Knowledge:', 'Skills:', 'Attitudes:', 'Practices:']
        for i, cat in enumerate(categories, 1):
            if cat in section_text:
                table.rows[i].cells[0].text = cat.replace(':', '')
                
                start = section_text.find(cat)
                next_cat = [c for c in categories if c != cat]
                end = len(section_text)
                for nc in next_cat:
                    pos = section_text.find(nc, start)
                    if pos > start:
                        end = min(end, pos)
                
                text = section_text[start:end]
                lines = [l.strip('- ').strip() for l in text.split('\n') if l.strip().startswith('-')]
                table.rows[i].cells[1].text = '\n'.join(f'• {l}' for l in lines if l)
        
        doc.add_paragraph()
    
    def _add_section_b(self, doc, section_text):
        """Add Overview table"""
        doc.add_heading('B. Overview', 2)
        
        table = doc.add_table(rows=4, cols=2)
        table.style = 'Light Grid Accent 1'
        
        hdr = table.rows[0].cells
        hdr[0].text = 'Element'
        hdr[1].text = 'Details'
        for c in hdr:
            c.paragraphs[0].runs[0].font.bold = True
        
        items = [
            ('Key Inquiry Question', 'KeyQuestion:'),
            ('Purpose in Storyline', 'Purpose:'),
            ('Safety Notes', 'Safety:')
        ]
        
        for i, (label, marker) in enumerate(items, 1):
            if marker in section_text:
                table.rows[i].cells[0].text = label
                
                start = section_text.find(marker) + len(marker)
                end = section_text.find('\n\n', start)
                if end == -1:
                    end = section_text.find('===', start)
                if end == -1:
                    end = len(section_text)
                
                text = section_text[start:end].strip()
                table.rows[i].cells[1].text = text
        
        doc.add_paragraph()
    
    def _add_section_c(self, doc, section_text):
        """Add 5-column Implementation Framework with EQUAL widths"""
        doc.add_heading('C. Lesson Implementation Framework', 2)
        
        # Count rows
        row_count = section_text.count('ROW ')
        
        if row_count == 0:
            # Fallback if no rows detected
            doc.add_paragraph("⚠ ERROR: Section C content not properly formatted")
            doc.add_paragraph(section_text[:500])
            return
        
        table = doc.add_table(rows=row_count + 1, cols=5)
        table.style = 'Light Grid Accent 1'
        
        # EQUAL column widths
        for row in table.rows:
            for i in range(5):
                row.cells[i].width = Inches(2.0)
        
        # Headers
        headers = ['Learner Experience', 'Resource Link', 'Teacher Moves',
                   'Sensemaking Strategy', 'Formative Assessment']
        for i, h in enumerate(headers):
            table.rows[0].cells[i].text = h
            table.rows[0].cells[i].paragraphs[0].runs[0].font.bold = True
        
        # Parse rows
        rows = section_text.split('ROW ')[1:]
        
        for row_idx, row_text in enumerate(rows, 1):
            if row_idx >= len(table.rows):
                break
            
            columns = [
                ('Experience:', 'Resources:'),
                ('Resources:', 'Teacher:'),
                ('Teacher:', 'Sensemaking:'),
                ('Sensemaking:', 'Assessment:'),
                ('Assessment:', 'ROW ')
            ]
            
            for col_idx, (start_marker, end_marker) in enumerate(columns):
                if start_marker in row_text:
                    start = row_text.find(start_marker) + len(start_marker)
                    end = row_text.find(end_marker, start) if end_marker in row_text[start:] else len(row_text)
                    text = row_text[start:end].strip()
                    table.rows[row_idx].cells[col_idx].text = text
        
        doc.add_paragraph()
    
    def _add_section_d(self, doc, section_text):
        """Add Teacher Reflection"""
        doc.add_heading('D. Teacher Reflection', 2)
        
        lines = section_text.split('\n')
        for line in lines:
            if line.strip() and line.strip()[0].isdigit():
                doc.add_paragraph(line.strip(), style='List Number')
        
        doc.add_paragraph()
    
    def _add_section_e(self, doc, section_text):
        """Add Summary Table Prompt"""
        doc.add_heading('E. Summary Table Prompt', 2)
        
        lines = [l.strip() for l in section_text.split('\n') if l.strip()]
        for line in lines[1:]:
            if line.startswith('- ') or line.startswith('•'):
                doc.add_paragraph(line.strip('- •').strip(), style='List Bullet')
            elif not line.startswith('==='):
                doc.add_paragraph(line)
    
    def generate_complete_lesson(self, subject: str, grade: str, strand: str,
                                 substrand: str, topic: str, number: int = 1,
                                 phenomenon: str = None, total_lessons: int = 22,
                                 include_overview: bool = True) -> Dict:
        """Generate complete lesson with validation"""
        
        print(f"\n{'='*70}")
        print(f"LESSON {number}: {topic}")
        print(f"{'='*70}\n")
        
        overview_content = ""
        if include_overview and number == 1:
            print("  → Generating sub-strand overview...")
            overview_content = self.generate_substrand_overview(
                subject, grade, strand, substrand
            )
            print("  ✓ Overview generated")
        
        print("  → Generating lesson content...")
        content = self.generate_lesson_content(
            subject, grade, strand, substrand, topic, number, phenomenon, total_lessons
        )
        
        # Validate content
        has_section_c = '===SECTION C:' in content
        print(f"  {'✓' if has_section_c else '✗'} Section C present")
        
        if has_section_c:
            row_count = content.count('ROW ')
            print(f"  → Detected {row_count} rows in Section C")
        
        print("  → Creating Word document...")
        filepath = self.create_word_document(
            content, overview_content, subject, grade, substrand,
            topic, number, total_lessons
        )
        print(f"  ✓ Saved: {filepath}")
        
        return {
            'lesson_number': number,
            'topic': topic,
            'filepath': filepath,
            'status': 'success' if has_section_c else 'warning_missing_section_c'
        }


def main():
    """Test with single lesson"""
    print("\n" + "="*70)
    print("CBE LESSON PLAN GENERATOR - FIXED VERSION")
    print("="*70 + "\n")
    
    generator = ProductionLessonGenerator()
    
    result = generator.generate_complete_lesson(
        subject="Chemistry",
        grade="Grade 10",
        strand="Matter and Its Changes",
        substrand="Atomic Structure",
        topic="Introduction to Atoms and Elements",
        number=1,
        phenomenon="Why do different elements have different properties?",
        total_lessons=18,
        include_overview=True
    )
    
    print(f"\n{'='*70}")
    print("GENERATION COMPLETE!")
    print(f"{'='*70}")
    print(f"\nStatus: {result['status']}")
    print(f"File: {result['filepath']}")


if __name__ == "__main__":
    main()
