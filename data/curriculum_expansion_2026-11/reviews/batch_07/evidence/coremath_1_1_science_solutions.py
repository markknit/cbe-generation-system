"""Independent exact arithmetic, table rounding, classification and task/mapping review evidence."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
import ast,operator,math,json
E=Path(__file__).parent;B=E.parents[2];M=json.loads((B/'materials/coremath_1_1.json').read_text());L=json.loads((B/'manuscripts/coremath_1_1.json').read_text());P=json.loads((B/'blueprints/coremath_1_1.json').read_text());S=json.loads((B/'sources/coremath_1_1.json').read_text())
values={'R4':F(1,4),'Rneg5':F(-1,5),'RtwoThirds':F(3,2),'Rroot2':1/math.sqrt(2),'Rmixed':F(2,3),'RnegMixed':F(-2,5),'Rdecimal':F(4),'RnegDecimal':F(-5,2),'R32':F(5,16),'R36':F(5,18),'Rscaled32':F(1,32),'RscaledPoint32':F(25,8),'Rscaled036':F(250,9),'portion':F(6),'strip':F(8),'division':F(-21,10),'FinalMixed':F(-4,7),'FinalFraction':F(5,3),'FinalRoot':1/math.sqrt(5),'FinalTable':F(5,21),'FinalScale':F(50,21),'FinalPortion':F(4)}
def calculate(n):
 if isinstance(n,ast.Expression):return calculate(n.body)
 if isinstance(n,ast.Constant) and isinstance(n.value,(int,float)):return n.value
 if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return -calculate(n.operand)
 if isinstance(n,ast.BinOp):return {ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.Pow:operator.pow}[type(n.op)](calculate(n.left),calculate(n.right))
 if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='sqrt' and len(n.args)==1:return math.sqrt(calculate(n.args[0]))
 raise ValueError(ast.dump(n))
registry=[]
for row in M['calculations']:
 v=values[row['id']];a=calculate(ast.parse(row['expression'],mode='eval'));registry.append({'id':row['id'],'independent':str(v),'expression_value':a,'author_expected':row['expected'],'pass':math.isclose(a,float(v),abs_tol=1e-12,rel_tol=1e-12) and math.isclose(row['expected'],float(v),abs_tol=1e-12,rel_tol=1e-12)})
def four_sf(s):
 with localcontext() as ctx:
  ctx.prec=50;v=D(1)/D(s);return str(v.quantize(D(1).scaleb(v.adjusted()-3)))
tabledata=[('3.0','0.3333'),('3.1','0.3226'),('3.2','0.3125'),('3.3','0.3030'),('3.4','0.2941'),('3.5','0.2857'),('3.6','0.2778'),('3.7','0.2703'),('3.8','0.2632'),('3.9','0.2564'),('4.0','0.2500'),('4.2','0.2381'),('4.8','0.2083')]
tables=[{'input':s,'listed':t,'independent_four_sf':four_sf(s),'pass':four_sf(s)==t} for s,t in tabledata]
def classify(n):
 divs=[d for d in range(1,n+1) if n%d==0] if n>0 else []
 return {'n':n,'parity':'even' if n%2==0 else 'odd','class':'prime' if n>1 and len(divs)==2 else 'composite' if n>1 else 'neither','positive_divisors':divs if n>0 else 'all positive integers divide0;not prime/composite'}
classification=[classify(n) for n in [0,1,2,3,4,9,11,15,17,21,25]]
checks={
'all22registry_independently_correct':len(registry)==22 and all(r['pass'] for r in registry),
'all13table_entries_four_sf_correct':all(t['pass'] for t in tables),
'cards10distinct':[c['id'] for c in M['items']]==[f'CRN{i}' for i in range(1,11)],
'lessons10x40':len(L['lessons'])==10 and all(sum(l['minutes'])==40 for l in L['lessons']),
'final_timing_4_8_8_10_7plus3':L['lessons'][-1]['minutes']==[4,8,8,10,10] and 'Allow7minutes for section4 and3minutes independent checking.' in L['lessons'][-1]['phases'][-1][1],
'lesson_blueprint_maps_match':all(l['number']==p['lesson'] and l['outcomes']==p['outcomes'] and l['materials']==p['materials'] and l['title']==p['title'] for l,p in zip(L['lessons'],P['lesson_map'])),
'all6source_outcomes_mapped':set().union(*(set(l['outcomes']) for l in L['lessons']))=={o['id'] for o in S['outcomes']},
'four_final_sections_and_criteria':len(L['assessment']['sections'])==len(L['assessment']['rubric'])==4,
'four_rubric_links_to_asked_skills':all(r['criterion']==i and r['tasks']==[f'I{i}'] for i,r in enumerate(P['rubric_links'],1)),
'unit_exact_source_values_competencies_pci':all(S[k]==L['unit'][k] for k in ['values','coreCompetencies','pcis']),
'no_official_allocation':S['official_lesson_allocation'] is None,
'negative_mixed_conversion':-F(2)-F(1,2)==F(-5,2) and 1/(-F(2)-F(1,2))==F(-2,5),
'negative_final_mixed_conversion':-F(1)-F(3,4)==F(-7,4) and 1/(-F(1)-F(3,4))==F(-4,7),
'context_reverse_checks':6*F(3,4)==F(9,2) and 8*F(3,10)==F(12,5) and F(-21,10)*F(2,7)==F(-3,5) and 4*F(7,8)==F(7,2),
'zero_even_neither':classify(0)['parity']=='even' and classify(0)['class']=='neither',
'one_odd_neither':classify(1)['parity']=='odd' and classify(1)['class']=='neither',
}
solutions={
'CRN1':'Even0,2,4;odd1,3,9,11,15,21. Prime2,3,11;composite4,9,15,21;neither0,1.9pairs1x9/3x3;15pairs1x15/3x5.9disproves odd=>prime.0=2x0. Every whole n=n/1,never irrational.',
'CRN2':'Rational -5/1,0/1,2/3,1/8,7/9,4/1,22/7;irrational exact sqrt2/pi. Integers-5,0,4;wholes0,4. Repeating7decimal=7/9 by10x-x=7. Finite sqrt display is an approximation;pi is not22/7.',
'CRN3':'1/4,-1/5,3/2,1/sqrt2;nonzero products1.0r is always0,never1. Additive opposite4 is-4;product inverse is1/4. Extra exit:-5 reciprocal-1/5/opposite+5.',
'CRN4':'3/2->2/3;-5/2->-2/5;1/4->4;-2/5->-5/2;1/9->9. All products1;wrong proposal(-5/2)*(-2/3)=5/3,not1. Preserve entire mixed-number sign.',
'CRN5':'Table all10 rows independently rounded above.1/3.2=5/16=.3125 exact;1/3.6=5/18 repeating approximately.2778.1/32=1/32=.03125;1/.32=25/8=3.125;1/.036=250/9 approximately27.78. Scaling input k multiplies inverse by1/k. No index-law prerequisite.',
'CRN6':'Exact5/18,-2/5,3/2,1/sqrt2;irrational/repeating4sf .2778/.7071. Actual device entry/display depends model,not supplied paper simulation. Device1/0error is not number/inverse. No actual action may be fabricated.',
'CRN7':'(9/2)/(3/4)=6portions;(12/5)/(3/10)=8pieces;(-3/5)/(2/7)=-21/10. Reverse checks above. Exact assumptions/nonzero divisors/no spills/no cut loss;no physical actions or upward rounding arbitrary portion counts.',
'CRN8':'Example classification0even but division by0 impossible;4.5L/.75L=6complete portions with product4.5L. Link evidence to planning decision and preserve assumptions/domain. Record real peer question/revision if shared;otherwise NOT OBSERVED. Varied correct messages valid.',
'CRN9':'A9counterexample;Bexactsqrt2/pi irrational despite display;Cwhole-negative mixed->-5/2->-2/5;D3.2inverse.3125/32inverse.03125;E0r=0cannot1. Learner generated evidence question has no single fixed answer.',
'I1':'0even/neither;1odd/neither;2even/prime;9odd/composite;17odd/prime;25odd/composite. Rational-3/1,1/5,5/1,22/7;irrational sqrt5/pi. All wholesn/1;finite sqrt5 approximation not definition.',
'I2':'-1.75=-7/4 inverse-4/7;3/5 inverse5/3;products1.0noinverse;exact1/sqrt5. Additive opposite sums0;reciprocal product1.',
'I3':'1/4.2=5/21 approximately.2381;1/.42=50/21 approximately2.381;1/sqrt5 approximately.4472 fourSF. Device record actual or NOT OBSERVED,pending;display finiteapprox. Precise original/table inputs do not make roundedentriesexact.',
'I4':'(7/2)/(7/8)=4complete portions;4*(7/8)L=3.5L. Written advice under no-spill/exact assumptions useful for plan;0portion no inverse. Written independent message does not prove peer delivery;F8actualsharing separate.'}
r={'registry':registry,'table_rounding':tables,'whole_classification':classification,'checks':checks,'pass':sum(checks.values()),'total':len(checks),'independent_task_solutions':solutions,'limits':'Exact rational arithmetic independent of author expected values;registry expressions parsed only after independent values assigned. Known irrational square roots/pi accepted school examples,no advanced proof required. No devices/peer actions performed.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'pass':r['pass'],'total':r['total'],'registry_pass':sum(x['pass'] for x in registry),'table_pass':sum(x['pass'] for x in tables),'failed':[k for k,v in checks.items() if not v]},indent=2));assert all(checks.values())
