"""Record final artifact provenance and inexpensive checks; no model calls."""
import hashlib,json,re,subprocess,zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
B=Path(__file__).resolve().parents[2]/'data/codex_pilot_2026-11'
suffixes=['CBE_LessonSequence','CompactTeacherGuide','StudentMaterials','MaterialsTeacherKey','FinalExplanation','FinalExplanation_TeacherKey','SummaryTable','StudentSummaryTable','AssessmentMaterials']
expected=[]
for p in sorted((B/'manuscripts').glob('*.json')):
 m=json.loads(p.read_text())
 expected.extend(m['prefix']+'_'+s for s in suffixes)
for ext,folder in [('docx',B/'outputs/v2'),('pdf',B/'outputs/PDF')]:
 actual=[p.stem for p in folder.rglob('*.'+ext)]
 assert sorted(actual)==sorted(expected),(ext,'missing/extra document or duplicate basename')
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
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
for p in (B/'outputs/v2').rglob('*.docx'):
 z=zipfile.ZipFile(p)
 xml=' '.join(z.read(n).decode() for n in z.namelist() if n.startswith('word/') and n.endswith('.xml'))
 assert 'Claude' not in xml and 'Anthropic' not in xml,p
 assert 'ChatGPT/Codex' in xml and 'OpenAI' in xml,p
 if p.stem.endswith('StudentSummaryTable'):
  body=ET.fromstring(z.read('word/document.xml'))
  for row in body.findall('.//w:tbl/w:tr',ns)[1:]:
   assert all(not ''.join(c.itertext()).strip() for c in row.findall('w:tc',ns)[1:]),p
for p in (B/'outputs/v2').rglob('*_data.json'):
 d=json.loads(p.read_text());final=d['LESSONS'][-1]
 assert all(v[k] is None for v in final['resourceLinks'].values() for k in ('video','reading')),p
 assert not any(s in ' '.join(x['sensemakingStrategy'] for x in final['framework']) for s in ('then paired comparison','Evidence-first group work','Revise a shared model')),p
 assert 'carboxylic acid naming' not in p.read_text().lower(),p
hashes={str(p.relative_to(B)):hashlib.sha256(p.read_bytes()).hexdigest() for folder in ['sources','blueprints','materials','manuscripts','modules','outputs'] for p in sorted((B/folder).rglob('*')) if p.is_file()}
(B/'evidence/artifact_sha256.json').write_text(json.dumps(hashes,indent=2))
print(len(rows),'PDFs; full inventory, attribution, blank student rows, assessment resources and placeholder checks pass; artifact hashes recorded')
for r in rows:
 if 'CompactTeacherGuide' in r['file']:print(r['file'],r['pages'],'pages')
