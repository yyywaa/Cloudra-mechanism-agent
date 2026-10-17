#!/usr/bin/env python3
"""HI1_E3: rank assembled I1 complex candidates for the C-C forming scan start.
Usage: python3 rank_i1_candidates.py CAND.xyz [CAND.xyz ...]
Prints, per candidate: fragments, CIP codes with 1-based atom indices, r(C1-C29) (enamine CH2 ... aldehyde C),
H-bond contacts to the aldehyde O28, and the C2=C1...C29=O28 attack geometry.
"""
import sys
import math
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds

def dist(c, i, j):
    a, b = c[i], c[j]
    return math.sqrt(sum((a[k] - b[k]) ** 2 for k in range(3)))

def angle(c, i, j, k):
    v1 = [c[i][t] - c[j][t] for t in range(3)]
    v2 = [c[k][t] - c[j][t] for t in range(3)]
    n1 = math.sqrt(sum(x * x for x in v1)); n2 = math.sqrt(sum(x * x for x in v2))
    cosv = sum(v1[t] * v2[t] for t in range(3)) / (n1 * n2)
    return math.degrees(math.acos(max(-1.0, min(1.0, cosv))))

def main():
    for path in sys.argv[1:]:
        m = Chem.MolFromXYZFile(path)
        if m is None:
            print(path, "PARSE_FAIL"); continue
        try:
            rdDetermineBonds.DetermineBonds(m, charge=0)
        except Exception as e:
            print(path, "BOND_FAIL", repr(e)); continue
        Chem.AssignStereochemistryFrom3D(m)
        Chem.AssignStereochemistry(m, cleanIt=True, force=True)
        conf = m.GetConformer()
        c = [(conf.GetAtomPosition(i).x, conf.GetAtomPosition(i).y, conf.GetAtomPosition(i).z) for i in range(m.GetNumAtoms())]
        frags = Chem.GetMolFrags(m)
        cip = [(a.GetIdx() + 1, a.GetProp('_CIPCode')) for a in m.GetAtoms() if a.HasProp('_CIPCode')]
        # heavy-atom contacts between fragments
        mins = {}
        for i, fr in enumerate(frags):
            for j, fr2 in enumerate(frags):
                if j <= i: continue
                best = min(dist(c, a, b) for a in fr for b in fr2)
                mins[f"{i}-{j}"] = round(best, 3)
        hb = {f"O10-H{x}": round(dist(c, 9, x - 1), 3) for x in range(12, 25)}
        hb2 = {f"O11-H{x}": round(dist(c, 10, x - 1), 3) for x in range(12, 25)}
        near10 = min(hb.items(), key=lambda kv: kv[1])
        near11 = min(hb2.items(), key=lambda kv: kv[1])
        print(f"{path}: nfrag={len(frags)} CIP={cip}")
        print(f"   r(C1-C29)={dist(c,0,28):.3f} A  r(C2-C29)={dist(c,1,28):.3f}  r(O28-C29)={dist(c,27,28):.3f}")
        print(f"   closest H to carboxyl O10(=O): {near10}   to O11(-OH): {near11}")
        print(f"   inter-fragment heavy-atom min dist: {mins}")
        print(f"   angle C2-C1...C29={angle(c,1,0,28):.1f} deg  angle C1-C29-O28={angle(c,0,28,27):.1f} deg")
    return 0

if __name__ == "__main__":
    sys.exit(main())
