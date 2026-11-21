from pathlib import Path
import json,hashlib,sys,copy,zipfile,re,difflib,xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[5];B=ROOT/'data/curriculum_expansion_2026-11';V=Path(__file__).parent;sys.path.insert(0,str(ROOT/'scripts'))
from curriculum_pipeline import content_fingerprint
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();norm=lambda s:re.sub(r'\s+',' ',s).strip()
old=json.loads((V/'gensci_1_7_science_pass1_word_check.json').read_text());baseline=V/'gensci_1_7_essential_source_review_pass_1/manuscripts_snapshot.json'
assert sha(baseline)==old['canonical_hashes']['manuscripts/gensci_1_7.json']
a=json.loads(baseline.read_text());b=json.loads((B/'manuscripts/gensci_1_7.json').read_text());changes=[]
def diff(a,b,path=''):
 if type(a)!=type(b):changes.append({'path':path,'old':a,'current':b});return
 if isinstance(a,dict):
  assert a.keys()==b.keys()
  for k in a:diff(a[k],b[k],path+'/'+k)
 elif isinstance(a,list):
  assert len(a)==len(b)
  for i,(x,y) in enumerate(zip(a,b)):diff(x,y,path+'/'+str(i))
 elif a!=b:changes.append({'path':path,'old':a,'current':b})
diff(a,b)
assert all(x['path']=='/lessons/11/story' or x['path'].startswith('/lessons/11/phases/') or x['path'].startswith('/lessons/11/minutes/') for x in changes)
reversed_current=copy.deepcopy(b)
for k in ['minutes','story','phases']:reversed_current['lessons'][11][k]=a['lessons'][11][k]
assert reversed_current==a
unchanged={k:sha(B/k)==h for k,h in old['canonical_hashes'].items() if k!='manuscripts/gensci_1_7.json'}
assert all(unchanged.values());assert b['assessment']==a['assessment'];assert b['lessons'][11]['minutes']==[5,10,10,10,5]
N={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'};O=B/'outputs/v2/General_Science/SS1.7_Microorganisms';bridge={}
for t,h in old['draft_word_hashes'].items():
 p=O/(b['prefix']+'_'+t+'.docx')
 with zipfile.ZipFile(p) as z:r=E.fromstring(z.read('word/document.xml'))
 current='\n'.join(''.join(q.text or '' for q in para.findall('.//w:t',N)) for para in r.findall('.//w:p',N));prior=(V/f'gensci_1_7_{t}_science_pass1_review_text.txt').read_text()
 same=current==prior;entry={'old_sha256':h,'current_sha256':sha(p),'binary_same':sha(p)==h,'body_identical':same}
 if t=='CompactTeacherGuide':
  marker='Lesson 12: '+b['lessons'][11]['title'];assert marker in current and marker in prior
  entry['prefix_before_lesson12_identical']=current.split(marker)[0]==prior.split(marker)[0];assert entry['prefix_before_lesson12_identical']
  entry['body_diff']=list(difflib.unified_diff(prior.splitlines(),current.splitlines(),fromfile='pass1',tofile='pass2',lineterm=''))
 else:assert same
 bridge[t]=entry
result={'old_fingerprint':old['content_fingerprint'],'current_fingerprint':content_fingerprint(B,'gensci_1_7'),'baseline_snapshot_sha256':sha(baseline),'baseline_matches_own_pass1_binding':True,'only_approved_lesson12_fields_changed':True,'changed_scalar_count':len(changes),'changes':changes,'other_canonical_unchanged':unchanged,'final_assessment_unchanged':True,'reverse_field_substitution_recovers_pass1_structure':True,'minutes':[5,10,10,10,5],'actual_five_word_bridge':bridge}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['changes','actual_five_word_bridge']},indent=2));print('word_bridge',{k:{f:v for f,v in row.items() if f!='body_diff'} for k,row in bridge.items()})
