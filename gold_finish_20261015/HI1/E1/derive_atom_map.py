#!/usr/bin/env python3
"""HI1_E1 / lane1 — derive and verify the FULL 41-atom 1-based reactant->product map
for ts_0008 (values indexed in PRODUCT order, values = 1-based REACTANT indices).

Read-only. Uses:
 R = jobs/declaration_0002/candidate_opt/optimized_seed.xyz   (run's built reactant)
 P = jobs/declaration_0002/product_seed_opt/optimized_seed.xyz(run's built product)
Heavy-atom correspondence comes from the declared (atom-mapped) SMILES; H-level correspondence
follows the declared H labels (H21 on N20 -> water, H22 on C3(methyl) -> water) and parent atoms.
"""
import numpy as np
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds

WS = "/home/ly/Cloudra-mechanism-agent"
R_PATH = WS + "/ts/ts_0008/jobs/declaration_0002/candidate_opt/optimized_seed.xyz"
P_PATH = WS + "/ts/ts_0008/jobs/declaration_0002/product_seed_opt/optimized_seed.xyz"
RSMI = "[CH3:1][C:2](=[O:4])[CH2:3]([H:22]).[O:5]=[CH:6][c:7]1[cH:8][cH:9][cH:10][cH:11][cH:12]1.[O:13]=[C:14]([OH:15])[C@@H:16]1[CH2:17][CH2:18][CH2:19][N:20]1([H:21])"
PSMI = "[CH3:1][C:2](=[CH2:3])[N:20]2[CH2:19][CH2:18][CH2:17][C@H:16]2[C:14](=[O:13])[OH:15].[O:4]([H:21])([H:22]).[O:5]=[CH:6][c:7]1[cH:8][cH:9][cH:10][cH:11][cH:12]1"

def load(p):
    m = Chem.RWMol(Chem.MolFromXYZFile(p))
    rdDetermineBonds.DetermineBonds(m, charge=0)
    return m.GetMol()

def coords(m):
    c = m.GetConformer()
    return np.array([list(c.GetAtomPosition(i)) for i in range(m.GetNumAtoms())])

R, P = load(R_PATH), load(P_PATH)
print("R atoms", R.GetNumAtoms(), "P atoms", P.GetNumAtoms())
for tag, m, s in (("R", R, RSMI), ("P", P, PSMI)):
    q = Chem.MolFromSmiles(s)
    match = m.GetSubstructMatch(q, useChirality=False) if False else Chem.RemoveHs(m).GetSubstructMatch(Chem.RemoveHs(q), useChirality=False)
    heavy = [i for i in range(m.GetNumAtoms()) if m.GetAtomWithIdx(i).GetAtomicNum() > 1]
    lab = [a.GetAtomMapNum() for a in Chem.RemoveHs(q).GetAtoms()]
    d = dict(zip(lab, [heavy[k]+1 for k in match]))
    print(tag, "heavy label->idx(1-based):", d)

# heavy correspondence: label -> idx
def labmap(m, s):
    q = Chem.MolFromSmiles(s)
    qh = Chem.RemoveHs(q)
    heavy = [i for i in range(m.GetNumAtoms()) if m.GetAtomWithIdx(i).GetAtomicNum() > 1]
    match = Chem.RemoveHs(m).GetSubstructMatch(qh, useChirality=False)
    lab = [a.GetAtomMapNum() for a in qh.GetAtoms()]
    return {lab[k]: heavy[match[k]]+1 for k in range(len(lab))}
lr, lp = labmap(R, RSMI), labmap(P, PSMI)

def hs_on(m, idx1):   # 1-based heavy idx -> sorted list of 1-based H indices bonded to it
    a = m.GetAtomWithIdx(idx1-1)
    return sorted(n.GetIdx()+1 for n in a.GetNeighbors() if n.GetAtomicNum() == 1)

# 1) heavy-atom backbone map: product heavy -> reactant heavy (by label)
amap = {}
for lab, pi in lp.items():
    amap[pi] = lr[lab]

