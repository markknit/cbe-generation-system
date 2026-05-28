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
