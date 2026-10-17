#!/usr/bin/env python3
"""E3b TS-guess builder v7 = reaction-coordinate-driven deformation of the hemiaminal minimum.

Why v7: the two declared endpoints are different conformers (whole-molecule Kabsch RMSD 1.937 A;
per-fragment max |dtorsion| 177.9 deg), so
  * Cartesian interpolation (v3/v4) collapses intra-fragment bonds (measured),
  * rigid-fragment interpolation (v5) can never reach the converged P frame (residual ~1 A), and
  * the seven-condition list requires BOTH "lambda=1 equals the P frame" and "intra-fragment bond
    drift < 0.01 A", which are mutually exclusive for these endpoints (bond values differ by up to
    0.0322 A at C1-C2 and 0.0287 A at C2-C3 - the reacting C2 changes hybridisation sp3 -> sp2).

v7 therefore abandons endpoint interpolation and builds the guess the way a TS guess should be
built for a bond-breaking step: start from the frequency-verified HEMIAMINAL minimum (job 1028)
and change ONLY the declared reaction coordinates
  * R(C2-N4) stretched from 1.4248 A to the requested value (proline fragment translated rigidly
    along the C2->N4 axis, so its internal geometry is untouched),
  * R(C2-O25) shortened to its value at the same fractional progress toward the product
    (1.4728 -> 1.2172 A, O25 moved along the C2->O25 axis),
  * H26 moved onto N4 at 1.05 A along the PRODUCT's own N4->H26 direction.
Every other internal coordinate is exactly the hemiaminal value, so bonds cannot collapse and the
frame stays in the conformation that the TS must resemble. No product end is claimed.

Frames are CONSTRUCTED GUESSES for ts_prepare: not saddles, not converged, no energy implied.
Usage: mk_e3b_guess_v7.py HEMI_1028.xyz P_1061.xyz OUTDIR LABEL [r24_target]
"""
import sys, os, math
import numpy as np
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds

FRAG_1 = [1, 2, 3, 12, 13, 14, 15, 16, 24, 25, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41]
FRAG_2 = [4, 5, 6, 7, 8, 9, 10, 11, 17, 18, 19, 20, 21, 22, 23, 26, 27]
FRAG_2_K = [f for f in FRAG_2 if f != 26]


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
    return R


