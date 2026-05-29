#!/usr/bin/env python3
"""
extract_generator_data.py
==========================
Extracts UNIT, LESSONS, and build-function data from an existing generator
script and writes a clean data module for the universal generator.

Run from project root:
    python3 scripts/extract_generator_data.py <generator_file> <output_name>

Example:
    python3 scripts/extract_generator_data.py \
        generators/biology_1_3_cell_structure.js \
        bio_1_3

Output: generators/data/bio_1_3_data.js
"""

import re
import sys
import os

def extract_block(src, start_marker, end_marker):
    """Extract text between start_marker and end_marker (inclusive of start)."""
    start = src.find(start_marker)
    if start == -1:
        return None, -1
    end = src.find(end_marker, start)
    if end == -1:
        return src[start:], start
    return src[start:end], start

def extract_const(src, const_name):
    """
    Extract a const declaration: const NAME = ...;
    Handles nested braces/brackets to find the matching end.
    Returns the full declaration text.
    """
    marker = f'\nconst {const_name} = '
    start_idx = src.find(marker)
    if start_idx == -1:
        marker = f'\nconst {const_name}= '
        start_idx = src.find(marker)
    if start_idx == -1:
        return None

    # Find the opening bracket/brace
    i = start_idx + len(marker)
    while i < len(src) and src[i] in ' \t\n':
        i += 1

    if i >= len(src):
        return None

    open_char = src[i]
    close_char = {'[': ']', '{': '}'}.get(open_char)
    if not close_char:
        return None

    # Count nested brackets
    depth = 0
    in_string = False
    string_char = None
    j = i

    while j < len(src):
        ch = src[j]

        if in_string:
            if ch == '\\':
                j += 2
                continue
            if ch == string_char:
                in_string = False
        else:
            if ch in ('"', "'", '`'):
                in_string = True
                string_char = ch
            elif ch == open_char:
                depth += 1
            elif ch == close_char:
                depth -= 1
                if depth == 0:
                    return src[start_idx + 1: j + 1].strip()
        j += 1

    return None


def extract_meta_from_build(src):
    """Extract title/subtitle from buildSoW function."""
    meta = {}

    # Title and subtitle
    title_m = re.search(r"const title = '([^']+)'", src)
    sub_m   = re.search(r"const subtitle = '([^']+)'", src)
    if title_m:   meta['titleDoc']    = title_m.group(1)
    if sub_m:     meta['subtitleDoc'] = sub_m.group(1)

    return meta


def extract_fe_data(src):
    """
    Extract Final Explanation data from buildFinalExplanation function.
    Returns a comment block with the FE section structure for manual completion.
    """
    fe_start = src.find('async function buildFinalExplanation')
    fe_end   = src.find('\nasync function ', fe_start + 10)
    if fe_start == -1:
        return None
    fe_block = src[fe_start: fe_end if fe_end != -1 else fe_start + 5000]
    return fe_block


def extract_st_data(src):
    """Extract Summary Table data from buildSummaryTable function."""
    st_start = src.find('async function buildSummaryTable')
    st_end   = src.find('\nasync function ', st_start + 10)
    if st_start == -1:
        return None, None
    return src[st_start: st_end if st_end != -1 else st_start + 5000]


