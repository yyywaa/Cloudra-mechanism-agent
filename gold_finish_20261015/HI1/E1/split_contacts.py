#!/usr/bin/env python3
"""Standard 27-atom contact table for the HI1_E1 split model. Elements are identified
from the XYZ file itself (never hand-typed indices)."""
import sys
def rd(p):
    L=open(p).read().splitlines(); n=int(L[0].split()[0])
    return [(l.split()[0],[float(x) for x in l.split()[1:4]]) for l in L[2:2+n]]
def d(g,i,j):
    a,b=g[i-1][1],g[j-1][1]; return sum((a[k]-b[k])**2 for k in range(3))**0.5
def near(g,i,els=("H",),k=3):
    out=sorted(((d(g,i,j),j) for j in range(1,len(g)+1) if g[j-1][0] in els and j!=i))[:k]
    return [(round(x,4),j,g[j-1][0]) for x,j in out]
g=rd(sys.argv[1])
els=[a[0] for a in g]
print("file:",sys.argv[1],"natoms:",len(g),"formula-els:", "".join(sorted(els)))
# element-order based identification of the split-model positions
assert els==list("CCOC"+"HHHHHH"+"OCOCCCCN"+"H"*9), els
P=dict(C1=1,C2=2,O4=3,C3=4,H22=10,O_carb=11,C_carb=12,O_hydroxyl=13,Ca=14,N20=18,H21=27)
pairs=[("C2-O4","C2","O4"),("C2-N20","C2","N20"),("O4-H21","O4","H21"),("N20-H21","N20","H21"),
       ("C2-C3","C2","C3"),("C3-H22","C3","H22"),("O_hydroxyl-H19(carboxyl O-H)","O_hydroxyl",None),
       ("C_carb-O_hydroxyl","C_carb","O_hydroxyl"),("C_carb-O_carb","C_carb","O_carb")]
for name,a,b in pairs:
    if b is None: continue
    print("  %-34s %8.4f  (atoms %d,%d)"%(name,d(g,P[a],P[b]),P[a],P[b]))
print("  carboxyl O-H: O_hydroxyl(13) nearest H:", near(g,P["O_hydroxyl"]))
print("  carboxyl =O   : O_carb(11) nearest H:", near(g,P["O_carb"]))
print("  N20 nearest H :", near(g,P["N20"]))
print("  C3(4) nearest H:", near(g,P["C3"],k=4))
