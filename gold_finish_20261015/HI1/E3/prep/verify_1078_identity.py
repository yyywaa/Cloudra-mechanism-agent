import numpy as np
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds, inchi
from rdkit.Geometry import Point3D
OPT="/home/ly/Cloudra-mechanism-agent/ts/ts_0020/jobs/declaration_0001/ts_opt/refine.log"
FRQ="/home/ly/Cloudra-mechanism-agent/ts/ts_0020/jobs/declaration_0001/frequency/frequency.log"
N=41
def lastblock(path):
    L=open(path).read().splitlines(); blocks=[]; i=0
    while i<len(L):
        if "Input orientation:" in L[i] or "Standard orientation:" in L[i]:
            k=i+1; co=[]; el=[]
            while k<len(L) and len(co)<N:
                p=L[k].split()
                if len(p)==6 and p[0].isdigit() and p[1].isdigit():
                    el.append(int(p[1])); co.append([float(p[3]),float(p[4]),float(p[5])])
                k+=1
            if len(co)==N: blocks.append((i+1,np.array(co),el))
            i=k
        else: i+=1
    return blocks[-1]
ho,Xo,el=lastblock(OPT); hf,Xf,elf=lastblock(FRQ)
print("opt last orientation L%d | freq last orientation L%d" % (ho,hf))
print("same element order: %s" % (el==elf))
m=np.abs(Xo-Xf).max()
print("max|delta| between opt-final and freq-final geometry = %.6f A" % m)
def kabsch(A,B):
    Ac=A-A.mean(0); Bc=B-B.mean(0)
    U,S,Vt=np.linalg.svd(Ac.T@Bc); d=np.sign(np.linalg.det(Vt.T@U.T))
    R=Vt.T@np.diag([1,1,d])@U.T
    dev=np.linalg.norm((R@Ac.T).T-Bc,axis=1)
    return float(np.sqrt((dev**2).mean())), float(dev.max()), float(np.linalg.det(R))
print("Kabsch rms %.6f max %.6f det %+.1f" % kabsch(Xo,Xf))
d=lambda X,a,b: float(np.linalg.norm(X[a-1]-X[b-1]))
print("freq-final key distances: C2-N4 %.4f | C2-O25 %.4f | N4-H27 %.4f | O10-H26 %.4f | O25-H26 %.4f | O10-H27 %.4f" % (d(Xf,2,4),d(Xf,2,25),d(Xf,4,27),d(Xf,10,26),d(Xf,25,26),d(Xf,10,27)))
heavy=[k for k in range(1,N+1) if el[k-1]!=1]
pairs=[]
for a in range(1,N+1):
    for b in range(a+1,N+1):
        r=d(Xf,a,b)
        bonded=(el[a-1]!=1 and el[b-1]!=1 and r<1.75) or ((el[a-1]==1)!=(el[b-1]==1) and r<1.25)
        pairs.append((r,a,b,bonded))
bl=[(r,a,b) for r,a,b,bo in pairs if bo]
nb={}
for r,a,b in bl: nb.setdefault(a,set()).add(b); nb.setdefault(b,set()).add(a)
is13=lambda a,b: bool(nb.get(a,set())&nb.get(b,set()))
o3=[(r,a,b) for r,a,b,bo in pairs if not bo and is13(a,b)]
nbn=[(r,a,b) for r,a,b,bo in pairs if not bo and not is13(a,b)]
Z={1:"H",6:"C",7:"N",8:"O"}
print("minsep bonded %.4f | 1-3 %.4f | non-bonded %.4f" % (sorted(bl)[0][0], sorted(o3)[0][0], sorted(nbn)[0][0]))
m2=Chem.RWMol()
for z in el: m2.AddAtom(Chem.Atom(int(z)))
for r,a,b in bl: m2.AddBond(a-1,b-1,Chem.BondType.SINGLE)
mol=m2.GetMol(); conf=Chem.Conformer(len(el))
for i in range(len(el)): conf.SetAtomPosition(i, Point3D(*[float(v) for v in Xf[i]]))
mol.AddConformer(conf, assignId=True)
rdDetermineBonds.DetermineBondOrders(mol, charge=0); Chem.SanitizeMol(mol)
from rdkit.Chem import rdmolops
print("freq-final InChIKey:", inchi.MolToInchiKey(mol), "| fragments:", [len(f) for f in rdmolops.GetMolFrags(mol)])
