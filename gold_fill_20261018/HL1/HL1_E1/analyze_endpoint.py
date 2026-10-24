#!/usr/bin/env python3
"""HL1_E1 endpoint identity report for a Gaussian opt/freq log.

Prints: last SCF energy, optimisation flag, imaginary-mode count, geometry flags
(R(1,2), R(2,9), R(1,9), R(N6,H*), R(9,16), C=N, N-O), proton ownership per oxygen/nitrogen,
and the number of fragments from a simple covalent-radius criterion.
Atom order = package order (1=O1, 2=H2 transfer proton, 3=H3, 4=H4, 5..10 heavy, 11-19 H).
"""
import sys, math, re

def read_log(p):
    return open(p, errors="replace").read().splitlines()

def last_geom(L):
    idx = [i for i, l in enumerate(L) if "Standard orientation" in l or "Input orientation" in l]
    if not idx:
        return None
    st = idx[-1]
    atoms = []
    for l in L[st + 1:]:
        f = l.split()
        if len(f) >= 6 and f[0].isdigit():
            atoms.append((int(f[0]), int(f[1]), (float(f[3]), float(f[4]), float(f[5]))))
        elif atoms and set(l.strip()) <= set("- "):
            break
    return atoms

RAD = {1: 0.31, 6: 0.76, 7: 0.71, 8: 0.66}

def frags(atoms):
    n = len(atoms)
    parent = list(range(n))
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]; a = parent[a]
        return a
    for i in range(n):
        for j in range(i + 1, n):
            d = math.dist(atoms[i][2], atoms[j][2])
            if d < 1.25 * (RAD[atoms[i][1]] + RAD[atoms[j][1]]):
                parent[find(i)] = find(j)
    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i + 1)
    return list(groups.values())

def main(p):
    L = read_log(p)
    print("log:", p)
    scf = [(i + 1, l) for i, l in enumerate(L) if "SCF Done" in l]
    print("last SCF (line %d): %s" % scf[-1] if scf else "no SCF")
    opt = [i + 1 for i, l in enumerate(L) if "Stationary point found" in l or "Optimization completed" in l]
    print("opt-converged lines:", opt[-3:] if opt else "none")
    print("normal termination:", [i + 1 for i, l in enumerate(L) if "Normal termination" in l])
    print("error termination:", [i + 1 for i, l in enumerate(L) if "Error termination" in l])
    neg = []
    for l in L:
        if l.lstrip().startswith("Frequencies --"):
            for v in re.findall(r"-\d+\.\d+", l):
                neg.append(float(v))
    print("imaginary (negative) frequencies:", neg if neg else "none")
    im_line = [i + 1 for i, l in enumerate(L) if "imaginary frequencies" in l]
    print("imaginary-frequency banner lines:", im_line)
    nfreq = sum(len(re.findall(r"-?\d+\.\d+", l)) for l in L if l.lstrip().startswith("Frequencies --"))
    print("total frequencies listed:", nfreq)
    atoms = last_geom(L)
    if not atoms:
        print("no geometry"); return
    print("geometry block atoms:", len(atoms))
    def d(i, j):
        return math.dist(atoms[i - 1][2], atoms[j - 1][2])
    def nearH(target, others):
        return sorted(((d(target, h), h) for h in others), key=lambda x: x[0])[:3]
    Hs = [a[0] for a in atoms if a[1] == 1]
    O1, N6, O7 = 1, 8, 9
    print("R(1,2)=%.4f  R(2,9)=%.4f  R(1,9)=%.4f" % (d(1, 2), d(2, 9), d(1, 9)))
    print("R(7,8)=C=N %.4f  R(8,9)=N-O %.4f  R(7,10)=%.4f R(7,6)=%.4f" % (d(7, 8), d(8, 9), d(7, 10), d(7, 6)))
    for name, at in (("O1", O1), ("N6", N6), ("O7", O7)):
        print("  nearest H to %s: %s" % (name, [(round(a, 3), h) for a, h in nearH(at, Hs)]))
    print("fragments:", frags(atoms))
    owner = {}
    for h in Hs:
        best = min(((d(h, x), n) for x, n in ((O1, "O1"), (N6, "N6"), (O7, "O7"))))
        owner.setdefault(best[1], []).append((h, round(best[0], 3)))
    print("proton ownership (nearest of O1/N6/O7):", owner)

if __name__ == "__main__":
    main(sys.argv[1])
