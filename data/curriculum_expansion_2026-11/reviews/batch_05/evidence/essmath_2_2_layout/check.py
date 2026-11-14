"""Read actual Word/PDF artifacts; write only this review's JSON evidence."""
from pathlib import Path
import json, hashlib, re, subprocess, sys, zipfile
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[6]
sys.path.insert(0,str(ROOT/'scripts'))
from curriculum_pipeline import content_fingerprint
W=ROOT/'data/curriculum_expansion_2026-11'
D=json.loads((W/'manuscripts/essmath_2_2.json').read_text()); M=json.loads((W/'materials/essmath_2_2.json').read_text())
OUT=next((W/'outputs/v2').rglob(D['prefix']+'_data.json')).parent
TYPES=['CBE_LessonSequence','CompactTeacherGuide','StudentMaterials','MaterialsTeacherKey','FinalExplanation','FinalExplanation_TeacherKey','SummaryTable','StudentSummaryTable','AssessmentMaterials']
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','x':'http://www.w3.org/1999/xhtml'}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def norm(s):
 return re.sub(r'(?<=-)\s+(?=\w)','',re.sub(r'\s+',' ',s)).strip()
hashes={}; words={}; blocks={}; streams={}; page_counts={}; trees={}
for typ in TYPES:
 docx=OUT/(D['prefix']+'_'+typ+'.docx');pdf=W/'outputs/PDF'/(D['prefix']+'_'+typ+'.pdf')
 hashes[typ]={'docx_sha256':sha(docx),'pdf_sha256':sha(pdf)}
 with zipfile.ZipFile(docx) as z:
  trees[typ]=ET.fromstring(z.read('word/document.xml'))
  words[typ]=norm(' '.join(t.text or '' for t in trees[typ].findall('.//w:t',NS)))
 xml=ET.fromstring(subprocess.check_output(['pdftotext','-bbox-layout',str(pdf),'-']))
 pages=xml.findall('.//x:page',NS);page_counts[typ]=len(pages);blocks[typ]=[]
 for page_n,page in enumerate(pages,1):
  for b in page.findall('.//x:block',NS):
   blocks[typ].append({'page':page_n,'x':float(b.attrib['xMin']),'y':float(b.attrib['yMin']),
       'text':' '.join(t.text or '' for t in b.findall('.//x:word',NS))})
 # Global block order plus per-column streams preserve split-cell continuations.
 bs=blocks[typ]; ss=[('global bbox blocks',norm(' '.join(b['text'] for b in bs))),('body excluding portrait footer',norm(' '.join(b['text'] for b in bs if b['y']<740)))]
 colspecs={'CBE_LessonSequence':[(136,278),(288,434),(440,582),(592,736)],
           'CompactTeacherGuide':[(50,145),(145,310),(310,490),(490,620),(620,760)],
           'FinalExplanation':[(60,200),(210,335),(343,470),(477,603),(610,735)],
           'FinalExplanation_TeacherKey':[(60,200),(210,335),(343,470),(477,603),(610,735),(210,735)],
           'SummaryTable':[(60,175),(180,362),(368,550),(556,735)]}
 for xmin,xmax in colspecs.get(typ,[]):
  ss.append((f'column {xmin}..{xmax}',norm(' '.join(b['text'] for b in bs if xmin<=b['x']<xmax))))
 streams[typ]=ss
rows=[]
def check(typ,label,text):
 n=norm(text); matches=[method for method,stream in streams[typ] if n in stream]
 if not matches:
  matches=[method+'; whitespace-insensitive characters' for method,stream in streams[typ] if re.sub(r'\s+','',n) in re.sub(r'\s+','',stream)]
 rows.append({'document':typ,'field':label,'word_pass':n in words[typ],'pdf_pass':bool(matches),'pdf_method':matches[0] if matches else None,**({'expected':text} if not matches else {})})
