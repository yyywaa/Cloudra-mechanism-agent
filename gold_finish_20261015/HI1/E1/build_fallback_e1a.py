#!/usr/bin/env python3
"""Build the agreed fallback (a) early-attack frame for HI1_E1a:
interpolate RC_27 (loose H-bond complex) -> carbinolamine_27 along C2-N18,
with the transferring proton H21 kept on the N side. Output XYZ + self-check numbers.
Inputs are on-disk tool-derived frames; nothing is hand-typed."""
import sys, numpy as np

A_PATH = "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split/RC_27_opt_frame.xyz"
B_PATH = "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split/INT1_27_opt_frame.xyz"
OUT    = "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split/E1A_fallback_earlyattack_R210.xyz"
TARGET = 2.10   # Angstrom, R(C2-N18)

def rd(p):
    L = open(p).read().splitlines(); n = int(L[0].split()[0])
    els = []; xyz = []
    for l in L[2:2+n]:
        f = l.split(); els.append(f[0]); xyz.append([float(x) for x in f[1:4]])
    return els, np.array(xyz)

eA, XA = rd(A_PATH); eB, XB = rd(B_PATH)
assert eA == eB, "element order mismatch"
H = np.array([e == "H" for e in eA])
C2, O3, C3, H22, N18, H21 = 1, 2, 3, 9, 17, 26   # 0-based for working-order 2,3,4,10,18,27

def kabsch_full(P_ref, Q_mob, Q_all):
    """Rigid transform from Q (mobile) onto P (reference), fitted on heavy atoms,
    then applied to every atom of Q_all."""
    pm = P_ref.mean(0); qm = Q_mob.mean(0)
    Pc = P_ref - pm; Qc = Q_mob - qm
    V, S, Wt = np.linalg.svd(Pc.T @ Qc)
    d = np.sign(np.linalg.det(V @ Wt))
    D = np.diag([1.0, 1.0, d])
    R = V @ D @ Wt
    return (Q_all - qm) @ R.T + pm

XB_al = kabsch_full(XA[~H], XB[~H], XB)

uA = (XA[H21] - XA[N18]); L_HN = np.linalg.norm(uA); uA = uA / L_HN

def geom(lam):
    X = (1.0 - lam) * XA + lam * XB_al
    X[H21] = X[N18] + L_HN * uA
    return X

def r(X, i, j): return float(np.linalg.norm(X[i] - X[j]))

def f(lam): return r(geom(lam), C2, N18) - TARGET

lo, hi = 0.0, 1.0
assert f(lo) > 0 and f(hi) < 0, (f(lo), f(hi))
for _ in range(200):
    mid = 0.5 * (lo + hi)
    if f(mid) > 0: lo = mid
    else: hi = mid
lam = 0.5 * (lo + hi)
X = geom(lam)

print("RC_27 file :", A_PATH)
print("INT1 file  :", B_PATH)
print("lambda     : %.6f" % lam)
print("R(C2-N18)  : %.4f  (target %.2f)" % (r(X, C2, N18), TARGET))
print("R(C2-O3)   : %.4f" % r(X, C2, O3))
print("R(N18-H21) : %.4f  (held at RC value %.4f)" % (r(X, N18, H21), L_HN))
print("R(O3-H21)  : %.4f" % r(X, O3, H21))
print("R(C2-C3)   : %.4f" % r(X, C2, C3))
print("R(C3-H22)  : %.4f" % r(X, C3, H22))
print("")
print("monotonic R(C2-N18) along the interpolated path:")
prev = None; mono = True
for s in [0.0, 0.1, 0.2, lam, 0.4, 0.6, 0.8, 1.0]:
    val = r(geom(s), C2, N18)
    if prev is not None and val > prev + 1e-9: mono = False
    prev = val
    print("  lambda=%.3f  R(C2-N18)=%.4f" % (s, val))
print("monotonic_decreasing =", mono)

ms, pair = None, None
for i in range(len(X)):
    for j in range(i+1, len(X)):
        d = r(X, i, j)
        if ms is None or d < ms: ms, pair = d, (i+1, j+1)
print("minsep     : %.4f A between atoms %d and %d" % (ms, pair[0], pair[1]))

with open(OUT, "w") as fh:
    fh.write("%d\n" % len(X))
    fh.write("E1a fallback (a): RC_27 -> carbinolamine_27 interpolation, lambda=%.4f, R(C2-N18)=%.3f A, H21 kept on N18" % (lam, r(X, C2, N18)))
    fh.write("\n")
    for e, c in zip(eA, X):
        fh.write("%-2s %14.8f %14.8f %14.8f\n" % (e, c[0], c[1], c[2]))
print("written:", OUT)
