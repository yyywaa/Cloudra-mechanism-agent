
import numpy as np
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds, rdMolDescriptors
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
def kab(P,Q):
    Pc=P-P.mean(0); Qc=Q-Q.mean(0); H=Pc.T@Qc; U,S,Vt=np.linalg.svd(H)
    d=np.sign(np.linalg.det(Vt.T@U.T)); R=Vt.T@np.diag([1.,1.,d])@U.T
    dev=np.linalg.norm((R@Pc.T).T-Qc,axis=1); return float(np.sqrt((dev**2).mean())),float(dev.max()),dev
# --- synthetic self-checks on kab() ---
rng=np.random.default_rng(7); X=rng.normal(size=(20,3))
th=0.7; Rm=np.array([[np.cos(th),-np.sin(th),0],[np.sin(th),np.cos(th),0],[0,0,1]])
t=np.array([1.0,-2.0,0.5])
print("(i)  known rot+trans -> %.3e  (expect 0)"%kab(X,X@Rm.T+t)[0])
Xm=X*np.array([1,-1,1]); print("(ii) mirror (reflection ALLOWED) -> %.6f (expect !=0)"%kab(X,Xm)[0])
Y=X.copy(); print("(iii) identical copy -> %.3e (expect 0)"%kab(X,Y)[0])
A=xyzf("1073_freq_final_frame.xyz"); B=xyzf("P_1061_last_frame.xyz")
PA=np.array([[x,y,z] for _,x,y,z in A]); PB=np.array([[x,y,z] for _,x,y,z in B])
mA=mol(A); mP=mol(B)
mapsA=[]; fragsA=Chem.GetMolFrags(mA,asMols=True,fragsMolAtomMapping=mapsA)
mapsP=[]; fragsP=Chem.GetMolFrags(mP,asMols=True,fragsMolAtomMapping=mapsP)
heavyA=[i for i,a in enumerate(mA.GetAtoms()) if a.GetAtomicNum()>1]
heavyB=[i for i,a in enumerate(mP.GetAtoms()) if a.GetAtomicNum()>1]
hA=Chem.RemoveHs(mA); hP=Chem.RemoveHs(mP)
mts=hA.GetSubstructMatches(hP,uniquify=False,maxMatches=1000)
# fragment heavy sets (original idx)
fset=[]
for k in range(2):
    hs=[mapsA[k][i] for i,a in enumerate(fragsA[k].GetAtoms()) if a.GetAtomicNum()>1]
    fset.append(set(hs))
print("frag heavy sets:",[sorted(x) for x in fset])
for k,mt in enumerate(mts):
    if len(mt)!=hA.GetNumAtoms(): continue
    pairs=[(heavyA[mt[i]],heavyB[i]) for i in range(len(heavyB))]
    assert all(A[a][0]==B[b][0] for a,b in pairs)
    oa=[a for a,_ in pairs]; ob=[b for _,b in pairs]
    print("--- mapping#%d ---"%(k+1))
    r,mx,dev=kab(PA[oa],PB[ob]); print("  (a) best-fit on all 20 heavy: rms=%.4f max=%.4f"%(r,mx))
    for fi,s in enumerate(fset):
        idx=[i for i in range(20) if oa[i] in s]
        r2,mx2,_=kab(PA[[oa[i] for i in idx]],PB[[ob[i] for i in idx]])
        print("  (b%d) fit on frag%d heavy=%d only, eval same subset: rms=%.4f max=%.4f"%(fi+1,fi+1,len(idx),r2,mx2))
    # (c) all-41 best fit with H mapped to nearest heavy partner, then heavy-only rms
    maph={}
    for a,b in pairs: maph[a]=b
    for i,a in enumerate(mA.GetAtoms()):
        if a.GetAtomicNum()!=1: continue
        nb=[n.GetIdx() for n in a.GetNeighbors()][0]
        cands=[j for j,y in enumerate(mP.GetAtoms()) if y.GetAtomicNum()==1 and [n.GetIdx() for n in y.GetNeighbors()]==[maph[nb]]]
        used=set(maph.values())
        cands=[c for c in cands if c not in used]
        if cands: maph[i]=cands[0]
    allpairs=sorted(maph.items())
    r3,mx3,_=kab(PA[[a for a,_ in allpairs]],PB[[b for _,b in allpairs]])
    print("  (c) best-fit on %d atoms (H by nearest heavy), then heavy-only rms:"%len(allpairs))
    r4,mx4,dev4=kab(PA[oa],PB[ob])
    # compute heavy rms under rotation derived from all-41 fit
    Pc=PA[[a for a,_ in allpairs]]; Qc=PB[[b for _,b in allpairs]]
    Pmean=Pc.mean(0); Qmean=Qc.mean(0)
    H=(Pc-Pmean).T@(Qc-Qmean); U,S,Vt=np.linalg.svd(H); d=np.sign(np.linalg.det(Vt.T@U.T))
    R=Vt.T@np.diag([1.,1.,d])@U.T
    dh=np.linalg.norm(((R@(PA[oa]-Pmean).T).T+Qmean)-PB[ob],axis=1)
    print("     heavy rms under all-41 rotation = %.4f (max %.4f)"%(np.sqrt((dh**2).mean()),dh.max()))
    print("  pairs (1073->P):",[(a+1,b+1) for a,b in pairs])
