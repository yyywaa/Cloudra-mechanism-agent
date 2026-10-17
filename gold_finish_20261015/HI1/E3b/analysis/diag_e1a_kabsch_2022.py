import re, sys, math
import numpy as np
path = sys.argv[1]
L = open(path, errors="replace").read().splitlines()
frames = []
for i, l in enumerate(L):
    if "Optimization completed." in l:
        j = i
        while j > 0 and "Input orientation" not in L[j]:
            j -= 1
        start = j + 5
        at = []
        while start < len(L) and len(at) < 60:
            p = L[start].split()
            if len(p) != 6 or not p[0].isdigit(): break
            at.append((int(p[0]), int(p[1]), float(p[3]), float(p[4]), float(p[5])))
            start += 1
        frames.append((i+1, at))
def kabsch(A, B):
    a = np.array([x[2:] for x in A]); b = np.array([x[2:] for x in B])
    a -= a.mean(0); b -= b.mean(0)
    H = a.T @ b
    U, S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    D = np.diag([1, 1, d])
    R = Vt.T @ D @ U.T
    ar = (R @ a.T).T
    return float(np.sqrt(((ar - b) ** 2).sum(1).mean())), [float(np.linalg.norm(x)) for x in (ar - b)]
print("frames", len(frames))
for k in range(1, len(frames)):
    r, per = kabsch(frames[k-1][1], frames[k][1])
    print("pt%d->pt%d  Kabsch RMSD %.3f A  max per-atom %.3f (atom %d)" % (k, k+1, r, max(per), 1 + per.index(max(per))))
