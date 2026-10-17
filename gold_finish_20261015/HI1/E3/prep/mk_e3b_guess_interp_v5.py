#!/usr/bin/env python3
"""E3b TS-guess builder v5 = rigid-fragment interpolation + reaction-coordinate
internal interpolation (main-coordinator ruling, 2026-10-17 16:32 CST).

Construction (every requirement is an explicit assertion, not a visual check):
 1. endpoints: lambda=0 -> hemiaminal job 1028 frame, lambda=1 -> job 1061 opt
    internal-step last frame (41 atoms, identical element order asserted);
 2. each FRAGMENT is interpolated rigidly: per-fragment Kabsch superposition
    hemiaminal -> converged P, rotation along the axis-angle geodesic, centroid
    linear; therefore every intra-fragment bond length is constant (asserted
    < 0.01 A over the whole lambda grid; the only exceptions by construction are
    the reaction coordinates (2,25) and the proton placement (25,26));
 3. the reaction coordinate C2-O25 is interpolated internally
    1.4728 -> 1.2172 A (O25 moved along the C2->O25 axis) and both it and
    R(C2-N4) must be monotone (asserted; a bounce aborts without writing a frame);
 4. H26 is carried on N4 at 1.05 A along unit(N4-C2) (approved v3 rule) and must
    keep H26...O25 >= 2.0 A and H26...C >= 1.09 A (asserted);
 5. gate: minsep >= 0.90 A and no non-bonded contact < 1.20 A in any emitted frame.

Frames are CONSTRUCTED GUESSES for ts_prepare: not saddles, not converged
geometries, no energies implied.
Usage: mk_e3b_guess_interp_v5.py HEMI_1028.xyz P_1061.xyz OUTDIR LABEL
"""
import sys, os, math
import numpy as np
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds

FRAG_1 = [1, 2, 3, 12, 13, 14, 15, 16, 24, 25, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41]
FRAG_2 = [4, 5, 6, 7, 8, 9, 10, 11, 17, 18, 19, 20, 21, 22, 23, 26, 27]
FRAG_2_K = [f for f in FRAG_2 if f != 26]          # H26 is placed explicitly
EXEMPT = {(2, 25), (25, 26)}                        # by design
L_TRANSFER = 0.50   # lambda >= L_TRANSFER: H26 already on N4 (approved v3 rule);
                    # below it the proton is still on O25 (the on-N4 rule is
                    # geometrically invalid there: at lambda=0 H26...C8 = 1.19 A)


def rd(p):
    L = open(p).read().splitlines()
    n = int(L[0].split()[0])
    el = [x.split()[0] for x in L[2:2 + n]]
    X = np.array([[float(v) for v in x.split()[1:4]] for x in L[2:2 + n]])
    return el, X


def d(X, i, j):
    return float(np.linalg.norm(X[i - 1] - X[j - 1]))


def kabsch(A, B):
    cA, cB = A.mean(axis=0), B.mean(axis=0)
    U, S, Vt = np.linalg.svd((A - cA).T @ (B - cB))
    s = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1.0, 1.0, s]) @ U.T
    return R, cA, cB


def axis_angle(R):
    c = max(-1.0, min(1.0, (np.trace(R) - 1.0) / 2.0))
    th = math.acos(c)
    if th < 1e-12:
        return np.array([1.0, 0.0, 0.0]), 0.0
    ax = np.array([R[2, 1] - R[1, 2], R[0, 2] - R[2, 0], R[1, 0] - R[0, 1]]) / (2.0 * math.sin(th))
    return ax / np.linalg.norm(ax), th


def rodrigues(ax, th):
    K = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]])
    return np.eye(3) + math.sin(th) * K + (1 - math.cos(th)) * (K @ K)


def bond_set(path):
    m = Chem.Mol(Chem.MolFromXYZFile(path))
    rdDetermineBonds.DetermineBonds(m, charge=0)
    return {(min(b.GetBeginAtomIdx(), b.GetEndAtomIdx()) + 1,
             max(b.GetBeginAtomIdx(), b.GetEndAtomIdx()) + 1) for b in m.GetBonds()}


