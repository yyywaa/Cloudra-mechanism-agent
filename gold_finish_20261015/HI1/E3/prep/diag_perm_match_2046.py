import math
import numpy as np
try:
    from scipy.optimize import linear_sum_assignment
    HAVE = True
except Exception as e:
    HAVE = False
    print('no scipy:', e)

exec(open('gold_finish_20261015/HI1/E3/prep/diag_kabsch_validate_2043.py').read().split('# ---------- 1)')[0])

f19 = 'ts/ts_0019/jobs/declaration_0001/ts_opt/refine.log'
fp  = 'gold_finish_20261015/HI1/E3/runs/P_e3b/P_optfreq.log'
f28 = 'gold_finish_20261015/HI1/E3/runs/interm_c160/interm_c160_optfreq.log'
a19,_ = last_geom(f19); ap,_ = last_geom(fp); a28,_ = last_geom(f28)

def heavy(a):
    idx = [i for i in range(len(a)) if a[i][0] != 1]
    return np.array([a[i][1:] for i in idx]), [a[i][0] for i in idx], idx

X19, Z19, i19 = heavy(a19); Xp, Zp, ip = heavy(ap); X28, Z28, i28 = heavy(a28)
print('element seqs equal 19/P:', Z19 == Zp, ' 19/1028:', Z19 == Z28)

def dmat(X):
    n = len(X); D = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            D[i,j] = np.linalg.norm(X[i]-X[j])
    return D

def spectrum(X):
    D = dmat(X); iu = np.triu_indices(len(X), 1)
    return np.sort(D[iu])

for nm, A, B in (('1069 vs P', X19, Xp), ('1069 vs 1028', X19, X28), ('P vs 1028', Xp, X28)):
    sa, sb = spectrum(A), spectrum(B)
    print('%s: sorted-distance-spectrum  mean|d|=%.4f  max|d|=%.4f' % (nm, np.abs(sa-sb).mean(), np.abs(sa-sb).max()))

if HAVE:
    def best_map(A, B, za, zb):
        n = len(A)
        cost = np.zeros((n,n))
        for i in range(n):
            for j in range(n):
                cost[i,j] = 1e6 if za[i] != zb[j] else np.linalg.norm(A[i]-B[j])
        r, c = linear_sum_assignment(cost)
        return r, c
    for nm, A, B, za, zb in (('1069 vs P', X19, Xp, Z19, Zp), ('P vs 1028', Xp, X28, Zp, Z28)):
        r, c = best_map(A, B, za, zb)
        same = sum(1 for i, j in zip(r, c) if i == j)
        rms, mx, det = kabsch(A[r], B[c])
        print('%s: element-constrained Hungarian on raw coords -> identity-mapped atoms %d/%d ; Kabsch(perm) RMSD=%.4f max=%.4f' % (nm, same, len(r), rms, mx))
        # distance-profile Hungarian (permutation invariant to rigid motion)
        DA, DB = dmat(A), dmat(B)
        cost = np.zeros_like(DA)
        for i in range(len(A)):
            for j in range(len(A)):
                cost[i,j] = 1e6 if za[i] != zb[j] else np.abs(DA[i]-DB[j]).sum()
        r2, c2 = linear_sum_assignment(cost)
        rms2, mx2, _ = kabsch(A[r2], B[c2])
        print('   distance-profile Hungarian: Kabsch RMSD=%.4f max=%.4f ; mapping(work-order 1-based) %s' % (rms2, mx2, [(i+1, j+1) for i, j in zip(r2, c2)][:8]))
