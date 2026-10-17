
import math, hashlib, datetime
import numpy as np
LOG="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan.log"
data=open(LOG,"rb").read()
print("snapshot", datetime.datetime.now().astimezone().isoformat(timespec="seconds"), "lines", data.count(b"\n"), "sha", hashlib.sha256(data).hexdigest()[:16])
lines=data.decode("utf-8","replace").splitlines()
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
            if len(p)==6: co[int(p[0])]=(int(p[1]),float(p[3]),float(p[4]),float(p[5]))
            k+=1
        blocks.append((k,co)); i=k
    else: i+=1
oc=[i for i,l in enumerate(lines) if "Optimization completed" in l]
frames=[ [b for b in blocks if b[0]<d][-1][1] for d in oc]
heavy=[a for a in frames[0] if frames[0][a][0]!=1]
def rms(A,B,mode):
    A=np.array(A); B=np.array(B)
    P=A[:,1:]; Q=B[:,1:]
    P=P-P.mean(0); Q=Q-Q.mean(0)
    if mode=="C_QtP": C=Q.T@P
    else: C=P.T@Q
    U,S,Vt=np.linalg.svd(C)
    d=np.sign(np.linalg.det(Vt.T@U.T))
    R=Vt.T@np.diag([1,1,d])@U.T
    if mode=="C_QtP":
        Qp=Q@R.T       # variant 1
    elif mode=="C_PtQ_T":
        Qp=(R@Q.T).T   # variant 2 (transposed usage -> suspected A-row bug)
    else:
        Qp=Q@R
    dist=np.linalg.norm(P-Qp,axis=1)
    return math.sqrt((dist**2).mean()), dist.max()
for mode in ("C_QtP","C_PtQ_T"):
    out=[]
    for n in range(len(frames)-1):
        A=[frames[n][a] for a in heavy]; B=[frames[n+1][a] for a in heavy]
        r,m=rms(A,B,mode); out.append(f"{r:.4f}/{m:.4f}")
    print(mode, " | ".join(out))
