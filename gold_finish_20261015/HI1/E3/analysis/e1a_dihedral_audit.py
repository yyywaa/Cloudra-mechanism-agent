# post-freeze asset: E1a (job 1072) dihedral audit, read-only. Cross-product convention self-tested (cis=0, trans=180).
import numpy as np
from rdkit import Chem
PT = Chem.GetPeriodicTable()
p = "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split/E1A_constrained_scan_R2692_2192_stepneg.log"
ls = open(p).read().splitlines()

def dih(p1, p2, p3, p4):
    b1 = p2 - p1; b2 = p3 - p2; b3 = p4 - p3
    n1 = np.cross(b1, b2); n2 = np.cross(b2, b3)
    m = np.cross(n1, b2 / np.linalg.norm(b2))
    x = float(np.dot(n1, n2)); y = float(np.dot(m, n2))
    return float(np.degrees(np.arctan2(y, x)))

# self-tests
a = np.array([0., 0., 0.]); b = np.array([1., 0., 0.]); c0 = np.array([1., 1., 0.])
cis = np.array([0., 1., 0.])    # same side -> 0
tr = np.array([0., 1., 2.])      # -> 90?  build explicit trans below
d_cis = dih(a, b, c0, np.array([2., 1., 0.]))
d_trans = dih(a, b, np.array([1., 0., 0.]), np.array([2., -0., 0.]))  # degenerate
# explicit: butane-like
p1 = np.array([0., 0., 0.]); p2 = np.array([1., 0., 0.]); p3 = np.array([1.5, 1.0, 0.])
p4_cis = np.array([2.5, 1.0, 0.]); p4_trans = np.array([2.5, -0.2, 1.2])
print("ST cis -> %.3f (expect ~0)" % dih(p1, p2, p3, p4_cis))
print("ST trans(planar) -> %.3f (expect ~180)" % dih(p1, p2, p3, np.array([2.4, -1.0, 0.])))

oc = [i for i, l in enumerate(ls) if 'Optimization completed' in l]
def frame_before(idx):
    h = [j for j in range(idx) if 'Standard orientation' in ls[j]][-1]
    d = [k for k in range(h, h + 10) if ls[k].strip().startswith('-----')]
    at = []; k = d[1] + 1
    while not ls[k].strip().startswith('-----'):
        q = ls[k].split(); at.append((int(q[1]), float(q[3]), float(q[4]), float(q[5]))); k += 1
    assert len(at) == 27
    return h + 1, at

pts = []
for n, i in enumerate(oc, 1):
    hdr, at = frame_before(i)
    X = np.array([[x, y, z] for _, x, y, z in at])
    j = [k for k in range(i) if 'SCF Done' in ls[k]][-1]
    E = float(ls[j].split('=')[1].split()[0])
    r2692 = float(np.linalg.norm(X[26-1] - X(0) if False else X[26-1] - X[1-1]))
    r2o = float(np.linalg.norm(X[2-1] - X[18-1]))
    pts.append((n, hdr, j + 1, E, X, r2o))
    print("sp%-2d hdr L%-6d SCF L%-6d E=%.9f R(2,18)=%.4f |tau(3,2,18,14)|=%.2f" % (n, hdr, j + 1, E, r2o, dih(X[3-1], X[2-1], X[18-1], X[14-1])))
print("element check 1..27:", ''.join(PT.GetElementSymbol(at[i-1][0]) for i in range(1, 28)))
print("atoms 3/2/18/14 =", PT.GetElementSymbol(at[2][0]), PT.GetElementSymbol(at[1][0]), PT.GetElementSymbol(at[17][0]), PT.GetElementSymbol(at[13][0]))
tau = [dih(q[4][3-1], q[4][2-1], q[4][18-1], q[4][14-1]) for q in pts]
print("tau list:", " ".join("%.2f" % t for t in tau))
print("tau sp1 -> sp_last : %.2f -> %.2f  delta=%.2f" % (tau[0], tau[-1], tau[-1] - tau[0]))
print("|tau| sp1 -> sp_last : %.2f -> %.2f  delta=%.2f" % (abs(tau[0]), abs(tau[-1]), abs(tau[-1]) - abs(tau[0])))
print("min|tau|=%.2f  max|tau|=%.2f  max-min=%.2f" % (min(abs(t) for t in tau), max(abs(t) for t in tau), max(abs(t) for t in tau) - min(abs(t) for t in tau)))
