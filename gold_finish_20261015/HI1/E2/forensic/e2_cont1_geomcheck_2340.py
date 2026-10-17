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

def get(path, hdrline):
    L, B = blocks(path)
    hit = [b for b in B if b[0] == hdrline]
    assert hit, 'hdr %d not found' % hdrline
    at = hit[0][1]
    assert len(at) == 41, len(at)
    return at

def kabsch_rmsd(P, Q):
    n = len(P)
    cp = [sum(p[k] for p in P) / n for k in range(3)]
    cq = [sum(q[k] for q in Q) / n for k in range(3)]
    Pc = [[p[k] - cp[k] for k in range(3)] for p in P]
    Qc = [[q[k] - cq[k] for k in range(3)] for q in Q]
    H = [[sum(Pc[i][a] * Qc[i][b] for i in range(n)) for b in range(3)] for a in range(3)]
    # SVD of 3x3 via numpy-free: use Jacobi on H^T H
    import itertools
    # simple: use numpy if available
    try:
        import numpy as np
    except ImportError:
        return None
    Hn = np.array(H)
    U, S, Vt = np.linalg.svd(Hn)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    D = np.diag([1.0, 1.0, d])
    R = Vt.T @ D @ U.T
    Pn = np.array(Pc); Qn = np.array(Qc)
    Pr = (R @ Pn.T).T
    diff = Pr - Qn
    dn = np.linalg.norm(diff, axis=1)
    rms = math.sqrt(float((dn ** 2).sum()) / n)
    return rms, float(dn.max()), int(dn.argmax()) + 1, float(np.linalg.det(R))

A = get('HI1/E2/scan_1d/build/E2_1D_scan.log', 85370)          # 主扫 pt8 收敛帧
Bc = get('HI1/E2/scan_1d/build/E2_1D_scan_cont1.log', 701)     # cont1 输入几何
print('element seq identical:', [a[1] for a in A] == [b[1] for b in Bc])
print('natoms', len(A), len(Bc))
P = [a[2:] for a in A]; Q = [b[2:] for b in Bc]
P20 = [a[2:] for a in A if a[1] != 1]; Q20 = [b[2:] for b in Bc if b[1] != 1]
print('heavy count', len(P20))
r20 = kabsch_rmsd(P20, Q20); r41 = kabsch_rmsd(P, Q)
print('heavy20 Kabsch rmsd/max/worst/det = %.4f / %.4f / %d / %.6f' % r20)
print('all41   Kabsch rmsd/max/worst/det = %.4f / %.4f / %d / %.6f' % r41)
# self-tests
import numpy as np
rot = np.array([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
tt = np.array([3.0, -2.0, 0.5])
P0 = np.array(P20); P1 = (rot @ P0.T).T + tt
print('self-test rot+trans (expect 0): %.3e' % kabsch_rmsd([list(x) for x in P0], [list(x) for x in P1])[0])
Pm = P0 * np.array([-1.0, 1.0, 1.0])
print('self-test mirror  (expect >0): %.4f det=%.3f' % (kabsch_rmsd([list(x) for x in P0], [list(x) for x in Pm])[0], kabsch_rmsd([list(x) for x in P0], [list(x) for x in Pm])[3]))
print('self-test copy    (expect 0): %.3e' % kabsch_rmsd([list(x) for x in P0], [list(x) for x in P0])[0])
def d(a, b, at):
    D = {x[0]: x for x in at}
    return math.dist(D[a][2:], D[b][2:])
print('pt8  R(1,29)=%.4f R(28,24)=%.4f R(11,24)=%.4f' % (d(1,29,A), d(28,24,A), d(11,24,A)))
print('cont1 R(1,29)=%.4f R(28,24)=%.4f R(11,24)=%.4f' % (d(1,29,Bc), d(28,24,Bc), d(11,24,Bc)))
