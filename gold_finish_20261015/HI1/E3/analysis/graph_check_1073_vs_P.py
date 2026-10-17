
import numpy as np
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds, inchi
from rdkit import RDLogger
RDLogger.DisableLog('rdApp.*')
RUNS="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/runs"
PT=Chem.GetPeriodicTable()
def xyzf(p):
    ls=open(p).read().splitlines(); n=int(ls[0]); a=[]
    for l in ls[2:2+n]:
        p2=l.split(); a.append((PT.GetAtomicNumber(p2[0]),float(p2[1]),float(p2[2]),float(p2[3])))
    return a
def mol(a):
    txt="\n".join([str(len(a)),"f"]+["%-3s %.8f %.8f %.8f"%(PT.GetElementSymbol(z),x,y,zz) for z,x,y,zz in a])+"\n"
    m=Chem.MolFromXYZBlock(txt); rdDetermineBonds.DetermineBonds(m,charge=0); return m
A=xyzf("1073_freq_final_frame.xyz"); B=xyzf("P_1061_last_frame.xyz")
mA=mol(A); mP=mol(B)
def desc(m):
    out=[]
    for b in m.GetBonds():
        i,j=b.GetBeginAtomIdx(),b.GetEndAtomIdx()
        si,sj=PT.GetElementSymbol(m.GetAtomWithIdx(i).GetAtomicNum()),PT.GetElementSymbol(m.GetAtomWithIdx(j).GetAtomicNum())
        out.append("%s%s%s(%.1f)"%(min(si,sj),max(si,sj),"-"[0:0],b.GetBondTypeAsDouble()))
    return sorted(out)
dA,dP=desc(mA),desc(mP)
print("1073 bond multiset == P bond multiset :", dA==dP)
print("1073 bonds:",dA)
print("P    bonds:",dP)
print("1073 frags:",[len(f) for f in Chem.GetMolFrags(mA)],"P frags:",[len(f) for f in Chem.GetMolFrags(mP)])
hA=Chem.RemoveHs(mA); hP=Chem.RemoveHs(mP)
print("heavy atoms 1073/P:",hA.GetNumAtoms(),hP.GetNumAtoms())
mt1=hA.GetSubstructMatches(hP,uniquify=False,maxMatches=10000)
mt2=hP.GetSubstructMatches(hA,uniquify=False,maxMatches=10000)
print("heavy matches 1073<-P:",len(mt1),"P<-1073:",len(mt2))
HA=[a.GetIdx() for a in hA.GetAtoms()]; HP=[a.GetIdx() for a in hP.GetAtoms()]
PA=np.array([[x,y,z] for _,x,y,z in A]); PB=np.array([[x,y,z] for _,x,y,z in B])
def kab(P,Q):
    Pc=P-P.mean(0); Qc=Q-Q.mean(0); H=Pc.T@Qc; U,S,Vt=np.linalg.svd(H)
    d=np.sign(np.linalg.det(Vt.T@U.T)); R=Vt.T@np.diag([1.,1.,d])@U.T
    dev=np.linalg.norm((R@Pc.T).T-Qc,axis=1); return float(np.sqrt((dev**2).mean())),float(dev.max()),dev
for k,mt in enumerate(mt1):
    p=PA[HA]; q=PB[[HP[t] for t in mt]]
    r,mx,dev=kab(p,q)
    wi=int(np.argmax(dev))
    print("  mapping#%d heavy rms=%.4f max=%.4f worst: 1073 atom %d(%s) <-> P atom %d(%s) dev=%.4f"%(k+1,r,mx,HA[wi]+1,PT.GetElementSymbol(A[HA[wi]][0]),HP[mt[wi]]+1,PT.GetElementSymbol(B[HP[mt[wi]]][0]),dev[wi]))
    print("     1073-order -> P-order pairs:",[(HA[i]+1,HP[mt[i]]+1) for i in range(len(mt))])
