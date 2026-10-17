#!/usr/bin/env python3
"""Fallback (a) for HI1_E1a, v5: early-attack frame at R(C2-N18) = 2.10 A.
Construction (all rigid for the acetone fragment, proline + H21 unchanged from RC_27):
 1) rotate the 10-atom acetone fragment about the C2 atom, around the axis perpendicular
    to the (C2, O3, N18) plane, so that the angle O3-C2...N18 becomes the Buergi-Dunitz
    value 110 deg (the carbonyl O then points away from the incoming N-H);
    both rotation senses are tried and the one with the larger O3...H21 clearance is kept;
 2) translate the fragment along the (rotated) C2->N18 direction until R(C2-N18)=2.10 A.
Every internal acetone distance and the proline geometry are preserved exactly;
H21 stays bonded to N18 at the RC_27 value. Inputs are on-disk tool-derived frames."""
import numpy as np
from numpy.linalg import norm

S = "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split"
A_PATH = S + "/RC_27_opt_frame.xyz"
OUT    = S + "/E1A_fallback_earlyattack_R210.xyz"
TARGET = 2.10
THETA  = np.deg2rad(110.0)

L = open(A_PATH).read().splitlines(); n = int(L[0].split()[0])
els = [f.split()[0] for f in L[2:2+n]]
X0 = np.array([[float(x) for x in f.split()[1:4]] for f in L[2:2+n]])
C2, O3, C3, H22, N18, H21 = 1, 2, 3, 9, 17, 26
ACETONE = list(range(0, 10))

def r(Z, i, j): return float(norm(Z[i] - Z[j]))
def ang(Z, i, j, k):
    a = Z[i]-Z[j]; b = Z[k]-Z[j]
    return float(np.arccos(np.clip(a @ b/(norm(a)*norm(b)), -1, 1)))

def rodrigues(axis, th):
    k = axis/norm(axis)
    K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
    return np.eye(3) + np.sin(th)*K + (1-np.cos(th))*(K @ K)

v1 = X0[O3]-X0[C2]; v2 = X0[N18]-X0[C2]
axis = np.cross(v1, v2); axis = axis/norm(axis)
phi0 = ang(X0, O3, C2, N18)
print("RC_27: R(C2-N18)=%.4f  angle O3-C2...N18=%.1f deg  R(O3-H21)=%.4f  minsep=%.4f" % (
    r(X0, C2, N18), np.rad2deg(phi0), r(X0, O3, H21),
    min(norm(X0[i]-X0[j]) for i in range(n) for j in range(i+1, n))))

cands = []
for sgn in (+1.0, -1.0):
    dth = sgn*(THETA - phi0)
    Rot = rodrigues(axis, dth)
    X = X0.copy()
    X[ACETONE] = X0[C2] + (X0[ACETONE]-X0[C2]) @ Rot.T
    u = (X[N18]-X[C2])/norm(X[N18]-X[C2])
    delta = r(X, C2, N18) - TARGET
    X[ACETONE] = X[ACETONE] + delta*u
    ms = min(norm(X[i]-X[j]) for i in range(n) for j in range(i+1, n))
    cands.append((sgn, Rot, X, ms, r(X, O3, H21), r(X, C2, N18), r(X, O3, N18)))
    print("sense %+d: dtheta=%7.2f deg -> R(C2-N18)=%.4f  R(O3-H21)=%.4f  R(O3-N18)=%.4f  minsep=%.4f" % (
        sgn, np.rad2deg(dth), cands[-1][5], cands[-1][4], cands[-1][6], ms))

good = [c for c in cands if c[3] >= 0.9]
if not good:
    raise SystemExit("no rotation sense gives minsep >= 0.9 A")
chosen = max(good, key=lambda c: c[4])
sgn, Rot, X, ms, oh, rcn, on = chosen
print("")
print("chosen sense %+d (max O3...H21 clearance)" % sgn)
for nm, (i, j) in [("R(C2-N18)", (C2, N18)), ("R(C2-O3)", (C2, O3)), ("R(N18-H21)", (N18, H21)),
                   ("R(O3-H21)", (O3, H21)), ("R(O3-N18)", (O3, N18)), ("R(C1-C2)", (0, 1)),
                   ("R(C2-C3)", (C2, C3)), ("R(C3-H22)", (C3, H22)), ("R(O13-H19)", (12, 18))]:
    print("  %-12s: %.4f" % (nm, r(X, i, j)))
print("  angle O3-C2...N18: %.1f deg" % np.rad2deg(ang(X, O3, C2, N18)))

print("")
print("lambda-style table (fraction of the final translation only, rotation applied):")
rows = []
Xrot = X0.copy(); Xrot[ACETONE] = X0[C2] + (X0[ACETONE]-X0[C2]) @ Rot.T
u = (Xrot[N18]-Xrot[C2])/norm(Xrot[N18]-Xrot[C2])
dtot = r(Xrot, C2, N18) - TARGET
for fr in [0.0, 0.2, 0.4, 0.6, 0.8, 0.9, 1.0]:
    Z = Xrot.copy(); Z[ACETONE] = Xrot[ACETONE] + fr*dtot*u
    rows.append((fr, r(Z, C2, N18), min(norm(Z[i]-Z[j]) for i in range(n) for j in range(i+1, n))))
for fr, val, m in rows:
    print("  f=%.1f  R(C2-N18)=%.4f  minsep=%.4f" % (fr, val, m))
sv = [row[1] for row in rows]
print("strictly monotonic decreasing =", all(sv[i] > sv[i+1] for i in range(len(sv)-1)))

ms2 = None; pr = None
for i in range(n):
    for j in range(i+1, n):
        d = r(X, i, j)
        if ms2 is None or d < ms2: ms2, pr = d, (i+1, els[i], j+1, els[j])
print("minsep of the delivered frame: %.4f A between atom %d(%s) and %d(%s)" % (ms2, pr[0], pr[1], pr[2], pr[3]))

with open(OUT, "w") as fh:
    fh.write("%d\n" % n)
    fh.write("E1a fallback(a) early attack: RC_27 acetone rotated about C2 to O3-C2...N18=110 deg (sense %+d) then slid along C2->N18; R(C2-N18)=%.3f A; proline+H21 unchanged from RC_27" % (sgn, r(X, C2, N18)))
    fh.write("\n")
    for e, c in zip(els, X):
        fh.write("%-2s %14.8f %14.8f %14.8f\n" % (e, c[0], c[1], c[2]))
print("written:", OUT)
