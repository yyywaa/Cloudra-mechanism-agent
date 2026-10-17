
import numpy as np, re
from rdkit import Chem
PT=Chem.GetPeriodicTable()
p="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan.log"
ls=open(p).read().splitlines()
print("lines",len(ls))
oc=[i for i,l in enumerate(ls) if 'Optimization completed' in l]
print("OPT lines(1-based):",[i+1 for i in oc])
def last_block_before(idx):
    h=[j for j in range(idx) if 'Standard orientation' in ls[j]][-1]
    d=[k for k in range(h,h+10) if ls[k].strip().startswith('-----')]
    a=[];k=d[1]+1
    while not ls[k].strip().startswith('-----'):
        q=ls[k].split(); a.append((int(q[1]),float(q[3]),float(q[4]),float(q[5]))); k+=1
    return h,a,d[1]+1,k
def last_scf_before(idx):
    return [j for j in range(idx) if 'SCF Done' in ls[j]][-1]
for n,i in enumerate(oc,1):
    h,a,s0,e0=last_block_before(i)
    X=np.array([[x,y,z] for _,x,y,z in a])
    j=last_scf_before(i)
    E=float(ls[j].split('=')[1].split()[0])
    print("frame%d OPT L%d | geom hdr L%d atomblock L%d-L%d N=%d | SCF L%d E=%.9f | R(1,29)=%.4f | R(28,24)=%.4f R(11,24)=%.4f"%(
        n,i+1,h+1,s0,e0,len(a),j+1,E,float(np.linalg.norm(X[0]-X[28])),float(np.linalg.norm(X[27]-X[23])),float(np.linalg.norm(X[10]-X[23]))))
sp=[i for i,l in enumerate(ls) if 'on scan point' in l]
print("last scan point line L%d: %s"%(sp[-1]+1,ls[sp[-1]].strip()))
print("Normal termination count:",sum(1 for l in ls if 'Normal termination' in l),"Error termination count:",sum(1 for l in ls if 'Error termination' in l))
print("last 2 SCF:",[ (j+1, ls[j].split('=')[1].split()[0]) for j in [i for i,l in enumerate(ls) if 'SCF Done' in l][-2:]])
