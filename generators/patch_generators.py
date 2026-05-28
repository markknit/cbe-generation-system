#!/usr/bin/env python3
"""
patch_generators.py — Batch ARES integration patcher
=====================================================
Applies the ARES resource integration to all generator scripts
except biology_1_3_cell_structure.js (already done).

Run from project root:
    python3 scripts/patch_generators.py

Each generator gets:
  1. require('./aresResources') added after path require
  2. aresRes lookup added inside sectionC()
  3. ph.resource / f.resource replaced with buildResourceParagraphs()
  4. TableLayoutType added to imports and makeTable
  5. aresKeywords added to each lesson object
"""

import re
import os

GENERATORS_DIR = 'generators'

# ── Per-generator config ─────────────────────────────────────────────────────
# Each entry: filename, substrand string, subject, loop_var (ph or f),
#             col_var (cw or CW), lessons list of (num, title, keywords)

GENERATORS = [
    {
        'file':      'biology_1_1_introduction.js',
        'substrand': 'Introduction to Biology',
        'subject':   'Biology',
        'loop_var':  'ph',
        'col_var':   'cw',
        'lessons': [
            (1,  'What is Biology',                  'biology living organisms scientific study'),
            (2,  'Branches of Biology',              'biology branches ecology genetics zoology'),
            (3,  'Scientific Method',                'scientific method hypothesis experiment observation'),
            (4,  'Laboratory Safety',                'laboratory safety equipment biology practical'),
            (5,  'Biology and Society',              'biology society Kenya applications careers'),
            (6,  'Review',                           'biology review summary assessment'),
        ],
    },
    {
        'file':      'biology_2_1_plant_nutrition.js',
        'substrand': 'Nutrition in Plants',
        'subject':   'Biology',
        'loop_var':  'f',
        'col_var':   'CW',
        'lessons': [
            (1,  'Pumpkin Mystery Phenomenon Launch', 'photosynthesis plant growth phenomenon'),
            (2,  'Types of Nutrition',               'autotrophic heterotrophic nutrition plants'),
            (3,  'Chloroplast Structure',            'chloroplast structure thylakoid grana stroma'),
            (4,  'Light Dependent Reactions',        'light stage photolysis ATP NADPH oxygen'),
            (5,  'Dark Stage Calvin Cycle',          'Calvin cycle carbon dioxide fixation glucose'),
            (6,  'Factors Affecting Photosynthesis', 'limiting factors light carbon dioxide temperature'),
            (7,  'Adaptations Kenyan Plants',        'leaf adaptations photosynthesis Kenya ecosystems'),
            (8,  'Heterotrophic Plants',             'parasitic carnivorous saprophytic Striga'),
            (9,  'Significance of Photosynthesis',  'photosynthesis significance food chains oxygen'),
            (10, 'Research Kenyan Applications',    'photosynthesis Kenya tea sugarcane agriculture'),
            (11, 'Synthesis',                       'photosynthesis synthesis model review'),
            (12, 'Final Explanation',               'photosynthesis final explanation assessment'),
        ],
    },
    {
        'file':      'math_2_2_reflection_congruence.js',
        'substrand': 'Reflection and Congruence',
        'subject':   'Mathematics',
        'loop_var':  'f',
        'col_var':   'CW',
        'lessons': [
            (1,  'Introduction to Reflection',      'reflection symmetry transformation geometry'),
            (2,  'Reflection on Axes',              'reflection x-axis y-axis coordinate plane'),
            (3,  'Congruence',                      'congruence congruent shapes transformation'),
            (4,  'Properties of Reflection',        'reflection properties distance angle invariant'),
            (5,  'Reflection in Practice',          'reflection real life applications symmetry'),
            (6,  'Review and Assessment',           'reflection congruence review assessment'),
        ],
    },
    {
        'file':      'math_2_3_rotation.js',
        'substrand': 'Rotation',
        'subject':   'Mathematics',
        'loop_var':  'f',
        'col_var':   'CW',
        'lessons': [
            (1,  'Introduction to Rotation',        'rotation centre angle transformation geometry'),
            (2,  'Rotation 90 and 180 degrees',     'rotation 90 180 degrees coordinate geometry'),
            (3,  'Properties of Rotation',          'rotation properties invariant point centre'),
            (4,  'Rotation and Symmetry',           'rotational symmetry order centre shapes'),
            (5,  'Combined Transformations',        'rotation reflection combined transformation'),
            (6,  'Review and Assessment',           'rotation transformation review assessment'),
        ],
    },
    {
        'file':      'math_2_4_trigonometry_1.js',
        'substrand': 'Trigonometry 1',
        'subject':   'Mathematics',
        'loop_var':  'f',
        'col_var':   'CW',
        'lessons': [
            (1,  'Introduction to Trigonometry',    'trigonometry right triangle angle ratio'),
            (2,  'Sine Cosine Tangent',             'sine cosine tangent SOH CAH TOA ratios'),
            (3,  'Finding Unknown Sides',           'trigonometry unknown sides right triangle'),
            (4,  'Finding Unknown Angles',          'trigonometry unknown angles inverse sine cosine'),
            (5,  'Angles of Elevation Depression',  'angles elevation depression trigonometry'),
            (6,  'Trigonometry Applications',       'trigonometry applications real life Kenya'),
            (7,  'Review and Assessment',           'trigonometry review assessment summary'),
        ],
    },
]

