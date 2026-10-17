#!/usr/bin/env python3
"""E3b TS-guess builder v6 = internal-coordinate interpolation (exact local-frame form).

Difference from v5 (rigid fragments): every bond length AND every atom's direction in a local
orthonormal frame are interpolated, so lambda=0 IS the hemiaminal frame and lambda=1 IS the
converged P frame (asserted), and no bond is compressed (no overshoot of its endpoint bracket).
This is a CHANGE OF CONSTRUCTION relative to the approved v5 and therefore needs the
coordinator's release before a run is created with it.

Endpoint frames are the declared ones only:
  lambda = 0 -> hemiaminal job 1028 last frame
  lambda = 1 -> job 1061 opt internal-step last frame (frequency-verified minimum)
The truncated E3a IRC points (job 1068) are NOT used as endpoints or path points here.

H26 (transferred proton): for lambda >= L_TRANSFER it sits on N4 at 1.05 A along the PRODUCT's
own N4->H26 direction (measured angle(C2-N4-H26) = 62.08 deg; the earlier unit(N4-C2) rule puts
H26 0.948 A from C8 at lambda = 0.50).

Frames are CONSTRUCTED GUESSES for ts_prepare: not saddles, not converged, no energy implied.
Usage: mk_e3b_guess_interp_v6.py HEMI_1028.xyz P_1061.xyz OUTDIR LABEL
"""
import sys, os, math
from collections import deque
import numpy as np
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds

L_TRANSFER = 0.50
REACTION_CENTRE = {2, 4, 25, 26}


def rd(p):
    L = open(p).read().splitlines()
    n = int(L[0].split()[0])
    return [x.split()[0] for x in L[2:2 + n]], np.array([[float(v) for v in x.split()[1:4]] for x in L[2:2 + n]])


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


def graph(path):
    m = Chem.Mol(Chem.MolFromXYZFile(path))
    rdDetermineBonds.DetermineBonds(m, charge=0)
    frags = [sorted(i + 1 for i in f) for f in Chem.GetMolFrags(m)]
    bonds = [(b.GetBeginAtomIdx() + 1, b.GetEndAtomIdx() + 1) for b in m.GetBonds()]
    return frags, bonds


def build_tree(frag, bonds):
    F = set(frag)
    nbr = {i: [] for i in F}
    for a, b in bonds:
        if a in F and b in F:
            nbr[a].append(b); nbr[b].append(a)
    for k in nbr:
        nbr[k].sort()
    root = min(F)
    parent = {root: None}
    order = [root]
    dq = deque([root])
    while dq:
        u = dq.popleft()
        for v in nbr[u]:
            if v not in parent:
                parent[v] = u; order.append(v); dq.append(v)
    seq = []
    for a in order:
        p1 = parent[a]
        p2 = parent[p1] if p1 is not None else None
        p3 = parent[p2] if p2 is not None else None
        seq.append((a, p1, p2, p3))
    return seq


def basis(X, p1, p2, p3):
    a1 = X[p1 - 1] - X[p2 - 1]
    a1 = a1 / np.linalg.norm(a1)
    n = np.cross(X[p2 - 1] - X[p3 - 1], a1)
    n = n / np.linalg.norm(n)
    return a1, np.cross(n, a1), n


