import numpy as np, json
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds
BASE="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/"
def lastblock(path):
    L=open(path).read().splitlines(); blk=None; i=0
    while i < len(L):
        if "Input orientation:" in L[i] or "Standard orientation:" in L[i]:
            k=i+1; co=[]; el=[]
            while k < len(L) and len(co)<41:
                p=L[k].split()
                if len(p)==6 and p[0].isdigit() and p[1].isdigit():
                    el.append(int(p[1])); co.append([float(p[3]),float(p[4]),float(p[5])])
                k+=1
            if len(co)==41: blk=(i+1,np.array(co),el)
            i=k
        else: i+=1
    return blk
def kab(A,B):
    A=np.asarray(A,float); B=np.asarray(B,float)
    A=A-A.mean(0); B=B-B.mean(0)
    U,S,Vt=np.linalg.svd(A.T@B); d=np.sign(np.linalg.det(U@Vt)); R=U@np.diag([1.0,1.0,d])@Vt
    D=((A@R)-B)**2; return float(np.sqrt(D.sum()/len(A))), float(np.sqrt(D.sum(1).max()))
b1=lastblock(BASE+"runs/build_seed_product_optfreq.log"); X=b1[1]; elX=b1[2]
b2=lastblock(BASE+"runs/P_e3b/P_optfreq.log"); P=b2[1]; elP=b2[2]
rows=json.load(open(BASE+"prep/seed_to_P_mapping_v4.json"))["rows"]
def mol(el,co):
    m=Chem.RWMol()
    for z in el: m.AddAtom(Chem.Atom(int(z)))
    conf=Chem.Conformer(len(el))
    for i,(x,y,z) in enumerate(co): conf.SetAtomPosition(i,(float(x),float(y),float(z)))
    mm=m.GetMol(); mm.AddConformer(conf); rdDetermineBonds.DetermineBonds(mm, charge=0); return mm
f1=[set(i+1 for i in f) for f in Chem.GetMolFrags(mol(elX,X), asMols=False)]
f2=[set(i+1 for i in f) for f in Chem.GetMolFrags(mol(elP,P), asMols=False)]
for k,row in enumerate(rows):
    if not row.get("complete"): continue
    order=row["order"]; pm={i+1:order[i] for i in range(41)}
    for fi,fa in enumerate(f1):
        tgtset=set()
        for a in fa:
            for j,f in enumerate(f2):
                if pm[a] in f: tgtset=f
        heavy=[a for a in fa if elX[a-1]!=1]
        r=kab(np.array([X[a-1] for a in heavy]), np.array([P[pm[a]-1] for a in heavy]))
        print("iso %d | 1073 frag%d (%d C) heavy(%d): RMSD %.4f max %.4f" % (row.get("iso"), fi, [elX[a-1] for a in fa].count(6), len(heavy), r[0], r[1]))
