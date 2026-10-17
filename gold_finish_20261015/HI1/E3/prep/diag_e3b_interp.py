#!/usr/bin/env python3
"""Diagnostic for the E3b Cartesian-interpolation gate failure (lambda 0.30-0.90).

Prints, per lambda: R(C2-N4), R(C2-O25), R(N4-H26), global minsep (pair), the
smallest HEAVY-atom separation (pair) and every pair closer than 1.20 A.
Read-only; writes nothing. Usage: diag_e3b_interp.py R.xyz P.xyz
"""
import sys, math

def rd(p):
    L = open(p).read().splitlines()
    n = int(L[0].split()[0])
    return [[x.split()[0]] + [float(v) for v in x.split()[1:4]] for x in L[2:2 + n]]

def d(A, i, j):
    return math.dist(A[i - 1][1:], A[j - 1][1:])

R = rd(sys.argv[1]); P = rd(sys.argv[2])
n = len(R)
heavy = [i + 1 for i in range(n) if R[i][0] != 'H']
print("natoms", n, "heavy", len(heavy))
print("lam  R(2,4)  R(2,25) R(25,26) minsep(pair)  minHeavy(pair)  contacts<1.20")
for k in range(30, 91, 2):
    lam = k / 100.0
    A = [[R[i][0]] + [R[i][c] + lam * (P[i][c] - R[i][c]) for c in (1, 2, 3)] for i in range(n)]
    # H26 on N4 at 1.05 A away from C2 (v4 rule)
    N4, C2 = A[3], A[1]
    u = [N4[c] - C2[c] for c in (1, 2, 3)]
    m = math.sqrt(sum(x * x for x in u)) or 1.0
    for c in (1, 2, 3):
        A[25][c] = N4[c] + 1.05 * u[c - 1] / m
    best = (9e9, 0, 0); bh = (9e9, 0, 0); bad = []
    for i in range(n):
        for j in range(i + 1, n):
            dd = math.dist(A[i][1:], A[j][1:])
            if dd < best[0]:
                best = (dd, i + 1, j + 1)
            if (i + 1) in heavy and (j + 1) in heavy and dd < bh[0]:
                bh = (dd, i + 1, j + 1)
            if dd < 1.20:
                bad.append("%d-%d:%.2f" % (i + 1, j + 1, dd))
    print("%.2f %8.4f %7.4f %7.4f  %.4f(%d-%d)   %.4f(%d-%d)   %s" % (
        lam, d(A, 2, 4), d(A, 2, 25), d(A, 25, 26), best[0], best[1], best[2],
        bh[0], bh[1], bh[2], " ".join(bad[:6]) if bad else "-"))
