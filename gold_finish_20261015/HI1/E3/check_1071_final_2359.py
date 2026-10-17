import math
P = 'ts/ts_0020/jobs/declaration_0001/ts_opt/refine.log'
L = open(P).read().splitlines()
print('lines', len(L))
scf = [(i+1, float(l.split('=')[1].split()[0])) for i, l in enumerate(L) if 'SCF Done' in l]
mn = min(scf, key=lambda x: x[1]); K = 627.509474
print('SCF count', len(scf), 'min L%d = %.9f  last L%d = %.9f' % (mn[0], mn[1], scf[-1][0], scf[-1][1]))
print('vs 1028 = %+.4f ; vs P = %+.4f' % ((mn[1]+939.312626605)*K, (mn[1]+939.319540184)*K))
for pat in ['Optimization completed', 'Stationary point found', 'Normal termination of Gaussian', 'Error termination via', 'Number of steps exceeded']:
    hits = [(i+1, l.strip()[:70]) for i, l in enumerate(L) if pat in l]
    print(pat, '->', len(hits), hits[-1] if hits else '')
# last full geometry block
def blocks(L):
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
B = blocks(L)
full = [b for b in B if len(b[1]) == 41]
print('blocks', len(B), 'full41', len(full), 'last hdr', full[-1][0])
at = full[-1][1]
def d(a, b):
    D = {x[0]: x for x in at}
    return math.dist(D[a][2:], D[b][2:])
print('C2-N4=%.4f C2-O25=%.4f O25-H26=%.4f O25-H27=%.4f O10-H27=%.4f O28-H24=%.4f N4-H27=%.4f N4-H26=%.4f R(1,29)=%.4f R(2,18)=%.4f' % (
    d(2,4), d(2,25), d(25,26), d(25,27), d(10,27), d(28,24), d(4,27), d(4,26), d(1,29), d(2,18)))
