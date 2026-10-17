import numpy as np, re
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds, inchi
LOG="/home/ly/Cloudra-mechanism-agent/ts/ts_0020/jobs/declaration_0001/ts_opt/refine.log"
L=open(LOG).read().splitlines()
N=41
blocks=[];i=0
while i<len(L):
    if "Input orientation:" in L[i] or "Standard orientation:" in L[i]:
        k=i+1;co=[];el=[]
        while k<len(L) and len(co)<N:
            p=L[k].split()
            if len(p)==6 and p[0].isdigit() and p[1].isdigit():
                el.append(int(p[1]));co.append([float(p[3]),float(p[4]),float(p[5])])
            k+=1
        if len(co)==N: blocks.append((i+1,np.array(co),el))
        i=k
    else: i+=1
hdr,X,el=blocks[-1]
Z={1:"H",6:"C",7:"N",8:"O"}
print("last orientation block L%d | atoms %d | C%d H%d N%d O%d" % (hdr,len(el),el.count(6),el.count(1),el.count(7),el.count(8)))
d=lambda a,b: float(np.linalg.norm(X[a-1]-X[b-1]))
print("E3 1-based key distances:")
for nm,(a,b) in [("C2-N4",(2,4)),("C2-O25",(2,25)),("N4-H26",(4,26)),("O25-H26",(25,26)),("C9-O10",(9,10)),("O10-H27",(10,27)),("N4-H27",(4,27)),("O10-H26",(10,26)),("C9-O11",(9,11)),("C2-O28",(2,28))]:
    print("   %-9s %8.4f" % (nm,d(a,b)))
heavy=[k for k in range(1,N+1) if el[k-1]!=1]
for h in (26,27):
    s=sorted(((d(h,k),k) for k in heavy))[:3]
    print("   H%d nearest heavy: " % h + ", ".join("%s%d %.4f" % (Z[el[k-1]],k,dist) for dist,k in s))
# minsep classification: bonded (both heavy & < 1.75 | heavy-H < 1.25), 1-3 (share a bonded neighbour), else non-bonded
pairs=[]
for a in range(1,N+1):
    for b in range(a+1,N+1):
        r=d(a,b)
        bonded = (el[a-1]!=1 and el[b-1]!=1 and r<1.75) or ((el[a-1]==1)!=(el[b-1]==1) and r<1.25)
        pairs.append((r,a,b,bonded))
bonded=[(r,a,b) for r,a,b,bo in pairs if bo]
nb={}
for r,a,b in bonded:
    nb.setdefault(a,set()).add(b); nb.setdefault(b,set()).add(a)
def is13(a,b):
    return bool(nb.get(a,set()) & nb.get(b,set()))
bond_list=[(r,a,b) for r,a,b,bo in pairs if bo]
one3=[(r,a,b) for r,a,b,bo in pairs if not bo and is13(a,b)]
nonb=[(r,a,b) for r,a,b,bo in pairs if not bo and not is13(a,b)]
print()
print("bonded pairs: %d | tightest 6: %s" % (len(bond_list), ", ".join("%s%d-%s%d %.4f" % (Z[el[a-1]],a,Z[el[b-1]],b,r) for r,a,b in sorted(bond_list)[:6])))
print("1-3 pairs   : %d | tightest 6: %s" % (len(one3), ", ".join("%s%d-%s%d %.4f" % (Z[el[a-1]],a,Z[el[b-1]],b,r) for r,a,b in sorted(one3)[:6])))
print("non-bonded  : %d | tightest 6: %s" % (len(nonb), ", ".join("%s%d-%s%d %.4f" % (Z[el[a-1]],a,Z[el[b-1]],b,r) for r,a,b in sorted(nonb)[:6])))
print("minsep non-bonded = %.4f A (>=1.20 gate: %s)" % (sorted(nonb)[0][0], "PASS" if sorted(nonb)[0][0]>=1.20 else "FAIL"))
print("minsep 1-3        = %.4f A" % sorted(one3)[0][0])
print("minsep bonded     = %.4f A" % sorted(bond_list)[0][0])
# connectivity / InChIKey
m=Chem.RWMol()
for z in el: m.AddAtom(Chem.Atom(int(z)))
for r,a,b in bond_list: m.AddBond(a-1,b-1,Chem.BondType.SINGLE)
mol=m.GetMol()
from rdkit.Geometry import Point3D
conf=Chem.Conformer(len(el))
for idx in range(len(el)):
    conf.SetAtomPosition(idx, Point3D(float(X[idx][0]),float(X[idx][1]),float(X[idx][2])))
mol.AddConformer(conf, assignId=True)
try:
    rdDetermineBonds.DetermineBondOrders(mol, charge=0)
    Chem.SanitizeMol(mol)
    from rdkit.Chem import rdmolops
    frags=rdmolops.GetMolFrags(mol)
    print()
    print("InChIKey:", inchi.MolToInchiKey(mol))
    print("fragments:", [len(f) for f in frags], "| heavy bonds:", mol.GetNumBonds()-sum(1 for at in mol.GetAtoms() if at.GetAtomicNum()==1))
except Exception as e:
    print("bond-order perception failed:", e)
