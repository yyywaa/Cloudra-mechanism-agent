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
marks = [i for i, l in enumerate(L) if "Optimization completed" in l]
frames = []
print("markers:", len(marks))
for i in marks:
    # scan point number from nearest preceding 'on scan point N out of'
    sp = None
    for j in range(i, max(0, i - 60), -1):
        m = re.search(r"on scan point\s+(\d+) out of", L[j])
        if m: sp = int(m.group(1)); break
    e = None
    for j in range(i, max(0, i - 3000), -1):
        m = re.search(r"SCF Done:\s+E\(RB3LYP\)\s+=\s+(-?\d+\.\d+)", L[j])
        if m: e = float(m.group(1)); break
    kind = "completed" if L[i].strip().endswith("completed.") else "negligible-forces"
    at = grab_frame(i); frames.append(at)
    A = {a[0]: a for a in at}
    if sp is None:
        sp = int(round((2.6920 - d(A[2], A[18])) / 0.05)) + 1
    print("sp%-2d L%-6d %-17s E=%.9f R(2,18)=%.4f R(2,3)=%.4f R(18,27)=%.4f minsep=%.4f dE=%+.2f" % (
        sp, i+1, kind, e, d(A[2], A[18]), d(A[2], A[3]), d(A[18], A[27]),
        min(d(x, y) for a_, x in enumerate(at) for y in at[a_+1:]), (e - RC) * H))
def kabsch(A, B):
    a = np.array([x[2:] for x in A]); b = np.array([x[2:] for x in B])
    a -= a.mean(0); b -= b.mean(0)
    U, S, Vt = np.linalg.svd(a.T @ b)
    dsign = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1, 1, dsign]) @ U.T
    ar = (R @ a.T).T
    return float(np.sqrt(((ar - b) ** 2).sum(1).mean()))
print("adjacent Kabsch RMSD:")
for k in range(1, len(frames)):
    r = kabsch(frames[k-1], frames[k])
    print("  %d->%d %.3f A %s" % (k, k+1, r, "<== JUMP" if r > 0.3 else ""))
print("dE vs R(2,18)  (monotonic check, excluding jump):")
