
import sys, math
import numpy as np
Z={1:"H",6:"C",8:"O"}
CUT={(6,6):1.80,(6,8):1.55,(6,1):1.25,(8,8):1.60,(8,1):1.20,(1,1):0.90,(8,6):1.55}
def pcut(a,b):
    return CUT.get((a,b), CUT.get((b,a), 1.7))
def read_xyz(p):
    L=open(p).read().splitlines()
    n=int(L[0].split()[0]); at=[]
    for k in range(2,2+n):
        t=L[k].split(); at.append((k-1, Zinv(t[0]), float(t[1]),float(t[2]),float(t[3])))
    return at
def Zinv(s):
    return {"H":1,"C":6,"O":8}[s]
def bonds(at):
    out=[]
    for i in range(len(at)):
        for j in range(i+1,len(at)):
            d=math.dist(at[i][2:],at[j][2:])
            if d < pcut(at[i][1],at[j][1]): out.append((i+1,j+1,d))
    return out
def frags(at):
    parent=list(range(len(at)))
    def find(x):
        while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]
        return x
    for i,j,d in bonds(at):
        a,b=find(i-1),find(j-1)
        if a!=b: parent[a]=b
    return len({find(k) for k in range(len(at))})
def kabsch(A,B):
    A=A-A.mean(0); B=B-B.mean(0)
    V,S,W=np.linalg.svd(A.T@B); d=np.sign(np.linalg.det(V@W))
    R=V@np.diag([1,1,d])@W; Ar=A@R; dv=np.linalg.norm(Ar-B,axis=1)
    return math.sqrt((dv**2).mean()), dv
def desc(p):
    at=read_xyz(p); bs=bonds(at)
    heavy={}
    print("==",p)
    print("   elems:","".join(Z[a[1]] for a in at))
    for i,j,d in bs:
        if at[i-1][1]!=1 or at[j-1][1]!=1:
            print("   bond %s%d-%s%d %.3f"%(Z[at[i-1][1]],i,Z[at[j-1][1]],j,d), end="")
    print()
    print("   nfrag(connectivity)=%d"%frags(at))
    # proton ownership: each H bonded to O -> which O
    own=[]
    for i,j,d in bs:
        if at[i-1][1]==1 or at[j-1][1]==1:
            pass
    for k,a in enumerate(at):
        if a[1]==1:
            near=sorted([(math.dist(a[2:],b[2:]), b) for b in at if b[1]!=1])[0]
            hb=[(math.dist(a[2:],b[2:]), b) for b in at if b[1]==8]
            if hb:
                hb.sort()
                own.append("H%d -> O%d(%.3f)%s"%(k+1, hb[0][1][0], hb[0][0], "" if hb[0][0]<1.25 else " [no O-H bond]"))
    print("   H-on-O:","; ".join(own))
    # per heavy-atom coordination
    for k,a in enumerate(at):
        if a[1]!=1:
            nb=[ "%s%d(%.2f)"%(Z[at[j-1][1]],j,math.dist(a[2:],at[j-1][2:])) for j in [x for x,y,dd in bs if x==k+1 or y==k+1]]
            nb2=[]
            for x,y,dd in bs:
                if x==k+1: nb2.append("%s%d(%.2f)"%(Z[at[y-1][1]],y,dd))
                elif y==k+1: nb2.append("%s%d(%.2f)"%(Z[at[x-1][1]],x,dd))
            print("   %s%d: %s"%(Z[a[1]],k+1," ".join(sorted(nb2))))
    return at
paths=sys.argv[1:]
ats={}
for p in paths:
    ats[p]=desc(p)
# aligned rmsd matrix
print("\n-- aligned RMSD matrix (only meaningful when atom order matches) --")
import itertools
for p,q in itertools.combinations(paths,2):
    A=ats[p]; B=ats[q]
    if len(A)!=len(B): print(p,q,"len"); continue
    if any(Z[A[i][1]]!=Z[B[i][1]] for i in range(len(A))):
        print("  %s vs %s: ORDER MISMATCH -> skip"%(p.split('/')[-1],q.split('/')[-1])); continue
    rms,dv=kabsch(np.array([a[2:] for a in A]),np.array([b[2:] for b in B]))
    big=sorted(range(len(A)), key=lambda i:-dv[i])[:5]
    print("  %s vs %s: rms=%.3f max=%.3f big=%s"%(p.split('/')[-1],q.split('/')[-1],rms,dv.max(),
        " ".join("%s%d:%.2f"%(Z[A[i][1]],A[i][0],dv[i]) for i in big)))
