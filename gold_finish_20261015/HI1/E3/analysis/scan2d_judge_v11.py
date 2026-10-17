# post-freeze asset (non-delivery evidence): 1074 6x6 grid judge v11
# - grid mapping scan# = 6*(col-1) + row ; row = R(2,4) index (1.4248 + 0.2*(row-1)) ; col = R(25,26) index (0.9693 + 0.25*(col-1))
# - converged points only (Optimization completed) ; in-progress point geometry probed separately
# - symmetric criterion (R137): one axis local max AND other axis local min ; boundary rows/cols never candidates
import numpy as np
from rdkit import Chem
PT = Chem.GetPeriodicTable(); K = 627.5095
p = "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/runs/e3b_scan2d_c2n4_o25h26.log"
ls = open(p).read().splitlines()

def kab(P, Q):
    Pc = P - P.mean(0); Qc = Q - Q.mean(0)
    H = Pc.T @ Qc; U, S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1., 1., d]) @ U.T
    dev = np.linalg.norm((R @ Pc.T).T - Qc, axis=1)
    return float(np.sqrt((dev**2).mean())), float(dev.max()), float(np.linalg.det(R))

rng = np.random.default_rng(2026); X = rng.normal(size=(20, 3)); th = 0.85
Rm = np.array([[np.cos(th), -np.sin(th), 0], [np.sin(th), np.cos(th), 0], [0, 0, 1]]); t = np.array([1.2, -0.7, 2.1])
print("SC(i) rot+trans -> %.3e" % kab(X, X @ Rm.T + t)[0])
print("SC(ii) mirror(allowed) -> %.6f" % kab(X, X * np.array([1, -1, 1]))[0])
print("SC(iii) identical copy -> %.3e" % kab(X, X)[0])

def frame_before(idx):
    h = [j for j in range(idx) if 'Standard orientation' in ls[j]][-1]
    d = [k for k in range(h, h + 10) if ls[k].strip().startswith('-----')]
    a = []; k = d[1] + 1
    while not ls[k].strip().startswith('-----'):
        q = ls[k].split(); a.append((int(q[1]), float(q[3]), float(q[4]), float(q[5]))); k += 1
    assert len(a) == 41
    assert ls[k].strip().startswith('-----')
    return h, d[1] + 1, a

oc = [i for i, l in enumerate(ls) if 'Optimization completed' in l]
pts = []
for n, i in enumerate(oc, 1):
    h, ab, a = frame_before(i)
    Xg = np.array([[x, y, z] for _, x, y, z in a])
    j = [k for k in range(i) if 'SCF Done' in ls[k]][-1]
    E = float(ls[j].split('=')[1].split()[0])
    d = lambda u, v: float(np.linalg.norm(Xg[u-1] - Xg[v-1]))
    hn = min([(d(26, k), k + 1, PT.GetElementSymbol(a[k-1][0])) for k in range(1, 42) if a[k-1][0] > 1 and k != 26])
    pts.append(dict(n=n, opt=i + 1, hdr=h + 1, ab=ab, scf=j + 1, E=E, X=Xg, a=a,
                    R24=d(2, 4), R2526=d(25, 26), R426=d(4, 26), R1027=d(10, 27), R225=d(2, 25), hn=hn))
E0 = pts[0]['E']; heavy = [i for i in range(41) if pts[0]['a'][i][0] > 1]
print("heavy", len(heavy), "converged", len(pts))
for q in pts:
    row = int(round((q['R24'] - 1.4248) / 0.2)) + 1
    col = int(round((q['R2526'] - 0.9693) / 0.25)) + 1
    q['row'], q['col'] = row, col
    print("pt%2d scan#%2d (row%d,col%d) OPT L%d hdr L%d SCF L%d E=%.9f dE=%+7.2f R(2,4)=%.4f R(25,26)=%.4f R(4,26)=%.4f R(10,27)=%.4f R(2,25)=%.4f H26near=%d%s %.4f" % (
        q['n'], q['n'], row, col, q['opt'], q['hdr'], q['scf'], q['E'], (q['E'] - E0) * K,
        q['R24'], q['R2526'], q['R426'], q['R1027'], q['R225'], q['hn'][1], q['hn'][2], q['hn'][0]))
