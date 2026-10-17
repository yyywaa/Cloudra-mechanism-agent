# INT1_27 (carbinolamine_27) — product-side provenance for E1a / denominator for E1b

**Species**: carbinolamine in the reduced 27-atom model ((S)-proline + acetone, C8H15NO3, charge 0, multiplicity 1).
This is the 27-atom projection of the task node **HI1_I1** `CC(C)(O)N1CCC[C@H]1C(=O)O.O=Cc1ccccc1`
after deleting the spectator fragment `.O=Cc1ccccc1` (benzaldehyde, task atom-map labels 5-12).

## 1. The frame
- Path: `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split/INT1_27_opt_frame.xyz`
- sha256: `b2f2ffaaf64169916e29d59fa44a49e223e394e21f69907980b8a83151fa5d36`, 27 atoms, header `opt step=37`
- Exported with `format_converter` (log -> xyz, "extracted final frame (frame 37)"), **no hand-typed coordinates**.
- Element sequence compared position-by-position with `RC_27_opt_frame.xyz` (sha256 `c1f789e0b6653c7de55a291c98f28dd3088f1e6cb3c0124617abecda398f691a`):
  **27/27 identical** (`C C O C H H H H H H O C O C C C C N H H H H H H H H H`), so `atom_map` = identity 1..27.

## 2. Source job (job 1051, INT1_27 Opt+Freq)
- log: `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split/INT1_27_optfreq.log`
  sha256 `c03e0a82d78d22b96474ab48ee40799adb63a894bb9cefcd27c7051799024f63`, 30,757 lines
- input: `INT1_27_optfreq.gjf` sha256 `613d0f90382bc53704d76537042b30317f303ea9178674a3b74691bfa3eee624`
  (route `#p opt freq B3LYP/def2SVP empiricaldispersion=gd3bj int=ultrafine scf=tight scrf=(cpcm,solvent=dmso)`, q0/m1, 8 cpu / 10240 MB)
- start: `INT1_27_start.xyz` sha256 `3c48099cf8e77f2bad7a5379901a23ab68503bdedc620955ae18f1ce0ad91a40` (the -1547.0708 cm-1 proton-transfer saddle frame; used **only** as an optimization start / TS guess, never as a product seed)
- **E(INT1_27) = -593.929762803 Eh**: L26615 ` SCF Done:  E(RB3LYP) =  -593.929762803     A.U. after    7 cycles` (opt, final) and L28142 ` SCF Done:  E(RB3LYP) =  -593.929762803     A.U. after    1 cycles` (freq stage, identical value)
- convergence: L26689 ` Step number  37 out of a maximum of  162`; L26903 `Optimization completed.`; L26904 `   -- Stationary point found.`
- **75 modes = 3N-6 (N=27)**, 25 `Frequencies --` bands; **0 imaginary**: no `imaginary frequencies` line exists anywhere in the log
  (a negative value in the `Low frequencies` line is a translational/rotational pseudo-mode and is not counted);
  L28588 ` Low frequencies ---   -7.9278   -4.0634   -0.0007   -0.0002    0.0005    9.9357` (pseudo-modes)
  **lowest real mode = 78.1490 cm-1**, L28598 ` Frequencies --     78.1490                91.3061              112.9005`
- thermochemistry (recorded only, never used for the electronic barrier): L29511 ` Zero-point correction=                           0.232709 (Hartree/Particle)`
- normal terminations: L27581 ` Normal termination of Gaussian 16 at Sat Oct 17 14:31:05 2026.` (internal step 1 = opt) and
  **L30757 ` Normal termination of Gaussian 16 at Sat Oct 17 14:35:06 2026.`** (whole job, incl. the Freq internal step 2 with route `#P Geom=AllCheck Guess=TCheck SCRF=Check GenCk RB3LYP/def2SVP Freq`, L27585)

## 3. Energy relative to the RC_27 minimum (same batch, pure electronic)
- `E(INT1_27) - E(RC_27) = -593.929762803 - (-593.934532807) = +0.004770004 Eh = +2.99 kcal/mol`
  (RC_27 = job 1044, `RC_27_optfreq.log` sha256 `9d68305052b492c15774082f528f94acf61ffcee9885d8729f020ed1a20589dd`, L11565/L13017)
- This is the **in-model carbinolamine vs RC hydrogen-bonded complex** energy difference. It is **NOT** the E1a barrier:
  the E1a DeltaE-double-dagger requires the TS and is still missing.

## 4. Proton assignment (element-identified from the XYZ, split_contacts.py, 1-based working order)
| quantity | measured | how identified |
|---|---|---|
| C2-O4 | **1.4208 A** | atoms 2-3 |
| C2-N20 | **1.4755 A** | atoms 2-18 |
| O4-H21 (C2-OH) | **0.9699 A** | atoms 3-27 |
| N20...H21 | 2.3798 A | atoms 18-27 |
| nearest H to N20 | **2.0603 A** (H at position 20) | nearest-H search around atom 18 |
| C14-N20 / C17-N20 | 1.4773 / 1.4680 A | ring bonds to N20 |
| carboxyl O13-H19 | **0.9739 A** | nearest H to atom 13 |
| carboxyl C12=O11 / C12-O13 | 1.2102 / 1.3409 A; O11 has no H (nearest H 2.2898 A) | atoms 12-11 / 12-13 |
| C2-C3 / C3-H22 | 1.5351 / 1.1006 A | atoms 2-4 / 4-10 |

**Verdict = case 1 "directly usable"**: N20 is three-coordinate with no H, the carboxyl is an intact COOH (O13-H19)
and C2 carries an OH (O4-H21) - exactly the protonation state of the HI1_I1 node string after deleting `.O=Cc1ccccc1`.
No tautomer double-notation is required. Process readings from the constrained start frame (+38.1 kcal/mol early,
+3.18 kcal/mol at step 31) are superseded by these terminal values and are kept only as process records.

## 5. Model conditions that travel with every number derived from this frame
- Only CPCM(DMSO) continuum; **no explicit solvent, no counterion, no added base**.
- Benzaldehyde is excluded (spectator) and enters no denominator.
- No proton shuttle is included in this 27-atom model; proline COOH acting as a shuttle remains an untested alternative.
- Pure electronic energies from this single Gaussian batch only; no ORCA or historical values are mixed in.
