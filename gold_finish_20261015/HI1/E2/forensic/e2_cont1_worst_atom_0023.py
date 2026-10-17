#!/usr/bin/env python3
"""Read-only: adjacent-pair Kabsch with BOTH atom sets (heavy20 and all-41),
and explicit worst-atom index (1-based file order) per pair. Reuses the exact
conventions of forensic/e2_cont1_table.py (SVD, C=Q^T P, Qp=Q R^T, det(R)=+1)."""
import os, sys, datetime
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import e2_cont1_table as T

Lc, shac, bc = T.read(T.CONT1)
bl = T.blocks(Lc)
fr = T.conv_frames(Lc, bl, "cont1")
heavy = [i for i in sorted(fr[0]["co"]) if fr[0]["co"][i][0] != 1]
allat = sorted(fr[0]["co"])
print("# snapshot", datetime.datetime.now().astimezone().isoformat(timespec="seconds"))
print("# cont1 log:", T.CONT1)
print(f"#   lines={len(Lc)} bytes={bc} sha256={shac}")
print(f"# frames={len(fr)} oc={[f['oc'] for f in fr]}")
print(f"# heavy={len(heavy)} all={len(allat)}")

def kab_idx(A, B, idx):
    P = np.array([A[i][1:] for i in idx]); Q = np.array([B[i][1:] for i in idx])
    Pm = P - P.mean(0); Qm = Q - Q.mean(0)
    C = Qm.T @ Pm
    U, S, Vt = np.linalg.svd(C)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1.0, 1.0, d]) @ U.T
    Qp = Qm @ R.T
    dist = np.linalg.norm(Pm - Qp, axis=1)
    w = int(np.argmax(dist))
    return float(np.sqrt((dist ** 2).mean())), float(dist.max()), float(d), idx[w], list(np.round(dist, 4))

for a, b in zip(fr, fr[1:]):
    r, m, d, wat, dd = kab_idx(a["co"], b["co"], heavy)
    R2, M2, D2, wa2, dd2 = kab_idx(a["co"], b["co"], allat)
    print(f"pt{fr.index(a)+1}->pt{fr.index(b)+1}  heavy20 rms={r:.4f} max={m:.4f} det={d:+.6f} worst_atom={wat} "
          f"| all41 rms={R2:.4f} max={M2:.4f} det={D2:+.6f} worst_atom={wa2}")
    print(f"    heavy20 top5 devs (atom, A): " + ", ".join(f"{heavy[i]}={v}" for i, v in sorted(enumerate(dd), key=lambda t: -t[1])[:5]))
    print(f"    all41   top5 devs (atom, A): " + ", ".join(f"{allat[i]}={v}" for i, v in sorted(enumerate(dd2), key=lambda t: -t[1])[:5]))

# synthetic self-checks (same as e2_kabsch_verify.py conventions)
rng = np.random.default_rng(7)
P = rng.normal(size=(20, 3))
th = 0.7
Rz = np.array([[np.cos(th), -np.sin(th), 0], [np.sin(th), np.cos(th), 0], [0, 0, 1]])
Q = P @ Rz.T + np.array([1.5, -2.0, 0.25])
A = {i + 1: (6, *P[i]) for i in range(20)}
B = {i + 1: (6, *Q[i]) for i in range(20)}
idx = list(range(1, 21))
print("SC(i) rot+trans -> 0 :", f"{kab_idx(A, B, idx)[0]:.3e}")
M = {i + 1: (6, P[i][0], P[i][1], -P[i][2]) for i in range(20)}
print("SC(ii) mirror(allowed-refit, det forced +1) :", f"{kab_idx(A, M, idx)[1]:.6f}")
print("SC(iii) identical copy -> 0 :", f"{kab_idx(A, dict(A), idx)[0]:.3e}")
