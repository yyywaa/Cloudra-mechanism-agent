#!/usr/bin/env python3
"""Read-only Kabsch-convention battery for the HI1 E2 1D scan (needed because the
frozen 0.3 A branch-switch guard is sensitive to the RMSD definition used).
Prints several explicitly-labelled conventions for each consecutive point pair;
writes nothing. Usage: python3 diag_kabsch_variants.py <log>
"""
import sys, math, datetime, hashlib
import numpy as np

ELEM = {1:"H",2:"He",3:"Li",4:"Be",5:"B",6:"C",7:"N",8:"O",9:"F",10:"Ne"}
MASS = {"H":1.008,"C":12.011,"N":14.007,"O":15.999}

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()

log = sys.argv[1]
lines = open(log, "r", errors="replace").read().split("\n")
oc = [i for i, ln in enumerate(lines) if ln.strip() == "Optimization completed."]
so = [i for i, ln in enumerate(lines) if "Standard orientation:" in ln]

def parse(start):
    i = start + 1
    while i < len(lines) and not lines[i].strip().startswith("---"):
        i += 1
    i += 1
    while i < len(lines) and not lines[i].strip().startswith("---"):
        i += 1
    i += 1
    a = []
    while i < len(lines) and not lines[i].strip().startswith("---"):
        t = lines[i].split()
        if len(t) >= 6:
            a.append((ELEM.get(int(t[1]), "X"), np.array([float(t[3]), float(t[4]), float(t[5])])))
        i += 1
    return a

frames = []
for k, o in enumerate(oc):
    prev = oc[k - 1] if k > 0 else -1
    s = [x for x in so if prev < x < o]
    frames.append((k + 1, parse(s[-1])))

elems = [a[0] for a in frames[0][1]]
n = len(elems)
heavy = [i for i, e in enumerate(elems) if e != "H"]

def kabsch_R(A, B, improper=False):
    Ac = A - A.mean(0); Bc = B - B.mean(0)
    U, S, Vt = np.linalg.svd(Bc.T @ Ac)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    if improper:
        d = 1.0
    R = Vt.T @ np.diag([1.0, 1.0, d]) @ U.T
    return R, Ac, Bc

