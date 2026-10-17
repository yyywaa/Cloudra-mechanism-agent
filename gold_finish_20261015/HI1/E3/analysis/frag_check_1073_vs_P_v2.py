
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
    dev=np.linalg.norm((R@Pc.T).T-Qc,axis=1); return float(np.sqrt((dev**2).mean())),float(dev.max())
frA=[list(f) for f in Chem.GetMolFrags(mA)]; frP=[list(f) for f in Chem.GetMolFrags(mP)]
print("1073 frags:",[len(f) for f in frA],"formulas:",[rdMolDescriptors.CalcMolFormula(Chem.PathToSubmol(mA,f)) for f in frA])
print("P    frags:",[len(f) for f in frP],"formulas:",[rdMolDescriptors.CalcMolFormula(Chem.PathToSubmol(mP,f)) for f in frP])
hA=Chem.RemoveHs(mA); hP=Chem.RemoveHs(mP)
mt=hA.GetSubstructMatches(hP,uniquify=False,maxMatches=10000)
HA=[a.GetIdx() for a in hA.GetAtoms()]; HP=[a.GetIdx() for a in hP.GetAtoms()]
best=None
for m in mt:
    r,mx=kab(PA[HA],PB[[HP[t] for t in m]])
    if best is None or r<best[0]: best=(r,mx,m)
r,mx,m=best; mp={HA[i]:HP[m[i]] for i in range(len(m))}
print("global heavy rms=%.4f max=%.4f over %d heavy atoms"%(r,mx,len(HA)))
for fi,f in enumerate(frA):
    hs=[i for i in f if i in mp]
    r2,mx2=kab(PA[hs],PB[[mp[i] for i in hs]])
    print("  frag%d n=%d heavy=%d intra-fragment rms=%.4f max=%.4f"%(fi+1,len(f),len(hs),r2,mx2))
fr0,fr1=frA
d=np.linalg.norm(PA[fr0][:,None,:]-PA[fr1][None,:,:],axis=2)
for k in np.argsort(d,axis=None)[:5]:
    i,j=np.unravel_index(k,d.shape); gi,gj=fr0[i],fr1[j]
    print("  1073 contact %.4f : atom %d(%s) -- atom %d(%s)"%(d[i,j],gi+1,PT.GetElementSymbol(A[gi][0]),gj+1,PT.GetElementSymbol(A[gj][0])))
fp0,fp1=frP
dp=np.linalg.norm(PB[fp0][:,None,:]-PB[fp1][None,:,:],axis=2)
for k in np.argsort(dp,axis=None)[:4]:
    i,j=np.unravel_index(k,dp.shape); gi,gj=fp0[i],fp1[j]
    print("  P   contact %.4f : atom %d(%s) -- atom %d(%s)"%(dp[i,j],gi+1,PT.GetElementSymbol(B[gi][0]),gj+1,PT.GetElementSymbol(B[gj][0])))
def dd(i,j): return float(np.linalg.norm(PA[i-1]-PA[j-1]))
for (i,j,lab) in [(26,25,'C26-O25'),(26,27,'C26-O27'),(26,32,'C26-N32'),(2,3,'C2-O3'),(32,33,'N32-H33'),(32,34,'N32-H34')]:
    print("  R(%d,%d)=%.4f  %s-%s  [%s]"%(i,j,dd(i,j),PT.GetElementSymbol(A[i-1][0]),PT.GetElementSymbol(A[j-1][0]),lab))
print("N32 neighbours:",[(n.GetIdx()+1,PT.GetElementSymbol(n.GetAtomicNum())) for n in mA.GetAtomWithIdx(31).GetNeighbors()])
print("C26 neighbours:",[(n.GetIdx()+1,PT.GetElementSymbol(n.GetAtomicNum())) for n in mA.GetAtomWithIdx(25).GetNeighbors()])
