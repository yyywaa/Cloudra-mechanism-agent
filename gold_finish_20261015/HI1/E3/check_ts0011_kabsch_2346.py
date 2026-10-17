import math, numpy as np
def blocks(path):
    L = open(path).read().splitlines()
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
    return L, out
_, B1 = blocks('ts/ts_0011/jobs/declaration_0004/ts_opt/refine.log')
_, B2 = blocks('ts/ts_0011/jobs/declaration_0004/frequency/frequency.log')
A = B1[-1][1]; B = B2[0][1]
def kab(X, Y):
    P = np.array([[x[2], x[3], x[4]] for x in X if x[1] != 1]); Q = np.array([[y[2], y[3], y[4]] for y in Y if y[1] != 1])
    Pc = P - P.mean(0); Qc = Q - Q.mean(0)
    U, S, Vt = np.linalg.svd(Pc.T @ Qc)
    d = np.sign(np.linalg.det(Vt.T @ U.T)); R = Vt.T @ np.diag([1,1,d]) @ U.T
    dn = np.linalg.norm((R @ Pc.T).T - Qc, axis=1)
    return math.sqrt(float((dn**2).sum())/len(P)), float(dn.max()), int(dn.argmax())+1, float(np.linalg.det(R))
print('elementary seq identical:', [a[1] for a in A] == [b[1] for b in B], 'n', len(A), len(B))
print('ts_opt_last vs freq_first heavy20: rms %.4f max %.4f worst %d det %.6f' % kab(A, B))
P = np.array([[x[2], x[3], x[4]] for x in A if x[1] != 1])
print('raw (no superposition) max|delta| = %.2f A  <-- orientation differs, not a geometry difference' % float(np.max(np.linalg.norm(P - np.array([[y[2], y[3], y[4]] for y in B if y[1] != 1]), axis=1))))
