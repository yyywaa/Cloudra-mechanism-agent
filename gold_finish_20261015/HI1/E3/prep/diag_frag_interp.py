#!/usr/bin/env python3
"""Rigid-fragment interpolation diagnostic for the E3b guess (read-only, writes nothing).

The all-atom Cartesian interpolation (v3/v4) collapses intra-fragment bond lengths when the
two endpoints are different conformers (the converged P from job 1061 is ~1.94 A whole-molecule
Kabsch RMSD away from the hemiaminal minimum). This tool interpolates each FRAGMENT rigidly:

  * per-fragment Kabsch superposition hemiaminal -> converged P,
  * the rotation is interpolated along its axis-angle geodesic, the centroid linearly,
  * therefore every INTRA-fragment distance stays exactly at its hemiaminal value and only the
    inter-fragment contacts change with lambda,
  * H26 is carried on N4 at 1.05 A along unit(N4 - C2) (the approved v3 proton placement).

Usage: diag_frag_interp.py HEMI.xyz P.xyz
"""
import sys, math
import numpy as np

FRAG_1 = [1, 2, 3, 12, 13, 14, 15, 16, 24, 25, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41]
FRAG_2 = [4, 5, 6, 7, 8, 9, 10, 11, 17, 18, 19, 20, 21, 22, 23, 26, 27]


def rd(p):
    L = open(p).read().splitlines()
    n = int(L[0].split()[0])
    return [x.split()[0] for x in L[2:2 + n]], np.array([[float(v) for v in x.split()[1:4]] for x in L[2:2 + n]])


def kabsch(A, B):
    """rotation R and translation t with  R @ A.T + t  ~=  B.T (row-vector coordinates)."""
    cA, cB = A.mean(axis=0), B.mean(axis=0)
    H = (A - cA).T @ (B - cB)
    U, S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1.0, 1.0, d]) @ U.T
    return R, cA, cB


def axis_angle(R):
    c = max(-1.0, min(1.0, (np.trace(R) - 1.0) / 2.0))
    th = math.acos(c)
    if th < 1e-9:
        return np.array([1.0, 0.0, 0.0]), 0.0
    ax = np.array([R[2, 1] - R[1, 2], R[0, 2] - R[2, 0], R[1, 0] - R[0, 1]]) / (2.0 * math.sin(th))
    return ax / np.linalg.norm(ax), th


def rodrigues(ax, th):
    K = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]])
    return np.eye(3) + math.sin(th) * K + (1 - math.cos(th)) * (K @ K)


def rigid_lerp(R0, c0, R1, c1, lam):
    ax, th = axis_angle(R0.T @ R1)
    Rl = R0 @ rodrigues(ax, lam * th)
    return Rl, c0 + lam * (c1 - c0)


def d(X, i, j):
    return float(np.linalg.norm(X[i - 1] - X[j - 1]))


el, H = rd(sys.argv[1])
elP, Pc = rd(sys.argv[2])
assert (el == elP) and len(el) == 41, "endpoints must be 41 atoms with identical element order"

frags = [FRAG_1, FRAG_2]
srcs = []
for f in frags:
    idx = [i - 1 for i in f]
    R, cH, cP = kabsch(H[idx], Pc[idx])
    ax, th = axis_angle(R)
    srcs.append((ax, th, cH, cP))

print("endpoint comparison")
for f in frags:
    idx = [i - 1 for i in f]
    R, cH, cP = kabsch(H[idx], Pc[idx])
    res = (H[idx] - cH) @ R.T + cP
    print("  frag atoms %d: per-fragment Kabsch RMSD = %.4f A" % (
        len(f), float(np.sqrt(((res - Pc[idx]) ** 2).sum() / len(f)))))

print("\nlam  R(2,4)  R(2,25) R(25,26) R(2,26)  minsep(pair)   intra_ok  heavy_min(pair)  contacts<1.20")
for k in range(20, 96, 5):
    lam = k / 100.0
    X = np.zeros_like(H)
    for f, (ax, th, cH, cP) in zip(frags, srcs):
        Rl = rodrigues(ax, lam * th)
        cl = cH + lam * (cP - cH)
        idx = [i - 1 for i in f]
        X[idx] = (H[idx] - cH) @ Rl.T + cl
    # proton H26 on N4, 1.05 A, direction unit(N4 - C2)
    u = X[3] - X[1]
    u = u / np.linalg.norm(u)
    X[25] = X[3] + 1.05 * u
    best = (9e9, 0, 0); bh = (9e9, 0, 0); bad = []
    n = len(el)
    for i in range(n):
        for j in range(i + 1, n):
            dd = float(np.linalg.norm(X[i] - X[j]))
            if dd < best[0]:
                best = (dd, i + 1, j + 1)
            if el[i] != "H" and el[j] != "H" and dd < bh[0]:
                bh = (dd, i + 1, j + 1)
            if dd < 1.20:
                bad.append("%d-%d:%.2f" % (i + 1, j + 1, dd))
    # intra-fragment sanity: largest deviation from hemiaminal bond-length set
    dm = 0.0
    for f in frags:
        for a in range(len(f)):
            for b in range(a + 1, len(f)):
                dm = max(dm, abs(d(X, f[a], f[b]) - d(H, f[a], f[b])))
    print("%.2f %8.4f %7.4f %7.4f %7.4f  %.4f(%d-%d)   %.2e   %.4f(%d-%d)   %s" % (
        lam, d(X, 2, 4), d(X, 2, 25), d(X, 25, 26), d(X, 2, 26), best[0], best[1], best[2],
        dm, bh[0], bh[1], bh[2], " ".join(bad[:6]) if bad else "-"))