def infer_meta(gen_file, src):
    """Infer META fields from the generator filename and content."""
    basename = os.path.basename(gen_file).replace('.js', '')
    parts    = basename.split('_')
    subject_map = {'biology': 'Biology', 'math': 'Mathematics',
                   'chemistry': 'Chemistry', 'physics': 'Physics'}
    subject = subject_map.get(parts[0], 'Biology')

    # Substrand number e.g. 1_3 → 1.3
    ss_num = ''
    if len(parts) >= 3:
        ss_num = f"{parts[1]}.{parts[2]}"

    # Output dir
    if subject == 'Biology':
        out_dir = f'Grade 10 Bio/Bio {ss_num}'
    elif subject == 'Mathematics':
        out_dir = f'Grade 10 Math/Math {ss_num} {" ".join(p.capitalize() for p in parts[3:])}'
    else:
        out_dir = f'Grade 10 {subject}/{subject} {ss_num}'

    # File prefix from title in buildSoW
    prefix_m = re.search(r"const title\s*=\s*'([^']+)'", src)
    file_prefix = ''
    if prefix_m:
        words = re.findall(r'[A-Z][a-z]+', prefix_m.group(1))
        file_prefix = ''.join(words[:4])

    # Column label detection
    col3 = 'Teacher Moves'
    if "cell('Teacher Actions'" in src or 'Teacher Actions' in src:
        col3 = 'Teacher Actions'

    col5 = 'Formative Assessment Strategy'
    if "cell('Assessment Strategy'" in src and 'Formative Assessment Strategy' not in src:
        col5 = 'Assessment Strategy'

    return {
        'subject':     subject,
        'grade':       10,
        'outputDir':   out_dir,
        'filePrefix':  file_prefix or f'{subject}{ss_num.replace(".", "")}',
        'col3Label':   col3,
        'col5Label':   col5,
    }


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 scripts/extract_generator_data.py <generator.js> <output_name>")
        sys.exit(1)

    gen_file    = sys.argv[1]
    output_name = sys.argv[2]
    output_path = f'generators/data/{output_name}_data.js'

    with open(gen_file) as f:
        src = f.read()

    print(f"Reading {gen_file} ...")

    # Extract UNIT
    unit_src = extract_const(src, 'UNIT')
    if not unit_src:
        print("ERROR: Could not find UNIT declaration")
        sys.exit(1)
    print(f"  ✓ UNIT extracted ({len(unit_src)} chars)")

    # Extract LESSONS
    lessons_src = extract_const(src, 'LESSONS')
    if not lessons_src:
        print("ERROR: Could not find LESSONS declaration")
        sys.exit(1)
    print(f"  ✓ LESSONS extracted ({len(lessons_src)} chars)")

    # Infer META
    meta = infer_meta(gen_file, src)
    build_meta = extract_meta_from_build(src)
    meta.update(build_meta)
    print(f"  ✓ META inferred: {meta}")

    # Write data file
    os.makedirs('generators/data', exist_ok=True)

    with open(output_path, 'w') as f:
        f.write(f"'use strict';\n")
        f.write(f"/**\n")
        f.write(f" * {output_name}_data.js — Sub-strand data for universal generator\n")
        f.write(f" * Auto-extracted from {os.path.basename(gen_file)}\n")
        f.write(f" * Run: node generators/generate.js {output_name}\n")
        f.write(f" */\n\n")

        # META
        f.write("const META = {\n")
        for k, v in meta.items():
            if isinstance(v, str):
                f.write(f"  {k}: {repr(v)},\n")
            else:
                f.write(f"  {k}: {v},\n")
        f.write("};\n\n")

        # UNIT
        f.write(f"const {unit_src};\n\n")

        # LESSONS
        f.write(f"const {lessons_src};\n\n")

        # FINAL_EXPLANATION and SUMMARY_TABLE — scaffold for manual completion
        f.write("// ── Final Explanation ──────────────────────────────────────────────────────\n")
        f.write("// TODO: extract from buildFinalExplanation() in the original generator\n")
        f.write("// See generators/data/SCHEMA.md for structure\n")
        f.write("const FINAL_EXPLANATION = null;  // fill in or extract manually\n\n")

        f.write("// ── Summary Table ──────────────────────────────────────────────────────────\n")
        f.write("// TODO: extract from buildSummaryTable() in the original generator\n")
        f.write("const SUMMARY_TABLE = null;  // fill in or extract manually\n\n")

        # Exports
        f.write("module.exports = { META, UNIT, LESSONS, FINAL_EXPLANATION, SUMMARY_TABLE };\n")

    print(f"\n✓ Written to {output_path}")
    print(f"\nNext step:")
    print(f"  node generators/generate.js {output_name}")
    print(f"\nNote: FINAL_EXPLANATION and SUMMARY_TABLE are null stubs.")
    print(f"The SoW will generate correctly. FE and ST need manual extraction from")
    print(f"buildFinalExplanation() and buildSummaryTable() in the original generator.")
    print(f"This will be automated in a future pass.")


if __name__ == '__main__':
    main()
