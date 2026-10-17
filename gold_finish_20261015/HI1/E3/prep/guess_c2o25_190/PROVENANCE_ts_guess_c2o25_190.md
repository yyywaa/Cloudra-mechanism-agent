# Provenance — provided TS guess for HI1_E3 (ts_0011), R(C2–O25) = 1.8996 Å frame

Guess file: `gold_finish_20261015/HI1/E3/prep/guess_c2o25_190/ts_guess_c2o25_190.xyz`
sha256 `2568ca035c3ee37dc9472cd86bd3a751547ba835f99332cf8ce2ac91177bb186` (41 atoms).

## 1. Source (raw native log, unchanged)
- `gold_finish_20261015/HI1/E3/runs/preorg_v3/scan_c2o25_220_160.log`
  sha256 `436c4cd9225bd29c1ae65086e1394b27b886e4d45206f4efa91133b331030f66` (60977 lines, job 980)
  - line 87: `# opt=(modredundant,maxstep=10) B3LYP/def2SVP EmpiricalDispersion=GD3B` (+ line 88 `J Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=DMSO)`)
  - line 158: `B       2      25 S   4 -0.150`  (relaxed scan 2.20 → 1.60 Å, 4 steps)
  - line 60977: `Normal termination of Gaussian 16 at Fri Oct 16 01:55:25 2026.`
- 5 converged scan points (SCF Done raw lines) and the scan coordinate from each point's
  `Optimized Parameters` table (raw line of `! R7    R(2,25) ...`):
  | point | SCF Done line | raw energy (a.u.) | R(2,25) line | R(2,25) (Å) | dE vs I2 min (kcal/mol) |
  |---|---|---|---|---|---|
  | 1 | 6225 | `SCF Done:  E(RB3LYP) =  -939.307665623     A.U. after   13 cycles` | 6593 | 2.1996 | +8.15 |
  | 2 | 16443 | `SCF Done:  E(RB3LYP) =  -939.302902987     A.U. after    7 cycles` | 16820 | 2.0496 | +11.14 |
  | 3 | 25258 | `SCF Done:  E(RB3LYP) =  -939.297771992     A.U. after    7 cycles` | 25632 | 1.8996 | +14.36 |
  | 4 | 53388 | `SCF Done:  E(RB3LYP) =  -939.301357590     A.U. after    6 cycles` | 53766 | 1.7496 | +12.11 |
  | 5 | 59324 | `SCF Done:  E(RB3LYP) =  -939.309047571     A.U. after    7 cycles` | 59692 | 1.5996 | +7.28 |
  (reference I2 minimum: `runs/I2_optfreq/I2_optfreq.log` sha256 `63dda25e04529e65920526304fb88755db9393e9c22bd3a6efb76eeee0af0d0e`, line 16950
  `SCF Done:  E(RB3LYP) =  -939.320655479     A.U. after    6 cycles`; 0 imaginary)
- accompanying raw internal coordinates of point 3 (same table): R(2,4) = 1.3308 (line 25631),
  R(10,27) = 1.5015 (25651), R(11,27) = n/a, R(24,28) = 0.9831 (25652), R(25,26) = 0.9693 (25653),
  R(25,27) = 1.0317 (25654).

## 2. Frame extraction and cross-check (tool: `E3/tools/mk_ts_guess_frame.py`, sha256 `246a6da449ea58290693571bcf3e66ab6fba289c91cd5e4c8e915a1c53d33139`)
- `format_converter(log → csv)` on the same log → `runs/preorg_v3/scan_c2o25_220_160_curve.csv`
  ("Detected gaussian opt+scan, wrote 5 frames"); frame with reaction_coordinate 1.89959
  has scf_energy_hartree −939.29777.
- The script locates the matching `Standard orientation` block in the **raw log**:
  header at **line 25159** (coordinates lines 25164–25204); max coordinate deviation
  CSV vs log = **0.00e+00** → the CSV frame *is* the raw-log converged point-3 geometry.
- Element sequence of the frame == `runs/I2_optfreq/I2_min_v5.xyz` (sha256 `9a6203ff67d9f0d95ad774e78b17bc397b22992f24cbcdf448f8c5558142ef2b`) element-by-element,
  and the perceived covalent bond graph is identical **at the same 1-based indices**
  → the frame is already written in the reactant working order; **no reordering was applied**.
- Key distances in the frame (Å): R(1,29)=1.5604, R(2,4)=1.3308, R(2,25)=**1.8996**,
  R(9,10)=1.2655, R(9,11)=1.2480, R(24,28)=0.9831, R(10,27)=**1.5015**, R(11,24)=1.7845,
  R(25,26)=0.9693, R(25,27)=**1.0317**, R(4,26)=3.3761, R(11,27)=3.3985.

## 3. Status / limits of this artifact (do not over-claim)
- This is a **constrained relaxed-scan peak geometry = a TS guess only**. The scan energy
  profile is used **exclusively** for choosing the guess; it is **not** barrier evidence.
- In this frame the water H27 bridges O25 (1.03 Å) and carboxylate O10 (1.50 Å) — i.e. the
  proton site that the constrained path visited is O10, whereas the declared 41-atom
  atom map requires H27 on O11 in the product. O10/O11 are the two carboxylate oxygens
  (C–O 1.2655/1.2480 Å, delocalised); the declared map and reaction_center are left
  untouched, and the unconstrained TS/IRC must resolve the O site. Flagged, not silently
  rewritten.
- At this frame C2–N4 is still only 1.3308 Å and H26 is still on the water (R(4,26)=3.3761):
  the frame is early along the C–N cleavage/proton-shuttle part of the concerted process.
  If the TS search fails from here, the R(2,25)=1.5996 Å frame of the same log (also a
  converged scan point, C2–N4 = 1.4012) is the next documented guess.
