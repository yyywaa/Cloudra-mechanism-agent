import sys, math
import numpy as np
def read(p):
    L=open(p).read().splitlines(); n=int(L[0].split()[0])
    return [np.array([float(x) for x in l.split()[1:4]]) for l in L[2:2+n]]
def dih(p0,p1,p2,p3):
    b1=p1-p0; b2=p2-p1; b3=p3-p2
    n1=np.cross(b1,b2); n2=np.cross(b2,b3)
    m=np.cross(n1,b2/np.linalg.norm(b2))
    return math.degrees(math.atan2(float(np.dot(n1,n2)), float(np.dot(m,n2))))
for f in sys.argv[1:]:
    a=read(f)
    print('%-46s tau(3,2,18,14)=%+8.2f  R(2,18)=%.4f  R(2,3)=%.4f  R(18,27)=%.4f  O3..H27=%.4f' % (f.split('/')[-1], dih(a[2],a[1],a[17],a[13]), np.linalg.norm(a[1]-a[17]), np.linalg.norm(a[1]-a[2]), np.linalg.norm(a[17]-a[26]), np.linalg.norm(a[2]-a[26])))