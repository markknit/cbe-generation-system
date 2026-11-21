"""Independent rational polynomial/arithmetic/geometry and complete task review evidence."""
from pathlib import Path
from fractions import Fraction as F
import ast,operator,math,json
E=Path(__file__).parent;B=E.parents[2];M=json.loads((B/'materials/coremath_1_3.json').read_text());L=json.loads((B/'manuscripts/coremath_1_3.json').read_text());P=json.loads((B/'blueprints/coremath_1_3.json').read_text());S=json.loads((B/'sources/coremath_1_3.json').read_text())
vals=dict(zip(['squarePlus','squareSum','squareMinus','stripArea','difference','differenceProduct','numeric102','numeric98','numeric51x49','numeric25','monicRoot2','monicRoot3','zeroRoot','zeroRoot3','nonmonicRootHalf','nonmonicRootNeg3','rearrange3','rearrangeNeg5','repeated','rectangle','array','border','finalNumeric','finalRootNegHalf','finalRoot3','finalArea28','finalArea40','finalNegativeRoot'],[36,36,9,9,21,21,10404,9604,2499,F(25,4),0,0,0,0,0,0,0,0,0,36,20,30,9801,0,0,28,40,0]))
def calc(n):
 if isinstance(n,ast.Expression):return calc(n.body)
 if isinstance(n,ast.Constant) and isinstance(n.value,(int,float)):return n.value
 if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return -calc(n.operand)
 if isinstance(n,ast.BinOp):return {ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.Pow:operator.pow}[type(n.op)](calc(n.left),calc(n.right))
 raise ValueError(ast.dump(n))
reg=[]
for r in M['calculations']:
 v=vals[r['id']];a=calc(ast.parse(r['expression'],mode='eval'));reg.append({'id':r['id'],'independent':str(v),'expression_value':a,'author_expected':r['expected'],'pass':math.isclose(a,float(v),abs_tol=1e-12) and math.isclose(r['expected'],float(v),abs_tol=1e-12)})
def mul(a,b):
 c=[F(0)]*(len(a)+len(b)-1)
 for i,u in enumerate(a):
  for j,v in enumerate(b):c[i+j]+=F(u)*F(v)
 return c
def ev(a,x):return sum(F(v)*x**i for i,v in enumerate(a))
# Coefficients listed constant-first. Each independently proposed linear factor is fully expanded.
cases=[('CQE5a',[0,9,6],3,[[0,1],[3,2]]),('CQE5b',[0,-5,1],1,[[0,1],[-5,1]]),('CQE5c',[0,8,-2],-2,[[0,1],[-4,1]]),('CQE6a',[6,5,1],1,[[2,1],[3,1]]),('CQE6b',[-6,-1,1],1,[[-3,1],[2,1]]),('CQE6c',[-9,0,1],1,[[-3,1],[3,1]]),('CQE6d_CQE13a',[9,6,1],1,[[3,1],[3,1]]),('CQE7a_CQE10a',[3,7,2],1,[[1,2],[3,1]]),('CQE7b',[-2,-1,6],1,[[-2,3],[1,2]]),('CQE7c',[-8,0,2],2,[[-2,1],[2,1]]),('CQE8roots',[-6,1,1],1,[[-2,1],[3,1]]),('CQE8repeated',[9,-6,1],1,[[-3,1],[-3,1]]),('CQE8rectangle_CQE10c',[-15,2,1],1,[[5,1],[-3,1]]),('CQE9a',[6,-5,1],1,[[-2,1],[-3,1]]),('CQE9b',[0,-6,2],2,[[0,1],[-3,1]]),('CQE10b',[-25,0,1],1,[[-5,1],[5,1]]),('CQE10d',[4,4,1],1,[[2,1],[2,1]]),('CQE11rectangle',[-36,5,1],1,[[9,1],[-4,1]]),('CQE11array',[-20,1,1],1,[[5,1],[-4,1]]),('CQE12square49',[-49,0,1],1,[[-7,1],[7,1]]),('CQE12square64',[-64,0,1],1,[[-8,1],[8,1]]),('CQE13b',[0,-4,1],1,[[0,1],[-4,1]]),('I2factor',[-3,5,2],1,[[-1,2],[3,1]]),('I3form',[-10,-3,1],1,[[2,1],[-5,1]]),('I3solve',[-3,-5,2],1,[[1,2],[-3,1]]),('I4area28',[-28,3,1],1,[[7,1],[-4,1]]),('I4area40',[-40,3,1],1,[[8,1],[-5,1]])]
poly=[]
for name,target,k,factors in cases:
 out=[F(k)]
 for f in factors:out=mul(out,f)
 roots=sorted({-F(c)/F(b) for c,b in factors});poly.append({'case':name,'target_coefficients':target,'factors':factors,'scalar':k,'expanded':[str(v) for v in out],'distinct_roots':[str(v) for v in roots],'original_substitutions':[str(ev(target,v)) for v in roots],'pass':out==list(map(F,target)) and all(ev(target,v)==0 for v in roots)})
