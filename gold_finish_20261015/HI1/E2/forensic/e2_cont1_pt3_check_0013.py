import math, numpy as np
P = 'HI1/E2/scan_1d/build/E2_1D_scan_cont1.log'
L = open(P).read().splitlines()
print('lines', len(L))
scf = [(i+1, float(l.split('=')[1].split()[0])) for i, l in enumerate(L) if 'SCF Done' in l]
conv = [i+1 for i, l in enumerate(L) if 'Optimization completed' in l]
sp = [i+1 for i, l in enumerate(L) if 'Stationary point found' in l]
print('SCF', len(scf), 'conv', conv, 'SP', sp)
def blocks(L):
    out = []
    for i, l in enumerate(L):
        if 'Standard orientation' in l:
            at = []; j = i + 5
            while j < len(L) and not L[j].strip().startswith('-----'):
                p = L[j].split()
                if len(p) == 6:
                    at.append((int(p[0]), int(p[1]), float(p[3]), float(p[4]), float(p[5])))
                j += 1
            out.append((i + 1, at))
    return out
B = blocks(L)
frames = []
for c in conv:
    g = [b for b in B if b[0] < c][-1]; s = [x for x in scf if x[0] < c][-1]
    frames.append((g, s, c))
for k, (g, s, c) in enumerate(frames, 1):
    D = {x[0]: x for x in g[1]}
    print('pt%d conv L%d | SCF L%d = %.9f | hdr L%d | R(1,29)=%.4f R(2,4)=%.4f R(11,24)=%.4f' % (
        k, c, s[0], s[1], g[0], math.dist(D[1][2:], D[29][2:]), math.dist(D[2][2:], D[4][2:]), math.dist(D[11][2:], D[24][2:])))
E1 = frames[0][1][1]
for k, (g, s, c) in enumerate(frames, 1):
    print('pt%d dE vs cont1 pt1 = %+.4f ; vs 原 pt1 = %+.4f' % (k, (s[1]-E1)*627.509474, (s[1]+939.308205969)*627.509474))
def kab_map(X, Y, mask):
    idx = [x[0] for x in X if mask(x)]
    Pm = np.array([[x[2], x[3], x[4]] for x in X if mask(x)]); Qm = np.array([[y[2], y[3], y[4]] for y in Y if mask(y)])
    Pc = Pm - Pm.mean(0); Qc = Qm - Qm.mean(0)
    U, S, Vt = np.linalg.svd(Pc.T @ Qc)
    d = np.sign(np.linalg.det(Vt.T @ U.T)); R = Vt.T @ np.diag([1,1,d]) @ U.T
    dn = np.linalg.norm((R @ Pc.T).T - Qc, axis=1)
    return math.sqrt(float((dn**2).sum())/len(Pm)), float(dn.max()), idx[int(dn.argmax())]
if len(frames) >= 3:
    print('pt2->pt3 heavy20 rms/max/worst = %.4f / %.4f / %d' % kab_map(frames[1][0][1], frames[2][0][1], lambda x: x[1] != 1))
    print('pt2->pt3 all41  rms/max/worst = %.4f / %.4f / %d' % kab_map(frames[1][0][1], frames[2][0][1], lambda x: True))
A = frames[1][0][1]
P0 = np.array([[x[2], x[3], x[4]] for x in A if x[1] != 1])
rot = np.array([[0.,-1.,0.],[1.,0.,0.],[0.,0.,1.]]); tt = np.array([1.,2.,-1.])
def kn(P, Q):
    Pc = P - P.mean(0); Qc = Q - Q.mean(0)
    U, S, Vt = np.linalg.svd(Pc.T @ Qc); d = np.sign(np.linalg.det(Vt.T @ U.T)); R = Vt.T @ np.diag([1,1,d]) @ U.T
    dn = np.linalg.norm((R @ Pc.T).T - Qc, axis=1); return math.sqrt(float((dn**2).sum())/len(P))
print('self r+t=%.3e mirror=%.4f copy=%.3e' % (kn(P0,(rot@P0.T).T+tt), kn(P0, P0*np.array([-1.,1.,1.])), kn(P0,P0)))
