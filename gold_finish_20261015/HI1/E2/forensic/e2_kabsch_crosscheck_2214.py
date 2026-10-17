
import math, hashlib, datetime
LOG="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan.log"
data=open(LOG,"rb").read()
print("snapshot", datetime.datetime.now().astimezone().isoformat(timespec="seconds"))
print("lines", data.count(b"\n"), "sha", hashlib.sha256(data).hexdigest(), "bytes", len(data))
lines=data.decode("utf-8","replace").splitlines()
# blocks
blocks=[]; i=0
while i < len(lines):
    if lines[i].strip().startswith("Standard orientation:"):
        j=i+1; d=0
        while j<len(lines) and d<2:
            if lines[j].strip().startswith("-----"): d+=1
            j+=1
        co={}; k=j
        while k<len(lines) and not lines[k].strip().startswith("-----"):
            p=lines[k].split()
            if len(p)==6:
                co[int(p[0])]=(int(p[1]),float(p[3]),float(p[4]),float(p[5]))
            k+=1
        blocks.append((k,co)); i=k
    else: i+=1
oc=[i for i,l in enumerate(lines) if "Optimization completed" in l]
frames=[]
for d in oc:
    c=[b for b in blocks if b[0]<d][-1]
    frames.append(c[1])
print("conv frames", len(frames))
heavy=[a for a in frames[0] if frames[0][a][0]!=1]
print("heavy count", len(heavy))
def kabsch(A,B):
    ca=[sum(p[i] for p in A)/len(A) for i in (1,2,3)]
    P=[[p[i]-ca[i-1] for i in (1,2,3)] for p in A]
    cb=[sum(p[i] for p in B)/len(B) for i in (1,2,3)]
    Q=[[p[i]-cb[i-1] for i in (1,2,3)] for p in B]
    H=[[sum(P[k][i]*Q[k][j] for k in range(len(P))) for j in range(3)] for i in range(3)]
    import itertools
    # Jacobi-free: use numpy if available
    try:
        import numpy as np
        Hm=np.array(H); U,S,Vt=np.linalg.svd(Hm); d=np.sign(np.linalg.det(Vt.T@U.T))
        D=np.diag([1,1,d]); R=Vt.T@D@U.T
        Pp=np.array(P); Qp=np.array(Q)@R.T
        diff=Pp-Qp
        dist=np.linalg.norm(diff,axis=1)
        return float(np.sqrt((dist**2).mean())), float(dist.max())
    except ImportError:
        return None,None
for n in range(len(frames)-1):
    A=[frames[n][a] for a in heavy]; B=[frames[n+1][a] for a in heavy]
    r,m=kabsch(A,B)
    print(f"pair {n+1}-{n+2}: rmsd={r:.4f} max={m:.4f}")
