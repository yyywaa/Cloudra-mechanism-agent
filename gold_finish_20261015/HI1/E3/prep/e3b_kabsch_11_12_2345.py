import math, numpy as np
P2 = 'HI1/E3/runs/e3b_scan2d_c2n4_o25h26.log'
L = open(P2).read().splitlines()
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
B = {h: a for h, a in blocks(L)}
def kab(X, Y):
    P = np.array([[x[2], x[3], x[4]] for x in X if x[1] != 1]); Q = np.array([[y[2], y[3], y[4]] for y in Y if y[1] != 1])
    Pc = P - P.mean(0); Qc = Q - Q.mean(0)
    U, S, Vt = np.linalg.svd(Pc.T @ Qc)
    d = np.sign(np.linalg.det(Vt.T @ U.T)); R = Vt.T @ np.diag([1,1,d]) @ U.T
    dn = np.linalg.norm((R @ Pc.T).T - Qc, axis=1)
    return math.sqrt(float((dn**2).sum())/len(P)), float(dn.max()), int(dn.argmax())+1, float(np.linalg.det(R))
print('11->12 heavy20 rms/max/worst/det = %.4f / %.4f / %d / %.6f' % kab(B[147582], B[157138]))
print('10->11 for reference        = %.4f / %.4f / %d / %.6f' % kab(B[135255], B[147582]))
P0 = np.array([[x[2], x[3], x[4]] for x in B[147582] if x[1] != 1])
rot = np.array([[0.,-1.,0.],[1.,0.,0.],[0.,0.,1.]]); tt = np.array([2.,1.,-3.])
def kab_np(P, Q):
    Pc = P - P.mean(0); Qc = Q - Q.mean(0)
    U, S, Vt = np.linalg.svd(Pc.T @ Qc)
    d = np.sign(np.linalg.det(Vt.T @ U.T)); R = Vt.T @ np.diag([1,1,d]) @ U.T
    dn = np.linalg.norm((R @ Pc.T).T - Qc, axis=1)
    return math.sqrt(float((dn**2).sum())/len(P))
print('self r+t=%.3e mirror=%.4f copy=%.3e' % (kab_np(P0,(rot@P0.T).T+tt), kab_np(P0, P0*np.array([-1.,1.,1.])), kab_np(P0,P0)))