for k in range(len(pts) - 1):
    r, mx, det = kab(pts[k]['X'][heavy], pts[k+1]['X'][heavy])
    print("Kabsch pt%d->pt%d heavy20 rms=%.4f max=%.4f det=%+.3f %s" % (k+1, k+2, r, mx, det, "*** >0.3" if r > 0.3 else ""))
grid = {(q['row'], q['col']): q for q in pts}
print("--- symmetric criterion (R137): interior rows 2-5, cols 2-5 ---")
any_cand = False
for (r0, c0), q in sorted(grid.items()):
    if not (2 <= r0 <= 5 and 2 <= c0 <= 5):
        continue
    nb = {'row-': (r0-1, c0), 'row+': (r0+1, c0), 'col-': (r0, c0-1), 'col+': (r0, c0+1)}
    if not all(k in grid for k in nb.values()):
        print("  (row%d,col%d) neighbours incomplete -> not judged" % (r0, c0)); continue
    E = q['E']
    along_row = 'max' if (E > grid[nb['row-']]['E'] and E > grid[nb['row+']]['E']) else ('min' if (E < grid[nb['row-']]['E'] and E < grid[nb['row+']]['E']) else 'monotone')
    along_col = 'max' if (E > grid[nb['col-']]['E'] and E > grid[nb['col+']]['E']) else ('min' if (E < grid[nb['col-']]['E'] and E < grid[nb['col+']]['E']) else 'monotone')
    kind = 'CANDIDATE(index-1)' if {along_row, along_col} == {'max', 'min'} else ('ridge(2 max)' if along_row == along_col == 'max' else ('basin(2 min)' if along_row == along_col == 'min' else 'none'))
    if 'CANDIDATE' in kind: any_cand = True
    print("  (row%d,col%d) R(2,4)=%.4f R(25,26)=%.4f dE=%+7.2f alongR24=%s alongR2526=%s -> %s" % (r0, c0, q['R24'], q['R2526'], (E - E0) * K, along_row, along_col, kind))
if not any_cand:
    print("  => 该 6x6 网格（当前已判读子集）未分辨出离散指标 1 的驻点；需扩窗或加密（不得写无 TS / 通道不存在）")
sp = [i for i, l in enumerate(ls) if 'on scan point' in l]
last = sp[-1]
cur = int(ls[last].split('on scan point')[1].split('out of')[0])
h, ab, a = frame_before(len(ls))
Xg = np.array([[x, y, z] for _, x, y, z in a])
j = [k for k in range(len(ls)) if 'SCF Done' in ls[k]][-1]
E = float(ls[j].split('=')[1].split()[0])
d = lambda u, v: float(np.linalg.norm(Xg[u-1] - Xg[v-1]))
hn = min([(d(26, k), k + 1, PT.GetElementSymbol(a[k-1][0])) for k in range(1, 42) if a[k-1][0] > 1 and k != 26])
print("--- in progress: scan#%d, last step line L%d: %s" % (cur, last + 1, ls[last].strip()))
print("    hdr L%d atomL%d SCF L%d E=%.9f dE=%+7.2f R(2,4)=%.4f R(25,26)=%.4f R(4,26)=%.4f R(10,27)=%.4f R(2,25)=%.4f H26near=%d%s %.4f" % (
    h + 1, ab, j + 1, E, (E - E0) * K, d(2, 4), d(25, 26), d(4, 26), d(10, 27), d(2, 25), hn[1], hn[2], hn[0]))
print("termination NL/EL:", sum(1 for l in ls if 'Normal termination' in l), sum(1 for l in ls if 'Error termination' in l))