print("### provenance")
print("- now (host) :", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z"))
print("- log        :", log)
print("- log sha256 :", sha256(log))
print("- frames     :", [f[0] for f in frames])
print("- heavy atoms:", len(heavy), "of", n)
print()

def variant(p, A_prev, A_cur):
    Xp = np.array([A_prev[i][1] for i in range(n)])
    Xc = np.array([A_cur[i][1] for i in range(n)])
    H = [i for i in heavy]
    out = {}
    # A: superpose heavy (proper), RMSD over heavy, sqrt(sum/N)
    R, Ac, Bc = kabsch_R(Xp[H], Xc[H])
    d = np.sqrt(((( R @ Ac.T).T - Bc) ** 2).sum(1))
    out["A heavy-superpose/heavy-RMSD sqrt(sum/N)"] = math.sqrt((d ** 2).sum() / len(H))
    out["B heavy-superpose/heavy-RMSD sqrt(sum/3N) [per-coordinate]"] = math.sqrt((d ** 2).sum() / (3 * len(H)))
    out["C heavy-superpose (reflection allowed)/heavy sqrt(sum/N)"] = None
    R, Ac, Bc = kabsch_R(Xp[H], Xc[H], improper=True)
    d = np.sqrt(((( R @ Ac.T).T - Bc) ** 2).sum(1))
    out["C heavy-superpose (reflection allowed)/heavy sqrt(sum/N)"] = math.sqrt((d ** 2).sum() / len(H))
    # D: superpose all atoms (proper), RMSD over heavy
    R, Ac, Bc = kabsch_R(Xp, Xc)
    disp = np.sqrt(((( R @ Ac.T).T - Bc) ** 2).sum(1))
    out["D all-superpose/heavy sqrt(sum/N)"] = math.sqrt((disp[H] ** 2).sum() / len(H))
    out["E all-superpose/all-atom sqrt(sum/N)"] = math.sqrt((disp ** 2).sum() / n)
    out["F all-superpose/heavy sqrt(sum/3N)"] = math.sqrt((disp[H] ** 2).sum() / (3 * len(H)))
    # G: heavy superpose, heavy RMSD excluding the constrained pair C1,C29
    Hx = [i for i in H if i not in (0, 28)]
    out["G heavy-superpose/heavy RMSD excluding C1,C29"] = math.sqrt((disp[Hx] ** 2).sum() / len(Hx))
    # H: heavy superpose, mean |d| over heavy (not RMS)
    R, Ac, Bc = kabsch_R(Xp[H], Xc[H])
    d = np.sqrt(((( R @ Ac.T).T - Bc) ** 2).sum(1))
    out["H heavy-superpose/heavy mean|d|"] = float(d.mean())
    # I: enamine-heavy superpose, heavy RMSD
    En = [i for i in H if i < 24]
    R, Ac, Bc = kabsch_R(Xp[En], Xc[En])
    d = np.sqrt(((( R @ Ac.T).T - Bc) ** 2).sum(1))
    out["I enamine-superpose/heavy sqrt(sum/N)"] = math.sqrt((d ** 2).sum() / len(H))
    # J: mass-weighted heavy superpose, heavy sqrt(sum/N)
    w = np.array([MASS[elems[i]] for i in H])
    cA = (Xp[H] * w[:, None]).sum(0) / w.sum()
    cB = (Xc[H] * w[:, None]).sum(0) / w.sum()
    U, S, Vt = np.linalg.svd(((Xc[H] - cB) * w[:, None]).T @ (Xp[H] - cA))
    dd = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1.0, 1.0, dd]) @ U.T
    dm = np.sqrt(((( R @ (Xp[H] - cA).T).T - (Xc[H] - cB)) ** 2).sum(1))
    out["J mass-weighted heavy superpose/heavy sqrt(sum/N)"] = math.sqrt((dm ** 2).sum() / len(H))
    # K: enamine heavy only, superpose and RMSD on the same 11 atoms
    En = [i for i in H if i < 24]
    R, Ac, Bc = kabsch_R(Xp[En], Xc[En])
    d = np.sqrt(((( R @ Ac.T).T - Bc) ** 2).sum(1))
    out["K enamine-heavy superpose/enamine-heavy sqrt(sum/N)"] = math.sqrt((d ** 2).sum() / len(En))
    # L: superpose heavy excluding water 25-27, RMSD on the same set
    Hw = [i for i in H if i not in (24, 25, 26)]
    R, Ac, Bc = kabsch_R(Xp[Hw], Xc[Hw])
    d = np.sqrt(((( R @ Ac.T).T - Bc) ** 2).sum(1))
    out["L heavy-no-water superpose/heavy-no-water sqrt(sum/N)"] = math.sqrt((d ** 2).sum() / len(Hw))
    # M: benzaldehyde heavy only (28-41), superpose and RMSD
    Bz = [i for i in H if i >= 27]
    R, Ac, Bc = kabsch_R(Xp[Bz], Xc[Bz])
    d = np.sqrt(((( R @ Ac.T).T - Bc) ** 2).sum(1))
    out["M benzaldehyde-heavy superpose/same-set sqrt(sum/N)"] = math.sqrt((d ** 2).sum() / len(Bz))
    # N: proline-ring + alpha C core only (atoms 2-9, i.e. C2,C3,N4,C5,C6,C7,C8,C9), superpose + RMSD
    core = [1, 2, 3, 4, 5, 6, 7, 8]
    R, Ac, Bc = kabsch_R(Xp[core], Xc[core])
    d = np.sqrt(((( R @ Ac.T).T - Bc) ** 2).sum(1))
    out["N ring-core(2-9) superpose/same-set sqrt(sum/N)"] = math.sqrt((d ** 2).sum() / len(core))
    out["O ring-core(2-9) superpose/same-set sqrt(sum/3N)"] = math.sqrt((d ** 2).sum() / (3 * len(core)))
    return out

for k in range(1, len(frames)):
    p0, A0 = frames[k - 1]
    p1, A1 = frames[k]
    print("- pair %d -> %d" % (p0, p1))
    for kk, vv in variant(None, A0, A1).items():
        print("    %-62s = %.4f" % (kk, vv))
    print()