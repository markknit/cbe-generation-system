"""Local checkpoint helper: only use after an explicit independent final PASS."""
import json,hashlib,sys,zipfile,datetime
from pathlib import Path
sys.path.insert(0,'scripts')
from curriculum_pipeline import content_fingerprint
b=Path('data/curriculum_expansion_2026-11')
n,reportname,expected,scope=sys.argv[1:5]
archive_name=sys.argv[5] if len(sys.argv)>5 else n+'_Reviewed.zip'
if Path(archive_name).name!=archive_name or Path(archive_name).suffix!='.zip':
 raise ValueError('archive name must be a simple .zip filename')
zp=b/archive_name
if zp.exists():
 raise FileExistsError('Frozen archive already exists; choose an explicit new version: '+str(zp))
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report_candidates=[Path(reportname),b/'reviews/batch_05'/reportname,b/'reviews/batch_06'/reportname]
report=next((p for p in report_candidates if p.is_file()),report_candidates[-1])
assert h(report)==expected
fp=content_fingerprint(b,n)
ca=json.loads((b/'reviews'/n/'content_acceptance.json').read_text());assert ca['content_fingerprint']==fp and ca['verdict']=='accepted'
review_evidence=[]
assert ca['evidence']
for item in ca['evidence']:
 resolved=Path(item['path']).resolve()
 assert resolved.is_relative_to(b.resolve()) and resolved.is_file()
 assert h(resolved)==item['sha256']
 review_evidence.append(b/resolved.relative_to(b.resolve()))
m=json.loads((b/'manuscripts'/f'{n}.json').read_text());prefix=m['prefix']
data=next((b/'outputs/v2').rglob(prefix+'_data.json'));out=data.parent
audit_candidates=sorted((b/'evidence').glob(f'artifact_audit_{n}_????-??-??.json'),reverse=True)+[b/'evidence'/f'batch_05_{n}_artifact_audit.json']
audit=next((p for p in audit_candidates if p.is_file()),audit_candidates[-1])
rows=json.loads(audit.read_text())['documents'];assert len(rows)==9 and {r['module'] for r in rows}=={n}
arts=[]
for r in rows:
 for typ,folder in [('docx',out),('pdf',b/'outputs/PDF')]:
  p=folder/(prefix+'_'+r['type']+'.'+typ);assert h(p)==r[typ+'_sha256'];arts.append(p)
arts.append(data)
ar=dict(verdict='accepted',kind='independent_scoped_artifact_review',content_fingerprint=fp,evidence=[dict(path=str(report),sha256=h(report))],artifacts=[dict(path=str(p.relative_to(b)),sha256=h(p)) for p in sorted(arts)],scope=scope)
p=b/'reviews'/n/'artifact_acceptance.json';p.write_text(json.dumps(ar,ensure_ascii=False,indent=2)+'\n')
files=set(arts+[p,b/'reviews'/n/'content_acceptance.json',report,b/'attribution.yaml',audit,b/'evidence'/f'{n}_resource_policy_snapshot.json'])
files.update(review_evidence)
for area in ('sources','blueprints','materials','manuscripts'):
 files.update((b/area).glob(n+'*'))
files={p for p in files if p.is_file()}
bank=json.loads((b/'materials'/f'{n}.json').read_text())
for card in bank['items']:
 for asset in card.get('assets',[]):files.add(b/'materials'/asset)
legacy=b/'materials/diagrams'
for card in bank['items']:
 p=legacy/(card['id']+'.png')
 if p.exists():files.add(p)
for parent in dict.fromkeys([b/'reviews/batch_05',b/'reviews/batch_05/evidence',b/'reviews/batch_06',b/'reviews/batch_06/evidence',report.parent,report.parent/'evidence',b/'evidence']+[parent for path in review_evidence for parent in (path.parent,path.parent/'evidence')]):
 for p in parent.glob(n+'*'):
  if p.is_dir():files.update(x for x in p.rglob('*') if x.is_file())
  else:files.add(p)
if n=='gensci_1_2':
 for p in [b/'reviews/batch_04/cell_asset_suitability_review.md',b/'materials/microscopy/source_manifest.json',b/'evidence/cell_caption_spacing_bridge.json',b/'evidence/cell_document_view_policy.md',b/'reviews/batch_05/cell_image_frame_code_review.md',b/'reviews/batch_05/cell_image_frame_code_recheck.md']:
  files.add(p)
 files.update(p for p in (b/'reviews/batch_04/evidence/cell_assets').rglob('*') if p.is_file())
if n=='gensci_1_5':
 files.update(p for p in (b/'reviews/batch_05/evidence/respiration_primary').rglob('*') if p.is_file())
mp=b/'evidence'/f'{n}_reviewed_manifest.json'
files.discard(mp)
manifest=dict(module=n,lessons=len(m['lessons']),created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),content_fingerprint=fp,content_verdict='accepted',artifact_verdict='scoped_review_pass',teacher_acceptance='pending',partner_ingestion='R1supportpending',files=[dict(path=str(p.relative_to(b)),sha256=h(p)) for p in sorted(files)])
mp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');files.add(mp)
with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(files):z.write(p,p.relative_to(b))
with zipfile.ZipFile(zp) as z:
 assert z.testzip() is None
 for row in manifest['files']:assert hashlib.sha256(z.read(row['path'])).hexdigest()==row['sha256']
 entries=len(z.namelist())
receipt=dict(archive=zp.name,sha256=h(zp),bytes=zp.stat().st_size,entries=entries,docx=9,pdf=9,structured_exports=1,scope='Local teacher-review package includes keys;no classroom sign-off/publication/partner ingestion claim.')
(b/'evidence'/f'{n}_package.json').write_text(json.dumps(receipt,indent=2)+'\n')
p=b/'inventory/progress.json';d=json.loads(p.read_text())
for u in d['units']:
 if u['module']==n:u.update(source_status='verified',stage='independent_review_and_artifacts_complete',new_lesson_count=len(m['lessons']),review_state='content_and_artifacts_accepted',correction_passes=ca.get('correction_passes',0),next_action='Teacher classroom/practical/access/pacing acceptance and partner ingestion remain separate.',package=receipt['archive'])
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
