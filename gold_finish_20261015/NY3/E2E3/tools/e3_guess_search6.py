#!/usr/bin/env python3
"""E3-guess ops search (v6).  Legal rigid-op sequence in ONE transform call:
 op1 rotate [11] about [9,7] by 180 deg   (H points away from O3 and from Na -> the Na-O9-H11 ring
                                          and the O3...H11 contact disappear, so the stretch is legal)
 op2 stretch [9,11] -> 1.25               (sets |O1-H6|)
 op3 rotate [2,3,4,5,6] about [1,7] theta (methoxide azimuth: keeps |Na-O3| and |C4...O3|)
 op4 rotate [11] about [9,x] by a         (axis through O1 -> |O1-H6| stays 1.25 exactly)
Search (theta, x, a) so that |O3-H6| = 1.25 too, with the O1-H6-O3 angle as linear as possible."""
import math
import numpy as np
def read_xyz(p):
    L=open(p).read().splitlines(); n=int(L[0].split()[0]); el=[];X=[]
    for l in L[2:2+n]:
        s=l.split(); el.append(s[0]); X.append([float(s[1]),float(s[2]),float(s[3])])
    return el, np.array(X)
def rot1(p,ap,u,deg):
    a=math.radians(deg); v=p-ap; par=u*(v@u); per=v-par
    return ap+par+per*math.cos(a)+np.cross(u,per)*math.sin(a)
def rot(P,ap,u,deg):
    a=math.radians(deg); v=P-ap; par=np.outer(v@u,u); per=v-par
    return ap+par+per*math.cos(a)+np.cross(np.tile(u,(len(P),1)),per)*math.sin(a)
el,X=read_xyz("gold_finish_20261015/NY3/prep/i2.xyz")
Na,O3,C4,O1,O1i,H6 = X[0],X[2],X[6],X[8],8,X[10]
# op1
Xa = X.copy(); Xa[10] = rot1(H6, O1, (C4-O1)/np.linalg.norm(C4-O1), 180)
print("after op1 (flip 180 about O1-C4): |O1-H6|=%.3f |O3...H6|=%.3f |Na...H6|=%.3f" % (
    np.linalg.norm(Xa[8]-Xa[10]), np.linalg.norm(Xa[2]-Xa[10]), np.linalg.norm(Xa[0]-Xa[10])))
# op2 stretch [9,11] -> 1.25  (move atom 11 radially from atom 9)
u = (Xa[10]-Xa[8])/np.linalg.norm(Xa[10]-Xa[8]); Xb = Xa.copy(); Xb[10] = Xa[8] + 1.25*u
print("after op2 (stretch [9,11]->1.25): |O1-H6|=%.3f |O3...H6|=%.3f |Na...H6|=%.3f" % (
    np.linalg.norm(Xb[8]-Xb[10]), np.linalg.norm(Xb[2]-Xb[10]), np.linalg.norm(Xb[0]-Xb[10])))
O1 = Xb[8]; H6 = Xb[10]; Na = Xb[0]; C4 = Xb[6]
ua = (C4-Na)/np.linalg.norm(C4-Na)
sols=[]
for x in range(11):
    if x == 8: continue
    axp = Xb[8]; axu = (Xb[x]-Xb[8])/np.linalg.norm(Xb[x]-Xb[8])
    if np.linalg.norm(Xb[x]-Xb[8]) < 1e-6: continue
    v = H6-axp; par = axu*(v@axu); c = axp+par; per = v-par; r = np.linalg.norm(per)
    if r < 1e-6: continue
    e1 = per/r; e2 = np.cross(axu, e1)
    for theta in np.arange(-180, 180, 0.05):
        O3t = rot1(O3, Na, ua, theta); d13 = np.linalg.norm(O1-O3t)
        if not (2.35 <= d13 <= 2.52): continue
        C4O3 = np.linalg.norm(C4-O3t); NaO3 = np.linalg.norm(Na-O3t)
        if C4O3 < 2.90 or NaO3 < 2.20: continue
        m = c-O1
        A = m@m+r*r; B = 2*r*(m@e1); C = 2*r*(m@e2)
        for target in (O3t,):
            mm = c-target; A2 = mm@mm+r*r; B2 = 2*r*(mm@e1); C2 = 2*r*(mm@e2)
            K = 1.25**2 - A2; R = math.hypot(B2, C2)
            if abs(K) > R: continue
            phi = math.atan2(C2, B2)
            for s in (1, -1):
                aa = math.asin(max(-1, min(1, K/R)))
                av = (aa if s > 0 else math.pi-aa) - phi
                p = c + r*(math.cos(av)*e1 + math.sin(av)*e2)
                d1 = np.linalg.norm(p-O1); d3 = np.linalg.norm(p-O3t)
                if abs(d1-1.25) > 0.004 or abs(d3-1.25) > 0.004: continue
                ang = math.degrees(math.acos(max(-1, min(1, ((O1-p)@(O3t-p))/(np.linalg.norm(O1-p)*np.linalg.norm(O3t-p))))))
                mind = 9.0; arg = None
                for k in range(11):
                    if k in (8, 2, 10): continue
                    dd = np.linalg.norm(p-Xb[k])
                    if dd < mind: mind, arg = dd, k+1
                sols.append((round(ang, 1), round(float(theta), 2), x+1, round(math.degrees(av), 2),
                             round(float(d13), 3), round(float(C4O3), 3), round(float(mind), 2), arg))
print("solutions (d1=d3=1.25 within 0.004):", len(sols))
sols.sort(key=lambda s: -s[0])
for s in sols[:15]:
    print("   O1-H6-O3=%.1f deg  theta=%.2f  ax[9,%d] a=%.2f  |O1...O3|=%.3f |C4...O3|=%.3f  mincontact=%.2f(atom%d)" % s)
