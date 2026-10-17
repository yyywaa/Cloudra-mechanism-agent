#!/usr/bin/env python3
"""Fallback (a) for HI1_E1a, v11: closest-contact early-attack frame that still satisfies
minsep >= 0.9 A, using the rigid acetone model (rotation to O3-C2...N18 = 105 deg,
azimuth spin 150 deg about the C2->N18 axis, H21 kept on N18 and re-oriented away from
the carbonyl, proline heavy atoms unchanged from RC_27).
The slide fraction is bisected so that the global minsep equals 0.90 A; the resulting
R(C2-N18) is reported (it is larger than 2.10 A because at 2.10 A a methyl-H/proline
contact would be 0.854 A, below the agreed 0.9 A floor)."""
import numpy as np
from numpy.linalg import norm
S = "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split"
A = S + "/RC_27_opt_frame.xyz"; OUT = S + "/E1A_fallback_earlyattack_minsep090.xyz"
FLOOR = 0.90
L = open(A).read().splitlines(); n = int(L[0].split()[0])
els = [f.split()[0] for f in L[2:2+n]]
X0 = np.array([[float(x) for x in f.split()[1:4]] for f in L[2:2+n]])
C2,O3,N18,H21,CA = 1,2,17,26,13
AC = list(range(10))
def r(Z,i,j): return float(norm(Z[i]-Z[j]))
def ang(Z,i,j,k):
    a=Z[i]-Z[j]; b=Z[k]-Z[j]
    return float(np.degrees(np.arccos(np.clip(a@b/(norm(a)*norm(b)),-1,1))))
def rod(axv,deg):
    th=np.radians(deg); k=axv/norm(axv)
    K=np.array([[0,-k[2],k[1]],[k[2],0,-k[0]],[-k[1],k[0],0]])
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
THETA, PHI = 105.0, 150.0
Rm=rod(ax,-(THETA-phi0))
Xr=X0.copy(); Xr[AC]=X0[C2]+(X0[AC]-X0[C2])@Rm.T
u=(Xr[N18]-Xr[C2])/norm(Xr[N18]-Xr[C2]); dtot=r(Xr,C2,N18)-2.10
Rs=rod(u,PHI)
def frame(fr):
    Z=Xr.copy(); Z[AC]=Xr[AC]+fr*dtot*u
    Z[AC]=Z[C2]+(Z[AC]-Z[C2])@Rs.T
    mid=0.5*(Z[C2]+Z[O3]); d=Z[N18]-mid; d=d/norm(d); Z[H21]=Z[N18]+LHN*d
    return Z
lo,hi=0.0,1.0
for _ in range(80):
    mid=0.5*(lo+hi)
    if ms(frame(mid))[0] > FLOOR: lo=mid
    else: hi=mid
fr=0.5*(lo+hi); Z=frame(fr); m=ms(Z)
print("bisected slide fraction f=%.4f" % fr)
print("R(C2-N18)  = %.4f A   (at f=1.0 it would be 2.10 A with minsep %.4f A)" % (r(Z,C2,N18), ms(frame(1.0))[0]))
print("minsep     = %.4f A between atoms %d and %d (floor %.2f)" % (m[0],m[1],m[2],FLOOR))
for nm,(i,j) in [("R(C2-O3)",(C2,O3)),("R(N18-H21)",(N18,H21)),("R(O3-H21)",(O3,H21)),("R(C2-H21)",(C2,H21)),("R(O3-N18)",(O3,N18)),("R(C3-H22)",(4,9)),("R(O13-H19)",(12,18))]:
    print("  %-12s %.4f" % (nm, r(Z,i,j)))
print("  angles: O3-C2...N18 %.1f ; H-N-Ca %.1f ; H-N-C17 %.1f" % (ang(Z,O3,C2,N18),ang(Z,H21,N18,CA),ang(Z,H21,N18,16)))
print("")
print("table of the same rigid model over the slide (R vs minsep):")
for f2 in [0.0,0.2,0.4,0.6,0.8,0.9,fr,1.0]:
    Z2=frame(f2); print("  f=%.3f R(C2-N18)=%.4f minsep=%.4f" % (f2, r(Z2,C2,N18), ms(Z2)[0]))
with open(OUT,"w") as fh:
    fh.write("%d\n" % n)
    fh.write("E1a fallback(a) early attack (rigid acetone, RC_27 basis): O3-C2...N18=%.0f deg, azimuth %.0f deg, slide bisected for minsep=%.2f A; R(C2-N18)=%.3f A; H21 on N18 (%.4f A) re-oriented away from carbonyl; proline heavy atoms unchanged" % (THETA,PHI,FLOOR,r(Z,C2,N18),LHN))
    fh.write("\n")
    for e,c in zip(els,Z): fh.write("%-2s %14.8f %14.8f %14.8f\n" % (e,c[0],c[1],c[2]))
print("written:",OUT)
