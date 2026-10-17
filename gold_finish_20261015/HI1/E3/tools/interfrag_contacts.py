import sys, math
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds
p = sys.argv[1]
m = Chem.MolFromXYZFile(p); rdDetermineBonds.DetermineBonds(m, charge=0)
conf = m.GetConformer()
c = [(conf.GetAtomPosition(i).x, conf.GetAtomPosition(i).y, conf.GetAtomPosition(i).z) for i in range(m.GetNumAtoms())]
frags = Chem.GetMolFrags(m); fid = {}
for i, fr in enumerate(frags):
    for a in fr: fid[a] = i
def d(i,j):
    return math.dist(c[i], c[j])
pairs = []
for i in range(m.GetNumAtoms()):
    for j in range(i+1, m.GetNumAtoms()):
        if fid[i] != fid[j]:
            pairs.append((round(d(i,j),3), i+1, m.GetAtomWithIdx(i).GetSymbol(), j+1, m.GetAtomWithIdx(j).GetSymbol(), f"{fid[i]}-{fid[j]}"))
pairs.sort()
for x in pairs[:12]: print(x)
