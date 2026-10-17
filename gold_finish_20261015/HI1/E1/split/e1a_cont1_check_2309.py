#!/usr/bin/env python3
"""Read-only: converged points of the E1a cont1 scan (27 atoms C8H15NO3).
Prints E, dE vs RC_27 (-593.934532807), R(2,18), R(3,27), R(18,27), R(13,19)."""
import math
LOG = "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split/E1A_scan_cont1_C2N18.log"
REF = -593.934532807
H = 627.509474
lines = open(LOG, "r", errors="replace").read().splitlines()
conv = [i for i, L in enumerate(lines) if "Optimization completed" in L]
print("n_conv=%d" % len(conv))
print("i | convLine | scfLine | E(H) | dE_vs_RC27 | R(2,18) | R(3,27) | R(18,27) | R(13,19)")
for n, ci in enumerate(conv, 1):
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
    d = lambda i, j: math.dist(at[i-1], at[j-1])
    print("%d | %6d | %6d | %.9f | %+7.2f | %.4f | %.4f | %.4f | %.4f"
          % (n, ci + 1, scf[0], scf[1], (scf[1] - REF) * H, d(2,18), d(3,27), d(18,27), d(13,19)))