# 2) H-level: product H's follow their parent heavy atom, except the two transferred protons
#    product water O = label 4 -> product idx; its H's are labeled H21,H22 (declared SMILES order)
p_water_O = lp[4]; r_carbonyl_O = lr[4]
p_lab21_atoms = [p_water_O]  # parent of H21/H22 in the product
r_H21 = 41 if True else None
# find reactant H21/H22 atoms: declared reactant SMILES labels H21 on N20, H22 on C3
# reactant N20 idx and C3(idx of label 3)
r_N20 = lr[20]; r_C3 = lr[3]
r_N20_H = hs_on(R, r_N20); r_C3_H = hs_on(R, r_C3)
print("reactant N20 idx", r_N20, "its H:", r_N20_H, " C3(map3) idx", r_C3, " its H:", r_C3_H)
p_water_H = hs_on(P, p_water_O)
print("product water O idx", p_water_O, "its H:", p_water_H)
# H21 = the single N-H of the reactant (declare as H21), H22 = the C3-H that leaves: pick the one
# whose label the declared reactant SMILES attaches: [CH2:3]([H:22]) -> the explicitly written H22.
# RDKit keeps the explicit H atom; identify it as the H that in the reactant geometry is closest to O4 (the
# proton being transferred) among the C3 hydrogens -> use geometry as the tie-break and report it.
Pr, Pp = coords(R), coords(P)
r_O4 = lr[4]
d_C3H = {h: float(np.linalg.norm(Pr[r_C3-1]-Pr[h-1])) for h in r_C3_H}
print("reactant C3-H distances:", d_C3H)
# H22 = methyl H that becomes water H; the declared SMILES writes it explicitly as H22 -> RDKit's
# 'explicit' atom = the one with noImplicit? use the highest-index H of the CH2 group by convention
# and document it; both methyl H's are chemically equivalent for the pathway.
r_H22 = r_C3_H[-1]
r_H21 = r_N20_H[0]
print("chosen reactant H21 (N20-H):", r_H21, " H22 (C3-H):", r_H22)
amap[p_water_H[1]] = r_H21 if False else r_H22   # placeholder overwritten below
# product water H order: SMILES [O:4]([H:21])([H:22]) -> first H = H21, second = H22
amap[p_water_H[0]] = r_H21
amap[p_water_H[1]] = r_H22

# 3) remaining H's: parent-based, skipping already assigned
used_r = set(v for v in amap.values())
for pi in range(1, P.GetNumAtoms()+1):
    if pi in amap: continue
    a = P.GetAtomWithIdx(pi-1)
    if a.GetAtomicNum() != 1: continue
    par_p = a.GetNeighbors()[0].GetIdx()+1
    par_r = amap[par_p]
    cand = [h for h in hs_on(R, par_r) if h not in used_r]
    if not cand:
        print("!! no free H on reactant parent", par_r, "for product H", pi); continue
    amap[pi] = cand[0]; used_r.add(cand[0])

out = [amap.get(j) for j in range(1, P.GetNumAtoms()+1)]
print("atom_map =", out)
print("len", len(out), "bijection", sorted(out) == list(range(1, 42)))

# element-wise check
ok = all(R.GetAtomWithIdx(out[j-1]-1).GetSymbol() == P.GetAtomWithIdx(j-1).GetSymbol() for j in range(1, 42))
print("element-wise match:", ok)

# geometry check: Kabsch superposition on scaffold atoms (excluding reacting set) then displacements
react_set_r = {2, 3, 4, 10, 32, 41}
scaffold = [j for j in range(1, 42) if out[j-1] not in react_set_r]
A = np.array([Pp[j-1] for j in scaffold]); B = np.array([Pr[out[j-1]-1] for j in scaffold])
Ac, Bc = A-A.mean(0), B-B.mean(0)
U, S, Vt = np.linalg.svd(Ac.T @ Bc)
d = np.sign(np.linalg.det(U @ Vt))
D = np.diag([1, 1, d])
Rot = U @ D @ Vt
Aal = Ac @ Rot
disp = np.linalg.norm(Aal - Bc, axis=1)
print("scaffold atoms: n=%d  RMSD=%.3f A  max=%.3f A" % (len(scaffold), float(np.sqrt((disp**2).mean())), float(disp.max())))
for j in sorted(scaffold, key=lambda j: -np.linalg.norm(Aal[scaffold.index(j)]-Bc[scaffold.index(j)]))[:6]:
    print("   largest scaffold displacement: product atom %d -> reactant %d : %.3f A" % (j, out[j-1], float(np.linalg.norm(Aal[scaffold.index(j)]-Bc[scaffold.index(j)]))))
for pair in [(2,3),(4,10),(32,41),(2,4),(2,32),(3,41),(3,10)]:
    print("   declared pair (reactant %d,%d): reactant distance %.3f A ; product distance %.3f A" % (
        pair[0], pair[1], float(np.linalg.norm(Pr[pair[0]-1]-Pr[pair[1]-1])),
        float(np.linalg.norm(Pp[out.index(pair[0]) if pair[0] in out else 0]-Pp[out.index(pair[1])]))))
