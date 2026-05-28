"""
CBE Lesson Plan Generator
Generates Kenya CBE lesson plans using templates and AI models
"""
import os
import sys
from pathlib import Path
from typing import Dict, List
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from template_loader import TemplateLoader

# Load environment variables
load_dotenv()


class LessonPlanGenerator:
    """Generate CBE lesson plans using templates and AI"""
    
    def __init__(self):
        """Initialize generator with template loader and API clients"""
        print("Initializing CBE Lesson Plan Generator...")
        
        # Load template
        self.template_loader = TemplateLoader()
        print(f"✓ Template loaded: {self.template_loader.template_config.get('template_type')}")
        
        # Initialize API clients (will add later)
        self._init_api_clients()
        
    def _init_api_clients(self):
        """Initialize API clients for generation"""
        # Check for API keys
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        
        if not all([self.anthropic_key, self.openai_key, self.gemini_key]):
            print("⚠️  Warning: Some API keys missing. Check .env file.")
        else:
            print("✓ API keys loaded")
    
    def generate_lesson(
        self,
        subject: str,
        grade: str,
        strand: str,
        substrand: str,
        lesson_topic: str,
        lesson_number: int = 1,
        phenomenon: str = None
    ) -> Dict:
        """Generate a single lesson plan"""
        
        print(f"\nGenerating Lesson {lesson_number}: {lesson_topic}")
        print(f"Subject: {subject}, Grade: {grade}")
        print(f"Strand: {strand}, Sub-strand: {substrand}")
        
        # Get system prompt with template
        system_prompt = self.template_loader.get_system_prompt_for_generation(
            subject=subject,
            grade=grade,
            strand=strand,
            substrand=substrand,
            lesson_topic=lesson_topic,
            phenomenon=phenomenon
        )
        
        print(f"✓ System prompt prepared ({len(system_prompt)} chars)")
        
        # For now, return the prompt (we'll add AI generation next)
        return {
            'lesson_number': lesson_number,
            'lesson_topic': lesson_topic,
            'system_prompt': system_prompt,
            'status': 'prompt_ready'
        }
    
    def generate_lesson_sequence(
        self,
        subject: str,
        grade: str,
        strand: str,
        substrand: str,
        lessons: List[Dict],
        phenomenon: str = None
    ) -> List[Dict]:
        """Generate a sequence of lessons"""
        
        print(f"\n{'='*70}")
        print(f"GENERATING LESSON SEQUENCE")
        print(f"{'='*70}")
        print(f"Subject: {subject}")
        print(f"Grade: {grade}")
        print(f"Strand: {strand}")
        print(f"Sub-strand: {substrand}")
        print(f"Number of lessons: {len(lessons)}")
        print(f"{'='*70}\n")
        
        results = []
        
        for i, lesson_info in enumerate(lessons, 1):
            result = self.generate_lesson(
                subject=subject,
                grade=grade,
                strand=strand,
                substrand=substrand,
                lesson_topic=lesson_info.get('topic'),
                lesson_number=i,
                phenomenon=phenomenon
            )
            results.append(result)
        
        print(f"\n{'='*70}")
        print(f"GENERATION COMPLETE")
        print(f"{'='*70}")
        print(f"Total lessons prepared: {len(results)}")
        
        return results


def main():
    """Main execution function"""
    print("\n" + "="*70)
    print("CBE LESSON PLAN GENERATOR")
    print("="*70 + "\n")
    
    # Initialize generator
    generator = LessonPlanGenerator()
    
    # Example: Generate a single lesson
    print("\n--- TEST: Generate Single Lesson ---")
    
    result = generator.generate_lesson(
        subject="Physics",
        grade="Grade 10",
        strand="Electricity",
        substrand="Current Electricity",
        lesson_topic="Introduction to Current Electricity",
        lesson_number=1,
        phenomenon="Why do some electrical devices get hot when plugged in?"
    )
    
    print(f"\n✓ Lesson prompt prepared")
    print(f"  Prompt length: {len(result['system_prompt'])} characters")
    print(f"  Status: {result['status']}")
    
    # Example: Generate lesson sequence
    print("\n--- TEST: Generate Lesson Sequence ---")
    
    lessons = [
        {'topic': 'Introduction to Current Electricity'},
        {'topic': 'Ohm\'s Law'},
        {'topic': 'Series and Parallel Circuits'}
    ]
    
    results = generator.generate_lesson_sequence(
        subject="Physics",
        grade="Grade 10",
        strand="Electricity",
        substrand="Current Electricity",
        lessons=lessons,
        phenomenon="Why do some electrical devices get hot when plugged in?"
    )
    
    print(f"\n✓ {len(results)} lesson prompts prepared")
    print("\nNext step: Add AI model integration to actually generate content")
    
    return results


if __name__ == "__main__":
    main()
