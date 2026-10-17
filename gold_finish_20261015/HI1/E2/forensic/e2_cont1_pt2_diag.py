import hashlib, math, sys
import numpy as np
CONT1="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan_cont1.log"
def read(p):
    b=open(p,"rb").read(); return b.decode("utf-8","replace").splitlines(), hashlib.sha256(b).hexdigest(), len(b)
def blocks(L):
    out=[];i=0;n=len(L)
    while i<n:
        if L[i].strip().startswith("Standard orientation:"):
            j=i+1;d=0
            while j<n and d<2:
                if L[j].strip().startswith("-----"): d+=1
                j+=1
            co={};k=j;cnt=0
            while k<n and not L[k].strip().startswith("-----"):
                p=L[k].split()
                if len(p)==6: co[int(p[0])]=(int(p[1]),float(p[3]),float(p[4]),float(p[5])); cnt+=1
                k+=1
            assert cnt==41
            out.append((i+1,k+1,co)); i=k
        else: i+=1
    return out
def frames(L):
    bl=blocks(L); oc=[i+1 for i,l in enumerate(L) if "Optimization completed" in l]; fr=[]
    for d in oc:
        hdr,end,co=[b for b in bl if b[1]<d][-1]
        scf=[(i+1,l) for i,l in enumerate(L) if "SCF Done" in l and hdr<i+1<d][-1]
        e=float(scf[1].split("=")[1].split("A.U.")[0])
        fr.append(dict(oc=d,hdr=hdr,scf=scf[0],E=e,co=co))
    return fr
Lc,shac,bc=read(CONT1); fr=frames(Lc)
A,B=fr[0],fr[1]
print(f"snapshot lines={len(Lc)} bytes={bc} sha={shac}")
print(f"cont1 pt1 oc L{A['oc']} E={A['E']:.9f} | pt2 oc L{B['oc']} E={B['E']:.9f} dE(pt1->pt2)={ (B['E']-A['E'])*627.5094740631:+.3f} kcal/mol")
heavy=[i for i in sorted(A["co"]) if A["co"][i][0]!=1]
P=np.array([A["co"][i][1:] for i in heavy]); Q=np.array([B["co"][i][1:] for i in heavy])
Pc=P-P.mean(0); Qc=Q-Q.mean(0)
C=Qc.T@Pc; U,S,Vt=np.linalg.svd(C); d=np.sign(np.linalg.det(Vt.T@U.T)); R=Vt.T@np.diag([1,1,d])@U.T
Qp=Qc@R.T
dist=np.linalg.norm(Pc-Qp,axis=1)
print(f"heavy20 Kabsch rmsd={math.sqrt((dist**2).mean()):.4f} max={dist.max():.4f} det={d:+.0f}")
order=np.argsort(-dist)
print("top heavy-atom deviations (1-based index, |d| A):")
for k in order[:10]:
    print(f"   atom {heavy[k]:2d} Z={int(A['co'][heavy[k]][0]):2d} |d|={dist[k]:.3f}")
print("\nkey distances (pt1 -> pt2):")
def dd(co,a,b): return math.dist(co[a][1:],co[b][1:])
for a,b,lab in [(1,29,"C1-C29 (scan)"),(28,24,"O28...H24"),(11,24,"O11-H24"),(2,4,"C2-N4"),(2,25,"C2=O25"),(10,27,"O10-H27"),(4,26,"N4-H26"),(4,27,"N4...H27"),(1,2,"C1-C2"),(25,26,"O25...H26")]:
    print(f"   {lab:14s} pt1={dd(A['co'],a,b):.4f}  pt2={dd(B['co'],a,b):.4f}  d={dd(B['co'],a,b)-dd(A['co'],a,b):+.4f}")
# dihedral-ish: angle of aldehyde O25 relative to ring, and N4-C2
def ang(co,a,b,c):
    v1=np.array(co[a][1:])-np.array(co[b][1:]); v2=np.array(co[c][1:])-np.array(co[b][1:])
    return math.degrees(math.acos(max(-1,min(1,float(v1@v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))))))
def dih(co,a,b,c,e):
    p=[np.array(co[i][1:]) for i in (a,b,c,e)]
    b1=p[1]-p[0]; b2=p[2]-p[1]; b3=p[3]-p[2]
    n1=np.cross(b1,b2); n2=np.cross(b2,b3)
    m=np.cross(n1,b2/np.linalg.norm(b2))
    return math.degrees(math.atan2(float(m@n2), float(n1@n2)))
for lab,quad in [("C1-C2-N4-C3",(1,2,4,3)),("C29-C1-C2-N4",(29,1,2,4)),("O25-C2-C1-C29",(25,2,1,29)),("C2-C1-C29-O28ref",(2,1,29,28))]:
    print(f"   dihedral {lab:20s} pt1={dih(A['co'],*quad):+8.2f}  pt2={dih(B['co'],*quad):+8.2f}  d={dih(B['co'],*quad)-dih(A['co'],*quad):+8.2f}")
