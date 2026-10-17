
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
    dev=np.linalg.norm((R@Pc.T).T-Qc,axis=1); return float(np.sqrt((dev**2).mean())),float(dev.max())
A=xyzf("1073_freq_final_frame.xyz"); B=xyzf("P_1061_last_frame.xyz")
PA=np.array([[x,y,z] for _,x,y,z in A]); PB=np.array([[x,y,z] for _,x,y,z in B])
mA=mol(A); mP=mol(B)
print("A) atom33 =",PT.GetElementSymbol(A[32][0]),"neighbours:",[(n.GetIdx()+1,PT.GetElementSymbol(n.GetAtomicNum())) for n in mA.GetAtomWithIdx(32).GetNeighbors()],"R:",[round(float(np.linalg.norm(PA[32]-PA[n.GetIdx()])),4) for n in mA.GetAtomWithIdx(32).GetNeighbors()])
print("B) atom3 =",PT.GetElementSymbol(A[2][0]),"neighbours:",[(n.GetIdx()+1,PT.GetElementSymbol(n.GetAtomicNum())) for n in mA.GetAtomWithIdx(2).GetNeighbors()])
print("   4 shortest O...H contacts 1073:",sorted([(round(float(np.linalg.norm(PA[i]-PA[j])),4),i+1,j+1) for i in range(41) if A[i][0]==8 for j in range(41) if A[j][0]==1])[:4])
mapsA=[]; fragsA=Chem.GetMolFrags(mA,asMols=True,fragsMolAtomMapping=mapsA)
mapsP=[]; fragsP=Chem.GetMolFrags(mP,asMols=True,fragsMolAtomMapping=mapsP)
print("C) fragments:",[rdMolDescriptors.CalcMolFormula(f) for f in fragsA],"|",[rdMolDescriptors.CalcMolFormula(f) for f in fragsP])
for k,(fA,fP) in enumerate(zip(fragsA,fragsP)):
    hvA=[i for i,a in enumerate(fA.GetAtoms()) if a.GetAtomicNum()>1]
    hvP=[i for i,a in enumerate(fP.GetAtoms()) if a.GetAtomicNum()>1]
    hA=Chem.RemoveHs(fA); hP=Chem.RemoveHs(fP)
    mts=hA.GetSubstructMatches(hP,uniquify=False,maxMatches=500)
    best=None
    for mt in mts:
        if sorted(mt)!=list(range(len(hvP))): continue
        oa=[mapsA[k][hvA[i]] for i in range(len(hvA))]
        ob=[mapsP[k][hvP[mt[i]]] for i in range(len(hvA))]
        r,mx=kab(PA[oa],PB[ob])
        if best is None or r<best[0]: best=(r,mx,oa,ob)
    print("  frag%d %s heavy=%d isomorphisms=%d best rms=%.4f max=%.4f"%(k+1,rdMolDescriptors.CalcMolFormula(fA),len(hvA),len(mts),best[0],best[1]))
    print("     pairs (1073->P 1-based):",[(a+1,b+1) for a,b in zip(best[2],best[3])])
# interfragment contacts
frA=[list(f) for f in Chem.GetMolFrags(mA)]; frP=[list(f) for f in Chem.GetMolFrags(mP)]
d=np.linalg.norm(PA[frA[0]][:,None,:]-PA[frA[1]][None,:,:],axis=2)
print("D) 1073 closest interfragment contacts:")
for kk in np.argsort(d,axis=None)[:4]:
    i,j=np.unravel_index(kk,d.shape); gi,gj=frA[0][i],frA[1][j]
    print("   %.4f : atom %d(%s) -- atom %d(%s)"%(d[i,j],gi+1,PT.GetElementSymbol(A[gi][0]),gj+1,PT.GetElementSymbol(A[gj][0])))
dp=np.linalg.norm(PB[frP[0]][:,None,:]-PB[frP[1]][None,:,:],axis=2)
print("   P closest:")
for kk in np.argsort(dp,axis=None)[:3]:
    i,j=np.unravel_index(kk,dp.shape); gi,gj=frP[0][i],frP[1][j]
    print("   %.4f : atom %d(%s) -- atom %d(%s)"%(dp[i,j],gi+1,PT.GetElementSymbol(B[gi][0]),gj+1,PT.GetElementSymbol(B[gj][0])))