# ── Patch functions ───────────────────────────────────────────────────────────

def patch_generator(config):
    path = os.path.join(GENERATORS_DIR, config['file'])
    with open(path, 'r') as f:
        src = f.read()

    original = src
    results = []
    lv  = config['loop_var']   # ph or f
    cv  = config['col_var']    # cw or CW

    # ── 1. Add require('./aresResources') ────────────────────────────────────
    if 'aresResources' not in src:
        old = "const path = require('path');"
        new = "const path = require('path');\nconst { getAllPhaseResources, buildResourceParagraphs } = require('./aresResources');"
        if old in src:
            src = src.replace(old, new)
            results.append("✓ require added")
        else:
            results.append("✗ require — path require not found")
    else:
        results.append("↩ require already present")

    # ── 2. Add TableLayoutType to imports ────────────────────────────────────
    if 'TableLayoutType' not in src:
        src = src.replace(
            "PageOrientation, HeadingLevel,",
            "PageOrientation, HeadingLevel, TableLayoutType,"
        )
        if 'TableLayoutType' in src:
            results.append("✓ TableLayoutType imported")
        else:
            results.append("✗ TableLayoutType import — HeadingLevel line not found")
    else:
        results.append("↩ TableLayoutType already imported")

    # ── 3. Add TableLayoutType.FIXED to makeTable ────────────────────────────
    if 'TableLayoutType.FIXED' not in src:
        old = "    width: { size: tableW, type: WidthType.DXA },\n    columnWidths,"
        new = "    width: { size: tableW, type: WidthType.DXA },\n    layout: TableLayoutType.FIXED,\n    columnWidths,"
        if old in src:
            src = src.replace(old, new)
            results.append("✓ TableLayoutType.FIXED added")
        else:
            results.append("✗ TableLayoutType.FIXED — makeTable pattern not found")
    else:
        results.append("↩ TableLayoutType.FIXED already present")

    # ── 4. Add aresRes lookup inside sectionC ────────────────────────────────
    if 'getAllPhaseResources' not in src:
        old = "function sectionC(lesson) {"
        new = (
            "function sectionC(lesson) {\n"
            "  const aresTopic = lesson.aresKeywords || lesson.title || '';\n"
            f"  const aresRes = getAllPhaseResources({{\n"
            f"    substrand: lesson.substrand || '{config['substrand']}',\n"
            f"    topic:     aresTopic,\n"
            f"    subject:   '{config['subject']}',\n"
            f"  }});\n"
        )
        if old in src:
            src = src.replace(old, new, 1)
            results.append("✓ aresRes lookup added")
        else:
            results.append("✗ aresRes — sectionC not found")
    else:
        results.append("↩ aresRes already present")

    # ── 5. Add PHASE_KEY map and replace resource cell ───────────────────────
    if 'PHASE_KEY' not in src:
        # Bio 1.1 uses inline ...map() syntax; Bio 2.1 and Math use same
        old_ph = (
            f"      cell({lv}.resource,            "
            f"{{ fill: C.grey,  w: {cv}[2], size: SZ }}),\n"
        )
        new_ph = (
            f"      cell(buildResourceParagraphs(aresRes[PHASE_KEY[{lv}.phase] || 'observe'], {lv}.phase),  "
            f"{{ fill: C.grey,  w: {cv}[2] }}),\n"
        )

        if old_ph in src:
            # Insert PHASE_KEY before the map call
            phase_key_block = (
                "\n  const PHASE_KEY = {\n"
                "    'Predict Phase':                         'predict',\n"
                "    'Observe Phase':                         'observe',\n"
                "    'Explain Phase':                         'explain',\n"
                "    'Driving Question Board (DQB) Creation': 'dqb',\n"
                "    'Model Building Phase':                  'model',\n"
                "  };\n"
            )
            # Find the map call and insert PHASE_KEY before it
            map_marker = f"    ...lesson.framework.map({lv} => new TableRow({{ children: ["
            if map_marker in src:
                src = src.replace(map_marker, phase_key_block + "  " + map_marker.strip())
                src = src.replace(old_ph, new_ph)
                results.append("✓ PHASE_KEY + resource cell replaced")
            else:
                results.append(f"✗ PHASE_KEY — map marker not found for loop_var={lv}")
        else:
            # Try alternate spacing
            alt = f"      cell({lv}.resource,          {{ fill: C.grey,  w: {cv}[2], size: SZ }}),\n"
            alt2 = f"      cell({lv}.resource,         {{ fill: C.grey,  w: {cv}[2], size: SZ }}),\n"
            found = False
            for candidate in [alt, alt2]:
                if candidate in src:
                    src = src.replace(
                        f"    ...lesson.framework.map({lv} => new TableRow({{ children: [",
                        phase_key_block + f"    ...lesson.framework.map({lv} => new TableRow({{ children: ["
                    )
                    src = src.replace(candidate, new_ph)
                    results.append("✓ PHASE_KEY + resource cell replaced (alt spacing)")
                    found = True
                    break
            if not found:
                results.append(f"✗ resource cell — ph.resource line not found (tried 3 spacings)")
    else:
        results.append("↩ PHASE_KEY already present")

    # ── 6. Add aresKeywords to lesson objects ─────────────────────────────────
    added_kw = 0
    for num, title, keywords in config['lessons']:
        # Match num: N, or num: N\n
        pattern = f"num: {num},"
        kw_line = f"aresKeywords: '{keywords}',"
        if pattern in src and kw_line not in src:
            src = src.replace(pattern, f"{pattern}\n      {kw_line}", 1)
            added_kw += 1
    if added_kw > 0:
        results.append(f"✓ aresKeywords added to {added_kw} lessons")
    elif all(f"aresKeywords: '{kw}'" in src for _, _, kw in config['lessons'][:1]):
        results.append("↩ aresKeywords already present")
    else:
        results.append(f"↩ aresKeywords: {added_kw} added (some may use title fallback)")

    # ── Save if changed ───────────────────────────────────────────────────────
    if src != original:
        backup = path.replace('.js', '_pre_ares.js')
        with open(backup, 'w') as f:
            f.write(original)
        with open(path, 'w') as f:
            f.write(src)
        results.append(f"💾 Saved (backup: {os.path.basename(backup)})")
    else:
        results.append("⚠ No changes written")

    return results


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("ARES Generator Batch Patcher")
    print("=" * 50)
    for config in GENERATORS:
        print(f"\n{config['file']}")
        results = patch_generator(config)
        for r in results:
            print(f"  {r}")
    print("\nDone.")
