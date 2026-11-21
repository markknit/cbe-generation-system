"""Pilot-only curation over the existing local ARES matcher; no model calls."""
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
POLICY=json.loads((ROOT/'data/codex_pilot_2026-11/resource_policy.json').read_text())
args=sys.argv[1:]
if '--text' in args:
 raise SystemExit('Pilot curation supports structured resources only')
def argument(name):
 return args[args.index(name)+1] if name in args else ''
raw=subprocess.check_output([sys.executable,str(ROOT/'src/ares_recommender.py'),*args],text=True)
data=json.loads(raw)
independent=argument('--title').lower().startswith(POLICY['independent_title_prefix'])
diag=data.setdefault('_diagnostics',{})
phases={k:v for k,v in data.items() if k!='_diagnostics'} if '--all-phases' in args else {argument('--phase') or 'observe':data}
for phase,resources in phases.items():
 for kind in ('video','reading'):
  resource=resources.get(kind)
  excluded=resource and any(term in resource['title'].lower() for term in POLICY['excluded_title_phrases'])
  if independent or excluded:
   resources[kind]=None
   slot=diag.setdefault('slots',{}).setdefault(f'{phase}.{kind}',{})
   slot.update(picked=None,fit=None,pilot_curation_reason='independent assessment' if independent else 'out-of-scope title')
print(json.dumps(data))
