import math, sys
def lastframe(path):
    L = open(path, errors="replace").read().splitlines()
    idx = [i for i, l in enumerate(L) if "Input orientation" in l]
    i = idx[-1]
    start = i + 1 + 4
    atoms = []
    while len(atoms) < 300:
        p = L[start].split()
        if len(p) != 6 or not p[0].isdigit():
            break
        atoms.append((int(p[0]), int(p[1]), float(p[3]), float(p[4]), float(p[5])))
        start += 1
    return i + 1, atoms
def d(a, b):
    return math.dist((a[2], a[3], a[4]), (b[2], b[3], b[4]))
els = {1: "H", 6: "C", 7: "N", 8: "O", 16: "S"}
path = sys.argv[1]
ln, at = lastframe(path)
print("file", path)
print("last_input_orientation_line", ln, "natoms", len(at), "Z", [a[1] for a in at[:12]])
A = {a[0]: a for a in at}
for p in [(2, 4), (2, 25), (4, 26), (25, 26), (10, 27), (25, 27), (2, 3), (1, 2), (9, 10)]:
    print("   R(%d,%d)=%.4f" % (p[0], p[1], d(A[p[0]], A[p[1]])))
for probe in [26, 27, 25, 10, 4]:
    near = sorted(((d(A[probe], A[b]), b) for b in A if b != probe))[:3]
    print("   probe %d %s:" % (probe, els.get(A[probe][1])),
          ["%s%d@%.3f" % (els.get(A[b][1]), b, x) for x, b in near])
