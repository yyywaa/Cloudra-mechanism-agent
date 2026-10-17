# post-freeze asset: independent double-sign of the 8-frame E2 table (pt8 proton metrics + 7->8 Kabsch)
import numpy as np
p = "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan.log"
ls = open(p).read().splitlines()
oc = [i for i, l in enumerate(ls) if 'Optimization completed' in l]
def frame(idx):
    h = [j for j in range(idx) if 'Standard orientation' in ls[j]][-1]
    d = [k for k in range(h, h + 10) if ls[k].strip().startswith('-----')]
    at = []; k = d[1] + 1
    while not ls[k].strip().startswith('-----'):
        q = ls[k].split(); at.append((int(q[1]), float(q[3]), float(q[4]), float(q[5]))); k += 1
    assert len(at) == 41
    j = [k for k in range(idx) if 'SCF Done' in ls[k]][-1]
    return h + 1, d[1] + 1, j + 1, float(ls[j].split('=')[1].split()[0]), np.array([[x, y, z] for _, x, y, z in at]), at
F = [frame(i) for i in oc]
print("frames", len(F))
for n, (hdr, ab, scf, E, X, at) in enumerate(F, 1):
    d = lambda u, v: float(np.linalg.norm(X[u-1] - X[v-1]))
    print("pt%-2d hdr L%-6d atomL L%-6d SCF L%-6d E=%.9f R(1,29)=%.4f R(28,24)=%.4f R(11,24)=%.4f R(2,4)=%.4f" % (
        n, hdr, ab, scf, E, d(1, 29), d(28, 24), d(11, 24), d(2, 4)))
heavy = [i for i in range(41) if F[0][5][i][0] > 1]
def kab(P, Q):
    Pc = P - P.mean(0); Qc = Q - Q.mean(0)
    H = Pc.T @ Qc; U, S, Vt = np.linalg.svd(H); dd = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1., 1., dd]) @ U.T
    dev = np.linalg.norm((R @ Pc.T).T - Qc, axis=1)
    return float(np.sqrt((dev ** 2).mean())), float(dev.max()), float(np.linalg.det(R))
print("pairs:", " ".join("%d->%d %.4f(max %.4f) " % (k+1, k+2, *kab(F[k][4][heavy], F[k+1][4][heavy])[:2]) for k in range(len(F)-1)))
print("termination NL/EL:", sum(1 for l in ls if 'Normal termination' in l), sum(1 for l in ls if 'Error termination' in l))
