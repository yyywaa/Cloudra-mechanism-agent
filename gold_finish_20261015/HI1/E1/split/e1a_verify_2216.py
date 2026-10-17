#!/usr/bin/env python3
"""Read-only audit of E1a scan log, v2: fixed row-vector Kabsch (R = U D Vt from
svd(Bc^T Ac)), 3 synthetic self-checks, converged-point count with both spellings."""
import numpy as np
LOG = "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split/E1A_constrained_scan_R2692_2192_stepneg.log"
lines = open(LOG, "r", errors="replace").read().splitlines()

def geom_before(ci):
    hdr = None
    for j in range(ci, -1, -1):
        if "Standard orientation:" in lines[j]:
            hdr = j
            break
    atoms = []; k = hdr + 5
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

conv = [i for i, L in enumerate(lines) if "Optimization completed" in L]
convP = [i for i, L in enumerate(lines) if "Optimization completed." in L]
print("count_with_period=%d  count_no_dot_constraint=%d  lines=%s"
      % (len(convP), len(conv), [c + 1 for c in conv]))
recs = []
for ci in conv:
    sl, E = scf_before(ci); hdr, atoms = geom_before(ci)
    recs.append((ci + 1, sl, E, hdr, atoms))
H = 627.509474
e0 = recs[0][2]
print("NAtoms=%d" % len(recs[0][4]))
print("pt | convLine | scfLine | E(H) | dE_vs_pt1_kcal | geomHdr")
for n, (cl, sl, E, hdr, atoms) in enumerate(recs, 1):
    print("%2d | %6d | %6d | %.9f | %+7.2f | %d" % (n, cl, sl, E, (E - e0) * H, hdr))

def kabsch(A, B):
    A = np.asarray(A, float); B = np.asarray(B, float)
    Ac = A - A.mean(0); Bc = B - B.mean(0)
    U, S, Vt = np.linalg.svd(Bc.T @ Ac)
    d = np.sign(np.linalg.det(U @ Vt))
    D = np.diag([1.0, 1.0, d])
    R = U @ D @ Vt
    rot = Bc @ R
    dd = np.linalg.norm(rot - Ac, axis=1)
    return float(np.sqrt((dd ** 2).sum() / len(A))), float(dd.max()), dd

rng = np.random.default_rng(7)
P = rng.normal(size=(12, 3))
Q, _, Vt2 = np.linalg.svd(rng.normal(size=(3, 3))); Q = Q @ Vt2
if np.linalg.det(Q) < 0: Q = Q @ np.diag([1, 1, -1])
print("SELF-CHECK rot+trans RMSD = %.3e (expect ~0)" % kabsch(P @ Q.T + np.array([3.0, -2.0, 5.0]), P)[0])
Mm = P.copy(); Mm[:, 2] *= -1.0
print("SELF-CHECK mirror RMSD = %.6f (expect >0)" % kabsch(Mm, P)[0])
print("SELF-CHECK copy RMSD = %.3e (expect ~0)" % kabsch(P.copy(), P)[0])

heavy = [i for i, a in enumerate(recs[0][4]) if a[0] != 1]
print("heavy_workorder=%s" % [i + 1 for i in heavy])
for a, b, tag in ((3, 4, "sp4->sp5"), (0, 1, "sp1->sp2"), (1, 2, "sp2->sp3"), (2, 3, "sp3->sp4")):
    A4 = [x[1:] for x in recs[a][4]]; A5 = [x[1:] for x in recs[b][4]]
    for label, idx in (("heavy12", heavy), ("all27", list(range(len(A4))))):
        r, mx, dd = kabsch([A4[i] for i in idx], [A5[i] for i in idx])
        w = max(range(len(idx)), key=lambda t: dd[t])
        print("%s %s: RMSD=%.4f maxdisp=%.4f worst_workorder=%d" % (tag, label, r, mx, idx[w] + 1))
