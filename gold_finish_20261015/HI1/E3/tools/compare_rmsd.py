#!/usr/bin/env python3
"""compare two Gaussian opt/freq logs (or xyz files): last-frame energies, dE in kcal/mol,
element-order RMSD (no rotation) + Kabsch-aligned RMSD + max deviation + per-atom outliers.

Usage:
  compare_rmsd.py LOG_A LOG_B            # logs (last SCF Done + last Standard orientation frame)
  compare_rmsd.py A.xyz B.xyz            # xyz files
Both structures must have identical atom count and identical element order; a mismatch is an
error (never silently reorder).  Hartree->kcal/mol = 627.5094740631 (CODATA-consistent value
already used in this lane's tables).
"""
import sys, math

HARTREE2KCAL = 627.5094740631

def read_last_xyz_from_log(path):
    lines = open(path, errors='replace').read().splitlines()
    # last Standard orientation / Input orientation block
    idx = None
    for i, l in enumerate(lines):
        if 'Standard orientation:' in l or 'Input orientation:' in l:
            idx = i
    if idx is None:
        raise SystemExit('no orientation block in %s' % path)
    atoms = []
    i = idx + 5
    while i < len(lines):
        t = lines[i].split()
        if len(t) != 6:
            break
        try:
            int(t[0]); int(t[1]); int(t[2])
            atoms.append((int(t[1]), float(t[3]), float(t[4]), float(t[5])))
        except ValueError:
            break
        i += 1
    return atoms

def read_xyz(path):
    L = open(path, errors='replace').read().splitlines()
    n = int(L[0].split()[0])
    out = []
    for k in range(n):
        t = L[2 + k].split()
        out.append((t[0], float(t[1]), float(t[2]), float(t[3])))
    return out

Z = {'H': 1, 'C': 6, 'N': 7, 'O': 8, 'F': 9, 'S': 16, 'Cl': 17}

def last_energy(path):
    e = None; ln = None
    for i, l in enumerate(open(path, errors='replace'), 1):
        if 'SCF Done' in l:
            for tok in l.replace('=', ' ').split():
                try:
                    v = float(tok)
                except ValueError:
                    continue
                if -1.0e4 < v < 0.0:
                    e = v; ln = i
    return e, ln

def rmsd_direct(A, B):
    n = len(A)
    s = sum((A[i][1] - B[i][1]) ** 2 + (A[i][2] - B[i][2]) ** 2 + (A[i][3] - B[i][3]) ** 2 for i in range(n))
    return math.sqrt(s / n)

def kabsch_rmsd(A, B):
    n = len(A)
    ca = [sum(a[k] for a in A) / n for k in (1, 2, 3)]
    cb = [sum(b[k] for b in B) / n for k in (1, 2, 3)]
    P = [[a[k] - ca[k - 1] for k in (1, 2, 3)] for a in A]
    Q = [[b[k] - cb[k - 1] for k in (1, 2, 3)] for b in B]
    # rotation matrix via Kabsch (SVD-free: use numpy if available)
    try:
        import numpy as np
        Pn = np.array(P); Qn = np.array(Q)
        H = Pn.T @ Qn
        U, S, Vt = np.linalg.svd(H)
        d = 1.0 if np.linalg.det(Vt.T @ U.T) > 0 else -1.0
        D = np.diag([1.0, 1.0, d])
        R = Vt.T @ D @ U.T
        Pn = Pn @ R.T
        return float(np.sqrt(((Pn - Qn) ** 2).sum() / n)), [float(x) for x in Pn.round(8).tolist()]
    except Exception:
        return None, None

def load(path):
    if path.lower().endswith('.xyz'):
        at = read_xyz(path)
        return [(Z.get(a[0], 0), a[1], a[2], a[3]) for a in at], [a[0] for a in at], None, None
    atoms = read_last_xyz_from_log(path)
    syms = [None] * len(atoms)
    return atoms, syms, None, None

def main():
    pa, pb = sys.argv[1], sys.argv[2]
    A, symA, _, _ = load(pa)
    B, symB, _, _ = load(pb)
    if len(A) != len(B):
        raise SystemExit('ATOM COUNT MISMATCH %d vs %d -> refuse' % (len(A), len(B)))
    if [a[0] for a in A] != [b[0] for b in B]:
        raise SystemExit('ELEMENT ORDER MISMATCH -> refuse (no silent reordering)')
    print('atoms %d, element order identical: True' % len(A))
    for tag, p in (('A', pa), ('B', pb)):
        if p.lower().endswith('.log'):
            e, ln = last_energy(p)
            print('E_%s = %s Eh (line %s)' % (tag, e, ln))
    ea, _ = (last_energy(pa) if pa.lower().endswith('.log') else (None, None))
    eb, _ = (last_energy(pb) if pb.lower().endswith('.log') else (None, None))
    if ea is not None and eb is not None:
        print('dE(B-A) = %+.6f kcal/mol' % ((eb - ea) * HARTREE2KCAL))
        print('dE(B-A) = %+.9f Eh' % (eb - ea))
    print('RMSD (element-order, no rotation) = %.6f A' % rmsd_direct(A, B))
    kr, _ = kabsch_rmsd(A, B)
    if kr is not None:
        print('RMSD (Kabsch, best-fit)            = %.6f A' % kr)
    devs = sorted(((math.dist(A[i][1:], B[i][1:]), i + 1) for i in range(len(A))), reverse=True)
    print('max per-atom |d| = %.4f A (atom %d); top5: %s' % (devs[0][0], devs[0][1],
          ', '.join('atom%d %.3f' % (i, d) for d, i in devs[:5])))

if __name__ == '__main__':
    main()
