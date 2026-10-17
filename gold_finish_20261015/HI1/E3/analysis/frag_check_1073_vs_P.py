
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
mA=mol(A); mP=mol(B)
PA=np.array([[x,y,z] for _,x,y,z in A]); PB=np.array([[x,y,z] for _,x,y,z in B])
frA=[list(f) for f in Chem.GetMolFrags(mA)]; frP=[list(f) for f in Chem.GetMolFrags(mP)]
print("1073 frags (0-based):",["["+",".join(map(str,f))+"]" for f in frA])
def kab(P,Q):
    Pc=P-P.mean(0); Qc=Q-Q.mean(0); H=Pc.T@Qc; U,S,Vt=np.linalg.svd(H)
    d=np.sign(np.linalg.det(Vt.T@U.T)); R=Vt.T@np.diag([1.,1.,d])@U.T
    dev=np.linalg.norm((R@Pc.T).T-Qc,axis=1); return float(np.sqrt((dev**2).mean())),float(dev.max())
# match fragments by size and formula
for f in frA:
    n=len(f)
    cands=[g for g in frP if len(g)==n]
    print("1073 frag size",n,"formula",Chem.rdMolDescriptors.CalcMolFormula(Chem.PathToSubmol(mA,f)))
    for g in cands:
        q=mA.GetSubstructMatches(mP.GetSubstructMatch and mP, uniquify=False) if False else None
# proper: use substructure match per fragment
hA=Chem.RemoveHs(mA); hP=Chem.RemoveHs(mP)
mt=hA.GetSubstructMatches(hP,uniquify=False,maxMatches=10000)
HA=[a.GetIdx() for a in hA.GetAtoms()]; HP=[a.GetIdx() for a in hP.GetAtoms()]
best=None
for m in mt:
    r,mx=kab(PA[HA],PB[[HP[t] for t in m]])
    if best is None or r<best[0]: best=(r,mx,m)
r,mx,m=best
print("best heavy overall rms=%.4f max=%.4f"%(r,mx))
mp={HA[i]:HP[m[i]] for i in range(len(m))}
# per-fragment rms using that mapping (restricted to mapped pairs within same fragment)
for fi,f in enumerate(frA):
    hs=[i for i in f if i in mp]
    r2,mx2=kab(PA[hs],PB[[mp[i] for i in hs]])
    print("  frag%d (n=%d, heavy=%d) intra-fragment rms=%.4f max=%.4f"%(fi+1,len(f),len(hs),r2,mx2))
# short inter-fragment contacts in 1073
fr0,fr1=frA[0],frA[1]
d=np.linalg.norm(PA[fr0][:,None,:]-PA[fr1][None,:,:],axis=2)
order=np.argsort(d,axis=None)[:6]
for k in order:
    i,j=np.unravel_index(k,d.shape)
    gi,gj=fr0[i],fr1[j]
    print("   contact %.4f A : 1073 atom %d(%s) -- atom %d(%s)"%(d[i,j],gi+1,PT.GetElementSymbol(A[gi][0]),gj+1,PT.GetElementSymbol(A[gj][0])))
fr0p,fr1p=frP[0],frP[1]
dp=np.linalg.norm(PB[fr0p][:,None,:]-PB[fr1p][None,:,:],axis=2)
ko=np.argsort(dp,axis=None)[:3]
for k in ko:
    i,j=np.unravel_index(k,dp.shape); gi,gj=fr0p[i],fr1p[j]
    print("   P contact %.4f A : P atom %d(%s) -- atom %d(%s)"%(dp[i,j],gi+1,PT.GetElementSymbol(B[gi][0]),gj+1,PT.GetElementSymbol(B[gj][0])))
print("1073 frag formulas:",[Chem.rdMolDescriptors.CalcMolFormula(Chem.PathToSubmol(mA,f)) for f in frA])
print("P    frag formulas:",[Chem.rdMolDescriptors.CalcMolFormula(Chem.PathToSubmol(mP,f)) for f in frP])
