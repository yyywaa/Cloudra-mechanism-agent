import numpy as np
BASE="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/"
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
            if len(co)==41: out.append((i+1,np.array(co),el))
            i=k
        else: i+=1
    return out
def xyz(path):
    L=open(path).read().splitlines(); n=int(L[0].split()[0]); co=[]; el=[]
    Z={"H":1,"C":6,"N":7,"O":8}
    for ln in L[2:2+n]:
        p=ln.split(); el.append(Z[p[0]]); co.append([float(p[1]),float(p[2]),float(p[3])])
    return np.array(co), el
def kabsch(A,B):
    A=np.asarray(A,float); B=np.asarray(B,float)
    A=A-A.mean(0); B=B-B.mean(0)
    U,S,Vt=np.linalg.svd(A.T@B); d=np.sign(np.linalg.det(U@Vt))
    R=U@np.diag([1.0,1.0,d])@Vt; D=((A@R)-B)**2
    return float(np.sqrt(D.sum()/len(A))), float(np.linalg.det(R)), float(np.sqrt(D.sum(1).max())), int(np.argmax(D.sum(1)))+1
def rotmat(ax,th):
    ax=np.array(ax,float); ax/=np.linalg.norm(ax); c,s=np.cos(th),np.sin(th); x,y,z=ax
    return np.array([[c+x*x*(1-c),x*y*(1-c)-z*s,x*z*(1-c)+y*s],[y*x*(1-c)+z*s,c+y*y*(1-c),y*z*(1-c)-x*s],[z*x*(1-c)-y*s,z*y*(1-c)+x*s,c+z*z*(1-c)]])
A=np.random.default_rng(23).normal(size=(41,3)); Rp=rotmat([0.2,0.9,-0.4],0.77); t=np.array([1.0,-4.0,6.0]); Mx=np.diag([1.0,1.0,-1.0]).dot(rotmat([1.0,0.0,0.0],0.5))
print("SELFCHECK (1) %.3e det=%+.12f | (2) %.6f det=%+.12f | (3) %.3e det=%+.12f" % (kabsch(A,A@Rp.T+t)[0],kabsch(A,A@Rp.T+t)[1],kabsch(A,A@Mx.T+t)[0],kabsch(A,A@Mx.T+t)[1],kabsch(A,A.copy())[0],kabsch(A,A.copy())[1]))

b=[x for x in blocks(BASE+"runs/build_seed_product_optfreq.log") if x[0] < 49775][-1]
X=b[1]; elX=b[2]
Pb=blocks(BASE+"runs/P_e3b/P_optfreq.log")[-1]; P=Pb[1]; elP=Pb[2]
full=[(1,3),(2,2),(3,25),(4,1),(5,29),(6,28),(7,30),(8,35),(9,34),(10,33),(11,32),(12,31),(13,14),(14,15),(15,16),(16,12),(17,13),(18,36),(19,24),(20,41),(21,40),(22,39),(23,38),(24,37),(25,11),(26,9),(27,10),(28,8),(29,7),(30,6),(31,5),(32,4),(33,27),(34,23),(35,21),(36,22),(37,19),(38,20),(39,17),(40,18),(41,26)]
print("pairs:", len(full), "| src covers 1..41 exactly once:", sorted(a for a,e in full)==list(range(1,42)), "| tgt covers 1..41 exactly once:", sorted(e for a,e in full)==list(range(1,42)))
bad=[(a,e,elX[a-1],elP[e-1]) for a,e in full if elX[a-1]!=elP[e-1]]
print("element mismatches:", len(bad), bad[:5])
Xa=np.array([X[a-1] for a,e in full]); Pa=np.array([P[e-1] for a,e in full])
r=kabsch(Xa,Pa); print("ALL-41 mapped Kabsch 1073->P: RMSD %.4f A det=%+.2f max %.4f A worst atom (1073) %d" % r)
heavypos=[i for i,(a,e) in enumerate(full) if elX[a-1]!=1]
Xh=Xa[heavypos]; Ph=Pa[heavypos]
rh=kabsch(Xh,Ph); print("heavy-20 subset of the SAME map: RMSD %.4f A det=%+.2f max %.4f A (worst heavy #%d of 20 -> 1073 atom %d)" % (rh[0],rh[1],rh[2],rh[3],full[heavypos[rh[3]-1]][0]))
print("coordinator claims: all-41 2.6798 / max 5.3753 / det +1.00 ; heavy 2.2976 / max 4.7027")

try:
    from rdkit import Chem
    from rdkit.Chem import rdDetermineBonds
    He,elH=xyz(BASE+"prep/hemiaminal_1028_lastframe.xyz")
    def mkmol(el,co,keepZ=None):
        m=Chem.RWMol()
        for z in el: m.AddAtom(Chem.Atom(int(z)))
        conf=Chem.Conformer(len(el))
        for i,(x,y,z) in enumerate(co): conf.SetAtomPosition(i,(float(x),float(y),float(z)))
        mol=m.GetMol(); mol.AddConformer(conf); rdDetermineBonds.DetermineConnectivity(mol); return mol
    m1073=mkmol(elX,X); m1028=mkmol(elH,He)
    h1073=[i for i,z in enumerate(elX) if z!=1]; h1028=[i for i,z in enumerate(elH) if z!=1]
    rw=Chem.RWMol(m1028)
    pos={o:k for k,o in enumerate(h1028)}
    i2,i4=pos[1],pos[3]   # E3 atoms 2 and 4 (0-based 1,3) in 1028
    bd=rw.GetBondBetweenAtoms(1,3)
    print("\n1028 heavy graph: bond E3 2-4 present:", bd is not None)
    rw.RemoveBond(1,3)
    m1028b=rw.GetMol(); Chem.SanitizeMol(m1028b)
    for tag,keepH in (("heavy-20 graph (H removed)",False),("full 41 graph",True)):
        q=Chem.RWMol(m1073); tg=Chem.RWMol(m1028b)
        if not keepH:
            q=Chem.RWMol(Chem.RemoveHs(q.GetMol())); tg=Chem.RWMol(Chem.RemoveHs(tg.GetMol()))
        mt=tg.GetSubstructMatches(q.GetMol(), uniquify=False, maxMatches=5000)
        print("   match count 1073 -> 1028(edge removed), %s: %d" % (tag, len(mt)))
        if mt and not keepH:
            bestc=None
            for m_ in mt:
                rk=kabsch(np.array([X[i] for i in h1073]), np.array([He[h1028[j]] for j in m_]))
                if bestc is None or rk[0]<bestc[0]: bestc=rk
            print("   best heavy Kabsch over those matches: %.4f A det=%+.2f max %.4f A" % (bestc[0],bestc[1],bestc[2]))
except Exception as ex:
    print("RDKit step failed:", repr(ex))
