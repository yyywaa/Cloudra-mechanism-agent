#!/usr/bin/env python3
"""Fallback (a) for HI1_E1a, v6: early-attack frame at R(C2-N18)=2.10 A.
Rigid acetone fragment (atoms 1-10) + separately handled transferring proton H21.
 1) rotate acetone about C2 around the axis perpendicular to the (C2,O3,N18) plane so that
    angle O3-C2...N18 = 110 deg (Buergi-Dunitz) - both senses tried;
 2) slide the fragment along C2->N18 until R(C2-N18)=2.10 A;
 3) the proton H21 is handled separately: it stays bonded to N18 (1.0228 A, the RC_27 value)
    but its orientation is re-set to point away from the incoming carbonyl group
    (unit vector N18 - midpoint(C2,O3)), i.e. an amine N-H rotation, so that the
    developing C...N contact is not blocked; the resulting H-N-Calpha / H-N-C17 angles
    are reported. Proline heavy atoms are unchanged from RC_27.
Input coordinates come from on-disk tool-derived frames; nothing is hand-typed."""
import numpy as np
from numpy.linalg import norm

S = "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split"
A_PATH = S + "/RC_27_opt_frame.xyz"
OUT    = S + "/E1A_fallback_earlyattack_R210.xyz"
TARGET = 2.10; THETA = np.deg2rad(110.0)

L = open(A_PATH).read().splitlines(); n = int(L[0].split()[0])
els = [f.split()[0] for f in L[2:2+n]]
X0 = np.array([[float(x) for x in f.split()[1:4]] for f in L[2:2+n]])
C2, O3, C3, H22, N18, H21, CA = 1, 2, 3, 9, 17, 26, 13
ACETONE = list(range(0, 10))

def r(Z, i, j): return float(norm(Z[i]-Z[j]))
def ang(Z, i, j, k):
    a = Z[i]-Z[j]; b = Z[k]-Z[j]
    return float(np.rad2deg(np.arccos(np.clip(a @ b/(norm(a)*norm(b)), -1, 1))))
def rodrigues(axis, th):
    k = axis/norm(axis)
    K = np.array([[0,-k[2],k[1]],[k[2],0,-k[0]],[-k[1],k[0],0]])
    return np.eye(3) + np.sin(th)*K + (1-np.cos(th))*(K @ K)

LHN = r(X0, N18, H21)
v1 = X0[O3]-X0[C2]; v2 = X0[N18]-X0[C2]
axis = np.cross(v1, v2); axis = axis/norm(axis)
phi0 = np.deg2rad(ang(X0, O3, C2, N18))
print("RC_27: R(C2-N18)=%.4f  angle O3-C2...N18=%.1f deg  R(O3-H21)=%.4f  R(N18-H21)=%.4f  minsep=%.4f" % (
    r(X0,C2,N18), np.rad2deg(phi0), r(X0,O3,H21), r(X0,N18,H21),
    min(norm(X0[i]-X0[j]) for i in range(n) for j in range(i+1,n))))
print("RC_27 N-H angles: H-N-Calpha=%.1f  H-N-C17=%.1f deg" % (ang(X0,H21,N18,CA), ang(X0,H21,N18,16)))

out = []
for sgn in (+1.0, -1.0):
    Rot = rodrigues(axis, sgn*(THETA-phi0))
    X = X0.copy()
    X[ACETONE] = X0[C2] + (X0[ACETONE]-X0[C2]) @ Rot.T
    u = (X[N18]-X[C2])/norm(X[N18]-X[C2])
    X[ACETONE] = X[ACETONE] + (r(X,C2,N18)-TARGET)*u
    # separate handling of the transferring proton
    mid = 0.5*(X[C2]+X[O3])
    d = X[N18]-mid; d = d/norm(d)
    X[H21] = X[N18] + LHN*d
    ms = min(norm(X[i]-X[j]) for i in range(n) for j in range(i+1,n))
    out.append((sgn, X, ms))
    print("sense %+d: R(C2-N18)=%.4f  R(O3-H21)=%.4f  R(C2-H21)=%.4f  H-N-Calpha=%.1f  H-N-C17=%.1f  minsep=%.4f" % (
        sgn, r(X,C2,N18), r(X,O3,H21), r(X,C2,H21), ang(X,H21,N18,CA), ang(X,H21,N18,16), ms))

good = [o for o in out if o[2] >= 0.9]
if not good: raise SystemExit("no sense reaches minsep >= 0.9 A")
sgn, X, ms = max(good, key=lambda o: o[2])
print("")
print("chosen sense %+d" % sgn)
for nm, (i,j) in [("R(C2-N18)",(C2,N18)),("R(C2-O3)",(C2,O3)),("R(N18-H21)",(N18,H21)),
                  ("R(O3-H21)",(O3,H21)),("R(C2-H21)",(C2,H21)),("R(O3-N18)",(O3,N18)),
                  ("R(C1-C2)",(0,1)),("R(C2-C3)",(C2,C3)),("R(C3-H22)",(C3,H22)),("R(O13-H19)",(12,18))]:
    print("  %-12s: %.4f" % (nm, r(X,i,j)))
print("  angle O3-C2...N18: %.1f deg ; H-N-Calpha %.1f ; H-N-C17 %.1f" % (ang(X,O3,C2,N18), ang(X,H21,N18,CA), ang(X,H21,N18,16)))

print("")
print("slide table (rotation + H21 reorientation fixed; f scales the final translation):")
Xr = X0.copy(); Xr[ACETONE] = X0[C2] + (X0[ACETONE]-X0[C2]) @ rodrigues(axis, sgn*(THETA-phi0)).T
u = (Xr[N18]-Xr[C2])/norm(Xr[N18]-Xr[C2])
dtot = r(Xr,C2,N18)-TARGET
rows = []
for fr in [0.0,0.2,0.4,0.6,0.8,0.9,1.0]:
    Z = Xr.copy(); Z[ACETONE] = Xr[ACETONE] + fr*dtot*u
    mid = 0.5*(Z[C2]+Z[O3]); d = Z[N18]-mid; d = d/norm(d); Z[H21] = Z[N18] + LHN*d
    rows.append((fr, r(Z,C2,N18), min(norm(Z[i]-Z[j]) for i in range(n) for j in range(i+1,n))))
for fr, val, m in rows: print("  f=%.1f  R(C2-N18)=%.4f  minsep=%.4f" % (fr, val, m))
sv = [row[1] for row in rows]
print("strictly monotonic decreasing =", all(sv[i] > sv[i+1] for i in range(len(sv)-1)))

ms2 = None; pr = None
for i in range(n):
    for j in range(i+1,n):
        d = r(X,i,j)
        if ms2 is None or d < ms2: ms2, pr = d, (i+1, els[i], j+1, els[j])
print("minsep of delivered frame: %.4f A between atom %d(%s) and %d(%s)" % (ms2, pr[0], pr[1], pr[2], pr[3]))

with open(OUT,"w") as fh:
    fh.write("%d\n" % n)
    fh.write("E1a fallback(a): RC_27 basis; acetone rigid-rotated about C2 to O3-C2...N18=110 deg (sense %+d) then slid to R(C2-N18)=%.3f A; H21 kept on N18 (%.4f A) and re-oriented away from the carbonyl; proline heavy atoms unchanged" % (sgn, r(X,C2,N18), LHN))
    fh.write("\n")
    for e, c in zip(els, X):
        fh.write("%-2s %14.8f %14.8f %14.8f\n" % (e, c[0], c[1], c[2]))
print("written:", OUT)