# Multivariate identities independently collected using exact coefficient dictionaries.
def pmul(a,b):
 out={}
 for (i,j),u in a.items():
  for (k,l),v in b.items():out[i+k,j+l]=out.get((i+k,j+l),0)+u*v
 return {k:v for k,v in out.items() if v}
plus={(1,0):1,(0,1):1};minus={(1,0):1,(0,1):-1}
geometry={'sum_square':pmul(plus,plus),'difference_square':pmul(minus,minus),'difference_squares':pmul(plus,minus)}
checks={'all28_registry_correct':len(reg)==28 and all(x['pass'] for x in reg),'all27_complete_factor_expansions_and_root_checks':len(poly)==27 and all(x['pass'] for x in poly),'sum_identity':geometry['sum_square']=={(2,0):1,(1,1):2,(0,2):1},'minus_identity':geometry['difference_square']=={(2,0):1,(1,1):-2,(0,2):1},'difference_identity':geometry['difference_squares']=={(2,0):1,(0,2):-1},'border_cancellation': [a-b for a,b in zip(mul([2,1],[5,1]),mul([0,1],[3,1]))]==[10,4,0],'border_solution_and_area':4*5+10==30 and 7*10-5*8==30,'area_numerical_checks':16+8+8+4==36 and 25-20+4==9 and 25-4==7*3==21,'zero_product_nonzero_rhs_not_valid':(2-2)*(2+3)==0 and (2-2)*(2+3)!=7,'all14cards_unique':[x['id'] for x in M['items']]==[f'CQE{i}' for i in range(1,15)],'all14lessons_40min':len(L['lessons'])==14 and all(sum(x['minutes'])==40 for x in L['lessons']),'L3_two_models_pacing':L['lessons'][2]['minutes']==[4,18,10,3,5],'final_4_8_8_8_10plus2':L['lessons'][-1]['minutes']==[4,8,8,8,12] and 'Allow10minutes for section4 and2minutes independent checking' in L['lessons'][-1]['phases'][-1][1],'blueprint_lesson_maps_consistent':all(l['number']==p['lesson'] and l['title']==p['title'] and l['materials']==p['materials'] and l['outcomes']==p['outcomes'] for l,p in zip(L['lessons'],P['lesson_map'])),'all8source_outcomes_have_routes':set().union(*(set(x['outcomes']) for x in L['lessons']))=={x['id'] for x in S['outcomes']},'final4criteria_4sections':len(L['assessment']['sections'])==len(L['assessment']['rubric'])==4,'source_metadata_exact':all(L['unit'][k]==S[k] for k in ['coreCompetencies','values','pcis']),'no_official_count':S['official_lesson_allocation'] is None}
solutions={
'CQE1':'2x²+3x-5,x²+4x,x²-1;leading2,1,1. Simplifiedx²-x²+3=3constant. Geometricx>0 vs all-realalgebra distinct.',
'CQE2':'a+b square split into a²,ab,ab,b²;sum a²+2ab+b². a4/b2 ->side6,total36=16+8+8+4cm². Positive lengths forarea,all-realidentity byexpansion. Fullydimensionedtext needs no externalfigure.',
'CQE3':'Two full strips ab each overlapb²,so leftover(a-b)²=a²-2ab+b². ForL remove onlyb²,partitionbottom a by(a-b),top-leftb by(a-b);rotate/append to make(a+b)by(a-b). a5b2 ->9and21cm². Differentregions;0<b<a geometry,all-realidentities separately.',
'CQE4':'102²=10404,98²=9604,51*49=2499,2.5²=25/4. Cross terms required;1+1square4vs1²+1²=2. Direct multiplicationcheck exact.',
'CQE5':'3x(2x+3),x(x-5),-2x(x-4). Full expansions recorded;factoring includesx0 unlike cancellingx inequation.',
'CQE6':'(x+2)(x+3),(x-3)(x+2),(x-3)(x+3),(x+3)². Sum/product coefficientsbothchecked;repeatedfactoronlyonedistinctroot later.',
'CQE7':'(2x+1)(x+3),(3x-2)(2x+1),2(x-2)(x+2). Middle splits6x+x and3x-4x. x²+1≥1forallrealx has no realzeros;failureoffactorsearchdoesnotmakethepolynomialmeaningless.',
'CQE8':'Roots2/-3 ->x²+x-6=0;repeated3->x²-6x+9=0. Monic fixesrepresentative;nonzeromultiples equivalentroots. Rectangle x²+2x-15=0withx>0;formationseparatefromsolve.',
'CQE9':'x²-5x+6 roots2,3;2x²-6x roots0,3. Dividingbyx without0losesroot. Product7cannotusefactorzero;x2product0not7. No assertiontherearenosolutions.',
'CQE10':'2x²+7x+3 roots-1/2,-3;x²25 roots±5;x²+2x15 roots-5,3;x²+4x+4 root-2repeated(one distinct). Factorand originalsubstitution checksabove.',
'CQE11':'Rectangle(x+9)(x-4)=0 ->roots-9,4,physical4mby9m=36m². Array(x+5)(x-4)=0 ->roots-5,4;4rows5columns20dots. Negative roots solvealgebra but notpositivelength/countdomains.',
'CQE12':'Squarex²49 ->±7physical7cm;changed64 ->±8physical8cm. Border(x+2)(x+5)-x(x+3)=4x+10;30givesx5cm,outer7x10=70inner5x8=40difference30cm². Linearaftercancellation,notautomaticallyquadratic. Suppliedfictionalpapercomparison+askedchangedparameter substantivelyexplore;externalresearchonlyifobserved.',
'CQE13':'A(x+3)²not(x+3)(x-3);B x(x-4) roots0,4;C negative-9 giveslength-4infeasiblevs4by9. Explicitexpansion/roots/contextchecks matchd/f/g.',
'I1':'x(x+4)=x²+4x;squarep+q partitionp²,pq,pq,q². Positivegeometry/all-realexpansionconditionscorrect.',
'I2':'99²=(100-1)²=9801;(2x-1)(x+3)=2x²+5x-3,allcoefficientsnotconstantonly.',
'I3':'Roots-2/5 ->(x+2)(x-5)=0 ->x²-3x-10=0;separate2x²-5x-3=(2x+1)(x-3) roots-1/2,3,originalsubstitution0both.',
'I4':'x²+3x-28=(x+7)(x-4) ->physical4cmby7cm,negative-7infeasible. Area40->x²+3x-40=(x+8)(x-5) ->physical5by8cm,negative-8infeasible. Onlyconstantchanges,sideoffsetfixed;units/exactassumptions preserved.'}
r={'registry':reg,'polynomial_factor_and_roots':poly,'geometry_polynomial_coefficients':{k:{str(a):v for a,v in p.items()} for k,p in geometry.items()},'checks':checks,'pass':sum(checks.values()),'total':len(checks),'independent_all_task_solutions':solutions,'limits':'Reviewer exact polynomial/area arithmetic only. No author tests,build,render,classroom device/drawing/peerresearchperformance or productcertification inferred.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'registry':sum(x['pass'] for x in reg),'factor_cases':sum(x['pass'] for x in poly),'checks_pass':r['pass'],'checks_total':r['total'],'failures':[k for k,v in checks.items() if not v]},indent=2));assert all(checks.values())
