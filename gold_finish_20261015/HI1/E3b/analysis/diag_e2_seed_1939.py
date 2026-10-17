import sys, itertools, math
def xyz(path):
    L = open(path).read().splitlines()
    n = int(L[0]); at = []
    for l in L[2:2+n]:
        p = l.split(); at.append((p[0], float(p[1]), float(p[2]), float(p[3])))
    return at
at = xyz(sys.argv[1])
print("natoms", len(at), "formula", {e: sum(1 for a in at if a[0]==e) for e in set(a[0] for a in at)})
C = [(i+1, a) for i, a in enumerate(at) if a[0] == "C"]
nonb = sorted(((math.dist(a[1:], b[1:]), i, j) for (i, a), (j, b) in itertools.combinations(C, 2) if math.dist(a[1:], b[1:]) > 1.8))[:5]
print("shortest nonbonded C...C:", [(round(d,3), i, j) for d, i, j in nonb])
X = [(i+1, a) for i, a in enumerate(at) if a[0] in ("N", "O")]
short = sorted(((math.dist(c[1][1:], x[1][1:]), c[0], x[0], x[1][0]) for c in C for x in X if math.dist(c[1][1:], x[1][1:]) > 2.0))[:5]
print("shortest C...N/O:", [(round(d,3), i, j, e) for d, i, j, e in short])
