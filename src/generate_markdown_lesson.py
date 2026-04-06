"""
Generate CBE Lessons in Markdown Format
Markdown tables convert perfectly to Word and are easy to read/edit
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent))
load_dotenv()


class MarkdownLessonGenerator:
    """Generate lessons in Markdown with proper tables"""
    
    def __init__(self):
        print("Initializing Markdown Lesson Generator...")
        import anthropic
        self.claude = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        print("✓ Ready")
    
    def generate_lesson(self, subject, grade, topic, number=1, phenomenon=None):
        """Generate lesson in Markdown format with proper tables"""
        
        print(f"\n{'='*70}")
        print(f"LESSON {number}: {topic}")
        print(f"{'='*70}")
        
        prompt = f"""Generate a complete CBE lesson plan for Kenya in MARKDOWN format.

**LESSON DETAILS:**
- Subject: {subject}
- Grade: {grade}
- Topic: {topic}
- Lesson Number: {number}
- Phenomenon: {phenomenon or 'N/A'}

**CRITICAL: You MUST use proper Markdown tables for structured content.**

**FORMAT TO FOLLOW EXACTLY:**

# Lesson {number}: {topic}
## Kenya Competency-Based Curriculum

---

## A. Specific Learning Outcomes

| Category | Outcomes |
|----------|----------|
| **Knowledge** | • By the end of the lesson, the learner should be able to...<br>• Understand that...<br>• Know that...<br>• Recognize that... |
| **Skills** | • Observing and recording...<br>• Analyzing data...<br>• Using equipment...<br>• Communicating findings... |
| **Attitudes** | • Appreciation for...<br>• Curiosity about...<br>• Respect for... |
| **Science and Engineering Practices** | • Asking questions<br>• Developing models<br>• Planning investigations<br>• Analyzing data |

---

## B. Overview

| Element | Details |
|---------|---------|
| **Key Inquiry Question** | What is the main question driving this lesson? |
| **Purpose in Storyline** | This lesson helps students understand... It builds on previous lessons by... It prepares for future lessons on... |
| **Safety Notes** | List specific safety precautions for this lesson, or write "n/a" if none required |

---

## C. Lesson Implementation Framework

| Learner Experience | Resource Link | Teacher Moves | Sensemaking Strategy | Formative Assessment |
|-------------------|---------------|---------------|---------------------|---------------------|
| **[Activity Name]**<br><br>Students observe/investigate/explore...<br><br>They record their observations in notebooks.<br><br>(20+ words describing what students DO) | • Physical materials list<br>• VIDEO: [Topic]<br>• [ARES VIDEO: {topic}]<br>• READING: [Title]<br>• INTERACTIVE: [Simulation]<br>• Laboratory equipment | **Facilitating [Activity]:**<br>• "What do you notice about...?"<br>• PROBING: "Why do you think...?"<br>• WAIT TIME: 5-10 seconds<br>• Circulating among groups<br>• Asking probing questions, NOT telling answers | **Think-Pair-Share:**<br>• Think: Individual (2 min)<br>• Pair: Discuss (3 min)<br>• Share: Present to class<br><br>Students record:<br>• Observations<br>• Patterns<br>• Questions | **Engagement Check:**<br>☐ Makes predictions<br>☐ Records observations<br>☐ Participates actively<br><br>**Quick Check:** "What did you observe?" |
| **[Next Activity]**<br><br>[Description of second activity]<br><br>(20+ words) | • [Resources for activity 2]<br>• [ARES resources] | **Facilitating:**<br>• [Questions]<br>• PROBING: [Follow-up]<br>• WAIT TIME: [seconds] | **[Strategy]:**<br>• [How students make sense]<br>• [Discussion format] | **Assessment:**<br>☐ [Criterion 1]<br>☐ [Criterion 2]<br><br>**Exit Ticket:** "[Question]" |
| **[Third Activity]**<br><br>[Description]<br><br>(Minimum 3 rows total) | • [Resources] | **Facilitating:**<br>• [Questions]<br>• WAIT TIME: [X seconds] | **[Strategy]:** | **Assessment:**<br>☐ [Criteria] |

---

## D. Teacher Reflection

1. Did students engage fully in the activities? What evidence showed engagement?
2. Can students explain the key concepts using evidence from the lesson?
3. What misconceptions emerged? How did I address them?
4. Did I use probing questions with sufficient wait time (5-15 seconds)?
5. What worked well? What would I change for next time?
6. **Student Feedback:** Ask students: "What helped you learn most today?" Record their responses.

