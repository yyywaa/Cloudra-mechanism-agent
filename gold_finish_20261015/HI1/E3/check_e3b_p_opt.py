import re,numpy as np
log="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/runs/P_e3b/P_optfreq.log"
lines=open(log,errors='ignore').read().splitlines()
term=[i for i,L in enumerate(lines) if L.startswith(' Normal termination')]
print('termination lines', [(i+1,lines[i].strip()) for i in term])
opt_end=term[0] if term else len(lines)
# last SCF before opt_end
scf=[(i+1,L.strip()) for i,L in enumerate(lines[:opt_end]) if L.strip().startswith('SCF Done')]
print('last SCF in opt segment:', scf[-1])
# last orientation block before opt_end
idx=[i for i,L in enumerate(lines[:opt_end]) if 'Standard orientation' in L or 'Input orientation' in L]
start=idx[-1]
dash=[i for i in range(start,start+20) if lines[i].strip().startswith('---')]
hdr=dash[1]
geo={}
k=hdr+1
while k<opt_end and len(geo)<41:
    p=lines[k].split()
    if len(p)==6 and p[0].isdigit():
        geo[int(p[0])]=(int(p[1]), np.array([float(p[3]),float(p[4]),float(p[5])]))
    k+=1
print('orientation header line', start+1, 'data rows', hdr+1, '->', hdr+len(geo), 'count', len(geo))
assert len(geo)==41, len(geo)
els={a:geo[a][0] for a in geo}
def R(a,b): return float(np.linalg.norm(geo[a][1]-geo[b][1]))
print('elements 2,4,25,26,27,28:', {a:els[a] for a in (2,4,25,26,27,28)})
for pair in [(2,4),(4,26),(2,26),(25,26),(2,25),(4,5),(4,8),(2,3),(9,10),(9,11),(25,27),(10,27)]:
    print('  R(%2d-%2d)=%.4f'%(pair[0],pair[1],R(*pair)))
# fragments by connectivity (covalent radii simple: d < 1.25*(r1+r2))
radii={1:0.31,6:0.76,7:0.71,8:0.66}
import itertools
parent=list(range(42))
def find(x):
    while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]
    return x
def union(a,b):
    ra,rb=find(a),find(b)
    if ra!=rb: parent[ra]=rb
for a,b in itertools.combinations(sorted(geo),2):
    d=R(a,b); lim=1.25*(radii[els[a]]+radii[els[b]])
    if d<lim: union(a,b)
from collections import defaultdict
frag=defaultdict(list)
for a in sorted(geo): frag[find(a)].append(a)
print('fragments:', [ (len(v), v[:6], '...') for v in frag.values() ])
# minsep global
best=(9e9,None)
for a,b in itertools.combinations(sorted(geo),2):
    d=R(a,b)
    if d<best[0]: best=(d,(a,b))
print('minsep %.4f %s'%(best[0],best[1]))
# H26 environment
nn=sorted(((R(26,a),a,els[a]) for a in geo if a!=26))[:3]
print('nearest to atom26:', [(round(d,4),a,el) for d,a,el in nn])
nn2=sorted(((R(4,a),a,els[a]) for a in geo if a!=4))[:4]
print('nearest to N4:', [(round(d,4),a,el) for d,a,el in nn2])
