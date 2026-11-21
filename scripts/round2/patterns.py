import sys,collections,re
sys.path.insert(0,'.')
import runs as R
W=R.W
for f in sys.argv[1:]:
    d=R.items(f); pat=collections.Counter(); typed=0; ex={}
    for k,cells in d.items():
        rs=[r for r in R.runs(cells[5])]
        # signature: for label runs
        sig=[]
        for t,fm in rs:
            t2=t.strip()
            if t2 in('Tick ONE:','If EDIT, type your requested change here:') or t2.startswith('Item '): continue
            if not t2 and not fm: continue
            sig.append((t2[:25],fm))
        s=tuple(sig); pat[s]+=1; ex.setdefault(s,k)
    print('==',f.split('/')[-1],len(d))
    for s,n in pat.most_common(12): print(n,ex[s],s)
