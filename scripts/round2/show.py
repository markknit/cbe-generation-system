import sys,json,zipfile,re
sys.path.insert(0,'.')
import decode
from lxml import etree
W=decode.W
f,dec=sys.argv[1],sys.argv[2]
root=etree.fromstring(zipfile.ZipFile(f).read('word/document.xml'))
d=json.load(open(dec))
txt=lambda c:' '.join(''.join(x.text or '' for x in p.iter(W+'t')) for p in c.iter(W+'p'))
for row in root.iter(W+'tr'):
    cells=row.findall(W+'tc')
    if len(cells)!=6: continue
    m=re.search(r'Item (\S+)\s*$',txt(cells[5]).strip())
    if not m: continue
    k=m.group(1); v=d[k]
    if v['decision'] in('EDIT','EDIT?','ACCEPT+COMMENT','AMBIGUOUS'):
        print(f"## {k} [{v['decision']}/{v['attention']}] WHERE: {txt(cells[1])[:90]}")
        print('   ABOUT:',re.sub(r'\s+',' ',txt(cells[2]))[:260])
        print('   TEACHER:',v['typed'][:700])
