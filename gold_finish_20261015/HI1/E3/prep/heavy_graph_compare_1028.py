import numpy as np
from collections import Counter
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds
BASE="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/"
def blocks(path):
    L=open(path).read().splitlines(); out=[]; i=0
    while i < len(L):
        if "Input orientation:" in L[i] or "Standard orientation:" in L[i]:
            k=i+1; co=[]; el=[]
            while k < len(L) and len(co) < 41:
                p=L[k].split()
                if len(p)==6 and p[0].isdigit() and p[1].isdigit():
                    el.append(int(p[1])); co.append([float(p[3]),float(p[4]),float(p[5])])
                k+=1
            if len(co)==41: out.append((i+1,np.array(co),el))
            i=k
        else: i+=1
    return out
def xyz(path):
    L=open(path).read().splitlines(); n=int(L[0].split()[0]); co=[]; el=[]; Z={"H":1,"C":6,"N":7,"O":8}
    for ln in L[2:2+n]:
        p=ln.split(); el.append(Z[p[0]]); co.append([float(p[1]),float(p[2]),float(p[3])])
    return np.array(co), el
def mkmol(el,co):
    m=Chem.RWMol()
    for z in el: m.AddAtom(Chem.Atom(int(z)))
    conf=Chem.Conformer(len(el))
    for i,(x,y,z) in enumerate(co): conf.SetAtomPosition(i,(float(x),float(y),float(z)))
    mol=m.GetMol(); mol.AddConformer(conf); rdDetermineBonds.DetermineConnectivity(mol); return mol
b=[x for x in blocks(BASE+"runs/build_seed_product_optfreq.log") if x[0] < 49775][-1]
X=b[1]; elX=b[2]; m1=mkmol(elX,X)
He,elH=xyz(BASE+"prep/hemiaminal_1028_lastframe.xyz"); m2=mkmol(elH,He)
def heavy_bonds(m,el,skip=None):
    out=[]
    for bd in m.GetBonds():
        i,j=bd.GetBeginAtomIdx(),bd.GetEndAtomIdx()
        if el[i]==1 or el[j]==1: continue
        if skip and set((i,j))==set(skip): continue
        out.append(tuple(sorted((el[i],el[j]))))
    return out
hb1=heavy_bonds(m1,elX); hb2=heavy_bonds(m2,elH,skip=(1,3))
print("1073 heavy bond multiset :", sorted(Counter(hb1).items()))
print("1028 heavy minus E3 2-4 :", sorted(Counter(hb2).items()))
print("multiset equal:", Counter(hb1)==Counter(hb2), "| n bonds:", len(hb1), len(hb2))
# heavy-degree profile
def degprof(m,el):
    d=[]
    for a in m.GetAtoms():
        i=a.GetIdx()
        if el[i]==1: continue
        d.append((el[i], sum(1 for nb in a.GetNeighbors() if el[nb.GetIdx()]!=1)))
    return sorted(Counter(d).items())
print("1073 heavy (element,heavy-degree):", sorted(degprof(m1,elX)))
print("1028 heavy (element,heavy-degree):", sorted(degprof(m2,elH)))
