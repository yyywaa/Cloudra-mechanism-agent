#!/usr/bin/env python3
"""HI1_E3 helper: read an xyz, perceive bonds, report fragments, per-atom identity and CIP labels.
Usage: python3 xyz_identity.py FILE.xyz [charge]
Prints: 1-based index, element, neighbors, CIP code, fragment id, and key ring info.
"""
import sys
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds

def main():
    path = sys.argv[1]
    charge = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    raw = Chem.MolFromXYZFile(path)
    if raw is None:
        print("PARSE_FAIL", path); return 1
    m = Chem.Mol(raw)
    try:
        rdDetermineBonds.DetermineBonds(m, charge=charge)
    except Exception as e:
        print("BOND_PERCEPTION_FAIL", repr(e)); return 1
    Chem.AssignStereochemistryFrom3D(m)
    Chem.AssignStereochemistry(m, cleanIt=True, force=True)
    Chem.FindPotentialStereo(m)
    frags = Chem.GetMolFrags(m)
    fid = {}
    for i, fr in enumerate(frags):
        for a in fr:
            fid[a] = i
    print(f"file={path} atoms={m.GetNumAtoms()} charge={Chem.GetFormalCharge(m)} nfrag={len(frags)} smiles={Chem.MolToSmiles(m)}")
    for a in m.GetAtoms():
        nbrs = [(n.GetIdx() + 1, n.GetSymbol()) for n in a.GetNeighbors()]
        cip = a.GetPropsAsDict().get('_CIPCode', '-')
        chg = a.GetFormalCharge()
        print(f"  idx1={a.GetIdx()+1:2d} {a.GetSymbol():2s} frag={fid[a.GetIdx()]} chg={chg:+d} nbrs={nbrs} CIP={cip}")
    ri = m.GetRingInfo()
    print(f"rings={[list(r) for r in ri.AtomRings()]}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
