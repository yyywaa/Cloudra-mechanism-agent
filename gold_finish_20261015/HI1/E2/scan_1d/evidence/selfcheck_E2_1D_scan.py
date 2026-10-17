#!/usr/bin/env python3
"""Read-only pre-submission self-check for HI1 E2 1D relaxed-scan input.
Reads bytes only; never writes/edits the .gjf or the seed.
Usage: python3 selfcheck_E2_1D_scan.py <gjf> <seed.xyz>
"""
import sys, hashlib, math, datetime

gjf, seed = sys.argv[1], sys.argv[2]

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

raw = open(gjf, "rb").read()
lines = raw.decode().split("\n")

print("=== 0. provenance ===")
print("now (host time) :", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z"))
print("gjf path        :", gjf)
print("gjf sha256      :", sha256(gjf))
print("gjf bytes       :", len(raw))
print("gjf newline count (== wc -l):", raw.count(b"\n"))
print("gjf split('\\n') element count:", len(lines), "(last element is '' because the file ends with an empty line)")
print("seed path       :", seed)
print("seed sha256     :", sha256(seed))

print()
print("=== 1. link0 + route, verbatim ===")
route_idx = None
for i, ln in enumerate(lines):
    if ln.startswith("%"):
        print("  line %d: %s" % (i+1, ln))
    elif route_idx is None and ln.startswith("#"):
        route_idx = i
        print("  line %d (route): %s" % (i+1, ln))
route = lines[route_idx]
low = route.lower()

print()
print("=== 2. required route tokens (case-insensitive, native Gaussian spelling) ===")
checks = [
    ("opt=modredundant", ["opt=(modredundant", "opt=modredundant"]),
    ("maxstep=8", ["maxstep=8"]),
    ("B3LYP/def2SVP", ["b3lyp/def2svp"]),
    ("EmpiricalDispersion=GD3BJ", ["empiricaldispersion=gd3bj"]),
    ("Int(UltraFine)", ["int(ultrafine)"]),
    ("SCF=Tight", ["scf=tight"]),
    ("CPCM", ["cpcm"]),
    ("DMSO", ["dmso"]),
    ("SCRF(...)", ["scrf=("]),
]
for label, alts in checks:
    hit = [a for a in alts if a in low]
    print("  %-28s -> %s%s" % (label, "present " if hit else "MISSING ",
                               ("as " + repr(route[low.find(hit[0]):low.find(hit[0])+len(hit[0])])) if hit else ""))
print("  ..CPCM(DMSO) is written in native Gaussian form SCRF=(CPCM,Solvent=DMSO); "
      "cpcm=%s dmso=%s" % ("cpcm" in low, "dmso" in low))
for bad in ["def2-svp", "cartesian", "z-matrix", "zmatrix", "geom=connectivity"]:
    print("  forbidden %-18s -> %s" % (bad, "PRESENT(!)" if bad in low else "absent"))
print("  no basis-lowercase hyphen form 'def2-svp':", "def2-svp" not in low)

print()
print("=== 3. end-of-file blank-line structure (byte level) ===")
print("  last 80 bytes repr:", repr(raw[-80:].decode()))
print("  ends with b'\\n\\n' (i.e. a genuine blank final line):", raw.endswith(b"\n\n"))
print("  nothing after the final '\\n':", raw.rsplit(b"\n", 1)[-1] == b"")

print()
print("=== 4. molecule specification structure ===")
i = route_idx + 1
while lines[i].strip() == "":
    i += 1
title_start = i
while lines[i].strip() != "":
    i += 1
print("  title line(s) %d-%d: %s" % (title_start+1, i, " | ".join(lines[title_start:i])))
cm_i = i + 1
while lines[cm_i].strip() == "":
    cm_i += 1
print("  line %d charge/multiplicity: %r" % (cm_i+1, lines[cm_i]))

periodic = set("H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr".split())
coords = []
j = cm_i + 1
while j < len(lines) and len(lines[j].split()) == 4 and lines[j].split()[0] in periodic:
    t = lines[j].split()
    coords.append((t[0], float(t[1]), float(t[2]), float(t[3]), j+1))
    j += 1
print("  atom count parsed:", len(coords), "(expected 41) ->", "OK" if len(coords) == 41 else "MISMATCH")
print("  first coord line: %d   last coord line: %d" % (coords[0][4], coords[-1][4]))
print("  lines from end of coordinate block to EOF:")
rest = [(k+1, lines[k]) for k in range(j, len(lines))]
for ln_no, ln in rest:
    print("    %d: %r" % (ln_no, ln))
mod = [ln for (_, ln) in rest if ln.strip()]
print("  ModRedundant non-blank lines:", mod)
print("  exactly one ModRedundant line:", len(mod) == 1)
print("  blank line separating coords from ModRedundant:", rest and rest[0][1].strip() == "")
print("  blank line after ModRedundant (line %d):" % (j+len(rest)), rest[-1][1] == "")

print()
print("=== 5. coordinate compare .gjf vs seed.xyz, per atom ===")
sraw = open(seed).read().split("\n")
scoords = []
for ln in sraw[2:]:
    t = ln.split()
    if len(t) == 4 and t[0] in periodic:
        scoords.append((t[0], float(t[1]), float(t[2]), float(t[3])))
print("  seed comment lines: 2 ; seed atom count:", len(scoords))
assert len(coords) == len(scoords) == 41, (len(coords), len(scoords))
maxd, argmax, elem_mismatch = 0.0, 0, []
for idx, (g, s) in enumerate(zip(coords, scoords), start=1):
    if g[0] != s[0]:
        elem_mismatch.append((idx, g[0], s[0]))
    d = max(abs(g[1]-s[1]), abs(g[2]-s[2]), abs(g[3]-s[3]))
    if d > maxd:
        maxd, argmax = d, idx
print("  element-order mismatches:", elem_mismatch if elem_mismatch else "none (41/41 identical)")
print("  MAX per-atom max|dx|,|dy|,|dz| over 41 atoms = %.17g Angstrom (largest at atom %d)" % (maxd, argmax))
print("  bit-identical coordinates (max|delta| == 0):", maxd == 0.0)

print()
print("=== 6. identity of atoms 1 and 29 + geometry cross-checks ===")
def dist(a, b):
    return math.sqrt((a[1]-b[1])**2 + (a[2]-b[2])**2 + (a[3]-b[3])**2)
a1, a29 = coords[0], coords[28]
print("  atom  1  (gjf line %d): %s   %14.8f %14.8f %14.8f" % (a1[4], a1[0], a1[1], a1[2], a1[3]))
print("  atom 29  (gjf line %d): %s   %14.8f %14.8f %14.8f" % (a29[4], a29[0], a29[1], a29[2], a29[3]))
print("  atom  2  element %s (enamine alpha-C: C=C partner of atom 1 -> atom 1 is the terminal =CH2)" % coords[1][0])
print("  atom 28  element %s (benzaldehyde carbonyl O: C=O partner of atom 29 -> atom 29 is the aldehyde C)" % coords[27][0])
print("  R(1,29)  = %.6f Angstrom  (design seed 4.3543 ; scan start)" % dist(a1, a29))
print("  R(1,2)   = %.4f  (enamine C=C)   R(28,29) = %.4f  (benzaldehyde C=O)" % (dist(coords[0], coords[1]), dist(coords[27], coords[28])))
print("  R(2,4)   = %.4f  (enamine C-N)" % dist(coords[1], coords[3]))
print("  R(O28...H24) = R(O28-H24) = %.4f  (identical atom pair; label differs only)" % dist(coords[27], coords[23]))
print("  R(O11-H24)   = %.4f  (donor covalent O-H of the proline carboxyl)" % dist(coords[10], coords[23]))

print()
print("=== 7. resource declarations vs authorisation (8 cpus / 10240 MB) ===")
print("  line 2: %r  -> nprocshared == 8 : %s" % (lines[1], lines[1].strip().replace(" ", "") == "%nprocshared=8"))
print("  line 3: %r  -> mem == 10240MB : %s" % (lines[2], lines[2].strip().replace(" ", "").upper() == "%MEM=10240MB"))
print("  charge/multiplicity: %r (design q0/m1: %s)" % (lines[cm_i], lines[cm_i].split() == ["0", "1"]))
