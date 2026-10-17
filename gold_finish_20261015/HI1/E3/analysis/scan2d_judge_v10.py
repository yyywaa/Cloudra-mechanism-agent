
import numpy as np
from rdkit import Chem
PT=Chem.GetPeriodicTable()
K=627.5095
p="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/runs/e3b_scan2d_c2n4_o25h26.log"
ls=open(p).read().splitlines()
def kab(P,Q):
    Pc=P-P.mean(0); Qc=Q-Q.mean(0); H=Pc.T@Qc; U,S,Vt=np.linalg.svd(H)
    d=np.sign(np.linalg.det(Vt.T@U.T)); R=Vt.T@np.diag([1.,1.,d])@U.T
    dev=np.linalg.norm((R@Pc.T).T-Qc,axis=1); return float(np.sqrt((dev**2).mean())),float(dev.max()),float(np.linalg.det(R))
rng=np.random.default_rng(2026); X=rng.normal(size=(20,3)); th=0.85
Rm=np.array([[np.cos(th),-np.sin(th),0],[np.sin(th),np.cos(th),0],[0,0,1]]); t=np.array([1.2,-0.7,2.1])
print("SC(i)  rot+trans -> %.3e"%kab(X,X@Rm.T+t)[0])
print("SC(ii) mirror(allowed) -> %.6f"%kab(X,X*np.array([1,-1,1]))[0])
print("SC(iii) identical copy -> %.3e"%kab(X,X)[0])
oc=[i for i,l in enumerate(ls) if 'Optimization completed' in l]
def frame_before(idx):
    h=[j for j in range(idx) if 'Standard orientation' in ls[j]][-1]
    d=[k for k in range(h,h+10) if ls[k].strip().startswith('-----')]
    a=[];k=d[1]+1
    while not ls[k].strip().startswith('-----'):
        q=ls[k].split(); a.append((int(q[1]),float(q[3]),float(q[4]),float(q[5]))); k+=1
    assert len(a)==41
    assert ls[k].strip().startswith('-----')
    return h,d[1]+1,a
pts=[]
for n,i in enumerate(oc,1):
    h,ab,a=frame_before(i); Xg=np.array([[x,y,z] for _,x,y,z in a])
    j=[k for k in range(i) if 'SCF Done' in ls[k]][-1]
    E=float(ls[j].split('=')[1].split()[0])
    d=lambda u,v: float(np.linalg.norm(Xg[u-1]-Xg[v-1]))
    hn=min([(d(26,k),k+1,PT.GetElementSymbol(a[k-1][0])) for k in range(1,42) if a[k-1][0]>1 and k!=26])
    pts.append(dict(n=n,opt=i+1,hdr=h+1,ab=ab,scf=j+1,E=E,X=Xg,a=a,R24=d(2,4),R2526=d(25,26),R426=d(4,26),R1027=d(10,27),R225=d(2,25),hn=hn))
heavy=[i for i in range(41) if pts[0]['a'][i][0]>1]
print("heavy count",len(heavy))
E0=pts[0]['E']
for q in pts:
    print("pt%d OPT L%d hdr L%d atomL%d SCF L%d E=%.9f dE=%+7.2f R(2,4)=%.4f R(25,26)=%.4f R(4,26)=%.4f R(10,27)=%.4f R(2,25)=%.4f H26near=%d%s %.4f"%(
        q['n'],q['opt'],q['hdr'],q['ab'],q['scf'],q['E'],(q['E']-E0)*K,q['R24'],q['R2526'],q['R426'],q['R1027'],q['R225'],q['hn'][1],q['hn'][2],q['hn'][0]))
for k in range(len(pts)-1):
    A=pts[k]['X'][heavy]; B=pts[k+1]['X'][heavy]
    r,mx,det=kab(A,B)
    print("Kabsch pt%d->pt%d heavy20 rms=%.4f max=%.4f det=%+.3f"%(k+1,k+2,r,mx,det))
print("--- candidate test (approved symmetric criterion) ---")
for k,q in enumerate(pts):
    prev = pts[k-1]['E'] if k>0 else None
    nxt = pts[k+1]['E'] if k+1<len(pts) else None
    along = None
    if prev is not None and nxt is not None:
        along = "max" if (q['E']>prev and q['E']>nxt) else ("min" if (q['E']<prev and q['E']<nxt) else "monotone")
    print("  pt%d row%d col1: E-along-R(2,4)=%s ; col1 is FIRST column => boundary, candidate=NO ; at-boundary=YES"%(q['n'],q['n'],along))
sp=[i for i,l in enumerate(ls) if 'on scan point' in l]
print("last step line L%d: %s"%(sp[-1]+1,ls[sp[-1]].strip()))
print("termination counts:",sum(1 for l in ls if 'Normal termination' in l),sum(1 for l in ls if 'Error termination' in l))
