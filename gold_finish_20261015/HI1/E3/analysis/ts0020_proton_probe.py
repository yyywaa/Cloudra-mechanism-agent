
import numpy as np
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds
from rdkit import RDLogger
RDLogger.DisableLog('rdApp.*')
PT=Chem.GetPeriodicTable()
p="/home/ly/Cloudra-mechanism-agent/ts/ts_0020/jobs/declaration_0001/ts_opt/refine.log"
ls=open(p).read().splitlines()
h=[i for i,l in enumerate(ls) if 'Standard orientation' in l][-1]
d=[k for k in range(h,h+10) if ls[k].strip().startswith('-----')]
a=[];k=d[1]+1
while not ls[k].strip().startswith('-----'):
    q=ls[k].split(); a.append((int(q[1]),float(q[3]),float(q[4]),float(q[5]))); k+=1
X=np.array([[x,y,z] for _,x,y,z in a])
txt="\n".join([str(len(a)),"f"]+["%-3s %.8f %.8f %.8f"%(PT.GetElementSymbol(z),x,y,zz) for z,x,y,zz in a])+"\n"
m=Chem.MolFromXYZBlock(txt); rdDetermineBonds.DetermineBonds(m,charge=0)
print("perceived fragments:",[len(f) for f in Chem.GetMolFrags(m)])
for idx in (26,27):
    nb=sorted([(round(float(np.linalg.norm(X[idx-1]-X[j])),4),j+1,PT.GetElementSymbol(a[j][0])) for j in range(len(a)) if j!=idx-1 and a[j][0]>1])
    print("H%d nearest heavy:"%idx, nb[:3])
    print("   graph bonds of H%d:"%idx, [(n.GetIdx()+1,PT.GetElementSymbol(n.GetAtomicNum())) for n in m.GetAtomWithIdx(idx-1).GetNeighbors()])
for idx in (2,4,10,25):
    print("atom %d (%s) graph bonds:"%(idx,PT.GetElementSymbol(a[idx-1][0])), [(n.GetIdx()+1,PT.GetElementSymbol(n.GetAtomicNum())) for n in m.GetAtomWithIdx(idx-1).GetNeighbors()])
from rdkit.Chem import inchi, rdMolDescriptors
print("formula:",rdMolDescriptors.CalcMolFormula(m))
print("InChIKey:",inchi.InchiToInchiKey(inchi.MolToInchi(m)))
print("InChI:",inchi.MolToInchi(m))
