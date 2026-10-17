import math
def blocks(path):
    L = open(path).read().splitlines()
    out = []
    for i, l in enumerate(L):
        if 'Standard orientation' in l:
            atoms = []
            j = i + 5
            while j < len(L) and not L[j].strip().startswith('-----'):
                parts = L[j].split()
                if len(parts) == 6:
                    atoms.append((int(parts[0]), int(parts[1]), float(parts[3]), float(parts[4]), float(parts[5])))
                j += 1
            out.append((i + 1, atoms))
    return L, out

def dist(at, a, b):
    A = {x[0]: x for x in at}
    return math.dist(A[a][2:], A[b][2:]) * 0.529177

for p in ['HI1/E2/scan_1d/build/E2_1D_scan_cont1.log', 'HI1/E2/scan_1d/build/E2_1D_scan.log']:
    L, B = blocks(p)
    print('===', p, 'blocks =', len(B))
    for hdr, at in B[:2] + B[-3:]:
        print('  hdr', hdr, 'natoms', len(at), 'R(1,29)=%.4f' % dist(at, 1, 29), 'Z1=%d Z29=%d Z28=%d Z24=%d Z11=%d' % (
            at[0][1], at[28][1], at[27][1], at[23][1], at[10][1]))
