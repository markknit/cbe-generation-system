#!/usr/bin/env python3
"""
Test Script - Generate 3 Lessons to Verify Fix
Physics, Chemistry, and Biology lessons
"""
import sys
sys.path.insert(0, 'src')

from production_generator_complete import ProductionLessonGenerator


def main():
    """Generate 3 test lessons"""
    
    print("\n" + "="*70)
    print("GENERATING 3 TEST LESSONS")
    print("="*70 + "\n")
    
    generator = ProductionLessonGenerator()
    
    # Define the 3 test lessons
    lessons = [
        {
            'subject': 'Physics',
            'grade': 'Grade 10',
            'strand': 'Electricity and Magnetism',
            'substrand': 'Current Electricity',
            'topic': 'Introduction to Current Electricity',
            'number': 1,
            'phenomenon': 'Why do electrical devices get hot when plugged in?',
            'total_lessons': 22
        },
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
            'subject': 'Biology',
            'grade': 'Grade 10',
            'strand': 'Cell Biology',
            'substrand': 'Cell Structure and Function',
            'topic': 'Introduction to Cells',
            'number': 1,
            'phenomenon': 'How do our bodies heal wounds?',
            'total_lessons': 15
        }
    ]
    
    results = []
    
    # Generate each lesson
    for i, lesson_spec in enumerate(lessons, 1):
        print(f"\n{'='*70}")
        print(f"GENERATING LESSON {i} of {len(lessons)}: {lesson_spec['subject']}")
        print(f"{'='*70}")
        
        try:
            result = generator.generate_complete_lesson(
                subject=lesson_spec['subject'],
                grade=lesson_spec['grade'],
                strand=lesson_spec['strand'],
                substrand=lesson_spec['substrand'],
                topic=lesson_spec['topic'],
                number=lesson_spec['number'],
                phenomenon=lesson_spec['phenomenon'],
                total_lessons=lesson_spec['total_lessons'],
                include_overview=True  # Include sub-strand overview for each
            )
            
            results.append({
                'subject': lesson_spec['subject'],
                'status': 'SUCCESS',
                'filepath': result['filepath']
            })
            
            print(f"✓ {lesson_spec['subject']} lesson completed")
            
        except Exception as e:
            print(f"✗ ERROR generating {lesson_spec['subject']}: {e}")
            results.append({
                'subject': lesson_spec['subject'],
                'status': 'FAILED',
                'error': str(e)
            })
    
    # Summary
    print("\n" + "="*70)
    print("GENERATION COMPLETE - SUMMARY")
    print("="*70 + "\n")
    
    for result in results:
        status_icon = "✓" if result['status'] == 'SUCCESS' else "✗"
        print(f"{status_icon} {result['subject']}: {result['status']}")
        if result['status'] == 'SUCCESS':
            print(f"    File: {result['filepath']}")
    
    print("\n" + "="*70)
    print("NEXT STEPS:")
    print("="*70)
    print("\n1. Verify all 3 files were created:")
    print("   ls -lh data/outputs/docx/")
    print("\n2. Analyze each file to check Section C:")
    print("   python3 analyze_docx.py data/outputs/docx/Lesson_001_Introduction_to_Current_Electricity.docx")
    print("   python3 analyze_docx.py data/outputs/docx/Lesson_001_Introduction_to_Atoms_and_Elements.docx")
    print("   python3 analyze_docx.py data/outputs/docx/Lesson_001_Introduction_to_Cells.docx")
    print("\n3. Or analyze all at once:")
    print("   for file in data/outputs/docx/Lesson_001_*.docx; do")
    print("       echo ''; echo \"Analyzing: $file\"")
    print("       python3 analyze_docx.py \"$file\" | grep -E '(ANALYZING|Section C|Implementation|ROW)'")
    print("   done")
    print("\n4. Open the files in Word to visually verify Section C appears!\n")


if __name__ == "__main__":
    main()
