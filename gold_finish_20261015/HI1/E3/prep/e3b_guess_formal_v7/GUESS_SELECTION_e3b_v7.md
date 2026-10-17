# E3b TS guess v7 - reaction-coordinate deformation of the hemiaminal minimum (e3b)

**Constructed GUESS for ts_prepare: not a saddle, not a converged geometry, no energy implied.**

* base frame (all other internal coordinates unchanged): `prep/hemiaminal_1028_lastframe.xyz`
* product reference for the N-H direction only: `prep/P_1061_optframe.xyz`
* script: `prep/mk_e3b_guess_v7.py`

## What was changed (nothing else)

* R(C2-N4): 1.4248 -> **2.2000 A** (proline fragment translated rigidly along the C2->N4 axis; its internal geometry untouched)
* R(C2-O25): 1.4728 -> **1.3688 A** (O25 moved along the C2->O25 axis, at the same fractional progress 0.407 of the C-N stretch toward the product)
* H26: moved from O25 to **N4 at 1.05 A**, along the product N4->H26 direction (measured angle(C2-N4-H26) = 62.08 deg in the converged P frame)
* every other bond/angle/torsion is exactly the hemiaminal value: max change of any non-reaction-centre bond = **2.2e-16 A** (asserted == 0)

## Checks

* 41 atoms, element order identical to both endpoints; atom map unchanged (N4=4, C2=2, O25=25, H26=26, H27=27).
* minsep **0.9673 A** (pair 24-28); no non-bonded contact < 1.20 A.
* 3 tightest non-bonded contacts: 12-13 1.7563 A ; 19-20 1.7753 A ; 14-15 1.7768 A
* H26...O25 = **3.0821 A** (>= 2.0); H26 nearest carbon = **1.8928 A** (>= 1.60); N4-H26 = 1.0500 A.
* R(O10-H27) = 0.9949 A (carboxyl O-H, untouched), R(C9-O10) = 1.3297 A, R(C9-O11) = 1.2137 A.

## Why this replaces the endpoint interpolation (measured)

* the two endpoints are different conformers: whole-molecule Kabsch RMSD 1.9369 A; per-fragment max |dtorsion| 177.9 deg (ketol) / 179.5 deg (proline);
* endpoint bond values differ by up to 0.0322 A (C1-C2) and 0.0287 A (C2-C3) because the reacting C2 goes sp3 -> sp2, so "lambda=1 equals the P frame" and "intra-fragment bond drift < 0.01 A" cannot hold together;
* v7 keeps the guess in the hemiaminal conformation, which is what a bond-breaking TS guess should resemble, and claims no product end.

## Limits

* guess only; E3b barrier stays null until a TS frequency with the intended imaginary mode (C2-N4 breaking + N4-H26 forming) and connectivity to both frequency-verified endpoints exist.
