"""

Professional CBE Lesson Plan Formatter - Matches Original Document Style
"""
from pathlib import Path


def add_professional_styling(html_content: str) -> str:
    """Add professional CSS styling matching CBE original format"""
    
    css = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CBE Lesson Plan - Kenya Competency-Based Curriculum</title>
    <style>
        @page {
            margin: 2cm;
        }
        
        body {
            font-family: 'Calibri', 'Arial', sans-serif;
            font-size: 11pt;
            line-height: 1.5;
            color: #000000;
            max-width: 210mm;
            margin: 0 auto;
            padding: 20px;
            background-color: #ffffff;
        }
        
        /* Main Headers */
        h1 {
            font-size: 16pt;
            font-weight: bold;
            color: #0070C0;
            text-align: center;
            margin: 20px 0 10px 0;
            text-transform: uppercase;
            border-bottom: 2px solid #0070C0;
            padding-bottom: 5px;
        }
        
        h2 {
            font-size: 14pt;
            font-weight: bold;
            color: #0070C0;
            margin: 25px 0 10px 0;
            border-bottom: 1px solid #0070C0;
            padding-bottom: 3px;
        }
        
        h3 {
            font-size: 12pt;
            font-weight: bold;
            color: #000000;
            margin: 15px 0 8px 0;
        }
        
        h4 {
            font-size: 11pt;
            font-weight: bold;
            color: #000000;
            margin: 10px 0 5px 0;
            font-style: italic;
        }
        
        p {
            margin: 8px 0;
            text-align: justify;
        }
        
        /* Tables - General */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 10pt;
            page-break-inside: avoid;
        }
        
        th {
            background-color: #4472C4;
            color: #FFFFFF;
            font-weight: bold;
            padding: 8px;
            border: 1px solid #2F5597;
            text-align: left;
            vertical-align: top;
        }
        
        td {
            padding: 8px;
            border: 1px solid #000000;
            vertical-align: top;
        }
        
        /* Learning Outcomes Table */
        .outcomes-table th {
            background-color: #70AD47;
            border: 1px solid #507E32;
        }
        
        .outcomes-table td {
            background-color: #E2EFDA;
        }
        
        /* Overview Table */
        .overview-table th {
            background-color: #5B9BD5;
            border: 1px solid #2E75B5;
            width: 30%;
        }
        
        .overview-table td {
            background-color: #FFFFFF;
        }
        
        /* 5-Column Implementation Framework - CRITICAL */
        .framework-table {
            margin: 20px 0;
            font-size: 9.5pt;
        }
        
        .framework-table th {
            background-color: #C65911;
            color: #FFFFFF;
            border: 1px solid #833C0C;
            font-size: 10pt;
            padding: 10px 6px;
            text-align: center;
        }
        
        .framework-table td {
            border: 1px solid #000000;
            padding: 8px;
            min-height: 80px;
        }
        
        /* Column widths for 5-column framework */
        .framework-table th:nth-child(1),
        .framework-table td:nth-child(1) {
            width: 22%;  /* Learner Experience */
        }
        
        .framework-table th:nth-child(2),
        .framework-table td:nth-child(2) {
            width: 15%;  /* Resource Link */
        }
        
        .framework-table th:nth-child(3),
        .framework-table td:nth-child(3) {
            width: 20%;  /* Teacher Moves */
        }
        
        .framework-table th:nth-child(4),
        .framework-table td:nth-child(4) {
            width: 23%;  /* Sensemaking Strategy */
        }
        
        .framework-table th:nth-child(5),
        .framework-table td:nth-child(5) {
            width: 20%;  /* Formative Assessment */
        }
        
        /* Lists */
        ul, ol {
            margin: 8px 0;
            padding-left: 25px;
        }
        
        li {
            margin: 5px 0;
        }
        
        /* Checkbox styling */
        .checkbox {
            font-family: 'Arial Unicode MS', Arial;
            margin-right: 5px;
        }
        
        /* Special boxes */
        .key-inquiry-box {
            background-color: #DEEBF7;
            border: 2px solid #2E75B5;
            padding: 12px;
            margin: 12px 0;
            font-weight: bold;
        }
        
        .safety-box {
            background-color: #FFF2CC;
            border: 2px solid #BF8F00;
            padding: 12px;
            margin: 12px 0;
        }
        
        .purpose-box {
            background-color: #E7E6E6;
            padding: 10px;
            margin: 10px 0;
            border-left: 4px solid #4472C4;
        }
        
        /* Reflection Section */
        .reflection-section {
            background-color: #F2F2F2;
            padding: 15px;
            margin: 20px 0;
            border: 1px solid #A6A6A6;
        }
        
        .reflection-section h3 {
            margin-top: 0;
            color: #0070C0;
        }
        
        .reflection-section ol {
            margin: 10px 0;
        }
        
        /* Summary Table Prompt */
        .summary-prompt {
            background-color: #FFF9E6;
            border: 2px solid #FFC000;
            padding: 15px;
            margin: 20px 0;
        }
        
        .summary-prompt h3 {
            margin-top: 0;
            color: #C65911;
        }
        
        /* Strong emphasis */
        strong, b {
            font-weight: bold;
            color: #000000;
        }
        
        /* Links */
        a {
            color: #0563C1;
            text-decoration: underline;
        }
        
        /* Section dividers */
        hr {
            border: none;
            border-top: 2px solid #0070C0;
            margin: 20px 0;
        }
        
        /* Print styles */
        @media print {
            body {
                margin: 0;
                padding: 0;
            }
            
            table {
                page-break-inside: avoid;
            }
            
            h1, h2, h3 {
                page-break-after: avoid;
            }
        }
        
        /* Document header style */
        .document-header {
            text-align: center;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #0070C0;
        }
        
        .document-header h1 {
            border: none;
            margin-bottom: 5px;
        }
        
        .lesson-metadata {
            font-size: 10pt;
            color: #595959;
            margin: 5px 0;
        }
    </style>
