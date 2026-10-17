#!/usr/bin/env python3
"""Read-only: independent heavy-20 Kabsch for consecutive converged points of the
E2 1D scan (job 1075). SVD, det=+1, R acts previous->next. 3 synthetic self-checks."""
import numpy as np
LOG = "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan.log"
lines = open(LOG, "r", errors="replace").read().splitlines()

def geom_before(ci):
    hdr = None
    for j in range(ci, -1, -1):
        if "Standard orientation:" in lines[j]:
            hdr = j; break
    atoms = []; k = hdr + 5
    while k < len(lines) and not lines[k].strip().startswith("---"):
        p = lines[k].split()
        if len(p) >= 6 and p[0].isdigit():
            atoms.append((int(p[1]), float(p[3]), float(p[4]), float(p[5])))
        k += 1
    return hdr + 1, atoms

conv = [i for i, L in enumerate(lines) if "Optimization completed." in L]
P = []
for ci in conv:
    h, a = geom_before(ci)
    P.append((h, a))
heavy = [i for i, x in enumerate(P[0][1]) if x[0] != 1]
print("n_conv=%d NAtoms=%d heavy=%d" % (len(P), len(P[0][1]), len(heavy)))

def kabsch(A, B):
    A = np.asarray(A, float); B = np.asarray(B, float)
    Ac = A - A.mean(0); Bc = B - B.mean(0)
    U, S, Vt = np.linalg.svd(Bc.T @ Ac)
    d = np.sign(np.linalg.det(U @ Vt))
    R = U @ np.diag([1.0, 1.0, d]) @ Vt
    dd = np.linalg.norm(Bc @ R - Ac, axis=1)
    return float(np.sqrt((dd ** 2).sum() / len(A))), float(dd.max())

rng = np.random.default_rng(11)
X = rng.normal(size=(20, 3))
Q, _, Vt2 = np.linalg.svd(rng.normal(size=(3, 3))); Q = Q @ Vt2
if np.linalg.det(Q) < 0: Q = Q @ np.diag([1, 1, -1])
print("SELF rot+trans  = %.3e (expect ~0)" % kabsch(X @ Q.T + np.array([1.0, 2.0, -3.0]), X)[0])
Xm = X.copy(); Xm[:, 0] *= -1
print("SELF mirror     = %.6f (expect >0)" % kabsch(Xm, X)[0])
print("SELF copy       = %.3e (expect ~0)" % kabsch(X.copy(), X)[0])

print("pair | hdrA | hdrB | heavy20_RMSD | maxdisp | all41_RMSD")
for n in range(len(P) - 1):
    A = [x[1:] for x in P[n][1]]; B = [x[1:] for x in P[n + 1][1]]
    r, mx = kabsch([A[i] for i in heavy], [B[i] for i in heavy])
    ra, _ = kabsch(A, B)
    print("%d->%d | %d | %d | %.4f | %.4f | %.4f" % (n + 1, n + 2, P[n][0], P[n + 1][0], r, mx, ra))
