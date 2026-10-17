import math
P = 'HI1/E3/runs/e3b_scan2d_c2n4_o25h26.log'
L = open(P).read().splitlines()
def geom_blocks(L):
    out = []
    for i, l in enumerate(L):
        if 'Standard orientation' in l:
            at = []; j = i + 5
            while j < len(L) and not L[j].strip().startswith('-----'):
                p = L[j].split()
                if len(p) == 6:
                    at.append((int(p[0]), int(p[1]), float(p[3]), float(p[4]), float(p[5])))
                j += 1
            out.append((i + 1, at))
    return out
B = geom_blocks(L)
scf = [(i + 1, float(l.split('=')[1].split()[0])) for i, l in enumerate(L) if 'SCF Done' in l]
conv = [i + 1 for i, l in enumerate(L) if 'Optimization completed' in l]
print('converged blocks =', len(conv))
def dist(at, a, b):
    D = {x[0]: x for x in at}
    return math.dist(D[a][2:], D[b][2:])
rows = []
for c in conv:
    s = [x for x in scf if x[0] < c][-1]
    g = [x for x in B if x[0] < c][-1]
    rows.append((c, s[0], s[1], g[0], dist(g[1], 2, 4), dist(g[1], 25, 26), dist(g[1], 10, 27)))
E0 = rows[0][2]
print('idx | conv_line | SCF_line | E(Eh) | dE(kcal) | R(2,4) | R(25,26) | O10-H27 | geom_hdr')
for k, r in enumerate(rows, 1):
    print('%2d | %7d | %7d | %.9f | %+7.2f | %.4f | %.4f | %.4f | %d' % (k, r[0], r[1], r[2], (r[2] - E0) * 627.509474, r[4], r[5], r[6], r[3]))
print('last big step line:', [l for l in L if 'on scan point' in l][-1].strip())
