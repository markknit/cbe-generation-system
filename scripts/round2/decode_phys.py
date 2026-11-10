import sys,zipfile,re,collections,json
sys.path.insert(0,'.')
import decode
from lxml import etree
W=decode.W
def run(f):
    root=etree.fromstring(zipfile.ZipFile(f).read('word/document.xml')); out={}
    for row in root.iter(W+'tr'):
        cells=row.findall(W+'tc')
        if len(cells)!=5: continue
        t=lambda c:' '.join(''.join(x.text or '' for x in p.iter(W+'t')) for p in c.iter(W+'p'))
        if t(cells[0]).startswith('Journal item'): continue
        key=re.sub(r'\s*\(\+\d+ related edits?\)','',t(cells[0])).strip()
        acc=edi=False; typed=[]; sect='pre'
        for rs in decode.paras(cells[4]):
            txt=''.join(a for a,_ in rs).strip()
            if not txt or txt.startswith('Tick ONE') or txt.startswith('Item '): continue
            if 'ACCEPT' in txt.upper() and len(txt)<14:
                acc=decode.REDISH({m for a,k in rs if a.strip() for m in k}) or bool(re.search('[✅☑☒✔✓]',txt)); sect='acc'; continue
            if re.fullmatch(r'\W*EDIT\W*',txt.upper()):
                edi=decode.REDISH({m for a,k in rs if a.strip() for m in k}) or bool(re.search('[✅☑☒✔✓]',txt)); sect='edit'; continue
            if txt.upper().startswith('IF EDIT, TYPE'): sect='typed'; continue
            typed.append((sect,txt))
        d='AMBIGUOUS' if acc and edi else 'EDIT' if edi else 'ACCEPT' if acc else ('EDIT?' if [x for s,x in typed if s in('typed','edit')] else 'UNMARKED')
        out[key]=dict(decision=d,typed=typed,type=t(cells[1]),where=t(cells[2]),issue=re.sub(r'\s+',' ',t(cells[3])))
    return out
if __name__=='__main__':
    o=run('finished_2026-11-09/Finished/Flagged_Items_Physics.docx')
    print(collections.Counter((v['decision'],v['type']) for v in o.values()))
    json.dump(o,open('Flagged_Items_Physics.decoded.json','w'),indent=1,ensure_ascii=False)
    for k,v in o.items():
        if v['decision']!='ACCEPT' or any(s=='typed' or s=='edit' for s,_ in v['typed']):
            print('##',k,v['decision'],v['type'],'|',v['where'][:60])
            print('   ISSUE:',v['issue'][:230])
            for s,x in v['typed']: print('   [%s]'%s,x[:420])
