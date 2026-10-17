#!/usr/bin/env python3
"""HI1_E3: extract the R(C2-O25)=1.8996 A frame of the constrained scan (job 980) as a
*provided TS guess*, with provenance and cross-checks. Constrained-scan peak geometry =
guess only; scan energies are NOT used as barrier evidence.

Evidence chain (verified in this script):
  log : gold_finish_20261015/HI1/E3/runs/preorg_v3/scan_c2o25_220_160.log
        sha256 436c4cd9225bd29c1ae65086e1394b27b886e4d45206f4efa91133b331030f66
  csv : .../preorg_v3/scan_c2o25_220_160_curve.csv  (format_converter log->csv, 5 frames)
  ref : gold_finish_20261015/HI1/E3/runs/I2_optfreq/I2_min_v5.xyz (reactant atom order)
        sha256 9a6203ff67d9f0d95ad774e78b17bc397b22992f24cbcdf448f8c5558142ef2b
The output xyz keeps the *reactant* atom order (the log frame is checked to use the same
element sequence and the same perceived covalent bond graph at the same indices).
"""
import csv, hashlib, os, math, sys

ROOT = "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3"
LOG  = os.path.join(ROOT, "runs/preorg_v3/scan_c2o25_220_160.log")
CSVL = os.path.join(ROOT, "runs/preorg_v3/scan_c2o25_220_160_curve.csv")
REF  = os.path.join(ROOT, "runs/I2_optfreq/I2_min_v5.xyz")
OUT  = (sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "prep/guess_c2o25_190/ts_guess_c2o25_190.xyz"))
SHA = {"log": "436c4cd9225bd29c1ae65086e1394b27b886e4d45206f4efa91133b331030f66",
       "ref": "9a6203ff67d9f0d95ad774e78b17bc397b22992f24cbcdf448f8c5558142ef2b"}
Z2S = {1: "H", 6: "C", 7: "N", 8: "O"}
RCOV1 = {"H": 0.31, "C": 0.76, "N": 0.71, "O": 0.66}

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def read_xyz(p):
    L = open(p).read().splitlines()
    n = int(L[0].split()[0])
    return [(t[0], float(t[1]), float(t[2]), float(t[3])) for t in (l.split() for l in L[2:2 + n])]

def dist(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a[1:], b[1:])))

assert sha256(LOG) == SHA["log"], "log sha256 mismatch (evidence changed!)"
assert sha256(REF) == SHA["ref"], "reference xyz sha256 mismatch"
ref = read_xyz(REF)

want = float(sys.argv[1]) if len(sys.argv) > 1 else 1.89959
frame = None
with open(CSVL) as f:
    for r in csv.DictReader(f):
        if abs(float(r["reaction_coordinate"]) - want) < 1e-4:
            frame = r
assert frame is not None, "csv frame not found"
csv_atoms = [(t[0], float(t[1]), float(t[2]), float(t[3]))
             for t in (l.split() for l in frame["xyz"].splitlines()[2:])]

lines = open(LOG).read().splitlines()
blocks = []
i = 0
while i < len(lines):
    if lines[i].strip().startswith("Standard orientation"):
        hdr = i + 1
        j = i + 5
        atoms = []
        while j < len(lines) and len(lines[j].split()) == 6:
            t = lines[j].split()
            atoms.append((Z2S[int(t[1])], float(t[3]), float(t[4]), float(t[5])))
            j += 1
        if len(atoms) == 41:
            blocks.append((hdr, atoms))
        i = j
    else:
        i += 1

match = None
for hdr, atoms in blocks:
    d = max(dist(a, b) for a, b in zip(atoms, csv_atoms))
    if d < 1e-4:
        match = (hdr, atoms, d)
assert match, "no log Standard-orientation block matches the csv frame"
hdr, atoms, maxdev = match

assert [a[0] for a in atoms] == [a[0] for a in ref], "element sequence differs from reactant xyz"
assert [a[0] for a in csv_atoms] == [a[0] for a in ref], "csv element sequence differs from reactant xyz"

def adj(at):
    g = {k: set() for k in range(len(at))}
    for a in range(len(at)):
        for b in range(a + 1, len(at)):
            if dist(at[a], at[b]) < 1.25 * (RCOV1[at[a][0]] + RCOV1[at[b][0]]):
                g[a].add(b); g[b].add(a)
    return g

ga, gr = adj(atoms), adj(ref)
iso = all(ga[k] == gr[k] for k in range(41))

WATCH = [(2, 4), (25, 26), (25, 27), (2, 25), (4, 26), (11, 27)]
KEY = [(1, 29), (2, 4), (9, 10), (9, 11), (24, 28), (10, 27), (11, 24),
       (25, 26), (25, 27), (28, 29), (2, 25), (4, 26), (11, 27)]

print("MATCHED log Standard orientation header line %d (csv/log max coord deviation %.2e)" % (hdr, maxdev))
print("element sequence identical to reactant xyz: True ; perceived bond graph identical at the same indices: %s" % iso)
print("degree (all atoms):", {k + 1: len(ga[k]) for k in sorted(ga)})
print()
print("key distances (A), 1.8996 A frame vs reactant minimum:")
for a, b in KEY:
    print("   R(%2d,%2d) %2s-%2s = %7.4f   [reactant %7.4f]" %
          (a, b, atoms[a - 1][0], atoms[b - 1][0], dist(atoms[a - 1], atoms[b - 1]), dist(ref[a - 1], ref[b - 1])))
print()
print("declared 6 watch pairs:")
for a, b in WATCH:
    print("   R(%2d,%2d) = %.4f" % (a, b, dist(atoms[a - 1], atoms[b - 1])))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    f.write("41\n")
    f.write("TS guess frame R(C2-O25)=1.8996 A | src %s sha256 %s | log Standard orientation line %d "
            "| scan point 3/5 converged, E(RB3LYP)=-939.297771992 (log line 25258) | atom order = "
            "I2_min_v5.xyz sha256 %s\n" % (LOG, SHA["log"], hdr, SHA["ref"]))
    for s, x, y, z in atoms:
        f.write("%-2s %14.8f %14.8f %14.8f\n" % (s, x, y, z))
print()
print("written:", OUT, sha256(OUT))
