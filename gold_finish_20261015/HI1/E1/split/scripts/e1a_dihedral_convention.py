
import math
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
base='gold_finish_20261015/HI1/E1/split/'
A4=read_xyz(base+'E1A_neg_scan_p4_R2542_branchA.xyz')
A11=read_xyz(base+'E1A_neg_scan_p11_R2192_branchB.xyz')
for nm,A in (('pt4',A4),('pt11',A11)):
    print('%s: dih(3,2,18,14)=%+8.2f  dih(3,2,14,18)=%+8.2f  sum=%.2f  |180-dih(3,2,18,14)|=%+8.2f' % (nm, dih(A,3,2,18,14), dih(A,3,2,14,18), dih(A,3,2,18,14)+dih(A,3,2,14,18), abs(180-abs(dih(A,3,2,18,14)))*1.0))
print()
print('identity check: dih(a,b,c,d) = -dih(d,c,b,a):', dih(A4,3,2,18,14), dih(A4,14,18,2,3))
