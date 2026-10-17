#!/usr/bin/env python3
"""Detail view of selected converged scan points of the HL1 round4 T3 scan.

Usage: python3 t3_detail.py T3_scan_curve.csv 1 8 11 15 20
Prints, per requested (1-based) point: proton inventory (heavy atom -> H within
1.25 A) and selected interatomic distances. Read-only (stdout only).

Atom order (package convention, 1-based):
1=O1 2=H2 3=H4 4=H10 5=C11 6=C5 7=C4 8=N6 9=O7 10=C3 11-13=H(C11)
14-15=H(C5) 16=H8(oxime OH) 17-19=H(C3)
Ligand labels are the registry's; the printed indices are the file order.
"""
import csv, math, sys

def dist(a, b):
    return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(3)))

def parse_xyz(text):
    lines = [l for l in text.splitlines() if l.strip()]
    n = int(lines[0].split()[0])
    return [(p[0], float(p[1]), float(p[2]), float(p[3]))
            for p in (l.split() for l in lines[2:2 + n])]

csv_path = sys.argv[1]
want = [int(x) for x in sys.argv[2:]]
rows = [r for r in csv.reader(open(csv_path)) if r and r[0] != "frame"]

for k in want:
    rec = rows[k - 1]
    atoms = parse_xyz(rec[6])
    print("=== scan point %d  R(2,9)=%s  E=%s Ha ===" % (k, rec[2], rec[3]))
    inv = {}
    for i, a in enumerate(atoms):
        if a[0] == "H":
            continue
        hs = [j + 1 for j, b in enumerate(atoms)
              if b[0] == "H" and dist(a[1:], b[1:]) < 1.25]
        inv[i + 1] = hs
    print("  heavy-atom H inventory (idx:el -> Hs): " +
          "; ".join("%d:%s->%s" % (i, atoms[i - 1][0], v) for i, v in inv.items()))
    pairs = [(1, 2), (1, 3), (1, 4), (1, 8), (1, 9), (2, 8), (2, 9), (3, 8), (3, 9),
             (4, 8), (4, 9), (7, 8), (8, 9), (9, 16), (8, 16), (1, 16)]
    print("  " + "  ".join("R(%d,%d)=%.4f" % (i, j, dist(atoms[i - 1][1:], atoms[j - 1][1:]))
                           for i, j in pairs))
