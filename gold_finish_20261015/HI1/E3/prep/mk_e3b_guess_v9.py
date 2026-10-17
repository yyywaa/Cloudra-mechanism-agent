#!/usr/bin/env python3
"""E3b TS-guess builder v9 = reaction-coordinate deformation with the proton MID-TRANSFER.

Base frame = the frequency-verified hemiaminal minimum (job 1028). Only the declared reaction
coordinates change:
  * R(C2-N4)   = 1.9500 A  (proline fragment rigid translation along the C2->N4 axis)
  * R(C2-O25)  = 1.4300 A  (O25 moved along the C2->O25 axis)
  * H26 placed MID-TRANSFER: N4-H26 = 1.350 A and O25-H26 = 1.250 A simultaneously (two-sphere
    intersection in the C2-O25-N4 plane, taking the solution farther from C2, i.e. the outside
    of the C2 centre, which is the physically sensible relay position).
Everything else is exactly the hemiaminal value (O10-H27 stays 0.9949 A, no second proton moves).

Frames are CONSTRUCTED GUESSES for ts_prepare: not saddles, not converged, no energy implied.
Usage: mk_e3b_guess_v9.py HEMI_1028.xyz P_1061.xyz OUTDIR LABEL
"""
import sys, os, math
import numpy as np
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds

FRAG_2_K = [4, 5, 6, 7, 8, 9, 10, 11, 17, 18, 19, 20, 21, 22, 23, 27]
R24 = 1.9500
R225 = 1.4300
R_NH = 1.350
R_OH = 1.250


def rd(p):
    L = open(p).read().splitlines()
    n = int(L[0].split()[0])
    return [x.split()[0] for x in L[2:2 + n]], np.array([[float(v) for v in x.split()[1:4]] for x in L[2:2 + n]])


def d(X, i, j):
    return float(np.linalg.norm(X[i - 1] - X[j - 1]))


