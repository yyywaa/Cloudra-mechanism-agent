# -*- coding: utf-8 -*-
# Graph-isomorphism mapping of the ts_0011 build product seed (41 atoms) onto the
# P frame (job 1061, E3 working order).  Read-only diagnostic, no QM.
import math, hashlib, itertools
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
print("seed atoms:", len(el_s), "P atoms:", len(el_p))
print("seed element census:", {e: el_s.count(e) for e in sorted(set(el_s))})
print("P element census:", {e: el_p.count(e) for e in sorted(set(el_p))})
print("element ORDER identical (per-index):", el_s == el_p, "-> mapping is done by graph isomorphism, not by index")

# ---- seed bond table from seed.mol (concrete) ----
m_s = Chem.MolFromMolFile(SEED_MOL, removeHs=False, sanitize=False)
assert m_s is not None, "seed.mol unreadable"
print("seed.mol atoms:", m_s.GetNumAtoms(), "bonds:", m_s.GetNumBonds())
s_el = [a.GetSymbol() for a in m_s.GetAtoms()]
print("seed.mol vs seed.xyz element order identical:", s_el == el_s)
seed_bonds = {}
for b in m_s.GetBonds():
    i, j = b.GetBeginAtomIdx(), b.GetEndAtomIdx()
    seed_bonds[(min(i, j), max(i, j))] = str(b.GetBondType())

# ---- P bond table from the real P geometry (rdDetermineBonds, charge 0) ----
L = open(P_XYZ).read().splitlines()
n = int(L[0])
block = str(n) + chr(10) + P_XYZ + chr(10) + chr(10).join(L[2:2+n]) + chr(10)
m_p = Chem.MolFromXYZBlock(block)
rdDetermineBonds.DetermineBonds(m_p, charge=0)
p_el = [a.GetSymbol() for a in m_p.GetAtoms()]
print("P determined bonds:", m_p.GetNumBonds())
p_bonds = {}
for b in m_p.GetBonds():
    i, j = b.GetBeginAtomIdx(), b.GetEndAtomIdx()
    p_bonds[(min(i, j), max(i, j))] = str(b.GetBondType())

# ---- heavy-atom graphs ----
hv_s = [i for i, e in enumerate(el_s) if e != "H"]
hv_p = [i for i, e in enumerate(el_p) if e != "H"]
print("heavy atoms: seed", len(hv_s), "P", len(hv_p))
adj_s = {i: [] for i in hv_s}
for (i, j) in seed_bonds:
    if i in adj_s and j in adj_s:
        adj_s[i].append(j); adj_s[j].append(i)
adj_p = {i: [] for i in hv_p}
for (i, j) in p_bonds:
    if i in adj_p and j in adj_p:
        adj_p[i].append(j); adj_p[j].append(i)

# ---- enumerate heavy-atom isomorphisms (backtracking, element + degree constrained) ----
iso = []
def extend(mapping, used):
    if len(mapping) == len(hv_s):
        iso.append(dict(mapping)); return
    for a in hv_s:
        if a in mapping: continue
        for b in hv_p:
            if b in used: continue
            if el_s[a] != el_p[b]: continue
            if len(adj_s[a]) != len(adj_p[b]): continue
            ok = True
            for a2, b2 in mapping.items():
                es = (a2 in adj_s[a]); ep = (b2 in adj_p[b])
                if es != ep: ok = False; break
            if ok:
                mapping[a] = b; used.add(b)
                extend(mapping, used)
                del mapping[a]; used.discard(b)
extend({}, set())
print("heavy-atom isomorphism count:", len(iso))

def kabsch_rmsd(A, B):
    A = A - A.mean(0); B = B - B.mean(0)
    U, S, Vt = np.linalg.svd(A.T @ B)
    d = np.sign(np.linalg.det(U @ Vt))
    D = np.diag([1.0, 1.0, d])
    R = U @ D @ Vt
    Ar = A @ R
    return float(np.sqrt(((Ar - B) ** 2).sum() / len(A)))

# ---- add hydrogens: H belongs to its unique heavy parent ----
def h_candidates(mapping):
    hmap = {}
    for h_s, e in enumerate(el_s):
        if e != "H": continue
        ps = [j for (i, j) in seed_bonds if i == h_s] + [i for (i, j) in seed_bonds if j == h_s]
        ps = [x for x in ps if el_s[x] != "H"]
        if len(ps) != 1: return None, "H atom %d has %d heavy parents" % (h_s + 1, len(ps))
        pp = mapping[ps[0]]
        cands = [h_p for h_p in range(len(el_p)) if el_p[h_p] == "H" and ((min(h_p, pp), max(h_p, pp)) in p_bonds)]
        if len(cands) != 1: return None, "parent %d has %d H slots in P" % (pp + 1, len(cands))
        hmap[h_s] = cands[0]
    return hmap, ""

