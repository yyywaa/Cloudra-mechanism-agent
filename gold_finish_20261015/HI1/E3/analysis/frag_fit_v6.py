
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
A=xyzf("1073_freq_final_frame.xyz"); B=xyzf("P_1061_last_frame.xyz")
PA=np.array([[x,y,z] for _,x,y,z in A]); PB=np.array([[x,y,z] for _,x,y,z in B])
mA=mol(A); mP=mol(B)
# fragment mols WITH original index mapping
mapsA=[]; fragsA=Chem.GetMolFrags(mA,asMols=True,fragsMolAtomMapping=mapsA)
mapsP=[]; fragsP=Chem.GetMolFrags(mP,asMols=True,fragsMolAtomMapping=mapsP)
print("frags 1073:",[rdMolDescriptors.CalcMolFormula(f) for f in fragsA]," P:",[rdMolDescriptors.CalcMolFormula(f) for f in fragsP])
def setup(f,mp):
    heavy=[i for i,a in enumerate(f.GetAtoms()) if a.GetAtomicNum()>1]
    orig=[mp[i] for i in heavy]
    return Chem.RemoveHs(f), orig
for k in range(2):
    hA,oA=setup(fragsA[k],mapsA[k]); hP,oP=setup(fragsP[k],mapsP[k])
    assert hA.GetNumAtoms()==len(oA) and hP.GetNumAtoms()==len(oP)
    mts=hA.GetSubstructMatches(hP,uniquify=False,maxMatches=1000)   # query=hP -> returns A-atom indices
    res=[]
    for mt in mts:
        if len(mt)!=hA.GetNumAtoms(): continue
        pairs=[(oA[mt[i]],oP[i]) for i in range(len(oP))]
        assert all(A[a][0]==B[b][0] for a,b in pairs), "element mismatch"
        r,mx,dev=kab(PA[[a for a,_ in pairs]],PB[[b for _,b in pairs]])
        res.append((r,mx,pairs))
    res.sort(key=lambda t:t[0])
    print("frag%d (%s) heavy=%d  full isomorphisms=%d"%(k+1,rdMolDescriptors.CalcMolFormula(fragsA[k]),len(oA),len(res)))
    for r,mx,pairs in res:
        print("   rms=%.4f max=%.4f pairs(1073->P 1-based)=%s"%(r,mx,[(a+1,b+1) for a,b in pairs]))
