#!/usr/bin/env python3
"""Read-only: E3b 2D grid (job 1074) traversal-order probe.
For each 'on scan point N out of 36' occurrence: first Standard orientation after it ->
measured (R(2,4), R(25,26), R(4,26), R(2,25)). Also per converged block: energy + distances."""
import math, re
LOG = "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/runs/e3b_scan2d_c2n4_o25h26.log"
lines = open(LOG, "r", errors="replace").read().splitlines()

def geom_after(k):
    hdr = None
    for j in range(k, len(lines)):
        if "Standard orientation:" in lines[j]:
            hdr = j; break
    atoms = []; m = hdr + 5
    while m < len(lines) and not lines[m].strip().startswith("---"):
        p = lines[m].split()
        if len(p) >= 6 and p[0].isdigit():
            atoms.append((float(p[3]), float(p[4]), float(p[5])))
        m += 1
    return hdr + 1, atoms

def d(atoms, i, j): return math.dist(atoms[i-1], atoms[j-1])

pre = re.compile(r"on scan point +([0-9]+) out of")
first = {}
for i, L in enumerate(lines):
    m = pre.search(L)
    if m:
        n = int(m.group(1))
        if n not in first:
            first[n] = i
print("scan points seen: %s" % sorted(first))
print("sp | firstStepLine | geomHdr | R(2,4) | R(25,26) | R(4,26) | R(2,25)")
for n in sorted(first):
    hdr, at = geom_after(first[n])
    print("%2d | %6d | %6d | %.4f | %.4f | %.4f | %.4f"
          % (n, first[n] + 1, hdr, d(at,2,4), d(at,25,26), d(at,4,26), d(at,2,25)))

conv = [i for i, L in enumerate(lines) if "Optimization completed" in L]
print("\nn_conv=%d" % len(conv))
H = 627.509474
e0 = None
print("idx | convLine | scfLine | E(H) | dE_vs_first | R(2,4) | R(25,26) | R(4,26)")
for k, ci in enumerate(conv, 1):
    scf = None
    for j in range(ci, -1, -1):
        if "SCF Done:" in lines[j]:
            scf = (j + 1, float(lines[j].split("=")[1].split()[0])); break
    hdr, at = geom_after(0)
    # geometry: last Standard orientation before ci
    h2 = None
    for j in range(ci, -1, -1):
        if "Standard orientation:" in lines[j]:
            h2 = j; break
    at = []; m = h2 + 5
    while m < len(lines) and not lines[m].strip().startswith("---"):
        p = lines[m].split()
        if len(p) >= 6 and p[0].isdigit():
            at.append((float(p[3]), float(p[4]), float(p[5])))
        m += 1
    if e0 is None: e0 = scf[1]
    print("%2d | %6d | %6d | %.9f | %+7.2f | %.4f | %.4f | %.4f"
          % (k, ci + 1, scf[0], scf[1], (scf[1] - e0) * H, d(at,2,4), d(at,25,26), d(at,4,26)))
