
import sys, math, itertools
import numpy as np
def read_xyz(p):
    L=open(p).read().splitlines(); n=int(L[0].split()[0])
    return [(t[0],float(t[1]),float(t[2]),float(t[3])) for t in (l.split() for l in L[2:2+n])]
def dih(A,a,b,c,d):
    p=[np.array(A[i-1][1:]) for i in (a,b,c,d)]
    b0=p[0]-p[1]; b1=p[2]-p[1]; b2=p[3]-p[2]
    b1n=b1/np.linalg.norm(b1)
    v=b0-np.dot(b0,b1n)*b1n; w=b2-np.dot(b2,b1n)*b1n
    return math.degrees(math.atan2(np.dot(np.cross(b1n,v),w), np.dot(v,w)))
files={'pt4':'gold_finish_20261015/HI1/E1/split/E1A_neg_scan_p4_R2542_branchA.xyz',
       'pt11':'gold_finish_20261015/HI1/E1/split/E1A_neg_scan_p11_R2192_branchB.xyz'}
A4=read_xyz(files['pt4']); A11=read_xyz(files['pt11'])
print('element order check (1-based):', {i:A4[i-1][0] for i in (2,3,14,15,16,17,18,27)})
for name,A in (('pt4',A4),('pt11(branchB)',A11)):
    print('---', name)
    for i in (2,3,14,15,16,17,18):
        print('   atom %2d (%s): %12.6f %12.6f %12.6f' % (i, A[i-1][0], A[i-1][1], A[i-1][2], A[i-1][3]))
    print('   dih(3,2,18,14) = %+8.2f   dih(14,18,2,3) = %+8.2f   dih(2,3,14,18) = %+8.2f' % (dih(A,3,2,18,14), dih(A,14,18,2,3), dih(A,2,3,14,18)))
    for X in (12,13,14,15,16,17):
        print('   dih(3,2,18,%2d) = %+8.2f   dih(3,2,18,%2d reversed) = %+8.2f' % (X, dih(A,3,2,18,X), X, dih(A,X,18,2,3)))
