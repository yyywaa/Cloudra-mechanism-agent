
import numpy as np
p="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan.log"
ls=open(p).read().splitlines()
def frame(hdr):
    d=[k for k in range(hdr,hdr+10) if ls[k].strip().startswith('-----')]
    a=[];k=d[1]+1
    while not ls[k].strip().startswith('-----'):
        q=ls[k].split(); a.append((int(q[1]),float(q[3]),float(q[4]),float(q[5]))); k+=1
    return a
def kab(P,Q):
    Pc=P-P.mean(0); Qc=Q-Q.mean(0); H=Pc.T@Qc; U,S,Vt=np.linalg.svd(H)
    d=np.sign(np.linalg.det(Vt.T@U.T)); R=Vt.T@np.diag([1.,1.,d])@U.T
    dev=np.linalg.norm((R@Pc.T).T-Qc,axis=1); return float(np.sqrt((dev**2).mean())),float(dev.max())
f1=frame(14777); f2=frame(23076); f3=frame(33028)
X=lambda f,i: np.array([f[i][1],f[i][2],f[i][3]])
heavy=[i for i in range(41) if f1[i][0]>1]; allat=list(range(41))
for (a,b,tag) in ((f1,f2,"1->2"),(f2,f3,"2->3")):
    A=np.array([X(a,i) for i in heavy]); B=np.array([X(b,i) for i in heavy])
    r,mx=kab(A,B); print("%s heavy20 rms=%.4f max=%.4f"%(tag,r,mx))
    A=np.array([X(a,i) for i in allat]); B=np.array([X(b,i) for i in allat])
    r2,mx2=kab(A,B); print("%s all41  rms=%.4f max=%.4f"%(tag,r2,mx2))
    # heavy-only rms under rotation fitted on all 41
    Pc=A-A.mean(0); Qc=B-B.mean(0); H=Pc.T@Qc; U,S,Vt=np.linalg.svd(H)
    d=np.sign(np.linalg.det(Vt.T@U.T)); R=Vt.T@np.diag([1.,1.,d])@U.T
    Ah=np.array([X(a,i) for i in heavy]); Bh=np.array([X(b,i) for i in heavy])
    dev=np.linalg.norm(((R@(Ah-A.mean(0)).T).T+B.mean(0))-Bh,axis=1)
    print("%s heavy20 under all41 rotation rms=%.4f max=%.4f"%(tag,float(np.sqrt((dev**2).mean())),float(dev.max())))
