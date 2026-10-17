import numpy as np, re
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds, inchi
LOG="/home/ly/Cloudra-mechanism-agent/ts/ts_0020/jobs/declaration_0001/ts_opt/refine.log"
L=open(LOG).read().splitlines()
blocks=[]; i=0
while i < len(L):
    if "Input orientation:" in L[i] or "Standard orientation:" in L[i]:
        k=i+1; co=[]; el=[]
        while k < len(L) and len(co)<41:
            p=L[k].split()
            if len(p)==6 and p[0].isdigit() and p[1].isdigit():
                el.append(int(p[1])); co.append([float(p[3]),float(p[4]),float(p[5])])
            k+=1
        if len(co)==41: blocks.append((i+1,np.array(co),el))
        i=k
    else: i+=1
X=blocks[-1][1]; el=blocks[-1][2]
print("log lines:", len(L), "| last orientation block L%d | atoms %d | elements C%d H%d N%d O%d" % (blocks[-1][0], len(el), el.count(6), el.count(1), el.count(7), el.count(8)))
Z={1:"H",6:"C",7:"N",8:"O"}
d=lambda a,b: float(np.linalg.norm(X[a-1]-X[b-1]))
print("E3 1-based key distances:")
for nm,(i1,j1) in [("C2-N4",(2,4)),("C2-O25",(2,25)),("N4-H26",(4,26)),("O25-H26",(25,26)),("C9-O10",(9,10)),("O10-H27",(10,27)),("N4-H27",(4,27)),("O10-H26",(10,26)),("C9-O11",(9,11))]:
    print("   %-9s %8.4f" % (nm, d(i1,j1)))
for a in (26,27):
    heavy=[k for k in range(1,42) if el[k-1]!=1]
    nn=min(((d(a,k),k) for k in heavy))
    print("   H%d nearest heavy: %s%d %.4f A" % (a, Z[el[nn[1]-1]], nn[1], nn[0]))
m=Chem.RWMol()
for z in el: m.AddAtom(Chem.Atom(int(z)))
conf=Chem.Conformer(len(el))
for i2,(x,y,z) in enumerate(X): conf.SetAtomPosition(i2,(float(x),float(y),float(z)))
mm=m.GetMol(); mm.AddConformer(conf)
rdDetermineBonds.DetermineBonds(mm, charge=0)
print("InChIKey:", inchi.MolToInchiKey(mm))
print("fragments:", [len(f) for f in Chem.GetMolFrags(mm, asMols=False)])
print("heavy bonds:", sum(1 for bd in mm.GetBonds() if bd.GetBeginAtom().GetAtomicNum()>1 and bd.GetEndAtom().GetAtomicNum()>1))