for typ in ['CBE_LessonSequence','CompactTeacherGuide']:
 for i,l in enumerate(D['lessons'],1):
  check(typ,f'lesson{i}.title',l['title'])
  for j,p in enumerate(l['phases'],1):
   for k,t in enumerate(p,1):check(typ,f'lesson{i}.phase{j}.{k}',t)
  check(typ,f'lesson{i}.reflection',l['reflection'])
  for key in (['purpose','knowledge','skills','attitudes','inquiry','story','overview','safety'] if typ=='CBE_LessonSequence' else ['purpose','knowledge','safety']):check(typ,f'lesson{i}.{key}',l[key])
source=json.loads((W/'sources/essmath_2_2.json').read_text())
for field in ['coreCompetencies','values','pcis']:check('CBE_LessonSequence','source.'+field,source[field])
for o in source['outcomes']:check('CBE_LessonSequence','source.outcome.'+o['id'],o['text'])
for typ in ['FinalExplanation','FinalExplanation_TeacherKey']:
 check(typ,'assessment.instructions',D['assessment']['instructions'])
 for i,s in enumerate(D['assessment']['sections'],1):
  check(typ,f'assessment.section{i}.prompt',s['prompt'])
  if typ.endswith('TeacherKey'):check(typ,f'assessment.section{i}.exemplar',s['exemplar'])
 for i,r in enumerate(D['assessment']['rubric'],1):
  for k,t in r.items():check(typ,f'assessment.rubric{i}.{k}',t)
for i,l in enumerate(D['lessons'],1):
 for k,t in l['summary'].items():
  check('SummaryTable',f'lesson{i}.summary.{k}',t)
  check('CBE_LessonSequence',f'lesson{i}.summary.{k}',t)
for c in M['items']:
 check('AssessmentMaterials' if c['id']=='RF12' else 'StudentMaterials',c['id']+'.student',c['student'])
 check('MaterialsTeacherKey',c['id']+'.student',c['student']);check('MaterialsTeacherKey',c['id']+'.teacher',c['teacher'])
# Procedural isolation and blank response evidence, independent of string-presence checks.
answer_rows=[]
for table in trees['FinalExplanation'].findall('.//w:tbl',NS):
 rs=table.findall('w:tr',NS)
 if len(rs)==3:
  first=''.join(t.text or '' for t in rs[0].findall('.//w:t',NS))
  if any(first==section['title'] for section in D['assessment']['sections']):
   answer_rows.append(''.join(t.text or '' for t in rs[2].findall('.//w:t',NS)).strip())
blank_final_answers=len(answer_rows)==4 and all(t=='Write your answer here:' for t in answer_rows)
attribution={}
for typ in TYPES:
 with zipfile.ZipFile(OUT/(D['prefix']+'_'+typ+'.docx')) as z:
  xml=' '.join(z.read(p).decode() for p in z.namelist() if p.startswith('word/') and p.endswith('.xml'))
 attribution[typ]={'word':all(t in xml for t in ['ChatGPT/Codex','OpenAI']),
                   'pdf':all(any(t in stream for _,stream in streams[typ]) for t in ['ChatGPT/Codex','OpenAI'])}

blank=True
for r in trees['StudentSummaryTable'].findall('.//w:tbl/w:tr',NS)[1:]:
 for c in r.findall('w:tc',NS)[1:]:
  blank=blank and not ''.join(t.text or '' for t in c.findall('.//w:t',NS)).strip()
