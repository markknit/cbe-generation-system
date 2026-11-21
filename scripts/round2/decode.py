import sys,json,re,zipfile
from lxml import etree
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
CHK=re.compile('[✅☑☒✔✓✗❌xX]')
def fmt(r):
    rp=r.find(W+'rPr'); k=set()
    if rp is not None:
        c=rp.find(W+'color'); h=rp.find(W+'highlight'); s=rp.find(W+'shd')
        if c is not None: k.add('color='+c.get(W+'val','').lower())
        if h is not None: k.add('hl='+h.get(W+'val','').lower())
        if s is not None and (s.get(W+'fill') or '').lower() not in('','auto','ffffff'): k.add('shd='+s.get(W+'fill').lower())
    return k
REDISH=lambda k:any(x in('color=ff0000','color=c00000','color=e06666','color=cc0000','color=ea4335','hl=red','hl=magenta','hl=darkred') or x.startswith('shd=ff') for x in k)
def paras(c):
    out=[]
    for p in c.findall('.//'+W+'p'):
        rs=[]
        for r in p.iter(W+'r'):
            t=''.join(x.text or '' for x in r.findall(W+'t'))
            # content-control checkbox state
            rs.append((t,fmt(r)))
        for sdt in p.iter('{http://schemas.microsoft.com/office/word/2010/wordml}checked'):
            rs.append(('[chk:%s]'%sdt.get('{http://schemas.microsoft.com/office/word/2010/wordml}val'),set()))
        out.append(rs)
    return out
def classify(cell):
    ps=paras(cell); res={'accept':[], 'edit':[], 'typed':[], 'notes':[]}
    state='pre'
    for rs in ps:
        txt=''.join(t for t,_ in rs)
        if re.match(r'\s*Item \S+\s*$',txt): continue
        if txt.strip().startswith('Tick ONE'): continue
        low=txt.upper()
        if 'IF EDIT, TYPE' in low: state='typed'; continue
        has_a='ACCEPT' in low; has_e=re.search(r'\bEDIT\b',low) is not None
        if state=='pre' and (has_a or has_e):
            # find which label this paragraph is about
            ev=[]
            checked=bool(re.search('[✅☑☒✔✓]',txt)) or 'chk:1' in txt
            red=any(REDISH(k) for t,k in rs if t.strip() and (('ACCEPT' in t.upper()) or re.search(r'\bEDIT\b',t.upper()) or t.strip() in('☐','✅','☑','☒','✔')))
            anyred=any(REDISH(k) for t,k in rs if t.strip())
            if has_a and not has_e: res['accept'].append(dict(text=txt,checked=checked,red=red or anyred))
            elif has_e and not has_a: res['edit'].append(dict(text=txt,checked=checked,red=red or anyred))
            else: res['notes'].append(('both-labels-in-one-paragraph',txt))
            # any text beyond the label counts as typed
            extra=re.sub(r'[☐✅☑☒✔✓]|ACCEPT|EDIT','',txt).strip(' -: ')
            if extra: res['typed'].append(extra)
        elif txt.strip():
            res['typed'].append(txt.strip())
    return res
def decide(res):
    a=any(x['checked'] or x['red'] for x in res['accept'])
    e=any(x['checked'] or x['red'] for x in res['edit'])
    typed=' '.join(res['typed']).strip()
    if a and e: return 'AMBIGUOUS','both accept and edit marked'
    if e: return 'EDIT','edit marked'
    if a and typed: return 'ACCEPT+COMMENT','accept marked with text'
    if a: return 'ACCEPT','accept marked'
    if typed: return 'EDIT?','no box marked but text typed'
    return 'UNMARKED','no mark (white => accepted)'
def run(f):
    root=etree.fromstring(zipfile.ZipFile(f).read('word/document.xml')); out={}
    for row in root.iter(W+'tr'):
        cells=row.findall(W+'tc')
        if len(cells)!=6: continue
        t5=''.join(x.text or '' for x in cells[5].iter(W+'t'))
        m=re.search(r'Item (\S+)\s*$',t5.strip())
        if not m: continue
        res=classify(cells[5]); d,why=decide(res)
        c0=''.join(x.text or '' for x in cells[0].iter(W+'t'))
        attn='FLAG' if '[FLAG]' in c0 else 'DECISION' if '[DECISION]' in c0 else 'normal'
        out[m.group(1)]=dict(decision=d,why=why,typed=' | '.join(res['typed']),attention=attn,notes=res['notes'])
    return out
if __name__=='__main__':
    import collections
    for f in sys.argv[1:]:
        o=run(f); print('==',f.split('/')[-1],len(o))
        print(collections.Counter((v['decision'],v['attention']) for v in o.values()))
        json.dump(o,open(f.split('/')[-1].replace('.docx','.decoded.json'),'w'),indent=1,ensure_ascii=False)
