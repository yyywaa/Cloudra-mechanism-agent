# -*- coding: utf-8 -*-
# v3: full 41-atom graph-isomorphism mapping (RDKit VF2 on order-agnostic heavy graph,
# then exhaustive H-permutation completion) of the ts_0011 build product seed onto the
# P frame (job 1061, E3 working order). Read-only diagnostic, no QM.
import hashlib, json
from itertools import permutations, product
import numpy as np
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds

BASE = "/home/ly/Cloudra-mechanism-agent/"
SEED_XYZ = BASE + "ts/ts_0011/build/input_0004/product/seed.xyz"
SEED_MOL = BASE + "ts/ts_0011/build/input_0004/product/seed.mol"
P_XYZ = BASE + "gold_finish_20261015/HI1/E3/prep/P_1061_optframe.xyz"

def load_xyz(p):
    L = open(p).read().splitlines()
    n = int(L[0]); rows = [l.split() for l in L[2:2+n]]
    return [r[0] for r in rows], np.array([[float(r[1]), float(r[2]), float(r[3])] for r in rows])

el_s, X_s = load_xyz(SEED_XYZ)
el_p, X_p = load_xyz(P_XYZ)
print("seed atoms:", len(el_s), "| P atoms:", len(el_p))
print("seed census:", {e: el_s.count(e) for e in sorted(set(el_s))}, "| P census:", {e: el_p.count(e) for e in sorted(set(el_p))})
print("per-index element order identical:", el_s == el_p, "-> mapping by graph isomorphism, not by index")

m_s = Chem.MolFromMolFile(SEED_MOL, removeHs=False, sanitize=False)
seed_bonds = {}
for b in m_s.GetBonds():
    i, j = b.GetBeginAtomIdx(), b.GetEndAtomIdx()
    seed_bonds[(min(i, j), max(i, j))] = str(b.GetBondType())
L = open(P_XYZ).read().splitlines(); n = int(L[0])
m_p = Chem.MolFromXYZBlock(str(n) + chr(10) + P_XYZ + chr(10) + chr(10).join(L[2:2+n]) + chr(10))
rdDetermineBonds.DetermineBonds(m_p, charge=0)
p_bonds = {}
for b in m_p.GetBonds():
    i, j = b.GetBeginAtomIdx(), b.GetEndAtomIdx()
    p_bonds[(min(i, j), max(i, j))] = str(b.GetBondType())
print("seed.mol atoms/bonds:", m_s.GetNumAtoms(), m_s.GetNumBonds(), "| P determined bonds:", m_p.GetNumBonds())

hv_s = [i for i, e in enumerate(el_s) if e != "H"]
hv_p = [i for i, e in enumerate(el_p) if e != "H"]
pos_s = {a: k for k, a in enumerate(hv_s)}
pos_p = {a: k for k, a in enumerate(hv_p)}
rw_s = Chem.RWMol(); [rw_s.AddAtom(Chem.Atom(el_s[i])) for i in hv_s]
for (i, j) in seed_bonds:
    if i in pos_s and j in pos_s: rw_s.AddBond(pos_s[i], pos_s[j], Chem.BondType.SINGLE)
rw_p = Chem.RWMol(); [rw_p.AddAtom(Chem.Atom(el_p[i])) for i in hv_p]
for (i, j) in p_bonds:
    if i in pos_p and j in pos_p: rw_p.AddBond(pos_p[i], pos_p[j], Chem.BondType.SINGLE)
q = rw_s.GetMol(); tgt = rw_p.GetMol()
Chem.SanitizeMol(q); Chem.SanitizeMol(tgt)
matches = tgt.GetSubstructMatches(q, uniquify=False, maxMatches=100000)
print("heavy-atom isomorphism count (VF2, order-agnostic, uniquify=False):", len(matches))

def kabsch_rmsd(A, B):
    A = A - A.mean(0); B = B - B.mean(0)
    U, S, Vt = np.linalg.svd(A.T @ B)
    d = np.sign(np.linalg.det(U @ Vt))
    R = U @ np.diag([1.0, 1.0, d]) @ Vt
    return float(np.sqrt((((A @ R) - B) ** 2).sum() / len(A)))

seed_h = {}
for h in range(len(el_s)):
    if el_s[h] != "H": continue
    par = [x for (i, j) in seed_bonds if h in (i, j) for x in (i, j) if el_s[x] != "H"]
    seed_h.setdefault(par[0], []).append(h)
print("H-bearing heavy parents (seed): ", {k + 1: len(v) for k, v in sorted(seed_h.items())})

cands = []
for k, mt in enumerate(matches):
    heavy_map = {hv_s[a]: hv_p[mt[a]] for a in range(len(hv_s))}
    groups = []
    ok = True
    for ps in sorted(seed_h):
        pp = heavy_map[ps]
        tgtH = [hp for hp in range(len(el_p)) if el_p[hp] == "H" and (min(hp, pp), max(hp, pp)) in p_bonds]
        if len(tgtH) != len(seed_h[ps]): ok = False; break
        groups.append((seed_h[ps], sorted(tgtH)))
    if not ok: continue
    for choice in product(*[list(permutations(t)) for (s, t) in groups]):
        full = dict(heavy_map)
        for (s, t), pm in zip(groups, choice):
            for h, hp in zip(s, pm): full[h] = hp
        order = [full[i] for i in range(41)]
        if len(set(order)) != 41 or any(el_s[i] != el_p[order[i]] for i in range(41)): continue
        rms_heavy = kabsch_rmsd(X_s[hv_s], X_p[[full[i] for i in hv_s]])
        rms_all = kabsch_rmsd(X_s, X_p[order])
        mism = []
        for (i, j), bo in seed_bonds.items():
            if el_s[i] == "H" or el_s[j] == "H": continue
            key = (min(full[i], full[j]), max(full[i], full[j]))
            if key not in p_bonds: mism.append([i + 1, j + 1, bo, "MISSING"])
            elif p_bonds[key] != bo: mism.append([i + 1, j + 1, bo, p_bonds[key]])
        fp = hashlib.md5(",".join(str(v + 1) for v in order).encode()).hexdigest()
        cands.append({"iso": k, "order": order, "rms_heavy": rms_heavy, "rms_all": rms_all, "mismatch": mism, "fp": fp})
