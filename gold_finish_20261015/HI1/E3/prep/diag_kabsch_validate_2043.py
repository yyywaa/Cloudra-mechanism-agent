import math, re
import numpy as np

def last_geom(path):
    lines = open(path, 'rb').read().decode('utf-8', 'replace').splitlines()
    start = None
    for i, ln in enumerate(lines):
        if 'Standard orientation:' in ln or 'Input orientation:' in ln:
            start = i
    k = start + 5
    atoms = []
    while k < len(lines):
        ln = lines[k]
        if ln.strip().startswith('-----'):
            break
        p = ln.split()
        if len(p) == 6 and p[0].isdigit():
            atoms.append((int(p[1]), float(p[3]), float(p[4]), float(p[5])))
        elif p:
            raise SystemExit('bad line %d' % (k+1))
        k += 1
    return atoms, start+1

def kabsch(A, B):
    A = np.asarray(A, float); B = np.asarray(B, float)
    ca = A.mean(0); cb = B.mean(0)
    H = (A-ca).T @ (B-cb)
    U, S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    if d == 0: d = 1.0
    R = Vt.T @ np.diag([1.0, 1.0, d]) @ U.T
    devs = np.linalg.norm((A-ca) @ R.T - (B-cb), axis=1)
    return float(np.sqrt((devs**2).mean())), float(devs.max()), float(np.linalg.det(R))

# ---------- 1) synthetic validation ----------
np.random.seed(0)
A = np.random.rand(8, 3) * 3.0
th = 0.7; axis = np.array([0.3, -0.5, 0.81]); axis /= np.linalg.norm(axis)
K = np.array([[0,-axis[2],axis[1]],[axis[2],0,-axis[0]],[-axis[1],axis[0],0]])
Rtrue = np.eye(3) + math.sin(th)*K + (1-math.cos(th))*(K@K)
B = A @ Rtrue.T + np.array([1.5, -2.0, 0.3])
r, m, det = kabsch(A, B)
print('SYNTH rotation+translation: RMSD=%.8f max=%.8f det=%+.3f (expect 0/0/+1)' % (r, m, det))
Bm = A * np.array([1.0, 1.0, -1.0])   # mirror
r2, m2, det2 = kabsch(A, Bm)
print('SYNTH mirror (must NOT be driven to 0): RMSD=%.4f det=%+.3f' % (r2, det2))

# ---------- 2) real structures ----------
f19 = 'ts/ts_0019/jobs/declaration_0001/ts_opt/refine.log'
fp  = 'gold_finish_20261015/HI1/E3/runs/P_e3b/P_optfreq.log'
f28 = 'gold_finish_20261015/HI1/E3/runs/interm_c160/interm_c160_optfreq.log'
a19, s19 = last_geom(f19); ap, sp = last_geom(fp); a28, s28 = last_geom(f28)
print('blocks: 1069 L%d (%d atoms), P L%d (%d), 1028 L%d (%d)' % (s19, len(a19), sp, len(ap), s28, len(a28)))
for nm, a, b in (('1069 vs P', a19, ap), ('1069 vs 1028', a19, a28), ('P vs 1028', ap, a28)):
    assert [x[0] for x in a] == [x[0] for x in b], 'element order mismatch ' + nm
    hv = [i for i in range(len(a)) if a[i][0] != 1]
    Aa = [a[i][1:] for i in hv]; Bb = [b[i][1:] for i in hv]
    rh, mh, dh = kabsch(Aa, Bb)
    ra, ma, da = kabsch([x[1:] for x in a], [x[1:] for x in b])
    print('%s: heavy n=%d RMSD=%.4f max=%.4f det=%+.2f | all41 RMSD=%.4f' % (nm, len(hv), rh, mh, dh, ra))