</head>
<body>
"""
    
    footer = """
</body>
</html>
"""
    
    # Check if content already has HTML structure
    if '<!DOCTYPE html>' in html_content or '<html' in html_content.lower():
        return html_content
    
    # Add CSS classes to tables
    styled_content = html_content
    
    # Try to identify and class different table types
    styled_content = styled_content.replace('<table>', '<table class="framework-table">')
    
    # Look for specific headers to identify table types
    if 'Knowledge' in styled_content and 'Skills' in styled_content and 'Attitudes' in styled_content:
        styled_content = styled_content.replace('<table class="framework-table">', '<table class="outcomes-table">', 1)
    
    if 'Key Inquiry Question' in styled_content or 'Purpose' in styled_content:
        # Find next table tag after these keywords
        import re
        pattern = r'(Key Inquiry Question|Purpose in Storyline).*?<table class="framework-table">'
        styled_content = re.sub(pattern, lambda m: m.group(0).replace('framework-table', 'overview-table'), styled_content, count=1, flags=re.DOTALL)
    
    return css + styled_content + footer


def format_lesson_file(input_path: str, output_path: str = None):
    """Format a lesson file with professional styling"""
    
    input_file = Path(input_path)
    
    if not input_file.exists():
        print(f"✗ File not found: {input_path}")
        return
    
    # Read content
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add professional styling
    styled_content = add_professional_styling(content)
    
    # Save
    output_file = Path(output_path) if output_path else input_file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(styled_content)
    
    print(f"✓ Professionally formatted: {output_file}")


def format_all_lessons(directory: str = "data/outputs/html"):
    """Format all lesson files with professional styling"""
    
    lesson_dir = Path(directory)
    
    if not lesson_dir.exists():
        print(f"✗ Directory not found: {directory}")
        return
    
    html_files = list(lesson_dir.glob("*.html"))
    
    if not html_files:
        print(f"✗ No HTML files found in {directory}")
        return
    
    print(f"Applying professional formatting to {len(html_files)} lessons...")
    
    for html_file in html_files:
        format_lesson_file(str(html_file))
    
    print(f"\n✅ All {len(html_files)} lessons professionally formatted!")
    print(f"✓ Matched original CBE document style")


if __name__ == "__main__":
    format_all_lessons()
