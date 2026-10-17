import json, math
import numpy as np

BASE="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/"
LOG1073=BASE+"runs/build_seed_product_optfreq.log"
PLOG=BASE+"runs/P_e3b/P_optfreq.log"
HEMI=BASE+"prep/hemiaminal_1028_lastframe.xyz"
MAP=BASE+"prep/seed_to_P_mapping_v4.json"

def blocks(path):
    L=open(path).read().splitlines(); out=[]; i=0
    while i < len(L):
        if "Input orientation:" in L[i] or "Standard orientation:" in L[i]:
            k=i+1; co=[]; el=[]
            while k < len(L) and len(co) < 41:
                p=L[k].split()
                if len(p)==6 and p[0].isdigit() and p[1].isdigit():
                    el.append(int(p[1])); co.append([float(p[3]),float(p[4]),float(p[5])])
                k+=1
            if len(co)==41: out.append((i+1,np.array(co),el,("Input" if "Input" in L[i] else "Standard")))
            i=k
        else: i+=1
    return out

def xyz(path):
    L=open(path).read().splitlines()
    n=int(L[0].split()[0]); co=[]; el=[]
    for ln in L[2:2+n]:
        p=ln.split(); el.append(p[0]); co.append([float(p[1]),float(p[2]),float(p[3])])
    Z={"H":1,"C":6,"N":7,"O":8}
    return np.array(co), np.array([Z[e] for e in el]), n

def kabsch(A,B):
    A=np.array(A,float); B=np.array(B,float)
    A=A-A.mean(0); B=B-B.mean(0)
    U,S,Vt=np.linalg.svd(A.T@B)
    d=np.sign(np.linalg.det(U@Vt)); R=U@np.diag([1.0,1.0,d])@Vt
    D=((A@R)-B)**2
    return float(np.sqrt(D.sum()/len(A))), float(np.linalg.det(R)), float(np.sqrt(D.sum(1).max())), int(np.argmax(D.sum(1)))+1

def rotmat(ax,th):
    ax=np.array(ax,float); ax/=np.linalg.norm(ax); c,s=np.cos(th),np.sin(th); x,y,z=ax
    return np.array([[c+x*x*(1-c),x*y*(1-c)-z*s,x*z*(1-c)+y*s],
                     [y*x*(1-c)+z*s,c+y*y*(1-c),y*z*(1-c)-x*s],
                     [z*x*(1-c)-y*s,z*y*(1-c)+x*s,c+z*z*(1-c)]])

print("=== kabsch() self-check (SVD, centroid removed, det forced +1) ===")
A=np.random.default_rng(7).normal(size=(41,3))
Rp=rotmat([0.31,-0.77,0.55],0.9123); t=np.array([3.7,-11.2,5.9])
print("(1) rot+trans 41 : %.3e A  det=%+.12f" % kabsch(A,A@Rp.T+t)[:2])
M=np.diag([1.0,1.0,-1.0]).dot(rotmat([0.0,1.0,0.0],0.4))
print("(2) mirrored  41 : %.6f A  det=%+.12f" % kabsch(A,A@M.T+t)[:2])
print("(3) copy      41 : %.3e A  det=%+.12f" % kabsch(A,A.copy())[:2])

order=json.load(open(MAP))["rows"][3]["order"]   # iso 3: seed index (1-based) -> E3 label
B=blocks(LOG1073)
pre=[b for b in B if b[0] < 49775]
final=pre[-1]
X=X if False else final[1]; el=final[2]
print("\n1073 opt-stage: last orientation block before 'Optimization completed' (L49775) is L%d (%s), %d atoms" % (final[0], final[3], len(X)))
# seed order -> E3 order
Xe=np.zeros((41,3))
for s in range(1,42):
    Xe[order[s-1]-1]=X[s-1]
def r(a,b): return float(np.linalg.norm(Xe[a-1]-Xe[b-1]))
print("key distances in E3 1-based labels (from 1073 final opt frame):")
for nm,(i,j) in {"R(2,4) C2-N4":(2,4),"R(2,25) C2-O25":(2,25),"R(4,26) N4-H26":(4,26),
                 "R(25,26) O25-H26":(25,26),"R(10,27) O10-H27":(10,27),"R(2,26) C2..H26":(2,26),
                 "R(25,4) O25..N4":(25,4),"R(2,27)":(2,27)}.items():
    print("  %-20s %.4f" % (nm, r(i,j)))
heavy=[i for i in range(1,42) if el[ [k for k in range(1,42) if order[k-1]==i][0]-1 ] != 1]
nn=min(((r(26,i),i) for i in heavy))
print("  H26 nearest heavy atom: %d at %.4f A" % (nn[1], nn[0]))

He,_,_=xyz(HEMI)
dd,detd,maxd,argd=kabsch(Xe,He)
print("\nKabsch 1073-final vs 1028 frame (all 41, SVD, mirror forbidden): RMSD %.4f A  det=%+.2f  max %.4f A at E3 atom %d" % (dd,detd,maxd,argd))
Pb=blocks(PLOG); P=Pb[-1][1]
dp,detp,maxp,argp=kabsch(Xe,P)
print("Kabsch 1073-final vs P (job 1061 optfreq last orientation L%d) (all 41, SVD, mirror forbidden): RMSD %.4f A  det=%+.2f  max %.4f A at E3 atom %d" % (Pb[-1][0],dp,detp,maxp,argp))
