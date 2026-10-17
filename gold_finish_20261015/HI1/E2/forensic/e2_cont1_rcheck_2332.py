import math, sys
p = 'HI1/E2/scan_1d/build/E2_1D_scan_cont1.log'
L = open(p).read().splitlines()

def blocks(L):
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
    return out

B = blocks(L)
scf = [(i + 1, l.strip()[:76]) for i, l in enumerate(L) if 'SCF Done' in l]
stat = [i + 1 for i, l in enumerate(L) if 'Stationary point found' in l]
print('SCF Done count =', len(scf))
for x in scf[:4]:
    print('  SCF', x)
print('Stationary point found lines =', stat)
hdr, at = [x for x in B if x[0] < stat[0]][-1]
print('geom block hdr line =', hdr, ' natoms =', len(at))
A = {x[0]: x for x in at}
def d(a, b):
    return math.dist(A[a][2:], A[b][2:]) * 0.529177
print('R(1,29)=%.4f  R(28,24)=%.4f  R(11,24)=%.4f' % (d(1,29), d(28,24), d(11,24)))
print('E(pt1) - E(8frame pt8) = %.3e Eh = %.3e kcal/mol' % (-939.297687579 - (-939.297687588), (-939.297687579 - (-939.297687588)) * 627.509474))
