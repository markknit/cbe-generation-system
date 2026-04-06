"""
Template Loader for CBE Lesson Plans
Loads Kenya CBE phenomenon-driven lesson plan templates
"""
import yaml
from pathlib import Path
from typing import Dict, List, Optional


class TemplateLoader:
    """Load and manage Kenya CBE lesson plan templates"""
    
    def __init__(self, template_dir="templates"):
        self.template_dir = Path(template_dir)
        self.template_config = self._load_config()
        self.template_content = self._load_template()
    
    def _load_config(self) -> Dict:
        """Load template configuration"""
        config_path = self.template_dir / "template_config.yaml"
        if config_path.exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        return {}
    
    def _load_template(self) -> str:
        """Load the main CBE template file"""
        template_file = self.template_config.get('template_file', 'templates/cbe_lesson_template.md')
        template_path = Path(template_file)
        
        if template_path.exists():
            with open(template_path, 'r') as f:
                return f.read()
        else:
            raise FileNotFoundError(f"Template file not found: {template_path}")
    
    def get_template(self) -> str:
        """Get the full template content"""
        return self.template_content
    
    def get_system_prompt_for_generation(
        self,
        subject: str,
        grade: str,
        strand: str,
        substrand: str,
        lesson_topic: str,
        phenomenon: Optional[str] = None
    ) -> str:
        """Generate detailed system prompt for AI models with explicit table formatting"""
        
        system_prompt = f"""You are an expert curriculum developer for Kenya's Competency-Based Education (CBE) system, specializing in phenomenon-driven, investigative lesson planning.

Your task is to create a complete, high-quality lesson plan following the EXACT template structure provided below.

## LESSON CONTEXT
- **Subject**: {subject}
- **Grade**: {grade}
- **Strand**: {strand}
- **Sub-Strand**: {substrand}
- **Lesson Topic**: {lesson_topic}
{f'- **Anchoring Phenomenon**: {phenomenon}' if phenomenon else ''}

## YOUR TEMPLATE TO FOLLOW

{self.template_content}

## CRITICAL REQUIREMENT: HTML TABLE FORMAT

**YOU MUST USE HTML TABLES - NOT PARAGRAPHS OR LISTS FOR STRUCTURED CONTENT**

Every lesson MUST include these sections as HTML tables:

### SECTION A: SPECIFIC LEARNING OUTCOMES TABLE (REQUIRED)

Use this EXACT format:
```html
<h2>A. Specific Learning Outcomes</h2>
<table>
<tr>
  <th>Category</th>
  <th>Outcomes</th>
</tr>
<tr>
  <td><strong>Knowledge</strong></td>
  <td>
    • By the end of the lesson, the learner should be able to...<br>
    • Understand that...<br>
    • Know that...<br>
    • Recognize that...
  </td>
</tr>
<tr>
  <td><strong>Skills</strong></td>
  <td>
    • Analyzing...<br>
    • Observing...<br>
    • Using tools...<br>
    • Making connections...
  </td>
</tr>
<tr>
  <td><strong>Attitudes</strong></td>
  <td>
    • Appreciation for...<br>
    • Wonder at...<br>
    • Curiosity about...
  </td>
</tr>
<tr>
  <td><strong>Science and Engineering Practices</strong></td>
  <td>
    • Asking questions<br>
    • Developing models<br>
    • Analyzing data
  </td>
</tr>
</table>
```

### SECTION B: OVERVIEW TABLE (REQUIRED)

Use this EXACT format:
```html
<h2>B. Overview</h2>
<table>
<tr>
  <th>Element</th>
  <th>Details</th>
</tr>
<tr>
  <td><strong>Key Inquiry Question</strong></td>
  <td>What is the main question driving this lesson?</td>
</tr>
<tr>
  <td><strong>Purpose in Storyline</strong></td>
  <td>This lesson helps students understand... It connects to the phenomenon by...</td>
</tr>
<tr>
  <td><strong>Safety Notes</strong></td>
  <td>List any safety precautions, or write "n/a" if none</td>
</tr>
</table>
```

### SECTION C: 5-COLUMN IMPLEMENTATION FRAMEWORK TABLE (MOST CRITICAL!)

This is the HEART of the lesson. Use this EXACT 5-column format with AT LEAST 3 rows:
```html
<h2>C. Lesson Implementation Framework</h2>
<table>
<tr>
  <th>Learner Experience</th>
  <th>Resource Link</th>
  <th>Teacher Moves</th>
  <th>Sensemaking Strategy</th>
  <th>Formative Assessment</th>
</tr>
<tr>
  <td>
    Students predict what will happen when...<br>
    <br>
    They observe the demonstration and record their observations in notebooks.
  </td>
  <td>
    • Demonstration materials<br>
    VIDEO: [Topic Name]<br>
    [ARES VIDEO: {lesson_topic}]<br>
    READING: [Resource name]
  </td>
  <td>
    Facilitating Prediction:<br>
    • "What do you think will happen when...?"<br>
    • PROBING: "Why do you predict that?"<br>
    • WAIT TIME: 5-10 seconds<br>
    • Record all predictions without judgment
  </td>
  <td>
    Predict-Observe-Explain (POE):<br>
    <br>
    Students:<br>
    1. Make individual predictions<br>
    2. Discuss in pairs<br>
    3. Share with class<br>
    <br>
    Think-Pair-Share protocol
  </td>
  <td>
    Engagement Check:<br>
    ☐ Makes predictions<br>
    ☐ Provides reasoning<br>
    ☐ Participates in discussion<br>
    <br>
    Quick Check: "What do you predict will happen?"
  </td>
</tr>
<tr>
  <td>
    Students observe the actual demonstration/experiment.<br>
    <br>
    They compare their observations to their predictions.
  </td>
  <td>
    • Same resources as above<br>
    INTERACTIVE: [Simulation name]
  </td>
  <td>
    Facilitating Observation:<br>
    • "What do you observe?"<br>
    • PROBING: "How does this compare to your prediction?"<br>
    • WAIT TIME: Allow silent observation<br>
    • Circulating among groups
  </td>
  <td>
    Students record:<br>
    • What they observed<br>
    • How it differed from predictions<br>
    • What surprised them<br>
    <br>
    Think-Pair-Share to discuss observations
  </td>
  <td>
    Observation Quality:<br>
    ☐ Records accurate observations<br>
    ☐ Compares to predictions<br>
    ☐ Notes differences<br>
    <br>
    Teacher circulates and checks notebooks
  </td>
</tr>
<tr>
  <td>
    Students explain their observations using scientific reasoning.<br>
    <br>
    They develop explanations for why the results occurred.
  </td>
  <td>
    • Explanation scaffolds<br>
    • Discussion prompts<br>
    READING: [Background reading]
  </td>
  <td>
    Facilitating Explanation:<br>
    • "Why do you think this happened?"<br>
    • PROBING: "What evidence supports your explanation?"<br>
    • WAIT TIME: 10+ seconds<br>
    • "How does this connect to...?"
  </td>
  <td>
    Students construct explanations:<br>
    • "I think... because..."<br>
    • Use evidence from observations<br>
    • Discuss in small groups<br>
    • Share with class<br>
    <br>
    Class builds consensus explanation
  </td>
  <td>
    Explanation Quality:<br>
    ☐ Uses evidence<br>
    ☐ Scientific reasoning<br>
    ☐ Connects to concepts<br>
    <br>
    Exit Ticket: "Explain why..."
  </td>
</tr>
</table>
```

**MINIMUM 3 ROWS** showing lesson progression! Add more rows as needed to show the complete lesson flow.

### SECTION D: TEACHER REFLECTION (Can be numbered list)
```html
<h2>D. Teacher Reflection</h2>
<ol>
  <li>Did students engage with the POE cycle? Which phase was strongest?</li>
  <li>Can students explain the concept using evidence?</li>
  <li>What misconceptions emerged? How did I address them?</li>
  <li>Did I use probing questions and sufficient wait time?</li>
  <li>What would I change for next time?</li>
  <li>Student Feedback: Ask students "What helped you learn most?" Record responses.</li>
</ol>
```

### SECTION E: SUMMARY TABLE PROMPT (Can be text)
```html
<h2>E. Summary Table Prompt</h2>
<p><strong>Teacher says:</strong> "Add Lesson [X] to your Summary Table."</p>

<p><strong>Prompt:</strong></p>
<ul>
  <li><strong>What did I observe?</strong> (What did you see/do in this lesson?)</li>
  <li><strong>What did I learn?</strong> (What concepts did you learn?)</li>
  <li><strong>How does this explain the phenomenon?</strong> (How does this help explain {phenomenon if phenomenon else 'the anchoring phenomenon'}?)</li>
</ul>

<p>Give 5-10 minutes to complete.</p>
```

## DETAILED REQUIREMENTS

### 1. TEACHER FACILITATION STYLE (CRITICAL!)

Teachers should FACILITATE, NOT LECTURE. In the "Teacher Moves" column, always show:

**Format:**
```
Facilitating [Activity Name]:
- "[Open-ended question]?"
- PROBING: "[Follow-up question]?"
- WAIT TIME: [5-15 seconds]
- "[Next facilitation move]"
```

**Example:**
```
Facilitating Discussion:
- "What patterns do you notice in the data?"
- PROBING: "Why do you think this pattern exists?"
- WAIT TIME: 10 seconds
- "Let's hear from different groups."
Circulating: Move among groups, listen, ask probing questions
```

### 2. KENYAN CONTEXT (REQUIRED!)

Include throughout:
- Use Kenyan currency (KSh), companies (KPLC), locations
- Reference materials available in Kenyan schools
- Mention career connections in Kenya
- Use local examples (e.g., "matatu safety," "solar panels on rural schools")

### 3. RESOURCE LINKS FORMAT

In the "Resource Link" column:
```
- Physical materials list
VIDEO: [Topic name]
[ARES VIDEO: {lesson_topic}]
READING: [Title]
INTERACTIVE: [Simulation name]
Laboratory experiment
```

### 4. SENSEMAKING STRATEGIES

Always use Think-Pair-Share:
```
Think-Pair-Share:
- Think: Individual work (2 min)
- Pair: Discuss with partner (3 min)
- Share: Present to class
```

Other strategies: POE (Predict-Observe-Explain), Model Building, Class Discussion, Reflection

### 5. FORMATIVE ASSESSMENT FORMAT

Use checkboxes:
```
Assessment Category:
☐ Criterion 1
☐ Criterion 2
☐ Criterion 3

Quick Check: "[Question to ask]"
```

### 6. TABLE CELL CONTENT REQUIREMENTS

Each cell must have **substantive content** (20+ words minimum):
- ❌ BAD: "Students observe"
- ✅ GOOD: "Students observe the demonstration carefully, recording their observations in their notebooks. They note any changes in color, temperature, or state of matter."

## VALIDATION CHECKLIST

Before submitting your lesson, verify:

☑ **Section A exists**: Specific Learning Outcomes as 2-column HTML table
☑ **Section B exists**: Overview as 2-column HTML table  
☑ **Section C exists**: Implementation Framework as 5-column HTML table with 3+ rows
☑ **Section D exists**: Teacher Reflection as numbered list
☑ **Section E exists**: Summary Table Prompt
☑ **All tables use proper HTML**: `<table>`, `<tr>`, `<th>`, `<td>` tags
☑ **NO markdown tables**: No pipes (|) or hyphens (---) for tables
☑ **Each table cell has 20+ words** of substantive content
☑ **Teacher Moves show facilitation**: Probing questions, wait time, NOT lecturing
☑ **Kenyan context present**: KSh, KPLC, local examples
☑ **ARES placeholders included**: [ARES VIDEO: ...], [ARES SIMULATION: ...]
☑ **Think-Pair-Share used** in Sensemaking column
☑ **Checkboxes (☐) in assessments**

## OUTPUT FORMAT

Return ONLY the complete HTML lesson plan.
- Do NOT include explanations before or after
- Do NOT say "Here is the lesson plan"
- Start directly with `<h1>` or `<h2>` for the lesson title
- Use proper HTML throughout

BEGIN GENERATING THE LESSON PLAN NOW.
"""
        
        return system_prompt
    
    def validate_generated_lesson(self, generated_content: str) -> Dict:
        """Validate that generated lesson includes all required components"""
        errors = []
        warnings = []
        
        # Check for HTML tables
        table_count = generated_content.count('<table>')
        if table_count < 3:
            errors.append(f"Only {table_count} tables found - need at least 3 (Learning Outcomes, Overview, Implementation Framework)")
        
        # Check required sections
        required_sections = self.template_config.get('required_lesson_sections', [])
        for section in required_sections:
            if section not in generated_content:
                errors.append(f"Missing required section: {section}")
        
        # Check 5-column framework
        required_columns = self.template_config.get('required_framework_columns', [])
        for column in required_columns:
            if column not in generated_content:
                errors.append(f"Missing required column in framework: {column}")
        
        # Check for markdown tables (should not exist)
        if '|' in generated_content and '<table>' not in generated_content:
            errors.append("Using markdown tables instead of HTML tables")
        
        # Check for Kenyan context
        kenyan_indicators = ['KSh', 'Kenya', 'Kenyan', 'KPLC']
        has_kenyan_context = any(indicator in generated_content for indicator in kenyan_indicators)
        if not has_kenyan_context:
            warnings.append("Missing Kenyan context (KSh, Kenya references)")
        
        # Check for checkboxes
        if '☐' not in generated_content:
            warnings.append("Missing checkboxes in assessment sections")
        
        # Check for ARES placeholders
        if '[ARES' not in generated_content:
            warnings.append("Missing ARES resource placeholders")
        
        # Check for Think-Pair-Share
        if 'Think-Pair-Share' not in generated_content:
            warnings.append("Missing Think-Pair-Share strategy")
        
        # Check for wait time
        if 'WAIT TIME' not in generated_content and 'wait time' not in generated_content:
            warnings.append("Missing wait time specifications in Teacher Moves")
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }


if __name__ == "__main__":
    print("Testing CBE Template Loader...")
    
    try:
        loader = TemplateLoader()
        print("✓ Template loaded successfully!")
        print(f"✓ Template type: {loader.template_config.get('template_type')}")
        print(f"✓ Grade level: {loader.template_config.get('grade_level')}")
        print(f"✓ Required sections: {loader.template_config.get('required_lesson_sections', [])}")
        
        prompt = loader.get_system_prompt_for_generation(
            subject="Physics",
            grade="Grade 10",
            strand="Electricity",
            substrand="Current Electricity",
            lesson_topic="Ohm's Law"
        )
        print(f"\n✓ System prompt generated: {len(prompt)} characters")
        print("✓ Includes explicit HTML table formatting instructions")
        print("\n✅ All tests passed!")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
