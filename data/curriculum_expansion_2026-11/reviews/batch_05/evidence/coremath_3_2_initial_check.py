"""Read-only draft binding and independent probability-model checks."""
from pathlib import Path
import json,hashlib,zipfile,re,xml.etree.ElementTree as ET,itertools
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[5];B=ROOT/'data/curriculum_expansion_2026-11';E=Path(__file__).resolve().parent
M=json.loads((B/'materials/coremath_3_2.json').read_text());N=json.loads((B/'manuscripts/coremath_3_2.json').read_text());S=json.loads((B/'sources/coremath_3_2.json').read_text());W={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'};D=B/'outputs/v2/Core_Mathematics/SS3.2_Probability_I';T={};X={};XML={};checks=[]
def ck(label,value):checks.append({'check':label,'pass':bool(value)})
norm=lambda s:re.sub(r'\s+','',s)
for p in D.glob('*.docx'):
 k=p.stem.removeprefix(N['prefix']+'_')
 with zipfile.ZipFile(p) as z:
  x=ET.fromstring(z.read('word/document.xml'));X[k]=x;T[k]='\n'.join(''.join(t.text or '' for t in q.findall('.//w:t',W)) for q in x.findall('.//w:p',W));XML[k]=' '.join(z.read(n).decode() for n in z.namelist() if n.startswith('word/') and n.endswith('.xml'))
for c in M['items']:
 for key in ['student','teacher']:ck(c['id']+'key'+key,norm(c[key]) in norm(T['MaterialsTeacherKey']))
 ck(c['id']+'studentpropagation',norm(c['student']) in norm(T['AssessmentMaterials' if c['id']=='PI12' else 'StudentMaterials']))
for l in N['lessons']:
 for key in ['title','purpose','knowledge','safety','reflection']:ck(f"L{l['number']}guide{key}",norm(l[key]) in norm(T['CompactTeacherGuide']))
 for i,phase in enumerate(l['phases']):
  for j,s in enumerate(phase):ck(f"L{l['number']}phase{i+1}cell{j+1}",norm(s) in norm(T['CompactTeacherGuide']))
 ck(f"L{l['number']}40min",sum(l['minutes'])==40)
for outcome in S['outcomes']:ck('guide source outcome'+outcome['id'],norm(outcome['text']) in norm(T['CompactTeacherGuide']))
ck('12sourceallocatedlessons',S['official_lesson_allocation']==len(N['lessons'])==12)
ck('PI12absentteaching','PI12' not in T['StudentMaterials']);ck('PI12presentassessment','PI12' in T['AssessmentMaterials'])
ck('assessmentonlyPI12',not any(re.search(r'\bPI'+str(i)+r'\b',T['AssessmentMaterials']) for i in range(1,12)))
ck('noteachersolutionsassessment',all(norm(c['teacher']) not in norm(T['AssessmentMaterials']) for c in M['items']))
ck('finaldatasetabsentguide',norm(M['items'][-1]['student']) not in norm(T['CompactTeacherGuide']))
ck('finalanswerabsentteaching',norm(M['items'][-1]['teacher']) not in norm(T['StudentMaterials']))
rows=X['StudentSummaryTable'].findall('.//w:tr',W);ck('summary12rows',len(rows)==13)
for i,r in enumerate(rows[1:],1):
 cs=r.findall('w:tc',W);ck(f'summary{i}threeblank',len(cs)==4 and all(not ''.join(t.text or '' for t in c.findall('.//w:t',W)).strip() for c in cs[1:]))
for k,s in XML.items():
 for word in ['SeaVuria','ARES','ChatGPT/Codex','OpenAI','BY-NC','4.0']:ck(k+'attribution'+word,word in s)

# Enumerate event membership and sum actual model weights; do not evaluate
# registered expression strings. All selection predicates come from task wording.
die={i:F(1,6) for i in range(1,7)};coin={'H':F(1,2),'T':F(1,2)};bag={'R':F(3,5),'B':F(2,5)};spin={'R':F(2,3),'B':F(1,3)}
def cross(a,b):return {(x,y):p*q for x,p in a.items() for y,q in b.items()}
def prob(space,predicate):return sum((p for event,p in space.items() if predicate(event)),F(0))
cd=cross(coin,die);cc=cross(coin,coin);bb=cross(bag,bag);final=cross(coin,spin)
even=lambda x:x%2==0;prime=lambda x:x in {2,3,5};greater=lambda x:x>3
spaceA=prob(cd,lambda e:e[0]=='H' and even(e[1]));spaceB=prob(cd,lambda e:e[0]=='T' or e[1]==6)
coinjoint=prob(cc,lambda e:e[0]=='H' and e[1]=='H');diejoint=prob(die,lambda i:even(i) and greater(i))
# No replacement: distinguish physical tokens to enumerate20equiprobable
# ordered pairs, then aggregate colours; this does not assume independence.
tokens=['R1','R2','R3','B1','B2'];norep={e:F(1,20) for e in itertools.permutations(tokens,2)};nrRR=prob(norep,lambda e:e[0][0]=='R' and e[1][0]=='R')
finalH=prob(final,lambda e:e[0]=='H');finalR=prob(final,lambda e:e[1]=='R');finalHR=prob(final,lambda e:e==('H','R'));finalHB=prob(final,lambda e:e==('H','B'));finalunion=prob(final,lambda e:e[0]=='H' or e[1]=='R');finalexactly=prob(final,lambda e:(e[0]=='H') != (e[1]=='R'))
computed=[prob(die,even),spaceA,spaceB,prob(die,lambda i:i in {1,6}),prob(die,lambda i:even(i) or prime(i)),diejoint,coinjoint,bb[('R','R')],bb[('R','B')],prob(bb,lambda e:e.count('R')==1),nrRR,prob(cc,lambda e:e.count('H')==1),prob(cc,lambda e:'H' in e),prob(bb,lambda e:'R' in e),F(2,6),F(18,30),prob(die,lambda i:even(i) or i in {1,3}),finalHR,finalHB,finalunion,finalexactly]
ck('21registrylength',len(computed)==len(M['calculations'])==21)
for c,value in zip(M['calculations'],computed):ck('independentregistry'+c['id'],abs(float(value)-c['expected'])<1e-10)
ck('coin12pairs',len(cd)==12 and set(cd.values())=={F(1,12)})
ck('PI5overlap',prob(die,lambda i:even(i) and prime(i))==F(1,6))
ck('PI6coinindependent',coinjoint==F(1,4));ck('PI6diedependent',diejoint!=prob(die,even)*prob(die,greater))
ck('replacementstageindependent',bb[('R','R')]==bag['R']**2);ck('noreplacementstagedependent',nrRR!=F(3,5)**2)
for name,space in [('coin',cc),('bag',bb),('final',final)]:ck(name+'terminaltotal1',sum(space.values())==1)
ck('finalunion5over6',finalunion==F(5,6));ck('finalexactlyhalf',finalexactly==F(1,2));ck('finaloverlaplaw',finalunion==finalH+finalR-finalHR)
ck('finalEFindependencefails',prob(die,lambda i:even(i) and i in {1,3})==0 and prob(die,even)*prob(die,lambda i:i in {1,3})==F(1,6))
ck('zeroprobexception',F(0)==F(0)*F(1,2))
ck('finalvalidinvaliddenominator',F(18,30)==F(3,5) and 30+2==32)
res={'passed':sum(x['pass'] for x in checks),'total':len(checks),'failed':[x for x in checks if not x['pass']],'checks':checks,'independent_models':{'coin_die':{str(k):str(v) for k,v in cd.items()},'two_coins':{str(k):str(v) for k,v in cc.items()},'replacement_bag':{str(k):str(v) for k,v in bb.items()},'noreplacement_colour_paths':{str(c):str(prob(norep,lambda e:tuple(t[0] for t in e)==c)) for c in itertools.product('RB',repeat=2)},'final_coin_spinner':{str(k):str(v) for k,v in final.items()},'final_union':str(finalunion),'final_exactlyone':str(finalexactly)},'note':'Event sets/weighted products and without-replacement physical-token enumeration are independent of the author expression strings. Actual classroom frequencies/game results have no fixed numeric key.'}
(E/'coremath_3_2_initial_checks.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:res[k] for k in ['passed','total','failed','independent_models']},indent=2))
