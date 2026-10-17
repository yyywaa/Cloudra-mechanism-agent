#!/usr/bin/env python3
"""Fallback (a) for HI1_E1a, v9: early-attack frame with R(C2-N18)=2.10 A.
Rigid acetone (atoms 1-10) rotated about C2 to a chosen O3-C2...N18 angle (radians fixed),
then slid along C2->N18; transferring proton H21 kept on N18 at the RC distance and
re-oriented away from the carbonyl. Proline heavy atoms unchanged.
Selection: minsep >= 0.9 A, O3...N18 >= 2.6 A, O3...H21 >= 1.6 A; take theta closest to 110 deg."""
import numpy as np
from numpy.linalg import norm
S = "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split"
A = S + "/RC_27_opt_frame.xyz"; OUT = S + "/E1A_fallback_earlyattack_R210.xyz"
TARGET = 2.10
L = open(A).read().splitlines(); n = int(L[0].split()[0])
els = [f.split()[0] for f in L[2:2+n]]
X0 = np.array([[float(x) for x in f.split()[1:4]] for f in L[2:2+n]])
C2,O3,C3,H22,N18,H21,CA = 1,2,3,9,17,26,13
AC = list(range(10))
def r(Z,i,j): return float(norm(Z[i]-Z[j]))
def ang(Z,i,j,k):
    a=Z[i]-Z[j]; b=Z[k]-Z[j]
    return float(np.degrees(np.arccos(np.clip(a@b/(norm(a)*norm(b)),-1,1))))
def rod_deg(ax,deg):
    th=np.radians(deg)
    k=ax/norm(ax); K=np.array([[0,-k[2],k[1]],[k[2],0,-k[0]],[-k[1],k[0],0]])
    return np.eye(3)+np.sin(th)*K+(1-np.cos(th))*(K@K)
def ms(Z):
    b=(9e9,0,0)
    for i in range(n):
        for j in range(i+1,n):
            d=r(Z,i,j)
            if d<b[0]: b=(d,i+1,j+1)
    return b
LHN=r(X0,N18,H21)
ax=np.cross(X0[O3]-X0[C2],X0[N18]-X0[C2]); ax=ax/norm(ax)
phi0=ang(X0,O3,C2,N18)
print("RC_27: R(C2-N18)=%.4f  O3-C2...N18=%.1f  N18-H21=%.4f  minsep=%.4f %s" % (r(X0,C2,N18),phi0,LHN,ms(X0)[0],ms(X0)[1:]))
def build(theta,sgn):
    X=X0.copy(); Rm=rod_deg(ax,sgn*(theta-phi0))
    X[AC]=X0[C2]+(X0[AC]-X0[C2])@Rm.T
    u=(X[N18]-X[C2])/norm(X[N18]-X[C2])
    X[AC]=X[AC]+(r(X,C2,N18)-TARGET)*u
    mid=0.5*(X[C2]+X[O3]); d=X[N18]-mid; d=d/norm(d); X[H21]=X[N18]+LHN*d
    return X,Rm
cand=[]
for th in (100.,105.,110.,115.,120.,125.,130.):
    for sg in (1.0,-1.0):
        X,Rm=build(th,sg); a=ang(X,O3,C2,N18); m=ms(X)
        ok = abs(a-th)<=1.0 and m[0]>=0.9 and r(X,O3,N18)>=2.6 and r(X,O3,H21)>=1.6
        print("th=%5.1f sg=%+.0f achieved=%6.1f ok=%s minsep=%.4f(%d-%d) O3N18=%.3f O3H21=%.3f HNCa=%.1f HNC17=%.1f" % (
            th,sg,a,ok,m[0],m[1],m[2],r(X,O3,N18),r(X,O3,H21),ang(X,H21,N18,CA),ang(X,H21,N18,16)))
        if ok: cand.append((th,sg,X,Rm))
print("")
print("acceptable:", [(c[0],c[1]) for c in cand])
if not cand: raise SystemExit("NO acceptable frame")
th,sg,X,Rm=min(cand,key=lambda c: abs(c[0]-110.0))
print("chosen theta=%.1f sense %+.0f" % (th,sg))
for nm,(i,j) in [("R(C2-N18)",(C2,N18)),("R(C2-O3)",(C2,O3)),("R(N18-H21)",(N18,H21)),("R(O3-H21)",(O3,H21)),("R(C2-H21)",(C2,H21)),("R(O3-N18)",(O3,N18)),("R(C1-C2)",(0,1)),("R(C2-C3)",(C2,C3)),("R(C3-H22)",(C3,H22)),("R(O13-H19)",(12,18))]:
    print("  %-12s %.4f" % (nm, r(X,i,j)))
m=ms(X); print("  minsep %.4f (atoms %d-%d); angles O3-C2...N18 %.1f, H-N-Ca %.1f, H-N-C17 %.1f" % (m[0],m[1],m[2],ang(X,O3,C2,N18),ang(X,H21,N18,CA),ang(X,H21,N18,16)))
print("")
print("slide table:")
Xr=X0.copy(); Xr[AC]=X0[C2]+(X0[AC]-X0[C2])@Rm.T
u=(Xr[N18]-Xr[C2])/norm(Xr[N18]-Xr[C2]); dt=r(Xr,C2,N18)-TARGET
tab=[]
for fr in [0.0,0.2,0.4,0.6,0.8,0.9,1.0]:
    Z=Xr.copy(); Z[AC]=Xr[AC]+fr*dt*u
    mid=0.5*(Z[C2]+Z[O3]); d=Z[N18]-mid; d=d/norm(d); Z[H21]=Z[N18]+LHN*d
    tab.append((fr,r(Z,C2,N18),ms(Z)[0])); print("  f=%.1f R(C2-N18)=%.4f minsep=%.4f" % tab[-1])
sv=[t[1] for t in tab]; print("strictly monotonic =", all(sv[i]>sv[i+1] for i in range(len(sv)-1)))
with open(OUT,"w") as fh:
    fh.write("%d\n" % n)
    fh.write("E1a fallback(a): RC_27 basis; acetone rigid-rotated about C2 to O3-C2...N18=%.1f deg (sense %+.0f) then slid to R(C2-N18)=%.3f A; H21 on N18 (%.4f A) re-oriented away from carbonyl; proline heavy atoms unchanged" % (th,sg,r(X,C2,N18),LHN))
    fh.write("\n")
    for e,c in zip(els,X): fh.write("%-2s %14.8f %14.8f %14.8f\n" % (e,c[0],c[1],c[2]))
print("written:",OUT)
