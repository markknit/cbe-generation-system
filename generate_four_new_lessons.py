#!/usr/bin/env python3
"""
Generate 4 New Sample Lessons
- Physics Lesson 2
- Chemistry Lesson 2
- Biology Lesson 2
- Mathematics Lesson 1 (NEW)
"""
import sys
sys.path.insert(0, 'src')

from production_generator_complete import ProductionLessonGenerator


def main():
    """Generate 4 new sample lessons"""
    
    print("\n" + "="*70)
    print("GENERATING 4 NEW SAMPLE LESSONS")
    print("="*70 + "\n")
    
    generator = ProductionLessonGenerator()
    
    # Define 4 new lessons
    lessons = [
        {
            'subject': 'Physics',
            'grade': 'Grade 10',
            'strand': 'Electricity and Magnetism',
            'substrand': 'Current Electricity',
            'topic': 'Ohms Law and Resistance',
            'number': 2,
            'phenomenon': 'Why do some materials conduct electricity better than others?',
            'total_lessons': 22
        },
        {
            'subject': 'Chemistry',
            'grade': 'Grade 10',
            'strand': 'Matter and Its Changes',
            'substrand': 'Atomic Structure',
            'topic': 'Electron Configuration and Periodic Trends',
            'number': 2,
            'phenomenon': 'Why do elements in the same group have similar properties?',
            'total_lessons': 18
        },
        {
            'subject': 'Biology',
            'grade': 'Grade 10',
            'strand': 'Cell Biology',
            'substrand': 'Cell Structure and Function',
            'topic': 'Cell Membrane and Transport',
            'number': 2,
            'phenomenon': 'How do cells control what enters and exits?',
            'total_lessons': 15
        },
        {
            'subject': 'Mathematics',
            'grade': 'Grade 10',
            'strand': 'Algebra',
            'substrand': 'Quadratic Expressions and Equations',
            'topic': 'Introduction to Quadratic Equations',
            'number': 1,
            'phenomenon': 'How can we model the path of a thrown ball mathematically?',
            'total_lessons': 20
        }
    ]
    
    results = []
    
    # Generate each lesson
    for i, lesson_spec in enumerate(lessons, 1):
        print(f"\n{'='*70}")
        print(f"GENERATING LESSON {i} of {len(lessons)}: {lesson_spec['subject']} - {lesson_spec['topic']}")
        print(f"{'='*70}")
        
        try:
            # Include overview only for first lesson in substrand (Math in this case)
            include_overview = (lesson_spec['number'] == 1)
            
            result = generator.generate_complete_lesson(
                subject=lesson_spec['subject'],
                grade=lesson_spec['grade'],
                strand=lesson_spec['strand'],
                substrand=lesson_spec['substrand'],
                topic=lesson_spec['topic'],
                number=lesson_spec['number'],
                phenomenon=lesson_spec['phenomenon'],
                total_lessons=lesson_spec['total_lessons'],
                include_overview=include_overview
            )
            
            results.append({
                'subject': lesson_spec['subject'],
                'topic': lesson_spec['topic'],
                'number': lesson_spec['number'],
                'status': 'SUCCESS',
                'filepath': result['filepath']
            })
            
            print(f"\n✓ Completed: {lesson_spec['subject']} Lesson {lesson_spec['number']}")
            
        except Exception as e:
            print(f"\n✗ ERROR: {e}")
            import traceback
            traceback.print_exc()
            
            results.append({
                'subject': lesson_spec['subject'],
                'topic': lesson_spec['topic'],
                'number': lesson_spec['number'],
                'status': 'FAILED',
                'error': str(e)
            })
    
    # Summary
    print("\n" + "="*70)
    print("GENERATION COMPLETE - SUMMARY")
    print("="*70 + "\n")
    
    successful = 0
    failed = 0
    
    for result in results:
        status_icon = "✓" if result['status'] == 'SUCCESS' else "✗"
        print(f"{status_icon} {result['subject']} Lesson {result['number']}: {result['topic']}")
        
        if result['status'] == 'SUCCESS':
            successful += 1
            print(f"    File: {result['filepath']}")
        else:
            failed += 1
            print(f"    Error: {result.get('error', 'Unknown error')}")
        print()
    
    print("="*70)
    print(f"Results: {successful} successful, {failed} failed")
    print("="*70 + "\n")
    
    if successful > 0:
        print("✓ New lesson files created in: data/outputs/docx/\n")
        print("To verify Section C in all files, run:")
        print("  python3 verify_section_c.py")
        print("\nTo analyze column widths, open the files in Word and check:")
        print("  - Sub-strand overview table: narrower left column, wider right column")
        print("  - Section A table: narrower left column, wider right column")
        print("  - Section B table: narrower left column, wider right column")
        print("  - Section C table: 5 equal-width columns\n")


if __name__ == "__main__":
    main()
