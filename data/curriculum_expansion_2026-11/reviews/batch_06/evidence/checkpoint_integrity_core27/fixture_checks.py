"""Run unchanged utility in temporary fixture roots, never production data."""
import hashlib,json,subprocess,sys,tempfile,zipfile
from pathlib import Path
R=Path(__file__).resolve().parents[6]
UTILITY=R/'data/curriculum_expansion_2026-11/evidence/procedures/verify_reviewed_checkpoint.py'
sha=lambda x:hashlib.sha256(x).hexdigest()
types=['CBE_LessonSequence','SummaryTable','CompactTeacherGuide','StudentMaterials','MaterialsTeacherKey','StudentSummaryTable','AssessmentMaterials','FinalExplanation','FinalExplanation_TeacherKey']
results=[]
for case in ['baseline','artifact_HOLD_and_changed_layout_report','wrong_nine_document_types','empty_member_manifest','archived_canonical_differs','bad_receipt_sha_control','bad_member_sha_control']:
 with tempfile.TemporaryDirectory(prefix='checkpoint_review_') as tmp:
  root=Path(tmp);b=root/'data/curriculum_expansion_2026-11';(root/'scripts').mkdir();(root/'scripts/curriculum_pipeline.py').write_text('def content_fingerprint(base, module): return "accepted-fingerprint"\n')
  def put(p,v):
   p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(v if isinstance(v,bytes) else json.dumps(v).encode())
  put(b/'manuscripts/demo.json',{'prefix':'Demo','lessons':[{}],'subject':'Fixture'})
  put(b/'inventory/progress.json',{'units':[]})
  report='data/curriculum_expansion_2026-11/reviews/content.md';put(root/report,b'accepted content report')
  put(b/'reviews/demo/content_acceptance.json',{'verdict':'accepted','unresolved_confirmed_errors':0,'content_fingerprint':'accepted-fingerprint','evidence':[{'path':report,'sha256':sha(b'accepted content report')}]})
  layout='data/curriculum_expansion_2026-11/reviews/layout.md';put(root/layout,b'changed layout report' if case=='artifact_HOLD_and_changed_layout_report' else b'accepted layout report')
  artifact_acceptance={'verdict':'HOLD' if case=='artifact_HOLD_and_changed_layout_report' else 'accepted','content_fingerprint':'accepted-fingerprint','evidence':[{'path':layout,'sha256':sha(b'accepted layout report')}],'artifacts':[]}
  put(b/'reviews/demo/artifact_acceptance.json',artifact_acceptance)
  entries={}
  for suffix in ['.docx','.pdf']:
   for i,t in enumerate(types):
    name=f'outputs/Demo_{"WrongType"+str(i) if case=="wrong_nine_document_types" else t}{suffix}';entries[name]=name.encode();put(b/name,entries[name])
  entries['outputs/Demo_data.json']=b'{}';put(b/'outputs/Demo_data.json',b'{}')
  for p in ['reviews/demo/content_acceptance.json','reviews/demo/artifact_acceptance.json','reviews/content.md','manuscripts/demo.json']:entries[p]=(b/p).read_bytes()
  entries['reviews/layout.md']=b'accepted layout report'
  if case=='archived_canonical_differs':entries['manuscripts/demo.json']=b'{"prefix":"OLD","lessons":[],"subject":"Old"}'
  manifest={'module':'demo','content_fingerprint':'accepted-fingerprint','files':[] if case=='empty_member_manifest' else [{'path':p,'sha256':sha(v)} for p,v in entries.items()]}
  if case=='bad_member_sha_control':manifest['files'][0]['sha256']='0'*64
  entries['evidence/demo_manifest.json']=json.dumps(manifest).encode()
  zp=b/'Fixture.zip'
  with zipfile.ZipFile(zp,'w') as z:
   for p,v in entries.items():z.writestr(p,v)
  put(b/'evidence/demo_package.json',{'archive':'Fixture.zip','sha256':'0'*64 if case=='bad_receipt_sha_control' else sha(zp.read_bytes())})
  r=subprocess.run([sys.executable,str(UTILITY)],cwd=root,text=True,capture_output=True)
  try:out=json.loads(r.stdout)
  except ValueError:out={'stderr':r.stderr,'stdout':r.stdout}
  results.append({'case':case,'exit_code':r.returncode,'result':out})
p=Path(__file__).with_name('fixture_results.json');p.write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
