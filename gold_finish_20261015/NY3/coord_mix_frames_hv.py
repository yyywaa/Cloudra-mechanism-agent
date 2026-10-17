#!/usr/bin/env python3
"""Attempt-2 E1 guess, corrected construction: mix ONLY the heavy-atom positions 2:1
(p6 0.667 + p5 0.333) and re-attach every hydrogen rigidly to its p6 parent atom.

Why: a naive per-atom 2:1 mix of ALL 11 atoms collapses the O1-H6 bond (0.508 A) and
shortens Na-O5 to 1.956 A, because H6 sits on opposite sides of O1 in p5 and p6
(hydroxyl torsion D(H6-O1-C4-O3) = +119.2 deg in p6 vs -56.1 deg in p5). The authorised
target readouts (O1-H6 ~0.968) require the O-H bond to stay intact.

Heavy atoms (1-based, reactant order): 1 Na, 2 O1, 4 C2, 5 O3, 6 C4, 7 O5.
Hydrogens + p6 parent: 3<-2, 8<-4, 9<-4, 10<-4, 11<-6.
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

p6 = rd(sys.argv[1]); p5 = rd(sys.argv[2]); W = 2.0/3.0; out = sys.argv[3]
assert [a[0] for a in p6] == [a[0] for a in p5]
HEAVY = [1, 2, 4, 5, 6, 7]
PARENT = {3: 2, 8: 4, 9: 4, 10: 4, 11: 6}
mix = [None] * 11
for i in HEAVY:
    mix[i-1] = (p6[i-1][0],) + tuple(W*p6[i-1][t] + (1-W)*p5[i-1][t] for t in (1, 2, 3))
for i, par in PARENT.items():
    mix[i-1] = (p6[i-1][0],) + tuple(mix[par-1][t] + (p6[i-1][t] - p6[par-1][t]) for t in (1, 2, 3))
with open(out, 'w') as f:
    f.write('11\nNY3 E1 attempt-2 guess: MACHINE construction - heavy atoms linear-mixed p6:p5 = 2:1, all H re-attached rigidly to their p6 parent (O-H kept intact). sources p6=%s 0.667 + p5=%s 0.333\n' % (sys.argv[1], sys.argv[2]))
    for a in mix:
        f.write('%-2s %14.8f %14.8f %14.8f\n' % a)
for tag, A in (('p6', p6), ('p5', p5), ('mix', mix)):
    print('%-4s C4-O1 %8.4f  Na-O1 %8.4f  C4=O5 %7.4f  C4-O3 %7.4f  O1-H6 %6.4f  Na-O5 %7.4f  Na-O3 %7.4f  D(H8-C2-O3-C4) %8.2f  D(H6-O1-C4-O3) %8.2f  C2-H8 %5.3f  C4-H11 %5.3f'
          % (tag, d(A,6,2), d(A,1,2), d(A,6,7), d(A,6,5), d(A,2,3), d(A,1,7), d(A,1,5), dih(A,8,4,5,6), dih(A,3,2,6,5), d(A,4,8), d(A,6,11)))
