#!/usr/bin/env python3
"""Fallback (a) for HI1_E1a, v7: early-attack frame at R(C2-N18)=2.10 A with self-checks.
Rigid acetone fragment + separately handled transferring proton.
For each rotation sense and each candidate Buergi-Dunitz angle theta, build the frame and
report: final O3-C2...N18 angle, key distances, global minsep and the atoms involved.
Selection rule (documented): the frame must satisfy minsep >= 0.9 A and O3...N18 >= 2.6 A
(no carbonyl-O/N overlap) and R(O3-H21) >= 1.6 A; among those, take the theta closest to 110 deg.
Proline heavy atoms are unchanged from RC_27; H21 stays bonded to N18 (RC value)."""
import numpy as np
from numpy.linalg import norm

S = "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split"
A_PATH = S + "/RC_27_opt_frame.xyz"
OUT    = S + "/E1A_fallback_earlyattack_R210.xyz"
TARGET = 2.10

L = open(A_PATH).read().splitlines(); n = int(L[0].split()[0])
els = [f.split()[0] for f in L[2:2+n]]
X0 = np.array([[float(x) for x in f.split()[1:4]] for f in L[2:2+n]])
C2, O3, C3, H22, N18, H21, CA = 1, 2, 3, 9, 17, 26, 13
ACETONE = list(range(0, 10))

def r(Z,i,j): return float(norm(Z[i]-Z[j]))
def ang(Z,i,j,k):
    a=Z[i]-Z[j]; b=Z[k]-Z[j]
    return float(np.rad2deg(np.arccos(np.clip(a@b/(norm(a)*norm(b)),-1,1))))
def rod(axis,th):
    k=axis/norm(axis); K=np.array([[0,-k[2],k[1]],[k[2],0,-k[0]],[-k[1],k[0],0]])
    return np.eye(3)+np.sin(th)*K+(1-np.cos(th))*(K@K)
def minsep(Z):
    best=(9e9,None,None)
    for i in range(n):
        for j in range(i+1,n):
            d=r(Z,i,j)
            if d<best[0]: best=(d,i+1,j+1)
    return best

LHN = r(X0,N18,H21)
v1=X0[O3]-X0[C2]; v2=X0[N18]-X0[C2]
axis=np.cross(v1,v2); axis=axis/norm(axis)
phi0=ang(X0,O3,C2,N18)
print("RC_27: R(C2-N18)=%.4f  O3-C2...N18=%.1f deg  R(O3-H21)=%.4f  N18-H21=%.4f  minsep=%.4f (%s)" % (
    r(X0,C2,N18), phi0, r(X0,O3,H21), LHN, minsep(X0)[0], minsep(X0)[1:]))

def build(theta, sgn):
    Rot = rod(axis, sgn*(theta-phi0))
    X = X0.copy()
    X[ACETONE] = X0[C2] + (X0[ACETONE]-X0[C2]) @ Rot.T
    u = (X[N18]-X[C2])/norm(X[N18]-X[C2])
    X[ACETONE] = X[ACETONE] + (r(X,C2,N18)-TARGET)*u
    mid = 0.5*(X[C2]+X[O3]); d = X[N18]-mid; d = d/norm(d)
    X[H21] = X[N18] + LHN*d
    return X, Rot

rows=[]
for theta in (105.0, 110.0, 115.0, 120.0, 125.0, 130.0):
    for sgn in (+1.0,-1.0):
        X,_ = build(theta,sgn)
        a = ang(X,O3,C2,N18)
        if abs(a-theta) > 1.0:            # this sense does not give the requested angle
            continue
        ms = minsep(X)
        rows.append((theta,sgn,a,ms,r(X,O3,N18),r(X,O3,H21),r(X,C2,H21),ang(X,H21,N18,CA),ang(X,H21,N18,16)))
        print("theta=%5.1f sense %+d -> achieved %.1f | minsep %.4f (%d-%d) | O3...N18 %.3f | O3-H21 %.3f | C2-H21 %.3f | H-N-Ca %.1f | H-N-C17 %.1f" % (
            theta,sgn,a,ms[0],ms[1],ms[2],rows[-1][5],rows[-1][6],rows[-1][7],rows[-1][8],rows[-1][9]))

ok=[x for x in rows if x[3][0]>=0.9 and x[4]>=2.6 and x[5]>=1.6]
print("")
print("frames passing minsep>=0.9, O3...N18>=2.6, O3-H21>=1.6 :", [(o[0],o[1]) for o in ok])
if not ok: raise SystemExit("no acceptable theta")
best=sorted(ok, key=lambda o: abs(o[0]-110.0))[0]
theta,sgn = best[0],best[1]
X,Rot = build(theta,sgn)
print("chosen: theta=%.1f deg, sense %+d" % (theta,sgn))
for nm,(i,j) in [("R(C2-N18)",(C2,N18)),("R(C2-O3)",(C2,O3)),("R(N18-H21)",(N18,H21)),("R(O3-H21)",(O3,H21)),
                  ("R(C2-H21)",(C2,H21)),("R(O3-N18)",(O3,N18)),("R(C1-C2)",(0,1)),("R(C2-C3)",(C2,C3)),
                  ("R(C3-H22)",(C3,H22)),("R(O13-H19)",(12,18))]:
    print("  %-12s: %.4f" % (nm, r(X,i,j)))
ms=minsep(X)
print("  minsep %.4f A between atom %d and %d" % (ms[0],ms[1],ms[2]))

print("")
print("slide table (rotation + H21 reorientation held fixed):")
Xr = X0.copy(); Xr[ACETONE] = X0[C2] + (X0[ACETONE]-X0[C2]) @ Rot.T
u=(Xr[N18]-Xr[C2])/norm(Xr[N18]-Xr[C2]); dtot=r(Xr,C2,N18)-TARGET
rows2=[]
for fr in [0.0,0.2,0.4,0.6,0.8,0.9,1.0]:
    Z=Xr.copy(); Z[ACETONE]=Xr[ACETONE]+fr*dtot*u
    mid=0.5*(Z[C2]+Z[O3]); d=Z[N18]-mid; d=d/norm(d); Z[H21]=Z[N18]+LHN*d
    rows2.append((fr, r(Z,C2,N18), minsep(Z)[0]))
for fr,val,m in rows2: print("  f=%.1f  R(C2-N18)=%.4f  minsep=%.4f" % (fr,val,m))
sv=[x[1] for x in rows2]
print("strictly monotonic decreasing =", all(sv[i]>sv[i+1] for i in range(len(sv)-1)))

with open(OUT,"w") as fh:
    fh.write("%d\n" % n)
    fh.write("E1a fallback(a): RC_27 basis; acetone rigid-rotated about C2 to O3-C2...N18=%.1f deg (sense %+d) then slid to R(C2-N18)=%.3f A; H21 on N18 (%.4f A) re-oriented away from the carbonyl; proline heavy atoms unchanged" % (theta, sgn, r(X,C2,N18), LHN))
    fh.write("\n")
    for e,c in zip(els,X): fh.write("%-2s %14.8f %14.8f %14.8f\n" % (e,c[0],c[1],c[2]))
print("written:", OUT)
