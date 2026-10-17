import numpy as np, math
LOG="gold_finish_20261015/HI1/E3/runs/e3b_scan2d_c2n4_o25h26.log"
L=open(LOG).read().splitlines()
blocks=[]; i=0
while i < len(L):
    if "Input orientation:" in L[i]:
        k=i+1; coords=[]; els=[]
        while k < len(L) and len(coords) < 41:
            p=L[k].split()
            if len(p)==6 and p[0].isdigit() and p[1].isdigit():
                els.append(int(p[1])); coords.append((float(p[3]),float(p[4]),float(p[5])))
            k+=1
        if len(coords)==41: blocks.append((i+1,coords,els))
        i=k
    else: i+=1
X=np.array(blocks[-1][1]); els=blocks[-1][2]
heavy=np.array([e!=1 for e in els])
print("source frame: L%d of %s, %d atoms (%d heavy, %d H)" % (blocks[-1][0], LOG, len(X), heavy.sum(), (~heavy).sum()))

def kabsch(A,B):
    A=np.array(A,dtype=float); B=np.array(B,dtype=float)
    A=A-A.mean(0); B=B-B.mean(0)
    U,S,Vt=np.linalg.svd(A.T@B)
    d=np.sign(np.linalg.det(U@Vt))
    R=U@np.diag([1.0,1.0,d])@Vt
    return float(np.sqrt((((A@R)-B)**2).sum()/len(A))), float(np.linalg.det(R))

def rotmat(ax,th):
    ax=np.array(ax,dtype=float); ax/=np.linalg.norm(ax)
    c,s=np.cos(th),np.sin(th); x,y,z=ax
    return np.array([[c+x*x*(1-c), x*y*(1-c)-z*s, x*z*(1-c)+y*s],
                     [y*x*(1-c)+z*s, c+y*y*(1-c), y*z*(1-c)-x*s],
                     [z*x*(1-c)-y*s, z*y*(1-c)+x*s, c+z*z*(1-c)]])

print("--- kabsch() self-checks (identical routine to prep/scan2d_pointcheck.py) ---")
ok=True
for tag,sel in (("all 41 atoms",np.ones(41,bool)),("heavy 20 atoms",heavy)):
    A=X[sel]
    Rp=rotmat([0.31,-0.77,0.55],0.9123); t=np.array([3.7,-11.2,5.9])
    r1,d1=kabsch(A,A@Rp.T+t)
    r3,d3=kabsch(A,A.copy())
    M=np.diag([1.0,1.0,-1.0]).dot(rotmat([0.0,1.0,0.0],0.4))
    r2,d2=kabsch(A,A@M.T+t)
    print("[%s]" % tag)
    print("  (1) rotation+translation : RMSD=%.3e A   det(R_opt)=%+.12f   -> %s" % (r1,d1,"PASS (expected 0, det +1)" if r1<1e-8 and abs(d1-1)<1e-9 else "FAIL"))
    print("  (2) mirrored (improper)  : RMSD=%.6f A   det(R_opt)=%+.12f   -> %s" % (r2,d2,"PASS (expected >0, det +1)" if r2>0.1 and abs(d2-1)<1e-9 else "FAIL"))
    print("  (3) identical copy       : RMSD=%.3e A   det(R_opt)=%+.12f   -> %s" % (r3,d3,"PASS (expected 0, det +1)" if r3<1e-12 and abs(d3-1)<1e-9 else "FAIL"))
    ok = ok and r1<1e-8 and r3<1e-12 and r2>0.1 and abs(d1-1)<1e-9 and abs(d2-1)<1e-9 and abs(d3-1)<1e-9
print("overall:", "ALL PASS" if ok else "FAIL")
