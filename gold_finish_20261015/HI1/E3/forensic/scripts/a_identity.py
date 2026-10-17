#!/usr/bin/env python3
"""
HI1/E3 ts_0011 identity forensics -- READ-ONLY, zero submissions.
Part A: structure identity (declared SMILES / built MOL / optimized endpoint frames / P / I2)
        + perceived bond tables + H-attachment + key distances + RMSD.
Every kept number carries file path, line number where applicable, and same-run sha256.
"""
import hashlib, json, math, os, sys
import numpy as np
from rdkit import Chem, RDLogger
from rdkit.Chem import rdDetermineBonds
from rdkit.Chem.rdMolDescriptors import CalcMolFormula
RDLogger.DisableLog("rdApp.*")

ROOT = "/home/ly/Cloudra-mechanism-agent"
RUN = ROOT + "/ts/ts_0011"
JOB = RUN + "/jobs/declaration_0004"
E3 = ROOT + "/gold_finish_20261015/HI1/E3"
NATOMS = 41
H2K = 627.5094740631
Z2SYM = {1: "H", 6: "C", 7: "N", 8: "O"}

_sha = {}
def sha(p):
    if p not in _sha:
        h = hashlib.sha256()
        with open(p, "rb") as fh:
            for c in iter(lambda: fh.read(1 << 20), b""):
                h.update(c)
        _sha[p] = h.hexdigest()
    return _sha[p]
def rel(p): return p.replace(ROOT + "/", "")
def rd(p):
    with open(p, "r", errors="replace") as fh: return fh.read().splitlines()
def read_xyz(p):
    L = rd(p); n = int(L[0].split()[0]); ats = []
    for k in range(n):
        q = L[2 + k].split()
        ats.append((q[0], float(q[1]), float(q[2]), float(q[3])))
    return ats, L[1]
def dist(a, b): return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(3)))
def d(ats, i, j): return dist(ats[i - 1][1:], ats[j - 1][1:])
def dmin(ats): 
    best = (9e9, 0, 0)
    for i in range(len(ats)):
        for j in range(i + 1, len(ats)):
            dd = dist(ats[i][1:], ats[j][1:])
            if dd < best[0]: best = (dd, i + 1, j + 1)
    return best

OUT = []
def say(*a): OUT.append(" ".join(str(x) for x in a))

proc = json.load(open(RUN + "/process.json"))
amap = proc["input_binding"]["atom_map"]
work_sym = [a["symbol"] for a in proc["structures"]["reactant"]["atoms"]]

def mol_xyz(ats, name="", charge=0):
    blk = "%d\n%s\n" % (len(ats), name) + "".join(
        "%s %.8f %.8f %.8f\n" % a for a in ats)
    m = Chem.MolFromXYZBlock(blk)
    assert m is not None and m.GetNumAtoms() == NATOMS
    rdDetermineBonds.DetermineBonds(m, charge=charge, allowChargedFragments=True, embedChiral=True)
    return m

def ik(m):
    from rdkit.Chem.inchi import MolToInchiKey
    return MolToInchiKey(m)

def smi(m): return Chem.MolToSmiles(Chem.RemoveHs(m))

def describe(tag, ats, charge=0, show_bonds=True):
    say("\n### %s" % tag)
    say("   symbols:", "".join(a[0] for a in ats))
    try:
        m = mol_xyz(ats, tag, charge)
    except Exception as exc:
        say("   BOND PERCEPTION FAILED:", exc); return None
    say("   formula=%s  charge=%d  fragments=%d" % (CalcMolFormula(m), Chem.GetFormalCharge(m),
                                                    len(Chem.GetMolFrags(m))))
    s = smi(m); k = ik(m)
    say("   canonical(SMILES-order-independent) SMILES =", s)
    say("   InChIKey =", k)
    if show_bonds:
        hb = []
        for b in m.GetBonds():
            a1, a2 = b.GetBeginAtom(), b.GetEndAtom()
            if a1.GetSymbol() == "H" or a2.GetSymbol() == "H": continue
            i, j = sorted((a1.GetIdx() + 1, a2.GetIdx() + 1))
            hb.append((i, j, a1.GetSymbol() + a2.GetSymbol(), str(b.GetBondType()),
                       round(dist(ats[i - 1][1:], ats[j - 1][1:]), 4)))
        say("   heavy bonds (%d): %s" % (len(hb), " ".join(
            "%d-%d%s:%s@%.3f" % x for x in sorted(set(hb)))))
        # H attachment, heavy atom + distance
        ha = []
        for b in m.GetBonds():
            a1, a2 = b.GetBeginAtom(), b.GetEndAtom()
            if a1.GetSymbol() == "H" and a2.GetSymbol() != "H":
                h, p = a1.GetIdx() + 1, a2.GetIdx() + 1
            elif a2.GetSymbol() == "H" and a1.GetSymbol() != "H":
                h, p = a2.GetIdx() + 1, a1.GetIdx() + 1
            else: continue
            ha.append("%dH-%d%s@%.3f" % (h, p, ats[p - 1][0], dist(ats[h - 1][1:], ats[p - 1][1:])))
        say("   H attachment (%d): %s" % (len(ha), " ".join(ha)))
    return m

