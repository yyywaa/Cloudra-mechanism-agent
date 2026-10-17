import sys, math, re
import numpy as np

C = 627.5095  # kcal/mol per Hartree

def last_geom(path):
    lines = open(path, 'rb').read().decode('utf-8', 'replace').splitlines()
    start = None
    for i, ln in enumerate(lines):
        if 'Standard orientation:' in ln or 'Input orientation:' in ln:
            start = i
    if start is None:
        raise SystemExit('no orientation block in ' + path)
    atoms = []
    k = start + 5
    closed = False
    while k < len(lines):
        ln = lines[k]
        if ln.strip().startswith('-----'):
            closed = True
            break
        parts = ln.split()
        if len(parts) == 6 and parts[0].isdigit():
            atoms.append((int(parts[1]), float(parts[3]), float(parts[4]), float(parts[5])))
        elif len(parts) != 0:
            raise SystemExit('unexpected line %d: %r' % (k+1, ln[:60]))
        k += 1
    if not closed:
        raise SystemExit('orientation block not closed after line %d' % (start+1))
    return atoms, start+1, k+1, len(lines)

def d(a, i, j):
    return math.dist(a[i-1][1:], a[j-1][1:])

f19 = 'ts/ts_0019/jobs/declaration_0001/ts_opt/refine.log'
fp = 'gold_finish_20261015/HI1/E3/runs/P_e3b/P_optfreq.log'
f1028 = 'gold_finish_20261015/HI1/E3/runs/interm_c160/interm_c160_optfreq.log'

a19, s19, e19, n19 = last_geom(f19)
ap, sp, ep, np_ = last_geom(fp)
a1028, s1028, e1028, n1028 = last_geom(f1028)
print('1069 block L%d..L%d of %d lines, natoms=%d' % (s19, e19, n19, len(a19)))
print('P    block L%d..L%d of %d lines, natoms=%d' % (sp, ep, np_, len(ap)))
print('1028 block L%d..L%d of %d lines, natoms=%d' % (s1028, e1028, n1028, len(a1028)))
assert len(a19) == len(ap) == len(a1028) == 41, 'atom count != 41'
for name, a in (('1069', a19), ('P', ap), ('1028', a1028)):
    print('%s: R(2,4)=%.4f R(2,25)=%.4f R(4,26)=%.4f R(25,26)=%.4f R(10,27)=%.4f R(4,10)=%.4f R(2,26)=%.4f' % (
        name, d(a,2,4), d(a,2,25), d(a,4,26), d(a,25,26), d(a,10,27), d(a,4,10), d(a,2,26)))
print('Z(2,4,25,26,10,27) 1069:', [a19[i-1][0] for i in (2,4,25,26,10,27)])

def kabsch(A, B):
    A = np.array(A); B = np.array(B)
    ca = A.mean(axis=0); cb = B.mean(axis=0)
    H = (A-ca).T @ (B-cb)
    U, S, Vt = np.linalg.svd(H)
    dd = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1.0, 1.0, dd]) @ U.T
    devs = np.linalg.norm((A-ca) @ R.T - (B-cb), axis=1)
    return float(np.sqrt((devs**2).mean())), float(devs.max()), int(devs.argmax())+1

heavy_idx = [i for i, p in enumerate(a19) if p[0] != 1]
H19 = [a19[i][1:] for i in heavy_idx]
HP  = [ap[i][1:] for i in heavy_idx]
H28 = [a1028[i][1:] for i in heavy_idx]
r1, m1, i1 = kabsch(H19, HP)
r2, m2, i2 = kabsch(H19, H28)
print('Kabsch heavy (%d atoms): 1069final vs P    RMSD=%.4f max=%.4f (atom line %d)' % (len(H19), r1, m1, i1))
print('Kabsch heavy (%d atoms): 1069final vs 1028 RMSD=%.4f max=%.4f (atom line %d)' % (len(H19), r2, m2, i2))

E19 = -939.320189491; EP = -939.319540184; E0 = -939.312626605
print('dE(1069final - P)    = %+.6f Ha = %+.2f kcal/mol' % (E19-EP, (E19-EP)*C))
print('dE(1069final - 1028) = %+.6f Ha = %+.2f kcal/mol' % (E19-E0, (E19-E0)*C))
