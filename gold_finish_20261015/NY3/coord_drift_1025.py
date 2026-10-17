#!/usr/bin/env python3
"""Drift of the two soft coordinates over the LAST N optimisation steps of a Gaussian
optimisation log, read from the log's own 'Input orientation' blocks (input atom order).

Atom numbering (prep/i2.xyz order, as in the job .gjf):
 1 Na | 2 C(OMe) | 3 O3(OMe) | 4,5,6 H(OMe) | 7 C4 | 8 O5(carbonyl) | 9 O1(hydroxyl) |
 10 H(C4) | 11 H6(on O1)
Soft coordinates: methyl torsion D(4-2-3-7), hydroxyl torsion D(11-9-7-8).
"""
import math, re, sys

def dih(A, i, j, k, l):
    def v(p, q): return [A[q-1][t]-A[p-1][t] for t in (1,2,3)]
    def cr(a, b): return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
    b1, b2, b3 = v(i,j), v(j,k), v(k,l)
    n1, n2 = cr(b1,b2), cr(b2,b3)
    nb = math.dist([0,0,0], b2)
    m = cr(n1, [x/nb for x in b2])
    return math.degrees(math.atan2(sum(m[t]*n2[t] for t in range(3)), sum(n1[t]*n2[t] for t in range(3))))

lines = open(sys.argv[1], errors='replace').read().split('\n')
atomre = re.compile(r'^\s*(\d+)\s+(\d+)\s+(\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s*$')
blocks = []
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
            blocks.append((i+1, at))
N = int(sys.argv[2]) if len(sys.argv) > 2 else 15
sel = blocks[-N:]
print('log=%s  total Input-orientation blocks=%d  showing last %d' % (sys.argv[1], len(blocks), len(sel)))
vals = []
for k, (ln, A) in enumerate(sel):
    dm = dih(A, 4, 2, 3, 7); do = dih(A, 11, 9, 7, 8)
    vals.append((ln, dm, do))
    print('  frame %2d  L%-6d  D(4-2-3-7) = %8.2f   D(11-9-7-8) = %8.2f' % (k+1, ln, dm, do))
def pp(idx, n):
    # circular spread: deviations from the last value mapped into (-180, 180]
    v = [x[idx] for x in vals[-n:]]
    dev = [((x - v[-1] + 180.0) % 360.0) - 180.0 for x in v]
    return max(dev) - min(dev)
print('last value      : D(Me) %8.2f   D(OH) %8.2f' % (vals[-1][1], vals[-1][2]))
print('peak-to-peak last 5 steps : D(Me) %6.2f   D(OH) %6.2f' % (pp(1,5), pp(2,5)))
print('peak-to-peak last 10 steps: D(Me) %6.2f   D(OH) %6.2f' % (pp(1,10), pp(2,10)))
print('verdict: %s' % ('DRIFT >10 deg in last 10 steps -> conformationally unconverged' if max(pp(1,10), pp(2,10)) > 10.0 else '<=10 deg in last 10 steps -> geometrically settled'))
