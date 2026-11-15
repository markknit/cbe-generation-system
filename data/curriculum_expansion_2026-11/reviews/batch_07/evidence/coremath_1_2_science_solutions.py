"""Independent exact arithmetic, log/inverse tables, all task answers and review checks."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext,ROUND_HALF_UP
import ast,operator,math,json
E=Path(__file__).parent;B=E.parents[2];M=json.loads((B/'materials/coremath_1_2.json').read_text());L=json.loads((B/'manuscripts/coremath_1_2.json').read_text());P=json.loads((B/'blueprints/coremath_1_2.json').read_text());S=json.loads((B/'sources/coremath_1_2.json').read_text())
vals={'positiveProduct':32,'quotient':27,'nested':64,'powerProduct':36,'zero':1,'negative':F(1,8),'fractional':9,'negFraction':F(1,9),'fifth':4,'tower':256,'minusInside':4,'minusOutside':-4,'log70Arithmetic':D('1.8451'),'logPoint007Arithmetic':D('-2.1549'),'logPoint02Arithmetic':D('-1.6990'),'productLog':D('.7781'),'scaledProductLog':D('3.7781'),'divisionLog':D('.7781'),'signedDivisionLog':D('2.7781'),'powerLog':D('.9030'),'rootLog':D('.23855'),'combinedLog':D('3.0791'),'finalProductLog':D('1.5441'),'finalDivisionLog':D('.3979'),'finalPowerLog':D('.9542'),'finalRootLog':D('.3495')}
anti=[('.7781','5.999'),('.3010','2.000'),('.4771','3.000'),('.6990','5.000'),('.9030','7.998'),('.2386','1.732'),('.0791','1.200'),('.3979','2.500'),('.5441','3.500'),('.9542','8.999'),('.3495','2.236')]
def calc(n):
 if isinstance(n,ast.Expression):return calc(n.body)
 if isinstance(n,ast.Constant) and isinstance(n.value,(int,float)):return n.value
 if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return -calc(n.operand)
 if isinstance(n,ast.BinOp):return {ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.Pow:operator.pow}[type(n.op)](calc(n.left),calc(n.right))
 raise ValueError(ast.dump(n))
def sig(v,n):return v.quantize(D(1).scaleb(v.adjusted()-n+1),rounding=ROUND_HALF_UP)
reg=[];tables=[]
with localcontext() as c:
 c.prec=60
 for row in M['calculations']:
  if row['id'].startswith('antilog_'):
   exponent=D(row['expression'].split('**')[1]);v=D(10)**exponent
  else:v=vals[row['id']]
  value=calc(ast.parse(row['expression'],mode='eval'));reg.append({'id':row['id'],'independent':str(v),'expression':value,'expected':row['expected'],'pass':math.isclose(float(v),value,rel_tol=1e-12,abs_tol=1e-12) and math.isclose(float(v),row['expected'],rel_tol=1e-12,abs_tol=1e-12)})
 for u,listed in anti:
  v=D(10)**D(u);rounded=sig(v,4);tables.append({'kind':'antilog','input':u,'independent_value':str(v),'four_sf':str(rounded),'listed':listed,'pass':str(rounded)==listed})
 for n,listed in [(1,'0'),(2,'.3010'),(3,'.4771'),(4,'.6021'),(5,'.6990'),(6,'.7782'),(7,'.8451'),(8,'.9031'),(9,'.9542'),(10,'1')]:
  v=D(n).log10();rounded=v.quantize(D('.0001'),rounding=ROUND_HALF_UP);tables.append({'kind':'commonlog','input':n,'independent_value':str(v),'four_dp':str(rounded),'listed':listed,'pass':D(listed)==rounded})
checks={'all37registry_correct':len(reg)==37 and all(r['pass'] for r in reg),'all21log_and_antilog_rows_correct':len(tables)==21 and all(t['pass'] for t in tables),'all14cards_unique':[x['id'] for x in M['items']]==[f'CIL{i}' for i in range(1,15)],'all14lessons40min':len(L['lessons'])==14 and all(sum(l['minutes'])==40 for l in L['lessons']),'final4_10_8_8_8plus2':L['lessons'][-1]['minutes']==[4,10,8,8,10] and 'Allow8minutes forsection4 and2minutes checking' in L['lessons'][-1]['phases'][-1][1],'blueprint_lesson_maps_match':all(l['number']==p['lesson'] and l['outcomes']==p['outcomes'] and l['materials']==p['materials'] and l['title']==p['title'] for l,p in zip(L['lessons'],P['lesson_map'])),'all7outcomes_have_routes':set().union(*(set(l['outcomes']) for l in L['lessons']))=={o['id'] for o in S['outcomes']},'four_final_sections_and_criteria':len(L['assessment']['sections'])==len(L['assessment']['rubric'])==4,'source_metadata_exact':all(L['unit'][k]==S[k] for k in ['coreCompetencies','values','pcis']),'no_official_allocation':S['official_lesson_allocation'] is None}
solutions={
'CIL1':'8=2^3;27=3^3;64=2^6=4^3=8^2;1000=10^3.3^4=81,not12. Base repeated factor,index factor count in initial integer setting.',
'CIL2':'Five2factors->32;cancel2of5factors3->27;six2factors->64;(2*3)^2=2^2*3^2=36. Samebase product add/quotient subtract with nonzero denominator;power nested multiply;product distributes for integer n.2²+2³=12,not32.',
'CIL3':'3²/3²=1=3^0;2²/2⁵=1/8=2^-3.5^0=1,2^-3=1/8,10^-2=1/100,4^-1=1/4. Nonzero bases required;no assertion0^0 or0^-n;negative exponent not negative sign.',
'CIL4':'16^.5=4;27^(2/3)=9;81^(-.5)=1/9;32^(2/5)=4. Root3of27=3/root5of32=2;check9³=27²=729,4⁵=32²=1024. Fraction1/n is the exponent,NOT the root value;the power x^(1/n) is root ofx.',
'CIL5':'A72,B12,C25,D64,E256,F4,G-4. (2+3)^2=25,not13. Differentbase products need own values;powerofpower/exponenttower differ,minusinside/outside differs.',
'CIL6':'log1000=3,log1=0,log.01=-2,log(sqrt10)=1/2;reverse equations given. log.1=-1.10^u>0 means no real log0/-1;negative outputallowedforpositiveinputbelow1.',
'CIL7':'log70≈1.8451;log.007≈-2.1549;log200≈2.3010;log.02≈-1.6990. m7/7/2/2 withk1/-3/2/-2. Full signed decimalnotnegativewholemagnitude/barshorthand. Powers10exact,otherrowsrounded.',
'CIL8':'Actualcommonlogs2≈.3010299957,.02≈-1.6989700043,7≈.8450980400;10^.3010≈1.9998618696 NOT exact2.4DP .3010,-1.6990,.8451. No assumed keylayout/actualdisplay;actualobservationpendingifunprovided.',
'CIL9':'xy=10^(u+v) forpositiveinputs. log2+log3≈.7781 ->5.999 ->6.00(3SF),exact6. log20+log300≈3.7781->10³*5.999=5999 ->6.00e3,exact6000. Exact law distinctfromroundedtables.',
'CIL10':'log30-log5≈1.4771-.6990=.7781 ->5.999 ->6.00;log300-log.5≈2.4771-(-.3010)=2.7781 ->599.9 ->6.00e2. Exact6/600. Reversing subtractioninvertsquotient;inputspositive.',
'CIL11':'3log2≈.9030->7.998->8.00,exact8. log3/2≈.23855 round.2386->1.732->1.73,exactsqrt3. log8/3≈.3010333 round.3010->2.000->2.00,exact2. Divideexponentbyrootindex,notbasenumber.',
'CIL12':'log20+log300-log5≈3.0791. Antilog10^3.0791=10³*10^.0791≈1000*1.200->1.20e3;directexact1200. Logitself3.0791 is NOT10³*10^.0791. Concretebenefit simpleroperations;limitsfiniteprecision,positiveinputs/directsimplearithmeticoftenpreferable.',
'CIL13':'A1/8;B1;Clog5≈.6990 notlog6≈.7781;Dlog.02≈-1.6990;Efiniteoutputsnotalways exact;F16^.5=4not8. Repairs/chartauditapplylaws;do not explicitlyrequirefactor-lawderivation,inversepower/lognotationorindividualusefulnessreflection.',
'I1':'10^-3,2^-5;3²*3³=3⁵=243;3⁵/3²=3³=27 byfactorcancellation;27^(2/3)=9;4^-1=1/4;5^0=1. Positivefractionalbases/nonzeroquotientandnegativeexponents.',
'I2':'log.01=-2,log1000=3;log70≈1.8451,log.007≈-2.1549. No reallog0/negativeinput. Actual log7 rounds.8451(4DP),action/displayobservedseparatelyorNOTOBSERVED.',
'I3':'log7+log5≈1.5441 ->10*3.500≈35.0(3SF),exact35. log20-log8≈1.3010-.9031=.3979 ->2.500≈2.50(3SF),exact2.5. Suppliedfinalrowscomplete.',
'I4':'2log3≈.9542 ->8.999≈9.00(3SF),exact9. log5/2≈.3495 ->2.236≈2.24(3SF),exactsqrt5. Benefitoperationconversion+specificprecision/domainlimit;reasoneddirectmethodpreferencevalid,enthusiasmnotgrade.'}
result={'registry':reg,'table_rows':tables,'checks':checks,'pass':sum(checks.values()),'total':len(checks),'task_solutions':solutions,'verdict_limit':'Arithmetic and table checks pass;this does NOT close two manuscript notation defects or L13 mapping gap identified in report. No actual device/group actions performed.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'registry':sum(x['pass'] for x in reg),'tables':sum(x['pass'] for x in tables),'checks':checks},indent=2));assert all(checks.values())
