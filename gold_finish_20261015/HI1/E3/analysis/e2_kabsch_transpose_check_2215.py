# post-freeze asset: verify the "transposed rotation" hypothesis reproduces BOTH Kabsch value sets from the same 7 frames.
import numpy as np
p = "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan.log"
ls = open(p).read().splitlines()
oc = [i for i, l in enumerate(ls) if 'Optimization completed' in l]
fr = []
for i in oc:
    h = [j for j in range(i) if 'Standard orientation' in ls[j]][-1]
    d = [k for k in range(h, h + 10) if ls[k].strip().startswith('-----')]
    at = []; k = d[1] + 1
    while not ls[k].strip().startswith('-----'):
        q = ls[k].split(); at.append((int(q[1]), float(q[3]), float(q[4]), float(q[5]))); k += 1
    assert len(at) == 41
    fr.append((h + 1, at))
heavy = [i for i in range(41) if fr[0][1][i][0] > 1]

def kab_correct(P, Q):
    Pc = P - P.mean(0); Qc = Q - Q.mean(0)
    Hm = Pc.T @ Qc; U, S, Vt = np.linalg.svd(Hm)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1., 1., d]) @ U.T          # maps P -> Q
    dev = np.linalg.norm((R @ Pc.T).T - Qc, axis=1)
    return np.sqrt((dev ** 2).mean()), dev.max(), np.linalg.det(R)

def kab_transposed(P, Q):
    Pc = P - P.mean(0); Qc = Q - Q.mean(0)
    Hm = Pc.T @ Qc; U, S, Vt = np.linalg.svd(Hm)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1., 1., d]) @ U.T          # same R
    Rt = R.T                                       # WRONG use: apply transpose
    dev = np.linalg.norm((Rt @ Pc.T).T - Qc, axis=1)
    return np.sqrt((dev ** 2).mean()), dev.max()

print("hdr:", [f[0] for f in fr])
print("pair  correct(rms,max)     transposed(rms,max)")
for k in range(len(fr) - 1):
    A = np.array([[x, y, z] for _, x, y, z in fr[k][1]])[heavy]
    B = np.array([[x, y, z] for _, x, y, z in fr[k + 1][1]])[heavy]
    r1, m1, det = kab_correct(A, B)
    r2, m2 = kab_transposed(A, B)
    print("%d->%d  %.4f  %.4f   |  %.4f  %.4f" % (k + 1, k + 2, r1, m1, r2, m2))
