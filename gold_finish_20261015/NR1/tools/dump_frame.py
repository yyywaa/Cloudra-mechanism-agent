#!/usr/bin/env python3
"""Print the geometry block immediately preceding a given line, with key internal coords."""
import sys, math
path, target = sys.argv[1], int(sys.argv[2])
L = open(path, errors='ignore').read().split('\n')
hdr = None
for i in range(target - 1, -1, -1):
    if 'orientation:' in L[i]:
        hdr = i; break
j = hdr + 5; el = []; co = []
while j < len(L) and '-----' not in L[j]:
    p = L[j].split()
    if len(p) >= 6:
        try:
            el.append(int(p[1])); co.append((float(p[3]), float(p[4]), float(p[5])))
        except ValueError:
            pass
    j += 1
print('geometry block at line', hdr + 1, 'natoms', len(co))
print('elements:', el)
for k, c in enumerate(co):
    print('  %2d %2d  %10.5f %10.5f %10.5f' % (k + 1, el[k], c[0], c[1], c[2]))
def d(a, b): return math.dist(co[a], co[b])
def ang(a, b, c):
    import numpy as np
    v1 = [co[a][k] - co[b][k] for k in range(3)]
    v2 = [co[c][k] - co[b][k] for k in range(3)]
    n1 = math.sqrt(sum(x * x for x in v1)); n2 = math.sqrt(sum(x * x for x in v2))
    return math.degrees(math.acos(sum(v1[k] * v2[k] for k in range(3)) / (n1 * n2)))
def dih(a, b, c, dd):
    import numpy as np
    p = [np.array(co[x]) for x in (a, b, c, dd)]
    b0 = p[0] - p[1]; b1 = p[2] - p[1]; b2 = p[3] - p[2]
    n1 = np.cross(b0, b1); n2 = np.cross(b1, b2)
    m = np.cross(n1, b1 / np.linalg.norm(b1))
    x = np.dot(n1, n2); y = np.dot(m, n2)
    return math.degrees(math.atan2(y, x))
print('r(O1-H4)=%.4f r(H4-O8)=%.4f r(O1-O8)=%.4f r(C6-O8)=%.4f' % (d(0, 3), d(3, 7), d(0, 7), d(5, 7)))
print('angle(O1-H4-O8)=%.2f  angle(H2-O1-H4)=%.2f  angle(H3-O1-H4)=%.2f' % (ang(0, 3, 7), ang(1, 0, 3), ang(2, 0, 3)))
print('dih(H2-O1-H4-O8)=%.2f  dih(H3-O1-H4-O8)=%.2f' % (dih(1, 0, 3, 7), dih(2, 0, 3, 7)))
print('r(O1-H2)=%.4f r(O1-H3)=%.4f' % (d(0, 1), d(0, 2)))
