from pathlib import Path
import json,hashlib,subprocess,sys,os,zipfile,difflib,datetime
E=Path(__file__).resolve().parent;R=Path.cwd();B=R/'data/curriculum_expansion_2026-11';source=B/'evidence/procedures/package_reviewed_unit.py';prior=E/'reviewed_package_helper.py';F=E/'closure_fixtures_v3';F.mkdir(exist_ok=False);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();n='essmath_1_3';helperbytes=source.read_bytes();env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
def put(root,path,raw):
 p=root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw if isinstance(raw,bytes) else raw.encode());return p
def snap(root):return {str(p.relative_to(root)):sha(p) for p in sorted(root.rglob('*')) if p.is_file()}
def setup(label):
 f=F/label;f.mkdir();b=f/'data/curriculum_expansion_2026-11';b.mkdir(parents=True);put(f,'helper.py',helperbytes);put(f,'scripts/curriculum_pipeline.py',"def content_fingerprint(*args,**kwargs):\n return 'isolated-fingerprint'\n")
 report=put(b,'reviews/batch_07/essmath_1_3_layout_v2.md','Isolated artifact report,not an actual acceptance.');legacy=put(b,'reviews/batch_03/essmath_1_3_initial.md',(B/'reviews/batch_03/essmath_1_3_initial.md').read_bytes());put(b,'reviews/batch_03/essmath_1_3_layout_review.md',(B/'reviews/batch_03/essmath_1_3_layout_review.md').read_bytes());put(b,'reviews/batch_03/evidence/essmath_1_3_probe.json','Legacy module evidence.');put(b,'reviews/batch_03/evidence/other_module_probe.json','Unrelated evidence excluded.');closure=put(b,'reviews/batch_07/essmath_1_3_content_v2.md','Isolated new CA closure.');outside=put(f,'data/outside.md','Outside workspace proof.');
 for p in ['reviews/essmath_1_3/artifact_acceptance.json','evidence/essmath_1_3_reviewed_manifest.json','evidence/essmath_1_3_package.json','inventory/progress.json']:put(b,p,'FROZEN sentinel '+p)

 with zipfile.ZipFile(b/(n+'_Reviewed.zip'),'w',zipfile.ZIP_DEFLATED) as z:z.writestr('frozen.txt','Frozen original isolated archive.')
 return f,b,report,legacy,closure,outside
def evidence(p):return {'path':str(p),'sha256':sha(p)}
results=[]
for label in ['dotdot_escape','symlink_escape','bad_hash','empty_evidence']:
 f,b,report,legacy,closure,outside=setup(label)
 if label=='dotdot_escape':entry=evidence(outside);entry['path']='data/curriculum_expansion_2026-11/../outside.md';items=[entry]
 elif label=='symlink_escape':link=b/'reviews/escape.md';link.symlink_to(outside);items=[evidence(link)]
 elif label=='bad_hash':items=[{'path':str(legacy),'sha256':'0'*64}]
 else:items=[]
 ca={'verdict':'accepted','content_fingerprint':'isolated-fingerprint','evidence':items};put(b,'reviews/essmath_1_3/content_acceptance.json',json.dumps(ca));before=snap(f)
 run=subprocess.run([sys.executable,str(f/'helper.py'),n,str(report.relative_to(f)),sha(report),'isolated proof',n+'_Reviewed_v2.zip'],cwd=f,env=env,text=True,capture_output=True);after=snap(f)
 ok=run.returncode!=0 and 'AssertionError' in run.stderr and before==after and not (b/(n+'_Reviewed_v2.zip')).exists();results.append({'case':label,'pass':ok,'all_files_unchanged':before==after,'before_hashes':before,'after_hashes':after,'stderr':run.stderr});assert ok,label
# Positive fixture executes the exact helper with synthetic artifacts only.
f,b,report,legacy,closure,outside=setup('valid_legacy_and_new_reports');prefix='Isolated_Quadratics';types=['CBE_LessonSequence','CompactTeacherGuide','StudentMaterials','MaterialsTeacherKey','FinalExplanation','FinalExplanation_TeacherKey','SummaryTable','StudentSummaryTable','AssessmentMaterials'];rows=[]
for typ in types:
 doc=put(b,f'outputs/v2/Isolated/{prefix}_{typ}.docx',f'isolated DOCX placeholder {typ}');pdf=put(b,f'outputs/PDF/{prefix}_{typ}.pdf',f'isolated PDF placeholder {typ}');rows.append({'module':n,'type':typ,'docx_sha256':sha(doc),'pdf_sha256':sha(pdf)})
