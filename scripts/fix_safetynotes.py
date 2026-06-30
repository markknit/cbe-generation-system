#!/usr/bin/env python3
"""Fix the quoted-key safetyNotes corruption that the prior script missed."""
import os, re, sys

REPO = os.getcwd()
DATA_DIR = os.path.join(REPO, 'generators', 'data')

# The corruption: "safety<N>otes" in quoted-key form
QUOTED_KEY_RE = re.compile(r'"safety(\d+)otes"(\s*:)')

total = 0
for fn in sorted(os.listdir(DATA_DIR)):
    if not fn.endswith('_data.js'): continue
    path = os.path.join(DATA_DIR, fn)
    with open(path) as f: src = f.read()
    new_src, n = QUOTED_KEY_RE.subn(r'"safetyNotes"\2', src)
    if n:
        with open(path, 'w') as f: f.write(new_src)
        print(f"  ✓ {fn}: {n} safetyNotes keys fixed")
        total += n
print(f"\nTotal: {total} corrupted keys fixed")
