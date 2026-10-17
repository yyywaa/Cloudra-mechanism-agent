#!/usr/bin/env python3
"""Read-only: recompute E2 1D scan converged-point energies and key distances.
No writes. Coordinator lane, 22:15 CST."""
import math
LOG = "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan.log"
lines = open(LOG, "r", errors="replace").read().splitlines()
conv = [i for i, L in enumerate(lines) if "Optimization completed." in L]
pts = []
for ci in conv:
    scf = None
    for j in range(ci, -1, -1):
        if "SCF Done:" in lines[j]:
            scf = (j + 1, float(lines[j].split("=")[1].split()[0]))
            break
    hdr = None
    for j in range(ci, -1, -1):
        if "Standard orientation:" in lines[j]:
            hdr = j
            break
    atoms = []
    if hdr is not None:
        k = hdr + 5
        while k < len(lines) and not lines[k].strip().startswith("---"):
            p = lines[k].split()
            if len(p) >= 6 and p[0].isdigit():
                atoms.append((float(p[3]), float(p[4]), float(p[5])))
            k += 1
    def d(i, j):
        return math.dist(atoms[i - 1], atoms[j - 1])
    pts.append((ci + 1, scf[0], scf[1], hdr + 1, len(atoms), d(1, 29), d(28, 24), d(11, 24)))
H = 627.509474
e0 = pts[0][2]
print("n_conv=%d  NAtoms_first=%d" % (len(pts), pts[0][4]))
print("pt | convLine | scfLine | E(H) | dE_kcal | R(1,29) | R(28,24) | R(11,24) | geomHdr")
for n, (cl, sl, E, hdr, na, r129, r2824, r1124) in enumerate(pts, 1):
    print("%2d | %7d | %7d | %.9f | %+7.2f | %.4f | %.4f | %.4f | %d (na=%d)"
          % (n, cl, sl, E, (E - e0) * H, r129, r2824, r1124, hdr, na))
