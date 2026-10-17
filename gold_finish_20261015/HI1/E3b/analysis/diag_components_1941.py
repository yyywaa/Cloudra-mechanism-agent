import sys, math
rad = {"H":0.31,"C":0.76,"N":0.71,"O":0.66,"S":1.05}
def xyz(path):
    L = open(path).read().splitlines()
    n = int(L[0]); at = []
    for l in L[2:2+n]:
        p = l.split(); at.append((p[0], float(p[1]), float(p[2]), float(p[3])))
    return at
for path in sys.argv[1:]:
    at = xyz(path)
    n = len(at)
    par = list(range(n))
    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]; a = par[a]
        return a
    def uni(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: par[ra] = rb
    bonds = 0
    for i in range(n):
        for j in range(i+1, n):
            d = math.dist(at[i][1:], at[j][1:])
            if d < 1.3 * (rad[at[i][0]] + rad[at[j][0]]):
                uni(i, j); bonds += 1
    comps = {}
    for i in range(n):
        comps.setdefault(find(i), []).append(i+1)
    print(path.split("/")[-3] + "/" + path.split("/")[-1], "natoms", n, "bonds", bonds, "components", len(comps), "sizes", sorted(len(v) for v in comps.values()))
    for k, v in comps.items():
        print("   frag", [at[i-1][0] for i in v].count("C"), "C", len(v), "atoms", v[:12], "..." if len(v) > 12 else "")
