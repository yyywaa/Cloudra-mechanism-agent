
import numpy as np
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds
from rdkit import RDLogger
RDLogger.DisableLog('rdApp.*')
PT=Chem.GetPeriodicTable()
def xyzf(p):
    ls=open(p).read().splitlines(); n=int(ls[0]); a=[]
    for l in ls[2:2+n]:
        q=l.split(); a.append((PT.GetAtomicNumber(q[0]),float(q[1]),float(q[2]),float(q[3])))
    return a
def mol(a):
    txt="\n".join([str(len(a)),"f"]+["%-3s %.8f %.8f %.8f"%(PT.GetElementSymbol(z),x,y,zz) for z,x,y,zz in a])+"\n"
    m=Chem.MolFromXYZBlock(txt); rdDetermineBonds.DetermineBonds(m,charge=0); return m
A=xyzf("1073_freq_final_frame.xyz"); B=xyzf("P_1061_last_frame.xyz")
PA=np.array([[x,y,z] for _,x,y,z in A]); PB=np.array([[x,y,z] for _,x,y,z in B])
mA=mol(A); mP=mol(B)
print("atom 33:",PT.GetElementSymbol(A[32][0]),"bonds:",[(n.GetIdx()+1,PT.GetElementSymbol(n.GetAtomicNum())) for n in mA.GetAtomWithIdx(32).GetNeighbors()])
for n in mA.GetAtomWithIdx(32).GetNeighbors():
    print("   R(33,%d)=%.4f"%(n.GetIdx()+1, np.linalg.norm(PA[32]-PA[n.GetIdx()])))
print("O3 (atom3):",PT.GetElementSymbol(A[2][0]),"bonds:",[(n.GetIdx()+1,PT.GetElementSymbol(n.GetAtomicNum())) for n in mA.GetAtomWithIdx(2).GetNeighbors()])
print("dist O3 to all H:",sorted([(round(float(np.linalg.norm(PA[2]-PA[i])),4),i+1) for i in range(41) if A[i][0]==1])[:4])
print("dist all O to all H (min 6):")
res=[]
for i in range(41):
    if A[i][0]!=8: continue
    for j in range(41):
        if A[j][0]!=1: continue
        res.append((round(float(np.linalg.norm(PA[i]-PA[j])),4),i+1,j+1))
res.sort(); print(res[:6])
print("N-H distances:")
for i in range(41):
    if A[i][0]!=7: continue
    for j in range(41):
        if A[j][0]!=1: continue
        print("   N%d-H%d = %.4f"%(i+1,j+1,np.linalg.norm(PA[i]-PA[j])))
def kab(P,Q):
    Pc=P-P.mean(0); Qc=Q-Q.mean(0); H=Pc.T@Qc; U,S,Vt=np.linalg.svd(H)
    d=np.sign(np.linalg.det(Vt.T@U.T)); R=Vt.T@np.diag([1.,1.,d])@U.T
    dev=np.linalg.norm((R@Pc.T).T-Qc,axis=1); return float(np.sqrt((dev**2).mean())),float(dev.max())
frA=[list(f) for f in Chem.GetMolFrags(mA)]; frP=[list(f) for f in Chem.GetMolFrags(mP)]
hA=Chem.RemoveHs(mA); hP=Chem.RemoveHs(mP)
HAo=[a.GetIdx() for a in mA.GetAtoms() if a.GetAtomicNum()>1]; HPo=[a.GetIdx() for a in mP.GetAtoms() if a.GetAtomicNum()>1]
# per-fragment best fit: enumerate all isomorphisms of the fragment graphs
for fi,f in enumerate(frA):
    # fragment mols with original index bookkeeping
    Am=mA; Pm=mP
    fa=[i for i in f if i in HAo]; 
    g=[list(x) for x in Chem.GetMolFrags(mP)]
    # pick P fragment with same size & formula
    from rdkit.Chem import rdMolDescriptors
    tgt=[x for x in g if len([i for i in x if i in HPo])==len(fa) and rdMolDescriptors.CalcMolFormula(Chem.PathToSubmol(Am,f))==rdMolDescriptors.CalcMolFormula(Chem.PathToSubmol(Pm,x))][0]
    fb=[i for i in tgt if i in HPo]
    # build submols and match
    q=Chem.RWMol(hA); # not needed; use full-mol match restricted
    matches=hA.GetSubstructMatches(hP,uniquify=False,maxMatches=10000)
    best=None
    for m in matches:
        pairs=[(HAo[i],HPo[m[i]]) for i in range(len(m))]
        if not set(a for a,_ in pairs)==set(fa): continue
        if not set(b for _,b in pairs)==set(fb): continue
        r,mx=kab(PA[[a for a,_ in pairs]],PB[[b for _,b in pairs]])
        if best is None or r<best[0]: best=(r,mx,pairs)
    print("frag%d heavy=%d best-fit rms=%.4f max=%.4f"%(fi+1,len(fa),best[0],best[1]))
    print("   pairs:",best[2])
