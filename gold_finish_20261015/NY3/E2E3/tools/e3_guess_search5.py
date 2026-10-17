#!/usr/bin/env python3
"""debug: how close can a 2-rotation-only op sequence get to d(O1-H6)=d(H6-O3)=1.25 ?"""
import math
import numpy as np
def read_xyz(p):
    L=open(p).read().splitlines(); n=int(L[0].split()[0]); el=[];X=[]
    for l in L[2:2+n]:
        s=l.split(); el.append(s[0]); X.append([float(s[1]),float(s[2]),float(s[3])])
    return el, np.array(X)
el,X=read_xyz("gold_finish_20261015/NY3/prep/i2.xyz")
Na,O3,C4,O1,H6 = X[0],X[2],X[6],X[8],X[10]
ua=(C4-Na)/np.linalg.norm(C4-Na)
def rot1(p,ap,u,deg):
    a=math.radians(deg); v=p-ap; par=u*(v@u); per=v-par
    return ap+par+per*math.cos(a)+np.cross(u,per)*math.sin(a)
lines=[(i,j,X[i],(X[j]-X[i])/np.linalg.norm(X[j]-X[i])) for i in range(11) for j in range(11) if i!=j]
best=[]
for theta in np.arange(-180,180,0.25):
    O3t=rot1(O3,Na,ua,theta); d13=np.linalg.norm(O1-O3t)
    if not (2.20<=d13<=2.55): continue
    for (i,j,ap,u) in lines:
        v=H6-ap; par=u*(v@u); c=ap+par; per=v-par; r=np.linalg.norm(per)
        if r<1e-6: continue
        e1=per/r; e2=np.cross(u,e1); m=c-O1
        A=m@m+r*r; B=2*r*(m@e1); C=2*r*(m@e2); K=1.25**2-A; R=math.hypot(B,C)
        if abs(K)>R: continue
        phi=math.atan2(C,B)
        for s in (1,-1):
            aa=math.asin(max(-1,min(1,K/R)))
            av=(aa if s>0 else math.pi-aa)-phi
            p=c+r*(math.cos(av)*e1+math.sin(av)*e2)
            d1=np.linalg.norm(p-O1); d3=np.linalg.norm(p-O3t)
            best.append((abs(d3-1.25)+abs(d1-1.25), round(float(theta),2), i+1, j+1, round(math.degrees(av),2),
                         round(float(d13),3), round(float(d1),4), round(float(d3),4)))
best.sort()
print("evaluated:", len(best))
for b in best[:15]: print("   resid=%.4f theta=%.2f ax(%d,%d) a=%.2f d13=%.3f  d(O1-H6)=%.4f d(O3-H6)=%.4f" % b)
