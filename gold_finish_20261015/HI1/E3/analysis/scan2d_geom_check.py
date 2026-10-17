
import numpy as np, re
from rdkit import Chem
PT=Chem.GetPeriodicTable()
p="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/runs/e3b_scan2d_c2n4_o25h26.log"
ls=open(p).read().splitlines()
h=[i for i,l in enumerate(ls) if 'Standard orientation' in l]
print("std-orientation blocks:",len(h),"last 3 headers:",[i+1 for i in h[-3:]])
def frame(hdr):
    d=[j for j in range(hdr,hdr+10) if ls[j].strip().startswith('-----')]
    a=[];j=d[1]+1
    while not ls[j].strip().startswith('-----'):
        q=ls[j].split(); a.append((int(q[1]),float(q[3]),float(q[4]),float(q[5]))); j+=1
    return a,d[1]+1,j
a,s0,e0=frame(h[-1])
X=np.array([[x,y,z] for _,x,y,z in a])
print("last block atom range L%d-L%d  NAtoms=%d"%(s0,e0,len(a)))
def d(i,j): return float(np.linalg.norm(X[i-1]-X[j-1]))
print("measured R(2,4)=%.4f  R(25,26)=%.4f  R(10,27)=%.4f  R(4,26)=%.4f"%(d(2,4),d(25,26),d(10,27),d(4,26)))
print("elements: 2=%s 4=%s 25=%s 26=%s 10=%s 27=%s"%(PT.GetElementSymbol(a[1][0]),PT.GetElementSymbol(a[3][0]),PT.GetElementSymbol(a[24][0]),PT.GetElementSymbol(a[25][0]),PT.GetElementSymbol(a[9][0]),PT.GetElementSymbol(a[26][0])))
# H26 nearest heavy
best=sorted([(round(float(np.linalg.norm(X[25]-X[k])),4),k+1,PT.GetElementSymbol(a[k][0])) for k in range(len(a)) if a[k][0]>1 and k!=25])[:3]
print("H26 nearest heavy:",best)
print("step 0.2 -> 6 values:",[round(1.4248+0.2*k,4) for k in range(6)])
print("step 0.2 -> 5 values(coor stated):",[round(1.4248+0.2*k,4) for k in range(5)])
print("step 0.25 -> 6 values:",[round(0.9693+0.25*k,4) for k in range(6)])
