import sys,zipfile,re
from lxml import etree
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
f=sys.argv[1]
root=etree.fromstring(zipfile.ZipFile(f).read('word/document.xml'))
body=root.find(W+'body')
tbls=body.findall(W+'tbl')
print('tables',len(tbls),'top-level paras',len(body.findall(W+'p')))
def rinfo(r):
    rp=r.find(W+'rPr'); d={}
    if rp is not None:
        for k in ('color','highlight','shd'):
            e=rp.find(W+k)
            if e is not None: d[k]=dict((a.split('}')[1],v) for a,v in e.attrib.items())
        for k in ('b','strike','u'):
            if rp.find(W+k) is not None: d[k]=1
    return d
t=tbls[int(sys.argv[2])]
for ri,row in enumerate(t.findall(W+'tr')):
    for ci,c in enumerate(row.findall(W+'tc')):
        tcp=c.find(W+'tcPr'); shd=tcp.find(W+'shd') if tcp is not None else None
        fill=shd.get(W+'fill') if shd is not None else None
        txt=''
        marks=set()
        for r in c.iter(W+'r'):
            tt=''.join(x.text or '' for x in r.findall(W+'t'))
            i=rinfo(r)
            if tt.strip() and i: marks.add((tuple(sorted((k,tuple(sorted(v.items())) if isinstance(v,dict) else v) for k,v in i.items())) ))
            txt+=tt
        sdt=len(list(c.iter(W+'sdt')))
        print(f'[r{ri}c{ci}] fill={fill} sdt={sdt} :: {txt[:110]!r}')
        if marks and ri<4: print('     marks',list(marks)[:4])
