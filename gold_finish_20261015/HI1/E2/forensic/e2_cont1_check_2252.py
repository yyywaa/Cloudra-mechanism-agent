#!/usr/bin/env python3
"""Read-only: converged points of an E2-family scan log (argv[1]).
Prints E, dE vs first converged point, dE vs original pt1 (-939.308205969), R(1,29),R(28,24),R(11,24)."""
import sys, math
LOG = sys.argv[1]
REF_PT1 = -939.308205969
H = 627.509474
lines = open(LOG, "r", errors="replace").read().splitlines()
conv = [i for i, L in enumerate(lines) if "Optimization completed" in L]
pts = []
for ci in conv:
    scf = None
    for j in range(ci, -1, -1):
        if "SCF Done:" in lines[j]:
            scf = (j + 1, float(lines[j].split("=")[1].split()[0])); break
    hdr = None
    for j in range(ci, -1, -1):
        if "Standard orientation:" in lines[j]:
            hdr = j; break
    at = []; k = hdr + 5
    while k < len(lines) and not lines[k].strip().startswith("---"):
        p = lines[k].split()
        if len(p) >= 6 and p[0].isdigit():
            at.append((float(p[3]), float(p[4]), float(p[5])))
        k += 1
    pts.append((ci + 1, scf[0], scf[1], hdr + 1, len(at),
                math.dist(at[0], at[28]), math.dist(at[27], at[23]), math.dist(at[10], at[23])))
print("log=%s  n_conv=%d  NAtoms=%d" % (LOG.split("/")[-1], len(pts), pts[0][4] if pts else 0))
print("i | convLine | scfLine | E(H) | dE_vs_cont1_pt1 | dE_vs_orig_pt1 | R(1,29) | R(28,24) | R(11,24)")
for n, (cl, sl, E, hdr, na, r129, r2824, r1124) in enumerate(pts, 1):
    d1 = (E - pts[0][2]) * H
    d2 = (E - REF_PT1) * H
    print("%d | %6d | %6d | %.9f | %+7.2f | %+7.2f | %.4f | %.4f | %.4f"
          % (n, cl, sl, E, d1, d2, r129, r2824, r1124))
