import numpy as np, re
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds
BASE="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/"
def lastblock(path):
    L=open(path).read().splitlines(); blk=None; i=0
    while i < len(L):
        if "Input orientation:" in L[i] or "Standard orientation:" in L[i]:
            k=i+1; co=[]; el=[]
            while k < len(L) and len(co)<41:
                p=L[k].split()
                if len(p)==6 and p[0].isdigit() and p[1].isdigit():
                    el.append(int(p[1])); co.append([float(p[3]),float(p[4]),float(p[5])])
                k+=1
            if len(co)==41: blk=(i+1,np.array(co),el)
            i=k
        else: i+=1
    return blk
def kabsch(A,B):
    A=np.asarray(A,float); B=np.asarray(B,float)
    A=A-A.mean(0); B=B-B.mean(0)
    U,S,Vt=np.linalg.svd(A.T@B); d=np.sign(np.linalg.det(U@Vt))
    R=U@np.diag([1.0,1.0,d])@Vt; D=((A@R)-B)**2
    return float(np.sqrt(D.sum()/len(A))), float(np.linalg.det(R)), float(np.sqrt(D.sum(1).max()))
def rotmat(ax,th):
    ax=np.array(ax,float); ax/=np.linalg.norm(ax); c,s=np.cos(th),np.sin(th); x,y,z=ax
    return np.array([[c+x*x*(1-c),x*y*(1-c)-z*s,x*z*(1-c)+y*s],[y*x*(1-c)+z*s,c+y*y*(1-c),y*z*(1-c)-x*s],[z*x*(1-c)-y*s,z*y*(1-c)+x*s,c+z*z*(1-c)]])
A=np.random.default_rng(5).normal(size=(41,3)); Rp=rotmat([1.0,0.2,-0.5],0.6); Mx=np.diag([1.0,1.0,-1.0]).dot(rotmat([0,1.0,0],0.4)); t=np.array([2.,3.,-4.])
print("SELFCHECK (1) %.3e det=%+.12f | (2) %.6f det=%+.12f | (3) %.3e det=%+.12f" % (kabsch(A,A@Rp.T+t)[0],kabsch(A,A@Rp.T+t)[1],kabsch(A,A@Mx.T+t)[0],kabsch(A,A@Mx.T+t)[1],kabsch(A,A.copy())[0],kabsch(A,A.copy())[1]))
b1=lastblock(BASE+"runs/build_seed_product_optfreq.log"); X=b1[1]; elX=b1[2]
b2=lastblock(BASE+"runs/P_e3b/P_optfreq.log"); P=b2[1]; elP=b2[2]
full=[(1,3),(2,2),(3,25),(4,1),(5,29),(6,28),(7,30),(8,35),(9,34),(10,33),(11,32),(12,31),(13,14),(14,15),(15,16),(16,12),(17,13),(18,36),(19,24),(20,41),(21,40),(22,39),(23,38),(24,37),(25,11),(26,9),(27,10),(28,8),(29,7),(30,6),(31,5),(32,4),(33,27),(34,23),(35,21),(36,22),(37,19),(38,20),(39,17),(40,18),(41,26)]
pairmap={a:e for a,e in full}
def mol(el,co):
    m=Chem.RWMol()
    for z in el: m.AddAtom(Chem.Atom(int(z)))
    conf=Chem.Conformer(len(el))
    for i,(x,y,z) in enumerate(co): conf.SetAtomPosition(i,(float(x),float(y),float(z)))
    mm=m.GetMol(); mm.AddConformer(conf); rdDetermineBonds.DetermineBonds(mm, charge=0); return mm
m1=mol(elX,X); m2=mol(elP,P)
f1=[set(i+1 for i in f) for f in Chem.GetMolFrags(m1, asMols=False)]
f2=[set(i+1 for i in f) for f in Chem.GetMolFrags(m2, asMols=False)]
print("1073 fragment sizes:", [len(f) for f in f1], "| P fragment sizes:", [len(f) for f in f2])
print("1073 frag element counts:", [[elX[a-1] for a in sorted(f)].count(6) for f in f1], "(C counts per fragment)")
for k,fa in enumerate(f1):
    groups={}
    for a in fa:
        e=pairmap[a]
        fi=[j for j,f in enumerate(f2) if e in f]
        if not fi: continue
        groups.setdefault(fi[0],[]).append(a)
    for fi,atoms in groups.items():
        heavy=[a for a in atoms if elX[a-1]!=1]
        r=kabsch(np.array([X[a-1] for a in atoms]), np.array([P[pairmap[a]-1] for a in atoms]))
        rh=kabsch(np.array([X[a-1] for a in heavy]), np.array([P[pairmap[a]-1] for a in heavy]))
        print("  1073 frag%d(%d atoms, %d C) -> P frag%d(%d atoms): all-atom(%d) RMSD %.4f det=%+.2f max %.4f | heavy(%d) %.4f max %.4f" % (k,len(fa),[elX[a-1] for a in fa].count(6),fi,len(f2[fi]),len(atoms),r[0],r[1],r[2],len(heavy),rh[0],rh[2]))
Xa=np.array([X[a-1] for a,e in full]); Pa=np.array([P[e-1] for a,e in full])
print("  whole-complex single Kabsch (all 41, mapped): %.4f A  <-- NOT a conformation metric for a 2-fragment complex" % kabsch(Xa,Pa)[0])
def rr(c,a,b_): return float(np.linalg.norm(c[a-1]-c[b_-1]))
print("  1073: O3...H33 = %.4f ; O3...O27 = %.4f | P: O25...H26 = %.4f" % (rr(X,3,33), rr(X,3,27), rr(P,25,26)))
L=open(BASE+"runs/build_seed_product_optfreq.log").read().splitlines()
fr=[]
for ln in L:
    if ln.strip().startswith("Frequencies --"):
        fr += [float(x) for x in re.findall(r'-?\d+\.\d+', ln.split("--",1)[1])]
segs=[sum(1 for v in fr if lo<=v<hi) for lo,hi in ((0,200),(200,800),(800,1800),(1800,99999))]
print("  segmentation <200/200-800/800-1800/>1800 =", segs, "| n =", len(fr), "| min %.4f max %.4f" % (min(fr), max(fr)))
print("  lowest 8:", ["%.2f"%v for v in sorted(fr)[:8]])
