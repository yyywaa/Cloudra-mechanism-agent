#!/usr/bin/env python3
"""Attempt-2 E1 guess, construction A (authorised): take the converged scan frame p6 and
translate O1 together with H6 rigidly along the C4->O1 axis toward C4 until
r(C4-O1) = 2.1271 A. Every other atom and every other internal coordinate is unchanged.

Rationale: minimal, chemically clean perturbation that sits in the 2.03-2.18 A crossing
window between branch 支-I1 and branch 支-RC, with the O-H bond intact and the Na+
coordination sphere uncompressed (contrast: per-atom linear position mixing collapses
O1-H6 to 0.508 A and Na-O5 to 1.956 A).
"""
import math, sys

def rd(p):
    L = open(p).read().split('\n')
    n = int(L[0].split()[0])
    return [(q[0], float(q[1]), float(q[2]), float(q[3])) for q in (l.split() for l in L[2:2+n])]

def d(A, i, j):
    return math.dist(A[i-1][1:4], A[j-1][1:4])

def dih(A, i, j, k, l):
    def v(p, q): return [A[q-1][t]-A[p-1][t] for t in (1, 2, 3)]
    def cr(a, b): return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
    b1, b2, b3 = v(i, j), v(j, k), v(k, l)
    n1, n2 = cr(b1, b2), cr(b2, b3)
    nb = math.dist([0,0,0], b2)
    m = cr(n1, [x/nb for x in b2])
    return math.degrees(math.atan2(sum(m[t]*n2[t] for t in range(3)), sum(n1[t]*n2[t] for t in range(3))))

src, target, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
A = rd(src)
C4, O1 = A[5][1:4], A[1][1:4]
r0 = math.dist(C4, O1)
u = [(O1[t]-C4[t])/r0 for t in range(3)]          # unit C4 -> O1
shift = r0 - target                                # move O1/H6 toward C4
B = [list(a) for a in A]
for idx in (1, 2):                                 # O1 = atom 2, H6 = atom 3 (1-based)
    for t in range(3):
        B[idx][t+1] = A[idx][t+1] - shift*u[t]
B = [tuple(b) for b in B]
with open(out, 'w') as f:
    f.write('11\nNY3 E1 attempt-2 guess (construction A): p6 with O1+H6 rigidly translated %.5f A along the C4->O1 axis to r(C4-O1)=%.4f A; all other atoms/internal coordinates unchanged. source=%s\n' % (shift, target, src))
    for a in B:
        f.write('%-2s %14.8f %14.8f %14.8f\n' % a)
BONDS = {(1,2),(2,3),(2,6),(4,5),(5,6),(6,7),(4,8),(4,9),(4,10),(6,11),(1,5),(1,7)}
print('shift = %.5f A (C4->O1 axis); elements identical: %s' % (shift, [a[0] for a in A] == [b[0] for b in B]))
for tag, X in (('p6', A), ('A', B)):
    print('%-3s C4-O1 %8.4f  O1-H6 %6.4f  Na-O1 %7.4f  Na-O5 %7.4f  Na-O3 %7.4f  C4=O5 %7.4f  C4-O3 %7.4f  C2-H8 %5.3f  C4-H11 %5.3f  D(H8-C2-O3-C4) %7.2f  D(H6-O1-C4-O3) %8.2f'
          % (tag, d(X,6,2), d(X,2,3), d(X,1,2), d(X,1,7), d(X,1,5), d(X,6,7), d(X,6,5), d(X,4,8), d(X,6,11), dih(X,8,4,5,6), dih(X,3,2,6,5)))
best = (9e9, None)
for i in range(1, 12):
    for j in range(i+1, 12):
        if (i, j) in BONDS or (j, i) in BONDS:
            continue
        dd = d(B, i, j)
        if dd < best[0]:
            best = (dd, (i, j))
print('min non-bonded separation = %.3f A (pair %s)' % best)
