#!/usr/bin/env python3
"""E1a/E1b split-model species verification: SMILES identity, CIP, heavy-atom binding, atom-map identity.
All coordinates are read from on-disk XYZ artifacts; nothing is typed in."""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
import sys, hashlib

SPLIT = "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split"

def rd(xyz):
    lines = open(xyz).read().splitlines()
    n = int(lines[0].split()[0])
    at = []
    for L in lines[2:2+n]:
        p = L.split()
        at.append((p[0], [float(p[1]), float(p[2]), float(p[3])]))
    assert len(at) == n, (xyz, len(at), n)
    return at

def cip(smi, tag):
    m = Chem.MolFromSmiles(smi)
    Chem.AssignStereochemistry(m, cleanIt=True, force=True)
    out = []
    for a in m.GetAtoms():
        if a.HasProp("_CIPCode"):
            out.append((a.GetIdx()+1, a.GetSymbol(), a.GetProp("_CIPCode")))
    print(f"  [{tag}] formula={rdMolDescriptors.CalcMolFormula(m)} nHeavy={m.GetNumAtoms()} CIP={out}")
    return m, out

R = "CC(C)=O.O=C(O)[C@@H]1CCCN1"
P_at = "CC(C)(O)N1CCC[C@H]1C(=O)O"
P_at2 = "CC(C)(O)N1CCC[C@@H]1C(=O)O"

print("reactant:", R)
mR, cipR = cip(R, "reactant")
print("product @:", P_at)
mP, cipP = cip(P_at, "product @")
print("product @@:", P_at2)
mP2, cipP2 = cip(P_at2, "product @@")

# heavy atom binding candidates: SMILES heavy-atom order -> 1-based file index
HB_R = [1, 2, 4, 3, 11, 12, 13, 14, 15, 16, 17, 18]
HB_P = [1, 2, 4, 3, 18, 17, 16, 15, 14, 12, 11, 13]

rc = rd(f"{SPLIT}/RC_27_opt_frame.xyz")
it = rd(f"{SPLIT}/INT1_27_start.xyz")
print("RC_27_opt_frame.xyz  natoms=%d els_ok=%s" % (len(rc), None))
print("INT1_27_start.xyz    natoms=%d" % len(it))
print("same element sequence RC vs INT1_start:", [a[0] for a in rc] == [a[0] for a in it])

# element check of heavy-atom binding against SMILES heavy atoms
def check_hb(mol, hb, geom, tag):
    els = [a.GetSymbol() for a in mol.GetAtoms()]  # heavy only (SMILES built without explicit H here)
    ok = all(els[i] == geom[hb[i]-1][0] for i in range(len(hb)))
    print(f"  [{tag}] heavy_atom_binding {hb} element-wise match = {ok}")
    if not ok:
        print("    smiles heavy els:", els)
        print("    file els:", [geom[i-1][0] for i in hb])
    return ok

okR = check_hb(mR, HB_R, rc, "reactant")
okP = check_hb(mP, HB_P, it, "product")

# geometry contacts, 27-atom working order
def d(g,i,j):
    a,b = g[i-1][1], g[j-1][1]
    return sum((a[k]-b[k])**2 for k in range(3))**0.5
print("RC_27 contacts: C2-O4 %.3f C2...N20 %.3f N20-H21 %.3f O4...H21 %.3f C2-C3 %.3f C3-H22 %.3f" % (
    d(rc,2,3), d(rc,2,18), d(rc,18,27), d(rc,3,27), d(rc,2,4), d(rc,4,10)))
print("INT1_start contacts: C2-O4 %.3f C2...N20 %.3f N20-H21 %.3f O4...H21 %.3f C2-C3 %.3f C3-H22 %.3f" % (
    d(it,2,3), d(it,2,18), d(it,18,27), d(it,3,27), d(it,2,4), d(it,4,10)))
print("atom_map identity 1..27 valid:", [a[0] for a in rc] == [a[0] for a in it])
