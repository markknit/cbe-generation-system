#!/usr/bin/env python3
"""Convert only pilot documents using an isolated LibreOffice profile."""
import json,subprocess,tempfile,sys
from pathlib import Path
B=Path(__file__).resolve().parents[2]/'data/codex_pilot_2026-11'
files=sorted((B/'outputs/v2').glob('*/*/*.docx'))
if sys.argv[1:]:
 prefixes=[json.loads((B/'manuscripts'/f'{name}.json').read_text())['prefix'] for name in sys.argv[1:]]
 files=[p for p in files if any(p.name.startswith(prefix+'_') for prefix in prefixes)]
if not files:raise SystemExit('No pilot DOCX files selected')
out=B/'outputs/PDF';out.mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(prefix='codex-pilot-lo-') as profile:
 cmd=['soffice','-env:UserInstallation='+Path(profile).as_uri(),'--headless','--convert-to','pdf','--outdir',str(out),*[str(p) for p in files]]
 r=subprocess.run(cmd,text=True,capture_output=True,timeout=240)
 print(r.stdout);print(r.stderr)
 if r.returncode:raise SystemExit(r.returncode)
 missing=[p.name for p in files if not (out/(p.stem+'.pdf')).exists()]
 if missing:raise SystemExit('Missing PDFs: '+str(missing))
 print('Verified',len(files),'PDFs')