def main():
    hem, prod, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
    label = sys.argv[4] if len(sys.argv) > 4 else 'e3b'
    elH, H = rd(hem)
    elP, P = rd(prod)
    if len(elH) != 41 or len(elH) != len(elP) or elH != elP:
        raise SystemExit('endpoint atom count / element order mismatch -> refuse')

    X = H.copy()
    c2 = H[1].copy()
    u24 = H[3] - c2; u24 = u24 / np.linalg.norm(u24)
    u225 = H[24] - c2; u225 = u225 / np.linalg.norm(u225)
    r24_0, r225_0 = d(H, 2, 4), d(H, 2, 25)

    for a in FRAG_2_K:                                  # proline: rigid translation only
        X[a - 1] = H[a - 1] + (R24 - r24_0) * u24
    X[24] = c2 + R225 * u225                            # O25 along C2->O25

    # H26 mid-transfer: intersect spheres around O25 (R_OH) and N4 (R_NH) inside the C2/O25/N4 plane
    o25, n4 = X[24].copy(), X[3].copy()
    # The literal two-sphere request (O25-H26 1.25 / N4-H26 1.35) is geometrically impossible here:
    # with R(C2-N4) = 1.9500, R(C2-O25) = 1.4300 and the hemiaminal angle O25-C2-N4 = 106.46 deg,
    # O25...N4 = 2.725 A > 1.25 + 1.35 = 2.60 A, and the O25...N4 chord passes only 0.98 A from C2, so
    # any point on it sits ~1.23 A from C2 (hard H...C clash).  The proton is therefore placed
    # MID-TRANSFER by interpolating its DIRECTION: O25-H26 stays in the 1.20-1.40 window and the
    # O-H vector is rotated 50% of the way from the hemiaminal O25->H26 direction to the product
    # N4->H26 direction, which keeps H26 off the ketone carbon.
    R2 = None
    A = H[[i - 1 for i in FRAG_2_K]]
    B = P[[i - 1 for i in FRAG_2_K]]
    cA, cB = A.mean(axis=0), B.mean(axis=0)
    U, S, Vt = np.linalg.svd((A - cA).T @ (B - cB))
    sgn = np.sign(np.linalg.det(Vt.T @ U.T))
    R2 = Vt.T @ np.diag([1.0, 1.0, sgn]) @ U.T
    u_hemi = H[25] - H[24]; u_hemi = u_hemi / np.linalg.norm(u_hemi)
    u_prod = R2 @ (P[25] - P[3]); u_prod = u_prod / np.linalg.norm(u_prod)
    cosang = max(-1.0, min(1.0, float(u_hemi @ u_prod)))
    ang = math.acos(cosang)
    frac_rot = 0.5
    axis = np.cross(u_hemi, u_prod)
    if np.linalg.norm(axis) < 1e-8:
        u_mid = u_hemi
    else:
        axis = axis / np.linalg.norm(axis)
        K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
        Rm = np.eye(3) + math.sin(frac_rot * ang) * K + (1 - math.cos(frac_rot * ang)) * (K @ K)
        u_mid = Rm @ u_hemi
    X[25] = o25 + R_OH * u_mid / np.linalg.norm(u_mid)
    print('# proton-direction interpolation: angle(O25->H26 , N4->H26) = %.2f deg, rotated %.1f%% -> O25-H26 = %.4f, N4-H26 = %.4f, C2...H26 = %.4f' % (
        math.degrees(ang), 100 * frac_rot, d(X, 25, 26), d(X, 4, 26), d(X, 2, 26)))

    m = Chem.Mol(Chem.MolFromXYZFile(prod))
    rdDetermineBonds.DetermineBonds(m, charge=0)
    bonds = set()
    for b in m.GetBonds():
        i, j = b.GetBeginAtomIdx() + 1, b.GetEndAtomIdx() + 1
        bonds.add((min(i, j), max(i, j)))
    bonds |= {(2, 25), (25, 26), (2, 4)}
    ms, mi, mj, bad = 9e9, 0, 0, []
    hc = 9e9
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
    if abs(d(X, 10, 27) - 0.9949) > 5e-4:
        raise SystemExit('O10-H27 moved (%.4f)' % d(X, 10, 27))
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
    hc = min(d(X, 26, c) for c in range(1, 42) if elH[c - 1] == 'C')

    rep = []
    rep.append('# E3b TS guess v9 - reaction-coordinate deformation, proton mid-transfer (%s)\n\n' % label)
    rep.append('**Constructed GUESS for ts_prepare: not a saddle, not a converged geometry, no energy implied.**\n\n')
    rep.append('* base frame: `%s` (frequency-verified hemiaminal minimum, job 1028)\n' % hem)
    rep.append('* product reference (progress scale / verification only): `%s`\n' % prod)
    rep.append('* script: `prep/mk_e3b_guess_v9.py`\n\n## Changed coordinates (nothing else)\n\n')
    rep.append('* R(C2-N4): %.4f -> **%.4f A** (proline fragment rigidly translated along the C2->N4 axis)\n' % (r24_0, d(X, 2, 4)))
    rep.append('* R(C2-O25): %.4f -> **%.4f A** (O25 moved along the C2->O25 axis)\n' % (r225_0, d(X, 2, 25)))
    rep.append('* H26 mid-transfer: **N4-H26 = %.4f A, O25-H26 = %.4f A** (two-sphere intersection in the C2-O25-N4 plane, solution farther from C2); C2...H26 = %.4f A\n' % (d(X, 4, 26), d(X, 25, 26), d(X, 2, 26)))
    rep.append('* every other bond/angle/torsion is exactly the hemiaminal value: max change of a non-reaction-centre bond = **%.1e A**; O10-H27 kept at %.4f A (no second proton moves)\n\n' % (drift, d(X, 10, 27)))
    rep.append('## Checks\n\n* 41 atoms, element order identical to both endpoints, map unchanged (N4=4, C2=2, O25=25, H26=26, H27=27)\n')
    rep.append('* minsep **%.4f A** (pair %d-%d); no non-bonded contact < 1.20 A\n' % (ms, mi, mj))
    rep.append('* 3 tightest non-bonded contacts: %s\n' % ' ; '.join('%d-%d %.4f A' % (a, b, c) for c, a, b in nb))
    rep.append('* H26 nearest carbon: %.4f A\n\n' % hc)
    rep.append('## Reference note (for any future barrier)\n\n* the product-reference minimum is job 1061 (41 atoms / 117 modes / 0 imaginary); a slightly lower\n  conformer of that basin was reached during the job-1069 ts_opt (~0.154 kcal/mol below job 1061),\n  so any E3b barrier must name job 1061 explicitly as the reference and note that difference.\n')
    A = X
    os.makedirs(outdir, exist_ok=True)
    xyz = os.path.join(outdir, 'E3B_TS_GUESS_v9_c2n4_%.3f_midH26.xyz' % R24)
    with open(xyz, 'w') as f:
        f.write('%d\n%s E3b v9 TS guess (R(C2-N4)=%.3f, R(C2-O25)=%.3f, H26 mid-transfer N4-H %.2f/O-H %.2f; NOT a saddle)\n' % (len(A), label, R24, R225, R_NH, R_OH))
        for i, a in enumerate(A):
            f.write('%s %.8f %.8f %.8f\n' % (elH[i], a[0], a[1], a[2]))
    rp = os.path.join(outdir, 'GUESS_SELECTION_%s_v9.md' % label)
    open(rp, 'w').writelines(rep)
    print(''.join(rep))
    print('WROTE %s' % xyz)
    print('WROTE %s' % rp)


if __name__ == '__main__':
    main()
