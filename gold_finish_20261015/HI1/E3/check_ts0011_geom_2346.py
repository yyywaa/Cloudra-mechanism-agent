import math
def blocks(path):
    L = open(path).read().splitlines()
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
    return L, out
L, B = blocks('ts/ts_0011/jobs/declaration_0004/ts_opt/refine.log')
print('blocks', len(B), 'natoms last', len(B[-1][1]))
scf = [(i + 1, float(l.split('=')[1].split()[0])) for i, l in enumerate(L) if 'SCF Done' in l]
print('SCF count', len(scf), 'last', scf[-1])
print('last conv/opt lines:')
for i, l in enumerate(L):
    if 'Optimization completed' in l or 'Stationary point found' in l:
        print('   L%d %s' % (i + 1, l.strip()[:80]))
def d(at, a, b):
    D = {x[0]: x for x in at}
    return math.dist(D[a][2:], D[b][2:])
at = B[-1][1]
print('ts_opt last block (hdr L%d): C2-N4=%.4f C2-O25=%.4f O25-H26=%.4f O25-H27=%.4f O10-H27=%.4f O28-H24=%.4f' % (
    B[-1][0], d(at,2,4), d(at,2,25), d(at,25,26), d(at,25,27), d(at,10,27), d(at,28,24)))
Lf, Bf = blocks('ts/ts_0011/jobs/declaration_0004/frequency/frequency.log')
atf = Bf[0][1]
print('freq first block (hdr L%d): C2-N4=%.4f C2-O25=%.4f O25-H26=%.4f O25-H27=%.4f O10-H27=%.4f O28-H24=%.4f' % (
    Bf[0][0], d(atf,2,4), d(atf,2,25), d(atf,25,26), d(atf,25,27), d(atf,10,27), d(atf,28,24)))
mx = max(math.dist(D1[2:], D2[2:]) for D1, D2 in zip(sorted(at), sorted(atf)))
print('per-atom max|delta| ts_opt_last vs freq_first = %.4f A' % mx)
