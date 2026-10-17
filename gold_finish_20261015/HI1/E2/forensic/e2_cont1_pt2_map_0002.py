import math, numpy as np
P = 'HI1/E2/scan_1d/build/E2_1D_scan_cont1.log'
L = open(P).read().splitlines()
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
A = B[3023]; C = B[55204]
def kab_map(X, Y, mask):
    idx = [x[0] for x in X if mask(x)]
    Pm = np.array([[x[2], x[3], x[4]] for x in X if mask(x)])
    Qm = np.array([[y[2], y[3], y[4]] for y in Y if mask(y)])
    Pc = Pm - Pm.mean(0); Qc = Qm - Qm.mean(0)
    U, S, Vt = np.linalg.svd(Pc.T @ Qc)
    d = np.sign(np.linalg.det(Vt.T @ U.T)); R = Vt.T @ np.diag([1,1,d]) @ U.T
    dn = np.linalg.norm((R @ Pc.T).T - Qc, axis=1)
    k = int(dn.argmax())
    return math.sqrt(float((dn**2).sum())/len(Pm)), float(dn.max()), idx[k], len(Pm)
h = kab_map(A, C, lambda x: x[1] != 1)
a = kab_map(A, C, lambda x: True)
print('heavy20: rms %.4f max %.4f worst ORIGINAL atom %d (of %d atoms)' % h)
print('all41  : rms %.4f max %.4f worst ORIGINAL atom %d (of %d)' % a)
# also report top-5 heavy movers with original indices
Pm = np.array([[x[2], x[3], x[4]] for x in A if x[1] != 1]); Qm = np.array([[y[2], y[3], y[4]] for y in C if y[1] != 1])
idx = [x[0] for x in A if x[1] != 1]
Pc = Pm - Pm.mean(0); Qc = Qm - Qm.mean(0)
U, S, Vt = np.linalg.svd(Pc.T @ Qc); d = np.sign(np.linalg.det(Vt.T @ U.T)); R = Vt.T @ np.diag([1,1,d]) @ U.T
dn = np.linalg.norm((R @ Pc.T).T - Qc, axis=1)
order = np.argsort(-dn)[:5]
print('top5 heavy movers:', ['atom %d |d|=%.4f' % (idx[i], dn[i]) for i in order])
