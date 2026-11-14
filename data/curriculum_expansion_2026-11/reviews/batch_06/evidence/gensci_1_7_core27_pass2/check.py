from pathlib import Path
import json,hashlib,zipfile,re,sys,xml.etree.ElementTree as ET
R=Path.cwd();B=R/'data/curriculum_expansion_2026-11';E=Path(__file__).resolve().parent;P=E.parent/'gensci_1_7_core27_pass1';sys.path.insert(0,str(R/'scripts'))
from curriculum_pipeline import content_fingerprint
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();norm=lambda s:re.sub(r'\s+','',s);old=json.loads((P/'binding.json').read_text());N=json.loads((B/'manuscripts/gensci_1_7.json').read_text());scope=json.loads((E/'restoration_scope.json').read_text());checks={};ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'};docs={};T={}
checks['immutable_pass1_report']=sha(B/'reviews/batch_06/gensci_1_7_review_core27_pass1.md')=='6c6d4491dd96d322b5af57898bec680d65ddba59b1c31959f68906cbd1c7599d'
for p,h in old['inputs'].items():
 if '/manuscripts/' not in p:checks['unchanged_'+p]=sha(R/p)==h
for p,h in old['sourcefiles'].items():checks['source_unchanged_'+p]=sha(R/p)==h
restored=json.loads(json.dumps(N))
for fld in ['story','minutes','phases']:restored['lessons'][-1][fld]=scope['old_'+fld]
checks['exact_pass1_restoration']=hashlib.sha256((json.dumps(restored,ensure_ascii=False,indent=2)+'\n').encode()).hexdigest()==scope['pass1_manuscript_sha256']
for k,d in old['documents'].items():
 p=R/d['path']
 with zipfile.ZipFile(p) as zz:
  x=ET.fromstring(zz.read('word/document.xml'));T[k]='\n'.join(''.join(t.text or '' for t in q.findall('.//w:t',ns)) for q in x.findall('.//w:p',ns));xml=' '.join(zz.read(q).decode() for q in zz.namelist() if q.startswith('word/') and q.endswith('.xml'));media=[q for q in zz.namelist() if q.startswith('word/media/')]
 docs[k]={'path':d['path'],'sha256':sha(p),'media':media};(E/f'{k}.txt').write_text(T[k]);checks[k+'_attribution']=all(t in xml for t in ['SeaVuria','ARES','ChatGPT/Codex','OpenAI','BY-NC','4.0']);checks[k+'_no_media']=not media
 if k!='CompactTeacherGuide':checks[k+'_text_unchanged']=norm(T[k])==norm((P/f'{k}.txt').read_text())
oldguide=(P/'CompactTeacherGuide.txt').read_text();tag='Lesson 12:';checks['guide_beforeL12_unchanged']=T['CompactTeacherGuide'].split(tag)[0]==oldguide.split(tag)[0];guide=T['CompactTeacherGuide'].split(tag,1)[1];l=N['lessons'][-1]
for fld in ['title','purpose','knowledge','safety','reflection']:checks['L12_'+fld]=norm(l[fld]) in norm(guide)
for i,ph in enumerate(l['phases']):
 for j,t in enumerate(ph):checks[f'L12_phase{i+1}_{j+1}']=norm(t) in norm(guide)
 checks[f'L12_phase{i+1}_time']=norm(str(l['minutes'][i])+' minutes. '+ph[1]) in norm(guide)
checks['timing_5_10_10_10_5']=l['minutes']==[5,10,10,10,5] and sum(l['minutes'])==40
for t in ['5minutes read MI12','10minutes Section1','10minutes Section2','10minutes Section3','5minutes check']:checks['final_instruction_'+t]=t in N['assessment']['instructions']
checks['no_old_guided_plan']=scope['old_phases'][0][1] not in guide;checks['no_old_guided_review']=scope['old_phases'][3][1] not in guide;checks['collect_before_feedback']='Collect before any feedback,discussion or teaching.' in guide
out={'fingerprint':content_fingerprint(B,'gensci_1_7'),'inputs':{p:sha(R/p) for p in old['inputs']},'sourcefiles':old['sourcefiles'],'documents':docs,'passed':sum(checks.values()),'total':len(checks),'failed':[k for k,v in checks.items() if not v],'checks':checks,'restoration_scope':scope,'scope':'Focused correction pass2 only; existing full current pass1 source/tasks/answers/mappings review remains applicable.'}
(E/'binding.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['fingerprint','passed','total','failed','documents']},indent=2));assert all(checks.values())
