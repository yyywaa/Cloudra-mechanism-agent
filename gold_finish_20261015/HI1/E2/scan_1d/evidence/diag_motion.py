#!/usr/bin/env python3
"""Read-only motion diagnostic for the HI1 E2 1D relaxed scan.

For each pair of CONSECUTIVE converged scan points:
  * rigid-body (Kabsch) superposition on the 20 heavy atoms, then per-atom displacement;
  * top movers (atom label + |d|);
  * RMSD of each fragment (enamine 1-24, water 25-27, benzaldehyde 28-41) after the SAME
    global superposition, so a drifting solvent molecule can be told apart from a
    reorganising reactant;
  * heavy-atom RMSD again with water 25-27 excluded.
Read-only: prints only. Usage: python3 diag_motion.py <log>
"""
import sys, math, datetime, hashlib
import numpy as np

ELEM = {1:"H",2:"He",3:"Li",4:"Be",5:"B",6:"C",7:"N",8:"O",9:"F",10:"Ne"}

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()

log = sys.argv[1]
raw = open(log, "r", errors="replace").read()
lines = raw.split("\n")

oc = [i for i, ln in enumerate(lines) if ln.strip() == "Optimization completed."]
so = [i for i, ln in enumerate(lines) if "Standard orientation:" in ln]
scf = [i for i, ln in enumerate(lines) if ln.strip().startswith("SCF Done:")]

def parse_orientation(start):
    i = start + 1
    while i < len(lines) and not lines[i].strip().startswith("---"):
        i += 1
    i += 1
    while i < len(lines) and not lines[i].strip().startswith("---"):
        i += 1
    i += 1
    atoms = []
    while i < len(lines) and not lines[i].strip().startswith("---"):
        t = lines[i].split()
        if len(t) >= 6:
            atoms.append((ELEM.get(int(t[1]), "X"), np.array([float(t[3]), float(t[4]), float(t[5])])))
        i += 1
    return atoms

frames = []
for k, o in enumerate(oc):
    prev = oc[k - 1] if k > 0 else -1
    s = [x for x in so if prev < x < o]
    if not s:
        continue
    frames.append((k + 1, parse_orientation(s[-1]), lines[scf[-1] if False else [x for x in scf if prev < x < o][-1]]))

elems = [a[0] for a in frames[0][1]]
heavy = [i for i, e in enumerate(elems) if e != "H"]

def kabsch(A, B):
    Ac = A - A.mean(0); Bc = B - B.mean(0)
    U, S, Vt = np.linalg.svd(Bc.T @ Ac)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1.0, 1.0, d]) @ U.T
    return (R @ Ac.T).T, Bc

print("### provenance")
print("- now (host) :", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z"))
print("- log        :", log)
print("- log sha256 :", sha256(log))
print("- log lines  :", raw.count("\n"))
print("- converged frames parsed:", [f[0] for f in frames])
print()
print("### consecutive-point motion (Kabsch on 20 heavy atoms, then per-atom displacement)")
for k in range(1, len(frames)):
    p_prev, A_prev, _ = frames[k - 1]
    p_cur, A_cur, _ = frames[k]
    Xp = np.array([A_prev[i][1] for i in heavy]); Xc = np.array([A_cur[i][1] for i in heavy])
    Ar, Bc = kabsch(Xp, Xc)
    rmsd_h = float(np.sqrt(((Ar - Bc) ** 2).sum() / len(heavy)))
    # apply the same transformation to all atoms (build with full-atom alignment)
    Afull_p = np.array([A_prev[i][1] for i in range(len(A_prev))])
    Afull_c = np.array([A_cur[i][1] for i in range(len(A_cur))])
    Ac_full = Afull_p - Xp.mean(0); Bc_full = Afull_c - Xc.mean(0)
    U, S, Vt = np.linalg.svd(Bc_full.T @ Ac_full)
    dd = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1.0, 1.0, dd]) @ U.T
    rot = (R @ Ac_full.T).T
    disp = np.sqrt(((rot - Bc_full) ** 2).sum(1))
    print("- point %d -> %d : heavy-atom Kabsch RMSD = %.3f A" % (p_prev, p_cur, rmsd_h))
    for name, idxs in (("enamine 1-24", list(range(0, 24))),
                       ("water 25-27", list(range(24, 27))),
                       ("benzaldehyde 28-41", list(range(27, 41)))):
        d = disp[idxs]
        print("    %-20s rms(d) = %.3f A, max|d| = %.3f A (%s%d)" % (
            name, float(math.sqrt((d ** 2).mean())), float(d.max()),
            elems[idxs[int(np.argmax(d))]], idxs[int(np.argmax(d))] + 1))
    hw = [i for i in heavy if i not in (24, 25, 26)]
    A2 = np.array([A_prev[i][1] for i in hw]); B2 = np.array([A_cur[i][1] for i in hw])
    Ar2, Bc2 = kabsch(A2, B2)
    print("    heavy atoms EXCLUDING water 25-27: Kabsch RMSD = %.3f A" % float(np.sqrt(((Ar2 - Bc2) ** 2).sum() / len(hw))))
    order = np.argsort(-disp)[:8]
    print("    top movers: " + ", ".join("%s%d |d|=%.2f" % (elems[i], i + 1, disp[i]) for i in order))
print()
print("### dihedral/geometry probes per converged point")
def dih(a, b, c, d):
    b0 = a - b; b1 = c - b; b2 = d - c
    b1n = b1 / np.linalg.norm(b1)
    v = b0 - np.dot(b0, b1n) * b1n
    w = b2 - np.dot(b2, b1n) * b1n
    x = np.dot(v, w); y = np.dot(np.cross(b1n, v), w)
    return math.degrees(math.atan2(y, x))
for p, A, _ in frames:
    X = [a[1] for a in A]
    # enamine ring pucker proxy: N4-C5-C6-C7 improper vs C3-C2-N4-C5 ; aryl torsion C30-C29 ...
    t_enamine = dih(X[2], X[1], X[3], X[4])          # C3-C2-N4-C5
    t_ald = dih(X[0], X[28], X[27], X[26])            # C1-C29-O28-C27 : approach torsion
    aryl = dih(X[28], X[29], X[30], X[31])            # C29-C30-C31-C32 aryl torsion
    wat = dih(X[23], X[24], X[26], X[27])             # H24-O25-H26-H27 water orientation proxy
    print("- point %2d: C3-C2-N4-C5 = %8.2f deg | C1-C29-O28-C27 = %8.2f deg | aryl C29-C30-C31-C32 = %8.2f deg | water H24-O25-H26-H27 = %8.2f deg"
          % (p, t_enamine, t_ald, aryl, wat))