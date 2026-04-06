#!/bin/bash
################################################################################
# CBE Generation System - Resource Integration Update
# This script integrates curriculum PDFs and template examples into the system
################################################################################

set -e  # Exit on error

echo ""
echo "========================================================================"
echo "CBE GENERATION SYSTEM - RESOURCE INTEGRATION UPDATE"
echo "========================================================================"
echo ""

PROJECT_DIR="$HOME/ares/cbe-generation-system"

# Navigate to project
cd "$PROJECT_DIR"

echo "→ Creating directory structure..."
mkdir -p data/raw/curriculum_pdfs
mkdir -p data/raw/template_examples
mkdir -p data/outputs/docx
mkdir -p data/outputs/markdown
mkdir -p config
mkdir -p src

echo "✓ Directories created"

# Create configuration file
echo "→ Creating generation configuration..."
cat > config/generation_config.yaml << 'EOF'
# CBE Lesson Generation Configuration

paths:
  curriculum_pdfs: "data/raw/curriculum_pdfs"
  template_examples: "data/raw/template_examples"
  output_docx: "data/outputs/docx"
  output_markdown: "data/outputs/markdown"
  templates: "templates"

# Curriculum sources mapping
curriculum_sources:
  physics:
    grade_10: "KICD_Grade_10_CBC_Physics_Curriculum_March_2025.pdf"
  biology:
    grade_10: "KICD_Grade_10_CBC_Biology_Curriculum_March_2025.pdf"
  chemistry:
    grade_10: "KICD_Grade_10_CBC_Chemistry_Curriculum_March_2025.pdf"

# Template examples
template_examples:
  primary: "Biology_CellStructure_CBE_LessonSequence_v1.docx"
  
# Generation settings
generation:
  model: "claude-sonnet-4-5-20250929"
  max_tokens: 12000
  temperature: 1.0
  
# Formatting settings
formatting:
  orientation: "landscape"
  margins: "narrow"  # 0.5 inch all around
  equal_columns: true
  column_count: 5
  font: "Calibri"
  font_size: 11

# Lesson structure
lesson_structure:
  sections:
    - "A. Specific Learning Outcomes"
    - "B. Overview"
    - "C. Lesson Implementation Framework"
    - "D. Teacher Reflection"
    - "E. Summary Table Prompt"
  
  framework_rows:
    - "PREDICT Phase"
    - "OBSERVE Phase"
    - "EXPLAIN Phase"
    - "Driving Questions Board"
    - "Initial Model Building"
    - "Kenya Context Connection"
    - "Model Revision"

# Include sub-strand overview before lessons
include_substrand_overview: true
EOF

echo "✓ Configuration file created"

# Create resource manager
echo "→ Creating resource manager..."
cat > src/resource_manager.py << 'EOF'
"""
Resource Manager - Handles curriculum PDFs and template examples
"""
from pathlib import Path
import yaml
from typing import Optional, List, Dict


