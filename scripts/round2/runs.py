import sys,zipfile,re,collections
from lxml import etree
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
def runs(c):
    out=[]
    for r in c.iter(W+'r'):
        tt=''.join(x.text or '' for x in r.findall(W+'t'))
        rp=r.find(W+'rPr'); k=[]
        if rp is not None:
            for n in ('color','highlight','shd'):
                e=rp.find(W+n)
                if e is not None: k.append(n+'='+(e.get(W+'val') or e.get(W+'fill') or '').lower())
            if rp.find(W+'strike') is not None: k.append('strike')
        out.append((tt,tuple(k)))
    return out
def items(f):
    root=etree.fromstring(zipfile.ZipFile(f).read('word/document.xml')); d={}
    for row in root.iter(W+'tr'):
        cells=row.findall(W+'tc')
        if len(cells)!=6: continue
        t5=''.join(x.text or '' for x in cells[5].iter(W+'t'))
        m=re.search(r'Item (\S+)\s*$',t5.strip())
        if m: d[m.group(1)]=cells
    return d
if __name__=='__main__':
    d=items(sys.argv[1])
    for k in sys.argv[2:]:
        print('==',k)
        for ci in (0,5):
            print(' c%d'%ci,[r for r in runs(d[k][ci]) if r[0].strip() or r[1]])
