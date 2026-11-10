import sys,zipfile,re,collections,json
from lxml import etree
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
def load(f):
    root=etree.fromstring(zipfile.ZipFile(f).read('word/document.xml'))
    items={}
    for t in root.iter(W+'tbl'):
        for row in t.findall(W+'tr'):
            cells=row.findall(W+'tc')
            if len(cells)!=6: continue
            txt=lambda c:'\n'.join(''.join(x.text or '' for x in p.iter(W+'t')) for p in c.iter(W+'p'))
            resp=txt(cells[5])
            m=re.search(r'Item (\S+)\s*$',resp.strip())
            if not m: continue
            sig=[]
            for ci,c in enumerate(cells):
                tcp=c.find(W+'tcPr'); shd=tcp.find(W+'shd') if tcp is not None else None
                fill=shd.get(W+'fill') if shd is not None else None
                fm=collections.Counter()
                for r in c.iter(W+'r'):
                    tt=''.join(x.text or '' for x in r.findall(W+'t'))
                    if not tt.strip(): continue
                    rp=r.find(W+'rPr'); k=[]
                    if rp is not None:
                        for n in ('color','highlight','shd'):
                            e=rp.find(W+n)
                            if e is not None: k.append(n+'='+(e.get(W+'val') or e.get(W+'fill') or ''))
                    fm[tuple(k)]+=1
                sig.append((fill,dict(fm)))
            chk=[(e.get('{http://schemas.microsoft.com/office/word/2010/wordml}val')) for e in c.iter('{http://schemas.microsoft.com/office/word/2010/wordml}checked')] if False else None
            items[m.group(1)]=dict(cells=[txt(c) for c in cells],sig=sig,xml=etree.tostring(cells[5]).decode())
    return items
if __name__=='__main__':
    o=load(sys.argv[1]); n=load(sys.argv[2])
    print('orig items',len(o),'returned items',len(n),'only-in-orig',len(set(o)-set(n)),'only-in-new',len(set(n)-set(o)))
    chg=collections.Counter(); ex=collections.defaultdict(list)
    for k in n:
        if k not in o: continue
        for ci in range(6):
            if o[k]['cells'][ci]!=n[k]['cells'][ci]: chg['text c%d'%ci]+=1; ex['text c%d'%ci].append(k)
            if o[k]['sig'][ci]!=n[k]['sig'][ci]: chg['fmt c%d'%ci]+=1; ex['fmt c%d'%ci].append(k)
    print(dict(chg))
    for k,v in ex.items(): print(k, v[:5])
