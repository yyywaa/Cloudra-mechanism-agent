# E1a provided TS guess — provenance (lane1)

**Purpose**: evidence artifact for `ts_prepare(input.guess = {kind: "provided", xyz_path: ...})` for edge HI1_E1a
(RC_27 → carbinolamine_27, 27-atom reduced model: (S)-proline + acetone, C8H15NO3, charge 0, multiplicity 1).

## 1. The guess file
- Path: `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split/INT1_27_start.xyz`
- sha256: `3c48099cf8e77f2bad7a5379901a23ab68503bdedc620955ae18f1ce0ad91a40`, 27 atoms
- Atom order: identical element sequence to `RC_27_opt_frame.xyz` (sha256 `c1f789e0b6653c7de55a291c98f28dd3088f1e6cb3c0124617abecda398f691a`),
  i.e. acetone atoms 1-10 then proline atoms 11-27; the `atom_map` is therefore the identity 1..27.
  Working indices used below: C2 = 2, O4 = 3, C3 = 4, H22 = 10, N20 = 18, H21 = 27,
  Cα = 14, carboxyl C = 12, carboxyl =O = 11, carboxyl -OH O = 13.

## 2. Where the coordinates came from (all artifacts on disk)
1. `/home/ly/Cloudra-mechanism-agent/ts/ts_0008/jobs/declaration_0003/ts_opt/refine.log`
   sha256 `0e726b3287df2413b256312bdba1bd6f1bb73c2f5c106e4c4dd2b0960c693b0b`
   - L159450 ` Step number 165 out of a maximum of  246` (converged ts_opt)
   - L159743 ` Optimization completed.` / L159744 ` Stationary point found.`
   - the last 41-atom `Input orientation` block starts at L159994; its 27-atom subset is this guess.
2. `/home/ly/Cloudra-mechanism-agent/ts/ts_0008/jobs/declaration_0003/frequency/frequency.log`
   sha256 `a5783c38955a630e1b0b8e90a50a51d9953156de219cdd11fa741b6624f11cbc`
   - L1507 ` ******    1 imaginary frequencies (negative Signs) ****** `
   - L1516 ` Frequencies --  -1547.0708                15.9682                22.9832`
   - the imaginary mode is H-dominated on pairs (3,41) 0.932 / (32,41) 0.795 (41-atom order) = (C3,H22)/(N20,H21),
     i.e. N20-H21 proton transfer; a genuine single saddle, **not** a 7-pair merged saddle.
3. Subset construction script: `gold_finish_20261015/HI1/E1/split_build.py` sha256 `0a6b12bb`
   (drops the 14 benzaldehyde rows = 41-atom indices 11-24; keeps 1-10 and 25-41 in order).

## 3. Chemistry of this guess (why it is a legitimate E1a guess)
- C2-O4 = 1.362 A (carbonyl already converted to a single C-O bond)
- C2...N20 = 1.633 A (C-N bond essentially formed)
- N20-H21 = 1.226 A and O4...H21 = 1.334 A (**H21 exactly between N and O**)
- C2-C3 = 1.531 A, C3-H22 = 1.097 A (the E1b pair is untouched here)
=> a late, concerted "amine addition + N-H proton transfer to the carbonyl O" saddle.

## 4. Denominator (E1a)
`RC_27_optfreq.log` sha256 `9d68305052b492c15774082f528f94acf61ffcee9885d8729f020ed1a20589dd`:
E(RC_27) = `-593.934532807` Eh (L11565 opt / L13017 freq), 75 modes = 3N-6, 0 imaginary,
L11841 `Optimization completed.`, L15572 `Normal termination ... 14:07:03 2026`.
The RC_27 minimum is a loose N-H...O=C hydrogen-bonded complex (C2...N20 = 3.757 A, O4...H21 = 2.030 A),
`RC_27_opt_frame.xyz` sha256 `c1f789e0b6653c7de55a291c98f28dd3088f1e6cb3c0124617abecda398f691a`.

## 5. Model conditions / unknowns that travel with any number derived from this guess
- Only CPCM(DMSO) continuum; **no explicit solvent, no counterion, no added base**.
- Benzaldehyde is excluded from the calculation model (spectator); it is **not** part of any denominator.
- The proton that leaves N20 goes to the acetone-derived O4 directly (no proton shuttle in this 27-atom model);
  proline COOH acting as an intramolecular shuttle remains an untested alternative.
