from pathlib import Path
from io import BytesIO
import hashlib,json,zipfile,sys,subprocess,re
from lxml import etree
R=Path.cwd();B=R/'data/curriculum_expansion_2026-11';O=B/'reviews/batch_07/evidence/essmath_1_3_rubric_correction_layout';chk=json.loads((O/'check.json').read_text());d=json.loads((B/'manuscripts/essmath_1_3.json').read_text());old=B/'Batch_03_Reviewed.zip';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();bh=lambda b:hashlib.sha256(b).hexdigest();ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'};pre=d['prefix'];out=next((B/'outputs/v2').rglob(pre+'_data.json')).parent
pairs=[('lost-zero explanation','lost-root explanation'),('valid zero-root explanation','valid lost-root explanation')]
def updated(t):
 for a,b in pairs:t=t.replace(a,b)
 return t
bridge={};narrow={};oldsha=sha(old)
def diff(a,b,p=''):
 if type(a)!=type(b):return[(p,a,b)]
 if isinstance(a,dict):return sum([diff(a.get(k),b.get(k),p+'/'+k)for k in sorted(set(a)|set(b))],[])
 if isinstance(a,list):
  if len(a)!=len(b):return[(p,a,b)]
  return sum([diff(x,y,p+'/'+str(i))for i,(x,y)in enumerate(zip(a,b))],[])
 return[]if a==b else[(p,a,b)]
with zipfile.ZipFile(old)as z:
 for typ in chk['artifact_hashes']:
  member=next(n for n in z.namelist()if n.endswith('_'+typ+'.docx'));cur=out/(pre+'_'+typ+'.docx');raw=z.read(member)
  def texts(b):
   with zipfile.ZipFile(BytesIO(b))as w:
    tree=etree.fromstring(w.read('word/document.xml'));return'\n'.join(t.text or''for t in tree.findall('.//w:t',ns))
  a,b=texts(raw),texts(cur.read_bytes());bridge[typ]={'old_word_sha256':bh(raw),'current_word_sha256':sha(cur),'body_text_identical':a==b,'body_text_only_rubric_replacements':updated(a)==b}
  # Old/current PDF text bridge is whitespace-normalised; preserve actual extracts.
  pm=next(n for n in z.namelist()if n.endswith('_'+typ+'.pdf'));tmp=O/('original_'+typ+'.pdf');tmp.write_bytes(z.read(pm));ap=subprocess.check_output(['pdftotext',str(tmp),'-'],text=True);bp=subprocess.check_output(['pdftotext',str(B/'outputs/PDF'/(pre+'_'+typ+'.pdf')),'-'],text=True)
  norm=lambda t:re.sub(r'\s+','',t)
  bridge[typ].update(old_pdf_sha256=bh(z.read(pm)),current_pdf_sha256=chk['artifact_hashes'][typ]['pdf_sha256'],pdf_text_identical=norm(ap)==norm(bp),pdf_text_only_rubric_replacements=norm(updated(ap))==norm(bp));(O/('original_'+typ+'.txt')).write_text(ap)
  if typ in ['FinalExplanation','FinalExplanation_TeacherKey']:
   narrow[typ]={'new_excellent_present':'lost-root explanation is precise.'in b,'new_proficient_present':'valid lost-root explanation.'in b,'old_excellent_absent':'lost-zero explanation'not in b,'old_proficient_absent':'zero-root explanation'not in b,'pdf_old_cues_absent':all(norm(t)not in norm(bp)for t in ['lost-zero explanation','zero-root explanation'])}
 expmember=next(n for n in z.namelist()if n.endswith('_data.json'));original_export=json.loads(z.read(expmember));current_export=json.loads((out/(pre+'_data.json')).read_text());expdiff=diff(original_export,current_export);narrow['export_diff']=expdiff
r={'original_archive_sha256':oldsha,'original_archive_unchanged':sha(old)==oldsha=='c17859c16fa2a960b6a5d798d2784cbca1fc4ef19f1760580897909afde4ad05','bridge':bridge,'rubric_checks':narrow,'export_schema':current_export.get('schemaVersion',current_export.get('SCHEMA_VERSION'))};(O/'old_current_bridge.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
