#!/usr/bin/env python3
"""Per-point analysis of the HL1 round4 T3 relaxed proton-transfer scan.

Input: T3_scan_curve.csv (written by format_converter log->csv from
T3_ptscan_H2O9_relaxed.log; 20 frames, one converged scan point each).
Read-only: prints tables to stdout, writes nothing.
Atom order (1-based, package convention): 1=O1 2=H2 3=H4 4=H10 5=C11 6=C5 7=C4
8=N6 9=O7 10=C3 11-13=H(C11) 14-15=H(C5) 16=H8(oxime OH) 17-19=H(C3).
"""
import csv, math, sys

HA2KCAL = 627.509474
PAIRS = [(1, 2), (2, 9), (1, 9), (1, 3), (1, 4), (3, 8), (2, 8), (8, 9), (9, 16), (7, 8), (1, 8)]

def dist(a, b):
    return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(3)))

def parse_xyz(text):
    lines = [l for l in text.splitlines() if l.strip()]
    n = int(lines[0].split()[0])
    out = []
    for l in lines[2:2 + n]:
        p = l.split()
        out.append((p[0], float(p[1]), float(p[2]), float(p[3])))
    return out

path = sys.argv[1] if len(sys.argv) > 1 else "T3_scan_curve.csv"
rows = []
with open(path) as fh:
    for rec in csv.reader(fh):
        if not rec or rec[0] == "frame":
            continue
        rows.append(rec)

print("frames=%d" % len(rows))
hdr = "pt  R(2,9)   R(1,2)   R(1,9)   R(1,3)   R(3,8)   R(2,8)   R(8,9)   E/Ha          dE/pt1   dE/pt1"
print(hdr + " (kcal/mol)")
e0 = float(rows[0][3])
best = (None, -1e9)
for i, rec in enumerate(rows, 1):
    atoms = parse_xyz(rec[6])
    d = {p: dist(atoms[p[0] - 1][1:], atoms[p[1] - 1][1:]) for p in PAIRS}
    e = float(rec[3])
    rel = (e - e0) * HA2KCAL
    if rel > best[1]:
        best = (i, rel)
    print("%2d  %7.4f  %7.4f  %7.4f  %7.4f  %7.4f  %7.4f  %7.4f  %12.8f  %+8.3f" % (
        i, d[(2, 9)], d[(1, 2)], d[(1, 9)], d[(1, 3)], d[(3, 8)], d[(2, 8)], d[(8, 9)], e, rel))
print("highest point: scan point %d, +%.3f kcal/mol relative to point 1" % best)
# internal maximum test (strict: a point strictly above both neighbours)
peaks = []
for i in range(1, len(rows) - 1):
    e = float(rows[i][3]); ep = float(rows[i - 1][3]); en = float(rows[i + 1][3])
    if e >= ep and e >= en and (e > ep or e > en):
        peaks.append((i + 1, (e - e0) * HA2KCAL))
print("internal maxima (strict local maxima, endpoints excluded):", peaks if peaks else "NONE")
print("monotonic rising then falling? %s" % ("yes" if peaks else "not established by this test"))