---

## E. Summary Table Prompt

**Teacher says:** "Add Lesson {number} to your Summary Table."

**Prompt for students:**

- **What did I observe?** (What did you see, do, or discover in this lesson? Note any DQB updates or Model revisions)
- **What did I learn?** (What key concepts or skills did you learn?)
- **How does this explain the phenomenon?** (How does today's learning help explain: {phenomenon or 'our anchoring phenomenon'}?)

**Give students 5-10 minutes to complete this reflection.**

---

**REQUIREMENTS:**

1. **Use Kenyan context throughout:**
   - Currency: KSh (not $ or £)
   - Companies: KPLC (Kenya Power & Lighting Company)
   - Local examples: matatus, boda-bodas, solar panels on rural schools, etc.
   - Career connections: How does this relate to jobs in Kenya?

2. **Include ARES resource placeholders:**
   - [ARES VIDEO: {topic}]
   - [ARES SIMULATION: {topic}]
   - [ARES ASSESSMENT: {topic}]

3. **Teacher facilitation (NOT lecturing):**
   - Always show probing questions
   - Always specify WAIT TIME (5-15 seconds)
   - Show circulating, guiding, eliciting student ideas

4. **Think-Pair-Share in every row** of the Implementation Framework

5. **Checkboxes (☐) in assessments**

6. **Minimum 3 rows** in Implementation Framework table, 5 rows preferred

7. **Each table cell must have substantive content** (20+ words, not just 1-2 words)

Generate the complete lesson now in proper Markdown format with all tables."""

        print("  → Claude: Generating lesson in Markdown...")
        
        response = self.claude.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.content[0].text
        print("  ✓ Lesson generated")
        
        return content
    
    def save_markdown(self, content, number, topic, output_dir="data/outputs/markdown"):
        """Save Markdown file"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        filename = f"Lesson_{number:03d}_{topic.replace(' ', '_')}.md"
        filepath = output_path / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✓ Saved Markdown: {filepath}")
        return str(filepath)
    
    def convert_to_docx(self, md_filepath, output_dir="data/outputs/docx"):
        """Convert Markdown to Word using pandoc if available"""
        import subprocess
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        md_file = Path(md_filepath)
        docx_file = output_path / md_file.name.replace('.md', '.docx')
        
        try:
            # Try using pandoc (best conversion)
            subprocess.run([
                'pandoc',
                str(md_file),
                '-o', str(docx_file),
                '--reference-doc=/dev/null',  # Use default styling
            ], check=True, capture_output=True)
            
            print(f"  ✓ Converted to Word: {docx_file}")
            return str(docx_file)
            
        except (FileNotFoundError, subprocess.CalledProcessError):
            print("  ⚠ Pandoc not found - install with: sudo apt install pandoc")
            print("  → You can still use the .md file - open in Word or any Markdown viewer")
            return None
    
    def generate_lesson_files(self, subject, grade, topic, number=1, phenomenon=None):
        """Generate lesson in both Markdown and Word formats"""
        
        # Generate Markdown
        content = self.generate_lesson(subject, grade, topic, number, phenomenon)
        
        # Save Markdown
        md_path = self.save_markdown(content, number, topic)
        
        # Try to convert to Word
        docx_path = self.convert_to_docx(md_path)
        
        return {
            'markdown': md_path,
            'docx': docx_path,
            'status': 'success'
        }


def main():
    print("\n" + "="*70)
    print("CBE LESSON GENERATOR - MARKDOWN FORMAT")
    print("="*70)
    
    gen = MarkdownLessonGenerator()
    
    result = gen.generate_lesson_files(
        subject="Physics",
        grade="Grade 10",
        topic="Introduction to Current Electricity",
        number=1,
        phenomenon="Why do electrical devices get hot when plugged in?"
    )
    
    print(f"\n{'='*70}")
    print("SUCCESS!")
    print(f"{'='*70}")
    print(f"✓ Markdown: {result['markdown']}")
    if result['docx']:
        print(f"✓ Word: {result['docx']}")
    
    print(f"\nYou can:")
    print(f"1. Open the .md file in any text editor")
    print(f"2. Open the .md file in Microsoft Word (File > Open)")
    print(f"3. Use the .docx file if pandoc converted it")


if __name__ == "__main__":
    main()
