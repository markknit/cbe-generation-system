"""Read actual Word/PDF artifacts; write only this review's JSON evidence."""
from pathlib import Path
import json, hashlib, re, subprocess, sys, zipfile
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[6]
sys.path.insert(0,str(ROOT/'scripts'))
from curriculum_pipeline import content_fingerprint
W=ROOT/'data/curriculum_expansion_2026-11'
D=json.loads((W/'manuscripts/coremath_1_1.json').read_text()); M=json.loads((W/'materials/coremath_1_1.json').read_text())
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
 if typ=='CompactTeacherGuide':
  header_words={'Phase / time','Learner activity','Teacher moves','Sensemaking','Evidence / check'}
  for xmin,xmax in [(36,100),(100,260),(260,470),(470,600),(600,760)]:
   ss.append((f'R1 column {xmin}..{xmax}, exact repeated table header blocks excluded',norm(' '.join(b['text'] for b in bs if xmin<=b['x']<xmax and norm(b['text']) not in header_words))))
 streams[typ]=ss
rows=[]
def check(typ,label,text):
 n=norm(text); matches=[method for method,stream in streams[typ] if n in stream]
 if not matches:
  matches=[method+'; whitespace-insensitive characters' for method,stream in streams[typ] if re.sub(r'\s+','',n) in re.sub(r'\s+','',stream)]
 rows.append({'document':typ,'field':label,'word_pass':n in words[typ],'pdf_pass':bool(matches),'pdf_method':matches[0] if matches else None,**({'expected':text} if not matches else {})})
for k,v in D['unit'].items():
 if k not in ['keyInquiryQuestions','teacherConfirmationRequired']:check('CBE_LessonSequence','unit.'+k,v)
for typ in ['CBE_LessonSequence','CompactTeacherGuide']:
 for i,l in enumerate(D['lessons'],1):
  check(typ,f'lesson{i}.title',l['title'])
  for j,p in enumerate(l['phases'],1):
   for k,t in enumerate(p,1):check(typ,f'lesson{i}.phase{j}.{k}',t)
  check(typ,f'lesson{i}.reflection',l['reflection'])
  for key in (['purpose','knowledge','skills','attitudes','inquiry','story','overview','safety'] if typ=='CBE_LessonSequence' else ['purpose','knowledge','safety']):check(typ,f'lesson{i}.{key}',l[key])
source=json.loads((W/'sources/coremath_1_1.json').read_text())
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
 check('AssessmentMaterials' if c['id']=='CRN10' else 'StudentMaterials',c['id']+'.student',c['student'])
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
allowed=json.loads((W/'resource_policy.json').read_text())['module_allowed_titles']['coremath_1_1']
result={'content_fingerprint':content_fingerprint(W,'coremath_1_1'),'artifact_hashes':hashes,'pdf_pages':page_counts,'checks':rows,'checks_total':len(rows),
        'word_pass':sum(r['word_pass'] for r in rows),'pdf_pass':sum(r['pdf_pass'] for r in rows),
        'blank_final_answer_cells':blank_final_answers,'attribution_openai':attribution,'blank_student_summary':blank,'student_exemplars_absent':student_exemplars_absent,
        'final_CRN10_absent_teaching_student':all('CRN10' not in stream for _,stream in streams['StudentMaterials']) and 'CRN10' not in words['StudentMaterials'],
        'final_slots':finalslots,'final_slots_null':all(x is None for v in finalslots.values() for x in v.values()),'selected_resources':selected,'selected_titles_allowed':all(r['title'] in allowed for r in selected),
        'normalization':'First collapse whitespace and join whitespace after retained hyphens. Fallback ignores whitespace only (PDF adds spaces at wrapped algebra/long comma lists); all nonspace characters, punctuation and mathematical glyphs retained. Column streams recover same-cell page continuations.'}

audit_path=W/'evidence/artifact_audit_coremath_1_1_2026-11-15.json';audit=json.loads(audit_path.read_text());result['audit_sha256']=sha(audit_path);result['all18audit_hashes_match']=len(audit['documents'])==9 and {r['module'] for r in audit['documents']}=={'coremath_1_1'} and all(hashes[r['type']]['docx_sha256']==r['docx_sha256'] and hashes[r['type']]['pdf_sha256']==r['pdf_sha256'] for r in audit['documents'])
ca_path=W/'reviews/coremath_1_1/content_acceptance.json';ca=json.loads(ca_path.read_text());result['CA_sha256']=sha(ca_path);result['CA_fp_matches']=ca['verdict']=='accepted' and ca['content_fingerprint']==result['content_fingerprint'];result['CA_evidence']=[dict(path=r['path'],sha256=r['sha256'],current_equal=sha(ROOT/r['path'])==r['sha256']) for r in ca['evidence']]
result['source_bindings']={str(p.relative_to(ROOT)):sha(p) for p in [W/'sources/coremath_1_1.json',W/'sources/coremath_1_1_source.png',W/'sources/coremath_1_1.verification.json',W/'evidence/coremath_1_1_source_verification.md',ROOT/source['pdf']]}
result['canonical_hashes']={str(p.relative_to(ROOT)):sha(p) for p in [W/a/'coremath_1_1.json' for a in ['sources','materials','blueprints','manuscripts']]}
result['all_private_card_keys_absent_student']={typ:all(norm(c['teacher']) not in words[typ] and not any(norm(c['teacher']) in t for _,t in streams[typ]) for c in M['items']) for typ in ['StudentMaterials','AssessmentMaterials','FinalExplanation']}
result['student_summary_blank_count']=sum(1 for r in trees['StudentSummaryTable'].findall('.//w:tbl/w:tr',NS)[1:] for c in r.findall('w:tc',NS)[1:] if not ''.join(t.text or '' for t in c.findall('.//w:t',NS)).strip())
result['final_answer_placeholders']=answer_rows;result['media']={};result['full_attribution']={}
for typ in TYPES:
 with zipfile.ZipFile(OUT/(D['prefix']+'_'+typ+'.docx')) as z:
  result['media'][typ]=[p for p in z.namelist() if p.startswith(('word/media/','word/embeddings/'))];xml=' '.join(z.read(p).decode() for p in z.namelist() if p.startswith('word/') and p.endswith('.xml'))
 result['full_attribution'][typ]={'Word':all(s in xml for s in ['SeaVuria','ARES','ChatGPT/Codex','OpenAI','BY-NC','4.0']),'PDF':all(any(s in stream for _,stream in streams[typ]) for s in ['SeaVuria','ARES','ChatGPT/Codex','OpenAI','BY-NC','4.0'])}
result['old_disclosure_absent_rubric']=all('4portions' not in r['proficient'] for r in D['assessment']['rubric']);result['neutral_descriptor_present_both_final']=all(r['word_pass'] and r['pdf_pass'] for r in rows if r['field']=='assessment.rubric4.proficient')
result['structured_export_sha256']=sha(OUT/(D['prefix']+'_data.json'));result['export_final_equal_canonical']=export['FINAL_EXPLANATION']==D['assessment'];result['resource_policy_sha256']=sha(W/'resource_policy.json')
Path(__file__).with_suffix('.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['checks','artifact_hashes','source_bindings','canonical_hashes','full_attribution','CA_evidence']},indent=2));print('FAILURES',json.dumps([r for r in rows if not r['word_pass'] or not r['pdf_pass']]))
