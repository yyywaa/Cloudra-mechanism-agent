import os, math
base="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NY3/E2E3"
gjf=os.path.join(base,"i2_min_readfc_optfreq/i2_min_readfc.gjf")
xyzf=os.path.join(base,"i2_min_candA.xyz")
def rd_gjf(p):
    L=open(p).read().splitlines(); out=[]
    for ln in L[8:]:
        f=ln.split()
        if len(f)==4: out.append((f[0],float(f[1]),float(f[2]),float(f[3])))
    return out
def rd_xyz(p):
    L=open(p).read().splitlines(); n=int(L[0].split()[0]); out=[]
    for ln in L[2:2+n]:
        f=ln.split(); out.append((f[0],float(f[1]),float(f[2]),float(f[3])))
    return out
a=rd_gjf(gjf); b=rd_xyz(xyzf)
print("gjf atoms",len(a),"xyz atoms",len(b))
print("gjf elem:", " ".join(x[0] for x in a))
print("xyz elem:", " ".join(x[0] for x in b))
if len(a)==len(b):
    d=[math.dist(a[i][1:],b[i][1:]) for i in range(len(a))]
    print("direct-order max delta = %.6f A ; per-atom:"%max(d), " ".join("%.3f"%x for x in d))
    for i in range(len(a)):
        if d[i]>0.02: print("  atom",i+1,a[i][0],"gjf",[round(v,4) for v in a[i][1:]],"xyz",[round(v,4) for v in b[i][1:]])