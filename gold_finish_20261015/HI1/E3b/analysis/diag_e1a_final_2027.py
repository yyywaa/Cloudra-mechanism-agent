import re, sys, math
import numpy as np
path = sys.argv[1]
L = open(path, errors="replace").read().splitlines()
RC = -593.934532807; H = 627.509474
def grab_frame(end):
    j = end
    while j > 0 and "Input orientation" not in L[j]:
        j -= 1
    start = j + 5; at = []
    while start < len(L) and len(at) < 60:
        p = L[start].split()
        if len(p) != 6 or not p[0].isdigit(): break
        at.append((int(p[0]), int(p[1]), float(p[3]), float(p[4]), float(p[5])))
        start += 1
    return at
def d(a, b): return math.dist(a[2:], b[2:])
marks = [i for i, l in enumerate(L) if "Optimization completed." in l]
print("Optimization completed count:", len(marks))
frames = []
for k, i in enumerate(marks, 1):
    e = None
    for j in range(i, max(0, i - 3000), -1):
        m = re.search(r"SCF Done:\s+E\(RB3LYP\)\s+=\s+(-?\d+\.\d+)", L[j])
        if m: e = float(m.group(1)); break
    rscan = None
    for j in range(i, max(0, i - 200), -1):
        m = re.search(r"R7\s+R\(2,18\)\s+(-?\d+\.\d+)\s+-DE/DX", L[j])
        if m: rscan = float(m.group(1)); break
    at = grab_frame(i); frames.append(at)
    A = {a[0]: a for a in at}
    print("pt%-2d L%-6d E=%.9f R(2,18)=%.4f R(2,3)=%.4f R(18,27)=%.4f minsep=%.4f dE=%+.2f" % (
        k, i+1, e, d(A[2], A[18]), d(A[2], A[3]), d(A[18], A[27]),
        min(d(x, y) for a, x in enumerate(at) for y in at[a+1:]), (e - RC) * H))
def kabsch(A, B):
    a = np.array([x[2:] for x in A]); b = np.array([x[2:] for x in B])
    a -= a.mean(0); b -= b.mean(0); Hm = a.T @ b
    U, S, Vt = np.linalg.svd(Hm)
    dsign = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1, 1, dsign]) @ U.T
    ar = (R @ a.T).T
    return float(np.sqrt(((ar - b) ** 2).sum(1).mean()))
print("adjacent Kabsch RMSD:")
for k in range(1, len(frames)):
    print("  pt%d->pt%d %.3f A" % (k, k+1, kabsch(frames[k-1], frames[k])))