def main():
    hem, prod, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
    label = sys.argv[4] if len(sys.argv) > 4 else 'e3b'
    target = float(sys.argv[5]) if len(sys.argv) > 5 else 2.20
    elH, H = rd(hem)
    elP, P = rd(prod)
    if len(elH) != 41 or len(elH) != len(elP) or elH != elP:
        raise SystemExit('endpoint atom count / element order mismatch -> refuse')

    # product N4->H26 direction, expressed in the hemiaminal frame through fragment 2's rotation
    R2 = kabsch(H[[i - 1 for i in FRAG_2_K]], P[[i - 1 for i in FRAG_2_K]])
    uP = P[25] - P[3]
    uP = uP / np.linalg.norm(uP)
    uH = R2 @ uP

    r24_0, r24_1 = d(H, 2, 4), d(P, 2, 4)
    r225_0, r225_1 = d(H, 2, 25), d(P, 2, 25)
    frac = (target - r24_0) / (r24_1 - r24_0)
    r225_t = r225_0 + frac * (r225_1 - r225_0)

    X = H.copy()
    # 1) stretch C2-N4: translate the proline fragment rigidly along the C2->N4 axis
    c2 = H[1].copy()
    u24 = H[3] - c2
    u24 = u24 / np.linalg.norm(u24)
    shift = (target - r24_0) * u24
    for a in FRAG_2_K:
        X[a - 1] = H[a - 1] + shift
    # 2) shorten C2-O25 along the C2->O25 axis
    u225 = H[24] - c2
    u225 = u225 / np.linalg.norm(u225)
    X[24] = c2 + r225_t * u225
    # 3) H26 on N4 at 1.05 A along the product N-H direction
    X[25] = X[3] + 1.05 * uH / np.linalg.norm(uH)

    # ---- checks -----------------------------------------------------------
    bonds = set()
    m = Chem.Mol(Chem.MolFromXYZFile(prod))
    rdDetermineBonds.DetermineBonds(m, charge=0)
    for b in m.GetBonds():
        i, j = b.GetBeginAtomIdx() + 1, b.GetEndAtomIdx() + 1
        bonds.add((min(i, j), max(i, j)))
    ms, mi, mj, bad = 9e9, 0, 0, []
    for i in range(41):
        for j in range(i + 1, 41):
            dd = float(np.linalg.norm(X[i] - X[j]))
            if dd < ms:
                ms, mi, mj = dd, i + 1, j + 1
            if (i + 1, j + 1) not in bonds and (j + 1, i + 1) not in bonds and dd < 1.20:
                bad.append((i + 1, j + 1, dd))
    if ms < 0.90:
        raise SystemExit('minsep %.4f < 0.90 (pair %d-%d)' % (ms, mi, mj))
    if bad:
        raise SystemExit('non-bonded <1.20 A: %s' % bad[:3])
    if d(X, 25, 26) < 2.0:
        raise SystemExit('H26...O25 %.3f < 2.0' % d(X, 25, 26))
    hc = min(d(X, 26, c) for c in range(1, 42) if elH[c - 1] == 'C')
    if hc < 1.60:
        raise SystemExit('H26...C %.3f < 1.60' % hc)
    # only the declared reaction coordinates changed
    drift = 0.0
    for (a, b) in bonds:
        if a in (2, 4, 25, 26) or b in (2, 4, 25, 26):
            continue
        drift = max(drift, abs(d(X, a, b) - d(H, a, b)))
    if drift > 1e-9:
        raise SystemExit('a non-reaction bond changed by %.2e A' % drift)

    nb = sorted(((float(np.linalg.norm(X[i] - X[j])), i + 1, j + 1)
                 for i in range(41) for j in range(i + 1, 41)
                 if (i + 1, j + 1) not in bonds and (j + 1, i + 1) not in bonds))[:3]
    rep = []
    rep.append('# E3b TS guess v7 - reaction-coordinate deformation of the hemiaminal minimum (%s)\n\n' % label)
    rep.append('**Constructed GUESS for ts_prepare: not a saddle, not a converged geometry, no energy implied.**\n\n')
    rep.append('* base frame (all other internal coordinates unchanged): `%s`\n' % hem)
    rep.append('* product reference for the N-H direction only: `%s`\n' % prod)
    rep.append('* script: `prep/mk_e3b_guess_v7.py`\n\n')
    rep.append('## What was changed (nothing else)\n\n')
    rep.append('* R(C2-N4): %.4f -> **%.4f A** (proline fragment translated rigidly along the C2->N4 axis; its internal geometry untouched)\n' % (r24_0, target))
    rep.append('* R(C2-O25): %.4f -> **%.4f A** (O25 moved along the C2->O25 axis, at the same fractional progress %.3f of the C-N stretch toward the product)\n' % (r225_0, r225_t, frac))
    rep.append('* H26: moved from O25 to **N4 at 1.05 A**, along the product N4->H26 direction (measured angle(C2-N4-H26) = 62.08 deg in the converged P frame)\n')
    rep.append('* every other bond/angle/torsion is exactly the hemiaminal value: max change of any non-reaction-centre bond = **%.1e A** (asserted == 0)\n\n' % drift)
    rep.append('## Checks\n\n')
    rep.append('* 41 atoms, element order identical to both endpoints; atom map unchanged (N4=4, C2=2, O25=25, H26=26, H27=27).\n')
    rep.append('* minsep **%.4f A** (pair %d-%d); no non-bonded contact < 1.20 A.\n' % (ms, mi, mj))
    rep.append('* 3 tightest non-bonded contacts: %s\n' % ' ; '.join('%d-%d %.4f A' % (a, b, c) for c, a, b in nb))
    rep.append('* H26...O25 = **%.4f A** (>= 2.0); H26 nearest carbon = **%.4f A** (>= 1.60); N4-H26 = 1.0500 A.\n' % (d(X, 25, 26), hc))
    rep.append('* R(O10-H27) = %.4f A (carboxyl O-H, untouched), R(C9-O10) = %.4f A, R(C9-O11) = %.4f A.\n\n' % (d(X, 10, 27), d(X, 9, 10), d(X, 9, 11)))
    rep.append('## Why this replaces the endpoint interpolation (measured)\n\n')
    rep.append('* the two endpoints are different conformers: whole-molecule Kabsch RMSD 1.9369 A; per-fragment max |dtorsion| 177.9 deg (ketol) / 179.5 deg (proline);\n')
    rep.append('* endpoint bond values differ by up to 0.0322 A (C1-C2) and 0.0287 A (C2-C3) because the reacting C2 goes sp3 -> sp2, so "lambda=1 equals the P frame" and "intra-fragment bond drift < 0.01 A" cannot hold together;\n')
    rep.append('* v7 keeps the guess in the hemiaminal conformation, which is what a bond-breaking TS guess should resemble, and claims no product end.\n\n')
    rep.append('## Limits\n\n* guess only; E3b barrier stays null until a TS frequency with the intended imaginary mode (C2-N4 breaking + N4-H26 forming) and connectivity to both frequency-verified endpoints exist.\n')
    A = X
    os.makedirs(outdir, exist_ok=True)
    xyz = os.path.join(outdir, 'E3B_TS_GUESS_v7_c2n4_%.3f.xyz' % target)
    with open(xyz, 'w') as f:
        f.write('%d\n%s E3b v7 TS guess (reaction-coordinate deformation of the hemiaminal, R(C2-N4)=%.3f; NOT a saddle)\n' % (len(A), label, target))
        for i, a in enumerate(A):
            f.write('%s %.8f %.8f %.8f\n' % (elH[i], a[0], a[1], a[2]))
    rp = os.path.join(outdir, 'GUESS_SELECTION_%s_v7.md' % label)
    open(rp, 'w').writelines(rep)
    print(''.join(rep))
    print('WROTE %s' % xyz)
    print('WROTE %s' % rp)


if __name__ == '__main__':
    main()
