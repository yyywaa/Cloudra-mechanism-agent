import numpy as np
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds, inchi
BASE="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/"
def lastblock(path):
    L=open(path).read().splitlines(); blk=None; i=0
    while i < len(L):
        if "Input orientation:" in L[i] or "Standard orientation:" in L[i]:
            k=i+1; co=[]; el=[]
            while k < len(L) and len(co) < 41:
                p=L[k].split()
                if len(p)==6 and p[0].isdigit() and p[1].isdigit():
                    el.append(int(p[1])); co.append([float(p[3]),float(p[4]),float(p[5])])
                k+=1
            if len(co)==41: blk=(i+1,np.array(co),el)
            i=k
        else: i+=1
    return blk
def xyz(path):
    L=open(path).read().splitlines(); n=int(L[0].split()[0]); co=[]; el=[]; Z={"H":1,"C":6,"N":7,"O":8}
    for ln in L[2:2+n]:
        p=ln.split(); el.append(Z[p[0]]); co.append([float(p[1]),float(p[2]),float(p[3])])
    return np.array(co), el
def gjf(path):
    L=open(path).read().splitlines(); i=L.index("0 1")+1 if "0 1" in L else None
    co=[]; el=[]; Z={"H":1,"C":6,"N":7,"O":8}
    while i < len(L) and len(co) < 41:
        p=L[i].split()
        if len(p)>=4 and p[0] in Z:
            el.append(Z[p[0]]); co.append([float(p[1]),float(p[2]),float(p[3])])
        i+=1
    return np.array(co), el
def key(el,co,tag):
    m=Chem.RWMol()
    for z in el: m.AddAtom(Chem.Atom(int(z)))
    conf=Chem.Conformer(len(el))
    for i,(x,y,z) in enumerate(co): conf.SetAtomPosition(i,(float(x),float(y),float(z)))
    mol=m.GetMol(); mol.AddConformer(conf)
    try:
        rdDetermineBonds.DetermineBonds(mol, charge=0)
        k=inchi.MolToInchiKey(mol); ik=inchi.MolToInchi(mol)
        nb=sum(1 for b in mol.GetBonds() if b.GetBeginAtom().GetAtomicNum()>1 and b.GetEndAtom().GetAtomicNum()>1)
        print("%-28s InChIKey = %s | heavy bonds = %d" % (tag, k, nb))
        return k, ik
    except Exception as ex:
        print("%-28s FAILED: %r" % (tag, ex)); return None, None
print("target (declared P) : SMPZMOQIWMNUBG-YBVIJTQESA-N")
k1,i1=key(*lastblock(BASE+"runs/build_seed_product_optfreq.log")[:2][::1][0:2] if False else (lastblock(BASE+"runs/build_seed_product_optfreq.log")[2], lastblock(BASE+"runs/build_seed_product_optfreq.log")[1]),"1073 freq final frame")
print("   InChI:", i1)
co,el=gjf(BASE+"runs/build_seed_product_optfreq.gjf"); k2,i2=key(el,co,"1073 input seed geom")
co3,el3=xyz(BASE+"prep/hemiaminal_1028_lastframe.xyz"); k3,i3=key(el3,co3,"1028 hemiaminal frame")
b=lastblock(BASE+"runs/P_e3b/P_optfreq.log"); k4,i4=key(b[2],b[1],"P (job 1061) final frame")
print("\nverdicts: 1073-final == declared P key:", k1=="SMPZMOQIWMNUBG-YBVIJTQESA-N", "| seed == declared P key:", k2=="SMPZMOQIWMNUBG-YBVIJTQESA-N")
print("1073-final vs P(1061) same key:", k1==k4, "| 1073-final vs 1028 same key:", k1==k3)