# ------------------------------------------------------------------ structures
S = {}
S["A1_declared_reactant_smiles"] = ("SMILES", proc["input"]["reaction"]["reactant_smiles"])
S["A2_declared_product_smiles"] = ("SMILES", proc["input"]["reaction"]["product_smiles"])

xyz_paths = {
 "B1_reactant_seed_xyz": RUN + "/build/input_0004/reactant/seed.xyz",
 "B2_product_seed_xyz":  RUN + "/build/input_0004/product/seed.xyz",
 "B3_buildP_cand000_xyz": E3 + "/prep/structure_build_P/assembly/complex_candidate_000.xyz",
 "C1_ts_guess_xyz":      E3 + "/prep/guess_c2o25_190/ts_guess_c2o25_190.xyz",
 "D1_I2_min_xyz":        E3 + "/runs/I2_optfreq/I2_min_v5.xyz",
 "D2_P_1061_frame_xyz":  E3 + "/prep/P_1061_optframe.xyz",
 "D3_P_seed41_xyz":      E3 + "/prep/P_e3b_product_41_seed.xyz",
}
mol_paths = {
 "B1m_reactant_seed_mol": RUN + "/build/input_0004/reactant/seed.mol",
 "B2m_product_seed_mol":  RUN + "/build/input_0004/product/seed.mol",
 "B3m_buildP_cand000_mol": E3 + "/prep/structure_build_P/assembly/complex_candidate_000.mol",
}

say("# HI1/E3 ts_0011 IDENTITY FORENSICS -- part A (structures)")
say("\n## A. FILE SHA256 (this run)")
for k, p in list(xyz_paths.items()) + list(mol_paths.items()):
    say("| %-24s | %-95s | sha256=%s |" % (k, rel(p), sha(p) if os.path.exists(p) else "MISSING"))

say("\n## B. DECLARED SPECIES (from process.json input.reaction, sha256=%s)" % sha(RUN + "/process.json"))
for tag, key in (("reactant_smiles", "reactant_smiles"), ("product_smiles", "product_smiles")):
    s = proc["input"]["reaction"][key]
    m = Chem.MolFromSmiles(s)
    mc = Chem.Mol(m)
    for _a in mc.GetAtoms(): _a.SetAtomMapNum(0)
    say("\n### %s (declared string)" % tag)
    say("   raw      =", s)
    say("   canonical=", Chem.MolToSmiles(mc))
    say("   formula=%s charge=%d fragments=%d" % (CalcMolFormula(m), Chem.GetFormalCharge(m),
                                                 len(Chem.GetMolFrags(m))))
    say("   InChIKey =", ik(m))
    say("   per-fragment:", [ik(f) for f in Chem.GetMolFrags(m, asMols=True)])

# ------------------------------------------------------------------ geometry
say("\n## C. GEOMETRY-DERIVED STRUCTURES")
mols = {}
for tag, p in xyz_paths.items():
    ats, comment = read_xyz(p)
    say("\n### %s   (%s)" % (tag, rel(p)))
    say("   comment/line2 = %r ; sha256=%s" % (comment[:120], sha(p)))
    say("   symbols=%s" % "".join(a[0] for a in ats))
    say("   same element order as canonical work table? %s" % ("".join(a[0] for a in ats) == "".join(work_sym)))
    b = dmin(ats); say("   min interatomic distance = %.4f A (%d-%d)" % b)
    mols[tag] = describe(tag + " [perceived]", ats)

for tag, p in mol_paths.items():
    say("\n### %s   (%s)  sha256=%s" % (tag, rel(p), sha(p)))
    m = Chem.MolFromMolFile(p, removeHs=False, sanitize=True)
    if m is None:
        say("   RDKit could not sanitize this MOL"); continue
    say("   formula=%s charge=%d fragments=%d" % (CalcMolFormula(m), Chem.GetFormalCharge(m),
                                                 len(Chem.GetMolFrags(m))))
    say("   canonical SMILES =", smi(m))
    say("   InChIKey =", ik(m))
    mols[tag] = m

print("\n".join(OUT))
