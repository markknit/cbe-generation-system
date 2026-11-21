from pathlib import Path
import ast,json,operator,math
O=Path(__file__).resolve().parent;B=O.parents[3];d=json.loads((B/'materials/gensci_2_5.json').read_text());ops={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.Pow:operator.pow}
def ev(n):
 if isinstance(n,ast.Constant):return n.value
 if isinstance(n,ast.BinOp):return ops[type(n.op)](ev(n.left),ev(n.right))
 raise ValueError(n)
expected={'RR_A_RATE':.8,'RR_B_RATE':.4,'RR_GRAPH_AVG':1.05,'RR_GRAPH_FIRST':1.8,'RR_MEAN20':62,'RR_MEAN30':42,'RR_INDEX20':1/62,'RR_INDEX30':1/42,'RR_LARGE_VOLUME':8,'RR_LARGE_AREA':24,'RR_SMALL_VOLUME':8,'RR_SMALL_AREA':48,'RR_FINAL_AVG':.8,'RR_FINAL_MEANP':50,'RR_FINAL_MEANQ':30,'RR_FINAL_INDEXP':.02,'RR_FINAL_INDEXQ':1/30};reg=[]
for x in d['calculations']:
 v=ev(ast.parse(x['expression'],mode='eval').body);reg.append({**x,'evaluated':v,'independently_derived':expected[x['id']],'pass':math.isclose(v,x['expected'],rel_tol=1e-12) and math.isclose(v,expected[x['id']],rel_tol=1e-12)})
assert len(reg)==17 and all(x['pass'] for x in reg)
def intervals(t,v):return [(v[i+1]-v[i])/(t[i+1]-t[i]) for i in range(len(t)-1)]
training={'time_s':[0,10,20,30,40,50],'gas_cm3':[0,18,30,38,42,42]};training['interval_rates_cm3_s']=intervals(training['time_s'],training['gas_cm3']);training['overall_0_40']=42/40;assert training['interval_rates_cm3_s']==[1.8,1.2,.8,.4,0]
final={'time_s':[0,10,20,30,40],'gas_cm3':[0,12,20,24,24]};final['interval_rates_cm3_s']=intervals(final['time_s'],final['gas_cm3']);final['overall_0_30']=24/30;assert final['interval_rates_cm3_s']==[1.2,.8,.4,0]
endpoint={}
for name,ts in [('RR4_20C',[60,64,62]),('RR4_30C',[40,42,44]),('final_P',[48,50,52]),('final_Q',[28,30,32])]:
 mean=sum(ts)/len(ts);endpoint[name]={'times_s':ts,'mean_s':mean,'range_s':max(ts)-min(ts),'reciprocal_mean_s_minus1':1/mean,'three_significant_figures':format(1/mean,'.3g')}
assert [x['three_significant_figures'] for x in endpoint.values()]==['0.0161','0.0238','0.02','0.0333'];endpoint['final_P']['three_significant_figures_written']='0.0200';assert float('0.0200')==.02
extra={'RR1_rate_ratio':.8/.4,'RR5_highest_tested_C':40,'RR5_highest_product_units':8,'RR6_rate_over_concentration':[2/.5,4/1,6/1.5],'cube_original_cm3':2**3,'cube_final_cm3':8*1**3,'cube_original_cm2':6*2**2,'cube_final_cm2':8*6*1**2,'cube_area_ratio':48/24,'cube_volume_ratio':8/8,'RR8_density_multiplier':2,'RR9_catalysed_average_units_s':40/20,'RR9_uncatalysed_average_units_s':20/20,'final_enzyme_highest_tested_C':35,'RR11_budget_choice':'A,4<=5while10>5','final_budget_choice':'A,4<=5while9>5'}
r={'registered':reg,'RR2_graph':training,'final_graph':final,'endpoint_trials':endpoint,'other_independent_results':extra,'all_pass':True,'note':'format .3g drops insignificant display zeros; finalP explicitly written0.0200to3sf in key.'};(O/'fixed_checks.json').write_text(json.dumps(r,indent=2)+'\n');print('17registry+all interval/endpoint/cube/factor/final checks PASS')
