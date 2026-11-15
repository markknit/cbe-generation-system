from pathlib import Path
import json,subprocess
from concurrent.futures import ThreadPoolExecutor
P=Path(__file__).resolve().parent
B=Path('data/curriculum_expansion_2026-11')
plan=json.loads((P/'readable_plan.json').read_text())
def render(x):
 typ,n=x;pdf=B/'outputs/PDF'/('Codex_Core_Mathematics_Rotation_'+typ+'.pdf');out=P/(typ+'_readable_'+str(n));subprocess.run(['pdftoppm','-r','130','-f',str(n),'-l',str(n),'-singlefile','-png',str(pdf),str(out)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
with ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(render,[(t,n) for t,ns in plan.items() for n in ns]))
print('Saved',sum(map(len,plan.values())),'readable page samples at130dpi from unchanged PDFs.')
