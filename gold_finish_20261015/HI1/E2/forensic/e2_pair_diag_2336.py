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

def dst(at, a, b):
    A = {x[0]: x for x in at}
    return math.dist(A[a][2:], A[b][2:])

L1, B1 = blocks('HI1/E2/scan_1d/build/E2_1D_scan.log')
L2, B2 = blocks('HI1/E2/scan_1d/build/E2_1D_scan_cont1.log')
f = B1[0][1]; l = B1[-1][1]
print('1075 first hdr', B1[0][0], 'last hdr', B1[-1][0])
print('pair scan candidates (|d_first-d_last| > 0.5):')
for j in range(2, 42):
    a, b = dst(f, 1, j), dst(l, 1, j)
    if abs(a - b) > 0.5 or a > 3.5:
        print('   d(1,%d): first %.4f  last %.4f  delta %.4f' % (j, a, b, b - a))
print('d(1,29): first %.4f last %.4f' % (dst(f,1,29), dst(l,1,29)))
c = B2[0][1]
print('cont1 first hdr', B2[0][0])
for j in (29, 28, 24, 11):
    print('   cont1 d(1,%d)=%.4f' % (j, dst(c, 1, j)) if j != 29 else '   cont1 d(1,29)=%.4f' % dst(c,1,29))
print('cont1 d(28,24)=%.4f d(11,24)=%.4f' % (dst(c,28,24), dst(c,11,24)))
print('1075 last d(28,24)=%.4f d(11,24)=%.4f' % (dst(l,28,24), dst(l,11,24)))
print('1075 first d(28,24)=%.4f d(11,24)=%.4f' % (dst(f,28,24), dst(f,11,24)))
grep = [i+1 for i, x in enumerate(L1) if 'B(' in x and 'R1' in x]
print('1075 R1 lines', grep[:3])
for i in [i for i, x in enumerate(L1) if 'R1' in x][:3]:
    print('   ', L1[i].strip()[:100])
