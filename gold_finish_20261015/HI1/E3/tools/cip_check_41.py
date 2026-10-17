#!/usr/bin/env python3
"""CIP / connectivity check for a 41-atom frame (P endpoint, hemiaminal, etc.).

Reads an .xyz, perceives bonds with RDKit DetermineBonds (charge given), assigns
stereochemistry from 3D, and prints: atom count, fragment sizes, all CIP centres,
the per-fragment canonical isomeric SMILES, and a few requested distances.

Usage: python3 cip_check_41.py frame.xyz [charge]
"""
import sys
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds, rdMolDescriptors

PAIRS = [(2, 4), (2, 25), (25, 27), (10, 27), (9, 10), (9, 11), (4, 26), (2, 26)]


def dist(conf, i, j):
    a = conf.GetAtomPosition(i - 1)
    b = conf.GetAtomPosition(j - 1)
    return (a - b).Length()


def main():
    path = sys.argv[1]
    charge = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    raw = Chem.MolFromXYZFile(path)
    if raw is None:
        raise SystemExit("cannot read " + path)
    mol = Chem.Mol(raw)
    rdDetermineBonds.DetermineBonds(mol, charge=charge)
    Chem.AssignStereochemistryFrom3D(mol)
    conf = mol.GetConformer()
    frags = Chem.GetMolFrags(mol)
    print("file:", path)
    print("natoms:", mol.GetNumAtoms())
    print("fragments:", [len(f) for f in frags])
    print("formula:", rdMolDescriptors.CalcMolFormula(mol))
    print("minsep_A: %.4f" % min(
        dist(conf, i + 1, j + 1)
        for i in range(mol.GetNumAtoms())
        for j in range(i + 1, mol.GetNumAtoms())))
    for p in PAIRS:
        print("R(%d,%d): %.4f" % (p[0], p[1], dist(conf, p[0], p[1])))
    for a in mol.GetAtoms():
        if a.HasProp("_CIPCode"):
            print("CIP atom %d %s = %s  neighbours(1-based) %s" % (
                a.GetIdx() + 1, a.GetSymbol(), a.GetProp("_CIPCode"),
                [n.GetIdx() + 1 for n in a.GetNeighbors()]))
    noh = Chem.RemoveHs(mol)  # heavy atoms only
    print("isomeric_smiles_all:", Chem.MolToSmiles(noh))
    for k, fm in enumerate(Chem.GetMolFrags(noh, asMols=True, sanitizeFrags=True)):
        print("frag%d_smiles:" % (k + 1), Chem.MolToSmiles(fm))


if __name__ == "__main__":
    main()
