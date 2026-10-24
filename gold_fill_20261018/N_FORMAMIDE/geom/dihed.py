import sys, numpy as np
def rd(f):
    L=open(f).read().split('\n')
    n=int(L[0]); out=[]
    for l in L[2:2+n]:
        p=l.split(); out.append((p[0],np.array(list(map(float,p[1:4])))))
    return out
def dih(a,b,c,d):
    b0=a-b; b1=c-b; b2=d-c
    b1n=b1/np.linalg.norm(b1)
    v=b0-np.dot(b0,b1n)*b1n; w=b2-np.dot(b2,b1n)*b1n
    return np.degrees(np.arctan2(np.dot(np.cross(b1n,v),w),np.dot(v,w)))
IS='build_I/prepared.xyz'
A=[x[1] for x in rd(IS)]
# file order: 1=N 2=C 3=O 4=H(N) 5=H(C) 6=H(O)
print('I seed d1 H(O)05-O3-C2-N1 (0-based 5,2,1,0) =', round(dih(A[5],A[2],A[1],A[0]),2))
print('I seed d2 O3-C2-N1-H(N) =', round(dih(A[2],A[1],A[0],A[3]),2))
print('I seed d3 H(C)-C2-N1-H(N) =', round(dih(A[4],A[1],A[0],A[3]),2))
print('I seed dist O3...H(N) =', round(float(np.linalg.norm(A[2]-A[3])),3))
R=[x[1] for x in rd('build_R/prepared.xyz')]
print('R seed H5(05)-N1-C2=O3 =', round(dih(R[4],R[0],R[1],R[2]),2))
print('R seed H4-N1-C2=O3 =', round(dih(R[3],R[0],R[1],R[2]),2))
print('R seed dist O3...H5 =', round(float(np.linalg.norm(R[2]-R[4])),3))