print("distinct complete 41-atom mappings:", len(cands))
cands.sort(key=lambda x: (len(x["mismatch"]), x["rms_heavy"]))
for c in cands[:8]:
    print("  iso %d heavy-Kabsch %.4f A | all-atom %.4f A | bond-order mismatches %d | MD5 %s" % (c["iso"], c["rms_heavy"], c["rms_all"], len(c["mismatch"]), c["fp"]))
by_rms = sorted(cands, key=lambda x: x["rms_heavy"])
print("top-2 by heavy RMSD: %.4f / %.4f A ; delta = %.4f A" % (by_rms[0]["rms_heavy"], by_rms[1]["rms_heavy"], by_rms[1]["rms_heavy"] - by_rms[0]["rms_heavy"]))
best = cands[0]
order = best["order"]; inv = {v: k for k, v in enumerate(order)}
print("CHOSEN: iso %d, heavy RMSD %.4f A, all-atom %.4f A, bond-order mismatches %d, MD5 %s"
      % (best["iso"], best["rms_heavy"], best["rms_all"], len(best["mismatch"]), best["fp"]))
print("bond-order mismatch rows (seed i,j 1-based, seed order, P order):", best["mismatch"])
print("--- 41-row mapping seed -> E3 working order ---")
for i in range(41):
    print("  seed %2d %-2s -> E3 %2d %-2s" % (i + 1, el_s[i], order[i] + 1, el_p[order[i]]))
print("--- hard check: E3 atom 2 (C2) neighbours in P + their seed partners ---")
nb_p = sorted([j for (i, j) in p_bonds if i == 1] + [i for (i, j) in p_bonds if j == 1])
print("P atom2 neighbours:", [(j + 1, el_p[j]) for j in nb_p])
print("their seed partners:", [(j + 1, el_p[j], inv[j] + 1, el_s[inv[j]]) for j in nb_p])
print("--- coordinator candidate hypotheses (verification only) ---")
for lbl, sidx in [("N32", 31), ("O27", 26), ("H33", 32), ("O6", 5), ("H19", 18)]:
    print("  %-6s seed %2d -> E3 %2d (%s)" % (lbl, sidx + 1, inv[sidx] + 1, el_p[order[sidx]]))
print("--- 5 key bonds: seed-side vs P-side ---")
KEY = [("C2-N4", 2, 4), ("C2-O25", 2, 25), ("N4-H26", 4, 26), ("O25-H26", 25, 26), ("O10-H27", 10, 27)]
kb = []
for name, a, b in KEY:
    ia, ib = inv[a - 1], inv[b - 1]
    ds = float(np.linalg.norm(X_s[ia] - X_s[ib])); dp = float(np.linalg.norm(X_p[a - 1] - X_p[b - 1]))
    kb.append({"bond": name, "seed_atoms_1based": [ia + 1, ib + 1], "seed_A": round(ds, 4), "e3_atoms_1based": [a, b], "P_A": round(dp, 4), "seed_minus_P": round(ds - dp, 4)})
    print("  %-8s seed(%2d,%2d)=%.4f A | P(%2d,%2d)=%.4f A | seed-P=%+.4f A" % (name, ia + 1, ib + 1, ds, a, b, dp, ds - dp))
prod_side = [x for x in kb if x["bond"] == "N4-H26"][0]["seed_A"] < 1.4 and [x for x in kb if x["bond"] == "O25-H26"][0]["seed_A"] > 2.2
print("VERDICT seed already product-side at bond-table level (N4-H26 ~1.0 AND O25-H26 ~3):", prod_side)
open(BASE + "gold_finish_20261015/HI1/E3/prep/seed_to_P_mapping.json", "w").write(json.dumps(
    {"chosen": {"iso": best["iso"], "rms_heavy": best["rms_heavy"], "rms_all": best["rms_all"], "md5": best["fp"],
                "order_seed_to_P_1based": [v + 1 for v in order], "bond_mismatch": best["mismatch"]},
     "n_iso_heavy": len(matches), "n_complete": len(cands), "key_bonds": kb, "seed_product_side_bondtable": bool(prod_side),
     "top2": [{"iso": c["iso"], "rms_heavy": c["rms_heavy"], "md5": c["fp"]} for c in by_rms[:4]],
     "all_candidates": [{"iso": c["iso"], "rms_heavy": round(c["rms_heavy"], 4), "rms_all": round(c["rms_all"], 4), "nmism": len(c["mismatch"]), "md5": c["fp"]} for c in cands]},
    indent=2, ensure_ascii=False))
print("wrote prep/seed_to_P_mapping.json")
