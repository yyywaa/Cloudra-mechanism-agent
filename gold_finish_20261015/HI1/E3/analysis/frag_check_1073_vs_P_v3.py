
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
A=xyzf("1073_freq_final_frame.xyz"); B=xyzf("P_1061_last_frame.xyz")
PA=np.array([[x,y,z] for _,x,y,z in A]); PB=np.array([[x,y,z] for _,x,y,z in B])
mA=mol(A); mP=mol(B)
def kab(P,Q):
    Pc=P-P.mean(0); Qc=Q-Q.mean(0); H=Pc.T@Qc; U,S,Vt=np.linalg.svd(H)
    d=np.sign(np.linalg.det(Vt.T@U.T)); R=Vt.T@np.diag([1.,1.,d])@U.T
    dev=np.linalg.norm((R@Pc.T).T-Qc,axis=1); return float(np.sqrt((dev**2).mean())),float(dev.max()),dev
frA_m=[m for m in Chem.GetMolFrags(mA,asMols=True)]; frP_m=Chem.GetMolFrags(mP,asMols=True)
print("1073 frag formulas:",[rdMolDescriptors.CalcMolFormula(m) for m in frA_m])
print("P    frag formulas:",[rdMolDescriptors.CalcMolFormula(m) for m in frP_m])
print("1073 frag sizes:",[len(f) for f in Chem.GetMolFrags(mA)],"P:",[len(f) for f in Chem.GetMolFrags(mP)])
hA=Chem.RemoveHs(mA); hP=Chem.RemoveHs(mP)
HAo=[a.GetIdx() for a in mA.GetAtoms() if a.GetAtomicNum()>1]
HPo=[a.GetIdx() for a in mP.GetAtoms() if a.GetAtomicNum()>1]
print("heavy counts:",len(HAo),len(HPo),"| hA atoms:",hA.GetNumAtoms(),hP.GetNumAtoms())
print("1073 heavy original idx:",[i+1 for i in HAo])
print("P    heavy original idx:",[i+1 for i in HPo])
# verify heavy order preserved by RemoveHs
assert [a.GetAtomicNum() for a in hA.GetAtoms()]==[a.GetAtomicNum() for a in mA.GetAtoms() if a.GetAtomicNum()>1]
assert [a.GetAtomicNum() for a in hP.GetAtoms()]==[a.GetAtomicNum() for a in mP.GetAtoms() if a.GetAtomicNum()>1]
mt=hA.GetSubstructMatches(hP,uniquify=False,maxMatches=10000)
print("heavy-graph full isomorphisms 1073->P:",len(mt))
best=None
for m in mt:
    p=PA[HAo]; q=PB[[HPo[t] for t in m]]
    r,mx,dev=kab(p,q)
    print("  heavy rms=%.4f max=%.4f"%(r,mx))
    if best is None or r<best[0]: best=(r,mx,m,dev)
r,mx,m,dev=best
wi=int(np.argmax(dev))
print("BEST heavy rms=%.4f max=%.4f | worst pair: 1073 atom %d(%s) <-> P atom %d(%s) dev=%.4f"%(r,mx,HAo[wi]+1,PT.GetElementSymbol(A[HAo[wi]][0]),HPo[m[wi]]+1,PT.GetElementSymbol(B[HPo[m[wi]]][0]),dev[wi]))
print("mapping 1073->P (1-based):",[(HAo[i]+1,HPo[m[i]]+1) for i in range(len(m))])
# per-fragment
frA=[list(f) for f in Chem.GetMolFrags(mA)]; frP=[list(f) for f in Chem.GetMolFrags(mP)]
mpset={HAo[i]:HPo[m[i]] for i in range(len(m))}
for fi,f in enumerate(frA):
    hs=[i for i in f if i in mpset]
    r2,mx2,_=kab(PA[hs],PB[[mpset[i] for i in hs]])
    print("  frag%d atoms=%d heavy=%d intra-fragment rms=%.4f max=%.4f"%(fi+1,len(f),len(hs),r2,mx2))
fr0,fr1=frA
d=np.linalg.norm(PA[fr0][:,None,:]-PA[fr1][None,:,:],axis=2)
for k in np.argsort(d,axis=None)[:5]:
    i,j=np.unravel_index(k,d.shape); gi,gj=fr0[i],fr1[j]
    print("  1073 interfragment %.4f : atom %d(%s) -- atom %d(%s)"%(d[i,j],gi+1,PT.GetElementSymbol(A[gi][0]),gj+1,PT.GetElementSymbol(A[gj][0])))
fp0,fp1=frP
dp=np.linalg.norm(PB[fp0][:,None,:]-PB[fp1][None,:,:],axis=2)
for k in np.argsort(dp,axis=None)[:4]:
    i,j=np.unravel_index(k,dp.shape); gi,gj=fp0[i],fp1[j]
    print("  P interfragment %.4f : atom %d(%s) -- atom %d(%s)"%(dp[i,j],gi+1,PT.GetElementSymbol(B[gi][0]),gj+1,PT.GetElementSymbol(B[gj][0])))
def dd(i,j): return float(np.linalg.norm(PA[i-1]-PA[j-1]))
for (i,j,lab) in [(2,3,'C2-O3'),(26,25,'C26-O25'),(26,27,'C26-O27'),(26,32,'C26-N32'),(32,41,'N32-H41')]:
    print("  R(%d,%d)=%.4f  %s-%s  [%s]"%(i,j,dd(i,j),PT.GetElementSymbol(A[i-1][0]),PT.GetElementSymbol(A[j-1][0]),lab))
print("C26 neighbours:",[(n.GetIdx()+1,PT.GetElementSymbol(n.GetAtomicNum())) for n in mA.GetAtomWithIdx(25).GetNeighbors()])
print("N32 neighbours:",[(n.GetIdx()+1,PT.GetElementSymbol(n.GetAtomicNum())) for n in mA.GetAtomWithIdx(31).GetNeighbors()])
