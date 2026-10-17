#!/usr/bin/env python3
"""E3-guess ops search (v7). Plan (stretch must be validated on an input whose graph has no ring):
 call1 (input prep/i2.xyz): rotate [11] about [9,7] by -90 deg  ->  A.xyz  (H11 far from Na and O3)
 call2 (input A.xyz): op1 stretch [9,11] -> 1.25 ;  op2 rotate [2,3,4,5,6] about [1,7] theta ;
                      op3 rotate [11] about [9,x] a
 Search (theta,x,a) so that |O1...O3| = 2.500 (so the H at 1.25 on the O1->O3 ray is 1.25 from both)."""
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

el,X=read_xyz("gold_finish_20261015/NY3/prep/i2.xyz")
O1=X[8]; C4=X[6]; Na=X[0]; O3=X[2]; ucd=(C4-O1)/np.linalg.norm(C4-O1); uNaC=(C4-Na)/np.linalg.norm(C4-Na)
# candidate theta values giving |O1...O3| = 2.500
th_c=[]
prev=None
for th in np.arange(-180,180,0.02):
    O3t=rot1(O3,Na,uNaC,th); d=np.linalg.norm(O1-O3t)
    if abs(d-2.5)<0.002: th_c.append(round(float(th),2))
print("theta candidates with |O1...O3|=2.50:", th_c)
sols=[]
for phi in np.arange(-180,180,0.5):
    Hf = rot1(X[10], O1, ucd, phi)                    # H11 after the call-1 flip
    d0 = (Hf-O1)/np.linalg.norm(Hf-O1)
    d0n = np.linalg.norm(Hf-O1)
    for th in th_c:
        Xa=X.copy(); Xa[[1,2,3,4,5]]=np.array([rot1(X[k],Na,uNaC,th) for k in [1,2,3,4,5]])
        O3t=Xa[2]; d13=np.linalg.norm(O1-O3t)
        if abs(d13-2.5)>0.005: continue
        w=(O3t-O1)/d13
        if np.linalg.norm(Xa[0]-Xa[2])<2.2: continue
        if np.linalg.norm(Xa[6]-Xa[2])<2.9: continue
        for x in range(11):
            if x==8: continue
            if np.linalg.norm(Xa[x]-O1)<1e-6: continue
            u=(Xa[x]-O1)/np.linalg.norm(Xa[x]-O1)
            resid=(d0-w)@u
            if abs(resid)>0.002: continue
            dp=d0-(d0@u)*u; wp=w-(w@u)*u
            a=math.degrees(math.atan2(float(np.dot(np.cross(dp,wp),u)), float(dp@wp)))
            sols.append((round(phi,2), round(float(th),2), x+1, round(a,3), round(float(np.degrees(np.arccos(np.clip(d0@w,-1,1)))),2)))
print("solutions:", len(sols))
for s in sols[:25]: print("   flip180->%.2f deg ; op2 rotate[2..6] ax[1,7] %.2f ; op3 rotate[11] ax[9,%d] %.3f  (dir change %.1f deg)" % s)
