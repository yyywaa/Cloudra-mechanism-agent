# E3b TS guess v9 - reaction-coordinate deformation, proton mid-transfer (e3b)

**Constructed GUESS for ts_prepare: not a saddle, not a converged geometry, no energy implied.**

* base frame: `prep/hemiaminal_1028_lastframe.xyz` (frequency-verified hemiaminal minimum, job 1028)
* product reference (progress scale / verification only): `prep/P_1061_optframe.xyz`
* script: `prep/mk_e3b_guess_v9.py`

## Changed coordinates (nothing else)

* R(C2-N4): 1.4248 -> **1.9500 A** (proline fragment rigidly translated along the C2->N4 axis)
* R(C2-O25): 1.4728 -> **1.4300 A** (O25 moved along the C2->O25 axis)
* H26 mid-transfer: **N4-H26 = 3.5374 A, O25-H26 = 1.2500 A** (two-sphere intersection in the C2-O25-N4 plane, solution farther from C2); C2...H26 = 1.6979 A
* every other bond/angle/torsion is exactly the hemiaminal value: max change of a non-reaction-centre bond = **2.2e-16 A**; O10-H27 kept at 0.9949 A (no second proton moves)

## Checks

* 41 atoms, element order identical to both endpoints, map unchanged (N4=4, C2=2, O25=25, H26=26, H27=27)
* minsep **0.9673 A** (pair 24-28); no non-bonded contact < 1.20 A
* 3 tightest non-bonded contacts: 2-26 1.6979 A ; 12-13 1.7563 A ; 19-20 1.7753 A
* H26 nearest carbon: 1.6979 A

## Reference note (for any future barrier)

* the product-reference minimum is job 1061 (41 atoms / 117 modes / 0 imaginary); a slightly lower
  conformer of that basin was reached during the job-1069 ts_opt (~0.154 kcal/mol below job 1061),
  so any E3b barrier must name job 1061 explicitly as the reference and note that difference.
