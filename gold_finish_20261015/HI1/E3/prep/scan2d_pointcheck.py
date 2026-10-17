import math, re
LOG="gold_finish_20261015/HI1/E3/runs/e3b_scan2d_c2n4_o25h26.log"
L=open(LOG).read().splitlines()
blocks=[]  # (lineno_of_header, coords, elements)
i=0
while i < len(L):
    if "Input orientation:" in L[i]:
        j=i+5  # skip dashed line, center, dashed, 4 header lines? handle generically
        # find first data row after header: rows with 6 fields where field0 int index
        k=i+1
        coords=[]; els=[]
        while k < len(L) and len(coords) < 41:
            parts=L[k].split()
            if len(parts)==6 and parts[0].isdigit() and parts[1].isdigit():
                els.append(int(parts[1])); coords.append((float(parts[3]),float(parts[4]),float(parts[5])))
            k+=1
        if len(coords)==41: blocks.append((i+1, coords, els))
        i=k
    else:
        i+=1
Z={1:"H",6:"C",7:"N",8:"O"}
print("total Input orientation blocks:", len(blocks))
optc=[k+1 for k,l in enumerate(L) if "Optimization completed." in l]
scfs=[(k+1,l) for k,l in enumerate(L) if "SCF Done" in l]
scanpt=[(k+1,l.strip()) for k,l in enumerate(L) if "on scan point" in l]
print("Optimization completed lines:", optc)
print("last scan point line:", scanpt[-1] if scanpt else None)
print("last SCF:", scfs[-1] if scfs else None)
def d(A,B): return math.dist(A,B)
def kabsch(A,B):
    import numpy as np
    A=np.array(A); B=np.array(B)
    A=A-A.mean(0); B=B-B.mean(0)
    U,S,Vt=np.linalg.svd(A.T@B)
    d=np.sign(np.linalg.det(U@Vt))
    R=U@np.diag([1.0,1.0,d])@Vt
    return float(np.sqrt((((A@R)-B)**2).sum()/len(A)))
def metrics(coords, tag):
    idx=lambda a: coords[a-1]
    r24=d(idx(2),idx(4)); r25=d(idx(2),idx(25)); r426=d(idx(4),idx(26)); r1027=d(idx(10),idx(27)); r2526=d(idx(25),idx(26))
    heavy=[a for a in range(1,42) if Z[blocks_b[2][a-1]]!="H" and a!=26]
    nn=min(((d(idx(26),idx(a)),a) for a in heavy))
    print("%-10s R(2,4)=%.4f R(25,26)=%.4f R(4,26)=%.4f R(10,27)=%.4f R(2,25)=%.4f R(2,26)=%.4f | H26 nearest heavy=%d%s %.4f A" % (tag, r24, r2526, r426, r1027, r25, d(idx(2),idx(26)), nn[1], Z[blocks_b[2][nn[1]-1]], nn[0]))
    return (r24, r25, r426, r1027, r25)
# pick last block before each Optimization completed
pts=[]
for oc in optc:
    cand=[b for b in blocks if b[0] < oc]
    if cand:
        b=cand[-1]; pt=len(pts)+1
        blocks_b=[b[0], b[1], b[2]]
        print("--- grid point", pt, "(last orientation at L%d, before Optimization completed at L%d)" % (b[0], oc))
        pts.append((b[0], b[1], b[2]))
        metrics(b[1], "point %d" % pt)
# current (in-progress) point
b=blocks[-1]; blocks_b=[b[0], b[1], b[2]]
print("--- current in-progress block at L%d (last of %d blocks)" % (b[0], len(blocks)))
cur=metrics(b[1], "current")
if len(pts)>=2:
    print("Kabsch RMSD (optimal superposition, all 41 atoms) point1 vs point2: %.4f A" % kabsch(pts[0][1], pts[1][1]))
    print("Kabsch RMSD point1 vs current: %.4f A" % kabsch(pts[0][1], b[1]))
if len(pts)>=1:
    print("Kabsch RMSD last completed point vs current: %.4f A" % kabsch(pts[-1][1], b[1]))
print("start reference 1.4248 / 0.9693 ; point1 and current above")