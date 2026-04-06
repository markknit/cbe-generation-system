#!/usr/bin/env python3
"""
Flexible Lesson Generator - Specify any subject/topic
"""
import sys
sys.path.insert(0, 'src')

from production_generator_complete import ProductionLessonGenerator

def main():
    """Generate lesson with command-line arguments or interactive prompts"""
    
    generator = ProductionLessonGenerator()
    
    # You can modify these values or make them command-line args
    lessons_to_generate = [
        {
            'subject': 'Chemistry',
            'grade': 'Grade 10',
            'strand': 'Matter and Its Changes',
            'substrand': 'Atomic Structure',
            'topic': 'Introduction to Atoms and Elements',
            'number': 1,
            'phenomenon': 'Why do different elements have different properties?',
            'total_lessons': 18
        },
        {
            'subject': 'Chemistry',
            'grade': 'Grade 10',
            'strand': 'Matter and Its Changes',
            'substrand': 'Atomic Structure',
            'topic': 'Electron Configuration',
            'number': 2,
            'phenomenon': 'Why do elements form specific types of bonds?',
            'total_lessons': 18
        },
        {
            'subject': 'Biology',
            'grade': 'Grade 10',
            'strand': 'Cell Biology',
            'substrand': 'Cell Structure and Function',
            'topic': 'Introduction to Cells',
            'number': 1,
            'phenomenon': 'How do our bodies heal wounds?',
            'total_lessons': 15
        },
        # Add more lessons here
    ]
    
    # Generate each lesson
    for i, lesson_spec in enumerate(lessons_to_generate, 1):
        print(f"\n{'='*70}")
        print(f"GENERATING LESSON {i} of {len(lessons_to_generate)}")
        print(f"{'='*70}")
        
        # Include overview only on first lesson of each substrand
        include_overview = lesson_spec['number'] == 1
        
        result = generator.generate_complete_lesson(
            subject=lesson_spec['subject'],
            grade=lesson_spec['grade'],
            strand=lesson_spec['strand'],
            substrand=lesson_spec['substrand'],
            topic=lesson_spec['topic'],
            number=lesson_spec['number'],
            phenomenon=lesson_spec.get('phenomenon'),
            total_lessons=lesson_spec['total_lessons'],
            include_overview=include_overview
        )
        
        print(f"\n✓ Lesson {i} complete: {result['filepath']}")
    
    print(f"\n{'='*70}")
    print(f"ALL LESSONS GENERATED!")
    print(f"{'='*70}")
    print(f"\nGenerated {len(lessons_to_generate)} lessons")
    print(f"Check: data/outputs/docx/")


if __name__ == "__main__":
    main()
