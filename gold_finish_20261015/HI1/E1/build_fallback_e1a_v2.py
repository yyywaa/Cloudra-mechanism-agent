#!/usr/bin/env python3
"""Fallback (a) for HI1_E1a: early-attack frame with R(C2-N18) = 2.10 A.
Method: superimpose carbinolamine_27 onto RC_27 using the PROLINE heavy atoms only
(the proline fragment barely changes), keep the proline fragment + H21 from RC_27,
and interpolate ONLY the acetone fragment (atoms 1-10) towards its carbinolamine position.
Then solve lambda so that R(C2-N18) = 2.10 A. Proton H21 stays on N18 (RC value).
All coordinates come from on-disk tool-derived frames; nothing is hand-typed."""
import numpy as np

S = "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split"
A_PATH = S + "/RC_27_opt_frame.xyz"
B_PATH = S + "/INT1_27_opt_frame.xyz"
OUT    = S + "/E1A_fallback_earlyattack_R210.xyz"
TARGET = 2.10

def rd(p):
    L = open(p).read().splitlines(); n = int(L[0].split()[0])
    els = []; xyz = []
    for l in L[2:2+n]:
        f = l.split(); els.append(f[0]); xyz.append([float(x) for x in f[1:4]])
    return els, np.array(xyz)

eA, XA = rd(A_PATH); eB, XB = rd(B_PATH)
assert eA == eB
C2, O3, C3, H22, N18, H21 = 1, 2, 3, 9, 17, 26     # 0-based (working order 2,3,4,10,18,27)
ACETONE = list(range(0, 10))                        # working order 1-10 = acetone fragment
PROL_HEAVY = [10, 11, 12, 13, 14, 15, 16, 17]       # working order 11-18 = proline heavy atoms

def kabsch_apply(ref, mob, all_pts):
    pm = ref.mean(0); qm = mob.mean(0)
    Pc = ref - pm; Qc = mob - qm
    V, Sv, Wt = np.linalg.svd(Pc.T @ Qc)
    d = np.sign(np.linalg.det(V @ Wt))
    R = V @ np.diag([1.0, 1.0, d]) @ Wt
    return (all_pts - qm) @ R.T + pm

XB_al = kabsch_apply(XA[PROL_HEAVY], XB[PROL_HEAVY], XB)   # B in A frame (proline-fitted)

def geom(lam):
    X = XA.copy()
    X[ACETONE] = (1.0 - lam) * XA[ACETONE] + lam * XB_al[ACETONE]
    return X

def r(X, i, j): return float(np.linalg.norm(X[i] - X[j]))

f = lambda lam: r(geom(lam), C2, N18) - TARGET
lo, hi = 0.0, 1.0
print("f(0)=%.4f  f(1)=%.4f" % (f(lo), f(hi)))
if f(lo) * f(hi) > 0:
    raise SystemExit("target not bracketed")
for _ in range(200):
    mid = 0.5 * (lo + hi)
    if f(mid) > 0: lo = mid
    else: hi = mid
lam = 0.5 * (lo + hi)
X = geom(lam)

print("lambda            : %.6f" % lam)
print("R(C2-N18)         : %.4f  (target %.2f)" % (r(X, C2, N18), TARGET))
print("R(C2-O3)          : %.4f" % r(X, C2, O3))
print("R(N18-H21)        : %.4f" % r(X, N18, H21))
print("R(O3-H21)         : %.4f" % r(X, O3, H21))
print("R(C1-C2)  (0,1)   : %.4f" % r(X, 0, 1))
print("R(C2-C3)          : %.4f" % r(X, C2, C3))
print("R(C3-H22)         : %.4f" % r(X, C3, H22))
print("R(O13-H19)        : %.4f" % r(X, 12, 18))
print("")
print("R(C2-N18) along the path (lambda ascending):")
prev = None; mono = True
for s in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.639, 0.7, 0.8, 0.9, 1.0]:
    val = r(geom(s), C2, N18)
    if prev is not None and val > prev + 1e-9: mono = False
    prev = val
    print("  lambda=%.3f  R(C2-N18)=%.4f" % (s, val))
print("monotonic_decreasing (sampled, ascending lambda) =", mono)

ms = None; pair = None
for i in range(len(X)):
    for j in range(i+1, len(X)):
        dd = r(X, i, j)
        if ms is None or dd < ms: ms, pair = dd, (i+1, j+1)
print("minsep            : %.4f A between atoms %d and %d" % (ms, pair[0], pair[1]))

with open(OUT, "w") as fh:
    fh.write("%d\n" % len(X))
    fh.write("E1a fallback(a) early attack: proline+H21 from RC_27, acetone interpolated to carbinolamine, lambda=%.4f, R(C2-N18)=%.3f A" % (lam, r(X, C2, N18)))
    fh.write("\n")
    for e, c in zip(eA, X):
        fh.write("%-2s %14.8f %14.8f %14.8f\n" % (e, c[0], c[1], c[2]))
print("written:", OUT)
