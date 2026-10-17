# post-freeze asset: ts_0019 (job 1069) terminal read-out + last-frame geometry (read-only)
import numpy as np
from rdkit import Chem
PT = Chem.GetPeriodicTable(); K = 627.5095; E1028 = -939.312626605
p = "/home/ly/Cloudra-mechanism-agent/ts/ts_0019/jobs/declaration_0001/ts_opt/refine.log"
ls = open(p).read().splitlines()
print("lines", len(ls))
for i, l in enumerate(ls, 1):
    if 'Error termination' in l or ('Normal termination' in l):
        print("TERM L%d: %s" % (i, l.strip()))
scf = [(i + 1, l) for i, l in enumerate(ls) if 'SCF Done' in l]
print("SCF count", len(scf))
for n, l in scf[-3:]:
    print("  L%d %s" % (n, l.strip()))
Elast = float(scf[-1][1].split('=')[1].split()[0])
print("last SCF %.9f  dE vs 1028 = %+0.4f" % (Elast, (Elast - E1028) * K))
low = min(scf, key=lambda t: float(t[1].split('=')[1].split()[0]))
print("lowest SCF L%d %.9f  dE vs 1028 = %+0.4f" % (low[0], float(low[1].split('=')[1].split()[0]), (float(low[1].split('=')[1].split()[0]) - E1028) * K))
h = [j for j in range(len(ls)) if 'Standard orientation' in ls[j]][-1]
d = [k for k in range(h, h + 10) if ls[k].strip().startswith('-----')]
a = []; k = d[1] + 1
while not ls[k].strip().startswith('-----'):
    q = ls[k].split(); a.append((int(q[1]), float(q[3]), float(q[4]), float(q[5]))); k += 1
assert len(a) == 41
X = np.array([[x, y, z] for _, x, y, z in a])
dd = lambda u, v: float(np.linalg.norm(X[u-1] - X[v-1]))
el = lambda i: PT.GetElementSymbol(a[i-1][0])
print("last frame hdr L%d atomL%d  element order check: %s" % (h + 1, d[1] + 1, ''.join(el(i) for i in range(1, 42))))
for pair in [(2, 4), (2, 25), (25, 26), (10, 26), (4, 26), (10, 27), (4, 27), (2, 11), (2, 10)]:
    print("  R(%d%s-%d%s) = %.4f" % (pair[0], el(pair[0]), pair[1], el(pair[1]), dd(*pair)))
for hh in (26, 27):
    near = sorted([(dd(hh, k), k, el(k)) for k in range(1, 42) if a[k-1][0] > 1 and k != hh])[:3]
    print("  H%d nearest heavy: %s" % (hh, ", ".join("%s%d %.4f" % (s, k, r) for r, k, s in near)))
