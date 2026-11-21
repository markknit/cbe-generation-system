"""Narrow isolated preflight proof. Copies reviewed helper; cannot reach production paths/state."""
from pathlib import Path
import json,hashlib,difflib,subprocess,sys,os,zipfile
E=Path(__file__).parent;B=E.parents[2];src=B/'evidence/procedures/package_reviewed_unit.py';prior=E/'package_audit_date_core27/reviewed_package_helper.py';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old=prior.read_text();new=src.read_text();block="""archive_name=sys.argv[5] if len(sys.argv)>5 else n+'_Reviewed.zip'
if Path(archive_name).name!=archive_name or Path(archive_name).suffix!='.zip':
 raise ValueError('archive name must be a simple .zip filename')
zp=b/archive_name
if zp.exists():
 raise FileExistsError('Frozen archive already exists; choose an explicit new version: '+str(zp))
"""
assert new.count(block)==1
restored=new.replace(block,'').replace("with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED) as z:","zp=b/(n+'_Reviewed.zip')\nwith zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED) as z:",1);assert restored==old
F=E/'package_version_guard_science_fixture';F.mkdir(exist_ok=False)
(F/'scripts').mkdir();(F/'scripts/curriculum_pipeline.py').write_text("def content_fingerprint(*args, **kwargs):\n    raise RuntimeError('UNEXPECTED_CANONICAL_ACCESS')\n")
helper=F/'reviewed_package_helper.py';helper.write_bytes(src.read_bytes());assert sha(helper)==sha(src)
b=F/'data/curriculum_expansion_2026-11';b.mkdir(parents=True);(F/'report.md').write_text('Isolated deliberately unmatched report.\n')
for name in ['isolated_unit_Reviewed.zip','isolated_unit_Reviewed_v1.zip']:
 with zipfile.ZipFile(b/name,'w',zipfile.ZIP_DEFLATED) as z:z.writestr('frozen.txt','Immutable isolated archive fixture.\n')
# Sentinels would expose acceptance/manifest/receipt/progress writes without relying on exceptions alone.
for path in ['reviews/isolated_unit/artifact_acceptance.json','evidence/isolated_unit_reviewed_manifest.json','evidence/isolated_unit_package.json','inventory/progress.json']:
 p=b/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('FROZEN SENTINEL '+path+'\n')
def snapshot():return {str(p.relative_to(F)):sha(p) for p in sorted(F.rglob('*')) if p.is_file()}
baseline=snapshot();env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1';results=[]
cases=[('existing default',None,'FileExistsError','Frozen archive already exists'),('existing explicit frozen version','isolated_unit_Reviewed_v1.zip','FileExistsError','Frozen archive already exists'),('invalid parent path','../escape.zip','ValueError','archive name must be a simple .zip filename'),('invalid suffix','isolated_unit_v2.txt','ValueError','archive name must be a simple .zip filename'),('new explicit version reaches unchanged report guard','isolated_unit_Reviewed_v2.zip','AssertionError','assert h(report)==expected')]
for label,name,exception,marker in cases:
 args=[sys.executable,str(helper.resolve()),'isolated_unit','report.md','0'*64,'isolated review fixture']
 if name is not None:args.append(name)
 r=subprocess.run(args,cwd=F,env=env,text=True,capture_output=True)
 current=snapshot();ok=r.returncode!=0 and exception in r.stderr and marker in r.stderr and 'UNEXPECTED_CANONICAL_ACCESS' not in r.stderr and not r.stdout and current==baseline
 results.append({'case':label,'optional_archive_name':name,'returncode':r.returncode,'expected_exception':exception,'stderr':r.stderr,'stdout':r.stdout,'all_files_unchanged':current==baseline,'pass':ok});assert ok,label
assert sha(src)==sha(helper)
result={'verdict':'PASS','scope':'Exactly six added preflight lines plus moved archive path assignment;five isolated fail-before-write scenarios only;no production helper execution or package/state mutation.','current_helper_sha256':sha(src),'prior_audit_date_helper_sha256':sha(prior),'exact_reverse_delta_matches_prior_reviewed_helper':True,'diff':''.join(difflib.unified_diff(old.splitlines(keepends=True),new.splitlines(keepends=True),fromfile='prior_audit_date_reviewed',tofile='version_guard')),'fixture_root':str(F),'fixture_initial_file_sha256':baseline,'cases':results,'all_fixture_files_unchanged':True,'production_helper_unchanged':True,'limit':'Preflight proof covers existing files at invocation under the serialized packaging workflow;it does not test successful production packaging or broaden earlier acceptance/audit review.'}
E.joinpath('package_version_guard_science_proof.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS:five isolated cases,all fixture archive/report/acceptance/manifest/receipt/progress bytes unchanged');print('helper SHA256',sha(src))
