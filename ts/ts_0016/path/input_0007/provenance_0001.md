# Provenance — E3a TS guess S2 (R(C2-O25) = 1.82 A interpolated frame)

- Source log (absolute): `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/runs/preorg_v3/scan_c2o25_220_160.log`
- Source log sha256: `436c4cd9225bd29c1ae65086e1394b27b886e4d45206f4efa91133b331030f66`
- Frame A: scan point 3 converged region, `Standard orientation` header at line **L25159** (1-based), official scan R(2,25) = 1.89959
- Frame B: scan point 4 converged region, `Standard orientation` header at line **L51856** (1-based), official scan R(2,25) = 1.74959
- Official scan summary: log L59910 (\`Summary of Optimized Potential Surface Scan\`), R7 row at L59911; energies L6225/L16443/L25258/L53388/L59324
- Interpolation: cartesian linear, `lambda = (R3 - R_target)/(R3 - R4) = (1.89959 - 1.82)/(1.89959 - 1.74959) = 0.530600`; `x = (1-lambda)*x_A + lambda*x_B`
- Element order identical in both frames: **yes** (41 atoms, working order = `runs/I2_optfreq/I2_min_v5.xyz` order)
- Output xyz: `/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/prep/guess_c2o25_182/ts_guess_c2o25_182.xyz`
- Output xyz sha256: `e3748c2c6c96af915c63d1fa8972187214916321999720667a68c9b2dd561b9e`

## Key internals (Angstrom)

| pair | frame A (L25159) | frame B (L51856) | S2 (interpolated) |
|---|---|---|---|
| 2 C - 25 O | 1.8996 | 1.7496 | 1.8168 |
| 10 O - 27 H | 1.5015 | 1.0242 | 1.2467 |
| 25 O - 27 H | 1.0317 | 1.5118 | 1.2789 |
| 25 O - 26 H | 0.9693 | 0.9690 | 0.9633 |
| 2 C - 4 N | 1.3308 | 1.3742 | 1.3493 |
| 4 N - 26 H | 3.3761 | 3.2824 | 3.3262 |
| 10 O - 25 O | 2.5201 | 2.5355 | 2.5231 |
| 11 O - 27 H | 3.3985 | 3.1000 | 3.1995 |
| 9 C - 10 O | 1.2655 | 1.3196 | 1.2689 |
| 9 C - 11 O | 1.2480 | 1.2164 | 1.1782 |
| 2 C - 1 C | 1.5277 | 1.5388 | 1.5335 |
| 2 C - 3 C | 1.5082 | 1.5173 | 1.5128 |

## O10 -> every H distance in S2 (Angstrom), with the two parent frames

| H atom | S2 | frame A | frame B |
|---|---|---|---|
| H27 | 1.2467 | 1.5015 | 1.0242 |
| H36 | 2.7028 | 2.6877 | 2.7612 |
| H20 | 3.0747 | 2.7891 | 3.3327 |
| H26 | 3.0829 | 3.0146 | 3.1525 |
| H23 | 3.1511 | 3.2325 | 3.0872 |
| H24 | 3.2138 | 3.2338 | 3.2936 |
| H17 | 3.5265 | 3.4378 | 3.6097 |
| H21 | 3.6184 | 3.4412 | 3.8037 |

## Admissibility self-check

- R(C2-O25) in S2 = **1.8168** (target 1.82) => interpolation reproduced the coordinate.
- R(C2-O25) monotonically ordered: frame A 1.8996 > S2 1.8168 > frame B 1.7496 => **yes**
- Minimum interatomic separation over all 861 pairs in S2 = **0.9633 A** => admissibility (>= 0.9 A) **PASS**
- Bond-length restoration: atom28-H24 interpolated 0.8420 A -> 0.9752 A (mean of the two parent frames, direction kept); pure cartesian interpolation of a rotating O-H shortens the bond.
- Distortion note: distances are nonlinear under cartesian interpolation, so bonded pairs are not exact weighted means. Largest bond distortion: C9-O11 = 1.1782 A (parents 1.2480 / 1.2164); C9-O10 = 1.2689 A (parents 1.2655 / 1.3196). These relax during TS optimisation and are recorded here for transparency.
- No atom added/removed/reordered; composition C15H21NO4, charge 0, multiplicity 1 unchanged.
- Provenance of the path: both frames are relaxed points of the constrained scan `B 2 25 S 4 -0.150` (constraint card log L158) whose starting geometry is the job 961 I2 minimum (`runs/I2_optfreq/I2_min_v5.xyz`, sha 9a6203ff...). No new conformer was constructed.

## Status

- This is a **guess only**: not a saddle, no barrier. E3a dE = missing measurement until a TS is verified.
- S1 backup guess: `prep/guess_c2o25_175/ts_guess_c2o25_175.xyz` sha256 `db055959e7ffe9277f9e71b253c6873574a3c6d7c712c194d9f7916fc5867fd5`
