#!/usr/bin/env python3
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
th_c=[round(float(t),2) for t in np.arange(-180,180,0.01) if abs(np.linalg.norm(O1-rot1(O3,Na,uNaC,t))-2.5)<0.001]
out=[]
for phi in np.arange(-180,180,0.5):
    Hf=rot1(X[10],O1,ucd,phi); d0=(Hf-O1)/np.linalg.norm(Hf-O1)
    for th in th_c:
        if not (-12.2 < th < -11.4): continue
        Xa=X.copy(); Xa[[1,2,3,4,5]]=np.array([rot1(X[k],Na,uNaC,th) for k in [1,2,3,4,5]])
        w=(Xa[2]-O1)/np.linalg.norm(Xa[2]-O1); T=O1+1.25*w
        for x in [7, 8, 1, 6, 5, 4, 3, 2]:
            u=(Xa[x-1]-O1)/np.linalg.norm(Xa[x-1]-O1)
            if abs(float((d0-w)@u))>0.002: continue
            dp=d0-(d0@u)*u; wp=w-(w@u)*u
            a=math.degrees(math.atan2(float(np.dot(np.cross(dp,wp),u)), float(dp@wp)))
            # contact check on the FINAL geometry
            Xf=Xa.copy(); Xf[10]=T
            d_me_H6=min(np.linalg.norm(T-Xf[k]) for k in [1,3,4,5])
            d_H6_C4=np.linalg.norm(T-Xf[6]); d_Na_H6=np.linalg.norm(Xf[0]-T)
            d_O5_meth=min(np.linalg.norm(Xf[7]-Xf[k]) for k in [1,2,3,4,5])
            out.append((round(phi,2), x, round(a,3), round(d_me_H6,3), round(d_Na_H6,3), round(d_O5_meth,3)))
print("solutions with theta ~ -11.79 for axes in [7,8,1,6,5,4,3,2]:", len(out))
for o in out[:25]: print("   flip %.2f -> op3 rotate[11] ax[9,%d] %.3f   || H6...methoxide=%.3f  Na...H6=%.3f  O5...methoxide=%.3f" % o)
