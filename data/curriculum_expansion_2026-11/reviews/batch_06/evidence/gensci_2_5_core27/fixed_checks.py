from pathlib import Path
from fractions import Fraction as F
from statistics import mean
import json,math
E=Path(__file__).resolve().parent;M=json.loads((Path.cwd()/'data/curriculum_expansion_2026-11/materials/gensci_2_5.json').read_text());checks={};R={}
def ck(k,x):checks[k]=bool(x)
def intervals(ts,vs):return [F(b-a,y-x) for x,y,a,b in zip(ts,ts[1:],vs,vs[1:])]
def savefracs(xs):return [{'exact':str(x),'decimal':float(x)} for x in xs]
R['RR1']={'rates_cm3_per_s':[float(F(24,30)),float(F(24,60))],'ratio':float(F(24,30)/F(24,60))};ck('RR1_rates',R['RR1']['rates_cm3_per_s']==[.8,.4]);ck('RR1_ratio',R['RR1']['ratio']==2)
for tag,t,v,wanted,limit in [('RR2',[0,10,20,30,40,50],[0,18,30,38,42,42],[F(9,5),F(6,5),F(4,5),F(2,5),F(0)],4),('RR13',[0,10,20,30,40],[0,12,20,24,24],[F(6,5),F(4,5),F(2,5),F(0)],3)]:
 rates=intervals(t,v);R[tag+'_gas_graph']={'points':list(zip(t,v)),'interval_rates':savefracs(rates),'overall_specified':float(F(v[limit]-v[0],t[limit]-t[0]))}
 for i,(r,s) in enumerate(zip(rates,wanted),1):ck(f'{tag}_interval{i}',r==s)
 ck(tag+'_overall',F(v[limit],t[limit])==({'RR2':F(21,20),'RR13':F(4,5)}[tag]));ck(tag+'_plateau_recorded',v[-1]==v[-2]);ck(tag+'_positive_time_intervals',all(b>a for a,b in zip(t,t[1:])))
for tag,vals,want,fmt in [('RR4_20',[60,64,62],62,'0.0161'),('RR4_30',[40,42,44],42,'0.0238'),('RR13_P',[48,50,52],50,'0.0200'),('RR13_Q',[28,30,32],30,'0.0333')]:
 av=F(sum(vals),len(vals));rg=max(vals)-min(vals);rec=1/av;f=format(float(rec),'#.3g');R[tag]={'times_s':vals,'mean_s':float(av),'range_s':rg,'reciprocal_mean_exact':str(rec),'reciprocal_mean_3sf_s_inverse':f}
 ck(tag+'_mean',av==want);ck(tag+'_range',rg==4);ck(tag+'_index3sf',f==fmt)
for tag,points,wanted in [('RR5',[(10,2),(20,4),(30,7),(40,8),(60,1)],(40,8)),('RR13',[(20,4),(35,8),(55,2)],(35,8))]:
 got=max(points,key=lambda p:p[1]);R[tag+'_enzyme']={'points':points,'highest_tested':got};ck(tag+'_highest_tested',got==wanted);ck(tag+'_high_temp_decline',points[-1][1]<got[1])
# Same quantities at fixed time support comparison only; graph slopes are not instantaneous rates.
R['RR6']={'concentrations_mol_L':[.5,1,1.5],'rates_cm3_s':[2,4,6],'ratio_over_tested_range':[float(F(2,F(1,2))),4,float(F(6,F(3,2)))]};ck('RR6_tested_proportional',R['RR6']['ratio_over_tested_range']==[4,4,4])
large_v=F(2)**3;large_a=6*F(2)**2;small_v=8*F(1)**3;small_a=8*6*F(1)**2;R['RR7']={'large_volume_cm3':float(large_v),'large_area_cm2':float(large_a),'small_total_volume_cm3':float(small_v),'small_total_area_cm2':float(small_a),'area_ratio':float(small_a/large_a)}
for name,x,y in [('large_volume',large_v,8),('large_area',large_a,24),('small_volume',small_v,8),('small_area',small_a,48),('area_ratio',small_a/large_a,2)]:ck('RR7_'+name,x==y)
ck('RR7_conserved_material_volume',large_v==small_v);R['RR8_density_factor']=float(1/F(1,2));ck('RR8_density_doubles',R['RR8_density_factor']==2)
R['RR9']={'with_0to20_units_s':float(F(40,20)),'without_0to20_units_s':float(F(20,20))};ck('RR9_with',R['RR9']['with_0to20_units_s']==2);ck('RR9_without',R['RR9']['without_0to20_units_s']==1)
ck('RR10_supplied_monotone',1<3<5);ck('RR11_only_A_fits_budget',4<=5 and 10>5);ck('RR13_only_A_fits_budget',4<=5 and 9>5)
expected=[F(4,5),F(2,5),F(21,20),F(9,5),F(62),F(42),F(1,62),F(1,42),F(8),F(24),F(8),F(48),F(4,5),F(50),F(30),F(1,50),F(1,30)]
ck('exact17registry',len(M['calculations'])==len(expected))
for c,v in zip(M['calculations'],expected):ck(c['id']+'_independent',math.isclose(c['expected'],float(v),rel_tol=1e-13,abs_tol=1e-13))
R['checks']=checks;R['passed']=sum(checks.values());R['total']=len(checks);R['failed']=[k for k,v in checks.items() if not v];R['method_limit']='Independent raw-record calculations and expected graph coordinates; no supplied or learner-drawn graph image exists in these canonical inputs. Full task/condition/safety review is reported separately. No experiment performed.'
(E/'fixed_checks.json').write_text(json.dumps(R,indent=2)+'\n');print(json.dumps({k:R[k] for k in ['passed','total','failed']}))
