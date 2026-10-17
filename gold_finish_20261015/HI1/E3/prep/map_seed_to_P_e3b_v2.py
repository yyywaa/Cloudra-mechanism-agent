# -*- coding: utf-8 -*-
# v2: graph-isomorphism mapping (RDKit VF2, order-agnostic heavy graph) of the
# ts_0011 build product seed (41 atoms) onto the P frame (job 1061, E3 working order).
# Read-only diagnostic, no QM.
import hashlib, json
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
    el = [r[0] for r in rows]
    X = np.array([[float(r[1]), float(r[2]), float(r[3])] for r in rows])
    return el, X

el_s, X_s = load_xyz(SEED_XYZ)
el_p, X_p = load_xyz(P_XYZ)
print("seed atoms:", len(el_s), "| P atoms:", len(el_p))
print("seed census:", {e: el_s.count(e) for e in sorted(set(el_s))})
print("P census:", {e: el_p.count(e) for e in sorted(set(el_p))})
print("per-index element order identical:", el_s == el_p, "-> mapping via graph isomorphism, not index")

m_s = Chem.MolFromMolFile(SEED_MOL, removeHs=False, sanitize=False)
print("seed.mol atoms:", m_s.GetNumAtoms(), "bonds:", m_s.GetNumBonds())
print("seed.mol element order == seed.xyz:", [a.GetSymbol() for a in m_s.GetAtoms()] == el_s)
seed_bonds = {}
for b in m_s.GetBonds():
    i, j = b.GetBeginAtomIdx(), b.GetEndAtomIdx()
    seed_bonds[(min(i, j), max(i, j))] = str(b.GetBondType())

L = open(P_XYZ).read().splitlines()
n = int(L[0])
block = str(n) + chr(10) + P_XYZ + chr(10) + chr(10).join(L[2:2+n]) + chr(10)
m_p = Chem.MolFromXYZBlock(block)
rdDetermineBonds.DetermineBonds(m_p, charge=0)
print("P determined bonds:", m_p.GetNumBonds())
p_bonds = {}
for b in m_p.GetBonds():
    i, j = b.GetBeginAtomIdx(), b.GetEndAtomIdx()
    p_bonds[(min(i, j), max(i, j))] = str(b.GetBondType())

hv_s = [i for i, e in enumerate(el_s) if e != "H"]
hv_p = [i for i, e in enumerate(el_p) if e != "H"]
print("heavy atoms: seed", len(hv_s), "| P", len(hv_p), "(tolerance: none - exact element/adjacency isomorphism)")

def heavy_query(el, hv):
    rw = Chem.RWMol()
    for i in hv:
        rw.AddAtom(Chem.Atom(el[i]))
    pos = {a: k for k, a in enumerate(hv)}
    for i in hv:
        for j in hv:
            if i < j:
                pass
    return rw, pos

# seed heavy graph (bonds made order-agnostic = SINGLE)
rw_s = Chem.RWMol()
for i in hv_s: rw_s.AddAtom(Chem.Atom(el_s[i]))
pos_s = {a: k for k, a in enumerate(hv_s)}
for (i, j) in seed_bonds:
    if i in pos_s and j in pos_s:
        rw_s.AddBond(pos_s[i], pos_s[j], Chem.BondType.SINGLE)
q = rw_s.GetMol()
# P heavy graph (order-agnostic)
rw_p = Chem.RWMol()
for i in hv_p: rw_p.AddAtom(Chem.Atom(el_p[i]))
pos_p = {a: k for k, a in enumerate(hv_p)}
for (i, j) in p_bonds:
    if i in pos_p and j in pos_p:
        rw_p.AddBond(pos_p[i], pos_p[j], Chem.BondType.SINGLE)
tgt = rw_p.GetMol()
Chem.SanitizeMol(q); Chem.SanitizeMol(tgt)
matches = tgt.GetSubstructMatches(q, uniquify=False, maxMatches=100000)
print("heavy-atom isomorphism count (VF2, uniquify=False):", len(matches))

def kabsch_rmsd(A, B):
    A = A - A.mean(0); B = B - B.mean(0)
    U, S, Vt = np.linalg.svd(A.T @ B)
    d = np.sign(np.linalg.det(U @ Vt))
    R = U @ np.diag([1.0, 1.0, d]) @ Vt
    return float(np.sqrt((((A @ R) - B) ** 2).sum() / len(A)))

def h_map(heavy_map):
    hm = {}
    for h in range(len(el_s)):
        if el_s[h] != "H": continue
        par = [x for (i, j) in seed_bonds for x in ((i, j) if j == h else ((j, i) if i == h else ())) if el_s[x] != "H"]
        par = [x for (i, j) in seed_bonds if h in (i, j) for x in (i, j) if el_s[x] != "H"]
        if len(par) != 1: return None, "H%d heavy parents=%d" % (h + 1, len(par))
        pp = heavy_map[par[0]]
        cands = [hp for hp in range(len(el_p)) if el_p[hp] == "H" and (min(hp, pp), max(hp, pp)) in p_bonds]
        if len(cands) != 1: return None, "parent P%d has %d H" % (pp + 1, len(cands))
        hm[h] = cands[0]
    return hm, ""

