#!/usr/bin/env python3
import itertools
S="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split"
def rd(p):
    L=open(p).read().splitlines(); n=int(L[0].split()[0])
    return [(l.split()[0],[float(x) for x in l.split()[1:4]]) for l in L[2:2+n]]
for f in ["INT1_27_start.xyz","RC_27_opt_frame.xyz"]:
    g=rd(f"{S}/{f}"); best=(9e9,0,0)
    for i,j in itertools.combinations(range(len(g)),2):
        d=sum((g[i][1][k]-g[j][1][k])**2 for k in range(3))**0.5
        if d<best[0]: best=(d,i+1,j+1)
    print(f, "natoms=%d minsep=%.4f A between atoms %d(%s) and %d(%s)"%(len(g),best[0],best[1],g[best[1]-1][0],best[2],g[best[2]-1][0]))
