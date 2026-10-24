#!/usr/bin/env python3
"""Per-point table for a Gaussian relaxed scan log (independent cross-check).
Point boundaries: each 'Optimization completed' line.
Point energy: last 'SCF Done' before that line.
Point geometry: last 'Input orientation' block before that line.
"""
import sys, re, math, hashlib

ZSYM = {1:'H',6:'C',7:'N',8:'O'}

def sha256(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda: f.read(1<<20), b''): h.update(b)
    return h.hexdigest()

def parse(path):
    lines = open(path).readlines()
    pts=[]
    last_scf=None; last_geom=None
    for i,l in enumerate(lines,1):
        if 'SCF Done' in l:
            m=re.search(r'=\s*(-?\d+\.\d+)', l)
            if m: last_scf=(i,float(m.group(1)))
        if 'Input orientation' in l:
            k=i+4-1  # i is 1-based; header at index i
            atoms=[]
            j=i+4
            # lines[j-1] is 4th line after header (the dashes); data starts at i+5 (1-based)
            j=i+5
            while j<=len(lines) and '-----' not in lines[j-1]:
                p=lines[j-1].split()
                if len(p)>=6: atoms.append((int(p[0]), ZSYM.get(int(p[1]),'X'), float(p[3]),float(p[4]),float(p[5])))
                j+=1
            last_geom=(i,atoms)
        if 'Optimization completed' in l or 'Stationary point found' in l:
            if 'Optimization completed' in l:
                pts.append({'optline':i,'scf':last_scf,'geom':last_geom})
    return pts

def d(at,i,j):
    p={a[0]:a for a in at}
    return math.dist(p[i][2:5],p[j][2:5])

if __name__=='__main__':
    path=sys.argv[1]; pairs=[tuple(map(int,s.split('-'))) for s in sys.argv[2:]]
    print('file', path); print('sha256', sha256(path))
    pts=parse(path)
    print('n_points', len(pts))
    e0=pts[0]['scf'][1] if pts and pts[0]['scf'] else None
    for n,p in enumerate(pts,1):
        at=p['geom'][1] if p['geom'] else []
        ds=' '.join('d%d-%d=%.4f'%(i,j,d(at,i,j)) for i,j in pairs)
        e=p['scf'][1]; ln=p['scf'][0]
        rel=(e-e0)*627.5095
        print('pt%02d  E=%.9f (L%d)  rel=%+7.3f kcal  geomline=%d  %s'%(n,e,ln,rel,p['geom'][0],ds))
