import itertools, numpy as np
def rd(p):
    L=open(p).read().split("\n")
    n=int(L[0].split()[0]); at=[]; xyz=[]
    for l in L[2:2+n]:
        s=l.split(); at.append(s[0]); xyz.append([float(v) for v in s[1:4]])
    return at, np.array(xyz)
files=["gold_fill_20261018/HI1/HI1_E1b/build/ts_guess_27.xyz",
       "gold_finish_20261015/HI1/E1/split/INT1_27_opt_frame.xyz",
       "gold_fill_20261018/HI1/HI1_E1b/build/product_start_27.xyz"]
for p in files:
    at,X=rd(p)
    d=lambda i,j: float(np.linalg.norm(X[i-1]-X[j-1]))
    m=min((np.linalg.norm(X[i]-X[j]),i+1,j+1) for i,j in itertools.combinations(range(len(at)),2))
    heavy=[i for i,a in enumerate(at) if a!="H"]
    hm=min((np.linalg.norm(X[i]-X[j]),i+1,j+1) for i in heavy for j in range(len(at)) if j!=i)
    print(p)
    print("  natoms",len(at),"elem"," ".join(at))
    print("  minsep(any)=%.4f (%d-%d)  minsep(heavy-other)=%.4f (%d-%d)"%(m[0],m[1],m[2],hm[0],hm[1],hm[2]))
    print("  R(2,4)C2C3=%.4f R(3,10)O4H22=%.4f R(4,10)C3H22=%.4f R(2,3)C2O4=%.4f R(3,27)O4H21=%.4f R(2,18)C2N20=%.4f R(2,10)C2H22=%.4f"%(d(2,4),d(3,10),d(4,10),d(2,3),d(3,27),d(2,18),d(2,10)))
