
import numpy as np
from rdkit import Chem
PT=Chem.GetPeriodicTable()
p="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/runs/e3b_scan2d_c2n4_o25h26.log"
ls=open(p).read().splitlines()
oc=[i for i,l in enumerate(ls) if 'Optimization completed' in l]
print("OPT lines:",[i+1 for i in oc])
def frame_before(idx):
    h=[j for j in range(idx) if 'Standard orientation' in ls[j]][-1]
    d=[k for k in range(h,h+10) if ls[k].strip().startswith('-----')]
    a=[];k=d[1]+1
    while not ls[k].strip().startswith('-----'):
        q=ls[k].split(); a.append((int(q[1]),float(q[3]),float(q[4]),float(q[5]))); k+=1
    assert len(a)==41
    return h,d[1]+1,k,a
rows=[]
for n,i in enumerate(oc,1):
    h,s0,e0,a=frame_before(i)
    X=np.array([[x,y,z] for _,x,y,z in a])
    j=[k for k in range(i) if 'SCF Done' in ls[k]][-1]
    E=float(ls[j].split('=')[1].split()[0])
    d=lambda u,v: float(np.linalg.norm(X[u-1]-X[v-1]))
    hb=min([(d(26,k),k+1,PT.GetElementSymbol(a[k-1][0])) for k in range(1,42) if a[k-1][0]>1 and k!=26])
    rows.append(dict(n=n,opt=i+1,hdr=h+1,ab=(s0,e0),scf=j+1,E=E,R24=d(2,4),R2526=d(25,26),R426=d(4,26),R1027=d(10,27),R225=d(2,25),h26=hb))
    print("pt%d OPT L%d | hdr L%d / L%d-%d | SCF L%d E=%.9f | R(2,4)=%.4f R(25,26)=%.4f R(4,26)=%.4f R(10,27)=%.4f R(2,25)=%.4f | H26-nearest=%s"%(
        n,i+1,h+1,s0,e0,j+1,E,d(2,4),d(25,26),d(4,26),d(10,27),d(2,25),hb))
Eref=rows[0]['E']
for r in rows[1:]:
    print("pt%d vs pt1: dE=%+.2f kcal/mol"%((r['E']-Eref)*627.5095))
