
import numpy as np
from rdkit import Chem
PT=Chem.GetPeriodicTable()
p="/home/ly/Cloudra-mechanism-agent/ts/ts_0020/jobs/declaration_0001/ts_opt/refine.log"
ls=open(p).read().splitlines()
h=[i for i,l in enumerate(ls) if 'Standard orientation' in l]
print("blocks:",len(h),"last:",h[-1]+1)
def frame(hdr):
    d=[k for k in range(hdr,hdr+10) if ls[k].strip().startswith('-----')]
    a=[];k=d[1]+1
    while not ls[k].strip().startswith('-----'):
        q=ls[k].split(); a.append((int(q[1]),float(q[3]),float(q[4]),float(q[5]))); k+=1
    return a,d[1]+1,k
a,s0,e0=frame(h[-1]); X=np.array([[x,y,z] for _,x,y,z in a])
print("NAtoms",len(a),"atom block L%d-L%d"%(s0,e0),"elem seq:",''.join(PT.GetElementSymbol(q[0]) for q in a))
d=lambda u,v: float(np.linalg.norm(X[u-1]-X[v-1]))
for (u,v,lab) in [(2,4,'C2-N4'),(2,25,'C2-O25'),(4,26,'N4-H26'),(25,26,'O25-H26'),(10,27,'O10-H27'),(4,27,'N4-H27'),(9,10,'C9-O10'),(2,3,'C2-O3')]:
    print("  %-10s R(%d,%d)=%.4f (%s-%s)"%(lab,u,v,d(u,v),PT.GetElementSymbol(a[u-1][0]),PT.GetElementSymbol(a[v-1][0])))
# energy deltas
E=float(ls[130669].split('=')[1].split()[0]); print("last SCF L130670 =",E)
for name,ref in (("1028",-939.312626605),("P/1061",-939.319540184),("1073",-939.316976731)):
    print("  dE vs %s = %+.2f kcal/mol"%((name),(E-ref)*627.5095))
