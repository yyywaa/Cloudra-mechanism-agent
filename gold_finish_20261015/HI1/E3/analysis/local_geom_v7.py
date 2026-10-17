
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
A=xyzf("1073_freq_final_frame.xyz"); PA=np.array([[x,y,z] for _,x,y,z in A]); mA=mol(A)
def d(i,j): return float(np.linalg.norm(PA[i-1]-PA[j-1]))
for i in (1,2,5,6,32):
    nb=[(n.GetIdx()+1,PT.GetElementSymbol(n.GetAtomicNum())) for n in mA.GetAtomWithIdx(i-1).GetNeighbors()]
    print("atom %d (%s) neighbours with R:"%(i,PT.GetElementSymbol(A[i-1][0])),[(k,s,round(d(i,k),4)) for k,s in nb])
print("C2...N32 = %.4f" % d(2,32))
print("O3...O27 = %.4f ; O3...H33 = %.4f ; O27-H33 = %.4f" % (d(3,27), d(3,33), d(27,33)))
print("C26...N32 = %.4f (proline Calpha-N)" % d(26,32))
print("C2-O6 = %.4f ; C5-O6 = %.4f" % (d(2,6), d(5,6)))