put(b,f'outputs/v2/Isolated/{prefix}_data.json','{}');put(b,f'evidence/artifact_audit_{n}_2026-11-15.json',json.dumps({'documents':rows}));put(b,f'evidence/{n}_resource_policy_snapshot.json','{}');put(b,f'manuscripts/{n}.json',json.dumps({'prefix':prefix,'lessons':[{'number':1}]}));put(b,f'materials/{n}.json','{"items":[]}');put(b,'attribution.yaml','Isolated attribution.');put(b,'inventory/progress.json',json.dumps({'units':[{'module':n}]}));
# A non-normalised absolute alias tests normalization before archive use;legacy bytes match the real report.
old_archive_sha=sha(b/(n+'_Reviewed.zip'));legacyalias=legacy.parent/'..'/'batch_03'/legacy.name;ca={'verdict':'accepted','content_fingerprint':'isolated-fingerprint','evidence':[evidence(legacyalias),evidence(closure)]};put(b,'reviews/essmath_1_3/content_acceptance.json',json.dumps(ca));run=subprocess.run([sys.executable,str(f/'helper.py'),n,str(report.relative_to(f)),sha(report),'isolated proof',n+'_Reviewed_v2.zip'],cwd=f,env=env,text=True,capture_output=True);assert run.returncode==0,run.stderr
zp=b/(n+'_Reviewed_v2.zip')
with zipfile.ZipFile(zp) as z:
 names=z.namelist();mp='evidence/'+n+'_reviewed_manifest.json';manifest=json.loads(z.read(mp));expected=['reviews/batch_03/essmath_1_3_initial.md','reviews/batch_03/essmath_1_3_layout_review.md','reviews/batch_03/evidence/essmath_1_3_probe.json','reviews/batch_07/essmath_1_3_content_v2.md'];checks={'old_archive_unchanged':sha(b/(n+'_Reviewed.zip'))==old_archive_sha,'manifest_no_self_entry':mp not in [r['path'] for r in manifest['files']],'manifest_covers_all_other_members':set(r['path'] for r in manifest['files'])==set(names)-{mp} and len(manifest['files'])==len(names)-1,'all_manifest_member_hashes':all(hashlib.sha256(z.read(r['path'])).hexdigest()==r['sha256'] for r in manifest['files']),'all_CA_reports_and_legacy_evidence_included':all(p in names for p in expected),'no_unrelated_asset':'reviews/batch_03/evidence/other_module_probe.json' not in names,'no_absolute_or_dotdot_members':all(not Path(p).is_absolute() and '..' not in Path(p).parts for p in names),'legacy_bytes_exact':z.read(expected[0])==legacy.read_bytes(),'CRC':z.testzip() is None};assert all(checks.values());results.append({'case':'valid_legacy_and_new_reports','pass':True,'checks':checks,'members':names,'receipt':json.loads(run.stdout),'helper_sha256':sha(f/'helper.py')})
# Production legacy report read-only recheck;no helper execution in production.
actualca=B/'reviews/essmath_1_3/content_acceptance.json';c=json.loads(actualca.read_text());actual=[]
for item in c['evidence']:
 p=Path(item['path']).resolve();actual.append({'path':str(p),'inside':p.is_relative_to(B.resolve()),'file':p.is_file(),'hash_match':sha(p)==item['sha256']})
result={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'helper_sha256':sha(source),'prior_HOLD_helper_sha256':sha(prior),'diff':''.join(difflib.unified_diff(prior.read_text().splitlines(True),source.read_text().splitlines(True))),'cases':results,'actual_current_CA_sha256':sha(actualca),'actual_current_CA_reports':actual,'production_helper_unchanged':sha(source)==hashlib.sha256(helperbytes).hexdigest(),'scope':'Exact helper executed only in isolated fixtures;negative cases snapshot every file before/after;positive uses synthetic 18artifact placeholders and two CA reports,one actual-byte legacy report. No production package or acceptance mutation.'}
(E/'manifest_closure_reviewed_helper.py').write_bytes(helperbytes);(E/'manifest_closure_proof.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS',len(results),'isolated cases; helper',sha(source));print('Actual CA reports',actual)
