
import numpy as np, sys
def read_xyz(p):
    L=open(p).read().splitlines(); n=int(L[0].split()[0])
    return [(t[0],float(t[1]),float(t[2]),float(t[3])) for t in (l.split() for l in L[2:2+n])]
def kabsch(A,B,idx):
    PA=np.array([[A[i-1][1],A[i-1][2],A[i-1][3]] for i in idx]); PB=np.array([[B[i-1][1],B[i-1][2],B[i-1][3]] for i in idx])
    QA=PA-PA.mean(0); QB=PB-PB.mean(0)
    H=QB.T@QA; U,S,Vt=np.linalg.svd(H)
    dd=np.sign(np.linalg.det(Vt.T@U.T)); R=Vt.T@np.diag([1,1,dd])@U.T
    QB2=(R@QB.T).T; disp=np.linalg.norm(QB2-QA,axis=1)
    return float(np.sqrt((disp**2).mean())), float(disp.max()), int(np.argmax(disp))+1, float(np.linalg.det(R))
A=read_xyz('/tmp/cont1_p1.xyz'); B=read_xyz('/tmp/cont1_p2.xyz')
heavy=[1,2,3,4,11,12,13,14,15,16,17,18]
print('pt1->pt2 heavy12: rms %.4f  max %.4f (atom %d)  det %+.3f' % kabsch(A,B,heavy))
print('pt1->pt2 all27  : rms %.4f  max %.4f (atom %d)  det %+.3f' % kabsch(A,B,list(range(1,28))))
