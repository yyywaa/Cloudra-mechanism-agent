#!/usr/bin/env python3
"""Read-only geometry reporter for HL1 round4 evidence.

Usage:
  python3 geo_check.py <file.xyz>                # element list + covalent-bond table
  python3 geo_check.py <file.xyz> 1 2 1 9 2 9    # (1-based) distance pairs
No files are written; prints to stdout only.
"""
import sys, math

COV = {"H": 0.31, "C": 0.76, "N": 0.71, "O": 0.66}

def load(path):
    lines = [l for l in open(path).read().splitlines()]
    n = int(lines[0].split()[0])
    atoms = []
    for l in lines[2:2 + n]:
        p = l.split()
        atoms.append((p[0], float(p[1]), float(p[2]), float(p[3])))
    return atoms

def dih(a, b, c, e):
    import numpy as np
    b1 = np.array(b[1:]) - np.array(a[1:])
    b2 = np.array(c[1:]) - np.array(b[1:])
    b3 = np.array(e[1:]) - np.array(c[1:])
    n1 = np.cross(b1, b2); n2 = np.cross(b2, b3)
    m = np.cross(n1, b2 / np.linalg.norm(b2))
    x = np.dot(n1, n2); y = np.dot(m, n2)
    return math.degrees(math.atan2(y, x))

def d(a, b):
    return math.sqrt(sum((a[i + 1] - b[i + 1]) ** 2 for i in range(3)))

def main():
    path = sys.argv[1]
    atoms = load(path)
    print("file=%s natoms=%d" % (path, len(atoms)))
    print("idx  el      x          y          z")
    for i, a in enumerate(atoms, 1):
        print("%3d  %-2s %10.5f %10.5f %10.5f" % (i, a[0], a[1], a[2], a[3]))
    if len(sys.argv) > 2 and sys.argv[2] == "dih":
        idx = [int(x) for x in sys.argv[3:]]
        if len(idx) % 4:
            print("ERROR: give groups of 4 indices for dihedrals")
            return
        for k in range(0, len(idx), 4):
            i, j, l, m = idx[k:k + 4]
            v = dih(atoms[i - 1], atoms[j - 1], atoms[l - 1], atoms[m - 1])
            print("D(%d,%d,%d,%d) = %.2f deg" % (i, j, l, m, v))
        return
    rest = [float(x) for x in sys.argv[2:]]
    if rest:
        if len(rest) % 2:
            print("ERROR: give pairs of 1-based indices")
            return
        for k in range(0, len(rest), 2):
            i, j = int(rest[k]), int(rest[k + 1])
            print("R(%d,%d) %s-%s = %.4f A" % (i, j, atoms[i - 1][0], atoms[j - 1][0], d(atoms[i - 1], atoms[j - 1])))
    else:
        print("-- bonds by covalent-radius sum * 1.25 --")
        for i in range(len(atoms)):
            for j in range(i + 1, len(atoms)):
                dist = d(atoms[i], atoms[j])
                if dist < 1.25 * (COV[atoms[i][0]] + COV[atoms[j][0]]):
                    print("  %2d %-2s - %2d %-2s  %.4f" % (i + 1, atoms[i][0], j + 1, atoms[j][0], dist))

main()
