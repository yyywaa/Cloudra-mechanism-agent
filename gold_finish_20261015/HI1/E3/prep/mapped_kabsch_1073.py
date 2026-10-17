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

A=np.random.default_rng(11).normal(size=(41,3)); Rp=rotmat([0.4,-0.6,0.7],1.1); t=np.array([2.0,5.0,-3.0])
Mx=np.diag([1.0,1.0,-1.0]).dot(rotmat([0.0,1.0,0.0],0.3))
print("SELFCHECK (1) rot+trans %.3e A det=%+.12f" % kabsch(A,A@Rp.T+t)[:2])
print("SELFCHECK (2) mirror    %.6f A det=%+.12f" % kabsch(A,A@Mx.T+t)[:2])
print("SELFCHECK (3) copy      %.3e A det=%+.12f" % kabsch(A,A.copy())[:2])

B=blocks(BASE+"runs/build_seed_product_optfreq.log")
b=[x for x in B if x[0] < 49775][-1]
X=b[1]; elX=b[2]
print("1073 block L%d elements: %s" % (b[0], "".join({1:"H",6:"C",7:"N",8:"O"}[z] for z in elX)))
P=blocks(BASE+"runs/P_e3b/P_optfreq.log")[-1][1]
He,elH=xyz(BASE+"prep/hemiaminal_1028_lastframe.xyz")
print("P elements :", "".join({1:"H",6:"C",7:"N",8:"O"}[z] for z in blocks(BASE+"runs/P_e3b/P_optfreq.log")[-1][2]))
print("1028 elements:", "".join({1:"H",6:"C",7:"N",8:"O"}[z] for z in elH))

pairs=[(1,3),(2,2),(3,25),(4,1),(5,29),(6,28),(7,30),(8,35),(9,34),(10,33),(11,32),(12,31),(25,11),(26,9),(27,10),(28,8),(29,7),(30,6),(31,5),(32,4)]
print("\n-- verify coordinator's 20 heavy pairs (1073 idx -> E3 idx), element check --")
ok=True
for a,e in pairs:
    if elX[a-1]!=elH[e-1]: ok=False; print("   MISMATCH %d(%d) -> %d(%d)"%(a,elX[a-1],e,elH[e-1]))
print("   element consistency:", ok, "| pairs:", len(pairs))
Xm=np.array([X[a-1] for a,e in pairs]); Pm=np.array([P[e-1] for a,e in pairs])
r,det,mx,w=kabsch(Xm,Pm)
print("   MAPPED heavy-20 Kabsch 1073->P (numpy SVD, mirror forbidden): RMSD %.4f A  det=%+.2f  max %.4f A  worst pair #%d (1073 atom %d -> E3 %d)"%(r,det,mx,w,pairs[w-1][0],pairs[w-1][1]))
Xh=np.array([X[a-1] for a,e in pairs]); Hh=np.array([He[e-1] for a,e in pairs])
r2,det2,mx2,w2=kabsch(Xh,Hh)
print("   SAME 20 pairs vs 1028 geometry: RMSD %.4f A det=%+.2f max %.4f A (only diagnostic: pair set derived from P)"%(r2,det2,mx2))
print("   index-based (VOID) all-41 value was 2.6798/2.8491 -> not to be cited")

try:
    from rdkit import Chem
    from rdkit.Chem import rdDetermineBonds
    def mkmol(el,co):
        m=Chem.RWMol()
        for z in el: m.AddAtom(Chem.Atom(int(z)))
        conf=Chem.Conformer(len(el))
        for i,(x,y,z) in enumerate(co): conf.SetAtomPosition(i,(float(x),float(y),float(z)))
        mol=m.GetMol(); mol.AddConformer(conf)
        rdDetermineBonds.DetermineConnectivity(mol)
        return mol
    m1073=mkmol(elX,X); mP=mkmol(blocks(BASE+"runs/P_e3b/P_optfreq.log")[-1][2],P); m1028=mkmol(elH,He)
    print("\n-- RDKit substructure matching (DetermineConnectivity, no stereo) --")
    print("   1073 heavy bonds:", sum(1 for bd in m1073.GetBonds() if bd.GetBeginAtom().GetAtomicNum()>1 and bd.GetEndAtom().GetAtomicNum()>1))
    print("   P    heavy bonds:", sum(1 for bd in mP.GetBonds() if bd.GetBeginAtom().GetAtomicNum()>1 and bd.GetEndAtom().GetAtomicNum()>1))
    print("   1028 heavy bonds:", sum(1 for bd in m1028.GetBonds() if bd.GetBeginAtom().GetAtomicNum()>1 and bd.GetEndAtom().GetAtomicNum()>1))
    mp=mP.GetSubstructMatches(m1073, uniquify=False, maxMatches=5000)
    print("   matches 1073->P:", len(mp))
    if mp:
        best=None
        for mt in mp:
            idx=[i for i in range(41) if elX[i]!=1]
            rk=kabsch(X[idx],[P[mt[i]] for i in idx])
            if best is None or rk[0]<best[0]: best=(rk[0],rk[1],rk[2],mt)
        print("   best heavy Kabsch over matches: %.4f A max %.4f (map sample %s)"%(best[0],best[2],best[3][:6]))
    # delete C2-N4 (E3 idx 2 and 4) in 1028 and rematch
    rw=Chem.RWMol(m1028)
    a1=[a.GetIdx() for a in rw.GetAtoms() if a.GetIdx()==1][0]
    if rw.GetBondBetweenAtoms(1,3) is not None:
        rw.RemoveBond(1,3); print("   removed 1028 bond E3 2-4 (0-based 1-3)")
    else:
        print("   !! 1028 bond E3 2-4 not found; existing bonds of atom 2:", [(bd.GetBeginAtomIdx(),bd.GetEndAtomIdx()) for bd in m1028.GetBonds() if 1 in (bd.GetBeginAtomIdx(),bd.GetEndAtomIdx())])
    m1028b=rw.GetMol(); Chem.SanitizeMol(m1028b)
    mq=m1028b.GetSubstructMatches(m1073, uniquify=False, maxMatches=5000)
    print("   matches 1073->1028(edge removed):", len(mq))
    if mq:
        best=None
        for mt in mq:
            idx=[i for i in range(41) if elX[i]!=1]
            rk=kabsch(X[idx],[He[mt[i]] for i in idx])
            if best is None or rk[0]<best[0]: best=(rk[0],rk[1],rk[2],mt)
        print("   best heavy Kabsch: %.4f A max %.4f"%(best[0],best[2]))
except Exception as ex:
    print("RDKit step failed:", repr(ex))
