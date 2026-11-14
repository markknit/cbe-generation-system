"""Execute verifier only in removed temporary fixture roots, using real fingerprint code."""
import hashlib,json,subprocess,sys,tempfile,zipfile
from pathlib import Path
R=Path(__file__).resolve().parents[6];UTILITY=R/'data/curriculum_expansion_2026-11/evidence/procedures/verify_reviewed_checkpoint.py'
sys.path.insert(0,str(R/'scripts'));from curriculum_pipeline import content_fingerprint
sha=lambda x:hashlib.sha256(x).hexdigest()
types=['CBE_LessonSequence','SummaryTable','CompactTeacherGuide','StudentMaterials','MaterialsTeacherKey','StudentSummaryTable','AssessmentMaterials','FinalExplanation','FinalExplanation_TeacherKey']
cases=['baseline','artifact_HOLD_and_changed_layout_report','wrong_nine_document_types','empty_member_manifest','archived_canonical_differs','bad_receipt_sha_control','bad_member_sha_control','legacy_fallback_positive','legacy_bad_verdict','legacy_changed_review','missing_implicit_image','changed_declared_asset','duplicate_manifest_row','artifact_acceptance_bad_hash','empty_content_evidence']
results=[]
for case in cases:
 with tempfile.TemporaryDirectory(prefix='checkpoint_recheck_') as tmp:
  root=Path(tmp);b=root/'data/curriculum_expansion_2026-11';(root/'scripts').mkdir();(root/'scripts/curriculum_pipeline.py').write_bytes((R/'scripts/curriculum_pipeline.py').read_bytes())
  def put(p,v):
   p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(v if isinstance(v,bytes) else json.dumps(v).encode())
  canonical={'manuscripts/demo.json':{'prefix':'Demo','lessons':[{}],'subject':'Fixture'},'sources/demo.json':{},'blueprints/demo.json':{},'materials/demo.json':{'items':[{'id':'D1','assets':['sample.bin']}]},'sources/demo.verification.json':{}}
  for p,v in canonical.items():put(b/p,v)
  for p,v in {'materials/diagrams/D1.png':b'implicit image','materials/sample.bin':b'declared asset'}.items():put(b/p,v)
  fp=content_fingerprint(b,'demo');put(b/'inventory/progress.json',{'units':[]})
  report='data/curriculum_expansion_2026-11/reviews/content.md';put(root/report,b'accepted content report')
  ca={'verdict':'accepted','unresolved_confirmed_errors':0,'content_fingerprint':fp,'evidence':[] if case=='empty_content_evidence' else [{'path':report,'sha256':sha(b'accepted content report')}]};put(b/'reviews/demo/content_acceptance.json',ca)
  layout='data/curriculum_expansion_2026-11/reviews/layout.md';put(root/layout,b'accepted layout report')
  entries={}
  for suffix in ['.docx','.pdf']:
   for i,t in enumerate(types):
    name=f'outputs/Demo_{"WrongType"+str(i) if case=="wrong_nine_document_types" else t}{suffix}';entries[name]=name.encode();put(b/name,entries[name])
  entries['outputs/Demo_data.json']=b'{}';put(b/'outputs/Demo_data.json',b'{}')
  ar={'verdict':'HOLD' if case=='artifact_HOLD_and_changed_layout_report' else 'accepted','content_fingerprint':fp,'evidence':[{'path':layout,'sha256':sha(b'accepted layout report')}],'artifacts':[{'path':p,'sha256':sha(v)} for p,v in entries.items()]}
  if case=='artifact_acceptance_bad_hash':ar['artifacts'][0]['sha256']='0'*64
  legacy=case.startswith('legacy_')
  if not legacy:put(b/'reviews/demo/artifact_acceptance.json',ar)
  for p in list(canonical)+['materials/diagrams/D1.png','materials/sample.bin','reviews/demo/content_acceptance.json','reviews/content.md','reviews/layout.md']+([] if legacy else ['reviews/demo/artifact_acceptance.json']):entries[p]=(b/p).read_bytes()
  if case in ['artifact_HOLD_and_changed_layout_report','legacy_changed_review']:put(root/layout,b'changed layout report')
  if case=='archived_canonical_differs':entries['manuscripts/demo.json']=b'{"prefix":"OLD","lessons":[],"subject":"Old"}'
  if case=='missing_implicit_image':del entries['materials/diagrams/D1.png']
  if case=='changed_declared_asset':entries['materials/sample.bin']=b'different asset'
  manifest={'module':'demo','content_fingerprint':fp,'artifact_verdict':'HOLD' if case=='legacy_bad_verdict' else 'scoped_review_pass','files':[] if case=='empty_member_manifest' else [{'path':p,'sha256':sha(v)} for p,v in entries.items()]}
  if case=='bad_member_sha_control':manifest['files'][0]['sha256']='0'*64
  if case=='duplicate_manifest_row':manifest['files'].append(manifest['files'][0].copy())
  entries['evidence/demo_manifest.json']=json.dumps(manifest).encode();zp=b/'Fixture.zip'
  with zipfile.ZipFile(zp,'w') as z:
   for p,v in entries.items():z.writestr(p,v)
  put(b/'evidence/demo_package.json',{'archive':'Fixture.zip','sha256':'0'*64 if case=='bad_receipt_sha_control' else sha(zp.read_bytes())})
  r=subprocess.run([sys.executable,str(UTILITY)],cwd=root,text=True,capture_output=True)
  try:out=json.loads(r.stdout)
  except ValueError:out={'stderr':r.stderr,'stdout':r.stdout}
  detail=json.loads((b/'evidence/checkpoint_integrity_2026-11-14.json').read_text()) if (b/'evidence/checkpoint_integrity_2026-11-14.json').exists() else {}
  expected=0 if case in ['baseline','legacy_fallback_positive'] else 1
  results.append({'case':case,'expected_exit':expected,'exit_code':r.returncode,'matches_expected':r.returncode==expected,'result':out,'created_utc':detail.get('created_utc'),'acceptance_mode':detail.get('modules',{}).get('demo',{}).get('artifact_acceptance_mode')})
p=Path(__file__).with_name('fixture_results.json');p.write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
