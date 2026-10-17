
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
for tag,f in (("1073","1073_freq_final_frame.xyz"),("P","P_1061_last_frame.xyz")):
    X=xyzf(f); P=np.array([[x,y,z] for _,x,y,z in X]); m=mol(X)
    fr=[list(g) for g in Chem.GetMolFrags(m)]
    print("### %s fragment sizes %s"%(tag,[len(g) for g in fr]))
    print("   elem seq:","".join(PT.GetElementSymbol(a[0]) for a in X))
    if len(fr)==2:
        d=np.linalg.norm(P[fr[0]][:,None,:]-P[fr[1]][None,:,:],axis=2)
        for k in np.argsort(d,axis=None)[:6]:
            i,j=np.unravel_index(k,d.shape); gi,gj=fr[0][i],fr[1][j]
            print("   %.4f  atom %d(%s) -- atom %d(%s)"%(d[i,j],gi+1,PT.GetElementSymbol(X[gi][0]),gj+1,PT.GetElementSymbol(X[gj][0])))
