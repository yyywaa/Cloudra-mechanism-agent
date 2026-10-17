# TS seed provenance — lane3 channel A (HI1_E2, major_face -> HI1_I2)

Author: HI1 lane3 (S)-system recompute. Created 2026-10-15.
This file is the provenance artifact referenced by `guess.evidence_refs` of the channel-A
durable TS run. It documents only the ORIGIN of the geometry seed. It is NOT QM evidence.

## 1 Seed artifact

- path: `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2EM1/build/TS_guess_E2_j58f7.xyz`
- sha256: `9e5ccc2fe5dde2e4c1900ad53cc8c1ddbae0e654a618c138adaffa58dd522e38`
- 41 atoms, element sequence identical to the ORCA job_51 order used by the (S)-I1 start
  geometry `gold_finish_20261015/HI1/E1/build/I1_S_start.xyz`
  (sha256 `c9d59aeab418c248629922ee37d4ea3822c64b7128dd63b3034d3c8c5ec2df3d`).
- declared reaction: `C=C(C)N1CCC[C@H]1C(=O)O.O.O=Cc1ccccc1`
  -> `CC(C[C@H]([O-])c1ccccc1)=[N+]1CCC[C@H]1C(=O)O.O` (q0/m1), channel A = HI1_E2 / HI1_I2 (map6 = S).

## 2 Source frame (historical ORCA geometry; energy is NOT used)

- path: `/home/ly/Cloudra-mechanism-agent/gold_compute/grant_materials_20261001/raw/HI1/job_58/scan_clean_np8.007.xyz`
- sha256: `e662627fe9d91cc7822961c1a26a4f3f8e08863af9e5f394ef2c7fab8e8f6a36`
- what it is: frame 7 of the ORCA job_58 relaxed scan of d(C3-C6) ("major" directory-name chain),
  d(C3-C6) = 2.275 A, d(C2-N20) = 1.358 A. Historical engine = ORCA 6.1.1; its absolute energy is
  **not** used anywhere in this package (no cross-engine subtraction, BRIEF §3).

## 3 Operation applied (mirror, no permutation)

Coordinates of the source frame were mirrored z -> -z; atom order and element labels unchanged.
Measured over all 41 atoms (same element sequence, numpy max |d|):

    TS_guess_E2_j58f7.xyz  scan_clean_np8.007.xyz  n=41  maxdev_zmirror=0.000000  maxdev_nomirror=10.999726

Reason for mirroring: the whole historical ORCA HI1 chain is built on (R)-proline geometry
(LEDGER 2026-10-15 L2 identity gap); the mirrored geometry carries the required (S)-proline centre
while leaving all conformer information intact.

## 4 Stereochemical prediction from this seed (GEOMETRY PREDICTION ONLY, not QM evidence)

Method: the seed coordinates are connected with the adduct topology (C3-C6 single bond formed,
iminium C2=N20+, alkoxide C6-O5-), then RDKit `AssignStereochemistryFrom3D` + `rdCIPLabeler`.

    cd /home/ly/Cloudra-mechanism-agent && python3 gold_finish_20261015/HI1/E2EM1/build/dbg_cip_adduct.py \
      gold_finish_20261015/HI1/E2EM1/build/TS_guess_E2_j58f7.xyz

raw output:

    TS_guess_E2_j58f7.xyz {8: ('C', [(4, 'N'), (7, 'C'), (9, 'C'), (23, 'H')], 'S'), 29: ('C', [(30, 'C'), (36, 'H'), (1, 'C'), (28, 'O')], 'S')}

(1-based atom 8 = proline C-alpha = map16 -> S; 1-based atom 29 = aldol carbon = map6 -> S.)
Script sha256 `8e7f852f43432519f7c646b32c04a0f4f09a3381bc827ec028de279c7ea47762`.

## 5 Limit of this artifact

The prediction in §4 holds the seed geometry rigid and only reads 3D handedness after forcing the
adduct connectivity. It does **not** prove that the seed is a saddle point, that the IRC connects
(S)-I1 with (S)-I2, or anything about the barrier. Those claims come only from this batch's
Gaussian 16 ts/IRC/endpoint logs.
