#!/usr/bin/env python3
"""NY3 包只读几何/身份核验：把给定 XYZ 坐标套到给定 MOL 模板（含 bond block + M CHG）上，
用 RDKit AssignStereochemistryFrom3D 实测 CIP；并打印若干距离。
用法: geom_check.py <template.mol> <frame.xyz> [i,j ...]
"""
import sys
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def read_xyz(p):
    # NOTE: the comment line may be blank -> do NOT drop blank lines positionally
    L = [l.rstrip("\n") for l in open(p)]
    n = int(L[0].split()[0])
    at, i = [], 2
    while len(at) < n:
        if i >= len(L):
            raise SystemExit("xyz truncated: %s" % p)
        if L[i].strip():
            f = L[i].split()
            at.append((f[0], float(f[1]), float(f[2]), float(f[3])))
        i += 1
    return at

def main():
    tmpl, frame = sys.argv[1], sys.argv[2]
    at = read_xyz(frame)
    lines = open(tmpl).read().split("\n")
    nat = int(lines[3][0:3])
    assert nat == len(at), (nat, len(at))
    for i in range(nat):
        old = lines[4 + i]
        tail = old[34:] if len(old) > 34 else ""
        s, x, y, z = at[i]
        lines[4 + i] = "%10.4f%10.4f%10.4f %-3s%s" % (x, y, z, s, tail)
    mb = "\n".join(lines)
    mol = Chem.MolFromMolBlock(mb, removeHs=False, sanitize=True)
    if mol is None:
        print("MOLPARSE_FAILED"); return 1
    Chem.AssignStereochemistryFrom3D(mol, confId=0, replaceExistingTags=True)
    Chem.AssignCIPLabels(mol)
    print("formula:", rdMolDescriptors.CalcMolFormula(mol))
    print("chiral centers (idx,CIP):", Chem.FindMolChiralCenters(mol, includeUnassigned=True, useLegacyImplementation=False))
    for a in mol.GetAtoms():
        if a.HasProp("_CIPCode"):
            print("  atom", a.GetIdx() + 1, a.GetSymbol(), "CIP=", a.GetProp("_CIPCode"))
    print("canonical SMILES:", Chem.MolToSmiles(Chem.RemoveHs(mol)))
    conf = mol.GetConformer()
    for pair in sys.argv[3:]:
        i, j = [int(t) for t in pair.split(",")]
        p, q = conf.GetAtomPosition(i - 1), conf.GetAtomPosition(j - 1)
        print("  d(%d,%d)= %.3f" % (i, j, (p - q).Length()))
    return 0

sys.exit(main())
