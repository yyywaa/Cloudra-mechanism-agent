# -*- coding: utf-8 -*-
# v4: per-isomorphism discrimination report for seed -> P (E3 working order) mapping.
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
    L = open(p).read().splitlines(); n = int(L[0]); rows = [l.split() for l in L[2:2+n]]
    return [r[0] for r in rows], np.array([[float(r[1]), float(r[2]), float(r[3])] for r in rows])
el_s, X_s = load_xyz(SEED_XYZ); el_p, X_p = load_xyz(P_XYZ)
m_s = Chem.MolFromMolFile(SEED_MOL, removeHs=False, sanitize=False)
seed_bonds = {(min(b.GetBeginAtomIdx(), b.GetEndAtomIdx()), max(b.GetBeginAtomIdx(), b.GetEndAtomIdx())): str(b.GetBondType()) for b in m_s.GetBonds()}
L = open(P_XYZ).read().splitlines(); n = int(L[0])
m_p = Chem.MolFromXYZBlock(str(n) + chr(10) + P_XYZ + chr(10) + chr(10).join(L[2:2+n]) + chr(10))
rdDetermineBonds.DetermineBonds(m_p, charge=0)
p_bonds = {(min(b.GetBeginAtomIdx(), b.GetEndAtomIdx()), max(b.GetBeginAtomIdx(), b.GetEndAtomIdx())): str(b.GetBondType()) for b in m_p.GetBonds()}
hv_s = [i for i, e in enumerate(el_s) if e != "H"]; hv_p = [i for i, e in enumerate(el_p) if e != "H"]
pos_s = {a: k for k, a in enumerate(hv_s)}; pos_p = {a: k for k, a in enumerate(hv_p)}
rw_s = Chem.RWMol(); [rw_s.AddAtom(Chem.Atom(el_s[i])) for i in hv_s]
for (i, j) in seed_bonds:
    if i in pos_s and j in pos_s: rw_s.AddBond(pos_s[i], pos_s[j], Chem.BondType.SINGLE)
rw_p = Chem.RWMol(); [rw_p.AddAtom(Chem.Atom(el_p[i])) for i in hv_p]
for (i, j) in p_bonds:
    if i in pos_p and j in pos_p: rw_p.AddBond(pos_p[i], pos_p[j], Chem.BondType.SINGLE)
q = rw_s.GetMol(); tgt = rw_p.GetMol(); Chem.SanitizeMol(q); Chem.SanitizeMol(tgt)
matches = tgt.GetSubstructMatches(q, uniquify=False, maxMatches=100000)

def kabsch(A, B):
    A = A - A.mean(0); B = B - B.mean(0)
    U, S, Vt = np.linalg.svd(A.T @ B)
    d = np.sign(np.linalg.det(U @ Vt)); R = U @ np.diag([1.0, 1.0, d]) @ Vt
    return float(np.sqrt((((A @ R) - B) ** 2).sum() / len(A)))
seed_h = {}
for h in range(len(el_s)):
    if el_s[h] == "H":
        par = [x for (i, j) in seed_bonds if h in (i, j) for x in (i, j) if el_s[x] != "H"]
        seed_h.setdefault(par[0], []).append(h)
KEY = [("C2-N4", 2, 4), ("C2-O25", 2, 25), ("N4-H26", 4, 26), ("O25-H26", 25, 26), ("O10-H27", 10, 27)]
ART = {("DOUBLE", "AROMATIC"), ("SINGLE", "AROMATIC"), ("AROMATIC", "DOUBLE"), ("AROMATIC", "SINGLE")}
rows = []
for k, mt in enumerate(matches):
    heavy_map = {hv_s[a]: hv_p[mt[a]] for a in range(len(hv_s))}
    groups = []; ok = True
    for ps in sorted(seed_h):
        pp = heavy_map[ps]
        t = [hp for hp in range(len(el_p)) if el_p[hp] == "H" and (min(hp, pp), max(hp, pp)) in p_bonds]
        if len(t) != len(seed_h[ps]): ok = False; break
        groups.append((seed_h[ps], sorted(t)))
    if not ok:
        rows.append({"iso": k, "complete": False, "reason": "H-slot count mismatch for some parent"}); continue
    best = None
    for choice in product(*[list(permutations(t)) for (s, t) in groups]):
        full = dict(heavy_map)
        for (s, t), pm in zip(groups, choice):
            for h, hp in zip(s, pm): full[h] = hp
        order = [full[i] for i in range(41)]
        r_all = kabsch(X_s, X_p[order]); r_hv = kabsch(X_s[hv_s], X_p[[full[i] for i in hv_s]])
        mism = []
        for (i, j), bo in seed_bonds.items():
            if el_s[i] == "H" or el_s[j] == "H": continue
            key = (min(full[i], full[j]), max(full[i], full[j]))
            if key not in p_bonds: mism.append([i + 1, j + 1, bo, "MISSING"])
            elif p_bonds[key] != bo: mism.append([i + 1, j + 1, bo, p_bonds[key]])
        real = [x for x in mism if (x[2], x[3]) not in ART]
        rec = {"order": order, "rms_all": r_all, "rms_hv": r_hv, "n_mism": len(mism), "n_real": len(real),
               "real": real, "fp": hashlib.md5(",".join(str(v + 1) for v in order).encode()).hexdigest()}
        if best is None or (rec["n_real"], rec["rms_hv"]) < (best["n_real"], best["rms_hv"]): best = rec
    inv = {v: s for s, v in enumerate(best["order"])}
    kb = []
    for name, a, b in KEY:
        ia, ib = inv[a - 1], inv[b - 1]
        kb.append((name, ia + 1, ib + 1, round(float(np.linalg.norm(X_s[ia] - X_s[ib])), 4), round(float(np.linalg.norm(X_p[a - 1] - X_p[b - 1])), 4)))
    rows.append({"iso": k, "complete": True, "rms_hv": round(best["rms_hv"], 4), "rms_all": round(best["rms_all"], 4),
                 "n_mism": best["n_mism"], "n_real": best["n_real"], "real": best["real"], "fp": best["fp"],
                 "key": kb, "order": [v + 1 for v in best["order"]]})
    print("iso %d COMPLETE | heavy-Kabsch %.4f A | all-atom %.4f A | mismatch rows %d (non-aromatic %d) | MD5 %s"
          % (k, best["rms_hv"], best["rms_all"], best["n_mism"], best["n_real"], best["fp"]))
    print("   non-aromatic mismatches:", best["real"])
    print("   key bonds (name, seed_i, seed_j, seed_A, P_A):", kb)
for r in rows:
    if not r.get("complete"): print("iso %d INCOMPLETE | %s" % (r["iso"], r["reason"]))
compl = [r for r in rows if r.get("complete")]
compl.sort(key=lambda x: (x["n_real"], x["rms_hv"]))
print("ranking key = (non-aromatic mismatches, heavy RMSD):")
for r in compl: print("   iso %d -> (%d, %.4f A)" % (r["iso"], r["n_real"], r["rms_hv"]))
print("top-2 heavy RMSD delta = %.4f A" % (compl[1]["rms_hv"] - compl[0]["rms_hv"]) if len(compl) > 1 else "single complete iso")
chosen = compl[0]
open(BASE + "gold_finish_20261015/HI1/E3/prep/seed_to_P_mapping_v4.json", "w").write(json.dumps({"chosen_iso": chosen["iso"], "rows": rows}, indent=2, ensure_ascii=False))
print("CHOSEN iso", chosen["iso"], "MD5", chosen["fp"], "order(seed->E3 1-based):", chosen["order"])
print("wrote prep/seed_to_P_mapping_v4.json")
