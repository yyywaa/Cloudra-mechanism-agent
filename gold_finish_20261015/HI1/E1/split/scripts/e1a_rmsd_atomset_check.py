
import numpy as np
def read_xyz(p):
    L=open(p).read().splitlines(); n=int(L[0].split()[0])
    return [(t[0],float(t[1]),float(t[2]),float(t[3])) for t in (l.split() for l in L[2:2+n])]
def kabsch(A,B,idx):
    PA=np.array([[A[i-1][1],A[i-1][2],A[i-1][3]] for i in idx]); PB=np.array([[B[i-1][1],B[i-1][2],B[i-1][3]] for i in idx])
    QA=PA-PA.mean(0); QB=PB-PB.mean(0)
    H=QB.T@QA; U,S,Vt=np.linalg.svd(H)
    d=np.sign(np.linalg.det(Vt.T@U.T)); R=Vt.T@np.diag([1,1,d])@U.T
    QB2=(R@QB.T).T; disp=np.linalg.norm(QB2-QA,axis=1)
    return float(np.sqrt((disp**2).mean())), float(disp.max()), int(np.argmax(disp))+1
base='gold_finish_20261015/HI1/E1/split/'
A=read_xyz(base+'E1A_neg_scan_p4_R2542_branchA.xyz'); B=read_xyz(base+'E1A_neg_scan_p11_R2192_branchB.xyz')
allidx=list(range(1,28)); heavy=[1,2,3,4,11,12,13,14,15,16,17,18]
r1=kabsch(A,B,allidx); r2=kabsch(A,B,heavy)
print('pt4 -> pt11 : all-27-atom RMSD %.3f A (max %.3f at atom %d)' % r1)
print('pt4 -> pt11 : heavy-12   RMSD %.3f A (max %.3f at atom %d)' % r2)
