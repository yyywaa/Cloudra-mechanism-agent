#!/usr/bin/env python3
"""HI1_E1 / lane1 — product-endpoint (I1) verification and heavy_atom_binding derivation.
Read-only analysis: no QM. Checks (1) xyz vs given MOL bond table/atom order,
(2) fragment composition vs declared product_smiles, (3) declared-SMILES heavy-atom order ->
file atom indices (the list to declare as heavy_atom_binding), (4) CIP of C-alpha.
"""
import json, hashlib, sys
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds, rdMolDescriptors

WS = "/home/ly/Cloudra-mechanism-agent"
PROD_XYZ = WS + "/gold_finish_20261015/HI1/E1/build/I1_S_start.xyz"
GIVEN_MOL = WS + "/gold_finish_20261015/HI1/E2EM1/build/I1_S_start_bonded.mol"
RC_XYZ = WS + "/gold_finish_20261015/HI1/E1/lane1/RC_S_canonical.xyz"
DECL = WS + "/ts/ts_0008/declare.json"

def sha(p):
    return hashlib.sha256(open(p,'rb').read()).hexdigest()

print("sha256 xyz   =", sha(PROD_XYZ))
print("sha256 gmol  =", sha(GIVEN_MOL))

decl = json.load(open(DECL))
rxn = decl["reaction"] if "reaction" in decl else decl["input"]["reaction"]
print("reactant_smiles =", rxn["reactant_smiles"])
print("product_smiles  =", rxn["product_smiles"])

# ---- geometry from xyz + bond perception
xyzmol = Chem.MolFromXYZFile(PROD_XYZ)
mol = Chem.RWMol(xyzmol)
rdDetermineBonds.DetermineBonds(mol, charge=0)
mol = mol.GetMol()
frags = Chem.GetMolFrags(mol, asMols=True, sanitizeFrags=True)
print("n_atoms =", mol.GetNumAtoms(), " n_fragments =", len(frags))
print("formula =", rdMolDescriptors.CalcMolFormula(mol))
for i,f in enumerate(frags):
    print("  frag%d = %s  (natoms %d)" % (i, Chem.MolToSmiles(Chem.RemoveHs(f)), f.GetNumAtoms()))

# ---- given MOL: same atom order + bond table?
gmol = Chem.MolFromMolFile(GIVEN_MOL, removeHs=False, sanitize=False)
ok_order = True
for i in range(mol.GetNumAtoms()):
    a, b = mol.GetAtomWithIdx(i), gmol.GetAtomWithIdx(i)
    pa, pb = mol.GetConformer().GetAtomPosition(i), gmol.GetConformer().GetAtomPosition(i)
    if a.GetSymbol() != b.GetSymbol() or max(abs(pa.x-pb.x),abs(pa.y-pb.y),abs(pa.z-pb.z)) > 2e-4:
        ok_order = False; print("MISMATCH atom", i+1)
print("given MOL atom order+coords identical to xyz (max dev 2e-4 A):", ok_order)
def kb(m):
    mm = Chem.Mol(m)
    Chem.Kekulize(mm, clearAromaticFlags=True)
    return sorted(tuple(sorted((b.GetBeginAtomIdx()+1, b.GetEndAtomIdx()+1)))+(int(b.GetBondTypeAsDouble()),) for b in mm.GetBonds())
print("bond tables identical after Kekulize-normalisation (xyz-perceived vs given MOL):", kb(mol) == kb(gmol))
print("canonical SMILES identical:", Chem.MolToSmiles(Chem.RemoveHs(mol)) == Chem.MolToSmiles(Chem.RemoveHs(gmol)),
      Chem.MolToSmiles(Chem.RemoveHs(gmol)))
print("bond table (1-based, given MOL, Kekule):")
print("  " + " ".join("%d-%d:%d" % b for b in kb(gmol)))
print("formal charges (xyz perception):", [a.GetFormalCharge() for a in mol.GetAtoms() if a.GetFormalCharge()!=0])
print("total charge:", sum(a.GetFormalCharge() for a in mol.GetAtoms()))

# ---- declared product SMILES -> file index map (heavy atoms, SMILES token order)
psmi = Chem.MolFromSmiles(rxn["product_smiles"])
psmi_heavy = Chem.RemoveHs(psmi)
amap = [a.GetAtomMapNum() for a in psmi_heavy.GetAtoms()]
print("product SMILES heavy-atom order, map labels:", amap)
heavy_idx = [i for i,a in enumerate(mol.GetAtoms()) if a.GetAtomicNum() > 1]
print("file heavy-atom indices (1-based, in file order):", [i+1 for i in heavy_idx])
match = Chem.RemoveHs(mol).GetSubstructMatch(psmi_heavy, useChirality=False)
match_chiral = Chem.RemoveHs(mol).GetSubstructMatch(psmi_heavy, useChirality=True)
idx = [heavy_idx[m]+1 for m in match]
print("heavy_atom_binding.indices (declared-SMILES heavy order -> 1-based file idx):", idx)
print("element check:", [(psmi_heavy.GetAtomWithIdx(i).GetSymbol(), mol.GetAtomWithIdx(match[i]).GetSymbol()) for i in range(psmi_heavy.GetNumAtoms()) if psmi_heavy.GetAtomWithIdx(i).GetSymbol()!=mol.GetAtomWithIdx(match[i]).GetSymbol()] or "all match")
print("chirality-consistent substructure match present:", bool(match_chiral), (list(match_chiral) if match_chiral else ""))

# ---- CIP labels
Chem.AssignStereochemistryFrom3D(mol)
Chem.AssignCIPLabels(mol)
cips = [(a.GetIdx()+1, a.GetSymbol(), a.GetPropsAsDict().get('_CIPCode')) for a in mol.GetAtoms() if a.HasProp('_CIPCode')]
print("I1 file CIP (3D):", cips)
Chem.AssignCIPLabels(psmi)
print("declared product_smiles CIP:", [(a.GetIdx(), a.GetAtomMapNum(), a.GetPropsAsDict().get('_CIPCode')) for a in psmi.GetAtoms() if a.HasProp('_CIPCode')])
rsmi = Chem.MolFromSmiles(rxn["reactant_smiles"])
Chem.AssignCIPLabels(rsmi)
print("declared reactant_smiles CIP:", [(a.GetIdx(), a.GetAtomMapNum(), a.GetPropsAsDict().get('_CIPCode')) for a in rsmi.GetAtoms() if a.HasProp('_CIPCode')])

# ---- RC reference geometry C-alpha
rc = Chem.RWMol(Chem.MolFromXYZFile(RC_XYZ))
rdDetermineBonds.DetermineBonds(rc, charge=0)
rc = rc.GetMol()
Chem.AssignStereochemistryFrom3D(rc)
Chem.AssignCIPLabels(rc)
print("RC file CIP (3D):", [(a.GetIdx()+1, a.GetSymbol(), a.GetPropsAsDict().get('_CIPCode')) for a in rc.GetAtoms() if a.HasProp('_CIPCode')])
print("RC formula:", rdMolDescriptors.CalcMolFormula(rc), "frags:", len(Chem.GetMolFrags(rc)))
