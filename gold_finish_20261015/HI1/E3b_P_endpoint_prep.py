
import numpy as np, json, os
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds

src = "gold_finish_20261015/HI1/E3/prep/hemiaminal_1028_lastframe.xyz"
lines = open(src).read().splitlines()
n = int(lines[0].strip())
atoms = []
for L in lines[2:2+n]:
    p = L.split()
    atoms.append((p[0], np.array([float(p[1]), float(p[2]), float(p[3])])))

# build mol with bonds from geometry
block = "%d\n\n" % n + "\n".join("%s %.6f %.6f %.6f" % (s, *c) for s, c in atoms) + "\n"
m = Chem.MolFromXYZBlock(block)
rdDetermineBonds.DetermineBonds(m, charge=0)
ri = m.GetRingInfo()

sym = [s for s, _ in atoms]
# find C2: carbon bonded to N and with an O neighbor that carries an H
cand = []
for a in m.GetAtoms():
    if a.GetSymbol() != "C": continue
    nbrs = [x for x in a.GetNeighbors()]
    ns = [x for x in nbrs if x.GetSymbol()=="N"]
    if not ns: continue
    for o in [x for x in nbrs if x.GetSymbol()=="O"]:
        hs = [h for h in o.GetNeighbors() if h.GetSymbol()=="H"]
        if hs:
            cand.append((a.GetIdx(), ns[0].GetIdx(), o.GetIdx(), hs[0].GetIdx()))
print("candidates (C2,N,Owater,Hwater):", [(c, [sym[i]+str(i+1) for i in c]) for c in cand])
assert len(cand)==1, "ambiguous C2 identification"
c2, nidx, oidx, hidx = cand[0]
print("C2 idx", c2+1, "N idx", nidx+1, "Owater idx", oidx+1, "H idx", hidx+1)

def dist(i,j): return float(np.linalg.norm(atoms[i][1]-atoms[j][1]))
print("C2-N %.4f  C2-Ow %.4f  Ow-H %.4f" % (dist(c2,nidx), dist(c2,oidx), dist(oidx,hidx)))

# fragment membership (connected components excluding the soon-to-be-broken C2-N bond)
frag = {}
def walk(start, ban):
    stack=[start]; seen={start}
    while stack:
        u=stack.pop()
        for v in [x.GetIdx() for x in m.GetAtomWithIdx(u).GetNeighbors()]:
            if (u,v)==ban or (v,u)==ban: continue
            if v not in seen: seen.add(v); stack.append(v)
    return seen
prol = walk(nidx, (c2,nidx))            # proline side (contains N)
ald  = set(range(n)) - prol             # aldol side
print("fragment sizes: proline %d, aldol %d, total %d" % (len(prol), len(ald), n))
assert hidx in prol or True

coords = {i: atoms[i][1].copy() for i in range(n)}
# 1) move the water-derived H onto N (N-H 1.02 A, placed opposite to the N->(ring) centroid)
ring_nbrs = [x.GetIdx() for x in m.GetAtomWithIdx(nidx).GetNeighbors() if x.GetIdx()!=c2]
cen = np.mean([coords[i] for i in ring_nbrs], axis=0)
u = coords[nidx]-cen; u/=np.linalg.norm(u)
coords[hidx] = coords[nidx] + 1.02*u
# 2) rigidly translate the proline fragment along C2->N until C2-N = 3.00 A
vec = coords[nidx]-coords[c2]; vec/=np.linalg.norm(vec)
cur = dist(c2,nidx)
shift = (3.00-cur)*vec
for i in prol: coords[i] = coords[i] + shift
print("after: C2-N %.4f" % dist(c2,nidx))

# checks
D = np.array([coords[i] for i in range(n)])
dmin = 1e9; pair=None
for i in range(n):
    for j in range(i+1,n):
        d = np.linalg.norm(D[i]-D[j])
        if d < dmin: dmin, pair = d, (i+1,j+1)
xmin=1e9; xp=None
for i in ald:
    for j in prol:
        d = np.linalg.norm(D[i]-D[j])
        if d < xmin: xmin, xp = d, (i+1, j+1)
print("minsep %.4f A at %s ; min inter-fragment contact %.4f A at %s" % (dmin, pair, xmin, xp))
print("composition:", {s: sym.count(s) for s in set(sym)})

os.makedirs("gold_finish_20261015/HI1/E3b_P_endpoint", exist_ok=True)
out = "gold_finish_20261015/HI1/E3b_P_endpoint/P_from_1028frame_stretch3.00.xyz"
with open(out,"w") as f:
    f.write("%d\n" % n)
    f.write("P endpoint seed: job1028 hemiaminal frame, C2-N broken (C2-N=3.00 A), water H moved to N\n")
    for i in range(n):
        f.write("%-2s %14.8f %14.8f %14.8f\n" % (sym[i], *D[i]))
print("wrote", out)
