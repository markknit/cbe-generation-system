"""Small record-writing helpers. Lesson content is explicitly authored, not model API generated."""
import json
from pathlib import Path
BASE=Path(__file__).resolve().parents[2]/'data/codex_pilot_2026-11'
def save(area,name,data):
 (BASE/area/(name+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2))
def item(i,title,student,teacher):return dict(id=i,title=title,student=student,teacher=teacher)
def check(i,expression,expected,tol=1e-8):return dict(id=i,expression=expression,expected=expected,absolute_tolerance=tol)
def lesson(n,title,outcomes,materials,purpose,knowledge,skills,inquiry,overview,phases,summary,safety='Use paper tasks and calculators; keep walkways clear.',minutes=None,independent=False):
 strategies=['Individual prediction, then paired comparison: keep the initial claim visible.','Evidence-first group work: record working or observations before comparing explanations.','Claim–evidence–reasoning: connect the result to a rule and state its limits.','Question sorting: mark an inquiry answered only when evidence supports it.','Revise a shared model: preserve the earlier version and annotate what changed.']
 if independent:
  strategies=['Read and interpret the task individually; clarify wording without discussing methods or answers.','Independent written working: no peer comparison, group solution or teacher exemplars before original work is collected.','Private reflection after collection; keep original responses unchanged and defer worked feedback.','Submit an individual question for later feedback without discussing assessment solutions.','Write an individual transfer statement using the assessed model; no shared revision during assessment.']
 attitudes='Work independently, record reasoning honestly, and check the stated assumptions.' if independent else 'Listen to alternative reasoning, record evidence honestly, and revise a claim when evidence warrants it.'
 return dict(number=n,title=title,outcomes=outcomes,materials=materials,purpose=purpose,knowledge=knowledge,skills=skills,attitudes=attitudes,inquiry=inquiry,story=overview,safety=safety,overview=overview,minutes=minutes or [4,16,10,4,6],phases=[[p[0],p[1],strategies[i],p[2]] for i,p in enumerate(phases)],summary=dict(zip(['observed','learned','explained'],summary)),reflection='Which learner work shows the intended outcome? Record one unresolved misconception and the adjustment needed before the next lesson.')
def rubric(criteria):
 return [dict(criterion=c,excellent='Gives a correct, complete explanation and independently checks the result or its limits.',proficient='Meets the stated criterion with correct reasoning and an appropriate conclusion.',developing='Shows relevant understanding but needs support to correct a significant error or omission.',belowExpectations='Does not yet demonstrate the criterion; needs guided work with a concrete example.') for c in criteria]
def publish(name,m,items,checks,reason,assessment_map):
 source=json.loads((BASE/'sources'/f'{name}.json').read_text())
 for k in ('coreCompetencies','values','pcis'):
  m['unit'][k]=source[k]
 # Improve prose spacing without altering compact card identifiers such as E1.
 import re
 def clean(x):
  if isinstance(x,str):
   # Preserve printed URLs, including percent-encoded digit/letter sequences.
   parts=re.split(r'(https?://[^\s]+)',x)
   for i in range(0,len(parts),2):
    t=re.sub(r'(?<=[a-z])(?=\d)|(?<=\d)(?=[A-Za-z])',' ',parts[i])
    t=re.sub(r'\b(KES|USD)(?=\d)',r'\1 ',t)
    parts[i]=re.sub(r'([,;:])(?=[A-Za-z0-9])',r'\1 ',t)
   return ''.join(parts)
  if isinstance(x,list):return [clean(v) for v in x]
  if isinstance(x,dict):return {k:clean(v) for k,v in x.items()}
  return x
 items=clean(items);m=clean(m)
 # Repeated decision results resolve from executable calculations at build time.
 tokens={
  'essmath_2_8':{'2137.50':'{{Q:.2f}}','5737.50':'{{newbudget:.2f}}','262.50':'{{remaining:.2f}}'},
  'coremath_2_5':{'58.1m²':'{{C8heptagon:.1f}}m²','77.3m²':'{{C8octagon:.1f}}m²','13200':'{{C11cost:.0f}}'},
 }.get(name,{})
 def template(x):
  if isinstance(x,str):
   for old,new in tokens.items():x=x.replace(old,new)
   return x
  if isinstance(x,list):return [template(v) for v in x]
  if isinstance(x,dict):return {k:template(v) for k,v in x.items()}
  return x
 items=template(items);m=template(m)
 save('materials',name,dict(items=items,calculations=checks))
 prerequisites={'essmath_2_8':['Four operations with money','Decimal and percentage equivalence'],'coremath_2_5':['Triangle area from base and perpendicular height','Sine and tangent for acute angles;degree-mode calculator','Scale and square units'],'gensci_2_4':['Observation versus explanation','Laboratory safety induction before live activity']}
 save('blueprints',name,dict(lesson_count=len(m['lessons']),lesson_minutes=40,allocation_status='Pilot authoring decision; no official count inferred',rationale=reason,prerequisites=prerequisites[name],teacher_confirmation_required=['Confirm classroom pacing and prerequisite knowledge;add support periods if needed.','Confirm materials,risk assessment and access adjustments;data interpretation is not hands-on skill.'],lesson_map=[dict(lesson=l['number'],title=l['title'],outcomes=l['outcomes'],materials=l['materials']) for l in m['lessons']],assessment_map=assessment_map,acceptance=['Every outcome has a teaching activity and observable assessment evidence.','All registered calculations pass; full reviewer still checks unregistered prose and practical feasibility.','No failed or incomplete review is treated as a clean review.']))
 save('manuscripts',name,m)
