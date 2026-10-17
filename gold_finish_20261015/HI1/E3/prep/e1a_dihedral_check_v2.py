import numpy as np, re, math
LOG="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split/E1A_constrained_scan_R2692_2192_stepneg.log"
L=open(LOG).read().splitlines()
N=27
blocks=[];i=0
while i<len(L):
    if "Input orientation:" in L[i] or "Standard orientation:" in L[i]:
        k=i+1;co=[];el=[]
        while k<len(L) and len(co)<N:
            p=L[k].split()
            if len(p)==6 and p[0].isdigit() and p[1].isdigit():
                el.append(int(p[1]));co.append([float(p[3]),float(p[4]),float(p[5])])
            k+=1
        if len(co)==N: blocks.append((i+1,np.array(co),el))
        i=k
    else: i+=1
opt=[i+1 for i,ln in enumerate(L) if "Optimization completed" in ln]
scf=[(i+1,float(re.search(r"E\(RB3LYP\) =\s*(-?\d+\.\d+)",ln).group(1))) for i,ln in enumerate(L) if "SCF Done" in ln]
def dih(p0,p1,p2,p3):
    b0=p0-p1; b1=p2-p1; b2=p3-p2
    b1=b1/np.linalg.norm(b1)
    v=b0-np.dot(b0,b1)*b1; w=b2-np.dot(b2,b1)*b1
    return math.degrees(math.atan2(np.dot(np.cross(b1,v),w), np.dot(v,w)))
pts=[]
for oc in opt:
    cand=[b for b in blocks if b[0]<oc]
    b=cand[-1]
    e=[(l,en) for l,en in scf if l<oc][-1]
    pts.append(dict(oc=oc,hdr=b[0],tau=dih(b[1][2],b[1][1],b[1][17],b[1][13]),E=e[1],Eln=e[0],note=L[oc-1].strip()))
k=627.5095
print("converged points:",len(pts))
print("pt | conv line | hdr line | tau (signed) | |tau| | E | dE vs pt1 (kcal/mol)")
for n,p in enumerate(pts,1):
    print(" %2d | L%-6d | L%-6d | %+8.3f | %7.3f | %.9f (L%d) | %+7.2f" % (n,p["oc"],p["hdr"],p["tau"],abs(p["tau"]),p["E"],p["Eln"],(p["E"]-pts[0]["E"])*k))
def wrap(x): return ((x+180.0)%360.0)-180.0
print()
print("pairwise shortest angular changes (selected):")
for (a,b) in [(0,3),(3,4),(0,10),(3,10),(4,10)]:
    print("  pt%d -> pt%d : %+8.3f -> %+8.3f ; shortest dtau = %+8.3f" % (a+1,b+1,pts[a]["tau"],pts[b]["tau"],wrap(pts[b]["tau"]-pts[a]["tau"])))
print()
print("note lines of the convergence blocks (verbatim):")
for n,p in enumerate(pts,1):
    print("  pt%-2d L%-6d %s" % (n,p["oc"],p["note"]))
