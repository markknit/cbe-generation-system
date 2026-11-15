from pathlib import Path
import json,hashlib,zipfile,re,sys,xml.etree.ElementTree as ET
R=Path.cwd();B=R/'data/curriculum_expansion_2026-11';E=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'scripts'))
from curriculum_pipeline import content_fingerprint
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();norm=lambda s:re.sub(r'\s+','',s);N=json.loads((B/'manuscripts/coremath_2_2.json').read_text());M=json.loads((B/'materials/coremath_2_2.json').read_text());S=json.loads((B/'sources/coremath_2_2.json').read_text());V=json.loads((B/'sources/coremath_2_2.verification.json').read_text());ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'};out=next((B/'outputs/v2').rglob(N['prefix']+'_CompactTeacherGuide.docx')).parent;T={};X={};docs={};checks={}
for p in sorted(out.glob('*.docx')):
 k=p.stem.removeprefix(N['prefix']+'_')
 with zipfile.ZipFile(p) as z:
  x=ET.fromstring(z.read('word/document.xml'));X[k]=x;T[k]='\n'.join(''.join(t.text or '' for t in q.findall('.//w:t',ns)) for q in x.findall('.//w:p',ns));xml=' '.join(z.read(q).decode() for q in z.namelist() if q.startswith('word/') and q.endswith('.xml'));media=[q for q in z.namelist() if q.startswith(('word/media/','word/embeddings/'))]
 docs[k]={'path':str(p.relative_to(R)),'sha256':sha(p),'media':media};(E/f'{k}.txt').write_text(T[k]);checks[k+'_attribution']=all(t in xml for t in ['SeaVuria','ARES','ChatGPT/Codex','OpenAI','BY-NC','4.0'])
for c in M['items']:
 for fld in ['student','teacher']:checks[c['id']+'_key_'+fld]=norm(c[fld]) in norm(T['MaterialsTeacherKey'])
 checks[c['id']+'_student']=norm(c['student']) in norm(T['AssessmentMaterials' if c['id']=='CRG13' else 'StudentMaterials'])
for l in N['lessons']:
 for fld in ['title','purpose','knowledge','safety','reflection']:checks[f'L{l["number"]}_{fld}']=norm(l[fld]) in norm(T['CompactTeacherGuide'])
 for i,phase in enumerate(l['phases'],1):
  for j,t in enumerate(phase,1):checks[f'L{l["number"]}_phase{i}_{j}']=norm(t) in norm(T['CompactTeacherGuide'])
 checks[f'L{l["number"]}_40min']=sum(l['minutes'])==40
for o in S['outcomes']:checks['source_'+o['id']]=norm(o['text']) in norm(T['CompactTeacherGuide'])
checks['CRG13_absent_teaching']='CRG13' not in T['StudentMaterials'];checks['CRG13_present_assessment']='CRG13' in T['AssessmentMaterials'];checks['assessment_no_teacher_answer']=norm(M['items'][-1]['teacher']) not in norm(T['AssessmentMaterials'])
rows=X['StudentSummaryTable'].findall('.//w:tr',ns);checks['thirteen_summary_rows']=len(rows)==14
for i,row in enumerate(rows[1:],1):checks[f'blank_row{i}']=all(not ''.join(t.text or '' for t in c.findall('.//w:t',ns)).strip() for c in row.findall('w:tc',ns)[1:])
sourcechecks={'pdf':sha(R/S['pdf'])==S['pdf_sha256'],'source':sha(B/'sources/coremath_2_2.json')==V['source_record_sha256'],'crop':sha(B/'sources/coremath_2_2_source.png')==V['crop_sha256'],'verification_evidence':sha(R/V['evidence'])==V['evidence_sha256']}
paths=[B/f'{k}/coremath_2_2.json' for k in ['sources','materials','blueprints','manuscripts']]+[B/'sources/coremath_2_2.verification.json'];binding={'fingerprint':content_fingerprint(B,'coremath_2_2'),'inputs':{str(p.relative_to(R)):sha(p) for p in paths},'sourcefiles':{str(p.relative_to(R)):sha(p) for p in [R/S['pdf'],B/'sources/coremath_2_2_source.png',R/V['evidence']]},'sourcechecks':sourcechecks,'documents':docs,'checks':checks,'passed':sum(checks.values()),'total':len(checks),'failed':[k for k,v in checks.items() if not v],'note':'Propagation/structure pass does not resolve absent task inputs, semantic mapping or project-performance coverage.'}
(E/'binding.json').write_text(json.dumps(binding,indent=2)+'\n');print(json.dumps({k:binding[k] for k in ['fingerprint','passed','total','failed','sourcechecks','documents']},indent=2))
