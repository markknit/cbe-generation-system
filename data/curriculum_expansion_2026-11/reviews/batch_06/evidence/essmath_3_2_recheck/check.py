from pathlib import Path
import json,hashlib,sys,copy
ROOT=Path.cwd();b=ROOT/'data/curriculum_expansion_2026-11';o=Path(__file__).resolve().parent;i=json.loads((b/'reviews/batch_06/evidence/essmath_3_2_initial/binding.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();h=lambda s:hashlib.sha256(s.encode()).hexdigest()
inputs={};reconstruct={}
for k in ['sources','materials','blueprints','manuscripts']:
 p=b/k/'essmath_3_2.json';d=json.loads(p.read_text());inputs[str(p.relative_to(ROOT))]=sha(p)
 if k in ['blueprints','manuscripts']:
  flags=[v for v in [False,True] if json.dumps(d,ensure_ascii=v,indent=2)+'\n'==p.read_text()];assert flags;old=copy.deepcopy(d)
  if k=='blueprints':
   next(x for x in old['assessment_tasks'] if x['id']=='F9')['outcomes'].insert(1,'c');next(x for x in old['assessment_map'] if x['task']=='F9')['outcomes'].insert(1,'c')
  else:old['lessons'][8]['outcomes'].insert(1,'c')
  reconstruct[k]={'restored_sha256':h(json.dumps(old,ensure_ascii=flags[0],indent=2)+'\n'),'initial_sha256':i['inputs'][str(p)]};assert reconstruct[k]['restored_sha256']==reconstruct[k]['initial_sha256']
 else:assert sha(p)==i['inputs'][str(p)]
sys.path.insert(0,str(ROOT/'scripts'));from curriculum_pipeline import content_fingerprint
fp=content_fingerprint(b,'essmath_3_2');assert fp=='547ab588a7ead1666b5ceda978e3b21756d758b492ce96c56deb2e8edf867324'
bp=json.loads((b/'blueprints/essmath_3_2.json').read_text());m=json.loads((b/'manuscripts/essmath_3_2.json').read_text());current={k:{'path':v['path'],'initial_sha256':v['sha256'],'current_sha256':sha(ROOT/v['path']),'unchanged':sha(ROOT/v['path'])==v['sha256']} for k,v in i['words'].items()};assert all(v['unchanged'] for v in current.values())
r={'scope':'Correction pass1 focused exact-diff and actual unchanged companion binding; not accepted','content_fingerprint':fp,'verdict':'HOLD','finding':'EM32-C1 remains open only in blueprint lesson_map lesson9','inputs':inputs,'original_report_sha256':sha(b/'reviews/batch_06/essmath_3_2_initial.md'),'exact_initial_reconstruction':reconstruct,'actual_words':current,'map_states':{'manuscript_L9':m['lessons'][8]['outcomes'],'blueprint_L9':bp['lesson_map'][8]['outcomes'],'F9_task':next(x['outcomes'] for x in bp['assessment_tasks'] if x['id']=='F9'),'F9_map':next(x['outcomes'] for x in bp['assessment_map'] if x['task']=='F9')},'prose_materials_source_assessment_answers_rubric_unchanged':True}
(o/'binding.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r['map_states']));print('Exact3-location restoration matches original byte hashes; all5 companion bytes unchanged; fingerprint confirmed')