def ics(X, el, seq):
    out = {}
    for a, p1, p2, p3 in seq:
        if p1 is None:
            out[a] = None
        elif p2 is None:
            out[a] = (float(np.linalg.norm(X[a - 1] - X[p1 - 1])),)
        elif p3 is None:
            r = float(np.linalg.norm(X[a - 1] - X[p1 - 1]))
            a1 = X[p1 - 1] - X[p2 - 1]
            a1 = a1 / np.linalg.norm(a1)
            pv = np.array([1.0, 0.0, 0.0]) if abs(a1[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
            a2 = np.cross(pv, a1); a2 = a2 / np.linalg.norm(a2)
            a3 = np.cross(a1, a2)
            u = (X[a - 1] - X[p1 - 1]) / r
            out[a] = (r, float(u @ a1), float(u @ a2), float(u @ a3))
        else:
            r = float(np.linalg.norm(X[a - 1] - X[p1 - 1]))
            a1, a2, a3 = basis(X, p1, p2, p3)
            u = (X[a - 1] - X[p1 - 1]) / r
            out[a] = (r, float(u @ a1), float(u @ a2), float(u @ a3))
    return out


def rebuild(ic0, ic1, seq, lam, el):
    X = np.zeros((len(el), 3))
    for a, p1, p2, p3 in seq:
        i0, i1 = ic0[a], ic1[a]
        if p1 is None:
            X[a - 1] = 0.0
            continue
        if p2 is None:
            r = i0[0] + lam * (i1[0] - i0[0])
            X[a - 1] = X[p1 - 1] + np.array([r, 0.0, 0.0])
            continue
        r = i0[0] + lam * (i1[0] - i0[0])
        if p3 is None:
            a1 = X[p1 - 1] - X[p2 - 1]
            a1 = a1 / np.linalg.norm(a1)
            pv = np.array([1.0, 0.0, 0.0]) if abs(a1[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
            a2 = np.cross(pv, a1); a2 = a2 / np.linalg.norm(a2)
            a3 = np.cross(a1, a2)
        else:
            a1, a2, a3 = basis(X, p1, p2, p3)
        comp = np.array([i0[1] + lam * (i1[1] - i0[1]),
                         i0[2] + lam * (i1[2] - i0[2]),
                         i0[3] + lam * (i1[3] - i0[3])])
        u = comp[0] * a1 + comp[1] * a2 + comp[2] * a3
        X[a - 1] = X[p1 - 1] + r * u / (np.linalg.norm(u) or 1.0)
    return X


def main():
    hem, prod, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
    label = sys.argv[4] if len(sys.argv) > 4 else 'e3b'
    elH, H = rd(hem)
    elP, P = rd(prod)
    if len(elH) != 41 or len(elP) != 41 or elH != elP:
        raise SystemExit('endpoint atom count / element order mismatch -> refuse')
    frags, bonds = graph(prod)
    if [len(f) for f in frags] != [24, 17]:
        raise SystemExit('unexpected fragments %s' % [len(f) for f in frags])
    frag_of = {a: k for k, f in enumerate(frags) for a in f}

    trees, ic0, ic1, trans = [], [], [], []
    for f in frags:
        seq = build_tree(f, bonds)
        trees.append(seq)
        ic0.append(ics(H, elH, seq))
        ic1.append(ics(P, elH, seq))
        idx = [i - 1 for i in f]
        R, cA, cB = kabsch(H[idx], P[idx])
        ax, th = axis_angle(R)
        trans.append((idx, ax, th, cA, cB))

    def frame(lam):
        X = np.zeros_like(H)
        for k, f in enumerate(frags):
            Xf = rebuild(ic0[k], ic1[k], trees[k], lam, elH)
            idx = [i - 1 for i in f]
            Rk, cA, cB = kabsch(Xf[idx], H[idx])
            Y = (Xf[idx] - cA) @ Rk.T + cB
            Rl = rodrigues(trans[k][1], lam * trans[k][2])
            cl = trans[k][3] + lam * (trans[k][4] - trans[k][3])
            X[idx] = (Y - trans[k][3]) @ Rl.T + cl
        n4 = X[3].copy()
        if lam >= L_TRANSFER:
            uP = P[25] - P[3]
            uP = uP / np.linalg.norm(uP)
            uH = rodrigues(trans[1][1], -trans[1][2]) @ uP
            u = rodrigues(trans[1][1], lam * trans[1][2]) @ uH
            X[25] = n4 + 1.05 * u / np.linalg.norm(u)
        else:
            v = rodrigues(trans[0][1], lam * trans[0][2]) @ (H[25] - H[24])
            X[25] = X[24] + v / np.linalg.norm(v) * d(H, 25, 26)
        return X

    X0, X1 = frame(0.0), frame(1.0)
    rms0 = math.sqrt(float(((X0 - H) ** 2).sum()) / 41)
    dev1 = float(np.abs(X1 - P).max())
    if rms0 > 1e-3:
        raise SystemExit('lambda=0 frame deviates from the hemiaminal endpoint (RMSD %.5f)' % rms0)
    if dev1 > 0.03:
        raise SystemExit('lambda=1 frame deviates from the converged P frame (max %.4f > 0.03 A)' % dev1)

    end_diff = {}
    for a, b in bonds:
        if frag_of.get(a) == frag_of.get(b):
            end_diff[(a, b)] = abs(d(P, a, b) - d(H, a, b))
    rows = []
    prev24, prev225, overshoot = -1.0, 1e9, 0.0
    for k in range(0, 101):
        lam = k / 100.0
        X = frame(lam)
        r24, r225 = d(X, 2, 4), d(X, 2, 25)
        if r24 < prev24 - 1e-6:
            raise SystemExit('R(C2-N4) not monotone at lambda %.2f' % lam)
        if r225 > prev225 + 1e-6:
            raise SystemExit('R(C2-O25) not monotone at lambda %.2f' % lam)
        prev24, prev225 = r24, r225
        ms, mi, mj, bad = 9e9, 0, 0, []
        for i in range(41):
            for j in range(i + 1, 41):
                dd = float(np.linalg.norm(X[i] - X[j]))
                if dd < ms:
                    ms, mi, mj = dd, i + 1, j + 1
                if (i + 1, j + 1) not in bonds and (j + 1, i + 1) not in bonds and dd < 1.20:
                    bad.append((i + 1, j + 1, dd))
        if ms < 0.90:
            raise SystemExit('GATE minsep %.4f < 0.90 at lambda %.2f (pair %d-%d)' % (ms, lam, mi, mj))
        if bad:
            raise SystemExit('non-bonded <1.20 A at lambda %.2f: %s' % (lam, bad[:3]))
        if lam >= L_TRANSFER:
            if d(X, 25, 26) < 2.0:
                raise SystemExit('H26...O25 %.3f < 2.0 at lambda %.2f' % (d(X, 25, 26), lam))
            hc = min(d(X, 26, c) for c in range(1, 42) if elH[c - 1] == 'C')
            if hc < 1.60:
                raise SystemExit('H26...C %.3f < 1.60 at lambda %.2f' % (hc, lam))
        for (a, b), ed in end_diff.items():
            overshoot = max(overshoot, abs(d(X, a, b) - d(H, a, b)) - ed)
        nb = sorted(((float(np.linalg.norm(X[i] - X[j])), i + 1, j + 1)
                     for i in range(41) for j in range(i + 1, 41)
                     if (i + 1, j + 1) not in bonds and (j + 1, i + 1) not in bonds))[:3]
        rows.append(dict(lam=lam, r24=r24, r225=r225, r1027=d(X, 10, 27), ms=ms, mi=mi, mj=mj,
                         nb=nb, X=X, ring=d(X, 29, 32)))
    if overshoot > 1e-6:
        raise SystemExit('a bond overshoots its endpoint bracket by %.2e A' % overshoot)

    win = [r for r in rows if r['ms'] >= 0.90 and 0.55 <= r['lam'] <= 0.65]
    cand = [r for r in win if 2.15 <= r['r24'] <= 2.25]
    if cand:
        best = sorted(cand, key=lambda r: (-round(r['ms'], 6), r['r24']))[0]
        rule = 'in-window largest minsep, tie -> lower R(C2-N4)'
    elif win:
        best = sorted(win, key=lambda r: abs(r['r24'] - 2.20))[0]
        rule = 'FALLBACK: no frame inside 2.15-2.25 A; nearest to 2.20 A'
    else:
        raise SystemExit('no acceptable frame in lambda 0.55-0.65')

    big = sorted(((v, k) for k, v in end_diff.items()), reverse=True)
    rep = []
    rep.append('# E3b TS guess v6 - internal-coordinate interpolation (%s)\n\n' % label)
    rep.append('**Constructed GUESS for ts_prepare: not a saddle, not a converged geometry, no energy implied.**\n\n')
    rep.append('## Inputs\n\n* reactant endpoint (lambda=0): `%s`\n* product endpoint (lambda=1): `%s`\n* script: `prep/mk_e3b_guess_interp_v6.py`\n* the truncated E3a IRC path (job 1068) is NOT used as endpoint or path reference\n\n' % (hem, prod))
    rep.append('## Self-checks (asserted in code; any failure aborts without writing a frame)\n\n')
    rep.append('* 41 atoms, identical element order, fragments 24 (ketol) + 17 (proline).\n')
    rep.append('* endpoint identity: lambda=0 RMSD vs the hemiaminal frame = **%.2e A**; lambda=1 max per-atom deviation vs the converged P frame = **%.4f A** (< 0.03 A).\n' % (rms0, dev1))
    rep.append('* no bond overshoots its endpoint bracket over lambda 0.00-1.00 (max overshoot %.2e A).\n' % max(overshoot, 0.0))
    rep.append('* intra-fragment bonds whose two endpoint values differ by >= 0.01 A (interpolated monotonically between them; chemically these are the reacting carbon C2 and the O-H bonds):\n')
    for v, k in big:
        if v >= 0.010:
            rep.append('  * %d-%d %s-%s: %.4f -> %.4f A (delta %.4f)\n' % (k[0], k[1], elH[k[0] - 1], elH[k[1] - 1], d(H, k[0], k[1]), d(P, k[0], k[1]), v))
    rep.append('* every other intra-fragment bond varies by less than 0.01 A over the whole grid.\n')
    rep.append('* reaction coordinates: R(C2-O25) %.4f -> %.4f A and R(C2-N4) %.4f -> %.4f A, both monotone over all 101 lambda values.\n' % (d(H, 2, 25), d(P, 2, 25), d(H, 2, 4), d(P, 2, 4)))
    rep.append('* H26: on N4 at 1.05 A along the PRODUCT N4->H26 direction for lambda >= %.2f (converged P: angle(C2-N4-H26) = 62.08 deg, R(C8,H26) = 2.10 A; the former unit(N4-C2) rule gives H26...C8 = 0.948 A at lambda = 0.50). H26...O25 >= 2.0 A and H26...C >= 1.60 A asserted per frame.\n' % L_TRANSFER)
    rep.append('* gate: minsep >= 0.90 A and no non-bonded contact < 1.20 A for all 101 lambda values.\n\n')
    rep.append('## Table, lambda 0.50 - 0.80 (step 0.02)\n\n| lambda | R(C2-N4) | R(C2-O25) | R(O10-H27) | R(O28-C29) | minsep | 3 tightest non-bonded | gate |\n|---|---|---|---|---|---|---|---|\n')
    for r in rows:
        if 0.50 <= r['lam'] <= 0.80 and abs(round(r['lam'] * 100) % 2) < 1e-9:
            nb = ' ; '.join('%d-%d %.3f' % (a, b, c) for c, a, b in r['nb'])
            rep.append('| %.2f | %.4f | %.4f | %.4f | %.4f | %.4f | %s | %s |\n' % (r['lam'], r['r24'], r['r225'], r['r1027'], r['ring'], r['ms'], nb, 'PASS' if r['ms'] >= 0.90 else 'FAIL'))
    rep.append('\n## Selected formal guess\n\n* lambda = **%.2f** (%s)\n' % (best['lam'], rule))
    rep.append('* R(C2-N4) = **%.4f A**, R(C2-O25) = **%.4f A**, R(N4-H26) = 1.0500 A, R(H26...O25) = %.4f A\n' % (best['r24'], best['r225'], d(best['X'], 25, 26)))
    rep.append('* R(O10-H27) = %.4f A, minsep = **%.4f A** (pair %d-%d)\n' % (best['r1027'], best['ms'], best['mi'], best['mj']))
    rep.append('* 3 tightest non-bonded: %s\n' % ' ; '.join('%d-%d %.4f A' % (a, b, c) for c, a, b in best['nb']))
    rep.append('\n## Limits\n\n* guess only. The P endpoint (job 1061) is frequency-verified (117 modes, 0 imaginary, lowest real mode\n  16.6787 cm-1). The E3b barrier stays null until a TS frequency with the intended imaginary mode and\n  connectivity to both endpoints exist.\n')
    A = best['X']
    os.makedirs(outdir, exist_ok=True)
    xyz = os.path.join(outdir, 'E3B_TS_GUESS_v6_lam%03d_c2n4_%.3f.xyz' % (round(best['lam'] * 100), best['r24']))
    with open(xyz, 'w') as f:
        f.write('%d\n%s E3b v6 TS guess (IC interpolation, lam=%.2f R(C2-N4)=%.4f; NOT a saddle)\n' % (len(A), label, best['lam'], best['r24']))
        for i, a in enumerate(A):
            f.write('%s %.8f %.8f %.8f\n' % (elH[i], a[0], a[1], a[2]))
    rp = os.path.join(outdir, 'GUESS_SELECTION_%s.md' % label)
    open(rp, 'w').writelines(rep)
    print(''.join(rep))
    print('WROTE %s' % xyz)
    print('WROTE %s' % rp)


if __name__ == '__main__':
    main()