results = []
for k, hv in enumerate(iso):
    hm, err = h_candidates(hv)
    if hm is None:
        results.append({"idx": k, "error": err}); continue
    full = dict(hv); full.update(hm)
    if len(set(full.values())) != 41:
        results.append({"idx": k, "error": "not a bijection"}); continue
    order = [full[i] for i in range(41)]
    rms_heavy = kabsch_rmsd(X_s[hv_s], X_p[[full[i] for i in hv_s]])
    rms_all = kabsch_rmsd(X_s, X_p[order])
    # bond-table edge-by-edge consistency (heavy bonds, bond order inclusive)
    mism = []
    for (i, j), bo in seed_bonds.items():
        if el_s[i] == "H" or el_s[j] == "H": continue
        key = (min(full[i], full[j]), max(full[i], full[j]))
        if key not in p_bonds:
            mism.append((i + 1, j + 1, bo, "MISSING in P"))
        elif p_bonds[key] != bo:
            mism.append((i + 1, j + 1, bo, p_bonds[key]))
    fp = hashlib.md5(",".join(str(v + 1) for v in order).encode()).hexdigest()
    results.append({"idx": k, "order": order, "rms_heavy": rms_heavy, "rms_all": rms_all,
                    "mismatch": mism, "fp": fp})

good = [r for r in results if "order" in r]
print("complete mapped candidates:", len(good))
for r in sorted(good, key=lambda x: x["rms_heavy"])[:6]:
    print("  cand %2d heavy-Kabsch RMSD %.4f A | all-atom %.4f | bond-order mismatches %d | map MD5 %s"
          % (r["idx"], r["rms_heavy"], r["rms_all"], len(r["mismatch"]), r["fp"]))
good.sort(key=lambda x: x["rms_heavy"])
print("top-2 heavy-Kabsch RMSD: %.4f / %.4f A ; delta = %.4f A (n_complete = %d)"
      % (good[0]["rms_heavy"], good[1]["rms_heavy"] if len(good) > 1 else float("nan"),
         (good[1]["rms_heavy"] - good[0]["rms_heavy"]) if len(good) > 1 else float("nan"), len(good)))
best = min(good, key=lambda x: (len(x["mismatch"]), x["rms_heavy"]))
print("CHOSEN cand:", best["idx"], "heavy RMSD %.4f" % best["rms_heavy"], "MD5", best["fp"])
print("bond-order mismatch list:", best["mismatch"])
order = best["order"]
print("--- 41-row mapping (seed 1-based -> E3 working / P 1-based) ---")
for i in range(41):
    print("  seed %2d %-2s -> E3 %2d %-2s" % (i + 1, el_s[i], order[i] + 1, el_p[order[i]]))
print("--- hard check: neighbours of E3 atom 2 (C2) in P, and their seed partners ---")
nb_p = sorted([j for (i, j) in p_bonds if i == 1] + [i for (i, j) in p_bonds if j == 1])
print("P atom2 neighbours (1-based, element):", [(j + 1, el_p[j]) for j in nb_p])
inv = {v: k for k, v in enumerate(order)}
print("seed partners of those P atoms:", [(j + 1, el_p[j], inv[j] + 1, el_s[inv[j]]) for j in nb_p])
print("candidate hypothesis check: seed N32 -> E3", inv.get(31, None) + 1 if 31 in inv else None)
for lbl, sidx in [("N32", 31), ("O27", 26), ("H33", 32), ("O6", 5), ("H19", 18)]:
    print("  %s (seed %d) -> E3 %s ; element %s" % (lbl, sidx + 1, inv[sidx] + 1, el_p[order[sidx]]))
# --- key-bond two-column check (E3 working labels, 1-based) ---
print("--- 5 key bonds: seed-side vs P-side (E3 1-based labels) ---")
KEY = [("C2-N4", 2, 4), ("C2-O25", 2, 25), ("N4-H26", 4, 26), ("O25-H26", 25, 26), ("O10-H27", 10, 27)]
kb = []
for name, a, b in KEY:
    ia, ib = inv[a - 1], inv[b - 1]          # seed 0-based indices
    ds = float(np.linalg.norm(X_s[ia] - X_s[ib]))
    dp = float(np.linalg.norm(X_p[a - 1] - X_p[b - 1]))
    kb.append({"bond": name, "seed_atoms_1based": [ia + 1, ib + 1], "seed_A": round(ds, 4),
               "e3_atoms_1based": [a, b], "P_A": round(dp, 4), "delta": round(ds - dp, 4)})
    print("  %-8s seed(%2d,%2d) = %.4f A | P(%2d,%2d) = %.4f A | seed - P = %+.4f A"
          % (name, ia + 1, ib + 1, ds, a, b, dp, ds - dp))
judge = [k for k in kb if k["bond"] == "N4-H26"][0]["seed_A"] < 1.4 and [k for k in kb if k["bond"] == "O25-H26"][0]["seed_A"] > 2.2
print("VERDICT seed bond-table already product-side (N4-H26 ~1.0 and O25-H26 ~3):", judge)
np.save("/tmp/seed_to_P_order.npy", np.array(order))
json_out = {"rms_heavy": best["rms_heavy"], "rms_all": best["rms_all"], "md5": best["fp"],
            "order_seed_to_P_1based": [v + 1 for v in order], "bond_mismatch": best["mismatch"],
            "n_iso_heavy": len(iso), "n_complete": len(good), "key_bonds": kb,
            "element_order_identical": el_s == el_p, "seed_product_side": bool(judge),
            "rmsd_top2_delta": (good[1]["rms_heavy"] - good[0]["rms_heavy"]) if len(good) > 1 else None,
            "alts": [{"idx": r["idx"], "rms_heavy": round(r["rms_heavy"], 4), "md5": r["fp"]} for r in sorted(good, key=lambda x: x["rms_heavy"])]}
open("/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/prep/seed_to_P_mapping.json", "w").write(__import__("json").dumps(json_out, indent=2, ensure_ascii=False))
print("wrote prep/seed_to_P_mapping.json")
