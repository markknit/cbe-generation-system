"""
CBE Lesson Plan Generator with AI
Full pipeline: Template + Multi-Model AI Generation
"""
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
from dotenv import load_dotenv
import json
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from template_loader import TemplateLoader

# Load environment variables
load_dotenv()


class AILessonGenerator:
    """Generate CBE lesson plans using AI models"""
    
    def __init__(self):
        """Initialize with template and API clients"""
        print("Initializing AI Lesson Generator...")
        
        # Load template
        self.template_loader = TemplateLoader()
        print(f"✓ Template loaded")
        
        # Initialize API clients
        self._init_apis()
        
    def _init_apis(self):
        """Initialize API clients"""
        try:
            import anthropic
            import openai
            import google.generativeai as genai
            
            self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
            self.openai_key = os.getenv("OPENAI_API_KEY")
            self.gemini_key = os.getenv("GEMINI_API_KEY")
            
            if not all([self.anthropic_key, self.openai_key, self.gemini_key]):
                raise ValueError("Missing API keys in .env file")
            
            # Initialize clients
            self.claude = anthropic.Anthropic(api_key=self.anthropic_key)
            self.openai_client = openai.OpenAI(api_key=self.openai_key)
            genai.configure(api_key=self.gemini_key)
            self.gemini = genai.GenerativeModel('gemini-pro')
            
            print("✓ API clients initialized (Claude, GPT, Gemini)")
            
        except ImportError as e:
            print(f"✗ Error importing API libraries: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"✗ Error initializing APIs: {e}")
            sys.exit(1)
    
    def generate_with_gemini(self, system_prompt: str, lesson_topic: str) -> str:
        """Generate draft with Gemini (cheapest)"""
        print(f"  → Gemini: Generating draft...")
        
        try:
            prompt = f"{system_prompt}\n\nGenerate a complete lesson plan for: {lesson_topic}"
            response = self.gemini.generate_content(prompt)
            print(f"  ✓ Gemini draft complete")
            return response.text
        except Exception as e:
            print(f"  ✗ Gemini error: {e}")
            return None
    
    def structure_with_gpt(self, draft: str, system_prompt: str) -> str:
        """Structure with GPT (balanced)"""
        print(f"  → GPT: Structuring into CBE format...")
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Structure this draft into proper CBE format:\n\n{draft}"}
                ],
                max_tokens=4000
            )
            print(f"  ✓ GPT structuring complete")
            return response.choices[0].message.content
        except Exception as e:
            print(f"  ✗ GPT error: {e}")
            return draft
    
    def polish_with_claude(self, structured: str, system_prompt: str) -> str:
        """Polish with Claude (highest quality)"""
        print(f"  → Claude: Final polish...")
        
        try:
            response = self.claude.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=8000,
                messages=[
                    {"role": "user", "content": f"{system_prompt}\n\nPolish this lesson plan:\n\n{structured}"}
                ]
            )
            print(f"  ✓ Claude polish complete")
            return response.content[0].text
        except Exception as e:
            print(f"  ✗ Claude error: {e}")
            return structured
    
    def generate_lesson(
        self,
        subject: str,
        grade: str,
        strand: str,
        substrand: str,
        lesson_topic: str,
        lesson_number: int = 1,
        phenomenon: str = None,
        use_multi_model: bool = True
    ) -> Dict:
        """Generate complete lesson using multi-model pipeline"""
        
        print(f"\n{'='*70}")
        print(f"LESSON {lesson_number}: {lesson_topic}")
        print(f"{'='*70}")
        
        # Get system prompt
        system_prompt = self.template_loader.get_system_prompt_for_generation(
            subject=subject,
            grade=grade,
            strand=strand,
            substrand=substrand,
            lesson_topic=lesson_topic,
            phenomenon=phenomenon
        )
        
        if use_multi_model:
            print("Using multi-model pipeline: Gemini → GPT → Claude")
            
            # Stage 1: Draft with Gemini
            draft = self.generate_with_gemini(system_prompt, lesson_topic)
            if not draft:
                return {'status': 'failed', 'error': 'Gemini draft failed'}
            
            # Stage 2: Structure with GPT
            structured = self.structure_with_gpt(draft, system_prompt)
            
            # Stage 3: Polish with Claude
            final = self.polish_with_claude(structured, system_prompt)
            
        else:
            print("Using single model: Claude Sonnet 4.5")
            final = self.polish_with_claude("", system_prompt)
        
        # Validate
        validation = self.template_loader.validate_generated_lesson(final)
        
        print(f"\n{'='*70}")
        print(f"VALIDATION RESULTS")
        print(f"{'='*70}")
        print(f"Valid: {validation['is_valid']}")
        print(f"Errors: {len(validation['errors'])}")
        print(f"Warnings: {len(validation['warnings'])}")
        if validation['errors']:
            for error in validation['errors']:
                print(f"  ✗ {error}")
        if validation['warnings']:
            for warning in validation['warnings']:
                print(f"  ⚠ {warning}")
        
        return {
            'lesson_number': lesson_number,
            'lesson_topic': lesson_topic,
            'content': final,
            'validation': validation,
            'status': 'success'
        }
    
    def save_lesson(self, lesson: Dict, output_dir: str = "data/outputs/html"):
        """Save lesson to HTML file"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        filename = f"Lesson_{lesson['lesson_number']:03d}_{lesson['lesson_topic'].replace(' ', '_')}.html"
        filepath = output_path / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(lesson['content'])
        
        print(f"✓ Saved: {filepath}")
        return str(filepath)


def main():
    """Main execution"""
    print("\n" + "="*70)
    print("CBE LESSON PLAN GENERATOR - AI POWERED")
    print("="*70 + "\n")
    
    # Initialize
    generator = AILessonGenerator()
    
    # Generate a test lesson
    print("\nGenerating test lesson...")
    
    result = generator.generate_lesson(
        subject="Physics",
        grade="Grade 10",
        strand="Electricity",
        substrand="Current Electricity",
        lesson_topic="Introduction to Current Electricity",
        lesson_number=1,
        phenomenon="Why do some electrical devices get hot when plugged in?",
        use_multi_model=False
    )
    
    if result['status'] == 'success':
        filepath = generator.save_lesson(result)
        
        print(f"\n{'='*70}")
        print(f"SUCCESS!")
        print(f"{'='*70}")
        print(f"Lesson saved to: {filepath}")
        print(f"Validation: {'✓ Valid' if result['validation']['is_valid'] else '✗ Has errors'}")
    else:
        print(f"\n✗ Generation failed: {result.get('error')}")


if __name__ == "__main__":
    main()
