import math, sys
def lastframe(path):
    L = open(path, errors="replace").read().splitlines()
    idx = [i for i, l in enumerate(L) if "Input orientation" in l]
    i = idx[-1]
    start = i + 1 + 4
    atoms = []
    while len(atoms) < 200:
        p = L[start].split()
        if len(p) != 6 or not p[0].isdigit():
            break
        atoms.append((int(p[0]), int(p[1]), float(p[3]), float(p[4]), float(p[5])))
        start += 1
    return i + 1, atoms
def d(a, b):
    return math.dist((a[2], a[3], a[4]), (b[2], b[3], b[4]))
els = {1: "H", 6: "C", 7: "N", 8: "O", 16: "S"}
ln, at = lastframe(sys.argv[1])
A = {a[0]: a for a in at}
for probe in [27, 10, 26]:
    near = sorted(((d(A[probe], A[b]), b, els.get(A[b][1])) for b in A if b != probe))[:4]
    print("probe atom", probe, els.get(A[probe][1]), [(float("%.3f" % x), y, z) for x, y, z in near])
