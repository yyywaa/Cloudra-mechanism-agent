#!/usr/bin/env python3
"""Build the authorised attempt-2 E1 guess: machine linear mix 2:1 of the converged
scan frames p6 (0.667) and p5 (0.333), in reactant/working order.

Sources (both on disk, unmodified):
  p6 -> E1/e1_tsguess_revscan_p6_reactantorder.xyz
  p5 -> E1/e1_tsguess_revscan_p5_reactantorder.xyz
This is a MACHINE CONSTRUCTION (per-atom weighted linear combination), not a scan frame
and not an interpolation of I1/RC.
"""
import math, sys

def rd(p):
    L = open(p).read().split('\n')
    n = int(L[0].split()[0])
    out = []
    for l in L[2:2+n]:
        q = l.split()
        out.append((q[0], float(q[1]), float(q[2]), float(q[3])))
    return out

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
assert [a[0] for a in p6] == [a[0] for a in p5], 'element order mismatch'
mix = [(p6[i][0], W*p6[i][1]+(1-W)*p5[i][1], W*p6[i][2]+(1-W)*p5[i][2], W*p6[i][3]+(1-W)*p5[i][3]) for i in range(11)]
with open(out, 'w') as f:
    f.write('11\nNY3 E1 attempt-2 guess: MACHINE linear mix p6:p5 = 2:1 (reactant order); sources p6=%s 0.667 + p5=%s 0.333\n' % (sys.argv[1], sys.argv[2]))
    for a in mix:
        f.write('%-2s %14.8f %14.8f %14.8f\n' % a)
for tag, A in (('p6', p6), ('p5', p5), ('mix', mix)):
    print('%-4s C4-O1 %8.4f  Na-O1 %8.4f  C4=O5 %7.4f  C4-O3 %7.4f  O1-H6 %6.4f  Na-O5 %7.4f  Na-O3 %7.4f  D(H8-C2-O3-C4) %8.2f  D(H6-O1-C4-O3) %8.2f'
          % (tag, d(A,6,2), d(A,1,2), d(A,6,7), d(A,6,5), d(A,2,3), d(A,1,7), d(A,1,5), dih(A,8,4,5,6), dih(A,3,2,6,5)))