- Energies are pure electronic energies from this one Gaussian batch; no ORCA or historical values are mixed in.

## 6. Removed spectator atoms (14) and the 41-atom -> 27-atom correspondence
- Removed fragment = **benzaldehyde = task atom-map labels 5-12 (14 atoms)**: O5, C6 (aldehyde C, carries the aldehyde H),
  aromatic carbons C7,C8,C9,C10,C11,C12 (6 C) and 5 aromatic H on C7-C12 => 8 heavy + 6 H = 14 atoms.
- Remaining 27 atoms are exactly task-map labels **1, 2, 3, 4, 22, 13, 14, 15, 16, 17, 18, 19, 20, 21** (acetone C1/C2/C3/O4 + H22;
  proline =O13, COOH C14, OH O15, C16-C19, N20, H21) together with their hydrogens.
- 41-atom built order -> 27-atom working order (row-level fragment of the full table):

| 41-atom built rows | 27-atom positions | identity (task map label) |
|---|---|---|
| 1, 2, 3, 4 | 1, 2, 3, 4 | map1 CH3 (C1); map2 C2; map4 carbonyl O4; map3 C3 (methylene) |
| 5-7 | 5-7 | three H on C1 |
| 8, 9 | 8, 9 | two H on C3 |
| 10 | 10 | **map22 H22** (the E1b transferring H) |
| 11-24 | dropped | **benzaldehyde maps 5-12 (14 atoms)** |
| 25 | 11 | map13 =O (carboxyl carbonyl O) |
| 26 | 12 | map14 COOH carbon |
| 27 | 13 | map15 OH oxygen |
| 28 | 14 | map16 C-alpha |
| 29, 30, 31 | 15, 16, 17 | map17, map18, map19 ring CH2 |
| 32 | 18 | map20 N |
| 33-40 | 19-26 | proline C-H hydrogens |
| 41 | 27 | **map21 H21** (the N-H proton that moves to O4) |

## 7. Minimum interatomic separation (acceptability check)
- `INT1_27_start.xyz`: minimum pairwise distance over the 27 atoms = **0.9749 A**, between working-order atom 13 (O) and atom 19 (H),
  i.e. the carboxyl O-H bond. Independent measurements agree: Coordinator (direct xyz pairwise minimum, 14:26 CST) and lane1 script
  `gold_finish_20261015/HI1/E1/split_minsep.py` (14:16 CST). >= 0.9 A.
- `RC_27_opt_frame.xyz`: minimum = **0.9737 A**, same atom pair 13(O)-19(H). >= 0.9 A.

## 8. Acceptance criterion for the E1a TS (upgraded by the main coordinator; binding for this lane)
1. exactly **one** imaginary frequency (band table + the `imaginary frequencies` header only; a negative value in the
   `Low frequencies` line is a translational/rotational pseudo-mode and is not a vibrational mode);
2. the imaginary mode must carry **non-negligible displacement on BOTH N20 and C2** (it must not be an almost pure proton transfer),
   and must also displace H21 and O4;
3. if a pure proton-transfer saddle appears (N20/C2 displacement near zero), it corresponds only to the proton-transfer sub-step:
   it must **not** be reported as E1a - report the mode table first, then either use the interpolated early-attack fallback frame
   (RC_27 <-> INT1_27_start, C2...N20 interpolated to 2.10 A with H21 still on N20, plus a new provenance artifact and a
   monotonic-N-C / minsep >= 0.9 A self-check) or split E1a into a further sub-step.

## 9. Qualitative provenance of the high-lying constrained frame (must accompany any number from it)
The intermediate reading +38.1 kcal/mol for the constrained start frame reflects a zwitterion-like arrangement that is stabilised only
by the CPCM(DMSO) continuum once benzaldehyde and the explicit hydrogen-bond partners are removed; it is a process reading, not a
denominator. Consequently the E1a barrier computed here carries the 'N-attack binding/desolvation cost' relative to the loose RC_27
hydrogen-bonded complex, and the E1b denominator is the **in-model** high-lying carbinolamine minimum (or, if job 1051 relaxes back to
the loose complex, E1b has no valid denominator and must be reported as missing).
