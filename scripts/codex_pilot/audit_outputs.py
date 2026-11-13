"""Record final artifact provenance and inexpensive checks; no model calls."""
import hashlib,json,re,subprocess,zipfile
from pathlib import Path
B=Path(__file__).resolve().parents[2]/'data/codex_pilot_2026-11'
rows=[]
for p in sorted((B/'outputs/PDF').glob('*.pdf')):
 info=subprocess.check_output(['pdfinfo',str(p)],text=True)
 text=subprocess.check_output(['pdftotext','-layout',str(p),'-'],text=True)
 (B/'evidence'/(p.stem+'.txt')).write_text(text)
 rows.append(dict(file=p.name,pages=int(re.search(r'Pages:\s+(\d+)',info)[1]),characters=len(text),suspect_tokens=[s for s in ['{{','undefined','NaN','FILL','\ufffd'] if s in text]))
(B/'evidence/pdf_inventory.json').write_text(json.dumps(rows,indent=2))
assert not any(r['suspect_tokens'] for r in rows)
for p in (B/'outputs/v2').glob('*/*/*_FinalExplanation.docx'):
 xml=zipfile.ZipFile(p).read('word/document.xml').decode()
 assert 'Exemplar answer' not in xml and 'Teacher Key: Exemplar' not in xml,p
hashes={str(p.relative_to(B)):hashlib.sha256(p.read_bytes()).hexdigest() for folder in ['sources','blueprints','materials','manuscripts','modules','outputs'] for p in sorted((B/folder).rglob('*')) if p.is_file()}
(B/'evidence/artifact_sha256.json').write_text(json.dumps(hashes,indent=2))
print(len(rows),'PDFs; no scanned placeholder tokens; artifact hashes recorded')
for r in rows:
 if 'CompactTeacherGuide' in r['file']:print(r['file'],r['pages'],'pages')
