#!/usr/bin/env python3
"""fix_v2_data.py — v2 generation remediation (corrected version)."""
import os, re, sys, shutil

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) if __file__.endswith('.py') else os.getcwd()
DATA_DIR = os.path.join(REPO, 'generators', 'data')

CANONICAL = {
    'predict':  'Predict Phase',
    'observe':  'Observe Phase',
    'explain':  'Explain Phase',
    'model':    'Model Building Phase',
    'dqb':      'Driving Question Board (DQB) Creation',
}

PHASE_RE = re.compile(r'"phase":\s*"([^"]+)"')
SAFETY_RE = re.compile(r'(\s+)safety(\d+)otes(\s*:)')

def normalize_phase(raw):
    s = raw.strip()
    # Strip "Phase N — " / "N. " / "N: " / "N — " prefix
    s = re.sub(r'^\s*(?:Phase\s+)?\d+\s*[—–\-:.\s]+\s*', '', s, flags=re.IGNORECASE)
    # Strip trailing "(...)" and ":subtitle"
    s = re.sub(r'\s*\([^)]*\)\s*$', '', s)
    s = re.sub(r'\s*:\s*.+$', '', s)
    low = s.lower().strip()
    # DQB first (most specific tokens)
    if 'dqb' in low or 'driving question board' in low:        return CANONICAL['dqb']
    if 'predict' in low:                                       return CANONICAL['predict']
    if 'observe' in low or 'evidence' in low:                  return CANONICAL['observe']
    # Phase 5 catch-all: model / final / reflection / synthesis
    if 'model' in low or 'final' in low or 'reflection' in low or 'synthesis' in low:
        return CANONICAL['model']
    if 'explain' in low or 'sensemaking' in low:               return CANONICAL['explain']
    return None

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        src = f.read()
    original = src
    actions = []
    unmapped = []

    # 1. Phase normalization — always write what we can; collect unmapped as warnings
    def phase_sub(m):
        raw = m.group(1)
        canon = normalize_phase(raw)
        if canon is None:
            unmapped.append(raw)
            return m.group(0)
        return f'"phase": "{canon}"'
    new_src = PHASE_RE.sub(phase_sub, src)
    changed = sum(1 for m in PHASE_RE.finditer(src)
                  if normalize_phase(m.group(1)) is not None
                  and f'"phase": "{normalize_phase(m.group(1))}"' != m.group(0))
    if changed:
        src = new_src
        actions.append(f"{changed} phases normalized")

    # 2. safetyNotes key
    src, n_safety = SAFETY_RE.subn(r'\1safetyNotes\3', src)
    if n_safety:
        actions.append(f"{n_safety} safetyNotes keys fixed")

    # 3. bio_1_2 internal "Sub-Strand 1.4" leftover
    if os.path.basename(path) == 'bio_1_2_data.js':
        before = src.count('Sub-Strand 1.4: Chemicals of Life')
        src = src.replace('Sub-Strand 1.4: Chemicals of Life', 'Sub-Strand 1.2: Chemicals of Life')
        after = src.count('Sub-Strand 1.4: Chemicals of Life')
        if before > after:
            actions.append(f"Sub-Strand 1.4 → 1.2 ({before-after})")

    if src != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(src)
        msg = ', '.join(actions) if actions else '(no-op write)'
        if unmapped:
            uniq = sorted(set(unmapped))
            msg += f"  [WARN: {len(uniq)} unmapped]"
        print(f"  ✓ {os.path.basename(path)}: {msg}")
    else:
        print(f"  · {os.path.basename(path)}: nothing to do")

    return unmapped

def main():
    print("--- fixing data files ---")
    files = sorted(f for f in os.listdir(DATA_DIR) if f.endswith('_data.js'))
    all_unmapped = {}
    for fn in files:
        u = fix_file(os.path.join(DATA_DIR, fn))
        if u: all_unmapped[fn] = sorted(set(u))

    if all_unmapped:
        print(f"\n--- UNMAPPED phases remaining: ---")
        for fn, vs in all_unmapped.items():
            print(f"  {fn}:")
            for v in vs: print(f"      {v!r}")
        print("\nAdd these to normalize_phase() and re-run.")
        sys.exit(1)
    else:
        print(f"\n--- all {len(files)} files clean ---")

if __name__ == '__main__':
    main()
