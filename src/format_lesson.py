"""
Format and style CBE lesson plans for better readability
"""
from pathlib import Path


def add_styling(html_content: str) -> str:
    """Add CSS styling to lesson HTML"""
    
    css = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CBE Lesson Plan</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        
        .lesson-container {
            background-color: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-top: 0;
        }
        
        h2 {
            color: #2980b9;
            margin-top: 30px;
            margin-bottom: 15px;
            border-left: 4px solid #3498db;
            padding-left: 15px;
        }
        
        h3 {
            color: #34495e;
            margin-top: 20px;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background-color: white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        th {
            background-color: #3498db;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            border: 1px solid #2980b9;
        }
        
        td {
            padding: 12px;
            border: 1px solid #ddd;
            vertical-align: top;
        }
        
        tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        
        tr:hover {
            background-color: #e8f4f8;
        }
        
        .outcomes-table th {
            background-color: #27ae60;
        }
        
        .framework-table th {
            background-color: #e74c3c;
            font-size: 0.9em;
        }
        
        .framework-table td {
            font-size: 0.95em;
        }
        
        ul, ol {
            margin: 10px 0;
            padding-left: 30px;
        }
        
        li {
            margin: 8px 0;
        }
        
        .safety-note {
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }
        
        .key-inquiry {
            background-color: #d1ecf1;
            border-left: 4px solid #17a2b8;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
            font-weight: 500;
        }
        
        .reflection-questions {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 4px;
            margin: 20px 0;
        }
        
        .reflection-questions ol {
            margin: 10px 0;
        }
        
        .summary-prompt {
            background-color: #e7f3ff;
            padding: 20px;
            border-radius: 4px;
            border: 2px solid #3498db;
            margin: 20px 0;
        }
        
        strong {
            color: #2c3e50;
        }
        
        .checkbox {
            margin-right: 8px;
        }
        
        @media print {
            body {
                background-color: white;
            }
            .lesson-container {
                box-shadow: none;
            }
        }
    </style>
</head>
<body>
    <div class="lesson-container">
"""
    
    footer = """
    </div>
</body>
</html>
"""
    
    # Check if content already has HTML structure
    if '<html' in html_content.lower():
        return html_content
    
    # Add styling
    return css + html_content + footer


def format_lesson_file(input_path: str, output_path: str = None):
    """Format a lesson file with proper styling"""
    
    input_file = Path(input_path)
    
    if not input_file.exists():
        print(f"✗ File not found: {input_path}")
        return
    
    # Read content
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add styling
    styled_content = add_styling(content)
    
    # Save
    output_file = Path(output_path) if output_path else input_file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(styled_content)
    
    print(f"✓ Formatted: {output_file}")


def format_all_lessons(directory: str = "data/outputs/html"):
    """Format all lesson files in directory"""
    
    lesson_dir = Path(directory)
    
    if not lesson_dir.exists():
        print(f"✗ Directory not found: {directory}")
        return
    
    html_files = list(lesson_dir.glob("*.html"))
    
    if not html_files:
        print(f"✗ No HTML files found in {directory}")
        return
    
    print(f"Formatting {len(html_files)} lesson files...")
    
    for html_file in html_files:
        format_lesson_file(str(html_file))
    
    print(f"\n✓ All {len(html_files)} lessons formatted!")


if __name__ == "__main__":
    format_all_lessons()
