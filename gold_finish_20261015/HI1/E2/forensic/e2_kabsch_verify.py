
import numpy as np
from rdkit import Chem
PT=Chem.GetPeriodicTable()
p="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan.log"
ls=open(p).read().splitlines()
def frame(hdr):
    d=[k for k in range(hdr,hdr+10) if ls[k].strip().startswith('-----')]
    a=[];k=d[1]+1
    while not ls[k].strip().startswith('-----'):
        q=ls[k].split(); a.append((int(q[1]),float(q[3]),float(q[4]),float(q[5]))); k+=1
    assert len(a)==41, len(a)
    return a,k
def kab(P,Q):
    Pc=P-P.mean(0); Qc=Q-Q.mean(0); H=Pc.T@Qc; U,S,Vt=np.linalg.svd(H)
    d=np.sign(np.linalg.det(Vt.T@U.T)); R=Vt.T@np.diag([1.,1.,d])@U.T
    dev=np.linalg.norm((R@Pc.T).T-Qc,axis=1); return float(np.sqrt((dev**2).mean())),float(dev.max()),float(np.linalg.det(R))
# self-checks
rng=np.random.default_rng(11); X=rng.normal(size=(20,3))
th=1.1; Rm=np.array([[np.cos(th),-np.sin(th),0],[np.sin(th),np.cos(th),0],[0,0,1]]); t=np.array([0.4,1.5,-2.0])
print("SC(i) rot+trans  -> %.3e"%kab(X,X@Rm.T+t)[0])
print("SC(ii) mirror(allowed) -> %.6f"%kab(X,X*np.array([1,-1,1]))[0])
print("SC(ii-b) det of fitted R on mirror = %+.6f (production forces +1)"%kab(X,X*np.array([1,-1,1]))[2])
print("SC(iii) identical copy -> %.3e"%kab(X,X)[0])
Hs=[(0,14777),(1,23076),(2,33028)]
fr=[]
for n,h in Hs:
    a,_=frame(h); fr.append(a)
    print("frame%d hdr L%d  first/last atom lines parsed ok  N=%d"%(n+1,h+1,len(a)))
heavy=[i for i in range(41) if fr[0][i][0]>1]
print("heavy count:",len(heavy),"(20 expected) elem seq:", "".join(PT.GetElementSymbol(fr[0][i][0]) for i in heavy))
for k in range(2):
    A=np.array([[fr[k][i][1],fr[k][i][2],fr[k][i][3]] for i in heavy])
    B=np.array([[fr[k+1][i][1],fr[k+1][i][2],fr[k+1][i][3]] for i in heavy])
    r,mx,det=kab(A,B)
    print("Kabsch frame%d->%d : rms=%.4f max=%.4f det(R)=%+.6f"%(k+1,k+2,r,mx,det))
