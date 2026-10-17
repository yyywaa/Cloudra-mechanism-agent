# post-freeze asset (non-delivery evidence): HI1 coordinator double-sign of job 1077 (E1a cont1) 6-point table
# read-only: parses E1A_scan_cont1_C2N18.log; no writes; no submission
import numpy as np, datetime
K = 627.5095
LOG = "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split/E1A_scan_cont1_C2N18.log"
RC27 = -593.934532807
ls = open(LOG).read().splitlines()

def kab(P, Q):
    Pc = P - P.mean(0); Qc = Q - Q.mean(0)
    H = Pc.T @ Qc; U, S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1., 1., d]) @ U.T
    dev = np.linalg.norm((R @ Pc.T).T - Qc, axis=1)
    return float(np.sqrt((dev**2).mean())), float(dev.max()), float(np.linalg.det(R))

rng = np.random.default_rng(77); X = rng.normal(size=(12, 3)); th = 0.6
Rm = np.array([[np.cos(th), -np.sin(th), 0], [np.sin(th), np.cos(th), 0], [0, 0, 1]]); t = np.array([0.4, 1.1, -0.9])
print("SC(i) rot+trans -> %.3e" % kab(X, X @ Rm.T + t)[0])
print("SC(ii) mirror -> %.6f" % kab(X, X * np.array([1, -1, 1]))[0])
print("SC(iii) copy -> %.3e" % kab(X, X)[0])

def frame_before(idx):
    h = [j for j in range(idx) if 'Standard orientation' in ls[j]][-1]
    d = [k for k in range(h, h + 12) if ls[k].strip().startswith('-----')]
    rows = []; k = d[1] + 1
    while not ls[k].strip().startswith('-----'):
        q = ls[k].split(); rows.append((int(q[1]), float(q[3]), float(q[4]), float(q[5]))); k += 1
    assert len(rows) == 27, len(rows)
    assert ls[k].strip().startswith('-----')
    return h + 1, d[1] + 1, rows

oc = [i for i, l in enumerate(ls) if 'Optimization completed' in l]
print("converged points:", len(oc))
pts = []
for n, i in enumerate(oc, 1):
    hdr, ab, rows = frame_before(i)
    Xg = np.array([[x, y, z] for _, x, y, z in rows])
    j = [k for k in range(i) if 'SCF Done' in ls[k]][-1]
    E = float(ls[j].split('=')[1].split()[0])
    d = lambda u, v: float(np.linalg.norm(Xg[u-1] - Xg[v-1]))
    pts.append(dict(n=n, opt=i+1, hdr=hdr, ab=ab, scf=j+1, E=E, X=Xg, Z=[z for z, _, _, _ in rows],
                    r218=d(2,18), r327=d(3,27), r1827=d(18,27), r1319=d(13,19), r23=d(2,3)))
els = [pts[0]['Z'][i] for i in range(27)]
print("elements (Z) seq:", els)
print("heavy atoms:", sum(1 for z in els if z != 1))
E1 = pts[0]['E']
for q in pts:
    print("pt%d OPT L%d hdr L%d SCF L%d E=%.9f  R(2,18)=%.4f R(3,27)=%.4f R(18,27)=%.4f R(13,19)=%.4f C2-O3=%.4f  dE_vs_RC27=%+7.2f dE_vs_pt1=%+7.2f" % (
        q['n'], q['opt'], q['hdr'], q['scf'], q['E'], q['r218'], q['r327'], q['r1827'], q['r1319'], q['r23'],
        (q['E'] - RC27) * K, (q['E'] - E1) * K))
heavy = [i for i in range(27) if els[i] != 1]
for k in range(len(pts) - 1):
    r, mx, det = kab(pts[k]['X'][heavy], pts[k+1]['X'][heavy])
    print("Kabsch pt%d->pt%d heavy%d rms=%.4f max=%.4f det=%+.3f %s" % (k+1, k+2, len(heavy), r, mx, det, "*** >0.3" if r > 0.3 else ""))
dE = [(q['E'] - E1) * K for q in pts]
mono = all(dE[i+1] > dE[i] for i in range(len(dE)-1))
print("monotone increasing vs pt1:", mono, "| values:", ["%+.2f" % v for v in dE])
print("R(18,27) range: %.4f - %.4f (H27 stays on N18 if <1.10)" % (min(q['r1827'] for q in pts), max(q['r1827'] for q in pts)))
print("termination lines:")
for i, l in enumerate(ls):
    if 'Normal termination' in l or 'Error termination' in l: print("  L%d : %s" % (i+1, l.strip()))
print("as of", datetime.datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z"), "| lines", len(ls))