class ResourceManager:
    """Manages curriculum documents and template examples"""
    
    def __init__(self, config_path: str = "config/generation_config.yaml"):
        self.config = self._load_config(config_path)
        self.curriculum_dir = Path(self.config['paths']['curriculum_pdfs'])
        self.examples_dir = Path(self.config['paths']['template_examples'])
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration"""
        config_file = Path(config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    
    def get_curriculum_pdf(self, subject: str, grade: str) -> Optional[Path]:
        """Get the curriculum PDF for a specific subject/grade"""
        subject_lower = subject.lower()
        grade_key = grade.lower().replace(" ", "_")
        
        # Check config first
        curriculum_sources = self.config.get('curriculum_sources', {})
        if subject_lower in curriculum_sources:
            if grade_key in curriculum_sources[subject_lower]:
                filename = curriculum_sources[subject_lower][grade_key]
                pdf_path = self.curriculum_dir / filename
                if pdf_path.exists():
                    return pdf_path
        
        # Fall back to searching directory
        for pdf in self.curriculum_dir.glob("*.pdf"):
            if subject_lower in pdf.name.lower() and grade.replace(" ", "") in pdf.name:
                return pdf
        
        return None
    
    def get_template_examples(self) -> List[Path]:
        """Get all template example documents"""
        if not self.examples_dir.exists():
            return []
        
        examples = []
        examples.extend(self.examples_dir.glob("*.docx"))
        examples.extend(self.examples_dir.glob("*.pdf"))
        return examples
    
    def get_primary_template(self) -> Optional[Path]:
        """Get the primary template example"""
        template_examples = self.config.get('template_examples', {})
        primary = template_examples.get('primary')
        
        if primary:
            template_path = self.examples_dir / primary
            if template_path.exists():
                return template_path
        
        # Fall back to first available
        examples = self.get_template_examples()
        return examples[0] if examples else None
    
    def list_available_curricula(self) -> List[Dict]:
        """List all available curriculum PDFs"""
        if not self.curriculum_dir.exists():
            return []
        
        curricula = []
        for pdf in self.curriculum_dir.glob("*.pdf"):
            curricula.append({
                'filename': pdf.name,
                'path': str(pdf),
                'size': pdf.stat().st_size
            })
        return curricula
    
    def list_available_templates(self) -> List[Dict]:
        """List all available template examples"""
        templates = []
        for doc in self.get_template_examples():
            templates.append({
                'filename': doc.name,
                'path': str(doc),
                'size': doc.stat().st_size
            })
        return templates
    
    def get_config(self, key: str = None):
        """Get configuration value"""
        if key:
            keys = key.split('.')
            value = self.config
            for k in keys:
                value = value.get(k, {})
            return value
        return self.config
    
    def validate_resources(self) -> Dict[str, bool]:
        """Validate that required resources are available"""
        validation = {
            'curriculum_dir_exists': self.curriculum_dir.exists(),
            'examples_dir_exists': self.examples_dir.exists(),
            'has_curricula': len(self.list_available_curricula()) > 0,
            'has_templates': len(self.list_available_templates()) > 0,
            'primary_template_exists': self.get_primary_template() is not None
        }
        return validation


if __name__ == "__main__":
    # Test the resource manager
    print("\n" + "="*70)
    print("TESTING RESOURCE MANAGER")
    print("="*70 + "\n")
    
    try:
        rm = ResourceManager()
        
        print("=== Available Curricula ===")
        curricula = rm.list_available_curricula()
        if curricula:
            for curr in curricula:
                print(f"  ✓ {curr['filename']}")
        else:
            print("  ⚠ No curriculum PDFs found in data/raw/curriculum_pdfs/")
        
        print("\n=== Available Template Examples ===")
        templates = rm.list_available_templates()
        if templates:
            for tmpl in templates:
                print(f"  ✓ {tmpl['filename']}")
        else:
            print("  ⚠ No template examples found in data/raw/template_examples/")
        
        print("\n=== Subject Lookup Test ===")
        physics_pdf = rm.get_curriculum_pdf("Physics", "Grade 10")
        if physics_pdf:
            print(f"  ✓ Found Physics curriculum: {physics_pdf.name}")
        else:
            print("  ⚠ Physics curriculum not found")
        
        primary_template = rm.get_primary_template()
        if primary_template:
            print(f"  ✓ Found primary template: {primary_template.name}")
        else:
            print("  ⚠ Primary template not found")
        
        print("\n=== Resource Validation ===")
        validation = rm.validate_resources()
        for check, passed in validation.items():
            status = "✓" if passed else "✗"
            print(f"  {status} {check.replace('_', ' ').title()}")
        
        all_valid = all(validation.values())
        if all_valid:
            print("\n✅ All resources validated successfully!")
        else:
            print("\n⚠ Some resources missing - please add files to appropriate directories")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
EOF

echo "✓ Resource manager created"

# Create README for data/raw
echo "→ Creating README..."
cat > data/raw/README.md << 'EOF'
# Raw Data Directory

This directory contains source materials for CBE lesson generation.

## Directory Structure

### `curriculum_pdfs/`
**Purpose:** Official KICD curriculum documents

**Contents:** 
- KICD Grade 10-12 curriculum PDFs for various subjects
- Used to extract: learning outcomes, strands, sub-strands, competencies, values, PCIs

**Example files:**
- `KICD_Grade_10_CBC_Physics_Curriculum_March_2025.pdf`
- `KICD_Grade_10_CBC_Biology_Curriculum_March_2025.pdf`

### `template_examples/`
**Purpose:** Reference lesson plans showing desired structure and formatting

**Contents:**
- Example CBE lesson plans (DOCX or PDF)
- Used as reference for: lesson organization, level of detail, pedagogical approach, formatting

**Example files:**
- `Biology_CellStructure_CBE_LessonSequence_v1.docx`

## Adding New Files

1. **Curriculum PDFs:** Place in `curriculum_pdfs/` and update `config/generation_config.yaml`
2. **Template Examples:** Place in `template_examples/`

## File Naming Convention

**Curricula:** `KICD_Grade_[XX]_CBC_[Subject]_Curriculum_[Date].pdf`
**Templates:** `[Subject]_[Topic]_CBE_LessonSequence_v[X].docx`
EOF

echo "✓ README created"

# Test the resource manager
echo "→ Testing resource manager..."
echo ""

if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    python3 src/resource_manager.py
else
    echo "⚠ Virtual environment not found - skipping Python test"
    echo "  Run 'source venv/bin/activate' and then 'python3 src/resource_manager.py' to test"
fi

echo ""
echo "========================================================================"
echo "UPDATE COMPLETE!"
echo "========================================================================"
echo ""
echo "Next steps:"
echo "1. Copy curriculum PDFs to: data/raw/curriculum_pdfs/"
echo "2. Copy template examples to: data/raw/template_examples/"
echo "3. Update config/generation_config.yaml if needed"
echo "4. Test: python3 src/resource_manager.py"
echo ""
echo "Directory structure created:"
echo "  ✓ data/raw/curriculum_pdfs/"
echo "  ✓ data/raw/template_examples/"
echo "  ✓ config/generation_config.yaml"
echo "  ✓ src/resource_manager.py"
echo "  ✓ data/raw/README.md"
echo ""