results = []
for k, mt in enumerate(matches):
    heavy_map = {hv_s[a]: hv_p[mt[a]] for a in range(len(hv_s))}
    hm, err = h_map(heavy_map)
    if hm is None:
        results.append({"idx": k, "error": err}); continue
    full = dict(heavy_map); full.update(hm)
    if len(set(full.values())) != 41:
        results.append({"idx": k, "error": "not bijection"}); continue
    order = [full[i] for i in range(41)]
    rms_heavy = kabsch_rmsd(X_s[hv_s], X_p[[full[i] for i in hv_s]])
    rms_all = kabsch_rmsd(X_s, X_p[order])
    mism = []
    for (i, j), bo in seed_bonds.items():
        if el_s[i] == "H" or el_s[j] == "H": continue
        key = (min(full[i], full[j]), max(full[i], full[j]))
        if key not in p_bonds: mism.append([i + 1, j + 1, bo, "MISSING"])
        elif p_bonds[key] != bo: mism.append([i + 1, j + 1, bo, p_bonds[key]])
    fp = hashlib.md5(",".join(str(v + 1) for v in order).encode()).hexdigest()
    results.append({"idx": k, "order": order, "rms_heavy": rms_heavy, "rms_all": rms_all, "mismatch": mism, "fp": fp,
                    "bijection": len(set(order)) == 41 and all(el_s[i] == el_p[order[i]] for i in range(41))})

good = [r for r in results if "order" in r]
good.sort(key=lambda x: x["rms_heavy"])
print("complete candidates:", len(good), "| errors:", len(results) - len(good))
for r in good[:6]:
    print("  cand %2d heavy-Kabsch %.4f A | all-atom %.4f A | bond-order mismatches %d | bijection+element ok %s | MD5 %s"
          % (r["idx"], r["rms_heavy"], r["rms_all"], len(r["mismatch"]), r["bijection"], r["fp"]))
if len(good) > 1:
    print("top-2 RMSD delta = %.4f A (%.4f vs %.4f)" % (good[1]["rms_heavy"] - good[0]["rms_heavy"], good[0]["rms_heavy"], good[1]["rms_heavy"]))
best = min(good, key=lambda x: (len(x["mismatch"]), x["rms_heavy"]))
order = best["order"]; inv = {v: k for k, v in enumerate(order)}
print("CHOSEN cand", best["idx"], "heavy RMSD %.4f A, all-atom %.4f A, mismatches %d, MD5 %s"
      % (best["rms_heavy"], best["rms_all"], len(best["mismatch"]), best["fp"]))
print("bond-order mismatch edges (seed 1-based i,j, seed order, P order):", best["mismatch"])
print("--- 41-row mapping seed -> E3 working order ---")
for i in range(41):
    print("  seed %2d %-2s -> E3 %2d %-2s" % (i + 1, el_s[i], order[i] + 1, el_p[order[i]]))
print("--- hard check: E3 atom 2 (C2) neighbours in P and their seed partners ---")
nb_p = sorted([j for (i, j) in p_bonds if i == 1] + [i for (i, j) in p_bonds if j == 1])
print("P atom2 neighbours:", [(j + 1, el_p[j]) for j in nb_p])
print("their seed partners:", [(j + 1, el_p[j], inv[j] + 1, el_s[inv[j]]) for j in nb_p])
print("--- coordinator candidate hypotheses (verification only) ---")
for lbl, sidx in [("N32", 31), ("O27-H33", 26), ("H33", 32), ("O6-H19", 5), ("H19", 18)]:
    print("  %-8s seed %2d -> E3 %2d (%s)" % (lbl, sidx + 1, inv[sidx] + 1, el_p[order[sidx]]))
print("--- 5 key bonds: seed-side vs P-side ---")
KEY = [("C2-N4", 2, 4), ("C2-O25", 2, 25), ("N4-H26", 4, 26), ("O25-H26", 25, 26), ("O10-H27", 10, 27)]
kb = []
for name, a, b in KEY:
    ia, ib = inv[a - 1], inv[b - 1]
    ds = float(np.linalg.norm(X_s[ia] - X_s[ib])); dp = float(np.linalg.norm(X_p[a - 1] - X_p[b - 1]))
    kb.append({"bond": name, "seed_atoms_1based": [ia + 1, ib + 1], "seed_A": round(ds, 4),
               "e3_atoms_1based": [a, b], "P_A": round(dp, 4), "seed_minus_P": round(ds - dp, 4)})
    print("  %-8s seed(%2d,%2d)=%.4f A | P(%2d,%2d)=%.4f A | seed-P=%+.4f A" % (name, ia + 1, ib + 1, ds, a, b, dp, ds - dp))
prod_side = [x for x in kb if x["bond"] == "N4-H26"][0]["seed_A"] < 1.4 and [x for x in kb if x["bond"] == "O25-H26"][0]["seed_A"] > 2.2
print("VERDICT seed already product-side at bond-table level (N4-H26 ~1.0 and O25-H26 ~3):", prod_side)
out = {"rms_heavy": best["rms_heavy"], "rms_all": best["rms_all"], "md5": best["fp"],
       "n_iso_heavy": len(matches), "n_complete": len(good), "element_order_identical_per_index": el_s == el_p,
       "order_seed_to_P_1based": [v + 1 for v in order], "bond_mismatch": best["mismatch"],
       "key_bonds": kb, "seed_product_side_bondtable": bool(prod_side),
       "alts": [{"idx": r["idx"], "rms_heavy": round(r["rms_heavy"], 4), "md5": r["fp"], "nmism": len(r["mismatch"])} for r in good[:8]]}
open(BASE + "gold_finish_20261015/HI1/E3/prep/seed_to_P_mapping.json", "w").write(json.dumps(out, indent=2, ensure_ascii=False))
print("wrote prep/seed_to_P_mapping.json")
