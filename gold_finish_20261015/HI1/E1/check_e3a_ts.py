import re, numpy as np
log='ts/ts_0016/jobs/declaration_0007/ts_opt/refine.log'
lines=open(log,errors='ignore').read().splitlines()
natom=41
idx=[k for k,L in enumerate(lines) if 'orientation:' in L]
k=idx[-1]
# structure: header line, sep line, col header, sep line, then natom rows
start=k+5
# find the two separators after header
seps=[i for i in range(k, min(k+8,len(lines))) if set(lines[i].strip())=={'-'} or lines[i].strip().startswith('----')]
start=seps[1]+1
rows=[]
i=start
while len(rows)<natom and i<len(lines):
    p=lines[i].split()
    if len(p)==6:
        rows.append((int(p[0]),p[1],float(p[3]),float(p[4]),float(p[5])))
    elif len(p)==5 and p[0].isdigit():
        rows.append((int(p[0]),p[1],float(p[2]),float(p[3]),float(p[4])))
    else:
        break
    i+=1
assert len(rows)==natom, ('row count', len(rows))
S=[r[1] for r in rows]; X=np.array([[r[2],r[3],r[4]] for r in rows])
print('block at line',k+1,'rows',len(rows),'elements',{s:S.count(s) for s in set(S)})
def d(a,b): return float(np.linalg.norm(X[a-1]-X[b-1]))
def ang(a,b,c):
    v1=X[a-1]-X[b-1]; v2=X[c-1]-X[b-1]
    return float(np.degrees(np.arccos(v1.dot(v2)/np.linalg.norm(v1)/np.linalg.norm(v2))))
for lab,a,b in [('C2-O25',2,25),('O25-H27',25,27),('O10-H27',10,27),('O11-H27',11,27),('O25-H26',25,26),('C2-N4',2,4),('C9-O10',9,10),('C9-O11',9,11)]:
    print('%-9s %.4f'%(lab,d(a,b)))
print('angle O25-H27...O10 %.1f'%ang(25,27,10))
D=np.linalg.norm(X[:,None,:]-X[None,:,:],axis=-1); np.fill_diagonal(D,9)
print('minsep %.4f'%D.min())