
import math, sys
def read_gjf(p):
    L=open(p).read().splitlines()
    i=L.index('0 1')
    at=[]
    for line in L[i+1:]:
        t=line.split()
        if len(t)==4: at.append((t[0],float(t[1]),float(t[2]),float(t[3])))
        else: break
    return at
def read_xyz(p):
    L=open(p).read().splitlines(); n=int(L[0].split()[0])
    return [(t[0],float(t[1]),float(t[2]),float(t[3])) for t in (l.split() for l in L[2:2+n])]
base='gold_finish_20261015/HI1/E1/split/'
G=read_gjf(base+'E1A_scan_cont1_C2N18.gjf'); P=read_xyz(base+'E1A_neg_scan_p11_R2192_branchB.xyz')
print('natoms gjf=%d p11=%d ; elements identical=%s' % (len(G), len(P), [a[0] for a in G]==[a[0] for a in P]))
mx=max(math.dist(G[k][1:], P[k][1:]) for k in range(len(G)))
print('max per-atom |delta| vs my p11 frame = %.12f A' % mx)
d=lambda A,a,b: math.dist(A[a-1][1:],A[b-1][1:])
print('gjf: R(2,18)=%.4f R(3,27)=%.4f R(18,27)=%.4f R(13,19)=%.4f R(2,3)=%.4f' % (d(G,2,18),d(G,3,27),d(G,18,27),d(G,13,19),d(G,2,3)))
print('p11: R(2,18)=%.4f R(3,27)=%.4f R(18,27)=%.4f R(13,19)=%.4f R(2,3)=%.4f' % (d(P,2,18),d(P,3,27),d(P,18,27),d(P,13,19),d(P,2,3)))
