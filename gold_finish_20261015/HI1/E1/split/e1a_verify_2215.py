#!/usr/bin/env python3
"""Read-only audit of E1a scan log: 11 converged points (energies) + sp4->sp5
Kabsch RMSD on heavy-atom subset and all atoms. numpy SVD, det=+1 forced.
Includes 3 synthetic self-checks. No writes."""
import numpy as np
LOG = "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split/E1A_constrained_scan_R2692_2192_stepneg.log"
lines = open(LOG, "r", errors="replace").read().splitlines()

def geom_before(ci):
    hdr = None
    for j in range(ci, -1, -1):
        if "Standard orientation:" in lines[j]:
            hdr = j
            break
    atoms = []
    k = hdr + 5
    while k < len(lines) and not lines[k].strip().startswith("---"):
        p = lines[k].split()
        if len(p) >= 6 and p[0].isdigit():
            atoms.append((int(p[1]), float(p[3]), float(p[4]), float(p[5])))
        k += 1
    return hdr + 1, atoms

def scf_before(ci):
    for j in range(ci, -1, -1):
        if "SCF Done:" in lines[j]:
            return j + 1, float(lines[j].split("=")[1].split()[0])
    return None, None

conv = [i for i, L in enumerate(lines) if "Optimization completed." in L]
recs = []
for ci in conv:
    sl, E = scf_before(ci)
    hdr, atoms = geom_before(ci)
    recs.append((ci + 1, sl, E, hdr, atoms))
H = 627.509474
print("n_conv=%d  NAtoms=%d" % (len(recs), len(recs[0][4])))
ZSYM = {1: "H", 6: "C", 7: "N", 8: "O"}
seq = "".join(ZSYM.get(a[0], "?") for a in recs[0][4])
print("element_seq=%s" % seq)
heavy = [i + 1 for i, a in enumerate(recs[0][4]) if a[0] != 1]
print("heavy_workorder=%s (n=%d)" % (heavy, len(heavy)))
e0 = recs[0][2]
print("pt | scfLine | E(H) | dE_vs_pt1_kcal | geomHdr")
for n, (cl, sl, E, hdr, atoms) in enumerate(recs, 1):
    print("%2d | %6d | %.9f | %+7.2f | %d" % (n, sl, E, (E - e0) * H, hdr))

def kabsch_rmsd(A, B):
    A = np.asarray(A, float); B = np.asarray(B, float)
    Ac = A - A.mean(0); Bc = B - B.mean(0)
    V, S, Wt = np.linalg.svd(Bc.T @ Ac)
    d = np.sign(np.linalg.det(V @ Wt))
    D = np.diag([1.0, 1.0, d])
    R = V @ D @ Wt
    rot = (R @ Bc.T).T
    dd = np.linalg.norm(rot - Ac, axis=1)
    return float(np.sqrt((dd ** 2).sum() / len(A))), float(dd.max()), dd

# synthetic self-checks
rng = np.random.default_rng(7)
P = rng.normal(size=(12, 3))
Q = rng.normal(size=(3, 3)); U, _, Vt = np.linalg.svd(Q); Q = U @ Vt
if np.linalg.det(Q) < 0: Q = U @ np.diag([1, 1, -1]) @ Vt
print("SELF-CHECK known rot+trans RMSD = %.3e (expect ~0)" % kabsch_rmsd(P @ Q.T + np.array([3.0, -2.0, 5.0]), P)[0])
M = P.copy(); M[:, 2] *= -1.0
print("SELF-CHECK mirror RMSD = %.6f (expect >0)" % kabsch_rmsd(M, P)[0])
print("SELF-CHECK copy RMSD = %.3e (expect ~0)" % kabsch_rmsd(P.copy(), P)[0])

_, _, _, _, g4 = recs[3]
_, _, _, _, g5 = recs[4]
assert len(g4) == len(g5)
A4 = [a[1:] for a in g4]; A5 = [a[1:] for a in g5]
hi = [i - 1 for i in heavy]
allidx = list(range(len(A4)))
for label, idx in (("heavy_%d" % len(hi), hi), ("all_%d" % len(allidx), allidx)):
    r, mx, dd = kabsch_rmsd([A4[i] for i in idx], [A5[i] for i in idx])
    worst = max(range(len(idx)), key=lambda t: dd[t])
    print("sp4->sp5 %s: RMSD=%.4f maxdisp=%.4f worst_atom_workorder=%d"
          % (label, r, mx, idx[worst] + 1))
