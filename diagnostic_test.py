#!/usr/bin/env python3
"""
Diagnostic Script - Debug Section C Generation
This will show you EXACTLY what Claude is generating
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, 'src')
from resource_manager import ResourceManager

load_dotenv()

def test_generation():
    """Generate content and show exactly what we get"""
    
    print("\n" + "="*70)
    print("DIAGNOSTIC: SECTION C GENERATION TEST")
    print("="*70 + "\n")
    
    import anthropic
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: No API key found")
        return
    
    client = anthropic.Anthropic(api_key=api_key)
    
    # Simplified, explicit prompt
    prompt = """Generate a CBE lesson plan for Kenya.

Subject: Chemistry
Topic: Introduction to Atoms and Elements

You MUST include ALL 5 sections. Return in this EXACT format:

===SECTION A: LEARNING OUTCOMES===
Knowledge:
- Point 1
- Point 2

Skills:
- Point 1

Attitudes:
- Point 1

Practices:
- Point 1

===SECTION B: OVERVIEW===
KeyQuestion: Why do elements have different properties?
Purpose: This lesson introduces atomic structure
Safety: n/a

===SECTION C: FRAMEWORK===

ROW 1 - PREDICT:
Experience: Students predict why elements differ
Resources: Materials list
Teacher: Questions with WAIT TIME: 10 seconds
Sensemaking: Think-Pair-Share
Assessment: Checklist

ROW 2 - OBSERVE:
Experience: Observe element samples
Resources: Materials
Teacher: Facilitation
Sensemaking: Data collection
Assessment: Criteria

ROW 3 - EXPLAIN:
Experience: Build explanations
Resources: Materials
Teacher: Questions only
Sensemaking: Class discussion
Assessment: Exit ticket

ROW 4 - DQB:
Experience: Generate questions
Resources: Chart paper
Teacher: Record questions
Sensemaking: Question list
Assessment: DQB started

ROW 5 - INITIAL MODEL:
Experience: Draw atomic models
Resources: Drawing materials
Teacher: Facilitate
Sensemaking: Model creation
Assessment: Model quality

ROW 6 - KENYA CONTEXT:
Experience: Kenya applications
Resources: Local examples
Teacher: Discuss
Sensemaking: Applications
Assessment: Context connections

ROW 7 - MODEL REVISION:
Experience: Revise models
Resources: Original models
Teacher: Compare
Sensemaking: Revisions
Assessment: Improvements

===SECTION D: REFLECTION===
1. Question 1
2. Question 2
3. Question 3

===SECTION E: SUMMARY PROMPT===
What did I learn?

Generate this complete structure now. Do not skip Section C."""

    print("→ Calling Claude API...")
    print(f"→ Prompt length: {len(prompt)} characters\n")
    
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=12000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    content = response.content[0].text
    
    print("="*70)
    print("RAW OUTPUT FROM CLAUDE:")
    print("="*70)
    print(content)
    print("="*70)
    
    # Save to file
    output_file = "diagnostic_output.txt"
    with open(output_file, 'w') as f:
        f.write("DIAGNOSTIC OUTPUT\n")
        f.write("="*70 + "\n")
        f.write(f"Model: claude-sonnet-4-5-20250929\n")
        f.write(f"Max tokens: 12000\n")
        f.write(f"Output length: {len(content)} characters\n")
        f.write("="*70 + "\n\n")
        f.write(content)
    
    print(f"\n✓ Full output saved to: {output_file}")
    
    # Analysis
    print("\n" + "="*70)
    print("ANALYSIS:")
    print("="*70)
    
    print(f"Total output length: {len(content)} characters")
    
    sections_found = []
    for section in ['A', 'B', 'C', 'D', 'E']:
        if f'===SECTION {section}:' in content:
            sections_found.append(section)
            print(f"  ✓ Section {section} found")
        else:
            print(f"  ✗ Section {section} MISSING")
    
    if 'C' in sections_found:
        # Count rows in Section C
        section_c_start = content.find('===SECTION C:')
        section_c_end = content.find('===SECTION D:', section_c_start)
        if section_c_end == -1:
            section_c_end = len(content)
        
        section_c_content = content[section_c_start:section_c_end]
        row_count = section_c_content.count('ROW ')
        
        print(f"\n  Section C analysis:")
        print(f"    - Length: {len(section_c_content)} characters")
        print(f"    - Rows detected: {row_count}")
        
        if row_count < 7:
            print(f"    ⚠ WARNING: Expected 7 rows, found {row_count}")
    else:
        print("\n  ✗✗✗ SECTION C IS COMPLETELY MISSING ✗✗✗")
        
        # Check if it appears anywhere else
        if 'SECTION C' in content or 'Section C' in content:
            print("    (But 'Section C' text appears somewhere - check diagnostic_output.txt)")
    
    print("\n" + "="*70)
    print(f"Full output saved to: {output_file}")
    print("Please examine this file to see what Claude actually generated")
    print("="*70 + "\n")


if __name__ == "__main__":
    test_generation()
