#!/usr/bin/env python3
"""Fallback (a) for HI1_E1a, v3: RIGID-BODY interpolation of the acetone fragment.
The proline fragment and the transferring proton H21 are taken unchanged from RC_27
(so H21 stays on N18), while the 10-atom acetone fragment is moved as a rigid body
from its RC position/orientation towards its carbinolamine position/orientation
(centroid linear interpolation + rotation slerp). lambda is solved so that
R(C2-N18) = 2.10 A. All internal acetone distances are therefore preserved exactly.
Input coordinates come from on-disk tool-derived frames; nothing is hand-typed."""
import numpy as np
from numpy.linalg import norm

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
C2, O3, C3, H22, N18, H21 = 1, 2, 3, 9, 17, 26
ACETONE = list(range(0, 10))
PROL_HEAVY = [10, 11, 12, 13, 14, 15, 16, 17]

def kabsch_apply(ref, mob, pts):
    pm = ref.mean(0); qm = mob.mean(0)
    V, Sv, Wt = np.linalg.svd((ref - pm).T @ (mob - qm))
    d = np.sign(np.linalg.det(V @ Wt))
    R = V @ np.diag([1.0, 1.0, d]) @ Wt
    return (pts - qm) @ R.T + pm

XB_al = kabsch_apply(XA[PROL_HEAVY], XB[PROL_HEAVY], XB)

def kabsch_R(P, Q):
    """rotation R with Q ~ P @ R.T, fitted on the given point sets"""
    pc = P - P.mean(0); qc = Q - Q.mean(0)
    V, Sv, Wt = np.linalg.svd(pc.T @ qc)
    d = np.sign(np.linalg.det(V @ Wt))
    return V @ np.diag([1.0, 1.0, d]) @ Wt

PA = XA[ACETONE]; PB = XB_al[ACETONE]
cA = PA.mean(0); cB = PB.mean(0)
Rrel = kabsch_R(PA, PB)          # maps (x - cA) onto (y - cB) via  y = cB + (x-cA) @ Rrel.T
print("acetone rigid fit: max internal-distance residual = %.2e A" % max(
    abs(norm(PA[i]-PA[j]) - norm(PB[i]-PB[j])) for i in range(10) for j in range(i+1,10)))

def logm(Rm):
    w, V = np.linalg.eig(Rm)
    idx = int(np.argmin(np.abs(w - 1.0)))
    axis = np.real(V[:, idx]); axis = axis / norm(axis)
    ang = np.arccos(np.clip((np.trace(Rm) - 1.0) / 2.0, -1.0, 1.0))
    if np.dot(axis, np.array([0., 0., 1.])) < 0: axis = -axis
    return axis * ang

def expm(v):
    th = norm(v)
    if th < 1e-12: return np.eye(3)
    k = v / th; K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
    return np.eye(3) + np.sin(th) * K + (1 - np.cos(th)) * (K @ K)

logv = logm(Rrel)

def geom(lam):
    X = XA.copy()
    c = (1.0 - lam) * cA + lam * cB
    Rl = expm(lam * logv)
    X[ACETONE] = c + (PA - cA) @ Rl.T
    return X

def r(X, i, j): return float(norm(X[i] - X[j]))

f = lambda lam: r(geom(lam), C2, N18) - TARGET
print("f(0)=%.4f  f(1)=%.4f" % (f(0.0), f(1.0)))
lo, hi = 0.0, 1.0
for _ in range(200):
    mid = 0.5 * (lo + hi)
    if f(mid) > 0: lo = mid
    else: hi = mid
lam = 0.5 * (lo + hi)
X = geom(lam)

print("lambda            : %.6f" % lam)
for nm, (i, j) in [("R(C2-N18)", (C2, N18)), ("R(C2-O3)", (C2, O3)), ("R(N18-H21)", (N18, H21)),
                   ("R(O3-H21)", (O3, H21)), ("R(C1-C2)", (0, 1)), ("R(C2-C3)", (C2, C3)),
                   ("R(C3-H22)", (C3, H22)), ("R(O13-H19)", (12, 18))]:
    print("%-12s: %.4f" % (nm, r(X, i, j)))
print("")
print("lambda table:")
prev = None; mono = True; rows = []
for s in [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, lam, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]:
    Xs = geom(s)
    val = r(Xs, C2, N18)
    ms = min(norm(Xs[i] - Xs[j]) for i in range(27) for j in range(i+1, 27))
    rows.append((s, val, ms))
for s, val, ms in rows:
    print("  lambda=%.3f  R(C2-N18)=%.4f  minsep=%.4f" % (s, val, ms))
sv = [row[1] for row in sorted(rows)]
mono = all(sv[i] >= sv[i+1] - 1e-9 for i in range(len(sv)-1))
print("monotonic decreasing over ascending lambda =", mono)
msc = min(row[2] for row in rows)
print("min minsep over sampled lambdas = %.4f" % msc)

with open(OUT, "w") as fh:
    fh.write("%d\n" % len(X))
    fh.write("E1a fallback(a): proline+H21 from RC_27; acetone rigid-body interp (centroid+slerp) to carbinolamine; lambda=%.4f; R(C2-N18)=%.3f A" % (lam, r(X, C2, N18)))
    fh.write("\n")
    for e, c in zip(eA, X):
        fh.write("%-2s %14.8f %14.8f %14.8f\n" % (e, c[0], c[1], c[2]))
print("written:", OUT)
