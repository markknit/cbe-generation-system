"""
Generate perfectly formatted CBE lesson using Claude's native formatting ability
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


def generate_perfect_lesson():
    """Use Anthropic API to generate perfectly formatted lesson"""
    import anthropic
    
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    print("\n" + "="*70)
    print("GENERATING PERFECTLY FORMATTED LESSON")
    print("="*70)
    
    # Load the actual template
    with open('templates/cbe_lesson_template.md', 'r') as f:
        template = f.read()
    
    prompt = f"""You are generating a CBE lesson plan for Kenya following this template EXACTLY.

HERE IS YOUR TEMPLATE (study it carefully):
{template[:5000]}  

[Template continues with full example lessons...]

NOW GENERATE:
- Subject: Physics
- Grade: Grade 10
- Topic: Introduction to Current Electricity
- Lesson Number: 1
- Phenomenon: Why do electrical devices get hot when plugged in?

CRITICAL REQUIREMENTS:
1. Use the EXACT table format from the template (with | pipes for markdown tables)
2. Include ALL sections: A, B, C, D, E
3. Section C must have 5 columns with AT LEAST 3 detailed rows
4. Use Kenyan context (KSh, KPLC, local examples)
5. Include [ARES VIDEO: topic] placeholders
6. Use Think-Pair-Share, POE cycles
7. Teacher facilitation with WAIT TIME specified
8. Checkboxes (☐) in assessments

Match the style, detail, and structure of the template EXACTLY.

Generate the complete lesson now in markdown format."""
    
    print("→ Generating lesson with Claude Sonnet 4.5...")
    
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=16000,  # Allow very long output
        messages=[{"role": "user", "content": prompt}]
    )
    
    content = response.content[0].text
    
    print("✓ Lesson generated!")
    
    # Save markdown
    output_dir = Path("data/outputs/markdown")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    md_file = output_dir / "Lesson_001_Introduction_to_Current_Electricity.md"
    
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Saved: {md_file}")
    
    # Also save as text for easy viewing
    txt_file = output_dir / "Lesson_001_Introduction_to_Current_Electricity.txt"
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Also saved as: {txt_file}")
    
    print("\n" + "="*70)
    print("SUCCESS!")
    print("="*70)
    print(f"\nYou can:")
    print(f"1. View in any text editor: {txt_file}")
    print(f"2. Open in Word: {md_file}")
    print(f"3. Convert with: pandoc {md_file} -o lesson.docx")
    
    return str(md_file)


if __name__ == "__main__":
    try:
        generate_perfect_lesson()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
