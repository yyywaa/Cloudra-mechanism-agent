import numpy as np
def rd(f):
    L=open(f).read().split('\n'); n=int(L[0]); out=[]
    for l in L[2:2+n]:
        p=l.split(); out.append((p[0],np.array(list(map(float,p[1:4])))))
    return out
def dih(a,b,c,d):
    b0=a-b; b1=c-b; b2=d-c; b1n=b1/np.linalg.norm(b1)
    v=b0-np.dot(b0,b1n)*b1n; w=b2-np.dot(b2,b1n)*b1n
    return np.degrees(np.arctan2(np.dot(np.cross(b1n,v),w),np.dot(v,w)))
def d(a,b): return float(np.linalg.norm(a-b))
A=[x[1] for x in rd('geom/R_syn_opt.xyz')]
print('R_syn_opt  order N,C,O,H_N1,H_N2,H_C')
print('  H_N1(4)-N-C=O =',round(dih(A[3],A[0],A[1],A[2]),2),' H_N2(5)-N-C=O =',round(dih(A[4],A[0],A[1],A[2]),2))
print('  r(O...H_N1)=',round(d(A[2],A[3]),3),' r(O...H_N2)=',round(d(A[2],A[4]),3),' r(C-O)=',round(d(A[1],A[2]),3),' r(C-N)=',round(d(A[1],A[0]),3))
for f in ['geom/I1_opt.xyz','geom/I2_opt.xyz']:
    B=[x[1] for x in rd(f)]
    print(f,' order N,C,O,H_N,H_C,H_O')
    print('  d1 H_O(6)-O-C-N =',round(dih(B[5],B[2],B[1],B[0]),2),' d2 O-C-N-H_N(4) =',round(dih(B[2],B[1],B[0],B[3]),2),
          ' r(O...H_N)=',round(d(B[2],B[3]),3),' r(C-O)=',round(d(B[1],B[2]),3),' r(C-N)=',round(d(B[1],B[0]),3))
