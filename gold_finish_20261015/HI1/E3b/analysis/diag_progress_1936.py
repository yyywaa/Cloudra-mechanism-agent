import math, itertools, sys
def lastframe(path):
    L = open(path, errors="replace").read().splitlines()
    idx = [i for i, l in enumerate(L) if "Input orientation" in l]
    i = idx[-1]
    k = i + 1
    assert L[k].strip().startswith("---"), L[k]
    start = k + 4
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
for tag, path in [("1069", sys.argv[1]), ("1071", sys.argv[2])]:
    ln, at = lastframe(path)
    print(tag, "input_orientation_line", ln, "natoms", len(at), "Zlist_first8", [a[1] for a in at[:8]])
    A = {a[0]: a for a in at}
    for p in [(2, 4), (2, 25), (4, 26), (25, 26), (10, 27), (2, 3), (1, 2), (25, 27)]:
        print("   R(%d,%d)=%.4f" % (p[0], p[1], d(A[p[0]], A[p[1]])))
    mn = (99.0, None)
    tight = []
    for x, y in itertools.combinations(at, 2):
        dd = d(x, y)
        if dd < mn[0]:
            mn = (dd, (x[0], y[0]))
        if dd < 0.90:
            tight.append((x[0], y[0], els.get(x[1]), els.get(y[1]), round(dd, 4)))
    print("   minsep=%.4f at %s" % (mn[0], str(mn[1])))
    if tight:
        print("   tight:", tight)
