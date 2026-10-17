#!/usr/bin/env python3
"""Search rigid internal-coordinate ops (for the internal_coordinates transform tool) that turn
prep/i2.xyz into an E3 proton-transfer guess: d(O1-H6) = d(H6-O3) ~ 1.25 A with C4...O3 kept at the
I2 (non-bonded) value.  Pure geometry search; writes NO coordinates (the chemistry tool does that)."""
import math, sys, itertools
import numpy as np

XYZ = "gold_finish_20261015/NY3/prep/i2.xyz"

def read_xyz(p):
    L = open(p).read().splitlines()
    n = int(L[0].split()[0])
    el = []; X = []
    for l in L[2:2+n]:
        s = l.split(); el.append(s[0]); X.append([float(s[1]), float(s[2]), float(s[3])])
    return el, np.array(X)

def rot(P, ap, u, deg):
    a = math.radians(deg)
    v = P - ap
    par = np.outer(v @ u, u)
    per = v - par
    cr = np.cross(np.tile(u, (len(P), 1)), per)
    return ap + par + per*math.cos(a) + cr*math.sin(a)

def rot1(p, ap, u, deg):
    a = math.radians(deg)
    v = p - ap
    par = u * (v @ u)
    per = v - par
    return ap + par + per*math.cos(a) + np.cross(u, per)*math.sin(a)

el, X = read_xyz(XYZ)
# 1-based: 1 Na, 2 C2, 3 O3, 4-6 H(Me), 7 C4, 8 O5, 9 O1, 10 H(C4), 11 H6
Na, C2, O3, C4, O5, O1, H6 = X[0], X[1], X[2], X[6], X[7], X[8], X[10]

# --- op1: rotate methoxide (atoms 2..6, 0-based 1..5) about the Na...C4 line so that O1...O3 -> ~2.50
u1 = (C4 - Na)/np.linalg.norm(C4 - Na)
best = None
for deg in np.arange(-180, 180.0001, 0.02):
    O3n = rot1(O3, Na, u1, deg)
    d = np.linalg.norm(O1 - O3n)
    if best is None or abs(d - 2.50) < best[0]:
        best = (abs(d - 2.50), deg, O3n, d)
_, bestdeg, O3n, d13 = best
print("op1: rotate atoms [2,3,4,5,6] about axis_atoms [1,7] by %.2f deg -> |O1-O3| = %.3f" % (bestdeg, d13))
X1 = X.copy()
X1[[1,2,3,4,5]] = rot(X[[1,2,3,4,5]], Na, u1, bestdeg)
O1n = X1[8]; O3n = X1[2]; H6n = X1[10]; C4n = X1[6]; Nan = X1[0]
print("  after op1: |Na-O3|=%.3f |C4...O3|=%.3f |O1-H6|=%.3f |O3...H6|=%.3f" % (
    np.linalg.norm(Nan-O3n), np.linalg.norm(C4n-O3n), np.linalg.norm(O1n-H6n), np.linalg.norm(O3n-H6n)))

T = O1n + 1.25*(O3n-O1n)/np.linalg.norm(O3n-O1n)
print("target T: |T-O1|=%.4f |T-O3|=%.4f  (required |H6-T|=%.3f)" % (
    np.linalg.norm(T-O1n), np.linalg.norm(T-O3n), np.linalg.norm(T-H6n)))

# --- search: op2 rotate [11] about (i,j) by a1, then op3 rotate [11] about (k,l) by a2  -> H6 at T
lines = [(i, j, X1[i], (X1[j]-X1[i])/np.linalg.norm(X1[j]-X1[i])) for i in range(11) for j in range(11) if i != j]
hits = []
for (i, j, ap, u) in lines:
    vp = H6n - ap; pp = vp - u*(vp @ u); rp = np.linalg.norm(pp)
    for a1 in range(0, 360, 3):
        p1 = rot1(H6n, ap, u, a1)
        for (k, l, ap2, u2) in lines:
            v1 = p1 - ap2; q1 = v1 - u2*(v1 @ u2); r1 = np.linalg.norm(q1)
            vt = T - ap2; qt = vt - u2*(vt @ u2); rt = np.linalg.norm(qt)
            if abs(r1 - rt) > 0.02: continue
            c = float(q1 @ qt)/(r1*rt)
            if c < -1.0000001 or c > 1.0000001: continue
            a2 = math.degrees(math.acos(max(-1.0, min(1.0, c))))
            if float(np.dot(np.cross(q1, qt), u2)) < 0: a2 = -a2
            if np.linalg.norm(rot1(p1, ap2, u2, a2) - T) < 0.005:
                hits.append((i+1, j+1, a1, k+1, l+1, round(a2, 2)))
print("two-rotation hits:", len(hits))
for h in hits[:25]:
    print("   rot[11] ax(%d,%d) %d deg  then rot[11] ax(%d,%d) %.2f deg" % h)
