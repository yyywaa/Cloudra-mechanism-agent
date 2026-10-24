#!/usr/bin/env python3
"""Per-point table for the E2 lane 1D constrained scan (job 917) and fine scan (964):
r(C4-O6) [rows 5-7], r(C4-O10) [5-11], dihedral O6-C4-C7-O10 [7-5-8-11], energy."""
import sys, math
sys.path.insert(0, '/home/ly/Cloudra-mechanism-agent/gold_fill_20261018/NR1/analysis')
from scan_table import parse, d, sha256

def vec(a,b): return [b[i]-a[i] for i in range(3)]
def dih(a,b,c,dd):
    b1=vec(b,a); b2=vec(c,b); b3=vec(dd,c)
    def cr(u,v): return [u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]
    def dt(u,v): return sum(u[i]*v[i] for i in range(3))
    n1=cr(b1,b2); n2=cr(b2,b3)
    m=cr(n1,[x/math.sqrt(dt(b2,b2)) for x in b2])
    return math.degrees(math.atan2(dt(m,n2),dt(n1,n2)))

path=sys.argv[1]
print('file', path); print('sha256', sha256(path))
pts=parse(path); print('n_points', len(pts))
for n,p in enumerate(pts,1):
    at={a[0]:a for a in p['geom'][1]}
    e=p['scf'][1]
    print('pt%02d E=%.9f (L%d) r(5-7)=%.4f r(5-11)=%.4f dih(7-5-8-11)=%+7.1f' % (
        n, e, p['scf'][0], d(p['geom'][1],5,7), d(p['geom'][1],5,11),
        dih(at[7][2:],at[5][2:],at[8][2:],at[11][2:])))
