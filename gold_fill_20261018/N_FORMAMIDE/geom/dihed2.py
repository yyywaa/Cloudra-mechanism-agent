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
for f in ['build_I/prepared.xyz','I2_seed.xyz','I3_seed.xyz']:
    A=[x[1] for x in rd(f)]
    print(f, 'd1[O1-H(O)-O3? ] H(O)(6)-O(3)-C(2)-N(1)=',round(dih(A[5],A[2],A[1],A[0]),1),
      '| d2 O(3)-C(2)-N(1)-HN(4)=',round(dih(A[2],A[1],A[0],A[3]),1),
      '| d3 HC(5)-C(2)-N(1)-HN(4)=',round(dih(A[4],A[1],A[0],A[3]),1),
      '| r(O...HN)=',round(float(np.linalg.norm(A[2]-A[3])),3),
      '| r(O...HC)=',round(float(np.linalg.norm(A[2]-A[4])),3))
