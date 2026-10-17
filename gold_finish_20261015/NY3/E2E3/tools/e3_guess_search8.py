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
th_c=[]
for th in np.arange(-180,180,0.01):
    if abs(np.linalg.norm(O1-rot1(O3,Na,uNaC,th))-2.5)<0.001: th_c.append(round(float(th),2))
print("theta giving |O1...O3| = 2.500:", th_c)
res=[]
for phi in np.arange(-180,180,0.5):
    Hf=rot1(X[10],O1,ucd,phi); d0=(Hf-O1)/np.linalg.norm(Hf-O1)
    for th in th_c:
        Xa=X.copy(); Xa[[1,2,3,4,5]]=np.array([rot1(X[k],Na,uNaC,th) for k in [1,2,3,4,5]])
        O3t=Xa[2]; w=(O3t-O1)/np.linalg.norm(O3t-O1)
        T=O1+1.25*w
        # clash metric for the final geometry (methoxide as rotated, H6 at T)
        minds=[]
        exclude={(0,1),(0,2),(1,2),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5),(6,7),(6,8),(6,9),(8,10),(2,10),(8,1),(2,0),(2,1)}
        for p in range(11):
            for q in range(p+1,11):
                if (p,q) in exclude or (q,p) in exclude: continue
                if p==10 or q==10:
                    dd=np.linalg.norm((T if p==10 else Xa[p])-(Xa[q] if p==10 else (T if q==10 else Xa[q])))
                else:
                    dd=np.linalg.norm(Xa[p]-Xa[q])
                minds.append((dd,p+1,q+1))
        minds.sort(); mind=minds[0]
        for x in range(11):
            if x in (8,11): continue
            u=(Xa[x]-O1)/np.linalg.norm(Xa[x]-O1)
            if abs(float((d0-w)@u))>0.002: continue
            dp=d0-(d0@u)*u; wp=w-(w@u)*u
            a=math.degrees(math.atan2(float(np.dot(np.cross(dp,wp),u)), float(dp@wp)))
            res.append((round(phi,2), round(float(th),2), x+1, round(a,3), round(mind[0],3), mind[1], mind[2]))
print("solutions:", len(res))
import collections
bys=collections.defaultdict(list)
for r in res: bys[r[1]].append(r)
for th in sorted(bys, key=lambda t: abs(t+11.77)):
    rs=sorted(bys[th], key=lambda r: -r[4])[:3]
    print("theta=%.2f  n=%d  best:" % (th, len(bys[th])), rs)
