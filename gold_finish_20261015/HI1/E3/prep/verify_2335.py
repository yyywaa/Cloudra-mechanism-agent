import math, numpy as np
# --- 1071 SCF minimum ---
P1 = '/home/ly/Cloudra-mechanism-agent/ts/ts_0020/jobs/declaration_0001/ts_opt/refine.log'
L = open(P1).read().splitlines()
scf = [(i + 1, float(l.split('=')[1].split()[0])) for i, l in enumerate(L) if 'SCF Done' in l]
mn = min(scf, key=lambda x: x[1])
E0 = -939.312626605; EP = -939.319540184
K = 627.509474
print('1071 SCF count = %d  min line = L%d  E = %.9f' % (len(scf), mn[0], mn[1]))
print('   vs 1028 = %+.4f kcal/mol ; vs P = %+.4f kcal/mol' % ((mn[1] - E0) * K, (mn[1] - EP) * K))
print('   snapshot span (max-min over all SCF) = %.4f' % ((max(x[1] for x in scf) - mn[1]) * K))

# --- 1074 Kabsch scan#10 -> scan#11 ---
P2 = 'HI1/E3/runs/e3b_scan2d_c2n4_o25h26.log'
L2 = open(P2).read().splitlines()
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
B = {h: a for h, a in blocks(L2)}
g10 = B[135255]; g11 = B[147582]
def kab(X, Y):
    P = np.array([[x[2], x[3], x[4]] for x in X if x[1] != 1]); Q = np.array([[y[2], y[3], y[4]] for y in Y if y[1] != 1])
    cp = P.mean(0); cq = Q.mean(0)
    Pc = P - cp; Qc = Q - cq
    H = Pc.T @ Qc
    U, S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1, 1, d]) @ U.T
    diff = (R @ Pc.T).T - Qc
    dn = np.linalg.norm(diff, axis=1)
    return math.sqrt(float((dn**2).sum())/len(P)), float(dn.max()), int(dn.argmax())+1, float(np.linalg.det(R))
r = kab(g10, g11)
print('scan#10->#11 heavy20: rms %.4f  max %.4f  worst atom %d  det %.6f' % r)
P0 = np.array([[x[2], x[3], x[4]] for x in g10 if x[1] != 1])
rot = np.array([[0.,-1.,0.],[1.,0.,0.],[0.,0.,1.]]); tt = np.array([2.,1.,-3.])
def kab_np(P, Q):
    Pc = P - P.mean(0); Qc = Q - Q.mean(0)
    U, S, Vt = np.linalg.svd(Pc.T @ Qc)
    d = np.sign(np.linalg.det(Vt.T @ U.T)); R = Vt.T @ np.diag([1,1,d]) @ U.T
    dn = np.linalg.norm((R @ Pc.T).T - Qc, axis=1)
    return math.sqrt(float((dn**2).sum())/len(P))
print('self r+t = %.3e ; mirror = %.4f ; copy = %.3e' % (kab_np(P0, (rot @ P0.T).T + tt), kab_np(P0, P0 * np.array([-1.,1.,1.])), kab_np(P0, P0)))
dE = (-939.266643733 - -939.312626605) * K
print('pt11 dE exact = %.4f kcal/mol' % dE)
