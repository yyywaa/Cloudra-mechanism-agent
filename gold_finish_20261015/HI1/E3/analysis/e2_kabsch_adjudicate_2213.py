# post-freeze asset: E2 adjacent-point Kabsch adjudication (read-only). Prints frame block headers, atom sets, BOTH normalizations, det.
import numpy as np
from rdkit import Chem
PT = Chem.GetPeriodicTable()
p = "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan.log"
ls = open(p).read().splitlines()

def kab(P, Q):
    Pc = P - P.mean(0); Qc = Q - Q.mean(0)
    H = Pc.T @ Qc; U, S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1., 1., d]) @ U.T
    dev = np.linalg.norm((R @ Pc.T).T - Qc, axis=1)
    return dev, float(np.linalg.det(R))

rng = np.random.default_rng(2026); X0 = rng.normal(size=(20, 3)); th = 0.85
Rm = np.array([[np.cos(th), -np.sin(th), 0], [np.sin(th), np.cos(th), 0], [0, 0, 1]]); t = np.array([1.2, -0.7, 2.1])
print("ST rot+trans rms=%.3e" % np.sqrt((kab(X0, X0 @ Rm.T + t)[0] ** 2).mean()))
print("ST mirror rms=%.6f" % np.sqrt((kab(X0, X0 * np.array([1, -1, 1]))[0] ** 2).mean()))
print("ST copy rms=%.3e" % np.sqrt((kab(X0, X0)[0] ** 2).mean()))

oc = [i for i, l in enumerate(ls) if 'Optimization completed' in l]
print("converged count:", len(oc))
frames = []
for n, i in enumerate(oc, 1):
    h = [j for j in range(i) if 'Standard orientation' in ls[j]][-1]
    d = [k for k in range(h, h + 10) if ls[k].strip().startswith('-----')]
    at = []; k = d[1] + 1
    while not ls[k].strip().startswith('-----'):
        q = ls[k].split(); at.append((int(q[1]), float(q[3]), float(q[4]), float(q[5]))); k += 1
    assert len(at) == 41
    j = [k for k in range(i) if 'SCF Done' in ls[k]][-1]
    E = float(ls[j].split('=')[1].split()[0])
    frames.append(dict(n=n, hdr=h + 1, atL=d[1] + 1, scf=j + 1, E=E, at=at))
    print("pt%d hdr L%d atomL%d SCF L%d E=%.9f" % (n, h + 1, d[1] + 1, j + 1, E))
heavy = [i for i in range(41) if frames[0]['at'][i][0] > 1]
print("heavy count", len(heavy), "| elements:", ''.join(PT.GetElementSymbol(frames[0]['at'][i][0]) for i in range(41)))
allat = list(range(41))
print("\n--- fit=heavy20 eval=heavy20 ---")
print("pair  rms(sqrt(1/N))  rms(sqrt(1/3N))  mean|d|  max|d|  det")
for k in range(len(frames) - 1):
    A = np.array([[x, y, z] for _, x, y, z in frames[k]['at']])[heavy]
    B = np.array([[x, y, z] for _, x, y, z in frames[k + 1]['at']])[heavy]
    dev, det = kab(A, B)
    print("%d->%d  %.4f  %.4f  %.4f  %.4f  %+.3f" % (k + 1, k + 2, np.sqrt((dev ** 2).mean()), np.sqrt((dev ** 2).sum() / (3 * len(dev))), float(np.abs(dev).mean()), float(dev.max()), det))
print("\n--- fit=all41 eval=heavy20 (rotation from all atoms, deviation on heavy) ---")
for k in range(len(frames) - 1):
    A41 = np.array([[x, y, z] for _, x, y, z in frames[k]['at']]); B41 = np.array([[x, y, z] for _, x, y, z in frames[k + 1]['at']])
    Ac = A41 - A41.mean(0); Bc = B41 - B41.mean(0)
    H = Ac.T @ Bc; U, S, Vt = np.linalg.svd(H); d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1., 1., d]) @ U.T
    devH = np.linalg.norm((R @ (A41[heavy] - A41.mean(0)).T).T - (B41[heavy] - B41.mean(0)), axis=1)
    devA = np.linalg.norm((R @ Ac.T).T - Bc, axis=1)
    print("%d->%d  heavy-eval %.4f (max %.4f) ; all41 %.4f" % (k + 1, k + 2, np.sqrt((devH ** 2).mean()), devH.max(), np.sqrt((devA ** 2).mean())))
