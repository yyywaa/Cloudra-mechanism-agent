#!/usr/bin/env python3
"""Frame-invariant identity comparison between a job-1025-style frame (Gaussian log's last
'Input orientation' block, atom order = the .gjf order) and a reference xyz.

Both files here use the prep/i2.xyz order: 1 Na | 2 C(OMe) | 3 O3(OMe) | 4,5,6 H(OMe) |
7 C4 | 8 O5(carbonyl) | 9 O1(hydroxyl) | 10 H(C4) | 11 H6(on O1).
Comparison = internal coordinates + per-atom deviation after centroid+3-anchor alignment.
"""
import math, re, sys

def rd_xyz(p):
    L = open(p).read().split('\n')
    n = int(L[0].split()[0])
    return [(q[0], float(q[1]), float(q[2]), float(q[3])) for q in (l.split() for l in L[2:2+n])]

def rd_last_input_orientation(p):
    lines = open(p, errors='replace').read().split('\n')
    atomre = re.compile(r'^\s*(\d+)\s+(\d+)\s+(\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s*$')
    SYM = {1: 'H', 6: 'C', 8: 'O', 11: 'Na'}
    best = None
    for i, l in enumerate(lines):
        if 'Input orientation:' in l:
            j = i+1
            while j < len(lines) and not atomre.match(lines[j]) and j-i <= 12:
                j += 1
            at = []
            while j < len(lines) and atomre.match(lines[j]):
                m = atomre.match(lines[j])
                at.append((SYM[int(m.group(2))], float(m.group(4)), float(m.group(5)), float(m.group(6))))
                j += 1
            if len(at) == 11:
                best = (i+1, at)
    return best

def d(A, i, j): return math.dist(A[i-1][1:4], A[j-1][1:4])

def ang(A, i, j, k):
    u = [A[i-1][t]-A[j-1][t] for t in (1,2,3)]; w = [A[k-1][t]-A[j-1][t] for t in (1,2,3)]
    c = sum(u[t]*w[t] for t in range(3))/(math.dist([0,0,0],u)*math.dist([0,0,0],w))
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))

def dih(A, i, j, k, l):
    def v(p, q): return [A[q-1][t]-A[p-1][t] for t in (1,2,3)]
    def cr(a, b): return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
    b1, b2, b3 = v(i,j), v(j,k), v(k,l)
    n1, n2 = cr(b1,b2), cr(b2,b3)
    nb = math.dist([0,0,0], b2)
    m = cr(n1, [x/nb for x in b2])
    return math.degrees(math.atan2(sum(m[t]*n2[t] for t in range(3)), sum(n1[t]*n2[t] for t in range(3))))

BONDS = [(1,3),(1,8),(1,9),(2,3),(2,4),(2,5),(2,6),(7,8),(7,9),(7,3),(7,10),(9,11)]
ANGS = [(1,3,2),(2,3,7),(3,7,9),(3,7,8),(7,9,11),(1,8,7),(8,7,9),(3,7,10)]
DIHS = [(11,9,7,8),(11,9,7,3),(4,2,3,7)]

def table(tag, A):
    print(tag+' bonds: '+' '.join('%d-%d %.3f' % (i,j,d(A,i,j)) for i,j in BONDS))
    print(tag+' angles: '+' '.join('%d-%d-%d %.1f' % (i,j,k,ang(A,i,j,k)) for i,j,k in ANGS))
    print(tag+' dihedrals: '+' '.join('%d-%d-%d-%d %.1f' % t[:4]+(dih(A,*t),) if False else '%d-%d-%d-%d %.1f' % (t[0],t[1],t[2],t[3],dih(A,*t)) for t in DIHS))

if __name__ == '__main__':
    ref = rd_xyz(sys.argv[1])
    (lno, fr) = rd_last_input_orientation(sys.argv[2])
    print('reference = %s (11 atoms, %s)' % (sys.argv[1], [a[0] for a in ref]))
    print('frame     = %s last Input orientation @L%d (%s)' % (sys.argv[2], lno, [a[0] for a in fr]))
    print('element orders identical: %s' % ([a[0] for a in ref] == [a[0] for a in fr]))
    table('REF ', ref); table('FRM ', fr)
    db = max(abs(d(ref,i,j)-d(fr,i,j)) for i,j in BONDS)
    print('max |d(bond)| deviation = %.4f A' % db)
    da = max(abs(ang(ref,*t)-ang(fr,*t)) for t in ANGS)
    print('max |d(angle)| deviation = %.2f deg' % da)
    ddd = max(abs(dih(ref,*t)-dih(fr,*t)) for t in DIHS)
    print('max |d(dihedral)| deviation = %.2f deg' % ddd)
    # per-atom deviation after centroid + 3-anchor alignment (Na, C4, O3)
    import itertools
    def centroid(X): return [sum(a[t] for a in X)/len(X) for t in (1,2,3)]
    def sub(X, c): return [[a[0]]+[a[t]-c[t-1] for t in (1,2,3)] for a in X]
    cR, cF = centroid(ref), centroid(fr)
    R, F = sub(ref, cR), sub(fr, cF)
    i0, i1, i2 = 0, 6, 2
    def frame_of(X):
        u = [X[i1][t]-X[i0][t] for t in (1,2,3)]
        nu = math.dist([0,0,0], u); u = [x/nu for x in u]
        w = [X[i2][t]-X[i0][t] for t in (1,2,3)]
        dot = sum(u[t]*w[t] for t in range(3)); w = [w[t]-dot*u[t] for t in range(3)]
        nw = math.dist([0,0,0], w); w = [x/nw for x in w] if nw > 1e-9 else [0,0,0]
        v = [u[1]*w[2]-u[2]*w[1], u[2]*w[0]-u[0]*w[2], u[0]*w[1]-u[1]*w[0]]
        return u, w, v
    uR, wR, vR = frame_of(R); uF, wF, vF = frame_of(F)
    def to_std(X, u, w, v):
        return [[a[0]]+[sum(a[t+1]*c[t] for t in range(3)) for c in (u, w, v)] for a in X]
    Rs, Fs = to_std(R, uR, wR, vR), to_std(F, uF, wF, vF)
    devs = [math.dist(Rs[i][1:4], Fs[i][1:4]) for i in range(11)]
    print('per-atom deviation after 3-anchor (Na,C4,O3) alignment: max %.3f A, mean %.3f A, argmax atom %d'
          % (max(devs), sum(devs)/len(devs), devs.index(max(devs))+1))
    print('per-atom: '+' '.join('%d:%.2f' % (i+1, devs[i]) for i in range(11)))
