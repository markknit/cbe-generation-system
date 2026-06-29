#!/usr/bin/env python3
"""
run_full_generation.py  —  CBE Grade 10 full generation orchestrator
=====================================================================
Phases: smoke (4) → biology (8) → chemistry (6) → physics (11) → maths (13)
Each phase: submit all sub-strands → poll batch statuses → collect → verify

Usage:
    python3 scripts/run_full_generation.py           # Start fresh (fails if state exists)
    python3 scripts/run_full_generation.py --resume  # Resume from saved state
    python3 scripts/run_full_generation.py --status  # Print state summary and exit

Crash recovery:
    State is written atomically to dashboards/run_state.json after every change.
    On crash/restart: --resume re-checks in-progress batches and continues from
    the last known position. Any substrand in 'collecting' state is re-collected.
    Any substrand in 'submitting' state is re-checked for a batch_id file, or
    re-queued if none was written.
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────

PROJECT_ROOT   = Path(__file__).parent.parent
DASHBOARDS_DIR = PROJECT_ROOT / 'dashboards'
STATE_FILE     = DASHBOARDS_DIR / 'run_state.json'
LOG_FILE       = DASHBOARDS_DIR / 'run.log'
GENERATOR_PY   = PROJECT_ROOT / 'src' / 'generate_substrand.py'
DATA_DIR       = PROJECT_ROOT / 'generators' / 'data'

# ── Sub-strand inventory ───────────────────────────────────────────────────────

SMOKE_TEST = [
    ('biology',     '2.2'),
    ('chemistry',   '2.1'),
    ('physics',     '1.4'),
    ('mathematics', '1.4'),
]

INVENTORY = {
    'biology':     ['1.1', '1.2', '1.3', '2.1', '2.2', '2.3', '3.1', '3.2', '3.3'],
    'chemistry':   ['1.1', '1.2', '1.3', '1.4', '1.5', '2.1', '3.1'],
    'physics':     ['1.1', '1.2', '1.3', '1.4', '1.5', '2.1',
                    '3.1', '3.2', '3.3', '3.4', '4.1', '4.2'],
    'mathematics': ['1.1', '1.2', '1.3', '1.4', '2.1', '2.2', '2.3', '2.4',
                    '3.1', '3.2', '3.3', '3.4', '4.1', '4.2'],
}

SMOKE_KEYS = {f"{s}/{ss}" for s, ss in SMOKE_TEST}

PRODUCTION = {
    subj: [ss for ss in subs if f"{subj}/{ss}" not in SMOKE_KEYS]
    for subj, subs in INVENTORY.items()
}

# Phase name → ordered list of (subject, substrand) pairs
PHASES = {
    'smoke':     list(SMOKE_TEST),
    'biology':   [('biology',     ss) for ss in PRODUCTION['biology']],
    'chemistry': [('chemistry',   ss) for ss in PRODUCTION['chemistry']],
    'physics':   [('physics',     ss) for ss in PRODUCTION['physics']],
    'maths':     [('mathematics', ss) for ss in PRODUCTION['mathematics']],
}
PHASE_ORDER = ['smoke', 'biology', 'chemistry', 'physics', 'maths']

SUBJ_ABBR = {
    'biology': 'bio', 'chemistry': 'chem',
    'physics': 'phys', 'mathematics': 'math',
}


def _oname(subject, substrand):
    return f"{SUBJ_ABBR[subject]}_{substrand.replace('.', '_')}"


def _key(subject, substrand):
    return f"{subject}/{substrand}"


# ── Logging ───────────────────────────────────────────────────────────────────

def _log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(line + '\n')
    except OSError:
        pass


# ── State management ──────────────────────────────────────────────────────────

def _now():
    return datetime.now(timezone.utc).isoformat()


def save_state(state):
    tmp = STATE_FILE.with_suffix('.json.tmp')
    with open(tmp, 'w') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    tmp.rename(STATE_FILE)


def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return None


def init_state():
    substrands = {}
    batches = {}

    for phase, pairs in PHASES.items():
        phase_keys = []
        for subject, ss in pairs:
            k = _key(subject, ss)
            phase_keys.append(k)
            substrands[k] = {
                'subject': subject,
                'substrand': ss,
                'output_name': _oname(subject, ss),
                'phase': phase,
                'status': 'queued',        # queued→submitting→submitted→batch_done→collecting→complete/failed
                'batch_id': None,
                'lesson_count': None,
                'lesson_count_source': None,
                'submitted_at': None,
                'completed_at': None,
                'files': [],
                'stubs': [],
                'cost_estimate_usd': None,
                'log': '',
            }
        batches[phase] = {
            'status': 'pending',           # pending→submitting→polling→collecting→complete/partial
            'substrands': phase_keys,
            'submitted_at': None,
            'completed_at': None,
        }

    return {
        'started_at': _now(),
        'phase': 'smoke',
        'batches': batches,
        'substrands': substrands,
        'totals': {'cost_estimate_usd': 0.0, 'lessons_generated': 0},
    }


def _reset_interrupted(state):
    """On resume: put partially-completed sub-strands back into a safe state."""
    for key, ss in state['substrands'].items():
        if ss['status'] == 'submitting':
            id_path = DATA_DIR / f".{ss['output_name']}_batch_id.txt"
            if id_path.exists():
                batch_id = id_path.read_text().strip()
                ss['batch_id'] = batch_id
                ss['status'] = 'submitted'
                _log(f"  Recovered {key}: batch_id={batch_id}")
            else:
                ss['status'] = 'queued'
                _log(f"  Reset {key}: no batch_id written, re-queuing")
        elif ss['status'] == 'collecting':
            ss['status'] = 'batch_done'
            _log(f"  Reset {key}: interrupted during collect, will re-collect")
    # Also reset any batch in 'submitting'/'polling'/'collecting' so the phase reruns cleanly
    for phase, batch in state['batches'].items():
        if batch['status'] in ('submitting', 'polling', 'collecting'):
            batch['status'] = 'pending'


# ── Per-sub-strand operations ─────────────────────────────────────────────────

def submit_one(key, state):
    """Submit one sub-strand batch via generate_substrand.py --batch."""
    ss = state['substrands'][key]
    subject, substrand = ss['subject'], ss['substrand']
    oname = ss['output_name']

    ss['status'] = 'submitting'
    save_state(state)

    result = subprocess.run(
        [sys.executable, str(GENERATOR_PY),
         '--subject', subject, '--substrand', substrand,
         '--output', oname, '--batch'],
        cwd=PROJECT_ROOT, capture_output=True, text=True,
        env=os.environ.copy(),
    )

    if result.returncode != 0:
        _log(f"  ERROR submit {key}: {result.stderr[:300]}")
        ss['status'] = 'failed'
        ss['log'] = result.stderr[:500]
        save_state(state)
        return False

    id_path = DATA_DIR / f'.{oname}_batch_id.txt'
    if not id_path.exists():
        _log(f"  ERROR: no batch_id file for {key}")
        ss['status'] = 'failed'
        save_state(state)
        return False

    batch_id = id_path.read_text().strip()

    # Read lesson count and source from batch checkpoint metadata
    meta_path = id_path.with_suffix('.json')
    lesson_count, lc_source = 8, 'default'
    if meta_path.exists():
        try:
            m = json.loads(meta_path.read_text())
            lesson_count = m.get('lessons', 8) or 8
            lc_source = m.get('lesson_count_source', 'unknown')
        except Exception:
            pass

    ss['status'] = 'submitted'
    ss['batch_id'] = batch_id
    ss['lesson_count'] = lesson_count
    ss['lesson_count_source'] = lc_source
    ss['submitted_at'] = _now()
    ss['cost_estimate_usd'] = round(0.35 * lesson_count / 8, 2)
    save_state(state)

    _log(f"  Submitted {key}: batch={batch_id}  lessons={lesson_count} ({lc_source})")
    return True


def poll_phase(phase_keys, state):
    """Poll Anthropic API until all 'submitted' sub-strands reach 'batch_done'."""
    try:
        from dotenv import load_dotenv
        load_dotenv(PROJECT_ROOT / '.env')
    except ImportError:
        pass

    import anthropic
    client = anthropic.Anthropic()

    while True:
        pending = [k for k in phase_keys
                   if state['substrands'][k]['status'] == 'submitted']
        if not pending:
            break

        newly_done = []
        for key in pending:
            batch_id = state['substrands'][key].get('batch_id')
            if not batch_id:
                state['substrands'][key]['status'] = 'failed'
                continue
            try:
                batch = client.beta.messages.batches.retrieve(batch_id)
                if batch.processing_status == 'ended':
                    state['substrands'][key]['status'] = 'batch_done'
                    newly_done.append(key)
            except Exception as e:
                _log(f"  WARNING: poll {key}: {e}")

        save_state(state)

        n_done  = sum(1 for k in phase_keys
                      if state['substrands'][k]['status'] in
                         ('batch_done', 'collecting', 'complete', 'failed'))
        n_total = len(phase_keys)
        still   = len(pending) - len(newly_done)

        if newly_done:
            for k in newly_done:
                _log(f"  Batch ready: {k}")

        _log(f"  Poll: {n_done}/{n_total} ready"
             + (f"  ({still} still processing)" if still > 0 else ""))

        if any(state['substrands'][k]['status'] == 'submitted' for k in phase_keys):
            time.sleep(60)


def collect_one(key, state):
    """Collect batch results and run the docx generator for one sub-strand."""
    ss = state['substrands'][key]
    oname = ss['output_name']

    ss['status'] = 'collecting'
    save_state(state)

    result = subprocess.run(
        [sys.executable, str(GENERATOR_PY), '--collect', oname, '--run'],
        cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=600,
        env=os.environ.copy(),
    )

    if result.returncode != 0:
        _log(f"  ERROR collect {key}: {result.stderr[:300]}")
        ss['status'] = 'failed'
        ss['log'] = (result.stdout + result.stderr)[:500]
        save_state(state)
        return False

    # Stub check
    data_file = DATA_DIR / f'{oname}_data.js'
    stubs = []
    if data_file.exists():
        data_path_js = json.dumps(str(data_file))
        stub_result = subprocess.run(
            ['node', '-e',
             f'var d=require({data_path_js});'
             'var s=d.LESSONS.filter(function(l){return !l.overview||l.overview.length<50;});'
             'if(s.length){process.stdout.write("STUBS:"+s.map(function(l){return l.number;}).join(",")+"\\n");}'],
            cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=30,
        )
        out = stub_result.stdout.strip()
        if out.startswith('STUBS:'):
            stubs = out[6:].split(',')
            _log(f"  WARNING: stub lessons in {key}: {', '.join(stubs)}")

    # Collect generated docx files (v2 output path mirrors v2_owner_inventory)
    subj_folder = 'Maths' if ss['subject'] == 'mathematics' else ss['subject'].capitalize()
    data_file_path = DATA_DIR / f'{oname}_data.js'
    out_dir = None
    if data_file_path.exists():
        meta_out = subprocess.run(
            ['node', '-e', f'var d=require({json.dumps(str(data_file_path))});console.log(d.META.outputDir);'],
            cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=15,
        )
        if meta_out.returncode == 0 and meta_out.stdout.strip():
            out_dir = PROJECT_ROOT / 'data' / 'outputs' / meta_out.stdout.strip()
    files = [f.name for f in sorted(out_dir.glob('*.docx'))] if (out_dir and out_dir.exists()) else []

    lc = ss.get('lesson_count') or 8
    ss['status'] = 'complete'
    ss['completed_at'] = _now()
    ss['files'] = files
    ss['stubs'] = stubs
    ss['log'] = result.stdout[-400:] if result.stdout else ''

    state['totals']['lessons_generated'] += lc
    state['totals']['cost_estimate_usd'] = round(
        state['totals']['cost_estimate_usd'] + (ss.get('cost_estimate_usd') or 0.0), 2)
    save_state(state)

    _log(f"  Complete: {key}  ({lc} lessons, {len(files)} files"
         + (f", {len(stubs)} STUBS" if stubs else "") + ")")
    return True


# ── Phase runner ──────────────────────────────────────────────────────────────

def run_phase(phase, state):
    batch = state['batches'][phase]
    keys  = batch['substrands']

    _log(f"\n{'='*60}")
    _log(f"Phase: {phase.upper()}  ({len(keys)} sub-strands)")
    _log('='*60)

    batch['status'] = 'submitting'
    batch['submitted_at'] = _now()
    save_state(state)

    # 1. Submit all queued sub-strands
    n_submitted = 0
    for key in keys:
        if state['substrands'][key]['status'] == 'queued':
            ok = submit_one(key, state)
            if ok:
                n_submitted += 1
            time.sleep(3)   # brief gap between API submissions

    _log(f"  Submitted {n_submitted} new batch(es)")

    # 2. Poll until all submitted batches complete
    if any(state['substrands'][k]['status'] == 'submitted' for k in keys):
        _log("  Polling batch statuses (checking every 60s)...")
        batch['status'] = 'polling'
        save_state(state)
        poll_phase(keys, state)

    # 3. Collect each batch-done sub-strand
    batch['status'] = 'collecting'
    save_state(state)

    for key in keys:
        if state['substrands'][key]['status'] == 'batch_done':
            collect_one(key, state)

    # 4. Tally
    n_complete = sum(1 for k in keys if state['substrands'][k]['status'] == 'complete')
    n_failed   = sum(1 for k in keys if state['substrands'][k]['status'] == 'failed')
    n_stubs    = sum(len(state['substrands'][k].get('stubs', [])) for k in keys)

    batch['status'] = 'complete' if n_failed == 0 else 'partial'
    batch['completed_at'] = _now()
    save_state(state)

    _log(f"Phase {phase}: {n_complete}/{len(keys)} complete, "
         f"{n_failed} failed, {n_stubs} stub lesson(s)")


# ── Status printer ────────────────────────────────────────────────────────────

def print_status(state):
    phase_labels = {
        'smoke': 'Smoke test', 'biology': 'Biology',
        'chemistry': 'Chemistry', 'physics': 'Physics', 'maths': 'Maths',
    }
    print(f"\nCurrent phase: {state['phase']}")
    print(f"Started:       {state['started_at'][:19].replace('T', ' ')} UTC\n")
    for phase in PHASE_ORDER:
        batch = state['batches'][phase]
        keys  = batch['substrands']
        counts = {
            'queued':    sum(1 for k in keys if state['substrands'][k]['status'] == 'queued'),
            'submitted': sum(1 for k in keys if state['substrands'][k]['status'] in ('submitted', 'batch_done', 'collecting')),
            'complete':  sum(1 for k in keys if state['substrands'][k]['status'] == 'complete'),
            'failed':    sum(1 for k in keys if state['substrands'][k]['status'] == 'failed'),
        }
        label = phase_labels.get(phase, phase)
        bar = f"{counts['complete']}/{len(keys)}"
        status = batch['status']
        extras = []
        if counts['submitted']: extras.append(f"{counts['submitted']} in-progress")
        if counts['failed']:    extras.append(f"{counts['failed']} FAILED")
        print(f"  {label:12s} {bar:7s}  [{status}]"
              + (f"  {', '.join(extras)}" if extras else ""))
    t = state['totals']
    print(f"\n  Lessons generated: {t['lessons_generated']}")
    print(f"  Estimated cost:    ~${t['cost_estimate_usd']:.2f}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='CBE Grade 10 full generation orchestrator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Dashboard: python3 -m http.server 8080 --directory dashboards/\n"
            "           then open http://jhm-spark:8080/progress.html"
        ),
    )
    parser.add_argument('--resume', action='store_true',
                        help='Resume from saved state (required if state file exists)')
    parser.add_argument('--status', action='store_true',
                        help='Print current state summary and exit')
    args = parser.parse_args()

    DASHBOARDS_DIR.mkdir(exist_ok=True)

    # Load environment
    env_file = PROJECT_ROOT / '.env'
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, _, v = line.partition('=')
                os.environ.setdefault(k.strip(), v.strip())

    existing = load_state()

    if args.status:
        if existing:
            print_status(existing)
        else:
            print("No run state found. Start with: python3 scripts/run_full_generation.py")
        return

    if existing and not args.resume:
        print(f"Run state exists (phase: {existing['phase']}).")
        print(f"  --resume   to continue from where it left off")
        print(f"  --status   to see current progress")
        print(f"  Delete {STATE_FILE} to start a completely fresh run")
        sys.exit(1)

    if existing:
        state = existing
        _log(f"Resuming run (saved phase: {state['phase']})")
        _reset_interrupted(state)
        save_state(state)
    else:
        state = init_state()
        save_state(state)
        _log("Starting fresh Grade 10 CBE generation run")
        _log(f"  42 sub-strands  ·  Biology / Chemistry / Physics / Mathematics")
        _log(f"  Dashboard: python3 -m http.server 8080 --directory dashboards/")

    for phase in PHASE_ORDER:
        batch = state['batches'][phase]

        if batch['status'] == 'complete':
            _log(f"Phase {phase}: already complete, skipping")
            continue

        # Production batches only run after smoke test is approved
        if phase != 'smoke' and state['batches']['smoke']['status'] != 'complete':
            _log("Smoke test not yet complete — stopping before production batches")
            _log("Review outputs, then: python3 scripts/run_full_generation.py --resume")
            break

        state['phase'] = phase
        save_state(state)

        run_phase(phase, state)

        if phase == 'smoke':
            lg = state['totals']['lessons_generated']
            ct = state['totals']['cost_estimate_usd']
            n_ok  = sum(1 for k in batch['substrands']
                        if state['substrands'][k]['status'] == 'complete')
            n_bad = len(batch['substrands']) - n_ok
            _log("\n" + "="*60)
            _log("SMOKE TEST COMPLETE — MANUAL REVIEW REQUIRED")
            _log("="*60)
            _log(f"  {n_ok}/4 sub-strands complete" + (f"  ({n_bad} FAILED)" if n_bad else ""))
            _log(f"  Lessons generated: {lg}    Cost so far: ~${ct:.2f}")
            _log(f"  Output docs:  data/outputs/docx/")
            _log(f"  Dashboard:    http://jhm-spark:8080/progress.html")
            _log(f"  Stub report:  check dashboards/run_state.json for 'stubs' fields")
            _log("")
            _log("Review the generated documents, then run:")
            _log("  python3 scripts/run_full_generation.py --resume")
            _log("="*60)
            state['phase'] = 'smoke_complete'
            save_state(state)
            break   # Always pause here for manual review

    else:
        # Loop completed without break = all phases done
        state['phase'] = 'done'
        save_state(state)
        lg = state['totals']['lessons_generated']
        ct = state['totals']['cost_estimate_usd']
        _log("\n" + "="*60)
        _log("ALL GENERATION COMPLETE")
        _log(f"  Total lessons generated: {lg}")
        _log(f"  Estimated total cost:    ~${ct:.2f}")
        _log(f"  Output docs:  data/outputs/docx/")
        _log("="*60)


if __name__ == '__main__':
    main()
