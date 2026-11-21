from pathlib import Path
import json,hashlib,sys,copy
ROOT=Path.cwd();b=ROOT/'data/curriculum_expansion_2026-11';o=Path(__file__).resolve().parent;p1=json.loads((b/'reviews/batch_06/evidence/essmath_3_2_recheck/binding.json').read_text());i=json.loads((b/'reviews/batch_06/evidence/essmath_3_2_initial/binding.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();h=lambda s:hashlib.sha256(s.encode()).hexdigest()
bp_path=b/'blueprints/essmath_3_2.json';bp=json.loads(bp_path.read_text());m=json.loads((b/'manuscripts/essmath_3_2.json').read_text());states={'manuscript_L9':m['lessons'][8]['outcomes'],'blueprint_L9':bp['lesson_map'][8]['outcomes'],'F9_task':next(x['outcomes'] for x in bp['assessment_tasks'] if x['id']=='F9'),'F9_map':next(x['outcomes'] for x in bp['assessment_map'] if x['task']=='F9')};assert all(x==['b','d','f','h','i'] for x in states.values())
inputs={};unchanged={}
for k in ['sources','materials','manuscripts','blueprints']:
 p=b/k/'essmath_3_2.json';rel=str(p.relative_to(ROOT));inputs[rel]=sha(p)
 if k!='blueprints':unchanged[k]=sha(p)==p1['inputs'][rel];assert unchanged[k]
old=copy.deepcopy(bp);old['lesson_map'][8]['outcomes'].insert(1,'c');flags=[v for v in [False,True] if json.dumps(bp,ensure_ascii=v,indent=2)+'\n'==bp_path.read_text()];assert flags
restored=h(json.dumps(old,ensure_ascii=flags[0],indent=2)+'\n');assert restored==p1['inputs'][str(bp_path.relative_to(ROOT))]
initial=copy.deepcopy(bp)
for row in [initial['lesson_map'][8],next(x for x in initial['assessment_tasks'] if x['id']=='F9'),next(x for x in initial['assessment_map'] if x['task']=='F9')]:row['outcomes'].insert(1,'c')
assert h(json.dumps(initial,ensure_ascii=flags[0],indent=2)+'\n')==i['inputs'][str(bp_path)]
oldm=copy.deepcopy(m);oldm['lessons'][8]['outcomes'].insert(1,'c');mflags=[v for v in [False,True] if json.dumps(m,ensure_ascii=v,indent=2)+'\n'==(b/'manuscripts/essmath_3_2.json').read_text()];assert mflags;assert h(json.dumps(oldm,ensure_ascii=mflags[0],indent=2)+'\n')==i['inputs'][str(b/'manuscripts/essmath_3_2.json')]
sys.path.insert(0,str(ROOT/'scripts'));from curriculum_pipeline import content_fingerprint
fp=content_fingerprint(b,'essmath_3_2');assert fp=='7340b23168e2832985c6ba588d8635c6a6d95eabb7657ac6a138ba1331786e43'
words={k:{'path':v['path'],'sha256':sha(ROOT/v['path']),'unchanged_since_initial':sha(ROOT/v['path'])==v['sha256']} for k,v in i['words'].items()};assert all(v['unchanged_since_initial'] for v in words.values())
reports={str(p.relative_to(ROOT)):sha(p) for p in [b/'reviews/batch_06/essmath_3_2_initial.md',b/'reviews/batch_06/essmath_3_2_recheck.md']};assert list(reports.values())==['874ffac162b08872ba94158900bf3f88f66755b6621f2ea9fc33bb79ff2cbd1c','56e2196d1e6252f3e402cb98ede4836dfdc236d686c011ce4112f3f16f950d5a']
r={'verdict':'PASS / ACCEPTED under explicit binary-component interpretation','content_fingerprint':fp,'confirmed_open_errors':0,'finding_closed':'EM32-C1','map_states':states,'inputs':inputs,'unchanged_since_pass1':unchanged,'pass1_blueprint_restored_sha256':restored,'exact_initial_hash_reconstruction_all4_mappings':True,'actual_words':words,'prior_reports':reports,'classroom_source_cap_confirmation_obtained':False,'prose_tasks_answers_rubric_source_materials_unchanged':True};(o/'binding.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(states));print(fp);print('Exact scope PASS; all5 unchanged actual companions; immutable reports verified')
