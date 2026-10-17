import numpy as np
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
def heavy_mol(el,co,drop_bond=None):
    """build a heavy-atom-only RDKit mol; drop_bond = (orig_i, orig_j) 0-based to omit"""
    hidx=[i for i,z in enumerate(el) if z!=1]
    pos={o:k for k,o in enumerate(hidx)}
    m=Chem.RWMol()
    for o in hidx: m.AddAtom(Chem.Atom(int(el[o])))
    # determine connectivity on the FULL molecule, then keep heavy-heavy bonds
    full=Chem.RWMol()
    for z in el: full.AddAtom(Chem.Atom(int(z)))
    conf=Chem.Conformer(len(el))
    for i,(x,y,z) in enumerate(co): conf.SetAtomPosition(i,(float(x),float(y),float(z)))
    fm=full.GetMol(); fm.AddConformer(conf); rdDetermineBonds.DetermineConnectivity(fm)
    kept=[]
    for bd in fm.GetBonds():
        i,j=bd.GetBeginAtomIdx(),bd.GetEndAtomIdx()
        if el[i]==1 or el[j]==1: continue
        if drop_bond and set((i,j))==set(drop_bond): continue
        m.AddBond(pos[i],pos[j],Chem.BondType.SINGLE); kept.append((pos[i],pos[j]))
    mol=m.GetMol()
    conf2=Chem.Conformer(len(hidx))
    for k,o in enumerate(hidx): conf2.SetAtomPosition(k,(float(co[o][0]),float(co[o][1]),float(co[o][2])))
    mol.AddConformer(conf2)
    return mol, hidx, kept
def kabsch(A,B):
    A=np.asarray(A,float); B=np.asarray(B,float)
    A=A-A.mean(0); B=B-B.mean(0)
    U,S,Vt=np.linalg.svd(A.T@B); d=np.sign(np.linalg.det(U@Vt))
    R=U@np.diag([1.0,1.0,d])@Vt; D=((A@R)-B)**2
    return float(np.sqrt(D.sum()/len(A))), float(np.linalg.det(R)), float(np.sqrt(D.sum(1).max()))
b=[x for x in blocks(BASE+"runs/build_seed_product_optfreq.log") if x[0] < 49775][-1]
X=b[1]; elX=b[2]
He,elH=xyz(BASE+"prep/hemiaminal_1028_lastframe.xyz")
q,hidx1,b1=heavy_mol(elX,X)
t,hidx2,b2=heavy_mol(elH,He,drop_bond=(1,3))
print("1073 heavy graph: %d atoms / %d bonds" % (q.GetNumAtoms(), q.GetNumBonds()))
print("1028 heavy graph minus bond(orig 2,4): %d atoms / %d bonds" % (t.GetNumAtoms(), t.GetNumBonds()))
mt=t.GetSubstructMatches(q, uniquify=False, maxMatches=5000)
print("match count 1073(heavy) -> 1028(heavy, edge removed):", len(mt))
best=None
for m_ in mt:
    rk=kabsch(np.array([X[hidx1[i]] for i in range(len(hidx1))]), np.array([He[hidx2[j]] for j in m_]))
    if best is None or rk[0]<best[0]: best=rk
if best: print("best heavy Kabsch: %.4f A det=%+.2f max %.4f A" % best)
