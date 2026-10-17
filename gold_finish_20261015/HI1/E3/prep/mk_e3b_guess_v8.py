#!/usr/bin/env python3
"""E3b TS-guess builder v8 = reaction-coordinate deformation, proton NOT yet transferred.

Same construction as v7 (base frame = the frequency-verified hemiaminal minimum, job 1028;
only the declared reaction coordinates change; every other internal coordinate is untouched),
with the coordinator's 18:32 CST change:
  * R(C2-N4) = 1.9000 A   (progress p = (1.90-1.4248)/(3.3308-1.4248) = 0.24932)
  * R(C2-O25) = 1.4091 A  (same progress p along 1.4728 -> 1.2172)
  * H26 STAYS on O25 (hemiaminal O25-H26 bond kept, moves with O25) - no proton transfer in the
    guess. v7 (H26 pre-transferred to N4) slid into the product basin, so the proton is left on
    the hydroxyl oxygen here.

Frames are CONSTRUCTED GUESSES for ts_prepare: not saddles, not converged, no energy implied.
Usage: mk_e3b_guess_v8.py HEMI_1028.xyz P_1061.xyz OUTDIR LABEL [r24_target]
"""
import sys, os, math
import numpy as np
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds

FRAG_2_K = [4, 5, 6, 7, 8, 9, 10, 11, 17, 18, 19, 20, 21, 22, 23, 27]


def rd(p):
    L = open(p).read().splitlines()
    n = int(L[0].split()[0])
    return [x.split()[0] for x in L[2:2 + n]], np.array([[float(v) for v in x.split()[1:4]] for x in L[2:2 + n]])


def d(X, i, j):
    return float(np.linalg.norm(X[i - 1] - X[j - 1]))


def main():
    hem, prod, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
    label = sys.argv[4] if len(sys.argv) > 4 else 'e3b'
    target = float(sys.argv[5]) if len(sys.argv) > 5 else 1.90
    elH, H = rd(hem)
    elP, P = rd(prod)
    if len(elH) != 41 or len(elH) != len(elP) or elH != elP:
        raise SystemExit('endpoint atom count / element order mismatch -> refuse')

    r24_0, r24_1 = d(H, 2, 4), d(P, 2, 4)
    r225_0, r225_1 = d(H, 2, 25), d(P, 2, 25)
    p = (target - r24_0) / (r24_1 - r24_0)
    r225_t = r225_0 + p * (r225_1 - r225_0)

    X = H.copy()
    c2 = H[1].copy()
    u24 = H[3] - c2
    u24 = u24 / np.linalg.norm(u24)
    for a in FRAG_2_K:                       # proline fragment: rigid translation only
        X[a - 1] = H[a - 1] + (target - r24_0) * u24
    u225 = H[24] - c2
    u225 = u225 / np.linalg.norm(u225)
    X[24] = c2 + r225_t * u225               # O25 along the C2->O25 axis
    X[25] = X[24] + (H[25] - H[24])          # H26 stays on O25, bond vector unchanged

    m = Chem.Mol(Chem.MolFromXYZFile(prod))
    rdDetermineBonds.DetermineBonds(m, charge=0)
    bonds = set()
    for b in m.GetBonds():
        i, j = b.GetBeginAtomIdx() + 1, b.GetEndAtomIdx() + 1
        bonds.add((min(i, j), max(i, j)))
    bonds.add((2, 25)); bonds.add((25, 26)); bonds.add((2, 4))
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
    drift = 0.0
    for (a, b) in bonds:
        if a in (2, 4, 25, 26) or b in (2, 4, 25, 26):
            continue
        drift = max(drift, abs(d(X, a, b) - d(H, a, b)))
    if drift > 1e-9:
        raise SystemExit('a non-reaction bond changed by %.2e A' % drift)
    if abs(d(X, 25, 26) - d(H, 25, 26)) > 1e-9:
        raise SystemExit('O25-H26 length changed')

    nb = sorted(((float(np.linalg.norm(X[i] - X[j])), i + 1, j + 1)
                 for i in range(41) for j in range(i + 1, 41)
                 if (i + 1, j + 1) not in bonds and (j + 1, i + 1) not in bonds))[:3]
    rep = []
    rep.append('# E3b TS guess v8 - reaction-coordinate deformation, proton NOT transferred (%s)\n\n' % label)
    rep.append('**Constructed GUESS for ts_prepare: not a saddle, not a converged geometry, no energy implied.**\n\n')
    rep.append('* base frame: `%s` (frequency-verified hemiaminal minimum, job 1028)\n' % hem)
    rep.append('* product reference (used only for the progress scale and for verification): `%s`\n' % prod)
    rep.append('* script: `prep/mk_e3b_guess_v8.py`\n\n')
    rep.append('## What was changed (nothing else)\n\n')
    rep.append('* R(C2-N4): %.4f -> **%.4f A** (proline fragment translated rigidly along the C2->N4 axis; internal geometry untouched)\n' % (r24_0, target))
    rep.append('* R(C2-O25): %.4f -> **%.4f A** (same progress p = %.5f as the C-N stretch, O25 moved along the C2->O25 axis)\n' % (r225_0, r225_t, p))
    rep.append('* **H26 stays on O25** at the hemiaminal O25-H26 distance (moves with O25); no proton transfer in this guess - this is the difference from v7\n')
    rep.append('* every other bond/angle/torsion is exactly the hemiaminal value: max change of a non-reaction-centre bond = **%.1e A**\n\n' % drift)
    rep.append('## Checks\n\n')
    rep.append('* 41 atoms, element order identical to both endpoints; map unchanged (N4=4, C2=2, O25=25, H26=26, H27=27).\n')
    rep.append('* minsep **%.4f A** (pair %d-%d); no non-bonded contact < 1.20 A.\n' % (ms, mi, mj))
    rep.append('* 3 tightest non-bonded contacts: %s\n' % ' ; '.join('%d-%d %.4f A' % (a, b, c) for c, a, b in nb))
    rep.append('* R(N4-H26) = **%.4f A** (proton still on O25), R(O25-H26) = %.4f A (hemiaminal value), R(O10-H27) = %.4f A\n' % (d(X, 4, 26), d(X, 25, 26), d(X, 10, 27)))
    rep.append('* R(C2-O25) target vs actual: %.4f / %.4f A; R(C2-N4) target vs actual: %.4f / %.4f A\n\n' % (r225_t, d(X, 2, 25), target, d(X, 2, 4)))
    rep.append('## Limits\n\n* guess only. E3b barrier stays null until a TS frequency with the intended imaginary mode\n  (C2-N4 breaking, N4-H26 forming) and connectivity to both frequency-verified endpoints exist.\n')
    A = X
    os.makedirs(outdir, exist_ok=True)
    xyz = os.path.join(outdir, 'E3B_TS_GUESS_v8_c2n4_%.3f_hnou.xyz' % target)
    with open(xyz, 'w') as f:
        f.write('%d\n%s E3b v8 TS guess (R(C2-N4)=%.3f, R(C2-O25)=%.4f, H26 on O25; NOT a saddle)\n' % (len(A), label, target, r225_t))
        for i, a in enumerate(A):
            f.write('%s %.8f %.8f %.8f\n' % (elH[i], a[0], a[1], a[2]))
    rp = os.path.join(outdir, 'GUESS_SELECTION_%s_v8.md' % label)
    open(rp, 'w').writelines(rep)
    print(''.join(rep))
    print('WROTE %s' % xyz)
    print('WROTE %s' % rp)


if __name__ == '__main__':
    main()
