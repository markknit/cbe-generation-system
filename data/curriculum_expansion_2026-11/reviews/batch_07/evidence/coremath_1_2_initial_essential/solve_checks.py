from pathlib import Path
from decimal import Decimal,localcontext,ROUND_HALF_UP
import json,math
P=Path(__file__).resolve().parent
m=json.loads((P/'materials_snapshot.json').read_text());checks=[]
for c in m['calculations']:
 v=eval(c['expression'],{'__builtins__':{}},{})
 checks.append({'id':c['id'],'expression':c['expression'],'independent_value':v,'registered_expected':c['expected'],'pass':math.isclose(v,c['expected'],rel_tol=1e-12,abs_tol=1e-12)})
rows=[]
with localcontext() as ctx:
 ctx.prec=45
 for x,expected in [('1','0.0000'),('2','0.3010'),('3','0.4771'),('4','0.6021'),('5','0.6990'),('6','0.7782'),('7','0.8451'),('8','0.9031'),('9','0.9542'),('10','1.0000')]:
  v=Decimal(x).log10();r=str(v.quantize(Decimal('.0001'),rounding=ROUND_HALF_UP));rows.append({'kind':'log10','x':x,'high_precision':str(v),'rounded':r,'expected':expected,'pass':r==expected})
 for x,expected in [('.7781','5.999'),('.3010','2.000'),('.4771','3.000'),('.6990','5.000'),('.9030','7.998'),('.2386','1.732'),('.0791','1.200'),('.5441','3.500'),('.3979','2.500'),('.9542','8.999'),('.3495','2.236')]:
  v=Decimal(10)**Decimal(x);r=str(v.quantize(Decimal('.001'),rounding=ROUND_HALF_UP));rows.append({'kind':'10^u','x':x,'high_precision':str(v),'rounded_4sf':r,'expected':expected,'pass':r==expected})
 d={'registry':checks,'unique_supplied_table_rows':rows,'registry_passed':sum(x['pass'] for x in checks),'table_rows_passed':sum(x['pass'] for x in rows)}
(P/'independent_numerical_checks.json').write_text(json.dumps(d,indent=2)+'\n')
assert all(x['pass'] for x in checks+rows)
print('Registry',len(checks),'PASS; unique table rows',len(rows),'PASS')
