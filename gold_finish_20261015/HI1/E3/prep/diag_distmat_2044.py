import math
import numpy as np
exec(open('gold_finish_20261015/HI1/E3/prep/diag_kabsch_validate_2043.py').read().split('# ---------- 1)')[0])

f19 = 'ts/ts_0019/jobs/declaration_0001/ts_opt/refine.log'
fp  = 'gold_finish_20261015/HI1/E3/runs/P_e3b/P_optfreq.log'
f28 = 'gold_finish_20261015/HI1/E3/runs/interm_c160/interm_c160_optfreq.log'
a19,_ = last_geom(f19); ap,_ = last_geom(fp); a28,_ = last_geom(f28)

def distmat(a):
    hv = [i for i in range(len(a)) if a[i][0] != 1]
    X = np.array([a[i][1:] for i in hv])
    n = len(X)
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            D[i,j] = np.linalg.norm(X[i]-X[j])
    return D, hv

for nm, a, b in (('1069 vs P', a19, ap), ('1069 vs 1028', a19, a28), ('P vs 1028', ap, a28)):
    Da, hv = distmat(a); Db, _ = distmat(b)
    iu = np.triu_indices(len(hv), 1)
    dd = np.abs(Da[iu] - Db[iu])
    print('%s: heavy-pair |dD| mean=%.4f max=%.4f (n_pairs=%d)' % (nm, dd.mean(), dd.max(), len(dd)))
print('heavy atom work-order indices (20):', [i+1 for i in hv])
