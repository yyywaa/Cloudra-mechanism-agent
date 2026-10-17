# TS seed provenance — lane3 channel B (HI1_EM1, minor_face -> HI1_M1)

Author: HI1 lane3 (S)-system recompute. Created 2026-10-15.
This file is the provenance artifact referenced by `guess.evidence_refs` of the channel-B
durable TS run. It documents only the ORIGIN of the geometry seed. It is NOT QM evidence.

## 1 Seed artifact

- path: `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2EM1/build/TS_guess_EM1_j59f9.xyz`
- sha256: `a7b50b7c23031e9c527ecaad4e08961bcfcec26880cac834b93f6bbfd5f214be`
- 41 atoms, element sequence identical to the ORCA job_51 order used by the (S)-I1 start
  geometry `gold_finish_20261015/HI1/E2EM1/build/I1_S_from_job59.xyz`
  (sha256 `22f730d231bc91c39f73851e62b9d8eba0db6357a7aaeeddab6484226df2e697`).
- declared reaction: `C=C(C)N1CCC[C@H]1C(=O)O.O.O=Cc1ccccc1`
  -> `CC(C[C@@H]([O-])c1ccccc1)=[N+]1CCC[C@H]1C(=O)O.O` (q0/m1), channel B = HI1_EM1 / HI1_M1 (map6 = R).

## 2 Source frame (historical ORCA geometry; energy is NOT used)

- path: `/home/ly/Cloudra-mechanism-agent/gold_compute/grant_materials_20261001/raw/HI1/job_59/scan_minor_clean.009.xyz`
- sha256: `ae2ca403265e2c24bc9036ec36f6c1a001cf59a5f4fffc03460eecbb0e75e0fa`
- what it is: frame 9 of the ORCA job_59 relaxed scan ("minor" directory-name chain),
  d(C3-C6) = 2.800 A, d(C2-N20) = 1.388 A. Historical engine = ORCA 6.1.1; its absolute energy is
  **not** used anywhere in this package (no cross-engine subtraction, BRIEF §3).

## 3 Operation applied (mirror, no permutation)

Coordinates of the source frame were mirrored z -> -z; atom order and element labels unchanged.
Measured over all 41 atoms (same element sequence, numpy max |d|):

    TS_guess_EM1_j59f9.xyz  scan_minor_clean.009.xyz  n=41  maxdev_zmirror=0.000000  maxdev_nomirror=7.805166

Reason for mirroring: the whole historical ORCA HI1 chain is built on (R)-proline geometry
(LEDGER 2026-10-15 L2 identity gap); the mirrored geometry carries the required (S)-proline centre
while leaving all conformer information intact.

## 4 Stereochemical prediction from this seed (GEOMETRY PREDICTION ONLY, not QM evidence)

Method: the seed coordinates are connected with the adduct topology (C3-C6 single bond formed,
iminium C2=N20+, alkoxide C6-O5-), then RDKit `AssignStereochemistryFrom3D` + `rdCIPLabeler`.

    cd /home/ly/Cloudra-mechanism-agent && python3 gold_finish_20261015/HI1/E2EM1/build/dbg_cip_adduct.py \
      gold_finish_20261015/HI1/E2EM1/build/TS_guess_EM1_j59f9.xyz

raw output:

    TS_guess_EM1_j59f9.xyz {8: ('C', [(4, 'N'), (7, 'C'), (9, 'C'), (23, 'H')], 'S'), 29: ('C', [(30, 'C'), (36, 'H'), (1, 'C'), (28, 'O')], 'R')}

(1-based atom 8 = proline C-alpha = map16 -> S; 1-based atom 29 = aldol carbon = map6 -> R.)
Script sha256 `8e7f852f43432519f7c646b32c04a0f4f09a3381bc827ec028de279c7ea47762`.

## 5 Limit of this artifact

The prediction in §4 holds the seed geometry rigid and only reads 3D handedness after forcing the
adduct connectivity. It does **not** prove that the seed is a saddle point, that the IRC connects
(S)-I1 with (S)-proline/(R)-aldol M1, or anything about the barrier. Those claims come only from
this batch's Gaussian 16 ts/IRC/endpoint logs.
