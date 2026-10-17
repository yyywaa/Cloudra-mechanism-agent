import numpy as np, re
LOG="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/runs/e3b_scan2d_c2n4_o25h26.log"
L=open(LOG).read().splitlines()
blocks=[];i=0
while i<len(L):
    if "Input orientation:" in L[i] or "Standard orientation:" in L[i]:
        k=i+1;co=[];el=[]
        while k<len(L) and len(co)<41:
            p=L[k].split()
            if len(p)==6 and p[0].isdigit() and p[1].isdigit():
                el.append(int(p[1]));co.append([float(p[3]),float(p[4]),float(p[5])])
            k+=1
        if len(co)==41: blocks.append((i+1,np.array(co),el))
        i=k
    else: i+=1
scf=[(i+1,float(re.search(r"E\(RB3LYP\) =\s*(-?\d+\.\d+)",ln).group(1))) for i,ln in enumerate(L) if "SCF Done" in ln]
opt=[i+1 for i,ln in enumerate(L) if "Optimization completed." in ln]
def kabsch(A,B):
    Ac=A-A.mean(0); Bc=B-B.mean(0)
    H=Ac.T@Bc; U,S,Vt=np.linalg.svd(H); d=np.sign(np.linalg.det(Vt.T@U.T))
    D=np.diag([1,1,d]); R=Vt.T@D@U.T
    Ar=(R@Ac.T).T
    dev=np.linalg.norm(Ar-Bc,axis=1)
    return float(np.sqrt((dev**2).mean())), float(dev.max()), float(np.linalg.det(R))
pts=[]
for oc in opt:
    cand=[b for b in blocks if b[0]<oc]
    b=cand[-1]; e=[en for l,en in scf if l<oc][-1]; ln=[l for l,en in scf if l<oc][-1]
    pts.append(dict(oc=oc,hdr=b[0],X=b[1],el=b[2],E=e,ln=ln))
k=627.5095
print("=== column-1 energies relative to grid point 1 (job 1028 reproduction) ===")
E1=pts[0]["E"]
for n,p in enumerate(pts,1):
    print("scan#%d  E=%.9f (SCF L%d)  dE=%+7.2f kcal/mol  (4dp %+8.4f)" % (n,p["E"],p["ln"],(p["E"]-E1)*k,(p["E"]-E1)*k))
print()
print("=== adjacent-point Kabsch (fit=20 heavy, eval=20 heavy; SVD, det=+1, mirror forbidden) ===")
heavy=[i for i in range(41) if pts[0]["el"][i]!=1]
print("heavy atom count:",len(heavy))
for n in range(len(pts)-1):
    A=pts[n]["X"][heavy]; B=pts[n+1]["X"][heavy]
    r,m,d=kabsch(A,B)
    A41=pts[n]["X"];B41=pts[n+1]["X"]
    r41,m41,d41=kabsch(A41,B41)
    print("scan#%d->#%d heavy20: rms %.4f max %.4f det %+.1f | all41: rms %.4f max %.4f det %+.1f" % (n+1,n+2,r,m,d,r41,m41,d41))
print()
print("=== synthesis self-checks (must pass before any Kabsch value is quoted) ===")
rng=np.random.default_rng(7)
X=pts[0]["X"]
th=0.7; Rz=np.array([[np.cos(th),-np.sin(th),0],[np.sin(th),np.cos(th),0],[0,0,1]])
t=np.array([1.3,-0.7,2.1])
r1,m1,d1=kabsch(X,(X@Rz.T)+t); print("  (1) rigid rotation+translation  -> rms %.3e max %.3e det %+.1f (expect 0)" % (r1,m1,d1))
Xm=X.copy(); Xm[:,0]*=-1
r2,m2,d2=kabsch(X,Xm); print("  (2) mirrored copy               -> rms %.4f max %.4f det %+.1f (expect >0, det<0 if mirror allowed)" % (r2,m2,d2))
r3,m3,d3=kabsch(X,X.copy()); print("  (3) identical copy              -> rms %.3e max %.3e det %+.1f (expect 0)" % (r3,m3,d3))