student_exemplars_absent={typ:all(norm(s['exemplar']) not in words[typ] and not any(norm(s['exemplar']) in t for _,t in streams[typ]) for s in D['assessment']['sections']) for typ in ['FinalExplanation','StudentMaterials','AssessmentMaterials']}
export=json.loads((OUT/(D['prefix']+'_data.json')).read_text()); finalslots={phase:{k:v[k] for k in ('video','reading')} for phase,v in export['LESSONS'][-1]['resourceLinks'].items()}
selected=[{'lesson':l['number'],'phase':phase,'kind':k,'title':v[k]['title'],'source':v[k]['source']} for l in export['LESSONS'] for phase,v in l['resourceLinks'].items() for k in ('video','reading') if v[k]]
allowed=json.loads((W/'resource_policy.json').read_text())['module_allowed_titles']['essmath_2_2']
result={'content_fingerprint':content_fingerprint(W,'essmath_2_2'),'artifact_hashes':hashes,'pdf_pages':page_counts,'checks':rows,'checks_total':len(rows),
        'word_pass':sum(r['word_pass'] for r in rows),'pdf_pass':sum(r['pdf_pass'] for r in rows),
        'blank_final_answer_cells':blank_final_answers,'attribution_openai':attribution,'blank_student_summary':blank,'student_exemplars_absent':student_exemplars_absent,
        'final_RF12_absent_teaching_student':all('RF12' not in stream for _,stream in streams['StudentMaterials']) and 'RF12' not in words['StudentMaterials'],
        'final_slots':finalslots,'final_slots_null':all(x is None for v in finalslots.values() for x in v.values()),'selected_resources':selected,'selected_titles_allowed':all(r['title'] in allowed for r in selected),
        'normalization':'First collapse whitespace and join whitespace after retained hyphens. Fallback ignores whitespace only (PDF adds spaces at wrapped algebra/long comma lists); all nonspace characters, punctuation and mathematical glyphs retained. Column streams recover same-cell page continuations.'}
# Bind unchanged current five companions and original blank grid bytes/aspects.
recheck=json.loads((Path(__file__).parent.parent/'essmath_2_2_recheck/binding.json').read_text())
result['draft_hashes_match_content_recheck']=all(hashes[k]['docx_sha256']==v['sha256'] for k,v in recheck['words'].items())
result['acceptance_record_sha256']=sha(W/'reviews/essmath_2_2/content_acceptance.json')
from docx import Document
from PIL import Image
result['grid_embeds']={}
for typ,ids in [('StudentMaterials',['RF4','RF5','RF6','RF8','RF9']),('MaterialsTeacherKey',['RF4','RF5','RF6','RF8','RF9','RF12']),('AssessmentMaterials',['RF12'])]:
 expected={sha(W/'materials/diagrams'/(k+'.png')) for k in ids}
 doc=Document(OUT/(D['prefix']+'_'+typ+'.docx'));entries=[]
 for inline in doc.inline_shapes:
  blip=inline._inline.graphic.graphicData.pic.blipFill.blip
  data=doc.part.related_parts[blip.embed].blob
  entries.append({'sha256':hashlib.sha256(data).hexdigest(),'aspect_ratio_preserved':abs(inline.width/inline.height-1)<1e-4})
 result['grid_embeds'][typ]={'expected_count':len(ids),'actual_count':len(entries),'entries':entries,'pass':len(entries)==len(ids) and {e['sha256'] for e in entries}==expected and all(e['aspect_ratio_preserved'] for e in entries)}
if not result['draft_hashes_match_content_recheck'] or not all(x['pass'] for x in result['grid_embeds'].values()):raise SystemExit('Draft/grid hash or aspect/count mismatch')
result['final_RF12_grid_absent_teaching_student']=sha(W/'materials/diagrams/RF12.png') not in {e['sha256'] for e in result['grid_embeds']['StudentMaterials']['entries']}
result['export_final_equals_canonical']=export['FINAL_EXPLANATION']==D['assessment']
Path(__file__).with_suffix('.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'checks_total':len(rows),'word_pass':result['word_pass'],'pdf_pass':result['pdf_pass'],'pages':page_counts,'failures':[r for r in rows if not r['word_pass'] or not r['pdf_pass']]},ensure_ascii=False,indent=2))
if result['word_pass']!=len(rows) or result['pdf_pass']!=len(rows) or not all([blank,blank_final_answers,result['final_RF12_absent_teaching_student'],result['final_RF12_grid_absent_teaching_student'],result['final_slots_null'],result['selected_titles_allowed'],result['export_final_equals_canonical'],*student_exemplars_absent.values()]) or not all(all(v.values()) for v in attribution.values()):raise SystemExit(1)
