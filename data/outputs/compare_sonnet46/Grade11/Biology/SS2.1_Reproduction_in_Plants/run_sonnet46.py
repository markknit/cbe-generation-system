"""Evaluation-only wrapper: run generate_substrand.py on claude-sonnet-4-6 the way
this project ran it before 2026-09-30 (no thinking), writing outside data/outputs/v2.
Not part of the repo: Mark's rule is Sonnet 5.5 minimum for real output.
Usage: same args as generate_substrand.py."""
import sys
sys.path.insert(0, '/home/markk/ares/cbe-generation-system/src')
import generate_substrand as g

g.MODEL = 'claude-sonnet-4-6'
g.PRICE_PER_MTOK = {'sync': {'input': 3.0, 'output': 15.0},
                    'batch': {'input': 1.5, 'output': 7.5}}

def _structured_params_46(schema):
    # Pre-2026-09-30 behaviour on 4.6: no thinking, default effort. Structured
    # outputs replace the old forced tool_choice (same schema either way).
    return {"output_config": {"format": {"type": "json_schema", "schema": schema}}}
g._structured_params = _structured_params_46

_orig_dir = g._v2_output_dir
def _compare_dir(*a, **k):
    return 'compare_sonnet46/' + _orig_dir(*a, **k)[len('v2/'):]
g._v2_output_dir = _compare_dir

sys.argv = ['generate_substrand.py'] + sys.argv[1:]
g.main()
