# E3b TS guess v8 - reaction-coordinate deformation, proton NOT transferred (e3b)

**Constructed GUESS for ts_prepare: not a saddle, not a converged geometry, no energy implied.**

* base frame: `prep/hemiaminal_1028_lastframe.xyz` (frequency-verified hemiaminal minimum, job 1028)
* product reference (used only for the progress scale and for verification): `prep/P_1061_optframe.xyz`
* script: `prep/mk_e3b_guess_v8.py`

## What was changed (nothing else)

* R(C2-N4): 1.4248 -> **1.9000 A** (proline fragment translated rigidly along the C2->N4 axis; internal geometry untouched)
* R(C2-O25): 1.4728 -> **1.4090 A** (same progress p = 0.24933 as the C-N stretch, O25 moved along the C2->O25 axis)
* **H26 stays on O25** at the hemiaminal O25-H26 distance (moves with O25); no proton transfer in this guess - this is the difference from v7
* every other bond/angle/torsion is exactly the hemiaminal value: max change of a non-reaction-centre bond = **4.4e-16 A**

## Checks

* 41 atoms, element order identical to both endpoints; map unchanged (N4=4, C2=2, O25=25, H26=26, H27=27).
* minsep **0.9673 A** (pair 24-28); no non-bonded contact < 1.20 A.
* 3 tightest non-bonded contacts: 12-13 1.7563 A ; 19-20 1.7753 A ; 14-15 1.7768 A
* R(N4-H26) = **3.5675 A** (proton still on O25), R(O25-H26) = 0.9693 A (hemiaminal value), R(O10-H27) = 0.9949 A
* R(C2-O25) target vs actual: 1.4090 / 1.4090 A; R(C2-N4) target vs actual: 1.9000 / 1.9000 A

## Limits

* guess only. E3b barrier stays null until a TS frequency with the intended imaginary mode
  (C2-N4 breaking, N4-H26 forming) and connectivity to both frequency-verified endpoints exist.
