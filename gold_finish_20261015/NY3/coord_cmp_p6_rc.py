#!/usr/bin/env python3
"""Compare job 1023 scan-point geometries (index-safe Input orientation, job .gjf order)
with the RC reference (reactant order) after the verified product<->reactant atom mapping.
0-based list indices for the reactant order (Na,O1,H6,C2,O3,C4,O5,H8,H9,H10,H11):
  0 Na | 1 O1 | 2 H6 | 3 C2 | 4 O3 | 5 C4 | 6 O5 | 7,8,9 H(Me) | 10 H(formyl)
Mapping J: r_k = j[J[k-1]]  (== E1_ATOM_MAP.md atom_map [1,4,5,6,2,7,8,9,10,11,3]).
Helper indices for ang()/dih() are 1-BASED.
"""
import math, re, sys

J = [1, 5, 11, 2, 3, 4, 6, 7, 8, 9, 10]
I1 = -467.004842486
RC = -466.986564979
K = 627.509474

def xy(a, b):
    return math.dist(a[1:4], b[1:4])

def ang(A, i, j, k):
    u = [A[i-1][t]-A[j-1][t] for t in (1, 2, 3)]
    w = [A[k-1][t]-A[j-1][t] for t in (1, 2, 3)]
    c = sum(u[t]*w[t] for t in range(3)) / (math.dist([0,0,0], u)*math.dist([0,0,0], w))
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))

def dih(A, i, j, k, l):
    def v(p, q): return [A[q-1][t]-A[p-1][t] for t in (1, 2, 3)]
    def cr(a, b): return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
    b1, b2, b3 = v(i, j), v(j, k), v(k, l)
    n1, n2 = cr(b1, b2), cr(b2, b3)
    nb = math.dist([0,0,0], b2)
    m = cr(n1, [x/nb for x in b2])
    return math.degrees(math.atan2(sum(m[t]*n2[t] for t in range(3)), sum(n1[t]*n2[t] for t in range(3))))

def xyz_read(path):
    ls = open(path).read().split('\n')
    n = int(ls[0].split()[0])
    return [(p[0], float(p[1]), float(p[2]), float(p[3])) for p in (l.split() for l in ls[2:2+n])]

def blocks(path):
    lines = open(path, errors='replace').read().split('\n')
    atomre = re.compile(r'^\s*(\d+)\s+(\d+)\s+(\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s*$')
    out = []
    for i, l in enumerate(lines):
        if 'Input orientation:' in l:
            j = i+1
            while j < len(lines) and not atomre.match(lines[j]) and j-i <= 12:
                j += 1
            at = []
            while j < len(lines) and atomre.match(lines[j]):
                m = atomre.match(lines[j])
                at.append(('X', float(m.group(4)), float(m.group(5)), float(m.group(6))))
                j += 1
            if len(at) == 11:
                out.append((i+1, at))
    return lines, out

def report(tag, A, energy=None):
    row = '%-6s' % tag
    if energy is not None:
        row += ' %14.9f  I1%+6.2f  RC%+6.2f' % (energy, (energy-I1)*K, (energy-RC)*K)
    row += (' | d(O1-C4) %5.3f  Na-O1 %5.3f  C4=O5 %5.3f  C4-O3 %5.3f  O1-H6 %5.3f  C4-H11 %5.3f'
            ' | ang(Na,O1,H6) %6.2f  ang(C4,O1,H6) %6.2f  d(H6-C4) %5.3f  d(H6-O5) %5.3f'
            ' | Na-O3 %5.3f  Na-O5 %5.3f  Na-C4 %5.3f  D(H6-O1-C4-O3) %7.2f'
            % (xy(A[1], A[5]), xy(A[0], A[1]), xy(A[5], A[6]), xy(A[5], A[4]), xy(A[1], A[2]),
               xy(A[5], A[10]), ang(A, 1, 2, 3), ang(A, 6, 2, 3), xy(A[2], A[5]), xy(A[2], A[6]),
               xy(A[0], A[4]), xy(A[0], A[6]), xy(A[0], A[5]), dih(A, 3, 2, 6, 5)))
    print(row)

rc = xyz_read('gold_finish_20261015/NY3/E1/rc_dft_min_working_order.xyz')
print('RC file element order: %s' % [a[0] for a in rc])
report('RC', rc)

lines, bl = blocks('gold_finish_20261015/NY3/E1/E1_revscan_O1C4.log')
done = [i+1 for i, l in enumerate(lines) if l.strip().startswith('Optimization completed.')]
scf = [(i+1, float(m.group(1))) for i, l in enumerate(lines)
       for m in [re.search(r'SCF Done:\s+E\(RB3LYP\)\s+=\s+(-?\d+\.\d+)', l)] if m]
for p, end in enumerate(done):
    b = [x for x in bl if x[0] < end]
    if not b:
        continue
    j_at = b[-1][1]
    A = [j_at[k-1] for k in J]
    ev = [x for x in scf if x[0] < end][-1][1]
    report('p%d' % (p+1), A, ev)
print('RC energy (job 967) = %.9f ; I1 (job 985/1020) = %.9f' % (RC, I1))
