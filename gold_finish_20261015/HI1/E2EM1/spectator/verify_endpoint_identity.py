import sys, math, hashlib
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds
from rdkit.Chem import rdMolDescriptors

REF = "CC(C[C@@H]([O-])c1ccccc1)=[N+]1CCC[C@H]1C(=O)O.O"

def main(path):
    L = open(path).read().splitlines()
    n = int(L[0].split()[0])
    rows = [l.split() for l in L[2:2+n]]
    el = [r[0] for r in rows]
    c = [[float(v) for v in r[1:4]] for r in rows]
    print("file:", path)
    print("sha256:", hashlib.sha256(open(path,'rb').read()).hexdigest())
    print("n:", n, "elements:", " ".join(el))
    print("d(1,29)=%.3f d(1,2)=%.3f d(2,4)=%.3f d(28,29)=%.3f" % (math.dist(c[0],c[28]), math.dist(c[0],c[1]), math.dist(c[1],c[3]), math.dist(c[27],c[28])))
    block = "\n".join(["%d" % n, ""] + [" ".join(r[:4]) for r in rows]) + "\n"
    m = Chem.MolFromXYZBlock(block)
    rdDetermineBonds.DetermineBonds(m, charge=0, allowChargedFragments=True, embedChiral=True)
    Chem.AssignStereochemistryFrom3D(m)
    cips = [(a.GetIdx()+1, a.GetProp('_CIPCode')) for a in m.GetAtoms() if a.HasProp('_CIPCode')]
    print("CIP (1-based):", cips)
    for (i,j,lab) in [(0,28,'1-29'),(0,1,'1-2'),(1,3,'2-4'),(27,28,'28-29')]:
        b = m.GetBondBetweenAtoms(i,j)
        print("bond %s:" % lab, b.GetBondType() if b else None)
    try:
        bst = m.GetBondBetweenAtoms(1,3)
        print("C2=N4 (bond 2-4) stereo (3D perception):", bst.GetStereo() if bst else None)
        print("C1-C2 (bond 1-2) stereo:", m.GetBondBetweenAtoms(0,1).GetStereo() if m.GetBondBetweenAtoms(0,1) else None)
    except Exception as ex:
        print("stereo probe failed:", ex)
    smi_raw = Chem.MolToSmiles(m)
    print("endpoint canonical SMILES (with explicit H):", smi_raw)
    mh = Chem.RemoveHs(m)
    smi = Chem.MolToSmiles(mh)
    print("endpoint canonical SMILES (H-suppressed)   :", smi)
    print("reference string (verbatim):", REF)
    ref = Chem.MolFromSmiles(REF)
    refsmi = Chem.MolToSmiles(ref) if ref is not None else None
    print("reference canonical SMILES (H-suppressed)  :", refsmi)
    print("verbatim char-identical (raw vs REF string):", smi_raw == REF)
    print("char-identical H-suppressed canonical vs reference canonical:", (smi == refsmi) if refsmi else None)
    if refsmi:
        a = smi.replace('/','').replace(chr(92),'')
        b = refsmi.replace('/','').replace(chr(92),'')
        print("char-identical after dropping E/Z direction markers:", a == b)
        print("  endpoint (markers stripped):", a)
        print("  reference(markers stripped):", b)
    if ref is not None:
        full = mh.GetSubstructMatch(ref)
        print("graph/isomerism full match (endpoint H-suppressed vs reference):", bool(full) and len(full) == ref.GetNumAtoms())
        print("reference atoms:", ref.GetNumAtoms(), "endpoint H-suppressed atoms:", mh.GetNumAtoms())
    print("molformula:", rdMolDescriptors.CalcMolFormula(m))
    frs = Chem.GetMolFrags(m, asMols=True, sanitizeFrags=False)
    print("components:", len(frs), [f.GetNumAtoms() for f in frs])

if __name__ == '__main__':
    main(sys.argv[1])