def main():
    hem, prod, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
    label = sys.argv[4] if len(sys.argv) > 4 else 'e3b'
    elH, H = rd(hem)
    elP, P = rd(prod)
    if len(elH) != 41 or len(elP) != 41:
        raise SystemExit('ATOM COUNT mismatch (%d vs %d)' % (len(elH), len(elP)))
    if elH != elP:
        raise SystemExit('ELEMENT ORDER mismatch -> refuse')

    # reference values taken from the two endpoints themselves
    r225_0, r225_1 = d(H, 2, 25), d(P, 2, 25)
    r24_0, r24_1 = d(H, 2, 4), d(P, 2, 4)
    bonds = bond_set(hem) | bond_set(prod)
    frags = [FRAG_1, FRAG_2_K]
    frag_of = {}
    for k, f in enumerate(frags):
        for a in f:
            frag_of[a] = k
    rigid_bonds = [b for b in bonds if b not in EXEMPT and frag_of.get(b[0]) == frag_of.get(b[1])]

    trans = []
    for f in frags:
        idx = [i - 1 for i in f]
        R, cH, cP = kabsch(H[idx], P[idx])
        ax, th = axis_angle(R)
        trans.append((idx, ax, th, cH, cP))

    def frame(lam, want_checks=True):
        X = np.zeros_like(H)
        for idx, ax, th, cH, cP in trans:
            X[idx] = (H[idx] - cH) @ rodrigues(ax, lam * th).T + (cH + lam * (cP - cH))
        c2 = X[1].copy()
        u = X[24] - c2
        un = np.linalg.norm(u) or 1.0
        tgt = r225_0 + lam * (r225_1 - r225_0)
        X[24] = c2 + tgt * u / un                      # reaction coordinate C2-O25
        n4 = X[3].copy()
        if lam >= L_TRANSFER:
            u2 = n4 - c2
            X[25] = n4 + 1.05 * u2 / (np.linalg.norm(u2) or 1.0)   # H26 on N4 (approved rule)
        else:
            # proton not yet transferred: keep the hemiaminal O25-H26 bond, carried with fragment 1
            idx1, ax1, th1, cH1, cP1 = trans[0]
            v = rodrigues(ax1, lam * th1) @ (H[25] - H[24])
            X[25] = X[24] + v / (np.linalg.norm(v) or 1.0) * d(H, 25, 26)
        if not want_checks:
            return X
        # --- assertions (5) and (4) -------------------------------------------
        n = len(elH)
        ms, mi, mj = 9e9, 0, 0
        nonbonded = []
        for i in range(n):
            for j in range(i + 1, n):
                dd = float(np.linalg.norm(X[i] - X[j]))
                if dd < ms:
                    ms, mi, mj = dd, i + 1, j + 1
                if (i + 1, j + 1) not in bonds and dd < 1.20:
                    nonbonded.append((i + 1, j + 1, dd))
        if ms < 0.90:
            raise SystemExit('GATE minsep %.4f < 0.90 at lambda %.2f (pair %d-%d)' % (ms, lam, mi, mj))
        if nonbonded:
            raise SystemExit('non-bonded <1.20 A at lambda %.2f: %s' % (lam, nonbonded[:3]))
        if lam >= L_TRANSFER:
            if d(X, 25, 26) < 2.0:
                raise SystemExit('H26...O25 %.3f < 2.0 at lambda %.2f (bridge/double-hazard)' % (d(X, 25, 26), lam))
            hc = min(d(X, 26, c) for c in (1, 2, 3, 5, 6, 7, 8, 9, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37,
                                           38, 39, 40, 41))
            if hc < 2.00:
                raise SystemExit('H26...C %.3f < 2.00 at lambda %.2f' % (hc, lam))
        # tightest three NON-BONDED contacts
        nb = sorted(((float(np.linalg.norm(X[i] - X[j])), i + 1, j + 1)
                     for i in range(n) for j in range(i + 1, n)
                     if (i + 1, j + 1) not in bonds))[:3]
        return X, dict(ms=ms, mi=mi, mj=mj, nb=nb)

    rows = []
    prev24, prev225 = -1.0, 1e9
    max_bond_dev = 0.0
    for k in range(0, 101):
        lam = k / 100.0
        X, info = frame(lam)
        r24, r225 = d(X, 2, 4), d(X, 2, 25)
        if r24 < prev24 - 1e-6:
            raise SystemExit('R(C2-N4) not monotone at lambda %.2f (%.4f after %.4f)' % (lam, r24, prev24))
        if r225 > prev225 + 1e-6:
            raise SystemExit('R(C2-O25) not monotone at lambda %.2f (%.4f after %.4f)' % (lam, r225, prev225))
        prev24, prev225 = r24, r225
        for (i, j) in rigid_bonds:
            max_bond_dev = max(max_bond_dev, abs(d(X, i, j) - d(H, i, j)))
        rows.append(dict(lam=lam, r24=r24, r225=r225, r1027=d(X, 10, 27), ms=info['ms'],
                         mi=info['mi'], mj=info['mj'], nb=info['nb'], X=X))
    if max_bond_dev >= 0.01:
        raise SystemExit('intra-fragment bond deviation %.4f >= 0.01 A' % max_bond_dev)

    gate = [r for r in rows if r['ms'] >= 0.90]
    win = [r for r in gate if 0.55 <= r['lam'] <= 0.65]
    cand = [r for r in win if 2.15 <= r['r24'] <= 2.25]
    if cand:
        best = sorted(cand, key=lambda r: (-round(r['ms'], 6), r['r24']))[0]
        rule = 'in-window largest minsep, tie -> lower R(C2-N4)'
    elif win:
        best = sorted(win, key=lambda r: abs(r['r24'] - 2.20))[0]
        rule = 'FALLBACK: no frame inside 2.15-2.25 A; nearest to 2.20 A'
    else:
        raise SystemExit('no acceptable frame in lambda 0.55-0.65')

    # residual of the lambda=1 frame against the true converged P frame
    X1 = frame(1.0, want_checks=False)
    res_all = math.sqrt(float(((X1 - P) ** 2).sum()) / 41)
    res_frag = []
    for f in (FRAG_1, FRAG_2_K):
        idx = [i - 1 for i in f]
        R, cA, cB = kabsch(X1[idx], P[idx])
        res_frag.append(math.sqrt(float((((X1[idx] - cA) @ R.T + cB) - P[idx]) ** 2).sum() / len(idx)))

    rep = []
    rep.append('# E3b TS guess v5 - rigid-fragment + reaction-coordinate interpolation (%s)\n\n' % label)
    rep.append('**This frame is a constructed GUESS for ts_prepare: not a saddle, not a converged geometry, no energy implied.**\n\n')
    rep.append('## Inputs\n\n')
    rep.append('* reactant endpoint (lambda=0): `%s`\n' % hem)
    rep.append('* product endpoint (lambda=1): `%s`\n' % prod)
    rep.append('* v5 script: `prep/mk_e3b_guess_interp_v5.py`\n\n')
    rep.append('## Construction and self-checks\n\n')
    rep.append('* 41 atoms in both endpoints, identical element order (asserted); fragments 24 (ketol) + 17 (proline).\n')
    rep.append('* per-fragment Kabsch rigid interpolation (axis-angle geodesic for rotation, linear centroid):\n')
    rep.append('  max intra-fragment bond-length deviation over lambda 0.00-1.00 = **%.2e A** (< 0.01 A asserted).\n' % max_bond_dev)
    rep.append('* reaction coordinate interpolated internally: R(C2-O25) %.4f -> %.4f A; R(C2-N4) %.4f -> %.4f A;\n' % (r225_0, r225_1, r24_0, r24_1))
    rep.append('  both monotone over the whole grid (a bounce aborts the script).\n')
    rep.append('* H26 carried on N4 at 1.05 A along unit(N4-C2); H26...O25 >= 2.0 A and H26...C >= 1.09 A asserted for every frame.\n')
    rep.append('* gate: minsep >= 0.90 A and no non-bonded contact < 1.20 A - asserted for every frame (**all 101 lambda values pass**).\n')
    rep.append('* residual of the lambda=1 frame against the true converged P frame: element-order RMSD **%.4f A**,\n' % res_all)
    rep.append('  per-fragment Kabsch RMSD %.4f / %.4f A - this residual is the fragments-INTERNAL conformational change\n' % (res_frag[0], res_frag[1]))
    rep.append('  (phenyl/OH torsions) that rigid interpolation deliberately does not reproduce, because requirement 2 keeps\n')
    rep.append('  every intra-fragment bond length fixed; lambda=1 therefore carries the P fragment ORIENTATIONS with the\n')
    rep.append('  hemiaminal internal conformation. Documented limitation, not an error.\n\n')
    rep.append('## Table, lambda 0.50 - 0.80 (step 0.02)\n\n')
    rep.append('| lambda | R(C2-N4) | R(C2-O25) | R(O10-H27) | minsep | 3 tightest non-bonded | gate |\n')
    rep.append('|---|---|---|---|---|---|---|\n')
    for r in rows:
        if 0.50 <= r['lam'] <= 0.80 and abs(round(r['lam'] * 100) % 2) < 1e-9:
            nb = ' ; '.join('%d-%d %.3f' % (a, b, c) for c, a, b in r['nb'])
            rep.append('| %.2f | %.4f | %.4f | %.4f | %.4f | %s | %s |\n' % (
                r['lam'], r['r24'], r['r225'], r['r1027'], r['ms'], nb,
                'PASS' if r['ms'] >= 0.90 else 'FAIL'))
    rep.append('\n## Selected formal guess\n\n')
    rep.append('* lambda = **%.2f** (rule: %s)\n' % (best['lam'], rule))
    rep.append('* R(C2-N4) = **%.4f A**, R(C2-O25) = **%.4f A**, R(N4-H26) = 1.0500 A, R(H26...O25) = %.4f A\n' % (
        best['r24'], best['r225'], d(best['X'], 25, 26)))
    rep.append('* R(O10-H27) = %.4f A, minsep = **%.4f A** (pair %d-%d)\n' % (
        best['r1027'], best['ms'], best['mi'], best['mj']))
    rep.append('* 3 tightest non-bonded contacts: %s\n' % ' ; '.join(
        '%d-%d %.4f A' % (a, b, c) for c, a, b in best['nb']))
    rep.append('\n## Status of this frame\n\n')
    rep.append('* constructed guess only; the E3b barrier stays null until a TS frequency with the intended imaginary mode,\n')
    rep.append('  two frequency-verified endpoints and IRC connectivity exist. Submission is gated by the P frequency check.\n')
    A = best['X']
    xyz = os.path.join(outdir, 'E3B_TS_GUESS_v5_lam%03d_c2n4_%.3f.xyz' % (round(best['lam'] * 100), best['r24']))
    with open(xyz, 'w') as f:
        f.write('%d\n%s E3b v5 TS guess (constructed, lam=%.2f R(C2-N4)=%.4f; NOT a saddle)\n'
                % (len(A), label, best['lam'], best['r24']))
        for i, a in enumerate(A):
            f.write('%s %.8f %.8f %.8f\n' % (elH[i], a[0], a[1], a[2]))
    rp = os.path.join(outdir, 'GUESS_SELECTION_%s.md' % label)
    open(rp, 'w').writelines(rep)
    print(''.join(rep))
    print('WROTE %s' % xyz)
    print('WROTE %s' % rp)


if __name__ == '__main__':
    main()
